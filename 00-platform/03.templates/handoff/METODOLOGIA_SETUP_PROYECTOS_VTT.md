# METODOLOGIA: Setup de Proyectos en VTT

**Version:** 1.0
**Fecha:** 2026-04-20
**Autor:** Martin Rivas (PM)
**Proposito:** Playbook reutilizable para setear cualquier proyecto nuevo en VTT (Virtual Teams Tracking) con sus fases SDLC, deliverables, tareas y bootstrap de repo.

---

## 0. OBJETIVO

Estandarizar el proceso de creacion de un proyecto desde cero en VTT, desde el alta del proyecto hasta la carga de tareas en cada deliverable, dejando el repo listo para que los agentes empiecen a trabajar.

**Resultado esperado al final:**
- Proyecto activo en VTT con 10 fases (Project Setup + 9 SDLC)
- Todos los deliverables creados por fase
- Tareas cargadas con agentes asignados, horas estimadas y prioridad
- Repo local inicializado con estructura estandar
- HO (Handoff) consolidado listo para el PJM

---

## 1. PRERREQUISITOS

### 1.1 Acceso y credenciales

| Item | Detalle |
|------|---------|
| URL VTT | http://77.42.88.106:3000 |
| Cuenta PJM | pjm@<proyecto>.vtt.ai |
| SERVICE_KEY | Proveida por admin VTT |
| UUID PJM | Obtenido al crear usuario |

### 1.2 Catalogos VTT (compartidos entre proyectos)

**Prioridades** (UUIDs globales):

| Prioridad | UUID |
|-----------|------|
| low | obtener via GET /api/priorities |
| medium | d0b619ef-27e7-42d8-8879-41030a602eed |
| high | 1a617554-6319-4c56-826f-8ef49a0ff9cc |
| critical | 90ec3df2-fac4-40fa-b2ce-29daf0f4956e |

**Valores validos task:**
- complexity: LOW | MEDIUM | HIGH
- category: development | design | testing | documentation | review | bugfix | deployment
- type: feature | bug | research | documentation | chore

### 1.3 Agentes del proyecto

Cada proyecto debe tener sus agentes registrados en VTT con siglas estandar:

| Sigla | Rol | Cuando se usa |
|-------|-----|---------------|
| PM | Product Manager | Siempre |
| PJM | Project Manager | Siempre |
| SA | Solution Architect | Proyectos con analisis formal |
| TL | Tech Lead | Proyectos con codigo |
| AR | Architect | Proyectos con arquitectura compleja |
| DB | Database Engineer | Proyectos con BD |
| BE | Backend Developer | Proyectos con backend |
| FE | Frontend Developer | Proyectos con UI |
| DL | Design Lead | Proyectos con UI |
| UX | UX Designer | Proyectos con UX formal |
| QA | QA Engineer | Siempre que haya codigo |
| DO | DevOps | Proyectos con deploy |

**Guardar los UUIDs de los 12 agentes al inicio — se usan en cada llamada de creacion de tarea.**

---

## 2. FLUJO MAESTRO — 7 PASOS

```
PASO 1: Discovery de alcance y decisiones tecnicas
   |
   v
PASO 2: Crear proyecto + 10 fases en VTT
   |
   v
PASO 3: Crear deliverables estandar por fase
   |
   v
PASO 4: Consolidar plan (master SDLC + analisis tecnico si existe)
   |
   v
PASO 5: Generar HO para PJM con tareas detalladas
   |
   v
PASO 6: PJM crea tareas en VTT via API
   |
   v
PASO 7: DO ejecuta bootstrap del repo (Project Setup)
```

---

## 3. PASO 1 — DISCOVERY

Antes de tocar VTT, responder por escrito:

- [ ] Nombre del proyecto y key (MEM, FOO, BAR...)
- [ ] Fechas inicio y fin objetivo
- [ ] Duracion de sprint (2 semanas estandar)
- [ ] Stakeholders y roles necesarios (cuales agentes de la lista 1.3)
- [ ] Existe analisis tecnico previo? (SPEC, reviews, plan aprobado)
- [ ] Requiere UI? → incluir FE + DL + UX
- [ ] Requiere BD? → incluir DB
- [ ] Requiere deploy? → incluir DO
- [ ] Hay dependencias con otros proyectos?

