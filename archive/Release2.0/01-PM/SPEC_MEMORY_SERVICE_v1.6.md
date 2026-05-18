# ESPECIFICACIÓN TÉCNICA: Memory Service

**Versión:** 1.4  
**Fecha:** 2026-04-12  
**Autor:** PM (Martin Rivas) + Claude (Analista)  
**Estado:** REVISADO TL — LISTO PARA CONSOLIDACIÓN SA  
**Documento relacionado:** METODOLOGIA_MEMORY_SERVICE_v1.1.md

---

## CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-11 | Documento inicial |
| 1.1 | 2026-04-11 | GAPs resueltos por DevOps: storage volume, SERVICE_KEY, connection_limit |
| 1.2 | 2026-04-11 | Agregada sección 16: UI Standalone |
| 1.3 | 2026-04-12 | **Revisión AR — 7 bloqueos resueltos:** B-01 multi-agente, B-02 GET /context, B-03 flujo PROCESSING + cleanup, B-04 temporalidad, B-05 contratos completos, B-06 auth por endpoint, B-07 Q-01/Q-05 cerradas |
| 1.4 | 2026-04-12 | **Correcciones AR:** primaryAgentRole, GET /context filtra projectId, cleanup job lógica, constraints únicos, idempotencia compuesta. **Consistencia interna:** importAgentReview idempotencia, D-MEM-05/06 alineadas. **Revisión TL:** D-MEM-43 (AMB-01 cerrada), constraint ConversationEntity, NOTA-SA-01 a NOTA-SA-05 para consolidación SA |

---

