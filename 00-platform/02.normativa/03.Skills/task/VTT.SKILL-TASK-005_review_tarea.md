# VTT.SKILL-TASK-005 — Review de Tarea (task_in_review → task_completed)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-TASK-005` |
| **Categoría** | TASK (Task CRUD) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | TL Reviewer |
| **Tokens estimados** | ~600 |
| **Cuándo se usa** | FASE 4 del PROTOCOL-ASG-001 §5.5 — cuando una tarea llega a `task_in_review` y el TL debe revisarla |
| **Reemplaza** | `SKL-TASK-05_review-tarea.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | Tarea a revisar |
| `assignment_path` | path | sí | ASSIGNMENT original (`knowledge/agent-tasks/assignments/.../ASSIGNMENT_<TASK_ID>_<slug>.md`) |
| `reviewer_uuid` | uuid | sí | UUID del TL Reviewer |
| `decision` | enum | sí | `approve` / `reject_with_feedback` / `escalate_blocker` (definido al final) |
| `review_notes` | string | sí (approve/reject) | Notas para APR-TL comment o feedback |
| `findings` | array (si reject) | depende | Lista de items pendientes a corregir |
| `blocker_data` | object (si escalate) | depende | `{type, title, description}` para `PUT /on-hold` |

---

## Precondición

- Tarea en status `task_in_review`
- $TOKEN obtenido (`VTT.SKILL-AUTH-001`)
- ASSIGNMENT original disponible
- PROTOCOL-ASG-001 §5.5.5.b (verificación de disciplina de worktree) ya ejecutado
- PROTOCOL-MAN-001 §5.4 (v1.5 del manifest) en preparación o ejecutado

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL                          # http://77.42.88.106:3000
$AGENT_UUID                            # = reviewer_uuid del TL
$STATUS_COMPLETED_UUID                 # aa5ceb90-5209-42a2-b874-a8cbee597a97
```

---

## Paso 1 — Leer entregables de la tarea

