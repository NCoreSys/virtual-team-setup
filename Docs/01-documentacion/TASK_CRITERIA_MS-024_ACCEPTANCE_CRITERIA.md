# TASK CRITERIA — MS-024: Acceptance Criteria
## Mapeo de escenarios Gherkin, DoD y DoR al modelo VTT V4

**Proyecto ID:** `d0fc276d-e764-4a83-96e9-d65f086ed803`
**Generado por:** SA Ejecutor (`0c128e3b-db3b-4e31-b107-0379b5791233`)
**Fecha:** 2026-05-06
**Endpoint:** `POST /api/tasks/{taskId}/criteria`

---

## 1. GHERKIN SCENARIOS → TASK CRITERIA (53 items)

Cada escenario se registra como criterio en la tarea VTT de la US correspondiente. El agente debe resolver `{taskId}` buscando la tarea de implementación de cada US en el sprint asignado.

### EP-01 · Import & Storage

| code | criteriaTypeCode | US | description | sprint |
|------|-----------------|-----|-------------|--------|
| AC-US-001-1 | `functional` | US-001 | Import exitoso CLAUDE_SDK: HTTP 201, IMPORTED, JSONL en /storage/, contentPreview 500 chars en BD, turns/blocks/usage persistidos, clasificación ejecutada | S02 |
| AC-US-001-2 | `functional` | US-001 | Validación Zod falla: HTTP 400 con detalle, sin registro en BD | S02 |
| AC-US-002-1 | `functional` | US-002 | Reimport mismo externalSessionId: HTTP 200, ALREADY_INDEXED, sin duplicados en BD ni storage | S02 |
| AC-US-003-1 | `functional` | US-003 | Race condition P2002: segundo request captura P2002, findUnique, retorna ALREADY_INDEXED. Un solo registro en BD | S02 |
| AC-US-004-1 | `functional` | US-004 | Import AGENT_REVIEW: HTTP 201, primaryAgentId=null, participants y messages persistidos, archivo en /storage/_reviews/ | S02 |
| AC-US-004-2 | `security` | US-004 | SERVICE_KEY inválida en import-review: HTTP 401, sin registros creados | S02 |
| AC-US-005-1 | `functional` | US-005 | Import incremental: append 3 mensajes nuevos, total 8, originales sin cambios | S04 |
| AC-US-005-2 | `functional` | US-005 | Upsert participante nuevo: agente-C agregado, A y B sin cambios, total 3 | S04 |
| AC-US-006-1 | `functional` | US-006 | Upload claude.ai: detecta formato CLAUDE_WEB, importa, retorna IMPORTED | S06 |
| AC-US-006-2 | `functional` | US-006 | Upload duplicado: retorna ALREADY_INDEXED | S06 |
| AC-US-007-1 | `functional` | US-007 | Import CLI: sourceCode=CLAUDE_CLI, archivo en /storage/CLAUDE_CLI/ | S02 |
| AC-US-008-1 | `functional` | US-008 | Import CLAUDE_WEB: totalCostUsd=null (adapter sin costo) | S04 |
| AC-US-009-1 | `functional` | US-009 | Import ChatGPT: totalCostUsd=null, aparece con $0.00 en cost-report | S04 |
| AC-US-010-1 | `functional` | US-010 | Error en import: estado permanece PROCESSING, NO cambia a ERROR, cleanup será responsable | S04 |

### EP-02 · Memory Context

| code | criteriaTypeCode | US | description | sprint |
|------|-----------------|-----|-------------|--------|
| AC-US-011-1 | `functional` | US-011 | Contexto respondido <500ms: HTTP 200, JSON con 6 secciones, solo IMPORTED | S03 |
| AC-US-011-2 | `performance` | US-011 | Carga 10 VU k6 60s: p95 latencia <500ms | S03 |
| AC-US-012-1 | `performance` | US-012 | Timeout >500ms: HTTP 504 MEM-ERR-504, sin respuesta parcial, sin retry, sin degraded | S03 |
| AC-US-013-1 | `functional` | US-013 | projectId ausente: HTTP 400 | S03 |
| AC-US-013-2 | `functional` | US-013 | Filtrado por proyecto: solo retorna conversaciones del proyecto solicitado | S03 |
| AC-US-014-1 | `functional` | US-014 | taskId filtra adicionalmente dentro del proyecto | S03 |
| AC-US-015-1 | `functional` | US-015 | Respuesta siempre síncrona, sin polling ni websocket | S03 |

