# HANDOFF — Sesión de Normativa VTT (Mayo 17-20, 2026)

| Campo | Valor |
|---|---|
| **Fecha de generación** | 2026-05-20 |
| **Sesiones cubiertas** | 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20 |
| **Generado por** | Agente saliente (Claude Sonnet 4.6) |
| **Para** | Agente entrante que continúe el trabajo de formalización normativa VTT |
| **PM responsable** | Martin Rivas |
| **Proyecto** | `virtual-teams-setup` (formalización canónica del modelo operativo VTT) |
| **Path canónico** | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/` |

---

## 0. LECTURA OBLIGATORIA ANTES DE EMPEZAR

> **Si sos el agente nuevo, lee este documento COMPLETO antes de tocar nada.**
> Tiene 4 horas de trabajo destilado. Saltarlo va a hacer que repitas errores ya cometidos.

### Tu identidad como agente

Sos un **agente de documentación normativa** para el proyecto VTT (Virtual Teams Tracking). VTT es un sistema de gestión de tareas que orquesta agentes IA + humanos para ejecutar proyectos de software completos (Memory Service es uno de esos proyectos).

`virtual-teams-setup` es la **formalización canónica** del modelo operativo VTT — toda la normativa, templates, skills y scripts viven aquí. Otros proyectos (memory-service, virtual-teams-tracking) consumen esta normativa.

### Tu interlocutor

**Martin Rivas (PM)** — habla español rioplatense informal, tiene typos frecuentes (no le corrijas), mucho contexto operativo en su cabeza. Cuando se frustra es porque perdiste el foco — pausá y volvé al norte.

---

## 1. ESTADO DEL TRABAJO (qué está hecho, qué falta)

### 1.1 LO QUE ESTÁ HECHO ✅

#### Sub-sistemas normativos completos

| Sub-sistema | Componentes | Estado |
|---|---|---|
| **Manifest (MAN)** | PROTOCOL-MAN-001 v1.1.1 + 4 Workflows + 2 Skills + 2 Scripts | ✅ Validado en producción (VTT-721, VTT-718) |
| **Worktrees (WT)** | PROTOCOL-WT-001 v1.0.1 + 5 Workflows + 2 Skills + 3 Scripts | ✅ Generado, sin validar aún |
| **Ciclo de tareas (ASG)** | PROTOCOL-ASG-001 v1.3.3 — solo el Protocol (sus 28 Workflows están declarados pero NO escritos) | ⚠️ Protocol completo, Workflows pendientes |

#### Meta-índices (gobernanza de nomenclatura)

| Documento | Versión | Path |
|---|---|---|
| Registro de acrónimos (categorías `<CAT>` + branches Git) | v1.4 | `02.normativa/00_REGISTRO_ACRONIMOS.md` |
| Convenciones de filesystem (estructura obligatoria del proyecto) | v1.0 | `02.normativa/00_CONVENCIONES_FILESYSTEM.md` |
| INVENTARIO maestro de documentos | v1.5 | `02.normativa/INVENTARIO.md` |
| Guía del autor (cómo crear normativa) | v1.0 | `02.normativa/GUIA_AUTOR.md` |

#### Skills VTT migradas (38 totales)

13 categorías activas. Todas las legacies `SKL-*` están marcadas `🟤 DEPRECADA` con puntero al reemplazo.

| Categoría | Cant. | Path |
|---|---:|---|
| AUTH | 1 | `03.Skills/auth/` |
| TASK | 5 | `03.Skills/task/` |
| STATUS | 6 | `03.Skills/status/` |
| QUERY | 5 | `03.Skills/query/` |
| COMMENT | 3 | `03.Skills/comment/` |
| DEV | 2 | `03.Skills/dev/` |
| ISS | 1 | `03.Skills/iss/` |
| ATTACH | 2 | `03.Skills/attach/` |
| GIT | 6 | `03.Skills/git/` |
| REPORT | 2 | `03.Skills/report/` |
| FILE | 1 | `03.Skills/file/` |
| MAN | 2 | `03.Skills/manifest/` |
| WT | 2 | `03.Skills/worktree/` |

#### Templates de autoría

Carpeta `03.templates/normativa/_autoria/` con 4 templates (PROTOCOL/WORKFLOW/SKILL/SCRIPT) + README.

#### Template de mensaje al agente

`03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md` v2.0 (única plantilla, sección Working Directory condicional WT/no-WT).

### 1.2 LO QUE FALTA ❌

#### Workflows del PROTOCOL-ASG-001 (24 pendientes de escribir)

El Protocol los declara en §6.1 pero **ninguno está escrito como archivo**. Estos son los slots:

```
.001  Validar inputs del handoff
.002  Analizar handoff y extraer scope                ← era el piloto (fue intentado y borrado)
.003  Determinar datos de tareas
.004  Setup inicial estructura VTT (Sprint+Deliveries+SETUP-SX)
.005  Mapear dependencias del sprint
.006  Crear tareas del sprint
.007  Generar y subir BRIEFs
.008  Analizar dependencias de datos
.009  Generar ASSIGNMENT desde código
.010  Entrega del agente (referencia)
.011  Analizar Issue y decidir acción
.012  Code review técnico
.013  Aplicar Modelo Dinámico al cierre
.014  🟤 Deprecado (reemplazado por WORKFLOW-MAN-001.004)
.015  Firma de stage development
.016  Cierre de sprint CLOSURE
.017  Revisar Living Documents impactados
.018  Registrar Document Impacts
.019  Ejecutar Hardcode Check
.020  Verificar worktree del agente
.021  🟤 Deprecado (reemplazado por WORKFLOW-MAN-001.001)
.022  🟤 Deprecado (reemplazado por WORKFLOW-MAN-001.002)
.023  Verificar disciplina de worktree (TL Reviewer)
.024  Cleanup branch local post-aprobación
.025  Vincular Trackable Items a tareas
.026  Generar CONTEXTO_SX.md
.027  Cerrar SETUP-SX
.028  Mantener SPRINT_STATUS_SX.md
```

**24 reales pendientes** (los 3 deprecados están cubiertos por sub-sistema MAN).

#### SOPs legacy pendientes de migrar (21 archivos)

Path: `02.normativa/01.Protocols/_pending-migration/`

**El más importante:** `PROCESO_ANALISIS_HO_GENERACION_BRIEFS.md` v1.5 (840 líneas, 12 PASOS) — es la fuente primaria para los Workflows `.002`, `.004`, `.005`, `.006`, `.007`, `.025`, `.026`, `.027`.

Otros SOPs legacy relevantes:
- `PROCESO_ASIGNACION_TAREAS.md` v1.6 (legacy de PROTOCOL-ASG)
- `PROCESO_ASIGNACION_TAREAS_v3.md` v3.1
- `PROCESO_CIERRE_TAREA_v2.md` v2.1
- `01_PM_PROCESO_ANALISIS_INICIAL.md`
- `02_PJM_PROCESO_SETUP_PROYECTO_VTT.md`
- `03_FLUJO_TL.md`, `06_FLUJO_DL.md`, `07_FLUJO_PJM.md`, `08_FLUJO_PM.md`, `10_FLUJO_SA_REVIEWER.md`
- `11_GUIA_AGENTES_MODELO_DINAMICO_V4.md` (alimenta Workflow .013)
- `SOP-LD-01_living_documents.md` (futuro PROTOCOL-LD-001)
- `SOP-TRK-01_trackable_items_workflow.md` (futuro PROTOCOL-TRK-001)
- `SOP-TRK-02_dynamic_item_creation.md`
- `SOP-EST-01_technical_estimates.md`
- `SOP-VEL-01_velocity_methodology.md`
- `SOP-RET-01_retrospective_analysis.md`
- `HANDOFF_PJM_ADDENDUM_V4.5.md`
- `CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md`
- `METODOLOGIA_TRABAJO_PM_VTT.md`
- `SETUP_PROCESS_PM.md`

#### Otros pendientes documentados

- **CARDs** (capa runtime liviana) — decisión arquitectónica postergada
- **Sub-sistema MSG** (formalizar mensaje al agente) — `SKL-MESSAGE-01` es legacy + `gen_mensaje.py` tiene formato hardcoded
- **Validación end-to-end** del PROTOCOL-WT-001 con proyecto real
- **PROTOCOL-ISS-001** (Proceso de Issue y on_hold)
- **WORKFLOW-MAN-001.005** (PM aprueba terminal → v2.0)

---

## 2. LECCIONES APRENDIDAS — Cómo NO repetir mis errores

### 2.1 Error fatal del agente saliente

**Generé el Workflow `.002_analizar_handoff` con código curl/Python inline.** Martin me corrigió:

> "los codigos deben ser los skill a desarrolalr / todo esto es basuira en un proceso"

**Regla resultante:** un Workflow **NO contiene código**. El Workflow es **lista de pasos** donde cada paso **invoca una skill por código** (`VTT.SKILL-XXX-NNN`). El código vive en la Skill o en el Script que la Skill orquesta.

### 2.2 Lo que sí funcionó (formato bueno)

Estos archivos son el **gold standard** del formato — copialos como referencia:

| Archivo | Por qué es bueno |
|---|---|
| `02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md` | Workflow ejecutable invocando solo skills, sin código inline |
| `02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.004_actualizar_task_manifest_v15.md` | Mismo formato, validado en producción |
| `02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | Skill con contrato + esquema + ejecución delegada a Script |
| `02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` | Script con argparse, stdout JSON, exit codes, sin lógica de negocio inline |

