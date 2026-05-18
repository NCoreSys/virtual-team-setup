# HANDOFF TL: Memory Service — Sprint MEM-S01

**Documento:** HANDOFF_TL_SPRINT_MEM-S01.md  
**Versión:** 1.0  
**De:** PJM-Agent  
**Para:** TL (Tech Lead)  
**Fecha:** 2026-04-21  
**Sprint:** MEM-S01 — Schema + Seeds + Setup Proyecto  
**Estado:** 📋 READY  
**Prerrequisitos:** Infraestructura provisionada (BD, volumen storage, SERVICE_KEY en VM)

---

## 0. RESUMEN EJECUTIVO

Este es el sprint fundacional del Memory Service. Sin él, ningún sprint posterior puede ejecutarse: DB necesita el schema para crear migraciones, BE necesita el schema para generar el Prisma Client, y los catálogos de seed deben existir antes de cualquier operación de importación.

El objetivo es triple: (1) DB crea el schema Prisma completo con las 19 tablas y 10 catálogos según SPEC v1.8 §4.1, aplica las migraciones y ejecuta el seed inicial; (2) BE crea la estructura de proyecto Express + TypeScript con la configuración base y el servicio de cache de catálogos; (3) TL valida que ambas piezas encajan y el proyecto compila sin errores.

Este sprint desbloquea todo el trabajo de MEM-S02 en adelante. Sin schema + setup, no hay endpoints ni tests posibles.

**Duración total:** 9 horas  
**Distribución:** DB: 6h | BE: 3h | TL: 1h (Code Review)

---

## 1. ARQUITECTURA DEL SPRINT

### 1.1 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│              SPRINT MEM-S01: Schema + Seeds + Setup              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────┐    ┌──────────────────────────────┐    │
│  │  DB (6h)             │    │  BE (3h)                     │    │
│  │                      │    │                              │    │
│  │  MEM-DB-001          │    │  MEM-BE-001                  │    │
│  │  schema.prisma       │───▶│  Express + TS setup          │    │
│  │  19 tablas           │    │  estructura carpetas         │    │
│  │  10 catálogos        │    │                              │    │
│  │         │            │    │  MEM-BE-002                  │    │
│  │  MEM-DB-002          │    │  catalog-cache.service.ts    │    │
│  │  migrate deploy      │    │  initCatalogCache() en boot  │    │
│  │  partial_indexes.sql │    │                              │    │
│  │         │            │    └──────────────────────────────┘    │
│  │  MEM-DB-003          │                                        │
│  │  seed.ts upsert      │                                        │
│  │  10 catálogos        │                                        │
│  └──────────────────────┘                                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  TL (1h) — Code Review: schema + setup                   │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 ADRs del Sprint

**ADRs previos relevantes (todos cerrados en SPEC v1.8):**

| ADR | Decisión | Por qué aplica |
|-----|----------|----------------|
| D-MEM-05 | Idempotencia `@@unique([sourceId, externalSessionId])` | DB-001 debe incluir este constraint |
| D-MEM-10 | IDs como String (TEXT), no UUID nativo | Todos los `@id` en schema.prisma deben ser `String` |
| D-MEM-20 | Catálogos en BD, sin enums Prisma | DB-001 crea 10 modelos de catálogo, no enums |
| D-MEM-21 | Join tables para topics/entities | `ConversationTopic`, `ConversationEntity` como modelos separados |
| D-MEM-29 | `primaryAgentId` nullable en multi-agent | Campo nullable en modelo `Conversation` |
| D-MEM-31 | `startedAt`/`endedAt` del contenido parseado | Campos DateTime en Conversation, NOT defaulted |
| D-MEM-32 | `importedAt` separado de `startedAt` | Campo `importedAt DateTime @default(now())` en Conversation |
| D-MEM-38 | `primaryAgentRole` desnormalizado | Campo String? en Conversation |
| D-MEM-41 | Constraints únicos en Turn y Block | `@@unique([conversationId, turnIndex])`, `@@unique([turnId, blockIndex])` |
| D-MEM-42 | Idempotencia compuesta sourceId+externalSessionId | `@@unique([sourceId, externalSessionId])` en Conversation |
| D-MEM-43 | `contentPreview` 500 chars en BD; content completo desde `/storage/` | `contentPreview String?` en ConversationTurn — NO campo `content` completo |

