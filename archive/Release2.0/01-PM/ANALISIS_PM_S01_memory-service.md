# ANÁLISIS PM — Memory Service (Módulo Independiente)

**Documento:** ANALISIS_PM_S01_memory-service.md
**Fase:** 02-Analysis / Sprint 01
**Versión:** 1.2
**Fecha:** 2026-04-09
**Autor:** PM (Martin Rivas)
**Estado:** 🟡 Listo para revisión SA → AR → TL
**Siguiente paso:** SA refina casos de uso y modelo funcional

---

## CONTEXTO — Por qué desde cero

### Lo que existe hoy (y por qué no sirve)

Existe un módulo llamado **VTM (virtual-teams-memory)** que fue construido de forma incremental y local:

- Corre en `localhost:3002` — no está en la VM
- Almacena datos en archivos locales (JSONL, JSON) — no tiene persistencia en BD
- Fue diseñado para **visualizar** conversaciones históricas, no para ser consumido por agentes
- No tiene API de contexto runtime
- El schema de BD existente (TagDefinition, Session, Turn, TurnClassification) fue diseñado para clasificación semántica, no para el modelo de datos que necesita el Hook Manager
- Los documentos de diseño existentes (v1.2, DISENO_MEMORY_SERVICE_VTT.md) tienen contradicciones entre sí

**Decisión:** El Memory Service se diseña como proyecto independiente desde cero. El repo `virtual-teams-memory` existente **se descarta como base de implementación** — puede consultarse como referencia de lógica de parseo, pero no se migra ni se reutiliza su estructura. El nuevo proyecto parte de cero con el proceso formal.

---

## 1. OBJETIVO DEL MÓDULO

El **Memory Service** es el servicio responsable de:

1. **Recibir y persistir** conversaciones de agentes IA — provenientes de múltiples fuentes
2. **Clasificar e indexar** el contenido para búsqueda rápida
3. **Proveer contexto runtime** al Hook Manager antes de lanzar un agente
4. **Exponer historial acumulado** por agente para auditoría y métricas de costo

### Consumidores del servicio

| Consumidor | Qué necesita |
|-----------|-------------|
| **Hook Manager** | Contexto relevante ANTES de lanzar un agente (`GET /context`) |
| **Hook Manager** | Endpoint para importar conversación DESPUÉS de que termina (`POST /import`) |
| **Dashboard VTT** | Historial de conversaciones por agente y costo acumulado |
| **TL-Agent** | Contexto histórico para armar assignments |
| **PM** | Métricas de costo por agente, tarea y proyecto |

---

## 2. PRINCIPIOS DE DISEÑO

| Principio | Decisión |
|-----------|---------|
| **Proyecto independiente** | Repo propio, BD propia, deploy independiente en VM |
| **BD propia** | PostgreSQL `memory_db` en shared-postgres (NO en vtt_db) |
| **Sin dependencia de VTT en runtime** | El Memory Service no llama a VTT para funcionar |
| **Referencia por ID** | Usa `projectId`, `taskId`, `agentId` de VTT como referencias, sin FK cruzadas |
| **Historial acumulado por agente** | Las conversaciones se acumulan en una línea de tiempo por agente, no por sesión aislada |
| **Extensible a cualquier fuente** | Diseñado para recibir conversaciones de cualquier modelo de IA |
| **Contenido en archivos, metadatos en BD** | BD liviana: guarda metadatos y clasificaciones; el contenido completo vive en archivos en la VM |
| **Idempotencia** | Si el mismo archivo se importa dos veces (mismo `externalSessionId`), se ignora la segunda importación — no se duplica |

---

## 3. FUENTES DE CONVERSACIONES

El Memory Service debe soportar 4 fuentes en R1 y ser extensible a más:

### 3.1 Claude CLI (source: `CLAUDE_CLI`)

- **Origen:** Sesiones de Claude Code (`~/.claude/projects/{dir}/{sessionId}.jsonl`)
- **Formato:** JSONL — una línea por evento (`user`, `assistant`, `tool_use`, `tool_result`)
- **Datos disponibles:** Historial completo de turns, tool calls, archivos tocados, branch git
- **Archivos:** 1 archivo `.jsonl` por sesión
- **Costo:** ❌ No disponible en CLI

