# TASK INDEX SEED — Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | TASK_INDEX_SEED_MEMORY_SERVICE.md |
| **Versión** | 2.1 |
| **Fecha** | 2026-04-22 |
| **Autor** | PM (Martin Rivas) |
| **Propósito** | Plan de **CREACIÓN desde cero** en VTT. Nada del proyecto existe en el sistema — hay que crear Project + 10 Phases + 65 Deliveries + 116 Tasks + 15 Dependencies. |
| **Audiencia** | PJM (ejecuta creación) · TL (review + asignaciones) |
| **Fuente endpoints** | `PROCESO_ASIGNACION_TAREAS.md` v1.6 |
| **Estado** | ✅ Listo para ejecución de scripts |

---

## CHANGELOG

| Versión | Cambios |
|---------|---------|
| 1.0 | Asumía existencia del proyecto en VTT (UUIDs stale). |
| 2.0 | Regenerado desde cero con scripts POST. Usuarios mapeados incorrectamente al namespace genérico VTT. |
| **2.1** | **Corrección de UUIDs de usuarios:** Memory Service tiene su propio namespace (`memory-service.vtt.ai`). Los 12 roles + 4 agentes adicionales (Product Strategy Analyst, Integration Reviewer, Competitive Intelligence Analyst, Market Research Analyst) quedan correctamente mapeados a sus UUIDs reales del proyecto. AR ya no es fallback — tiene su usuario dedicado. |

---

## 1. ESTADO INICIAL EN VTT

| Entidad | Existe en VTT | Acción |
|---------|:-:|--------|
| Usuarios Memory Service (12 roles + 4 adicionales) | ✅ | Ver §2.3 — usar sus UUIDs como `assigneeId` |
| Catálogo Status | ✅ | Usar sus UUIDs |
| Catálogo Priority | ✅ | Usar sus UUIDs |
| Project "Memory Service" | ❌ | **Crear** con POST |
| Las 10 Phases | ❌ | **Crear** con POST |
| Los 65 Deliveries | ❌ | **Crear** con POST |
| Las 116 Tasks | ❌ | **Crear** con POST |
| Las 15 Dependencies | ❌ | **Crear** con POST |

---

## 2. REFERENCE UUIDs (globales, existen en VTT)

### 2.1 Status UUIDs

| Code | UUID |
|------|------|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

### 2.2 Priority UUIDs

| Code | UUID | Ref |
|------|------|-----|
| critical | `90ec3df2-fac4-40fa-b2ce-29daf0f4956e` | **[C]** |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` | **[H]** |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` | **[M]** |
| low | `95f2e731-41b9-4a7d-9a43-31f00a4ddd7e` | **[L]** |

### 2.3 Mapeo de roles Memory Service → Usuarios VTT

**Usuarios específicos del proyecto Memory Service** (namespace `memory-service.vtt.ai`, password común `VttAgent2026`, `platform_super_admin`):

| Rol Memory Service | UUID | Email |
|--------------------|------|-------|
| **PM** | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` | pm@memory-service.vtt.ai |
| **PJM** | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` | pjm@memory-service.vtt.ai |
| **TL** | `92225290-6b6b-4c1f-a940-dcb4262507aa` | tl@memory-service.vtt.ai |
| **SA** (Solution Analyst) | `0c128e3b-db3b-4e31-b107-0379b5791233` | sa@memory-service.vtt.ai |
| **AR** (Architect) | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | ar@memory-service.vtt.ai |
| **BE** | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | be@memory-service.vtt.ai |
| **DB** | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | db@memory-service.vtt.ai |
| **FE** | `d23c9cd9-a156-433b-8900-94add5488eec` | fe@memory-service.vtt.ai |
| **UX** | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` | ux@memory-service.vtt.ai |
| **DL** | `b3a09269-cded-468c-a475-15a48f203cb0` | dl@memory-service.vtt.ai |
| **QA** | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | qa@memory-service.vtt.ai |
| **DO** | `322e3745-9756-4a7c-af11-44b33edef44d` | do@memory-service.vtt.ai |

**Usuarios adicionales creados para el proyecto** (reserva / reviewers / roles especializados):

| Rol | UUID | Email | Uso previsto |
|-----|------|-------|--------------|
| Product Strategy Analyst | `a43f6bd0-3452-46ea-85ae-78589c071a3e` | product-strategy@memory-service.vtt.ai | Apoyo a PM en Value Proposition, Strategy |
| Integration Reviewer | `f3e358f7-679f-400f-8dd7-df41517bca15` | integration-reviewer@memory-service.vtt.ai | Review de tareas de integración (MEM-078, MEM-079, MEM-080) |
| Competitive Intelligence Analyst | `4ccfe002-ddd3-4df7-bf31-825dcebd576e` | competitive-intel@memory-service.vtt.ai | No usado en R1 (feature interna — subfase 0.2 excluida) |
| Market Research Analyst | `44e7bfb3-2aca-4ac1-820e-0836e95cd718` | market-research@memory-service.vtt.ai | No usado en R1 (feature interna — subfase 0.1 excluida) |

### 2.4 Categorías válidas (POST task)

| Código | Uso |
|--------|-----|
| `development` | Código (backend, frontend, DB) |
| `design` | Wireframes, mockups, design system |
| `testing` | Test planning, QA execution |
| `documentation` | Docs de discovery, planning, analysis, design técnico, ops |
| `deployment` | Docker, CI/CD, deploy |
| `chore` | Setup, tooling, infra |
| `bugfix` | Correcciones post-review |
| `review` | Code/design reviews |

### 2.5 Complexity (MAYÚSCULAS — obligatorio)

`LOW` · `MEDIUM` · `HIGH`

### 2.6 Campos correctos de POST task (VTT-506 lessons)

```json
{
  "title": "string",
  "description": "string (max 2000 chars)",
  "priorityId": "UUID",
  "statusId": "UUID",
  "assignedToId": "UUID",   // NO 'assignedTo' (se ignora silenciosamente)
  "assignedBy": "UUID",
  "category": "development | design | testing | documentation | deployment | chore | bugfix | review",
  "complexity": "LOW | MEDIUM | HIGH",
  "createdBy": "UUID"
}
```

**Errores frecuentes a evitar:**
- `assignedTo` → se ignora · usar `assignedToId`
- `priority_id` → rechazado · usar `priorityId`
- `complexity: "medium"` → rechazado · usar `"MEDIUM"`
- `description > 2000 chars` → 400 `too_big`

---

## 3. PLAN DE CREACIÓN EN VTT (desde cero, sin wizard)

Secuencia de 6 pasos. Cada paso captura UUIDs nuevos que el siguiente consume.

### Paso 1 · Crear Project

```bash
POST http://77.42.88.106:3000/api/projects
Authorization: Bearer $TOKEN
Content-Type: application/json

