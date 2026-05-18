#!/usr/bin/env python3
"""
<<PROYECTO>> — VTT Creation Script — TEMPLATE
==============================================
Crea en VTT desde cero:
  - 1 Project
  - N Phases
  - N Deliveries
  - N Tasks (con metadata completa)
  - N Dependencies criticas

Salida:
  VTT_UUIDS_<<PROYECTO>>.json con todos los UUIDs capturados.

Uso:
  export VTT_SERVICE_KEY=...
  python3 create_<<proyecto>>_vtt.py

Requiere Python 3.8+.

INSTRUCCIONES PARA USAR ESTE TEMPLATE:
  1. Copiar a `scripts/create_<<proyecto>>_vtt.py`
  2. Reemplazar `<<PROYECTO>>` con nombre real
  3. Completar UUIDs reales en seccion "UUIDs DE USUARIOS"
  4. Llenar PROJECT, PHASES, DELIVERIES, TASKS, DEPENDENCIES
  5. Validar sintaxis: python3 -c "import py_compile; py_compile.compile('create_<<proyecto>>_vtt.py')"
  6. Ejecutar segun HO_PJM_CARGA_VTT_<<PROYECTO>>.md
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from typing import Any

# ============================================================================
# CONFIG
# ============================================================================

API_URL = os.environ.get("VTT_API_URL", "http://77.42.88.106:3000")
SERVICE_KEY = os.environ.get("VTT_SERVICE_KEY")

if not SERVICE_KEY:
    sys.exit("ERROR: Define VTT_SERVICE_KEY en el entorno antes de ejecutar.")

OUTPUT_FILE = "VTT_UUIDS_<<PROYECTO>>.json"

# ============================================================================
# UUIDs DE USUARIOS
# ============================================================================
# REEMPLAZAR con UUIDs reales del proyecto (de .claude/rules/Proyect_data.md)

PM_UUID  = "<<UUID_PM>>"
PJM_UUID = "<<UUID_PJM>>"
TL_UUID  = "<<UUID_TL>>"

USERS = {
    "PM":  PM_UUID,
    "PJM": PJM_UUID,
    "TL":  TL_UUID,
    "SA":  "<<UUID_SA>>",
    "AR":  "<<UUID_AR>>",
    "BE":  "<<UUID_BE>>",
    "DB":  "<<UUID_DB>>",
    "FE":  "<<UUID_FE>>",
    "UX":  "<<UUID_UX>>",
    "DL":  "<<UUID_DL>>",
    "QA":  "<<UUID_QA>>",
    "DO":  "<<UUID_DO>>",
}

# ============================================================================
# UUIDs DE CATALOGOS GLOBALES (estandar VTT — no cambiar)
# ============================================================================

STATUS_PENDING = "335fd9c6-f0d6-4966-a6ea-f518c78bc422"

PRIORITY = {
    "C": "90ec3df2-fac4-40fa-b2ce-29daf0f4956e",  # critical
    "H": "1a617554-6319-4c56-826f-8ef49a0ff9cc",  # high
    "M": "d0b619ef-27e7-42d8-8879-41030a602eed",  # medium
    "L": "95f2e731-41b9-4a7d-9a43-31f00a4ddd7e",  # low
}

# ============================================================================
# PROJECT
# ============================================================================

PROJECT = {
    "name": "<<NOMBRE_PROYECTO>>",
    "code": "<<CODIGO_3_LETRAS>>",
    "description": "<<descripcion 500-2000 chars del proyecto>>",
    "projectTypeCode": "SOFTWARE",
}

# ============================================================================
# PHASES
# ============================================================================
# (name, order, description)
PHASES = [
    ("<<Fase 1>>", 1, "<<descripcion>>"),
    ("<<Fase 2>>", 2, "<<descripcion>>"),
    # ... agregar todas las fases
]

# ============================================================================
# DELIVERIES
# ============================================================================
# (phase_name, delivery_name, order, description)
DELIVERIES = [
    # Fase 1
    ("<<Fase 1>>", "<<Delivery 1>>", 1, "<<descripcion>>"),
    # Fase 2
    ("<<Fase 2>>", "<<Delivery 1>>", 1, "<<descripcion>>"),
    # ... agregar todos los deliveries
]

# ============================================================================
# TASKS
# ============================================================================
# (code, phase_name, delivery_name, title, description, role, category, complexity, hours, priority)
#
# IMPORTANTE (lessons VTT-506):
# - role: debe existir en USERS dict
# - category: development|design|testing|documentation|deployment|chore|bugfix|review
# - complexity: MAYUSCULAS "LOW"|"MEDIUM"|"HIGH"
# - hours: integer
# - priority: "C"|"H"|"M"|"L" (ref a PRIORITY dict)
# - description: max 2000 chars

TASKS = [
    # Ejemplo:
    # ("MEM-001", "Project Setup", "Project Foundation Ready", "Infra Setup",
    #  "Descripcion detallada de 150-2000 chars...",
    #  "DO", "chore", "MEDIUM", 4, "M"),

    # ... agregar todas las tareas
]

# ============================================================================
# DEPENDENCIES (criticas)
# ============================================================================
# (task_code, depends_on_code, razon)
DEPENDENCIES = [
    # Ejemplo:
    # ("MEM-006", "MEM-005", "Discovery despues de Kickoff"),

    # ... agregar dependencias criticas
]

# ============================================================================
# HELPERS
# ============================================================================

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def auth_token(user_id: str) -> str:
    """Obtiene JWT de servicio para un user_id."""
    req = urllib.request.Request(
        f"{API_URL}/api/auth/service-token",
        data=json.dumps({"userId": user_id, "serviceKey": SERVICE_KEY}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())["data"]["token"]
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR auth: {e.code} {e.reason} — {e.read().decode(errors='ignore')}")


def post(path: str, body: dict[str, Any], token: str) -> dict[str, Any]:
    """POST con Authorization Bearer."""
    req = urllib.request.Request(
        f"{API_URL}{path}",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="ignore")
        log(f"ERROR POST {path}: {e.code} {e.reason} — {detail}")
        raise


def extract_id(response: dict[str, Any]) -> str:
    """Extrae id/UUID del payload."""
    if isinstance(response.get("data"), dict) and "id" in response["data"]:
        return response["data"]["id"]
    if "id" in response:
        return response["id"]
    raise ValueError(f"No se encontro id en respuesta: {response}")


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    log(f"<<PROYECTO>> — VTT Creation Script")
    log(f"API: {API_URL}")
    log(f"Ejecutado por PJM: {PJM_UUID}")

    # Auth como PJM
    token = auth_token(PJM_UUID)
    log("✓ Token JWT obtenido")

    uuids: dict[str, Any] = {
        "projectId": None,
        "phases": {},
        "deliveries": {},
        "tasks": {},
    }

    # ─── Paso 1: Create Project ──────────────────────────────────────────
    log("\n=== Paso 1: Crear Project ===")
    project_body = dict(PROJECT, createdBy=PM_UUID)
    project = post("/api/projects", project_body, token)
    uuids["projectId"] = extract_id(project)
    log(f"✓ Project creado: {uuids['projectId']} — '{PROJECT['name']}'")

    # ─── Paso 2: Create Phases ───────────────────────────────────────────
    log(f"\n=== Paso 2: Crear {len(PHASES)} Phases ===")
    for name, order, desc in PHASES:
        body = {
            "name": name,
            "order": order,
            "description": desc,
            "createdBy": PM_UUID,
        }
        p = post(f"/api/projects/{uuids['projectId']}/phases", body, token)
        uuids["phases"][name] = extract_id(p)
        log(f"  ✓ Phase {order:2d}. {name}: {uuids['phases'][name]}")

    # ─── Paso 3: Create Deliveries ───────────────────────────────────────
    log(f"\n=== Paso 3: Crear {len(DELIVERIES)} Deliveries ===")
    for phase_name, deliv_name, order, desc in DELIVERIES:
        body = {
            "phaseId": uuids["phases"][phase_name],
            "name": deliv_name,
            "order": order,
            "description": desc,
            "createdBy": PJM_UUID,
        }
        d = post("/api/deliveries", body, token)
        uuids["deliveries"][deliv_name] = extract_id(d)
        log(f"  ✓ [{phase_name}] {deliv_name}: {uuids['deliveries'][deliv_name]}")

    # ─── Paso 4: Create Tasks ────────────────────────────────────────────
    log(f"\n=== Paso 4: Crear {len(TASKS)} Tasks ===")
    for (code, phase_name, deliv_name, title, desc, role, cat, cmplx, hours, pri) in TASKS:
        assignee = USERS[role]
        body = {
            "title": title,
            "description": desc,
            "priorityId": PRIORITY[pri],
            "statusId": STATUS_PENDING,
            "assignedToId": assignee,
            "assignedBy": PJM_UUID,
            "category": cat,
            "complexity": cmplx,
            "estimatedHours": hours,
            "createdBy": PJM_UUID,
        }
        t = post(f"/api/phases/{uuids['phases'][phase_name]}/tasks", body, token)
        task_id = extract_id(t)
        uuids["tasks"][code] = task_id
        log(f"  ✓ {code} [{role} {hours}h {cmplx}] {title} -> {task_id}")

        # Paso 5 (inline): Asignar task al delivery
        deliv_id = uuids["deliveries"][deliv_name]
        try:
            post(
                f"/api/deliveries/{deliv_id}/tasks/{task_id}",
                {"assignedBy": PJM_UUID},
                token,
            )
        except urllib.error.HTTPError as e:
            log(f"    ⚠ No se pudo asignar a delivery '{deliv_name}': {e.code}")

    # ─── Paso 6: Create Dependencies ─────────────────────────────────────
    log(f"\n=== Paso 6: Crear {len(DEPENDENCIES)} Dependencies criticas ===")
    for (task_code, dep_code, razon) in DEPENDENCIES:
        task_id = uuids["tasks"][task_code]
        dep_id = uuids["tasks"][dep_code]
        try:
            post(
                f"/api/tasks/{task_id}/dependencies",
                {"dependsOnTaskId": dep_id},
                token,
            )
            log(f"  ✓ {task_code} depende de {dep_code} ({razon})")
        except urllib.error.HTTPError as e:
            log(f"  ⚠ Dependencia {task_code} -> {dep_code} falló: {e.code} — registrar manualmente")

    # ─── Guardar UUIDs ───────────────────────────────────────────────────
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(uuids, f, indent=2)
    log(f"\n✅ Completado. UUIDs guardados en {OUTPUT_FILE}")
    log(f"   Project:    1 creado")
    log(f"   Phases:     {len(uuids['phases'])} creadas")
    log(f"   Deliveries: {len(uuids['deliveries'])} creados")
    log(f"   Tasks:      {len(uuids['tasks'])} creadas")
    log(f"   Deps:       {len(DEPENDENCIES)} procesadas")


if __name__ == "__main__":
    main()

# ============================================================================
# TEMPLATE SOURCE
# ============================================================================
# Template source: TEMPLATE_create_vtt_script_V1.0.py
# Proceso asociado: 09_PROCESO_CIERRE_PM_HANDOFF_PJM.md (paso 8)
# ============================================================================