### 3.2 Claude Web (source: `CLAUDE_WEB`)

- **Origen:** Export manual desde claude.ai
- **Formato:** JSON único con `chat_messages[]`
- **Datos disponibles:** Historial completo, timestamps, attachments
- **Archivos:** 1 archivo `.json`
- **Costo:** ❌ No disponible

### 3.3 Agent SDK (source: `CLAUDE_SDK`)

- **Origen:** Agentes ejecutados via `claude_agent_sdk` (Python)
- **Formato:** DOS archivos por sesión:
  - `session_{id}.json` — historial completo de turns
  - `log_{id}.jsonl` — eventos con `ResultMessage` al final (contiene costo y tokens)
- **Datos disponibles:** Historial completo + **costo en USD + tokens desagregados** ← única fuente con costo real
- **Archivos:** 2 archivos por sesión — ambos se envían al importar
- **Costo:** ✅ Disponible via `ResultMessage.total_cost_usd` en `log_{id}.jsonl`

### 3.4 ChatGPT Export (source: `CHATGPT`)

- **Origen:** Export manual desde ChatGPT (OpenAI)
- **Formato:** JSON con estructura `mapping` (árbol de nodos, no lista lineal)
- **Datos disponibles:** Historial de turns
- **Archivos:** 1 archivo `.json`
- **Costo:** ❌ No disponible

### 3.5 Extensibilidad futura

El campo `source` debe ser extensible (string, no enum cerrado) para soportar:
- Gemini, Copilot, otros modelos de IA
- Importación manual desde cualquier formato

---

## 4. REQUERIMIENTOS FUNCIONALES

### RF-001: Importación de conversaciones

El servicio debe recibir conversaciones via API. El archivo se envía con su contenido completo — **el archivo se copia físicamente a la VM** y queda almacenado en el filesystem del Memory Service.

Para `CLAUDE_SDK` se envían **dos archivos** en el mismo request:

```
POST /api/conversations/import
Content-Type: multipart/form-data

source: "CLAUDE_CLI" | "CLAUDE_WEB" | "CLAUDE_SDK" | "CHATGPT" | string
agentId: UUID           // referencia a User.id en VTT
projectId: UUID         // referencia a Project.id en VTT
taskId?: UUID           // opcional para sesiones sin tarea asignada
externalSessionId: string  // ID original del archivo — usado para deduplicación
file: [archivo.jsonl | archivo.json]       // archivo principal
logFile?: [log_{id}.jsonl]                 // solo para CLAUDE_SDK
```

El servicio:
1. Verifica que `externalSessionId` no exista ya en BD — si existe, retorna `{ status: "ALREADY_INDEXED" }` sin procesar
2. Recibe y **guarda el/los archivo(s) en el filesystem de la VM** bajo la ruta organizada por agente/fecha
3. Detecta el formato por `source`
4. Parsea el/los archivo(s) con el adapter correspondiente
5. Extrae metadatos (turns, tool calls, archivos tocados, tokens si hay)
6. Clasifica el contenido por reglas determinísticas (V1 — sin LLM)
7. Persiste metadatos + ruta(s) al archivo en BD
8. Concatena la sesión al AgentTimeline del agente (ordenado por `startedAt`)

> **Principio clave:** El archivo original no se lee remotamente. Se transfiere a la VM y vive ahí permanentemente.

### RF-002: Historial acumulado por agente (AgentTimeline)

```
GET /api/agents/{agentId}/timeline?projectId=X&limit=10
```

Retorna las conversaciones del agente ordenadas cronológicamente, como una línea de tiempo continua:

