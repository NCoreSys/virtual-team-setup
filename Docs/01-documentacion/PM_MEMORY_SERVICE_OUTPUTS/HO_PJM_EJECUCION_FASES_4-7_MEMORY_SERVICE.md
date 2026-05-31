# HANDOFF — Ejecución Fases 4-7 Memory Service R1
## Para: PJM Agent
**Fecha:** 2026-05-19
**Origen:** Design Technical (Phase 3B) completado — TL entregó 3B.9.1 a 3B.9.10
**Estado:** Fases 0-3B completadas. Crear tareas en VTT y arrancar S1.

---

## 1. Perfil y Rol

Eres el **Project Manager** del proyecto Memory Service.
- UUID: `0ff63a29-0bc0-465a-b9bd-5f71476bc91d`
- Reportas a: PM Martin Rivas (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)
- Tu función: crear sprints y tareas en VTT, emitir HANDOFFs por sprint al TL, monitorear avance, reportar desvíos al PM
- **NO apruebas tareas** — eso es del PM
- **NO haces code review** — eso es del TL
- **NO inventas detalle técnico** — usas el routing index (3B.9.10)

---

## 2. Contexto del Proyecto

**Memory Service:** Sistema centralizado de memoria operativa para agentes de IA del ecosistema VTT.
- Tech stack: Node.js 20 + Express 4.x + TypeScript 5.x strict + Prisma 5.x + PostgreSQL 15 + Redis 7.x
- API: puerto 3002 | UI: puerto 3003 (React 18 + Vite 5.x + Tailwind 3.x)
- Backend URL (VTT): `http://77.42.88.106:3000`
- Project ID: `d0fc276d-e764-4a83-96e9-d65f086ed803`
- Project Key: MS
- 4 repos: `memory-service-project`, `memory-service-api`, `memory-service-backend`, `memory-service-frontend`
- SPEC: `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — 43 decisiones cerradas, 11 endpoints, 29 entidades

---

## 3. Lo que se Completó

| Fase | Estado | Gate |
|------|:------:|------|
| Phase 0 — Discovery | ✅ | MS-009 Value Validation aprobado |
| Phase 1 — Planning | ✅ | MS-017 Budget & Resources cerrado |
| Phase 2 — Analysis | ✅ | Requerimientos validados contra Scope |
| Phase 3A — Design UX/UI | ✅ | MS-038 Design Handoff entregado |
| Phase 3B — Design Technical | ✅ | 3B.9.1 a 3B.9.10 entregados por TL |

**Lo que toca ahora:** crear sprints S1-S8 en VTT, generar HANDOFFs por sprint para el TL.

---

## 4. Decisiones YA Aprobadas (NO reabrir)

| # | Decisión | Valor |
|---|----------|-------|
| D-MEM-01 | Sistema standalone | BD propia `memory_service_db`, puerto 3002 |
| D-MEM-05/42 | Idempotencia | `@@unique([sourceId, externalSessionId])` → ALREADY_INDEXED |
| D-MEM-07/37 | SLA GET /context | <500ms p95, fail-fast `Promise.race` + `MEM-ERR-504` |
| D-MEM-08 | Clasificación | Reglas determinísticas, sin ML en R1 |
| D-MEM-14 | Fuentes | 5: CLAUDE_SDK, CLAUDE_CLI, CLAUDE_WEB, CHATGPT, VTT_CHANNEL |
| D-MEM-20 | Catálogos | En BD, extensibles sin migración |
| D-MEM-26 | Auth R1 | SERVICE_KEY solamente. JWT en R2 |
| D-MEM-35 | Cleanup job | Cada 5 min, max 3 retries, luego ERROR |
| D-MEM-38 | Cost report | `primaryAgentRole` desnormalizado |
| D-MEM-43 | Storage | Filesystem bind mount `/storage/` |
| Bloque 0 Lite | Fundamentos | AppError (MEM-ERR-xxx) + Winston + Helmet/CORS/rate limiting en S1 |

43 decisiones cerradas en total. Cualquier cambio requiere aprobación del PM.

---

## 5. Documento Clave: Routing Index (3B.9.10)

**Ruta:** `phases/03-design/deliverables/estimates/3B.9.10_routing_index.md`

Este documento es **obligatorio** para generar cualquier HANDOFF o ASSIGNMENT. Mapea cada uno de los 174 deliverables a su spec source, sección específica, decisiones D-MEM aplicables y documentos que el agente debe leer.

**Cómo usarlo:** Para cada deliverable del sprint, buscar su fila en 3B.9.10 y copiar las columnas al HANDOFF:

```
Ejemplo: deliverable 4.2.3 Seed Data

