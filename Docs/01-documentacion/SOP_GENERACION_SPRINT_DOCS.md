# SOP: Generación de Documentación de Sprint (SETUP + HANDOFF + CLOSURE)

**Proceso:** Generación del trío de documentos por sprint para Memory Service
**Versión:** 1.0
**Fecha:** 2026-05-12
**Actor principal:** PJM (Project Manager Agent)
**Metodología:** Basado en `SOP_Generation_Guide.md`

---

## 1. Portada

| Campo | Valor |
|-------|-------|
| **Nombre del proceso** | Generación de documentación de sprint (trío SETUP + HANDOFF_TL + CLOSURE) |
| **Trigger de inicio** | PM o SA asigna un sprint a documentar / Sprint anterior completado |
| **Condición de fin** | 3 documentos entregados, revisados por SA, sin correcciones pendientes |
| **Actores** | PJM (ejecutor), SA (reviewer), PM (proveedor de contexto), TL (consumidor) |
| **Sistemas** | VTT API (destino de los scripts), repositorio Git (destino de archivos) |
| **Artefactos producidos** | SETUP_S[N].md, HANDOFF_TL_S[N].md, CLOSURE_S[N].md |

---

## 2. Leyenda de Simbología

| Elemento | Representación | Uso |
|----------|---------------|-----|
| Inicio / Fin | `[START]` / `[END]` | Puntos de entrada y salida del proceso |
| Paso de proceso | `PJM: Acción` | Acción ejecutada por un actor |
| Decisión | `¿Pregunta?` → Sí/No | Bifurcación del flujo |
| Documento | `>> Documento <<` | Artefacto generado o consumido |
| Nota contextual | `(nota)` | Regla de negocio o restricción |

---

## 3. Actores y Responsabilidades

| Actor | Tipo | Responsabilidad |
|-------|------|----------------|
| **PJM** | Agente IA | Ejecuta el proceso completo: recopila inputs, analiza scope, genera los 3 documentos, corrige tras review |
| **SA** | Agente IA | Revisa los 3 documentos contra las 4 metodologías base. Aprueba o devuelve con correcciones |
| **PM** | Humano | Provee contexto adicional si el PJM lo solicita. Sube documentos faltantes. Aprueba el resultado final |
| **TL** | Agente IA | Consumidor final. Ejecuta SETUP en VTT, usa HANDOFF para coordinar agentes, gestiona CLOSURE para cierre |

---

## 4. Artefactos del Proceso

| Artefacto | Tipo | Generado en | Consumido por |
|-----------|------|-------------|---------------|
| `3B.9.9_capacity_plan.md` | Input | Pre-existente (TL) | PJM (Fase 1) |
| `3B.9.3_task_breakdown.md` | Input | Pre-existente (TL) | PJM (Fase 1) |
| `3B.9.7_dependencies_map.md` | Input | Pre-existente (TL) | PJM (Fase 2) |
| `CONTEXTO_S[N-1].md` | Input | Sprint anterior (TL) | PJM (Fase 2) |
| `4 metodologías base` | Referencia | Pre-existente | PJM (Fase 3), SA (Fase 4) |
| `SETUP_S[N].md` | Output | PJM (Fase 3) | TL (ejecución) |
| `HANDOFF_TL_S[N].md` | Output | PJM (Fase 3) | TL (ejecución), BE/FE/DB/DO (lectura) |
| `CLOSURE_S[N].md` | Output | PJM (Fase 3) | PM (sign-off), TL/AR/DL/QA (firmas) |

---

