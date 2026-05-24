# Proceso de Asignacion de Tareas - Tech Lead

**Fecha:** 2026-03-19
**Version:** 1.4
**Contexto:** Proceso definido por el PM (Martin) para la asignacion correcta de tareas a agentes.

---

## Documentos Base (LEER SIEMPRE)

| # | Documento | Proposito |
|---|-----------|-----------|
| 1 | `knowledge/PROCEDIMIENTOS_OPERATIVOS_AGENTES.md` | Reglas operativas, APIs, UUIDs, git flow, endpoints completos |
| 2 | `_project-management/templates/PERFIL_TEACHLEAD_STANDARD.md` | Rol del Tech Lead, 8 elementos obligatorios en cada assignment |
| 3 | `_project-management/templates/TEMPLATE_ASIGNACION_TAREARev.md` | Template exacto para assignments (12 pasos, 5 entregables, checklist) |
| 4 | `_project-management/templates/06.PROCESO_CONSULTA_DOCS_TL.md` | Qué documentos consultar (routes/, schema.prisma, router.tsx) antes de escribir un assignment |

---

## Las Dos Fases del Proceso (LL-005)

El proceso tiene DOS fases distintas con responsabilidades diferentes:

### FASE 1 — Planificacion (al recibir el handoff)
- Leer el handoff del PM: que features, fechas, dependencias entre tareas
- Generar el plan del sprint con oleadas y bloqueantes
- Crear las tareas en el sistema via API
- Generar los BRIEFs (uno por tarea) y subirlos como attachments
- **Esta fase NO requiere leer codigo** — es planificacion de alto nivel
- Output: lista de tareas en el sistema con BRIEFs adjuntos

### FASE 2 — Asignacion (al momento de asignar una tarea)
- Escribir el ASSIGNMENT con informacion actualizada y verificada
- Para tareas FE con endpoints BE: completar la seccion `API/RECURSOS DISPONIBLES` desde el router/schemas real del backend — NO desde el handoff del PM
- Para tareas BE: leer el schema Prisma y los archivos de configuracion relevantes
- **NO es lectura a nivel detalle** (colores, radio buttons, comportamiento interactivo — eso lo lee el agente desde los HTMLs del UX)
- Subir el ASSIGNMENT como attachment de la tarea
- Output: ASSIGNMENT adjunto en la tarea, tarea asignada al agente

> **Regla LL-005:** El template de asignacion ya tiene la estructura correcta. El error es llenarlo desde la memoria o el handoff del PM en lugar de desde los artefactos ya generados (router.py, schemas.py, App.tsx, HTML del UX-Agent). El contrato tecnico lo define el codigo ya entregado, no la intencion de diseno del handoff.

---

## Flujo Completo (paso a paso)

### Paso 1: Recibir Handoff
- El PM da la lista de tareas pendientes o un handoff
- El Tech Lead analiza dependencias y define orden de implementacion

### Paso 2: Generar Briefs y Crear Tareas (FASE 1)
- Un BRIEF por cada tarea
- Ubicacion: `knowledge/agent-tasks/briefs/BRIEF_[VTT-XXX]_[nombre].md`
- El brief es el diseno original (inmutable)
- **Subir el BRIEF como attachment** de la tarea al crearse:
  ```bash
  # Subir BRIEF como attachment (via Python multipart — ver ERR-002 para backticks)
  POST http://77.42.88.106:3000/api/tasks/{taskId}/attachments
  # fields: file (binary), fileType="brief", uploadedById="UUID_TL"
  ```

### Paso 3: Generar Assignment (UNO A LA VEZ) (FASE 2)
- **REGLA CRITICA: Una tarea a la vez, a menos que el PM diga lo contrario**
- Usar template: `TEMPLATE_ASIGNACION_TAREARev.md`
- Ubicacion: `knowledge/agent-tasks/assignments/ASSIGNMENT_[VTT-XXX]_[nombre].md`

El assignment DEBE incluir (8 elementos del perfil Tech Lead):
1. Estado actual del proyecto
2. APIs y servicios disponibles (con ejemplos reales del codebase)
3. Arquitectura y estructura (patrones existentes)
4. Contexto de integracion (como se conecta con el resto)
5. Entidades y modelos (schema Prisma real)
6. Recursos de diseno (si aplica)
7. Checklist detallado (minimo 10-15 items verificables)
8. Archivos a revisar ANTES de empezar (con ruta y proposito)

**NO es codigo. Son instrucciones, API, configuracion, schema, diagramas.**

**Checklist LL-005 para completar el template** (tareas FE con endpoints BE):
```
Seccion: API/RECURSOS DISPONIBLES
  [ ] Abrir backend/src/routes/ o backend/app/api/ → identificar el router del modulo
  [ ] Leer decoradores/routes → copiar paths exactos al template
  [ ] Abrir schemas o types → copiar campos reales de response y body
  [ ] Marcar como [OK] los que existen, [FALTA] los que se asumen

Seccion: CRITICO — archivos que DEBES leer primero
  [ ] Listar cada HTML del UX-Agent (Design/screens/ y Design/components/)
  [ ] Listar el archivo FE existente que se va a modificar
  [ ] NO listar el handoff del PM — ese ya fue leido en Fase 1

Seccion: Rutas Frontend
  [ ] Abrir frontend/src/router/index.tsx → copiar rutas existentes del modulo
  [ ] Verificar si el componente objetivo ya existe o hay que crearlo desde cero
```

