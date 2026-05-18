# TEMPLATE — TASK INDEX SEED

> **Cómo usar este template:**
> 1. Copiar a `01-PM/TASK_INDEX_SEED_<<PROYECTO>>.md`
> 2. Completar §2 con UUIDs reales del proyecto (users, catálogos VTT)
> 3. Llenar §4 con todas las tareas y sus descripciones (150-2000 chars)
> 4. Validar gates del `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` §PASO 7
> 5. Borrar este bloque antes de emitir

---

# TASK INDEX SEED — <<NOMBRE_PROYECTO>>

| Campo | Valor |
|-------|-------|
| **Documento** | TASK_INDEX_SEED_<<PROYECTO>>.md |
| **Versión** | 1.0 |
| **Fecha** | <<YYYY-MM-DD>> |
| **Autor** | PM (<<Nombre>>) |
| **Propósito** | Plan de CREACIÓN desde cero en VTT. Todos los campos requeridos por el sistema VTT para carga en una sola pasada. |
| **Audiencia** | PJM (ejecuta carga) · TL (review + asignaciones) |
| **Fuente endpoints** | `PROCESO_ASIGNACION_TAREAS.md` |
| **Estado** | ✅ Listo para ejecución |

---

## 1. ESTADO INICIAL EN VTT

| Entidad | Existe en VTT | Acción |
|---------|:-:|--------|
| Usuarios del proyecto | ✅ | Usar UUIDs del §2.3 |
| Catálogo Status | ✅ | Usar UUIDs del §2.1 |
| Catálogo Priority | ✅ | Usar UUIDs del §2.2 |
| Project "<<NOMBRE>>" | ❌ | **Crear** con POST |
| <<N>> Phases | ❌ | **Crear** con POST |
| <<N>> Deliveries | ❌ | **Crear** con POST |
| <<N>> Tasks | ❌ | **Crear** con POST |
| <<N>> Dependencies | ❌ | **Crear** con POST |

---

## 2. REFERENCE UUIDs (globales)

### 2.1 Status UUIDs

| Code | UUID |
|------|------|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

### 2.2 Priority UUIDs

| Code | UUID | Ref |
|------|------|-----|
| critical | `90ec3df2-fac4-40fa-b2ce-29daf0f4956e` | **[C]** |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` | **[H]** |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` | **[M]** |
| low | `95f2e731-41b9-4a7d-9a43-31f00a4ddd7e` | **[L]** |

### 2.3 Mapeo de roles → Usuarios VTT

> Completar con UUIDs reales de `.claude/rules/Proyect_data.md` o equivalente.

| Rol | UUID | Email |
|-----|------|-------|
| PM | `<<UUID>>` | <<email>> |
| PJM | `<<UUID>>` | <<email>> |
| TL | `<<UUID>>` | <<email>> |
| SA | `<<UUID>>` | <<email>> |
| AR | `<<UUID>>` | <<email>> |
| BE | `<<UUID>>` | <<email>> |
| DB | `<<UUID>>` | <<email>> |
| FE | `<<UUID>>` | <<email>> |
| UX | `<<UUID>>` | <<email>> |
| DL | `<<UUID>>` | <<email>> |
| QA | `<<UUID>>` | <<email>> |
| DO | `<<UUID>>` | <<email>> |

### 2.4 Categorías válidas (POST task)

| Código | Uso |
|--------|-----|
| `development` | Código (backend, frontend, DB) |
| `design` | Wireframes, mockups, design system |
| `testing` | Test planning, QA execution |
| `documentation` | Docs de todas las fases de planeación y diseño |
| `deployment` | Docker, CI/CD, deploy |
| `chore` | Setup, tooling, infra |
| `bugfix` | Correcciones post-review |
| `review` | Code/design reviews |

### 2.5 Complexity (MAYÚSCULAS — obligatorio)

`LOW` · `MEDIUM` · `HIGH`

### 2.6 Campos correctos de POST task (VTT-506 lessons)

```json
{
  "title": "string",
  "description": "string (max 2000 chars)",
  "priorityId": "UUID",
  "statusId": "UUID",
  "assignedToId": "UUID",
  "assignedBy": "UUID",
  "category": "development | design | testing | documentation | deployment | chore | bugfix | review",
  "complexity": "LOW | MEDIUM | HIGH",
  "createdBy": "UUID"
}
```

**Errores frecuentes a evitar:**
- `assignedTo` → se ignora · usar `assignedToId`
- `priority_id` → rechazado · usar camelCase `priorityId`
- `complexity: "medium"` → rechazado · MAYÚSCULAS
- `description > 2000 chars` → 400 `too_big`

---

## 3. PLAN DE CREACIÓN EN VTT (secuencia de 6 pasos)

### Paso 1 · Crear Project (simple, sin wizard)

```bash
POST <<API_URL>>/api/projects
{
  "name": "<<NOMBRE>>",
  "code": "<<CODIGO>>",
  "description": "<<descripción 500-2000 chars>>",
  "projectTypeCode": "SOFTWARE",
  "createdBy": "<<UUID_PM>>"
}
```

