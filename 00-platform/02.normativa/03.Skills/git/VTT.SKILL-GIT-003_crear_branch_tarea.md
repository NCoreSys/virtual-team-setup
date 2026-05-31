# VTT.SKILL-GIT-003 — Crear branch de tarea (feature/<TASK_ID>)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-GIT-003` |
| **Categoría** | GIT |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles ejecutores |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Paso 0 del workflow del agente — antes de cualquier modificación de código |
| **Reemplaza** | `SKL-GIT-01_crear-branch.md` (legacy) |
| **Relacionada con** | `VTT.SKILL-GIT-001` (validar branch contra patrón) — esta crea, GIT-001 valida |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `worktree_path` | path | sí (si WT) | Worktree del rol (del execution_manifest) |
| `base_branch` | string | sí/no | Default: `main`. Otro caso: branch de tarea padre (ver `PROTOCOL-WT-001 §5.4.2`) |

---

## Precondición

- `git` instalado
- El agente está posicionado en su worktree (`VTT.WORKFLOW-WT-001.002`)
- `$TOKEN` no es necesario (solo operaciones git locales)

---

## Variables del entorno

No usa variables VTT — solo locales del shell.

---

## Convención de naming

Según `00_REGISTRO_ACRONIMOS.md §3.bis`:

| Pattern | Cuándo |
|---|---|
| `feature/<TASK_ID>` | **Default** — tarea normal (ej. `feature/MS-293`) |
| `fix/<TASK_ID>` | Re-entrega tras `task_rejected` |
| `tl/<TASK_ID>-close` | NO crear con esta skill (es del TL Reviewer, no del agente) |

---

## Ejecución

### Opción A — Branch desde main (caso default)

```bash
cd <worktree_path>     # ej. .vtt/worktrees/backend-be
git status             # debe estar limpio
git fetch origin
git checkout main && git pull origin main
git checkout -b feature/<TASK_ID> origin/main
```

### Opción B — Branch desde otra branch (dependencia no-mergeada)

Si la tarea depende de una branch padre que aún NO está en main (ver `PROTOCOL-WT-001 §5.4.2`):

```bash
cd <worktree_path>
git fetch origin
git checkout -b feature/<TASK_ID> origin/feature/<PARENT_TASK_ID>
```

Cuando la branch padre mergee a main → rebase con `VTT.SKILL-GIT-004`.

### Opción C — Re-entrega tras rechazo

```bash
cd <worktree_path>
git fetch origin
git checkout feature/<TASK_ID>   # ya existe de la entrega previa
git pull origin feature/<TASK_ID>
```

> **NO crear branch nueva** en re-entrega — usar la misma `feature/<TASK_ID>` para preservar historia.

---

## Validación

```bash
# Branch activa correcta
git branch --show-current
# Esperado: feature/<TASK_ID>

# Working tree limpio (no hay cambios pendientes)
git status
# Esperado: nothing to commit, working tree clean

# Base correcta
git log --oneline -1 origin/main..HEAD
# Esperado: vacío (recién creada) o solo tus commits si re-entrega
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Crear branch desde otro feature/X | No estabas en main al crear | `git checkout main && git pull` antes de Opción A |
| `fatal: 'feature/MS-XXX' already exists` | Branch ya existe (re-entrega o duplicado) | Si es re-entrega → Opción C; si es duplicado → escalar al TL |
| Branch creada en clon base (no worktree) | Olvidaste `cd` al worktree | Borrar branch local, `cd` al worktree correcto, recrear |
| Pull rechaza por divergencias | Tu local difería con remote | Si re-entrega: `git pull --rebase`. Si es la primera vez: `git reset --hard origin/main` |
| `error: src refspec` al push | Aún no se commiteó nada | OK — push después del primer commit |

---

## Skills invocadas

Ninguna — solo git CLI local.

---

## Skills que invocan ESTA

- Workflow del agente al iniciar tarea (Paso 0)
- `VTT.WORKFLOW-MAN-001.002` — el agente verifica branch contra `execution_manifest.branchExpected`

---

## Cuándo NO usar esta Skill

- **Si es branch del TL `tl/<TASK_ID>-close`** — usar `PROTOCOL-ASG-001 §5.5.bis` (FASE 4.5)
- **Si es `wt-<repo>-<rol>` (idle del worktree)** — la crea automáticamente `VTT.SCRIPT-WT-001` en setup
- **Si solo necesitás validar branch contra patrón** — usar `VTT.SKILL-GIT-001`

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-GIT-01_crear-branch.md` con renumeración a `GIT-003` (GIT-001/002 ya estaban tomados por PROTOCOL-GOV-002). Ampliación: 3 opciones (default / dependencia / re-entrega) según `PROTOCOL-WT-001 §5.4`. Cross-ref con convenciones de `00_REGISTRO_ACRONIMOS §3.bis`. |
