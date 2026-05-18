# METODOLOGÍA DE EJECUCIÓN DE SPRINTS V1

**Documento:** METODOLOGIA_EJECUCION_SPRINTS_V1.md  
**Versión:** 1.0  
**Fecha:** 2026-03-30  
**Autor:** PJM-Agent  
**Aplica a:** Todos los proyectos gestionados con VTT y equipo de agentes  
**Estado:** 📋 ESTÁNDAR OBLIGATORIO

---

## 0. PROPÓSITO Y ALCANCE

### 0.1 Propósito

Este documento define el proceso estándar para ejecutar sprints en proyectos con equipos de agentes virtuales. Establece las fases, roles, entregables, validaciones y criterios de cierre que garantizan la calidad y completitud de cada sprint.

### 0.2 Alcance

- **Aplica a:** Cualquier proyecto gestionado con VTT (Virtual Teams Tracking)
- **Roles:** Configurable por proyecto (ver §1.2)
- **Sistema de gestión:** VTT obligatorio
- **Documentos de referencia:** Guías separadas (ver §10)

### 0.3 Principios Fundamentales

| Principio | Descripción |
|-----------|-------------|
| **Completitud > Velocidad** | Validar que TODO lo planificado se implementó antes de cerrar |
| **Quien implementa no valida** | Separación de responsabilidades en validación |
| **4 Firmas para cerrar** | AR + QA + TL + DL deben aprobar antes del cierre |
| **VTT es fuente de verdad** | Tareas, dependencias y estados viven en el sistema |
| **Documentos de referencia** | Cada validación tiene un documento contra el cual verificar |
| **Guías = Cómo / Handoffs = Qué** | Las guías explican el proceso; los handoffs definen el trabajo concreto |

### 0.4 Motivación del Proceso

Este proceso surgió de tres necesidades concretas:

1. **Sistema MGP activo:** VTT puede calcular Gantt, CPM, burndown y alertas — pero necesita `estimatedHours`, `complexity`, `category` y `dependsOn` en cada tarea. Sin estos campos, el motor de planificación no funciona.

2. **Equipo multi-agente:** Con múltiples agentes trabajando en paralelo, cada rol necesita un documento de entrada que consolide exactamente lo que le corresponde — no asumir contexto del handoff de otro rol.

3. **Validación de implementación:** Se requiere un mecanismo formal para verificar que FE implementó lo que DL diseñó, y que el código respeta las decisiones arquitectónicas (ADRs).

---

## 1. ECOSISTEMA DE DOCUMENTOS

### 1.1 Visión General

Cada sprint genera dos tipos de documentos:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ECOSISTEMA DE DOCUMENTOS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   HANDOFFS (por sprint)              GUÍAS (cross-sprint)        │
│   ─────────────────────              ────────────────────        │
│   Dicen QUÉ hacer                    Dicen CÓMO hacerlo          │
│   Cambian cada sprint                No cambian por sprint       │
│   1 por rol activo                   1 por área de proceso       │
│                                                                  │
│   • HANDOFF_TL_SPRINT_XX.md          • CODE_REVIEW_GUIDE.md      │
│   • HANDOFF_DL_SPRINT_XX.md          • INTEGRATION_AUDIT.md      │
│   • HANDOFF_FE_SPRINT_XX.md          • TESTING_GUIDE.md          │
│   • HANDOFF_QA_SPRINT_XX.md                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Los 4 Handoffs de Rol

Cada sprint genera exactamente 4 handoffs. Son documentos **de entrada** para cada rol — el agente los lee al arrancar.

```
Sprint start
    │
    ├── HANDOFF_TL_  ──→  TL coordina DO + DB + BE (arquitectura, schedule, plan VTT)
    │
    └── HANDOFF_DL_  ──→  DL produce HTMLs + UX Specs (en paralelo con TL)

         │                       │
         ▼                       ▼
      BE entrega              DL entrega
      endpoints               HTMLs + Specs
         │                       │
         └──────────┬────────────┘
                    ▼
             HANDOFF_FE_  ──→  FE implementa (recibe outputs de DL + contratos BE)
                    │
                    ▼
             HANDOFF_QA_  ──→  QA valida todo
```

| Handoff | Para quién | Inputs | Outputs |
|---------|-----------|--------|---------|
| `HANDOFF_TL_` | Tech Lead | Backlog + arquitectura + ADRs | Briefs BE/DB/DO, schedule, plan VTT |
| `HANDOFF_DL_` | Design Lead | Backlog + specs UX | HTMLs + UX Specs por pantalla + Design System |
| `HANDOFF_FE_` | Frontend | HTMLs (DL) + contratos API (BE) | Componentes + pantallas implementadas |
| `HANDOFF_QA_` | QA | Todos los anteriores | Test plan + reporte de bugs + cobertura |

> **Regla crítica:** FE nunca empieza hasta que DL entregó HTMLs Y BE tiene endpoints en `in_review`. Es el último en arrancar.

### 1.3 Las 3 Guías de Proceso

Estos documentos **no cambian por sprint** — definen la metodología. El agente los lee una sola vez al onboarding.

| Documento | Para quién | Qué explica |
|-----------|-----------|-------------|
| `CODE_REVIEW_GUIDE.md` | TL, CR | Cómo hacer code review: checklist técnico, qué aprobar/rechazar |
| `INTEGRATION_AUDIT_CHECKLIST.md` | AR | Cómo hacer el audit de integración: ADR compliance, DB schema, boundary checks |
| `TESTING_GUIDE.md` | QA | Cómo testear: pirámide, coverage mínimo, herramientas, mocking strategy |

---

## 2. ESTRUCTURA ESTÁNDAR DE HANDOFFS

### 2.1 Secciones Obligatorias

Todo handoff debe incluir estas 6 secciones al final, después del contenido específico del rol:

#### §N. TAREAS DEL SPRINT

Tabla formal con IDs de tarea, agente responsable, estimado en horas, complejidad y categoría.

```markdown
## N. TAREAS DEL SPRINT

### Fase: [Nombre fase] (Días X-Y)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| BE-001 | Descripción | BE | 4h | HIGH | development |
| TL-001 | Code Review | TL | 3h | MEDIUM | review |
| APR-001 | PM Aprobación | PM | 1h | LOW | review |
```

**Valores válidos:**
- `Complejidad`: `LOW` | `MEDIUM` | `HIGH`
- `Categoría`: `development` | `design` | `testing` | `deployment` | `review` | `documentation`

#### §N+1. DEPENDENCIAS ENTRE TAREAS

Tabla de dependencias formales. Tipo `FS` = Finish-to-Start (la más común).

```markdown
## N+1. DEPENDENCIAS ENTRE TAREAS

| Tarea | Depende de | Tipo | Nota |
|-------|-----------|------|------|
| BE-002 | DB-001 | FS | Necesita schema creado |
| FE-001 | BE-008, DL-007 | FS | Necesita endpoint + HTML |
```

> **Regla crítica:** Estas dependencias se configuran en VTT vía `POST /api/tasks/{id}/dependencies`. Al crearlas, la tarea pasa automáticamente a `task_blocked` y se libera sola cuando todas sus dependencias completan.

#### §N+2. VTT PLANNING DATA

Tabla lista para cargar al sistema de gestión.

```markdown
## N+2. VTT PLANNING DATA

> Tabla para crear tareas en VTT. [Rol responsable] crea las tareas en el sistema.

| Tarea | estimatedHours | complexity | category | dependsOn |
|-------|---------------|-----------|----------|-----------|
| BE-001 | 4 | HIGH | development | — |
| BE-002 | 8 | HIGH | development | DB-001, DB-002 |
| TL-001 | 3 | MEDIUM | review | BE-008 |

**Total [rol]:** Xh
```

> **¿Por qué en todos los handoffs?** El sistema MGP usa `estimatedHours`, `complexity` y `category` para calcular Gantt y detectar ruta crítica. Sin estos campos, el motor de planificación no funciona. Si falta `complexity` o `category`, la API rechaza la tarea (400 error).

#### §N+3. DOCUMENTOS DINÁMICOS A ACTUALIZAR

Lista de documentos que deben actualizarse durante el sprint y quién lo hace.

```markdown
## N+3. DOCUMENTOS DINÁMICOS A ACTUALIZAR

| Documento | Quién actualiza | Cuándo | Verificado en |
|-----------|----------------|--------|---------------|
| `API_CONTRACT.md` | BE | Al completar endpoints | Code Review (TL) |
| `.LOGIC.md` (por archivo) | BE/DB | Al completar cada tarea | Code Review (TL) |
```

#### §N+4. DoD — [ROL]

Checklist binario de Definition of Done específico para el rol.

```markdown
## N+4. DoD — [ROL]

[Área 1]:
[ ] Item 1
[ ] Item 2

[Área 2]:
[ ] Item 3
[ ] Item 4
```

#### §N+5. GATES DE APROBACIÓN

Condiciones de transición de fase y quién autoriza.

```markdown
## N+5. GATES DE APROBACIÓN

| Gate | Condición | Acción en VTT |
|------|-----------|---------------|
| [Rol] puede arrancar | [Condición previa] | TL desbloquea / notifica |
| Sprint cerrado | [Condición final] | TL crea APR para PM |
```

### 2.2 Contenido Específico por Rol

Además de las 6 secciones obligatorias, cada handoff tiene contenido específico:

| Handoff | Secciones específicas |
|---------|----------------------|
| **HANDOFF_TL_** | Arquitectura, Endpoints a implementar, Briefs para BE/DB, Variables de entorno, Riesgos |
| **HANDOFF_DL_** | Componentes a diseñar, Estados visuales, Design Tokens, Breakpoints responsive, Assets |
| **HANDOFF_FE_** | Estructura de archivos, Rutas, Contratos API, Store Zustand, Dependencias npm |
| **HANDOFF_QA_** | Escenarios BE, Escenarios FE, QA-FLOW scenarios, Proceso de bugs, Coverage mínimo |

### 2.3 Template Genérico

Los handoffs usan variables para ser agnósticos de proyecto:
- `[PROYECTO]` → nombre del proyecto
- `[SPRINT_N]` → número del sprint
- `[SISTEMA_GESTION]` → nombre del sistema (VTT)

```markdown
# HANDOFF [ROL]: [PROYECTO] — Sprint N

## Header
De / Para / Fecha / Sprint / Estado / Prerrequisitos

## 0. Resumen Ejecutivo

## [Secciones específicas del rol]

## §N.   Tareas del Sprint (tabla formal)
## §N+1. Dependencias entre Tareas
## §N+2. VTT Planning Data
## §N+3. Documentos Dinámicos a Actualizar
## §N+4. DoD — [ROL]
## §N+5. Gates de Aprobación

## §Ref. Referencias
```

---

## 3. ROLES Y CONFIGURACIÓN

### 3.1 Roles del Ecosistema

El ecosistema soporta roles configurables por proyecto. No todos los roles participan en todos los sprints.

```
ROLES DE DISEÑO                    ROLES DE CÓDIGO
───────────────                    ───────────────
DL  Design Lead                    TL  Tech Lead
UX  UX Designer                    DB  Database Engineer
                                   BE  Backend Engineer
                                   FE  Frontend Engineer
                                   
ROLES DE VALIDACIÓN                ROLES DE GESTIÓN
───────────────────                ─────────────────
QA  QA Engineer                    PM  Product Manager
AR  Architect                      PJM Program Manager
CR  Code Reviewer (externo)
```

### 3.2 Configuración por Proyecto

