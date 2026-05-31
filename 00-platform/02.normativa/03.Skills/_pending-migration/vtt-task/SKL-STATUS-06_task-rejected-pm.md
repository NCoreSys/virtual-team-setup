# SKL-STATUS-06: Rechazar tarea (solo PM)

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-STATUS-006_task_rejected.md`** en `02.normativa/03.Skills/status/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** VTT-STATUS  
**Aplica a:** PM únicamente  
**Tokens estimados:** ~70  
**Cuándo:** Revisión funcional NO cumple criteria

## Precondición

OBLIGATORIO: Agregar comentario con feedback específico con SKL-COMMENT-01 ANTES de rechazar.

## Variables requeridas

- `$TOKEN` — JWT de sesión
- `$TASK_ID` — ID de tarea
- `$AGENT_UUID` — UUID del PM: `350831b2-e1ae-4dbe-b2eb-7e023ec2e103`
- `$VTT_BASE_URL=http://77.42.88.106:3000`

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"335fd9c6-f0d6-4966-a6ea-f518c78bc422\", \"changedBy\": \"$AGENT_UUID\"}"
```

## Validación

HTTP 200
