# VTT.SKILL-CODE-001 — Implementación + .LOGIC.md espejo + Development Log

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-CODE-001` |
| **Categoría** | CODE (Implementación) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor durante implementación |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | `WORKFLOW-ASG-001.034` pasos 5, 7, 10 |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string | sí | |
| `brief_path` | path | sí | |
| `assignment_path` | path | sí | |
| `execution_manifest` | object | sí | con allowedPaths/deniedPaths |
| `files_to_create_or_modify` | array | sí | |

## Precondición

- Branch `feature/<TASK_ID>` creada
- Tarea en `task_in_progress`
- Template `TEMPLATE_CODE_LOGIC.md` disponible

## Variables del entorno

- `$VTT_SETUP`

## Reglas

- R1 PROHIBIDO tocar fuera de `allowedPaths`
- R2 PROHIBIDO mockear datos (`RULE-DATA-001`)
- R3 UN `.LOGIC.md` espejo por archivo (`RULE-CODE-001`)
- R4 Espejo en `knowledge/code-logic/` con misma estructura
- R5 `.LOGIC.md` NO contiene código fuente — solo descripciones
- R6 Si archivo `.LOGIC.md` ya existe → ACTUALIZAR (no crear segundo)
- R7 Development Log al cierre: `knowledge/development-log/YYYY-MM-DD_<TASK_ID>_<desc>.md`

## Ejecución

```bash
# Por cada archivo creado/modificado:
python $VTT_SETUP/02.normativa/04.Scripts/code/SCRIPT-CODE-001_create_logic_md.py \
  --source-file "src/controllers/example.ts" \
  --template "$VTT_SETUP/03.templates/code-logic/TEMPLATE_CODE_LOGIC.md"

# Al cierre:
python $VTT_SETUP/02.normativa/04.Scripts/code/SCRIPT-CODE-002_create_devlog.py \
  --task-id "$TASK_ID" \
  --template "$VTT_SETUP/03.templates/development-log/TEMPLATE_DEVELOPMENT_LOG.md"
```

## Validación

- Todos los archivos modificados tienen `.LOGIC.md` espejo
- Development Log con secciones obligatorias

## Error común

- Tocar fuera de allowedPaths → revertir + escalar TL
- Falta `.LOGIC.md` → crear (R3)
- Doble `.LOGIC.md` para un archivo → consolidar (R6)
- Código en `.LOGIC.md` → quitar (R5)

## Scripts invocados

- `SCRIPT-CODE-001_create_logic_md.py`
- `SCRIPT-CODE-002_create_devlog.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. Implementación + `.LOGIC.md` espejo + Development Log. |