## 5. Diagrama de Flujo del Proceso Principal

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                 FASE 1: RECOPILACIÓN DE INPUTS                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  [START] Sprint S[N] asignado a documentar                                      │
│     │                                                                           │
│     ▼                                                                           │
│  PJM: Identificar documentos requeridos                                         │
│     │                                                                           │
│     ├── >> 3B.9.9 Capacity Plan << (deliverables por sprint)                    │
│     ├── >> 3B.9.3 Task Breakdown << (detalle individual de cada deliverable)    │
│     ├── >> 3B.9.7 Dependencies Map << (dependencias críticas)                   │
│     ├── >> CONTEXTO_S[N-1] << (IDs VTT del sprint anterior)                    │
│     └── >> 4 metodologías base << (SETUP_FASE, PLAN_VTT, EJECUCION, CIERRE)   │
│                                                                                 │
│     ▼                                                                           │
│  ◆ ¿Todos los inputs disponibles?                                               │
│     │                                                                           │
│     ├── NO → PJM: Solicitar documentos faltantes al PM                          │
│     │         │                                                                 │
│     │         ▼                                                                 │
│     │    PM: Sube documentos faltantes                                          │
│     │         │                                                                 │
│     │         └── (volver a verificar inputs)                                   │
│     │                                                                           │
│     └── SÍ → continuar                                                          │
│                                                                                 │
│     (REGLA: NO generar nada sin todos los inputs. No inventar datos.)           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                 FASE 2: ANÁLISIS DEL SPRINT                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  PJM: Extraer deliverables del sprint desde 3B.9.9                              │
│     │                                                                           │
│     ▼                                                                           │
│  PJM: Para cada deliverable, obtener de 3B.9.3:                                │
│     ├── ID catálogo (ej: 4.2.3)                                                │
│     ├── Nombre completo                                                         │
│     ├── Rol responsable (BE, DB, FE, DO, QA, TL)                               │
│     ├── Horas estimadas / SP                                                    │
│     ├── Complejidad (LOW / MEDIUM / HIGH / VERY HIGH)                           │
│     ├── Aplica (✅ / ⚪ / ❌)                                                   │
│     └── Dependencias (internas y externas)                                      │
│                                                                                 │
│     (REGLA: Deliverables ❌ → NO crear. Deliverables ⚪ → crear con flag.)      │
│                                                                                 │
│     ▼                                                                           │
│  PJM: Identificar roles activos en el sprint                                    │
│     │                                                                           │
│     ▼                                                                           │
│  ◆ ¿El sprint tiene FE?                                                         │
│     ├── SÍ → 3 firmas cierre: TL + AR + DL. Agregar DL-S[N]-REV.              │
│     └── NO → 2 firmas cierre: TL + AR solamente.                               │
│                                                                                 │
│     ▼                                                                           │
│  PJM: Mapear dependencias desde 3B.9.7 + CONTEXTO_S[N-1]                       │
│     ├── Cross-sprint: IDs VTT de tareas S[N-1] que bloquean S[N]               │
│     ├── Intra-sprint: cadenas internas (ej: DB → BE → Services convergencia)   │
│     └── Gate entre sprints: CIERRE-S[N-1] → SETUP-S[N]                         │
│                                                                                 │
│     ▼                                                                           │
│  PJM: Determinar Deliveries (agrupación por módulo/rol)                         │
│     │                                                                           │
│     (REGLA: 1 Delivery por módulo por sprint. Naming: ROL-S[N]: Descripción)    │
│     │                                                                           │
│     ▼                                                                           │
│  PJM: Identificar milestone del sprint desde 3B.9.9 §11                         │
│     │                                                                           │
│     >> Checklist de análisis completado <<                                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                 FASE 3: GENERACIÓN DE DOCUMENTOS                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐     │
│  │ SUBFASE 3A: GENERAR SETUP_S[N].md                                     │     │
│  │                                                                        │     │
│  │ PJM: Generar script Python con pasos secuenciales:                    │     │
│  │  1. Crear/verificar Release R1 (solo si es S1, si no ya existe)       │     │
│  │  2. Crear Sprint S[N] en VTT (POST /releases/{id}/sprints)           │     │
│  │  3. Crear tarea SETUP-S[N]                                            │     │
│  │  4. Crear Deliveries (POST /deliveries)                               │     │
│  │  5. Vincular Deliveries al Sprint (PATCH /deliveries/{id} {sprintId}) │     │
│  │  6. Crear tareas por rol (POST /phases/{id}/tasks) — 1 bloque por rol │     │
│  │  7. Crear tareas validación + CIERRE + APR                            │     │
│  │  8. Asociar tareas a Deliveries (POST /deliveries/{id}/tasks/{tid})   │     │
│  │  9. Registrar dependencias (POST /tasks/{id}/dependencies)            │     │
│  │  10. Template CONTEXTO_S[N].md                                        │     │
│  │  11. Checklist de verificación                                        │     │
│  │                                                                        │     │
│  │ (REGLA: Cada tarea tiene campo "Registrar:" para que TL anote el ID)  │     │
│  │ (REGLA: NO auto-completar SETUP — TL lo cierra tras verificar)        │     │
│  │ (REGLA: VERY HIGH → mapear a HIGH en API — campo no acepta VERY HIGH) │     │
│  │                                                                        │     │
│  │ >> SETUP_S[N].md <<                                                   │     │
│  └────────────────────────────────────────────────────────────────────────┘     │
│     │                                                                           │
│     ▼                                                                           │
│  ┌────────────────────────────────────────────────────────────────────────┐     │
│  │ SUBFASE 3B: GENERAR HANDOFF_TL_S[N].md                                │     │
│  │                                                                        │     │
│  │ PJM: Generar documento con 11 secciones (Template v2.1):             │     │
│  │  §0  Resumen ejecutivo (horas, distribución, milestone)               │     │
│  │      + Nota si no hay FE/DL/QA en el sprint                          │     │
│  │  §1  Arquitectura (diagrama ASCII, ADRs nuevos/previos, deps ext.)   │     │
│  │  §2  Briefs por agente (DB/BE/FE/DO según roles del sprint)          │     │
│  │      Cada brief: tabla tareas, docs referencia, CAs verificables     │     │
│  │      + Archivos a crear (estructura de carpetas)                      │     │
│  │  §3  Variables de entorno                                             │     │
│  │  §4  Riesgos y mitigaciones (del 3B.9.6 filtrados por sprint)        │     │
│  │  §5  Tareas del sprint (tabla: ID, tarea, agente, horas, complex.)   │     │
│  │  §6  Dependencias entre tareas (tabla FS con notas)                   │     │
│  │  §7  VTT Planning Data (con columna deliveryId)                       │     │
│  │  §8  Documentos dinámicos a actualizar                                │     │
│  │  §9  DoD — TL (checklist binario + gate milestone)                   │     │
│  │  §10 Gates de aprobación (condiciones para que cada rol arranque)    │     │
│  │  §11 Referencias                                                      │     │
│  │                                                                        │     │
│  │ (REGLA: CAs son verificables — no "funciona" sino "X retorna Y")     │     │
│  │ (REGLA: §7 incluye deliveryId — sin esto, SETUP no puede asociar)    │     │
│  │ (REGLA: Brief FE diferido si hay gate DL — nota en §2)               │     │
│  │                                                                        │     │
│  │ >> HANDOFF_TL_S[N].md <<                                              │     │
│  └────────────────────────────────────────────────────────────────────────┘     │
│     │                                                                           │
│     ▼                                                                           │
│  ┌────────────────────────────────────────────────────────────────────────┐     │
│  │ SUBFASE 3C: GENERAR CLOSURE_S[N].md                                   │     │
│  │                                                                        │     │
│  │ PJM: Generar template de evidencia con secciones:                     │     │
│  │  §0  Qué es (para el PM), cuántas firmas, condición de cierre        │     │
│  │  §1  Resumen (métricas esperadas, deliveries VTT)                    │     │
│  │  §2  Verificación de deliverables (tabla ⬜ por delivery, por CA)     │     │
│  │  §3  Firma TL — Code Review (criterios + comando API stage dev)      │     │
│  │  §4  Firma AR — Integration Audit (criterios + comando API stage)    │     │
│  │  §5  Firma DL — Visual Review (solo si FE en sprint + comando API)   │     │
│  │  §6  Milestone M[N] — Verificación (criterios GO/NO-GO)              │     │
│  │  §7  Métricas finales (estimado vs real vs varianza)                  │     │
│  │  §8  Gate final — PM sign-off (checklist de condiciones)              │     │
│  │  §9  Proceso de cierre (tabla de firmas secuenciales + APR en VTT)   │     │
│  │  §10 Firmas de cierre (tabla ⬜ con fecha)                            │     │
│  │  §11 Referencias                                                      │     │
│  │                                                                        │     │
│  │ (REGLA: Firmas incluyen comando API real — no solo checklist en papel)│     │
│  │ (REGLA: APR-S[N] es tarea formal en VTT — no solo texto)             │     │
│  │ (REGLA: Si no hay FE → no hay firma DL → justificar en §0)           │     │
│  │                                                                        │     │
│  │ >> CLOSURE_S[N].md <<                                                 │     │
│  └────────────────────────────────────────────────────────────────────────┘     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                 FASE 4: REVIEW Y CORRECCIÓN                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  PJM: Entregar 3 documentos al PM/SA                                            │
│     │                                                                           │
│     ▼                                                                           │
│  SA: Revisar contra las 4 metodologías base                                     │
│     │                                                                           │
│     ├── >> METODOLOGIA_SETUP_FASE << — ¿Release, Sprint, Deliveries, Task→Del? │
│     ├── >> METODOLOGIA_SETUP_PLAN_VTT << — ¿Grafo sin huérfanos ni hojas?      │
│     ├── >> METODOLOGIA_EJECUCION_SPRINTS << — ¿6 secciones obligatorias?       │
│     └── >> METODOLOGIA_CIERRE_SPRINT_FASE << — ¿Firmas API, APR formal?        │
│                                                                                 │
│     ▼                                                                           │
│  ◆ ¿Aprobado sin correcciones?                                                  │
│     │                                                                           │
│     ├── SÍ → continuar a Fase 5                                                │
│     │                                                                           │
│     └── NO → SA: Emitir lista de correcciones con bloques de código             │
│               │                                                                 │
│               ▼                                                                 │
│          PJM: Aplicar correcciones a los 3 documentos                           │
│               │                                                                 │
│               ▼                                                                 │
│          PJM: Re-entregar documentos corregidos (v2.0+)                         │
│               │                                                                 │
│               └── (volver a review SA)                                          │
│                                                                                 │
│  (REGLA: No entregar al TL sin aprobación SA. El error se propaga a 7 sprints) │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                 FASE 5: ENTREGA                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  PJM: Presentar 3 archivos al PM                                                │
│     │                                                                           │
│     ├── >> SETUP_S[N].md <<                                                     │
│     ├── >> HANDOFF_TL_S[N].md <<                                                │
│     └── >> CLOSURE_S[N].md <<                                                   │
│                                                                                 │
│     ▼                                                                           │
│  ◆ ¿PM confirma continuar con siguiente sprint?                                 │
│     │                                                                           │
│     ├── SÍ → [START] con S[N+1] (volver a Fase 1)                              │
│     └── NO (último sprint de la fase) → [END]                                   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Diagrama de Flujo — Subfase 3A: Generación del SETUP

