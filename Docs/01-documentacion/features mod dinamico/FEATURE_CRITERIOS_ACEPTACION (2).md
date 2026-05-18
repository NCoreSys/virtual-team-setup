# FEATURE: CRITERIOS DE ACEPTACIÓN

| Campo | Valor |
|-------|-------|
| **Feature** | Criterios de Aceptación (AC, DoD, DoR, Templates) |
| **Versión** | 2.0 |
| **Fecha** | 2026-05-06 |
| **Sprint origen** | S09, S10 + Propuesta Criteria System |
| **Estado** | ✅ Diseño completo — Pendiente implementación de templates |

---

## 1. QUÉ ES

Sistema integral de criterios que define las condiciones de éxito para las tareas. Incluye:

| Tipo | Código | Propósito |
|------|--------|-----------|
| **Acceptance Criteria (AC)** | AC-US-XXX-N | Criterios funcionales derivados de User Stories (formato Gherkin) |
| **Definition of Done (DoD)** | DOD-XX-NN | Checklist de completitud por tipo de tarea |
| **Definition of Ready (DoR)** | DOR-NN | Precondiciones para iniciar una tarea |

---

## 2. PARA QUÉ SIRVE

- **Claridad** — Define exactamente qué significa "terminado" y "listo para empezar"
- **Verificación** — Checklist objetivo para agentes y revisores
- **Trazabilidad** — Registro de quién verificó qué y cuándo
- **Calidad** — Evita ambigüedad, garantiza estándares mínimos
- **Gate** — DoR bloquea inicio, DoD bloquea cierre si no se cumplen

---

## 3. ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CRITERIA SYSTEM                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TEMPLATES (Plantillas reutilizables)                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  GLOBALES (por projectTypeCode)          PROYECTO (específicos)    │   │
│  │  ┌─────────────────────────┐            ┌─────────────────────┐    │   │
│  │  │ DOD-BE-01: Compila TS   │            │ DOD-BE-06: Máquina  │    │   │
│  │  │ DOD-BE-02: Zod impl.    │     +      │   de estados        │    │   │
│  │  │ DOD-BE-03: Tests pasan  │            │ DOD-BE-07: Idempot. │    │   │
│  │  │ ...                     │            │ ...                 │    │   │
│  │  └─────────────────────────┘            └─────────────────────┘    │   │
│  │              │                                    │                 │   │
│  │              └────────────┬───────────────────────┘                 │   │
│  │                           ▼                                         │   │
│  │                  HERENCIA AL CREAR TAREA                           │   │
│  │                           │                                         │   │
│  └───────────────────────────┼─────────────────────────────────────────┘   │
│                              ▼                                              │
│  TASK CRITERIA (Criterios en la tarea)                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  Tarea VTT-423: Implementar POST /users                            │   │
│  │  taskTypeCode: backend                                              │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐       │   │
│  │  │ DoR (14 items)  │ │ DoD (12 items)  │ │ AC Gherkin (5)  │       │   │
│  │  │ DOR-01..14      │ │ DOD-BE-01..12   │ │ AC-US-001-1..5  │       │   │
│  │  │ Gate: start     │ │ Gate: complete  │ │ Funcionales     │       │   │
│  │  └─────────────────┘ └─────────────────┘ └─────────────────┘       │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. PRECONDICIONES

| Precondición | Tabla/Entidad | ¿Existe? |
|--------------|---------------|----------|
| Proyecto creado | `projects` | ✅ |
| Tarea creada | `tasks` | ✅ |
| Catálogo criteria types | `criteria_type_catalog` | ✅ (actualizar con dod, dor) |
| Catálogo task types | `task_type_catalog` | 🆕 Nuevo |
| Templates de criterios | `criteria_template` | 🆕 Nuevo |

### Seeds necesarios

**criteria_type_catalog (agregar):**

| code | name | Descripción |
|------|------|-------------|
| `dod` | Definition of Done | Criterio de completitud |
| `dor` | Definition of Ready | Precondición para iniciar |

---

## 5. CRITERIA TEMPLATES

### 5.1 Concepto

Un template es un criterio predefinido que se aplica automáticamente a las tareas según su contexto.

### 5.2 Niveles de scope

| Scope | Aplica a | Gestionado por | Ejemplo |
|-------|----------|----------------|---------|
| **Global** | Todos los proyectos de un `projectTypeCode` | Admin VTT | "Código compila TS" para todo `software` |
| **Proyecto** | Solo un proyecto específico | PM + AR del proyecto | "Idempotencia verificada" solo para Memory Service |

