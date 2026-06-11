# VTT.SKILL-DEV-004 — Lifecycle de devlog entry (cambio de status formal)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-DEV-004` |
| **Categoría** | DEV (Devlog) |
| **Versión** | 1.1 |
| **Fecha** | 2026-06-10 |
| **Aplica a** | Todos los roles ejecutores + TL Reviewer (resolver/deferir en cierre) |
| **Tokens estimados** | ~420 |
| **Cuándo se usa** | Transición formal de un devlog entry por su ciclo de vida: `acknowledged`, `in_progress`, `resolved`, `wont_fix`, `deferred`. **Único endpoint correcto para cambiar `status`** (R13 del Protocol DEV-001 v1.1.0 §7). |
| **Permiso requerido** | `tasks.update` |
| **Pertenece a** | `VTT.WORKFLOW-DEV-001.002` (FASE 3 del `VTT.PROTOCOL-DEV-001` v1.1.0) y `VTT.WORKFLOW-DEV-001.003` (FASE 4 cierre sprint) |

---

## ⚠️ ESTADOS FINALES IRREVERSIBLES

Una vez que un entry pasa a uno de estos 3 estados, **NO se puede cambiar más**:

| Estado final | Reversible | Acción si te equivocaste |
|---|:---:|---|
| `resolved` | ❌ Irreversible | Borrar con `VTT.SKILL-DEV-005` y crear nuevo |
| `wont_fix` | ❌ Irreversible | Borrar y crear nuevo |
| `deferred` | ❌ Irreversible | Borrar y crear nuevo |

Si intentás cambiar el status de un entry ya en estado final → HTTP 400 `ENTRY_ALREADY_FINAL`.

---

## ⚠️ CUÁNDO USAR ESTA SKILL vs `VTT.SKILL-DEV-003`

| Caso | DEV-003 (edit) | Esta skill (DEV-004) |
|---|:---:|:---:|
| Corregir typo en `title`/`description` | ✅ | ❌ |
| Cambiar `severity` | ✅ | ❌ |
| Pasar a `acknowledged` | ❌ | ✅ (única opción) |
| Pasar a `in_progress` | ❌ | ✅ (única opción) |
| Cerrar como `resolved` con `resolution` formal + auto-timestamp | ⚠️ Permisivo (sin validaciones) | ✅ **Recomendado** |
| Cerrar como `wont_fix` | ❌ | ✅ (única opción) |
| Deferir con tracking formal | ⚠️ Permisivo | ✅ **Recomendado** |

> **Política:** usar **DEV-004** para transiciones formales del lifecycle. El backend ejecuta validaciones cruzadas y registra timestamps automáticos.

---

## Estados del lifecycle

```
                 ┌─────────────────────────┐
                 │      open (default)     │
                 └────┬──────────────┬─────┘
                      │              │
                      ▼              ▼
            ┌──────────────┐  ┌──────────────┐
            │ acknowledged │  │  in_progress │ ────┐
            └──────┬───────┘  └──────┬───────┘     │
                   │                 │             │
                   └──────┬──────────┘             │
                          │                        │
              ┌───────────┼───────────┬────────────┘
              ▼           ▼           ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ resolved │ │ wont_fix │ │ deferred │  ← ESTADOS FINALES
        └──────────┘ └──────────┘ └──────────┘
```

| Estado | Significado | Quién lo activa típicamente |
|---|---|---|
| `open` | Entry recién creado, sin acción | El backend al crear |
| `acknowledged` | El TL/PM vio el entry pero todavía no actúa | TL durante review |
| `in_progress` | Hay alguien activamente trabajando en resolverlo | Agente o TL |
| `resolved` | El entry quedó solucionado | TL o agente que resolvió |
| `wont_fix` | Se decidió NO arreglar (acepta el comportamiento) | TL/PM |
| `deferred` | Se pospone a otra fase del proyecto | TL/PM |

---

## Comportamiento automático del backend

| Transición a | Acción automática del backend |
|---|---|
| `resolved` | Registra `resolvedAt = now` y `resolvedBy = reportedBy original del entry` |
| `wont_fix` | Registra `resolvedAt = now` (NO registra `resolvedBy` porque no fue resuelto) |
| `deferred` | **Limpia** `resolvedAt`, `resolvedBy`, `resolution` (queda como pendiente en otra fase) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea dueña del entry |
| `entry_id` | uuid | sí | UUID del devlog entry a transicionar |
| `status` | enum | **sí** | `acknowledged` / `in_progress` / `resolved` / `wont_fix` / `deferred` |
| `resolution` | string ≥1 char | **condicional** | **OBLIGATORIO** si `status` ∈ {`resolved`, `wont_fix`} |
| `deferredToPhaseId` | uuid | **condicional** | **OBLIGATORIO** si `status = deferred` |
| `fixTaskId` | string (`VTT-XXX` o uuid) | opcional | Tarea que resuelve el devlog (recomendado con `resolved`) |

