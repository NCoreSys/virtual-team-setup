# VTT.CARD-ISS-001 — Agente crea Issue en VTT (bloqueante)

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-ISS-001` |
| **Tipo** | `CARD-mini` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-EXE-004` |
| **Pertenece a** | WORKFLOW-ASG-001.035 |
| **Tokens estimados** | ~690 |

---

## Cuándo aplica

Cuando detectás un bloqueante REAL durante ejecución:
- Datos faltantes (catálogo vacío, configuración incompleta)
- Conflicto TI ↔ ASSIGNMENT (lección MS-328)
- Dependencia no implementada
- Error técnico irresoluble por consulta

**PROHIBIDO mockear datos** (`RULE-DATA-001`). **PROHIBIDO improvisar** ante conflicto TI.

## Antes de crear el Issue

- Intentar al menos UNA resolución
- Confirmar que es bloqueante real (no duda resoluble por consulta al TL)

## Crear el Issue

```bash
python $VTT_SETUP/02.normativa/04.Scripts/issue/SCRIPT-ISSUE-001_create_issue.py \
  --task-id "$TASK_ID" \
  --type "<dato_faltante|requirement|dependency|tech_error|scope_unclear|infra_failure>" \
  --severity "<critical|high|medium|low>" \
  --title "<síntoma corto>" \
  --description "<description estructurada>" \
  --project-id "$PROJECT_ID" \
  --sprint "$SPRINT" \
  --reported-by "$AGENT_UUID"
```

El script automáticamente:
- Agrega marker textual `[TASK:<TASK_ID>] [SPRINT:<S>]` al title + description
- Registra devlog `blocker` enlazado con el `issueId`

## Description estructurada (4 secciones obligatorias)

```markdown
## Síntoma
<qué está pasando concretamente, errores específicos, paths afectados>

## Intentado
- <resolución 1>: resultado
- <resolución 2>: resultado

## Solicitud
<qué necesitás del TL/PM, específico: "Necesito X del catálogo Y poblado con N registros">

## Impacto si no se resuelve
- Tarea <TASK_ID> no puede completarse
- Downstream: <otras tareas afectadas si aplica>
- Sprint impact: <bajo|medio|alto>
```

## Severity según impacto al sprint

| Impacto | Severity |
|---|---|
| Bloquea sprint completo | `critical` |
| Bloquea tarea + downstream | `high` |
| Bloquea solo tarea | `medium` |
| Workaround posible | `low` |

> **Severity NO es severidad técnica** — es impacto al sprint.

## Después de crear

Tomar `issueId` y pasar a **CARD-ISS-002** (solicitar on_hold).

## Si falla

| Síntoma | Acción |
|---|---|
| HTTP 400 invalid issueType | Usar enum cerrado |
| Sin marker en title | El script lo agrega — verificar versión |
| Severity incorrecta | Re-clasificar según impacto al sprint |

## Output

Issue creado con marker + devlog `blocker` enlazado. Próximo: **CARD-ISS-002** (solicitar on_hold).
