# PLAN — 116 Tareas Memory Service

**Preparado por:** TL (Tech Lead)
**Fuente:** `HO_ACTUALIZAR_TAREAS_VTT.md` v2.1 (PJM, 2026-04-21)
**Fecha revisión TL:** 2026-04-21
**Proyecto:** Memory Service (`d0fc276d-e764-4a83-96e9-d65f086ed803`)
**Total:** 116 tareas, 381h, 10 fases, 12 roles

> **Propósito:** vista TL del plan completo de 116 tareas con reassignments propuestos donde el rol asignado por PJM no corresponde al scope del rol.
>
> **Pendiente:** validación de PM sobre los 2 reassignments propuestos (§Reassignments).

---

## RESUMEN POR ROL (post-reassignments propuestos)

| Rol | Tareas | Horas | Cambio vs PJM |
|-----|--------|-------|---------------|
| PM | 7 | 16h | = |
| PJM | 7 | 15h | = |
| TL | 5 | 15h | −2 tareas (−10h) |
| SA | 8 | 40h | +1 tarea (+4h) |
| AR | 7 | 29h | +1 tarea (+6h) |
| DB | 4 | 12h | = |
| BE | 28 | 74h | = |
| DL | 11 | 28h | = |
| UX | 3 | 11h | = |
| FE | 13 | 46h | = |
| QA | 11 | 54h | = |
| DO | 12 | 33h | = |
| **TOTAL** | **116** | **381h** | — |

---

## REASSIGNMENTS PROPUESTOS (flags para PM)

Propongo 2 cambios respecto al HO del PJM. Ambos mueven tareas de **TL** a otro rol porque el scope no corresponde al Tech Lead.

| Task | Título | Fase | Plan PJM | **Propuesta TL** | Razón |
|------|--------|------|----------|------------------|-------|
| MEM-022 | Business Rules | Analysis | TL | **SA** | Business rules es un artefacto de análisis de sistemas, propio del System Architect. TL lee esto como input, no lo produce. |
| MEM-039 | Solution Architecture | Design Technical | TL | **AR** | Solution Architecture es el deliverable principal del Architect (AR). TL revisa, no produce. |

**Si PM aprueba:**
- TL baja de 7 tareas (25h) → 5 tareas (15h). Más consistente con rol "planear + revisar".
- SA sube de 7 tareas (36h) → 8 tareas (40h).
- AR sube de 6 tareas (23h) → 7 tareas (29h).

---

## LISTADO COMPLETO DE 116 TAREAS

### Phase 1: Project Setup (MEM-001..005) — 11h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-001 | Infra Setup | DO | 2h | MEDIUM |
| MEM-002 | Repo Structure | PJM | 2h | LOW |
| MEM-003 | Team Onboarding | PJM | 1h | LOW |
| MEM-004 | Tooling Setup | DO | 2h | MEDIUM |
| MEM-005 | Project Kickoff | PM | 4h | MEDIUM |

### Phase 2: Discovery (MEM-006..009) — 9h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-006 | Problem Definition | SA | 3h | MEDIUM |
| MEM-007 | Problem Validation | PM | 2h | LOW |
| MEM-008 | Value Proposition | SA | 3h | MEDIUM |
| MEM-009 | Value Validation | PM | 1h | LOW |

### Phase 3: Planning (MEM-010..017) — 23h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-010 | Vision | PM | 3h | MEDIUM |
| MEM-011 | Objectives | PM | 2h | MEDIUM |
| MEM-012 | Scope | SA | 4h | HIGH |
| MEM-013 | Stakeholders | PJM | 2h | LOW |
| MEM-014 | Risks | PJM | 3h | MEDIUM |
| MEM-015 | Timeline | PJM | 4h | HIGH |
| MEM-016 | Milestones | PJM | 3h | MEDIUM |
| MEM-017 | Budget & Resources | PM | 2h | LOW |

### Phase 4: Analysis (MEM-018..025) — 41h