### Paso 4: Asignar Tarea en el Sistema
- Usar API para asignar el agente:
```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/VTT-XXX \
  -H "Content-Type: application/json" \
  -d '{"assigneeId": "UUID_DEL_AGENTE"}'
```
- **Subir el ASSIGNMENT como attachment** de la tarea al asignar:
  ```bash
  # Subir ASSIGNMENT como attachment (via Python multipart — ver ERR-002)
  POST http://77.42.88.106:3000/api/tasks/{taskId}/attachments
  # fields: file (binary), fileType="assignment", uploadedById="UUID_TL"
  ```

### Paso 5: Generar Mensaje para el Agente
- El PM (Martin) pega este mensaje como comentario en la tarea desde la UI
- El mensaje debe incluir TODO lo siguiente:

---

## Formato del Mensaje para el Agente

```
Tienes tarea nueva asignada: VTT-XXX (Titulo de la tarea).

1. Lee el assignment completo: knowledge/agent-tasks/ASSIGNMENT_VTT-XXX_nombre.md
2. Lee el brief: knowledge/agent-tasks/BRIEF_VTT-XXX_nombre.md
3. Lee los procedimientos operativos: knowledge/PROCEDIMIENTOS_OPERATIVOS_AGENTES.md
4. Lee los templates:
   - _project-management/templates/TEMPLATE_DEVELOPMENT_LOG.md
   - _project-management/templates/TEMPLATE_CODE_LOGIC.md

Indicaciones del sistema:

0) Obtén tu JWT de servicio (EJECUTAR PRIMERO — requerido para todos los PATCH de status):
python3 -c "
import urllib.request, json, sys
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({'userId': 'UUID_AGENTE', 'serviceKey': 'SERVICE_KEY_VALOR'}).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    sys.stdout.write(json.loads(r.read())['data']['token'])
"
Guarda la salida como TOKEN=<resultado> — el token tiene validez de 30 dias.

a) Mueve la tarea VTT-XXX a in_progress:
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/VTT-XXX/status -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d '{"statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56", "changedBy": "UUID_AGENTE"}'

b) Trabaja la tarea siguiendo el workflow del assignment (13 pasos)

c) DURANTE la tarea, registrar devlog entries en VTT:
curl -s -X POST "http://77.42.88.106:3000/api/tasks/VTT-XXX/devlog-entries" -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d '{"categoryCode": "decision", "severity": null, "title": "Descripcion de la decision", "reportedBy": "UUID_AGENTE"}'

d) Al completar, reportar cumplimiento de criterios de aceptacion (criteriaIds en el assignment):
curl -s -X POST "http://77.42.88.106:3000/api/tasks/VTT-XXX/criteria/CRITERIA_ID/fulfill" -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d '{"status": "met", "evidence": "Descripcion de evidencia concreta"}'

e) Si aplica, crear o vincular TrackableItems (ADRs, RFs, mejoras formales):
curl -s -X POST "http://77.42.88.106:3000/api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/trackable-items" -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d '{"typeCode": "ADR", "title": "...", "description": "...", "priority": "high"}'

f) ANTES de mover a in_review, subir entregables y verificar review gate:

   f.1) Verificar review gate (OBLIGATORIO — blockers critical/high bloquean con 422):
   curl -s "http://77.42.88.106:3000/api/tasks/VTT-XXX/review-gate" -H "Authorization: Bearer TOKEN"
   # Esperado: { "data": { "canProceedToReview": true } }
   # Si canProceedToReview = false → resolver entries bloqueantes primero

   f.2) Sube tu DevLog a la tarea:
   curl -s -X POST "http://77.42.88.106:3000/api/tasks/VTT-XXX/attachments" -F "file=@ruta/devlog.md" -F "fileType=devlog" -F "uploadedById=UUID_AGENTE"

   f.3) Sube tu(s) Code Logic a la tarea:
   curl -s -X POST "http://77.42.88.106:3000/api/tasks/VTT-XXX/attachments" -F "file=@ruta/archivo.LOGIC.md" -F "fileType=code_logic" -F "uploadedById=UUID_AGENTE"

   f.4) Sube tu reporte/comentario a la tarea (formato del assignment seccion REPORTE):
   curl -s -X POST http://77.42.88.106:3000/api/tasks/VTT-XXX/comments -H "Content-Type: application/json" -d '{"message": "Tu reporte de entrega aqui...", "userId": "UUID_AGENTE"}'

g) Mueve VTT-XXX a in_review:
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/VTT-XXX/status -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d '{"statusId": "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d", "changedBy": "UUID_AGENTE"}'

IMPORTANTE: Entregables OBLIGATORIOS antes de in_review:
1. Devlog entries registrados (decisiones, blockers, observaciones)
2. CAs reportados con fulfill (todos los criteriaIds del assignment)
3. TrackableItems creados/vinculados (o N/A confirmado)
4. Review gate: canProceedToReview = true
5. DevLog subido como attachment
6. Code Logic subido como attachment
7. Comentario de reporte con formato del assignment

e) Dame el reporte de entrega con el formato especificado en el assignment para que te la revise.

Datos del sistema:
- Tu user ID: UUID_AGENTE
- Tu SERVICE_KEY: SERVICE_KEY_VALOR
- Status in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
- Status in_review: 1ec975a5-7581-4a1a-ab8f-51b1a7ef868d
- Backend: http://77.42.88.106:3000
- Swagger: http://77.42.88.106:3000/api-docs
- Auth endpoint: POST /api/auth/service-token (body: userId + serviceKey)
```

