# VTT.WORKFLOW-HO-001.013 — Consolidar PAQUETE_TRAZABILIDAD_BLOQUE

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.013` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.3.6 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PM |
| **Tipo** | [PROCESO] sub-procedimiento de cierre FASE 3 |

---

## 1. Propósito

PM consolida todos los dictámenes y reviews emitidos en FASE 3 en un único documento que sirve como evidencia de validación cross-rol del paquete técnico. Input para FASE 4.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `dictamen_be` | path | WORKFLOW invocado por BE | sí | DICTAMEN_BE firmado |
| `dictamen_db` | path | WORKFLOW invocado por DB | sí | DICTAMEN_DB firmado |
| `dictamen_tl` | path | WORKFLOW invocado por TL | sí | DICTAMEN_TL firmado |
| `review_ar` | path | WORKFLOW-011 | sí | REVIEW_AR_CROSS_MODULE firmado |
| `revision_sa` | path | WORKFLOW-012 | no | REVISION_SA_FUNCIONAL firmada (si SA en cadena) |
| `template_paquete_trazabilidad` | path | templates | sí | Template canónico |

---

## 3. Precondiciones

- Todos los dictámenes y reviews obligatorios firmados.
- PM tiene visibilidad de hallazgos abiertos vs cerrados.

---

## 4. Reglas del Workflow

- **R1:** PAQUETE_TRAZABILIDAD consolida, NO interpreta. Cada hallazgo se cita textual del documento origen.
- **R2:** Hallazgos bloqueantes deben estar RESUELTOS antes de cerrar FASE 3. Si quedan abiertos → FASE 3 NO cierra.
- **R3:** Hallazgos menores quedan como DEUDA DOCUMENTADA con plan de resolución (en FASE 4 o bloque siguiente).
- **R4:** Documento es input obligatorio de FASE 4 — TL lo lee antes de iniciar Task Breakdown.

---

## 5. Pasos

### Paso 1 — PM recopila los dictámenes y reviews

Verifica que todos los documentos requeridos están firmados.

Si falta alguno → cancela este workflow, regresa al workflow del rol faltante.

### Paso 2 — PM extrae hallazgos de cada documento

Por cada dictamen/review:
- Lista de hallazgos
- Severidad de cada uno
- Estado (abierto / cerrado / diferido)

### Paso 3 — PM clasifica hallazgos según resolución

| Categoría | Acción |
|---|---|
| Bloqueante CERRADO | Solo registrar para trazabilidad |
| Bloqueante ABIERTO | FASE 3 no cierra — escalar al rol responsable |
| Mayor cerrado | Registrar para trazabilidad |
| Mayor abierto | Documentar como DEUDA con plan de resolución |
| Menor | Documentar como diferido o aceptado |

### Paso 4 — PM redacta PAQUETE_TRAZABILIDAD_BLOQUE

Estructura del documento:
- Resumen ejecutivo (estado del paquete técnico)
- Cuadro síntesis: dictamen / firmante / fecha / estado
- Sección por dictamen con resumen + hallazgos
- Cuadro de hallazgos abiertos (con plan de resolución)
- Decisiones cerradas referenciadas a SPEC (D-XX-NN)
- Routing pre-3B.9: qué información debe alimentar a FASE 4

### Paso 5 — PM firma y entrega como input a FASE 4

Documento: `PAQUETE_TRAZABILIDAD_<BLOQUE>_v1.0.md`

PM notifica al TL que FASE 4 puede arrancar con el paquete técnico + trazabilidad consolidados.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `PAQUETE_TRAZABILIDAD_<BLOQUE>_v1.0.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |

---

## 7. Validación

- Todos los dictámenes obligatorios citados.
- Hallazgos clasificados (bloqueante/mayor/menor + abierto/cerrado/diferido).
- Hallazgos bloqueantes: 0 abiertos.
- Plan de resolución para hallazgos abiertos.
- Decisiones cerradas referenciadas a SPEC.
- Firma PM presente.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Hallazgo bloqueante registrado como cerrado sin evidencia | Optimismo | Verificar resolución antes de cerrar FASE 3 |
| Deuda documentada sin plan | Procrastinación | Forzar plan con fecha o sprint objetivo |
| Hallazgos no clasificados | Trabajo incompleto | Clasificar todos antes de firmar |
| Dictamen pendiente y FASE 3 cierra | Violación R1 | Bloquear cierre hasta tener todos los dictámenes |

---

## 9. Skills invocadas

- `VTT.SKILL-ATTACH-001`
- `VTT.SKILL-COMMENT-001` (notificar al TL)

---

**Documento:** `VTT.WORKFLOW-HO-001.013_consolidar_paquete_trazabilidad.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
