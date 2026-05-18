# Catálogo de Skills — Memory Service

| Campo | Valor |
|-------|-------|
| **Versión** | 1.2 |
| **Fecha** | 2026-05-12 |
| **Proyecto** | Memory Service (R1) |
| **Propósito** | Referencia para Orquestador, Prompt Builder y TL — qué skills existen, qué hacen, qué inyectar |

---

## 1. Concepto: Skills vs Documentos Operativos

```
DOCUMENTO OPERATIVO (.md)          SKILL
─────────────────────────          ─────
Quién soy, reglas, contexto   →    Qué ejecutar, cómo ejecutarlo
Leído por el agente           →    Inyectado en WORKFLOW del prompt
Completo (~800 tokens)        →    Atómico (~60–150 tokens por skill)
Fallback cuando hay dudas     →    Instrucción precisa para acción concreta
```

**Cuándo usar cada uno:**

| Situación | Qué inyectar |
|-----------|-------------|
| Agente nuevo ejecutando primera tarea | Documento Operativo completo (sección WORKFLOW) |
| Agente experimentado con tarea clara | Solo skills relevantes para esa tarea |
| Tarea de mantenimiento simple | 2–3 skills específicas |
| Debug / diagnóstico | Skill + sección ESCALACIÓN del OPERATIVO |

---

## 2. Formato de una Skill

Cada skill es un **archivo Markdown** (no script Python). El agente lee la skill y ejecuta los comandos dentro.

**¿Por qué MD y no script Python?**

| Python script | Markdown skill |
|---------------|----------------|
| El agente ejecuta el script | El agente lee las instrucciones y ejecuta los curl/git |
| Requiere entorno configurado | Solo necesita bash + curl (ya disponibles) |
| Difícil de auditar qué hace | Transparente: el agente muestra cada comando |
| Versionar scripts es complejo | Versionar MD es trivial |
| No permite decisión contextual | El agente puede adaptar según contexto |

**Estructura estándar de skill:**

```markdown
# SKL-[CAT]-[NUM]: [Nombre de la skill]

**Categoría:** [VTT-OPS / GIT-OPS / FILE-OPS / REPORT]
**Aplica a:** [PM, TL, BE, ...] o "Todos"
**Tokens estimados:** ~XX

## Precondición
[Qué debe ser verdad antes de ejecutar]

## Variables requeridas
- `$TOKEN` — JWT obtenido con auth (ver SKL-AUTH-01)
- `$TASK_ID` — ID de la tarea (ej: MS-145)
- `$AGENT_UUID` — UUID del agente (de su .env)

## Ejecución
[Comandos exactos con placeholders]

## Validación
[Cómo saber si funcionó]

## Error común
[Qué falla frecuentemente y cómo resolverlo]
```

---

## 3. Credenciales del Agente — Patrón `.env`

Cada agente tiene un `.env` (o sección en su OPERATIVO) con:

```bash
# .env del agente (en workspace del agente)
VTT_BASE_URL=http://77.42.88.106:3000
AGENT_UUID=<UUID del agente en VTT>
SERVICE_KEY=hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
PROJECT_ID=d0fc276d-e764-4a83-96e9-d65f086ed803
PROJECT_KEY=MS
```

Las skills referencian estas variables como `$AGENT_UUID`, `$SERVICE_KEY`, etc.
El agente las carga desde su `.env` al inicio de sesión (SKL-AUTH-01).

---

## 4. Catálogo Completo

### 4.1 Categoría: AUTH — Autenticación

---

#### SKL-AUTH-01: Obtener JWT de Sesión

**Aplica a:** Todos  
**Tokens estimados:** ~80  
**Cuándo:** Al iniciar cualquier sesión, antes de cualquier llamada VTT

```python
import urllib.request, json, os

req = urllib.request.Request(
    f"{os.getenv('VTT_BASE_URL')}/api/auth/service-token",
    data=json.dumps({
        'userId': os.getenv('AGENT_UUID'),
        'serviceKey': os.getenv('SERVICE_KEY')
    }).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
response = json.loads(urllib.request.urlopen(req).read())
TOKEN = response['data']['token']
print(f"TOKEN obtenido: {TOKEN[:20]}...")
```

**Validación:** `TOKEN` no es vacío, empieza con `eyJ`  
**Error común:** `SERVICE_KEY` incorrecto → 401. Verificar en `.env`.

---

### 4.2 Categoría: VTT-TASK — Gestión de Tareas (crear, asignar, notificar)

