# VTT.SKILL-DEV-003 — Editar devlog entry (campos genéricos)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-DEV-003` |
| **Categoría** | DEV (Devlog) |
| **Versión** | 1.1 |
| **Fecha** | 2026-06-10 |
| **Aplica a** | Todos los roles ejecutores + TL Reviewer (correcciones durante review) |
| **Tokens estimados** | ~310 |
| **Cuándo se usa** | Corregir typos, agregar `description` faltante, cambiar `severity` sobre un devlog entry **ya creado**. **NUNCA para cambiar `status`** — usar `VTT.SKILL-DEV-004` (PATCH `/status`). Ver §Error CRÍTICO (R13) abajo. |
| **Permiso requerido** | `tasks.update` |
| **Pertenece a** | `VTT.WORKFLOW-DEV-001.002` (FASE 3 del `VTT.PROTOCOL-DEV-001` v1.1.0) |

---

## 🚨 ERROR CRÍTICO — H-3 BUG-CONSISTENCIA + R13 (v1.1)

> **Origen:** `VTT.PROTOCOL-DEV-001 v1.1.0 §7 R13` + hallazgo H-3 confirmado empíricamente VTS-026 §2.2.2.

### El bug en el endpoint genérico

El endpoint que sirve esta Skill — `PATCH /api/tasks/:taskId/devlog/:entryId` (body) — **acepta** `status` en el body Y **lo persiste a medias**, dejando el entry en estado **inconsistente**:

```bash
# Lo que NO debe hacerse:
PATCH /api/tasks/<TASK>/devlog/<ENTRY>
{
  "status": "resolved",
  "resolution": "Decision documentada"
}
```

| Campo | Lo que el cliente espera | Lo que el backend realmente hace |
|---|---|---|
| `status` | `pending` → `resolved` | **NO se mueve** (queda `pending`) |
| `resolvedAt` | seteado a `now` | **Sí se setea** a `now` |
| `resolvedBy` | seteado al `reportedBy` | **Sí se setea** |
| `resolution` | persistida | **Sí se persiste** |

Resultado: entry con `status:"pending"` PERO `resolvedAt`/`resolvedBy`/`resolution` poblados. Visualmente parece resuelta — operativamente no lo está. El Review Gate la cuenta como **no terminal** y la TL la ve en el feed con marcas confusas. **Causa: la doc del endpoint v1.0 (esta Skill) decía que aceptaba `status`. El backend lo "acepta" pero el ProtoLifecycle real está en `/status`.**

### R13 (regla del Protocol — bloqueante)

> **DEV-003 NUNCA para cambiar `status`.** Para cualquier transición de lifecycle usar **exclusivamente** `VTT.SKILL-DEV-004` (PATCH `/devlog/:entryId/status`).

Si necesitás cambiar `status`:
- `pending → acknowledged / in_progress / resolved / wont_fix / deferred` → **invocar `VTT.SKILL-DEV-004`** (no esta Skill).
- Si ya cometiste el error y la entry quedó inconsistente: borrar con `VTT.SKILL-DEV-005` y recrear (los estados finales son irreversibles vía PATCH — `ENTRY_ALREADY_FINAL`).

### Qué SÍ hace DEV-003

| Campo editable | Permitido en DEV-003 | Alternativa para lifecycle |
|---|---|---|
| `title` | ✅ Sí | — |
| `description` (agregar/corregir) | ✅ Sí | — |
| `severity` | ✅ Sí (respetando `severityLevels` de la categoría) | — |
| `status` | ❌ **EXCLUIDO — R13** | DEV-004 |
| `resolution` (sin cambio de status) | ⚠️ Permitido pero NO recomendado (queda colgado sin trazabilidad) | DEV-004 |
| `deferredToPhaseId` (sin cambio de status) | ⚠️ Permitido pero ineficaz | DEV-004 |
| `fixTaskId` (link documental, sin cambio de status) | ✅ Sí | — |

---

## ⚠️ CUÁNDO USAR ESTA SKILL vs `VTT.SKILL-DEV-004`

| Caso | Esta skill (DEV-003) | DEV-004 (lifecycle) |
|---|:---:|:---:|
| Corregir typo en `title` o `description` | ✅ | ❌ |
| Agregar `description` que faltaba | ✅ | ❌ |
| Cambiar `severity` (low ↔ high) | ✅ | ❌ |
| Pasar a `acknowledged` o `in_progress` | ❌ **EXCLUIDO (R13)** | ✅ |
| Cerrar como `wont_fix` con resolution | ❌ **EXCLUIDO (R13)** | ✅ |
| `resolved` con `resolution` + `fixTaskId` formal | ❌ **EXCLUIDO (R13 — BUG-CONSISTENCIA H-3)** | ✅ Único correcto |
| `deferred` con `deferredToPhaseId` formal | ❌ **EXCLUIDO (R13)** | ✅ Único correcto |

