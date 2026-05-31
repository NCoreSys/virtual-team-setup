# SKL-TASK-01: Crear Tarea en VTT

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-TASK-001_crear_tarea.md`** en `02.normativa/03.Skills/task/`.
> Migración 1:1, contrato sin cambios. Esta versión se conserva como referencia histórica.


**Categoría:** VTT-TASK  
**Aplica a:** TL  
**Tokens estimados:** ~180  
**Cuándo:** FASE 1 — al crear una tarea nueva en VTT a partir de un handoff

---

## Precondición

- `$TOKEN` obtenido (SKL-AUTH-01)
- Handoff del PM/PJM leído y analizado
- BRIEF escrito y guardado en `knowledge/agent-tasks/briefs/BRIEF_$TASK_ID_$SLUG.md`

---

## Reglas obligatorias antes de ejecutar

### R1 — Delivery obligatorio (ninguna tarea huérfana)
Toda tarea debe pertenecer a un Delivery. Antes de crear la tarea:
- Si el Delivery del sprint/grupo ya existe → usar su `$DELIVERY_ID`
- Si no existe → crear primero con el endpoint de Deliveries
- Si la tarea es un **bug** → asignarla al Delivery `BUGS` de su fase (existe en todas las fases)

```bash
# Crear Delivery si no existe
curl -s -X POST "$VTT_BASE_URL/api/deliveries" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"phaseId\": \"$PHASE_ID\",
    \"name\": \"$DELIVERY_NAME\",
    \"order\": $DELIVERY_ORDER,
    \"createdBy\": \"$AGENT_UUID\",
    \"statusId\": \"$STATUS_PENDING_UUID\"
  }"
```

### R2 — Dependencias obligatorias (ninguna tarea sin dependencia)
Toda tarea debe tener al menos una dependencia. Analizar:

| Origen de la tarea | Dependencia lógica |
|--------------------|--------------------|
| Sale de análisis/gap detectado en otra tarea | Esa tarea origen |
| Es un bug | La tarea donde se detectó el bug |
| Es la primera de su fase | La última tarea completada de la fase anterior |
| No hay dependencia obvia | **Confirmar con PM antes de crear** |

---

## Variables requeridas

- `$TOKEN` — JWT (SKL-AUTH-01)
- `$PHASE_ID` — UUID de la fase donde va la tarea
- `$DELIVERY_ID` — UUID del Delivery al que pertenece
- `$TASK_TITLE` — título descriptivo
- `$TASK_DESCRIPTION` — descripción (máx 2000 chars)
- `$STATUS_PENDING_UUID` — `335fd9c6-f0d6-4966-a6ea-f518c78bc422`
- `$PRIORITY_UUID` — UUID de prioridad (ver catálogo de prioridades)
- `$COMPLEXITY` — `LOW`, `MEDIUM` o `HIGH` (mayúsculas obligatorio)
- `$CATEGORY` — `development`, `design`, `testing`, `documentation`, `review`, `bugfix`, `deployment`
- `$ESTIMATED_HOURS` — número
- `$ASSIGNEE_UUID` — UUID del agente ejecutor
- `$AGENT_UUID` — UUID del TL (quien crea)

---

## Ejecución

### Paso 1 — Crear la tarea
```bash
TASK_RESPONSE=$(curl -s -X POST "$VTT_BASE_URL/api/phases/$PHASE_ID/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"title\": \"$TASK_TITLE\",
    \"description\": \"$TASK_DESCRIPTION\",
    \"statusId\": \"$STATUS_PENDING_UUID\",
    \"priorityId\": \"$PRIORITY_UUID\",
    \"estimatedHours\": $ESTIMATED_HOURS,
    \"assignedToId\": \"$ASSIGNEE_UUID\",
    \"assignedBy\": \"$AGENT_UUID\",
    \"category\": \"$CATEGORY\",
    \"complexity\": \"$COMPLEXITY\",
    \"createdBy\": \"$AGENT_UUID\"
  }")
TASK_ID=$(echo $TASK_RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
echo "Tarea creada: $TASK_ID"
```

### Paso 2 — Asignar al Delivery
```bash
curl -s -X POST "$VTT_BASE_URL/api/deliveries/$DELIVERY_ID/tasks/$TASK_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"assignedBy\": \"$AGENT_UUID\"}"
```

### Paso 3 — Agregar dependencias
```bash
# Repetir por cada dependencia
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/dependencies" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"dependsOnTaskId\": \"$DEPENDS_ON_TASK_ID\"}"
```

### Paso 4 — Subir BRIEF como attachment
```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/briefs/BRIEF_${TASK_ID}_${TASK_SLUG}.md" \
  -F "fileType=brief" \
  -F "uploadedById=$AGENT_UUID"
```

---

## Validación

- Paso 1: response incluye `data.id` → guardar como `$TASK_ID`
- Paso 2: HTTP 200/201
- Paso 3: HTTP 201. Si devuelve `CIRCULAR_DEPENDENCY` → revisar cadena de dependencias
- Paso 4: HTTP 201, response incluye `id` del attachment

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Campo ignorado silenciosamente | Usar `assignedTo` en vez de `assignedToId` | Usar `assignedToId` |
| 400 `too_big` | `description` > 2000 chars | Recortar descripción |
| 400 `VALIDATION_ERROR` | `complexity` en minúsculas | Usar `LOW`, `MEDIUM`, `HIGH` |
| `CIRCULAR_DEPENDENCY` | Dependencia circular | Revisar cadena, consultar PM |
| 409 `PHASE_HAS_ACTIVE_TASKS` | Intento de DELETE phase con tareas | No eliminar fases con tareas |
| Sin dependencias | No se analizaron dependencias | Volver a R2 antes de crear |
