# VTT.WORKFLOW-MAN-001.004 — Actualizar Task Manifest v1.5

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-MAN-001.004` |
| **Pertenece a** | `VTT.PROTOCOL-MAN-001` §5.4 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-17 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL Reviewer |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-MAN-001 §5.4.3 (que a su vez corresponde a PROTOCOL-ASG-001 §5.5.13) |
| **Schema del manifest** | v1.2 |

---

## 1. Propósito

Generar el **Task Manifest v1.5** que el TL Reviewer sube como NUEVO attachment al cerrar el review de una tarea. El v1.5 enriquece el v1.0 del agente con:

- `delivery.dynamic_model_actions` — las 4 acciones del Modelo Dinámico aplicadas por el TL
- `review.tl_review` — verdict, verifications, comment_id del APR-TL
- `task.current_status` actualizado a `task_completed`
- Devlog entries marcadas como `resolved` por el TL
- TIs nuevos creados por el TL agregados a `delivery.trackable_items_actual.related_to`

> El v1.0 del agente queda intacto en VTT como historial. El v1.5 se sube como ATTACHMENT NUEVO (VTT no permite reemplazar).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_id` | string | Tarea que el TL está revisando | sí | MS-XXX |
| `tl_uuid` | uuid | Operativo TL | sí | UUID del TL Reviewer |
| `v10_attachment_id` | uuid | `GET /api/tasks/<TASK_ID>/attachments` filtrando `fileType=manifest` | sí | El v1.0 del agente |
| `apr_tl_comment_id` | uuid | Comment APR-TL ya posteado en VTT | sí | Para `review.tl_review.comment_id` |
| `dynamic_actions_data` | dict | Output del Modelo Dinámico aplicado por el TL | sí | `{new_tis_created, evidences_added, devlog_resolved_count, notes}` |
| `verifications_data` | dict | Checklist del TL al revisar | sí | Los 6 flags de `review.tl_review.verifications` |
| `vtt_token` | JWT | `SKL-AUTH-01` del TL | sí | Para GETs/POSTs |

---

## 3. Precondiciones (las 11 sagradas)

Antes de ejecutar este Workflow, **TODAS** estas deben cumplirse:

1. ✅ Review Gate verificado (`canProceedToReview=true`)
2. ✅ CAs verificados (todos `met` con evidencia válida)
3. ✅ Attachments verificados (`brief`, `assignment`, `devlog`, `code_logic`, manifest v1.0)
4. ✅ PRs verificados en GitHub (`state=OPEN`, `mergeable=MERGEABLE`)
5. ✅ Disciplina de worktree verificada (diff respeta `allowedPaths` del Execution Manifest)
6. ✅ Living Documents declarados por el agente
7. ✅ Hardcode Check verificado (críticos/altos = 0, FPs justificados)
8. ✅ Code review técnico aprobado (`PROTOCOL-ASG-001 §5.5.8`)
9. ✅ Modelo Dinámico aplicado (TIs creados, evidencias agregadas con marker, devlog resolved)
10. ✅ APR-TL comment posteado (`apr_tl_comment_id` disponible)
11. ✅ Status moveado a `task_completed`

**Si CUALQUIERA falta → STOP. NO ejecutar este Workflow.**

---

## 4. Reglas del Workflow

- **R1:** El v1.0 del agente se lee como **base inmutable**. El TL NO modifica los campos del agente (excepto `devlog_entries[].status` que ahora son `resolved`).
- **R2:** **Subir como NUEVO attachment** — VTT no permite DELETE. v1.0 y v1.5 coexisten.
- **R3:** **`schema_version` sigue siendo `"1.2"`** — el v1.5 es un instance bump, no schema bump.
- **R4:** **`review.pm_approval` queda `null`** — es del PM en v2.0 futuro.
- **R5:** **Si hubo correcciones intermedias** (rechazado y re-entregado) — el v1.5 documenta el ciclo completo, no inventa fixes silenciosos.
- **R6:** **`last_updated_block`** = `"review.tl_review + delivery.dynamic_model_actions"` exactamente.

---

## 5. Pasos

### Paso 1 — Verificar las 11 precondiciones

Igual que en .003 pero con el checklist del TL:

