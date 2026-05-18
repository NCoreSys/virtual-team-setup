# CIERRE PM + HANDOFF OPERATIVO PJM — MEMORY SERVICE R1

| Campo | Valor |
|-------|-------|
| **Documento** | CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-04-22 |
| **Fase SDLC** | 02-Analysis → Cierre · 04-Development → Handoff |
| **Autor** | PM (Martin Rivas) |
| **Destinatario** | PJM (Project Manager) |
| **Proyecto** | Memory Service R1 (`51e169f7-8a23-4628-8b78-04864b633ac7`, key MEM) |
| **Estado** | ✅ CERRADO — Listo para ejecución |

---

## PARTE I: CIERRE PM DEL ANÁLISIS

### 1. DOCUMENTOS CONSUMIDOS
`C:\Users\Martin\Documents\virtual-teams\memory-service\memory-service-project\Release2.0`

| # | Documento | Versión | Autor | Estado |
|---|-----------|---------|-------|--------|
| 1 | SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md | 1.9 | PM + SA | ✅ Aprobado PM 2026-04-21 |
| 2 | METODOLOGIA_MEMORY_SERVICE_v1.2.md | 1.1 | PM | ✅ Vigente |
| 3 | ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md | 1.1 | PM | ✅ Aprobado PM, integrado al SPEC |
| 4 | FASES_APLICABLES_MEMORY_SERVICE.md | 2.0 | PM | ✅ Aprobado PM 2026-04-22 |
| 5 | CONSOLIDADO_MEMORY_SERVICE_R1.md | 1.0 | PM | ✅ Plan maestro |
| 6 | PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md | 1.0 | PM | ✅ 24 tareas iniciación |
| 7 | PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md | 1.0 | PM | ✅ 66 tareas implementación |
| 8 | PLAN_116_TAREAS.md | 1.0 | TL | ✅ Vista TL del plan |
| 9 | HO_ACTUALIZAR_TAREAS_VTT.md | 2.1 | PJM | ✅ UUIDs tareas + deliveries |
| 10 | AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md | 1.0 | AR | ✅ 7 bloqueos resueltos |
| 11 | DB_REVIEW_SPEC_MEMORY_SERVICE_v1.md | 1.0 | DB | ✅ Aprobado con observaciones |
| 12 | TL_REVIEW_SPEC_MEMORY_SERVICE_v1.md | 1.0 | TL | ✅ Aprobado (AMB-01 cerrada) |
| 13 | SPEC_RUNTIME_v1.1.md | 1.1 | PM upstream | Referencia integración |
| 14 | SPEC_PROMPT_BUILDER_v1.3.md | 1.3 | PM upstream | Referencia integración |

---

### 2. DECISIONES PM FINALES (48 FROZEN)

Todas las decisiones están **CONGELADAS**. No se reabren.

#### 2.1 Arquitectura R1 (D-MEM-01 a D-MEM-28) — 28 decisiones

| ID | Decisión |
|----|----------|
| D-MEM-01 | Sistema **independiente** de VTT |
| D-MEM-02 | VTM legacy se descarta |
| D-MEM-03 | Transporte multipart a VM |
| D-MEM-04 | SDK envía 2 archivos (session + log) |
| D-MEM-05 | Idempotencia compuesta `sourceId + externalSessionId` |
| D-MEM-06 | Storage paths diferenciados (TASK · REVIEW) |
| D-MEM-07 | Contexto `<500ms` síncrono, fail-fast |
| D-MEM-08 | Clasificación R1 por reglas determinísticas |
| D-MEM-09 | Fuentes en catálogo extensible |
| D-MEM-10 | IDs String (TEXT) |
| D-MEM-11 | `taskId` (UUID) + `taskKey` auxiliar |
| D-MEM-12 | `taskTitle` desnormalizado |
| D-MEM-13 | Status PENDING → PROCESSING → IMPORTED/ERROR |
| D-MEM-14 | Endpoints separados JSONL vs VTT_CHANNEL |
| D-MEM-15 | `conversationType` discriminador |
| D-MEM-16 | VTT_CHANNEL incremental |
| D-MEM-17 | `platformRefs` JSON nullable |
| D-MEM-18 | JSONL sin stripping |
| D-MEM-19 | Entregables responsabilidad de Hook Manager |
| D-MEM-20 | Tipos en catálogos BD |
| D-MEM-21 | `topics`/`entities` join tables |
| D-MEM-22 | Rate limit memory → Redis |
| D-MEM-23 | Redis prefix `mem` |
| D-MEM-24 | BD `memory_service_db` |
| D-MEM-25 | Storage bind mount |
| D-MEM-26 | Auth SERVICE_KEY |
| D-MEM-27 | `connection_limit=20` |
| D-MEM-28 | `mem_limit: 512m` |

#### 2.2 Revisión AR (D-MEM-29 a D-MEM-37) — 9 decisiones

| ID | Decisión |
|----|----------|
| D-MEM-29 | `primaryAgentId` nullable; AGENT_REVIEW → NULL + participants |
| D-MEM-30 | PlatformCatalog incluye VTT_CHANNEL y GOOGLE_DOCS |
| D-MEM-31 | `startedAt`/`endedAt` del contenido, no del import |
| D-MEM-32 | `importedAt` separado para auditoría |
| D-MEM-33 | `GET /context` usa `projectId`/`taskId` |
| D-MEM-34 | PROCESSING explícito antes de escribir |
| D-MEM-35 | Cleanup cron cada 5 min · STALE > 10 min |
| D-MEM-36 | `agentId` = User.id VTT (Q-01 cerrada) |
| D-MEM-37 | `GET /context` siempre síncrono fail-fast (Q-05 cerrada) |

#### 2.3 Correcciones AR v1.4 (D-MEM-38 a D-MEM-42) — 5 decisiones

| ID | Decisión |
|----|----------|
| D-MEM-38 | `primaryAgentRole` desnormalizado en import |
| D-MEM-39 | `GET /context` SIEMPRE filtra por `projectId` |
| D-MEM-40 | Cleanup: `retryCount <= MAX_RETRIES` |
| D-MEM-41 | Constraints `@@unique([conversationId, turnIndex])` y `@@unique([turnId, blockIndex])` |
| D-MEM-42 | Idempotencia compuesta robusta cross-source |

#### 2.4 Revisión TL v1.4 (D-MEM-43) — 1 decisión

| ID | Decisión |
|----|----------|
| D-MEM-43 | `contentPreview` (500 chars) en BD · `GET /content` parsea `/storage/` (AMB-01 cerrada) |

#### 2.5 Integración Cross-Service (D-INT-01 a D-INT-05) — 5 decisiones

| ID | Decisión | Origen |
|----|----------|--------|
| D-INT-01 | Granularidad: una conversación por ronda | Runtime v1.1 |
| D-INT-02 | `externalSessionId = {run_id}:r{N}:{agentRole}` | Runtime v1.1 |
| D-INT-03 | `sourceCode: CLAUDE_SDK` (no nueva fuente) | Runtime v1.1 |
| D-INT-04 | `run_id` en `platformRefs.runtime_run_id` | Runtime v1.1 |
| D-INT-05 | Transformación JSON→texto responsabilidad PB | PB v1.3 |