| Task | Título | Rol PJM | **Rol TL** | Horas | Complexity |
|------|--------|---------|------------|-------|------------|
| MEM-018 | Functional Requirements | SA | SA | 6h | HIGH |
| MEM-019 | Non-Functional Requirements | AR | AR | 4h | HIGH |
| MEM-020 | Use Cases | SA | SA | 5h | MEDIUM |
| MEM-021 | User Stories | SA | SA | 8h | HIGH |
| **MEM-022** | **Business Rules** | **TL** | ⚠️ **SA** | 4h | HIGH |
| MEM-023 | User Flows | UX | UX | 4h | MEDIUM |
| MEM-024 | Acceptance Criteria | SA | SA | 6h | HIGH |
| MEM-025 | Traceability Matrix | SA | SA | 4h | MEDIUM |

### Phase 5: Design UX/UI (MEM-026..038) — 35h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-026 | Personas | UX | 3h | MEDIUM |
| MEM-027 | Information Architecture | UX | 4h | MEDIUM |
| MEM-028 | Design System | DL | 3h | MEDIUM |
| MEM-029 | Wireframes — Dashboard | DL | 4h | HIGH |
| MEM-030 | Wireframes — Timeline | DL | 3h | MEDIUM |
| MEM-031 | Wireframes — Viewer | DL | 4h | HIGH |
| MEM-032 | Wireframes — Cost Report | DL | 4h | HIGH |
| MEM-033 | Wireframes — Lista Convs | DL | 2h | MEDIUM |
| MEM-034 | Wireframes — Import Manual | DL | 2h | MEDIUM |
| MEM-035 | Wireframes — Health | DL | 2h | MEDIUM |
| MEM-036 | Wireframes — Extras | DL | 1h | LOW |
| MEM-037 | Design Handoff — Assets | DL | 2h | MEDIUM |
| **MEM-038** | **Design Handoff — Final** | **DL** | **DL** | 1h | LOW |

> ⚠️ **HITO crítico:** MEM-038 (Design Handoff) bloquea MEM-081 (inicio de FE).

### Phase 6: Design Technical (MEM-039..047) — 45h

| Task | Título | Rol PJM | **Rol TL** | Horas | Complexity |
|------|--------|---------|------------|-------|------------|
| **MEM-039** | **Solution Architecture** | **TL** | ⚠️ **AR** | 6h | HIGH |
| MEM-040 | Code Architecture | TL | TL | 4h | HIGH |
| MEM-041 | Database Design | DB | DB | 6h | HIGH |
| MEM-042 | API Design | BE | BE | 8h | HIGH |
| MEM-043 | Sequence Diagrams | AR | AR | 6h | HIGH |
| MEM-044 | Architecture Decision Records | TL | TL | 4h | MEDIUM |
| MEM-045 | Security Plan | AR | AR | 4h | HIGH |
| MEM-046 | Infrastructure Plan | DO | DO | 4h | MEDIUM |
| MEM-047 | Technical Estimates | TL | TL | 3h | MEDIUM |

### Phase 7: Development (MEM-048..093) — 116h

#### S01: Schema + Seeds (MEM-048..052) — 9h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-048 | DB Schema Prisma completo | DB | 3h | HIGH |
| MEM-049 | Migraciones + Partial Indexes | DB | 2h | MEDIUM |
| MEM-050 | Seed Catálogos | DB | 1h | LOW |
| MEM-051 | Setup Express + estructura | BE | 2h | MEDIUM |
| MEM-052 | Catalog Cache startup | BE | 1h | LOW |

#### S02: Import + Timeline (MEM-053..057) — 12h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-053 | POST /import (SDK/CLI/Web/ChatGPT) | BE | 4h | HIGH |
| MEM-054 | POST /import-review (VTT_CHANNEL) | BE | 2h | MEDIUM |
| MEM-055 | POST /upload (manual) | BE | 3h | HIGH |
| MEM-056 | GET /agents/:id/timeline | BE | 2h | MEDIUM |
| MEM-057 | Error handling + cleanup delegation | BE | 1h | LOW |

