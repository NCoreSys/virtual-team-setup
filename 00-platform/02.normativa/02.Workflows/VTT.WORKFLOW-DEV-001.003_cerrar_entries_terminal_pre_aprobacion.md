# VTT.WORKFLOW-DEV-001.003 — Cerrar entries terminales pre-aprobación del sprint

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-DEV-001.003` |
| **Pertenece a** | `VTT.PROTOCOL-DEV-001` §5.4 (FASE 4 — Cierre de devlog al cierre de sprint) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-02 |
| **Autor** | TW-OPS (auditoría VTS-007) |
| **Aplica a** | TL Reviewer + PM (cierre formal del sprint, antes del reporte M) |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por Protocol padre §5.4 |
| **CARD asociada** | `VTT.CARD-DEV-003` (pendiente — creada en commit 4 de VTS-007) |

> **Scope confirmado por Coord (issue 6a8e7df6 Q5):** este Workflow cubre **FASE 4 cierre de sprint**. El "pre-aprobacion" del título refiere a "antes de aprobar el reporte M / cerrar el sprint formalmente", NO a la pre-aprobación de una tarea individual (eso está cubierto en FASE 3 vía Workflow .002).

---

## 1. Propósito

Auditar el devlog del sprint completo y garantizar que **0 entries quedan en estados no-terminales** antes de aprobar el reporte M del sprint.

Iterar todas las tareas del sprint, listar entries en `status ∈ {pending, acknowledged, in_progress}`, y mover cada una a un estado terminal (`resolved` / `wont_fix` / `deferred`) según decisión del PM.

Es el último gate operativo antes del cierre formal del sprint (registrado por PM en el reporte M / milestone).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `sprint_id` | UUID | Sprint en cierre | sí | Sprint cuyas tareas se auditan |
| `sprint_tasks` | array de string | Listado del sprint | sí | IDs de TODAS las tareas del sprint (incluso `task_approved`) |
| `actor_uuid_tl` | UUID | OPERATIVO TL | sí | UUID del TL Reviewer que conduce la auditoría |
| `actor_uuid_pm` | UUID | OPERATIVO PM | sí | UUID del PM que decide destino de entries pendientes |
| `vtt_token` | string (JWT) | `VTT.SKILL-AUTH-001` previo | sí | Token de autenticación |
| `target_phase_id` | UUID | Fase destino para `deferred` | sí si hay entries diferidas | Fase a la que se difieren entries futuras |

---

## 3. Precondiciones

- Todas las tareas del sprint están en estado terminal (`task_approved`, `task_completed`, `task_cancelled` o `task_rejected`)
- TL completó procesamiento FASE 3 de cada tarea individual (vía Workflow .002)
- PM confirma que el sprint está listo para cerrar (no quedan tareas vivas)
- Manifest v1.5 ya fue agregado por el TL a tareas aprobadas (registra `devlog_resolved_count`)

---

## 4. Reglas operativas del Workflow

| # | Regla |
|---|---|
| WF1 | **0 entries en `pending/acknowledged/in_progress`** es condición no-negociable para cerrar sprint (R10 del Protocol). NO aprobar reporte M con entries vivas |
| WF2 | Decisión por entry según destino: `resolved` (hay fix listo), `wont_fix` (no se va a resolver, justificación), `deferred` (va a otro sprint, con `deferredToPhaseId`) |
| WF3 | Decisión final de `wont_fix` y `deferred` es del PM. El TL ejecuta las transiciones pero la decisión es PM (especialmente en entries `critical`/`high`) |
| WF4 | Si una entry se difiere y va a generar tarea hija en sprint siguiente: registrar `fixTaskId` en la entry cuando exista esa tarea (puede ser post-cierre) |
| WF5 | Re-ejecutar auditoría (Paso 7) después de aplicar todas las transiciones para confirmar `count(pending+acknowledged+in_progress) == 0` |
| WF6 | Reporte M debe incluir el resumen del devlog procesado (totales por categoryCode + totales por destino terminal + listado de diferidos) |

---

## 5. Pasos

### Paso 1 — Auditoría inicial: listar entries no-terminales del sprint

```bash
TOKEN=$(cat .vtt_jwt)
PENDING_ALL=()
for TASK in "${SPRINT_TASKS[@]}"; do
  ENTRIES=$(curl -s "https://api.vttagent.com/api/tasks/$TASK/devlog" \
    -H "Authorization: Bearer $TOKEN" \
    | python -c "import sys,json; d=json.load(sys.stdin)['data']; [print(f'$TASK {e[\"id\"]} {e[\"categoryCode\"]} {e.get(\"severity\",\"-\")} {e[\"status\"]} {e[\"title\"][:60]}') for e in d if e['status'] in ('pending','acknowledged','in_progress')]")
  PENDING_ALL+=("$ENTRIES")