Routing index dice:
  Spec Source: 3B.3.7_seed_plan.md
  Sección: §catálogos — 10 tablas
  D-MEM: D-MEM-14, D-MEM-20, D-MEM-16
  Docs para el agente: 3B.3.7, 3B.3.2, 3B.3.5

Entonces en el HANDOFF al TL escribes:
  "4.2.3 Seed Data — DB — 8h
   Spec: 3B.3.7 §catálogos
   Docs: 3B.3.7, 3B.3.2, 3B.3.5
   Respetar: D-MEM-14, D-MEM-20, D-MEM-16"
```

**Regla:** si un doc referenciado en 3B.9.10 no existe en el repo → `task_on_hold` + notificar al TL. Nunca inventar el contenido.

---

## 6. Plan de Sprints — Fases 4-7

**Total:** 719h | 174 deliverables ✅ | 8 sprints × 2 semanas | ~16 semanas
**Risk-adjusted:** 766h (+47h buffers) | Worst case: ~900h

### S1: Infra & BD Foundation (~61h)

**Objetivo:** Containers operativos, BD migrada con 29 entidades, foundation de error handling y logging.
**Agentes:** DO + TL + BE + DB (4 en paralelo)

| ID | Deliverable | Rol | Horas | Spec Source (3B.9.10) |
|----|-------------|:---:|:-----:|----------------------|
| 4.1.1 | Development Environment | DO | 5 | 3B.8.1 §stack, §puertos |
| 4.1.2 | Environment Setup Guide | DO | 3 | 3B.8.1 + 3B.8.5 §setup |
| 4.1.3 | Environment Variables | DO | 3 | 3B.8.5 completo |
| 4.1.4 | Docker Compose | DO | 5 | 3B.8.1 §docker |
| 4.1.5 | Makefile/Scripts | DO | 3 | 3B.8.1 §automatización |
| 4.1.6-10 | IDE + Linter + Formatter + Pre-commit + Git | TL | 10 | 3B.2.2 §editor..§git-flow |
| 4.3.14 | Error Handling — AppError + MEM-ERR-xxx | BE | 8 | 3B.4.5 + 3B.2.6 completo |
| 4.3.15 | Logging — Winston + correlationId | BE | 5 | 3B.2.2 + 3B.7.10 §Winston |
| 4.2.1 | Initial Migration — 29 entidades | DB | 8 | 3B.3.2 completo |
| 4.2.2 | Schema Migrations | DB | 8 | 3B.3.6 completo |
| 4.2.6 | Constraints | DB | 3 | 3B.3.2 + 3B.3.3 §unique |

**Gate M1:** ✓ Containers UP ✓ BD migrada ✓ Seed OK ✓ AppError compilando

---

### S2: Core Backend (~75h)

**Objetivo:** Catálogos cargados, índices aplicados, middleware chain completo, 5 services implementados.
**Agentes:** BE + DB + TL (3 en paralelo)

| ID | Deliverable | Rol | Horas | Spec Source (3B.9.10) |
|----|-------------|:---:|:-----:|----------------------|
| 4.2.3 | Seed Data — 10 catálogos | DB | 8 | 3B.3.7 §catálogos |
| 4.2.4 | Test Data | DB | 5 | 3B.3.7 §datos de prueba |
| 4.2.5 | Indexes — partial + GIN + composite | DB | 8 | 3B.3.4 completo |
| 4.2.9 | Migration Guide | DB | 3 | 3B.3.6 §guía operativa |
| 4.2.10 | Rollback Scripts | DB | 5 | 3B.3.6 §rollback |
| 4.3.7 | Middlewares — Auth + Validation + RateLimit + ErrorHandler | BE | 8 | 3B.4.6 + 3B.4.7 + 3B.4.8 + 3B.2.6 |
| 4.3.5 | DTOs/Schemas — Zod | BE | 5 | 3B.4.2 + 3B.4.3 §schemas |
| 4.3.3 | Models — Prisma client + catalogCache | BE | 5 | 3B.3.2 completo |
| 4.3.4 | Repositories — ConversationRepository + 6 queries | BE | 8 | 3B.3.1 + 3B.3.8 |
| 4.3.2 | Services — Import + ContextQuery + Classifier + CostCalc + Storage | BE | 13 | 3B.1.4 + 3B.5.3 §5 services |
| 4.3.8 | Utils | BE | 3 | 3B.2.2 + 3B.7.9 |
| — | TL reviews + coordinación | TL | 4 | — |

**Gate M2:** ✓ Auth MW activo ✓ catalogCache cargado ✓ Zod OK ✓ Repository testeado

---

### S3: Features BE + FE Start (~77h)

**Objetivo:** 11 endpoints funcionales, 3 integraciones, FE foundation desplegada.
**Agentes:** BE + FE + TL (3 en paralelo)

| ID | Deliverable | Rol | Horas | Spec Source (3B.9.10) |
|----|-------------|:---:|:-----:|----------------------|
| 4.3.1 | API Endpoints — 11 endpoints | BE | 13 | 3B.4.2 completo |
| 4.3.6 | Workers — Cleanup Job | BE | 8 | 3B.5.6 + 3B.4.2 |
| 4.5.1 | Integration Code — Runtime + PB + HM | BE | 8 | 3B.1.4 + 3B.5.3 |
| 4.5.2 | API Clients | BE | 5 | 3B.4.2 §contracts |
| 4.5.3 | Webhooks — POST /import-review | BE | 5 | 3B.5.5 §VTT_CHANNEL |
| 4.5.5 | Third-party SDKs | BE | 3 | 3B.1.5 §dependencies |
| 4.4.1 | Components — shared + layout | FE | 8 | 3B.2.1 + 3A.9.1 Design Handoff |
| 4.4.3 | Layouts | FE | 3 | 3B.2.1 + 3A.9.1 |
| 4.4.4 | Hooks | FE | 5 | 3B.4.2 §endpoints |
| 4.4.5 | State Management | FE | 5 | 3B.2.3 §React Context |
| 4.4.6 | API Client FE | FE | 5 | 3B.4.2 + 3B.4.6 §auth |
| 4.4.7 | Types/Interfaces | FE | 3 | 3B.4.2 + 3B.4.3 |
| 4.4.8 | Styles — Tailwind | FE | 3 | 3A.7.1 design tokens |
| — | TL reviews | TL | 3 | — |

**Gate M3:** ✓ POST /import e2e OK ✓ JSONL procesado ✓ IMPORTED en BD ✓ FE foundation

---

### S4: FE Features + Context SLA (~73h)

**Objetivo:** 8 pantallas renderizan, GET /context <500ms validado, unit tests passing.
**Agentes:** BE + FE + TL (3 en paralelo)

| ID | Deliverable | Rol | Horas | Spec Source (3B.9.10) |
|----|-------------|:---:|:-----:|----------------------|
| 4.4.2 | Pages — 8 pantallas | FE | 13 | Wireframes 3A.5.x por pantalla |
| 4.4.9 | Utils FE | FE | 2 | 3B.2.2 §formatters |
| 4.4.15 | Responsive | FE | 5 | 3A.6.3 breakpoints |
| 4.4.10 | Unit Tests FE | FE | 5 | 3B.2.2 §Vitest |
| 4.4.11 | Component Tests | FE | 5 | 3B.2.2 §RTL |
| 4.4.13 | Frontend README | FE | 2 | 3B.2.1 §estructura FE |
| 4.5.8+9 | Error Handling + Retry Logic | BE | 10 | 3B.2.6 + 3B.5.5 |
| 4.5.6 | Integration Tests | BE | 8 | 3B.5.3 + 3B.5.5 |
| 4.5.7 | Integration Docs | BE | 3 | ADDENDUM §2, §4 |
| 4.3.11 | API Docs — Swagger | BE | 5 | 3B.4.1 completo |
| 4.3.12 | Postman Collection | BE | 3 | 3B.4.10 completo |
| 4.3.9 | Unit Tests BE | BE | 8 | 3B.4.2 + 3B.4.5 |
| — | TL reviews + SLA validation | TL | 4 | — |

**⚠️ Gate M4 (MAYOR RIESGO):** ✓ GET /context <500ms p95 ✓ 8 pantallas renderizan ✓ Unit tests passing

Si M4 falla: (1) EXPLAIN ANALYZE query más lenta, (2) agregar índice, (3) re-ejecutar k6, (4) si no resuelve en 3 días → escalar PM (+20h buffer R-01)

---

### S5: Testing Phase 1 (~84h)

**Objetivo:** Test plan, functional y integration tests passing.
**Agentes:** QA + DO + DB + TL (4 en paralelo)

| ID | Deliverable | Rol | Horas | Spec Source (3B.9.10) |
|----|-------------|:---:|:-----:|----------------------|
| 5.1.1-5 | Test Plan + Strategy + Scope + Schedule + Resources | QA | 14 | 2.7.1 + 3B.4.2 |
| 5.2.1-4 | Test Cases + IDs + Data + Expected | QA | 18 | 3B.4.2 + 3B.4.5 + 2.7.1 |
| 5.3.1 | Test Environment | DO | 5 | 3B.8.1 + 3B.8.5 |
| 5.3.2-4 | Test Database + Seeding + Docs | DB | 8 | 3B.3.7 + 3B.3.2 |
| 5.4.1-5 | Functional Tests | QA | 17 | 3B.4.2 + 2.7.1 |
| 5.5.1-4 | Integration Tests | QA | 18 | 3B.5.5 + ADDENDUM |
| — | TL coordinación | TL | 4 | — |

**Gate M5:** ✓ Functional pass ✓ Integration pass ✓ E2E críticos pass

---

### S6: Testing Phase 2 + Docs + Reviews (~75h)

**Objetivo:** Performance, security, UAT sign-off, documentación y code review cerrados.
**Agentes:** QA + BE + TL (3 en paralelo)

| ID | Deliverable | Rol | Horas | Spec Source (3B.9.10) |
|----|-------------|:---:|:-----:|----------------------|
| 5.6.1-5 | E2E Tests (Playwright) | QA | 19 | 3B.4.2 + wireframes 3A.5.x |
| 5.7.1-6 | Load Tests (k6) + Bottleneck | QA | 24 | 3B.8.10 + 3B.3.4 |
| 5.8.1-7 | Security Tests + OWASP + Sign-off | QA+TL | 24 | 3B.7.1 + 3B.7.6 |
| 5.10.1-5 | UAT + Sign-off | TL | 13 | 2.7.1 + SPEC §15 |
| 5.11.1-3 | Bug Fixes + Regression | BE+QA | 15 | 3B.4.5 + 3B.2.6 |
| 4.6.1-7 | Unit Tests QA | QA | 30 | 3B.4.2 + 3B.2.2 |
| 4.3.10 | Integration Tests BE | BE | 8 | 3B.5.3 + 3B.5.5 |
| 4.7.1-8 | Tech Docs | TL+BE | 24 | 3B.2.1 + 3B.2.2 |
| 4.8.1-4 | Code Review | TL | 22 | 3B.6.2 ADR index |

**Gate M5b:** ✓ Load test <500ms p95 50VU ✓ Security sign-off ✓ UAT sign-off

---

### S7: Deploy Staging (~73h)

**Objetivo:** Staging live, CI/CD activo, smoke tests OK.
**Agentes:** DO + DB + QA + TL (4 en paralelo)

| ID | Deliverable | Rol | Horas | Spec Source (3B.9.10) |
|----|-------------|:---:|:-----:|----------------------|
| 6.1.1-4 | Infrastructure + Servers + Network + Security | DO | 16 | 3B.8.1 + 3B.8.2 |
| 6.1.6+8 | Database Ready + SSL | DO | 8 | 3B.8.1 + 3B.8.2 |
| 6.2.1 | CI Pipeline — GitHub Actions 4 repos | DO | 8 | 3B.8.1 + 3B.2.1 |
| 6.2.2 | CD Pipeline | DO | 8 | 3B.8.1 + 3B.8.2 |
| 6.2.3-6 | Build + Deploy Scripts + Env Configs + Docs | DO | 13 | 3B.8.1 + 3B.8.5 |
| 6.3.1-2 | Staging Deploy + URL | DO | 7 | 3B.8.2 + 3B.8.5 |
| 6.3.3 | Migration Run staging | DB | 3 | 3B.3.6 §deploy |
| 6.3.4 | Health Check | DO | 2 | 3B.4.2 §GET /health |
| 6.4.1-3 | Smoke Tests + Sign-off | QA+TL | 6 | 3B.4.2 + 2.7.1 |
| — | TL coordinación deploy | TL | 2 | — |

**Gate M6:** ✓ Staging live ✓ Smoke tests OK ✓ CI/CD activo

---

### S8: Deploy Producción + Operations (~62h)

**Objetivo:** Producción live, monitoring activo, rollback probado.
**Agentes:** DO + TL (2 en paralelo)

| ID | Deliverable | Rol | Horas | Spec Source (3B.9.10) |
|----|-------------|:---:|:-----:|----------------------|
| 6.5.1-6 | Production Deploy + URL + DNS + SSL + Release Notes | DO+TL | 13 | 3B.8.2 + 3B.8.5 |
| 6.6.1-2 | Monitoring Dashboard + Alerts | DO | 8 | 3B.8.11 |
| 6.6.6 | Post-Deploy Report 24h | DO | 2 | 3B.8.11 |
| 6.7.1-5 | Rollback Plan + Scripts + Tested + Runbook + Criteria | DO | 13 | 3B.8.7 + 3B.8.8 |
| 7.1.1-4 | Uptime + Perf + Error + Weekly Reports | DO+TL | 12 | 3B.8.11 + 3B.8.10 |
| 7.2.1+3+4 | Support Process + SLA + Metrics | TL | 7 | 3B.8.10 + 3B.4.2 |
| 7.3.1+3 | Hotfix Process + Bug Tracking | TL | 4 | 3B.2.2 + 3B.8.8 |
| — | TL release sign-off | TL | 3 | — |

**Gate M7 (FINAL):** ✓ Producción live ✓ Monitoring activo ✓ Rollback probado → 🎯 R1 ENTREGADO

---

## 7. Lo que Falta Definir

| # | Pendiente | Quién decide | Impacto |
|---|-----------|:------------:|---------|
| 1 | Fechas absolutas de S1-S8 | PM | Sin fechas no se crean sprints en VTT |
| 2 | Contratos congelados Runtime v1.1, PB v1.3, Hook Manager | PM + TL | R-02, R-03, R-04 (hasta +13h rework) |
| 3 | Deliverables F7 post-S8 (7.4.x, 7.5.x, 7.6.x) | PM | ~35h sin sprint asignado |
| 4 | Incluir ⚪ opcionales (Storybook, Accessibility, Log Aggregation) | PM | +24h si se incluyen |

---

## 8. Top 10 Riesgos

| ID | Riesgo | Prob. | Buffer | Sprint |
|----|--------|:-----:|:------:|:------:|
| R-01 | GET /context no cumple SLA <500ms | 0.40 | +8h | S4 |
| R-02 | Runtime v1.1 cambia contrato | 0.25 | +6h | S3 |
| R-12 | CI/CD falla primer deploy prod | 0.35 | +4.2h | S7-S8 |
| R-14 | Playwright flaky en CI | 0.40 | +3.2h | S5-S6 |
| R-15 | k6 descubre N+1 queries | 0.30 | +3h | S6 |
| R-05 | P2002 concurrente en import | 0.30 | +2.4h | S2-S3 |
| R-07 | TS strict rework Prisma | 0.35 | +2.8h | S2-S3 |
| R-03 | PB v1.3 incompatible | 0.20 | +4h | S3 |
| R-06 | Partial indexes insuficientes | 0.25 | +2.5h | S2, S6 |
| R-04 | Hook Manager cambia formato | 0.20 | +3.2h | S3 |

Total buffer: +46.75h | Expected: 766h | Worst case: ~900h

Detalle completo de 15 riesgos con mitigaciones: `3B.9.6_risk_adjusted_estimates.md`

---

## 9. Documentos de Referencia

| Documento | Cuándo consultarlo |
|-----------|:------------------:|
| **3B.9.10 Routing Index** | **SIEMPRE — al crear cada HANDOFF y ASSIGNMENT. Es obligatorio.** |
| 3B.9.3 Task Breakdown | Al crear tareas en VTT — tiene los 174 deliverables con horas y roles |
| 3B.9.9 Capacity Plan | Al planificar cada sprint — deliverables detallados por sprint |
| 3B.9.7 Dependencies Map | Al secuenciar tareas — critical path y gates |
| 3B.9.6 Risk-Adjusted Estimates | Cuando un riesgo se materializa — plan de contingencia |
| 3B.9.4 Effort Matrix | Al verificar carga por agente — horas por rol × subfase |
| 3B.9.5 Complexity Analysis | Al priorizar reviews TL — top 10 complejos |
| SPEC v1.9 | Cuando hay duda técnica — fuente de verdad |
| Addendum Bloque 0 Lite | Para S1 — specs Error Handling + Logging + Security Base |
| ANALISIS_FASES_COMPLETO_PARA_PM | Catálogo estándar 438 deliverables — definición de cada uno |

---

## 10. Flujo Pendiente

```
TL (estimaciones + routing index) ✅ HECHO
    ↓