Al inicio del proyecto, el PM define qué roles participan:

```yaml
# Ejemplo: proyecto_config.yaml
proyecto: "MiProyecto"
roles_activos:
  diseño: [DL, UX]
  código: [TL, DB, BE, FE]
  validación: [QA, AR]
  gestión: [PM]
  
code_review:
  modelo: "escalonado"  # ver §7.3
```

### 3.3 Responsabilidades Detalladas por Rol

#### Tech Lead (TL)

**HANDOFF_TL_ le dice:**
- Qué tareas coordinar (DO, DB, BE) con IDs, horas y complejidad
- Dependencias formales entre módulos
- VTT Planning Data para crear tareas en sistema (TL es responsable de BE+DB+DO)
- Gates: cuándo puede arrancar FE, cuándo puede arrancar QA
- Cómo hacer Code Review: referencia a `CODE_REVIEW_GUIDE.md`
- Qué documentos dinámicos verificar (API_CONTRACT, LOGIC.md, etc.)

**Tareas típicas TL:**
```
TL-001  Code Review PRs Backend       review      3h   MEDIUM
TL-002  Actualización docs dinámicos  documentation  2h   LOW
APR-xxx PM Aprobación final           review      1h   LOW
```

#### Architect (AR)

**Rol en el ecosistema:**
- Participa en Fase 0 (diseño arquitectónico) generando ADRs
- Ejecuta Integration Audit en Fase 3: verifica que la implementación respeta los ADRs
- Tarea formal: `AR-001` con 2-3h MEDIUM/HIGH
- Depende de: TL Code Review completado
- Referencia: `INTEGRATION_AUDIT_CHECKLIST.md`

> **Separación TL vs AR:** TL verifica calidad técnica (patrones, tests, seguridad); AR verifica coherencia arquitectónica (ADRs, boundaries, schema).

#### Design Lead (DL)

**HANDOFF_DL_ le dice:**
- Qué pantallas diseñar (HTML + UX Spec por pantalla)
- Design System a mantener/actualizar
- Flujos de navegación entre pantallas
- VTT Planning Data (DL crea sus propias tareas en sistema)
- Gate APR-DL: PM aprueba HTMLs antes de autorizar arranque de FE

**DL-REVIEW (tarea de validación):**
Tarea formal donde DL verifica que la implementación FE coincide con los HTMLs diseñados.

```
DL-REVIEW  Revisar implementación FE vs HTMLs  3h  MEDIUM  review
```

> **Regla:** DL aprueba diseño. PM aprueba funcionalidad. TL/AR aprueban técnico. Son aprobaciones distintas.

#### Frontend (FE)

**HANDOFF_FE_ le dice:**
- Qué componentes crear (con referencia al HTML de DL)
- Contratos API que consumir (endpoints, schemas, auth)
- Dependencias críticas (ej: @dnd-kit para drag-drop)
- Store Zustand a extender
- VTT Planning Data (FE crea sus propias tareas en sistema)
- DoD: la implementación debe pasar DL-REVIEW

> **Regla crítica:** FE solo implementa lo que DL diseñó. Nunca diseña pantallas. Si el HTML no existe → reportar al PM antes de empezar.

#### QA

**HANDOFF_QA_ le dice:**
- Escenarios de prueba BE (por endpoint)
- Escenarios de prueba FE (por pantalla/componente)
- Escenarios de flujo de navegación (QA-FLOW-*)
- Proceso de bugs via VTT issues
- VTT Planning Data (QA crea sus propias tareas o TL si QA reporta a TL)
- Coverage mínimo requerido: BE ≥ 70%, FE ≥ 60%

**QA-FLOW Scenarios:**
Escenarios específicos que verifican el flujo de navegación entre pantallas.

```
QA-FLOW-01  [Pantalla A] → [Pantalla B]  Navegación automática sin error
QA-FLOW-02  [Step X] → [Step Y]          Progress bar actualizado
QA-FLOW-06  Ruta directa inválida        Redirige al step correcto
```

### 3.4 Matriz de Participación por Fase

| Fase | Roles que participan | Roles que validan |
|------|---------------------|-------------------|
| 0. Planificación | PM, AR, PJM | — |
| 1. Diseño | DL, UX | PM |
| 2. Desarrollo | DB, BE, FE, TL | CR (según tamaño PR) |
| 3. Validación | — | AR, QA, TL, DL |
| 4. Cierre | TL | PM |

---

## 4. FLUJO COMPLETO DEL SPRINT

### 4.1 Diagrama de Fases

```
FASE 0              FASE 1           FASE 2              FASE 3              FASE 4
PLANIFICACIÓN       DISEÑO           DESARROLLO          VALIDACIÓN          CIERRE
─────────────       ──────           ──────────          ──────────          ──────

PM + AR + PJM       DL + UX          DB → BE → FE        AR  QA  TL  DL      TL → PM
     │                 │             (según deps)         │   │   │   │         │
     ▼                 ▼                  │               │   │   │   │         ▼
┌─────────┐      ┌─────────┐              │               ▼   ▼   ▼   ▼    ┌─────────┐
│ Alcance │      │ HTMLs + │              ▼           ┌─────────────────┐  │   APR   │
│ + ADRs  │──────│ Specs   │────────►┌─────────┐      │ 4 VALIDACIONES  │──│  SPRINT │
│         │      │         │         │ Código  │──────│   EN PARALELO   │  │         │
└─────────┘      └─────────┘         │ + Tests │      └─────────────────┘  └─────────┘
     │                 │             └─────────┘              │                  │
     ▼                 ▼                  │                   ▼                  ▼
 Handoffs          APR-DL            Code Review         4 Firmas ✅         Sprint
 generados        (PM aprueba)       (por PR)            requeridas         Cerrado
```

### 4.2 Duración Típica por Fase

