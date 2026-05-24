#!/usr/bin/env python3
# =============================================================================
# VTT.SCRIPT-MSG-001 - gen_mensaje.py
# Version: 1.0.0 (2026-05-22)
# =============================================================================
#
# Proposito: Generar el mensaje de asignacion de tarea para un agente VTT
#            leyendo formalmente el template canonico v2.1 (RULE-TEMPLATE-001)
#            y resolviendo placeholders {{VAR}} con datos vivos de VTT API.
#
# Path canonico (RULE-SCRIPT-001 v1.0):
#   $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py
#
# Modos de operacion:
#
# 1) --output <path>   Genera el mensaje a un archivo local. NO postea.
#                      Idempotente: SI (sobreescribe el archivo).
#
# 2) --post            Genera, valida internamente, postea como comment en
#                      VTT (chunking automatico si supera 5000 chars) y
#                      guarda copia local.
#                      Idempotente: NO (cada llamada crea comment nuevo).
#
# 3) --validate <path> Verifica que un mensaje generado cumple el template
#                      v2.1. Retorna JSON con {valid, findings:[...]}.
#                      Idempotente: SI.
#
# Inputs comunes:
#   --task-id          MS-XXX | VTT-XXX (req)
#   --template-path    Path al template. Default: $VTT_SETUP/03.templates/
#                      tarea/TEMPLATE_MENSAJE_ASIGNACION.md
#   --project-root     Path raiz del proyecto (req salvo --validate)
#   --vtt-setup        Path a $VTT_SETUP. Default desde env VTT_SETUP
#   --token-env        Env var con JWT (default: TOKEN)
#   --base-url         VTT base URL (default: http://77.42.88.106:3000)
#
# Outputs (stdout JSON):
#   --output:   {"success": true, "output_path": "...", "rendered_size": N}
#   --post:     {"success": true, "comment_ids": ["..."], "output_path": "..."}
#   --validate: {"valid": true|false, "findings": [{"block","severity","msg"}]}
#
# Exit codes:
#   0  OK
#   1  Argumentos invalidos
#   2  Precondicion no cumplida (template/proyecto/task no existe)
#   3  HTTP error de VTT
#   4  Validate fallo (mensaje no cumple template)
#
# Reglas que aplican:
#   - RULE-SCRIPT-001 v1.0: invocar SIEMPRE desde el path canonico
#   - RULE-TEMPLATE-001:    leer el template como archivo, NO hardcodear
#                           el formato del mensaje en el script
# =============================================================================

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime

DEFAULT_BASE_URL = "http://77.42.88.106:3000"
SERVICE_KEY_DEFAULT = "hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"

STATUS_IN_PROGRESS = "2a76888a-e595-4cfc-ac4c-a3ae5087ef56"
STATUS_IN_REVIEW = "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d"

# Mapeo email -> (role_code, role_nombre, agent_uuid)
ROLE_BY_EMAIL = {
    "memory-service.be@vtt.ai":       ("BE", "Backend Engineer",     "ebbe3cee-abed-4b3b-860d-0a81f632b08a"),
    "backend@memory-service.vtt.ai":  ("BE", "Backend Engineer",     "ebbe3cee-abed-4b3b-860d-0a81f632b08a"),
    "memory-service.db@vtt.ai":       ("DB", "Database Engineer",    "6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7"),
    "database@memory-service.vtt.ai": ("DB", "Database Engineer",    "6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7"),
    "memory-service.fe@vtt.ai":       ("FE", "Frontend Engineer",    "d23c9cd9-a156-433b-8900-94add5488eec"),
    "frontend@memory-service.vtt.ai": ("FE", "Frontend Engineer",    "d23c9cd9-a156-433b-8900-94add5488eec"),
    "memory-service.qa@vtt.ai":       ("QA", "QA Engineer",          "613c9538-658c-45fe-a6d7-c1ea9ff04b78"),
    "qa@memory-service.vtt.ai":       ("QA", "QA Engineer",          "613c9538-658c-45fe-a6d7-c1ea9ff04b78"),
    "memory-service.devops@vtt.ai":   ("DO", "DevOps Engineer",      "322e3745-9756-4a7c-af11-44b33edef44d"),
    "devops@memory-service.vtt.ai":   ("DO", "DevOps Engineer",      "322e3745-9756-4a7c-af11-44b33edef44d"),
    "memory-service.ux@vtt.ai":       ("UX", "UX Designer",          "a75a1dae-754a-4b6f-a3ff-db8d51f6a91b"),
    "ux@memory-service.vtt.ai":       ("UX", "UX Designer",          "a75a1dae-754a-4b6f-a3ff-db8d51f6a91b"),
    "memory-service.dl@vtt.ai":       ("DL", "Design Lead",          "b3a09269-cded-468c-a475-15a48f203cb0"),
    "design-lead@memory-service.vtt.ai": ("DL", "Design Lead",       "b3a09269-cded-468c-a475-15a48f203cb0"),
    "memory-service.tl@vtt.ai":       ("TL", "Tech Lead Executor",   "92225290-6b6b-4c1f-a940-dcb4262507aa"),
    "tl@memory-service.vtt.ai":       ("TL", "Tech Lead Executor",   "92225290-6b6b-4c1f-a940-dcb4262507aa"),
    "pm@memory-service.vtt.ai":       ("PM", "Product Manager",      "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"),
    "ar@memory-service.vtt.ai":       ("AR", "Architect",            "e9403c25-c1f8-4b64-b2ef-f447d53115e2"),
}