### 5.3 Herencia

Al crear una tarea con `taskTypeCode=backend` en proyecto `software`:

```
1. Sistema busca templates globales:
   scope=global AND projectTypeCode=software AND taskTypeCode=backend

2. Sistema busca templates de proyecto:
   scope=project AND projectId={projectId} AND taskTypeCode=backend

3. Combina ambos (proyecto puede override global si mismo código)

4. Crea criterios en la tarea automáticamente
```

### 5.4 Ejemplo de templates DoD por taskType

**DOD-BE (Backend):**

| code | description |
|------|-------------|
| DOD-BE-01 | Código compila sin errores TypeScript (tsc --noEmit) |
| DOD-BE-02 | Validación Zod implementada para el endpoint |
| DOD-BE-03 | Tests unitarios pasan (npm test) |
| DOD-BE-04 | Endpoint probado localmente con curl/Postman |
| DOD-BE-05 | Swagger/JSDoc actualizado |
| DOD-BE-06 | Máquina de estados respetada (sin transiciones prohibidas) |
| DOD-BE-07 | Idempotencia verificada si aplica |
| DOD-BE-08 | Code Logic (.LOGIC.md) creado/actualizado |
| DOD-BE-09 | Development Log creado |
| DOD-BE-10 | PR creado con referencia a tarea VTT |
| DOD-BE-11 | Sin console.log de debug |
| DOD-BE-12 | Sin TODOs sin resolver |

**DOD-FE (Frontend):**

| code | description |
|------|-------------|
| DOD-FE-01 | Componente renderiza sin errores en browser |
| DOD-FE-02 | Happy path probado manualmente |
| DOD-FE-03 | Estados de error implementados (404, 500, timeout) |
| DOD-FE-04 | Estado de carga implementado (spinner/skeleton) |
| DOD-FE-05 | Desktop ≥1280px verificado |
| DOD-FE-06 | Integración con endpoint backend verificada |
| DOD-FE-07 | Code Logic (.LOGIC.md) creado/actualizado |
| DOD-FE-08 | Development Log creado |
| DOD-FE-09 | Sin console.log de debug |

**DOD-DOC (Documentation):**

| code | description |
|------|-------------|
| DOD-DOC-01 | Todos los archivos del delivery creados en ruta del ASSIGNMENT |
| DOD-DOC-02 | Criterios de completitud del BRIEF cumplidos |
| DOD-DOC-03 | Sin secciones vacías, TODOs ni placeholders |
| DOD-DOC-04 | Devlog creado |
| DOD-DOC-05 | Code Logic creado si aplica |
| DOD-DOC-06 | Archivos subidos a VTT con fileType correcto |
| DOD-DOC-07 | Comentario de entrega en tarea VTT |
| DOD-DOC-08 | Tarea movida a task_in_review |

**DOD-QA (Testing):**

| code | description |
|------|-------------|
| DOD-QA-01 | Plan de pruebas documentado |
| DOD-QA-02 | Test cases ejecutados (pass/fail registrado) |
| DOD-QA-03 | Defectos registrados como Bug en VTT |
| DOD-QA-04 | Cobertura de escenarios críticos verificada |
| DOD-QA-05 | Resultados documentados en devlog |
| DOD-QA-06 | Evidence screenshots/logs para features visuales |

### 5.5 Templates DoR (Universal)

| code | description |
|------|-------------|
| DOR-01 | ASSIGNMENT leído completamente |
| DOR-02 | Todas las dependencias en task_completed |
| DOR-03 | Ambigüedades resueltas o escaladas |
| DOR-04 | Fuentes de referencia accesibles |
| DOR-05 | BD accesible desde entorno de desarrollo |
| DOR-06 | Storage montado con permisos |
| DOR-07 | Variables de entorno configuradas |
| DOR-08 | Rama Git creada: feature/{TASK-CODE} |
| DOR-09 | npm install sin errores |
| DOR-10 | SPEC disponible y leída |
| DOR-11 | Documentos de análisis relevantes disponibles |
| DOR-12 | Si modifica schema: migration verificada local |
| DOR-13 | Si depende de catálogos: seed ejecutado |
| DOR-14 | Contrato del endpoint definido (solo BE) |

---

## 6. FLUJO OPERATIVO

