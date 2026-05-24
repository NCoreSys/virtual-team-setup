# VTT.SKILL-STATUS-002 — Mover tarea a `task_in_review`

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-STATUS-002` |
| **Categoría** | STATUS (Status transitions) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles ejecutores (BE, DB, FE, QA, DO, DL, UX, TL, AR, SA) |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Paso 12 del workflow del agente — al completar trabajo, antes de notificar al revisor |
| **Reemplaza** | `SKL-STATUS-02_task-in-review.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `agent_uuid` | uuid | sí | UUID del agente (= `changedBy`) |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en status `task_in_progress`
- **Antes de pasar a in_review**, el agente DEBE haber:
  - Subido devlog como attachment (`fileType=devlog`)
  - Subido code_logic por cada archivo modificado (`fileType=code_logic`)
  - Reportado todos los CAs con `PATCH /criteria/<id>`
  - Verificado `canProceedToReview=true` en el review gate
  - Creado PR en GitHub

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL
$AGENT_UUID
$STATUS_IN_REVIEW_UUID      # 1ec975a5-7581-4a1a-ab8f-51b1a7ef868d (fijo)
```

---

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"statusId\": \"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d\",
    \"changedBy\": \"$AGENT_UUID\"
  }"
```

> **Importante:** la generación del Task Manifest v1.0 (`WORKFLOW-MAN-001.003`) ocurre **DESPUÉS** de este paso, no antes. El status `task_in_review` es una de las 8 precondiciones del manifest.

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])"
# Esperado: task_in_review
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `INVALID_TRANSITION` | Tarea NO estaba en `task_in_progress` | Verificar status actual primero |
| HTTP 400 `REVIEW_GATE_BLOCKED` | `canProceedToReview=false` | Resolver entries pendientes del devlog antes |
| HTTP 403 | Agente no es el `assignedToId` | Confirmar asignación |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Cuándo NO usar esta Skill

- **Si faltan entregables** (devlog, code_logic, PR) — completar primero
- **Si el review gate bloquea** — el sistema rechazará; resolver entries pendientes

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-STATUS-02_task-in-review.md`. Contrato sin cambios. |
