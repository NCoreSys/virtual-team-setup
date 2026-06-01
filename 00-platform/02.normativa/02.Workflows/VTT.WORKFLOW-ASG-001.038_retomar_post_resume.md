# VTT.WORKFLOW-ASG-001.038 — Agente retoma tras auto-resume

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.038` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.4.7-8 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor cuando sistema VTT auto-resume tras resolución de Issue |
| **Reglas Nivel 0** | `RULE-AGENT-001`, `RULE-SCRIPT-001` |
| **CARD asociada** | `VTT.CARD-ISS-005` |

---

## 1. Propósito

Formalizar el retake del agente cuando sistema VTT auto-resume:
1. Detectar estado
2. Leer comment del TL
3. `git stash pop` del código pendiente
4. Retomar desde paso del `.034` donde se bloqueó

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `agent_id` | UUID | |
| `previous_blocking_issue_id` | UUID | Issue resuelto |

## 3. Precondiciones

- Issue previo en `resolved`/`wont_fix`/`pending_corrective`
- Tarea movida por VTT a `previousStatus` (`task_in_progress`)

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Leer comment del TL ANTES de retomar |
| R2 | `git stash pop` del stash del `.036` |
| R3 | Si `resume_strategy=wait_corrective` → NO retomar todavía |
| R4 | Ack al TL como comment |
| R5 | Retomar desde paso del `.034` donde se bloqueó (NO desde inicio) |
| R6 | Registrar devlog `resume_from_hold` |

## 5. Pasos

### Paso 1 — Detectar auto-resume
```bash
CURRENT=$(curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>" | python -c "...")
case "$CURRENT" in
  task_in_progress) ;;
  task_on_hold) echo "Esperar"; exit 0 ;;
  *) exit 1 ;;
esac
```

### Paso 2 — Leer comment del TL (R1)
```bash
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>/comments?limit=10&order=desc" | python -m json.tool
```

Buscar comment más reciente del TL con instrucciones.

### Paso 3 — Determinar `resume_strategy`
```bash
python $VTT_SETUP/02.normativa/04.Scripts/resume/SCRIPT-RESUME-001_resume_task.py \
  --task-id "$TASK_ID" \
  --previous-issue-id "$PREVIOUS_ISSUE_ID" \
  --agent-id "$AGENT_UUID" \
  --worktree-path "$WORKTREE_PATH"
```

Output:
- `continue` (Issue resolved/wont_fix) → retomar
- `wait_corrective` (Issue pending_corrective) → esperar correctiva aprobada

### Paso 4 — Si `wait_corrective` → esperar (R3)
NO retomar. Sistema VTT vuelve a disparar cuando correctiva aprobada.

### Paso 5 — Si `continue` → `git stash pop` (R2)
```bash
cd .vtt/worktrees/<repo>-<rol>
STASH=$(git stash list | grep "stash-<TASK_ID>-on-hold" | head -1 | cut -d: -f1)
[ -n "$STASH" ] && git stash pop "$STASH"
```

Si conflicto → resolver manualmente. NO descartar stash.

### Paso 6 — Aplicar instrucciones TL (R5)

| Opción del .037 | Acción del agente |
|---|---|
| B `resolve_inline` | Implementar fix indicado |
| C `accept_workaround` | Implementar workaround (NO fix completo) |
| D `reject_issue` | Continuar con ASSIGNMENT original |

### Paso 7 — Devlog `resume_from_hold` (R6)
```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/devlog-entries" \
  -d '{"entries":[{
    "categoryCode":"observation",
    "severity":"low",
    "title":"Resume from on_hold (ISS-<id> resolved)",
    "description":"...",
    "reportedBy":"<AGENT_UUID>",
    "status":"resolved",
    "resolution":"Tarea retomada exitosamente"
  }]}'
```

### Paso 8 — Ack al TL (R4)
```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/comments" \
  -d '{"comment":"✅ Retomada tras ISS-<id>.","authorId":"<AGENT_UUID>"}'
```

### Paso 9 — Retomar `WORKFLOW-ASG-001.034`
Desde el paso del `.034` donde se bloqueó (documentado en devlog blocker original del `.035`).

## 6. Outputs

| Output | Descripción |
|---|---|
| `previous_status` | `task_on_hold` |
| `new_status` | `task_in_progress` |
| `resume_strategy` | `continue`/`wait_corrective` |
| `stash_recovered` | bool |
| `step_resumed_from` | string |

## 7. Validación

Estado `task_in_progress` + código recuperado + ack enviado.

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Estado no cambió | onHoldIssueId mismatch | Verificar |
| Conflicto stash pop | Cambios en main | Resolver manualmente |
| Stash no encontrado | Nombre incorrecto | `git stash list` y buscar |
| Comment TL no encontrado | Filtro mal | Listar y buscar por authorId+timestamp |

## 9. Skills invocadas

- `SKILL-RESUME-001`, `SKILL-GIT-001`, `SKILL-COMMENT-001`, `SKILL-DEV-001`

## 10. Scripts invocados

- `SCRIPT-RESUME-001_resume_task.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Detección auto-resume + estrategia + stash pop + retake desde paso correcto. |
