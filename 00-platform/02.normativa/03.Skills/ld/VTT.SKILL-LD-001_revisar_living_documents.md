# VTT.SKILL-LD-001 — Revisar catálogo de Living Documents

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-LD-001` |
| **Categoría** | LD (Living Documents) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor al cierre (ANTES del commit) |
| **Tokens estimados** | ~120 |
| **Cuándo se usa** | Paso 5.3.5 del PROTOCOL-ASG-001 / `WORKFLOW-ASG-001.017` / `CARD-EXE-005` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string | sí | TASK_ID |
| `project_name` | string | sí | |
| `living_docs_catalog_path` | path | sí | `LIVING_DOCUMENTS_<PROYECTO>.md` |
| `files_changed` | array | sí | `git diff --name-only main...HEAD` |

## Precondición

- Catálogo LDs existe
- Cambios NO committeados

## Variables del entorno

- `$VTT_TOKEN`

## Reglas

- R1 Revisar TODOS los LDs sin excepción
- R2 Declarar "sin cambios" explícito (no implícito)
- R3 LD modificado → `SKILL-DOCIMP-001`
- R4 Inconsistencias menores → `tech_debt` + TI

## Ejecución

```bash
python $VTT_SETUP/02.normativa/04.Scripts/ld/SCRIPT-LD-001_check_impacts.py \
  --task-id "$TASK_ID" \
  --catalog "$LIVING_DOCS_CATALOG_PATH" \
  --files-changed "$FILES_CHANGED_JSON"
```

Script extrae lista de LDs del catálogo + sugiere impacts según `files_changed`.

## Validación

- Total revisados = Total catálogo
- Devlog entry por LD (sin cambios o modificado)

## Error común

- Catálogo no existe → escalar al PM
- LD físico no existe (path desactualizado) → actualizar catálogo

## Scripts invocados

- `SCRIPT-LD-001_check_impacts.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. |
