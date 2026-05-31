# VTT.SKILL-STATUS-001 — Mover tarea a `task_in_progress`

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-STATUS-001` |
| **Categoría** | STATUS (Status transitions) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles ejecutores (BE, DB, FE, QA, DO, DL, UX, TL, AR, SA) |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Paso 1 del workflow del agente — al iniciar trabajo en una tarea (después de leer ASSIGNMENT + BRIEF + execution_manifest) |
| **Reemplaza** | `SKL-STATUS-01_task-in-progress.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `agent_uuid` | uuid | sí | UUID del agente que toma la tarea (= `changedBy`) |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- La tarea existe en VTT en status `task_pending`
- El agente leyó ASSIGNMENT + BRIEF + execution_manifest

---

## Variables del entorno

```bash
$TOKEN                      # JWT
$VTT_BASE_URL               # http://77.42.88.106:3000
$AGENT_UUID                 # UUID del agente
$STATUS_IN_PROGRESS_UUID    # 2a76888a-e595-4cfc-ac4c-a3ae5087ef56 (fijo)
```

---

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"statusId\": \"2a76888a-e595-4cfc-ac4c-a3ae5087ef56\",
    \"changedBy\": \"$AGENT_UUID\"
  }"
```

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])"
# Esperado: task_in_progress
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `INVALID_TRANSITION` | Tarea NO está en `task_pending` (ej. ya estaba en in_progress o in_review) | Verificar status actual antes de retry |
| HTTP 400 `INVALID_STATUS_ID` | `statusId` mal copiado | Usar exactamente `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| HTTP 403 | Agente no es el `assignedToId` de la tarea | Verificar asignación con `GET /tasks/<id>` |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Cuándo NO usar esta Skill

- **Si la tarea ya está en `task_in_progress`** — no-op silencioso, no llamar
- **Si la tarea está en `task_blocked` o `task_on_hold`** — primero resolver el bloqueo

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-STATUS-01_task-in-progress.md`. Contrato sin cambios. |
