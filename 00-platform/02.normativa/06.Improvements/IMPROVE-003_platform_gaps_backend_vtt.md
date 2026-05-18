# IMPROVE-003 — Platform Gaps del Backend VTT

| Campo | Valor |
|---|---|
| **Código** | `IMPROVE-003` |
| **Título** | Platform Gaps del Backend VTT — 5 fixes tácticos |
| **Categoría** | Backend / API / Tactical fixes |
| **Prioridad** | 🟡 Media (2 gaps) / 🟢 Baja (3 gaps) |
| **Estimación rough** | 15 horas (~2 días) |
| **Estado** | Propuesta — pendiente de evaluación PM |
| **Autor** | TL Memory Service (`92225290-6b6b-4c1f-a940-dcb4262507aa`) |
| **Fecha** | 2026-05-13 |
| **Origen** | Cierre de MS-283, MS-284, MS-285 con modelo dinámico completo |
| **Validado contra** | Backend VTT `http://77.42.88.106:3000` (versión productiva 2026-05-13) |

---

## Relación con otras mejoras

- **IMPROVE-001 (Pool de Transacciones)**: independiente — los gaps siguen aplicando con o sin pool
- **IMPROVE-002 (BD de Manifiestos)**: cuando se implemente, resuelve naturalmente:
  - **GAP-VTT-04** (`taskId` en evidencias) → la migración de IMPROVE-002 §6 Fase 3 agrega esta columna
  - **GAP-VTT-05** (`GET /tasks/:id/trackable-items`) → las vistas materializadas lo habilitan
- **GAPs restantes** (01, 02, 03) son fixes puntuales que no dependen de IMPROVE-001/002 — pueden implementarse independientemente

---

## Resumen ejecutivo

Durante el cierre de las 3 primeras tareas del Sprint S1 (Memory Service) aplicando el workflow de modelo dinámico (crear TIs detectados → vincular evidencias → resolver devlog), detectamos **4 gaps de feature en el backend VTT** que están documentados en SOPs (`SOP-TRK-01`, `FEATURE_TRACKABLE_ITEMS`) pero no implementados, más **2 restricciones de catálogo** que limitan el uso real del modelo dinámico en proyectos `software`.

Todos tienen **workarounds operacionales aplicados** (marker textuales, downgrade de typeCode), pero ninguno es solución limpia. Este documento pide priorización para que las features queden implementadas y los workarounds se retiren.

---

## GAP-VTT-01 — Endpoint `/defer` y status `ti_deferred` no existen

### Síntoma

El SOP `SOP-TRK-01_trackable_items_workflow.md §5.5 — DIFERIR ITEM (Deferred Scope)` y `FEATURE_TRACKABLE_ITEMS.md §5.5` documentan el flujo completo de diferir items a un release futuro:

```
POST /api/trackable-items/:itemId/defer
{
  "targetType": "release",
  "targetReleaseId": "<uuid R2>",
  "reason": "...",
  "deferredBy": "<uuid>"
}
```

Y existe el endpoint de reporte:
```
GET /api/projects/:projectId/trackable-items/deferred
```

Ambos están **documentados pero devuelven 404** en producción (`http://77.42.88.106:3000`).

### Rutas probadas (todas 404)

| Método | Ruta |
|---|---|
| POST | `/api/trackable-items/:tiId/defer` |
| POST | `/api/trackable-items/:tiId/deferrals` |
| POST | `/api/trackable-items/:tiId/deferment` |
| POST | `/api/deferred-items` |
| POST | `/api/projects/:projectId/deferred-items` |
| POST | `/api/projects/:projectId/trackable-items/:tiId/defer` |
| GET | `/api/projects/:projectId/trackable-items/deferred` |

Adicionalmente, intentar `PATCH /api/trackable-items/:tiId` con `statusCode=ti_deferred` devuelve:
```json
{"success":false,"error":"Status ti_deferred no válido para trackable_item","code":"INVALID_STATUS_CODE"}
```