---

### 3. CORRECCIONES INCORPORADAS (24)

Todas integradas al SPEC v1.9.

| Origen | Código | Corrección |
|--------|--------|------------|
| AR | AR-OBS-01 | Versionado header/changelog/footer |
| AR | AR-OBS-02 | Cleanup usa `statusId` |
| DB | DB-OBS-01 | `@@unique([conversationId, entityName])` |
| DB | DB-OBS-02 | Cleanup por `statusId` |
| DB | DB-OBS-03 | N+1 en `importAgentReview` (prefetch catálogos) |
| DB | DB-OBS-04 | Partial indexes como SQL manual |
| DB | DB-OBS-05 | Índice `(primaryAgentId, projectId, startedAt DESC)` |
| DB | DB-OBS-06 | Índice `AgentMessage(conversationId, timestamp DESC)` |
| DB | DB-OBS-07 | Índice `Conversation(importedAt DESC)` |
| DB | DB-OBS-08 | Manejo P2002 race condition |
| TL | DEC-04/AMB-01 | `contentPreview` vs contenido completo |
| TL | TL-01 | Pre-fetch `statusId` antes de transacción |
| TL | TL-03 | Maps pre-fetcheados en cache |
| TL | AMB-07 | Catch delega siempre al cleanup job |
| PM | Punto 1 | Constraint ConversationEntity |
| PM | Punto 2 | Partial indexes SQL manual |
| PM | Punto 3 | Manejo P2002 idempotencia concurrente |
| PM | Punto 4 | Cache catálogos en startup |
| PM | Punto 5 | Cleanup filtra por `statusId` |
| PM | Punto 6 | Prefetch catálogos en importAgentReview |
| PM | Punto 7 | Índices DB adicionales |
| PM | Punto 8 | Versionado consistente |
| ADDENDUM | INT-01 | platformRefs Runtime documentado §4.1 SPEC |
| ADDENDUM | INT-02 | Índice GIN `idx_conv_runtime_run` §6.1 SPEC |

---

### 4. LIMITACIONES R1 DOCUMENTADAS

| # | Limitación | Fase resolución |
|---|------------|-----------------|
| LIM-01 | No hay búsqueda full-text sobre contenido | R2 |
| LIM-02 | No hay búsqueda semántica / embeddings | R2 |
| LIM-03 | Clasificación solo por reglas (no LLM) | R3 |
| LIM-04 | Multi-agente solo en REVIEW/CLARIFICATION | R2 |
| LIM-05 | Sin RBAC / `workspaceId` | Cuando VTT lo active |
| LIM-06 | Sin retención automática / purge | R2 |
| LIM-07 | UI sin autenticación | R2 |
| LIM-08 | UI solo desktop (sin mobile/tablet/dark) | R2 |
| LIM-09 | Sin export PDF/CSV | R2 |
| LIM-10 | Cleanup job resetea a PENDING sin re-parseo | R1 aceptado |

---

### 5. REASSIGNMENTS APROBADOS

| Task | Título | Fase | Plan PJM | Aprobado PM | Razón |
|------|--------|------|----------|-------------|-------|
| MEM-022 | Business Rules | Analysis | TL | ✅ **SA** | Artefacto de análisis de sistemas |
| MEM-039 | Solution Architecture | Design Technical | TL | ✅ **AR** | Deliverable principal del Architect |

**Impacto:** TL 7→5 tareas (25h→15h) · SA 7→8 (36h→40h) · AR 6→7 (23h→29h).

---

### 6. VEREDICTO PM

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ✅ ANÁLISIS CERRADO — APROBADO PARA EJECUCIÓN                          ║
║                                                                           ║
║   48 decisiones PM congeladas (43 D-MEM + 5 D-INT)                       ║
║   24 correcciones incorporadas al SPEC v1.9                              ║
║   10 limitaciones R1 documentadas                                        ║
║   2  reassignments TL → SA/AR aprobados                                  ║
║   0  bloqueos pendientes de decisión PM                                  ║
║   0  inconsistencias abiertas                                             ║
║                                                                           ║
║   Alcance R1:                                                             ║
║   · 19 tablas principales + 10 catálogos                                 ║
║   · 11 endpoints API R1                                                  ║
║   · 9 pantallas UI standalone (P0-P3)                                    ║
║   · 5 fuentes soportadas (CLI, Web, SDK, ChatGPT, VTT_CHANNEL)           ║
║   · Integraciones: Runtime v1.1 · Prompt Builder v1.3 · Hook Manager     ║
║                                                                           ║
║   Plan maestro:                                                           ║
║   · Iniciación (pre-SDLC): 24 tareas · 32h                               ║
║   · Fases SDLC 0-7:        116 tareas · 381h                             ║
║   · 65 deliveries VTT  ·  390 deliverables aplicables                    ║
║   · TOTAL: 135 tareas · ~402h                                             ║
║                                                                           ║
║   El paquete está listo para ejecución operativa vía PJM.                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## PARTE II: HANDOFF OPERATIVO PARA PJM

### 7. ALCANCE FINAL R1

#### 7.1 Tablas principales (19) + catálogos (10)

**Tablas principales:** `conversation` · `conversation_turn` · `turn_block` · `conversation_usage` · `classification` · `conversation_topic` · `conversation_entity` · `conversation_participant` · `agent_message`.

**Catálogos (seed data):** SourceCatalog · ConversationTypeCatalog · ConversationStatusCatalog · WorkTypeCatalog · BlockTypeCatalog · MessageTypeCatalog · MessageStatusCatalog · PlatformCatalog · TopicCatalog · PriorityCatalog.

#### 7.2 Endpoints R1 (11)

| # | Método | Ruta | Auth | Consumidor |
|---|--------|------|------|------------|
| 1 | POST | `/api/conversations/import` | SERVICE_KEY | Hook Manager / Runtime |
| 2 | POST | `/api/conversations/import-review` | SERVICE_KEY | Hook Manager |
| 3 | POST | `/api/conversations/upload` | Público R1 | UI |
| 4 | GET | `/api/conversations` | Público R1 | UI |
| 5 | GET | `/api/conversations/:id/content` | Público R1 | UI |
| 6 | GET | `/api/context` | SERVICE_KEY | Prompt Builder |
| 7 | GET | `/api/agents/:id/timeline` | Público R1 | UI |
| 8 | GET | `/api/projects/:id/cost-report` | Público R1 | UI |
| 9 | GET | `/api/agents/:id/cost-report` | Público R1 | UI |
| 10 | GET | `/api/dashboard/stats` | Público R1 | UI |
| 11 | GET | `/health` | Público | Monitoring |

#### 7.3 UI Standalone (9 pantallas, puerto 3003)

