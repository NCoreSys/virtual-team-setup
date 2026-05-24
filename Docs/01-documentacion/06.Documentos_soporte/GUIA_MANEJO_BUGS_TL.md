# GUIA — Manejo de Bugs por el TL (Proceso de 10 pasos)

**Versión:** 1.1
**Fecha:** 2026-05-21
**Aplicable a:** TL Reviewer Memory Service (y otros proyectos VTT)
**Motivo:** Formalizar el proceso de bug tracking detectado durante review. Sin este proceso los fixes inline pierden trazabilidad, las métricas se rompen, y no hay relación entre la corrección y la tarea afectada.

**Documento base autoritativo:** `00-agent-setup/06.Documentos_soporte/PROCESO_ASIGNACION_TAREAS_v3.md` — esta guía es complemento específico para el caso "bug detectado en review".

**Cambios v1.0 → v1.1:**
- Payload `POST /api/phases/:id/tasks` alineado con doc v3 (statusId, assignedBy, createdBy obligatorios)
- CAs incluyen `required: true` (gotcha doc v3)
- Limitación de issue→tarea documentada (no existe campo `resolvedByTaskId` aceptado por POST)
- Linking se logra via: dependency + onHoldIssueId + marker textual `[TASK:MS-XXX]`

---

## REGLA FUNDAMENTAL

> **Cualquier corrección detectada durante review ES UN BUG.**
>
> No importa si es lint, scope mezclado, falta de docs, error de lógica, refactor menor, o cualquier otra cosa. Todo se maneja con tarea hija consecutiva (siguiente MS-XXX) y la tarea padre se pone en `task_on_hold`.

**NUNCA**:
- Pedir "fix inline" sin generar tarea hija
- Inventar acrónimos tipo `MS-322-FIX`, `MS-322b`, `FIX-322` — usar consecutivos `MS-XXX`
- Dejar la padre en `task_in_review` mientras el agente corrige
- Saltarte el paso 4 (ligar bug + on_hold)

---

## PROCESO DE 10 PASOS (orden de ejecución correcto)

| # | Paso | Responsable | Endpoint / Acción |
|---|------|-------------|-------------------|
| 1 | Detectar el bug | TL | — (durante review) |
| 2 | **Escribir ASSIGNMENT.md a mano** | TL | crear archivo local en `knowledge/agent-tasks/assignments/ASSIGNMENT_MS-XXX_<desc>.md` |
| 3 | **Escribir lista de CAs** | TL | archivo `cas.json` o sección `cas` del spec |
| 4 | **Correr `crear_tarea_bug.py`** (automatiza 4a-4i) | TL | un solo comando |
| 4a | Crear tarea hija | script | `POST /api/phases/:id/tasks` |
| 4b | Asignar agente (workaround gotcha) | script | `PUT /api/tasks/:id` |
| 4c | Subir ASSIGNMENT como attachment | script | `POST /api/tasks/:id/attachments` |
| 4d | Crear CAs | script | `POST /api/tasks/:id/criteria` |
| 4e | Crear bug entry en padre | script | `POST /api/tasks/:padre/issues` |
| 4f | Crear dependencia padre→hija | script | `POST /api/tasks/:padre/dependencies` |
| 4g | Mover padre a `task_on_hold` | script | `PUT /api/tasks/:padre/on-hold` |
| 4h | Generar MENSAJE_MS-XXX.md | script | `gen_mensaje.py` |
| 4i | (opcional `--post`) postear mensaje en VTT | script | `POST /api/tasks/:id/comments` |
| 5 | Agente trabaja la hija | Agente | `PATCH /api/tasks/:hija/status` (in_progress) |
| 6 | Agente reporta entrega completa | Agente | SKL-REPORT-01 + `POST /api/tasks/:id/comments` |
| 7 | TL revisa la hija | TL | `GET /api/tasks/:hija/review-gate` + criterios |
| 8 | TL aprueba hija → padre libera | TL | `PATCH /api/tasks/:hija/status` (completed) + `PUT /api/tasks/:padre/release-hold` |
| 9 | TL re-revisa la padre con código corregido | TL | `/vtt-review` sobre padre |
| 10 | Continúa la padre (aprobar o nueva hija si hay más bugs) | TL | normal flow |

