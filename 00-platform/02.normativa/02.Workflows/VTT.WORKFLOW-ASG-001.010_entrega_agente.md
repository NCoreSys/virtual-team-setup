# VTT.WORKFLOW-ASG-001.010 — Entrega final del agente + manifest v1.0

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.010` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.9 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor — cierre formal de su tarea |
| **Reglas Nivel 0** | `RULE-MAN-001`, `RULE-DELIV-001`, `RULE-SCRIPT-001` |
| **Origen** | Lección **PROC-MANIFEST-01** — manifest al FINAL del workflow |
| **CARD asociada** | `VTT.CARD-EXE-008` |

---

## 1. Propósito

Formalizar el **cierre ordenado** de la ejecución del agente. **El orden importa** — generar manifest antes de tener attachments + dynamic_model resulta en campos null (lección PROC-MANIFEST-01).

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `agent_id` | UUID | |
| `pr_url` | url | |
| `cas_to_report` | array | |
| `living_documents_modified` | array | (output .017) |
| `document_impacts_count` | int | (output .018) |
| `hardcode_check_status` | object | (output .019) |
| `devlog_summary` | object | |

## 3. Precondiciones

- Implementación + tests locales OK
- Commits + push (Paso 11 del `.034`)
- PR creado (Paso 13 del `.034`)
- `.017` `.018` `.019` ejecutados (este último con status PASS)
- Devlog `critical`/`high` en `status=resolved`

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Fulfill via `PATCH /criteria/:cid` NO `POST /fulfill` (404) |
| R2 | SKL-REPORT-01 obligatorio con 4 secciones: Living Docs / Document Impacts / Hardcode Check / Devlog por status |
| R3 | **Manifest v1.0 al FINAL** — después de attachments + status + dynamic_model (PROC-MANIFEST-01) |
| R4 | Path canónico: `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_v1.0.json` + render obligatorio |
| R5 | Antes de in_review → verificar `review-gate` retorna `canProceedToReview: true` |
| R6 | Reportar a TL via SKL-REPORT-01 formato canónico (NO informal) |
| R7 | Manifest sube como attachment `fileType=manifest` + commit al PR |

## 5. Pasos

### Orden obligatorio

1. Fulfill CAs
2. SKL-REPORT-01 comment
3. Review gate
4. `task_in_review`
5. Manifest v1.0 (AL FINAL)
6. Subir manifest attachment
7. Commit manifest al PR
8. Render en pantalla (auditoría visual)

### Paso 1 — Fulfill CAs
```bash
curl -X PATCH "$VTT_BASE_URL/api/tasks/<TASK_ID>/criteria/<CRITERIA_ID>" \
  -d '{"status":"met","evidence":"<concreta>","notes":"<opt>"}'
```

### Paso 2 — Consolidar datos para SKL-REPORT-01
4 secciones: Living Docs (output .017), Document Impacts (output .018), Hardcode Check (output .019), Devlog por status.

### Paso 3 — Postear SKL-REPORT-01 como comment
Comments ≤5000 chars. Si excede → attachment `fileType=report` + comment con link.

### Paso 4 — Verificar Review Gate
```bash
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>/review-gate"
```

Si false → resolver `blockers[]` + reintentar (max 3).

### Paso 5 — Mover a `task_in_review`
```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-002_mover_in_review.py \
  --task-id "$TASK_ID" --agent-id "$AGENT_UUID" --reason "Entrega completa"
```

### Paso 6 — Generar manifest v1.0 (AL FINAL — PROC-MANIFEST-01)

```bash
python $VTT_SETUP/02.normativa/04.Scripts/manifest/SCRIPT-MAN-001_generate_v10.py \
  --task-id "$TASK_ID" \
  --output "knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_v1.0.json"
```

> ⚠️ AL FINAL porque manifest necesita: `task_status=in_review`, `attachments[]`, `pr_url`, `cas_summary` (todos poblados por pasos 1-5).

### Paso 7 — Validar manifest
```bash
python $VTT_SETUP/02.normativa/04.Scripts/manifest/SCRIPT-MAN-002_validate.py \
  --manifest <path> --schema-version v1.0
```

### Paso 8 — Subir como attachment
```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/attachments" \
  -F "file=@<path>" -F "fileType=manifest" -F "description=Task Manifest v1.0"
```

### Paso 9 — Commit manifest al PR
```bash
git add knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_v1.0.json
git commit -m "chore(<TASK_ID>): Task Manifest v1.0

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin feature/<TASK_ID>
```

### Paso 10 — Render manifest (auditoría visual obligatoria)
```bash
cat knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_v1.0.json | python -m json.tool
```

## 6. Outputs

| Output | Descripción |
|---|---|
| `cas_reported_met` | int |
| `cas_reported_na` | int (justificados) |
| `skl_report_01_posted` | true |
| `review_gate_passed` | true |
| `task_status` | `task_in_review` |
| `manifest_v10_path` | path |
| `manifest_v10_attachment_id` | UUID |
| `manifest_committed_to_pr` | true |
| `ready_for_tl_review` | true |

## 7. Validación

- Review gate PASS
- Manifest v1.0 sin campos null
- Attachment fileType=manifest existe en VTT
- Commit del manifest en feature branch

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| 404 fulfill | `POST /fulfill` | Usar `PATCH /criteria/:cid` (R1) |
| Comment > 5000 chars | SKL-REPORT-01 muy largo | Attachment + link |
| Review gate FAIL | Blockers | Leer `blockers[]` + resolver |
| Manifest campos null | Generado antes de in_review | Mover paso 6 al final (R3) |
| Manifest no commited al PR | Olvido paso 9 | `git add` + commit + push |

## 9. Skills invocadas

`SKILL-CFL-001`, `SKILL-REPORT-001`, `SKILL-QUERY-003`, `SKILL-STATUS-002`, `SKILL-MAN-001`, `SKILL-ATTACH-001`

## 10. Scripts invocados

`SCRIPT-CFL-001`, `SCRIPT-REPORT-001_post_skl`, `SCRIPT-QUERY-003_review_gate`, `SCRIPT-STATUS-002`, `SCRIPT-MAN-001_generate_v10`, `SCRIPT-MAN-002_validate`, `SCRIPT-ATTACH-001`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Lección PROC-MANIFEST-01 incorporada (manifest al FINAL). Orden ordenado: CAs → SKL-REPORT-01 → review-gate → in_review → manifest → attachment → commit → render. Path canónico `knowledge/task-manifests/<phase>/<sprint>/`. |
