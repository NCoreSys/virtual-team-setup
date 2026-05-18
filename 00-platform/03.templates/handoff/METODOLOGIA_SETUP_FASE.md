# METODOLOGÍA: Setup de Fase/Bloque

**Documento:** METODOLOGIA_SETUP_FASE.md  
**Versión:** 1.0  
**Autor:** PJM-Agent  
**Fecha:** 2026-04-02  
**Audiencia:** TL (Tech Lead)  
**Propósito:** Definir el proceso formal de inicio de fase/bloque en VTT

---

## 1. PRINCIPIO FUNDAMENTAL

> **Toda actividad tiene inicio y fin.**

Así como definimos el proceso de cierre (METODOLOGIA_CIERRE_SPRINT_FASE.md), necesitamos definir el proceso de inicio. Sin un nodo de inicio formal:

- No hay estructura en VTT para dar seguimiento
- Los agentes no saben qué tareas existen
- No hay dependencias configuradas
- No hay contexto compartido

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUJO COMPLETO DE FASE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   SETUP      │───▶│   EJECUCIÓN  │───▶│   CIERRE     │                  │
│  │   (TL)       │    │  (Sprints)   │    │   (PM)       │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│        │                    │                   │                           │
│        │                    │                   │                           │
│   METODOLOGIA_         HANDOFF_TL_S[N]     CLOSURE_S[N]                    │
│   SETUP_FASE.md        (ejecución)         CLOSURE_BLOQUE                  │
│   SETUP_BLOQUE_[N].md                      (firmas + PM)                   │
│        │                                                                    │
│        ▼                                                                    │
│   Tarea SETUP-BLOQUE-[N]                                                   │
│   en VTT como gate                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. OBJETIVO DEL SETUP

El Setup de Fase tiene como objetivo:

| # | Objetivo | Resultado |
|---|----------|-----------|
| 1 | Crear estructura en VTT | Proyecto, releases, sprints existen en BD |
| 2 | Crear todas las tareas | Tareas de todos los sprints registradas |
| 3 | Configurar dependencias | Flujo de ejecución definido |
| 4 | Documentar contexto | IDs, estructura disponible para agentes |
| 5 | Establecer gate de inicio | Sprints no pueden iniciar hasta que setup complete |

---

## 3. RESPONSABLE

**TL (Tech Lead)** es responsable de ejecutar el Setup de Fase porque:

- Conoce la estructura técnica del proyecto
- Tiene acceso a crear tareas en VTT
- Coordina a los agentes de desarrollo
- Es el punto de entrada para la ejecución

---

## 4. PROCESO DE SETUP

### 4.1 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROCESO: SETUP DE FASE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────┐                                   │
│  │ 1. TL recibe SETUP_BLOQUE_[N].md    │                                   │
│  │    del PJM con instrucciones        │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 2. TL verifica prerrequisitos:      │                                   │
│  │    • Fase anterior cerrada          │                                   │
│  │    • HANDOFFs disponibles           │                                   │
│  │    • Acceso a VTT                   │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 3. TL crea/verifica proyecto en VTT │                                   │
│  │    POST /api/projects               │                                   │
│  │    (si no existe)                   │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 4. TL crea releases si necesario    │                                   │
│  │    POST /api/projects/:id/releases  │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 5. TL crea sprints del bloque       │                                   │
│  │    POST /api/releases/:id/sprints   │                                   │
│  │    (S09, S10, S11, etc.)            │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 6. TL lee TODOS los HANDOFFs        │                                   │
│  │    del bloque y extrae tareas       │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 7. TL crea TODAS las tareas         │                                   │
│  │    POST /api/projects/:id/tasks     │                                   │
│  │    con dependencias configuradas    │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 8. TL crea tareas de CIERRE         │                                   │
│  │    CIERRE-S[N] por cada sprint      │                                   │
│  │    CIERRE-BLOQUE-[N] para fase      │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 9. TL documenta contexto            │                                   │
│  │    • IDs de proyecto, releases      │                                   │
│  │    • IDs de sprints                 │                                   │
│  │    • IDs de tareas clave            │                                   │
│  │    → CONTEXTO_BLOQUE_[N].md         │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 10. TL marca SETUP-BLOQUE-[N]       │                                   │
│  │     como task_completed             │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 11. FASE LISTA PARA EJECUTAR        │                                   │
│  │     • Sprints pueden iniciar        │                                   │
│  │     • Agentes tienen contexto       │                                   │
│  │     • Dependencias configuradas     │                                   │
│  └─────────────────────────────────────┘                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Tarea SETUP como Gate