PM (este HO) ✅ HECHO
    ↓
PJM (crear sprints + tareas en VTT) ← AQUÍ ESTÁS
    ↓
PJM (generar HANDOFF S1 para TL — usar 3B.9.10 para referencias)
    ↓
TL (generar ASSIGNMENTs S1 — abrir docs 3B referenciados en 3B.9.10)
    ↓
Agentes ejecutan S1 con specs reales
    ↓
Repetir S2..S8
    ↓
PM (sign-off M7 → R1 entregado)
```

---

## 11. Próximo Paso

1. **Confirmar fechas con PM** — S1 arranca cuando PM diga GO
2. **Crear Sprint S1 en VTT** — 11 deliverables de la tabla S1
3. **Generar HANDOFF S1 para TL** — para cada deliverable, abrir 3B.9.10 y copiar Spec Source + Sección + D-MEM + Docs para el agente
4. **TL recibe HANDOFF** → genera ASSIGNMENTs abriendo los 3B referenciados → asigna a DO, BE, DB
5. **Monitorear** avance y reportar al PM si Δ > 20%

---

## 12. Equipo

| Rol | UUID | Horas ✅ | Función |
|-----|------|:-------:|---------|
| PM | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` | — | Aprueba tareas, GO/NO-GO milestones |
| PJM (TÚ) | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` | — | Sprints, HANDOFFs, monitoreo |
| TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` | 37h | Review PRs, ASSIGNMENTs, SLA validation |
| BE | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | 205h | 11 endpoints + services + integraciones |
| DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | 57h | Schema 29 entidades + migrations + indexes |
| FE | `d23c9cd9-a156-433b-8900-94add5488eec` | 73h | 8 pantallas React + Tailwind |
| QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | 186h | Testing completo F5 |
| DO | `322e3745-9756-4a7c-af11-44b33edef44d` | 145h | Infra + Docker + CI/CD + deploy |
| SA | `0c128e3b-db3b-4e31-b107-0379b5791233` | — | Reviewer si PM lo solicita |

---

## 13. Reglas de Escalación al PM

| Situación | Acción |
|-----------|--------|
| Varianza > +15% | Notificar PM |
| 2 sprints con desvío | PM + TL revisan estimaciones |
| Milestone NO-GO | PM decide: buffer, reducir scope o escalar |
| Riesgo materializado | PM + TL plan de acción en 24h |
| Doc referenciado en 3B.9.10 no existe | `task_on_hold` + notificar TL |
| Contrato integración cambia | STOP → PM congela o escala |

---

**Última actualización:** 2026-05-19
**Generado por:** PM Memory Service
**Documento clave companion:** `3B.9.10_routing_index.md` — obligatorio para toda operación downstream
