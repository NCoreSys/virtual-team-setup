# FEATURE: RELEASES Y SPRINTS

| Campo | Valor |
|-------|-------|
| **Feature** | Releases y Sprints |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Sprint origen** | S03 |
| **Estado** | ✅ Implementado (BE/DB) |

---

## 1. QUÉ ES

Estructura jerárquica para organizar el trabajo del proyecto en ciclos de entrega. Un **Release** agrupa varios **Sprints**, y cada Sprint contiene tareas a ejecutar.

```
Proyecto
└── Release (v1.0, v2.0, MVP)
    └── Sprint (S01, S02, S03)
        └── Tareas
```

---

## 2. PARA QUÉ SIRVE

- **Planificación** — Organizar trabajo en iteraciones manejables
- **Seguimiento** — Medir velocidad, burndown, progreso
- **Entrega** — Agrupar funcionalidad para releases
- **Métricas** — Story points, horas, cobertura por sprint/release
- **Gobernanza** — Firmas y aprobaciones por nivel

---

## 3. PRECONDICIONES

| Precondición | Tabla/Entidad | ¿Existe? |
|--------------|---------------|----------|
| Proyecto creado | `projects` | ✅ |

---

## 4. MODELO DE DATOS

### 4.1 Releases

Un release representa una versión o hito de entrega del proyecto.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID | Identificador único |
| `projectId` | UUID | FK al proyecto |
| `code` | String | Código corto (ej: "R1", "MVP", "v2.0") |
| `name` | String | Nombre descriptivo |
| `description` | Text | Descripción del alcance |
| `status` | Enum | Estado del release |
| `startDate` | Date | Fecha de inicio planificada |
| `endDate` | Date | Fecha de fin planificada |
| `actualStartDate` | Date | Fecha de inicio real |
| `actualEndDate` | Date | Fecha de fin real |
| `goals` | Text[] | Objetivos del release |

### 4.2 Sprints

Un sprint es una iteración de trabajo dentro de un release.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID | Identificador único |
| `releaseId` | UUID | FK al release |
| `code` | String | Código corto (ej: "S01", "S02") |
| `name` | String | Nombre descriptivo |
| `order` | Int | Orden dentro del release |
| `status` | Enum | Estado del sprint |
| `startDate` | Date | Fecha de inicio |
| `endDate` | Date | Fecha de fin |
| `velocity` | Int | Velocidad planificada (SP) |
| `actualVelocity` | Int | Velocidad real |
| `sprintGoal` | Text | Objetivo del sprint |

---

## 5. ESTADOS

### 5.1 Estados de Release

| Estado | Código | Descripción |
|--------|--------|-------------|
| Planificado | `planned` | Release definido, sin iniciar |
| En Progreso | `in_progress` | Al menos un sprint activo |
| En QA | `in_qa` | Todos los sprints completados, en validación final |
| Completado | `completed` | Release entregado y cerrado |
| Cancelado | `cancelled` | Release cancelado |

### 5.2 Estados de Sprint

| Estado | Código | Descripción |
|--------|--------|-------------|
| Planificado | `planned` | Sprint definido, sin iniciar |
| Activo | `active` | Sprint en ejecución |
| En Review | `in_review` | Tareas completadas, en revisión |
| En QA | `in_qa` | En testing/validación |
| Completado | `completed` | Sprint cerrado exitosamente |
| Cancelado | `cancelled` | Sprint cancelado |

### 5.3 Transiciones válidas

```
RELEASE:
planned → in_progress → in_qa → completed
                    ↘ cancelled

SPRINT:
planned → active → in_review → in_qa → completed
                           ↘ cancelled
```

---

## 6. FLUJO OPERATIVO

### 6.1 Crear Release

```
POST /api/projects/:projectId/releases
```

```json
{
  "code": "R1",
  "name": "Release 1 - MVP",
  "description": "Primera versión con funcionalidad core",
  "startDate": "2026-05-01",
  "endDate": "2026-07-31",
  "goals": [
    "Import de conversaciones funcional",
    "Context endpoint para Runtime",
    "Dashboard básico"
  ]
}
```

### 6.2 Crear Sprint dentro de Release

```
POST /api/releases/:releaseId/sprints
```

```json
{
  "code": "S01",
  "name": "Sprint 1 - Fundamentos",
  "order": 1,
  "startDate": "2026-05-01",
  "endDate": "2026-05-14",
  "velocity": 21,
  "sprintGoal": "Catálogos base y estructura de datos"
}
```

### 6.3 Iniciar Sprint

```
PATCH /api/sprints/:sprintId/start
```

```json
{
  "startedBy": "uuid-pm"
}
```

**Efecto:**
- Sprint pasa a `active`
- `actualStartDate` se registra
- Release pasa a `in_progress` si estaba en `planned`

### 6.4 Completar Sprint

```
PATCH /api/sprints/:sprintId/complete
```

```json
{
  "completedBy": "uuid-pm",
  "retrospectiveNotes": "Velocidad real: 19 SP. Blocker por dependencia externa."
}
```

