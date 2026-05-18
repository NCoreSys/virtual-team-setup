# 02 — OPERACIÓN DEL AGENTE

**Capa:** Estándar (genérico, portable)
**Audiencia:** Todos los agentes de ejecución (BE, FE, DB, DO, QA, UX)
**Versión:** 1.0
**Complementa:** `00_INDEX.md`, `01_ONBOARDING.md`, `03_FLUJO_TL.md`

---

## 1. PROPÓSITO

Define las reglas operativas comunes a todos los agentes que ejecutan tareas en la plataforma Virtual Teams. Cubre ciclo de vida de una tarea, gestión de issues, on-hold/resume, git flow, documentación obligatoria, comunicación con el PM y referencia de endpoints.

> **No contiene UUIDs, URLs, ni datos específicos del proyecto.** Esos viven en `PROJECT_MEMORY.md` y `OPERATIVO_[ROL].md` del proyecto.

---

## 2. ROLES Y ÁMBITOS DE RESPONSABILIDAD

| Rol | Responsabilidad | NO puede |
|-----|-----------------|----------|
| **PM (Coordinador)** | Administra tareas en UI, merge PRs, aprobar/rechazar, crear proyectos | — |
| **Tech Lead (TL)** | Generar briefs, assignments, code review, decisiones de arquitectura | Asignar tareas en UI, merge PRs, modificar schema de BD |
| **Backend Dev (BE)** | Servicios, controladores, validators, tipos TS del backend | Modificar schema de BD, hacer deploys |
| **Frontend Dev (FE)** | Componentes, hooks, tipos TS del frontend | Modificar backend directamente |
| **Database Engineer (DB)** | Schema, migraciones, documentación del esquema | — |
| **DevOps (DO)** | Docker, VM, deploys, migraciones en producción, rebuild containers | — |
| **QA Engineer** | Test plans, test execution, bug reports | Modificar código de producción |
| **Design Lead (DL)** | Coordinar diseño, QA visual, UX specs, aprobar diseños del UX | Generar HTML/mockups, programar |
| **UX Designer** | Generar HTMLs, mockups, flujos visuales | Programar, tomar decisiones de diseño sin DL |

### Regla fundamental

> Si un agente necesita un cambio **fuera de su ámbito**, debe crear un **issue** en la tarea correspondiente para que el agente responsable lo ejecute. NUNCA modificar archivos fuera de tu responsabilidad.

---

## 3. CICLO DE VIDA DE UNA TAREA

### Estados disponibles

```
task_created → task_pending → task_in_progress → task_in_review → task_completed → task_approved
                    ↓                                 ↑
                    └→ task_blocked / task_on_hold ──┘
                                      ↓
                                task_rejected → task_cancelled
```

| Estado | Significado | Quién lo cambia |
|--------|-------------|------------------|
| `task_created` | Recién creada, sin asignar | Sistema / PM |
| `task_pending` | Asignada, esperando inicio | Sistema (auto al asignar) |
| `task_in_progress` | Agente trabajando activamente | Agente ejecutor |
| `task_in_review` | PR creado, esperando review | Agente ejecutor |
| `task_completed` | Review aprobado, trabajo terminado | PM / Tech Lead |
| `task_approved` | Aprobación final (terminal) | **Solo PM** |
| `task_blocked` | Dependencia no resuelta | Sistema (auto) |
| `task_on_hold` | Pausada por issue bloqueante | PM / Tech Lead |
| `task_rejected` | Rechazada, requiere corrección | PM / Tech Lead |
| `task_cancelled` | Cancelada (terminal) | PM |

### Flujo típico

```
PM asigna tarea (pending)
  → Agente la toma (in_progress)
    → Agente crea branch, implementa, commitea
      → Agente pushea, crea PR (in_review)
        → TL/PM revisan
          → Si OK: completed → approved
          → Si NO: rejected → agente corrige → in_review de nuevo
```

### Regresiones (reason obligatorio)

Una transición es **regresión** cuando:
1. El estado destino tiene **orden menor** que el actual
2. El estado destino es `task_rejected` o `task_cancelled`

