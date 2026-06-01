# VTT.SKILL-PR-001 — Crear Pull Request en GitHub

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-PR-001` |
| **Categoría** | PR (Pull Requests) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor al cierre (paso 13 del `.034`) |
| **Tokens estimados** | ~110 |
| **Cuándo se usa** | `WORKFLOW-ASG-001.034` paso 13 |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string | sí | |
| `title_summary` | string | sí | |
| `devlog_path` | path | sí | |
| `manifest_path` | path | sí | |
| `cas_summary` | array | sí | |
| `hardcode_status` | object | sí | |
| `base_branch` | string | opcional | default `main` |

## Precondición

- Branch `feature/<TASK_ID>` con commits y push
- Working tree limpio
- `gh` CLI auth OK

## Variables del entorno

- `$VTT_SETUP`, `GH_TOKEN`

## Reglas

- R1 Título `[<TASK_ID>] <descripción>`
- R2 Body incluye: Resumen, link devlog, link manifest, CAs, Hardcode Check, Co-Authored-By
- R3 Base = `main` (NO commit directo a main)
- R4 Desde worktree del rol (NO clone base)

## Ejecución

```bash
python $VTT_SETUP/02.normativa/04.Scripts/pr/SCRIPT-PR-001_create_pr.py \
  --task-id "$TASK_ID" \
  --title-summary "$TITLE_SUMMARY" \
  --devlog-path "$DEVLOG_PATH" \
  --manifest-path "$MANIFEST_PATH" \
  --cas-json "$CAS_JSON" \
  --hardcode-status "$HARDCODE_STATUS"
```

Script construye body con template + `gh pr create`.

## Validación

- PR URL retornado
- PR enlaza con feature branch
- Base = `main`

## Error común

- `gh: must be on branch` → checkout feature branch (R4)
- `gh: auth required` → `gh auth login`
- PR vacío → verificar commits + push

## Scripts invocados

- `SCRIPT-PR-001_create_pr.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. PR canónico con body estructurado. |
