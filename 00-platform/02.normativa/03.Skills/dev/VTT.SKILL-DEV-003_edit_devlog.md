# VTT.SKILL-DEV-003 — Editar devlog entry (campos genéricos)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-DEV-003` |
| **Categoría** | DEV (Devlog) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-20 |
| **Aplica a** | Todos los roles ejecutores + TL Reviewer (correcciones durante review) |
| **Tokens estimados** | ~250 |
| **Cuándo se usa** | Corregir typos, agregar `description` faltante, cambiar `severity` o aplicar lifecycle simple (open/resolved/deferred) sobre un devlog entry **ya creado** |
| **Permiso requerido** | `tasks.update` |

---

## ⚠️ CUÁNDO USAR ESTA SKILL vs `VTT.SKILL-DEV-004`

| Caso | Esta skill (DEV-003) | DEV-004 (lifecycle) |
|---|:---:|:---:|
| Corregir typo en `title` o `description` | ✅ | ❌ |
| Agregar `description` que faltaba | ✅ | ❌ |
| Cambiar `severity` (low ↔ high) | ✅ | ❌ |
| Pasar a `acknowledged` o `in_progress` | ❌ (no soporta) | ✅ |
| Cerrar como `wont_fix` con resolution | ❌ (no soporta) | ✅ |
| `resolved` con `resolution` + `fixTaskId` formal | ⚠️ Funciona pero permisivo | ✅ Recomendado (validaciones estrictas) |
| `deferred` simple (sin lifecycle estricto) | ✅ Permitido | ✅ Recomendado |

> **Política:** usar **DEV-003** para correcciones de contenido. Usar **DEV-004** para transiciones formales del ciclo de vida del entry (con validaciones cruzadas).

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea dueña del entry |
| `entry_id` | uuid | sí | UUID del devlog entry a actualizar |
| `field_updates` | object | sí | **≥1 campo** del set permitido (ver §Campos editables abajo) |

### Campos editables (todos opcionales individualmente, ≥1 obligatorio en el body)

| Campo | Tipo | Notas |
|---|---|---|
| `title` | string (1-500) | Editar título |
| `description` | string | Agregar/corregir descripción |
| `severity` | enum `critical` / `high` / `medium` / `low` | Cambiar severidad |
| `status` | enum **`open` / `resolved` / `deferred`** (set reducido) | Lifecycle simple (sin validaciones estrictas) |
| `resolution` | string | Texto de cómo se resolvió |
| `deferredToPhaseId` | uuid | Solo si se difiere a otra fase |
| `fixTaskId` | string (`VTT-XXX` o uuid) | Tarea que resuelve el devlog |

> **Restricción crítica:** body con **≥1 campo**. Si enviás `{}` → HTTP 400 con mensaje `"Debe enviar al menos un campo para actualizar"`.

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
$VTT_BASE_URL              # http://77.42.88.106:3000
$TASK_ID                   # ID de la tarea (MS-XXX)
$ENTRY_ID                  # UUID del entry a editar
```

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
