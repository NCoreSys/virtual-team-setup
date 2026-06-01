# VTT.CARD-EXE-003 — Agente mueve tarea a `task_in_progress`

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-003` |
| **Tipo** | `CARD-mini` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution_start AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-EXE-002`, `CARD-MAN-004` |
| **Pertenece a** | WORKFLOW-ASG-001.033 |
| **Tokens estimados** | ~430 |

---

## Qué hacer

Transición `task_assigned`/`task_pending` → `task_in_progress`. **La hace el AGENTE**, no el TL.

```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-001_mover_in_progress.py \
  --task-id "$TASK_ID" \
  --agent-id "$AGENT_UUID" \
  --reason "Iniciando ejecución según ASSIGNMENT"
```

El script verifica:
- Estado actual = `task_assigned` o `task_pending`
- Si ya está en `task_in_progress` → idempotente, salta
- Si está en `on_hold`/`cancelled`/etc → falla, escalar al TL

Internamente ejecuta `PATCH /api/tasks/<TASK_ID>/status` con `statusId=2a76888a-e595-4cfc-ac4c-a3ae5087ef56` (UUID canónico de `task_in_progress`) + `changedBy=<AGENT_UUID>` (auditoría).

## Decisión por exit code

| Exit | Significado | Acción |
|---|---|---|
| 0 | OK (transición o skip si ya estaba) | Continuar con **CARD-EXE-004** |
| 3 | Estado inesperado (on_hold/cancelled/etc) | Escalar al TL |
| 4 | HTTP error | Verificar VTT health + reintentar (max 3) |
| 5 | RULE-SCRIPT-001 violation | Invocar desde path canónico `$VTT_SETUP/02.normativa/04.Scripts/` |
| 6 | Estado no persistió | Reintentar (max 3) o escalar |

## Output

Tarea en `task_in_progress`, auditoría con `changedBy = agent_id` registrada. Comienza ejecución del workflow del ASSIGNMENT (**CARD-EXE-004**).
