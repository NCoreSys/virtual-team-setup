#!/usr/bin/env python3
"""
VTT.SCRIPT-ISSUE-001 — Crear Issue en VTT + devlog blocker enlazado

Propósito: crear Issue formal cuando agente detecta bloqueante.
           Agrega marker textual [TASK:MS-XXX] [SPRINT:SX] automáticamente.
           Registra devlog `blocker` enlazado con el issueId.
Idempotente: No (siempre crea Issue nuevo).

Aplicado por: SKILL-ISSUE-001
Pertenece a: PROTOCOL-ASG-001 §5.4.1 (WORKFLOW-ASG-001.035 / CARD-ISS-001)

Inputs (CLI):
  --task-id        TASK_ID origen (parent)
  --type           dato_faltante | requirement | dependency | tech_error | scope_unclear | infra_failure
  --severity       critical | high | medium | low
  --title          Título corto
  --description    Description estructurada (4 secciones)
  --category       Sub-categoría (default "general")
  --project-id     UUID del proyecto en VTT
  --sprint         Sprint (ej. S03)
  --reported-by    UUID del agente reportador

Inputs (env):
  $VTT_BASE_URL, $VTT_TOKEN

Outputs (stdout JSON):
  {"success": bool, "issue_id": UUID, "devlog_entry_id_blocker": UUID, ...}

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
    expected_suffix = os.path.join("02.normativa", "04.Scripts", "issue")
    actual = os.path.abspath(__file__)
    if expected_suffix.replace("\\", "/") not in actual.replace("\\", "/"):
        print(json.dumps({"success": False, "error": "RULE-SCRIPT-001 violation"}))
        sys.exit(5)


def http_post(url, token, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") or "{}"
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"raw": body[:500]}


def main():
    enforce_canonical_path()

    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--type", required=True, choices=[
        "dato_faltante", "requirement", "dependency",
        "tech_error", "scope_unclear", "infra_failure"
    ])
    parser.add_argument("--severity", required=True, choices=["critical", "high", "medium", "low"])
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--category", default="general")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--sprint", default="")
    parser.add_argument("--reported-by", required=True)
    args = parser.parse_args()

    base_url = os.environ.get("VTT_BASE_URL")
    token = os.environ.get("VTT_TOKEN")
    if not base_url or not token:
        print(json.dumps({"success": False, "error": "VTT_BASE_URL y VTT_TOKEN requeridos"}))
        sys.exit(1)

    # Marker textual obligatorio (R3 del WORKFLOW-ASG-001.035)
    marker_prefix = f"[TASK:{args.task_id}]"
    if args.sprint:
        marker_prefix += f" [SPRINT:{args.sprint}]"

    title = args.title if marker_prefix in args.title else f"{marker_prefix} {args.title}"
    description = args.description if marker_prefix in args.description else f"{marker_prefix}\n\n{args.description}"

    # Crear Issue
    issue_url = f"{base_url}/api/projects/{args.project_id}/issues"
    issue_payload = {
        "title": title,
        "description": description,
        "issueType": args.type,
        "severity": args.severity,
        "category": args.category,
        "sourceTaskId": args.task_id,
        "reportedBy": args.reported_by,
        "status": "open",
    }
    code, resp = http_post(issue_url, token, issue_payload)
    if code not in (200, 201):
        print(json.dumps({"success": False, "http_code": code, "response": resp, "hint": "POST /api/projects/:id/issues"}))
        sys.exit(4)

    issue_id = resp.get("id") or resp.get("issueId")

    # Devlog blocker enlazado
    devlog_url = f"{base_url}/api/tasks/{args.task_id}/devlog-entries"
    devlog_payload = {
        "entries": [{
            "categoryCode": "blocker",
            "severity": args.severity,
            "title": f"Blocker: {args.title[:150]} (ISS-{issue_id})",
            "description": f"Issue formal: {issue_id}.\nTarea movida a task_on_hold via WORKFLOW-ASG-001.036.\nEsperando análisis del TL (WORKFLOW-ASG-001.011).",
            "reportedBy": args.reported_by,
            "status": "pending",
        }]
    }
    code2, devlog_resp = http_post(devlog_url, token, devlog_payload)
    devlog_entry_id = None
    if code2 in (200, 201):
        entries = devlog_resp.get("entries", [devlog_resp]) if isinstance(devlog_resp, dict) else devlog_resp
        if entries and isinstance(entries, list) and len(entries) > 0:
            first = entries[0]
            devlog_entry_id = first.get("id") if isinstance(first, dict) else None

    print(json.dumps({
        "success": True,
        "issue_id": issue_id,
        "issue_type": args.type,
        "severity": args.severity,
        "status": "open",
        "source_task_id": args.task_id,
        "devlog_entry_id_blocker": devlog_entry_id,
    }))


if __name__ == "__main__":
    main()
