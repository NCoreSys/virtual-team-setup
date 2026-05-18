# REFERENCE — Setup de Fase: Phases, Releases, Sprints, Deliveries, Tareas y Dependencias

**Audiencia:** Tech Lead (cualquier proyecto que use el backend VTT)
**Fecha:** 2026-05-12
**Versión:** 1.0
**Backend base:** `http://77.42.88.106:3000`

> Este documento es la fuente única de verdad para el setup de fase en VTT.
> Lee y aplica los pasos en orden. NO inventes endpoints — todos los listados aquí están verificados contra el código real en `backend/src/routes/`.

---

## 1. Modelo Conceptual

```
Project
  └── Phase  (puede tener subfases vía parentId)
        └── Delivery  (entregable que agrupa tareas DENTRO de una fase)
              └── Task (1 task = 1 Delivery a la vez — RN-004)

Project
  └── Release
        └── Sprint
              └── Delivery (vía Delivery.sprintId — relación 1 Delivery → 1 Sprint)
```

**Reglas clave:**

| Regla | Significado |
|-------|-------------|
| **RN-010** | Tarea y Delivery deben estar en la MISMA fase |
| **RN-004** | Una tarea NO puede estar en dos Deliveries simultáneamente |
| **Delivery → 1 Sprint** | Un Delivery solo puede vincularse a UN sprint. Si un módulo cruza varios sprints, crear varios Deliveries (uno por sprint) |
| **Sprint no tiene tasks directas** | Las tareas heredan el sprint a través del Delivery |

---

## 2. Orden Correcto del Setup (PASOS EXACTOS)

### Paso 1 — Crear Phases (Fases del proyecto)

```bash
POST /api/projects/:projectId/phases
Content-Type: application/json
Authorization: Bearer <TOKEN>

{
  "name": "Project Setup",
  "order": 1,
  "type": "analysis"   // analysis | design | development | testing | deployment
}
```

**Sub-fases** (jerarquía):

```bash
POST /api/projects/:projectId/phases
{
  "name": "A. VTT Setup",
  "order": 1,
  "type": "analysis",
  "parentId": "<UUID_FASE_PADRE>"
}
```

> Guarda el `id` retornado de cada fase — lo necesitas para los pasos 5 y 6.

---

### Paso 2 — Crear Release

```bash
POST /api/projects/:projectId/releases
{
  "name": "V1.0",
  "description": "Release inicial",
  "startDate": "2026-05-01T00:00:00Z",
  "endDate":   "2026-06-30T00:00:00Z",
  "createdBy": "<UUID_TL>"
}
```

---

### Paso 3 — Crear Sprints dentro del Release

```bash
POST /api/releases/:releaseId/sprints
{
  "number": 1,                  // OBLIGATORIO — número entero
  "name": "S01 — Foundation",
  "goal": "Setup técnico base",
  "startDate": "2026-05-01T00:00:00Z",
  "endDate":   "2026-05-15T00:00:00Z"
}
```

> Repetir 1 vez por cada sprint. Guardar los `id` retornados.

---

### Paso 4 — Crear Tareas en las Phases

```bash
POST /api/phases/:phaseId/tasks
{
  "title": "SETUP Fase 4 - Development",
  "description": "...",
  "priorityId": "<UUID_PRIORIDAD>",
  "statusId":   "335fd9c6-f0d6-4966-a6ea-f518c78bc422",  // task_pending
  "estimatedHours": 4,
  "assigneeId": "<UUID_AGENTE>"  // opcional al crear
}
```

> ⚠️ **El Task NO acepta `sprintId` directamente.** La asignación al sprint se hace en el Paso 6 vía el Delivery.

---

### Paso 5 — Crear Deliveries (UNO POR SPRINT POR MÓDULO)

```bash
POST /api/deliveries
{
  "phaseId":   "<UUID_FASE>",      // OBLIGATORIO — misma fase de las tareas
  "name":      "C1. Backend Core — S2",
  "order":     1,
  "createdBy": "<UUID_TL>",
  "description": "Backend Core para Sprint 2"
}
```

**REGLA DE NOMENCLATURA cuando un módulo cruza varios sprints:**

| ❌ MAL (1 Delivery para módulo completo) | ✅ BIEN (1 Delivery por sprint) |
|------------------------------------------|----------------------------------|
| `C. Backend Core` (vinculado solo a S2) | `C1. Backend Core — S2` (vinculado a S2) |
|                                          | `C2. Backend Core — S3` (vinculado a S3) |
|                                          | `C3. Backend Core — S4` (vinculado a S4) |

