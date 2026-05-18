#!/usr/bin/env python3
"""
Memory Service R1 — Restructure Phase 1 Project Setup
=====================================================

Objetivo:
  1. Cancelar las 5 tareas umbrella MEM-001..005 (no borrar, solo cancel)
  2. Renombrar el delivery 'Project Foundation Ready' a 'A. VTT Setup'
  3. Crear 6 deliveries nuevos: B Repo, C VM, D Team, E Tooling, F Docs, G Kickoff
  4. Crear 26 tareas INIT-A..G atomicas vinculadas a sus deliveries
  5. Guardar los nuevos UUIDs en VTT_UUIDS_PHASE1_RESTRUCTURED.json

Requiere:
  VTT_SERVICE_KEY como variable de entorno.
  Python 3.8+.
"""

import os, sys, json, time, urllib.request, urllib.error

API_URL     = os.environ.get("VTT_API_URL", "http://77.42.88.106:3000")
SERVICE_KEY = os.environ.get("VTT_SERVICE_KEY")
if not SERVICE_KEY:
    sys.exit("ERROR: Define VTT_SERVICE_KEY antes de ejecutar.")

PJM_UUID = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"

# ── Contexto del proyecto (obtenido previamente) ─────────────────────────────
PROJECT_ID = "d0fc276d-e764-4a83-96e9-d65f086ed803"
PHASE_PROJECT_SETUP_ID = "52c37a8b-70de-48e6-80fb-30032805025e"
DELIVERY_OLD_ID = "98a0be7a-c703-4bd3-a905-63b070e389d3"  # Project Foundation Ready

# ── UUIDs de usuarios ────────────────────────────────────────────────────────
USERS = {
    "PM":  "350831b2-e1ae-4dbe-b2eb-7e023ec2e103",
    "PJM": "0ff63a29-0bc0-465a-b9bd-5f71476bc91d",
    "TL":  "92225290-6b6b-4c1f-a940-dcb4262507aa",
    "DO":  "322e3745-9756-4a7c-af11-44b33edef44d",
}

# ── UUIDs de status y prioridad ──────────────────────────────────────────────
STATUS = {
    "pending":    "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
    "completed":  "aa5ceb90-5209-42a2-b874-a8cbee597a97",
    "cancelled":  "b9488db1-2969-43aa-b804-3fcb49f355a4",
    "in_progress":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56",
    "blocked":    "c897cbd6-99b9-4640-a760-e0056384fae5",
}
PRIORITY = {
    "C": "90ec3df2-fac4-40fa-b2ce-29daf0f4956e",
    "H": "1a617554-6319-4c56-826f-8ef49a0ff9cc",
    "M": "d0b619ef-27e7-42d8-8879-41030a602eed",
    "L": "95f2e731-41b9-4a7d-9a43-31f00a4ddd7e",
}

# ── Tareas umbrella a cancelar ───────────────────────────────────────────────
UMBRELLA_TASKS = ["MS-001", "MS-002", "MS-003", "MS-004", "MS-005"]

# ── Deliveries nuevos (el old se renombra al A, luego B..G son nuevos) ───────
NEW_DELIVERIES = [
    # (order, name, description)
    (2, "B. Repository Setup",  "Repositorio Git, estructura V3.1, branch protection y conventions."),
    (3, "C. VM Configuration",  "Verificar infraestructura Hetzner, conectividad y docs de infra."),
    (4, "D. Agent Team Setup",  "OPERATIVOs por rol, contextos de sesion, accesos y onboarding."),
    (5, "E. Tooling Setup",     "Node + TypeScript + linters + formatters + CI minimo."),
    (6, "F. Documentation",     "README, CONTRIBUTING y ARCHITECTURE del repo."),
    (7, "G. Kickoff",           "Documento formal de kickoff y sesion de arranque del equipo."),
]

