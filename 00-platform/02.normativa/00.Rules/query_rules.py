#!/usr/bin/env python3
"""
query_rules.py — Motor de filtros del sistema de Reglas VTT

Simula el endpoint /api/rules/applicable?taskId=... antes de tener BD.

Uso:
    # Validar el catálogo contra el schema
    python query_rules.py --validate

    # Listar todas las reglas activas
    python query_rules.py --list

    # Simular reglas aplicables a un contexto
    python query_rules.py --simulate-task MS-285

    # Probar contexto custom
    python query_rules.py --context-json '{
        "actor_type": "AGENT",
        "actor_role": "ws_developer",
        "actor_capabilities": ["tasks.read", "tasks.update"],
        "project_id": "memory-service",
        "phase_id": "04-Development",
        "phase_key": "04",
        "task": {
            "id": "MS-285",
            "has_code_files": true,
            "has_endpoints": false,
            "creates_assignment": false
        }
    }'

Outputs:
    Lista de reglas aplicables al contexto + summary por marker.
"""
import argparse
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
RULES_CATALOG = BASE_DIR / "rules_catalog.json"
RULES_SCHEMA = BASE_DIR / "rules_schema.json"
CAPABILITIES_CATALOG = BASE_DIR / "capabilities_catalog.json"
ROLES_CATALOG = BASE_DIR / "roles_catalog.json"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_catalog(catalog, schema):
    """Validación básica del catálogo contra el schema."""
    errors = []

    if catalog.get("schema_version") != "1.0":
        errors.append(f"schema_version != 1.0: {catalog.get('schema_version')}")

    required_top = ["schema_version", "generated_at", "rules", "summary"]
    for key in required_top:
        if key not in catalog:
            errors.append(f"Missing top-level key: {key}")

    valid_levels = {"PLATFORM", "ORGANIZATION", "WORKSPACE", "PROJECT", "PHASE", "TASK", "ROLE", "AGENT"}
    valid_actor_types = {"HUMAN", "AGENT", "SERVICE_ACCOUNT", "EXTERNAL"}
    valid_status = {"active", "deprecated", "superseded", "draft"}

    rule_ids = set()
    for i, rule in enumerate(catalog.get("rules", [])):
        rid = rule.get("id", f"<index {i}>")

        if rid in rule_ids:
            errors.append(f"{rid}: Duplicate rule ID")
        rule_ids.add(rid)

        for field in ["id", "title", "rule_text", "status", "scope", "actor_types", "markers", "source_origin"]:
            if field not in rule:
                errors.append(f"{rid}: Missing field '{field}'")

        if rule.get("status") not in valid_status:
            errors.append(f"{rid}: Invalid status '{rule.get('status')}'")

        scope = rule.get("scope", {})
        if scope.get("level") not in valid_levels:
            errors.append(f"{rid}: Invalid scope.level '{scope.get('level')}'")

        for at in rule.get("actor_types", []):
            if at not in valid_actor_types:
                errors.append(f"{rid}: Invalid actor_type '{at}'")

    return errors


def matches_scope(rule, ctx):
    """Verifica si el scope de la regla aplica al contexto."""
    scope = rule.get("scope", {})
    level = scope.get("level")

    if level == "PLATFORM":
        return True

    if level == "ORGANIZATION":
        if scope.get("organization_id") is None:
            return True
        return scope.get("organization_id") == ctx.get("organization_id")

    if level == "WORKSPACE":
        if scope.get("workspace_id") is None:
            return True
        return scope.get("workspace_id") == ctx.get("workspace_id")

    if level == "PROJECT":
        if scope.get("project_id") is None:
            return True
        return scope.get("project_id") == ctx.get("project_id")

    if level == "PHASE":
        if scope.get("phase_id") is not None:
            return scope.get("phase_id") == ctx.get("phase_id")
        if scope.get("phase_key") is not None:
            return scope.get("phase_key") == ctx.get("phase_key")
        return True

    if level == "TASK":
        criteria = scope.get("task_criteria") or {}
        if criteria.get("any") is True:
            return True
        task = ctx.get("task", {})
        for k, v in criteria.items():
            if k == "any":
                continue
            if task.get(k) != v:
                return False
        return True

    if level == "ROLE":
        role_codes = scope.get("role_codes") or []
        return ctx.get("actor_role") in role_codes

    if level == "AGENT":
        return scope.get("agent_id") == ctx.get("actor_id")

    return False


def matches_actor_type(rule, ctx):
    """Verifica si el actor_type del contexto está permitido por la regla."""
    return ctx.get("actor_type") in rule.get("actor_types", [])


def has_required_capabilities(rule, ctx):
    """Verifica si el actor tiene las capabilities requeridas."""
    required = rule.get("required_capabilities", [])
    if not required:
        return True
    actor_caps = set(ctx.get("actor_capabilities", []))
    return all(cap in actor_caps for cap in required)


def has_required_role(rule, ctx):
    """Verifica si el actor tiene un rol requerido (si la regla lo exige)."""
    required = rule.get("required_role_codes", [])
    if not required:
        return True
    return ctx.get("actor_role") in required


def get_applicable_rules(catalog, ctx):
    """Devuelve las reglas que aplican al contexto dado."""
    applicable = []
    for rule in catalog.get("rules", []):
        if rule.get("status") != "active":
            continue
        if not matches_scope(rule, ctx):
            continue
        if not matches_actor_type(rule, ctx):
            continue
        if not has_required_capabilities(rule, ctx):
            continue
        if not has_required_role(rule, ctx):
            continue
        applicable.append(rule)
    return applicable