Si no se provee `reason` en una regresión, la API devuelve `400 REASON_REQUIRED`.

### Automatizaciones al completar tarea

Cuando una tarea cambia a `task_completed` o `task_approved`, el sistema ejecuta:

1. **Auto-unblock:** Marca dependencias como completadas, desbloquea tareas dependientes.
2. **Auto-resolve issues:** Resuelve issues vinculados vía `resolvedByTaskId`.
3. **Auto-resume:** Si todos los issues de una tarea en `on_hold` están resueltos, la reanuda al `previousStatus`.

---

## 4. GESTIÓN DE TAREAS VÍA API

### Consultar tarea

```
GET /api/tasks/{TASK_ID}
GET /api/tasks                             # listar todas
GET /api/tasks?status=task_in_progress     # filtrar por status
GET /api/tasks?assigneeId={UUID}           # filtrar por asignado
```

### Crear tarea (dentro de una fase)

```
POST /api/phases/{phaseId}/tasks
body: {
  "title": "string",
  "description": "string (max 2000 caracteres)",
  "statusId": "{UUID_PENDING}",
  "priorityId": "{UUID_PRIORIDAD}",
  "estimatedHours": 4,
  "assignedToId": "{UUID_AGENTE}",          ← campo correcto (no 'assignedTo')
  "assignedBy": "{UUID_PM_O_TL}",
  "category": "development | bugfix | review | design | testing",
  "complexity": "LOW | MEDIUM | HIGH",      ← MAYÚSCULAS
  "createdBy": "{UUID_PM_O_TL}",
  "sourceIssueId": "{UUID_ISSUE}"            ← opcional, vincula issue resolutora
}
```

**Errores frecuentes al crear tareas:**
- ❌ `assignedTo` se ignora silenciosamente. Usar `assignedToId`.
- ❌ `priority_id`, `status_id` (snake_case) rechazados. Usar camelCase.
- ❌ `complexity: "medium"` rechazado. Valores válidos: `"LOW"`, `"MEDIUM"`, `"HIGH"`.
- ❌ `description > 2000 chars` → 400 `too_big`.

### Actualizar tarea

```
PATCH /api/tasks/{TASK_ID}                 # actualización parcial
body: { "title": "...", "description": "...", "estimatedHours": 6 }

PUT /api/tasks/{TASK_ID}                   # actualización completa
body: { ... todos los campos ... }
```

### Cambiar status

```
PATCH /api/tasks/{TASK_ID}/status
body: {
  "statusId": "{UUID_NUEVO_STATUS}",
  "changedBy": "{UUID_USUARIO}",
  "reason": "Motivo (obligatorio en regresiones)"
}
```

---

## 5. GESTIÓN DE ISSUES VÍA API

### Crear issue en una tarea

```
POST /api/tasks/{TASK_ID}/issues
body: {
  "title": "Título descriptivo del issue",
  "description": "Contexto, causa y solución propuesta",
  "type": "bug | improvement | requirement | other",
  "severity": "low | medium | high | critical"
}
```

### Consultar issues

```
GET /api/tasks/{TASK_ID}/issues            # issues de una tarea
GET /api/issues/{ISSUE_ID}                 # issue específico
```

### Actualizar issue

```
PUT /api/issues/{ISSUE_ID}
body: {
  "isResolved": true,
  "resolvedByTaskId": "{TASK_ID_RESOLUTORA}"
}
```

**Campos actualizables:** `title`, `description`, `type`, `severity`, `isResolved`, `resolvedByTaskId`.

### Vincular issue con tarea resolutora

Al crear una tarea **desde un issue** (para resolverlo), incluir `sourceIssueId`:

```
POST /api/phases/{PHASE_ID}/tasks
body: {
  "title": "[Bug] Título del issue origen",
  "description": "Tarea creada para resolver issue...",
  "statusId": "{UUID_PENDING}",
  "priorityId": "{UUID_PRIORIDAD}",
  "sourceIssueId": "{UUID_ISSUE_ORIGEN}"
}
```

