# IMPROVE-002 — Base de Datos para Manifiestos y TrackableItems

| Campo | Valor |
|---|---|
| **Código** | `IMPROVE-002` |
| **Título** | Base de Datos para Manifiestos y TrackableItems (consultable, queryable) |
| **Categoría** | Infrastructure / Database / Reporting |
| **Prioridad** | 🟡 Media |
| **Estimación rough** | 6-8 días (+1 día vs original por tabla `manifest_operations` y vista derivada) |
| **Estado** | Propuesta — pendiente de evaluación PM |
| **Autor** | PM Martin Rivas |
| **Fecha** | 2026-05-13 |
| **Última actualización** | 2026-05-17 — incorpora manifest schema v1.1 (bloque DevOps) |
| **Origen** | Sesión TL Memory Service — discusión sobre archivos JSON con metadata de TIs y manifests por tarea |
| **Schemas soportados** | Manifest **v1.0** y **v1.1** (con bloque `delivery.operations`) |

---

## 1. Problema que resuelve

Hoy los **Task Manifests** y la metadata operativa de los **TrackableItems** viven en dos formatos no queryables:

### Manifests
- Vivien como **JSON files en disco** (`knowledge/task-manifests/[fase]/[sprint]/MS-XXX.json`)
- Y como **attachments en VTT** (`fileType=manifest`)
- Pero **no hay tabla `manifests`** que los indexe

### TrackableItems metadata
- Existe el catálogo `ms_trackable_items.json` (210 items) en `c:/tmp/`
- Se consulta por filename + grep — no por query estructurada
- La metadata enriquecida (evidencias agregadas, status real, deferred, etc.) está fragmentada entre:
  - Tabla `trackable_items` de VTT (datos base)
  - Tabla `trackable_item_evidences` (evidencias)
  - Tablas separadas para `deferrals`, `links`, etc.
  - Manifests JSON con el bloque `dynamic_model_actions`

### Consecuencias

| Pregunta operativa | Hoy se responde con | Tiempo |
|---|---|---|
| "¿Qué tareas cerradas tienen tech_debt vinculado para R2?" | Iterar JSON manifests + cruzar con TIs | ~10 min manual |
| "¿Cuántas evidencias se agregaron en S1?" | Sumar `evidences_added.length` en cada manifest | ~5 min manual |
| "¿Qué TIs no tienen evidencias?" | GET cada TI uno por uno | ~30 min |
| "¿Velocity real del agente DO en S1?" | Leer cada manifest + calcular `actual_hours` | ~15 min |
| "¿Qué tareas mencionaron LD-12?" | grep en todos los manifests | ~3 min |

Para un proyecto pequeño es manejable. Para un proyecto con **100+ tareas** o **multi-proyecto** se vuelve insostenible.

## 2. Impacto / valor que aporta

### Cuantitativo
- **Reportes de cierre de sprint**: de 30 min manuales → 30 segundos (query SQL)
- **Velocity por agente**: actualizable en tiempo real
- **Audit trail** para auditoría externa: consulta única en vez de inspección de archivos
- **Dashboard del PM**: posible solo con BD consultable

### Cualitativo
- **Manifests dejan de ser dead-end** — se convierten en fuente de verdad de la entrega
- **Reportes ad-hoc** por filtros (TI, sprint, agente, severidad de devlog, etc.)
- **Compliance** facilitado (queries en vez de inspección manual)
- **Métricas de proceso** medibles (% tareas con tech_debt, % evidencias con marker correcto, etc.)

## 3. Concepto / Solución propuesta

### Arquitectura

