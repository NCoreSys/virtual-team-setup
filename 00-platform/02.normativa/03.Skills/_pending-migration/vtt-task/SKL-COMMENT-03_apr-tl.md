# SKL-COMMENT-03: Comentario de aprobación APR-TL

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-COMMENT-003_apr_tl.md`** en `02.normativa/03.Skills/comment/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** VTT-COMMENT  
**Aplica a:** TL únicamente  
**Tokens estimados:** ~85  
**Cuándo:** Al aprobar técnicamente — ejecutar ANTES de SKL-STATUS-03

## Variables requeridas

- `$TOKEN`, `$TASK_ID`, `$VTT_BASE_URL`
- `$AGENT_UUID` — UUID del TL: `92225290-6b6b-4c1f-a940-dcb4262507aa`
- `$NOTAS` — notas de revisión técnica

## Ejecución

```bash
COMMENT_MESSAGE="APR-TL: revisión técnica aprobada. Code quality OK. Tests OK. Notas: $NOTAS"

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\": \"$COMMENT_MESSAGE\", \"userId\": \"$AGENT_UUID\"}"
```

## Validación

HTTP 201. Luego ejecutar SKL-STATUS-03.