### Tabla de obligatoriedad por status

| Status objetivo | `resolution` | `deferredToPhaseId` | `fixTaskId` |
|---|:---:|:---:|:---:|
| `acknowledged` | — | — | opcional |
| `in_progress` | — | — | opcional |
| `resolved` | **obligatorio** | — | recomendado |
| `wont_fix` | **obligatorio** | — | — |
| `deferred` | — | **obligatorio** | opcional |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- El `entry_id` existe en la tarea identificada por `task_id`
- **El entry NO está en estado final** (`resolved`/`wont_fix`/`deferred`) — verificar con GET previo si hay duda
- El actor tiene permiso `tasks.update`
- Si vas a `resolved`/`wont_fix`: tenés `resolution` listo
- Si vas a `deferred`: tenés `deferredToPhaseId` (UUID de la fase destino)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # https://api.vttagent.com  (siempre dominio — RULE-SEC-001 prohibe IP)
$TASK_ID                   # MS-XXX o VTS-XXX
$ENTRY_ID                  # UUID del entry
```

> **⚠️ Drift IP corregido en v1.1 (VTS-028):** la versión 1.0 documentaba `$VTT_BASE_URL=http://77.42.88.106:3000` — violaba RULE-SEC-001. Corregido a dominio prod. Hallazgo VTS-026 Anexo C.

---

## Ejecución

### Caso 1 — `acknowledged` (TL vio el entry pero no actúa todavía)

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "acknowledged"
  }'
```

### Caso 2 — `in_progress` (alguien está trabajando en resolverlo)

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "in_progress"
  }'
```

### Caso 3 — `resolved` con `resolution` + `fixTaskId` (recomendado)

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "resolved",
    "resolution": "Corregido en commit abc1234 — se agregó moduleResolution bundler en tsconfig.json",
    "fixTaskId": "MS-340"
  }'
```

> **Backend ejecuta auto:** `resolvedAt = now`, `resolvedBy = reportedBy del entry`.

### Caso 4 — `wont_fix` con `resolution` (decidir NO arreglar)

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "wont_fix",
    "resolution": "Decisión PM: el costo de fix supera el beneficio. Se documenta como comportamiento aceptado."
  }'
```

> **Backend ejecuta auto:** `resolvedAt = now`. NO registra `resolvedBy` (no fue resuelto).

### Caso 5 — `deferred` a otra fase (T2 BY-DESIGN + R14)

> **🚨 Comportamiento BY-DESIGN del backend (T2 — confirmado empíricamente VTS-026):** al transicionar a `deferred`, el backend **limpia a `null`** los campos `resolution`, `resolvedAt` y `resolvedBy`. NO es bug — es comportamiento intencional documentado en `PROTOCOL-DEV-001 v1.1.0 §4` tabla auto-side-effects + servicio línea 227. La FEATURE v1.1 §4.1 exige "referencia obligatoria al destino" en `deferred`, pero esa referencia **NO puede vivir en `resolution`** (se borra).
>
> **Regla R14 del Protocol DEV-001 v1.1.0 §7:** *"Cuando se transiciona a `deferred`, **NUNCA** confiar en `resolution` para guardar la referencia al destino: el backend la limpia a `null` (BY-DESIGN — T2 confirmado VTS-026). Usar `description` original, comment en la tarea, o `fixTaskId` (si el destino es una tarea)."*

#### Ejemplo básico (sin workaround — la referencia se pierde)

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "deferred",
    "deferredToPhaseId": "<UUID_FASE_DESTINO>",
    "resolution": "Elevado a TD-CORE-003"
  }'
```

> ❌ **NO HACER ASÍ:** el `resolution` enviado se descarta a `null`. La referencia "TD-CORE-003" se pierde silenciosamente. Solo queda `deferredToPhaseId` (el UUID de la fase, sin contexto operativo).

#### 3 workarounds para preservar la referencia al destino (R14)

Aplicar **una** de las 3 opciones según el momento en que se conoce el destino:

##### Workaround 1 — `description` original (destino conocido al CREAR el entry)

Si al crear la entry (en FASE 1) ya sabés que va a diferirse a un destino concreto, escribilo en el `description` original. El backend **preserva `description`** en cualquier transición.

```bash
# Al crear (FASE 1, VTT.SKILL-DEV-001 o DEV-002):
{
  "categoryCode": "tech_debt",
  "title": "CleanupService fuera de scope S2",
  "description": "Memoria crece sin límite. Si se difiere, va a TD-CORE-003 del proyecto.",
  ...
}

