# SKL-COMMENT-02: Comentario de aprobación APR-PM

**Categoría:** VTT-COMMENT  
**Aplica a:** PM únicamente  
**Tokens estimados:** ~85  
**Cuándo:** Al aprobar funcional — ejecutar ANTES de SKL-STATUS-04

## Precondición

Haber leído los acceptance criteria de la tarea (SKL-QUERY-03).

## Variables requeridas

- `$TOKEN`, `$TASK_ID`, `$VTT_BASE_URL`
- `$AGENT_UUID` — UUID del PM: `350831b2-e1ae-4dbe-b2eb-7e023ec2e103`
- `$AC_VERIFICADOS` — lista de acceptance criteria verificados
- `$NOTAS` — notas opcionales

## Ejecución

```bash
COMMENT_MESSAGE="APR-PM: tarea aprobada funcionalmente. Acceptance criteria verificados: $AC_VERIFICADOS. Notas: $NOTAS"

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\": \"$COMMENT_MESSAGE\", \"userId\": \"$AGENT_UUID\"}"
```

## Validación

HTTP 201. Luego ejecutar SKL-STATUS-04.
