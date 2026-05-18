# CONTEXTO TL — Estado de Sesión Persistente

> **PLANTILLA** — Copiar a `[REPO]/knowledge/agent-tasks/CONTEXTO_TL_SESION.md` y rellenar con datos reales.
> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** [YYYY-MM-DD]

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | [NOMBRE_AGENTE] (Tech Lead) |
| UUID | `[UUID_AGENTE]` |
| Email | `[EMAIL_AGENTE]` |
| API | `[BASE_URL]` |
| Proyecto ID | `[PROJECT_ID_UUID]` |
| Fase activa ID | `[UUID_FASE_ACTIVA]` |

---

## Sprint Activo

**Sprint [NN] — [Nombre del Sprint]**

[Breve descripción del bloque/fase actual y qué se está trabajando]

---

## Estado de Tareas TL — Sprint [NN]

| Tarea | Título | Estado | Agente asignado | Notas |
|-------|--------|--------|-----------------|-------|
| [TASK-ID] | [título] | [⏳ pending / 🔵 in_progress / 🟡 in_review / ✅ completed / 🔴 blocked] | [nombre] | [notas] |

---

## Tareas en in_review pendientes de mi Code Review

| Tarea | Agente | Días en in_review | Acción |
|-------|--------|-------------------|--------|
| [TASK-ID] | [nombre] | [N] | [pendiente revisión / rechazada / aprobada] |

---

## Blockers Activos

| Tarea | Blocker | Días abierto | Quien debe resolver |
|-------|---------|--------------|---------------------|
| [TASK-ID] | [descripción] | [N] | [rol] |

---

## Decisiones Técnicas Tomadas (este sprint)

- [YYYY-MM-DD] [decisión 1]: [contexto breve]
- [YYYY-MM-DD] [decisión 2]: [contexto breve]

---

## Siguiente Acción

**PRIORIDAD INMEDIATA:** [qué debo hacer en la siguiente sesión]

1. [Acción 1]
2. [Acción 2]
3. [Acción 3]

**Cadena de desbloqueo:**
```
[TASK-A] ✅ → [TASK-B] ✅ → [TASK-C] se desbloquea → [TASK-D]
```

---

## Handoff de Referencia (el que estoy ejecutando)

- [ruta al HANDOFF_TL_S[NN].md]

---

## Dependencias con Otros Roles

| Esperando de | Qué | Desde |
|--------------|-----|-------|
| PM | [qué espera] | [YYYY-MM-DD] |
| DL | [qué espera] | [YYYY-MM-DD] |
| PJM | [qué espera] | [YYYY-MM-DD] |

---

## Notas y Pendientes

- [nota o pendiente 1]
- [nota o pendiente 2]

---

## Cómo Actualizar Este Archivo

Al terminar sesión, actualizar:

1. Estado de tareas (tabla principal)
2. Sección "Siguiente Acción"
3. Decisiones técnicas nuevas (si hay)
4. Blockers activos (cuáles se resolvieron, cuáles nuevos)
5. Fecha de última actualización (línea 5)

---

**PLANTILLA.** Creada a partir de `Project_setup/templates/CONTEXTO_TL_SESION_TEMPLATE.md`.
