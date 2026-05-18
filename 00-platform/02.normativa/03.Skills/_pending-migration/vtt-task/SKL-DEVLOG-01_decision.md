# SKL-DEVLOG-01: Registrar decisión en devlog VTT

**Categoría:** VTT-DEVLOG  
**Aplica a:** Todos  
**Tokens estimados:** ~90  
**Cuándo:** Para registrar decisiones técnicas o de producto importantes

## Variables requeridas

- `$TOKEN`, `$TASK_ID`, `$VTT_BASE_URL`
- `$DECISION_TITLE` — título corto de la decisión
- `$DECISION_DESCRIPTION` — qué se decidió y por qué
- `$IMPACT_DESCRIPTION` — qué áreas afecta

## Ejecución

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog-entries" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"type\": \"decision\",
    \"title\": \"$DECISION_TITLE\",
    \"description\": \"$DECISION_DESCRIPTION\",
    \"impact\": \"$IMPACT_DESCRIPTION\"
  }"
```

## Validación

HTTP 201
