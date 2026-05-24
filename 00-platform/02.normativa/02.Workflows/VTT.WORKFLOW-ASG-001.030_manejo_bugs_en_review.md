# VTT.WORKFLOW-ASG-001.030 — Manejo de Bugs detectados en Code Review

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.030` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.5 (FASE 4 — Cierre con Modelo Dinámico) |
| **Versión** | 1.0.1 |
| **Fecha** | 2026-05-22 |
| **Aplica a** | TL Reviewer (ejecutor principal), Agente ejecutor de la tarea hija (BE/FE/DB/DO/etc.) |
| **Reglas Nivel 0 aplicables** | `RULE-SCRIPT-001`, `RULE-TEMPLATE-001`, `RULE-AGENT-001` |
| **Origen** | `00-agent-setup/06.Documentos_soporte/GUIA_MANEJO_BUGS_TL.md` v1.1 (legacy memory-service) — formalizado a workflow canónico el 2026-05-22 |

---

## 1. Propósito

Formalizar el sub-proceso del TL Reviewer cuando, durante code review (FASE 4 del PROTOCOL-ASG-001), detecta un **bug** que requiere corrección antes de aprobar. En lugar de pedir "fix inline" sin trazabilidad, se crea una **tarea hija con consecutivo MS-XXX**, la padre pasa a `task_on_hold`, y se restablece el ciclo cuando la hija aprueba.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `parent_task_id` | string (MS-XXX) | Tarea padre actualmente en `task_in_review` donde el TL detectó el bug |
| `bug_description` | texto | Descripción del bug (lint, scope mezclado, error funcional, falta de docs, etc.) |
| `bug_severity` | enum (`critical`/`high`/`medium`/`low`) | Severidad del bug |
| `bug_category` | string | Categoría: `scope_violation` / `ci_failure` / `lint_error` / `missing_docs` / `logic_error` / `refactor_needed` / otro |
| `assignee_role` | enum (BE/FE/DB/DO/QA/DL/UX/AR/SA) | Rol del agente que arreglará el bug |
| `cas_list` | array `[{title, description}]` | Lista de Criterios de Aceptación de la tarea hija (mínimo 1) |
| `assignment_md_path` | path local | Ruta al ASSIGNMENT_MS-XXX_<desc>.md ya escrito por el TL (formato canónico) |
| `sprint` | string | Sprint actual (ej. `S03`) |

## 3. Precondiciones

- TL ejecutó Paso 0 (`VTT.SKILL-PRECHECK-001` — `$VTT_SETUP` exportado, scripts canónicos disponibles, no copias locales)
- `parent_task_id` existe en VTT y está en estado revisable (`task_in_review` típicamente)
- El TL ya **escribió a mano** dos artefactos locales (NO automatizable):
  1. `ASSIGNMENT_MS-XXX_<desc>.md` con template canónico v3.0
  2. Lista de CAs (JSON inline o `cas.json`)
- `$TOKEN` JWT válido del TL (vía `VTT.SKILL-AUTH-001`)

## 4. Reglas del Workflow

| # | Regla |
|---|---|
| **R1** | **Cualquier corrección detectada durante review ES UN BUG.** No importa si es lint, scope mezclado, falta de docs, error de lógica o refactor menor — todo se maneja con tarea hija consecutiva. |
| **R2** | NUNCA pedir "fix inline" sin generar tarea hija. |
| **R3** | NUNCA usar acrónimos como `MS-322-FIX`, `MS-322b`, `FIX-322`. Usar consecutivos canónicos `MS-XXX`. |
| **R4** | NUNCA dejar la padre en `task_in_review` mientras el agente corrige — la padre **DEBE** moverse a `task_on_hold` antes de notificar al agente. |
| **R5** | NUNCA usar `PATCH /status` para `task_on_hold` — usar el endpoint dedicado `PUT /api/tasks/{ID}/on-hold` con payload completo. |
| **R6** | El TL crea la tarea, la asigna y la activa, pero **el agente** es quien mueve a `task_in_progress` (no el TL). |
| **R7** | El POST a `/devlog-entries` (plural) **requiere wrapper `{"entries":[...]}`**. Para 1 entry usar `POST /devlog` (singular). |
| **R8** | El campo canónico de assignee es **`assignedToId`**, NO `assigneeId` (VTT acepta `assigneeId` con 200 OK pero no persiste). |
| **R9** | El campo canónico de tipo de CA es **`criteriaTypeCode`**, NO `type`. Endpoint es `/criteria`, NO `/acceptance-criteria`. |
| **R10** | Linking bug → hija se hace con **3 mecanismos paralelos**: marker textual `[TASK:MS-XXX]` en title+description del issue, `onHoldIssueId` en el PUT /on-hold, y dependency formal `blocks` padre→hija. |
| **R11** | El reporte de la tarea hija sigue **`VTT.SKILL-REPORT-001 v1.1`** (path nuevo `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md` + render obligatorio en pantalla). |
| **R12** | Manifest v1.0 al FINAL del workflow del agente — NUNCA antes de attachments + status + dynamic_model (lección PROC-MANIFEST-01). |

---

## 5. Pasos

```
┌───────────────────────────────────────────────────────────────────────┐
│  Paso 1 — DETECTAR el bug durante review                              │
│  Paso 2 — TL escribe ASSIGNMENT.md (a mano)                           │
│  Paso 3 — TL escribe lista de CAs (a mano)                            │
│  Paso 4 — TL ejecuta script crear_tarea_bug.py (automatiza 4a-4i)     │
│           ├── 4a: Crear tarea hija (POST /phases/:id/tasks)           │
│           ├── 4b: Asignar agente (PUT /api/tasks/:id) - workaround    │
│           ├── 4c: Subir ASSIGNMENT como attachment                    │
│           ├── 4d: Crear CAs (1 por bug + verificación)                │
│           ├── 4e: Crear bug entry en padre (POST /issues)             │
│           ├── 4f: Crear dependency padre→hija (POST /dependencies)    │
│           ├── 4g: Mover padre a task_on_hold (PUT /on-hold)           │
│           ├── 4h: Generar MENSAJE_MS-XXX.md (gen_mensaje)             │
│           └── 4i: (opcional --post) postear mensaje en VTT            │
│  Paso 5 — Agente trabaja la hija (in_progress → CAs → in_review)      │
│  Paso 6 — Agente reporta entrega (SKILL-REPORT-001 v1.1)              │
│  Paso 7 — TL revisa la hija (review-gate + criterios)                 │
│  Paso 8 — TL aprueba hija → padre libera (PUT /release-hold)          │
│  Paso 9 — TL re-revisa la padre con código corregido                  │
│  Paso 10 — Continúa la padre (aprobar o nueva hija si quedan bugs)    │
└───────────────────────────────────────────────────────────────────────┘
```

### Paso 1 — Detectar el bug

Durante el code review (skill `/vtt-review`), si el TL detecta:

- CI Build+Lint failing
- Scope mezclado (archivos de otra tarea en el PR)
- Errores funcionales en código entregado
- Falta de docs (LOGIC.md, devlog, manifest)
- Reporte del agente en path legacy `knowledge/agent-tasks/reports/...` (violación I2 v1.1)
- Reporte mostrado con `cat` y no renderizado en pantalla (violación I3 v1.1)
- Cualquier otra cosa que requiera corrección antes de aprobar

**NO procede a aprobar.** Pasa al Paso 2.

### Paso 2 — TL escribe ASSIGNMENT.md (a mano)

Crear archivo local:
```
knowledge/agent-tasks/assignments/ASSIGNMENT_MS-XXX_<descripcion-kebab>.md
```

Usar template canónico:
```
$VTT_SETUP/03.templates/tarea/TEMPLATE_ASSIGNMENT_v3.md
```

Secciones obligatorias:
1. Encabezado con metadata (task_id, padre, asignado, sprint, worktree)
2. CONTEXTO (qué bugs hay, link al PR/comments donde se detectaron)
3. SCOPE (archivos a tocar, archivos a NO tocar)
4. ACCIONES (pasos concretos, comandos git)
5. CRITERIOS DE ACEPTACIÓN (1 por bug + verificación)
6. ENTREGABLES (branches, PRs, SKL-REPORT-01 v1.1, manifest)
7. WORKFLOW (in_progress → in_review)

### Paso 3 — TL escribe lista de CAs (a mano)

Definir CAs en JSON (inline en spec o archivo separado `cas.json`):

```json
{
  "cas": [
    {"title": "CA-01: <criterio>", "description": "<cómo se verifica>"},
    {"title": "CA-02: CI build + lint passing", "description": "GitHub Actions verde"},
    {"title": "CA-03: ...", "description": "..."}
  ]
}
```

Mínimo 1 CA por bug + CAs de verificación (CI verde, lint clean, tests passing).

### Paso 4 — TL ejecuta script `VTT.SCRIPT-ASG-001` (automatiza 4a-4i)

> **Script canónico (promovido el 2026-05-22):**
> `$VTT_SETUP/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py`
>
> El script tiene **enforcement runtime de RULE-SCRIPT-001**: si se invoca desde una copia local en lugar del path canónico, aborta con exit 2 + mensaje JSON de violación.
> Bypass solo para desarrollo del script: `VTT_SCRIPT_ALLOW_LOCAL=1`.

Invocación canónica:

```bash
# Modo interactivo (primera vez)
python $VTT_SETUP/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py --interactive

