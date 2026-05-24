# SKL-COMMENT-01: Agregar comentario en tarea

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-COMMENT-001_comentario_generico.md`** en `02.normativa/03.Skills/comment/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** VTT-COMMENT  
**Aplica a:** Todos  
**Tokens estimados:** ~75  
**Cuándo:** Feedback, notas, reportes en una tarea

## CRÍTICO

Campos son `message` + `userId`.  
**NUNCA** usar `content` + `authorId` — devuelve 400.

## Variables requeridas

- `$TOKEN`, `$TASK_ID`, `$AGENT_UUID`, `$VTT_BASE_URL`
- `$COMMENT_MESSAGE` — texto del comentario

## Ejecución

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"$COMMENT_MESSAGE\",
    \"userId\": \"$AGENT_UUID\"
  }"
```

## Validación

HTTP 201
