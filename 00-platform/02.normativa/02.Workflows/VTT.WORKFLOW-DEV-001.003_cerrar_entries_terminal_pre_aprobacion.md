# VTT.WORKFLOW-DEV-001.003 — Cerrar entries a estado terminal pre-aprobación del sprint

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-DEV-001.003` |
| **Pertenece a** | `VTT.PROTOCOL-DEV-001` v1.1.0 §5.4 + §5.6 (FASE 4 — Cierre de devlog al cierre de sprint) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-10 |
| **Autor** | TW-OPS (Technical Writer of Operational Processes) |
| **Aplica a** | TL (ejecución y auditoría), PM (decisión final por entries `wont_fix`/`deferred`) |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por `PROTOCOL-DEV-001 §5.4` antes del reporte M del sprint |

---

## 1. Propósito

Llevar **todas** las devlog entries del sprint a estado terminal (`resolved` / `wont_fix` / `deferred`) **antes** de la aprobación formal del sprint (reporte M). Garantiza 0 entries no-terminales al cierre, aplicando el **mapa de gates por familia (D-65)** del `PROTOCOL-DEV-001 v1.1.0 §5.6` y las decisiones D-63 (findings también bloquean) + D-64 (elevación a TI con Sprint DEUDA).

> **Alcance — Q5 resuelta por VTS-026:** este Workflow cubre **FASE 4 del Protocol** (cierre de sprint, TL+PM), NO FASE 3 (code review de tarea individual, que es jurisdicción de `VTT.WORKFLOW-DEV-001.002`). El nombre `cerrar_entries_terminal_pre_aprobacion` se interpreta como "antes de la **aprobación del sprint**" en el reporte M, no como "antes de la aprobación de una tarea individual".

> **Cuándo se invoca:** después de que todas las tareas del sprint pasen a `task_completed` o `task_approved`, antes de que el TL genere el reporte M del sprint y antes de que PM/AR/DL firmen el cierre.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `sprintId` | UUID | Cierre formal del sprint | sí | UUID del sprint cuyo devlog se va a cerrar |
| `taskIds[]` | array de strings (`VTS-XXX`) | `GET /api/sprints/:id/tasks` | derivable | Lista de tareas del sprint a auditar (se deriva si no se pasa explícito) |
| `phaseId` | UUID | Contexto del sprint | condicional | Necesario si hay entries que van a `deferred` con destino la siguiente fase |
| `nextSprintId` | UUID | Planificación PM | opcional | Para entries `deferred` con destino sprint específico |
| `tlUuid` | UUID | Sesión TL | sí | UUID del TL ejecutor (`changedBy` para PATCH de status) |
| `pmUuid` | UUID | Sesión PM | sí | UUID del PM (decide `wont_fix`/`deferred` por entries críticas) |

---

## 3. Precondiciones

- Token JWT válido del TL y disponibilidad del PM (sincrónica o asincrónica vía comments).
- **Todas las tareas del sprint** en estado `task_completed` o `task_approved` (no quedan tareas `in_progress` o `in_review` huérfanas).
- TL con capability `tasks.update` + acceso al sprint.
- Reglas Nivel 0 verificadas para el sprint (ver §10).
- FASE 3 del Protocol completada — todas las tareas pasaron por code review individual; las entries que llegan a este Workflow son las que el TL no resolvió por tarea (típicamente `tech_debt` cross-tarea o decisiones que requieren PM).

> **Si una precondición falla:** ver §8 Errores comunes.

---

## 4. Reglas del Workflow

### 4.1 Mapa de gates por familia (D-65) — qué bloquea qué

> Origen: `PROTOCOL-DEV-001 v1.1.0 §5.6`.

Este Workflow opera sobre el cierre de sprint. **Antes de iterar entries**, el TL debe verificar las 4 familias del Modelo Dinámico:

| Familia | Estado que bloquea cierre de sprint | Cómo se desbloquea |
|---|---|---|
| **Devlog** | Entries `critical`/`high` en `pending`/`acknowledged`/`in_progress` en cualquier tarea del sprint | Aplicar este Workflow (FASE 4) — llevar a terminal |
| **Findings** (D-63) | Findings `open` `critical`/`high` sin dictamen del TL | TL dictamina cada finding por 1 de los 5 caminos de `GUIA_DEVLOG_FINDINGS §2.2` (resolved/wont_fix/false_positive con justificación) |
| **CAs** | Algún CA en `not_met` (DoD incumplido) | Agente / TL completa cada CA con `met` + fulfillment |
| **TIs** | TI vinculado a tareas del sprint sin evidencia válida | Agregar evidencia al TI (link a PR/archivo/decisión) |

**Política operativa: 0 entries no-terminales antes del reporte M.** El review-gate de transiciones individuales permite `medium`/`low` no terminales, pero el cierre de sprint exige terminal en TODAS sin excepción (R10 del Protocol).

### 4.2 D-63 — Findings también bloquean (cross-check con cierre)

> Origen: `PROTOCOL-DEV-001 v1.1.0 §5.2.1`.

Al iniciar este Workflow, el TL **debe** verificar que `GET /api/sprints/:id/findings?status=open&severity=high,critical` retorna **lista vacía**. Si hay findings abiertos `high`/`critical`, **NO arrancar este Workflow** — primero dictaminar los findings invocando `GUIA_DEVLOG_FINDINGS §2.2` (no es jurisdicción de este Workflow, pero su no-resolución bloquea el cierre).

### 4.3 D-64 — Elevación a TrackableItem con patrón Sprint DEUDA

> Origen: `PROTOCOL-DEV-001 v1.1.0 §4` (definiciones) + `GUIA_DEVLOG_FINDINGS §2.2 dictamen 2/3`.

Cuando una entry en este Workflow se transiciona a `deferred` y el destino es un compromiso del proyecto cross-tarea / largo plazo:

- **Elevar a TrackableItem** (`POST /api/trackable-items`) con `originTaskId` = tarea origen + `originRef` = `entryId`.
- Si el compromiso queda para el release actual → vincularlo a una tarea del **Sprint DEUDA** del release.
- Si queda para release futuro → TI `ti_deferred` con `deferredToReleaseId`.
- Si queda como compromiso vigente a vigilar → TI `ti_approved` (activo para monitoreo).

El registro local del devlog cierra como `deferred` con `description` referenciando el código del TI (R14 + workaround §5.3.5 del Protocol).

### 4.4 R14 + workaround T2 al transicionar a `deferred`

> Origen: `PROTOCOL-DEV-001 v1.1.0 §7 R14`.

**NUNCA usar `resolution` para registrar el destino del `deferred`** — el backend la limpia a `null` BY-DESIGN (T2 confirmado VTS-026). Usar una de las 3 opciones:

| # | Opción | Aplicar cuándo |
|---|---|---|
| 1 | `description` original | Si el destino se conocía al crear la entry (típicamente NO en cierre de sprint) |
| 2 | Comment en la tarea origen | Si el destino se decide al diferir (caso típico en cierre de sprint) |
| 3 | `fixTaskId` | Si el destino es una tarea concreta del Sprint DEUDA |

---

## 5. Pasos

### Paso 1 — Verificar precondiciones del sprint

→ invoca **`VTT.SKILL-AUTH-001`** + verificar:

```bash
# Tareas del sprint en estado terminal
curl -s "$VTT_BASE_URL/api/sprints/$SPRINT_ID/tasks" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
tasks = json.load(sys.stdin).get('data', [])
non_terminal = [t for t in tasks if t.get('status',{}).get('code') not in ('task_completed','task_approved','task_cancelled')]
print(f'tareas no-terminales: {len(non_terminal)}')
for t in non_terminal: print(f\"  {t.get('id')} - {t.get('status',{}).get('code')}\")
"

# Findings open high/critical en el sprint (D-63)
curl -s "$VTT_BASE_URL/api/sprints/$SPRINT_ID/findings?status=open" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
findings = json.load(sys.stdin).get('data', [])
blocking = [f for f in findings if f.get('severity') in ('high','critical')]
print(f'findings bloqueantes: {len(blocking)}')
"
```

Si hay tareas no-terminales o findings bloqueantes → **abortar** y resolver antes de continuar.

### Paso 2 — Iterar tareas del sprint y recolectar entries no-terminales

Para cada `taskId` del sprint:

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
entries = json.load(sys.stdin).get('data', [])
pending = [e for e in entries if e.get('status') in ('pending','acknowledged','in_progress')]
for e in pending:
    print(f\"$TASK_ID,{e['id']},{e['categoryCode']},{e.get('severity','-')},{e['title']}\")
"
```

Consolidar en un listado `(taskId, entryId, categoryCode, severity, title, status)` — input para Paso 3.

### Paso 3 — [PROCESO] Para cada entry pendiente, decisión PM

Para cada entry del listado, el PM (con consulta al TL) decide:

| Si la entry... | Acción |
|---|---|
| Tiene fix listo (PR mergeado o tarea correctiva cerrada) | → Paso 4 — transicionar a `resolved` con `resolution` + `fixTaskId` |
| Refleja comportamiento aceptado / decisión de no resolver | → Paso 5 — transicionar a `wont_fix` con `resolution` (justificación) |
| Es compromiso cross-tarea / largo plazo (P1-P3 guía TIs) | → Paso 6 — **elevar a TI** (D-64) + transicionar entry a `deferred` con referencia al código del TI |
| Va a sprint futuro / release siguiente sin elevarse a TI | → Paso 6 alternativo — transicionar a `deferred` con `deferredToPhaseId` + workaround R14 |

### Paso 4 — Transicionar a `resolved`

→ invoca **`VTT.SKILL-DEV-004`** (PATCH `/devlog/:id/status`):

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"status\": \"resolved\",
    \"resolution\": \"<como se resolvio + referencia a PR/commit/tarea>\",
    \"fixTaskId\": \"<VTS-XXX si aplica>\"
  }"
