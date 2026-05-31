# SKL-REPORT-02: Reporte ejecutivo PJM al PM

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-REPORT-002_reporte_pjm.md`** en `02.normativa/03.Skills/report/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** REPORT  
**Aplica a:** PJM  
**Tokens estimados:** ~115  
**Cuándo:** Diario o al cierre de sprint

## Precondición

Ejecutar SKL-QUERY-04 para obtener datos de avance por fase.

## Template de reporte

```markdown
## Reporte Ejecutivo PJM — $FECHA

### % Avance por Fase:
| Fase | Total | Completadas | % |
|------|-------|-------------|---|
| Setup | X | Y | Z% |
| S01 | X | Y | Z% |
| S02 | X | Y | Z% |

### Blockers activos: $NUM_BLOCKERS
$LISTA_BLOCKERS (task_on_hold + owner + tiempo en hold)

### En revisión >48h sin TL: $NUM_PENDIENTES
$LISTA_PENDIENTES

### Próxima oleada a asignar:
$TAREAS_PROXIMAS (max 3 — regla LL-001: una tarea a la vez por agente)

### Recomendación:
$RECOMENDACION
```

## Uso

Enviar al PM vía comentario en tarea de coordinación o mensaje directo.
