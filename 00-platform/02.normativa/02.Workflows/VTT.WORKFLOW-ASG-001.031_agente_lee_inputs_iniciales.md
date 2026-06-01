# VTT.WORKFLOW-ASG-001.031 — Agente lee inputs iniciales

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.031` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.1 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor (BE/DB/FE/DO/QA/DL/UX/AR/SA) |
| **Reglas Nivel 0** | `RULE-TEMPLATE-001`, `RULE-AGENT-001` |
| **CARD asociada** | `VTT.CARD-EXE-001` |

---

## 1. Propósito

Garantizar que el agente lee y comprende todos los inputs iniciales antes de iniciar la ejecución técnica. Lección MS-029..035: sin lectura formal completa → entregables incorrectos.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | ID de la tarea asignada |
| `agent_id` | UUID | UUID del agente |
| `agent_role` | enum | BE/DB/FE/DO/QA/DL/UX/AR/SA |
| `assignment_zip_path` | path | Ruta al ZIP de asignación |
| `vtt_token` | string (JWT) | Token JWT |

## 3. Precondiciones

- Notificación de TL recibida con ZIP de asignación
- Tarea en `task_assigned` o `task_pending`
- `$VTT_SETUP` y `$VTT_TOKEN` exportados

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Leer ASSIGNMENT + BRIEF + OPERATIVO COMPLETOS |
| R2 | Verificar Reglas Nivel 0 listadas en header del ASSIGNMENT |
| R3 | Verificar sección TIs APLICABLES (`RULE-TL-002`) |
| R4 | Archivos REFERENCIA OBLIGATORIOS deben existir, si no → STOP |
| R5 | Conflicto TI ↔ ASSIGNMENT → `SKILL-ISSUE-001` ANTES de tocar código (MS-328) |

## 5. Pasos

### Paso 1 — Login + verificar tarea asignada

```bash
export VTT_TOKEN=$(curl -s -X POST "$VTT_BASE_URL/api/auth/login" \
  -d "{\"email\":\"$AGENT_EMAIL\",\"password\":\"$AGENT_PASSWORD\"}" \
  | python -c "import sys,json; print(json.load(sys.stdin)['token'])")
```

### Paso 2 — Leer ASSIGNMENT completo
`knowledge/agent-assignments/<sprint>/<TASK_ID>/ASSIGNMENT_<TASK_ID>.md` → `SKILL-CFL-001`

### Paso 3 — Leer BRIEF completo
`knowledge/agent-assignments/<sprint>/<TASK_ID>/BRIEF_<TASK_ID>.md` → `SKILL-CFL-001`

### Paso 4 — Leer OPERATIVO del rol
`.claude/agents/OPERATIVO_<ROL>_<PROYECTO>.md` → `SKILL-CFL-001`

### Paso 5 — Verificar Reglas Nivel 0 aplicables
Leer cada `RULE-XXX` listada en header del ASSIGNMENT.

### Paso 6 — Verificar TIs APLICABLES
TIs a ATENDER (`ti_approved`) vs TIs a RESPETAR (`ti_draft`). Si conflicto → `SKILL-ISSUE-001`.

### Paso 7 — Verificar archivos REFERENCIA OBLIGATORIOS
Si falta uno → STOP, escalar TL.

## 6. Outputs

| Output | Descripción |
|---|---|
| `assignment_read` | true |
| `brief_read` | true |
| `operativo_read` | true |
| `reference_docs_missing` | [] (debe ser vacío) |
| `conflicts_detected` | [] (debe ser vacío) |

## 7. Validación

- `cat ASSIGNMENT BRIEF OPERATIVO` sin errores
- Todos los archivos referencia listados existen

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Tarea no asignada al agente | Error routing | Escalar TL |
| Archivos referencia faltantes | TL no incluyó | STOP + escalar TL |
| Conflicto TI detectado | ADR vigente vs ASSIGNMENT | `SKILL-ISSUE-001` type=`requirement` severity=`high` |

## 9. Skills invocadas

- `SKILL-AUTH-001`, `SKILL-CFL-001`, `SKILL-ISSUE-001` (condicional)

## 10. Reglas Nivel 0 aplicables

`RULE-TEMPLATE-001`, `RULE-AGENT-001`, `RULE-TL-002`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Formaliza PROTOCOL-ASG-001 §5.3.1. |
