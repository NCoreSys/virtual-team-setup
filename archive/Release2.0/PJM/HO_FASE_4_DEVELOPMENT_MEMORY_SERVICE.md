# HANDOFF — Fase 4: Development · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_FASE_4_DEVELOPMENT_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PJM — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Para** | TL — `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| **CC** | BE — `ebbe3cee-abed-4b3b-860d-0a81f632b08a` · DB — `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` · FE — `d23c9cd9-a156-433b-8900-94add5488eec` · QA — `613c9538-658c-45fe-a6d7-c1ea9ff04b78` · DO — `322e3745-9756-4a7c-af11-44b33edef44d` |
| **Rol líder** | TL (Tech Lead) |
| **Proyecto** | Memory Service |
| **Fase VTT** | Development (Phase order 7) |
| **Estado** | ✅ APROBADO — listo para ejecución |

---

## RESUMEN EJECUTIVO

Esta fase implementa **el sistema completo**: 6 sprints backend (S01..S06) + 4 sprints frontend (UI-01..UI-04). Tiene 46 tareas VTT (MEM-048..093), 116h totales, distribuidas en 10 VTT Deliveries.

**Roles activos:** DB · BE · FE · QA · DO  
**Líder de seguimiento:** TL  
**Criterio de entrada BE:** Gate Design Technical cerrado (MEM-047 `task_completed`)  
**Criterio de entrada FE:** Gate Design Handoff Final cerrado (MEM-038 `task_completed` — HITO CRÍTICO)  
**Criterio de salida:** MEM-093 `task_completed` + todos los endpoints del SLA verificados

> **🚨 FE (MEM-081..093) NO arranca hasta MEM-038 `task_completed`.**  
> BE (MEM-048..080) puede arrancar en paralelo con Fase 3A (desde MEM-047).

---

## 1. ARQUITECTURA DE LA FASE