**Output del paso 1:** documento `PROJECT_KICKOFF_<KEY>.md` con respuestas.

---

## 4. PASO 2 — CREAR PROYECTO + 10 FASES EN VTT

### 4.1 Estructura estandar de fases

| Order | Fase | Cuando se usa |
|-------|------|---------------|
| 1 | Project Setup | Siempre (bootstrap repo) |
| 2 | Discovery | Siempre |
| 3 | Planning | Siempre |
| 4 | Analysis | Siempre |
| 5 | Design UX/UI | Si hay UI |
| 6 | Design Technical | Siempre |
| 7 | Development | Siempre |
| 8 | Testing | Siempre |
| 9 | Deploy | Siempre que haya codigo |
| 10 | Operations | Post-MVP |

### 4.2 Script base

```python
import urllib.request, json

BASE_URL = "http://77.42.88.106:3000"
PJM_ID = "<uuid-del-PJM>"
SK = "<service-key>"

# Auth
r = urllib.request.urlopen(urllib.request.Request(
    BASE_URL + "/api/auth/service-token",
    data=json.dumps({"userId": PJM_ID, "serviceKey": SK}).encode(),
    headers={"Content-Type": "application/json"}, method="POST"))
TOKEN = json.loads(r.read())["data"]["token"]
HEADERS = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}

# Crear proyecto
proj_body = {
    "name": "<Nombre Proyecto>",
    "key": "<KEY>",
    "description": "...",
    "startDate": "2026-MM-DD",
    "endDate": "2026-MM-DD"
}
r = urllib.request.urlopen(urllib.request.Request(
    BASE_URL + "/api/projects",
    data=json.dumps(proj_body).encode(),
    headers=HEADERS, method="POST"))
PROJECT_ID = json.loads(r.read())["data"]["id"]

# Crear 10 fases — IMPORTANTE: order=1 para Project Setup
phases_spec = [
    (1,  "Project Setup",     "Bootstrap del repositorio"),
    (2,  "Discovery",         "Problema, propuesta de valor"),
    (3,  "Planning",          "Vision, scope, riesgos, timeline"),
    (4,  "Analysis",          "Requisitos, user stories, reglas"),
    (5,  "Design UX/UI",      "Personas, wireframes, mockups"),
    (6,  "Design Technical",  "Arquitectura, BD, API, ADRs"),
    (7,  "Development",       "Implementacion por sprints"),
    (8,  "Testing",           "QA, performance, security, UAT"),
    (9,  "Deploy",            "CI/CD, staging, produccion"),
    (10, "Operations",        "Monitoreo, soporte, mejoras"),
]

phase_ids = {}
for order, name, desc in phases_spec:
    r = urllib.request.urlopen(urllib.request.Request(
        BASE_URL + f"/api/projects/{PROJECT_ID}/phases",
        data=json.dumps({"name": name, "description": desc, "order": order}).encode(),
        headers=HEADERS, method="POST"))
    phase_ids[name] = json.loads(r.read())["data"]["id"]
    print(f"OK {order:2d} {name}")
```

### 4.3 Si algo sale mal con el order

Si tras crear las fases notas que una quedo en la posicion incorrecta:

```python
# Usar el endpoint de reorder (batch)
import urllib.request, json

body = {
    "phaseIds": [id_order1, id_order2, ..., id_order10]  # en el orden deseado
}
req = urllib.request.Request(
    BASE_URL + f"/api/projects/{PROJECT_ID}/phases/reorder",
    data=json.dumps(body).encode(),
    headers=HEADERS, method="PATCH")
urllib.request.urlopen(req)
```

**Nota critica:** `PUT /api/phases/{id}` **NO actualiza `order`** (bug conocido — silenciosamente lo ignora). El unico endpoint que reordena es `PATCH /api/projects/{id}/phases/reorder`.

---

## 5. PASO 3 — CREAR DELIVERABLES ESTANDAR POR FASE

### 5.1 Matriz estandar de deliverables