```
[START: Análisis completado]
    │
    ▼
◆ ¿Es el primer sprint (S1)?
    │
    ├── SÍ → PJM: Generar bloque "Crear/verificar Release R1"
    │         (POST /projects/{id}/releases)
    │
    └── NO → PJM: Generar bloque "Recuperar RELEASE_ID de CONTEXTO_S[N-1]"
    │
    ▼
PJM: Generar bloque "Crear Sprint S[N]"
    (POST /releases/{id}/sprints — con number, name, goal, startDate, endDate)
    │
    ▼
PJM: Generar bloque "Crear tarea SETUP-S[N]"
    │
    ▼
PJM: Determinar cantidad de Deliveries
    │
    (REGLA: 1 por módulo/rol activo + 1 REV para validación)
    │
    ▼
PJM: Generar bloque "Crear Deliveries"
    (POST /deliveries — con phaseId, name, order)
    │
    ▼
PJM: Generar bloque "Vincular Deliveries al Sprint"
    (PATCH /deliveries/{id} { sprintId })
    │
    (NOTA: Sin este paso, las tareas quedan sin sprint visible)
    │
    ▼
PJM: Generar bloques de creación de tareas (1 bloque por rol)
    │
    ├── Para cada tarea:
    │   ├── title: "[ID_CATALOGO] Nombre"
    │   ├── description: deliverable + sprint + rol + horas + complejidad + deps
    │   ├── assigneeId: UUID del rol
    │   ├── estimatedHours, priorityId, complexity, category
    │   └── Campo "Registrar:" para que TL anote el UUID devuelto
    │
    ▼
PJM: Generar bloque "Tareas de validación"
    ├── TL-S[N]-REV (Code Review)
    ├── AR-S[N] (Integration Audit)
    ├── DL-S[N]-REV (Visual Review — solo si FE en sprint)
    ├── CIERRE-S[N]
    └── APR-S[N] (Aprobación PM — tarea formal)
    │
    ▼
PJM: Generar bloque "Asociar tareas a Deliveries"
    (POST /deliveries/{id}/tasks/{taskId})
    │
    (REGLA: Cada tarea debe estar en exactamente 1 Delivery)
    │
    ▼
PJM: Generar bloque "Registrar dependencias"
    │
    ├── Cross-sprint: SETUP-S[N] ← CIERRE-S[N-1]
    ├── Cross-sprint: tareas S[N] ← tareas completadas de S[N-1]
    ├── Intra-sprint: cadenas por rol (ej: DB → BE convergencia)
    └── Validación: deliverables → TL Review → AR → (DL) → CIERRE → APR
    │
    ▼
PJM: Generar template CONTEXTO_S[N].md
    │
    ▼
PJM: Generar checklist de verificación
    │
    ▼
[END: SETUP_S[N].md completo]
```

