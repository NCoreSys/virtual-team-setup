# PROJECT MEMORY — Memory Service

**Propósito:** Memoria persistente del proyecto para agentes (TL, BE, DB, FE, QA, DO, DL). Qué estamos construyendo, con qué stack, cuál es el estado, y qué particularidades no se pueden derivar del código.

**Última actualización:** 2026-05-04
**Fuente primaria:** `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`

---

## 1. QUÉ ESTAMOS CONSTRUYENDO

**Memory Service** es un sistema **independiente** (no parte de VTT) de **memoria centralizada para agentes de IA**. Persiste conversaciones producidas por distintas fuentes, las clasifica por reglas determinísticas, calcula costos, y entrega contexto estructurado en **<500ms** al runtime de agentes.

### Responsabilidades

| SÍ hace | NO hace |
|---------|---------|
| Importar conversaciones (5 fuentes) | Ejecutar agentes (lo hace Runtime) |
| Clasificar por topics/workType (reglas) | Formatear prompts (lo hace Prompt Builder) |
| Persistir JSONL + metadata | Seleccionar qué contexto incluir (lo hace PB) |
| Entregar contexto estructurado (JSON) | Tokenizar o transformar a texto |
| Métricas de costo (tokens + USD) | Decidir retry policies de agentes |
| UI propia (SPA puerto 3003) | Exponer UI a usuarios finales |

### 5 Fuentes de conversaciones

| Código | Origen | Endpoint |
|--------|--------|----------|
| `CLAUDE_SDK` | Runtime orquestado (Claude SDK) | `POST /import` |
| `CLAUDE_CLI` | CLI Claude Code | `POST /import` |
| `CLAUDE_WEB` | claude.ai export | `POST /import` (adapter Web) |
| `CHATGPT` | chatgpt.com export | `POST /import` (adapter ChatGPT) |
| `VTT_CHANNEL` | AGENT_REVIEW / AGENT_CLARIFICATION | `POST /import-review` |

### 3 Tipos de conversación

| Tipo | Descripción | Agentes |
|------|-------------|---------|
| `TASK_EXECUTION` | Agente ejecutando una tarea | 1 (primary) |
| `AGENT_REVIEW` | Revisión entre agentes | N (participantes) |
| `AGENT_CLARIFICATION` | Agente pregunta, otro responde | N (incremental) |

---

## 2. STACK TÉCNICO

| Componente | Tecnología |
|------------|------------|
| Runtime | Node.js 20 + TypeScript |
| Framework | Express |
| ORM | Prisma |
| BD | PostgreSQL `memory_service_db` en shared-postgres |
| Cache / Rate Limit | Redis `shared-redis` (prefix: `mem`) |
| Storage de archivos | Volumen Docker bind mount → `/root/memory-service-storage/` |
| Frontend | React + Vite + TailwindCSS |
| Containerization | Docker + docker-compose |
| Deploy | VM Hetzner `77.42.88.106` |

### Puertos

| Puerto | Uso |
|--------|-----|
| 3002 | API Memory Service |
| 3003 | UI Standalone Memory Service |
| 3000 | API VTT (backend de tareas, no es Memory Service) |

### Paths clave

```
/root/memory-service/                        ← código desplegado
/root/memory-service-storage/                ← bind mount de storage
  ├── {primaryAgentId}/{YYYY-MM}/{sessionId}/   ← TASK_EXECUTION
  └── _reviews/{projectId}/{YYYY-MM}/{sessionId}/  ← AGENT_REVIEW / CLARIFICATION
```

---

## 3. MODELO DE DATOS (resumen)

19 tablas + 10 catálogos. Ver SPEC v1.9 §4 para detalle completo.

### Tablas principales

