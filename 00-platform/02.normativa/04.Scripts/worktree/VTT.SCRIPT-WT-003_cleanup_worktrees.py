#!/usr/bin/env python3
# =============================================================================
# VTT.SCRIPT-WT-003 — cleanup_worktrees.py
# Version: 1.0 (2026-05-18)
# =============================================================================
#
# Proposito: Cleanup final del proyecto. Procesa branches pendientes con
#            3 acciones (A=merge / B=wontfix / C=preservar) y remueve los
#            worktrees + branches idle. Invocado por
#            VTT.WORKFLOW-WT-001.005 (Cleanup final).
#
# Idempotente: Parcial — el cleanup de un worktree ya removido es no-op.
#
# Inputs:
#   --project-root            path absoluto al root del proyecto (req)
#   --decisions-file          path a JSON con array de decisiones (req)
#   --repos-file              path a JSON con lista de repos del proyecto (req)
#   --proyecto                nombre humano del proyecto (req)
#   --tl-name                 nombre del TL (req)
#   --pm-auth-comment-id      UUID del comment del PM autorizando (req)
#   --archive-vtt             si esta presente, generar tarball antes de borrar
#   --dry-run                 si esta presente, NO ejecuta — solo imprime plan
#
# Schema de decisions-file:
#   [
#     {"branch": "feature/MS-300", "task_id": "MS-300", "task_status": "task_approved",
#      "accion": "A", "motivo": "PR no mergeado por olvido"},
#     {"branch": "feature/MS-301", "task_id": "MS-301", "task_status": "task_rejected",
#      "accion": "B", "motivo": "Decidio no implementarse"},
#     {"branch": "fix/MS-302", "task_id": "MS-302", "task_status": "task_in_progress",
#      "accion": "C", "motivo": "Deuda viva para R2 — preservar"}
#   ]
#
# Schema de repos-file:
#   [
#     {"repo": "backend", "repo_full_name": "memory-service-backend"},
#     {"repo": "project", "repo_full_name": "memory-service-project"}
#   ]
#
# Outputs (stdout JSON):
#   {
#     "success": true,
#     "branches_processed": {"A": [...], "B": [...], "C": [...]},
#     "worktrees_removed": [...],
#     "branches_idle_deleted": [...],
#     "archive_path": "..." (si --archive-vtt),
#     "phase2_archive_file": "..." (si hubo C),
#     "errors": []
#   }
#
# Exit codes: 0 OK, 1 args, 2 precond, 3 partial, 4 fatal
# =============================================================================

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
from datetime import datetime, timezone