Cuando la tarea resolutora se complete, el issue origen se auto-resuelve.

---

## 6. ON-HOLD Y RESUME

### 🚨 REGLA CRÍTICA

```
NUNCA usar PATCH /api/tasks/{id}/status para poner una tarea en on_hold.

Si usas PATCH /status con task_on_hold:
  - El campo previousStatus queda NULL
  - El endpoint resume falla: "Task has no previous status to restore"
  - La tarea queda ATRAPADA — ningún endpoint la puede desbloquear
  - Requiere fix manual directo en BD para recuperarla
```

### Quién puede poner una tarea en on_hold

**Solo el Tech Lead o PM** deben poner tareas en on_hold.

Los agentes ejecutores (BE, FE, QA, etc.) **NO deben mover la tarea a on_hold por su cuenta**. Proceso correcto cuando un agente encuentra un bloqueador:

1. Postear comentario explicando el bloqueador
2. Crear issue en la tarea (`POST /api/tasks/{id}/issues`)
3. Notificar al Tech Lead o PM
4. **Esperar** — el TL decide si pone la tarea en on_hold

### Poner tarea en espera (solo TL/PM)

```
PUT /api/tasks/{TASK_ID}/on-hold
headers:
  Content-Type: application/json
  x-user-id: {UUID_USUARIO}
body: {
  "type": "blocker | bug | clarification | dependency",
  "title": "Título del bloqueador",
  "description": "Descripción del problema"
}
```

La tarea guarda su `previousStatus` para restaurarlo al reanudar.

### Reanudar tarea

```
PUT /api/tasks/{TASK_ID}/resume
headers:
  Content-Type: application/json
  x-user-id: {UUID_USUARIO}
body: {
  "issueAction": "resolved | open | closed",
  "comment": "Issues resueltos, tarea puede continuar"
}
```

Solo PM y Tech Lead pueden reanudar tareas.

### Cadena de automatización

```
Tarea completada/aprobada
  ├→ 1. Auto-unblock: desbloquea tareas dependientes
  ├→ 2. Auto-resolve: resuelve issues con resolvedByTaskId = esta tarea
  └→ 3. Auto-resume: si la tarea parent (on_hold) tiene TODOS sus issues resueltos
         → restaura previousStatus
```

---

## 7. COMENTARIOS Y ACTIVIDAD

### Crear comentario

```
POST /api/tasks/{TASK_ID}/comments
body: {
  "message": "Texto del comentario",        ← el campo es 'message' (no 'content')
  "userId": "{UUID_USUARIO}"
}
```

### Consultar

```
GET /api/tasks/{TASK_ID}/comments          # comentarios de una tarea
GET /api/tasks/{TASK_ID}/activity          # feed unificado (comentarios + status + attachments)
GET /api/tasks/{TASK_ID}/history           # historial de cambios de status
```

---

## 8. ATTACHMENTS (BRIEF, ASSIGNMENT, DEVLOG, CODE LOGIC)

### Subir attachment (multipart/form-data)

```
POST /api/tasks/{TASK_ID}/attachments
fields:
  file: (binary)
  fileType: "brief | assignment | devlog | code_logic | spec | other"
  uploadedById: "{UUID_USUARIO}"
```

### Consultar

```
GET /api/tasks/{TASK_ID}/attachments       # listar
GET /api/attachments/{ID}                  # detalle
GET /api/attachments/{ID}/download         # URL de descarga
DELETE /api/attachments/{ID}               # eliminar
```

### Regla de nomenclatura

| fileType | Cuándo | Quien sube |
|----------|--------|------------|
| `brief` | Al crear la tarea | TL (o DL para tareas UX) |
| `assignment` | Al asignar la tarea | TL (o DL para tareas UX) |
| `devlog` | Antes de mover a in_review | Agente ejecutor |
| `code_logic` | Antes de mover a in_review | Agente ejecutor (1 por archivo modificado) |
| `spec` | Handoff DL → FE | DL |

