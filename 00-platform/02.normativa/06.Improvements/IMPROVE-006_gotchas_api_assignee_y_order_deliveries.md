# IMPROVE-006 — Gotchas API: `assigneeId` vs `assignedToId` + colisión de `order` en Deliveries

| Campo | Valor |
|---|---|
| **Código** | `IMPROVE-006` |
| **Título** | Documentar/fix gotchas API: `assigneeId` ignorado y `order` Deliveries sin validación de unicidad |
| **Categoría** | Backend / API / Documentation |
| **Prioridad** | 🟡 Media (2 gaps documentación) / 🟢 Baja (fix opcional) |
| **Estimación rough** | 4 horas (fix BE) o 1 hora (solo documentación) |
| **Estado** | Propuesta — pendiente de evaluación PM |
| **Autor** | TL VTT (`abdff0db-ad0b-4a0c-99f5-c898d18bd2d8`) |
| **Fecha** | 2026-05-16 |
| **Origen** | Setup Sprint S06-FIX-A en Fase 11 MGP — 2 gotchas detectados en producción |
| **Validado contra** | Backend VTT `http://77.42.88.106:3000` (versión productiva 2026-05-16) |

---

## Relación con otras mejoras

- **IMPROVE-003 (Platform Gaps)**: similar en naturaleza — son gaps entre lo documentado y lo implementado
- **Independiente** de IMPROVE-001/002/004/005

---

## Resumen ejecutivo

Durante el setup del Sprint S06-FIX-A en Fase 11 MGP (creación de 16 tareas + 6 Deliveries + dependencias + asignación), detectamos **2 gotchas en endpoints VTT** que rompen el flujo si el TL no los conoce:

1. **GAP-VTT-06** — `POST /api/phases/:id/tasks` y `PATCH /api/tasks/:id` ignoran `assigneeId` silenciosamente. El campo correcto es `assignedToId`.
2. **GAP-VTT-07** — `POST /api/deliveries` acepta `order` duplicado dentro de la misma fase sin validación, causando colisiones de orden en el Gantt.

Ambos están **resueltos con workarounds** pero no documentados en ningún OPERATIVO, BRIEF, ASSIGNMENT ni README. Esto causa que cada TL los descubra "en caliente" — gastando tiempo y creando inconsistencias.

---

## GAP-VTT-06 — `assigneeId` vs `assignedToId` (CRÍTICO)

### Síntoma

Al crear tareas con `POST /api/phases/:phaseId/tasks`:

```bash
POST /api/phases/64d9fbb4-.../tasks
{
  "title": "...",
  "assigneeId": "a3a2ce62-28d8-419d-9888-44203a963894",  ← IGNORADO
  "estimatedHours": 1,
  "complexity": "LOW",
  "category": "development"
}
```

**Response 201 OK**, pero la tarea queda creada con `assignee: null`. El campo `assigneeId` se ignora silenciosamente — no hay warning, no hay error, no hay log.

Lo mismo ocurre con `PATCH /api/tasks/:id`:

```bash
PATCH /api/tasks/VTT-704
{ "assigneeId": "abdff0db-..." }   ← Retorna 200 OK pero assignee queda null
```

### Campo correcto

`assignedToId` (en PATCH funciona; en POST también probablemente).

```bash
PATCH /api/tasks/VTT-704
{ "assignedToId": "abdff0db-..." }   ✅ Funciona
```

### Reproducción

```bash
# Crear tarea con assigneeId
TASK=$(curl -s -X POST "http://77.42.88.106:3000/api/phases/$PHASE_ID/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Test","assigneeId":"...","estimatedHours":1,"complexity":"LOW","category":"development"}')

echo "$TASK" | jq '.data.assignee'  # null  ← BUG

# Patch con assigneeId
curl -X PATCH "http://77.42.88.106:3000/api/tasks/VTT-XXX" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"assigneeId":"..."}'   # 200 OK pero assignee sigue null

# Patch con assignedToId
curl -X PATCH "http://77.42.88.106:3000/api/tasks/VTT-XXX" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"assignedToId":"..."}'  # 200 OK + assignee asignado ✅
```

### Impacto

