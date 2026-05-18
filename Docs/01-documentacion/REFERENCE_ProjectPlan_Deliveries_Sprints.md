---
name: Project Plan — Deliveries y Sprints
description: Cómo funciona el Gantt, el Dashboard y la agrupación de tareas por entregables y sprints
type: reference
---

# REFERENCE: Project Plan — Deliveries, Sprints y Agrupación

**Última actualización:** 2026-05-12

---

## TL;DR — La pregunta más común

> "¿Por qué mis tareas aparecen en 'SIN ENTREGABLE' si ya creé los Deliveries?"

**Porque crear un Delivery no asigna las tareas automáticamente.**  
Crear el Delivery es solo crear el contenedor. Para que una tarea aparezca bajo un Delivery, debes asignarla explícitamente vía API:

```
POST /api/deliveries/:deliveryId/tasks/:taskId
Body: { "assignedBy": "<userId>" }
```

---

## 1. Conceptos: Delivery vs Sprint

| Concepto | Qué es | Dónde vive |
|----------|--------|-----------|
| **Delivery** | Contenedor de tareas dentro de una Fase. Es el agrupador principal en el Gantt y Dashboard. | `Deliveries` table — `phaseId` FK |
| **Sprint** | Agrupador de tareas dentro de un Release (módulo Releases/Sprints). Independiente del Gantt. | `Sprint` table — `releaseId` FK |
| **deliveryId** | Campo en `Task` que indica a qué Delivery pertenece (null = sin entregable) | `Task.deliveryId` nullable |
| **sprintId** | Campo en `Task` que indica a qué Sprint pertenece (null = sin sprint) | `Task.sprintId` nullable |

**Una tarea puede tener ambos** (deliveryId Y sprintId) — son relaciones independientes.

---

## 2. Flujo de datos: Project Plan (Gantt)

### Cómo carga el Gantt la agrupación

Cuando el usuario selecciona una Fase y activa **"Agrupar: Entregable"**, el Gantt hace **dos fetches en paralelo**:

```
Fetch 1: GET /api/phases/:phaseId/deliveries
         → Lista de deliveries de la fase, con tasksByStatus y _count.tasks

Fetch 2: GET /api/tasks?phaseId=:phaseId&limit=500
         → Todas las tareas de la fase, con campo deliveryId en cada una
```

Luego construye un mapa `taskId → Delivery` y agrupa las tareas.

### Resultado de la agrupación

```
groupedRows = [
  { type: 'header', name: 'Sprint 1 — Backend',  taskCount: 5 },
  { type: 'task',   key: 'VTT-100', ... },
  { type: 'task',   key: 'VTT-101', ... },
  ...
  { type: 'header', name: 'Sprint 2 — Frontend', taskCount: 3 },
  { type: 'task',   key: 'VTT-110', ... },
  ...
  { type: 'header', name: 'Sin entregable',       taskCount: 8 },  ← tareas sin deliveryId
  { type: 'task',   key: 'VTT-120', ... },
  ...
]
```

### Sin toggle "Agrupar: Entregable"

Las tareas se ordenan **por sprint detectado en el título** (parsing del patrón `-S11`, `-S10`, etc.) y luego por número VTT. No usa deliveries ni sprintId — es solo orden visual.

```
Título "VTT-463 — [BE-S11-01] Endpoint X" → sprint order = 11
Título "VTT-464 — [FE-S09-02] Component Y" → sprint order = 9
```

---

## 3. Flujo de datos: Dashboard

### PhaseProgressTable (tabla principal del dashboard)

- Muestra una fila por Fase con totales de tareas
- Botón **"+"** expande la fila → carga deliveries de esa fase
- Cada Delivery aparece como sub-fila indentada con su progreso

```
Fase 11 — MGP Sprint        [+]    100 tareas    45% completado
  └── Sprint S11 — Backend         20 tareas     60% completado
  └── Sprint S11 — Frontend        30 tareas     40% completado
  └── Bugs S11                     10 tareas     30% completado
```

El progreso de cada Delivery se calcula:
```
denominator = total_tareas - cancelled
progress    = round((approved + completed) / denominator * 100)
```

### TaskListPanel (modal de lista de tareas)

Aparece cuando haces click en una fase o un número de tareas. Si recibe `phaseId`:
1. Carga deliveries de la fase con `usePhaseDeliveries`
2. Agrupa las tareas por `deliveryId`
3. Tareas sin `deliveryId` van a la sección "Sin deliverable"

---

## 4. Hook: usePhaseDeliveries

```
usePhaseDeliveries(phaseId, enabled)
  └── GET /api/phases/:phaseId/deliveries        → lista base con tasksByStatus
  └── GET /api/deliveries/:id  (por cada delivery) → enriquece con taskIds[]
```

**Por qué hace N+1 fetches:** El endpoint de lista no retorna los IDs individuales de las tareas, solo el conteo. El hook necesita los IDs para hacer el mapeo tarea→delivery en el frontend.

---