**IMPORTANTE:** Sin los 3 entregables (DevLog + Code Logic + Comentario), el sistema puede bloquear la transición a `in_review`.

---

## 9. GIT FLOW ESTÁNDAR

### Estructura de branches

```
main (protegida: PR + 1 approval)
  ← feature/{TASK_ID}-nombre-descriptivo
```

> Algunos proyectos usan `develop` intermedio. Consultar `PROJECT_MEMORY.md` del proyecto.

### Procedimiento del agente

```bash
# 1. Partir desde main (o develop) actualizado
git checkout main && git pull origin main

# 2. Crear feature branch
git checkout -b feature/{TASK_ID}-nombre-descriptivo

# 3. Implementar y commitear
git add archivos_especificos    # NUNCA usar git add -A o git add .
git commit -m "feat(scope): descripción del cambio

Co-Authored-By: Claude <noreply@anthropic.com>
Refs: #{TASK_ID}"

# 4. Push
git push -u origin feature/{TASK_ID}-nombre-descriptivo

# 5. Crear PR via gh CLI
gh pr create --title "feat(scope): {TASK_ID} descripción" --body "## Summary
- Cambio 1
- Cambio 2

## Test plan
- [ ] Verificar X
- [ ] Verificar Y"
```

### Reglas críticas de Git

| Regla | Detalle |
|-------|---------|
| **PM hace los merges** | NUNCA un agente o Tech Lead hace merge |
| **Trabajar desde main actualizado** | `git pull` antes de crear branch |
| **Verificar antes de entregar** | La rama debe tener TODOS los fixes necesarios |
| **No force push** | NUNCA `--force`, `--no-verify`, `reset --hard` sin autorización |
| **Archivos específicos** | NUNCA `git add .` o `git add -A` (riesgo de incluir .env, credentials) |
| **No usar -i flag** | NUNCA `git rebase -i` o `git add -i` (requieren input interactivo) |
| **Tiempo máximo en branch: 24h** | Si la tarea toma más, rebase diario con main |
| **Rebase antes de PR** | `git fetch origin && git rebase origin/main && git push --force-with-lease` |
| **PR inmediato tras completar** | No dejar commits locales sin pushear |
| **Merge rápido (max 2h post-approval)** | No dejar PRs aprobados sin merge |

### Formato de commits

```
[tipo]([repo]) [TASK_ID]: Descripción breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude <noreply@anthropic.com>
Refs: #{TASK_ID}
```

**Tipos:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

---

## 10. REGLAS OPERATIVAS CRÍTICAS

### 🚨 10.1 Code Review — leer comentarios antes de completar

**ANTES de mover cualquier tarea a `task_completed`:**

1. Leer TODOS los comentarios de la tarea: `GET /api/tasks/{id}/comments`
2. Si un comentario menciona un BUG, issue o pendiente → verificar su estado
3. Si hay un issue abierto en OTRA tarea relacionado → también bloquea el cierre
4. **NUNCA mover a `completed` una tarea con condiciones FAIL** — dejar en `in_review` con comentario explicando qué falla
5. El review no es solo verificar que existen archivos — verificar CADA condición obligatoria del handoff
6. **Tareas de code review** (rol revisor): NO completar si hay tareas revisadas con NEEDS_FIXES. El review termina SOLO cuando TODAS las tareas revisadas están en PASS.

### 🚨 10.2 Una tarea no se completa con issues abiertos

- Verificar SIEMPRE: `GET /api/tasks/{taskId}/issues` → si hay `isResolved: false` → NO mover a completed.
- Flujo correcto: issues abiertos → tarea permanece en `task_in_review` hasta que TODOS estén resueltos.
- NO importa si el trabajo del agente es bueno — si hay issues abiertos, la tarea no termina.

### 🚨 10.3 Aprobación — solo el PM aprueba

- **Roles técnicos (TL, DL, PJM)** mueven a `task_completed` tras revisión.
- **PM es el ÚNICO que aprueba** (`task_approved`) — JAMÁS otro rol.
- Mover a `task_approved` sin ser PM = acción irreversible y grave.

