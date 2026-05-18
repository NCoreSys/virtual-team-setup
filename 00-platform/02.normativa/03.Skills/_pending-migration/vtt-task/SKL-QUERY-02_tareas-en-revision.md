# SKL-QUERY-02: Obtener tareas en revisión del proyecto

**Categoría:** VTT-QUERY  
**Aplica a:** TL, PM  
**Tokens estimados:** ~60  
**Cuándo:** Rutina de apertura para revisar pendientes de review

## Ejecución

```bash
curl -s "$VTT_BASE_URL/api/tasks?projectId=$PROJECT_ID&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Constante:** `$PROJECT_ID=d0fc276d-e764-4a83-96e9-d65f086ed803`
