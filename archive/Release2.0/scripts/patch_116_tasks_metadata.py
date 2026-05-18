"""
INIT-A-04: PATCH 116 tareas en VTT con metadata completa
Ejecuta: python3 patch_116_tasks_metadata.py
Salida: /tmp/patch_116_results.json
"""
import urllib.request, json, urllib.error

API = "http://77.42.88.106:3000"

USERS = {
    "PM":  "350831b2-e1ae-4dbe-b2eb-7e023ec2e103",
    "PJM": "0ff63a29-0bc0-465a-b9bd-5f71476bc91d",
    "TL":  "92225290-6b6b-4c1f-a940-dcb4262507aa",
    "SA":  "0c128e3b-db3b-4e31-b107-0379b5791233",
    "AR":  "e9403c25-c1f8-4b64-b2ef-f447d53115e2",
    "BE":  "ebbe3cee-abed-4b3b-860d-0a81f632b08a",
    "DB":  "6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7",
    "FE":  "d23c9cd9-a156-433b-8900-94add5488eec",
    "UX":  "a75a1dae-754a-4b6f-a3ff-db8d51f6a91b",
    "DL":  "b3a09269-cded-468c-a475-15a48f203cb0",
    "QA":  "613c9538-658c-45fe-a6d7-c1ea9ff04b78",
    "DO":  "322e3745-9756-4a7c-af11-44b33edef44d",
}

PRIORITY = {
    "C": "90ec3df2-fac4-40fa-b2ce-29daf0f4956e",
    "H": "1a617554-6319-4c56-826f-8ef49a0ff9cc",
    "M": "d0b619ef-27e7-42d8-8879-41030a602eed",
    "L": "95f2e731-41b9-4a7d-9a43-31f00a4ddd7e",
}