---

#### SKL-TASK-01: Crear Tarea en VTT

**Aplica a:** TL  
**Tokens estimados:** ~180  
**Cuándo:** FASE 1 — al crear una tarea nueva a partir de un handoff

**Reglas clave:**
- R1: Toda tarea debe pertenecer a un Delivery (nunca huérfana). Si es bug → Delivery `BUGS` de su fase.
- R2: Toda tarea debe tener al menos una dependencia. Si no hay dependencia obvia → confirmar con PM antes de crear.

Ver skill completa: `00-platform/06.Skills/vtt-task/SKL-TASK-01_crear-tarea.md`

---

#### SKL-TASK-02: Generar ASSIGNMENT

**Aplica a:** TL  
**Tokens estimados:** ~200  
**Cuándo:** FASE 2 — antes de asignar, para preparar el documento de instrucciones al agente

Pasos: verificar dependencias de datos → leer artefactos reales del codebase → escribir ASSIGNMENT con 8 elementos obligatorios + sección "Documentos de referencia OBLIGATORIOS".

Ver skill completa: `00-platform/06.Skills/vtt-task/SKL-TASK-02_generar-assignment.md`

---

#### SKL-TASK-03: Asignar Tarea a Agente

**Aplica a:** TL  
**Tokens estimados:** ~150  
**Cuándo:** FASE 2 — después de tener el ASSIGNMENT listo, para asignar formalmente la tarea

Pasos: subir ASSIGNMENT como attachment → PATCH `assignedToId`.

Ver skill completa: `00-platform/06.Skills/vtt-task/SKL-TASK-03_asignar-tarea.md`

---

#### SKL-TASK-04: Generar Mensaje para el Agente

**Aplica a:** TL  
**Tokens estimados:** ~130  
**Cuándo:** FASE 2 — después de asignar, para que el PM lo pegue como comentario en la tarea

Ver skill completa: `00-platform/06.Skills/vtt-task/SKL-TASK-04_mensaje-agente.md`

---

#### SKL-TASK-05: Review de Tarea

**Aplica a:** TL  
**Tokens estimados:** ~170  
**Cuándo:** Cuando una tarea llega a `task_in_review` — leer entregables, verificar checklist, decidir

Pasos: leer attachments + comentarios → verificar checklist del assignment → entregables obligatorios → consistencia técnica → issues abiertos → APR-TL + task_completed / feedback / on-hold.

Ver skill completa: `00-platform/06.Skills/vtt-task/SKL-TASK-05_review-tarea.md`

---

### 4.3 Categoría: VTT-STATUS — Cambios de Estado de Tarea

---

#### SKL-STATUS-01: Mover tarea a `task_in_progress`

**Aplica a:** BE, DB, FE, QA, DO, DL, UX, TL, AR, SA  
**Tokens estimados:** ~70  
**Cuándo:** Al iniciar trabajo en una tarea

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"2a76888a-e595-4cfc-ac4c-a3ae5087ef56\", \"changedBy\": \"$AGENT_UUID\"}"
```

**Validación:** HTTP 200, campo `status` del response = `task_in_progress`  
**Error común:** 400 si `statusId` o `changedBy` son inválidos. Verificar UUIDs.

---

#### SKL-STATUS-02: Mover tarea a `task_in_review`

**Aplica a:** BE, DB, FE, QA, DO, DL, UX, TL, AR, SA  
**Tokens estimados:** ~70  
**Cuándo:** Al completar trabajo, antes de notificar al revisor

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d\", \"changedBy\": \"$AGENT_UUID\"}"
```

**Validación:** HTTP 200, campo `status` = `task_in_review`

---

#### SKL-STATUS-03: Mover tarea a `task_completed` (solo TL)

**Aplica a:** TL  
**Tokens estimados:** ~70  
**Cuándo:** Después de aprobar revisión técnica de una tarea

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"aa5ceb90-5209-42a2-b874-a8cbee597a97\", \"changedBy\": \"$AGENT_UUID\"}"
```

**Validación:** HTTP 200, campo `status` = `task_completed`  
**Restricción:** Solo TL puede usar esta skill. PM usa SKL-STATUS-04.

---

#### SKL-STATUS-04: Mover tarea a `task_approved` (solo PM)

**Aplica a:** PM  
**Tokens estimados:** ~75  
**Cuándo:** Después de aprobación funcional (APR-PM)

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"b9ca4951-6e14-4d82-b1d8-440793bbaf47\", \"changedBy\": \"$AGENT_UUID\"}"
```

