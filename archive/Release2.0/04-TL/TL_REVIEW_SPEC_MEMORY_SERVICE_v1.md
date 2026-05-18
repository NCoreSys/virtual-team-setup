reporte T# REVISIÓN TL: SPEC_MEMORY_SERVICE v1.5

**Revisor:** Tech Lead (TL-Agent `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8`)
**Fecha:** 2026-04-12
**Documento revisado:** SPEC_MEMORY_SERVICE_v1.5.md (internamente v1.4)
**Documentos de entrada:** METODOLOGIA_MEMORY_SERVICE_v1.2.md, AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md, DB_REVIEW_SPEC_MEMORY_SERVICE_v1.md
**Alcance:** Viabilidad técnica e implementabilidad dentro del flujo Fase 3B
**Resultado:** VIABLE CON AJUSTES REQUERIDOS ANTES DE S01

---

## 1. VEREDICTO GENERAL

**VIABLE CON AJUSTES**

La spec está en condiciones de pasar a implementación una vez resueltos los puntos indicados en este documento. El diseño central es sólido: la separación single-agent / multi-agent es coherente, el modelo de datos está normalizado correctamente, los contratos de API son completos y consistentes con los flujos de importación, y el requisito <500ms tiene un mecanismo de fail-fast implementable.

Los ajustes requeridos son concretos y acotados. Ninguno implica rediseño arquitectónico. El bloqueante DB-OBS-01 debe incorporarse en el schema antes de ejecutar la migración inicial S01. Los demás deben resolverse en los sprints indicados por DB.

No se reabre revisión arquitectónica ni de modelo de datos. Las decisiones D-MEM-01 a D-MEM-42 se consideran cerradas para esta revisión.

---

## 2. FLUJOS Y ENDPOINTS: ANÁLISIS DE VIABILIDAD

### 2.1 POST /api/conversations/import (TASK_EXECUTION)

**Viabilidad: VIABLE con una observación**

El flujo es implementable tal como está especificado. La secuencia PENDING → PROCESSING → IMPORTED/ERROR está correctamente separada: el registro se crea primero, se escribe el archivo en /storage/, y la transacción final persiste turns/blocks/usage/classification junto con el status IMPORTED. Si falla la escritura de archivo, queda en PROCESSING para el cleanup job.

**Observación TL-01 — Transacción interna inconsistente con status PROCESSING:**

En el código de §9.1, el paso de PENDING a PROCESSING ocurre fuera de la transacción final `prisma.$transaction`. Luego la transacción interna intenta hacer un UPDATE a IMPORTED. Esto es correcto en la lógica de compensación, pero el código pseudo dentro de `$transaction` llama internamente a `tx.conversationStatusCatalog.findUnique({ where: { code: 'IMPORTED' } })`. Ese lookup debe hacerse fuera de la transacción o al inicio de ella, no en tiempo de UPDATE, para evitar una query de catálogo innecesaria dentro de la transacción. El BE debe decidir el patrón: o pre-fetcha todos los status IDs al inicio del flujo de importación (recomendado) o acepta los lookups repetidos. Esta decisión debe quedar documentada antes de S01.

**Observación TL-02 — El error handler en el catch deja el registro en PROCESSING sin actualizar:**

```typescript
} catch (error) {
  console.error('Import failed:', error);
  throw error;
}
```

Si el catch re-lanza el error sin mover el status a ERROR, el registro queda en PROCESSING y depende del cleanup job para recuperarse. Eso es intencional por la atomicidad por compensación, pero la spec no documenta si el catch debe intentar mover a ERROR directamente o delegar siempre al cleanup. Esta ambigüedad debe cerrarse: la decisión impacta si el BE necesita un bloque de recovery inmediato en el import o no. Recomendación TL: siempre delegar al cleanup, dado que el error podría ser transitorio.

### 2.2 POST /api/conversations/import-review (AGENT_REVIEW / AGENT_CLARIFICATION)

**Viabilidad: VIABLE con riesgo de rendimiento identificado (DB-OBS-03)**