### 🚨 10.4 Cambio de status — solo tus propias tareas

- Cada agente SOLO puede cambiar status de tareas asignadas a sí mismo.
- **NUNCA mover a `in_progress` una tarea asignada a otro agente** — rompe las métricas.
- Cuando se asigna una tarea a otro rol → ese rol cambia el status por sí mismo.
- Excepción: roles revisores (TL/DL/PJM) pueden mover `in_review → completed` tras aprobar el review.

### 🚨 10.5 No mockear datos

Si detectas que faltan datos reales (catálogos vacíos, seed data, configuraciones):

1. **NUNCA** crear/mockear datos.
2. **CREAR un ISSUE** con template estándar.
3. **COMPLETAR** todo lo posible de la tarea.
4. **CAMBIAR status** a `task_on_hold` (usar endpoint `PUT /on-hold`, NO `PATCH /status`).
5. **ESPERAR** resolución del ISSUE.
6. **REGRESAR** a completar cuando haya datos reales.

### 🚨 10.6 Migraciones de BD

Cuando se requiere una migración (ALTER TABLE, CREATE TABLE, etc.):

1. Crear el archivo SQL de migración localmente (referencia).
2. Crear un **BUG para DevOps** con los comandos SQL exactos a ejecutar.
3. El **DevOps** aplica la migración en producción — el BE NUNCA lo hace directamente.
4. Endpoint: `POST /api/tasks/{taskId}/bugs`.

### 🚨 10.7 VM — nunca tocar directamente

- **NUNCA** ejecutar comandos directos en la VM (`ssh docker exec`, `docker restart`, edición de `.env`, `docker-compose`).
- **Si hay problema en la VM** → SOLO reportar al PM y esperar al Admin.
- Los agentes (TL, DL, etc.) NO tienen autorización para operar la VM.
- Crear un BUG dentro de una tarea existente del DevOps con los comandos exactos.

### 🚨 10.8 Deliveries — obligatorio en setup de fase

Al crear tareas en una fase, SIEMPRE crear Deliveries para agruparlas:

1. `POST /api/deliveries` con `{ phaseId, name, order, createdBy, statusId }`.
2. `POST /api/deliveries/{id}/tasks/{taskId}` con `{ assignedBy }` por cada tarea.
- **Agrupación:** 1 Delivery por sprint/grupo (PRE, S01, S02, BUGS, etc.).
- **RN-010:** tarea y Delivery deben tener la misma `phaseId`.

### 🚨 10.9 DevOps — solo description

Tareas asignadas a DevOps **NO requieren BRIEF ni ASSIGNMENT** — la description de la tarea es suficiente handoff si detalla: objetivo, SQL/comandos, pre/post checks, rollback.

### 🚨 10.10 Nunca commit directo a main

Proceso correcto (sin excepciones):

1. `git checkout -b feature/[TASK_ID]`
2. Commits en el branch
3. `git push origin feature/[TASK_ID]`
4. `gh pr create` con título descriptivo
5. Esperar approval del Coordinador
6. Coordinador hace merge

### 🚨 10.11 Branch management — rebase frecuente

- Crear branch al inicio de tarea.
- **Tiempo máximo en branch: 24 horas** — si la tarea toma más, rebase diario con main.
- Rebase frecuente con main **ANTES de crear PR**.
- Crear PR INMEDIATAMENTE después de completar.
- **ANTES de merge:** validar que NO se perdió código (revisar "Files Changed" en GitHub).

---

## 11. REGLAS DE COMUNICACIÓN CON EL PM

- **Pregunta del PM → SOLO RESPONDER.** No lanzar agentes, no ejecutar acciones.
- **Acciones solo cuando el PM dice explícitamente:** "hazlo", "crea", "genera", "ejecuta", "sí", "aplica".
- Si el PM dice "espera" o "no hagas nada" → **NO HACER NADA**.
- NUNCA tocar código sin autorización del PM (ni bugs "fáciles" ni refactors obvios).
- NUNCA crear tareas de "decisión" sin autorización del PM.
- Si detectas algo fuera de tu alcance → **reportar**, no actuar.

