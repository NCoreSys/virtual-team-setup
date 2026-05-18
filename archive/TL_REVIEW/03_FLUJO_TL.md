# 03 — FLUJO OPERATIVO DEL TECH LEAD

**Capa:** Estándar (genérico, portable)
**Audiencia:** Tech Lead de cualquier proyecto gestionado en la plataforma
**Versión:** 1.0
**Complementa:** `00_INDEX.md`, `02_OPERACION_AGENTE.md`

---

## 1. PROPÓSITO

Define el flujo de trabajo del Tech Lead (TL) desde que recibe un handoff del PM/PJM hasta que cierra el review de una tarea. Cubre las dos fases del proceso (planificación y asignación), los 8 elementos obligatorios del assignment, y el mapa de fuentes de verdad a consultar.

> **Fuente de verdad final:** Siempre el código implementado, el schema real y el estado del sistema de gestión. Los handoffs y documentos son intención, no contrato técnico.

---

## 2. LAS DOS FASES DEL PROCESO

El proceso del TL tiene **DOS fases distintas** con responsabilidades diferentes:

### FASE 1 — Planificación (al recibir el handoff)

**Input:** Handoff del PM/PJM con features, fechas, dependencias.

**Actividades:**
- Leer el handoff completo (features, fechas, dependencias entre tareas)
- Generar el plan del sprint con oleadas y bloqueantes
- Crear las tareas en el sistema de gestión vía API
- Generar los BRIEFs (uno por tarea) y subirlos como attachments
- **Esta fase NO requiere leer código** — es planificación de alto nivel

**Output:** Lista de tareas en el sistema con BRIEFs adjuntos.

---

### FASE 2 — Asignación (al momento de asignar una tarea)

**Input:** Tarea lista para asignar + agente disponible.

**Actividades:**
- Escribir el ASSIGNMENT con información actualizada y **verificada contra el código real**
- Para tareas FE con endpoints BE: completar la sección `API/RECURSOS DISPONIBLES` desde el router/schemas real del backend — **NO desde el handoff**
- Para tareas BE: leer el schema Prisma y los archivos de configuración relevantes
- **NO es lectura a nivel detalle** (colores, radio buttons, comportamiento interactivo — eso lo lee el agente desde los HTMLs del UX)
- Subir el ASSIGNMENT como attachment de la tarea
- Asignar la tarea al agente vía API (o solicitar al PM que lo haga desde la UI)

**Output:** ASSIGNMENT adjunto en la tarea, tarea asignada al agente.

---

### Regla crítica LL-005 (de dónde llenar el ASSIGNMENT)

> **El template de asignación ya tiene la estructura correcta. El error es llenarlo desde la memoria o el handoff del PM en lugar de desde los artefactos ya generados** (router, schemas, código, HTML del UX-Agent). El contrato técnico lo define el código ya entregado, no la intención de diseño del handoff.

**Consecuencia:** Si un endpoint en el handoff no existe en `backend/src/routes/`, marcarlo como `[FALTA]` en el assignment — no asumir que existe.

---

## 3. FLUJO COMPLETO (paso a paso)

### Paso 1: Recibir Handoff del PM/PJM

- PM/PJM entrega documento de handoff con lista de features/tareas + dependencias
- TL analiza dependencias y define orden de implementación (oleadas)

### Paso 2: Generar BRIEFs y Crear Tareas (FASE 1)

- **Un BRIEF por cada tarea**
- Ubicación estándar: `knowledge/agent-tasks/briefs/BRIEF_[TASK_ID]_[nombre].md`
- El BRIEF es el diseño original (inmutable tras aprobación)
- Crear la tarea en el sistema vía API
- **Subir el BRIEF como attachment** de la tarea recién creada:
  ```
  POST /api/tasks/{taskId}/attachments
  fields: file (binary), fileType="brief", uploadedById=[UUID_TL]
  ```

### Paso 3: Generar ASSIGNMENT (UNO A LA VEZ) (FASE 2)

> **REGLA CRÍTICA:** Una tarea a la vez, a menos que el PM instruya lo contrario.

- Usar el template estándar de assignment del proyecto
- Ubicación: `knowledge/agent-tasks/assignments/ASSIGNMENT_[TASK_ID]_[nombre].md`
- **Completar llenando desde el código real** (ver sección 5 de este documento)

