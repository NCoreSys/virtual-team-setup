# SKL-TASK-02: Asignar Tarea a Agente

**Categoría:** VTT-TASK  
**Aplica a:** TL  
**Tokens estimados:** ~150  
**Cuándo:** FASE 2 — al momento de asignar una tarea ya creada a un agente ejecutor

---

## Precondición

- `$TOKEN` obtenido (SKL-AUTH-01)
- Tarea ya existe en VTT con status `task_pending`
- Dependencias de la tarea en `task_completed` o `task_approved`
- ASSIGNMENT escrito con los 8 elementos obligatorios (ver `03_FLUJO_TL.md §4`)
- Inputs/documentos de la tarea verificados según `MAPA_DEPENDENCIAS_ENTREGABLES.md`

---

## Regla obligatoria antes de ejecutar

### R1 — Verificar inputs antes de asignar
Antes de generar el ASSIGNMENT, confirmar que todos los documentos input de la tarea existen en el repo con su ruta exacta. Si alguno falta → `task_blocked` en VTT + notificar PM. No asignar hasta que estén disponibles.

---

## Variables requeridas

- `$TOKEN` — JWT (SKL-AUTH-01)
- `$TASK_ID` — ID de la tarea (ej: MS-048)
- `$ASSIGNEE_UUID` — UUID del agente ejecutor
- `$AGENT_UUID` — UUID del TL
- `$TASK_SLUG` — nombre corto (ej: `setup-express`)
- `$ASSIGNMENT_PATH` — ruta al archivo ASSIGNMENT

---

## Ejecución

### Paso 1 — Subir ASSIGNMENT como attachment
```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$ASSIGNMENT_PATH" \
  -F "fileType=assignment" \
  -F "uploadedById=$AGENT_UUID"
```

### Paso 2 — Asignar agente a la tarea
```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"assignedToId\": \"$ASSIGNEE_UUID\"}"
```

> ⚠️ **Regla del proyecto Memory Service:** confirmar con PM si prefiere hacer la asignación desde la UI. Si el PM lo hace desde la UI, omitir Paso 2 y entregar el mensaje (SKL-TASK-03) para que el PM lo pegue.

---

## Validación

- Paso 1: HTTP 201, response incluye `id` del attachment
- Paso 2: HTTP 200, response incluye `assignedToId` = `$ASSIGNEE_UUID`
- Verificar: `GET /api/tasks/$TASK_ID` → `status` debe ser `task_pending`

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| 400 en attachment | `uploadedById` ausente | Agregar `-F "uploadedById=$AGENT_UUID"` |
| Agente no recibe la tarea | `assignedTo` en vez de `assignedToId` | Usar `assignedToId` |
| Tarea en `task_blocked` | Dependencia sin completar | Verificar estado de dependencias antes de asignar |
