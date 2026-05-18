# 01 — ONBOARDING CONCEPTUAL

**Capa:** Estándar (genérico, portable)
**Audiencia:** TODOS los agentes (SA, AR, PM, PJM, TL, DL, BE, FE, DB, DO, QA, UX)
**Versión:** 1.0
**Cuándo leerlo:** UNA SOLA VEZ al empezar a operar en la plataforma. Es el primer contacto conceptual.

---

## REGLA #1: LEE ESTO PRIMERO

Antes de crear, modificar o consultar CUALQUIER cosa en la plataforma, entiende esta jerarquía:

```
PROYECTO
    └── RELEASE
            └── SPRINT (opcional — solo si la metodología lo usa)
                    └── FASE
                            └── DELIVERY (entregable)
                                    └── TAREA
```

**Si no entiendes esta jerarquía, NO toques el sistema.**

---

## QUÉ ES CADA COSA

### PROYECTO

Es el producto o iniciativa completa.

| Correcto | Incorrecto |
|----------|------------|
| "Virtual Teams Tracking" | "Virtual Teams Tracking Sprint 1" |
| "DesignMine" | "DesignMine MVP" |
| "CRM Cliente X" | "Fase de Análisis" |

**Un proyecto es UNO. No se duplica. No se crea otro proyecto para cada versión.**

---

### RELEASE

Es una versión del proyecto. Un proyecto tiene VARIOS releases.

| Proyecto | Releases |
|----------|----------|
| Virtual Teams Tracking | MVP, V2.0, V3.0 |
| DesignMine | Alpha, Beta, V1.0 |

**NO crees un proyecto nuevo para cada versión. Crea un RELEASE dentro del proyecto existente.**

---

### SPRINT (Opcional)

Es una iteración de tiempo (ej: 2 semanas). Solo se usa si la metodología lo requiere.

| Metodología | ¿Usa Sprint? |
|-------------|--------------|
| Scrum | ✅ Sí |
| Kanban | ❌ No |
| Waterfall | ❌ No |
| Custom | Depende del proyecto |

**Si el proyecto no usa sprints, NO los crees.**

---

### FASE

Es una etapa del ciclo de desarrollo. Las fases son **FIJAS** para cada proyecto según su metodología. Vienen del template del wizard.

| Código | Fase |
|--------|------|
| 00 | Discovery |
| 01 | Planning |
| 02 | Analysis |
| 03A | Design UX/UI |
| 03B | Design Technical |
| 04 | Development |
| 05 | Testing |
| 06 | Deployment |
| 07 | Operations |

**NO crees fases manualmente. El proyecto ya tiene sus fases según el template seleccionado en el wizard.**

> Detalle completo en `05_CATALOGO_DELIVERABLES.md`.

---

### DELIVERY (Entregable)

Es un artefacto que se produce en una fase. Ejemplos:

| Fase | Deliveries |
|------|------------|
| Requirements (02) | PRD, User Stories, SRS |
| Analysis (02) | Casos de Uso, Business Rules |
| Technical Design (03B) | ERD, ADR, API Design |
| Development (04) | Código, Swagger, Devlog |
| Testing (05) | Test Plan, QA Report |
| Deployment (06) | Deploy Guide, Runbook |

**Un delivery es un DOCUMENTO o ARTEFACTO, NO una tarea.**

---

### TAREA

Es una unidad de trabajo ejecutable que produce o contribuye a un delivery.

| Delivery | Tareas |
|----------|--------|
| API Design | Diseñar endpoint POST /users |
| API Design | Diseñar endpoint GET /users/:id |
| ERD | Crear modelo User |
| ERD | Crear modelo Project |

**Las tareas van DENTRO de deliveries. No flotan solas.**

---

## FLUJO DE CREACIÓN

### ¿Necesitas un proyecto nuevo?

```
¿Ya existe el proyecto en la plataforma?
    │
    ├── SÍ → NO crees otro. Usa el existente.
    │         ¿Necesitas una nueva versión? → Crea un RELEASE
    │
    └── NO → Crea el proyecto con el wizard
```

### ¿Cómo crear un proyecto correctamente?

1. **Selecciona el tipo** (software, marketing, research, consulting, custom)
2. **Selecciona la metodología** (Scrum, Kanban, Waterfall, Custom)
3. **Configura sprints** (solo si la metodología los usa)
4. **Las fases se crean automáticamente** según el template
5. **Los deliveries se asignan** según la fase

### REGLAS:

- ❌ NO crees fases manualmente
- ❌ NO dupliques proyectos
- ❌ NO crees un proyecto por cada release
- ❌ NO mezcles deliveries de diferentes fases

---

## ERRORES COMUNES Y CÓMO EVITARLOS

### Error 1: Crear proyecto duplicado

```
❌ INCORRECTO:
- Proyecto: "VTT"
- Proyecto: "VTT V2"
- Proyecto: "VTT Modelo Dinámico"

✅ CORRECTO:
- Proyecto: "VTT"
    └── Release: "MVP"
    └── Release: "V2.0"
    └── Release: "Modelo Dinámico V4"
```

