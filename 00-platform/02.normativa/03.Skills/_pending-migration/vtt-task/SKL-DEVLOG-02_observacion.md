# SKL-DEVLOG-02: Registrar observación en devlog VTT

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-DEV-002_observacion.md`** en `02.normativa/03.Skills/dev/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** VTT-DEVLOG  
**Aplica a:** Todos  
**Tokens estimados:** ~85  
**Cuándo:** Para registrar observaciones, hallazgos, notas técnicas

## Variables requeridas

- `$TOKEN`, `$TASK_ID`, `$VTT_BASE_URL`
- `$OBS_TITLE` — título
- `$OBS_DESCRIPTION` — descripción de la observación

## Ejecución

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog-entries" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"type\": \"observation\",
    \"title\": \"$OBS_TITLE\",
    \"description\": \"$OBS_DESCRIPTION\"
  }"
```

## Validación

HTTP 201
