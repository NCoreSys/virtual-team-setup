# VTT.WORKFLOW-MAN-001.003 — Generar Task Manifest v1.0

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-MAN-001.003` |
| **Pertenece a** | `VTT.PROTOCOL-MAN-001` §5.3 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-17 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | Agente ejecutor (BE/DB/FE/DO/QA/DL/UX/AR/SA) |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-MAN-001 §5.3.2 (que a su vez corresponde a PROTOCOL-ASG-001 §5.3.9) |
| **Schema del manifest** | v1.2 (definido en `SKL-MAN-001 §Esquema`) |

---

## 1. Propósito

Generar el **Task Manifest v1.0** que el agente ejecutor sube como attachment `fileType=manifest` al cierre de su entrega. Este JSON captura toda la metadata estructurada de la tarea (qué se hizo, qué archivos se tocaron, qué CAs pasaron, qué devlog se generó, qué tech_debt quedó pendiente) y es la fuente para el v1.5 que generará el TL.

> **Regla crítica PROC-MANIFEST-01:** este Workflow se ejecuta AL FINAL del workflow del agente (paso 15 de 15). NUNCA antes de completar attachments + status `task_in_review` + PRs. Si se ejecuta prematuramente, quedan campos null en `delivery.*` y el TL rechaza el cierre.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_id` | string (MS-XXX) | Execution Manifest leído en .002 | sí | ID externo de la tarea |
| `agent_uuid` | uuid | Operativo del agente | sí | UUID del agente para `delivery.delivered_by` |
| `report_path` | path | Generado en paso 14 del agente | sí | Reporte SKL-REPORT-01 en disco — fuente de campos narrativos |
| `vtt_token` | JWT | `SKL-AUTH-01` | sí | Para GETs a VTT |
| `vtt_report_comment_id` | uuid | Posteo del extracto del reporte | sí | El comment-extracto ya posteado en VTT |
| `phase` | string (ej. `04-development`) | Convención del proyecto | sí | Para construir path local del manifest |
| `sprint` | string (ej. `S01`) | Convención del proyecto | sí | Para construir path local del manifest |

---

## 3. Precondiciones (las 8 sagradas)

Antes de ejecutar este Workflow, **TODAS** estas deben cumplirse:

1. ✅ Reporte SKL-REPORT-01 guardado como archivo local en `knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md`
2. ✅ Extracto del reporte posteado como comment en VTT (`vtt_report_comment_id` disponible)
3. ✅ Devlog subido como attachment `fileType=devlog`
4. ✅ Code Logic subido (real o placeholder `N/A`) como attachment `fileType=code_logic`
5. ✅ Status de la tarea moveado a `task_in_review` (`PATCH /api/tasks/<TASK_ID>/status`)
6. ✅ PR(s) creados en GitHub con URL específica (`pr_url`, `pr_number`, `commit_sha`)
7. ✅ CAs reportados con `PATCH /api/tasks/<TASK_ID>/criteria/<cid>` con `{status:"met", evidence}`
8. ✅ Review Gate verificado (`canProceedToReview=true`)

**Si CUALQUIERA falta → STOP. Completar lo faltante. NO ejecutar este Workflow.**

> Caso histórico que originó esta regla: MS-284 tuvo 10+ campos null porque el manifest se generó antes de completar attachments.

---

## 4. Reglas del Workflow

