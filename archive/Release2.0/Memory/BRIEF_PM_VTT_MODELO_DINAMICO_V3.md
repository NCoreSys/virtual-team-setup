# BRIEF PM — VTT MODELO DINÁMICO DE GESTIÓN DE PROYECTOS

| Campo | Valor |
|-------|-------|
| **Proyecto** | Virtual Teams Tracking (VTT) |
| **Módulo** | Modelo Dinámico de Gestión |
| **Versión** | 3.0.0 |
| **Fecha** | 2026-03-24 |
| **Fase SDLC** | 02-Analysis |
| **Estado** | 🔄 En análisis — Pendiente AR |
| **Autor** | PM (Martin Rivas) |
| **Siguiente** | AR (Arquitecto) |

---

## 1. RESUMEN EJECUTIVO

### 1.1 Visión

Transformar VTT de un sistema de tracking de proyectos de software a una **plataforma genérica de gestión de proyectos** que soporte cualquier tipo de proyecto (software, marketing, investigación, custom) con flujos configurables, entregables dinámicos, control de documentos y requisitos obligatorios por tarea.

### 1.2 Objetivos

| # | Objetivo | Métrica de Éxito |
|---|----------|------------------|
| O1 | Soportar múltiples tipos de proyecto | ≥3 tipos predefinidos + custom |
| O2 | Flujos configurables por proyecto | Usuario puede definir fases y orden |
| O3 | Entregables dinámicos con templates | 100% de entregables con template opcional |
| O4 | Control de cambios en documentos | Fixed/Controlled/Dynamic funcionando |
| O5 | Requisitos obligatorios por tarea | Bloqueo de status si no cumple |
| O6 | QA puede auditar cumplimiento | Checklist automático visible |

### 1.3 Alcance

| En Scope | Fuera de Scope |
|----------|----------------|
| Catálogos genéricos (tipos, fases, entregables) | Integración con herramientas externas |
| Flujos predefinidos (SDLC-Scrum, Kanban, Waterfall) | Generación automática de templates por IA (v2) |
| Configuración de flujo por proyecto | Workflow engine con reglas complejas |
| Control de documentos (fixed/controlled/dynamic) | Versionado automático de documentos |
| Requisitos obligatorios por tarea | Aprobaciones multi-nivel |
| Vista de Documentos (Split View) | Editor de documentos inline |
| Templates de entregables | — |

---

## 2. ESTADO ACTUAL DE BD

### 2.1 Lo Que Ya Existe

```
✅ StatusCatalog (process: project|phase|task|import|delivery)
✅ PriorityCatalog
✅ DocumentTypeCatalog
✅ Deliveries (phaseId, lifecycleStage, statusId)
✅ Task.deliveryId
✅ Document / ProjectDocument / TaskAttachment
✅ Phase.lifecycleStage
```

### 2.2 Lo Que Se Creará

```
⬜ ProjectTypeCatalog
⬜ PhaseCatalog (genérico)
⬜ DeliverableCatalog (genérico)
⬜ FlowTemplateCatalog
⬜ FlowPhaseConfig
⬜ PhaseDeliverableConfig
⬜ DocumentTemplate
⬜ TaskRequirementCatalog
⬜ TaskTypeRequirements
⬜ TaskRequirementStatus
⬜ Release
⬜ Sprint
⬜ Campos nuevos en Project, Phase, Task, ProjectDocument
```

---

## 3. ARQUITECTURA DE DATOS

### 3.1 Módulo A: Catálogos Base