El status `ti_deferred` no existe en el catálogo de estados.

### Impacto

- Los tech_debts identificados durante una tarea no pueden marcarse formalmente como diferidos al R2.
- El reporte de cobertura R1 vs R2 no se puede generar (queda dentro de la tabla `trackable_item_deferrals` que tampoco se puede consultar).
- Auditoría de scope diferido depende de leer manifests JSON manualmente.

### Workaround aplicado en S1

Marker textual en `title` y `description`:
- `title`: `[DEFER R2] <título>`
- `description`: `[Deferred to R2] <razón> ...`

Los TIs quedan en `statusCode=ti_draft` con el marker. Sin trazabilidad estructurada.

### Solución pedida

1. Implementar `POST /api/trackable-items/:tiId/defer` según `FEATURE_TRACKABLE_ITEMS.md §5.5`.
2. Agregar status `ti_deferred` al catálogo (`trackable_item_statuses`).
3. Implementar `GET /api/projects/:projectId/trackable-items/deferred`.
4. Migración de datos: detectar TIs con `[DEFER R2]` en title/description y crear registros en `trackable_item_deferrals` retroactivamente.

### Prioridad sugerida

🟡 **Media** — Necesario antes de cerrar Sprint S1 (firma de stage) si queremos reporte limpio de scope diferido al R2.

---

## GAP-VTT-02 — `typeCode = process_improvement` no válido para project_type `software`

### Síntoma

Al intentar crear un TI tipo `process_improvement` en un proyecto `software`:

```
POST /api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803/trackable-items
{
  "code": "PROC-SECRETS-01",
  "typeCode": "process_improvement",
  "title": "...",
  "description": "...",
  "statusCode": "ti_draft",
  "createdById": "..."
}
```

Respuesta:
```json
{"success":false,"error":"Type process_improvement not valid for project type software","code":"INVALID_TYPE_CODE"}
```

### TypeCodes válidos hoy para `software` (validado contra TIs existentes)

`adr | assumption | business_rule | constraint | rf | rnf | tech_debt | use_case | user_story`

### TypeCodes probados y rechazados

`process_improvement | process | improvement | pattern | best_practice | lesson_learned`

### Impacto

- Mejoras de proceso identificadas durante ejecución (gobierno, workflow, política operativa) no tienen typeCode propio.
- Se mezclan con `tech_debt` rompiendo la semántica del modelo.
- Reportes de "qué mejoras de proceso identificamos en R1" no son segmentables.

### Workaround aplicado en S1

Crear como `tech_debt` con marker `[PROCESS]` en title + `[Subtype: process_improvement]` en description.

Ejemplo aplicado en MS-285:
- `PROC-SECRETS-01` (canal seguro PM→Servidor)
- `PROC-REVIEW-01` (Review Gate exige code_logic)

Ambos viven como `tech_debt` pero conceptualmente son mejoras de proceso.

### Solución pedida

Agregar `process_improvement` como typeCode válido para `projectType=software` en la matriz `trackable_item_types × project_types`.

Opcional: agregar también `pattern`, `lesson_learned` para tener vocabulario completo del modelo dinámico.

### Prioridad sugerida

🟢 **Baja** — Workaround funciona; limpieza semántica.

---

## GAP-VTT-03 — DELETE de evidencias no existe

### Síntoma

Rutas probadas (todas 404):

| Método | Ruta |
|---|---|
| DELETE | `/api/trackable-item-evidences/:eid` (según `FEATURE_TRACKABLE_ITEMS.md §6 Endpoints`) |
| DELETE | `/api/trackable-items/:tiId/evidence/:eid` |

### Impacto

- Si una evidencia se crea con título mal formateado (sin marker `[TASK:MS-XXX]`), no se puede corregir.
- Las TIs acumulan evidencias duplicadas o legacy cuando se aplica el patrón retroactivamente.
- Hoy NFR-SEC-05 tiene 8 evidencias: 4 con marker estándar (válidas) + 4 legacy sin marker (basura visual).

