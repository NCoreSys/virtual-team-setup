# INSTRUCCIONES TL: Uso de APIs V4 para Proyecto Nuevo

| Campo | Valor |
|-------|-------|
| **Documento** | INSTRUCCIONES_TL_USO_APIS_V4_SIN_UI.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-04 |
| **De** | PM (Martin Rivas) |
| **Para** | TL del proyecto nuevo (R3) |
| **Contexto** | Las APIs V4 están funcionando y testeadas. No hay UI integrada aún. Este documento indica cómo usar las APIs directamente. |

---

## 1. SITUACIÓN ACTUAL

```
╔═══════════════════════════════════════════════════════════════════════════╗
║ APIs V4: ✅ Funcionando y testeadas (S01-S10 aprobados)                   ║
║ UI V4:   ⬜ Pendiente integración (S12 en desarrollo paralelo)            ║
║                                                                           ║
║ Mientras S12 se desarrolla, el proyecto nuevo puede usar las APIs        ║
║ directamente para registrar toda la trazabilidad.                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 2. CÓMO REGISTRAR EL PROYECTO NUEVO

### 2.1 Crear Release

```bash
POST /api/projects/{VTT_PROJECT_ID}/releases
Content-Type: application/json

{
  "code": "R3",
  "name": "Métricas, Planning y Costos",
  "status": "release_planned",
  "startDate": "2026-04-04"
}
```

**Response:** Guardar el `releaseId` para los siguientes pasos.

---

### 2.2 Crear Sprints

```bash
POST /api/releases/{releaseId}/sprints
Content-Type: application/json

# Sprint P0-ACTN
{
  "code": "P0-ACTN",
  "name": "Fundamentos",
  "order": 1,
  "status": "sprint_planned"
}

# Sprint P1-PLANNING
{
  "code": "P1-PLANNING",
  "name": "Planning V2",
  "order": 2,
  "status": "sprint_planned"
}

# Sprint P2-METRICAS
{
  "code": "P2-METRICAS",
  "name": "Métricas",
  "order": 3,
  "status": "sprint_planned"
}

# Sprint P3-COSTOS
{
  "code": "P3-COSTOS",
  "name": "Costos/Tokens",
  "order": 4,
  "status": "sprint_planned"
}

# Sprint P4-SETTINGS
{
  "code": "P4-SETTINGS",
  "name": "Settings Proyecto",
  "order": 5,
  "status": "sprint_planned"
}

# Sprint P5-DASHBOARD
{
  "code": "P5-DASHBOARD",
  "name": "Dashboard UX",
  "order": 6,
  "status": "sprint_planned"
}
```

---

### 2.3 Crear Deliverables por Sprint

```bash
POST /api/sprints/{sprintId}/deliveries
Content-Type: application/json

# Ejemplo para P0-ACTN
{
  "code": "D0.1",
  "name": "Análisis del Algoritmo ACTN",
  "phaseCode": "01-analysis",
  "status": "delivery_planned"
}
```

**Deliverables completos por sprint:** Ver SETUP_TEORICO_R3_METRICAS_PLANNING_COSTOS.md

---

## 3. CÓMO REGISTRAR REQUERIMIENTOS (TRACKABLE ITEMS)

### 3.1 Crear Requerimiento Funcional

```bash
POST /api/projects/{projectId}/trackable-items
Content-Type: application/json

{
  "code": "RF-R3-001",
  "typeCode": "RF",
  "title": "El sistema debe calcular actualHours correctamente",
  "description": "Corregir algoritmo ACTN para excluir tiempo en review, on_hold, overnight",
  "status": "trackable_draft"
}
```

### 3.2 Tipos disponibles (trackable_type_catalog)

| typeCode | Uso |
|----------|-----|
| `RF` | Requerimiento Funcional |
| `RNF` | Requerimiento No Funcional |
| `ADR` | Decisión Arquitectónica |
| `UC` | Caso de Uso |
| `KPI` | Indicador de Negocio |

---

## 4. CÓMO VINCULAR REQUERIMIENTOS A TAREAS

### 4.1 Vincular RF a Tarea

```bash
POST /api/trackable-items/{trackableItemId}/tasks
Content-Type: application/json