### Paso 4: Asignar la Tarea en el Sistema

- Subir el ASSIGNMENT como attachment:
  ```
  POST /api/tasks/{taskId}/attachments
  fields: file (binary), fileType="assignment", uploadedById=[UUID_TL]
  ```
- Asignar el agente vía API:
  ```
  PATCH /api/tasks/[TASK_ID]
  body: { "assignedToId": "[UUID_AGENTE]" }
  ```
- **IMPORTANTE:** Muchos proyectos requieren que el PM haga la asignación en la UI para control de flujo. Confirmar la regla del proyecto antes de asignar por API.

### Paso 5: Generar el MENSAJE para el Agente

- El TL prepara un mensaje que el PM pega como comentario en la tarea
- Debe incluir: documentos a leer, comandos de sistema, UUIDs del sistema, datos del agente
- Ver sección 4 de este documento para el formato

---

## 4. LOS 8 ELEMENTOS OBLIGATORIOS DEL ASSIGNMENT

Todo assignment debe incluir estos 8 elementos:

1. **Estado actual del proyecto**
   - ¿Qué está completado? ¿Qué branches hay abiertos? ¿Qué PRs previos deben estar mergeados?

2. **APIs y servicios disponibles**
   - Endpoints con ejemplos reales del codebase (request/response, paths exactos)
   - Marcar `[OK]` los que existen, `[FALTA]` los que se asumen

3. **Arquitectura y estructura**
   - Carpetas, patrones, convenciones del proyecto

4. **Contexto de integración**
   - Cómo se conecta esta tarea con el resto del sistema

5. **Entidades y modelos**
   - Schema de BD real, relaciones, tipos (copiar de `schema.prisma`)

6. **Recursos de diseño** (si aplica)
   - Mockups, design specs, tokens

7. **Checklist detallado**
   - Mínimo 10-15 items verificables

8. **Archivos a revisar ANTES de empezar**
   - Lista con ruta exacta y propósito de cada archivo

---

## 5. MAPA DE FUENTES DE VERDAD (qué consultar antes de escribir el ASSIGNMENT)

> **Regla de jerarquía:** Si hay conflicto, el **código implementado siempre gana** sobre documentos de diseño. El código es la verdad final.

### Capa: API Contract

| Fuente primaria (verdad real) | Fuente secundaria (diseño original) |
|-------------------------------|-------------------------------------|
| `backend/src/routes/[modulo].ts` o `[modulo].routes.ts` | Docs de arquitectura API |

### Capa: Modelo de Datos

| Fuente primaria | Fuente secundaria |
|------------------|-------------------|
| `backend/prisma/schema.prisma` | DOC de modelo de datos / ERD |

### Capa: Arquitectura del Sistema

| Fuente primaria | Fuente secundaria |
|------------------|-------------------|
| `docker-compose.yml` + `backend/src/server.ts` | DOC de arquitectura del sistema |

### Capa: Patrones Frontend

| Fuente primaria | Fuente secundaria |
|------------------|-------------------|
| `frontend/src/router/index.tsx` + `frontend/src/hooks/` + componentes existentes | DOC de flujo de pantallas |

### Capa: Design System

| Fuente primaria | Fuente secundaria |
|------------------|-------------------|
| `frontend/src/index.css` (tokens App) | DOC de design system / specs UI |

### Capa: Permisos / Auth

| Fuente primaria | Fuente secundaria |
|------------------|-------------------|
| `backend/src/middleware/` + `backend/src/services/permissions.service.ts` | DOC de auth / RBAC |

---

## 6. CADENA DE CONSULTA POR TIPO DE TAREA

### Para tareas FE (componente / página)

**Orden obligatorio de consulta:**

1. **`frontend/src/router/index.tsx`** — Verificar si la ruta ya existe. Identificar el componente que la maneja. Si no existe, confirmar dónde agregarla.
2. **`backend/src/routes/[modulo].ts`** — Obtener endpoints que el componente FE va a consumir (método, path, query params, body).
3. **Componentes FE existentes** — Buscar si el componente ya existe en `frontend/src/components/` o `frontend/src/pages/`.
4. **`frontend/src/hooks/`** — Verificar si ya existe un hook que consume el endpoint. Si existe, el agente lo reutiliza.
5. **`frontend/src/index.css`** — Verificar tokens disponibles. El agente NO inventa tokens ni usa colores hardcodeados.

