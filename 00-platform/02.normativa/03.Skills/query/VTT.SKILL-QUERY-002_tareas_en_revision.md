# VTT.SKILL-QUERY-002 — Obtener tareas en revisión del proyecto

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-QUERY-002` |
| **Categoría** | QUERY (Consultas de lectura) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | TL Reviewer, PM, SA Reviewer |
| **Tokens estimados** | ~120 |
| **Cuándo se usa** | Rutina de apertura del TL/PM — listar pendientes de review para priorizar |
| **Reemplaza** | `SKL-QUERY-02_tareas-en-revision.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `project_id` | uuid | sí | UUID del proyecto donde buscar |
| `target_status` | enum | sí/no | Default: `task_in_review`. Otros: `task_completed` (PM ve los del TL aprobados), `task_on_hold` |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- El agente tiene rol con permisos para ver tareas del proyecto completo

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$PROJECT_ID                # UUID del proyecto (en el OPERATIVO del proyecto)
```

---

## Ejecución

### Opción A — Tareas en review del proyecto

```bash
curl -s "$VTT_BASE_URL/api/tasks?projectId=$PROJECT_ID&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

### Opción B — Tareas completadas pendientes de aprobación PM

```bash
curl -s "$VTT_BASE_URL/api/tasks?projectId=$PROJECT_ID&status=task_completed" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

### Opción C — Listado parseado con assignee + tiempo en review

```bash
curl -s "$VTT_BASE_URL/api/tasks?projectId=$PROJECT_ID&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
from datetime import datetime, timezone
tasks = json.load(sys.stdin).get('data', [])
now = datetime.now(timezone.utc)
print(f'=== TAREAS EN REVIEW ({len(tasks)}) ===\n')
for t in tasks:
    updated = t.get('updatedAt')
    if updated:
        u = datetime.fromisoformat(updated.replace('Z','+00:00'))
        hours = (now - u).total_seconds() / 3600
        print(f\"{t['id']} | {t.get('title')} | {t.get('assignedTo',{}).get('email','sin-asignar')} | {hours:.1f}h en review\")
    else:
        print(f\"{t['id']} | {t.get('title')}\")
"
```

---

## Validación

```bash
# Conteo de pendientes
curl -s "$VTT_BASE_URL/api/tasks?projectId=$PROJECT_ID&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
print('pendientes_review:', len(json.load(sys.stdin).get('data', [])))
"
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Lista vacía cuando esperaba tareas | `projectId` incorrecto | Verificar UUID del proyecto en el OPERATIVO |
| HTTP 403 | Token sin permisos sobre el proyecto | Confirmar rol del agente |
| Filtro status no aplica | Nombre de status equivocado | Usar `task_in_review` exacto (no `in_review` ni `review`) |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- Rutina de apertura del TL Reviewer
- `VTT.SKILL-TASK-005_review_tarea` — el TL primero lista pendientes, luego revisa una por una

---

## Cuándo NO usar esta Skill

- **Si querés ver tus tareas asignadas** (no las del proyecto) — usar `VTT.SKILL-QUERY-001`
- **Si querés ver tareas de OTRO proyecto** — pasar el `projectId` correcto, no asumir uno por default

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-QUERY-02_tareas-en-revision.md`. Ampliación: opción C con tiempo en review calculado (útil para priorizar tareas que llevan mucho tiempo esperando). Eliminado el `PROJECT_ID` hardcoded del legacy. |