```json
{
  "agentId": "abdff0db-...",
  "projectId": "d837bcd5-...",
  "totalSessions": 47,
  "totalCostUsd": 12.45,
  "timeline": [
    {
      "conversationId": "...",
      "source": "CLAUDE_CLI",
      "date": "2026-02-01",
      "taskId": "VTT-123",
      "taskTitle": "Implementar auth service",
      "turnCount": 18,
      "filesModified": ["src/auth.service.ts", "src/user.service.ts"],
      "topics": ["authentication", "jwt"],
      "costUsd": null
    },
    {
      "conversationId": "...",
      "source": "CLAUDE_SDK",
      "date": "2026-02-05",
      "taskId": "VTT-130",
      "costUsd": 0.82,
      "turnCount": 6
    }
  ]
}
```

> El AgentTimeline no es una estructura especial — es un query `ORDER BY startedAt ASC` sobre `Conversation` filtrado por `agentId` y `projectId`.

### RF-003: Contexto runtime para Hook Manager

El endpoint más crítico del servicio. El Hook Manager lo consulta ANTES de lanzar un agente:

```
GET /api/context?agentId=X&taskId=Y&projectId=Z&topics=authentication,jwt&limit=5
```

Retorna contexto relevante compacto para inyectar en el prompt del agente:

```json
{
  "agentContext": {
    "recentWork": [...],
    "relevantSessions": [...],
    "filesFrequentlyModified": [],
    "lessonsLearned": [],
    "estimatedCost": 0.50
  }
}
```

> Debe responder en < 500ms — es síncrono y bloqueante para el Hook Manager.

### RF-004: Lectura de contenido de conversación

Para que VTT frontend (ConversationViewer) pueda renderizar el texto completo de una conversación:

```
GET /api/conversations/{conversationId}/content
```

Memory Service lee el archivo almacenado en la VM y retorna el contenido parseado:

```json
{
  "conversationId": "...",
  "source": "CLAUDE_CLI",
  "turns": [
    { "role": "user", "content": "...", "timestamp": "..." },
    { "role": "assistant", "content": "...", "timestamp": "..." }
  ]
}
```

> El ConversationViewer en VTT frontend **no se mueve** al Memory Service — permanece en VTT. Sí requiere **rediseño** para consumir esta nueva API en lugar del VTM local. Ese rediseño es scope de una tarea FE separada.

### RF-005: Métricas de costo

```
GET /api/projects/{projectId}/cost-report
GET /api/agents/{agentId}/cost-report?projectId=X
```

- Costo total por agente (solo source=SDK tiene costo real)
- Costo por tarea
- Cache hit ratio (cacheReadTokens / totalTokens)
- Tokens por turno promedio
- Distribución por fuente (cuántas sesiones medidas vs no medidas)

### RF-006: Upload manual de conversaciones (UI)

Para sesiones CLI/Web que no pasan por Hook Manager:

```
POST /api/conversations/upload
Content-Type: multipart/form-data
source, agentId, projectId, taskId
file: [archivo.jsonl | archivo.json]
logFile?: [log_{id}.jsonl]  // solo para SDK manual
```

> Mismo proceso que RF-001 — comparte la lógica de importación.

---

## 5. REQUERIMIENTOS NO FUNCIONALES

| Requerimiento | Valor |
|--------------|-------|
| **Deploy** | Docker container independiente en VM Hetzner |
| **Puerto** | 3002 (ya establecido) |
| **BD** | PostgreSQL `memory_db` en shared-postgres |
| **Storage archivos** | Filesystem local de la VM (volumen Docker mapeado) — estructura: `/storage/{agentId}/{YYYY-MM}/{externalSessionId}/` |
| **Red** | `shared-network` (misma red que VTT y Hook Manager) |
| **Auth** | Service token (misma estrategia que VTT: `x-service-key` header) |
| **Escalabilidad** | Horizontal — stateless, BD + filesystem son el estado |
| **Latencia contexto** | < 500ms para `GET /api/context` (es síncrono y bloqueante) |
| **Idempotencia** | Import duplicado por `externalSessionId` retorna `ALREADY_INDEXED` sin error |
| **Retención** | Sin límite inicial; política de retención como feature futura |
| **Render conversaciones** | ConversationViewer permanece en VTT frontend — consume `GET /conversations/{id}/content` del Memory Service. Requiere rediseño FE (scope separado) |

---

