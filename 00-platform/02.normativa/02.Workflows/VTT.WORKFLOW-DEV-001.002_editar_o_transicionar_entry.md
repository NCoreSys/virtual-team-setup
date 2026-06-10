# VTT.WORKFLOW-DEV-001.002 — Editar o transicionar devlog entry en code review

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-DEV-001.002` |
| **Pertenece a** | `VTT.PROTOCOL-DEV-001` v1.1.0 §5.3 (FASE 3 — Procesamiento en code review) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-10 |
| **Autor** | TW-OPS (Technical Writer of Operational Processes) |
| **Aplica a** | TL Reviewer (uso principal), Agente ejecutor (correcciones propias antes de `task_in_review`) |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por `PROTOCOL-DEV-001 §5.3.3` |

---

## 1. Propósito

Editar el contenido de una devlog entry existente (`title`/`description`/`severity`) o transicionarla a un estado del lifecycle (`acknowledged` / `in_progress` / `resolved` / `wont_fix` / `deferred`), aplicando las reglas críticas **R13** (DEV-003 NUNCA para cambiar status) y **R14** (preservar referencia en `deferred`) del `PROTOCOL-DEV-001 v1.1.0 §7`.

> **Cuándo se invoca:** durante FASE 3 del Protocol — cuando la tarea está en `task_in_review` y el TL Reviewer procesa todas las entries del devlog. También el agente puede invocarlo en FASE 1 para corregir typos o agregar `description` que faltaba ANTES de mover la tarea a `task_in_review`.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `taskId` | string (`VTS-XXX` / `MS-XXX`) | Tarea VTT activa | sí | ID de la tarea dueña de la entry |
| `entryId` | UUID | Salida de `VTT.WORKFLOW-DEV-001.001` o `GET /devlog` | sí | UUID de la entry a editar/transicionar |
| `accion` | enum `edit` / `lifecycle` | Decisión del actor | sí | Determina qué Skill se invoca (DEV-003 para edit, DEV-004 para lifecycle) |
| `field_updates` | object | Decisión del actor | sí si `accion=edit` | ≥1 campo del set permitido (ver §5 Paso 3a). Excluye `status` (R13). |
| `status` | enum (5 valores) | Decisión del actor | sí si `accion=lifecycle` | `acknowledged` / `in_progress` / `resolved` / `wont_fix` / `deferred` |
| `resolution` | string ≥1 char | Decisión del actor | condicional | OBLIGATORIO si `status ∈ {resolved, wont_fix}` (NO se usa en `deferred` — R14) |
| `deferredToPhaseId` | UUID | `phaseId` destino del traspaso | condicional | OBLIGATORIO si `status = deferred` |
| `fixTaskId` | string (`VTS-XXX` / `MS-XXX`) o UUID | Decisión del actor | opcional | Recomendado con `status=resolved` formal; usar para flujo manual T3 (ver §5 Paso 6) |

---

## 3. Precondiciones

- Token JWT válido (`VTT.SKILL-AUTH-001` ya ejecutado).
- Entry `entryId` existe y pertenece a `taskId` (validar con GET previo si hay duda).
- Si `accion=lifecycle` con `status ∈ {resolved, wont_fix, deferred}`: la entry **NO** está en estado terminal (`status ∈ {pending, acknowledged, in_progress}`). Si está terminal → HTTP 400 `ENTRY_ALREADY_FINAL`; workaround = borrar con `VTT.SKILL-DEV-005` y recrear.
- Actor con capability `tasks.update`.
- Si transición a `resolved`/`wont_fix`: `resolution` ya tiene contenido válido.
- Si transición a `deferred`: el destino del traspaso ya está decidido (TI / tarea futura / sprint DEUDA) y registrado **fuera de `resolution`** (ver R14 + §5 Paso 5).

> **Si una precondición falla:** ver §8 Errores comunes.

---

## 4. Reglas del Workflow

### 4.1 R13 — DEV-003 NUNCA para cambiar `status` (regla bloqueante)

> Origen: `PROTOCOL-DEV-001 v1.1.0 §7 R13` + BUG-CONSISTENCIA H-3 confirmado VTS-026.

El endpoint genérico `PATCH /api/tasks/:taskId/devlog/:entryId` (que ejecuta `VTT.SKILL-DEV-003`) **acepta** `status:resolved` en el body pero **NO mueve el `status`** — sí setea `resolvedAt`/`resolvedBy`/`resolution` y deja la entry **inconsistente** (`status:pending` con marca de resuelta).

**Regla operativa:**

- Si `accion = edit` (corregir `title`/`description`/`severity`) → invocar `VTT.SKILL-DEV-003`. **NUNCA** incluir `status` en el body de DEV-003.
- Si `accion = lifecycle` (transicionar `status`) → invocar **exclusivamente** `VTT.SKILL-DEV-004` (PATCH `/devlog/:entryId/status`).

### 4.2 R14 — Preservar referencia en `deferred` (regla bloqueante)

> Origen: `PROTOCOL-DEV-001 v1.1.0 §7 R14` + T2 BY-DESIGN confirmado VTS-026.

Cuando se transiciona una entry a `deferred`, el backend limpia automáticamente `resolution`, `resolvedAt` y `resolvedBy` a `null` (ver `PROTOCOL-DEV-001 §4` tabla auto side-effects). Es comportamiento intencional, no bug.

**Regla operativa: NUNCA usar `resolution` para registrar el destino del traspaso.** Aplicar una de las 3 opciones de workaround (`PROTOCOL-DEV-001 §5.3.5`):

| # | Opción | Aplicar cuándo |
|---|---|---|
| 1 | Escribir destino en `description` original | Si el destino se conocía al crear la entry |
| 2 | Postear comment en la tarea referenciando entry + destino | Si el destino se decide al diferir (caso típico) |
| 3 | Setear `fixTaskId` si destino es una tarea concreta | El campo se preserva al diferir |

### 4.3 Distinción trazabilidad vs bloqueo (cross-ref ASG-001 §5.4)

> Origen: `PROTOCOL-DEV-001 v1.1.0 §5.5`.

Este Workflow **NO** crea tareas correctivas con bloqueo del padre. Si la entry detecta un bug-de-scope que debe bloquear la tarea padre (con auto-resume al cerrar la correctiva):

- **NO usar este Workflow.** Invocar `PROTOCOL-ASG-001 §5.4` (sub-ciclo Issue bloqueante con `VTT.SKILL-ISS-001`).
- Padre → `task_on_hold`. Hija con `sourceIssueId`. Auto-resume cuando todas las Issues bloqueantes cierran.

Si la entry solo necesita **trazabilidad post-hoc** con una tarea correctiva (sin bloqueo del padre), aplicar el **flujo manual T3** (ver §5 Paso 6). El campo `fixTaskId` es solo un link documental — NO bloquea nada.

---

## 5. Pasos

### Paso 1 — Leer entry actual

→ invoca **`VTT.SKILL-QUERY-003`** (o `GET /api/tasks/$TASK_ID/devlog` filtrado por `entryId`) para obtener el estado actual de la entry.

Verificar:
- `status` actual (debe ser **no terminal** si vamos a transicionar)
- `categoryCode`, `severity`, `description` actuales (para decidir si requieren edit)
- `resolvedAt`, `resolvedBy`, `resolution` actuales (para detectar inconsistencias H-3 históricas — entry con `resolvedAt!=null` pero `status=pending` → indicio de R13 violada previamente; reportar)

### Paso 2 — [DECISIÓN] ¿editar contenido o transicionar status?

¿Solo corregir `title`/`description`/`severity`? →
- **SÍ** → Paso 3a (edit con DEV-003)
- **NO** → ¿Cambiar `status` (lifecycle)? →
  - **SÍ** → Paso 3b (lifecycle con DEV-004)
  - **NO** → ¿Borrar entry duplicada/errónea? → Paso 7

### Paso 3a — Edit con DEV-003 (NO tocar `status`)

→ invoca **`VTT.SKILL-DEV-003`** con campos del set permitido **EXCLUYENDO `status`** (R13):

| Campo editable | Tipo | Notas |
|---|---|---|
| `title` | string 1-500 | Editar título |
| `description` | string | Agregar/corregir descripción |
| `severity` | enum del catálogo de la categoría | Cambiar severidad (respetando `severityLevels`) |

> **⚠️ R13 BLOQUEANTE:** NO pasar `status` en el body de DEV-003. Aunque el backend lo acepte, no mueve el status — solo crea inconsistencia. Para `status` → siempre DEV-004.

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "...",
    "description": "...",
    "severity": "medium"
  }'
```