```

Backend: `resolvedAt = now`, `resolvedBy = reportedBy original`, `resolution` preservada.

### Paso 5 — Transicionar a `wont_fix`

→ invoca **`VTT.SKILL-DEV-004`**:

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"status\": \"wont_fix\",
    \"resolution\": \"<por que no se resuelve — decision PM con justificacion concreta>\"
  }"
```

Backend: `resolvedAt = now`, `resolvedBy = null` (no fue resuelto), `resolution` preservada.

**Regla:** `wont_fix` se reserva para decisiones definitivas. Un diferido NUNCA es `wont_fix` (pierde tracking) — si va a otra fase/release, usar `deferred` + elevación a TI (Paso 6).

### Paso 6 — Transicionar a `deferred` (con elevación a TI si aplica)

Decisión previa: ¿la entry pasa el test P1-P3 de guía de TIs (cross-tarea + largo plazo + compromiso del proyecto)?

#### Paso 6a — SÍ pasa P1-P3: elevar a TI (D-64)

1. Crear TI:

```bash
curl -s -X POST "$VTT_BASE_URL/api/trackable-items" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"type\": \"tech_debt|adr|rf|risk|...\",
    \"code\": \"TD-CORE-NNN o equivalente segun trackable_type_catalog\",
    \"title\": \"<titulo del compromiso>\",
    \"description\": \"<contexto + referencia a entry origen>\",
    \"originTaskId\": \"$TASK_ID\",
    \"originRef\": \"devlog_entry:$ENTRY_ID\",
    \"status\": \"ti_approved (si vigente) o ti_deferred (si va a release futuro)\"
  }"
```