```
╔══════════════════════════════════════════════════════════════╗
║   GATE BE: MEM-047 task_completed (Design Technical OK)      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   S01: Schema + Seeds (5 tareas · 9h)                        ║
║   ├─ MEM-048  DB Schema Prisma         DB  3h  HIGH          ║
║   ├─ MEM-049  Migraciones + Indexes    DB  2h  MED           ║
║   ├─ MEM-050  Seed Catálogos           DB  1h  MED           ║
║   ├─ MEM-051  Setup Express            BE  2h  MED           ║
║   └─ MEM-052  Catalog Cache startup    BE  1h  MED           ║
║                                                              ║
║   S02: Import + Timeline (5 tareas · 12h)                    ║
║   ├─ MEM-053  POST /import (4 fuentes) BE  4h  HIGH          ║
║   ├─ MEM-054  POST /import-review      BE  2h  MED           ║
║   ├─ MEM-055  POST /upload (manual)    BE  3h  MED           ║
║   ├─ MEM-056  GET /agents/:id/timeline BE  2h  MED           ║
║   └─ MEM-057  Error handling + cleanup BE  1h  MED           ║
║                                                              ║
║   S03: Content + Context (5 tareas · 12h)                    ║
║   ├─ MEM-058  GET /content             BE  2h  MED           ║
║   ├─ MEM-059  GET /context (<500ms)    BE  4h  CRITICAL      ║
║   ├─ MEM-060  Classifier determinístico BE 2h  MED           ║
║   ├─ MEM-061  Tests performance        QA  2h  MED           ║
║   └─ MEM-062  Tests classifier         QA  2h  MED           ║
║                                                              ║
║   S04: Adapters + Cleanup (6 tareas · 12h)                   ║
║   ├─ MEM-063  Adapter CLAUDE_WEB       BE  3h  MED           ║
║   ├─ MEM-064  Adapter CHATGPT          BE  2h  MED           ║
║   ├─ MEM-065  Storage writer JSONL     BE  2h  MED           ║
║   ├─ MEM-066  Cleanup cron (5min)      BE  2h  MED           ║
║   ├─ MEM-067  Status transitions       BE  1h  MED           ║
║   └─ MEM-068  Tests adapters           BE  2h  MED           ║
║                                                              ║
║   S05: Lista + Cost + Dashboard (6 tareas · 11h)             ║
║   ├─ MEM-069  GET /conversations       BE  2h  MED           ║
║   ├─ MEM-070  GET /projects/:id/cost   BE  2h  MED           ║
║   ├─ MEM-071  GET /agents/:id/cost     BE  2h  MED           ║
║   ├─ MEM-072  GET /dashboard/stats     BE  2h  MED           ║
║   ├─ MEM-073  GET /health              BE  2h  MED           ║
║   └─ MEM-074  Integration tests S05    BE  1h  MED           ║
║                                                              ║
║   S06: Docker + Integration (6 tareas · 14h)                 ║
║   ├─ MEM-075  Dockerfile + compose     DO  2h  MED           ║
║   ├─ MEM-076  CI config                DO  2h  MED           ║
║   ├─ MEM-077  Env vars + secrets       DO  1h  MED           ║
║   ├─ MEM-078  Integración Hook Manager BE  4h  MED           ║
║   ├─ MEM-079  E2E test Runtime         QA  3h  MED           ║
║   └─ MEM-080  E2E test Prompt Builder  QA  2h  MED           ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║   GATE FE: MEM-038 task_completed (Design Handoff OK) 🚨     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   UI-01: Setup + Timeline + Viewer (5 tareas · 16h)          ║
║   ├─ MEM-081  Setup React + Vite       FE  2h  MED           ║
║   ├─ MEM-082  Routing + layout         FE  1h  MED           ║
║   ├─ MEM-083  Page Timeline agente     FE  5h  MED           ║
║   ├─ MEM-084  Component Viewer         FE  6h  MED           ║
║   └─ MEM-085  Auth context (key)       FE  2h  MED           ║
║                                                              ║
║   UI-02: Dashboard + Cost + Import (3 tareas · 12h)          ║
║   ├─ MEM-086  Page Dashboard           FE  4h  MED           ║
║   ├─ MEM-087  Page Cost Proyecto       FE  4h  MED           ║
║   └─ MEM-088  Page Import Manual       FE  4h  MED           ║
║                                                              ║
║   UI-03: Viewer REVIEW + Lista (2 tareas · 10h)              ║
║   ├─ MEM-089  Page Lista convs         FE  5h  MED           ║
║   └─ MEM-090  Component AGENT_REVIEW   FE  5h  MED           ║
║                                                              ║
║   UI-04: Cost Agente + Health (3 tareas · 8h)                ║
║   ├─ MEM-091  Page Cost Agente         FE  3h  MED           ║
║   ├─ MEM-092  Page Health              FE  2h  MED           ║
║   └─ MEM-093  Polish + responsive      FE  3h  MED           ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║   GATE DE SALIDA: MEM-093 completed + SLA verificados        ║
║   → Habilita Fase 5 Testing (MEM-094)                        ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. SECUENCIA DE SPRINTS BACKEND

```
MEM-047 (Design Technical gate)
    │
    ▼
S01: MEM-048 → MEM-049 → MEM-050   (DB chain)
     MEM-051 → MEM-052              (BE parallel)
    │
    ▼ (MEM-052 + MEM-050 completados)
S02: MEM-053 → MEM-054 → MEM-055 → MEM-056 → MEM-057
    │
    ▼ (MEM-057 completado)
S03: MEM-058 → MEM-059 (CRITICAL) → MEM-060
              MEM-061 ←────────────────────┘ (post MEM-059)
              MEM-062 ←─── MEM-060
    │
    ▼ (MEM-062 completado)
S04: MEM-063 → MEM-064 → MEM-065 → MEM-066 → MEM-067 → MEM-068
    │
    ▼ (MEM-068 completado)