{
  "taskId": "{taskId}"
}
```

### 4.2 Consultar tareas de un RF

```bash
GET /api/trackable-items/{trackableItemId}/tasks
```

---

## 5. CÓMO REGISTRAR CRITERIOS DE ACEPTACIÓN

### 5.1 Crear Criterio

```bash
POST /api/projects/{projectId}/acceptance-criteria
Content-Type: application/json

{
  "typeCode": "acceptance",
  "description": "El algoritmo debe excluir tiempo en status task_in_review del cálculo de actualHours",
  "status": "criteria_draft"
}
```

### 5.2 Vincular Criterio a Trackable Item

```bash
POST /api/acceptance-criteria/{criteriaId}/trackables
Content-Type: application/json

{
  "trackableItemId": "{trackableItemId}"
}
```

### 5.3 Asignar Criterio a Tarea

```bash
POST /api/tasks/{taskId}/criteria/{criteriaId}/assign
```

---

## 6. CÓMO REPORTAR CUMPLIMIENTO

### 6.1 Agente Reporta Fulfillment

```bash
POST /api/tasks/{taskId}/criteria/{criteriaId}/fulfill
Content-Type: application/json

{
  "status": "met",
  "evidence": "Ver commit abc123 donde se implementó la exclusión de task_in_review"
}
```

### 6.2 Estados de Fulfillment

| status | Descripción |
|--------|-------------|
| `pending` | Asignado, no evaluado |
| `met` | Cumplido |
| `not_met` | No cumplido |
| `partial` | Parcialmente cumplido |
| `deferred` | Diferido a otro sprint |

---

## 7. CÓMO REGISTRAR DEVLOG ENTRIES

### 7.1 Agente Reporta Issues/Decisiones/Deuda

```bash
POST /api/tasks/{taskId}/devlog-entries
Content-Type: application/json

{
  "entries": [
    {
      "categoryCode": "issue",
      "severity": "high",
      "title": "Inconsistencia en cálculo de overnight",
      "description": "El servicio actual no considera zona horaria del proyecto"
    },
    {
      "categoryCode": "decision",
      "severity": "medium",
      "title": "Usar UTC para todos los cálculos",
      "description": "Se decidió normalizar a UTC para evitar problemas de timezone"
    },
    {
      "categoryCode": "tech_debt",
      "severity": "low",
      "title": "Refactorizar TimeService",
      "description": "El servicio tiene demasiadas responsabilidades"
    }
  ]
}
```

### 7.2 Categorías disponibles (devlog_category_catalog)

| categoryCode | Uso | severityLevels |
|--------------|-----|----------------|
| `issue` | Issue encontrado | critical, high, medium, low |
| `tech_debt` | Deuda técnica | high, medium, low |
| `decision` | Decisión tomada | — |
| `testing_note` | Nota de QA | medium, low |
| `blocker` | Bloqueador | critical, high |
| `risk` | Riesgo identificado | critical, high, medium |

---

## 8. CÓMO CONSULTAR GATE DE DEVLOG

### 8.1 Verificar si Sprint puede avanzar a QA

```bash
GET /api/sprints/{sprintId}/devlog-review
```

**Response:**

```json
{
  "canProceed": false,
  "pendingCritical": 1,
  "pendingHigh": 2,
  "entries": [
    {
      "id": "...",
      "categoryCode": "issue",
      "severity": "critical",
      "title": "...",
      "status": "pending"
    }
  ]
}
```

### 8.2 Resolver Entry para Desbloquear

```bash
PATCH /api/devlog-entries/{entryId}
Content-Type: application/json

# Opción A: Crear tarea para resolver
{
  "status": "in_progress",
  "fixTaskId": "{newTaskId}"
}

# Opción B: Diferir a siguiente sprint
{
  "status": "deferred",
  "deferredToSprintId": "{nextSprintId}"
}

# Opción C: Marcar como no aplica
{
  "status": "wont_fix",
  "resolution": "No aplica porque..."
}
```

---

## 9. CÓMO REGISTRAR DOCUMENTOS

### 9.1 Crear Documento de Proyecto

```bash
POST /api/projects/{projectId}/documents
Content-Type: application/json