```bash
# Ver attachments (devlog, code-logic, assignment, manifest)
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool

# Leer TODOS los comentarios (incluye el SKL-REPORT-01 del agente)
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool

# Feed de actividad completo
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/activity" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

**Checklist de existencia:**

- [ ] Devlog attachment (`fileType=devlog`)
- [ ] Code Logic attachments (`fileType=code_logic`) — uno por archivo creado/modificado
- [ ] Manifest v1.0 attachment (`fileType=manifest`, generado por agente)
- [ ] Comentario de entrega del agente con formato SKL-REPORT-01
- [ ] PR en GitHub (URL en el comentario de entrega)
- [ ] Manifest commiteado al PR del agente (PROTOCOL-MAN-001 §5.3.7)

---

## Paso 2 — Verificar checklist del ASSIGNMENT original

Abrir el ASSIGNMENT y validar **CADA** item del checklist (mínimo 10 items según `VTT.SKILL-TASK-002`).

**NO basta con verificar que existan archivos** — verificar la condición específica de cada item.

---

## Paso 3 — Verificar entregables obligatorios

```
[ ] Código funcional (compila + corre localmente — el TL ejecuta `npm test` o equivalente)
[ ] .LOGIC.md por cada archivo creado/modificado (verificar en repo)
[ ] Development Log en `knowledge/development-log/YYYY-MM-DD_<TASK_ID>_<slug>.md`
[ ] Commit con `Co-Authored-By` + `Refs: #<TASK_ID>`
[ ] Swagger docs agregados y visibles en `/api-docs` (si hay endpoints)
[ ] PR creado con `gh pr create` (no commits sueltos)
[ ] Manifest v1.0 generado y commiteado (PROTOCOL-MAN-001 §5.3.7)
```

---

## Paso 4 — Verificar Living Documents actualizados

Si la tarea está en alguna de las categorías que tocan LDs (ver `VTT.SKILL-TASK-002 §Paso 3.5`):

| Tipo tarea | LDs obligatorios |
|---|---|
| `codigo_db` | LD-01 schema_prisma + LD-02 erd + LD-06 si hay índices |
| `codigo_be` | LD-03 openapi_spec + LD-04 endpoints_list + LD-05 si hay errores nuevos |
| `devops` | LD-12 env_matrix si hay vars nuevas |
| TL/AR | LD-10 component_diagram + LD-13 decision_log si hay decisiones arquitectónicas |

**Verificar:** ¿La sección "Document Impacts" del SKL-REPORT-01 lista estos archivos?

- Actualizó correctamente → incluir en APR-TL: "Living Documents verificados: LD-01 ✅, LD-03 ✅"
- Falta alguno → **rechazar** con feedback: "Falta actualizar LD-XX [nombre]"

---

## Paso 5 — Verificar consistencia técnica

Según `task_type`:

| Tipo | Qué verificar |
|---|---|
| `codigo_be` | Patrones del router, validators, manejo de errores con try-catch, sin `console.log` de debug |
| `codigo_fe` | Tokens del design system (no hardcoded), componentes reutilizados, hooks existentes |
| `codigo_db` | Convenciones UUID/naming, sin datos mock, migration correcta |
| `wireframe`/`design_system` | Design system respetado, rutas exactas referenciadas, sin suposiciones |
| `documentacion` | Rutas exactas, sin datos inventados, trazabilidad a tarea origen |

Verificar contrato contra **SPEC** del proyecto en la sección correspondiente.

---

## Paso 6 — Verificar issues abiertos

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/issues" \
  -H "Authorization: Bearer $TOKEN" | python -c "
import sys, json
issues = json.load(sys.stdin)
open_issues = [i for i in issues.get('data', []) if not i.get('isResolved')]
print(f'Issues abiertos: {len(open_issues)}')
for i in open_issues:
    print(f'  - {i[\"title\"]} ({i[\"severity\"]})')
"
```

**Si hay issues abiertos → NO mover a `task_completed`.**

---

## Paso 7 — Procesar items detectados por el agente

Leer la sección "Items detectados para trackeo" del SKL-REPORT-01 del agente.

Por cada item:

1. **Verificar si ya existe** en VTT: `GET /api/projects/<PROJECT_ID>/trackable-items?limit=200`
2. **Clasificar:**
   - **Tipo A — Retroactivo** (RF, NFR, BR, UC nuevos): revisar tareas ya aprobadas y en curso para vincularlos
   - **Tipo B — No retroactivo** (ADR, assumption, constraint, tech_debt): solo aplica hacia adelante
3. **Ejecutar** la acción del Modelo Dinámico (FASE 4 de PROTOCOL-ASG-001 §5.5.10)
4. **Registrar decisión** en el APR-TL comment:
   ```
   Items detectados procesados:
   - ADR-SA-007: CREADO. No retroactivo. Linkeado a esta tarea.
   - BR-024: CREADO. Retroactivo: linkeado a MS-052 y MS-054. Cerrado (ti_approved).
   - NFR-PERF-07: PENDIENTE — requiere decisión PM (posible nueva tarea de testing).
   ```

Si no hay items → omitir esta sección.

---

## Paso 8 — Decisión y acción

### Opción A — Aprobar (si todo OK)

```bash
# 1. APR-TL comment (ANTES de cambiar status)
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"APR-TL: revisión técnica aprobada. Entregables completos. Checklist OK. Living Documents verificados. Contrato SPEC verificado. Notas: $REVIEW_NOTES\",
    \"userId\": \"$AGENT_UUID\"
  }"

# 2. Mover a task_completed
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"$STATUS_COMPLETED_UUID\", \"changedBy\": \"$AGENT_UUID\"}"

# 3. Continuar con WORKFLOW-MAN-001.004 (manifest v1.5)
# 4. Continuar con FASE 4.5 del PROTOCOL-ASG-001 (commit del TL en tl/<TASK_ID>-close)
```