## ÍNDICE

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Decisiones Cerradas](#2-decisiones-cerradas)
3. [Stack Tecnológico](#3-stack-tecnológico)
4. [Modelo de Datos](#4-modelo-de-datos)
5. [Catálogos (Seed Data)](#5-catálogos-seed-data)
6. [Índices de Base de Datos](#6-índices-de-base-de-datos)
7. [Autenticación por Endpoint](#7-autenticación-por-endpoint)
8. [API Endpoints — Contratos Completos](#8-api-endpoints--contratos-completos)
9. [Flujos de Importación](#9-flujos-de-importación)
10. [Atomicidad y Recovery](#10-atomicidad-y-recovery)
11. [Servicio de Contexto Runtime](#11-servicio-de-contexto-runtime)
12. [Clasificación por Reglas](#12-clasificación-por-reglas)
13. [Almacenamiento de Archivos](#13-almacenamiento-de-archivos)
14. [Plan de Implementación](#14-plan-de-implementación)
15. [Criterios de Aceptación](#15-criterios-de-aceptación)
16. [Docker-Compose (Producción)](#16-docker-compose-producción)
17. [UI Standalone](#17-ui-standalone)

---

## 1. RESUMEN EJECUTIVO

### 1.1 Objetivo

Implementar el Memory Service como sistema independiente de memoria centralizada para agentes de IA, con capacidad de:

- Importar conversaciones de 5 fuentes (CLI, Web, SDK, ChatGPT, VTT_CHANNEL)
- Clasificar automáticamente por reglas determinísticas
- Proveer contexto runtime en <500ms (síncrono, fail-fast)
- Exponer timeline y métricas de costo
- Soportar conversaciones single-agent (TASK_EXECUTION) y multi-agent (AGENT_REVIEW, AGENT_CLARIFICATION)

### 1.2 Alcance R1

| Componente | Descripción |
|------------|-------------|
| **Import** | POST /import (JSONL), POST /import-review (VTT_CHANNEL), POST /upload (manual) |
| **Timeline** | GET /agents/:id/timeline |
| **Contenido** | GET /conversations/:id/content |
| **Contexto** | GET /context (<500ms, síncrono) |
| **Costos** | GET /projects/:id/cost-report, GET /agents/:id/cost-report |
| **Lista/Búsqueda** | GET /conversations (con filtros para UI) |
| **Dashboard** | GET /dashboard/stats |
| **Health** | GET /health |
| **UI** | SPA standalone puerto 3003 |

### 1.3 Stack

| Componente | Tecnología |
|------------|------------|
| Runtime | Node.js 20 + TypeScript |
| Framework | Express |
| ORM | Prisma |
| Base de datos | PostgreSQL `memory_service_db` en shared-postgres |
| Cache/Rate Limit | Redis `shared-redis` (prefix: `mem`) |
| Storage archivos | Volumen Docker bind mount → `/root/memory-service-storage/` |
| Puerto API | 3002 |
| Puerto UI | 3003 |
| Red Docker | `shared-network` |
| Path VM | `/root/memory-service/` |

### 1.4 Infraestructura Provisionada

| Recurso | Estado | Detalle |
|---------|--------|---------|
| BD `memory_service_db` | ✅ Creada | En shared-postgres |
| Volumen storage | ✅ Creado | `/root/memory-service-storage/` → `/storage/` en container |
| SERVICE_KEY | ✅ Generada | En `/root/memory-service/.env` |
| docker-compose.yml | ✅ Listo | Con `connection_limit=20`, `mem_limit: 512m` |
| Código backend | ⏳ Pendiente | Deploy cuando se implemente |

---

## 2. DECISIONES CERRADAS

### 2.1 Decisiones de Arquitectura (D-MEM-01 a D-MEM-28)

| ID | Tema | Decisión | Justificación |
|----|------|----------|---------------|
| **D-MEM-01** | Arquitectura | Sistema independiente | Reutilizable, resiliente, escalable |
| **D-MEM-02** | VTM legacy | Descartar | Diseño incompatible |
| **D-MEM-03** | Transporte archivos | Multipart a VM | No acceso a filesystem remoto |
| **D-MEM-04** | SDK files | 2 archivos (session + log) | Costo en log, no session |
| **D-MEM-05** | Duplicados | Idempotencia compuesta `sourceId + externalSessionId` | Robusto cross-source (ver D-MEM-42) |
| **D-MEM-06** | Storage path | TASK_EXECUTION: `/storage/{primaryAgentId}/{YYYY-MM}/{sessionId}/`; AGENT_REVIEW: `/storage/_reviews/{projectId}/{YYYY-MM}/{sessionId}/` | Paths diferenciados por tipo |
| **D-MEM-07** | Contexto | <500ms obligatorio, síncrono, fail-fast | No cuello de botella |
| **D-MEM-08** | Clasificación | Reglas determinísticas | Simple, predecible, sin costo |
| **D-MEM-09** | Fuentes | Catálogo extensible | Sin migración para agregar |
| **D-MEM-10** | IDs | String (TEXT) | Consistente con VTT |
| **D-MEM-11** | taskId | Task.id (UUID) + taskKey | FK real + código legible |
| **D-MEM-12** | taskTitle | Desnormalizado | No llamar a VTT en runtime |
| **D-MEM-13** | Status flow | PENDING → PROCESSING → IMPORTED/ERROR | Atomicidad por compensación |
| **D-MEM-14** | Endpoints | Separados JSONL vs VTT_CHANNEL | Payloads incompatibles |
| **D-MEM-15** | conversationType | Discriminador | 1 agente vs N agentes |
| **D-MEM-16** | VTT_CHANNEL | Import incremental | Docs append-only |
| **D-MEM-17** | platformRefs | JSON nullable | Cross-platform linking |
| **D-MEM-18** | JSONL | Sin stripping | BD solo metadata |
| **D-MEM-19** | Entregables | Hook Manager responsable | Memory Service no participa |
| **D-MEM-20** | Tipos | Catálogos en BD | Sin enums Prisma |
| **D-MEM-21** | topics/entities | Join tables | Relacional, no arrays |
| **D-MEM-22** | Store rate limit | Memory (dev) → Redis (prod) | Escalabilidad futura |
| **D-MEM-23** | Redis prefix | `mem` | Consistente con INFRASTRUCTURE_GUIDE |
| **D-MEM-24** | BD name | `memory_service_db` | Convención `{app}_db` |
| **D-MEM-25** | Storage | Volumen bind mount | Filesystem para R1, MinIO en R2 |
| **D-MEM-26** | Auth service-to-service | SERVICE_KEY pattern | Consistencia con VTT |
| **D-MEM-27** | Connection limit | 20 conexiones | Límite infraestructura |
| **D-MEM-28** | RAM limit | 512MB max, 256MB reserved | Límite VM compartida |

### 2.2 Decisiones Revisión AR v1.3 (D-MEM-29 a D-MEM-37)

| ID | Tema | Decisión | Justificación |
|----|------|----------|---------------|
| **D-MEM-29** | Multi-agente | `primaryAgentId` nullable; para AGENT_REVIEW es NULL, participantes en ConversationParticipant | Soporta 1 agente y N agentes |
| **D-MEM-30** | PlatformCatalog | Agregar VTT_CHANNEL y GOOGLE_DOCS | Cobertura completa de plataformas |
| **D-MEM-31** | Temporalidad | `startedAt`/`endedAt` del contenido parseado, no de import; storage usa fecha real | Timeline y reportes correctos |
| **D-MEM-32** | importedAt | Nuevo campo para auditoría de cuándo se importó | Separar fecha sesión vs fecha import |
| **D-MEM-33** | GET /context | Usa projectId/taskId en queries; sin campo summary | Contrato consistente con implementación |
| **D-MEM-34** | Estado PROCESSING | Usar explícitamente antes de escribir archivo | Flujo completo PENDING→PROCESSING→IMPORTED/ERROR |
| **D-MEM-35** | Cleanup job | Cron cada 5 min: PENDING/PROCESSING > 10 min → retry o ERROR | Recovery automático |
| **D-MEM-36** | agentId | = User.id de VTT; Memory Service NO tiene catálogo propio | Q-01 cerrada |
| **D-MEM-37** | GET /context modo | Siempre síncrono <500ms; si no cumple, fail-fast | Q-05 cerrada |

### 2.3 Decisiones Corrección AR v1.4 (D-MEM-38 a D-MEM-42)

| ID | Tema | Decisión | Justificación |
|----|------|----------|---------------|
| **D-MEM-38** | primaryAgentRole | Desnormalizado en import (Hook Manager envía rol) | Cost-report necesita rol sin consultar VTT |
| **D-MEM-39** | GET /context scope | Todas las queries filtran por projectId | Evitar contaminar contexto con otros proyectos |
| **D-MEM-40** | Cleanup job query | `retryCount <= MAX_RETRIES` para incluir límite | Lógica correcta para marcar ERROR definitivo |
| **D-MEM-41** | Constraints únicos | `@@unique([conversationId, turnIndex])` en Turn, `@@unique([turnId, blockIndex])` en Block | Evitar duplicados en import/reproceso |
| **D-MEM-42** | Idempotencia | Unicidad compuesta `@@unique([sourceId, externalSessionId])` | Robusto cross-source sin asumir namespacing |

### 2.4 Decisión Revisión TL v1.4 (D-MEM-43)

| ID | Tema | Decisión | Justificación |
|----|------|----------|---------------|
| **D-MEM-43** | Contenido completo (AMB-01) | `contentPreview` en BD solo primeros 500 chars; `GET /content` lee desde `/storage/` | BD ligera, storage tiene fuente de verdad |

**Resolución AMB-01:** El contenido completo de los turns NO se persiste en la tabla `ConversationTurn`. Solo se guarda `contentPreview` (primeros 500 caracteres) para búsquedas rápidas y previews en UI. El endpoint `GET /conversations/:id/content` lee el archivo completo desde `/storage/` y parsea los turns en runtime.

---

## 2.5 NOTAS PARA CONSOLIDACIÓN SA

Los siguientes puntos quedaron pendientes de validación TL y deben consolidarse en la spec final:

### NOTA-SA-01: Constraint ConversationEntity

Agregar constraint único compuesto en `ConversationEntity`:

```prisma
model ConversationEntity {
  // ... campos existentes ...
  
  @@unique([conversationId, entityName])  // Evitar duplicados de entidad por conversación
  @@index([conversationId])
  @@map("conversation_entity")
}
```

### NOTA-SA-02: Partial Indexes

Prisma no soporta nativamente partial indexes con cláusula `WHERE`. Los índices parciales definidos en sección 6 deben implementarse como **migración SQL manual**:

```sql
-- Ejecutar post-migración Prisma
CREATE INDEX idx_conv_agent_time ON conversation(primary_agent_id, started_at DESC) 
  WHERE primary_agent_id IS NOT NULL;

CREATE INDEX idx_conv_task ON conversation(task_id) 
  WHERE task_id IS NOT NULL;

CREATE INDEX idx_block_filepath ON turn_block(file_path) 
  WHERE file_path IS NOT NULL;
```

Documentar en `prisma/migrations/manual/partial_indexes.sql`.

### NOTA-SA-03: Manejo P2002 en Import

En caso de race condition donde dos imports concurrentes intentan crear la misma conversación, Prisma lanza error `P2002` (unique constraint violation). El catch del import debe manejar esto como idempotencia:

```typescript
} catch (error) {
  // Race condition: otro proceso ya insertó esta conversación
  if (error.code === 'P2002') {
    const existing = await prisma.conversation.findUnique({
      where: {
        sourceId_externalSessionId: { sourceId, externalSessionId },
      },
    });
    if (existing) {
      return { conversationId: existing.id, status: 'ALREADY_INDEXED' };
    }
  }
  // Otro error: queda en PROCESSING para cleanup job
  console.error('Import failed:', error);
  throw error;
}
```

### NOTA-SA-04: Cache de Catálogos en Startup

Para evitar lookups repetidos en `GET /context` y cleanup job, cargar catálogos en memoria al iniciar el servicio:

```typescript
// services/catalog-cache.service.ts
interface CatalogCache {
  sources: Map<string, string>;      // code -> id
  types: Map<string, string>;        // code -> id
  statuses: Map<string, string>;     // code -> id
  // ... otros catálogos
}

let cache: CatalogCache;

export async function initCatalogCache(): Promise<void> {
  const [sources, types, statuses] = await Promise.all([
    prisma.sourceCatalog.findMany(),
    prisma.conversationTypeCatalog.findMany(),
    prisma.conversationStatusCatalog.findMany(),
  ]);
  
  cache = {
    sources: new Map(sources.map(s => [s.code, s.id])),
    types: new Map(types.map(t => [t.code, t.id])),
    statuses: new Map(statuses.map(s => [s.code, s.id])),
  };
}

export function getSourceId(code: string): string {
  const id = cache.sources.get(code);
  if (!id) throw new Error(`Unknown source: ${code}`);
  return id;
}
// ... getters similares
```

Llamar `initCatalogCache()` en `app.ts` antes de levantar el servidor.

### NOTA-SA-05: Cleanup Job — Solo Cambio de Estado

El cleanup job (sección 10.2) **solo cambia estados** (PENDING/PROCESSING → retry o ERROR). El **reproceso real** (re-leer archivo, re-parsear, persistir turns) queda fuera de alcance R1 y se implementará en Sprint S04.

Por ahora, si una conversación queda en PENDING después de max retries:
1. Se marca como ERROR con `errorMessage`
2. Aparece en `GET /dashboard/stats` → `errorsToReview`
3. El operador puede investigar manualmente y re-importar si es necesario

---

## 3. STACK TECNOLÓGICO

### 3.1 Dependencias Principales

```bash
# Core
npm install express typescript ts-node
npm install @prisma/client prisma
npm install dotenv zod

# Multipart upload
npm install multer
npm install @types/multer -D

# Utilidades
npm install uuid dayjs
npm install @types/uuid -D

# Cron para cleanup job
npm install node-cron
npm install @types/node-cron -D

# Development
npm install nodemon -D
npm install @types/express @types/node -D
```

### 3.2 Estructura de Proyecto

```
memory-service/
├── prisma/
│   ├── schema.prisma
│   ├── seed.ts
│   └── migrations/
├── src/
│   ├── index.ts
│   ├── app.ts
│   ├── config/
│   │   └── env.ts
│   ├── routes/
│   │   ├── index.ts
│   │   ├── conversations.routes.ts
│   │   ├── agents.routes.ts
│   │   ├── projects.routes.ts
│   │   ├── context.routes.ts
│   │   ├── dashboard.routes.ts
│   │   └── health.routes.ts
│   ├── controllers/
│   ├── services/
│   │   ├── importer.service.ts
│   │   ├── storage.service.ts
│   │   ├── classifier.service.ts
│   │   ├── context.service.ts
│   │   ├── cleanup.service.ts
│   │   └── adapters/
│   │       ├── cli.adapter.ts
│   │       ├── web.adapter.ts
│   │       ├── sdk.adapter.ts
│   │       ├── chatgpt.adapter.ts
│   │       └── vtt-channel.adapter.ts
│   ├── middleware/
│   │   ├── error-handler.ts
│   │   ├── validate.ts
│   │   └── auth.ts
│   ├── jobs/
│   │   └── cleanup.job.ts
│   ├── schemas/
│   └── utils/
├── storage/              # Volumen Docker mapeado
├── .env
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── package.json
```

---

## 4. MODELO DE DATOS

### 4.1 Schema Prisma

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ============================================================
// CATÁLOGOS
// ============================================================

model SourceCatalog {
  id           String         @id @default(uuid())
  code         String         @unique // CLAUDE_CLI, CLAUDE_WEB, CLAUDE_SDK, CHATGPT, VTT_CHANNEL
  label        String
  createdAt    DateTime       @default(now())
  conversations Conversation[]

  @@map("source_catalog")
}

model ConversationTypeCatalog {
  id           String         @id @default(uuid())
  code         String         @unique // TASK_EXECUTION, AGENT_REVIEW, AGENT_CLARIFICATION
  label        String
  createdAt    DateTime       @default(now())
  conversations Conversation[]

  @@map("conversation_type_catalog")
}

model ConversationStatusCatalog {
  id           String         @id @default(uuid())
  code         String         @unique // PENDING, PROCESSING, IMPORTED, ERROR
  label        String
  createdAt    DateTime       @default(now())
  conversations Conversation[]

  @@map("conversation_status_catalog")
}

model WorkTypeCatalog {
  id             String           @id @default(uuid())
  code           String           @unique // implementation, bug-fix, review, migration, deploy, exploration
  label          String
  createdAt      DateTime         @default(now())
  classifications Classification[]

  @@map("work_type_catalog")
}

model BlockTypeCatalog {
  id        String      @id @default(uuid())
  code      String      @unique // TEXT, TOOL_USE, TOOL_RESULT, THINKING
  label     String
  createdAt DateTime    @default(now())
  blocks    TurnBlock[]

  @@map("block_type_catalog")
}

model MessageTypeCatalog {
  id        String         @id @default(uuid())
  code      String         @unique // REVIEW_REQUEST, REVIEW_RESPONSE, CLARIFICATION, DECISION, BLOCKER, SYSTEM_NOTE
  label     String
  createdAt DateTime       @default(now())
  messages  AgentMessage[]

  @@map("message_type_catalog")
}

model MessageStatusCatalog {
  id        String         @id @default(uuid())
  code      String         @unique // OPEN, ACK, IN_PROGRESS, BLOCKED, DONE, REJECTED
  label     String
  createdAt DateTime       @default(now())
  messages  AgentMessage[]

  @@map("message_status_catalog")
}

model PlatformCatalog {
  id           String                    @id @default(uuid())
  code         String                    @unique // CLAUDE_WEB, CLAUDE_CODE, CHATGPT, VTT_CHANNEL, GOOGLE_DOCS
  label        String
  createdAt    DateTime                  @default(now())
  participants ConversationParticipant[]

  @@map("platform_catalog")
}

model TopicCatalog {
  id           String              @id @default(uuid())
  code         String              @unique
  label        String
  category     String?
  createdAt    DateTime            @default(now())
  conversations ConversationTopic[]

  @@map("topic_catalog")
}

model PriorityCatalog {
  id        String         @id @default(uuid())
  code      String         @unique // HIGH, MEDIUM, LOW
  label     String
  createdAt DateTime       @default(now())
  messages  AgentMessage[]

  @@map("priority_catalog")
}

// ============================================================
// ENTIDADES PRINCIPALES
// ============================================================

model Conversation {
  id                String   @id @default(uuid())
  
  // Referencias a catálogos
  sourceId          String
  source            SourceCatalog @relation(fields: [sourceId], references: [id])
  
  conversationTypeId String
  conversationType   ConversationTypeCatalog @relation(fields: [conversationTypeId], references: [id])
  
  statusId          String
  status            ConversationStatusCatalog @relation(fields: [statusId], references: [id])
  
  // Idempotencia: único por fuente + sessionId externo
  externalSessionId String   // ID de sesión en origen (único dentro de cada source)
  
  // Referencias a VTT (String, no UUID)
  // Para TASK_EXECUTION: primaryAgentId/Role = el agente que ejecutó
  // Para AGENT_REVIEW/CLARIFICATION: primaryAgentId = NULL, participantes en ConversationParticipant
  primaryAgentId    String?  // VTT User.id — NULLABLE para multi-agent
  primaryAgentRole  String?  // BE-Agent, DB-Agent, etc. — Desnormalizado desde import
  projectId         String   // VTT Project.id
  taskId            String?  // VTT Task.id (nullable)
  taskKey           String?  // VTT-123 (auxiliar, legible)
  taskTitle         String?  // Desnormalizado, enviado en import
  
  // Multi-plataforma
  platformRefs      Json?    // { claude_web: "...", claude_code: "..." }
  
  // Solo para AGENT_REVIEW
  reviewRound       Int?
  outputFilePath    String?  // Documento generado
  
  // Timestamps — DE LA SESIÓN REAL, no del import
  startedAt         DateTime  // Fecha/hora inicio de la sesión original
  endedAt           DateTime? // Fecha/hora fin de la sesión original
  
  // Auditoría
  importedAt        DateTime @default(now()) // Cuándo se importó a Memory Service
  
  // Métricas
  turnCount         Int      @default(0)
  
  // Storage
  filePath          String?  // Ruta en /storage/
  logFilePath       String?  // Solo SDK
  
  // Error info (cuando status = ERROR)
  errorMessage      String?
  retryCount        Int      @default(0)
  
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt
  
  // Relaciones
  turns             ConversationTurn[]
  usage             ConversationUsage?
  classification    Classification?
  topics            ConversationTopic[]
  entities          ConversationEntity[]
  participants      ConversationParticipant[]
  messages          AgentMessage[]

  // Constraint de idempotencia: único por sourceId + externalSessionId
  @@unique([sourceId, externalSessionId])
  
  // Índices para queries frecuentes
  @@index([primaryAgentId, startedAt(sort: Desc)])
  @@index([projectId, startedAt(sort: Desc)])
  @@index([conversationTypeId, startedAt(sort: Desc)])
  @@index([statusId])
  @@index([taskId])
  @@map("conversation")
}

model ConversationTurn {
  id             String   @id @default(uuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  turnIndex      Int
  role           String   // USER, ASSISTANT, SYSTEM
  timestamp      DateTime?
  contentPreview String?  // Primeros 500 chars
  
  blocks         TurnBlock[]

  // Constraint: evitar duplicados en import/reproceso
  @@unique([conversationId, turnIndex])
  @@index([conversationId])
  @@map("conversation_turn")
}

model TurnBlock {
  id          String   @id @default(uuid())
  turnId      String
  turn        ConversationTurn @relation(fields: [turnId], references: [id], onDelete: Cascade)
  
  blockIndex  Int
  
  blockTypeId String
  blockType   BlockTypeCatalog @relation(fields: [blockTypeId], references: [id])
  
  toolName    String?  // Read, Edit, Write, Bash, etc.
  filePath    String?  // Archivo tocado
  success     Boolean? // Para TOOL_RESULT
  contentLength Int?

  // Constraint: evitar duplicados en import/reproceso
  @@unique([turnId, blockIndex])
  @@index([filePath])
  @@map("turn_block")
}

model ConversationUsage {
  id                  String   @id @default(uuid())
  conversationId      String   @unique
  conversation        Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  inputTokens         Int
  outputTokens        Int
  cacheCreationTokens Int      @default(0)
  cacheReadTokens     Int      @default(0)
  costUsd             Decimal  @db.Decimal(10, 6)
  durationMs          Int?
  modelId             String?
  isError             Boolean  @default(false)

  @@map("conversation_usage")
}

model Classification {
  id             String   @id @default(uuid())
  conversationId String   @unique
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  workTypeId     String?
  workType       WorkTypeCatalog? @relation(fields: [workTypeId], references: [id])
  
  confidence     Float    @default(0)
  classifiedAt   DateTime @default(now())
  classifiedBy   String   @default("rules-v1")

  @@map("classification")
}

model ConversationTopic {
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  topicId        String
  topic          TopicCatalog @relation(fields: [topicId], references: [id])

  @@id([conversationId, topicId])
  @@index([conversationId])
  @@map("conversation_topic")
}

model ConversationEntity {
  id             String   @id @default(uuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  entityName     String

  // Constraint: evitar duplicados de entidad por conversación
  @@unique([conversationId, entityName])
  @@index([conversationId])
  @@map("conversation_entity")
}

// Solo para AGENT_REVIEW / AGENT_CLARIFICATION
model ConversationParticipant {
  id             String   @id @default(uuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  agentId        String   // VTT User.id
  agentRole      String   // PM_REVISOR, AR, TL, DB, SA, etc.
  
  platformId     String?  // Nullable — puede no saberse la plataforma
  platform       PlatformCatalog? @relation(fields: [platformId], references: [id])

  @@unique([conversationId, agentId])
  @@index([agentId])
  @@map("conversation_participant")
}

// Solo para VTT_CHANNEL
model AgentMessage {
  id             String   @id @default(uuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  messageId      String   // AR-001, PM-002, etc.
  inReplyTo      String?  // messageId referenciado
  
  fromAgentId    String   // VTT User.id
  toAgentId      String   // VTT User.id
  
  messageTypeId  String
  messageType    MessageTypeCatalog @relation(fields: [messageTypeId], references: [id])
  
  messageStatusId String
  messageStatus   MessageStatusCatalog @relation(fields: [messageStatusId], references: [id])
  
  priorityId     String
  priority       PriorityCatalog @relation(fields: [priorityId], references: [id])
  
  topic          String?
  body           String
  expectedOutput String?
  timestamp      DateTime

  @@unique([conversationId, messageId])
  @@index([conversationId, messageStatusId])
  @@map("agent_message")
}
```

---

## 5. CATÁLOGOS (SEED DATA)

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // SourceCatalog
  const sources = [
    { code: 'CLAUDE_CLI', label: 'Claude CLI (Claude Code)' },
    { code: 'CLAUDE_WEB', label: 'Claude Web (claude.ai)' },
    { code: 'CLAUDE_SDK', label: 'Claude Agent SDK' },
    { code: 'CHATGPT', label: 'ChatGPT Export' },
    { code: 'VTT_CHANNEL', label: 'VTT Channel (Multi-Agent)' },
  ];
  for (const s of sources) {
    await prisma.sourceCatalog.upsert({
      where: { code: s.code },
      update: {},
      create: s,
    });
  }

  // ConversationTypeCatalog
  const types = [
    { code: 'TASK_EXECUTION', label: 'Task Execution (Single Agent)' },
    { code: 'AGENT_REVIEW', label: 'Agent Review (Multi-Agent)' },
    { code: 'AGENT_CLARIFICATION', label: 'Agent Clarification' },
  ];
  for (const t of types) {
    await prisma.conversationTypeCatalog.upsert({
      where: { code: t.code },
      update: {},
      create: t,
    });
  }

  // ConversationStatusCatalog
  const statuses = [
    { code: 'PENDING', label: 'Pending (awaiting processing)' },
    { code: 'PROCESSING', label: 'Processing (writing files)' },
    { code: 'IMPORTED', label: 'Imported successfully' },
    { code: 'ERROR', label: 'Error during import' },
  ];
  for (const s of statuses) {
    await prisma.conversationStatusCatalog.upsert({
      where: { code: s.code },
      update: {},
      create: s,
    });
  }

  // WorkTypeCatalog
  const workTypes = [
    { code: 'implementation', label: 'Implementation' },
    { code: 'bug-fix', label: 'Bug Fix' },
    { code: 'review', label: 'Code Review' },
    { code: 'migration', label: 'Migration' },
    { code: 'deploy', label: 'Deployment' },
    { code: 'exploration', label: 'Exploration / Research' },
  ];
  for (const w of workTypes) {
    await prisma.workTypeCatalog.upsert({
      where: { code: w.code },
      update: {},
      create: w,
    });
  }

  // BlockTypeCatalog
  const blockTypes = [
    { code: 'TEXT', label: 'Text' },
    { code: 'TOOL_USE', label: 'Tool Use' },
    { code: 'TOOL_RESULT', label: 'Tool Result' },
    { code: 'THINKING', label: 'Thinking' },
  ];
  for (const b of blockTypes) {
    await prisma.blockTypeCatalog.upsert({
      where: { code: b.code },
      update: {},
      create: b,
    });
  }

  // MessageTypeCatalog
  const messageTypes = [
    { code: 'REVIEW_REQUEST', label: 'Review Request' },
    { code: 'REVIEW_RESPONSE', label: 'Review Response' },
    { code: 'CLARIFICATION', label: 'Clarification' },
    { code: 'DECISION', label: 'Decision' },
    { code: 'BLOCKER', label: 'Blocker' },
    { code: 'SYSTEM_NOTE', label: 'System Note' },
  ];
  for (const m of messageTypes) {
    await prisma.messageTypeCatalog.upsert({
      where: { code: m.code },
      update: {},
      create: m,
    });
  }

  // MessageStatusCatalog
  const messageStatuses = [
    { code: 'OPEN', label: 'Open' },
    { code: 'ACK', label: 'Acknowledged' },
    { code: 'IN_PROGRESS', label: 'In Progress' },
    { code: 'BLOCKED', label: 'Blocked' },
    { code: 'DONE', label: 'Done' },
    { code: 'REJECTED', label: 'Rejected' },
  ];
  for (const m of messageStatuses) {
    await prisma.messageStatusCatalog.upsert({
      where: { code: m.code },
      update: {},
      create: m,
    });
  }

  // PlatformCatalog — EXTENDIDO con VTT_CHANNEL y GOOGLE_DOCS
  const platforms = [
    { code: 'CLAUDE_WEB', label: 'Claude Web' },
    { code: 'CLAUDE_CODE', label: 'Claude Code' },
    { code: 'CHATGPT', label: 'ChatGPT' },
    { code: 'VTT_CHANNEL', label: 'VTT Channel' },
    { code: 'GOOGLE_DOCS', label: 'Google Docs' },
  ];
  for (const p of platforms) {
    await prisma.platformCatalog.upsert({
      where: { code: p.code },
      update: {},
      create: p,
    });
  }

  // TopicCatalog
  const topics = [
    { code: 'authentication', label: 'Authentication', category: 'security' },
    { code: 'authorization', label: 'Authorization', category: 'security' },
    { code: 'database', label: 'Database', category: 'backend' },
    { code: 'prisma', label: 'Prisma ORM', category: 'backend' },
    { code: 'api', label: 'API', category: 'backend' },
    { code: 'frontend', label: 'Frontend', category: 'frontend' },
    { code: 'ui', label: 'UI Components', category: 'frontend' },
    { code: 'testing', label: 'Testing', category: 'quality' },
    { code: 'migration', label: 'Migration', category: 'devops' },
    { code: 'docker', label: 'Docker', category: 'devops' },
  ];
  for (const t of topics) {
    await prisma.topicCatalog.upsert({
      where: { code: t.code },
      update: {},
      create: t,
    });
  }

  // PriorityCatalog
  const priorities = [
    { code: 'HIGH', label: 'High' },
    { code: 'MEDIUM', label: 'Medium' },
    { code: 'LOW', label: 'Low' },
  ];
  for (const p of priorities) {
    await prisma.priorityCatalog.upsert({
      where: { code: p.code },
      update: {},
      create: p,
    });
  }

  console.log('✅ Seed completed');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

---

## 6. ÍNDICES DE BASE DE DATOS

```sql
-- Idempotencia: único por sourceId + externalSessionId (Prisma genera automáticamente)
-- CREATE UNIQUE INDEX idx_conv_source_external ON conversation(source_id, external_session_id);

-- Timeline por agente (single-agent)
CREATE INDEX idx_conv_agent_time ON conversation(primary_agent_id, started_at DESC) 
  WHERE primary_agent_id IS NOT NULL;

-- Timeline por proyecto
CREATE INDEX idx_conv_project_time ON conversation(project_id, started_at DESC);

-- Por tipo de conversación
CREATE INDEX idx_conv_type ON conversation(conversation_type_id, started_at DESC);

-- Por status (para cleanup job)
CREATE INDEX idx_conv_status ON conversation(status_id, updated_at);

-- Por tarea
CREATE INDEX idx_conv_task ON conversation(task_id) WHERE task_id IS NOT NULL;

-- Constraints de integridad (Prisma genera automáticamente)
-- CREATE UNIQUE INDEX idx_turn_conv_index ON conversation_turn(conversation_id, turn_index);
-- CREATE UNIQUE INDEX idx_block_turn_index ON turn_block(turn_id, block_index);

-- Archivos tocados
CREATE INDEX idx_block_filepath ON turn_block(file_path) WHERE file_path IS NOT NULL;

-- Mensajes por conversación
CREATE INDEX idx_message_conv ON agent_message(conversation_id, message_status_id);

-- Participantes por agente (para timeline multi-agent)
CREATE INDEX idx_participant_agent ON conversation_participant(agent_id);

-- Participantes por conversación
CREATE INDEX idx_participant_conv ON conversation_participant(conversation_id);

-- Topics por conversación
CREATE INDEX idx_topic_conv ON conversation_topic(conversation_id);
```

---

## 7. AUTENTICACIÓN POR ENDPOINT

### 7.1 Política de Auth R1

| Endpoint | Auth | Consumidor | Middleware |
|----------|------|------------|------------|
| `POST /api/conversations/import` | SERVICE_KEY | Hook Manager | `requireServiceKey` |
| `POST /api/conversations/import-review` | SERVICE_KEY | Hook Manager | `requireServiceKey` |
| `GET /api/context` | SERVICE_KEY | Hook Manager | `requireServiceKey` |
| `POST /api/conversations/upload` | Público R1 | UI | ninguno |
| `GET /api/agents/*` | Público R1 | UI | ninguno |
| `GET /api/conversations` | Público R1 | UI | ninguno |
| `GET /api/conversations/:id/content` | Público R1 | UI | ninguno |
| `GET /api/projects/:id/cost-report` | Público R1 | UI | ninguno |
| `GET /api/dashboard/stats` | Público R1 | UI | ninguno |
| `GET /api/health` | Público | UI, monitoring | ninguno |

### 7.2 Middleware requireServiceKey

```typescript
// middleware/auth.ts
import { Request, Response, NextFunction } from 'express';

const SERVICE_KEY = process.env.SERVICE_KEY;

export function requireServiceKey(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      error: 'Missing or invalid Authorization header',
      code: 'MEM-ERR-401',
    });
  }
  
  const token = authHeader.substring(7);
  
  if (token !== SERVICE_KEY) {
    return res.status(403).json({
      error: 'Invalid service key',
      code: 'MEM-ERR-403',
    });
  }
  
  next();
}
```

---

## 8. API ENDPOINTS — CONTRATOS COMPLETOS

### 8.1 Resumen

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `POST` | `/api/conversations/import` | SERVICE_KEY | Import JSONL (single-agent) |
| `POST` | `/api/conversations/import-review` | SERVICE_KEY | Import VTT_CHANNEL (multi-agent) |
| `POST` | `/api/conversations/upload` | Público | Upload manual desde UI |
| `GET` | `/api/conversations` | Público | Lista con filtros |
| `GET` | `/api/conversations/:id/content` | Público | Contenido completo |
| `GET` | `/api/agents/:agentId/timeline` | Público | Timeline del agente |
| `GET` | `/api/agents/:agentId/cost-report` | Público | Costos del agente |
| `GET` | `/api/projects/:projectId/cost-report` | Público | Costos del proyecto |
| `GET` | `/api/context` | SERVICE_KEY | Contexto runtime <500ms |
| `GET` | `/api/dashboard/stats` | Público | Métricas globales para UI |
| `GET` | `/api/health` | Público | Health check |

---

### 8.2 POST /api/conversations/import

Import de conversación single-agent (TASK_EXECUTION).

**Auth:** `Authorization: Bearer {SERVICE_KEY}`

**Request (multipart/form-data):**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `source` | string | ✅ | CLAUDE_CLI, CLAUDE_WEB, CLAUDE_SDK, CHATGPT |
| `agentId` | string | ✅ | VTT User.id del agente |
| `agentRole` | string | ✅ | Rol del agente (BE-Agent, DB-Agent, etc.) — Desnormalizado |
| `projectId` | string | ✅ | VTT Project.id |
| `externalSessionId` | string | ✅ | ID único de la sesión en origen |
| `taskId` | string | ❌ | VTT Task.id |
| `taskKey` | string | ❌ | VTT-123 |
| `taskTitle` | string | ❌ | Título desnormalizado |
| `file` | file | ✅ | Archivo principal (.json o .jsonl) |
| `logFile` | file | ❌ | Log file (solo SDK) |

**Response 201 (Created):**

```json
{
  "conversationId": "uuid-nuevo",
  "status": "IMPORTED",
  "turnCount": 15,
  "startedAt": "2026-04-10T10:00:00Z",
  "endedAt": "2026-04-10T10:30:00Z",
  "costUsd": 0.82,
  "classification": {
    "topics": ["authentication", "prisma"],
    "workType": "implementation",
    "entities": ["AuthService", "PrismaClient"]
  }
}
```

**Response 200 (Already exists):**

```json
{
  "conversationId": "uuid-existente",
  "status": "ALREADY_INDEXED"
}
```

**Response 400 (Validation error):**

```json
{
  "error": "Validation failed",
  "code": "MEM-ERR-400",
  "details": [
    { "field": "agentId", "message": "Required" }
  ]
}
```

---

### 8.3 POST /api/conversations/import-review

Import de conversación multi-agent (AGENT_REVIEW / AGENT_CLARIFICATION).

**Auth:** `Authorization: Bearer {SERVICE_KEY}`

**Request (multipart/form-data):**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `conversationType` | string | ✅ | AGENT_REVIEW o AGENT_CLARIFICATION |
| `projectId` | string | ✅ | VTT Project.id |
| `externalSessionId` | string | ✅ | ID único del canal/doc |
| `taskId` | string | ❌ | VTT Task.id |
| `taskKey` | string | ❌ | VTT-123 |
| `taskTitle` | string | ❌ | Título desnormalizado |
| `reviewRound` | number | ❌ | Número de ronda (1, 2, ...) |
| `participants` | JSON | ✅ | Array de participantes |
| `file` | file | ✅ | Archivo markdown con [VTT_MESSAGE] |

**participants JSON:**

```json
[
  { "agentId": "uuid-pm", "agentRole": "PM_REVISOR", "platform": "CLAUDE_CODE" },
  { "agentId": "uuid-ar", "agentRole": "AR", "platform": "CLAUDE_WEB" },
  { "agentId": "uuid-tl", "agentRole": "TL", "platform": "GOOGLE_DOCS" }
]
```

**Response 201:**

```json
{
  "conversationId": "uuid-nuevo",
  "status": "IMPORTED",
  "messageCount": 6,
  "participants": ["PM_REVISOR", "AR", "TL"],
  "startedAt": "2026-04-11T10:00:00Z",
  "endedAt": "2026-04-11T11:30:00Z"
}
```

**Response 200 (Incremental import):**

```json
{
  "conversationId": "uuid-existente",
  "status": "UPDATED",
  "newMessages": 2,
  "totalMessages": 8
}
```

---

### 8.4 POST /api/conversations/upload

Upload manual desde UI.

**Auth:** Público R1

**Request (multipart/form-data):**

Igual que `/import` pero sin `Authorization` header.

**Response:** Igual que `/import`.

---

### 8.5 GET /api/conversations

Lista de conversaciones con filtros para UI.

**Auth:** Público R1

**Query params:**

| Param | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `agentId` | string | - | Filtrar por agente |
| `projectId` | string | - | Filtrar por proyecto |
| `taskId` | string | - | Filtrar por tarea |
| `conversationType` | string | - | TASK_EXECUTION, AGENT_REVIEW, AGENT_CLARIFICATION |
| `source` | string | - | CLAUDE_CLI, CLAUDE_SDK, etc. |
| `status` | string | IMPORTED | PENDING, PROCESSING, IMPORTED, ERROR |
| `topic` | string | - | Filtrar por topic code |
| `workType` | string | - | implementation, bug-fix, etc. |
| `startDate` | ISO date | - | Desde (startedAt) |
| `endDate` | ISO date | - | Hasta (startedAt) |
| `limit` | number | 20 | Máximo 100 |
| `offset` | number | 0 | Paginación |

**Response 200:**

```json
{
  "total": 145,
  "limit": 20,
  "offset": 0,
  "conversations": [
    {
      "id": "uuid",
      "conversationType": "TASK_EXECUTION",
      "source": "CLAUDE_SDK",
      "primaryAgentId": "uuid-agent",
      "projectId": "uuid-project",
      "taskKey": "VTT-123",
      "taskTitle": "Implementar auth",
      "startedAt": "2026-04-10T10:00:00Z",
      "endedAt": "2026-04-10T10:30:00Z",
      "turnCount": 15,
      "costUsd": 0.82,
      "topics": ["authentication", "prisma"],
      "workType": "implementation"
    }
  ]
}
```

---

### 8.6 GET /api/conversations/:id/content

Contenido completo de una conversación.

**Auth:** Público R1

**Response 200 (TASK_EXECUTION):**

```json
{
  "conversationId": "uuid",
  "conversationType": "TASK_EXECUTION",
  "source": "CLAUDE_SDK",
  "primaryAgentId": "uuid-agent",
  "projectId": "uuid-project",
  "taskKey": "VTT-123",
  "taskTitle": "Implementar auth",
  "startedAt": "2026-04-10T10:00:00Z",
  "endedAt": "2026-04-10T10:30:00Z",
  "usage": {
    "inputTokens": 12400,
    "outputTokens": 8500,
    "cacheCreationTokens": 4500,
    "cacheReadTokens": 9800,
    "costUsd": 0.82,
    "modelId": "claude-sonnet-4-6"
  },
  "classification": {
    "topics": ["authentication", "prisma"],
    "workType": "implementation",
    "entities": ["AuthService"]
  },
  "turns": [
    {
      "turnIndex": 0,
      "role": "user",
      "content": "Implementa el auth service...",
      "timestamp": "2026-04-10T10:00:00Z"
    },
    {
      "turnIndex": 1,
      "role": "assistant",
      "timestamp": "2026-04-10T10:00:15Z",
      "blocks": [
        { "type": "text", "content": "Voy a crear el archivo..." },
        { "type": "tool_use", "tool": "Write", "filePath": "src/auth.service.ts", "success": true }
      ]
    }
  ]
}
```

**Response 200 (AGENT_REVIEW):**

```json
{
  "conversationId": "uuid",
  "conversationType": "AGENT_REVIEW",
  "source": "VTT_CHANNEL",
  "projectId": "uuid-project",
  "taskKey": "VTT-345",
  "taskTitle": "Modelo dinámico v4",
  "reviewRound": 1,
  "startedAt": "2026-04-11T10:00:00Z",
  "endedAt": "2026-04-11T11:30:00Z",
  "participants": [
    { "agentId": "uuid-pm", "agentRole": "PM_REVISOR", "platform": "CLAUDE_CODE" },
    { "agentId": "uuid-ar", "agentRole": "AR", "platform": "CLAUDE_WEB" }
  ],
  "messages": [
    {
      "messageId": "PM-001",
      "fromAgentId": "uuid-pm",
      "fromAgentRole": "PM_REVISOR",
      "toAgentId": "uuid-ar",
      "toAgentRole": "AR",
      "messageType": "REVIEW_REQUEST",
      "messageStatus": "DONE",
      "priority": "HIGH",
      "topic": "Validar modelo dinámico v4",
      "body": "Necesito que valides el modelo...",
      "expectedOutput": "ANALISIS_AR_S01_VTT-345.md",
      "timestamp": "2026-04-11T10:00:00Z",
      "inReplyTo": null
    },
    {
      "messageId": "AR-001",
      "fromAgentId": "uuid-ar",
      "toAgentId": "uuid-pm",
      "messageType": "REVIEW_RESPONSE",
      "messageStatus": "DONE",
      "priority": "HIGH",
      "body": "Revisé el modelo. Encontré 3 observaciones...",
      "timestamp": "2026-04-11T10:45:00Z",
      "inReplyTo": "PM-001"
    }
  ]
}
```

**Response 404:**

```json
{
  "error": "Conversation not found",
  "code": "MEM-ERR-404"
}
```

---

### 8.7 GET /api/agents/:agentId/timeline

Timeline de un agente.

**Auth:** Público R1

**Query params:**

| Param | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `projectId` | string | - | Filtrar por proyecto |
| `conversationType` | string | - | Filtrar por tipo |
| `limit` | number | 20 | Máximo 100 |
| `offset` | number | 0 | Paginación |

**Response 200:**

```json
{
  "agentId": "uuid-agent",
  "total": 45,
  "conversations": [
    {
      "id": "uuid",
      "conversationType": "TASK_EXECUTION",
      "source": "CLAUDE_SDK",
      "taskKey": "VTT-123",
      "taskTitle": "Implementar auth",
      "startedAt": "2026-04-10T10:00:00Z",
      "endedAt": "2026-04-10T10:30:00Z",
      "turnCount": 15,
      "costUsd": 0.82,
      "topics": ["authentication", "prisma"]
    }
  ]
}
```

**Nota:** Incluye tanto conversaciones donde `primaryAgentId = agentId` como conversaciones multi-agent donde el agente es participante.

---

### 8.8 GET /api/agents/:agentId/cost-report

Reporte de costos de un agente.

**Auth:** Público R1

**Query params:**

| Param | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `startDate` | ISO date | 30 días atrás | Desde |
| `endDate` | ISO date | hoy | Hasta |
| `projectId` | string | - | Filtrar por proyecto |

**Response 200:**

```json
{
  "agentId": "uuid-agent",
  "period": {
    "start": "2026-03-12",
    "end": "2026-04-12"
  },
  "summary": {
    "totalConversations": 45,
    "totalCostUsd": 18.30,
    "totalInputTokens": 450000,
    "totalOutputTokens": 280000
  },
  "byWeek": [
    { "week": "2026-W14", "costUsd": 4.50, "conversations": 12 },
    { "week": "2026-W15", "costUsd": 5.20, "conversations": 15 }
  ],
  "byWorkType": [
    { "workType": "implementation", "costUsd": 12.00, "conversations": 30 },
    { "workType": "bug-fix", "costUsd": 4.00, "conversations": 10 }
  ],
  "topTasks": [
    { "taskKey": "VTT-123", "taskTitle": "Implementar auth", "costUsd": 2.46, "sessions": 3 },
    { "taskKey": "VTT-234", "taskTitle": "DB migration", "costUsd": 1.80, "sessions": 2 }
  ]
}
```

---

### 8.9 GET /api/projects/:projectId/cost-report

Reporte de costos de un proyecto.

**Auth:** Público R1

**Query params:**

| Param | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `startDate` | ISO date | 30 días atrás | Desde |
| `endDate` | ISO date | hoy | Hasta |

**Response 200:**

```json
{
  "projectId": "uuid-project",
  "period": {
    "start": "2026-03-12",
    "end": "2026-04-12"
  },
  "summary": {
    "totalConversations": 120,
    "totalCostUsd": 45.67,
    "totalInputTokens": 1200000,
    "totalOutputTokens": 750000
  },
  "byAgent": [
    { "agentId": "uuid-be", "agentRole": "BE-Agent", "costUsd": 18.30, "conversations": 45, "percentage": 40 },
    { "agentId": "uuid-db", "agentRole": "DB-Agent", "costUsd": 11.20, "conversations": 28, "percentage": 25 }
  ],
  "topTasks": [
    { "taskKey": "VTT-234", "taskTitle": "DB migration", "costUsd": 4.10, "sessions": 5 },
    { "taskKey": "VTT-123", "taskTitle": "Auth service", "costUsd": 2.46, "sessions": 3 }
  ]
}
```

---

### 8.10 GET /api/context

Contexto runtime para Hook Manager. **DEBE responder en <500ms o fail-fast.**

**Auth:** `Authorization: Bearer {SERVICE_KEY}`

**Query params:**

| Param | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `agentId` | string | ✅ | VTT User.id del agente |
| `projectId` | string | ✅ | VTT Project.id |
| `taskId` | string | ❌ | VTT Task.id (para buscar sesiones de misma tarea) |
| `topics` | string | ❌ | Comma-separated topic codes |
| `limit` | number | 5 | Máximo items por sección |

**Response 200:**

```json
{
  "agentId": "uuid-agent",
  "projectId": "uuid-project",
  "generatedAt": "2026-04-12T10:00:00Z",
  "responseTimeMs": 180,
  "context": {
    "recentSessions": [
      {
        "conversationId": "uuid",
        "conversationType": "TASK_EXECUTION",
        "taskKey": "VTT-122",
        "taskTitle": "Middleware auth",
        "startedAt": "2026-04-10T10:00:00Z",
        "topics": ["authentication", "middleware"]
      }
    ],
    "taskRelatedSessions": [
      {
        "conversationId": "uuid",
        "taskKey": "VTT-123",
        "startedAt": "2026-04-09T14:00:00Z"
      }
    ],
    "topicRelatedSessions": [
      {
        "conversationId": "uuid",
        "topics": ["authentication"],
        "startedAt": "2026-04-08T09:00:00Z"
      }
    ],
    "recentReviews": [
      {
        "conversationId": "uuid",
        "conversationType": "AGENT_REVIEW",
        "taskKey": "VTT-120",
        "outcome": "DONE"
      }
    ],
    "frequentFiles": [
      "src/auth.service.ts",
      "src/middleware/auth.ts",
      "prisma/schema.prisma"
    ],
    "totalCostUsd": 12.50
  }
}
```

**Response 504 (timeout):**

Si la query tarda >500ms, retorna inmediatamente:

```json
{
  "error": "Context generation timeout",
  "code": "MEM-ERR-504",
  "message": "Proceed without context"
}
```

---

### 8.11 GET /api/dashboard/stats

Métricas globales para UI dashboard.

**Auth:** Público R1

**Response 200:**

```json
{
  "generatedAt": "2026-04-12T10:00:00Z",
  "totals": {
    "conversations": 1250,
    "conversationsToday": 15,
    "totalCostUsd": 456.78,
    "costThisMonth": 89.50,
    "activeAgents": 7
  },
  "byStatus": {
    "imported": 1240,
    "pending": 5,
    "processing": 2,
    "error": 3
  },
  "recentActivity": [
    {
      "conversationId": "uuid",
      "conversationType": "TASK_EXECUTION",
      "primaryAgentId": "uuid",
      "taskKey": "VTT-456",
      "importedAt": "2026-04-12T09:55:00Z"
    }
  ],
  "errorsToReview": [
    {
      "conversationId": "uuid",
      "externalSessionId": "session_xyz",
      "errorMessage": "Failed to parse JSONL",
      "updatedAt": "2026-04-12T09:30:00Z"
    }
  ]
}
```

---

### 8.12 GET /api/health

Health check.

**Auth:** Público

**Response 200:**

```json
{
  "status": "healthy",
  "timestamp": "2026-04-12T10:00:00Z",
  "checks": {
    "database": { "status": "ok", "latencyMs": 5 },
    "storage": { "status": "ok", "path": "/storage", "writable": true },
    "redis": { "status": "ok", "latencyMs": 2 }
  },
  "stats": {
    "lastImportAt": "2026-04-12T09:55:00Z",
    "pendingCount": 5,
    "errorCount": 3
  }
}
```

**Response 503 (unhealthy):**

```json
{
  "status": "unhealthy",
  "timestamp": "2026-04-12T10:00:00Z",
  "checks": {
    "database": { "status": "error", "error": "Connection refused" },
    "storage": { "status": "ok" },
    "redis": { "status": "ok" }
  }
}
```

---

## 9. FLUJOS DE IMPORTACIÓN

### 9.1 Flujo TASK_EXECUTION (Single-Agent)

```typescript
// services/importer.service.ts

async function importTaskExecution(input: ImportInput): Promise<ImportResult> {
  const { externalSessionId, source, agentId, agentRole, projectId } = input;

  // 1. Verificar idempotencia (compuesta: sourceId + externalSessionId)
  const sourceRecord = await prisma.sourceCatalog.findUnique({ where: { code: source } });
  if (!sourceRecord) {
    throw new Error(`Unknown source: ${source}`);
  }
  
  const existing = await prisma.conversation.findUnique({
    where: {
      sourceId_externalSessionId: {
        sourceId: sourceRecord.id,
        externalSessionId,
      },
    },
  });
  if (existing) {
    return { conversationId: existing.id, status: 'ALREADY_INDEXED' };
  }

  // 2. Parsear archivo PRIMERO para obtener fechas reales
  const adapter = getAdapter(source);
  const parsed = await adapter.parse(input.file, input.logFile);
  
  // 3. Obtener IDs de catálogos
  const [typeRecord, pendingStatus] = await Promise.all([
    prisma.conversationTypeCatalog.findUnique({ where: { code: 'TASK_EXECUTION' } }),
    prisma.conversationStatusCatalog.findUnique({ where: { code: 'PENDING' } }),
  ]);

  // 4. INSERT con status PENDING y fechas REALES de la sesión
  const conversation = await prisma.conversation.create({
    data: {
      externalSessionId,
      sourceId: sourceRecord.id,
      conversationTypeId: typeRecord!.id,
      statusId: pendingStatus!.id,
      primaryAgentId: agentId,      // Single-agent: siempre tiene primaryAgentId
      primaryAgentRole: agentRole,  // Desnormalizado para cost-report
      projectId,
      taskId: input.taskId,
      taskKey: input.taskKey,
      taskTitle: input.taskTitle,
      startedAt: parsed.startedAt,  // FECHA REAL de la sesión
      endedAt: parsed.endedAt,       // FECHA REAL de la sesión
      turnCount: 0,
      // importedAt se setea automáticamente por @default(now())
    },
  });

  // 5. UPDATE a PROCESSING antes de escribir archivo
  const processingStatus = await prisma.conversationStatusCatalog.findUnique({
    where: { code: 'PROCESSING' },
  });
  await prisma.conversation.update({
    where: { id: conversation.id },
    data: { statusId: processingStatus!.id },
  });

  try {
    // 6. Escribir archivo en /storage/ usando FECHA REAL
    const storagePath = await storageService.save({
      primaryAgentId: agentId,
      startedAt: parsed.startedAt,  // Para organizar por mes real
      externalSessionId,
      file: input.file,
      logFile: input.logFile,
    });

    // 7. Clasificar
    const classification = await classifierService.classify(parsed);

    // 8. Persistir turns, blocks, usage, classification
    await prisma.$transaction(async (tx) => {
      // ... (código de persistencia igual que antes)
      
      // UPDATE status IMPORTED
      const importedStatus = await tx.conversationStatusCatalog.findUnique({
        where: { code: 'IMPORTED' },
      });
      await tx.conversation.update({
        where: { id: conversation.id },
        data: {
          statusId: importedStatus!.id,
          filePath: storagePath.filePath,
          logFilePath: storagePath.logFilePath,
          turnCount: parsed.turns.length,
        },
      });
    });

    return {
      conversationId: conversation.id,
      status: 'IMPORTED',
      turnCount: parsed.turns.length,
      startedAt: parsed.startedAt,
      endedAt: parsed.endedAt,
      costUsd: parsed.usage?.costUsd,
      classification,
    };
  } catch (error) {
    // Queda en PROCESSING para cleanup job
    console.error('Import failed:', error);
    throw error;
  }
}
```

### 9.2 Flujo AGENT_REVIEW (Multi-Agent)

```typescript
async function importAgentReview(input: ImportReviewInput): Promise<ImportResult> {
  const { externalSessionId, projectId, participants } = input;

  // 1. Resolver sourceId para VTT_CHANNEL
  const sourceRecord = await prisma.sourceCatalog.findUnique({ 
    where: { code: 'VTT_CHANNEL' } 
  });
  if (!sourceRecord) {
    throw new Error('Source VTT_CHANNEL not found in catalog');
  }

  // 2. Verificar si existe (idempotencia compuesta: sourceId + externalSessionId)
  const existing = await prisma.conversation.findUnique({
    where: {
      sourceId_externalSessionId: {
        sourceId: sourceRecord.id,
        externalSessionId,
      },
    },
    include: { messages: true },
  });

  // 3. Parsear archivo
  const parsed = await vttChannelAdapter.parse(input.file);

  if (existing) {
    // Import incremental: solo agregar mensajes nuevos
    const existingMessageIds = new Set(existing.messages.map(m => m.messageId));
    const newMessages = parsed.messages.filter(m => !existingMessageIds.has(m.messageId));
    
    if (newMessages.length === 0) {
      return { conversationId: existing.id, status: 'ALREADY_INDEXED' };
    }

    // Insertar nuevos mensajes
    await prisma.$transaction(async (tx) => {
      for (const msg of newMessages) {
        await tx.agentMessage.create({
          data: {
            conversationId: existing.id,
            messageId: msg.messageId,
            // ... resto de campos
          },
        });
      }
      
      // Actualizar endedAt si hay mensajes más recientes
      const latestTimestamp = Math.max(...newMessages.map(m => m.timestamp.getTime()));
      await tx.conversation.update({
        where: { id: existing.id },
        data: { endedAt: new Date(latestTimestamp) },
      });
    });

    return {
      conversationId: existing.id,
      status: 'UPDATED',
      newMessages: newMessages.length,
      totalMessages: existing.messages.length + newMessages.length,
    };
  }

  // 4. Nueva conversación multi-agent
  const [typeRecord, pendingStatus] = await Promise.all([
    prisma.conversationTypeCatalog.findUnique({ where: { code: input.conversationType } }),
    prisma.conversationStatusCatalog.findUnique({ where: { code: 'PENDING' } }),
  ]);

  // 5. INSERT con primaryAgentId = NULL (multi-agent)
  const conversation = await prisma.conversation.create({
    data: {
      externalSessionId,
      sourceId: sourceRecord.id,  // Usar sourceRecord ya resuelto
      conversationTypeId: typeRecord!.id,
      statusId: pendingStatus!.id,
      primaryAgentId: null,  // NULL para multi-agent
      projectId,
      taskId: input.taskId,
      taskKey: input.taskKey,
      taskTitle: input.taskTitle,
      reviewRound: input.reviewRound,
      startedAt: parsed.startedAt,
      endedAt: parsed.endedAt,
    },
  });

  // 6. UPDATE a PROCESSING
  const processingStatus = await prisma.conversationStatusCatalog.findUnique({
    where: { code: 'PROCESSING' },
  });
  await prisma.conversation.update({
    where: { id: conversation.id },
    data: { statusId: processingStatus!.id },
  });

  try {
    // 7. Escribir archivo
    const storagePath = await storageService.saveReview({
      projectId,
      externalSessionId,
      startedAt: parsed.startedAt,
      file: input.file,
    });

    // 7. Persistir participants y messages
    await prisma.$transaction(async (tx) => {
      // Participants
      for (const p of participants) {
        const platform = p.platform
          ? await tx.platformCatalog.findUnique({ where: { code: p.platform } })
          : null;
        
        await tx.conversationParticipant.create({
          data: {
            conversationId: conversation.id,
            agentId: p.agentId,
            agentRole: p.agentRole,
            platformId: platform?.id,
          },
        });
      }

      // Messages
      for (const msg of parsed.messages) {
        await tx.agentMessage.create({
          data: {
            conversationId: conversation.id,
            messageId: msg.messageId,
            inReplyTo: msg.inReplyTo,
            fromAgentId: msg.fromAgentId,
            toAgentId: msg.toAgentId,
            messageTypeId: (await tx.messageTypeCatalog.findUnique({ where: { code: msg.messageType } }))!.id,
            messageStatusId: (await tx.messageStatusCatalog.findUnique({ where: { code: msg.messageStatus } }))!.id,
            priorityId: (await tx.priorityCatalog.findUnique({ where: { code: msg.priority } }))!.id,
            topic: msg.topic,
            body: msg.body,
            expectedOutput: msg.expectedOutput,
            timestamp: msg.timestamp,
          },
        });
      }

      // UPDATE status IMPORTED
      const importedStatus = await tx.conversationStatusCatalog.findUnique({
        where: { code: 'IMPORTED' },
      });
      await tx.conversation.update({
        where: { id: conversation.id },
        data: {
          statusId: importedStatus!.id,
          filePath: storagePath.filePath,
        },
      });
    });

    return {
      conversationId: conversation.id,
      status: 'IMPORTED',
      messageCount: parsed.messages.length,
      participants: participants.map(p => p.agentRole),
      startedAt: parsed.startedAt,
      endedAt: parsed.endedAt,
    };
  } catch (error) {
    console.error('Import review failed:', error);
    throw error;
  }
}
```

---

## 10. ATOMICIDAD Y RECOVERY

### 10.1 Flujo de Estados

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE ESTADOS                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PENDING ──────────────► PROCESSING ──────────────► IMPORTED │
│     │                        │                               │
│     │                        │ (si falla)                    │
│     │                        ▼                               │
│     │                      ERROR                             │
│     │                        ▲                               │
│     │ (timeout sin          │                               │
│     │  avanzar a            │                               │
│     │  PROCESSING)          │                               │
│     └────────────────────────┘                               │
│                                                              │
│  PENDING: Registro creado, esperando procesamiento           │
│  PROCESSING: Escribiendo archivo en /storage/                │
│  IMPORTED: Completado exitosamente                           │
│  ERROR: Falló, requiere intervención o retry                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 10.2 Cleanup Job

```typescript
// jobs/cleanup.job.ts
import cron from 'node-cron';

const STALE_THRESHOLD_MINUTES = 10;
const MAX_RETRIES = 3;

// Ejecutar cada 5 minutos
cron.schedule('*/5 * * * *', async () => {
  console.log('[Cleanup] Starting cleanup job...');
  
  const staleThreshold = new Date(Date.now() - STALE_THRESHOLD_MINUTES * 60 * 1000);
  
  // Buscar conversaciones stuck en PENDING o PROCESSING
  // Incluye retryCount <= MAX_RETRIES para poder marcar ERROR definitivo
  const staleConversations = await prisma.conversation.findMany({
    where: {
      status: {
        code: { in: ['PENDING', 'PROCESSING'] },
      },
      updatedAt: { lt: staleThreshold },
      retryCount: { lte: MAX_RETRIES },  // <= para incluir los que están en el límite
    },
    include: {
      status: true,
    },
  });

  for (const conv of staleConversations) {
    console.log(`[Cleanup] Processing stale conversation: ${conv.id} (status: ${conv.status.code}, retries: ${conv.retryCount})`);
    
    if (conv.retryCount >= MAX_RETRIES) {
      // Marcar como ERROR definitivo (ya llegó al límite)
      const errorStatus = await prisma.conversationStatusCatalog.findUnique({
        where: { code: 'ERROR' },
      });
      await prisma.conversation.update({
        where: { id: conv.id },
        data: {
          statusId: errorStatus!.id,
          errorMessage: `Max retries (${MAX_RETRIES}) exceeded`,
        },
      });
      console.log(`[Cleanup] Marked as ERROR (max retries): ${conv.id}`);
    } else {
      // Incrementar retry y volver a PENDING para reprocesar
      const pendingStatus = await prisma.conversationStatusCatalog.findUnique({
        where: { code: 'PENDING' },
      });
      await prisma.conversation.update({
        where: { id: conv.id },
        data: {
          statusId: pendingStatus!.id,
          retryCount: conv.retryCount + 1,
          errorMessage: null,
        },
      });
      console.log(`[Cleanup] Reset to PENDING (retry ${conv.retryCount + 1}): ${conv.id}`);
      
      // TODO: Trigger reprocesamiento si el archivo original está disponible
    }
  }

  console.log(`[Cleanup] Processed ${staleConversations.length} stale conversations`);
});
```

---

## 11. SERVICIO DE CONTEXTO RUNTIME

### 11.1 Implementación (<500ms, Fail-Fast)

```typescript
// services/context.service.ts

const CONTEXT_TIMEOUT_MS = 500;

interface ContextInput {
  agentId: string;
  projectId: string;
  taskId?: string;
  topics?: string[];
  limit?: number;
}

export const contextService = {
  async getContext(input: ContextInput): Promise<ContextResponse> {
    const startTime = Date.now();
    const limit = input.limit || 5;

    try {
      // Todas las queries en paralelo con timeout
      const results = await Promise.race([
        this.executeQueries(input, limit),
        this.timeoutPromise(CONTEXT_TIMEOUT_MS),
      ]);

      const responseTimeMs = Date.now() - startTime;

      return {
        agentId: input.agentId,
        projectId: input.projectId,
        generatedAt: new Date().toISOString(),
        responseTimeMs,
        context: results,
      };
    } catch (error) {
      if (error.message === 'TIMEOUT') {
        return {
          error: 'Context generation timeout',
          code: 'MEM-ERR-504',
          message: 'Proceed without context',
        };
      }
      throw error;
    }
  },

  async executeQueries(input: ContextInput, limit: number) {
    const importedStatus = await prisma.conversationStatusCatalog.findUnique({
      where: { code: 'IMPORTED' },
    });
    const importedStatusId = importedStatus!.id;

    const [recentSessions, taskRelated, topicRelated, reviews, files, cost] = await Promise.all([
      // Sesiones recientes del agente EN ESTE PROYECTO
      prisma.conversation.findMany({
        where: {
          primaryAgentId: input.agentId,
          projectId: input.projectId,  // Filtrar por proyecto
          statusId: importedStatusId,
        },
        orderBy: { startedAt: 'desc' },
        take: limit,
        select: {
          id: true,
          conversationType: { select: { code: true } },
          taskKey: true,
          taskTitle: true,
          startedAt: true,
          topics: { include: { topic: true } },
        },
      }),

      // Sesiones de la misma tarea (si se proporciona taskId)
      input.taskId
        ? prisma.conversation.findMany({
            where: {
              taskId: input.taskId,
              projectId: input.projectId,  // Filtrar por proyecto
              statusId: importedStatusId,
            },
            orderBy: { startedAt: 'desc' },
            take: limit,
            select: {
              id: true,
              taskKey: true,
              startedAt: true,
            },
          })
        : [],

      // Sesiones con topics similares
      input.topics?.length
        ? prisma.conversation.findMany({
            where: {
              primaryAgentId: input.agentId,
              projectId: input.projectId,
              statusId: importedStatusId,
              topics: {
                some: {
                  topic: { code: { in: input.topics } },
                },
              },
            },
            orderBy: { startedAt: 'desc' },
            take: limit,
            select: {
              id: true,
              startedAt: true,
              topics: { include: { topic: true } },
            },
          })
        : [],

      // Reviews recientes donde participó EN ESTE PROYECTO
      prisma.conversation.findMany({
        where: {
          projectId: input.projectId,  // Filtrar por proyecto
          OR: [
            { primaryAgentId: input.agentId },
            { participants: { some: { agentId: input.agentId } } },
          ],
          conversationType: { code: { in: ['AGENT_REVIEW', 'AGENT_CLARIFICATION'] } },
          statusId: importedStatusId,
        },
        orderBy: { startedAt: 'desc' },
        take: 3,
        select: {
          id: true,
          conversationType: { select: { code: true } },
          taskKey: true,
          messages: {
            take: 1,
            orderBy: { timestamp: 'desc' },
            select: { messageStatus: { select: { code: true } } },
          },
        },
      }),

      // Archivos frecuentemente modificados
      prisma.turnBlock.groupBy({
        by: ['filePath'],
        where: {
          filePath: { not: null },
          turn: {
            conversation: {
              primaryAgentId: input.agentId,
              projectId: input.projectId,
              statusId: importedStatusId,
            },
          },
        },
        _count: { filePath: true },
        orderBy: { _count: { filePath: 'desc' } },
        take: 10,
      }),

      // Costo total del agente en este proyecto
      prisma.conversationUsage.aggregate({
        where: {
          conversation: {
            primaryAgentId: input.agentId,
            projectId: input.projectId,
            statusId: importedStatusId,
          },
        },
        _sum: { costUsd: true },
      }),
    ]);

    return {
      recentSessions: recentSessions.map(s => ({
        conversationId: s.id,
        conversationType: s.conversationType.code,
        taskKey: s.taskKey,
        taskTitle: s.taskTitle,
        startedAt: s.startedAt.toISOString(),
        topics: s.topics.map(t => t.topic.code),
      })),
      taskRelatedSessions: taskRelated.map(s => ({
        conversationId: s.id,
        taskKey: s.taskKey,
        startedAt: s.startedAt.toISOString(),
      })),
      topicRelatedSessions: topicRelated.map(s => ({
        conversationId: s.id,
        topics: s.topics.map(t => t.topic.code),
        startedAt: s.startedAt.toISOString(),
      })),
      recentReviews: reviews.map(r => ({
        conversationId: r.id,
        conversationType: r.conversationType.code,
        taskKey: r.taskKey,
        outcome: r.messages[0]?.messageStatus.code || 'UNKNOWN',
      })),
      frequentFiles: files.filter(f => f.filePath).map(f => f.filePath!),
      totalCostUsd: Number(cost._sum.costUsd || 0),
    };
  },

  timeoutPromise(ms: number): Promise<never> {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error('TIMEOUT')), ms);
    });
  },
};
```

---

## 12. CLASIFICACIÓN POR REGLAS

(Sin cambios respecto a v1.2 — código de clasificación permanece igual)

---

## 13. ALMACENAMIENTO DE ARCHIVOS

### 13.1 Storage Service (Corregido para Temporalidad)

```typescript
// services/storage.service.ts
import fs from 'fs/promises';
import path from 'path';
import dayjs from 'dayjs';

const STORAGE_ROOT = process.env.STORAGE_PATH || '/storage';

interface SaveInput {
  primaryAgentId: string;
  startedAt: Date;  // FECHA REAL de la sesión
  externalSessionId: string;
  file: Buffer;
  logFile?: Buffer;
}

interface SaveReviewInput {
  projectId: string;
  startedAt: Date;
  externalSessionId: string;
  file: Buffer;
}

export const storageService = {
  async save(input: SaveInput): Promise<{ filePath: string; logFilePath?: string }> {
    const { primaryAgentId, startedAt, externalSessionId, file, logFile } = input;
    
    // Usar YYYY-MM de startedAt REAL, no del momento de import
    const yearMonth = dayjs(startedAt).format('YYYY-MM');

    const dir = path.join(STORAGE_ROOT, primaryAgentId, yearMonth, externalSessionId);
    await fs.mkdir(dir, { recursive: true });

    const filePath = path.join(dir, 'session.json');
    await fs.writeFile(filePath, file);

    let logFilePath: string | undefined;
    if (logFile) {
      logFilePath = path.join(dir, 'log.jsonl');
      await fs.writeFile(logFilePath, logFile);
    }

    return { filePath, logFilePath };
  },

  async saveReview(input: SaveReviewInput): Promise<{ filePath: string }> {
    const { projectId, startedAt, externalSessionId, file } = input;
    
    // Para multi-agent, organizar por proyecto
    const yearMonth = dayjs(startedAt).format('YYYY-MM');

    const dir = path.join(STORAGE_ROOT, '_reviews', projectId, yearMonth, externalSessionId);
    await fs.mkdir(dir, { recursive: true });

    const filePath = path.join(dir, 'channel.md');
    await fs.writeFile(filePath, file);

    return { filePath };
  },

  async read(filePath: string): Promise<Buffer> {
    return fs.readFile(filePath);
  },

  async exists(filePath: string): Promise<boolean> {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  },
};
```

### 13.2 Estructura de Storage

```
/storage/
├── {primaryAgentId}/           # Conversaciones single-agent
│   └── {YYYY-MM}/              # Mes de startedAt REAL
│       └── {externalSessionId}/
│           ├── session.json
│           └── log.jsonl       # Solo SDK
│
└── _reviews/                   # Conversaciones multi-agent
    └── {projectId}/
        └── {YYYY-MM}/
            └── {externalSessionId}/
                └── channel.md
```

---

## 14. PLAN DE IMPLEMENTACIÓN

### 14.1 Tareas por Sprint (Actualizado)

| Sprint | Tarea | Horas | Owner |
|--------|-------|-------|-------|
| **S01** | Schema Prisma v1.4 + migraciones | 4h | DB |
| **S01** | Seed de catálogos (incl. VTT_CHANNEL, GOOGLE_DOCS) | 2h | DB |
| **S01** | Setup proyecto (Express, estructura, middleware auth) | 3h | BE |
| **S01** | POST /import — CLI adapter + storage | 6h | BE |
| **S02** | POST /import — SDK adapter (2 archivos, costo) | 4h | BE |
| **S02** | GET /agents/:id/timeline (single + multi-agent) | 4h | BE |
| **S02** | Clasificación por reglas | 4h | BE |
| **S03** | GET /conversations/:id/content (ambos tipos) | 4h | BE |
| **S03** | GET /context (<500ms, fail-fast) | 5h | BE |
| **S03** | Tests de rendimiento contexto (<500ms) | 3h | QA |
| **S04** | POST /import-review (VTT_CHANNEL, multi-agent) | 6h | BE |
| **S04** | POST /import — Web + ChatGPT adapters | 4h | BE |
| **S04** | Cleanup job (cron cada 5 min) | 2h | BE |
| **S05** | GET /conversations (lista con filtros) | 3h | BE |
| **S05** | GET /cost-report (proyecto + agente) | 4h | BE |
| **S05** | GET /dashboard/stats | 2h | BE |
| **S05** | POST /upload + GET /health | 2h | BE |
| **S06** | Dockerfile + docker-compose | 2h | DevOps |
| **S06** | Deploy VM + volumen storage | 3h | DevOps |
| **S06** | Integración Hook Manager | 4h | BE |
| **S06** | Tests E2E (todos los endpoints) | 5h | QA |
| | **TOTAL BACKEND** | **76h** | |

### 14.2 Estimación por Rol

| Rol | Horas |
|-----|-------|
| DB Engineer | 6h |
| BE Engineer | 57h |
| DevOps | 5h |
| QA | 8h |
| **TOTAL BACKEND** | **76h** |
| **UI (de sección 17)** | **46h** |
| **TOTAL PROYECTO** | **122h** |

---

## 15. CRITERIOS DE ACEPTACIÓN

### 15.1 Funcionales

- [ ] Import TASK_EXECUTION retorna conversationId, status IMPORTED, timestamps reales
- [ ] Import AGENT_REVIEW soporta múltiples participantes, primaryAgentId = NULL
- [ ] Import incremental VTT_CHANNEL agrega solo mensajes nuevos
- [ ] Import duplicado retorna ALREADY_INDEXED sin error
- [ ] Timeline incluye conversaciones single-agent y participaciones multi-agent
- [ ] Content retorna estructura correcta para ambos tipos
- [ ] Contexto responde en <500ms o retorna error 504
- [ ] Cost-report suma correctamente por proyecto/agente
- [ ] Clasificación detecta topics, workType, entities
- [ ] Dashboard stats muestra totales y errores pendientes

### 15.2 Técnicos

- [ ] Schema Prisma v1.4 sin errores de migración
- [ ] Todos los catálogos seedeados (incl. VTT_CHANNEL, GOOGLE_DOCS)
- [ ] Índices creados correctamente
- [ ] Storage organizado por fecha REAL de sesión
- [ ] Cleanup job ejecuta cada 5 min
- [ ] Estados: PENDING → PROCESSING → IMPORTED/ERROR correctamente
- [ ] Health check retorna status de BD, storage, Redis

### 15.3 Integración

- [ ] Hook Manager puede llamar POST /import con SERVICE_KEY
- [ ] Hook Manager puede llamar GET /context con SERVICE_KEY
- [ ] UI puede llamar todos los endpoints públicos sin auth
- [ ] Endpoints SERVICE_KEY rechazan requests sin header

### 15.4 Seguridad

- [ ] No exponer stack traces en producción
- [ ] Validación de inputs con Zod
- [ ] SERVICE_KEY no en código ni logs
- [ ] Endpoints públicos no exponen datos sensibles

---

## 16. DOCKER-COMPOSE (PRODUCCIÓN)

```yaml
# /root/memory-service/docker-compose.yml
version: '3.8'

services:
  memory-service:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: memory-service
    restart: always
    ports:
      - "3002:3002"
    environment:
      NODE_ENV: production
      PORT: 3002
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@shared-postgres:5432/memory_service_db?connection_limit=20
      REDIS_URL: redis://shared-redis:6379
      REDIS_PREFIX: mem
      SERVICE_KEY: ${SERVICE_KEY}
      STORAGE_PATH: /storage
    volumes:
      - /root/memory-service-storage:/storage
    networks:
      - shared-network
    mem_limit: 512m
    mem_reservation: 256m

networks:
  shared-network:
    external: true
```

---

## 17. UI STANDALONE

(Sin cambios respecto a v1.2 — contenido de UI permanece igual)

### 17.1 Arquitectura

| Aspecto | Valor |
|---------|-------|
| **Tipo** | SPA standalone |
| **Puerto** | 3003 |
| **API** | Consume `http://{host}:3002/api/...` |
| **Stack** | React 18 + TypeScript + Vite + TailwindCSS |
| **Deploy** | Nginx en VM, container separado |
| **Auth R1** | Sin autenticación — acceso directo |

### 17.2 Plan de Implementación UI

| Sprint | Pantalla | Horas | Owner |
|--------|----------|-------|-------|
| **S-UI-01** | Setup proyecto | 2h | FE |
| **S-UI-01** | Agent Timeline | 6h | FE |
| **S-UI-01** | Conversation Viewer (TASK_EXECUTION) | 8h | FE |
| **S-UI-02** | Dashboard | 4h | FE |
| **S-UI-02** | Cost Report Proyecto | 4h | FE |
| **S-UI-02** | Import Manual | 4h | FE |
| **S-UI-03** | Conversation Viewer (AGENT_REVIEW) | 6h | FE |
| **S-UI-03** | Lista/Búsqueda con filtros | 4h | FE |
| **S-UI-04** | Cost Report Agente | 3h | FE |
| **S-UI-04** | Health Page | 2h | FE |
| **S-UI-04** | Estados de error, empty, loading | 3h | FE |
| | **TOTAL UI** | **46h** | |

---

**Documento:** SPEC_MEMORY_SERVICE_v1.4.md  
**Versión:** 1.4  
**Estado:** REVISADO TL — LISTO PARA CONSOLIDACIÓN SA  

---

*Documento relacionado: METODOLOGIA_MEMORY_SERVICE_v1.1.md*
