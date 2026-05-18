# SKL-STATUS-04: Mover tarea a `task_approved` (solo PM)

**Categoría:** VTT-STATUS  
**Aplica a:** PM únicamente  
**Tokens estimados:** ~75  
**Cuándo:** Después de aprobación funcional (APR-PM)

## Precondición

OBLIGATORIO: Ejecutar SKL-COMMENT-02 (APR-PM) ANTES de esta skill.  
NUNCA aprobar sin haber leído los acceptance criteria de la tarea.

## Variables requeridas

- `$TOKEN` — JWT de sesión (SKL-AUTH-01)
- `$TASK_ID` — ID de tarea
- `$AGENT_UUID` — UUID del PM: `350831b2-e1ae-4dbe-b2eb-7e023ec2e103`
- `$VTT_BASE_URL=http://77.42.88.106:3000`

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"b9ca4951-6e14-4d82-b1d8-440793bbaf47\", \"changedBy\": \"$AGENT_UUID\"}"
```

## Validación

HTTP 200, campo `status` = `task_approved`