{
  "name": "Memory Service",
  "code": "MEM",
  "description": "Microservicio independiente de memoria centralizada para agentes IA. Persiste conversaciones, clasifica por reglas, calcula costos y entrega contexto estructurado en <500ms.",
  "projectTypeCode": "SOFTWARE",
  "createdBy": "07a07147-cf5a-4117-8fbd-2fd1ccb95d54"
}
```

**Captura:** `projectId` → guardar en `VTT_UUIDS.json` como `projectId`.

### Paso 2 · Crear 10 Phases

```bash
POST http://77.42.88.106:3000/api/projects/{projectId}/phases
```

| # | Nombre | Order | Descripción |
|---|--------|------:|-------------|
| 1 | Project Setup | 1 | Iniciación + infra + repo + tooling + kickoff |
| 2 | Discovery | 2 | Problem Definition + Value Proposition |
| 3 | Planning | 3 | Vision + Scope + Stakeholders + Risks + Timeline + Budget |
| 4 | Analysis | 4 | FR + NFR + Use Cases + User Stories + Business Rules + Flows + AC + Traceability |
| 5 | Design UX/UI | 5 | Personas + IA + Design System + Wireframes + Mockups + Handoff |
| 6 | Design Technical | 6 | Solution Arch + Code Arch + DB Design + API Design + Seq + ADRs + Security + Infra + Estimates |
| 7 | Development | 7 | S01..S06 (backend) + UI-01..04 (frontend) |
| 8 | Testing | 8 | Test Planning + Cases + Environment + Functional + Integration + E2E + Performance + Security + UAT + Bug Fixes |
| 9 | Deploy | 9 | Infra Setup + CI/CD + Staging + Smoke + Production + Monitoring + Rollback |
| 10 | Operations | 10 | Monitoring + Support + Bug Fixes + Improvements + Security Updates + Scaling |

**Captura:** 10 `phaseId` en `VTT_UUIDS.json` como `phases["Project Setup"]`, `phases["Discovery"]`, etc.

### Paso 3 · Crear 65 Deliveries

```bash
POST http://77.42.88.106:3000/api/deliveries

{
  "phaseId": "{phaseId del Paso 2}",
  "name": "Project Foundation Ready",
  "order": 1,
  "createdBy": "49937318-7a1d-4b83-9b7e-81aa49394d92",
  "description": "Entregable agrupador: infra + repo + tooling + team + kickoff listos"
}
```

Lista completa de los 65 deliveries con su fase asignada (ver §4).

**Captura:** 65 `deliveryId` en `VTT_UUIDS.json` como `deliveries["Project Foundation Ready"]`, etc.

### Paso 4 · Crear 116 Tasks

```bash
POST http://77.42.88.106:3000/api/phases/{phaseId}/tasks

{
  "title": "Infra Setup",
  "description": "Coordinar con Admin VM la provisión y verificación de: BD memory_service_db en shared-postgres, volumen /root/memory-service-storage/, SERVICE_KEY, Redis con prefix mem, firewall puertos 3002/3003, shared-network Docker. Documentar config en docs/INFRASTRUCTURE.md. Confirmar conectividad desde local.",
  "priorityId": "d0b619ef-27e7-42d8-8879-41030a602eed",
  "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
  "assignedToId": "b2e00b9d-a657-4bdb-b982-3dcf1f5b5757",
  "assignedBy": "49937318-7a1d-4b83-9b7e-81aa49394d92",
  "category": "chore",
  "complexity": "MEDIUM",
  "createdBy": "49937318-7a1d-4b83-9b7e-81aa49394d92"
}
```

**Captura:** 116 `taskId` en `VTT_UUIDS.json` como `tasks["MEM-001"]`, `tasks["MEM-002"]`, etc.

> El sistema genera **IDs autonuméricos** (ej: VTT-1, VTT-2). El mapeo "MEM-XXX → VTT-N" se construye en la captura. En los scripts siguientes usar el VTT-N capturado.

### Paso 5 · Asignar Tasks a Deliveries

```bash
POST http://77.42.88.106:3000/api/deliveries/{deliveryId}/tasks/{taskId}

{
  "assignedBy": "49937318-7a1d-4b83-9b7e-81aa49394d92"
}
```

**Validación (RN-010, RN-004):** task y delivery deben estar en la **misma fase**; task no puede estar en dos deliveries a la vez.

### Paso 6 · Crear 15 Dependencies

```bash
POST http://77.42.88.106:3000/api/tasks/{taskId}/dependencies