Backend retorna 200 con la entry actualizada. Saltar al Paso 8 (validación).

### Paso 3b — Lifecycle con DEV-004 (transición de `status`)

→ invoca **`VTT.SKILL-DEV-004`** (PATCH `/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status`).

[DECISIÓN] elegir `status` destino:

| Status destino | Cuándo aplicar | Campos obligatorios adicionales |
|---|---|---|
| `acknowledged` | TL vio la entry pero todavía no decide | (ninguno) |
| `in_progress` | Hay alguien trabajando en resolverla | (ninguno) |
| `resolved` | La entry queda resuelta (con fix o documentada) | `resolution` (≥1 char). Recomendado: `fixTaskId` si hay PR/tarea asociada |
| `wont_fix` | TL/PM deciden NO arreglar (con justificación) | `resolution` (≥1 char). NO `resolvedBy` (backend lo deja null) |
| `deferred` | Se transfiere a TI / tarea futura / sprint DEUDA | `deferredToPhaseId` (UUID de fase destino). **NO `resolution`** (R14: backend la limpia) |

Saltar al Paso 4 si destino es `deferred`; al Paso 8 (validación) en otros casos.

### Paso 4 — [DECISIÓN] ¿status destino es `deferred`? — aplicar R14 + workaround T2

Si `status = deferred`, **antes** de invocar DEV-004:

