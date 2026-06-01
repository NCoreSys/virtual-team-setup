# VTT.CARD-EXE-002 — Agente verifica worktree del rol

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-002` |
| **Tipo** | `CARD-mini` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution_start AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-EXE-001` |
| **Pertenece a** | WORKFLOW-ASG-001.032 |
| **Tokens estimados** | ~580 |

---

## Qué hacer

Verificar que estás en el worktree dedicado de tu rol (PROC-COORD-01 / RULE-AGENT-001):

```bash
WORKTREE_PATH=".vtt/worktrees/<repo>-<rol_minuscula>"

# 1. Worktree existe
[ -d "$WORKTREE_PATH" ] || { echo "Worktree no existe — escalar al TL"; exit 2; }

# 2. cd al worktree (NO al clone base)
cd "$WORKTREE_PATH"
pwd  # confirmar path contiene .vtt/worktrees/<repo>-<rol>

# 3. main limpio y actualizado
git status                              # debe estar limpio
git checkout main && git pull origin main

# 4. Verificar no hay feature/<TASK_ID> previa
git rev-parse --verify "feature/<TASK_ID>" 2>/dev/null && {
  echo "WARN: branch existe (intento anterior) — consultar TL antes de borrar"
}
```

## Prohibido

- ❌ Trabajar en clone base (`git/<repo>/`) — solo el TL
- ❌ Trabajar en worktree de otro rol — escalar coordinación al TL
- ❌ Clonar el repo de nuevo — si falta worktree, escalar al TL (`SCRIPT-WT-002_create_worktree.py`)
- ❌ `git reset --hard` para "limpiar" — usa `git stash` y consulta TL

## Si working tree sucio

```bash
git stash push -m "stash-pre-<TASK_ID>"  # preserva trabajo previo
```

## Si falla

| Síntoma | Acción |
|---|---|
| Worktree no existe | Escalar TL (necesita `SCRIPT-WT-002`) |
| En clone base por error | `cd` al worktree correcto |
| Working tree sucio | `git stash` (NO `reset --hard`) |
| main local desactualizado | `git pull origin main` |
| Branch feature/<TASK_ID> existe (intento previo) | Consultar TL antes de borrar — puede tener trabajo no commited |

## Output

Listo en worktree correcto + branch main actualizada + working tree limpio. Próximo: **CARD-MAN-004** (leer execution_manifest), luego **CARD-EXE-003**.