### 2.3 Reglas de oro del modelo de 4 niveles

```
Nivel 4 — PROTOCOL    Gobierna el proceso completo (qué/por qué/quién)
Nivel 3 — WORKFLOW    Pasos secuenciales (qué hacer, invocando skills)
Nivel 2 — SKILL       Capacidad reusable (contrato + endpoints VTT)
Nivel 1 — SCRIPT      Ejecutable atómico (código real con argparse)
```

**Regla #1:** un Workflow invoca skills por código (`VTT.SKILL-XXX-NNN`). No tiene curl.

**Regla #2:** una Skill describe **qué hace** y **cómo invocarla** — el código puede vivir inline si es trivial (≤30 líneas) o delegarse a Script.

**Regla #3:** un Script es atómico — una llamada HTTP o una operación filesystem. Sin lógica de negocio.

**Regla #4:** un Protocol **NO ejecuta** — gobierna. Sus pasos referencian Workflows por código.

### 2.4 Errores específicos detectados en producción (anti-patterns)

| Anti-pattern | Solución | Donde lo aprendimos |
|---|---|---|
| Generar manifest prematuramente (antes de attachments) | Regla PROC-MANIFEST-01 — manifest AL FINAL | Caso MS-284 (10+ campos null) |
| Worktree compartido entre agentes (`git checkout` cross-agente) | PROC-COORD-01 — un worktree por rol | Caso MS-286 (3 agentes pisaron código) |
| Drift de paths (`<sprint>/` vs `<phase>/<sprint>/`) | `00_CONVENCIONES_FILESYSTEM.md` v1.0 | Caso VTT-718 (4 archivos duplicados en 2 carpetas) |
| Skills con código del proyecto hardcodeado | Las skills VTT son agnósticas del proyecto | Caso `gen_mensaje.py` viejo |
| Categorías de normativa sin registro central | `00_REGISTRO_ACRONIMOS.md` §3 | Detectado durante migración de skills |
| TL no commitea sus cambios (acumula untracked files) | PROTOCOL-ASG-001 §5.5.bis FASE 4.5 — branch `tl/<TASK_ID>-close` + PR | Validado con VTT-721/718 |
| `rejected` modelado como estado (mal) | Es ACCIÓN, el backend auto-mueve a in_progress. Pero `task_rejected` SÍ existe en BD del backend actual (hay tensión con METODOLOGIA conceptual) | Discusión inconclusa — ver §3.4 |

