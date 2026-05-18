# SETUP — Tech Lead

**Propósito:** Esto es lo que debes leer al iniciar sesión como Tech Lead en CUALQUIER proyecto. No leas toda la carpeta Project_setup. Solo lo que dice acá.

**`[REPO]`** = raíz del repositorio del proyecto donde trabajarás (ej: `virtual-teams-tracking/`, `memory-service/`, etc.). El PM te dirá cuál.

---

## PASO 0 — Verifica si el proyecto ya tiene archivos TL (si es proyecto nuevo, créalos primero)

Antes de PASO 1, verifica que estos 3 archivos existan en el repo:

```
[REPO]/.claude/agents/OPERATIVO_TECH_LEAD.md
[REPO]/knowledge/PROJECT_MEMORY.md
[REPO]/knowledge/agent-tasks/CONTEXTO_TL_SESION.md
```

### Si los 3 archivos EXISTEN
✅ Salta al PASO 1 directamente.

### Si FALTAN (proyecto nuevo)
Debes crearlos desde las plantillas **antes** de empezar a trabajar. No trabajes sin ellos — no tendrás UUIDs, URLs ni SERVICE_KEY.

**Pasos para crear los 3 archivos:**

| # | Plantilla (copiar de) | Destino | Con qué rellenarla |
|---|----------------------|---------|---------------------|
| 1 | `Project_setup/templates/OPERATIVO_TL_TEMPLATE.md` | `[REPO]/.claude/agents/OPERATIVO_TECH_LEAD.md` | Datos del handoff del PM: `[UUID_AGENTE]`, `[BASE_URL]`, `[SERVICE_KEY]`, `[PROJECT_ID_UUID]`, equipo, fases |
| 2 | `Project_setup/templates/MEMORY_TEMPLATE.md` | `[REPO]/knowledge/PROJECT_MEMORY.md` | Datos del handoff del PM: stack, fases, equipo, URLs |
| 3 | `Project_setup/templates/CONTEXTO_TL_SESION_TEMPLATE.md` | `[REPO]/knowledge/agent-tasks/CONTEXTO_TL_SESION.md` | Estado inicial (sprint 0 o sprint activo, tareas aún no creadas) |

### ¿De dónde saco los datos para rellenar los placeholders?

Del **handoff del PM** (`HANDOFF_TL_S[XX].md` o `HO_PJM_PLAN_SPRINTS_*.md`), del **spec** del proyecto, y consultando al PM si algo falta.

**Datos mínimos que necesitas del PM:**

```
[UUID_AGENTE]           tu UUID como TL en este proyecto
[BASE_URL]              URL del backend (ej: http://77.42.88.106:3000 u otro)
[SERVICE_KEY]           clave de servicio para obtener JWT
[PROJECT_ID_UUID]       UUID del proyecto en el sistema
[UUID_FASE_ACTIVA]      UUID de la fase donde trabajarás
[EMAIL_AGENTE]          tu email
[UUID_PM], [UUID_DL]... UUIDs del resto del equipo
```

**Si el PM no te dio estos datos, pregúntale. No inventes.**

Una vez creados los 3 archivos, continúa al PASO 1.

---

## PASO 1 — Lee estos 3 archivos del proyecto

Son los que tienen los datos reales (UUIDs, URLs, SERVICE_KEY, estado del sprint).

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `[REPO]/.claude/agents/OPERATIVO_TECH_LEAD.md` | Tu UUID, URL del backend, SERVICE_KEY, comandos curl/python listos, equipo del proyecto |
| 2 | `[REPO]/knowledge/PROJECT_MEMORY.md` | Stack técnico, fases del proyecto, particularidades |
| 3 | `[REPO]/knowledge/agent-tasks/CONTEXTO_TL_SESION.md` | Estado actual del sprint, tareas en curso, pendientes |

---

## PASO 2 — Lee estos 2 archivos del estándar (solo 1 vez, no cada sesión)

Son reglas comunes a todos los proyectos. Los lees UNA vez cuando empiezas a operar como TL en la plataforma y los recuerdas.

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `Project_setup/standard/02_OPERACION_AGENTE.md` | Ciclo de vida de tareas, issues, on-hold, git flow, endpoints API comunes |
| 2 | `Project_setup/standard/03_FLUJO_TL.md` | Tu flujo de trabajo: FASE 1 (planificar) y FASE 2 (asignar), los 8 elementos del ASSIGNMENT, cómo hacer code review |

---

## PASO 3 — Ejecuta comandos de arranque

Los comandos exactos están en `OPERATIVO_TECH_LEAD.md § Auth` y `§ Cambios de Status`. Ejecuta:

1. **Obtener token JWT** (script Python en OPERATIVO § Auth)
2. **Listar tus tareas asignadas** (`GET /api/tasks?assigneeId={TU_UUID}`)
3. **Listar tareas en `task_in_review`** (pendientes de tu review)
4. **Listar tareas en `task_on_hold`** (blockers a conocer)

