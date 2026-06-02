# VTT.WORKFLOW-HO-001.025 — Analizar Scope por Sprint

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.025` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.6.2 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PJM |
| **Tipo** | [PROCESO] sub-procedimiento de análisis FASE 6 |

---

## 1. Propósito

PJM extrae del Implementation Plan el scope por sprint: deliverables asignados, roles activos, dependencias cross-sprint e intra-sprint, milestones. Es la base para producir SETUP, HANDOFFs y CLOSURE.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_breakdown_v1_4` | path (.md+.json) | WORKFLOW-015 | sí | Pivote |
| `capacity_plan_3b9_7` | path | WORKFLOW-016 | sí | Asignación por sprint |
| `dependency_map_3b9_4` | path | WORKFLOW-016 | sí | Critical path + paralelismo |
| `scheduling_inputs_3b9_9` | path | WORKFLOW-016 | sí | Gates y milestones |
| `routing_index_3b9_10` | path | WORKFLOW-017 | sí | Mapa deliverable → spec |

---

## 3. Precondiciones

- PJM recibió 6 artefactos (WORKFLOW-024 OK).
- Sprints están definidos en Capacity Plan.

---

## 4. Reglas del Workflow

- **R1:** Análisis se hace UNA vez para todo el bloque, no por sprint.
- **R2:** PJM no modifica el Implementation Plan (solo extrae y reorganiza para sprint).
- **R3:** Si encuentra inconsistencia → reporta al PM, no resuelve.

---

## 5. Pasos

### Paso 1 — PJM lee Capacity Plan

Para cada sprint S0X:
- Lista de deliverables asignados
- Total de horas por sprint
- Roles que entran al sprint

### Paso 2 — PJM construye matriz Sprint × Deliverable

Por cada sprint:
- Tabla con deliverables del sprint
- Por cada deliverable: ID, nombre, rol primario, horas, complejidad, dependencias (4 dimensiones), spec_source desde Routing Index

### Paso 3 — PJM identifica roles activos por sprint

Lista de roles que producen al menos un deliverable en cada sprint.

Ejemplos:
- S00 puede tener solo DO + TL (Setup).
- S01 puede tener BE + DB + TL + AR.
- S03 puede agregar FE + DL + UX si hay UI.

Esta lista define qué handoffs por rol genera el PJM en WORKFLOW-027.

### Paso 4 — PJM mapea dependencias cross-sprint

Por cada sprint S0X:
- Lista de tareas de S0X que dependen de tareas de S0(X-1) o anteriores
- Tipo de dependencia: técnica vs continuidad-rol vs gate

### Paso 5 — PJM identifica milestones por sprint

Del Scheduling Inputs (3B.9.9):
- Milestone de cada sprint (objetivo de cierre)
- Gates de release asociados (`GATE-S0X`)
- Criterios GO/NO-GO

### Paso 6 — PJM consolida en documento de análisis interno

PJM crea documento interno `ANALISIS_SCOPE_<BLOQUE>_PJM.md` con:
- Matriz Sprint × Deliverable
- Roles activos por sprint
- Dependencias cross-sprint
- Milestones por sprint

Este documento es input para WORKFLOWS-026/027/028.

### Paso 7 — PJM detecta inconsistencias

¿Encuentra alguna inconsistencia? Ejemplos:
- Deliverable asignado a sprint pero su dep_technical está en sprint posterior.
- Rol activo en sprint pero no hay deliverables para ese rol.
- Milestone sin criterios GO/NO-GO definidos.

Si hay inconsistencias → reporta al PM (no resuelve), suspende WORKFLOW hasta clarificación.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `ANALISIS_SCOPE_<BLOQUE>_PJM.md` | archivo .md (interno PJM) | `_project-management/Fases/<BLOQUE>/Sprints/` |

---

## 7. Validación

- Matriz Sprint × Deliverable completa.
- Roles activos por sprint identificados.
- Dependencias cross-sprint mapeadas.
- Milestones con criterios GO/NO-GO.
- Inconsistencias (si las hay) reportadas al PM.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| PJM modifica horas del Capacity Plan | Violación R2 | NO, reportar inconsistencia al PM |
| Deliverable con dep_technical en sprint posterior | Plan inconsistente | Reportar al PM, suspender |
| Rol declarado activo sin deliverables | Cadena mal mapeada | Reportar al PM |
| Milestone sin criterios | Plan incompleto | Reportar al PM |

---

## 9. Skills invocadas

- `VTT.SKILL-ATTACH-001`
- `VTT.SKILL-COMMENT-001` (si reporta inconsistencias)

---

**Documento:** `VTT.WORKFLOW-HO-001.025_analizar_scope_sprint.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
