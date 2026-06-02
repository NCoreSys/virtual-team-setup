# VTT.WORKFLOW-HO-001.016 — Producir 9 Derivados del 3B.9

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.016` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.4.11 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 4 |

---

## 1. Propósito

TL produce los 9 derivados del 3B.9 (excluye 3B.9.3 que es pivote y 3B.9.10 que tiene workflow propio) según orden topológico: derivados directos primero, derivados compuestos después, síntesis final al cierre.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_breakdown_v1_4` | path | WORKFLOW-015 aprobado | sí | Pivote definitivo |
| `paquete_3b` | array<path> | FASE 2 | sí | Para 3B.9.5 (complejidad técnica) |
| `risk_register` | path | FASE 1 | sí | Para 3B.9.6 |
| `project_schedule` | path | FASE 1 | sí | Para 3B.9.8 + 3B.9.9 |

---

## 3. Precondiciones

- Task Breakdown v1.4 aprobado.
- Inputs de Fase 1 disponibles (schedule, risk register).

---

## 4. Reglas del Workflow

- **R1:** Cada subsección mantiene .md + .json sincronizados.
- **R2:** Orden topológico es no negociable.
- **R3:** Cada subsección pasa por REVMA antes de cerrarse.
- **R4:** 3B.9.1 se escribe AL FINAL (síntesis ejecutiva de las otras 9 subsecciones).

---

## 5. Pasos

### Paso 1 — Producir derivados directos (paralelo entre sí)

Estos 4 documentos solo necesitan 3B.9.3. Se pueden producir en paralelo.

| Subsección | Contenido |
|---|---|
| **3B.9.2 WBS** | Work Breakdown Structure jerárquico de los deliverables |
| **3B.9.5 Complexity Analysis** | Top deliverables HIGH/VERY HIGH con justificación técnica + matriz complejidad×rol |
| **3B.9.8 Migration & Rollout Plan** | Estrategia de despliegue por sprint con gates `GATE-S0X` |
| **3B.9.4 Dependency Map** | Grafo visual de dependencias (mermaid) con critical path destacado |

Por cada subsección: producir .md + .json + REVMA → firmado.

### Paso 2 — Producir derivados compuestos (orden dentro)

Estos necesitan 2+ subsecciones del Paso 1.

| Subsección | Inputs adicionales |
|---|---|
| **3B.9.6 Risk-Adjusted Estimates** | 3B.9.5 + Risk Register |
| **3B.9.9 Scheduling Inputs for PM** | 3B.9.4 + Project Schedule |
| **3B.9.7 Capacity Plan** | 3B.9.4 + 3B.9.9 (asignación por sprint con capacity por rol) |

Por cada subsección: producir .md + .json + REVMA → firmado.

### Paso 3 — Producir Routing Index 3B.9.10

→ invoca **`VTT.WORKFLOW-HO-001.017_producir_routing_index`**

### Paso 4 — Producir 3B.9.1 Scope Baseline (síntesis final)

Documento de cierre que consolida:
- Resumen ejecutivo del bloque
- Métricas globales (total horas, distribución por rol, sprints)
- Decisiones cerradas
- Referencias a las otras 9 subsecciones

→ invoca REVMA.

### Paso 5 — Marcar paquete 3B.9 completo

Las 10 subsecciones firmadas. .md + .json sincronizados en todas.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `3B.9.1` a `3B.9.10` (10 subsecciones) | .md + .json sincronizados | `_project-management/Fases/<BLOQUE>/` |

---

## 7. Validación

- 10 subsecciones existen y están firmadas.
- .md + .json sincronizados en TODAS.
- 3B.9.1 escrita al final (síntesis).
- 3B.9.10 cubre 100% de deliverables ✅ del 3B.9.3.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| 3B.9.1 escrita primero | Violación R4 | Reescribir al final |
| 3B.9.5 sin justificación técnica | Atajo | Justificar HIGH/VERY HIGH contra 3B.X |
| 3B.9.7 supera capacidad real | Sobre-planificación | Redistribuir entre sprints |
| .json desincronizado | Fallo manual | Re-ejecutar WORKFLOW-019 |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.001` (REVMA por cada subsección)
- `VTT.WORKFLOW-HO-001.017` (Routing Index)
- `VTT.WORKFLOW-HO-001.019` (sincronización JSON)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.016_producir_derivados_3b9.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
