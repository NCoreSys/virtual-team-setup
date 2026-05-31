# VTT.SKILL-TASK-001 — Crear Tarea en VTT

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-TASK-001` |
| **Categoría** | TASK (Task CRUD) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | TL (creador principal), PJM (setup inicial de sprint) |
| **Tokens estimados** | ~400 |
| **Cuándo se usa** | FASE 1 del PROTOCOL-ASG-001 §5.1.7 — al crear una tarea nueva en VTT a partir de un handoff |
| **Reemplaza** | `SKL-TASK-01_crear-tarea.md` (legacy en `_pending-migration/vtt-task/`) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `phase_id` | uuid | sí | UUID de la fase donde va la tarea |
| `delivery_id` | uuid | sí | UUID del Delivery — toda tarea pertenece a uno (R1) |
| `title` | string | sí | Título descriptivo de la tarea |
| `description` | string ≤2000 | sí | Descripción de la tarea (truncar si excede) |
| `priority_id` | uuid | sí | UUID de prioridad — ver catálogo de prioridades de VTT |
| `complexity` | enum `LOW`/`MEDIUM`/`HIGH` | sí | Mayúsculas obligatorio |
| `category` | enum | sí | `development`, `design`, `testing`, `documentation`, `review`, `bugfix`, `deployment` |
| `estimated_hours` | number | sí | Estimación en horas |
| `assignee_uuid` | uuid | sí | UUID del agente al que se le asignará |
| `creator_uuid` | uuid | sí | UUID del TL que crea (típicamente él mismo) |
| `brief_path` | path | sí | Ruta local al BRIEF (`knowledge/agent-tasks/briefs/<phase>/<sprint>/BRIEF_<TASK_ID>_<slug>.md`) |
| `task_slug` | string snake_case | sí | Slug para naming de archivos |
| `dependencies` | array<uuid> | sí | UUIDs de tareas predecesoras — mínimo 1 (R2) |

> **Política contractual:** las 12 entradas son obligatorias. NO se permite crear tarea con `dependencies=[]` salvo excepciones documentadas con el PM.

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Handoff del PM/PJM leído y analizado
- BRIEF escrito y guardado en `knowledge/agent-tasks/briefs/<phase>/<sprint>/`
- Delivery destino existe (si no — crear primero, ver §Reglas R1)

---

## Variables del entorno

```bash
$TOKEN              # JWT (VTT.SKILL-AUTH-001)
$VTT_BASE_URL       # default http://77.42.88.106:3000
$AGENT_UUID         # UUID del TL que ejecuta
$STATUS_PENDING_UUID  # 335fd9c6-f0d6-4966-a6ea-f518c78bc422 (fijo en backend VTT)
```

---

## Reglas obligatorias antes de ejecutar

### R1 — Delivery obligatorio (ninguna tarea huérfana)

Toda tarea pertenece a un Delivery. Decisión:

| Caso | Acción |
|---|---|
| Delivery del sprint/grupo existe | Usar su `delivery_id` |
| No existe | Crear primero con `POST /api/deliveries` (ver §Ejecución) |
| La tarea es un **bug** | Usar el Delivery `BUGS` de su fase (existe en todas las fases) |

### R2 — Dependencias obligatorias (ninguna tarea sin dependencia)

Toda tarea tiene ≥1 dependencia. Tabla de origen → dependencia lógica:

| Origen | Dependencia |
|---|---|
| Sale de análisis/gap en otra tarea | La tarea origen |
| Es un bug | La tarea donde se detectó el bug |
| Es la primera de su fase | La última tarea aprobada de la fase anterior |
| No hay dependencia obvia | **Confirmar con PM** antes de crear |

---

## Ejecución

### Paso 0 — (Opcional) Crear Delivery si no existe

```bash
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

TASK_ID=$(echo $TASK_RESPONSE | python -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
echo "Tarea creada: $TASK_ID"
```

### Paso 2 — Asignar al Delivery

```bash
curl -s -X POST "$VTT_BASE_URL/api/deliveries/$DELIVERY_ID/tasks/$TASK_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"assignedBy\": \"$AGENT_UUID\"}"
```

### Paso 3 — Agregar dependencias (loop por cada una)

```bash
for DEPENDS_ON in "${DEPENDENCIES[@]}"; do
    curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/dependencies" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d "{\"dependsOnTaskId\": \"$DEPENDS_ON\"}"
done
```

### Paso 4 — Subir BRIEF como attachment

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$BRIEF_PATH" \
  -F "fileType=brief" \
  -F "uploadedById=$AGENT_UUID"
```

---

## Validación

```bash
# Check 1: task creada con ID
[ -n "$TASK_ID" ] && echo "OK: TASK_ID=$TASK_ID"

# Check 2: tarea pertenece al delivery
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; d=json.load(sys.stdin)['data']; print(f\"Delivery: {d.get('deliveryId')}\")"

# Check 3: dependencias registradas
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/dependencies" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print(f\"Deps: {len(json.load(sys.stdin)['data'])}\")"

# Check 4: brief attachment presente
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; ats=json.load(sys.stdin)['data']; print('brief:' , any(a['fileType']=='brief' for a in ats))"
```

**Esperado:** `OK: TASK_ID=...`, `Delivery: <uuid>`, `Deps: >=1`, `brief: True`.

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Campo ignorado silenciosamente | Usar `assignedTo` en vez de `assignedToId` | Usar `assignedToId` exacto |
| HTTP 400 `too_big` | `description` > 2000 chars | Recortar a ≤2000 o mover detalles al BRIEF |
| HTTP 400 `VALIDATION_ERROR` complexity | `complexity` en minúsculas | Usar `LOW`/`MEDIUM`/`HIGH` mayúsculas |
| HTTP 409 `CIRCULAR_DEPENDENCY` | Dependencia circular en cadena | Revisar el grafo de deps, consultar PM |
| HTTP 409 `PHASE_HAS_ACTIVE_TASKS` | Intento de DELETE phase con tareas | No eliminar fases con tareas activas |
| Tarea sin dependencias | No se aplicó R2 | Volver y confirmar con PM antes de retry |
| HTTP 400 attachment brief | `uploadedById` faltante en multipart | Agregar campo `-F "uploadedById=$AGENT_UUID"` |

---

## Scripts invocados

Ninguno — lógica inline en bash/curl ≤4 endpoints.

> Si en el futuro se requiere bulk-create (crear N tareas de un sprint en una sola llamada), generar `VTT.SCRIPT-TASK-001_crear_tareas_bulk.py`.

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — para obtener `$TOKEN`
- (al terminar) `VTT.SKILL-TASK-002_generar_assignment` — siguiente paso del flujo de asignación

---

## Cuándo NO usar esta Skill

- **Si la tarea es de un sprint legacy ya en curso** — usar la UI del PM, no crear vía API
- **Si no tenés `assignee_uuid` definido aún** — esperar a que el PM/PJM lo asigne

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-TASK-01_crear-tarea.md`. Mantiene contrato funcional. Ampliación: tabla de Inputs contractuales (12 fields), separación de R1/R2 en sección dedicada, 4 checks de validación, 7 errores comunes documentados. |
