# VTT.PROTOCOL-DEV-001 — Ciclo de vida del Devlog Entry

| Campo | Valor |
|---|---|
| **Código** | `VTT.PROTOCOL-DEV-001` |
| **Título** | Ciclo de vida del Devlog Entry (creación → review → cierre de sprint) |
| **Versión** | 1.1.0 |
| **Fecha** | 2026-06-02 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | Agentes ejecutores, TL Reviewer, PM (cierre de sprint), QA (durante review) |
| **Estado** | Aprobado para uso |
| **Tipo** | Genérico VTT — aplica a cualquier proyecto y cualquier fase del SDLC |
| **Reglas aplicables (Nivel 0)** | Ver `00.Rules/rules_catalog.json` — Review Gate bloquea con entries `critical`/`high` no resueltas |
| **Feature origen** | `Docs/01-documentacion/features mod dinamico/FEATURE_DEVLOG_LIFECYCLE.md` |
| **Endpoints VTT cubiertos** | `POST/PATCH/DELETE /api/tasks/:taskId/devlog[/:entryId][/status]` |
| **Protocols relacionados** | `VTT.PROTOCOL-ASG-001` (el devlog se mueve dentro del ciclo de asignación; §5.4 / §5.4.bis son los destinos de escalación cuando una entry `issue` debe convertirse en Issue formal — ver §6.3), `VTT.PROTOCOL-MAN-001` (el TL registra `devlog_resolved_count` en el manifest v1.5) |

---

## Tabla de Contenido

