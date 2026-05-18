"""
PATCH todas las 116 tareas con deliveryId + assigneeId correctos.
"""
import urllib.request, urllib.error, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://77.42.88.106:3000"
PJM_ID   = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
SK       = "hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"

# Agents
PM  = "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"
PJM = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
TL  = "92225290-6b6b-4c1f-a940-dcb4262507aa"
BE  = "ebbe3cee-abed-4b3b-860d-0a81f632b08a"
DB  = "6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7"
FE  = "d23c9cd9-a156-433b-8900-94add5488eec"
QA  = "613c9538-658c-45fe-a6d7-c1ea9ff04b78"
DO  = "322e3745-9756-4a7c-af11-44b33edef44d"
DL  = "b3a09269-cded-468c-a475-15a48f203cb0"
UX  = "a75a1dae-754a-4b6f-a3ff-db8d51f6a91b"
SA  = "0c128e3b-db3b-4e31-b107-0379b5791233"
AR  = "e9403c25-c1f8-4b64-b2ef-f447d53115e2"

# Priorities
HIGH   = "1a617554-6319-4c56-826f-8ef49a0ff9cc"
MEDIUM = "d0b619ef-27e7-42d8-8879-41030a602eed"
LOW_P  = "95f2e731-1f30-429b-a8c9-c7d60adeaac3"

with open("c:/Users/Martin/Documents/virtual-teams/Project_setup/deprecated/scripts/mem_structure.json") as f:
    struct = json.load(f)
D = struct["deliverables"]

# Delivery UUID lookup by phase+name
def dv(phase, name):
    items = D[phase]
    for it in items:
        if it["name"] == name:
            return it["id"]
    raise ValueError(f"Delivery not found: {phase} / {name}")

