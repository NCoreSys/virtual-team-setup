# Guía de Agentes: Modelo Dinámico de Gestión de Proyectos V4

**Versión:** 2.0
**Fecha:** 2026-04-27
**Elaborado por:** Technical Research Engineer
**Fuentes verificadas:** R3 (Handoffs S01–S12) + R4 (Catálogos V4 consolidados) + schema.prisma (73 modelos)
**Propósito:** Referencia completa para que cualquier agente pueda usar el Modelo Dinámico V4 sin preguntar.

---

## POR QUÉ EXISTE ESTE DOCUMENTO

Los agentes encuentran errores al usar el Modelo Dinámico V4 porque:
1. No saben qué catálogos necesitan seed antes de usarse
2. Confunden sistemas distintos (devlog entries vs. trackable items, releases vs. sprints)
3. Usan `categoryCode` o paths de endpoint incorrectos
4. No conocen el Gate de Revisión (D-41) que bloquea `task_in_review`
5. No tienen un mapa de qué endpoints existen

Este documento consolida **TODO** lo que necesitas saber, organizado por módulo funcional.

---

## MAPA DEL SISTEMA V4 — 13 SPRINTS, 4 BLOQUES

```
BLOQUE 1: Técnico Base (S01–S08)
├── S01  Catálogos base (project-types, phases, deliverables, trackable-types)
├── S02  Flow Templates (templates reutilizables de flujo de proyecto)
├── S03  Releases + Sprints (jerarquía temporal del proyecto)
├── S04  Trackable Items (RFs, ADRs, bugs, user stories trazables)
├── S04B Deferred Scope (diferir items a fase/sprint/release futuro)
├── S05  Project Folders (árbol de carpetas + sync BD→FS)
├── S06  Living Docs + Document Index (docs dinámicos + búsqueda)
├── S07  Compliance Checks (validaciones automáticas/manuales)
└── S08  Firmas + Findings + Anti-Hardcode (aprobaciones en cascada)

BLOQUE 2: Trazabilidad (S09–S10)
├── S09  Catálogos de trazabilidad + Links + Acceptance Criteria
└── S10  Fulfillment + Devlog Entries + Document Sources + Reports

BLOQUE 3: Gestión de Proyectos (S11)
└── S11  Wizard crear proyecto + Settings post-creación

BLOQUE 4: Integración UX (S12)
└── S12  Devlog Entry Status + Gate 422 + 53 pantallas FE
```

> **NOTA CRÍTICA:** Los modelos Prisma de TODOS los bloques existen en `backend/prisma/schema.prisma` (73 modelos). El Bloque 1 está implementado en código aunque sus handoffs de documentación formal estén en `Sprint01_08/`.

---

## SECCIÓN 1: CATÁLOGOS — LO PRIMERO QUE DEBES SABER

### 1.1 Estado de catálogos en producción

| Catálogo | Tabla | Estado | ¿Qué hacer? |
|----------|-------|--------|-------------|
| Status de tareas | `status_catalog` | ✅ Datos | Usar directo |
| Prioridades | `priority_catalog` | ✅ Datos | Usar directo |
| Tipos de entidad | `entity_type_catalog` | ✅ Datos | Usar directo |
| Tipos de documento | `document_type_catalog` | ✅ Datos | Usar directo |
| Tipos de archivo | `file_type_catalog` | ✅ Datos | Usar directo |
| Tipos de proyecto | `project_type_catalog` | ✅ Datos | Ver sección 3 |
| Tipos trazables | `trackable_type_catalog` | ✅ Datos | Ver sección 6 |
| **Categorías Devlog** | `devlog_category_catalog` | ⚠️ Requiere seed | Ver 1.2 |
| **Tipos de Criterio** | `criteria_type_catalog` | ⚠️ Requiere seed | Ver 1.2 |
| **Tipos de Link** | `link_type_catalog` | ⚠️ Requiere seed | Ver 1.2 |
| **Fuentes Living Doc** | `living_doc_source_catalog` | ⚠️ Requiere seed | Ver 1.2 |

