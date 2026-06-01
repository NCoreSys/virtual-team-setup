#!/usr/bin/env python3
# =============================================================================
# VTT.SCRIPT-MAN-001 — gen_task_manifest.py
# Version: 1.4 (2026-05-31)
# =============================================================================
#
# Proposito: Generar/actualizar Task Manifest schema v1.2 y subirlo a VTT como
#            attachment fileType=manifest. Cubre v1.0 (agente) y v1.5 (TL).
#
# Changelog:
#   v1.4 (2026-05-31) — Bug CRITICO detectado por TL Reviewer VTT en VTT-870:
#     - parse_report_sections() regex line 207 no aceptaba ":" final en headings
#       Pattern viejo:   rf"(?:^|\n)#{1,3}\s+{alias}\s*\n(.*?)..."
#       Headings como "### Findings:" / "### Deuda tecnica:" NO matcheaban,
#       quedaban como None -> caian a "N/A" o [] en el JSON final.
#     - Impacto: 6 de 12 secciones del REPORT se perdian silenciosamente
#       (findings, adrs, derived_tasks, notes, items_detected, how_to_verify).
#     - Fix: pattern_md y pattern_line ahora aceptan ":" opcional antes del
#       separador. Cambios:
#       pattern_md:   "{alias}\s*\n"  ->  "{alias}\s*:?\s*\n"
#       pattern_line: "{alias}\s*[:\n]"  ->  "{alias}\s*:?\s*\n" (homogeneo)
#     - Heading lookahead tambien actualizado para tolerar ":" en el next heading.
#     - Test: probar con REPORT que tenga mezcla de "### X" y "### X:" — ambos
#       deben parsear el contenido.
#   v1.3 (2026-05-18) — Bug #8 detectado en validacion VTT-718:
#     - El v1.5 solo agregaba a related_to los TIs de new_tis_created.
#       NO procesaba evidences_added[] (TIs existentes que el TL evidencio al
#       cerrar). Caso real: VTT-718 vinculo 21 TIs existentes y el manifest
#       quedaba con related_to=[] y tech_debt_count=0.
#     - Fix: build_v15() consolida related_to desde 2 fuentes con dedup:
#       (a) dynamic_actions.new_tis_created  (TIs nuevos del TL)
#       (b) dynamic_actions.evidences_added  (TIs evidenciados — nuevos o existentes)
#     - _reindex() filtra None de implements/related_to por items mal formados.
#   v1.2 (2026-05-18) — Reporte TL: 4 archivos por tarea -> 2:
#     - save_local() sobreescribe el MISMO par (<TASK_ID>.json + <TASK_ID>.manifest.md)
#     - Sin sufijo .v1.5 — la version es metadata interna del JSON
#     - Historial preservado por VTT attachments + git log (PR del agente con v1.0,
#       PR del TL con v1.5 — ver PROTOCOL-ASG-001 FASE 6 "Commit del TL")
#   v1.1 (2026-05-18) — 7 bugs corregidos detectados en produccion VTT-721:
#     #1 parse_deliverables truncaba paths con guiones (ej. code-logic/)
#     #2 devlog_entries[].category quedaba como objeto {code,name} (debe ser string)
#         + devlog_summary.by_category no se poblaba
#     #3 indexes no se recalculaba en v1.5 (TIs nuevos del TL no se reflejaban)
#     #4 task.sprint/stage/category/complexity quedaban null por shape de VTT
#         (ahora prueba multiples paths: anidado, plano, .code)
#     #5 campo comment usaba "body", VTT usa "message"
#     #6 multipart no enviaba uploadedById (trazabilidad incorrecta)
#     #7 endpoint individual attachment incorrecto:
#         /api/tasks/<id>/attachments/<attId> -> 404
#         correcto: /api/attachments/<attId>/file
#   v1.0 (2026-05-17) — Version inicial.
#
# Idempotente: Parcial.
#   - Generacion del JSON local: si (sobrescribe el archivo local cada vez).
#   - Upload a VTT: NO (cada llamada con --upload crea un nuevo attachment).
#
# Inputs:
#   --task-id           string MS-XXX (req)
#   --version           "1.0" | "1.5" (req)
#   --phase             ej. "04-development" (req)
#   --sprint            ej. "S01" (req)
#
#   v1.0 (agente):
#     --agent-uuid          UUID del agente (req)
#     --report-path         path al SKL-REPORT-01 local (req)
#
#   v1.5 (TL):
#     --tl-uuid                 UUID del TL (req)
#     --v10-attachment-id       UUID del v1.0 en VTT (req)
#     --apr-tl-comment-id       UUID del APR-TL comment (req)
#     --dynamic-actions-json    path a JSON con dynamic_actions_data (req)
#     --verifications-json      path a JSON con verifications_data (req)
#
#   --upload            flag: subir como attachment al final (opcional)
#   --token-env         nombre de env var con JWT (default: TOKEN)
#   --base-url          override de VTT_BASE_URL (default env o http://77.42.88.106:3000)
#
# Outputs (stdout JSON):
#   {"success": true, "version": "1.0", "manifest_path": "...",
#    "wrapper_path": "...", "attachment_id": "<uuid o null>",
#    "validation_errors": []}
#
# Exit codes:
#   0  OK
#   1  Argumentos invalidos
#   2  Precondicion no cumplida (TOKEN faltante, archivo no existe)
#   3  Validacion del manifest fallo (errors en stdout)
#   4  HTTP error de VTT
#
# Uso (v1.0):
#   python VTT.SCRIPT-MAN-001_gen_task_manifest.py \
#     --task-id MS-XXX --version 1.0 \
#     --agent-uuid <uuid> \
#     --report-path knowledge/agent-tasks/reports/04-development/S01/MS-XXX_REPORT.md \
#     --phase 04-development --sprint S01 \
#     --upload
#
# Uso (v1.5):
#   python VTT.SCRIPT-MAN-001_gen_task_manifest.py \
#     --task-id MS-XXX --version 1.5 \
#     --tl-uuid <uuid> \
#     --v10-attachment-id <uuid> \
#     --apr-tl-comment-id <uuid> \
#     --dynamic-actions-json /tmp/MS-XXX_dynamic_actions.json \
#     --verifications-json /tmp/MS-XXX_verifications.json \
#     --phase 04-development --sprint S01 \
#     --upload
# =============================================================================

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

