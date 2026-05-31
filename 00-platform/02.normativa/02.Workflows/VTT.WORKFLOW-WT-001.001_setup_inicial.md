# VTT.WORKFLOW-WT-001.001 — Setup Inicial de Worktrees

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-WT-001.001` |
| **Pertenece a** | `VTT.PROTOCOL-WT-001` §5.1 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-18 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | Coordinador humano (Martin) o TL principal |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-WT-001 §5.1.4 y §5.1.5 |
| **Frecuencia** | UNA VEZ por proyecto (al iniciarlo) |

---

## 1. Propósito

Crear la estructura completa de worktrees + workspaces VSCode para un proyecto VTT multi-rol al inicio del trabajo. Idempotente — si se ejecuta dos veces, no rompe nada (skip de los que ya existen).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `project_root` | path absoluto | Estructura del proyecto | sí | Ej. `c:/Users/Martin/Documents/virtual-teams/memory-service` |
| `roles_activos` | array de objetos `{rol, repo}` | Plan del proyecto | sí | Lista de roles que arrancan el proyecto |
| `vtt_setup_path` | path absoluto | Variable `$VTT_SETUP` | sí | Para copiar `_template.execution.json` |

### Ejemplo de `roles_activos`

```json
[
  { "rol": "tl", "repo": "project" },
  { "rol": "pm", "repo": "project" },
  { "rol": "sa", "repo": "project" },
  { "rol": "be", "repo": "backend" },
  { "rol": "db", "repo": "backend" },
  { "rol": "do", "repo": "backend" },
  { "rol": "qa", "repo": "backend" }
]
```

---

## 3. Precondiciones

- Los clones base de TODOS los repos del proyecto existen en `<project_root>/<repo>-<sufijo>/`
- Cada clon tiene `origin/main` accesible (`git fetch origin` funciona)
- No existe ya una carpeta `.vtt/worktrees/` (o existe y está vacía — si tiene contenido, hacer cleanup primero o usar el WORKFLOW-WT-001.003 para agregar incremental)
- Coordinador tiene permisos para escribir en `<project_root>/`

---

## 4. Reglas del Workflow

- **R1:** Idempotente — si ya existe el worktree, skip (NO falla)
- **R2:** Branch idle se llama exactamente `wt-<repo>-<rol>` (sin variantes)
- **R3:** Worktree path: `.vtt/worktrees/<repo>-<rol>/` (lowercase, separador guion)
- **R4:** Workspace VSCode path: `.vtt/workspaces/<repo>-<rol>.code-workspace` (mismo naming)
- **R5:** Si un rol opera en múltiples repos, se crea **un worktree por (repo, rol)** — ej. el TL puede tener `project-tl` y `backend-tl` simultáneamente

---

## 5. Pasos

### Paso 1 — Crear estructura `.vtt/`

```bash
cd <project_root>
mkdir -p .vtt/{worktrees,workspaces,manifests}
```

### Paso 2 — Copiar template del execution_manifest

```bash
cp $VTT_SETUP/03.templates/normativa/_template.execution.json \
   .vtt/manifests/_template.execution.json
```

Si el template no existe en el setup, crearlo con estructura mínima:
```json
{
  "schema_version": "1.0",
  "manifest_type": "execution",
  "task": { "id": "TBD" },
  "agent": { "uuid": "TBD", "role": "TBD" },
  "worktreePath": "TBD",
  "branchExpected": "TBD",
  "allowedPaths": [],
  "expectedOutputs": []
}
```

### Paso 3 — Agregar `.vtt/` al `.gitignore` del proyecto

```bash
cd <project_root>/<repo_principal>
grep -q "^\.vtt/" .gitignore || echo ".vtt/" >> .gitignore
```

Esto garantiza que los worktrees NO se commiteen (son infraestructura local).

### Paso 4 — Por cada rol en `roles_activos`, crear worktree

```bash
for each {rol, repo} in roles_activos:
    REPO_DIR=<project_root>/<repo_full_name>      # ej. memory-service-backend
    WT_PATH=<project_root>/.vtt/worktrees/<repo>-<rol>
    BRANCH_IDLE=wt-<repo>-<rol>

    # Si ya existe, skip
    if [ -d "$WT_PATH" ]; then
        echo "Skip: $WT_PATH ya existe"
        continue
    fi

    cd $REPO_DIR
    git fetch origin

    # Si la branch idle ya existe (de proyecto previo), reusar
    if git rev-parse --verify "$BRANCH_IDLE" >/dev/null 2>&1; then
        git worktree add $WT_PATH $BRANCH_IDLE
    else
        git worktree add $WT_PATH -b $BRANCH_IDLE origin/main
    fi