El flujo incremental es correcto: verifica existencia, filtra mensajes nuevos por messageId, inserta solo los nuevos, actualiza endedAt. La separación entre import nuevo e import incremental dentro del mismo endpoint es limpia.

**Observación TL-03 — N+1 en loop de mensajes (DB-OBS-03 confirmado):**

El código de §9.2 hace 3 catalog lookups dentro del loop de mensajes (`messageTypeCatalog`, `messageStatusCatalog`, `priorityCatalog`). Para un canal VTT con 20 mensajes eso son 60 queries de catálogo dentro de la transacción. El BE debe resolver esto antes de S04 con el patrón Map pre-fetcheado que propone DB. Esta observación es de media severidad pero impacta directamente la latencia de import en canales con mucho tráfico.

**Observación TL-04 — `totalMessages` en response UPDATED es inexacto:**

```typescript
totalMessages: existing.messages.length + newMessages.length,
```

`existing.messages` se carga con `include: { messages: true }` al inicio del flujo. En un canal incremental con muchos mensajes, esto carga toda la lista de mensajes en memoria solo para obtener el count. El BE debe considerar usar `_count` de Prisma o un `COUNT` directo, en lugar de cargar la colección completa para contarla. Es una observación menor en impacto funcional pero puede ser significativa en memoria para canales grandes. Documentar decisión antes de S04.

**Observación TL-05 — Participantes no se actualizan en import incremental:**

En el flujo incremental, el código solo inserta nuevos mensajes y actualiza `endedAt`. No verifica si llegaron participantes nuevos al canal entre el primer import y el re-import. Para AGENT_CLARIFICATION donde puede sumarse un agente nuevo después del primer import, esto puede generar participantes faltantes en la BD. La spec debe definir si el import incremental actualiza participantes o solo mensajes. Este punto es una ambigüedad que debe cerrarse antes de S04.

### 2.3 POST /api/conversations/upload (Import manual UI)

**Viabilidad: VIABLE**

El contrato dice que usa el mismo payload y flujo que `/import` pero sin header Authorization. No hay inconsistencia. El BE puede reutilizar el mismo servicio de importación con un flag de `skipAuth`. No hay observaciones adicionales aquí.

### 2.4 GET /api/conversations

**Viabilidad: VIABLE**

Los filtros están bien definidos. La paginación por `limit/offset` es correcta para R1. El default de `status=IMPORTED` en la query params es razonable para la UI.

**Observación TL-06 — Filtro por `topic` y `workType` puede requerir joins costosos:**

El filtro por `topic` hace un join con `ConversationTopic` → `TopicCatalog`, y el filtro por `workType` hace un join con `Classification` → `WorkTypeCatalog`. Si se usan ambos filtros combinados con `agentId` o `projectId`, el planner de PostgreSQL puede no usar los índices óptimos. Para R1 con volumen bajo es aceptable, pero el BE debe monitorearlo. Documentar como known limitation R1.

### 2.5 GET /api/conversations/:id/content

**Viabilidad: VIABLE**

El contrato diferencia correctamente la respuesta para TASK_EXECUTION (turns + blocks) y AGENT_REVIEW (participants + messages). La estructura del response es implementable con una query de Prisma con includes anidados.

**Observación TL-07 — El endpoint lee de BD, no del filesystem:**

La spec §7 indica que los archivos originales se guardan completos en /storage/ y que "la BD tiene índices y resúmenes para búsqueda rápida". El endpoint de content retorna turns y blocks desde la BD (no lee el archivo JSONL). Esto es correcto por performance, pero significa que la BD debe tener el contenido completo de los turns para que el endpoint funcione. El campo `contentPreview` en ConversationTurn guarda solo los primeros 500 chars. El response de content muestra `content` completo en el turno de tipo `user`. Verificar si el BE debe guardar el contenido completo del turno en BD o solo el preview. Esta ambigüedad debe cerrarse antes de S03: si el content endpoint necesita el texto completo, el import debe persistir el texto completo del turno, no solo el preview. Actualmente el schema solo tiene `contentPreview`.

Este es un punto de ambigüedad crítico para implementación.

### 2.6 GET /api/agents/:agentId/timeline