**Lo crítico**: pasos 2 y 3 son **a mano** (input del TL). El script solo automatiza desde el paso 4a.

---

## AUTOMATIZACIÓN — `scripts/crear_tarea_bug.py`

**ANTES de correr el script (TL hace a mano)**:

1. Crear el ASSIGNMENT local:
   ```
   knowledge/agent-tasks/assignments/ASSIGNMENT_MS-XXX_<descripcion-kebab>.md
   ```
   Usar template v3.0 con secciones: contexto, scope, archivos a tocar/no tocar, acciones git, CAs, workflow.

2. Definir CAs en JSON (lista de `{title, description}`):
   - Inline en el spec JSON, o
   - Archivo separado `cas.json`

3. Saber: rol del agente (BE/FE/DB/...), sprint, severidad, categoría del bug.

**Correr el script** (automatiza pasos 4a-4i):

```bash
# Modo interactivo (primera vez)
python3 scripts/crear_tarea_bug.py --interactive

# Modo con archivo de especificacion JSON (preferido para repetir)
python3 scripts/crear_tarea_bug.py --spec scripts/examples/bug_spec_ejemplo.json --post

# Modo CLI completo
python3 scripts/crear_tarea_bug.py \
    --parent MS-322 \
    --title "[BUG] MS-322 PR cleanup: fix lint + separar scope" \
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

**Lo que hace el script automaticamente**:
1. Auto-detecta siguiente consecutivo MS-XXX
2. Crea la tarea via POST
3. Asigna agente via PUT (workaround del gotcha)
4. Sube ASSIGNMENT.md como attachment
5. Crea todos los CAs
6. Crea bug entry en la padre
7. Crea dependency padre→hija
8. Mueve padre a task_on_hold (PUT /on-hold)
9. Genera MENSAJE_MS-XXX.md (delegando a gen_mensaje.py)
10. Postea nota en la padre informando el on_hold
11. Opcional `--post`: postea mensaje en VTT como comment

**Lo que el TL hace antes de correr el script**:
- Crear el archivo `ASSIGNMENT_MS-XXX_<descripcion>.md` localmente (template v3.0)
- Definir los CAs (mínimo 1)
- Saber el rol del agente (BE/FE/DB/etc)

**Formato del spec JSON** (ejemplo completo en `scripts/examples/bug_spec_ejemplo.json`):
```json
{
  "parent": "MS-322",
  "title": "[BUG] MS-322 ...",
  "description": "...",
  "assignee": "BE",
  "estimated_hours": 2,
  "priority": "high",
  "severity": "high",
  "bug_category": "scope_violation",
  "sprint": "S03",
  "assignment_md_path": "knowledge/.../ASSIGNMENT_MS-XXX.md",
  "cas": [
    {"title": "CA-01: ...", "description": "..."},
    {"title": "CA-02: ...", "description": "..."}
  ]
}
```

---

## DETALLE DE CADA PASO

### Paso 1 — Detectar el bug

Durante el code review (skill `/vtt-review`), si detectas:
- CI Build+Lint failing
- Scope mezclado (archivos de otra tarea en el PR)
- Errores funcionales en código entregado
- Falta de docs (LOGIC.md, devlog, manifest)
- Cualquier otra cosa que requiera corrección antes de aprobar

**No procedas a aprobar.** Pasa al Paso 2.

---

### Paso 2 — Crear tarea hija en VTT

**Endpoint**:
```
POST /api/phases/{PHASE_UUID}/tasks
```

**Phase ID Memory Service**: `c5f9f305-de20-4d09-b939-39a84654362c` (Development)

**Payload** (alineado con `PROCESO_ASIGNACION_TAREAS_v3.md` Paso 2):
```json
{
  "title": "[BUG] MS-XXX <descripcion corta>",
  "description": "<contexto del bug + lista de items + tarea padre, max 2000 chars>",
  "priorityId": "1a617554-6319-4c56-826f-8ef49a0ff9cc",
  "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
  "assignedToId": "<UUID del agente>",
  "assignedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa",
  "createdBy": "92225290-6b6b-4c1f-a940-dcb4262507aa",
  "complexity": "MEDIUM",
  "category": "bugfix",
  "type": "bug",
  "estimatedHours": 2
}
```

**Campos obligatorios según doc v3**:
- `statusId`: pending (`335fd9c6-...`) para que arranque en pending
- `assignedToId`: UUID del agente (NO `assigneeId` — gotcha #1)
- `assignedBy`: UUID del TL que asigna
- `createdBy`: UUID del TL que crea
- `description` max 2000 chars

**Nota**: aunque el doc v3 dice que `assignedToId` debería persistir desde el POST, en la práctica a veces no lo hace. El script `crear_tarea_bug.py` hace verificación + fallback con `PUT /api/tasks/{ID}` en paso 3c.

**Cómo obtener siguiente MS-XXX**:
```bash
# Paginar todas las tareas y encontrar el max
for off in 0 100 200 300; do
  curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&limit=100&offset=$off" \
    -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
