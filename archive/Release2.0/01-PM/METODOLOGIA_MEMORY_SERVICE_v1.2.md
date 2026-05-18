# METODOLOGÍA: Memory Service

**Versión:** 1.1  
**Fecha:** 2026-04-11  
**Autor:** PM (Martin Rivas) + Claude (Analista)  
**Estado:** LISTO PARA VALIDACIÓN  
**Documento técnico:** SPEC_MEMORY_SERVICE_v1.2.md

---

## CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-11 | Documento inicial |
| 1.1 | 2026-04-11 | Agregada sección 15: UI Standalone. Actualizada D-MEM-10. UI incluida en alcance R1 |

---

## 1. ¿QUÉ ES Y PARA QUÉ SIRVE?

### 1.1 Definición Simple

El Memory Service es el **sistema de memoria centralizado** para los agentes de IA. Piensa en ello como:

- **Un cuaderno de bitácora compartido** (cada agente anota qué hizo)
- **Un asistente que prepara briefs** (antes de trabajar, te dice qué pasó antes)
- **Un contador** (sabe cuánto cuesta cada conversación)
- **Un archivero** (guarda todo organizado por agente y fecha)

### 1.2 Problema que Resuelve

| Sin Memory Service | Con Memory Service |
|--------------------|-------------------|
| Agentes no recuerdan qué hicieron | Historial completo por agente |
| Repiten errores de sesiones pasadas | Contexto inyectado antes de ejecutar |
| No se sabe cuánto cuesta cada tarea | Métricas de costo por agente/proyecto |
| Archivos dispersos en diferentes formatos | Almacenamiento centralizado y organizado |
| El orquestador no puede dar contexto | Hook Manager obtiene contexto en <500ms |

### 1.3 Las 5 Funciones Principales