## 5. Endpoints de Deliveries

### CRUD

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `POST /api/deliveries` | POST | Crear delivery |
| `GET /api/phases/:phaseId/deliveries` | GET | Listar deliveries de una fase |
| `GET /api/deliveries/:id` | GET | Detalle con lista de tareas |
| `PUT /api/deliveries/:id` | PUT | Actualizar nombre, orden, status |
| `DELETE /api/deliveries/:id` | DELETE | Eliminar (libera deliveryId en tareas) |

### Asignación de tareas

| Endpoint | Método | Body | Descripción |
|----------|--------|------|-------------|
| `POST /api/deliveries/:id/tasks/:taskId` | POST | `{ assignedBy }` | Asignar tarea al delivery |
| `DELETE /api/deliveries/:id/tasks/:taskId` | DELETE | `{ unassignedBy }` | Desasignar tarea |

### Body de creación

```json
{
  "phaseId": "uuid-de-la-fase",
  "name": "Sprint S11 — Backend",
  "order": 1,
  "createdBy": "uuid-del-usuario",
  "statusId": "2f115b5b-2664-42b4-ba96-88c3b62863a2"
}
```

---

## 6. Reglas de negocio

| Regla | Descripción |
|-------|-------------|
| **RN-010** | La tarea y el Delivery deben pertenecer a la misma Fase. Si no coinciden → 409 `RN-010_PHASE_MISMATCH` |
| **RN-004** | Una tarea solo puede estar en UN Delivery a la vez. Asignar a otro → 409 `RN-004_ALREADY_ASSIGNED` |
| **VTT-506** | El nombre del Delivery debe ser único dentro de la Fase |

---

## 7. Cuándo aparece "SIN ENTREGABLE"

Una tarea aparece bajo "Sin entregable" en el Gantt cuando:

1. `task.deliveryId` es `null` (nunca fue asignada a un Delivery)
2. `task.deliveryId` apunta a un Delivery que no pertenece a la fase seleccionada
3. El Delivery fue eliminado (Prisma hace `onDelete: SetNull` → limpia el FK)

### Solución: asignar masivamente

Si ya tienes los Deliveries creados y necesitas asignar 60+ tareas, la forma más rápida es via API en bulk:

```bash
# Obtener deliveries de la fase
GET /api/phases/:phaseId/deliveries

# Para cada tarea:
POST /api/deliveries/:deliveryId/tasks/:taskId
Body: { "assignedBy": "<userId>" }
```

---

## 8. Campos en el modelo Task relevantes para agrupación

| Campo | Tipo | Controla |
|-------|------|----------|
| `deliveryId` | String? | Agrupación en Gantt y Dashboard |
| `sprintId` | String? | Agrupación en módulo Releases/Sprints (SprintDetailPage) |
| `phase` | via `phaseTasks` | En qué fase aparece la tarea |

**El campo `deliveryId` es el único que controla la agrupación en el Gantt y el Dashboard.**  
El campo `sprintId` es independiente y solo afecta el módulo de Sprints.

---

## 9. Estructura del response de deliveries

```json
// GET /api/phases/:phaseId/deliveries
[
  {
    "id": "uuid-delivery",
    "phaseId": "uuid-fase",
    "name": "Sprint S11 — Backend",
    "order": 1,
    "lifecycleStage": "development",
    "status": { "id": "...", "code": "delivery_active", "name": "Active" },
    "_count": { "tasks": 20 },
    "tasksByStatus": {
      "pending": 5,
      "in_progress": 3,
      "in_review": 2,
      "completed": 4,
      "approved": 6,
      "on_hold": 0,
      "cancelled": 0
    }
  }
]

// GET /api/deliveries/:id  (detalle)
{
  "id": "uuid-delivery",
  "name": "Sprint S11 — Backend",
  ...
  "tasks": [
    { "id": "VTT-463", "title": "...", "status": {...} },
    { "id": "VTT-464", "title": "...", "status": {...} }
  ]
}
```

---

## 10. Archivos clave en el codebase

| Archivo | Responsabilidad |
|---------|----------------|
| [GanttChart.tsx](../../../frontend/src/components/gantt/GanttChart.tsx) | Lógica de agrupación, fetch de deliveries, toggle, colapso |
| [usePhaseDeliveries.ts](../../../frontend/src/hooks/usePhaseDeliveries.ts) | Hook — carga deliveries + enriquece con taskIds |
| [TaskListPanel.tsx](../../../frontend/src/components/dashboard/TaskListPanel.tsx) | Modal de lista de tareas agrupadas por delivery |
| [PhaseProgressTable.tsx](../../../frontend/src/components/dashboard/PhaseProgressTable.tsx) | Tabla del dashboard con sub-filas de deliveries |
| [delivery.service.ts](../../../backend/src/services/delivery.service.ts) | Lógica backend — CRUD, assignTask, validaciones |
| [deliveries.ts (routes)](../../../backend/src/routes/deliveries.ts) | Endpoints REST de deliveries |