> **NOTA LL-006 / VTT-296:** Desde 2026-03-20 todas las rutas de mutacion requieren JWT.
> El paso 0 obtiene un token de 30 dias via service account — no requiere password de usuario.
> Reemplaza `TOKEN` con el valor obtenido y `SERVICE_KEY_VALOR` con la clave provista por el PM.

---

## UUIDs de Agentes

| Agente | UUID | Email |
|--------|------|-------|
| Martin Rivas (PM) | `07a07147-cf5a-4117-8fbd-2fd1ccb95d54` | pm@vtt.com |
| Claude (Tech Lead) | `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` | tech.lead@vtt.ai |
| UX Designer | `ce8a2ace-21cb-44e9-978b-aa5f45977478` | ux.designer@vtt.ai |
| Design Lead | `ebf0f384-51ba-49f5-8e98-fa7569ce1d31` | design.lead@vtt.ai |
| Backend API Specialist | `8834830b-578f-46be-933b-0abcbbc5da99` | backend.dev@vtt.ai |
| Frontend Dev #1 | `84ad0fbe-996d-4aa7-abf6-57d64d4671de` | frontend.dev1@vtt.ai |
| Frontend Dev #2 | `9b8d927e-0013-4291-850d-bff968b37c84` | frontend.dev2@vtt.ai |
| Database Engineer | `a3a2ce62-28d8-419d-9888-44203a963894` | db.engineer@vtt.ai |
| DevOps Engineer | `b2e00b9d-a657-4bdb-b982-3dcf1f5b5757` | devops@vtt.ai |
| Integration Reviewer | `fbef6ae6-ba0d-43ce-8cc1-2f28c9c6346d` | integration.reviewer@vtt.ai |
| Integration Auditor | `f294a61d-ffcd-411f-9f24-3adcccae446b` | integration.auditor@vtt.ai |
| Auditor Reviewer | `9cc9e322-3c36-4823-af2e-78d13f5b895b` | auditor.reviewer@vtt.ai |
| Product Owner | `4128b577-eec1-4bc2-a595-42bd6b43db5e` | product.owner@vtt.ai |
| Product Manager | `07395164-eeb8-4ef8-9600-70f2f89c2b24` | product.manager@vtt.ai |
| Program Manager | `c6e012c7-de80-4d37-b375-f9a2d6abdec7` | program.manager@vtt.ai |
| Project Manager (PJM) | `49937318-7a1d-4b83-9b7e-81aa49394d92` | project.manager@vtt.ai |
| QA Engineer | `1d8eb958-aef7-42f4-ba30-1a7d33a60d39` | qa.engineer@vtt.ai |
| Systems Analyst | `becdf45a-039b-4e8f-8c83-09f473a914a8` | systems.analyst@vtt.ai |

## UUIDs de Status

| Status | UUID |
|--------|------|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

## UUIDs de Prioridad

| Prioridad | UUID |
|-----------|------|
| critical | `90ec3df2-fac4-40fa-b2ce-29daf0f4956e` |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` |
| low | `95f2e731-41b9-4a7d-9a43-31f00a4ddd7e` |

---

## Plan de Implementacion Actual (Fase 4-A2)

### Oleada 1 (paralelo):
| Tarea | Agente | Status |
|-------|--------|--------|
| VTT-033 (FE-10 Kanban/Filter) | Frontend Dev #1 | COMPLETADA (PR #106) |
| VTT-051+052 (Versionado + CRUD Docs) | Backend API Specialist | ASIGNADA |
| VTT-054 (Design 404 Page) | Design Lead | PENDIENTE |
| VTT-055 (Design Estados UI) | Design Lead | PENDIENTE |
| VTT-056 (Design Responsive) | Design Lead | PENDIENTE |

### Oleada 2 (despues de Oleada 1):
| Tarea | Agente | Status |
|-------|--------|--------|
| VTT-053 (Auth Basico) | Backend API Specialist | PENDIENTE (necesita campo password - issue DB Engineer) |
| VTT-057 (QA Visual) | Design Lead | PENDIENTE (depende de 054/055/056) |

### Oleada 3 (despues de backend):
| Tarea | Agente | Status |
|-------|--------|--------|
| VTT-058 (Frontend Login) | Frontend Dev | PENDIENTE (brief por crear) |
| VTT-059 (Frontend 404) | Frontend Dev | PENDIENTE (brief por crear) |
| VTT-060 (Frontend Documentos) | Frontend Dev | PENDIENTE (brief por crear) |

### Oleada 4 (ultimo):
| Tarea | Agente | Status |
|-------|--------|--------|
| VTT-061 (Testing E2E) | Frontend Dev | PENDIENTE (brief por crear) |

---

## Reglas Criticas

1. **UNA tarea a la vez** - No asignar multiples tareas salvo que el PM lo autorice
2. **Assignment con integracion real** - No instrucciones genericas, incluir codigo/schema/API del codebase actual
3. **El PM hace los merges** - NUNCA el Tech Lead ni los agentes
4. **El PM asigna en la UI** - El Tech Lead puede asignar via API cuando el PM lo instruya
5. **Verificar estado real** antes de crear assignment - No asumir, leer el codigo
6. **Seguir el template** TEMPLATE_ASIGNACION_TAREARev.md al pie de la letra
7. **LL-005: Llenar el template desde artefactos verificados** - La seccion `API/RECURSOS DISPONIBLES` se completa desde el router/schemas real del BE, NO desde el handoff del PM. El handoff es intencion de diseno, no contrato tecnico.
8. **BRIEF = adjunto al crear la tarea. ASSIGNMENT = adjunto al asignar la tarea.** No subir retroactivamente si se puede evitar.

---

## Ciclo de Vida Completo de una Tarea

### Flujo normal (sin issues)

```
1. Tech Lead genera Brief + Assignment
2. Tech Lead asigna tarea via API (PATCH /api/tasks/VTT-XXX assigneeId)
   -> Sistema auto-transiciona: task_created -> task_pending
