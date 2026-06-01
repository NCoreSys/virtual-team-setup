# VTT.WORKFLOW-ASG-001.019 — Ejecutar Hardcode Check

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.019` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.7 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor — ANTES del commit + in_review |
| **Reglas Nivel 0** | `RULE-SEC-001`, `RULE-SCRIPT-001`, `RULE-DATA-001` |
| **CARD asociada** | `VTT.CARD-EXE-007` |

---

## 1. Propósito

Verificar que el código NO contiene **secretos hardcodeados** (passwords, API keys, tokens, service keys, JWT, DB strings, AWS/GCP/Azure keys). Sin este check, tarea NO puede pasar a `task_in_review`.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `worktree_path` | path | |
| `scan_dirs` | array | default: `src/` |
| `exclude_patterns` | array | default: `.git,node_modules,dist,build` |

## 3. Precondiciones

- Implementación completada (paso 5 del `.034`)
- Working tree con cambios aplicados

## 4. Reglas

| # | Regla |
|---|---|
| R1 | 9 patrones canónicos (passwords, api keys, tokens, service keys, JWT, DB, AWS, GCP) |
| R2 | 0 findings críticos/altos en producción (`src/`) |
| R3 | FPs DEBEN justificarse en devlog `decision` (patrón + por qué FP + path:line) |
| R4 | FP recurrente: grep auto-referenciales en docs (documentar aunque conocido) |
| R5 | Sin check ejecutado → bloquea Review Gate |
| R6 | Finding REAL → corregir a env var antes de in_review |
| R7 | Tests con secretos fake → mover a fixtures o env vars de test |

## 5. Pasos

### Paso 1 — Ejecutar script canónico
```bash
$VTT_SETUP/02.normativa/04.Scripts/hardcode/SCRIPT-HARDCODE-001_check.sh \
  --root "$WORKTREE_PATH" \
  --scan-dirs "src/" \
  --exclude ".git,node_modules,dist,build" \
  --output "$WORKTREE_PATH/.vtt/hardcode-check.json"
```

### Paso 2 — Analizar resultados (JSON)
```json
{
  "total_findings": 5,
  "findings": [
    {"pattern":"password","file":"src/config/db.ts","line":23,"match":"...","severity_estimated":"critical"},
    {"pattern":"token","file":"docs/SETUP.md","line":142,"match":"grep -rn 'token' src/","severity_estimated":"low"}
  ]
}
```

### Paso 3 — Clasificar cada finding

Pregunta 1: ¿secreto real? → sí: REAL crítico/alto / no: FP severity low.
Pregunta 2 (si REAL): ¿en producción (`src/`)? → sí: bloquea gate / no (tests/fixtures): mover a env var.

### Paso 4 — Corregir findings REALES
1. `.env.example` con placeholder
2. Código lee de `process.env.VAR`
3. Re-ejecutar check

### Paso 5 — Justificar FPs en devlog
Por cada FP, devlog `decision` con title `Hardcode Check FP: <path:line>` + description con patrón + justificación.

### Paso 6 — Re-verificar status final
```bash
SCRIPT-HARDCODE-002_validate_fp.py --check-output ... --fps-justified ...
```

Esperado: 0 críticos/altos en producción + FPs justificados con devlog IDs + Status PASS.

### Paso 7 — Reportar en SKL-REPORT-01

## 6. Outputs

| Output | Descripción |
|---|---|
| `total_findings` | int |
| `real_findings_count` | int |
| `real_findings_in_production_count` | int (debe = 0) |
| `false_positives_count` | int |
| `false_positives_justified` | array devlog IDs |
| `check_status` | `PASS` / `FAIL` |

## 7. Validación

`check_status == "PASS"` con `real_findings_in_production_count == 0`

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Script no encontrado | Path canónico mal | Usar `$VTT_SETUP/02.normativa/04.Scripts/hardcode/` |
| Findings REALES > 0 producción | Secretos hardcoded | Mover a env var |
| Re-check sigue findings | Archivos no guardados | Guardar + re-ejecutar |
| FP grep auto-referencial | grep en doc matchea su patrón | Documentar + agregar a `.hardcode-ignore` |

## 9. Skills invocadas

- `SKILL-HARDCODE-001`, `SKILL-DEV-001`

## 10. Scripts invocados

- `SCRIPT-HARDCODE-001_check.sh`
- `SCRIPT-HARDCODE-002_validate_fp.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. 9 patrones canónicos + clasificación + FPs justificados. |
