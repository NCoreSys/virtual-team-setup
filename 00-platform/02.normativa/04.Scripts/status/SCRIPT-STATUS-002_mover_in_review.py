#!/usr/bin/env python3
"""
VTT.SCRIPT-STATUS-002 — Mover tarea a task_in_review

Propósito: transición task_in_progress → task_in_review al cierre del agente.
Idempotente: No (la operación es one-shot al cerrar la tarea).

Aplicado por: SKILL-STATUS-002
Pertenece a: PROTOCOL-ASG-001 §5.3.9 (WORKFLOW-ASG-001.010 / CARD-EXE-008)

Inputs (CLI):
  --task-id           ID de la tarea
  --agent-id          UUID del agente
  --reason            (opcional) Default: "Entrega completa según WORKFLOW-ASG-001.010"
  --skip-gate-check   DEBUG ONLY: saltar verificación review-gate

Inputs (env):
  $VTT_BASE_URL, $VTT_TOKEN

Outputs (stdout JSON):
  {"success": bool, "task_id": ..., "new_status": "task_in_review"}

Exit codes:
  0 OK
  1 args/env faltantes
  2 No se pudo consultar gate
  4 HTTP error en PATCH
  5 RULE-SCRIPT-001 violation
  7 Review-gate FAIL (canProceedToReview=false)
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

STATUS_ID_IN_REVIEW = "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d"


def enforce_canonical_path():
    expected_suffix = os.path.join("02.normativa", "04.Scripts", "status")
    actual = os.path.abspath(__file__)
    if expected_suffix.replace("\\", "/") not in actual.replace("\\", "/"):
        print(json.dumps({"success": False, "error": "RULE-SCRIPT-001 violation", "actual_path": actual}))
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

    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--reason", default="Entrega completa según WORKFLOW-ASG-001.010")
    parser.add_argument("--skip-gate-check", action="store_true", help="DEBUG ONLY")
    args = parser.parse_args()

    base_url = os.environ.get("VTT_BASE_URL")
    token = os.environ.get("VTT_TOKEN")
    if not base_url or not token:
        print(json.dumps({"success": False, "error": "VTT_BASE_URL y VTT_TOKEN requeridos"}))
        sys.exit(1)

    # Pre-check: review-gate
    if not args.skip_gate_check:
        gate_url = f"{base_url}/api/tasks/{args.task_id}/review-gate"
        try:
            gate = http_get(gate_url, token)
            if not gate.get("canProceedToReview"):
                print(json.dumps({
                    "success": False,
                    "error": "review-gate FAIL",
                    "blockers": gate.get("blockers", []),
                    "checks": gate.get("checks", {}),
                }))
                sys.exit(7)
        except Exception as e:
            print(json.dumps({"success": False, "error": f"No se pudo consultar review-gate: {e}"}))
            sys.exit(2)

    # Transición
    patch_url = f"{base_url}/api/tasks/{args.task_id}/status"
    payload = {
        "statusId": STATUS_ID_IN_REVIEW,
        "changedBy": args.agent_id,
        "reason": args.reason,
    }
    code, resp = http_patch(patch_url, token, payload)

    if code != 200:
        print(json.dumps({"success": False, "http_code": code, "response": resp}))
        sys.exit(4)

    print(json.dumps({
        "success": True,
        "task_id": args.task_id,
        "new_status": "task_in_review",
        "changed_by": args.agent_id,
    }))


if __name__ == "__main__":
    main()