| Fase | Duración típica | % del Sprint |
|------|-----------------|--------------|
| 0. Planificación | 0.5-1 día | 5-10% |
| 1. Diseño | 1-2 días | 15-20% |
| 2. Desarrollo | 3-5 días | 50-60% |
| 3. Validación | 1-2 días | 15-20% |
| 4. Cierre | 0.5 día | 5-10% |

---

## 5. FASE 0: PLANIFICACIÓN

### 5.1 Participantes

| Rol | Responsabilidad |
|-----|-----------------|
| PM | Define alcance, prioriza backlog, aprueba estimaciones |
| AR | Diseña arquitectura, genera ADRs si hay decisiones nuevas |
| PJM | Genera handoffs, carga tareas en VTT, configura dependencias |

### 5.2 Entradas

- Backlog priorizado
- Documentación existente (SRS, ADRs previos, MODELO_DATOS)
- Capacidad del equipo

### 5.3 Actividades

```
1. PM presenta alcance del sprint
        │
        ▼
2. AR evalúa impacto arquitectónico
        │
        ├── Hay decisiones nuevas → AR genera ADR_SPRINT_XX.md
        │
        └── No hay decisiones nuevas → Continúa
        │
        ▼
3. PJM estima tareas con input de TL
        │
        ▼
4. PJM genera Handoffs (1 por rol activo)
        │
        ▼
5. PJM carga tareas en VTT con:
   - estimatedHours
   - complexity (LOW | MEDIUM | HIGH)
   - category (development | design | testing | review | documentation)
   - dependsOn (IDs de tareas bloqueantes)
        │
        ▼
6. VTT calcula Gantt + Ruta Crítica automáticamente
```

### 5.4 Salidas

| Entregable | Responsable | Destino |
|------------|-------------|---------|
| `HANDOFF_TL_SPRINT_XX.md` | PJM | TL |
| `HANDOFF_DL_SPRINT_XX.md` | PJM | DL |
| `HANDOFF_FE_SPRINT_XX.md` | PJM | FE |
| `HANDOFF_QA_SPRINT_XX.md` | PJM | QA |
| `ADR_SPRINT_XX.md` (si aplica) | AR | Todos |
| Tareas cargadas en VTT | PJM | Sistema |

### 5.5 Gate de Salida

- [ ] Todos los handoffs generados
- [ ] Todas las tareas cargadas en VTT con campos obligatorios
- [ ] Dependencias configuradas
- [ ] ADRs documentados (si aplica)
- [ ] PM aprueba plan

---

## 6. FASE 1: DISEÑO

### 6.1 Participantes

| Rol | Responsabilidad |
|-----|-----------------|
| DL | Genera HTMLs de pantallas, define componentes |
| UX | Define flujos, estados, microinteracciones |
| PM | Aprueba diseños vs requerimientos funcionales |

### 6.2 Actividades

```
DL + UX reciben HANDOFF_DL
        │
        ▼
Generan HTMLs + UX Specs por pantalla
        │
        ▼
Actualizan Design System (si hay componentes nuevos)
        │
        ▼
Entregan para revisión PM
        │
        ▼
PM revisa diseños vs CAs funcionales
        │
        ├── ✅ Aprobado → APR-DL creado en VTT
        │
        └── 🔴 Cambios requeridos → DL corrige → Re-revisión
```

### 6.3 Salidas

| Entregable | Formato | Ubicación |
|------------|---------|-----------|
| HTMLs de pantallas | `.html` | `/diseño/sprint_XX/` |
| UX Specs | `.md` | `/diseño/sprint_XX/specs/` |
| Design Tokens (si hay nuevos) | `.json` | `/diseño/tokens/` |
| Assets exportados | `.svg`, `.png` | `/diseño/assets/` |

### 6.4 Gate de Salida

- [ ] Todos los HTMLs entregados
- [ ] UX Specs completos (estados, errores, responsive)
- [ ] PM aprobó diseños (APR-DL en VTT)
- [ ] DL notifica a TL que FE puede arrancar

---

## 7. FASE 2: DESARROLLO

### 7.1 Participantes

| Rol | Responsabilidad |
|-----|-----------------|
| DB | Migraciones, seeds, índices |
| BE | Services, endpoints, validaciones |
| FE | Componentes, pantallas, integración API |
| TL | Coordina, desbloquea, hace/asigna Code Review |
| CR | Code Review de PRs según tamaño (externo) |

### 7.2 Secuencia de Ejecución

La secuencia NO es fija — está determinada por las dependencias configuradas en VTT.

```
VTT calcula secuencia automáticamente basado en dependsOn
        │
        ▼
Tareas sin dependencias → Comienzan inmediatamente
        │
        ▼
Tareas con dependencias → Estado 'task_blocked' hasta que dependencias completen
        │
        ▼
Cuando dependencia completa → Sistema desbloquea automáticamente
```

**Patrón típico (no obligatorio):**

```
DB (migraciones)
   │
   ├──► BE (services que usan nuevas tablas)
   │       │
   │       └──► BE (endpoints que usan services)
   │               │
   └───────────────┴──► FE (componentes que consumen endpoints)
                              │
                              └──► FE (pantallas que usan componentes)
```

### 7.3 Code Review — Modelo Escalonado

| Tamaño PR | Líneas | Reviewer | Tiempo máximo |
|-----------|--------|----------|---------------|
| Pequeño | < 100 | TL solo | 4 horas |
| Mediano | 100-500 | TL + Code Reviewer | 8 horas |
| Grande | > 500 | Code Reviewer obligatorio | 24 horas |
| Arquitectura | Cualquiera con ADR | Code Reviewer + AR | 24 horas |

**Flujo de Code Review:**