```
┌─────────────────────────────────────────────────────────────┐
│                FUNCIONES DEL MEMORY SERVICE                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. IMPORTAR CONVERSACIONES                                  │
│     Recibir y guardar conversaciones de 5 fuentes            │
│                                                              │
│  2. CLASIFICAR AUTOMÁTICAMENTE                               │
│     Etiquetar por temas, tipo de trabajo, archivos tocados   │
│                                                              │
│  3. PROVEER CONTEXTO RUNTIME                                 │
│     Dar contexto relevante al orquestador en <500ms          │
│                                                              │
│  4. EXPONER TIMELINE                                         │
│     Mostrar historial acumulado de cada agente               │
│                                                              │
│  5. REPORTAR COSTOS                                          │
│     Métricas de consumo por proyecto/agente/tarea            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. ¿POR QUÉ ES UN SISTEMA INDEPENDIENTE?

### 2.1 Separación de VTT

El Memory Service **NO vive dentro de VTT**. Es un proyecto separado con:

| Aspecto | Memory Service | VTT |
|---------|----------------|-----|
| Base de datos | `memory_db` | `vtt_db` |
| Puerto | 3002 | 3000 |
| Repositorio | Propio | Propio |
| Deploy | Independiente | Independiente |

### 2.2 Beneficios

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  ✅ REUTILIZABLE                                             │
│     Puede servir a múltiples proyectos, no solo VTT          │
│                                                              │
│  ✅ RESILIENTE                                               │
│     Si VTT cae, Memory Service sigue funcionando             │
│                                                              │
│  ✅ ESCALABLE                                                │
│     Puede crecer independientemente según demanda            │
│                                                              │
│  ✅ SIMPLE                                                   │
│     No hereda la complejidad de VTT                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 El Sistema Anterior se Descarta

Existía un módulo llamado **VTM (virtual-teams-memory)** que:
- Corría en localhost, no en la VM
- Almacenaba en archivos locales
- Fue diseñado para visualizar, no para dar contexto a agentes

**Decisión:** VTM se descarta. Memory Service se diseña desde cero.

---

## 3. LAS 5 FUENTES DE CONVERSACIONES

### 3.1 Claude CLI (Claude Code)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Sesiones manuales desde terminal |
| **Quién lo usa** | Desarrolladores usando Claude Code |
| **Formato** | `.jsonl` — una línea por evento |
| **Costo disponible** | ❌ No |

### 3.2 Claude Web

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Export manual desde claude.ai |
| **Quién lo usa** | Cualquiera que exporte conversaciones |
| **Formato** | JSON único |
| **Costo disponible** | ❌ No |

### 3.3 Agent SDK

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Agentes ejecutados programáticamente |
| **Quién lo usa** | El sistema automatizado (Hook Manager) |
| **Formato** | DOS archivos: `session_{id}.json` + `log_{id}.jsonl` |
| **Costo disponible** | ✅ Sí — esta es la única fuente con costo real |

### 3.4 ChatGPT Export

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Export manual desde ChatGPT |
| **Quién lo usa** | Usuarios que trabajan con GPT |
| **Formato** | JSON con estructura `mapping` |
| **Costo disponible** | ❌ No |

### 3.5 VTT Channel (Comunicación Multi-Agente)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Canal de comunicación entre agentes via Google Docs |
| **Quién lo usa** | El orquestador para revisiones entre agentes |
| **Formato** | Markdown con bloques `[VTT_MESSAGE]` |
| **Costo disponible** | ❌ No |
| **Diferencia clave** | Múltiples agentes participan en la misma conversación |

### 3.6 Resumen Visual

```
┌─────────────────────────────────────────────────────────────┐
│                  FUENTES DE CONVERSACIONES                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   CLAUDE_CLI ──────┐                                         │
│   (terminal)       │                                         │
│                    │                                         │
│   CLAUDE_WEB ──────┤                                         │
│   (claude.ai)      │                                         │
│                    ├──────► MEMORY SERVICE ──► memory_db     │
│   CLAUDE_SDK ──────┤         (API:3002)                      │
│   (agentes) ✅$    │              │                          │
│                    │              ▼                          │
│   CHATGPT ─────────┤         /storage/                       │
│   (export)         │         (archivos)                      │
│                    │                                         │
│   VTT_CHANNEL ─────┘                                         │
│   (multi-agente)                                             │
│                                                              │
│   ✅$ = única fuente con costo real                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. TIPOS DE CONVERSACIÓN

### 4.1 Los 3 Tipos

No todas las conversaciones son iguales:

| Tipo | Descripción | Participantes |
|------|-------------|---------------|
| **TASK_EXECUTION** | Un agente ejecuta una tarea | 1 agente |
| **AGENT_REVIEW** | Agentes revisando un entregable | Múltiples agentes |
| **AGENT_CLARIFICATION** | Aclaración puntual entre agentes | 2+ agentes |

### 4.2 ¿Por qué importa?

