# CONSOLIDADO MEMORY SERVICE R1 — Plan Maestro

| Campo | Valor |
|-------|-------|
| **Documento** | CONSOLIDADO_MEMORY_SERVICE_R1.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **Autor** | PM (Martin Rivas) |
| **Proyecto** | Memory Service R1 (`51e169f7-8a23-4628-8b78-04864b633ac7`, key MEM) |
| **Propósito** | Plan maestro consolidado: iniciación del proyecto + fases SDLC aplicables + tareas de implementación reemplazando deliverables en fases 4-7 |
| **Supersedes / Consolida** | `PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md` · `FASES_APLICABLES_MEMORY_SERVICE.md v2.0` · `PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md` |
| **Estado** | ✅ Listo para revisión PM |

---

## ÍNDICE

1. [Jerarquía y contexto](#1-jerarquía-y-contexto)
2. [Fase de Iniciación (pre-SDLC)](#2-fase-de-iniciación-del-proyecto-pre-sdlc)
3. [Fases SDLC aplicables](#3-fases-sdlc-aplicables)
   - [3.1 Fase 0 Discovery](#31-fase-0--discovery)
   - [3.2 Fase 1 Planning](#32-fase-1--planning)
   - [3.3 Fase 2 Analysis](#33-fase-2--analysis)
   - [3.4 Fase 3A Design UX/UI](#34-fase-3a--design-uxui)
   - [3.5 Fase 3B Design Technical](#35-fase-3b--design-technical)
   - [3.6 Fase 4 Development (tareas)](#36-fase-4--development)
   - [3.7 Fase 5 Testing (tareas)](#37-fase-5--testing)
   - [3.8 Fase 6 Deploy (tareas)](#38-fase-6--deploy)
   - [3.9 Fase 7 Operations (tareas)](#39-fase-7--operations)
4. [Resumen ejecutivo](#4-resumen-ejecutivo)
5. [Siguiente paso](#5-siguiente-paso)

---

## 1. JERARQUÍA Y CONTEXTO

### 1.1 Jerarquía (Modelo Dinámico V3)

```
Memory Service (Project)
  └── R1 (Release)
        └── Iniciación (pre-SDLC) + 9 Fases SDLC
              └── Deliverables (390 SDLC aplicables) / Tareas (para fases de implementación)
                    └── Artefactos (docs, código, tests, deploy)
```

### 1.2 Contexto del proyecto

| Aspecto | Valor |
|---------|-------|
| Tipo | Feature interna de VTT (microservicio independiente) |
| Stack | Node.js 20 + TypeScript + Express + Prisma + PostgreSQL + Redis + React + Vite |
| Infra | Hetzner `77.42.88.106` (shared-postgres, shared-redis, shared-network) |
| Puertos | 3002 API · 3003 UI |
| Integraciones | Runtime v1.1 · Prompt Builder v1.3 · Hook Manager VTT |
| SLA crítico | `<500ms` p95 en `GET /context` (fail-fast) |

### 1.3 Totales maestros

| Bloque | Unidades | Horas | Fuente |
|--------|---------:|------:|--------|
| Iniciación (pre-SDLC) | 24 tareas | 32h | §2 |
| Fases 0-3B (docs/design) | 203 deliverables + 42 tareas VTT | 153h | §3.1–§3.5 |
| Fases 4-7 (implementación) | 66 tareas | 217h | §3.6–§3.9 |
| **TOTAL proyecto** | **132 tareas ejecutables + 203 deliverables** | **~402h** | |

> Las 116 tareas VTT oficiales se mantienen intactas. Las 24 tareas de iniciación son **desglose operativo de MEM-001..005** (cuyas horas en VTT deben actualizarse 11h → 32h).

---

## 2. FASE DE INICIACIÓN DEL PROYECTO (pre-SDLC)

**24 tareas · 32h** antes de arrancar Phase 0 Discovery.

### 2.1 Resumen por categoría

| Categoría | Tareas | Horas | Rol principal |
|-----------|-------:|------:|---------------|
| A. VTT Setup | 5 | 6h | PJM |
| B. Repository Setup | 5 | 5h | DO + PJM |
| C. VM Configuration | 4 | 4h | DO |
| D. Agent Team Setup | 5 | 8h | PM + PJM |
| E. Tooling Setup | 3 | 4h | DO + TL |
| F. Documentation | 2 | 2h | PM + TL |
| G. Kickoff | 2 | 3h | PM |

### 2.2 Categoría A · VTT Setup (5 tareas · 6h)

| ID | Título | Rol | Horas | Estado |
|----|--------|-----|------:|--------|
| INIT-A-01 | Verificar proyecto en VTT | PJM | 0.5h | ✅ Hecho |
| INIT-A-02 | Verificar 10 fases en VTT | PJM | 0.5h | ✅ Hecho |
| INIT-A-03 | Verificar 65 deliveries en VTT | PJM | 0.5h | ✅ Hecho |
| INIT-A-04 | Ejecutar PATCH de 116 tareas en VTT (assigneeId, complexity, category, hours) | PJM + DO | 2h | 🟡 Pendiente |
| INIT-A-05 | Crear 15 dependencias críticas manualmente | PJM | 2.5h | 🟡 Pendiente |

### 2.3 Categoría B · Repository Setup (5 tareas · 5h)

| ID | Título | Rol | Horas | Estado |
|----|--------|-----|------:|--------|
| INIT-B-01 | Crear/verificar repo Git (remoto actual apunta a `twitter-react`) | DO | 1h | 🔴 Bloqueado (multi-repo) |
| INIT-B-02 | Inicializar estructura V3.1 | PJM | 1h | 🟡 Pendiente |
| INIT-B-03 | `.gitignore`, `.gitattributes`, `.editorconfig`, `README.md`, `CONTRIBUTING.md` | PJM | 1h | 🟡 Pendiente |
| INIT-B-04 | Branch protection + CODEOWNERS + PR templates | DO | 1h | 🟡 Pendiente |
| INIT-B-05 | Git user + convenciones commit (`Co-Authored-By`) | PJM | 1h | 🟡 Pendiente |

### 2.4 Categoría C · VM Configuration (4 tareas · 4h)

| ID | Título | Rol | Horas | Estado |
|----|--------|-----|------:|--------|
| INIT-C-01 | Verificar infra provisionada (BD, volumen, SERVICE_KEY, Redis, firewall, network) | DO | 1h | ✅ Hecho |
| INIT-C-02 | Tests de conectividad local → VM | DO | 1h | 🟡 Pendiente |
| INIT-C-03 | Distribuir SERVICE_KEY a Runtime, Prompt Builder, Hook Manager, FE | DO | 1h | 🟡 Pendiente |
| INIT-C-04 | `docs/INFRASTRUCTURE.md` con config VM | DO | 1h | 🟡 Pendiente |

### 2.5 Categoría D · Agent Team Setup (5 tareas · 8h)

| ID | Título | Rol | Horas | Estado |
|----|--------|-----|------:|--------|
| INIT-D-01 | OPERATIVO_<ROL>.md para 12 roles | PM + PJM | 3h | 🟡 Parcial (2/12: PM, TL) |
| INIT-D-02 | PROJECT_MEMORY.md consolidado | PM | 0.5h | ✅ Hecho |
| INIT-D-03 | CONTEXTO_<ROL>_SESION.md por rol | PJM | 1h | 🟡 Parcial (1/7+: PM) |
| INIT-D-04 | Distribuir accesos (repo, VTT, docs) | PJM | 1h | 🟡 Pendiente |
| INIT-D-05 | Reuniones onboarding por rol activo | PM | 2.5h | 🟡 Pendiente |

### 2.6 Categoría E · Tooling Setup (3 tareas · 4h)

| ID | Título | Rol | Horas | Estado |
|----|--------|-----|------:|--------|
| INIT-E-01 | Node 20 + TypeScript + package.json scripts | DO + TL | 2h | 🟡 Pendiente |
| INIT-E-02 | ESLint + Prettier + Husky + lint-staged | DO | 1h | 🟡 Pendiente |
| INIT-E-03 | CI mínimo (build + lint + test en PR) | DO | 1h | 🟡 Pendiente |

### 2.7 Categoría F · Documentation (2 tareas · 2h)

| ID | Título | Rol | Horas | Estado |
|----|--------|-----|------:|--------|
| INIT-F-01 | README.md + CONTRIBUTING.md del repo | PM + TL | 1h | 🟡 Pendiente |
| INIT-F-02 | `docs/ARCHITECTURE.md` (resumen con link a SPEC v1.9) | TL | 1h | 🟡 Pendiente |

### 2.8 Categoría G · Kickoff (2 tareas · 3h)

| ID | Título | Rol | Horas | Estado |
|----|--------|-----|------:|--------|
| INIT-G-01 | `KICKOFF_MEMORY_SERVICE.md` (visión, scope, roadmap, equipo) | PM | 2h | 🟡 Pendiente |
| INIT-G-02 | Kickoff call + acta | PM + todos | 1h | 🟡 Pendiente |

### 2.9 Mapeo a MEM-001..005 en VTT

| MEM actual | INIT-* que absorbe | Horas originales | Horas reales |
|-----------|---------------------|-----------------:|-------------:|
| MEM-001 Infra Setup | INIT-C-01..04 | 2h | 4h |
| MEM-002 Repo Structure | INIT-B-01..05 | 2h | 5h |
| MEM-003 Team Onboarding | INIT-A-01..05 + INIT-D-01..05 | 1h | 14h |
| MEM-004 Tooling Setup | INIT-E-01..03 | 2h | 4h |
| MEM-005 Project Kickoff | INIT-F-01..02 + INIT-G-01..02 | 4h | 5h |
| | **TOTAL** | **11h** | **32h** |

**Acción requerida:** PATCH horas estimadas de MEM-001..005 en VTT (11h → 32h).

---

## 3. FASES SDLC APLICABLES

### 3.1 FASE 0 · DISCOVERY

**Entregables aplicables:** 10 de 22 · **Tareas VTT:** 4 (MEM-006..009) · **Horas:** 9h

#### 3.1.1 Deliverables (10)

**0.3 Problem Definition (5)** — produce MEM-006 + MEM-007

| # | Deliverable |
|---|-------------|
| 0.3.1 | Problem Statement |
| 0.3.2 | User Pain Points |
| 0.3.3 | Current Solutions |
| 0.3.4 | Why Now |
| 0.3.5 | Problem Validation (adaptado: validación interna VTT) |

**0.4 Value Proposition (5)** — produce MEM-008 + MEM-009

| # | Deliverable |
|---|-------------|
| 0.4.1 | Value Proposition Canvas |
| 0.4.2 | UVP Statement |
| 0.4.3 | Key Differentiators |
| 0.4.4 | Target Customer Profile (adaptado: agentes AI + devs VTT) |
| 0.4.5 | Value Hypothesis |

#### 3.1.2 Tareas VTT (4 · 9h)

| Task | Título | Delivery | Rol | Horas | Produce |
|------|--------|----------|-----|------:|---------|
| MEM-006 | Problem Definition | Problem Definition | SA | 3h | 0.3.1, 0.3.2, 0.3.3, 0.3.4 |
| MEM-007 | Problem Validation | Problem Definition | PM | 2h | 0.3.5 |
| MEM-008 | Value Proposition | Value Proposition | SA | 3h | 0.4.1, 0.4.2, 0.4.3, 0.4.4, 0.4.5 |
| MEM-009 | Value Validation | Value Proposition | PM | 1h | Sign-off de 0.4.* |

**Excluidos:** 0.1 Market Research (5) · 0.2 Competitive Analysis (7). Razón: feature interna.

---

### 3.2 FASE 1 · PLANNING

**Entregables aplicables:** 33 de 33 · **Tareas VTT:** 8 (MEM-010..017) · **Horas:** 23h

#### 3.2.1 Deliverables (33)

| Subfase | Deliverables |
|---------|--------------|
| 1.1 Vision & Objectives (6) | Vision · Mission · Goals · KPIs · North Star · OKRs |
| 1.2 Scope (6) | Scope Statement · In-Scope · Out-of-Scope · MVP Definition · Future Phases · Assumptions |
| 1.3 Stakeholders (4) | Stakeholder Map · Register · RACI · Communication Plan |
| 1.4 Risks (5) | Risk Register · Assessment · Mitigation · Contingency · Monitoring |
| 1.5 Timeline (7) | Schedule · Milestones · Phase Breakdown · Sprint Calendar · Dependencies · Critical Path · Buffer |
| 1.6 Budget (5) | Estimate · Breakdown · Resource Plan · ROI · Tracking |

#### 3.2.2 Tareas VTT (8 · 23h)

| Task | Título | Delivery | Rol | Horas |
|------|--------|----------|-----|------:|
| MEM-010 | Vision | Vision & Objectives | PM | 3h |
| MEM-011 | Objectives | Vision & Objectives | PM | 2h |
| MEM-012 | Scope | Scope | SA | 4h |
| MEM-013 | Stakeholders | Stakeholders | PJM | 2h |
| MEM-014 | Risks | Risks | PJM | 3h |
| MEM-015 | Timeline | Timeline | PJM | 4h |
| MEM-016 | Milestones | Timeline | PJM | 3h |
| MEM-017 | Budget & Resources | Budget & Resources | PM | 2h |

---

### 3.3 FASE 2 · ANALYSIS

**Entregables aplicables:** 47 de 47 · **Tareas VTT:** 8 (MEM-018..025) · **Horas:** 41h

#### 3.3.1 Deliverables (47)

| Subfase | Deliverables |
|---------|--------------|
| 2.1 Functional Requirements (6) | SRS · Requirements List · Priority Matrix (MoSCoW) · Feature List · Functional Decomposition · Approval |
| 2.2 Non-Functional Requirements (6) | NFR Doc · Performance (`<500ms`) · Security (SERVICE_KEY) · Scalability · Availability · Usability |
| 2.3 Use Cases (6) | Use Case Doc · Diagram · List · Detailed · Actor Definitions · Relationships |
| 2.4 User Stories (6) | Product Backlog · User Stories · Story Map · Epics · Estimation · Sprint Assignment |
| 2.5 Business Rules (7) | Rules Doc · List · Validation · Calculation (USD cost) · Authorization (SERVICE_KEY) · State Transition · Glossary |
| 2.6 User Flows (7) | Flow Diagrams · Happy Path · Error Flows · Edge Cases · User Journey · Task Flows · Navigation Map |
| 2.7 Acceptance Criteria (5) | AC Doc · Per Story · DoD · DoR · Test Scenarios |
| 2.8 Traceability Matrix (4) | Matrix · RF→US · US→Test · Coverage Report |

#### 3.3.2 Tareas VTT (8 · 41h)

| Task | Título | Delivery | Rol | Horas |
|------|--------|----------|-----|------:|
| MEM-018 | Functional Requirements | Functional Requirements | SA | 6h |
| MEM-019 | Non-Functional Requirements | NFR | AR | 4h |
| MEM-020 | Use Cases | Use Cases | SA | 5h |
| MEM-021 | User Stories | User Stories | SA | 8h |
| MEM-022 | Business Rules | Business Rules | SA ⚠️ (reassigned from TL) | 4h |
| MEM-023 | User Flows | User Flows | UX | 4h |
| MEM-024 | Acceptance Criteria | Acceptance Criteria | SA | 6h |
| MEM-025 | Traceability Matrix | Traceability Matrix | SA | 4h |

---

### 3.4 FASE 3A · DESIGN UX/UI

**Entregables aplicables:** 40 de 72 · **Tareas VTT:** 13 (MEM-026..038) · **Horas:** 35h

#### 3.4.1 Deliverables (40)

| Subfase | Aplican | Excluidos |
|---------|--------:|----------:|
| 3A.1 User Research | 0 | 9 (sin usuarios externos) |
| 3A.2 Personas | 6 | 2 (Anti-Personas, Empathy Maps) |
| 3A.3 Information Architecture | 7 | 1 (Card Sorting) |
| 3A.4 Wireframes | 7 | 2 (Mobile, Tablet) |
| 3A.5 Mockups | 6 | 4 (Mobile, Tablet, Dark Mode, Responsive) |
| 3A.6 Prototypes | 0 | 6 (herramienta interna) |
| 3A.7 Design System | 9 | 1 (Brand Guidelines) |
| 3A.8 Usability Testing | 0 | 7 (sin usuarios externos) |
| 3A.9 Design Handoff | 5 | 0 |

#### 3.4.2 Tareas VTT (13 · 35h)

| Task | Título | Delivery | Rol | Horas |
|------|--------|----------|-----|------:|
| MEM-026 | Personas | Personas | UX | 3h |
| MEM-027 | Information Architecture | IA | UX | 4h |
| MEM-028 | Design System | Design System | DL | 3h |
| MEM-029 | Wireframes — Dashboard | Wireframes | DL | 4h |
| MEM-030 | Wireframes — Timeline | Wireframes | DL | 3h |
| MEM-031 | Wireframes — Viewer | Wireframes / Mockups | DL | 4h |
| MEM-032 | Wireframes — Cost Report | Wireframes / Mockups | DL | 4h |
| MEM-033 | Wireframes — Lista Convs | Wireframes | DL | 2h |
| MEM-034 | Wireframes — Import Manual | Wireframes | DL | 2h |
| MEM-035 | Wireframes — Health | Wireframes | DL | 2h |
| MEM-036 | Wireframes — Extras | Wireframes | DL | 1h |
| MEM-037 | Design Handoff — Assets | Design Handoff | DL | 2h |
| **MEM-038** | **Design Handoff — Final** 🚨 | Design Handoff | DL | 1h |

> 🚨 **MEM-038 es HITO crítico:** bloquea el inicio de FE (MEM-081+).

---

### 3.5 FASE 3B · DESIGN TECHNICAL

**Entregables aplicables:** 73 de 73 · **Tareas VTT:** 9 (MEM-039..047) · **Horas:** 45h

#### 3.5.1 Deliverables (73)

La mayoría **ya están contenidos** en SPEC v1.9, METODOLOGIA v1.2 y ADDENDUM v1.1. Las tareas VTT los consolidan como documentos independientes.

| Subfase | Deliverables |
|---------|--------------|
| 3B.1 Solution Architecture (7) | Architecture Doc · C4 L1/L2/L3 · Tech Stack · Integration Points · Data Flow |
| 3B.2 Code Architecture (6) | Folder Structure · Coding Standards · Design Patterns · Module Deps · Naming · Error Handling |
| 3B.3 Database Design (8) | ERD · Prisma Schema · Table Specs · Index Strategy · Data Dictionary · Migration · Seed · Backup |
| 3B.4 API Design (11) | OpenAPI · Endpoints List · R/R Examples · Pagination · Error Codes (MEM-ERR-*) · Auth · AuthZ · Rate Limit · Versioning · Postman · Guidelines |
| 3B.5 Sequence Diagrams (6) | Auth · Business Flows · Error · Integration · Async |
| 3B.6 ADR (4) | Template · Index · ADR Docs (48 decisiones) · Decision Log |
| 3B.7 Security Plan (11) | Security Plan · AuthN · AuthZ · Data Protection · Encryption · OWASP · Headers · Secrets · Input Validation · Logging · Incident Response |
| 3B.8 Infrastructure Plan (11) | Infra Plan · Diagram (Hetzner) · Server Specs · Network · Env Matrix · Scaling · Backup · DR · Cost · SLA · Monitoring |
| 3B.9 Technical Estimates (9) | Estimates · Story Points · Task Breakdown · Effort Matrix · Complexity · Risk-adjusted · Dependencies · Velocity · Capacity |

#### 3.5.2 Tareas VTT (9 · 45h)

| Task | Título | Delivery | Rol | Horas |
|------|--------|----------|-----|------:|
| MEM-039 | Solution Architecture | Solution Architecture | AR ⚠️ (reassigned from TL) | 6h |
| MEM-040 | Code Architecture | Code Architecture | TL | 4h |
| MEM-041 | Database Design | Database Design | DB | 6h |
| MEM-042 | API Design | API Design | BE | 8h |
| MEM-043 | Sequence Diagrams | Sequence Diagrams | AR | 6h |
| MEM-044 | Architecture Decision Records | ADRs | TL | 4h |
| MEM-045 | Security Plan | Security Plan | AR | 4h |
| MEM-046 | Infrastructure Plan | Infrastructure Plan | DO | 4h |
| MEM-047 | Technical Estimates | Technical Estimates | TL | 3h |

---

### 3.6 FASE 4 · DEVELOPMENT

> **Deliverables reemplazados por tareas de implementación.** Los 75 deliverables aplicables (ej. "4.3.1 API Endpoints", "4.2.1 Initial Migration") son producidos por las 46 tareas VTT abajo detalladas. Ver mapeo en §3.6.8.

**Tareas VTT:** 46 (MEM-048..093) · **Horas:** 116h

#### 3.6.1 S01 · Schema + Seeds (5 tareas · 9h)

| Task | Título | Rol | Horas | Complexity | Produce (archivos) |
|------|--------|-----|------:|------------|---------------------|
| MEM-048 | DB Schema Prisma completo (19 tablas + 10 catálogos) | DB | 3h | HIGH | `prisma/schema.prisma` |
| MEM-049 | Migraciones + Partial Indexes + índice GIN | DB | 2h | MEDIUM | `prisma/migrations/` + `partial_indexes.sql` |
| MEM-050 | Seed de 10 catálogos | DB | 1h | LOW | `prisma/seed.ts` |
| MEM-051 | Setup Express + estructura carpetas | BE | 2h | MEDIUM | `src/app.ts`, `src/index.ts`, estructura |
| MEM-052 | Catalog cache startup | BE | 1h | LOW | `src/services/catalog-cache.service.ts` |

#### 3.6.2 S02 · Import + Timeline (5 tareas · 12h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-053 | POST `/api/conversations/import` | BE | 4h | HIGH | Controller + service, 4 adapters, idempotencia |
| MEM-054 | POST `/api/conversations/import-review` | BE | 2h | MEDIUM | Multi-agent import incremental |
| MEM-055 | POST `/api/conversations/upload` | BE | 3h | HIGH | Endpoint manual multipart |
| MEM-056 | GET `/api/agents/:id/timeline` | BE | 2h | MEDIUM | Timeline paginado |
| MEM-057 | Error handling + cleanup delegation | BE | 1h | LOW | Middleware error-handler + zod |

#### 3.6.3 S03 · Content + Context (5 tareas · 12h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-058 | GET `/api/conversations/:id/content` | BE | 2h | MEDIUM | Parse archivo desde `/storage/` (D-MEM-43) |
| MEM-059 | GET `/api/context` (`<500ms` fail-fast) | BE | 4h | HIGH | `context.service.ts` con `Promise.race(queries, timeout)` |
| MEM-060 | Classifier determinístico | BE | 2h | HIGH | `classifier.service.ts` por reglas |
| MEM-061 | Tests performance contexto | QA | 2h | MEDIUM | Benchmark `<500ms` p95 |
| MEM-062 | Tests classifier | QA | 2h | MEDIUM | Fixtures + assertions topics/entities |

#### 3.6.4 S04 · Adapters + Cleanup (6 tareas · 12h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-063 | Adapter CLAUDE_WEB | BE | 3h | MEDIUM | `adapters/web.adapter.ts` |
| MEM-064 | Adapter CHATGPT | BE | 2h | MEDIUM | `adapters/chatgpt.adapter.ts` |
| MEM-065 | Storage writer JSONL | BE | 2h | MEDIUM | `storage.service.ts` (D-MEM-06) |
| MEM-066 | Cleanup cron (5 min) | BE | 2h | MEDIUM | `jobs/cleanup.job.ts` (D-MEM-35, D-MEM-40) |
| MEM-067 | Status transitions handler | BE | 1h | LOW | Helper con cache |
| MEM-068 | Tests adapters | BE | 2h | MEDIUM | Fixtures JSONL reales |

#### 3.6.5 S05 · Lista + Cost + Dashboard (6 tareas · 11h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-069 | GET `/api/conversations` (filtros) | BE | 2h | MEDIUM | Lista paginada |
| MEM-070 | GET `/api/projects/:id/cost-report` | BE | 2h | MEDIUM | Agregación por agente/tarea |
| MEM-071 | GET `/api/agents/:id/cost-report` | BE | 2h | MEDIUM | Breakdown por workType/semana |
| MEM-072 | GET `/api/dashboard/stats` | BE | 2h | MEDIUM | Totales globales |
| MEM-073 | GET `/health` | BE | 2h | MEDIUM | Check BD + storage + Redis |
| MEM-074 | Integration tests endpoints | BE | 1h | LOW | Smoke tests |

#### 3.6.6 S06 · Docker + Integration (6 tareas · 14h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-075 | Dockerfile + docker-compose | DO | 2h | MEDIUM | Container config con `mem_limit: 512m` |
| MEM-076 | CI config | DO | 2h | MEDIUM | Pipeline build + test + lint |
| MEM-077 | Env vars + secrets | DO | 1h | LOW | `.env.example`, secret management |
| MEM-078 | Integración Hook Manager VTT | BE | 4h | HIGH | Cliente + validación cross-service |
| MEM-079 | E2E test Runtime integration | QA | 3h | HIGH | Mock Runtime con `sourceCode=CLAUDE_SDK` |
| MEM-080 | E2E test Prompt Builder integration | QA | 2h | MEDIUM | Mock PB con SERVICE_KEY |

#### 3.6.7 UI-01..04 · Frontend (13 tareas · 46h)

**UI-01 · Setup + Timeline + Viewer (5 tareas · 16h)**

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-081 | Setup React + Vite + Tailwind | FE | 2h | MEDIUM | Proyecto FE 3003 |
| MEM-082 | Routing + layout base | FE | 1h | LOW | React Router + layout |
| MEM-083 | Page Timeline agente | FE | 5h | HIGH | `/agents/:id/timeline` |
| MEM-084 | Component Conversation Viewer | FE | 6h | HIGH | Viewer TASK_EXECUTION |
| MEM-085 | Auth context (SERVICE_KEY) | FE | 2h | MEDIUM | Header Bearer |

**UI-02 · Dashboard + Cost + Import (3 tareas · 12h)**

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-086 | Page Dashboard | FE | 4h | HIGH | `/` con stats |
| MEM-087 | Page Cost Report Proyecto | FE | 4h | MEDIUM | `/projects/:id/cost` |
| MEM-088 | Page Import Manual | FE | 4h | MEDIUM | `/import` multipart |

**UI-03 · Viewer REVIEW + Lista (2 tareas · 10h)**

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-089 | Page Lista conversaciones | FE | 5h | HIGH | `/conversations` con filtros |
| MEM-090 | Component AGENT_REVIEW | FE | 5h | HIGH | Thread multi-agente |

**UI-04 · Cost Agente + Health (3 tareas · 8h)**

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-091 | Page Cost Report Agente | FE | 3h | MEDIUM | `/agents/:id/cost` |
| MEM-092 | Page Health | FE | 2h | LOW | `/health` UI |
| MEM-093 | Polish + responsive desktop | FE | 3h | MEDIUM | Empty/loading/error states |

> 🚨 **Bloqueo UI:** MEM-081..093 no arrancan hasta MEM-038 `task_approved`.

#### 3.6.8 Mapeo Tareas → Deliverables SDLC Fase 4

| Subfase SDLC | Deliverables aplicables | Tareas VTT que los producen |
|--------------|-------------------------|------------------------------|
| 4.1 Environment Setup (10) | Docker, scripts, IDE, pre-commit, linters, formatters | **cubierto por INIT-E-*** y MEM-075, MEM-077 |
| 4.2 Database Implementation (8) | Migrations, Seed, Indexes, Constraints, Rollback | MEM-048, MEM-049, MEM-050 |
| 4.3 Backend Development (15) | Endpoints, Services, Models, DTOs, Workers, Middlewares, Tests, API Docs | MEM-051..057, MEM-058..062, MEM-063..068, MEM-069..074, MEM-103 |
| 4.4 Frontend Development (15) | Components, Pages, Layouts, Hooks, State, API Client, Types, Styles, Utils, Tests, Storybook, Accessibility, Responsive | MEM-081..093 |
| 4.5 Integrations (8) | Integration code, API Clients, Webhooks, SDKs, Tests, Docs, Error Handling, Retry | MEM-078, MEM-053 (parcial) |
| 4.6 Unit Tests (7) | Tests BE, FE, Coverage, Mocks, Fixtures, Utils | MEM-061, MEM-062, MEM-068, MEM-074 |
| 4.7 Technical Documentation (8) | README, Swagger, Comments, Architecture Docs, Contributing, Changelog | producidos a lo largo de S01..UI-04 + INIT-F-* |
| 4.8 Code Review (4) | PR Reviews, Code Quality, Tech Debt, Refactoring | continuo (TL reviewer) |

---

### 3.7 FASE 5 · TESTING

> **Deliverables reemplazados por tareas.** Los 51 deliverables aplicables son producidos por las 10 tareas VTT abajo.

**Tareas VTT:** 10 (MEM-094..103) · **Horas:** 60h

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-094 | Test Planning | Test Planning | QA | 4h | MEDIUM | Test plan + strategy + scope + schedule |
| MEM-095 | Test Cases completos | Test Cases | QA | 8h | HIGH | Casos por endpoint + escenarios error + matriz |
| MEM-096 | Test Environment setup | Test Environment | DO | 4h | MEDIUM | BD testing, seed, docker-compose CI |
| MEM-097 | Functional Testing | Functional Testing | QA | 8h | HIGH | Ejecución + report + evidence |
| MEM-098 | Integration Testing | Integration Testing | QA | 6h | HIGH | Suite BE + BD + storage |
| MEM-099 | E2E Testing | E2E Testing | QA | 8h | HIGH | Suite Playwright UI + API |
| MEM-100 | Performance Testing | Performance Testing | QA | 6h | HIGH | Load + stress + validación SLA `<500ms` |
| MEM-101 | Security Testing | Security Testing | AR | 4h | HIGH | Pentesting, OWASP, vulnerability scan |
| MEM-102 | UAT | UAT | PM | 4h | MEDIUM | UAT plan + test cases + sign-off (equipo VTT interno) |
| MEM-103 | Bug Fixes | Bug Fixes | BE | 8h | HIGH | Reserva esfuerzo post-testing |

**Excluido:** 5.9.3 Screen Reader Test (herramienta interna).

---

### 3.8 FASE 6 · DEPLOY

> **Deliverables reemplazados por tareas.** Los 38 deliverables aplicables son producidos por las 7 tareas VTT abajo.

**Tareas VTT:** 7 (MEM-104..110) · **Horas:** 26h

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-104 | Infrastructure Setup (producción) | Infrastructure Setup | DO | 4h | MEDIUM | Servers, SSL, DNS, network final |
| MEM-105 | CI/CD Configuration | CI/CD | DO | 6h | HIGH | Pipeline completo staging + prod |
| MEM-106 | Staging Deploy | Staging Deploy | DO | 4h | MEDIUM | Deploy automatizado + health check |
| MEM-107 | Smoke Testing | Smoke Testing | QA | 3h | MEDIUM | Suite smoke post-deploy |
| MEM-108 | Production Deploy | Production Deploy | DO | 4h | HIGH | Deploy prod + DNS + SSL + release notes |
| MEM-109 | Post-Deploy Monitoring | Post-Deploy Monitoring | DO | 3h | MEDIUM | Grafana + alerts + logs + error tracking |
| MEM-110 | Rollback Plan (doc) | Rollback Plan | TL | 2h | MEDIUM | Runbook + decision criteria |

---

### 3.9 FASE 7 · OPERATIONS

**Tareas VTT:** 6 (MEM-111..116) · **Horas:** 15h

| Task | Título | Delivery | Rol | Horas | Complexity | Tipo |
|------|--------|----------|-----|------:|------------|------|
| MEM-111 | Monitoring setup | Monitoring | DO | 3h | MEDIUM | Implementación |
| MEM-112 | User Support docs | User Support | PM | 2h | LOW | Doc |
| MEM-113 | Bug Fixes Operations playbook | Bug Fixes Operations | TL | 2h | MEDIUM | Doc |
| MEM-114 | Incremental Improvements | Incremental Improvements | PM | 3h | MEDIUM | Proceso |
| MEM-115 | Security Updates | Security Updates | AR | 2h | MEDIUM | Proceso |
| MEM-116 | Scaling plan | Scaling | AR | 3h | HIGH | Doc |

**Deliverables producidos (23):** Uptime/Performance/Error/Weekly Reports, Support Process/Ticket/SLA/Metrics, Hotfix Process/Releases/Tracking, Minor Releases/Feature Flags/A/B/Backlog, Security Patches/Dependencies/Audits/Vulnerabilities, Scaling Reports/Capacity/Auto-scaling/Cost Optimization.

---

## 4. RESUMEN EJECUTIVO

### 4.1 Totales maestros

| Bloque | Tareas | Horas | Deliverables |
|--------|-------:|------:|-------------:|
| Iniciación (pre-SDLC) | 24 | 32 | — |
| Fase 0 Discovery | 4 | 9 | 10 |
| Fase 1 Planning | 8 | 23 | 33 |
| Fase 2 Analysis | 8 | 41 | 47 |
| Fase 3A Design UX/UI | 13 | 35 | 40 |
| Fase 3B Design Technical | 9 | 45 | 73 |
| Fase 4 Development | 46 | 116 | 75 (producidos por tareas) |
| Fase 5 Testing | 10 | 60 | 51 (producidos por tareas) |
| Fase 6 Deploy | 7 | 26 | 38 (producidos por tareas) |
| Fase 7 Operations | 6 | 15 | 23 (producidos por tareas) |
| **TOTAL** | **135 tareas** | **402h** | **390 deliverables** |

> Nota: 116 tareas VTT oficiales + 24 INIT (desglose operativo de MEM-001..005 que en VTT suman 11h pero realmente requieren 32h).

### 4.2 Resumen por rol

| Rol | Tareas | Horas |
|-----|-------:|------:|
| PM | 7 VTT + 5 INIT = 12 | 16 + 5.5 = 21.5h |
| PJM | 7 VTT + 8 INIT = 15 | 15 + 8 = 23h |
| TL | 5 VTT + 3 INIT = 8 | 15 + 4 = 19h |
| SA | 8 VTT | 40h |
| AR | 7 VTT | 29h |
| DB | 4 VTT | 12h |
| BE | 28 VTT | 74h |
| DL | 11 VTT | 28h |
| UX | 3 VTT | 11h |
| FE | 13 VTT | 46h |
| QA | 11 VTT | 54h |
| DO | 12 VTT + 8 INIT = 20 | 33 + 14.5 = 47.5h |
| **TOTAL** | **135** | **~402h** |

### 4.3 Hitos críticos

| Hito | Bloquea | Fase |
|------|---------|------|
| Iniciación completa (checklist §2) | Arranque de Phase 0 Discovery | pre-SDLC |
| MEM-038 Design Handoff | MEM-081+ (FE arranque) | 3A → 4 |
| MEM-048..052 S01 | MEM-053..080 (todo backend posterior) | 4 |
| MEM-080..093 completos | MEM-094+ (Testing) | 4 → 5 |
| MEM-094..103 Testing | MEM-104+ (Deploy) | 5 → 6 |
| MEM-104..110 Deploy | MEM-111+ (Operations) | 6 → 7 |

### 4.4 Bloqueos activos (pre-arranque)

| # | Bloqueo | Resolver antes de |
|---|---------|-------------------|
| 1 | Repo Git real (multi-repo) | INIT-B-* | Cualquier trabajo de código |
| 2 | Endpoint VTT de dependencias | INIT-A-05 | Registro de dependencias |
| 3 | Actualización horas MEM-001..005 en VTT (11h→32h) | INIT-A-04 | Arranque iniciación |
| 4 | OPERATIVOs faltantes (10/12) | INIT-D-01 | Onboarding de roles |

---

## 5. SIGUIENTE PASO

Con este consolidado:

1. **Revisa y aprueba el plan completo** (iniciación + fases + tareas).
2. **PM ejecuta PATCH en VTT:**
   - MEM-001..005: actualizar horas (11h → 32h)
   - MEM-022, MEM-039: aplicar reassignments (TL→SA, TL→AR)
   - MEM-006..116: asignar assigneeId, complexity, category según este doc
3. **PM emite HO formal al PJM** con este consolidado + pre-handoffs como anexos.
4. **PJM genera BRIEFs downstream** por rol/sprint para que agentes ejecuten.
5. **Kickoff call** una vez checklist de iniciación esté en ≥80%.

---

**Documento:** CONSOLIDADO_MEMORY_SERVICE_R1.md  
**Versión:** 1.0  
**Estado:** ✅ Listo para revisión PM  
**Fecha:** 2026-04-22  

**Consolida:**
- `PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md` (iniciación pre-SDLC)
- `FASES_APLICABLES_MEMORY_SERVICE.md v2.0` (390 deliverables aplicables)
- `PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md` (66 tareas código/tests/deploy)

**Referencias:**
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` (contrato técnico)
- `METODOLOGIA_MEMORY_SERVICE_v1.2.md` (metodología funcional)
- `ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md` (integración cross-service)
- `PLAN_116_TAREAS.md` (vista TL del plan operativo)
- `HO_ACTUALIZAR_TAREAS_VTT.md v2.1` (fuente PJM de tareas y deliveries)

---

**PM — Martin Rivas**
