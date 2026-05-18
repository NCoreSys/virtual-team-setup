---
name: verificar-sprint
description: Consulta el estado actual del sprint en VTT — tareas por estado, bloqueantes, progreso por rol — y genera un reporte ejecutivo para el TL o PM.
role: TL, PM, PJM
vtt_version: "1.0"
---

# Skill: /verificar-sprint

## Propósito
Consulta VTT API para obtener el estado real del sprint actual.
Identifica tareas bloqueadas, en progreso, y el camino crítico.
Produce un reporte ejecutivo accionable.

## Cuándo usar
- Al inicio de cada sesión del TL/PM
- Antes de asignar nuevas tareas
- Cuando el PM quiere saber el avance general
- Equivale a la "Rutina de apertura" del OPERATIVO_TL y OPERATIVO_PM

## Pasos de ejecución

### 1. Obtener tareas del proyecto

```bash
# Todas las tareas del proyecto actual
curl -s -X GET "$API_URL/api/tasks?projectId=$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# O filtrar por estado
curl -s -X GET "$API_URL/api/tasks?projectId=$PROJECT_ID&status=task_in_progress" \
  -H "Authorization: Bearer $TOKEN" | jq '.[] | {id,title,assignee,status}'
```

### 2. Agrupar por estado

Organizar resultados en grupos:
- `task_in_progress` — ¿quién está trabajando en qué?
- `task_on_hold` — ¿qué está bloqueado y por qué?
- `task_in_review` — ¿qué está esperando revisión del TL?
- `pending` o `task_assigned` — ¿qué está listo para iniciar?
- `task_completed` — ¿qué se completó en este sprint?

### 3. Identificar bloqueantes

Para cada tarea en `task_on_hold`:
```bash
curl -s -X GET "$API_URL/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '{id,status,comment,dependencies}'
```

Registrar: ¿qué tarea bloquea a qué otra tarea?

### 4. Detectar camino crítico

Tareas que bloquean >2 tareas son críticas.
Si están on_hold o in_progress demasiado tiempo → escalar.

### 5. Calcular progreso

```
Progreso = task_completed / total_tareas_sprint * 100
```

### 6. Generar reporte

```markdown
## Estado del Sprint — [FECHA]
**Proyecto:** [PROYECTO_KEY] | **Sprint:** [N]

### Resumen
| Estado | Cantidad |
|--------|----------|
| Completadas | N |
| En progreso | N |
| En revisión | N |
| Bloqueadas   | N |
| Pendientes   | N |
| **Total**    | **N** |

**Progreso:** N% completado

### En progreso ahora
| Tarea | Rol | Desde |
|-------|-----|-------|
| MEM-BE-001 | BE | 2026-04-25 |

### Bloqueantes (acción requerida)
| Tarea | Bloqueada por | Acción |
|-------|--------------|--------|
| MEM-FE-003 | MEM-BE-001 | Esperar entrega BE |

### Para revisión TL
| Tarea | PR | Rol |
|-------|-----|-----|
| MEM-DB-001 | #14 | DB |

### Próximas a iniciar (desbloqueadas)
| Tarea | Rol asignado | Dependencias OK |
|-------|-------------|-----------------|
| MEM-BE-002 | BE | ✅ |
```

### 7. Acciones sugeridas

Basado en el reporte, sugerir:
- Tareas listas para asignar
- PRs que el TL debe revisar hoy
- Blockers que requieren intervención del PM/PJM
