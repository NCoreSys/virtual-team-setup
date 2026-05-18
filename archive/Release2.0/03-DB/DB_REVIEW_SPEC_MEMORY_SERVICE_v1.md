# REVISIÓN DB: SPEC_MEMORY_SERVICE v1.5

**Revisor:** DB Engineer (`a3a2ce62-28d8-419d-9888-44203a963894`)
**Fecha:** 2026-04-12
**Documento revisado:** SPEC_MEMORY_SERVICE_v1.5.md (internamente v1.4)
**Alcance:** Validación DB — modelo, constraints, índices, migraciones, cleanup job, integridad
**Resultado:** ✅ APROBADO CON OBSERVACIONES (1 bloqueante, 4 medianas, 3 menores)

---

## 1. RESUMEN EJECUTIVO

El modelo de datos es sólido en su estructura central. Las 10 tablas de catálogo más las 9 entidades principales están bien normalizadas y las relaciones con cascade delete son correctas. Las constraints de unicidad clave (D-MEM-41, D-MEM-42) están correctamente declaradas.

Se identifican **8 observaciones** ordenadas por severidad:

| ID | Severidad | Categoría | Resumen |
|----|-----------|-----------|---------|
| **DB-OBS-01** | BLOQUEANTE | Integridad | ConversationEntity sin constraint único — riesgo real de duplicados en retry |
| **DB-OBS-02** | MEDIA | Performance | Cleanup job filtra por `status.code` — no usa `idx_conv_status` eficientemente |
| **DB-OBS-03** | MEDIA | Performance | N+1 en importAgentReview — catalog lookups dentro del loop de messages |
| **DB-OBS-04** | MEDIA | Migración | Partial indexes en §6 no tienen equivalente en schema.prisma — migración generará indexes full |
| **DB-OBS-05** | MEDIA | Performance | Falta índice compuesto `(primaryAgentId, projectId)` — queries recentSessions y frequentFiles pueden ser lentas en escala |
| **DB-OBS-06** | MENOR | Performance | Falta índice en `AgentMessage(conversationId, timestamp DESC)` — query de último mensaje en content endpoint |
| **DB-OBS-07** | MENOR | Performance | Falta índice en `Conversation(importedAt)` — dashboard recentActivity sin cobertura |
| **DB-OBS-08** | MENOR | Integridad | Race condition en idempotencia — error P2002 no manejado explícitamente en flujos import |

---

## 2. VALIDACIÓN: MODELO DE DATOS Y RELACIONES

### 2.1 Catálogos (10 tablas) CORRECTO

Todos los catálogos tienen `code String @unique` como identificador natural. Las back-relations están declaradas correctamente en cada catálogo. Pattern correcto y consistente.

| Catálogo | FK usada por | Estado |
|----------|-------------|--------|
| SourceCatalog | Conversation.sourceId | OK |
| ConversationTypeCatalog | Conversation.conversationTypeId | OK |
| ConversationStatusCatalog | Conversation.statusId | OK |
| WorkTypeCatalog | Classification.workTypeId | OK |
| BlockTypeCatalog | TurnBlock.blockTypeId | OK |
| MessageTypeCatalog | AgentMessage.messageTypeId | OK |
| MessageStatusCatalog | AgentMessage.messageStatusId | OK |
| PlatformCatalog | ConversationParticipant.platformId | OK |
| TopicCatalog | ConversationTopic.topicId | OK |
| PriorityCatalog | AgentMessage.priorityId | OK |

### 2.2 Entidades principales (9 tablas) CORRECTO con observación

| Tabla | Relación | Cascade | Estado |
|-------|----------|---------|--------|
| Conversation | Central | — | OK |
| ConversationTurn | N:1 → Conversation | onDelete:Cascade | OK |
| TurnBlock | N:1 → ConversationTurn | onDelete:Cascade | OK |
| ConversationUsage | 1:1 → Conversation | onDelete:Cascade | OK |
| Classification | 1:1 → Conversation | onDelete:Cascade | OK |
| ConversationTopic | Join Conversation×TopicCatalog | onDelete:Cascade | OK |
| ConversationEntity | N:1 → Conversation | onDelete:Cascade | VER DB-OBS-01 |
| ConversationParticipant | N:1 → Conversation | onDelete:Cascade | OK |
| AgentMessage | N:1 → Conversation | onDelete:Cascade | OK |

