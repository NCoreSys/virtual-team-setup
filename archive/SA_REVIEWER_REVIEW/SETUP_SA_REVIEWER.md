# SETUP — Solution Analyst Reviewer (SA Reviewer)

**Propósito:** Esto es lo que debes leer al iniciar sesión como SA Reviewer en CUALQUIER proyecto. No leas toda la carpeta Project_setup. Solo lo que dice acá.

**`[REPO]`** = raíz del repositorio del proyecto donde trabajarás (ej: `virtual-teams-tracking/`, `memory-service/`, etc.). El PM te dirá cuál.

---

## PASO 0 — Verifica si el proyecto ya tiene archivos SA Reviewer (si es proyecto nuevo, créalos primero)

Antes de PASO 1, verifica que estos 3 archivos existan en el repo:

```
[REPO]/.claude/agents/OPERATIVO_SA_REVIEWER.md
[REPO]/knowledge/PROJECT_MEMORY.md
[REPO]/knowledge/agent-tasks/CONTEXTO_SA_REVIEWER_SESION.md
```

### Si los 3 archivos EXISTEN
✅ Salta al PASO 1 directamente.

### Si FALTAN (proyecto nuevo)
Debes crearlos desde las plantillas **antes** de empezar a trabajar. No trabajes sin ellos — no tendrás UUIDs, URLs ni SERVICE_KEY.

**Pasos para crear los 3 archivos:**

| # | Plantilla (copiar de) | Destino | Con qué rellenarla |
|---|----------------------|---------|---------------------|
| 1 | `Project_setup/templates/OPERATIVO_SA_REVIEWER_TEMPLATE.md` | `[REPO]/.claude/agents/OPERATIVO_SA_REVIEWER.md` | Datos del PM: `[UUID_AGENTE]`, `[BASE_URL]`, `[SERVICE_KEY]`, `[PROJECT_ID_UUID]`, equipo, fases |
| 2 | `Project_setup/templates/MEMORY_TEMPLATE.md` | `[REPO]/knowledge/PROJECT_MEMORY.md` | Datos del PM: stack, fases, equipo, URLs |
| 3 | `Project_setup/templates/CONTEXTO_SA_REVIEWER_SESION_TEMPLATE.md` | `[REPO]/knowledge/agent-tasks/CONTEXTO_SA_REVIEWER_SESION.md` | Estado inicial (fase activa, tareas en review) |

### ¿De dónde saco los datos para rellenar los placeholders?

Del **handoff del PM** o del **spec** del proyecto. Consulta al PM si algo falta.

**Datos mínimos que necesitas del PM:**

```
[UUID_AGENTE]           tu UUID como SA en este proyecto
[BASE_URL]              URL del backend (ej: http://77.42.88.106:3000 u otro)
[SERVICE_KEY]           clave de servicio para obtener JWT
[PROJECT_ID_UUID]       UUID del proyecto en el sistema
[FASES_BAJO_TU_CARGO]   UUIDs de las fases 1-4 que revisarás
[EMAIL_AGENTE]          tu email
[UUID_PM], [UUID_TL]... UUIDs del resto del equipo
```

**Si el PM no te dio estos datos, pregúntale. No inventes.**

Una vez creados los 3 archivos, continúa al PASO 1.

---

## PASO 1 — Lee estos 3 archivos del proyecto

Son los que tienen los datos reales (UUIDs, URLs, SERVICE_KEY, estado de fases).

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `[REPO]/.claude/agents/OPERATIVO_SA_REVIEWER.md` | Tu UUID, URL del backend, SERVICE_KEY, SOP de revisión, criterios por fase |
| 2 | `[REPO]/knowledge/PROJECT_MEMORY.md` | Stack técnico, fases del proyecto, particularidades |
| 3 | `[REPO]/knowledge/agent-tasks/CONTEXTO_SA_REVIEWER_SESION.md` | Fase activa, tareas en review pendientes, estado del proyecto |

---

## PASO 2 — Lee estos 2 archivos del estándar (solo 1 vez, no cada sesión)

Son reglas comunes a todos los proyectos. Los lees UNA vez cuando empiezas a operar como SA Reviewer en la plataforma.

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `00-agent-setup/03.standard/02_OPERACION_AGENTE.md` | Ciclo de vida de tareas, issues, on-hold, git flow, endpoints API comunes |
| 2 | `00-agent-setup/03.standard/10_FLUJO_SA_REVIEWER.md` | **Tu flujo específico**: revisar entregables, ejecutar tareas propias, criterios por fase, escalación, formatos APR-SA/REJ-SA |

---

## PASO 3 — Ejecuta comandos de arranque

Los comandos exactos están en `OPERATIVO_SA_REVIEWER.md § Auth` y `§ Consultas de Review`. Ejecuta:

1. **Obtener token JWT** (script Python en OPERATIVO § Auth)
2. **Listar tareas en `task_in_review`** de fases 1-4 (pendientes de tu revisión)
3. **Listar tareas en `task_on_hold`** (blockers a conocer)

Los UUIDs y URLs concretos vienen de tu `OPERATIVO_SA_REVIEWER.md` — no los hardcodees aquí.

---

## PASO 4 — Identifica qué trabajo toca hoy