done
echo "${PENDING_ALL[@]}" > /tmp/sprint_devlog_pending.txt
wc -l /tmp/sprint_devlog_pending.txt
```

→ output: listado tabular `taskId entryId categoryCode severity status title`

### Paso 2 — Generar reporte de decisión para el PM

Agrupar entries pendientes por categoría + severidad. Para cada una proponer destino (`resolved`/`wont_fix`/`deferred`) basado en:

| Si... | Destino propuesto |
|---|---|
| Hay fix listo en código (PR mergeado) | `resolved` con `resolution` + `fixTaskId` |
| Comportamiento aceptado, no se va a resolver | `wont_fix` con `resolution` justificando |
| Va a sprint S+1 / S+2 / release futuro | `deferred` con `deferredToPhaseId` |
| TL no decide solo (escalación) | Esperar decisión PM |

Entregable: tabla con N filas (una por entry pendiente) + columna "Destino propuesto" + "Justificación".

### Paso 3 — Decisión PM por cada entry

PM revisa la propuesta del TL y confirma/ajusta cada destino. Output: tabla con decisión final por cada entry.

### Paso 4 — Aplicar transiciones (TL ejecuta)

Por cada entry decidida, → invoca **`VTT.WORKFLOW-DEV-001.002`** Vía B (transicionar lifecycle) con (`task_id`, `entry_id`, `actor_uuid_tl`, `target_status`, payload según destino).

Iterar hasta procesar todas las entries.

### Paso 5 — Registrar `fixTaskId` en `deferred` (si corresponde)

Para entries `deferred` que ya tienen tarea hija identificada en sprint siguiente: actualizar la entry con `fixTaskId` apuntando a la tarea destino. → invoca **`VTT.WORKFLOW-DEV-001.002`** Vía A (editar contenido — aunque la entry esté en terminal, el campo `fixTaskId` se puede actualizar post-terminal). **Verificar con el backend si esto está permitido** — si no, dejar `fixTaskId` para registro out-of-band.

### Paso 6 — Snapshot de manifest v1.5 (actualización conteos)

Si los conteos `devlog_resolved_count` / `devlog_wontfix_count` / `devlog_deferred_count` cambiaron desde el procesamiento FASE 3 (ej. una entry `acknowledged` se movió ahora a `wont_fix`), actualizar el Task Manifest v1.5 correspondiente. → ver `VTT.PROTOCOL-MAN-001` §5.4.

### Paso 7 — Auditoría final: verificar 0 pendientes

Re-ejecutar Paso 1 sobre el sprint completo.

¿`count(pending+acknowledged+in_progress) == 0`? →
- **SÍ** → continuar Paso 8 (cierre formal)
- **NO** → STOP. Iterar Pasos 3-4 hasta cumplir. NO aprobar reporte M con entries vivas.

### Paso 8 — Generar resumen para reporte M

Resumen del devlog del sprint:

```
Sprint <ID>
═══════════════
Total entries: <N>
  Por categoryCode:
    decision:       <n1>
    observation:    <n2>
    blocker:        <n3>
    tech_debt:      <n4>
    testing_note:   <n5>
    risk:           <n6>
    issue:          <n7>
  Por destino terminal:
    resolved:       <r>
    wont_fix:       <w>
    deferred:       <d> → ver listado abajo
    deleted:        <del>
  Total no-terminales: 0  ✅

