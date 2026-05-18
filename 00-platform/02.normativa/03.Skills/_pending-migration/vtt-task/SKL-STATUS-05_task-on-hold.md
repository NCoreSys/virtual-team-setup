# SKL-STATUS-05: Poner tarea en `task_on_hold`

**Categoría:** VTT-STATUS  
**Aplica a:** BE, DB, FE, QA, DO, DL, UX, TL, AR, SA  
**Tokens estimados:** ~95  
**Cuándo:** Cuando hay un blocker real que impide continuar

## CRÍTICO

Usar `PUT /on-hold` con header `x-user-id`.  
**NUNCA** usar `PATCH /status` con `statusId` de on_hold — endpoint diferente.

## Variables requeridas

- `$TOKEN` — JWT de sesión
- `$TASK_ID` — ID de tarea
- `$AGENT_UUID` — UUID del agente
- `$VTT_BASE_URL=http://77.42.88.106:3000`
- `$BLOCKER_TITLE` — Título corto (ej: "Falta schema de BD")
- `$BLOCKER_DESCRIPTION` — Descripción detallada del blocker

## Ejecución

```bash
curl -s -X PUT "$VTT_BASE_URL/api/tasks/$TASK_ID/on-hold" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-user-id: $AGENT_UUID" \
  -d "{
    \"type\": \"blocker\",
    \"title\": \"$BLOCKER_TITLE\",
    \"description\": \"$BLOCKER_DESCRIPTION\"
  }"
```

## Validación

HTTP 200

## Error común

Usar `PATCH /status` en vez de `PUT /on-hold` → tarea queda en estado incorrecto.