S05: MEM-069 → MEM-070 → MEM-071 → MEM-072 → MEM-073 → MEM-074
    │
    ▼ (MEM-074 completado)
S06: MEM-075 → MEM-076 → MEM-077   (DO chain)
     MEM-078 → MEM-079 → MEM-080   (BE+QA chain, parallel con DO)
```

## 3. SECUENCIA DE SPRINTS FRONTEND

```
🚨 MEM-038 (Design Handoff Final — HITO CRÍTICO)
    │
    ▼
UI-01: MEM-081 (Setup) → MEM-082 (Routing)
                              │
                    ┌─────────┴──────────┐
                    ▼                    ▼
              MEM-083 (Timeline)   MEM-084 (Viewer)
              MEM-085 (Auth)
    │
    ▼ (MEM-085 completado)
UI-02: MEM-086 → MEM-087 → MEM-088
    │
    ▼ (MEM-088 completado)
UI-03: MEM-089 → MEM-090
    │
    ▼ (MEM-090 completado)
UI-04: MEM-091 → MEM-092 → MEM-093
```

---

## 4. RESUMEN DE TAREAS POR SPRINT

### S01 · Schema + Seeds (9h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-048 | DB Schema Prisma completo | DB | 3 | HIGH | H |
| MS-049 | Migraciones + Partial Indexes | DB | 2 | MEDIUM | M |
| MS-050 | Seed Catálogos | DB | 1 | LOW | M |
| MS-051 | Setup Express + estructura | BE | 2 | MEDIUM | M |
| MS-052 | Catalog Cache startup | BE | 1 | LOW | M |

**Entregables:** `prisma/schema.prisma` (19 tablas + 10 catálogos) · `partial_indexes.sql` · `prisma/seed.ts` (10 catálogos) · `src/app.ts` + estructura · `src/services/catalog-cache.service.ts`

### S02 · Import + Timeline (12h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-053 | POST /import (4 fuentes) | BE | 4 | HIGH | H |
| MS-054 | POST /import-review (VTT_CHANNEL) | BE | 2 | MEDIUM | M |
| MS-055 | POST /upload (manual) | BE | 3 | HIGH | M |
| MS-056 | GET /agents/:id/timeline | BE | 2 | MEDIUM | M |
| MS-057 | Error handling + cleanup delegation | BE | 1 | LOW | M |

**Entregables:** Endpoints import/review/upload/timeline · Middleware error-handler · Zod schemas

### S03 · Content + Context (12h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-058 | GET /content (parse storage) | BE | 2 | MEDIUM | M |
| MS-059 | GET /context (<500ms) | BE | 4 | HIGH | **C** |
| MS-060 | Classifier determinístico | BE | 2 | HIGH | M |
| MS-061 | Tests performance contexto | QA | 2 | MEDIUM | M |
| MS-062 | Tests classifier | QA | 2 | MEDIUM | M |

**Notas MEM-059 (CRITICAL):** `context.service.ts` con `Promise.race(queries, timeout(500))`. Queries paralelas. SIEMPRE filtra projectId (D-MEM-39). Timeout → 504 MEM-ERR-504.

### S04 · Adapters + Cleanup (12h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-063 | Adapter CLAUDE_WEB | BE | 3 | MEDIUM | M |
| MS-064 | Adapter CHATGPT | BE | 2 | MEDIUM | M |
| MS-065 | Storage writer JSONL | BE | 2 | MEDIUM | M |
| MS-066 | Cleanup cron (5 min) | BE | 2 | MEDIUM | M |
| MS-067 | Status transitions handler | BE | 1 | LOW | M |
| MS-068 | Tests adapters | BE | 2 | MEDIUM | M |

**Entregables:** `adapters/web.adapter.ts` · `adapters/chatgpt.adapter.ts` · `storage.service.ts` · `jobs/cleanup.job.ts` (STALE >10min, retry ≤3)

### S05 · Lista + Cost + Dashboard (11h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-069 | GET /conversations (lista) | BE | 2 | MEDIUM | M |
| MS-070 | GET /projects/:id/cost-report | BE | 2 | MEDIUM | M |
| MS-071 | GET /agents/:id/cost-report | BE | 2 | MEDIUM | M |
| MS-072 | GET /dashboard/stats | BE | 2 | MEDIUM | M |
| MS-073 | GET /health | BE | 2 | MEDIUM | M |
| MS-074 | Integration tests endpoints | BE | 1 | LOW | M |

### S06 · Docker + Integration (14h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-075 | Dockerfile + docker-compose | DO | 2 | MEDIUM | M |
| MS-076 | CI config | DO | 2 | MEDIUM | M |
| MS-077 | Env vars + secrets | DO | 1 | LOW | M |
| MS-078 | Integración Hook Manager VTT | BE | 4 | HIGH | M |
| MS-079 | E2E test Runtime integration | QA | 3 | HIGH | M |
| MS-080 | E2E test Prompt Builder | QA | 2 | MEDIUM | M |

**Notas MEM-078:** Cliente HTTP Memory → Hook Manager. Mock si no listo. Integrar con `integration-reviewer@memory-service.vtt.ai` (`f3e358f7-...`) para review.

### UI-01 · Setup + Timeline + Viewer (16h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-081 | Setup React + Vite + Tailwind | FE | 2 | MEDIUM | M |
| MS-082 | Routing + layout base | FE | 1 | LOW | M |
| MS-083 | Page Timeline agente | FE | 5 | HIGH | M |
| MS-084 | Component Conversation Viewer | FE | 6 | HIGH | M |
| MS-085 | Auth context (SERVICE_KEY) | FE | 2 | MEDIUM | M |

**Notas:** Puerto 3003. tailwind.config.js con tokens del DL (MEM-028). React Router + sidebar + breadcrumbs.

### UI-02 · Dashboard + Cost + Import (12h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-086 | Page Dashboard | FE | 4 | HIGH | M |
| MS-087 | Page Cost Report Proyecto | FE | 4 | MEDIUM | M |
| MS-088 | Page Import Manual | FE | 4 | MEDIUM | M |

### UI-03 · Viewer REVIEW + Lista (10h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-089 | Page Lista conversaciones | FE | 5 | HIGH | M |
| MS-090 | Component AGENT_REVIEW | FE | 5 | HIGH | M |

### UI-04 · Cost Agente + Health (8h)

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-091 | Page Cost Report Agente | FE | 3 | MEDIUM | M |
| MS-092 | Page Health | FE | 2 | LOW | M |
| MS-093 | Polish + responsive desktop | FE | 3 | MEDIUM | M |

---

## 5. TOTALES

| Sprint | Rol | Tareas | h |
|--------|-----|:------:|--:|
| S01 | DB + BE | 5 | 9 |
| S02 | BE | 5 | 12 |
| S03 | BE + QA | 5 | 12 |
| S04 | BE | 6 | 12 |
| S05 | BE | 6 | 11 |
| S06 | DO + BE + QA | 6 | 14 |
| UI-01 | FE | 5 | 16 |
| UI-02 | FE | 3 | 12 |
| UI-03 | FE | 2 | 10 |
| UI-04 | FE | 3 | 8 |
| **TOTAL** | | **46** | **116h** |

---

## 6. USUARIOS VTT ACTIVOS EN ESTA FASE

| Rol | UUID |
|-----|------|
| TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| BE | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| FE | `d23c9cd9-a156-433b-8900-94add5488eec` |
| QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` |
| DO | `322e3745-9756-4a7c-af11-44b33edef44d` |
| Integration Reviewer | `f3e358f7-679f-400f-8dd7-df41517bca15` |

