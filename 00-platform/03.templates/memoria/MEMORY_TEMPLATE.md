# [PROJECT_NAME] — Agent Memory

> Plantilla de memoria de agente específica del proyecto.
> Reemplazar los placeholders `[...]` con datos reales.
> Las reglas operativas GENÉRICAS viven en `Project_setup/standard/` — este archivo solo contiene datos específicos del proyecto.

---

# 1. PROYECTO

- **Nombre**: [PROJECT_NAME]
- **Descripción**: [breve descripción del proyecto]
- **PM (Coordinador)**: [Nombre] — [email]
- **PM UUID**: `[UUID]`
- **Repo**: [URL del repositorio Git]
- **Branch principal**: `main`
- **Fecha kickoff**: [YYYY-MM-DD]

---

# 2. ARCHIVOS BASE DEL AGENTE

Cada sesión del agente carga estas capas:

| # | Archivo | Propósito | Capa |
|---|---------|-----------|------|
| 1 | **Este MEMORY.md** | Datos específicos del proyecto + estado actual | Proyecto |
| 2 | `C:\Users\Martin\.claude\rules\rules_agents.instructions.md` | Reglas globales de workflow | Global |
| 3 | `Project_setup/standard/00_INDEX.md` | Jerarquía de documentos | Estándar |
| 4 | `Project_setup/standard/02_OPERACION_AGENTE.md` | Operación común (ciclo vida, endpoints, git) | Estándar |
| 5 | `Project_setup/standard/[03_FLUJO_TL.md \| rol específico]` | Flujo específico del rol | Estándar |
| 6 | **Perfil operativo del rol** | `.claude/agents/OPERATIVO_[ROL].md` | Proyecto |

**Ubicación del onboarding pack del proyecto**: `[ruta al 00-platform del proyecto si existe]`

---

# 3. SISTEMA DE GESTIÓN

- **API Base URL**: `[http://IP:PUERTO]` (NUNCA localhost en producción)
- **Swagger**: `[http://IP:PUERTO/api-docs]`
- **Project ID**: `[UUID]`
- **SERVICE_KEY**: `[SERVICE_KEY]` (pedir al PM)

### Phase IDs
| Fase | Nombre | UUID |
|------|--------|------|
| [N] | [nombre_fase] | `[UUID]` |
| [N] | [nombre_fase] | `[UUID]` |

### Status UUIDs (globales — no cambian por proyecto)
| Status | UUID |
|--------|------|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