### 2.5 Bugs corregidos del SCRIPT-MAN-001 (8 fixes en v1.3)

Esto es histórico — ya está aplicado, pero documentado por si reaparecen:

| # | Bug | Fix aplicado |
|---|---|---|
| 1 | Parser de deliverables corta en `-` (rompe `code-logic/`) | Regex acepta guion dentro del path |
| 2 | `devlog_entries[].category` viene como objeto | `_norm_category()` extrae `.code` |
| 3 | `indexes` no se recalcula en v1.5 | `_reindex()` al final de `build_v15()` |
| 4 | `task.sprint/stage/category` null por shape de VTT | `_pick()` prueba múltiples paths |
| 5 | Campo comment `body` (incorrecto) | Usar `message` (correcto en VTT) |
| 6 | `uploadedById` falta en multipart | Agregado al form-data |
| 7 | Endpoint `/api/tasks/<id>/attachments/<attId>` → 404 | Usar `/api/attachments/<id>/file` |
| 8 | v1.5 solo agregaba `new_tis_created` al `related_to` | También consolidar `evidences_added` |

---

## 3. CONTEXTO TÉCNICO QUE TIENES QUE SABER

### 3.1 Backend VTT (producción)

```
Base URL:    http://77.42.88.106:3000
Auth:        Service token (POST /api/auth/service-token con userId + serviceKey)
Token life:  30 días
```