La tarea `SETUP-BLOQUE-[N]` funciona como gate de inicio:

```
SETUP-BLOQUE-2 (task_completed)
       │
       ├────────────────────────────────────┐
       │                                    │
       ▼                                    ▼
Primera tarea S09               Primera tarea S10
(puede iniciar)                 (puede iniciar cuando S09 termine)
```

**Todas las tareas de desarrollo dependen de SETUP-BLOQUE-[N].**

---

## 5. ENTRADAS Y SALIDAS

### 5.1 Entradas (lo que TL necesita)

| Entrada | Descripción | Fuente |
|---------|-------------|--------|
| SETUP_BLOQUE_[N].md | Instrucciones específicas del bloque | PJM |
| HANDOFF_TL_S[N].md | Tareas de cada sprint | PJM |
| HANDOFF_DL_S[N].md | Tareas de diseño (si hay FE) | PJM |
| HANDOFF_FE_S[N].md | Tareas de frontend (si hay FE) | PJM |
| HANDOFF_QA_S[N].md | Tareas de QA | PJM |
| Acceso a VTT API | Credenciales y permisos | DevOps |

### 5.2 Salidas (lo que TL produce)

| Salida | Descripción | Uso |
|--------|-------------|-----|
| Proyecto en VTT | Estructura base | Todos los agentes |
| Releases creados | Contenedores de sprints | Planificación |
| Sprints creados | S09, S10, S11, etc. | Asignación de tareas |
| Tareas creadas | Todas las tareas del bloque | Ejecución |
| Dependencias | Flujo de ejecución | Desbloqueo automático |
| CONTEXTO_BLOQUE_[N].md | IDs y estructura | Todos los agentes |

---

## 6. ESTRUCTURA DE TAREAS

### 6.1 Tipos de Tareas a Crear

| Tipo | Ejemplo | Categoría | Creado por |
|------|---------|-----------|------------|
| Setup | SETUP-BLOQUE-2 | setup | TL |
| Desarrollo DB | DB-S09-01 | development | TL (desde HANDOFF) |
| Desarrollo BE | BE-S09a | development | TL (desde HANDOFF) |
| Desarrollo FE | FE-S11-01 | development | TL (desde HANDOFF) |
| Diseño | DL-S11-01 | design | TL (desde HANDOFF) |
| Review | TL-S09-01 | review | TL (desde HANDOFF) |
| Audit | AR-S09-01 | review | TL (desde HANDOFF) |
| Testing | QA-S09-01 | testing | TL (desde HANDOFF) |
| Cierre Sprint | CIERRE-S09 | review | TL |
| Cierre Bloque | CIERRE-BLOQUE-2 | review | TL |

### 6.2 Dependencias Estándar

```
SETUP-BLOQUE-[N]
       │
       ├──► DB-S[N]-01 ──► DB-S[N]-02 ──► ...
       │         │
       │         ▼
       ├──► BE-S[N]a ──► BE-S[N]b ──► ...
       │                      │
       │                      ▼
       │              TL-S[N]-01 (Code Review)
       │                      │
       │                      ▼
       │              AR-S[N]-01 (Integration Audit)
       │                      │
       │                      ▼
       │              CIERRE-S[N]
       │                      │
       ▼                      ▼
CIERRE-BLOQUE-[N] ◄───────────┘
```

---

## 7. DOCUMENTO DE CONTEXTO

Al finalizar el Setup, TL genera `CONTEXTO_BLOQUE_[N].md` con:

```markdown
# CONTEXTO: Bloque [N] — [Nombre]

## 1. IDs del Proyecto

| Entidad | ID | Nombre |
|---------|-----|--------|
| Proyecto | uuid-xxx | VTT V4 |
| Release | uuid-xxx | V4.0 |

## 2. IDs de Sprints

| Sprint | ID | Nombre |
|--------|-----|--------|
| S09 | uuid-xxx | Catálogos + Trazabilidad |
| S10 | uuid-xxx | Fulfillment + Devlog |

## 3. IDs de Tareas Clave

| Tarea | ID | Sprint |
|-------|-----|--------|
| SETUP-BLOQUE-2 | uuid-xxx | — |
| CIERRE-S09 | uuid-xxx | S09 |
| CIERRE-S10 | uuid-xxx | S10 |
| CIERRE-BLOQUE-2 | uuid-xxx | — |

## 4. Estructura de Fases

| Fase | Código | ID |
|------|--------|-----|
| Planning | 01-planning | uuid-xxx |
| Development | 04-development | uuid-xxx |
| Testing | 05-testing | uuid-xxx |

## 5. Agentes Asignados

| Rol | UUID | Nombre |
|-----|------|--------|
| TL | uuid-xxx | TL-Agent |
| AR | uuid-xxx | AR-Agent |
| DB | uuid-xxx | DB-Agent |
| BE | uuid-xxx | BE-Agent |
| QA | uuid-xxx | QA-Agent |
```

Este documento es la **referencia compartida** para todos los agentes durante la ejecución.

---

## 8. CHECKLIST DEL TL

```markdown
## Setup de Fase — Checklist TL

### Prerrequisitos
[ ] Fase anterior cerrada (si aplica)
[ ] HANDOFFs disponibles en /outputs/
[ ] SETUP_BLOQUE_[N].md recibido
[ ] Acceso a VTT API verificado

### Estructura
[ ] Proyecto existe o creado
[ ] Release existe o creado
[ ] Sprints del bloque creados
[ ] Fases del proyecto configuradas

### Tareas
[ ] Todas las tareas de DB creadas
[ ] Todas las tareas de BE creadas
[ ] Todas las tareas de FE creadas (si aplica)
[ ] Todas las tareas de DL creadas (si aplica)
[ ] Todas las tareas de QA creadas
[ ] Tareas de review (TL, AR) creadas
[ ] Tareas de CIERRE-S[N] creadas
[ ] Tarea CIERRE-BLOQUE-[N] creada

### Dependencias
[ ] Dependencias entre tareas configuradas
[ ] SETUP-BLOQUE-[N] es dependencia de primera tarea de cada sprint
[ ] CIERRE-S[N] depende de última tarea de validación
[ ] CIERRE-BLOQUE-[N] depende de todos los CIERRE-S[N]

### Documentación
[ ] CONTEXTO_BLOQUE_[N].md generado
[ ] IDs documentados
[ ] Agentes notificados

### Cierre Setup
[ ] SETUP-BLOQUE-[N] marcado como task_completed
[ ] Fase lista para ejecutar
```

---

## 9. ERRORES COMUNES

| Error | Consecuencia | Prevención |
|-------|--------------|------------|
| No crear tarea SETUP | Sin gate de inicio | Siempre crear SETUP primero |
| Olvidar dependencias | Tareas se ejecutan en desorden | Revisar HANDOFF sección dependencias |
| No documentar IDs | Agentes no encuentran entidades | Siempre generar CONTEXTO |
| Crear tareas incompletas | Faltan campos requeridos | Usar JSON del HANDOFF |
| No crear tareas de cierre | Sprint/fase nunca se cierra formalmente | Incluir CIERRE en setup |

---

## 10. RELACIÓN CON OTROS DOCUMENTOS

| Documento | Relación |
|-----------|----------|
| SETUP_BLOQUE_[N].md | Instrucciones específicas (usa esta metodología) |
| HANDOFF_TL_S[N].md | Fuente de tareas a crear |
| CONTEXTO_BLOQUE_[N].md | Salida del setup |
| METODOLOGIA_CIERRE_SPRINT_FASE.md | Proceso complementario (cierre) |
| CLOSURE_S[N].md | Tareas de cierre a crear |

---

## 11. IMPLEMENTACIÓN FUTURA

### 11.1 Fase Actual (Manual)

- TL lee SETUP_BLOQUE_[N].md
- TL crea estructura manualmente via API
- TL documenta contexto manualmente

### 11.2 Fase Futura (Automatizado)

Cuando se implemente automatización:

1. PJM genera SETUP_BLOQUE_[N].md
2. Sistema parsea HANDOFFs automáticamente
3. Sistema crea estructura y tareas
4. Sistema genera CONTEXTO automáticamente
5. TL solo revisa y aprueba

---

## 12. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-04-02 | PJM-Agent | Versión inicial |

---

**FIN DEL DOCUMENTO METODOLÓGICO**
