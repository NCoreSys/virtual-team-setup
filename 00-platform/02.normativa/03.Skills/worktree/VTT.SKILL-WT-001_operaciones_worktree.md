# VTT.SKILL-WT-001 — Operaciones de Worktree

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-WT-001` |
| **Categoría** | WT (Worktree) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-18 |
| **Aplica a** | Coordinador (setup), TL (add/remove/cleanup), Agentes (verify_status) |
| **Tokens estimados** | ~600 |
| **Cuándo se usa** | Cualquier operación sobre worktrees del proyecto: crear, listar, verificar, remover, archivar/cerrar branches |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `action` | enum | sí | Una de: `add_worktree`, `remove_worktree`, `list_worktrees`, `verify_worktree_status`, `close_branch_wontfix`, `archive_branch_for_phase2` |
| `project_root` | path absoluto | sí | Raíz del proyecto |
| `repo_full_name` | string | depende | Nombre del repo (ej. `memory-service-backend`) — req para `add_worktree`, `remove_worktree` |
| `repo` | string | depende | Nombre corto del repo (ej. `backend`) — req para `add_worktree` |
| `rol` | string | depende | Rol lowercase (ej. `be`) — req para `add_worktree`, `verify_worktree_status` |
| `worktree_path` | path | depende | Ej. `.vtt/worktrees/backend-be/` — req para `remove_worktree`, `verify_worktree_status` |
| `branch_idle` | string | opcional | Default: `wt-<repo>-<rol>` — para `add_worktree` |
| `branch_name` | string | depende | Para `close_branch_wontfix`, `archive_branch_for_phase2` |
| `task_id` | string | depende | Para `close_branch_wontfix`, `archive_branch_for_phase2` |
| `motivo` | string | depende | Para `close_branch_wontfix`, `archive_branch_for_phase2` |

---

## Precondición

- Git instalado (`git --version` retorna)
- `project_root` existe
- Para acciones que tocan VTT: JWT válido (`SKL-AUTH-01`)
- Para `gh pr ...`: GitHub CLI configurada (`gh auth status` OK)

---

## Variables del entorno

```bash
$TOKEN              # JWT para operaciones VTT (close_branch_wontfix, etc.)
$VTT_BASE_URL       # http://77.42.88.106:3000
```

---

## Acciones

### action=add_worktree

Crea un git worktree con su branch idle.

```bash
REPO_DIR="$PROJECT_ROOT/$REPO_FULL_NAME"
WT_PATH="$PROJECT_ROOT/.vtt/worktrees/$REPO-$ROL"
BRANCH_IDLE="${BRANCH_IDLE:-wt-$REPO-$ROL}"

# Idempotente: skip si ya existe
if [ -d "$WT_PATH" ]; then
    echo '{"success": true, "skipped": true, "reason": "worktree ya existe"}'
    exit 0
fi

cd "$REPO_DIR"
git fetch origin

if git rev-parse --verify "$BRANCH_IDLE" >/dev/null 2>&1; then
    git worktree add "$WT_PATH" "$BRANCH_IDLE"
else
    git worktree add "$WT_PATH" -b "$BRANCH_IDLE" origin/main
fi
```

Output: `{"success": true, "worktree_path": "...", "branch_idle": "..."}`

### action=remove_worktree

Remueve un worktree y opcionalmente borra su branch idle.

```bash
cd "$PROJECT_ROOT/$REPO_FULL_NAME"
git worktree remove "$WORKTREE_PATH"
# Opcional: --force si tiene cambios
# git worktree remove --force "$WORKTREE_PATH"

# Opcional: borrar branch idle
git branch -D "wt-$REPO-$ROL" 2>/dev/null || true
```

Output: `{"success": true, "removed": "..."}`

### action=list_worktrees

Lista los worktrees activos en formato estructurado.

```bash
cd "$PROJECT_ROOT/$REPO_FULL_NAME"
git worktree list --porcelain | python -c "
import sys, json
data = sys.stdin.read().split('\n\n')
result = []
for block in data:
    if not block.strip():
        continue
    wt = {}
    for line in block.split('\n'):
        if line.startswith('worktree '):
            wt['path'] = line[9:]
        elif line.startswith('HEAD '):
            wt['head'] = line[5:]
        elif line.startswith('branch '):
            wt['branch'] = line[7:]
        elif line == 'bare':
            wt['bare'] = True
    result.append(wt)
print(json.dumps(result, indent=2))
"
```

Output: array JSON de objetos `{path, head, branch}`.

### action=verify_worktree_status

Para agente — verifica estado del worktree y devuelve qué caso aplica (A/B/C según §5.2.4.bis del Protocol).

```bash
cd "$WORKTREE_PATH"
BRANCH=$(git branch --show-current)
STATUS_LINES=$(git status --porcelain | wc -l)
EXPECTED_IDLE="wt-$REPO-$ROL"

