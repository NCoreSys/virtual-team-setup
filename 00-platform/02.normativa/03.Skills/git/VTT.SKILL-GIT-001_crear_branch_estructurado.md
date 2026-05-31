# VTT.SKILL-GIT-001 — Crear branch estructurado verificable contra un patrón

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-GIT-001` |
| **Categoría** | GIT |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-17 |
| **Aplica a** | Todos los roles que editen cualquier repo gobernado por VTT |
| **Tokens estimados** | ~180 |
| **Cuándo se usa** | ANTES de modificar archivos en un repo. Garantiza que el branch cumple el patrón de naming que ese repo exige. |

---

## Inputs (contractuales)

Parámetros que la Skill recibe SIEMPRE de igual forma, independiente del repo o del contexto:

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `branch_pattern_regex` | string (regex) | sí | Expresión regular extendida que el nombre del branch debe cumplir. Definida por la gobernanza del repo. Ej: `^agent/(tl\|pm\|be)/[a-z0-9-]{3,30}/[a-z0-9-]{3,50}$` |
| `branch_name` | string | sí | Nombre exacto del branch a crear. La Skill valida que cumple `branch_pattern_regex` antes de crearlo. |
| `base_ref` | string | no (default `origin/main`) | Referencia desde donde se crea el branch. Suele ser `origin/main`. |
| `repo_path` | path | no (default `.`) | Path al repo donde se crea el branch. |

> **Regla contractual:** la Skill NO contiene el patrón de naming de ningún repo. El patrón se pasa siempre como input. La lógica "qué formato usar" vive en el Workflow o documento de gobernanza que invoca esta Skill.

---

## Precondición

Condiciones que deben ser verdaderas ANTES de ejecutar esta Skill:

- El directorio `repo_path` es un repo Git válido (`.git/` existe)
- `git fetch origin` se puede ejecutar (acceso al remote)
- `base_ref` existe en el remote (ej. `origin/main` no es `null`)
- `branch_name` aún no existe (ni local ni remoto) — si existe, se debe escalar antes de invocar la Skill
- El working tree está limpio o el agente acepta llevar sus cambios al branch nuevo

---

## Variables del entorno

```bash
$GIT_AUTHOR_NAME       # Configurado vía git config (no se setea aquí)
$GIT_AUTHOR_EMAIL      # Configurado vía git config (no se setea aquí)
```

> **Política:** esta Skill NO usa variables específicas de proyecto. Todo se recibe como input contractual.

---

## Ejecución

La Skill valida que `branch_name` cumple `branch_pattern_regex`, sincroniza `base_ref`, y crea+checkea el nuevo branch.

### Comando(s)

```bash
# Inputs (ejemplo)
BRANCH_PATTERN_REGEX='^agent/(tl|pm|pjm|be|db|fe|do|qa|ux|dl|sa|ar|sec|setup)/[a-z0-9-]{3,30}/[a-z0-9-]{3,50}$'
BRANCH_NAME="agent/pm/vtt-setup/skills-git-001-002"
BASE_REF="origin/main"
REPO_PATH="."

cd "$REPO_PATH"

# 1. Validar formato del branch contra el regex del repo
echo "$BRANCH_NAME" | grep -qE "$BRANCH_PATTERN_REGEX" \
  || { echo "ABORT: branch_name '$BRANCH_NAME' no cumple branch_pattern_regex"; exit 1; }

# 2. Sincronizar base_ref
git fetch origin

# 3. Validar que base_ref existe
git rev-parse --verify "$BASE_REF" \
  || { echo "ABORT: base_ref '$BASE_REF' no existe"; exit 1; }

# 4. Validar que branch_name no existe
git show-ref --verify --quiet "refs/heads/$BRANCH_NAME" \
  && { echo "ABORT: branch local '$BRANCH_NAME' ya existe"; exit 1; }
git ls-remote --exit-code --heads origin "$BRANCH_NAME" >/dev/null 2>&1 \
  && { echo "ABORT: branch remoto '$BRANCH_NAME' ya existe"; exit 1; }