**Nota positiva:** `AgentMessage.inReplyTo` es `String?` (referencia soft a `messageId`, no FK). Correcto para R1 — no hay riesgo de FK violation si un mensaje se elimina.

---

## 3. VALIDACIÓN: CONSTRAINTS Y UNICIDADES

### 3.1 Constraints declaradas — todas correctas

| Constraint | Tabla | Decisión | Estado |
|------------|-------|----------|--------|
| `@@unique([sourceId, externalSessionId])` | Conversation | D-MEM-42 | OK |
| `@@unique([conversationId, turnIndex])` | ConversationTurn | D-MEM-41 | OK |
| `@@unique([turnId, blockIndex])` | TurnBlock | D-MEM-41 | OK |
| `@@unique([conversationId, agentId])` | ConversationParticipant | — | OK |
| `@@unique([conversationId, messageId])` | AgentMessage | — | OK |
| `conversationId @unique` | ConversationUsage | — | OK (1:1) |
| `conversationId @unique` | Classification | — | OK (1:1) |
| `@@id([conversationId, topicId])` | ConversationTopic | — | OK (PK compuesta evita duplicados) |

El nombre del constraint para `findUnique` será `sourceId_externalSessionId`. El código en §9.1 lo usa correctamente:
```typescript
where: { sourceId_externalSessionId: { sourceId: sourceRecord.id, externalSessionId } }
```
Alineado.

### 3.2 DB-OBS-01 — ConversationEntity sin constraint único — BLOQUEANTE

**Modelo actual:**
```prisma
model ConversationEntity {
  id             String   @id @default(uuid())
  conversationId String
  entityName     String
  @@index([conversationId])
}
```

**Problema:** No hay `@@unique([conversationId, entityName])`. Si el clasificador se ejecuta en un retry (conversación vuelve de PROCESSING → PENDING → reimport), insertará las mismas entidades duplicadas.

**Escenario real de riesgo:**
```
1. Import → classifierService inserta "AuthService", "PrismaClient"
2. Falla al escribir archivo → queda en PROCESSING
3. Cleanup lo resetea a PENDING
4. Reimport → classifierService inserta "AuthService", "PrismaClient" otra vez
5. Resultado: entidades duplicadas por conversación
```

**Corrección requerida en schema.prisma:**
```prisma
model ConversationEntity {
  id             String   @id @default(uuid())
  conversationId String
  entityName     String

  @@unique([conversationId, entityName])   // AGREGAR
  @@index([conversationId])
  @@map("conversation_entity")
}
```

Alternativamente, usar `upsert` en classifierService en lugar de `create`. La constraint en BD es la corrección más robusta porque protege incluso ante bugs de aplicación.

---

## 4. VALIDACIÓN: ÍNDICES VS QUERIES REALES

### 4.1 DB-OBS-04 — Partial indexes en §6 vs schema.prisma — MEDIA

**Inconsistencia:** §6 documenta partial indexes con `WHERE ... IS NOT NULL`. El schema.prisma usa `@@index([primaryAgentId, startedAt(sort: Desc)])` sin condición.

`prisma migrate deploy` generará indexes FULL, no parciales. Los comentarios en §6 quedan desincronizados con la migración real.

Prisma soporta partial indexes desde v4.6:
```prisma
@@index([primaryAgentId, startedAt(sort: Desc)], where: { primaryAgentId: { not: null } })
@@index([taskId], where: { taskId: { not: null } })
```

**Opción para implementador:** Actualizar schema.prisma con la sintaxis Prisma de partial index, o crear los partial indexes en una migración SQL manual post-deploy. Decidir y documentar antes de S01.

### 4.2 DB-OBS-05 — Falta índice compuesto `(primaryAgentId, projectId)` — MEDIA (impacta <500ms)

**Query recentSessions (§11):**
```typescript
where: {
  primaryAgentId: input.agentId,
  projectId: input.projectId,
  statusId: importedStatusId,
},
orderBy: { startedAt: 'desc' },
```

