# VTT.WORKFLOW-HO-001.023 — Validar Gate Duro del Routing Index

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.023` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.5.3 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PM |
| **Tipo** | [PROCESO] sub-procedimiento de validación crítica |

---

## 1. Propósito

PM ejecuta validación del Routing Index al inicio de FASE 5. Si falta una fila → DEVUELVE al TL (no completa manualmente). Es el gate más crítico del Protocol.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_breakdown_v1_4` | path | WORKFLOW-015 | sí | Pivote del 3B.9 |
| `routing_index_v1_0` | path | WORKFLOW-017 | sí | 3B.9.10 |

---

## 3. Precondiciones

- Task Breakdown v1.4 firmado.
- Routing Index v1.0 firmado.

---

## 4. Reglas del Workflow

- **R1:** Cobertura 100% — toda fila de Task Breakdown con ✅ debe tener fila correspondiente en Routing Index (`RULE-HO-001`).
- **R2:** Si falta UNA fila → DEVUELVE al TL.
- **R3:** PM NO completa manualmente las filas faltantes.
- **R4:** Routing Index NO se puede emitir parcial.

---

## 5. Pasos

### Paso 1 — PM carga ambos archivos

PM lee:
- `3B.9.3_TASK_BREAKDOWN_v1.4.json` → lista de `task_id` con `aplica = ✅`.
- `3B.9.10_ROUTING_INDEX_v1.0.json` → lista de `deliverable_id`.

### Paso 2 — PM ejecuta diff entre los dos conjuntos

Conjunto A = Task IDs ✅ del Task Breakdown.
Conjunto B = Deliverable IDs del Routing Index.

Diferencias buscadas:
- `A - B` = Task IDs ✅ que NO están en Routing Index → **FALTAN filas**.
- `B - A` = Deliverable IDs en Routing Index que NO son ✅ → **filas extra** (también es error).

### Paso 3 — PM evalúa resultado

¿`A - B` está vacío AND `B - A` está vacío? → **[DECISIÓN]**
- **SÍ** → Gate aprobado, continuar a Paso 5.
- **NO** → Gate falla, ir a Paso 4.

### Paso 4 — PM DEVUELVE al TL

PM redacta mensaje al TL listando:
- Task IDs ✅ que faltan en Routing Index (de `A - B`).
- Deliverable IDs en Routing Index que NO deberían estar (de `B - A`).

PM marca FASE 5 como SUSPENDIDA hasta que TL emita Routing Index v1.1 con cobertura 100%.

→ invoca **`VTT.SKILL-COMMENT-001`** al TL.

WORKFLOW termina con resultado FALLO.

### Paso 5 — PM valida calidad de cada fila

Para cada fila del Routing Index:
- ¿`spec_source` cita doc 3B real (verificar existencia)?
- ¿`seccion` es específica (no solo "completo" salvo justificación)?
- ¿`docs_para_agente` tiene 2-5 entradas razonables?
- ¿`decisiones_aplicables` referencia ADRs existentes en 3B.6?

Si alguna fila falla → reportar al TL como observación menor (no bloquea, se corrige en v1.1 o queda como deuda).

### Paso 6 — PM emite veredicto

| Veredicto | Acción |
|---|---|
| Cobertura 100% + calidad OK | Aprobado, FASE 5 continúa |
| Cobertura 100% + calidad con observaciones menores | Aprobado con observaciones, FASE 5 continúa |
| Cobertura <100% | DEVUELTO al TL, FASE 5 suspendida |

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Veredicto (APROBADO/DEVUELTO) | sección en bitácora FASE 5 | DECISION_BLOQUE |
| Lista de faltantes (si DEVUELTO) | mensaje al TL | comentario VTT |

---

## 7. Validación

- Diff ejecutado correctamente sobre ambos JSONs.
- Veredicto registrado.
- Si DEVUELTO → mensaje al TL emitido.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| PM completa filas faltantes manualmente | Violación R3 | DEVOLVER al TL siempre |
| PM emite HO Maestro con Routing Index parcial | Violación R4 | Cancelar emisión |
| Diff impreciso (solo cuenta filas, no compara IDs) | Implementación pobre | Comparar conjuntos por ID, no por cantidad |
| Calidad de filas no validada | Falta de rigor | Aplicar Paso 5 siempre |

---

## 9. Skills invocadas

- `VTT.SKILL-COMMENT-001` (si DEVUELTO)

---

**Documento:** `VTT.WORKFLOW-HO-001.023_validar_gate_routing_index.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
