# Reglas de Ubicación de Documentos — Memory Service

**Versión:** 1.0
**Fecha:** 2026-05-14
**Aplicable a:** TODOS los roles (BE, DO, DB, QA, FE, TL, PM, SA, AR, DL, UX, SEC, PJM)
**Estado:** NORMATIVO — obligatorio cumplimiento
**Origen:** Conflictos de escritura cruzada entre agentes durante Sprint S1 (MS-285..MS-293)

---

## Principio central

> **Un documento vive en UN solo repo. El repo donde vive determina qué rol lo crea, modifica y commitea.**

Si un agente necesita un documento que vive en otro repo, lo **lee** (path absoluto o desde VTT), pero NO lo modifica.

---

## Mapa maestro de ubicaciones

### Repo 1: `virtual-teams-setup` — fuente de verdad GENÉRICA

**Solo lectura durante ejecución del proyecto.** Nadie escribe aquí mientras hay tareas activas.

```
virtual-teams-setup/
├── templates/                              ← Templates genéricos reutilizables
│   ├── TEMPLATE_ASIGNACION_TAREA.md
│   ├── TEMPLATE_BRIEF.md
│   ├── TEMPLATE_DEVELOPMENT_LOG.md
│   ├── TEMPLATE_CODE_LOGIC.md
│   └── OPERATIVO_<ROL>_TEMPLATE.md
├── sops/                                   ← SOPs genéricos VTT
│   ├── SOP-LD-01_living_documents.md
│   ├── SOP-TRK-01_trackable_items.md
│   ├── SOP-EST-01_technical_estimates.md
│   └── SOP-RET-01_retrospective_analysis.md
├── rules/                                  ← Reglas globales VTT
│   ├── rules_agents.instructions.md
│   └── rules_catalog.json
├── protocols/                              ← Protocolos operativos
│   ├── PROTOCOL-ASG-001_asignacion.md
│   └── PROTOCOL-CIERRE-001_cierre.md
└── docs/                                   ← Documentación general VTT
    └── INVENTARIO_DOCUMENTOS_VTT.md
```

**Quién escribe aquí:**
- PM/Coordinador VTT (cambios a templates/SOPs genéricos)
- NUNCA durante ejecución de tareas de un proyecto específico

**Quién lee aquí:**
- TL al inicializar (lee templates y SOPs como referencia)
- Cualquier agente que necesite el template base de algún artefacto

---

### Repo 2: `memory-service-project` — específico del proyecto, COORDINACIÓN

**Solo el TL escribe aquí.** Es el repo de coordinación, governance y entregables de fases sin código.

```
memory-service-project/
├── .claude/
│   ├── agents/
│   │   └── OPERATIVO_<ROL>_MEMORY-SERVICE.md      ← TL escribe; copia tropicalizada del template
│   └── rules/
│       ├── PROJECT_RULES.md
│       └── MAPA_DEPENDENCIAS_ENTREGABLES.md
├── 00-agent-setup/
│   ├── 05.Templates/                              ← (Pendiente migrar a virtual-teams-setup)
│   ├── 06.Documentos_soporte/                     ← Guías operativas del proyecto
│   │   ├── REGLAS_UBICACION_DOCUMENTOS.md         ← (este doc)
│   │   ├── GUIA_WORKTREES_MEMORY_SERVICE.md
│   │   ├── GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md
│   │   ├── GUIA_REVISION_TAREA_TL_REVIEWER.md
│   │   ├── PROCESO_ASIGNACION_TAREAS_v3.md
│   │   ├── PROCESO_CIERRE_TAREA_v2.md
│   │   └── ANALISIS_FASES_COMPLETO_PARA_PM.md
│   └── 06.Skills/                                 ← Skills (markdown atómicos)
│       ├── CATALOGO_SKILLS_MEMORY_SERVICE.md
│       ├── dynamic-model/
│       └── manifest/
├── knowledge/
│   ├── agent-tasks/                               ← Artefactos de asignación por tarea
│   │   ├── briefs/04-development/S01/             ← TL crea BRIEF_MS-XXX.md
│   │   ├── assignments/04-development/S01/        ← TL crea ASSIGNMENT_MS-XXX.md
│   │   ├── messages/04-development/S01/           ← TL crea MENSAJE_MS-XXX.md
│   │   └── reports/04-development/S01/            ← TL extrae SKL-REPORT-01 al cerrar
│   ├── task-manifests/04-development/S01/         ← TL crea manifest v1.5 al cerrar
│   ├── platform-feedback/                         ← TL reporta gaps de plataforma VTT
│   └── kickoff/                                   ← PM crea actas de kickoff
├── phases/                                        ← Entregables de fases sin código
│   ├── 00-discovery/deliverables/
│   ├── 01-planning/deliverables/
│   ├── 02-analysis/deliverables/
│   └── 03-design/deliverables/
├── Release2.0/                                    ← Specs aprobadas (read-only)
│   ├── 01-PM/
│   ├── 02-AR/
│   ├── 03-DB/
│   └── 04-TL/
└── scripts/                                       ← Scripts operativos del proyecto
    └── gen_mensaje.py
```