3. PM pega mensaje al agente con documentos + curls + datos del sistema
4. Agente mueve a in_progress (PATCH status, changedBy: UUID_AGENTE)
5. Agente trabaja la tarea (codigo, docs, git, PR)
6. Agente mueve a in_review (PATCH status, changedBy: UUID_AGENTE)
7. Tech Lead revisa:
   - Lee entregables (spec, codigo, docs)
   - Verifica consistencia (tokens, patrones, design system)
   - Verifica checklist del assignment
8. Tech Lead mueve a completed (PATCH status, changedBy: UUID_TECHLEAD)
9. PM aprueba -> task_approved (PATCH status, changedBy: UUID_PM)
```

### Flujo con issue (on-hold + auto-resume)

```
1-6. Igual que flujo normal hasta in_review

7. Tech Lead (o PM) detecta problema -> crea issue en la tarea:
   POST /api/tasks/VTT-XXX/issues
   body: {"title": "...", "description": "...", "type": "...", "severity": "..."}

8. PM pone tarea en on_hold vinculada al issue:
   PUT /api/tasks/VTT-XXX/on-hold
   headers: x-user-id: UUID_PM
   body: {"issueId": "UUID_ISSUE", "comment": "Motivo"}
   -> Sistema guarda previousStatus (ej: task_in_review)

9. Se crea tarea nueva vinculada al issue:
   POST /api/phases/{phaseId}/tasks
   body: {..., "sourceIssueId": "UUID_ISSUE"}
   -> Sistema vincula automaticamente: issue.resolvedByTaskId = nueva tarea

10. Nueva tarea pasa por el flujo completo:
    pending -> in_progress -> in_review -> completed

11. Al completar la nueva tarea, el sistema automaticamente:
    a) Marca el issue como resuelto (isResolved: true)
    b) Si TODOS los issues de la tarea on_hold estan resueltos:
       -> Auto-resume: tarea vuelve a previousStatus (ej: task_in_review)

12. Tech Lead retoma el review de la tarea original
    -> Si todo OK: mueve a completed
    -> PM aprueba: task_approved
```

### Responsabilidades por status

| Status | Quien lo ejecuta | Accion |
|--------|------------------|--------|
| task_created -> task_pending | Sistema (auto al asignar) | Asignar assigneeId |
| task_pending -> task_in_progress | Agente | Empieza a trabajar |
| task_in_progress -> task_in_review | Agente | Termino, creo PR |
| task_in_review -> task_completed | Tech Lead | Review aprobado |
| task_completed -> task_approved | PM (Martin) | Aprobacion final |
| cualquiera -> task_on_hold | PM | Hay issue bloqueante |
| task_on_hold -> previousStatus | Sistema (auto-resume) | Issues resueltos |

### Comandos del Tech Lead para review

> **JWT requerido desde VTT-296.** Usar Python para obtener token y hacer PATCH de status (evita expansion de `!` en bash — ERR-010):

```python
# Obtener token TL y mover tarea a completed
import urllib.request, json

req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({'userId': 'abdff0db-ad0b-4a0c-99f5-c898d18bd2d8', 'serviceKey': 'SERVICE_KEY_VALOR'}).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    token = json.loads(r.read())['data']['token']

# Mover a completed
req2 = urllib.request.Request(
    'http://77.42.88.106:3000/api/tasks/VTT-XXX/status',
    data=json.dumps({'statusId': 'aa5ceb90-5209-42a2-b874-a8cbee597a97', 'changedBy': 'abdff0db-ad0b-4a0c-99f5-c898d18bd2d8'}).encode(),
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}, method='PATCH')
with urllib.request.urlopen(req2) as r2:
    print(json.loads(r2.read()))
```

```bash
# Agregar comentario de review (comentarios no requieren JWT)
curl -s -X POST http://77.42.88.106:3000/api/tasks/VTT-XXX/comments \
  -H "Content-Type: application/json" \
  -d '{"message": "Review aprobado. [detalles]", "userId": "abdff0db-ad0b-4a0c-99f5-c898d18bd2d8"}'