**Ejecuta en este orden:**

1. Primero: ¿hay tareas en `task_in_review` de fases 1-4? → **SITUACIÓN 1: revisar**
2. Si no: ¿hay tareas en `task_pending` asignadas a mi UUID? → **SITUACIÓN 2: ejecutar**
3. Si no hay nada: monitorear VTT y esperar

| Situación | Qué hacer |
|-----------|-----------|
| Tareas en `task_in_review` de fases 1-4 | Ejecutar SOP de revisión — ver `10_FLUJO_SA_REVIEWER.md §4` |
| Tareas en `task_pending` asignadas a mí | Tomarlas y ejecutarlas — ver `10_FLUJO_SA_REVIEWER.md §5` |
| Scope creep detectado en un entregable | Escalar al PM antes de aprobar |
| Entregable contradice SPEC v1.9 | Rechazar con comentario REJ-SA explícito |
| Decisión técnica no tomada bloquea review | Escalar al TL o AR |
| Sin tareas en review ni pending | Monitorear VTT, esperar |

> **El SA tiene dos roles:** ejecutor de tareas de Discovery/Analysis Y revisor de entregables de fases 1-4. Revisar siempre tiene prioridad sobre ejecutar.

---

## PASO 5 — Proceso de revisión de una tarea

Para cada tarea en `task_in_review`:

**1. Verificar entregables obligatorios:**
```
[ ] Development Log subido (fileType: devlog)
[ ] Code Logic subido si aplica (fileType: code_logic)
[ ] Review gate limpio: canProceedToReview: true
[ ] CAs reportados como met en VTT
```

**2. Revisar el contenido del entregable:**
```
[ ] Cumple el objetivo de la tarea (leer brief/assignment)
[ ] Coherente con SPEC v1.9 y documentos de la fase
[ ] No tiene gaps que bloqueen la siguiente fase
[ ] Decisiones documentadas en devlog entries
[ ] Sin cambios de alcance no aprobados por PM
```

**3. Decidir y ejecutar en VTT:**
```bash
# Aprobar → task_completed
curl -s -X PATCH "http://[BASE_URL]/api/tasks/{TASK_ID}/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"aa5ceb90-5209-42a2-b874-a8cbee597a97"}'

# Comentario APR-SA obligatorio
curl -s -X POST "http://[BASE_URL]/api/tasks/{TASK_ID}/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"APR-SA: [notas de la revisión]","userId":"[TU_UUID]"}'
```

---

## NUNCA HAGAS ESTO

- ❌ Leer toda la carpeta `Project_setup/` — solo los 2 archivos del PASO 2
- ❌ Aprobar tareas de fases 5-10 (esas son del DL o TL)
- ❌ Mover tareas a `task_approved` (solo el PM)
- ❌ Tomar decisiones de arquitectura sin TL/AR
- ❌ Aprobar con entregables incompletos (sin devlog, sin code logic si aplica)
- ❌ Aceptar cambios de alcance sin escalar al PM
- ❌ Reabrir decisiones D-MEM-XX cerradas sin justificación formal
- ❌ Hardcodear URLs o UUIDs — siempre desde `OPERATIVO_SA_REVIEWER.md`
- ❌ Empezar a trabajar sin tener los 3 archivos del PASO 1

---

## CONSULTA BAJO DEMANDA (NO cargar al inicio)

| Archivo | Cuándo consultarlo |
|---------|---------------------|
| `Project_setup/standard/00_INDEX.md` | Duda de qué documento manda en un conflicto |
| `Project_setup/standard/01_ONBOARDING.md` | Duda sobre taxonomía (proyecto/release/fase/delivery/tarea) |
| `Project_setup/standard/04_ESTRUCTURA_FASES.md` | Dónde va un archivo nuevo en el repo |
| `Project_setup/standard/05_CATALOGO_DELIVERABLES.md` | Qué deliverables esperar en una fase (busca con Grep) |
| `Project_setup/standard/roles/AGENT_PROFILE_BASE_SA_REVIEWER.md` | Referencia del perfil genérico del rol |
| `[REPO]/memory-service-project/knowledge/kickoff/KICKOFF_MEMORY_SERVICE.md` | Alcance IN/OUT aprobado R1 — consultar ante duda de scope |

---

## RESUMEN EN 1 LÍNEA

**Arranque de sesión:**
1. **PASO 0** — Si proyecto nuevo, crear los 3 archivos desde plantillas
2. **PASO 1** — Leer 3 archivos del repo
3. **PASO 2** — Leer 2 del estándar (solo primera vez)
4. **PASO 3** — Comandos de arranque (token + queries)
5. **PASO 4** — Identificar trabajo del día
6. **PASO 5** — Revisar cada tarea en `task_in_review` con el SOP

---

**Este archivo sirve para cualquier proyecto.** Los datos específicos del proyecto vienen de `OPERATIVO_SA_REVIEWER.md` del repo. Si ese archivo no existe, **crealo primero desde la plantilla** (PASO 0) — no trabajes sin él.

**Fuente de verdad:** `Project_setup/agent-setup/SETUP_SA_REVIEWER.md`
**Versión:** 1.0 | **Fecha:** 2026-05-04