**Viabilidad: VIABLE**

La nota del contrato indica que incluye tanto conversaciones donde `primaryAgentId = agentId` como participaciones multi-agent. Esto requiere una query con OR: `WHERE primary_agent_id = X OR conversation_id IN (SELECT conversation_id FROM conversation_participant WHERE agent_id = X)`. Es implementable pero el BE debe prever que sin el índice `idx_participant_agent` la segunda parte puede ser lenta.

### 2.7 GET /api/agents/:agentId/cost-report

**Viabilidad: VIABLE**

El reporte agrega por semana y por workType. La query usa ConversationUsage (join con Conversation). La respuesta incluye `agentRole` en `byAgent` del project cost-report, lo que requiere el campo `primaryAgentRole` desnormalizado en Conversation. Este campo está en el schema, correcto.

**Observación TL-08 — `byWeek` requiere date trunc en PostgreSQL:**

La agrupación `byWeek` en el formato `YYYY-W##` no es directamente soportada por `groupBy` de Prisma. El BE necesitará usar `prisma.$queryRaw` con `DATE_TRUNC('week', started_at)` o calcular el agrupamiento en la capa de servicio después de traer los datos por rango. Decidir estrategia antes de S05.

### 2.8 GET /api/context

**Viabilidad: VIABLE — ver sección 3 para análisis detallado de riesgos**

### 2.9 GET /api/dashboard/stats

**Viabilidad: VIABLE**

El stat `activeAgents` requiere contar agentes distintos con conversaciones en los últimos N días. La spec no define "activo" (¿últimas 24h, 7 días, 30 días?). Esta ambigüedad debe cerrarse antes de S05.

### 2.10 GET /api/health

**Viabilidad: VIABLE**

El health check verifica BD, storage, Redis. Implementación estándar. Sin observaciones.

---

## 3. RIESGOS DE RUNTIME

### 3.1 GET /context — Riesgo <500ms

**Evaluación: VIABLE PERO CON RIESGO REAL EN ESCALA**

El diseño usa `Promise.race` contra un timeout de 500ms. Todas las queries corren en paralelo con `Promise.all`. Los índices definidos cubren la mayoría de las queries. Sin embargo, se identifican tres vectores de riesgo:

**Riesgo 1 — frequentFiles groupBy (confirmado por AR):**

```typescript
prisma.turnBlock.groupBy({
  by: ['filePath'],
  where: {
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
})
```

Este groupBy requiere join TurnBlock → ConversationTurn → Conversation con filtro en Conversation. Prisma traduce esto como un subquery o join complejo. Sin el índice compuesto `(primaryAgentId, projectId, startedAt DESC)` en Conversation (DB-OBS-05), la query de Conversation dentro del join puede ser un seq scan parcial. Con 500+ conversaciones por agente esto puede superar los 500ms.

**Decisión TL requerida:** Agregar índice compuesto `(primaryAgentId, projectId)` en Conversation antes de S03. El DB ya lo documentó como DB-OBS-05 crítico para <500ms.

**Riesgo 2 — recentReviews con OR y subquery de participants:**

```typescript
OR: [
  { primaryAgentId: input.agentId },
  { participants: { some: { agentId: input.agentId } } },
],
```

Prisma traduce `participants: { some: ... }` como un EXISTS subquery. Combinado con OR y el filtro de projectId, puede ser ineficiente. Para R1 con volumen bajo es manejable. El índice `idx_participant_agent` en ConversationParticipant ayuda al subquery. Monitorear.

**Riesgo 3 — lookup de statusId en cada ejecución:**

```typescript
const importedStatus = await prisma.conversationStatusCatalog.findUnique({
  where: { code: 'IMPORTED' },
});
const importedStatusId = importedStatus!.id;
```

Este lookup se hace en cada llamada a `getContext`. Son datos estáticos de catálogo que no cambian. El BE debe cachearlos en memoria al inicio del proceso (startup cache de IDs de catálogo), no en Redis, sino en un objeto singleton en el módulo. Esto elimina una query de catálogo en cada ejecución del endpoint más crítico del sistema.