**Endpoints clave validados en producción:**

| Endpoint | Método | Notas |
|---|---|---|
| `/api/auth/service-token` | POST | Obtener JWT |
| `/api/releases/{releaseId}/sprints` | POST | Crear sprint |
| `/api/deliveries` | POST | Crear delivery (sprintId obligatorio en body) |
| `/api/deliveries/{id}` | PUT | Reordenar (NO funciona con PATCH) |
| `/api/phases/{phaseId}/tasks` | POST | Crear tarea |
| `/api/deliveries/{deliveryId}/tasks/{taskId}` | POST | Vincular task a delivery (paso separado) |
| `/api/tasks/{id}/dependencies` | POST | Agregar dependencia |
| `/api/tasks/{id}/status` | PATCH | Cambiar estado (excepto on_hold) |
| `/api/tasks/{id}/on-hold` | PUT | Poner en on_hold (header `x-user-id` obligatorio) |
| `/api/tasks/{id}/criteria` | POST | Crear AC (campo `criteriaTypeCode`, NO `type`) |
| `/api/tasks/{id}/devlog-entries` | POST | Registrar devlog entry (campo `categoryCode`, NO `type`) |
| `/api/tasks/{id}/devlog` | GET | Leer devlog (singular, NO plural en GET) |
| `/api/tasks/{id}/attachments` | POST | Multipart con `uploadedById` obligatorio |
| `/api/attachments/{id}/file` | GET | Descargar archivo (NO `/tasks/{id}/attachments/{attId}`) |
| `/api/tasks/{id}/comments` | POST | Comment (campos `message` + `userId`, NO `body`/`authorId`) |
| `/api/tasks/{id}/review-gate` | GET | Verifica `canProceedToReview` |
| `/api/projects/{id}/trackable-items` | POST | Crear TI |
| `/api/trackable-items/{id}/tasks` | POST | Vincular TI a tarea |
| `/api/sprints/{id}/stages/{stage}/sign` | POST | Firmar stage (development/integration/design) |

### 3.2 Status UUIDs fijos del backend

| Status | UUID |
|---|---|
| `task_pending` | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| `task_in_progress` | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| `task_in_review` | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| `task_completed` | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| `task_approved` | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |

> **Gotcha:** `task_rejected` y `task_pending` comparten el UUID `335fd9c6-...`. VTT distingue por contexto (si venía de `task_completed` → `task_rejected`; si está nueva → `task_pending`).

### 3.3 Modelo de datos VTT (jerarquía completa)

```
Project
  └── Release          (ej: MVP, R1)
        └── Sprint     (ej: S1, S2, S3)
              └── Delivery   (agrupador, ej: DB-S2, BE-S2)
                    └── Task (unidad de trabajo, código MS-XXX o VTT-XXX)
```

**Nomenclatura estándar de Deliveries:**
- `SX-SETUP` (order 1 — siempre primero)
- `SX-DB`, `SX-BE`, `SX-FE` (order 2+)
- `SX-TL` (penúltimo)
- `SX-REV` (último)

### 3.4 Tensión NO resuelta: estados con/sin prefijo `task_`

**Situación:** el documento `METODOLOGIA_CICLO_VIDA_TAREA_v1.md` (de `virtual-teams-tracking/_project-management/planV2/`) describe estados **sin prefijo** (`completed`, `approved`, etc.) y dice que `rejected` **NO es un estado, es una acción**.

**Pero el backend real** usa `task_completed`, `task_approved`, `task_rejected` con prefijo y `task_rejected` SÍ es estado.

**Lo que Martin clarificó:** la METODOLOGIA es el **diseño conceptual original** (Febrero 2026), pero el backend evolucionó (Mayo 2026) y agregó prefijos + extensiones (Release/Sprint/Delivery que el modelo conceptual no tenía).

**Conclusión:** **el backend real es la fuente de verdad.** La METODOLOGIA es documento histórico.

### 3.5 Convención de filesystem de cualquier proyecto VTT

Documentada en `00_CONVENCIONES_FILESYSTEM.md` v1.0. Esquema obligatorio:

```
<project_root>/
├── knowledge/
│   ├── agent-tasks/
│   │   ├── briefs/<phase>/<sprint>/BRIEF_<TASK_ID>_<slug>.md
│   │   ├── assignments/<phase>/<sprint>/ASSIGNMENT_<TASK_ID>_<slug>.md
│   │   ├── messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md
│   │   └── reports/<phase>/<sprint>/<TASK_ID>_REPORT.md
│   ├── task-manifests/<phase>/<sprint>/<TASK_ID>.json (+.manifest.md)
│   ├── development-log/<YYYY-MM-DD>_<TASK_ID>_<slug>.md
│   ├── code-logic/<modulo>/<archivo>.LOGIC.md
│   └── platform-feedback/
├── scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py (copia del setup)
└── .vtt/ (opcional — solo proyectos con worktrees por rol)
    ├── worktrees/<repo>-<rol>/
    ├── workspaces/<repo>-<rol>.code-workspace
    └── manifests/<TASK_ID>.execution.json
```

### 3.6 Convención de branches Git

Documentada en `00_REGISTRO_ACRONIMOS.md` §3.bis. Patterns activos:

| Pattern | Actor | Propósito |
|---|---|---|
| `feature/<TASK_ID>` | Agente ejecutor | Implementación de tarea + commit del manifest v1.0 |
| `tl/<TASK_ID>-close` | TL Reviewer | Manifest v1.5 + archivos modificados durante review |
| `fix/<TASK_ID>` | Agente (re-entrega) | Correcciones tras `task_rejected` |
| `hotfix/<DESCRIPTOR>` | TL/agente con autorización PM | Bug crítico sin TASK_ID |
| `wt-<repo>-<rol>` | Setup de worktree | Branch idle del worktree por rol |

**NO se permite commit directo a main.** Toda branch va por PR.

---

## 4. PROCESO DE MIGRACIÓN — Cómo trabajar bien

### 4.1 Patrón de migración que funcionó

Cuando migramos las 38 skills (proceso que Martin describió como "extraordinario" antes de que perdiera el foco):

```
Para cada bloque de skills (categoría):
  1. Listar los SKL-* legacy del bloque
  2. Leer TODOS antes de generar el primero
  3. Identificar inputs contractuales, endpoints, gotchas
  4. Generar las nuevas VTT.SKILL-* en lote
  5. Marcar las legacies como 🟤 DEPRECADA con puntero al reemplazo
  6. Actualizar INVENTARIO
  7. Pausar — confirmar con Martin antes de seguir
```

### 4.2 Patrón de migración que falló

Lo que rompió la sesión cuando intenté migrar Workflows:

```
❌ MAL: leer un solo SOP, generar pedazos de Workflows sueltos
❌ MAL: meter código curl/Python dentro de Workflows
❌ MAL: agrupar pasos en Workflows sin validar el mapeo con Martin antes
❌ MAL: no entender que un Workflow es lista de pasos invocando skills
```

### 4.3 Patrón correcto para migrar Workflows (no validado aún)

Lo que **Martin esperaba** que hiciera y yo no entendí a tiempo:

```
Para CADA Workflow del PROTOCOL-ASG-001:

  1. Leer el SOP fuente COMPLETO (no fragmentos)

  2. Identificar el rango de pasos del SOP que alimenta este Workflow
     (ej. .002 ← PASO 1 + Sección 1 + Sección 2 del SOP)

  3. Identificar QUÉ skills necesita invocar el Workflow
     (cada operación VTT = una skill)

  4. Verificar que esas skills YA existen en 02.normativa/03.Skills/
     - Si existe: usar su código `VTT.SKILL-XXX-NNN`
     - Si NO existe: PAUSAR, generar la skill primero, después continuar

  5. Generar el Workflow como LISTA DE PASOS:
     - Paso N: descripción en lenguaje natural
     - → invoca `VTT.SKILL-XXX-NNN` con (inputs)
     - SIN código inline

  6. Validar con Martin antes de seguir con el siguiente Workflow
```

**Regla crítica:** un Workflow NO tiene código curl/Python/bash inline. Solo referencias a skills.

### 4.4 Mapeo SOP `PROCESO_ANALISIS_HO_GENERACION_BRIEFS.md` → Workflows del PROTOCOL-ASG-001

Validado conmigo en sesión, sirve como input para el agente nuevo:

| Contenido del SOP | Workflow VTT destino |
|---|---|
| PASO 0 — Consultar VTT + CONTEXTO sprint anterior | `.001` validar inputs del handoff |
| PASO 1 — Leer HO y evaluar fuentes | `.002` analizar handoff |
| PASOS 2-4 — Crear Sprint + Deliveries + SETUP-SX | `.004` setup estructura VTT |
| PASOS 5-7 — Crear tareas operativas + cierre + vincular a deliveries | `.006` crear tareas del sprint |
| PASO 8 — Registrar dependencias | `.005` mapear dependencias |
| PASOS 9-10 — Generar BRIEFs + crear AC | `.007` generar y subir BRIEFs |
| PASO 10.1 — Vincular Trackable Items | `.025` vincular TIs (Workflow NUEVO) |
| PASO 11 — Generar CONTEXTO_SX.md | `.026` generar CONTEXTO_SX.md (Workflow NUEVO) |
| PASO 11.1 — Cerrar SETUP-SX | `.027` cerrar SETUP-SX (Workflow NUEVO) |
| PASO 12 — Checklist final | Validación del flujo |
| Sección 4 — Al momento de asignar (Fase 2) | `.009` generar ASSIGNMENT |
| Sección 5 — Cierre del sprint (CLOSURE_SX) | `.015` firma stage + `.016` CLOSURE |
| Sección 6 — Análisis dependencias reales | Sub-procedimiento de `.005` |
| Sección 7 — SPRINT_STATUS_SX | `.028` mantener SPRINT_STATUS (Workflow NUEVO) |
| Lecciones aprendidas | Cada §Error común de cada Workflow |

### 4.5 Skills que faltan (detectadas pero NO generadas)

Cuando intenté generar el `.002`, descubrí que faltan 2 skills nuevas que no migré:

| Skill faltante | Por qué se necesita |
|---|---|
| `VTT.SKILL-QUERY-006_listar_sprints` | `.002` necesita listar sprints de un release |
| `VTT.SKILL-ATTACH-003_descargar_attachment` | `.002` necesita descargar el CONTEXTO_S(X-1).md de VTT |

Probablemente surjan más a medida que se escriban los Workflows restantes. **El patrón es:** detectás la necesidad → pausás → generás la skill → seguís.

---

## 5. INVENTARIO DETALLADO DE ARCHIVOS GENERADOS

### 5.1 Protocols (Nivel 4)

| Código | Path | Versión |
|---|---|---|
| `VTT.PROTOCOL-MAN-001` | `02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | v1.1.1 |
| `VTT.PROTOCOL-WT-001` | `02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | v1.0.1 |
| `VTT.PROTOCOL-ASG-001` | `02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` | v1.3.3 |

### 5.2 Workflows (Nivel 3) — 9 generados

```
02.normativa/02.Workflows/
├── VTT.WORKFLOW-MAN-001.001_generar_execution_manifest.md
├── VTT.WORKFLOW-MAN-001.002_leer_execution_manifest.md
├── VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md
├── VTT.WORKFLOW-MAN-001.004_actualizar_task_manifest_v15.md
├── VTT.WORKFLOW-WT-001.001_setup_inicial.md
├── VTT.WORKFLOW-WT-001.002_apertura_sesion_diaria.md
├── VTT.WORKFLOW-WT-001.003_agregar_rol.md
├── VTT.WORKFLOW-WT-001.004_casos_especiales.md
└── VTT.WORKFLOW-WT-001.005_cleanup_final.md
```

### 5.3 Skills (Nivel 2) — 38 totales

Listado completo en `02.normativa/INVENTARIO.md` §5.

### 5.4 Scripts (Nivel 1) — 6 generados

```
02.normativa/04.Scripts/
├── git/VTT.SCRIPT-GIT-001_validate_branch_and_commit.py
├── manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py    (v1.3 — validado en producción)
├── manifest/VTT.SCRIPT-EXM-001_gen_execution_manifest.py
├── worktree/VTT.SCRIPT-WT-001_setup_worktrees.py
├── worktree/VTT.SCRIPT-WT-002_add_worktree.py
└── worktree/VTT.SCRIPT-WT-003_cleanup_worktrees.py
```

### 5.5 Templates

```
03.templates/
├── normativa/_autoria/
│   ├── TEMPLATE_PROTOCOL.md
│   ├── TEMPLATE_WORKFLOW.md
│   ├── TEMPLATE_SKILL.md
│   ├── TEMPLATE_SCRIPT.py
│   └── README.md
├── normativa/
│   ├── VTT.TEMPLATE-CLO-001_closure_sprint.md
│   ├── VTT.TEMPLATE-CFL-001_criteria_fulfillment.md
│   └── VTT.TEMPLATE-APR-001_apr_tl_comment.md
└── tarea/
    └── TEMPLATE_MENSAJE_ASIGNACION.md (v2.0)
```