P0: Agent Timeline · Conversation Viewer (TASK)
P1: Dashboard · Cost Report Proyecto · Import Manual
P2: Conversation Viewer (REVIEW) · Lista/Búsqueda
P3: Cost Report Agente · Health

#### 7.4 Infraestructura (Hetzner compartida)

| Recurso | Valor |
|---------|-------|
| VM | `77.42.88.106` |
| Puertos | API 3002 · UI 3003 |
| BD | `memory_service_db` en shared-postgres (connection_limit=20) |
| Redis | shared-redis prefix `mem` |
| Storage | Bind mount `/root/memory-service-storage/` |
| RAM | 512 MB / 256 MB reserved |
| Red | `shared-network` |

#### 7.5 Integraciones cross-service

| Consumidor | Endpoint | Cuándo |
|------------|---------|--------|
| Runtime v1.1 | `POST /import` (CLAUDE_SDK) | Al terminar ronda por agente |
| Prompt Builder v1.3 | `GET /context` | Al ensamblar prompt |
| Hook Manager VTT | `POST /import-review` | Canal VTT_CHANNEL |
| UI Standalone | Todos los GET + `POST /upload` | Interacción usuario |

#### 7.6 Diferido a R2+

Ver §4 (LIM-01 a LIM-09).

---

### 8. FASE DE INICIACIÓN DEL PROYECTO (pre-SDLC)

**24 tareas · 32h** antes de arrancar Phase 0 Discovery. Desglose operativo de MEM-001..005 (cuyas horas en VTT deben actualizarse 11h → 32h).

#### 8.1 Resumen por categoría

| Categoría | Tareas | Horas | MEM original |
|-----------|-------:|------:|--------------|
| A. VTT Setup | 5 | 6h | MEM-003 (parcial) |
| B. Repository Setup | 5 | 5h | MEM-002 |
| C. VM Configuration | 4 | 4h | MEM-001 |
| D. Agent Team Setup | 5 | 8h | MEM-003 |
| E. Tooling Setup | 3 | 4h | MEM-004 |
| F. Documentation | 2 | 2h | MEM-005 (parcial) |
| G. Kickoff | 2 | 3h | MEM-005 |

Ver detalle completo en `PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md` §4.

#### 8.2 Estado actual (bloqueos pre-arranque)

| Item | Estado | Acción |
|------|--------|--------|
| Proyecto VTT + 10 fases + 65 deliveries + 116 tareas | ✅ Hecho | — |
| Infra VM provisionada (BD, volumen, SERVICE_KEY, Redis) | ✅ Hecho | — |
| PATCH 116 tareas con metadata (assigneeId, complexity, hours) | 🟡 Pendiente | INIT-A-04, PJM+DO |
| Repo Git real (remoto apunta a `twitter-react`) | 🔴 Bloqueado | PM define multi-repo |
| Endpoint VTT de dependencias | 🔴 Bloqueado | Registro manual por ahora |
| OPERATIVOs de roles (2/12 hechos) | 🟡 Parcial | PM crea los 10 faltantes |

---

### 9. SECUENCIA DE FASES SDLC

```
╔════════════════════════════════════════════════════════════════════════╗
║ FASE 0: INICIACIÓN (pre-SDLC)  ·  24 tareas  ·  32h                    ║
║   A. VTT · B. Repo · C. VM · D. Team · E. Tooling · F. Docs · G. Kickoff║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE A: FUNDACIÓN                                                      ║
╠════════════════════════════════════════════════════════════════════════╣
║  Discovery (MEM-006..009) ─────────────── 4 tareas · 9h                ║
║  Planning  (MEM-010..017) ─────────────── 8 tareas · 23h               ║
║  Analysis  (MEM-018..025) ─────────────── 8 tareas · 41h               ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE B: DISEÑO (paralelo UX/UI ↔ Technical)                            ║
╠════════════════════════════════════════════════════════════════════════╣
║  Design UX/UI       (MEM-026..038) · 13 tareas · 35h · 🚨 MEM-038 hito ║
║  Design Technical   (MEM-039..047) ·  9 tareas · 45h                   ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE C: DESARROLLO BACKEND (secuencial S01 → S06)                      ║
╠════════════════════════════════════════════════════════════════════════╣
║  S01 Schema + Seeds          (MEM-048..052) · 5 tareas ·  9h           ║
║  S02 Import + Timeline       (MEM-053..057) · 5 tareas · 12h           ║
║  S03 Content + Context       (MEM-058..062) · 5 tareas · 12h           ║
║  S04 Adapters + Cleanup      (MEM-063..068) · 6 tareas · 12h           ║
║  S05 Lista + Cost + Dashboard(MEM-069..074) · 6 tareas · 11h           ║
║  S06 Docker + Integration    (MEM-075..080) · 6 tareas · 14h           ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE D: DESARROLLO FRONTEND (desbloqueado por MEM-038)                 ║
╠════════════════════════════════════════════════════════════════════════╣
║  UI-01 Setup + Timeline + Viewer (MEM-081..085) · 5 tareas · 16h       ║
║  UI-02 Dashboard + Cost + Import (MEM-086..088) · 3 tareas · 12h       ║
║  UI-03 Viewer REVIEW + Lista     (MEM-089..090) · 2 tareas · 10h       ║
║  UI-04 Cost Agente + Health      (MEM-091..093) · 3 tareas ·  8h       ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE E: VALIDACIÓN                                                     ║
╠════════════════════════════════════════════════════════════════════════╣
║  Testing (MEM-094..103) ───────────────── 10 tareas · 60h              ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE F: LANZAMIENTO                                                    ║
╠════════════════════════════════════════════════════════════════════════╣
║  Deploy     (MEM-104..110) ─────────────── 7 tareas · 26h              ║
║  Operations (MEM-111..116) ─────────────── 6 tareas · 15h              ║
╚════════════════════════════════════════════════════════════════════════╝

TOTAL: 135 tareas · ~402h · 10 fases + iniciación
```

**Paralelismo permitido:**
- Design UX/UI ↔ Design Technical (paralelo)
- Backend y Frontend en paralelo una vez UI-01 arranca
- DO tareas INIT + MEM-075..077 pueden adelantarse

---

### 10. PLAN COMPLETO DE TAREAS POR FASE (con mapeo tarea → deliverables)

> **Nota metodológica crítica:** Cada tarea VTT puede producir **varios deliverables SDLC**. La columna "Produce" hace explícito ese mapeo para evitar la ambigüedad que causó retrabajo en el análisis previo.

#### 10.1 Fase 0 · Discovery (4 tareas · 9h · 10 deliverables)

| Task | Título | Delivery | Rol | Horas | Complexity | Produce (deliverables SDLC) |
|------|--------|----------|-----|------:|------------|------------------------------|
| MEM-006 | Problem Definition | Problem Definition | SA | 3h | MEDIUM | 0.3.1 Problem Statement · 0.3.2 User Pain Points · 0.3.3 Current Solutions · 0.3.4 Why Now |
| MEM-007 | Problem Validation | Problem Definition | PM | 2h | LOW | 0.3.5 Problem Validation (interno VTT) |
| MEM-008 | Value Proposition | Value Proposition | SA | 3h | MEDIUM | 0.4.1 VPC · 0.4.2 UVP Statement · 0.4.3 Key Differentiators · 0.4.4 Target Customer · 0.4.5 Value Hypothesis |
| MEM-009 | Value Validation | Value Proposition | PM | 1h | LOW | Sign-off de 0.4.* |