**Por qué:** Como `Delivery → 1 Sprint`, agrupar todo en uno hace que S3 y S4 no vean esas tareas en su métrica de progreso/velocity/firmas.

---

### Paso 6 — Vincular Delivery a Sprint (esto es donde se "asigna" el sprint)

```bash
PATCH /api/deliveries/:deliveryId
{
  "sprintId": "<UUID_SPRINT>"
}
```

> Cuando el Delivery está vinculado a un Sprint, **todas sus tareas quedan en ese sprint** automáticamente (la relación es Task → Delivery → Sprint).

---

### Paso 7 — Asignar Tarea al Delivery

```bash
POST /api/deliveries/:deliveryId/tasks/:taskId
{
  "assignedBy": "<UUID_TL>"
}
```

**Validaciones del backend:**
- RN-010: tarea y delivery deben estar en la misma fase → error si no
- RN-004: tarea no puede estar ya en otro delivery → error si no

---

### Paso 8 — Configurar Dependencias entre Tareas

```bash
POST /api/tasks/:taskId/dependencies
{
  "dependsOnTaskId": "<UUID_O_KEY_DE_TAREA_BLOQUEANTE>"
}
```

**Reglas:**
- `:taskId` = la tarea que va a ESPERAR
- `dependsOnTaskId` = la tarea que la BLOQUEA
- Acepta UUID o key (`VTT-XXX` / `MS-XXX`)
- El sistema marca `isBlocked: true` automáticamente si la bloqueante no está completada

**Consultar / Eliminar:**

```bash
GET    /api/tasks/:taskId/dependencies
GET    /api/tasks/:taskId/dependencies/status
DELETE /api/tasks/:taskId/dependencies/:depId
```

---

## 3. Errores Frecuentes — NO LOS COMETAS

### ❌ Error 1: Intentar asignar `sprintId` vía PATCH del task

```bash
# ❌ MAL — esto NO persiste sprintId
PATCH /api/tasks/MS-164 { "sprintId": "..." }
```

```bash
# ✅ BIEN — asignar sprint al Delivery
PATCH /api/deliveries/<deliveryId> { "sprintId": "..." }
```

**Razón:** El validador de update de task NO incluye `sprintId` en su schema Zod. El campo `sprintId` vive en el modelo `Delivery`, no en `Task`. El backend responde 200 OK pero ignora el campo silenciosamente.

---

### ❌ Error 2: Un solo Delivery para módulo que cruza varios sprints

Si Backend Core tiene tareas en S2, S3 y S4 y creas UN solo Delivery `C. Backend Core` vinculado a S2, las tareas de S3 y S4 **no aparecen en sus sprints** porque el Delivery solo apunta a S2.

**Solución:** crear `C1`, `C2`, `C3` — uno por sprint.

---

### ❌ Error 3: Crear tarea sin Delivery

Tareas sin Delivery aparecen "huérfanas" — no cuentan en métricas de sprint ni se pueden firmar/aprobar en cierre de sprint.

**Solución:** después de `POST /api/phases/:id/tasks`, siempre hacer `POST /api/deliveries/:deliveryId/tasks/:taskId`.

---

### ❌ Error 4: Asignar tarea a Delivery de OTRA fase

```
Tarea está en Fase "Development"
Delivery está en Fase "Testing"
→ POST /api/deliveries/:id/tasks/:taskId → ERROR RN-010
```

**Solución:** verificar antes de asignar:

```bash
curl -s "http://77.42.88.106:3000/api/tasks/MS-164" | jq '.data.phase.id'
curl -s "http://77.42.88.106:3000/api/deliveries/<id>" | jq '.data.phaseId'
# Deben ser iguales
```

---

### ❌ Error 5: Tarea de SETUP/INICIO mal estructurada

La tarea `SETUP-FASE-X` o `SETUP-BLOQUE-X` es el **gate de inicio**. Debe:

1. **Existir en la fase correcta** (la fase del bloque que arranca)
2. **Estar en su propio Delivery** (`Setup` o `Governance`)
3. **No tener dependencias** (es la primera — nada la bloquea)
4. **Ser dependencia de la PRIMERA tarea de cada sprint** del bloque
5. **Tener status `task_pending` o `task_in_progress` al inicio**

