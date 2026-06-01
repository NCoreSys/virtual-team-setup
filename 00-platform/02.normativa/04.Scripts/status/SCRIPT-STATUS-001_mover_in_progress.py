#!/usr/bin/env python3
"""
VTT.SCRIPT-STATUS-001 — Mover tarea a task_in_progress

Propósito: transición canónica task_assigned/task_pending → task_in_progress
           ejecutada por el AGENTE (no el TL).
Idempotente: Sí (si ya está en task_in_progress, salta con exit 0).

Aplicado por: SKILL-STATUS-001
Pertenece a: PROTOCOL-ASG-001 §5.3.3 (WORKFLOW-ASG-001.033 / CARD-EXE-003)
Cumple RULE-SCRIPT-001 (path canónico).

Inputs (CLI):
  --task-id    ID de la tarea (ej. MS-286)
  --agent-id   UUID del agente (auditoría)
  --reason     (opcional) Motivo. Default: "Iniciando ejecución según ASSIGNMENT"

Inputs (env):
  $VTT_BASE_URL
  $VTT_TOKEN

Outputs (stdout JSON):
  {"success": bool, "task_id": ..., "previous_status": ..., "new_status": ...}

Exit codes:
  0 OK (transición o skip si ya estaba)
  1 args inválidos / env vars faltantes
  2 No se pudo consultar tarea
  3 Estado inesperado (on_hold/cancelled/etc)
  4 HTTP error en PATCH
  5 RULE-SCRIPT-001 violation
  6 Estado no persistió
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

STATUS_ID_IN_PROGRESS = "2a76888a-e595-4cfc-ac4c-a3ae5087ef56"


def enforce_canonical_path():
    expected_suffix = os.path.join("02.normativa", "04.Scripts", "status")
    actual = os.path.abspath(__file__)
    if expected_suffix.replace("\\", "/") not in actual.replace("\\", "/"):
        print(json.dumps({
            "success": False,
            "error": "RULE-SCRIPT-001 violation",
            "message": "Script invocado fuera de path canónico",
            "actual_path": actual,
            "expected_suffix": expected_suffix,
        }))
        sys.exit(5)


def http_get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_patch(url, token, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") or "{}"
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"raw": body[:300]}


def main():
    enforce_canonical_path()

    parser = argparse.ArgumentParser(description="Mover tarea a task_in_progress")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--reason", default="Iniciando ejecución según ASSIGNMENT")
    args = parser.parse_args()

    base_url = os.environ.get("VTT_BASE_URL")
    token = os.environ.get("VTT_TOKEN")
    if not base_url or not token:
        print(json.dumps({"success": False, "error": "VTT_BASE_URL y VTT_TOKEN requeridos"}))
        sys.exit(1)

    # Pre-check: estado actual (idempotencia)
    task_url = f"{base_url}/api/tasks/{args.task_id}"
    try:
        task = http_get(task_url, token)
        current_status = task.get("status", {}).get("code")
    except Exception as e:
        print(json.dumps({"success": False, "error": f"No se pudo consultar tarea: {e}"}))
        sys.exit(2)

    if current_status == "task_in_progress":
        print(json.dumps({
            "success": True,
            "skipped": True,
            "reason": "Ya estaba en task_in_progress",
            "task_id": args.task_id,
        }))
        sys.exit(0)

    if current_status not in ("task_assigned", "task_pending"):
        print(json.dumps({
            "success": False,
            "error": f"Estado inesperado: {current_status}",
            "message": "Solo task_assigned/task_pending pueden transicionar a task_in_progress",
            "current_status": current_status,
        }))
        sys.exit(3)

    # Transición
    patch_url = f"{base_url}/api/tasks/{args.task_id}/status"
    payload = {
        "statusId": STATUS_ID_IN_PROGRESS,
        "changedBy": args.agent_id,
        "reason": args.reason,
    }
    code, resp = http_patch(patch_url, token, payload)

    if code != 200:
        print(json.dumps({"success": False, "http_code": code, "response": resp}))
        sys.exit(4)

    # Verificar persistencia
    task_after = http_get(task_url, token)
    new_status = task_after.get("status", {}).get("code")
    if new_status != "task_in_progress":
        print(json.dumps({
            "success": False,
            "error": "Estado no persistió",
            "new_status": new_status,
        }))
        sys.exit(6)

    print(json.dumps({
        "success": True,
        "task_id": args.task_id,
        "previous_status": current_status,
        "new_status": "task_in_progress",
        "changed_by": args.agent_id,
        "reason": args.reason,
    }))


if __name__ == "__main__":
    main()
