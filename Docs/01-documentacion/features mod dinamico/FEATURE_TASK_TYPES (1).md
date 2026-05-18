# FEATURE: TASK TYPES (Tipos de Tarea)

| Campo | Valor |
|-------|-------|
| **Feature** | Task Types |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Estado** | 📋 DISEÑADO — Pendiente implementación |
| **Origen** | PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md (P3) |

---

## 1. QUÉ ES

Catálogo que clasifica las tareas por tipo de trabajo (backend, frontend, documentation, testing, etc.). Determina qué templates de DoD/DoR se aplican automáticamente y permite reportes de velocidad por tipo.

---

## 2. PARA QUÉ SIRVE

- **Herencia de DoD** — Cada tipo de tarea hereda automáticamente sus criterios de Definition of Done
- **Reportes** — Velocidad y métricas por tipo de trabajo
- **Filtros** — Buscar tareas por tipo en el backlog
- **Asignación** — Sugerir asignado según tipo (BE-Agent para backend, etc.)

---

## 3. PRECONDICIONES

| Precondición | Tabla/Entidad | ¿Existe? |
|--------------|---------------|----------|
| Catálogo de tipos de proyecto | `project_type_catalog` | ✅ |
| Tareas existentes | `tasks` | ✅ |

---

## 4. CATÁLOGO DE TASK TYPES

### 4.1 Tipos iniciales

| code | name | Descripción | DoD que hereda | Parent category |
|------|------|-------------|----------------|-----------------|
| `backend` | Backend Development | Endpoints, servicios, lógica de negocio | DOD-BE-01..12 | development |
| `frontend` | Frontend Development | Componentes UI, vistas, interacción | DOD-FE-01..09 | development |
| `database` | Database | Schema, migrations, seeds, índices | DOD-BE-01..12 | development |
| `documentation` | Documentation / Analysis | Documentos SDLC, análisis, specs | DOD-DOC-01..08 | documentation |
| `testing` | QA Testing | Tests, validación, certificación | DOD-QA-01..06 | testing |
| `devops` | Infrastructure / DevOps | Docker, CI/CD, monitoreo, deployment | DOD-BE subset | development |
| `design` | Design | Wireframes, design system, specs UX | DOD-DL (por definir) | design |
| `research` | Research | Investigación, spikes, PoC | Ninguno | analysis |
| `meeting` | Meeting | Reuniones, ceremonies | Ninguno | coordination |

### 4.2 Relación con projectTypeCode

Los task types están filtrados por tipo de proyecto:

| projectTypeCode | Task types disponibles |
|-----------------|------------------------|
| `software` | backend, frontend, database, documentation, testing, devops, design, research |
| `marketing` | documentation, design, research, meeting |
| `research` | documentation, research, meeting |

---

## 5. CÓMO SE ACTIVA

### ¿Cómo se asigna el taskTypeCode?

**Modo híbrido:** Se infiere del rol del asignado pero es editable.

| Rol asignado | taskTypeCode inferido |
|--------------|----------------------|
| BE-Agent, DB-Agent | `backend` |
| FE-Agent | `frontend` |
| SA, AR | `documentation` |
| QA | `testing` |
| DL | `design` |
| DevOps | `devops` |
| PM, TL | (no se infiere, debe asignarse) |

### ¿Se puede cambiar después?

| Estado de tarea | ¿Editable? | ¿Quién? |
|-----------------|------------|---------|
| Pending / Defined | ✅ Sí | PM, TL, asignado |
| In Progress | ⚠️ Sí, con advertencia | PM, TL |
| In Review / Completed | ❌ No | — |

**Advertencia al cambiar en In Progress:** "Cambiar el tipo de tarea puede modificar los criterios DoD aplicables. ¿Continuar?"

---

## 6. FLUJO OPERATIVO

### 6.1 Al crear tarea

```
PASO 1: PM/TL crea tarea y asigna a agente
─────────────────────────────────────────────────
POST /api/tasks
{
  "title": "Implementar POST /users",
  "assigneeId": "uuid-be-agent",
  ...
}

PASO 2: Sistema infiere taskTypeCode
─────────────────────────────────────────────────
BE-Agent tiene role=backend → taskTypeCode="backend"

PASO 3: Sistema aplica templates de DoD
─────────────────────────────────────────────────
Busca criteria_template WHERE taskTypeCode="backend"
Crea acceptance_criteria en la tarea automáticamente

PASO 4: Tarea creada con DoD heredado
─────────────────────────────────────────────────
La tarea tiene 12 criterios DOD-BE-01..12 automáticamente
```

### 6.2 Override manual

```
PASO 1: PM decide que la tarea es realmente de documentación
─────────────────────────────────────────────────
Aunque la asignó a BE-Agent, es una tarea de análisis.

PASO 2: PM cambia taskTypeCode
─────────────────────────────────────────────────
PATCH /api/tasks/:id
{
  "taskTypeCode": "documentation"
}

PASO 3: Sistema pregunta qué hacer con DoD
─────────────────────────────────────────────────
Response:
{
  "warning": "Task type changed. DoD criteria will be updated.",
  "currentDoD": ["DOD-BE-01", "DOD-BE-02", ...],
  "newDoD": ["DOD-DOC-01", "DOD-DOC-02", ...],
  "action": "confirm_required"
}

PASO 4: PM confirma
─────────────────────────────────────────────────
PATCH /api/tasks/:id/confirm-type-change
{
  "confirmed": true
}

→ Se eliminan DOD-BE-*, se agregan DOD-DOC-*
```

---

## 7. ¿ES BLOQUEANTE?