| Fase | Deliverables estandar |
|------|----------------------|
| Project Setup | (1) Repo + estructura, (2) TASK_TRACKING, (3) Templates, (4) .env + docker-compose, (5) Briefs iniciales |
| Discovery | (1) Problem Definition, (2) Value Proposition |
| Planning | (1) Vision, (2) Scope, (3) Stakeholders, (4) Risks, (5) Timeline, (6) Budget |
| Analysis | (1) Functional Req, (2) Non-Functional Req, (3) Use Cases, (4) User Stories, (5) Business Rules, (6) User Flows, (7) Acceptance Criteria, (8) Traceability Matrix |
| Design UX/UI | (1) Personas, (2) Information Architecture, (3) Wireframes, (4) Mockups, (5) Design System, (6) Design Handoff |
| Design Technical | (1) Solution Arch, (2) Code Arch, (3) DB Design, (4) API Design, (5) Sequence Diagrams, (6) ADRs, (7) Security Plan, (8) Infra Plan, (9) Tech Estimates |
| Development | Un deliverable por sprint (ej. S01 Schema, S02 Auth, UI-01 Setup...) |
| Testing | (1) Test Planning, (2) Test Cases, (3) Test Env, (4-9) Test execution types, (10) UAT, (11) Bug Fixes |
| Deploy | (1) Infra Setup, (2) CI/CD, (3) Staging, (4) Smoke Test, (5) Prod Deploy, (6) Monitoring, (7) Rollback Plan |
| Operations | (1) Monitoring, (2) User Support, (3) Bug Fixes Ops, (4) Incremental Improvements, (5) Security Updates, (6) Scaling |

### 5.2 Script para crear deliverables

```python
# Deliverables son "tareas" en VTT, asignadas a una fase
def create_deliverable(phase_id, title, priority_id, complexity, category, order, assignee_id=None):
    body = {
        "title": title,
        "priorityId": priority_id,
        "complexity": complexity,
        "category": category,
        "type": "documentation",
        "order": order,
        "estimatedHours": 1,  # placeholder, se actualiza despues
    }
    if assignee_id:
        body["assigneeId"] = assignee_id
    req = urllib.request.Request(
        BASE_URL + f"/api/phases/{phase_id}/tasks",
        data=json.dumps(body).encode(),
        headers=HEADERS, method="POST")
    return json.loads(urllib.request.urlopen(req).read())["data"]["id"]
```

---

## 6. PASO 4 — CONSOLIDAR PLAN

### 6.1 Si existe analisis tecnico previo

Cuando el proyecto ya tiene SPEC, reviews (AR/DB/TL), y un HO de plan aprobado con sprints concretos, **NO duplicar tareas**. Consolidar asi:

1. Usar el plan maestro SDLC (fases Discovery, Planning, Analysis, 3B, Testing, Deploy, Operations + UX)
2. Usar el analisis aprobado SOLO para Design UX/UI DL + Development (tareas concretas)
3. Agregar columna `Origen` a cada tabla de tareas:
   - `maestro` = plan SDLC generico
   - `ANALISIS` = plan aprobado especifico

### 6.2 Si NO existe analisis previo

Usar templates genericos del plan maestro en todas las fases. El analisis tecnico se hara como parte de Phase 4 (Analysis) y Phase 6 (Design Technical) del propio proyecto.

### 6.3 Estructura del HO consolidado

Archivo: `<proyecto>/Release<X>/PJM/HANDOFF_PJM_SPRINT_SETUP_VTT.md`

Secciones obligatorias:
1. Contexto + datos proyecto (Project ID, credenciales, calendario)
2. Phase IDs (tabla de 10 UUIDs)
3. Deliverables (tabla ID → Fase → Nombre)
4. Agentes y UUIDs + Prioridades
5. Calendario de sprints (Pre-Sprint + Sprint 0-N)
6. API para crear tareas (con body ejemplo)
7. Tareas detalladas por fase (con columna Origen)
8. Resumen de horas (por fase y por rol)
9. Dependencias criticas (ASCII diagram)
10. Checklist PJM
11. Documentos de referencia

---

## 7. PASO 5 — GENERAR HO PARA PJM

El HO es **el unico input que el PJM necesita** para crear tareas en VTT. Debe ser autocontenido:

- Credenciales (PJM UUID, SERVICE_KEY, BASE_URL)
- Phase UUIDs listos para copiar al body
- Agent UUIDs para `assigneeId`
- Priority UUIDs para `priorityId`
- Tablas con `title | agente | horas | complexity | category | origen | deliverable`