**API de catálogos:**
```
GET /api/catalogs/project-types
GET /api/catalogs/trackable-types
GET /api/catalogs/criteria-types
GET /api/catalogs/devlog-categories
GET /api/catalogs/link-types
GET /api/catalogs/living-doc-sources
GET /api/catalogs/phases
GET /api/catalogs/deliverables
```

### 1.2 Valores válidos — catálogos que requieren seed

#### devlog_category_catalog

| code | ¿Tiene severity? | Cuándo usar |
|------|-----------------|-------------|
| `issue` | critical/high/medium/low | Inconsistencia detectada (NO bug formal) |
| `tech_debt` | critical/high/medium/low | Deuda técnica |
| `decision` | ninguno | Decisión técnica tomada |
| `blocker` | critical/high/medium/low | Algo bloquea tu avance |
| `risk` | critical/high/medium/low | Riesgo identificado |
| `testing_note` | critical/high/medium/low | Resultado de test |
| `observation` | ninguno | Observación general |
| `question` | high/medium/low | Pregunta pendiente |
| `dependency` | high/medium | Dependencia entre tareas/sistemas |
| `improvement` | medium/low | Mejora para iteración futura |
| `feedback` | high/medium/low | Feedback de stakeholder |
| `brand_issue` | critical/high/medium | Issue de marca/diseño |

> ⚠️ `"improvement"` es válido en el seed consolidado (VTT-341+VTT-680). La spec V4 original tenía solo 6 categorías — el seed consolidado tiene 12.

#### criteria_type_catalog

**Tipos de framework/proceso:** `acceptance`, `dod`, `dor`, `quality_gate`, `launch_criteria`, `brand_compliance`, `legal_approval`

**Tipos de dominio técnico:** `functional`, `technical`, `ux`, `security`, `performance`, `accessibility`, `integration`

#### link_type_catalog

`implements`, `depends_on`, `related_to`, `blocks`, `relates_to`, `supports`, `derives_from`, `parent_of`, `child_of`, `duplicates`, `supersedes`

> `relates_to` ≠ `related_to` — son códigos distintos con semántica diferente.

---

## SECCIÓN 2: AUTENTICACIÓN

```python
import urllib.request, json

req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({
        'userId': 'UUID_DEL_AGENTE',
        'serviceKey': 'SERVICE_KEY_VALOR'
    }).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req) as r:
    token = json.loads(r.read())['data']['token']
```

> Token válido 30 días. Usar en header: `Authorization: Bearer TOKEN`

---

## SECCIÓN 3: PROYECTOS DINÁMICOS (S01 + S11)

### Crear proyecto — payload atómico (recomendado)

```
POST /api/projects
Authorization: Bearer JWT
X-Organization-Id: UUID_ORG

Body:
{
  "name": "Mi Proyecto",
  "key": "MP",
  "methodology": "scrum",
  "projectTypeCode": "SOFTWARE",
  "sprintEnabled": true,
  "sprintDurationWeeks": 2,
  "startDate": "2026-04-17T00:00:00.000Z",
  "endDate": "2026-06-30T00:00:00.000Z",
  "createdBy": "UUID_AGENTE",
  "phases": [
    { "id": "local-p1", "name": "Planning", "order": 1 },
    { "id": "local-p2", "name": "Development", "order": 2 }
  ],
  "deliverables": [
    { "name": "Plan", "phaseId": "local-p1", "isIncluded": true }
  ]
}
```

Restricciones:
- `key`: solo mayúsculas, 2–6 chars
- `methodology`: `scrum` | `kanban` | `waterfall` | `custom`
- `projectTypeCode`: `SOFTWARE` | `MARKETING` | `RESEARCH` | `CONSULTING` | `CUSTOM`
- `startDate`/`endDate`: ISO 8601 con offset (NO solo `YYYY-MM-DD`)
- `phases[].id`: ID local solo para mapear deliverables en la misma llamada
- `createdBy` en deliverables: UUID obligatorio

