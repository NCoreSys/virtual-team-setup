# VTT.CARD-DEV-001 — Crear devlog entry

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-DEV-001` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase IN [execution, review] AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA,TL]` |
| **Requiere Cards previas** | ninguna |
| **Pertenece a** | `WORKFLOW-DEV-001.001` |
| **Tokens estimados** | ~769 (medidos con chars/4 el 2026-06-02) |

---

## Qué hacer

Cuando detectás un evento que debe quedar registrado en el devlog de la tarea (decisión técnica, observación, bloqueante, tech debt, testing note, riesgo, issue no-bug):

1. **Decidir `categoryCode`** (uno de 7):

   | Evento | `categoryCode` | Severidad? |
   |---|---|---|
   | Decisión con trade-off | `decision` | no |
   | Observación contextual | `observation` | no |
   | Bloqueante | `blocker` | sí (high/critical) |
   | Deuda técnica | `tech_debt` | sí (low/medium) |
   | Resultado testing | `testing_note` | sí (según) |
   | Riesgo potencial | `risk` | sí (según) |
   | Inconsistencia no-bug | `issue` | sí (según) |

2. **Si el síntoma es bug/blocker/question formal** (no devlog) → STOP, ver `CARD-ISS-001..` (escalación a `VTT.PROTOCOL-ASG-001` §5.4 / §5.4.bis). La entry devlog NO escala issues — los registra.

3. **POST entry** (singular endpoint):

   ```bash
   TOKEN=$(cat .vtt_jwt)
   curl -s -X POST "https://api.vttagent.com/api/tasks/$TASK_ID/devlog" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "categoryCode": "decision",
       "title": "<titulo corto>",
       "description": "<contexto + por que + impacto — NO vacio>",
       "reportedBy": "<TU_UUID>"
     }'
   ```

   Si categoría con severidad → agregar `"severity": "low|medium|high|critical"` (R2).

4. **Capturar `entry_id`** del response para trazabilidad.

## Reglas duras

- `description` **obligatorio y no-vacío** (R1 — caso MS-333: el TL borra entries sin description)
- `severity` enum estricto si aplica (R2 — sin valor → HTTP 400)
- Entry nace en `status: pending` — la transiciona el TL en FASE 3 (CARD-DEV-002) o el PM en FASE 4 (CARD-DEV-003)
- **NO** transicionar entries propias a terminal en esta CARD (excepto correcciones inmediatas — usar DEV-005 para borrar+recrear si fue error)

## Si falla

| Síntoma | Acción |
|---|---|
| 400 `description es requerido` | Re-enviar con descripción ≥1 char no-vacío |
| 400 `severity must be one of [...]` | Verificar enum válido o categoría sin severidad |
| 400 `categoryCode is required` | Usar `categoryCode` (NO `type` — campo legacy) |
| 403 `Missing capability` | Escalar al Coord — gap RBAC del rol |
| 422 `task status invalid` | Tarea no está en `in_progress`/`in_review` |

## Output

Entry creada con `entry_id`, `status: pending`, `reportedBy = TU_UUID`. Lista para procesamiento del TL en code review (`CARD-DEV-002`) o del PM en cierre de sprint (`CARD-DEV-003`).

Si la entry es `critical`/`high` → recordar que bloqueará el Review Gate hasta que se resuelva.
