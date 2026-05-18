# ASSIGNMENT: MS-144 / INIT-E-01 — Configurar gobernanza GitHub 4 repos (ADR-001)

```
Hola DO,

El ADR-001 esta aprobado. Tu tarea es implementar las Fases 1 y 2: crear los
Fine-grained PATs por rol y configurar branch protection en los 4 repos de
la org NCoreSys.

### TAREA ASIGNADA

MS-144: INIT-E-01 — Configurar gobernanza GitHub 4 repos (ADR-001 Fases 1+2)
- Estimacion: 6 horas
- Complejidad: MEDIUM
- Categoria: infrastructure (deployment en VTT)
- Prioridad: HIGH
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-E-01_github-governance-4-repos.md
- ADR: memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md

---

### ANTES DE EMPEZAR - LEE ESTO PRIMERO

1. ADR-001 completo — especialmente secciones D-ADR-001-A (PATs) y D-ADR-001-B (branch protection)
2. BRIEF_INIT-E-01_github-governance-4-repos.md — secciones 3 y 4 (pasos detallados)
3. PROJECT_RULES.md §3 y §9

---

### CONTEXTO CRITICO

Los 4 repos en NCoreSys:
    memory-service-project   → docs/ADRs/handoffs (rol PM/PJM)
    memory-service-api       → contrato OpenAPI (rol TL)
    memory-service-backend   → Node.js backend (rol BE/DB)
    memory-service-frontend  → React frontend (rol FE)

IMPORTANTE: Los Fine-grained PATs los crea el Coordinador (Martin Rivas)
manualmente en github.com — NO se pueden crear via API. Tu rol es:
a) Preparar el inventario de PATs requeridos
b) Configurar branch protection via gh CLI
c) Activar security features
d) Documentar todo

---

### CREDENCIALES

Agente DO:
    userId:     322e3745-9756-4a7c-af11-44b33edef44d
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d

GitHub: gh CLI autenticado como NCoreSys

API VTT:
    Base:    http://77.42.88.106:3000

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

---

### ENTREGABLES OBLIGATORIOS

| # | Entregable | Aplica |
|---|------------|--------|
| 1 | PAT_INVENTORY.md (sin valores) | SI |
| 2 | Branch protection confirmada (curl output en DevLog) | SI |
| 3 | Development Log | SI |
| 4 | Code Logic | SI |
| 5 | Git (rama + commit) | SI |

---

### WORKFLOW (12 pasos)

Paso 0: Crear rama
    git checkout -b feature/MS-144

Paso 1: Mover a task_in_progress con credenciales DO

Paso 2: Obtener JWT DO

Paso 3: Verificar que los 4 repos tienen rama main
    for repo in memory-service-project memory-service-api \
                memory-service-backend memory-service-frontend; do
      gh api repos/NCoreSys/$repo/branches --jq '.[].name'
    done

Paso 4 (MANUAL — Coordinador): Crear Fine-grained PATs en github.com
    El DO prepara el inventario y se lo pasa al Coordinador para creacion.
    PATs requeridos (ADR-001 §D-ADR-001-A):
    - PAT_MEM_BE: Write en memory-service-backend
    - PAT_MEM_FE: Write en memory-service-frontend
    - PAT_MEM_DO: Write en memory-service-project, memory-service-api
    - PAT_MEM_TL: Write en todos (review)
    - PAT_MEM_PM: Write en memory-service-project, Read en resto

Paso 5: Configurar branch protection en main (los 4 repos)
    for repo in memory-service-project memory-service-api \
                memory-service-backend memory-service-frontend; do
      gh api repos/NCoreSys/$repo/branches/main/protection \
        --method PUT \
        -f "required_pull_request_reviews[required_approving_review_count]=1" \
        -f "required_pull_request_reviews[dismiss_stale_reviews]=true" \
        -f "enforce_admins=true" \
        -f "allow_force_pushes=false" \
        -f "allow_deletions=false" \
        -F "restrictions=null" \
        -F "required_status_checks=null"
    done

Paso 6: Activar secret scanning y Dependabot
    for repo in memory-service-project memory-service-api \
                memory-service-backend memory-service-frontend; do
      gh api repos/NCoreSys/$repo/vulnerability-alerts --method PUT
    done

Paso 7: Verificar branch protection activa
    for repo in memory-service-project memory-service-api \
                memory-service-backend memory-service-frontend; do
      echo "=== $repo ==="
      gh api repos/NCoreSys/$repo/branches/main/protection \
        --jq '{enforce_admins: .enforce_admins.enabled,
               required_reviews: .required_pull_request_reviews.required_approving_review_count,
               force_push_blocked: .allow_force_pushes.enabled}'
    done

Paso 8: Crear PAT_INVENTORY.md
    knowledge/pat-inventory/PAT_INVENTORY.md
    (sin valores de tokens — solo metadata: nombre, repos, expiracion)

Paso 9: Crear DevLog:
    devlogs/2026-04-24_MS-144_gobernanza-github-4-repos.md

Paso 10: Crear Code Logic:
    knowledge/code-logic/phase1/MS-144_github-governance.LOGIC.md

Paso 11: Commit y push, subir attachments a VTT

Paso 12: Mover a task_in_review

---

### CHECKLIST DE EXITO

- [ ] 4 repos con rama main inicializada
- [ ] Branch protection activa (enforce_admins=true, force_push=false)
- [ ] required_approving_review_count >= 1
- [ ] Secret scanning activado (4 repos)
- [ ] PAT_INVENTORY.md creado (sin valores, solo metadata)
- [ ] DevLog con output de verificacion
- [ ] Si los PATs aun no estan creados: documentar como pendiente y dejar tarea en task_on_hold hasta que Coordinador los genere

---

### FORMATO DE REPORTE AL COMPLETAR

    ## Entrega: MS-144 - INIT-E-01: Gobernanza GitHub 4 repos

    ### Branch protection:
    - memory-service-project: [OK/PENDIENTE]
    - memory-service-api: [OK/PENDIENTE]
    - memory-service-backend: [OK/PENDIENTE]
    - memory-service-frontend: [OK/PENDIENTE]

    ### PATs:
    - Inventario creado: [si/no]
    - PATs generados por Coordinador: [si/no/pendiente]

    ### Security:
    - Secret scanning activo: [4/4 repos]
    - Dependabot activo: [4/4 repos]

    ### Development Log:
    devlogs/2026-04-24_MS-144_gobernanza-github-4-repos.md

    ### Commit SHA: [hash]

---

IMPORTANTE: Si el Coordinador prefiere ejecutar la creacion de PATs directamente,
notificarlo al PM y cerrar esta tarea como "ejecutada por Coordinador".

Saludos,
Tech Lead / PJM (coordinacion Fase 1 Project Setup)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-144_gobernanza-github-4-repos.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