### Paso 2 · Crear N Phases

```bash
POST <<API_URL>>/api/projects/{projectId}/phases
```

| # | Nombre | Order | Descripción |
|---|--------|------:|-------------|
| 1 | <<Fase 1>> | 1 | <<desc>> |
| ... | ... | ... | ... |

### Paso 3 · Crear N Deliveries

```bash
POST <<API_URL>>/api/deliveries
{
  "phaseId": "{phaseId}",
  "name": "<<nombre>>",
  "order": N,
  "createdBy": "<<UUID_PJM>>"
}
```

### Paso 4 · Crear N Tasks

```bash
POST <<API_URL>>/api/phases/{phaseId}/tasks
{
  "title": "<<título>>",
  "description": "<<descripción detallada>>",
  "priorityId": "<<UUID_priority>>",
  "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
  "assignedToId": "<<UUID_user>>",
  "assignedBy": "<<UUID_PJM>>",
  "category": "<<categoría>>",
  "complexity": "MEDIUM",
  "estimatedHours": N,
  "createdBy": "<<UUID_PJM>>"
}
```

### Paso 5 · Asignar Tasks a Deliveries

```bash
POST <<API_URL>>/api/deliveries/{deliveryId}/tasks/{taskId}
{"assignedBy": "<<UUID_PJM>>"}
```

### Paso 6 · Crear Dependencies críticas

```bash
POST <<API_URL>>/api/tasks/{taskId}/dependencies
{"dependsOnTaskId": "{otroTaskId}"}
```

---

## 4. ÍNDICE DE N TAREAS POR FASE

### 4.1 Fase 1 · <<Nombre>> (<<N>> tareas · <<N>>h)

**Deliveries en esta fase (<<N>>):**
- <<Delivery 1>>
- <<Delivery 2>>

| ID | Título | Rol | Cat | Cmplx | h | Pri | Delivery | Produces |
|----|--------|-----|-----|:------|--:|:---:|----------|----------|
| <<MEM-XXX>> | <<título>> | <<rol>> | <<cat>> | <<LOW/MEDIUM/HIGH>> | <<N>> | <<C/H/M/L>> | <<Delivery>> | <<0.X.Y, ...>> |

**Descripciones:**

- **<<MEM-XXX>> <<título>>:** <<descripción 150-300 chars explicando qué hace la tarea, qué entrega, contexto técnico relevante>>

### 4.2 Fase 2 · ...

<<repetir estructura para cada fase>>

---

## 5. DEPENDENCIAS CRÍTICAS (<<N>>)

| # | Task | Depende de | Razón | Impacto |
|---:|------|-----------|-------|---------|
| 1 | <<MEM-XXX>> | <<MEM-YYY>> | <<razón>> | Alto/Medio/Crítico |
| ... | ... | ... | ... | ... |

---

## 6. ANEXO: DESGLOSE INIT (si aplica)

Las INIT son desglose operativo de MEM-001..005. **NO se cargan como tareas separadas** en VTT.

### A. VTT Setup (dentro de MEM-003)
- INIT-A-01 ...

### B. Repo Setup (dentro de MEM-002)
### C. VM Configuration (dentro de MEM-001)
### D. Agent Team (dentro de MEM-003)
### E. Tooling (dentro de MEM-004)
### F. Documentation (dentro de MEM-005)
### G. Kickoff (dentro de MEM-005)

---

## 7. TOTALES VERIFICACIÓN

| Fase | Tareas | Horas | Rol principal |
|------|-------:|------:|---------------|
| 1 <<Nombre>> | <<N>> | <<N>> | <<roles>> |
| ... | ... | ... | ... |
| **TOTAL** | **<<N>>** | **<<N>>h** | **<<N>> roles** |

---

## 8. POST-EJECUCIÓN (output esperado)

Tras ejecutar el script (ver `create_<<proyecto>>_vtt.py`), se genera `VTT_UUIDS_<<PROYECTO>>.json`:

```json
{
  "projectId": "{nuevo-uuid}",
  "phases": {
    "<<Fase 1>>": "{uuid}",
    ...
  },
  "deliveries": {
    "<<Delivery 1>>": "{uuid}",
    ...
  },
  "tasks": {
    "<<MEM-001>>": "{uuid}",
    ...
  }
}
```

Este archivo es el **source of truth de UUIDs** post-creación.

---

**Documento:** TASK_INDEX_SEED_<<PROYECTO>>.md
**Versión:** 1.0
**Estado:** ✅ Listo para ejecución
**Fecha:** <<YYYY-MM-DD>>

**Usado por:**
- PJM: carga inicial al sistema VTT
- TL: review de asignaciones
- PM: validación de metadata antes de ejecución

---

**PM — <<Nombre>>**

---

**Template source:** `TEMPLATE_TASK_INDEX_SEED_V1.0.md`
**Proceso asociado:** `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` (paso 7)