# Crear tarea vinculada a un issue (para resolver el issue)
curl -s -X POST http://77.42.88.106:3000/api/phases/{phaseId}/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "...", "description": "...", "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422", "priorityId": "UUID", "sourceIssueId": "UUID_ISSUE"}'
```

### Nota sobre campo de comentarios

El campo para crear comentarios es `message` (NO `content`):
```bash
POST /api/tasks/VTT-XXX/comments -> body: {"message": "texto", "userId": "UUID"}
```

---

## Proceso de Issues (cuando un agente necesita algo)

Los issues son el mecanismo para que un agente "levante la mano" cuando:
- Necesita un cambio fuera de su ambito (ej: Backend necesita migration -> issue para DB Engineer)
- Encuentra un bug durante su implementacion
- Detecta que falta un requisito o hay una mejora necesaria
- Tiene un bloqueante que otro agente debe resolver

### Cuando crear un issue

| Situacion | Tipo | Severidad | Ejemplo |
|-----------|------|-----------|---------|
| Necesito cambio en schema.prisma | `requirement` | `medium`/`high` | "Agregar campo password a User" |
| Encontre un bug en codigo existente | `bug` | segun impacto | "El endpoint X devuelve 500 cuando..." |
| Falta funcionalidad que bloquea mi tarea | `requirement` | `high`/`critical` | "No existe endpoint para Y" |
| Mejora que facilita la implementacion | `improvement` | `low`/`medium` | "Agregar index en tabla Z" |
| Necesito deploy o rebuild de container | `requirement` | `high` | "Ejecutar migration y rebuild backend" |

### Como crear un issue

```bash
curl -s -X POST {BASE_URL}/api/tasks/{TASK_ID}/issues \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Titulo claro y descriptivo",
    "description": "## Contexto\nQue estoy haciendo y por que necesito esto\n\n## Que necesito\nDescripcion exacta del cambio requerido\n\n## Archivos afectados\n- ruta/archivo.ts\n\n## Quien debe resolverlo\nDB Engineer / DevOps / Frontend / etc",
    "type": "bug | improvement | requirement | other",
    "severity": "low | medium | high | critical"
  }'
```

**IMPORTANTE:** El issue se crea en la tarea donde se detecto el problema o la necesidad. NO en la tarea del agente que lo debe resolver.

### En que tarea crear el issue

| Situacion | Donde crear el issue |
|-----------|---------------------|
| Necesito algo para completar MI tarea | En MI tarea (VTT-XXX) |
| Encontre bug en funcionalidad de OTRA tarea | En la tarea donde esta el bug |
| Mejora general del proyecto | En la tarea de issues abiertos (ej: VTT-050) |

### Flujo completo de un issue

```
1. Agente detecta necesidad
   -> Crea issue en la tarea correspondiente (POST /api/tasks/{taskId}/issues)

2. Agente notifica al PM
   -> Comenta en la tarea explicando el issue y quien debe resolverlo
   -> Si es bloqueante: solicita poner tarea en on_hold

3. PM coordina
   -> Asigna al agente responsable (DB Engineer, DevOps, etc.)
   -> O crea una tarea nueva para resolver el issue

4. Agente responsable resuelve
   -> Implementa el cambio
   -> Marca el issue como resuelto:
   curl -s -X PUT {BASE_URL}/api/issues/{ISSUE_ID} \
     -H "Content-Type: application/json" \
     -d '{"isResolved": true}'

5. Si se creo una tarea para resolver el issue, vincularla:
   curl -s -X PUT {BASE_URL}/api/issues/{ISSUE_ID} \
     -H "Content-Type: application/json" \
     -d '{"resolvedByTaskId": "VTT-YYY"}'
   -> Cuando VTT-YYY se complete, el issue se auto-resuelve

6. Si la tarea original estaba en on_hold y TODOS sus issues se resuelven:
   -> El sistema la reanuda automaticamente (auto-resume)
```

### Consultar issues

```bash
# Ver issues de una tarea
GET /api/tasks/{TASK_ID}/issues

# Ver issue especifico
GET /api/issues/{ISSUE_ID}

# Actualizar issue
PUT /api/issues/{ISSUE_ID} -> body: {"isResolved": true, "resolvedByTaskId": "VTT-YYY"}

# Eliminar issue
DELETE /api/issues/{ISSUE_ID}
```

### Reglas de issues

1. **Cada agente crea issues en su propia tarea** para documentar que necesita
2. **NO resolver issues de otros** - cada agente resuelve lo que le corresponde
3. **Describir claramente** que se necesita y quien debe hacerlo
4. **Si es bloqueante**, pedir al PM que ponga la tarea en on_hold vinculada al issue
5. **El issue NO es un chat** - es un registro formal de una necesidad. Para discusion usar comentarios

---

## APIs del Sistema (referencia rapida)

### Tareas e Issues

```bash
# Asignar tarea
PATCH /api/tasks/VTT-XXX  -> body: {"assigneeId": "UUID"}

# Cambiar status
PATCH /api/tasks/VTT-XXX/status -> body: {"statusId": "UUID", "changedBy": "UUID"}

# Crear comentario
POST /api/tasks/VTT-XXX/comments -> body: {"message": "texto", "userId": "UUID"}

# Crear issue
POST /api/tasks/VTT-XXX/issues -> body: {"title": "...", "description": "...", "type": "bug|improvement|blocker|other", "reportedById": "UUID"}

# Actualizar issue (linkear tarea correctiva)
PUT /api/issues/{ISSUE_ID} -> body: {"isResolved": true, "resolvedByTaskId": "VTT-YYY"}

# Ver issues de una tarea
GET /api/tasks/VTT-XXX/issues

