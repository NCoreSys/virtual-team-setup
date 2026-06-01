# VTT.WORKFLOW-ASG-001.036 — Agente solicita on_hold + transición

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.036` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.4.2 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor post `.035` |
| **Reglas Nivel 0** | `RULE-SCRIPT-001` |
| **CARD asociada** | `VTT.CARD-ISS-002` |

---

## 1. Propósito

Mover tarea a `task_on_hold` con `onHoldIssueId` enlazado. Habilita auto-resume del sistema VTT cuando el Issue se resuelve.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `agent_id` | UUID | |
| `issue_id` | UUID | del `.035` |
| `reason` | string | 1 línea |

## 3. Precondiciones

- Issue creado y en `status=open` (output del `.035`)
- Tarea en `task_in_progress`

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Endpoint dedicado `PUT /api/tasks/:id/on-hold` (NO `PATCH /status` — 405) |
| R2 | `onHoldIssueId` OBLIGATORIO — sin él no hay auto-resume |
| R3 | `reason` en 1 línea operativa — detalle en el Issue |
| R4 | Header `x-user-id` obligatorio |
| R5 | NOTIFICAR al TL como comment después de transición |
| R6 | NO commitear código pendiente — stash hasta resolución |

## 5. Pasos

### Paso 1 — Validar Issue creado
```bash
ISSUE_STATUS=$(curl -s "$VTT_BASE_URL/api/issues/<ISSUE_ID>" | python -c "...")
[ "$ISSUE_STATUS" = "open" ] || exit 1
```

### Paso 2 — Transición on_hold
```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-005_request_on_hold.py \
  --task-id "$TASK_ID" \
  --issue-id "$ISSUE_ID" \
  --user-id "$AGENT_UUID" \
  --reason "Bloqueado por <síntoma> — ver ISS-<ID>"
```

Internamente:
```
PUT /api/tasks/:id/on-hold
  Header: x-user-id: <AGENT_UUID>
  Body: { onHoldIssueId, reason, changedBy }
```

### Paso 3 — Validar persistencia
```bash
NEW_STATUS=$(curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>" | python -c "import sys,json; d=json.load(sys.stdin); print(d['status']['code'], d.get('onHoldIssueId',''))")
# Esperado: "task_on_hold <ISSUE_ID>"
```

### Paso 4 — Notificar al TL
```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/comments" \
  -d '{"comment":"🟠 Tarea en task_on_hold por bloqueante.\n- Issue: ISS-<ID>\n- Motivo: <reason>\n- TL: necesito análisis (.011).","authorId":"<AGENT_UUID>"}'
```

### Paso 5 — Stash código no commited (R6)
```bash
cd .vtt/worktrees/<repo>-<rol>
git status
# Si hay cambios:
git stash push -m "stash-<TASK_ID>-on-hold-pending-<issueId>"
```

NUNCA `git reset --hard`.

### Paso 6 — Esperar resolución del TL
Sistema VTT auto-resume cuando Issue → `resolved`/`wont_fix`.

## 6. Outputs

| Output | Descripción |
|---|---|
| `previous_status` | `task_in_progress` |
| `new_status` | `task_on_hold` |
| `on_hold_issue_id` | UUID |
| `notification_sent` | true |
| `code_stashed` | bool |

## 7. Validación

Estado persistió + onHoldIssueId enlazado + comment posted.

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| HTTP 405 | PATCH en vez de PUT | Usar PUT (R1) |
| HTTP 400 onHoldIssueId required | Falta campo | Incluir (R2) |
| HTTP 403 sin x-user-id | Header faltante | Agregar (R4) |
| Auto-resume no dispara | onHoldIssueId no persistió | Re-PUT |

## 9. Skills invocadas

- `SKILL-STATUS-005`, `SKILL-COMMENT-001`, `SKILL-GIT-001`

## 10. Scripts invocados

- `SCRIPT-STATUS-005_request_on_hold.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. PUT dedicado + onHoldIssueId obligatorio + x-user-id header + stash de código. |