### Opción B — Rechazar con feedback

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"REVIEW-TL: cambios requeridos antes de aprobar:\n1. $CAMBIO_1\n2. $CAMBIO_2\nTarea queda en in_review hasta que se corrijan.\",
    \"userId\": \"$AGENT_UUID\"
  }"
# NO cambiar status — queda en task_in_review
```

### Opción C — Escalar bloqueante técnico

```bash
# Poner en on_hold (NUNCA usar PATCH /status para esto)
curl -s -X PUT "$VTT_BASE_URL/api/tasks/$TASK_ID/on-hold" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-user-id: $AGENT_UUID" \
  -d "{
    \"type\": \"blocker\",
    \"title\": \"$BLOCKER_TITLE\",
    \"description\": \"$BLOCKER_DESCRIPTION\"
  }"
# Notificar al PM
```

---

## Reglas críticas

- ❌ NUNCA mover a `task_completed` con issues abiertos (Paso 6)
- ❌ NUNCA mover a `task_completed` con comentarios de bugs sin verificar
- ❌ NUNCA mover a `task_completed` sin devlog, code-logic o PR (Paso 3)
- ❌ NUNCA mover a `task_approved` — eso es **del PM**
- ❌ NUNCA usar `PATCH /status` para poner `on_hold` — usar `PUT /on-hold`
- ✅ Siempre postear APR-TL **ANTES** de mover a completed
- ✅ Feedback con lista puntual numerada, no genérica
- ✅ Si Living Doc faltante → rechazar SIEMPRE (no aprobar "con observación")

---

## Validación post-acción

### Si aprobaste:

```bash
# Check 1: status correcto
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])"
# Esperado: task_completed

# Check 2: APR-TL comment posteado
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
comments = json.load(sys.stdin)['data']
apr = [c for c in comments if 'APR-TL' in (c.get('message') or '')]
print('APR-TL comments:', len(apr))
"
# Esperado: >= 1
```

### Si rechazaste:

```bash
# Tarea sigue en task_in_review
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])"
# Esperado: task_in_review
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Falta APR-TL antes de mover a completed | Saltar Paso 8 Opción A.1 | Postear el comment ANTES del PATCH status |
| HTTP 400 al cambiar status | UUID del status incorrecto | Usar `$STATUS_COMPLETED_UUID` (no hardcodear) |
| `PUT /on-hold` falla 401 | Falta header `x-user-id` | Agregar `-H "x-user-id: $AGENT_UUID"` (es header dedicado, no Authorization) |
| Aprobé pero issues abiertos | Saltar Paso 6 | RECHAZAR — el approve fue incorrecto. Revertir status a in_review |
| LD faltante pero aprobé igual | Saltar Paso 4 | Aplicar regla crítica — siempre rechazar si falta LD |

---

## Scripts invocados

Ninguno — operaciones inline con curl.

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-COMMENT-003_apr_tl` (cuando se migre) — para postear APR-TL formal
- `VTT.SKILL-STATUS-003_task_completed` (cuando se migre) — para el PATCH de status
- (al aprobar) `VTT.WORKFLOW-MAN-001.004_actualizar_task_manifest_v15` — generar v1.5
- (después) PROTOCOL-ASG-001 §5.5.bis FASE 4.5 — commit del TL en branch `tl/<TASK_ID>-close`

---

## Cuándo NO usar esta Skill

- **Si la tarea está en task_rejected** — esa la cierra el PM, no el TL
- **Si la tarea ya está en task_completed** — re-review no aplica, contactar PM si hay observación posterior

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-TASK-05_review-tarea.md`. Estructura 8 pasos con decisión final (A/B/C). Cross-ref con WORKFLOW-MAN-001.004 + FASE 4.5 del PROTOCOL-ASG-001. Reglas críticas extraídas en sección propia. |
