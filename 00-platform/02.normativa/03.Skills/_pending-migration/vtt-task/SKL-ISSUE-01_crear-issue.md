# SKL-ISSUE-01: Crear issue/blocker en tarea

**Categoría:** VTT-ISSUE  
**Aplica a:** Todos  
**Tokens estimados:** ~90  
**Cuándo:** Cuando hay un blocker real — datos faltantes, dependencia rota, impedimento externo

## CRÍTICO

Crear un issue pone la tarea en `on_hold` automáticamente en VTT.  
Solo usar para blockers reales, no para notas o mejoras.

## Variables requeridas

- `$TOKEN`, `$TASK_ID`, `$VTT_BASE_URL`
- `$ISSUE_TITLE` — título del issue
- `$ISSUE_DESCRIPTION` — descripción detallada
- `$ISSUE_TYPE` — `blocker` | `requirement` | `improvement` | `bug`
- `$ISSUE_SEVERITY` — `low` | `medium` | `high` | `critical`

## Ejecución

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/issues" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"title\": \"$ISSUE_TITLE\",
    \"description\": \"$ISSUE_DESCRIPTION\",
    \"type\": \"$ISSUE_TYPE\",
    \"severity\": \"$ISSUE_SEVERITY\"
  }"
```

## Validación

HTTP 201. La tarea pasa automáticamente a `on_hold`.
