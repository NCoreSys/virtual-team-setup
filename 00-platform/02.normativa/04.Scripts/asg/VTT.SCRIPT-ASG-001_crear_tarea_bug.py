#!/usr/bin/env python
"""Crea tarea hija de tipo BUG y aplica el proceso completo de 10 pasos.

PRE-REQUISITOS (input del TL a mano):
  1. Archivo ASSIGNMENT_MS-XXX_<desc>.md existente en knowledge/agent-tasks/assignments/
     (escrito a mano por el TL con el detalle especifico del bug)
  2. Lista de CAs definida en:
     - el spec JSON (campo "cas")
     - o un archivo separado (--cas-file)
  3. Tarea padre existente en VTT y en estado revisable

Automatiza los pasos 4a-4i de GUIA_MANEJO_BUGS_TL.md:
  4a. Detecta siguiente consecutivo MS-XXX
  4b. Crea la tarea hija en VTT (POST /api/phases/:id/tasks)
  4c. Asigna agente con PUT /api/tasks/:id usando `assignedToId` (NO `assigneeId`)
  4d. Sube ASSIGNMENT.md como attachment (POST /api/tasks/:id/attachments)
  4e. Crea N CAs (POST /api/tasks/:id/criteria)
  4f. Crea bug entry en padre (POST /api/tasks/:padre/issues)
  4f.2 Liga bug entry a tarea hija (PUT /api/issues/:id con resolvedByTaskId)
  4g. Crea dependencia padre->hija (POST /api/tasks/:padre/dependencies)
  4h. Mueve padre a task_on_hold (PUT /api/tasks/:padre/on-hold)
  4i. Genera mensaje al agente (delegando a gen_mensaje.py)
  Opcional --post: postea mensaje en VTT como comment

Uso:
    # Modo interactivo (recomendado primer uso):
    python scripts/crear_tarea_bug.py --interactive

    # Modo con archivo de especificacion JSON:
    python scripts/crear_tarea_bug.py --spec bugs/MS-322_spec.json --post

    # Modo CLI completo:
    python scripts/crear_tarea_bug.py \\
        --parent MS-322 \\
        --title "[BUG] MS-322 PR cleanup: fix lint + separar scope" \\
        --description "..." \\
        --assignee BE \\
        --estimated-hours 2 \\
        --priority high \\
        --category bugfix \\
        --severity high \\
        --bug-category scope_violation \\
        --sprint S03 \\
        --assignment-md path/to/ASSIGNMENT.md \\
        --cas-file path/to/cas.json \\
        --post

Formato spec JSON (para --spec):
{
  "parent": "MS-322",
  "title": "[BUG] ...",
  "description": "...",
  "assignee": "BE",
  "estimated_hours": 2,
  "priority": "high",
  "category": "bugfix",
  "severity": "high",
  "bug_category": "scope_violation",
  "sprint": "S03",
  "assignment_md_path": "knowledge/.../ASSIGNMENT_MS-XXX.md",
  "cas": [
    {"title": "CA-01: ...", "description": "..."},
    ...
  ]
}

Variables de entorno:
    MEM_VTT_TOKEN     # JWT (si no, se genera via service-token)
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import uuid
from datetime import datetime, timezone

# Forzar UTF-8 en stdout/stderr para Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

BASE_URL = "http://77.42.88.106:3000"
WORKSPACE_ROOT = "c:/Users/Martin/Documents/virtual-teams/memory-service"
TL_UUID = "92225290-6b6b-4c1f-a940-dcb4262507aa"
SERVICE_KEY = "hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"
PHASE_DEVELOPMENT = "c5f9f305-de20-4d09-b939-39a84654362c"
PROJECT_MS = "d0fc276d-e764-4a83-96e9-d65f086ed803"

# Priority UUIDs
PRIORITY_IDS = {
    "high": "1a617554-6319-4c56-826f-8ef49a0ff9cc",
    # medium y low se pueden agregar consultando VTT
}

# Status UUIDs (de PROCESO_ASIGNACION_TAREAS_v3.md tabla Status)
STATUS_PENDING = "335fd9c6-f0d6-4966-a6ea-f518c78bc422"
STATUS_IN_PROGRESS = "2a76888a-e595-4cfc-ac4c-a3ae5087ef56"
STATUS_IN_REVIEW = "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d"
STATUS_COMPLETED = "aa5ceb90-5209-42a2-b874-a8cbee597a97"
STATUS_APPROVED = "b9ca4951-6e14-4d82-b1d8-440793bbaf47"
STATUS_ON_HOLD = "c62eb334-b7bc-4c9f-af85-a5666c262aaa"

# Agentes
AGENTS = {
    "BE": ("ebbe3cee-abed-4b3b-860d-0a81f632b08a", "Backend Engineer"),
    "DB": ("6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7", "Database Engineer"),
    "FE": ("d23c9cd9-a156-433b-8900-94add5488eec", "Frontend Engineer"),
    "QA": ("613c9538-658c-45fe-a6d7-c1ea9ff04b78", "QA Engineer"),
    "DO": ("322e3745-9756-4a7c-af11-44b33edef44d", "DevOps Engineer"),
    "DL": ("b3a09269-cded-468c-a475-15a48f203cb0", "Design Lead"),
    "UX": ("a75a1dae-754a-4b6f-a3ff-db8d51f6a91b", "UX Designer"),
    "AR": ("e9403c25-c1f8-4b64-b2ef-f447d53115e2", "Architect"),
    "SA": ("0c128e3b-db3b-4e31-b107-0379b5791233", "Solution Analyst"),
    "PM": ("350831b2-e1ae-4dbe-b2eb-7e023ec2e103", "Product Manager"),
    "TL": ("92225290-6b6b-4c1f-a940-dcb4262507aa", "Tech Lead"),
}


# ============================================================
# HTTP helpers
# ============================================================

def get_token():
    """Obtiene JWT token via service-key. Usa MEM_VTT_TOKEN si esta seteado."""
    if os.environ.get("MEM_VTT_TOKEN"):
        return os.environ["MEM_VTT_TOKEN"]
    body = json.dumps({"userId": TL_UUID, "serviceKey": SERVICE_KEY}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/api/auth/service-token",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["data"]["token"]


def api_request(method, path, body=None, token=None, raw_body=None, extra_headers=None):
    headers = {"Authorization": f"Bearer {token}"}
    if extra_headers:
        headers.update(extra_headers)
    if body is not None and raw_body is None:
        headers.setdefault("Content-Type", "application/json; charset=utf-8")
        data = json.dumps(body).encode("utf-8")
    else:
        data = raw_body
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        raise RuntimeError(f"HTTP {e.code} on {method} {path}: {err}") from None


# ============================================================
# Paso 2 — Encontrar siguiente MS-XXX y crear tarea
# ============================================================

def find_next_ms_id(token):
    """Devuelve el siguiente consecutivo MS-XXX disponible."""
    max_num = 0
    offset = 0
    while True:
        page = api_request("GET", f"/api/tasks?projectId={PROJECT_MS}&limit=100&offset={offset}", token=token)
        tasks = page.get("data", [])
        if not tasks:
            break
        for t in tasks:
            tid = t.get("id", "")
            if tid.startswith("MS-"):
                try:
                    n = int(tid.split("-")[1])
                    max_num = max(max_num, n)
                except (ValueError, IndexError):
                    pass
        if len(tasks) < 100:
            break
        offset += 100
    return f"MS-{max_num + 1}"


def create_task(spec, token):
    """Crea tarea en VTT. Retorna task_id.

    Payload alineado con PROCESO_ASIGNACION_TAREAS_v3.md Paso 2:
    - statusId pending explicito
    - assignedToId (NO assigneeId - gotcha 1)
    - assignedBy + createdBy obligatorios para trazabilidad
    """
    priority_id = PRIORITY_IDS.get(spec["priority"], PRIORITY_IDS["high"])
    agent_code = spec["assignee"]
    agent_uuid = AGENTS[agent_code][0]
    body = {
        "title": spec["title"],
        "description": spec["description"][:2000],  # max 2000 chars segun doc v3
        "priorityId": priority_id,
        "statusId": STATUS_PENDING,
        "assignedToId": agent_uuid,
        "assignedBy": TL_UUID,
        "createdBy": TL_UUID,
        "complexity": spec.get("complexity", "MEDIUM"),
        "category": spec.get("category", "bugfix"),
        "type": "bug",
        "estimatedHours": spec.get("estimated_hours", 2),
    }
    result = api_request("POST", f"/api/phases/{PHASE_DEVELOPMENT}/tasks", body, token=token)
    task_id = result["data"]["id"]
    return task_id


# ============================================================
# Paso 3c — Asignar agente (workaround del gotcha)
# ============================================================

def assign_agent(task_id, agent_uuid, token):
    # IMPORTANTE: el campo canonico en VTT es `assignedToId`, NO `assigneeId`.
    # `assigneeId` parece aceptarse (200 OK) pero no persiste el assignee.
    body = {"assignedToId": agent_uuid}
    api_request("PUT", f"/api/tasks/{task_id}", body, token=token)


# ============================================================
# Paso 3 — Subir ASSIGNMENT como attachment
# ============================================================

def upload_attachment(task_id, file_path, file_type, uploader_id, token):
    with open(file_path, "rb") as f:
        content = f.read()
    boundary = "----vtt" + uuid.uuid4().hex
    filename = os.path.basename(file_path)

    def field(name, value):
        return (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n"
        ).encode()

    body = b""
    body += field("fileType", file_type)
    body += field("uploadedById", uploader_id)
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode()
    body += b"Content-Type: text/markdown\r\n\r\n"
    body += content
    body += f"\r\n--{boundary}--\r\n".encode()

    result = api_request(
        "POST",
        f"/api/tasks/{task_id}/attachments",
        raw_body=body,
        token=token,
        extra_headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    return result["data"]["id"]


# ============================================================
# Paso 3b — Crear CAs
# ============================================================

def create_cas(task_id, cas, token):
    """cas: list of dicts {title, description}

    Payload alineado con doc v3 Paso 6:
    - criteriaTypeCode (NO type - gotcha 2)
    - required: true para CAs obligatorios
    - Endpoint /criteria (NO /acceptance-criteria - gotcha 2)
    """
    ids = []
    for i, ca in enumerate(cas, 1):
        body = {
            "title": ca["title"],
            "description": ca["description"],
            "criteriaTypeCode": "acceptance",
            "required": True,
            "order": i,
        }
        result = api_request("POST", f"/api/tasks/{task_id}/criteria", body, token=token)
        ids.append(result["data"]["id"])
    return ids


# ============================================================
# Paso 4 — Bug entry + dependencia + on_hold en padre
# ============================================================

def create_bug_entry(parent_id, title, description, severity, category, reporter_id, token):
    body = {
        "title": title,
        "description": description,
        "severity": severity,
        "category": category,
        "reportedById": reporter_id,
    }
    result = api_request("POST", f"/api/tasks/{parent_id}/issues", body, token=token)
    return result["data"]["id"]


def link_issue_to_task(issue_id, resolving_task_id, token):
    """Liga bug entry a la tarea hija via PUT /api/issues/{id}.
    resolvedByTaskId NO persiste en POST — requiere PUT separado (gotcha descubierto MS-375).
    """
    body = {"resolvedByTaskId": resolving_task_id}
    api_request("PUT", f"/api/issues/{issue_id}", body, token=token)


def create_dependency(parent_id, child_id, token):
    body = {
        "taskId": parent_id,
        "dependsOnTaskId": child_id,
        "type": "blocks",
    }
    result = api_request("POST", f"/api/tasks/{parent_id}/dependencies", body, token=token)
    return result["data"]["id"]


def move_to_on_hold(parent_id, bug_title, bug_description, child_task_id, token):
    # on-hold crea el issue internamente — NO llamar create_bug_entry por separado.
    body = {
        "type": "bug",
        "title": bug_title[:200],
        "description": bug_description[:500],
    }
    result = api_request("PUT", f"/api/tasks/{parent_id}/on-hold", body, token=token)
    # Extraer el issue_id creado por on-hold
    return result.get("data", {}).get("issue", {}).get("id") or result.get("data", {}).get("onHoldIssue", {}).get("id")


# ============================================================
# Paso 5 — Generar mensaje al agente
# ============================================================

def post_comment(task_id, message, user_id, token, chunk_size=5000):
    """Postea mensaje en chunks de chunk_size si supera el límite."""
    chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]
    ids = []
    for idx, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            chunk = f"[{idx}/{len(chunks)}]\n{chunk}"
        body = {"userId": user_id, "message": chunk}
        result = api_request("POST", f"/api/tasks/{task_id}/comments", body, token=token)
        ids.append(result["data"]["id"])
    return ids[0] if len(ids) == 1 else ids


def generate_message_via_script(task_id, do_post=False):
    """Llama a scripts/gen_mensaje.py para generar el archivo MENSAJE_MS-XXX.md."""
    import subprocess
    script = os.path.join(os.path.dirname(__file__), "gen_mensaje.py")
    cmd = ["python3", script, task_id]
    if do_post:
        cmd.append("--post")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            print(f"[warn] gen_mensaje.py exit {result.returncode}: {result.stderr[:300]}")
        return result.returncode == 0
    except Exception as e:
        print(f"[warn] gen_mensaje.py error: {e}")
        return False


# ============================================================
# Interactivo
# ============================================================

def interactive_spec():
    print("=== Modo interactivo crear_tarea_bug.py ===\n")
    spec = {}
    spec["parent"] = input("Tarea padre (ej. MS-322): ").strip()
    spec["title"] = input("Titulo (formato: [BUG] MS-XXX <descripcion>): ").strip()
    print("Descripcion (multilinea, terminar con linea '.' sola):")
    desc_lines = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        desc_lines.append(line)
    spec["description"] = "\n".join(desc_lines)
    print(f"\nRoles disponibles: {', '.join(AGENTS.keys())}")
    spec["assignee"] = input("Rol asignado (BE/DB/FE/QA/DO/DL/UX/AR/SA): ").strip().upper()
    spec["estimated_hours"] = int(input("Horas estimadas (default 2): ").strip() or "2")
    spec["priority"] = input("Prioridad (high/medium/low, default high): ").strip() or "high"
    spec["category"] = "bugfix"
    spec["severity"] = input("Severidad (critical/high/medium/low, default high): ").strip() or "high"
    spec["bug_category"] = input("Categoria del bug (lint/scope_violation/logic_error/missing_docs/ci_failure): ").strip() or "scope_violation"
    spec["sprint"] = input("Sprint (ej. S03): ").strip()
    spec["assignment_md_path"] = input("Ruta a ASSIGNMENT.md (relativa al repo): ").strip()

    print("\nCAs — formato: titulo|descripcion. Linea vacia para terminar.")
    cas = []
    while True:
        line = input(f"CA-{len(cas)+1}: ").strip()
        if not line:
            break
        if "|" not in line:
            print("  Falta '|'. Reintentar.")
            continue
        title, desc = line.split("|", 1)
        cas.append({"title": title.strip(), "description": desc.strip()})
    spec["cas"] = cas
    return spec


# ============================================================
# Main pipeline
# ============================================================

def run(spec, do_post=False):
    token = get_token()
    print(f"[info] Token OK")

    # Validaciones
    parent = spec["parent"]
    if not parent.startswith("MS-"):
        raise ValueError(f"parent debe ser MS-XXX, got {parent!r}")
    agent_code = spec["assignee"]
    if agent_code not in AGENTS:
        raise ValueError(f"assignee desconocido {agent_code!r}. Validos: {list(AGENTS.keys())}")
    agent_uuid, agent_name = AGENTS[agent_code]

    if not os.path.isfile(spec["assignment_md_path"]):
        raise FileNotFoundError(f"ASSIGNMENT.md no existe: {spec['assignment_md_path']}")

    if not spec.get("cas") or len(spec["cas"]) == 0:
        raise ValueError("Se requiere al menos 1 CA")

    # Paso 2 — buscar consecutivo + crear tarea
    next_id = find_next_ms_id(token)
    print(f"[paso 2] Siguiente consecutivo: {next_id}")
    task_id = create_task(spec, token)
    print(f"[paso 2] Tarea creada: {task_id}")
    if task_id != next_id:
        print(f"[warn] Esperado {next_id}, VTT asigno {task_id}. Continuando.")

    # Paso 3c — verificar/forzar asignacion (workaround del gotcha)
    # create_task ya manda assignedToId, pero hacemos verificacion explicita
    current = api_request("GET", f"/api/tasks/{task_id}", token=token)["data"]
    if not current.get("assignee") or current["assignee"].get("id") != agent_uuid:
        assign_agent(task_id, agent_uuid, token)
        print(f"[paso 3c] Agente asignado via PUT: {agent_code} ({agent_uuid})")
    else:
        print(f"[paso 3c] Agente ya asignado en POST: {agent_code}")

    # Paso 3 — subir ASSIGNMENT
    attachment_id = upload_attachment(task_id, spec["assignment_md_path"], "assignment", TL_UUID, token)
    print(f"[paso 3] ASSIGNMENT attachment: {attachment_id}")

    # Paso 3b — crear CAs
    ca_ids = create_cas(task_id, spec["cas"], token)
    print(f"[paso 3b] {len(ca_ids)} CAs creados")

    # Paso 4a+4c — on-hold crea el issue bug en un solo paso
    bug_title = f"[BUG] {parent}: {spec['title'].lstrip('[BUG] ').lstrip('[BUG]').strip()[:120]}"
    bug_desc = (
        f"Bugs detectados en review:\n{spec['description'][:400]}\n\n"
        f"Tarea hija: {task_id}. Padre en task_on_hold hasta aprobacion."
    )
    parent_data = api_request("GET", f"/api/tasks/{parent}", token=token)["data"]
    if parent_data.get("status", {}).get("code") == "task_on_hold":
        print(f"[paso 4a] {parent} ya en task_on_hold — creando issue separado")
        bug_id = create_bug_entry(parent, bug_title, bug_desc, spec["severity"], spec["bug_category"], TL_UUID, token)
        print(f"[paso 4a] Bug entry en {parent}: {bug_id}")
        link_issue_to_task(bug_id, task_id, token)
    else:
        bug_id = move_to_on_hold(parent, bug_title, bug_desc, task_id, token)
        print(f"[paso 4a+4c] {parent} movido a on_hold, bug creado: {bug_id}")
        if bug_id:
            link_issue_to_task(bug_id, task_id, token)
            print(f"[paso 4a.2] Bug {str(bug_id)[:8]} ligado a {task_id}")

    # Paso 4b — dependencia
    dep_id = create_dependency(parent, task_id, token)
    print(f"[paso 4b] Dependencia {parent}<-{task_id}: {dep_id}")

    # Paso 5 — mensaje
    print(f"[paso 5] Generando mensaje via gen_mensaje.py {'(--post)' if do_post else ''}...")
    ok = generate_message_via_script(task_id, do_post=do_post)
    if ok:
        print(f"[paso 5] MENSAJE generado")
    else:
        print(f"[paso 5] gen_mensaje.py fallo - generar a mano y postear")

    # Postear nota en la padre informando el on_hold
    parent_note = (
        f"### {parent} movido a task_on_hold\n\n"
        f"Bug {bug_id[:8]} creado y ligado a tarea hija {task_id}.\n\n"
        f"**Razon**: {bug_title}\n\n"
        f"**Tarea hija**: {task_id} - {spec['title']}\n\n"
        f"{parent} sale de on_hold automaticamente cuando {task_id} sea aprobada por TL.\n\n"
        f"- TL Reviewer"
    )
    post_comment(parent, parent_note, TL_UUID, token)
    print(f"[paso 4d] Nota en {parent} posteada")

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"Tarea hija:       {task_id}")
    print(f"Tarea padre:      {parent} (task_on_hold)")
    print(f"Agente:           {agent_code} - {agent_name}")
    print(f"Attachment:       {attachment_id}")
    print(f"Bug entry padre:  {bug_id}")
    print(f"Dependency:       {dep_id}")
    print(f"CAs creados:      {len(ca_ids)}")
    print()
    print(f"VTT: {BASE_URL}/tasks/{task_id}")
    print()
    if not do_post:
        print(f"Siguiente paso: revisar MENSAJE_MS-XXX.md y postear con:")
        print(f"  python3 scripts/gen_mensaje.py {task_id} --post")


def enforce_canonical_path():
    """
    Enforcement runtime de RULE-SCRIPT-001 v1.0:
    El script SOLO puede ejecutarse desde su path canonico en virtual-teams-setup.

    Permitido:  .../virtual-teams-setup/00-platform/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001*.py
    Prohibido:  cualquier copia local (ej. memory-service/.vtt/worktrees/<rol>/scripts/...)

    Excepcion: VTT_SCRIPT_ALLOW_LOCAL=1 permite ejecucion local (solo desarrollo del script).
    """
    script_path = os.path.abspath(__file__)
    if os.environ.get("VTT_SCRIPT_ALLOW_LOCAL") == "1":
        return
    marker = "02.normativa/04.Scripts/asg"
    if marker not in script_path.replace("\\", "/"):
        print(json.dumps({
            "success": False,
            "error": "RULE-SCRIPT-001 violation",
            "message": "Este script SOLO puede ejecutarse desde su path canonico en virtual-teams-setup. "
                       "Detectada ejecucion desde copia local prohibida.",
            "script_path": script_path,
            "expected_canonical": "$VTT_SETUP/02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py",
            "fix": "Invocar el script con su path canonico, NO desde scripts/ del worktree. "
                   "Ver $VTT_SETUP/02.normativa/00.Rules/rules_catalog.json#RULE-SCRIPT-001 "
                   "y $VTT_SETUP/02.normativa/02.Workflows/VTT.WORKFLOW-ASG-001.030_manejo_bugs_en_review.md",
            "bypass": "VTT_SCRIPT_ALLOW_LOCAL=1 (solo desarrolladores del script - NO usar en produccion)"
        }, indent=2))
        sys.exit(2)


def main():
    enforce_canonical_path()
    p = argparse.ArgumentParser(description="Crear tarea hija de tipo BUG con proceso completo")
    p.add_argument("--interactive", action="store_true", help="Modo interactivo")
    p.add_argument("--spec", help="Archivo JSON con la especificacion completa")
    p.add_argument("--parent", help="Tarea padre (MS-XXX)")
    p.add_argument("--title", help="Titulo de la tarea hija")
    p.add_argument("--description", help="Descripcion")
    p.add_argument("--assignee", help="Rol asignado (BE/DB/FE/QA/...)")
    p.add_argument("--estimated-hours", type=int, default=2)
    p.add_argument("--priority", default="high")
    p.add_argument("--category", default="bugfix")
    p.add_argument("--severity", default="high")
    p.add_argument("--bug-category", default="scope_violation")
    p.add_argument("--sprint", help="Sprint (S03, S04, ...)")
    p.add_argument("--assignment-md", help="Path al ASSIGNMENT.md")
    p.add_argument("--cas-file", help="Path a JSON con lista de CAs [{title,description}]")
    p.add_argument("--post", action="store_true", help="Postear mensaje en VTT al final")
    args = p.parse_args()

    if args.interactive:
        spec = interactive_spec()
    elif args.spec:
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        if not all([args.parent, args.title, args.description, args.assignee,
                    args.assignment_md, args.cas_file, args.sprint]):
            p.error("Faltan args. Usa --interactive o --spec o todos los flags requeridos.")
        with open(args.cas_file, "r", encoding="utf-8") as f:
            cas = json.load(f)
        spec = {
            "parent": args.parent,
            "title": args.title,
            "description": args.description,
            "assignee": args.assignee.upper(),
            "estimated_hours": args.estimated_hours,
            "priority": args.priority,
            "category": args.category,
            "severity": args.severity,
            "bug_category": args.bug_category,
            "sprint": args.sprint,
            "assignment_md_path": args.assignment_md,
            "cas": cas,
        }

    try:
        run(spec, do_post=args.post)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
