#!/usr/bin/env python3
"""
Memory Service R1 — Resume Script (Tasks + Dependencies)
=========================================================
Reanuda la carga desde el Paso 4 (tasks) usando los UUIDs ya generados
en VTT_UUIDS_MEMORY_SERVICE.json (Project + Phases + Deliveries ya creados).

Fix aplicado: categoria "chore" reemplazada por equivalente valido.
  - chore (infra/tooling) -> "deployment"
  - chore (repo/docs)     -> "documentation"
  - chore (dev setup)     -> "development"
"""

import os, sys, json, time, urllib.request, urllib.error
from typing import Any

API_URL = os.environ.get("VTT_API_URL", "http://77.42.88.106:3000")
SERVICE_KEY = os.environ.get("VTT_SERVICE_KEY")
if not SERVICE_KEY:
    sys.exit("ERROR: Define VTT_SERVICE_KEY antes de ejecutar.")

UUIDS_FILE = "VTT_UUIDS_MEMORY_SERVICE.json"

# UUIDs fijos
PM_UUID  = "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"
PJM_UUID = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"

USERS = {
    "PM":  PM_UUID,
    "PJM": PJM_UUID,
    "TL":  "92225290-6b6b-4c1f-a940-dcb4262507aa",
    "SA":  "0c128e3b-db3b-4e31-b107-0379b5791233",
    "AR":  "e9403c25-c1f8-4b64-b2ef-f447d53115e2",
    "BE":  "ebbe3cee-abed-4b3b-860d-0a81f632b08a",
    "DB":  "6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7",
    "FE":  "d23c9cd9-a156-433b-8900-94add5488eec",
    "UX":  "a75a1dae-754a-4b6f-a3ff-db8d51f6a91b",
    "DL":  "b3a09269-cded-468c-a475-15a48f203cb0",
    "QA":  "613c9538-658c-45fe-a6d7-c1ea9ff04b78",
    "DO":  "322e3745-9756-4a7c-af11-44b33edef44d",
}

STATUS_PENDING = "335fd9c6-f0d6-4966-a6ea-f518c78bc422"
PRIORITY = {
    "C": "90ec3df2-fac4-40fa-b2ce-29daf0f4956e",
    "H": "1a617554-6319-4c56-826f-8ef49a0ff9cc",
    "M": "d0b619ef-27e7-42d8-8879-41030a602eed",
    "L": "95f2e731-41b9-4a7d-9a43-31f00a4ddd7e",
}

