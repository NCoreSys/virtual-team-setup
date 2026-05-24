# VTT.SKILL-QUERY-005 — Estado de fase: qué tareas son asignables

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-QUERY-005` |
| **Categoría** | QUERY (Consultas de lectura) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | TL, SA Reviewer, PM |
| **Tokens estimados** | ~400 |
| **Cuándo se usa** | Al revisar el avance de una fase para decidir qué tareas asignar en el siguiente ciclo (planificación de sprint, asignación incremental) |
| **Reemplaza** | `SKL-QUERY-05_estado-fase-asignable.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `phase_uuid` | uuid | sí | UUID de la fase a analizar |
| `project_id` | uuid | sí | UUID del proyecto |
| `verbose` | bool | sí/no | Si `true`, también verifica attachments de cada `task_pending` |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- `PHASE_UUID` conocido (en el OPERATIVO del proyecto)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$PHASE_UUID                # UUID de la fase
```

---

## Paso 1 — Obtener todas las tareas de la fase agrupadas por status

```bash
curl -s "$VTT_BASE_URL/api/tasks?phaseId=$PHASE_UUID" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
tasks = json.load(sys.stdin).get('data', [])

by_status = {}
for t in tasks:
    s = t.get('statusCode', 'unknown')
    by_status.setdefault(s, []).append({
        'id': t['id'],
        'title': t.get('title'),
        'assignee': (t.get('assignedTo') or {}).get('email', 'sin-asignar')
    })

order = ['task_pending','task_blocked','task_in_progress','task_in_review','task_completed','task_approved','task_on_hold']
for s in order:
    items = by_status.get(s, [])
    if items:
        print(f'\n=== {s.upper()} ({len(items)}) ===')
        for t in items:
            print(f\"  {t['id']} | {t['title']} | {t['assignee']}\")
"
```

---

## Paso 2 — Identificar qué tareas son asignables AHORA

Una tarea es **asignable** si cumple **todo**:

```
[ ] status = task_pending
[ ] Tiene ASSIGNMENT subido como attachment (fileType=assignment)
[ ] Sus dependencias están en task_completed o task_approved
```

### Verificar attachments de una tarea pending

```bash
TASK_ID=<MS-XXX>

curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
att = json.load(sys.stdin).get('data', [])
types = [a.get('fileType') for a in att]
has_assignment = 'assignment' in types
has_brief = 'brief' in types
print(f'BRIEF: {\"✅\" if has_brief else \"❌ FALTA\"}')
print(f'ASSIGNMENT: {\"✅ asignable\" if has_assignment else \"❌ generar primero VTT.SKILL-TASK-002\"}')
"
```

### Verificar status de dependencias

```bash
DEPS=$(curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/dependencies" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
deps = json.load(sys.stdin).get('data', [])
print(' '.join(d.get('dependsOnTaskId') for d in deps))
")

for DEP in $DEPS; do
    STATUS=$(curl -s "$VTT_BASE_URL/api/tasks/$DEP" -H "Authorization: Bearer $TOKEN" \
      | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])")
    if [[ "$STATUS" != "task_completed" && "$STATUS" != "task_approved" ]]; then
        echo "BLOCKED: $DEP en $STATUS"
    else
        echo "OK: $DEP en $STATUS"
    fi
done
```

---

## Paso 3 — Interpretar y decidir

| Status | Acción TL |
|---|---|
| `task_pending` + sin ASSIGNMENT | Generar ASSIGNMENT con `VTT.SKILL-TASK-002` antes de asignar |
| `task_pending` + con ASSIGNMENT + deps OK | ✅ **Asignable ahora** (`VTT.SKILL-TASK-003`) |
| `task_pending` + con ASSIGNMENT + deps NO OK | Esperar — verificar dependencias |
| `task_blocked` | Investigar la causa — esperar dependencias o resolver bloqueo |
| `task_in_progress` | Monitorear — preguntar al agente si necesita soporte |
| `task_in_review` | **Hacer review** con `VTT.SKILL-TASK-005` |
| `task_on_hold` | Diagnosticar blocker — escalar al PM si no se puede resolver |
| `task_completed` | Esperar aprobación PM (`VTT.SKILL-STATUS-004`) |
| `task_approved` | Cerrada — no requiere acción |

---

## Paso 4 — Generar reporte para PM

```markdown
## Estado Fase <NOMBRE> — <FECHA>

### Resumen
- Pending: <N> | Blocked: <N> | In Progress: <N> | In Review: <N> | Completed: <N> | Approved: <N>

### Asignables ahora (pending + ASSIGNMENT listo + deps OK):
- <TASK_ID> <título> → Agente sugerido: <ROL>

### Pending sin ASSIGNMENT (necesitan preparación):
- <TASK_ID> <título> → Generar ASSIGNMENT antes de asignar

### Bloqueadas (dependencias pendientes):
- <TASK_ID> <título> → Bloqueada por <DEP_TASK_ID> (status: <X>)

### En review (pendientes de mi acción):
- <TASK_ID> <título> → Ejecutar VTT.SKILL-TASK-005

### En hold (requieren atención):
- <TASK_ID> <título> → Causa: <descripción>

### Recomendación de TL:
<Qué asignar primero y por qué>
```

---

## Reglas críticas

- ❌ NUNCA asignar una tarea sin ASSIGNMENT subido en VTT
- ❌ NUNCA asignar si las dependencias no están en `task_completed` o `task_approved`
- ✅ Una tarea `task_blocked` solo se desbloquea cuando su dependencia llega a completed/approved
- ✅ Si hay tareas en `task_in_review` → **hacer review ANTES** de asignar nuevas

---

## Validación

```bash
# Verificar conteo total
curl -s "$VTT_BASE_URL/api/tasks?phaseId=$PHASE_UUID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print('total:', len(json.load(sys.stdin).get('data',[])))"
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Lista vacía | `PHASE_UUID` incorrecto | Verificar UUID en el OPERATIVO |
| Tarea aparece como `task_pending` pero no es asignable | Sin ASSIGNMENT o deps pendientes | Ejecutar paso 2 para diagnosticar |
| Reporte sin "asignables ahora" | Todas pending sin assignment | Generar ASSIGNMENTs faltantes con `VTT.SKILL-TASK-002` |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-QUERY-003_detalle_tarea` — para attachments y dependencies por tarea

---

## Skills que invocan ESTA

- Rutina de apertura del TL al iniciar sprint
- Antes de invocar `VTT.SKILL-TASK-003` (asignar tarea), el TL debe correr esta para confirmar candidatas

---

## Cuándo NO usar esta Skill

- **Si solo querés el % de avance** — usar `VTT.SKILL-QUERY-004` (más liviano)
- **Si querés ver tareas del sprint** (no de la fase) — usar `?sprintId=<id>` en lugar de `?phaseId=`

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-QUERY-05_estado-fase-asignable.md`. Estructura los 4 pasos (listar, verificar attachments, interpretar, reportar) con reglas críticas. Cross-refs actualizadas a las skills nuevas. |
