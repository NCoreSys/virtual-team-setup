# SKL-QUERY-03: Obtener detalle de una tarea

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-QUERY-003_detalle_tarea.md`** en `02.normativa/03.Skills/query/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** VTT-QUERY  
**Aplica a:** Todos  
**Tokens estimados:** ~55  
**Cuándo:** Para leer acceptance criteria, devlog entries, attachments

## Ejecución

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```