# Categorias validas: development, design, testing, documentation, review, bugfix, deployment
# "chore" NO existe en la API — mapeado a equivalente:
TASKS = [
    # Phase 1 Project Setup (5 / 32h)
    ("MEM-001", "Project Setup", "Project Foundation Ready", "Infra Setup",
     "Coordinar con Admin VM la provision y verificacion de: BD memory_service_db, volumen /root/memory-service-storage/, SERVICE_KEY, Redis prefix mem, firewall puertos 3002/3003, shared-network Docker. Documentar en docs/INFRASTRUCTURE.md.",
     "DO", "deployment", "MEDIUM", 4, "M"),
    ("MEM-002", "Project Setup", "Project Foundation Ready", "Repo Structure",
     "Crear repo Git + estructura V3.1 (phases/00-07, _pm/, docs/, archive/, .claude/agents/). Configurar .gitignore, README, CONTRIBUTING, branch protection, CODEOWNERS, PR templates.",
     "PJM", "documentation", "MEDIUM", 5, "M"),
    ("MEM-003", "Project Setup", "Project Foundation Ready", "Team Onboarding",
     "Crear OPERATIVO_ROL.md por cada uno de los 12 roles + CONTEXTO_ROL_SESION.md. PROJECT_MEMORY.md consolidado. Distribuir acceso a repo + VTT + docs. Reuniones onboarding. Verificar asignaciones en VTT.",
     "PJM", "documentation", "MEDIUM", 14, "M"),
    ("MEM-004", "Project Setup", "Project Foundation Ready", "Tooling Setup",
     "Configurar Node 20 + TypeScript + tsconfig estricto + package.json scripts + .nvmrc + ESLint + Prettier + Husky + lint-staged pre-commit + CI minimo GitHub Actions.",
     "DO", "deployment", "MEDIUM", 4, "M"),
    ("MEM-005", "Project Setup", "Project Foundation Ready", "Project Kickoff",
     "README.md + CONTRIBUTING.md + docs/ARCHITECTURE.md (link a SPEC v1.9) + KICKOFF_MEMORY_SERVICE.md (vision, objetivos, alcance, equipo, roadmap, riesgos, criterios exito). Kickoff call + acta.",
     "PM", "documentation", "MEDIUM", 5, "H"),

    # Phase 2 Discovery (4 / 9h)
    ("MEM-006", "Discovery", "Problem Definition", "Problem Definition",
     "Autorar 4 docs SDLC: 0.3.1 Problem Statement, 0.3.2 User Pain Points (equipo VTT), 0.3.3 Current Solutions (VTM legacy + modulo 5F), 0.3.4 Why Now (urgencia + costos sin trackear).",
     "SA", "documentation", "MEDIUM", 3, "M"),
    ("MEM-007", "Discovery", "Problem Definition", "Problem Validation",
     "Validacion interna del Problem Statement con equipo VTT. Entregable 0.3.5 Problem Validation report con consultas a TL/SA/DL confirmando pain points reales.",
     "PM", "documentation", "LOW", 2, "M"),
    ("MEM-008", "Discovery", "Value Proposition", "Value Proposition",
     "Autorar 5 docs: 0.4.1 VPC, 0.4.2 UVP Statement (1 frase), 0.4.3 Key Differentiators vs VTM/5F, 0.4.4 Target Customer Profile (agentes AI + devs VTT), 0.4.5 Value Hypothesis.",
     "SA", "documentation", "MEDIUM", 3, "M"),
    ("MEM-009", "Discovery", "Value Proposition", "Value Validation",
     "Sign-off de los 5 deliverables 0.4.* tras revision con equipo VTT. Confirmar UVP y diferenciadores antes de Planning.",
     "PM", "documentation", "LOW", 1, "M"),

    # Phase 3 Planning (8 / 23h)
    ("MEM-010", "Planning", "Vision & Objectives", "Vision",
     "Autorar 3 docs: 1.1.1 Vision Statement (1-3 anos), 1.1.2 Mission Statement, 1.1.5 North Star Metric (ej: % sesiones con contexto <500ms).",
     "PM", "documentation", "MEDIUM", 3, "M"),
    ("MEM-011", "Planning", "Vision & Objectives", "Objectives",
     "Autorar 3 docs: 1.1.3 Product Goals SMART, 1.1.4 Success Metrics KPIs (incluye <500ms), 1.1.6 OKRs de feature.",
     "PM", "documentation", "MEDIUM", 2, "M"),
    ("MEM-012", "Planning", "Scope", "Scope",
     "Autorar 6 docs: 1.2.1 Scope Statement, 1.2.2 In-Scope, 1.2.3 Out-of-Scope (LIM-01..09), 1.2.4 MVP Definition, 1.2.5 Future Phases (R2/R3), 1.2.6 Assumptions.",
     "SA", "documentation", "HIGH", 4, "M"),
    ("MEM-013", "Planning", "Stakeholders", "Stakeholders",
     "Autorar 4 docs: 1.3.1 Map, 1.3.2 Register (12 roles + Admin VM + consumidores Runtime/PB/Hook Manager), 1.3.3 RACI Matrix, 1.3.4 Communication Plan.",
     "PJM", "documentation", "LOW", 2, "M"),
    ("MEM-014", "Planning", "Risks", "Risks",
     "Autorar 5 docs: 1.4.1 Register (basado en R1-R12 del HO), 1.4.2 Assessment (matriz prob x impacto), 1.4.3 Mitigation, 1.4.4 Contingency, 1.4.5 Monitoring.",
     "PJM", "documentation", "MEDIUM", 3, "M"),
    ("MEM-015", "Planning", "Timeline", "Timeline",
     "Autorar 4 docs: 1.5.1 Schedule (Gantt 116 tareas), 1.5.5 Dependencies (15 criticas), 1.5.6 Critical Path (MEM-038->MEM-081 hito critico), 1.5.7 Buffer Time.",
     "PJM", "documentation", "HIGH", 4, "M"),
    ("MEM-016", "Planning", "Timeline", "Milestones",
     "Autorar 3 docs: 1.5.2 Milestones, 1.5.3 Phase Breakdown (402h por fase), 1.5.4 Sprint Calendar (fechas S01..S06 + UI-01..04).",
     "PJM", "documentation", "MEDIUM", 3, "M"),
    ("MEM-017", "Planning", "Budget & Resources", "Budget & Resources",
     "Autorar 5 docs: 1.6.1 Estimate (horas por rol), 1.6.2 Cost Breakdown por sprint, 1.6.3 Resource Plan (12 roles), 1.6.4 ROI Analysis, 1.6.5 Budget Tracking.",
     "PM", "documentation", "LOW", 2, "M"),

    # Phase 4 Analysis (8 / 41h)
    ("MEM-018", "Analysis", "Functional Requirements", "Functional Requirements",
     "Autorar 6 docs: 2.1.1 SRS, 2.1.2 Requirements List (RF-XXX sobre 11 endpoints R1), 2.1.3 MoSCoW, 2.1.4 Feature List, 2.1.5 Functional Decomposition, 2.1.6 Approval.",
     "SA", "documentation", "HIGH", 6, "M"),
    ("MEM-019", "Analysis", "Non-Functional Requirements", "Non-Functional Requirements",
     "Autorar 6 docs: 2.2.1 NFR Doc, 2.2.2 Performance (<500ms contractual), 2.2.3 Security (SERVICE_KEY + OWASP), 2.2.4 Scalability, 2.2.5 Availability, 2.2.6 Usability.",
     "AR", "documentation", "HIGH", 4, "M"),
    ("MEM-020", "Analysis", "Use Cases", "Use Cases",
     "Autorar 6 docs: 2.3.1 Use Case Doc, 2.3.2 UML Diagram, 2.3.3 List, 2.3.4 Detailed (import/context/timeline/cost/upload), 2.3.5 Actors, 2.3.6 Relationships.",
     "SA", "documentation", "MEDIUM", 5, "M"),
    ("MEM-021", "Analysis", "User Stories", "User Stories",
     "Autorar 6 docs: 2.4.1 Product Backlog, 2.4.2 User Stories, 2.4.3 Story Map, 2.4.4 Epics, 2.4.5 Estimation, 2.4.6 Sprint Assignment.",
     "SA", "documentation", "HIGH", 8, "M"),
    ("MEM-022", "Analysis", "Business Rules", "Business Rules",
     "Autorar 7 docs: 2.5.1 Doc, 2.5.2 Rules List (BR-XXX), 2.5.3 Validation (zod), 2.5.4 Calculation (costo USD), 2.5.5 Authorization (SERVICE_KEY), 2.5.6 State Transition, 2.5.7 Glossary.",
     "SA", "documentation", "HIGH", 4, "M"),
    ("MEM-023", "Analysis", "User Flows", "User Flows",
     "Autorar 7 docs: 2.6.1 Flow Diagrams, 2.6.2 Happy Path, 2.6.3 Error Flows, 2.6.4 Edge Cases, 2.6.5 User Journey Maps (agentes), 2.6.6 Task Flows, 2.6.7 Navigation Map.",
     "UX", "design", "MEDIUM", 4, "M"),
    ("MEM-024", "Analysis", "Acceptance Criteria", "Acceptance Criteria",
     "Autorar 5 docs: 2.7.1 AC Doc, 2.7.2 Gherkin per Story, 2.7.3 Definition of Done, 2.7.4 Definition of Ready, 2.7.5 Test Scenarios.",
     "SA", "documentation", "HIGH", 6, "M"),
    ("MEM-025", "Analysis", "Traceability Matrix", "Traceability Matrix",
     "Autorar 4 docs: 2.8.1 Matrix completa, 2.8.2 RF->US mapping, 2.8.3 US->Test Cases, 2.8.4 Coverage Report.",
     "SA", "documentation", "MEDIUM", 4, "M"),

    # Phase 5 Design UX/UI (13 / 35h)
    ("MEM-026", "Design UX/UI", "Personas", "Personas",
     "Autorar 6 docs: 3A.2.1 Doc, 3A.2.2 Cards (3-5), 3A.2.3 Primary (TL consultando), 3A.2.4 Secondary (PM cost, BE import), 3A.2.6 Scenarios, 3A.2.8 Jobs to be Done.",
     "UX", "design", "MEDIUM", 3, "M"),
    ("MEM-027", "Design UX/UI", "Information Architecture", "Information Architecture",
     "Autorar 7 docs: 3A.3.1 Site Map (Dashboard/Timeline/Viewer/Import/Cost/Health), 3A.3.2 Navigation, 3A.3.3 Patterns, 3A.3.4 Content Inventory, 3A.3.5 Taxonomy, 3A.3.7 Menu, 3A.3.8 URL Structure.",
     "UX", "design", "MEDIUM", 4, "M"),
    ("MEM-028", "Design UX/UI", "Design System", "Design System",
     "Autorar 9 docs del Design System independiente de VTT: 3A.7.1 Tokens, 3A.7.2 Color, 3A.7.3 Typography, 3A.7.4 Spacing, 3A.7.5 Icons, 3A.7.6 Component Library, 3A.7.7 Documentation, 3A.7.8 Pattern Library, 3A.7.10 Assets.",
     "DL", "design", "MEDIUM", 3, "M"),
    ("MEM-029", "Design UX/UI", "Wireframes", "Wireframes - Dashboard",
     "Wireframes low-fi + mid-fi + desktop de la pagina Dashboard: stats globales, actividad reciente, errores pendientes, KPIs. Flujos conectados.",
     "DL", "design", "HIGH", 4, "M"),
    ("MEM-030", "Design UX/UI", "Wireframes", "Wireframes - Timeline",
     "Wireframes de Agent Timeline con filtros (proyecto, fechas, tipo), paginacion, links a Conversation Viewer.",
     "DL", "design", "MEDIUM", 3, "M"),
    ("MEM-031", "Design UX/UI", "Wireframes", "Wireframes - Viewer",
     "Wireframes + mockups del Conversation Viewer TASK_EXECUTION: turns expandibles, tool calls con archivo + success/error, panel metadata.",
     "DL", "design", "HIGH", 4, "M"),
    ("MEM-032", "Design UX/UI", "Wireframes", "Wireframes - Cost Report",
     "Wireframes + mockups del Cost Report por proyecto y agente: breakdown por workType, semana, top tareas costosas.",
     "DL", "design", "HIGH", 4, "M"),
    ("MEM-033", "Design UX/UI", "Wireframes", "Wireframes - Lista Convs",
     "Wireframes de Lista/Busqueda con filtros (agente, proyecto, fuente, tipo, fechas), paginacion, acciones rapidas.",
     "DL", "design", "MEDIUM", 2, "M"),
    ("MEM-034", "Design UX/UI", "Wireframes", "Wireframes - Import Manual",
     "Wireframes del formulario Import Manual: upload multipart con progreso, selector de fuente, proyecto/agente/tarea, feedback post-import.",
     "DL", "design", "MEDIUM", 2, "M"),
    ("MEM-035", "Design UX/UI", "Wireframes", "Wireframes - Health",
     "Wireframes de Health page: estado BD/storage/Redis, errores pendientes cleanup, metricas de contexto <500ms.",
     "DL", "design", "MEDIUM", 2, "M"),
    ("MEM-036", "Design UX/UI", "Wireframes", "Wireframes - Extras",
     "3A.4.7 Annotations, 3A.4.8 Flows conectados, 3A.4.9 Responsive Breakpoints desktop, 3A.5.5-8 Component/Empty/Error/Loading States.",
     "DL", "design", "LOW", 1, "M"),
    ("MEM-037", "Design UX/UI", "Design Handoff", "Design Handoff - Assets",
     "Exportacion de assets + specs: 3A.9.2 Specs Export (Figma/Zeplin), 3A.9.3 Asset Export (SVG/PNG), 3A.9.4 CSS Variables para FE.",
     "DL", "design", "MEDIUM", 2, "M"),
    ("MEM-038", "Design UX/UI", "Design Handoff", "Design Handoff - Final",
     "HITO CRITICO: 3A.9.1 Handoff Document + 3A.9.5 Redlines con medidas. DESBLOQUEA MEM-081+ (FE arranque). Sin aprobacion, FE NO arranca.",
     "DL", "design", "LOW", 1, "C"),

    # Phase 6 Design Technical (9 / 45h)
    ("MEM-039", "Design Technical", "Solution Architecture", "Solution Architecture",
     "Autorar 7 docs: 3B.1.1 Architecture Doc, 3B.1.2 Context C4 L1, 3B.1.3 Container L2, 3B.1.4 Component L3, 3B.1.5 Tech Stack (Node 20+TS+Express+Prisma+PG+Redis+React), 3B.1.6 Integration Points, 3B.1.7 Data Flow.",
     "AR", "documentation", "HIGH", 6, "M"),
    ("MEM-040", "Design Technical", "Code Architecture", "Code Architecture",
     "Autorar 6 docs: 3B.2.1 Folder Structure (SPEC 3.2), 3B.2.2 Coding Standards, 3B.2.3 Design Patterns, 3B.2.4 Module Deps, 3B.2.5 Naming, 3B.2.6 Error Handling Strategy.",
     "TL", "documentation", "HIGH", 4, "M"),
    ("MEM-041", "Design Technical", "Database Design", "Database Design",
     "Autorar 8 docs: 3B.3.1 ERD (19 tablas+10 catalogos), 3B.3.2 Schema Prisma, 3B.3.3 Table Specs, 3B.3.4 Index Strategy (partial+GIN), 3B.3.5 Data Dictionary, 3B.3.6 Migration Strategy, 3B.3.7 Seed Plan, 3B.3.8 Backup Strategy.",
     "DB", "documentation", "HIGH", 6, "M"),
    ("MEM-042", "Design Technical", "API Design", "API Design",
     "Autorar 11 docs: OpenAPI, Endpoints List (11 R1), R/R Examples, Pagination, Error Codes MEM-ERR-*, Auth (SERVICE_KEY), AuthZ, Rate Limit, Versioning, Postman, Guidelines.",
     "BE", "documentation", "HIGH", 8, "M"),
    ("MEM-043", "Design Technical", "Sequence Diagrams", "Sequence Diagrams",
     "Autorar 6 docs: Sequence Doc, Auth Flow (SERVICE_KEY), Business Flows (import/context/cleanup), Error Flows, Integration Flows (Runtime/PB/Hook Manager), Async Flows.",
     "AR", "documentation", "HIGH", 6, "M"),
    ("MEM-044", "Design Technical", "ADRs", "Architecture Decision Records",
     "Formalizar 48 decisiones (43 D-MEM + 5 D-INT) como ADRs independientes: 3B.6.1 Template, 3B.6.2 Index, 3B.6.3 Documents (1 archivo por decision), 3B.6.4 Decision Log.",
     "TL", "documentation", "MEDIUM", 4, "M"),
    ("MEM-045", "Design Technical", "Security Plan", "Security Plan",
     "Autorar 11 docs: Plan, AuthN (SERVICE_KEY), AuthZ, Data Protection, Encryption, OWASP Top 10, Security Headers, Secrets Management, Input Validation, Security Logging, Incident Response.",
     "AR", "documentation", "HIGH", 4, "M"),
    ("MEM-046", "Design Technical", "Infrastructure Plan", "Infrastructure Plan",
     "Autorar 11 docs: Plan, Diagram (Hetzner 77.42.88.106), Server Specs, Network (shared-network), Env Matrix, Scaling, Backup, DR, Cost, SLA (<500ms), Monitoring Strategy.",
     "DO", "documentation", "MEDIUM", 4, "M"),
    ("MEM-047", "Design Technical", "Technical Estimates", "Technical Estimates",
     "Autorar 9 docs: Estimates (402h), Story Points, Task Breakdown (116), Effort Matrix por rol, Complexity, Risk-adjusted, Dependencies Map (15), Velocity, Capacity.",
     "TL", "documentation", "MEDIUM", 3, "M"),

    # Phase 7 Development S01 (5 / 9h)
    ("MEM-048", "Development", "S01: Schema + Seeds", "DB Schema Prisma completo",
     "Implementar prisma/schema.prisma con 19 tablas + 10 catalogos segun SPEC v1.9 4.1. Constraints: unique(sourceId, externalSessionId), unique(conversationId, turnIndex), unique(turnId, blockIndex), unique(conversationId, entityName). Ejecutar prisma generate.",
     "DB", "development", "HIGH", 3, "H"),
    ("MEM-049", "Development", "S01: Schema + Seeds", "Migraciones + Partial Indexes",
     "prisma migrate deploy. Aplicar partial_indexes.sql: idx_conv_agent_time, idx_conv_task, idx_block_filepath + indice GIN idx_conv_runtime_run (ADDENDUM 5.3).",
     "DB", "development", "MEDIUM", 2, "M"),
    ("MEM-050", "Development", "S01: Schema + Seeds", "Seed Catalogos",
     "prisma/seed.ts con 10 catalogos: SourceCatalog(5), ConversationTypeCatalog(3), ConversationStatusCatalog(4), WorkTypeCatalog(6), BlockTypeCatalog(4), MessageTypeCatalog(6), MessageStatusCatalog(6), PlatformCatalog(5), TopicCatalog(10), PriorityCatalog(3).",
     "DB", "development", "LOW", 1, "M"),
    ("MEM-051", "Development", "S01: Schema + Seeds", "Setup Express + estructura",
     "Crear src/app.ts, src/index.ts, src/config/env.ts. Estructura routes/, controllers/, services/adapters/, middleware/, jobs/, schemas/, utils/ segun SPEC 3.2. Middlewares cors, helmet, body-parser.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-052", "Development", "S01: Schema + Seeds", "Catalog Cache startup",
     "src/services/catalog-cache.service.ts con initCatalogCache() que carga 10 catalogos en Maps al bootstrap. Getters getSourceId, getStatusId, etc. Llamar antes de app.listen().",
     "BE", "development", "LOW", 1, "M"),

    # Phase 7 Development S02 (5 / 12h)
    ("MEM-053", "Development", "S02: Import + Timeline", "POST /import (4 fuentes)",
     "POST /api/conversations/import con 4 adapters (CLI/Web/SDK/ChatGPT). Idempotencia [sourceId, externalSessionId]. Flow PENDING->PROCESSING->IMPORTED. Manejo P2002 -> ALREADY_INDEXED. Catch delega cleanup (AMB-07).",
     "BE", "development", "HIGH", 4, "H"),
    ("MEM-054", "Development", "S02: Import + Timeline", "POST /import-review (VTT_CHANNEL)",
     "POST /api/conversations/import-review multi-agente. Import incremental para Google Docs append-only. primaryAgentId=NULL. Persist ConversationParticipant + AgentMessage. Prefetch catalogos (DB-OBS-03).",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-055", "Development", "S02: Import + Timeline", "POST /upload (manual)",
     "POST /api/conversations/upload publico sin SERVICE_KEY. Recibe multipart, auto-detecta fuente por formato (.jsonl, .json, .md). Delega a flujo interno de /import.",
     "BE", "development", "HIGH", 3, "M"),
    ("MEM-056", "Development", "S02: Import + Timeline", "GET /agents/:id/timeline",
     "GET /api/agents/:id/timeline. Query combina primaryAgentId + ConversationParticipant.agentId. Paginacion cursor startedAt DESC. Filtros: projectId, fechas, conversationType.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-057", "Development", "S02: Import + Timeline", "Error handling + cleanup delegation",
     "Middleware error-handler centralizado + validacion zod. AMB-07: catch NO mueve a ERROR; deja PROCESSING para cleanup job.",
     "BE", "development", "LOW", 1, "M"),

    # Phase 7 Development S03 (5 / 12h)
    ("MEM-058", "Development", "S03: Content + Context", "GET /content (parse storage)",
     "GET /api/conversations/:id/content segun D-MEM-43. Lee archivo completo desde /storage/ (NO de BD). Parsea segun sourceId y retorna turnos con tool calls.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-059", "Development", "S03: Content + Context", "GET /context (<500ms fail-fast)",
     "GET /api/context consumido por Prompt Builder. context.service.ts con Promise.race(queries, timeout(500)). Queries paralelas. Filtra projectId (D-MEM-39). Timeout -> 504 MEM-ERR-504.",
     "BE", "development", "HIGH", 4, "C"),
    ("MEM-060", "Development", "S03: Content + Context", "Classifier deterministico",
     "classifier.service.ts con reglas deterministicas. Detecta topics por keywords en paths+tool calls, workType por patrones, entities de paths. Output {workTypeId, topics, entities, confidence}.",
     "BE", "development", "HIGH", 2, "M"),
    ("MEM-061", "Development", "S03: Content + Context", "Tests performance contexto",
     "Benchmark GET /context con 100 conv x 10 agentes x 5 proyectos. Validar p95 <500ms con k6. Reporte performance con percentiles.",
     "QA", "testing", "MEDIUM", 2, "M"),
    ("MEM-062", "Development", "S03: Content + Context", "Tests classifier",
     "Suite tests classifier: fixtures 20 conv por workType, 30 topics mezclados, edge cases. Assertions workType, topics, entities, confidence > threshold.",
     "QA", "testing", "MEDIUM", 2, "M"),

    # Phase 7 Development S04 (6 / 12h)
    ("MEM-063", "Development", "S04: Adapters + Cleanup", "Adapter CLAUDE_WEB",
     "src/services/adapters/web.adapter.ts. Parsea JSON unico de claude.ai. Extrae metadata + messages + adjuntos. Output formato interno {startedAt, endedAt, turns[]}.",
     "BE", "development", "MEDIUM", 3, "M"),
    ("MEM-064", "Development", "S04: Adapters + Cleanup", "Adapter CHATGPT",
     "src/services/adapters/chatgpt.adapter.ts. Parsea estructura 'mapping' (arbol) de export chatgpt.com. Reconstruye conversacion lineal.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-065", "Development", "S04: Adapters + Cleanup", "Storage writer JSONL",
     "src/services/storage.service.ts con save() TASK y saveReview() REVIEW segun D-MEM-06.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-066", "Development", "S04: Adapters + Cleanup", "Cleanup cron (5 min)",
     "src/jobs/cleanup.job.ts con node-cron cada 5 min. STALE > 10 min, retryCount <= MAX_RETRIES (D-MEM-35, D-MEM-40). Usa statusId del cache.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-067", "Development", "S04: Adapters + Cleanup", "Status transitions handler",
     "Helper transitionStatus(conversationId, fromCode, toCode) con validacion y logging. Usa cache.",
     "BE", "development", "LOW", 1, "M"),
    ("MEM-068", "Development", "S04: Adapters + Cleanup", "Tests adapters",
     "Tests 5 adapters (CLI/Web/SDK/ChatGPT/VTT_CHANNEL) con fixtures JSONL reales. Casos felices + edge cases.",
     "BE", "testing", "MEDIUM", 2, "M"),

    # Phase 7 Development S05 (6 / 11h)
    ("MEM-069", "Development", "S05: Lista + Cost + Dashboard", "GET /conversations (lista)",
     "GET /api/conversations con filtros query: agentId, projectId, taskId, conversationType, sourceCode, fechas, status. Paginacion cursor. Default ultimas 50.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-070", "Development", "S05: Lista + Cost + Dashboard", "GET /projects/:id/cost-report",
     "GET /api/projects/:id/cost-report. Agrega ConversationUsage.costUsd de conversaciones IMPORTED. Agrupa por agente, tarea, workType. Solo SDK tiene costo real.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-071", "Development", "S05: Lista + Cost + Dashboard", "GET /agents/:id/cost-report",
     "GET /api/agents/:id/cost-report. Breakdown del agente por workType, semana, proyecto. Solo SDK con costUsd.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-072", "Development", "S05: Lista + Cost + Dashboard", "GET /dashboard/stats",
     "GET /api/dashboard/stats. Totales globales: conv por source, costo, last 7 dias, errorsToReview (cleanup), agentes activos.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-073", "Development", "S05: Lista + Cost + Dashboard", "GET /health",
     "GET /health publico sin auth. Check BD (SELECT 1), storage (fs.access), Redis (PING). Retorna {status, checks: {db, storage, redis}, version}.",
     "BE", "development", "MEDIUM", 2, "M"),
    ("MEM-074", "Development", "S05: Lista + Cost + Dashboard", "Integration tests endpoints",
     "Smoke tests sobre endpoints S05 con supertest. Happy path + 1 error case por endpoint.",
     "BE", "testing", "LOW", 1, "M"),

    # Phase 7 Development S06 (6 / 14h)
    ("MEM-075", "Development", "S06: Docker + Integration", "Dockerfile + docker-compose",
     "Dockerfile multi-stage Node 20 Alpine. docker-compose.yml con service memory-service (3002, mem_limit 512m, reservation 256m, volume /root/memory-service-storage/:/storage, shared-network, connection_limit=20). COPY prisma ./prisma.",
     "DO", "deployment", "MEDIUM", 2, "M"),
    ("MEM-076", "Development", "S06: Docker + Integration", "CI config",
     ".github/workflows/ci.yml con jobs lint + type-check + test + build en cada PR. Matrix Node 20. Cache npm.",
     "DO", "deployment", "MEDIUM", 2, "M"),
    ("MEM-077", "Development", "S06: Docker + Integration", "Env vars + secrets",
     ".env.example con DATABASE_URL, REDIS_URL, REDIS_PREFIX, SERVICE_KEY, STORAGE_PATH, PORT, NODE_ENV. docs/ENVIRONMENT.md. SERVICE_KEY desde secrets.",
     "DO", "documentation", "LOW", 1, "M"),
    ("MEM-078", "Development", "S06: Docker + Integration", "Integracion Hook Manager VTT",
     "Cliente HTTP Memory -> Hook Manager. Validar que Hook Manager puede llamar POST /import y POST /import-review con SERVICE_KEY. Mock si no esta listo. Documentar contrato.",
     "BE", "development", "HIGH", 4, "M"),
    ("MEM-079", "Development", "S06: Docker + Integration", "E2E test Runtime integration",
     "Test E2E con Mock Runtime: simula Runtime v1.1 con sourceCode=CLAUDE_SDK, externalSessionId={run_id}:r{N}:{agentRole}, platformRefs={runtime_run_id, round, orchestrated:true}. Verifica persistencia + idempotencia.",
     "QA", "testing", "HIGH", 3, "M"),
    ("MEM-080", "Development", "S06: Docker + Integration", "E2E test Prompt Builder integration",
     "Test E2E Mock Prompt Builder: llama GET /context con SERVICE_KEY. Verifica JSON structure, filtrado por projectId (D-MEM-39), latencia <500ms.",
     "QA", "testing", "MEDIUM", 2, "M"),

    # Phase 7 Development UI-01 (5 / 16h)
    ("MEM-081", "Development", "UI-01: Setup + Timeline + Viewer", "Setup React + Vite + Tailwind",
     "Inicializar FE puerto 3003: React 18 + TS + Vite + TailwindCSS. vite.config.ts, tailwind.config.js con tokens DL (MEM-028), tsconfig, estructura src/{components, pages, hooks, services, types, utils}.",
     "FE", "development", "MEDIUM", 2, "M"),
    ("MEM-082", "Development", "UI-01: Setup + Timeline + Viewer", "Routing + layout base",
     "React Router con rutas P0-P3. Layout base con sidebar + header + breadcrumbs. Navegacion segun wireframes DL.",
     "FE", "development", "LOW", 1, "M"),
    ("MEM-083", "Development", "UI-01: Setup + Timeline + Viewer", "Page Timeline agente",
     "Pagina /agents/:id/timeline consumiendo GET /api/agents/:id/timeline. Lista cronologica con filtros, paginacion, click a Viewer. Estados loading/empty/error. Responsive desktop.",
     "FE", "development", "HIGH", 5, "M"),
    ("MEM-084", "Development", "UI-01: Setup + Timeline + Viewer", "Component Conversation Viewer",
     "Componente ConversationViewer type=TASK_EXECUTION. Renderiza turns user/assistant con tool calls expandibles. Consume GET /api/conversations/:id/content. Panel metadata (task, agente, costo, tokens). Syntax highlighting.",
     "FE", "development", "HIGH", 6, "M"),
    ("MEM-085", "Development", "UI-01: Setup + Timeline + Viewer", "Auth context (SERVICE_KEY)",
     "AuthContext con SERVICE_KEY desde VITE_SERVICE_KEY en header Bearer. HTTP client wrapper con interceptor. Manejo 401/403.",
     "FE", "development", "MEDIUM", 2, "M"),

    # Phase 7 Development UI-02 (3 / 12h)
    ("MEM-086", "Development", "UI-02: Dashboard + Cost + Import", "Page Dashboard",
     "Pagina / (Dashboard) consumiendo GET /api/dashboard/stats. Widgets: total conversaciones, costo total, actividad reciente, errores pendientes (link detalle). Responsive desktop.",
     "FE", "development", "HIGH", 4, "M"),
    ("MEM-087", "Development", "UI-02: Dashboard + Cost + Import", "Page Cost Report Proyecto",
     "Pagina /projects/:id/cost consumiendo GET /api/projects/:id/cost-report. Breakdown por agente (tabla) + tarea (tabla) + workType (grafico). Filtro fechas. Export CSV opcional.",
     "FE", "development", "MEDIUM", 4, "M"),
    ("MEM-088", "Development", "UI-02: Dashboard + Cost + Import", "Page Import Manual",
     "Pagina /import con formulario multipart. Inputs: proyecto, agente, tarea, archivo (drop zone). Consume POST /api/conversations/upload. Progress bar + feedback.",
     "FE", "development", "MEDIUM", 4, "M"),

    # Phase 7 Development UI-03 (2 / 10h)
    ("MEM-089", "Development", "UI-03: Viewer REVIEW + Lista", "Page Lista conversaciones",
     "Pagina /conversations consumiendo GET /api/conversations. Tabla ordenable con filtros (agente, proyecto, fuente, tipo, rango, status). Paginacion cursor. Click a Viewer segun tipo.",
     "FE", "development", "HIGH", 5, "M"),
    ("MEM-090", "Development", "UI-03: Viewer REVIEW + Lista", "Component AGENT_REVIEW multi-agente",
     "Componente ConversationViewer type=AGENT_REVIEW con thread multi-agente. Renderiza AgentMessage por agente con badges (role, status OPEN/ACK/IN_PROGRESS/DONE/REJECTED). Replies anidados (inReplyTo). Timeline.",
     "FE", "development", "HIGH", 5, "M"),

    # Phase 7 Development UI-04 (3 / 8h)
    ("MEM-091", "Development", "UI-04: Cost Agente + Health", "Page Cost Report Agente",
     "Pagina /agents/:id/cost consumiendo GET /api/agents/:id/cost-report. Breakdown por workType, semana, proyecto. Graficos de tendencia.",
     "FE", "development", "MEDIUM", 3, "M"),
    ("MEM-092", "Development", "UI-04: Cost Agente + Health", "Page Health",
     "Pagina /health consumiendo GET /health. Estado BD/storage/Redis con indicadores visuales (green/yellow/red). Errores pendientes del cleanup con link a detalle.",
     "FE", "development", "LOW", 2, "M"),
    ("MEM-093", "Development", "UI-04: Cost Agente + Health", "Polish + responsive desktop",
     "Revision UX final: estados empty/loading/error en todas las paginas, responsive breakpoints desktop, accessibility basico (ARIA, keyboard nav), tests componentes Testing Library.",
     "FE", "development", "MEDIUM", 3, "M"),

    # Phase 8 Testing (10 / 60h)
    ("MEM-094", "Testing", "Test Planning", "Test Planning",
     "Test Plan v1.0: Plan completo, Strategy (unit/integration/E2E/performance/security), Scope (11 endpoints+9 paginas), Schedule, Resource Allocation.",
     "QA", "testing", "MEDIUM", 4, "M"),
    ("MEM-095", "Testing", "Test Cases", "Test Cases completos",
     "Test Cases Document: Doc (TC-001..TC-N), Test Case IDs unicos, Test Data (fixtures 5 fuentes), Expected Results. Cubre happy + errores + edge + idempotencia.",
     "QA", "testing", "HIGH", 8, "M"),
    ("MEM-096", "Testing", "Test Environment", "Test Environment setup",
     "Setup ambiente testing: Docker Compose local, Test DB (memory_service_test_db), Test Data Seeding (scripts), Environment documentation.",
     "DO", "testing", "MEDIUM", 4, "M"),
    ("MEM-097", "Testing", "Functional Testing", "Functional Testing",
     "Ejecutar pruebas funcionales: Results por endpoint, Execution Log, Defects Found, Pass/Fail Summary, Screenshots/Evidence. Validar idempotencia, multi-agente, state transitions.",
     "QA", "testing", "HIGH", 8, "M"),
    ("MEM-098", "Testing", "Integration Testing", "Integration Testing",
     "Suite integracion con Jest+supertest: Test Suite, Results, API Contract Tests, Integration Coverage. Cubre BE+BD+storage+Redis.",
     "QA", "testing", "HIGH", 6, "M"),
    ("MEM-099", "Testing", "E2E Testing", "E2E Testing",
     "Suite E2E con Playwright: Test Suite (UI+API), Results, Critical Path Coverage (P0), Visual Regression, Documentation. Tests automatizados en CI.",
     "QA", "testing", "HIGH", 8, "M"),
    ("MEM-100", "Testing", "Performance Testing", "Performance Testing",
     "Performance con k6: Load Test Plan, Results, Stress Results, Performance Metrics, Bottleneck Analysis, Optimization Recommendations. VALIDAR SLA <500ms en /context p95.",
     "QA", "testing", "HIGH", 6, "C"),
    ("MEM-101", "Testing", "Security Testing", "Security Testing",
     "Security testing: Plan, Penetration Test Results, Vulnerability Scan (npm audit + OWASP ZAP), OWASP Compliance, Findings, Remediation Plan, Sign-off. Validar SERVICE_KEY, no leaks en logs.",
     "AR", "testing", "HIGH", 4, "H"),
    ("MEM-102", "Testing", "UAT", "UAT",
     "UAT adaptado con equipo VTT interno: UAT Plan, Test Cases, Results, User Feedback consolidado, UAT Sign-off formal PM.",
     "PM", "testing", "MEDIUM", 4, "M"),
    ("MEM-103", "Testing", "Bug Fixes", "Bug Fixes",
     "Reserva esfuerzo para corregir bugs reportados por QA durante MEM-097..102: Bug Fixes Implemented, Regression Tests, Bug Resolution Report con root causes.",
     "BE", "bugfix", "HIGH", 8, "M"),

    # Phase 9 Deploy (7 / 26h)
    ("MEM-104", "Deploy", "Infrastructure Setup", "Infrastructure Setup",
     "Setup infra produccion: Infrastructure Ready, Servers (Hetzner), Network (shared-network), Security Groups, LB (si aplica), Database Ready, Storage Ready, SSL Certificates.",
     "DO", "deployment", "MEDIUM", 4, "M"),
    ("MEM-105", "Deploy", "CI/CD Configuration", "CI/CD Configuration",
     "Pipeline CI/CD completo: CI Pipeline (build+test+lint), CD Pipeline (deploy staging+prod), Build Scripts, Deploy Scripts (zero-downtime), Environment Configs, Pipeline Documentation.",
     "DO", "deployment", "HIGH", 6, "M"),
    ("MEM-106", "Deploy", "Staging Deploy", "Staging Deploy",
     "Deploy staging automatizado: Deploy exitoso (logs), Staging URL accesible, Migration Run (prisma migrate+seed), Health Check verification.",
     "DO", "deployment", "MEDIUM", 4, "M"),
    ("MEM-107", "Deploy", "Smoke Testing", "Smoke Testing",
     "Smoke tests post-deploy staging: Smoke Test Results, Critical Paths Verified (import/context/UI), Smoke Test Sign-off para aprobar prod.",
     "QA", "testing", "MEDIUM", 3, "M"),
    ("MEM-108", "Deploy", "Production Deploy", "Production Deploy",
     "Deploy produccion: Prod Deploy exitoso, Production URL (77.42.88.106:3002), DNS Configured, SSL Active, Release Notes, Deployment Log.",
     "DO", "deployment", "HIGH", 4, "C"),
    ("MEM-109", "Deploy", "Post-Deploy Monitoring", "Post-Deploy Monitoring",
     "Monitoring post-deploy: Dashboard Grafana, Alerts (latencia/errores/BD), Log Aggregation (ELK/Loki), Metrics Collection (Prometheus), Error Tracking (Sentry), Post-Deploy Report 24h.",
     "DO", "deployment", "MEDIUM", 3, "M"),
    ("MEM-110", "Deploy", "Rollback Plan", "Rollback Plan",
     "Plan rollback documentado: Rollback Plan, Rollback Scripts, Tested en staging, Rollback Runbook, Decision Criteria. Incluye rollback de migraciones Prisma.",
     "TL", "documentation", "MEDIUM", 2, "M"),

    # Phase 10 Operations (6 / 15h)
    ("MEM-111", "Operations", "Monitoring", "Monitoring setup",
     "Monitoring operacional continuo: Uptime Reports (weekly), Performance Reports (p95 /context), Error Reports (cleanup ERROR), Weekly Reports consolidados para PM/TL.",
     "DO", "deployment", "MEDIUM", 3, "M"),
    ("MEM-112", "Operations", "User Support", "User Support docs",
     "Documentacion soporte interno: Support Process (flujo interno VTT), Ticket System (VTT issues), SLA Definitions, Support Metrics.",
     "PM", "documentation", "LOW", 2, "M"),
    ("MEM-113", "Operations", "Bug Fixes Operations", "Bug Fixes Operations playbook",
     "Playbook operaciones: Hotfix Process (flow para bugs criticos), Hotfix Releases process, Bug Tracking procedure (crear issue VTT, task fix con sourceIssueId).",
     "TL", "documentation", "MEDIUM", 2, "M"),
    ("MEM-114", "Operations", "Incremental Improvements", "Incremental Improvements",
     "Proceso mejoras incrementales: Minor Releases process, Feature Flags strategy, A/B Tests framework (futuro), Improvement Backlog priorizado para R2.",
     "PM", "documentation", "MEDIUM", 3, "M"),
    ("MEM-115", "Operations", "Security Updates", "Security Updates",
     "Proceso actualizaciones seguridad: Security Patches process, Dependency Updates (renovate/dependabot), Security Audits periodicos, Vulnerability Reports.",
     "AR", "documentation", "MEDIUM", 2, "M"),
    ("MEM-116", "Operations", "Scaling", "Scaling plan",
     "Plan scaling: Scaling Reports (metricas), Capacity Planning, Auto-scaling Config (si aplica), Cost Optimization. Evaluar cuando R2 requiere migrar a MinIO o split BD.",
     "AR", "documentation", "HIGH", 3, "M"),
]