# Modo con spec JSON (preferido para repetir)
python $VTT_SETUP/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py \
  --spec bugs/MS-XXX_spec.json --post

# Modo CLI completo (10+ flags — ver --help)
python $VTT_SETUP/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py \
  --parent MS-XXX \
  --title "[BUG] MS-XXX <desc>" \
  --description "..." \
  --assignee BE \
  --estimated-hours 2 \
  --priority high \
  --severity high \
  --bug-category scope_violation \
  --sprint S03 \
  --assignment-md knowledge/agent-tasks/assignments/ASSIGNMENT_MS-XXX.md \
  --cas-file cas.json \
  --post
```

**Deuda técnica pendiente (futuro refactor — no bloquea uso actual):**
- Modo `--validate` que verifique pre-condiciones antes de tocar VTT
- Lectura formal de `TEMPLATE_ASSIGNMENT_v3.md` (`RULE-TEMPLATE-001`) en lugar de asumir formato libre
- Tests unitarios contra mocks VTT

#### 4a. Crear tarea hija

```
POST /api/phases/{PHASE_UUID}/tasks
```

Payload:
```json
{
  "title": "[BUG] MS-XXX <descripcion corta>",
  "description": "<contexto del bug + lista de items + tarea padre, max 2000 chars>",
  "priorityId": "<UUID priority>",
  "statusId": "<UUID task_pending>",
  "assignedToId": "<UUID del agente>",
  "assignedBy": "<UUID del TL>",
  "createdBy": "<UUID del TL>",
  "complexity": "MEDIUM",
  "category": "bugfix",
  "type": "bug",
  "estimatedHours": 2
}
```

**Cómo obtener siguiente consecutivo MS-XXX:**
```bash
# Paginar tareas del proyecto y encontrar el max
for off in 0 100 200 300; do
  curl -s "$BASE_URL/api/tasks?projectId=$PROJECT_ID&limit=100&offset=$off" \
    -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