```
TASK_EXECUTION (normal):
┌─────────────────────────────────────────────────────────────┐
│  Hook Manager lanza BE-Agent para implementar auth          │
│  BE-Agent trabaja solo                                       │
│  Genera session_{id}.json + log_{id}.jsonl                  │
│  Hook Manager importa a Memory Service                       │
└─────────────────────────────────────────────────────────────┘

AGENT_REVIEW (multi-agente):
┌─────────────────────────────────────────────────────────────┐
│  PM-Revisor pide a AR que valide un diseño                  │
│  AR responde con observaciones                               │
│  PM-Revisor responde                                         │
│  TL se suma con comentarios técnicos                         │
│                                                              │
│  Todo queda en un Google Doc con protocolo [VTT_MESSAGE]    │
│  El orquestador importa el canal completo                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. ¿QUIÉN USA EL MEMORY SERVICE?

### 5.1 Hook Manager (Orquestador)

El Hook Manager es el **consumidor principal**:

| Momento | Qué hace | Endpoint |
|---------|----------|----------|
| **ANTES de lanzar agente** | Pide contexto relevante | `GET /api/context` |
| **DESPUÉS de que termina** | Importa la conversación | `POST /api/conversations/import` |

### 5.2 Dashboard VTT

El frontend de VTT consume datos para mostrar:

| Pantalla | Qué consume |
|----------|-------------|
| Timeline de agente | Lista de conversaciones |
| Visor de conversación | Contenido completo |
| Reportes de costo | Métricas agregadas |

### 5.3 PM / TL

Los roles de gestión consultan:

| Consulta | Para qué |
|----------|----------|
| Costo por proyecto | Presupuesto |
| Costo por tarea | Identificar tareas costosas |
| Costo por agente | Ver eficiencia |

### 5.4 Flujo Simplificado

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   1. Hook Manager: "Voy a lanzar BE-Agent"                   │
│                    │                                         │
│                    ▼                                         │
│   2. GET /api/context?agentId=X&taskId=Y                     │
│                    │                                         │
│                    ▼                                         │
│   3. Memory Service: "Aquí tienes contexto:                  │
│                       - Últimas 3 sesiones                   │
│                       - Archivos que toca seguido            │
│                       - Temas relacionados"                  │
│                    │                                         │
│                    ▼                                         │
│   4. Hook Manager inyecta contexto en prompt                 │
│                    │                                         │
│                    ▼                                         │
│   5. BE-Agent ejecuta tarea                                  │
│                    │                                         │
│                    ▼                                         │
│   6. POST /api/conversations/import (archivos generados)     │
│                    │                                         │
│                    ▼                                         │
│   7. Memory Service: "Guardada y clasificada"                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. CONTEXTO RUNTIME (<500ms)

### 6.1 ¿Qué es?

Un resumen compacto de información relevante que se inyecta al agente **antes de ejecutar**.

### 6.2 ¿Por qué debe ser rápido?

```
SIN requisito de velocidad:
  Hook Manager pide contexto
  Memory Service tarda 5 segundos
  Cada lanzamiento de agente se retrasa 5 segundos
  ❌ Cuello de botella

CON requisito <500ms:
  Hook Manager pide contexto
  Memory Service responde en 200ms
  Lanzamiento casi instantáneo
  ✅ Sistema ágil
```

### 6.3 ¿Cómo lo logra?

| Estrategia | Descripción |
|------------|-------------|
| **Solo consulta BD** | NO lee archivos del filesystem |
| **Metadatos pre-indexados** | La clasificación ya está hecha |
| **Índices optimizados** | Queries rápidas por agentId + fecha |
| **Sin LLM** | Reglas determinísticas, no IA |

### 6.4 ¿Qué incluye el contexto?

```
{
  "recentWork": [
    "Implementó middleware de auth hace 2 días",
    "Corrigió bug en jwt.service ayer"
  ],
  "relevantSessions": [
    "Sesión sobre autenticación (VTT-120)",
    "Sesión sobre JWT refresh (VTT-118)"
  ],
  "filesFrequentlyModified": [
    "src/auth.service.ts",
    "src/middleware/auth.ts"
  ],
  "estimatedCostUsd": 0.50
}
```

---

## 7. ALMACENAMIENTO DE ARCHIVOS

### 7.1 Principio Fundamental

> **Los archivos originales se guardan COMPLETOS. La BD guarda solo METADATOS.**

Esto significa:
- El JSONL completo vive en el filesystem
- La BD tiene índices y resúmenes para búsqueda rápida
- Se puede reconstruir cualquier conversación leyendo el archivo

### 7.2 Organización

```
/storage/
└── {agentId}/
    └── {YYYY-MM}/
        └── {externalSessionId}/
            ├── session.json     # Historial
            ├── log.jsonl        # Eventos + costo (SDK)
            └── attachments/     # Archivos adjuntos (si hay)
