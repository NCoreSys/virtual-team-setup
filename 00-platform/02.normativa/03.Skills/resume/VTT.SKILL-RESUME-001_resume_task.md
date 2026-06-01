# VTT.SKILL-RESUME-001 — Retomar tarea tras auto-resume

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-RESUME-001` |
| **Categoría** | RESUME (Resume Lifecycle) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor cuando sistema VTT auto-resume tras resolución Issue |
| **Tokens estimados** | ~130 |
| **Cuándo se usa** | `WORKFLOW-ASG-001.038` / `CARD-ISS-005` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string | sí | |
| `previous_issue_id` | UUID | sí | Issue resuelto |
| `agent_id` | UUID | sí | |
| `worktree_path` | path | opcional | para buscar stash |

## Precondición

- Issue previo en `resolved`/`wont_fix`/`pending_corrective`
- Tarea movida por VTT a `previousStatus` (`task_in_progress`)

## Variables del entorno

- `$VTT_TOKEN`, `$VTT_BASE_URL`, `$VTT_SETUP`

## Reglas

- R1 Leer comment del TL ANTES de retomar
- R2 `git stash pop` del stash del `.036`
- R3 `wait_corrective` → NO retomar (esperar correctiva aprobada)
- R4 Ack al TL como comment
- R5 Retomar desde paso del `.034` donde se bloqueó (NO desde inicio)
- R6 Registrar devlog `resume_from_hold`

## Ejecución

```bash
python $VTT_SETUP/02.normativa/04.Scripts/resume/SCRIPT-RESUME-001_resume_task.py \
  --task-id "$TASK_ID" \
  --previous-issue-id "$PREVIOUS_ISSUE_ID" \
  --agent-id "$AGENT_UUID" \
  --worktree-path "$WORKTREE_PATH"
```

Script:
1. Detecta estado tarea
2. Determina `resume_strategy` según Issue status
3. Si `continue` → busca stash, prepara `git stash pop`
4. Sugiere paso del `.034` para retomar

## Validación

- Estado `task_in_progress` detectado
- `resume_strategy` ∈ {`continue`, `wait_corrective`}

## Error común

- Auto-resume no disparó → verificar `task.onHoldIssueId`
- Conflicto stash pop → resolver manualmente (no descartar)
- Stash no encontrado → `git stash list` y buscar

## Scripts invocados

- `SCRIPT-RESUME-001_resume_task.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. Detección estrategia + stash pop + retake. |