tasks = json.load(sys.stdin).get('data', [])
nums = [int(t['id'].split('-')[1]) for t in tasks if t.get('id','').startswith('MS-')]
print(max(nums) if nums else 0)
"
done
# Tomar el max + 1
```

#### 4b. Asignar agente (workaround del gotcha)

`POST /api/phases/:id/tasks` ignora silenciosamente el assignee. Después del 4a:

```
PUT /api/tasks/{TASK_ID}
Body: {"assignedToId": "<UUID del agente>"}
```

⚠️ Usar **`assignedToId`** (no `assigneeId` — VTT lo acepta con 200 OK pero no persiste).

Verificar:
```bash
curl -s "$BASE_URL/api/tasks/{TASK_ID}" -H "Authorization: Bearer $TOKEN" | jq '.data.assignee'
# Debe devolver {id, name, email, role}, NO null
```

#### 4c. Subir ASSIGNMENT como attachment

```
POST /api/tasks/{TASK_ID}/attachments
Content-Type: multipart/form-data
```

Form fields:
- `file`: el archivo .md
- `fileType`: `"assignment"`
- `uploadedById`: UUID del TL

#### 4d. Crear CAs

Para cada CA del paso 3:

```
POST /api/tasks/{TASK_ID}/criteria
```

Payload:
```json
{
  "title": "CA-01: <criterio>",
  "description": "<como se verifica>",
  "criteriaTypeCode": "acceptance",
  "required": true,
  "order": 1
}
```

⚠️ Campo es **`criteriaTypeCode`**, no `type`. Endpoint es `/criteria`, no `/acceptance-criteria`.

#### 4e. Crear bug entry en la tarea PADRE

```
POST /api/tasks/{PADRE_ID}/issues
```

Payload:
```json
{
  "type": "bug",
  "title": "[TASK:MS-XXX-hija] [SPRINT:SX] <descripcion corta>",
  "description": "[TASK:MS-XXX-hija] [SPRINT:SX] <lista de items + referencia a tarea hija>",
  "severity": "high",
  "reportedById": "<UUID del TL>"
}
```

Severidades válidas: `critical | high | medium | low`
Tipos válidos: `bug | question | requirement | other`

> ⚠️ **Limitación crítica del linking issue ↔ hija:** VTT NO acepta `resolvedByTaskId` ni campos similares en el POST de issue (acepta con 200 OK pero no persiste). PUT/PATCH `/issues/{id}` no existen (404).
>
> **Workaround (3 mecanismos paralelos):**
> 1. **Marker textual obligatorio** en title + description (ver payload arriba)
> 2. **`onHoldIssueId`** en el PUT /on-hold (paso 4g)
> 3. **Dependency `blocks`** (paso 4f)

Guardar el `id` del issue retornado — se usa en 4g.

#### 4f. Crear dependency padre→hija

```
POST /api/tasks/{PADRE_ID}/dependencies
```

Payload:
```json
{
  "taskId": "<PADRE_ID>",
  "dependsOnTaskId": "<HIJA_ID>",
  "type": "blocks"
}
```

Esto hace que la padre figure como `isBlocked: true` mientras la hija esté abierta.

#### 4g. Mover padre a `task_on_hold`

⚠️ **NUNCA usar PATCH `/status` para `task_on_hold`** — usar endpoint dedicado:

```
PUT /api/tasks/{PADRE_ID}/on-hold
```

Payload:
```json
{
  "type": "bug",
  "title": "<mismo título del bug entry>",
  "description": "<razón corta>",
  "blockedById": "<HIJA_ID>",
  "onHoldIssueId": "<ID del issue del 4e>",
  "raisedById": "<UUID del TL>"
}
```

Verificar:
```bash
curl -s "$BASE_URL/api/tasks/{PADRE_ID}" -H "Authorization: Bearer $TOKEN" \
  | jq '.data | {status: .status.code, isBlocked}'