El índice actual `(primaryAgentId, startedAt DESC)` no incluye `projectId`. Un agente con conversaciones en múltiples proyectos genera scans adicionales para filtrar por proyecto.

**Query frequentFiles groupBy (§11):**
```typescript
turn: {
  conversation: {
    primaryAgentId: input.agentId,
    projectId: input.projectId,
    statusId: importedStatusId,
  },
},
```

Join profundo TurnBlock → ConversationTurn → Conversation. La Conversation se filtra por `(primaryAgentId, projectId)`. Sin índice compuesto puede requerir seq scan post-join.

**Corrección recomendada:**
```prisma
// Reemplazar o agregar junto al existente
@@index([primaryAgentId, projectId, startedAt(sort: Desc)])
```

Este índice cubre tanto `recentSessions` como el filtro del `frequentFiles groupBy` y es crítico para el requisito de <500ms.

### 4.3 DB-OBS-06 — Falta índice en AgentMessage timestamp — MENOR

**Query afectada (§11, reviews):**
```typescript
messages: {
  take: 1,
  orderBy: { timestamp: 'desc' },
}
```

El índice `@@index([conversationId, messageStatusId])` no cubre ORDER BY `timestamp DESC`. PostgreSQL necesita sort sobre todos los mensajes de la conversación para encontrar el más reciente.

**Corrección:**
```prisma
@@index([conversationId, timestamp(sort: Desc)])
```

### 4.4 DB-OBS-07 — Falta índice en importedAt para dashboard — MENOR

`GET /api/dashboard/stats` → `recentActivity` requiere ORDER BY `importedAt DESC`. Sin índice → seq scan + sort en toda la tabla `conversation`.

**Corrección:**
```prisma
@@index([importedAt(sort: Desc)])
```

---

## 5. VALIDACIÓN: VIABILIDAD DE MIGRACIONES

### 5.1 Aislamiento de BD — Correcto

`memory_service_db` es completamente independiente de `virtual_teams_tracking_db`. Sin FK cross-database, sin tablas conflictivas, sin naming collision. Las migraciones son autónomas.

### 5.2 Tipos de datos — Correctos

| Campo | Tipo Prisma | Tipo PostgreSQL | Estado |
|-------|------------|-----------------|--------|
| IDs | `String @id @default(uuid())` | TEXT (UUID app-generated) | OK |
| costUsd | `Decimal @db.Decimal(10, 6)` | DECIMAL(10,6) | OK |
| platformRefs | `Json?` | JSONB | OK |
| Timestamps | `DateTime @default(now())` | TIMESTAMP(3) | OK |

**Nota IDs:** El proyecto usa `@default(uuid())` (Prisma genera en app layer) vs el patrón VTT `@default(dbgenerated("gen_random_uuid()::text"))` (DB genera). Ambos producen UUID strings en TEXT. Para el Memory Service como proyecto independiente, el enfoque Prisma es válido y consistente internamente.

**Nota costUsd:** `_sum: { costUsd: true }` en Prisma retorna `Prisma.Decimal`. El código usa `Number(cost._sum.costUsd || 0)` que es la conversión correcta.

### 5.3 Instrucción crítica: usar `prisma migrate` no `prisma db push`

El plan §14 indica correctamente "Schema Prisma v1.4 + migraciones" para S01. Confirmar que el Memory Service use `prisma migrate dev` para generar migraciones formales. No repetir el patrón S09 de VTT (db push sin migración).

---

## 6. VALIDACIÓN: CLEANUP JOB Y CONSISTENCIA DE QUERIES

### 6.1 Lógica de retry — Correcta

| retryCount al entrar | Condición lte 3 | Condición >= 3 | Acción | retryCount al salir |
|---------------------|-----------------|---------------|--------|---------------------|
| 0 | incluido | No | PENDING + retry++ | 1 |
| 1 | incluido | No | PENDING + retry++ | 2 |
| 2 | incluido | No | PENDING + retry++ | 3 |
| 3 | incluido | Sí | ERROR definitivo | 3 |

3 reintentos efectivos antes de ERROR. Consistente con D-MEM-35 y D-MEM-40. Lógica correcta.

