# SKL-TASK-03: Generar Mensaje para el Agente

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-TASK-004_mensaje_agente.md`** en `02.normativa/03.Skills/task/`.
> Migración 1:1, contrato sin cambios. Esta versión se conserva como referencia histórica.


**Categoría:** VTT-TASK  
**Aplica a:** TL  
**Tokens estimados:** ~130  
**Cuándo:** FASE 2 — después de asignar la tarea (SKL-TASK-02), para que el PM lo pegue como comentario

---

## Precondición

- Tarea asignada al agente (SKL-TASK-02 ejecutada)
- ASSIGNMENT subido como attachment
- BRIEF subido como attachment
- UUIDs del agente y status disponibles (del OPERATIVO_TECH_LEAD.md)

---

## Variables requeridas

- `$TASK_ID` — ID de la tarea (ej: MS-048)
- `$TASK_TITLE` — título de la tarea
- `$ASSIGNEE_ROLE` — rol del agente (ej: BE, FE, DB)
- `$ASSIGNEE_UUID` — UUID del agente ejecutor
- `$SERVICE_KEY` — service key del proyecto
- `$UUID_IN_PROGRESS` — `2a76888a-e595-4cfc-ac4c-a3ae5087ef56`
- `$UUID_IN_REVIEW` — `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d`
- `$ASSIGNMENT_PATH` — ruta al archivo ASSIGNMENT
- `$BRIEF_PATH` — ruta al archivo BRIEF
- `$VTT_BASE_URL` — `http://77.42.88.106:3000`

---

## Ejecución

Generar este texto y entregarlo al PM para que lo pegue como comentario en la tarea:

```markdown
Agente Memory Service $ASSIGNEE_ROLE
Tienes tarea nueva asignada: $TASK_ID ($TASK_TITLE).

1. Lee el assignment completo: $ASSIGNMENT_PATH
2. Lee el brief: $BRIEF_PATH
3. Lee tu OPERATIVO: .claude/agents/OPERATIVO_${ASSIGNEE_ROLE}_MEMORY-SERVICE.md

Indicaciones del sistema:

0) Obtén tu JWT:
   curl -s -X POST $VTT_BASE_URL/api/auth/service-token \
     -H "Content-Type: application/json" \
     -d '{"userId":"$ASSIGNEE_UUID","serviceKey":"$SERVICE_KEY"}' \
     | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])"

a) Mueve la tarea a in_progress:
   curl -s -X PATCH $VTT_BASE_URL/api/tasks/$TASK_ID/status \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"statusId":"$UUID_IN_PROGRESS","changedBy":"$ASSIGNEE_UUID"}'

b) Trabaja la tarea siguiendo el workflow del assignment (12 pasos).

c) ANTES de mover a in_review, sube estos entregables:
   c.1) DevLog    → POST $VTT_BASE_URL/api/tasks/$TASK_ID/attachments (fileType=devlog)
   c.2) Code Logic → POST $VTT_BASE_URL/api/tasks/$TASK_ID/attachments (fileType=code_logic)
   c.3) Comentario de entrega → POST $VTT_BASE_URL/api/tasks/$TASK_ID/comments

d) Mueve la tarea a in_review:
   curl -s -X PATCH $VTT_BASE_URL/api/tasks/$TASK_ID/status \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"statusId":"$UUID_IN_REVIEW","changedBy":"$ASSIGNEE_UUID"}'

e) Entrega el reporte con el formato del assignment para revisión del TL.

Datos del sistema:
- Tu user ID: $ASSIGNEE_UUID
- Tu SERVICE_KEY: $SERVICE_KEY
- Status in_progress UUID: $UUID_IN_PROGRESS
- Status in_review UUID: $UUID_IN_REVIEW
- Backend: $VTT_BASE_URL

Atentamente,
Tech Lead
```

---

## Validación

- El mensaje contiene: TASK_ID, rutas exactas de ASSIGNMENT y BRIEF, UUID del agente, UUIDs de status, comandos completos
- El PM lo pega como comentario en la tarea vía SKL-COMMENT-01

---

## Nota

Los UUIDs de status son fijos para Memory Service. Si cambian, actualizar en `OPERATIVO_TECH_LEAD.md` y aquí.