```
┌────────────────────────────────────────────────────────────────┐
│ MANIFEST DB (Postgres)                                          │
│                                                                 │
│  Tabla: manifests                                               │
│    - manifest_id (uuid)                                         │
│    - task_id (FK a VTT tasks)                                   │
│    - schema_version                                             │
│    - generated_at                                               │
│    - generated_by (FK users)                                    │
│    - status (draft|published|superseded)                        │
│    - current_version_number                                     │
│    - json_payload (JSONB) — el manifest completo                │
│                                                                 │
│  Tabla: manifest_versions                                       │
│    - manifest_version_id                                        │
│    - manifest_id (FK)                                           │
│    - version_number (1.0, 1.5, 1.6, etc.)                       │
│    - created_at                                                 │
│    - changed_block (review.tl_review, delivery.x, etc.)         │
│    - json_payload (snapshot)                                    │
│                                                                 │
│  Tabla: manifest_indexes (vistas materializadas o columnas)     │
│    - task_id                                                    │
│    - sprint_id                                                  │
│    - implements_codes[] — array desde JSON                      │
│    - related_to_codes[]                                         │
│    - tech_debt_count                                            │
│    - criteria_met_ratio                                         │
│    - devlog_resolved_count                                      │
│    - evidences_added_count                                      │
│    - verdict (approved|rejected|pending)                        │
│    - dynamic_model_applied (bool)                               │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ TRACKABLE ITEMS DB (extender el actual)                         │
│                                                                 │
│  Tabla: trackable_items (ya existe — agregar columnas)          │
│    - + tags (TEXT[]) — para markers [DEFER R2], [PROCESS], etc. │
│    - + last_evidence_at                                         │
│    - + evidences_count (cached)                                 │
│    - + tasks_count (cached)                                     │
│                                                                 │
│  Tabla: trackable_item_evidences (agregar columnas)             │
│    - + task_id (FK opcional) ← gap GAP-VTT-04                   │
│    - + sprint_id (FK opcional)                                  │
│    - + parsed_marker (JSONB) — extraído de description          │
│                                                                 │
│  Vista materializada: v_trackable_items_with_metadata           │
│    - código, título, tipo                                       │
│    - tareas vinculadas (array)                                  │
│    - evidencias por task (array)                                │
│    - estado deferred                                            │
│    - markers detectados                                         │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ INGESTOR / SYNC                                                 │
│                                                                 │
│  Cron / Webhook que escucha:                                    │
│    - POST /api/tasks/:id/attachments con fileType=manifest      │
│  → parsea JSON                                                  │
│  → inserta/actualiza en manifests + manifest_versions           │
│  → recalcula manifest_indexes                                   │
│                                                                 │
│  Cron / Webhook que escucha:                                    │
│    - POST /api/trackable-items/:id/evidence                     │
│  → parsea marker [TASK:MS-XXX] [SPRINT:SX]                      │
│  → actualiza columnas task_id, sprint_id, parsed_marker         │
└────────────────────────────────────────────────────────────────┘
```

### Schema SQL inicial