```prisma
// ============================================
// TIPOS DE PROYECTO
// ============================================
model ProjectTypeCatalog {
  id          String   @id @default(uuid())
  code        String   @unique  // "software", "marketing", "research", "custom"
  name        String
  description String?
  icon        String?  // emoji o código de ícono
  isSystem    Boolean  @default(false)  // true = no se puede eliminar
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
  
  flowTemplates FlowTemplateCatalog[]
  projects      Project[]
  
  @@map("project_type_catalog")
}

// ============================================
// FASES (GENÉRICAS)
// ============================================
model PhaseCatalog {
  id              String   @id @default(uuid())
  code            String   @unique  // "discovery", "planning", "design-ux", "development"
  name            String
  description     String?
  icon            String?
  projectTypeCode String?  // null = aplica a todos los tipos
  isSystem        Boolean  @default(false)
  isActive        Boolean  @default(true)
  createdAt       DateTime @default(now())
  
  flowPhases   FlowPhaseConfig[]
  deliverables PhaseDeliverableConfig[]
  
  @@index([projectTypeCode])
  @@map("phase_catalog")
}

// ============================================
// ENTREGABLES (GENÉRICOS)
// ============================================
model DeliverableCatalog {
  id                String   @id @default(uuid())
  code              String   @unique  // "prd", "srs", "erd", "test-plan", "campaign-brief"
  name              String
  description       String?
  documentTypeCode  String   // FK lógico a DocumentTypeCatalog
  projectTypeCode   String?  // null = aplica a todos
  
  // Control de cambios
  changeControl     String   @default("dynamic")  // "fixed" | "controlled" | "dynamic"
  approversRequired String[] @default([])  // ["PO", "PM"] si es fixed/controlled
  updateFrequency   String   @default("per_task")  // "per_task" | "per_sprint" | "per_release" | "once"
  isLivingDocument  Boolean  @default(false)  // true = se actualiza constantemente
  
  isSystem          Boolean  @default(false)
  isActive          Boolean  @default(true)
  createdAt         DateTime @default(now())
  
  phaseConfigs PhaseDeliverableConfig[]
  templates    DocumentTemplate[]
  
  @@index([projectTypeCode])
  @@index([documentTypeCode])
  @@map("deliverable_catalog")
}
```

### 3.2 Módulo B: Flujos y Configuración

```prisma
// ============================================
// TEMPLATES DE FLUJO (predefinidos)
// ============================================
model FlowTemplateCatalog {
  id              String   @id @default(uuid())
  code            String   @unique  // "sdlc-scrum", "sdlc-kanban", "sdlc-waterfall", "marketing-campaign"
  name            String
  description     String?
  projectTypeCode String
  
  // Configuración de metodología
  methodology     String   @default("hybrid")  // "scrum" | "kanban" | "waterfall" | "hybrid"
  sprintEnabled   Boolean  @default(true)
  sprintDuration  Int?     @default(14)  // días
  
  isSystem        Boolean  @default(false)
  isDefault       Boolean  @default(false)  // default para ese projectType
  isActive        Boolean  @default(true)
  createdAt       DateTime @default(now())
  
  projectType ProjectTypeCatalog @relation(fields: [projectTypeCode], references: [code])
  phases      FlowPhaseConfig[]
  projects    Project[]
  
  @@index([projectTypeCode])
  @@map("flow_template_catalog")
}

// ============================================
// FASES DEL FLUJO
// ============================================
model FlowPhaseConfig {
  id               String   @id @default(uuid())
  flowTemplateId   String
  phaseCode        String   // FK lógico a PhaseCatalog
  
  order            Int      // 1, 2, 3...
  isRequired       Boolean  @default(true)
  canRunInParallel Boolean  @default(false)
  dependsOnPhaseId String?  // FK a otra FlowPhaseConfig (para flujos no lineales)
  
  createdAt        DateTime @default(now())
  
  flowTemplate    FlowTemplateCatalog      @relation(fields: [flowTemplateId], references: [id], onDelete: Cascade)
  dependsOnPhase  FlowPhaseConfig?         @relation("PhaseDependency", fields: [dependsOnPhaseId], references: [id])
  dependentPhases FlowPhaseConfig[]        @relation("PhaseDependency")
  deliverables    PhaseDeliverableConfig[]
  
  @@unique([flowTemplateId, phaseCode])
  @@index([flowTemplateId])
  @@map("flow_phase_config")
}

// ============================================
// ENTREGABLES POR FASE DEL FLUJO
// ============================================
model PhaseDeliverableConfig {
  id               String   @id @default(uuid())
  flowPhaseId      String
  deliverableCode  String   // FK lógico a DeliverableCatalog
  phaseCode        String   // FK lógico a PhaseCatalog (redundante pero útil)
  
  order            Int      @default(0)
  isRequired       Boolean  @default(false)
  defaultTemplateId String? // FK a DocumentTemplate
  
  createdAt        DateTime @default(now())
  
  flowPhase       FlowPhaseConfig   @relation(fields: [flowPhaseId], references: [id], onDelete: Cascade)
  phase           PhaseCatalog      @relation(fields: [phaseCode], references: [code])
  deliverable     DeliverableCatalog @relation(fields: [deliverableCode], references: [code])
  defaultTemplate DocumentTemplate? @relation(fields: [defaultTemplateId], references: [id])
  
  @@unique([flowPhaseId, deliverableCode])
  @@index([flowPhaseId])
  @@map("phase_deliverable_config")
}

// ============================================
// TEMPLATES DE DOCUMENTOS
// ============================================
model DocumentTemplate {
  id              String   @id @default(uuid())
  deliverableCode String   // FK lógico a DeliverableCatalog
  
  name            String
  description     String?
  fileName        String   // nombre en MinIO
  filePath        String   // ruta completa en MinIO
  fileSize        Int
  mimeType        String
  version         Int      @default(1)
  
  isSystem        Boolean  @default(false)  // true = proveído por nosotros
  isDefault       Boolean  @default(false)  // default para ese deliverable
  isActive        Boolean  @default(true)
  
  uploadedById    String?
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
  
  deliverable    DeliverableCatalog       @relation(fields: [deliverableCode], references: [code])
  uploadedBy     User?                    @relation(fields: [uploadedById], references: [id])
  phaseDeliverables PhaseDeliverableConfig[]
  
  @@index([deliverableCode])
  @@map("document_templates")
}
```

