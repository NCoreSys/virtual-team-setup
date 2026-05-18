# HANDOFF — PJM: Ejecución Fases 4-7 Memory Service R1

**Para:** PJM Agent (`0ff63a29-0bc0-465a-b9bd-5f71476bc91d`)
**De:** PM — Martin Rivas (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)
**Fecha:** 2026-05-12
**Estado:** Design Technical (Phase 3B) completado por TL. Listo para iniciar ejecución.

---

## 1. Contexto

Memory Service R1 completó Discovery, Planning, Analysis y Design. El TL produjo 9 documentos de estimación (3B.9.1 a 3B.9.9) que definen completamente la ejecución de Fases 4-7. Este handoff traduce esos documentos en un plan operativo para que el PJM gestione los sprints.

**Fuente de verdad técnica:** SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md (43 decisiones cerradas)
**Fuente de estimaciones:** 3B.9.1 a 3B.9.9 (TL, 2026-05-12, v2.0)

---

## 2. Números Clave

| Métrica | Valor |
|---------|-------|
| Deliverables ✅ aplica R1 | 174 |
| Deliverables ⚪ opcionales | 9 (24h) |
| Horas estimadas (expected) | 719h |
| Horas risk-adjusted | 766h (+47h buffers) |
| Best case | ~575h (−20%) |
| Worst case | ~900h (+25%) |
| Sprints | 8 sprints × 2 semanas |
| Duración total | ~16 semanas (~4 meses) |
| Equipo | 6 roles: TL, BE, FE, DB, QA, DO |
| Riesgos cuantificados | 15 (46.75h de buffer total) |
| Milestones | 8 (M1 a M7 + M5b) |
| Scale: 1 SP ≈ 1h | Escala lineal directa |

---

## 3. Equipo y Roles

