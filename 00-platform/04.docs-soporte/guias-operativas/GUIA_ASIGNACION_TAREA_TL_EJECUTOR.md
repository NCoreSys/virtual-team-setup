# Guía operativa — Asignación de tarea (TL Ejecutor)

**Versión:** 2.1
**Fecha:** 2026-05-14
**Aplicable a:** TL Ejecutor Memory Service
**Tiempo estimado por tarea:** 30-45 min

Cheatsheet completo del `PROCESO_ASIGNACION_TAREAS_v3.md` (FASE 1 + FASE 2) aterrizado a pasos concretos con comandos curl listos para pegar.

**Changelog v1.0 → v2.1:**
- Paso 8.5 NUEVO: crear execution_manifest desde template antes de generar mensaje
- Referencias a `VTT.PROTOCOL-WT-001`

---

## Variables que necesitas exportar al inicio de sesión

```bash
export BASE="http://77.42.88.106:3000"
export TL="92225290-6b6b-4c1f-a940-dcb4262507aa"
export SK="hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"
export PROJECT_ID="d0fc276d-e764-4a83-96e9-d65f086ed803"

export TOKEN=$(curl -s -X POST "$BASE/api/auth/service-token" \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"$TL\",\"serviceKey\":\"$SK\"}" \
  | python -c "import sys,json;print(json.load(sys.stdin)['data']['token'])")
```

## UUIDs del equipo (memorizar o copiar)

| Rol | UUID |
|---|---|
| TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| Backend | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| Frontend | `d23c9cd9-a156-433b-8900-94add5488eec` |
| QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` |
| DevOps | `322e3745-9756-4a7c-af11-44b33edef44d` |
| DL | `b3a09269-cded-468c-a475-15a48f203cb0` |
| UX | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` |
| SA | `0c128e3b-db3b-4e31-b107-0379b5791233` |
| AR | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` |

## UUIDs de Status

| Status | UUID |
|---|---|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

---

## FASE 1 — Planificación (al recibir handoff del PM)

### Paso 1 — Leer Handoff del PM + SPEC v1.9

- `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — fuente de verdad funcional
- `Release2.0/PJM/HO_PJM_PLAN_SPRINTS_MEMORY_SERVICE.md` — calendario y owners
- `.claude/rules/MAPA_DEPENDENCIAS_ENTREGABLES.md` — inputs obligatorios por tarea

### Paso 2 — Crear Tarea en VTT

```bash
export TASK_ID="MS-XXX"   # ID que se asignará después de POST

curl -s -X POST "$BASE/api/phases/{phaseId}/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "[4.X.Y] <Nombre descriptivo>",
    "description": "<max 2000 chars>",
    "priorityId": "<uuid>",
    "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
    "assignedToId": "<UUID_AGENTE>",
    "assignedBy": "'$TL'",
    "category": "development|deployment|documentation|test|infrastructure",
    "complexity": "LOW|MEDIUM|HIGH",
    "estimatedHours": N,
    "createdBy": "'$TL'"
  }'
```

**Gotchas:**
- Usar `assignedToId` NO `assigneeId` (backend ignora silenciosamente este último).
- `complexity` mayúscula obligatoria.
- `priorityId` requiere UUID válido (no string).

### Paso 3 — Crear y Subir BRIEF

**Ubicación local:** `knowledge/agent-tasks/briefs/04-development/S01/BRIEF_MS-XXX_<nombre>.md`

**Estructura mínima del BRIEF:**
1. §1 Contexto y objetivo
2. §2 Alcance (in/out scope)
3. §3 Inputs obligatorios (rutas exactas)
4. §4 Deliverables esperados (paths + estado)
5. §5 Acceptance Criteria (lista numerada CA-01..CA-NN)
6. §6 TrackableItems aplicables (o "Ninguno")
7. §7 Living Documents impactados (o "Sin cambios")
8. §8 Hardcode Check (patrones a verificar)

**Subir como attachment:**

```bash
curl -s -X POST "$BASE/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/briefs/04-development/S01/BRIEF_MS-XXX_nombre.md" \
  -F "fileType=brief" \
  -F "uploadedById=$TL"
```

**Gotcha:** `uploadedById` obligatorio o devuelve 400 silencioso.

---

## FASE 2 — Asignación (al momento de asignar la tarea)

### Paso 4 — Análisis de Dependencias de Datos

> **Regla absoluta:** NO generar ASSIGNMENT sin completar primero este análisis.

Checklist (ver `PROCESO_ANALISIS_DEPENDENCIAS_ASSIGNMENT.md`):

