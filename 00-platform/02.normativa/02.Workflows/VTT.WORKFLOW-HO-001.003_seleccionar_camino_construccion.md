# VTT.WORKFLOW-HO-001.003 — Seleccionar Camino de Construcción (A/B/C)

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.003` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.0.3 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PM |
| **Tipo** | [DECISIÓN] sub-procedimiento de selección |

---

## 1. Propósito

Determinar qué camino se sigue para producir el paquete técnico fundacional según los inputs disponibles: A (sin SPEC), B (con SPEC consolidada), C (feature en sistema operando con repo existente).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `metodologia_path` | path | FASE 0 | sí | METODOLOGIA borrador o aprobada |
| `spec_path` | path | FASE 0 | no | SPEC consolidada (si existe) |
| `repo_existente` | path | configuración del proyecto | no | Path al repo si feature opera sobre código vivo |
| `tipo_feature` | enum | análisis PM | sí | `nueva` / `refactor` / `feature_en_sistema_operando` |

---

## 3. Precondiciones

- PM tiene visibilidad de qué documentación existe.
- PM conoce el contexto del proyecto (es nuevo, está operando, etc.).

---

## 4. Reglas del Workflow

- **R1:** Camino A solo aplica si NO hay SPEC consolidada (caso raro en VTT operativo).
- **R2:** Camino B aplica cuando hay SPEC pero el sistema NO está operando todavía.
- **R3:** Camino C aplica SIEMPRE que haya repo con código vivo, aunque haya SPEC.
- **R4:** Si dudas entre B y C → elegir C (es más robusto, captura estado real del código).

---

## 5. Pasos

### Paso 1 — PM verifica disponibilidad de SPEC consolidada

¿Existe `spec_path` con SPEC aprobada o en borrador maduro? → **[DECISIÓN]**
- **NO** → Camino A (saltar al Paso 4 — Camino A).
- **SÍ** → continuar a Paso 2.

### Paso 2 — PM verifica si hay repo con código vivo

¿Existe `repo_existente` con código que la feature modifica/extiende? → **[DECISIÓN]**
- **NO** → Camino B (saltar al Paso 5 — Camino B).
- **SÍ** → Camino C (saltar al Paso 6 — Camino C).

### Paso 3 — (No usado, slot reservado)

### Paso 4 — Camino A — Configuración

PM registra en DECISION_BLOQUE:
- Camino: A (sin SPEC)
- Inputs requeridos en FASE 2: 16 docs de Fase 1+2 SDLC + ANALISIS_FASES_COMPLETO
- Workflows que se activan: producción manual de cada 3B.X desde análisis SDLC formal

Advertencia: este camino implica esfuerzo significativo en FASE 2 (producir docs Fase 1+2 si no existen).

### Paso 5 — Camino B — Configuración

PM registra en DECISION_BLOQUE:
- Camino: B (con SPEC consolidada)
- Inputs requeridos en FASE 2: SPEC + METODOLOGIA + ANALISIS_FASES_COMPLETO + Project Schedule + Risk Register
- Workflows que se activan: producción de 3B.X usando SPEC como fuente única (sin pista de análisis de repo)

### Paso 6 — Camino C — Configuración

PM registra en DECISION_BLOQUE:
- Camino: C (feature en sistema operando)
- Inputs requeridos en FASE 2: SPEC + METODOLOGIA + ANALISIS_FASES_COMPLETO + repo existente
- Workflows que se activan en paralelo:
  - **Pista A** — `WORKFLOW-HO-001.005_extraccion_desde_spec` (genera docs 3B sintéticos)
  - **Pista B** — `WORKFLOW-HO-001.006_analisis_repo_actual` (genera docs `3B.X_actual_*`)
- Las 2 pistas convergen en FASE 2.5.x para producir 3B.X finales

### Paso 7 — PM registra decisión en DECISION_BLOQUE

PM actualiza `DECISION_BLOQUE_<NOMBRE>_v1.0.md` con la decisión final y la justificación.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Decisión de camino registrada | sección en DECISION_BLOQUE | `_project-management/Fases/<BLOQUE>/` |
| Lista de inputs requeridos en FASE 2 | sección en DECISION_BLOQUE | mismo doc |

---

## 7. Validación

- DECISION_BLOQUE tiene sección "Camino elegido" con A/B/C explícito.
- Lista de inputs requeridos en FASE 2 está completa según el camino.
- Justificación de la decisión está documentada.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Se eligió B pero el repo tiene código vivo que la feature modifica | No se aplicó R3 | Cambiar a Camino C |
| Camino A elegido sin tener los 16 docs Fase 1+2 | Inputs insuficientes | Cambiar a B si hay SPEC, o producir Fase 1+2 primero |

---

## 9. Skills invocadas

(Ninguna — es decisión del PM)

---

**Documento:** `VTT.WORKFLOW-HO-001.003_seleccionar_camino_construccion.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
