# INVENTARIO COMPLETO: Paquete VTT Modelo Dinámico V4

| Campo | Valor |
|-------|-------|
| **Documento** | INVENTARIO_FEATURES_MODELO_DINAMICO_V4.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-04 |
| **Autor** | PM (Martin Rivas) |
| **Estado** | ✅ Análisis cerrado |

---

## 1. RESUMEN EJECUTIVO

| Métrica | Cantidad |
|---------|----------|
| **Features totales** | 29 |
| **Addendums** | 4 |
| **Sprints** | 12 (S01-S11 + S04-B) |
| **Tablas nuevas** | 29 |
| **Tablas ALTER** | 10 |
| **Rutas API** | 74 |
| **Decisiones PM** | 30 |
| **Horas estimadas** | ~205h |

---

## 2. SPEC BASE V4 — SPRINTS S01 A S08

### S01: Catálogos Base (~6h)

**Objetivo:** Crear catálogos fundamentales para configuración dinámica de proyectos.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `project_type_catalog` | Tipos de proyecto (software, marketing, research) | code, name, description, iconUrl, isActive |
| `phase_catalog` | Fases del ciclo SDLC | code, name, order, isRequired, defaultDuration |
| `deliverable_catalog` | Tipos de entregables | code, name, phaseCode, isRequired |
| `trackable_type_catalog` | Tipos de items rastreables (RF, ADR, KPI) | code, name, description, iconUrl |

**Endpoints:**
- GET /api/project-types
- GET /api/phases
- GET /api/deliverables
- GET /api/trackable-types

---

### S02: Flow Templates (~8h)

**Objetivo:** Permitir configurar flujos de trabajo predefinidos por tipo de proyecto.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `flow_template_catalog` | Templates de flujo (Agile, Waterfall, Custom) | code, name, projectTypeCode, description |
| `flow_phase_config` | Fases incluidas en cada template | flowTemplateCode, phaseCode, order, isRequired |
| `phase_deliverable_config` | Deliverables por fase en template | flowPhaseConfigId, deliverableCode, isRequired |

**Endpoints:**
- GET /api/flow-templates
- GET /api/flow-templates?projectType={code}
- GET /api/flow-templates/:id

---

### S03: Releases y Sprints (~10h)

**Objetivo:** Implementar estructura de releases y sprints para agrupar trabajo.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `releases` | Agrupador de sprints/fases | code, name, projectId, status, startDate, endDate |
| `sprints` | Iteraciones de trabajo | code, name, releaseId, order, status, startDate, endDate |
| `deliveries` (ALTER) | Agregar campos para vincular a sprint/release | sprintId, releaseId, phaseCode |

**Endpoints:**
- CRUD /api/projects/:id/releases
- CRUD /api/releases/:id/sprints
- PATCH /api/deliveries/:id (vincular a sprint)

---

### S04: Trackable Items (~8h)

**Objetivo:** Permitir rastrear requerimientos, ADRs, KPIs y vincularlos a tareas.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `trackable_items` | Items a rastrear (RF-001, ADR-002) | code, typeCode, projectId, title, description, status |
| `trackable_item_tasks` | Relación N:M item↔tarea | trackableItemId, taskId |
| `trackable_item_evidences` | Evidencias de cumplimiento | trackableItemId, type, url, description |

**Endpoints:**
- CRUD /api/projects/:id/trackable-items
- POST /api/trackable-items/:id/tasks
- POST /api/trackable-items/:id/evidences

---

### S04-B: Deferred Scope (ADDENDUM 1) (~4h)

**Objetivo:** Permitir diferir items a sprints futuros con tracking formal.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `trackable_item_deferrals` | Registro de diferimientos | trackableItemId, fromSprintId, toSprintId, reason, status |

**Estados:** deferral_pending, deferral_scheduled, deferral_completed, deferral_cancelled

**Endpoints:**
- POST /api/trackable-items/:id/defer
- GET /api/sprints/:id/deferrals
- PATCH /api/deferrals/:id/cancel

**Decisiones PM (D-13 a D-17):**
- D-13: Addendum entra como Sprint 4-B
- D-14: ID usa @default(uuid())
- D-15: Status codes con prefijo "deferral_"
- D-16: FK con onDelete: Cascade
- D-17: Operación "cancel" entra al MVP

---

### S05: Carpetas de Proyecto (~6h)

**Objetivo:** Organizar documentos en estructura de carpetas.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `project_folders` | Carpetas jerárquicas | projectId, name, parentId, path, order |

**Endpoints:**
- CRUD /api/projects/:id/folders
- PATCH /api/folders/:id/move

---

### S06: Documentos de Proyecto (~12h)