{
  "dependsOnTaskId": "{otroTaskId}"
}
```

Lista de 15 dependencias críticas (ver §5).

---

## 4. ÍNDICE DE 116 TAREAS POR FASE

### 4.1 Fase 1 · Project Setup (5 tareas · 32h)

**Deliveries en esta fase (1):**
- Project Foundation Ready

| ID | Título | Rol | Cat | Cmplx | h | Pri | Delivery |
|----|--------|-----|-----|:------|--:|:---:|----------|
| MEM-001 | Infra Setup | DO | chore | MEDIUM | 4 | M | Project Foundation Ready |
| MEM-002 | Repo Structure | PJM | chore | MEDIUM | 5 | M | Project Foundation Ready |
| MEM-003 | Team Onboarding | PJM | documentation | MEDIUM | 14 | M | Project Foundation Ready |
| MEM-004 | Tooling Setup | DO | chore | MEDIUM | 4 | M | Project Foundation Ready |
| MEM-005 | Project Kickoff | PM | documentation | MEDIUM | 5 | H | Project Foundation Ready |

**Descripciones:**

- **MEM-001 Infra Setup:** Coordinar con Admin VM la provisión y verificación de: BD memory_service_db en shared-postgres, volumen /root/memory-service-storage/, SERVICE_KEY, Redis con prefix mem, firewall puertos 3002/3003, shared-network Docker. Documentar config en docs/INFRASTRUCTURE.md. Confirmar conectividad desde local.
- **MEM-002 Repo Structure:** Crear repo Git del proyecto (multi-repo pendiente de definir). Inicializar estructura V3.1: phases/00-discovery a phases/07-operations, _pm/, docs/, archive/, .claude/agents/. Configurar .gitignore, README, CONTRIBUTING, branch protection en main, CODEOWNERS, PR templates.
- **MEM-003 Team Onboarding:** Onboarding operativo de los 12 roles: crear OPERATIVO_ROL.md por rol, CONTEXTO_ROL_SESION.md por rol activo, PROJECT_MEMORY.md consolidado. Distribuir acceso a repo + VTT API + docs. Reuniones onboarding por rol. Verificar asignaciones en VTT.
- **MEM-004 Tooling Setup:** Configurar base: Node 20 + TypeScript con tsconfig estricto, package.json con scripts (dev, build, start, test, lint, format, migrate, seed), .nvmrc, ESLint, Prettier, Husky + lint-staged pre-commit, CI mínimo en GitHub Actions.
- **MEM-005 Project Kickoff:** Cierre formal de iniciación: README.md, CONTRIBUTING.md, docs/ARCHITECTURE.md (link a SPEC v1.9), KICKOFF_MEMORY_SERVICE.md (visión, objetivos, alcance, equipo, roadmap, riesgos, criterios de éxito). Kickoff call + acta con compromisos por rol.

### 4.2 Fase 2 · Discovery (4 tareas · 9h)

**Deliveries (2):** Problem Definition · Value Proposition

| ID | Título | Rol | Cat | Cmplx | h | Pri | Delivery | Produces |
|----|--------|-----|-----|:------|--:|:---:|----------|----------|
| MEM-006 | Problem Definition | SA | documentation | MEDIUM | 3 | M | Problem Definition | 0.3.1, 0.3.2, 0.3.3, 0.3.4 |
| MEM-007 | Problem Validation | PM | documentation | LOW | 2 | M | Problem Definition | 0.3.5 |
| MEM-008 | Value Proposition | SA | documentation | MEDIUM | 3 | M | Value Proposition | 0.4.1..0.4.5 |
| MEM-009 | Value Validation | PM | documentation | LOW | 1 | M | Value Proposition | Sign-off 0.4.* |

**Descripciones:**

- **MEM-006 Problem Definition:** Autorar 4 docs SDLC: 0.3.1 Problem Statement, 0.3.2 User Pain Points (equipo VTT), 0.3.3 Current Solutions (VTM legacy, módulo 5F), 0.3.4 Why Now (urgencia + costos sin trackear).
- **MEM-007 Problem Validation:** Validación interna del Problem Statement con equipo VTT. Entregable 0.3.5 con consultas a TL, SA, DL confirmando pain points reales y priorizados.
- **MEM-008 Value Proposition:** Autorar 5 docs: 0.4.1 VPC, 0.4.2 UVP Statement (1 frase), 0.4.3 Key Differentiators vs VTM legacy y submódulo 5F, 0.4.4 Target Customer Profile (agentes AI + devs VTT), 0.4.5 Value Hypothesis.
- **MEM-009 Value Validation:** Sign-off de 0.4.* tras revisión con equipo VTT interno. Confirmar UVP y diferenciadores antes de Planning.

### 4.3 Fase 3 · Planning (8 tareas · 23h)

**Deliveries (6):** Vision & Objectives · Scope · Stakeholders · Risks · Timeline · Budget & Resources

| ID | Título | Rol | Cat | Cmplx | h | Pri | Delivery |
|----|--------|-----|-----|:------|--:|:---:|----------|
| MEM-010 | Vision | PM | documentation | MEDIUM | 3 | M | Vision & Objectives |
| MEM-011 | Objectives | PM | documentation | MEDIUM | 2 | M | Vision & Objectives |
| MEM-012 | Scope | SA | documentation | HIGH | 4 | M | Scope |
| MEM-013 | Stakeholders | PJM | documentation | LOW | 2 | M | Stakeholders |
| MEM-014 | Risks | PJM | documentation | MEDIUM | 3 | M | Risks |
| MEM-015 | Timeline | PJM | documentation | HIGH | 4 | M | Timeline |
| MEM-016 | Milestones | PJM | documentation | MEDIUM | 3 | M | Timeline |
| MEM-017 | Budget & Resources | PM | documentation | LOW | 2 | M | Budget & Resources |

**Descripciones:**

- **MEM-010 Vision:** Autorar 1.1.1 Vision Statement (1-3 años), 1.1.2 Mission Statement, 1.1.5 North Star Metric.
- **MEM-011 Objectives:** Autorar 1.1.3 Product Goals SMART, 1.1.4 Success Metrics KPIs (incluye `<500ms`), 1.1.6 OKRs de feature.
- **MEM-012 Scope:** Autorar 1.2.1 Scope Statement, 1.2.2 In-Scope, 1.2.3 Out-of-Scope, 1.2.4 MVP Definition, 1.2.5 Future Phases, 1.2.6 Assumptions.
- **MEM-013 Stakeholders:** Autorar 1.3.1 Map, 1.3.2 Register, 1.3.3 RACI, 1.3.4 Communication Plan.
- **MEM-014 Risks:** Autorar 1.4.1 Register, 1.4.2 Assessment, 1.4.3 Mitigation, 1.4.4 Contingency, 1.4.5 Monitoring.
- **MEM-015 Timeline:** Autorar 1.5.1 Schedule, 1.5.5 Dependencies, 1.5.6 Critical Path (MEM-038 → MEM-081), 1.5.7 Buffer.
- **MEM-016 Milestones:** Autorar 1.5.2 Milestones, 1.5.3 Phase Breakdown, 1.5.4 Sprint Calendar.
- **MEM-017 Budget & Resources:** Autorar 1.6.1 Estimate, 1.6.2 Cost Breakdown, 1.6.3 Resource Plan, 1.6.4 ROI, 1.6.5 Budget Tracking.

### 4.4 Fase 4 · Analysis (8 tareas · 41h)

**Deliveries (8):** Functional Requirements · NFR · Use Cases · User Stories · Business Rules · User Flows · Acceptance Criteria · Traceability Matrix

| ID | Título | Rol | Cat | Cmplx | h | Pri | Delivery |
|----|--------|-----|-----|:------|--:|:---:|----------|
| MEM-018 | Functional Requirements | SA | documentation | HIGH | 6 | M | Functional Requirements |
| MEM-019 | Non-Functional Requirements | AR | documentation | HIGH | 4 | M | Non-Functional Requirements |
| MEM-020 | Use Cases | SA | documentation | MEDIUM | 5 | M | Use Cases |
| MEM-021 | User Stories | SA | documentation | HIGH | 8 | M | User Stories |
| MEM-022 | Business Rules | SA | documentation | HIGH | 4 | M | Business Rules |
| MEM-023 | User Flows | UX | design | MEDIUM | 4 | M | User Flows |
| MEM-024 | Acceptance Criteria | SA | documentation | HIGH | 6 | M | Acceptance Criteria |
| MEM-025 | Traceability Matrix | SA | documentation | MEDIUM | 4 | M | Traceability Matrix |

**Descripciones:**

- **MEM-018 Functional Requirements:** Autorar 2.1.1 SRS, 2.1.2 Requirements List (RF-XXX sobre 11 endpoints R1), 2.1.3 MoSCoW, 2.1.4 Feature List, 2.1.5 Functional Decomposition, 2.1.6 Approval.
- **MEM-019 Non-Functional Requirements:** Autorar 2.2.1 NFR Doc, 2.2.2 Performance (`<500ms` contractual), 2.2.3 Security (SERVICE_KEY + OWASP), 2.2.4 Scalability, 2.2.5 Availability, 2.2.6 Usability.
- **MEM-020 Use Cases:** Autorar 2.3.1 Doc, 2.3.2 UML Diagram, 2.3.3 List, 2.3.4 Detailed (import, context, timeline, cost, upload), 2.3.5 Actor Definitions, 2.3.6 Relationships.
- **MEM-021 User Stories:** Autorar 2.4.1 Product Backlog, 2.4.2 User Stories, 2.4.3 Story Map, 2.4.4 Epics, 2.4.5 Estimation, 2.4.6 Sprint Assignment.
- **MEM-022 Business Rules:** Autorar 2.5.1 Doc, 2.5.2 Rules List, 2.5.3 Validation (zod), 2.5.4 Calculation (costo USD), 2.5.5 Authorization (SERVICE_KEY), 2.5.6 State Transition (PENDING→PROCESSING→IMPORTED/ERROR), 2.5.7 Glossary.
- **MEM-023 User Flows:** Autorar 2.6.1..2.6.7 (Diagrams, Happy Path, Error, Edge Cases, Journey Maps agentes, Task Flows, Navigation Map UI).
- **MEM-024 Acceptance Criteria:** Autorar 2.7.1 Doc, 2.7.2 Gherkin por story, 2.7.3 DoD, 2.7.4 DoR, 2.7.5 Test Scenarios.
- **MEM-025 Traceability Matrix:** Autorar 2.8.1 Matrix, 2.8.2 RF→US, 2.8.3 US→Test Cases, 2.8.4 Coverage Report.

### 4.5 Fase 5 · Design UX/UI (13 tareas · 35h)

**Deliveries (6):** Personas · Information Architecture · Design System · Wireframes · Mockups UI Design · Design Handoff

| ID | Título | Rol | Cat | Cmplx | h | Pri | Delivery |
|----|--------|-----|-----|:------|--:|:---:|----------|
| MEM-026 | Personas | UX | design | MEDIUM | 3 | M | Personas |
| MEM-027 | Information Architecture | UX | design | MEDIUM | 4 | M | Information Architecture |
| MEM-028 | Design System | DL | design | MEDIUM | 3 | M | Design System |
| MEM-029 | Wireframes — Dashboard | DL | design | HIGH | 4 | M | Wireframes |
| MEM-030 | Wireframes — Timeline | DL | design | MEDIUM | 3 | M | Wireframes |
| MEM-031 | Wireframes — Viewer | DL | design | HIGH | 4 | M | Wireframes |
| MEM-032 | Wireframes — Cost Report | DL | design | HIGH | 4 | M | Wireframes |
| MEM-033 | Wireframes — Lista Convs | DL | design | MEDIUM | 2 | M | Wireframes |
| MEM-034 | Wireframes — Import Manual | DL | design | MEDIUM | 2 | M | Wireframes |
| MEM-035 | Wireframes — Health | DL | design | MEDIUM | 2 | M | Wireframes |
| MEM-036 | Wireframes — Extras | DL | design | LOW | 1 | M | Wireframes |
| MEM-037 | Design Handoff — Assets | DL | design | MEDIUM | 2 | M | Design Handoff |
| **MEM-038** 🚨 | **Design Handoff — Final** | DL | design | LOW | 1 | **C** | Design Handoff |

> 🚨 **MEM-038 = HITO CRÍTICO** con priority CRITICAL. Bloquea MEM-081+ (FE arranque).

**Descripciones (compactas):**

- **MEM-026 Personas:** 6 docs: Personas Doc, Cards (3-5), Primary (TL consultando), Secondary (PM cost, BE import), Scenarios, Jobs to be Done.
- **MEM-027 IA:** 7 docs: Site Map (Dashboard, Timeline, Viewer, Import, Cost, Health), Navigation, Patterns, Content Inventory, Taxonomy, Menu, URL Structure.
- **MEM-028 Design System:** 9 docs: Tokens independientes de VTT, Color, Typography, Spacing, Icons, Component Library, Docs, Pattern Library, Assets.
- **MEM-029..035 Wireframes:** Low-fi + mid-fi + desktop de cada página del UI (Dashboard, Timeline, Viewer, Cost Report, Lista Convs, Import Manual, Health).
- **MEM-036 Wireframes Extras:** Annotations, Flows conectados, Responsive Breakpoints desktop, Component/Empty/Error/Loading States.
- **MEM-037 Design Handoff Assets:** 3A.9.2 Specs Export, 3A.9.3 Asset Export, 3A.9.4 CSS Variables.
- **MEM-038 Design Handoff Final 🚨:** HITO CRÍTICO: 3A.9.1 Handoff Doc + 3A.9.5 Redlines. DESBLOQUEA MEM-081+ (FE).

### 4.6 Fase 6 · Design Technical (9 tareas · 45h)

**Deliveries (9):** Solution Architecture · Code Architecture · Database Design · API Design · Sequence Diagrams · ADRs · Security Plan · Infrastructure Plan · Technical Estimates

| ID | Título | Rol | Cat | Cmplx | h | Pri | Delivery |
|----|--------|-----|-----|:------|--:|:---:|----------|
| MEM-039 | Solution Architecture | AR | documentation | HIGH | 6 | M | Solution Architecture |
| MEM-040 | Code Architecture | TL | documentation | HIGH | 4 | M | Code Architecture |
| MEM-041 | Database Design | DB | documentation | HIGH | 6 | M | Database Design |
| MEM-042 | API Design | BE | documentation | HIGH | 8 | M | API Design |
| MEM-043 | Sequence Diagrams | AR | documentation | HIGH | 6 | M | Sequence Diagrams |
| MEM-044 | ADRs | TL | documentation | MEDIUM | 4 | M | ADRs |
| MEM-045 | Security Plan | AR | documentation | HIGH | 4 | M | Security Plan |
| MEM-046 | Infrastructure Plan | DO | documentation | MEDIUM | 4 | M | Infrastructure Plan |
| MEM-047 | Technical Estimates | TL | documentation | MEDIUM | 3 | M | Technical Estimates |

**Descripciones:**

- **MEM-039 Solution Architecture:** 7 docs: Arch Doc, C4 L1-L3 diagrams, Tech Stack, Integration Points, Data Flow.
- **MEM-040 Code Architecture:** 6 docs: Folder Structure, Coding Standards, Design Patterns, Module Deps, Naming, Error Handling.
- **MEM-041 Database Design:** 8 docs: ERD (19 tablas + 10 catálogos), Schema Prisma, Table Specs, Index Strategy (partial + GIN), Data Dictionary, Migration Strategy, Seed Plan, Backup.
- **MEM-042 API Design:** 11 docs: OpenAPI, Endpoints (11 R1), R/R Examples, Pagination, Error Codes (MEM-ERR-*), Auth (SERVICE_KEY), AuthZ, Rate Limit, Versioning, Postman, Guidelines.
- **MEM-043 Sequence Diagrams:** 6 docs: Doc, Auth Flow, Business Flows (import, context, cleanup), Error Flows, Integration Flows (Runtime, PB, Hook Manager), Async Flows.
- **MEM-044 ADRs:** Formalizar 48 decisiones (43 D-MEM + 5 D-INT) como ADRs. 4 docs: Template, Index, Documents individuales, Decision Log.
- **MEM-045 Security Plan:** 11 docs: Plan, AuthN (SERVICE_KEY), AuthZ, Data Protection, Encryption, OWASP, Headers, Secrets, Input Validation, Logging, Incident Response.
- **MEM-046 Infrastructure Plan:** 11 docs: Plan, Diagram (Hetzner 77.42.88.106), Server Specs, Network (shared-network), Env Matrix, Scaling, Backup, DR, Cost, SLA (`<500ms`), Monitoring.
- **MEM-047 Technical Estimates:** 9 docs: Estimates (381h), Story Points, Task Breakdown, Effort Matrix, Complexity, Risk-adjusted, Dependencies Map (15), Velocity, Capacity.

### 4.7 Fase 7 · Development (46 tareas · 116h)

**Deliveries (10):** S01: Schema + Seeds · S02: Import + Timeline · S03: Content + Context · S04: Adapters + Cleanup · S05: Lista + Cost + Dashboard · S06: Docker + Integration · UI-01: Setup + Timeline + Viewer · UI-02: Dashboard + Cost + Import · UI-03: Viewer REVIEW + Lista · UI-04: Cost Agente + Health

#### S01 (5 tareas · 9h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-048 | DB Schema Prisma completo | DB | development | HIGH | 3 | **H** |
| MEM-049 | Migraciones + Partial Indexes | DB | development | MEDIUM | 2 | M |
| MEM-050 | Seed Catálogos | DB | development | LOW | 1 | M |
| MEM-051 | Setup Express + estructura | BE | development | MEDIUM | 2 | M |
| MEM-052 | Catalog Cache startup | BE | development | LOW | 1 | M |

- **MEM-048:** `prisma/schema.prisma` con 19 tablas + 10 catálogos. Constraints: `@@unique([sourceId, externalSessionId])`, `@@unique([conversationId, turnIndex])`, `@@unique([turnId, blockIndex])`, `@@unique([conversationId, entityName])`. Ejecutar `prisma generate`.
- **MEM-049:** `prisma migrate deploy`. Aplicar `partial_indexes.sql`: `idx_conv_agent_time`, `idx_conv_task`, `idx_block_filepath` + índice GIN `idx_conv_runtime_run` (ADDENDUM §5.3).
- **MEM-050:** `prisma/seed.ts` con 10 catálogos: SourceCatalog(5), ConversationTypeCatalog(3), ConversationStatusCatalog(4), WorkTypeCatalog(6), BlockTypeCatalog(4), MessageTypeCatalog(6), MessageStatusCatalog(6), PlatformCatalog(5), TopicCatalog(10), PriorityCatalog(3).
- **MEM-051:** `src/app.ts`, `src/index.ts`, `src/config/env.ts`. Estructura: routes/, controllers/, services/adapters/, middleware/, jobs/, schemas/, utils/.
- **MEM-052:** `src/services/catalog-cache.service.ts` con `initCatalogCache()` antes de `app.listen()`. Getters por cada catálogo.

#### S02 (5 tareas · 12h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-053 | POST /import (4 fuentes) | BE | development | HIGH | 4 | **H** |
| MEM-054 | POST /import-review (VTT_CHANNEL) | BE | development | MEDIUM | 2 | M |
| MEM-055 | POST /upload (manual) | BE | development | HIGH | 3 | M |
| MEM-056 | GET /agents/:id/timeline | BE | development | MEDIUM | 2 | M |
| MEM-057 | Error handling + cleanup delegation | BE | development | LOW | 1 | M |

- **MEM-053:** Endpoint con 4 adapters. Idempotencia [sourceId, externalSessionId]. Status PENDING→PROCESSING→IMPORTED. P2002 → ALREADY_INDEXED. Catch delega cleanup (AMB-07).
- **MEM-054:** Import incremental multi-agente. primaryAgentId=NULL. Persist ConversationParticipant + AgentMessage. Prefetch catálogos (DB-OBS-03).
- **MEM-055:** Endpoint público sin SERVICE_KEY. Auto-detecta fuente por formato. Delega a flujo interno.
- **MEM-056:** Query combina primaryAgentId + participants. Paginación cursor startedAt DESC.
- **MEM-057:** Middleware error-handler + zod. AMB-07: catch no mueve a ERROR, delega a cleanup.

#### S03 (5 tareas · 12h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-058 | GET /content (parse storage) | BE | development | MEDIUM | 2 | M |
| MEM-059 | GET /context (<500ms) | BE | development | HIGH | 4 | **C** |
| MEM-060 | Classifier determinístico | BE | development | HIGH | 2 | M |
| MEM-061 | Tests performance contexto | QA | testing | MEDIUM | 2 | M |
| MEM-062 | Tests classifier | QA | testing | MEDIUM | 2 | M |

- **MEM-058:** D-MEM-43. NO lee BD; parsea archivo desde /storage/ con adapter apropiado.
- **MEM-059:** `context.service.ts` con `Promise.race(queries, timeout(500))`. Queries paralelas. SIEMPRE filtra projectId (D-MEM-39). Timeout → 504 MEM-ERR-504.
- **MEM-060:** Reglas determinísticas. Topics por keywords en paths + tool calls. WorkType por patrones. Entities de paths.
- **MEM-061:** Benchmark con 100 conv × 10 agentes × 5 proyectos. p95 `<500ms` con k6.
- **MEM-062:** Fixtures 20 conv por workType, 30 topics mezclados, edge cases.

#### S04 (6 tareas · 12h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-063 | Adapter CLAUDE_WEB | BE | development | MEDIUM | 3 | M |
| MEM-064 | Adapter CHATGPT | BE | development | MEDIUM | 2 | M |
| MEM-065 | Storage writer JSONL | BE | development | MEDIUM | 2 | M |
| MEM-066 | Cleanup cron (5 min) | BE | development | MEDIUM | 2 | M |
| MEM-067 | Status transitions handler | BE | development | LOW | 1 | M |
| MEM-068 | Tests adapters | BE | testing | MEDIUM | 2 | M |

- **MEM-063:** `adapters/web.adapter.ts` parsea JSON único de claude.ai.
- **MEM-064:** `adapters/chatgpt.adapter.ts` parsea estructura `mapping`.
- **MEM-065:** `storage.service.ts` con save() TASK y saveReview() REVIEW (D-MEM-06).
- **MEM-066:** `jobs/cleanup.job.ts` node-cron cada 5 min. STALE > 10 min. retryCount <= 3 (D-MEM-35, D-MEM-40).
- **MEM-067:** Helper `transitionStatus` con cache.
- **MEM-068:** Tests 5 adapters con fixtures reales + edge cases.

#### S05 (6 tareas · 11h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-069 | GET /conversations (lista) | BE | development | MEDIUM | 2 | M |
| MEM-070 | GET /projects/:id/cost-report | BE | development | MEDIUM | 2 | M |
| MEM-071 | GET /agents/:id/cost-report | BE | development | MEDIUM | 2 | M |
| MEM-072 | GET /dashboard/stats | BE | development | MEDIUM | 2 | M |
| MEM-073 | GET /health | BE | development | MEDIUM | 2 | M |
| MEM-074 | Integration tests endpoints | BE | testing | LOW | 1 | M |

- **MEM-069:** Filtros: agentId, projectId, taskId, conversationType, sourceCode, fechas, status. Paginación cursor.
- **MEM-070:** Agrega costUsd. Agrupa por agente/tarea/workType. Solo SDK con costo real.
- **MEM-071:** Breakdown por workType, semana, proyecto.
- **MEM-072:** Totales globales: conv por source, costo, last 7 días, errorsToReview, agentes activos.
- **MEM-073:** Check BD, storage, Redis. Retorna `{status, checks, version}`.
- **MEM-074:** Smoke tests sobre endpoints S05 con supertest.

#### S06 (6 tareas · 14h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-075 | Dockerfile + docker-compose | DO | deployment | MEDIUM | 2 | M |
| MEM-076 | CI config | DO | deployment | MEDIUM | 2 | M |
| MEM-077 | Env vars + secrets | DO | deployment | LOW | 1 | M |
| MEM-078 | Integración Hook Manager VTT | BE | development | HIGH | 4 | M |
| MEM-079 | E2E test Runtime integration | QA | testing | HIGH | 3 | M |
| MEM-080 | E2E test Prompt Builder integration | QA | testing | MEDIUM | 2 | M |

- **MEM-075:** Dockerfile multi-stage + docker-compose.yml con mem_limit 512m, volume /root/memory-service-storage/:/storage, shared-network.
- **MEM-076:** `.github/workflows/ci.yml` con lint + type-check + test + build.
- **MEM-077:** `.env.example`, `docs/ENVIRONMENT.md`. SERVICE_KEY desde secrets.
- **MEM-078:** Cliente HTTP Memory → Hook Manager. Validar Hook Manager llama POST /import y /import-review con SERVICE_KEY. Mock si no listo.
- **MEM-079:** Mock Runtime con sourceCode=CLAUDE_SDK, externalSessionId compuesto, platformRefs. Verifica persistencia + idempotencia.
- **MEM-080:** Mock PB llama GET /context con SERVICE_KEY. Verifica JSON structure, filtrado projectId, latencia `<500ms`.

#### UI-01 (5 tareas · 16h)

🚨 **Bloqueo:** MEM-081..093 NO arrancan hasta MEM-038 `task_approved`.

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-081 | Setup React + Vite + Tailwind | FE | development | MEDIUM | 2 | M |
| MEM-082 | Routing + layout base | FE | development | LOW | 1 | M |
| MEM-083 | Page Timeline agente | FE | development | HIGH | 5 | M |
| MEM-084 | Component Conversation Viewer | FE | development | HIGH | 6 | M |
| MEM-085 | Auth context (SERVICE_KEY) | FE | development | MEDIUM | 2 | M |

- **MEM-081:** React 18 + TS + Vite + TailwindCSS puerto 3003. tailwind.config.js con tokens DL.
- **MEM-082:** React Router + Layout con sidebar + header + breadcrumbs.
- **MEM-083:** `/agents/:id/timeline` consumiendo API. Filtros, paginación, estados loading/empty/error.
- **MEM-084:** `<ConversationViewer type='TASK_EXECUTION'>` con turns + tool calls expandibles + metadata panel.
- **MEM-085:** AuthContext con VITE_SERVICE_KEY en header Bearer. HTTP client wrapper + interceptor.

#### UI-02 (3 tareas · 12h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-086 | Page Dashboard | FE | development | HIGH | 4 | M |
| MEM-087 | Page Cost Report Proyecto | FE | development | MEDIUM | 4 | M |
| MEM-088 | Page Import Manual | FE | development | MEDIUM | 4 | M |

- **MEM-086:** `/` con widgets de stats globales, actividad reciente, errores.
- **MEM-087:** `/projects/:id/cost` con breakdown por agente/tarea/workType + filtro fechas.
- **MEM-088:** `/import` con formulario multipart drop zone + progress + feedback.

#### UI-03 (2 tareas · 10h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-089 | Page Lista conversaciones | FE | development | HIGH | 5 | M |
| MEM-090 | Component AGENT_REVIEW | FE | development | HIGH | 5 | M |

- **MEM-089:** `/conversations` con tabla ordenable + filtros (agente, proyecto, fuente, tipo, fechas, status) + paginación.
- **MEM-090:** `<ConversationViewer type='AGENT_REVIEW'>` con thread multi-agente, badges, replies anidados.

#### UI-04 (3 tareas · 8h)

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-091 | Page Cost Report Agente | FE | development | MEDIUM | 3 | M |
| MEM-092 | Page Health | FE | development | LOW | 2 | M |
| MEM-093 | Polish + responsive desktop | FE | development | MEDIUM | 3 | M |

- **MEM-091:** `/agents/:id/cost` con breakdown workType + semana + proyecto + gráficos.
- **MEM-092:** `/health` con estado BD/storage/Redis + indicadores visuales.
- **MEM-093:** Estados empty/loading/error + responsive desktop + accessibility básico + tests Testing Library.

### 4.8 Fase 8 · Testing (10 tareas · 60h)

**Deliveries (10):** Test Planning · Test Cases · Test Environment · Functional Testing · Integration Testing · E2E Testing · Performance Testing · Security Testing · UAT · Bug Fixes

| ID | Título | Rol | Cat | Cmplx | h | Pri | Delivery |
|----|--------|-----|-----|:------|--:|:---:|----------|
| MEM-094 | Test Planning | QA | testing | MEDIUM | 4 | M | Test Planning |
| MEM-095 | Test Cases completos | QA | testing | HIGH | 8 | M | Test Cases |
| MEM-096 | Test Environment setup | DO | testing | MEDIUM | 4 | M | Test Environment |
| MEM-097 | Functional Testing | QA | testing | HIGH | 8 | M | Functional Testing |
| MEM-098 | Integration Testing | QA | testing | HIGH | 6 | M | Integration Testing |
| MEM-099 | E2E Testing | QA | testing | HIGH | 8 | M | E2E Testing |
| MEM-100 | Performance Testing | QA | testing | HIGH | 6 | **C** | Performance Testing |
| MEM-101 | Security Testing | AR | testing | HIGH | 4 | **H** | Security Testing |
| MEM-102 | UAT | PM | testing | MEDIUM | 4 | M | UAT |
| MEM-103 | Bug Fixes | BE | bugfix | HIGH | 8 | M | Bug Fixes |

Descripciones: ver §3.8 de `CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md` o `CONSOLIDADO_MEMORY_SERVICE_R1.md §3.7`.

### 4.9 Fase 9 · Deploy (7 tareas · 26h)

**Deliveries (7):** Infrastructure Setup · CI/CD Configuration · Staging Deploy · Smoke Testing · Production Deploy · Post-Deploy Monitoring · Rollback Plan

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-104 | Infrastructure Setup | DO | deployment | MEDIUM | 4 | M |
| MEM-105 | CI/CD Configuration | DO | deployment | HIGH | 6 | M |
| MEM-106 | Staging Deploy | DO | deployment | MEDIUM | 4 | M |
| MEM-107 | Smoke Testing | QA | testing | MEDIUM | 3 | M |
| MEM-108 | Production Deploy | DO | deployment | HIGH | 4 | **C** |
| MEM-109 | Post-Deploy Monitoring | DO | deployment | MEDIUM | 3 | M |
| MEM-110 | Rollback Plan | TL | documentation | MEDIUM | 2 | M |

### 4.10 Fase 10 · Operations (6 tareas · 15h)

**Deliveries (6):** Monitoring · User Support · Bug Fixes Operations · Incremental Improvements · Security Updates · Scaling

| ID | Título | Rol | Cat | Cmplx | h | Pri |
|----|--------|-----|-----|:------|--:|:---:|
| MEM-111 | Monitoring setup | DO | deployment | MEDIUM | 3 | M |
| MEM-112 | User Support docs | PM | documentation | LOW | 2 | M |
| MEM-113 | Bug Fixes Operations playbook | TL | documentation | MEDIUM | 2 | M |
| MEM-114 | Incremental Improvements | PM | documentation | MEDIUM | 3 | M |
| MEM-115 | Security Updates | AR | documentation | MEDIUM | 2 | M |
| MEM-116 | Scaling plan | AR | documentation | HIGH | 3 | M |

---

## 5. DEPENDENCIAS CRÍTICAS (15)

Crear tras Paso 4 (tasks) usando los taskIds capturados.

```bash
POST http://77.42.88.106:3000/api/tasks/{taskId}/dependencies
{"dependsOnTaskId": "{otroTaskId}"}
```

| # | Task | Depende de | Razón | Impacto |
|---:|------|-----------|-------|---------|
| 1 | MEM-006 | MEM-005 | Discovery después de Kickoff | Alto |
| 2 | MEM-039 | MEM-025 | Design Technical después de Analysis | Alto |
| 3 | MEM-048 | MEM-047 | Development después de Design Technical | Alto |
| 4 | MEM-053 | MEM-052 | S02 depende de S01 | Alto |
| 5 | MEM-058 | MEM-057 | S03 depende de S02 | Medio |
| 6 | MEM-063 | MEM-062 | S04 depende de S03 | Medio |
| 7 | MEM-069 | MEM-068 | S05 depende de S04 | Medio |
| 8 | MEM-075 | MEM-074 | S06 depende de S05 | Medio |
| 9 | **MEM-081** | **MEM-038** | **HITO DL→FE** | 🚨 **CRÍTICO** |
| 10 | MEM-086 | MEM-085 | UI-02 depende de UI-01 | Alto |
| 11 | MEM-089 | MEM-088 | UI-03 depende de UI-02 | Alto |
| 12 | MEM-091 | MEM-090 | UI-04 depende de UI-03 | Alto |
| 13 | MEM-094 | MEM-093 | Testing depende de Development | Alto |
| 14 | MEM-104 | MEM-103 | Deploy depende de Testing | Alto |
| 15 | MEM-111 | MEM-110 | Operations depende de Deploy | Alto |

---

## 6. ANEXO: DESGLOSE INIT DE MEM-001..005

Las 24 INIT son **desglose operativo** de MEM-001..005. NO se cargan como tareas separadas en VTT — viven solo aquí como referencia de ejecución.

### A. VTT Setup (dentro de MEM-003)
- INIT-A-01 Verificar proyecto VTT · PJM · 0.5h · ✅ (este doc lo crea)
- INIT-A-02 Verificar 10 fases · PJM · 0.5h · ✅ (Paso 2)
- INIT-A-03 Verificar 65 deliveries · PJM · 0.5h · ✅ (Paso 3)
- INIT-A-04 POST 116 tareas con metadata · PJM+DO · 2h (Paso 4)
- INIT-A-05 POST 15 dependencias · PJM · 2.5h (Paso 6)

### B. Repo Setup (dentro de MEM-002)
- INIT-B-01 Crear repo Git (multi-repo pendiente)
- INIT-B-02 Estructura V3.1
- INIT-B-03 .gitignore, README, CONTRIBUTING
- INIT-B-04 Branch protection + CODEOWNERS + PR templates
- INIT-B-05 Git conventions

### C. VM Configuration (dentro de MEM-001)
- INIT-C-01 Verificar infra ya provisionada (✅ hecho previamente)
- INIT-C-02 Tests conectividad local → VM
- INIT-C-03 Distribuir SERVICE_KEY
- INIT-C-04 `docs/INFRASTRUCTURE.md`

### D. Agent Team (dentro de MEM-003)
- INIT-D-01 OPERATIVO_<ROL>.md para 12 roles
- INIT-D-02 PROJECT_MEMORY.md (✅ existe)
- INIT-D-03 CONTEXTO_<ROL>_SESION.md
- INIT-D-04 Distribuir accesos
- INIT-D-05 Onboarding calls

### E. Tooling (dentro de MEM-004)
- INIT-E-01 Node 20 + TS + scripts
- INIT-E-02 ESLint + Prettier + Husky
- INIT-E-03 CI mínimo

### F. Documentation (dentro de MEM-005)
- INIT-F-01 README + CONTRIBUTING
- INIT-F-02 docs/ARCHITECTURE.md

### G. Kickoff (dentro de MEM-005)
- INIT-G-01 KICKOFF_MEMORY_SERVICE.md
- INIT-G-02 Kickoff call + acta

---

## 7. SCRIPT DE EJECUCIÓN COMPLETO (pseudo-código Python)

```python
import os, json, urllib.request