### Workaround aplicado en S1

Dejar evidencias mal formateadas como "legacy" y agregar las correctas. Los manifests documentan cuáles son las válidas.

### Solución pedida

Implementar `DELETE /api/trackable-item-evidences/:eid` con autorización: solo el `createdBy` o un rol con permiso `evidence.delete`.

### Prioridad sugerida

🟢 **Baja** — Cosmético hasta que tengamos auditorías formales.

---

## GAP-VTT-04 — Falta campo `taskId` (FK) en `trackable_item_evidences`

### Síntoma

El schema actual de `trackable_item_evidences`:

```sql
CREATE TABLE trackable_item_evidences (
  id TEXT PRIMARY KEY,
  trackable_item_id TEXT NOT NULL REFERENCES trackable_items(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  url TEXT,
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);
```

No tiene `task_id`. Las evidencias se vinculan a una TI pero no se sabe **de qué tarea** vino la evidencia.

### Impacto

- Al ver pantalla de TI con 8 evidencias: no se sabe a simple vista qué tarea aportó cada una.
- No se puede filtrar evidencias por tarea desde la API sin parsear el texto del title/description.
- Reportes "qué evidencias dejó MS-285" requieren cruce manual.

### Workaround aplicado en S1

Marker estructurado en title + description (formato estándar del SKL-DYNAMIC-MODEL-01):

```json
{
  "type": "link",
  "title": "[MS-285] [S1] docs/SECRETS.md + 8 GH Secrets",
  "url": "https://github.com/NCoreSys/memory-service-backend/pull/15",
  "description": "[TASK:MS-285] [SPRINT:S1] PR #15 — docs/SECRETS.md (336 lineas)..."
}
```

Filtrado en cliente con regex sobre `description`.

### Solución pedida

1. **Migración:** agregar columna opcional `task_id TEXT REFERENCES tasks(id)` a `trackable_item_evidences`.
2. **Endpoint POST:** aceptar campo opcional `taskId` en el body.
3. **Endpoint GET:** soportar query param `?taskId=MS-285` para filtrar.
4. **Migración de datos:** parsear `[TASK:MS-XXX]` de los existing y backfillear.

### Prioridad sugerida

🟡 **Media** — Es el campo más útil para reportería del modelo dinámico. Sin esto, el filtrado por tarea queda en cliente.

---

## GAP-VTT-05 (bonus) — Endpoint `/api/tasks/:id/trackable-items` no existe

### Síntoma

```
GET /api/tasks/MS-285/trackable-items
→ 404
```

### Impacto

Para saber qué TIs están vinculadas a una tarea hay que iterar **todos los TIs del proyecto** y buscar la tarea en cada uno (`GET /api/projects/:projectId/trackable-items?limit=300` + filtrar localmente).

### Solución pedida

Implementar `GET /api/tasks/:taskId/trackable-items` que devuelva lista de TIs vinculadas con su `linkType`.

### Prioridad sugerida

🟢 **Baja** — Workaround viable; conveniencia API.

---

## Resumen de gaps y prioridad

| ID | Gap | Prioridad | Workaround disponible |
|---|---|---|---|
| GAP-VTT-01 | `/defer` + `ti_deferred` status | 🟡 Media | ⚠️ Marker textual `[DEFER R2]` |
| GAP-VTT-02 | typeCode `process_improvement` software | 🟢 Baja | ⚠️ `tech_debt` + `[PROCESS]` marker |
| GAP-VTT-03 | DELETE evidencias | 🟢 Baja | ⚠️ Dejar legacy + agregar nuevas |
| GAP-VTT-04 | Campo `taskId` en evidencias | 🟡 Media | ⚠️ Marker `[TASK:MS-XXX]` en description |
| GAP-VTT-05 | `GET /tasks/:id/trackable-items` | 🟢 Baja | ⚠️ Iterar TIs del proyecto |

---

## Endpoints validados correctamente durante operación S1 (no son gaps)

Para que el equipo VTT tenga claridad sobre lo que sí funciona:

| Endpoint | Estado |
|---|---|
| `POST /api/projects/:projectId/trackable-items` | ✅ OK (scoped, no global) |
| `GET /api/projects/:projectId/trackable-items` | ✅ OK con query params |
| `GET /api/trackable-items/:tiId` | ✅ OK |
| `PATCH /api/trackable-items/:tiId` | ✅ OK |
| `DELETE /api/trackable-items/:tiId` | ✅ OK |
| `POST /api/trackable-items/:tiId/tasks` | ✅ OK (vincular) |
| `POST /api/trackable-items/:tiId/evidence` | ✅ OK (singular, no /evidences) |
| `GET /api/trackable-items/:tiId/evidence` | ✅ OK |
| `GET /api/tasks/:taskId/devlog` | ✅ OK (singular) |
| `POST /api/tasks/:taskId/devlog-entries` | ✅ OK (plural) |
| `PATCH /api/tasks/:taskId/devlog/:eid/status` | ✅ OK (requiere `resolution` si status=resolved/wont_fix) |
| `GET /api/tasks/:taskId/review-gate` | ✅ OK |

---

## Tareas sugeridas para VTT backlog

Si el equipo VTT decide trabajar estos gaps, las tareas propuestas son:

| ID sugerido | Tarea | Prioridad | Estimación |
|---|---|---|---|
| VTT-FIX-DEFER-01 | Implementar `/defer` + status `ti_deferred` + `GET /deferred` | 🟡 Media | 6h |
| VTT-FIX-EVD-TASK-01 | Agregar `task_id` a `trackable_item_evidences` + endpoint filter | 🟡 Media | 4h |
| VTT-FIX-TYPECODE-01 | Habilitar `process_improvement` para software projects | 🟢 Baja | 2h |
| VTT-FIX-EVD-DELETE-01 | Implementar `DELETE /trackable-item-evidences/:eid` | 🟢 Baja | 2h |
| VTT-FIX-TASK-TI-01 | Endpoint `GET /tasks/:id/trackable-items` | 🟢 Baja | 1h |

**Total estimado:** 15h (~2 días)

---

## Decisión solicitada al PM

1. ¿Subir este documento como `ProjectDocument` al proyecto VTT (no a memory-service) para que quede como input para su backlog?
2. ¿Crear las 5 tareas VTT-FIX-* en el proyecto VTT con prioridades sugeridas?
3. ¿Mantener los workarounds en SKL-DYNAMIC-MODEL-01 mientras tanto?
4. ¿Implementar estos fixes **antes** o **después** de IMPROVE-001 y IMPROVE-002?
   - Recomendación: los 3 gaps independientes (01, 02, 03) ahora (2 días); los gaps 04 y 05 se difieren si IMPROVE-002 entra en roadmap.

---

## Referencias

- Documento maestro (esta copia): `virtual-teams-setup/00-platform/07.Normativa/IMPROVEMENTS/IMPROVE-003_platform_gaps_backend_vtt.md`
- Copia original del reporte: `memory-service-project/knowledge/platform-feedback/VTT_PLATFORM_GAPS_2026-05-13.md`
- Subido a VTT como ProjectDocument: `c20eda2c` (documentType: `reference`, proyecto Memory Service)
- Mejoras relacionadas:
  - `IMPROVE-001_pool_transacciones_vtt.md` (independiente)
  - `IMPROVE-002_bd_manifiestos_y_tis.md` (resuelve GAP-VTT-04 y GAP-VTT-05 al implementarse)
- SOPs documentados pero no implementados:
  - `SOP-TRK-01_trackable_items_workflow.md §5.5`
  - `FEATURE_TRACKABLE_ITEMS.md §5.5`

## Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Documento inicial — reportado como VTT_PLATFORM_GAPS desde TL Memory Service |
| 1.1 | 2026-05-13 | Migrado a IMPROVEMENTS/ con metadata estandarizada + referencias cruzadas a IMPROVE-001 y IMPROVE-002 |