```
[ ] Identifiqué qué documentos fuente necesita el agente
[ ] Tracé cada dependencia a su ruta exacta
[ ] Verifiqué que los documentos existen y están aprobados
[ ] El ASSIGNMENT referenciará rutas exactas en "DOCUMENTOS DE REFERENCIA OBLIGATORIOS"
```

**Lección MS-029..035:** Un assignment sin trazado de dependencias = el agente trabaja en el vacío (perdió ~1M tokens en regeneración).

### Paso 5 — Verificar Dependencias en VTT

```bash
# Confirmar que las tareas upstream están en task_completed o task_approved
curl -s "$BASE/api/tasks/$TASK_ID/dependencies" -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; [print(d.get('dependsOnTaskId'), d.get('dependsOn',{}).get('status',{}).get('code')) for d in json.load(sys.stdin)['data']]"
```

**Si alguna upstream no está completed/approved → no asignar.** Marcar `task_blocked` y notificar.

### Paso 6 — Generar ASSIGNMENT

**Ubicación local:** `knowledge/agent-tasks/assignments/04-development/S01/ASSIGNMENT_MS-XXX_<nombre>.md`

**Usar template:** `00-platform/05.Templates/05.Proyecto/02.Genericos/TEMPLATE_ASIGNACION_TAREARev.md` v3.1

**Secciones obligatorias:**

1. **§1 Objetivo + alcance** — qué construir
2. **§2 DOCUMENTOS DE REFERENCIA OBLIGATORIOS** — rutas exactas (ver Paso 4)
3. **§3 Acceptance Criteria** — los UUIDs reales (a crear en Paso 7)
4. **§4 TrackableItems a vincular** — implements / related_to
5. **§5 Living Documents impactados** — declarar incluso si "sin cambios"
6. **§6 Workflow del agente** — 15 pasos (manifest AL FINAL)
7. **§7 Hardcode Check** — patrones específicos a buscar
8. **§8 Tech debts e items detectados** — sección obligatoria para el SKL-REPORT-01

**Sección crítica (Tech debts del reporte SKL-REPORT-01):**

El ASSIGNMENT debe incluir esta tabla vacía para que el agente la rellene al cerrar:

```markdown
### Tech debts detectados durante la ejecución

| Código sugerido | Descripción | Urgencia | ¿Retroactivo? |
|---|---|---|---|
| (a llenar por el agente) | | | |

### Items detectados para trackeo (TL revisar)

| Tipo sugerido | Código sugerido | Descripción | Urgencia |
|---|---|---|---|
| (a llenar por el agente) | | | |
```

**Subir ASSIGNMENT:**

```bash
curl -s -X POST "$BASE/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/assignments/04-development/S01/ASSIGNMENT_MS-XXX_nombre.md" \
  -F "fileType=assignment" \
  -F "uploadedById=$TL"
```

### Paso 7 — Crear Acceptance Criteria en VTT

Por cada CA del ASSIGNMENT:

```bash
curl -s -X POST "$BASE/api/tasks/$TASK_ID/criteria" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CA-01: <descripcion corta>",
    "description": "<criterio detallado y como verificarlo>",
    "criteriaTypeCode": "acceptance",
    "required": true
  }'
```

**Gotchas:**
- Campo es `criteriaTypeCode`, NO `type`.
- Endpoint es `/criteria`, NO `/acceptance-criteria` (este devuelve 404).
- Guardar los UUIDs devueltos para incluirlos en el ASSIGNMENT (referenciables por el agente).

**Script para crear varios a la vez:**

```python
import urllib.request, json, os
cas = [
    ("CA-01: ...", "evidencia ..."),
    ("CA-02: ...", "evidencia ..."),
    # ...
]
for title, desc in cas:
    body = {"title": title, "description": desc, "criteriaTypeCode": "acceptance", "required": True}
    req = urllib.request.Request(f"{BASE}/api/tasks/{TASK_ID}/criteria",
        data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type':'application/json'},
        method='POST')
    r = json.loads(urllib.request.urlopen(req).read())
    print(f"  {title[:30]}: {r['data']['id']}")
```

### Paso 8 — Vincular TrackableItems

Si la tarea implementa o se relaciona con TIs existentes (RFs, NFRs, ADRs, Assumptions):

```bash
# Localizar UUID del TI por código
curl -s "$BASE/api/projects/$PROJECT_ID/trackable-items?code=NFR-SEC-05" \
  -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; print(json.load(sys.stdin)['data'][0]['id'])"

# Vincular a la tarea
curl -s -X POST "$BASE/api/trackable-items/$TI_ID/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"taskId":"'$TASK_ID'","linkType":"implements"}'
```