### Configuración del proyecto

```
GET   /api/projects/:id/configuration
PATCH /api/projects/:id/configuration
Body: { "methodology": "kanban", "settings": { "allowParallelPhases": true, "requireCriteriaBeforeClose": true, "defaultTaskComplexity": "medium" } }
```

> ⚠️ `sprintEnabled`/`sprintDurationWeeks` NO se pueden cambiar vía PATCH después de creación (Zod los descarta).

### Fases

```
GET    /api/projects/:projectId/phases
POST   /api/projects/:projectId/phases     { "name": "Discovery", "order": 1 }
PATCH  /api/projects/:id/phases/:phaseId   { "name": "..." }
DELETE /api/projects/:id/phases/:phaseId
PATCH  /api/projects/:id/phases/reorder    { "phaseIds": ["UUID1","UUID2"] }
```

> ⚠️ El body de reorder usa `"phaseIds"` (NO `"orderedPhaseIds"` que envía el FE — el BE rechaza ese campo).

### Deliverables de fase

```
POST   /api/projects/:id/phases/:phaseId/deliverables
Body: { "name": "Doc arq.", "order": 1, "createdBy": "UUID_AGENTE" }   ← createdBy OBLIGATORIO

DELETE /api/projects/:id/phases/:phaseId/deliverables/:deliverableId
```

---

## SECCIÓN 4: FLOW TEMPLATES (S02)

Templates reutilizables que definen la estructura de fases y deliverables. Se pueden aplicar al crear un proyecto.

```
GET /api/flow-templates
GET /api/flow-templates/:id
GET /api/flow-templates/:id/phases
GET /api/flow-templates/:id/phases/:phaseCode/deliverables
```

---

## SECCIÓN 5: RELEASES Y SPRINTS (S03)

### Jerarquía temporal

```
Proyecto
  └── Release (MVP, V2, V3...)
        └── Sprint (opcional, según metodología)
```

### Releases

```
GET    /api/projects/:projectId/releases
POST   /api/projects/:projectId/releases   { "name": "MVP", "startDate": "...", "endDate": "..." }
GET    /api/releases/:id
PATCH  /api/releases/:id
DELETE /api/releases/:id
```

### Sprints

```
GET    /api/releases/:releaseId/sprints
POST   /api/releases/:releaseId/sprints    { "name": "S01", "startDate": "...", "endDate": "..." }
GET    /api/sprints/:id
PATCH  /api/sprints/:id
DELETE /api/sprints/:id
```

> Nota: En endpoints de devlog-summary/review, "sprint" se materializa como `Phase` en VTT. Ejemplo: `GET /api/phases/:id/devlog-summary` (NO `/api/sprints/:sprintId/devlog-summary`).

---

## SECCIÓN 6: TRACKABLE ITEMS (S04)

Items trazables formales del proyecto: Requisitos Funcionales (RF), ADRs, User Stories, Bugs formales, KPIs.

> **No confundir con TaskDevlogEntry** (log de trabajo de una tarea). Los TrackableItems son entidades de primer nivel del proyecto.

### CRUD de items

```
GET    /api/projects/:projectId/trackable-items
POST   /api/projects/:projectId/trackable-items
Body: {
  "typeCode": "RF",          ← código del trackable_type_catalog
  "title": "...",
  "description": "...",
  "priority": "high"
}

GET    /api/trackable-items/:id
PATCH  /api/trackable-items/:id
DELETE /api/trackable-items/:id
```

### Vincular tareas a un item

```
POST   /api/trackable-items/:id/tasks       { "taskId": "VTT-XXX" }
DELETE /api/trackable-items/:id/tasks/:taskId
```

### Evidencias