## 6. MODELO DE DATOS CONCEPTUAL

> Nota: El modelo exacto (Prisma schema) es responsabilidad del DB Engineer en fase 03-design.
> Aquí se define el concepto, no la implementación.

### 6.1 Entidades principales

```
AgentProfile
  agentId (referencia a User.id en VTT — NO se crea catálogo propio)
  projectId
  totalSessions
  totalCostUsd

Conversation
  id
  source (CLAUDE_CLI | CLAUDE_WEB | CLAUDE_SDK | CHATGPT | string)
  agentId → AgentProfile
  projectId
  taskId (nullable)
  externalSessionId (ID original — campo único para deduplicación)
  startedAt / endedAt
  turnCount
  filePath (ruta al archivo principal en VM)
  logFilePath (ruta al log file — solo SDK)
  status (INDEXED | PROCESSING | ERROR)

ConversationTurn
  conversationId
  turnIndex
  role (USER | ASSISTANT)
  timestamp
  toolsUsed[] (nombres de tools: Write, Edit, Bash...)
  filesModified[] (paths extraídos del input de tools)

ConversationUsage (solo source=SDK)
  conversationId
  inputTokens
  outputTokens
  cacheCreationTokens
  cacheReadTokens
  totalCostUsd
  durationMs
  modelId

ClassificationTag
  conversationId
  tag (topic/authentication, tipo/implementation, agente/backend...)
  confidence
  classifiedBy (rules-v1 | manual)
```

### 6.2 Principio de contenido

- **BD almacena:** metadatos, clasificaciones, métricas, rutas a archivos
- **BD NO almacena:** texto completo de los mensajes (queda en archivos en la VM)
- **Para leer el texto:** `GET /api/conversations/{id}/content` lee el archivo desde la VM bajo demanda

---

## 7. FLUJOS PRINCIPALES

### Flujo A: Post-corrida (automático via Hook Manager)

```
1. Agente termina sesión en máquina local
2. Hook Stop (Claude Code hook) se dispara localmente
3. Hook lee el/los archivos generados:
   - CLI: ~/.claude/projects/{dir}/{sessionId}.jsonl
   - SDK: session_{id}.json + log_{id}.jsonl
4. Hook envía el/los archivos (multipart) a Memory Service en VM:
   POST http://77.42.88.106:3002/api/conversations/import
5. Memory Service:
   a. Verifica idempotencia por externalSessionId — si ya existe, retorna ALREADY_INDEXED
   b. Guarda el/los archivo(s) en /storage/{agentId}/{YYYY-MM}/{externalSessionId}/
   c. Selecciona adapter según source
   d. Parsea archivo(s) — extrae turns, tool calls, archivos tocados
   e. Extrae costo/tokens del log file si es SDK
   f. Clasifica por reglas determinísticas (keywords en tools/archivos)
   g. Persiste metadatos + ruta(s) del archivo en BD
   h. Concatena al AgentTimeline (ordenado por startedAt)
   i. Retorna { conversationId, status: "INDEXED" }
6. Hook termina — agente continúa
```

### Flujo B: Pre-corrida (contexto runtime)

```
1. Hook Manager recibe nueva tarea para agente X
2. Hook Manager llama GET /api/context?agentId=X&taskId=Y&topics=...
3. Memory Service (< 500ms):
   a. Busca últimas N sesiones del agente (query BD)
   b. Busca sesiones con topics similares (query BD)
   c. Extrae filesModified frecuentes en ese módulo (query BD)
   d. Compila contexto compacto — NO lee archivos (todo desde metadatos en BD)
4. Memory Service retorna contexto
5. Hook Manager inyecta contexto en el prompt del agente
```

### Flujo C: Importación manual (UI)

```
Usuario sube archivo desde ConversationViewer en VTT
    ↓
POST /api/conversations/upload (multipart)
    ↓
Mismo proceso que Flujo A desde paso 5
    ↓
UI muestra confirmación con conversationId
```

### Flujo D: Lectura para render en VTT frontend

