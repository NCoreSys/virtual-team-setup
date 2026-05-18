# SKL-QUERY-03: Obtener detalle de una tarea

**Categoría:** VTT-QUERY  
**Aplica a:** Todos  
**Tokens estimados:** ~55  
**Cuándo:** Para leer acceptance criteria, devlog entries, attachments

## Ejecución

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```