tasks=json.load(sys.stdin).get('data',[])
nums=[int(t['id'].split('-')[1]) for t in tasks if t.get('id','').startswith('MS-')]
print(max(nums) if nums else 0)
"
done
# Tomar el max + 1
```

---

### Paso 3 — Generar ASSIGNMENT + subir attachment

**Archivo local**:
```
knowledge/agent-tasks/assignments/ASSIGNMENT_MS-{XXX}_<descripcion-kebab>.md
```

Usar template `ASSIGNMENT_TEMPLATE_v3.md` con estas secciones:
1. Encabezado con metadata (task_id, padre, asignado, sprint, worktree, etc.)
2. CONTEXTO (qué bugs hay, link al PR/comments donde se detectaron)
3. SCOPE (archivos a tocar, archivos a NO tocar)
4. ACCIONES (pasos concretos, comandos git)
5. CRITERIOS DE ACEPTACIÓN (1 por bug + verificación)
6. ENTREGABLES (branches, PRs, SKL-REPORT-01)
7. WORKFLOW (in_progress → in_review)

**Subir como attachment**:
```
POST /api/tasks/{TASK_ID}/attachments
Content-Type: multipart/form-data
```

Form fields:
- `file`: el archivo .md
- `fileType`: `"assignment"`
- `uploadedById`: UUID del TL (`92225290-6b6b-4c1f-a940-dcb4262507aa`)

Ejemplo Python:
```python
import urllib.request, uuid
boundary = "----vtt" + uuid.uuid4().hex
body = (
    f"--{boundary}\r\nContent-Disposition: form-data; name=\"fileType\"\r\n\r\nassignment\r\n"
    f"--{boundary}\r\nContent-Disposition: form-data; name=\"uploadedById\"\r\n\r\n{TL}\r\n"
    f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
    f"Content-Type: text/markdown\r\n\r\n"
).encode() + content + f"\r\n--{boundary}--\r\n".encode()
```

---

### Paso 3b — Crear los Criterios de Aceptación (CAs)

**Endpoint** (doc v3 Paso 6):
```
POST /api/tasks/{TASK_ID}/criteria
```

**Payload por CA**:
```json
{
  "title": "CA-01: <criterio>",
  "description": "<como se verifica>",
  "criteriaTypeCode": "acceptance",
  "required": true,
  "order": 1
}
```

**Gotchas (doc v3 gotcha #2)**:
- Campo es `criteriaTypeCode`, **NO** `type`
- Endpoint es `/criteria`, **NO** `/acceptance-criteria`
- `required: true` para CAs que deben estar `met` antes de aprobar

Crear 1 CA por bug + CAs de verificación (CI verde, lint clean, tests passing, etc.)

---

### Paso 3c — Asignar el agente (workaround del gotcha)

`POST /api/phases/:id/tasks` ignora el assignee al crear. Después del paso 2:

**Endpoint**:
```
PUT /api/tasks/{TASK_ID}
```

**Payload**:
```json
{
  "assignedToId": "<UUID del agente>"
}
```

⚠️ **CAMPO CRÍTICO**: usar **`assignedToId`**, NO `assigneeId`.

VTT acepta `assigneeId` y devuelve `200 OK` con success=true, pero **no persiste** el assignee. El campo canónico que SÍ persiste es `assignedToId`. Validado el 2026-05-21 con la prueba de MS-376.

Verificar:
```bash
curl -s "http://77.42.88.106:3000/api/tasks/{TASK_ID}" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.assignee'
# debe devolver {id, name, email, role}, NO null
```

---

### Paso 4 — LIGAR BUG + MOVER PADRE A on_hold (CRÍTICO)

Este es el paso más importante. Sin él las métricas se rompen.

**4a. Crear el bug entry (issue) en la tarea PADRE**:

```
POST /api/tasks/{PADRE_ID}/issues
```

Payload:
```json
{
  "type": "bug",
  "title": "[TASK:MS-XXX-hija] [SPRINT:SX] <descripcion corta del bug>",
  "description": "[TASK:MS-XXX-hija] [SPRINT:SX] <lista de items + referencia a tarea hija>",
  "severity": "high",
  "reportedById": "<UUID del TL>"
}
```

**Severidades válidas**: `critical | high | medium | low`
**Tipos válidos**: `bug | question | requirement | other`

#### ⚠️ Limitación crítica del linking issue ↔ tarea hija

**VTT NO acepta `resolvedByTaskId` ni campos similares en el POST de issue.** Validado el 2026-05-21:
- POST acepta `resolvedByTaskId: "MS-XXX"` con 200 OK pero NO persiste (queda null)
- Mismo comportamiento con `resolutionTaskId`, `linkedTaskId`, `fixTaskId`, `blockedById`, `childTaskId`, `derivedTaskId`
- PUT/PATCH `/issues/{id}` no existen (404)

**Workaround para ligar bug → hija (3 mecanismos paralelos)**:

1. **Marker textual obligatorio en title + description**:
   ```
   "title": "[TASK:MS-XXX] [SPRINT:SX] PR cleanup ..."
   "description": "[TASK:MS-XXX] [SPRINT:SX] Tarea hija MS-XXX creada para resolver. ..."
   ```
   Mismo patrón que doc v3 §12.2 usa para evidencias.

2. **`onHoldIssueId` en el PUT /on-hold** (paso 4c) apunta al issue específico.

3. **Dependency `blocks`** (paso 4b) crea la relación formal padre→hija.

**Guardar el `id` del issue** — se usa en 4c.

**4b. Crear dependencia padre-hija**:

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

**4c. Mover padre a `task_on_hold`**:

⚠️ **NUNCA usar PATCH `/status` para `on_hold`**. Usar el endpoint dedicado:

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
  "raisedById": "<UUID del TL>"
}
```