- **R1:** **Manifest AL FINAL** — las 8 precondiciones se verifican primero. Si falta una → STOP.
- **R2:** **No inventar valores** — todos los IDs (attachment_id, comment_id, commit_sha) se obtienen vía GET a VTT/GitHub. NO hardcodear.
- **R3:** **`review.tl_review` queda null** — es del TL, no tocar.
- **R4:** **Wrappear en .md** — VTT no acepta `application/json` puro. Subir como `<TASK_ID>.manifest.md` con bloque ` ```json `.
- **R5:** **Schema v1.2** — todos los campos del schema están especificados en `SKL-MAN-001 §Esquema`. NO desviarse.
- **R6:** **Si DevOps → bloque `operations`** — tareas con `task.category ∈ [deployment, devops, operation, sql_migration, rollback, smoke_test, config_change, restart_service]` requieren `delivery.operations` poblado.
- **R7:** **Campos `null` con `note`** — si `brief`, `assignment` o `delivery.git` son null (DevOps típico), agregar `note` explicando POR QUÉ.

---

## 5. Pasos

### Paso 1 — Verificar las 8 precondiciones

Ejecutar checks contra VTT y filesystem:

```bash
# 1. Reporte local existe
ls knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md

# 2-4. Attachments en VTT
curl -s "$BASE/api/tasks/<TASK_ID>/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(.fileType) | sort | unique'
# Esperado: incluye "brief", "assignment", "devlog", "code_logic"

# 5. Status correcto
curl -s "$BASE/api/tasks/<TASK_ID>" -H "Authorization: Bearer $TOKEN" | \
  jq '.data.statusCode'
# Esperado: "task_in_review"

# 6. PR creado (verificar manualmente o vía gh CLI)
gh pr view <PR_NUM> --json url,number,headRefOid

# 7. CAs reportados
curl -s "$BASE/api/tasks/<TASK_ID>/criteria" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(.status) | unique'
# Esperado: ["met"]

# 8. Review Gate
curl -s "$BASE/api/tasks/<TASK_ID>" -H "Authorization: Bearer $TOKEN" | \
  jq '.data.reviewGate.canProceedToReview'
