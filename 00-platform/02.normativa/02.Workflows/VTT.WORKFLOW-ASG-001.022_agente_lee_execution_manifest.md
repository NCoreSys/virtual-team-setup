# VTT.WORKFLOW-ASG-001.022 — Agente lee execution_manifest.json

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.022` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.2.b |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor antes de tocar código |
| **Reglas Nivel 0** | `RULE-AGENT-001`, `RULE-MAN-001` |
| **Workflow padre del manifest** | `WORKFLOW-MAN-001.002` (este es alias contextualizado en ASG) |
| **CARD asociada** | `VTT.CARD-MAN-004` |

---

## 1. Propósito

El agente lee su `execution_manifest.json` para conocer `allowedPaths`, `deniedPaths`, `expectedOutputs`, `branchExpected` ANTES de tocar código. Sin esta lectura → toca archivos fuera de scope → bloquea Review Gate.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `agent_id` | UUID | |
| `execution_manifest_path` | path | `.vtt/manifests/<TASK_ID>.execution.json` |

## 3. Precondiciones

- TL generó el execution_manifest (paso 5.2.11 del protocol) usando `WORKFLOW-MAN-001.001`
- Manifest existe en path canónico

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Manifest debe existir antes de tocar código |
| R2 | Si `agentId` no aparece en manifest → escalar TL inmediato |
| R3 | Tocar archivo fuera de `allowedPaths` → escalar TL (NO mockear) |
| R4 | Branch debe coincidir con `branchExpected` (`feature/<TASK_ID>`) |

## 5. Pasos

### Paso 1 — Verificar manifest existe
```bash
MANIFEST_PATH=".vtt/manifests/<TASK_ID>.execution.json"
[ -f "$MANIFEST_PATH" ] || { echo "Escalar al TL"; exit 1; }
```

### Paso 2 — Leer manifest
```bash
cat "$MANIFEST_PATH" | python -m json.tool
```

### Paso 3 — Extraer datos para SU agentId
```bash
AGENT_ALLOWED_PATHS=$(python -c "import json; m=json.load(open('$MANIFEST_PATH')); print(json.dumps(m['agents']['$AGENT_UUID']['allowedPaths']))")
AGENT_DENIED_PATHS=$(python -c "...")
EXPECTED_OUTPUTS=$(python -c "...")
COMMIT_PATTERN=$(python -c "...")
BRANCH_EXPECTED=$(python -c "...")
```

Si `agents.$AGENT_UUID` no existe → STOP, escalar al TL.

### Paso 4 — Validar restricciones
- `allowedPaths`: lista de paths que PUEDE tocar
- `deniedPaths`: lista que NO debe tocar
- `expectedOutputs`: archivos esperados al final
- `branchExpected`: nombre del feature branch
- `rules.commitPattern`: formato de commits

### Paso 5 — Internalizar
El agente debe recordar estas restricciones durante toda la implementación (`.034` paso 5).

## 6. Outputs

| Output | Descripción |
|---|---|
| `allowed_paths` | array de paths |
| `denied_paths` | array |
| `expected_outputs` | array |
| `branch_expected` | string |
| `commit_pattern` | string |
| `manifest_validated` | true |

## 7. Validación

`agentId` aparece en manifest + `allowedPaths` no vacío + `branchExpected` consistente con `feature/<TASK_ID>`.

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Manifest no existe | TL no generó | Escalar al TL (`SCRIPT-MAN-001`) |
| agentId no en manifest | TL olvidó incluir | Escalar al TL |
| Path en allowed/denied incoherente | Manifest mal generado | Escalar al TL |

## 9. Skills invocadas

- `SKILL-EXM-001` (Execution Manifest)

## 10. Scripts invocados

- `SCRIPT-EXM-001_read_execution_manifest.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Formaliza PROTOCOL-ASG-001 §5.3.2.b como alias contextualizado de WORKFLOW-MAN-001.002. |