```
POST   /api/trackable-items/:id/evidence    { "type": "screenshot", "url": "..." }
GET    /api/trackable-items/:id/evidence
```

---

## SECCIÓN 7: DEFERRED SCOPE (S04-B)

Mecanismo formal para diferir un TrackableItem que no se puede resolver en el sprint/fase actual.

> Esto es distinto a diferir un **devlog entry** (ver Sección 10.5). TrackableItem defer = compromiso formal de proyecto. Devlog entry defer = nota de trabajo individual.

### Diferir un item

```
POST /api/trackable-items/:id/defer
Body: {
  "reason": "No hay capacidad en este sprint",
  "targetType": "phase",     ← "phase" | "sprint" | "release"
  "targetPhaseId": "UUID_FASE_DESTINO"
}
```

### Gestionar diferimientos

```
PATCH  /api/deferrals/:id/schedule    { "targetType": "sprint", "targetSprintId": "UUID" }
PATCH  /api/deferrals/:id/cancel
GET    /api/projects/:id/deferrals
```

### Verificar si una fase puede cerrarse

```
GET /api/phases/:id/can-close
```

Retorna `canClose: false` si hay TrackableItems sin resolver o diferir.

---

## SECCIÓN 8: PROJECT FOLDERS (S05)

Sistema de carpetas jerárquicas para organizar artefactos del proyecto.

```
GET    /api/projects/:projectId/folders      ← retorna árbol completo
POST   /api/projects/:projectId/folders      { "name": "docs", "parentId": "UUID_PADRE" }
GET    /api/project-folders/:id
PATCH  /api/project-folders/:id
DELETE /api/project-folders/:id
POST   /api/project-folders/:id/move         { "newParentId": "UUID" }
POST   /api/projects/:id/sync-filesystem     ← sincroniza árbol BD → FS
```

> Las carpetas sistema (`briefs/`, `assignments/`, `devlogs/`, etc.) se crean automáticamente al crear el proyecto (`createSystemFolders`).

---

## SECCIÓN 9: LIVING DOCS + DOCUMENT INDEX (S06)

### Living Documents — documentos que se auto-actualizan

```
GET   /api/living-docs                     ← listar configs
GET   /api/living-docs/:type/regenerate    ← regenerar (async 202)
POST  /api/living-docs/:type/regenerate    ← forzar regeneración
PATCH /api/living-docs/:type               ← actualizar config
```

> Las regeneraciones retornan `202 Accepted` con header `Location` para polling — son asíncronas.

### Document Sources (multi-fuente)

```
POST   /api/project-documents/:id/sources
Body: { "sourceCode": "prisma_schema", "config": { "filePath": "prisma/schema.prisma" } }

GET    /api/project-documents/:id/sources
DELETE /api/project-documents/:id/sources/:sourceCode
```

Fuentes disponibles (requieren seed): `prisma_schema`, `swagger_openapi`, `typescript_types`, `env_template`, `package_json`, `db_query`

### Búsqueda y reindexado

```
GET   /api/projects/:id/documents/search?q=texto
POST  /api/projects/:id/reindex
PATCH /api/project-documents/:id
```

---

## SECCIÓN 10: DEVLOG ENTRIES + GATE DE REVISIÓN (S10 + S12)

### 10.1 Mapa rápido

```
TaskDevlogEntry = log de trabajo de UNA TAREA específica
  ↳ POST /api/tasks/:id/devlog-entries

TrackableItemDeferral = diferir un RF/ADR/KPI formal
  ↳ POST /api/trackable-items/:id/defer
```

### 10.2 Crear entries

```
POST /api/tasks/:taskId/devlog-entries
Body (individual o batch):
{
  "categoryCode": "decision",
  "severity": null,
  "title": "Usar UUID en lugar de auto-increment",
  "description": "Por consistencia con el sistema",
  "reportedBy": "UUID_AGENTE"
}

// O en batch (máx 50):
{
  "entries": [
    { "categoryCode": "blocker", "severity": "high", "title": "...", "reportedBy": "UUID" },
    { "categoryCode": "decision", "severity": null, "title": "...", "reportedBy": "UUID" }
  ]
}
```