Tipos válidos en el campo `type`: `bug | question | requirement | other`

Verificar:
```bash
curl -s "http://77.42.88.106:3000/api/tasks/{PADRE_ID}" \
  -H "Authorization: Bearer $TOKEN" | jq '.data | {status: .status.code, isBlocked}'
# Esperado: status=task_on_hold, isBlocked=true
```

---

### Paso 5 — Generar mensaje + postear en VTT

**Script automatizado**:
```bash
python3 scripts/gen_mensaje.py MS-XXX --post
```

Auto-detecta:
- Email del agente asignado (desde `assignee.email` de VTT)
- CAs creados (los lista en el mensaje)
- ASSIGNMENT path (desde attachments)
- Worktree dedicado del agente

**Gotcha**: Si la tarea no tiene `assignee` poblado (paso 3c no se ejecutó), el script falla con: `ERROR: agente con email '' no esta en el mapa`.

**Archivo generado**:
```
knowledge/agent-tasks/messages/04-development/{SPRINT}/MENSAJE_MS-{XXX}.md
```

Con `--post`, además crea comment en VTT vía:
```
POST /api/tasks/{TASK_ID}/comments
```

Payload manual (si necesitas postear sin script):
```json
{
  "userId": "<UUID del TL>",
  "message": "<contenido del mensaje>"
}
```

---

### Paso 6 — Agente trabaja la tarea hija

El agente:
1. Lee el mensaje en VTT (su comment más reciente)
2. Lee el ASSIGNMENT adjunto
3. Mueve a in_progress (NO el TL):
   ```
   PATCH /api/tasks/{HIJA_ID}/status
   Body: {"statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56", "changedBy": "<agent_uuid>"}
   ```
4. Trabaja la corrección en su worktree
5. Registra devlog entries:
   ```
   POST /api/tasks/{HIJA_ID}/devlog-entries
   Body: {"entries": [{"categoryCode": "decision", "title": "...", "reportedBy": "<agent_uuid>"}]}
   ```