> **Nota sobre D-MEM-43:** `ConversationTurn` NO tiene campo `content`. Solo `contentPreview` (primeros 500 chars). El contenido completo vive en `/storage/` y lo lee `GET /conversations/:id/content` en runtime.

### 1.3 Dependencias Externas

| Servicio | Usado para | Configuración |
|----------|-----------|---------------|
| PostgreSQL `memory_service_db` | Base de datos principal | `DATABASE_URL` en `.env` — ya provisionada en shared-postgres |
| Redis `shared-redis` | Cache futuro (MEM-S01 solo inicializa, no usa) | `REDIS_URL` en `.env` — declarar en `.env.example`, no se usa aún |
| Volume bind mount `/storage/` | Archivos de conversaciones | `STORAGE_PATH=/storage` — ya provisionado en VM |

---

## 2. ENDPOINTS A IMPLEMENTAR

> **Este sprint no implementa endpoints.** MEM-BE-001 crea la estructura del proyecto y MEM-BE-002 implementa el servicio interno de catalog cache. Los primeros endpoints llegan en MEM-S02 (MEM-BE-003: POST /api/conversations/import).

---

## 3. BRIEFS PARA AGENTES

### 3.1 Brief DB Engineer

| Tarea | Descripción | Estimado |
|-------|-------------|----------|
| MEM-DB-001 | Crear `prisma/schema.prisma` completo: 19 tablas + 10 catálogos | 3h |
| MEM-DB-002 | Ejecutar `prisma migrate deploy` + aplicar `partial_indexes.sql` manualmente | 2h |
| MEM-DB-003 | Ejecutar `prisma/seed.ts` con upsert para los 10 catálogos | 1h |

**Schema esperado — 10 modelos de catálogo:**

```
SourceCatalog          → source_catalog
ConversationTypeCatalog → conversation_type_catalog
ConversationStatusCatalog → conversation_status_catalog
WorkTypeCatalog        → work_type_catalog
BlockTypeCatalog       → block_type_catalog
MessageTypeCatalog     → message_type_catalog
MessageStatusCatalog   → message_status_catalog
PlatformCatalog        → platform_catalog
TopicCatalog           → topic_catalog
PriorityCatalog        → priority_catalog
```

**Schema esperado — 9 modelos de datos:**

```
Conversation           → conversation
ConversationTurn       → conversation_turn
TurnBlock              → turn_block
ConversationUsage      → conversation_usage
Classification         → classification
ConversationTopic      → conversation_topic
ConversationEntity     → conversation_entity
ConversationParticipant → conversation_participant
AgentMessage           → agent_message
```

> El schema completo (campo por campo) está en **SPEC v1.8 §4.1**. DB debe copiar/implementar exactamente esa definición.

**Partial indexes críticos (SQL manual en `prisma/migrations/manual/partial_indexes.sql`):**

```sql
-- Índice parcial: solo conversaciones IMPORTED para contexto <500ms
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_conv_imported_agent_project
ON conversation (primary_agent_id, project_id, started_at DESC)
WHERE status_id = (SELECT id FROM conversation_status_catalog WHERE code = 'IMPORTED');

-- Índice parcial: solo conversaciones PENDING/PROCESSING para cleanup job
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_conv_pending_created
ON conversation (created_at)
WHERE status_id IN (
  SELECT id FROM conversation_status_catalog WHERE code IN ('PENDING', 'PROCESSING')
);
```

**Seed data — 10 catálogos con upsert (ver SPEC v1.8 §5 para el código completo de `seed.ts`):**

