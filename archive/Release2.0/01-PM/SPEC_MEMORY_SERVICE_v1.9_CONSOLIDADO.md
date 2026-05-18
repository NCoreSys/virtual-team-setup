# ESPECIFICACIÓN TÉCNICA: Memory Service

**Versión:** 1.9  
**Fecha:** 2026-04-21  
**Autor:** PM (Martin Rivas) + SA-Agent (Consolidación)  
**Estado:** ✅ APROBADO PM — CIERRE FINAL  
**Documento relacionado:** METODOLOGIA_MEMORY_SERVICE_v1.2.md  
**Firma cierre:** PM Martin Rivas — 2026-04-21

---

## CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-11 | Documento inicial |
| 1.1 | 2026-04-11 | GAPs resueltos por DevOps: storage volume, SERVICE_KEY, connection_limit |
| 1.2 | 2026-04-11 | Agregada sección 17: UI Standalone |
| 1.3 | 2026-04-12 | **Revisión AR:** 7 bloqueos resueltos (B-01 a B-07) |
| 1.4 | 2026-04-12 | **Correcciones AR:** primaryAgentRole, GET /context filtra projectId, cleanup job lógica, constraints únicos, idempotencia compuesta. **Revisión TL:** D-MEM-43 (AMB-01 cerrada) |
| 1.5 | 2026-04-12 | Corrección versionado interno, NOTA-SA-01 a NOTA-SA-05 para consolidación |
| 1.6 | 2026-04-12 | Integración parcial de observaciones AR/DB/TL |
| 1.7 | 2026-04-12 | **CONSOLIDACIÓN SA FINAL:** Integradas todas las observaciones AR/DB/TL. Sin notas pendientes. |
| 1.8 | 2026-04-12 | Corrección estado de proceso: pendiente cierre final PM Revisor (no implementación) |
| **1.9** | **2026-04-21** | **CIERRE FINAL PM (Martin Rivas).** Integrado ADDENDUM v1.1 (§5.2 platformRefs para Runtime + §5.3 índice GIN). Alcance §14 marcado como OBSOLETO (plan vigente: `HO_ACTUALIZAR_TAREAS_VTT.md v2.1` — 116 tareas, 381h). Versionado interno alineado con nombre de archivo. |

### Observaciones integradas en v1.7

| Origen | ID | Integración |
|--------|-----|-------------|
| PM | Punto 1 | `@@unique([conversationId, entityName])` en ConversationEntity — §4.1 |
| PM | Punto 2 | Partial indexes por migración SQL manual — §6.1 |
| PM | Punto 3 | Manejo error P2002 para idempotencia concurrente — §9.1, §9.2 |
| PM | Punto 4 | Cache de catálogos en startup + uso en GET /context y cleanup — §3.3, §10.2, §11.1 |
| PM | Punto 5 | Cleanup job filtra por `statusId` (no `status.code`) — §10.2 |
| PM | Punto 6 | Prefetch catálogos en importAgentReview (N+1 corregido) — §9.2 |
| PM | Punto 7 | Índices DB adicionales — §6.1 |
| PM | Punto 8 | Versionado consistente header/footer/changelog — Documento completo |
| AR | AR-OBS-01 | Versionado corregido |
| AR | AR-OBS-02 | Cleanup usa statusId — §10.2 |
| DB | DB-OBS-01 | Constraint ConversationEntity — §4.1 |
| DB | DB-OBS-02 | Cleanup por statusId — §10.2 |
| DB | DB-OBS-03 | N+1 en importAgentReview — §9.2 |
| DB | DB-OBS-04 | Partial indexes documentados — §6.1 |
| DB | DB-OBS-05 | Índice `(primaryAgentId, projectId, startedAt DESC)` — §6.1 |
| DB | DB-OBS-06 | Índice `AgentMessage(conversationId, timestamp DESC)` — §6.1 |
| DB | DB-OBS-07 | Índice `Conversation(importedAt DESC)` — §6.1 |
| DB | DB-OBS-08 | Manejo P2002 — §9.1, §9.2 |
| TL | DEC-04/AMB-01 | D-MEM-43: contentPreview en BD, content desde /storage/ — §2.4 |
| TL | TL-01 | Pre-fetch statusId antes de transacción — §9.1 |
| TL | TL-03 | N+1 corregido con Maps pre-fetcheados — §9.2 |
| TL | AMB-07 | Catch delega siempre al cleanup job — §9.1 |

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
| **Contenido** | GET /conversations/:id/content (lee desde /storage/) |
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
│       └── manual/
│           └── partial_indexes.sql
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
│   │   ├── catalog-cache.service.ts
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