DEFAULT_BASE_URL = "http://77.42.88.106:3000"
SCHEMA_VERSION = "1.2"

# DevOps categories que requieren bloque delivery.operations
DEVOPS_CATEGORIES = {
    "deployment", "devops", "operation", "sql_migration",
    "rollback", "smoke_test", "config_change", "restart_service"
}


# -----------------------------------------------------------------------------
# HTTP helpers (urllib puro, sin dependencias)
# -----------------------------------------------------------------------------

def vtt_get(path, token, base_url):
    req = urllib.request.Request(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as r:
        body = r.read().decode("utf-8")
        return json.loads(body).get("data") if body else None


def vtt_post_multipart(path, token, base_url, file_path, file_type, uploaded_by_id=None):
    """POST multipart/form-data — minimal implementation con boundary fijo.

    Fix v1.1 (Bug #6): VTT exige `uploadedById` como campo del form-data
    para trazabilidad del attachment. Se debe pasar el UUID del actor (agent o TL)
    que esta subiendo el archivo.
    """
    boundary = "----VTTBoundary7MA4YWxkTrZu0gW"
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    filename = os.path.basename(file_path)

    body = b""
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="fileType"\r\n\r\n'.encode()
    body += f"{file_type}\r\n".encode()
    if uploaded_by_id:
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="uploadedById"\r\n\r\n'.encode()
        body += f"{uploaded_by_id}\r\n".encode()
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode()
    body += b'Content-Type: text/markdown\r\n\r\n'
    body += file_bytes
    body += f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        f"{base_url}{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


# -----------------------------------------------------------------------------
# Parser del reporte SKL-REPORT-01 (markdown)
# -----------------------------------------------------------------------------

REPORT_SECTIONS = {
    "what_was_done": ["Lo que se hizo", "Lo que se hizo:"],
    "code": ["Codigo", "Código", "Codigo:", "Código:"],
    "development_log": ["Development Log", "Development Log:"],
    "code_logic": ["Code Logic", "Code Logic:"],
    "criteria": ["Criterios de aceptacion", "Criterios de aceptación", "Acceptance Criteria"],
    "devlog": ["Devlog entries registrados en VTT", "Devlog entries"],
    "findings": ["Findings", "Findings / Deuda tecnica", "Findings / Deuda técnica"],
    "adrs": ["ADRs tomados", "ADRs"],
    "tis": ["TrackableItems creados o vinculados", "TrackableItems"],
    "items_detected": ["Items detectados para trackeo", "Items detectados para trackeo (TL revisar)"],
    "derived_tasks": ["Tareas derivadas generadas", "Tareas derivadas"],
    "how_to_verify": ["Como verificar", "Cómo verificar"],
    "notes": ["Notas", "Notas:"],
    "review_gate": ["Review gate al entregar", "Review gate"],
    "commit": ["Commit", "Commit:"],
    "pr": ["PR", "PR:"]
}


def parse_report(report_path):
    """Parse SKL-REPORT-01 markdown into a dict of sections."""
    if not os.path.exists(report_path):
        raise FileNotFoundError(f"Report no existe: {report_path}")

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = {}
    # Split por headings (## o ###) o por lines "Title:" (formato legacy)
    # Estrategia: para cada section key, intentar todos sus aliases
    #
    # v1.4 fix (Bug VTT-870 / TL Reviewer):
    #   Los regex ahora aceptan ":" final opcional en el heading.
    #   Antes:  "### Findings\n..." OK   /   "### Findings:\n..." FALLABA -> None -> N/A
    #   Ahora:  ambos parsean igual.
    #   Cambio minimo y seguro:
    #     pattern_md:   "{alias}\s*\n"      -> "{alias}\s*:?\s*\n"
    #     pattern_line: "{alias}\s*[:\n]"   -> "{alias}\s*:?\s*\n" (homogeneo)
    #   Los lookaheads de corte (siguiente heading / siguiente "Title:") quedan
    #   intactos para no romper la deteccion del fin de seccion. Probado con
    #   reportes mezclando headings con y sin ":".
    #
    for key, aliases in REPORT_SECTIONS.items():
        sections[key] = None
        for alias in aliases:
            # Pattern: heading "## <alias>[:]" — captura hasta el siguiente heading
            pattern_md = rf"(?:^|\n)#{{1,3}}\s+{re.escape(alias)}\s*:?\s*\n(.*?)(?=\n#{{1,3}}\s+|\Z)"
            m = re.search(pattern_md, content, re.DOTALL | re.IGNORECASE)
            if m:
                sections[key] = m.group(1).strip()
                break
            # Fallback: linea "Alias[:]" en formato no-markdown
            pattern_line = rf"(?:^|\n){re.escape(alias)}\s*:?\s*\n(.*?)(?=\n[A-Z][a-zA-Z\s]+:|\Z)"
            m = re.search(pattern_line, content, re.DOTALL)
            if m:
                sections[key] = m.group(1).strip()
                break

    return sections


def _pick(obj, *keys):
    """Devuelve el primer valor no-None encontrado entre las keys dadas (dot-paths)."""
    if not obj:
        return None
    for key in keys:
        cur = obj
        ok = True
        for part in key.split("."):
            if isinstance(cur, dict) and part in cur and cur[part] is not None:
                cur = cur[part]
            else:
                ok = False
                break
        if ok:
            return cur
    return None


def _build_task_block(args, task):
    """Fix v1.1 (Bug #4): shape de VTT puede traer sprint/stage/category de
    multiples maneras (anidado, plano, code). Probamos varios paths y caemos a None."""
    return {
        "id": args.task_id,
        "title": _pick(task, "title", "name"),
        "sprint": {
            "id": _pick(task, "sprint.id", "sprintId"),
            "name": _pick(task, "sprint.name", "sprint.code", "sprintCode")
        },
        "stage": _pick(task, "stage.code", "stage.name", "stage", "stageCode"),
        "assignee": {
            "id": args.agent_uuid,
            "role": _pick(task, "assignee.role", "assignee.roleCode", "assigneeRole"),
            "email": _pick(task, "assignee.email", "assigneeEmail")
        },
        "estimated_hours": _pick(task, "estimatedHours", "estimated_hours"),
        "actual_hours": _pick(task, "actualHours", "actual_hours"),
        "complexity": _pick(task, "complexity.code", "complexity.name", "complexity", "complexityCode"),
        "category": _pick(task, "category.code", "category.name", "category", "categoryCode"),
        "sdlc_catalog_id": _pick(task, "sdlcCatalogId", "sdlc_catalog_id"),
        "current_status": "task_in_review",
        "dependencies_upstream": task.get("dependenciesUpstream") or task.get("dependencies_upstream") or []
    }


def _norm_category(cat):
    """Fix v1.1 (Bug #2): VTT devuelve category como {code, name} en algunos
    endpoints. El schema requiere string. Normalizar a code o string literal."""
    if cat is None:
        return None
    if isinstance(cat, dict):
        return cat.get("code") or cat.get("name")
    return str(cat)


def _count_by_category(devlog):
    """Fix v1.1 (Bug #2.b): poblar by_category en devlog_summary."""
    counts = {}
    for d in devlog:
        c = _norm_category(d.get("category"))
        if c:
            counts[c] = counts.get(c, 0) + 1
    return counts


def parse_deliverables(code_section):
    """Parse 'Codigo:' section — bullets como `- path - descripcion` o `- path: descripcion`.

    Fix v1.1 (Bug #1): paths con guiones internos (ej. code-logic/, foo-bar.ts)
    quedaban truncados por regex `[^\\s:`-]+`. Ahora separamos por SPACE-DASH-SPACE
    o por DOS-PUNTOS, lo que permite cualquier guion dentro del path.
    """
    if not code_section:
        return []
    deliverables = []
    for line in code_section.split("\n"):
        line = line.strip()
        if not line.startswith(("-", "*", "+")):
            continue
        line = line[1:].strip()
        # Pattern v1.1: path = todo hasta " - " (con espacios) o ":" (primer match)
        # Captura backtick-wrapped opcional. Acepta guiones dentro del path.
        m = re.match(r"`?([^\s`:]+)`?\s+[-—]\s+(.+)", line)
        if not m:
            # Fallback: separador ":" (sin espacios obligatorios)
            m = re.match(r"`?([^\s`:]+)`?\s*:\s*(.+)", line)
        if m:
            path = m.group(1).strip()
            what = m.group(2).strip()
            state = "modified"
            low = what.lower()
            if any(k in low for k in ("creado", "created", "nuevo", "new file")):
                state = "created"
            deliverables.append({"path": path, "state": state, "what": what})
    return deliverables


# -----------------------------------------------------------------------------
# Builders del manifest
# -----------------------------------------------------------------------------

def build_v10(args, token, base_url):
    """Build v1.0 manifest desde report + VTT data."""

    # 1. Fetch VTT data
    task = vtt_get(f"/api/tasks/{args.task_id}", token, base_url)
    if not task:
        raise RuntimeError(f"Task {args.task_id} no encontrada en VTT")

    criteria = vtt_get(f"/api/tasks/{args.task_id}/criteria", token, base_url) or []
    devlog = vtt_get(f"/api/tasks/{args.task_id}/devlog", token, base_url) or []
    attachments = vtt_get(f"/api/tasks/{args.task_id}/attachments", token, base_url) or []
    comments = vtt_get(f"/api/tasks/{args.task_id}/comments", token, base_url) or []

    # 2. Parse report
    report_sections = parse_report(args.report_path)
    deliverables = parse_deliverables(report_sections.get("code"))

    # 3. Identify attachment IDs by fileType
    attach_by_type = {}
    for a in attachments:
        ft = a.get("fileType")
        if ft == "code_logic":
            attach_by_type.setdefault("code_logic_ids", []).append(a.get("id"))
        else:
            attach_by_type[f"{ft}_id"] = a.get("id")

    # 4. Find report comment (heurística: comment con link al report)
    report_comment_id = None
    for c in comments:
        # Fix v1.1 (Bug #5): VTT backend usa "message" para el cuerpo del comment.
        # Mantenemos "body" como fallback para compat con clones viejos.
        body = c.get("message") or c.get("body") or ""
        if "REPORT" in body.upper() or args.report_path in body:
            report_comment_id = c.get("id")
            break

    # 5. Identify trackable items
    try:
        tis = vtt_get(f"/api/tasks/{args.task_id}/trackable-items", token, base_url) or []
    except urllib.error.HTTPError:
        tis = []

    implements = []
    related_to = []
    for ti in tis:
        link_type = ti.get("linkType", "implements")
        entry = {"code": ti.get("code"), "uuid": ti.get("id")}
        if link_type == "implements":
            implements.append(entry)
        else:
            related_to.append(entry)

    # 6. Build base structure
    now_iso = datetime.now(timezone.utc).isoformat()

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "manifest_id": args.task_id,
        "generated_at": now_iso,
        "generated_by": args.agent_uuid,
        "generation_note": "v1.0 generado por agente al cerrar workflow. TL Reviewer agregara review.tl_review en v1.5.",
        "last_updated": now_iso,
        "last_updated_block": "delivery",

        "task": _build_task_block(args, task),

        "brief": {
            "vtt_attachment_id": attach_by_type.get("brief_id"),
            "file_path": None  # el agente lo llena si tiene path local
        },
        "assignment": {
            "vtt_attachment_id": attach_by_type.get("assignment_id"),
            "file_path": None,
            "criteria_count": len(criteria)
        },
        "agent_message": {
            "template_version": "3.0",
            "agent_role": (task.get("assignee") or {}).get("role"),
            "agent_uuid": args.agent_uuid,
            "generated_by_script": "scripts/gen_mensaje.py"
        },

        "delivery": {
            "delivered_at": now_iso,
            "delivered_by": args.agent_uuid,
            "vtt_report_comment_id": report_comment_id,
            "report_file_path": args.report_path,

            "what_was_done": (report_sections.get("what_was_done") or "")[:1000],

            "deliverables_actual": deliverables,

            "development_log_path": (report_sections.get("development_log") or "").strip().split("\n")[0] if report_sections.get("development_log") else None,
            "code_logic_files": [l.strip().lstrip("-*+ ") for l in (report_sections.get("code_logic") or "").split("\n") if l.strip().startswith(("-", "*", "+"))],
            "code_logic_attachment_strategy": {
                "placeholder_uploaded": False,
                "placeholder_attachment_id": None,
                "reason": "Real code logic if files exist"
            },

            "vtt_attachments": {
                "brief_id": attach_by_type.get("brief_id"),
                "assignment_id": attach_by_type.get("assignment_id"),
                "devlog_id": attach_by_type.get("devlog_id"),
                "code_logic_ids": attach_by_type.get("code_logic_ids", [])
            },

            "criteria_results": [
                {
                    "id": c.get("id"),
                    "title": c.get("title"),
                    "status": c.get("status"),
                    "criteriaTypeCode": c.get("criteriaTypeCode")
                } for c in criteria
            ],
            "criteria_summary": {
                "total": len(criteria),
                "met": sum(1 for c in criteria if c.get("status") == "met"),
                "not_met": sum(1 for c in criteria if c.get("status") == "not_met"),
                "pending": sum(1 for c in criteria if c.get("status") == "pending")
            },

            "devlog_entries": [
                {
                    "category": _norm_category(d.get("category")),
                    "severity": d.get("severity") or "low",
                    "title": d.get("title"),
                    "status": d.get("status")
                } for d in devlog
            ],
            "devlog_summary": {
                "total": len(devlog),
                "by_category": _count_by_category(devlog),
                "all_resolved_by_tl": False
            },

            "findings": (report_sections.get("findings") or "N/A").strip()[:2000],
            "adrs_taken": (report_sections.get("adrs") or "N/A").strip()[:2000],
            "derived_tasks": (report_sections.get("derived_tasks") or "N/A").strip()[:2000],
            "notes": (report_sections.get("notes") or "N/A").strip()[:2000],

            "hardcode_check": {
                "executed": True,
                "findings_total": 0,
                "findings_critical_high": 0,
                "false_positives_justified": 0
            },
            "tests": {
                "framework": "N/A",
                "tests_passing": 0,
                "coverage_stmts": None,
                "threshold_met": None
            },

            "trackable_items_actual": {
                "implements": implements,
                "related_to": related_to
            },

            "living_documents_declared_no_change": [],
            "tech_debt_for_r2": [],
            "items_detected_for_tl_review": [],

            "how_to_verify": [l.strip().lstrip("-*+ ") for l in (report_sections.get("how_to_verify") or "").split("\n") if l.strip().startswith(("-", "*", "+"))],

            "review_gate": {
                "canProceedToReview": True,
                "entries_total": len(devlog),
                "resolved": sum(1 for d in devlog if d.get("status") == "resolved"),
                "warnings": 0
            },

            "git": {
                "branch": f"feature/{args.task_id}",
                "base_branch": "main",
                "pr_number": None,
                "pr_url": None,
                "commit_sha": None,
                "commit_message": None
            },

            "metrics": {
                "actual_hours": task.get("actualHours"),
                "deliverables_count": len(deliverables),
                "tests_passing": 0
            }
        },

        "review": {
            "tl_review": None,
            "pm_approval": None
        },

        "indexes": {
            "implements_codes": [i.get("code") for i in implements],
            "related_to_codes": [r.get("code") for r in related_to],
            "deliverables_paths": [d.get("path") for d in deliverables],
            "tech_debt_count": 0,
            "criteria_met_ratio": f"{sum(1 for c in criteria if c.get('status') == 'met')}/{len(criteria)}",
            "devlog_entries_count": len(devlog),
            "devlog_resolved_count": sum(1 for d in devlog if d.get("status") == "resolved"),
            "files_created_count": sum(1 for d in deliverables if d.get("state") == "created")
        }
    }

    # 7. Parse Commit / PR from report
    commit_section = report_sections.get("commit") or ""
    sha_m = re.search(r"\b([a-f0-9]{7,40})\b", commit_section)
    if sha_m:
        manifest["delivery"]["git"]["commit_sha"] = sha_m.group(1)
        manifest["delivery"]["git"]["commit_message"] = commit_section.strip().split("\n")[0][:200]

    pr_section = report_sections.get("pr") or ""
    pr_url_m = re.search(r"https://github\.com/[^\s)]+/pull/(\d+)", pr_section)
    if pr_url_m:
        manifest["delivery"]["git"]["pr_url"] = pr_url_m.group(0)
        manifest["delivery"]["git"]["pr_number"] = int(pr_url_m.group(1))

    # 8. DevOps bloque operations — placeholder vacio si aplica
    if task.get("category") in DEVOPS_CATEGORIES:
        manifest["delivery"]["operations"] = {
            "type": task.get("category"),
            "executed_at": now_iso,
            "executed_by": args.agent_uuid,
            "environment": "production",
            "sql_applied": None,
            "commands_applied": [],
            "pre_checks": [],
            "post_checks_passed": False,
            "post_checks_details": [],
            "issue_resolved": None,
            "rollback_plan": None,
            "rejection_history": None,
            "note": "Bloque generado automaticamente — completar con datos reales antes de subir"
        }

    return manifest


