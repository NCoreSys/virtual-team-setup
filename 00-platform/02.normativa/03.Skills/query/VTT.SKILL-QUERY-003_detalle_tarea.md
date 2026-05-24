# VTT.SKILL-QUERY-003 — Detalle completo de una tarea

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-QUERY-003` |
| **Categoría** | QUERY (Consultas de lectura) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Para leer acceptance criteria, attachments, devlog entries y metadata completa de una tarea |
| **Reemplaza** | `SKL-QUERY-03_detalle-tarea.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `include` | enum array | sí/no | Default: solo metadata. Opciones extra: `criteria`, `attachments`, `devlog`, `comments`, `dependencies`, `issues`, `trackable_items` |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
```

---

## Ejecución

### Opción A — Metadata básica de la tarea

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

Campos clave del response:
- `title`, `description`, `statusCode`, `assignedToId`
- `phaseId`, `sprintId`, `deliveryId`
- `estimatedHours`, `actualHours`, `complexity`, `category`
- `createdAt`, `updatedAt`, `previousStatus`

### Opción B — Acceptance Criteria

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/criteria" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
cas = json.load(sys.stdin).get('data', [])
print(f'CAs total: {len(cas)}')
for ca in cas:
    print(f\"  {ca['id'][:8]}.. | {ca.get('status'):<10} | {ca.get('title')}\")
"
```

### Opción C — Attachments

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
ats = json.load(sys.stdin).get('data', [])
print(f'Attachments: {len(ats)}')
for a in ats:
    print(f\"  {a.get('fileType'):<15} | {a.get('fileName')} | by {(a.get('uploadedBy') or {}).get('email','?')}\")
"
```

### Opción D — Devlog entries

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
entries = json.load(sys.stdin).get('data', [])
print(f'Devlog entries: {len(entries)}')
for e in entries:
    cat = e.get('category') if isinstance(e.get('category'), str) else (e.get('category') or {}).get('code')
    print(f\"  [{cat}] {e.get('status'):<10} | {e.get('title')}\")
"
```

### Opción E — Comments

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
cs = json.load(sys.stdin).get('data', [])
print(f'Comments: {len(cs)}')
for c in cs:
    msg = (c.get('message') or '')[:80]
    print(f\"  {c.get('createdAt','?')[:19]} | {(c.get('user') or {}).get('email','?')} | {msg}\")
"
```

### Opción F — Bundle completo (script al inicio de review del TL)

```bash
echo '=== TASK ==='
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
d = json.load(sys.stdin)['data']
print(f\"title: {d.get('title')}\")
print(f\"status: {d.get('statusCode')}\")
print(f\"assignee: {(d.get('assignedTo') or {}).get('email')}\")
print(f\"estimated: {d.get('estimatedHours')}h | actual: {d.get('actualHours')}h\")
"

echo
echo '=== CAs ==='
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/criteria" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; cas=json.load(sys.stdin).get('data',[]); print(f'{len(cas)} CAs, met: {sum(1 for c in cas if c.get(\"status\")==\"met\")}')"

echo
echo '=== ATTACHMENTS ==='
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
ats = json.load(sys.stdin).get('data', [])
types = {}
for a in ats:
    types[a.get('fileType')] = types.get(a.get('fileType'),0) + 1
print(types)
"
```

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
d = json.load(sys.stdin).get('data')
print('OK' if d and d.get('id') else 'NOT_FOUND')
"
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 404 | TASK_ID no existe | Verificar el ID — debe ser el externo (MS-XXX), no el UUID interno |
| HTTP 401 | TOKEN expirado | Renovar con `VTT.SKILL-AUTH-001` |
| Endpoint devlog 404 | URL incorrecta | Es `/devlog` (singular), NO `/devlog-entries` |
| Lista vacía de criteria | Tarea nueva sin CAs aún | Generar CAs primero (parte del ASSIGNMENT) |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- `VTT.SKILL-TASK-005_review_tarea` (Paso 1 — leer entregables)
- `VTT.WORKFLOW-MAN-001.003` (recolección de IDs para el manifest v1.0)
- `VTT.SKILL-QUERY-001/.002` (después de listar, leer detalle de una)

---

## Cuándo NO usar esta Skill

- **Si solo querés conteo o lista** — usar `VTT.SKILL-QUERY-001/.002` (más liviano)
- **Si querés review_gate específicamente** — usar `GET /api/tasks/<id>/review-gate` directo

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-QUERY-03_detalle-tarea.md`. Ampliación: 6 opciones (A-F) con bundle completo para review del TL. Documentación de cada sub-endpoint (criteria, attachments, devlog, comments). |