**Validación:** HTTP 200, campo `status` = `task_approved`  
**Regla crítica:** PM DEBE comentar `APR-PM: [notas]` con SKL-COMMENT-01 ANTES de ejecutar esta skill.

---

#### SKL-STATUS-05: Poner tarea en `task_on_hold` (blocker)

**Aplica a:** Todos (excepto PM que usa SKL-STATUS-06)  
**Tokens estimados:** ~90  
**Cuándo:** Cuando hay un blocker real que impide continuar  
**CRÍTICO:** Usar `PUT /on-hold`, NUNCA `PATCH /status` para on_hold

```bash
curl -s -X PUT "$VTT_BASE_URL/api/tasks/$TASK_ID/on-hold" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-user-id: $AGENT_UUID" \
  -d "{
    \"type\": \"blocker\",
    \"title\": \"$BLOCKER_TITLE\",
    \"description\": \"$BLOCKER_DESCRIPTION\"
  }"
```

**Variables adicionales:**
- `$BLOCKER_TITLE` — Título corto del blocker (ej: "Falta schema de BD para continuar")
- `$BLOCKER_DESCRIPTION` — Descripción detallada

**Validación:** HTTP 200  
**Error común:** Usar `PATCH /status` en vez de `PUT /on-hold` → tarea queda en estado incorrecto. SIEMPRE usar `PUT /on-hold`.

---

#### SKL-STATUS-06: Rechazar tarea (solo PM)

**Aplica a:** PM  
**Tokens estimados:** ~70  
**Cuándo:** Después de revisión funcional que NO cumple criterios

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"335fd9c6-f0d6-4966-a6ea-f518c78bc422\", \"changedBy\": \"$AGENT_UUID\"}"
```

**Validación:** HTTP 200  
**Regla:** Siempre agregar comentario con feedback específico con SKL-COMMENT-01 ANTES de rechazar.

---

### 4.4 Categoría: VTT-QUERY — Consultas de Tareas

---

#### SKL-QUERY-01: Obtener mis tareas asignadas

**Aplica a:** Todos  
**Tokens estimados:** ~60  
**Cuándo:** Rutina de apertura de sesión

```bash
curl -s "$VTT_BASE_URL/api/tasks?assigneeId=$AGENT_UUID&status=task_assigned" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

#### SKL-QUERY-02: Obtener tareas en revisión del proyecto

**Aplica a:** TL, PM  
**Tokens estimados:** ~60  
**Cuándo:** Para revisar qué hay pendiente de review

```bash
curl -s "$VTT_BASE_URL/api/tasks?projectId=$PROJECT_ID&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

#### SKL-QUERY-03: Obtener detalle de una tarea

**Aplica a:** Todos  
**Tokens estimados:** ~55  
**Cuándo:** Para leer acceptance criteria, devlog entries, attachments

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

#### SKL-QUERY-04: Obtener avance por fases del proyecto

**Aplica a:** PJM, TL, PM  
**Tokens estimados:** ~60  
**Cuándo:** Reporte semanal, apertura de sesión PJM

```bash
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/phases" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

#### SKL-QUERY-05: Estado de fase activa — qué tareas se pueden asignar

**Aplica a:** TL, SA Reviewer, PM  
**Tokens estimados:** ~120  
**Cuándo:** Al revisar el avance de una fase para decidir qué asignar en el próximo ciclo

Ver archivo completo: `vtt-task/SKL-QUERY-05_estado-fase-asignable.md`

**Qué hace:**
1. Lista todas las tareas de una fase agrupadas por status
2. Verifica si cada tarea pending tiene ASSIGNMENT subido
3. Produce un reporte con 3 columnas: asignables ahora / sin ASSIGNMENT / bloqueadas
4. Sugiere acción concreta para cada grupo

**Output esperado:**
```
=== TASK_PENDING (4) ===
  MS-048 | Environment Setup | sin asignar
  MS-049 | DB Schema | sin asignar
...
=== TASK_IN_REVIEW (1) ===
  MS-039 | Architecture | memory-service.ar@vtt.ai
```

---

### 4.5 Categoría: VTT-COMMENT — Comentarios en Tareas

---

#### SKL-COMMENT-01: Agregar comentario en tarea

**Aplica a:** Todos  
**Tokens estimados:** ~75  
**CRÍTICO:** Campos son `message` + `userId`. NUNCA `content` + `authorId`.

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"$COMMENT_MESSAGE\",
    \"userId\": \"$AGENT_UUID\"
  }"