### 3.3 Cache de Catálogos en Startup

Para evitar lookups repetidos en `GET /context`, cleanup job e imports, cargar catálogos en memoria al iniciar el servicio:

```typescript
// services/catalog-cache.service.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

interface CatalogCache {
  sources: Map<string, string>;           // code -> id
  conversationTypes: Map<string, string>; // code -> id
  statuses: Map<string, string>;          // code -> id
  workTypes: Map<string, string>;         // code -> id
  blockTypes: Map<string, string>;        // code -> id
  messageTypes: Map<string, string>;      // code -> id
  messageStatuses: Map<string, string>;   // code -> id
  platforms: Map<string, string>;         // code -> id
  priorities: Map<string, string>;        // code -> id
}

let cache: CatalogCache | null = null;

export async function initCatalogCache(): Promise<void> {
  const [
    sources,
    conversationTypes,
    statuses,
    workTypes,
    blockTypes,
    messageTypes,
    messageStatuses,
    platforms,
    priorities,
  ] = await Promise.all([
    prisma.sourceCatalog.findMany(),
    prisma.conversationTypeCatalog.findMany(),
    prisma.conversationStatusCatalog.findMany(),
    prisma.workTypeCatalog.findMany(),
    prisma.blockTypeCatalog.findMany(),
    prisma.messageTypeCatalog.findMany(),
    prisma.messageStatusCatalog.findMany(),
    prisma.platformCatalog.findMany(),
    prisma.priorityCatalog.findMany(),
  ]);

  cache = {
    sources: new Map(sources.map(s => [s.code, s.id])),
    conversationTypes: new Map(conversationTypes.map(t => [t.code, t.id])),
    statuses: new Map(statuses.map(s => [s.code, s.id])),
    workTypes: new Map(workTypes.map(w => [w.code, w.id])),
    blockTypes: new Map(blockTypes.map(b => [b.code, b.id])),
    messageTypes: new Map(messageTypes.map(m => [m.code, m.id])),
    messageStatuses: new Map(messageStatuses.map(m => [m.code, m.id])),
    platforms: new Map(platforms.map(p => [p.code, p.id])),
    priorities: new Map(priorities.map(p => [p.code, p.id])),
  };

  console.log('✅ Catalog cache initialized');
}

export function getCache(): CatalogCache {
  if (!cache) {
    throw new Error('Catalog cache not initialized. Call initCatalogCache() first.');
  }
  return cache;
}

// Getters con validación
export function getSourceId(code: string): string {
  const id = getCache().sources.get(code);
  if (!id) throw new Error(`Unknown source: ${code}`);
  return id;
}

export function getStatusId(code: string): string {
  const id = getCache().statuses.get(code);
  if (!id) throw new Error(`Unknown status: ${code}`);
  return id;
}

export function getConversationTypeId(code: string): string {
  const id = getCache().conversationTypes.get(code);
  if (!id) throw new Error(`Unknown conversation type: ${code}`);
  return id;
}

export function getBlockTypeId(code: string): string {
  const id = getCache().blockTypes.get(code);
  if (!id) throw new Error(`Unknown block type: ${code}`);
  return id;
}

export function getMessageTypeId(code: string): string {
  const id = getCache().messageTypes.get(code);
  if (!id) throw new Error(`Unknown message type: ${code}`);
  return id;
}

export function getMessageStatusId(code: string): string {
  const id = getCache().messageStatuses.get(code);
  if (!id) throw new Error(`Unknown message status: ${code}`);
  return id;
}

export function getPriorityId(code: string): string {
  const id = getCache().priorities.get(code);
  if (!id) throw new Error(`Unknown priority: ${code}`);
  return id;
}

export function getPlatformId(code: string): string | undefined {
  return getCache().platforms.get(code);
}
```

Llamar `initCatalogCache()` en `app.ts` antes de levantar el servidor:

```typescript
// app.ts
import { initCatalogCache } from './services/catalog-cache.service';

async function bootstrap() {
  await initCatalogCache();
  
  // Setup express app...
  app.listen(PORT, () => {
    console.log(`Memory Service running on port ${PORT}`);
  });
}

bootstrap();
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
  // Formato general: { claude_web: "...", claude_code: "..." }
  // Formato cuando source = CLAUDE_SDK y viene de Runtime orquestado (D-INT-04, ADDENDUM v1.1 §5.2):
  //   {
  //     runtime_run_id: string,   // UUID del run (para trazabilidad de run completo)
  //     round: number,             // Número de ronda (1, 2, ...)
  //     orchestrated: true         // Flag que indica origen Runtime
  //   }
  platformRefs      Json?
  
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
  @@index([primaryAgentId, projectId, startedAt(sort: Desc)])  // DB-OBS-05: contexto <500ms
  @@index([projectId, startedAt(sort: Desc)])
  @@index([conversationTypeId, startedAt(sort: Desc)])
  @@index([statusId])
  @@index([taskId])
  @@index([importedAt(sort: Desc)])  // DB-OBS-07: dashboard recentActivity
  @@map("conversation")
}

model ConversationTurn {
  id             String   @id @default(uuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  turnIndex      Int
  role           String   // USER, ASSISTANT, SYSTEM
  timestamp      DateTime?
  contentPreview String?  // Primeros 500 chars (D-MEM-43)
  
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

  // Constraint: evitar duplicados de entidad por conversación (DB-OBS-01)
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
  inReplyTo      String?  // messageId referenciado (soft reference, no FK)
  
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
  @@index([conversationId, timestamp(sort: Desc)])  // DB-OBS-06: último mensaje en content
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

  // PlatformCatalog
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

### 6.1 Índices Definidos

Los índices se dividen en dos categorías:

**Índices generados por Prisma** (declarados en schema.prisma):

```prisma
// Conversation
@@index([primaryAgentId, startedAt(sort: Desc)])
@@index([primaryAgentId, projectId, startedAt(sort: Desc)])  // DB-OBS-05
@@index([projectId, startedAt(sort: Desc)])
@@index([conversationTypeId, startedAt(sort: Desc)])
@@index([statusId])
@@index([taskId])
@@index([importedAt(sort: Desc)])  // DB-OBS-07

// AgentMessage
@@index([conversationId, messageStatusId])
@@index([conversationId, timestamp(sort: Desc)])  // DB-OBS-06
```

**Partial indexes (migración SQL manual):**

Prisma no soporta nativamente partial indexes con cláusula `WHERE`. Estos deben implementarse como migración SQL manual post-deploy:

```sql
-- prisma/migrations/manual/partial_indexes.sql
-- Ejecutar DESPUÉS de prisma migrate deploy

-- Timeline single-agent (excluye multi-agent donde primaryAgentId es NULL)
CREATE INDEX idx_conv_agent_time ON conversation(primary_agent_id, started_at DESC) 
  WHERE primary_agent_id IS NOT NULL;

-- Conversaciones con tarea asignada
CREATE INDEX idx_conv_task ON conversation(task_id) 
  WHERE task_id IS NOT NULL;

-- Bloques con archivo tocado
CREATE INDEX idx_block_filepath ON turn_block(file_path) 
  WHERE file_path IS NOT NULL;

-- Trazabilidad de runs completos de Runtime (ADDENDUM v1.1 §5.3)
-- Permite: SELECT ... WHERE platform_refs->>'runtime_run_id' = '...'
CREATE INDEX idx_conv_runtime_run ON conversation
  USING gin (platform_refs jsonb_path_ops)
  WHERE platform_refs IS NOT NULL;
```

Documentar en `prisma/migrations/manual/README.md`:

```markdown
# Migraciones SQL Manuales

## partial_indexes.sql

Ejecutar DESPUÉS de `prisma migrate deploy`:

```bash
psql $DATABASE_URL -f prisma/migrations/manual/partial_indexes.sql
```

Estos índices parciales no pueden declararse en schema.prisma porque Prisma
no soporta la sintaxis `WHERE` en índices.
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
      error: 'UNAUTHORIZED',
      message: 'Missing or invalid Authorization header',
    });
  }
  
  const token = authHeader.substring(7);
  
  if (token !== SERVICE_KEY) {
    return res.status(403).json({
      error: 'FORBIDDEN',
      message: 'Invalid service key',
    });
  }
  
  next();
}
```

---

## 8. API ENDPOINTS — CONTRATOS COMPLETOS

(Sin cambios respecto a v1.6 — los contratos de API permanecen iguales)

---

## 9. FLUJOS DE IMPORTACIÓN

### 9.1 Flujo TASK_EXECUTION (Single-Agent)

```typescript
// services/importer.service.ts
import { getSourceId, getStatusId, getConversationTypeId, getBlockTypeId } from './catalog-cache.service';

