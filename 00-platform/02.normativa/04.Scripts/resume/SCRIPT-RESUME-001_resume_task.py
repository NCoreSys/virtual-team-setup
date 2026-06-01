#!/usr/bin/env python3
"""
VTT.SCRIPT-RESUME-001 — Detectar auto-resume + determinar estrategia

Propósito: cuando sistema VTT auto-resume una tarea, este script:
  1. Detecta estado actual de la tarea
  2. Determina resume_strategy según status del Issue previo
  3. Busca el stash del .036 si aplica
Idempotente: Sí (consulta read-only + búsqueda local).

Aplicado por: SKILL-RESUME-001
Pertenece a: PROTOCOL-ASG-001 §5.4.7-8 (WORKFLOW-ASG-001.038 / CARD-ISS-005)

Inputs (CLI):
  --task-id              TASK_ID
  --previous-issue-id    UUID del Issue resuelto
  --agent-id             UUID del agente
  --worktree-path        (opcional) path del worktree para buscar stash

Outputs (stdout JSON):
  {
    "success": bool,
    "task_status": "task_in_progress" | "task_on_hold",
    "resume_strategy": "continue" | "wait_corrective" | "unknown",
    "stash_found": <stash_name|null>,
    "corrective_task_id": <uuid|null>,
    "ready_to_resume": bool,
    "previous_issue_status": "resolved" | "wont_fix" | "pending_corrective"
  }

Exit codes:
  0 OK (continue o wait_corrective)
  1 args/env faltantes
  2 No se pudo consultar tarea
  3 Estado inesperado
  4 No se pudo consultar Issue
  5 RULE-SCRIPT-001 violation
"""
import os
import sys
import json
import argparse
import subprocess
import urllib.request
import urllib.error


def enforce_canonical_path():
    expected_suffix = os.path.join("02.normativa", "04.Scripts", "resume")
    actual = os.path.abspath(__file__)
    if expected_suffix.replace("\\", "/") not in actual.replace("\\", "/"):
        print(json.dumps({"success": False, "error": "RULE-SCRIPT-001 violation"}))
        sys.exit(5)


def http_get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    enforce_canonical_path()

    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--previous-issue-id", required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--worktree-path", default=None)
    args = parser.parse_args()

    base_url = os.environ.get("VTT_BASE_URL")
    token = os.environ.get("VTT_TOKEN")
    if not base_url or not token:
        print(json.dumps({"success": False, "error": "VTT_BASE_URL y VTT_TOKEN requeridos"}))
        sys.exit(1)

    # 1. Estado actual de la tarea
    try:
        task = http_get(f"{base_url}/api/tasks/{args.task_id}", token)
        task_status = task.get("status", {}).get("code")
    except Exception as e:
        print(json.dumps({"success": False, "error": f"GET task fail: {e}"}))
        sys.exit(2)

    if task_status == "task_on_hold":
        print(json.dumps({
            "success": True,
            "task_status": task_status,
            "ready_to_resume": False,
            "message": "Tarea aún en on_hold — esperar",
        }))
        sys.exit(0)

    if task_status != "task_in_progress":
        print(json.dumps({
            "success": False,
            "task_status": task_status,
            "error": "Estado inesperado",
        }))
        sys.exit(3)

    # 2. Estado del Issue previo
    try:
        issue = http_get(f"{base_url}/api/issues/{args.previous_issue_id}", token)
        issue_status = issue.get("status")
    except Exception as e:
        print(json.dumps({"success": False, "error": f"GET issue fail: {e}"}))
        sys.exit(4)

    # 3. Determinar resume_strategy
    if issue_status in ("resolved", "wont_fix"):
        resume_strategy = "continue"
    elif issue_status == "pending_corrective":
        resume_strategy = "wait_corrective"
    else:
        resume_strategy = "unknown"

    # 4. Buscar stash (best effort)
    stash_found = None
    if args.worktree_path and resume_strategy == "continue":
        try:
            result = subprocess.run(
                ["git", "stash", "list"],
                capture_output=True, text=True, cwd=args.worktree_path
            )
            if result.returncode == 0:
                pattern = f"stash-{args.task_id}-on-hold"
                for line in result.stdout.split("\n"):
                    if pattern in line:
                        stash_found = line.split(":")[0]
                        break
        except Exception:
            pass

    # 5. Identificar corrective_task_id si aplica
    corrective_task_id = issue.get("correctiveTaskId") if resume_strategy == "wait_corrective" else None

    print(json.dumps({
        "success": True,
        "task_id": args.task_id,
        "task_status": task_status,
        "previous_issue_status": issue_status,
        "resume_strategy": resume_strategy,
        "stash_found": stash_found,
        "corrective_task_id": corrective_task_id,
        "ready_to_resume": resume_strategy == "continue",
        "wait_corrective_id": corrective_task_id,
    }))


if __name__ == "__main__":
    main()