ROLE_TO_REPO = {
    "BE": "backend", "DO": "backend", "DB": "backend", "QA": "backend",
    "FE": "frontend",
    "TL": "project", "PM": "project", "AR": "project", "UX": "project", "DL": "project",
}

# Phase slug normalizer (igual al script legacy)
PHASE_MAP = {
    "discovery": "00-discovery",
    "planning":  "01-planning",
    "analysis":  "02-analysis",
    "design":    "03-design",
    "design-ux-ui": "03-design",
    "design-technical": "03-design",
    "development": "04-development",
    "testing":   "05-testing",
    "deploy":    "06-deploy",
    "deployment": "06-deploy",
    "operations": "07-operations",
}


# -----------------------------------------------------------------------------
# HTTP helpers
# -----------------------------------------------------------------------------

def vtt_get(path, token, base_url):
    req = urllib.request.Request(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read()).get("data")


def vtt_post_comment(task_id, message, user_id, token, base_url, chunk_size=5000):
    """Postea como comment. Si message > chunk_size, chunkea en N partes."""
    effective = chunk_size - 8  # reservar 8 chars para prefijo "[N/N]\n"
    chunks = [message[i:i + effective] for i in range(0, len(message), effective)]
    ids = []
    for idx, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            chunk = f"[{idx}/{len(chunks)}]\n{chunk}"
        body = json.dumps({"message": chunk, "userId": user_id}).encode()
        req = urllib.request.Request(
            f"{base_url}/api/tasks/{task_id}/comments",
            data=body,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as r:
            ids.append(json.loads(r.read()).get("data", {}).get("id"))
    return ids


def obtain_token(user_uuid, base_url, service_key):
    """Obtiene JWT via service-token endpoint."""
    body = json.dumps({"userId": user_uuid, "serviceKey": service_key}).encode()
    req = urllib.request.Request(
        f"{base_url}/api/auth/service-token",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["data"]["token"]


# -----------------------------------------------------------------------------
# Template loader (RULE-TEMPLATE-001)
# -----------------------------------------------------------------------------

def load_template(template_path):
    """Carga el template canonico y extrae el bloque markdown.

    El template tiene esta estructura:
      # TEMPLATE: ...
      ...intro...
      ```markdown
      <CUERPO DEL MENSAJE CON {{VARS}}>
      ```
      ...placeholders ref...

    Devuelve solo el cuerpo entre los fences ```markdown ... ```.
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template no existe: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # El template tiene bloques bash ANIDADOS dentro del bloque markdown outer.
    # Por eso usamos greedy `.*` (no `.*?`) para capturar hasta el ULTIMO ```
    # del archivo (que es el cierre del bloque markdown outer).
    # Si usaramos non-greedy matchearia el primer ``` de un bloque bash interno
    # y truncaria el template (bug original — generaba mensajes de 26 lineas
    # en lugar de 184).
    m = re.search(r"```markdown\s*\n(.*)\n```", raw, re.DOTALL)
    if not m:
        raise ValueError(
            f"Template {template_path} no tiene bloque ```markdown ... ``` "
            "(estructura v2.x requerida)"
        )
    return m.group(1)


def resolve_placeholders(template, mapping):
    """Reemplaza {{VAR}} por su valor. Deja {{VAR}} si no hay valor."""
    result = template
    for k, v in mapping.items():
        result = result.replace("{{" + k + "}}", str(v) if v is not None else "")
    return result


def strip_variant(template, keep="A"):
    """Elimina la variante NO elegida de la seccion Working Directory.

    El template tiene:
      <!-- VARIANTE A - ... -->
      <!-- Borrar esta variante si el proyecto NO usa worktrees -->
      ...contenido A...
      <!-- VARIANTE B - ... -->
      <!-- Borrar esta variante si el proyecto SI usa worktrees -->
      ...contenido B...
      <!-- FIN - fin de las 2 variantes -->

    keep="A" deja solo A, keep="B" deja solo B. Si no encuentra los markers
    devuelve el template original sin tocar.
    """
    marker_a = re.search(r"<!--\s*VARIANTE A.*?-->", template)
    marker_b = re.search(r"<!--\s*VARIANTE B.*?-->", template)
    marker_end = re.search(r"<!--\s*FIN.*?-->", template)

    if not (marker_a and marker_b and marker_end):
        return template

    a_start = marker_a.start()
    b_start = marker_b.start()
    end_pos = marker_end.end()

    block_a = template[a_start:b_start]
    block_b = template[b_start:end_pos]

    # Limpiar los comentarios markers del bloque elegido
    def clean(block):
        block = re.sub(r"<!--\s*VARIANTE [AB].*?-->\n?", "", block)
        block = re.sub(r"<!--\s*Borrar.*?-->\n?", "", block)
        block = re.sub(r"<!--\s*FIN.*?-->\n?", "", block)
        return block.strip("\n")

    chosen = clean(block_a if keep == "A" else block_b)
    return template[:a_start] + chosen + template[end_pos:]


# -----------------------------------------------------------------------------
# Build context (fetch desde VTT + filesystem)
# -----------------------------------------------------------------------------

def slugify(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "task"


def detect_phase_folder(phase_name):
    slug = (phase_name or "").lower().replace(" ", "-").replace("/", "-")
    slug = slug.replace("?", "").replace(":", "-")
    return PHASE_MAP.get(slug, slug or "unknown")


def detect_sprint_code(sprint_name):
    m = re.search(r"S(?:print\s*)?(\d+)", sprint_name or "")
    return f"S{int(m.group(1)):02d}" if m else "S01"


def port_for_task(task_id):
    fixed = {
        "MS-283": 3001, "MS-284": 3002, "MS-285": 3003,
        "MS-286": 3004, "MS-287": 3005, "MS-288": 3006,
        "MS-293": 3013,
    }
    if task_id in fixed:
        return fixed[task_id]
    try:
        suffix = int(task_id.split("-")[1])
        return 3000 + (suffix % 1000)
    except Exception:
        return 3000


def build_cas_section(criteria):
    if not criteria:
        return "(No hay CAs registrados para esta tarea)"
    lines = []
    for c in criteria:
        cid = c.get("id", "")
        title = c.get("title", "")
        lines.append(f"- {cid}: {title}")
    return "\n".join(lines)


def build_context(task_id, project_root, vtt_setup_path, token, base_url):
    """Fetch desde VTT y deriva todos los valores que necesita el template."""
    task = vtt_get(f"/api/tasks/{task_id}", token, base_url)
    if not task:
        raise RuntimeError(f"Task {task_id} no encontrada en VTT")

    criteria = vtt_get(f"/api/tasks/{task_id}/criteria", token, base_url) or []

    # Resolver agente
    assignee = task.get("assignedTo") or task.get("assignee") or {}
    email = assignee.get("email", "")
    if email not in ROLE_BY_EMAIL:
        raise RuntimeError(
            f"Agente '{email}' no esta en el mapa ROLE_BY_EMAIL. "
            f"Validos: {list(ROLE_BY_EMAIL.keys())}"
        )
    role_code, role_nombre, agent_uuid = ROLE_BY_EMAIL[email]
    repo = ROLE_TO_REPO.get(role_code, "project")

    # Phase / Sprint
    phase_obj = task.get("phase") or {}
    phase_folder = detect_phase_folder(phase_obj.get("name") or "")
    sprint_obj = task.get("sprint") or {}
    sprint_code = detect_sprint_code(sprint_obj.get("name") or "")

    # Detectar variante A vs B basado en worktree
    worktree_path = f"{project_root}/.vtt/worktrees/{repo}-{role_code.lower()}"
    variant = "A" if os.path.isdir(worktree_path) else "B"
    cwd_agente = worktree_path if variant == "A" else project_root

    # Proyecto display
    pn = (task.get("project") or {}).get("name") or "Memory Service"
    proyecto_corto = pn
    proyecto_upper = pn.replace(" ", "-").upper()

    return {
        "_task": task,
        "_criteria": criteria,
        "_variant": variant,
        "ROL_NOMBRE": role_nombre,
        "ROL": role_code,
        "ROL_LOWER": role_code.lower(),
        "TASK_ID": task_id,
        "TITULO": task.get("title", ""),
        "SPRINT": sprint_code,
        "PHASE": phase_folder,
        "SLUG": slugify(task.get("title", "")),
        "PROJECT_ROOT": project_root,
        "REPO": repo,
        "CWD_DEL_AGENTE": cwd_agente,
        "VTT_SETUP_PATH": vtt_setup_path,
        "AGENT_UUID": agent_uuid,
        "SERVICE_KEY": SERVICE_KEY_DEFAULT,
        "PORT": port_for_task(task_id),
        "PROYECTO": proyecto_upper,
        "PROYECTO_CORTO": proyecto_corto,
        "ESTIM_HORAS": task.get("estimatedHours") or "?",
        "LISTA_CAs": build_cas_section(criteria),
    }


def render_message(template_path, ctx):
    template = load_template(template_path)
    template = strip_variant(template, keep=ctx["_variant"])
    return resolve_placeholders(template, ctx)


# -----------------------------------------------------------------------------
# Output writers
# -----------------------------------------------------------------------------

def default_output_path(project_root, phase, sprint, task_id, role_code):
    """Path canonico: $PROJECT_ROOT/.vtt/worktrees/project-tl/knowledge/
    agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md"""
    base = f"{project_root}/.vtt/worktrees/project-tl/knowledge/agent-tasks/messages"
    return f"{base}/{phase}/{sprint}/MENSAJE_{task_id}.md"


def write_local(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# -----------------------------------------------------------------------------
# VALIDATE mode (Bloques A / B / C)
# -----------------------------------------------------------------------------

def validate_message(message_path, token=None, base_url=DEFAULT_BASE_URL):
    """Verifica que un mensaje generado cumple el template v2.1.

    Bloque A - Secciones obligatorias
    Bloque B - Coherencia cruzada con VTT (requiere token)
    Bloque C - Higiene (encoding, markdown, placeholders sin resolver)
    """
    if not os.path.exists(message_path):
        return {"valid": False, "findings": [
            {"block": "A", "severity": "error", "msg": f"Mensaje no existe: {message_path}"}
        ]}

    with open(message_path, "r", encoding="utf-8") as f:
        text = f.read()

    findings = []

    # ---- BLOQUE A -- Secciones obligatorias --------------------------------

    # A1 - Working Directory con UNA variante
    has_wd_header = "WORKING DIRECTORY" in text
    if not has_wd_header:
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta seccion 'WORKING DIRECTORY'"})

    has_marker_a = re.search(r"<!--\s*VARIANTE A", text) is not None
    has_marker_b = re.search(r"<!--\s*VARIANTE B", text) is not None
    if has_marker_a or has_marker_b:
        findings.append({"block": "A", "severity": "error",
                         "msg": "Mensaje aun tiene markers <!-- VARIANTE A/B --> "
                                "(el script debe haber elegido UNA variante y borrado la otra)"})

    # A2 - Branch feature/<TASK_ID>
    task_id_m = re.search(r"asignada:\s*\*\*([A-Z]+-\d+)\*\*", text)
    task_id = task_id_m.group(1) if task_id_m else None
    if task_id:
        if not re.search(rf"feature/{re.escape(task_id)}\b", text):
            findings.append({"block": "A", "severity": "error",
                             "msg": f"Falta patron 'feature/{task_id}' (branch)"})
    else:
        findings.append({"block": "A", "severity": "error",
                         "msg": "No se pudo extraer TASK_ID del mensaje"})

    # A3 - Execution manifest
    if not re.search(r"\.vtt/manifests/[A-Z]+-\d+\.execution\.json", text):
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta 'Execution manifest:' con path .vtt/manifests/<TASK_ID>.execution.json"})

    # A4 - Workspace VSCode
    if not re.search(r"\.code-workspace", text):
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta 'Workspace VSCode:' con path .code-workspace"})

    # A5 - Reglas aplicables (NORMATIVA DE REFERENCIA)
    if "NORMATIVA DE REFERENCIA" not in text:
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta seccion 'NORMATIVA DE REFERENCIA' (Reglas aplicables)"})

    # A6 - Comando VTT.SCRIPT-MAN-001 con flags pre-rellenados
    has_man = re.search(r"VTT\.SCRIPT-MAN-001_gen_task_manifest\.py", text)
    has_flags = re.search(r"--task-id\s+[A-Z]+-\d+", text) and \
                re.search(r"--version\s+1\.0", text) and \
                re.search(r"--agent-uuid\s+[0-9a-f-]{36}", text)
    if not has_man:
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta invocacion de VTT.SCRIPT-MAN-001_gen_task_manifest.py"})
    elif not has_flags:
        findings.append({"block": "A", "severity": "error",
                         "msg": "VTT.SCRIPT-MAN-001 invocado sin todos los flags pre-rellenados "
                                "(requiere --task-id, --version, --agent-uuid resueltos)"})

    # A7 - Entregables con commit del manifest al PR
    if "ENTREGABLES AL CERRAR" not in text:
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta seccion 'ENTREGABLES AL CERRAR'"})
    elif not re.search(r"git add knowledge/task-manifests/.*\.json", text):
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta paso 'git add knowledge/task-manifests/.../<TASK_ID>.json' (commit manifest al PR)"})

    # A8 - $VTT_SETUP=...
    if not re.search(r"\$VTT_SETUP=", text):
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta definicion de '$VTT_SETUP=...'"})

    # A9 - QUE PASA DESPUES
    if "QUE PASA DESPUES" not in text:
        findings.append({"block": "A", "severity": "error",
                         "msg": "Falta seccion 'QUE PASA DESPUES'"})

    # A10 - Referencia a VTT.SKILL-REPORT-001 (I1)
    if "VTT.SKILL-REPORT-001" not in text:
        findings.append({"block": "A", "severity": "warning",
                         "msg": "Falta referencia a VTT.SKILL-REPORT-001 (instruccion I1 del template v2.1)"})

    # ---- BLOQUE B -- Coherencia cruzada con VTT ----------------------------

    if task_id and token:
        try:
            task = vtt_get(f"/api/tasks/{task_id}", token, base_url)
            criteria = vtt_get(f"/api/tasks/{task_id}/criteria", token, base_url) or []

            # B1 - agent_uuid del mensaje == assignee.id de la task
            agent_uuid_m = re.search(r"\*\*Tu user ID:\*\*\s*`([0-9a-f-]{36})`", text)
            if agent_uuid_m:
                msg_uuid = agent_uuid_m.group(1)
                actual_id = ((task.get("assignedTo") or task.get("assignee") or {}).get("id"))
                if actual_id and msg_uuid != actual_id:
                    findings.append({"block": "B", "severity": "error",
                                     "msg": f"agent_uuid del mensaje ({msg_uuid[:8]}) != assignee.id de VTT ({actual_id[:8]})"})
            else:
                findings.append({"block": "B", "severity": "warning",
                                 "msg": "No se pudo extraer 'Tu user ID' del mensaje"})

            # B2 - taskId del path del execution_manifest == TASK_ID del mensaje
            exm_m = re.search(r"\.vtt/manifests/([A-Z]+-\d+)\.execution\.json", text)
            if exm_m and exm_m.group(1) != task_id:
                findings.append({"block": "B", "severity": "error",
                                 "msg": f"taskId en path execution_manifest ({exm_m.group(1)}) != TASK_ID del mensaje ({task_id})"})

            # B3 - worktree_path apunta a directorio existente
            wt_m = re.search(r"`([^`]+/\.vtt/worktrees/[^`]+/?)`", text)
            if wt_m:
                wt_path = wt_m.group(1).rstrip("/")
                if not os.path.isdir(wt_path):
                    findings.append({"block": "B", "severity": "warning",
                                     "msg": f"worktreePath no existe en disco: {wt_path}"})

            # B4 - CAs listadas == criteria de VTT (count + UUIDs)
            cas_in_msg = set(re.findall(r"\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b:", text))
            cas_vtt = {c.get("id") for c in criteria if c.get("id")}
            missing = cas_vtt - cas_in_msg
            extra = cas_in_msg - cas_vtt
            if missing:
                findings.append({"block": "B", "severity": "error",
                                 "msg": f"CAs faltantes en mensaje: {len(missing)} (de {len(cas_vtt)} en VTT)"})
            if extra:
                # extra puede incluir UUIDs de status/agent — solo warning
                findings.append({"block": "B", "severity": "warning",
                                 "msg": f"UUIDs en mensaje que no son CAs de VTT: {len(extra)} (posibles status/agent IDs)"})

            # B5 - Ubicacion del reporte segun politica v2.1 (I2)
            # Path correcto: knowledge/task-manifests/<phase>/<sprint>/<TASK>_REPORT.md
            # Path deprecado: knowledge/agent-tasks/reports/...
            #
            # IMPORTANTE: el path legacy aparece en texto DESCRIPTIVO del template
            # (la propia advertencia "NO usar knowledge/agent-tasks/reports/...").
            # Para evitar falso positivo, solo marcamos cuando aparece como path
            # ACTIVO: dentro de `git add`, `--report-path`, o bloque bash.
            patterns_uso_activo = [
                r"git add\s+knowledge/agent-tasks/reports/",
                r"--report-path\s+knowledge/agent-tasks/reports/",
                r"^\s*knowledge/agent-tasks/reports/.*_REPORT\.md\s*$",   # path solo en una linea
            ]
            uso_activo_detectado = any(
                re.search(p, text, re.MULTILINE) for p in patterns_uso_activo
            )
            if uso_activo_detectado:
                findings.append({"block": "B", "severity": "warning",
                                 "msg": "Reporte ubicado en path legacy 'knowledge/agent-tasks/reports/' "
                                        "(deprecado en v2.1 - usar 'knowledge/task-manifests/<phase>/<sprint>/')"})

        except urllib.error.HTTPError as e:
            findings.append({"block": "B", "severity": "warning",
                             "msg": f"No se pudo consultar VTT para Bloque B: HTTP {e.code}"})
        except Exception as e:
            findings.append({"block": "B", "severity": "warning",
                             "msg": f"Bloque B skipped: {type(e).__name__}: {e}"})

    elif task_id and not token:
        findings.append({"block": "B", "severity": "info",
                         "msg": "Bloque B skipped (no se proveyo --token-env con valor para consultar VTT)"})

    # ---- BLOQUE C -- Higiene -----------------------------------------------

    # C1 - 0 placeholders sin resolver
    unresolved = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if unresolved:
        unique = sorted(set(unresolved))
        # Devuelve linea aproximada del primer match
        first = unresolved[0]
        line_no = text[:text.index(first)].count("\n") + 1
        findings.append({"block": "C", "severity": "error",
                         "msg": f"{len(unresolved)} placeholder(s) sin resolver: {unique[:5]}{'...' if len(unique) > 5 else ''} (primero en linea {line_no})"})

    # C2 - Endpoint devlog correcto
    # Bueno: POST /devlog (singular) o POST /devlog-entries con wrapper {entries:[
    has_bad_devlog = False
    # Buscar POST a /devlog-entries SIN wrapper proximo
    for m in re.finditer(r'POST.*?/devlog-entries[^\n]*', text):
        # Mirar ~200 chars siguientes para ver si hay '"entries"'
        chunk = text[m.start():m.start() + 600]
        if '"entries"' not in chunk and "'entries'" not in chunk:
            has_bad_devlog = True
            break
    if has_bad_devlog:
        findings.append({"block": "C", "severity": "error",
                         "msg": "POST a /devlog-entries SIN wrapper '{entries:[...]}' "
                                "- causa HTTP 400 (caso MS-333). Usar /devlog singular para 1 entry."})

    # C3 - Endpoint fulfill CAs - PATCH /criteria/:cid (NO POST /fulfill)
    if re.search(r"POST.*?/criteria/.*?/fulfill", text):
        findings.append({"block": "C", "severity": "error",
                         "msg": "Endpoint incorrecto 'POST /criteria/.../fulfill' "
                                "- usar 'PATCH /api/tasks/<id>/criteria/<cid>' con {status:'met', evidence:'...'}"})

    # C4 - Encoding UTF-8 sin caracteres rotos
    # Detectar mojibake comun (Â, Ã±, etc.)
    if re.search(r"[ÂÃ][\x80-\xBF]", text):
        findings.append({"block": "C", "severity": "warning",
                         "msg": "Posible mojibake (encoding roto) detectado"})

    # C5 - Markdown bien formado: bloques ``` cerrados
    fences = text.count("```")
    if fences % 2 != 0:
        findings.append({"block": "C", "severity": "error",
                         "msg": f"Bloques ``` impares ({fences}) - hay un fence sin cerrar"})

    # Veredicto
    has_errors = any(f["severity"] == "error" for f in findings)
    return {"valid": not has_errors, "findings": findings}


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def enforce_canonical_path():
    """
    Enforcement runtime de RULE-SCRIPT-001 v1.0:
    El script SOLO puede ejecutarse desde su path canonico en virtual-teams-setup.

    Permitido:  .../virtual-teams-setup/00-platform/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001*.py
    Prohibido:  cualquier copia local (ej. memory-service/.vtt/worktrees/<rol>/scripts/...)

    Excepcion: VTT_SCRIPT_ALLOW_LOCAL=1 permite ejecucion local (solo desarrollo del script).
    """
    script_path = os.path.abspath(__file__)
    if os.environ.get("VTT_SCRIPT_ALLOW_LOCAL") == "1":
        return
    marker = "02.normativa/04.Scripts/msg"
    if marker not in script_path.replace("\\", "/"):
        print(json.dumps({
            "success": False,
            "error": "RULE-SCRIPT-001 violation",
            "message": "Este script SOLO puede ejecutarse desde su path canonico en virtual-teams-setup. "
                       "Detectada ejecucion desde copia local prohibida.",
            "script_path": script_path,
            "expected_canonical": "$VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py",
            "fix": "Invocar el script con su path canonico, NO desde scripts/ del worktree. "
                   "Ver $VTT_SETUP/02.normativa/00.Rules/rules_catalog.json#RULE-SCRIPT-001 "
                   "y $VTT_SETUP/04.docs-soporte/guias-operativas/CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md",
            "bypass": "VTT_SCRIPT_ALLOW_LOCAL=1 (solo desarrolladores del script — NO usar en produccion)"
        }, indent=2))
        sys.exit(2)


def main():
    enforce_canonical_path()
    p = argparse.ArgumentParser(
        description="VTT.SCRIPT-MSG-001 - Generador de mensaje de asignacion (lee template v2.1)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("task_id", nargs="?", help="ID de la tarea (ej. MS-289). No requerido en modo --validate.")
    p.add_argument("--post", action="store_true", help="Postear como comment en VTT y guardar copia local")
    p.add_argument("--output", help="Path destino del mensaje (modo --output, NO postea)")
    p.add_argument("--validate", help="Path al mensaje a validar (modo --validate)")

    p.add_argument("--template-path",
                   default=None,
                   help="Path al template canonico. Default: $VTT_SETUP/03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md")
    p.add_argument("--project-root",
                   default=None,
                   help="Path raiz del proyecto (requerido salvo en --validate)")
    p.add_argument("--vtt-setup",
                   default=os.environ.get("VTT_SETUP"),
                   help="Path a $VTT_SETUP. Default desde env VTT_SETUP")
    p.add_argument("--token-env", default="TOKEN", help="Env var con JWT (default: TOKEN)")
    p.add_argument("--base-url", default=os.environ.get("VTT_BASE_URL", DEFAULT_BASE_URL))
    p.add_argument("--tl-uuid", default=os.environ.get("TL_UUID", "92225290-6b6b-4c1f-a940-dcb4262507aa"),
                   help="UUID que postea el comment (default TL Memory Service)")

    args = p.parse_args()

    # ---- Mode: --validate -------------------------------------------------
    if args.validate:
        token = os.environ.get(args.token_env)
        result = validate_message(args.validate, token=token, base_url=args.base_url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["valid"] else 4)

    # Para --output y --post requerimos task_id y project_root
    if not args.task_id:
        print(json.dumps({"success": False, "error": "task_id requerido (salvo en --validate)"}))
        sys.exit(1)

    if not args.project_root:
        print(json.dumps({"success": False, "error": "--project-root requerido para generar mensaje"}))
        sys.exit(1)

    if not args.vtt_setup:
        print(json.dumps({"success": False, "error": "--vtt-setup o env VTT_SETUP requerido"}))
        sys.exit(1)

    # Resolver template path
    template_path = args.template_path or os.path.join(
        args.vtt_setup, "03.templates", "tarea", "TEMPLATE_MENSAJE_ASIGNACION.md"
    )
    if not os.path.exists(template_path):
        print(json.dumps({"success": False, "error": f"Template no existe: {template_path}"}))
        sys.exit(2)

    # Token
    token = os.environ.get(args.token_env)
    if not token:
        try:
            token = obtain_token(args.tl_uuid, args.base_url, SERVICE_KEY_DEFAULT)
            print(f"[info] Token obtenido via service-token (TL {args.tl_uuid[:8]})", file=sys.stderr)
        except Exception as e:
            print(json.dumps({"success": False, "error": f"No se pudo obtener token: {e}"}))
            sys.exit(2)

    # Build context + render
    try:
        ctx = build_context(args.task_id, args.project_root, args.vtt_setup, token, args.base_url)
        message = render_message(template_path, ctx)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:300]
        print(json.dumps({"success": False, "http_status": e.code, "error": body}))
        sys.exit(3)
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"success": False, "error": f"{type(e).__name__}: {e}"}))
        sys.exit(2)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"{type(e).__name__}: {e}"}))
        sys.exit(3)

    # ---- Mode: --output ---------------------------------------------------
    if args.output:
        out_path = args.output
        write_local(out_path, message)
        print(json.dumps({
            "success": True,
            "mode": "output",
            "output_path": out_path,
            "rendered_size": len(message),
            "variant": ctx["_variant"],
        }, indent=2, ensure_ascii=False))
        sys.exit(0)

    # ---- Mode: --post -----------------------------------------------------
    if args.post:
        out_path = default_output_path(args.project_root, ctx["PHASE"], ctx["SPRINT"],
                                       args.task_id, ctx["ROL"])
        write_local(out_path, message)

        # Validar antes de postear
        v = validate_message(out_path, token=token, base_url=args.base_url)
        if not v["valid"]:
            print(json.dumps({
                "success": False,
                "mode": "post",
                "error": "Validacion fallo - NO se posteo",
                "output_path": out_path,
                "validation": v,
            }, indent=2, ensure_ascii=False))
            sys.exit(4)

        try:
            ids = vtt_post_comment(args.task_id, message, args.tl_uuid, token, args.base_url)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:300]
            print(json.dumps({"success": False, "http_status": e.code, "error": body,
                              "output_path": out_path}))
            sys.exit(3)

        print(json.dumps({
            "success": True,
            "mode": "post",
            "output_path": out_path,
            "comment_ids": ids,
            "chunks": len(ids),
            "rendered_size": len(message),
            "variant": ctx["_variant"],
            "validation_warnings": [f for f in v["findings"] if f["severity"] != "error"],
        }, indent=2, ensure_ascii=False))
        sys.exit(0)

    # Sin --output / --post / --validate: error
    print(json.dumps({"success": False, "error": "Especificar uno de: --output <path>, --post, --validate <path>"}))
    sys.exit(1)


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    main()