**Validaciones previas:**
- Todas las tareas en `completed` o `cancelled`
- Firmas de stage requeridas (si feature Firmas habilitada)
- Gate de devlog pasado (si feature habilitada)

### 6.5 Ver métricas de Sprint

```
GET /api/sprints/:sprintId/metrics
```

```json
{
  "sprintId": "uuid",
  "code": "S01",
  "status": "active",
  "tasks": {
    "total": 15,
    "completed": 8,
    "inProgress": 5,
    "pending": 2
  },
  "storyPoints": {
    "planned": 21,
    "completed": 13,
    "remaining": 8
  },
  "hours": {
    "estimated": 84,
    "actual": 62,
    "remaining": 22
  },
  "burndown": [
    { "day": 1, "remaining": 21 },
    { "day": 2, "remaining": 19 },
    { "day": 3, "remaining": 16 }
  ],
  "velocity": {
    "current": 13,
    "projected": 18
  }
}
```

### 6.6 Ver métricas de Release

```
GET /api/releases/:releaseId/metrics
```

```json
{
  "releaseId": "uuid",
  "code": "R1",
  "status": "in_progress",
  "sprints": {
    "total": 6,
    "completed": 2,
    "active": 1,
    "planned": 3
  },
  "progress": {
    "tasksCompleted": 45,
    "tasksTotal": 120,
    "percent": 37.5
  },
  "storyPoints": {
    "total": 126,
    "completed": 42,
    "velocity": 21
  },
  "timeline": {
    "startDate": "2026-05-01",
    "endDate": "2026-07-31",
    "daysElapsed": 30,
    "daysRemaining": 62,
    "onTrack": true
  }
}
```

---

## 7. ASIGNACIÓN DE TAREAS A SPRINT

### 7.1 Asignar tarea a sprint

```
PATCH /api/tasks/:taskId
```

```json
{
  "sprintId": "uuid-sprint"
}
```

### 7.2 Mover tarea entre sprints

```
PATCH /api/tasks/:taskId/move-sprint
```

```json
{
  "fromSprintId": "uuid-s01",
  "toSprintId": "uuid-s02",
  "reason": "No alcanzó a completarse en S01",
  "movedBy": "uuid-pm"
}
```

**Efecto:**
- Se registra en historial
- Se puede trackear como "spillover"

### 7.3 Ver tareas del sprint

```
GET /api/sprints/:sprintId/tasks
```

---

## 8. BACKLOG

### 8.1 Backlog del Release

Tareas asignadas al release pero sin sprint específico.

```
GET /api/releases/:releaseId/backlog
```

### 8.2 Backlog del Proyecto

Tareas sin release ni sprint asignado.

```
GET /api/projects/:projectId/backlog
```

---

## 9. SPRINT PLANNING

### 9.1 Crear planning session

```
POST /api/sprints/:sprintId/planning
```

```json
{
  "plannedVelocity": 21,
  "participants": ["uuid-pm", "uuid-tl", "uuid-ar"],
  "notes": "Planning del Sprint 3"
}
```

### 9.2 Agregar tareas al sprint durante planning

```
POST /api/sprints/:sprintId/planning/tasks
```

```json
{
  "taskIds": ["uuid-task-1", "uuid-task-2", "uuid-task-3"],
  "addedBy": "uuid-pm"
}
```

---

## 10. ¿ES BLOQUEANTE?

| Situación | ¿Bloquea? |
|-----------|-----------|
| Tarea sin sprint | ❌ No (va al backlog) |
| Sprint sin tareas | ❌ No |
| Completar sprint con tareas pendientes | ⚠️ Configurable |
| Iniciar sprint sin planning | ❌ No |

### Configuración bloqueante

```json
{
  "sprintsConfig": {
    "requireAllTasksComplete": true,
    "requireStageApprovals": true,
    "requireDevlogGate": true
  }
}
```

---

## 11. RESPONSABLES

| Acción | PM | TL | AR | Agente |
|--------|----|----|----|----|
| Crear release | ✅ | ❌ | ❌ | ❌ |
| Crear sprint | ✅ | ✅ | ❌ | ❌ |
| Iniciar sprint | ✅ | ✅ | ❌ | ❌ |
| Completar sprint | ✅ | ✅ | ❌ | ❌ |
| Asignar tarea a sprint | ✅ | ✅ | ✅ | ❌ |
| Ver métricas | ✅ | ✅ | ✅ | ✅ |
| Mover tarea entre sprints | ✅ | ✅ | ❌ | ❌ |

---

## 12. ENDPOINTS

