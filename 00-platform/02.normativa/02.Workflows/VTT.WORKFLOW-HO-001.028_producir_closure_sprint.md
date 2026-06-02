# VTT.WORKFLOW-HO-001.028 — Producir CLOSURE_S[N]

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.028` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.6.6 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PJM |
| **Tipo** | [PROCESO] sub-procedimiento por sprint |

---

## 1. Propósito

PJM produce template de evidencia de cierre formal del sprint con firmas API (TL/AR/QA/DL si aplica), criterios GO/NO-GO del milestone, métricas estimado vs real.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `analisis_scope` | path | WORKFLOW-025 | sí | Análisis del sprint |
| `sprint_id` | string | iterador | sí | Sprint actual |
| `roles_activos` | array | derivado | sí | Determina cantidad de firmas |
| `template_closure` | path | templates | sí | TEMPLATE_CLOSURE canónico |
| `metodologia_cierre` | path | metodologías | sí | METODOLOGIA_CIERRE_SPRINT_FASE |
| `milestone_data` | objeto | 3B.9.9 §11 | sí | Criterios GO/NO-GO |

---

## 3. Precondiciones

- WORKFLOW-025 cerrado.
- Roles activos del sprint identificados.

---

## 4. Reglas del Workflow

- **R1:** Firmas con comando API real, no checklist en papel (`RULE-VTT-005`).
- **R2:** APR-S[N] es tarea formal en VTT (no solo texto).
- **R3:** Cantidad de firmas según roles activos:
   - Sprint sin FE: TL + AR + QA (3 firmas)
   - Sprint con FE: TL + AR + QA + DL (4 firmas)
   - Justificación en §0 si <4 firmas.
- **R4:** Estados válidos para tareas de cierre: `task_draft` → `task_ready` → `task_in_progress` → `task_completed`. NUNCA `task_approved` para tareas de cierre.

---

## 5. Pasos

### Paso 1 — PJM abre template canónico

Lee `TEMPLATE_CLOSURE_S[N].md` y preserva estructura.

### Paso 2 — PJM rellena §0 con cantidad de firmas

Si sprint tiene FE → 4 firmas (TL+AR+QA+DL).
Si no → 3 firmas (TL+AR+QA) + justificación de ausencia de DL.

### Paso 3 — PJM rellena §1 Resumen

Métricas esperadas del sprint, Deliveries VTT que corresponden.

### Paso 4 — PJM rellena §2 Verificación de Deliverables (por Delivery)

Tabla por Delivery del sprint con check ☐ por cada CA.

NO por tarea suelta — por Delivery.

### Paso 5 — PJM rellena §3 Firma TL - Code Review

Criterios + comando API:
```
POST /sprints/{id}/stages/development/sign
{ userId, role: "TL", comment }
```

### Paso 6 — PJM rellena §4 Firma AR - Integration Audit

Criterios + comando API stage integration.

### Paso 7 — PJM rellena §5 Firma DL - Visual Review (solo si FE)

Criterios + comando API stage design.

Si sprint sin FE → omitir §5 + justificar en §0.

### Paso 8 — PJM rellena §6 Milestone M[N] - Criterios GO/NO-GO

Del 3B.9.9 §11, milestone correspondiente al sprint.

### Paso 9 — PJM rellena §7 Métricas Finales

Tabla estimado vs real vs varianza por rol.

(El TL llenará con valores reales al cerrar sprint en `ASG-001`.)

### Paso 10 — PJM rellena §8 Gate Final PM Sign-off

Checklist de condiciones que PM verifica antes de firmar APR-S[N].

### Paso 11 — PJM rellena §9 Proceso de Cierre

Tabla de firmas secuenciales + APR en VTT.

### Paso 12 — PJM rellena §10 Firmas de Cierre

Tabla ☐ con fecha (llenable por los firmantes durante ejecución).

### Paso 13 — PJM rellena §11 Referencias

### Paso 14 — PJM produce CLOSURE_S[N].md final

### Paso 15 — PJM produce CLOSURE_S[N].json sincronizado

→ invoca **`VTT.WORKFLOW-HO-001.019`**

### Paso 16 — PJM ejecuta REVMA sobre CLOSURE

→ invoca **`VTT.WORKFLOW-HO-001.001`** con SA o PM Revisor.

Validación contra METODOLOGIA_CIERRE_SPRINT_FASE (firmas API reales, APR formal).

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `CLOSURE_S[N].md` | archivo .md | `_project-management/Fases/<BLOQUE>/Sprints/` |
| `CLOSURE_S[N].json` | archivo .json sincronizado | mismo lugar |

---

## 7. Validación

- §0 con cantidad de firmas justificada.
- §2 verificación por Delivery, no por tarea.
- §3, §4 con comandos API reales.
- §5 presente si FE, ausente con justificación si no.
- §6 con criterios GO/NO-GO del milestone.
- §10 tabla de firmas con fecha (llenable).
- .md + .json sincronizados.
- REVMA aprobado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Firmas sin comando API | Violación R1 | Agregar POST a stage signature |
| APR-S[N] como texto, no tarea | Violación R2 | Crear como tarea formal en SETUP |
| Sprint con FE sin firma DL | Violación R3 | Agregar §5 |
| Tarea cierre con estado `task_approved` | Violación R4 | Solo `task_completed` |
| Verificación por tarea, no por Delivery | Diseño incorrecto | Reagrupar por Delivery |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.019` (sincronización JSON)
- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.028_producir_closure_sprint.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
