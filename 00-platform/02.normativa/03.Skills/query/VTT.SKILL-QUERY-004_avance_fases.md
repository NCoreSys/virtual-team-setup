# VTT.SKILL-QUERY-004 — Avance por fases del proyecto

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-QUERY-004` |
| **Categoría** | QUERY (Consultas de lectura) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | PJM (reporte ejecutivo), TL, PM |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Reporte de avance al PM, apertura de sesión del PJM, cierre de sprint |
| **Reemplaza** | `SKL-QUERY-04_avance-fases.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `project_id` | uuid | sí | UUID del proyecto |
| `output_format` | enum | sí/no | `json` (default) / `table` / `markdown_report` |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$PROJECT_ID                # UUID del proyecto (del OPERATIVO)
```

---

## Ejecución

### Opción A — Raw JSON

```bash
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/phases" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

### Opción B — Tabla resumen con porcentajes

```bash
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/phases" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
phases = json.load(sys.stdin).get('data', [])
print(f'{'PHASE':<30} {'TOTAL':>6} {'DONE':>6} {'%':>6}')
print('-' * 50)
for p in phases:
    total = p.get('tasksCount', 0)
    done = p.get('completedTasksCount', 0)
    pct = (done / total * 100) if total > 0 else 0
    name = p.get('name','?')[:28]
    print(f'{name:<30} {total:>6} {done:>6} {pct:>5.1f}%')
"
```

### Opción C — Reporte markdown para PM

```bash
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/phases" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
from datetime import date
phases = json.load(sys.stdin).get('data', [])
print(f'# Avance del proyecto — {date.today().isoformat()}\n')
print('| Phase | Total | Done | In Review | In Progress | % |')
print('|---|---:|---:|---:|---:|---:|')
total_all = total_done = 0
for p in phases:
    t = p.get('tasksCount', 0)
    d = p.get('completedTasksCount', 0)
    ir = p.get('inReviewCount', 0)
    ip = p.get('inProgressCount', 0)
    pct = (d / t * 100) if t > 0 else 0
    name = p.get('name','?')
    print(f'| {name} | {t} | {d} | {ir} | {ip} | {pct:.1f}% |')
    total_all += t; total_done += d
total_pct = (total_done / total_all * 100) if total_all > 0 else 0
print(f'\n**Total del proyecto:** {total_done}/{total_all} ({total_pct:.1f}%)')
"
```

---

## Datos útiles del response

| Campo | Tipo | Para qué sirve |
|---|---|---|
| `tasksCount` | int | Total de tareas en la fase |
| `completedTasksCount` | int | Tareas en `task_completed` + `task_approved` |
| `inReviewCount` | int | Tareas pendientes de review TL/PM |
| `inProgressCount` | int | Tareas activas |
| `blockedCount` | int | Tareas en `task_blocked` o `task_on_hold` |
| `name` | string | Nombre humano de la fase |
| `order` | int | Orden de la fase en el SDLC |

> **Cálculo de %:** `completedTasksCount / tasksCount * 100`. NO incluir `inReviewCount` en el numerador — eso es work-in-progress.

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/phases" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
phases = json.load(sys.stdin).get('data', [])
print(f'fases: {len(phases)}')
"
# Esperado: >= 1 (típicamente 7-8 fases SDLC)
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 404 | `PROJECT_ID` incorrecto | Verificar UUID del proyecto en el OPERATIVO |
| Lista vacía | Proyecto sin fases creadas | Setup del proyecto incompleto — ver SETUP_PM |
| Campos `*Count` faltantes | Backend versión vieja | Actualizar VTT backend |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- Rutina de apertura del PJM
- Reportes ejecutivos del PM al cierre de sprint
- `VTT.WORKFLOW-MSG-XXX` (cuando se cree) — incluir avance en mensaje de PM al equipo

---

## Cuándo NO usar esta Skill

- **Si querés detalle por sprint** — esta da por **fase** (más granular que sprint pero distinto)
- **Si querés solo una fase específica** — usar `GET /api/phases/<phase_id>` directo

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-QUERY-04_avance-fases.md`. Ampliación: 3 opciones (raw / tabla / markdown report). Eliminado `PROJECT_ID` hardcoded del legacy. |