# Esperado: true
```

¿Todas las 8 OK? →
- **NO** → completar las faltantes, regresar a Paso 1
- **SÍ** → continuar

### Paso 2 — Recolectar IDs reales desde VTT

→ invoca **`VTT.SKILL-MAN-001`** con (`action=fetch_vtt_data`, `task_id=<TASK_ID>`, `version=1.0`)

Endpoints consultados internamente:
- `GET /api/tasks/<TASK_ID>` → metadata, status, sprint, assignee, category, dependencies
- `GET /api/tasks/<TASK_ID>/criteria` → CAs con sus IDs y status
- `GET /api/tasks/<TASK_ID>/devlog` → entries para llenar `devlog_entries[]`
- `GET /api/tasks/<TASK_ID>/attachments` → IDs de brief, assignment, devlog, code_logic
- `GET /api/tasks/<TASK_ID>/comments` → ID del comment SKL-REPORT-01 extracto
- `GET /api/tasks/<TASK_ID>/trackable-items` → TIs vinculados (implements, related_to)

Output: estructura de datos en memoria con todos los IDs reales.

### Paso 3 — Extraer campos narrativos del reporte local

→ invoca **`VTT.SKILL-MAN-001`** con (`action=parse_report`, `report_path=<report_path>`)

Mapeo del reporte a campos del manifest (ver `SKL-MAN-001 §Mapeo report→manifest`):

| Sección del reporte | Campo del manifest |
|---|---|
| `Lo que se hizo:` | `delivery.what_was_done` |
| `Código:` (lista de archivos) | `delivery.deliverables_actual[].{path, state, what}` |
| `Development Log:` | `delivery.development_log_path` |
| `Code Logic:` | `delivery.code_logic_files[]` |
| `Criterios de aceptación:` | `delivery.criteria_results[]` + `delivery.criteria_summary` |
| `Devlog entries registrados en VTT:` | `delivery.devlog_entries[]` + `delivery.devlog_summary` |
| `Findings / Deuda técnica:` | `delivery.findings` |
| `ADRs tomados:` | `delivery.adrs_taken` |
| `TrackableItems creados o vinculados:` | `delivery.trackable_items_actual` |
| `Items detectados para trackeo:` | `delivery.items_detected_for_tl_review[]` |
| `Tareas derivadas generadas:` | `delivery.derived_tasks` |
| `Cómo verificar:` | `delivery.how_to_verify[]` |
| `Notas:` | `delivery.notes` |
| `Review gate al entregar:` | `delivery.review_gate` |
| `Commit:` | `delivery.git.{commit_sha, commit_message}` |
| `PR:` | `delivery.git.{pr_url, pr_number}` |

### Paso 4 — Si DevOps, llenar bloque `operations`

¿`task.category` ∈ `[deployment, devops, operation, sql_migration, rollback, smoke_test, config_change, restart_service]`? →
- **SÍ** → poblar `delivery.operations` con `{type, executed_at, executed_by, environment, sql_applied, commands_applied, pre_checks, post_checks_passed, post_checks_details, issue_resolved, rollback_plan, rejection_history}`
- **NO** → omitir el bloque

→ invoca **`VTT.SKILL-MAN-001`** con (`action=add_operations_block`) — solo si aplica

### Paso 5 — Componer el JSON v1.0

→ invoca **`VTT.SKILL-MAN-001`** con (`action=compose`, `version=1.0`, datos de pasos 2-4)

Estructura mínima (ver `SKL-MAN-001 §Esquema v1.0` para el detalle completo):

```json
{
  "schema_version": "1.2",
  "manifest_id": "<TASK_ID>",
  "generated_at": "<ISO timestamp UTC>",
  "generated_by": "<AGENT_UUID>",
  "generation_note": "v1.0 generado por agente al cerrar workflow. TL Reviewer agregara review.tl_review en v1.5.",

  "task": { ... },
  "brief": { "vtt_attachment_id": "...", "file_path": "..." },
  "assignment": { "vtt_attachment_id": "...", "file_path": "..." },
  "agent_message": { ... },

  "delivery": {
    "delivered_at": "<ISO>",
    "delivered_by": "<AGENT_UUID>",
    "vtt_report_comment_id": "<uuid>",
    "report_file_path": "<report_path>",
    "what_was_done": "...",
    "deliverables_actual": [...],
    "vtt_attachments": { ... },
    "criteria_results": [...],
    "devlog_entries": [...],
    "review_gate": { ... },
    "git": { ... }
  },

  "review": {
    "tl_review": null,
    "pm_approval": null
  },

  "indexes": {
    "implements_codes": [...],
    "deliverables_paths": [...]
  }
}
```

### Paso 6 — Validar v1.0

→ invoca **`VTT.SKILL-MAN-001`** con (`action=validate`, `version=1.0`)

Validaciones obligatorias (aborts del script):

| Validación | Condición de fallo |
|---|---|
| Schema version correcto | `schema_version != "1.2"` |
| `what_was_done` poblado | vacío o < 20 chars |
| Al menos 1 deliverable | `deliverables_actual.length == 0` |
| Cada deliverable tiene `what` | algún elemento sin `what` |
| `report_file_path` existe en disco | archivo no existe |
| `vtt_report_comment_id` presente | null |
| `vtt_attachments.devlog_id` presente | null |
| `review_gate.canProceedToReview=true` | false |
| `git.pr_url` presente (o `note` si DevOps) | null sin note |
| `indexes.deliverables_paths` espeja `deliverables_actual[].path` | mismatch |
| `review.tl_review === null` | poblado por error |
| Si DevOps → `delivery.operations` presente | falta el bloque |
| Si null intencional → `note` explicativo | null sin note |

¿Validación OK? →
- **NO** → leer el mensaje de error, corregir y volver al Paso 5
- **SÍ** → continuar

### Paso 7 — Guardar copia local

```
knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json
```

→ invoca **`VTT.SKILL-MAN-001`** con (`action=save_local`)

### Paso 8 — Wrappear en .md para upload

VTT no acepta `application/json` puro como MIME type. Wrappear el JSON dentro de un archivo `.md` con bloque de código:

```markdown
# Task Manifest <TASK_ID> — v1.0

\`\`\`json
{
  "schema_version": "1.2",
  ...
}
\`\`\`
```

Guardar como `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.manifest.md`.

