# Guía operativa — Revisión de tarea (TL Reviewer)

**Versión:** 1.0
**Fecha:** 2026-05-14
**Aplicable a:** TL Reviewer Memory Service
**Tiempo estimado por tarea:** 20-30 min

Cheatsheet completo del `PROCESO_CIERRE_TAREA_v2.md` aterrizado a pasos concretos con comandos curl listos para pegar.

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

export TASK_ID="MS-XXX"   # cambiar por la tarea a revisar
```

---

## FASE A — Verificación (5-10 min)

### Paso 1 — Leer el reporte SKL-REPORT-01 del agente

```bash
# Buscar el comment de entrega del agente
curl -s "$BASE/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; [print(c['id'][:8],c['userId'][:8],c['message'][:80].replace(chr(10),' ')) for c in json.load(sys.stdin)['data']]"
```

O leer el archivo si el agente lo guardó: `knowledge/agent-tasks/reports/MS-XXX_REPORT.md`

### Paso 2 — Estado de la tarea

```bash
curl -s "$BASE/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; d=json.load(sys.stdin)['data']; print(f\"status: {d['status']['code']}\")"
```

**Esperado:** `task_in_review`. Si no, pedir al agente que la mueva.

### Paso 3 — Acceptance Criteria

```bash
curl -s "$BASE/api/tasks/$TASK_ID/criteria" -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; d=json.load(sys.stdin)['data']; print(f\"{sum(1 for c in d if c['status']=='met')}/{len(d)} met\")"
```

**Esperado:** todos `met`. Si hay alguno `pending`, leer el CA y validar contra el reporte.

### Paso 4 — Review Gate

```bash
curl -s "$BASE/api/tasks/$TASK_ID/review-gate" -H "Authorization: Bearer $TOKEN" | \
  python -m json.tool
```

**Esperado:** `canProceedToReview: true`, `blockers: []`. Warnings `low` no bloquean.

### Paso 5 — Attachments (verificar entregables)

```bash
curl -s "$BASE/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; print([a['fileType'] for a in json.load(sys.stdin)['data']])"
```

**Mínimo esperado:** `['brief', 'assignment', 'devlog', 'code_logic', 'manifest']`

### Paso 6 — PRs en GitHub

```bash
# Buscar PRs de la tarea
gh pr list --repo NCoreSys/memory-service-backend --search "$TASK_ID" --state all --json number,url,state,mergeable
gh pr list --repo NCoreSys/memory-service-project --search "$TASK_ID" --state all --json number,url,state,mergeable
```

**Esperado:** state=OPEN mergeable=MERGEABLE (o MERGED si ya hicieron merge).

### Paso 7 — Devlog entries (para FASE B)

```bash
curl -s "$BASE/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; [print(d['id'][:8], d.get('categoryCode','?'), d.get('status','?'), d['title'][:60]) for d in json.load(sys.stdin)['data']]"
```

Guarda esta lista. Los marcarás `resolved` en el Paso 11.

---

## Decisión punto de control

Después de FASE A, tienes 3 caminos:

| Estado | Acción |
|---|---|
| Todo verde + reporte claro | **Continuar a FASE B** (cierre normal) |
| CAs incompletos o gate rojo | **Rechazar**: `PATCH status → task_rejected` con feedback en comment, regresa al agente |
| Reporte ambiguo / dato faltante | **on_hold**: `PATCH status → task_on_hold`, crear ISSUE, escalar a PM |

---

## FASE B — Modelo Dinámico (10-15 min)

> Skill: `SKL-DYNAMIC-MODEL-01_cierre-modelo-dinamico.md`

### Paso 8 — Identificar items detectados por el agente

Del reporte del agente lee:

- **"Items detectados para trackeo (TL revisar)"** → cada fila se vuelve un TI nuevo
- **"Findings / Deuda técnica"** → si menciona algo no listado en la tabla anterior, también es TI nuevo
- **"TrackableItems creados o vinculados"** → estos son los **heredados** (ya vinculados); les agregas evidencias en Paso 10

### Paso 9 — Crear TIs nuevos

Por cada item detectado:

```bash
curl -s -X POST "$BASE/api/projects/$PROJECT_ID/trackable-items" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "DEBT-XXX-NN",
    "title": "[DEFER R2] <titulo descriptivo>",
    "description": "[Deferred to R2] <descripcion completa con contexto>",
    "typeCode": "tech_debt",
    "statusCode": "ti_draft",
    "createdById": "'$TL'"
  }' | python -c "import sys,json; print('TI id:', json.load(sys.stdin)['data']['id'])"