`severity` es `null` para categorías sin severity (`decision`, `observation`).

### 10.3 Consultar entries

```
GET /api/tasks/:taskId/devlog-entries
GET /api/tasks/:taskId/devlog-entries?status=pending
GET /api/tasks/:taskId/devlog-entries?severity=critical,high&status=pending
```

### 10.4 Estados de un entry

| Estado | ¿Final? |
|--------|---------|
| `pending` | No |
| `acknowledged` | No |
| `in_progress` | No |
| `resolved` | ✅ Sí |
| `deferred` | ✅ Sí |
| `wont_fix` | ✅ Sí |

Un entry en estado final **no puede cambiar** — error si intentas modificarlo.

### 10.5 Cambiar estado de un entry

```
PATCH /api/tasks/:taskId/devlog/:entryId/status

// Resolver (requiere resolution):
{ "status": "resolved", "resolution": "Migración ejecutada por DevOps" }

// Diferir (requiere deferredToPhaseId):
{ "status": "deferred", "deferredToPhaseId": "UUID_PHASE" }

// No corregir (requiere resolution):
{ "status": "wont_fix", "resolution": "No aplica por decisión de alcance" }

// Alternativa para diferir:
PATCH /api/devlog-entries/:id/defer
{ "deferredToPhaseId": "UUID_FASE_FUTURA" }
```

### 10.6 Crear fix task desde un entry

```
POST /api/devlog-entries/:id/create-fix-task
{ "title": "Fix: Refactorizar TimeService", "assignedToId": "UUID_USUARIO" }
```

El entry queda con `fixTaskId` apuntando a la nueva tarea.

### 10.7 Gate de revisión (D-41) — CRÍTICO

**El gate bloquea `task_in_review` con 422 si hay entries `severity=critical|high` y `status=pending`.**

```
// Verificar ANTES de mover a in_review:
GET /api/tasks/:taskId/review-gate

Response:
{
  "data": {
    "canProceedToReview": false,
    "blockers": [...],
    "warnings": [...],
    "summary": {
      "total": 3,
      "byStatus": { "pending": 1, "resolved": 2 },
      "bySeverity": { "critical": 1, "high": 0, "medium": 2 }
    }
  }
}
```

Error si intentas mover con blockers:
```json
{ "code": "DEVLOG_GATE_BLOCKED", "message": "Cannot move task to review: it has N devlog blocker(s)...", "details": { "blockers": [...] } }
```

### Flujo correcto antes de in_review

```
1. GET /api/tasks/:taskId/review-gate
   → si canProceedToReview = false → resolver blockers

2. Por cada blocker:
   PATCH /api/tasks/:taskId/devlog/:entryId/status
   { "status": "resolved", "resolution": "Cómo lo resolví" }

3. Re-verificar hasta canProceedToReview = true

4. PATCH /api/tasks/:taskId/status
   { "statusId": "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d", "changedBy": "UUID_AGENTE" }
```

### Resumen por fase/sprint

```
GET /api/phases/:id/devlog-summary      ← "sprint" en VTT = Phase
GET /api/phases/:id/devlog-review       ← gate por fase
```

---

## SECCIÓN 11: TRAZABILIDAD — LINKS Y CRITERIOS (S09 + S10)

### Links entre TrackableItems

```
POST   /api/trackable-items/:id/links
Body: { "targetId": "UUID_ITEM", "linkTypeCode": "depends_on" }

GET    /api/trackable-items/:id/links
DELETE /api/trackable-items/:id/links/:linkId
```

### Links entre Tareas

```
POST   /api/tasks/:parentId/links
Body: { "childId": "UUID_TAREA", "linkTypeCode": "implements" }

GET    /api/tasks/:id/links
DELETE /api/task-links/:id
```