| Catálogo | Valores |
|----------|---------|
| SourceCatalog | CLAUDE_CLI, CLAUDE_WEB, CLAUDE_SDK, CHATGPT, VTT_CHANNEL |
| ConversationTypeCatalog | TASK_EXECUTION, AGENT_REVIEW, AGENT_CLARIFICATION |
| ConversationStatusCatalog | PENDING, PROCESSING, IMPORTED, ERROR |
| WorkTypeCatalog | implementation, bug-fix, review, migration, deploy, exploration |
| BlockTypeCatalog | TEXT, TOOL_USE, TOOL_RESULT, THINKING |
| MessageTypeCatalog | REVIEW_REQUEST, REVIEW_RESPONSE, CLARIFICATION, DECISION, BLOCKER, SYSTEM_NOTE |
| MessageStatusCatalog | OPEN, ACK, IN_PROGRESS, BLOCKED, DONE, REJECTED |
| PlatformCatalog | CLAUDE_WEB, CLAUDE_CODE, CHATGPT, VTT_CHANNEL, GOOGLE_DOCS |
| TopicCatalog | (vacío en seed, se completa con datos reales de proyectos) |
| PriorityCatalog | HIGH, MEDIUM, LOW |

**Criterios de Aceptación DB:**
- [ ] CA-DB-01: `npx prisma migrate status` muestra todas las migraciones aplicadas
- [ ] CA-DB-02: `npx prisma db seed` termina sin errores
- [ ] CA-DB-03: `SELECT count(*) FROM source_catalog` retorna 5
- [ ] CA-DB-04: `SELECT count(*) FROM conversation_status_catalog` retorna 4
- [ ] CA-DB-05: Partial indexes creados — `\d conversation` en psql muestra los índices
- [ ] CA-DB-06: Constraint `@@unique([sourceId, externalSessionId])` verificado con `\d conversation`
- [ ] CA-DB-07: Archivo `prisma/schema.prisma` creado con `@@map` en todos los modelos
- [ ] CA-DB-08: Archivo `.LOGIC.md` creado para `schema.prisma` y para `seed.ts`

### 3.2 Brief Backend Engineer

| Tarea | Descripción | Estimado | Depende de |
|-------|-------------|----------|-----------|
| MEM-BE-001 | Inicializar proyecto Node.js + TypeScript + Express con estructura de carpetas | 2h | MEM-DB-001 (schema para instalar @prisma/client) |
| MEM-BE-002 | Implementar `catalog-cache.service.ts` y llamar `initCatalogCache()` en bootstrap | 1h | MEM-DB-003 (seed ejecutado) |

**Instalación de dependencias (MEM-BE-001):**

```bash
# Init proyecto
npm init -y
npm install express typescript ts-node @types/express @types/node dotenv zod
npm install @prisma/client prisma
npm install uuid dayjs multer node-cron
npm install @types/uuid @types/multer @types/node-cron -D
npm install nodemon -D

# Generar Prisma Client
npx prisma generate
```

**Archivos a crear (MEM-BE-001):**

```
memory-service/
├── package.json              (con scripts: dev, build, start, seed)
├── tsconfig.json             (target: ES2020, module: commonjs, strict: true)
├── .env.example              (todas las variables documentadas)
├── prisma/
│   └── schema.prisma         (creado por DB — BE solo ejecuta prisma generate)
├── src/
│   ├── index.ts              (entry point: llama bootstrap())
│   ├── app.ts                (bootstrap: initCatalogCache() → app.listen())
│   ├── config/
│   │   └── env.ts            (valida y exporta todas las vars de entorno)
│   ├── routes/
│   │   └── index.ts          (router vacío — se completa en S02+)
│   ├── middleware/
│   │   ├── auth.ts           (valida SERVICE_KEY header — lógica completa)
│   │   └── error-handler.ts  (middleware de error global)
│   └── services/
│       └── catalog-cache.service.ts  (MEM-BE-002)
```

**Implementación `catalog-cache.service.ts` (MEM-BE-002):**

El código completo de este servicio está en **SPEC v1.8 §3.3**. BE debe implementar exactamente esa lógica:
- `initCatalogCache()`: carga los 9 catálogos en Maps `code → id`
- `getCache()`: retorna el cache con validación (throw si no inicializado)
- Getters individuales: `getSourceId()`, `getStatusId()`, `getConversationTypeId()`, `getBlockTypeId()`, `getMessageTypeId()`, `getMessageStatusId()`, `getPriorityId()`, `getPlatformId()`

**Bootstrap en `app.ts`:**