| Tabla | Descripción |
|-------|-------------|
| `Conversation` | 1 conversación = 1 ronda de 1 agente (o 1 canal VTT_CHANNEL). PK: `id` (UUID). Unicidad: `@@unique([sourceId, externalSessionId])` |
| `ConversationTurn` | Cada turno user/assistant. Solo `contentPreview` (500 chars). Contenido completo en `/storage/`. |
| `ConversationBlock` | Sub-bloques dentro de un turn (tool_use, text, etc.) |
| `ConversationParticipant` | Agentes participantes (para multi-agent) |
| `ConversationUsage` | Tokens + costo USD (6 decimales) |
| `ConversationTopic` | Join con `TopicCatalog` |
| `ConversationWorkType` | Join con `WorkTypeCatalog` |
| `ConversationClassification` | Confianza de clasificación |

### Catálogos (seed data, cache en startup)

`SourceCatalog`, `ConversationStatusCatalog`, `ConversationTypeCatalog`, `PlatformCatalog`, `TopicCatalog`, `WorkTypeCatalog`, `MessageTypeCatalog`, `MessageStatusCatalog`, `PriorityCatalog`, `BlockTypeCatalog`.

### Decisión clave — contentPreview (D-MEM-43)

> El contenido completo de turns NO se persiste en BD. Solo `contentPreview` (500 chars) para búsquedas/previews. `GET /content` parsea el archivo de `/storage/` en runtime.

**Motivo:** BD ligera, storage tiene fuente de verdad, cumple <500ms en `/context`.

---

## 4. CONTRATOS API (endpoints R1)

| Método | Ruta | Propósito |
|--------|------|-----------|
| POST | `/api/conversations/import` | Import JSONL (SDK/CLI/Web/ChatGPT) |
| POST | `/api/conversations/import-review` | Import VTT_CHANNEL (incremental) |
| POST | `/api/conversations/upload` | Import manual desde UI (sin auth) |
| GET  | `/api/conversations` | Lista con filtros/paginación |
| GET  | `/api/conversations/:id/content` | Contenido completo (parsea `/storage/`) |
| GET  | `/api/context` | Contexto estructurado para Runtime **<500ms** |
| GET  | `/api/agents/:id/timeline` | Cronología de conversaciones del agente |
| GET  | `/api/projects/:id/cost-report` | Costo total proyecto |
| GET  | `/api/agents/:id/cost-report` | Costo por agente con breakdown |
| GET  | `/api/dashboard/stats` | Stats globales |
| GET  | `/health` | Estado BD/storage/cache |

**Detalle exhaustivo de contratos:** SPEC v1.9 §8.

---

## 5. DECISIONES CERRADAS (no reabrir)

43 decisiones `D-MEM-01` a `D-MEM-43`. Las más importantes para implementación:

| ID | Decisión |
|----|----------|
| D-MEM-01 | Sistema **independiente** de VTT |
| D-MEM-05 / D-MEM-42 | Idempotencia por `@@unique([sourceId, externalSessionId])` |
| D-MEM-06 | Storage paths diferenciados por tipo de conversación |
| D-MEM-07 | `GET /context` **<500ms síncrono, fail-fast** |
| D-MEM-08 | Clasificación por **reglas determinísticas** (no LLM) |
| D-MEM-13 | Status flow: PENDING → PROCESSING → IMPORTED/ERROR |
| D-MEM-20 | Catálogos en BD, **no enums Prisma** |
| D-MEM-26 | Auth service-to-service vía **SERVICE_KEY** |
| D-MEM-29 | `primaryAgentId` nullable (para AGENT_REVIEW es NULL) |
| D-MEM-35 | Cleanup job cron cada 5 min |
| D-MEM-36 | `agentId` = `User.id` de VTT (NO catálogo propio) |
| D-MEM-38 | `primaryAgentRole` desnormalizado en import |
| D-MEM-41 | `@@unique([conversationId, turnIndex])` y `@@unique([turnId, blockIndex])` |
| D-MEM-43 | `contentPreview` en BD, contenido completo desde `/storage/` |

