# VTT.SKILL-REPORT-002 — Reporte ejecutivo PJM al PM

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-REPORT-002` |
| **Categoría** | REPORT |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | PJM (Project Manager) |
| **Tokens estimados** | ~200 |
| **Cuándo se usa** | Diario o al cierre de sprint — reporte ejecutivo del PJM hacia el PM |
| **Reemplaza** | `SKL-REPORT-02_reporte-pjm.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `fecha` | YYYY-MM-DD | sí | Fecha del reporte |
| `project_id` | uuid | sí | UUID del proyecto |
| `avance_por_fase` | array | sí | Output de `VTT.SKILL-QUERY-004` |
| `blockers_activos` | array | sí | Tareas en `task_on_hold` con metadata |
| `pendientes_review_48h` | array | sí | Tareas en `task_in_review` por >48h |
| `proxima_oleada` | array (max 3) | sí | Tareas a asignar próximamente |
| `recomendacion` | string | sí | Análisis y recomendación del PJM |

---

## Precondición

- Ejecutar `VTT.SKILL-QUERY-004` antes — provee datos de avance por fase
- Tener listado de tareas activas — `VTT.SKILL-QUERY-002`

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$PROJECT_ID
```

---

## Regla LL-001 (una tarea por agente)

La sección "Próxima oleada a asignar" tiene un **máximo de 3 tareas** porque cada agente toma 1 tarea por vez. Si el equipo tiene 3 agentes activos → máximo 3 candidatas.

---

## Template del reporte

```markdown
## Reporte Ejecutivo PJM — <FECHA>

### % Avance por Fase

| Fase | Total | Completadas | % |
|------|------:|------------:|---:|
| Setup | <N> | <N> | <%> |
| Discovery | <N> | <N> | <%> |
| Planning | <N> | <N> | <%> |
| Analysis | <N> | <N> | <%> |
| Design | <N> | <N> | <%> |
| Development | <N> | <N> | <%> |
| Testing | <N> | <N> | <%> |
| Deploy | <N> | <N> | <%> |

**Total proyecto:** <N>/<N> (<%>)

### Blockers activos: <N>

| TASK_ID | Título | Owner | Tiempo en hold | Causa |
|---|---|---|---|---|
| <MS-XXX> | <título> | <agente> | <Xh> | <issue title> |

### En revisión >48h sin acción TL: <N>

| TASK_ID | Título | Agente que entregó | Tiempo en review |
|---|---|---|---|
| <MS-XXX> | <título> | <agente> | <Xh> |

### Próxima oleada a asignar (max 3 — regla LL-001):

| Orden | TASK_ID | Título | Agente sugerido |
|------:|---|---|---|
| 1 | <MS-XXX> | <título> | <ROL> |
| 2 | <MS-XXX> | <título> | <ROL> |
| 3 | <MS-XXX> | <título> | <ROL> |

### Recomendación del PJM:

<ANÁLISIS Y RECOMENDACIÓN>

### Riesgos identificados (opcional):

- <riesgo 1>
- <riesgo 2>

### Métricas adicionales (opcional):

- Velocidad sprint actual: <N> tareas/semana
- Tareas creadas vs aprobadas: <N>/<N>
- Deuda técnica acumulada: <N> items
```

---

## Ejecución

### Paso 1 — Generar el reporte localmente

```bash
REPORT_PATH="knowledge/reports/pjm/$(date +%Y-%m-%d)_reporte_pjm.md"
mkdir -p "$(dirname "$REPORT_PATH")"

# Recopilar datos
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/phases" -H "Authorization: Bearer $TOKEN" > /tmp/phases.json
curl -s "$VTT_BASE_URL/api/tasks?projectId=$PROJECT_ID&status=task_on_hold" -H "Authorization: Bearer $TOKEN" > /tmp/blockers.json
curl -s "$VTT_BASE_URL/api/tasks?projectId=$PROJECT_ID&status=task_in_review" -H "Authorization: Bearer $TOKEN" > /tmp/review.json

# Generar el archivo con el template arriba (llenar manualmente o con script)
# El PJM completa la sección de Recomendación
```

### Paso 2 — Entregar al PM

Opciones para entregar:

**Opción A — Comment en tarea de coordinación PJM↔PM:**

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/<TASK_COORDINACION_ID>/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$(python -c "
import json
with open('$REPORT_PATH') as f:
    content = f.read()
print(json.dumps({'message': content, 'userId': '$PJM_UUID', 'type': 'report'}))
")"
```

**Opción B — Mensaje directo al PM** (si no hay tarea de coordinación):

Pegar el contenido del reporte directamente en el canal de comunicación PM↔PJM acordado.

---

## Validación

```bash
# Verificar que el reporte tiene todas las secciones
SECTIONS="% Avance por Fase|Blockers activos|En revisión|Próxima oleada|Recomendación"
grep -E "^### ($SECTIONS)" "$REPORT_PATH" | wc -l
# Esperado: 5
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Más de 3 tareas en próxima oleada | Falta regla LL-001 | Acotar a 3 — más entran en backlog del próximo reporte |
| % Avance solo cuenta `task_completed` (no `task_approved`) | Cálculo incompleto | Sumar ambos status |
| Sin sección de recomendación | El PJM solo copió datos | El reporte es **ejecutivo** — el PM espera análisis del PJM, no solo numeros |
| Blockers sin causa | Falta lectura del issue | Hacer `GET /tasks/<id>/issues` para cada `task_on_hold` |
| Reporte sin fecha | Olvido | Header `# Reporte ... <FECHA>` obligatorio |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-QUERY-004` — avance por fases
- `VTT.SKILL-QUERY-002` — tareas en review del proyecto
- `VTT.SKILL-COMMENT-001` — para postear el reporte (Opción A)

---

## Skills que invocan ESTA

- Rutina diaria del PJM
- Workflow de cierre de sprint

---

## Cuándo NO usar esta Skill

- **Si es reporte de entrega de tarea** (no ejecutivo) — usar `VTT.SKILL-REPORT-001`
- **Si solo querés el % de avance bruto** — `VTT.SKILL-QUERY-004` directo

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-REPORT-02_reporte-pjm.md`. Ampliación: template estructurado con 6+2 secciones (5 obligatorias + 2 opcionales). Regla LL-001 documentada (max 3 tareas en próxima oleada). |