### 3.3 Módulo C: Instancias de Proyecto

```prisma
// ============================================
// MODIFICACIONES A PROJECT
// ============================================
model Project {
  // ... campos existentes ...
  
  // Nuevos campos
  projectTypeCode  String?  @default("software") @map("project_type_code")
  flowTemplateId   String?  @map("flow_template_id")
  sprintEnabled    Boolean  @default(true) @map("sprint_enabled")
  sprintDuration   Int?     @default(14) @map("sprint_duration")
  
  projectType   ProjectTypeCatalog?  @relation(fields: [projectTypeCode], references: [code])
  flowTemplate  FlowTemplateCatalog? @relation(fields: [flowTemplateId], references: [id])
  releases      Release[]
  
  @@map("projects")
}

// ============================================
// RELEASES
// ============================================
model Release {
  id          String    @id @default(uuid())
  projectId   String
  
  name        String    // "MVP", "v2.0", "Q1 Campaign"
  version     String?
  description String?
  statusId    String
  
  startDate   DateTime?
  targetDate  DateTime?
  releaseDate DateTime?
  
  order       Int       @default(0)
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
  
  project Project       @relation(fields: [projectId], references: [id], onDelete: Cascade)
  status  StatusCatalog @relation(fields: [statusId], references: [id])
  phases  Phase[]
  sprints Sprint[]
  
  @@index([projectId])
  @@map("releases")
}

// ============================================
// SPRINTS
// ============================================
model Sprint {
  id        String    @id @default(uuid())
  releaseId String
  
  code      String    // "S01", "S07"
  name      String?
  goal      String?
  
  startDate DateTime
  endDate   DateTime
  statusId  String
  
  order     Int       @default(0)
  createdAt DateTime  @default(now())
  updatedAt DateTime  @updatedAt
  
  release     Release       @relation(fields: [releaseId], references: [id], onDelete: Cascade)
  status      StatusCatalog @relation(fields: [statusId], references: [id])
  deliveries  Deliveries[]
  tasks       Task[]
  
  @@unique([releaseId, code])
  @@index([releaseId])
  @@map("sprints")
}

// ============================================
// MODIFICACIONES A PHASE
// ============================================
model Phase {
  // ... campos existentes ...
  
  // Nuevos campos
  releaseId    String?  @map("release_id")
  phaseCode    String?  @map("phase_code")  // FK lógico a PhaseCatalog
  type         String   @default("sdlc")    // "sdlc" | "module" | "custom"
  
  release Release? @relation(fields: [releaseId], references: [id], onDelete: SetNull)
  
  @@map("phases")
}

// ============================================
// MODIFICACIONES A DELIVERIES
// ============================================
model Deliveries {
  // ... campos existentes ...
  
  // Nuevos campos
  sprintId        String?  @map("sprint_id")
  deliverableCode String?  @map("deliverable_code")  // FK lógico a DeliverableCatalog
  templateId      String?  @map("template_id")
  
  sprint   Sprint?           @relation(fields: [sprintId], references: [id], onDelete: SetNull)
  template DocumentTemplate? @relation(fields: [templateId], references: [id])
  
  @@map("deliveries")
}

// ============================================
// MODIFICACIONES A TASK
// ============================================
model Task {
  // ... campos existentes ...
  
  // Nuevos campos
  sprintId String? @map("sprint_id")
  
  sprint              Sprint?                 @relation(fields: [sprintId], references: [id], onDelete: SetNull)
  requirementStatuses TaskRequirementStatus[]
  
  @@map("tasks")
}
```

### 3.4 Módulo D: Control de Documentos