```

### 7.3 ¿Por qué no guardar todo en BD?

| Guardar en BD | Guardar en Filesystem |
|---------------|----------------------|
| BD se vuelve enorme | BD liviana |
| Backups lentos | Backups separados |
| Queries sobre texto = lento | Queries sobre metadatos = rápido |
| Difícil de inspeccionar | Archivos legibles directamente |

---

## 8. CLASIFICACIÓN AUTOMÁTICA

### 8.1 ¿Qué es?

Cuando se importa una conversación, el sistema la **etiqueta automáticamente** para búsqueda.

### 8.2 ¿Qué se clasifica?

| Clasificación | Ejemplos | Cómo se detecta |
|---------------|----------|-----------------|
| **Temas** | authentication, database, frontend | Keywords en archivos y tool calls |
| **Tipo de trabajo** | implementation, bug-fix, review | Patrones en el contenido |
| **Archivos modificados** | src/auth.ts, prisma/schema.prisma | Extraídos de tool_use blocks |
| **Entidades** | AuthService, PrismaClient | Nombres detectados en paths |

### 8.3 ¿Por qué reglas y no IA?

| Reglas determinísticas | LLM |
|------------------------|-----|
| Predecible | Variable |
| Instantáneo | Tarda segundos |
| Sin costo | Cuesta tokens |
| Suficiente para R1 | Mejor para R2+ |

**Decisión:** R1 usa reglas. LLM y embeddings vienen en fases futuras.

---

## 9. CATÁLOGOS EXTENSIBLES

### 9.1 ¿Qué son?

En lugar de hardcodear valores como `CLAUDE_CLI`, `PENDING`, `bug-fix`, usamos **tablas de catálogo** en la BD.

### 9.2 ¿Por qué?

```
CON ENUMS HARDCODEADOS:
  Quiero agregar nueva fuente "GEMINI"
  Tengo que cambiar el código
  Tengo que hacer migración de BD
  Tengo que hacer deploy
  ❌ Fricción

CON CATÁLOGOS EN BD:
  Quiero agregar nueva fuente "GEMINI"
  INSERT INTO source_catalog (code, label) VALUES ('GEMINI', 'Google Gemini')
  ✅ Listo, sin deploy
```

### 9.3 Catálogos del Sistema

| Catálogo | Valores iniciales |
|----------|------------------|
| **SourceCatalog** | CLAUDE_CLI, CLAUDE_WEB, CLAUDE_SDK, CHATGPT, VTT_CHANNEL |
| **ConversationTypeCatalog** | TASK_EXECUTION, AGENT_REVIEW, AGENT_CLARIFICATION |
| **ConversationStatusCatalog** | PENDING, PROCESSING, IMPORTED, ERROR |
| **WorkTypeCatalog** | implementation, bug-fix, review, migration, deploy |
| **BlockTypeCatalog** | TEXT, TOOL_USE, TOOL_RESULT, THINKING |
| **TopicCatalog** | authentication, database, frontend, backend, testing... |
| **PriorityCatalog** | HIGH, MEDIUM, LOW |

---

## 10. IDEMPOTENCIA Y ATOMICIDAD

### 10.1 Idempotencia

> Si importo la misma conversación dos veces, no se duplica.

```
Primera importación:
  POST /import { externalSessionId: "abc123", ... }
  → 201 Created { status: "IMPORTED" }

Segunda importación (mismo ID):
  POST /import { externalSessionId: "abc123", ... }
  → 200 OK { status: "ALREADY_INDEXED" }

