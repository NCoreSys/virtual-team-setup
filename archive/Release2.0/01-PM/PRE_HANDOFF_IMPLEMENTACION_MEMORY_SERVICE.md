# PRE-HANDOFF — Tareas de Implementación Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **Autor** | PM (Martin Rivas) |
| **Propósito** | Inventario consolidado de tareas de **código** derivadas del análisis de feature. Insumo para el HO formal al PJM. |
| **Alcance** | Tareas que producen código, tests, infra o deploy. NO incluye tareas de Discovery, Planning, Analysis ni Design. |
| **Estado** | ✅ Listo para revisión PM previo al HO a PJM |

---

## 1. FUENTES CONSUMIDAS

Documentos de análisis de feature en `memory-service-project/Release2.0/01-PM/`:

| Documento | Qué aporta al pre-handoff |
|-----------|---------------------------|
| `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | Schema Prisma, endpoints R1, flujos import, context service, storage, cleanup job, docker-compose |
| `METODOLOGIA_MEMORY_SERVICE_v1.2.md` | 5 fuentes, 3 tipos de conversación, catálogos, UI standalone |
| `ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md` | Integración Runtime v1.1 (CLAUDE_SDK + platformRefs) y Prompt Builder v1.3 |
| `FASES_APLICABLES_MEMORY_SERVICE.md v2.0` | 390 deliverables aplicables (contexto total del proyecto) |
| `HO_ACTUALIZAR_TAREAS_VTT.md v2.1` | 116 tareas + 65 deliveries VTT cargadas |
| `PLAN_116_TAREAS.md` | Vista TL con rol/horas/complexity por tarea |

---

## 2. CONTEXTO DE IMPLEMENTACIÓN

### 2.1 Qué se construye

Microservicio independiente de memoria centralizada para agentes IA:

- **Backend API** (puerto 3002) — 11 endpoints REST
- **Base de datos** PostgreSQL `memory_service_db` — 19 tablas + 10 catálogos
- **Storage filesystem** — `/root/memory-service-storage/` (bind mount)
- **Cleanup job** — cron cada 5 min para conversaciones stale
- **UI standalone** (puerto 3003) — SPA React + Vite + Tailwind (9 pantallas)
- **Integraciones** — Runtime v1.1, Prompt Builder v1.3, Hook Manager VTT

### 2.2 Stack

| Componente | Tecnología |
|-----------|------------|
| Runtime | Node.js 20 + TypeScript |
| Framework | Express |
| ORM | Prisma |
| BD | PostgreSQL (shared-postgres, `memory_service_db`) |
| Cache / Rate limit | Redis (shared-redis, prefix `mem`) |
| Storage | Filesystem bind mount |
| Frontend | React 18 + Vite + TailwindCSS |
| Container | Docker + docker-compose |
| Red | `shared-network` Docker |
| Host | VM Hetzner `77.42.88.106` |

### 2.3 Criterio de "tarea de implementación"

Se incluyen en este pre-handoff las tareas que producen:

- Código fuente (backend, frontend, DB migrations, seeds)
- Tests automatizados (unit, integration, E2E, performance)
- Configuración de infra y CI/CD (Dockerfile, docker-compose, pipelines)
- Deploy (staging, producción, rollback)
- Observabilidad en producción (monitoring, logs, alerts)

**No se incluyen:** tareas de Discovery, Planning, Analysis, Design UX/UI, Design Technical docs (esas están en otros HOs).

---

## 3. INVENTARIO DE TAREAS DE IMPLEMENTACIÓN

**Total: 66 tareas · 213h** (de las 116 tareas totales del proyecto).

### 3.1 Resumen por rol

| Rol | Tareas | Horas | % del pre-handoff |
|-----|-------:|------:|------------------:|
| DB Engineer | 3 | 6h | 3% |
| BE Engineer | 27 | 73h | 34% |
| FE Engineer | 13 | 46h | 22% |
| DevOps | 11 | 29h | 14% |
| QA Engineer | 11 | 54h | 25% |
| AR (Security Testing) | 1 | 4h | 2% |
| **TOTAL** | **66** | **212h** | **100%** |

### 3.2 Resumen por sprint / delivery

| Delivery VTT | Tareas | Horas | Fase VTT |
|--------------|-------:|------:|----------|
| S01: Schema + Seeds | 5 | 9h | Development |
| S02: Import + Timeline | 5 | 12h | Development |
| S03: Content + Context | 5 | 12h | Development |
| S04: Adapters + Cleanup | 6 | 12h | Development |
| S05: Lista + Cost + Dashboard | 6 | 11h | Development |
| S06: Docker + Integration | 6 | 14h | Development |
| UI-01: Setup + Timeline + Viewer | 5 | 16h | Development |
| UI-02: Dashboard + Cost + Import | 3 | 12h | Development |
| UI-03: Viewer REVIEW + Lista | 2 | 10h | Development |
| UI-04: Cost Agente + Health | 3 | 8h | Development |
| Testing (todas las subfases 5.1..5.11) | 10 | 60h | Testing |
| Deploy (todas las subfases 6.1..6.7) | 7 | 26h | Deploy |
| Operations — Monitoring | 1 | 3h | Operations |
| Project Setup (infra + tooling) | 2 | 4h | Project Setup |

---

## 4. DETALLE DE TAREAS POR CATEGORÍA

### 4.1 Database Engineer (3 tareas · 6h)

Todas en sprint **S01**, delivery `S01: Schema + Seeds`.

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-048 | DB Schema Prisma completo | 3h | HIGH | `prisma/schema.prisma` con 19 tablas principales + 10 catálogos + constraints `@@unique([sourceId, externalSessionId])`, `@@unique([conversationId, turnIndex])`, `@@unique([turnId, blockIndex])`, `@@unique([conversationId, entityName])` |
| MEM-049 | Migraciones + Partial Indexes | 2h | MEDIUM | `prisma migrate deploy` + `prisma/migrations/manual/partial_indexes.sql` con: índice parcial `idx_conv_agent_time`, `idx_conv_task`, `idx_block_filepath` + índice GIN `idx_conv_runtime_run` (ADDENDUM §5.3) |
| MEM-050 | Seed de 10 catálogos | 1h | LOW | `prisma/seed.ts` con SourceCatalog (5 códigos), ConversationTypeCatalog (3), ConversationStatusCatalog (4), WorkTypeCatalog (6), BlockTypeCatalog (4), MessageTypeCatalog (6), MessageStatusCatalog (6), PlatformCatalog (5), TopicCatalog (10), PriorityCatalog (3) |

### 4.2 Backend Engineer (27 tareas · 73h)

#### S01 · Schema + Seeds (2 tareas · 3h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-051 | Setup Express + estructura carpetas | 2h | MEDIUM | `src/app.ts`, `src/index.ts`, `src/config/env.ts`, estructura `routes/`, `controllers/`, `services/`, `middleware/`, `jobs/`, `schemas/`, `utils/` según SPEC §3.2 |
| MEM-052 | Catalog cache startup | 1h | LOW | `src/services/catalog-cache.service.ts` con `initCatalogCache()`, getters `getSourceId`, `getStatusId`, etc. Llamada en bootstrap antes de `app.listen()` |

#### S02 · Import + Timeline (5 tareas · 12h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-053 | `POST /api/conversations/import` (SDK/CLI/Web/ChatGPT) | 4h | HIGH | Controller + service con adapters para 4 fuentes. Idempotencia por `[sourceId, externalSessionId]`. Manejo P2002. Status flow PENDING→PROCESSING→IMPORTED/ERROR. Catch delega a cleanup |
| MEM-054 | `POST /api/conversations/import-review` (VTT_CHANNEL) | 2h | MEDIUM | Import incremental multi-agente. Persiste participants + messages. `primaryAgentId = NULL` |
| MEM-055 | `POST /api/conversations/upload` (manual) | 3h | HIGH | Endpoint público R1 multipart. Auto-detecta fuente por formato. Usa mismo flujo interno que `/import` |
| MEM-056 | `GET /api/agents/:id/timeline` | 2h | MEDIUM | Lista cronológica single-agent + participaciones multi-agent, paginada |
| MEM-057 | Error handling + cleanup delegation | 1h | LOW | Middleware `error-handler`, zod validation, AMB-07 (catch no mueve a ERROR, delega a cleanup job) |

#### S03 · Content + Context (3 tareas · 8h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-058 | `GET /api/conversations/:id/content` | 2h | MEDIUM | Lee archivo desde `/storage/` y parsea según fuente. D-MEM-43: no lee de BD, parsea archivo |
| MEM-059 | `GET /api/context` (`<500ms` fail-fast) | 4h | HIGH | `context.service.ts` con `Promise.race(queries, timeout)`. Queries paralelas: recentSessions, taskRelated, topicRelated, reviews, frequentFiles, cost. Filtra SIEMPRE por `projectId` (D-MEM-39). Usa cache catálogos |
| MEM-060 | Classifier determinístico (topics/workType) | 2h | HIGH | `classifier.service.ts` por reglas sobre paths + tool calls + contenido. Output: workType, topics, entities, confidence |

#### S04 · Adapters + Cleanup (5 tareas · 10h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-063 | Adapter CLAUDE_WEB | 3h | MEDIUM | `src/services/adapters/web.adapter.ts`. Parsea JSON único de export claude.ai |
| MEM-064 | Adapter CHATGPT | 2h | MEDIUM | `src/services/adapters/chatgpt.adapter.ts`. Parsea estructura `mapping` de export chatgpt.com |
| MEM-065 | Storage writer JSONL | 2h | MEDIUM | `src/services/storage.service.ts` con `save()` TASK y `saveReview()` REVIEW según D-MEM-06 |
| MEM-066 | Cleanup cron (5 min) | 2h | MEDIUM | `src/jobs/cleanup.job.ts` con `node-cron`. STALE > 10 min, `retryCount <= MAX_RETRIES` (D-MEM-40). Marca ERROR o vuelve a PENDING |
| MEM-067 | Status transitions handler | 1h | LOW | Helper para transiciones de `statusId` usando cache, con logging |

#### S05 · Lista + Cost + Dashboard (5 tareas · 10h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-069 | `GET /api/conversations` (lista con filtros) | 2h | MEDIUM | Filtros por `agentId`, `projectId`, `taskId`, `conversationType`, rango fechas. Paginación |
| MEM-070 | `GET /api/projects/:id/cost-report` | 2h | MEDIUM | Agrega `ConversationUsage.costUsd`, agrupa por agente y por tarea. Solo conversaciones IMPORTED |
| MEM-071 | `GET /api/agents/:id/cost-report` | 2h | MEDIUM | Cost-report por agente con breakdown por workType y semana |
| MEM-072 | `GET /api/dashboard/stats` | 2h | MEDIUM | Totales globales: conversaciones, costo, errores, importsRecientes |
| MEM-073 | `GET /health` | 2h | MEDIUM | Check BD, storage (`fs.access`), Redis (`PING`) |

#### S06 · Integración (1 tarea · 4h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-078 | Integración Hook Manager VTT | 4h | HIGH | Cliente HTTP para consumir Hook Manager desde Memory (si aplica), y validar que Hook Manager puede llamar `POST /import` y `POST /import-review` con SERVICE_KEY. Mock si Hook Manager no está listo |

#### Testing — Bug Fixes (1 tarea · 8h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-103 | Bug Fixes | 8h | HIGH | Reserva de esfuerzo post-testing para corregir bugs reportados por QA |

#### Integration tests (1 tarea · 1h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-074 | Integration tests endpoints | 1h | LOW | Tests de smoke sobre cada endpoint implementado en S05 |

#### Adapter tests (1 tarea · 2h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-068 | Tests adapters | 2h | MEDIUM | Fixtures JSONL reales de cada adapter + tests de parseo |

### 4.3 Frontend Engineer (13 tareas · 46h)

**Bloqueo crítico:** No inicia hasta que MEM-038 (Design Handoff) esté `task_approved`.

#### UI-01 · Setup + Timeline + Viewer (5 tareas · 16h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-081 | Setup React + Vite + Tailwind | 2h | MEDIUM | Proyecto FE independiente puerto 3003, configuración base |
| MEM-082 | Routing + layout base | 1h | LOW | React Router, layout principal con sidebar/topbar |
| MEM-083 | Page Timeline agente | 5h | HIGH | `/agents/:id/timeline` con lista cronológica, filtros, paginación |
| MEM-084 | Component Conversation Viewer | 6h | HIGH | Viewer TASK_EXECUTION con turns + tool calls expandibles |
| MEM-085 | Auth context (SERVICE_KEY) | 2h | MEDIUM | Contexto de auth con header Bearer, env var `VITE_SERVICE_KEY` |

#### UI-02 · Dashboard + Cost + Import (3 tareas · 12h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-086 | Page Dashboard | 4h | HIGH | `/` con stats globales, actividad reciente, errores pendientes |
| MEM-087 | Page Cost Report Proyecto | 4h | MEDIUM | `/projects/:id/cost` con breakdown por agente y tarea |
| MEM-088 | Page Import Manual | 4h | MEDIUM | `/import` con formulario multipart, progreso, feedback |

#### UI-03 · Viewer REVIEW + Lista (2 tareas · 10h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-089 | Page Lista conversaciones | 5h | HIGH | `/conversations` con filtros (agente, proyecto, fuente, tipo, rango), tabla ordenable |
| MEM-090 | Component AGENT_REVIEW multi-agente | 5h | HIGH | Thread view con badges de participantes, mensajes por status, replies anidados |

#### UI-04 · Cost Agente + Health (3 tareas · 8h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-091 | Page Cost Report Agente | 3h | MEDIUM | `/agents/:id/cost` con breakdown semanal por workType |
| MEM-092 | Page Health | 2h | LOW | `/health` con estado BD/storage/Redis, errores en cleanup |
| MEM-093 | Polish + responsive desktop | 3h | MEDIUM | Empty/loading/error states, responsive desktop breakpoints, revisión UX |

### 4.4 DevOps (11 tareas · 29h)

#### Project Setup (2 tareas · 4h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-001 | Infra Setup | 2h | MEDIUM | Coordinación con admin VM: confirmación de `memory_service_db`, volumen storage, SERVICE_KEY, firewall, shared-network |
| MEM-004 | Tooling Setup | 2h | MEDIUM | `.eslintrc`, `.prettierrc`, pre-commit hooks, `.gitignore`, IDE config |

#### S06 · Docker + CI (3 tareas · 5h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-075 | Dockerfile + docker-compose | 2h | MEDIUM | `Dockerfile` multi-stage, `docker-compose.yml` con `mem_limit: 512m`, red `shared-network`, volumen `/storage/` |
| MEM-076 | CI config | 2h | MEDIUM | GitHub Actions (o equivalente): build + test + lint + docker build |
| MEM-077 | Env vars + secrets | 1h | LOW | `.env.example`, documentación de vars, SERVICE_KEY desde secrets manager |

#### Testing — Environment (1 tarea · 4h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-096 | Test Environment setup | 4h | MEDIUM | BD de testing, seed de test data, docker-compose para CI |

#### Deploy (4 tareas · 17h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-104 | Infrastructure Setup (producción) | 4h | MEDIUM | Servidor listo, SSL, DNS, network config final |
| MEM-105 | CI/CD Configuration | 6h | HIGH | Pipeline completo con build, test, deploy a staging y prod |
| MEM-106 | Staging Deploy | 4h | MEDIUM | Deploy automatizado a staging, migraciones aplicadas, health check |
| MEM-108 | Production Deploy | 4h | HIGH | Deploy a producción, DNS, SSL, release notes |

#### Post-Deploy + Operations (2 tareas · 6h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-109 | Post-Deploy Monitoring | 3h | MEDIUM | Grafana dashboard, alertas configuradas, log aggregation, error tracking |
| MEM-111 | Monitoring setup (operational) | 3h | MEDIUM | Uptime, performance, error reports semanales |

### 4.5 QA Engineer (11 tareas · 54h)

#### Test Strategy (2 tareas · 12h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-094 | Test Planning | 4h | MEDIUM | Test plan + estrategia + scope + schedule |
| MEM-095 | Test Cases completos | 8h | HIGH | Casos de prueba por endpoint + escenarios de error + matriz de cobertura |

#### Performance / Classifier early tests (2 tareas · 4h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-061 | Tests performance contexto | 2h | MEDIUM | Benchmark de `GET /context` con dataset representativo, validar `<500ms` p95 |
| MEM-062 | Tests classifier | 2h | MEDIUM | Fixtures por workType + assertions sobre topics/entities detectados |

#### E2E cross-service (2 tareas · 5h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-079 | E2E test Runtime integration | 3h | HIGH | Mock Runtime envía conversación vía `POST /import` con `sourceCode=CLAUDE_SDK` y `platformRefs` completo. Verifica persistencia |
| MEM-080 | E2E test Prompt Builder integration | 2h | MEDIUM | Mock Prompt Builder llama `GET /context` con SERVICE_KEY. Verifica estructura JSON y `<500ms` |

#### Testing suite (5 tareas · 36h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-097 | Functional Testing | 8h | HIGH | Ejecución de casos funcionales + report + screenshots/evidence |
| MEM-098 | Integration Testing | 6h | HIGH | Suite de tests de integración BE + BD + storage |
| MEM-099 | E2E Testing | 8h | HIGH | Suite completa E2E con Playwright (UI + API) |
| MEM-100 | Performance Testing | 6h | HIGH | Load test, stress test, bottleneck analysis, validación SLA `<500ms` |
| MEM-107 | Smoke Testing | 3h | MEDIUM | Smoke suite post-deploy a staging y prod |

### 4.6 AR — Security Testing (1 tarea · 4h)

| Task | Título | Horas | Complexity | Qué produce |
|------|--------|------:|------------|-------------|
| MEM-101 | Security Testing | 4h | HIGH | Pentesting básico, validación SERVICE_KEY, OWASP checklist, vulnerability scan |

---

## 5. DEPENDENCIAS CRÍTICAS

### 5.1 Cadena serial backend (obligatoria)

```
MEM-048 → MEM-049 → MEM-050 → MEM-051 → MEM-052   (S01)
                                           ↓