```sql
-- Manifests
CREATE TABLE manifests (
  manifest_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id TEXT NOT NULL,
  schema_version TEXT NOT NULL DEFAULT '1.0',
  generated_at TIMESTAMPTZ NOT NULL,
  generated_by UUID NOT NULL,
  status TEXT NOT NULL DEFAULT 'published',  -- draft|published|superseded
  current_version_number TEXT NOT NULL,
  json_payload JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(task_id, status) WHERE status = 'published'
);

CREATE INDEX idx_manifests_task ON manifests(task_id);
CREATE INDEX idx_manifests_status ON manifests(status);
CREATE INDEX idx_manifests_json_gin ON manifests USING GIN (json_payload);

-- Histórico de versiones
CREATE TABLE manifest_versions (
  manifest_version_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  manifest_id UUID NOT NULL REFERENCES manifests(manifest_id) ON DELETE CASCADE,
  version_number TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  changed_block TEXT,
  json_payload JSONB NOT NULL,

  UNIQUE(manifest_id, version_number)
);

-- Índices derivados del manifest (para queries rápidas)
CREATE MATERIALIZED VIEW manifest_indexes AS
SELECT
  m.task_id,
  m.json_payload->'task'->>'sprint'->>'id' AS sprint_id,
  m.json_payload->'task'->>'assignee'->>'id' AS assignee_id,
  m.json_payload->'task'->>'category' AS category,
  m.json_payload->'review'->'tl_review'->>'verdict' AS verdict,
  (m.json_payload->'delivery'->'criteria_summary'->>'met')::INT AS criteria_met,
  (m.json_payload->'delivery'->'criteria_summary'->>'total')::INT AS criteria_total,
  (m.json_payload->'delivery'->'devlog_summary'->>'total')::INT AS devlog_total,
  m.json_payload->'delivery'->'dynamic_model_actions'->>'devlog_resolved_count' AS devlog_resolved,
  jsonb_array_length(
    COALESCE(m.json_payload->'delivery'->'dynamic_model_actions'->'evidences_added', '[]'::jsonb)
  ) AS evidences_added_count,
  jsonb_array_length(
    COALESCE(m.json_payload->'delivery'->'tech_debt_for_r2', '[]'::jsonb)
  ) AS tech_debt_count,
  ARRAY(
    SELECT jsonb_array_elements_text(
      COALESCE(m.json_payload->'indexes'->'implements_codes', '[]'::jsonb)
    )
  ) AS implements_codes,
  ARRAY(
    SELECT jsonb_array_elements_text(
      COALESCE(m.json_payload->'indexes'->'related_to_codes', '[]'::jsonb)
    )
  ) AS related_to_codes,
  m.generated_at,
  m.updated_at
FROM manifests m
WHERE m.status = 'published';

CREATE INDEX idx_manifest_indexes_sprint ON manifest_indexes(sprint_id);
CREATE INDEX idx_manifest_indexes_assignee ON manifest_indexes(assignee_id);
CREATE INDEX idx_manifest_indexes_verdict ON manifest_indexes(verdict);
```

### Tabla `manifest_operations` (NUEVA — schema v1.1)

Tabla derivada para tareas DevOps/operación que tienen bloque `delivery.operations`:

```sql
CREATE TABLE manifest_operations (
  operation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  manifest_id UUID NOT NULL REFERENCES manifests(manifest_id) ON DELETE CASCADE,
  task_id TEXT NOT NULL,

  -- Tipo y entorno
  operation_type TEXT NOT NULL,            -- sql_migration|deploy|rollback|config_change|smoke_test|restart_service
  environment TEXT NOT NULL,               -- production|staging|local
  executed_at TIMESTAMPTZ NOT NULL,
  executed_by UUID NOT NULL,

  -- Comandos ejecutados
  sql_applied TEXT,                        -- NULL si no aplica
  commands_applied JSONB,                  -- array de strings

  -- Validaciones
  pre_checks JSONB,                        -- array de {check, result}
  post_checks_passed BOOLEAN NOT NULL,
  post_checks_details JSONB NOT NULL,      -- array de {check, result}

  -- Trazabilidad
  issue_resolved UUID,                     -- FK a issues si aplica
  rollback_plan TEXT,
  rejection_history TEXT,                  -- si es re-entrega

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_manifest_operations_task ON manifest_operations(task_id);
CREATE INDEX idx_manifest_operations_type ON manifest_operations(operation_type);
CREATE INDEX idx_manifest_operations_env ON manifest_operations(environment);
CREATE INDEX idx_manifest_operations_issue ON manifest_operations(issue_resolved) WHERE issue_resolved IS NOT NULL;
```

### Vista materializada `v_devops_audit_trail`

Para auditoría de cambios en producción:

```sql
CREATE MATERIALIZED VIEW v_devops_audit_trail AS
SELECT
  mo.task_id,
  m.json_payload->'task'->>'title' AS task_title,
  mo.operation_type,
  mo.environment,
  mo.executed_at,
  mo.executed_by,
  mo.sql_applied,
  mo.post_checks_passed,
  mo.issue_resolved,
  mo.rejection_history IS NOT NULL AS is_reentrega,
  m.json_payload->'review'->'tl_review'->>'verdict' AS tl_verdict,
  m.json_payload->'review'->'pm_approval'->>'approved_at' AS pm_approved_at
FROM manifest_operations mo
JOIN manifests m ON m.manifest_id = mo.manifest_id
WHERE m.status = 'published'
ORDER BY mo.executed_at DESC;

CREATE INDEX idx_devops_audit_trail_env ON v_devops_audit_trail(environment, executed_at DESC);
```