### Decisiones integración (addendum v1.1)

| ID | Decisión |
|----|----------|
| D-INT-01 | Runtime persiste 1 conv por ronda por agente |
| D-INT-02 | `externalSessionId = {run_id}:r{N}:{agentRole}` |
| D-INT-03 | `sourceCode = CLAUDE_SDK` (no crear `RUNTIME_ORCHESTRATED`) |
| D-INT-04 | `run_id` va en `platformRefs.runtime_run_id` |
| D-INT-05 | Prompt Builder transforma JSON→texto (Memory no) |

---

## 6. FASES DEL PROYECTO (VTT) — 10 fases, 116 tareas, 381h

**Project ID:** `d0fc276d-e764-4a83-96e9-d65f086ed803` (Project Key: MS)
**Fuente:** `HO_ACTUALIZAR_TAREAS_VTT.md` v2.1 (2026-04-21)

### Estado actual de fases

| Fase | Estado |
|------|--------|
| Phase 1 — Project Setup | ✅ COMPLETADA (gate MS-142 aprobado 2026-05-04) |
| Phase 2 — Discovery | 🔵 EN CURSO (recién iniciada) |
| Phase 3+ | ⏳ Pendiente |

| Order | Fase | Phase UUID | Tareas | Horas |
|-------|------|-----------|--------|-------|
| 1 | Project Setup | `83f56bad-7e60-4ffa-bc19-9c0f9ba097a1` | MEM-001..005 | 11h |
| 2 | Discovery | `3ee3a429-f836-45ea-afde-1753c78db9ac` | MEM-006..009 | 9h |
| 3 | Planning | `a0dcfb69-b862-4784-b8c9-5aad233dfb9d` | MEM-010..017 | 23h |
| 4 | Analysis | `26ecb1f6-1eb8-494f-930e-7e173c4ee559` | MEM-018..025 | 41h |
| 5 | Design UX/UI | `2c8f0f2f-992a-46e5-b80f-9739180c2532` | MEM-026..038 | 35h |
| 6 | Design Technical | `5f452a38-6cc6-4bbc-a8d5-1f50da2562af` | MEM-039..047 | 45h |
| 7 | Development | `c2804591-b21c-4340-9065-59fd23e14b63` | MEM-048..093 | 116h |
| 8 | Testing | `7ab83ed0-2238-4241-a915-8a957144d63e` | MEM-094..103 | 60h |
| 9 | Deploy | `137d3082-f280-48da-81e7-abd3c1789f63` | MEM-104..110 | 26h |
| 10 | Operations | `2ffc2179-2376-4197-93d1-56a878cd976e` | MEM-111..116 | 15h |

### Development phase — deliveries internas (S01..S06 + UI-01..04)

| Delivery | Tareas | Contenido |
|----------|--------|-----------|
| S01: Schema + Seeds | MEM-048..052 | DB schema + seed catálogos |
| S02: Import + Timeline | MEM-053..057 | Endpoints import + timeline agente |
| S03: Content + Context | MEM-058..062 | GET /content + GET /context (<500ms) |
| S04: Adapters + Cleanup | MEM-063..068 | Adapters (Web/ChatGPT) + cron cleanup |
| S05: Lista + Cost + Dashboard | MEM-069..074 | Lista convs + cost-report + stats |
| S06: Docker + Integration | MEM-075..080 | Docker + Hook Manager VTT integration |
| UI-01: Setup + Timeline + Viewer | MEM-081..085 | React setup + timeline view |
| UI-02: Dashboard + Cost + Import | MEM-086..088 | Stats + cost UI + manual upload |
| UI-03: Viewer REVIEW + Lista | MEM-089, MEM-090 | Lista convs + detalle |
| UI-04: Cost Agente + Health | MEM-091..093 | Cost breakdown + health |

### Dependencias críticas (pendientes de crear en VTT)

