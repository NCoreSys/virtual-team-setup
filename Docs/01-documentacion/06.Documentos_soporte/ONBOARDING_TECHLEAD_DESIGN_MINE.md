# Onboarding Tech Lead - Proyecto Design Mine

**Fecha**: 2026-02-13
**Para**: Tech Lead del proyecto Design Mine
**De**: Backend API Specialist (VTT)

---

## 1. Tu Equipo - IDs de Usuarios

Estos son los usuarios registrados en el sistema para tu proyecto:

| Rol | Nombre | UUID |
|-----|--------|------|
| **Tech Lead** | Design Mine Tech Lead | `05ce9f37-0e6a-41da-bff9-0eab37bc3e9f` |
| **Backend API Specialist** | Design Mine Backend | `e79afbd1-b284-4a44-8597-ff1480f5fd2d` |
| **Frontend Dev #1** | Design Mine Frontend 1 | `4fd083ee-3d88-4a64-8cec-24de44e3a06d` |
| **Frontend Dev #2** | Design Mine Frontend 2 | `ac2f014b-3d25-40fd-aca7-a4661d5469a8` |
| **Database Engineer** | Design Mine DB Engineer | `cc21a565-d40a-4b7c-ae21-f9a7551432bc` |
| **DevOps Engineer** | Design Mine DevOps | `4467a1f0-3312-4143-9d29-a2fcb17a0780` |
| **Design Lead** | Design Mine Design Lead | `8aa456a8-818b-4a3f-ad48-8f8cb0a7f15c` |
| **System** | Design Mine System | `20e792ea-8903-454b-81a8-846cbf4eb666` |

---

## 2. Configuracion Base

```
BASE_URL = http://77.42.88.106:3000
SWAGGER = http://77.42.88.106:3000/api-docs
```

> NUNCA usar `localhost`. Siempre usar la IP del servidor.

---

## 3. Paso 0: Obtener Catalogos

**Antes de crear cualquier cosa**, obtener los UUIDs dinamicos del sistema:

```bash
# Status de tareas
curl -s "http://77.42.88.106:3000/api/catalogs/status?process=task" | jq .

# Status de proyectos
curl -s "http://77.42.88.106:3000/api/catalogs/status?process=project" | jq .

# Status de fases
curl -s "http://77.42.88.106:3000/api/catalogs/status?process=phase" | jq .

# Prioridades
curl -s "http://77.42.88.106:3000/api/catalogs/priorities" | jq .

# Verificar usuarios
curl -s "http://77.42.88.106:3000/api/users" | jq .
```

> Guarda los UUIDs de status y prioridades. Los necesitaras para crear tareas.

---

## 4. Paso 1: Crear el Proyecto

```bash
curl -s -X POST http://77.42.88.106:3000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Design Mine",
    "description": "Descripcion del proyecto Design Mine",
    "key": "DM"
  }' | jq .
```

**Campos:**

| Campo | Tipo | Requerido | Descripcion |
|-------|------|-----------|-------------|
| `name` | string | Si | Nombre del proyecto |
| `description` | string | No | Descripcion del proyecto |
| `key` | string (2-6 chars, UPPERCASE) | No | Clave del proyecto (ej: "DM"). Si no se envia, se genera automaticamente |
| `statusId` | UUID | No | Status inicial. Por defecto se asigna el primer status de project |

**Response exitosa (201):**
```json
{
  "data": {
    "id": "uuid-del-proyecto",
    "name": "Design Mine",
    "key": "DM",
    "description": "...",
    "statusId": "...",
    "createdAt": "...",
    "updatedAt": "..."
  }
}
```

> **IMPORTANTE**: Guarda el `id` del proyecto, lo necesitas para crear fases.

### Verificar proyecto creado

```bash
curl -s "http://77.42.88.106:3000/api/projects" | jq .
```

---

## 5. Paso 2: Crear Fases

Las fases organizan el trabajo dentro del proyecto. Cada fase contiene tareas.

```bash
curl -s -X POST http://77.42.88.106:3000/api/projects/{PROJECT_ID}/phases \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fase 1 - Setup Inicial",
    "description": "Configuracion del entorno y estructura base del proyecto"
  }' | jq .
```

**Campos:**