**Objetivo:** Gestión completa de documentos con soporte para living documents.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `project_documents` (ALTER) | Agregar campos living doc | isLivingDocument, autoUpdateSource, lastSyncAt, syncStatus |
| `document_index` | Índice para búsqueda | projectDocumentId, content, embeddings, lastIndexedAt |
| `living_document_configs` | Config adicional de docs vivos | projectDocumentId, updateTrigger, parserConfig |

**Endpoints:**
- CRUD /api/projects/:id/documents
- POST /api/documents/:id/sync
- GET /api/documents/:id/index

**Decisiones PM (D-01 a D-12):**
- D-01: deliveries ya existe → ALTER, no CREATE
- D-02: Task↔Delivery 1:N via Task.deliveryId
- D-03: Tabla objetivo = project_documents
- D-04: document_index referencia project_documents.id
- D-05: DocumentIndex.projectDocumentId como PK
- D-06: changeControl = fixed | controlled | dynamic
- D-07: BD es fuente de verdad, FileSystem es espejo
- D-08: Backend VTT = escritor único
- D-09: Living Docs MVP = solo Schema + API Endpoints
- D-10: Indexación post-commit asíncrona
- D-11: Extender servicios existentes
- D-12: Usar nombres reales de Prisma

---

### S07: Compliance Checks (~8h)

**Objetivo:** Verificaciones de cumplimiento configurables.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `compliance_checks` | Definición de checks | code, name, type, validationRule, severity, isActive |

**Endpoints:**
- CRUD /api/compliance-checks
- POST /api/tasks/:id/run-compliance
- GET /api/sprints/:id/compliance-summary

---

### S08: Firmas y Validación (ADDENDUM 2) (~18h)

**Objetivo:** Sistema de firmas en cascada y validación de calidad.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `stage_approvals` | Firmas a nivel de fase/stage | phaseId, role, userId, status, signedAt, comments |
| `sprint_approvals` | Firmas a nivel de sprint | sprintId, role, userId, status, signedAt |
| `release_approvals` | Firmas a nivel de release | releaseId, role, userId, status, signedAt |
| `task_findings` | Hallazgos por tarea | taskId, type, severity, description, status, resolution |
| `hardcode_patterns` | Patrones anti-hardcode | pattern, description, severity, isActive |

**Flujo de Firmas:**
```
Stage Approval (AR, QA, TL)
    ↓ todos firmados
Sprint Approval (AR, PM)
    ↓ todos firmados
Release Approval (AR, PM, Stakeholders)
```

**Endpoints:**
- POST /api/phases/:id/approvals
- POST /api/sprints/:id/approvals
- POST /api/releases/:id/approvals
- CRUD /api/tasks/:id/findings
- GET /api/tasks/:id/hardcode-check

**Decisiones PM (D-18 a D-21):**
- D-18: critical/high BLOQUEAN cierre de tarea
- D-19: Delegación solo para Sprint/Release, NO Stage
- D-20: Stakeholders externos NO obligatorios en MVP
- D-21: Check anti-hardcode HÍBRIDO (automático + manual)

---

## 3. ADDENDUM 3: TRAZABILIDAD Y DOCS DINÁMICOS — S09 Y S10

### S09: Catálogos + Trazabilidad Base (~16h)

**Objetivo:** Catálogos para trazabilidad y relaciones entre items.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `criteria_type_catalog` | Tipos de criterios (DoD, DoR, acceptance) | code, name, iconUrl, iconType |
| `devlog_category_catalog` | Categorías de devlog (issue, tech_debt, decision) | code, name, severityLevels, iconUrl |
| `link_type_catalog` | Tipos de relación (implements, depends_on) | code, name, iconUrl |
| `living_doc_source_catalog` | Fuentes de docs vivos (prisma_schema, swagger) | code, name, generationType, parserService |
| `trackable_item_links` | Relaciones entre items | sourceId, targetId, linkTypeCode |
| `acceptance_criteria` | Criterios de aceptación | projectId, typeCode, description, status |
| `acceptance_criteria_trackables` | N:M criterio↔item | criteriaId, trackableItemId |

**Endpoints:**
- GET /api/catalogs/criteria-types
- GET /api/catalogs/devlog-categories
- GET /api/catalogs/link-types
- GET /api/catalogs/living-doc-sources
- CRUD /api/trackable-items/:id/links
- CRUD /api/projects/:id/acceptance-criteria
- POST /api/acceptance-criteria/:id/trackables

---

### S10: Fulfillment + Devlog + Sources (~29h)

**Objetivo:** Cumplimiento de criterios, devlog estructurado y fuentes de documentos.

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `task_criteria_fulfillments` | Cumplimiento de criterios por tarea | taskId, criteriaId, status, evidence, verifiedBy |
| `task_devlog_entries` | Entradas estructuradas del devlog | taskId, categoryCode, severity, title, description, status |
| `project_document_sources` | Fuentes por documento (N:M) | projectDocumentId, sourceCode, priority, config |
| `task_document_impacts` | Impacto de tareas en documentos | taskId, projectDocumentId, status, completedAt |
| `tasks` (ALTER) | Back-refs para devlog | — |