**Checklist de calidad del HO:**
- [ ] Todas las tareas tienen agente asignado
- [ ] Todas las tareas tienen horas estimadas
- [ ] Todas las tareas tienen complexity y category validos
- [ ] Dependencias criticas documentadas
- [ ] Calendario con fechas reales (no "TBD")

---

## 8. PASO 6 — PJM CREA TAREAS EN VTT

Script tipo del PJM:

```python
def create_task(phase_id, title, assignee, hours, complexity, category, order, priority=MEDIUM):
    body = {
        "title": title,
        "priorityId": priority,
        "complexity": complexity,
        "category": category,
        "type": "feature",
        "order": order,
        "estimatedHours": hours,
        "assigneeId": assignee
    }
    req = urllib.request.Request(
        BASE_URL + f"/api/phases/{phase_id}/tasks",
        data=json.dumps(body).encode(),
        headers=HEADERS, method="POST")
    r = urllib.request.urlopen(req)
    return json.loads(r.read())["data"]

# Iterar por cada fase leyendo la tabla del HO
for row in parse_ho_tables():
    create_task(
        phase_id=PHASES[row["fase"]],
        title=row["titulo"],
        assignee=AGENTS[row["agente"]],
        hours=row["horas"],
        complexity=row["complexity"],
        category=row["category"],
        order=row["order"]
    )
```

---

## 9. PASO 7 — BOOTSTRAP DEL REPO (Project Setup)

El DO ejecuta las 5 tareas de Phase 1:

```bash
# Tarea 1: estructura de carpetas
mkdir -p <proyecto>/{src,docs/context,knowledge/development-log,knowledge/code-logic,_project-management/briefs,_project-management/templates,prisma}
git init

# Tarea 2: TASK_TRACKING.md
# Exportar desde VTT las tareas con GET /api/tasks?projectId=X
# Generar tabla markdown con estados iniciales

# Tarea 3: templates
cp ~/.claude/templates/TEMPLATE_CODE_LOGIC.md <proyecto>/_project-management/templates/
cp ~/.claude/templates/TEMPLATE_DEVELOPMENT_LOG.md <proyecto>/_project-management/templates/

# Tarea 4: config base
# - .env.example con variables placeholder
# - .gitignore con node_modules, .env, /dist, /build
# - docker-compose.yml con Postgres + servicio base

# Tarea 5: briefs iniciales
# Un brief por tarea en _project-management/briefs/<TASK_ID>_<nombre>.md
```

---

## 10. LECCIONES APRENDIDAS (Gotchas)

### 10.1 API de VTT

| Gotcha | Solucion |
|--------|----------|
| `POST /api/projects` acepta array `deliverables` pero lo ignora | Crear deliverables uno por uno via `POST /api/phases/{id}/tasks` |
| `PUT /api/phases/{id}` devuelve 200 pero no actualiza `order` | Usar `PATCH /api/projects/{id}/phases/reorder` |
| `POST /api/phases` permite `order` duplicado sin error | Validar unicidad antes de crear |
| `order` debe ser entero positivo (>= 1) | No usar 0 |
| Response de GET phases esta anidada: `resp.data.data` | Acceder `resp["data"]["data"]` |
| Crear task requiere `priorityId` como UUID (no string "medium") | Obtener UUIDs via GET /api/priorities al inicio |
| Bash en Windows no reconoce /tmp, usar paths Windows | `c:/Users/Martin/...` en scripts Python |

### 10.2 Consolidacion de planes

- **Nunca duplicar tareas** entre el plan maestro SDLC y el analisis tecnico. Usar columna `Origen` para marcar fuente.
- **Mantener solo UN HO** para el PJM (no crear varios que confundan).
- Tareas UX genericas (Personas, Sitemap) del maestro **no chocan** con tareas DL especificas del analisis (wireframes, tokens). Se complementan.
- Las tareas del maestro en Development son placeholders — se reemplazan completas con las del analisis aprobado.

### 10.3 Estructura de carpetas por proyecto

