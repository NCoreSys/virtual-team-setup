#!/usr/bin/env python3
"""
VTT.SCRIPT-STATUS-003 — Actualizar SPRINT_STATUS_SX.md (dashboard del TL)

Propósito: regenerar secciones §1-§5 del SPRINT_STATUS desde datos de VTT.
           Preserva §6 (próximos pasos manual del TL).
           Agrega entry §7 Historial.
Idempotente: Parcial (§1-§5 se regeneran, §6-§7 se preservan/anexan).

Aplicado por: SKILL-STATUS-007
Pertenece a: PROTOCOL-ASG-001 §5.3.bis (WORKFLOW-ASG-001.028 / CARD-EXE-009)

Inputs (CLI):
  --sprint           ej. S03
  --status-path      path al SPRINT_STATUS_<sprint>.md
  --trigger-event    evento que dispara update
  --sprint-id        UUID del sprint en VTT
  --tl-name          (opcional) Nombre del TL

Outputs (stdout JSON):
  {"success": bool, "sections_updated": [...], "tasks_count_by_status": {...}}

Exit codes:
  0 OK
  1 args/env faltantes
  2 No se pudo consultar VTT
  5 RULE-SCRIPT-001 violation
"""
import os
import sys
import json
import argparse
import datetime
import urllib.request
import urllib.error