**Decisión TL requerida:** Implementar startup cache de IDs de catálogo estáticos (status, types, sources) como singleton en memoria antes de S03.

### 3.2 Import TASK_EXECUTION — Riesgo de latencia en clasificación

La clasificación (`classifierService.classify(parsed)`) ocurre después de escribir el archivo. El flujo no especifica cuánto tarda la clasificación. Para conversaciones con cientos de turns y miles de blocks, el parsing de keywords puede ser lento si no está optimizado. La spec indica que es "reglas determinísticas" sin LLM, pero no define el algoritmo ni su complejidad. El BE debe asegurar que la clasificación corre en tiempo lineal sobre los blocks.

**Observación TL-09:** Antes de S02 (sprint donde se implementa clasificación), el BE debe definir el algoritmo de clasificación con complejidad conocida y añadir un timeout interno para no bloquear el import si la clasificación tarda.

### 3.3 Import AGENT_REVIEW incremental — Riesgo de carga de mensajes en memoria

Como se indicó en TL-04, cargar `include: { messages: true }` en el check de existencia trae todos los mensajes para comparar con los nuevos. Para canales con 100+ mensajes históricos, esto es ineficiente.

**Recomendación:** Cargar solo `messageId` en el include inicial para el check de idempotencia:

```typescript
const existing = await prisma.conversation.findUnique({
  where: { sourceId_externalSessionId: { ... } },
  include: { messages: { select: { messageId: true } } },
});
```

El BE debe aplicar esto antes de S04.

### 3.4 Cleanup Job — Riesgo de estado PROCESSING sin recovery real

El cleanup job mueve conversaciones de PROCESSING o PENDING a PENDING (retry) pero la spec dice:

```typescript
// TODO: Trigger reprocesamiento si el archivo original está disponible
```

Este TODO en el código de §10.2 es una brecha funcional real. El retry incrementa el contador y vuelve al estado PENDING, pero no tiene mecanismo para volver a procesar la conversación. Dado que el archivo original fue enviado como multipart en el request original, no está disponible en el retry del job.

**Esto significa que el retry automático del cleanup job no puede reimportar la conversación — solo puede marcarla como PENDING infinitamente hasta llegar al ERROR definitivo.**

El retry solo tiene valor si el fallo fue en la escritura del archivo (disco lleno, permiso) y el sistema se recuperó. En ese caso, el import original debería poder reintentarse desde el request del Hook Manager. La spec no define si el Hook Manager reintenta el request en caso de error 500. Esta brecha debe cerrarse antes de S04.

**Decisión TL requerida antes de S04:** Definir qué hace el cleanup job en el retry si no tiene el archivo. Opciones: (a) marcar directamente como ERROR en lugar de retry cuando no hay mecanismo de reintento real, o (b) diseñar un mecanismo de retry con el Hook Manager (fuera del alcance R1). Para R1, la opción más honesta es (a): si no hay mecanismo de reintento externo, el cleanup debe marcar ERROR directamente en lugar de dar falsa esperanza con retries sin acción real.

---

## 4. AMBIGÜEDADES DE SPEC QUE DEBEN CERRARSE ANTES DE IMPLEMENTACIÓN

| ID | Sección | Ambigüedad | Impacto | Deadline |
|----|---------|------------|---------|----------|
| **AMB-01** | §8.6, §4.1 | `contentPreview` vs contenido completo en turns: el endpoint GET /content retorna `content` completo en los turns, pero el schema solo tiene `contentPreview String?` (500 chars). ¿El import persiste el texto completo de cada turno o solo el preview? | Bloqueante para S03 | Antes de S01 (afecta schema) |
| **AMB-02** | §9.2 | Import incremental AGENT_REVIEW: ¿se actualizan participantes nuevos o solo mensajes? | Funcional S04 | Antes de S04 |
| **AMB-03** | §8.11 | `activeAgents` en dashboard stats: ¿cuál es la ventana de tiempo para considerar un agente "activo"? | Funcional S05 | Antes de S05 |
| **AMB-04** | §10.2 | Cleanup job retry sin mecanismo de reintento real: ¿qué hace el job si la conversación está en PENDING/PROCESSING pero el archivo ya no está disponible? | Funcional S04 | Antes de S04 |
| **AMB-05** | §9.1 | Pattern para manejo de status IDs de catálogos en el flujo de import: ¿se pre-fetchean una vez al inicio del proceso o se buscan en cada request? | Performance | Antes de S01 |
| **AMB-06** | §8.8 | Agrupación `byWeek` en cost-report: ¿se implementa con `$queryRaw` + `DATE_TRUNC` o con agrupamiento en capa de servicio? | Implementación S05 | Antes de S05 |
| **AMB-07** | §9.1 | Error handler en catch de import: ¿el import intenta mover a ERROR directamente o siempre delega al cleanup job? | Funcional S01 | Antes de S01 |

