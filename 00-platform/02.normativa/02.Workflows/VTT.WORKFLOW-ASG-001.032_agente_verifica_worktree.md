# VTT.WORKFLOW-ASG-001.032 — Agente verifica worktree del rol

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.032` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.2 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor — verificación obligatoria ANTES de tocar código |
| **Reglas Nivel 0** | `RULE-AGENT-001` (PROC-COORD-01), `RULE-GIT-004`, `RULE-SCRIPT-001` |
| **CARD asociada** | `VTT.CARD-EXE-002` |

---

## 1. Propósito

Garantizar que el agente trabaja en su **worktree dedicado de rol** (`.vtt/worktrees/<repo>-<rol>`), NO en clone base ni worktree ajeno. Evita pérdida de código por checkout cross-agente.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `agent_role` | enum | BE/DB/FE/DO/QA/DL/UX/AR/SA |
| `repo_name` | string | ej. `memory-service-project` |
| `expected_worktree_path` | path | `.vtt/worktrees/<repo>-<rol>` |

## 3. Precondiciones

- Worktree del rol existe (creado por TL via `SCRIPT-WT-002`)
- Workspace VSCode existe (opcional)
- `$VTT_SETUP` exportado

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Path del worktree depende del ROL, NO del TASK_ID |
| R2 | PROHIBIDO clone base — solo TL |
| R3 | PROHIBIDO worktree de otro rol — escalar al TL |
| R4 | PROHIBIDO clonar el repo de nuevo — escalar al TL para `SCRIPT-WT-002` |
| R5 | Branch base debe ser `main` actualizado (`git pull`) ANTES de feature branch |
| R6 | Working tree limpio antes de empezar (`git stash`, NO `reset --hard`) |

## 5. Pasos

### Paso 1 — Variables del entorno
```bash
[ -n "$VTT_SETUP" ] || exit 1
[ -n "$VTT_TOKEN" ] || exit 1
```

### Paso 2 — Verificar worktree del rol
```bash
WORKTREE_PATH=".vtt/worktrees/${REPO_NAME}-${AGENT_ROLE,,}"
[ -d "$WORKTREE_PATH" ] || { echo "Escalar al TL"; exit 2; }
```

### Paso 3 — Abrir workspace VSCode (opcional)
`code .vtt/workspaces/<repo>-<rol>.code-workspace`

### Paso 4 — Entrar al worktree
```bash
cd "$WORKTREE_PATH"
pwd  # confirmar
```

### Paso 5 — Verificar branch limpio
```bash
git status
# Esperado: On branch main, Working tree clean
```

Si sucio → `git stash push -m "stash-pre-<TASK_ID>"` (NO `reset --hard`).

### Paso 6 — Actualizar main
```bash
git checkout main && git pull origin main
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)
[ "$LOCAL" = "$REMOTE" ] || exit 4
```

### Paso 7 — Verificar no hay feature/<TASK_ID> previa
Si existe → consultar TL antes de borrar.

## 6. Outputs

| Output | Tipo | Descripción |
|---|---|---|
| `worktree_path_verified` | path | |
| `is_clone_base` | bool | false |
| `is_role_worktree` | bool | true |
| `main_up_to_date` | bool | true |
| `working_tree_clean` | bool | true |

## 7. Validación

```bash
[ "$is_role_worktree" = "true" ] && [ "$working_tree_clean" = "true" ]
```

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Worktree no existe | TL no ejecutó setup | Escalar TL (`SCRIPT-WT-002`) |
| En clone base por error | `cd` incorrecto | Volver al worktree del rol |
| Working tree sucio | Intento anterior | `git stash` |
| main desactualizado | Falta pull | `git pull origin main` |
| feature/<TASK_ID> ya existe | Intento anterior abortado | Consultar TL |

## 9. Skills invocadas

- `SKILL-WT-001`, `SKILL-GIT-001`

## 10. Scripts invocados

- `SCRIPT-WT-001_verify_worktree.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Formaliza PROTOCOL-ASG-001 §5.3.2 (PROC-COORD-01). |