```
Developer completa tarea
        │
        ▼
Crea PR con:
- Descripción
- Link a tarea VTT
- Tests pasando
- Screenshots (si es FE)
        │
        ▼
¿Tamaño del PR?
        │
        ├── < 100 líneas → TL revisa solo
        │
        ├── 100-500 líneas → TL + Code Reviewer
        │
        └── > 500 líneas → Code Reviewer obligatorio
        │
        ▼
Reviewer usa CODE_REVIEW_GUIDE.md
        │
        ├── ✅ Approved → Merge → Tarea a 'task_in_review'
        │
        └── 🔴 Changes requested → Developer corrige → Re-review
```

### 7.4 Documentación Durante Desarrollo

| Documento | Quién actualiza | Cuándo | Verificado en |
|-----------|----------------|--------|---------------|
| `API_CONTRACT.md` | BE | Al completar endpoint | Code Review |
| `*.LOGIC.md` | BE/DB | Al completar tarea | Code Review |
| `MODELO_DATOS.md` | DB | Al crear/modificar tabla | Code Review |
| DevLog | Todos | Al completar tarea | TL |

### 7.5 DevLog Obligatorio

Todo DevLog debe incluir estas secciones (no opcionales):

```markdown
## Información General
- Fecha, tarea, repo, agente

## Qué se implementó
- Resumen de cambios

## Archivos creados/modificados
- Lista con .LOGIC.md correspondiente

## Decisiones técnicas
- Por qué se eligió X sobre Y

## Issues encontrados
- Errores encontrados durante implementación
- Cómo se resolvieron o por qué quedaron pendientes

## Cómo probar
- Comandos exactos para verificar que funciona

## Dependencias agregadas
- Si se instaló algo nuevo, reportarlo aquí
```

### 7.6 Gate de Salida

- [ ] Todas las tareas de desarrollo en `task_in_review` o `task_completed`
- [ ] Todos los PRs aprobados y mergeados
- [ ] Tests pasando (CI verde)
- [ ] Documentación dinámica actualizada
- [ ] TL confirma que desarrollo está completo

---

## 8. FASE 3: VALIDACIÓN

### 8.1 Modelo de 4 Firmantes

La validación requiere **4 aprobaciones independientes** antes del cierre. Cada firmante valida su área contra documentos de referencia específicos.

```
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDACIONES EN PARALELO                      │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│     AR      │     QA      │     TL      │     DL      │         │
│             │             │             │             │         │
│ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │         │
│ │ ADRs    │ │ │ CAs     │ │ │ API     │ │ │ Impl vs │ │         │
│ │ Schema  │ │ │ Tests   │ │ │ Docs    │ │ │ Diseño  │ │         │
│ │ Bounds  │ │ │ E2E     │ │ │ Security│ │ │         │ │         │
│ │         │ │ │ Integr  │ │ │ CodeRev │ │ │         │ │         │
│ └────┬────┘ │ └────┬────┘ │ └────┬────┘ │ └────┬────┘ │         │
│      │      │      │      │      │      │      │      │         │
│      ▼      │      ▼      │      ▼      │      ▼      │         │
│     ✅?     │     ✅?     │     ✅?     │     ✅?     │         │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
                              │
                    ¿4 firmas ✅?
                              │
              ┌───────────────┴───────────────┐
              │                               │
             Sí                              No
              │                               │
              ▼                               ▼
        FASE 4: CIERRE                 Issues creados
                                       Fix → Re-validar
```

### 8.2 Secuencia de Revisiones

```
[Implementación completa]
        │
        ▼
  TL Code Review (TL-001)              ← calidad técnica, tests, .LOGIC.md
        │
        ▼
  AR Integration Audit (AR-001)        ← ADR compliance, DB schema, boundaries
        │
        ├──── DL-REVIEW (paralelo)     ← impl FE vs HTMLs diseñados
        │
        ├──── QA-FLOW validation       ← flujos de navegación E2E
        │
        ▼
  TL recolecta firmas → APR para PM → sprint cerrado
```

### 8.3 Responsabilidades por Firmante

#### AR — Integration Audit

| Qué valida | Documento de referencia | Evidencia requerida |
|------------|------------------------|---------------------|
| ADRs respetados | `ADR_SPRINT_XX.md` | Checklist vs código |
| Schema implementado = diseñado | `MODELO_DATOS.md` | `\d tabla` vs doc |
| Boundaries correctos | `ARQUITECTURA.md` | Code inspection |
| Integraciones configuradas | Diseño técnico | Test conectividad |

**Guía:** `guias/INTEGRATION_AUDIT_CHECKLIST.md`

#### QA — Testing & Functional Validation

| Qué valida | Documento de referencia | Evidencia requerida |
|------------|------------------------|---------------------|
| CAs cumplidos | User Stories / SRS | Test results |
| Cobertura de tests | `TESTING_GUIDE.md` | Coverage report |
| Flujos E2E funcionan | Test Cases | E2E passing |
| Integraciones operativas | Specs de integración | Integration tests |

**Guía:** `guias/TESTING_GUIDE.md`

#### TL — Technical Validation

| Qué valida | Documento de referencia | Evidencia requerida |
|------------|------------------------|---------------------|
| API contracts completos | `API_CONTRACT.md` | Swagger vs doc |
| Docs dinámicos actualizados | Lista docs sprint | Docs actuales |
| Code Review completado | `CODE_REVIEW_GUIDE.md` | PRs aprobados |
| Seguridad implementada | Specs de seguridad | Auth/permisos OK |

**Guía:** `guias/CODE_REVIEW_GUIDE.md`

#### DL — Design Validation

| Qué valida | Documento de referencia | Evidencia requerida |
|------------|------------------------|---------------------|
| Implementación = Diseño | HTMLs + UX Specs | Screenshots comparativos |
| Responsive funciona | Breakpoints definidos | Test en dispositivos |
| Estados visuales correctos | UX Specs | Demo de estados |
| Design tokens aplicados | Design System | Inspección CSS |

