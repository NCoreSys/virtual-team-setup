#!/usr/bin/env python3
"""
TEMPLATE_SCRIPT — Molde para crear un Script nuevo (Nivel 1)

Cómo usar:
    1. Copia este archivo a `02.normativa/04.Scripts/<categoria>/` con nombre
       `VTT.SCRIPT-<CAT>-<NNN>_<titulo_snake>.py`.
    2. Reemplaza los placeholders `<...>` en el header y código.
    3. Borra este bloque de instrucciones antes de publicar.

Antes de empezar:
    Verifica que es realmente un Script (Nivel 1 — comando atómico ejecutable).
    Si tiene decisiones de negocio o orquesta varios scripts → es una Skill (Nivel 2).
    Si es solo 1 línea de curl → considera incluirlo inline en la Skill que lo invoca.

Requisitos obligatorios:
    1. Header docstring con: propósito, idempotencia, inputs, outputs, exit codes
    2. Stdout en JSON (para que las skills puedan parsear el resultado)
    3. Exit codes claros: 0 OK, 1 args, 2 precondición, 3 HTTP error
    4. Sin secrets hardcoded — usar env vars
    5. Idempotencia documentada: Sí / No / Parcial + por qué

Referencias:
    - 02.normativa/README.md §3 — Tabla decisoria (Script vs Skill)
    - 02.normativa/README.md §8 — Estructura obligatoria del Script
    - 02.normativa/GUIA_AUTOR.md — Anti-patterns
    - Ejemplos reales: 02.normativa/04.Scripts/ (cuando existan)
"""

# =============================================================================
# VTT.SCRIPT-<CAT>-<NNN> — <Título descriptivo>
# =============================================================================
#
# Propósito: <una línea — qué hace el script>
#
# Idempotente: <Sí | No | Parcial>
#   <Sí — explicar por qué (ej. "GET de solo lectura — no modifica estado")>
#   <No — explicar por qué (ej. "POST que siempre crea un recurso nuevo")>
#   <Parcial — explicar (ej. "Crea si no existe, update si existe")>
#
# Inputs:
#   --param1   <descripción + tipo + ejemplo>
#   --param2   <descripción + tipo + ejemplo>
#   $TOKEN     JWT VTT (env var) — REQUERIDO
#   $VTT_BASE_URL  Base URL VTT (env var, default http://77.42.88.106:3000)
#
# Outputs (stdout JSON):
#   Éxito: {"success": true, "data": {...}, "http_status": 201}
#   Error: {"success": false, "error": "...", "http_status": <code>}
#
# Exit codes:
#   0 — OK (operación exitosa)
#   1 — Argumentos inválidos (faltantes o formato incorrecto)
#   2 — Precondición no cumplida (TOKEN faltante, recurso inexistente, etc.)
#   3 — HTTP error (4xx / 5xx del backend VTT)
#
# Uso:
#   python VTT.SCRIPT-<CAT>-<NNN>.py --param1=<valor> --param2=<valor>
# =============================================================================

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def main():
    # -------------------------------------------------------------------------
    # 1. Parser de argumentos
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="<Descripción del script (1 línea)>"
    )
    parser.add_argument(
        "--param1",
        required=True,
        help="<descripción del param1>"
    )
    parser.add_argument(
        "--param2",
        required=False,
        default=None,
        help="<descripción del param2 (opcional)>"
    )
    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # 2. Validación de precondiciones (env vars + args)
    # -------------------------------------------------------------------------
    token = os.environ.get("TOKEN")
    if not token:
        print(json.dumps({
            "success": False,
            "error": "TOKEN env var requerido"
        }))
        sys.exit(2)

    base_url = os.environ.get("VTT_BASE_URL", "http://77.42.88.106:3000")

    # Validaciones adicionales del input (si aplica)
    # if not _valid_uuid(args.param1):
    #     print(json.dumps({"success": False, "error": "param1 no es UUID válido"}))
    #     sys.exit(1)

    # -------------------------------------------------------------------------
    # 3. Ejecución (HTTP call al backend VTT)
    # -------------------------------------------------------------------------
    payload = {
        "<field_1>": args.param1,
        # "<field_2>": args.param2,
    }

    req = urllib.request.Request(
        f"{base_url}/api/<endpoint>",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"  # GET / POST / PATCH / DELETE según corresponda
    )

    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            data = json.loads(response_body).get("data") if response_body else None

            print(json.dumps({
                "success": True,
                "http_status": response.status,
                "data": data
            }))
            sys.exit(0)

    except urllib.error.HTTPError as e:
        # 4xx / 5xx — error controlado
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(json.dumps({
            "success": False,
            "http_status": e.code,
            "error": body
        }))
        sys.exit(3)

    except urllib.error.URLError as e:
        # Conexión rota, DNS, etc.
        print(json.dumps({
            "success": False,
            "error": f"Connection error: {e.reason}"
        }))
        sys.exit(3)

    except Exception as e:
        # Otros errores inesperados
        print(json.dumps({
            "success": False,
            "error": f"Unexpected error: {type(e).__name__}: {e}"
        }))
        sys.exit(3)


if __name__ == "__main__":
    # Encoding UTF-8 para Windows
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
