# VTT.PROTOCOL-DEV-001 — Ciclo de vida del Devlog Entry

| Campo | Valor |
|---|---|
| **Código** | `VTT.PROTOCOL-DEV-001` |
| **Título** | Ciclo de vida del Devlog Entry (creación → review → cierre de sprint) |
| **Versión** | 1.1.0 |
| **Fecha** | 2026-06-10 |
| **Autor** | PM Martin Rivas — bump v1.1.0 por TW-OPS (VTS-051) sobre validación VTS-026 |
| **Aplica a** | Agentes ejecutores, TL Reviewer, PM (cierre de sprint), QA (durante review) |
| **Estado** | Aprobado para uso |
| **Tipo** | Genérico VTT — aplica a cualquier proyecto y cualquier fase del SDLC |
| **Reglas aplicables (Nivel 0)** | Ver `00.Rules/rules_catalog.json` — Review Gate bloquea con entries `critical`/`high` no resueltas |
| **Feature origen** | `Docs/01-documentacion/features mod dinamico/FEATURE_DEVLOG_LIFECYCLE.md` v1.0 (2026-05-21) + bump alineado con `FEATURE_DEVLOG_LIFECYCLE_v1.1.md` (2026-06-04) y `GUIA_DEVLOG_FINDINGS.md` (2026-06-04) |
| **Endpoints VTT cubiertos** | `POST/PATCH/DELETE /api/tasks/:taskId/devlog[/:entryId][/status]` |
| **Protocols relacionados** | `VTT.PROTOCOL-ASG-001` (el devlog se mueve dentro del ciclo de asignación; §5.4 sub-ciclo Issue bloqueante referenciado desde §5.5), `VTT.PROTOCOL-MAN-001` (el TL registra `devlog_resolved_count` en el manifest v1.5) |
| **Origen del bump v1.1.0** | Reporte `knowledge/agent-tasks/audits/VALIDATE_VTS-026_DEV-001_vs_MOD-DIN-V4.md` §5.1 (10 cambios C1-C10) + dictamen PM (comment `9054851e` en VTS-026) |

---

## Tabla de Contenido

