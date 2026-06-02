# VTT.WORKFLOW-HO-001.018 — Calibrar Estimaciones con Velocity Histórica

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.018` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.4.13 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL |
| **Tipo** | [PROCESO] sub-procedimiento de calibración de FASE 4 |

---

## 1. Propósito

Si existe velocity histórica del proyecto/equipo, TL ajusta las estimaciones del Task Breakdown aplicando el FV (Factor de Velocity) por tipo de deliverable. Si no existe, se marca como "primera iteración sin calibración".

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_breakdown_actual` | path | WORKFLOW-014 v1.0 o WORKFLOW-015 | sí | Versión del breakdown a calibrar |
| `velocity_historica` | path | proyecto (puede no existir) | no | VELOCITY_HISTORICA_<PROYECTO>.md |

---

## 3. Precondiciones

- Task Breakdown existe con estimaciones base (horas + complejidad).
- Si velocity histórica existe, está actualizada con cierres recientes.

---

## 4. Reglas del Workflow

- **R1:** Si no hay velocity histórica → no aplicar ajuste, marcar como "primera iteración".
- **R2:** Si hay velocity con <5 muestras del tipo de deliverable → no ajustar (insuficiente estadísticamente).
- **R3:** FV se aplica por TIPO de deliverable (README, Endpoint REST MEDIUM, Migración DB, etc.), no globalmente.
- **R4:** Si proyecto tiene características muy distintas (stack distinto, dominio distinto) → no aplicar.
- **R5:** Ajuste se documenta en cada celda modificada (registrar valor original + FV + valor ajustado).

---

## 5. Pasos

### Paso 1 — TL verifica disponibilidad de velocity histórica

¿Existe `VELOCITY_HISTORICA_<PROYECTO>.md`? → **[DECISIÓN]**
- **NO** → marcar Task Breakdown como "primera iteración sin calibración", saltar a Paso 6.
- **SÍ** → continuar a Paso 2.

### Paso 2 — TL lee FV por tipo de deliverable

De velocity histórica extrae:
- FV por tipo de deliverable (`Endpoint REST MEDIUM` → 0.84, `Migración DB` → 1.19, etc.)
- Número de muestras por tipo

### Paso 3 — TL clasifica cada deliverable del breakdown por tipo

Por cada deliverable del breakdown actual, asigna tipo (mismo vocabulario que velocity histórica).

### Paso 4 — TL aplica ajuste donde corresponde

Por cada deliverable:
- Si tipo tiene FV con ≥5 muestras → ajustar horas: `horas_ajustadas = horas_originales × FV`.
- Si tipo tiene <5 muestras → no ajustar, marcar como "sin calibración suficiente".
- Si proyecto es distinto significativamente → no ajustar, marcar como "calibración no aplicable".

### Paso 5 — TL documenta cambios

Por cada celda ajustada, agrega comentario inline:
```
8h (original) → ajuste FV=0.84 → 6.7h
```

### Paso 6 — TL produce versión incrementada del Task Breakdown

Si hubo ajustes → emite siguiente versión (v1.0 → v1.0.calibrated, o se incorpora a la siguiente versión natural v1.1).

Si no hubo ajustes → marca el documento con sello "primera iteración" y mantiene versión.

### Paso 7 — TL notifica a PM

PM debe estar al tanto del ajuste agregado (impacta totales del bloque).

→ invoca **`VTT.SKILL-COMMENT-001`**.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Task Breakdown calibrado | .md + .json sincronizados | misma ubicación |
| Sello "primera iteración" o cambios documentados | metadata en doc | mismo doc |

---

## 7. Validación

- Cada celda ajustada tiene comentario con original + FV + ajustado.
- Tipos con <5 muestras no se ajustaron.
- Totales recalculados son coherentes (suma de horas ajustadas).

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Se aplicó FV globalmente | Violación R3 | Recalcular por tipo |
| Se ajustó con 2 muestras | Violación R2 | Revertir, marcar como insuficiente |
| Proyecto nuevo con stack distinto se calibró | Violación R4 | Revertir, marcar "no aplicable" |
| Sin velocity histórica pero TL inventó FV | Atajo peligroso | NO. Marcar primera iteración |

---

## 9. Skills invocadas

- `VTT.SKILL-COMMENT-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.018_calibrar_con_velocity.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
