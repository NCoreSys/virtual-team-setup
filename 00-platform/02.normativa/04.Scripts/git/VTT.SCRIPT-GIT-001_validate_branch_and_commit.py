#!/usr/bin/env python3
# =============================================================================
# VTT.SCRIPT-GIT-001 — Validar nombre de branch y formato de commit message
# =============================================================================
#
# Propósito: validar que el branch actual y/o el mensaje de commit cumplen
#            el patrón de gobernanza configurado para el repo. Diseñado para
#            ejecutarse desde hooks de git (pre-commit, pre-push, commit-msg)
#            o invocarse on-demand por agentes y CI.
#
# Idempotente: Sí — operación de solo lectura sobre el estado de git.
#              No modifica el repo. Ejecutable N veces sin side effects.
#
# Inputs:
#   --mode               Modo de validación. Uno de:
#                          branch        valida solo el branch actual
#                          commit        valida solo el mensaje del commit
#                          both          valida ambos (default)
#                          commit-msg    valida un archivo de commit msg
#                                        (uso desde hook commit-msg de git)
#   --commit-msg-file    (modo commit-msg) Path al archivo con el mensaje.
#                        Git lo pasa como argv[1] al hook commit-msg.
#   --config             Path al JSON con la configuración de gobernanza.
#                        Default: .git/hooks/vtt_governance.json en repo root.
#   --repo-path          Path al repo (default: cwd).
#   --quiet              Suprime stdout JSON. Solo retorna exit code.
#
# Configuración esperada (vtt_governance.json):
#   {
#     "branch_pattern_regex": "^agent/(tl|pm|...)/[a-z0-9-]{3,30}/[a-z0-9-]{3,50}$",
#     "header_regex": "^\\[agente:[a-z]+\\] \\[proyecto:[a-z0-9-]+\\] \\[scope:[^]]+\\] \\[type:(editorial|functional|structural|breaking)\\]",
#     "required_trailers": ["Motivo:", "Origen:", "Consumidores:"],
#     "block_branches": ["main"]
#   }
#
# Outputs (stdout JSON):
#   Éxito (todas las validaciones OK):
#     {"success": true, "checks": [{"name": "...", "passed": true}, ...]}
#   Fallo (≥1 validación falla):
#     {"success": false, "failed_checks": [{"name": "...", "reason": "..."}],
#      "all_checks": [...]}
#
# Exit codes:
#   0 — OK (todas las validaciones aplicables pasaron)
#   1 — Argumentos inválidos (modo desconocido, falta --commit-msg-file, etc.)
#   2 — Precondición no cumplida (config no existe, no estás en repo git, etc.)
#   3 — Validación falló (branch o commit no cumplen gobernanza)
#
# Uso desde CLI:
#   python VTT.SCRIPT-GIT-001_validate_branch_and_commit.py --mode=both
#
# Uso desde hook .git/hooks/pre-commit:
#   #!/bin/sh
#   python <repo>/00-platform/02.normativa/04.Scripts/git/VTT.SCRIPT-GIT-001_*.py \
#     --mode=branch || exit 1
#
# Uso desde hook .git/hooks/commit-msg (git lo invoca con el archivo de msg):
#   #!/bin/sh
#   python <repo>/00-platform/02.normativa/04.Scripts/git/VTT.SCRIPT-GIT-001_*.py \
#     --mode=commit-msg --commit-msg-file="$1" || exit 1
# =============================================================================

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_CONFIG_RELATIVE = ".git/hooks/vtt_governance.json"


def emit_result(payload: dict, quiet: bool) -> None:
    if not quiet:
        print(json.dumps(payload, ensure_ascii=False))


def fail_arg(msg: str, quiet: bool) -> int:
    emit_result({"success": False, "error": msg, "exit_reason": "args"}, quiet)
    return 1


def fail_precondition(msg: str, quiet: bool) -> int:
    emit_result({"success": False, "error": msg, "exit_reason": "precondition"}, quiet)
    return 2


def fail_validation(failed: list, all_checks: list, quiet: bool) -> int:
    emit_result(
        {
            "success": False,
            "failed_checks": failed,
            "all_checks": all_checks,
        },
        quiet,
    )
    return 3


def ok(all_checks: list, quiet: bool) -> int:
    emit_result({"success": True, "checks": all_checks}, quiet)
    return 0


def load_config(repo_path: Path, config_arg: str | None) -> tuple[dict | None, str]:
    config_path = (
        Path(config_arg) if config_arg else repo_path / DEFAULT_CONFIG_RELATIVE
    )
    if not config_path.exists():
        return None, f"config not found: {config_path}"
    try:
        return json.loads(config_path.read_text(encoding="utf-8")), str(config_path)
    except json.JSONDecodeError as exc:
        return None, f"config not valid JSON ({config_path}): {exc}"


def is_git_repo(repo_path: Path) -> bool:
    return (repo_path / ".git").exists()