| Campo | Tipo | Requerido | Descripcion |
|-------|------|-----------|-------------|
| `name` | string | Si | Nombre de la fase |
| `description` | string | No | Descripcion de la fase |
| `order` | number (int positivo) | No | Orden de la fase. Si no se envia, se calcula automaticamente |

**Response exitosa (201):**
```json
{
  "data": {
    "id": "uuid-de-la-fase",
    "name": "Fase 1 - Setup Inicial",
    "description": "...",
    "order": 1,
    "projectId": "...",
    "statusId": "...",
    "createdAt": "..."
  }
}
```

> **IMPORTANTE**: Guarda el `id` de cada fase para crear tareas dentro de ella.

### Ejemplo: Crear varias fases

```bash
# Fase 1
curl -s -X POST http://77.42.88.106:3000/api/projects/{PROJECT_ID}/phases \
  -H "Content-Type: application/json" \
  -d '{"name": "Fase 1 - Setup y Base de Datos", "description": "Schema inicial, migraciones, seed data"}'

# Fase 2
curl -s -X POST http://77.42.88.106:3000/api/projects/{PROJECT_ID}/phases \
  -H "Content-Type: application/json" \
  -d '{"name": "Fase 2 - Backend Core", "description": "APIs CRUD principales"}'

# Fase 3
curl -s -X POST http://77.42.88.106:3000/api/projects/{PROJECT_ID}/phases \
  -H "Content-Type: application/json" \
  -d '{"name": "Fase 3 - Frontend Core", "description": "Interfaz de usuario principal"}'
```

### Consultar fases de un proyecto

```bash
curl -s "http://77.42.88.106:3000/api/projects/{PROJECT_ID}/phases" | jq .
```

---

## 6. Paso 3: Crear Tareas

Las tareas se crean dentro de una fase.

```bash
curl -s -X POST http://77.42.88.106:3000/api/phases/{PHASE_ID}/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Crear schema inicial de base de datos",
    "description": "Definir modelos Prisma para User, Project, Phase, Task",
    "type": "feature",
    "priorityId": "{UUID_PRIORIDAD}",
    "statusId": "{UUID_TASK_CREATED}",
    "estimatedHours": 4,
    "assigneeId": "{UUID_DEL_AGENTE}"
  }' | jq .
```

**Campos:**

| Campo | Tipo | Requerido | Descripcion |
|-------|------|-----------|-------------|
| `title` | string (1-200 chars) | Si | Titulo de la tarea |
| `description` | string (max 2000) | No | Descripcion detallada |
| `type` | enum | No | `feature`, `bug`, `research`, `documentation`, `chore` |
| `statusId` | UUID | No | Status inicial (default: `task_pending`) |
| `priorityId` | UUID | Si | UUID de la prioridad (obtener de catalogos) |
| `estimatedHours` | number (positivo) | No | Horas estimadas |
| `startDate` | datetime ISO | No | Fecha de inicio |
| `endDate` | datetime ISO | No | Fecha de fin |
| `assigneeId` | UUID | No | UUID del usuario asignado (puede ser null) |
| `sourceIssueId` | UUID | No | Si la tarea se crea para resolver un issue |

**Response exitosa (201):**
```json
{
  "data": {
    "id": "uuid-de-la-tarea",
    "title": "...",
    "taskNumber": "DM-001",
    "phaseId": "...",
    "statusId": "...",
    "priorityId": "...",
    "assignedToId": "...",
    "createdAt": "..."
  }
}
```

### Listar tareas de una fase

```bash
curl -s "http://77.42.88.106:3000/api/phases/{PHASE_ID}/tasks" | jq .
```

### Listar todas las tareas (con filtros)

```bash
# Por proyecto
curl -s "http://77.42.88.106:3000/api/tasks?projectId={PROJECT_ID}" | jq .

# Por status
curl -s "http://77.42.88.106:3000/api/tasks?status=task_pending" | jq .

# Por asignado
curl -s "http://77.42.88.106:3000/api/tasks?assigneeId={USER_ID}" | jq .
```

---

## 7. Gestion de Status de Tareas

### Cambiar status

```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/{TASK_ID}/status \
  -H "Content-Type: application/json" \
  -d '{
    "statusId": "{UUID_NUEVO_STATUS}",
    "changedBy": "{UUID_USUARIO_QUE_CAMBIA}",
    "reason": "Motivo del cambio (obligatorio en regresiones)"
  }'
```