# task_id -> (deliveryId, assigneeId, priorityId, estimatedHours, complexity, category)
TASKS = {
    # Project Setup
    "MEM-001": (dv("Project Setup","Project Foundation Ready"), DO, HIGH, 2, "MEDIUM", "deployment"),
    "MEM-002": (dv("Project Setup","Project Foundation Ready"), PJM, MEDIUM, 2, "LOW", "documentation"),
    "MEM-003": (dv("Project Setup","Project Foundation Ready"), PJM, LOW_P, 1, "LOW", "documentation"),
    "MEM-004": (dv("Project Setup","Project Foundation Ready"), DO, MEDIUM, 2, "MEDIUM", "deployment"),
    "MEM-005": (dv("Project Setup","Project Foundation Ready"), PM, MEDIUM, 4, "MEDIUM", "documentation"),

    # Discovery
    "MEM-006": (dv("Discovery","Problem Definition"), SA, MEDIUM, 3, "MEDIUM", "documentation"),
    "MEM-007": (dv("Discovery","Problem Definition"), PM, LOW_P, 2, "LOW", "review"),
    "MEM-008": (dv("Discovery","Value Proposition"), SA, MEDIUM, 3, "MEDIUM", "documentation"),
    "MEM-009": (dv("Discovery","Value Proposition"), PM, LOW_P, 1, "LOW", "review"),

    # Planning
    "MEM-010": (dv("Planning","Vision & Objectives"), PM, MEDIUM, 3, "MEDIUM", "documentation"),
    "MEM-011": (dv("Planning","Vision & Objectives"), PM, MEDIUM, 2, "MEDIUM", "documentation"),
    "MEM-012": (dv("Planning","Scope"), SA, HIGH, 4, "HIGH", "documentation"),
    "MEM-013": (dv("Planning","Stakeholders"), PJM, LOW_P, 2, "LOW", "documentation"),
    "MEM-014": (dv("Planning","Risks"), PJM, MEDIUM, 3, "MEDIUM", "documentation"),
    "MEM-015": (dv("Planning","Timeline"), PJM, HIGH, 4, "HIGH", "documentation"),
    "MEM-016": (dv("Planning","Timeline"), PJM, MEDIUM, 3, "MEDIUM", "documentation"),
    "MEM-017": (dv("Planning","Budget & Resources"), PM, LOW_P, 2, "LOW", "documentation"),

    # Analysis
    "MEM-018": (dv("Analysis","Functional Requirements"), SA, HIGH, 6, "HIGH", "documentation"),
    "MEM-019": (dv("Analysis","Non-Functional Requirements"), AR, HIGH, 4, "HIGH", "documentation"),
    "MEM-020": (dv("Analysis","Use Cases"), SA, MEDIUM, 5, "MEDIUM", "documentation"),
    "MEM-021": (dv("Analysis","User Stories"), SA, HIGH, 8, "HIGH", "documentation"),
    "MEM-022": (dv("Analysis","Business Rules"), TL, HIGH, 4, "HIGH", "documentation"),
    "MEM-023": (dv("Analysis","User Flows"), UX, MEDIUM, 4, "MEDIUM", "design"),
    "MEM-024": (dv("Analysis","Acceptance Criteria"), SA, HIGH, 6, "HIGH", "documentation"),
    "MEM-025": (dv("Analysis","Traceability Matrix"), SA, MEDIUM, 4, "MEDIUM", "documentation"),

    # Design UX/UI
    "MEM-026": (dv("Design UX/UI","Personas"), UX, MEDIUM, 3, "MEDIUM", "design"),
    "MEM-027": (dv("Design UX/UI","Information Architecture"), UX, MEDIUM, 4, "MEDIUM", "design"),
    "MEM-028": (dv("Design UX/UI","Design System"), DL, MEDIUM, 3, "MEDIUM", "design"),
    "MEM-029": (dv("Design UX/UI","Wireframes"), DL, HIGH, 4, "HIGH", "design"),
    "MEM-030": (dv("Design UX/UI","Wireframes"), DL, MEDIUM, 3, "MEDIUM", "design"),
    "MEM-031": (dv("Design UX/UI","Wireframes"), DL, HIGH, 4, "HIGH", "design"),
    "MEM-032": (dv("Design UX/UI","Mockups UI Design"), DL, HIGH, 4, "HIGH", "design"),
    "MEM-033": (dv("Design UX/UI","Wireframes"), DL, MEDIUM, 2, "MEDIUM", "design"),
    "MEM-034": (dv("Design UX/UI","Wireframes"), DL, MEDIUM, 2, "MEDIUM", "design"),
    "MEM-035": (dv("Design UX/UI","Wireframes"), DL, MEDIUM, 2, "MEDIUM", "design"),
    "MEM-036": (dv("Design UX/UI","Wireframes"), DL, LOW_P, 1, "LOW", "design"),
    "MEM-037": (dv("Design UX/UI","Design Handoff"), DL, MEDIUM, 2, "MEDIUM", "documentation"),
    "MEM-038": (dv("Design UX/UI","Design Handoff"), DL, LOW_P, 1, "LOW", "documentation"),

    # Design Technical
    "MEM-039": (dv("Design Technical","Solution Architecture"), TL, HIGH, 6, "HIGH", "documentation"),
    "MEM-040": (dv("Design Technical","Code Architecture"), TL, HIGH, 4, "HIGH", "documentation"),
    "MEM-041": (dv("Design Technical","Database Design"), DB, HIGH, 6, "HIGH", "documentation"),
    "MEM-042": (dv("Design Technical","API Design"), BE, HIGH, 8, "HIGH", "documentation"),
    "MEM-043": (dv("Design Technical","Sequence Diagrams"), AR, HIGH, 6, "HIGH", "documentation"),
    "MEM-044": (dv("Design Technical","Architecture Decision Records"), TL, MEDIUM, 4, "MEDIUM", "documentation"),
    "MEM-045": (dv("Design Technical","Security Plan"), AR, HIGH, 4, "HIGH", "documentation"),
    "MEM-046": (dv("Design Technical","Infrastructure Plan"), DO, MEDIUM, 4, "MEDIUM", "documentation"),
    "MEM-047": (dv("Design Technical","Technical Estimates"), TL, MEDIUM, 3, "MEDIUM", "documentation"),

    # Development - BE sprints
    "MEM-048": (dv("Development","S01: Schema + Seeds"), DB, HIGH, 3, "HIGH", "development"),
    "MEM-049": (dv("Development","S01: Schema + Seeds"), DB, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-050": (dv("Development","S01: Schema + Seeds"), DB, LOW_P, 1, "LOW", "development"),
    "MEM-051": (dv("Development","S01: Schema + Seeds"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-052": (dv("Development","S01: Schema + Seeds"), BE, LOW_P, 1, "LOW", "development"),

    "MEM-053": (dv("Development","S02: Import + Timeline"), BE, HIGH, 4, "HIGH", "development"),
    "MEM-054": (dv("Development","S02: Import + Timeline"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-055": (dv("Development","S02: Import + Timeline"), BE, HIGH, 3, "HIGH", "development"),
    "MEM-056": (dv("Development","S02: Import + Timeline"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-057": (dv("Development","S02: Import + Timeline"), BE, LOW_P, 1, "LOW", "development"),

    "MEM-058": (dv("Development","S03: Content + Context"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-059": (dv("Development","S03: Content + Context"), BE, HIGH, 4, "HIGH", "development"),
    "MEM-060": (dv("Development","S03: Content + Context"), BE, HIGH, 2, "HIGH", "development"),
    "MEM-061": (dv("Development","S03: Content + Context"), QA, MEDIUM, 2, "MEDIUM", "testing"),
    "MEM-062": (dv("Development","S03: Content + Context"), QA, MEDIUM, 2, "MEDIUM", "testing"),

    "MEM-063": (dv("Development","S04: Adapters + Cleanup"), BE, MEDIUM, 3, "MEDIUM", "development"),
    "MEM-064": (dv("Development","S04: Adapters + Cleanup"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-065": (dv("Development","S04: Adapters + Cleanup"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-066": (dv("Development","S04: Adapters + Cleanup"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-067": (dv("Development","S04: Adapters + Cleanup"), BE, LOW_P, 1, "LOW", "development"),
    "MEM-068": (dv("Development","S04: Adapters + Cleanup"), BE, MEDIUM, 2, "MEDIUM", "testing"),

    "MEM-069": (dv("Development","S05: Lista + Cost + Dashboard"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-070": (dv("Development","S05: Lista + Cost + Dashboard"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-071": (dv("Development","S05: Lista + Cost + Dashboard"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-072": (dv("Development","S05: Lista + Cost + Dashboard"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-073": (dv("Development","S05: Lista + Cost + Dashboard"), BE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-074": (dv("Development","S05: Lista + Cost + Dashboard"), BE, LOW_P, 1, "LOW", "development"),

    "MEM-075": (dv("Development","S06: Docker + Integration"), DO, MEDIUM, 2, "MEDIUM", "deployment"),
    "MEM-076": (dv("Development","S06: Docker + Integration"), DO, MEDIUM, 2, "MEDIUM", "deployment"),
    "MEM-077": (dv("Development","S06: Docker + Integration"), DO, LOW_P, 1, "LOW", "deployment"),
    "MEM-078": (dv("Development","S06: Docker + Integration"), BE, HIGH, 4, "HIGH", "development"),
    "MEM-079": (dv("Development","S06: Docker + Integration"), QA, HIGH, 3, "HIGH", "testing"),
    "MEM-080": (dv("Development","S06: Docker + Integration"), QA, MEDIUM, 2, "MEDIUM", "testing"),

    # Development - DL control (hitos - sin tareas reales, pero hay que asignar a la delivery DL)
    # Estas son las tareas flotantes que mapean a los hitos DL
    # En realidad las tareas DL son las MEM-028..038 en Design UX/UI
    # Los hitos DL-01..04 son deliveries de CONTROL sin tareas propias

    # Development - FE
    "MEM-081": (dv("Development","UI-01: Setup + Timeline + Viewer"), FE, MEDIUM, 2, "MEDIUM", "development"),
    "MEM-082": (dv("Development","UI-01: Setup + Timeline + Viewer"), FE, LOW_P, 1, "LOW", "development"),
    "MEM-083": (dv("Development","UI-01: Setup + Timeline + Viewer"), FE, HIGH, 5, "HIGH", "development"),
    "MEM-084": (dv("Development","UI-01: Setup + Timeline + Viewer"), FE, HIGH, 6, "HIGH", "development"),
    "MEM-085": (dv("Development","UI-01: Setup + Timeline + Viewer"), FE, MEDIUM, 2, "MEDIUM", "development"),

    "MEM-086": (dv("Development","UI-02: Dashboard + Cost + Import"), FE, HIGH, 4, "HIGH", "development"),
    "MEM-087": (dv("Development","UI-02: Dashboard + Cost + Import"), FE, MEDIUM, 4, "MEDIUM", "development"),
    "MEM-088": (dv("Development","UI-02: Dashboard + Cost + Import"), FE, MEDIUM, 4, "MEDIUM", "development"),

    "MEM-089": (dv("Development","UI-03: Viewer REVIEW + Lista"), FE, HIGH, 5, "HIGH", "development"),
    "MEM-090": (dv("Development","UI-03: Viewer REVIEW + Lista"), FE, HIGH, 5, "HIGH", "development"),

    "MEM-091": (dv("Development","UI-04: Cost Agente + Health"), FE, MEDIUM, 3, "MEDIUM", "development"),
    "MEM-092": (dv("Development","UI-04: Cost Agente + Health"), FE, LOW_P, 2, "LOW", "development"),
    "MEM-093": (dv("Development","UI-04: Cost Agente + Health"), FE, MEDIUM, 3, "MEDIUM", "development"),

    # Testing
    "MEM-094": (dv("Testing","Test Planning"), QA, MEDIUM, 4, "MEDIUM", "documentation"),
    "MEM-095": (dv("Testing","Test Cases"), QA, HIGH, 8, "HIGH", "testing"),
    "MEM-096": (dv("Testing","Test Environment"), DO, MEDIUM, 4, "MEDIUM", "deployment"),
    "MEM-097": (dv("Testing","Functional Testing"), QA, HIGH, 8, "HIGH", "testing"),
    "MEM-098": (dv("Testing","Integration Testing"), QA, HIGH, 6, "HIGH", "testing"),
    "MEM-099": (dv("Testing","E2E Testing"), QA, HIGH, 8, "HIGH", "testing"),
    "MEM-100": (dv("Testing","Performance Testing"), QA, HIGH, 6, "HIGH", "testing"),
    "MEM-101": (dv("Testing","Security Testing"), AR, HIGH, 4, "HIGH", "testing"),
    "MEM-102": (dv("Testing","UAT"), PM, MEDIUM, 4, "MEDIUM", "review"),
    "MEM-103": (dv("Testing","Bug Fixes"), BE, HIGH, 8, "HIGH", "bugfix"),

    # Deploy
    "MEM-104": (dv("Deploy","Infrastructure Setup"), DO, HIGH, 4, "HIGH", "deployment"),
    "MEM-105": (dv("Deploy","CI/CD Configuration"), DO, HIGH, 6, "HIGH", "deployment"),
    "MEM-106": (dv("Deploy","Staging Deploy"), DO, MEDIUM, 4, "MEDIUM", "deployment"),
    "MEM-107": (dv("Deploy","Smoke Testing"), QA, MEDIUM, 3, "MEDIUM", "testing"),
    "MEM-108": (dv("Deploy","Production Deploy"), DO, HIGH, 4, "HIGH", "deployment"),
    "MEM-109": (dv("Deploy","Post-Deploy Monitoring"), DO, MEDIUM, 3, "MEDIUM", "review"),
    "MEM-110": (dv("Deploy","Rollback Plan"), TL, LOW_P, 2, "LOW", "documentation"),

    # Operations
    "MEM-111": (dv("Operations","Monitoring"), DO, MEDIUM, 3, "MEDIUM", "review"),
    "MEM-112": (dv("Operations","User Support"), PM, LOW_P, 2, "LOW", "documentation"),
    "MEM-113": (dv("Operations","Bug Fixes Operations"), TL, LOW_P, 2, "LOW", "documentation"),
    "MEM-114": (dv("Operations","Incremental Improvements"), PM, MEDIUM, 3, "MEDIUM", "documentation"),
    "MEM-115": (dv("Operations","Security Updates"), AR, LOW_P, 2, "LOW", "documentation"),
    "MEM-116": (dv("Operations","Scaling"), AR, MEDIUM, 3, "MEDIUM", "documentation"),
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
        except: return e.code, {"error": str(e)}

print(f"Patching {len(TASKS)} tasks...")
ok = 0
fail = 0
for task_id, (delivery_id, assignee_id, priority_id, hours, complexity, category) in TASKS.items():
    body = {
        "deliveryId": delivery_id,
        "assigneeId": assignee_id,
        "priorityId": priority_id,
        "estimatedHours": hours,
        "complexity": complexity,
        "category": category,
    }
    s, d = patch(task_id, body)
    if s in (200, 201):
        ok += 1
        print(f"  OK [{s}] {task_id}")
    else:
        fail += 1
        print(f"  FAIL [{s}] {task_id}: {json.dumps(d)[:150]}")

print(f"\nDone: {ok} ok, {fail} fail")