```bash
# 1-4. Status, CAs, attachments, PRs — checks de cierre
curl -s "$BASE/api/tasks/<TASK_ID>" -H "Authorization: Bearer $TOKEN" | \
  jq '{status: .data.statusCode, gate: .data.reviewGate.canProceedToReview}'
# Esperado: status="task_completed", gate=true

# 5. Disciplina worktree (verificada en PROTOCOL-ASG-001 §5.5.5.b)
git diff main...feature/<TASK_ID> --name-only
# Cada path debe estar en allowedPaths del execution_manifest

# 9. Modelo dinámico aplicado
curl -s "$BASE/api/tasks/<TASK_ID>/devlog" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(.status) | unique'
# Esperado: solo "resolved" y/o "wont_fix"

# 10. APR-TL comment
curl -s "$BASE/api/tasks/<TASK_ID>/comments" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.body | startswith("APR-TL"))) | length >= 1'
# Esperado: true
```

¿Todas las 11 OK? →
- **NO** → completar lo faltante, regresar
- **SÍ** → continuar

### Paso 2 — Descargar v1.0 del agente

→ invoca **`VTT.SKILL-MAN-001`** con (`action=download_v10`, `task_id=<TASK_ID>`, `attachment_id=<v10_attachment_id>`)

Internamente:
```
GET /api/tasks/<TASK_ID>/attachments/<v10_attachment_id>
```

Output: copia local en `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.v1.0.json` (parsea el wrapper .md si viene wrappeado).

### Paso 3 — Parsear y validar v1.0

→ invoca **`VTT.SKILL-MAN-001`** con (`action=validate`, `version=1.0`, `manifest=<contenido v1.0>`)

¿v1.0 válido contra schema v1.2? →
- **NO** → STOP y rechazar — el agente debe corregir su v1.0 antes de que el TL pueda generar v1.5
- **SÍ** → continuar

### Paso 4 — Aplicar transformaciones v1.0 → v1.5

→ invoca **`VTT.SKILL-MAN-001`** con (`action=enrich_to_v15`, `base=<v1.0>`, `tl_data=<datos del TL>`)

Cambios aplicados (todos en memoria, no escritos aún):

| Campo | Cambio |
|---|---|
| `task.current_status` | `"task_in_review"` → `"task_completed"` |
| `last_updated` | timestamp actual del TL |
| `last_updated_block` | `"delivery"` → `"review.tl_review + delivery.dynamic_model_actions"` |
| `generation_note` | Anexar: `"v1.5 enriquecido por TL Reviewer <TL_UUID> al cerrar review."` |
| `delivery.devlog_summary.all_resolved_by_tl` | `false` → `true` |
| `delivery.devlog_entries[].status` | actualizar a `"resolved"` los que el TL cerró |
| `delivery.trackable_items_actual.related_to` | agregar TIs nuevos creados por TL desde `items_detected_for_tl_review` |
| `delivery.tech_debt_for_r2[].ti_id` | poblar con UUIDs reales (en v1.0 eran solo `code_suggested`) |

### Paso 5 — Agregar bloque `delivery.dynamic_model_actions`

→ invoca **`VTT.SKILL-MAN-001`** con (`action=add_dynamic_actions`, `data=<dynamic_actions_data>`)

Estructura:

```json
{
  "delivery": {
    "dynamic_model_actions": {
      "new_tis_created": [
        { "code": "DEBT-XXX-NN", "id": "<uuid>", "linked_as": "related_to MS-XXX" }
      ],
      "evidences_added": [
        { "ti_code": "NFR-SEC-XX", "ti_id": "<uuid>", "type": "link", "title": "[MS-XXX] [SX] ..." }
      ],
      "devlog_resolved_count": <N>,
      "devlog_wont_fix_count": <N>,
      "notes": "Modelo dinámico aplicado correctamente. <observaciones adicionales del TL>",
      "note_defer_endpoint_missing": "Endpoint /defer no existe en VTT backend (IMPROVE-003 GAP-VTT-09). Workaround: marcar wont_fix con resolution.",
      "note_typecode_constraint": "Software-only acepta tech_debt pero no process_improvement (validado contra schema VTT)."
    }
  }
}
```

### Paso 6 — Agregar bloque `review.tl_review`

