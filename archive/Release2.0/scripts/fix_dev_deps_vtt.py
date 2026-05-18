#!/usr/bin/env python3
"""
Memory Service R1 — Fix Development Sprint Dependencies
========================================================
Agrega dependencias intra-sprint faltantes en la fase Development (S01..S06 y UI-02..04).

Problema: solo los "inter-sprint gates" estaban seteados (criticos 15 deps).
Las tareas DENTRO de cada sprint flotaban desde el dia 1 sin predecesor.

Ejemplo: MEM-051 (Express Setup) no tenia dependencia -> aparecia el dia 1 en el Gantt
aunque deberia esperar a que Design Technical (MEM-047) este completo.

Solucion: agregar cadena de dependencias dentro de S01..S06 y UI-02..04.
"""

import os, sys, json, time, urllib.request, urllib.error

API_URL     = os.environ.get("VTT_API_URL", "http://77.42.88.106:3000")
SERVICE_KEY = os.environ.get("VTT_SERVICE_KEY")
if not SERVICE_KEY:
    sys.exit("ERROR: Define VTT_SERVICE_KEY antes de ejecutar.")

PJM_UUID   = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
UUIDS_FILE = "VTT_UUIDS_MEMORY_SERVICE.json"

# ─────────────────────────────────────────────────────────────────────────────
# Dependencias intra-sprint faltantes
# Formato: (task_que_depende, depende_de, razon)
# ─────────────────────────────────────────────────────────────────────────────
NEW_DEPS = [
    # ── S01: Schema + Seeds (MEM-048..052) ──────────────────────────────────
    # MEM-048 ya tiene dep critica: MEM-048 -> MEM-047
    ("MEM-049", "MEM-048", "S01: Migrations after Schema Prisma"),
    ("MEM-050", "MEM-049", "S01: Seed after Migrations applied"),
    ("MEM-051", "MEM-048", "S01: Express setup needs schema ready"),
    ("MEM-052", "MEM-051", "S01: Catalog cache after Express setup"),
    ("MEM-052", "MEM-050", "S01: Catalog cache needs seeds to preload"),

    # ── S02: Import + Timeline (MEM-053..057) ───────────────────────────────
    # MEM-053 ya tiene dep critica: MEM-053 -> MEM-052
    ("MEM-054", "MEM-053", "S02: import-review after base import endpoint"),
    ("MEM-055", "MEM-053", "S02: upload endpoint after basic import"),
    ("MEM-056", "MEM-053", "S02: timeline needs import data to exist"),
    ("MEM-057", "MEM-056", "S02: error handler after timeline (final cleanup S02)"),

    # ── S03: Content + Context (MEM-058..062) ───────────────────────────────
    # MEM-058 ya tiene dep critica: MEM-058 -> MEM-057
    ("MEM-059", "MEM-058", "S03: GET /context after GET /content (same data layer)"),
    ("MEM-060", "MEM-058", "S03: classifier after content parsing available"),
    ("MEM-061", "MEM-059", "S03: performance tests after /context implemented"),
    ("MEM-062", "MEM-060", "S03: classifier tests after classifier implemented"),

    # ── S04: Adapters + Cleanup (MEM-063..068) ──────────────────────────────
    # MEM-063 ya tiene dep critica: MEM-063 -> MEM-062
    ("MEM-064", "MEM-063", "S04: CHATGPT adapter after CLAUDE_WEB adapter"),
    ("MEM-065", "MEM-063", "S04: storage writer after first adapter"),
    ("MEM-066", "MEM-065", "S04: cleanup cron needs storage writer"),
    ("MEM-067", "MEM-066", "S04: status transitions helper after cleanup"),
    ("MEM-068", "MEM-067", "S04: adapter tests after all adapters+helpers done"),

    # ── S05: Lista + Cost + Dashboard (MEM-069..074) ────────────────────────
    # MEM-069 ya tiene dep critica: MEM-069 -> MEM-068
    ("MEM-070", "MEM-069", "S05: cost-report after conversations endpoint"),
    ("MEM-071", "MEM-069", "S05: agent cost-report after conversations"),
    ("MEM-072", "MEM-069", "S05: dashboard stats after conversations data"),
    ("MEM-073", "MEM-069", "S05: health endpoint after main endpoints done"),
    ("MEM-074", "MEM-073", "S05: integration tests after all S05 endpoints"),

    # ── S06: Docker + Integration (MEM-075..080) ────────────────────────────
    # MEM-075 ya tiene dep critica: MEM-075 -> MEM-074
    ("MEM-076", "MEM-075", "S06: CI config after Dockerfile"),
    ("MEM-077", "MEM-075", "S06: env vars setup after Dockerfile base"),
    ("MEM-078", "MEM-077", "S06: Hook Manager integration after env vars"),
    ("MEM-079", "MEM-078", "S06: E2E Runtime test after integration code"),
    ("MEM-080", "MEM-078", "S06: E2E Prompt Builder test after integration"),

    # ── UI-02: Dashboard + Cost + Import (MEM-086..088) ─────────────────────
    # MEM-086 ya tiene dep critica: MEM-086 -> MEM-085
    ("MEM-087", "MEM-086", "UI-02: Cost Proyecto after Dashboard"),
    ("MEM-088", "MEM-086", "UI-02: Import Manual after Dashboard base"),

    # ── UI-03: Viewer REVIEW + Lista (MEM-089..090) ──────────────────────────
    # MEM-089 ya tiene dep critica: MEM-089 -> MEM-088
    ("MEM-090", "MEM-089", "UI-03: AGENT_REVIEW viewer after Lista convs"),

    # ── UI-04: Cost Agente + Health (MEM-091..093) ───────────────────────────
    # MEM-091 ya tiene dep critica: MEM-091 -> MEM-090
    ("MEM-092", "MEM-091", "UI-04: Health page after Cost Agente"),
    ("MEM-093", "MEM-092", "UI-04: Polish after all pages done"),
]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def auth_token():
    req = urllib.request.Request(
        f"{API_URL}/api/auth/service-token",
        data=json.dumps({"userId": PJM_UUID, "serviceKey": SERVICE_KEY}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())["data"]["token"]


def post_dep(task_id, dep_id, token):
    req = urllib.request.Request(
        f"{API_URL}/api/tasks/{task_id}/dependencies",
        data=json.dumps({"dependsOnTaskId": dep_id}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="ignore")
        return None, f"{e.code} — {detail[:120]}"


def main():
    log("Memory Service R1 — Fix Development Sprint Dependencies")
    log(f"API: {API_URL}")
    log(f"Deps a agregar: {len(NEW_DEPS)}")

    with open(UUIDS_FILE, encoding="utf-8") as f:
        uuids = json.load(f)

    log("Token JWT obteniendo...")
    token = auth_token()
    log("Token OK\n")

    ok = 0
    errors = 0

    for (task_code, dep_code, razon) in NEW_DEPS:
        task_id = uuids["tasks"].get(task_code)
        dep_id  = uuids["tasks"].get(dep_code)

        if not task_id or not dep_id:
            log(f"  ERROR: UUID no encontrado para {task_code} o {dep_code}")
            errors += 1
            continue

        resp, err = post_dep(task_id, dep_id, token)
        if err:
            log(f"  WARN {task_code} -> {dep_code}: {err}")
            errors += 1
        else:
            log(f"  OK {task_code} -> {dep_code}  ({razon})")
            ok += 1

    log(f"\n{'='*50}")
    log(f"Resultado: {ok} OK / {errors} errores")
    log(f"{'='*50}")

    if errors:
        log("WARN: Algunos deps no se pudieron crear. Revisar manualmente.")
    else:
        log("Todas las dependencias de sprints agregadas exitosamente.")
        log("Recargar el Gantt en VTT para verificar la nueva secuencia.")


if __name__ == "__main__":
    main()