### EP-03 · Timeline & History

| code | criteriaTypeCode | US | description | sprint |
|------|-----------------|-----|-------------|--------|
| AC-US-016-1 | `functional` | US-016 | Timeline incluye TASK_EXECUTION por primaryAgentId, ordenado DESC | S02 |
| AC-US-016-2 | `functional` | US-016 | Timeline incluye participaciones multi-agente via ConversationParticipant | S02 |
| AC-US-017-1 | `functional` | US-017 | Contenido leído desde /storage/ (NO BD). BD solo tiene contentPreview 500 chars. D-MEM-43 | S03 |
| AC-US-017-2 | `functional` | US-017 | Archivo faltante: HTTP 404 MEM-ERR-404, NO intenta leer de BD | S03 |
| AC-US-018-1 | `functional` | US-018 | Listado con filtros: retorna metadata (turnCount, tokens, topics, preview), NO contenido completo | S05 |
| AC-US-018-2 | `functional` | US-018 | Default sin filtro status: solo retorna IMPORTED | S05 |
| AC-US-019-1 | `functional` | US-019 | Reviews en timeline via ConversationParticipant con conversationType | S05 |
| AC-US-020-1 | `functional` | US-020 | contentPreview visible en listado GET /conversations | S05 |
| AC-US-021-1 | `functional` | US-021 | UI recibe JSONL completo, no sabe que vino de /storage/. D-MEM-43 | S03 |

### EP-04 · Cost Tracking

| code | criteriaTypeCode | US | description | sprint |
|------|-----------------|-----|-------------|--------|
| AC-US-022-1 | `functional` | US-022 | Totales por proyecto: totalConversations, totalCostUsd (suma), breakdown agente/modelo | S05 |
| AC-US-022-2 | `functional` | US-022 | Filtro from/to aplica sobre startedAt | S05 |
| AC-US-023-1 | `functional` | US-023 | Breakdown por agente dentro de proyecto | S05 |
| AC-US-024-1 | `functional` | US-024 | Cost report por agente: breakdown proyecto/modelo | S05 |
| AC-US-025-1 | `functional` | US-025 | Costo importado del SDK (totalCostUsd=1.42), no recalculado | S05 |
| AC-US-026-1 | `functional` | US-026 | Adapter sin costo: $0.00 en reporte, conv NO excluida, conteo la incluye | S05 |
| AC-US-027-1 | `technical` | US-027 | groupBy=byWeek: formato YYYY-W##, usa prisma.$queryRaw con DATE_TRUNC, NO Prisma groupBy nativo. TL-08 | S05 |

### EP-05 · Operations & Dashboard

| code | criteriaTypeCode | US | description | sprint |
|------|-----------------|-----|-------------|--------|
| AC-US-028-1 | `functional` | US-028 | Stats globales: breakdown por status/source/type, activeAgents (30 días), recentActivity | S05 |
| AC-US-029-1 | `functional` | US-029 | Health OK: HTTP 200, { status: "ok" } | S05 |
| AC-US-030-1 | `functional` | US-030 | Health detalle: db/storage/redis status reportados | S05 |
| AC-US-030-2 | `functional` | US-030 | BD caída: HTTP 503, { status: "down", db: "down" } | S05 |
| AC-US-031-1 | `functional` | US-031 | Cleanup ejecuta cada 5 min automáticamente, busca STALE >10min | S04 |
| AC-US-032-1 | `functional` | US-032 | Reintento: PROCESSING >10min, retryCount=1 → PENDING, retryCount=2 | S04 |
| AC-US-032-2 | `functional` | US-032 | MAX_RETRIES excedido: retryCount=4 → ERROR, "Max retries exceeded" | S04 |
| AC-US-032-3 | `functional` | US-032 | Archivo faltante: → ERROR directo, "Storage file missing", retryCount no cambia | S04 |
| AC-US-033-1 | `functional` | US-033 | 10 catálogos cargados como Maps al startup, imports resuelven IDs sin queries | S01 |
| AC-US-033-2 | `functional` | US-033 | BD inaccesible al inicio: servicio aborta, NO levanta HTTP | S01 |