```typescript
import { initCatalogCache } from './services/catalog-cache.service';

async function bootstrap() {
  await initCatalogCache();
  // setup express, routes, middleware...
  app.listen(PORT, () => console.log(`Memory Service running on port ${PORT}`));
}

bootstrap().catch(err => {
  console.error('Bootstrap failed:', err);
  process.exit(1);
});
```

**Criterios de Aceptación BE:**
- [ ] CA-BE-01: `npm run dev` arranca sin errores y muestra `Memory Service running on port 3002`
- [ ] CA-BE-02: `Memory Service running on port 3002` aparece seguido de `✅ Catalog cache initialized`
- [ ] CA-BE-03: `GET http://localhost:3002/health` retorna 200 (aunque sea `{ status: 'ok' }` básico)
- [ ] CA-BE-04: Archivo `src/config/env.ts` valida que `DATABASE_URL` y `SERVICE_KEY` existen — lanza error si faltan
- [ ] CA-BE-05: Archivo `.LOGIC.md` creado para `catalog-cache.service.ts`, `app.ts`, `env.ts`, `auth.ts`, `error-handler.ts`

### 3.3 Brief DevOps Engineer

> No hay tareas DO en este sprint. MEM-DO-001 (Dockerfile) llega en MEM-S06.

---

## 4. VARIABLES DE ENTORNO

| Variable | Descripción | Ejemplo | Requerida |
|----------|-------------|---------|-----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@shared-postgres:5432/memory_service_db?connection_limit=20` | ✅ |
| `SERVICE_KEY` | API key para autenticación service-to-service | `hBCG...` (ver `.env` en VM) | ✅ |
| `PORT` | Puerto del servidor | `3002` | ✅ |
| `STORAGE_PATH` | Ruta al volumen de storage | `/storage` | ✅ |
| `REDIS_URL` | Redis para rate limiting (se usa en S02+) | `redis://shared-redis:6379` | ❌ S01, ✅ S02 |
| `NODE_ENV` | Entorno de ejecución | `development` | ✅ |

**Agregar a `.env.example`:**

```bash
# Memory Service — Sprint MEM-S01
DATABASE_URL=postgresql://user:pass@localhost:5432/memory_service_db?connection_limit=20
SERVICE_KEY=your-service-key-here
PORT=3002
STORAGE_PATH=./storage
REDIS_URL=redis://localhost:6379
NODE_ENV=development
```

> **⚠️ NUNCA** hacer commit del `.env` real. El `.env` con credenciales reales ya existe en la VM en `/root/memory-service/.env`. Solo crear `.env.example` con valores de ejemplo.

---

## 5. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| `prisma migrate deploy` falla por permisos en BD | Media | Alto | Verificar que el usuario PG tiene permisos DDL en `memory_service_db` antes de empezar |
| Partial indexes `CONCURRENTLY` falla si hay lock | Baja | Medio | Ejecutar partial_indexes.sql en horario sin carga o sin `CONCURRENTLY` en dev |
| `initCatalogCache()` falla si seed no se ejecutó | Alta | Alto | DB-003 debe completarse antes de que BE arranque el servidor |
| `@prisma/client` generado con versión diferente al schema | Media | Medio | Ejecutar `npx prisma generate` después de que DB entregue el schema final |

---

## 6. TAREAS DEL SPRINT

### Fase: Desarrollo (DB primero, BE después de DB-001)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| MEM-DB-001 | Crear schema Prisma completo (19 tablas, 10 catálogos) | DB | 3h | HIGH | development |
| MEM-DB-002 | Migraciones + partial indexes (SQL manual) | DB | 2h | MEDIUM | development |
| MEM-DB-003 | Seed catálogos (sources, statuses, topics, workTypes, etc.) | DB | 1h | LOW | development |
| MEM-BE-001 | Setup proyecto Express + TypeScript + estructura carpetas | BE | 2h | MEDIUM | development |
| MEM-BE-002 | Catalog cache en startup (prefetch para evitar N+1) | BE | 1h | LOW | development |

### Fase: Validación

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| MEM-TL-001 | Code Review PRs (schema + setup) | TL | 1h | MEDIUM | review |

---