0. [Matriz de entidades de trazabilidad (D-61, D-62)](#0-matriz-de-entidades-de-trazabilidad-d-61-d-62)
1. [Propósito](#1-propósito)
2. [Campo de Aplicación](#2-campo-de-aplicación)
3. [Responsabilidades](#3-responsabilidades)
4. [Definiciones](#4-definiciones)
5. [Procedimiento](#5-procedimiento)
   - 5.1 [FASE 1 — Creación durante ejecución (agente)](#51-fase-1--creación-durante-ejecución)
   - 5.2 [FASE 2 — Review Gate (verificación automática)](#52-fase-2--review-gate)
   - 5.3 [FASE 3 — Procesamiento en code review (TL)](#53-fase-3--procesamiento-en-code-review)
   - 5.4 [FASE 4 — Cierre de devlog al cierre de sprint (TL + PM)](#54-fase-4--cierre-de-devlog-al-cierre-de-sprint)
   - 5.5 [Crear Fix Task desde Entry — distinción trazabilidad vs bloqueo](#55-crear-fix-task-desde-entry--distinción-trazabilidad-vs-bloqueo)
   - 5.6 [Mapa de gates por familia (D-65)](#56-mapa-de-gates-por-familia-d-65)
6. [Referencias Cruzadas](#6-referencias-cruzadas)
7. [Reglas críticas](#7-reglas-críticas)
8. [Resumen de Revisiones](#8-resumen-de-revisiones)

---

## 0. Matriz de entidades de trazabilidad (D-61, D-62)

Los devlog entries son **una de cuatro entidades** del Modelo Dinámico V4. Antes de crear cualquier entry, identificar la entidad correcta:

| Entidad | Pregunta que responde | Cuándo crear |
|---|---|---|
| **Devlog entry** | "¿Qué pasó durante la ejecución?" | Trazabilidad del proceso — decisión técnica, observación, bloqueo local, finding narrativo |
| **Finding** (`task_findings`) | "¿Qué se detectó y debe atenderse?" | Hallazgo accionable que requiere decisión explícita (TL dictamina) |
| **Issue** | "¿Qué impide cumplir los CAs?" | Bloqueo de scope o consulta no resoluble localmente (mueve la tarea a `task_on_hold` si es bloqueante real) |
| **TrackableItem** (`trackable_items`) | "¿Qué debe seguirse a largo plazo?" | Compromiso del proyecto cross-tarea (tech_debt, RF, ADR, risk del proyecto) |

### D-61 — Registro único

**Cada cosa se registra UNA SOLA VEZ, en su entidad.** No duplicar.

- Una decisión técnica vive en **devlog `decision`**, no como finding ni como TI hasta que pase el filtro de "compromiso cross-tarea".
- Un hallazgo accionable vive en **finding**, no como devlog `tech_debt`/`issue` paralelo.
- Un bug que impide los CAs vive en **issue**, no como devlog `blocker`.
- Un compromiso del proyecto vive en **TI**, con rastro de origen en devlog/finding pero sin duplicación operativa.

### D-62 — Prohibidos los pares espejo

**No crear pares `devlog ↔ issue` ni `finding ↔ TI`** que repitan el mismo contenido.

- El doc narrativo del devlog puede *mencionar* un finding/issue/TI, pero el registro estructurado vive una sola vez.
- Las categorías `tech_debt`, `issue` y `risk` del devlog se preservan por compatibilidad operativa, pero **lo accionable va a findings** — el devlog en esas categorías queda como contexto narrativo.

> **Referencia conceptual completa:** `FEATURE_DEVLOG_LIFECYCLE_v1.1.md` §0 (Modelo Dinámico V4) y `GUIA_DEVLOG_FINDINGS.md` §0 (árbol de decisión P1-P5).

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

- Crear devlog entries **durante** la ejecución de su tarea, eligiendo el `categoryCode` correcto del catálogo vivo (12 categorías activas en `GET /api/catalogs/devlog-categories`):

| `categoryCode` | `severityLevels` permitidos | Cuándo usar |
|---|---|---|
| `decision` | (sin severity — `severityLevels: []`) | Decisión técnica activa con trade-off explícito durante la ejecución |
| `observation` | (sin severity — `severityLevels: []`) | Observación de comportamiento o contexto a documentar, sin acción requerida |
| `blocker` | critical/high/medium/low | Bloqueante real que detiene la tarea (si es bug de scope → preferir Issue, ver §5.5) |
| `tech_debt` | critical/high/medium/low | Deuda técnica detectada — nota narrativa; lo accionable va a finding (D-62) |
| `testing_note` | critical/high/medium/low | Resultado de prueba o verificación (QA típicamente) |
| `risk` | critical/high/medium/low | Riesgo local identificado — si es del proyecto, evaluar elevación a TI tipo `risk` (D-64) |
| `issue` | critical/high/medium/low | Inconsistencia narrativa — el bug accionable va a finding/issue, no acá (D-62) |
| `question` | high/medium/low | Consulta del agente al TL no resoluble localmente — ver `PROTOCOL-ASG-001 §5.4.bis` (sub-ciclo question) |
| `dependency` | high/medium | Dependencia externa detectada entre tareas o sistemas |
| `improvement` | medium/low | Mejora propuesta para iteración futura |
| `feedback` | high/medium/low | Feedback recibido de stakeholder o usuario |
| `brand_issue` | critical/high/medium | Tema de adherencia a guías de marca |

> **⚠️ Nota crítica sobre severity (H-2 confirmado VTS-026):** las categorías `decision` y `observation` declaran `severityLevels: []` en el catálogo vivo. El backend **descarta silenciosamente** cualquier `severity` enviado en esas categorías (lo normaliza a `null` sin retornar warning ni 400). **NO incluir el campo `severity` en payloads de `decision` u `observation`** — confiar en severity ahí no bloquea el Review Gate aunque el agente envíe `high`/`critical`.

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

**`fixTaskId`:** ID de tarea que resuelve el entry (recomendado en `resolved` formal, opcional en otros casos). Permite trazar el devlog al PR que lo cerró. **No es un mecanismo de bloqueo** — ver §5.5 (distinción trazabilidad vs bloqueo).

**`deferred` como TRANSFERIDO (resignificación v1.1):** un entry en `deferred` no significa "pospuesto ambiguo" — significa que el **seguimiento del tema se transfirió** a otro lugar (TI, tarea futura, sprint DEUDA). El devlog conserva el rastro de origen; el tracking activo vive en el destino.

**Elevación a TrackableItem (D-64):** cuando un entry resulta ser un compromiso del proyecto (cross-tarea, largo plazo), se **eleva** a un TI con referencia al código del TI. El entry queda `deferred` (transferido al TI) y el TI hereda `originTaskId`/`originRef`. Patrón típico: `tech_debt` detectado en una tarea → elevado a `TD-CORE-XXX` o trasladado a una tarea del **Sprint DEUDA** del release. Sin la elevación, el compromiso se pierde al cerrar la tarea.

**Auto side-effects del backend en transiciones terminales:**

| Transición | `resolvedAt` | `resolvedBy` | `resolution` | Notas |
|---|:---:|:---:|:---:|---|
| → `resolved` | NOW() | `reportedBy` original | preservado | Caso normal. Recomendado incluir `fixTaskId` |
| → `wont_fix` | NOW() | (null, no fue resuelto) | preservado | `resolution` obligatorio con justificación |
| → `deferred` | (limpia a null) | (limpia a null) | **(limpia a null) — BY-DESIGN** | Backend ejecuta `updateData.resolution = null` intencionalmente. NO es bug. Para preservar la referencia al destino, ver §5.3.5 (workaround) y R14 (regla crítica). |

> **⚠️ T2 confirmado empíricamente VTS-026:** la línea 227 del service code del backend limpia `resolution` al transicionar a `deferred` por diseño. Validado con `curl` directo a `api.vttagent.com`. La FEATURE v1.1 §4.1 exige "referencia obligatoria al destino" en deferred — operativamente esa referencia **no** puede vivir en `resolution` (el backend la borra). Usar `description` original o comment en la tarea (ver §5.3.5 y R14).

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

| Si... | Usar |
|---|---|
| Trazabilidad de decisión/observación/finding | **Devlog entry** (esta fase) |
| Comunicación con el equipo, no requiere trazabilidad | Comment (`VTT.SKILL-COMMENT-001`) |
| Bloqueante real que detiene la tarea ahora | Issue (`VTT.SKILL-ISS-001`) + on_hold |

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

#### 5.2.1 Findings también bloquean (D-63)

El Review Gate de **`in_review → completed`** también considera los **findings** de la tarea (`task_findings`), no solo el devlog. Esto es parte del mapa de gates por familia (ver §5.6):

| Condición | Resultado |
|---|---|
| Findings `open` con severity `high`/`critical` (sin dictamen del TL) | 🔴 **BLOQUEADO** — HTTP 422 en `in_review → completed` |
| Findings dictaminados (`resolved`/`wont_fix`/`false_positive`) | ✅ OK |
| Findings `open` `medium`/`low` | ✅ OK (no bloquean) |

> D-63: el TL debe dictaminar todos los findings `open` `high`/`critical` antes de mover la tarea a `task_completed`. Esto evita que findings accionables queden colgando al cierre de la tarea. El dictamen sigue la tabla de `GUIA_DEVLOG_FINDINGS.md` §2.2 (5 caminos: reclasificar como issue, formalizar Sprint DEUDA, elevar a TI, `wont_fix`, `false_positive`).

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

#### 5.3.5 Workaround para preservar referencia en `deferred` (T2 / H-4)

El backend limpia `resolution`/`resolvedAt`/`resolvedBy` al transicionar a `deferred` (BY-DESIGN — ver §4 tabla auto side-effects). Para que el destino del traspaso quede registrado en el devlog, usar una de estas 3 opciones **antes** o **al momento** de diferir:

| # | Opción | Cómo se aplica | Cuándo conviene |
|---|---|---|---|
| 1 | `description` original | Al **crear** el entry, escribir el destino dentro del `description` (ej. "Si se difiere, va a TD-CORE-003"). El backend preserva `description` en cualquier transición. | El destino se conoce al crear el entry |
| 2 | Comment en la tarea | Antes del PATCH a `deferred`, postear `POST /api/tasks/:taskId/comments` con `message: "Entry <entryId> diferido → TD-CORE-003 / VTS-XXX / Sprint DEUDA-B1A"` | El destino se decide al momento de diferir (caso típico) |
| 3 | `fixTaskId` | Si el destino es una **tarea concreta** del backlog, setear `fixTaskId` en el PATCH `/status` (el backend preserva ese campo en `deferred`) | El destino es una tarea correctiva ya creada |

> **Anti-patrón:** confiar en `resolution` al diferir. El backend la limpia y la información se pierde sin trazabilidad. Ver R14.

#### 5.3.6 PASS del code review

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

### 5.5 Crear Fix Task desde Entry — distinción trazabilidad vs bloqueo

> **Origen:** dictamen PM Martin Rivas (2026-06-09, comment `9054851e` en VTS-026) + validación empírica VTS-026 (T3 confirmado). Aplica recomendación **Opción B** del reporte VTS-026 §3.4: el flujo legacy "Crear Fix Task desde Entry" queda **absorbido** al flujo Issue de `PROTOCOL-ASG-001 §5.4` para los casos de bloqueo, y se documenta como **patrón de uso del campo `fixTaskId`** para los casos de trazabilidad post-hoc.

#### 5.5.1 Distinción

Cuando una entry detecta un problema cuya corrección requiere una tarea separada, existen **dos mecanismos distintos** según la necesidad. Elegir mal lleva a violar D-61 (matriz de roles) y D-62 (registro único).

| Necesidad | Mecanismo correcto | Resultado |
|---|---|---|
| **Solo trazabilidad post-hoc** (la tarea hija existe o se va a crear, queremos linkearla a este entry, **sin pausar la tarea padre**) | Flujo manual T3 (3 pasos) con `fixTaskId` en devlog | Entry pasa a `resolved`. Tarea padre sigue su curso sin cambios de status. El link es solo documental. |
| **Bloqueo del padre con auto-resume** (la tarea padre **no puede avanzar** hasta que la correctiva cierre) | Issue `type=bug` por `PROTOCOL-ASG-001 §5.4` (sub-ciclo Issue bloqueante) | Padre → `task_on_hold`. Hija creada con `sourceIssueId`. Al cerrar la hija, el padre vuelve automáticamente a su `previousStatus` (auto-resume del backend). |

> **Nunca mezclar:** `fixTaskId` en devlog **no es** un mecanismo de bloqueo. Es solo un link documental. Si la situación requiere que el padre se pause hasta el fix, **debe ser Issue**, no devlog `fixTaskId`.

#### 5.5.2 Flujo manual T3 — solo trazabilidad post-hoc

> **T3 confirmado VTS-026:** no existe endpoint dedicado `POST /api/tasks/:id/devlog/:entryId/create-fix-task`. El flujo correcto es **manual** en 3 pasos.

```
Paso 1: POST /api/phases/:phaseId/tasks
        body: { title, description, ... }
        → response: { data: { id: "VTS-XXX-nueva" } }

Paso 2: Capturar el taskId resultante (formato VTS-XXX / MS-XXX según proyecto)

Paso 3: PATCH /api/tasks/:taskIdPadre/devlog/:entryId/status
        body: {
          "status": "resolved",
          "fixTaskId": "VTS-XXX-nueva",
          "resolution": "Reclasificado como tarea correctiva <ID> — ver feed VTS-XXX-nueva"
        }
        → entry pasa a `resolved` con `fixTaskId` apuntando a la correctiva
```

Este flujo **NO tiene Workflow ni Skill propios** — es un patrón de uso de DEV-004 (PATCH `/status`) con el campo opcional `fixTaskId`. Su único propósito es dejar trazabilidad documental.

#### 5.5.3 Para bloqueo del padre — invocar PROTOCOL-ASG-001 §5.4

Si la situación requiere que la tarea padre se **pause** hasta que la correctiva cierre, **NO usar el flujo T3 arriba**. Invocar el sub-ciclo Issue bloqueante de `PROTOCOL-ASG-001 §5.4`:

1. Agente crea Issue `type=bug` o `type=blocker` con `severity` `high`/`critical` invocando `VTT.SKILL-ISS-001`.
2. Backend (o PM/TL) mueve la tarea padre a `task_on_hold` (`PUT /api/tasks/:id/on-hold`).
3. TL evalúa y crea (si aplica) tarea correctiva con `sourceIssueId` apuntando al Issue.
4. La tarea correctiva sigue el ciclo completo del PROTOCOL-ASG-001 (recursión).
5. Al cerrarse todos los Issues bloqueantes del padre, el backend ejecuta **auto-resume**: la tarea padre vuelve a su `previousStatus` (típicamente `task_in_review` o `task_in_progress`).

Ver `PROTOCOL-ASG-001 §5.4` para el detalle completo del sub-ciclo bloqueante y `§5.4.bis` para consultas no bloqueantes (`type=question`).

#### 5.5.4 Justificación de absorción (Opción B)

La absorción del flujo legacy al flujo Issue (en vez de mantenerlo como capacidad de primera clase del devlog) responde a 4 razones:

- **D-61:** devlog = bitácora (hechos); issue = bloqueo de scope. Una tarea correctiva nace de un bug-de-scope, jurisdicción de Issue.
- **D-62:** crear capacidad propia del devlog para fix tasks duplicaría con Issue→correctiva (ASG-001 §5.4), violando el registro único.
- **T3 (validación empírica):** el endpoint dedicado no existe en el backend; mantener doble flujo aumenta confusión sin valor agregado.
- **`GUIA_DEVLOG_FINDINGS.md` §2.2 dictamen 1** ya documenta la redirección oficial: "AHORA — bug-de-scope mal clasificado: `resolved` 'Reclasificado como issue X' → POST /issues + correctiva en el sprint actual, tarea on-hold."

### 5.6 Mapa de gates por familia (D-65)

> **Origen:** D-65 (FEATURE_DEVLOG_LIFECYCLE v1.1 §7). Tabla canónica del Modelo Dinámico V4 — cada familia vigila una pieza distinta. Esta sección es **referencia única** dentro del paquete DEV-001 para entender qué bloquea qué.

Las 4 familias del Modelo Dinámico vigilan transiciones diferentes:

| Familia | Estado que bloquea | Transición bloqueada | Cómo se desbloquea |
|---|---|---|---|
| **Devlog** | Entries `critical`/`high` en `pending`/`acknowledged`/`in_progress` | `task_in_progress → task_in_review` y `task_in_review → task_completed` | Llevar a estado terminal (`resolved`/`wont_fix`/`deferred`) — ver §5.3 |
| **Findings** (D-63) | Findings `open` `critical`/`high` sin dictamen | `task_in_review → task_completed` | TL dictamina cada finding por uno de los 5 caminos de `GUIA_DEVLOG_FINDINGS.md` §2.2 |
| **Criterios de Aceptación** | Algún CA en `not_met` (DoD) | `task_in_review → task_completed` | Agente completa o TL valida cada CA con `met` + fulfillment |
| **TrackableItems** | TI vinculado a la tarea sin evidencia válida (`ti_*` no en estado consistente) | `task_completed → task_approved` (PM) y cierre de fase/release | Agregar evidencia al TI (link a PR / archivo / decisión) o cambiar status del TI según corresponda |

**Lectura en una frase:** el devlog vigila que **nada quede sin procesar**, los findings que **nada quede sin dictaminar**, los CAs que **la entrega cumpla**, y los TIs que **los compromisos no se pierdan**.

> **Referencia conceptual:** `FEATURE_DEVLOG_LIFECYCLE_v1.1.md` §7 es la fuente canónica. Esta tabla la replica para que el agente o TL que opera el devlog la tenga visible sin saltar de doc.

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
| **R13 — DEV-003 NUNCA para cambiar `status`** | Para cualquier transición de lifecycle usar **exclusivamente** `VTT.SKILL-DEV-004` (PATCH `/status`). El endpoint genérico de DEV-003 (PATCH `/devlog/:entryId` body) acepta `status:resolved` pero **no mueve el `status`** — sí setea `resolvedAt`/`resolvedBy`/`resolution` (BUG-CONSISTENCIA H-3 confirmado VTS-026). El entry queda inconsistente. | Entry con `status:pending` pero `resolvedAt`/`resolvedBy`/`resolution` poblados — engaña al TL en code review y puede colar entries no terminales al gate |
| **R14 — Preservar referencia en `deferred`** | Cuando se transiciona a `deferred`, **NUNCA** confiar en `resolution` para guardar la referencia al destino: el backend la limpia a `null` (BY-DESIGN — T2 confirmado VTS-026). Usar `description` original (escrito al crear el entry), comment en la tarea, o `fixTaskId` (si el destino es una tarea). Ver §5.3.5 para las 3 opciones de workaround. | Pérdida silenciosa del contexto de "a dónde se transfirió" — el devlog queda como referencia muerta, viola D-66 (referencia obligatoria al destino en deferred) |

---

## 8. Resumen de Revisiones

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-22 | PM Martin Rivas | Versión inicial. Documenta el lifecycle de devlog entries en 4 fases (creación / Review Gate / review / cierre de sprint). Cubre los 7 categoryCode (decision, observation, blocker, tech_debt, testing_note, risk, issue), los 6 estados (pending → acknowledged → in_progress → resolved/wont_fix/deferred) y las 12 reglas críticas (R1-R12). Origen: `FEATURE_DEVLOG_LIFECYCLE.md` v1.0 + skills DEV-001..005. Define 3 workflows hijos (.001/.002/.003) a desarrollar en siguientes iteraciones. |
| 1.1.0 | 2026-06-10 | TW-OPS (VTS-051) — revisión LEAD_NPL | **Bump de validación VTS-026 — 10 cambios C1-C10 del reporte madre `knowledge/agent-tasks/audits/VALIDATE_VTS-026_DEV-001_vs_MOD-DIN-V4.md` §5.1 + dictamen PM (comment `9054851e`).** (C1) §0 nueva al inicio "Matriz de entidades de trazabilidad" con D-61 (registro único) + D-62 (prohibidos pares espejo) — alinea con `FEATURE_DEVLOG_LIFECYCLE_v1.1.md` §0. (C2) §3.1 ampliada de 7 a **12 categorías** del catálogo vivo (`GET /api/catalogs/devlog-categories`) — agrega `question`, `dependency`, `improvement`, `feedback`, `brand_issue` con `severityLevels` permitidos + nota crítica sobre H-2 (severity en `decision`/`observation` se normaliza a `null` BY-DESIGN). (C3) §4 tabla auto-side-effects ampliada con fila `deferred → resolution: null BY-DESIGN` (T2 confirmado empíricamente VTS-026) + §5.3.5 nueva "Workaround para preservar referencia en `deferred`" con 3 opciones (description original, comment, fixTaskId). (C4) §5.5 nueva "Crear Fix Task desde Entry — distinción trazabilidad vs bloqueo" con tabla mecanismo correcto + flujo manual T3 de 3 pasos (T3 confirmado: endpoint dedicado no existe) + cross-ref a `PROTOCOL-ASG-001 §5.4` para el caso de bloqueo + justificación de absorción (Opción B del reporte VTS-026 §3.4). (C5) §7 R13 nueva "DEV-003 NUNCA para cambiar `status`" — documenta BUG-CONSISTENCIA H-3 (PATCH body acepta `status:resolved` pero deja entry inconsistente). (C6) §7 R14 nueva "Preservar referencia en `deferred`" — usar description/comment/fixTaskId, NUNCA `resolution`. (C7) §5.2.1 D-63 "Findings también bloquean" — findings `open` `high`/`critical` bloquean `in_review → completed` (no solo el devlog). (C8) §4 definición ampliada de "elevación a TrackableItem" + concepto Sprint DEUDA (D-64). (C9) §5.6 nueva "Mapa de gates por familia" (D-65) con tabla canónica de 4 familias (devlog/findings/CAs/TIs) — referencia única dentro del paquete DEV-001. (C10) Header bump v1.0.0 → v1.1.0 + fecha 2026-06-10 + nueva fila "Origen del bump v1.1.0" referenciando reporte VTS-026 y dictamen PM. **NO modifica reglas R1-R12 ni numeración existente, NO crea Workflows/Skills/CARDs (esas son tareas hijas VTS-027/028/049), NO bumpea Skills DEV-001..005 (eso es VTS-028).** Estructura del Protocol v1.0.0 preservada en su totalidad — solo se agregan secciones y filas nuevas. |

---

| Editor | Dueño | Última Actualización |
|---|---|---|
| TW-OPS (Technical Writer of Operational Processes) — revisión LEAD_NPL | PM Martin Rivas | 2026-06-10 |

**Versión:** 1.1.0 — Bump de validación VTS-026 — Ciclo de vida del Devlog Entry
**Estado:** Aprobado para uso

*Versión más reciente en el repo `virtual-teams-setup`. No controlada si se imprime.*