#### 10.2 Fase 1 · Planning (8 tareas · 23h · 33 deliverables)

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-010 | Vision | Vision & Objectives | PM | 3h | MEDIUM | 1.1.1 Vision · 1.1.2 Mission · 1.1.5 North Star |
| MEM-011 | Objectives | Vision & Objectives | PM | 2h | MEDIUM | 1.1.3 Goals · 1.1.4 KPIs · 1.1.6 OKRs |
| MEM-012 | Scope | Scope | SA | 4h | HIGH | 1.2.1 a 1.2.6 (6 docs) |
| MEM-013 | Stakeholders | Stakeholders | PJM | 2h | LOW | 1.3.1 a 1.3.4 (4 docs) |
| MEM-014 | Risks | Risks | PJM | 3h | MEDIUM | 1.4.1 a 1.4.5 (5 docs) |
| MEM-015 | Timeline | Timeline | PJM | 4h | HIGH | 1.5.1 Schedule · 1.5.5 Dependencies · 1.5.6 Critical Path · 1.5.7 Buffer |
| MEM-016 | Milestones | Timeline | PJM | 3h | MEDIUM | 1.5.2 Milestones · 1.5.3 Phase Breakdown · 1.5.4 Sprint Calendar |
| MEM-017 | Budget & Resources | Budget & Resources | PM | 2h | LOW | 1.6.1 a 1.6.5 (5 docs) |

#### 10.3 Fase 2 · Analysis (8 tareas · 41h · 47 deliverables)

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-018 | Functional Requirements | Functional Requirements | SA | 6h | HIGH | 2.1.1 a 2.1.6 (6 docs) |
| MEM-019 | Non-Functional Requirements | NFR | AR | 4h | HIGH | 2.2.1 a 2.2.6 (6 docs) incluye `<500ms` + SERVICE_KEY |
| MEM-020 | Use Cases | Use Cases | SA | 5h | MEDIUM | 2.3.1 a 2.3.6 (6 docs) |
| MEM-021 | User Stories | User Stories | SA | 8h | HIGH | 2.4.1 a 2.4.6 (6 docs) |
| MEM-022 | Business Rules | Business Rules | SA ⚠️ | 4h | HIGH | 2.5.1 a 2.5.7 (7 docs) |
| MEM-023 | User Flows | User Flows | UX | 4h | MEDIUM | 2.6.1 a 2.6.7 (7 docs) |
| MEM-024 | Acceptance Criteria | Acceptance Criteria | SA | 6h | HIGH | 2.7.1 a 2.7.5 (5 docs) |
| MEM-025 | Traceability Matrix | Traceability Matrix | SA | 4h | MEDIUM | 2.8.1 a 2.8.4 (4 docs) |

#### 10.4 Fase 3A · Design UX/UI (13 tareas · 35h · 40 deliverables)

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-026 | Personas | Personas | UX | 3h | MEDIUM | 3A.2.1, 3A.2.2, 3A.2.3, 3A.2.4, 3A.2.6, 3A.2.8 (6 docs) |
| MEM-027 | Information Architecture | IA | UX | 4h | MEDIUM | 3A.3.1, 3A.3.2, 3A.3.3, 3A.3.4, 3A.3.5, 3A.3.7, 3A.3.8 (7 docs) |
| MEM-028 | Design System | Design System | DL | 3h | MEDIUM | 3A.7.1 a 3A.7.8 + 3A.7.10 (9 docs) |
| MEM-029 | Wireframes — Dashboard | Wireframes | DL | 4h | HIGH | 3A.4 parcial (Dashboard) |
| MEM-030 | Wireframes — Timeline | Wireframes | DL | 3h | MEDIUM | 3A.4 parcial (Timeline) |
| MEM-031 | Wireframes — Viewer | Wireframes / Mockups | DL | 4h | HIGH | 3A.4 + 3A.5 parcial (Viewer) |
| MEM-032 | Wireframes — Cost Report | Wireframes / Mockups | DL | 4h | HIGH | 3A.4 + 3A.5 parcial (Cost) |
| MEM-033 | Wireframes — Lista Convs | Wireframes | DL | 2h | MEDIUM | 3A.4 parcial (Lista) |
| MEM-034 | Wireframes — Import Manual | Wireframes | DL | 2h | MEDIUM | 3A.4 parcial (Import) |
| MEM-035 | Wireframes — Health | Wireframes | DL | 2h | MEDIUM | 3A.4 parcial (Health) |
| MEM-036 | Wireframes — Extras | Wireframes | DL | 1h | LOW | 3A.4.7, 3A.4.8, 3A.4.9 · 3A.5.5..3A.5.8 (estados) |
| MEM-037 | Design Handoff — Assets | Design Handoff | DL | 2h | MEDIUM | 3A.9.2 Specs · 3A.9.3 Assets · 3A.9.4 CSS Variables |
| **MEM-038** | **Design Handoff — Final** 🚨 | Design Handoff | DL | 1h | LOW | 3A.9.1 Handoff Doc · 3A.9.5 Redlines |

> 🚨 **MEM-038 bloquea MEM-081+ (inicio FE).**

#### 10.5 Fase 3B · Design Technical (9 tareas · 45h · 73 deliverables)

> La mayoría de deliverables 3B **ya están contenidos en SPEC v1.9**, METODOLOGIA v1.2 y ADDENDUM v1.1. Las tareas los consolidan como documentos independientes.

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-039 | Solution Architecture | Solution Architecture | AR ⚠️ | 6h | HIGH | 3B.1.1 a 3B.1.7 (7 docs, C4 L1-L3) |
| MEM-040 | Code Architecture | Code Architecture | TL | 4h | HIGH | 3B.2.1 a 3B.2.6 (6 docs) |
| MEM-041 | Database Design | Database Design | DB | 6h | HIGH | 3B.3.1 a 3B.3.8 (8 docs) |
| MEM-042 | API Design | API Design | BE | 8h | HIGH | 3B.4.1 a 3B.4.11 (11 docs) |
| MEM-043 | Sequence Diagrams | Sequence Diagrams | AR | 6h | HIGH | 3B.5.1 a 3B.5.6 (6 docs) |
| MEM-044 | ADRs | ADRs | TL | 4h | MEDIUM | 3B.6.1 a 3B.6.4 (4 docs + 48 ADRs individuales) |
| MEM-045 | Security Plan | Security Plan | AR | 4h | HIGH | 3B.7.1 a 3B.7.11 (11 docs) |
| MEM-046 | Infrastructure Plan | Infrastructure Plan | DO | 4h | MEDIUM | 3B.8.1 a 3B.8.11 (11 docs) |
| MEM-047 | Technical Estimates | Technical Estimates | TL | 3h | MEDIUM | 3B.9.1 a 3B.9.9 (9 docs) |