---

## 7. Reglas de Negocio Críticas

| # | Regla | Consecuencia si se viola |
|:-:|-------|-------------------------|
| R1 | No generar sin todos los inputs | Documentos con datos inventados — SA rechaza |
| R2 | Release → Sprint → Delivery → Task (jerarquía obligatoria) | Tareas huérfanas sin sprint visible, métricas MGP no funcionan |
| R3 | Vincular Delivery al Sprint vía PATCH (no existe Task.sprintId) | Tareas no aparecen en dashboard de sprint |
| R4 | Cada tarea asociada a exactamente 1 Delivery | Tarea duplicada en métricas o invisible |
| R5 | CIERRE-S[N-1] → SETUP-S[N] (gate entre sprints secuenciales) | Sprint N puede iniciar sin que N-1 haya cerrado |
| R6 | VERY HIGH → mapear a HIGH en campo `complexity` | Error de validación de API al crear tarea |
| R7 | No auto-completar SETUP — TL lo cierra tras verificar | SETUP queda completado sin que el TL haya verificado |
| R8 | APR-S[N] como tarea formal en VTT (no solo texto) | Sprint no tiene gate formal de aprobación PM |
| R9 | Firmas con comando API real (POST /sprints/{id}/stages/.../sign) | Cierre queda como checklist en papel, sin registro en sistema |
| R10 | §7 VTT Planning Data incluye columna deliveryId | SETUP no puede asociar tareas a Deliveries |
| R11 | Si sprint tiene FE → agregar firma DL + DL-S[N]-REV | FE foundation sin review visual, bugs de design system |
| R12 | CAs verificables: no "funciona" sino "X retorna Y cuando Z" | Criterios ambiguos — reviewer no sabe qué verificar |