**Secciones del assignment que alimenta cada fuente:**

| Sección del Assignment | Fuente |
|-------------------------|--------|
| `API/RECURSOS DISPONIBLES` | `backend/src/routes/[modulo].ts` |
| `CRÍTICO ANTES DE EMPEZAR → componentes existentes` | `frontend/src/components/` + `frontend/src/hooks/` |
| `RUTAS FRONTEND` | `frontend/src/router/index.tsx` |
| `ARQUITECTURA → tokens y design system` | `frontend/src/index.css` + DOC de design system |
| Contexto de la feature | DOC de flujo de pantallas |

---

### Para tareas BE (endpoint / servicio)

**Orden obligatorio de consulta:**

1. **`backend/src/routes/index.ts`** — Ver módulos registrados y sus prefijos. Confirmar si el módulo existe o hay que crearlo.
2. **`backend/src/routes/[modulo].ts`** — Si el módulo existe, ver endpoints actuales para no duplicarlos. Ver patrones de autenticación (`authenticate`, `requireCapability`).
3. **`backend/prisma/schema.prisma`** — Verificar entidades y relaciones. Confirmar nombres reales de campos.
4. **DOC de arquitectura API** — Leer diseño original del endpoint (parámetros, responses, reglas de negocio). Comparar contra código para detectar drift.
5. **`backend/src/middleware/`** — Si toca auth o permisos, leer middleware existente para entender el patrón.

---

### Para tareas DB (migración / schema)

**Orden obligatorio de consulta:**

1. **`backend/prisma/schema.prisma`** — Estado actual del modelo.
2. **DOC de modelo de datos + ERD** — Modelo lógico de entidades a agregar. Comparar con schema actual para detectar drift.
3. **`backend/prisma/migrations/`** — Últimas migraciones para entender patrón SQL.
4. **Reglas críticas DB del proyecto** (incluir SIEMPRE en BRIEFs de DB Engineer):
   - PKs: verificar convención (UUID nativo vs TEXT)
   - Nombres de columnas: camelCase vs snake_case
   - Tablas: mayúsculas vs minúsculas en prod

---

### Para tareas DevOps (infraestructura / deploy)

**Orden obligatorio de consulta:**

1. **`docker-compose.yml`** — Servicios actuales, puertos, env vars, nombres de contenedores.
2. **`backend/.env.example`** — Variables de entorno requeridas.
3. **`frontend/nginx.conf`** (si aplica) — Routing o proxy.
4. **DOC de arquitectura del sistema** — Infraestructura de referencia.

> **Excepción DevOps:** Las tareas de DevOps **NO requieren BRIEF ni ASSIGNMENT** si la descripción detalla correctamente: objetivo, SQL/comandos, pre/post checks, rollback. La description de la tarea es suficiente handoff.

---

### Para tareas Design (componente UI / landing)

**Orden obligatorio de consulta:**

1. **`frontend/src/components/`** — Componentes existentes.
2. **DOC de design system** — Tokens (en proyectos con Landing + App, nunca mezclar tokens de ambos contextos).
3. **`knowledge/design/`** — Specs de copywriting y assets.
4. **Wireframes / design specs** — Diseño original.

---

## 7. PROCESO PASO A PASO ANTES DE ESCRIBIR UN ASSIGNMENT

### Paso A: Identificar módulo y archivos afectados (< 5 min)

```
1. Leer el handoff del PM — qué feature/módulo implementar
2. Usar Glob para encontrar el archivo de ruta:
   → Glob: backend/src/routes/[modulo]*.ts
3. Usar Glob para encontrar componentes FE:
   → Glob: frontend/src/components/features/[Modulo]*.tsx
   → Glob: frontend/src/pages/[Modulo]*.tsx
4. Anotar:
   - Ruta del archivo backend (real)
   - Ruta del componente FE (si existe o hay que crearlo)
   - Si es modificación o creación nueva
```

### Paso B: Verificar Contrato de API (< 10 min) — solo si toca API

