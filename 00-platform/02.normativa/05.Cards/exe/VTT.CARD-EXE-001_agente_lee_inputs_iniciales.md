# VTT.CARD-EXE-001 — Agente lee inputs iniciales

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-001` |
| **Tipo** | `CARD-mini` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = assignment AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | ninguna |
| **Pertenece a** | WORKFLOW-ASG-001.031 |
| **Tokens estimados** | ~520 |

---

## Qué hacer

Al recibir notificación de asignación, ANTES de tocar código:

1. **Login VTT** + capturar `AGENT_UUID` del JWT:
   ```bash
   export VTT_TOKEN=$(curl -s -X POST "$VTT_BASE_URL/api/auth/login" \
     -H "Content-Type: application/json" \
     -d "{\"email\":\"$AGENT_EMAIL\",\"password\":\"$AGENT_PASSWORD\"}" \
     | python -c "import sys,json; print(json.load(sys.stdin)['token'])")
   ```

2. **Leer ASSIGNMENT completo**: `knowledge/agent-assignments/<sprint>/<TASK_ID>/ASSIGNMENT_<TASK_ID>.md`

3. **Leer BRIEF completo**: referenciado por ASSIGNMENT

4. **Leer OPERATIVO del rol**: `.claude/agents/OPERATIVO_<ROL>_<PROYECTO>.md`

5. **Verificar Reglas Nivel 0** listadas en el header del ASSIGNMENT (leer en `00.Rules/` las que no conozcas)

6. **Revisar sección TIs APLICABLES** del ASSIGNMENT:
   - **TIs a ATENDER** (`ti_approved`) — tarea responsable de implementarlos
   - **TIs a RESPETAR** (`ti_draft` ADR/RNF) — restricciones del código

7. **Verificar archivos REFERENCIA OBLIGATORIOS** existen en disco. Sin uno → STOP, escalar al TL.

## Si detectas conflicto TI ↔ ASSIGNMENT

**NO improvisar.** Crear Issue `type=requirement` `severity=high` via **CARD-ISS-001** ANTES de tocar código.

**Lección MS-328:** agente entregó sidebar colapsable contradiciendo ADR-UX-15 (no colapsable) porque el ADR no se leyó al asignar. Detectado tarde en review.

## Si falla

| Síntoma | Acción |
|---|---|
| Archivo de referencia faltante | STOP + escalar al TL — NO ejecutar con inputs parciales |
| TI contradice ASSIGNMENT | Issue antes de tocar código (CARD-ISS-001) |
| OPERATIVO no encontrado | Consultar TL — fallback con guía genérica del rol |
| Tarea no aparece asignada al agente | Verificar `assignedToId` con TL — posible error de routing |

## Output

Comprensión completa: scope, restricciones, CAs, entregables esperados. Listo para **CARD-EXE-002** (verificar worktree).