MEM-053..057 (S02 Import + Timeline)
                                           ↓
MEM-058..062 (S03 Content + Context + QA tests performance/classifier)
                                           ↓
MEM-063..068 (S04 Adapters + Cleanup)
                                           ↓
MEM-069..074 (S05 Lista + Cost + Dashboard)
                                           ↓
MEM-075..080 (S06 Docker + Integration + E2E)
```

### 5.2 Cadena UI (bloqueada hasta DL)

```
MEM-038 (Design Handoff DL — externa a este pre-handoff) 🚨
                    ↓
MEM-081..085 (UI-01) → MEM-086..088 (UI-02) → MEM-089..090 (UI-03) → MEM-091..093 (UI-04)
```

### 5.3 Cadena testing + deploy

```
MEM-048..093 (todo el Development)
                    ↓
MEM-094..103 (Testing)
                    ↓
MEM-104..110 (Deploy)
                    ↓
MEM-111 (Monitoring operational)
```

### 5.4 Paralelismo permitido

- **Backend y Frontend** pueden correr en paralelo una vez que UI-01 arranca (FE consume API que ya está en S05 o mockeada).
- **DevOps** tareas MEM-001, MEM-004, MEM-075..077 pueden arrancar antes/durante S01.

---

## 6. OUTPUTS ESPERADOS (resumen)

### 6.1 Repositorio de código

```
memory-service/
├── src/
│   ├── app.ts
│   ├── config/
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   │   └── adapters/
│   ├── middleware/
│   ├── jobs/
│   └── schemas/
├── prisma/
│   ├── schema.prisma
│   ├── seed.ts
│   └── migrations/
│       └── manual/partial_indexes.sql
├── ui/                        ← FE SPA
│   └── src/
├── tests/
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