# Al diferir (este Caso 5):
{ "status": "deferred", "deferredToPhaseId": "<UUID>" }

# Resultado: description preservado con la referencia. Trazabilidad OK.
```

##### Workaround 2 — Comment en la tarea (destino decidido AL diferir — caso típico)

Si el destino se decide al momento del diferimiento, postear un comment en la tarea **antes** del PATCH a `deferred`. El comment queda en activity feed visible y permanente.

```bash
# Paso 1: comment de trazabilidad
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Entry $ENTRY_ID diferido → TD-CORE-003 (compromiso cross-sprint) / Sprint DEUDA-B1A\",
    \"userId\": \"$AGENT_UUID\"
  }"

# Paso 2: PATCH /status a deferred
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "deferred",
    "deferredToPhaseId": "<UUID_FASE_DESTINO>"
  }'
```

##### Workaround 3 — `fixTaskId` (destino es una tarea concreta)

Si el destino del traspaso es una tarea concreta del backlog (típicamente del Sprint DEUDA), setear `fixTaskId` en el mismo PATCH. El backend **preserva `fixTaskId`** al diferir.

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "deferred",
    "deferredToPhaseId": "<UUID_FASE_DESTINO>",
    "fixTaskId": "VTS-940"
  }'
```

> El campo `fixTaskId` queda en BD como link documental a la tarea destino. El TL/PM al revisar la entry en code review o cierre de sprint puede saltar a la tarea correctiva con ese campo.

#### Auto-side-effects que SÍ aplican en `deferred`

| Campo | Comportamiento |
|---|---|
| `status` | → `deferred` (terminal — irreversible) |
| `resolvedAt` | **limpia a `null`** (T2 BY-DESIGN) |
| `resolvedBy` | **limpia a `null`** (T2 BY-DESIGN) |
| `resolution` | **limpia a `null`** (T2 BY-DESIGN — viola R14 si se confió ahí) |
| `description` | **preservado** (workaround 1) |
| `deferredToPhaseId` | persistido (obligatorio) |
| `fixTaskId` | **preservado** si se envió (workaround 3) |

> **Validación post-PATCH:** verificar con `GET /devlog` que `description` y/o `fixTaskId` siguen poblados con la referencia al destino. Si ambos están vacíos y solo se confió en `resolution`, la trazabilidad se perdió — postear comment retroactivo (workaround 2) inmediatamente para no perder el contexto.

---

## Validación post-update

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" \
  -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
data = json.load(sys.stdin).get('data', [])
e = next((x for x in data if x.get('id') == '$ENTRY_ID'), None)
if e:
    print(f'status: {e.get(\"status\")}')
    print(f'resolvedAt: {e.get(\"resolvedAt\")}')
    print(f'resolvedBy: {e.get(\"resolvedBy\")}')
    print(f'resolution: {e.get(\"resolution\")}')
    print(f'fixTaskId: {e.get(\"fixTaskId\")}')
    print(f'deferredToPhaseId: {e.get(\"deferredToPhaseId\")}')
else:
    print('NOT FOUND')