### Criterios de aceptación (solo PM/TL pueden crear — D-33)

```
POST   /api/projects/:id/acceptance-criteria
Body: {
  "criteriaTypeCode": "functional",
  "title": "Usuario puede registrarse con email",
  "description": "POST /users acepta email válido"
}

GET    /api/projects/:id/acceptance-criteria
GET    /api/acceptance-criteria/:id
```

### Criterios por tarea

```
GET  /api/tasks/:id/criteria
```

### Reportar cumplimiento (agente)

```
POST   /api/tasks/:id/criteria/:criteriaId/fulfill
Body: {
  "status": "met",          ← "pending" | "met" | "not_met" | "partial" | "deferred"
  "evidence": "Commit abc123",
  "notes": "Verificado manualmente"
}

PATCH  /api/tasks/:id/criteria/:criteriaId   ← actualizar fulfillment
GET    /api/tasks/:id/criteria-fulfillments
```

### Reportes de trazabilidad

```
GET /api/projects/:id/traceability-report    ← RF→Task completo
GET /api/projects/:id/criteria-coverage      ← cobertura criterios
GET /api/sprints/:id/fulfillment-summary     ← resumen cumplimiento
```

---

## SECCIÓN 12: DOCUMENT IMPACTS (S10)

Registrar qué documentos impacta una tarea durante su ejecución.

```
POST   /api/tasks/:id/document-impacts
Body: {
  "documentSourceId": "UUID",
  "impactType": "modified",   ← "added" | "modified" | "removed" | "referenced"
  "description": "Agregué nuevo endpoint al schema"
}

GET    /api/tasks/:id/document-impacts
POST   /api/tasks/:id/document-impacts/:docId/complete   ← reportar que se actualizó
```

---

## SECCIÓN 13: COMPLIANCE CHECKS (S07)

Verificaciones automáticas y manuales de cumplimiento.

```
GET    /api/projects/:projectId/compliance-checks
POST   /api/projects/:projectId/compliance-checks
Body: {
  "name": "JWT en todas las rutas",
  "type": "automatic",        ← "automatic" | "manual" | "hybrid"
  "scope": "sprint",          ← "task" | "sprint" | "release" | "project"
  "pattern": "/api/(?!auth)"
}

GET    /api/compliance-checks/:id
PATCH  /api/compliance-checks/:id
DELETE /api/compliance-checks/:id
POST   /api/compliance-checks/:id/execute
GET    /api/compliance-checks/:id/results
GET    /api/sprints/:id/compliance
```

---

## SECCIÓN 14: FIRMAS Y APROBACIONES (S08)

Sistema de firmas en cascada: Stage → Sprint → Release.

> Findings con `severity=critical|high` bloquean el cierre.

### Firmas por etapa (Stage)

```
GET  /api/sprints/:id/stages/:phaseCode/approvals
POST /api/sprints/:id/stages/:phaseCode/sign
Body: { "userId": "UUID", "role": "tech_lead", "comment": "Aprobado" }
```

### Firmas de Sprint

```
GET  /api/sprints/:id/approvals
POST /api/sprints/:id/sign      { "userId": "UUID", "comment": "Sprint cerrado" }
POST /api/sprints/:id/reject    { "userId": "UUID", "reason": "Hay findings pendientes" }
```

### Firmas de Release

```
GET  /api/releases/:id/approvals
POST /api/releases/:id/sign     { "userId": "UUID", "comment": "Release aprobado" }
```

### Mis aprobaciones pendientes

```
GET /api/approvals/pending
```

---

## SECCIÓN 15: FINDINGS Y ANTI-HARDCODE (S08)

### Findings estructurados

```
GET    /api/tasks/:id/findings
POST   /api/tasks/:id/findings
Body: {
  "type": "tech_debt",     ← "issue" | "tech_debt" | "decision" | "hardcode"
  "severity": "high",
  "title": "...",
  "description": "..."
}
PATCH  /api/tasks/:id/findings/:findingId

GET    /api/sprints/:id/findings
GET    /api/sprints/:id/tech-debt
GET    /api/sprints/:id/decisions
```

