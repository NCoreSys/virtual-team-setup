# CONTEXTO TL — Sesión de trabajo

**Última actualización:** 2026-04-21
**TL:** `92225290-6b6b-4c1f-a940-dcb4262507aa`
**Proyecto:** Memory Service (`d0fc276d-e764-4a83-96e9-d65f086ed803`) — Project Key: MS

---

## 1. ESTADO ACTUAL DEL PROYECTO

| Aspecto | Estado |
|---------|--------|
| **Estructura** | 10 fases, **116 tareas**, 381h (confirmado por HO_ACTUALIZAR_TAREAS_VTT.md v2.1) |
| **Tareas creadas en VTT** | ✅ Las 116 están creadas como MEM-001..MEM-116 |
| **Tareas asignadas** | ⏳ Pendiente — PM/DO ejecutan el script PATCH del HO v2.1 |
| **Código escrito** | 0 líneas. Multi-repo aún no definido (pendiente PM) |
| **Sprints (dates)** | ⚠️ Pendiente update PM (el plan de 14 sprints/52 tareas quedó obsoleto) |

---

## 2. QUÉ HA PASADO (últimos hitos)

| Fecha | Hito | Owner |
|-------|------|-------|
| 2026-04-12 | TL Review de SPEC v1.5 entregado (observaciones TL-01..TL-N) | TL anterior |
| 2026-04-13 | SPEC v1.6 + ADDENDUM v1.0 publicados | PM |
| 2026-04-15 | Handoff PM → PJM firmado (150h, 14 sprints, 52 tareas) — **OBSOLETO** | PM |
| 2026-04-18 | SPEC consolidado a v1.9 (43 decisiones cerradas) | PM |
| 2026-04-19 | Handoff PJM para crear tareas en VTT | PM |
| 2026-04-21 | **Onboarding TL** (OPERATIVO + PROJECT_MEMORY + este archivo) | Martin Rivas |
| 2026-04-21 | **HO v2.1:** 116 tareas creadas en nuevo project `51e169f7-...`, plan refactorizado a 10 fases / 381h | PJM |
| 2026-04-21 | Reglas del proyecto creadas (`.claude/rules/PROJECT_RULES.md`) | TL |
| 2026-04-21 | Plan de 116 tareas con asignaciones TL (`knowledge/agent-tasks/PLAN_116_TAREAS.md`) | TL |

---

## 3. QUÉ FALTA ANTES DE QUE TL PUEDA OPERAR

### ⏳ Bloqueantes pre-kickoff