```prisma
// ============================================
// MODIFICACIONES A PROJECT_DOCUMENT
// ============================================
model ProjectDocument {
  // ... campos existentes ...
  
  // Nuevos campos para V3.1
  phaseCode        String?  @map("phase_code")       // "04-development"
  subFolder        String?  @map("sub_folder")       // "deliverables" | "_pm" | "knowledge"
  sprintId         String?  @map("sprint_id")
  taskId           String?  @map("task_id")          // vinculación opcional
  deliverableCode  String?  @map("deliverable_code") // FK lógico a DeliverableCatalog
  
  // Control de cambios
  changeControl    String?  @map("change_control")   // heredado de DeliverableCatalog o override
  lockedAt         DateTime? @map("locked_at")       // si está bloqueado
  lockedById       String?  @map("locked_by_id")
  lockedReason     String?  @map("locked_reason")
  
  // Para documentos "living"
  lastReviewedAt   DateTime? @map("last_reviewed_at")
  lastReviewedById String?   @map("last_reviewed_by_id")
  reviewRequired   Boolean   @default(false) @map("review_required")
  
  @@index([phaseCode])
  @@index([sprintId])
  @@index([deliverableCode])
  @@map("project_documents")
}

// ============================================
// HISTORIAL DE CAMBIOS EN DOCUMENTOS
// ============================================
model DocumentChangeRequest {
  id              String    @id @default(uuid())
  documentId      String
  
  requestedById   String
  reason          String
  proposedChanges String?   // descripción o diff
  
  status          String    @default("pending")  // "pending" | "approved" | "rejected"
  reviewedById    String?
  reviewedAt      DateTime?
  reviewNotes     String?
  
  createdAt       DateTime  @default(now())
  
  @@index([documentId])
  @@index([status])
  @@map("document_change_requests")
}
```

### 3.5 Módulo E: Requisitos Obligatorios

```prisma
// ============================================
// CATÁLOGO DE REQUISITOS
// ============================================
model TaskRequirementCatalog {
  id             String   @id @default(uuid())
  code           String   @unique  // "upload_devlog", "update_schema", "create_pr", "update_api_docs"
  name           String
  description    String?
  
  type           String   // "file_upload" | "document_update" | "external_action" | "checklist_item"
  category       String   // "documentation" | "code_quality" | "process" | "delivery"
  
  // Validación
  validationType String   @default("manual")  // "manual" | "auto_file_exists" | "auto_doc_modified"
  targetDocument String?  // código del documento que debe actualizarse (ej: "schema_reference")
  
  // Configuración
  isBlocking     Boolean  @default(true)   // true = no puede mover status si no cumple
  blockingStatus String[] @default(["completed"])  // en qué transiciones bloquea
  
  isSystem       Boolean  @default(false)
  isActive       Boolean  @default(true)
  createdAt      DateTime @default(now())
  
  taskTypeRequirements TaskTypeRequirement[]
  
  @@index([category])
  @@map("task_requirement_catalog")
}

// ============================================
// REQUISITOS POR TIPO DE TAREA
// ============================================
model TaskTypeRequirement {
  id                String   @id @default(uuid())
  
  taskType          String   // "feature" | "bug" | "database" | "api" | "frontend" | "documentation"
  requirementCode   String   // FK lógico a TaskRequirementCatalog
  
  isRequired        Boolean  @default(true)
  order             Int      @default(0)
  
  // Documentos que DEBEN actualizarse para este tipo de tarea
  documentsToUpdate String[] @default([])  // ["schema_reference", "api_endpoints", "services"]
  
  createdAt         DateTime @default(now())
  
  requirement TaskRequirementCatalog @relation(fields: [requirementCode], references: [code])
  
  @@unique([taskType, requirementCode])
  @@index([taskType])
  @@map("task_type_requirements")
}

// ============================================
// ESTADO DE REQUISITOS POR TAREA
// ============================================
model TaskRequirementStatus {
  id              String    @id @default(uuid())
  taskId          String
  requirementCode String    // FK lógico a TaskRequirementCatalog
  
  status          String    @default("pending")  // "pending" | "completed" | "skipped" | "not_applicable"
  
  // Evidencia
  completedAt     DateTime?
  completedById   String?
  evidence        Json?     // { fileId?, documentId?, prUrl?, notes? }
  
  // Si se saltó
  skippedReason   String?
  skippedById     String?
  skippedAt       DateTime?
  
  createdAt       DateTime  @default(now())
  updatedAt       DateTime  @updatedAt
  
  task        Task @relation(fields: [taskId], references: [id], onDelete: Cascade)
  
  @@unique([taskId, requirementCode])
  @@index([taskId])
  @@index([status])
  @@map("task_requirement_status")
}
```

---

## 4. DATOS SEED

### 4.1 Tipos de Proyecto