**Quién escribe aquí (worktree `.vtt/worktrees/project-tl/`):**
- TL principalmente (asignación + cierre + governance)
- PM en `knowledge/kickoff/` (al inicio del proyecto)
- SA en `phases/02-analysis/` (cuando fase activa)
- AR en `phases/03-design/architecture/` (cuando fase activa)
- DL en `phases/03-design/wireframes/` (cuando fase activa)
- UX en `phases/03-design/personas/`, `phases/03-design/ia/` (cuando fase activa)

**Quién lee aquí:**
- TODOS los agentes leen su BRIEF/ASSIGNMENT desde aquí o desde VTT comments.
- Agentes de código (BE, DO, DB, QA, FE) NO escriben en este repo.

---

### Repo 3: `memory-service-backend` — código del servicio backend

**Quien escribe aquí:** agentes que producen código de servidor (BE, DO, DB, QA).

```
memory-service-backend/
├── src/                                    ← Código del servicio
├── tests/                                  ← Tests
├── prisma/                                 ← Schema BD (DB Engineer)
├── docker/                                 ← Docker config (DevOps)
├── .vscode/                                ← Workspace config (TL/DevOps)
├── docs/                                   ← Docs técnicos del backend
└── knowledge/
    ├── code-logic/                         ← .LOGIC.md por archivo .ts/.js
    │   ├── controllers/
    │   ├── services/
    │   ├── middleware/
    │   └── errors/
    └── development-log/                    ← Devlogs del agente que ejecuta tarea
        └── YYYY-MM-DD_MS-XXX_<slug>.md
```

**Worktrees por rol que tocan este repo:**
- `.vtt/worktrees/backend-be/` ← BE Engineer
- `.vtt/worktrees/backend-do/` ← DevOps
- `.vtt/worktrees/backend-db/` ← DB Engineer
- `.vtt/worktrees/backend-qa/` ← QA Engineer

**Regla clave:** TODO lo que un agente produce trabajando en este repo (código + devlog + code_logic) **se commitea junto** en su PR a `memory-service-backend`. Es 1 PR = 1 tarea = todo el contexto en un lugar.

---

### Repo 4: `memory-service-api` — API REST / contratos

Mismo modelo que backend, pero para el repo de API.

```
memory-service-api/
├── src/
├── tests/
├── openapi/                                ← OpenAPI specs
├── docs/
└── knowledge/
    ├── code-logic/
    └── development-log/
```

**Worktrees que tocan este repo:**
- `.vtt/worktrees/api-be/` (cuando se cree)
- `.vtt/worktrees/api-qa/` (cuando se cree)

---

### Repo 5: `memory-service-frontend` — UI

Mismo modelo.

```
memory-service-frontend/
├── src/
├── tests/
├── public/
├── docs/
└── knowledge/
    ├── code-logic/
    └── development-log/
```

**Worktrees que tocan este repo:**
- `.vtt/worktrees/frontend-fe/` (cuando se cree)
- `.vtt/worktrees/frontend-dl/` (cuando se cree, si DL revisa implementación)

---

### Carpeta fuera de repos: `memory-service/.vtt/`

**No es un repo.** Es infraestructura local de operación. NUNCA se commitea.

```
memory-service/.vtt/
├── worktrees/                              ← Worktrees por rol (físicos)
├── workspaces/                             ← .code-workspace por rol
├── manifests/                              ← execution_manifest por tarea (TL crea al asignar)
├── reports/                                ← Reports operacionales (futuro Hook Manager)
├── diffs/                                  ← .patch files (futuro)
├── locks/                                  ← File locks (futuro)
├── agent-runs/                             ← Logs (futuro)
├── memory/                                 ← Memoria persistente del proyecto
├── skills/                                 ← Skills cargadas en runtime
├── manifest.yaml                           ← Manifest VTT del proyecto
└── teams.md                                ← Equipo
```

**Quién escribe aquí:**
- TL crea `manifests/MS-XXX.execution.json` al asignar tarea (no se commitea, queda local)
- Sistema local (no agentes) gestiona el resto

---

## Tabla maestra: cada artefacto, dónde vive