---

## 5. DECISIONES TÉCNICAS QUE EL BE DEBE TOMAR O QUE DEBEN QUEDAR DEFINIDAS

### DEC-01: Startup cache de IDs de catálogo (REQUERIDO antes de S01)

Los IDs de catálogos (status codes, conversation types, source codes) son estáticos post-seed. El BE debe implementar un singleton que cargue estos IDs al iniciar el proceso y los mantenga en memoria. Esto elimina decenas de lookups por request en los flujos críticos (import, context).

Patrón sugerido:
```
src/config/catalog-cache.ts
  → loadCatalogIds(): Promise<void>  // llamado en app startup
  → getCatalogIds(): CatalogIds      // acceso síncrono
```

Esta decisión impacta S01 (setup del proyecto) y debe estar implementada antes de que el primer endpoint se integre.

### DEC-02: Partial indexes — Prisma nativo vs SQL manual (REQUERIDO antes de S01)

DB-OBS-04 identifica que los partial indexes del §6 no tienen equivalente en schema.prisma. El BE debe decidir antes de S01:

- Opción A: Usar sintaxis Prisma de partial index (`where:` en `@@index`) — requiere Prisma v4.6+. Verificar versión del stack.
- Opción B: Crear partial indexes en una migración SQL manual post-deploy, fuera del schema.prisma. Documentar en `/prisma/migrations/` como migration custom.

La decisión afecta cómo se gestiona el schema going forward y debe quedar documentada en el devlog de S01.

### DEC-03: Estrategia de classficación — complejidad y timeout interno (REQUERIDO antes de S02)

El clasificador procesa turns y blocks para detectar topics, workType y entities. La spec no define el algoritmo. El BE debe documentar:

- Algoritmo: keyword matching sobre `filePath` de TurnBlocks + `toolName` + text content preview
- Complejidad: O(N) sobre número de blocks
- Timeout interno: si clasificación supera X ms (sugerido: 2000ms), skippear y dejar classification sin workType

### DEC-04: Contenido completo de turns en BD (BLOQUEANTE para schema S01)

AMB-01 debe resolverse antes de generar la migración inicial. Si el endpoint GET /content necesita texto completo de cada turno, el schema debe agregar un campo `content Text?` en ConversationTurn. Si solo se necesita el preview, el campo `contentPreview` es suficiente pero el endpoint de content debe leer del archivo en /storage/ para obtener el texto completo.

Opciones:
- A: Agregar `content Text?` en ConversationTurn — BD puede crecer significativamente
- B: Mantener solo `contentPreview`, el endpoint de content lee del filesystem — agrega latencia al endpoint de content por I/O de disco
- C: Híbrido: BD tiene preview, endpoint content sirve desde BD para el preview y desde archivo solo si se pide contenido completo (requiere dos endpoints o un flag)

Esta decisión cambia el schema y debe cerrarse antes de S01.

### DEC-05: Redis como rate limiter vs uso actual (INFORMATIVA)

La spec incluye Redis (`shared-redis`) pero la tabla de auth (§7.1) no muestra rate limiting configurado. La dependencia de Redis en el docker-compose es real pero su uso en R1 se limita al rate limiter configurado como "Memory (dev) → Redis (prod)" (D-MEM-22). El BE debe asegurar que el servicio de rate limit sea opcional (si Redis no está disponible, fallback a Memory) para no generar dependencia de startup bloqueante.