{
  "name": "SPEC_ACTN_ALGORITMO_V1.md",
  "type": "specification",
  "folderId": "{folderId}",
  "isLivingDocument": false,
  "changeControl": "controlled"
}
```

### 9.2 Marcar Impacto de Tarea en Documento

```bash
POST /api/tasks/{taskId}/document-impacts
Content-Type: application/json

{
  "projectDocumentId": "{documentId}",
  "impactType": "update"
}
```

### 9.3 Completar Impacto

```bash
POST /api/tasks/{taskId}/document-impacts/{documentId}/complete
Content-Type: application/json

{
  "status": "updated"
}
```

---

## 10. CÓMO REGISTRAR FIRMAS

### 10.1 Firmar Stage (Fase)

```bash
POST /api/phases/{phaseId}/approvals
Content-Type: application/json

{
  "role": "TL",
  "status": "approved",
  "comments": "Implementación completa, tests passing"
}
```

### 10.2 Firmar Sprint

```bash
POST /api/sprints/{sprintId}/approvals
Content-Type: application/json

{
  "role": "AR",
  "status": "approved",
  "comments": "Arquitectura validada"
}
```

### 10.3 Firmar Release

```bash
POST /api/releases/{releaseId}/approvals
Content-Type: application/json

{
  "role": "PM",
  "status": "approved",
  "comments": "Release aprobado para producción"
}
```

---

## 11. FLUJO COMPLETO RECOMENDADO

```
1. SETUP INICIAL (una vez por release)
   ├── Crear Release (POST /releases)
   ├── Crear Sprints (POST /sprints)
   └── Crear Deliverables (POST /deliveries)

2. ANÁLISIS (por cada sprint)
   ├── Crear Trackable Items (POST /trackable-items)
   ├── Crear Acceptance Criteria (POST /acceptance-criteria)
   └── Vincular Criteria a Items (POST /criteria/:id/trackables)

3. PLANNING (por cada tarea)
   ├── Crear Task (existente)
   ├── Vincular a Trackable Item (POST /trackable-items/:id/tasks)
   ├── Asignar Criteria a Task (POST /tasks/:id/criteria/:id/assign)
   └── Registrar Document Impacts (POST /tasks/:id/document-impacts)

4. EJECUCIÓN (durante desarrollo)
   ├── Reportar Fulfillment (POST /tasks/:id/criteria/:id/fulfill)
   ├── Reportar Devlog Entries (POST /tasks/:id/devlog-entries)
   └── Completar Document Impacts (POST /document-impacts/:id/complete)

5. REVIEW (antes de QA)
   ├── Consultar Gate (GET /sprints/:id/devlog-review)
   ├── Resolver entries critical/high
   └── Verificar canProceed: true

6. CIERRE (por nivel)
   ├── Firmar Stages (POST /phases/:id/approvals)
   ├── Firmar Sprint (POST /sprints/:id/approvals)
   └── Firmar Release (POST /releases/:id/approvals)
```

---

## 12. QUERIES ÚTILES

### Ver estado de trazabilidad de un RF

```bash
GET /api/trackable-items/{id}?include=tasks,criteria,fulfillments
```

### Ver cobertura de criterios del proyecto

```bash
GET /api/projects/{id}/criteria-coverage
```

### Ver resumen de cumplimiento del sprint

```bash
GET /api/sprints/{id}/fulfillment-summary
```

### Ver reporte de trazabilidad completo

```bash
GET /api/projects/{id}/traceability-report
```

---

## 13. NOTAS IMPORTANTES

1. **Todos los endpoints requieren JWT** — Autenticarse primero
2. **Los IDs son UUIDs** — Guardar los IDs que retornan los POST
3. **Los catálogos ya tienen seeds** — Usar los codes existentes (RF, ADR, acceptance, issue, etc.)
4. **El gate de devlog bloquea** — Resolver critical/high antes de transitionToQA
5. **Las firmas son en cascada** — Stage → Sprint → Release

---

**Documento:** INSTRUCCIONES_TL_USO_APIS_V4_SIN_UI.md  
**Versión:** 1.0  
**Estado:** ✅ Listo para uso  
**Fecha:** 2026-04-04

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