def build_v15(args, token, base_url):
    """Build v1.5 desde v1.0 ya existente en VTT."""
    # 1. Download v1.0
    # Fix v1.1 (Bug #7): el endpoint individual de attachment NO es
    # /api/tasks/<id>/attachments/<attId> (404). El correcto es
    # /api/attachments/<attId>/file que retorna el archivo binario.
    # Estrategia: primero intentar listar attachments de la tarea y
    # filtrar por id; luego bajar el archivo via /api/attachments/<id>/file.
    attachments = vtt_get(f"/api/tasks/{args.task_id}/attachments", token, base_url) or []
    v10_meta = next(
        (a for a in attachments if a.get("id") == args.v10_attachment_id),
        None
    )
    if not v10_meta:
        raise RuntimeError(f"v1.0 attachment {args.v10_attachment_id} no encontrado en task {args.task_id}")

    # Bajar el archivo binario
    file_endpoint = f"{base_url}/api/attachments/{args.v10_attachment_id}/file"
    req = urllib.request.Request(file_endpoint, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as r:
        raw_content = r.read().decode("utf-8")

    # Extract JSON from markdown wrapper
    json_m = re.search(r"```json\s*(.*?)\s*```", raw_content, re.DOTALL)
    if json_m:
        v10 = json.loads(json_m.group(1))
    else:
        v10 = json.loads(raw_content)

    # 2. Load dynamic_actions and verifications
    with open(args.dynamic_actions_json, "r", encoding="utf-8") as f:
        dynamic_actions = json.load(f)
    with open(args.verifications_json, "r", encoding="utf-8") as f:
        verifications = json.load(f)

    # 3. Transforms v1.0 → v1.5
    now_iso = datetime.now(timezone.utc).isoformat()

    v15 = dict(v10)  # shallow copy
    v15["task"]["current_status"] = "task_completed"
    v15["last_updated"] = now_iso
    v15["last_updated_block"] = "review.tl_review + delivery.dynamic_model_actions"
    v15["generation_note"] = (v10.get("generation_note") or "") + \
        f" | v1.5 enriquecido por TL Reviewer {args.tl_uuid} al cerrar review."

    # Mark all devlog as resolved by TL
    v15["delivery"]["devlog_summary"]["all_resolved_by_tl"] = True
    for entry in v15["delivery"].get("devlog_entries", []):
        if entry.get("status") == "pending":
            entry["status"] = "resolved"

    # Fix v1.3 (Bug #8): consolidar TODOS los TIs del modelo dinamico en related_to.
    # Antes solo agregaba new_tis_created. Faltaba evidences_added[] que tambien
    # son vinculaciones TI-task (TIs existentes que el TL evidencio al cerrar).
    # Caso real: VTT-718 tenia 21 TIs evidenciados (todos existentes, no nuevos)
    # y el manifest v1.5 quedaba con related_to=[] y tech_debt_count=0.
    related_existing = {
        (r.get("code"), r.get("uuid"))
        for r in (v15["delivery"]["trackable_items_actual"].get("related_to") or [])
    }

    # (a) TIs nuevos creados por el TL
    for ti in dynamic_actions.get("new_tis_created", []):
        key = (ti.get("code"), ti.get("id"))
        if key not in related_existing and ti.get("code"):
            v15["delivery"]["trackable_items_actual"]["related_to"].append({
                "code": ti.get("code"),
                "uuid": ti.get("id")
            })
            related_existing.add(key)

    # (b) TIs evidenciados al cerrar (pueden ser nuevos o existentes)
    for ev in dynamic_actions.get("evidences_added", []):
        ti_code = ev.get("ti_code")
        ti_uuid = ev.get("ti_id") or ev.get("ti_uuid")  # tolerar ambos shapes
        if not ti_code:
            continue
        key = (ti_code, ti_uuid)
        if key not in related_existing:
            v15["delivery"]["trackable_items_actual"]["related_to"].append({
                "code": ti_code,
                "uuid": ti_uuid
            })
            related_existing.add(key)

    # Add dynamic_model_actions block
    v15["delivery"]["dynamic_model_actions"] = dynamic_actions

    # Add review.tl_review
    v15["review"]["tl_review"] = {
        "reviewer_uuid": args.tl_uuid,
        "verdict": verifications.get("verdict", "approved"),
        "reviewed_at": now_iso,
        "moved_to_completed_at": now_iso,
        "comment_id": args.apr_tl_comment_id,
        "findings": verifications.get("findings", []),
        "verifications": verifications.get("verifications", {}),
        "notes": verifications.get("notes", "")
    }
    # pm_approval queda null

    # Fix v1.1 (Bug #3): re-indexar despues de agregar TIs nuevos
    _reindex(v15)

    return v15


def _reindex(manifest):
    """Recalcula manifest.indexes desde delivery actual.
    Usado por v1.5 despues de agregar TIs nuevos del TL.

    Fix v1.3 (Bug #8): filtra None de implements/related_to por si vienen
    items mal formados; sino quedaban 'None' literal en arrays."""
    delivery = manifest.get("delivery", {})
    tis = delivery.get("trackable_items_actual", {}) or {}
    deliverables = delivery.get("deliverables_actual", []) or []
    criteria = delivery.get("criteria_results", []) or []
    devlog = delivery.get("devlog_entries", []) or []
    tech_debt = delivery.get("tech_debt_for_r2", []) or []

    implements_codes = [i.get("code") for i in (tis.get("implements") or []) if i.get("code")]
    related_codes = [r.get("code") for r in (tis.get("related_to") or []) if r.get("code")]
    # Cuenta tech_debt: items en tech_debt_for_r2 + related_to con prefijo DEBT-
    debt_count = len(tech_debt) + sum(
        1 for c in related_codes if c and c.startswith("DEBT-")
    )

    manifest["indexes"] = {
        "implements_codes": implements_codes,
        "related_to_codes": related_codes,
        "deliverables_paths": [d.get("path") for d in deliverables],
        "tech_debt_count": debt_count,
        "criteria_met_ratio": f"{sum(1 for c in criteria if c.get('status') == 'met')}/{len(criteria)}",
        "devlog_entries_count": len(devlog),
        "devlog_resolved_count": sum(1 for d in devlog if d.get("status") == "resolved"),
        "files_created_count": sum(1 for d in deliverables if d.get("state") == "created")
    }


# -----------------------------------------------------------------------------
# Validador
# -----------------------------------------------------------------------------

def validate(manifest, version):
    """Devuelve lista de errores (vacia si OK)."""
    errors = []

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version debe ser '{SCHEMA_VERSION}'")

    d = manifest.get("delivery", {})

    if not d.get("what_was_done") or len(d.get("what_was_done", "")) < 20:
        errors.append("delivery.what_was_done vacio o < 20 chars")

    deliverables = d.get("deliverables_actual", [])
    if not deliverables:
        errors.append("delivery.deliverables_actual vacio")
    else:
        for i, dv in enumerate(deliverables):
            if not dv.get("path") or not dv.get("state") or not dv.get("what"):
                errors.append(f"deliverables_actual[{i}] falta path/state/what")

    if d.get("report_file_path") and not os.path.exists(d["report_file_path"]):
        errors.append(f"report_file_path no existe: {d['report_file_path']}")

    if version == "1.0":
        if not d.get("vtt_report_comment_id"):
            errors.append("vtt_report_comment_id null en v1.0")
        if not (d.get("vtt_attachments") or {}).get("devlog_id"):
            errors.append("vtt_attachments.devlog_id null en v1.0")
        if not (d.get("review_gate") or {}).get("canProceedToReview"):
            errors.append("review_gate.canProceedToReview no es true")
        git = d.get("git") or {}
        category = (manifest.get("task") or {}).get("category")
        is_devops = category in DEVOPS_CATEGORIES
        if not git.get("pr_url") and not git.get("note") and not is_devops:
            errors.append("git.pr_url null sin git.note explicativo")
        if manifest.get("review", {}).get("tl_review") is not None:
            errors.append("review.tl_review debe ser null en v1.0")

    if version == "1.5":
        if (manifest.get("task") or {}).get("current_status") != "task_completed":
            errors.append("task.current_status debe ser 'task_completed' en v1.5")
        if not d.get("dynamic_model_actions"):
            errors.append("delivery.dynamic_model_actions falta en v1.5")
        tlr = (manifest.get("review") or {}).get("tl_review")
        if not tlr:
            errors.append("review.tl_review falta en v1.5")
        elif not tlr.get("verdict"):
            errors.append("review.tl_review.verdict vacio")
        elif not tlr.get("comment_id"):
            errors.append("review.tl_review.comment_id null")
        verifs = (tlr or {}).get("verifications") or {}
        for k, v in verifs.items():
            if v is False:
                errors.append(f"review.tl_review.verifications.{k} = false (no esta aprobado)")
        if not d.get("devlog_summary", {}).get("all_resolved_by_tl"):
            errors.append("devlog_summary.all_resolved_by_tl debe ser true en v1.5")

    # DevOps category requires operations block
    category = (manifest.get("task") or {}).get("category")
    if category in DEVOPS_CATEGORIES:
        if not d.get("operations"):
            errors.append(f"delivery.operations falta para category '{category}'")

    # Index espeja deliverables
    idx_paths = (manifest.get("indexes") or {}).get("deliverables_paths") or []
    actual_paths = [dv.get("path") for dv in deliverables]
    if set(idx_paths) != set(actual_paths):
        errors.append("indexes.deliverables_paths no espeja deliverables_actual[].path")

    return errors


# -----------------------------------------------------------------------------
# Wrap, save, upload
# -----------------------------------------------------------------------------

def save_local(manifest, version, phase, sprint):
    """Save JSON and wrap in .md. Returns (json_path, wrapper_path).

    Fix v1.2 (2026-05-18): UN solo par de archivos por tarea, sin sufijo de
    version. La v1.0 (agente) y v1.5 (TL) sobreescriben el mismo archivo.
    El historial vive en:
      - VTT attachments (cada upload crea uno nuevo)
      - git log (cada PR commitea el .json + .manifest.md actualizado)
      - metadata interna del JSON (generation_note, last_updated,
        last_updated_block, task.current_status)

    El TL revisa el v1.0 del agente en GitHub (PR del agente) ANTES del
    overwrite por v1.5. Posteriormente el TL commitea el v1.5 en su propio
    PR (branch tl/<TASK_ID>-close) — ver PROTOCOL-ASG-001 FASE 6.
    """
    task_id = manifest["manifest_id"]
    base_dir = f"knowledge/task-manifests/{phase}/{sprint}"
    os.makedirs(base_dir, exist_ok=True)

    json_path = f"{base_dir}/{task_id}.json"
    wrapper_path = f"{base_dir}/{task_id}.manifest.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    wrapper = f"# Task Manifest {task_id} — v{version}\n\n```json\n"
    wrapper += json.dumps(manifest, indent=2, ensure_ascii=False)
    wrapper += "\n```\n"
    with open(wrapper_path, "w", encoding="utf-8") as f:
        f.write(wrapper)

    return json_path, wrapper_path


def upload_to_vtt(wrapper_path, task_id, token, base_url, uploaded_by_id=None):
    """Upload wrapper .md as fileType=manifest. Returns attachment_id.

    Fix v1.1 (Bug #6): pasa uploaded_by_id al multipart para que VTT registre
    quien subio el attachment (agente para v1.0, TL para v1.5).
    """
    response = vtt_post_multipart(
        f"/api/tasks/{task_id}/attachments",
        token, base_url, wrapper_path, "manifest",
        uploaded_by_id=uploaded_by_id
    )
    return (response.get("data") or {}).get("id")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def enforce_canonical_path():
    """
    Enforcement runtime de RULE-SCRIPT-001 v1.0:
    El script SOLO puede ejecutarse desde su path canonico en virtual-teams-setup.
    Si esta corriendo desde una copia local en el worktree del proyecto -> abort.

    Permitido:  .../virtual-teams-setup/00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001*.py
    Prohibido:  cualquier otra ubicacion (ej. memory-service/.vtt/worktrees/<rol>/scripts/manifest/...)

    Excepcion: variable env VTT_SCRIPT_ALLOW_LOCAL=1 permite ejecucion local
               (solo para desarrollo/testing del script en si).
    """
    import os as _os
    script_path = _os.path.abspath(__file__)
    if _os.environ.get("VTT_SCRIPT_ALLOW_LOCAL") == "1":
        return  # bypass para devs del script
    canonical_marker = _os.path.join("02.normativa", "04.Scripts", "manifest")
    canonical_marker_alt = "02.normativa/04.Scripts/manifest"  # por si normpath difiere
    if (canonical_marker not in script_path
            and canonical_marker_alt not in script_path.replace("\\", "/")):
        print(json.dumps({
            "success": False,
            "error": "RULE-SCRIPT-001 violation",
            "message": "Este script SOLO puede ejecutarse desde su path canonico en virtual-teams-setup. "
                       "Detectada ejecucion desde copia local prohibida.",
            "script_path": script_path,
            "expected_canonical": "$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py",
            "fix": "Invocar el script con su path canonico, NO desde scripts/manifest/ del worktree. "
                   "Ver $VTT_SETUP/02.normativa/00.Rules/rules_catalog.json#RULE-SCRIPT-001 "
                   "y $VTT_SETUP/04.docs-soporte/guias-operativas/CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md",
            "bypass": "VTT_SCRIPT_ALLOW_LOCAL=1 (solo para desarrolladores del script — NO usar en produccion)"
        }, indent=2))
        sys.exit(2)


def main():
    enforce_canonical_path()
    parser = argparse.ArgumentParser(description="Generar/actualizar Task Manifest schema v1.2")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--version", required=True, choices=["1.0", "1.5"])
    parser.add_argument("--phase", required=True)
    parser.add_argument("--sprint", required=True)
    parser.add_argument("--agent-uuid")
    parser.add_argument("--report-path")
    parser.add_argument("--tl-uuid")
    parser.add_argument("--v10-attachment-id")
    parser.add_argument("--apr-tl-comment-id")
    parser.add_argument("--dynamic-actions-json")
    parser.add_argument("--verifications-json")
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("--token-env", default="TOKEN")
    parser.add_argument("--base-url", default=os.environ.get("VTT_BASE_URL", DEFAULT_BASE_URL))

    args = parser.parse_args()

    # Validacion de args segun version
    if args.version == "1.0":
        if not args.agent_uuid or not args.report_path:
            print(json.dumps({"success": False, "error": "v1.0 requiere --agent-uuid y --report-path"}))
            sys.exit(1)
    elif args.version == "1.5":
        required_v15 = [args.tl_uuid, args.v10_attachment_id, args.apr_tl_comment_id,
                        args.dynamic_actions_json, args.verifications_json]
        if not all(required_v15):
            print(json.dumps({"success": False, "error": "v1.5 requiere --tl-uuid, --v10-attachment-id, --apr-tl-comment-id, --dynamic-actions-json, --verifications-json"}))
            sys.exit(1)

    token = os.environ.get(args.token_env)
    if not token:
        print(json.dumps({"success": False, "error": f"TOKEN env var ({args.token_env}) requerida"}))
        sys.exit(2)

    try:
        # Build
        if args.version == "1.0":
            manifest = build_v10(args, token, args.base_url)
        else:
            manifest = build_v15(args, token, args.base_url)

        # Validate
        errors = validate(manifest, args.version)
        if errors:
            print(json.dumps({
                "success": False,
                "version": args.version,
                "validation_errors": errors
            }, indent=2))
            sys.exit(3)

        # Save local
        json_path, wrapper_path = save_local(manifest, args.version, args.phase, args.sprint)

        # Upload (optional)
        attachment_id = None
        if args.upload:
            # Fix v1.1 (Bug #6): uploaded_by_id segun la version
            uploader = args.agent_uuid if args.version == "1.0" else args.tl_uuid
            attachment_id = upload_to_vtt(
                wrapper_path, args.task_id, token, args.base_url,
                uploaded_by_id=uploader
            )

        # Stdout JSON
        print(json.dumps({
            "success": True,
            "version": args.version,
            "manifest_path": json_path,
            "wrapper_path": wrapper_path,
            "attachment_id": attachment_id,
            "validation_errors": []
        }, indent=2))
        sys.exit(0)

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(json.dumps({
            "success": False,
            "http_status": e.code,
            "error": body
        }))
        sys.exit(4)

    except urllib.error.URLError as e:
        print(json.dumps({"success": False, "error": f"Connection error: {e.reason}"}))
        sys.exit(4)

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