1. Verificar que el destino del traspaso (TI / tarea / sprint) ya esté **registrado fuera de `resolution`** según una de las 3 opciones del §4.2.
2. Setear `deferredToPhaseId` correctamente (UUID de la fase destino).
3. Opcional pero recomendado: setear `fixTaskId` si el destino es una tarea concreta.

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "deferred",
    "deferredToPhaseId": "<UUID_FASE_DESTINO>",
    "fixTaskId": "VTS-XXX-destino"
  }'
```

> Backend retorna 200 pero con `resolution: null`, `resolvedAt: null`, `resolvedBy: null` (T2 BY-DESIGN). El `description` original y el `fixTaskId` SÍ se preservan. Si el destino no quedó registrado fuera de `resolution`, postear comment de trazabilidad en la tarea **inmediatamente** referenciando `entryId` + destino.

### Paso 5 — [DECISIÓN] ¿status destino es `resolved` con `fixTaskId` apuntando a tarea correctiva nueva? — aplicar §5.bis

Si el caso es: "la entry detectó un problema, se va a crear una tarea correctiva nueva para arreglarlo, y queremos linkear las dos para trazabilidad" → **NO mezclar con bloqueo**. Aplicar §5.bis (flujo manual T3).

Si en cambio la entry solo se resuelve con un fix en el mismo PR (sin crear tarea correctiva nueva) → setear `fixTaskId` con la tarea actual o dejar `fixTaskId: null` y agregar el commit/PR en `resolution`. Saltar al Paso 8.

### Paso 5.bis — Flujo manual T3 (Crear Fix Task — solo trazabilidad post-hoc)

> Origen: `PROTOCOL-DEV-001 v1.1.0 §5.5.2` + T3 confirmado VTS-026. **Aplicar SOLO si la situación NO requiere bloqueo del padre.** Si requiere bloqueo → invocar `PROTOCOL-ASG-001 §5.4` (NO este Workflow).

3 pasos manuales:

#### Paso 5.bis.1 — Crear tarea fix

```bash
curl -s -X POST "$VTT_BASE_URL/api/phases/$PHASE_ID/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "[FIX] <descripcion del problema detectado en la entry>",
    "description": "<contexto + referencia a entryId origen + criterios de resolucion>",
    "assignedToId": "<UUID_agente>",
    "priorityId": "<UUID_priority>"
  }'
```

Capturar el `data.id` de la respuesta (formato `VTS-XXX` / `MS-XXX`).

#### Paso 5.bis.2 — Capturar `taskIdFix`

`taskIdFix = data.id` retornado en el paso anterior.

#### Paso 5.bis.3 — PATCH /devlog/:entryId/status con `fixTaskId` para linkeo trazable

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"status\": \"resolved\",
    \"fixTaskId\": \"$TASK_ID_FIX\",
    \"resolution\": \"Reclasificado como tarea correctiva $TASK_ID_FIX — ver feed de esa tarea para tracking del fix.\"
  }"
```

> **Resultado:** la entry pasa a `resolved` con `fixTaskId` apuntando a la correctiva. La tarea padre **no se mueve** de status (no es bloqueo). El link es solo documental — al ver la entry en code review, el TL puede saltar a la tarea correctiva con el `fixTaskId`.
>
> **Cross-ref bloqueo:** si la situación requiere que el padre se pause hasta que la correctiva cierre, **NO usar este flujo**. Invocar `PROTOCOL-ASG-001 §5.4` (`VTT.SKILL-ISS-001` con `type=bug` `severity=high/critical` → padre auto-on-hold → al cerrar todos los Issues, padre auto-resume).