#### 10.6 Fase 4 · Development (46 tareas · 116h)

**Deliverables aplicables 4.1-4.8 (75)** son producidos por estas tareas:

##### S01 · Schema + Seeds (5 tareas · 9h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-048 | DB Schema Prisma completo | DB | 3h | HIGH | 4.2.1 Initial Migration · `prisma/schema.prisma` (19 tablas + 10 catálogos) |
| MEM-049 | Migraciones + Partial Indexes + GIN | DB | 2h | MEDIUM | 4.2.2 Schema Migrations · 4.2.5 Indexes · 4.2.6 Constraints · 4.2.9 Migration Guide · 4.2.10 Rollback Scripts |
| MEM-050 | Seed de 10 catálogos | DB | 1h | LOW | 4.2.3 Seed Data · 4.2.4 Test Data |
| MEM-051 | Setup Express + estructura | BE | 2h | MEDIUM | 4.3.1 a 4.3.8 infraestructura base · 4.3.13 Backend README |
| MEM-052 | Catalog cache startup | BE | 1h | LOW | `catalog-cache.service.ts` (soporte 4.3.2 services) |

##### S02 · Import + Timeline (5 tareas · 12h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-053 | POST /import (4 fuentes) | BE | 4h | HIGH | 4.3.1 Endpoints · 4.5.1 Integration Code · 4.5.2 API Clients |
| MEM-054 | POST /import-review (VTT_CHANNEL) | BE | 2h | MEDIUM | 4.3.1 parcial · 4.5.3 Webhooks |
| MEM-055 | POST /upload (manual) | BE | 3h | HIGH | 4.3.1 parcial |
| MEM-056 | GET /agents/:id/timeline | BE | 2h | MEDIUM | 4.3.1 parcial |
| MEM-057 | Error handling + cleanup delegation | BE | 1h | LOW | 4.3.14 Error Handling · 4.3.15 Logging |

##### S03 · Content + Context (5 tareas · 12h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-058 | GET /content (parse storage) | BE | 2h | MEDIUM | 4.3.1 parcial (endpoint crítico D-MEM-43) |
| MEM-059 | GET /context (<500ms fail-fast) | BE | 4h | HIGH | 4.3.1 parcial (endpoint SLA crítico) |
| MEM-060 | Classifier determinístico | BE | 2h | HIGH | 4.3.2 Services (classifier) |
| MEM-061 | Tests performance contexto | QA | 2h | MEDIUM | 4.6.1 Unit Tests BE parcial |
| MEM-062 | Tests classifier | QA | 2h | MEDIUM | 4.6.1 Unit Tests BE parcial |

##### S04 · Adapters + Cleanup (6 tareas · 12h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-063 | Adapter CLAUDE_WEB | BE | 3h | MEDIUM | 4.3.2 Services (adapter) |
| MEM-064 | Adapter CHATGPT | BE | 2h | MEDIUM | 4.3.2 Services (adapter) |
| MEM-065 | Storage writer JSONL | BE | 2h | MEDIUM | 4.3.2 Services (storage) |
| MEM-066 | Cleanup cron (5 min) | BE | 2h | MEDIUM | 4.3.6 Workers (cleanup job) |
| MEM-067 | Status transitions handler | BE | 1h | LOW | 4.3.8 Utils |
| MEM-068 | Tests adapters | BE | 2h | MEDIUM | 4.6.5 Mock Factories · 4.6.6 Test Fixtures |

##### S05 · Lista + Cost + Dashboard (6 tareas · 11h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-069 | GET /conversations (lista) | BE | 2h | MEDIUM | 4.3.1 parcial |
| MEM-070 | GET /projects/:id/cost-report | BE | 2h | MEDIUM | 4.3.1 parcial |
| MEM-071 | GET /agents/:id/cost-report | BE | 2h | MEDIUM | 4.3.1 parcial |
| MEM-072 | GET /dashboard/stats | BE | 2h | MEDIUM | 4.3.1 parcial |
| MEM-073 | GET /health | BE | 2h | MEDIUM | 4.3.1 parcial |
| MEM-074 | Integration tests endpoints | BE | 1h | LOW | 4.3.10 Integration Tests |

##### S06 · Docker + Integration (6 tareas · 14h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-075 | Dockerfile + docker-compose | DO | 2h | MEDIUM | 4.1.4 Docker Compose · 4.1.1 Dev Environment |
| MEM-076 | CI config | DO | 2h | MEDIUM | 4.1.5 Makefile / Scripts (CI) |
| MEM-077 | Env vars + secrets | DO | 1h | LOW | 4.1.3 Environment Variables |
| MEM-078 | Integración Hook Manager VTT | BE | 4h | HIGH | 4.5.1 Integration Code · 4.5.2 API Clients · 4.5.6 Integration Tests · 4.5.7 Integration Docs |
| MEM-079 | E2E test Runtime integration | QA | 3h | HIGH | 4.5.6 Integration Tests |
| MEM-080 | E2E test Prompt Builder integration | QA | 2h | MEDIUM | 4.5.6 Integration Tests |

##### UI-01..04 · Frontend (13 tareas · 46h)

| Task | Título | Rol | Horas | Complexity | Produce |
|------|--------|-----|------:|------------|---------|
| MEM-081 | Setup React + Vite + Tailwind | FE | 2h | MEDIUM | 4.4.8 Styles · 4.4.13 Frontend README |
| MEM-082 | Routing + layout base | FE | 1h | LOW | 4.4.2 Pages · 4.4.3 Layouts |
| MEM-083 | Page Timeline agente | FE | 5h | HIGH | 4.4.1 Components · 4.4.2 Pages |
| MEM-084 | Component Conversation Viewer | FE | 6h | HIGH | 4.4.1 Components (TASK viewer) |
| MEM-085 | Auth context (SERVICE_KEY) | FE | 2h | MEDIUM | 4.4.4 Hooks · 4.4.5 State Management · 4.4.6 API Client |
| MEM-086 | Page Dashboard | FE | 4h | HIGH | 4.4.2 Pages |
| MEM-087 | Page Cost Report Proyecto | FE | 4h | MEDIUM | 4.4.2 Pages |
| MEM-088 | Page Import Manual | FE | 4h | MEDIUM | 4.4.2 Pages |
| MEM-089 | Page Lista conversaciones | FE | 5h | HIGH | 4.4.2 Pages |
| MEM-090 | Component AGENT_REVIEW | FE | 5h | HIGH | 4.4.1 Components (REVIEW thread) |
| MEM-091 | Page Cost Report Agente | FE | 3h | MEDIUM | 4.4.2 Pages |
| MEM-092 | Page Health | FE | 2h | LOW | 4.4.2 Pages |
| MEM-093 | Polish + responsive desktop | FE | 3h | MEDIUM | 4.4.10 Unit Tests FE · 4.4.11 Component Tests · 4.4.14 Accessibility · 4.4.15 Responsive |