```
<proyecto>/
├── src/                             # codigo
├── docs/context/                    # docs de entrada (git)
├── knowledge/                       # docs de salida (NO git)
│   ├── development-log/
│   └── code-logic/                  # espejo de /src
├── _project-management/
│   ├── briefs/                      # un brief por tarea
│   ├── templates/
│   └── reportes/
├── prisma/                          # si aplica
└── TASK_TRACKING.md                 # local, se sincroniza con VTT
```

### 10.4 Commit convention

```
[tipo](<repo>) [TASK_ID]: Descripcion breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Refs: #<TASK_ID>
```

Tipos: feat | fix | docs | refactor | test | chore

---

## 11. CHECKLIST FINAL DE SETUP

Antes de notificar que el proyecto esta listo para arrancar:

### Proyecto VTT
- [ ] Proyecto creado con nombre, key, fechas
- [ ] 10 fases con orders 1-10 correctos (verificar con GET)
- [ ] Deliverables estandar creados por fase
- [ ] Tareas detalladas cargadas con agente, horas, complexity, category
- [ ] Prioridad asignada a cada tarea
- [ ] Total de tareas coincide con HO (`GET /api/tasks?projectId=X`)

### Repo local
- [ ] Estructura de carpetas estandar
- [ ] .git inicializado
- [ ] .env.example con variables placeholder
- [ ] .gitignore con exclusiones estandar
- [ ] docker-compose.yml base
- [ ] Templates copiados
- [ ] TASK_TRACKING.md generado con tareas en estado 🟡 pending / 🔴 blocked segun dependencias

### Documentacion
- [ ] PROJECT_KICKOFF_<KEY>.md
- [ ] HANDOFF_PJM_SPRINT_SETUP_VTT.md (consolidado)
- [ ] Briefs iniciales por tarea critica
- [ ] Readme con como levantar el proyecto local

### Notificacion
- [ ] PJM recibio el HO y confirmo entender
- [ ] DO recibio asignacion de Phase 1 y arranco
- [ ] Kickoff reunion con todos los agentes (opcional)

---

## 12. PLANTILLAS RAPIDAS

### 12.1 PROJECT_KICKOFF_<KEY>.md

```markdown
# PROJECT KICKOFF: <Nombre>

## Datos basicos
- Key: <KEY>
- Inicio: YYYY-MM-DD
- Fin objetivo: YYYY-MM-DD
- Sprint: 2 semanas

## Alcance
- En scope: ...
- Out of scope: ...

## Agentes necesarios
- PM, PJM, TL, BE, DB, FE, QA, DO, DL (marcar los que aplican)

## Analisis previo existente?
- Si / No
- Si si: listar docs (SPEC, reviews, HO plan aprobado)

## Dependencias con otros proyectos
- ...

## Riesgos iniciales
- ...
```

### 12.2 HO_PJM para proyecto sin analisis previo

Todas las tareas son `Origen=maestro`. Copiar el HO de Memory Service quitando secciones del analisis y usar tareas genericas por fase.

### 12.3 HO_PJM para proyecto con analisis previo

Copiar estructura de `memory-service/Release2.0/PJM/HANDOFF_PJM_SPRINT_SETUP_VTT.md`:
- Seccion 7.X para cada fase con columna Origen
- Seccion 7.0 Project Setup siempre presente
- Seccion 7 Development con tareas ANALISIS detalladas

---

## 13. REFERENCIAS

- Memory Service (ejemplo completo): `memory-service/memory-service-project/Release2.0/PJM/`
- Reglas de agentes: `~/.claude/rules/rules_agents.instructions.md`
- Templates globales: `~/.claude/templates/` (crear si no existe)
- VTT API docs: `http://77.42.88.106:3000/api-docs`

---

## 14. PROXIMAS MEJORAS (backlog de esta metodologia)

- [ ] Script unico `setup_new_project.py` que tome un YAML de configuracion y ejecute los pasos 2-6 automaticamente
- [ ] Template generador de briefs a partir de la tabla de tareas del HO
- [ ] Integracion con Hook Manager VTT para poblar Memory Service al arrancar el proyecto
- [ ] Dashboard de salud inicial (fases creadas, tareas pendientes, agentes asignados)

---

**Estado:** v1.0 funcional, probada en Memory Service
**Siguiente iteracion:** aplicar en los proximos 2 proyectos y ajustar gotchas detectados
