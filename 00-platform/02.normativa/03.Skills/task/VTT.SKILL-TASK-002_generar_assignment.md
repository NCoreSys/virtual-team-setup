# VTT.SKILL-TASK-002 — Generar ASSIGNMENT

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-TASK-002` |
| **Categoría** | TASK (Task CRUD) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | TL (genera el documento), SA Reviewer (revisa antes de entregar al agente) |
| **Tokens estimados** | ~500 |
| **Cuándo se usa** | FASE 2 del PROTOCOL-ASG-001 §5.2.5 — antes de asignar tarea al agente |
| **Reemplaza** | `SKL-TASK-02_generar-assignment.md` (legacy en `_pending-migration/vtt-task/`) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea ya creada |
| `brief_path` | path | sí | Ruta al BRIEF (`knowledge/agent-tasks/briefs/<phase>/<sprint>/BRIEF_<TASK_ID>_<slug>.md`) |
| `task_type` | enum | sí | `wireframe`/`design_system`/`spec_tecnica`/`codigo_be`/`codigo_fe`/`tests`/`documentacion`/`devops` |
| `dependencies_data_paths` | array<path> | sí | Rutas absolutas a docs source (Personas, User Flows, etc.) |
| `assignment_path` | path | sí | Output: `knowledge/agent-tasks/assignments/<phase>/<sprint>/ASSIGNMENT_<TASK_ID>_<slug>.md` |
| `living_documents_aplicables` | array<string> | sí/no | Si la tarea toca BD/endpoints/infra — IDs de LDs (LD-01, LD-03, etc.) |
| `trackable_items_linked` | array<{code, type, title}> | sí | TIs (RFs, NFRs, ADRs, BRs) que esta tarea implementa |

> **Política contractual:** los 7 inputs son fijos. La calidad del ASSIGNMENT depende 100% de la profundidad de `dependencies_data_paths` (R1 del análisis de dependencias).

---

## Precondición

- BRIEF de la tarea existe en disco
- Tarea creada en VTT con status `task_pending` (`VTT.SKILL-TASK-001` ejecutada)
- Dependencias declaradas en R2 de la tarea (todas en `task_completed` o `task_approved`)
- $TOKEN obtenido (`VTT.SKILL-AUTH-001`)

---

## Variables del entorno

```bash
$TOKEN              # JWT
$VTT_BASE_URL       # http://77.42.88.106:3000
$AGENT_UUID         # UUID del TL que ejecuta
$VTT_SETUP          # path al Source of Truth de la normativa
```

---

## Paso 1 — Análisis de dependencias de datos (R1 — OBLIGATORIO)

> **Regla absoluta:** Ningún ASSIGNMENT se genera sin completar este análisis. Un ASSIGNMENT sin dependencias verificadas = el agente trabaja en el vacío = entrega incorrecta.
>
> **Caso de origen** (lección PROC-MS-029): el DL generó wireframes MS-029..035 sin leer User Flows ni Personas. Supuso 9 pantallas desde la SPEC. Costo: ~1M tokens en regeneración. **Esta skill existe para evitar que se repita.**

### 1.1 Leer el BRIEF completo

Identificar:
- Tipo de entregable (wireframe / código / spec / etc.)
- Archivos específicos a generar
- Criterios de completitud

### 1.2 Identificar datos necesarios según `task_type`

| `task_type` | Datos source mínimos |
|---|---|
| `wireframe` | Personas, User Flows, Site Map/IA, Design System, User Stories |
| `design_system` | Brand guidelines, tokens previos, referencias visuales |
| `spec_tecnica` | SPEC v1.X, decisiones de arquitectura (D-XXX), modelo de datos |
| `codigo_be` | Schema Prisma, contratos de API, reglas de negocio, error codes |
| `codigo_fe` | Wireframes aprobados, Design System, contratos de API |
| `tests` | Código a testear, criterios de aceptación, casos de error |
| `documentacion` | Todo lo anterior del módulo correspondiente |
| `devops` | docker-compose, env.example, infra spec |

### 1.3 Trazar cada dependencia a su documento concreto

Por cada item identificado en 1.2:
```
Tarea origen → Entregable específico → Ruta exacta en repo
```

### 1.4 Verificar que los documentos existen en disco

```bash
for DOC in "${DEPENDENCIES_DATA_PATHS[@]}"; do
    if [ ! -f "$DOC" ]; then
        echo "FALTA: $DOC"
        # Marcar tarea como bloqueada
        curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer $TOKEN" \
          -d "{\"statusId\": \"$STATUS_BLOCKED_UUID\", \"changedBy\": \"$AGENT_UUID\", \"reason\": \"Falta $DOC\"}"
        exit 1
    fi
done
```

### 1.5 Verificar que las tareas dependencia están `task_completed` o `task_approved`

```bash
for DEP_TASK in "${DEPENDS_ON_TASKS[@]}"; do
    STATUS=$(curl -s "$VTT_BASE_URL/api/tasks/$DEP_TASK" -H "Authorization: Bearer $TOKEN" \
      | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])")
    if [[ "$STATUS" != "task_completed" && "$STATUS" != "task_approved" ]]; then
        echo "Dependencia $DEP_TASK en $STATUS — esperar"
        exit 1
    fi