#### 10.7 Fase 5 · Testing (10 tareas · 60h · 51 deliverables)

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-094 | Test Planning | Test Planning | QA | 4h | MEDIUM | 5.1.1 a 5.1.5 (5 docs) |
| MEM-095 | Test Cases completos | Test Cases | QA | 8h | HIGH | 5.2.1 a 5.2.4 (4 docs) |
| MEM-096 | Test Environment setup | Test Environment | DO | 4h | MEDIUM | 5.3.1 a 5.3.4 (4 docs) |
| MEM-097 | Functional Testing | Functional Testing | QA | 8h | HIGH | 5.4.1 a 5.4.5 (5 docs) |
| MEM-098 | Integration Testing | Integration Testing | QA | 6h | HIGH | 5.5.1 a 5.5.4 (4 docs) |
| MEM-099 | E2E Testing | E2E Testing | QA | 8h | HIGH | 5.6.1 a 5.6.5 (5 docs) |
| MEM-100 | Performance Testing | Performance Testing | QA | 6h | HIGH | 5.7.1 a 5.7.6 (6 docs) — validación SLA <500ms |
| MEM-101 | Security Testing | Security Testing | AR | 4h | HIGH | 5.8.1 a 5.8.7 (7 docs) |
| MEM-102 | UAT | UAT | PM | 4h | MEDIUM | 5.10.1 a 5.10.5 (5 docs) — equipo VTT interno |
| MEM-103 | Bug Fixes | Bug Fixes | BE | 8h | HIGH | 5.11.1 a 5.11.3 (3 docs) + correcciones |

Accessibility (5.9.1, 5.9.2, 5.9.4) producidos transversalmente en MEM-097 + MEM-093.

#### 10.8 Fase 6 · Deploy (7 tareas · 26h · 38 deliverables)

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-104 | Infrastructure Setup | Infrastructure Setup | DO | 4h | MEDIUM | 6.1.1 a 6.1.8 (8 docs) |
| MEM-105 | CI/CD Configuration | CI/CD | DO | 6h | HIGH | 6.2.1 a 6.2.6 (6 docs) |
| MEM-106 | Staging Deploy | Staging Deploy | DO | 4h | MEDIUM | 6.3.1 a 6.3.4 (4 docs) |
| MEM-107 | Smoke Testing | Smoke Testing | QA | 3h | MEDIUM | 6.4.1 a 6.4.3 (3 docs) |
| MEM-108 | Production Deploy | Production Deploy | DO | 4h | HIGH | 6.5.1 a 6.5.6 (6 docs) |
| MEM-109 | Post-Deploy Monitoring | Post-Deploy Monitoring | DO | 3h | MEDIUM | 6.6.1 a 6.6.6 (6 docs) |
| MEM-110 | Rollback Plan | Rollback Plan | TL | 2h | MEDIUM | 6.7.1 a 6.7.5 (5 docs) |

#### 10.9 Fase 7 · Operations (6 tareas · 15h · 23 deliverables)

| Task | Título | Delivery | Rol | Horas | Complexity | Produce |
|------|--------|----------|-----|------:|------------|---------|
| MEM-111 | Monitoring setup | Monitoring | DO | 3h | MEDIUM | 7.1.1 a 7.1.4 (4 docs) |
| MEM-112 | User Support docs | User Support | PM | 2h | LOW | 7.2.1 a 7.2.4 (4 docs) |
| MEM-113 | Bug Fixes Operations playbook | Bug Fixes Ops | TL | 2h | MEDIUM | 7.3.1 a 7.3.3 (3 docs) |
| MEM-114 | Incremental Improvements | Incremental | PM | 3h | MEDIUM | 7.4.1 a 7.4.4 (4 docs) |
| MEM-115 | Security Updates | Security Updates | AR | 2h | MEDIUM | 7.5.1 a 7.5.4 (4 docs) |
| MEM-116 | Scaling plan | Scaling | AR | 3h | HIGH | 7.6.1 a 7.6.4 (4 docs) |

#### 10.10 Resumen consolidado por rol (post-reassignments, incluye iniciación)

| Rol | Tareas VTT | Tareas INIT | Total | Horas VTT | Horas INIT | Total h |
|-----|-----------:|------------:|------:|----------:|-----------:|--------:|
| PM | 7 | 5 | 12 | 16 | 5.5 | 21.5 |
| PJM | 7 | 8 | 15 | 15 | 8 | 23 |
| TL | 5 | 3 | 8 | 15 | 4 | 19 |
| SA | 8 | 0 | 8 | 40 | 0 | 40 |
| AR | 7 | 0 | 7 | 29 | 0 | 29 |
| DB | 4 | 0 | 4 | 12 | 0 | 12 |
| BE | 28 | 0 | 28 | 74 | 0 | 74 |
| DL | 11 | 0 | 11 | 28 | 0 | 28 |
| UX | 3 | 0 | 3 | 11 | 0 | 11 |
| FE | 13 | 0 | 13 | 46 | 0 | 46 |
| QA | 11 | 0 | 11 | 54 | 0 | 54 |
| DO | 12 | 8 | 20 | 33 | 14.5 | 47.5 |
| **TOTAL** | **116** | **24** | **140** | **373h** | **32h** | **~405h** |

> Diferencia con 381h de PLAN_116_TAREAS: +24h redistribución INIT + diferencias de redondeo.

---

### 11. DEPENDENCIAS POR ROL

#### 11.1 DO (DevOps)

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Admin VM: BD, volumen, SERVICE_KEY, firewall, shared-network | Antes de MEM-048 | DO coordina |
| Redis disponible con prefix `mem` | Antes de MEM-075 | DO |
| Dockerfile `COPY prisma ./prisma` | Antes de MEM-075 | DO |

#### 11.2 DB (Database)

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Verificar `@unique` en `code` de todos los catálogos | Durante MEM-048 | DB |
| `partial_indexes.sql` POST `prisma migrate deploy` | Durante MEM-049 | DB |
| Índice GIN `idx_conv_runtime_run` aplicado | Durante MEM-049 | DB |

#### 11.3 BE (Backend)

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| `initCatalogCache()` en bootstrap | MEM-051 / MEM-052 | BE |
| Usar `statusId` del cache (no `status.code`) | Todos los sprints | BE |
| Manejo P2002 en import (race condition) | MEM-053 / MEM-054 | BE |
| Catch delega siempre al cleanup (AMB-07) | MEM-053 / MEM-054 | BE |
| `contentPreview` (500 chars) · `GET /content` parsea archivo | MEM-058 | BE |

#### 11.4 DL (Design Lead)

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Design System independiente de VTT | MEM-028 | DL |
| **Design Handoff MEM-038** con UX Spec completo | Antes de MEM-081 | DL |

#### 11.5 FE (Frontend)

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| NO iniciar hasta MEM-038 `task_approved` | Antes de MEM-081 | FE |
| SERVICE_KEY vía env var (no hardcode) | MEM-085 | FE |
| Setup desktop only (sin mobile/tablet/dark en R1) | MEM-081 | FE |