# ── 26 tareas INIT-A..G (task_id, delivery_key, titulo, rol, horas, complex, status, desc) ───
# delivery_key = letra (A..G) para mapear al deliveryId
TASKS = [
    # ── A. VTT Setup (PJM, 6h) ───────────────────────────────────────────────
    ("INIT-A-01", "A", "Verificar proyecto en VTT", "PJM", 1, "LOW", "completed",
     "Confirmar que el Project 'Memory Service R1' existe en VTT con la key MEM y ownerId del PM. Verificar que el projectId es d0fc276d-e764-4a83-96e9-d65f086ed803. Entregable: captura o registro del estado del proyecto."),
    ("INIT-A-02", "A", "Verificar 10 fases en VTT", "PJM", 1, "LOW", "completed",
     "Listar las 10 fases del proyecto via GET /api/projects/{id}/phases. Validar que los nombres y order coinciden con el plan (Project Setup, Discovery, Planning, Analysis, Design UX/UI, Design Technical, Development, Testing, Deploy, Operations). Guardar UUIDs en PROJECT_MEMORY."),
    ("INIT-A-03", "A", "Verificar 65 deliveries en VTT", "PJM", 1, "LOW", "completed",
     "Recorrer cada fase y listar sus deliveries via GET /api/phases/{id}/deliveries. Validar que el total es 65 deliveries distribuidos segun el plan maestro. Guardar UUIDs en VTT_UUIDS_MEMORY_SERVICE.json."),
    ("INIT-A-04", "A", "PATCH 116 tareas en VTT con metadata completa", "PJM", 2, "MEDIUM", "pending",
     "Verificar que las 116 tareas del proyecto tienen asignados correctamente: assigneeId, complexity (MAYUSCULAS), category, estimatedHours, priorityId. Aplicar reassignments documentados: MEM-022 a SA y MEM-039 a AR. Entregable: reporte de 116 tareas con metadata validada."),
    ("INIT-A-05", "A", "Crear 15 dependencias criticas en VTT", "PJM", 3, "MEDIUM", "pending",
     "Registrar las 15 dependencias criticas inter-fase via POST /api/tasks/{id}/dependencies. Incluye: Discovery->Planning, Analysis->Design, Design Tech->BE, Design UX->FE (MEM-038->MEM-081 HITO), BE+FE->Testing, Testing->Deploy, Deploy->Operations. Entregable: 15 dependencias visibles en Gantt."),

    # ── B. Repository Setup (PJM + DO, 5h) ───────────────────────────────────
    ("INIT-B-01", "B", "Crear y verificar repo Git", "DO", 1, "MEDIUM", "blocked",
     "Crear repo Git en GitHub para Memory Service con URL correcta (NO debe apuntar a twitter-react.git). BLOQUEADO: requiere que el PM defina el esquema multi-repo (PROJECT_RULES §8). Sin esto, toda la categoria B queda bloqueada. Entregable: URL del repo funcional."),
    ("INIT-B-02", "B", "Inicializar estructura de carpetas V3.1", "PJM", 1, "LOW", "pending",
     "Crear estructura V3.1 del repo: phases/00-discovery/ a phases/07-operations/, _pm/, docs/, archive/, .claude/agents/. Basarse en el plan PROJECT_RULES y HO_INICIACION §3.B. Entregable: estructura inicial committeada."),
    ("INIT-B-03", "B", "Configurar archivos base del repo", "PJM", 1, "LOW", "pending",
     ".gitignore (node_modules, dist, .env, storage), .gitattributes, .editorconfig (2 spaces TS, LF), README.md inicial, CONTRIBUTING.md con flujo de PRs. Entregable: 5 archivos committeados."),
    ("INIT-B-04", "B", "Branch protection + CODEOWNERS + PR template", "DO", 1, "MEDIUM", "pending",
     "Activar branch protection en main (requires PR, requires review, requires status checks). Crear .github/CODEOWNERS con PM y TL como owners globales. Crear .github/pull_request_template.md con checklist de review. Entregable: protecciones visibles en GitHub Settings."),
    ("INIT-B-05", "B", "Git user config + commit conventions", "PJM", 1, "LOW", "pending",
     "Configurar user.name='Martin Rivas' y user.email='martin.rivas@prompt-ai.studio' en el repo. Documentar convention de commits '[tipo] [TASK_ID]: desc' con Co-Authored-By obligatorio. Entregable: CONTRIBUTING actualizado con convention, git config verificado."),

    # ── C. VM Configuration (DO, 4h) ─────────────────────────────────────────
    ("INIT-C-01", "C", "Verificar infraestructura provisionada en Hetzner", "DO", 1, "MEDIUM", "completed",
     "Verificar que existen: BD memory_service_db accesible desde shared-postgres, volumen /root/memory-service-storage/ con permisos correctos, Redis prefix mem accesible, firewall abierto en puertos 3002 (API) y 3003 (UI), shared-network Docker. Entregable: checklist en docs/INFRASTRUCTURE.md."),
    ("INIT-C-02", "C", "Tests de conectividad local a VM", "DO", 1, "MEDIUM", "pending",
     "Validar conectividad desde maquina local hacia la VM: conexion Prisma a memory_service_db OK, escritura en /root/memory-service-storage/ desde container OK, Redis ping OK, curl http://77.42.88.106:3002/health responde. Entregable: reporte de tests en INFRASTRUCTURE.md."),
    ("INIT-C-03", "C", "Distribuir SERVICE_KEY a consumidores", "DO", 1, "MEDIUM", "pending",
     "Entregar SERVICE_KEY a los consumidores del Memory Service: Runtime v1.1, Prompt Builder v1.3, Hook Manager, FE (variable env). Documentar a quien se entrego y verificar cada uno puede autenticarse. Entregable: confirmacion de los 4 consumidores."),
    ("INIT-C-04", "C", "Documentar configuracion VM en repo", "DO", 1, "LOW", "pending",
     "Escribir docs/INFRASTRUCTURE.md con: IP servidor (77.42.88.106), puertos (3002 API, 3003 UI), paths (/root/memory-service-storage/), schema de backups, procedimiento de escalacion al Admin VM. Entregable: INFRASTRUCTURE.md committeado."),

    # ── D. Agent Team Setup (PM + PJM, 8h) ───────────────────────────────────
    ("INIT-D-01", "D", "Crear OPERATIVO por cada rol activo", "PM", 3, "MEDIUM", "in_progress",
     "Crear .claude/agents/OPERATIVO_<ROL>.md para los 12 roles: PM, PJM, TL, SA, AR, BE, DB, FE, UX, DL, QA, DO. Cada uno incluye: funciones, tokens, endpoints VTT que usa, referencias a reglas. Hechos: PM, TL. Pendientes: 10. Prioridad: BE + DB + DO antes de Sprint S01. Entregable: 12 archivos OPERATIVO."),
    ("INIT-D-02", "D", "Consolidar PROJECT_MEMORY.md", "PM", 1, "LOW", "completed",
     "Consolidar PROJECT_MEMORY.md con: stack, fases, decisiones D-XX, UUIDs del equipo, referencias a SPEC. Memoria persistente que todos los agentes leen al iniciar sesion. Entregable: PROJECT_MEMORY.md en el repo."),
    ("INIT-D-03", "D", "CONTEXTO de sesion por rol", "PJM", 1, "LOW", "in_progress",
     "Crear knowledge/agent-tasks/CONTEXTO_<ROL>_SESION.md para roles principales: PM, TL, PJM, BE, FE, DB, DO, QA. Hecho: PM. Pendientes: 7. Entregable: 8 archivos CONTEXTO."),
    ("INIT-D-04", "D", "Distribuir accesos al equipo", "PJM", 1, "LOW", "pending",
     "Verificar que cada rol activo tiene: acceso al repo Git, UUID VTT, SERVICE_KEY para autenticarse. Documentar en una matriz accesos x rol. Entregable: matriz de accesos verificada."),
    ("INIT-D-05", "D", "Reuniones de onboarding por rol", "PM", 3, "MEDIUM", "pending",
     "Sesion de kick-off por cada rol activo donde se revisa: SPEC v1.9, PROJECT_MEMORY, OPERATIVO del rol, se resuelven preguntas. Entregable: actas de onboarding por rol."),

    # ── E. Tooling Setup (DO + TL, 4h) ───────────────────────────────────────
    ("INIT-E-01", "E", "Base Node + TypeScript backend", "DO", 2, "MEDIUM", "pending",
     "Crear package.json con scripts: dev, build, start, test, lint, format, migrate, seed. tsconfig.json estricto (strict:true, noImplicitAny). .nvmrc con Node 20. nodemon.json para dev mode. Dependencias base: express, typescript, tsx, nodemon, eslint, prettier. Entregable: proyecto Node inicial bootstrapeado."),
    ("INIT-E-02", "E", "Linters + formatters + pre-commit hooks", "DO", 1, "LOW", "pending",
     ".eslintrc.json con reglas TypeScript estrictas. .prettierrc con config del proyecto. Husky + lint-staged para ejecutar lint + prettier + type-check en pre-commit. Entregable: hooks activos que bloquean commits invalidos."),
    ("INIT-E-03", "E", "CI minimo (smoke) en GitHub Actions", "DO", 1, "MEDIUM", "pending",
     "Crear .github/workflows/ci.yml con un job 'build + lint + test' que corre en cada PR. Node 20, cache de npm, fallos bloquean el merge. El CI de deploy va en MEM-105. Entregable: workflow corriendo y verde en un PR de prueba."),

    # ── F. Documentation (PM + TL, 2h) ───────────────────────────────────────
    ("INIT-F-01", "F", "README + CONTRIBUTING del repo", "PM", 1, "LOW", "pending",
     "README.md con: descripcion del proyecto, stack, setup local (pasos para correr), enlaces al SPEC y PROJECT_RULES. CONTRIBUTING.md con flujo de commits, PRs, branches. Entregable: 2 archivos committeados."),
    ("INIT-F-02", "F", "ARCHITECTURE.md operativo", "TL", 1, "MEDIUM", "pending",
     "docs/ARCHITECTURE.md con resumen arquitectonico breve + link a SPEC v1.9 consolidado. NO duplica SPEC, solo da vista de alto nivel para onboarding rapido. Entregable: ARCHITECTURE.md committeado."),

    # ── G. Kickoff (PM + todos, 3h) ──────────────────────────────────────────
    ("INIT-G-01", "G", "Documento formal de Kickoff", "PM", 2, "MEDIUM", "pending",
     "KICKOFF_MEMORY_SERVICE.md con: vision, objetivos R1, alcance in/out, equipo con roles y UUIDs, roadmap (fechas por fase), riesgos, criterios de exito R1. Entregable: documento firmado por PM."),
    ("INIT-G-02", "G", "Kickoff call del equipo (GATE)", "PM", 1, "HIGH", "pending",
     "HITO: sesion de arranque con el equipo completo. Se revisa KICKOFF doc, se asignan compromisos por rol, se definen action items. Acta con firmas. Esta tarea es el GATE que habilita Fase 2 Discovery. Entregable: acta del kickoff firmada."),
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def auth_token():
    req = urllib.request.Request(
        f"{API_URL}/api/auth/service-token",
        data=json.dumps({"userId": PJM_UUID, "serviceKey": SERVICE_KEY}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())["data"]["token"]


def api_call(method, endpoint, token, payload=None):
    url = f"{API_URL}{endpoint}"
    data = json.dumps(payload).encode() if payload else None
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="ignore")
        return None, f"{e.code} - {detail[:300]}"


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    log("=" * 70)
    log("Memory Service R1 - Restructure Phase 1")
    log("=" * 70)
    log(f"API: {API_URL}")
    log(f"Project: {PROJECT_ID}")
    log(f"Phase Project Setup: {PHASE_PROJECT_SETUP_ID}")
    log("")

    token = auth_token()
    log("JWT token obtenido OK\n")

    uuids = {
        "projectId": PROJECT_ID,
        "phaseId":   PHASE_PROJECT_SETUP_ID,
        "deliveries": {},
        "tasks":     {},
        "cancelled_umbrella": [],
    }

    # ── PASO 1: Cancelar tareas umbrella ─────────────────────────────────────
    log("PASO 1 - Cancelar tareas umbrella MEM-001..005")
    for task_code in UMBRELLA_TASKS:
        resp, err = api_call(
            "PATCH",
            f"/api/tasks/{task_code}/status",
            token,
            {"statusId": STATUS["cancelled"], "changedBy": PJM_UUID,
             "reason": "Reemplazada por tareas atomicas INIT-*. Ver HO_INICIACION y PROCESO_SETUP_PROYECTO_VTT.md"}
        )
        if err:
            log(f"  WARN {task_code}: {err}")
        else:
            log(f"  OK   {task_code} -> task_cancelled")
            uuids["cancelled_umbrella"].append(task_code)
    log("")

    # ── PASO 2: Renombrar delivery existente ─────────────────────────────────
    log("PASO 2 - Renombrar delivery 'Project Foundation Ready' -> 'A. VTT Setup'")
    resp, err = api_call(
        "PUT",
        f"/api/deliveries/{DELIVERY_OLD_ID}",
        token,
        {"name": "A. VTT Setup",
         "description": "Verificacion del proyecto, fases, deliveries y tareas en VTT.",
         "order": 1}
    )
    if err:
        log(f"  WARN: {err}")
    else:
        log(f"  OK   Delivery A renombrado")
        uuids["deliveries"]["A"] = DELIVERY_OLD_ID
    log("")

    # ── PASO 3: Crear 6 deliveries nuevos ────────────────────────────────────
    log("PASO 3 - Crear 6 deliveries nuevos (B..G)")
    for order, name, description in NEW_DELIVERIES:
        resp, err = api_call(
            "POST",
            "/api/deliveries",
            token,
            {"phaseId": PHASE_PROJECT_SETUP_ID,
             "name": name,
             "order": order,
             "description": description,
             "createdBy": PJM_UUID}
        )
        if err:
            log(f"  ERROR {name}: {err}")
            sys.exit(1)
        delivery_id = resp.get("data", resp).get("id")
        letter = name[0]  # 'B. Repository...' -> 'B'
        uuids["deliveries"][letter] = delivery_id
        log(f"  OK   {name} -> {delivery_id}")
    log("")

    # ── PASO 4: Crear 26 tareas INIT-A..G ────────────────────────────────────
    log("PASO 4 - Crear 26 tareas atomicas INIT-A..G")
    for (task_code, delivery_letter, title, role, hours, complexity, status, description) in TASKS:
        delivery_id = uuids["deliveries"].get(delivery_letter)
        if not delivery_id:
            log(f"  ERROR {task_code}: delivery {delivery_letter} no existe")
            continue

        assignee_id = USERS.get(role) or USERS["PJM"]
        status_id   = STATUS.get(status, STATUS["pending"])

        payload = {
            "title":         f"{task_code}: {title}",
            "description":   description[:1900],
            "priorityId":    PRIORITY["M"],
            "statusId":      status_id,
            "assignedToId":  assignee_id,
            "assignedBy":    PJM_UUID,
            "category":      "documentation" if role in ("PM", "PJM", "TL") else "deployment",
            "complexity":    complexity,
            "estimatedHours": hours,
            "createdBy":     PJM_UUID,
        }

        # 4.a: crear tarea en fase
        resp, err = api_call(
            "POST",
            f"/api/phases/{PHASE_PROJECT_SETUP_ID}/tasks",
            token,
            payload
        )
        if err:
            log(f"  ERROR {task_code}: {err}")
            continue

        new_task = resp.get("data", resp)
        task_uuid   = new_task.get("id")
        task_number = new_task.get("taskNumber") or task_uuid
        uuids["tasks"][task_code] = {
            "uuid": task_uuid,
            "vttCode": task_number,
            "deliveryId": delivery_id,
            "role": role,
            "hours": hours,
            "status": status,
        }

        # 4.b: vincular al delivery
        resp2, err2 = api_call(
            "POST",
            f"/api/deliveries/{delivery_id}/tasks/{task_uuid}",
            token,
            {"assignedBy": PJM_UUID}
        )
        link_msg = "OK" if not err2 else f"WARN link: {err2}"

        log(f"  OK   {task_code} [{role}, {hours}h, {complexity}] -> {task_number} | delivery {delivery_letter} | link {link_msg}")

    log("")

    # ── Guardar UUIDs capturados ─────────────────────────────────────────────
    output_file = "VTT_UUIDS_PHASE1_RESTRUCTURED.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(uuids, f, indent=2)
    log(f"UUIDs guardados en {output_file}")

    # ── Resumen ──────────────────────────────────────────────────────────────
    log("")
    log("=" * 70)
    log("RESUMEN")
    log("=" * 70)
    log(f"Umbrella cancelled:   {len(uuids['cancelled_umbrella'])} / 5")
    log(f"Deliveries totales:   {len(uuids['deliveries'])} / 7")
    log(f"Tareas INIT creadas:  {len(uuids['tasks'])} / 26")
    log("=" * 70)


if __name__ == "__main__":
    main()