API_URL = "http://77.42.88.106:3000"
SERVICE_KEY = os.environ["VTT_SERVICE_KEY"]

# UUIDs de usuarios Memory Service (namespace memory-service.vtt.ai)
PM_UUID = "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"   # PM
PJM_UUID = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"  # PJM
TL_UUID = "92225290-6b6b-4c1f-a940-dcb4262507aa"   # TL

USERS = {
    "PM":  PM_UUID,
    "PJM": PJM_UUID,
    "TL":  TL_UUID,
    "SA":  "0c128e3b-db3b-4e31-b107-0379b5791233",  # Solution Analyst
    "AR":  "e9403c25-c1f8-4b64-b2ef-f447d53115e2",  # Architect
    "BE":  "ebbe3cee-abed-4b3b-860d-0a81f632b08a",
    "DB":  "6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7",
    "FE":  "d23c9cd9-a156-433b-8900-94add5488eec",
    "UX":  "a75a1dae-754a-4b6f-a3ff-db8d51f6a91b",
    "DL":  "b3a09269-cded-468c-a475-15a48f203cb0",
    "QA":  "613c9538-658c-45fe-a6d7-c1ea9ff04b78",
    "DO":  "322e3745-9756-4a7c-af11-44b33edef44d",
    # Usuarios adicionales (no usados en asignaciones default de las 116 tareas):
    "PSA": "a43f6bd0-3452-46ea-85ae-78589c071a3e",  # Product Strategy Analyst
    "IR":  "f3e358f7-679f-400f-8dd7-df41517bca15",  # Integration Reviewer
    "CIA": "4ccfe002-ddd3-4df7-bf31-825dcebd576e",  # Competitive Intelligence (excluido R1)
    "MRA": "44e7bfb3-2aca-4ac1-820e-0836e95cd718",  # Market Research (excluido R1)
}