```

**Variable:** `$COMMENT_MESSAGE` — texto del comentario  
**Validación:** HTTP 201  
**Error común:** Usar `content` en vez de `message` → 400 Bad Request.

---

#### SKL-COMMENT-02: Comentario de aprobación APR-PM

**Aplica a:** PM  
**Tokens estimados:** ~80  
**Cuándo:** Al aprobar funcional una tarea — ejecutar ANTES de SKL-STATUS-04

```bash
COMMENT_MESSAGE="APR-PM: tarea aprobada funcionalmente. Acceptance criteria verificados: [LISTA]. Notas: [NOTAS_OPCIONALES]"

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\": \"$COMMENT_MESSAGE\", \"userId\": \"$AGENT_UUID\"}"
```

---

#### SKL-COMMENT-03: Comentario de aprobación APR-TL

**Aplica a:** TL  
**Tokens estimados:** ~80  
**Cuándo:** Al aprobar técnicamente una tarea — ejecutar ANTES de SKL-STATUS-03

```bash
COMMENT_MESSAGE="APR-TL: revisión técnica aprobada. Code quality OK. Tests OK. Notas: [NOTAS_OPCIONALES]"

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\": \"$COMMENT_MESSAGE\", \"userId\": \"$AGENT_UUID\"}"
```

---

### 4.6 Categoría: VTT-ATTACH — Adjuntos

---

#### SKL-ATTACH-01: Subir archivo como attachment

**Aplica a:** Todos  
**Tokens estimados:** ~85  
**CRÍTICO:** `uploadedById` es obligatorio — sin él la API devuelve 400.

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$FILE_PATH" \
  -F "fileType=$FILE_TYPE" \
  -F "uploadedById=$AGENT_UUID"
```

**Variables:**
- `$FILE_PATH` — ruta local al archivo (ej: `knowledge/development-log/2026-05-01_MS-145_setup.md`)
- `$FILE_TYPE` — tipo: `brief`, `devlog`, `code_logic`, `spec`, `assignment`

**Validación:** HTTP 201, response incluye `id` del attachment  
**Error común:** Olvidar `-F "uploadedById=$AGENT_UUID"` → 400 Bad Request.

---

#### SKL-ATTACH-02: Subir devlog de tarea

**Aplica a:** BE, DB, FE, QA, DO, DL, UX, AR, SA  
**Tokens estimados:** ~90  
**Cuándo:** Al completar una tarea (paso 11 del workflow)

```bash
DEVLOG_PATH="knowledge/development-log/$(date +%Y-%m-%d)_${TASK_ID}_${TASK_SLUG}.md"

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$DEVLOG_PATH" \
  -F "fileType=devlog" \
  -F "uploadedById=$AGENT_UUID"
```

**Variable adicional:** `$TASK_SLUG` — nombre corto descriptivo (ej: `setup-express`)

---

### 4.7 Categoría: VTT-DEVLOG — Registro de Decisiones

---

#### SKL-DEVLOG-01: Registrar entrada de decisión en devlog

**Aplica a:** Todos  
**Tokens estimados:** ~90  
**Cuándo:** Para registrar decisiones técnicas o de producto directamente en VTT

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog-entries" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"type\": \"decision\",
    \"title\": \"$DECISION_TITLE\",
    \"description\": \"$DECISION_DESCRIPTION\",
    \"impact\": \"$IMPACT_DESCRIPTION\"
  }"
```

**Variables:**
- `$DECISION_TITLE` — título corto
- `$DECISION_DESCRIPTION` — qué se decidió y por qué
- `$IMPACT_DESCRIPTION` — qué áreas afecta

---

#### SKL-DEVLOG-02: Registrar observación en devlog

**Aplica a:** Todos  
**Tokens estimados:** ~85

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog-entries" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"type\": \"observation\",
    \"title\": \"$OBS_TITLE\",
    \"description\": \"$OBS_DESCRIPTION\"
  }"
```

---

### 4.8 Categoría: VTT-ISSUE — Issues y Blockers

---

#### SKL-ISSUE-01: Crear issue/blocker en tarea

**Aplica a:** Todos  
**Tokens estimados:** ~90  
**CRÍTICO:** Crear un issue pone la tarea en `on_hold` automáticamente en VTT. Solo usar para blockers reales.

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/issues" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"title\": \"$ISSUE_TITLE\",
    \"description\": \"$ISSUE_DESCRIPTION\",
    \"type\": \"$ISSUE_TYPE\",
    \"severity\": \"$ISSUE_SEVERITY\"
  }"