# (role, category, complexity, estimatedHours, priority)
TASKS = {
    # Phase 1 - Project Setup (cancelled, skip en runtime)
    "MS-001": ("DO",  "chore",         "MEDIUM", 4,  "M"),
    "MS-002": ("PJM", "chore",         "MEDIUM", 5,  "M"),
    "MS-003": ("PJM", "documentation", "MEDIUM", 14, "M"),
    "MS-004": ("DO",  "chore",         "MEDIUM", 4,  "M"),
    "MS-005": ("PM",  "documentation", "MEDIUM", 5,  "H"),
    # Phase 2 - Discovery
    "MS-006": ("SA",  "documentation", "MEDIUM", 3,  "M"),
    "MS-007": ("PM",  "documentation", "LOW",    2,  "M"),
    "MS-008": ("SA",  "documentation", "MEDIUM", 3,  "M"),
    "MS-009": ("PM",  "documentation", "LOW",    1,  "M"),
    # Phase 3 - Planning
    "MS-010": ("PM",  "documentation", "MEDIUM", 3,  "M"),
    "MS-011": ("PM",  "documentation", "MEDIUM", 2,  "M"),
    "MS-012": ("SA",  "documentation", "HIGH",   4,  "M"),
    "MS-013": ("PJM", "documentation", "LOW",    2,  "M"),
    "MS-014": ("PJM", "documentation", "MEDIUM", 3,  "M"),
    "MS-015": ("PJM", "documentation", "HIGH",   4,  "M"),
    "MS-016": ("PJM", "documentation", "MEDIUM", 3,  "M"),
    "MS-017": ("PM",  "documentation", "LOW",    2,  "M"),
    # Phase 4 - Analysis
    "MS-018": ("SA",  "documentation", "HIGH",   6,  "M"),
    "MS-019": ("AR",  "documentation", "HIGH",   4,  "M"),
    "MS-020": ("SA",  "documentation", "MEDIUM", 5,  "M"),
    "MS-021": ("SA",  "documentation", "HIGH",   8,  "M"),
    "MS-022": ("SA",  "documentation", "HIGH",   4,  "M"),
    "MS-023": ("UX",  "design",        "MEDIUM", 4,  "M"),
    "MS-024": ("SA",  "documentation", "HIGH",   6,  "M"),
    "MS-025": ("SA",  "documentation", "MEDIUM", 4,  "M"),
    # Phase 5 - Design UX/UI
    "MS-026": ("UX",  "design",        "MEDIUM", 3,  "M"),
    "MS-027": ("UX",  "design",        "MEDIUM", 4,  "M"),
    "MS-028": ("DL",  "design",        "MEDIUM", 3,  "M"),
    "MS-029": ("DL",  "design",        "HIGH",   4,  "M"),
    "MS-030": ("DL",  "design",        "MEDIUM", 3,  "M"),
    "MS-031": ("DL",  "design",        "HIGH",   4,  "M"),
    "MS-032": ("DL",  "design",        "HIGH",   4,  "M"),
    "MS-033": ("DL",  "design",        "MEDIUM", 2,  "M"),
    "MS-034": ("DL",  "design",        "MEDIUM", 2,  "M"),
    "MS-035": ("DL",  "design",        "MEDIUM", 2,  "M"),
    "MS-036": ("DL",  "design",        "LOW",    1,  "M"),
    "MS-037": ("DL",  "design",        "MEDIUM", 2,  "M"),
    "MS-038": ("DL",  "design",        "LOW",    1,  "C"),
    # Phase 6 - Design Technical
    "MS-039": ("AR",  "documentation", "HIGH",   6,  "M"),
    "MS-040": ("TL",  "documentation", "HIGH",   4,  "M"),
    "MS-041": ("DB",  "documentation", "HIGH",   6,  "M"),
    "MS-042": ("BE",  "documentation", "HIGH",   8,  "M"),
    "MS-043": ("AR",  "documentation", "HIGH",   6,  "M"),
    "MS-044": ("TL",  "documentation", "MEDIUM", 4,  "M"),
    "MS-045": ("AR",  "documentation", "HIGH",   4,  "M"),
    "MS-046": ("DO",  "documentation", "MEDIUM", 4,  "M"),
    "MS-047": ("TL",  "documentation", "MEDIUM", 3,  "M"),
    # Phase 7 - Development S01
    "MS-048": ("DB",  "development",   "HIGH",   3,  "H"),
    "MS-049": ("DB",  "development",   "MEDIUM", 2,  "M"),
    "MS-050": ("DB",  "development",   "LOW",    1,  "M"),
    "MS-051": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-052": ("BE",  "development",   "LOW",    1,  "M"),
    # S02
    "MS-053": ("BE",  "development",   "HIGH",   4,  "H"),
    "MS-054": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-055": ("BE",  "development",   "HIGH",   3,  "M"),
    "MS-056": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-057": ("BE",  "development",   "LOW",    1,  "M"),
    # S03
    "MS-058": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-059": ("BE",  "development",   "HIGH",   4,  "C"),
    "MS-060": ("BE",  "development",   "HIGH",   2,  "M"),
    "MS-061": ("QA",  "testing",       "MEDIUM", 2,  "M"),
    "MS-062": ("QA",  "testing",       "MEDIUM", 2,  "M"),
    # S04
    "MS-063": ("BE",  "development",   "MEDIUM", 3,  "M"),
    "MS-064": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-065": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-066": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-067": ("BE",  "development",   "LOW",    1,  "M"),
    "MS-068": ("BE",  "testing",       "MEDIUM", 2,  "M"),
    # S05
    "MS-069": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-070": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-071": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-072": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-073": ("BE",  "development",   "MEDIUM", 2,  "M"),
    "MS-074": ("BE",  "testing",       "LOW",    1,  "M"),
    # S06
    "MS-075": ("DO",  "deployment",    "MEDIUM", 2,  "M"),
    "MS-076": ("DO",  "deployment",    "MEDIUM", 2,  "M"),
    "MS-077": ("DO",  "deployment",    "LOW",    1,  "M"),
    "MS-078": ("BE",  "development",   "HIGH",   4,  "M"),
    "MS-079": ("QA",  "testing",       "HIGH",   3,  "M"),
    "MS-080": ("QA",  "testing",       "MEDIUM", 2,  "M"),
    # UI-01
    "MS-081": ("FE",  "development",   "MEDIUM", 2,  "M"),
    "MS-082": ("FE",  "development",   "LOW",    1,  "M"),
    "MS-083": ("FE",  "development",   "HIGH",   5,  "M"),
    "MS-084": ("FE",  "development",   "HIGH",   6,  "M"),
    "MS-085": ("FE",  "development",   "MEDIUM", 2,  "M"),
    # UI-02
    "MS-086": ("FE",  "development",   "HIGH",   4,  "M"),
    "MS-087": ("FE",  "development",   "MEDIUM", 4,  "M"),
    "MS-088": ("FE",  "development",   "MEDIUM", 4,  "M"),
    # UI-03
    "MS-089": ("FE",  "development",   "HIGH",   5,  "M"),
    "MS-090": ("FE",  "development",   "HIGH",   5,  "M"),
    # UI-04
    "MS-091": ("FE",  "development",   "MEDIUM", 3,  "M"),
    "MS-092": ("FE",  "development",   "LOW",    2,  "M"),
    "MS-093": ("FE",  "development",   "MEDIUM", 3,  "M"),
    # Phase 8 - Testing
    "MS-094": ("QA",  "testing",       "MEDIUM", 4,  "M"),
    "MS-095": ("QA",  "testing",       "HIGH",   8,  "M"),
    "MS-096": ("DO",  "testing",       "MEDIUM", 4,  "M"),
    "MS-097": ("QA",  "testing",       "HIGH",   8,  "M"),
    "MS-098": ("QA",  "testing",       "HIGH",   6,  "M"),
    "MS-099": ("QA",  "testing",       "HIGH",   8,  "M"),
    "MS-100": ("QA",  "testing",       "HIGH",   6,  "C"),
    "MS-101": ("AR",  "testing",       "HIGH",   4,  "H"),
    "MS-102": ("PM",  "testing",       "MEDIUM", 4,  "M"),
    "MS-103": ("BE",  "bugfix",        "HIGH",   8,  "M"),
    # Phase 9 - Deploy
    "MS-104": ("DO",  "deployment",    "MEDIUM", 4,  "M"),
    "MS-105": ("DO",  "deployment",    "HIGH",   6,  "M"),
    "MS-106": ("DO",  "deployment",    "MEDIUM", 4,  "M"),
    "MS-107": ("QA",  "testing",       "MEDIUM", 3,  "M"),
    "MS-108": ("DO",  "deployment",    "HIGH",   4,  "C"),
    "MS-109": ("DO",  "deployment",    "MEDIUM", 3,  "M"),
    "MS-110": ("TL",  "documentation", "MEDIUM", 2,  "M"),
    # Phase 10 - Operations
    "MS-111": ("DO",  "deployment",    "MEDIUM", 3,  "M"),
    "MS-112": ("PM",  "documentation", "LOW",    2,  "M"),
    "MS-113": ("TL",  "documentation", "MEDIUM", 2,  "M"),
    "MS-114": ("PM",  "documentation", "MEDIUM", 3,  "M"),
    "MS-115": ("AR",  "documentation", "MEDIUM", 2,  "M"),
    "MS-116": ("AR",  "documentation", "HIGH",   3,  "M"),
}