def enforce_canonical_path():
    expected_suffix = os.path.join("02.normativa", "04.Scripts", "status")
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
    parser.add_argument("--sprint", required=True)
    parser.add_argument("--status-path", required=True)
    parser.add_argument("--trigger-event", required=True)
    parser.add_argument("--sprint-id", required=True)
    parser.add_argument("--tl-name", default="TL")
    args = parser.parse_args()

    base_url = os.environ.get("VTT_BASE_URL")
    token = os.environ.get("VTT_TOKEN")
    if not base_url or not token:
        print(json.dumps({"success": False, "error": "VTT_BASE_URL y VTT_TOKEN requeridos"}))
        sys.exit(1)

    # 1. Tareas del sprint
    try:
        tasks_resp = http_get(f"{base_url}/api/sprints/{args.sprint_id}/tasks?include=status,assignedTo", token)
        tasks = tasks_resp.get("items", tasks_resp if isinstance(tasks_resp, list) else [])
    except Exception as e:
        print(json.dumps({"success": False, "error": f"GET tasks fail: {e}"}))
        sys.exit(2)

    # 2. Agrupar por status
    by_status = {}
    for t in tasks:
        code = (t.get("status") or {}).get("code", "unknown")
        by_status.setdefault(code, []).append(t)

    # 3. Issues abiertos (best effort)
    issues_open = []
    try:
        issues_resp = http_get(f"{base_url}/api/sprints/{args.sprint_id}/issues?status=open,acknowledged", token)
        issues_open = issues_resp.get("items", issues_resp if isinstance(issues_resp, list) else [])
    except Exception:
        pass

    # 4. Devlog critical/high pendientes (best effort)
    devlog_blockers = []
    try:
        devlog_resp = http_get(f"{base_url}/api/sprints/{args.sprint_id}/devlog?severity=critical,high&status=pending", token)
        devlog_blockers = devlog_resp.get("items", devlog_resp if isinstance(devlog_resp, list) else [])
    except Exception:
        pass

    # 5. Construir markdown
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(len(v) for v in by_status.values())
    approved_count = len(by_status.get("task_approved", []))

    md = f"""# SPRINT_STATUS_{args.sprint}

> Dashboard operativo del TL — vivo, no checkpoint. Actualizado al momento del evento.

## §1. Resumen Sprint {args.sprint}

- **Sprint:** {args.sprint}
- **Última actualización:** {now} por {args.tl_name}
- **Última trigger_event:** `{args.trigger_event}`
- **Progreso:** {approved_count}/{total} tareas aprobadas

## §2. Tareas por estado

"""

    status_icons = {
        "task_approved": "🟢",
        "task_in_review": "🟤",
        "task_in_progress": "🔵",
        "task_on_hold": "🟠",
        "task_pending": "🟡",
        "task_assigned": "🟡",
        "task_blocked": "🔴",
        "task_rejected": "🔴",
        "task_cancelled": "⚫",
    }

    for status_code in ["task_approved", "task_in_review", "task_in_progress", "task_on_hold", "task_pending", "task_assigned", "task_blocked"]:
        items = by_status.get(status_code, [])
        if not items:
            continue
        icon = status_icons.get(status_code, "")
        md += f"### {icon} {status_code} ({len(items)})\n\n"
        for t in items:
            tid = t.get("code") or t.get("id", "?")
            title = t.get("title", "?")
            assignee = (t.get("assignedTo") or {}).get("name", "—") if t.get("assignedTo") else "—"
            md += f"- {tid} — {title} — agente: {assignee}\n"
        md += "\n"

    md += "## §3. Blockers activos\n\n"
    if devlog_blockers:
        md += "| Tarea | Tipo | Descripción |\n|---|---|---|\n"
        for b in devlog_blockers:
            md += f"| {b.get('taskId', '?')} | {b.get('categoryCode', '?')} | {(b.get('title') or '?')[:80]} |\n"
    else:
        md += "_Sin blockers críticos pendientes._\n"

    md += "\n## §4. Issues abiertos\n\n"
    if issues_open:
        md += "| Issue | Severidad | Tipo | Tarea origen | Status |\n|---|---|---|---|---|\n"
        for i in issues_open:
            iid = str(i.get("id", "?"))[:8]
            md += f"| {iid} | {i.get('severity','?')} | {i.get('issueType','?')} | {i.get('sourceTaskId','?')} | {i.get('status','?')} |\n"
    else:
        md += "_Sin issues abiertos._\n"

    md += "\n## §5. KPIs\n\n"
    md += f"- **Tareas totales:** {total}\n"
    md += f"- **Aprobadas:** {approved_count}\n"
    md += f"- **Issues abiertos:** {len(issues_open)}\n"
    md += f"- **Devlog critical/high pendientes:** {len(devlog_blockers)} (debe ser 0 al cierre)\n"

    # §6 preservada — leer si existe el archivo
    section_6 = ""
    if os.path.exists(args.status_path):
        try:
            with open(args.status_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "## §6." in content:
                start = content.find("## §6.")
                end = content.find("## §7.")
                if start >= 0:
                    section_6 = content[start:end if end > 0 else len(content)].strip() + "\n"
        except Exception:
            pass

    if section_6:
        md += "\n" + section_6 + "\n"
    else:
        md += "\n## §6. Próximos pasos del TL\n\n_Editar manualmente — el script NO sobrescribe esta sección si existe contenido._\n"

    # §7 append-only
    existing_history = ""
    if os.path.exists(args.status_path):
        try:
            with open(args.status_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "## §7." in content:
                start = content.find("## §7.")
                hist_block = content[start:].strip()
                # Extraer entries (líneas que empiezan con "-")
                lines = hist_block.split("\n")
                history_lines = [l for l in lines if l.strip().startswith("-")]
                existing_history = "\n".join(history_lines)
        except Exception:
            pass

    md += f"\n## §7. Historial de cambios\n\n"
    md += f"- {now} — `{args.trigger_event}` — {args.tl_name}\n"
    if existing_history:
        md += existing_history + "\n"

    # Escribir
    os.makedirs(os.path.dirname(args.status_path) or ".", exist_ok=True)
    with open(args.status_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(json.dumps({
        "success": True,
        "sprint_status_path": args.status_path,
        "trigger_event": args.trigger_event,
        "tasks_count_by_status": {k: len(v) for k, v in by_status.items()},
        "issues_open": len(issues_open),
        "blockers_pending": len(devlog_blockers),
    }))


if __name__ == "__main__":
    main()
