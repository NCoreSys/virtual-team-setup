# ASSIGNMENT: MS-122 / INIT-B-01 — Crear y verificar repo Git

```
Hola DO,

La decision de arquitectura multi-repo esta aprobada (ADR-001, 2026-04-23).
Los 4 repos ya existen en la org NCoreSys. Tu tarea es verificarlos,
inicializarlos con rama main, y configurar branch protection en cada uno.

### TAREA ASIGNADA

MS-122: INIT-B-01 — Crear y verificar repo Git
- Estimacion: 1 hora
- Complejidad: MEDIUM
- Categoria: deployment
- Prioridad: HIGH
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-B-01_crear-y-verificar-repo-git.md

---

### ANTES DE EMPEZAR - LEE ESTO PRIMERO

1. ADR-001: memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md
   - Seccion 3: URLs de los 4 repos
   - Seccion D-ADR-001-A: tabla de PATs por rol
   - Seccion D-ADR-001-B: reglas de branch protection
2. PROJECT_RULES.md §3 y §9 (workflow, checklist de entrega)
3. Este ASSIGNMENT completo

Config Git (ejecutar antes del primer commit):
    git config user.name "Martin Rivas"
    git config user.email "martin.rivas@prompt-ai.studio"

---

### CONTEXTO CRITICO

Los 4 repos de la org NCoreSys:

    https://github.com/NCoreSys/memory-service-project
    https://github.com/NCoreSys/memory-service-api
    https://github.com/NCoreSys/memory-service-backend
    https://github.com/NCoreSys/memory-service-frontend

El repo local (c:\Users\Martin\Documents\virtual-teams\memory-service\) tiene el
remote mal configurado — apunta a twitter-react.git. Esto se corrige en el Paso 4.

---

### ENTREGABLES OBLIGATORIOS

| # | Entregable | Aplica |
|---|------------|--------|
| 1 | Codigo | NO |
| 2 | Development Log | SI — obligatorio |
| 3 | Code Logic (.LOGIC.md) | NO (no hay codigo) — placeholder minimo |
| 4 | Git (rama + commit + PR) | SI — solo DevLog al repo |
| 5 | Swagger docs | NO |

Attachments requeridos en VTT antes de in_review:
- DevLog (fileType="devlog")
- Code Logic placeholder (fileType="code_logic")
- Comentario/reporte en la tarea

---

### CREDENCIALES

Agente DO:
    userId:     322e3745-9756-4a7c-af11-44b33edef44d
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
    email:      memory-service.devops@vtt.ai

GitHub: gh CLI autenticado como NCoreSys (ya configurado)

API VTT:
    Base:  http://77.42.88.106:3000
    Auth:  POST /api/auth/service-token
    Token: 30 dias de validez

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

---

### WORKFLOW (12 pasos)

Paso 0: Crear rama de Git
    git checkout -b feature/MS-122

Paso 1: Mover tarea a task_in_progress (ya hecho por PJM — verificar)
    curl -s http://77.42.88.106:3000/api/tasks/MS-122 \
      -H "Authorization: Bearer $TOKEN" | python3 -c \
      "import sys,json; print(json.load(sys.stdin)['data']['status']['code'])"
    # debe mostrar: task_in_progress

Paso 2: Obtener JWT con credenciales DO
    python3 -c "
    import urllib.request, json
    req = urllib.request.Request(
        'http://77.42.88.106:3000/api/auth/service-token',
        data=json.dumps({
            'userId': '322e3745-9756-4a7c-af11-44b33edef44d',
            'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'
        }).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        print(json.loads(r.read())['data']['token'])
    " > /tmp/token_do.txt

Paso 3: Verificar existencia de los 4 repos
    for repo in memory-service-project memory-service-api \
                memory-service-backend memory-service-frontend; do
      gh repo view NCoreSys/$repo --json name,url,defaultBranchRef
    done
    # Resultado esperado: los 4 repos accesibles

Paso 4: Corregir remote del repo local
    cd c:\Users\Martin\Documents\virtual-teams\memory-service
    git remote set-url origin \
      https://github.com/NCoreSys/memory-service-project.git
    git remote -v
    # Debe mostrar: NCoreSys/memory-service-project.git

Paso 5: Inicializar rama main en repos que no la tengan
    # Verificar cuales tienen main:
    for repo in memory-service-project memory-service-api \
                memory-service-backend memory-service-frontend; do
      gh api repos/NCoreSys/$repo/branches \
        --jq '.[].name' 2>/dev/null || echo "$repo: sin ramas"
    done
    # Para cada repo sin main: hacer push inicial con README basico

Paso 6: Configurar branch protection en main de los 4 repos (ADR-001 §D-ADR-001-B)
    for repo in memory-service-project memory-service-api \
                memory-service-backend memory-service-frontend; do
      gh api repos/NCoreSys/$repo/branches/main/protection \
        --method PUT \
        --field required_status_checks=null \
        --field enforce_admins=true \
        --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
        --field restrictions=null \
        --field allow_force_pushes=false \
        --field allow_deletions=false
    done

Paso 7: Activar security features en los 4 repos
    for repo in memory-service-project memory-service-api \
                memory-service-backend memory-service-frontend; do
      gh api repos/NCoreSys/$repo/vulnerability-alerts \
        --method PUT 2>/dev/null
    done

Paso 8: Verificar clone funciona
    cd /tmp && git clone \
      https://github.com/NCoreSys/memory-service-project.git \
      ms-verify-clone
    cd ms-verify-clone && git remote -v
    # Debe mostrar la URL correcta
    cd /tmp && rm -rf ms-verify-clone

Paso 9: Crear Development Log
    devlogs/2026-04-24_MS-122_crear-verificar-repo-git.md

Paso 10: Crear Code Logic placeholder
    knowledge/code-logic/phase1/MS-122_no-code.LOGIC.md

Paso 11: Subir attachments a VTT y postear comentario de entrega en MS-122

Paso 12: Mover MS-122 a task_in_review

---

### CHECKLIST DE VERIFICACION

- [ ] 4 repos accesibles via gh repo view
- [ ] Rama main existe en los 4 repos
- [ ] Remote local corregido (ya no apunta a twitter-react.git)
- [ ] git clone funciona con la URL correcta
- [ ] Branch protection configurada en main (los 4 repos)
- [ ] allow_force_pushes = false
- [ ] allow_deletions = false
- [ ] required_approving_review_count >= 1

---

### ARCHIVOS A CREAR

    devlogs/2026-04-24_MS-122_crear-verificar-repo-git.md
    knowledge/code-logic/phase1/MS-122_no-code.LOGIC.md

---

### FORMATO DE REPORTE AL COMPLETAR

    ## Entrega: MS-122 - INIT-B-01: Crear y verificar repo Git

    ### Repos verificados:
    - memory-service-project: [URL] — main: [si/no] — protection: [si/no]
    - memory-service-api: [URL] — main: [si/no] — protection: [si/no]
    - memory-service-backend: [URL] — main: [si/no] — protection: [si/no]
    - memory-service-frontend: [URL] — main: [si/no] — protection: [si/no]

    ### Remote local corregido:
    origin -> https://github.com/NCoreSys/memory-service-project.git

    ### Clone verificado: [si/no]

    ### Development Log:
    devlogs/2026-04-24_MS-122_crear-verificar-repo-git.md

    ### Commit SHA: [hash]

---

Empieza por el Paso 3 (verificar repos). Si algun repo no tiene rama main,
inicializalo antes de configurar branch protection.

Saludos,
Tech Lead / PJM (coordinacion Fase 1 Project Setup)
```

---

## Metadata del archivo

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-122_crear-verificar-repo-git.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready para asignar

## Fuentes consultadas

| Artefacto | Dato extraido |
|-----------|---------------|
| ADR-001 §3 | URLs de los 4 repos en NCoreSys |
| ADR-001 §D-ADR-001-A | Credenciales DO (UUID, serviceKey) |
| ADR-001 §D-ADR-001-B | Reglas de branch protection |
| BRIEF_INIT-B-01 | Criterios de exito, objetivo |
| gh repo view (verificado) | 4 repos existen, sin rama main aun |
| git remote -v (verificado) | Remote local apunta a twitter-react.git |
