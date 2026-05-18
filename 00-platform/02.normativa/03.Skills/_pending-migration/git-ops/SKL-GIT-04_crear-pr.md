# SKL-GIT-04: Crear PR con gh CLI

**Categoría:** GIT-OPS  
**Aplica a:** Todos  
**Tokens estimados:** ~70  
**Cuándo:** Paso 11 del workflow — inmediatamente después del commit y push

## Variables requeridas

- `$TASK_ID` — ej: `MS-145`
- `$PR_TITLE` — título descriptivo
- `$PR_DESCRIPTION` — descripción de cambios
- `$HOW_TO_TEST` — pasos para probar
- `$TASK_SLUG` — nombre corto (ej: `setup-express`)

## Ejecución

```bash
git push origin feature/$TASK_ID

gh pr create \
  --title "[$TASK_ID] $PR_TITLE" \
  --body "$(cat <<'EOF'
## Cambios
$PR_DESCRIPTION

## Cómo probar
$HOW_TO_TEST

Ver devlog: knowledge/development-log/$(date +%Y-%m-%d)_${TASK_ID}_${TASK_SLUG}.md
EOF
)" \
  --base main
```

## Validación

gh devuelve URL del PR creado. Copiar URL para incluir en SKL-REPORT-01.