### Ingestor: parseo de bloque `operations`

El ingestor (cron/webhook) detecta `schema_version >= "1.1"` y `delivery.operations` no-null:

```python
def ingest_operations_block(manifest_id, json_payload):
    """Si el manifest tiene delivery.operations, insertar en manifest_operations."""
    ops = json_payload.get('delivery', {}).get('operations')
    if not ops:
        return  # Tarea normal sin operations

    db.execute("""
        INSERT INTO manifest_operations (
          manifest_id, task_id, operation_type, environment,
          executed_at, executed_by,
          sql_applied, commands_applied,
          pre_checks, post_checks_passed, post_checks_details,
          issue_resolved, rollback_plan, rejection_history
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (manifest_id) DO UPDATE SET ...
    """, (
        manifest_id,
        json_payload['manifest_id'],
        ops['type'],
        ops['environment'],
        ops['executed_at'],
        ops['executed_by'],
        ops.get('sql_applied'),
        json.dumps(ops.get('commands_applied', [])),
        json.dumps(ops.get('pre_checks', [])),
        ops['post_checks_passed'],
        json.dumps(ops['post_checks_details']),
        ops.get('issue_resolved'),
        ops.get('rollback_plan'),
        ops.get('rejection_history'),
    ))
```

### Queries habilitadas (ejemplos)

```sql
-- ¿Qué tareas cerradas tienen tech_debt para R2?
SELECT task_id, tech_debt_count, related_to_codes
FROM manifest_indexes
WHERE tech_debt_count > 0
  AND verdict = 'approved'
ORDER BY tech_debt_count DESC;

-- ¿Cuántas evidencias se agregaron en S1?
SELECT SUM(evidences_added_count)
FROM manifest_indexes
WHERE sprint_id = '6f2d4310-0b3c-40b7-b2fb-088143deb4f2';

-- ¿Qué TIs no tienen evidencias?
SELECT code, title
FROM trackable_items ti
WHERE NOT EXISTS (
  SELECT 1 FROM trackable_item_evidences ev
  WHERE ev.trackable_item_id = ti.id
);

-- Velocity del agente DO en S1
SELECT
  COUNT(*) AS tareas_completadas,
  AVG((json_payload->'task'->>'estimated_hours')::numeric) AS estim_promedio,
  AVG((json_payload->'task'->>'actual_hours')::numeric) AS real_promedio
FROM manifests
WHERE json_payload->'task'->'assignee'->>'id' = '322e3745-9756-4a7c-af11-44b33edef44d'
  AND json_payload->'task'->>'sprint'->>'id' = '6f2d4310-...';

-- ¿Qué tareas mencionaron LD-12?
SELECT task_id
FROM manifests
WHERE json_payload->'delivery'->'living_documents_declared_no_change' @> '["LD-12"]';

-- ===== Queries DevOps (schema v1.1, tabla manifest_operations) =====

-- Auditoría: ¿qué SQL se aplicó en producción en S6?
SELECT task_id, operation_type, executed_at, sql_applied, post_checks_passed
FROM manifest_operations
WHERE environment = 'production'
  AND executed_at >= '2026-05-01'
ORDER BY executed_at DESC;

-- ¿Qué re-entregas hubo (tareas DevOps rechazadas y vueltas a entregar)?
SELECT task_id, operation_type, executed_at, rejection_history
FROM manifest_operations
WHERE rejection_history IS NOT NULL
ORDER BY executed_at DESC;

-- ¿Operaciones en producción que NO pasaron post_checks?
SELECT task_id, operation_type, executed_at, post_checks_details
FROM manifest_operations
WHERE environment = 'production'
  AND post_checks_passed = false;

-- ¿Issues resueltos por operaciones DevOps?
SELECT mo.task_id, mo.operation_type, mo.executed_at, mo.issue_resolved,
       i.title AS issue_title
FROM manifest_operations mo
LEFT JOIN issues i ON i.id = mo.issue_resolved
WHERE mo.issue_resolved IS NOT NULL;

-- Audit trail completo (vista materializada)
SELECT task_id, task_title, operation_type, environment,
       executed_at, executed_by, post_checks_passed,
       is_reentrega, tl_verdict, pm_approved_at
FROM v_devops_audit_trail
WHERE environment = 'production'
ORDER BY executed_at DESC
LIMIT 50;

-- Métrica: tasa de éxito DevOps por entorno
SELECT environment,
       COUNT(*) AS total_ops,
       SUM(CASE WHEN post_checks_passed THEN 1 ELSE 0 END) AS exitosas,
       SUM(CASE WHEN rejection_history IS NOT NULL THEN 1 ELSE 0 END) AS re_entregas,
       ROUND(100.0 * SUM(CASE WHEN post_checks_passed THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_exito
FROM manifest_operations
GROUP BY environment;
```