---

## 7. GATE DE SALIDA — CRITERIOS DE COMPLETITUD

```
[ ] MEM-048..050 task_completed — Schema 19 tablas + seeds 10 catálogos
[ ] MEM-051..052 task_completed — Express setup + catalog cache
[ ] MEM-053..057 task_completed — Endpoints import/review/upload/timeline + error handler
[ ] MEM-058..060 task_completed — /content + /context (<500ms) + classifier
[ ] MEM-061..062 task_completed — Tests performance (p95 <500ms k6) + tests classifier
[ ] MEM-063..068 task_completed — 5 adapters + storage + cleanup cron + tests
[ ] MEM-069..074 task_completed — /conversations + /cost-report + /dashboard + /health + tests
[ ] MEM-075..077 task_completed — Dockerfile + CI + env vars
[ ] MEM-078..080 task_completed — Hook Manager integration + E2E tests
[ ] MEM-081..085 task_completed — React setup + routing + Timeline + Viewer + Auth
[ ] MEM-086..088 task_completed — Dashboard + Cost Proyecto + Import Manual
[ ] MEM-089..090 task_completed — Lista Convs + AGENT_REVIEW viewer
[ ] MEM-091..093 task_completed — Cost Agente + Health + Polish
[ ] SLA verificado: GET /context p95 <500ms (MEM-061 benchmark pasado)
[ ] 11 endpoints respondiendo correctamente
[ ] MEM-094 desbloqueado en VTT (Fase Testing arranca)
```