| code | name | isSystem |
|------|------|----------|
| software | Desarrollo de Software | true |
| marketing | Campaña de Marketing | true |
| research | Investigación | true |
| custom | Proyecto Personalizado | true |

### 4.2 Fases (Catálogo Genérico)

| code | name | projectTypeCode | isSystem |
|------|------|-----------------|----------|
| discovery | Discovery | software | true |
| planning | Planning | software | true |
| analysis | Analysis | software | true |
| design-ux | Design UX/UI | software | true |
| design-tech | Design Technical | software | true |
| development | Development | software | true |
| testing | Testing | software | true |
| deploy | Deploy | software | true |
| operations | Operations | software | true |
| brief | Brief | marketing | true |
| strategy | Strategy | marketing | true |
| creative | Creative | marketing | true |
| production | Production | marketing | true |
| launch | Launch | marketing | true |
| measurement | Measurement | marketing | true |

### 4.3 Templates de Flujo

| code | name | projectTypeCode | methodology | sprintEnabled |
|------|------|-----------------|-------------|---------------|
| sdlc-scrum | SDLC Scrum | software | scrum | true |
| sdlc-kanban | SDLC Kanban | software | kanban | false |
| sdlc-waterfall | SDLC Waterfall | software | waterfall | false |
| sdlc-hybrid | SDLC Híbrido | software | hybrid | true |
| marketing-campaign | Campaña Marketing | marketing | kanban | false |

### 4.4 Entregables con Control de Cambios

| code | name | changeControl | approversRequired | isLivingDocument |
|------|------|---------------|-------------------|------------------|
| vision | Vision Statement | fixed | ["PO"] | false |
| prd | Product Requirements | fixed | ["PO", "PM"] | false |
| scope | Scope Document | controlled | ["PM"] | false |
| srs | Software Requirements | controlled | ["PM", "SA"] | false |
| schema_reference | Schema Reference | dynamic | [] | true |
| api_endpoints | API Endpoints | dynamic | [] | true |
| services_doc | Services Documentation | dynamic | [] | true |
| design_system | Design System | dynamic | [] | true |
| changelog | Changelog | dynamic | [] | true |
| devlog | Devlog | dynamic | [] | false |

### 4.5 Requisitos Obligatorios

| code | name | type | isBlocking | category |
|------|------|------|------------|----------|
| upload_devlog | Subir Devlog | file_upload | true | documentation |
| upload_logic | Subir archivo de lógica | file_upload | true | documentation |
| update_schema | Actualizar SCHEMA_REFERENCE | document_update | true | documentation |
| update_api_docs | Actualizar API_ENDPOINTS | document_update | true | documentation |
| update_services | Actualizar SERVICES_DOC | document_update | true | documentation |
| create_pr | Crear Pull Request | external_action | true | code_quality |
| pr_approved | PR Aprobado | external_action | true | code_quality |
| run_tests | Ejecutar tests | external_action | false | code_quality |
| code_review | Code Review completado | external_action | true | code_quality |

### 4.6 Requisitos por Tipo de Tarea

| taskType | requirementCode | documentsToUpdate |
|----------|-----------------|-------------------|
| database | upload_devlog | ["schema_reference"] |
| database | upload_logic | [] |
| database | update_schema | ["schema_reference"] |
| database | create_pr | [] |
| api | upload_devlog | ["api_endpoints", "services_doc"] |
| api | upload_logic | [] |
| api | update_api_docs | ["api_endpoints"] |
| api | update_services | ["services_doc"] |
| api | create_pr | [] |
| frontend | upload_devlog | ["design_system"] |
| frontend | create_pr | [] |
| feature | upload_devlog | [] |
| feature | create_pr | [] |
| feature | pr_approved | [] |
| bug | upload_devlog | [] |
| bug | create_pr | [] |

---

## 5. REGLAS DE NEGOCIO

### 5.1 Proyectos y Flujos

| Código | Regla |
|--------|-------|
| RN-001 | Project debe tener un projectTypeCode |
| RN-002 | Project puede tener un flowTemplateId (opcional = custom) |
| RN-003 | Si flowTemplateId es null, usuario define fases manualmente |
| RN-004 | Release pertenece a un Project |
| RN-005 | Sprint pertenece a un Release |
| RN-006 | Sprint.code único dentro del Release |
| RN-007 | Si Project.sprintEnabled = false, no se pueden crear sprints |
| RN-008 | Sprint.endDate > Sprint.startDate |

### 5.2 Control de Documentos