## 4. Beneficios secundarios

### Combinación con IMPROVE-001 (Pool de Transacciones)

Las dos mejoras se complementan:

```
IMPROVE-001 (Pool):
  Agente → emite operations JSON → Pool ejecuta → audita en pool_transactions

IMPROVE-002 (Manifest DB):
  TL genera manifest → upload a VTT → ingestor parsea → BD queryable

Juntos:
  El bloque delivery.dynamic_model_actions del manifest se construye
  AUTOMÁTICAMENTE consultando pool_transactions WHERE task_id = MS-XXX
```

Es decir: con ambas mejoras, **el TL ya no escribe manualmente `dynamic_model_actions`** — se genera desde el pool de transacciones.

### Para PM
- Dashboard "estado del proyecto" en tiempo real
- Reportes ejecutivos al cierre de sprint sin esfuerzo manual

### Para TL
- "¿qué tech_debts tengo abiertos?" → query 1 línea
- "¿qué tareas tengo en review desde hace más de 48h?" → query con JOIN

### Para auditoría
- Trazabilidad completa de cada manifest desde su versión 1.0 hasta la última
- Comparación entre versiones (qué cambió entre v1.5 y v1.6)

## 5. Riesgos / consideraciones

| Riesgo | Mitigación |
|---|---|
| Duplicación de datos (manifest en VTT + BD) | El attachment VTT es la fuente; la BD es un índice |
| Sincronización fallida | Reconciliación periódica (cron) que re-ingesta manifests |
| Evolución del schema JSON del manifest | `schema_version` + adaptadores por versión |
| Costo de infra (Postgres extra) | Aceptable si ahorra reporting manual |
| Performance de queries sobre JSONB | Índices GIN + vistas materializadas |

## 6. Plan de implementación sugerido (MVP)

### Fase 1 — Schema y modelo (1 día)
- Tabla `manifests` + `manifest_versions`
- **Tabla `manifest_operations`** (schema v1.1)
- Vista materializada `manifest_indexes`
- **Vista materializada `v_devops_audit_trail`**
- Migración inicial con manifests existentes (MS-283..MS-293, VTT-706, VTT-720)
- Parser que detecta `schema_version` y aplica adaptador correcto (v1.0 vs v1.1)

### Fase 2 — Ingestor de manifests (2 días)
- Webhook/cron que detecta nuevos attachments `fileType=manifest`
- Parser JSON + insert en manifests + manifest_versions
- **Parser del bloque `delivery.operations`** → insert en `manifest_operations` si existe
- Refresh de vistas materializadas
- Validación: si `task.category=deployment` y NO hay `operations`, marcar warning

### Fase 3 — Extender TrackableItems (1 día)
- Agregar columnas: `tags`, `last_evidence_at`, `evidences_count`, `tasks_count`
- Agregar a evidences: `task_id`, `sprint_id`, `parsed_marker`
- Parser de marker `[TASK:MS-XXX] [SPRINT:SX]` desde description

