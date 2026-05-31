# SKL-REPORT-01: Reporte de entrega de tarea

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-REPORT-001_entrega_tarea.md`** en `02.normativa/03.Skills/report/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** REPORT  
**Aplica a:** BE, DB, FE, QA, DO, DL, UX, AR, SA  
**Tokens estimados:** ~220  
**Cuándo:** Después de pasar el review-gate y ejecutar SKL-STATUS-02

---

## Paso previo OBLIGATORIO antes de entregar

```bash
# 1. Verificar review gate — NUNCA saltar este paso
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/review-gate" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Si canProceedToReview = false → resolver cada blocker:
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "resolved", "resolution": "Descripción de cómo se resolvió"}'

# 2. Solo cuando canProceedToReview = true → ejecutar SKL-STATUS-02
```

---

## Template de entrega (todos los campos obligatorios — poner N/A si no aplica)

```markdown
## Entrega: $TASK_ID — $TASK_NAME

### Lo que se hizo:
$RESUMEN_TRABAJO
<!-- Concreto y específico: qué se creó, configuró, desplegó o corrigió -->

### Código:
- `$ARCHIVO_1` — $DESCRIPCION_1
- `$ARCHIVO_2` — $DESCRIPCION_2

### Development Log:
`knowledge/development-log/$FECHA_$TASK_ID_$SLUG.md`

### Code Logic:
- `knowledge/code-logic/$ARCHIVO_1.LOGIC.md`
- `knowledge/code-logic/$ARCHIVO_2.LOGIC.md`

### Criterios de aceptación:
| CA | Criterio | Resultado |
|----|----------|-----------|
| CA-1 | $CRITERIO_1 | ✅ / ❌ |
| CA-2 | $CRITERIO_2 | ✅ / ❌ |
<!-- N/A si la tarea no tenía CAs definidos en VTT -->

### Devlog entries registrados en VTT:
| Categoría | Severidad | Título | Estado |
|-----------|-----------|--------|--------|
| decision | — | $DECISION_TITULO | resolved |
| blocker | high | $BLOCKER_TITULO | resolved |
| improvement | medium | $MEJORA_TITULO | pending |
<!-- Listar todos los entries registrados durante la tarea.
     N/A si no se registró ninguno. -->

### Findings / Deuda técnica:
$FINDINGS
<!-- Issues de tech_debt, hardcode, riesgos detectados.
     Deben estar registrados como devlog-entries categoryCode=tech_debt o findings en VTT.
     N/A si no hay. -->

### ADRs tomados:
$ADRS
<!-- Decisiones de arquitectura registradas como devlog-entries categoryCode=decision
     o como TrackableItems typeCode=ADR en VTT.
     N/A si no hay. -->

### TrackableItems creados o vinculados:
$TRACKABLE_ITEMS
<!-- RFs, ADRs, User Stories, KPIs creados o vinculados a esta tarea.
     Formato: RF-001 "Nombre" — vinculado / ADR-003 "Nombre" — creado
     N/A si no aplica. -->

### Items detectados para trackeo (TL revisar):
<!-- Si no hay items, escribir: "Sin items detectados." -->
<!-- El TL decide si crear, si ya existe con otro código, y si aplica retroactividad. -->
<!-- Ver SOP-TRK-02 para el proceso de decisión del TL. -->

| Tipo sugerido | Código sugerido | Descripción breve | ¿Retroactivo? | Urgencia |
|--------------|-----------------|-------------------|---------------|----------|
| rnf/rf/adr/business_rule/tech_debt | NFR-XX / RF-XX / ADR-XX | Descripción del gap o decisión detectada | Sí / No | Alta / Media / Baja |

<!-- Retroactivo = Sí: el item puede afectar tareas ya realizadas (RFs, NFRs, BRs implementadas sin registrar) -->
<!-- Retroactivo = No: es una decisión o deuda que aplica desde ahora en adelante (ADRs, assumptions, tech_debt) -->

### Tareas derivadas generadas:
$TAREAS_DERIVADAS
<!-- Tareas nuevas creadas durante la ejecución (ej: $TASK_ID_NUEVO para DevOps).
     Incluir ID, asignado a quién, y motivo.
     N/A si no se generaron. -->

### Cómo verificar:
$PASOS_O_QUERY_VERIFICACION
<!-- Comandos curl, queries SQL, o pasos manuales para que el TL valide.
     Ser específico: URLs reales, parámetros reales, resultado esperado. -->

### Notas:
$NOTAS
<!-- Contexto relevante para el revisor: merge recovery, edge cases,
     limitaciones conocidas, dependencias con otras tareas.
     N/A si no hay. -->

### Review gate al entregar:
`canProceedToReview: true` — $NUM_ENTRIES entries totales, $NUM_RESOLVED resueltos, $NUM_WARNINGS warnings

### Commit:
`$COMMIT_TYPE [$TASK_ID]: $COMMIT_DESCRIPTION`
SHA: `$COMMIT_SHA`

### PR:
$PR_URL
```

---

## Uso — flujo de 3 pasos

### Paso 1 — Guardar reporte completo en archivo local (fuente de verdad)

```bash
# Ruta obligatoria
knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md

# Ejemplos:
# Memory Service: knowledge/agent-tasks/reports/04-development/S01/MS-293_REPORT.md
# VTT:            knowledge/agent-tasks/reports/S06-FIX-A/VTT-705_REPORT.md
```

Este archivo contiene el reporte **COMPLETO sin truncar**. Es la fuente de verdad que SKL-MANIFEST-01 leerá para incrustar en `skl_report_01_full` del JSON.

### Paso 2 — Postear extracto como comment en VTT

```bash
# VTT limita comments a 5000 chars. El reporte completo suele exceder este límite.
# Postear las primeras 8-10 líneas + link al archivo.
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "## Entrega: '"$TASK_ID"' - '"$TASK_NAME"'\n\n[primeras 8-10 lineas del reporte]\n\n**Reporte completo:** knowledge/agent-tasks/reports/<phase>/<sprint>/'"$TASK_ID"'_REPORT.md",
    "userId": "'"$AGENT_UUID"'"
  }'
```

### Paso 3 — SKL-MANIFEST-01 lee el archivo (no el comment)

El script de manifest hace:
```python
report_path = f"knowledge/agent-tasks/reports/<phase>/<sprint>/{TASK_ID}_REPORT.md"
with open(report_path, 'r', encoding='utf-8') as f:
    skl_report_01_full = f.read()   # completo, sin límite de chars
```

---

## Reglas

- Todos los campos del template son obligatorios. Usar `N/A` cuando no aplica — nunca omitir sección.
- El reporte completo SIEMPRE en archivo. El comment de VTT es solo un extracto navegable.
- Si el comment de VTT excede 5000 chars → 400 Bad Request. Por eso el extracto.
- El archivo se commitea al repo correspondiente (regla §Regla 7 de GUIA_WORKTREES).
