#!/usr/bin/env bash
# VTT.SCRIPT-HARDCODE-001 — Hardcode Check (secretos en código)
#
# Propósito: detectar 9 patrones canónicos de secretos hardcodeados.
# Idempotente: Sí (puede correr varias veces, output es determinístico).
#
# Aplicado por: SKILL-HARDCODE-001
# Pertenece a: PROTOCOL-ASG-001 §5.3.7 (WORKFLOW-ASG-001.019 / CARD-EXE-007)
# RULE-SCRIPT-001: solo invocable desde $VTT_SETUP/02.normativa/04.Scripts/hardcode/
#
# Inputs (CLI):
#   --root         path raíz del worktree
#   --scan-dirs    dirs a escanear (default: "src/")
#   --exclude      patrones excluidos (default: ".git,node_modules,dist,build")
#   --output       (opcional) escribir JSON resultado a archivo
#
# Outputs:
#   stdout JSON con {success, total_findings, findings: [...]}
#   exit 0 si 0 findings, 1 si hay findings (clasificación humana posterior)

set -uo pipefail

# enforce_canonical_path
SCRIPT_PATH="$(realpath "$0" 2>/dev/null || readlink -f "$0" 2>/dev/null || echo "$0")"
EXPECTED_SUFFIX="02.normativa/04.Scripts/hardcode"
if [[ "$SCRIPT_PATH" != *"$EXPECTED_SUFFIX"* ]]; then
  echo '{"success":false,"error":"RULE-SCRIPT-001 violation","script_path":"'"$SCRIPT_PATH"'"}'
  exit 5
fi

# Args
ROOT=""
SCAN_DIRS="src/"
EXCLUDE=".git,node_modules,dist,build,.next,coverage"
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --scan-dirs) SCAN_DIRS="$2"; shift 2 ;;
    --exclude) EXCLUDE="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) echo "Argumento desconocido: $1"; exit 1 ;;
  esac
done

if [[ -z "$ROOT" ]]; then
  echo '{"success":false,"error":"--root requerido"}'
  exit 1
fi

cd "$ROOT" || { echo '{"success":false,"error":"No se pudo cd a root"}'; exit 1; }

# 9 patrones canónicos
PATTERNS=(
  'password\s*[:=]\s*["'\''][^"'\'']{8,}["'\'']'
  'api[_-]?key\s*[:=]\s*["'\''][A-Za-z0-9]{20,}["'\'']'
  'token\s*[:=]\s*["'\''][A-Za-z0-9_-]{20,}["'\'']'
  'service[_-]?key\s*[:=]\s*["'\''][A-Za-z0-9]{20,}["'\'']'
  'jwt[_-]?secret\s*[:=]\s*["'\''][^"'\'']{16,}["'\'']'
  'postgres(ql)?://[^:]+:[^@]+@'
  'mongodb(\+srv)?://[^:]+:[^@]+@'
  '(AKIA|ASIA)[A-Z0-9]{16}'
  'AIza[0-9A-Za-z_-]{35}'
)

EXCLUDE_FLAGS=""
IFS=',' read -ra EXCLUDE_ARR <<< "$EXCLUDE"
for d in "${EXCLUDE_ARR[@]}"; do
  EXCLUDE_FLAGS="$EXCLUDE_FLAGS --exclude-dir=$d"
done

FINDINGS_JSON="[]"
TOTAL=0

for pattern in "${PATTERNS[@]}"; do
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    FILE=$(echo "$line" | cut -d: -f1)
    LINENO=$(echo "$line" | cut -d: -f2)
    MATCH=$(echo "$line" | cut -d: -f3- | sed 's/"/\\"/g')

    FINDINGS_JSON=$(python3 -c "
import sys, json
existing = json.loads(sys.argv[1])
new = {'pattern': sys.argv[2], 'file': sys.argv[3], 'line': int(sys.argv[4]), 'match': sys.argv[5][:200]}
existing.append(new)
print(json.dumps(existing))
" "$FINDINGS_JSON" "$pattern" "$FILE" "$LINENO" "$MATCH")
    TOTAL=$((TOTAL + 1))
  done < <(grep -rnE "$pattern" $SCAN_DIRS $EXCLUDE_FLAGS 2>/dev/null || true)
done

# Output JSON
RESULT=$(python3 -c "
import json, sys
findings = json.loads(sys.argv[1])
result = {
    'success': True,
    'scan_root': sys.argv[2],
    'scan_dirs': sys.argv[3].split(','),
    'total_findings': len(findings),
    'findings': findings,
}
print(json.dumps(result, indent=2))
" "$FINDINGS_JSON" "$ROOT" "$SCAN_DIRS")

if [[ -n "$OUTPUT" ]]; then
  mkdir -p "$(dirname "$OUTPUT")"
  echo "$RESULT" > "$OUTPUT"
fi

echo "$RESULT"

# Exit 0 si 0 findings, 1 si hay findings (clasificación humana posterior)
if [[ "$TOTAL" -eq 0 ]]; then
  exit 0
else
  exit 1
fi