→ invoca **`VTT.SKILL-MAN-001`** con (`action=add_tl_review`, `data=<verifications_data>`)

Estructura:

```json
{
  "review": {
    "tl_review": {
      "reviewer_uuid": "<TL_UUID>",
      "verdict": "approved",
      "reviewed_at": "<ISO timestamp>",
      "moved_to_completed_at": "<ISO timestamp>",
      "comment_id": "<apr_tl_comment_id>",
      "findings": [],
      "verifications": {
        "review_gate_verified": true,
        "criteria_evidence_verified": true,
        "living_docs_verified": true,
        "hardcode_check_verified": true,
        "deliverables_match_assignment": true,
        "dynamic_model_applied": true,
        "worktree_discipline_verified": true,
        "allowed_paths_respected": true
      },
      "notes": "Cierre estándar. <observaciones del TL si las hay>"
    },
    "pm_approval": {
      "approver_uuid": null,
      "approved_at": null,
      "comment_id": null
    }
  }
}
```

### Paso 7 — Validar v1.5

→ invoca **`VTT.SKILL-MAN-001`** con (`action=validate`, `version=1.5`)

Validaciones específicas v1.5 (aborts del script):

| Validación | Condición de fallo |
|---|---|
| `task.current_status="task_completed"` | distinto |
| `last_updated_block` correcto | distinto |
| `delivery.dynamic_model_actions` presente | falta o null |
| `delivery.devlog_summary.all_resolved_by_tl=true` | false |
| `review.tl_review.verdict` poblado | null |
| `review.tl_review.comment_id` presente | null |
| Todas las `verifications.*` son `true` | alguna `false` o null |
| `review.pm_approval` queda null | poblado por error |
| schema_version sigue `"1.2"` | cambió |
| Datos del agente preservados | `delivery.what_was_done` modificado |

¿Validación OK? →
- **NO** → corregir
- **SÍ** → continuar

### Paso 8 — Guardar localmente (SOBREESCRIBE el v1.0 del agente)

El script `VTT.SCRIPT-MAN-001` v1.2 escribe siempre en el mismo par de archivos:

```
knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json
knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.manifest.md
```

Esto sobreescribe el `.json` que el agente commiteó en su PR. El historial v1.0 del agente queda preservado en `git log` (commit del agente en la branch `feature/<TASK_ID>` ya mergeada a main).

> Si necesitas auditar el v1.0 del agente: `git show <commit_sha_del_agente>:knowledge/task-manifests/.../<TASK_ID>.json` o consultar el attachment v1.0 en VTT (ambos siguen existiendo).

### Paso 9 — Subir como NUEVO attachment a VTT

```
POST /api/tasks/<TASK_ID>/attachments
  fileType=manifest
  file=<TASK_ID>.manifest.md
```

→ invoca **`VTT.SKILL-MAN-001`** con (`action=upload`, `version=1.5`)

VTT NO permite DELETE — el v1.0 queda intacto como attachment. Ahora hay 2 attachments con `fileType=manifest` (v1.0 del agente + v1.5 del TL).

### Paso 10 — Verificar attachment v1.5

```bash
curl -s "$BASE/api/tasks/<TASK_ID>/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '[.data[] | select(.fileType=="manifest")] | length'
# Esperado: >= 2 (v1.0 + v1.5)

# Identificar el v1.5 por uploadedBy
curl -s "$BASE/api/tasks/<TASK_ID>/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '[.data[] | select(.fileType=="manifest" and .uploadedBy=="<TL_UUID>")] | length'
# Esperado: >= 1
```

### Paso 11 — Actualizar APR-TL comment con `attachment_id` del v1.5

Si el APR-TL ya posteado no incluye el `attachment_id` del v1.5 (porque el v1.5 se genera DESPUÉS del APR), agregar un comment de seguimiento:

```
"v1.5 del manifest subido — attachment_id: <uuid>"
```

→ invoca **`VTT.SKILL-COMMENT-01`** (legacy)

### Paso 12 — Crear branch del TL y commitear archivos (OBLIGATORIO)

El TL **NO commitea directo a main**. Crea su propia branch:

```bash
cd .vtt/worktrees/<repo>-tl       # worktree del TL Reviewer
git fetch origin
git checkout main
git pull origin main              # asegurar main al día (PR del agente ya mergeado)

git checkout -b tl/<TASK_ID>-close

git add knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json
git add knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.manifest.md

# Otros archivos del TL (si los hay) — ver Paso 13
git add knowledge/agent-tasks/briefs/<phase>/<sprint>/BRIEF_<TASK_ID>_*.md      # si fue modificado
git add knowledge/agent-tasks/assignments/<phase>/<sprint>/ASSIGNMENT_<TASK_ID>_*.md  # si fue modificado

git commit -m "[<TASK_ID>] manifest v1.5 + cierre review — TL approved

- Manifest v1.5 con review.tl_review + dynamic_model_actions
- BRIEF/ASSIGNMENT actualizados (si aplica)
- Modelo dinámico aplicado: <N> TIs nuevos, <N> evidencias, <N> devlog resolved

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Refs: #<TASK_ID>"

git push origin tl/<TASK_ID>-close
```

### Paso 13 — Crear PR del TL a main

```bash
gh pr create \
  --title "[<TASK_ID>] Manifest v1.5 + cierre review" \
  --body "Manifest v1.5 generado tras aprobar review de #<TASK_ID>.

Cambios:
- knowledge/task-manifests/.../<TASK_ID>.json — overwrite con v1.5
- knowledge/task-manifests/.../<TASK_ID>.manifest.md — overwrite con v1.5
- (otros archivos modificados por el TL durante el review)

Ver attachment v1.5 en VTT: <attachment_id>
Ver APR-TL comment: <apr_tl_comment_id>

🤖 Generated with [Claude Code](https://claude.com/claude-code)" \
  --base main
```

> **Política de merge:** hoy el PM aprueba manualmente. Auto-merge si CI pasa es una mejora futura no bloqueante.

### Paso 14 — Verificar git status limpio post-PR

```bash
cd .vtt/worktrees/<repo>-tl
git status
# Esperado: working tree clean (sin untracked files)
```

**Regla operativa:** después de cada review aprobado, el `git status` del worktree del TL DEBE estar limpio. Si quedan archivos modificados sin commitear → completar el PR antes de continuar con la siguiente tarea.

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `<TASK_ID>.json` | archivo JSON local | `knowledge/task-manifests/<phase>/<sprint>/` | Manifest v1.5 (sobreescribe v1.0 del agente) |
| `<TASK_ID>.manifest.md` | archivo Markdown local | `knowledge/task-manifests/<phase>/<sprint>/` | Wrapper v1.5 (sobreescribe v1.0 del agente) |
| Attachment v1.5 en VTT | record VTT | `task.attachments` | `fileType=manifest`, `uploadedBy=<TL_UUID>` (v1.0 del agente sigue existiendo) |
| Comment opcional con `attachment_id` | VTT comment | `task.comments` | Trazabilidad |
| Branch del TL | git | `tl/<TASK_ID>-close` | Contiene overwrite del manifest v1.5 + otros archivos del TL |
| PR del TL | GitHub | `<branch> → main` | Para que PM apruebe los cambios del TL |

---

## 7. Validación de salida

```bash
# Check 1: archivos locales
ls knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.v1.5.json

# Check 2: dynamic_model_actions presente
jq '.delivery.dynamic_model_actions | keys' \
   knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.v1.5.json
# Esperado: incluye new_tis_created, evidences_added, devlog_resolved_count

# Check 3: review.tl_review poblado
jq '.review.tl_review.verdict' <TASK_ID>.v1.5.json
# Esperado: "approved"

# Check 4: current_status correcto
jq '.task.current_status' <TASK_ID>.v1.5.json
# Esperado: "task_completed"

# Check 5: all_resolved_by_tl
jq '.delivery.devlog_summary.all_resolved_by_tl' <TASK_ID>.v1.5.json
# Esperado: true

# Check 6: review.pm_approval queda null
jq '.review.pm_approval.approver_uuid' <TASK_ID>.v1.5.json
# Esperado: null

# Check 7: hay 2+ manifests en VTT
curl -s "$BASE/api/tasks/<TASK_ID>/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '[.data[] | select(.fileType=="manifest")] | length >= 2'
# Esperado: true
```

