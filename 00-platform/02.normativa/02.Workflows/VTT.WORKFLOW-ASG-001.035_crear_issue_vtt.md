# VTT.WORKFLOW-ASG-001.035 — Agente crea Issue en VTT

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.035` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.4.1 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor cuando detecta bloqueante |
| **Reglas Nivel 0** | `RULE-DATA-001`, `RULE-SCRIPT-001` |
| **CARD asociada** | `VTT.CARD-ISS-001` |

---

## 1. Propósito

Crear Issue formal en VTT cuando el agente detecta un bloqueante. Gate anti-mockeo (`RULE-DATA-001`) y anti-improvisación (lección MS-328).

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | tarea origen (parent) |
| `agent_id` | UUID | |
| `issue_type` | enum | `dato_faltante`/`requirement`/`dependency`/`tech_error`/`scope_unclear`/`infra_failure` |
| `severity` | enum | `critical`/`high`/`medium`/`low` |
| `title` | string | max 200 chars |
| `description` | text | 4 secciones obligatorias |
| `category` | string | sub-categoría |

## 3. Precondiciones

- Tarea en `task_in_progress`
- Bloqueante REAL (no duda resoluble por consulta)
- Agente intentó ≥1 resolución antes

## 4. Reglas

| # | Regla |
|---|---|
| R1 | PROHIBIDO mockear datos (`RULE-DATA-001`) |
| R2 | PROHIBIDO improvisar ante conflicto TI ↔ ASSIGNMENT (MS-328) |
| R3 | Title `[<TASK_ID>] [<SPRINT>] <síntoma>` + marker `[TASK:<TASK_ID>]` en description |
| R4 | Description estructurada 4 secciones: Síntoma / Intentado / Solicitud / Impacto |
| R5 | Severity según impacto al sprint, NO severidad técnica |
| R6 | Crear Issue ANTES de pedir on_hold (`issueId` se pasa al `.036`) |
| R7 | Registrar devlog `blocker` enlazado en paralelo |

## 5. Pasos

### Paso 1 — Validar precondiciones
Tarea en `task_in_progress`.

### Paso 2 — Estructurar description (R4)
```markdown
## Síntoma
<qué pasa concretamente>

## Intentado
- <resolución 1>: resultado
- <resolución 2>: resultado

## Solicitud
<qué necesitás del TL/PM, específico>

## Impacto si no se resuelve
- Tarea bloqueada
- Downstream: <tareas afectadas>
```

### Paso 3 — Crear Issue
```bash
python $VTT_SETUP/02.normativa/04.Scripts/issue/SCRIPT-ISSUE-001_create_issue.py \
  --task-id "$TASK_ID" \
  --type "$ISSUE_TYPE" \
  --severity "$SEVERITY" \
  --title "$TITLE" \
  --description "$DESCRIPTION" \
  --project-id "$PROJECT_ID" \
  --sprint "$SPRINT" \
  --reported-by "$AGENT_UUID"
```

Script agrega automáticamente marker textual + devlog blocker enlazado.

### Paso 4 — Validar
```bash
curl -s "$VTT_BASE_URL/api/issues/<issueId>" | python -m json.tool
```

Esperado: `status=open`, `sourceTaskId=<TASK_ID>`, `reportedBy=<AGENT_UUID>`.

### Paso 5 — Pasar al `.036`
`issueId` se usa como `onHoldIssueId` en `WORKFLOW-ASG-001.036`.

## 6. Outputs

| Output | Descripción |
|---|---|
| `issue_id` | UUID |
| `status` | `open` |
| `devlog_entry_id_blocker` | UUID |

## 7. Validación

Issue creado + devlog blocker enlazado + marker textual presente.

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| HTTP 400 invalid issueType | Fuera enum | Usar enum cerrado |
| Sin marker en title | Olvido | PATCH /issues/<id> con marker |
| Severity incorrecta | Confundió técnica vs sprint | Re-clasificar (R5) |

## 9. Skills invocadas

- `SKILL-ISSUE-001`, `SKILL-DEV-001`

## 10. Scripts invocados

- `SCRIPT-ISSUE-001_create_issue.py`

## 11. Sub-workflows invocados

- `WORKFLOW-ASG-001.036` (siguiente paso)

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Gate anti-mockeo + anti-improvisación. Description estructurada 4 secciones. Devlog blocker enlazado. |