```

**Variables:**
- `$ISSUE_TYPE` — `blocker`, `requirement`, `improvement`, `bug`
- `$ISSUE_SEVERITY` — `low`, `medium`, `high`, `critical`

**Validación:** HTTP 201  
**Consecuencia:** Tarea pasa automáticamente a `on_hold` en VTT.

---

### 4.9 Categoría: GIT-OPS — Operaciones Git

---

#### SKL-GIT-01: Crear branch de tarea

**Aplica a:** BE, DB, FE, QA, DO, DL, UX, TL, AR, SA  
**Tokens estimados:** ~55  
**Cuándo:** Paso 0 del workflow — antes de cualquier modificación

```bash
git checkout -b feature/$TASK_ID
```

**Validación:** `git branch` muestra `* feature/$TASK_ID`  
**Error común:** Estar en un branch distinto de `main` al crear. Hacer `git checkout main && git pull` primero.

---

#### SKL-GIT-02: Rebase con main antes de PR

**Aplica a:** Todos  
**Tokens estimados:** ~65  
**Cuándo:** Antes de crear PR, si han pasado más de 4 horas desde la creación del branch

```bash
git fetch origin
git rebase origin/main
# Si hay conflictos: resolverlos, luego:
git push origin feature/$TASK_ID --force-with-lease
```

**Validación:** `git log --oneline -5` muestra commits de main como base  
**Error común:** Conflictos al hacer rebase → resolverlos manualmente, no forzar.

---

#### SKL-GIT-03: Commit con formato del proyecto

**Aplica a:** Todos  
**Tokens estimados:** ~70  
**Cuándo:** Paso 10 del workflow

```bash
git add $FILES_TO_ADD

git commit -m "$(cat <<'EOF'
$COMMIT_TYPE [$TASK_ID]: $COMMIT_DESCRIPTION

- $CAMBIO_1
- $CAMBIO_2

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #$TASK_ID
EOF
)"
```

**Variables:**
- `$COMMIT_TYPE` — `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- `$FILES_TO_ADD` — archivos específicos (evitar `git add .`)

---

#### SKL-GIT-04: Crear PR con gh CLI

**Aplica a:** Todos  
**Tokens estimados:** ~65  
**Cuándo:** Paso 11 del workflow — inmediatamente después del commit

```bash
gh pr create \
  --title "[$TASK_ID] $PR_TITLE" \
  --body "$(cat <<'EOF'
## Cambios
$PR_DESCRIPTION

## Cómo probar
$HOW_TO_TEST

Ver devlog: knowledge/development-log/$(date +%Y-%m-%d)_${TASK_ID}_${TASK_SLUG}.md
EOF
)" \
  --base main
```

---

### 4.10 Categoría: VTT-TRACK — Trackable Items, Acceptance Criteria y Fulfillment

---

#### SKL-TRACK-01: Linkear tarea a Trackable Item (implements)

**Aplica a:** TL  
**Tokens estimados:** ~80  
**Cuándo:** Al iniciar sprint — después de que PJM crea las tareas, el TL mapea qué RF/NFR implementa cada tarea

```python
# Para cada (task_id, trackable_item_id) del mapeo:
result = api_call(
    f"{BASE_URL}/api/trackable-items/{ITEM_ID}/tasks",
    {"taskId": TASK_ID}
)
# 409 = ya estaba linkeado, también es OK
```

**Tipos de relación:**
- `implements` → la tarea implementa directamente el requerimiento (usar para tareas de Fase 4 y 5)
- `related_to` → la tarea contribuye parcialmente (usar para NFRs con múltiples tareas)

**Referencia:** SOP-TRK-01 §4.1 — `00-platform/06.Documentos_soporte/SOP-TRK-01_trackable_items_workflow.md`

---

#### SKL-TRACK-02: Crear Acceptance Criterion en tarea

**Aplica a:** TL  
**Tokens estimados:** ~90  
**Cuándo:** Al asignar tarea — definir qué debe cumplir el agente antes de poder moverla a `task_in_review`

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/criteria" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"title\": \"$CA_TITLE\",
    \"description\": \"$CA_DESCRIPTION\",
    \"type\": \"$CA_TYPE\",
    \"required\": true
  }"