### Paso 6 — Validar respuesta del backend

DEV-003 (edit): retorna 200 con la entry completa actualizada (campos editados).

DEV-004 (lifecycle): retorna 200 con la entry y los auto-side-effects aplicados:
- `resolved` → `resolvedAt: now`, `resolvedBy: reportedBy original`, `resolution: preservado`
- `wont_fix` → `resolvedAt: now`, `resolvedBy: null`, `resolution: preservado`
- `deferred` → `resolvedAt: null`, `resolvedBy: null`, `resolution: null` (BY-DESIGN — R14)

### Paso 7 — Borrar entry duplicada/errónea (caso especial)

> Solo si la entry es duplicada o creada por error con contenido inválido. **NO** borrar entries con contenido válido aunque estén en estado terminal.

→ invoca **`VTT.SKILL-COMMENT-001`** para postear comment de trazabilidad en la tarea ANTES del DELETE (R1 SKL-DEV-005: el backend no loggea quién/cuándo borró):

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\":\"Eliminando devlog entry $ENTRY_ID — razon: <justificacion>\",\"userId\":\"$AGENT_UUID\"}"
```

→ invoca **`VTT.SKILL-DEV-005`** (DELETE):

```bash
curl -s -X DELETE "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
  -H "Authorization: Bearer $TOKEN" -w "HTTP %{http_code}\n"
```

Esperado: HTTP 204 sin body.

### Paso 8 — Registrar resultado en SKL-REPORT-01

Si este Workflow se invoca dentro de FASE 3 del Protocol (TL Reviewer cerrando tarea), agregar al SKL-REPORT-01 del TL:

- Entries editadas (con `entryId` + qué se editó)
- Entries transicionadas (con `entryId` + `status` final + `fixTaskId` si aplica)
- Entries borradas (con `entryId` + razón + comment id de trazabilidad previo)

Conteo del manifest v1.5 (`delivery.dynamic_model_actions`):
- `devlog_resolved_count`
- `devlog_wontfix_count`
- `devlog_deferred_count`
- `devlog_deleted_count`

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| Entry actualizada | record VTT en `task_devlog_entries` | BD del backend VTT | Campos modificados + auto-side-effects según transición |
| `fixTaskId` link (caso §5.bis) | string (`VTS-XXX`) | Campo de la entry | Link documental a tarea correctiva (NO bloqueo) |
| Comment de trazabilidad (caso §5 Paso 7) | activity entry | Backend VTT | Razón del DELETE preservada en activity feed |
| Tarea correctiva nueva (caso §5.bis) | record VTT en `tasks` | Backend VTT | Solo si se aplicó flujo manual T3 |

---

## 7. Validación de salida

```bash
# Check 1: la entry tiene los campos esperados post-transicion
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
e = next((x for x in json.load(sys.stdin).get('data', []) if x.get('id') == '$ENTRY_ID'), None)
if not e:
    print('NOT FOUND (borrada o id incorrecto)')