def summarize(rules):
    """Resumen por marker."""
    by_marker = {
        "mandatory": 0,
        "sensitive": 0,
        "human_only": 0,
        "sod_enforcement": 0,
        "blocks_review_gate": 0,
        "agent_default_forbidden": 0,
    }
    by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for r in rules:
        markers = r.get("markers", {})
        for k in by_marker:
            if markers.get(k):
                by_marker[k] += 1
        sev = (r.get("violation") or {}).get("severity")
        if sev in by_severity:
            by_severity[sev] += 1
    return {"by_marker": by_marker, "by_severity": by_severity}


def cmd_validate():
    catalog = load_json(RULES_CATALOG)
    schema = load_json(RULES_SCHEMA)
    errors = validate_catalog(catalog, schema)
    if errors:
        print(f"[FAIL] Validación: {len(errors)} errores")
        for e in errors[:50]:
            print(f"  - {e}")
        return 1
    print(f"[OK] Validación: catálogo válido")
    print(f"     Total reglas: {len(catalog.get('rules', []))}")
    print(f"     Activas: {sum(1 for r in catalog['rules'] if r['status'] == 'active')}")
    return 0


def cmd_list():
    catalog = load_json(RULES_CATALOG)
    print(f"\n=== Reglas en el catálogo ({len(catalog['rules'])}) ===\n")
    for r in catalog["rules"]:
        scope = r["scope"]
        level = scope["level"]
        status = r["status"]
        sev = (r.get("violation") or {}).get("severity", "?")
        print(f"  [{r['id']:18s}] {level:13s} {status:10s} sev={sev:8s} {r['title']}")
    print()
    sm = catalog.get("summary", {})
    print(f"Summary by_level: {sm.get('by_level', {})}")
    print(f"Summary by_severity: {sm.get('by_severity', {})}")
    return 0


def cmd_simulate_task(task_id):
    """Simula contexto típico para una tarea del Memory Service."""
    catalog = load_json(RULES_CATALOG)
    ctx = {
        "actor_type": "AGENT",
        "actor_role": "ws_developer",
        "actor_id": "fake-uuid-agent",
        "actor_capabilities": [
            "tasks.read", "tasks.update", "tasks.status",
            "issues.create", "issues.update", "attachments.manage",
            "catalogs.read", "phases.read", "workspaces.read", "deliveries.read",
            "lifecycle.read", "users.read"
        ],
        "organization_id": "memory-service-org",
        "workspace_id": "memory-service-ws",
        "project_id": "memory-service",
        "phase_id": "04-Development",
        "phase_key": "04",
        "task": {
            "id": task_id,
            "any": True,
            "has_code_files": True,
            "has_endpoints": True,
            "creates_assignment": False,
            "creates_evidences": False,
            "installs_dependencies": False,
            "has_code_logic_files": True,
        },
    }
    print(f"\n=== Simulación: tarea {task_id} ===\n")
    print(f"Contexto: actor_type={ctx['actor_type']}, role={ctx['actor_role']}")
    print(f"          phase={ctx['phase_key']}, project={ctx['project_id']}")
    print(f"          task criteria: has_code_files=True, has_endpoints=True")
    print()
    rules = get_applicable_rules(catalog, ctx)
    print(f"=== Reglas aplicables: {len(rules)} ===\n")
    for r in rules:
        sev = (r.get("violation") or {}).get("severity", "?")
        markers = r.get("markers", {})
        flags = []
        if markers.get("mandatory"):
            flags.append("MAND")
        if markers.get("blocks_review_gate"):
            flags.append("GATE")
        if markers.get("sensitive"):
            flags.append("SENS")
        if markers.get("human_only"):
            flags.append("HUMN")
        if markers.get("agent_default_forbidden"):
            flags.append("AGNT-NO")
        flag_str = ",".join(flags) if flags else "-"
        print(f"  [{r['id']:18s}] sev={sev:8s} {flag_str:25s} {r['title']}")
    print()
    sm = summarize(rules)
    print(f"By marker:   {sm['by_marker']}")
    print(f"By severity: {sm['by_severity']}")
    return 0


def cmd_context_json(ctx_str):
    """Probar con contexto JSON custom."""
    catalog = load_json(RULES_CATALOG)
    try:
        ctx = json.loads(ctx_str)
    except json.JSONDecodeError as e:
        print(f"[FAIL] JSON inválido: {e}")
        return 1
    print(f"\n=== Contexto custom ===\n{json.dumps(ctx, indent=2)}\n")
    rules = get_applicable_rules(catalog, ctx)
    print(f"=== Reglas aplicables: {len(rules)} ===")
    for r in rules:
        print(f"  [{r['id']}] {r['title']}")
    print()
    return 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--validate", action="store_true", help="Validar catalog contra schema")
    grp.add_argument("--list", action="store_true", help="Listar todas las reglas")
    grp.add_argument("--simulate-task", metavar="TASK_ID", help="Simular reglas aplicables a tarea")
    grp.add_argument("--context-json", metavar="JSON", help="Contexto JSON custom")
    args = p.parse_args()

    if args.validate:
        return cmd_validate()
    if args.list:
        return cmd_list()
    if args.simulate_task:
        return cmd_simulate_task(args.simulate_task)
    if args.context_json:
        return cmd_context_json(args.context_json)


if __name__ == "__main__":
    sys.exit(main())