# Ver actividad / Ver tarea
GET /api/tasks/VTT-XXX/activity
GET /api/tasks/VTT-XXX
```

---

### Devlog Entries (Modelo Dinámico V4 — S10 + S12)

> Obligatorio en toda tarea. Registrar decisiones, blockers, deuda técnica, observaciones.

```bash
# Crear entry individual
POST /api/tasks/VTT-XXX/devlog-entries
body: {
  "categoryCode": "decision|tech_debt|blocker|risk|testing_note|observation|improvement|brand_issue",
  "severity": null,          # null para decision/observation. "critical|high|medium|low" para el resto
  "title": "Descripción del entry",
  "description": "Contexto adicional (opcional)",
  "reportedBy": "UUID_AGENTE"
}

# Crear múltiples entries en una llamada (máx 50)
POST /api/tasks/VTT-XXX/devlog-entries
body: {
  "entries": [
    {"categoryCode": "decision", "severity": null, "title": "...", "reportedBy": "UUID"},
    {"categoryCode": "blocker",  "severity": "high", "title": "...", "reportedBy": "UUID"}
  ]
}

# Consultar entries (con filtros opcionales)
GET /api/tasks/VTT-XXX/devlog-entries
GET /api/tasks/VTT-XXX/devlog-entries?status=pending
GET /api/tasks/VTT-XXX/devlog-entries?severity=critical,high&status=pending

# Cambiar estado de un entry (resolver/diferir/wont_fix)
PATCH /api/tasks/VTT-XXX/devlog/{entryId}/status
body: {"status": "resolved", "resolution": "Cómo se resolvió"}           # resolved
body: {"status": "deferred", "deferredToPhaseId": "UUID_PHASE"}          # deferred
body: {"status": "wont_fix", "resolution": "Razón de no corrección"}     # wont_fix
```

**Categorías válidas** (seed en producción):
| code | severity | Cuándo usar |
|------|----------|-------------|
| `decision` | null | Decisión técnica tomada |
| `observation` | null | Observación general |
| `tech_debt` | critical/high/medium/low | Deuda técnica |
| `blocker` | critical/high/medium/low | Bloquea el avance |
| `risk` | critical/high/medium/low | Riesgo identificado |
| `testing_note` | critical/high/medium/low | Resultado de test |
| `improvement` | medium/low | Mejora para iteración futura |
| `brand_issue` | critical/high/medium | Issue de marca/diseño |

---

### Review Gate — CRÍTICO antes de mover a in_review

> Entries con `severity=critical|high` y `status=pending` bloquean el gate con error 422.

```bash
# Verificar gate ANTES de mover a in_review
GET /api/tasks/VTT-XXX/review-gate
# Esperado: { "data": { "canProceedToReview": true } }

# Si hay blockers → resolverlos primero:
PATCH /api/tasks/VTT-XXX/devlog/{entryId}/status
body: {"status": "resolved", "resolution": "Descripción"}

# Resumen de devlog por fase/sprint
GET /api/phases/{phaseId}/devlog-summary
GET /api/phases/{phaseId}/devlog-review
```

---

### Criterios de Aceptación (S09 + S10)

> El TL crea los CAs ANTES de asignar la tarea. El agente reporta cumplimiento al completar.

```bash
# TL: Crear CA en el proyecto (obtener criteriaId UUID)
POST /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/acceptance-criteria
body: {
  "criteriaTypeCode": "functional|technical|ux|security|performance|integration",
  "title": "Título del criterio",
  "description": "Descripción detallada"
}

# Ver CAs de una tarea
GET /api/tasks/VTT-XXX/criteria

# Agente: reportar cumplimiento de un CA
POST /api/tasks/VTT-XXX/criteria/{criteriaId}/fulfill
body: {
  "status": "met",         # "pending|met|not_met|partial|deferred"
  "evidence": "PR #123, verificado con curl GET /api/...",
  "notes": "Notas opcionales"
}

# Reporte de cobertura de criterios del proyecto
GET /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/criteria-coverage
```

---

### Trackable Items — RFs, ADRs, User Stories, KPIs (S04)

> Crear cuando la tarea implementa un requisito funcional, decisión de arquitectura o KPI formal.

```bash
# Crear TrackableItem
POST /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/trackable-items
body: {
  "typeCode": "RF|ADR|USER_STORY|BUG|KPI",
  "title": "Título",
  "description": "Descripción",
  "priority": "critical|high|medium|low"
}

# Vincular tarea a un TrackableItem existente
POST /api/trackable-items/{itemId}/tasks
body: {"taskId": "VTT-XXX"}

# Ver items del proyecto
GET /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/trackable-items

# Diferir un TrackableItem (no se puede resolver en este sprint)
POST /api/trackable-items/{itemId}/defer
body: {
  "reason": "Sin capacidad en este sprint",
  "targetType": "phase|sprint|release",
  "targetPhaseId": "UUID_FASE_DESTINO"
}

# Reporte de trazabilidad completo
GET /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/traceability-report
```

---

### Document Impacts (S10)

> Registrar qué documentos impacta la tarea durante su ejecución.

```bash
# Registrar impacto
POST /api/tasks/VTT-XXX/document-impacts
body: {
  "documentSourceId": "UUID",
  "impactType": "added|modified|removed|referenced",
  "description": "Qué cambió y por qué"
}

