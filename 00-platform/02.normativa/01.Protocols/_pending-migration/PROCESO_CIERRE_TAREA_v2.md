# PROCESO DE CIERRE DE TAREA — Modelo Dinámico aplicado (v2)

**Versión:** 2.0
**Fecha:** 2026-05-13
**Aplicable a:** TL Reviewer (Memory Service y futuros proyectos)
**Reemplaza:** versión 1.x del PROCESO_ASIGNACION_TAREAS (sección cierre)
**Razón del cambio:** Aplicar las features del modelo dinámico (TIs, evidencias, devlog status) que estaban documentadas en SOPs pero no integradas al workflow operativo del TL Reviewer.

---

## Resumen del cambio

Antes (v1.x) el cierre de tarea se limitaba a:
1. Verificar Review Gate + CAs
2. Postear APR-TL
3. Mover a `task_completed`
4. Actualizar manifest

Resultado: las features del modelo dinámico quedaban **sin uso real**:
- Tech debts del reporte del agente → solo en manifest JSON
- Tab "EVIDENCIAS" de cada TI → vacío
- Devlog entries → quedaban en `pending` para siempre
- Notas/findings → texto libre del comment

Ahora (v2.0) el cierre incluye **4 pasos del modelo dinámico** entre la verificación y el APR-TL.

---

## Diagrama del flujo completo

```
┌────────────────────────────────────────────────────────────────────┐
│  TAREA EN task_in_review                                            │
│  (entregada por el agente con SKL-REPORT-01)                        │
└─────────────────────────┬──────────────────────────────────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  FASE A — VERIFICACIÓN      │
            │  (Pasos 1-4 del v1)         │
            └─────────────┬───────────────┘
                          │
                          ▼
   ┌─────────────────────────────────────────────────────┐
   │  FASE B — MODELO DINÁMICO (NUEVO en v2)             │
   │                                                      │
   │  Paso 5.1 — Crear TIs detectados por el agente      │
   │  Paso 5.2 — Agregar evidencias a TIs vinculadas     │
   │  Paso 5.3 — Resolver devlog entries                  │
   │  Paso 5.4 — Registrar acciones en manifest          │
   │                                                      │
   │  Skill: SKL-DYNAMIC-MODEL-01                         │
   └─────────────────────┬───────────────────────────────┘
                         │
                         ▼
            ┌─────────────────────────────┐
            │  FASE C — CIERRE FORMAL     │
            │  (Pasos 6-8)                 │
            └─────────────┬───────────────┘
                          │
                          ▼
        ┌────────────────────────────────────────┐
        │  TAREA EN task_completed                │
        │  Pendiente solo aprobación PM           │
        └────────────────────────────────────────┘
```

---

## FASE A — Verificación (Pasos 1-4)

### Paso 1 — Review Gate

```bash
curl -s "$BASE/api/tasks/$TASK_ID/review-gate" -H "Authorization: Bearer $TOKEN" | jq
```

**Criterio:** `canProceedToReview: true`, `blockers: []`. Warnings `low` no bloquean.

Si no pasa → devolver con feedback al agente, NO cerrar.

### Paso 2 — Acceptance Criteria

```bash
curl -s "$BASE/api/tasks/$TASK_ID/criteria" -H "Authorization: Bearer $TOKEN" | jq '.data | map({title, status})'
```

**Criterio:** todas las CAs requeridas en `status=met` con evidencia válida.

### Paso 3 — Attachments

```bash
curl -s "$BASE/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" | jq '.data | map({fileType, fileName, fileSize})'
```

**Mínimo:** brief, assignment, devlog, code_logic (o placeholder si N/A), manifest.

### Paso 4 — PRs en GitHub

```bash
gh pr view $PR_NUMBER --repo NCoreSys/memory-service-backend --json state,mergeable,url
```

**Criterio:** state=OPEN, mergeable=MERGEABLE (sin conflictos).

### Paso 4b — Verificar disciplina de worktree (NUEVO v2.1)

> Aplica desde adopción de worktrees por rol (`VTT.PROTOCOL-WT-001`).

**Verifica 3 cosas:**

1. **El agente trabajó en su worktree** (no en el clon base):
```bash
WORKTREE=".vtt/worktrees/backend-be"   # ajustar al rol del agente
cd $WORKTREE
git log --oneline -3                    # debe mostrar commits feature/$TASK_ID

cd ../../../memory-service-backend      # clon base
git status                              # debe estar en main, clean (sin tocar)
```