---

## 8. Checklist de Completitud por Documento

### 8.1 SETUP_S[N].md

- [ ] Release R1 verificado/creado (solo S1)
- [ ] Sprint S[N] creado con number, name, goal, dates
- [ ] Deliveries creados (1 por módulo/rol)
- [ ] Deliveries vinculados al Sprint (PATCH con sprintId)
- [ ] Tareas creadas con los 6 campos obligatorios (title, description, assigneeId, estimatedHours, priorityId, complexity, category)
- [ ] Tareas de validación + CIERRE + APR creadas
- [ ] Todas las tareas asociadas a Deliveries
- [ ] Dependencias registradas (cross-sprint + intra-sprint)
- [ ] Template CONTEXTO generado
- [ ] Checklist de verificación incluido
- [ ] No se auto-completa el SETUP

### 8.2 HANDOFF_TL_S[N].md

- [ ] §0 con nota de roles ausentes (si no hay FE/DL/QA)
- [ ] §1 Diagrama de componentes con Deliveries referenciados
- [ ] §2 Brief por agente con CAs verificables + archivos a crear
- [ ] §3 Variables de entorno (nuevas o referencia a sprint anterior)
- [ ] §4 Riesgos filtrados del 3B.9.6
- [ ] §5 Tabla completa de tareas
- [ ] §6 Dependencias con tipo FS
- [ ] §7 VTT Planning Data con columna deliveryId
- [ ] §8 Documentos dinámicos
- [ ] §9 DoD con gate milestone verificable
- [ ] §10 Gates de aprobación con condiciones concretas
- [ ] §11 Referencias a documentos 3B

