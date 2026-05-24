# SKL-STATUS-02: Mover tarea a `task_in_review`

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-STATUS-002_task_in_review.md`** en `02.normativa/03.Skills/status/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** VTT-STATUS  
**Aplica a:** BE, DB, FE, QA, DO, DL, UX, TL, AR, SA  
**Tokens estimados:** ~70  
**Cuándo:** Paso 12 del workflow — al completar trabajo, antes de notificar al revisor

## Variables requeridas

- `$TOKEN` — JWT de sesión (SKL-AUTH-01)
- `$TASK_ID` — ID de tarea
- `$AGENT_UUID` — UUID del agente
- `$VTT_BASE_URL=http://77.42.88.106:3000`

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d\", \"changedBy\": \"$AGENT_UUID\"}"
```

## Validación

HTTP 200, campo `status` = `task_in_review`