**Gate de Devlog (D-32):**
```
GET /api/sprints/:id/devlog-review
    ↓
{ canProceed: false } si hay entries critical/high con status=pending
    ↓
SprintService.transitionToQA() retorna 409 Conflict
```

**Endpoints:**
- GET /api/tasks/:id/criteria
- POST /api/tasks/:id/criteria/:criteriaId/fulfill
- POST /api/tasks/:id/devlog-entries (batch)
- GET /api/sprints/:id/devlog-review
- POST /api/project-documents/:id/sources
- POST /api/tasks/:id/document-impacts/:docId/complete
- GET /api/projects/:id/traceability-report

**Decisiones PM (D-32 a D-35):**
- D-32: Gate de devlog BLOQUEA avance a QA si hay critical/high pendientes
- D-33: Solo PM/TL pueden crear criterios de aceptación
- D-34: Agente puede reportar fulfillment; TL revisa en gate
- D-35: Catálogos son GLOBALES (todos los proyectos comparten)

**Condiciones Técnicas Obligatorias:**
- C001: Relación DevlogEntryTask + back-refs en Task
- C002: Mapping autoUpdateSource (schema→prisma_schema, api_endpoints→swagger_openapi)
- M001: Back-refs en User (S09, S10)
- M002: Back-refs en Sprint (S09, S10)
- TL-D01: Gate 409 en transitionToQA()
- TL-D02: Async 202 + setImmediate + polling GET syncStatus
- TL-D03: PrismaParserService + SwaggerParserService en S10c

---

## 4. ADDENDUM 4: UX GESTIÓN DE PROYECTOS — S11

### S11: UX Configuración de Proyecto (~34h: BE 10h, FE 24h)

**Objetivo:** Wizard de creación y settings de proyecto post-creación.

#### Pantallas del Wizard (7 pasos)

| # | Pantalla | Descripción |
|---|----------|-------------|
| P1 | Selección de Tipo | Elegir tipo de proyecto del catálogo |
| P2 | Selección de Metodología | Elegir flow template o modo custom |
| P3 | Configuración de Sprints | Habilitar sprints, definir duración |
| P4 | Configuración de Fases | Reordenar, marcar requeridas/opcionales |
| P5 | Configuración de Deliverables | Seleccionar por fase desde catálogo |
| P6 | Resumen | Vista previa de configuración |
| P7 | Confirmación | Crear proyecto |

#### Pantallas de Settings (4 tabs)

| # | Pantalla | Descripción |
|---|----------|-------------|
| P8 | Settings - General | Nombre, descripción, tipo, metodología |
| P9 | Settings - Fases | Editar fases del proyecto |
| P10 | Settings - Deliverables | Editar deliverables por fase |
| P11 | Settings - Sprints | Configuración de sprints |
| P12 | Settings - Vista Completa | Todas las tabs integradas |

#### Componentes UI

| # | Componente | Uso |
|---|------------|-----|
| C1 | ProjectTypeSelector | Selector visual de tipo de proyecto |
| C2 | FlowTemplateSelector | Selector de metodología/template |
| C3 | SprintConfigPanel | Panel de configuración de sprints |
| C4 | PhaseListEditor | Editor de lista de fases con drag-drop |
| C5 | PhaseItem | Item individual de fase |
| C6 | DeliverableAccordion | Acordeón de deliverables por fase |
| C7 | DeliverableCheckbox | Checkbox de deliverable individual |
| C8 | ProjectSummaryCard | Resumen de configuración |
| C9 | WizardStepper | Navegación del wizard |
| C10 | PhaseCatalogPicker | Picker de fases del catálogo |
| C11 | DeliverableCatalogPicker | Picker de deliverables del catálogo |

#### Frontera de Persistencia (Regla Crítica)

| Tipo | Comportamiento |
|------|----------------|
| **Catálogos globales** | INMUTABLES desde wizard (solo lectura) |
| **Instancias de proyecto** | EDITABLES |

Template se clona al crear proyecto → proyecto independiente.

**Endpoints S11:**
- POST /api/projects (crear con wizard)
- GET /api/projects/:id/configuration
- PATCH /api/projects/:id/configuration
- POST /api/projects/:id/phases
- PATCH /api/projects/:id/phases/reorder
- DELETE /api/projects/:id/phases/:phaseId
- POST /api/projects/:id/phases/:phaseId/deliverables
- DELETE /api/projects/:id/phases/:phaseId/deliverables/:deliverableId

**Decisiones PM (D-22 a D-26):**
- D-22: Wizard tiene 7 pasos obligatorios
- D-23: Configuración se copia del template al proyecto; cambios son independientes
- D-24: Sprints se crean bajo demanda, no automáticamente
- D-25: Modo CUSTOM no tiene template; configuración manual completa
- D-26: Esta funcionalidad corresponde a S11