Capturar `tiCode` del TI creado.

2. Si el destino es el Sprint DEUDA del release actual, vincular el TI a una tarea de ese sprint (`POST /api/sprints/:deudaSprintId/tasks` con referencia al TI).

3. Postear comment en la tarea origen ANTES del PATCH (R14 workaround opción 2):

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\":\"Entry $ENTRY_ID elevada a TI $TI_CODE (D-64). Diferida con destino Sprint DEUDA.\",\"userId\":\"$TL_UUID\"}"
```

4. PATCH a `deferred`:

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"status\": \"deferred\",
    \"deferredToPhaseId\": \"$PHASE_ID_DESTINO\",
    \"fixTaskId\": \"<VTS-XXX-deuda si hay tarea concreta del Sprint DEUDA>\"
  }"
```

Backend limpia `resolution` a null (R14 BY-DESIGN) — pero la referencia al TI ya quedó preservada en el comment del paso 3.

#### Paso 6b — NO pasa P1-P3: `deferred` simple sin TI

Aplicar workaround R14 (postear comment con destino antes del PATCH) y luego:

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"status\": \"deferred\",
    \"deferredToPhaseId\": \"$PHASE_ID_DESTINO\"
  }"
```

### Paso 7 — Re-ejecutar auditoría (loop hasta 0 pendientes)

Volver a Paso 2 — iterar tareas del sprint. Cuando el conteo de entries no-terminales = 0 en TODAS las tareas → continuar al Paso 8.

> **Si quedan entries sin decidir:** detener cierre de sprint, escalar al PM con listado consolidado de entries pendientes. NO forzar terminal con `wont_fix` sin razón real (viola R10 política operativa).

### Paso 8 — Generar input para reporte M del sprint

Una vez confirmado 0 pending, generar resumen consolidado:

| Métrica | Valor |
|---|---|
| Total entries del sprint | <N> |
| Entries por categoría | `{decision: X, observation: Y, blocker: Z, ...}` |
| Entries resueltas (`resolved`) | <X> |
| Entries `wont_fix` con justificación | <Y> |
| Entries `deferred` con destino registrado | <Z> |
| TIs nuevos creados por elevación D-64 | <W> |

Listado de `deferred` con destino (taskId origen → tiCode/sprintId destino) para incluir en el reporte M.

### Paso 9 — Re-verificar mapa de gates D-65 antes de aprobar sprint

```bash
# Las 4 familias en estado limpio para el sprint
# 1. Devlog: 0 no-terminales (verificado en Paso 7)
# 2. Findings: 0 open high/critical (verificado en Paso 1, re-verificar por seguridad)
curl -s "$VTT_BASE_URL/api/sprints/$SPRINT_ID/findings?status=open" -H "Authorization: Bearer $TOKEN"
# 3. CAs: 0 not_met en tareas del sprint
# 4. TIs: 0 vinculados sin evidencia
```

Si las 4 familias están limpias → input listo para reporte M. Si no → volver al Paso del gate que falla.

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| 0 entries no-terminales en el sprint | estado consolidado | BD del backend | Política operativa R10 cumplida |
| Listado de transiciones | tabla en reporte M | Documento de cierre del sprint | Input para el reporte M con conteos por categoría/status final |
| TIs nuevos | records en `trackable_items` | BD del backend | Compromisos elevados por D-64 con `originTaskId`/`originRef` |
| Comments de trazabilidad para `deferred` | activity entries | Backend VTT | Preservan destino del traspaso (R14 workaround) |
| Tareas en Sprint DEUDA | records en `tasks` | BD del backend | Si hay TIs que se vinculan a Sprint DEUDA del release |

---

## 7. Validación de salida

```bash
# Check 1: 0 entries no-terminales en TODAS las tareas del sprint
for TASK_ID in $(curl -s "$VTT_BASE_URL/api/sprints/$SPRINT_ID/tasks" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; [print(t['id']) for t in json.load(sys.stdin).get('data',[])]"); do
  N=$(curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
    | python -c "import sys,json; e=json.load(sys.stdin).get('data',[]); print(len([x for x in e if x.get('status') in ('pending','acknowledged','in_progress')]))")
  echo "$TASK_ID: $N no-terminales"
done
# Esperado: todas las lineas con ': 0 no-terminales'

# Check 2: 0 findings open high/critical en el sprint (D-63)
curl -s "$VTT_BASE_URL/api/sprints/$SPRINT_ID/findings?status=open&severity=high,critical" \
  -H "Authorization: Bearer $TOKEN" | python -c "import sys,json; print(len(json.load(sys.stdin).get('data',[])))"
# Esperado: 0

# Check 3: review-gate del sprint
curl -s "$VTT_BASE_URL/api/sprints/$SPRINT_ID/review-gate" -H "Authorization: Bearer $TOKEN"
# Esperado: canProceedToApproval:true (o equivalente segun backend)
```

Lista verificable:

- [ ] 0 entries `pending`/`acknowledged`/`in_progress` en cualquier tarea del sprint
- [ ] 0 findings `open` `high`/`critical` en el sprint (D-63)
- [ ] Todos los `deferred` tienen su destino registrado fuera de `resolution` (R14 workaround aplicado)
- [ ] Cada elevación D-64 tiene su TI creado con `originTaskId`/`originRef` y comment de trazabilidad
- [ ] Reporte M tiene el listado consolidado por categoría/status final

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Tareas no-terminales en el sprint al arrancar | El TL llamó este Workflow antes de cerrar todas las tareas del sprint | Esperar a que todas las tareas pasen a `task_completed`/`task_approved`. NO forzar cierre del sprint con tareas en curso |
| Findings `open` `high`/`critical` bloquean | D-63: gate del sprint exige dictamen de findings | Dictaminar findings invocando `GUIA_DEVLOG_FINDINGS §2.2` ANTES de arrancar este Workflow |
| Entry con `wont_fix` sin razón real | Atajo para destrabar el gate | Viola política operativa R10. Si no se puede justificar `wont_fix`, evaluar `deferred` con elevación a TI (D-64) |
| `deferred` quedó sin destino trackeable | R14 violada: se intentó usar `resolution` para registrar destino | El backend la limpió a null. Postear comment de trazabilidad en la tarea referenciando `entryId` + destino. Si destino debía ser TI, crear el TI ahora y vincular en comment |
| HTTP 400 al crear TI por elevación D-64 | `type` o `code` fuera del catálogo `trackable_type_catalog` | Consultar catálogo: `GET /api/catalogs/trackable-types` |
| Loop infinito en Paso 7 | El PM no decide alguna entry y queda colgando | Escalar al PM con listado explícito. NO forzar `wont_fix` sin decisión real |

---

## 9. Skills invocadas

| Skill | Para qué se usa en este Workflow |
|---|---|
| `VTT.SKILL-AUTH-001` | Obtener `$TOKEN` JWT |
| `VTT.SKILL-DEV-004` | Lifecycle por cada entry (PATCH `/status`) — Pasos 4/5/6 |
| `VTT.SKILL-COMMENT-001` | Postear comment de trazabilidad para `deferred` (R14 workaround) — Paso 6 |
| `VTT.SKILL-QUERY-003` | GET de tareas / devlog / findings del sprint — Pasos 1, 2, 7, 9 |

> **NO se invocan** Skills de creación de entries (DEV-001/002) — este Workflow opera sobre entries ya existentes.

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-DATA-001` Prohibido mockear datos | NO inventar `resolution` para `wont_fix` con tal de destrabar el gate del sprint. La decisión debe ser real |
| `RULE-AGENT-001` Worktree por rol | El TL ejecuta este Workflow desde su worktree de rol. NO desde el clone base ni desde worktree de agente |
| `RULE-SEC-001` No postear datos sensibles | Comments de trazabilidad del R14 quedan en activity feed visible. Prohibido incluir credenciales, IPs prod, paths absolutos sensibles |
| `RULE-VTT-004` Manifest al final | El TL registra `devlog_resolved_count`/`devlog_wontfix_count`/`devlog_deferred_count` en el manifest del sprint AL FINAL — no parcial |

> Para descubrir reglas aplicables al sprint: `python 00.Rules/query_rules.py --simulate-task <sprintId>` (con contexto de sprint).

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-06-10 | TW-OPS (VTS-027) — revisión LEAD_NPL | Versión inicial. Materializa **FASE 4 del `PROTOCOL-DEV-001 v1.1.0` §5.4** (cierre de devlog al cierre de sprint, TL+PM — Q5 resuelta por VTS-026: FASE 4 cierre sprint, NO FASE 3 task review). Incorpora: **D-65 mapa de gates por familia** (referencia §5.6 del Protocol con 4 familias devlog/findings/CAs/TIs) + **D-63 findings también bloquean** (verificación obligatoria en Paso 1 + Paso 9) + **D-64 elevación a TrackableItem con patrón Sprint DEUDA** (Paso 6a) + **R14 workaround T2** al transicionar a `deferred` (Paso 6 + comments de trazabilidad). Skills invocadas: DEV-004 / COMMENT-001 / QUERY-003 / AUTH-001. Origen: reporte VTS-026 §4.1 + bump Protocol VTS-051 (§5.6 mapa gates + §5.2.1 D-63 + §4 D-64). |
