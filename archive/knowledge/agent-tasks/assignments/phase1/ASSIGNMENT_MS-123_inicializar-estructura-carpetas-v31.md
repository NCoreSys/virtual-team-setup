# ASSIGNMENT: MS-123 / INIT-B-02 — Inicializar estructura de carpetas V3.1

```
Hola PJM,

Esta tarea te corresponde directamente como PJM coordinando el setup del repo.
El objetivo es crear la estructura de carpetas estándar V3.1 en memory-service-project.

### TAREA ASIGNADA

MS-123: INIT-B-02 — Inicializar estructura de carpetas V3.1
- Estimacion: 1 hora
- Complejidad: LOW
- Categoria: documentation
- Prioridad: MEDIUM
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-B-02_inicializar-estructura-de-carpetas-v31.md

---

### ANTES DE EMPEZAR

1. Este ASSIGNMENT completo
2. PROJECT_RULES.md §13 (estructura de carpetas)
3. HO_INICIACION_MEMORY_SERVICE.md §B (Repository Setup)

---

### CREDENCIALES

Agente PJM:
    userId:     0ff63a29-0bc0-465a-b9bd-5f71476bc91d
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
    email:      pjm@memory-service.vtt.ai

API VTT:
    Base:    http://77.42.88.106:3000
    Auth:    POST /api/auth/service-token

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

---

### CONTEXTO

El repo memory-service-project ya existe en GitHub (NCoreSys/memory-service-project).
La estructura V3.1 define dónde van los artefactos de cada fase del proyecto, permitiendo que
todos los agentes encuentren docs de forma consistente.

---

### ESTRUCTURA A CREAR

En el repo memory-service-project (local: memory-service/memory-service-project):

```
memory-service-project/
├── phases/
│   ├── 00-discovery/
│   ├── 01-planning/
│   ├── 02-analysis/
│   ├── 03-design/
│   ├── 04-development/
│   ├── 05-testing/
│   ├── 06-deploy/
│   └── 07-operations/
├── _pm/
│   └── (planes, reportes, sprints)
├── docs/
│   └── (documentación técnica general)
├── archive/
│   └── (versiones anteriores, docs deprecados)
└── .claude/
    └── agents/
        └── (OPERATIVOs de cada rol)
```

Cada carpeta debe tener un `.gitkeep` para que Git la trackee.
Crear también un `README.md` raíz que explique cada carpeta.

---

### WORKFLOW (12 pasos)

Paso 0: Verificar rama actual
    git checkout feature/MS-123
    # o crear: git checkout -b feature/MS-123

Paso 1: Mover MS-123 a task_in_progress con credenciales PJM

Paso 2: Crear las carpetas con .gitkeep
    mkdir -p memory-service-project/phases/{00-discovery,01-planning,02-analysis,\
      03-design,04-development,05-testing,06-deploy,07-operations}
    mkdir -p memory-service-project/{_pm,docs,archive}
    mkdir -p memory-service-project/.claude/agents
    find memory-service-project/phases memory-service-project/_pm \
         memory-service-project/docs memory-service-project/archive \
         -type d -exec touch {}/.gitkeep \;

Paso 3: Crear README.md en memory-service-project/
    Explicar propósito de cada carpeta (phases/, _pm/, docs/, archive/, .claude/)

Paso 4: Verificar estructura
    ls -la memory-service-project/phases/
    # Debe mostrar las 8 subcarpetas (00-discovery..07-operations)

Paso 5: Crear DevLog:
    devlogs/2026-04-24_MS-123_estructura-carpetas-v31.md

Paso 6: Crear Code Logic placeholder:
    knowledge/code-logic/phase1/MS-123_estructura-carpetas.LOGIC.md
    (no hay código — solo documentación de la estructura)

Paso 7: Commit y push
    git add memory-service-project/
    git commit -m "docs [MS-123]: Inicializar estructura carpetas V3.1

    - Crear phases/00-discovery..07-operations
    - Crear _pm/, docs/, archive/, .claude/agents/
    - README.md con descripcion de cada carpeta

    Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
    Refs: #MS-123"
    git push origin feature/MS-123

Paso 8: Subir attachments a VTT (devlog, code_logic)

Paso 9: Postear comentario de entrega en MS-123

Paso 10: Mover MS-123 a task_in_review

---

### CHECKLIST DE EXITO

- [ ] phases/00-discovery..07-operations creadas (8 carpetas)
- [ ] _pm/ creada
- [ ] docs/ creada
- [ ] archive/ creada
- [ ] .claude/agents/ creada
- [ ] README.md raíz explica cada carpeta
- [ ] git ls-files muestra las carpetas (via .gitkeep)
- [ ] DevLog completo
- [ ] Commit + Push realizado

---

### FORMATO DE REPORTE

    ## Entrega: MS-123 - INIT-B-02: Estructura V3.1

    ### Carpetas creadas:
    - phases/ (8 subcarpetas) ✅
    - _pm/ ✅
    - docs/ ✅
    - archive/ ✅
    - .claude/agents/ ✅
    - README.md ✅

    ### Development Log:
    devlogs/2026-04-24_MS-123_estructura-carpetas-v31.md

    ### Commit SHA: [hash]

---

Saludos,
PJM (auto-asignación)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-123_inicializar-estructura-carpetas-v31.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
