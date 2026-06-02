# VTT.WORKFLOW-HO-001.027 — Producir HANDOFF_<ROL>_S[N]

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.027` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.6.5 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PJM |
| **Tipo** | [PROCESO] sub-procedimiento parametrizado por rol y sprint |

---

## 1. Propósito

PJM produce un HANDOFF por cada rol activo en cada sprint. La cantidad NO es fija — depende de qué roles están activos en el sprint específico. Sigue template canónico sin reinterpretar (`RULE-TEMPLATE-001`).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `analisis_scope` | path | WORKFLOW-025 | sí | Roles activos por sprint |
| `sprint_id` | string | iterador | sí | Sprint actual |
| `rol_activo` | enum | derivado de análisis | sí | TL / DL / FE / QA / etc. |
| `template_handoff_rol` | path | templates | sí | TEMPLATE_HANDOFF_<ROL>_v<X>.md |
| `metodologia_ejecucion_sprints` | path | metodologías | sí | METODOLOGIA_EJECUCION_SPRINTS_V1.1 |
| `routing_index` | path | FASE 4 | sí | 3B.9.10 para llenar Spec Source |

---

## 3. Precondiciones

- WORKFLOW-025 cerrado con roles activos identificados.
- Template del rol existe en `_project-management/templates/handoff/`.

---

## 4. Reglas del Workflow

- **R1:** Sigue template SIN reinterpretar (`RULE-TEMPLATE-001`).
- **R2:** Las 6 secciones obligatorias del final del handoff están presentes (Tareas / Dependencias / VTT Planning Data / Documentos Dinámicos / DoD / Gates).
- **R3:** Estado en header explícito: 🟢 READY o 🟠 BLOCKED con condición Y.
- **R4:** Tabla de tareas con columna "Spec Source (3B.9.10)" llenada desde Routing Index — NO inventar.
- **R5:** CAs verificables (no "funciona" sino "X retorna Y cuando Z").

---

## 5. Pasos

### Paso 1 — PJM abre template del rol

Lee `TEMPLATE_HANDOFF_<ROL>_v<X>.md` y conserva su estructura.

### Paso 2 — PJM rellena §0 Resumen Ejecutivo

- Objetivo del sprint para ese rol
- Horas estimadas para ese rol en ese sprint
- Roles ausentes en sprint (notas si aplica)

### Paso 3 — PJM determina estado de gate del handoff

¿El rol puede arrancar al inicio del sprint o espera condición?

- TL del sprint: 🟢 READY (arranca con SETUP)
- DL: 🟢 READY si UI nueva, arranca con diseños
- FE: 🟠 BLOCKED (espera APR-DL + BE in_review)
- QA: 🟠 BLOCKED (espera FE completado + DL-REVIEW)

Estado se declara en header del handoff.

### Paso 4 — PJM rellena §1 (contenido específico del rol)

Según rol:
- TL: Arquitectura del sprint, ADRs, dependencias externas
- DL: Pantallas a diseñar + flujo de navegación
- FE: Componentes a crear, contratos API a consumir
- QA: Estrategia de testing, escenarios BE/FE/E2E
- BE: Endpoints a implementar con contratos

### Paso 5 — PJM rellena §2 Briefs / Endpoints / Pantallas (específico del rol)

Estructura específica según rol. Incluye tablas, archivos a crear, CAs verificables.

### Paso 6 — PJM rellena §3 Variables de Entorno

Variables nuevas requeridas en ese sprint para ese rol.

### Paso 7 — PJM rellena §4 Riesgos del sprint para ese rol

Filtra del 3B.9.6 los riesgos relevantes al rol.

### Paso 8 — PJM rellena §5 Tareas del Sprint (tabla canónica)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría | Spec Source (3B.9.10) |
|---|---|---|---|---|---|---|

Filas: tareas del rol en ese sprint, con Spec Source LLENADA desde Routing Index (no inventada).

### Paso 9 — PJM rellena §6 Dependencias entre Tareas

Tabla FS (Finish-to-Start) + las 4 dimensiones cuando aplique.

### Paso 10 — PJM rellena §7 VTT Planning Data

Tabla lista para cargar al sistema VTT (estimatedHours, complexity, category, deliveryId, dependsOn).

### Paso 11 — PJM rellena §8 Documentos Dinámicos

Lista de docs que se actualizarán durante el sprint (API_CONTRACT, .LOGIC.md, etc.).

### Paso 12 — PJM rellena §9 DoD por rol

Checklist binario específico al rol.

### Paso 13 — PJM rellena §10 Gates de Aprobación

Tabla de gates: condición → acción → responsable.

### Paso 14 — PJM rellena §11 Referencias

Documentos cross-sprint, ADRs, etc.

### Paso 15 — PJM produce HANDOFF_<ROL>_S[N].md final

### Paso 16 — PJM produce HANDOFF_<ROL>_S[N].json sincronizado

→ invoca **`VTT.WORKFLOW-HO-001.019_producir_json_sincronizado`**

### Paso 17 — PJM ejecuta REVMA sobre el handoff

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`** con SA o PM Revisor.

Validación contra METODOLOGIA_EJECUCION_SPRINTS V1.1 (6 secciones obligatorias presentes, CAs verificables).

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `HANDOFF_<ROL>_S[N].md` | archivo .md | `_project-management/Fases/<BLOQUE>/Sprints/` |
| `HANDOFF_<ROL>_S[N].json` | archivo .json sincronizado | mismo lugar |

---

## 7. Validación

- Header con estado de gate explícito.
- Las 6 secciones canónicas presentes.
- Tabla de tareas con Spec Source llenada desde Routing Index.
- CAs verificables.
- VTT Planning Data con deliveryId.
- .md + .json sincronizados.
- REVMA aprobado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Falta estado de gate en header | Olvido | Agregar 🟢 READY o 🟠 BLOCKED |
| Spec Source inventado | Atajo | Copiar desde Routing Index |
| CA "el endpoint funciona" | No verificable | Reformular: "POST /memories retorna 201 con id" |
| §7 sin deliveryId | Violación R10 (SPRINT-001) | Agregar columna |
| Template alterado | Violación R1 | Restaurar template oficial |
| Handoff QA sin estado BLOCKED | Violación R3 | Marcar BLOCKED hasta FE completo |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.019` (sincronización JSON)
- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.027_producir_handoff_rol.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