| Rol | UUID | Horas ✅ | % | Fases activas | Pico de carga |
|-----|------|:-------:|:-:|:-------------:|:-------------:|
| BE | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | 205h | 28.5% | F4, F5, F7 | S2-S3 (~50-60h) |
| QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | 186h | 25.9% | F4-F7 | S5-S6 (~60-70h) |
| DO | `322e3745-9756-4a7c-af11-44b33edef44d` | 145h | 20.2% | F4-F7 | S7 (~50h) |
| FE | `d23c9cd9-a156-433b-8900-94add5488eec` | 73h | 10.2% | F4 | S3-S4 (~40-50h) |
| DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | 57h | 7.9% | F4-F6 | S1-S2 (~30-40h) |
| TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` | 37h | 5.1% | F4-F7 | Continuo (~4-6h/sprint) |
| Cross | — | 16h | 2.2% | F6-F7 | — |
| **Total** | | **719h** | **100%** | | |

**Reviewer por fase:**
- Fase 4 (Development): TL revisa todos los PRs
- Fase 5 (Testing): TL revisa resultados y sign-offs
- Fase 6 (Deploy): TL revisa producción
- Fase 7 (Operations): TL + PM

---

## 4. Calendario de Sprints

| Sprint | Semanas | Fechas | Fase | Horas | Roles activos | Milestone |
|:------:|:-------:|:------:|:----:|:-----:|:-------------:|:---------:|
| S1 | 1-2 | 2026-06-01 / 06-14 | F4 | 61h | TL+BE+DB+DO | M1 |
| S2 | 3-4 | 2026-06-15 / 06-28 | F4 | 75h | TL+BE+DB | M2 |
| S3 | 5-6 | 2026-06-29 / 07-12 | F4 | 77h | TL+BE+FE | M3 |
| S4 | 7-8 | 2026-07-13 / 07-26 | F4 | 73h | TL+BE+FE | M4 |
| S5 | 9-10 | 2026-07-27 / 08-09 | F5 | 84h | TL+QA+DO+DB | M5 |
| S6 | 11-12 | 2026-08-10 / 08-23 | F5 | 75h | TL+QA+BE | M5b |
| S7 | 13-14 | 2026-08-24 / 09-06 | F6 | 73h | TL+DO+DB+QA | M6 |
| S8 | 15-16 | 2026-09-07 / 09-20 | F6+F7 | 62h | TL+DO | M7 |

---

## 5. Detalle por Sprint — Deliverables y Asignaciones

### Sprint S1 — Infra & BD Foundation (61h)

**Objetivo:** Containers operativos, BD migrada con 29 entidades, seed de catálogos, foundation de error handling y logging.

| ID | Deliverable | Rol | Horas | Dependencia |
|----|-------------|:---:|:-----:|-------------|
| 4.1.1 | Development Environment | DO | 5 | 3B.8.1 |
| 4.1.2 | Environment Setup Guide | DO | 3 | 4.1.1 |
| 4.1.3 | Environment Variables | DO | 3 | 3B.8.5 |
| 4.1.4 | Docker Compose | DO | 5 | 3B.8.1 |
| 4.1.5 | Makefile/Scripts | DO | 3 | 4.1.4 |
| 4.1.6-10 | IDE + Linter + Formatter + Pre-commit + Git | TL | 10 | 3B.2.1 |
| 4.3.14 | Error Handling — AppError + MEM-ERR-xxx | BE | 8 | 3B.4.5 |
| 4.3.15 | Logging — Winston + correlationId | BE | 5 | — |
| 4.2.1 | Initial Migration — 29 entidades | DB | 8 | 3B.3.2 |
| 4.2.2 | Schema Migrations setup | DB | 8 | 4.2.1 |
| 4.2.6 | Constraints | DB | 3 | 4.2.1 |

**Gate M1:** ✓ Containers UP ✓ BD migrada ✓ Seed OK ✓ AppError compilando

---

### Sprint S2 — Core Backend (75h)

**Objetivo:** Catálogos cargados, índices aplicados, middleware chain completo, services implementados.

| ID | Deliverable | Rol | Horas | Dependencia |
|----|-------------|:---:|:-----:|-------------|
| 4.2.3 | Seed Data — 10 catálogos | DB | 8 | 4.2.1 |
| 4.2.4 | Test Data | DB | 5 | 4.2.3 |
| 4.2.5 | Indexes — partial + GIN + composite | DB | 8 | 4.2.1 |
| 4.2.9 | Migration Guide | DB | 3 | 4.2.2 |
| 4.2.10 | Rollback Scripts | DB | 5 | 4.2.2 |
| 4.3.7 | Middlewares — Auth + Validation + RateLimit + ErrorHandler | BE | 8 | 4.3.14 |
| 4.3.5 | DTOs/Schemas — Zod | BE | 5 | 3B.4.2 |
| 4.3.3 | Models — Prisma client + catalogCache | BE | 5 | 4.2.1 |
| 4.3.4 | Repositories — ConversationRepository | BE | 8 | 4.2.1, 4.3.3 |
| 4.3.2 | Services — Import + ContextQuery + Classifier + CostCalc + Storage | BE | 13 | 4.3.4, 4.2.3 |
| 4.3.8 | Utils — path sanitization + correlationId | BE | 3 | — |
| — | TL: Reviews + coordinación | TL | 4 | — |

**Gate M2:** ✓ Auth MW activo ✓ catalogCache cargado ✓ Zod schemas OK ✓ ConversationRepository testeado

---

### Sprint S3 — Features BE + FE Start (77h)

**Objetivo:** 11 endpoints funcionales, 3 integraciones, FE foundation desplegada.

| ID | Deliverable | Rol | Horas | Dependencia |
|----|-------------|:---:|:-----:|-------------|
| 4.3.1 | API Endpoints — 11 endpoints | BE | 13 | 4.3.7, 4.3.2, 4.2.1 |
| 4.3.6 | Workers — Cleanup Job | BE | 8 | 4.3.2 |
| 4.5.1 | Integration Code — 3 integraciones | BE | 8 | 4.3.2 |
| 4.5.2 | API Clients (consumidores) | BE | 5 | 4.3.1 |
| 4.5.3 | Webhooks — POST /import-review | BE | 5 | 4.3.1 |
| 4.5.5 | Third-party SDKs — ioredis, node-cron, multer | BE | 3 | — |
| 4.4.1 | Components — shared + layout | FE | 8 | 3B wireframes |
| 4.4.3 | Layouts | FE | 3 | 4.4.1 |
| 4.4.4 | Hooks — useConversations, useContext, useCosts | FE | 5 | 4.3.1 |
| 4.4.5 | State Management | FE | 5 | — |
| 4.4.6 | API Client FE | FE | 5 | 4.3.1 |
| 4.4.7 | Types/Interfaces — @NCoreSys/api-types | FE | 3 | 3B.4.2 |
| 4.4.8 | Styles — Tailwind setup | FE | 3 | — |
| — | TL: Reviews + SLA check preliminar | TL | 3 | — |

**Gate M3:** ✓ POST /import e2e OK ✓ JSONL procesado ✓ Estado IMPORTED en BD ✓ FE foundation desplegada

---

### Sprint S4 — FE Features + Context SLA (73h)

**Objetivo:** 8 pantallas FE renderizan, GET /context <500ms validado, unit tests BE passing.

| ID | Deliverable | Rol | Horas | Dependencia |
|----|-------------|:---:|:-----:|-------------|
| 4.4.2 | Pages — 8 pantallas | FE | 13 | 4.4.1, 4.3.1 |
| 4.4.9 | Utils FE | FE | 2 | — |
| 4.4.15 | Responsive Implementation | FE | 5 | 4.4.2 |
| 4.4.10 | Unit Tests FE | FE | 5 | 4.4.2 |
| 4.4.11 | Component Tests | FE | 5 | 4.4.1 |
| 4.4.13 | Frontend README | FE | 2 | 4.4.2 |
| 4.5.8+9 | Error Handling Integ. + Retry Logic | BE | 10 | 4.5.1 |
| 4.5.6 | Integration Tests | BE | 8 | 4.3.1, 4.5.1 |
| 4.5.7 | Integration Docs | BE | 3 | 4.5.6 |
| 4.3.11 | API Documentation — Swagger | BE | 5 | 4.3.1 |
| 4.3.12 | Postman Collection | BE | 3 | 4.3.11 |
| 4.3.9 | Unit Tests BE | BE | 8 | 4.3.1-7 |
| — | TL: Reviews + SLA validation prep | TL | 4 | — |

**Gate M4 (MILESTONE DE MAYOR RIESGO):** ✓ GET /context <500ms p95 en staging ✓ 8 pantallas FE renderizan ✓ Unit tests BE passing

⚠️ **Si M4 falla (SLA <500ms):** (1) EXPLAIN ANALYZE en staging para query más lenta, (2) agregar índice compuesto faltante, (3) re-ejecutar k6 con 50 VU, (4) si no resuelve en 3 días → escalar a TL (+20h buffer R-01)

---

### Sprint S5 — Testing Phase 1 (84h)

**Objetivo:** Functional, integration y E2E tests passing. Test environment estable.

| ID | Deliverable | Rol | Horas | Dependencia |
|----|-------------|:---:|:-----:|-------------|
| 5.1.1-5 | Test Plan + Strategy + Scope + Schedule + Resources | QA | 14 | — |
| 5.2.1-4 | Test Cases Document + IDs + Data + Expected Results | QA | 18 | 5.1.1 |
| 5.3.1 | Test Environment | DO | 5 | 4.1.4 |
| 5.3.2-4 | Test Database + Seeding + Docs | DB | 8 | 4.2.3 |
| 5.4.1-5 | Functional Test Results + Log + Defects + Summary + Evidence | QA | 17 | 4.3.1, 5.2.1 |
| 5.5.1-4 | Integration Test Suite + Results + API Contracts + Coverage | QA | 18 | 4.3.1, 4.5.1 |
| — | TL: Coordinación testing | TL | 4 | — |

**Gate M5:** ✓ Functional tests pass ✓ Integration tests pass ✓ E2E críticos pass

---

### Sprint S6 — Testing Phase 2 + Docs + Reviews (75h)

**Objetivo:** Performance validado (SLA <500ms), security sign-off, UAT sign-off, documentación completa, code review cerrado.

| ID | Deliverable | Rol | Horas | Dependencia |
|----|-------------|:---:|:-----:|-------------|
| 5.6.1-5 | E2E Test Suite + Results + Critical Path + Visual Reg. + Docs | QA | 19 | 4.4.2 |
| 5.7.1-6 | Load Test Plan + Results + Stress + Metrics + Bottleneck + Recs | QA | 24 | 4.3.1, 4.2.5 |
| 5.8.1-7 | Security Test Plan + PenTest + Scan + OWASP + Findings + Remed. + Sign-off | QA+TL | 24 | 4.3.7 |
| 5.10.1-5 | UAT Plan + Cases + Results + Feedback + Sign-off | TL | 13 | 5.5, 5.6 |
| 5.11.1-3 | Bug Fixes + Regression Tests + Bug Report | BE+QA | 15 | 5.4-5.8 |
| 4.6.1-7 | Unit Tests QA + Coverage + Mocks + Fixtures + Utils | QA | 30 | 4.3.1-7 |
| 4.3.10 | Integration Tests BE | BE | 8 | 4.3.1 |
| 4.7.1-8 | Tech Docs: READMEs + Contributing + Changelog | TL+BE | 24 | Todos F4 |
| 4.8.1-4 | Code Review: PRs + Quality + Debt + Refactoring | TL | 22 | Todos F4 |

**Gate M5b:** ✓ Load test: GET /context <500ms p95 con 50 VU ✓ Security sign-off ✓ UAT sign-off

---

### Sprint S7 — Deploy Staging (73h)

**Objetivo:** Staging live en Hetzner, CI/CD activo, smoke tests passing.

| ID | Deliverable | Rol | Horas | Dependencia |
|----|-------------|:---:|:-----:|-------------|
| 6.1.1-4 | Infrastructure + Servers + Network + Security Groups | DO | 16 | 3B.8.1 |
| 6.1.6+8 | Database Ready + SSL | DO | 8 | 6.1.1 |
| 6.2.1 | CI Pipeline — GitHub Actions 4 repos | DO | 8 | 6.1.1 |
| 6.2.2 | CD Pipeline — staging + producción | DO | 8 | 6.2.1 |
| 6.2.3-6 | Build Scripts + Deploy Scripts + Env Configs + CI/CD Docs | DO | 13 | 6.2.1 |
| 6.3.1-2 | Staging Deploy + URL | DO | 7 | 6.2.2 |
| 6.3.3 | Migration Run en staging | DB | 3 | 6.3.1 |
| 6.3.4 | Health Check staging | DO | 2 | 6.3.1 |
| 6.4.1-3 | Smoke Test Results + Critical Paths + Sign-off | QA+TL | 6 | 6.3.1 |
| — | TL: Coordinación deploy | TL | 2 | — |

**Gate M6:** ✓ Staging live en 77.42.88.106 ✓ Smoke tests OK ✓ CI/CD activo

---

### Sprint S8 — Deploy Producción + Operations Inicio (62h)

**Objetivo:** Sistema live en producción, monitoring activo, rollback probado, equipo en operations.

| ID | Deliverable | Rol | Horas | Dependencia |
|----|-------------|:---:|:-----:|-------------|
| 6.5.1-6 | Production Deploy + URL + DNS + SSL + Release Notes + Log | DO+TL | 13 | M6 |
| 6.6.1-2 | Monitoring Dashboard + Alerts | DO | 8 | 6.5.1 |
| 6.6.6 | Post-Deploy Report 24h | DO | 2 | 6.5.1 |
| 6.7.1-5 | Rollback Plan + Scripts + Tested + Runbook + Criteria | DO | 13 | 6.5.1 |
| 7.1.1-4 | Uptime + Performance + Error + Weekly Reports | DO+TL | 12 | 6.6.1 |
| 7.2.1+3+4 | Support Process + SLA Definitions + Metrics | TL | 7 | 6.5.1 |
| 7.3.1+3 | Hotfix Process + Bug Tracking | TL | 4 | 6.7.1 |
| — | TL: Release sign-off + coordinación | TL | 3 | — |

**Gate M7 (FINAL):** ✓ Producción live ✓ Monitoring activo ✓ Rollback probado ✓ Equipo en operations

🎯 **Memory Service R1 = ENTREGADO**

---

## 6. Milestones y Gates GO/NO-GO

| Milestone | Sprint | Fecha | Criterios | Quién valida |
|:---------:|:------:|:-----:|-----------|:------------:|
| **M1** | S1 fin | 2026-06-14 | Containers UP, BD migrada, seed OK, AppError compilando | TL |
| **M2** | S2 fin | 2026-06-28 | Auth MW activo, catalogCache cargado, Zod OK, Repository testeado | TL |
| **M3** | S3 fin | 2026-07-12 | POST /import e2e OK, JSONL procesado, IMPORTED en BD, FE foundation | TL |
| **M4** | S4 fin | 2026-07-26 | **GET /context <500ms p95 en staging** — milestone de mayor riesgo | TL + QA |
| **M5** | S5 fin | 2026-08-09 | Functional + integration + E2E tests pass | QA + TL |
| **M5b** | S6 fin | 2026-08-23 | Load test <500ms p95 50VU, security sign-off, UAT sign-off | QA + TL |
| **M6** | S7 fin | 2026-09-06 | Staging live, smoke tests OK, CI/CD activo | DO + TL |
| **M7** | S8 fin | 2026-09-20 | **Producción live**, monitoring activo, rollback probado | PM |

---

## 7. Critical Path

```
4.1.1 Dev Env → 4.2.1 Migration → 4.3.7 Middlewares → 4.3.2 Services → 4.3.1 Endpoints
                                                                              ↓
                                         4.4.2 Pages → 5.6.1 E2E Tests → 5.10.5 UAT Sign-off
                                                                              ↓
                                         4.2.5 Indexes → 5.7.2 Load Tests → 6.2.x CI/CD
                                                                              ↓
                                                              6.3.1 Staging → 6.5.1 Production → Fase 7