done
```

---

## Paso 2 — Leer artefactos REALES del codebase (LL-005)

> **Regla LL-005:** Llenar el ASSIGNMENT desde artefactos verificados, NUNCA desde memoria ni desde el handoff del PM.

Según `task_type`, leer:

| `task_type` | Archivos a leer |
|---|---|
| `codigo_fe` | `frontend/src/router/index.tsx`, `backend/src/routes/<modulo>.ts`, `frontend/src/components/features/`, `frontend/src/hooks/use*.ts`, `frontend/src/index.css` |
| `codigo_be` | `backend/src/routes/index.ts`, `backend/src/routes/<modulo>.ts`, `backend/prisma/schema.prisma`, `backend/src/middleware/` |
| `codigo_db` | `backend/prisma/schema.prisma`, DOC de modelo de datos + ERD, `backend/prisma/migrations/` (último) |
| `devops` | `docker-compose.yml`, `backend/.env.example`, `frontend/nginx.conf` (si aplica) |
| `wireframe` / `design_system` | `frontend/src/components/`, DOC design system, `knowledge/design/`, wireframes/mockups aprobados |

---

## Paso 3 — Escribir el ASSIGNMENT

**Ubicación:** `knowledge/agent-tasks/assignments/<phase>/<sprint>/ASSIGNMENT_<TASK_ID>_<slug>.md`

### Estructura — 8 secciones obligatorias

```markdown
## 1. Estado actual del proyecto
- Branches abiertos: [lista]
- PRs pendientes de merge: [lista]
- Qué debe estar mergeado antes de empezar

## 2. APIs y servicios disponibles
| Endpoint | Método | Estado | Notas |
|---|---|---|---|
| /api/... | POST | [OK] | ... |
| /api/... | GET | [FALTA] | BE debe crear primero |

## 3. Arquitectura y estructura
- Carpetas del proyecto
- Patrones y convenciones
- Nomenclatura

## 4. Contexto de integración
- Cómo se conecta con el resto del sistema
- Dependencias con otros módulos

## 5. Entidades y modelos
(Copiar desde schema.prisma — NO inventar nombres de campos)

## 6. Recursos de diseño (si aplica)
- Wireframe: <ruta exacta>
- Design tokens: <ruta exacta>
- Mockup: <ruta exacta>

## 7. Checklist detallado (mínimo 10-15 items verificables)
- [ ] Item 1
- [ ] Item 2
...

## 8. Archivos a revisar ANTES de empezar
| Archivo | Propósito |
|---|---|
| ruta/exacta/archivo.ts | descripción |

## DOCUMENTOS DE REFERENCIA OBLIGATORIOS

Leer TODOS antes de comenzar. Sin estos documentos no se puede ejecutar la tarea.