# 5. Crear y checkear branch desde base_ref
git checkout -b "$BRANCH_NAME" "$BASE_REF"
```

> **Política:** lógica ≤30 líneas, sin Script externo. Si el repo requiere comportamiento extra (worktrees, hooks pre-branch), eso pertenece a un Workflow específico que invoca esta Skill como un paso.

---

## Validación

Cómo saber si la Skill funcionó:

- `git rev-parse --abbrev-ref HEAD` retorna exactamente `branch_name`
- `git rev-parse HEAD` apunta al mismo commit que `base_ref` (no hay commits aún en el branch nuevo)
- El branch local existe (`git branch --list "$BRANCH_NAME"` muestra una línea)

```bash
# Comando de validación post-ejecución
CURRENT=$(git rev-parse --abbrev-ref HEAD)
[ "$CURRENT" = "$BRANCH_NAME" ] || { echo "FAIL: HEAD no apunta a $BRANCH_NAME"; exit 1; }
echo "$CURRENT" | grep -qE "$BRANCH_PATTERN_REGEX" || { echo "FAIL: branch creado no cumple patron"; exit 1; }
echo "OK — branch '$CURRENT' creado desde '$BASE_REF'"
```

---

## Error común

| Error | Causa probable | Solución |
|---|---|---|
| `ABORT: branch_name no cumple branch_pattern_regex` | El nombre tiene mayúsculas, underscores, o falta segmento | Ajustar `branch_name` al patrón. Para vtt-setup: `agent/<rol>/<proyecto>/<desc>` solo `[a-z0-9-]` |
| `ABORT: base_ref no existe` | Mal escrito (`origin/master`) o repo sin remote | Verificar `git remote -v` y nombre del branch principal |
| `ABORT: branch ya existe` | Trabajo previo no terminado en esa rama | Cambiar `branch_name` (sufijo `-v2`) o reanudar el branch existente |
| `not a git repository` | `repo_path` mal configurado | Confirmar `cd` al repo correcto antes de invocar |
| `couldn't find remote ref` en fetch | Conectividad o auth | Verificar `gh auth status` y conectividad |

---

## Scripts invocados

Sin Scripts externos — lógica inline en sección Ejecución (30 líneas, dentro del límite de ≤5 líneas por bloque conceptual del template).

> Cuando el catálogo `04.Scripts/` esté poblado, esta Skill podrá refactorizarse para invocar `VTT.SCRIPT-GIT-001_validate_branch_name.py` + `VTT.SCRIPT-GIT-002_create_branch_from_ref.py`.

---

## Ejemplo de uso — gobierno editorial de virtual-teams-setup

Para el repo `virtual-teams-setup` durante la Fase de Desarrollo, el patrón de naming exigido por la gobernanza es:

```
agent/<rol>/<proyecto-origen>/<descripcion-kebab-case>
```

Con esto, los inputs a la Skill son:

```bash
BRANCH_PATTERN_REGEX='^agent/(tl|pm|pjm|be|db|fe|do|qa|ux|dl|sa|ar|sec|setup)/[a-z0-9-]{3,30}/[a-z0-9-]{3,50}$'
BRANCH_NAME="agent/pm/vtt-setup/skills-git-001-002"
BASE_REF="origin/main"
```

Donde:

| Segmento | Significado | Valores válidos |
|---|---|---|
| `<rol>` | Rol corto del agente | `tl, pm, pjm, be, db, fe, do, qa, ux, dl, sa, ar, sec, setup` |
| `<proyecto-origen>` | Slug del proyecto que originó el cambio | `vtt-setup, memory-service, designmine, ...` |
| `<descripcion-kebab-case>` | Qué se cambia | `[a-z0-9-]{3,50}` |

> Este ejemplo es **instancia** de la Skill, no la Skill misma. Si otro repo (ej. memory-service-backend) exige un patrón distinto (`feature/<TASK_ID>`), la misma Skill se invoca con otro `branch_pattern_regex`.

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial. Skill genérica para crear branch verificado contra un regex. Inputs contractuales: `branch_pattern_regex`, `branch_name`, `base_ref`, `repo_path`. |

> **Política de versionado** (Incremental):
> - **v1, v2, v3...** — incremento por cambio de contrato (inputs/outputs) o de comportamiento mayor.
> - Mejoras internas que no cambian el contrato → misma versión, actualizar fecha.