#### 11.6 QA

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Tests `<500ms` para `GET /context` | MEM-061 / MEM-100 | QA |
| Tests idempotencia (ALREADY_INDEXED, P2002) | MEM-097 | QA |
| E2E Runtime (CLAUDE_SDK + platformRefs) | MEM-079 | QA |
| E2E Prompt Builder (JSON + SERVICE_KEY) | MEM-080 | QA |

#### 11.7 AR (Architect)

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Solution Architecture con C4 L1-L3 | MEM-039 | AR |
| Security Plan cubre SERVICE_KEY + OWASP | MEM-045 | AR |
| Sequence diagrams: auth, import, context, cleanup, integración | MEM-043 | AR |

---

### 12. DEPENDENCIAS CRÍTICAS (15)

| From | To | Razón | Impacto |
|------|-----|-------|---------|
| INICIACION (A-G) | MEM-006 | Proyecto debe estar configurado | 🚨 CRÍTICO |
| MEM-018..025 | MEM-039 | Analysis cerrado antes de Design Technical | Alto |
| MEM-039..047 | MEM-048 | Design Technical cerrado antes de Development | Alto |
| MEM-048..052 | MEM-053 | S02 depende de S01 | Alto |
| MEM-053..057 | MEM-058 | S03 depende de S02 | Medio |
| MEM-058..062 | MEM-063 | S04 depende de S03 | Medio |
| MEM-063..068 | MEM-069 | S05 depende de S04 | Medio |
| MEM-069..074 | MEM-075 | S06 depende de S05 | Medio |
| **MEM-038** | **MEM-081** | **HITO DL→FE** | 🚨 **CRÍTICO** |
| MEM-081..085 | MEM-086 | UI-02 depende de UI-01 | Alto |
| MEM-086..088 | MEM-089 | UI-03 depende de UI-02 | Alto |
| MEM-089..090 | MEM-091 | UI-04 depende de UI-03 | Alto |
| MEM-075..093 | MEM-094 | Testing requiere backend + UI completos | Alto |
| MEM-094..103 | MEM-104 | Deploy requiere Testing aprobado | Alto |
| MEM-104..110 | MEM-111 | Operations tras Deploy exitoso | Alto |

---

### 13. RIESGOS Y MITIGACIONES

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|--------|-------|---------|------------|
| R1 | `<500ms` no se cumple bajo carga | Media | Alto | Fail-fast (D-MEM-07) · tests MEM-061/100 · partial indexes + cache |
| R2 | Pérdida de `/storage/` | Baja | Alto | BD solo metadata · backups diarios DO · storage source of truth |
| R3 | Hook Manager no listo (MEM-078) | Media | Alto | Mock para E2E · contrato API congelado · coordinar PM+PJM+DO |
| R4 | MEM-038 atrasa y bloquea FE | Media | 🚨 Alto | DL entrega por bloques · seguimiento diario PJM · escalación PM >24h |
| R5 | Endpoint VTT de dependencias no confirmado | Media | Medio | Registro manual · PJM valida por sprint · escalación si se rompen |
| R6 | Multi-repo no definido | Media | Bajo | PM define antes de Sprint 1 · formato commit ajustable |
| R7 | SERVICE_KEY expuesta en logs/código | Baja | Alto | Middleware valida Bearer · env vars no versionadas · MEM-101 valida |
| R8 | Race P2002 en import idempotencia | Media | Bajo | Captura explícita → ALREADY_INDEXED (D-MEM-42) · test MEM-097 |
| R9 | Cleanup produce ERROR prematuro | Baja | Medio | `retryCount <= MAX_RETRIES` · STALE 10 min · LIM-10 aceptado |
| R10 | Catálogos no cargan al bootstrap | Baja | Alto | `initCatalogCache()` blocking antes de `app.listen()` |
| R11 | Admin VM no disponible para cambios | Media | Medio | DO anticipa pedidos · PM escala si bloqueo >24h |
| R12 | Plan sprints obsoleto (v2.0 52 tareas vs 116 actuales) | Alta | Medio | PJM confirma distribución temporal antes de kickoff |

---

### 14. CHECKLIST PJM ANTES DE INICIAR

```
INICIACIÓN (pre-arranque):
[ ] PM ejecuta PATCH MEM-001..005 con horas actualizadas (11h → 32h)
[ ] PM ejecuta PATCH MEM-022 → SA, MEM-039 → AR (reassignments)
[ ] PM ejecuta PATCH 116 tareas con assigneeId, complexity, category, estimatedHours
[ ] PJM confirma distribución temporal de 116 tareas en sprints
[ ] PM define naming multi-repo (formato commit con (repo))
[ ] DO coordina con Admin VM: BD + volumen + SERVICE_KEY + firewall verificados
[ ] DO completa INIT-B-02 estructura V3.1 en repo real
[ ] PM crea OPERATIVOs faltantes (10/12 roles pendientes)
[ ] DO completa INIT-C-02 tests conectividad local → VM
[ ] PM emite KICKOFF doc formal

INFRAESTRUCTURA:
[ ] BD `memory_service_db` accesible desde contenedor
[ ] Redis accesible con prefix `mem`
[ ] `shared-network` Docker con resolución DNS interna
[ ] Volumen `/storage/` con permisos correctos
[ ] SERVICE_KEY distribuida a: Runtime, Prompt Builder, Hook Manager, FE

VALIDACIÓN DE CONTRATO:
[ ] TL confirma lectura SPEC v1.9 + ADDENDUM v1.1
[ ] AR confirma Solution Architecture (MEM-039) sin bloqueos
[ ] DB confirma schema (MEM-041) aplicable con `prisma migrate deploy`
[ ] BE confirma contrato de 11 endpoints R1 sin ambigüedad
[ ] DL confirma Design System independiente de VTT

ASIGNACIÓN DE TAREAS EN VTT:
[ ] 116 tareas con assigneeId, priorityId, complexity, category, estimatedHours
[ ] Dependencias críticas registradas (15 de §12)
[ ] Deliveries (65) vinculados a tareas
[ ] Hitos marcados: MEM-038 (Design Handoff), MEM-048 (Development kickoff)

DOCUMENTOS DE REFERENCIA EN MANO:
[ ] SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md
[ ] METODOLOGIA_MEMORY_SERVICE_v1.2.md
[ ] ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md
[ ] FASES_APLICABLES_MEMORY_SERVICE.md v2.0
[ ] CONSOLIDADO_MEMORY_SERVICE_R1.md
[ ] PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md
[ ] PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md
[ ] Este documento (CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md)
[ ] PLAN_116_TAREAS.md
[ ] HO_ACTUALIZAR_TAREAS_VTT.md v2.1
```

---

### 15. CRITERIO DE ÉXITO

Memory Service R1 se considera **COMPLETADO** cuando:

1. ✅ Las **19 tablas principales** + **10 catálogos** existen en producción (schema Prisma v1.9 aplicado)
2. ✅ Seed de 10 catálogos ejecutado (`prisma db seed`)
3. ✅ Los **11 endpoints R1** responden contratos SPEC §8
4. ✅ `GET /context` responde `<500ms` en p95 o retorna `504 MEM-ERR-504`
5. ✅ Import idempotente: reimport retorna `ALREADY_INDEXED` sin error (MEM-097)
6. ✅ Import concurrente (P2002) retorna `ALREADY_INDEXED` (D-MEM-42)
7. ✅ Timeline incluye single-agent + participaciones multi-agent
8. ✅ `GET /content` parsea archivo desde `/storage/` (D-MEM-43)
9. ✅ Cost-report suma correctamente por proyecto, agente, tarea
10. ✅ Clasificación determinística detecta topics, workType, entities, files
11. ✅ Cleanup cron ejecuta cada 5 min sin producir errores en estado válido
12. ✅ Health check retorna estado BD + storage + Redis
13. ✅ UI standalone (puerto 3003) navega las 9 pantallas P0–P3
14. ✅ Hook Manager VTT puede llamar `POST /import` y `POST /import-review` con SERVICE_KEY
15. ✅ Prompt Builder v1.3 puede llamar `GET /context` con SERVICE_KEY
16. ✅ Runtime v1.1 persiste 1 conv por ronda con `externalSessionId` compuesto (D-INT-02)
17. ✅ Backward compatibility: no se rompe ningún endpoint existente en VTT
18. ✅ UAT aprobado por equipo VTT interno (MEM-102)
19. ✅ Security Testing sin findings críticos (MEM-101)
20. ✅ Performance Testing confirma SLA `<500ms` en `/context` (MEM-100)

---

### 16. HANDOFFS DOWNSTREAM (el PJM genera)

**Regla:** Los HOs se generan para el **líder de área** o para **roles con responsabilidad de decisión** (no para cada agente ejecutor). El líder distribuye el trabajo a los ejecutores de su área.

| Líder del área | Cubre |
|---------------|-------|
| TL | BE, DB, DO, FE (todo lo de código) |
| DL | UX (todo lo de diseño) |
| PM / PJM / SA / AR / QA | Cada uno por separado (roles con responsabilidad) |

**Estructura: 10 HOs secuenciales, uno por fase.** Cada HO concentra **todas las tareas de la fase** (independientemente del rol ejecutor) y es seguido por el líder que corresponda.

| # | HO | Fase | Seguimiento | Tareas | Horas | Roles activos |
|---:|----|------|-------------|-------:|------:|---------------|
| 1 | `HO_INICIACION_MEMORY_SERVICE.md` | Pre-SDLC | PJM | 24 INIT | 32h | PJM, DO, PM, TL |
| 2 | `HO_FASE_0_DISCOVERY_MEMORY_SERVICE.md` | Fase 0 Discovery | PM | 4 VTT | 9h | SA, PM |
| 3 | `HO_FASE_1_PLANNING_MEMORY_SERVICE.md` | Fase 1 Planning | PM + PJM | 8 VTT | 23h | PM, PJM, SA |
| 4 | `HO_FASE_2_ANALYSIS_MEMORY_SERVICE.md` | Fase 2 Analysis | SA | 8 VTT | 41h | SA, AR, UX |
| 5 | `HO_FASE_3A_DESIGN_UXUI_MEMORY_SERVICE.md` | Fase 3A Design UX/UI | DL | 13 VTT | 35h | UX, DL |
| 6 | `HO_FASE_3B_DESIGN_TECH_MEMORY_SERVICE.md` | Fase 3B Design Technical | TL + AR | 9 VTT | 45h | AR, TL, DB, BE, DO |
| 7 | `HO_FASE_4_DEVELOPMENT_MEMORY_SERVICE.md` | Fase 4 Development | TL | 46 VTT | 116h | DB, BE, FE, DO, QA |
| 8 | `HO_FASE_5_TESTING_MEMORY_SERVICE.md` | Fase 5 Testing | QA (bajo TL) | 10 VTT | 60h | QA, AR, DO, PM, BE |
| 9 | `HO_FASE_6_DEPLOY_MEMORY_SERVICE.md` | Fase 6 Deploy | TL + DO | 7 VTT | 26h | DO, QA, TL |
| 10 | `HO_FASE_7_OPERATIONS_MEMORY_SERVICE.md` | Fase 7 Operations | TL | 6 VTT | 15h | DO, PM, TL, AR |
| | | **TOTAL** | | **140** | **~402h** | |

Cada HO por fase contiene:
- Tareas de esa fase con descripción, rol, horas, complexity, dependencias
- Deliverables producidos por cada tarea (mapeo explícito)
- Inputs requeridos (qué debe leer cada rol antes de ejecutar)
- Criterios de aceptación por tarea
- Criterio de cierre de la fase (gate)
- Firmas: PM (emite), Líder de área (recibe), roles activos

### 16.1 INDEX / SEED de tareas

Para que el PJM o TL realicen la **carga de las 140 tareas al sistema VTT** en una sola pasada (sin repetir el análisis), existe un documento seed con todos los campos requeridos:

`TASK_INDEX_SEED_MEMORY_SERVICE.md` (140 tareas × campos del sistema: ID, título, descripción, rol, assigneeId UUID, category, complexity, estimatedHours, priorityId UUID, phaseId UUID, deliveryId UUID, dependencias, deliverables producidos).

Este seed **evita el retrabajo** que tuvimos en la primera corrida.

---

### 17. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PM** | **Martin Rivas** | **✅ APROBADO** | **2026-04-22** |
| PJM | (pendiente) | ⬜ | — |
| TL | (pendiente) | ⬜ | — |
| AR | (pendiente) | ⬜ | — |
| SA | (pendiente) | ⬜ | — |
| DB | (pendiente) | ⬜ | — |
| BE | (pendiente) | ⬜ | — |
| FE | (pendiente) | ⬜ | — |
| DL | (pendiente) | ⬜ | — |
| UX | (pendiente) | ⬜ | — |
| QA | (pendiente) | ⬜ | — |
| DO | (pendiente) | ⬜ | — |

---

**Documento:** CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md  
**Versión:** 1.0.0  
**Estado:** ✅ CERRADO — Listo para ejecución  
**Fecha:** 2026-04-22  

**Consolida:**
- PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md (24 tareas iniciación)
- FASES_APLICABLES_MEMORY_SERVICE.md v2.0 (390 deliverables aplicables)
- PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md (66 tareas implementación)
- CONSOLIDADO_MEMORY_SERVICE_R1.md (plan maestro)

**Referencias técnicas:**
- SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md (contrato técnico)
- METODOLOGIA_MEMORY_SERVICE_v1.2.md (metodología funcional)
- ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md (integración cross-service)
- PLAN_116_TAREAS.md (vista TL operativa)
- HO_ACTUALIZAR_TAREAS_VTT.md v2.1 (fuente PJM de tareas + deliveries)

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