---

## 2. RESUMEN POR CRITERIA TYPE

| criteriaTypeCode | name | Cantidad | Escenarios ejemplo |
|-----------------|------|----------|-------------------|
| `functional` | Funcional | 44 | Import exitoso, ALREADY_INDEXED, timeline, listado, cost report |
| `performance` | Rendimiento | 3 | Context <500ms p95, timeout 504, carga 10 VU |
| `security` | Seguridad | 1 | SERVICE_KEY inválida → 401 |
| `technical` | Técnico | 1 | byWeek requiere SQL raw |
| `integration` | Integración | 0 | (cubiertos por functional — Runtime/PB son actores de los functional) |
| **Total** | | **49** | |

> **Nota:** 4 escenarios del total de 53 son redundantes (cubren el mismo comportamiento desde distintas US). Se registran 49 criterios únicos para evitar duplicación.

---

## 3. DoD → CRITERIA TEMPLATE (criteriaTypeCode: `dod`)

Los DoD se registran como **template de criterios** que se aplica a todas las tareas del tipo correspondiente. No se vinculan a una US específica sino al sprint/fase.

### DoD Backend (12 criteria)

| code | description |
|------|-------------|
| DOD-BE-01 | Código compila sin errores TypeScript (tsc --noEmit) |
| DOD-BE-02 | Validación Zod implementada para el endpoint |
| DOD-BE-03 | Tests unitarios pasan (npm test) |
| DOD-BE-04 | Endpoint probado localmente con curl/Postman (happy path + error) |
| DOD-BE-05 | Swagger/JSDoc actualizado |
| DOD-BE-06 | Máquina de estados respetada: sin transiciones prohibidas (2.5.6) |
| DOD-BE-07 | Idempotencia verificada si aplica |
| DOD-BE-08 | Code Logic (.LOGIC.md) creado/actualizado |
| DOD-BE-09 | Development Log creado |
| DOD-BE-10 | PR creado con referencia a tarea VTT |
| DOD-BE-11 | Sin console.log de debug |
| DOD-BE-12 | Sin TODOs sin resolver |

### DoD Frontend (9 criteria)

| code | description |
|------|-------------|
| DOD-FE-01 | Componente renderiza sin errores en browser |
| DOD-FE-02 | Happy path probado manualmente |
| DOD-FE-03 | Estados de error implementados (404, 500, timeout) |
| DOD-FE-04 | Estado de carga implementado (spinner/skeleton) |
| DOD-FE-05 | Desktop ≥1280px verificado (LIM-08) |
| DOD-FE-06 | Integración con endpoint backend verificada |
| DOD-FE-07 | Code Logic (.LOGIC.md) creado/actualizado |
| DOD-FE-08 | Development Log creado |
| DOD-FE-09 | Sin console.log de debug |

### DoD Documentación (8 criteria)

| code | description |
|------|-------------|
| DOD-DOC-01 | Todos los archivos del delivery creados en ruta del ASSIGNMENT |
| DOD-DOC-02 | Criterios de completitud del BRIEF cumplidos |
| DOD-DOC-03 | Sin secciones vacías, TODOs ni placeholders |
| DOD-DOC-04 | Devlog creado |
| DOD-DOC-05 | Code Logic creado si aplica |
| DOD-DOC-06 | Archivos subidos a VTT con fileType correcto |
| DOD-DOC-07 | Comentario de entrega en tarea VTT |
| DOD-DOC-08 | Tarea movida a task_in_review |

### DoD QA (6 criteria)

| code | description |
|------|-------------|
| DOD-QA-01 | Plan de pruebas documentado |
| DOD-QA-02 | Test cases ejecutados (pass/fail registrado) |
| DOD-QA-03 | Defectos registrados como Bug en VTT |
| DOD-QA-04 | Cobertura de escenarios críticos verificada contra 2.7.5 |
| DOD-QA-05 | Resultados documentados en devlog |
| DOD-QA-06 | Evidence screenshots/logs para features visuales |

