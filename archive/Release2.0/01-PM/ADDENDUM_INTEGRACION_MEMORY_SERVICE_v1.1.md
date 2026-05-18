# ADDENDUM: Integración Cross-Module Memory Service

**Versión:** 1.1  
**Fecha:** 2026-04-15  
**Autor:** PM (Martin Rivas)  
**Estado:** ✅ APROBADO PM — INTEGRADO AL SPEC v1.9  
**Firma cierre:** PM Martin Rivas — 2026-04-21  
**Documento base:** SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md (antes v1.8)  
**Documentos upstream:** SPEC_RUNTIME_v1.1.md, SPEC_PROMPT_BUILDER_v1.3.md

---

## ✅ ESTADO DE INTEGRACIÓN (2026-04-21)

Los cambios requeridos por este addendum **ya fueron integrados** en `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`:

| Punto del addendum | Sección del SPEC donde fue integrado | Estado |
|--------------------|---------------------------------------|--------|
| §5.2 — Documentar `platformRefs` para Runtime (`runtime_run_id`, `round`, `orchestrated`) | SPEC §4.1 (modelo `Conversation`, campo `platformRefs`) | ✅ Integrado |
| §5.3 — Agregar índice GIN `idx_conv_runtime_run` | SPEC §6.1 (Partial indexes SQL manual) | ✅ Integrado |
| §5.1 — No crear nueva fuente `RUNTIME_ORCHESTRATED` | SPEC §2.1 (D-MEM-09) + §5 (seed catalog) — ya cumplido | ✅ Cumplido |

**Este addendum queda APROBADO y sus cambios forman parte del SPEC v1.9.** No requiere nuevas acciones técnicas derivadas — solo seguimiento de implementación cuando Runtime/Prompt Builder ejecuten contra los contratos.

---

## 1. PROPÓSITO

Este addendum documenta cómo Memory Service recibe y almacena las conversaciones producidas por Runtime, y cómo Prompt Builder consume el contexto estructurado de Memory. 

**Principio rector:** Memory Service NO decide temas ya cerrados en Runtime v1.1 o Prompt Builder v1.3. Este addendum solo documenta la alineación.

---

## 2. ALINEACIÓN CON RUNTIME v1.1

### 2.1 Granularidad de Persistencia (ya decidida en Runtime)

**Decisión Runtime v1.1:** Una conversación por ronda por agente.

Memory Service recibe y persiste según esta granularidad. No hay opciones A/B/C pendientes.

| Aspecto | Valor (desde Runtime v1.1) |
|---------|---------------------------|
| **Granularidad** | Una conversación por ronda |
| **externalSessionId** | `{run_id}:r{N}:{agentRole}` |
| **Ejemplo** | `run-abc-123:r1:BE` |

### 2.2 Mapeo de Campos Runtime → Memory

| Campo Runtime v1.1 | Campo Memory Service | Notas |
|-------------------|---------------------|-------|
| `run_id` | En `platformRefs.runtime_run_id` | NO es externalSessionId directo |
| `{run_id}:r{N}:{agentRole}` | `externalSessionId` | Formato compuesto de Runtime |
| `project_id` | `projectId` | VTT Project.id, directo |
| `task_id` | `taskId` | VTT Task.id, directo |
| `task_key` | `taskKey` | VTT-123 |
| `agent_user_id` | `primaryAgentId` | VTT User.id del agente |
| `agent_role_code` | `primaryAgentRole` | BE, DB, etc. |
| `started_at` | `startedAt` | Timestamp inicio de ronda |
| `ended_at` | `endedAt` | Timestamp fin de ronda |
| `round_number` | En `platformRefs.round` | Número de ronda (1, 2, ...) |

### 2.3 Source Code (ya decidido en Runtime)

**Decisión Runtime v1.1:** `sourceCode: "CLAUDE_SDK"`

Runtime usa Claude SDK para ejecutar agentes. Memory Service recibe `sourceCode: "CLAUDE_SDK"` en el import, NO una fuente nueva `RUNTIME_ORCHESTRATED`.

```
Runtime ejecuta con Claude SDK
       ↓
POST /import con sourceCode: "CLAUDE_SDK"
       ↓
Memory persiste con sourceId = SourceCatalog("CLAUDE_SDK").id
```

**No se agrega nueva fuente.** CLAUDE_SDK ya existe en el catálogo de Memory Service.

### 2.4 Estructura de platformRefs

Runtime v1.1 define que `platformRefs` contenga:

```json
{
  "runtime_run_id": "run-abc-123",
  "review_chain": ["AR", "DB", "TL"],
  "vtt_task_id": "VTT-142"
}
```

Memory Service persiste este JSON sin modificación.

### 2.5 Endpoint de Import

Runtime usa `POST /api/conversations/import` existente:

```
source: "CLAUDE_SDK"
agentId: {agent_user_id}
agentRole: {agent_role_code}
projectId: {project_id}
taskId: {task_id}
taskKey: {task_key}
externalSessionId: "{run_id}:r{N}:{agentRole}"
platformRefs: { "runtime_run_id": "{run_id}", "round": N, "orchestrated": true }
file: {conversation_jsonl}
```

**No se requiere nuevo endpoint ni nueva fuente.**