PRIORITY = {
    "C": "90ec3df2-fac4-40fa-b2ce-29daf0f4956e",  # critical
    "H": "1a617554-6319-4c56-826f-8ef49a0ff9cc",  # high
    "M": "d0b619ef-27e7-42d8-8879-41030a602eed",  # medium
    "L": "95f2e731-41b9-4a7d-9a43-31f00a4ddd7e",  # low
}

STATUS_PENDING = "335fd9c6-f0d6-4966-a6ea-f518c78bc422"

# Obtener JWT
req = urllib.request.Request(
    f"{API_URL}/api/auth/service-token",
    data=json.dumps({"userId": PJM_UUID, "serviceKey": SERVICE_KEY}).encode(),
    headers={"Content-Type": "application/json"}, method="POST")
TOKEN = json.loads(urllib.request.urlopen(req).read())["data"]["token"]
H = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}

uuids = {"phases": {}, "deliveries": {}, "tasks": {}}

# ─── PASO 1: Create Project ────────────────────────────────────────────
def post(path, body):
    req = urllib.request.Request(
        f"{API_URL}{path}",
        data=json.dumps(body).encode(),
        headers=H, method="POST")
    return json.loads(urllib.request.urlopen(req).read())

project = post("/api/projects", {
    "name": "Memory Service",
    "code": "MEM",
    "description": "Microservicio independiente de memoria centralizada para agentes IA...",
    "projectTypeCode": "SOFTWARE",
    "createdBy": PM_UUID,
})
project_id = project["data"]["id"]

