# VTT.WORKFLOW-ASG-001.033 — Agente mueve tarea a `task_in_progress`

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.033` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.3 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor |
| **Reglas Nivel 0** | `RULE-SCRIPT-001` |
| **CARD asociada** | `VTT.CARD-EXE-003` |

---

## 1. Propósito

Formalizar la transición `task_assigned`/`task_pending` → `task_in_progress` ejecutada por el AGENTE (no el TL). Marca el inicio formal de ejecución para auditoría + métricas + devlogs asociados al estado.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `agent_id` | UUID | UUID del agente |
| `reason` | string | opcional |

## 3. Precondiciones

- `.031` `.032` `.022` completados
- Branch `feature/<TASK_ID>` creada
- Tarea en `task_assigned` o `task_pending`

## 4. Reglas

| # | Regla |
|---|---|
| R1 | La transición la ejecuta el AGENTE, NO el TL |
| R2 | `statusId` canónico: `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| R3 | `changedBy = agent_id` para auditoría |
| R5 | Si tarea NO en `task_assigned`/`task_pending` → escalar al TL |

## 5. Pasos

### Paso 1 — Verificar estado actual
```bash
CURRENT=$(curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  | python -c "import sys,json; print(json.load(sys.stdin)['status']['code'])")

case "$CURRENT" in
  task_assigned|task_pending) ;;
  task_in_progress) exit 0 ;;  # idempotente
  *) exit 1 ;;
esac
```

### Paso 2 — Ejecutar transición
```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-001_mover_in_progress.py \
  --task-id "$TASK_ID" \
  --agent-id "$AGENT_UUID" \
  --reason "Iniciando ejecución según ASSIGNMENT"
```

### Paso 3 — Validar persistencia
```bash
NEW=$(curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>" | python -c "..." )
[ "$NEW" = "task_in_progress" ] || exit 3
```

## 6. Outputs

| Output | Descripción |
|---|---|
| `previous_status` | `task_assigned`/`task_pending` |
| `new_status` | `task_in_progress` |
| `changed_by` | `<AGENT_UUID>` |

## 7. Validación

HTTP 200 + `status.code = "task_in_progress"` + auditoría `task_status_history` con `changedBy = <AGENT_UUID>`.

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| HTTP 403 | Token expirado | Re-login `SKILL-AUTH-001` |
| HTTP 400 invalid statusId | UUID mal | Usar canónico R2 |
| Tarea en on_hold | Bloqueada | Escalar al TL |

## 9. Skills invocadas

- `SKILL-STATUS-001`

## 10. Scripts invocados

- `SCRIPT-STATUS-001_mover_in_progress.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Transición ejecutada por agente. |