**No.** El taskTypeCode es informativo y para herencia de DoD. No bloquea ninguna transición.

| Situación | ¿Bloquea? |
|-----------|-----------|
| Tarea sin taskTypeCode | ❌ No (pero no hereda DoD) |
| taskTypeCode inválido | ❌ Error de validación al crear |
| Cambiar taskTypeCode en In Progress | ❌ No (solo advertencia) |

---

## 8. RESPONSABLES

| Acción | PM | TL | Agente |
|--------|----|----|--------|
| Crear task type en catálogo | ❌ | ❌ | ❌ (Admin VTT) |
| Asignar taskTypeCode a tarea | ✅ | ✅ | ✅ (su propia tarea) |
| Cambiar taskTypeCode | ✅ | ✅ | ⚠️ (solo si pending) |
| Ver taskTypeCode | ✅ | ✅ | ✅ |

---

## 9. ENDPOINTS

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/task-types` | Listar tipos disponibles |
| GET | `/api/task-types?projectTypeCode=software` | Filtrar por tipo de proyecto |
| GET | `/api/task-types/:code` | Detalle de un tipo |

**Nota:** CRUD completo solo para Admin VTT. Los proyectos usan el catálogo existente.

---

## 10. EJEMPLO COMPLETO

### Escenario

Crear tarea de backend en proyecto Memory Service (software).

```
POST /api/tasks
{
  "projectId": "uuid-memory-service",
  "title": "Implementar POST /api/conversations/import",
  "assigneeId": "uuid-be-agent"
}

Response:
{
  "id": "uuid-task",
  "title": "Implementar POST /api/conversations/import",
  "taskTypeCode": "backend",  // Inferido de BE-Agent
  "criteria": [
    { "code": "DOD-BE-01", "description": "Código compila sin errores TypeScript" },
    { "code": "DOD-BE-02", "description": "Validación Zod implementada" },
    { "code": "DOD-BE-03", "description": "Tests unitarios pasan" },
    // ... 12 criterios DOD-BE heredados
  ]
}
```

---

## 11. TABLAS EN BASE DE DATOS

### task_type_catalog

```sql
CREATE TABLE task_type_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  parent_category VARCHAR(50),  -- development, testing, documentation, design, coordination
  project_type_code VARCHAR(50) REFERENCES project_type_catalog(code),
  dod_template_group VARCHAR(50),  -- DOD-BE, DOD-FE, DOD-DOC, DOD-QA
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_task_type_project ON task_type_catalog(project_type_code);
```

### Seed inicial

```sql
INSERT INTO task_type_catalog (code, name, description, parent_category, project_type_code, dod_template_group, sort_order) VALUES
('backend',       'Backend Development',      'Endpoints, servicios, lógica de negocio',    'development',   'software', 'DOD-BE',  1),
('frontend',      'Frontend Development',     'Componentes UI, vistas, interacción',        'development',   'software', 'DOD-FE',  2),
('database',      'Database',                 'Schema, migrations, seeds, índices',         'development',   'software', 'DOD-BE',  3),
('documentation', 'Documentation / Analysis', 'Documentos SDLC, análisis, specs',           'documentation', 'software', 'DOD-DOC', 4),
('testing',       'QA Testing',               'Tests, validación, certificación',           'testing',       'software', 'DOD-QA',  5),
('devops',        'Infrastructure / DevOps',  'Docker, CI/CD, monitoreo, deployment',       'development',   'software', 'DOD-BE',  6),
('design',        'Design',                   'Wireframes, design system, specs UX',        'design',        'software', NULL,      7),
('research',      'Research',                 'Investigación, spikes, PoC',                 'analysis',      'software', NULL,      8),
('meeting',       'Meeting',                  'Reuniones, ceremonies',                      'coordination',  'software', NULL,      9);
```

### ALTER tasks

```sql
ALTER TABLE tasks 
ADD COLUMN task_type_code VARCHAR(50) REFERENCES task_type_catalog(code);

CREATE INDEX idx_tasks_type ON tasks(task_type_code);
```

---

## 12. INTEGRACIÓN CON OTRAS FEATURES

| Feature | Integración |
|---------|-------------|
| **Criteria Templates** | taskTypeCode determina qué DoD se hereda |
| **Firmas** | DoD debe estar met para firmar stage/sprint |
| **Reportes** | Velocidad por taskType, distribución de trabajo |
| **Asignación** | Sugerir agente según taskType |

---

## 13. CONFIGURACIÓN

### En proyecto (opcional)

```json
{
  "taskTypeConfig": {
    "inferFromRole": true,
    "allowChangeInProgress": true,
    "requireTaskType": false
  }
}
```

| Campo | Descripción | Default |
|-------|-------------|---------|
| `inferFromRole` | Inferir taskTypeCode del rol del asignado | `true` |
| `allowChangeInProgress` | Permitir cambiar en In Progress | `true` |
| `requireTaskType` | Obligar taskTypeCode al crear tarea | `false` |

---

## 14. FAQ

**¿Puedo crear mis propios task types?**
No. El catálogo es global y gestionado por Admin VTT. Si necesitas un tipo nuevo, solicítalo.

**¿Qué pasa si no asigno taskTypeCode?**
La tarea se crea sin DoD heredado. Los criterios se deben agregar manualmente.

**¿El taskTypeCode afecta el flujo de la tarea?**
No directamente. Solo afecta qué DoD se hereda y cómo aparece en reportes.

**¿Puedo tener una tarea de backend asignada a FE-Agent?**
Sí. El taskTypeCode y el assignee son independientes. El tipo se puede asignar manualmente.

---

**Documento:** FEATURE_TASK_TYPES.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06