else:
    print(f\"status: {e.get('status')}\")
    print(f\"resolvedAt: {e.get('resolvedAt')}\")
    print(f\"resolvedBy: {e.get('resolvedBy')}\")
    print(f\"resolution: {repr(e.get('resolution'))}\")
    print(f\"fixTaskId: {e.get('fixTaskId')}\")
    print(f\"deferredToPhaseId: {e.get('deferredToPhaseId')}\")
"

# Check 2: si transicion a resolved/wont_fix/deferred, el review-gate refleja el cambio
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/review-gate" -H "Authorization: Bearer $TOKEN"
# Esperado: si la entry era critical/high y pasó a terminal -> 1 blocker menos
```

Lista verificable post-lifecycle:

- [ ] `status` final coincide con el esperado (NO `pending` si pedimos terminal)
- [ ] Para `resolved`: `resolvedAt != null`, `resolvedBy != null`, `resolution` preservada
- [ ] Para `wont_fix`: `resolvedAt != null`, `resolvedBy = null`, `resolution` preservada
- [ ] Para `deferred`: `resolvedAt = null`, `resolvedBy = null`, `resolution = null`, `deferredToPhaseId` seteado (R14 aplicada — destino registrado fuera de `resolution`)
- [ ] **NO usar este Workflow para bloqueo del padre** — verificar que se aplicó `PROTOCOL-ASG-001 §5.4` si el caso lo requería

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| HTTP 400 `ENTRY_ALREADY_FINAL` | Intentar transicionar entry ya en `resolved`/`wont_fix`/`deferred` | Estados terminales son irreversibles. Workaround: `VTT.SKILL-DEV-005` (DELETE) + crear nuevo |
| HTTP 400 `"resolution es requerido"` | `status=resolved` o `wont_fix` sin `resolution` | Agregar `resolution` con descripción concreta del fix o justificación |
| HTTP 400 `"deferredToPhaseId es requerido"` | `status=deferred` sin UUID | Agregar `deferredToPhaseId` con UUID de fase destino |
| Entry queda inconsistente: `status:pending` pero `resolvedAt`/`resolvedBy`/`resolution` poblados | **R13 violada**: se usó DEV-003 con `status:resolved` en body | **NO usar DEV-003 para status.** Usar DEV-004 + `PATCH /status`. Para corregir el estado inconsistente: DELETE + recrear |
| Entry `deferred` quedó con `resolution: null` sin destino registrado | **R14 violada**: se intentó usar `resolution` para registrar el destino | El destino se perdió. Postear comment en la tarea referenciando `entryId` + destino para recuperar la trazabilidad. En futuras transiciones a `deferred`, aplicar workaround §4.2 (description / comment / fixTaskId) ANTES del PATCH |
| HTTP 400 `"Debe enviar al menos un campo"` (DEV-003) | Body `{}` vacío | Enviar ≥1 campo del set permitido |
| HTTP 400 `"Invalid enum value. Expected 'open' \| 'resolved' \| 'deferred'"` (DEV-003) | Se intentó `acknowledged` / `in_progress` / `wont_fix` en DEV-003 body | DEV-003 acepta set reducido — para esos status usar DEV-004 |
| HTTP 404 al DELETE | `entryId` no pertenece a `taskId` del path | Verificar ambos IDs coinciden |
| HTTP 403 al DELETE | Sin capability `tasks.update` | Renovar JWT (L8) — capabilities pueden estar desactualizadas |

---

## 9. Skills invocadas

| Skill | Para qué se usa en este Workflow |
|---|---|
| `VTT.SKILL-AUTH-001` | Obtener `$TOKEN` JWT |
| `VTT.SKILL-QUERY-003` | GET de la entry actual (Paso 1) — opcional pero recomendado |
| `VTT.SKILL-DEV-003` | Editar contenido (`title`/`description`/`severity`) — Paso 3a. **NUNCA para `status`** (R13) |
| `VTT.SKILL-DEV-004` | Transicionar lifecycle (PATCH `/status`) — Paso 3b/4/5.bis.3 |
| `VTT.SKILL-DEV-005` | DELETE entry duplicada/errónea — Paso 7. **Requiere comment de trazabilidad previo** |
| `VTT.SKILL-COMMENT-001` | Postear comment de trazabilidad antes del DELETE (Paso 7) o para registrar destino del `deferred` (R14 workaround) |

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-AGENT-001` Worktree por rol | El TL ejecuta este Workflow desde su worktree de rol (`project-tl`) — no desde el worktree del agente |
| `RULE-SEC-001` No postear datos sensibles | El `resolution` y `description` editados quedan visibles. Prohibido incluir credenciales o IPs prod |
| `RULE-DATA-001` Prohibido mockear datos | No "inventar" `resolution` para destrabar el gate. Si no se puede justificar, transicionar a `wont_fix` con razón real o crear Finding |

> Para descubrir reglas adicionales: `python 00.Rules/query_rules.py --simulate-task <TASK_ID>`.

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-06-10 | TW-OPS (VTS-027) — revisión LEAD_NPL | Versión inicial. Materializa FASE 3 del `PROTOCOL-DEV-001 v1.1.0` §5.3. Incorpora: **R13 destacada** (regla 4.1 — DEV-003 NUNCA para cambiar `status`, BUG-CONSISTENCIA H-3) + **R14 destacada** (regla 4.2 — preservar referencia en `deferred`, T2 BY-DESIGN) + **§5.bis flujo manual T3** (3 pasos POST `/phases/:id/tasks` → capturar `taskId` → PATCH `/devlog/:id/status` con `fixTaskId`) + **cross-ref explícito a `PROTOCOL-ASG-001 §5.4`** para casos de bloqueo del padre con auto-resume. Skills invocadas: DEV-003 / DEV-004 / DEV-005 / COMMENT-001 / QUERY-003 / AUTH-001. Origen: reporte VTS-026 §4.1 + bump Protocol VTS-051 (§5.5 + §7 R13/R14). |
