#!/usr/bin/env python3
# =============================================================================
# VTT.SCRIPT-WT-001 — setup_worktrees.py
# Version: 1.0 (2026-05-18)
# =============================================================================
#
# Proposito: Setup inicial idempotente de N worktrees + N workspaces VSCode
#            para un proyecto VTT multi-rol. Invocado por
#            VTT.WORKFLOW-WT-001.001 (Setup inicial one-time).
#
# Idempotente: Si — skip los que ya existen, no rompe estado previo.
#
# Inputs:
#   --project-root        path absoluto al root del proyecto (req)
#   --config              path al archivo JSON con configuracion (req)
#   --proyecto-display    nombre humano del proyecto (req)
#
# Schema del config JSON:
#   {
#     "roles": [
#       { "rol": "tl", "rol_descripcion": "Tech Lead", "repo": "project",
#         "repo_full_name": "memory-service-project" },
#       { "rol": "be", "rol_descripcion": "Backend Engineer", "repo": "backend",
#         "repo_full_name": "memory-service-backend" }
#     ]
#   }
#
# Outputs (stdout JSON):
#   {
#     "success": true,
#     "created_worktrees": [...],
#     "skipped_worktrees": [...],
#     "created_workspaces": [...],
#     "skipped_workspaces": [...],
#     "vtt_dir": "...",
#     "errors": []
#   }
#
# Exit codes:
#   0 OK
#   1 Argumentos invalidos
#   2 Precondicion no cumplida (project_root no existe, config invalido)
#   3 Error parcial (algunos worktrees fallaron — ver errors[])
#   4 Error fatal
# =============================================================================

import argparse
import json
import os
import subprocess
import sys


