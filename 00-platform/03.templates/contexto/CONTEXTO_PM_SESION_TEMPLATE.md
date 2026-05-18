# CONTEXTO PM — Estado de Sesión Persistente

> **PLANTILLA** — Copiar a `[REPO]/knowledge/agent-tasks/CONTEXTO_PM_SESION.md` y rellenar con datos reales.
> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** [YYYY-MM-DD]

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | [NOMBRE_PM] (PM) |
| UUID | `[UUID_AGENTE]` |
| Email | `[EMAIL_PM]` |
| API | `[BASE_URL]` |
| Proyecto ID | `[PROJECT_ID_UUID]` |
| Fase activa ID | `[UUID_FASE_ACTIVA]` |

---

## Estado del Proyecto

**Fase actual:** [N — Nombre de la fase SDLC]
**Sprint activo:** [S[NN] — nombre]
**Release actual:** [MVP / V2.0 / etc.]

---

## Tareas Pendientes de MI Aprobación

### En `task_completed` esperando `task_approved`

| Tarea | TL aprobó | PR mergeado | Pendiente de |
|-------|-----------|-------------|--------------|
| [TASK-ID] | [fecha] | [sí/no] | [qué falta para aprobar] |

### PRs Abiertos Esperando Merge

| PR # | Tarea | TL revisó | Files Changed OK | Acción |
|------|-------|-----------|-------------------|--------|
| [#NN] | [TASK-ID] | [sí/no] | [sí/no] | [merge / review files changed / rechazar] |

---

## Handoffs Pendientes de Emitir

| Rol destino | Sprint/Feature | Estado | Fecha límite |
|-------------|-----------------|--------|--------------|
| TL | [nombre] | [pendiente / en redacción / emitido] | [YYYY-MM-DD] |
| DL | [nombre] | [pendiente / emitido] | [YYYY-MM-DD] |
| PJM | [nombre] | [pendiente / emitido] | [YYYY-MM-DD] |

---

## Escalaciones Recibidas (del PJM, TL, DL)

| De | Tipo | Descripción | Decisión tomada |
|----|------|-------------|-----------------|
| PJM | [blocker/riesgo] | [descripción] | [decisión o pendiente] |
| TL | [pregunta técnica/alcance] | [descripción] | [decisión o pendiente] |
| DL | [APR-DL/otro] | [descripción] | [aprobado/rechazado/pendiente] |

---

## Decisiones de Negocio Pendientes

| Decisión | Contexto | Información que necesito | Quién puede ayudar |
|----------|----------|---------------------------|---------------------|
| [descripción] | [contexto] | [qué info falta] | [TL/PJM/SA/Sponsor] |

---

## Alcance (in scope / out of scope)

### Sprint actual — In scope

- [Feature 1]
- [Feature 2]

### Sprint actual — Out of scope

- [No incluye 1]
- [No incluye 2]

### MVP Definition vigente

[Descripción breve del MVP y su estado]

---

## Reportes del PJM Recibidos

| Reporte | Fecha | Acción tomada |
|---------|-------|---------------|
| Sprint Report S[NN] | [YYYY-MM-DD] | [decisión] |
| Executive Report | [YYYY-MM-DD] | [decisión] |

---

## Gates por Aprobar

| Gate | Fase | Condición de aprobación | Estado |
|------|------|--------------------------|--------|
| APR-DL Sprint [NN] | 3A | QA Visual del DL + entregables completos | [pendiente / aprobado] |
| APR-PM Fase [N] | [N] | Entregables + gates de §15 de 08_FLUJO_PM | [pendiente / aprobado] |
| Go/No-Go Deploy | 6 | QA aprobado + rollback definido | [pendiente / aprobado] |

---

## Siguiente Acción

**PRIORIDAD INMEDIATA:**

1. [Acción 1 — ej: Aprobar APR-DL Sprint NN]
2. [Acción 2 — ej: Mergear PR #NN]
3. [Acción 3 — ej: Emitir handoff para Sprint NN+1]

---

## Riesgos Conocidos (decisión PM)

| Riesgo | Impacto | Decisión |
|--------|---------|----------|
| [descripción] | [alto/medio/bajo] | [asumir / mitigar / escalar] |

---

## Notas / Pendientes Estratégicos

- [nota o decisión estratégica pendiente]
- [alineamiento con sponsor pendiente]

---

## Cómo Actualizar Este Archivo

Al terminar sesión, actualizar:

1. Tareas aprobadas (remover de la lista)
2. PRs mergeados (remover)
3. Handoffs emitidos (marcar como emitidos)
4. Escalaciones resueltas (marcar decisión)
5. Gates aprobados (remover de pendientes)
6. Siguiente acción
7. Fecha de última actualización (línea 5)

---

**PLANTILLA.** Creada a partir de `Project_setup/templates/CONTEXTO_PM_SESION_TEMPLATE.md`.
