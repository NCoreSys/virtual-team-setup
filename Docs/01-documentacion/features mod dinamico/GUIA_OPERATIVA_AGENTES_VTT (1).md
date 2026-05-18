# GUÍA OPERATIVA PARA AGENTES VTT
## Cómo Operar en el Sistema de Gestión de Proyectos

**Versión:** 1.0  
**Fecha:** 2026-04-12  
**Audiencia:** Agentes AI (SA, AR, TL, DB, BE, FE, QA, DL, PJM)

---

## REGLA #1: LEE ESTO PRIMERO

Antes de crear, modificar o consultar CUALQUIER cosa en VTT, entiende esta jerarquía:

```
PROYECTO
    └── RELEASE
            └── SPRINT (opcional)
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
| "VTT" | "VTT Sprint 1" |
| "DesignMine" | "DesignMine MVP" |
| "CRM Cliente X" | "Fase de Análisis" |

**Un proyecto es UNO. No se duplica. No se crea otro proyecto para cada versión.**

---

### RELEASE

Es una versión del proyecto. Un proyecto tiene VARIOS releases.

| Proyecto | Releases |
|----------|----------|
| VTT | MVP, V2.0, V3.0 |
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

**Si el proyecto no usa sprints, NO los crees.**

---

### FASE

Es una etapa del ciclo de desarrollo. Las fases son FIJAS para cada proyecto según su metodología.

| Código | Fase |
|--------|------|
| 00 | Planning |
| 01 | Requirements |
| 02 | Analysis |
| 03a | UX/UI Design |
| 03b | Technical Design |
| 04 | Development |
| 05 | Testing |
| 06 | Deployment |
| 07 | Operations |

**NO crees fases manualmente. El proyecto ya tiene sus fases según el template seleccionado.**

---

### DELIVERY (Entregable)

Es un artefacto que se produce en una fase. Ejemplos:

| Fase | Deliveries |
|------|------------|
| Requirements | PRD, User Stories |
| Analysis | SRS, Casos de Uso |
| Technical Design | ERD, ADR, API Design |
| Development | Código, Swagger, Devlog |
| Testing | Test Plan, QA Report |

**Un delivery es un DOCUMENTO o ARTEFACTO, no una tarea.**

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
¿Ya existe el proyecto en VTT?
    │
    ├── SÍ → NO crees otro. Usa el existente.
    │         ¿Necesitas una nueva versión? → Crea un RELEASE
    │
    └── NO → Crea el proyecto con el wizard
```

### ¿Cómo crear un proyecto correctamente?

1. **Selecciona el tipo** (software, marketing, research)
2. **Selecciona la metodología** (Scrum, Kanban, Waterfall, Custom)
3. **Configura sprints** (solo si la metodología los usa)
4. **Las fases se crean automáticamente** según el template
5. **Los deliveries se asignan** según la fase

**NO:**
- ❌ Crees fases manualmente
- ❌ Dupliques proyectos
- ❌ Crees un proyecto por cada release
- ❌ Mezcles deliveries de diferentes fases

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
Las fases ya existen. Solo asigna tareas a la fase correspondiente.
```

### Error 4: Ignorar la metodología

```
❌ INCORRECTO:
Proyecto Kanban con sprints de 2 semanas

✅ CORRECTO:
Kanban NO usa sprints. El trabajo fluye continuo.
```

---

## CÓMO ASIGNAR TRABAJO

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
POST /api/tasks
{
  "title": "Implementar endpoint POST /users",
  "deliveryId": "uuid-del-delivery-api-endpoints",
  "phaseId": "uuid-de-la-fase-development",
  "sprintId": "uuid-del-sprint-actual" // si aplica
}
```

### Paso 3: Registra tu trabajo en el devlog

Durante la ejecución, registra:
- Observaciones
- Decisiones tomadas
- Blockers encontrados
- Tech debt identificada

```
POST /api/tasks/:id/devlog-entries
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
| Bugs | Sistema de bugs separado |
| Código | Repositorio Git |
| Documentación técnica | `/knowledge/` |

---

## ANTES DE CERRAR UNA TAREA

### Checklist obligatorio:

1. ✅ ¿Completé el trabajo?
2. ✅ ¿Registré mis observaciones en devlog?
3. ✅ ¿Hay entries critical/high pendientes? → **NO puedo cerrar**
4. ✅ ¿El delivery asociado está actualizado?

### Gate de revisión:

Si intentas pasar una tarea a `task_in_review` y tienes devlog entries con `severity=critical` o `severity=high` en `status=pending`, el sistema te va a bloquear con error 422.

**Primero resuelve los blockers, luego cierra la tarea.**

---

## RESUMEN VISUAL

```
┌─────────────────────────────────────────────────────────────────┐
│                         PROYECTO                                │
│                      (VTT, DesignMine)                         │
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
│   │   │   │      (Analysis, Development, QA)        │   │   │   │
│   │   │   │                                         │   │   │   │
│   │   │   │   ┌─────────────────────────────────┐   │   │   │   │
│   │   │   │   │           DELIVERY              │   │   │   │   │
│   │   │   │   │       (PRD, ERD, API)           │   │   │   │   │
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

## COMANDOS RÁPIDOS

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

### Crear tarea
```
POST /api/tasks
{
  "title": "...",
  "deliveryId": "...",
  "assignedToId": "..."
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

**Documento:** GUIA_OPERATIVA_AGENTES_VTT.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12