```
Development sequential:
  S01 → S02 → S03 → S04 → S05 → S06

UI depends on Design Handoff (HITO):
  MEM-038 (Design Handoff) ─────▶ MEM-081 (UI-01 start)

UI sequential:
  UI-01 → UI-02 → UI-03 → UI-04
```

> ⚠️ **Endpoint de dependencias VTT aún no confirmado** (HO v2.1 §10). Las dependencias NO se crean automáticamente. Requiere mecanismo manual de verificación hasta que DO/PM resuelvan el endpoint.

### Sprints

> ⚠️ **Sprint structure pendiente de actualización por PM.** El plan anterior (14 sprints, 52 tareas) quedó obsoleto con el handoff v3.0. La distribución temporal (sprint dates) de las 116 tareas debe confirmarla PM antes del kickoff.

### Dependencias operacionales clave

- **FE (MEM-081+) NO puede iniciar** sin MEM-038 (Design Handoff) completado.
- **MEM-078 (Integration Hook Manager)** requiere Hook Manager VTT operativo (coordinación PM+PJM).
- **MEM-048 (DB Schema)** es el inicio real del desarrollo — bloquea toda la fase Development.

---

## 7. PARTICULARIDADES (no derivables del código)

### 7.1 Idempotencia robusta

Un reimport del mismo run/ronda/agente **no duplica**. La unicidad es `@@unique([sourceId, externalSessionId])`. Captura de `P2002` de Prisma = respuesta `ALREADY_INDEXED`, no error 500.

### 7.2 <500ms en `GET /context` es contractual

Si no se cumple → **fail-fast**, no degradar. El runtime de agentes asume este SLA. Optimización vía índices parciales + prefetch de `statusId` al inicio del handler.

### 7.3 Cleanup como único camino de recovery

El catch del handler `import` **siempre delega al cleanup** (AMB-07). No intenta mover a ERROR directamente. Cleanup job corre cada 5 min y marca ERROR tras 3 retries.

### 7.4 Catálogos en BD, no enums

Para agregar una fuente nueva: INSERT en `SourceCatalog`. Sin migración Prisma. Mismo para topics, workTypes, statuses.

### 7.5 Cache de catálogos en startup (D-MEM-01 → DEC-01)

Los catálogos (10 tablas) se cargan en memoria al boot y se refrescan on-demand. Evita N+1 en import-review (observación TL-03 del review).

### 7.6 Partial indexes con SQL manual (DEC-02)

Prisma no soporta partial indexes. Se aplican como migración SQL cruda en `partial_indexes.sql` después de `prisma migrate deploy`. Ver SPEC §6 / subarchivo `partial_indexes.sql`.

### 7.7 Storage es fuente de verdad del contenido

BD tiene solo metadata + preview. Si hay discrepancia entre BD y `/storage/`, **gana storage**. `GET /content` siempre parsea desde filesystem.

### 7.8 Runtime envía `primaryAgentRole` desnormalizado (D-MEM-38)

Memory Service **no consulta VTT** para obtener el rol del agente. Runtime lo envía en el import. Cost-report lo usa sin lookups cross-service.

### 7.9 `GET /context` filtra SIEMPRE por projectId (D-MEM-39)

Nunca entregar contexto de otros proyectos. Todas las queries del handler aplican `WHERE projectId = :projectId`.

### 7.10 Multi-agent usa ConversationParticipant, no primaryAgentId

Para `AGENT_REVIEW`: `primaryAgentId = NULL`, participantes en tabla join. Queries de timeline por agente deben unir por `ConversationParticipant.agentId` además de `primaryAgentId`.

---

## 8. INFRAESTRUCTURA (ya provisionada)

| Recurso | Estado | Detalle |
|---------|--------|---------|
| BD `memory_service_db` | ✅ Creada | En shared-postgres, `connection_limit=20` |
| Volumen storage | ✅ Creado | `/root/memory-service-storage/` → `/storage/` |
| SERVICE_KEY | ✅ Generada | En `.env` del VM |
| docker-compose.yml | ✅ Listo | `mem_limit: 512m`, `shared-network` |
| Código backend | ⏳ Pendiente | Se implementa en Sprint 2 (May 19) |