| # | Item | Responsable | ETA |
|---|------|-------------|-----|
| 1 | PM/DO ejecuta script PATCH del HO v2.1 (asignar 116 tareas) | PM/DO | Antes kickoff |
| 2 | PM confirma sprint dates actualizados (las del plan v2.0 quedaron obsoletas) | PM | Pre-kickoff |
| 3 | PM define esquema **multi-repo** (1 repo por agente) | PM | Antes kickoff |
| 4 | PM valida **reassignments propuestos** (ver PLAN_116_TAREAS.md §Reassignments) | PM | Esta semana |
| 5 | Endpoint VTT para crear **dependencias** aún no confirmado (HO v2.1 §10) | DO | Pre-kickoff |
| 6 | Decidir: ¿endpoint auth es `/service-login` o `/service-token`? (HO v2.1 usa `/service-token`) | PM/DO | Al ejecutar script |
| 7 | Resolver gotcha `deliveryId` no persiste (HO v2.1 §5 #2) | PM + backend VTT | No bloqueante pero deja issue abierto |

### 🟢 Listo

- Spec v1.9 cerrada (43 decisiones D-MEM + 5 D-INT)
- Infra provisionada (BD, volumen storage, SERVICE_KEY, docker-compose)
- UUIDs confirmados: 12 agentes en 10 fases
- 10 Phase UUIDs + 116 Task IDs + 34 Delivery UUIDs mapeados en HO v2.1
- Reglas del proyecto en `.claude/rules/PROJECT_RULES.md` (estados VTT, no emojis, no mock data)

---

## 4. QUÉ TENGO QUE HACER YO (TL) EN LAS PRÓXIMAS 2 SEMANAS

### Esta semana (2026-04-21 → 2026-04-27)

- [ ] Entregar a PM `PLAN_116_TAREAS.md` con reassignments propuestos para que valide.
- [ ] Coordinar con PM la decisión de multi-repo (bloquea arranque).
- [ ] Releer SPEC v1.9 §4 (modelo de datos) — input para cuando revise MEM-041 (Database Design).
- [ ] Releer SPEC v1.9 §9.1 (flujo import) + §11 (context) — input para code review de S02+.

### Después del script PATCH (PJM/DO ejecuta)

- [ ] Ejecutar comando OPERATIVO §5.1 (`GET /api/tasks?assigneeId=$TL_UUID`) para listar **mis tareas TL oficiales**.
- [ ] Validar que las tareas que me tocan coinciden con el plan: `PLAN_116_TAREAS.md §Tareas TL`.
- [ ] Preparar checklist de code review para Analysis + Design Technical (mis fases principales).

### Durante las fases donde soy ejecutor (Analysis, Design Technical, Deploy, Operations)

- [ ] Ejecutar mis tareas asignadas (ver §5 abajo).
- [ ] Mantener canal abierto con AR, SA, DB, BE para decisiones de arquitectura compartidas.

---

## 5. MIS TAREAS COMO TL EJECUTOR (post-reassignments propuestos)

> **Fuente:** `PLAN_116_TAREAS.md` — listado completo. Lo de abajo es solo las tareas que ejecuto yo.

| Task ID | Título | Fase | Horas | Complexity | Notas |
|---------|--------|------|-------|------------|-------|
| MEM-040 | Code Architecture | Design Technical | 4h | HIGH | TL lidera estructura de código |
| MEM-044 | Architecture Decision Records | Design Technical | 4h | MEDIUM | ADRs = TL/AR compartido |
| MEM-047 | Technical Estimates | Design Technical | 3h | MEDIUM | TL estima |
| MEM-110 | Rollback Plan (doc) | Deploy | 2h | MEDIUM | TL documenta plan rollback |
| MEM-113 | Bug Fixes Operations (doc) | Operations | 2h | MEDIUM | TL documenta playbook |

**Total horas TL como ejecutor:** 15h

**Reassignments propuestos (eran TL, van a otro rol):**
- MEM-022 (Business Rules, Analysis) → **SA** (business rules es scope de SA, no TL)
- MEM-039 (Solution Architecture, Design Technical) → **AR** (deliverable arquitectural es AR)

Si PM valida estos reassignments, mi scope como ejecutor baja de 25h a 15h — lo cual es más consistente con el rol TL (planear + revisar).

**Además reviso (no ejecuto):** todas las tareas de BE, DB, FE, QA, DO que pasan por `task_in_review`.

---

## 6. TAREAS IN REVIEW / ON HOLD

**Ninguna.** El proyecto aún no tiene tareas ejecutadas (Sprint 2 no ha arrancado).

Cuando haya tareas en `task_in_review`, listarlas acá con:

```
| Task ID | Título | Ejecutor | Fecha entregada | Acción TL |
|---------|--------|----------|----------------|-----------|
```

---

## 7. RIESGOS TÉCNICOS CONOCIDOS (para vigilar)

| # | Riesgo | Sprint | Mitigación |
|---|--------|--------|------------|
| R1 | `GET /context` <500ms difícil con dataset grande | S03 | QA corre tests con 10/100/1000 convs + 50 concurrent (MEM-QA-001) |
| R2 | N+1 en import-review por catalog lookups dentro del loop | S04 | Prefetch Map al inicio del handler (MEM-BE-011) |
| R3 | Integración Hook Manager VTT (depende de servicio externo) | S06 | PM + PJM coordinan disponibilidad antes de May 19 |
| R4 | FE bloqueado si DL se atrasa en MEM-022 | Sprint 3 | Monitorear S-DL-04 de cerca; DL puede usar mocks para desbloquear |
| R5 | Partial indexes en Postgres shared requieren permisos | S01 | DO valida permisos antes de correr migración SQL cruda |

---

## 8. DECISIONES PENDIENTES QUE BLOQUEAN ASSIGNMENTS

Ninguna. Todas las decisiones D-MEM-01 a D-MEM-43 y D-INT-01 a D-INT-05 están cerradas.

Si en FASE 1 (planificación) descubro ambigüedad en la SPEC al escribir un ASSIGNMENT, **escalar a PM** antes de asignar.

---

## 9. NOTAS DE LA ÚLTIMA SESIÓN

(Esta sección se actualiza manualmente después de cada sesión de trabajo TL.)

**2026-04-21 — Onboarding inicial**
- Creados `OPERATIVO_TECH_LEAD.md`, `PROJECT_MEMORY.md`, y este archivo.
- Todavía no he ejecutado los comandos de arranque (PASO 3 del SETUP_TL) porque primero había que tener este contexto.
- Próxima sesión: ejecutar auth + listar tareas + verificar que PJM creó las 52 tareas.

---

### 2026-04-21 — Adaptación reglas VTT → Memory Service

**Hecho:**
- Revisado `memory-service-project/00-agent-setup/templates/AGENT_RULES_Rev.md` (865 líneas, v1.3 original de VTT).
- Identificados 7 bloques con datos VTT-específicos y adaptados a Memory Service:
  - Header: proyecto, versión 1.4
  - Sección 1: `TASK_TRACKING.md` → `GET /api/tasks/{TASK_ID}` (VTT API)
  - Sección 2: cambio de estado vía `PATCH /api/tasks/{TASK_ID}/status`
  - Sección 5: ejemplos devlog con IDs `MEM-BE-001`, `MEM-DB-001`
  - Sección 6.5: workflow 12 pasos adaptado, quitado `(repo)` del commit
  - Sección 7: Swagger en puerto `3002`, setup inicial en `MEM-BE-001`
  - Sección 8: formato commit sin `(repo)` + ejemplo Memory Service
  - Sección 9: checklist y cambio de estado a `task_in_review` vía API
  - Sección 10: reporte de problemas con `task_on_hold` vía API
  - Sección 12: tabla reemplazada con 8 estados VTT (sin emojis)
  - Sección 15.3/15.4/15.5: flujo ISSUE + datos faltantes con VTT API
  - Footer: versión 1.4 con changelog
- Creada copia oficial en `memory-service/.claude/rules/PROJECT_RULES.md` (886 líneas).
- Agregado encabezado de jerarquía de reglas en `PROJECT_RULES.md`:
  1. Este archivo manda en Memory Service
  2. `~/.claude/rules/rules_agents.instructions.md` aplica solo si este archivo no lo cubre
  3. En conflicto → gana PROJECT_RULES (específico del proyecto)

**Archivos tocados:**
- `memory-service-project/00-agent-setup/templates/AGENT_RULES_Rev.md` (editado — copia maestra)
- `memory-service/.claude/rules/PROJECT_RULES.md` (creado — source of truth operativa)
- `memory-service/.claude/rules/` (carpeta creada)

**Pendiente próxima sesión:**
- Ejecutar comandos de arranque OPERATIVO §5 (auth JWT + listar mis tareas + `task_in_review` + `task_on_hold`).
- Verificar que PJM creó las 52 tareas en VTT con conteo global.
- Empezar FASE 2: escribir ASSIGNMENTs de S01 (MEM-DB-001/002/003 + MEM-BE-001/002).

**Blockers nuevos:**
- **Multi-repo:** PM debe definir el esquema (1 repo por agente) antes de Sprint 2. Hasta entonces, commits sin `(repo)` y no se puede crear skeleton `memory-service-api/` oficial.
- Cuando PM decida: actualizar `PROJECT_RULES.md` §8 (agregar `(repo)` al commit format) + `PROJECT_MEMORY.md` (mapping agente → repo) + ASSIGNMENTs de S01.

**Escalaciones:**
- A PM: definición de multi-repo (naming + asignación por agente). Bloquea MEM-BE-001 y commits oficiales.

**Decisiones tomadas en sesión:**
- Eliminado sistema de emojis de estados (🟡🔵🟣...): ya no aplica porque el estado vive en VTT, no en `TASK_TRACKING.md`.
- Mantener 2 archivos sincronizados: template maestro en `00-agent-setup/` + copia operativa en `.claude/rules/`.
- NO tocar reglas globales (`~/.claude/rules/rules_agents.instructions.md`) porque afectan otros proyectos (DesignMine, Prompt AI Studio).

---

### 2026-04-21 — Reconciliación con HO_ACTUALIZAR_TAREAS_VTT.md v2.1

**Hecho:**
- Leído HO v2.1 del PJM (2026-04-21). Detectadas 5 discrepancias críticas contra mi memoria:
  - Total tareas: 52 → **116** (+381h)
  - Project ID: cambió a `d0fc276d-e764-4a83-96e9-d65f086ed803`
  - Phases: 2 → **10 fases** (Project Setup, Discovery, Planning, Analysis, Design UX/UI, Design Technical, Development, Testing, Deploy, Operations)
  - Equipo: 9 → **12 roles** (+SA, AR, UX)
  - Task IDs: `MEM-DB-001` → **numeración plana MEM-001..MEM-116**
- Actualizado `OPERATIVO_TECH_LEAD.md`: Project ID nuevo + 10 Phase UUIDs + 12 agentes + auth endpoint corregido a `/service-token` (con `.data.token`) + SERVICE_KEY movida a `$MEM_VTT_SERVICE_KEY` + API gotchas documentados.
- Actualizado `PROJECT_MEMORY.md` §6: fases rehechas, deliveries de Development (S01..S06 + UI-01..04) documentadas, referencias actualizadas.
- Actualizado este archivo §1-§5: estado real, hitos hasta hoy, mis 5 tareas reales como ejecutor (15h), reassignments propuestos.
- Creado `knowledge/agent-tasks/PLAN_116_TAREAS.md` con las 116 tareas + reassignments propuestos.

**Reassignments propuestos al PM (FLAGS para validación):**
- **MEM-022 (Business Rules, Analysis):** TL → **SA** (Business Rules es scope de System Architect, no TL)
- **MEM-039 (Solution Architecture, Design Technical):** TL → **AR** (deliverable arquitectural es AR, no TL)
- Resto de mis tareas (MEM-040, 044, 047, 110, 113) se mantienen en TL (code architecture, ADRs, estimates, rollback doc, ops doc).

**Pendiente próxima sesión:**
- Esperar que PM valide reassignments propuestos en `PLAN_116_TAREAS.md`.
- PM/DO ejecuta script PATCH del HO v2.1 para asignar las 116 tareas.
- Yo ejecuto `GET /api/tasks?assigneeId=$TL_UUID` para validar mis tareas oficiales.
- PM actualiza sprint dates (el plan v2.0 con 14 sprints quedó obsoleto).

**Blockers nuevos:**
- Sprint dates desactualizados (plan v2.0 obsoleto, v3.0 aún no tiene dates concretas).
- Endpoint de dependencias VTT no confirmado (HO v2.1 §10) — no hay forma automática de encadenar S01→S02→...→S06.
- Gotcha `deliveryId` no persiste en GET task — no puedo trazar task→delivery automáticamente.
- Multi-repo sigue pendiente (blocker preexistente).

**Escalaciones:**
- A PM: validar 2 reassignments (MEM-022 → SA, MEM-039 → AR).
- A PM: confirmar sprint dates actualizados para las 116 tareas.
- A PM+DO: endpoint de dependencias VTT (para crear MEM-038 → MEM-081 y cadenas S01→S06).
- A PM: definir multi-repo.

**Decisiones tomadas en sesión:**
- Proyecto correcto es `d0fc276d-e764-4a83-96e9-d65f086ed803`, el anterior (`a56a76e6-...`) se descarta.
- Auth endpoint correcto es `POST /api/auth/service-token` con response `.data.token` (según HO v2.1 script de PJM probado).
- Reassignments conservadores: solo flagueo 2 (MEM-022, MEM-039) — el resto de lo que me asignó PJM lo acepto aunque podría discutirse.

---

## 10. TEMPLATE PARA ACTUALIZAR ESTE ARCHIVO AL CIERRE DE SESIÓN

```markdown
### YYYY-MM-DD — <título sesión>

**Hecho:**
- ...

**Pendiente próxima sesión:**
- ...

**Blockers nuevos:**
- ...

**Escalaciones:**
- ...
```

---

**Regla:** este archivo es **el estado operativo vivo** del TL. Se actualiza al inicio y al cierre de cada sesión. Si está desactualizado más de 3 días, regenerar desde VTT con los comandos de `OPERATIVO_TECH_LEAD.md §5`.