### Paso 9 — Subir como attachment `fileType=manifest`

```
POST /api/tasks/<TASK_ID>/attachments
  Content-Type: multipart/form-data
  Authorization: Bearer $TOKEN

  file: <ruta al .manifest.md>
  fileType: manifest
```

→ invoca **`VTT.SKILL-MAN-001`** con (`action=upload`) — internamente llama a `SKL-ATTACH-01`

Output: `attachment_id` retornado por VTT.

### Paso 10 — Verificar upload exitoso

```bash
curl -s "$BASE/api/tasks/<TASK_ID>/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.fileType == "manifest")) | length'
# Esperado: >= 1
```

¿Manifest aparece? →
- **SÍ** → continuar
- **NO** → reintentar upload una vez. Si falla 2x → STOP y notificar al TL

### Paso 11 — Registrar en reporte de entrega

Agregar el `attachment_id` del manifest al reporte de entrega del agente como referencia cruzada (campo opcional).

### Paso 12 — Commit del manifest al PR del agente (OBLIGATORIO)

Los archivos `<TASK_ID>.json` + `<TASK_ID>.manifest.md` se commitean en la branch del agente (`feature/<TASK_ID>`) como parte del mismo PR de la tarea. Esto preserva el snapshot v1.0 en git para auditoría posterior del TL.

```bash
cd .vtt/worktrees/<repo>-<rol>   # worktree del agente

git add knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json
git add knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.manifest.md

git commit -m "[<TASK_ID>] manifest v1.0 — agent delivery

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Refs: #<TASK_ID>"

git push origin feature/<TASK_ID>
```

**Regla:** ambos archivos van al mismo PR de la tarea. NO crear PR separado solo para el manifest. Si el PR ya está abierto, este es un commit adicional encima del feature branch.

> Cuando el TL apruebe y genere v1.5, sobreescribirá estos archivos en SU propio PR (`tl/<TASK_ID>-close`) — ver `VTT.WORKFLOW-MAN-001.004` Paso 13 y `PROTOCOL-ASG-001` FASE 6.

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `<TASK_ID>.json` | archivo JSON local | `knowledge/task-manifests/<phase>/<sprint>/` | Manifest v1.0 fuente — commiteado al PR del agente |
| `<TASK_ID>.manifest.md` | archivo Markdown local | `knowledge/task-manifests/<phase>/<sprint>/` | Wrapper para upload — commiteado al PR del agente |
| Attachment en VTT | record VTT | `task.attachments` | `fileType=manifest`, generado por agent_uuid |
| `attachment_id` | string | Reporte de entrega del agente | Para referenciar en APR del TL |
| Commit con ambos archivos | git | branch `feature/<TASK_ID>` del agente | Snapshot v1.0 inmutable en git para auditoría |

---

## 7. Validación de salida

```bash
# Check 1: archivos locales existen
ls knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json
ls knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.manifest.md

# Check 2: JSON válido
jq '.' knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json > /dev/null

# Check 3: schema correcto
jq '.schema_version' knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json
# Esperado: "1.2"

# Check 4: campos críticos
jq '.delivery.what_was_done != null and (.delivery.what_was_done | length) > 20' \
   knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json
# Esperado: true

# Check 5: review.tl_review queda null (es del TL)
jq '.review.tl_review' knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json
# Esperado: null

# Check 6: attachment subido a VTT
curl -s "$BASE/api/tasks/<TASK_ID>/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '[.data[] | select(.fileType=="manifest")] | length >= 1'
# Esperado: true

# Check 7: Si DevOps, operations completo
CATEGORY=$(jq -r '.task.category' <TASK_ID>.json)
if echo "$CATEGORY" | grep -qE 'deployment|devops|operation|sql_migration|rollback'; then
  jq '.delivery.operations | (.type != null and .post_checks_passed != null)' <TASK_ID>.json
  # Esperado: true
fi
```