## 7. DEPENDENCIAS ENTRE TAREAS

| Tarea | Depende de | Tipo | Nota |
|-------|-----------|------|------|
| MEM-DB-002 | MEM-DB-001 | FS | Necesita schema para migrate |
| MEM-DB-003 | MEM-DB-002 | FS | Necesita tablas creadas para seed |
| MEM-BE-001 | MEM-DB-001 | FS | Necesita schema para `prisma generate` |
| MEM-BE-002 | MEM-DB-003 | FS | Necesita seed ejecutado para que initCatalogCache() no falle |
| MEM-TL-001 | MEM-BE-002 | FS | Code Review cuando todo el sprint esté integrado |

> **Tipo FS:** Finish-to-Start. La tarea no puede iniciar hasta que la anterior termine.

---

## 8. VTT PLANNING DATA

> TL: crear estas tareas en VTT usando `POST /api/phases/{PHASE_4_UUID}/tasks`.
> Phase 4 UUID: `7e003478-cd98-4953-ae79-676e864fb1f8`
> Delivery MEM-032 UUID: ver HANDOFF_PJM_SPRINT_SETUP_VTT.md §3 para el UUID exacto.

| Tarea | title | estimatedHours | complexity | category | assigneeId |
|-------|-------|---------------|-----------|----------|-----------|
| MEM-DB-001 | Crear schema Prisma completo (19 tablas, 10 catálogos) | 3 | HIGH | development | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| MEM-DB-002 | Migraciones + partial indexes (SQL manual) | 2 | MEDIUM | development | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| MEM-DB-003 | Seed catálogos (sources, statuses, topics, workTypes) | 1 | LOW | development | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| MEM-BE-001 | Setup proyecto Express + estructura carpetas | 2 | MEDIUM | development | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| MEM-BE-002 | Catalog cache en startup (prefetch para evitar N+1) | 1 | LOW | development | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| MEM-TL-001 | Code Review PRs MEM-S01 | 1 | MEDIUM | review | `92225290-6b6b-4c1f-a940-dcb4262507aa` |

**priorityId para todas:** `1a617554-6319-4c56-826f-8ef49a0ff9cc` (high)

**Nota API:** El campo `assigneeId` en POST actualmente no persiste (bug VTT conocido). Asignar vía PATCH después de crear. Ver `HO_ACTUALIZAR_TAREAS_VTT.md` para el script de actualización.

**Total TL scope este sprint:** 1h (solo MEM-TL-001 Code Review)

---

## 9. DOCUMENTOS DINÁMICOS A ACTUALIZAR

| Documento | Quién actualiza | Cuándo | Verificado en |
|-----------|----------------|--------|---------------|
| `knowledge/code-logic/prisma/schema.LOGIC.md` | DB | Al completar MEM-DB-001 | Code Review (TL) |
| `knowledge/code-logic/prisma/seed.LOGIC.md` | DB | Al completar MEM-DB-003 | Code Review (TL) |
| `knowledge/code-logic/src/services/catalog-cache.service.LOGIC.md` | BE | Al completar MEM-BE-002 | Code Review (TL) |
| `knowledge/code-logic/src/config/env.LOGIC.md` | BE | Al completar MEM-BE-001 | Code Review (TL) |
| `knowledge/code-logic/src/middleware/auth.LOGIC.md` | BE | Al completar MEM-BE-001 | Code Review (TL) |

---

## 10. DoD — TL

### Coordinación:
- [ ] Tareas MEM-DB-001, 002, 003 creadas en VTT bajo Phase 4 con assigneeId DB
- [ ] Tareas MEM-BE-001, 002 creadas en VTT bajo Phase 4 con assigneeId BE
- [ ] Tarea MEM-TL-001 creada en VTT para Code Review
- [ ] Dependencias configuradas en VTT (DB-002 depende de DB-001, etc.)
- [ ] Brief entregado a DB y BE (este documento)
- [ ] Variables de entorno documentadas en `.env.example`
- [ ] **FE bloqueado** — no participa en este sprint