### Flujo de estados

```
task_created -> task_pending -> task_in_progress -> task_in_review -> task_completed -> task_approved
```

| Transicion | Quien la ejecuta |
|------------|------------------|
| created -> pending | PM al asignar |
| pending -> in_progress | Agente al empezar a trabajar |
| in_progress -> in_review | Agente al crear PR |
| in_review -> completed | PM/Tech Lead al aprobar review |
| completed -> approved | PM (terminal, no se puede revertir) |

### Regresiones (requieren `reason`)

Si mueves a un estado "anterior" (ej: in_review -> in_progress), el campo `reason` es **obligatorio**.

### Validacion: Assignee requerido

No se puede mover una tarea a `in_progress`, `in_review` o `completed` si **no tiene assignee** (`assignedToId`). Primero asigna la tarea, luego cambia el status.

---

## 8. Asignar una Tarea a un Agente

Para asignar (o reasignar) una tarea a un usuario:

```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/{TASK_ID} \
  -H "Content-Type: application/json" \
  -d '{
    "assigneeId": "{UUID_DEL_AGENTE}"
  }'
```

> **NOTA**: La asignacion tambien se puede hacer desde la UI del sistema. El PM (Martin) normalmente hace las asignaciones desde la interfaz.

---

## 9. Gestion de Issues

Los issues permiten reportar problemas/bugs en una tarea.

### Crear issue

```bash
curl -s -X POST http://77.42.88.106:3000/api/tasks/{TASK_ID}/issues \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Descripcion del problema",
    "description": "Detalle del issue con contexto y solucion propuesta",
    "type": "bug",
    "severity": "high"
  }'
```

| Tipos | Severidades |
|-------|-------------|
| `bug` | `low` |
| `improvement` | `medium` |
| `requirement` | `high` |
| `other` | `critical` |

### Consultar issues

```bash
# Issues de una tarea
curl -s "http://77.42.88.106:3000/api/tasks/{TASK_ID}/issues" | jq .

# Issue especifico
curl -s "http://77.42.88.106:3000/api/issues/{ISSUE_ID}" | jq .
```

### Resolver issue

```bash
curl -s -X PUT http://77.42.88.106:3000/api/issues/{ISSUE_ID} \
  -H "Content-Type: application/json" \
  -d '{
    "isResolved": true,
    "resolvedByTaskId": "{TASK_ID_QUE_RESUELVE}"
  }'
```

---

## 10. On-Hold y Resume

### Poner tarea en espera (por issue bloqueante)

```bash
curl -s -X PUT http://77.42.88.106:3000/api/tasks/{TASK_ID}/on-hold \
  -H "Content-Type: application/json" \
  -H "x-user-id: {TU_UUID_TECH_LEAD}" \
  -d '{
    "type": "bug",
    "title": "Descripcion del bloqueo",
    "description": "Detalle",
    "priority": "high"
  }'
```

> Requiere header `x-user-id`. Solo PM y Tech Lead pueden ejecutar.

### Reanudar tarea

```bash
curl -s -X PUT http://77.42.88.106:3000/api/tasks/{TASK_ID}/resume \
  -H "Content-Type: application/json" \
  -H "x-user-id: {TU_UUID_TECH_LEAD}" \
  -d '{
    "issueAction": "resolved",
    "comment": "Issues resueltos, reanudando tarea"
  }'
```

### Auto-resume

El sistema automaticamente reanuda tareas `on_hold` cuando **todos** sus issues se resuelven (ya sea manualmente o por completar la tarea resolutora).

---

## 11. Comentarios en Tareas

```bash
# Crear comentario
curl -s -X POST http://77.42.88.106:3000/api/tasks/{TASK_ID}/comments \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Texto del comentario con instrucciones para el agente",
    "userId": "{TU_UUID_TECH_LEAD}"
  }'

# Listar comentarios
curl -s "http://77.42.88.106:3000/api/tasks/{TASK_ID}/comments" | jq .
```

---

## 12. Dependencias entre Tareas

```bash
# Agregar dependencia (tarea A depende de tarea B)
curl -s -X POST http://77.42.88.106:3000/api/tasks/{TASK_A_ID}/dependencies \
  -H "Content-Type: application/json" \
  -d '{
    "dependsOnTaskId": "{TASK_B_ID}"
  }'

# Listar dependencias
curl -s "http://77.42.88.106:3000/api/tasks/{TASK_ID}/dependencies" | jq .

# Ver estado de dependencias
curl -s "http://77.42.88.106:3000/api/tasks/{TASK_ID}/dependencies/status" | jq .
```