| Artefacto | Repo destino | Worktree de quién lo crea | Termina en PR a... |
|---|---|---|---|
| BRIEF de tarea | memory-service-project | TL | memory-service-project |
| ASSIGNMENT de tarea | memory-service-project | TL | memory-service-project |
| MENSAJE de tarea | memory-service-project | TL | memory-service-project |
| Report SKL-REPORT-01 (extracción) | memory-service-project | TL (al cerrar) | memory-service-project |
| Task Manifest v1.0 | memory-service-project | El agente que ejecuta (paso 15 propio) | memory-service-project (commit del TL al cerrar, o del agente si tiene acceso) |
| Task Manifest v1.5 | memory-service-project | TL (al cerrar) | memory-service-project |
| execution_manifest.json | `.vtt/manifests/` (fuera de repos) | TL al asignar | Nunca (local) |
| Código (.ts/.js/.py) | memory-service-{backend\|api\|frontend} | El agente que ejecuta | El repo correspondiente |
| Tests | Mismo repo del código | El agente que ejecuta | Mismo PR del código |
| Devlog `YYYY-MM-DD_MS-XXX_*.md` | **El repo del código** | El agente que ejecuta | El repo del código |
| Code Logic `.LOGIC.md` | **El repo del código** | El agente que ejecuta | El repo del código |
| Spec técnica de fase (3B.X, 4.X) | memory-service-project/phases/ | El agente que produce la fase | memory-service-project |
| Schema Prisma (cambios) | memory-service-backend/prisma/ | DB Engineer | memory-service-backend |
| Docker config | memory-service-backend/docker/ | DevOps | memory-service-backend |
| VSCode workspace config | memory-service-backend/.vscode/ | TL/DevOps | memory-service-backend |
| Wireframes, Personas, IA | memory-service-project/phases/03-design/ | UX/DL | memory-service-project |
| ADRs | memory-service-project/Release2.0/ARCHITECTURE/ | AR | memory-service-project |
| Templates genéricos | virtual-teams-setup/templates/ | PM Coordinador VTT | virtual-teams-setup (PR separado, fuera de flujo de tareas) |
| SOPs genéricos | virtual-teams-setup/sops/ | PM Coordinador VTT | virtual-teams-setup |
| Reglas globales | virtual-teams-setup/rules/ | PM Coordinador VTT | virtual-teams-setup |

---

## Reglas operativas

### Regla 1 — Un commit, un repo, un PR

Cuando un agente ejecuta una tarea, **todo lo que produce** vive en UN solo repo. Hace 1 commit + 1 PR a ese repo.

**Ejemplo correcto (BE haciendo MS-287):**
```
worktree backend-be:
  src/services/foo.ts           (código)
  tests/unit/foo.test.ts        (test)
  knowledge/code-logic/services/foo.LOGIC.md   (code_logic)
  knowledge/development-log/2026-05-14_MS-287_foo.md   (devlog)

Resultado: 1 PR a memory-service-backend con los 4 archivos.
```

**Ejemplo incorrecto (NO hacer):**
```
worktree backend-be:
  src/services/foo.ts
  tests/unit/foo.test.ts

worktree project-tl (otro repo):
  knowledge/development-log/...   ← MAL: el devlog del BE no va aquí
```

### Regla 2 — Los agentes ejecutores NO tocan `memory-service-project`

El BE, DO, DB, QA, FE **NO escriben** en el repo project. Si necesitan leer su BRIEF o ASSIGNMENT, lo leen:

- Desde **VTT** (el TL lo postea como comment o attachment)
- Con **path absoluto** desde el worktree del TL (solo lectura)

No clonan ni hacen pull de project.

### Regla 3 — El TL es el único que toca `memory-service-project`

Todo lo que es de coordinación (BRIEF, ASSIGNMENT, MENSAJE, manifest, governance) lo crea/edita el TL desde su worktree `.vtt/worktrees/project-tl/`.

Excepciones (cuando una fase está activa con un rol distinto):
- SA escribe en `phases/02-analysis/` desde su worktree `.vtt/worktrees/project-sa/`
- AR escribe en `phases/03-design/architecture/` desde `.vtt/worktrees/project-ar/`
- DL escribe en `phases/03-design/wireframes/` desde `.vtt/worktrees/project-dl/`
- UX escribe en `phases/03-design/personas/`, `phases/03-design/ia/` desde `.vtt/worktrees/project-ux/`
- PM escribe en `knowledge/kickoff/` al inicio

En estos casos, **solo 1 rol a la vez escribe en project** para evitar conflictos. Coordina el TL.

### Regla 4 — `virtual-teams-setup` es solo de lectura durante ejecución

Cero escrituras a `virtual-teams-setup` mientras hay tareas activas en `memory-service`. Si se necesita actualizar un template genérico, se hace en PR separado fuera del flujo de tareas.

### Regla 5 — `.vtt/` no se commitea

Todo lo que vive en `.vtt/` (worktrees, manifests, workspaces, reports, diffs, locks, agent-runs) es operacional local. No se sube a git.