# Esperado: status=task_on_hold, isBlocked=true
```

#### 4h. Generar `MENSAJE_MS-XXX.md`

```bash
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  MS-XXX \
  --project-root <PROJECT_ROOT> \
  --vtt-setup $VTT_SETUP \
  --output knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_MS-XXX.md
```

#### 4i. (opcional `--post`) postear mensaje en VTT

```bash
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  MS-XXX --post \
  --project-root <PROJECT_ROOT> \
  --vtt-setup $VTT_SETUP
```

### Paso 5 — Agente trabaja la tarea hija

El agente (BE/FE/DB/...) ejecuta su workflow normal de tarea, con énfasis en:

1. **Pre-check obligatorio** (`VTT.SKILL-PRECHECK-001`) — antes de tocar código
2. Mueve a `task_in_progress` (**el agente, no el TL**)
3. Trabaja la corrección en su worktree dedicado
4. Registra devlog entries (`VTT.SKILL-DEV-001..005` según corresponda)
5. Cumple CAs (`PATCH /criteria/<cid>` con `{status:"met", evidence:"..."}`)
6. Verifica review gate `canProceedToReview: true`

### Paso 6 — Agente reporta entrega

Sigue `VTT.SKILL-REPORT-001 v1.1`:

1. **R6:** reporte en `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md` (MISMA carpeta del JSON del manifest)
2. **R7:** muestra el reporte renderizado en pantalla (NO `cat`)
3. Sube devlog y code-logic como attachments (`fileType=devlog`, `fileType=code_logic`)
4. Crea PR en GitHub
5. Genera manifest v1.0:
```bash
python $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
  --task-id MS-XXX \
  --version 1.0 \
  --agent-uuid <agent_uuid> \
  --report-path knowledge/task-manifests/<phase>/<sprint>/MS-XXX_REPORT.md \
  --phase <phase> --sprint <sprint> --upload