# Ver impactos de la tarea
GET /api/tasks/VTT-XXX/document-impacts

# Marcar documento como actualizado
POST /api/tasks/VTT-XXX/document-impacts/{docId}/complete
```

---

### Releases y Sprints (S03)

```bash
# Crear release
POST /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/releases
body: {"name": "MVP", "startDate": "2026-05-01T00:00:00Z", "endDate": "2026-06-30T00:00:00Z"}

# Crear sprint dentro de un release
POST /api/releases/{releaseId}/sprints
body: {"name": "S13", "number": 13, "startDate": "...", "endDate": "..."}

# Ver sprints de un release
GET /api/releases/{releaseId}/sprints

# Ver detalle de sprint (incluye tasks[])
GET /api/sprints/{sprintId}
```

---

### Firmas y Aprobaciones (S08)

```bash
# Firmar cierre de sprint
POST /api/sprints/{sprintId}/sign
body: {"userId": "UUID", "comment": "Sprint cerrado correctamente"}

# Ver aprobaciones pendientes del usuario
GET /api/approvals/pending

# Verificar si una fase puede cerrarse (TrackableItems sin resolver)
GET /api/phases/{phaseId}/can-close
```

---

### Compliance Checks (S07)

```bash
# Ver checks del proyecto
GET /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/compliance-checks

# Ejecutar un check
POST /api/compliance-checks/{checkId}/execute

# Ver compliance de un sprint
GET /api/sprints/{sprintId}/compliance
```

---

## Deliveries (Entregables) — Nueva Característica MGP

Los **Deliveries** son entregables que agrupan tareas dentro de una fase. Permiten organizar el trabajo en paquetes funcionales que pueden ser auditados, revisados y aprobados de forma independiente.

### Jerarquía MGP

```
Proyecto
  └── Fase
        └── Delivery (Entregable)
              └── Tarea (puede estar en un solo Delivery a la vez)
```

**Uso principal:** Agrupar tareas relacionadas (ej: todos los fixes de una fase de auditoría) para seguimiento y revisión.

---

### Estados de un Delivery

| Estado | Código |
|--------|--------|
| Planificado | `delivery_planned` |
| En progreso | `delivery_in_progress` |
| Completado | `delivery_completed` |
| Cancelado | `delivery_cancelled` |

---

### Reglas de Negocio

| Regla | Descripción |
|-------|-------------|
| **RN-010** | Una tarea debe estar en la **misma fase** que el Delivery al que se asigna |
| **RN-004** | Una tarea **no puede estar en dos Deliveries** al mismo tiempo |

---

### API de Deliveries — Endpoints

#### Crear un Delivery

```bash
curl -s -X POST http://77.42.88.106:3000/api/deliveries \
  -H "Content-Type: application/json" \
  -d '{
    "phaseId": "PHASE_ID",
    "name": "Nombre del entregable",
    "order": 1,
    "createdBy": "UUID_AGENTE",
    "description": "Descripcion opcional",
    "startDate": "2026-03-18T00:00:00Z",
    "endDate": "2026-04-01T00:00:00Z"
  }'
```

Campos obligatorios: `phaseId`, `name`, `order`, `createdBy`

#### Obtener un Delivery (con tareas asignadas)

```bash
curl -s http://77.42.88.106:3000/api/deliveries/{deliveryId}
```

Respuesta incluye: delivery + lista de tareas + status + fase.

#### Actualizar un Delivery

```bash
curl -s -X PUT http://77.42.88.106:3000/api/deliveries/{deliveryId} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nuevo nombre",
    "description": "Nueva descripcion",
    "order": 2,
    "startDate": "2026-03-18T00:00:00Z",
    "endDate": "2026-04-15T00:00:00Z",
    "statusId": "UUID_STATUS",
    "lifecycleStage": "development"
  }'
```

#### Eliminar un Delivery

```bash
curl -s -X DELETE http://77.42.88.106:3000/api/deliveries/{deliveryId}
```

**Nota:** Al eliminar, las tareas asociadas quedan libres (`deliveryId = null`), no se eliminan.

#### Asignar una Tarea a un Delivery

```bash
curl -s -X POST http://77.42.88.106:3000/api/deliveries/{deliveryId}/tasks/{taskId} \
  -H "Content-Type: application/json" \
  -d '{"assignedBy": "UUID_AGENTE"}'
```

**Validaciones:** RN-010 (misma fase) y RN-004 (tarea libre).

#### Desasignar una Tarea de un Delivery

```bash
curl -s -X DELETE http://77.42.88.106:3000/api/deliveries/{deliveryId}/tasks/{taskId}
```

---

### Flujo de Trabajo con Deliveries

**Escenario:** Organizar fixes de auditoría de integración en Deliveries.

```
1. Identificar las fases que contienen las tareas a agrupar
2. Crear un Delivery por grupo funcional dentro de la fase correspondiente:
   POST /api/deliveries (phaseId, name, order, createdBy)
3. Asignar las tareas al Delivery:
   POST /api/deliveries/{deliveryId}/tasks/{taskId}
   -> VERIFICAR que tarea y delivery esten en la MISMA FASE (RN-010)
4. Trackear progreso via GET /api/deliveries/{deliveryId}
5. Actualizar estado del Delivery segun avance:
   PUT /api/deliveries/{deliveryId} -> { statusId, lifecycleStage }