### 6.1 Crear tarea con herencia de templates

```
PASO 1: PM/TL crea tarea
─────────────────────────────────────────────────
POST /api/tasks
{
  "title": "Implementar POST /users",
  "assigneeId": "uuid-be-agent",
  "taskTypeCode": "backend"  // O se infiere del rol
}

PASO 2: Sistema hereda templates
─────────────────────────────────────────────────
- Busca DOD-BE-* globales + de proyecto
- Busca DOR-* universales
- Crea criterios en la tarea

PASO 3: Tarea creada con criterios
─────────────────────────────────────────────────
Response incluye 12 DOD + 14 DOR + 0 AC (AC se agregan después)
```

### 6.2 Agregar Acceptance Criteria (Gherkin)

```
PASO 1: SA/PM define AC funcionales
─────────────────────────────────────────────────
POST /api/tasks/:taskId/criteria
{
  "criteriaTypeCode": "functional",
  "code": "AC-US-001-1",
  "title": "Import exitoso primera vez",
  "description": "Given JSONL válido, When POST /import, Then HTTP 201 IMPORTED"
}

PASO 2: Criterio agregado a la tarea
─────────────────────────────────────────────────
Se suma a los DOD y DOR ya heredados.
```

### 6.3 Validación DoR al iniciar tarea (BLOQUEANTE)

```
PASO 1: Agente intenta iniciar tarea
─────────────────────────────────────────────────
PATCH /api/tasks/:id/status
{ "statusCode": "in_progress" }

PASO 2: Sistema verifica DoR
─────────────────────────────────────────────────
Busca criterios tipo "dor" con status != "met"

PASO 3a: Si todos met → OK
─────────────────────────────────────────────────
Transición permitida.

PASO 3b: Si hay pending → BLOQUEADO
─────────────────────────────────────────────────
Response:
{
  "statusCode": 422,
  "error": "DOR_NOT_MET",
  "pendingCriteria": ["DOR-05", "DOR-12"],
  "message": "2 DoR criteria pending. Provide overrideReason to proceed."
}

PASO 4: Override con justificación (opcional)
─────────────────────────────────────────────────
PATCH /api/tasks/:id/status
{
  "statusCode": "in_progress",
  "overrideReason": "BD no disponible aún, pero puedo avanzar con lógica pura"
}

→ Se registra override en historial
→ Transición permitida
```

### 6.4 Fulfillment dual: Agente reporta → TL verifica

```
PASO 1: Agente completa trabajo
─────────────────────────────────────────────────
Implementó el endpoint.

PASO 2: Agente reporta cumplimiento
─────────────────────────────────────────────────
POST /api/criteria/:criteriaId/fulfill
{
  "status": "reported",
  "evidence": "Endpoint probado con curl. PR #125 creado."
}

→ fulfillmentStatus = "reported"
→ reportedBy = agente
→ reportedAt = now()

PASO 3: Agente mueve a review
─────────────────────────────────────────────────
PATCH /api/tasks/:id/status { "statusCode": "in_review" }

Requiere: todos los DoD en "reported" mínimo.

PASO 4: TL verifica
─────────────────────────────────────────────────
POST /api/criteria/:criteriaId/verify
{
  "status": "verified",
  "comment": "Confirmado en code review"
}

→ fulfillmentStatus = "verified"
→ verifiedBy = TL
→ verifiedAt = now()

PASO 5: Si TL rechaza
─────────────────────────────────────────────────
POST /api/criteria/:criteriaId/verify
{
  "status": "rejected",
  "reason": "Test unitario no cubre edge case X"
}

→ fulfillmentStatus = "rejected"
→ Tarea vuelve a in_progress para corrección
```

### 6.5 Desactivar criterio que no aplica

```
PASO 1: PM/TL determina que DOD-BE-07 no aplica
─────────────────────────────────────────────────
Es un endpoint GET de solo lectura, no requiere idempotencia.

PASO 2: PM/TL desactiva
─────────────────────────────────────────────────
PATCH /api/criteria/:criteriaId
{
  "isApplicable": false,
  "disabledReason": "Endpoint GET de solo lectura, no aplica idempotencia"
}

→ isApplicable = false
→ disabledReason = "..."
→ disabledBy = PM/TL
→ Criterio no cuenta en validaciones
→ Sigue visible con indicador "(No aplica)"
```

### 6.6 Deprecar AC (corregir sin perder historial)

