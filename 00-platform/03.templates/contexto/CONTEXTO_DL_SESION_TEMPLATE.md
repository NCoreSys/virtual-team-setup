# CONTEXTO DL — Estado de Sesión Persistente

> **PLANTILLA** — Copiar a `[REPO]/knowledge/agent-tasks/CONTEXTO_DL_SESION.md` y rellenar con datos reales.
> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** [YYYY-MM-DD]

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | [NOMBRE_AGENTE] (Design Lead) |
| UUID | `[UUID_AGENTE]` |
| Email | `[EMAIL_AGENTE]` |
| API | `[BASE_URL]` |
| Proyecto ID | `[PROJECT_ID_UUID]` |
| Fase activa ID | `[UUID_FASE_ACTIVA]` |

---

## Sprint Activo

**Sprint [NN] — [Nombre del Sprint]**

[Breve descripción del bloque de diseño que estoy coordinando]

---

## Estado de Tareas DL — Sprint [NN]

| Tarea | Título | Estado | Notas |
|-------|--------|--------|-------|
| [TASK-ID] | DL-S[NN]-01: [nombre pantalla] | [✅ completed / ⏳ pending / 🔴 blocked] | [notas] |

---

## HTMLs Disponibles en `[REPO]/knowledge/design/sprint_[NN]/`

| Archivo | Sprint | Estado DL |
|---------|--------|-----------|
| [nombre].html | [TASK-ID] | [✅ Aprobado / ⏳ Pendiente QA Visual / 🔴 Rechazado] |

---

## Tareas UX en in_review pendientes de QA Visual

| Tarea UX | Agente | Pantalla | Acción |
|----------|--------|----------|--------|
| [TASK-ID] | [UX-Agent] | [nombre] | [QA pendiente / aprobada / rechazada] |

---

## Handoff a FE (post APR-DL)

| Tarea FE | UX Spec creado | Entregado al FE |
|----------|----------------|-----------------|
| [TASK-ID] | [sí/no] | [fecha o pendiente] |

---

## Decisiones de Design System Tomadas

- Tokens base: `[REPO]/frontend/src/index.css`
- [Decisión 1]: [contexto]
- [Decisión 2]: [contexto]
- Tokens nuevos este sprint: `[REPO]/knowledge/design/sprint_[NN]/tokens/s[NN]_tokens.json`
- Breakpoints: desktop, tablet (768px), mobile (375px)

---

## Siguiente Acción

**PRIORIDAD INMEDIATA:** [TASK-ID]

1. [Acción 1]
2. [Acción 2]
3. [Acción 3]

**Cadena de desbloqueo:**
```
[TASK-A] ✅ → [TASK-B] ✅ → [TASK-C] se desbloquea → APR-DL → FE puede arrancar
```

---

## Handoff de Referencia

- `[REPO]/[ruta al HANDOFF_DL_S[NN].md]`

---

## Dependencias con Otros Roles

| Esperando de | Qué | Desde |
|--------------|-----|-------|
| PM | APR-DL | [YYYY-MM-DD] |
| TL | [qué] | [YYYY-MM-DD] |
| UX | [qué] | [YYYY-MM-DD] |

---

## Notas y Pendientes

- [nota o pendiente 1]
- [nota o pendiente 2]

---

## Cómo Actualizar Este Archivo

Al terminar sesión, actualizar:

1. Estado de tareas (columna Estado)
2. Sección "Siguiente Acción"
3. Cualquier decisión DS nueva
4. HTMLs entregados por el UX
5. Fecha de última actualización (línea 5)

---

**PLANTILLA.** Creada a partir de `Project_setup/templates/CONTEXTO_DL_SESION_TEMPLATE.md`.