- **Tiempo perdido por TL**: ~15 minutos cada vez que se descubre (debugging del status `Cannot move task to In Progress without an assignee`).
- **Setup que parecen correctos pero no lo están** — el TL crea 16 tareas, todas con `assigneeId`, y todas quedan sin assignee. Solo se descubre al intentar mover la primera tarea a `in_progress`.
- **Inconsistencia con documentación**: `PROCESO_ASIGNACION_TAREAS.md §"APIs del Sistema"` dice:
  ```
  PATCH /api/tasks/VTT-XXX -> body: {"assigneeId": "UUID"}
  ```
  Esto **es incorrecto** según el comportamiento real del backend.

### Workarounds aplicados

1. **PATCH posterior con `assignedToId`** después de crear cada tarea (descubierto en sesión 2026-05-16, Sprint S06-FIX-A setup, 16 tareas afectadas).

### Solución propuesta

**Opción A — Solo documentación (1h):**
- Actualizar `PROCESO_ASIGNACION_TAREAS.md` cambiando `assigneeId` por `assignedToId` en todos los ejemplos
- Agregar gotcha #1 a §18 GOTCHAS del template `OPERATIVO_TL_REVIEWER.md`:
  ```
  | 1 | POST/PATCH /tasks ignora assigneeId | Usar assignedToId — assigneeId se acepta silenciosamente pero no persiste |
  ```
- Actualizar `OPERATIVO_TL_EJECUTOR.md` §4 con la misma nota

**Opción B — Fix BE + documentación (4h):**
- Aceptar AMBOS campos en el validador Zod (`assigneeId` como alias de `assignedToId`) por retrocompatibilidad
- Loguear warning si se usa `assigneeId` ("deprecated, use assignedToId")
- En ~6 meses, deprecar `assigneeId` completamente

---

## GAP-VTT-07 — `order` duplicado en Deliveries dentro de la misma fase

### Síntoma

`POST /api/deliveries` con `order: 1` se acepta sin error aunque ya exista otro delivery con `order: 1` en la **misma fase**.

```bash
# Delivery existente
{ "phaseId": "64d9fbb4-...", "name": "PRE: Setup", "order": 1 }

# Crear nuevo
POST /api/deliveries
{ "phaseId": "64d9fbb4-...", "name": "SETUP-S06-FIX-A", "order": 1 }   ← Aceptado sin error
```

**Resultado en Gantt**: ambos deliveries pelean por la misma posición. El frontend ordena por `order ASC` y desempata de forma indefinida (alfabético, createdAt, aleatorio según implementación), causando que **alguno se muestre fuera de lugar**.

### Reproducción

```bash
TOKEN=$(...)
PHASE_ID="64d9fbb4-..."

# Crear 2 deliveries con order=99
for n in 1 2; do
  curl -X POST "http://77.42.88.106:3000/api/deliveries" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"phaseId\":\"$PHASE_ID\",\"name\":\"Test $n\",\"order\":99,\"createdBy\":\"$TL\"}"
done

# Ambos creados sin error
curl "http://77.42.88.106:3000/api/phases/$PHASE_ID/deliveries" -H "Authorization: Bearer $TOKEN" \
  | jq '.data | map(select(.order == 99))'
# Retorna 2 elementos con order=99
```

### Impacto

- **Setup S06-FIX-A**: 6 deliveries nuevos creados con `order: 1-6` chocaron con 6 deliveries preexistentes (PRE, S09, S10, BUGS S10, S11, S12). El Gantt los mostró intercalados.
- **Visualización rota** en el dashboard de Progreso por Fases — el orden de ejecución cronológica no se respeta.
- **El TL no tiene forma de validar** desde el HANDOFF/SETUP cuál es el próximo `order` disponible — tiene que hacer `GET /api/phases/:id/deliveries` y calcular `max(order) + 1`.

### Workaround aplicado

```python
# Patrón correcto que el TL debe seguir manualmente:
resp = get(f"/api/phases/{phase_id}/deliveries")
max_order = max(d['order'] for d in resp['data'])
next_order = max_order + 1
# crear deliveries con next_order, next_order+1, next_order+2, ...
```

### Solución propuesta

**Opción A — Solo documentación + script helper (1h):**
- Agregar gotcha #2 a §18 GOTCHAS del template `OPERATIVO_TL_REVIEWER.md`:
  ```
  | 2 | POST /api/deliveries no valida unicidad de order por fase | Hacer GET /phases/:id/deliveries primero y usar max(order)+1 |
  ```