```
PASO 1: SA descubre error en AC-US-001-1
─────────────────────────────────────────────────
Debería ser HTTP 200, no HTTP 201 (por idempotencia).

PASO 2: SA depreca el original
─────────────────────────────────────────────────
PATCH /api/criteria/:criteriaId
{
  "acStatus": "deprecated"
}

PASO 3: SA crea el nuevo
─────────────────────────────────────────────────
POST /api/tasks/:taskId/criteria
{
  "code": "AC-US-001-1b",
  "description": "Import exitoso retorna HTTP 200",
  "acStatus": "added_post_approval"
}

PASO 4: Vincular reemplazo
─────────────────────────────────────────────────
PATCH /api/criteria/:oldId
{
  "supersededBy": "uuid-new-criteria"
}

→ Historial: AC-US-001-1 → deprecated → AC-US-001-1b
```

---

## 7. REGLAS DE TRANSICIÓN

| Transición | Validación de criterios |
|------------|------------------------|
| → `in_progress` | Todos los DoR deben estar `met` (o override) |
| → `in_review` | Todos los DoD deben estar `reported` mínimo |
| → `completed` | Todos los DoD deben estar `verified` |

---

## 8. ¿ES BLOQUEANTE?

| Tipo | ¿Bloquea? | Configuración |
|------|-----------|---------------|
| **DoR** | ✅ Sí (con override) | `dorBlockingEnabled: true` |
| **DoD** | ✅ Sí para `completed` | `dodBlockingEnabled: true` |
| **AC funcionales** | ❌ No por default | `acBlockingEnabled: false` |

---

## 9. RESPONSABLES

| Acción | PM | TL | SA | QA | Agente |
|--------|----|----|----|----|--------|
| Crear template global | ❌ | ❌ | ❌ | ❌ | ❌ (Admin) |
| Crear template proyecto | ✅ | ❌ | ✅ | ❌ | ❌ |
| Crear AC en tarea | ✅ | ✅ | ✅ | ✅ | ❌ |
| Reportar fulfillment | ✅ | ✅ | ❌ | ✅ | ✅ |
| Verificar fulfillment | ✅ | ✅ | ❌ | ✅ | ❌ |
| Desactivar criterio | ✅ | ✅ | ❌ | ❌ | ❌ |
| Deprecar AC | ✅ | ❌ | ✅ | ❌ | ❌ |

---

## 10. ENDPOINTS

### Templates

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/criteria-templates` | Listar templates |
| GET | `/api/criteria-templates?scope=global&projectTypeCode=software` | Filtrar |
| POST | `/api/criteria-templates` | Crear template |
| PATCH | `/api/criteria-templates/:id` | Actualizar template |
| DELETE | `/api/criteria-templates/:id` | Eliminar template |
| GET | `/api/criteria-templates/preview?projectId=X&taskTypeCode=backend` | Preview de herencia |

### Criterios de tarea

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/tasks/:taskId/criteria` | Listar criterios |
| POST | `/api/tasks/:taskId/criteria` | Crear criterio |
| POST | `/api/tasks/:taskId/criteria/bulk` | Crear múltiples |
| POST | `/api/tasks/:taskId/criteria/apply-templates` | Aplicar templates manualmente |
| PATCH | `/api/criteria/:id` | Actualizar criterio |
| DELETE | `/api/criteria/:id` | Eliminar criterio |

### Fulfillment

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/criteria/:id/fulfill` | Reportar cumplimiento |
| POST | `/api/criteria/:id/verify` | Verificar (TL/QA) |

### Reportes

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/tasks/:taskId/criteria/summary` | Resumen de criterios |
| GET | `/api/sprints/:sprintId/criteria-report` | Reporte del sprint |

---

## 11. CAMPOS DE TESTING (para QA)

Criterios tipo `functional` en tareas de testing tienen campos adicionales:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `testResult` | Enum | pass, fail, blocked, skipped |
| `executedAt` | DateTime | Cuándo se ejecutó |
| `executedBy` | UUID | Quién ejecutó |
| `evidence` | String | Link a screenshot, log, video |
| `defectId` | UUID | FK a bug si fail |
| `executionNotes` | String | Notas de ejecución |

---

## 12. TABLAS EN BASE DE DATOS

### criteria_template