✅ No hay duplicados
✅ No hay error
✅ Reintentos seguros
```

### 10.2 Atomicidad por Compensación

¿Qué pasa si falla a mitad del proceso?

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  PASO 1: INSERT Conversation { status: PENDING }             │
│          ✅ Registro creado                                  │
│                                                              │
│  PASO 2: Escribir archivo en /storage/                       │
│          ❌ FALLA (disco lleno, permiso, etc.)               │
│                                                              │
│  RESULTADO:                                                  │
│  - Registro queda en status = PENDING                        │
│  - Job de cleanup lo detecta                                 │
│  - Reintenta o marca como ERROR                              │
│  - NO hay registros fantasma sin archivo                     │
│                                                              │
│  PASO 3 (si paso 2 OK):                                      │
│          UPDATE { status: IMPORTED, filePath: "..." }        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 11. DIFERENCIA CON SUBMÓDULO 5F

### 11.1 ¿Son lo mismo?

**NO.** Son módulos complementarios con propósitos diferentes:

| Aspecto | Memory Service | Submódulo 5F |
|---------|----------------|--------------|
| **Propósito** | Memoria y contexto para agentes | Auditoría de costos para PM |
| **Ubicación** | Proyecto independiente | Dentro de VTT |
| **BD** | `memory_db` | `vtt_db` |
| **Fuentes** | 5 fuentes | Solo CLI |
| **Carga** | Automática via Hook Manager | Manual via upload |
| **Costo** | Solo SDK tiene real | Calcula desde pricing catalog |

### 11.2 ¿Por qué existen ambos?

```
MEMORY SERVICE:
  "¿Qué contexto le doy al agente antes de ejecutar?"
  "¿Qué hizo este agente en el pasado?"

SUBMÓDULO 5F:
  "¿Cuánto me costó esta sesión de Claude Code?"
  "¿Cuánto llevo gastado este mes en Claude?"