### 6.2 Artefactos desplegados

- Container `memory-service` corriendo en Hetzner `77.42.88.106:3002`
- Container `memory-service-ui` corriendo en Hetzner `77.42.88.106:3003`
- BD `memory_service_db` poblada con 10 catálogos + schema v1.9
- Volumen `/root/memory-service-storage/` con permisos correctos
- Pipeline CI/CD ejecutando en cada push
- Dashboard Grafana con métricas de contexto + errores

### 6.3 Artefactos de testing

- Suite de tests unitarios con cobertura ≥80%
- Suite de integración (BE + BD + storage)
- Suite E2E (UI + API)
- Suite de performance con validación SLA `<500ms`
- Reporte de security testing sin findings críticos

---

## 7. RIESGOS DE IMPLEMENTACIÓN

| # | Riesgo | Mitigación |
|---|--------|------------|
| R1 | `<500ms` no se cumple bajo carga | Fail-fast (D-MEM-07) · tests MEM-061/MEM-100 · partial indexes · cache catálogos |
| R2 | Pérdida de archivos `/storage/` | Backups diarios DO · BD solo metadata · storage es source of truth |
| R3 | Hook Manager no listo para MEM-078 | Mock del Hook Manager para E2E · continuar sin bloqueo |
| R4 | MEM-038 atrasa y bloquea FE | FE arranca con mocks de API · DL entrega por bloques |
| R5 | Race P2002 en import concurrente | Captura explícita → ALREADY_INDEXED (D-MEM-42) · test concurrente MEM-097 |
| R6 | SERVICE_KEY expuesta | `.env` no versionado · validación en MEM-101 |