def get_current_branch(repo_path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def validate_branch(branch: str, config: dict) -> tuple[bool, str]:
    pattern = config.get("branch_pattern_regex")
    if not pattern:
        return False, "config.branch_pattern_regex no definido"
    if not re.search(pattern, branch):
        return False, f"branch '{branch}' no cumple branch_pattern_regex"
    return True, "branch cumple el patrón"


def validate_block_branches(branch: str, config: dict) -> tuple[bool, str]:
    blocked = config.get("block_branches", ["main"])
    if branch in blocked:
        return False, f"commit a '{branch}' bloqueado por gobernanza (block_branches={blocked})"
    return True, f"branch '{branch}' no está en block_branches"


def validate_commit_header(msg: str, config: dict) -> tuple[bool, str]:
    pattern = config.get("header_regex")
    if not pattern:
        return False, "config.header_regex no definido"
    first_line = msg.splitlines()[0] if msg else ""
    if not re.search(pattern, first_line):
        return False, f"línea 1 no cumple header_regex: '{first_line[:80]}'"
    return True, "header cumple el patrón"


def validate_commit_trailers(msg: str, config: dict) -> tuple[bool, str]:
    trailers = config.get("required_trailers", [])
    missing = [t for t in trailers if t not in msg]
    if missing:
        return False, f"faltan trailers obligatorios: {missing}"
    return True, f"todos los trailers presentes ({len(trailers)})"


def get_last_commit_message(repo_path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "log", "-1", "--format=%B"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def run(args: argparse.Namespace) -> int:
    repo_path = Path(args.repo_path).resolve()

    if not is_git_repo(repo_path):
        return fail_precondition(f"no es repo git: {repo_path}", args.quiet)

    config, config_info = load_config(repo_path, args.config)
    if config is None:
        return fail_precondition(config_info, args.quiet)

    checks: list[dict] = []
    failed: list[dict] = []

    def record(name: str, passed: bool, detail: str) -> None:
        entry = {"name": name, "passed": passed, "detail": detail}
        checks.append(entry)
        if not passed:
            failed.append({"name": name, "reason": detail})

    # ---- Branch checks ----
    if args.mode in ("branch", "both", "commit-msg"):
        branch = get_current_branch(repo_path)
        if branch is None:
            return fail_precondition("no se pudo obtener branch actual", args.quiet)

        # block_branches aplica siempre (incluso en commit-msg)
        passed, detail = validate_block_branches(branch, config)
        record("block_branches", passed, detail)

        # branch_pattern_regex aplica en branch/both. En commit-msg es opcional
        # (algunos repos permiten hooks de commit-msg en branches sin nombre estricto).
        if args.mode in ("branch", "both"):
            passed, detail = validate_branch(branch, config)
            record("branch_pattern_regex", passed, detail)

    # ---- Commit message checks ----
    if args.mode == "commit-msg":
        if not args.commit_msg_file:
            return fail_arg("--commit-msg-file requerido en modo commit-msg", args.quiet)
        msg_file = Path(args.commit_msg_file)
        if not msg_file.exists():
            return fail_precondition(f"commit-msg file no existe: {msg_file}", args.quiet)
        msg = msg_file.read_text(encoding="utf-8")
        passed, detail = validate_commit_header(msg, config)
        record("commit_header_regex", passed, detail)
        passed, detail = validate_commit_trailers(msg, config)
        record("commit_required_trailers", passed, detail)

    elif args.mode in ("commit", "both"):
        msg = get_last_commit_message(repo_path)
        if msg is None:
            return fail_precondition(
                "no se pudo obtener mensaje del último commit (¿repo sin commits?)",
                args.quiet,
            )
        passed, detail = validate_commit_header(msg, config)
        record("commit_header_regex", passed, detail)
        passed, detail = validate_commit_trailers(msg, config)
        record("commit_required_trailers", passed, detail)

    if failed:
        return fail_validation(failed, checks, args.quiet)
    return ok(checks, args.quiet)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida branch y commit contra gobernanza VTT"
    )
    parser.add_argument(
        "--mode",
        choices=["branch", "commit", "both", "commit-msg"],
        default="both",
        help="Qué validar (default: both)",
    )
    parser.add_argument(
        "--commit-msg-file",
        help="Path al archivo de mensaje (modo commit-msg)",
    )
    parser.add_argument(
        "--config",
        help=f"Path al JSON de gobernanza (default: <repo>/{DEFAULT_CONFIG_RELATIVE})",
    )
    parser.add_argument(
        "--repo-path",
        default=os.getcwd(),
        help="Path al repo (default: cwd)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="No emitir stdout JSON, solo exit code",
    )
    return parser.parse_args()


if __name__ == "__main__":
    try:
        sys.exit(run(parse_args()))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001
        # Cualquier excepción no esperada se reporta como precondición no cumplida
        print(
            json.dumps(
                {
                    "success": False,
                    "error": f"unexpected: {type(exc).__name__}: {exc}",
                    "exit_reason": "precondition",
                },
                ensure_ascii=False,
            )
        )
        sys.exit(2)