2. **El diff respeta `allowedPaths` del execution_manifest:**
```bash
# Si existe el manifest de la tarea
test -f .vtt/manifests/$TASK_ID.execution.json && \
  echo "allowedPaths declarados:" && \
  python -c "import json; print(json.load(open('.vtt/manifests/$TASK_ID.execution.json'))['agents'][0]['allowedPaths'])"

# Comparar con archivos modificados en el PR
gh pr view $PR_NUMBER --repo NCoreSys/memory-service-backend --json files -q '.files[].path'
```

3. **No hay cross-contamination con otros worktrees:**
```bash
cd memory-service-backend
git worktree list                       # cada worktree en su branch propia, sin sorpresas
```

**Banderas rojas que bloquean el cierre:**
- Clon base con cambios sin commitear → agente trabajó en lugar incorrecto
- Diff toca archivos fuera de `allowedPaths` → escalar a TL Ejecutor
- Branch desaparecida del worktree del agente → algo se rompió

---

## FASE B — Modelo Dinámico (Pasos 5.1-5.4) — **NUEVO**

> **Skill:** `00-platform/06.Skills/dynamic-model/SKL-DYNAMIC-MODEL-01_cierre-modelo-dinamico.md`
>
> **Input:** Reporte SKL-REPORT-01 del agente, secciones:
> - **Tech debts detectados** → crear TIs (Paso 5.1)
> - **Items detectados para trackeo** → crear TIs (Paso 5.1)
> - **TrackableItems creados o vinculados** → agregar evidencias (Paso 5.2)
> - **Devlog entries registrados** → resolver (Paso 5.3)
> - **PRs y commits** → evidencias con marker (Paso 5.2)

### Paso 5.1 — Crear TIs detectados

Por cada item del reporte:

```bash
curl -s -X POST "$BASE/api/projects/$PROJECT_ID/trackable-items" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "DEBT-XXX-NN",
    "title": "[PROCESS]/[DEFER R2] <titulo>",
    "description": "[Subtype: process_improvement] [Deferred to R2] <descripcion>",
    "typeCode": "tech_debt",
    "statusCode": "ti_draft",
    "createdById": "<TL_UUID>"
  }'
```

**Constraints conocidos:**
- Solo `typeCode={adr,assumption,business_rule,constraint,rf,rnf,tech_debt,use_case,user_story}` es válido para projectType=software.
- `process_improvement` NO permitido → usar `tech_debt` + `[PROCESS]` marker.
- Status `ti_deferred` NO existe → marker `[DEFER R2]` textual.
- Endpoint `/defer` NO existe → no llamar.

**Vincular a la tarea cerrada:**
```bash
curl -s -X POST "$BASE/api/trackable-items/$TI_ID/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"taskId":"MS-XXX","linkType":"related_to"}'
```

### Paso 5.2 — Agregar evidencias a TIs vinculadas

Para cada TI vinculada (heredada + nueva), una evidencia por cada PR:

```bash
curl -s -X POST "$BASE/api/trackable-items/$TI_ID/evidence" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "link",
    "title": "[MS-XXX] [S1] <descripcion corta>",
    "url": "https://github.com/.../pull/N",
    "description": "[TASK:MS-XXX] [SPRINT:S1] <descripcion completa>",
    "createdById": "<TL_UUID>"
  }'
```

**Formato OBLIGATORIO del marker:**
- `title`: `[MS-XXX] [SX] <descripción corta>`
- `description`: `[TASK:MS-XXX] [SPRINT:SX] <descripción completa>`
- `url`: PR específico (no URL base)

**Enum válidos para `type`:** `document | link | test_result | screenshot` (NO `pr`).

**Endpoint singular `/evidence`** (no `/evidences`).

**No hay DELETE** → leer 2 veces antes de POST.

### Paso 5.3 — Resolver devlog entries

```bash
# Listar entries de la tarea
curl -s "$BASE/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" | jq '.data[] | {id, title, status, categoryCode}'

# Por cada entry no resuelto:
curl -s -X PATCH "$BASE/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "resolution": "Revisado por TL durante cierre MS-XXX. Entry tipo <cat> incorporada al manifest."
  }'
```

**`resolution` es REQUERIDO** cuando status=`resolved` o `wont_fix`. Sin él → 400 VALIDATION_ERROR.

**Status válidos:** `pending | acknowledged | in_progress | resolved | deferred | wont_fix`.

### Paso 5.4 — Registrar acciones en manifest

Bloque `delivery.dynamic_model_actions` en el JSON del manifest:

```json
{
  "delivery": {
    "dynamic_model_actions": {
      "new_tis_created": [
        {"code": "DEBT-XXX-NN", "id": "<uuid>", "linked_as": "related_to MS-XXX"}
      ],
      "evidences_added": [
        {"ti_code": "NFR-SEC-05", "type": "link", "title": "[MS-XXX] [S1] ..."}
      ],
      "devlog_resolved_count": 6,
      "note_defer_endpoint_missing": "POST /trackable-items/:id/defer NO existe...",
      "note_typecode_constraint": "Software acepta solo tech_debt..."
    }
  }
}
```

---

## FASE C — Cierre Formal (Pasos 6-8)

### Paso 6 — APR-TL Comment

```bash
curl -s -X POST "$BASE/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"## APR-TL: ... [include resumen FASE B]","userId":"<TL_UUID>"}'
```

El comment debe incluir sección **"Acciones aplicadas al cerrar (modelo dinámico)"** con resumen de TIs creados, evidencias agregadas y devlog resueltos.

### Paso 7 — Status → task_completed

```bash
curl -s -X PATCH "$BASE/api/tasks/$TASK_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97",
    "changedBy": "<TL_UUID>",
    "reason": "APR-TL: aprobado tras code review + modelo dinamico aplicado"
  }'
```

### Paso 8 — Manifest v1.5 (actualizar v1.0 del agente)

> Skill: `SKL-MANIFEST-01_generar-manifest.md` — PARTE B
>
> **Precondición:** El agente generó v1.0 al cerrar SU workflow (paso 15 del agente). Está en disco como `knowledge/task-manifests/[fase]/[sprint]/MS-XXX.json` y subido a VTT como `fileType=manifest`.
>
> **Tu trabajo (TL):** NO regenerar desde cero. **Actualizar** v1.0 → v1.5 agregando los bloques del cierre.

**Cambios v1.0 → v1.5:**

| Campo | v1.0 (agente) | v1.5 (TL) |
|---|---|---|
| `task.current_status` | `"task_in_review"` | `"task_completed"` |
| `last_updated_block` | `"delivery"` | `"review.tl_review + delivery.dynamic_model_actions"` |
| `delivery.dynamic_model_actions` | (no existe) | **NUEVO bloque** con TIs nuevos, evidencias agregadas, devlog resueltos |
| `delivery.devlog_summary.all_resolved_by_tl` | `false` | `true` |
| `delivery.trackable_items_actual.related_to` | TIs heredados | + TIs nuevos creados en FASE B |
| `delivery.tech_debt_for_r2[].ti_id` | (no incluido aún) | UUIDs reales de los TIs creados |
| `delivery.how_to_verify` | (lo que dejó el agente) | (puede enriquecer con más comandos curl) |
| `review.tl_review` | `null` | **NUEVO objeto** con verdict, verifications, notes |

**Pasos operativos:**

1. Leer `knowledge/task-manifests/04-development/S01/MS-XXX.json` (v1.0 del agente)
2. Modificar campos en memoria (ver tabla arriba)
3. Reescribir JSON local
4. Regenerar wrapper `MS-XXX.manifest.md` con header "v1.5"
5. Subir como NUEVO attachment `fileType=manifest` (el v1.0 sigue existiendo, queda como historial)

**Subir:**
```bash
curl -s -X POST "$BASE/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/task-manifests/04-development/S01/MS-XXX.manifest.md" \
  -F "fileType=manifest" \
  -F "uploadedById=<TL_UUID>" \
  -F "description=Manifest MS-XXX v1.5 - review.tl_review COMPLETADO. Modelo dinamico aplicado."
```

**Si el agente NO generó v1.0** (omisión del paso 15 del agente):
- Construir el manifest desde cero leyendo VTT directamente (patrón usado en MS-284/285 retroactivos)
- Documentar la omisión en `generation_note`: "v1.0 omitido por el agente — reconstruido por TL al cerrar"
- Registrar como devlog `observation` para tracking del proceso

### Paso 9 — Cleanup branch local en worktree (NUEVO v2.1)

> Aplica solo después de que el PR esté **mergeado en GitHub** (lo hace el PM).
> Deja el worktree del agente limpio para su próxima tarea.

