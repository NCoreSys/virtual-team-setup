# VTT.SKILL-GIT-004 — Rebase con main antes de PR

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-GIT-004` |
| **Categoría** | GIT |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles ejecutores |
| **Tokens estimados** | ~200 |
| **Cuándo se usa** | Antes de crear PR — obligatorio si han pasado más de 4 horas desde crear el branch o si main divergió |
| **Reemplaza** | `SKL-GIT-02_rebase-main.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `worktree_path` | path | sí (si WT) | Worktree del rol |
| `branch_name` | string | sí | Branch a rebasar (típicamente `feature/<TASK_ID>`) |
| `base_branch` | string | sí/no | Default: `main` |

---

## Precondición

- Estás en el worktree del agente (`VTT.WORKFLOW-WT-001.002`)
- Tu branch local tiene commits (al menos 1)
- `git status` muestra working tree limpio (commitear cambios pendientes antes)

---

## Variables del entorno

Ninguna específica — solo git CLI.

---

## Ejecución

### Opción A — Rebase normal (sin conflictos)

```bash
cd <worktree_path>
git status                                    # limpio
git fetch origin
git rebase origin/main
```

Si retorna `Successfully rebased` → push:

```bash
git push origin <branch_name> --force-with-lease
```

### Opción B — Rebase con conflictos

```bash
git fetch origin
git rebase origin/main
# CONFLICT (content): Merge conflict in ...
```

Resolver conflictos manualmente en cada archivo:

```bash
# Editar archivos conflictivos
git status              # lista files con conflicto
# editar src/foo.ts (resolver <<<<<<< / ======= / >>>>>>>)
git add src/foo.ts

# Continuar rebase
git rebase --continue

# Si más conflictos, repetir. Si hay error grave:
git rebase --abort      # cancela el rebase, vuelve al estado previo
```

Cuando termina:

```bash
git push origin <branch_name> --force-with-lease
```

### Opción C — Rebase con dependencia parent que ya mergeó

Caso del `PROTOCOL-WT-001 §5.4.2` — tu branch nació desde `feature/MS-309` que ya mergeó a main:

```bash
cd <worktree_path>
git fetch origin
# Rebase quita los commits de MS-309 que ya están en main, deja solo los tuyos
git rebase origin/main
git push origin <branch_name> --force-with-lease
```

---

## Validación

```bash
# Verificar que tu branch está al día con main
git log --oneline origin/main..<branch_name>
# Esperado: solo tus commits (los de main NO aparecen)

# Confirmar que no hay diff "atrás" de main
git log --oneline <branch_name>..origin/main
# Esperado: vacío
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Conflictos durante rebase | Otro PR tocó los mismos archivos | Resolver manualmente, `git add`, `git rebase --continue` |
| `git push --force` (sin lease) destruyó commits | Push fuerza sin verificar remote | **NUNCA `--force` sin `--force-with-lease`** — abortó cambios de otro agente |
| Working tree no limpio | Hay cambios pendientes | Commitear o stash antes de rebase (ver `PROTOCOL-WT-001 §5.4.3`) |
| Rebase rompió todo | Conflictos mal resueltos | `git rebase --abort` y reintentar con cuidado |
| Push rechazado "behind remote" | Otro agente pusheó a la misma branch | Imposible si seguís disciplina de worktree (PROTOCOL-WT-001 §7.1). Si pasa: investigar antes de force |
| `divergent branches` después de rebase | Llaves cruzadas con stash | `git stash pop` con cuidado, resolver conflicto |

---

## Cuándo hacer rebase

| Caso | ¿Rebase? |
|---|---|
| Acabás de empezar la tarea | ❌ No (acabás de salir de main, no hay drift) |
| Trabajaste >4h en la tarea y main puede haber cambiado | ✅ Sí — antes de crear PR |
| Tu PR falla CI porque main cambió | ✅ Sí — rebase y push de nuevo |
| Otro PR mergeó algo que afecta tu código | ✅ Sí — rebase para integrar antes de CI |
| Vas a abrir PR ahora | ✅ Sí — rebase + push antes de `gh pr create` |

---

## Skills invocadas

Ninguna — solo git CLI.

---

## Skills que invocan ESTA

- `VTT.SKILL-GIT-006_crear_pr` (cuando se cree) — rebase es precondición del PR
- Workflow del agente antes de cerrar entrega

---

## Cuándo NO usar esta Skill

- **Si la branch fue creada hoy mismo y nadie tocó main** — rebase innecesario
- **Si hay cambios sin commitear** — commitear primero (o stash)
- **Si estás en la branch idle `wt-<repo>-<rol>`** — esa NO se rebasa, ver `PROTOCOL-WT-001 §7.5`

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-GIT-02_rebase-main.md` con renumeración a `GIT-004`. Ampliación: 3 opciones (normal / con conflictos / con dependencia parent) + tabla "Cuándo hacer rebase". Refuerza la regla `--force-with-lease` (nunca `--force`). |