#### S03: Content + Context (MEM-058..062) — 12h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-058 | GET /conversations/:id/content (parse storage) | BE | 2h | MEDIUM |
| MEM-059 | GET /context (<500ms fail-fast) | BE | 4h | HIGH |
| MEM-060 | Classifier determinístico (topics/workType) | BE | 2h | HIGH |
| MEM-061 | Tests performance context | QA | 2h | MEDIUM |
| MEM-062 | Tests classifier | QA | 2h | MEDIUM |

#### S04: Adapters + Cleanup (MEM-063..068) — 12h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-063 | Adapter CLAUDE_WEB | BE | 3h | MEDIUM |
| MEM-064 | Adapter CHATGPT | BE | 2h | MEDIUM |
| MEM-065 | Storage writer JSONL | BE | 2h | MEDIUM |
| MEM-066 | Cleanup cron (5 min) | BE | 2h | MEDIUM |
| MEM-067 | Status transitions handler | BE | 1h | LOW |
| MEM-068 | Tests adapters | BE | 2h | MEDIUM |

#### S05: Lista + Cost + Dashboard (MEM-069..074) — 11h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-069 | GET /conversations (lista) | BE | 2h | MEDIUM |
| MEM-070 | GET /projects/:id/cost-report | BE | 2h | MEDIUM |
| MEM-071 | GET /agents/:id/cost-report | BE | 2h | MEDIUM |
| MEM-072 | GET /dashboard/stats | BE | 2h | MEDIUM |
| MEM-073 | GET /health | BE | 2h | MEDIUM |
| MEM-074 | Integration tests endpoints | BE | 1h | LOW |

#### S06: Docker + Integration (MEM-075..080) — 14h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-075 | Dockerfile + docker-compose | DO | 2h | MEDIUM |
| MEM-076 | CI config | DO | 2h | MEDIUM |
| MEM-077 | Env vars + secrets | DO | 1h | LOW |
| MEM-078 | Integración Hook Manager VTT | BE | 4h | HIGH |
| MEM-079 | E2E test Runtime integration | QA | 3h | HIGH |
| MEM-080 | E2E test Prompt Builder integration | QA | 2h | MEDIUM |

#### UI-01: Setup + Timeline + Viewer (MEM-081..085) — 16h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-081 | Setup React + Vite + Tailwind | FE | 2h | MEDIUM |
| MEM-082 | Routing + layout base | FE | 1h | LOW |
| MEM-083 | Page: Timeline agente | FE | 5h | HIGH |
| MEM-084 | Component: Conversation Viewer | FE | 6h | HIGH |
| MEM-085 | Auth context (SERVICE_KEY) | FE | 2h | MEDIUM |

#### UI-02: Dashboard + Cost + Import (MEM-086..088) — 12h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-086 | Page: Dashboard stats | FE | 4h | HIGH |
| MEM-087 | Page: Cost report proyecto | FE | 4h | MEDIUM |
| MEM-088 | Page: Import manual (upload) | FE | 4h | MEDIUM |

#### UI-03: Viewer REVIEW + Lista (MEM-089..090) — 10h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-089 | Page: Lista conversaciones | FE | 5h | HIGH |
| MEM-090 | Component: AGENT_REVIEW multi-agent | FE | 5h | HIGH |

#### UI-04: Cost Agente + Health (MEM-091..093) — 8h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-091 | Page: Cost report por agente | FE | 3h | MEDIUM |
| MEM-092 | Page: Health status | FE | 2h | LOW |
| MEM-093 | Polish + responsive | FE | 3h | MEDIUM |

### Phase 8: Testing (MEM-094..103) — 60h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-094 | Test Planning | QA | 4h | MEDIUM |
| MEM-095 | Test Cases completos | QA | 8h | HIGH |
| MEM-096 | Test Environment setup | DO | 4h | MEDIUM |
| MEM-097 | Functional Testing | QA | 8h | HIGH |
| MEM-098 | Integration Testing | QA | 6h | HIGH |
| MEM-099 | E2E Testing | QA | 8h | HIGH |
| MEM-100 | Performance Testing (<500ms context) | QA | 6h | HIGH |
| MEM-101 | Security Testing | AR | 4h | HIGH |
| MEM-102 | UAT | PM | 4h | MEDIUM |
| MEM-103 | Bug Fixes | BE | 8h | HIGH |