### Releases

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/projects/:projectId/releases` | Listar releases |
| POST | `/api/projects/:projectId/releases` | Crear release |
| GET | `/api/releases/:id` | Ver release |
| PATCH | `/api/releases/:id` | Actualizar release |
| DELETE | `/api/releases/:id` | Eliminar release |
| GET | `/api/releases/:id/metrics` | Métricas del release |
| GET | `/api/releases/:id/backlog` | Backlog del release |
| PATCH | `/api/releases/:id/complete` | Completar release |

### Sprints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/releases/:releaseId/sprints` | Listar sprints |
| POST | `/api/releases/:releaseId/sprints` | Crear sprint |
| GET | `/api/sprints/:id` | Ver sprint |
| PATCH | `/api/sprints/:id` | Actualizar sprint |
| DELETE | `/api/sprints/:id` | Eliminar sprint |
| PATCH | `/api/sprints/:id/start` | Iniciar sprint |
| PATCH | `/api/sprints/:id/complete` | Completar sprint |
| GET | `/api/sprints/:id/metrics` | Métricas del sprint |
| GET | `/api/sprints/:id/tasks` | Tareas del sprint |
| GET | `/api/sprints/:id/burndown` | Datos de burndown |

### Planning

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/sprints/:id/planning` | Crear planning session |
| POST | `/api/sprints/:id/planning/tasks` | Agregar tareas |
| GET | `/api/sprints/:id/planning` | Ver planning |

---

## 13. EJEMPLO COMPLETO

### Escenario

Proyecto Memory Service con Release R1 y 6 sprints.

```
CREAR RELEASE
────────────────────────────────────────────────────────────

POST /api/projects/memory-service/releases
{
  "code": "R1",
  "name": "Memory Service MVP",
  "startDate": "2026-05-01",
  "endDate": "2026-07-15"
}
→ Release creado, status=planned

CREAR SPRINTS
────────────────────────────────────────────────────────────

POST /api/releases/uuid-r1/sprints
{ "code": "S01", "name": "Fundamentos", "order": 1, "velocity": 18 }

POST /api/releases/uuid-r1/sprints
{ "code": "S02", "name": "Import Core", "order": 2, "velocity": 21 }

(... S03 a S06)

INICIAR SPRINT
────────────────────────────────────────────────────────────

PATCH /api/sprints/uuid-s01/start
→ Sprint S01: active
→ Release R1: in_progress

ASIGNAR TAREAS
────────────────────────────────────────────────────────────

PATCH /api/tasks/uuid-task-1
{ "sprintId": "uuid-s01" }

PATCH /api/tasks/uuid-task-2
{ "sprintId": "uuid-s01" }

VER PROGRESO
────────────────────────────────────────────────────────────

GET /api/sprints/uuid-s01/metrics
{
  "tasks": { "total": 12, "completed": 8, "inProgress": 3, "pending": 1 },
  "storyPoints": { "planned": 18, "completed": 14 }
}

COMPLETAR SPRINT
────────────────────────────────────────────────────────────

PATCH /api/sprints/uuid-s01/complete
{ "retrospectiveNotes": "Completado con velocidad 16 SP" }

→ Sprint S01: completed
→ actualVelocity: 16
```

---

## 14. TABLAS EN BASE DE DATOS

### releases

```sql
CREATE TABLE releases (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  
  code VARCHAR(50) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  
  status VARCHAR(50) DEFAULT 'planned',
  
  start_date DATE,
  end_date DATE,
  actual_start_date DATE,
  actual_end_date DATE,
  
  goals TEXT[],
  
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(project_id, code)
);

CREATE INDEX idx_releases_project ON releases(project_id);
CREATE INDEX idx_releases_status ON releases(status);
```

### sprints

```sql
CREATE TABLE sprints (
  id TEXT PRIMARY KEY,
  release_id TEXT NOT NULL REFERENCES releases(id) ON DELETE CASCADE,
  
  code VARCHAR(50) NOT NULL,
  name VARCHAR(255) NOT NULL,
  "order" INT NOT NULL,
  
  status VARCHAR(50) DEFAULT 'planned',
  
  start_date DATE,
  end_date DATE,
  actual_start_date DATE,
  actual_end_date DATE,
  
  velocity INT,
  actual_velocity INT,
  
  sprint_goal TEXT,
  retrospective_notes TEXT,
  
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(release_id, code)
);

CREATE INDEX idx_sprints_release ON sprints(release_id);
CREATE INDEX idx_sprints_status ON sprints(status);
```

### ALTER tasks

```sql
ALTER TABLE tasks 
ADD COLUMN sprint_id TEXT REFERENCES sprints(id),
ADD COLUMN release_id TEXT REFERENCES releases(id);

CREATE INDEX idx_tasks_sprint ON tasks(sprint_id);
CREATE INDEX idx_tasks_release ON tasks(release_id);
```

---

## 15. CONFIGURACIÓN

### Por proyecto

```json
{
  "sprintsConfig": {
    "enabled": true,
    "defaultDuration": 14,
    "defaultVelocity": 21,
    "requireAllTasksComplete": false,
    "requireStageApprovals": true,
    "requireDevlogGate": true,
    "autoCreateSprintFolders": true
  }
}
```

---

## 16. INTEGRACIÓN CON OTRAS FEATURES

| Feature | Integración |
|---------|-------------|
| **Firmas** | Stage/Sprint/Release approvals |
| **Trackable Items** | Deferrals entre sprints |
| **Criterios** | DoD gate para completar sprint |
| **Project Folders** | Auto-crear carpeta por sprint |
| **Métricas** | Velocidad, burndown, story points |

---

**Documento:** FEATURE_RELEASES_SPRINTS.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06
