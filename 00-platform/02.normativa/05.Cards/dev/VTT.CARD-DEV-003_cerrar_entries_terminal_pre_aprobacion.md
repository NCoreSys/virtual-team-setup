# VTT.CARD-DEV-003 — Cerrar entries terminales pre-aprobación del sprint

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-DEV-003` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `sprint.action = close AND agent.role IN [TL, PM]` |
| **Requiere Cards previas** | ninguna (es la última fase del sprint) |
| **Pertenece a** | `WORKFLOW-DEV-001.003` |
| **Tokens estimados** | ~1029 (medidos con chars/4 el 2026-06-02) |

---

## Qué hacer

Al cerrar el sprint, garantizar que **0 entries del devlog quedan en estados no-terminales** (`pending`, `acknowledged`, `in_progress`) antes de aprobar el reporte M.

> **Scope:** este es el cierre del SPRINT completo, NO de una tarea individual. La pre-aprobación es del reporte M / milestone del sprint, no del PASS de code review de una tarea.

### Paso 1 — Auditoría inicial: listar pending del sprint completo

```bash
TOKEN=$(cat .vtt_jwt)
SPRINT_TASKS=( "PROJ-101" "PROJ-102" "PROJ-103" )   # del GET /api/sprints/:id/tasks

for T in "${SPRINT_TASKS[@]}"; do
  curl -s "https://api.vttagent.com/api/tasks/$T/devlog" -H "Authorization: Bearer $TOKEN" \
    | python -c "
import sys, json
d = json.load(sys.stdin)['data']
for e in d:
    if e['status'] in ('pending','acknowledged','in_progress'):
        print(f\"$T {e['id'][:8]} {e['categoryCode']:14s} {e.get('severity') or '-':8s} {e['status']:14s} {e['title'][:60]}\")
"
done
```

### Paso 2 — Decisión PM por cada entry

PM evalúa caso por caso:

| Si... | Destino |
|---|---|
| Hay fix listo (PR mergeado) | `resolved` con `resolution` + `fixTaskId` |
| No se va a resolver (comportamiento aceptado) | `wont_fix` con `resolution` justificando |
| Va a sprint S+1, S+2, release futuro | `deferred` con `deferredToPhaseId` (+ `fixTaskId` si ya se conoce) |

TL ejecuta las transiciones via **CARD-DEV-002 Vía B** para cada entry. Iterar hasta procesar todas.

### Paso 3 — Re-auditar: confirmar `count == 0`

```bash
COUNT=0
for T in "${SPRINT_TASKS[@]}"; do
  C=$(curl -s "https://api.vttagent.com/api/tasks/$T/devlog" -H "Authorization: Bearer $TOKEN" \
    | python -c "import sys,json; print(sum(1 for e in json.load(sys.stdin)['data'] if e['status'] in ('pending','acknowledged','in_progress')))")
  COUNT=$((COUNT+C))
done
echo "Sprint pending: $COUNT"
test "$COUNT" -eq 0 && echo "OK — listo para reporte M" || echo "BLOCK — iterar paso 2"
```

### Paso 4 — Resumen para reporte M

Generar bloque markdown para incluir en el reporte M:

```markdown
## Devlog del sprint <ID>

| categoryCode | total | resolved | wont_fix | deferred |
|---|---|---|---|---|
| decision | <n> | <r> | <w> | <d> |
| observation | <n> | <r> | <w> | <d> |
| ... | | | | |

### Deferred (con destino)
- <entry_uuid>  taskA  "<title>"  → fase <X>  [fixTaskId: PROJ-NNN o TBD]
- ...

Total no-terminales al cierre: 0 ✅
```

## Reglas duras

- **0 entries no-terminales** es condición no-negociable (R10 del Protocol)
- Decisión `wont_fix` y `deferred` la confirma el PM. El TL ejecuta pero no decide solo en entries `critical`/`high`
- Entries `critical`/`high` que quedan pending bloquean Review Gate de TODAS las tareas del sprint
- Actualizar Task Manifest v1.5 si los conteos cambian respecto a FASE 3 (ver MAN-001 §5.4)
- `fixTaskId` puede registrarse post-cierre cuando se crea la tarea hija en sprint siguiente

## Si falla

| Síntoma | Acción |
|---|---|
| Count > 0 después de Paso 3 | Re-ejecutar Paso 1 + mostrar listado al PM para destrabar |
| Una tarea del sprint no responde al GET /devlog | Tarea cancelada/eliminada — confirmar lista del sprint con `GET /api/sprints/:id/tasks` |
| 400 al transicionar entries en masa | Ver CARD-DEV-002 errores comunes |
| PM no decide sobre entry `critical` | Escalar verbalmente — NO cerrar sprint con la entry viva |

## Output

Sprint con `count(pending+acknowledged+in_progress) == 0` en todas sus tareas. Reporte M con resumen del devlog procesado (totales por categoryCode + listado deferred). Task Manifests v1.5 actualizados si hubo cambios. **Listo para aprobación formal del reporte M y cierre del sprint**.