```

**Deliverables en critical path (bloquean todo si se retrasan):**
1. 4.1.1 Development Environment — sin env no hay nada
2. 4.2.1 Initial Migration — sin BD no hay endpoints
3. 4.3.7 Middlewares — auth + validation obligatorios
4. 4.3.1 API Endpoints — sin APIs no hay UI ni testing
5. 4.4.2 Pages — sin UI no hay E2E ni UAT
6. 5.7.2 Load Test Results — gate de calidad SLA <500ms
7. 6.5.1 Production Deploy — release R1

---

## 8. Top 15 Riesgos Cuantificados

| ID | Riesgo | Prob. | Buffer (h) | Sprint afectado | Mitigación |
|----|--------|:-----:|:----------:|:---------------:|------------|
| R-01 | GET /context no cumple SLA <500ms | 0.40 | +8.0h | S4 | EXPLAIN ANALYZE en staging, índices adicionales |
| R-02 | Runtime v1.1 cambia contrato | 0.25 | +6.0h | S3 | Congelar versión antes de S2 |
| R-03 | PB v1.3 incompatible con context query | 0.20 | +4.0h | S3 | Revisar spec PB en S1 |
| R-04 | Hook Manager cambia formato VTT_CHANNEL | 0.20 | +3.2h | S3 | Obtener spec HM en S1 |
| R-05 | P2002 concurrente en import | 0.30 | +2.4h | S2-S3 | Retry con backoff en ImportService |
| R-06 | Partial indexes insuficientes | 0.25 | +2.5h | S2, S6 | EXPLAIN ANALYZE en staging |
| R-07 | TS strict genera rework en Prisma | 0.35 | +2.8h | S2-S3 | Leer types Prisma antes de escribir services |
| R-08 | Filesystem bind mount lleno | 0.20 | +1.6h | S3-S4 | Monitoreo de disco en staging |
| R-09 | Redis no disponible | 0.15 | +1.5h | S2 | Fallback sin rate limiting |
| R-10 | Renovate no bumps api-types | 0.20 | +1.6h | S3, S7 | Bump manual si falla |
| R-11 | GIN index degradado bajo carga | 0.15 | +1.5h | S6 | k6 con 50 VU valida |
| R-12 | CI/CD falla en primer deploy prod | 0.35 | +4.2h | S7-S8 | Deploy staging primero, rollback automático |
| R-13 | Seed catálogos orden FK incorrecto | 0.25 | +1.25h | S2 | Validar orden de FK deps antes de seed |
| R-14 | Playwright tests flaky en CI | 0.40 | +3.2h | S5-S6 | Retry automático, tests deterministas |
| R-15 | k6 descubre N+1 queries | 0.30 | +3.0h | S6 | Logging query count por request |
| | **Total buffer riesgo** | | **+46.75h** | | |

---

## 9. Paralelismo por Sprint

| Sprint | Agentes simultáneos | Tracks paralelos |
|:------:|:-------------------:|:----------------:|
| S1 | 4 (TL+BE+DB+DO) | Infra // BD // Error+Logging // Config |
| S2 | 3 (TL+BE+DB) | Seed+Indexes // Middlewares+Services |
| S3 | 3 (TL+BE+FE) | Endpoints+Integraciones // FE Foundation |
| S4 | 3 (TL+BE+FE) | Pages FE // Tests BE // Docs |
| S5 | 4 (TL+QA+DO+DB) | Test Plan+Cases // Test Env // Functional+Integration |
| S6 | 3 (TL+QA+BE) | E2E+Perf+Security // Bug Fixes // Docs+Reviews |
| S7 | 4 (TL+DO+DB+QA) | Infra+CI/CD // Staging Deploy // Smoke |
| S8 | 2 (TL+DO) | Prod Deploy // Monitoring // Rollback |

**Máximo 4 agentes simultáneos.** Sin conflictos cross-repo por scope claro en ASSIGNMENTs.

---

## 10. Indicadores de Tracking

### 10.1 Métricas por Sprint

| Indicador | Fórmula | Verde | Amarillo | Rojo |
|-----------|---------|:-----:|:--------:|:----:|
| Varianza de horas | (reales - estimadas) / estimadas × 100 | ±10% | ±15% | >±15% |
| Deliverables completados | completados / planificados × 100 | ≥80% al 75% del sprint | ≥60% | <60% |
| PRs pendientes de review | count PRs open > 48h | 0 | 1-2 | >2 |
| Blockers activos | count blockers sin resolver | 0 | 1 | >1 |

### 10.2 Reglas de Escalación al PM

| Situación | Acción |
|-----------|--------|
| Varianza acumulada > +15% | PJM notifica PM. Evaluar replanificación. |
| Sprint con Δ > +50% en horas | PM revisa estimación con TL. |
| 2 sprints consecutivos con desvío | PM convoca revisión de estimaciones restantes. |
| Milestone GO/NO-GO = NO-GO | PM decide: buffer adicional, reducción scope, o escalación. |
| Riesgo R-01 materializado (SLA) | PM + TL definen plan de acción en 24h. |
| Riesgo R-02/R-03/R-04 materializado (integración) | PM congela contrato o escala. |

---

## 11. Deliverables Opcionales (⚪) — No planificar, disponibles si hay margen

| ID | Deliverable | Horas | Fase | Condición para incluir |
|----|-------------|:-----:|:----:|------------------------|
| 4.4.12 | Storybook | 3h | F4 | S4 termina antes de tiempo |
| 4.4.14 | Accessibility | 3h | F4 | S4 termina antes de tiempo |
| 5.9.1-3 | Accessibility Testing (3 deliverables) | 9h | F5 | S6 termina antes de tiempo |
| 6.6.3-5 | Performance Baseline + Scaling Docs + Capacity Plan | 9h | F6 | S7 termina antes de tiempo |

**Total ⚪:** 24h. Solo si hay margen. Nunca a costa del critical path.

---

## 12. Contingencias

| Situación | Acción |
|-----------|--------|
| S2 sin catalogCache | BLOQUEAR 4.3.1 endpoints hasta resolución |
| SLA <500ms no cumplido en M4 | EXPLAIN ANALYZE + índices + aumentar CONTEXT_TIMEOUT_MS a 600ms temporal |
| S4 supera 90h | Mover 4.4.14 Accessibility y 4.4.12 Storybook (⚪) a backlog R2 |
| Bugs críticos en S5 | BE regresa a S6 con 8h adicionales para hotfixes |
| Deploy staging falla en S7 | Rollback CI/CD automático. Logs en 2h. Re-deploy en 24h. |
| Deploy producción falla en M7 | Rollback plan 6.7 activo. RCA en 48h. |
| Agente bloqueado por dependencia cross-repo | TL bump manual, desbloqueo en <4h |

---

## 13. Documentos de Referencia

| Documento | Qué contiene | Cuándo consultar |
|-----------|-------------|:----------------:|
| 3B.9.1 estimates_doc | Resumen ejecutivo, escenarios, milestones | Inicio de cada sprint |
| 3B.9.2 story_points | SP por fase, por rol, top 8 VERY HIGH | Asignar tareas |
| 3B.9.3 task_breakdown | Catálogo completo 174 deliverables con horas/rol/dependencias | Crear ASSIGNMENTs |
| 3B.9.4 effort_matrix | Rol × Fase × Subfase (horas detalladas) | Verificar carga por agente |
| 3B.9.5 complexity_analysis | Top 10 deliverables complejos, riesgos por stack | Priorizar reviews TL |
| 3B.9.6 risk_adjusted_estimates | 15 riesgos cuantificados, buffers, worst case | Gestión de riesgos |
| 3B.9.7 dependencies_map | Critical path, gates entre fases, orden de implementación | Secuenciar tareas |
| 3B.9.8 velocity_assumptions | SP/sprint por rol, supuestos, factores de reducción | Calibrar velocity real |
| 3B.9.9 capacity_plan | Calendario detallado S1-S8, milestones GO/NO-GO | Tracking semanal |
| SPEC v1.9 | 43 decisiones cerradas, 11 endpoints, modelo de datos | Resolver dudas técnicas |
| ADDENDUM Bloque 0 Lite | Error handling + logging + seguridad base | Sprint S1 |

---

## 14. Definición de Done por Deliverable

Para que un deliverable cuente como completado:

- [ ] Artefacto existe en la ruta del catálogo (doc o código)
- [ ] Compila sin errores (`tsc --noEmit`)
- [ ] Tests unitarios passing (si aplica)
- [ ] DevLog en `knowledge/development-log/`
- [ ] Code Logic en `knowledge/code-logic/` (si es código)
- [ ] Commit con formato correcto + `Co-Authored-By: Claude Sonnet 4.x`
- [ ] PR creado y aprobado por TL
- [ ] Tarea movida a `task_in_review` en VTT

---

**Documento:** HO_PJM_EJECUCION_FASES_4-7_MEMORY_SERVICE.md
**Versión:** 1.0
**Fecha:** 2026-05-12
**Emitido por:** PM — Martin Rivas
**Para:** PJM (`0ff63a29-0bc0-465a-b9bd-5f71476bc91d`)
