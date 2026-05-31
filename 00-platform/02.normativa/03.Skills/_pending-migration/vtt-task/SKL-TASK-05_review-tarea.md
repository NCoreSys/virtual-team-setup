# SKL-TASK-05: Review de Tarea (task_in_review → task_completed)

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-TASK-005_review_tarea.md`** en `02.normativa/03.Skills/task/`.
> Migración 1:1, contrato sin cambios. Esta versión se conserva como referencia histórica.


**Categoría:** VTT-TASK  
**Aplica a:** TL  
**Tokens estimados:** ~170  
**Cuándo:** Cuando una tarea llega a `task_in_review` y el TL debe revisarla

---

## Precondición

- Tarea en status `task_in_review`
- `$TOKEN` obtenido (SKL-AUTH-01)
- ASSIGNMENT original disponible en `knowledge/agent-tasks/assignments/ASSIGNMENT_$TASK_ID_$SLUG.md`

---

## Paso 1 — Leer entregables de la tarea

```bash
# Ver attachments (devlog, code-logic, assignment)
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Leer TODOS los comentarios
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Feed de actividad completo
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/activity" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Verificar que existen:
- [ ] Devlog (`fileType=devlog`)
- [ ] Code Logic (`fileType=code_logic`) — uno por cada archivo creado/modificado
- [ ] Comentario de entrega del agente con formato de reporte
- [ ] PR en GitHub (URL en el comentario de entrega)

---

## Paso 2 — Verificar checklist del ASSIGNMENT

Abrir el ASSIGNMENT original y validar CADA item del checklist. No es solo verificar que existan archivos — verificar cada condición específica.

---

## Paso 3 — Verificar entregables obligatorios

```
[ ] Código funcional (compila + corre localmente)
[ ] .LOGIC.md por cada archivo creado/modificado (verificar en repo)
[ ] Development Log en knowledge/development-log/YYYY-MM-DD_$TASK_ID_*.md
[ ] Commit con Co-Authored-By + Refs: #$TASK_ID
[ ] Swagger docs agregados y visibles en /api-docs (si hay endpoints)
[ ] PR creado con gh pr create (no commits sueltos sin PR)
```

---

## Paso 3.5 — Verificar Living Documents actualizados

Según el tipo de tarea, el agente DEBE haber actualizado los Living Documents correspondientes.
Ver tabla completa en `00-platform/06.Documentos_soporte/LIVING_DOCUMENTS_MEMORY_SERVICE.md §4.3`.

| Tipo tarea | Living Docs obligatorios |
|------------|--------------------------|
| DB (4.2.x) | LD-01 schema_prisma.md, LD-02 erd.md (+ LD-06 si hay índices nuevos) |
| BE (4.3.x) | LD-03 openapi_spec.md, LD-04 endpoints_list.md (+ LD-05 si hay errores nuevos) |
| DO (4.1.x, 6.x) | LD-12 env_matrix.md si hay vars nuevas |
| TL | LD-10 component_diagram.md, LD-13 decision_log.md si hay cambios arquitectónicos |

**Verificar:** ¿La sección "Document Impacts" del reporte del agente lista estos archivos?

- Si actualizó correctamente → incluir en APR-TL: "Living Documents verificados: LD-01 ✅, LD-03 ✅"
- Si falta alguno → **RECHAZAR** con feedback: "Falta actualizar LD-XX [nombre del archivo]"

---

## Paso 4 — Verificar consistencia técnica

Según tipo de tarea:

| Tipo | Qué verificar |
|------|--------------|
| BE | Patrones del router, validators, manejo de errores con try-catch, sin console.log de debug |
| FE | Tokens del design system (no hardcoded), componentes reutilizados, hooks existentes |
| DB | Convenciones UUID/naming, sin datos mock, migration correcta |
| Design | Design system respetado, rutas exactas referenciadas, sin suposiciones |
| Docs | Rutas exactas, sin datos inventados, trazabilidad a tarea origen |

Verificar contrato contra **SPEC v1.9** en la sección correspondiente.

---

## Paso 5 — Verificar issues abiertos

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/issues" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
issues = json.load(sys.stdin)
open_issues = [i for i in issues.get('data', []) if not i.get('isResolved')]
print(f'Issues abiertos: {len(open_issues)}')
for i in open_issues:
    print(f'  - {i[\"title\"]} ({i[\"severity\"]})')
"
```

**Si hay issues abiertos → NO mover a completed.**

---

## Paso 5.5 — Procesar items detectados por el agente (SOP-TRK-02)

Leer la sección "Items detectados para trackeo" del comentario de entrega del agente.

Para cada item listado:

1. **Verificar si ya existe** en VTT: `GET /api/projects/{PROJECT_ID}/trackable-items?limit=200`
2. **Clasificar:**
   - **Tipo A** (Retroactivo = Sí) → RF, NFR, BR, UC nuevos: revisar tareas ya aprobadas y en curso
   - **Tipo B** (Retroactivo = No) → ADR, assumption, constraint, tech_debt: solo aplica hacia adelante
3. **Ejecutar:** Ver SOP-TRK-02 §4 (Tipo A) o §5 (Tipo B)
4. **Registrar decisión** en el comentario APR-TL:
   ```
   Items detectados procesados:
   - ADR-SA-007: CREADO. No retroactivo. Linkeado a esta tarea.
   - BR-024: CREADO. Retroactivo: linkeado a MS-052 y MS-054. Cerrado (ti_approved).
   - NFR-PERF-07: PENDIENTE — requiere decisión PM (posible nueva tarea de testing).
   ```

Si no hay items → omitir esta sección del comentario APR-TL.

---

## Paso 6 — Decisión y acción

### Si todo OK → Aprobar

```bash
# 1. Comentario APR-TL (ANTES de cambiar status)
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"APR-TL: revisión técnica aprobada. Entregables completos. Checklist OK. Contrato SPEC verificado. Notas: $REVIEW_NOTES\",
    \"userId\": \"$AGENT_UUID\"
  }"

# 2. Mover a task_completed
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"aa5ceb90-5209-42a2-b874-a8cbee597a97\", \"changedBy\": \"$AGENT_UUID\"}"
```

### Si hay observaciones → Rechazar con feedback

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"REVIEW-TL: cambios requeridos antes de aprobar:\n1. $CAMBIO_1\n2. $CAMBIO_2\nTarea queda en in_review hasta que se corrijan.\",
    \"userId\": \"$AGENT_UUID\"
  }"
# No cambiar status — queda en task_in_review
```

### Si hay bloqueante técnico → Escalar

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
# Luego notificar al PM
```

---

## Reglas críticas

- ❌ NUNCA mover a `task_completed` con issues abiertos
- ❌ NUNCA mover a `task_completed` si hay comentarios con bugs sin verificar
- ❌ NUNCA mover a `task_completed` si falta devlog, code-logic o PR
- ❌ NUNCA mover a `task_approved` — eso es **solo del PM**
- ❌ NUNCA usar `PATCH /status` para poner `on_hold` — usar `PUT /on-hold`
- ✅ Siempre comentar APR-TL ANTES de mover a completed
- ✅ Si hay feedback → comentario con lista puntual, no genérica