---

## 3. CORRELACIÓN DE IDS

### 3.1 Tabla de Correlación (alineada con Runtime v1.1)

| ID | Origen | Campo Memory | Formato |
|----|--------|--------------|---------|
| `project_id` | VTT → Runtime → Memory | `projectId` | UUID |
| `task_id` | VTT → Runtime → Memory | `taskId` | UUID |
| `task_key` | VTT → Runtime → Memory | `taskKey` | VTT-123 |
| `agent_user_id` | VTT → Runtime → Memory | `primaryAgentId` | UUID |
| `agent_role_code` | VTT → Runtime → Memory | `primaryAgentRole` | String (BE, etc.) |
| `run_id` | Runtime | `platformRefs.runtime_run_id` | UUID |
| `round` | Runtime | `platformRefs.round` | Integer |
| `externalSessionId` | Runtime (compuesto) | `externalSessionId` | `{run_id}:r{N}:{agentRole}` |
| `sourceId` | Memory (lookup) | `sourceId` | FK a SourceCatalog(CLAUDE_SDK) |

### 3.2 Idempotencia

La unicidad compuesta `@@unique([sourceId, externalSessionId])` garantiza:
- Mismo run + misma ronda + mismo agente = mismo registro
- Reimport es idempotente (retorna ALREADY_INDEXED)

### 3.3 Trazabilidad de Run Completo

Para obtener todas las conversaciones de un run:

```sql
SELECT * FROM conversation 
WHERE platform_refs->>'runtime_run_id' = 'run-abc-123'
ORDER BY (platform_refs->>'round')::int, primary_agent_role;
```

---

## 4. CONSUMO POR PROMPT BUILDER v1.3

### 4.1 Principio

**Memory Service entrega contexto estructurado (JSON). Prompt Builder lo transforma a texto tokenizado mediante su adapter interno.**

Memory Service NO conoce ni decide:
- Formato de prompts
- Tokenización
- Selección de qué contexto incluir
- Estructura del prompt final

### 4.2 Contrato

Prompt Builder v1.3 consume `GET /api/context` de Memory Service tal como está definido en SPEC_MEMORY_SERVICE_v1.8 §11.

La transformación de JSON a texto ocurre dentro del Memory Context Adapter de Prompt Builder, según lo documentado en SPEC_PROMPT_BUILDER_v1.3.

### 4.3 Responsabilidades

| Responsabilidad | Owner |
|-----------------|-------|
| Persistir conversaciones | Memory Service |
| Clasificar por topics/workType | Memory Service |
| Entregar contexto estructurado | Memory Service |
| Transformar a texto tokenizado | Prompt Builder |
| Seleccionar contexto relevante | Prompt Builder |
| Ensamblar prompt final | Prompt Builder |

---

## 5. CAMBIOS REQUERIDOS EN SPEC BASE

### 5.1 Sin nuevas fuentes

No se agrega `RUNTIME_ORCHESTRATED`. El catálogo existente con `CLAUDE_SDK` es suficiente.

### 5.2 Documentar platformRefs para Runtime

Agregar a §4.1 (Conversation model) la documentación de `platformRefs` cuando `source = CLAUDE_SDK` y viene de Runtime:

```typescript
// platformRefs cuando viene de Runtime orquestado
platformRefs: {
  runtime_run_id: string;  // UUID del run
  round: number;           // Número de ronda (1, 2, ...)
  orchestrated: true;      // Flag que indica origen Runtime
}
```

### 5.3 Agregar índice para queries por run_id

En §6.1 (Índices), agregar:

```sql
-- Para trazabilidad de runs completos
CREATE INDEX idx_conv_runtime_run ON conversation 
  USING gin (platform_refs jsonb_path_ops)
  WHERE platform_refs IS NOT NULL;
```

---

## 6. DECISIONES CERRADAS

| ID | Tema | Decisión | Origen |
|----|------|----------|--------|
| **D-INT-01** | Granularidad persistencia | Una conversación por ronda | Runtime v1.1 |
| **D-INT-02** | Formato externalSessionId | `{run_id}:r{N}:{agentRole}` | Runtime v1.1 |
| **D-INT-03** | Source code | `CLAUDE_SDK` (existente) | Runtime v1.1 |
| **D-INT-04** | Campo run_id | En `platformRefs.runtime_run_id` | Runtime v1.1 |
| **D-INT-05** | Transformación a texto | Responsabilidad de Prompt Builder | PB v1.3 |

**No hay decisiones pendientes.** Este addendum solo documenta alineación con decisiones upstream.

---

## 7. PRÓXIMOS PASOS

1. PM aprueba addendum v1.1
2. Se aplican cambios mínimos a SPEC base (documentación platformRefs + índice GIN)
3. Addendum se anexa como §18 o documento complementario
4. Runtime y Prompt Builder implementan contra contratos ya definidos

---

**Documento:** ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md  
**Versión:** 1.1  
**Estado:** ✅ APROBADO PM — INTEGRADO AL SPEC v1.9  
**Firma cierre:** PM Martin Rivas — 2026-04-21  

---

*Documento base: SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md*  
*Upstream: SPEC_RUNTIME_v1.1.md, SPEC_PROMPT_BUILDER_v1.3.md*