---

## 5. MAPA DE DECISIONES PM

### Decisiones D-01 a D-12 (SPEC Base)

| # | Decisión | Sprint |
|---|----------|--------|
| D-01 | deliveries ya existe → ALTER, no CREATE | S03 |
| D-02 | Task↔Delivery 1:N via Task.deliveryId | S03 |
| D-03 | Tabla objetivo = project_documents | S06 |
| D-04 | document_index referencia project_documents.id | S06 |
| D-05 | DocumentIndex.projectDocumentId como PK | S06 |
| D-06 | changeControl = fixed \| controlled \| dynamic | S06 |
| D-07 | BD es fuente de verdad, FileSystem es espejo | S06 |
| D-08 | Backend VTT = escritor único | S06 |
| D-09 | Living Docs MVP = solo Schema + API Endpoints | S06 |
| D-10 | Indexación post-commit asíncrona | S06 |
| D-11 | Extender servicios existentes | S06 |
| D-12 | Usar nombres reales de Prisma | S06 |

### Decisiones D-13 a D-17 (Deferred Scope)

| # | Decisión | Sprint |
|---|----------|--------|
| D-13 | Addendum entra como Sprint 4-B | S04-B |
| D-14 | ID usa @default(uuid()) | S04-B |
| D-15 | Status codes con prefijo "deferral_" | S04-B |
| D-16 | FK con onDelete: Cascade | S04-B |
| D-17 | Operación "cancel" entra al MVP | S04-B |

### Decisiones D-18 a D-21 (Firmas y Validación)

| # | Decisión | Sprint |
|---|----------|--------|
| D-18 | critical/high BLOQUEAN cierre de tarea | S08 |
| D-19 | Delegación solo para Sprint/Release, NO Stage | S08 |
| D-20 | Stakeholders externos NO obligatorios en MVP | S08 |
| D-21 | Check anti-hardcode HÍBRIDO | S08 |

### Decisiones D-22 a D-26 (UX Gestión de Proyectos)

| # | Decisión | Sprint |
|---|----------|--------|
| D-22 | Wizard tiene 7 pasos obligatorios | S11 |
| D-23 | Config se copia del template; cambios independientes | S11 |
| D-24 | Sprints se crean bajo demanda | S11 |
| D-25 | Modo CUSTOM no tiene template | S11 |
| D-26 | Funcionalidad corresponde a S11 | S11 |

### Decisiones D-32 a D-35 (Trazabilidad y Docs Dinámicos)

| # | Decisión | Sprint |
|---|----------|--------|
| D-32 | Gate de devlog BLOQUEA avance a QA | S10 |
| D-33 | Solo PM/TL pueden crear criterios | S09 |
| D-34 | Agente puede reportar fulfillment | S10 |
| D-35 | Catálogos son GLOBALES | S09 |

> **Nota:** D-27 a D-31 no existen (gap intencional entre bloques).

---

## 6. ESTRUCTURA DE BLOQUES

```
BLOQUE 1: TÉCNICO BASE (~126h)
├── S01: Catálogos Base
├── S02: Flow Templates
├── S03: Releases y Sprints
├── S04: Trackable Items
├── S04-B: Deferred Scope (Addendum 1)
├── S05: Carpetas
├── S06: Documentos
├── S07: Compliance
└── S08: Firmas y Validación (Addendum 2)

BLOQUE 2: TRAZABILIDAD (~45h)
├── S09: Catálogos + Trazabilidad Base
└── S10: Fulfillment + Devlog + Sources (Addendum 3)

BLOQUE 3: GESTIÓN DE PROYECTOS (~34h)
└── S11: UX Configuración de Proyecto (Addendum 4)
```

---

## 7. DEPENDENCIAS ENTRE SPRINTS

```
S01 ──────────────────────────────────────────────────────►
S02 ← S01 ────────────────────────────────────────────────►
S03 ────────────────────────────────────────────────────────►
S04 ← S01 ────────────────────────────────────────────────►
S04-B ← S04 ──────────────────────────────────────────────►
S05 ← S03 ────────────────────────────────────────────────►
S06 ← S03, S05 ───────────────────────────────────────────►
S07 ← S06 ────────────────────────────────────────────────►
S08 ← S03, S06 ───────────────────────────────────────────►
S09 ← S04 ────────────────────────────────────────────────►
S10 ← S09, S06 ───────────────────────────────────────────►
S11 ← S01, S02, S03, S06 ─────────────────────────────────►
```

---

**Documento:** INVENTARIO_FEATURES_MODELO_DINAMICO_V4.md  
**Versión:** 1.0  
**Estado:** ✅ Completo  
**Fecha:** 2026-04-04

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
