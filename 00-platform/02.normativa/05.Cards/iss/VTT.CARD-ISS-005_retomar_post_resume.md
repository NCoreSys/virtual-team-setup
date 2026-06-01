# VTT.CARD-ISS-005 — Agente retoma tarea tras auto-resume

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-ISS-005` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | ninguna (entry-point al detectar auto-resume) |
| **Pertenece a** | WORKFLOW-ASG-001.038 |
| **Tokens estimados** | ~900 |

---

## Cuándo aplica

Cuando el sistema VTT auto-resume tu tarea: `task.status` pasó de `task_on_hold` a `task_in_progress`. Lo detectás por notificación VTT o polling.

## Paso 1 — Detectar estrategia

```bash
python $VTT_SETUP/02.normativa/04.Scripts/resume/SCRIPT-RESUME-001_resume_task.py \
  --task-id "$TASK_ID" \
  --previous-issue-id "$PREVIOUS_ISSUE_ID" \
  --agent-id "$AGENT_UUID" \
  --worktree-path "$WORKTREE_PATH"
```

Output `resume_strategy`:
- **`continue`** — Issue cerrado (resolved/wont_fix) → retomar
- **`wait_corrective`** — tarea correctiva pendiente (Opción A del TL) → esperar (NO retomar todavía)

## Paso 2 — Si `wait_corrective` → esperar

NO retomar. El sistema VTT vuelve a disparar auto-resume cuando la correctiva alcanza `task_approved`. Quedate esperando.

## Paso 3 — Si `continue`:

### 3.a — Leer comment del TL

```bash
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>/comments?limit=10&order=desc" \
  -H "Authorization: Bearer $VTT_TOKEN" | python -m json.tool
```

Buscar comment más reciente del TL con instrucciones (timestamp posterior al `acknowledged` del Issue + `authorId` del TL).

### 3.b — `git stash pop`

```bash
cd .vtt/worktrees/<repo>-<rol>
STASH=$(git stash list | grep "stash-<TASK_ID>-on-hold" | head -1 | cut -d: -f1)
[ -n "$STASH" ] && git stash pop "$STASH"
```

Si hay conflicto al pop → resolver manualmente. **NO descartar stash** sin confirmar con TL.

### 3.c — Aplicar instrucciones del TL según opción

| Opción del .037 | Acción del agente |
|---|---|
| B `resolve_inline` | Implementar el fix indicado en el comment |
| C `accept_workaround` | Implementar workaround (NO el fix completo — eso es del TI) |
| D `reject_issue` | Continuar con ASSIGNMENT original |

### 3.d — Devlog `resume_from_hold`

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/devlog-entries" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{"entries":[{
    "categoryCode":"observation",
    "severity":"low",
    "title":"Resume from on_hold (ISS-<id> resolved)",
    "description":"Issue previo: ISS-<id> (<status>)\nEstrategia: continue\nPaso del .034 donde se bloqueó: <paso>\nPaso donde retoma: <paso>\nStash recuperado: <yes/no>\nInstrucciones TL: <breve>",
    "reportedBy":"<AGENT_UUID>",
    "status":"resolved",
    "resolution":"Tarea retomada exitosamente"
  }]}'
```

### 3.e — Ack al TL

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/comments" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{
    "comment": "✅ Retomada tras ISS-<id>.\nEstrategia: continue\nPaso retomado: <X>\nStash recuperado: <yes/no>",
    "authorId": "<AGENT_UUID>"
  }'
```

## Paso 4 — Retomar **CARD-EXE-004** desde paso correcto

NO desde el inicio. Desde el paso del `.034` donde te bloqueaste (lo dice el devlog `blocker` original creado en CARD-ISS-001).

## Si falla

| Síntoma | Acción |
|---|---|
| Estado no cambió a `task_in_progress` | Verificar `task.onHoldIssueId` apuntaba al Issue resuelto |
| Conflicto en `git stash pop` | Resolver manualmente (NO descartar) |
| Stash no encontrado | `git stash list` y buscar por TASK_ID |
| Comment del TL no aparece | Listar todos los comments y buscar por `authorId` + timestamp |

## Output

Tarea en `task_in_progress`, código recuperado, instrucciones del TL aplicadas, ack enviado. **Continúa con CARD-EXE-004 desde el paso donde se bloqueó.**