---

## 6. AJUSTES REQUERIDOS DERIVADOS DE OBSERVACIONES DB

### 6.1 DB-OBS-01 — ConversationEntity constraint único (BLOQUEANTE para schema S01)

El schema actual no tiene `@@unique([conversationId, entityName])` en ConversationEntity. Esto permite duplicados en retries. Este ajuste debe incorporarse en el schema ANTES de generar la migración inicial de S01.

**Acción:** El DB Engineer debe confirmar que el schema final a migrar en S01 incluye este constraint. Es el único bloqueante confirmado para proceder.

### 6.2 DB-OBS-02 — Cleanup job debe filtrar por statusId, no por status.code

El cleanup job debe pre-fetchear los IDs de status al inicio del cron y filtrar directamente por `statusId: { in: [pendingId, processingId] }`. Esto aplica el índice `idx_conv_status` correctamente.

**Acción:** BE implementa el patrón pre-fetch de IDs antes de S04. Puede reutilizar DEC-01 (startup cache).

### 6.3 DB-OBS-03 — N+1 en importAgentReview

El loop de mensajes en import-review debe usar Maps pre-fetcheados de catálogos en lugar de un lookup por mensaje.

**Acción:** BE implementa el patrón Map antes de S04. El código exacto de corrección está en la revisión DB §6.3.

### 6.4 DB-OBS-04 — Partial indexes

Requiere decisión DEC-02. Acción previa a S01.

### 6.5 DB-OBS-05 — Índice compuesto `(primaryAgentId, projectId, startedAt DESC)` en Conversation

Crítico para el requisito <500ms en GET /context. Debe estar en el schema antes de S03.

**Acción:** Agregar al schema.prisma el índice compuesto. Generar migración en S01 junto con el resto del schema.

### 6.6 DB-OBS-06, 07, 08 — Índices menores y manejo P2002

- AgentMessage: agregar `@@index([conversationId, timestamp(sort: Desc)])` antes de S04
- Conversation: agregar `@@index([importedAt(sort: Desc)])` antes de S05
- Manejo explícito de error P2002 en el catch del create de Conversation antes de S01

---

## 7. OBSERVACIONES AR CONFIRMADAS

**AR-OBS-01 — Versionado del documento:**

El documento se titula v1.5 externamente pero declara v1.4 en header y footer. Esta inconsistencia no bloquea pero debe corregirse en la próxima versión del documento para evitar confusión durante implementación.

**AR-OBS-02 — Query del cleanup job por status.code:**

Confirmado por DB como DB-OBS-02. La corrección está detallada en §6.2 de este documento.

---

## 8. CHECKLIST DE CIERRE ANTES DE PASAR A CONSOLIDACIÓN SA

### Bloqueantes (deben resolverse antes de arrancar S01)

- [ ] **DEC-04 / AMB-01**: Definir si ConversationTurn almacena `content Text?` completo o solo `contentPreview`. Si se decide texto completo, agregar campo al schema. Si se decide leer de filesystem en el endpoint de content, documentar el comportamiento esperado del endpoint GET /content.
- [ ] **DB-OBS-01**: Confirmar que el schema final incluye `@@unique([conversationId, entityName])` en ConversationEntity antes de generar la migración inicial.
- [ ] **DEC-01**: Implementar startup cache de IDs de catálogos estáticos como singleton en el proyecto. Incluir en el setup de S01.
- [ ] **DEC-02**: Decidir estrategia de partial indexes (Prisma nativo vs SQL manual) y documentar en el plan de implementación de S01.
- [ ] **AMB-07**: Definir comportamiento del catch en el flujo de import (delegar siempre al cleanup vs intentar mover a ERROR directamente).
- [ ] **DB-OBS-08**: Agregar manejo explícito de error P2002 en el create de Conversation para race conditions.

### Requeridos antes de S03 (GET /context)