```
6. Mueve a `task_in_review`

### Paso 7 — TL revisa la tarea hija

TL ejecuta `/vtt-review MS-XXX` y valida las 5 verificaciones de la política de review v1.1 (ver `VTT.SKILL-REPORT-001` y `OPERATIVO_TL_REVIEWER.md` §3.bis):

| Check | Endpoint |
|-------|----------|
| Reporte en path canónico (task-manifests/, no agent-tasks/reports/) | filesystem |
| Reporte renderizado por el agente (no `cat`) | pantalla |
| Manifest v1.0 commiteado al PR (3 archivos) | `git log` |
| Devlog en estado terminal | `GET /api/tasks/{ID}/devlog` |
| Review gate `canProceedToReview: true` | `GET /api/tasks/{ID}/review-gate` |

Si algo falla → postear NEEDS_FIXES (la corrección se queda en la misma hija, NO se crea nueva hija).

Si todo OK → Paso 8.

### Paso 8 — Aprobar hija + liberar padre

Aplicar el ciclo del PROTOCOL-ASG-001 §5.5 (modelo dinámico) a la hija:

**8.1 — Resolver devlog entries pendientes** (`VTT.PROTOCOL-DEV-001 §FASE 3`):

```bash
curl -s -X PATCH "$BASE_URL/api/tasks/{HIJA_ID}/devlog/<ENTRY_ID>/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "resolution": "Revisado por TL durante cierre de bug MS-XXX. <decision/observacion>."
  }'
```

⚠️ `resolution` es REQUERIDO cuando status=`resolved` o `wont_fix`. Sin él → 400.

**8.2 — Aplicar modelo dinámico** si el reporte del agente lista TIs/tech_debt nuevos:

```bash
# Crear TI
curl -s -X POST "$BASE_URL/api/projects/$PROJECT_ID/trackable-items" ...

# Vincular TI a hija
curl -s -X POST "$BASE_URL/api/trackable-items/<TI_ID>/tasks" \
  -d '{"taskId":"<HIJA_ID>","linkType":"related_to"}'

# Agregar evidencia (PR)
curl -s -X POST "$BASE_URL/api/trackable-items/<TI_ID>/evidence" \
  -d '{
    "type": "link",
    "title": "[MS-XXX] [SX] PR fix",
    "url": "https://github.com/.../pull/N",
    "description": "[TASK:MS-XXX] [SPRINT:SX] PR de la tarea hija que cierra el bug",
    "createdById": "<TL_UUID>"
  }'
```

**8.3 — APR-TL Comment:**

```bash
curl -s -X POST "$BASE_URL/api/tasks/{HIJA_ID}/comments" \
  -d '{
    "message": "## APR-TL: MS-XXX aprobado tras code review + modelo dinamico aplicado\n\n...",
    "userId": "<TL_UUID>"
  }'