def run_git(cmd, cwd, check=True):
    """Run git command, return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8"
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git failed: {result.stderr.strip()}")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def ensure_vtt_dir(project_root):
    """Crea .vtt/{worktrees,workspaces,manifests} si no existen."""
    vtt = os.path.join(project_root, ".vtt")
    for sub in ("worktrees", "workspaces", "manifests"):
        os.makedirs(os.path.join(vtt, sub), exist_ok=True)
    return vtt


def add_to_gitignore(repo_dir):
    """Agrega .vtt/ al .gitignore del repo si no esta."""
    gi = os.path.join(repo_dir, ".gitignore")
    line = ".vtt/"
    if os.path.exists(gi):
        with open(gi, "r", encoding="utf-8") as f:
            if any(l.strip() == line for l in f):
                return False  # ya estaba
    with open(gi, "a", encoding="utf-8") as f:
        f.write(f"\n{line}\n")
    return True


def add_worktree(project_root, role_config):
    """Crea worktree. Devuelve dict con resultado."""
    repo = role_config["repo"]
    rol = role_config["rol"]
    repo_full = role_config["repo_full_name"]
    branch_idle = f"wt-{repo}-{rol}"

    repo_dir = os.path.join(project_root, repo_full)
    wt_path = os.path.join(project_root, ".vtt", "worktrees", f"{repo}-{rol}")

    if not os.path.isdir(repo_dir):
        return {"success": False, "rol": rol, "error": f"repo no existe: {repo_dir}"}

    if os.path.isdir(wt_path):
        return {"success": True, "rol": rol, "skipped": True, "reason": "worktree existe"}

    try:
        # Fetch
        run_git(["git", "fetch", "origin"], cwd=repo_dir)

        # Verificar si la branch idle existe
        rc, _, _ = run_git(["git", "rev-parse", "--verify", branch_idle], cwd=repo_dir, check=False)
        branch_exists = rc == 0

        if branch_exists:
            run_git(["git", "worktree", "add", wt_path, branch_idle], cwd=repo_dir)
        else:
            run_git(["git", "worktree", "add", wt_path, "-b", branch_idle, "origin/main"], cwd=repo_dir)

        return {
            "success": True,
            "rol": rol,
            "worktree_path": wt_path,
            "branch_idle": branch_idle,
            "branch_reused": branch_exists
        }
    except RuntimeError as e:
        return {"success": False, "rol": rol, "error": str(e)}


def generate_workspace(project_root, role_config, proyecto_display):
    """Crea .code-workspace. Skip si ya existe."""
    repo = role_config["repo"]
    rol = role_config["rol"]
    rol_desc = role_config["rol_descripcion"]
    rol_upper = rol.upper()

    ws_file = os.path.join(project_root, ".vtt", "workspaces", f"{repo}-{rol}.code-workspace")

    if os.path.isfile(ws_file):
        return {"success": True, "rol": rol, "skipped": True, "reason": "workspace existe"}

    workspace = {
        "folders": [
            {
                "name": f"{rol_upper} {rol_desc}",
                "path": f"../worktrees/{repo}-{rol}"
            }
        ],
        "settings": {
            "window.title": f"{rol_upper} - {rol_desc} | {proyecto_display}",
            "terminal.integrated.cwd": "${workspaceFolder}"
        }
    }

    with open(ws_file, "w", encoding="utf-8") as f:
        json.dump(workspace, f, indent=2, ensure_ascii=False)

    return {"success": True, "rol": rol, "workspace_path": ws_file}


def copy_template_manifest(project_root, vtt_setup):
    """Copia _template.execution.json desde el setup."""
    if not vtt_setup:
        return {"success": True, "skipped": True, "reason": "VTT_SETUP no definida"}

    src = os.path.join(vtt_setup, "03.templates", "normativa", "_template.execution.json")
    dst = os.path.join(project_root, ".vtt", "manifests", "_template.execution.json")

    if os.path.isfile(dst):
        return {"success": True, "skipped": True, "reason": "template existe"}

    if not os.path.isfile(src):
        # Generar fallback minimo
        fallback = {
            "schema_version": "1.0",
            "manifest_type": "execution",
            "task": {"id": "TBD"},
            "agent": {"uuid": "TBD", "role": "TBD"},
            "worktreePath": "TBD",
            "branchExpected": "TBD",
            "allowedPaths": [],
            "expectedOutputs": []
        }
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(fallback, f, indent=2)
        return {"success": True, "fallback_generated": True}

    import shutil
    shutil.copyfile(src, dst)
    return {"success": True, "copied_from": src}


def main():
    parser = argparse.ArgumentParser(description="Setup inicial de worktrees + workspaces")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--config", required=True, help="Path a JSON con array de roles")
    parser.add_argument("--proyecto-display", required=True)
    args = parser.parse_args()

    project_root = os.path.abspath(args.project_root)
    if not os.path.isdir(project_root):
        print(json.dumps({"success": False, "error": f"project_root no existe: {project_root}"}))
        sys.exit(2)

    if not os.path.isfile(args.config):
        print(json.dumps({"success": False, "error": f"config no existe: {args.config}"}))
        sys.exit(2)

    try:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(json.dumps({"success": False, "error": f"config JSON invalido: {e}"}))
        sys.exit(2)

    roles = config.get("roles", [])
    if not roles:
        print(json.dumps({"success": False, "error": "config.roles vacio"}))
        sys.exit(1)

    result = {
        "success": True,
        "vtt_dir": None,
        "created_worktrees": [],
        "skipped_worktrees": [],
        "created_workspaces": [],
        "skipped_workspaces": [],
        "errors": []
    }

    # 1. Crear estructura .vtt/
    result["vtt_dir"] = ensure_vtt_dir(project_root)

    # 2. Copiar template execution_manifest
    vtt_setup = os.environ.get("VTT_SETUP")
    template_result = copy_template_manifest(project_root, vtt_setup)
    result["template_manifest"] = template_result

    # 3. Actualizar .gitignore en cada repo unico
    repos_seen = set()
    for r in roles:
        repo_full = r["repo_full_name"]
        if repo_full in repos_seen:
            continue
        repos_seen.add(repo_full)
        repo_dir = os.path.join(project_root, repo_full)
        if os.path.isdir(repo_dir):
            add_to_gitignore(repo_dir)

    # 4. Crear worktrees
    for r in roles:
        res = add_worktree(project_root, r)
        if res.get("skipped"):
            result["skipped_worktrees"].append(res)
        elif res["success"]:
            result["created_worktrees"].append(res)
        else:
            result["errors"].append({"action": "add_worktree", **res})

    # 5. Generar workspaces
    for r in roles:
        res = generate_workspace(project_root, r, args.proyecto_display)
        if res.get("skipped"):
            result["skipped_workspaces"].append(res)
        elif res["success"]:
            result["created_workspaces"].append(res)
        else:
            result["errors"].append({"action": "generate_workspace", **res})

    if result["errors"]:
        result["success"] = False
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(3)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    main()