| Código | Regla |
|--------|-------|
| RN-010 | Documento "fixed" no se puede modificar sin ChangeRequest aprobado |
| RN-011 | Documento "controlled" requiere aprobación de approversRequired |
| RN-012 | Documento "dynamic" se puede modificar libremente |
| RN-013 | isLivingDocument = true implica que debe actualizarse cada vez que cambie su área |
| RN-014 | Documento bloqueado (lockedAt != null) no se puede modificar |

### 5.3 Requisitos Obligatorios

| Código | Regla |
|--------|-------|
| RN-020 | Al crear Task, se generan TaskRequirementStatus según su taskType |
| RN-021 | Si requirement.isBlocking = true, Task no puede moverse a status bloqueado |
| RN-022 | Requisitos con validationType = "auto_doc_modified" se validan automáticamente |
| RN-023 | Requisitos "skipped" requieren skippedReason y skippedById |
| RN-024 | QA puede ver checklist de requisitos para auditoría |

### 5.4 Documentos UX

| Código | Regla |
|--------|-------|
| RN-030 | subFolder se deriva automáticamente del documentType |
| RN-031 | Handoff, Brief, Assignment → subFolder = "_pm" |
| RN-032 | Spec, Arquitectura, ERD, Mockup → subFolder = "deliverables" |
| RN-033 | Devlog, Error, Bug, QA → subFolder = "knowledge" |

---

## 6. FLUJOS PREDEFINIDOS (SEEDS)

### 6.1 SDLC-Scrum

```
Fases: planning → analysis → design-ux → design-tech → development → testing → deploy → operations
       (paralelo: design-ux ↔ design-tech)
       (paralelo: development ↔ testing)

Sprint: Habilitado, 14 días

Fases requeridas: planning, development, testing, deploy
Fases opcionales: discovery, analysis, design-ux, design-tech, operations
```

### 6.2 SDLC-Kanban

```
Fases: development → testing → deploy → operations
       (flujo continuo, sin sprints)

Sprint: Deshabilitado

Todas las fases requeridas
```

### 6.3 SDLC-Waterfall

```
Fases: discovery → planning → analysis → design-ux → design-tech → development → testing → deploy → operations
       (secuencial estricto, no paralelo)

Sprint: Deshabilitado

Todas las fases requeridas
```

### 6.4 Marketing-Campaign

```
Fases: brief → strategy → creative → production → launch → measurement
       (paralelo: creative ↔ production)

Sprint: Deshabilitado

Fases requeridas: brief, creative, launch
```

---

## 7. UX DE DOCUMENTOS

