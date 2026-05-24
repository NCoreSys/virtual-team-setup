# VTT.SKILL-QUERY-001 — Obtener mis tareas asignadas

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-QUERY-001` |
| **Categoría** | QUERY (Consultas de lectura) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles (cada agente consulta sus propias tareas) |
| **Tokens estimados** | ~120 |
| **Cuándo se usa** | Rutina de apertura de sesión — el agente verifica qué tareas tiene asignadas |
| **Reemplaza** | `SKL-QUERY-01_mis-tareas.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `agent_uuid` | uuid | sí | UUID del agente que consulta |
| `status_filter` | enum status | sí/no | Filtrar por status (default: todos los activos) |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID                # UUID del agente
```

---

## Ejecución

### Opción A — Solo tareas asignadas activas (default)

```bash
curl -s "$VTT_BASE_URL/api/tasks?assigneeId=$AGENT_UUID&status=task_assigned" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

### Opción B — Filtrar por status específico

```bash
# Tareas en in_progress (las que estoy ejecutando)
curl -s "$VTT_BASE_URL/api/tasks?assigneeId=$AGENT_UUID&status=task_in_progress" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool

# Tareas en in_review (esperando review del TL)
curl -s "$VTT_BASE_URL/api/tasks?assigneeId=$AGENT_UUID&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

### Opción C — Todas mis tareas activas (parseado)

```bash
curl -s "$VTT_BASE_URL/api/tasks?assigneeId=$AGENT_UUID" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
tasks = json.load(sys.stdin).get('data', [])
by_status = {}
for t in tasks:
    s = t.get('statusCode', 'unknown')
    by_status.setdefault(s, []).append({'id': t['id'], 'title': t.get('title')})
for status, items in by_status.items():
    print(f'\n=== {status} ({len(items)}) ===')
    for t in items:
        print(f\"  {t['id']} | {t['title']}\")
"
```

---

## Validación

```bash
# Lista NO está vacía si el agente tiene tareas
curl -s "$VTT_BASE_URL/api/tasks?assigneeId=$AGENT_UUID" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
print('total:', len(json.load(sys.stdin).get('data', [])))
"
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Lista vacía | Aún no tiene tareas asignadas | OK — esperar a que el TL/PM asigne |
| HTTP 401 | TOKEN expirado | Renovar con `VTT.SKILL-AUTH-001` |
| Status code desconocido | Filtro mal escrito | Usar: `task_pending`/`task_in_progress`/`task_in_review`/`task_on_hold` |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- Rutina de apertura de cualquier agente
- `VTT.SKILL-QUERY-003` (detalle de tarea) — typically se llama después con el `task_id` que esta devuelve

---

## Cuándo NO usar esta Skill

- **Si querés ver tareas de OTROS agentes** — usar `VTT.SKILL-QUERY-002` (tareas en revisión del proyecto) o consulta directa con `?assigneeId=<otro>`

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-QUERY-01_mis-tareas.md`. Ampliación: 3 opciones de ejecución (filtro estricto, filtro por status, parseado en grupos). Contrato sin cambios. |
