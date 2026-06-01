# VTT.WORKFLOW-ASG-001.017 — Revisar Living Documents impactados

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.017` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.5 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor — ANTES del commit final |
| **Reglas Nivel 0** | `RULE-CODE-001`, `RULE-DOCS-001`, `RULE-SCRIPT-001` |
| **CARD asociada** | `VTT.CARD-EXE-005` |
| **Origen** | `SOP-LD-01_living_documents.md` |

---

## 1. Propósito

Revisar **catálogo completo de Living Documents (LDs)** del proyecto y declarar explícitamente cuáles modifica la tarea. Sin revisión → LDs desactualizados (problema histórico Memory Service: SPEC v1.8 vs implementación real).

**LDs típicos:** SPEC del sistema, ERD/Schema DB, API Contract/Swagger, Diagrama Arquitectura, Catálogo Endpoints, Catálogo Componentes FE, ADRs, Catálogo TIs.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `project_name` | string | |
| `living_docs_catalog_path` | path | `LIVING_DOCUMENTS_<PROYECTO>.md` |
| `files_changed` | array | `git diff --name-only main...HEAD` |

## 3. Precondiciones

- Implementación completada (paso 5 del `.034`)
- Catálogo LDs existe en `knowledge/` o `docs/`
- Cambios NO committeados (este workflow puede generar updates en LDs)

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Revisar TODOS los LDs del catálogo, sin excepción |
| R2 | Declarar "sin cambios" explícitamente si no aplica (NO implícito) |
| R3 | LD modificado → invocar `.018` Document Impact |
| R4 | LD debe quedar consistente con código entregado |
| R5 | Inconsistencias menores → registrar `tech_debt` + crear TI |
| R6 | Sin revisión → bloquea Review Gate |

## 5. Pasos

### Paso 1 — Localizar catálogo
```bash
for path in knowledge/LIVING_DOCUMENTS_${PROJECT_NAME}.md \
           docs/LIVING_DOCUMENTS_${PROJECT_NAME}.md \
           knowledge/living-documents/CATALOG.md; do
  [ -f "$path" ] && LD_CATALOG="$path" && break
done
[ -n "$LD_CATALOG" ] || { echo "Escalar al PM"; exit 1; }
```

### Paso 2 — Extraer lista de LDs
`SKILL-LD-001` parsea la tabla del catálogo.

### Paso 3 — Por cada LD, evaluar impacto

Análisis típico por tipo de tarea:

| Tipo tarea | LDs típicamente impactados |
|---|---|
| BE — nuevo endpoint | API Contract, Catálogo Endpoints |
| BE — lógica de negocio | SPEC, ADRs |
| DB — migration | ERD, Schema, SPEC §Schema |
| FE — nueva pantalla | Componentes FE, Site Map, Wireframes |
| DO — infra | Arquitectura, Infrastructure Plan |
| QA — suite nueva | Test Strategy, KPIs calidad |
| DL — componente Design | Design System |

### Paso 4 — Declaración explícita por LD

**Si NO se modifica:**
```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/devlog-entries" \
  -d '{"entries":[{
    "categoryCode":"observation",
    "severity":"low",
    "title":"LD-XX (<nombre>): sin cambios",
    "description":"Tarea no afecta este LD porque <justificación>",
    "reportedBy":"<AGENT_UUID>"
  }]}'
```

**Si SÍ se modifica:**
1. Actualizar LD físicamente
2. Registrar devlog `decision` con cambios + sección §X.Y
3. Invocar `WORKFLOW-ASG-001.018` (Document Impact)

### Paso 5 — Inconsistencias menores → tech_debt
Devlog `tech_debt` severity=`medium` + crear TI tipo `tech_debt` vinculado al sprint próximo.

### Paso 6 — Checklist final
```
[ ] Total LDs revisados = Total del catálogo
[ ] Cada LD tiene devlog (sin cambios o actualizado)
[ ] LDs modificados están físicamente actualizados
[ ] Document Impacts registrados via .018 para LDs modificados
```

## 6. Outputs

| Output | Descripción |
|---|---|
| `total_lds_in_catalog` | int |
| `lds_reviewed` | int (debe = total) |
| `lds_modified` | array `[{ld_id, path, section}]` |
| `lds_unchanged` | array |
| `devlog_entries_created` | int ≥ total |

## 7. Validación

`total_lds_in_catalog == lds_reviewed`

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Catálogo no existe | Proyecto sin LDs formalizados | Escalar al PM |
| LD físico no existe | Path desactualizado | Actualizar catálogo + PM |
| Total revisados < catálogo | Saltó alguno | Volver al Paso 3 |
| LD actualizado sin Document Impact | Olvido paso 4 | Invocar `.018` |

## 9. Skills invocadas

- `SKILL-LD-001`, `SKILL-DEV-001`, `SKILL-DOCIMP-001` (condicional)

## 10. Scripts invocados

- `SCRIPT-LD-001_check_impacts.py`

## 11. Sub-workflows invocados

- `WORKFLOW-ASG-001.018` (si LD modificado)

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Formaliza PROTOCOL-ASG-001 §5.3.5 + SOP-LD-01. |