### Anti-Hardcode

```
GET  /api/hardcode-patterns
POST /api/hardcode-patterns         { "pattern": "localhost", "severity": "high" }
GET  /api/tasks/:id/hardcode-check
POST /api/tasks/:id/hardcode-check
POST /api/tasks/:id/hardcode-check/:patternId/false-positive
```

---

## SECCIÓN 16: FLUJO COMPLETO DE UNA TAREA CON V4

```
1. Mover a in_progress:
   PATCH /api/tasks/VTT-XXX/status { statusId: "2a76888a...", changedBy: "UUID" }

2. Durante trabajo — registrar observaciones:
   POST /api/tasks/VTT-XXX/devlog-entries
   { "categoryCode": "decision", "title": "...", "reportedBy": "UUID" }

3. Si encuentras blocker crítico/high:
   POST /api/tasks/VTT-XXX/devlog-entries
   { "categoryCode": "blocker", "severity": "high", "title": "...", "reportedBy": "UUID" }
   → DEBES resolverlo ANTES de ir a in_review

4. Reportar cumplimiento de criterios:
   POST /api/tasks/VTT-XXX/criteria/:criteriaId/fulfill
   { "status": "met", "evidence": "PR #123", "reportedBy": "UUID" }

5. Registrar impactos en documentos (si aplica):
   POST /api/tasks/VTT-XXX/document-impacts
   { "documentSourceId": "UUID", "impactType": "modified", "description": "..." }

6. Verificar gate ANTES de mover a in_review:
   GET /api/tasks/VTT-XXX/review-gate
   → si canProceedToReview = false → resolver/diferir blockers primero

7. Subir entregables:
   POST /api/tasks/VTT-XXX/attachments (multipart: devlog.md, *.LOGIC.md)

8. Mover a in_review:
   PATCH /api/tasks/VTT-XXX/status { statusId: "1ec975a5...", changedBy: "UUID" }
```

---

## SECCIÓN 17: DISCREPANCIAS HANDOFF vs CÓDIGO REAL

| Tema | Lo que decía el handoff S12 | Lo que está en el código |
|------|----------------------------|--------------------------|
| Devlog summary sprint | `GET /api/sprints/:sprintId/devlog-summary` | `GET /api/phases/:id/devlog-summary` |
| Devlog review sprint | `GET /api/sprints/:id/devlog-review` | `GET /api/phases/:id/devlog-review` |
| Reordenar fases | `orderedPhaseIds` (lo envía el FE) | `phaseIds` (lo espera el BE) |
| Settings sprints post-creación | Configurable vía PATCH | Zod lo descarta — solo aplica en POST |
| Crear deliverable settings | Solo `name` | `createdBy` UUID es OBLIGATORIO |
| Organizaciones | Endpoints `/api/organizations` | No existe — usar headers `X-Organization-Id` |
| Regeneración living docs | Síncrono | 202 Accepted + polling por Location header |

---

## SECCIÓN 18: SQL SEED PARA CATÁLOGOS VACÍOS

> **Enviar al DevOps Agent para ejecución en producción. NO ejecutar directamente.**

Para el SQL completo de todos los catálogos:
```
_project-management/Fases/11 Gestion de Proyectos/R4/SEED_CATALOGOS_VTT_CONSOLIDATED.sql
```