# ─── PASO 2: Create 10 Phases ──────────────────────────────────────────
PHASES = [
    ("Project Setup", 1), ("Discovery", 2), ("Planning", 3), ("Analysis", 4),
    ("Design UX/UI", 5), ("Design Technical", 6), ("Development", 7),
    ("Testing", 8), ("Deploy", 9), ("Operations", 10),
]
for name, order in PHASES:
    p = post(f"/api/projects/{project_id}/phases", {
        "name": name, "order": order, "createdBy": PM_UUID,
    })
    uuids["phases"][name] = p["data"]["id"]

# ─── PASO 3: Create 65 Deliveries ──────────────────────────────────────
DELIVERIES = [
    ("Project Setup", "Project Foundation Ready", 1),
    ("Discovery", "Problem Definition", 1),
    ("Discovery", "Value Proposition", 2),
    ("Planning", "Vision & Objectives", 1),
    ("Planning", "Scope", 2),
    # ... resto de 60 deliveries ...
]
for phase_name, deliv_name, order in DELIVERIES:
    d = post("/api/deliveries", {
        "phaseId": uuids["phases"][phase_name],
        "name": deliv_name,
        "order": order,
        "createdBy": PJM_UUID,
    })
    uuids["deliveries"][deliv_name] = d["data"]["id"]