`@updatedAt` se resetea en cada `update()`, lo que reinicia el timer de 10 minutos correctamente en cada retry.

### 6.2 DB-OBS-02 — Cleanup job filtra por status.code, no statusId — MEDIA

**Código actual:**
```typescript
const staleConversations = await prisma.conversation.findMany({
  where: {
    status: {
      code: { in: ['PENDING', 'PROCESSING'] },  // filtro por relación
    },
    updatedAt: { lt: staleThreshold },
    retryCount: { lte: MAX_RETRIES },
  },
  include: { status: true },
});
```

**Problema técnico:** Filtra por `status.code` (campo del catálogo relacionado). Prisma genera JOIN o subquery. El `idx_conv_status (status_id, updated_at)` no se usa directamente porque la condición es sobre `code`, no sobre `status_id`.

**Problema adicional:** Dentro del loop hace 2 catalog lookups por conversación (errorStatus + pendingStatus), que podrían hacerse una vez antes del loop.

**Corrección recomendada:**
```typescript
// Al inicio del job (una vez):
const [pendingRecord, processingRecord, errorRecord, pendingStatusForRetry] = await Promise.all([
  prisma.conversationStatusCatalog.findUnique({ where: { code: 'PENDING' } }),
  prisma.conversationStatusCatalog.findUnique({ where: { code: 'PROCESSING' } }),
  prisma.conversationStatusCatalog.findUnique({ where: { code: 'ERROR' } }),
]);

// En el cron — usa statusId directamente (aprovecha idx_conv_status):
const staleConversations = await prisma.conversation.findMany({
  where: {
    statusId: { in: [pendingRecord!.id, processingRecord!.id] },
    updatedAt: { lt: staleThreshold },
    retryCount: { lte: MAX_RETRIES },
  },
});

// Loop sin catalog lookups adicionales
for (const conv of staleConversations) {
  if (conv.retryCount >= MAX_RETRIES) {
    await prisma.conversation.update({
      where: { id: conv.id },
      data: { statusId: errorRecord!.id, errorMessage: `Max retries exceeded` },
    });
  } else {
    await prisma.conversation.update({
      where: { id: conv.id },
      data: { statusId: pendingRecord!.id, retryCount: conv.retryCount + 1, errorMessage: null },
    });
  }
}
```

### 6.3 DB-OBS-03 — N+1 en importAgentReview — MEDIA

**Código actual (§9.2):**
```typescript
for (const msg of parsed.messages) {
  await tx.agentMessage.create({
    data: {
      messageTypeId: (await tx.messageTypeCatalog.findUnique({ where: { code: msg.messageType } }))!.id,
      messageStatusId: (await tx.messageStatusCatalog.findUnique({ where: { code: msg.messageStatus } }))!.id,
      priorityId: (await tx.priorityCatalog.findUnique({ where: { code: msg.priority } }))!.id,
      ...
    },
  });
}
```

3 catalog lookups × N mensajes dentro de la transacción. Para 10 mensajes = 30 lookups + 10 inserts = 40 queries.

**Corrección:**
```typescript
// Antes del loop
const [messageTypeRows, messageStatusRows, priorityRows] = await Promise.all([
  tx.messageTypeCatalog.findMany(),
  tx.messageStatusCatalog.findMany(),
  tx.priorityCatalog.findMany(),
]);
const typeMap = new Map(messageTypeRows.map(r => [r.code, r.id]));
const statusMap = new Map(messageStatusRows.map(r => [r.code, r.id]));
const priorityMap = new Map(priorityRows.map(r => [r.code, r.id]));

for (const msg of parsed.messages) {
  await tx.agentMessage.create({
    data: {
      messageTypeId: typeMap.get(msg.messageType)!,
      messageStatusId: statusMap.get(msg.messageStatus)!,
      priorityId: priorityMap.get(msg.priority)!,
      ...
    },
  });
}
```

Total: 3 fetches + N inserts en lugar de 3N + N.

---

## 7. RIESGOS DE INTEGRIDAD Y COMPATIBILIDAD

### 7.1 DB-OBS-08 — Race condition en idempotencia — MENOR