### Formato de reporte al PM tras completar tarea

```markdown
## Entrega: [TASK_ID] - [Nombre de la tarea]

### Código
- `src/...` - [descripción]

### Development Log
`knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[nombre].md`

### Code Logic
- `knowledge/code-logic/.../[archivo].LOGIC.md`

### Commit
[tipo]([repo]) [TASK_ID]: Descripción
SHA: [hash del commit]

### Cómo probar
[comandos o pasos para validar]
```

---

## 12. PROCESOS OPERATIVOS

### 12.1 Proceso de cierre de tarea (agente ejecutor)

Checklist obligatorio antes de mover a `task_completed`:

- [ ] Código funciona localmente
- [ ] Archivos `.LOGIC.md` creados/actualizados (1 por archivo de código)
- [ ] Swagger docs agregados (si hay endpoints)
- [ ] Development Log completo en `knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[nombre].md`
- [ ] Commit con formato correcto + `Co-Authored-By`
- [ ] Push a branch `feature/[TASK_ID]`
- [ ] PR creado con `gh pr create`
- [ ] Comentarios de la tarea revisados (leer TODOS)
- [ ] Issues de la tarea resueltos (`isResolved: true`)
- [ ] DevLog, Code Logic y Comentario subidos como attachments
- [ ] Status cambiado a `task_in_review`

### 12.2 Proceso On-Hold / Resume

```
# BLOQUEAR tarea (on-hold)
PUT /api/tasks/{taskId}/on-hold
Header: x-user-id: {userId}
Body: { "type": "blocker|bug|clarification|dependency", "title": "...", "description": "..." }

# LIBERAR tarea (resume)
PUT /api/tasks/{taskId}/resume
Header: x-user-id: {userId}
Body: { "issueAction": "resolved|open|closed", "comment": "..." }
```

**NUNCA usar `PATCH /status` para poner on_hold** — rompe `previousStatus` y bloquea el resume.

### 12.3 Proceso de issues / fixes

- Crear tarea de fix con `sourceIssueId` apuntando al issue origen.
- NO resolver directamente con `PUT /api/issues`.
- Issues → Tarea de fix → PR → Merge → Issue resuelto automáticamente.

---

## 13. DOCUMENTACIÓN OBLIGATORIA

### Al completar cada tarea

| Documento | Cuándo | Dónde |
|-----------|--------|-------|
| **Code Logic** (`.LOGIC.md`) | Por cada archivo creado o modificado significativamente | `knowledge/code-logic/{ruta_relativa}/` |
| **Development Log** | Al finalizar la tarea | `knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[nombre].md` |
| **BRIEF actualizado** (si el scope cambió) | Si hubo cambios durante implementación | `knowledge/agent-tasks/briefs/` |

### Estructura de archivos LOGIC

```
knowledge/code-logic/
  backend/
    src/services/       -> *.LOGIC.md por cada service
    src/controllers/    -> *.LOGIC.md por cada controller
    src/validators/     -> *.LOGIC.md por cada validator
    prisma/             -> schema.LOGIC.md
  frontend/
    src/components/     -> ComponentName.LOGIC.md
    src/hooks/          -> useHookName.LOGIC.md
    src/types/          -> typeName.LOGIC.md
```

### Contenido mínimo de un LOGIC

1. Propósito del archivo.
2. Funciones/componentes exportados con descripción breve.
3. Flujo de datos principal.
4. Historial de cambios (fecha, tarea, autor).
5. Bugs conocidos y mejoras futuras (si aplica).

---

## 14. REFERENCIA COMPLETA DE ENDPOINTS

> Esta sección lista los endpoints comunes. Los paths específicos y extensiones del proyecto (Modelo Dinámico V4, Deliveries, etc.) viven en `OPERATIVO_[ROL].md` del proyecto.