```
1. Abrir: backend/src/routes/[modulo].ts
   → Buscar router.get/post/patch/delete
   → Copiar: método, path exacto, middleware aplicado
   → Identificar si usa authenticate, requireCapability

2. Si el endpoint NO existe aún → confirmarlo en el assignment:
   → Marcar como [FALTA — BE debe crear primero]
   → Verificar si hay una tarea BE pendiente que lo cree

3. Verificar tipos/schemas:
   → backend/src/validators/ o schemas
   → Interfaces inline en el route handler
```

### Paso C: Verificar Estado de Componentes FE (solo tareas FE)

```
1. Glob: frontend/src/components/features/*.tsx  ← componentes existentes
2. Glob: frontend/src/hooks/use*.ts  ← hooks disponibles
3. Leer router: frontend/src/router/index.tsx
   → ¿La ruta existe? ¿Está bajo ProtectedRoute?
4. Para cada archivo que el agente DEBE modificar:
   → Listar la ruta exacta en el campo CRITICO ANTES DE EMPEZAR
   → NO listar el handoff del PM — ese ya fue leído en Fase 1
```

### Paso D: Verificar Schema (solo tareas BE o DB)

```
1. Abrir: backend/prisma/schema.prisma
2. Buscar el modelo relevante
3. Anotar:
   - Nombre real del campo (camelCase o snake_case con @map)
   - Tipo (String, Int, DateTime, etc.)
   - Si es FK o PK
   - Tabla real (@@map si existe)
4. Copiar al assignment — NO inventar nombres de campos
```

### Paso E: Revisar Reglas de Permisos (opcional — solo si toca auth)

```
Si la tarea toca autenticación, permisos o RBAC:
1. Abrir: backend/src/middleware/authorization.middleware.ts
2. Abrir: backend/src/services/permissions.service.ts
3. Ver cómo se usa requireCapability en rutas similares
4. Incluir en el assignment: patrón de middleware a seguir
```

---

## 8. CHECKLIST ANTES DE ENTREGAR EL ASSIGNMENT

```
[ ] ¿Abrí backend/src/routes/[modulo].ts para copiar paths reales?
[ ] Para tareas FE: ¿verifiqué si el componente/hook ya existe?
[ ] Para tareas FE: ¿anoté las rutas exactas en CRÍTICO ANTES DE EMPEZAR?
[ ] ¿El campo API/RECURSOS DISPONIBLES tiene paths verificados (no del handoff)?
[ ] Para tareas DB: ¿copié nombres reales de campos desde schema.prisma?
[ ] ¿Incluí reglas críticas DB del proyecto (convenciones UUID/naming/tablas)?
[ ] ¿Incluí un checklist de mínimo 10 items verificables?
[ ] ¿Incluí archivos a revisar antes de empezar con ruta exacta?
[ ] ¿Subí el ASSIGNMENT como attachment de la tarea?
[ ] ¿El mensaje para el agente tiene todos los UUIDs del sistema?
```

---

## 9. FORMATO DEL MENSAJE PARA EL AGENTE

Plantilla genérica que el TL entrega al PM para que pegue como comentario en la tarea:

```markdown
Tienes tarea nueva asignada: [TASK_ID] (Título de la tarea).

1. Lee el assignment completo: knowledge/agent-tasks/assignments/ASSIGNMENT_[TASK_ID]_[nombre].md
2. Lee el brief: knowledge/agent-tasks/briefs/BRIEF_[TASK_ID]_[nombre].md
3. Lee los procedimientos operativos: [ruta a 02_OPERACION_AGENTE.md]
4. Lee los templates de devlog/code-logic del proyecto

Indicaciones del sistema:

0) Obtén tu JWT de servicio (si el proyecto requiere auth en mutaciones):
   [Script Python o curl para /api/auth/service-token con userId + serviceKey]

a) Mueve la tarea a in_progress:
   PATCH /api/tasks/[TASK_ID]/status con statusId=[UUID_IN_PROGRESS] y changedBy=[UUID_AGENTE]

b) Trabaja la tarea siguiendo el workflow del assignment

c) ANTES de mover a in_review, sube estos 3 entregables:
   c.1) DevLog — POST /api/tasks/[TASK_ID]/attachments con fileType="devlog"
   c.2) Code Logic — POST /api/tasks/[TASK_ID]/attachments con fileType="code_logic"
   c.3) Comentario de entrega — POST /api/tasks/[TASK_ID]/comments con el reporte

d) Mueve la tarea a in_review:
   PATCH /api/tasks/[TASK_ID]/status con statusId=[UUID_IN_REVIEW] y changedBy=[UUID_AGENTE]

e) Entrega el reporte con el formato del assignment para revisión.

Datos del sistema:
- Tu user ID: [UUID_AGENTE]
- Tu SERVICE_KEY: [SERVICE_KEY]
- Status in_progress: [UUID]
- Status in_review: [UUID]
- Backend: [BASE_URL]
- Swagger: [BASE_URL]/api-docs
```

