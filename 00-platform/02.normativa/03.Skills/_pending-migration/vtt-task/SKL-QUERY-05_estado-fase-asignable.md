# SKL-QUERY-05: Estado de fase activa — qué tareas se pueden asignar

**Categoría:** VTT-QUERY  
**Aplica a:** TL, SA Reviewer, PM  
**Tokens estimados:** ~120  
**Cuándo:** Al revisar el avance de una fase para decidir qué tareas asignar en el siguiente ciclo

---

## Precondición

- `$TOKEN` obtenido (SKL-AUTH-01)
- `$PHASE_UUID` — UUID de la fase a revisar (del OPERATIVO del proyecto)
- `$PROJECT_ID` — UUID del proyecto

---

## Paso 1 — Obtener todas las tareas de la fase

```bash
curl -s "$VTT_BASE_URL/api/tasks?phaseId=$PHASE_UUID" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
tasks = json.load(sys.stdin).get('data', [])
by_status = {}
for t in tasks:
    s = t.get('status', 'unknown')
    by_status.setdefault(s, []).append({'id': t['id'], 'title': t['title'], 'assignee': t.get('assignedTo', {}).get('email', 'sin asignar')})

order = ['task_pending','task_blocked','task_in_progress','task_in_review','task_completed','task_approved','task_on_hold']
for s in order:
    items = by_status.get(s, [])
    if items:
        print(f'\n=== {s.upper()} ({len(items)}) ===')
        for t in items:
            print(f'  {t[\"id\"]} | {t[\"title\"]} | {t[\"assignee\"]}')
"
```

---

## Paso 2 — Identificar qué tareas son asignables

Una tarea es **asignable ahora** si cumple todo:

```
[ ] status = task_pending
[ ] Tiene ASSIGNMENT subido como attachment (fileType=assignment)
[ ] Sus dependencias están en task_completed o task_approved
```

```bash
# Verificar attachments de una tarea pending
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
att = json.load(sys.stdin).get('data', [])
types = [a.get('fileType') for a in att]
has_assignment = 'assignment' in types
has_brief = 'brief' in types
print(f'BRIEF: {\"✅\" if has_brief else \"❌ FALTA\"}')
print(f'ASSIGNMENT: {\"✅\" if has_assignment else \"❌ FALTA — generar antes de asignar\"}')
"
```

---

## Paso 3 — Interpretar y decidir

| Status | Acción TL |
|--------|-----------|
| `task_pending` + sin ASSIGNMENT | Generar ASSIGNMENT (SKL-TASK-02) antes de asignar |
| `task_pending` + con ASSIGNMENT | ✅ Asignable ahora (SKL-TASK-03) |
| `task_blocked` | Verificar dependencias — no asignar hasta que dependencias estén completed/approved |
| `task_in_progress` | Monitorear — preguntar al agente si necesita soporte |
| `task_in_review` | Hacer review (SKL-TASK-05) |
| `task_on_hold` | Diagnosticar blocker — escalar al PM si no se puede resolver |

---

## Paso 4 — Reportar al PM

```markdown
## Estado Fase [NOMBRE] — [FECHA]

### Resumen
- Pending: [N] | Blocked: [N] | In Progress: [N] | In Review: [N] | Completed: [N] | Approved: [N]

### Asignables ahora (pending + ASSIGNMENT listo):
- [TASK_ID] [título] → Agente sugerido: [ROL]

### Pending sin ASSIGNMENT (necesitan preparación):
- [TASK_ID] [título] → Generar ASSIGNMENT antes de asignar

### Bloqueadas (dependencias pendientes):
- [TASK_ID] [título] → Bloqueada por [TASK_ID_DEPENDENCIA] (status: [X])

### En revisión (pendientes de mi review):
- [TASK_ID] [título] → Ejecutar SKL-TASK-05

### En hold (requieren atención):
- [TASK_ID] [título] → Causa: [descripción]

### Recomendación:
[Qué asignar primero y por qué]
```

---

## Reglas críticas

- ❌ NUNCA asignar una tarea sin ASSIGNMENT subido en VTT
- ❌ NUNCA asignar si las dependencias no están en task_completed o task_approved
- ✅ Una tarea blocked solo se desbloquea cuando su dependencia llega a completed/approved
- ✅ Si hay tareas en task_in_review → hacer review ANTES de asignar nuevas