```

→ invoca **`VTT.SKILL-WT-001`** con (`action=add_worktree`, `repo`, `rol`, `worktree_path`, `branch_idle`)

### Paso 5 — Por cada rol, generar workspace VSCode

```bash
for each {rol, repo} in roles_activos:
    WS_FILE=<project_root>/.vtt/workspaces/<repo>-<rol>.code-workspace

    if [ -f "$WS_FILE" ]; then
        echo "Skip: $WS_FILE ya existe"
        continue
    fi

    # Generar desde template
    cat > $WS_FILE <<EOF
    {
      "folders": [
        { "name": "<ROL_UPPER> <Rol Descripción>",
          "path": "../worktrees/<repo>-<rol>" }
      ],
      "settings": {
        "window.title": "<ROL_UPPER> - <Rol Descripción> | <Proyecto>",
        "terminal.integrated.cwd": "\${workspaceFolder}"
      }
    }
    EOF
```

→ invoca **`VTT.SKILL-WT-002`** con (`action=generate_workspace`, `rol`, `rol_descripcion`, `proyecto`, `worktree_relative_path`)

### Paso 6 — Verificar setup completo

```bash
cd <project_root>/<repo_principal>
git worktree list
# Esperado: lista incluye TODOS los worktrees creados

ls -la <project_root>/.vtt/worktrees/
# Esperado: una carpeta por rol

ls <project_root>/.vtt/workspaces/
# Esperado: un .code-workspace por rol

ls <project_root>/.vtt/manifests/_template.execution.json
# Esperado: archivo existe
```

### Paso 7 — Reportar al PM

Generar resumen:
```
Setup completado:
- N worktrees creados (lista)
- N workspaces VSCode generados (lista)
- .gitignore actualizado
- Template execution_manifest copiado
- Branches idle creadas: wt-<repo>-<rol> (N total)
```

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `.vtt/worktrees/<repo>-<rol>/` | carpeta git worktree | local | Una por cada rol activo |
| `.vtt/workspaces/<repo>-<rol>.code-workspace` | archivo JSON | local | Una por cada rol |
| `.vtt/manifests/_template.execution.json` | archivo JSON | local | Template del execution_manifest |
| Entrada en `.gitignore` | línea | repo principal | `.vtt/` ignorado |
| Branch idle `wt-<repo>-<rol>` | branch git | cada repo | Una por cada rol (no se pushea) |

---

## 7. Validación de salida

```bash
# Check 1: estructura .vtt/ existe
ls -d <project_root>/.vtt/{worktrees,workspaces,manifests}

# Check 2: N worktrees creados
git worktree list | wc -l
# Esperado: N + 1 (los N nuevos + clon base)

# Check 3: N workspaces creados
ls <project_root>/.vtt/workspaces/*.code-workspace | wc -l
# Esperado: N

# Check 4: .vtt en .gitignore
grep "^\.vtt/" <project_root>/<repo>/.gitignore
# Esperado: línea presente

# Check 5: cada worktree tiene su branch idle activa
for wt in <project_root>/.vtt/worktrees/*/; do
    (cd $wt && git branch --show-current)
done
# Esperado: todos en wt-<repo>-<rol>
```

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `fatal: '<branch>' is already checked out at '<path>'` | Branch idle ya está en uso en otro worktree | OK — el script debe detectarlo y skip |
| `fatal: not a git repository` | El path del repo es incorrecto | Verificar `<project_root>/<repo>-<sufijo>` |
| `Permission denied: .gitignore` | Permisos de escritura | Verificar permisos / abrir terminal con permisos correctos |
| Workspace VSCode no abre el folder correcto | Path relativo mal calculado | Path en `.code-workspace` debe ser `../worktrees/<repo>-<rol>` (relativo a `.vtt/workspaces/`) |
| `mkdir: cannot create directory '.vtt'` | Permission denied | Verificar permisos del `<project_root>` |
| Worktree creado pero VSCode muestra "folder vacío" | Path absoluto en `.code-workspace` (no debería) | Usar path relativo `../worktrees/<repo>-<rol>` |

---

## 9. Skills invocadas

- `VTT.SKILL-WT-001` — `action=add_worktree` (Paso 4)
- `VTT.SKILL-WT-002` — `action=generate_workspace` (Paso 5)

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-WT-001` Worktree policy | Aplica directamente — este Workflow materializa la regla |
| `RULE-AGENT-001 v2.0` Worktree por rol | Define la convención `<repo>-<rol>` |

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-18 | PM Martin Rivas | Versión inicial. Formaliza el setup que se hacía manual en memory-service. Idempotente — soporta re-ejecución sin romper estado existente. |
