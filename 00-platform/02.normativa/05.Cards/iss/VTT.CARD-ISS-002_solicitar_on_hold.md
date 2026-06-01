# VTT.CARD-ISS-002 — Agente solicita `task_on_hold`

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-ISS-002` |
| **Tipo** | `CARD-mini` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-ISS-001` |
| **Pertenece a** | WORKFLOW-ASG-001.036 |
| **Tokens estimados** | ~580 |

---

## Qué hacer

Después de crear Issue (CARD-ISS-001), mover la tarea a `task_on_hold` con `onHoldIssueId` enlazado.

```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-005_request_on_hold.py \
  --task-id "$TASK_ID" \
  --issue-id "$ISSUE_ID" \
  --user-id "$AGENT_UUID" \
  --reason "Bloqueado por <síntoma corto> — ver ISS-<ID>"
```

## Endpoint correcto

**`PUT /api/tasks/:id/on-hold`** (NO `PATCH /status` — devuelve 405).
**Header obligatorio:** `x-user-id: <AGENT_UUID>`.
**Body obligatorio:** `onHoldIssueId` — sin él, sistema VTT no puede auto-resume.

## Notificar al TL

Postear comment en la tarea:

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/comments" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{
    "comment": "🟠 Tarea en task_on_hold por bloqueante.\n- Issue: ISS-<ID>\n- Motivo: <reason>\n- TL: necesito análisis (CARD-ISS-003 / WORKFLOW-ASG-001.011).",
    "authorId": "<AGENT_UUID>"
  }'
```

## Stash del código no commiteado

```bash
cd .vtt/worktrees/<repo>-<rol>
git status
# Si hay cambios sin commit:
git stash push -m "stash-<TASK_ID>-on-hold-pending-<issueId>"
```

NUNCA `git reset --hard` sin consultar TL — puede perder trabajo.

## Auto-resume

Sistema VTT auto-resume la tarea cuando el Issue cambia a `resolved`/`wont_fix`. Por eso `onHoldIssueId` es **obligatorio**.

## Esperar

Quedás en espera del TL. Cuando auto-resume dispare → aplicar **CARD-ISS-005** (retomar).

## Si falla

| Síntoma | Acción |
|---|---|
| HTTP 405 | Usaste PATCH en vez de PUT — corregir |
| HTTP 400 onHoldIssueId required | Falta el campo en el body |
| HTTP 403 sin x-user-id | Agregar header `x-user-id` |
| Auto-resume no dispara cuando se resuelve | onHoldIssueId no se persistió — verificar y re-PUT |

## Output

Tarea en `task_on_hold` con `onHoldIssueId` enlazado + código stashed + TL notificado. Quedás esperando resolución del TL.