```
ConversationViewer selecciona conversación del AgentTimeline
    ↓
GET /api/agents/{agentId}/timeline (metadatos — BD)
    ↓
Usuario selecciona conversación específica
    ↓
GET /api/conversations/{id}/content (texto completo — lee archivo de VM)
    ↓
ConversationViewer renderiza los turns
```

---

## 8. CLASIFICACIÓN (SCOPE R1)

Para R1, la clasificación usa **reglas determinísticas** (sin LLM, sin embeddings). Se ejecuta sincrónicamente en el momento de la importación:

- Detectar topics por keywords en tool calls y archivos modificados (ej: `auth`, `prisma`, `migration`, `docker`)
- Detectar tipo de trabajo por patrones (implementation, bug-fix, review, migration, deploy)
- Detectar fase/módulo por `taskId` si está disponible
- Detectar archivos frecuentemente modificados por el agente

Las reglas de clasificación son **configurables** — lista de keywords por topic guardada en archivo de configuración o tabla en BD.

> **V2 (fuera de scope R1):**
> - Búsqueda semántica / embeddings
> - Full-text search sobre el texto de los mensajes
> - Clasificación automática por LLM

---

## 9. LO QUE NO INCLUYE ESTE MÓDULO (OUT OF SCOPE R1)

| Fuera de scope | Razón |
|---------------|-------|
| Búsqueda semántica / embeddings | R2 |
| Full-text search sobre contenido de mensajes | R2 |
| Multi-agente en una conversación | R2 |
| Integración con RBAC de VTT | Cuando RBAC esté activo — `workspaceId` nullable por ahora |
| Retención automática (purge de datos viejos) | R2 |
| Dashboard UI propio | VTT consume la API — no hay UI propia en Memory Service |
| Rediseño del ConversationViewer | Tarea FE separada — fuera del scope de este módulo |
| Migración de datos del VTM actual | VTM se descarta — se parte de cero |

---

## 10. DECISIONES TOMADAS (PM)

| # | Decisión | Detalle |
|---|---------|---------|
| D-01 | Los archivos se copian a la VM | El Hook local lee el archivo y lo envía via multipart a `POST /import`. Memory Service lo almacena en el filesystem de la VM. No hay lectura remota. |
| D-02 | SDK envía dos archivos | `session_{id}.json` + `log_{id}.jsonl` — el segundo contiene el costo. Ambos se envían en el mismo request multipart. |
| D-03 | Idempotencia por externalSessionId | Si el mismo archivo llega dos veces, se retorna `ALREADY_INDEXED` sin error. |
| D-04 | Storage organizado por agente/fecha | `/storage/{agentId}/{YYYY-MM}/{externalSessionId}/` |
| D-05 | ConversationViewer permanece en VTT | Se redeseña para consumir la API del Memory Service. Tarea FE separada. |
| D-06 | VTM existente se descarta | No se migra. Se parte de cero. El repo puede consultarse solo como referencia de lógica. |
| D-07 | AgentTimeline = query ordenado | No es estructura especial — es `ORDER BY startedAt ASC` sobre `Conversation`. |

---

## 11. PREGUNTAS ABIERTAS PARA SA / AR

| # | Pregunta | Para quién |
|---|---------|-----------|
| Q-01 | ¿`agentId` en Memory Service es el mismo `User.id` de VTT, o se crea un catálogo propio de agentes? | SA |
| Q-03 | ¿Cómo se autentica el Hook Manager contra Memory Service? ¿Service key compartida o token independiente? | AR |
| Q-04 | ¿Memory Service necesita consultarle algo a VTT en runtime (ej: nombre de la tarea para el timeline)? ¿O trabaja solo con los IDs? | SA |
| Q-05 | ¿El contexto runtime (RF-003) puede ser asíncrono o siempre debe ser síncrono (< 500ms)? | AR |

---

## 12. RELACIÓN CON OTROS MÓDULOS