### Code Review (MEM-TL-001):
- [ ] Schema Prisma tiene todos los constraints documentados en SPEC v1.8 §4.1
- [ ] D-MEM-43 cumplido: `ConversationTurn` NO tiene campo `content`, solo `contentPreview`
- [ ] D-MEM-10 cumplido: todos los `@id` son `String` con `@default(uuid())`
- [ ] D-MEM-20 cumplido: 10 modelos de catálogo, sin enums Prisma
- [ ] Partial indexes aplicados y verificables en psql
- [ ] `npm run dev` arranca y muestra `✅ Catalog cache initialized`
- [ ] Archivos `.LOGIC.md` creados por DB y BE para todos los archivos de código
- [ ] Sin `console.log` de debug (solo logs informativos)

### Validación:
- [ ] DB entregó devlog con evidencia de `prisma migrate status` y `seed` exitosos
- [ ] BE entregó devlog con evidencia de `npm run dev` funcionando
- [ ] ⚠️ **NUNCA** mover ninguna tarea a `task_approved` — ese estado es del PM/Owner

---

## 11. GATES DE APROBACIÓN

| Gate | Condición | Acción en VTT |
|------|-----------|---------------|
| DB puede arrancar | Sprint iniciado | TL notifica a DB |
| BE puede arrancar | MEM-DB-001 completado (schema listo) | TL notifica a BE |
| MEM-TL-001 puede arrancar | MEM-BE-002 completado | TL hace Code Review |
| MEM-S02 puede arrancar | MEM-TL-001 aprobado (APR-TL) | TL entrega HANDOFF_TL_SPRINT_MEM-S02.md |
| FE puede arrancar | NO en este sprint — requiere APR-DL (MEM-022) + BE endpoints `in_review` | — |

---

## 12. REFERENCIAS

| Documento | Ubicación | Para qué |
|-----------|-----------|----------|
| `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | `Release2.0/01-PM/` | Schema §4.1, Catálogos §5, Stack §3 — fuente de verdad |
| `HANDOFF_PJM_SPRINT_SETUP_VTT.md` | `Release2.0/PJM/` | UUIDs de agents, deliveries, phases para VTT |
| `HO_PJM_PLAN_SPRINTS_MEMORY_SERVICE.md` | `Release2.0/PJM/` | Plan completo de sprints, tareas por sprint |
| `HO_ACTUALIZAR_TAREAS_VTT.md` | `Release2.0/PJM/` | Script para actualizar metadata de tareas en VTT via PATCH |
| `TEMPLATE_HANDOFF_TL_V2.1.md` | `00-agent-setup/templates/Handoff_proceso/extracted/` | Template base de este documento |

---

## 13. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-04-21 | PJM-Agent | Versión inicial — Sprint fundacional MEM-S01 |

---

## RESPUESTA A PREGUNTAS DEL TL

### P1: ¿Leo 01_ONBOARDING.md + 03_FLUJO_TL.md para el proceso de descomposición?

**Sí.** Lee ambos archivos antes de iniciar cualquier sprint. Son el proceso estándar de tu rol como TL en este proyecto — definen cómo leer un handoff, cómo coordinar con DB/BE, cómo hacer Code Review, y cuándo crear las tareas FE.

### P2: ¿La descomposición la hago en VTT (POST) directamente, o primero en documento?

**Directamente en VTT.** Las tareas de este sprint ya están especificadas en la §8 (VTT Planning Data) con todos los campos. Tu trabajo es crear las tareas en VTT via `POST /api/phases/{PHASE_UUID}/tasks` y luego actualizar el `assigneeId` via PATCH (por el bug conocido en la API).

No necesitas documento intermedio — este Handoff ES el documento de planificación.

### P3: ¿Los 116 items en VTT se quedan como deliveries, o los conviertes?

**Se quedan como deliveries.** Los 116 MEM-XXX son deliverables (entregas), no tareas atómicas. Tu trabajo como TL es crear las tareas atómicas (MEM-DB-001, MEM-DB-002, etc.) dentro de la fase correcta usando `POST /api/phases/{phase_id}/tasks`. Las tareas están ya descompuestas en este Handoff (§6 y §8). No necesitas tocar los 116 deliveries existentes — esos son hitos de control del PM.

---

**FIN DEL HANDOFF TL**
