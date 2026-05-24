# VTT.SKILL-STATUS-005 — Poner tarea en `task_on_hold`

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-STATUS-005` |
| **Categoría** | STATUS (Status transitions) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles (BE, DB, FE, QA, DO, DL, UX, TL, AR, SA, PM) |
| **Tokens estimados** | ~250 |
| **Cuándo se usa** | Cuando hay un blocker real que impide continuar la tarea (issue externo, dependencia faltante, decisión PM pendiente) |
| **Reemplaza** | `SKL-STATUS-05_task-on-hold.md` (legacy) |

---

## ⚠️ CRÍTICO — endpoint distinto al resto de status

Esta skill **NO usa `PATCH /api/tasks/<id>/status`** como las otras. Usa un endpoint dedicado:

```
PUT /api/tasks/<id>/on-hold
+ Header obligatorio: x-user-id: <agent_uuid>
```

**NUNCA usar `PATCH /status` con `statusId` de on_hold** — el endpoint diferente porque:
- Requiere registrar `type`, `title`, `description` del blocker
- Crea automáticamente un Issue vinculado a la tarea
- Captura el `previousStatus` para auto-resume cuando se resuelva

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `agent_uuid` | uuid | sí | UUID del agente (va en header `x-user-id`) |
| `blocker_type` | enum | sí | `blocker` / `dependency` / `pm_decision` / `external` |
| `blocker_title` | string ≤200 | sí | Título corto del blocker (ej. "Falta schema de BD") |
| `blocker_description` | string ≤2000 | sí | Descripción detallada con contexto y qué se necesita para desbloquear |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en cualquier status excepto `task_approved` o `task_cancelled` (estados terminales)
- El blocker es **real y verificable** — no on_hold por "tengo dudas", eso son comments al PM

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL
$AGENT_UUID                # va en x-user-id header
```

---

## Ejecución

```bash
curl -s -X PUT "$VTT_BASE_URL/api/tasks/$TASK_ID/on-hold" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-user-id: $AGENT_UUID" \
  -d "{
    \"type\": \"$BLOCKER_TYPE\",
    \"title\": \"$BLOCKER_TITLE\",
    \"description\": \"$BLOCKER_DESCRIPTION\"
  }"
```

---

## Comportamiento automático del backend

Cuando esta skill se ejecuta correctamente, VTT:

1. Cambia status a `task_on_hold`
2. Guarda el `previousStatus` (para auto-resume)
3. Crea Issue automáticamente vinculado a la tarea (con `sourceTaskId=<TASK_ID>`)
4. Notifica al PM (si tiene notificaciones configuradas)

Cuando el Issue se resuelve (vía `PATCH /issues/<id>/resolve`), VTT **auto-resume** la tarea al `previousStatus`.

---

## Validación

```bash
# Check 1: status correcto
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; d=json.load(sys.stdin)['data']; print('status:', d['statusCode'], 'prev:', d.get('previousStatus'))"
# Esperado: status: task_on_hold, prev: <status anterior>

# Check 2: issue creado
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/issues" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
issues = json.load(sys.stdin)['data']
open_issues = [i for i in issues if not i.get('isResolved')]
print('open_issues:', len(open_issues))
for i in open_issues:
    print(f\"  - {i['title']} ({i['type']})\")
"
# Esperado: open_issues: >= 1, con el title que pasaste
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `MISSING_HEADER` | Falta header `x-user-id` | Agregar `-H "x-user-id: $AGENT_UUID"` |
| HTTP 400 `INVALID_TYPE` | `blocker_type` no en enum | Usar `blocker`/`dependency`/`pm_decision`/`external` |
| Usar `PATCH /status` | Endpoint equivocado | Usar `PUT /on-hold` — son endpoints DIFERENTES |
| HTTP 403 | Token sin permisos | Verificar service-key del proyecto |
| Tarea en `task_approved` | Estado terminal, no se puede pausar | Crear tarea nueva de fix en su lugar |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Cómo desbloquear la tarea

Cuando el blocker se resuelva:

```bash
# Obtener el issue_id vinculado
ISSUE_ID=$(curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/issues" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; i=[x for x in json.load(sys.stdin)['data'] if not x.get('isResolved')][0]; print(i['id'])")

# Resolver issue → auto-resume
curl -s -X PATCH "$VTT_BASE_URL/api/issues/$ISSUE_ID/resolve" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"resolution\": \"<descripción del fix>\", \"resolvedBy\": \"$AGENT_UUID\"}"
```

La tarea vuelve automáticamente al `previousStatus` (típicamente `task_in_progress` o `task_in_review`).

---

## Cuándo NO usar esta Skill

- **Si tenés dudas, no bloqueante** — usar `VTT.SKILL-COMMENT-001` para consultar al PM
- **Si la tarea está aprobada** — crear tarea nueva de fix en su lugar
- **Si el "blocker" es priorización** — eso lo resuelve el PM con re-ordenamiento

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-STATUS-05_task-on-hold.md`. Contrato sin cambios. Ampliación: explicación del comportamiento automático del backend (issue + previousStatus + auto-resume) y comando para desbloquear. |
