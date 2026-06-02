# VTT.WORKFLOW-HO-001.026 — Producir SETUP_S[N]

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.026` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.6.4 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PJM |
| **Tipo** | [PROCESO] sub-procedimiento por sprint en FASE 6 |

---

## 1. Propósito

PJM produce el documento SETUP_S[N] para cada sprint del bloque. SETUP contiene script Python con pasos secuenciales que el TL ejecutará (en `ASG-001`) para crear estructura VTT del sprint. Este Protocol NO ejecuta el script, solo lo produce.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `analisis_scope` | path | WORKFLOW-025 | sí | Análisis interno del PJM |
| `sprint_id` | string (S00..S0N) | iterador | sí | Sprint a producir |
| `metodologia_setup_fase` | path | metodologías | sí | Estructura del SETUP |
| `metodologia_setup_plan_vtt` | path | metodologías | sí | Reglas del grafo |
| `template_setup` | path | templates | sí | Template canónico |

---

## 3. Precondiciones

- WORKFLOW-025 cerrado sin inconsistencias.
- Sprint tiene deliverables asignados en Capacity Plan.

---

## 4. Reglas del Workflow

- **R1:** SETUP NO se ejecuta dentro de este Protocol. Solo se PRODUCE como documento.
- **R2:** Script Python sigue la jerarquía Release → Sprint → Delivery → Task.
- **R3:** Cada tarea creada debe tener campo `Registrar:` para que TL anote el UUID devuelto por API.
- **R4:** Estructura sigue METODOLOGIA_SETUP_PLAN_VTT (grafo sin huérfanos ni hojas, verificable por script).
- **R5:** R6 del SPRINT-001 v1.0.0: VERY HIGH → mapear a HIGH en campo `complexity` (API no acepta VERY HIGH).
- **R6:** No incluir auto-completar SETUP — TL lo cierra tras verificar (`RULE-SETUP-MANUAL-CLOSE`).

---

## 5. Pasos

### Paso 1 — PJM lee análisis de scope del sprint S[N]

Extrae deliverables del sprint, roles activos, dependencias cross-sprint.

### Paso 2 — PJM genera bloque "Crear/verificar Release"

¿Es S00 o S01 (primer sprint del bloque)? → **[DECISIÓN]**
- **SÍ** → bloque para crear Release del bloque (`POST /api/projects/{id}/releases`).
- **NO** → bloque para recuperar RELEASE_ID de CONTEXTO_S(N-1).

### Paso 3 — PJM genera bloque "Crear Sprint S[N]"

`POST /api/releases/{id}/sprints` con campos: `number`, `name`, `goal`, `startDate`, `endDate`.

### Paso 4 — PJM genera bloque "Crear tarea SETUP-S[N]"

Tarea formal `SETUP-S[N]` que el TL ejecuta y cierra al verificar.

### Paso 5 — PJM genera bloque "Crear Deliveries"

Por cada módulo/rol activo en el sprint → 1 Delivery + 1 Delivery REV.

Naming: `S[N]-<ROL>: <descripción>`.

Endpoint: `POST /api/deliveries` con `phaseId`, `name`, `order`.

### Paso 6 — PJM genera bloque "Vincular Deliveries al Sprint"

`PATCH /api/deliveries/{id}` con body `{ sprintId }`.

Sin este paso, las tareas quedan sin sprint visible en dashboard.

### Paso 7 — PJM genera bloques de creación de tareas (1 bloque por rol)

Por cada tarea del rol:
- title: `[ID_CATALOGO] Nombre`
- description: deliverable + sprint + rol + horas + complejidad + dependencias
- assigneeId: UUID del rol
- estimatedHours, priorityId, complexity (mapear VERY HIGH → HIGH), category
- Campo `Registrar:` vacío para que TL anote UUID

### Paso 8 — PJM genera bloque "Tareas de validación + CIERRE + APR"

Tareas obligatorias:
- TL-S[N]-REV (Code Review) — assignee TL
- AR-S[N] (Integration Audit) — assignee AR
- DL-S[N]-REV (Visual Review) — solo si FE en sprint
- CIERRE-S[N] — assignee TL
- APR-S[N] (Aprobación PM) — assignee PM

### Paso 9 — PJM genera bloque "Asociar tareas a Deliveries"

`POST /api/deliveries/{id}/tasks/{taskId}` por cada tarea.

Cada tarea en exactamente 1 Delivery (`RULE-VTT-004`).

### Paso 10 — PJM genera bloque "Registrar dependencias"

`POST /api/tasks/{id}/dependencies` por cada dep.

Cadena obligatoria:
- Cross-sprint: `SETUP-S[N]` → `CIERRE-S[N-1]`
- Validación: `deliverables → TL Review → AR Audit → (DL Review) → CIERRE → APR`

### Paso 11 — PJM genera template CONTEXTO_S[N].md

Template que el TL llenará con UUIDs reales al ejecutar SETUP.

### Paso 12 — PJM genera checklist de verificación

Lista que el TL ejecuta al final para confirmar que estructura quedó bien creada.

### Paso 13 — PJM produce SETUP_S[N].md final

Documento completo con script + checklist + template CONTEXTO.

### Paso 14 — PJM produce SETUP_S[N].json sincronizado

→ invoca **`VTT.WORKFLOW-HO-001.019_producir_json_sincronizado`** con (`md_path=SETUP_S[N].md`)

### Paso 15 — PJM ejecuta REVMA sobre SETUP_S[N]

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`** con SA como revisor (o PM Revisor si SA no en cadena).

Validación contra METODOLOGIA_SETUP_FASE + METODOLOGIA_SETUP_PLAN_VTT.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `SETUP_S[N].md` | archivo .md | `_project-management/Fases/<BLOQUE>/Sprints/` |
| `SETUP_S[N].json` | archivo .json sincronizado | mismo lugar |

---

## 7. Validación

- Script Python sigue jerarquía Release → Sprint → Delivery → Task.
- Cada tarea tiene campo `Registrar:` vacío.
- VERY HIGH mapeado a HIGH.
- No incluye auto-completar SETUP.
- CONTEXTO template incluido.
- Checklist de verificación incluido.
- .md + .json sincronizados.
- REVMA aprobado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Tareas sin campo `Registrar:` | Olvido | Agregar a todas |
| Delivery sin PATCH a sprintId | Violación R4 | Agregar bloque |
| VERY HIGH sin mapear | Violación R5 | Mapear a HIGH |
| SETUP auto-completa | Violación R6 | Eliminar paso de cierre automático |
| Tarea en >1 Delivery | Inconsistencia | Asignar a exactamente 1 |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.019` (sincronización JSON)
- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.026_producir_setup_sprint.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
