import urllib.request, urllib.error, json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://77.42.88.106:3000"
PJM_ID   = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
SK       = "hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"
PM  = "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"
PJM = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
TL  = "92225290-6b6b-4c1f-a940-dcb4262507aa"
BE  = "ebbe3cee-abed-4b3b-860d-0a81f632b08a"
DB  = "6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7"
FE  = "d23c9cd9-a156-433b-8900-94add5488eec"
QA  = "613c9538-658c-45fe-a6d7-c1ea9ff04b78"
DO  = "322e3745-9756-4a7c-af11-44b33edef44d"
DL  = "b3a09269-cded-468c-a475-15a48f203cb0"
AR  = "e9403c25-c1f8-4b64-b2ef-f447d53115e2"
LOW = "95f2e731-41b9-4a7d-9a43-31f00a4ddd7e"
MED = "d0b619ef-27e7-42d8-8879-41030a602eed"

with open("c:/Users/Martin/Documents/virtual-teams/Project_setup/deprecated/scripts/mem_structure.json") as f:
    struct = json.load(f)
D = struct["deliverables"]
def dv(phase, name):
    for it in D[phase]:
        if it["name"] == name: return it["id"]
    raise ValueError(f"{phase}/{name}")

FAILED = {
    "MEM-003": (dv("Project Setup","Project Foundation Ready"), PJM, LOW, 1, "LOW", "documentation"),
    "MEM-007": (dv("Discovery","Problem Definition"), PM, LOW, 2, "LOW", "review"),
    "MEM-009": (dv("Discovery","Value Proposition"), PM, LOW, 1, "LOW", "review"),
    "MEM-013": (dv("Planning","Stakeholders"), PJM, LOW, 2, "LOW", "documentation"),
    "MEM-017": (dv("Planning","Budget & Resources"), PM, LOW, 2, "LOW", "documentation"),
    "MEM-036": (dv("Design UX/UI","Wireframes"), DL, LOW, 1, "LOW", "design"),
    "MEM-038": (dv("Design UX/UI","Design Handoff"), DL, LOW, 1, "LOW", "documentation"),
    "MEM-050": (dv("Development","S01: Schema + Seeds"), DB, LOW, 1, "LOW", "development"),
    "MEM-052": (dv("Development","S01: Schema + Seeds"), BE, LOW, 1, "LOW", "development"),
    "MEM-057": (dv("Development","S02: Import + Timeline"), BE, LOW, 1, "LOW", "development"),
    "MEM-067": (dv("Development","S04: Adapters + Cleanup"), BE, LOW, 1, "LOW", "development"),
    "MEM-074": (dv("Development","S05: Lista + Cost + Dashboard"), BE, LOW, 1, "LOW", "development"),
    "MEM-077": (dv("Development","S06: Docker + Integration"), DO, LOW, 1, "LOW", "deployment"),
    "MEM-082": (dv("Development","UI-01: Setup + Timeline + Viewer"), FE, LOW, 1, "LOW", "development"),
    "MEM-092": (dv("Development","UI-04: Cost Agente + Health"), FE, LOW, 2, "LOW", "development"),
    "MEM-110": (dv("Deploy","Rollback Plan"), TL, LOW, 2, "LOW", "documentation"),
    "MEM-112": (dv("Operations","User Support"), PM, LOW, 2, "LOW", "documentation"),
    "MEM-113": (dv("Operations","Bug Fixes Operations"), TL, LOW, 2, "LOW", "documentation"),
    "MEM-115": (dv("Operations","Security Updates"), AR, LOW, 2, "LOW", "documentation"),
}

r = urllib.request.urlopen(urllib.request.Request(
    BASE_URL + "/api/auth/service-token",
    data=json.dumps({"userId": PJM_ID, "serviceKey": SK}).encode(),
    headers={"Content-Type": "application/json"}, method="POST"))
token = json.loads(r.read())["data"]["token"]

def patch(task_id, body):
    req = urllib.request.Request(
        f"{BASE_URL}/api/tasks/{task_id}",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        method="PATCH")
    try:
        r = urllib.request.urlopen(req)
        raw = r.read()
        return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read())
        except: return e.code, {}

ok = fail = 0
for task_id, (delivery_id, assignee_id, priority_id, hours, complexity, category) in FAILED.items():
    s, d = patch(task_id, {"deliveryId": delivery_id, "assigneeId": assignee_id,
                            "priorityId": priority_id, "estimatedHours": hours,
                            "complexity": complexity, "category": category})
    if s in (200, 201):
        ok += 1
        print(f"  OK {task_id}")
    else:
        fail += 1
        print(f"  FAIL [{s}] {task_id}: {json.dumps(d)[:150]}")

print(f"\nDone: {ok} ok, {fail} fail")