> **Política v1.1:** usar **DEV-003** EXCLUSIVAMENTE para edición de contenido (`title`/`description`/`severity`/`fixTaskId`). Para **cualquier** cambio de `status` usar `VTT.SKILL-DEV-004` (R13 bloqueante del Protocol v1.1.0).

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea dueña del entry |
| `entry_id` | uuid | sí | UUID del devlog entry a actualizar |
| `field_updates` | object | sí | **≥1 campo** del set permitido (ver §Campos editables abajo) |

### Campos editables (todos opcionales individualmente, ≥1 obligatorio en el body)

| Campo | Tipo | Permitido en v1.1 | Notas |
|---|---|---|---|
| `title` | string (1-500) | ✅ Sí | Editar título |
| `description` | string | ✅ Sí | Agregar/corregir descripción |
| `severity` | enum `critical` / `high` / `medium` / `low` | ✅ Sí | Cambiar severidad (respetando `severityLevels` de la categoría) |
| `status` | enum `open` / `resolved` / `deferred` | ❌ **EXCLUIDO (R13)** | **PROHIBIDO** — el backend acepta el body pero deja la entry inconsistente (H-3). Para lifecycle usar SIEMPRE `VTT.SKILL-DEV-004`. Ver §Error CRÍTICO arriba. |
| `resolution` | string | ⚠️ Permitido pero NO recomendado | Sin cambio de `status` (que está excluido) queda colgado sin trazabilidad. Usar DEV-004 para lifecycle con `resolution`. |
| `deferredToPhaseId` | uuid | ⚠️ Permitido pero ineficaz | Sin transición a `deferred` (excluida acá) no surte efecto. Usar DEV-004. |
| `fixTaskId` | string (`VTT-XXX` o uuid) | ✅ Sí | Link documental a tarea (NO bloqueante — ver Protocol §5.5 distinción trazabilidad vs bloqueo). |

> **Restricción crítica:** body con **≥1 campo**. Si enviás `{}` → HTTP 400 con mensaje `"Debe enviar al menos un campo para actualizar"`.
>
> **R13 (Protocol DEV-001 v1.1.0 §7):** si tu intención es cambiar `status` y de todos modos pasás `status` en el body de DEV-003, el backend lo "acepta" pero NO mueve el `status` — la entry queda inconsistente con `resolvedAt`/`resolvedBy`/`resolution` seteados pero `status:"pending"`. **Usar `VTT.SKILL-DEV-004` (PATCH `/status`) para CUALQUIER cambio de lifecycle.**

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- El `entry_id` existe en la tarea identificada por `task_id` (validar con GET previo si hay duda)
- El actor tiene permiso `tasks.update`
- Si vas a cambiar a `status=resolved` con `resolution`: el campo `resolution` ya tiene contenido válido
- Si vas a cambiar a `status=deferred`: tenés el UUID de la fase destino

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # https://api.vttagent.com  (siempre dominio — RULE-SEC-001 prohibe IP)
$TASK_ID                   # ID de la tarea (MS-XXX o VTS-XXX)
$ENTRY_ID                  # UUID del entry a editar
```

> **⚠️ Drift IP corregido en v1.1 (VTS-028):** la versión 1.0 documentaba `$VTT_BASE_URL=http://77.42.88.106:3000` — violaba RULE-SEC-001. Corregido a dominio prod. Hallazgo VTS-026 Anexo C.

---

## Ejecución

### Caso 1 — Corregir typo en `title`

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Decision corregida: usar Vite directo, no compilar el package"
  }'
```

### Caso 2 — Agregar `description` que faltaba

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "description": "Contexto agregado: se eligió path alias porque Vite resuelve directo TS sin compilar el package"
  }'
```

### Caso 3 — Cambiar `severity` de `low` → `medium`

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "severity": "medium"
  }'
```

### Caso 4 — Editar varios campos a la vez

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "description": "Contexto agregado: ...",
    "severity": "medium"
  }'
```

> **Respuesta esperada (200):** retorna el entry completo actualizado.

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
    print(f'title: {e.get(\"title\")}')
    print(f'severity: {e.get(\"severity\")}')
    print(f'status: {e.get(\"status\")}')
    print(f'description (len): {len(e.get(\"description\") or \"\")}')
else:
    print('NOT FOUND')
