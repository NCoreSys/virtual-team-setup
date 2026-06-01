#!/usr/bin/env python3
"""
VTT.SCRIPT-STATUS-005 — Solicitar task_on_hold con onHoldIssueId

Propósito: transición task_in_progress → task_on_hold via endpoint dedicado.
Idempotente: No.

Aplicado por: SKILL-STATUS-005
Pertenece a: PROTOCOL-ASG-001 §5.4.2 (WORKFLOW-ASG-001.036 / CARD-ISS-002)

ENDPOINT: PUT /api/tasks/:id/on-hold (NO PATCH /status — devuelve 405)
HEADER: x-user-id obligatorio
BODY: onHoldIssueId obligatorio (sin él no hay auto-resume)

Inputs (CLI):
  --task-id    ID de la tarea
  --issue-id   UUID del Issue creado en SCRIPT-ISSUE-001
  --user-id    UUID del agente
  --reason     Motivo 1 línea

Inputs (env):
  $VTT_BASE_URL, $VTT_TOKEN

Outputs (stdout JSON):
  {"success": bool, "task_id": ..., "new_status": "task_on_hold", "on_hold_issue_id": ...}

Exit codes:
  0 OK
  1 args/env faltantes
  4 HTTP error
  5 RULE-SCRIPT-001 violation
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error


def enforce_canonical_path():
    expected_suffix = os.path.join("02.normativa", "04.Scripts", "status")
    actual = os.path.abspath(__file__)
    if expected_suffix.replace("\\", "/") not in actual.replace("\\", "/"):
        print(json.dumps({"success": False, "error": "RULE-SCRIPT-001 violation"}))
        sys.exit(5)


def main():
    enforce_canonical_path()

    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--issue-id", required=True)
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()

    base_url = os.environ.get("VTT_BASE_URL")
    token = os.environ.get("VTT_TOKEN")
    if not base_url or not token:
        print(json.dumps({"success": False, "error": "VTT_BASE_URL y VTT_TOKEN requeridos"}))
        sys.exit(1)

    # PUT dedicado (NO PATCH /status)
    url = f"{base_url}/api/tasks/{args.task_id}/on-hold"
    payload = {
        "onHoldIssueId": args.issue_id,
        "reason": args.reason,
        "changedBy": args.user_id,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "x-user-id": args.user_id,
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(json.dumps({
            "success": False,
            "http_code": e.code,
            "response": body[:500],
            "hint": "Si 405 → revisar que sea PUT (no PATCH). Si 400 → revisar onHoldIssueId/changedBy. Si 403 → revisar x-user-id.",
        }))
        sys.exit(4)

    print(json.dumps({
        "success": True,
        "task_id": args.task_id,
        "new_status": "task_on_hold",
        "on_hold_issue_id": args.issue_id,
        "auto_resume_enabled": True,
    }))


if __name__ == "__main__":
    main()
