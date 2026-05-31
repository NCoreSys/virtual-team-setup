# VTT.SKILL-WT-002 — Generar Workspace VSCode

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-WT-002` |
| **Categoría** | WT (Worktree) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-18 |
| **Aplica a** | Coordinador (setup inicial), TL (onboarding de rol nuevo) |
| **Tokens estimados** | ~250 |
| **Cuándo se usa** | Al crear o regenerar un archivo `.code-workspace` VSCode para un rol específico |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `action` | enum | sí | Una de: `generate_workspace`, `regenerate_workspace` |
| `project_root` | path absoluto | sí | Raíz del proyecto |
| `repo` | string | sí | Nombre corto del repo (ej. `backend`) |
| `rol` | string | sí | Rol lowercase (ej. `be`) |
| `rol_descripcion` | string | sí | Descripción humana (ej. "Backend Engineer") |
| `proyecto_display` | string | sí | Nombre humano del proyecto (ej. "Memory Service") |

---

## Precondición

- El worktree del rol existe en `.vtt/worktrees/<repo>-<rol>/`
- La carpeta `.vtt/workspaces/` existe (creada por `WORKFLOW-WT-001.001 §5.1.3`)

---

## Variables del entorno

Ninguna específica. La Skill solo necesita los inputs.

---

## Schema del workspace generado

```json
{
  "folders": [
    {
      "name": "<ROL_UPPER> <Rol Descripción>",
      "path": "../worktrees/<repo>-<rol>"
    }
  ],
  "settings": {
    "window.title": "<ROL_UPPER> - <Rol Descripción> | <Proyecto>",
    "terminal.integrated.cwd": "${workspaceFolder}"
  }
}
```

### Reglas del schema

- **`folders[0].name`**: usar `<ROL_UPPER>` (rol en mayúsculas) + descripción. Ej. `"BE Backend Engineer"`.
- **`folders[0].path`**: SIEMPRE relativo (`../worktrees/<repo>-<rol>`) — NO absoluto, para portabilidad.
- **`settings.window.title`**: identificable a simple vista — formato `<ROL_UPPER> - <Descripción> | <Proyecto>`.
- **`settings.terminal.integrated.cwd`**: `${workspaceFolder}` para que el terminal abra en el worktree del rol.

---

## Acciones

### action=generate_workspace

Crea el archivo `.code-workspace`. Falla si ya existe (para evitar sobrescribir customizaciones).

```bash
WS_FILE="$PROJECT_ROOT/.vtt/workspaces/$REPO-$ROL.code-workspace"

if [ -f "$WS_FILE" ]; then
    echo '{"success": false, "error": "workspace ya existe, usar action=regenerate_workspace"}'
    exit 1
fi

ROL_UPPER=$(echo "$ROL" | tr '[:lower:]' '[:upper:]')

cat > "$WS_FILE" <<EOF
{
  "folders": [
    {
      "name": "$ROL_UPPER $ROL_DESCRIPCION",
      "path": "../worktrees/$REPO-$ROL"
    }
  ],
  "settings": {
    "window.title": "$ROL_UPPER - $ROL_DESCRIPCION | $PROYECTO_DISPLAY",
    "terminal.integrated.cwd": "\${workspaceFolder}"
  }
}
EOF

echo "{\"success\": true, \"workspace_path\": \"$WS_FILE\"}"
```

### action=regenerate_workspace

Sobrescribe el workspace existente (descarta customizaciones).

```bash
WS_FILE="$PROJECT_ROOT/.vtt/workspaces/$REPO-$ROL.code-workspace"

ROL_UPPER=$(echo "$ROL" | tr '[:lower:]' '[:upper:]')

cat > "$WS_FILE" <<EOF
{ ... mismo contenido ... }
EOF

echo "{\"success\": true, \"workspace_path\": \"$WS_FILE\", \"overwritten\": true}"
```

---

## Validación post-ejecución

```bash
# JSON válido
python -m json.tool < "$WS_FILE" > /dev/null

# Path relativo en folder
jq -r '.folders[0].path' "$WS_FILE"
# Esperado: ../worktrees/<repo>-<rol>

# Title presente
jq -r '.settings."window.title"' "$WS_FILE"
# Esperado: "<ROL_UPPER> - <Descripción> | <Proyecto>"

# Worktree referenciado existe
WT_PATH="$PROJECT_ROOT/.vtt/worktrees/$REPO-$ROL"
[ -d "$WT_PATH" ] && echo "OK" || echo "ERROR: worktree no existe"
```

---

## Error común

| Error | Causa probable | Solución |
|---|---|---|
| Workspace ya existe | `generate_workspace` sobre archivo existente | Usar `regenerate_workspace` o borrar manualmente primero |
| JSON inválido al generar | Caracteres especiales en `<Descripción>` (comillas, $) | Escapar `\` ANTES de pasar como input |
| VSCode no abre el worktree | Path absoluto en lugar de relativo | Verificar que el archivo usa `../worktrees/...` |
| `window.title` no aparece | VSCode antiguo no soporta `window.title` en workspace settings | Verificar versión VSCode ≥ 1.40 |
| Workspace abre folder vacío | Worktree no existe | Crear worktree primero con SKILL-WT-001 |

---

## Scripts invocados

Ninguno — esta Skill genera el archivo directamente (lógica inline ≤30 líneas).

Sin embargo, los Scripts `VTT.SCRIPT-WT-001` (setup_worktrees.py) y `VTT.SCRIPT-WT-002` (add_worktree.py) **invocan internamente** esta Skill (composición Skill→Skill via Python).

---

## Casos especiales

### Rol que opera en múltiples repos

Si un rol opera en repos distintos (ej. TL en `project` y eventualmente en `backend`), generar **un workspace por (repo, rol)**:
- `.vtt/workspaces/project-tl.code-workspace` (worktree principal)
- `.vtt/workspaces/backend-tl.code-workspace` (auxiliar, generalmente solo para review)

Cada uno apunta a su worktree correspondiente.

### Workspace multi-folder (compuesto)

Si el TL necesita ver varios worktrees en una sola ventana, generar un workspace compuesto:

```json
{
  "folders": [
    { "name": "TL Project",  "path": "../worktrees/project-tl" },
    { "name": "TL Backend",  "path": "../worktrees/backend-tl" }
  ],
  "settings": { ... }
}
```

> **NO recomendado para uso diario** — viola la regla "una ventana = un rol = un repo". Solo para casos puntuales de review cross-repo.

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-18 | Versión inicial. Schema del workspace VSCode + 2 acciones (generate/regenerate). Casos especiales (multi-repo, multi-folder) documentados pero NO recomendados. |