- Agregar a `OPERATIVO_TL_EJECUTOR.md` §4 (Workflow SETUP-BLOQUE):
  ```
  Antes de crear deliveries:
  1. GET /api/phases/:phaseId/deliveries
  2. next_order = max(d.order for d in resp.data) + 1
  3. Asignar order incremental desde next_order
  ```

**Opción B — Fix BE + documentación (4h):**
- Agregar unique constraint `(phaseId, order)` en BD: `@@unique([phaseId, order])` en Prisma model
- Validador Zod del endpoint debe retornar 409 CONFLICT si ya existe:
  ```typescript
  { error: "Order N already used in phase X", code: "ORDER_CONFLICT" }
  ```
- O alternativamente: si `order` viene vacío, autocalcularlo como `max(order)+1`

---

## Plan de implementación

### Si PM aprueba Opción A (recomendado — 1h)

| # | Tarea | Owner |
|---|---|---|
| 1 | Actualizar `PROCESO_ASIGNACION_TAREAS.md` con `assignedToId` | TL |
| 2 | Agregar §13 GOTCHAS API a `TEMPLATE_BASE_TL_REVISOR.md` con los 2 gotchas (numeración correlativa al gotcha #8 ya existente — quedarían #9 y #10) | TL |
| 3 | Agregar nota en `TEMPLATE_BASE_TL_EJECUTOR.md` §4 Paso 8 (crear deliveries) sobre validar `max(order)+1` | TL |
| 4 | Agregar a Reglas Críticas (§9) del TL Ejecutor: "NUNCA usar `assigneeId` en POST/PATCH — siempre `assignedToId`" | TL |
| 5 | Notificar al PM para que regenere las tropicalizaciones (Memory Service `OPERATIVO_TL_REVIEWER.md`, etc.) | PM |

### Si PM aprueba Opción B (4h adicional)

Sumar al plan A:

| # | Tarea | Owner |
|---|---|---|
| 6 | Fix BE: alias `assigneeId` → `assignedToId` en validadores Zod | BE |
| 7 | Fix BE: unique constraint `(phaseId, order)` en `delivery` model + migración | DB |
| 8 | Fix BE: handler 409 CONFLICT en POST /deliveries | BE |
| 9 | Tests de regresión para ambos comportamientos | QA |

---

## Riesgos / consideraciones

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Opción B rompe scripts existentes que ya usan `assignedToId` correctamente | Baja | Aceptar AMBOS campos en transición de 6 meses |
| Opción B con unique constraint rompe deliveries históricos con `order` duplicado | Media | Auditar BD pre-migración, asignar nuevos `order` a duplicados existentes |
| Documentación que se actualiza solo no previene futuros errores en agentes IA | Alta | Los OPERATIVOs los lee el agente al inicio de sesión — la documentación SÍ funciona si está bien colocada |

---

## Decisión solicitada al PM

1. **¿Opción A (solo documentación) u Opción B (fix BE + documentación)?**
2. **Si Opción A**: ¿prioridad para esta semana o se difiere?
3. **¿Convertir en tarea VTT del Sprint actual o ir directo a IMPROVE backlog?**

---

## Referencias

- Sesión de detección: 2026-05-16, Sprint S06-FIX-A setup (Fase 11 MGP, R4)
- Tareas afectadas: VTT-704 a VTT-719 (16 tareas creadas con `assigneeId` que quedaron sin assignee)
- Deliveries afectados: 6 deliveries con `order: 1-6` que colisionaron — corregidos posteriormente a `order: 17-22`
- Endpoint API afectados:
  - `POST /api/phases/:phaseId/tasks`
  - `PATCH /api/tasks/:id`
  - `POST /api/deliveries`
- Documentos a actualizar:
  - `virtual-teams-tracking/knowledge/tl-docs/PROCESO_ASIGNACION_TAREAS.md`
  - `virtual-teams-setup/.../TEMPLATE_BASE_TL_REVISOR.md`
  - `virtual-teams-setup/.../TEMPLATE_BASE_TL_EJECUTOR.md`

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-16 | Versión inicial — propuesta de los 2 gotchas detectados durante setup S06-FIX-A |