- [ ] Las 8 precondiciones verificadas antes de ejecutar
- [ ] JSON local generado en `knowledge/task-manifests/`
- [ ] Wrapper `.md` generado
- [ ] Attachment subido a VTT
- [ ] Schema `1.2` confirmado
- [ ] `review.tl_review` = null
- [ ] Si DevOps → `delivery.operations` poblado
- [ ] Campos null intencionales tienen `note`
- [ ] **Ambos archivos (`<TASK_ID>.json` + `<TASK_ID>.manifest.md`) committeados al PR del agente** (`feature/<TASK_ID>`)
- [ ] `git status` en el worktree del agente está limpio post-commit (sin untracked files)

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `what_was_done: null` | Parser no extrajo la sección del reporte | Verificar formato del reporte — debe tener heading `## Lo que se hizo` o `Lo que se hizo:` |
| `deliverables_actual[].what` faltante | Solo copió path+state | Cada deliverable debe tener `what` descriptivo del bullet "Código" |
| `devlog_entries: []` con `devlog_summary.total>0` | Solo llenó summary | Llenar también el array estructurado con cada entry |
| `indexes.deliverables_paths: []` | No espejó `deliverables_actual.path` | Indexar todos los paths para queries de IMPROVE-002 |
| `vtt_attachments.devlog_id: null` | Devlog no subido como attachment antes del manifest | Subir devlog primero — es la precondición #3 |
| 400 al subir manifest | JSON puro rechazado por VTT | Wrappear en `.md` con bloque ` ```json ` |
| Manifest reemplazado en vez de agregar | Confusión: VTT no permite reemplazar | OK — VTT crea uno nuevo. El viejo queda como historial |
| Tarea DevOps sin `delivery.operations` | Olvido del agente | Validar antes de subir — el bloque es OBLIGATORIO para DevOps |
| `brief.vtt_attachment_id: null` sin `note` | Validador no sabe si es intencional o error | Agregar `brief.note = "DevOps task — no requiere BRIEF"` |
| Schema 1.0 o 1.1 con campos v1.2 | Inconsistencia | Bumpear `schema_version` a `"1.2"` |
| Tarea re-entregada sin `rejection_history` | TL no sabrá por qué se rechazó la primera vez | En DevOps, agregar `operations.rejection_history` |
| Manifest generado prematuramente con null en `git.pr_url` | PR no creado todavía | STOP — crear PR primero (precondición #6) |

---

## 9. Skills invocadas

- `VTT.SKILL-MAN-001` — Skill principal (`action=fetch_vtt_data`, `parse_report`, `add_operations_block`, `compose`, `validate`, `save_local`, `upload`)
- `VTT.SKILL-AUTH-01` (legacy) — Token JWT
- `VTT.SKILL-ATTACH-01` (legacy) — Upload del wrapper .md como attachment

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-VTT-004` Manifest AL FINAL (PROC-MANIFEST-01) | Bloquea generación prematura — las 8 precondiciones la materializan |
| `RULE-AGENT-001 v2.0` Worktree por rol | El agente ejecuta este Workflow desde su worktree |
| Reglas de auto_detect | Cubiertas en el código review del TL (FASE 4 del Protocol) |

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-17 | PM Martin Rivas | Versión inicial. Workflow normativo ejecutable que reemplaza la guía descriptiva `GUIA_MANIFEST_PARA_AGENTES.md` v4.0 §3-§9. Formaliza las 8 precondiciones (PROC-MANIFEST-01) y mapea cada paso a `SKL-MAN-001`. |
| 1.1.0 | 2026-05-18 | PM Martin Rivas | Paso 12 nuevo: **commit obligatorio** del `<TASK_ID>.json` + `<TASK_ID>.manifest.md` al PR del agente (`feature/<TASK_ID>`). Preserva snapshot v1.0 en git para auditoría del TL. Output table actualizado con la nueva fila. Checklist con 2 ítems nuevos. Reflejo del script v1.2 (un solo par de archivos sin sufijo). |