```

**Reglas de codificación de TI:**

- Tech debt técnico: `DEBT-<área>-<NN>` (DEBT-DOCKER-01, DEBT-INFRA-VTT-02)
- Mejora de proceso: `PROC-<área>-<NN>` + `[PROCESS]` marker en title
- Issue de documentación: `DOC-<área>-<NN>`

**Vincular el TI nuevo a la tarea:**

```bash
curl -s -X POST "$BASE/api/trackable-items/$TI_ID/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"taskId":"'$TASK_ID'","linkType":"related_to"}'
```

### Paso 10 — Agregar evidencias a TIs (heredados + nuevos)

Por cada TI vinculada × cada PR del entregable:

```bash
curl -s -X POST "$BASE/api/trackable-items/$TI_ID/evidence" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "link",
    "title": "[MS-XXX] [S1] <descripcion corta>",
    "url": "https://github.com/NCoreSys/memory-service-backend/pull/N",
    "description": "[TASK:MS-XXX] [SPRINT:S1] <descripcion completa con paths/numeros>",
    "createdById": "'$TL'"
  }'
```

**Reglas del marker (obligatorio):**

- `title`: empieza con `[MS-XXX] [SX]`
- `description`: empieza con `[TASK:MS-XXX] [SPRINT:SX]`
- `url`: PR específico (`.../pull/N`), no URL base
- `type`: `document | link | test_result | screenshot` (NO `pr`)

**Tipos sugeridos:**

- `link` → PR de GitHub
- `document` → spec/doc en project repo
- `test_result` → coverage Jest/output de tests
- `screenshot` → captura de pantalla

### Paso 11 — Resolver devlog entries

Por cada entry no resuelto:

```bash
curl -s -X PATCH "$BASE/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "resolution": "Revisado por TL durante cierre '$TASK_ID'. <accion tomada o decision aceptada>"
  }'
```

**`resolution` es REQUERIDO** (sin él → 400 VALIDATION_ERROR).

**Plantillas de resolution según categoría:**

- `decision` → "Decisión consolidada al cierre formal de la tarea. Incorporada al manifest."
- `tech_debt` → "Promovido a TI <CODIGO-TI> con marker [DEFER R2]."
- `observation` → "Observación incorporada al manifest. Sin acción correctiva inmediata."
- `testing_note` → "Resultado de testing validado. Métricas registradas en manifest."

---

## FASE C — Cierre Formal (5 min)

### Paso 12 — APR-TL Comment

Template del comment (adaptar a la tarea):

```markdown
## APR-TL: MS-XXX aprobado por TL Reviewer

**Code review segun PROCESO_CIERRE_TAREA_v2 (FASE A + B + C):**

### FASE A — Verificacion
- [x] Review Gate: canProceedToReview=true (0 blockers, N warnings)
- [x] CAs: N/N met con evidencia
- [x] Devlog: N entries — todos resueltos al cierre
- [x] Attachments: brief + assignment + devlog + code_logic + manifest
- [x] PRs: backend #N + project #M
- [x] TIs heredados: <CODIGO> (implements), <CODIGO> (related_to)
- [x] LD-XX declarado <sin cambios | actualizado>

### Verificacion tecnica manual
- [x] <Verificación específica de la tarea 1>
- [x] <Verificación específica de la tarea 2>

### FASE B — Modelo dinamico aplicado
- N TIs nuevos creados y marcados [DEFER R2]:
  - <CODIGO-1> (<tipo>): <descripcion>
  - <CODIGO-2> (<tipo>): <descripcion>
- N evidencias agregadas a N TIs con marker [TASK:MS-XXX] [SPRINT:SX]
- N devlog entries marcados resolved