# ─── PASO 4: Create 116 Tasks ──────────────────────────────────────────
TASKS = [
    # (code, phase_name, delivery_name, title, description, rol, cat, cmplx, hours, pri)
    ("MEM-001", "Project Setup", "Project Foundation Ready",
     "Infra Setup",
     "Coordinar con Admin VM la provisión...",
     "DO", "chore", "MEDIUM", 4, "M"),
    # ... resto de 115 tareas ...
]
for code, phase, deliv, title, desc, rol, cat, cmplx, hours, pri in TASKS:
    t = post(f"/api/phases/{uuids['phases'][phase]}/tasks", {
        "title": title,
        "description": desc,
        "priorityId": PRIORITY[pri],
        "statusId": STATUS_PENDING,
        "assignedToId": USERS[rol],
        "assignedBy": PJM_UUID,
        "category": cat,
        "complexity": cmplx,
        "createdBy": PJM_UUID,
    })
    uuids["tasks"][code] = t["data"]["id"]

    # Paso 5: Asignar a delivery
    post(f"/api/deliveries/{uuids['deliveries'][deliv]}/tasks/{uuids['tasks'][code]}", {
        "assignedBy": PJM_UUID,
    })

# ─── PASO 6: Create 15 Dependencies ────────────────────────────────────
DEPS = [
    ("MEM-006", "MEM-005"), ("MEM-039", "MEM-025"), ("MEM-048", "MEM-047"),
    ("MEM-053", "MEM-052"), ("MEM-058", "MEM-057"), ("MEM-063", "MEM-062"),
    ("MEM-069", "MEM-068"), ("MEM-075", "MEM-074"),
    ("MEM-081", "MEM-038"),  # HITO CRÍTICO
    ("MEM-086", "MEM-085"), ("MEM-089", "MEM-088"), ("MEM-091", "MEM-090"),
    ("MEM-094", "MEM-093"), ("MEM-104", "MEM-103"), ("MEM-111", "MEM-110"),
]
for task, dep in DEPS:
    post(f"/api/tasks/{uuids['tasks'][task]}/dependencies", {
        "dependsOnTaskId": uuids["tasks"][dep],
    })