async function importConversation(input: ImportInput): Promise<ImportResult> {
  const { externalSessionId, agentId, agentRole, projectId, source } = input;

  // 1. Resolver IDs desde cache (no queries)
  const sourceId = getSourceId(source);
  const pendingStatusId = getStatusId('PENDING');
  const processingStatusId = getStatusId('PROCESSING');
  const importedStatusId = getStatusId('IMPORTED');
  const conversationTypeId = getConversationTypeId('TASK_EXECUTION');

  // 2. Verificar idempotencia (antes de INSERT)
  const existing = await prisma.conversation.findUnique({
    where: {
      sourceId_externalSessionId: { sourceId, externalSessionId },
    },
  });

  if (existing) {
    return { conversationId: existing.id, status: 'ALREADY_INDEXED' };
  }

  // 3. Parsear archivo (antes de crear registro)
  const parsed = await adapter.parse(input.file);

  // 4. INSERT con status PENDING
  let conversation;
  try {
    conversation = await prisma.conversation.create({
      data: {
        externalSessionId,
        sourceId,
        conversationTypeId,
        statusId: pendingStatusId,
        primaryAgentId: agentId,
        primaryAgentRole: agentRole,
        projectId,
        taskId: input.taskId,
        taskKey: input.taskKey,
        taskTitle: input.taskTitle,
        startedAt: parsed.startedAt,
        endedAt: parsed.endedAt,
      },
    });
  } catch (error: any) {
    // DB-OBS-08: Race condition — otro proceso ya insertó
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
    throw error;
  }

  // 5. UPDATE a PROCESSING antes de escribir archivo
  await prisma.conversation.update({
    where: { id: conversation.id },
    data: { statusId: processingStatusId },
  });

  try {
    // 6. Escribir archivo en /storage/
    const storagePath = await storageService.save({
      agentId,
      externalSessionId,
      startedAt: parsed.startedAt,
      file: input.file,
      logFile: input.logFile,
    });

    // 7. Transacción: persistir turns, blocks, usage, classification + status IMPORTED
    const result = await prisma.$transaction(async (tx) => {
      // Turns y Blocks usando IDs del cache
      for (const turn of parsed.turns) {
        const turnRecord = await tx.conversationTurn.create({
          data: {
            conversationId: conversation.id,
            turnIndex: turn.index,
            role: turn.role,
            timestamp: turn.timestamp,
            contentPreview: turn.content?.substring(0, 500),
          },
        });

        for (const block of turn.blocks) {
          await tx.turnBlock.create({
            data: {
              turnId: turnRecord.id,
              blockIndex: block.index,
              blockTypeId: getBlockTypeId(block.type),
              toolName: block.toolName,
              filePath: block.filePath,
              success: block.success,
              contentLength: block.contentLength,
            },
          });
        }
      }

      // Usage
      if (parsed.usage) {
        await tx.conversationUsage.create({
          data: {
            conversationId: conversation.id,
            inputTokens: parsed.usage.inputTokens,
            outputTokens: parsed.usage.outputTokens,
            cacheCreationTokens: parsed.usage.cacheCreationTokens || 0,
            cacheReadTokens: parsed.usage.cacheReadTokens || 0,
            costUsd: parsed.usage.costUsd,
            durationMs: parsed.usage.durationMs,
            modelId: parsed.usage.modelId,
          },
        });
      }

      // Clasificación
      const classification = await classifierService.classify(parsed);
      await tx.classification.create({
        data: {
          conversationId: conversation.id,
          workTypeId: classification.workTypeId,
          confidence: classification.confidence,
        },
      });

      // Topics
      for (const topicCode of classification.topics) {
        const topic = await tx.topicCatalog.findUnique({ where: { code: topicCode } });
        if (topic) {
          await tx.conversationTopic.create({
            data: { conversationId: conversation.id, topicId: topic.id },
          });
        }
      }

      // Entities (con constraint único, upsert para idempotencia)
      for (const entityName of classification.entities) {
        await tx.conversationEntity.upsert({
          where: {
            conversationId_entityName: { conversationId: conversation.id, entityName },
          },
          update: {},
          create: { conversationId: conversation.id, entityName },
        });
      }

      // UPDATE status IMPORTED
      await tx.conversation.update({
        where: { id: conversation.id },
        data: {
          statusId: importedStatusId,
          filePath: storagePath.filePath,
          logFilePath: storagePath.logFilePath,
          turnCount: parsed.turns.length,
        },
      });

      return classification;
    });

    return {
      conversationId: conversation.id,
      status: 'IMPORTED',
      turnCount: parsed.turns.length,
      startedAt: parsed.startedAt,
      endedAt: parsed.endedAt,
      classification: result,
    };
  } catch (error) {
    // AMB-07: Delegar siempre al cleanup job, no intentar mover a ERROR aquí
    // El registro queda en PROCESSING para que el cleanup lo detecte
    console.error('Import failed:', error);
    throw error;
  }
}
```

### 9.2 Flujo AGENT_REVIEW (Multi-Agent)

```typescript
// services/importer.service.ts
import {
  getSourceId,
  getStatusId,
  getConversationTypeId,
  getMessageTypeId,
  getMessageStatusId,
  getPriorityId,
  getPlatformId,
} from './catalog-cache.service';