```

**Variable `$CA_TYPE`:** `functional` | `technical` | `security` | `performance` | `ux`  
**Validación:** HTTP 201, `required: true` bloquea Review Gate si no se cumple  
**Fuente de CA:** SOP-TRK-01 §5 — niveles proyecto/fase/tarea

---

#### SKL-TRACK-03: Reportar fulfillment de Acceptance Criterion

**Aplica a:** BE, DB, FE, QA, DO  
**Tokens estimados:** ~80  
**Cuándo:** Al completar implementación — marcar cada CA como met/not_met ANTES de mover a `task_in_review`

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/criteria/$CA_ID/fulfill" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"status\": \"$FULFILL_STATUS\",
    \"notes\": \"$FULFILL_EVIDENCE\"
  }"
```

**Variable `$FULFILL_STATUS`:** `met` | `not_met`  
**Variable `$FULFILL_EVIDENCE`:** evidencia concreta (ej: "Verificado en test/integration/memories.test.ts:45. PR #67.")  
**Regla:** `not_met` → agregar devlog entry tipo `blocker` o `tech_debt` según impacto

---

#### SKL-TRACK-04: Verificar Review Gate

**Aplica a:** BE, DB, FE, QA, DO (antes de mover a in_review)  
**Tokens estimados:** ~60  
**Cuándo:** Antes de ejecutar SKL-STATUS-02 — verificar que no hay blockers

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/review-gate" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
# Badge 🟢 = puede avanzar | Badge 🔴 = hay blockers (devlog entries critical/high pendientes)
```

**Si hay 🔴:** resolver devlog entries marcándolos como resueltos ANTES de intentar mover a in_review

---

#### SKL-TRACK-05: Cerrar Trackable Item (ti_approved)

**Aplica a:** TL  
**Tokens estimados:** ~75  
**Cuándo:** Cuando TODAS las tareas que implementan un RF/NFR están en `task_approved`

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/trackable-items/$ITEM_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusCode\": \"ti_approved\"}"
```

**Precondición:** Verificar con `GET /api/trackable-items/{item_id}` que todas las tareas linkeadas están `task_approved`  
**Para NFRs:** Requiere además devlog entry `testing_note` que confirme el SLA (ej: "P95 = 380ms < 500ms")

---

#### SKL-TRACK-06: Consultar Trackable Items pendientes (dashboard de sprint)

**Aplica a:** TL, PM  
**Tokens estimados:** ~65  
**Cuándo:** Al cerrar sprint — verificar qué RFs/NFRs se pueden cerrar

```bash
# RFs pendientes:
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/trackable-items?status=pending&type=rf" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# NFRs pendientes:
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/trackable-items?status=pending&type=rnf" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Acción post-query:** Por cada RF donde todas las tareas están `task_approved` → ejecutar SKL-TRACK-05

---

### 4.11 Categoría: FILE-STRUCTURE — Ubicación de Entregables

---

#### SKL-STRUCTURE-01: Ubicar entregable en estructura del proyecto

**Aplica a:** SA, DL, UX, AR, TL, BE, DB, FE, QA, DO, PJM  
**Tokens estimados:** ~120  
**Cuándo:** Antes de crear cualquier entregable — determinar ruta correcta

**Regla:** Todo entregable va en `phases/{fase}/deliverables/`. NUNCA en `docs/`, `Release2.0/`, ni carpetas ad-hoc.

Ver skill completa: `00-platform/06.Skills/file-structure/SKL-STRUCTURE-01_ubicar-entregable.md`

---

### 4.11 Categoría: REPORT — Reportes al TL/PM/Coordinador

---

#### SKL-REPORT-01: Reporte de entrega de tarea

**Aplica a:** BE, DB, FE, QA, DO, DL, UX, AR, SA  
**Tokens estimados:** ~100  
**Cuándo:** Al completar el workflow (después de cambiar status a `task_in_review`)

```markdown
## Entrega: $TASK_ID — $TASK_NAME

### Código:
- `$ARCHIVO_1` — $DESCRIPCION_1
- `$ARCHIVO_2` — $DESCRIPCION_2

### Development Log:
`knowledge/development-log/$FECHA_$TASK_ID_$SLUG.md`

### Code Logic:
- `knowledge/code-logic/$ARCHIVO.LOGIC.md`

### PR:
[$PR_URL]($PR_URL)

### Commit SHA:
$COMMIT_SHA