### 5.6 Meta-índices

```
02.normativa/
├── 00_REGISTRO_ACRONIMOS.md (v1.4)        ← categorías + branches Git
├── 00_CONVENCIONES_FILESYSTEM.md (v1.0)   ← estructura obligatoria por proyecto
├── INVENTARIO.md (v1.5)                   ← catálogo maestro
└── GUIA_AUTOR.md (v1.0)                   ← cómo crear normativa
```

---

## 6. CASOS REALES VALIDADOS EN PRODUCCIÓN

### 6.1 VTT-721 (Memory Service Backend — Fix MIME)

**Proyecto:** virtual-teams-tracking
**Sprint:** S06-FIX-A
**Resultado:** Cierre end-to-end con script v1.2 (antes del Fix #8)

Lo que validó:
- ✅ Manifest v1.0 (agente) + v1.5 (TL) generados con `VTT.SCRIPT-MAN-001`
- ✅ Commit del manifest al PR del agente (PROTOCOL-MAN-001 §5.3.7)
- ✅ Branch `tl/VTT-721-close` con PR a main (PROTOCOL-ASG-001 §5.5.bis FASE 4.5)
- ⚠️ Detectó 7 bugs del script → fixes #1-#7 aplicados

PRs activos:
- #719 `feature/VTT-721` (BE agent) — fix MIME en código
- #721 `feature/VTT-721-manifest` (BE agent) — Paso 12 commit del manifest
- #722 `tl/VTT-721-close` (TL) — FASE 4.5

### 6.2 VTT-718 (QA Engineer — Cierre con 21 TIs)

**Proyecto:** virtual-teams-tracking
**Sprint:** S06-FIX-A
**Resultado:** Detectó el Bug #8 (re-indexación de TIs evidenciados)

Lo que validó:
- ✅ 21 TIs evidenciados con marker `[TASK:VTT-718]`
- ✅ 8/8 devlog entries resolved
- ✅ APR-TL comment posteado
- ❌ Manifest v1.5 inicial tenía `related_to_codes: []` (Bug #8)
- ✅ Fix #8 aplicado en v1.3 del script
- ✅ Re-generación de v1.5 con script v1.3 → `related_to_codes: 21` correcto

PR activo:
- #723 `tl/VTT-718-close` (TL) — FASE 4.5 con Fix #8 aplicado

### 6.3 Estructura de archivos en `virtual-teams-tracking` (caso real)

```
knowledge/
└── task-manifests/
    └── 04-development/
        └── S06-FIX-A/
            ├── VTT-721.json
            ├── VTT-721.manifest.md
            ├── VTT-718.json
            └── VTT-718.manifest.md
```

> **NOTA:** detectamos drift inicial (archivos duplicados en `S06-FIX-A/` sin `04-development/`). Lo corregimos con `00_CONVENCIONES_FILESYSTEM.md`. Si volvés a ver duplicados, revisá esa convención.

---

## 7. LO QUE MARTIN ESPERA DE TI

### 7.1 Tu rol

Sos el agente que **completa la formalización normativa de VTT**. El proyecto está al 60% — sub-sistemas MAN y WT cerrados, ASG con Protocol pero Workflows pendientes.

### 7.2 Lo que NO debes hacer

1. **NO generar pedazos sueltos.** Antes de tocar un archivo, entiende el contexto completo.
2. **NO inventar.** Si un dato falta, preguntá a Martin. NO inventes UUIDs, paths, ni endpoints.
3. **NO mezclar niveles.** Un Workflow NO tiene código. Una Skill SÍ. Un Script SÍ.
4. **NO migrar SOPs a Protocols nuevos** sin antes verificar si su contenido alimenta Workflows del PROTOCOL-ASG-001 existente.
5. **NO actuar sin confirmación** en decisiones arquitectónicas (ej. categoría nueva, naming convention).

### 7.3 Lo que SÍ debes hacer

1. **Leer este HANDOFF completo antes de tocar nada.**
2. **Leer el SOP fuente completo** antes de generar un Workflow derivado.
3. **Verificar que las skills que va a invocar el Workflow EXISTEN** en `02.normativa/03.Skills/`. Si no existen, generarlas primero.
4. **Pausar y confirmar** con Martin después de cada bloque (no después de cada archivo, no después del proyecto entero).
5. **Mantener el INVENTARIO actualizado** con cada archivo nuevo.

### 7.4 Cómo comunicarte con Martin

- Es PM, no developer. Habla en español rioplatense informal.
- Tiene typos frecuentes — entendelos por contexto, no le corrijas.
- Cuando se frustra es porque perdiste el foco — pausá y volvé al norte.
- Le gusta cuando le proponés opciones (A/B/C) con votación tuya.
- Le molesta cuando generás cosas sin entender el proceso completo.

### 7.5 Cuando perdés el foco (te va a pasar)

Síntomas:
- Empezás a generar pedazos sin coherencia
- Mezclás niveles (código en Workflow, lógica de negocio en Script)
- Martin te dice "no entendiste" más de 2 veces

Acción:
1. **PAUSAR inmediatamente**
2. Releer este HANDOFF
3. Releer el último mensaje de Martin (no los anteriores)
4. Preguntar a Martin: "¿estoy en el camino correcto?"

---

## 8. PRÓXIMOS PASOS SUGERIDOS

### 8.1 Inmediato (primera sesión del agente nuevo)

**Tarea 1 — Validar el HANDOFF.**

Leer este documento completo, recorrer los paths mencionados, verificar que todo lo descrito existe en disco. Reportar a Martin:
- ✅ Confirmo el estado del proyecto
- ❌ Inconsistencias detectadas (si hay)

**Tarea 2 — Decidir el siguiente bloque.**

Opciones (en orden de prioridad sugerida):
- **A.** Continuar con el Workflow `.002_analizar_handoff` (intento previo borrado) — siguiendo el patrón correcto de §4.3
- **B.** Generar las 2 skills faltantes detectadas (`QUERY-006`, `ATTACH-003`) antes del Workflow .002
- **C.** Otra cosa que Martin priorice

### 8.2 Mediano plazo (siguiente semana)

- Generar los 24 Workflows pendientes del PROTOCOL-ASG-001 siguiendo el patrón correcto
- Migrar SOPs específicos (LD, TRK, EST, VEL, RET) a Protocols propios
- Validar sub-sistema WT con un proyecto real
- Generar sub-sistema MSG (formalizar mensaje al agente)

### 8.3 Largo plazo

- CARDs (capa runtime liviana — postponed)
- Auditoría tl-docs/ (16 archivos del TL pesan ~72K tok)
- Validación end-to-end del Protocol completo con un sprint real

---

## 9. ARCHIVOS DE REFERENCIA OBLIGATORIA

Antes de tocar nada, abrí estos archivos en orden:

1. **Este HANDOFF** (estás leyéndolo)
2. **`02.normativa/INVENTARIO.md` v1.5** — catálogo maestro
3. **`02.normativa/00_REGISTRO_ACRONIMOS.md` v1.4** — convenciones de nomenclatura
4. **`02.normativa/00_CONVENCIONES_FILESYSTEM.md` v1.0** — estructura de proyectos
5. **`02.normativa/GUIA_AUTOR.md` v1.0** — cómo crear normativa
6. **`02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` v1.3.3** — Protocol core
7. **Un Workflow "gold standard"** (ej. `VTT.WORKFLOW-MAN-001.003`) — para copiar el formato
8. **El SOP a migrar** (ej. `PROCESO_ANALISIS_HO_GENERACION_BRIEFS.md` v1.5)

---

## 10. CONTACTO Y CIERRE

**Si necesitás algo del agente saliente:** este documento es la única forma de transferencia. Las conversaciones de chat NO se preservan entre agentes.

**Si Martin te pregunta "¿qué hiciste?":** dale el path al INVENTARIO + este HANDOFF.

**Si te pierdes:** pausá. Pregúntale a Martin "¿qué objetivo concreto querés cumplir ahora?" antes de seguir generando.

---

**Fin del HANDOFF.**

*Generado por agente saliente como acta de transferencia tras 4 días de trabajo intensivo. La sesión generó 38 skills + 9 workflows + 6 scripts + 3 protocols + meta-índices. El trabajo fue extraordinario en el bloque de migración de skills, y se perdió foco al intentar migrar workflows del PROTOCOL-ASG-001 sin entender el patrón correcto. El siguiente agente debe leer este documento ANTES de tocar cualquier archivo.*