"
```

---

## Respuestas del backend

| Código | Significado |
|---|---|
| **200** | Entry actualizado — retorna el entry completo |
| **400** | Body vacío, validación fallida o `entry_id` no es UUID |
| **401** | Sin token |
| **403** | Sin permiso `tasks.update` |
| **404** | Entry no existe o no pertenece a la tarea |

---

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `"Debe enviar al menos un campo para actualizar"` | Body `{}` vacío | Enviar **≥1 campo** del set permitido |
| HTTP 400 `"entryId debe ser un UUID válido"` | Path param no es UUID | Verificar el `entry_id` — debe ser UUID, NO el código de la tarea |
| HTTP 404 | Entry no pertenece a la tarea del path | Verificar **ambos IDs** (`task_id` + `entry_id` deben coincidir) |
| HTTP 403 | Token sin permiso `tasks.update` | Confirmar rol del agente — usar token con permisos correctos |
| Status quedó `resolved` pero sin `resolvedAt` | Usar DEV-003 para resolver | DEV-003 NO ejecuta lógica automática de timestamps — usar **DEV-004** para `resolved` formal |
| `status` rechazado con valor `acknowledged`/`in_progress`/`wont_fix` | Set reducido | DEV-003 solo acepta `open`/`resolved`/`deferred`. Para los otros estados → **DEV-004** |

---

## Política de uso

- **DEV-003 es para edición libre de contenido.** No ejecuta validaciones cruzadas ni transiciones automáticas (timestamps, resolvedBy, etc.).
- **NO usar DEV-003 para cerrar formal de un entry** (`resolved`/`wont_fix`). Para eso usar **`VTT.SKILL-DEV-004`** que ejecuta el lifecycle completo con validaciones.
- **NO usar DEV-003 para deferir formal.** Para `deferred` con seguimiento usar `VTT.SKILL-DEV-004`.

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — obtener `$TOKEN`
- `VTT.SKILL-QUERY-003` (opcional, GET detalle de tarea) — verificar que el entry existe antes de editar

---

## Skills que invocan ESTA

- TL Reviewer durante review (corregir typos en devlog del agente sin cambiar lifecycle)
- Workflow del agente cuando corrige un entry propio antes de mover a `task_in_review`

---

## Cuándo NO usar esta Skill

- **Para cambiar a `acknowledged` / `in_progress` / `wont_fix`** → usar `VTT.SKILL-DEV-004` (DEV-003 no soporta esos estados)
- **Para cerrar formal con `resolution` + auto-timestamp `resolvedAt`/`resolvedBy`** → usar `VTT.SKILL-DEV-004`
- **Para deferir formal con tracking** → usar `VTT.SKILL-DEV-004`
- **Para CREAR un entry nuevo** → usar `VTT.SKILL-DEV-001` (decision) o `VTT.SKILL-DEV-002` (observation)
- **Para BORRAR un entry** → usar `VTT.SKILL-DEV-005` (delete)

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-20 | Versión inicial. Cubre el endpoint `PATCH /api/tasks/:taskId/devlog/:entryId` (genérico). Spec provista por BE de VTT. Documentación del set reducido de `status` permitido aquí (open/resolved/deferred) y referencia explícita a DEV-004 para los casos del lifecycle estricto (acknowledged/in_progress/wont_fix). |
| 1.1 | 2026-06-10 | **Bump VTS-028 sobre hallazgos VTS-026 + alineación con Protocol DEV-001 v1.1.0.** (1) **Drift IP corregido (RULE-SEC-001):** `$VTT_BASE_URL` cambia de `http://77.42.88.106:3000` a `https://api.vttagent.com`. Hallazgo VTS-026 Anexo C. (2) **§Error CRÍTICO nueva (BUG-CONSISTENCIA H-3 + R13):** documenta empíricamente que el endpoint genérico acepta `status` en body pero NO lo mueve — sí setea `resolvedAt`/`resolvedBy`/`resolution` y deja la entry inconsistente. Validación VTS-026 §2.2.2. Cita literal a R13 del Protocol DEV-001 v1.1.0 §7: "DEV-003 NUNCA para cambiar `status` — usar SIEMPRE DEV-004 (PATCH /status)". (3) Tabla §Campos editables actualizada: `status` marcado como **EXCLUIDO (R13)**; `resolution` y `deferredToPhaseId` marcados como permitidos pero NO recomendados sin cambio de status (que está excluido); `fixTaskId` permitido como link documental. (4) Tabla §Cuándo usar DEV-003 vs DEV-004 actualizada: `resolved`/`wont_fix`/`deferred`/`acknowledged`/`in_progress` todas marcadas EXCLUIDO en DEV-003 con R13. (5) Header agrega "Pertenece a `VTT.WORKFLOW-DEV-001.002`" (FASE 3 del Protocol). (6) Header §Cuándo se usa aclarado: "NUNCA para cambiar `status`". |