Si necesitas que algo de `.vtt/` quede auditable, **copia** el contenido al repo correspondiente:
- `execution_manifest.json` → resumen en `delivery.execution_context` del Task Manifest v1.5
- `reports/` → extracto en `delivery.skl_report_01_full` del Task Manifest v1.5
- `agent-runs/` → extracto en devlog si hay incidente relevante

---

## Casos especiales

### Caso 1: TL coordina tarea de BE pero también necesita ajustar code_logic

El TL puede leer cualquier code_logic con path absoluto desde el worktree del BE. Si necesita **editarlo**, lo correcto es:

- Opción A: pedir al BE que lo ajuste (escala devuelta al agente)
- Opción B: el TL crea un PR de fix al repo backend desde su propio worktree del backend si tuviera uno (no usa el del BE)

Nunca el TL edita archivos en el worktree del BE.

### Caso 2: Devlog del TL al revisar (APR-TL, observaciones, decisiones de proceso)

Estos van como **comment en VTT** y/o como **devlog_entry tipo "observation"** en VTT. NO como archivo en algún repo.

Si el TL necesita documentar algo persistente, va a `memory-service-project/knowledge/agent-tasks/reports/.../MS-XXX_REPORT.md` (extracto del SKL-REPORT-01) o al manifest v1.5.

### Caso 3: Cambio de scope durante ejecución (agente necesita tocar otro repo)

El agente NO toca el otro repo. Escala al TL. El TL decide:

- Si es trivial: el TL hace el cambio en project desde su worktree
- Si es complejo: el TL crea una sub-tarea para el rol correcto (FE, DB, etc.) con su propio worktree

### Caso 4: Template del repo `virtual-teams-setup` necesita actualizarse

Esto NO es responsabilidad de un agente de proyecto. Es del PM Coordinador VTT. Se hace en un ciclo aparte, en su propio PR a `virtual-teams-setup`, con el flujo VTT propio.

---

## Diagrama de flujo de un PR de tarea

```
Tarea MS-287 asignada al BE
       │
       ├─→ TL en .vtt/worktrees/project-tl/
       │     │
       │     ├─ Crea BRIEF/ASSIGNMENT/MENSAJE/execution_manifest
       │     ├─ Commit + Push + PR a memory-service-project
       │     └─ PM mergea PR
       │
       └─→ BE en .vtt/worktrees/backend-be/
             │
             ├─ git checkout -b feature/MS-287 origin/main
             ├─ Implementa código + tests + code_logic + devlog
             ├─ Commit + Push + PR a memory-service-backend
             ├─ Sube attachments a VTT (devlog, code_logic, manifest v1.0)
             ├─ Postea SKL-REPORT-01 como comment en VTT
             └─ Mueve tarea a task_in_review

       ↓ Cierre

       TL en .vtt/worktrees/project-tl/
         │
         ├─ Revisa PR backend en GitHub
         ├─ FASE A + B + C (modelo dinámico)
         ├─ Actualiza manifest v1.5 en memory-service-project
         ├─ APR-TL comment en VTT
         ├─ Mueve tarea a task_completed
         ├─ Commit + Push + PR del manifest v1.5 a memory-service-project
         └─ PM mergea PR project + PR backend
```

Cada PR es a su repo. Cada repo tiene su historia limpia. Cero archivos cruzados.

---

## Cómo aplicar este documento en flujos existentes

| Documento | Acción |
|---|---|
| `GUIA_WORKTREES_MEMORY_SERVICE.md` | Agregar referencia a este doc y tabla maestra simplificada |
| `OPERATIVO_<ROL>_MEMORY-SERVICE.md` | Cada operativo debe declarar: "Tu repo de escritura es X. Tus artefactos van a Y. NO escribes en Z." |
| `SETUP_<ROL>.md` (en agent-kits) | Working directory primario = worktree del rol. Output destination = repo correspondiente. |
| `gen_mensaje.py` | Escribir MENSAJE_MS-XXX.md en el worktree del TL (no en clon base) |
| `TEMPLATE_ASIGNACION_TAREARev.md` | Paso 14 del workflow del agente debe especificar "todos tus outputs van al repo del worktree donde estás" |

---

## Migración a `virtual-teams-setup`

Este documento es **específico de Memory Service** (menciona repos por nombre y UUIDs). Cuando se migre a `virtual-teams-setup` como SOP genérico:

1. Reemplazar `memory-service-*` por `<project>-*` (placeholder)
2. Reemplazar UUIDs del equipo por roles genéricos
3. Mantener la estructura de las 5 reglas operativas tal cual

Path destino futuro: `virtual-teams-setup/sops/SOP-DOC-LOC-01_ubicacion_documentos.md`

---

## Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| **1.0** | **2026-05-14** | **Versión inicial. Origen: conflictos de escritura cruzada en Sprint S1.** |