### 8.4 Proceso de Validación

```
Desarrollo completo
        │
        ▼
TL notifica inicio de validación
        │
        ▼
4 validadores ejecutan EN PARALELO:
        │
        ├── AR: Integration Audit (1-2h)
        │
        ├── QA: Testing validation (2-4h)
        │
        ├── TL: Technical validation (1-2h)
        │
        └── DL: Design validation (1-2h)
        │
        ▼
Cada validador:
        │
        ├── ✅ Aprobado → Firma en VTT (tarea APR-XX-[ROL])
        │
        └── 🔴 Issues encontrados:
                │
                ├── Crea Issue en VTT con severidad
                │
                ├── Asigna a responsable
                │
                └── NO firma hasta que se resuelvan S1/S2
        │
        ▼
¿4 firmas completas?
        │
        ├── Sí → Continúa a Fase 4
        │
        └── No → Resolver issues → Re-validar áreas afectadas
```

### 8.5 Severidad de Issues

| Severidad | Definición | Acción | Bloquea firma |
|-----------|------------|--------|---------------|
| **S1 - Blocker** | Funcionalidad core rota | Fix inmediato | ✅ Sí |
| **S2 - Critical** | Feature importante no funciona | Fix antes de cierre | ✅ Sí |
| **S3 - Major** | Feature secundaria afectada | Fix en siguiente sprint | ❌ No |
| **S4 - Minor** | Cosmético, UX degradada | Backlog | ❌ No |

### 8.6 Proceso de Bugs (VTT Issues)

**Regla:** Bugs NO se crean como tareas directas. Se reportan como issues vinculados a la tarea origen.

```
Bug detectado por QA
        │
        ▼
POST /api/tasks/{taskId}/issues      ← tarea pasa a on_hold automáticamente
        │
        ▼
TL crea FIX task → asigna al agente responsable
        │
        ▼
Agente ejecuta fix (workflow completo: código + devlog + .LOGIC.md + PR)
        │
        ▼
TL revisa fix → FIX task a task_completed
        │
        ▼
PUT /api/issues/{id} {"isResolved": true}  ← tarea vuelve a previousStatus
```

> **NUNCA:** `PUT /api/issues/{id}` sin fix real ejecutado. Bypasea trazabilidad y el sistema queda inconsistente.

### 8.7 Gate de Salida

- [ ] AR firmó (APR-AR en VTT)
- [ ] QA firmó (APR-QA en VTT)
- [ ] TL firmó (APR-TL en VTT)
- [ ] DL firmó (APR-DL-REVIEW en VTT)
- [ ] No hay issues S1 o S2 abiertos
- [ ] Issues S3/S4 documentados para siguiente sprint

---

## 9. FASE 4: CIERRE

### 9.1 Participantes

| Rol | Responsabilidad |
|-----|-----------------|
| TL | Recolecta 4 firmas, genera APR-SPRINT |
| PM | Revisión final, aprobación, cierre oficial |

### 9.2 Proceso de Cierre

```
4 firmas completas (AR + QA + TL + DL)
        │
        ▼
TL genera APR-SPRINT-XX en VTT
        │
        ├── Adjunta: 4 firmas
        │
        ├── Adjunta: Issues S3/S4 pendientes
        │
        └── Adjunta: Métricas del sprint
        │
        ▼
PM revisa APR-SPRINT
        │
        ├── ✅ Aprobado → PM mueve sprint a 'task_approved'
        │
        └── 🔴 Rechazado → Vuelve a Fase 3
        │
        ▼
Sprint cerrado oficialmente
        │
        ▼
PJM genera retrospectiva (opcional)
```

### 9.3 Contenido de APR-SPRINT

```markdown
# APR-SPRINT-XX: [Nombre del Sprint]

## Firmas de Validación

| Rol | Firmante | Fecha | Estado |
|-----|----------|-------|--------|
| AR | [Nombre] | YYYY-MM-DD | ✅ APROBADO |
| QA | [Nombre] | YYYY-MM-DD | ✅ APROBADO |
| TL | [Nombre] | YYYY-MM-DD | ✅ APROBADO |
| DL | [Nombre] | YYYY-MM-DD | ✅ APROBADO |

## Métricas del Sprint

| Métrica | Planificado | Real | Variación |
|---------|-------------|------|-----------|
| Horas totales | XX | XX | +/- XX% |
| Tareas completadas | XX | XX | XX% |
| Issues S1/S2 | 0 | X | — |
| Cobertura tests | XX% | XX% | +/- XX% |

## Issues Pendientes (S3/S4)

| ID | Descripción | Severidad | Asignado a sprint |
|----|-------------|-----------|-------------------|
| ISS-001 | ... | S3 | Sprint XX+1 |

## Decisión

- [x] APROBADO para release
- [ ] APROBADO con condiciones
- [ ] RECHAZADO

**Firma PM:** _______________
**Fecha:** _______________
```

### 9.4 Gate de Salida

- [ ] APR-SPRINT generado con 4 firmas
- [ ] PM revisó y aprobó
- [ ] Sprint marcado como `task_approved` en VTT
- [ ] Issues S3/S4 movidos a backlog del siguiente sprint

---

## 10. DOCUMENTOS DE REFERENCIA

### 10.1 Estructura de Archivos

```
/metodologia/
├── METODOLOGIA_EJECUCION_SPRINTS_V1.md    ← Este documento
│
├── /guias/                                 ← Guías cross-sprint
│   ├── CODE_REVIEW_GUIDE.md               
│   ├── INTEGRATION_AUDIT_CHECKLIST.md     
│   └── TESTING_GUIDE.md                   
│
├── /templates/                             ← Templates de handoffs
│   ├── TEMPLATE_HANDOFF_TL.md
│   ├── TEMPLATE_HANDOFF_DL.md
│   ├── TEMPLATE_HANDOFF_FE.md
│   ├── TEMPLATE_HANDOFF_QA.md
│   ├── TEMPLATE_BRIEF_SHORT.md
│   ├── TEMPLATE_BRIEF_LARGE.md
│   └── TEMPLATE_DEVLOG.md
│
└── /ejemplos/                              ← Ejemplos reales
    └── EJEMPLO_SPRINT_5D.md
```

