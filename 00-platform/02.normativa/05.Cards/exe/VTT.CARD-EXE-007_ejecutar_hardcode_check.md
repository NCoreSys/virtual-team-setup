# VTT.CARD-EXE-007 — Ejecutar Hardcode Check

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-007` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-EXE-006` |
| **Pertenece a** | WORKFLOW-ASG-001.019 |
| **Tokens estimados** | ~1,000 |

---

## Qué hacer

Antes del commit final, verificar que NO hay secretos hardcodeados (`RULE-SEC-001`):

```bash
$VTT_SETUP/02.normativa/04.Scripts/hardcode/SCRIPT-HARDCODE-001_check.sh \
  --root "$WORKTREE_PATH" \
  --scan-dirs "src/" \
  --exclude ".git,node_modules,dist,build" \
  --output "$WORKTREE_PATH/.vtt/hardcode-check.json"
```

## 9 patrones canónicos detectados

- `password\s*[:=]\s*["\x27][^"\x27]{8,}["\x27]`
- `api[_-]?key\s*[:=]\s*["\x27][A-Za-z0-9]{20,}["\x27]`
- `token\s*[:=]\s*["\x27][A-Za-z0-9_-]{20,}["\x27]`
- `service[_-]?key\s*[:=]\s*["\x27][A-Za-z0-9]{20,}["\x27]`
- `jwt[_-]?secret\s*[:=]\s*["\x27][^"\x27]{16,}["\x27]`
- DB strings (`postgresql://...`, `mongodb://...`)
- AWS keys (`AKIA...`, `ASIA...`)
- GCP API keys (`AIza...`)

## Por cada finding — clasificar

**Pregunta 1: ¿es secreto real?**
- SÍ → finding REAL → severity `critical`/`high`
- NO → False Positive (FP) → severity `low`

**Pregunta 2 (si REAL): ¿en `src/` producción?**
- SÍ → **bloquea Review Gate** — corregir antes de continuar
- NO (tests/fixtures) → severity `medium` + mover a env var

## Corregir findings REALES

1. Crear/actualizar `.env.example` con placeholder:
   ```bash
   DB_PASSWORD=<your_db_password>
   ```
2. Modificar código: leer de env var:
   ```typescript
   const password = process.env.DB_PASSWORD;
   if (!password) throw new Error('DB_PASSWORD env var required');
   ```
3. Re-ejecutar check para confirmar 0 findings críticos/altos

## Justificar False Positives en devlog

Por CADA FP, registrar devlog `decision`:

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/devlog-entries" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{"entries":[{
    "categoryCode":"decision",
    "severity":"low",
    "title":"Hardcode Check FP: <path:line>",
    "description":"Match del patrón <X> en <path:line>.\nContenido: <fragment>\nClasificado FP porque <justificación>: ejemplo en doc / regex / fixture test.\nNo requiere corrección.",
    "reportedBy":"<AGENT_UUID>"
  }]}'
```

Capturar el `devlog_entry_id` para SKL-REPORT-01.

## FP recurrente conocido

Comandos `grep` dentro de docs matchean su propio patrón (gotcha). Documentar como FP aunque sea conocido. Si recurrente → agregar archivo a `.hardcode-ignore`.

## Bloqueo

**Sin check ejecutado → bloquea Review Gate.**
**0 findings críticos/altos en producción = PASS.**

## Si falla

| Síntoma | Acción |
|---|---|
| Script no encontrado | Usar path canónico `$VTT_SETUP/02.normativa/04.Scripts/hardcode/` |
| Findings REALES en producción | Mover a env var antes de continuar |
| Re-check sigue con findings | Guardar archivos modificados + re-ejecutar |

## Output

Status PASS + lista de FPs justificados (con devlog IDs) + lista de correcciones aplicadas. Pasa a commit final (Paso 11 de CARD-EXE-004).