- [ ] Las 11 precondiciones verificadas antes de ejecutar
- [ ] v1.0 descargado y parseado
- [ ] Transformaciones v1.0 → v1.5 aplicadas
- [ ] `delivery.dynamic_model_actions` agregado
- [ ] `review.tl_review` poblado con verdict + verifications
- [ ] `review.pm_approval` queda null
- [ ] v1.5 subido como NUEVO attachment (no reemplazó el v1.0)
- [ ] **Branch `tl/<TASK_ID>-close` creada y `.json` + `.manifest.md` committeados**
- [ ] **Otros archivos modificados por el TL** (BRIEF/ASSIGNMENT si aplica) committeados en la misma branch
- [ ] **PR del TL creado con `gh pr create`**
- [ ] **`git status` del worktree TL queda limpio** (sin untracked files post-PR)

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `dynamic_model_actions: missing` | SKL-DYNAMIC-MODEL-01 no aplicada antes | Ejecutar el Modelo Dinámico (FASE 4 del Protocol padre) primero |
| `review.tl_review.comment_id: null` | APR-TL no posteado | Postear APR-TL comment antes de generar v1.5 |
| Manifest reemplazado en vez de agregar | Backend interpretó upload como update | OK — VTT siempre crea nuevo. Verificar que hay 2 manifests |
| `verifications.dynamic_model_applied: false` | TL no marcó la verificación | Marcar `true` solo si efectivamente se aplicaron las 4 acciones |
| `current_status` sigue en `task_in_review` | Olvidó mover el status a `task_completed` antes | Mover status primero (`PATCH /status`) |
| `devlog_summary.all_resolved_by_tl: false` | No todos los entries están resolved | Volver al Modelo Dinámico — resolver todos los entries pendientes |
| v1.0 inválido contra schema | Agente generó manifest malformado | Rechazar la tarea (`task_rejected`) — el agente debe regenerar v1.0 |
| `tech_debt_for_r2[].ti_id` sigue null | TL no creó los TIs antes de generar v1.5 | Volver a FASE B del cierre — crear TIs primero, luego sus IDs aquí |
| `living_docs_verified: false` | Agente no declaró LDs impactados | Devolver con rechazo — el agente debe declarar antes del cierre |

---

## 9. Skills invocadas

- `VTT.SKILL-MAN-001` — Skill principal (acciones: `download_v10`, `validate`, `enrich_to_v15`, `add_dynamic_actions`, `add_tl_review`, `save_local`, `upload`)
- `VTT.SKILL-AUTH-01` (legacy) — Token JWT del TL
- `VTT.SKILL-ATTACH-01` (legacy) — Upload del wrapper .md
- `VTT.SKILL-COMMENT-01` (legacy) — Comment opcional con `attachment_id`
- `VTT.SKILL-DYNAMIC-MODEL-01` (legacy/pendiente migración) — Provee los datos para `dynamic_model_actions`

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-VTT-004` Manifest AL FINAL | Aplica también al v1.5 — las 11 precondiciones la materializan |
| `RULE-TL-001` Worktree TL | TL ejecuta este Workflow desde su worktree `project-tl` |
| `RULE-WT-003` Cleanup post-aprobación | Después de aprobar v1.5 → archivar Execution Manifest (PROTOCOL-ASG-001 §5.5.18) |

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-17 | PM Martin Rivas | Versión inicial. Reemplaza la referencia legacy `VTT.WORKFLOW-ASG-001.014`. Formaliza las 11 precondiciones y el modelo de attachment v1.0 + v1.5 coexistentes (VTT sin DELETE). |
| 1.1.0 | 2026-05-18 | PM Martin Rivas | **Refactor mayor.** Filesystem: un solo par de archivos (`<TASK_ID>.json` + `<TASK_ID>.manifest.md`) que el TL sobreescribe del v1.0 del agente. Paso 8 reescrito (sin sufijo `.v1.5`). Pasos 12-14 nuevos: **branch `tl/<TASK_ID>-close` + PR del TL obligatorio** (NO merge directo a main). Output table + checklist actualizados. Refleja PROTOCOL-ASG-001 FASE 6 nuevo. |