```sql
CREATE TABLE criteria_template (
  id TEXT PRIMARY KEY,
  code VARCHAR(50) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  criteria_type_code VARCHAR(50) NOT NULL REFERENCES criteria_type_catalog(code),
  
  -- Scope
  scope VARCHAR(50) NOT NULL,  -- 'global' o 'project'
  project_type_code VARCHAR(50) REFERENCES project_type_catalog(code),
  project_id TEXT REFERENCES projects(id),
  task_type_code VARCHAR(50) REFERENCES task_type_catalog(code),
  
  -- Control
  is_required BOOLEAN DEFAULT true,
  is_active BOOLEAN DEFAULT true,
  sort_order INT DEFAULT 0,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  CONSTRAINT scope_check CHECK (
    (scope = 'global' AND project_type_code IS NOT NULL AND project_id IS NULL) OR
    (scope = 'project' AND project_id IS NOT NULL)
  ),
  UNIQUE(code, scope, COALESCE(project_type_code, ''), COALESCE(project_id::text, ''))
);
```

### criteria_template_history

```sql
CREATE TABLE criteria_template_history (
  id TEXT PRIMARY KEY,
  template_id TEXT NOT NULL REFERENCES criteria_template(id),
  previous_description TEXT,
  new_description TEXT,
  apply_to VARCHAR(50) NOT NULL,  -- 'new_only', 'pending', 'all_active'
  changed_by TEXT REFERENCES users(id),
  changed_at TIMESTAMP DEFAULT NOW(),
  reason TEXT
);
```

### acceptance_criteria (campos nuevos)

```sql
ALTER TABLE acceptance_criteria ADD COLUMN
  -- Q1: Desactivación
  is_applicable BOOLEAN DEFAULT true,
  disabled_reason TEXT,
  disabled_by TEXT REFERENCES users(id),
  
  -- Q3: Deprecación
  ac_status VARCHAR(50) DEFAULT 'active',
  superseded_by TEXT REFERENCES acceptance_criteria(id),
  
  -- Q5: Fulfillment dual
  fulfillment_status VARCHAR(50) DEFAULT 'pending',
  reported_by TEXT REFERENCES users(id),
  reported_at TIMESTAMP,
  report_evidence TEXT,
  verified_by TEXT REFERENCES users(id),
  verified_at TIMESTAMP,
  verification_comment TEXT,
  rejection_reason TEXT,
  
  -- Q6: Testing
  test_result VARCHAR(50),
  executed_at TIMESTAMP,
  executed_by TEXT REFERENCES users(id),
  evidence TEXT,
  defect_id TEXT REFERENCES trackable_items(id),
  execution_notes TEXT,
  
  -- Trazabilidad
  source_template_id TEXT REFERENCES criteria_template(id);
```

---

## 13. CONFIGURACIÓN

### Por proyecto

```json
{
  "criteriaConfig": {
    "enabled": true,
    "dorBlockingEnabled": true,
    "dorAllowOverride": true,
    "dodBlockingEnabled": true,
    "dodRequireVerification": true,
    "acBlockingEnabled": false,
    "autoApplyTemplates": true,
    "autoGenerateCode": true,
    "codePrefix": "CA"
  }
}
```

---

## 14. ERRORES COMUNES

| Error | Causa | Solución |
|-------|-------|----------|
| "DOR_NOT_MET" | Hay DoR pending al iniciar | Cumplir DoR o usar overrideReason |
| "DOD_NOT_VERIFIED" | Hay DoD sin verificar al completar | TL debe verificar |
| "CRITERIA_DEPRECATED" | Intentas fulfillment en criterio deprecated | Usa el criterio que lo reemplaza |
| "CANNOT_DISABLE" | Solo PM/TL pueden desactivar | Pide a PM/TL |

---

## 15. FAQ

**¿Puedo agregar criterios después de iniciar la tarea?**
Sí. AC se pueden agregar en cualquier momento excepto cuando la tarea está completed.

**¿Qué pasa si cambio el taskTypeCode?**
Se recalculan los templates. Los criterios anteriores se marcan como "orphaned" pero no se eliminan.

**¿El agente puede marcar DoD como verified?**
No. El agente solo puede reportar. La verificación es de TL/QA.

**¿Puedo saltar el DoR?**
Sí, con override y justificación obligatoria. Queda registrado.

**¿Los templates se pueden versionar?**
Sí. Cada cambio queda en `criteria_template_history` con before/after.

---

**Documento:** FEATURE_CRITERIOS_ACEPTACION.md  
**Versión:** 2.0  
**Fecha:** 2026-05-06