```

---

### Instrucciones para el Tech Lead VTT — Uso de Deliveries en Auditorías

Cuando el PM solicite organizar tareas usando Deliveries:

1. **Identificar la fase** donde viven las tareas a agrupar
2. **Crear el Delivery** usando el TL como `createdBy`:
   ```bash
   curl -s -X POST http://77.42.88.106:3000/api/deliveries \
     -H "Content-Type: application/json" \
     -d '{
       "phaseId": "PHASE_ID_CORRECTO",
       "name": "Fixes Auditoria — [Sprint/Area]",
       "order": 1,
       "createdBy": "abdff0db-ad0b-4a0c-99f5-c898d18bd2d8",
       "description": "Entregable que agrupa los fixes de [descripcion]"
     }'
   ```
3. **Asignar las tareas** una por una (verificar misma fase):
   ```bash
   curl -s -X POST http://77.42.88.106:3000/api/deliveries/{DELIVERY_ID}/tasks/{TASK_ID} \
     -H "Content-Type: application/json" \
     -d '{"assignedBy": "abdff0db-ad0b-4a0c-99f5-c898d18bd2d8"}'
   ```
4. **Verificar** que el Delivery tiene todas las tareas esperadas:
   ```bash
   curl -s http://77.42.88.106:3000/api/deliveries/{DELIVERY_ID}
   ```

**NUNCA** asignar una tarea a un Delivery de una fase distinta — el API retornara error (RN-010).

---

## Actualizar Campos de Tiempo en Tareas

Los agentes pueden actualizar la estimacion de horas de su propia tarea cuando detectan que la estimacion original es incorrecta. **Requiere autorizacion del PM o TL** excepto cuando el brief lo indica explicitamente.

### Campos disponibles

| Campo | Descripcion | Cuando usarlo |
|-------|-------------|---------------|
| `estimatedHours` | Horas estimadas para completar la tarea | Al inicio si la estimacion original esta muy desviada |
| `plannedStartDate` | Fecha de inicio planificada (ISO 8601) | Solo el TL o PM — define el plan del proyecto |
| `plannedEndDate` | Fecha de fin planificada (ISO 8601) | Solo el TL o PM — define el plan del proyecto |

### Reglas

1. **`estimatedHours`**: El agente puede actualizarla si detecta que la estimacion original es incorrecta. DEBE mencionar el cambio en el comentario/reporte de entrega.
2. **`plannedStartDate` / `plannedEndDate`**: Solo el TL o PM. Afectan el Gantt y la ruta critica del proyecto.
3. **NUNCA actualizar tiempos sin mencionarlo** — siempre dejar comentario explicando la razon.

### Como actualizar (requiere JWT)

```python
# Actualizar estimatedHours de una tarea
import urllib.request, json

with open('/tmp/vtt_token.txt') as f:
    token = f.read().strip()

body = json.dumps({'estimatedHours': 8}).encode()
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/tasks/VTT-XXX',
    data=body,
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
    method='PATCH')
with urllib.request.urlopen(req) as r:
    print(json.loads(r.read()))
```

```bash
# Alternativa curl (si el token no contiene caracteres especiales)
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/VTT-XXX \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"estimatedHours": 8}'

# Actualizar fechas planificadas (solo TL/PM)
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/VTT-XXX \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"plannedStartDate": "2026-04-01T00:00:00Z", "plannedEndDate": "2026-04-03T00:00:00Z"}'
```

### Comentario obligatorio al cambiar estimacion

Cuando un agente cambia `estimatedHours`, DEBE dejar un comentario en la tarea:

```bash
curl -s -X POST http://77.42.88.106:3000/api/tasks/VTT-XXX/comments \
  -H "Content-Type: application/json" \
  -d '{"message": "Actualice estimatedHours de X a Y horas. Razon: [explicacion breve]", "userId": "UUID_AGENTE"}'
```

---

**Ultima actualizacion:** 2026-05-01
**Version:** 1.6

### Changelog
- v1.6 (2026-05-01): Integración Modelo Dinámico V4 — nueva sección "APIs del Sistema" con endpoints de Devlog Entries, Review Gate, Criterios de Aceptación (fulfill), Trackable Items, Document Impacts, Releases/Sprints, Firmas y Compliance. Mensaje del agente actualizado con 7 entregables obligatorios (devlog, CAs, trackables, review gate, devlog attachment, code logic, comentario). Template de assignment actualizado a v3.0.
- v1.5 (2026-03-20): LL-006/VTT-296 — JWT requerido en rutas de mutacion. Mensaje del agente actualizado con paso 0 (service token via Python), Authorization header en curls de status, entregables obligatorios antes de in_review. Comandos TL actualizados con Python + service token. Nueva seccion "Actualizar Campos de Tiempo en Tareas".
- v1.4 (2026-03-19): LL-005 — Dos fases del proceso (Planificacion vs Asignacion). Regla: template debe llenarse desde artefactos verificados (router/schemas/HTML), no desde handoff del PM. Checklist para seccion API/RECURSOS DISPONIBLES. Pasos de upload de BRIEF y ASSIGNMENT como attachments.
- v1.3 (2026-03-18): Agregada seccion completa de Deliveries (Entregables MGP) — endpoints, reglas de negocio, flujo de uso y guia para el TL VTT
- v1.2 (2026-02-12): Version anterior
