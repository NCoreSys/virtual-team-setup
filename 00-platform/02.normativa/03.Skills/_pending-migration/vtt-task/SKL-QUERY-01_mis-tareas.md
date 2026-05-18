# SKL-QUERY-01: Obtener mis tareas asignadas

**Categoría:** VTT-QUERY  
**Aplica a:** Todos  
**Tokens estimados:** ~60  
**Cuándo:** Rutina de apertura de sesión

## Ejecución

```bash
curl -s "$VTT_BASE_URL/api/tasks?assigneeId=$AGENT_UUID&status=task_assigned" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

## Validación

Lista de tareas con `status: task_assigned` para `$AGENT_UUID`
