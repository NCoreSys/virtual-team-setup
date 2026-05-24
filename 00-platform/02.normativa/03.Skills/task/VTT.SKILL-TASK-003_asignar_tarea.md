# VTT.SKILL-TASK-003 — Asignar Tarea a Agente

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-TASK-003` |
| **Categoría** | TASK (Task CRUD) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | TL |
| **Tokens estimados** | ~250 |
| **Cuándo se usa** | FASE 2 del PROTOCOL-ASG-001 §5.2.8-5.2.9 — al momento de asignar tarea ya creada a un agente ejecutor |
| **Reemplaza** | `SKL-TASK-03_asignar-tarea.md` (legacy, mal-nombrado como SKL-TASK-02 en su header) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea ya creada |
| `assignee_uuid` | uuid | sí | UUID del agente ejecutor |
| `assignment_path` | path | sí | Ruta local al ASSIGNMENT (`knowledge/agent-tasks/assignments/<phase>/<sprint>/...`) |
| `creator_uuid` | uuid | sí | UUID del TL que asigna |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea existe en VTT con status `task_pending` (`VTT.SKILL-TASK-001` ejecutada)
- Dependencias de la tarea en `task_completed` o `task_approved` (verificado en `VTT.SKILL-TASK-002` Paso 1.5)
- ASSIGNMENT escrito con los 8 elementos obligatorios (`VTT.SKILL-TASK-002` ejecutada)
- Worktree del agente existe (`VTT.WORKFLOW-WT-001.001` o `.003` ya ejecutados — ver `PROTOCOL-ASG-001 §5.2.10`)

---

## Variables del entorno

```bash
$TOKEN              # JWT
$VTT_BASE_URL       # http://77.42.88.106:3000
$AGENT_UUID         # UUID del TL
```

---

## Reglas obligatorias

### R1 — Verificar inputs ANTES de asignar

Confirmar que todos los documentos input de la tarea existen en el repo con su ruta exacta (lo cubre `VTT.SKILL-TASK-002` Paso 1.4). Si alguno falta → `task_blocked` en VTT + notificar al PM. **No asignar hasta que estén disponibles.**

### R2 — Confirmar política de asignación del proyecto

Algunos proyectos tienen política de que el PM hace la asignación final desde la UI (no por API). En ese caso:
- TL **omite Paso 2** (PATCH `assignedToId`)
- TL entrega el mensaje del agente (`VTT.SKILL-TASK-004`) al PM para que lo pegue manualmente

Confirmar la política con el PM al inicio del proyecto.

---

## Ejecución

### Paso 1 — Subir ASSIGNMENT como attachment `fileType=assignment`

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$ASSIGNMENT_PATH" \
  -F "fileType=assignment" \
  -F "uploadedById=$AGENT_UUID"
```

Output: `attachment_id` retornado por VTT.

### Paso 2 — Asignar agente a la tarea (PATCH)

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"assignedToId\": \"$ASSIGNEE_UUID\"}"
```

> ⚠️ **Si el proyecto tiene política "asignación por UI" (R2):** omitir este paso. El PM hace el PATCH desde la UI.

---

## Validación

```bash
# Check 1: attachment subido
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; ats=json.load(sys.stdin)['data']; print('assignment:', any(a['fileType']=='assignment' for a in ats))"
# Esperado: assignment: True

# Check 2: tarea asignada al agente
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; d=json.load(sys.stdin)['data']; print('assignee:', d.get('assignedToId'))"
# Esperado: assignee: <ASSIGNEE_UUID>

# Check 3: tarea sigue en task_pending (lista para que el agente la tome)
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; d=json.load(sys.stdin)['data']; print('status:', d['statusCode'])"
# Esperado: status: task_pending
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 en attachment | `uploadedById` ausente en multipart | Agregar `-F "uploadedById=$AGENT_UUID"` |
| Agente no recibe la tarea | Usar `assignedTo` en vez de `assignedToId` | Usar `assignedToId` exacto |
| HTTP 409 `TASK_BLOCKED` | Dependencia sin completar | Verificar deps con `VTT.SKILL-TASK-002 §1.5` antes de retry |
| HTTP 404 task | TASK_ID incorrecto | Validar el ID — debe ser el externo (MS-XXX), no el UUID interno |
| Asignación pisó otra | Tarea ya estaba asignada a otro agente | Confirmar con PM que es re-asignación, no error |

---

## Scripts invocados

Ninguno — 2 endpoints curl directos.

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — para `$TOKEN`
- (al terminar) `VTT.WORKFLOW-MAN-001.001_generar_execution_manifest` — generar manifest (siguiente paso del PROTOCOL-ASG-001 §5.2.11)
- (siguiente) `VTT.SKILL-TASK-004_mensaje_agente` — generar mensaje al agente

---

## Cuándo NO usar esta Skill

- **Si la política del proyecto es asignación por UI** (R2) — el PM lo hace manualmente
- **Si la tarea ya está asignada al mismo agente** (re-asignación = no-op) — saltar al siguiente paso

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-TASK-03_asignar-tarea.md`. Corrige el bug del header legacy que decía "SKL-TASK-02". Documenta explícitamente R2 (política de asignación PM-via-UI vs TL-via-API). Cross-ref con WT-001 + MAN-001 actualizados. |