6. Marca CAs como `met` conforme avanza:
   ```
   PATCH /api/tasks/{HIJA_ID}/criteria/{CA_ID}
   Body: {"status": "met", "evidence": "<evidencia concreta>"}
   ```

---

### Paso 7 — Agente reporta entrega

El agente:
1. Verifica review-gate:
   ```
   GET /api/tasks/{HIJA_ID}/review-gate
   ```
   Debe retornar `canProceedToReview: true`.
2. Sube devlog y code-logic como attachments (`fileType=devlog`, `fileType=code_logic`).
3. Crea PR en GitHub.
4. Genera SKL-REPORT-01 (`.md` local + comment en VTT).
5. Genera task manifest v1.0:
   ```bash
   python3 $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
     --task-id MS-XXX --version 1.0 --agent-uuid <agent_uuid> \
     --report-path knowledge/agent-tasks/reports/04-development/{SPRINT}/MS-XXX_REPORT.md \
     --phase 04-development --sprint {SPRINT} --upload
   ```
6. Mueve a in_review:
   ```
   PATCH /api/tasks/{HIJA_ID}/status
   Body: {"statusId": "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d", "changedBy": "<agent_uuid>"}
   ```

---

### Paso 8 — TL revisa la tarea hija

Ejecutar skill `/vtt-review MS-XXX` que valida:

| Check | Endpoint |
|-------|----------|
| Status = task_in_review | `GET /api/tasks/{HIJA_ID}` |
| Todos los CAs en `met` | `GET /api/tasks/{HIJA_ID}/criteria` |
| Review gate `canProceedToReview: true` | `GET /api/tasks/{HIJA_ID}/review-gate` |
| 0 issues abiertos | `GET /api/tasks/{HIJA_ID}/issues` |
| Devlog entries registrados | `GET /api/tasks/{HIJA_ID}/devlog` |
| PR existe + CI verde | `gh pr view <num> --json statusCheckRollup` |
| Devlog/code-logic/manifest commited | `git status` + `git log` en worktree del agente |

Si algo falla → postear NEEDS_FIXES (no crear nueva hija; la corrección se queda en la misma hija).

Si todo OK → **Paso 9**.

---

### Paso 9 — Aprobar hija + liberar padre (con modelo dinámico)

Sigue el ciclo completo del doc v3 (Pasos 8-16) aplicado a la tarea hija de bug:

**9.1 — Verificaciones (doc v3 Pasos 8-11)**:
- Review gate `canProceedToReview: true`
- Todos los CAs en `met`
- Attachments completos (devlog, code_logic, manifest)
- PR mergeable

**9.2 — Modelo dinámico (doc v3 Paso 12 — SKL-DYNAMIC-MODEL-01)**:

Si el agente reportó TIs nuevos o tech_debt en el SKL-REPORT-01:

```bash
# Crear TI por cada item del reporte
curl -s -X POST "$BASE/api/projects/$PROJECT_ID/trackable-items" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "code": "DEBT-XXX-NN",
    "title": "[DEFER R2] <titulo>",
    "typeCode": "tech_debt",
    "statusCode": "ti_draft",
    "createdById": "<TL_UUID>"
  }'

# Vincular TI a la tarea
curl -s -X POST "$BASE/api/trackable-items/<TI_ID>/tasks" \
  -d '{"taskId":"<HIJA_ID>","linkType":"related_to"}'

# Agregar evidencia (PR) — endpoint singular /evidence (gotcha #11)
curl -s -X POST "$BASE/api/trackable-items/<TI_ID>/evidence" \
  -d '{
    "type": "link",
    "title": "[MS-XXX] [SX] PR fix lint + scope cleanup",
    "url": "https://github.com/.../pull/N",
    "description": "[TASK:MS-XXX] [SPRINT:SX] PR de la tarea hija que cierra el bug",
    "createdById": "<TL_UUID>"
  }'
```

**Resolver devlog entries (doc v3 Paso 12.3)**:

```bash
curl -s -X PATCH "$BASE/api/tasks/{HIJA_ID}/devlog/<ENTRY_ID>/status" \
  -d '{
    "status": "resolved",
    "resolution": "Revisado por TL durante cierre de bug MS-XXX. <decision/observacion>."
  }'
```