---

## 8. NOTAS TÉCNICAS CRÍTICAS

1. **MEM-059 GET /context <500ms:** Implementar con `Promise.race(queries, timeout(500))`. Queries en paralelo. SIEMPRE filtrar projectId (D-MEM-39). Failure → 504 MEM-ERR-504. TL revisa implementación antes de task_completed.
2. **AMB-07 — Cleanup delegation:** El catch en import NO mueve status a ERROR. Delega al cleanup cron (5min, STALE >10min, retry ≤3). Implementado en MEM-057 + MEM-066.
3. **Idempotencia import:** `@@unique([sourceId, externalSessionId])`. P2002 → `ALREADY_INDEXED` (no es error). Implementado en MEM-053.
4. **D-MEM-43 — /content NO lee BD:** MEM-058 parsea archivo desde /storage/ con adapter apropiado. Sin query a BD.
5. **Adapters en MEM-078:** Si Hook Manager no está listo para integración, usar mock. NO bloquear desarrollo.
6. **FE puerto 3003:** API en 3002, UI en 3003. VITE_SERVICE_KEY en .env para auth context (MEM-085).

---

## 9. ESCALACIÓN

| Bloqueo | Escalar a |
|---------|-----------|
| GET /context no alcanza <500ms | TL + AR |
| Hook Manager API no disponible | PM (usar mock) |
| Schema change necesario post-MEM-048 | TL + DB |
| Conflicto en adapters (formato inesperado) | TL + BE |
| FE bloqueado por Design Handoff incompleto | DL (MEM-038 gate) |

---

## 10. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PJM (emite)** | PJM Agent | ✅ EMITIDO | 2026-04-22 |
| **TL (recibe y lidera)** | TL Agent | ⬜ Pendiente acuse | — |
| **PM (valida)** | Martin Rivas | ⬜ Pendiente sign-off | — |

---

## 11. REFERENCIAS

- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — §4.7 Development tasks
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — §4 Development sprints
- `ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md` — AMB-07, D-MEM-39, D-MEM-43, D-MEM-35
- `HO_FASE_3B_DESIGN_TECH_MEMORY_SERVICE.md` — Gate previo (API Design, DB Design)
- `HO_FASE_3A_DESIGN_UXUI_MEMORY_SERVICE.md` — Gate FE (MEM-038)
- `VTT_UUIDS_MEMORY_SERVICE.json` — UUIDs tareas MS-048..093

---

**Documento:** HO_FASE_4_DEVELOPMENT_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ EMITIDO — Pendiente sign-off TL y PM  
**Fecha:** 2026-04-22

---

**PJM — Memory Service**  
Virtual Teams Tracking