> Los UUIDs, URLs y SERVICE_KEY concretos viven en `PROJECT_MEMORY.md` del proyecto específico, no en este documento estándar.

---

## 10. CICLO DE VIDA COMPLETO DE UNA TAREA (referencia)

### Flujo normal (sin issues)

```
1. TL genera Brief + Assignment
2. TL (o PM) asigna tarea vía API
   → Sistema auto-transiciona: task_created → task_pending
3. PM pega mensaje al agente con documentos + comandos + datos del sistema
4. Agente mueve a in_progress (PATCH status, changedBy: UUID_AGENTE)
5. Agente trabaja la tarea (código, docs, git, PR)
6. Agente mueve a in_review (PATCH status, changedBy: UUID_AGENTE)
7. TL revisa:
   - Lee entregables (devlog, code-logic, comentario)
   - Verifica consistencia (tokens, patrones, design system)
   - Verifica checklist del assignment
8. TL mueve a completed (PATCH status, changedBy: UUID_TL)
9. PM aprueba → task_approved (PATCH status, changedBy: UUID_PM)
```

### Responsabilidades por transición de status

| Transición | Quién ejecuta | Acción |
|------------|---------------|--------|
| `task_created → task_pending` | Sistema (auto al asignar) | Asignar assigneeId |
| `task_pending → task_in_progress` | Agente ejecutor | Empieza a trabajar |
| `task_in_progress → task_in_review` | Agente ejecutor | Terminó, creó PR |
| `task_in_review → task_completed` | Tech Lead | Review aprobado |
| `task_completed → task_approved` | PM | Aprobación final (terminal) |
| `cualquiera → task_on_hold` | PM / TL | Hay issue bloqueante |
| `task_on_hold → previousStatus` | Sistema (auto-resume) | Issues resueltos |

> **Regla crítica:** El PM es el ÚNICO que puede mover a `task_approved`. El TL no puede — es una acción terminal irreversible.

---

## 11. REGLAS CRÍTICAS DEL TL

1. **UNA tarea a la vez** — No asignar múltiples tareas salvo que el PM lo autorice.
2. **Assignment con integración real** — No instrucciones genéricas, incluir código/schema/API del codebase actual.
3. **El PM hace los merges** — NUNCA el TL ni los agentes.
4. **El PM asigna en la UI** — El TL puede asignar vía API solo cuando el PM lo instruya.
5. **Verificar estado real antes de crear assignment** — No asumir, leer el código.
6. **Seguir el template de assignment al pie de la letra** — Los 8 elementos son obligatorios.
7. **LL-005: Llenar el template desde artefactos verificados** — La sección `API/RECURSOS DISPONIBLES` se completa desde el router/schemas real del BE, NO desde el handoff del PM.
8. **BRIEF = adjunto al crear la tarea. ASSIGNMENT = adjunto al asignar.** No subir retroactivamente si se puede evitar.
9. **NUNCA mover a completed una tarea con FAIL** — dejar en in_review con comentario explicando qué falla.
10. **NUNCA mover a completed una tarea con issues abiertos** — verificar `GET /api/tasks/{id}/issues` primero.
11. **Leer TODOS los comentarios antes de completar** — si mencionan bugs o pendientes, verificar estado.

---

## 12. COMANDOS DEL TL PARA REVIEW

> Los comandos específicos (con JWT, URLs reales, UUIDs) viven en `OPERATIVO_[PROYECTO]_TECH_LEAD.md`. Este documento solo describe el flujo.