### Error 2: Confundir delivery con tarea

```
❌ INCORRECTO:
- Tarea: "PRD"
- Tarea: "ERD"
- Tarea: "API Design"

✅ CORRECTO:
- Delivery: "PRD"
    └── Tarea: "Escribir sección de alcance"
    └── Tarea: "Definir user stories"
- Delivery: "ERD"
    └── Tarea: "Modelar tabla users"
    └── Tarea: "Modelar tabla projects"
```

### Error 3: Crear fases manualmente

```
❌ INCORRECTO:
POST /api/phases { name: "Development" }

✅ CORRECTO:
Las fases ya existen al crear el proyecto con el wizard.
Solo asigna tareas a la fase correspondiente.
```

### Error 4: Ignorar la metodología

```
❌ INCORRECTO:
Proyecto Kanban con sprints de 2 semanas

✅ CORRECTO:
Kanban NO usa sprints. El trabajo fluye continuo.
```

### Error 5: Campos incorrectos al crear tarea

```
❌ INCORRECTO:
POST /api/phases/{id}/tasks con:
  { "assignedTo": "uuid" }        ← se ignora silenciosamente
  { "priority_id": "uuid" }        ← rechazado (snake_case)
  { "complexity": "medium" }       ← rechazado (minúsculas)

✅ CORRECTO:
  { "assignedToId": "uuid" }       ← camelCase correcto
  { "priorityId": "uuid" }
  { "complexity": "MEDIUM" }        ← MAYÚSCULAS
```

> Detalle operativo completo en `02_OPERACION_AGENTE.md` §4.

---

## CÓMO ASIGNAR TRABAJO (si eres TL/DL/PJM)

### Paso 1: Identifica el contexto

```
¿En qué proyecto estoy trabajando?
¿En qué release?
¿En qué sprint? (si aplica)
¿En qué fase?
¿En qué delivery?
```

### Paso 2: Crea la tarea en el lugar correcto

```
POST /api/phases/{phaseId}/tasks
{
  "title": "Implementar endpoint POST /users",
  "description": "...",
  "statusId": "{UUID_PENDING}",
  "priorityId": "{UUID_PRIORIDAD}",
  "deliveryId": "uuid-del-delivery-api-endpoints",
  "assignedToId": "{UUID_AGENTE}",
  "assignedBy": "{UUID_TL}",
  "category": "development",
  "complexity": "MEDIUM",
  "createdBy": "{UUID_TL}"
}
```

### Paso 3: Registra tu trabajo en el devlog

Durante la ejecución, registra:
- Observaciones
- Decisiones tomadas
- Blockers encontrados
- Tech debt identificada

```
POST /api/tasks/{id}/devlog-entries
{
  "categoryCode": "decision",
  "title": "Usar UUID en lugar de auto-increment",
  "description": "Por consistencia con el resto del sistema"
}
```

---

## DEVLOG: QUÉ VA Y QUÉ NO VA

### SÍ va en devlog:

| Categoría | Ejemplo |
|-----------|---------|
| `decision` | "Decidimos usar Redis para cache" |
| `tech_debt` | "Falta refactorizar el TimeService" |
| `blocker` | "Esperando migración de Admin" |
| `testing_note` | "Endpoint responde en 200ms" |
| `risk` | "API externa puede cambiar" |
| `issue` | "Inconsistencia en formato de fechas" |

### NO va en devlog:

| Qué | Dónde va |
|-----|----------|
| Bugs críticos | Sistema de bugs separado (`POST /api/tasks/{id}/bugs`) |
| Código | Repositorio Git |
| Documentación técnica | `/knowledge/code-logic/` |

---

## ANTES DE CERRAR UNA TAREA

### Checklist obligatorio:

1. ✅ ¿Completé el trabajo?
2. ✅ ¿Registré mis observaciones en devlog?
3. ✅ ¿Hay entries critical/high pendientes? → **NO puedo cerrar**
4. ✅ ¿Hay issues abiertos en la tarea? → **NO puedo cerrar**
5. ✅ ¿Leí TODOS los comentarios de la tarea?
6. ✅ ¿El delivery asociado está actualizado?

### Gate de revisión

Si intentas pasar una tarea a `task_in_review` y tienes devlog entries con `severity=critical` o `severity=high` en `status=pending`, el sistema te va a bloquear con **error 422 Unprocessable Entity**.

**Primero resuelve los blockers, luego cierra la tarea.**

**Cómo desbloquear:**
1. Resolver los blockers: `PATCH /api/devlog-entries/{id}/status` con status `resolved` + `resolution`
2. O pedir al TL que los marque `acknowledged`/`deferred`/`wont_fix`
3. Reintentar la transición a `task_in_review`

---

## RESUMEN VISUAL