```

---

## 12. PREGUNTAS FRECUENTES

### 12.1 ¿El Memory Service consulta a VTT?

**No.** El Hook Manager envía `taskTitle` y otros datos desnormalizados al importar. Memory Service no llama a VTT en runtime.

### 12.2 ¿Qué pasa si pierdo los archivos de /storage/?

Los archivos son la fuente de verdad del contenido completo. La BD solo tiene metadatos. Si pierdes /storage/, pierdes el contenido pero mantienes los índices.

**Recomendación:** Backups regulares de /storage/.

### 12.3 ¿Por qué <500ms para contexto?

Se ejecuta ANTES de cada lanzamiento de agente. Si tarda, todo el sistema se vuelve lento. 500ms es el máximo tolerable.

### 12.4 ¿Puedo agregar nuevas fuentes?

Sí. El campo `source` referencia un catálogo extensible. Solo insertas en `SourceCatalog` y creas un nuevo Adapter.

### 12.5 ¿Por qué no usar LLM para clasificar?

En R1, las reglas son suficientes, predecibles, y sin costo. LLM viene en R2+ cuando se necesite clasificación más inteligente.

### 12.6 ¿Qué es `platformRefs`?

Permite vincular sesiones que son parte del mismo trabajo lógico pero en diferentes plataformas:

```json
{
  "platformRefs": {
    "claude_web": "01e4b085-...",
    "claude_code": "04841bcf-..."
  }
}
```

"Esta sesión de Claude Code continúa lo que empecé en Claude Web."

---

## 13. GLOSARIO

| Término | Definición |
|---------|------------|
| **Agente** | Instancia de IA que ejecuta tareas (BE-Agent, FE-Agent, TL-Agent) |
| **Bloque** | Unidad dentro de un turno: texto, tool_use, tool_result, thinking |
| **Catálogo** | Tabla de BD que contiene valores extensibles (fuentes, tipos, estados) |
| **Clasificación** | Etiquetas asignadas automáticamente (temas, tipo de trabajo, archivos) |
| **Contexto runtime** | Resumen compacto inyectado en prompt antes de ejecutar (<500ms) |
| **Conversación** | Sesión completa de trabajo entre usuario/sistema y agente |
| **externalSessionId** | ID original de la sesión en la fuente (para idempotencia) |
| **Hook Manager** | Orquestador que lanza agentes y reporta resultados |
| **Idempotencia** | Operación que puede ejecutarse múltiples veces sin duplicar |
| **Join table** | Tabla intermedia para relaciones muchos-a-muchos |
| **Metadatos** | Información sobre la conversación sin el contenido completo |
| **Source / Fuente** | Origen de la conversación (CLI, Web, SDK, ChatGPT, VTT_CHANNEL) |
| **Timeline** | Línea de tiempo de todas las conversaciones de un agente |
| **Token** | Unidad de texto procesada por el modelo de IA |
| **Turno** | Un intercambio: mensaje del usuario + respuesta del agente |
| **VTM** | Virtual Teams Memory — módulo anterior que se descarta |
| **VTT_CHANNEL** | Canal de comunicación multi-agente via Google Docs |

---

## 14. DECISIONES TOMADAS

| ID | Decisión | Opción elegida | Por qué |
|----|----------|----------------|---------|
| **D-MEM-01** | Sistema independiente | Proyecto y BD propios | Reutilizable, resiliente |
| **D-MEM-02** | VTM legacy | Se descarta | Diseño incompatible |
| **D-MEM-03** | Archivos | Copiar a VM | Memory Service no accede filesystem remoto |
| **D-MEM-04** | SDK | Envía 2 archivos | Costo está en log, no en session |
| **D-MEM-05** | Duplicados | Idempotencia por externalSessionId | Reintentos seguros |
| **D-MEM-06** | Storage | Organizado por agente/fecha | Fácil de navegar |
| **D-MEM-07** | Contexto | <500ms obligatorio | No ser cuello de botella |
| **D-MEM-08** | Clasificación R1 | Reglas determinísticas | Simple, predecible, sin costo |
| **D-MEM-09** | Fuentes | Catálogo extensible | Sin migración para agregar |
| **D-MEM-10** | UI | App standalone separada (puerto 3003) | Independiente de VTT FE |
| **D-MEM-11** | IDs | String (TEXT) no UUID nativo | Consistente con VTT |
| **D-MEM-12** | taskId | Task.id (UUID) + taskKey auxiliar | FK real + código legible |
| **D-MEM-13** | taskTitle | Desnormalizado en import | No llamar a VTT en runtime |
| **D-MEM-14** | Status | PENDING → PROCESSING → IMPORTED/ERROR | Atomicidad por compensación |
| **D-MEM-15** | Fallo escritura | Queda PENDING, job reintenta | Sin registros fantasma |
| **D-MEM-16** | Endpoints | Separados para JSONL vs VTT_CHANNEL | Payloads incompatibles |
| **D-MEM-17** | conversationType | Discriminador (TASK/REVIEW/CLARIFICATION) | Diferencia 1 agente vs N agentes |
| **D-MEM-18** | VTT_CHANNEL | Import incremental | Google Docs son append-only |
| **D-MEM-19** | platformRefs | JSON nullable | Vincular sesiones cross-platform |
| **D-MEM-20** | JSONL | Almacenar completo, sin stripping | BD solo indexa metadata |
| **D-MEM-21** | Entregables | Responsabilidad del Hook Manager | Memory Service no participa |
| **D-MEM-22** | Tipos/clasificaciones | Catálogos en BD | Sin enums, sin migración |
| **D-MEM-23** | topics/entities | Join tables | No arrays String[], relacional |

---

## 15. INTERFAZ DE USUARIO (UI)

### 15.1 ¿Cómo veo las conversaciones?

El Memory Service incluye una **aplicación web standalone** para visualizar datos. No está integrada en VTT — corre en su propio puerto (3003).

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   Memory Service UI                                          │
│   http://{host}:3003                                         │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Dashboard  │ Agentes │ Conversaciones │ Import │... │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
│                       ↓ Consume                              │
│                                                              │
│   Memory Service API                                         │
│   http://{host}:3002/api/...                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 15.2 ¿Qué puedo hacer en la UI?

| Pantalla | Para qué sirve |
|----------|---------------|
| **Dashboard** | Vista rápida: total de conversaciones, costos, actividad reciente |
| **Agentes** | Ver lista de agentes con sus estadísticas |
| **Timeline** | Ver historial cronológico de un agente específico |
| **Conversation Viewer** | Ver contenido completo de una sesión de trabajo |
| **Review Viewer** | Ver thread de mensajes entre agentes (revisiones) |
| **Cost Report** | Ver cuánto ha costado un proyecto o agente |
| **Import Manual** | Subir archivos de conversación manualmente |
| **Health** | Ver estado del servicio y errores pendientes |

### 15.3 ¿Cómo se ve una conversación de trabajo?

```
┌─────────────────────┬────────────────────────────────────────┐
│ METADATA            │ CONVERSACIÓN                           │
│                     │                                        │
│ Task: VTT-123       │ ┌── Usuario ────────────────────────┐  │
│ Agente: BE-Agent    │ │ Implementa el auth service con    │  │
│ Turnos: 18          │ │ JWT y refresh tokens...           │  │
│ Costo: $0.82        │ └───────────────────────────────────┘  │
│                     │                                        │
│ ARCHIVOS:           │ ┌── Asistente ──────────────────────┐  │
│ • auth.service.ts   │ │ Voy a crear el servicio...        │  │
│ • schema.prisma     │ │                                   │  │
│                     │ │ ▶ Write  src/auth.service.ts      │  │
│                     │ │ ▶ Bash   npx prisma migrate       │  │
│                     │ └───────────────────────────────────┘  │
└─────────────────────┴────────────────────────────────────────┘
```

### 15.4 ¿Cómo se ve una revisión multi-agente?

```
┌─────────────────────┬────────────────────────────────────────┐
│ PARTICIPANTES       │ THREAD                                 │
│                     │                                        │
│ 👤 PM_REVISOR       │ ┌── PM → AR ─────────────────────────┐ │
│ 👤 AR               │ │ PM-001 | Validar modelo v4         │ │
│ 👤 TL               │ │ Necesito tu review del diseño...  │ │
│                     │ └────────────────────────────────────┘ │
│                     │    │                                   │
│                     │    └─ ┌── AR → PM ─────────────────┐   │
│                     │       │ AR-001 | 3 observaciones    │   │
│                     │       │ Revisé y encontré...        │   │
│                     │       └─────────────────────────────┘   │
└─────────────────────┴────────────────────────────────────────┘
```

### 15.5 ¿Necesito autenticación?

**En R1: No.** La UI es de acceso directo — solo necesitas la URL.

En R2+ se agregará autenticación con el mismo patrón que VTT (JWT).

---

## 16. ALCANCE R1 Y EXCLUSIONES

### 16.1 Incluido en R1

| Funcionalidad | Descripción |
|---------------|-------------|
| Import de 5 fuentes | CLI, Web, SDK, ChatGPT, VTT_CHANNEL |
| Clasificación por reglas | Topics, workType, files, entities |
| Timeline por agente | Historial acumulado ordenado |
| Contexto runtime <500ms | Para Hook Manager |
| Lectura de contenido | Ver conversación completa |
| Reportes de costo | Por proyecto/agente/tarea |
| Catálogos extensibles | Sin hardcoding |
| **UI Standalone** | Dashboard, Timeline, Viewers, Import, Costs |

### 16.2 Excluido de R1 (fases futuras)

| Funcionalidad | Fase |
|---------------|------|
| Búsqueda semántica / embeddings | R2 |
| Full-text search sobre contenido | R2 |
| Clasificación por LLM | R3 |
| Multi-agente en TASK_EXECUTION | R2 |
| RBAC / workspaceId | Cuando VTT lo active |
| Retención automática (purge) | R2 |
| Auth en UI | R2 |
| Dark mode UI | R2 |
| Export PDF/CSV | R2 |

---

**Documento:** METODOLOGIA_MEMORY_SERVICE_v1.1.md  
**Versión:** 1.1  
**Estado:** LISTO PARA VALIDACIÓN  

---

*Documento técnico relacionado: SPEC_MEMORY_SERVICE_v1.2.md*
