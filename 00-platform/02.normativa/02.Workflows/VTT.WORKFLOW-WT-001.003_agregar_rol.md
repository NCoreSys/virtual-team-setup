# VTT.WORKFLOW-WT-001.003 — Agregar Worktree de Rol Nuevo

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-WT-001.003` |
| **Pertenece a** | `VTT.PROTOCOL-WT-001` §5.3 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-18 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL principal del proyecto |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-WT-001 §5.3.2 y §5.3.3 |
| **Frecuencia** | Bajo demanda — cuando entra un rol nuevo al proyecto |

---

## 1. Propósito

Agregar **incrementalmente** un worktree + workspace VSCode para un rol que NO existía al iniciar el proyecto. Casos típicos:
- FE entra al llegar a Fase 4.4 (Frontend) cuando antes solo había BE/DB/QA
- SEC entra a Fase 3B.7 (Security Plan)
- AR entra al primer review arquitectónico

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `project_root` | path absoluto | Estructura del proyecto | sí | Ya inicializado por WORKFLOW-WT-001.001 |
| `rol` | string | Decisión del TL | sí | Lowercase — ej. `fe`, `sec`, `ar` |
| `rol_descripcion` | string | Operativo del rol | sí | Ej. "Frontend Engineer" |
| `repo` | string | Repo donde operará | sí | Ej. `frontend`, `project` |
| `repo_full_name` | string | Estructura del proyecto | sí | Ej. `memory-service-frontend` |
| `proyecto_display` | string | Nombre humano del proyecto | sí | Ej. "Memory Service" |

---

## 3. Precondiciones

- WORKFLOW-WT-001.001 (Setup inicial) ya ejecutado — existe `.vtt/{worktrees,workspaces,manifests}/`
- El repo donde operará el rol nuevo está clonado en `<project_root>/<repo_full_name>/`
- El rol NO tiene worktree aún (este Workflow no es para casos existentes — para eso usar la apertura diaria)
- TL tiene permisos de escritura en `<project_root>/`

---

## 4. Reglas del Workflow

- **R1:** Verificar que el worktree NO existe ANTES de crear (evitar choque con setup previo)
- **R2:** Usar mismo naming convention que en WORKFLOW-WT-001.001 (`<repo>-<rol>` + `wt-<repo>-<rol>`)
- **R3:** Si el rol opera en múltiples repos, ejecutar este Workflow una vez por cada `(rol, repo)`
- **R4:** Notificar al Coordinador para que abra la ventana cuando empiece a usarse

---

## 5. Pasos

### Paso 1 — Verificar que el worktree no existe

```bash
WT_PATH=<project_root>/.vtt/worktrees/<repo>-<rol>

if [ -d "$WT_PATH" ]; then
    echo "ERROR: worktree ya existe — usar Apertura Diaria o abortar"
    exit 1
fi
```

### Paso 2 — Verificar repo del rol

```bash
REPO_DIR=<project_root>/<repo_full_name>

if [ ! -d "$REPO_DIR/.git" ]; then
    echo "ERROR: $REPO_DIR no es git repo"
    exit 1
fi

cd $REPO_DIR
git fetch origin
```

### Paso 3 — Crear worktree con branch idle

```bash
BRANCH_IDLE=wt-<repo>-<rol>

# Si la branch idle ya existe (raro pero posible), reusar
if git rev-parse --verify "$BRANCH_IDLE" >/dev/null 2>&1; then
    git worktree add $WT_PATH $BRANCH_IDLE
else
    git worktree add $WT_PATH -b $BRANCH_IDLE origin/main
fi
```

→ invoca **`VTT.SKILL-WT-001`** con (`action=add_worktree`, `repo`, `rol`, `worktree_path`, `branch_idle`)

### Paso 4 — Generar workspace VSCode

```bash
WS_FILE=<project_root>/.vtt/workspaces/<repo>-<rol>.code-workspace

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

→ invoca **`VTT.SKILL-WT-002`** con (`action=generate_workspace`, datos del input)

### Paso 5 — Verificar

```bash
# Worktree creado
git worktree list | grep "<repo>-<rol>"

# Workspace creado
ls $WS_FILE

# Branch idle activa
cd $WT_PATH && git branch --show-current
# Esperado: wt-<repo>-<rol>
```

### Paso 6 — Documentar el onboarding

Agregar entrada en el handoff del proyecto o en el catálogo de roles:

```
Rol nuevo onboardeado:
- Rol: <rol> (<rol_descripcion>)
- Repo principal: <repo_full_name>
- Worktree: .vtt/worktrees/<repo>-<rol>/
- Workspace VSCode: .vtt/workspaces/<repo>-<rol>.code-workspace
- Fecha: <YYYY-MM-DD>
- Onboardeado por: TL <nombre>
```

### Paso 7 — Notificar al Coordinador

Mensaje:
> Rol <rol> (<rol_descripcion>) listo para empezar. Abrir workspace VSCode: `.vtt/workspaces/<repo>-<rol>.code-workspace`.

El Coordinador procede a abrir la ventana cuando el rol vaya a empezar (siguiente sesión diaria).

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `.vtt/worktrees/<repo>-<rol>/` | carpeta git worktree | local | Worktree dedicado del rol nuevo |
| `.vtt/workspaces/<repo>-<rol>.code-workspace` | archivo JSON | local | Workspace VSCode |
| Branch idle `wt-<repo>-<rol>` | branch git | repo local | Branch base del worktree |
| Notificación al Coordinador | mensaje | chat coordinador | Confirma que el rol puede empezar |
| Entrada de documentación | texto | handoff del proyecto | Audit trail del onboarding |

---

## 7. Validación de salida

```bash
# Check 1: worktree existe y activo
git worktree list | grep "<repo>-<rol>"

# Check 2: workspace tiene JSON válido
python -m json.tool < <project_root>/.vtt/workspaces/<repo>-<rol>.code-workspace > /dev/null

# Check 3: branch idle correcta
cd <project_root>/.vtt/worktrees/<repo>-<rol>
git branch --show-current
# Esperado: wt-<repo>-<rol>

# Check 4: working tree limpio
git status
# Esperado: nothing to commit
```

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Worktree ya existe | Rol ya fue onboardeado | Usar Apertura Diaria, no este Workflow |
| `git worktree add fatal: invalid reference` | Branch idle name inválido | Verificar naming `wt-<repo>-<rol>` (lowercase, sin espacios) |
| Repo del rol no clonado | El rol opera en repo que aún no está local | Clonar el repo primero: `git clone <url>` en `<project_root>/` |
| Workspace VSCode no abre el folder | Path relativo mal | Verificar `../worktrees/<repo>-<rol>` (relativo a `.vtt/workspaces/`) |
| Coordinador no sabe que el rol entró | Falta Paso 7 | Notificación es obligatoria |

---

## 9. Skills invocadas

- `VTT.SKILL-WT-001` — `action=add_worktree` (Paso 3)
- `VTT.SKILL-WT-002` — `action=generate_workspace` (Paso 4)

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-WT-001` Worktree policy | Mantener un worktree por rol |
| `RULE-AGENT-001 v2.0` Worktree por rol | Cada rol nuevo respeta la convención |

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-18 | PM Martin Rivas | Versión inicial. Cubre el caso de roles que entran después del setup inicial. Reutiliza las mismas Skills (`WT-001`, `WT-002`) que el setup inicial. |
