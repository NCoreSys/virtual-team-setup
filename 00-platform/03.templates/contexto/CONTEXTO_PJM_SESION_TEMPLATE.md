# CONTEXTO PJM — Estado de Sesión Persistente

> **PLANTILLA** — Copiar a `[REPO]/knowledge/agent-tasks/CONTEXTO_PJM_SESION.md` y rellenar con datos reales.
> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** [YYYY-MM-DD]

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | [NOMBRE_AGENTE] (Project Manager) |
| UUID | `[UUID_AGENTE]` |
| Email | `[EMAIL_AGENTE]` |
| API | `[BASE_URL]` |
| Proyecto ID | `[PROJECT_ID_UUID]` |
| Fase activa ID | `[UUID_FASE_ACTIVA]` |

---

## Sprint Activo

**Sprint [NN] — [Nombre del Sprint]**
**Plan original:** [X tareas / Y horas / Z días]
**Baseline de velocity:** [tareas/día]

---

## Snapshot Último (fecha: [YYYY-MM-DD])

### Distribución por status

| Status | Cantidad | % |
|--------|----------|---|
| task_pending | [N] | [%] |
| task_in_progress | [N] | [%] |
| task_in_review | [N] | [%] |
| task_completed | [N] | [%] |
| task_approved | [N] | [%] |
| task_on_hold | [N] | [%] |
| task_blocked | [N] | [%] |

### KPIs

| Indicador | Valor actual | Umbral | Estado |
|-----------|--------------|--------|--------|
| % completion del sprint | [%] | — | [🟢/🟡/🔴] |
| Velocity | [tareas/día] | baseline: [X] | [🟢/🟡/🔴] |
| Días promedio en in_review | [N] | ≤2 | [🟢/🟡/🔴] |
| Blockers activos | [N] | ≤2 | [🟢/🟡/🔴] |
| Tareas sin asignar | [N] | 0 | [🟢/🟡/🔴] |
| Issues críticos sin resolver | [N] | 0 | [🟢/🟡/🔴] |

---

## Blockers Activos

| Tarea | Agente bloqueado | Blocker | Días abierto | Escalado al PM | Quién debe resolver |
|-------|-------------------|---------|--------------|-----------------|---------------------|
| [TASK-ID] | [nombre] | [descripción] | [N] | [sí/no] | [rol] |

---

## Tareas Atascadas (>48h en in_review)

| Tarea | Agente | En status desde | Revisor esperado |
|-------|--------|-----------------|------------------|
| [TASK-ID] | [nombre] | [fecha] | TL |

---

## Riesgos Identificados

| Riesgo | Impacto | Probabilidad | Mitigación propuesta |
|--------|---------|--------------|-----------------------|
| [descripción] | [A/M/B] | [A/M/B] | [acción sugerida] |

---

## Reportes Generados

| Reporte | Fecha | Ruta |
|---------|-------|------|
| Sprint Report | [YYYY-MM-DD] | `[REPO]/knowledge/reports/YYYY-MM-DD_sprint-report-S[NN].md` |
| Executive Report | [YYYY-MM-DD] | `[REPO]/knowledge/reports/YYYY-MM-DD_executive.md` |

---

## Siguiente Acción

**PRIORIDAD INMEDIATA:**

1. [Acción 1]
2. [Acción 2]

---

## Escalaciones Pendientes al PM

| Tipo | Descripción | Urgencia | Reportado |
|------|-------------|----------|-----------|
| [blocker/riesgo/milestone] | [descripción] | [alta/media/baja] | [YYYY-MM-DD] |

---

## Handoff de Referencia (sprint actual)

- `[REPO]/[ruta al HANDOFF_PJM_S[NN].md]`

---

## Dependencias Cruzadas (de qué depende este sprint)

| Espera de | Tarea/Entregable | Desde |
|-----------|-------------------|-------|
| [rol] | [qué] | [YYYY-MM-DD] |

---

## Lecciones Aprendidas (este sprint)

- [LL-xxx]: [descripción]

---

## Cómo Actualizar Este Archivo

Al terminar sesión, actualizar:

1. Snapshot (distribución de tareas + KPIs)
2. Blockers activos (resueltos quitar, nuevos agregar)
3. Reportes generados (si hay)
4. Escalaciones pendientes
5. Fecha de última actualización (línea 5)

---

**PLANTILLA.** Creada a partir de `Project_setup/templates/CONTEXTO_PJM_SESION_TEMPLATE.md`.