### 8.3 CLOSURE_S[N].md

- [ ] §0 con número de firmas y justificación si <4
- [ ] §2 Verificación por Delivery (no por tarea suelta)
- [ ] §3 Firma TL con criterios + comando API stage development
- [ ] §4 Firma AR con criterios + comando API stage integration
- [ ] §5 Firma DL con criterios + comando API stage design (si FE)
- [ ] §6 Milestone con criterios GO/NO-GO del 3B.9.9
- [ ] §7 Métricas estimado vs real
- [ ] §8 Gate final con checklist de condiciones
- [ ] §9 Proceso de firmas secuencial + APR como tarea VTT
- [ ] §10 Tabla de firmas con fecha

---

## 9. Excepciones y Caminos Alternativos

### 9.1 Documento de input faltante

```
PJM detecta que falta un input (ej: 3B.9.3 no subido)
    → PJM solicita al PM el documento específico con nombre exacto
    → PJM NO genera nada hasta recibir el documento
    → PM sube el documento
    → PJM retoma desde Fase 1
```

### 9.2 SA rechaza con correcciones

```
SA emite lista de correcciones con bloques de código
    → PJM lee cada corrección
    → PJM regenera los documentos afectados (versión N+1)
    → PJM re-entrega al SA
    → SA re-revisa
    → Si aprobado → Fase 5
    → Si no → otro ciclo de corrección
```

### 9.3 Sprint tiene roles que no aparecieron en sprints anteriores

```
PJM detecta rol nuevo (ej: QA aparece por primera vez en S5)
    → Agregar Delivery para el nuevo rol
    → Agregar firma de cierre si corresponde (QA → firma QA en CLOSURE)
    → Agregar brief en HANDOFF
    → Documentar en §0 del HANDOFF que este rol es nuevo
```

### 9.4 Deliverables ⚪ (opcionales)

```
PJM encuentra deliverable marcado ⚪ en 3B.9.3
    → Crear tarea en VTT con priorityId = MEDIUM
    → Agregar "[OPCIONAL R1 — implementar si hay tiempo/presupuesto]" en description
    → Incluir en el sprint normalmente (no excluir)
```

---

## 10. Métricas del Proceso

| Métrica | Target | Cómo medir |
|---------|--------|------------|
| Tiempo de generación del trío | ≤30 min por sprint | Desde inicio de Fase 3 hasta entrega |
| Ciclos de corrección SA | ≤1 (idealmente 0) | Cantidad de veces que SA devuelve |
| Completitud del checklist §8 | 100% (todos los ítems ✅) | Auto-verificación antes de entregar |
| Documentos faltantes solicitados | ≤1 por sprint | Veces que PJM pide inputs al PM |

---

**Documento:** SOP_GENERACION_SPRINT_DOCS.md
**Versión:** 1.0
**Fecha:** 2026-05-12
**Autor:** PJM
