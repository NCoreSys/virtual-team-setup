# VTT.SKILL-HARDCODE-001 — Ejecutar Hardcode Check (secretos)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-HARDCODE-001` |
| **Categoría** | HARDCODE (Security check) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor — verificación obligatoria ANTES de commit + in_review |
| **Tokens estimados** | ~140 |
| **Cuándo se usa** | `WORKFLOW-ASG-001.019` / `CARD-EXE-007` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `worktree_path` | path | sí | |
| `scan_dirs` | array | opcional | default `src/` |
| `exclude` | array | opcional | default `.git,node_modules,dist,build` |

## Precondición

- Working tree con cambios aplicados

## Variables del entorno

- `$VTT_SETUP`

## Reglas

- R1 9 patrones canónicos: passwords/api_keys/tokens/service_keys/JWT/DB/AWS/GCP
- R2 0 findings críticos/altos en producción (`src/`)
- R3 FPs DEBEN justificarse en devlog `decision`
- R4 Sin check → bloquea Review Gate
- R5 Finding REAL → mover a env var
- R6 Tests con secretos fake → fixtures o env vars de test

## Ejecución

```bash
$VTT_SETUP/02.normativa/04.Scripts/hardcode/SCRIPT-HARDCODE-001_check.sh \
  --root "$WORKTREE_PATH" \
  --scan-dirs "src/" \
  --exclude ".git,node_modules,dist,build" \
  --output "$WORKTREE_PATH/.vtt/hardcode-check.json"

# Después de clasificar FPs:
$VTT_SETUP/02.normativa/04.Scripts/hardcode/SCRIPT-HARDCODE-002_validate_fp.py \
  --check-output "$WORKTREE_PATH/.vtt/hardcode-check.json" \
  --fps-justified "$WORKTREE_PATH/.vtt/hardcode-fps.json"
```

## Validación

`status == PASS` + `real_findings_in_production_count == 0`

## Error común

- Findings REALES > 0 → mover a env var
- FP recurrente grep auto-referencial → `.hardcode-ignore`
- Re-check sigue findings → guardar archivos + re-ejecutar

## Scripts invocados

- `SCRIPT-HARDCODE-001_check.sh`
- `SCRIPT-HARDCODE-002_validate_fp.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. 9 patrones + clasificación + FPs. |
