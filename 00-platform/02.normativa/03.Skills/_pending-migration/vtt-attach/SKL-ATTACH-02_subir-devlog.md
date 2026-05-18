# SKL-ATTACH-02: Subir devlog de tarea

**Categoría:** VTT-ATTACH  
**Aplica a:** BE, DB, FE, QA, DO, DL, UX, AR, SA  
**Tokens estimados:** ~90  
**Cuándo:** Paso 11 del workflow — al completar tarea

## Variables requeridas

- `$TOKEN`, `$TASK_ID`, `$AGENT_UUID`, `$VTT_BASE_URL`
- `$TASK_SLUG` — nombre corto descriptivo (ej: `setup-express`, `schema-usuarios`)

## Ejecución

```bash
DEVLOG_PATH="knowledge/development-log/$(date +%Y-%m-%d)_${TASK_ID}_${TASK_SLUG}.md"

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$DEVLOG_PATH" \
  -F "fileType=devlog" \
  -F "uploadedById=$AGENT_UUID"
```

## Validación

HTTP 201. Verificar que el archivo existe localmente antes de ejecutar.