### 7.1 Vista Split View

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Documentos                    [Estructura][Todos][Recientes]  [+ Subir] │
├──────────────┬────────────────────────────────────┬─────────────────────┤
│ ÁRBOL        │ ARCHIVOS                           │ PREVIEW             │
│              │                                    │                     │
│ 📦 Proyecto  │ Breadcrumb: Proyecto > Fase > Sub  │ Nombre archivo      │
│ ├─ _pm/      │                                    │                     │
│ ├─ docs/     │ [Filtros por tipo]                 │ Información         │
│ ├─ phases/   │                                    │ ─────────────       │
│ │  ├─ 01-... │ Lista de archivos con badges      │ Tipo, Fase, Sprint  │
│ │  ├─ 02-... │ - Estado (fixed/dynamic)          │ Control de cambios  │
│ │  └─ ...    │ - Sprint                          │ Vinculación         │
│ └─ archive/  │ - Última actualización            │                     │
│              │                                    │ [Ver][Descargar]    │
└──────────────┴────────────────────────────────────┴─────────────────────┘
```

### 7.2 Modal Subida Manual

| Sección | Campo | Tipo | Requerido |
|---------|-------|------|-----------|
| **Archivo** | Upload | Dropzone | ✅ |
| **📍 Ubicación** | Proyecto | Select | ✅ |
| | Fase | Select | ✅ |
| | Sprint | Select | Opcional |
| **🏷️ Clasificación** | Tipo de documento | Select (categorizado) | ✅ |
| **🔗 Vinculación** | Tarea | Input | Opcional |
| | Entregable | Select | Opcional |

**Subcarpeta:** Se deriva automáticamente del tipo de documento.

### 7.3 Indicadores de Control de Cambios

| Indicador | Significado |
|-----------|-------------|
| 🔒 | Documento fijo (no editable sin aprobación) |
| 🔐 | Documento controlado (requiere aprobación) |
| 📝 | Documento dinámico (editable) |
| 🔄 | Living document (actualización constante) |
| ⚠️ | Requiere revisión/actualización |

---

## 8. PLAN DE SPRINTS

### Sprint S01 — Catálogos Base (16h)

| ID | Tarea | Responsable | Horas |
|----|-------|-------------|-------|
| S01-001 | Crear tabla `project_type_catalog` | DB Engineer | 1h |
| S01-002 | Crear tabla `phase_catalog` | DB Engineer | 2h |
| S01-003 | Crear tabla `deliverable_catalog` | DB Engineer | 2h |
| S01-004 | Seed: 4 tipos de proyecto | DB Engineer | 1h |
| S01-005 | Seed: ~15 fases genéricas | DB Engineer | 2h |
| S01-006 | Seed: ~50 entregables con control de cambios | DB Engineer | 3h |
| S01-007 | API GET catálogos (read-only) | Backend Dev | 4h |
| S01-008 | Tests unitarios | Backend Dev | 1h |

**Entregable:** Catálogos base poblados y APIs de consulta

---

### Sprint S02 — Flujos y Configuración (20h)

| ID | Tarea | Responsable | Horas |
|----|-------|-------------|-------|
| S02-001 | Crear tabla `flow_template_catalog` | DB Engineer | 2h |
| S02-002 | Crear tabla `flow_phase_config` | DB Engineer | 2h |
| S02-003 | Crear tabla `phase_deliverable_config` | DB Engineer | 2h |
| S02-004 | Crear tabla `document_templates` | DB Engineer | 2h |
| S02-005 | Seed: 5 templates de flujo | DB Engineer | 2h |
| S02-006 | Seed: Configuración de fases por flujo | DB Engineer | 2h |
| S02-007 | Seed: Entregables por fase | DB Engineer | 2h |
| S02-008 | API CRUD FlowTemplates | Backend Dev | 3h |
| S02-009 | API GET configuración de flujo | Backend Dev | 2h |
| S02-010 | Tests unitarios | Backend Dev | 1h |

**Entregable:** Sistema de flujos configurables funcionando

---

### Sprint S03 — Instancias de Proyecto (20h)

| ID | Tarea | Responsable | Horas |
|----|-------|-------------|-------|
| S03-001 | Crear tabla `releases` | DB Engineer | 2h |
| S03-002 | Crear tabla `sprints` | DB Engineer | 2h |
| S03-003 | Agregar campos a `Project` | DB Engineer | 1h |
| S03-004 | Agregar campos a `Phase` | DB Engineer | 1h |
| S03-005 | Agregar campos a `Deliveries` | DB Engineer | 1h |
| S03-006 | Agregar `sprintId` a `Task` | DB Engineer | 1h |
| S03-007 | Migración: crear Release "Default" por proyecto | DB Engineer | 2h |
| S03-008 | Migración: asignar phases a Release Default | DB Engineer | 2h |
| S03-009 | CRUD API Releases | Backend Dev | 4h |
| S03-010 | CRUD API Sprints | Backend Dev | 3h |
| S03-011 | Tests unitarios | Backend Dev | 1h |

**Entregable:** Modelo de instancias (Release, Sprint) funcionando

---

### Sprint S04 — Control de Documentos (16h)

| ID | Tarea | Responsable | Horas |
|----|-------|-------------|-------|
| S04-001 | Agregar campos control a `ProjectDocument` | DB Engineer | 2h |
| S04-002 | Crear tabla `document_change_requests` | DB Engineer | 2h |
| S04-003 | API validación de cambios (fixed/controlled) | Backend Dev | 4h |
| S04-004 | API crear/aprobar ChangeRequest | Backend Dev | 4h |
| S04-005 | API marcar documento como "review required" | Backend Dev | 2h |
| S04-006 | Tests unitarios | Backend Dev | 2h |

**Entregable:** Sistema de control de cambios en documentos

---

### Sprint S05 — Requisitos Obligatorios (24h)

| ID | Tarea | Responsable | Horas |
|----|-------|-------------|-------|
| S05-001 | Crear tabla `task_requirement_catalog` | DB Engineer | 2h |
| S05-002 | Crear tabla `task_type_requirements` | DB Engineer | 2h |
| S05-003 | Crear tabla `task_requirement_status` | DB Engineer | 2h |
| S05-004 | Seed: ~10 requisitos base | DB Engineer | 2h |
| S05-005 | Seed: Requisitos por tipo de tarea | DB Engineer | 2h |
| S05-006 | API GET requisitos de una tarea | Backend Dev | 3h |
| S05-007 | API actualizar estado de requisito | Backend Dev | 3h |
| S05-008 | Validación: bloquear transición de status | Backend Dev | 4h |
| S05-009 | Auto-validación: verificar documento modificado | Backend Dev | 3h |
| S05-010 | Tests unitarios | Backend Dev | 1h |

**Entregable:** Sistema de requisitos obligatorios con bloqueo de status

---

### Sprint S06 — Documentos UX (20h)

| ID | Tarea | Responsable | Horas |
|----|-------|-------------|-------|
| S06-001 | Agregar campos V3.1 a `ProjectDocument` | DB Engineer | 2h |
| S06-002 | Modificar API upload documentos | Backend Dev | 3h |
| S06-003 | API GET documentos con filtros | Backend Dev | 3h |
| S06-004 | FE: Componente árbol de navegación | Frontend Dev | 4h |
| S06-005 | FE: Vista split (archivos + preview) | Frontend Dev | 4h |
| S06-006 | FE: Modal subida actualizado | Frontend Dev | 3h |
| S06-007 | FE: Indicadores de control de cambios | Frontend Dev | 1h |

**Entregable:** Sección Documentos con UX completa

---

### Sprint S07 — Seeds Completos y QA (12h)

| ID | Tarea | Responsable | Horas |
|----|-------|-------------|-------|
| S07-001 | Seed: 438 deliverables SDLC completos | DB Engineer | 4h |
| S07-002 | Seed: Templates de documentos base | DB Engineer | 2h |
| S07-003 | Validar flujos predefinidos end-to-end | QA | 3h |
| S07-004 | Documentación técnica | Tech Writer | 3h |

**Entregable:** Sistema completo con datos de producción

---

## 9. RESUMEN DE ESTIMACIÓN

| Sprint | Nombre | Horas |
|--------|--------|-------|
| S01 | Catálogos Base | 16h |
| S02 | Flujos y Configuración | 20h |
| S03 | Instancias de Proyecto | 20h |
| S04 | Control de Documentos | 16h |
| S05 | Requisitos Obligatorios | 24h |
| S06 | Documentos UX | 20h |
| S07 | Seeds y QA | 12h |
| **TOTAL** | | **128h** |

**Tiempo estimado:** ~6-8 semanas (asumiendo 20-24h/semana)

---

## 10. DEPENDENCIAS ENTRE SPRINTS

```
S01 (Catálogos Base)
 │
 ├──► S02 (Flujos y Configuración)
 │     │
 │     └──► S03 (Instancias de Proyecto)
 │           │
 │           └──► S07 (Seeds Completos)
 │
 ├──► S04 (Control de Documentos)
 │     │
 │     └──► S06 (Documentos UX)
 │
 └──► S05 (Requisitos Obligatorios)