### Fase 4 — API de queries (2 días)
- `GET /api/reports/manifest-index?sprint_id=&assignee_id=&verdict=`
- `GET /api/reports/tech-debt-pending?priority=`
- `GET /api/reports/velocity?agent_id=&sprint_id=`
- `GET /api/trackable-items?has_evidence=true&with_metadata=true`
- **`GET /api/reports/devops-audit-trail?environment=&from=&to=`** (NUEVO)
- **`GET /api/reports/devops-reentregas`** (NUEVO)

### Fase 5 — Dashboards (1 día)
- Vista PM: estado global del proyecto + **tasa éxito DevOps por entorno**
- Vista TL: tareas en review + tech debts abiertos + **operaciones recientes en prod**
- Vista agente: sus tareas pasadas con métricas
- **Vista DevOps: audit trail filtrable por entorno/tipo/fecha**

### Fase 6 — Soporte de schemas múltiples (NUEVO, 1 día)
- Adaptador `manifest_v1_0_to_v1_1`: enriquece manifests v1.0 viejos cuando se re-parsean
- Migración opcional: backfill de `manifest_operations` desde manifests v1.0 que sean `category=deployment`
- Documentación del versionado de schema en la BD

**Total estimado:** 8 días (era 7; +1 día por bloque operations y vistas DevOps)

## 7. Combinación con Pool de Transacciones (IMPROVE-001)

Si ambas mejoras se implementan, el flujo end-to-end queda así:

```
1. TL ejecuta cierre de tarea
   → emite operations JSON al Pool
   → Pool ejecuta y registra en pool_transactions
   → Pool retorna IDs de TIs creados, evidencias agregadas, devlog resuelto

2. TL genera manifest
   → consulta pool_transactions WHERE task_id = MS-XXX
   → arma bloque delivery.dynamic_model_actions AUTOMÁTICAMENTE
   → sube manifest a VTT como attachment

3. Manifest ingestor
   → detecta nuevo manifest
   → parsea JSON
   → inserta en manifests + manifest_versions
   → refresca manifest_indexes

4. PM / TL / agente
   → consulta dashboards
   → ve métricas en tiempo real
```

## 8. Decisión solicitada al PM

1. ¿Aprobar como **tarea VTT** del proyecto VTT (no de Memory Service)?
2. ¿Implementar **antes**, **después** o **junto** con IMPROVE-001 (Pool)?
   - Recomendación: **junto** — se diseñan considerándose mutuamente
3. ¿En qué motor de BD? Postgres compartido con VTT o BD separada
4. Si se aprueba: ¿cuáles son los reportes/dashboards prioritarios para el primer release?

## 9. Referencias

- Sesión origen: TL Memory Service 2026-05-13 (cierre MS-285 con modelo dinámico — discusión sobre archivos JSON queryables)
- Documentos relacionados:
  - `IMPROVE-001_pool_transacciones_vtt.md` (mejora complementaria)
  - `00_GUIA_NORMATIVA_VTT.md` §2.5 (donde se documentó el concepto inicial)
  - `knowledge/platform-feedback/VTT_PLATFORM_GAPS_2026-05-13.md`:
    - GAP-VTT-04 (campo `task_id` en evidence) — se resuelve con esta mejora
    - GAP-VTT-05 (`GET /tasks/:id/trackable-items`) — facilitado por vistas materializadas
- Manifests existentes que sirven de input:
  - `knowledge/task-manifests/04-development/S01/MS-283.json` v1.6
  - `knowledge/task-manifests/04-development/S01/MS-284.json` v1.6
  - `knowledge/task-manifests/04-development/S01/MS-285.json` v1.5.1
- Catálogo TIs original: `c:/tmp/ms_trackable_items.json` (210 items)

## 10. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Documento inicial — propuesta para evaluación PM |
| **1.1** | **2026-05-17** | **Soporte para manifest schema v1.1 (bloque DevOps): tabla `manifest_operations`, vista `v_devops_audit_trail`, queries y dashboards DevOps. Fase 6 nueva (adaptadores multi-schema). +1 día estimación. Triggers: manifests VTT-706 (DB normal) y VTT-720 (DevOps SQL) que requirieron formalizar el patrón.** |