> El sistema detecta dependencias circulares y las rechaza.
> Cuando una tarea bloqueante se completa, las dependientes se desbloquean automaticamente.

---

## 13. Flujo Completo de Trabajo

### Como Tech Lead, tu flujo es:

```
1. CREAR PROYECTO (una vez)
   POST /api/projects

2. CREAR FASES (una vez por fase)
   POST /api/projects/{projectId}/phases

3. Para cada unidad de trabajo:
   a. GENERAR BRIEF
      -> Documento tecnico: knowledge/agent-tasks/BRIEF_{ID}_{nombre}.md

   b. GENERAR ASSIGNMENT
      -> Documento de asignacion: knowledge/agent-tasks/ASSIGNMENT_{ID}_{nombre}.md
      -> Incluir: rama base, PRs previos, dependencias, archivos a leer, checklist

   c. CREAR TAREA en el sistema
      POST /api/phases/{phaseId}/tasks

   d. NOTIFICAR AL PM
      -> El PM asigna la tarea al agente desde la UI
      -> El PM pega los comentarios/mensajes en la tarea

   e. El agente trabaja y cambia status:
      pending -> in_progress -> in_review

   f. REVIEW
      -> Verificar que el agente completo todos los items del checklist
      -> Verificar documentacion (Code Logic, Dev Log)
      -> El PM mueve a completed -> approved

4. Si hay problemas:
   -> Crear ISSUE en la tarea
   -> Si es bloqueante: poner en on_hold
   -> Crear tarea resolutora si es necesario
   -> Cuando se resuelva: auto-resume o resume manual
```

---

## 14. Reglas Criticas

1. **El PM hace los merges** - NUNCA hacer merge de PRs tu mismo
2. **Asignaciones desde la UI** - El PM asigna tareas desde la interfaz, no via API
3. **Cada agente trabaja en su ambito** - Backend no toca frontend, DB Engineer maneja Prisma, etc.
4. **Si falta algo, crea un issue** - No mockear datos, no asumir
5. **Git flow**: `main` <- `develop` <- `feature/{TASK_ID}-descripcion`
6. **Documentar todo**: Cada tarea completada debe tener Code Logic y Dev Log

---

## 15. Referencia Rapida de Endpoints

| Accion | Metodo | Endpoint |
|--------|--------|----------|
| Crear proyecto | POST | `/api/projects` |
| Listar proyectos | GET | `/api/projects` |
| Obtener proyecto | GET | `/api/projects/{id}` |
| Crear fase | POST | `/api/projects/{projectId}/phases` |
| Listar fases | GET | `/api/projects/{projectId}/phases` |
| Crear tarea | POST | `/api/phases/{phaseId}/tasks` |
| Listar tareas | GET | `/api/tasks?projectId={id}` |
| Cambiar status | PATCH | `/api/tasks/{id}/status` |
| Asignar tarea | PATCH | `/api/tasks/{id}` |
| Crear issue | POST | `/api/tasks/{taskId}/issues` |
| Resolver issue | PUT | `/api/issues/{id}` |
| On-hold | PUT | `/api/tasks/{id}/on-hold` |
| Resume | PUT | `/api/tasks/{id}/resume` |
| Comentar | POST | `/api/tasks/{id}/comments` |
| Dependencias | POST | `/api/tasks/{id}/dependencies` |
| Catalogos status | GET | `/api/catalogs/status?process=task` |
| Catalogos prioridades | GET | `/api/catalogs/priorities` |
| Listar usuarios | GET | `/api/users` |
| Swagger docs | GET | `/api-docs` |

---

## 16. Documentos de Referencia

- **Procedimientos Operativos Standard**: `_project-management/templates/PROCEDIMIENTOS_OPERATIVOS_STANDARD.md`
- **Perfil Tech Lead Standard**: `_project-management/templates/PERFIL_TEACHLEAD_STANDARD.md`
- **Swagger interactivo**: http://77.42.88.106:3000/api-docs (todos los endpoints con ejemplos)

---

**Creado por**: Backend API Specialist (VTT)
**Fecha**: 2026-02-13