```

**Paralelos posibles:**
- S04 y S05 pueden ejecutarse en paralelo después de S01
- S06 depende de S03 y S04

---

## 11. RIESGOS

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Migración de datos existentes | Alto | Crear Release "Default" automáticamente |
| Complejidad de validación de requisitos | Medio | Empezar con validación manual, automatizar después |
| Performance con muchos catálogos | Bajo | Índices apropiados, cache si es necesario |
| UX compleja para usuario | Medio | Flujos predefinidos simplifican configuración |

---

## 12. MOCKUPS DE REFERENCIA

| Mockup | Ubicación |
|--------|-----------|
| Vista Documentos Split View | `/mnt/user-data/outputs/mockup_documentos_v31.html` |
| Modal Subida Manual | `/mnt/user-data/outputs/mockup_modal_subir_manual.html` |

---

## 13. DOCUMENTOS DE REFERENCIA

| Documento | Propósito |
|-----------|-----------|
| ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md | Estructura de carpetas estándar |
| ANALISIS_FASES_COMPLETO_PARA_PM.md | 68 subfases, 438 deliverables |
| GUIA_MIGRACION_ESTRUCTURA_VTT.md | Reglas de mapeo |
| schema.prisma | Estado actual de BD |

---

## 14. SIGUIENTE PASO

**AR (Arquitecto)** debe revisar y validar:

1. ¿El modelo de datos propuesto es correcto?
2. ¿Hay conflictos con tablas existentes?
3. ¿Las relaciones son correctas (FK lógicos vs reales)?
4. ¿La estrategia de migración es viable?
5. ¿Los índices propuestos son suficientes?
6. ¿Hay consideraciones de performance?

---

## 15. APROBACIONES PENDIENTES

| Rol | Estado | Fecha |
|-----|--------|-------|
| PM | ✅ Elaborado | 2026-03-24 |
| AR | ⬜ Pendiente | — |
| TL | ⬜ Pendiente | — |
| PO | ⬜ Pendiente | — |

---

**Documento:** BRIEF_PM_VTT_MODELO_DINAMICO_V3.md  
**Versión:** 3.0.0  
**Estado:** 🔄 Pendiente revisión AR
