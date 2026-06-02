# VTT.WORKFLOW-HO-001.024 — Recopilar Inputs del PJM

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.024` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.6.1 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PJM |
| **Tipo** | [PROCESO] sub-procedimiento de inicio de FASE 6 |

---

## 1. Propósito

PJM verifica que recibió los 6 artefactos completos del paquete entregado por PM al cierre de FASE 5. Si falta alguno → NO genera nada, solicita al PM antes de arrancar (`RULE-PJM-NOGEN`).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `paquete_pm_pjm` | array<path> | FASE 5 | sí | 6 artefactos entregados por PM |

---

## 3. Precondiciones

- PJM fue notificado por PM (acuse de recibo).
- PJM tiene acceso al repo del proyecto.

---

## 4. Reglas del Workflow

- **R1:** Si falta UN input → NO generar nada (`RULE-PJM-NOGEN`).
- **R2:** PJM solicita inputs faltantes con nombre exacto al PM.
- **R3:** PJM no improvisa contenido para suplir inputs faltantes.

---

## 5. Pasos

### Paso 1 — PJM verifica los 6 artefactos

| # | Artefacto | Verificación |
|---|---|---|
| 1 | HO Maestro | `HO_PM_PJM_<BLOQUE>_IMPLEMENTACION_v<X>.md` existe |
| 2 | 3B.9 Implementation Plan | 10 subsecciones .md + .json sincronizados |
| 3 | Routing Index | `3B.9.10_ROUTING_INDEX_v<X>.md` + .json |
| 4 | Metodologías obligatorias | 5 docs presentes |
| 5 | Templates obligatorios | TEMPLATE_HANDOFF_<ROL>, TEMPLATE_SETUP, TEMPLATE_CLOSURE |
| 6 | Guías cross-sprint | CODE_REVIEW_GUIDE, TESTING_GUIDE, INTEGRATION_AUDIT_CHECKLIST |

### Paso 2 — PJM evalúa completitud

¿Los 6 artefactos están completos? → **[DECISIÓN]**
- **SÍ** → continuar a Paso 4.
- **NO** → ir a Paso 3.

### Paso 3 — PJM solicita faltantes al PM

PJM redacta solicitud con:
- Lista exacta de qué falta (nombre + ubicación esperada)
- Confirmación de que NO va a generar nada hasta recibirlos

→ invoca **`VTT.SKILL-COMMENT-001`** al PM.

PJM SUSPENDE FASE 6 hasta recibir respuesta.

### Paso 4 — PJM verifica consistencia interna

- ¿HO Maestro referencia mismos Task IDs que 3B.9.3?
- ¿Routing Index tiene cobertura 100% según WORKFLOW-023?

Si hay inconsistencias → reporta al PM (no improvisa).

### Paso 5 — PJM registra recepción

PJM emite acuse formal de recepción de los 6 artefactos.

→ invoca **`VTT.SKILL-COMMENT-001`** al PM.

PJM está listo para arrancar Paso 1 de WORKFLOW-025.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Acuse de recibo del PJM | comentario formal | VTT |
| (Si falta) solicitud de inputs | comentario formal | al PM |

---

## 7. Validación

- Los 6 artefactos verificados.
- Consistencia interna OK.
- Acuse formal emitido al PM.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| PJM genera sin algún input | Violación R1 | Suspender, solicitar |
| PJM improvisa para suplir | Violación R3 | Cancelar, solicitar al PM |
| PJM acusa recibo de paquete incompleto | Falta verificación | Re-verificar antes de acusar |

---

## 9. Skills invocadas

- `VTT.SKILL-COMMENT-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.024_recopilar_inputs_pjm.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