---

## 9. INTEGRACIÓN CROSS-SERVICE

| Consumidor | Endpoint consumido | Cuándo |
|------------|-------------------|--------|
| **Runtime v1.1** | `POST /import` (sourceCode=CLAUDE_SDK) | Al terminar cada ronda de cada agente |
| **Prompt Builder v1.3** | `GET /context` | Al ensamblar prompt, via Memory Context Adapter |
| **Hook Manager VTT** | `POST /import-review` | Cuando se crea/actualiza un canal VTT_CHANNEL |
| **UI Standalone** | Todos los GET + `POST /upload` | Interacción de usuario |

---

## 10. REFERENCIAS

- SPEC completo: `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`
- **Plan 116 tareas (VTT):** `memory-service-project/Release2.0/PJM/HO_ACTUALIZAR_TAREAS_VTT.md` (v2.1, 2026-04-21) ← fuente actual
- Plan sprints (anterior, obsoleto): `memory-service-project/Release2.0/PJM/HO_PJM_PLAN_SPRINTS_MEMORY_SERVICE.md` (v2.0 — 52 tareas, ya no aplica)
- Addendum integración: `memory-service-project/Release2.0/01-PM/ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md`
- TL Review previa: `memory-service-project/Release2.0/04-TL/TL_REVIEW_SPEC_MEMORY_SERVICE_v1.md`
- **Plan de 116 tareas con asignaciones TL:** `knowledge/agent-tasks/PLAN_116_TAREAS.md`
- Reglas del proyecto: `.claude/rules/PROJECT_RULES.md`
- Reglas globales de agentes: `~/.claude/rules/rules_agents.instructions.md`

---

## 11. ROLES Y REVISORES POR FASE

| Fases | Reviewer | UUID |
|-------|----------|------|
| Fases 1-4 (Setup, Discovery, Planning, Analysis) | SA Reviewer | `0c128e3b-db3b-4e31-b107-0379b5791233` |
| Fases 5-6 (Design UX/UI + Technical) | Design Lead | `b3a09269-cded-468c-a475-15a48f203cb0` |
| Fases 7-10 (Development, Testing, Deploy, Operations) | Tech Lead | `92225290-6b6b-4c1f-a940-dcb4262507aa` |

### Archivos de setup por rol

| Rol | OPERATIVO | CONTEXTO sesión | SETUP |
|-----|-----------|-----------------|-------|
| Tech Lead | `.claude/agents/OPERATIVO_TECH_LEAD.md` | `knowledge/agent-tasks/CONTEXTO_TL_SESION.md` | `00-agent-setup/01.agent-setup/SETUP_TL.md` |
| SA Reviewer | `.claude/agents/OPERATIVO_SA_REVIEWER.md` | `knowledge/agent-tasks/CONTEXTO_SA_REVIEWER_SESION.md` | `00-agent-setup/01.agent-setup/SETUP_SA_REVIEWER.md` |

### Documentos clave del proyecto

| Documento | Ruta |
|-----------|------|
| Kickoff formal | `memory-service-project/knowledge/kickoff/KICKOFF_MEMORY_SERVICE.md` |
| Acta Kickoff (Phase 1 → 2) | `memory-service-project/knowledge/kickoff/KICKOFF_ACTA_2026-05-04.md` |
| SPEC v1.9 | `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` |

---

**Mantenimiento:** este archivo se actualiza cuando cambia el stack, las fases, o hay nuevas decisiones arquitectónicas. No se actualiza con cambios de tareas individuales (eso va en `CONTEXTO_TECH_LEAD_SESION.md` o `CONTEXTO_SA_REVIEWER_SESION.md`).