| Documento | Tarea origen | Ruta exacta |
|---|---|---|
| <nombre> | MS-XXX | phases/.../<archivo>.md |
```

---

## Paso 3.5 — Sección de Living Documents (si aplica)

Si `living_documents_aplicables.length >= 1`, agregar al ASSIGNMENT:

```markdown
## Living Documents a actualizar (obligatorio antes de task_in_review)

Actualizar ANTES de mover a in_review. Incluir en SKL-REPORT-01 sección "Document Impacts".

- [ ] **LD-XX** `phases/.../archivo.md` — [qué actualizar]
- [ ] **LD-XX** `phases/.../archivo.md` — [qué actualizar]
```

**Tabla de defaults por `task_type`:**

| `task_type` | LDs típicos |
|---|---|
| `codigo_db` | LD-01 (schema_prisma), LD-02 (erd) + LD-06 si hay índices nuevos |
| `codigo_be` | LD-03 (openapi_spec), LD-04 (endpoints_list) + LD-05 si hay errores nuevos |
| `devops` | LD-12 (env_matrix) si hay vars nuevas |

Si la tarea NO toca ningún LD → omitir esta sección.

---

## Paso 4 — Trackable Items linkeados

Agregar al ASSIGNMENT:

```markdown
## Trackable Items linkeados (TL ya los registró en VTT)

| Código | Tipo | Título |
|---|---|---|
| RF-001 | rf | El sistema permite registrar memorias |
| NFR-PERF-01 | rnf | GET /context < 500ms P95 |
| ADR-SA-004 | adr | X-Service-Key para autenticación |

**Acceptance Criteria en VTT** (visibles en la tarea — marcar como met/not_met al completar)
```

---

## Validación

```
[ ] Paso 1 ejecutado (análisis de dependencias completo)
[ ] Tarea NO está en task_blocked (R1 cumplido)
[ ] Todas las dependencias en task_completed o task_approved
[ ] ASSIGNMENT tiene los 8 secciones obligatorias
[ ] Checklist tiene ≥10 items verificables
[ ] Rutas en el ASSIGNMENT son exactas (no aproximadas)
[ ] Sección Living Documents incluida (si aplica)
[ ] Sección Trackable Items linkeados incluida
[ ] DOCUMENTOS DE REFERENCIA OBLIGATORIOS poblada con rutas verificadas
[ ] El agente puede ejecutar SIN suponer nada
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| ASSIGNMENT con dependencias vagas ("ver design system") | No se ejecutó Paso 1.3 | Trazar cada dep a su archivo con ruta |
| Rutas que no existen | Falta Paso 1.4 verificación | Ejecutar `ls $RUTA` antes de incluir |
| Datos inventados del schema | Falta Paso 2 (LL-005) | Leer `schema.prisma` real, NO desde memoria |
| Checklist con <5 items | Falta granularidad | Mínimo 10 items verificables uno a uno |
| Falta sección LD | tarea de BD/BE/DO sin Living Docs | Aplicar tabla §Paso 3.5 |

---

## Scripts invocados

Ninguno — Skill descriptiva del proceso. La escritura del ASSIGNMENT es manual del TL (o futuro `VTT.SCRIPT-TASK-002_gen_assignment.py` para auto-generar el esqueleto).

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — para PATCH de bloqueo en Paso 1.4 si falta doc
- (siguiente del flujo) `VTT.SKILL-TASK-003_asignar_tarea` — subir ASSIGNMENT y asignar al agente

---

## Cuándo NO usar esta Skill

- **Si el ASSIGNMENT ya existe y solo se va a re-asignar** — usar directamente `VTT.SKILL-TASK-003`
- **Si la tarea fue rechazada y solo se corrigen findings** — el ASSIGNMENT original sigue válido, no regenerar

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-TASK-02_generar-assignment.md`. Mantiene el contrato funcional + las reglas R1/LL-005. Estructura los 8 elementos obligatorios y el sub-paso 3.5 (Living Documents). |
