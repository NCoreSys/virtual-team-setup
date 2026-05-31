#!/usr/bin/env python3
# =============================================================================
# VTT.SCRIPT-WT-002 — add_worktree.py
# Version: 1.0 (2026-05-18)
# =============================================================================
#
# Proposito: Agregar UN worktree + workspace para un rol nuevo. Invocado por
#            VTT.WORKFLOW-WT-001.003 (Agregar worktree de rol nuevo) o por
#            VTT.WORKFLOW-WT-001.004 §1.c (worktree auxiliar temporal).
#
# Diferencia con SCRIPT-WT-001:
#   - SCRIPT-WT-001 procesa un array de roles en bulk (setup inicial)
#   - SCRIPT-WT-002 procesa UN solo rol (rol nuevo o auxiliar)
#
# Idempotente: Si — devuelve "skipped" si ya existe.
#
# Inputs:
#   --project-root        path absoluto al root del proyecto (req)
#   --repo                nombre corto del repo (req, ej. "frontend")
#   --repo-full-name      nombre completo del repo (req, ej. "memory-service-frontend")
#   --rol                 rol lowercase (req, ej. "fe")
#   --rol-descripcion     descripcion humana (req, ej. "Frontend Engineer")
#   --proyecto-display    nombre del proyecto (req)
#   --suffix              opcional, sufijo para worktree auxiliar (ej. "-aux")
#
# Outputs (stdout JSON):
#   {
#     "success": true,
#     "rol": "fe",
#     "worktree_path": "...",
#     "workspace_path": "...",
#     "branch_idle": "wt-frontend-fe",
#     "skipped": false
#   }
#
# Exit codes: 0 OK, 1 args, 2 precond, 3 partial, 4 fatal
# =============================================================================

import argparse
import json
import os
import subprocess
import sys


def run_git(cmd, cwd, check=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if check and result.returncode != 0:
        raise RuntimeError(f"git failed: {result.stderr.strip()}")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def add_worktree(project_root, repo, repo_full_name, rol, suffix=""):
    """Crea worktree, devuelve dict."""
    role_full = f"{rol}{suffix}"  # ej. "be" o "be-aux"
    branch_idle = f"wt-{repo}-{role_full}"
    repo_dir = os.path.join(project_root, repo_full_name)
    wt_path = os.path.join(project_root, ".vtt", "worktrees", f"{repo}-{role_full}")

    if not os.path.isdir(repo_dir):
        return {"success": False, "error": f"repo no existe: {repo_dir}"}

    if os.path.isdir(wt_path):
        return {
            "success": True,
            "skipped": True,
            "worktree_path": wt_path,
            "branch_idle": branch_idle,
            "reason": "worktree existe"
        }

    try:
        # Asegurar .vtt/worktrees/ existe
        os.makedirs(os.path.dirname(wt_path), exist_ok=True)

        run_git(["git", "fetch", "origin"], cwd=repo_dir)

        rc, _, _ = run_git(["git", "rev-parse", "--verify", branch_idle], cwd=repo_dir, check=False)
        branch_exists = rc == 0

        if branch_exists:
            run_git(["git", "worktree", "add", wt_path, branch_idle], cwd=repo_dir)
        else:
            run_git(["git", "worktree", "add", wt_path, "-b", branch_idle, "origin/main"], cwd=repo_dir)

        return {
            "success": True,
            "worktree_path": wt_path,
            "branch_idle": branch_idle,
            "branch_reused": branch_exists,
            "skipped": False
        }
    except RuntimeError as e:
        return {"success": False, "error": str(e)}


def generate_workspace(project_root, repo, rol, rol_descripcion, proyecto_display, suffix=""):
    """Crea .code-workspace para el rol. Skip si existe."""
    role_full = f"{rol}{suffix}"
    rol_upper = rol.upper() + (suffix.upper() if suffix else "")

    ws_file = os.path.join(project_root, ".vtt", "workspaces", f"{repo}-{role_full}.code-workspace")

    if os.path.isfile(ws_file):
        return {
            "success": True,
            "skipped": True,
            "workspace_path": ws_file,
            "reason": "workspace existe"
        }

    os.makedirs(os.path.dirname(ws_file), exist_ok=True)

    workspace = {
        "folders": [
            {
                "name": f"{rol_upper} {rol_descripcion}",
                "path": f"../worktrees/{repo}-{role_full}"
            }
        ],
        "settings": {
            "window.title": f"{rol_upper} - {rol_descripcion} | {proyecto_display}",
            "terminal.integrated.cwd": "${workspaceFolder}"
        }
    }

    with open(ws_file, "w", encoding="utf-8") as f:
        json.dump(workspace, f, indent=2, ensure_ascii=False)

    return {"success": True, "workspace_path": ws_file, "skipped": False}


def main():
    parser = argparse.ArgumentParser(description="Agregar UN worktree + workspace")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--repo-full-name", required=True)
    parser.add_argument("--rol", required=True)
    parser.add_argument("--rol-descripcion", required=True)
    parser.add_argument("--proyecto-display", required=True)
    parser.add_argument("--suffix", default="", help="ej. '-aux' para worktree auxiliar")
    args = parser.parse_args()

    project_root = os.path.abspath(args.project_root)
    if not os.path.isdir(project_root):
        print(json.dumps({"success": False, "error": f"project_root no existe: {project_root}"}))
        sys.exit(2)

    try:
        wt_result = add_worktree(
            project_root, args.repo, args.repo_full_name, args.rol, args.suffix
        )
        if not wt_result["success"]:
            print(json.dumps({"success": False, "step": "add_worktree", **wt_result}))
            sys.exit(3)

        ws_result = generate_workspace(
            project_root, args.repo, args.rol, args.rol_descripcion,
            args.proyecto_display, args.suffix
        )
        if not ws_result["success"]:
            print(json.dumps({"success": False, "step": "generate_workspace", **ws_result}))
            sys.exit(3)

        print(json.dumps({
            "success": True,
            "rol": args.rol + args.suffix,
            "worktree_path": wt_result["worktree_path"],
            "workspace_path": ws_result["workspace_path"],
            "branch_idle": wt_result.get("branch_idle"),
            "worktree_skipped": wt_result.get("skipped", False),
            "workspace_skipped": ws_result.get("skipped", False)
        }, indent=2, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"success": False, "error": f"{type(e).__name__}: {e}"}))
        sys.exit(4)


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    main()