Listado de deferred:
  - entry <uuid1> (taskA): "<title>" → fase <X> [fixTaskId: PROJ-NNN]
  - entry <uuid2> (taskB): "<title>" → fase <Y> [fixTaskId: TBD]
  ...
```

→ output: bloque de markdown listo para pegarse en reporte M.

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `audit_initial_count` | int | Reporte M | Total entries no-terminales al iniciar |
| `audit_final_count` | int | Reporte M | Total entries no-terminales al cerrar (debe ser 0) |
| `resolved_count` | int | Reporte M + Manifest v1.5 | Entries resueltas en esta FASE 4 |
| `wontfix_count` | int | Reporte M + Manifest v1.5 | Entries marcadas wont_fix |
| `deferred_count` | int | Reporte M + Manifest v1.5 | Entries diferidas |
| `deferred_listing` | tabla | Reporte M | Listado con UUID, taskId, title, target phase, fixTaskId |

---

## 7. Validación de salida

```bash
# Validación: 0 pending+acknowledged+in_progress en todo el sprint
TOKEN=$(cat .vtt_jwt)
COUNT=0
for TASK in "${SPRINT_TASKS[@]}"; do
  C=$(curl -s "https://api.vttagent.com/api/tasks/$TASK/devlog" \
    -H "Authorization: Bearer $TOKEN" \
    | python -c "import sys,json; print(sum(1 for e in json.load(sys.stdin)['data'] if e['status'] in ('pending','acknowledged','in_progress')))")
  COUNT=$((COUNT+C))
done
echo "Sprint pending entries: $COUNT"
test "$COUNT" -eq 0 && echo "OK — sprint puede cerrarse" || echo "BLOCK — iterar FASE 4"
```

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Entry no se mueve a `resolved` | Falta `resolution` o `fixTaskId` mal formado | Ver Workflow .002 §8 |
| `deferred` sin `deferredToPhaseId` | El backend rechaza con HTTP 400 | Confirmar fase destino con PM antes de PATCH |
| Una tarea del sprint no responde a `GET /devlog` | Tarea cancelada/eliminada | Confirmar lista de tareas del sprint con `GET /api/sprints/:id` |
| Count > 0 después de Paso 7 | Hay entries que no se procesaron | Re-ejecutar Paso 1 y mostrar el listado al PM para destrabar |

---

## 9. Skills invocadas

| Skill | Cuándo |
|---|---|
| `VTT.SKILL-AUTH-001` | Si `$VTT_TOKEN` expiró |
| `VTT.SKILL-DEV-004` | Cada transición de lifecycle (vía Workflow .002 Paso 4) |
| `VTT.SKILL-DEV-003` | Si hay que actualizar `fixTaskId` en entries deferred |
| `VTT.SKILL-QUERY-*` | Listar tareas del sprint (`GET /api/sprints/:id/tasks`) |

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-VTT-002` | `resolution` requerido al resolver — aplica a TODOS los `wont_fix` y `resolved` de esta fase |
| `RULE-VTT-001` | Entries `critical`/`high` que queden en pending bloquean cierre del sprint |
| `RULE-AGENT-001` | El PM aprueba `wont_fix` (humano, no agente) — el TL no decide solo |

---

## 11. Cambios

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-06-02 | TW-OPS (auditoría VTS-007) | Versión inicial. Workflow operativo de la FASE 4 (cierre de sprint) del PROTOCOL-DEV-001. Cubre auditoría inicial → decisión PM por entry → transiciones masivas → re-auditoría → resumen para reporte M. Origen: gap G1 detectado en auditoría VTS-007. Scope FASE 4 confirmado por Coord en issue `6a8e7df6` Q5 — el "pre_aprobacion" del título refiere a la aprobación del reporte M del sprint. |

---

**Pertenece a:** `VTT.PROTOCOL-DEV-001` §5.4
**Workflow padre:** `VTT.PROTOCOL-DEV-001`
**Consumidores:** TL Reviewer + PM (cierre de sprint)