def get_token():
    req = urllib.request.Request(
        f'{API}/api/auth/service-token',
        data=json.dumps({'userId': '350831b2-e1ae-4dbe-b2eb-7e023ec2e103',
                         'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'}).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())['data']['token']


def get_task(token, task_id):
    req = urllib.request.Request(
        f'{API}/api/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())['data']


def patch_task(token, task_id, payload):
    req = urllib.request.Request(
        f'{API}/api/tasks/{task_id}',
        data=json.dumps(payload).encode(),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='PATCH')
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        return None, json.loads(e.read())


def main():
    print("Obteniendo token...")
    token = get_token()
    with open('/tmp/token_pm.txt', 'w') as f:
        f.write(token)

    results = {"patched": [], "skipped": [], "errors": []}
    patched = skipped = errors = 0

    print(f"Procesando {len(TASKS)} tareas...\n")

    for task_id, (role, category, complexity, hours, priority_code) in TASKS.items():
        expected_assignee = USERS[role]
        expected_priority = PRIORITY[priority_code]

        try:
            t = get_task(token, task_id)
        except Exception as e:
            print(f"  {task_id} GET ERROR: {e}")
            errors += 1
            results["errors"].append({"task": task_id, "error": str(e)})
            continue

        status = t.get('status', {}).get('code', '')
        if status == 'task_cancelled':
            skipped += 1
            results["skipped"].append(task_id)
            print(f"  {task_id} SKIP (cancelled)")
            continue

        current_assignee = (t.get('assignee') or {}).get('id', '')
        current_complexity = t.get('complexity') or ''
        current_category = t.get('category') or ''
        current_priority = (t.get('priority') or {}).get('id', '')
        current_hours = t.get('estimatedHours', 0)

        payload = {}
        if current_complexity != complexity:
            payload['complexity'] = complexity
        if current_category != category:
            payload['category'] = category
        if current_assignee != expected_assignee:
            payload['assignedToId'] = expected_assignee
        if current_priority != expected_priority:
            payload['priorityId'] = expected_priority
        if current_hours != hours:
            payload['estimatedHours'] = hours

        if not payload:
            skipped += 1
            results["skipped"].append(task_id)
            print(f"  {task_id} OK")
            continue

        d, err = patch_task(token, task_id, payload)
        if err:
            print(f"  {task_id} ERROR: {err.get('error')}")
            errors += 1
            results["errors"].append({"task": task_id, "error": err})
        else:
            patched += 1
            results["patched"].append({"task": task_id, "fields": list(payload.keys())})
            print(f"  {task_id} PATCHED [{', '.join(payload.keys())}]")

    results["summary"] = {"total": len(TASKS), "patched": patched, "skipped": skipped, "errors": errors}

    with open('/tmp/patch_116_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n=== RESULTADO ===")
    print(f"Total:   {len(TASKS)}")
    print(f"Patched: {patched}")
    print(f"OK/Skip: {skipped}")
    print(f"Errors:  {errors}")


if __name__ == '__main__':
    main()
