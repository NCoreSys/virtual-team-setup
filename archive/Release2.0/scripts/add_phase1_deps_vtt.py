#!/usr/bin/env python3
"""
Memory Service R1 — Add Intra-Phase Dependencies (Phase 1 Project Setup)
========================================================================
Agrega las dependencias intra-fase entre las 26 tareas INIT-A..G
segun el HO_INICIACION §5 ORDEN DE EJECUCION.

Resultado: el Gantt muestra las tareas en orden correcto en vez de
todas al dia 1.

NO toca estados de tareas. NO asigna. Solo POST deps.
"""

import os, sys, json, time, urllib.request, urllib.error

API_URL     = os.environ.get("VTT_API_URL", "http://77.42.88.106:3000")
SERVICE_KEY = os.environ.get("VTT_SERVICE_KEY")
if not SERVICE_KEY:
    sys.exit("ERROR: Define VTT_SERVICE_KEY antes de ejecutar.")

PJM_UUID   = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
UUIDS_FILE = "VTT_UUIDS_PHASE1_RESTRUCTURED.json"

# ── Dependencias intra-fase (tarea_que_depende, depende_de, razon) ───────────
# Basado en HO_INICIACION_MEMORY_SERVICE.md §5 ORDEN DE EJECUCION
DEPS = [
    # ── A. VTT Setup ─────────────────────────────────────────────────────────
    # A-01, A-02, A-03 arrancan en paralelo (sin deps - verificaciones independientes)
    ("INIT-A-04", "INIT-A-01", "A: PATCH 116 tareas tras verificar proyecto"),
    ("INIT-A-04", "INIT-A-02", "A: PATCH 116 tareas tras verificar fases"),
    ("INIT-A-04", "INIT-A-03", "A: PATCH 116 tareas tras verificar deliveries"),
    ("INIT-A-05", "INIT-A-04", "A: Dependencias tras PATCH metadata completo"),

    # ── B. Repository Setup ──────────────────────────────────────────────────
    # B-01 arranca (bloqueado por multi-repo PM)
    ("INIT-B-02", "INIT-B-01", "B: Estructura V3.1 requiere repo Git creado"),
    ("INIT-B-03", "INIT-B-02", "B: Archivos base tras estructura inicializada"),
    ("INIT-B-04", "INIT-B-01", "B: Branch protection requiere repo creado"),
    ("INIT-B-05", "INIT-B-03", "B: Git conventions tras CONTRIBUTING creado"),

    # ── C. VM Configuration ──────────────────────────────────────────────────
    # C-01 arranca (verificacion inicial)
    ("INIT-C-02", "INIT-C-01", "C: Tests conectividad tras infra verificada"),
    ("INIT-C-03", "INIT-C-01", "C: Distribuir SERVICE_KEY tras infra OK"),
    ("INIT-C-04", "INIT-C-02", "C: Docs VM tras tests ejecutados"),
    ("INIT-C-04", "INIT-C-03", "C: Docs VM tras SERVICE_KEY distribuida"),

    # ── D. Agent Team Setup ──────────────────────────────────────────────────
    # D-02 arranca (consolidar memoria - independiente)
    ("INIT-D-01", "INIT-A-04", "D: OPERATIVOs tras validar equipo en VTT"),
    ("INIT-D-03", "INIT-D-01", "D: CONTEXTOs por rol tras OPERATIVOs"),
    ("INIT-D-04", "INIT-D-01", "D: Distribuir accesos tras roles definidos"),
    ("INIT-D-04", "INIT-B-01", "D: Distribuir accesos requiere repo existente"),
    ("INIT-D-05", "INIT-D-01", "D: Onboarding tras roles definidos"),
    ("INIT-D-05", "INIT-D-04", "D: Onboarding tras accesos distribuidos"),

    # ── E. Tooling Setup ─────────────────────────────────────────────────────
    ("INIT-E-01", "INIT-B-02", "E: Base Node requiere estructura repo"),
    ("INIT-E-02", "INIT-E-01", "E: Linters sobre base Node"),
    ("INIT-E-03", "INIT-E-02", "E: CI tras linters funcionando"),

    # ── F. Documentation ─────────────────────────────────────────────────────
    ("INIT-F-01", "INIT-B-02", "F: README requiere estructura repo"),
    ("INIT-F-02", "INIT-F-01", "F: ARCHITECTURE despues de README"),
    ("INIT-F-02", "INIT-E-01", "F: ARCHITECTURE despues de base tecnica"),

    # ── G. Kickoff (gate de la fase) ─────────────────────────────────────────
    ("INIT-G-01", "INIT-A-05", "G: Doc kickoff tras dependencias VTT listas"),
    ("INIT-G-01", "INIT-D-05", "G: Doc kickoff tras onboarding completo"),
    ("INIT-G-01", "INIT-E-03", "G: Doc kickoff tras CI funcionando"),
    ("INIT-G-01", "INIT-F-02", "G: Doc kickoff tras docs base completas"),
    ("INIT-G-02", "INIT-G-01", "G: Kickoff call tras doc kickoff listo (GATE fase)"),
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


def post_dep(task_uuid, dep_uuid, token):
    req = urllib.request.Request(
        f"{API_URL}/api/tasks/{task_uuid}/dependencies",
        data=json.dumps({"dependsOnTaskId": dep_uuid}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="ignore")
        return None, f"{e.code} - {detail[:200]}"


def main():
    log("=" * 70)
    log("Memory Service R1 - Add Phase 1 Intra-Phase Dependencies")
    log("=" * 70)
    log(f"API: {API_URL}")
    log(f"Deps a agregar: {len(DEPS)}")
    log("")

    if not os.path.exists(UUIDS_FILE):
        sys.exit(f"ERROR: falta {UUIDS_FILE}.")

    with open(UUIDS_FILE, encoding="utf-8") as f:
        uuids = json.load(f)

    token = auth_token()
    log("Token JWT obtenido OK\n")

    ok, errors = 0, 0
    for (task_code, dep_code, razon) in DEPS:
        task_info = uuids["tasks"].get(task_code)
        dep_info  = uuids["tasks"].get(dep_code)

        if not task_info or not dep_info:
            log(f"  ERROR: UUID no encontrado para {task_code} o {dep_code}")
            errors += 1
            continue

        resp, err = post_dep(task_info["uuid"], dep_info["uuid"], token)
        if err:
            log(f"  WARN {task_code} <- {dep_code}: {err}")
            errors += 1
        else:
            ok += 1
            log(f"  OK   {task_code} <- {dep_code}  ({razon})")

    log("")
    log("=" * 70)
    log("RESUMEN")
    log("=" * 70)
    log(f"Deps OK:     {ok} / {len(DEPS)}")
    log(f"Errores:     {errors}")
    log("=" * 70)

    if ok == len(DEPS):
        log("")
        log("Todas las dependencias intra-fase registradas.")
        log("Recargar el Gantt en VTT para verificar la nueva secuencia.")


if __name__ == "__main__":
    main()