### 10.2 Cuándo Consultar Cada Guía

| Guía | Quién la usa | Cuándo |
|------|--------------|--------|
| `CODE_REVIEW_GUIDE.md` | TL, CR, Devs | Durante Code Review (Fase 2) |
| `INTEGRATION_AUDIT_CHECKLIST.md` | AR | Durante Integration Audit (Fase 3) |
| `TESTING_GUIDE.md` | QA, Devs | Durante desarrollo y validación (Fases 2-3) |

### 10.3 Templates Disponibles

| Template | Uso |
|----------|-----|
| `TEMPLATE_HANDOFF_TL.md` | Generar handoff para Tech Lead |
| `TEMPLATE_HANDOFF_DL.md` | Generar handoff para Design Lead |
| `TEMPLATE_HANDOFF_FE.md` | Generar handoff para Frontend |
| `TEMPLATE_HANDOFF_QA.md` | Generar handoff para QA |
| `TEMPLATE_BRIEF_SHORT.md` | Brief corto para tareas simples |
| `TEMPLATE_BRIEF_LARGE.md` | Brief extenso para features complejas |
| `TEMPLATE_DEVLOG.md` | Documentar trabajo completado |

---

## 11. VTT — CAMPOS Y ESTADOS

### 11.1 Campos Obligatorios por Tarea

| Campo | Tipo | Obligatorio | Qué hace el sistema |
|-------|------|-------------|---------------------|
| `title` | string | ✅ | Nombre descriptivo de la tarea |
| `estimatedHours` | number | ✅ | Calcula duración barra Gantt |
| `complexity` | enum | ✅ | `LOW` \| `MEDIUM` \| `HIGH` — Reglas auto-dependencias |
| `category` | enum | ✅ | Agrupación en burndown y métricas |
| `dependsOn` | ID[] | cuando aplica | Configura BFS propagation |
| `assignee` | ID | ✅ | Agente responsable |
| `plannedStartDate` | ISO date | opcional | El algoritmo lo calcula si hay Gantt activo |
| `plannedEndDate` | ISO date | opcional | El algoritmo propaga en cascada |

> **Si falta `complexity` o `category`:** la API rechaza la tarea (400 error).

### 11.2 Responsabilidad de Carga

| Rol | Quién crea las tareas en VTT |
|-----|------------------------------|
| DO, DB, BE | TL (coordina estos agentes) |
| TL, AR | TL (sus propias tareas) |
| DL | DL (si es líder) o TL (si DL reporta a TL) |
| FE | FE (si es líder) o TL (si FE reporta a TL) |
| QA | QA (si es líder) o TL (si QA reporta a TL) |

> **Regla:** Las tareas las crea el líder del agente, no el agente que ejecuta.

### 11.3 Proceso de Modificación de Tiempos

| Campo | Quién puede modificar | Cuándo |
|-------|----------------------|--------|
| `estimatedHours` | Agente ejecutor + TL | Antes de in_progress; comentario obligatorio |
| `plannedStartDate/EndDate` | Solo TL o PM | Con plan Gantt activo; el algoritmo propaga |
| `actualHours` | Sistema automático | Via `SUM(timeEntries.hours)` — no modificar manualmente |

> **Si se cambia `estimatedHours`:** Postear comentario obligatorio: `"Cambio estimación: Xh → Yh. Razón: [...]"`

### 11.4 Estados de Tarea

```
task_draft
    │
    ▼
task_ready ──────────────────────────────────────┐
    │                                            │
    ▼                                            │
task_blocked (si tiene dependencias)             │
    │                                            │
    │ (dependencias completas)                   │
    ▼                                            │
task_in_progress ◄───────────────────────────────┘
    │
    ▼
task_in_review
    │
    ├── (rechazado) ──► task_in_progress
    │
    ▼
task_completed
    │
    ▼
task_approved  ← ESTADO TERMINAL (solo PM)
```

### 11.5 Tareas Especiales de Validación

| Tarea | Responsable | Fase | Descripción |
|-------|-------------|------|-------------|
| `APR-DL` | PM | 1 | Aprobación de diseños |
| `APR-AR` | AR | 3 | Firma de Integration Audit |
| `APR-QA` | QA | 3 | Firma de Testing Validation |
| `APR-TL` | TL | 3 | Firma de Technical Validation |
| `APR-DL-REVIEW` | DL | 3 | Firma de Design Validation |
| `APR-SPRINT` | PM | 4 | Cierre oficial del sprint |

---

## 12. CHECKLIST RÁPIDO POR FASE

### Fase 0: Planificación
```
[ ] Alcance definido por PM
[ ] AR evaluó impacto arquitectónico
[ ] ADRs generados (si aplica)
[ ] Handoffs generados (TL, DL, FE, QA)
[ ] Tareas cargadas en VTT con campos obligatorios
[ ] Dependencias configuradas
[ ] PM aprobó plan
```

### Fase 1: Diseño
```
[ ] DL + UX recibieron HANDOFF_DL
[ ] HTMLs generados para todas las pantallas
[ ] UX Specs completos
[ ] Design System actualizado (si aplica)
[ ] PM aprobó diseños (APR-DL)
[ ] TL notificado para desbloquear FE
```

### Fase 2: Desarrollo
```
[ ] Tareas ejecutadas según dependencias VTT
[ ] PRs creados con descripción + tests
[ ] Code Review completado (según tamaño)
[ ] Documentación dinámica actualizada
[ ] CI verde (tests pasando)
[ ] TL confirma desarrollo completo
```