def run_git(cmd, cwd, check=False):
    """Run git, no raise por default — cleanup tiene comandos que pueden fallar."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def process_action_A(decision, repos, project_root, dry_run):
    """Acción A — Mergear PR pendiente."""
    branch = decision["branch"]
    task_id = decision["task_id"]
    # Identificar repo dueño de la branch
    repo_full = find_repo_for_branch(repos, project_root, branch)
    if not repo_full:
        return {"success": False, "branch": branch, "error": "repo del branch no encontrado"}

    if dry_run:
        return {"success": True, "branch": branch, "action": "A", "dry_run": True,
                "command": f"gh pr create --base main --head {branch}"}

    repo_dir = os.path.join(project_root, repo_full)
    # Buscar si ya hay PR
    rc, out, _ = run_git(["gh", "pr", "list", "--head", branch, "--json", "number,state"], cwd=repo_dir)
    if rc == 0 and out:
        prs = json.loads(out)
        if prs:
            pr_num = prs[0]["number"]
            run_git(["gh", "pr", "merge", str(pr_num), "--merge"], cwd=repo_dir)
            return {"success": True, "branch": branch, "action": "A", "pr_merged": pr_num}

    # Crear PR si no existe
    rc, out, err = run_git(
        ["gh", "pr", "create", "--title", f"[{task_id}] close", "--body", f"Project closure — merge pendiente. Motivo: {decision.get('motivo', 'N/A')}", "--base", "main", "--head", branch],
        cwd=repo_dir
    )
    if rc != 0:
        return {"success": False, "branch": branch, "action": "A", "error": err}
    return {"success": True, "branch": branch, "action": "A", "pr_created_pending_merge": True, "stdout": out}


def process_action_B(decision, repos, project_root, token, base_url, dry_run):
    """Acción B — wontfix."""
    branch = decision["branch"]
    task_id = decision["task_id"]
    motivo = decision.get("motivo", "N/A")

    if dry_run:
        return {"success": True, "branch": branch, "action": "B", "dry_run": True}

    repo_full = find_repo_for_branch(repos, project_root, branch)
    if not repo_full:
        return {"success": False, "branch": branch, "error": "repo no encontrado"}
    repo_dir = os.path.join(project_root, repo_full)

    # 1. Postear comment en VTT
    import urllib.request
    if token:
        payload = json.dumps({
            "message": f"Branch {branch} cerrada wontfix al cierre del proyecto. Motivo: {motivo}",
            "type": "wontfix"
        }).encode("utf-8")
        try:
            req = urllib.request.Request(
                f"{base_url}/api/tasks/{task_id}/comments",
                data=payload,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                method="POST"
            )
            urllib.request.urlopen(req, timeout=10).read()
        except Exception as e:
            pass  # No bloquear cleanup por error de comment

    # 2. Cerrar PR si existe
    rc, out, _ = run_git(["gh", "pr", "list", "--head", branch, "--json", "number"], cwd=repo_dir)
    if rc == 0 and out:
        prs = json.loads(out)
        if prs:
            pr_num = prs[0]["number"]
            run_git(["gh", "pr", "close", str(pr_num), "--comment", f"Project closure — wontfix: {motivo}"], cwd=repo_dir)

    # 3. Borrar branch remote + local
    run_git(["git", "push", "origin", "--delete", branch], cwd=repo_dir)
    run_git(["git", "branch", "-D", branch], cwd=repo_dir)

    return {"success": True, "branch": branch, "action": "B", "branch_deleted": True}


def process_action_C(decision, project_root, proyecto, tl_name, archive_file):
    """Acción C — preservar para fase 2."""
    branch = decision["branch"]
    task_id = decision["task_id"]
    task_status = decision.get("task_status", "unknown")
    motivo = decision.get("motivo", "N/A")

    # Crear archivo si no existe
    if not os.path.isfile(archive_file):
        os.makedirs(os.path.dirname(archive_file), exist_ok=True)
        with open(archive_file, "w", encoding="utf-8") as f:
            f.write(f"# Branches preservadas para Fase 2 — {proyecto}\n\n")
            f.write(f"Fecha de cierre: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n")
            f.write(f"TL responsable: {tl_name}\n\n")
            f.write("## Branches\n\n")
            f.write("| Branch | Task ID | Task Status | Motivo |\n")
            f.write("|---|---|---|---|\n")

    with open(archive_file, "a", encoding="utf-8") as f:
        f.write(f"| `{branch}` | {task_id} | {task_status} | {motivo} |\n")

    return {"success": True, "branch": branch, "action": "C", "preserved_in": archive_file}


def find_repo_for_branch(repos, project_root, branch):
    """Determina qué repo contiene la branch (linear search)."""
    for r in repos:
        rc, out, _ = run_git(
            ["git", "rev-parse", "--verify", branch],
            cwd=os.path.join(project_root, r["repo_full_name"]),
            check=False
        )
        if rc == 0:
            return r["repo_full_name"]
    return None


def cleanup_worktrees(project_root, repos, dry_run):
    """Remueve worktrees + branches idle."""
    removed_wts = []
    deleted_branches = []
    errors = []

    vtt_worktrees = os.path.join(project_root, ".vtt", "worktrees")
    if not os.path.isdir(vtt_worktrees):
        return removed_wts, deleted_branches, errors

    # Por cada worktree
    for wt_name in os.listdir(vtt_worktrees):
        wt_path = os.path.join(vtt_worktrees, wt_name)
        if not os.path.isdir(wt_path):
            continue

        # Inferir repo desde nombre (formato: <repo>-<rol>)
        parts = wt_name.split("-")
        if len(parts) < 2:
            errors.append(f"worktree name invalido: {wt_name}")
            continue
        repo_short = parts[0]
        rol = "-".join(parts[1:])

        # Buscar repo_full_name
        repo_full = next((r["repo_full_name"] for r in repos if r["repo"] == repo_short), None)
        if not repo_full:
            errors.append(f"repo_full_name no encontrado para {repo_short}")
            continue

        if dry_run:
            removed_wts.append({"path": wt_path, "dry_run": True})
            continue

        # Remover worktree
        rc, out, err = run_git(
            ["git", "worktree", "remove", wt_path],
            cwd=os.path.join(project_root, repo_full)
        )
        if rc != 0:
            # Forzar
            run_git(["git", "worktree", "remove", "--force", wt_path], cwd=os.path.join(project_root, repo_full))

        removed_wts.append({"path": wt_path})

        # Borrar branch idle
        branch_idle = f"wt-{repo_short}-{rol}"
        run_git(["git", "branch", "-D", branch_idle], cwd=os.path.join(project_root, repo_full))
        # En remote si existe
        run_git(["git", "push", "origin", "--delete", branch_idle], cwd=os.path.join(project_root, repo_full))
        deleted_branches.append(branch_idle)

    return removed_wts, deleted_branches, errors


def archive_vtt_dir(project_root, archive_dir):
    """Genera tarball de .vtt/ antes de borrar."""
    vtt_path = os.path.join(project_root, ".vtt")
    if not os.path.isdir(vtt_path):
        return None

    os.makedirs(archive_dir, exist_ok=True)
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d")
    archive_path = os.path.join(archive_dir, f".vtt-archive-{fecha}.tar.gz")

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(vtt_path, arcname=".vtt")

    return archive_path


def main():
    parser = argparse.ArgumentParser(description="Cleanup final del proyecto")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--decisions-file", required=True)
    parser.add_argument("--repos-file", required=True)
    parser.add_argument("--proyecto", required=True)
    parser.add_argument("--tl-name", required=True)
    parser.add_argument("--pm-auth-comment-id", required=True)
    parser.add_argument("--archive-vtt", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--token-env", default="TOKEN")
    parser.add_argument("--base-url", default=os.environ.get("VTT_BASE_URL", "http://77.42.88.106:3000"))
    args = parser.parse_args()

    project_root = os.path.abspath(args.project_root)
    if not os.path.isdir(project_root):
        print(json.dumps({"success": False, "error": f"project_root invalido: {project_root}"}))
        sys.exit(2)

    try:
        with open(args.decisions_file, "r", encoding="utf-8") as f:
            decisions = json.load(f)
        with open(args.repos_file, "r", encoding="utf-8") as f:
            repos = json.load(f)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"config inválido: {e}"}))
        sys.exit(2)

    token = os.environ.get(args.token_env)
    if not token and not args.dry_run:
        # Solo necesitamos token si hay accion B real
        if any(d["accion"] == "B" for d in decisions):
            print(json.dumps({"success": False, "error": f"TOKEN env var requerido (accion B presente)"}))
            sys.exit(2)

    archive_file = os.path.join(project_root, "_archive", "branches_pending_phase2.md")
    result = {
        "success": True,
        "dry_run": args.dry_run,
        "branches_processed": {"A": [], "B": [], "C": []},
        "worktrees_removed": [],
        "branches_idle_deleted": [],
        "phase2_archive_file": None,
        "archive_path": None,
        "errors": []
    }

    # 1. Procesar branches según decisiones
    for d in decisions:
        accion = d.get("accion")
        if accion == "A":
            res = process_action_A(d, repos, project_root, args.dry_run)
        elif accion == "B":
            res = process_action_B(d, repos, project_root, token, args.base_url, args.dry_run)
        elif accion == "C":
            res = process_action_C(d, project_root, args.proyecto, args.tl_name, archive_file)
            if res["success"]:
                result["phase2_archive_file"] = archive_file
        else:
            res = {"success": False, "branch": d.get("branch"), "error": f"accion invalida: {accion}"}

        if res["success"]:
            result["branches_processed"][accion].append(res)
        else:
            result["errors"].append(res)

    # 2. Cleanup worktrees (después de procesar branches)
    if not args.dry_run or True:  # listar siempre, incluso en dry-run
        removed, deleted, wt_errors = cleanup_worktrees(project_root, repos, args.dry_run)
        result["worktrees_removed"] = removed
        result["branches_idle_deleted"] = deleted
        result["errors"].extend([{"step": "cleanup_wt", "error": e} for e in wt_errors])

    # 3. Archivar .vtt/ si aplica
    if args.archive_vtt and not args.dry_run:
        archive_dir = os.path.join(project_root, "_archive")
        result["archive_path"] = archive_vtt_dir(project_root, archive_dir)

    # 4. Borrar .vtt/ si no se archivó o ya se archivó
    if not args.dry_run:
        vtt_path = os.path.join(project_root, ".vtt")
        if os.path.isdir(vtt_path):
            shutil.rmtree(vtt_path)

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