### Catálogos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/catalogs/status?process={p}` | Catálogo de status (process: project/phase/task/import) |
| GET | `/api/catalogs/priorities` | Prioridades |
| GET | `/api/catalogs/entity-types` | Tipos de entidad |
| GET | `/api/catalogs/document-types` | Tipos de documento |
| GET | `/api/catalogs/file-types` | Tipos de archivo |

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/users` | Listar usuarios |
| GET | `/api/users/{id}` | Obtener usuario |
| POST | `/api/users` | Crear usuario |
| PATCH | `/api/users/{id}` | Actualizar usuario |
| DELETE | `/api/users/{id}` | Desactivar (soft delete) |
| GET | `/api/users/{id}/workload` | Workload |

### Proyectos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/projects` | Listar |
| GET | `/api/projects/{id}` | Obtener con fases |
| POST | `/api/projects` | Crear (soporta wizard) |
| PUT | `/api/projects/{id}` | Actualizar |
| DELETE | `/api/projects/{id}` | Eliminar (cascade) |

### Fases

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/projects/{projectId}/phases` | Listar fases |
| POST | `/api/projects/{projectId}/phases` | Crear fase |
| GET | `/api/phases/{id}` | Obtener con tareas |
| PUT | `/api/phases/{id}` | Actualizar |
| DELETE | `/api/phases/{id}` | Eliminar |
| PATCH | `/api/phases/{id}/reorder` | Reordenar |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks` | Listar (con filtros) |
| GET | `/api/tasks/{id}` | Obtener |
| POST | `/api/phases/{phaseId}/tasks` | Crear en fase |
| GET | `/api/phases/{phaseId}/tasks` | Listar de fase |
| PUT | `/api/tasks/{id}` | Actualizar (full) |
| PATCH | `/api/tasks/{id}` | Actualizar (parcial) |
| DELETE | `/api/tasks/{id}` | Eliminar |
| PATCH | `/api/tasks/{id}/status` | Cambiar status (con audit) |
| PUT | `/api/tasks/{id}/on-hold` | Poner en espera (header `x-user-id`) |
| PUT | `/api/tasks/{id}/resume` | Reanudar (header `x-user-id`) |

### Dependencias

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/tasks/{id}/dependencies` | Agregar dependencia |
| GET | `/api/tasks/{id}/dependencies` | Listar dependencias |
| DELETE | `/api/tasks/{id}/dependencies/{depId}` | Eliminar |
| GET | `/api/tasks/{id}/dependencies/status` | Estado de dependencias |
| GET | `/api/phases/{id}/dependencies` | Dependencias de fase |
| POST | `/api/phases/{id}/dependencies` | Agregar (valida ciclos) |
| DELETE | `/api/phases/{id}/dependencies/{depId}` | Eliminar |

### Issues

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/tasks/{taskId}/issues` | Crear issue |
| GET | `/api/tasks/{taskId}/issues` | Listar issues de tarea |
| GET | `/api/issues/{id}` | Obtener |
| PUT | `/api/issues/{id}` | Actualizar (resolver, vincular) |
| DELETE | `/api/issues/{id}` | Eliminar |

### Comentarios e Historial

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/tasks/{id}/comments` | Crear (body: `{message, userId}`) |
| GET | `/api/tasks/{id}/comments` | Listar comentarios |
| GET | `/api/tasks/{id}/activity` | Feed unificado |
| GET | `/api/tasks/{taskId}/history` | Historial de status |

### Attachments

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks/{taskId}/attachments` | Listar |
| POST | `/api/tasks/{taskId}/attachments` | Subir (multipart/form-data) |
| GET | `/api/attachments/{id}` | Detalle |
| GET | `/api/attachments/{id}/download` | URL de descarga |
| DELETE | `/api/attachments/{id}` | Eliminar |

### Deliveries (MGP)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/deliveries` | Crear delivery |
| GET | `/api/deliveries/{id}` | Obtener delivery con tareas |
| PUT | `/api/deliveries/{id}` | Actualizar delivery |
| DELETE | `/api/deliveries/{id}` | Eliminar (tareas quedan libres) |
| POST | `/api/deliveries/{deliveryId}/tasks/{taskId}` | Asignar tarea a delivery |
| DELETE | `/api/deliveries/{deliveryId}/tasks/{taskId}` | Desasignar tarea |