DEPENDENCIES = [
    ("MEM-006", "MEM-005", "Discovery despues de Kickoff"),
    ("MEM-039", "MEM-025", "Design Technical despues de Analysis"),
    ("MEM-048", "MEM-047", "Development despues de Design Technical"),
    ("MEM-053", "MEM-052", "S02 depende de S01"),
    ("MEM-058", "MEM-057", "S03 depende de S02"),
    ("MEM-063", "MEM-062", "S04 depende de S03"),
    ("MEM-069", "MEM-068", "S05 depende de S04"),
    ("MEM-075", "MEM-074", "S06 depende de S05"),
    ("MEM-081", "MEM-038", "HITO CRITICO DL->FE"),
    ("MEM-086", "MEM-085", "UI-02 depende de UI-01"),
    ("MEM-089", "MEM-088", "UI-03 depende de UI-02"),
    ("MEM-091", "MEM-090", "UI-04 depende de UI-03"),
    ("MEM-094", "MEM-093", "Testing despues de Development"),
    ("MEM-104", "MEM-103", "Deploy despues de Testing"),
    ("MEM-111", "MEM-110", "Operations despues de Deploy"),
]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def auth_token(user_id):
    req = urllib.request.Request(
        f"{API_URL}/api/auth/service-token",
        data=json.dumps({"userId": user_id, "serviceKey": SERVICE_KEY}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())["data"]["token"]


def post(path, body, token):
    req = urllib.request.Request(
        f"{API_URL}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="ignore")
        log(f"ERROR POST {path}: {e.code} — {detail}")
        raise


def extract_id(response):
    if isinstance(response.get("data"), dict) and "id" in response["data"]:
        return response["data"]["id"]
    if "id" in response:
        return response["id"]
    raise ValueError(f"No id en respuesta: {response}")


def main():
    log("Memory Service R1 — RESUME (Tasks + Dependencies)")
    log(f"API: {API_URL}")

    with open(UUIDS_FILE, encoding="utf-8") as f:
        uuids = json.load(f)

    log(f"UUIDs cargados: project={uuids['projectId']}")
    log(f"  Phases: {len(uuids['phases'])} | Deliveries: {len(uuids['deliveries'])}")

    token = auth_token(PJM_UUID)
    log("Token JWT obtenido")

    # Paso 4: Crear 116 Tasks
    log(f"\n=== Paso 4: Crear 116 Tasks ===")
    for (code, phase_name, deliv_name, title, desc, role, cat, cmplx, hours, pri) in TASKS:
        assignee = USERS[role]
        body = {
            "title": title,
            "description": desc,
            "priorityId": PRIORITY[pri],
            "statusId": STATUS_PENDING,
            "assignedToId": assignee,
            "assignedBy": PJM_UUID,
            "category": cat,
            "complexity": cmplx,
            "estimatedHours": hours,
            "createdBy": PJM_UUID,
        }
        t = post(f"/api/phases/{uuids['phases'][phase_name]}/tasks", body, token)
        task_id = extract_id(t)
        uuids["tasks"][code] = task_id
        log(f"  OK {code} [{role} {hours}h {cmplx}] {title}")

        # Asignar al delivery
        deliv_id = uuids["deliveries"][deliv_name]
        try:
            post(f"/api/deliveries/{deliv_id}/tasks/{task_id}", {"assignedBy": PJM_UUID}, token)
        except urllib.error.HTTPError as e:
            log(f"    WARN delivery '{deliv_name}': {e.code}")

    # Paso 6: Crear 15 Dependencies
    log(f"\n=== Paso 6: Crear 15 Dependencies ===")
    for (task_code, dep_code, razon) in DEPENDENCIES:
        task_id = uuids["tasks"][task_code]
        dep_id  = uuids["tasks"][dep_code]
        try:
            post(f"/api/tasks/{task_id}/dependencies", {"dependsOnTaskId": dep_id}, token)
            log(f"  OK {task_code} -> {dep_code} ({razon})")
        except urllib.error.HTTPError as e:
            log(f"  WARN dep {task_code}->{dep_code}: {e.code} — registrar manualmente")

    # Guardar UUIDs completos
    with open(UUIDS_FILE, "w", encoding="utf-8") as f:
        json.dump(uuids, f, indent=2)

    log(f"\nCompletado. UUIDs actualizados en {UUIDS_FILE}")
    log(f"  Tasks:  {len(uuids['tasks'])} creadas")
    log(f"  Deps:   {len(DEPENDENCIES)} procesadas")


if __name__ == "__main__":
    main()