Los UUIDs y URLs concretos vienen de tu `OPERATIVO_TECH_LEAD.md` — no los hardcodees aquí.

---

## PASO 4 — Identifica qué trabajo toca hoy

| Situación | Qué hacer |
|-----------|-----------|
| PM te pasa handoff nuevo | FASE 1: planear + crear BRIEFs (ver `03_FLUJO_TL.md` §2-3) |
| Hay tareas listas para asignar | FASE 2: escribir ASSIGNMENT (ver §5-8 y PASO 5 abajo) |
| Hay tareas en `task_in_review` | Code review (ver checklist en `OPERATIVO_TECH_LEAD.md § Proceso de Code Review`) |
| Hay escalación del PJM/DL | Resolver primero, luego seguir |

---

## PASO 5 — Solo si vas a escribir un ASSIGNMENT (FASE 2)

NO leas todo el código. Lee **solo los archivos relevantes a esa tarea específica**:

| Tipo de tarea | Lee estos archivos del repo |
|---------------|------------------------------|
| **FE** | `frontend/src/router/index.tsx` + `backend/src/routes/[modulo].ts` + `frontend/src/components/features/[Modulo]*.tsx` + `frontend/src/hooks/use[Modulo]*.ts` + `frontend/src/index.css` |
| **BE** | `backend/src/routes/[modulo].ts` + `backend/prisma/schema.prisma` + `backend/src/validators/[modulo].validator.ts` |
| **DB** | `backend/prisma/schema.prisma` + `backend/prisma/migrations/` (último) |
| **DevOps** | `docker-compose.yml` + `backend/.env.example` |

**Usa Glob/Grep primero para encontrar, luego Read solo el archivo específico.**

---

## NUNCA HAGAS ESTO

- ❌ Leer toda la carpeta `Project_setup/` — solo los 2 archivos del PASO 2
- ❌ Leer `backend/src/**/*` completo — usa Glob/Grep
- ❌ Leer `frontend/src/**/*` completo — usa Glob/Grep
- ❌ Leer `05_CATALOGO_DELIVERABLES.md` completo (1430 líneas) — busca la fase específica con Grep
- ❌ Leer handoffs o briefs de sprints anteriores sin necesidad
- ❌ Cargar `node_modules/`, `.git/`, `dist/`
- ❌ Hardcodear URLs o UUIDs — siempre desde `OPERATIVO_TECH_LEAD.md`
- ❌ Empezar a trabajar sin tener los 3 archivos del PASO 1 (PASO 0 es obligatorio en proyectos nuevos)

---

## CONSULTA BAJO DEMANDA (NO cargar al inicio)

Si durante la sesión necesitas algo específico, consulta solo la sección que necesitas:

| Archivo | Cuándo consultarlo |
|---------|---------------------|
| `Project_setup/standard/00_INDEX.md` | Duda de qué documento manda en un conflicto |
| `Project_setup/standard/01_ONBOARDING.md` | Duda sobre taxonomía (proyecto/release/fase/delivery/tarea) |
| `Project_setup/standard/04_ESTRUCTURA_FASES.md` | Dónde va un archivo nuevo en el repo |
| `Project_setup/standard/05_CATALOGO_DELIVERABLES.md` | Qué deliverables esperar en una fase (busca con Grep) |
| `Project_setup/standard/06_FLUJO_DL.md` | Si tienes que coordinar con el Design Lead |
| `Project_setup/standard/07_FLUJO_PJM.md` | Si recibes reporte del PJM |
| `Project_setup/standard/roles/AGENT_PROFILE_BASE_TL.md` | Referencia del perfil genérico del rol |
| `Project_setup/templates/` | Plantillas para crear artefactos nuevos |

---

## RESUMEN EN 1 LÍNEA

**Arranque de sesión:**
1. **PASO 0** — Si proyecto nuevo, crear los 3 archivos desde plantillas de `Project_setup/templates/`
2. **PASO 1** — Leer 3 archivos del repo
3. **PASO 2** — Leer 2 del estándar (solo primera vez)
4. **PASO 3** — Comandos de arranque (token + queries)
5. **PASO 4** — Identificar trabajo del día
6. **PASO 5** — Si asignas: lee solo lo relevante del codebase
7. Todo lo demás: consulta bajo demanda

---

**Este archivo sirve para cualquier proyecto.** Los datos específicos del proyecto vienen de `OPERATIVO_TECH_LEAD.md` del repo. Si ese archivo no existe, **crealo primero desde la plantilla** (PASO 0) — no trabajes sin él.

**Fuente de verdad:** `Project_setup/agent-setup/SETUP_TL.md`
**Versión:** 1.2 | **Fecha:** 2026-04-21