```bash
WORKTREE=".vtt/worktrees/backend-be"   # ajustar al rol del agente
cd $WORKTREE

# 1. Actualizar main local con el merge del PR
git checkout main
git pull origin main

# 2. Borrar branch local de la tarea (ya está mergeada en GitHub)
git branch -d feature/$TASK_ID

# 3. Verificar estado limpio
git status                              # On branch main, working tree clean
git log --oneline -1                    # último commit es el squash merge del PR

# 4. (Opcional) Archivar execution_manifest
mkdir -p ../../.vtt/manifests/_archived
mv ../../.vtt/manifests/$TASK_ID.execution.json \
   ../../.vtt/manifests/_archived/
```

**Si `git branch -d` falla** ("branch not fully merged"):
- Investigar antes de forzar. Puede haber commits no pusheados.
- Si confirmas vía `gh pr view` que el merge fue squash: `git branch -D feature/$TASK_ID`

---

## Validación final antes de avisar al PM

```bash
# 1. Status
curl -s "$BASE/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" | jq '.data.status.code'
# Esperado: "task_completed"

# 2. Devlog: todos resolved
curl -s "$BASE/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.status != "resolved")) | length'
# Esperado: 0

# 3. Evidencias en TIs (cada una >=1 con marker [TASK:MS-XXX])
for TI_ID in <uuids>; do
  curl -s "$BASE/api/trackable-items/$TI_ID/evidence" -H "Authorization: Bearer $TOKEN" | \
    jq --arg t "$TASK_ID" '.data | map(select(.description | contains("[TASK:" + $t + "]"))) | length'
done

# 4. Manifest última versión incluye review.tl_review.verdict=approved
curl -s "$BASE/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.fileType=="manifest")) | sort_by(.createdAt) | last | .id'
```

---

## Tiempo estimado por cierre

| Fase | Tiempo |
|---|---|
| FASE A — Verificación | 5-10 min |
| FASE B — Modelo dinámico | 10-15 min |
| FASE C — Cierre formal | 5 min |
| **Total** | **20-30 min** |

---

## Errores comunes y cómo evitarlos

| Error | Síntoma | Solución |
|---|---|---|
| `POST /evidences` 404 | Plural en URL | Usar singular `/evidence` |
| `type: "pr"` rechazado | Enum inválido | Usar `link` para PRs |
| Devlog resolve 400 | Falta `resolution` | Agregar texto en `resolution` |
| `process_improvement` rechazado | typeCode inválido software | Usar `tech_debt` + `[PROCESS]` marker |
| `/defer` 404 | Endpoint no existe | Marker `[DEFER R2]` textual |
| Evidencia duplicada visible | No hay DELETE | Aceptar y agregar la correcta |
| Manifest con `null` en delivery | Agente lo generó antes del paso 14 de su workflow | Recordarle que manifest v1.0 va AL FINAL (después de attachments + status + PRs + SKL-REPORT-01) |
| TL regeneró desde cero en lugar de actualizar v1.0 | Confusión del flujo | El agente genera v1.0; el TL actualiza a v1.5 — leer Paso 8 |
| URL evidencia = URL base repo | No identifica el PR | Usar PR específico `.../pull/N` |

---

## Documentos relacionados

| Documento | Rol |
|---|---|
| `SKL-DYNAMIC-MODEL-01_cierre-modelo-dinamico.md` | Skill operativa de los Pasos 5.1-5.4 |
| `SKL-MANIFEST-01_generar-manifest.md` | Skill operativa del Paso 8 |
| `OPERATIVO_TL_REVIEWER.md v3.2` | Operativo completo del rol |
| `VTT_PLATFORM_GAPS_2026-05-13.md` | Gaps de feature del backend VTT |
| `reference_vtt_modelo_dinamico_endpoints.md` (memoria) | Cheatsheet de endpoints reales |
| `feedback_evidence_marker_pattern.md` (memoria) | Patrón del marker en evidencias |

---

## Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-08 | Versión inicial (solo verificación + APR-TL + status) |
| 2.0 | 2026-05-13 | Agregada FASE B (modelo dinámico): TIs + evidencias + devlog resolve. Aplicado a MS-285 como primera prueba; retroactivo a MS-283 y MS-284. |
| 2.1 | 2026-05-14 | Paso 8 corregido: el TL ACTUALIZA v1.0 → v1.5 (no regenera desde cero). El agente genera v1.0 en su paso 15. Clarificación de cambios entre versiones. |
| **2.2** | **2026-05-14** | **Worktrees por rol: Paso 4b (verificar disciplina de worktree) + Paso 9 (cleanup branch local). Referencias a `VTT.PROTOCOL-WT-001`. Cierra PROC-COORD-01.** |