1. [Propósito](#1-propósito)
2. [Campo de Aplicación](#2-campo-de-aplicación)
3. [Responsabilidades](#3-responsabilidades)
4. [Definiciones](#4-definiciones)
5. [Procedimiento](#5-procedimiento)
   - 5.1 [FASE 1 — Creación durante ejecución (agente)](#51-fase-1--creación-durante-ejecución)
   - 5.2 [FASE 2 — Review Gate (verificación automática)](#52-fase-2--review-gate)
   - 5.3 [FASE 3 — Procesamiento en code review (TL)](#53-fase-3--procesamiento-en-code-review)
   - 5.4 [FASE 4 — Cierre de devlog al cierre de sprint (TL + PM)](#54-fase-4--cierre-de-devlog-al-cierre-de-sprint)
6. [Referencias Cruzadas](#6-referencias-cruzadas)
7. [Reglas críticas](#7-reglas-críticas)
8. [Resumen de Revisiones](#8-resumen-de-revisiones)

---

## 1. Propósito

Establecer el proceso normativo único para crear, transicionar y cerrar **devlog entries** durante el ciclo de vida de una tarea VTT y de un sprint completo.

Un devlog entry es una unidad de **trazabilidad** generada durante la ejecución de una tarea: decisión técnica, observación, deuda detectada, bloqueante, nota de testing o riesgo. Cada entry nace en `pending` y debe avanzar **explícitamente** a un estado terminal (`resolved` / `wont_fix` / `deferred`) antes del cierre del sprint.

> **Por qué existe este Protocol:** sin gobernanza unificada los agentes registran entries inconsistentes, el TL no sabe cuándo procesarlas, los entries `critical`/`high` quedan colgando y el Review Gate bloquea sprints completos. Este Protocol unifica los 3 momentos del lifecycle (creación, review, cierre) en un solo proceso end-to-end con responsabilidades claras por rol.

---

## 2. Campo de Aplicación

Aplica a:

- **Toda tarea VTT** que pase por `task_in_progress → task_in_review → task_completed`
- **Todo sprint VTT** al ejecutar su cierre formal (todas las tareas del sprint en estado terminal)
- Cualquier rol ejecutor que pueda detectar decisiones, observaciones, blockers, tech debt, testing notes, risks o issues durante su trabajo
- Cualquier categoría de tarea (development, deployment, devops, documentation, testing, design)

No aplica a:

- **Comentarios** en tareas (`POST /api/tasks/:id/comments`) — eso es comunicación, no trazabilidad
- **Issues bloqueantes activos** que paran la tarea — usar `VTT.SKILL-ISS-001` (issue, no devlog)
- Devlog de procesos internos VTT (código del backend) — fuera de scope

---

## 3. Responsabilidades

### 3.1 Agente ejecutor

- Crear devlog entries **durante** la ejecución de su tarea, cuando detecte:
  - Decisión técnica activa → `categoryCode: decision`
  - Observación de comportamiento → `categoryCode: observation`
  - Deuda técnica fuera de scope → `categoryCode: tech_debt`
  - Bloqueante real → `categoryCode: blocker`
  - Nota de testing / resultado de verificación → `categoryCode: testing_note`
  - Riesgo identificado → `categoryCode: risk`
  - Issue/inconsistencia (no bug) → `categoryCode: issue`
- Garantizar que toda entry tenga `description` con contexto real (caso MS-333: entries sin description son borradas)
- **NO** transicionar entries propias a estado terminal sin revisión del TL (excepto correcciones propias y re-creaciones)
- Antes de mover la tarea a `task_in_review`, verificar que no hay entries `critical`/`high` en estado no terminal que vaya a bloquear el Review Gate

### 3.2 TL Reviewer

- Leer **todas** las entries del devlog de la tarea durante el code review
- Procesar cada entry: `pending → acknowledged` (reconocer) y eventualmente a estado terminal
- Para entries de severidad `critical`/`high` que bloquean el Review Gate: resolver o coordinar con PM antes de hacer PASS
- Registrar el conteo de entries resueltas en el Task Manifest v1.5 (`delivery.dynamic_model_actions.devlog_resolved_count`)
- Detectar entries duplicadas/erróneas y borrarlas con `VTT.SKILL-DEV-005` (siempre con comment de trazabilidad previo)
- Si decide `wont_fix` o `deferred`, exigir justificación en `resolution` o `deferredToPhaseId`

### 3.3 PM (cierre de sprint)

- Antes de cerrar un sprint: verificar que **0 entries** quedan en estados no terminales en **todas** las tareas del sprint
- Decidir qué entries van a `wont_fix` (no se va a resolver) vs `deferred` (se pospone a sprint futuro)
- Asignar `deferredToPhaseId` (UUID de la fase destino) para entries `deferred`
- Cuando un entry `deferred` resulta en una tarea concreta del sprint siguiente, registrar `fixTaskId` con esa tarea

### 3.4 QA (durante review de tareas con `task_in_review`)

- Crear entries `testing_note` con resultados de las pruebas que ejecuta
- Promover hallazgos críticos a `issue` o `blocker` según corresponda
- Procesar entries propias antes de cerrar su pase de testing

---

## 4. Definiciones

**Devlog entry:** unidad de trazabilidad creada durante la ejecución de una tarea. Cada entry tiene `categoryCode`, `title`, `description`, opcionalmente `severity`, y un `status` del lifecycle. Persiste en la tabla `task_devlog_entries`.

**Lifecycle:** secuencia de estados que un entry recorre desde su creación (`pending`) hasta un estado terminal (`resolved` / `wont_fix` / `deferred`). Las transiciones son **irreversibles**.

**Estado terminal:** `resolved`, `wont_fix` o `deferred`. Una vez en estado terminal, el entry no puede cambiar más — `PATCH /status` retorna `400 ENTRY_ALREADY_FINAL`. Único workaround: borrar con `VTT.SKILL-DEV-005` y recrear.

**Review Gate:** validación automática del backend al intentar mover una tarea a `task_in_review` o `task_completed`. Bloquea (422) si hay entries `critical`/`high` en estado no terminal (`pending` / `acknowledged` / `in_progress`).

**Severidad bloqueante:** `critical` y `high`. Las severidades `medium`, `low` y los entries sin severidad (`decision`, `observation`) **NO** bloquean el gate, pero igualmente deben llegar a estado terminal antes del cierre de sprint.

**Categorías con severidad:** `blocker`, `tech_debt`, `testing_note`, `risk`, `issue`. Categorías **sin** severidad: `decision`, `observation`.

**Resolution:** texto obligatorio cuando se transiciona a `resolved` o `wont_fix`. Es el registro auditable de **cómo se resolvió** o **por qué se decidió no resolver**.

**`deferredToPhaseId`:** UUID de la fase destino cuando un entry se difiere. Obligatorio para `status=deferred`.

**`fixTaskId`:** ID de tarea que resuelve el entry (recomendado en `resolved` formal, opcional en otros casos). Permite trazar el devlog al PR que lo cerró.

**Auto side-effects del backend en transiciones terminales:**

| Transición | `resolvedAt` | `resolvedBy` | Limpia `resolution` |
|---|:---:|:---:|:---:|
| → `resolved` | NOW() | `reportedBy` original | — |
| → `wont_fix` | NOW() | (null, no fue resuelto) | — |
| → `deferred` | (limpia) | (limpia) | (limpia) |

---

## 5. Procedimiento

El ciclo se divide en 4 fases. Las fases 1 y 3 se ejecutan **por tarea**. La fase 2 es **automática del backend**. La fase 4 se ejecuta **una vez al cierre de sprint**.

```
┌─────────────────────────────────────────────────────────────────┐
│  FASE 1  — Agente crea entries durante task_in_progress         │
│            (categoryCode + title + description + severity?)     │
│            → entries quedan en status: pending                  │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 2  — Agente mueve tarea a task_in_review                  │
│            Review Gate verifica entries critical/high           │
│            → si bloquea: 422  → si OK: continúa                 │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 3  — TL procesa devlog en code review                     │
│            pending → acknowledged → resolved/wont_fix/deferred  │
│            Registra devlog_resolved_count en manifest v1.5      │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 4  — Cierre de sprint                                     │
│            Iterar tareas del sprint                             │
│            0 entries no-terminales → cierre formal OK           │
└─────────────────────────────────────────────────────────────────┘
```

### 5.1 FASE 1 — Creación durante ejecución

**Quién:** Agente ejecutor (incluye QA durante su pase de testing)
**Cuándo:** En cualquier momento mientras la tarea esté en `task_in_progress` o `task_in_review`
**Workflow:** Ver `VTT.WORKFLOW-DEV-001.001` (Crear devlog entries durante ejecución)

#### 5.1.1 Identificación

El agente detecta uno de los 7 tipos de evento durante su trabajo:

| Evento | `categoryCode` | Severidad |
|---|---|---|
| Tomó una decisión técnica con trade-off explícito | `decision` | — (no usa) |
| Observó comportamiento/contexto a documentar | `observation` | — (no usa) |
| Detectó bloqueante real que impide avanzar | `blocker` | `critical`/`high` |
| Detectó deuda técnica fuera del scope actual | `tech_debt` | `low`/`medium` típicamente |
| Ejecutó testing y registra resultado | `testing_note` | según resultado |
| Identificó riesgo potencial | `risk` | según probabilidad |
| Detectó inconsistencia (no bug) | `issue` | según gravedad |

#### 5.1.2 Decisión: ¿devlog, comment o issue?

Primer corte — qué herramienta usar según la naturaleza del registro:

| Si... | Usar |
|---|---|
| Trazabilidad de decisión/observación/finding | **Devlog entry** (esta fase) |
| Comunicación con el equipo, no requiere trazabilidad | Comment (`VTT.SKILL-COMMENT-001`) |
| Bloqueante real que detiene la tarea ahora | Issue (`VTT.SKILL-ISS-001`) + on_hold |

#### 5.1.2.bis Cuándo una entry devlog escala a Issue formal (frontera con ASG-001 §5.4 / §5.4.bis)

Algunas categorías de entry pueden volverse bloqueantes técnicos o consultas formales que exceden el ámbito del devlog y requieren un **Issue formal** procesado por el sub-ciclo correspondiente del `VTT.PROTOCOL-ASG-001`. La siguiente tabla define la frontera:

| `categoryCode` de la entry | Acción del agente | ¿Escala a Issue formal? | Sub-ciclo destino |
|---|---|---|---|
| `decision` | registrar y seguir | no | — |
| `observation` | registrar y seguir | no | — |
| `tech_debt` | registrar + derivar tarea futura | no (queda en devlog) | — |
| `issue` (no-bug, no-blocker) | registrar y seguir | no | — |
| `issue` con síntoma `bug`/`blocker` (severity `high`/`critical`) | crear Issue formal + mover tarea a `task_on_hold` | **sí** — `POST /api/tasks/:id/issues` con `type=bug` o `type=blocker` | `VTT.PROTOCOL-ASG-001` §5.4 |
| `issue` con síntoma `question` (severity `low`/`medium`, NUNCA `high`/`critical`) | crear Issue formal sin `on_hold` | **sí** — `POST /api/tasks/:id/issues` con `type=question` | `VTT.PROTOCOL-ASG-001` §5.4.bis |

> **Heurística de ASG-001 §4 para distinguir `bug`/`blocker` vs `question`:**
> - "¿Debería hacer X o Y?" (decisión de diseño/scope/criterio) → `question`
> - "X no funciona, error Y al ejecutar Z" (síntoma técnico) → `bug` o `blocker` según severidad
> - Si la pregunta sube a severity `high`/`critical` → ya no es pregunta, es blocker → `§5.4` con `task_on_hold`

#### 5.1.3 Creación

- Invocar `VTT.WORKFLOW-DEV-001.001` con `categoryCode`, `title`, `description`, `severity?`, `reportedBy`
- El workflow invoca `VTT.SKILL-DEV-001` (decisión) o `VTT.SKILL-DEV-002` (observación) o equivalentes
- Entry nace en `status: pending`

#### 5.1.4 Corrección durante ejecución

Si el agente detecta que un entry propio tiene typo o le falta contexto:

- Para corregir contenido (title/description/severity) → `VTT.SKILL-DEV-003` (edit)
- Si el entry fue creado por error y debe eliminarse → `VTT.SKILL-DEV-005` (delete) con comment de trazabilidad previo

> **Regla:** el agente **NO** transiciona entries propias a estado terminal en esta fase. Los estados terminales los aplica el TL en la FASE 3 (con excepción del caso `deferred` previo coordinado con PM).

### 5.2 FASE 2 — Review Gate

**Quién:** Backend VTT (automático)
**Cuándo:** Al ejecutar `PATCH /api/tasks/:id/status` con destino `task_in_review` o `task_completed`

El Review Gate verifica devlog entries según esta tabla:

| Condición | Resultado |
|---|---|
| Entries `critical` o `high` en `pending`/`acknowledged`/`in_progress` | 🔴 **BLOQUEADO** — HTTP 422 |
| Entries `critical` o `high` en `resolved`/`wont_fix`/`deferred` | ✅ OK |
| Entries `medium`/`low` en cualquier estado | ✅ OK (no bloquean) |
| Entries sin severidad (`decision`/`observation`) | ✅ OK (no bloquean) |

> **Comportamiento crítico:** el Review Gate NO bloquea por entries `pending` de baja severidad, pero la **política operativa** exige que TODOS los entries lleguen a estado terminal antes de la FASE 4 (cierre de sprint). El TL no debe pasar a `task_completed` con entries no-terminales aunque el gate lo permita.

Si el gate bloquea:

1. Agente identifica las entries bloqueantes con `GET /api/tasks/:id/devlog`
2. Coordina con el TL: ¿se resuelven antes de review o el TL las resuelve en FASE 3?
3. Si el agente puede resolver (es trabajo propio del scope): invoca `VTT.SKILL-DEV-004` (lifecycle) con `resolved` + `resolution` + `fixTaskId`
4. Reintenta el cambio de status

### 5.3 FASE 3 — Procesamiento en code review

**Quién:** TL Reviewer
**Cuándo:** Cuando la tarea está en `task_in_review` y el TL realiza el code review
**Workflow:** Ver `VTT.WORKFLOW-DEV-001.002` (Procesar devlog en code review)

#### 5.3.1 Lectura del devlog

- TL ejecuta `GET /api/tasks/:id/devlog` y lee TODAS las entries (no solo las bloqueantes)
- Identifica entries duplicadas/erróneas para borrar (con `VTT.SKILL-DEV-005`)
- Identifica entries con contenido a corregir (con `VTT.SKILL-DEV-003`)

#### 5.3.2 Decisión por entry

Para cada entry no-terminal, el TL decide el destino:

| Si... | Aplicar |
|---|---|
| El finding fue corregido en código (PR existe) | `resolved` con `resolution` describiendo el fix + `fixTaskId` si aplica |
| La decisión fue documentada y se acepta | `resolved` con `resolution: "Decisión documentada y aceptada"` |
| Es un finding que se decide NO arreglar (con justificación) | `wont_fix` con `resolution` explicando por qué |
| El finding se pospone a otro sprint/fase | `deferred` con `deferredToPhaseId` del destino |
| El TL no decide todavía y necesita más contexto | `acknowledged` (intermedio, NO es terminal) |
| Entry duplicado/erróneo, sin valor | DELETE con `VTT.SKILL-DEV-005` (comment de trazabilidad previo) |

#### 5.3.3 Ejecución

- Invocar `VTT.WORKFLOW-DEV-001.002` que orquesta `VTT.SKILL-DEV-004` (lifecycle) para cada transición
- Para entries `critical`/`high` que el TL no puede decidir solo: escalar a PM

#### 5.3.4 Registro en Manifest v1.5

Al terminar el procesamiento, el TL debe registrar en el Task Manifest v1.5 (ver `VTT.PROTOCOL-MAN-001` §5.4):

```json
{
  "delivery": {
    "dynamic_model_actions": {
      "devlog_resolved_count": 7,
      "devlog_wontfix_count": 1,
      "devlog_deferred_count": 2,
      "devlog_deleted_count": 0
    }
  }
}
```

#### 5.3.5 PASS del code review

- 0 entries no-terminales → TL puede ejecutar PASS y mover la tarea a `task_completed`
- Si quedan entries `acknowledged` sin terminal: NO hacer PASS — completar la decisión primero

### 5.4 FASE 4 — Cierre de devlog al cierre de sprint

**Quién:** TL + PM
**Cuándo:** Al ejecutar el cierre formal del sprint (antes del reporte M / milestone)
**Workflow:** Ver `VTT.WORKFLOW-DEV-001.003` (Cerrar devlog al cerrar sprint)

#### 5.4.1 Auditoría

- Iterar TODAS las tareas del sprint
- Para cada tarea, `GET /api/tasks/:id/devlog`
- Filtrar entries con `status ∈ {pending, acknowledged, in_progress}`
- Generar listado de entries pendientes con: `taskId`, `entryId`, `categoryCode`, `severity`, `title`

#### 5.4.2 Decisión PM por cada entry pendiente

| Si... | Acción |
|---|---|
| Es resoluble inmediatamente (hay fix listo) | `resolved` con `resolution` + `fixTaskId` |
| No se va a resolver — comportamiento aceptado | `wont_fix` con `resolution` explicando |
| Va a sprint S+1, S+2 o release futuro | `deferred` con `deferredToPhaseId` |

#### 5.4.3 Validación

- Re-ejecutar la auditoría del 5.4.1
- Confirmar que **0 entries** quedan en estados no terminales
- Si quedan: NO cerrar sprint — iterar hasta llegar a 0

#### 5.4.4 Reporte M

Una vez confirmado 0 pending, generar el reporte M del sprint con el resumen del devlog procesado:

- Total entries del sprint (por categoryCode)
- Total resueltas vs deferidas vs wont_fix
- Listado de `deferred` con destino (sprint/release/tarea futura)

---

## 6. Referencias Cruzadas

### 6.1 Workflows hijos

| Código | Documento | Quién ejecuta |
|---|---|---|
| `VTT.WORKFLOW-DEV-001.001` | Crear devlog entries durante ejecución | Agente ejecutor |
| `VTT.WORKFLOW-DEV-001.002` | Procesar devlog en code review | TL Reviewer |
| `VTT.WORKFLOW-DEV-001.003` | Cerrar devlog al cerrar sprint | TL + PM |

### 6.2 Skills invocadas (Nivel 2)

| Código | Capacidad |
|---|---|
| `VTT.SKILL-AUTH-001` | Obtener `$TOKEN` JWT |
| `VTT.SKILL-DEV-001` | Registrar decisión en devlog |
| `VTT.SKILL-DEV-002` | Registrar observación en devlog |
| `VTT.SKILL-DEV-003` | Editar campos genéricos de un entry (PATCH `/devlog/:entryId`) |
| `VTT.SKILL-DEV-004` | Lifecycle del entry (PATCH `/devlog/:entryId/status`) |
| `VTT.SKILL-DEV-005` | Eliminar entry (DELETE `/devlog/:entryId`) |
| `VTT.SKILL-COMMENT-001` | Postear comment (trazabilidad antes de DELETE) |
| `VTT.SKILL-ISS-001` | Crear issue (cuando es bloqueante real) |

### 6.3 Protocols relacionados

| Código | Relación |
|---|---|
| `VTT.PROTOCOL-ASG-001` | El lifecycle del devlog ocurre **dentro** del ciclo de asignación. El review (FASE 3) coincide con el PASS del code review del PROTOCOL-ASG-001 §5.5. |
| `VTT.PROTOCOL-ASG-001` §5.4 | Sub-ciclo de Issue tipo `bug`/`blocker` — destino al que escala una entry devlog `categoryCode: issue` con síntoma técnico severity `high`/`critical`. La tarea pasa a `task_on_hold`. Ver tabla §5.1.2.bis. |
| `VTT.PROTOCOL-ASG-001` §5.4.bis | Sub-ciclo de Issue tipo `question` — destino al que escala una entry devlog `categoryCode: issue` con síntoma de consulta de diseño/scope (severity `low`/`medium`). La tarea NO pasa a `task_on_hold`. Ver tabla §5.1.2.bis. |
| `VTT.PROTOCOL-MAN-001` | El TL registra `devlog_resolved_count` (y conteos asociados) en el Task Manifest v1.5 (FASE 4 del MAN-001). |
| `VTT.PROTOCOL-GOV-001` | Este Protocol sigue el modelo de 4 niveles de la Guía Normativa VTT. |

### 6.4 Endpoints VTT

| Endpoint | Uso en este Protocol |
|---|---|
| `POST /api/tasks/:taskId/devlog` | Crear 1 entry (FASE 1 — Opción A recomendada) |
| `POST /api/tasks/:taskId/devlog-entries` | Crear varias entries en batch (FASE 1 — Opción B, requiere wrapper `{entries:[...]}`) |
| `GET /api/tasks/:taskId/devlog` | Listar entries de una tarea (FASE 3, FASE 4) |
| `PATCH /api/tasks/:taskId/devlog/:entryId` | Editar campos (FASE 3 — correcciones) |
| `PATCH /api/tasks/:taskId/devlog/:entryId/status` | Transicionar lifecycle (FASE 3, FASE 4) |
| `DELETE /api/tasks/:taskId/devlog/:entryId` | Borrar entry (FASE 3 — entries duplicadas/erróneas, workaround `ENTRY_ALREADY_FINAL`) |

### 6.5 Feature origen

`Docs/01-documentacion/features mod dinamico/FEATURE_DEVLOG_LIFECYCLE.md` v1.0 (2026-05-21)

---

## 7. Reglas críticas

| Regla | Detalle | Consecuencia si se viola |
|---|---|---|
| **R1 — Description obligatorio** | Todo entry creado debe tener `description` con contexto real (no string vacío) | El TL borra el entry en FASE 3 (caso MS-333) |
| **R2 — `severity` no-null** | Para categorías con severidad, el campo es enum obligatorio (low/medium/high/critical) | HTTP 400 al crear |
| **R3 — Estados terminales irreversibles** | Una vez en `resolved`/`wont_fix`/`deferred`, NO se puede cambiar el estado | HTTP 400 `ENTRY_ALREADY_FINAL` — único workaround: borrar y recrear |
| **R4 — Review Gate bloquea con critical/high pending** | El backend retorna 422 al intentar mover tarea con entries críticos no resueltos | La tarea no puede pasar de `task_in_progress` → `task_in_review` ni de `task_in_review` → `task_completed` |
| **R5 — Trazabilidad obligatoria antes de DELETE** | Comment en la tarea explicando por qué se borra el entry, ANTES de invocar DEV-005 | El devlog deja de ser audit trail; el backend no loggea quién/cuándo borró |
| **R6 — Wrapper `entries:[]` en endpoint batch** | `POST /devlog-entries` (plural) requiere `{ "entries": [...] }`; sin wrapper → 400 | Causa común de bug — usar `/devlog` (singular) si es 1 entry |
| **R7 — `resolution` obligatorio en `resolved`/`wont_fix`** | Validación Zod del backend: `resolution` debe tener ≥1 char (no espacios) | HTTP 400 `"resolution es requerido cuando status es resolved o wont_fix"` |
| **R8 — `deferredToPhaseId` obligatorio en `deferred`** | UUID válido de la fase destino | HTTP 400 `"deferredToPhaseId es requerido cuando status es deferred"` |
| **R9 — `resolvedBy` lo setea el backend, no el cliente** | El backend usa el `reportedBy` original del entry, no el agente que ejecuta el PATCH | No intentar enviar `resolvedBy` en el body |
| **R10 — 0 entries no-terminales antes de cerrar sprint** | Política operativa: todas las entries del sprint deben estar en estado terminal antes del reporte M | Cierre de sprint inválido — el TL debe iterar FASE 4 hasta cumplir |
| **R11 — Sin restricción de autoría en DELETE** | Cualquier agente con `tasks.update` puede borrar entries de otros | Coordinar con TL antes de borrar entries ajenas |
| **R12 — Sin endpoint batch DELETE** | Para borrar varios entries: iterar uno por uno | No hay atomicidad — si necesita rollback masivo, coordinar con DevOps |

---

## 8. Resumen de Revisiones

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-22 | PM Martin Rivas | Versión inicial. Documenta el lifecycle de devlog entries en 4 fases (creación / Review Gate / review / cierre de sprint). Cubre los 7 categoryCode (decision, observation, blocker, tech_debt, testing_note, risk, issue), los 6 estados (pending → acknowledged → in_progress → resolved/wont_fix/deferred) y las 12 reglas críticas (R1-R12). Origen: `FEATURE_DEVLOG_LIFECYCLE.md` v1.0 + skills DEV-001..005. Define 3 workflows hijos (.001/.002/.003) a desarrollar en siguientes iteraciones. |
| 1.1.0 | 2026-06-02 | TW-OPS (auditoría VTS-007) | **Frontera DEV-001 ↔ ASG-001 §5.4/§5.4.bis** (escalación de entries `issue` a Issue formal). Cambios: (1) §5.1.2.bis nuevo — tabla de 6 filas con cuándo escalar entry devlog → Issue formal (`bug`/`blocker` → ASG-001 §5.4 / `question` → §5.4.bis) + heurística de distinción tomada de ASG-001 §4. (2) §6.3 Protocols relacionados ampliada con 2 entradas explícitas para ASG-001 §5.4 y §5.4.bis (antes mencionaba solo §5.5 — cross-link unidireccional incompleto detectado en auditoría VTS-007). (3) Frontmatter §1: fecha actualizada + ampliada la descripción de ASG-001 en "Protocols relacionados". Confirmado por Coord en comments `02d88544` + `83c7aba4` (issue `6a8e7df6`). NO se tocó la prosa del cuerpo del Protocol — los workflows hijos `.001/.002/.003` y las skills `DEV-001..005` mantienen sus contratos. Auditoría completa: `knowledge/agent-tasks/audits/AUDIT_VTS-007_DEV-001.md`. |

---

| Editor | Dueño | Última Actualización |
|---|---|---|
| TW-OPS Agent | PM Martin Rivas | 2026-06-02 |

**Versión:** 1.1.0 — Frontera DEV-001 ↔ ASG-001 §5.4/§5.4.bis
**Estado:** Aprobado para uso

*Versión más reciente en el repo `virtual-teams-setup`. No controlada si se imprime.*