### Phase 9: Deploy (MEM-104..110) — 26h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-104 | Infrastructure Setup | DO | 4h | MEDIUM |
| MEM-105 | CI/CD Configuration | DO | 6h | HIGH |
| MEM-106 | Staging Deploy | DO | 4h | MEDIUM |
| MEM-107 | Smoke Testing | QA | 3h | MEDIUM |
| MEM-108 | Production Deploy | DO | 4h | HIGH |
| MEM-109 | Post-Deploy Monitoring | DO | 3h | MEDIUM |
| MEM-110 | Rollback Plan (doc) | TL | 2h | MEDIUM |

### Phase 10: Operations (MEM-111..116) — 15h

| Task | Título | Rol | Horas | Complexity |
|------|--------|-----|-------|------------|
| MEM-111 | Monitoring setup | DO | 3h | MEDIUM |
| MEM-112 | User Support docs | PM | 2h | LOW |
| MEM-113 | Bug Fixes Operations playbook | TL | 2h | MEDIUM |
| MEM-114 | Incremental Improvements | PM | 3h | MEDIUM |
| MEM-115 | Security Updates | AR | 2h | MEDIUM |
| MEM-116 | Scaling plan | AR | 3h | HIGH |

---

## MIS TAREAS COMO TL (ejecutor) — post-reassignments

| Task | Título | Fase | Horas |
|------|--------|------|-------|
| MEM-040 | Code Architecture | Design Technical | 4h |
| MEM-044 | Architecture Decision Records | Design Technical | 4h |
| MEM-047 | Technical Estimates | Design Technical | 3h |
| MEM-110 | Rollback Plan (doc) | Deploy | 2h |
| MEM-113 | Bug Fixes Operations (doc) | Operations | 2h |

**Total:** 5 tareas, 15h

## MIS TAREAS COMO TL (reviewer)

Todas las tareas de: **BE (28), DB (4), FE (13), QA (11), DO (12)** = **68 tareas** que pasan por `task_in_review` conmigo como reviewer.

Code review además de:
- Tareas de arquitectura (AR: 7, SA: 8) donde tenga impacto en código/implementación.

---

## DEPENDENCIAS CRÍTICAS (a crear manualmente hasta que VTT tenga endpoint)

| From | To | Razón | Impacto |
|------|-----|-------|---------|
| MEM-048..052 | MEM-053 | S02 depende de S01 (schema+setup) | Alto |
| MEM-053..057 | MEM-058 | S03 depende de S02 | Medio |
| MEM-058..062 | MEM-063 | S04 depende de S03 | Medio |
| MEM-063..068 | MEM-069 | S05 depende de S04 | Medio |
| MEM-069..074 | MEM-075 | S06 depende de S05 | Medio |
| **MEM-038** | **MEM-081** | **HITO DL→FE** | **CRÍTICO** |
| MEM-081..085 | MEM-086 | UI-02 depende de UI-01 | Alto |
| MEM-086..088 | MEM-089 | UI-03 depende de UI-02 | Alto |
| MEM-089..090 | MEM-091 | UI-04 depende de UI-03 | Alto |

---

## PENDIENTES ANTES DEL KICKOFF

| # | Item | Responsable |
|---|------|-------------|
| 1 | PM valida los 2 reassignments propuestos (MEM-022, MEM-039) | PM |
| 2 | PM/DO ejecuta script PATCH del HO v2.1 (asigna 116 tareas) | PM/DO |
| 3 | PM confirma sprint dates para las 116 tareas (el plan 52/14 quedó obsoleto) | PM |
| 4 | PM define multi-repo | PM |
| 5 | Endpoint VTT para crear dependencias | DO + PM |
| 6 | Resolver gotcha `deliveryId` no persiste en GET task | PM + backend VTT |

---

**Mantenimiento:** este archivo se actualiza cuando:
- PM aprueba/rechaza reassignments propuestos
- Aparecen nuevas tareas en VTT (cambios de alcance)
- Se redistribuyen horas tras re-estimación