```
┌─────────────────────────────────────────────────────────────────┐
│                         PROYECTO                                │
│                (VTT, DesignMine, CRM Cliente X)                 │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                      RELEASE                            │   │
│   │                   (MVP, V2.0, V3.0)                     │   │
│   │                                                         │   │
│   │   ┌─────────────────────────────────────────────────┐   │   │
│   │   │                   SPRINT                        │   │   │
│   │   │              (S01, S02, S03...)                 │   │   │
│   │   │              [SOLO SI APLICA]                   │   │   │
│   │   │                                                 │   │   │
│   │   │   ┌─────────────────────────────────────────┐   │   │   │
│   │   │   │                 FASE                    │   │   │   │
│   │   │   │     (Analysis, Development, QA, etc.)   │   │   │   │
│   │   │   │                                         │   │   │   │
│   │   │   │   ┌─────────────────────────────────┐   │   │   │   │
│   │   │   │   │           DELIVERY              │   │   │   │   │
│   │   │   │   │       (PRD, ERD, API, etc.)     │   │   │   │   │
│   │   │   │   │                                 │   │   │   │   │
│   │   │   │   │   ┌─────────────────────────┐   │   │   │   │   │
│   │   │   │   │   │         TAREA           │   │   │   │   │   │
│   │   │   │   │   │   (Crear endpoint X)    │   │   │   │   │   │
│   │   │   │   │   └─────────────────────────┘   │   │   │   │   │
│   │   │   │   │   ┌─────────────────────────┐   │   │   │   │   │
│   │   │   │   │   │         TAREA           │   │   │   │   │   │
│   │   │   │   │   │   (Crear modelo Y)      │   │   │   │   │   │
│   │   │   │   │   └─────────────────────────┘   │   │   │   │   │
│   │   │   │   └─────────────────────────────────┘   │   │   │   │
│   │   │   └─────────────────────────────────────────┘   │   │   │
│   │   └─────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## COMANDOS RÁPIDOS (referencia inicial)

> Comandos operativos completos en `02_OPERACION_AGENTE.md`.
> URL base y UUIDs específicos del proyecto en `PROJECT_MEMORY.md`.

### Ver proyectos existentes
```
GET /api/projects
```

### Ver releases de un proyecto
```
GET /api/projects/:id/releases
```

### Ver fases de un proyecto
```
GET /api/projects/:id/phases
```

### Ver deliveries de una fase
```
GET /api/phases/:id/deliveries
```

### Ver tareas de un delivery
```
GET /api/deliveries/:id/tasks
```

### Crear tarea (campos correctos)
```
POST /api/phases/{phaseId}/tasks
{
  "title": "...",
  "priorityId": "...",         # camelCase, NO 'priority_id'
  "statusId": "...",
  "assignedToId": "...",        # NO 'assignedTo' (se ignora silencio)
  "assignedBy": "...",
  "category": "development",
  "complexity": "MEDIUM",       # MAYÚSCULAS
  "createdBy": "..."
}
```

### Registrar en devlog
```
POST /api/tasks/:id/devlog-entries
{
  "categoryCode": "decision|tech_debt|blocker|risk|testing_note|issue",
  "severity": "critical|high|medium|low",
  "title": "...",
  "description": "..."
}
```

---

## REGLAS DE ORO

1. **UN proyecto = UN producto/iniciativa**
2. **Las versiones son RELEASES, no proyectos nuevos**
3. **Las fases vienen del template, no las crees manualmente**
4. **Los deliveries son artefactos, las tareas son trabajo**
5. **Todo tu trabajo va en devlog**
6. **Resuelve blockers antes de cerrar tareas**
7. **Si no entiendes algo, pregunta antes de actuar**

---

## QUÉ LEER DESPUÉS DE ESTE DOCUMENTO

Este onboarding te da la **taxonomía conceptual**. Para operar, lee en este orden:

| # | Documento | Propósito |
|---|-----------|-----------|
| 1 | `00_INDEX.md` | Reglas de precedencia entre documentos |
| 2 | `02_OPERACION_AGENTE.md` | Operación del día a día (ciclo vida, endpoints, git) |
| 3 | `04_ESTRUCTURA_FASES.md` | Dónde vive cada archivo en el proyecto |
| 4 | Si eres TL → `03_FLUJO_TL.md` | Flujo específico del Tech Lead |
| 5 | Si eres DL → `07.PROCESO_CONSULTA_DOCS_DL.md` del proyecto | Flujo del Design Lead |
| 6 | `PROJECT_MEMORY.md` del proyecto | Datos específicos (UUIDs, URLs, agentes) |
| 7 | `OPERATIVO_[ROL].md` del proyecto | Tu instancia de rol específica |

---

## HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-20 | Versión inicial consolidada desde `GUIA_OPERATIVA_AGENTES_VTT.md` v1.0 (2026-04-12). Correcciones: endpoint `POST /api/phases/{id}/tasks` (no `POST /api/tasks`), lesson VTT-506 sobre campos (`assignedToId`, `priorityId`, `complexity` MAYÚSCULAS, max 2000 chars). Agregado gate D-41 (422). |

---

**Fuente de verdad de este documento:** `Project_setup/standard/01_ONBOARDING.md`