```
Hook Manager (local)
  ├── POST /api/conversations/import  → Memory Service (post-corrida, envía archivos)
  └── GET /api/context                → Memory Service (pre-corrida, síncrono < 500ms)

VTT Frontend (ConversationViewer — rediseño pendiente)
  ├── GET /api/agents/:id/timeline    → Memory Service (lista de sesiones)
  └── GET /api/conversations/:id/content → Memory Service (texto completo para render)

VTT Backend / Dashboard
  └── GET /api/projects/:id/cost-report → Memory Service

Agent Runtime (SDK)
  └── Genera session_{id}.json + log_{id}.jsonl
      → Hook Stop los detecta → Memory Service los importa

Claude Code CLI
  └── Genera {sessionId}.jsonl
      → Hook Stop lo detecta → Memory Service lo importa
```

---

## 13. ESTRUCTURA DEL PROYECTO (nueva)

Siguiendo ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1:

```
virtual-teams-memory/          ← repo independiente (nuevo desde cero)
├── phases/
│   ├── 02-analysis/
│   │   ├── deliverables/
│   │   └── _pm/analisis/S01/
│   │       ├── 01-PM/         ← este documento
│   │       ├── 02-SA/
│   │       ├── 03-AR/
│   │       └── 04-TL/
│   ├── 03-design/
│   │   └── deliverables/      ← schema Prisma, API design, ERD
│   ├── 04-development/
│   │   ├── _pm/
│   │   └── knowledge/
│   ├── 05-testing/
│   └── 06-deploy/
├── docs/
├── src/
│   ├── adapters/              ← CLI, Web, SDK, ChatGPT adapters
│   ├── importer/              ← ImporterService (RF-001, RF-006)
│   ├── classifier/            ← reglas determinísticas (RF — clasificación)
│   ├── context/               ← ContextService (RF-003)
│   ├── storage/               ← gestión de archivos en filesystem VM
│   └── index.ts
├── prisma/
│   └── schema.prisma
├── storage/                   ← volumen Docker mapeado — archivos de conversaciones
│   └── {agentId}/{YYYY-MM}/{externalSessionId}/
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## 14. SECUENCIA DE IMPLEMENTACIÓN (propuesta)

| Sprint | Contenido | Owner |
|--------|-----------|-------|
| S01 | Schema Prisma `memory_db` + migraciones | DB Engineer |
| S01 | POST /import — CLI adapter + storage en VM | BE |
| S02 | POST /import — SDK adapter (dos archivos, costo) | BE |
| S02 | GET /agents/:id/timeline | BE |
| S03 | GET /conversations/:id/content (para render VTT) | BE |
| S03 | GET /context (contexto runtime < 500ms) | BE |
| S04 | POST /import — Web + ChatGPT adapters | BE |
| S04 | GET /cost-report endpoints | BE |
| S05 | POST /upload (importación manual) | BE |
| S06 | Deploy en VM + integración Hook Manager | DevOps + BE |
| S07 | Rediseño ConversationViewer en VTT | FE (tarea separada) |

---

## 15. REFERENCIAS

| Documento | Uso |
|-----------|-----|
| `2.DISENO_MEMORY_SERVICE_VTT.md` | Diseño anterior — referencia de flujos |
| `ANALISIS_CONVERSACIONES_AGENTES_VTT_v1.2.md` | Modelo de datos base (ADRs 001-015) |
| `1.CONVERSATION_SPEC.md` | Schema real de conversation.jsonl del SDK |
| `1.USAGE_TRACKER_SPEC.md` | Schema real de usage.jsonl del SDK |
| `DIAGRAMAS_SISTEMA_MEMORIA_VTT_v1.0.md` | Diagramas de arquitectura |
| `ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md` | Proceso formal de desarrollo |

---

## 16. PRÓXIMOS PASOS

```
01-PM  ✅ Este documento (v1.2)
02-SA  → Responder Q-01 y Q-04 — modelo funcional detallado, casos de uso
03-AR  → Responder Q-03 y Q-05 — decisiones técnicas de autenticación y async/sync
04-TL  → Schema Prisma, contratos de API, secuencia de implementación confirmada
05-PJM → Plan de sprints, estimación, handoff formal
```

---

**Fin del documento ANALISIS_PM_S01_memory-service.md**
**Versión 1.2 — 2026-04-09 — PM: Martin Rivas**
