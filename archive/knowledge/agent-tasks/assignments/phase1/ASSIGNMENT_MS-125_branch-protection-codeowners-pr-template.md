# ASSIGNMENT: MS-125 / INIT-B-04 — Branch protection + CODEOWNERS + PR template

```
Hola DO,

Esta tarea complementa MS-144 (gobernanza GitHub). MS-144 configuró branch protection
via gh CLI. Esta tarea agrega los archivos CODEOWNERS y PR template dentro del repo
memory-service-project, y verifica que la protección esté activa.

### TAREA ASIGNADA

MS-125: INIT-B-04 — Branch protection + CODEOWNERS + PR template
- Estimacion: 1 hora
- Complejidad: MEDIUM
- Categoria: deployment
- Prioridad: MEDIUM
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-B-04_branch-protection-+-codeowners-+-pr-temp.md

---

### ANTES DE EMPEZAR

1. Este ASSIGNMENT completo
2. PROJECT_RULES.md §15.2 (nunca commit directo a main)
3. ADR-001 §D-ADR-001-B (branch protection rules)
4. Verificar que MS-144 está completada (branch protection ya activa en los 4 repos)

---

### CREDENCIALES

Agente DO:
    userId:     322e3745-9756-4a7c-af11-44b33edef44d
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
    email:      memory-service.devops@vtt.ai

GitHub: gh CLI autenticado como NCoreSys

API VTT:
    Base:    http://77.42.88.106:3000

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

---

### CONTEXTO

MS-144 ya configuró branch protection en los 4 repos via gh CLI.
Esta tarea agrega los archivos que van DENTRO del repo:
1. CODEOWNERS — define quién debe aprobar PRs por área
2. PR template — obliga a incluir TASK_ID y descripción en cada PR

Repo objetivo: memory-service-project (es el repo de documentación/governance)

---

### ARCHIVOS A CREAR

#### 1. CODEOWNERS
Ubicación: `memory-service-project/.github/CODEOWNERS`

```
# Memory Service — Code Owners
# Formato: <patrón> <owner1> <owner2>

# Owners globales (todo el repo)
*   @NCoreSys/tech-lead @NCoreSys/project-manager

# Documentación de arquitectura
/phases/03-design/   @NCoreSys/tech-lead
/phases/04-development/  @NCoreSys/tech-lead

# Infra y DevOps
/phases/06-deploy/   @NCoreSys/devops-engineer
```

#### 2. PR Template
Ubicación: `memory-service-project/.github/pull_request_template.md`

```markdown
## [TASK_ID] Descripción del cambio

<!-- Reemplaza TASK_ID con el ID de la tarea VTT (ej: MS-123) -->

### Tipo de cambio
- [ ] feat — Nueva funcionalidad
- [ ] fix — Corrección de bug
- [ ] docs — Solo documentación
- [ ] chore — Mantenimiento

### Descripción
<!-- Qué cambió y por qué -->

### Checklist
- [ ] Sigo las convenciones de PROJECT_RULES.md
- [ ] Creé/actualicé archivos .LOGIC.md correspondientes
- [ ] Creé Development Log en devlogs/
- [ ] No hay commits directos a main

### Link a tarea VTT
Task: MS-XXX
```

---

### WORKFLOW (12 pasos)

Paso 0: Crear rama
    git checkout -b feature/MS-125

Paso 1: Mover MS-125 a task_in_progress con credenciales DO

Paso 2: Verificar que branch protection de MS-144 está activa
    gh api repos/NCoreSys/memory-service-project/branches/main/protection \
      --jq '{enforce_admins: .enforce_admins.enabled, required_reviews: .required_pull_request_reviews.required_approving_review_count}'

Paso 3: Crear directorio .github si no existe
    mkdir -p memory-service-project/.github

Paso 4: Crear CODEOWNERS
    (contenido arriba)

Paso 5: Crear pull_request_template.md
    (contenido arriba)

Paso 6: Commit y push
    git add memory-service-project/.github/
    git commit -m "chore [MS-125]: Agregar CODEOWNERS y PR template

    - .github/CODEOWNERS define owners por área
    - .github/pull_request_template.md obliga a linkear TASK_ID

    Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
    Refs: #MS-125"
    git push origin feature/MS-125

Paso 7: Crear PR y verificar que el template aparece
    gh pr create --title "[MS-125] Agregar CODEOWNERS y PR template" \
      --body "Ver devlog para detalles." --base main
    # Verificar que el template se carga en la UI

Paso 8: Crear DevLog:
    devlogs/2026-04-24_MS-125_codeowners-pr-template.md

Paso 9: Crear Code Logic:
    knowledge/code-logic/phase1/MS-125_codeowners-pr-template.LOGIC.md

Paso 10: Subir attachments a VTT (devlog, code_logic)

Paso 11: Postear comentario de entrega en MS-125

Paso 12: Mover MS-125 a task_in_review

---

### CHECKLIST DE EXITO

- [ ] Branch protection verificada activa en memory-service-project
- [ ] .github/CODEOWNERS creado y commiteado
- [ ] .github/pull_request_template.md creado y commiteado
- [ ] PR de prueba muestra el template automáticamente
- [ ] DevLog con output de verificación
- [ ] Commit + Push + PR realizados

---

### FORMATO DE REPORTE

    ## Entrega: MS-125 - INIT-B-04: Branch protection + CODEOWNERS + PR template

    ### Branch protection (verificación):
    - enforce_admins: [true/false]
    - required_reviews: [N]

    ### Archivos creados:
    - .github/CODEOWNERS ✅
    - .github/pull_request_template.md ✅

    ### PR template verificado: [si/no]

    ### Development Log:
    devlogs/2026-04-24_MS-125_codeowners-pr-template.md

    ### Commit SHA: [hash]

---

Saludos,
PJM (coordinación Fase 1 Project Setup)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-125_branch-protection-codeowners-pr-template.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