- [ ] **DB-OBS-05**: Agregar índice compuesto `@@index([primaryAgentId, projectId, startedAt(sort: Desc)])` al schema.prisma. Incluir en migración de S01 si aún está disponible.
- [ ] **DEC-03**: Documentar algoritmo de clasificación con complejidad conocida y timeout interno.
- [ ] **TL-09**: Asegurar que la clasificación no bloquea el import si tarda más del límite definido.

### Requeridos antes de S04 (import-review, cleanup)

- [ ] **DB-OBS-02**: Refactorizar cleanup job para filtrar por statusId en lugar de status.code.
- [ ] **DB-OBS-03**: Resolver N+1 en importAgentReview con Maps pre-fetcheados.
- [ ] **AMB-02**: Definir si el import incremental actualiza participantes o solo mensajes.
- [ ] **AMB-04**: Definir qué hace el cleanup en retry si no hay mecanismo de reintento real del archivo.
- [ ] **TL-04**: Refactorizar carga de mensajes en import-review a `select: { messageId: true }` para check de idempotencia.

### Requeridos antes de S05 (dashboard, cost-report)

- [ ] **DB-OBS-06**: Agregar `@@index([conversationId, timestamp(sort: Desc)])` en AgentMessage.
- [ ] **DB-OBS-07**: Agregar `@@index([importedAt(sort: Desc)])` en Conversation.
- [ ] **AMB-03**: Definir ventana de tiempo para `activeAgents` en dashboard stats.
- [ ] **AMB-06**: Definir estrategia de agrupación `byWeek` (raw SQL vs capa de servicio).

### Informativas (documentar, no bloquean sprint)

- [ ] **AR-OBS-01**: Corregir versionado del documento SPEC (v1.4 interno vs v1.5 externo).
- [ ] **TL-06**: Documentar como known limitation R1 la posible lentitud en filtros combinados de GET /conversations.
- [ ] **DEC-05**: Confirmar que Redis es opcional en startup (fallback a memory) para no crear dependencia bloqueante.
- [ ] **TL-08**: Confirmar estrategia de agrupación byWeek con el BE antes de S05.

---

## 9. RESUMEN DE RIESGOS TÉCNICOS POR SEVERIDAD

| Riesgo | Severidad | Sprint impactado | Acción |
|--------|-----------|------------------|--------|
| AMB-01: campo content en Turn (schema) | BLOQUEANTE | S01 (schema) | DEC-04 antes de migración |
| DB-OBS-01: ConversationEntity duplicados | BLOQUEANTE | S01 (schema) | Agregar @@unique antes de migración |
| frequentFiles groupBy latencia | ALTO | S03 (context <500ms) | DB-OBS-05 + DEC-01 |
| Startup cache de catálogos ausente | ALTO | S01, S03 | DEC-01 |
| Cleanup job retry sin reintento real | MEDIO | S04 | AMB-04 |
| N+1 en importAgentReview | MEDIO | S04 | DB-OBS-03 |
| Carga completa de mensajes en incremental | MEDIO | S04 | TL-04 |
| Race condition P2002 | MEDIO | S01 | DB-OBS-08 |
| byWeek agrupación en cost-report | BAJO | S05 | AMB-06 |
| activeAgents sin definición | BAJO | S05 | AMB-03 |

---

## 10. SIGUIENTE PASO

| Actor | Acción | Deadline |
|-------|--------|----------|
| **PM** | Revisar AMB-01 (DEC-04): campo content vs contentPreview en Turn — decisión impacta schema de S01 | Antes de SA consolidation |
| **SA** | Recibir este documento y los de AR + DB para consolidar spec final | Después de que PM resuelva AMB-01 |
| **DB** | Confirmar schema final con @@unique ConversationEntity + índices adicionales antes de migración S01 | Antes de arranque S01 |
| **BE** | Leer checklist §8 e incorporar en plan de trabajo de cada sprint | Antes de arranque S01 |

---

**Documento:** TL_REVIEW_SPEC_MEMORY_SERVICE_v1.md
**Revisor:** Tech Lead (TL-Agent)
**Fecha:** 2026-04-12
**Estado:** COMPLETADO — pendiente resolución de AMB-01 por PM antes de consolidación SA