```

Max 5000 chars.

**8.4 — Mover hija a `task_completed`:**

```bash
curl -s -X PATCH "$BASE_URL/api/tasks/{HIJA_ID}/status" \
  -d '{
    "statusId": "<UUID task_completed>",
    "changedBy": "<TL_UUID>",
    "reason": "APR-TL: bug MS-XXX cerrado, padre lista para re-review"
  }'
```

**8.5 — Liberar padre de on_hold:**

```
PUT /api/tasks/{PADRE_ID}/release-hold
Body: {"releasedById": "<TL_UUID>", "reason": "Tarea hija MS-XXX aprobada"}
```

La padre vuelve a `task_in_review`.

**8.6 — Manifest v1.5 de la hija al FINAL** (lección PROC-MANIFEST-01):

```bash
python $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
  --task-id MS-XXX --version 1.5 ...
```

### Paso 9 — TL re-revisa la padre

Una vez liberada:
1. Ejecutar `/vtt-review` sobre la padre con el código corregido (probablemente nuevo PR mergeado o commits adicionales)
2. Si todo pasa → aprobar normal (Paso 10)
3. Si encuentra MÁS bugs → repetir desde Paso 1 (puede haber varias hijas por una padre)

### Paso 10 — Continuar la tarea padre

Si la padre quedó en `task_in_review` y todas las validaciones pasaron → mover a `task_completed` siguiendo el flujo normal del PROTOCOL-ASG-001 §5.5.

---

## 6. Outputs

| Output | Tipo | Ubicación |
|---|---|---|
| Tarea hija creada en VTT | task | `MS-XXX` con `status=task_pending`, `assignee=<rol>` |
| ASSIGNMENT como attachment | file | VTT attachment, `fileType=assignment` |
| Bug entry en padre | issue | `POST /tasks/{PADRE_ID}/issues` → guardar `id` |
| Dependency padre→hija | dependency | `type=blocks` |
| Padre en `task_on_hold` | task state | con `isBlocked=true` |
| Mensaje al agente | file | `knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_MS-XXX.md` |
| Comment de activación en padre | comment | informa al equipo del on_hold |
| (Al cerrar) Padre liberada | task state | `status=task_in_review`, `isBlocked=false` |

---

## 7. Validación

### Después del Paso 4 (creación de hija + on_hold de padre)

```bash
# Hija creada correctamente
curl -s "$BASE_URL/api/tasks/<HIJA_ID>" -H "Authorization: Bearer $TOKEN" \
  | jq '.data | {id, title, status: .status.code, assignee: .assignee.email}'
# Esperado: id=MS-XXX, status=task_pending, assignee=<rol>@memory-service.vtt.ai

# Padre en on_hold
curl -s "$BASE_URL/api/tasks/<PADRE_ID>" -H "Authorization: Bearer $TOKEN" \
  | jq '.data | {status: .status.code, isBlocked, onHoldIssueId}'
# Esperado: status=task_on_hold, isBlocked=true, onHoldIssueId=<UUID del bug entry>

# Dependency creada
curl -s "$BASE_URL/api/tasks/<PADRE_ID>/dependencies" -H "Authorization: Bearer $TOKEN" \
  | jq '.data[] | select(.type=="blocks")'
# Esperado: array con la dependency padre→hija
```

### Después del Paso 8 (cierre de hija + liberación de padre)

```bash
# Hija aprobada
curl -s "$BASE_URL/api/tasks/<HIJA_ID>" -H "Authorization: Bearer $TOKEN" \
  | jq '.data | {status: .status.code}'
# Esperado: status=task_completed

# Padre liberada
curl -s "$BASE_URL/api/tasks/<PADRE_ID>" -H "Authorization: Bearer $TOKEN" \
  | jq '.data | {status: .status.code, isBlocked}'
