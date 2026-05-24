# VTT.SKILL-GIT-006 — Crear PR con gh CLI

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-GIT-006` |
| **Categoría** | GIT |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles ejecutores (agente y TL) |
| **Tokens estimados** | ~250 |
| **Cuándo se usa** | Paso 11 del workflow del agente — inmediatamente después del commit + push. También usado por el TL en FASE 4.5 |
| **Reemplaza** | `SKL-GIT-04_crear-pr.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `branch_name` | string | sí | Branch a hacer PR (típicamente `feature/<TASK_ID>` o `tl/<TASK_ID>-close`) |
| `pr_title` | string | sí | Título del PR — formato `[<TASK_ID>] <descripción>` |
| `pr_description` | string | sí | Descripción técnica de cambios |
| `how_to_test` | string | sí | Pasos para que el reviewer pruebe |
| `task_slug` | string snake_case | sí/no | Para link al devlog |
| `base_branch` | string | sí/no | Default: `main` |

---

## Precondición

- `gh` CLI instalada y autenticada (`gh auth status` retorna logged in)
- La branch ya fue pusheada (`git push origin <branch>` ejecutado)
- Rebase con main ya hecho si han pasado >4h (`VTT.SKILL-GIT-004`)
- El working tree está limpio en el worktree

---

## Variables del entorno

Ninguna específica — solo gh CLI.

---

## Convención del título del PR

```
[<TASK_ID>] <descripción concisa de qué hace el PR>
```

### Ejemplos

| Tipo | Título |
|---|---|
| Tarea normal del agente | `[MS-293] Error handling con AppError + MEM-ERR-xxx` |
| Fix tras rechazo | `[MS-293] Fix: agregar tests faltantes del errorHandler` |
| PR del TL al cerrar review (FASE 4.5) | `[VTT-718] Manifest v1.5 + cierre review` |
| Hotfix con autorización PM | `[hotfix] Disable WebSocket reconnection loop` |

---

## Ejecución

### Opción A — PR del agente al cerrar tarea

```bash
cd <worktree_path>

# Asegurar que está pusheado
git push origin feature/<TASK_ID>

# Crear PR
gh pr create \
  --title "[<TASK_ID>] <PR_TITLE>" \
  --body "$(cat <<'EOF'
## Cambios

<PR_DESCRIPTION>

## Cómo probar

<HOW_TO_TEST>

## Referencias

- Ver devlog: knowledge/development-log/<YYYY-MM-DD>_<TASK_ID>_<TASK_SLUG>.md
- Tarea VTT: <TASK_ID>
- Manifest v1.0 commiteado en este PR (PROTOCOL-MAN-001 §5.3.7)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" \
  --base main
```

### Opción B — PR del TL en FASE 4.5 (cierre review)

```bash
cd <worktree_path_TL>     # ej. .vtt/worktrees/project-tl

git push origin tl/<TASK_ID>-close

gh pr create \
  --title "[<TASK_ID>] Manifest v1.5 + cierre review" \
  --body "$(cat <<'EOF'
## Cambios

Manifest v1.5 generado tras aprobar review de #<TASK_ID>.

- knowledge/task-manifests/.../<TASK_ID>.json — overwrite con v1.5
- knowledge/task-manifests/.../<TASK_ID>.manifest.md — overwrite con v1.5
- (otros archivos modificados por el TL durante el review)

## Referencias

- Ver attachment v1.5 en VTT: <ATTACHMENT_ID>
- Ver APR-TL comment: <APR_TL_COMMENT_ID>
- PROTOCOL-ASG-001 §5.5.bis FASE 4.5

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" \
  --base main
```

### Opción C — PR con dependencia (parent branch)

Si tu branch nació de `feature/<PARENT>` que aún NO mergeó:

```bash
# IMPORTANTE: el target SIGUE siendo main (no la parent branch)
gh pr create \
  --title "[<TASK_ID>] <PR_TITLE>" \
  --body "..." \
  --base main         # ← main, no feature/<PARENT>
```

Cuando la parent mergee, hacer rebase (`VTT.SKILL-GIT-004 Opción C`) y push de nuevo.

---

## Capturar URL del PR

```bash
PR_URL=$(gh pr view --json url --jq '.url')
PR_NUMBER=$(gh pr view --json number --jq '.number')

echo "PR_URL=$PR_URL"
echo "PR_NUMBER=$PR_NUMBER"
```

Estos valores se inyectan en:
- `delivery.git.pr_url` y `delivery.git.pr_number` del manifest v1.0
- El reporte SKL-REPORT-01 del agente
- El comment del agente al pasar a `task_in_review`

---

## Validación

```bash
# PR creado y accesible
gh pr view <PR_NUMBER> --json state,mergeable
# Esperado: state=OPEN, mergeable=MERGEABLE (no CONFLICTS)

# Listar PRs del agente para la tarea
gh pr list --head feature/<TASK_ID> --json number,title,state
# Esperado: 1 PR open
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| `pull request already exists` | PR ya creado para esa branch | OK — usar el existente (`gh pr view` para ver URL) |
| `no commits between main and feature/X` | Branch sin commits propios | Verificar `git log origin/main..HEAD` — debe tener tus commits |
| `gh: not authenticated` | gh CLI sin login | `gh auth login` con tu cuenta GitHub |
| Mergeable = CONFLICTS | Branch desfasada con main | Hacer rebase con `VTT.SKILL-GIT-004` y `git push --force-with-lease` |
| Title sin `[<TASK_ID>]` | Convención no respetada | Editar PR: `gh pr edit <NUM> --title "[<TASK_ID>] ..."` |
| PR target feature/<PARENT> | Confusión con dependencia | Cambiar base a `main`: `gh pr edit <NUM> --base main` |

---

## Skills invocadas

Ninguna — solo gh CLI.

---

## Skills que invocan ESTA

- Workflow del agente al cerrar tarea (Paso 11)
- `PROTOCOL-ASG-001 §5.5.bis.5` — PR del TL en FASE 4.5
- `VTT.WORKFLOW-WT-001.005 §5.5.4 Acción A` — PR para mergear branches pendientes al cierre del proyecto

---

## Cuándo NO usar esta Skill

- **Si la branch no está pusheada** — push primero
- **Si todavía estás en WIP** — esperar a tener commits finales
- **Si la base correcta no es main** (caso muy raro) — verificar con TL antes

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-GIT-04_crear-pr.md` con renumeración a `GIT-006`. Ampliación: 3 opciones (PR del agente / PR del TL FASE 4.5 / PR con dependencia parent). Captura explícita de PR_URL y PR_NUMBER para inyectar en manifest. Convención del título y referencia a Claude Code en el body. |
