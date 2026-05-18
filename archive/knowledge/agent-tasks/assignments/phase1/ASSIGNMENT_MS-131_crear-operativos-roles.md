# ASSIGNMENT: MS-131 / INIT-D-01 — Crear OPERATIVO por cada rol activo

```
Hola PM,

Tenemos 2 de 12 OPERATIVOs completos (PM y TL). Esta tarea es crear los 10
restantes. Prioridad: BE, DB, DO antes de que arranque el Sprint S01.

### TAREA ASIGNADA

MS-131: INIT-D-01 — Crear OPERATIVO por cada rol activo
- Estimacion: 3 horas
- Complejidad: MEDIUM
- Categoria: documentation
- Prioridad: HIGH
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-D-01_crear-operativo-por-cada-rol-activo.md

---

### ANTES DE EMPEZAR

1. Leer OPERATIVOs existentes como referencia:
   - .claude/agents/OPERATIVO_PM_MEMORY-SERVICE.md
   - .claude/agents/OPERATIVO_TECH_LEAD.md
2. .claude/rules/Proyect_data.md — UUIDs de todos los roles
3. .claude/rules/PROJECT_RULES.md — reglas del proyecto
4. memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md §stack

---

### CREDENCIALES

Agente PM:
    userId:     350831b2-e1ae-4dbe-b2eb-7e023ec2e103
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
    email:      pm@memory-service.vtt.ai

---

### OPERATIVOs A CREAR (10 pendientes)

Ubicacion: .claude/agents/OPERATIVO_<ROL>_MEMORY-SERVICE.md

| Archivo | UUID | Email | Prioridad |
|---------|------|-------|-----------|
| OPERATIVO_PJM_MEMORY-SERVICE.md | 0ff63a29-0bc0-465a-b9bd-5f71476bc91d | pjm@memory-service.vtt.ai | Alta |
| OPERATIVO_BE_MEMORY-SERVICE.md  | ebbe3cee-abed-4b3b-860d-0a81f632b08a | memory-service.be@vtt.ai  | 🔴 ANTES S01 |
| OPERATIVO_DB_MEMORY-SERVICE.md  | 6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7 | memory-service.db@vtt.ai  | 🔴 ANTES S01 |
| OPERATIVO_DO_MEMORY-SERVICE.md  | 322e3745-9756-4a7c-af11-44b33edef44d | memory-service.devops@vtt.ai | 🔴 ANTES S01 |
| OPERATIVO_FE_MEMORY-SERVICE.md  | d23c9cd9-a156-433b-8900-94add5488eec | memory-service.fe@vtt.ai  | Media |
| OPERATIVO_QA_MEMORY-SERVICE.md  | 613c9538-658c-45fe-a6d7-c1ea9ff04b78 | memory-service.qa@vtt.ai  | Media |
| OPERATIVO_SA_MEMORY-SERVICE.md  | 0c128e3b-db3b-4e31-b107-0379b5791233 | sa@memory-service.vtt.ai  | Media |
| OPERATIVO_AR_MEMORY-SERVICE.md  | e9403c25-c1f8-4b64-b2ef-f447d53115e2 | ar@memory-service.vtt.ai  | Media |
| OPERATIVO_UX_MEMORY-SERVICE.md  | a75a1dae-754a-4b6f-a3ff-db8d51f6a91b | memory-service.ux@vtt.ai  | Baja |
| OPERATIVO_DL_MEMORY-SERVICE.md  | b3a09269-cded-468c-a475-15a48f203cb0 | memory-service.dl@vtt.ai  | Baja |

---

### ESTRUCTURA DE CADA OPERATIVO

Usar OPERATIVO_PM_MEMORY-SERVICE.md como plantilla. Cada archivo debe incluir:

1. **Identidad del agente**: rol, UUID, email, serviceKey
2. **Responsabilidades**: qué hace este rol en el proyecto
3. **Fases donde actúa**: qué tareas le pertenecen
4. **Stack técnico relevante**: solo lo que usa su rol
5. **Endpoints VTT**: auth + tasks de su rol
6. **Reglas críticas**: refs a PROJECT_RULES.md secciones relevantes
7. **Repos GitHub**: cuál es su repo de escritura (ADR-001)
8. **Rutina de apertura de sesión**: qué leer al arrancar

---

### ENTREGABLES OBLIGATORIOS

| # | Entregable | Aplica |
|---|------------|--------|
| 1 | 10 archivos OPERATIVO_<ROL>.md | SI |
| 2 | Development Log | SI |
| 3 | Code Logic placeholder | SI |
| 4 | Git (rama + commit) | SI |

---

### WORKFLOW (12 pasos)

Paso 0: git checkout -b feature/MS-131

Paso 1: Mover MS-131 a task_in_progress con credenciales PM

Paso 2: Leer OPERATIVO_PM como plantilla

Paso 3: Crear los 3 prioritarios primero (BE, DB, DO)

Paso 4: Crear los 7 restantes (PJM, FE, QA, SA, AR, UX, DL)

Paso 5: Verificar que son 12 en total:
    ls .claude/agents/OPERATIVO_*.md | wc -l
    # debe dar 12

Paso 6: Crear DevLog:
    devlogs/2026-04-24_MS-131_crear-operativos-roles.md

Paso 7: Crear Code Logic placeholder:
    knowledge/code-logic/phase1/MS-131_no-code.LOGIC.md

Paso 8: Commit y push de los 10 archivos nuevos

Paso 9: Subir attachments a VTT (devlog, code_logic)

Paso 10: Postear comentario de entrega en MS-131

Paso 11: Mover MS-131 a task_in_review

---

### CHECKLIST DE EXITO

- [ ] OPERATIVO_BE.md creado
- [ ] OPERATIVO_DB.md creado
- [ ] OPERATIVO_DO.md creado
- [ ] OPERATIVO_PJM.md creado
- [ ] OPERATIVO_FE.md creado
- [ ] OPERATIVO_QA.md creado
- [ ] OPERATIVO_SA.md creado
- [ ] OPERATIVO_AR.md creado
- [ ] OPERATIVO_UX.md creado
- [ ] OPERATIVO_DL.md creado
- [ ] Total: 12 OPERATIVOs en .claude/agents/

---

### FORMATO DE REPORTE

    ## Entrega: MS-131 - INIT-D-01: OPERATIVOs por rol

    ### Archivos creados (10):
    - OPERATIVO_BE_MEMORY-SERVICE.md ✅
    - OPERATIVO_DB_MEMORY-SERVICE.md ✅
    - OPERATIVO_DO_MEMORY-SERVICE.md ✅
    - [resto...]

    ### Total en .claude/agents/: [N]/12

    ### Development Log:
    devlogs/2026-04-24_MS-131_crear-operativos-roles.md

    ### Commit SHA: [hash]

---

Saludos,
PJM (coordinación Fase 1)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-131_crear-operativos-roles.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