---

## 8. CHECKLIST PM ANTES DE HO FORMAL AL PJM

```
[ ] Confirmar reassignments MEM-022 (SA) y MEM-039 (AR) aplicados en VTT
[ ] Confirmar que admin VM ya provisionó BD + volumen + SERVICE_KEY + firewall
[ ] Confirmar que Hook Manager tiene endpoint para recibir llamadas (o mock acordado)
[ ] Confirmar sprint dates propuestas por PJM (obsoletas del plan v2.0 52 tareas)
[ ] Confirmar repo Git real del proyecto
[ ] Definir formato multi-repo si aplica (pendiente desde PROJECT_RULES §8)
```

---

## 9. SIGUIENTE PASO

Con este pre-handoff consolidado, el PM genera el **HO formal al PJM** (`HANDOFF_PM_PJM_IMPLEMENTACION_MEMORY_SERVICE.md`) que incluirá:

- Contenido de este pre-handoff
- Criterios de aceptación por tarea
- Asignación de responsable confirmada por rol
- Fechas de inicio/fin por sprint (requiere input PJM)
- Firmas PM + PJM + roles principales
- Lista de BRIEFs que el PJM generará downstream

El PJM luego descompone cada sprint en BRIEFs individuales por agente ejecutor.

---

**Documento:** PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ Listo para revisión PM  
**Fecha:** 2026-04-22  

---

**PM — Martin Rivas**