---

## 4. DoR → CRITERIA TEMPLATE (criteriaTypeCode: `dor`)

Se registra como template que se valida ANTES de mover cualquier tarea a `task_in_progress`.

| code | description |
|------|-------------|
| DOR-01 | ASSIGNMENT leído completamente |
| DOR-02 | Todas las dependencias en task_completed |
| DOR-03 | Ambigüedades resueltas o escaladas |
| DOR-04 | Fuentes de referencia accesibles |
| DOR-05 | BD memory_service_db accesible |
| DOR-06 | Storage /storage/ montado con permisos |
| DOR-07 | Variables de entorno configuradas (DATABASE_URL, SERVICE_KEY) |
| DOR-08 | Rama Git creada: feature/MS-XXX |
| DOR-09 | npm install sin errores |
| DOR-10 | SPEC v1.9 disponible y leída |
| DOR-11 | Documentos de análisis relevantes disponibles |
| DOR-12 | Si modifica schema: migration verificada local |
| DOR-13 | Si depende de catálogos: seed ejecutado |
| DOR-14 | Contrato del endpoint definido en SPEC §8 (solo BE) |

---

## 5. TEST SCENARIOS → CRITERIA (criteriaTypeCode: `functional`)

Los 8 test suites de 2.7.5 se registran como criterios en las tareas de QA de cada sprint.

| code | test suite | escenarios | sprint QA | tareas US cubiertas |
|------|-----------|------------|-----------|---------------------|
| TS-01 | Idempotencia Import | 5 | S02 QA | US-001, US-002, US-003 |
| TS-02 | Context <500ms | 6 | S03 QA | US-011, US-012 |
| TS-03 | Cleanup Cron | 8 | S04 QA | US-010, US-031, US-032 |
| TS-04 | Cost Report | 7 | S05 QA | US-022, US-025, US-026, US-027 |
| TS-05 | Health Check | 5 | S05 QA | US-029, US-030 |
| TS-06 | GET /content Storage | 4 | S03 QA | US-017, US-021 |
| TS-07 | VTT_CHANNEL Incremental | 5 | S04 QA | US-004, US-005 |
| TS-08 | SERVICE_KEY Auth | 6 | S02 QA | US-001, US-004, US-011 |

---

## 6. INSTRUCCIONES PARA EL AGENTE

### Paso 1 — Registrar Gherkin AC en tareas de US

Para cada escenario de la sección 1:

```
POST /api/tasks/{taskId}/criteria
{
  "criteriaTypeCode": "{criteriaTypeCode de la tabla}",
  "description": "{description de la tabla}",
  "code": "{code de la tabla}"
}
```

El `{taskId}` se resuelve buscando la tarea de implementación de cada US en el sprint correspondiente.

### Paso 2 — Registrar DoD como template

Los DoD se registran una vez y se vinculan a todas las tareas del tipo correspondiente:

- DOD-BE-01..12 → todas las tareas taggeadas como `backend`
- DOD-FE-01..09 → todas las tareas taggeadas como `frontend`
- DOD-DOC-01..08 → todas las tareas taggeadas como `documentation`
- DOD-QA-01..06 → todas las tareas taggeadas como `testing`

### Paso 3 — Registrar DoR como template

DOR-01..14 se vinculan a TODAS las tareas del proyecto como precondición de `task_in_progress`.

### Paso 4 — Registrar Test Scenarios en tareas QA

TS-01..08 se registran como criterios `functional` en las tareas de testing de cada sprint.

---

## RESUMEN TOTAL

| Tipo | Cantidad |
|------|----------|
| Gherkin AC (functional, performance, security, technical) | 49 |
| DoD Backend | 12 |
| DoD Frontend | 9 |
| DoD Documentación | 8 |
| DoD QA | 6 |
| DoR Universal | 14 |
| Test Scenarios (en tareas QA) | 46 |
| **Total criteria a registrar** | **144** |

---

**Documento:** TASK_CRITERIA_MS-024_ACCEPTANCE_CRITERIA.md
**Versión:** 1.0
**Fecha:** 2026-05-06