Seed mínimo de `devlog_category_catalog`:
```sql
INSERT INTO devlog_category_catalog (code, name, description, severity_levels, is_active, "order") VALUES
('issue',        'Issue',        'Observación o inconsistencia detectada',    ARRAY['critical','high','medium','low'], true, 0),
('tech_debt',    'Tech Debt',    'Deuda técnica identificada',                ARRAY['critical','high','medium','low'], true, 1),
('decision',     'Decision',     'Decisión técnica o de proceso tomada',      ARRAY[]::text[],                         true, 2),
('blocker',      'Blocker',      'Algo que bloquea el avance',                ARRAY['critical','high','medium','low'], true, 3),
('risk',         'Risk',         'Riesgo identificado',                       ARRAY['critical','high','medium','low'], true, 4),
('testing_note', 'Testing Note', 'Resultado de testing/QA',                  ARRAY['critical','high','medium','low'], true, 5),
('observation',  'Observation',  'Observación general',                       ARRAY[]::text[],                         true, 6),
('question',     'Question',     'Pregunta pendiente de resolver',            ARRAY['high','medium','low'],             true, 7),
('dependency',   'Dependencia',  'Dependencia entre tareas/sistemas',         ARRAY['high','medium'],                  true, 8),
('improvement',  'Mejora',       'Mejora para iteración futura',              ARRAY['medium','low'],                   true, 9),
('feedback',     'Feedback',     'Feedback de stakeholder',                   ARRAY['high','medium','low'],             true, 10),
('brand_issue',  'Issue Marca',  'Issue de marca/diseño',                     ARRAY['critical','high','medium'],        true, 11)
ON CONFLICT (code) DO UPDATE SET
  name = EXCLUDED.name, description = EXCLUDED.description,
  severity_levels = EXCLUDED.severity_levels, is_active = EXCLUDED.is_active;
```

---

## SECCIÓN 19: REFERENCIA DE ARCHIVOS

### Backend

| Propósito | Archivo |
|-----------|---------|
| Rutas principales | `backend/src/routes/index.ts` |
| Rutas proyectos | `backend/src/routes/projects.ts` |
| Rutas devlog | `backend/src/routes/taskDevlog.ts` |
| Servicio devlog | `backend/src/services/taskDevlog.service.ts` |
| Servicio review gate | `backend/src/services/reviewGate.service.ts` |
| Schema completo | `backend/prisma/schema.prisma` |
| Seed | `backend/prisma/seed.ts` |

### Documentos PM

| Propósito | Archivo |
|-----------|---------|
| Manual completo V4 | `_project-management/Fases/11 Gestion de Proyectos/R3/02 Implementacion/MANUAL_USUARIO_AGENTE_MODELO_DINAMICO_V4.md` |
| Catálogo de features | `_project-management/Fases/11 Gestion de Proyectos/R4/CATALOGO_FEATURES_VTT_V4.md` |
| Seed SQL consolidado | `_project-management/Fases/11 Gestion de Proyectos/R4/SEED_CATALOGOS_VTT_CONSOLIDATED.sql` |
| Handoffs S01-S08 | `_project-management/Fases/11 Gestion de Proyectos/R3/02 Implementacion/Sprint01_08/HANDOFF_TL_S0X.md` |
| Auditoría planificado vs implementado | `_project-management/Fases/11 Gestion de Proyectos/R3/02 Implementacion/Sprint01_08/AUDITORIA_PLANIFICADO_VS_IMPLEMENTADO_V4.md` |

### Rutas UI

| Pantalla | Ruta |
|----------|------|
| Crear proyecto | `/projects/new` |
| Settings de proyecto | `/projects/:id/settings` |
| Releases | `/projects/:id/releases` |
| Sprint | `/sprints/:sprintId` |
| Admin catálogos | `/admin/devlog-categories` |
| Admin trackable types | `/admin/trackable-types` |
| Admin flow templates | `/admin/flow-templates` |
| Devlog de tarea | `/tasks/:taskId/devlog` |
| Review gate | `/tasks/:taskId/review-gate` |
| Compliance | `/compliance` |

---

*Documento elaborado por Technical Research Engineer — 2026-04-27*
*Fuentes: R3 (Handoffs S01–S12) + R4 (Catálogos consolidados) + schema.prisma (73 modelos verificados)*
