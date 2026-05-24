#!/usr/bin/env python3
# =============================================================================
# VTT.SCRIPT-EXM-001 — gen_execution_manifest.py
# =============================================================================
#
# Proposito: Generar/leer Execution Manifest (instructivo local del TL al
#            agente). NO se sube a VTT — vive en .vtt/manifests/ del proyecto.
#
# Idempotente: Si (sobrescribe el archivo cada vez).
#
# Modo generacion (TL):
#   --task-id            MS-XXX (req)
#   --agent-uuid         UUID del agente (req)
#   --agent-role         BE|DB|FE|DO|QA|DL|UX|AR|SA (req)
#   --assignment-path    path al ASSIGNMENT local (req)
#   --worktree-path      ruta al worktree del rol (req)
#   --branch-expected    default feature/<TASK_ID> (opcional)
#   --template-path      .vtt/manifests/_template.execution.json (req)
#   --output             .vtt/manifests/<TASK_ID>.execution.json (req)
#   --token-env          env var con JWT (default: TOKEN)
#   --base-url           VTT base URL
#
# Modo lectura (agente):
#   --validate-and-read
#   --manifest-path      ruta al manifest (req)
#   --expected-uuid      UUID del agente que verifica que es el dueno (req)
#
# Outputs (stdout JSON):
#   Generacion:  {"success": true, "manifest_path": "...", "allowed_paths_count": N}
#   Lectura:     {"success": true, "worktreePath": "...", "branchExpected": "...",
#                 "allowedPaths": [...], "expectedOutputs": [...]}
#
# Exit codes:
#   0  OK
#   1  Argumentos invalidos
#   2  Precondicion no cumplida (template/assignment/worktree no existe, UUID mismatch)
#   3  Validacion fallo
#   4  HTTP/IO error
# =============================================================================

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

DEFAULT_BASE_URL = "http://77.42.88.106:3000"
VALID_ROLES = {"BE", "DB", "FE", "DO", "QA", "DL", "UX", "AR", "SA"}


