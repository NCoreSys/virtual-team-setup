# ASSIGNMENT: MS-132 / INIT-D-02 — Consolidar PROJECT_MEMORY.md

```
Hola PM,

El proyecto Memory Service tiene contexto disperso en varios documentos.
Tu tarea es consolidar toda la informacion persistente en PROJECT_MEMORY.md
para que cualquier agente pueda arrancar una sesion leyendo solo ese archivo.

### TAREA ASIGNADA

MS-132: INIT-D-02 — Consolidar PROJECT_MEMORY.md
- Estimacion: 1 hora
- Complejidad: LOW
- Categoria: documentation
- Prioridad: MEDIUM
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-D-02_consolidar-project_memorymd.md

---

### ANTES DE EMPEZAR - LEE ESTO PRIMERO

1. knowledge/PROJECT_MEMORY.md — archivo existente (verificar su estado actual)
2. memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md
3. memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md
4. .claude/rules/PROJECT_RULES.md (PROJECT_RULES §8 — configuracion repo)
5. .claude/rules/Proyect_data.md — UUIDs del equipo

---

### CREDENCIALES

Agente PM:
    userId:     350831b2-e1ae-4dbe-b2eb-7e023ec2e103
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
    email:      pm@memory-service.vtt.ai

API VTT:
    Base:    http://77.42.88.106:3000
    Auth:    POST /api/auth/service-token

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

---

### ENTREGABLES OBLIGATORIOS

| # | Entregable | Aplica |
|---|------------|--------|
| 1 | knowledge/PROJECT_MEMORY.md (actualizado) | SI |
| 2 | Development Log | SI |
| 3 | Code Logic placeholder | SI (gate VTT) |
| 4 | Git (rama + commit) | SI |
| 5 | Swagger | NO |

---

### CONTENIDO MINIMO DE PROJECT_MEMORY.md

El archivo debe tener al menos estas 5 secciones:

1. **Proyecto** — nombre, key MS, projectId, descripcion, status
2. **Stack tecnico** — Node 20 + Express + Prisma + PostgreSQL + Redis + React + Vite
3. **Fases y horas** — 10 fases, 381h totales, estado actual por fase
4. **Equipo** — roles y UUIDs (tabla de .claude/rules/Proyect_data.md)
5. **Decisiones aprobadas** — ADR-001 (polirrepo 4 repos, NCoreSys org)
6. **4 Repos GitHub** — URLs de memory-service-project/api/backend/frontend
7. **Referencias clave** — SPEC v1.9, PROJECT_RULES v1.5, ADR-001

---

### WORKFLOW (12 pasos)

Paso 0: Crear rama
    git checkout -b feature/MS-132

Paso 1: Mover a task_in_progress con tus credenciales PM

Paso 2: Leer el archivo actual
    cat knowledge/PROJECT_MEMORY.md

Paso 3: Leer SPEC v1.9 para extraer stack tecnico y puertos
    memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md

Paso 4: Extraer UUIDs del equipo de .claude/rules/Proyect_data.md

Paso 5: Consultar estado actual de fases en VTT
    GET http://77.42.88.106:3000/api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803

Paso 6: Actualizar/crear knowledge/PROJECT_MEMORY.md con las 7 secciones

Paso 7: Verificar que tiene al menos 5 secciones (criterio del BRIEF)

Paso 8: Crear DevLog en:
    devlogs/2026-04-24_MS-132_consolidar-project-memory.md

Paso 9: Crear Code Logic placeholder:
    knowledge/code-logic/phase1/MS-132_no-code.LOGIC.md

Paso 10: Commit y push
    git add knowledge/PROJECT_MEMORY.md \
      devlogs/2026-04-24_MS-132_consolidar-project-memory.md \
      knowledge/code-logic/phase1/MS-132_no-code.LOGIC.md
    git commit -m "docs [MS-132]: Consolidar PROJECT_MEMORY.md"

Paso 11: Subir attachments a VTT, postear comentario, mover a task_in_review

---

### FORMATO DE REPORTE AL COMPLETAR

    ## Entrega: MS-132 - INIT-D-02: Consolidar PROJECT_MEMORY.md

    ### Archivo:
    knowledge/PROJECT_MEMORY.md — [N] secciones, [N] lineas

    ### Secciones incluidas:
    - [x] Proyecto (nombre, key, projectId)
    - [x] Stack tecnico
    - [x] Fases y horas
    - [x] Equipo (UUIDs)
    - [x] Decisiones ADR-001
    - [x] Repos GitHub
    - [x] Referencias clave

    ### Development Log:
    devlogs/2026-04-24_MS-132_consolidar-project-memory.md

    ### Commit SHA: [hash]

---

Saludos,
Tech Lead / PJM (coordinacion Fase 1 Project Setup)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-132_consolidar-project-memory.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
