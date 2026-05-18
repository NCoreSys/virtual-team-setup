# SKL-STATUS-03: Mover tarea a `task_completed` (solo TL)

**Categoría:** VTT-STATUS  
**Aplica a:** TL únicamente  
**Tokens estimados:** ~75  
**Cuándo:** Después de aprobar revisión técnica

## Precondición

Ejecutar SKL-COMMENT-03 (APR-TL) ANTES de esta skill.

## Variables requeridas

- `$TOKEN` — JWT de sesión (SKL-AUTH-01)
- `$TASK_ID` — ID de tarea
- `$AGENT_UUID` — UUID del TL: `92225290-6b6b-4c1f-a940-dcb4262507aa`
- `$VTT_BASE_URL=http://77.42.88.106:3000`

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"aa5ceb90-5209-42a2-b874-a8cbee597a97\", \"changedBy\": \"$AGENT_UUID\"}"
```

## Validación

HTTP 200, campo `status` = `task_completed`

## Restricción

Solo TL puede ejecutar esta skill. El PM usa SKL-STATUS-04 para `task_approved`.