```bash
# Crear SETUP
POST /api/phases/:setupPhaseId/tasks {
  "title": "SETUP Fase X",
  "statusId": "335fd9c6-...",   // task_pending
  ...
}

# Crear dependencia: primera tarea de cada sprint depende del SETUP
POST /api/tasks/<primeraTareaSprint1>/dependencies {
  "dependsOnTaskId": "<SETUP_TASK_ID>"
}
POST /api/tasks/<primeraTareaSprint2>/dependencies {
  "dependsOnTaskId": "<SETUP_TASK_ID>"
}
```

---

## 4. Checklist de Setup Correcto

```
[ ] Project existe (POST /api/projects si no)
[ ] Phases creadas con jerarquía correcta (parentId si aplica)
[ ] Release creado
[ ] Sprints creados dentro del Release
[ ] Tareas creadas en las Phases correspondientes
[ ] Deliveries creados — UNO POR SPRINT POR MÓDULO
[ ] Cada Delivery vinculado a su Sprint vía PATCH /api/deliveries/:id { sprintId }
[ ] Cada tarea asignada a un Delivery vía POST /api/deliveries/:id/tasks/:taskId
[ ] Tarea SETUP-X creada SIN dependencias
[ ] Primera tarea de cada sprint tiene dependencia del SETUP
[ ] Dependencias entre tareas configuradas según handoff
[ ] Verificar visualmente: GET /api/sprints/:id devuelve tasks via deliveries
```

---

## 5. Endpoints — Tabla de Referencia Rápida

| Operación | Método | Endpoint |
|-----------|--------|----------|
| Crear fase | POST | `/api/projects/:projectId/phases` |
| Crear release | POST | `/api/projects/:projectId/releases` |
| Crear sprint | POST | `/api/releases/:releaseId/sprints` |
| Crear tarea | POST | `/api/phases/:phaseId/tasks` |
| Crear delivery | POST | `/api/deliveries` |
| **Vincular delivery a sprint** | **PATCH** | **`/api/deliveries/:deliveryId`** body `{ sprintId }` |
| Asignar tarea a delivery | POST | `/api/deliveries/:deliveryId/tasks/:taskId` |
| Desasignar tarea de delivery | DELETE | `/api/deliveries/:deliveryId/tasks/:taskId` |
| Crear dependencia | POST | `/api/tasks/:taskId/dependencies` body `{ dependsOnTaskId }` |
| Ver dependencias | GET | `/api/tasks/:taskId/dependencies` |
| Ver tareas de un sprint | GET | `/api/sprints/:sprintId` |

---

## 6. Cómo Verificar que el Setup Quedó Bien

```bash
# 1. Ver tareas de un sprint
curl -s "http://77.42.88.106:3000/api/sprints/<SPRINT_ID>" -H "Authorization: Bearer $TOKEN"
# Debe devolver tasks[] con todas las tareas que pertenecen a Deliveries vinculados al sprint

# 2. Ver deliveries de una fase
curl -s "http://77.42.88.106:3000/api/phases/<PHASE_ID>/deliveries" -H "Authorization: Bearer $TOKEN"

# 3. Ver dependencias de una tarea
curl -s "http://77.42.88.106:3000/api/tasks/<TASK_ID>/dependencies/status" -H "Authorization: Bearer $TOKEN"

# 4. Confirmar que SETUP es la única sin dependencias
# Y que la primera tarea de cada sprint depende del SETUP
```

---

## 7. UUIDs Estándar (Status)

| Status | UUID |
|--------|------|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |
| delivery_planned | `2f115b5b-2664-42b4-ba96-88c3b62863a2` |

---

## 8. Si Algo No Funciona

1. **NO inventar endpoints**. Si el backend responde 404 → el endpoint no existe.
2. **NO inventar campos**. Si un PATCH devuelve 200 pero el campo no persiste → el validador Zod lo está rechazando silenciosamente. Verificar el schema en `backend/src/validators/`.
3. **Revisar siempre el código real** antes de asumir:
   - Routes: `backend/src/routes/`
   - Validators: `backend/src/validators/`
   - Schema: `backend/prisma/schema.prisma`
4. **NO tocar datos de otros proyectos** (memory-service tiene su propia BD). Si hay duda → preguntar al PM.

---

**Fin del documento.**