# Esperado: status=task_in_review, isBlocked=false
```

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Hija creada pero `assignee=null` | `POST /phases/:id/tasks` ignora el assignee (gotcha #1) | Ejecutar paso 4b: `PUT /api/tasks/{ID}` con `assignedToId` (NO `assigneeId`) |
| `POST /criteria` retorna 400 "type required" | Usaste `type` en lugar de `criteriaTypeCode` | Cambiar campo a `criteriaTypeCode` |
| `POST /devlog-entries` retorna 400 | Falta wrapper `{"entries":[...]}` | Usar `/devlog` singular para 1 entry, o `/devlog-entries` con wrapper |
| `POST /issues` con `resolvedByTaskId` no liga la hija | Campo no persiste en VTT (gotcha #22) | Usar workaround de 3 mecanismos: marker textual + onHoldIssueId + dependency blocks |
| `PATCH /status` con `task_on_hold` falla | Endpoint incorrecto (gotcha #18) | Usar `PUT /api/tasks/{ID}/on-hold` con payload completo |
| `PATCH /devlog/{eid}/status` con `resolved` retorna 400 | Falta `resolution` (gotcha #12) | Agregar `resolution` con descripción real (no string vacío) |
| Comment > 5000 chars retorna 400 | Límite VTT (gotcha #5) | Dividir comment o adjuntar archivo |
| Agente reporta y reporte está en path legacy | Agente no leyó política I2 v1.1 | Devolver NEEDS_FIXES — mover a `knowledge/task-manifests/<phase>/<sprint>/` |
| Agente muestra reporte con `cat` | Agente no leyó política I3 v1.1 | Devolver NEEDS_FIXES — pedir render markdown |
| Padre no se libera de on_hold | Falta `PUT /release-hold` después del cierre de hija | Ejecutar paso 8.5 |
| Script aborta con `RULE-SCRIPT-001 violation` | Invocaste desde copia local del worktree, no desde `$VTT_SETUP` | Usar path canónico `python $VTT_SETUP/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py` |
| Script no encontrado en `$VTT_SETUP/.../asg/` | Repo `virtual-teams-setup` desactualizado | `cd $VTT_SETUP/../.. && git pull origin main` para sincronizar |

---

## 9. Skills invocadas

- `VTT.SKILL-AUTH-001` (obtener JWT)
- `VTT.SKILL-PRECHECK-001` (validar entorno antes de Paso 4)
- `VTT.SKILL-TASK-001` (crear tarea — paso 4a)
- `VTT.SKILL-TASK-003` (asignar agente — paso 4b)
- `VTT.SKILL-ATTACH-001` (subir ASSIGNMENT — paso 4c)
- `VTT.SKILL-ISS-001` (crear bug entry — paso 4e)
- `VTT.SKILL-STATUS-005` (mover a on_hold — paso 4g, usar PUT no PATCH)
- `VTT.SKILL-MSG-001` (generar mensaje — paso 4h/4i)
- `VTT.SKILL-COMMENT-001` (comments en padre/hija — pasos 4i, 8.3)
- `VTT.SKILL-DEV-004` (resolver devlog entries — paso 8.1)
- `VTT.SKILL-REPORT-001` v1.1 (TL valida el reporte del agente — paso 7)
- `VTT.PROTOCOL-DEV-001` §FASE 3 (procesamiento devlog en review — paso 8.1)

---

## 10. Cuándo NO usar este Workflow

| Caso | En su lugar |
|---|---|
| El bug es del **TL Reviewer mismo** (error suyo durante review) | Comentar en la tarea explicando + revisar de nuevo, sin crear hija |
| El bug es **trivial** (un typo en docstring que el TL puede arreglar in-place) | Postear comment + fix inline en la propia padre, registrar en devlog del TL como `observation` |
| El bug es **del TL Ejecutor** durante planificación (BRIEF/ASSIGNMENT mal escrito) | El TL Reviewer notifica al TL Ejecutor + se corrige el doc original, no genera hija |
| El "bug" es en realidad un **scope nuevo** (agregar feature no planificada) | NO usar este workflow — generar nueva tarea independiente con dependency, no hija de bug |
| El bug afecta a **múltiples tareas en curso** | Escalar al PM — puede requerir reordenar sprint, no se resuelve con una hija |

---

## 11. Referencias cruzadas

| Documento | Relación |
|---|---|
| `VTT.PROTOCOL-ASG-001` §5.5 | Protocol padre — este workflow es el sub-proceso de "bug detectado en review" |
| `VTT.PROTOCOL-DEV-001` §FASE 3 | Procesamiento de devlog en review (invocado en paso 8.1) |
| `VTT.PROTOCOL-MAN-001` | Manifest v1.0/v1.5 (paso 6, paso 8.6) |
| `VTT.SKILL-REPORT-001` v1.1 | Política I2/I3 que el TL valida en paso 7 |
| `VTT.SKILL-DEV-004` | Lifecycle de devlog entries en paso 8.1 |
| `VTT.SKILL-MSG-001` + `VTT.SCRIPT-MSG-001` | Mensaje al agente en paso 4h/4i |
| `00-agent-setup/06.Documentos_soporte/GUIA_MANEJO_BUGS_TL.md` (legacy) | Documento origen — archivado a `_archive/` el 2026-05-22 tras formalización |
| `VTT.SCRIPT-ASG-001_crear_tarea_bug.py` | Script canónico que automatiza pasos 4a-4i. Path: `$VTT_SETUP/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py`. Promovido 2026-05-22 con enforcement runtime de RULE-SCRIPT-001 |

---

## 12. Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-22 | **Formalización del manejo de bugs en review como Workflow VTT canónico.** Origen: `GUIA_MANEJO_BUGS_TL.md` v1.1 (legacy memory-service, 805 líneas) transformada al modelo de 4 niveles VTT (Workflow nivel 3 que pertenece a `PROTOCOL-ASG-001`). Cambios al transformar: (1) Header canónico VTT con código, versión, reglas Nivel 0 aplicables. (2) Referencias a `00-agent-setup/06.Documentos_soporte/PROCESO_ASIGNACION_TAREAS_v3.md` reemplazadas por `VTT.PROTOCOL-ASG-001` canónico. (3) Fix de bug heredado: `POST /devlog-entries` ahora documentado con wrapper requerido `{entries:[]}` o `/devlog` singular para 1 entry. (4) Cross-refs actualizadas a skills DEV-001..005 (decision/observation/edit/lifecycle/delete), PROTOCOL-DEV-001 §FASE 3 para procesamiento devlog en paso 8.1. (5) Política de review v1.1 (I2 path nuevo + I3 render obligatorio) agregada como criterios de detección de bug en Paso 1 y validación en Paso 7. (6) Skill MSG-001 + SCRIPT-MSG-001 referenciados en Paso 4h/4i (path canónico desde `$VTT_SETUP`). (7) Script `crear_tarea_bug.py` declarado como **pendiente de promoción** a `VTT.SCRIPT-ASG-001` siguiendo RULE-SCRIPT-001 (mismo refactor que `gen_mensaje.py` → `VTT.SCRIPT-MSG-001` en VTT-725). (8) Estructura reorganizada en las 12 secciones canónicas de Workflow (PROTOCOL-GOV-001 §6). (9) Caso real MS-322 → MS-375 documentado como ejemplo histórico. |
| 1.0.1 | 2026-05-22 | **Script promovido a `$VTT_SETUP`.** El script `crear_tarea_bug.py` (576 líneas) fue copiado de `memory-service/.vtt/worktrees/project-tl/scripts/` a `$VTT_SETUP/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py`. Se agregó `enforce_canonical_path()` al inicio de `main()` que aborta con exit 2 si se invoca desde copia local (mismo patrón que SCRIPT-MSG-001 y SCRIPT-MAN-001). Probado: invocación canónica `--help` OK / copia local `--help` aborta con JSON RULE-SCRIPT-001. Cambios al workflow: Paso 4 actualizado con invocación canónica, errores comunes actualizados, §11 referencias cruzadas marca script como canónico. Deuda técnica pendiente declarada explícitamente (modo `--validate`, lectura formal de TEMPLATE_ASSIGNMENT, tests). |
