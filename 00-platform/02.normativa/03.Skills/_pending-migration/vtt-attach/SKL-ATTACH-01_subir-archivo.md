# SKL-ATTACH-01: Subir archivo como attachment

**Categoría:** VTT-ATTACH  
**Aplica a:** Todos  
**Tokens estimados:** ~85  
**Cuándo:** Al subir cualquier archivo a una tarea VTT

## CRÍTICO

`uploadedById` es OBLIGATORIO. Sin él la API devuelve 400.

## Variables requeridas

- `$TOKEN`, `$TASK_ID`, `$AGENT_UUID`, `$VTT_BASE_URL`
- `$FILE_PATH` — ruta local al archivo (ej: `knowledge/development-log/2026-05-01_MS-145_setup.md`)
- `$FILE_TYPE` — `brief` | `devlog` | `code_logic` | `spec` | `assignment`

## Ejecución

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$FILE_PATH" \
  -F "fileType=$FILE_TYPE" \
  -F "uploadedById=$AGENT_UUID"
```

## Validación

HTTP 201, response incluye `id` del attachment