"
```

---

## Respuestas del backend

| Código | Significado |
|---|---|
| **200** | Estado actualizado — retorna entry completo |
| **400 `ENTRY_ALREADY_FINAL`** | El entry ya está en `resolved`/`deferred`/`wont_fix` — irreversible |
| **400** `"resolution es requerido..."` | `status=resolved` o `wont_fix` sin `resolution` |
| **400** `"deferredToPhaseId es requerido..."` | `status=deferred` sin `deferredToPhaseId` |
| **400** `"entryId debe ser un UUID válido"` | Path param no es UUID |
| **401** | Sin token |
| **403** | Sin permiso `tasks.update` |
| **404** | Entry no existe o no pertenece a la tarea |

---

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `ENTRY_ALREADY_FINAL` | Entry ya está en `resolved`/`deferred`/`wont_fix` | Estados finales son **irreversibles** — borrar con `VTT.SKILL-DEV-005` y crear nuevo entry |
| HTTP 400 `"resolution es requerido"` | `status=resolved` o `wont_fix` sin `resolution` | Agregar `resolution` con descripción concreta del fix |
| HTTP 400 `"deferredToPhaseId es requerido"` | `status=deferred` sin UUID de fase | Agregar `deferredToPhaseId` con el UUID de la fase destino |
| `resolution` vacío string `""` | Pasar string vacío | El backend valida `≥1 char` — no aceptar vacío |
| Status quedó `resolved` pero `resolvedAt` null | Usaste DEV-003 en vez de DEV-004 | DEV-003 no ejecuta lógica automática. Usar DEV-004 para `resolved` formal |
| `deferred` borró mi `resolution` | Comportamiento esperado del backend | `deferred` limpia `resolution/resolvedAt/resolvedBy` por diseño |
| HTTP 404 | `entry_id` no pertenece al `task_id` del path | Verificar ambos IDs — el entry pertenece a UNA tarea específica |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — obtener `$TOKEN`
- `VTT.SKILL-QUERY-003` (opcional, GET devlog de tarea) — verificar status actual del entry antes de transicionar (evita el `ENTRY_ALREADY_FINAL`)

---

## Skills que invocan ESTA

- **TL Reviewer** durante FASE 4 del PROTOCOL-ASG-001 (Modelo Dinámico §5.5.10) — resolver/deferir todos los entries pendientes al cerrar la tarea
- **Agente** durante ejecución cuando resuelve una decisión/observación propia
- `VTT.WORKFLOW-MAN-001.004 §Paso 5` — TL agrega `dynamic_model_actions.devlog_resolved_count` al manifest v1.5 (esos resolved se hacen con esta skill)

---

## Cuándo NO usar esta Skill

- **Para editar `title`/`description`/`severity`** sin cambiar lifecycle → usar `VTT.SKILL-DEV-003`
- **Para CREAR un entry** → usar `VTT.SKILL-DEV-001` (decision) o `VTT.SKILL-DEV-002` (observation)
- **Para corregir un entry ya en estado final** → no se puede; borrar con `VTT.SKILL-DEV-005` y crear nuevo
- **Si solo querés actualizar `severity` sin cambiar `status`** → DEV-003 (DEV-004 espera `status` obligatorio)

---

## Cómo prevenir `ENTRY_ALREADY_FINAL`

Antes de invocar DEV-004 con un status final:

```bash
# Verificar status actual del entry
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
e = next((x for x in json.load(sys.stdin).get('data', []) if x.get('id') == '$ENTRY_ID'), None)
if not e:
    print('NOT FOUND')
elif e.get('status') in ('resolved','wont_fix','deferred'):
    print(f'YA EN FINAL: {e[\"status\"]} — NO transicionar')
else:
    print(f'OK transicionar desde: {e.get(\"status\")}')
"
```

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-22 | Versión inicial. Cubre el endpoint `PATCH /api/tasks/:taskId/devlog/:entryId/status` (lifecycle estricto con validaciones cruzadas). Spec provista por BE de VTT. Documenta los 3 estados finales irreversibles (`resolved`/`wont_fix`/`deferred`), la lógica automática de timestamps (`resolvedAt`/`resolvedBy`) y la tabla de obligatoriedad de `resolution`/`deferredToPhaseId` según status objetivo. |
| 1.1 | 2026-06-10 | **Bump VTS-028 sobre hallazgos VTS-026 + alineación con Protocol DEV-001 v1.1.0.** (1) **Drift IP corregido (RULE-SEC-001):** `$VTT_BASE_URL` cambia de `http://77.42.88.106:3000` a `https://api.vttagent.com`. Hallazgo VTS-026 Anexo C. (2) **§Caso 5 (`deferred`) ampliado con T2 BY-DESIGN + 3 workarounds (R14).** Documenta empíricamente que el backend limpia `resolution`/`resolvedAt`/`resolvedBy` a `null` al transicionar a `deferred` — NO es bug, es comportamiento intencional (T2 confirmado VTS-026 §2.3 + Protocol §4 tabla auto-side-effects). Agrega 3 workarounds explícitos para preservar la referencia al destino sin confiar en `resolution`: (W1) escribir destino en `description` original al crear la entry; (W2) postear comment de trazabilidad antes del PATCH (caso típico cuando destino se decide al diferir); (W3) usar `fixTaskId` si destino es tarea concreta del backlog. Cita literal a R14 del Protocol DEV-001 v1.1.0 §7: "NUNCA confiar en `resolution` para guardar la referencia al destino". (3) Header §Cuándo se usa marca DEV-004 como **único endpoint correcto para cambiar `status`** con cita a R13. (4) Header agrega "Pertenece a `VTT.WORKFLOW-DEV-001.002`" (FASE 3) y `VTT.WORKFLOW-DEV-001.003` (FASE 4). |