Entre el `findUnique` (paso 1) y el `create` (paso 4) dos requests concurrentes pueden pasar el check simultáneamente. La `@@unique` capturará el segundo como error Prisma P2002. El código actual no lo maneja explícitamente.

**Corrección:**
```typescript
try {
  const conversation = await prisma.conversation.create({ data: {...} });
} catch (error: any) {
  if (error.code === 'P2002') {
    const existing = await prisma.conversation.findUnique({
      where: { sourceId_externalSessionId: { sourceId: sourceRecord.id, externalSessionId } }
    });
    return { conversationId: existing!.id, status: 'ALREADY_INDEXED' };
  }
  throw error;
}
```

### 7.2 Riesgos menores aceptables para R1

| # | Riesgo | Estado |
|---|--------|--------|
| A | AgentMessage.inReplyTo es String?, no FK | Aceptable R1 — validar en app layer |
| B | Timeline multi-agent requiere OR + subquery de participants | Aceptable R1 por volumen bajo |
| C | `totalMessages` en UPDATED response puede ser inexacto (usa .length, no COUNT) | Impacto cosmético únicamente |

---

## 8. CAMBIOS RECOMENDADOS EN schema.prisma

### 8.1 DB-OBS-01 — Agregar antes de S01 (BLOQUEANTE)

```prisma
model ConversationEntity {
  id             String   @id @default(uuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  entityName     String

  @@unique([conversationId, entityName])   // AGREGAR
  @@index([conversationId])
  @@map("conversation_entity")
}
```

### 8.2 DB-OBS-05 — Agregar antes de S03 (impacta <500ms)

```prisma
model Conversation {
  ...
  @@index([primaryAgentId, startedAt(sort: Desc)])              // existente (mantener o reemplazar)
  @@index([primaryAgentId, projectId, startedAt(sort: Desc)])   // AGREGAR
  @@index([projectId, startedAt(sort: Desc)])                   // existente
  @@index([conversationTypeId, startedAt(sort: Desc)])          // existente
  @@index([statusId])                                            // existente
  @@index([taskId])                                              // existente
  @@index([importedAt(sort: Desc)])                             // AGREGAR (DB-OBS-07)
  ...
}
```

### 8.3 DB-OBS-06 — Agregar antes de S04

```prisma
model AgentMessage {
  ...
  @@unique([conversationId, messageId])
  @@index([conversationId, messageStatusId])                    // existente
  @@index([conversationId, timestamp(sort: Desc)])             // AGREGAR
  @@map("agent_message")
}
```

---

## 9. RESUMEN EJECUTIVO DE VEREDICTO

| Área | Estado | Notas |
|------|--------|-------|
| Modelo de datos y relaciones | CORRECTO | Cascade delete correcto en todas las entidades |
| Constraints y unicidades | CON CORRECCIÓN | DB-OBS-01 es bloqueante (ConversationEntity) |
| Índices vs queries | CON MEJORAS | DB-OBS-05 impacta requisito <500ms |
| Viabilidad de migraciones | VIABLE | BD aislada, tipos correctos, usar migrate no db push |
| Cleanup job | CON MEJORAS | Funcional pero subóptimo (DB-OBS-02) |
| Integridad / performance | ACEPTABLE R1 | Con correcciones DB-OBS-01 y DB-OBS-08 |

---

## 10. RESULTADO FINAL

### APROBADO CON OBSERVACIONES

**Condición bloqueante para avance a S01:**
- DB-OBS-01 debe corregirse en schema.prisma antes de generar la migración inicial

**Observaciones medianas — corregir antes del sprint indicado:**
- DB-OBS-05: antes de S03 (implementación GET /context)
- DB-OBS-02 y DB-OBS-03: antes de S04 (cleanup job e importAgentReview)
- DB-OBS-04: decisión de implementador antes de S01

**Observaciones menores — corregir en sprint correspondiente:**
- DB-OBS-06: antes de S04 (AgentMessage content)
- DB-OBS-07: antes de S05 (dashboard stats)
- DB-OBS-08: antes de S01 (manejo P2002)

---

**Documento:** DB_REVIEW_SPEC_MEMORY_SERVICE_v1.md
**Revisor:** DB Engineer
**Fecha:** 2026-04-12
**Estado:** COMPLETADO