### Fase 3: Validación
```
[ ] AR ejecutó Integration Audit → APR-AR
[ ] QA ejecutó Testing Validation → APR-QA
[ ] TL ejecutó Technical Validation → APR-TL
[ ] DL ejecutó Design Validation → APR-DL-REVIEW
[ ] No hay issues S1/S2 abiertos
[ ] Issues S3/S4 documentados
```

### Fase 4: Cierre
```
[ ] 4 firmas completas
[ ] TL generó APR-SPRINT
[ ] PM revisó APR-SPRINT
[ ] PM aprobó sprint (task_approved)
[ ] Issues pendientes movidos a siguiente sprint
```

---

## 13. APÉNDICE: FIRMAS Y APROBACIONES

### 13.1 Registro de Firmas por Sprint

Este apéndice debe completarse para cada sprint. Sirve como registro formal de las aprobaciones.

```
═══════════════════════════════════════════════════════════════════
                    REGISTRO DE FIRMAS — SPRINT [XX]
═══════════════════════════════════════════════════════════════════

PROYECTO: _______________________
SPRINT:   _______________________
PERÍODO:  _______________________ a _______________________

───────────────────────────────────────────────────────────────────
                         FASE 1: DISEÑO
───────────────────────────────────────────────────────────────────

APROBACIÓN DE DISEÑOS (APR-DL)

Diseños entregados por:
  DL: _________________________ Fecha: _______________

Aprobado por:
  PM: _________________________ Fecha: _______________
      Firma: _________________________

Observaciones:
___________________________________________________________________
___________________________________________________________________

───────────────────────────────────────────────────────────────────
                       FASE 3: VALIDACIÓN
───────────────────────────────────────────────────────────────────

INTEGRATION AUDIT (APR-AR)

Ejecutado por:
  AR: _________________________ Fecha: _______________

Resultado:
  [ ] APROBADO sin observaciones
  [ ] APROBADO con observaciones menores (S3/S4)
  [ ] RECHAZADO — Issues S1/S2 pendientes

Issues encontrados:
  S1: _____ S2: _____ S3: _____ S4: _____

Firma AR: _________________________

───────────────────────────────────────────────────────────────────

TESTING VALIDATION (APR-QA)

Ejecutado por:
  QA: _________________________ Fecha: _______________

Cobertura alcanzada:
  BE Unit: _____%    FE Unit: _____%
  Integration: _____%    E2E: _____%

Resultado:
  [ ] APROBADO sin observaciones
  [ ] APROBADO con observaciones menores (S3/S4)
  [ ] RECHAZADO — Issues S1/S2 pendientes

Issues encontrados:
  S1: _____ S2: _____ S3: _____ S4: _____

Firma QA: _________________________

───────────────────────────────────────────────────────────────────

TECHNICAL VALIDATION (APR-TL)

Ejecutado por:
  TL: _________________________ Fecha: _______________

PRs revisados: _____
Documentación actualizada: [ ] Sí [ ] No

Resultado:
  [ ] APROBADO sin observaciones
  [ ] APROBADO con observaciones menores (S3/S4)
  [ ] RECHAZADO — Issues S1/S2 pendientes

Issues encontrados:
  S1: _____ S2: _____ S3: _____ S4: _____

Firma TL: _________________________

───────────────────────────────────────────────────────────────────

DESIGN VALIDATION (APR-DL-REVIEW)

Ejecutado por:
  DL: _________________________ Fecha: _______________

Pantallas verificadas: _____ / _____

Resultado:
  [ ] APROBADO — Implementación coincide con diseño
  [ ] APROBADO con ajustes menores (S3/S4)
  [ ] RECHAZADO — Discrepancias significativas

Issues encontrados:
  S1: _____ S2: _____ S3: _____ S4: _____

Firma DL: _________________________

───────────────────────────────────────────────────────────────────
                        FASE 4: CIERRE
───────────────────────────────────────────────────────────────────

RESUMEN DE FIRMAS

| Rol | Firmante        | Fecha      | Estado    |
|-----|-----------------|------------|-----------|
| AR  | _______________ | __________ | _________ |
| QA  | _______________ | __________ | _________ |
| TL  | _______________ | __________ | _________ |
| DL  | _______________ | __________ | _________ |

APROBACIÓN FINAL (APR-SPRINT)

[ ] Las 4 firmas están completas
[ ] No hay issues S1/S2 abiertos
[ ] Issues S3/S4 documentados para siguiente sprint

Decisión PM:
  [ ] ✅ APROBADO — Sprint cerrado exitosamente
  [ ] ⚠️ APROBADO CON CONDICIONES — Ver observaciones
  [ ] ❌ RECHAZADO — Volver a Fase 3

Observaciones:
___________________________________________________________________
___________________________________________________________________
___________________________________________________________________

Firma PM: _________________________
Fecha:   _________________________

═══════════════════════════════════════════════════════════════════
                         FIN DEL REGISTRO
═══════════════════════════════════════════════════════════════════
```

### 13.2 Instrucciones para Completar el Registro

1. **Crear una copia** de este registro para cada sprint
2. **Nombrar el archivo:** `FIRMAS_SPRINT_XX.md`
3. **Completar progresivamente** a medida que avanza el sprint
4. **Archivar** junto con los handoffs del sprint al cerrar

### 13.3 Validación del Registro

Antes de que PM apruebe el cierre:

- [ ] Todas las secciones completadas
- [ ] Todas las firmas presentes
- [ ] Fechas consistentes con timeline del sprint
- [ ] Issues documentados con severidad correcta
- [ ] Archivo guardado en ubicación estándar

---

## 14. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-03-30 | PJM-Agent | Versión inicial — consolida proceso + ecosistema de documentos |

---

**FIN DEL DOCUMENTO**