**Flujo de review:**

```
1. Leer entregables de la tarea (devlog + code-logic + comentario + código del PR)
2. Verificar checklist del assignment
3. Verificar consistencia técnica (patrones, design system, convenciones)
4. Verificar que NO haya issues abiertos (GET /api/tasks/{id}/issues)
5. Si todo OK → PATCH status a task_completed + comentario de aprobación
6. Si hay observaciones → dejar en in_review + comentario con qué corregir
```

---

## 13. PROCESO DE ISSUES (cuando un agente levanta la mano)

### Cuándo crear un issue

| Situación | Tipo | Severidad | Ejemplo |
|-----------|------|-----------|---------|
| Necesito cambio en schema.prisma | `requirement` | `medium`/`high` | "Agregar campo password a User" |
| Encontré un bug en código existente | `bug` | según impacto | "El endpoint X devuelve 500 cuando..." |
| Falta funcionalidad que bloquea mi tarea | `requirement` | `high`/`critical` | "No existe endpoint para Y" |
| Mejora que facilita la implementación | `improvement` | `low`/`medium` | "Agregar index en tabla Z" |
| Necesito deploy o rebuild | `requirement` | `high` | "Ejecutar migration y rebuild backend" |

### Reglas de issues

1. **Cada agente crea issues en su propia tarea** para documentar qué necesita.
2. **NO resolver issues de otros** — cada agente resuelve lo que le corresponde.
3. **Describir claramente** qué se necesita y quién debe hacerlo.
4. **Si es bloqueante**, pedir al PM que ponga la tarea en `on_hold` vinculada al issue.
5. **El issue NO es un chat** — es un registro formal de una necesidad. Para discusión usar comentarios.
6. **NUNCA usar `PATCH /status` para poner `on_hold`** — usar `PUT /api/tasks/{id}/on-hold` con header `x-user-id`.

### En qué tarea crear el issue

| Situación | Dónde crear el issue |
|-----------|----------------------|
| Necesito algo para completar MI tarea | En MI tarea |
| Encontré bug en funcionalidad de OTRA tarea | En la tarea donde está el bug |
| Mejora general del proyecto | En la tarea de issues abiertos (si existe) |

---

## 14. INTEGRACIÓN CON LA ESTRUCTURA DE FASES

> Ver `04_ESTRUCTURA_FASES.md` para el layout completo del repositorio.

**Ubicación estándar de los artefactos del TL:**

```
phases/XX-[nombre]/_pm/
├── HANDOFF_[DISC]_[SPRINT]_[desc].md       ← lo genera el PM/PJM
├── BRIEF_[DISC]_[SPRINT]_[TASK_ID]_[desc].md ← lo genera el TL (FASE 1)
└── ASSIGNMENT_[DISC]_[SPRINT]_[TASK_ID].md   ← lo genera el TL (FASE 2)
```

> Ver `05_CATALOGO_DELIVERABLES.md` para el catálogo completo de 438 deliverables por fase SDLC.

---

## 15. DOCUMENTOS RELACIONADOS

| Documento | Propósito |
|-----------|-----------|
| `00_INDEX.md` | Jerarquía y precedencia de documentos |
| `01_ONBOARDING.md` | Taxonomía del sistema (proyecto, release, fase, delivery, tarea) |
| `02_OPERACION_AGENTE.md` | Reglas operativas comunes a todos los agentes |
| `04_ESTRUCTURA_FASES.md` | Layout de carpetas por fase SDLC |
| `05_CATALOGO_DELIVERABLES.md` | 438 deliverables por fase |
| `roles/AGENT_PROFILE_BASE_TL.md` | Perfil base del rol TL |
| `OPERATIVO_[PROYECTO]_TECH_LEAD.md` | Instancia específica del proyecto (UUIDs, URLs, comandos) |
| `PROJECT_MEMORY.md` | Memoria del proyecto (datos específicos) |

---

## 16. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-20 | Versión inicial consolidada desde `PROCESO_ASIGNACION_TAREAS.md` v1.6 + `06.PROCESO_CONSULTA_DOCS_TL.md` v1.0. Extracción de la parte genérica/portable. |

---

**Fuente de verdad de este documento:** `Project_setup/standard/03_FLUJO_TL.md`
