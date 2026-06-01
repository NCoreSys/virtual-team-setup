#!/usr/bin/env python3
"""
VTT.SCRIPT-WT-004 — Verificar worktree dedicado del rol (PROC-COORD-01)

Propósito: verificar que el agente está en el worktree correcto antes de tocar código.
Idempotente: Sí (consulta read-only).

Aplicado por: SKILL-WT-001 (lectura/check) — los SCRIPT-WT-001/002/003 son setup/add/cleanup.
Pertenece a: PROTOCOL-ASG-001 §5.3.2 (WORKFLOW-ASG-001.032 / CARD-EXE-002)

Inputs (CLI):
  --repo            Nombre del repo
  --role            Rol del agente (BE/DB/FE/DO/QA/DL/UX/AR/SA/TL)
  --expected-path   Path esperado del worktree (.vtt/worktrees/<repo>-<rol>)

Outputs (stdout JSON):
  {
    "success": bool,
    "worktree_path": ...,
    "is_clone_base": bool (false esperado),
    "is_role_worktree": bool (true esperado),
    "current_branch": ...,
    "working_tree_clean": bool,
    "main_up_to_date": bool,
    "existing_feature_branches": [...]
  }

Exit codes:
  0 OK
  2 Worktree no existe
  3 No es worktree del rol (path inválido)
  4 git error
  5 RULE-SCRIPT-001 violation
  6 Checks fallaron
"""
import os
import sys
import json
import argparse
import subprocess


def enforce_canonical_path():
    expected_suffix = os.path.join("02.normativa", "04.Scripts", "worktree")
    actual = os.path.abspath(__file__)
    if expected_suffix.replace("\\", "/") not in actual.replace("\\", "/"):
        print(json.dumps({"success": False, "error": "RULE-SCRIPT-001 violation"}))
        sys.exit(5)


def run(cmd, cwd=None):
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main():
    enforce_canonical_path()

    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--role", required=True,
                        choices=["BE", "DB", "FE", "DO", "QA", "DL", "UX", "AR", "SA", "TL"])
    parser.add_argument("--expected-path", required=True)
    args = parser.parse_args()

    result = {
        "success": False,
        "worktree_path": args.expected_path,
        "is_clone_base": False,
        "is_role_worktree": False,
        "working_tree_clean": False,
        "main_up_to_date": False,
        "current_branch": None,
        "existing_feature_branches": [],
        "errors": [],
    }

    # Check 1: worktree existe
    if not os.path.isdir(args.expected_path):
        result["errors"].append(f"Worktree no existe: {args.expected_path}")
        print(json.dumps(result))
        sys.exit(2)

    # Check 2: ¿estamos en un worktree del rol?
    expected_pattern = f".vtt/worktrees/{args.repo}-{args.role.lower()}"
    if expected_pattern not in args.expected_path.replace("\\", "/"):
        result["errors"].append(f"Path no parece worktree del rol {args.role}")
        result["is_clone_base"] = True
        print(json.dumps(result))
        sys.exit(3)

    result["is_role_worktree"] = True

    # Check 3: branch actual
    rc, branch, err = run(["git", "branch", "--show-current"], cwd=args.expected_path)
    if rc != 0:
        result["errors"].append(f"git branch error: {err}")
        print(json.dumps(result))
        sys.exit(4)
    result["current_branch"] = branch

    # Check 4: working tree limpio
    rc, status, _ = run(["git", "status", "--porcelain"], cwd=args.expected_path)
    result["working_tree_clean"] = (rc == 0 and not status)

    # Check 5: main up to date (best effort — no falla si no hay remote)
    if branch == "main":
        run(["git", "fetch", "origin", "main"], cwd=args.expected_path)
        rc1, local_sha, _ = run(["git", "rev-parse", "HEAD"], cwd=args.expected_path)
        rc2, remote_sha, _ = run(["git", "rev-parse", "origin/main"], cwd=args.expected_path)
        if rc1 == 0 and rc2 == 0:
            result["main_up_to_date"] = (local_sha == remote_sha)

    # Check 6: branch feature/<TASK_ID> previa
    rc, branches, _ = run(["git", "branch", "--list", "feature/*"], cwd=args.expected_path)
    if rc == 0 and branches:
        result["existing_feature_branches"] = [b.strip(" *") for b in branches.split("\n") if b.strip()]

    result["success"] = (
        result["is_role_worktree"]
        and result["working_tree_clean"]
        and (branch in ("main", "master") or not result["working_tree_clean"])
    )

    print(json.dumps(result))
    sys.exit(0 if result["success"] else 6)


if __name__ == "__main__":
    main()