⚠️ Gotcha #13: `resolution` es REQUERIDO cuando status=`resolved` o `wont_fix`. Sin él → 400.

**9.3 — APR-TL Comment (doc v3 Paso 13)**:

```bash
curl -s -X POST "$BASE/api/tasks/{HIJA_ID}/comments" \
  -d '{
    "message": "## APR-TL: MS-XXX aprobado tras code review + modelo dinamico aplicado\n\n...",
    "userId": "<TL_UUID>"
  }'
```

Máximo 5000 chars (gotcha #5).

**9.4 — Mover hija a `task_completed` (doc v3 Paso 14)**:

```bash
curl -s -X PATCH "$BASE/api/tasks/{HIJA_ID}/status" \
  -d '{
    "statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97",
    "changedBy": "<TL_UUID>",
    "reason": "APR-TL: bug MS-XXX cerrado, padre lista para re-review"
  }'
```

**9.5 — Liberar padre de on_hold**:

```
PUT /api/tasks/{PADRE_ID}/release-hold
Body: {"releasedById": "<TL_UUID>", "reason": "Tarea hija MS-XXX aprobada"}
```

La padre vuelve al estado previo (`task_in_review`).

**9.6 — Manifest al FINAL (doc v3 Paso 15)**:

```
POST /api/tasks/{HIJA_ID}/attachments
fileType=manifest
```

⚠️ Regla crítica doc v3: manifest se genera DESPUÉS de attachments + status + dynamic model.

Status IDs Memory Service (de doc v3):
| Status | UUID |
|--------|------|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

Verificar:
```bash
curl -s "$BASE/api/tasks/{PADRE_ID}" | jq '.data | {status: .status.code, isBlocked}'
# Esperado: status=task_in_review, isBlocked=false
```

---

### Paso 10 — Continuar la tarea padre

Una vez la padre está liberada:
1. Si quedó en `task_in_review`: TL ejecuta `/vtt-review` sobre la padre con el código ya corregido.
2. Si todo pasa → aprobar normal (`PATCH /status` a `task_completed`).
3. Si encuentra MÁS bugs → repetir desde Paso 1 (puede haber varias hijas por una padre).

---

## EJEMPLO REAL — MS-322 → MS-375

Caso documentado el 2026-05-21:

**Padre**: MS-322 (API Endpoints — 11 endpoints)
**Bugs detectados en review**:
1. CI Build+Lint falló con 53 errores (curly, no-misused-promises, require-await)
2. PR mezcla archivos de MS-327 (multer.ts, redis.ts)
3. PR mezcla cleanupJob.ts (stub MS-323)

**Hija creada**: MS-375 ([BUG] MS-322 PR cleanup)

**IDs registrados**:
- ASSIGNMENT attachment: `34dc47c7-6bb0-4ee5-a9a6-25f48836ee2f`
- Issue en MS-322: `bf32703b-edd1-46c0-8ff6-883a8344e800`
- Dependency MS-322 → MS-375: `2a4a39ea-f989-4ff7-ab20-e8808937b9e5`
- 7 CAs creados: CA-01..CA-07
- Comment activación: `c72c5571-e73d-4736-b339-5377434af9ee`

**Estado final**:
- MS-322: `task_on_hold` + `isBlocked: true`
- MS-375: `task_pending` con assignee=BE

---

## TABLA DE ENDPOINTS USADOS (RESUMEN)

| Acción | Método | URL |
|--------|:------:|-----|
| Listar tareas (paginadas) | GET | `/api/tasks?projectId=&limit=100&offset=N` |
| Ver tarea | GET | `/api/tasks/{ID}` |
| Crear tarea | POST | `/api/phases/{PHASE_ID}/tasks` |
| Actualizar tarea (asignar) | PUT | `/api/tasks/{ID}` |
| Cambiar status | PATCH | `/api/tasks/{ID}/status` |
| Mover a on_hold | PUT | `/api/tasks/{ID}/on-hold` |
| Liberar de on_hold | PUT | `/api/tasks/{ID}/release-hold` |
| Subir attachment | POST | `/api/tasks/{ID}/attachments` (multipart) |
| Crear CA | POST | `/api/tasks/{ID}/criteria` |
| Marcar CA met | PATCH | `/api/tasks/{ID}/criteria/{CA_ID}` |
| Crear bug entry | POST | `/api/tasks/{ID}/issues` |
| Resolver bug entry | PATCH | `/api/tasks/{ID}/issues/{ISSUE_ID}` |
| Listar issues | GET | `/api/tasks/{ID}/issues` |
| Crear dependencia | POST | `/api/tasks/{ID}/dependencies` |
| Listar dependencias | GET | `/api/tasks/{ID}/dependencies` |
| Postear comentario | POST | `/api/tasks/{ID}/comments` |
| Listar comentarios | GET | `/api/tasks/{ID}/comments` |
| Ver review-gate | GET | `/api/tasks/{ID}/review-gate` |
| Listar devlog entries | GET | `/api/tasks/{ID}/devlog` |
| Crear devlog entry | POST | `/api/tasks/{ID}/devlog-entries` |
| Obtener JWT token | POST | `/api/auth/service-token` |
| Listar proyectos | GET | `/api/projects` |
| Ver sprint | GET | `/api/sprints/{SPRINT_ID}` |

**Base URL**: `http://77.42.88.106:3000`

---

## STATUS IDs MEMORY SERVICE

| Estado | UUID |
|--------|------|
| task_pending | (se asigna por defecto al crear) |
| task_assigned | (no usado en MS) |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |
| task_approved | (movido por PM, no TL) |
| task_blocked | (sistema asigna por dependencias) |

**Quién mueve cada status (regla VTT)**:

| Status destino | Quién lo mueve |
|----------------|----------------|
| task_in_progress | **Agente asignado** (NO el TL) |
| task_in_review | Agente |
| task_completed | TL Reviewer |
| task_on_hold | TL (via `PUT /on-hold`, NO via PATCH /status) |
| task_approved | PM |
| task_rejected | TL Reviewer |

---

## USER IDs MEMORY SERVICE

| Rol | UUID | Email |
|-----|------|-------|
| TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` | tl@memory-service.vtt.ai |
| BE | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | backend@memory-service.vtt.ai |
| DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | memory-service.db@vtt.ai |
| FE | `d23c9cd9-a156-433b-8900-94add5488eec` | memory-service.fe@vtt.ai |
| QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | memory-service.qa@vtt.ai |
| DevOps | `322e3745-9756-4a7c-af11-44b33edef44d` | memory-service.devops@vtt.ai |
| DL | `b3a09269-cded-468c-a475-15a48f203cb0` | memory-service.dl@vtt.ai |
| UX | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` | memory-service.ux@vtt.ai |
| AR | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | ar@memory-service.vtt.ai |
| SA | `0c128e3b-db3b-4e31-b107-0379b5791233` | sa@memory-service.vtt.ai |

---

## PRIORITY IDs

| Prioridad | UUID |
|-----------|------|
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |
| medium | (consultar en VTT) |
| low | (consultar en VTT) |

---

## GOTCHAS DOCUMENTADOS

Tabla consolidada combinando los del `PROCESO_ASIGNACION_TAREAS_v3.md` + descubiertos en pruebas de bug:

| # | Concepto | Detalle | Origen |
|---|----------|---------|--------|
| 1 | `assignedToId` NO `assigneeId` | Backend acepta `assigneeId` con 200 OK pero ignora silenciosamente. Solo `assignedToId` persiste. | doc v3 + MS-376 |
| 2 | `criteriaTypeCode` NO `type` | Para CAs. Endpoint `/criteria` NO `/acceptance-criteria` | doc v3 |
| 3 | `PUT /deliveries` NO PATCH | El template antiguo decía PATCH | doc v3 |
| 4 | JSON requiere wrapper `.md` | Backend whitelist no incluye `application/json` para attachments | doc v3 |
| 5 | Comments ≤ 5000 chars | Dividir o adjuntar archivo | doc v3 |
| 6 | Severity devlog enum no nullable | Usar `"low"` mínimo | doc v3 |
| 7 | GET `/devlog` singular, POST `/devlog-entries` plural | Verbos opuestos en el mismo recurso | doc v3 |
| 8 | Review Gate exige code_logic | Incluso documentation/deployment → placeholder N/A | doc v3 |
| 9 | TI create scoped a project | `POST /api/projects/:id/trackable-items` (no global) | doc v3 |
| 10 | Evidence endpoint singular `/evidence` | NO `/evidences` | doc v3 |
| 11 | Evidence enum type | `document\|link\|test_result\|screenshot` (NO `pr`) | doc v3 |
| 12 | Devlog resolve requiere `resolution` | Cuando status=resolved/wont_fix; sin él 400 | doc v3 |
| 13 | `/defer` NO existe | Marker `[DEFER R2]` textual | doc v3 |
| 14 | `process_improvement` NO válido en software | Usar `tech_debt` + `[PROCESS]` marker | doc v3 |
| 15 | DELETE evidence NO existe | Cuidar formato al crear | doc v3 |
| 16 | `GET /tasks/:id/trackable-items` NO existe | Iterar TIs del proyecto | doc v3 |
| 17 | Manifest al FINAL | Generar AFTER attachments + status + dynamic_model (lección PROC-MANIFEST-01) | doc v3 |
| 18 | PATCH `/status` con `task_on_hold` falla | Usar PUT `/on-hold` con payload completo | descubierto |
| 19 | PATCH `/status` requiere `statusId` no `statusCode` | Obtener UUID primero | descubierto |
| 20 | task_pending → task_in_review requiere devlog + code-logic | Sin ellos: 400 REQUIREMENTS_NOT_MET | descubierto |
| 21 | task_pending → task_completed bloqueado | Debe pasar por in_progress → in_review | descubierto |
| 22 | Issue `resolvedByTaskId` no persiste en POST | VTT acepta el campo con 200 OK pero ignora. No hay PUT/PATCH `/issues/{id}` (404). Linking via marker textual `[TASK:MS-XXX]` | descubierto MS-376 |
| 23 | Windows cp1252 falla con `→` | Usar UTF-8 explícito en Python (`encode("utf-8")`) | descubierto |
| 24 | Pagination max limit 100 por página | No 300, hay que paginar | descubierto |
| 25 | El TL SÍ puede ser assignee | No es limitación del modelo, solo del campo. Validado en MS-376. | descubierto |

---

## CHECKLIST FINAL DEL TL ANTES DE CERRAR EL BUG

### Antes de correr crear_tarea_bug.py (a mano)
```
[ ] 1. Bug detectado durante review (no fix inline)
[ ] 2. ASSIGNMENT_MS-XXX_<desc>.md escrito en knowledge/agent-tasks/assignments/
[ ] 3. Lista de CAs definida (spec JSON o cas.json)
[ ] 4. Rol del agente confirmado (BE/FE/DB/...)
[ ] 5. Padre existe en VTT y esta en estado revisable
```

### Despues de correr crear_tarea_bug.py (auto-verificado)
```
[ ] 6. Tarea hija creada con consecutivo MS-XXX (no acronimos)
[ ] 7. Agente asignado via PUT /api/tasks/{ID}
[ ] 8. ASSIGNMENT subido como attachment
[ ] 9. CAs creados (1 por bug + verificacion)
[ ] 10. Bug entry creado en padre (POST /issues)
[ ] 11. Dependencia creada (POST /dependencies)
[ ] 12. Padre movido a task_on_hold (PUT /on-hold)
[ ] 13. Mensaje generado (+ posteado si --post)
[ ] 14. Archivo MENSAJE en knowledge/agent-tasks/messages/{phase}/{sprint}/
[ ] 15. Nota informativa posteada en la padre
```

### Despues de que el agente entregue y se apruebe
```
[ ] 16. CAs de la hija todos en met
[ ] 17. Review gate canProceedToReview=true
[ ] 18. PR de la hija con CI verde
[ ] 19. Bug entry resuelto en padre (PATCH /issues)
[ ] 20. Padre liberada de on_hold (PUT /release-hold)
[ ] 21. Memoria actualizada si hay aprendizajes nuevos
```

---

**Documento:** GUIA_MANEJO_BUGS_TL.md
**Versión:** 1.0
**Fecha:** 2026-05-21
**Autor:** TL Reviewer Memory Service
**Aplicable a:** Cualquier TL en proyectos VTT con stack identico
