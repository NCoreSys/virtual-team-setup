# VTT.WORKFLOW-ASG-001.018 — Registrar Document Impacts en VTT

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.018` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.6 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor |
| **Reglas Nivel 0** | `RULE-SCRIPT-001`, `RULE-DOCS-001` |
| **CARD asociada** | `VTT.CARD-EXE-006` |

---

## 1. Propósito

Registrar formalmente en VTT (vía `POST /api/tasks/:id/document-impacts`) cada documento canónico afectado. Alimenta trazabilidad code ↔ docs.

**Gotcha DEBT-INFRA-VTT-01:** endpoint exige `documentSourceId` no siempre expuesto al DO → fallback a devlog `observation` con detalle.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `documents_affected` | array | `[{path, impact_type, description, document_source_id?}]` |

`impact_type` ∈ {`added`, `modified`, `removed`, `referenced`}

## 3. Precondiciones

- `.017` ejecutado (LDs revisados — fuente principal de impacts)

## 4. Reglas

| # | Regla |
|---|---|
| R1 | UN Document Impact por doc — NO agrupar |
| R2 | `impactType` del enum cerrado |
| R3 | Si no acceso a `documentSourceId` → fallback devlog `observation` |
| R4 | `description` concreta (qué + por qué + sección) — NO genérica |
| R5 | `referenced` cuando código nuevo menciona doc sin modificarlo |

## 5. Pasos

### Paso 1 — Consolidar lista
Outputs `.017` (LDs modificados) + `.LOGIC.md` nuevos + ADRs creados + otros docs canónicos.

### Paso 2 — Resolver `documentSourceId`
```bash
DOC_SOURCE_ID=$(curl -s "$VTT_BASE_URL/api/projects/<PROJECT_ID>/document-sources?path=<path>" \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d['items'][0]['id'] if d.get('items') else '')")
```

### Paso 3 — POST /document-impacts (camino normal)
```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/document-impacts" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{
    "documentSourceId":"<UUID>",
    "impactType":"modified",
    "description":"Actualizada §X.Y — <qué cambió + por qué>"
  }'
```

### Paso 4 — Fallback devlog (DEBT-INFRA-VTT-01)
Si 403/404:
```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/devlog-entries" \
  -d '{"entries":[{
    "categoryCode":"observation",
    "severity":"low",
    "title":"Document Impacts (fallback DEBT-INFRA-VTT-01)",
    "description":"POST /document-impacts no accesible. Declaración:\n1. ...\n2. ..."
  }]}'
```

### Paso 5 — Validar
```bash
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>/document-impacts" | python -m json.tool
```

`count(impacts) >= count(documents_affected)` O fallback devlog OK.

### Paso 6 — Reportar en SKL-REPORT-01 (paso 12.b del .034)

## 6. Outputs

| Output | Descripción |
|---|---|
| `impacts_attempted` | int |
| `impacts_registered_endpoint` | int |
| `impacts_registered_fallback` | int |
| `total_registered` | int (debe = attempted) |

## 7. Validación

`total_registered == impacts_attempted`

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| HTTP 403 | Sin acceso documentSourceId | Fallback devlog (R3) |
| HTTP 400 invalid impactType | Fuera enum | Solo added/modified/removed/referenced |
| Saltó algún doc | Lista incompleta | Volver al Paso 1 |

## 9. Skills invocadas

- `SKILL-DOCIMP-001`, `SKILL-DEV-001` (fallback)

## 10. Scripts invocados

- `SCRIPT-DOCIMP-001_register_impact.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Endpoint dedicado + fallback DEBT-INFRA-VTT-01. |
