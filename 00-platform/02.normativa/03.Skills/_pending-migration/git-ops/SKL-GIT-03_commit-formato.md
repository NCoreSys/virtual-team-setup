# SKL-GIT-03: Commit con formato del proyecto

**Categoría:** GIT-OPS  
**Aplica a:** Todos  
**Tokens estimados:** ~75  
**Cuándo:** Paso 10 del workflow

## Variables requeridas

- `$FILES_TO_ADD` — archivos específicos a agregar (evitar `git add .`)
- `$COMMIT_TYPE` — `feat` | `fix` | `docs` | `refactor` | `test` | `chore`
- `$TASK_ID` — ej: `MS-145`
- `$COMMIT_DESCRIPTION` — descripción breve
- `$CAMBIO_1`, `$CAMBIO_2` — cambios realizados

## Ejecución

```bash
git add $FILES_TO_ADD

git commit -m "$(cat <<'EOF'
$COMMIT_TYPE [$TASK_ID]: $COMMIT_DESCRIPTION

- $CAMBIO_1
- $CAMBIO_2

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #$TASK_ID
EOF
)"
```

## Regla

`Co-Authored-By` es OBLIGATORIO en todos los commits.

## Validación

`git log --oneline -1` muestra el commit con formato correcto.
