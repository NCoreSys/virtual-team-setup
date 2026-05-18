"""
Probar PATCH en phaseTask record con deliveryId.
"""
import urllib.request, urllib.error, json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://77.42.88.106:3000"
PJM_ID   = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
SK       = "hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"

with open("c:/Users/Martin/Documents/virtual-teams/Project_setup/deprecated/scripts/mem_structure.json") as f:
    struct = json.load(f)
PROJECT_ID = struct["projectId"]
SETUP_ID = struct["phases"]["Project Setup"]["id"]
FOUNDATION_DELIVERY_ID = struct["deliverables"]["Project Setup"][0]["id"]

r = urllib.request.urlopen(urllib.request.Request(
    BASE_URL + "/api/auth/service-token",
    data=json.dumps({"userId": PJM_ID, "serviceKey": SK}).encode(),
    headers={"Content-Type": "application/json"}, method="POST"))
token = json.loads(r.read())["data"]["token"]

def call(method, path, body=None):
    req = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        method=method)
    try:
        r = urllib.request.urlopen(req)
        raw = r.read()
        return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read())
        except: return e.code, {}

# Get phaseTasks for Project Setup
s, d = call("GET", f"/api/projects/{PROJECT_ID}")
phases = d.get("data", {}).get("phases", [])
setup = next((p for p in phases if p.get("name") == "Project Setup"), None)
phase_tasks = setup.get("phaseTasks", [])
print(f"Project Setup phaseTasks: {len(phase_tasks)}")
for pt in phase_tasks:
    print(f"  phaseTask id={pt['id']} taskId={pt['taskId']}")

# Try PATCH on phaseTask with deliveryId
if phase_tasks:
    pt = phase_tasks[0]
    pt_id = pt["id"]
    print(f"\nTrying PATCH phaseTask {pt_id} with deliveryId={FOUNDATION_DELIVERY_ID}")

    for ep in [
        f"/api/phase-tasks/{pt_id}",
        f"/api/phasetasks/{pt_id}",
        f"/api/phases/{SETUP_ID}/tasks/{pt['taskId']}",
        f"/api/phases/{SETUP_ID}/phase-tasks/{pt_id}",
    ]:
        s, d = call("PATCH", ep, {"deliveryId": FOUNDATION_DELIVERY_ID})
        print(f"  [{s}] PATCH {ep}")
        if s in (200, 201):
            print(f"    WORKS: {json.dumps(d.get('data', d))[:200]}")

    # Also try DELETE + recreate via delivery
    print(f"\nTrying POST task directly in delivery")
    for ep in [
        f"/api/deliveries/{FOUNDATION_DELIVERY_ID}/tasks/{pt['taskId']}",
        f"/api/phases/{SETUP_ID}/deliveries/{FOUNDATION_DELIVERY_ID}/tasks",
    ]:
        if "tasks/" in ep:
            s, d = call("POST", ep, {})
        else:
            s, d = call("POST", ep, {"taskId": pt["taskId"]})
        print(f"  [{s}] POST {ep}")
        if s in (200, 201):
            print(f"    WORKS: {json.dumps(d.get('data', d))[:200]}")

    # Try linking via PUT
    print(f"\nTrying PUT task to delivery")
    for ep in [
        f"/api/deliveries/{FOUNDATION_DELIVERY_ID}/tasks",
        f"/api/phases/{SETUP_ID}/deliveries/{FOUNDATION_DELIVERY_ID}/tasks",
    ]:
        s, d = call("PUT", ep, {"taskIds": [pt["taskId"]]})
        print(f"  [{s}] PUT {ep}")
        if s in (200, 201):
            print(f"    WORKS: {json.dumps(d.get('data', d))[:200]}")