# Guardar UUIDs capturados
with open("VTT_UUIDS_MEMORY_SERVICE.json", "w") as f:
    json.dump({"projectId": project_id, **uuids}, f, indent=2)

print(f"✅ Completado: project + 10 phases + 65 deliveries + 116 tasks + 15 deps")
print(f"UUIDs guardados en VTT_UUIDS_MEMORY_SERVICE.json")
```

El script completo con las 116 tareas y 65 deliveries expandidos se genera del §4 de este documento.

---

## 8. TOTALES VERIFICACIÓN

| Fase | Tareas | Horas | Rol principal |
|------|-------:|------:|---------------|
| 1 Project Setup | 5 | 32 | DO, PJM, PM |
| 2 Discovery | 4 | 9 | SA, PM |
| 3 Planning | 8 | 23 | PM, PJM, SA |
| 4 Analysis | 8 | 41 | SA, AR, UX |
| 5 Design UX/UI | 13 | 35 | UX, DL |
| 6 Design Technical | 9 | 45 | AR, TL, DB, BE, DO |
| 7 Development | 46 | 116 | DB, BE, FE, DO, QA |
| 8 Testing | 10 | 60 | QA, AR, DO, PM, BE |
| 9 Deploy | 7 | 26 | DO, QA, TL |
| 10 Operations | 6 | 15 | DO, PM, TL, AR |
| **TOTAL** | **116 tasks** | **402h** | **12 roles** |

---

## 9. POST-EJECUCIÓN (output esperado)

Tras ejecutar el script, se genera `VTT_UUIDS_MEMORY_SERVICE.json`:

```json
{
  "projectId": "{nuevo-uuid-project}",
  "phases": {
    "Project Setup": "{nuevo-uuid-phase-1}",
    "Discovery": "{nuevo-uuid-phase-2}",
    ...
  },
  "deliveries": {
    "Project Foundation Ready": "{nuevo-uuid-delivery-1}",
    "Problem Definition": "{nuevo-uuid-delivery-2}",
    ...
  },
  "tasks": {
    "MEM-001": "{nuevo-vtt-id-task-1}",
    "MEM-002": "{nuevo-vtt-id-task-2}",
    ...
  }
}
```

Este archivo es el **source of truth de UUIDs** post-creación. Todos los documentos operativos posteriores (HOs por fase, BRIEFs, PATCH status, etc.) referencian este JSON.

---

**Documento:** TASK_INDEX_SEED_MEMORY_SERVICE.md  
**Versión:** 2.0  
**Estado:** ✅ Listo para ejecución de creación  
**Fecha:** 2026-04-22  

**Fuente de endpoints:** PROCESO_ASIGNACION_TAREAS.md v1.6 (2026-04-20)

**Usado por:**
- PJM: ejecuta script Python para crear project + phases + deliveries + tasks + deps
- TL: review post-creación de asignaciones y metadata
- PM: firma antes de ejecutar, valida post-creación

---

**PM — Martin Rivas**