def vtt_get(path, token, base_url):
    req = urllib.request.Request(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as r:
        body = r.read().decode("utf-8")
        return json.loads(body).get("data") if body else None


def parse_allowed_paths(assignment_path):
    """Extract paths from ## Scope or ## Archivos autorizados section."""
    if not os.path.exists(assignment_path):
        raise FileNotFoundError(f"Assignment no existe: {assignment_path}")

    with open(assignment_path, "r", encoding="utf-8") as f:
        content = f.read()

    patterns = [
        r"#{1,3}\s+Scope\s*\n(.*?)(?=\n#{1,3}\s+|\Z)",
        r"#{1,3}\s+Archivos\s+autorizados\s*\n(.*?)(?=\n#{1,3}\s+|\Z)",
        r"#{1,3}\s+Allowed\s*Paths?\s*\n(.*?)(?=\n#{1,3}\s+|\Z)",
        r"#{1,3}\s+Alcance\s*\n(.*?)(?=\n#{1,3}\s+|\Z)",
    ]

    section = None
    for pat in patterns:
        m = re.search(pat, content, re.DOTALL | re.IGNORECASE)
        if m:
            section = m.group(1)
            break

    if not section:
        return []

    paths = []
    for line in section.split("\n"):
        line = line.strip()
        if not line.startswith(("-", "*", "+")):
            continue
        line = line[1:].strip().strip("`")
        # primer token antes de espacios/dash
        first_token = re.split(r"[\s—-]", line, maxsplit=1)[0].strip("`")
        if first_token and ("/" in first_token or "." in first_token):
            paths.append(first_token)

    return paths


def parse_expected_outputs(assignment_path):
    """Extract expected outputs from ## Entregables section."""
    with open(assignment_path, "r", encoding="utf-8") as f:
        content = f.read()

    patterns = [
        r"#{1,3}\s+Entregables\s*\n(.*?)(?=\n#{1,3}\s+|\Z)",
        r"#{1,3}\s+Deliverables?\s*\n(.*?)(?=\n#{1,3}\s+|\Z)",
        r"#{1,3}\s+Outputs?\s*\n(.*?)(?=\n#{1,3}\s+|\Z)",
    ]

    section = None
    for pat in patterns:
        m = re.search(pat, content, re.DOTALL | re.IGNORECASE)
        if m:
            section = m.group(1)
            break

    if not section:
        return []

    outputs = []
    for line in section.split("\n"):
        line = line.strip()
        if not line.startswith(("-", "*", "+")):
            continue
        desc = line[1:].strip()

        # Heurística para tipo
        type_guess = "code"
        lower = desc.lower()
        if "test" in lower:
            type_guess = "test"
        elif "migration" in lower or "schema" in lower:
            type_guess = "migration"
        elif "doc" in lower or ".md" in lower:
            type_guess = "documentation"
        elif "devlog" in lower:
            type_guess = "devlog_entry"
        elif "logic.md" in lower or "code logic" in lower:
            type_guess = "code_logic"
        elif "pr" in lower.split() or "pull request" in lower:
            type_guess = "pr"

        outputs.append({"type": type_guess, "description": desc[:200]})

    return outputs


def build_manifest(args, token):
    """Build execution manifest desde ASSIGNMENT + VTT data."""
    # 1. Verify template
    if not os.path.exists(args.template_path):
        raise FileNotFoundError(f"Template no existe: {args.template_path}")

    with open(args.template_path, "r", encoding="utf-8") as f:
        template = json.load(f)

    # 2. Verify worktree
    if not os.path.exists(args.worktree_path):
        raise FileNotFoundError(f"Worktree no existe: {args.worktree_path}")

    # 3. Verify assignment
    if not os.path.exists(args.assignment_path):
        raise FileNotFoundError(f"Assignment no existe: {args.assignment_path}")

    # 4. Fetch task from VTT
    task = vtt_get(f"/api/tasks/{args.task_id}", token, args.base_url)
    if not task:
        raise RuntimeError(f"Task {args.task_id} no encontrada en VTT")

    # 5. Find attachment IDs
    attachments = vtt_get(f"/api/tasks/{args.task_id}/attachments", token, args.base_url) or []
    brief_id = None
    assignment_id = None
    for a in attachments:
        if a.get("fileType") == "brief":
            brief_id = a.get("id")
        elif a.get("fileType") == "assignment":
            assignment_id = a.get("id")

    # 6. Parse allowed_paths and expected_outputs from assignment
    allowed_paths = parse_allowed_paths(args.assignment_path)
    expected_outputs = parse_expected_outputs(args.assignment_path)

    # 7. Compose
    now_iso = datetime.now(timezone.utc).isoformat()
    branch = args.branch_expected or f"feature/{args.task_id}"

    manifest = {
        "schema_version": "1.0",
        "manifest_type": "execution",
        "generated_at": now_iso,
        "generated_by": os.environ.get("AGENT_UUID", "unknown"),

        "task": {
            "id": args.task_id,
            "title": task.get("title"),
            "sprint": {
                "id": (task.get("sprint") or {}).get("id"),
                "name": (task.get("sprint") or {}).get("name")
            },
            "vtt_task_uuid": task.get("id"),
            "estimated_hours": task.get("estimatedHours"),
            "complexity": task.get("complexity"),
            "category": task.get("category")
        },

        "agent": {
            "uuid": args.agent_uuid,
            "role": args.agent_role,
            "email": (task.get("assignee") or {}).get("email")
        },

        "worktreePath": args.worktree_path,
        "branchExpected": branch,

        "allowedPaths": allowed_paths,
        "expectedOutputs": expected_outputs,

        "deadlines": {
            "due_at": task.get("dueAt"),
            "soft_deadline_at": None
        },

        "references": {
            "assignment_path": args.assignment_path,
            "brief_path": None,
            "vtt_assignment_attachment_id": assignment_id,
            "vtt_brief_attachment_id": brief_id
        },

        "constraints": {
            "must_create_pr": True,
            "must_run_tests": True,
            "must_update_code_logic": True,
            "max_files_outside_allowed_paths": 0
        }
    }

    return manifest


def validate_manifest(m, mode="generation"):
    """Devuelve lista de errores."""
    errors = []

    if m.get("schema_version") != "1.0":
        errors.append("schema_version debe ser '1.0'")

    if m.get("manifest_type") != "execution":
        errors.append("manifest_type debe ser 'execution'")

    if not (m.get("task") or {}).get("id"):
        errors.append("task.id vacio")

    agent_uuid = (m.get("agent") or {}).get("uuid")
    if not agent_uuid or not re.match(r"^[0-9a-f-]{36}$", agent_uuid, re.IGNORECASE):
        errors.append("agent.uuid no es UUID valido")

    role = (m.get("agent") or {}).get("role")
    if role not in VALID_ROLES:
        errors.append(f"agent.role '{role}' no en {VALID_ROLES}")

    if not m.get("allowedPaths"):
        errors.append("allowedPaths vacio — debe tener >= 1 entrada")

    if not m.get("expectedOutputs"):
        errors.append("expectedOutputs vacio — debe tener >= 1 entrada")

    if mode == "generation":
        wt = m.get("worktreePath")
        if not wt or not os.path.exists(wt):
            errors.append(f"worktreePath no existe en disco: {wt}")

    branch = m.get("branchExpected", "")
    task_id = (m.get("task") or {}).get("id", "")
    if branch and task_id and not branch.endswith(task_id) and "feature/" not in branch:
        errors.append(f"branchExpected '{branch}' no matches pattern 'feature/{task_id}'")

    return errors


def run_generation(args):
    token = os.environ.get(args.token_env)
    if not token:
        print(json.dumps({"success": False, "error": f"TOKEN env var ({args.token_env}) requerida"}))
        sys.exit(2)

    try:
        manifest = build_manifest(args, token)

        errors = validate_manifest(manifest, mode="generation")
        if errors:
            print(json.dumps({"success": False, "validation_errors": errors}, indent=2))
            sys.exit(3)

        # Write
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(json.dumps({
            "success": True,
            "manifest_path": args.output,
            "allowed_paths_count": len(manifest["allowedPaths"]),
            "expected_outputs_count": len(manifest["expectedOutputs"])
        }, indent=2))
        sys.exit(0)

    except FileNotFoundError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(2)

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(json.dumps({"success": False, "http_status": e.code, "error": body}))
        sys.exit(4)

    except Exception as e:
        print(json.dumps({"success": False, "error": f"{type(e).__name__}: {e}"}))
        sys.exit(4)


def run_read(args):
    if not os.path.exists(args.manifest_path):
        print(json.dumps({"success": False, "error": f"Manifest no existe: {args.manifest_path}"}))
        sys.exit(2)

    try:
        with open(args.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(json.dumps({"success": False, "error": f"JSON invalido: {e}"}))
        sys.exit(3)

    errors = validate_manifest(manifest, mode="read")
    if errors:
        print(json.dumps({"success": False, "validation_errors": errors}, indent=2))
        sys.exit(3)

    # Verify UUID match
    actual_uuid = (manifest.get("agent") or {}).get("uuid")
    if actual_uuid != args.expected_uuid:
        print(json.dumps({
            "success": False,
            "error": f"agent.uuid mismatch — manifest dice {actual_uuid}, esperado {args.expected_uuid}"
        }))
        sys.exit(2)

    print(json.dumps({
        "success": True,
        "worktreePath": manifest.get("worktreePath"),
        "branchExpected": manifest.get("branchExpected"),
        "allowedPaths": manifest.get("allowedPaths"),
        "expectedOutputs": manifest.get("expectedOutputs"),
        "taskId": (manifest.get("task") or {}).get("id"),
        "agentRole": (manifest.get("agent") or {}).get("role")
    }, indent=2))
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Generar/leer Execution Manifest")

    parser.add_argument("--validate-and-read", action="store_true",
                        help="Modo lectura por el agente")

    # Modo generacion
    parser.add_argument("--task-id")
    parser.add_argument("--agent-uuid")
    parser.add_argument("--agent-role", choices=list(VALID_ROLES))
    parser.add_argument("--assignment-path")
    parser.add_argument("--worktree-path")
    parser.add_argument("--branch-expected", default=None)
    parser.add_argument("--template-path")
    parser.add_argument("--output")
    parser.add_argument("--token-env", default="TOKEN")
    parser.add_argument("--base-url", default=os.environ.get("VTT_BASE_URL", DEFAULT_BASE_URL))

    # Modo lectura
    parser.add_argument("--manifest-path")
    parser.add_argument("--expected-uuid")

    args = parser.parse_args()

    if args.validate_and_read:
        if not args.manifest_path or not args.expected_uuid:
            print(json.dumps({
                "success": False,
                "error": "modo --validate-and-read requiere --manifest-path y --expected-uuid"
            }))
            sys.exit(1)
        run_read(args)
    else:
        required = [args.task_id, args.agent_uuid, args.agent_role,
                    args.assignment_path, args.worktree_path,
                    args.template_path, args.output]
        if not all(required):
            print(json.dumps({
                "success": False,
                "error": "modo generacion requiere: --task-id, --agent-uuid, --agent-role, --assignment-path, --worktree-path, --template-path, --output"
            }))
            sys.exit(1)
        run_generation(args)


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    main()