if [ "$BRANCH" = "$EXPECTED_IDLE" ] && [ "$STATUS_LINES" -eq 0 ]; then
    echo '{"case": "A", "branch": "'$BRANCH'", "dirty": false, "action": "ready"}'
elif [[ "$BRANCH" == feature/* ]] || [[ "$BRANCH" == fix/* ]]; then
    # Verificar si la branch está mergeada
    git fetch origin --quiet
    if git branch --merged origin/main | grep -q "^  $BRANCH$"; then
        echo '{"case": "B", "branch": "'$BRANCH'", "merged": true, "action": "cleanup_retroactive"}'
    else
        echo '{"case": "C", "branch": "'$BRANCH'", "merged": false, "dirty": '$([ "$STATUS_LINES" -gt 0 ] && echo true || echo false)', "action": "task_in_progress"}'
    fi
else
    echo '{"case": "unknown", "branch": "'$BRANCH'", "action": "escalate_to_tl"}'
fi
```

Output: `{case, branch, action, ...}`.

### action=close_branch_wontfix

Cierra una branch sin mergear (Acción B de §5.5.4 del Protocol).

```bash
# 1. Postear comment en VTT
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Branch $BRANCH_NAME cerrada wontfix al final del proyecto. Motivo: $MOTIVO\", \"type\": \"wontfix\"}"

# 2. Cerrar PR si existe
PR_NUM=$(gh pr list --head "$BRANCH_NAME" --json number --jq '.[0].number')
if [ -n "$PR_NUM" ]; then
    gh pr close "$PR_NUM" --comment "Project closure — wontfix per TL decision: $MOTIVO"
fi

# 3. Borrar branch en remote
cd "$PROJECT_ROOT/$REPO_FULL_NAME"
git push origin --delete "$BRANCH_NAME" 2>/dev/null || echo "Branch ya no en remote"
git branch -D "$BRANCH_NAME" 2>/dev/null || echo "Branch ya no en local"
```

Output: `{"success": true, "task_id": "...", "pr_closed": <num o null>}`

### action=archive_branch_for_phase2

Preserva una branch para fase 2 (Acción C de §5.5.4).

```bash
ARCHIVE_FILE="$PROJECT_ROOT/_archive/branches_pending_phase2.md"

mkdir -p "$(dirname "$ARCHIVE_FILE")"

# Generar archivo si no existe (con header)
if [ ! -f "$ARCHIVE_FILE" ]; then
    cat > "$ARCHIVE_FILE" <<EOF
# Branches preservadas para Fase 2 — $PROYECTO

Fecha de cierre: $(date +%Y-%m-%d)
TL responsable: $TL_NAME

## Branches

EOF
fi

# Agregar entrada
echo "- \`$BRANCH_NAME\` | task=$TASK_ID | task_status=$TASK_STATUS | motivo=$MOTIVO" >> "$ARCHIVE_FILE"
```

Output: `{"success": true, "archived_in": "_archive/branches_pending_phase2.md"}`

NO se borra la branch — queda viva para que fase 2 la retome.

---

## Validación post-ejecución

```bash
# add_worktree
git worktree list | grep "$WT_PATH"
# Esperado: línea presente

# remove_worktree
git worktree list | grep "$WT_PATH"
# Esperado: NO match (worktree removido)

# close_branch_wontfix
git branch -a | grep "$BRANCH_NAME"
# Esperado: NO match

# archive_branch_for_phase2
grep "$BRANCH_NAME" "$ARCHIVE_FILE"
# Esperado: línea presente
```

---

## Error común

| Error | Causa probable | Solución |
|---|---|---|
| `fatal: '<path>' is already checked out` | Branch idle ya en uso | Detectar antes con `git worktree list` y skip |
| `fatal: '<path>' is missing` | Worktree fue borrado manualmente | `git worktree prune` antes de retry |
| `fatal: 'wt-X' is locked` | Lock file de operación anterior | `rm <repo>/.git/worktrees/<wt>/locked` |
| `gh pr close: PR not found` | Branch nunca tuvo PR | OK — saltear el `gh pr close` |
| `git push origin --delete: ref does not exist` | Branch nunca fue pusheada | OK — solo cleanup local |
| `_archive/` no se puede crear | Permission denied | Verificar permisos en `$PROJECT_ROOT` |

---

## Scripts invocados

- `VTT.SCRIPT-WT-001` (`setup_worktrees.py`) — usa `add_worktree` en bulk
- `VTT.SCRIPT-WT-002` (`add_worktree.py`) — wrapper directo de `add_worktree`
- `VTT.SCRIPT-WT-003` (`cleanup_worktrees.py`) — usa `remove_worktree` + `close_branch_wontfix` + `archive_branch_for_phase2` en bulk

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-18 | Versión inicial. 6 acciones cubren los Workflows .001 a .005 del Protocol. |
