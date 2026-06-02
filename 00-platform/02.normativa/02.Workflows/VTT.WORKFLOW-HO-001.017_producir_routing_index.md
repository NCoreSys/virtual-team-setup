# VTT.WORKFLOW-HO-001.017 — Producir Routing Index 3B.9.10

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.017` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.4.12 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL |
| **Tipo** | [PROCESO] sub-procedimiento crítico de FASE 4 |

---

## 1. Propósito

TL produce 3B.9.10 Routing Index — mapa de cada deliverable ✅ a su spec source (5 columnas obligatorias). Sin él, FASE 5 NO puede emitir HO Maestro (gate duro).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_breakdown_v1_4` | path | WORKFLOW-015 | sí | Pivote con todos los deliverables ✅ |
| `paquete_3b` | array<path> | FASE 2 | sí | 8 docs 3B.X (para mapear spec_source) |
| `template_routing_index` | path | templates | sí | Template canónico |

---

## 3. Precondiciones

- Task Breakdown v1.4 firmado.
- Los 8 documentos 3B.X disponibles.

---

## 4. Reglas del Workflow

- **R1:** Las 5 columnas son obligatorias, no negociables.
- **R2:** Cobertura 100% — toda fila de Task Breakdown con ✅ debe tener fila correspondiente en Routing Index.
- **R3:** Spec Source NO se inventa — siempre cita doc 3B real (`RULE-HO-002`).
- **R4:** Sección NO es genérica — cita sección específica del doc 3B para que el agente no lea todo.
- **R5:** Docs para el agente: 2-5 docs por fila (ahorro de tokens downstream).
- **R6:** Decisiones aplicables: lista de D-XX-NN que el agente debe respetar.

---

## 5. Pasos

### Paso 1 — TL extrae lista de deliverables ✅ del Task Breakdown

Lee `3B.9.3_TASK_BREAKDOWN_v1.4.json`, filtra `aplica = ✅`.

### Paso 2 — Por cada deliverable, identifica spec_source

TL lee el deliverable y determina:
- ¿En qué documento 3B está su spec técnica?
- ¿En qué sección específica?

Ejemplo:
- Deliverable `4.2.1 Initial Migration` → Spec Source: `3B.3_DATABASE_DESIGN.md` → Sección: `§4 Schema + §5 Migration Strategy`.

### Paso 3 — Identifica decisiones aplicables

Por cada deliverable, lista las D-XX-NN (de 3B.6 ADRs) que aplican:
- Ej. `4.3.7 Middlewares` → `D-MEM-26 (auth strategy), D-MEM-09 (rate limiting)`.

### Paso 4 — Identifica docs para el agente

Lista de 2-5 documentos que el agente ejecutor debe leer para esa tarea concreta:
- Spec source principal
- Docs adyacentes (3B.X cross-referenciados)
- Si camino C: documento `actual_*` correspondiente
- Addendums si aplican

### Paso 5 — TL produce 3B.9.10 v1.0 en .md

Tabla con 5 columnas obligatorias por cada deliverable ✅:

| Deliverable ID | Nombre | Spec Source | Sección | Docs para el agente |
|---|---|---|---|---|
| 4.2.1 | Initial Migration | 3B.3_DATABASE_DESIGN.md | §4, §5 | 3B.3, 3B.8 |

(Decisiones aplicables se incluyen como columna adicional o anexo.)

### Paso 6 — TL produce 3B.9.10 v1.0 en .json sincronizado

Schema canónico:
```json
{
  "deliverable_id": "4.3.1",
  "nombre": "API Endpoints",
  "spec_source": "3B.4_API_DESIGN.md",
  "seccion": "§endpoints — 11 endpoints, SLA <500ms",
  "decisiones_aplicables": ["D-XXX-07", "D-XXX-05"],
  "docs_para_agente": ["3B.4", "3B.4.1", "3B.4.3", "3B.5.3", "3B.2.1"]
}
```

### Paso 7 — TL valida cobertura 100%

¿Cada deliverable ✅ del Task Breakdown tiene fila en Routing Index?

Si falta UNO → completar antes de continuar.

### Paso 8 — TL ejecuta REVMA sobre 3B.9.10

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`**

PM Revisor valida que cada Spec Source efectivamente contiene la sección citada (sin alucinación).

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `3B.9.10_ROUTING_INDEX_v1.0.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |
| `3B.9.10_ROUTING_INDEX_v1.0.json` | archivo .json sincronizado | mismo lugar |

---

## 7. Validación

- 5 columnas obligatorias presentes en cada fila.
- Cobertura 100% deliverables ✅.
- Spec_source cita documento 3B real (verificable).
- Sección específica (no "completo" salvo justificación).
- Docs para el agente: 2-5 por fila.
- .md + .json sincronizados.
- REVMA aprobado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Cobertura <100% | Olvido | Completar antes de FASE 5 |
| Spec_source inventado | Atajo | Verificar contra doc 3B real, corregir |
| Sección genérica "completo" sin justificación | Pereza | Citar sección específica |
| Docs para el agente: 10+ por fila | No se filtró | Reducir a 2-5 esenciales |
| `D-XX-NN` que no existe en 3B.6 | Error | Verificar contra ADRs reales |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.WORKFLOW-HO-001.019` (sincronización JSON)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.017_producir_routing_index.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