### Veredicto
APROBADO. Tarea movida a task_completed. Pendiente aprobacion terminal PM.
```

```bash
curl -s -X POST "$BASE/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"<el texto del APR-TL>\",\"userId\":\"$TL\"}"
```

**Límite:** 5000 chars. Si excede, dividir o subir como attachment.

### Paso 13 — Status → task_completed

```bash
curl -s -X PATCH "$BASE/api/tasks/$TASK_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97",
    "changedBy": "'$TL'",
    "reason": "APR-TL: aprobado tras code review FASE A+B+C + modelo dinamico"
  }'
```

### Paso 14 — Generar Manifest v1.5

> Skill: `SKL-MANIFEST-01_generar-manifest.md`
>
> **Regla crítica:** este paso va AL FINAL, después del status change. Si lo haces antes, quedan campos `null` en `delivery`.

Si el agente ya generó manifest v1.0, lo reescribes a v1.5 agregando:

- `delivery.dynamic_model_actions` (TIs creados, evidencias agregadas, devlog resueltos)
- `review.tl_review` con verdict, verifications, notes
- `delivery.how_to_verify` con comandos curl
- `delivery.skl_report_01_full` con el texto literal del comment del agente

Archivos a generar/actualizar:

- `knowledge/task-manifests/04-development/S01/MS-XXX.json`
- `knowledge/task-manifests/04-development/S01/MS-XXX.manifest.md` (wrapper)

Subir el `.md` como `fileType=manifest`:

```bash
curl -s -X POST "$BASE/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/task-manifests/04-development/S01/MS-XXX.manifest.md" \
  -F "fileType=manifest" \
  -F "uploadedById=$TL" \
  -F "description=Manifest MS-XXX v1.5 - review.tl_review COMPLETADO. Modelo dinamico."
```

### Paso 15 — Validación final

```bash
# Status correcto
curl -s "$BASE/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; print('status:', json.load(sys.stdin)['data']['status']['code'])"
# Esperado: task_completed

# Devlog: 0 pending
curl -s "$BASE/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" | \
  python -c "import sys,json; d=json.load(sys.stdin)['data']; print('not resolved:', sum(1 for x in d if x.get('status')!='resolved'))"
# Esperado: 0

# Evidencias con marker
for TI_ID in <uuids>; do
  curl -s "$BASE/api/trackable-items/$TI_ID/evidence" -H "Authorization: Bearer $TOKEN" | \
    python -c "import sys,json; d=json.load(sys.stdin)['data']; print('  marker count:', sum(1 for e in d if '[TASK:'+'$TASK_ID'+']' in (e.get('description') or '')))"
done
# Esperado: >=1 por TI
```

---

## Tiempos estimados

| Fase | Tiempo |
|---|---|
| A — Verificación | 5-10 min |
| B — Modelo dinámico | 10-15 min |
| C — Cierre formal | 5 min |
| **Total por tarea** | **20-30 min** |

---

## Atajos prácticos

### Si quieres delegarme el cierre completo

Solo dime: `cierra MS-XXX` y yo:

1. Leo el reporte (comment del agente o archivo en `knowledge/agent-tasks/reports/`)
2. Genero un script Python que ejecuta FASE A + B + C completas
3. Te muestro el resumen con los IDs de TIs creados, evidencias, manifest

### Si quieres revisar manualmente algo antes de cerrar

Pídeme `verifica MS-XXX` y solo corro FASE A, te muestro hallazgos, y decides si cerramos o rechazamos.

### Si quieres aprobación terminal PM (task_approved)

Es un paso adicional **del PM**, no del TL. Cambia status a `task_approved` (UUID `b9ca4951-6e14-4d82-b1d8-440793bbaf47`). Te puedo armar el comando si lo necesitas.

---

## Documentos de referencia

| Doc | Para qué sirve |
|---|---|
| `PROCESO_CIERRE_TAREA_v2.md` | Workflow completo detallado |
| `SKL-DYNAMIC-MODEL-01_*.md` | Skill operativa de Paso 8-11 |
| `SKL-MANIFEST-01_*.md` | Skill operativa de Paso 14 |
| `reference_vtt_modelo_dinamico_endpoints.md` (memoria) | Cheatsheet endpoints + gotchas |
| `VTT_PLATFORM_GAPS_2026-05-13.md` | Gaps de feature backend VTT |