### Priority UUIDs (globales)
| Prioridad | UUID |
|-----------|------|
| critical | `90ec3df2-fac4-40fa-b2ce-29daf0f4956e` |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` |
| low | `95f2e731-41b9-4a7d-9a43-31f00a4ddd7e` |

---

# 4. EQUIPO

| Agente | Rol | userId | Email |
|--------|-----|--------|-------|
| [Nombre] | PM | `[UUID]` | [email] |
| [Nombre] | Tech Lead (TL) | `[UUID]` | [email] |
| [Nombre] | Project Manager (PJM) | `[UUID]` | [email] |
| [Nombre] | Backend (BE) | `[UUID]` | [email] |
| [Nombre] | Frontend (FE) | `[UUID]` | [email] |
| [Nombre] | Database (DB) | `[UUID]` | [email] |
| [Nombre] | DevOps (DO) | `[UUID]` | [email] |
| [Nombre] | QA Engineer | `[UUID]` | [email] |
| [Nombre] | Design Lead (DL) | `[UUID]` | [email] |
| [Nombre] | UX Designer | `[UUID]` | [email] |
| [Nombre] | Auditor Reviewer (AR) | `[UUID]` | [email] |
| [Nombre] | Integration Reviewer (IR) | `[UUID]` | [email] |

---

# 5. MI ROL — [ROLE_NAME]

- **UUID**: `[UUID]`
- **Email**: `[email]`
- **Perfil base**: `Project_setup/standard/roles/AGENT_PROFILE_BASE_[ROL].md`
- **Perfil operativo (instancia del proyecto)**: `[ruta en .claude/agents/]`

### Responsabilidades principales
1. [Responsabilidad 1]
2. [Responsabilidad 2]
3. [Responsabilidad 3]

### Lo que NO hago
- [Fuera de alcance 1]
- [Fuera de alcance 2]

---

# 6. STACK TÉCNICO

- **Frontend**: [framework + versión + librerías clave]
- **Backend**: [framework + versión + ORM]
- **Base de datos**: [motor + versión]
- **Infraestructura**: [Docker, VM, servicios]
- **Router FE**: [archivo del router principal]
- **Auth FE**: [hook/pattern usado, ej. `useAuth()` → `user.id`]

### Design Tokens
> Algunos proyectos tienen **un único** sistema; otros separan Landing (marketing) de App (producto).

| Contexto | Tokens | Ubicación |
|----------|--------|-----------|
| [Landing / App / Único] | [descripción del tema] | `[ruta al archivo de tokens]` |

**REGLAS DE DISEÑO:**
- ❌ NO mezclar tokens entre Landing y App (si existen ambos)
- ❌ NO modificar tokens de App para ajustes de marketing
- ✅ Landing = marketing, App = producto

---

# 7. ESTRUCTURA DE CARPETAS DEL PROYECTO

> El layout estándar está en `Project_setup/standard/04_ESTRUCTURA_FASES.md`. Esta sección documenta especificidades del proyecto.

```
[repo]/
├── src/                                  ← código fuente
├── backend/                              ← (si aplica)
├── frontend/                             ← (si aplica)
├── phases/                               ← según 04_ESTRUCTURA_FASES.md
│   ├── 00-discovery/
│   ├── 01-planning/
│   ├── ...
│   └── 07-operations/
├── _pm/
│   ├── roles/
│   ├── templates/
│   └── operativos/
├── docs/                                 ← referencia técnica viva
├── archive/                              ← histórico
└── prisma/ (si aplica)
```

### Particularidades del proyecto
- [Carpetas o convenciones específicas, si las hay]

---

# 8. HANDOFF INICIAL DEL PROYECTO

- **Handoff del PM/PJM**: `[ruta al HO inicial]`
- **Plan de sprints/fases**: `[ruta al plan]`
- **Checklist onboarding**: `[ruta al CHECKLIST_NUEVO_PROYECTO.md si existe]`

### Documentos de onboarding del proyecto (si aplica)
| # | Documento | Contenido |
|---|-----------|-----------|
| 01 | PROYECTO_CONTEXT.md | Nombre, objetivo, stack, URL API, Swagger |
| 02 | EQUIPO.md | Roster: nombre, rol, email, UUID |
| 03 | CREDENCIALES.md | Service token, URL base API |
| 04 | IDS_SISTEMA.md | Project ID, Phase IDs, Status/Priority UUIDs |
| 05 | ENDPOINTS_CRITICOS.md | Endpoints frecuentes |

---

# 9. CONFIGURACIÓN GIT DEL AGENTE

- **user.name**: `[Nombre coordinador / agente]`
- **user.email**: `[email]`
- **Co-Authored-By**: OBLIGATORIO en TODOS los commits
  - Formato: `Co-Authored-By: Claude <noreply@anthropic.com>`

### Formato de commits (específico del proyecto si aplica)
```
[tipo]([repo]) [TASK_ID]: Descripción breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude <noreply@anthropic.com>
Refs: #[TASK_ID]
```

---

# 10. REFERENCIAS AL ESTÁNDAR

Las reglas operativas, procesos y convenciones **genéricas** viven en el estándar portable. Consultar:

| Tema | Documento estándar | Ubicación |
|------|---------------------|-----------|
| Jerarquía y precedencia | `00_INDEX.md` | `Project_setup/standard/` |
| Taxonomía del sistema | `01_ONBOARDING.md` | `Project_setup/standard/` |
| Ciclo de vida de tareas, issues, on-hold, git | `02_OPERACION_AGENTE.md` | `Project_setup/standard/` |
| Flujo Tech Lead (2 fases, 8 elementos) | `03_FLUJO_TL.md` | `Project_setup/standard/` |
| Layout de carpetas por fase | `04_ESTRUCTURA_FASES.md` | `Project_setup/standard/` |
| 438 deliverables por fase SDLC | `05_CATALOGO_DELIVERABLES.md` | `Project_setup/standard/` |
| Perfil base del rol | `roles/AGENT_PROFILE_BASE_[ROL].md` | `Project_setup/standard/roles/` |

> **No dupliques aquí contenido del estándar.** Si detectas un patrón que aplica a todos los proyectos, proponlo al estándar. Si es específico de este proyecto, documéntalo en §12 (Notas de Incidentes).

---

# 11. DOCUMENTOS DE REFERENCIA ESPECÍFICOS DEL PROYECTO

| Documento | Ubicación | Para qué |
|-----------|-----------|----------|
| Proceso de Asignación del proyecto | `[ruta al PROCESO_ASIGNACION.md del proyecto]` | Adaptación del `03_FLUJO_TL.md` con detalles del proyecto |
| Perfil operativo del rol (instancia) | `[ruta al OPERATIVO_[ROL].md]` | Comandos concretos, UUIDs, URLs |
| Contexto de sesión | `[ruta al CONTEXTO_[ROL]_SESION.md]` | Estado actual del sprint (live) |
| Template de asignación | `[ruta al TEMPLATE_ASIGNACION.md]` | Template del ASSIGNMENT |
| Template devlog | `[ruta al TEMPLATE_DEVELOPMENT_LOG.md]` | Template del DevLog |
| Template code logic | `[ruta al TEMPLATE_CODE_LOGIC.md]` | Template del Code Logic |
| Formato reporte | `[ruta al FORMATO_REPORTE_[ROL].md]` | Formato de entrega al PM |
| Handoff inicial del proyecto | `[ruta al HO del PM/PJM]` | Contexto original |

---

# 12. CONTEXTO ACTUAL (actualizar por sprint)

**Sprint/Fase activa**: [descripción]

### Tareas en curso
| Tarea | Descripción | Estado | Notas |
|-------|-------------|--------|-------|
| [TASK_ID] | [nombre] | [status] | [notas] |

### Instrucción operativa
- **Al completar una tarea** → actualizar esta sección Y `CONTEXTO_[ROL]_SESION.md`
- **Fuente de verdad del estado actual**: `[ruta al CONTEXTO_[ROL]_SESION.md]`
- **Al iniciar sesión** → leer esta sección primero

---

# 13. NOTAS DE INCIDENTES (memoria larga del proyecto)

### Convención de códigos
- **ERR-xxx**: errores técnicos recurrentes (bugs de plataforma, quirks de stack)
- **LL-xxx**: lecciones aprendidas de procesos (workflows rotos, PRs mal dirigidos)
- **DSM-xxx**: decisiones de stack / arquitectura
- **AUD-xxx**: hallazgos de auditorías

### Formato de entrada
```markdown
- **[YYYY-MM-DD] ERR-xxx**: [descripción corta del incidente]
  - **Contexto**: [qué se intentaba hacer]
  - **Causa raíz**: [por qué falló]
  - **Regla derivada**: [qué NO repetir / qué SÍ hacer]
```

### Incidentes registrados
> Agregar aquí conforme surjan. Los primeros incidentes suelen repetirse — capturarlos evita pérdida de tiempo futura.

- **[YYYY-MM-DD] [CODIGO]**: [descripción] → regla: [...]

---

**Última actualización**: [YYYY-MM-DD]
**Versión**: 2.0 (template reducido — reglas operativas movidas al estándar `Project_setup/standard/`)

### Changelog
- v2.0 (2026-04-20): Reducido a 13 secciones. Eliminadas secciones 10-14 del v1.0 (reglas operativas, reglas comunicación PM, procesos operativos, endpoints, formato commits) — ahora viven en `02_OPERACION_AGENTE.md` del estándar. Agregada §10 "Referencias al estándar" para enlazar. Resultado: ~280 líneas vs 550 anteriores, sin duplicación.
- v1.0 (2026-02-10): Versión inicial con 17 secciones autocontenidas.