async function importAgentReview(input: ImportReviewInput): Promise<ImportResult> {
  const { externalSessionId, projectId, participants } = input;

  // 1. Resolver IDs desde cache
  const sourceId = getSourceId('VTT_CHANNEL');
  const pendingStatusId = getStatusId('PENDING');
  const processingStatusId = getStatusId('PROCESSING');
  const importedStatusId = getStatusId('IMPORTED');
  const conversationTypeId = getConversationTypeId(input.conversationType);

  // 2. Verificar idempotencia
  const existing = await prisma.conversation.findUnique({
    where: {
      sourceId_externalSessionId: { sourceId, externalSessionId },
    },
    include: {
      messages: { select: { messageId: true } },
    },
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

    // DB-OBS-03 CORREGIDO: Pre-fetch catálogos ANTES del loop
    // (Los IDs ya están en cache, solo validamos que existen los codes)
    
    // Insertar nuevos mensajes usando IDs del cache
    await prisma.$transaction(async (tx) => {
      for (const msg of newMessages) {
        await tx.agentMessage.create({
          data: {
            conversationId: existing.id,
            messageId: msg.messageId,
            inReplyTo: msg.inReplyTo,
            fromAgentId: msg.fromAgentId,
            toAgentId: msg.toAgentId,
            messageTypeId: getMessageTypeId(msg.messageType),
            messageStatusId: getMessageStatusId(msg.messageStatus),
            priorityId: getPriorityId(msg.priority),
            topic: msg.topic,
            body: msg.body,
            expectedOutput: msg.expectedOutput,
            timestamp: msg.timestamp,
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
  let conversation;
  try {
    conversation = await prisma.conversation.create({
      data: {
        externalSessionId,
        sourceId,
        conversationTypeId,
        statusId: pendingStatusId,
        primaryAgentId: null, // NULL para multi-agent
        projectId,
        taskId: input.taskId,
        taskKey: input.taskKey,
        taskTitle: input.taskTitle,
        reviewRound: input.reviewRound,
        startedAt: parsed.startedAt,
        endedAt: parsed.endedAt,
      },
    });
  } catch (error: any) {
    // DB-OBS-08: Race condition
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
    throw error;
  }

  // 5. UPDATE a PROCESSING
  await prisma.conversation.update({
    where: { id: conversation.id },
    data: { statusId: processingStatusId },
  });

  try {
    // 6. Escribir archivo
    const storagePath = await storageService.saveReview({
      projectId,
      externalSessionId,
      startedAt: parsed.startedAt,
      file: input.file,
    });

    // 7. Persistir participants y messages usando IDs del cache
    await prisma.$transaction(async (tx) => {
      // Participants
      for (const p of participants) {
        const platformId = p.platform ? getPlatformId(p.platform) : null;
        await tx.conversationParticipant.create({
          data: {
            conversationId: conversation.id,
            agentId: p.agentId,
            agentRole: p.agentRole,
            platformId,
          },
        });
      }

      // Messages (DB-OBS-03 CORREGIDO: usando cache, no queries en loop)
      for (const msg of parsed.messages) {
        await tx.agentMessage.create({
          data: {
            conversationId: conversation.id,
            messageId: msg.messageId,
            inReplyTo: msg.inReplyTo,
            fromAgentId: msg.fromAgentId,
            toAgentId: msg.toAgentId,
            messageTypeId: getMessageTypeId(msg.messageType),
            messageStatusId: getMessageStatusId(msg.messageStatus),
            priorityId: getPriorityId(msg.priority),
            topic: msg.topic,
            body: msg.body,
            expectedOutput: msg.expectedOutput,
            timestamp: msg.timestamp,
          },
        });
      }

      // UPDATE status IMPORTED
      await tx.conversation.update({
        where: { id: conversation.id },
        data: {
          statusId: importedStatusId,
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
    // AMB-07: Delegar al cleanup job
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
import { getStatusId } from '../services/catalog-cache.service';

const STALE_THRESHOLD_MINUTES = 10;
const MAX_RETRIES = 3;

// Ejecutar cada 5 minutos
cron.schedule('*/5 * * * *', async () => {
  console.log('[Cleanup] Starting cleanup job...');

  const staleThreshold = new Date(Date.now() - STALE_THRESHOLD_MINUTES * 60 * 1000);

  // DB-OBS-02 CORREGIDO: Usar statusId directamente (no status.code)
  // Los IDs vienen del cache inicializado en startup
  const pendingStatusId = getStatusId('PENDING');
  const processingStatusId = getStatusId('PROCESSING');
  const errorStatusId = getStatusId('ERROR');

  // Buscar conversaciones stuck en PENDING o PROCESSING
  const staleConversations = await prisma.conversation.findMany({
    where: {
      statusId: { in: [pendingStatusId, processingStatusId] },
      updatedAt: { lt: staleThreshold },
      retryCount: { lte: MAX_RETRIES },
    },
  });

  for (const conv of staleConversations) {
    const currentStatus = conv.statusId === pendingStatusId ? 'PENDING' : 'PROCESSING';
    console.log(`[Cleanup] Processing stale conversation: ${conv.id} (status: ${currentStatus}, retries: ${conv.retryCount})`);

    if (conv.retryCount >= MAX_RETRIES) {
      // Marcar como ERROR definitivo (ya llegó al límite)
      await prisma.conversation.update({
        where: { id: conv.id },
        data: {
          statusId: errorStatusId,
          errorMessage: `Max retries (${MAX_RETRIES}) exceeded`,
        },
      });
      console.log(`[Cleanup] Marked as ERROR (max retries): ${conv.id}`);
    } else {
      // Incrementar retry y volver a PENDING para reprocesar
      await prisma.conversation.update({
        where: { id: conv.id },
        data: {
          statusId: pendingStatusId,
          retryCount: conv.retryCount + 1,
          errorMessage: null,
        },
      });
      console.log(`[Cleanup] Reset to PENDING (retry ${conv.retryCount + 1}): ${conv.id}`);

      // NOTA: El reproceso real (re-leer archivo, re-parsear) queda fuera de alcance R1.
      // El registro vuelve a PENDING pero sin trigger automático.
      // Conversaciones en ERROR aparecen en GET /dashboard/stats → errorsToReview.
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
import { getStatusId } from './catalog-cache.service';

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
    } catch (error: any) {
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
    // Usar statusId del cache (no query a BD)
    const importedStatusId = getStatusId('IMPORTED');

    const [recentSessions, taskRelated, topicRelated, reviews, files, cost] = await Promise.all([
      // Sesiones recientes del agente EN ESTE PROYECTO
      prisma.conversation.findMany({
        where: {
          primaryAgentId: input.agentId,
          projectId: input.projectId,
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
              projectId: input.projectId,
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
          projectId: input.projectId,
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

(Sin cambios respecto a v1.6 — código de clasificación permanece igual)

---

## 13. ALMACENAMIENTO DE ARCHIVOS

### 13.1 Storage Service

```typescript
// services/storage.service.ts
import * as fs from 'fs/promises';
import * as path from 'path';
import dayjs from 'dayjs';

const STORAGE_PATH = process.env.STORAGE_PATH || '/storage';

interface SaveInput {
  agentId: string;
  externalSessionId: string;
  startedAt: Date;
  file: Buffer;
  logFile?: Buffer;
}

interface SaveReviewInput {
  projectId: string;
  externalSessionId: string;
  startedAt: Date;
  file: Buffer;
}

export const storageService = {
  // TASK_EXECUTION: /storage/{agentId}/{YYYY-MM}/{sessionId}/
  async save(input: SaveInput): Promise<{ filePath: string; logFilePath?: string }> {
    const month = dayjs(input.startedAt).format('YYYY-MM');
    const dir = path.join(STORAGE_PATH, input.agentId, month, input.externalSessionId);
    
    await fs.mkdir(dir, { recursive: true });
    
    const filePath = path.join(dir, 'session.json');
    await fs.writeFile(filePath, input.file);
    
    let logFilePath: string | undefined;
    if (input.logFile) {
      logFilePath = path.join(dir, 'log.jsonl');
      await fs.writeFile(logFilePath, input.logFile);
    }
    
    return { filePath, logFilePath };
  },

  // AGENT_REVIEW: /storage/_reviews/{projectId}/{YYYY-MM}/{sessionId}/
  async saveReview(input: SaveReviewInput): Promise<{ filePath: string }> {
    const month = dayjs(input.startedAt).format('YYYY-MM');
    const dir = path.join(STORAGE_PATH, '_reviews', input.projectId, month, input.externalSessionId);
    
    await fs.mkdir(dir, { recursive: true });
    
    const filePath = path.join(dir, 'channel.md');
    await fs.writeFile(filePath, input.file);
    
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

> ⚠️ **§14 OBSOLETA — NO USAR COMO FUENTE DE PLANIFICACIÓN.**
>
> El plan original de esta sección (150h = 76h BE + 74h UI) **queda superado**.
>
> **Plan vigente (decisión PM 2026-04-21):** `memory-service-project/Release2.0/PJM/HO_ACTUALIZAR_TAREAS_VTT.md` (v2.1, 2026-04-21)
> — **116 tareas, 381h, 10 fases** cargadas en VTT (Project ID `51e169f7-8a23-4628-8b78-04864b633ac7`).
>
> Esta sección se conserva como histórico de la estimación inicial producida durante la consolidación SA. Cualquier referencia operativa a "sprints S01..S06" debe leerse como nomenclatura interna del SPEC, no como el plan de ejecución real.

### 14.1 Tareas por Sprint (HISTÓRICO — ver HO v2.1 para plan real)

| Sprint | Tarea | Horas | Owner |
|--------|-------|-------|-------|
| **S01** | Schema Prisma v1.7 + migraciones + partial indexes SQL | 4h | DB |
| **S01** | Seed de catálogos | 2h | DB |
| **S01** | Setup proyecto + catalog-cache.service | 3h | BE |
| **S01** | POST /import — CLI adapter + storage + manejo P2002 | 6h | BE |
| **S02** | POST /import — SDK adapter (2 archivos, costo) | 4h | BE |
| **S02** | GET /agents/:id/timeline (single + multi-agent) | 4h | BE |
| **S02** | Clasificación por reglas | 4h | BE |
| **S03** | GET /conversations/:id/content (lee desde /storage/) | 4h | BE |
| **S03** | GET /context (<500ms, fail-fast, usa cache) | 5h | BE |
| **S03** | Tests de rendimiento contexto (<500ms) | 3h | QA |
| **S04** | POST /import-review (VTT_CHANNEL, multi-agent, prefetch corregido) | 6h | BE |
| **S04** | POST /import — Web + ChatGPT adapters | 4h | BE |
| **S04** | Cleanup job (usa statusId, no status.code) | 2h | BE |
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
| Design Lead (DL) | 28h |
| Frontend (FE) | 46h |
| **TOTAL UI** | **74h** |
| **TOTAL PROYECTO** | **150h** |

---

## 15. CRITERIOS DE ACEPTACIÓN

### 15.1 Funcionales

- [ ] Import TASK_EXECUTION retorna conversationId, status IMPORTED, timestamps reales
- [ ] Import AGENT_REVIEW soporta múltiples participantes, primaryAgentId = NULL
- [ ] Import incremental VTT_CHANNEL agrega solo mensajes nuevos
- [ ] Import duplicado retorna ALREADY_INDEXED sin error
- [ ] Import concurrente (race condition P2002) retorna ALREADY_INDEXED
- [ ] Timeline incluye conversaciones single-agent y participaciones multi-agent
- [ ] Content retorna estructura correcta para ambos tipos (lee desde /storage/)
- [ ] Contexto responde en <500ms o retorna error 504
- [ ] Cost-report suma correctamente por proyecto/agente
- [ ] Clasificación detecta topics, workType, entities
- [ ] Dashboard stats muestra totales y errores pendientes

### 15.2 Técnicos

- [ ] Schema Prisma v1.7 sin errores de migración
- [ ] Partial indexes aplicados via SQL manual
- [ ] Todos los catálogos seedeados (incl. VTT_CHANNEL, GOOGLE_DOCS)
- [ ] Catalog cache inicializado en startup
- [ ] Storage organizado por fecha REAL de sesión
- [ ] Cleanup job ejecuta cada 5 min con statusId (no status.code)
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

### 17.1 Arquitectura

| Aspecto | Valor |
|---------|-------|
| **Tipo** | SPA standalone |
| **Puerto** | 3003 |
| **API** | Consume `http://{host}:3002/api/...` |
| **Stack** | React 18 + TypeScript + Vite + TailwindCSS |
| **Deploy** | Nginx en VM, container separado |
| **Auth R1** | Sin autenticación — acceso directo |

### 17.2 Pantallas por Prioridad

| Prioridad | Pantalla | Descripción |
|-----------|----------|-------------|
| **P0** | Agent Timeline | Historial cronológico de un agente |
| **P0** | Conversation Viewer (TASK_EXECUTION) | Turns + tool calls de sesión de trabajo |
| **P1** | Dashboard | Métricas globales, actividad reciente, errores |
| **P1** | Cost Report Proyecto | Costos por agente, top tareas |
| **P1** | Import Manual | Formulario upload de conversaciones |
| **P2** | Conversation Viewer (AGENT_REVIEW) | Thread multi-agente con badges |
| **P2** | Lista/Búsqueda | Browse con filtros |
| **P3** | Cost Report Agente | Costos por semana, workType |
| **P3** | Health Page | Estado del servicio |

### 17.3 Plan de Implementación — Design Lead (DL)

**BLOQUEANTE:** FE no puede iniciar S-UI-01 sin handoff de DL.

| Sprint | Tarea | Horas | Owner |
|--------|-------|-------|-------|
| **S-DL-01** | Design System tokens (paleta, tipografía, espaciado) — separado de VTT | 4h | DL |
| **S-DL-01** | Wireframes: Dashboard | 3h | DL |
| **S-DL-01** | Wireframes: Agent Timeline | 3h | DL |
| **S-DL-02** | Wireframes: Conversation Viewer (TASK_EXECUTION) | 4h | DL |
| **S-DL-02** | Wireframes: Conversation Viewer (AGENT_REVIEW) | 4h | DL |
| **S-DL-03** | Wireframes: Import Manual | 2h | DL |
| **S-DL-03** | Wireframes: Cost Reports (Proyecto + Agente) | 3h | DL |
| **S-DL-03** | Wireframes: Lista/Búsqueda + Health | 2h | DL |
| **S-DL-04** | UX Spec completo (medidas, estados, interacciones) | 3h | DL |
| | **TOTAL DL** | **28h** | |

### 17.4 Plan de Implementación — Frontend (FE)

**DEPENDENCIA:** Inicia después de S-DL-04 (handoff DL).

| Sprint | Tarea | Horas | Owner |
|--------|-------|-------|-------|
| **S-UI-01** | Setup proyecto (React + Vite + Tailwind + tokens DL) | 2h | FE |
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
| | **TOTAL FE** | **46h** | |

### 17.5 Entregables DL

| Entregable | Formato | Descripción |
|------------|---------|-------------|
| Design System tokens | CSS/Tailwind config | Paleta, tipografía, espaciado, radii — independiente de VTT |
| Wireframes | Figma / HTML estático | Todas las pantallas P0-P3 |
| UX Spec | Markdown + anotaciones | Handoff para FE: medidas exactas, estados (loading, empty, error), interacciones |

### 17.6 Resumen Horas UI

| Rol | Horas |
|-----|-------|
| Design Lead (DL) | 28h |
| Frontend (FE) | 46h |
| **TOTAL UI** | **74h** |

---

**Documento:** SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md  
**Versión:** 1.9  
**Estado:** ✅ APROBADO PM — CIERRE FINAL  
**Consolidador:** SA-Agent (v1.7) + PM (v1.9)  
**Firma cierre:** PM Martin Rivas — 2026-04-21  

---

*Documento relacionado: METODOLOGIA_MEMORY_SERVICE_v1.2.md*  
*Addendum integrado: ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md (§5.2 y §5.3 incorporados en §4.1 y §6.1)*  
*Plan de ejecución vigente: HO_ACTUALIZAR_TAREAS_VTT.md v2.1 (sustituye §14)*