### Auth (si el proyecto usa JWT)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/service-token` | Token de servicio (body: `{userId, serviceKey}`) |

### Health

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check (DB, Redis, MinIO) |

---

## 15. HEADERS Y CÓDIGOS DE ERROR COMUNES

### Headers

| Header | Cuándo | Valor |
|--------|--------|-------|
| `Content-Type` | En POST, PUT, PATCH | `application/json` |
| `x-user-id` | En on-hold y resume | UUID del usuario |
| `Authorization` | En rutas de mutación (si el proyecto usa JWT) | `Bearer {JWT}` |

### Códigos de error comunes

| Código | Significado |
|--------|-------------|
| `REASON_REQUIRED` | Falta `reason` en regresión de status |
| `STATUS_NOT_FOUND` | UUID de status inválido |
| `UNAUTHORIZED` | Falta `x-user-id` header o JWT |
| `NOT_FOUND` | Recurso no existe |
| `CIRCULAR_DEPENDENCY` | Dependencia circular detectada |
| `INVALID_TRANSITION` | Transición de status no permitida |
| `VALIDATION_ERROR` | Zod rechazó payload (ver `details[]`) |
| `PHASE_ORDER_CONFLICT` (409) | Order duplicado en fase |
| `PHASE_HAS_ACTIVE_TASKS` (409) | DELETE phase con tareas asignadas |
| `DELIVERABLE_HAS_DOCUMENTS` (409) | DELETE deliverable con docs |
| `DELIVERABLE_HAS_TASKS` (409) | DELETE deliverable con tareas |

---

## 16. INICIALIZACIÓN DE PROYECTO NUEVO

Checklist para el TL al iniciar un proyecto:

```
[ ] 1. Verificar que el proyecto existe en el sistema
       GET {BASE_URL}/api/projects

[ ] 2. Obtener y documentar los UUIDs del proyecto
       GET {BASE_URL}/api/catalogs/status?process=task
       GET {BASE_URL}/api/catalogs/priorities
       GET {BASE_URL}/api/users

[ ] 3. Rellenar PROJECT_MEMORY.md con datos del proyecto
       - URLs, UUIDs, agentes concretos
       - Stack técnico
       - Fase actual

[ ] 4. Crear estructura de carpetas según 04_ESTRUCTURA_FASES.md
       - phases/00-discovery, 01-planning, ...
       - _pm/, docs/, archive/

[ ] 5. Configurar Git flow
       - Verificar branches protegidas
       - Configurar reglas de PR

[ ] 6. Generar primer BRIEF y ASSIGNMENT
       - Usar templates estándar
       - Incluir contexto del proyecto
```

---

## 17. DOCUMENTOS RELACIONADOS

| Documento | Propósito |
|-----------|-----------|
| `00_INDEX.md` | Jerarquía y precedencia de documentos |
| `01_ONBOARDING.md` | Taxonomía del sistema |
| `03_FLUJO_TL.md` | Flujo específico del Tech Lead |
| `04_ESTRUCTURA_FASES.md` | Layout de carpetas por fase |
| `05_CATALOGO_DELIVERABLES.md` | 438 deliverables por fase |
| `roles/AGENT_PROFILE_BASE_[ROL].md` | Perfil base del rol |
| `OPERATIVO_[PROYECTO]_[ROL].md` | Instancia específica del proyecto |
| `PROJECT_MEMORY.md` | Memoria del proyecto (datos específicos) |

---

## 18. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-20 | Versión inicial consolidada desde `PROCEDIMIENTOS_OPERATIVOS_STANDARD.md` v1.1 + `PROCEDIMIENTOS_OPERATIVOS_AGENTES.md` v1.1 (parte genérica). Extracción de la capa portable. |

---

**Fuente de verdad de este documento:** `Project_setup/standard/02_OPERACION_AGENTE.md`