**linkType válidos:**
- `implements` — la tarea cumple/realiza el TI (ej: NFR-SEC-04 = "sin stack en prod" + tarea de error handler)
- `related_to` — la tarea está relacionada pero no lo implementa directamente (ej: AS-001 = "VM Hetzner")
- `depends_on` — la tarea depende del TI
- `blocks` — la tarea bloquea el TI

**Si el TI ya está linked:** devuelve 409 "already linked" (esperado y benigno).

### Paso 8.5 — Crear execution_manifest de la tarea (NUEVO v2.1)

> Aplica desde adopción de worktrees por rol (`VTT.PROTOCOL-WT-001`).
> El manifest declara qué agente trabaja, en qué worktree, con qué archivos permitidos.
> El agente lee este manifest al arrancar la tarea.

```bash
# 1. Copiar template
cp .vtt/manifests/_template.execution.json .vtt/manifests/$TASK_ID.execution.json

# 2. Editar campos críticos:
#    - taskId: MS-XXX
#    - title: copiar del BRIEF
#    - agents[]: dejar solo el rol que ejecutará (BE, DO, DB, QA, etc.)
#    - agents[0].agentUuid: UUID del rol (de la tabla de equipo arriba)
#    - agents[0].branch: feature/MS-XXX
#    - agents[0].assignedWorkdir: .vtt/worktrees/<repo>-<rol-lower>
#    - agents[0].allowedPaths: paths que el agente puede tocar (del BRIEF §3)
#    - agents[0].deniedPaths: .env*, .vtt/**, node_modules/**
#    - agents[0].expectedOutputs: paths esperados de reports/diffs
```

**Para tareas que tocan múltiples repos** (raro pero pasa):
```bash
# Agregar entradas adicionales en agents[]
# Ejemplo: BE toca backend (código) + project (devlog/docs)
{
  "agents": [
    { "agentId": "BE", "repoId": "backend", "assignedWorkdir": ".vtt/worktrees/backend-be", ... },
    { "agentId": "BE", "repoId": "project", "assignedWorkdir": ".vtt/worktrees/backend-be-docs", ... }
  ]
}
# Si necesita un worktree adicional, crearlo:
#   cd memory-service-project
#   git worktree add ../.vtt/worktrees/backend-be-docs -b wt-backend-be-docs origin/main
```

**Validación rápida:**
```bash
python -m json.tool .vtt/manifests/$TASK_ID.execution.json   # parse OK
```

El manifest queda disponible para:
- El agente al leer su mensaje (lo referencia)
- El TL Reviewer en FASE A Paso 5b (validar diff vs allowedPaths)

### Paso 9 — Generar Mensaje al Agente

**Skill: SKL-MESSAGE-01**

```bash
# Genera y publica como comment en VTT
python scripts/gen_mensaje.py $TASK_ID --post
```

El script auto-detecta:
- Agente asignado (de `task.assignedToId`)
- Sprint y posición dentro del sprint
- CAs creados (los lista en el mensaje)
- Paths del BRIEF y ASSIGNMENT
- Comandos de arranque (JWT + move to in_progress)
- Referencia a SKL-MANIFEST-01

También guarda el mensaje localmente en `knowledge/agent-tasks/messages/04-development/S01/MENSAJE_MS-XXX.md`.

**Si `--post` falla** (rate limit, comment too long), correr sin flag y pegar manualmente:
```bash
python scripts/gen_mensaje.py $TASK_ID > /tmp/msg.md
# Copiar contenido y postear como comment manualmente
```

---

## Decisión punto de control

Después del Paso 9, la tarea está oficialmente asignada. El agente la verá en sus tareas y comenzará trabajo.

**Si necesitas pausar:**

```bash
# Mover a task_on_hold
curl -s -X PATCH "$BASE/api/tasks/$TASK_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "statusId": "c62eb334-b7bc-4c9f-af85-a5666c262aaa",
    "changedBy": "'$TL'",
    "reason": "<motivo en 1 linea>"
  }'
```

---

## Workflow del Agente (informativo para TL)

El TL Ejecutor no ejecuta estos pasos, pero los conoce porque están en el ASSIGNMENT (§6) y el agente los seguirá:

| # | Paso del agente |
|---|---|
| 0 | Crear branch `feature/MS-XXX` desde `main` (o desde tarea upstream si no está en main) |
| 1 | Mover tarea a `task_in_progress` |
| 2 | Leer BRIEF completo |
| 3 | Leer documentos de referencia listados en §2 del ASSIGNMENT |
| 4 | Verificar prerequisitos (servicios, BD, dependencias) |
| 5 | Implementar archivos según especificación |
| 6 | Crear archivos `.LOGIC.md` (uno por archivo TS/JS producido) |
| 7 | Probar localmente |
| 8 | Testing manual de escenarios del BRIEF |
| 9 | Registrar devlog entries (decisiones, observaciones, tech_debt) |
| 10 | Reportar cumplimiento de CAs (`PATCH /criteria/:cid`) |
| 11 | Commit y push |
| 12 | Crear PR(s) con `gh pr create` |
| 13 | Verificar Review Gate + mover a `task_in_review` |
| 14 | Subir attachments (devlog, code_logic) a VTT |
| 15 | Reportar al TL con SKL-REPORT-01 (estructurado, todas las secciones del modelo dinámico) |

---

## Errores comunes y cómo evitarlos

| Error | Síntoma | Solución |
|---|---|---|
| `assigneeId` ignorado | Tarea queda sin asignar | Usar `assignedToId` |
| 400 silencioso en attachment | Sin error claro | Verificar `uploadedById` en form |
| `type` en CA → 404 | Endpoint no acepta payload | Usar `criteriaTypeCode` |
| `/acceptance-criteria` 404 | Endpoint incorrecto | Usar `/criteria` |
| ASSIGNMENT sin dependencias | Agente trabaja en el vacío | Completar Paso 4 SIEMPRE |
| `gen_mensaje.py --post` falla | Rate limit o comment too long | Postear manualmente |
| TI ya linked → 409 | Vinculación duplicada | Ignorar, es benigno |
| Tarea creada sin BRIEF | Agente no tiene contexto | Subir BRIEF inmediatamente después del POST |
| Manifest generado por el agente prematuramente | Campos null en delivery | Documentar en ASSIGNMENT que el manifest es del TL |

---

## Tiempos estimados

| Fase | Tiempo |
|---|---|
| FASE 1 — Planificación (Pasos 1-3) | 15-20 min |
| FASE 2 — Asignación (Pasos 4-9) | 15-25 min |
| **Total por tarea** | **30-45 min** |

---

## Atajos prácticos

### Asignación de varias tareas en paralelo

Si vas a asignar 2+ tareas a la vez (independientes), procesa cada una hasta Paso 8 y bulk-postea los mensajes con `gen_mensaje.py --post` al final.

### Cadenas de dependencias

Si MS-Y depende de MS-X y MS-X aún no está en `task_completed`:
- NO asignar MS-Y todavía
- Marcar como `task_blocked` en VTT
- El TL Reviewer al cerrar MS-X notificará cuáles tareas se desbloquean

### Si quieres delegarme la generación

Dime: `genera assignment para MS-XXX` y yo:
1. Leo el BRIEF y el handoff
2. Verifico dependencias (Paso 4-5)
3. Genero ASSIGNMENT con CAs propuestos y trackable items detectados
4. Te muestro el draft para que valides antes de crear CAs y subir

### Si quieres revisar un ASSIGNMENT antes de asignar

Pídeme `valida assignment MS-XXX` y reviso checklist completo:
- Dependencias trazadas
- CAs claros y verificables
- TIs heredados identificados
- Workflow del agente actualizado a v3 (15 pasos)
- Sección "Tech debts detectados" presente

---

## Documentos de referencia

| Doc | Para qué sirve |
|---|---|
| `PROCESO_ASIGNACION_TAREAS_v3.md` | Workflow completo 16 pasos (asignación + cierre) |
| `PROCESO_ANALISIS_DEPENDENCIAS_ASSIGNMENT.md` | Análisis obligatorio del Paso 4 |
| `MAPA_DEPENDENCIAS_ENTREGABLES.md` | Inputs por tarea según fase |
| `TEMPLATE_ASIGNACION_TAREARev.md` v3.1 | Template del ASSIGNMENT |
| `SKL-MESSAGE-01_*.md` | Skill operativa del Paso 9 |
| `OPERATIVO_TL_MEMORY-SERVICE.md` | Operativo del rol TL Ejecutor |
| `GUIA_REVISION_TAREA_TL_REVIEWER.md` | Guía hermana — qué pasa al CERRAR |
| `reference_vtt_endpoints_cheatsheet.md` (memoria) | Cheatsheet endpoints + gotchas |
