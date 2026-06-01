# VTT.SKILL-DOCIMP-001 — Registrar Document Impact en VTT

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-DOCIMP-001` |
| **Categoría** | DOCIMP (Document Impacts) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor — registrar impacto formal en VTT |
| **Tokens estimados** | ~130 |
| **Cuándo se usa** | `WORKFLOW-ASG-001.018` / `CARD-EXE-006` — por cada doc canónico afectado |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string | sí | |
| `document_source_id` | UUID | sí si no fallback | |
| `impact_type` | enum | sí | `added`/`modified`/`removed`/`referenced` |
| `description` | text | sí | concreta (qué+por qué+sección) |
| `document_path` | path | opcional | para fallback |

## Precondición

- `$VTT_TOKEN` vigente

## Variables del entorno

- `$VTT_TOKEN`, `$VTT_BASE_URL`

## Reglas

- R1 UN impact por doc — NO agrupar
- R2 `impactType` del enum cerrado
- R3 Si no accesso a `documentSourceId` → fallback devlog `observation` (DEBT-INFRA-VTT-01)
- R4 `description` concreta — NO genérica

## Ejecución

```bash
python $VTT_SETUP/02.normativa/04.Scripts/docimp/SCRIPT-DOCIMP-001_register_impact.py \
  --task-id "$TASK_ID" \
  --document-source-id "$DOC_SOURCE_ID" \
  --impact-type "$IMPACT_TYPE" \
  --description "$DESCRIPTION" \
  [--fallback-document-path "$DOC_PATH"]
```

Internamente:
```bash
POST /api/tasks/<TASK_ID>/document-impacts
  {documentSourceId, impactType, description}
```

Si 403/404 → fallback `POST /devlog-entries` con observation.

## Validación

HTTP 201 con impact registrado, O fallback devlog OK.

## Error común

- HTTP 403 → fallback devlog (DEBT-INFRA-VTT-01)
- HTTP 400 invalid impactType → usar enum
- description vaga → re-redactar con especificidad

## Scripts invocados

- `SCRIPT-DOCIMP-001_register_impact.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. Endpoint + fallback DEBT-INFRA-VTT-01. |
