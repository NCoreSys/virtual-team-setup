# SKL-STATUS-01: Mover tarea a `task_in_progress`

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-STATUS-001_task_in_progress.md`** en `02.normativa/03.Skills/status/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** VTT-STATUS  
**Aplica a:** BE, DB, FE, QA, DO, DL, UX, TL, AR, SA  
**Tokens estimados:** ~70  
**Cuándo:** Paso 1 del workflow — al iniciar trabajo en una tarea

## Precondición

`$TOKEN` obtenido con SKL-AUTH-01

## Variables requeridas

- `$TOKEN` — JWT de sesión
- `$TASK_ID` — ID de tarea (ej: `MS-145`)
- `$AGENT_UUID` — UUID del agente
- `$VTT_BASE_URL=http://77.42.88.106:3000`

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"2a76888a-e595-4cfc-ac4c-a3ae5087ef56\", \"changedBy\": \"$AGENT_UUID\"}"
```

## Validación

HTTP 200, campo `status` en response = `task_in_progress`

## Error común

400 si `statusId` o `changedBy` son inválidos — verificar UUIDs.