### Cómo probar:
$PASOS_PRUEBA
```

---

#### SKL-REPORT-02: Reporte ejecutivo PJM al PM

**Aplica a:** PJM  
**Tokens estimados:** ~110  
**Cuándo:** Diario o al final de sprint

```markdown
## Reporte Ejecutivo — $FECHA

### % Avance por Fase:
| Fase | Total | Completadas | % |
|------|-------|-------------|---|
| Setup | X | Y | Z% |
| S01 | X | Y | Z% |

### Blockers activos: $NUM_BLOCKERS
$LISTA_BLOCKERS

### En revisión >48h sin TL: $NUM_PENDIENTES
$LISTA_PENDIENTES

### Próxima oleada a asignar:
$TAREAS_PROXIMAS

### Recomendación:
$RECOMENDACION
```

---

## 5. Índice por Rol — Qué Skills inyectar

| Rol | Skills de apertura | Skills en workflow | Skills especiales |
|-----|-------------------|-------------------|-------------------|
| **PM** | AUTH-01, QUERY-01, QUERY-02 | STATUS-04 (APR-PM), COMMENT-02, STATUS-06 | STATUS-04 (solo PM) |
| **PJM** | AUTH-01, QUERY-04, QUERY-01 | COMMENT-01, ATTACH-01, **STRUCTURE-01** | REPORT-02 |
| **TL** | AUTH-01, QUERY-02, QUERY-01, **QUERY-05** | TASK-01, TASK-02, TASK-03, TASK-04, TASK-05, STATUS-03 (APR-TL), COMMENT-03, DEVLOG-01, **STRUCTURE-01**, **TRACK-01, TRACK-02, TRACK-05, TRACK-06** | STATUS-03 (solo TL) |
| **BE** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, ATTACH-02, GIT-01..04, **STRUCTURE-01**, **TRACK-03, TRACK-04** | REPORT-01 |
| **DB** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, ATTACH-02, GIT-01..04, **STRUCTURE-01**, **TRACK-03, TRACK-04** | REPORT-01 |
| **FE** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, ATTACH-02, GIT-01..04, **STRUCTURE-01**, **TRACK-03, TRACK-04** | REPORT-01 |
| **QA** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, ISSUE-01, ATTACH-02, **STRUCTURE-01**, **TRACK-03, TRACK-04** | REPORT-01 |
| **DO** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, ATTACH-02, GIT-01..04, **STRUCTURE-01**, **TRACK-03, TRACK-04** | REPORT-01 |
| **DL** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, COMMENT-01, DEVLOG-01, **STRUCTURE-01** | REPORT-01 |
| **UX** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, ATTACH-01, GIT-01..04, **STRUCTURE-01** | REPORT-01 |
| **AR** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, DEVLOG-01, ATTACH-01, **STRUCTURE-01** | REPORT-01 |
| **SA** | AUTH-01, QUERY-01 | STATUS-01, STATUS-02, DEVLOG-01, COMMENT-01, **STRUCTURE-01** | REPORT-01 |

---

## 6. Integración con Prompt Builder

### Cómo el Prompt Builder inyecta skills

Las skills se inyectan en el `runRequest` como parte de la sección **WORKFLOW** del prompt del agente, o como entradas en `context.references`:

```json
{
  "prompts": {
    "system": "[11 secciones del template, incluyendo WORKFLOW con skills]",
    "user": "[descripción de la tarea]"
  },
  "context": {
    "references": [
      { "type": "skill", "id": "SKL-AUTH-01", "content": "..." },
      { "type": "skill", "id": "SKL-STATUS-01", "content": "..." },
      { "type": "skill", "id": "SKL-REPORT-01", "content": "..." }
    ]
  }
}
```

### Estrategia de selección de skills (para el Orquestador)

```
1. Identificar rol del agente (de task.agentId → project_agents.roleCode)
2. Siempre inyectar: SKL-AUTH-01
3. Para apertura de sesión: + skills QUERY del rol
4. Para ejecución de tarea: + skills STATUS-01, STATUS-02, ATTACH-02, GIT-01..04, REPORT-01
5. Para roles especiales: + skills exclusivas (STATUS-03 para TL, STATUS-04 para PM)
6. Calcular tokens: ~60-110 por skill. Budget: 8,000 tokens total.
```

### Budget estimado por ejecución típica

| Componente | Tokens estimados |
|------------|-----------------|
| 11 secciones del template (SETUP) | ~1,200 |
| Task description (user prompt) | ~300 |
| Memory context | ~500 |
| Skills inyectadas (6–8 skills) | ~500 |
| Knowledge references | ~300 |
| **Total estimado** | **~2,800 tokens** |
| **Budget disponible** | **8,000 tokens** |
| **Margen** | **~5,200 tokens** |

---

## 7. Ubicación de Skills en el Repo

```
memory-service-project/
└── 00-platform/
    └── 06.Skills/
        ├── CATALOGO_SKILLS_MEMORY_SERVICE.md   ← este archivo
        ├── auth/
        │   └── SKL-AUTH-01_obtener-jwt.md
        ├── vtt-task/                              ← objeto: tareas (crear, asignar, status, queries, comentarios, issues, devlog)
        │   ├── SKL-TASK-01_crear-tarea.md
        │   ├── SKL-TASK-02_generar-assignment.md
        │   ├── SKL-TASK-03_asignar-tarea.md
        │   ├── SKL-TASK-04_mensaje-agente.md
        │   ├── SKL-TASK-05_review-tarea.md
        │   ├── SKL-STATUS-01_task-in-progress.md
        │   ├── SKL-STATUS-02_task-in-review.md
        │   ├── SKL-STATUS-03_task-completed-tl.md
        │   ├── SKL-STATUS-04_task-approved-pm.md
        │   ├── SKL-STATUS-05_task-on-hold.md
        │   ├── SKL-STATUS-06_task-rejected-pm.md
        │   ├── SKL-QUERY-01_mis-tareas.md
        │   ├── SKL-QUERY-02_tareas-en-revision.md
        │   ├── SKL-QUERY-03_detalle-tarea.md
        │   ├── SKL-QUERY-04_avance-fases.md
        │   ├── SKL-QUERY-05_estado-fase-asignable.md
        │   ├── SKL-COMMENT-01_comentario-generico.md
        │   ├── SKL-COMMENT-02_apr-pm.md
        │   ├── SKL-COMMENT-03_apr-tl.md
        │   ├── SKL-ISSUE-01_crear-issue.md
        │   ├── SKL-DEVLOG-01_decision.md
        │   └── SKL-DEVLOG-02_observacion.md
        ├── vtt-attach/
        │   ├── SKL-ATTACH-01_subir-archivo.md
        │   └── SKL-ATTACH-02_subir-devlog.md
        ├── git-ops/
        │   ├── SKL-GIT-01_crear-branch.md
        │   ├── SKL-GIT-02_rebase-main.md
        │   ├── SKL-GIT-03_commit-formato.md
        │   └── SKL-GIT-04_crear-pr.md
        ├── report/
        │   ├── SKL-REPORT-01_entrega-tarea.md
        │   └── SKL-REPORT-02_reporte-pjm.md
        ├── file-structure/
        │   └── SKL-STRUCTURE-01_ubicar-entregable.md
        └── vtt-track/
            ├── SKL-TRACK-01_linkear-trackable-item.md
            ├── SKL-TRACK-02_crear-acceptance-criterion.md
            ├── SKL-TRACK-03_fulfillment-criterion.md
            ├── SKL-TRACK-04_verificar-review-gate.md
            ├── SKL-TRACK-05_cerrar-trackable-item.md
            └── SKL-TRACK-06_dashboard-trackable-items.md
```

---

## 8. Próximos Pasos

1. ~~**Crear los archivos individuales**~~ ✅ Completado v1.1
2. **Registrar en BD del Prompt Builder** — cuando PB-01 esté listo, cargar skills como `agent_role_templates` o como referencias en `project_agents.template`
3. **Sync en Project_setup** — copiar carpeta `06.Skills/` a `Project_setup/00-platform/` como template reutilizable
4. **Tarea VTT** — crear tarea MS-XXX para que PJM cargue las skills en VTT como referencias de contexto

---

## Historial de Versiones

| Versión | Fecha | Cambio |
|---------|-------|--------|
| 1.0 | 2026-05-01 | Versión inicial — 22 skills en 8 categorías |
| 1.1 | 2026-05-11 | Consolidación por objeto: vtt-status, vtt-query, vtt-comment, vtt-issue, vtt-devlog → vtt-task/. 3 skills nuevas: TASK-01, TASK-02, TASK-03. Total: 25 skills en 6 categorías |
| 1.2 | 2026-05-12 | Nueva categoría VTT-TRACK (6 skills): TRACK-01..06 para Trackable Items, Acceptance Criteria y Fulfillment. Sustenta SOP-TRK-01. Total: 31 skills en 7 categorías |
