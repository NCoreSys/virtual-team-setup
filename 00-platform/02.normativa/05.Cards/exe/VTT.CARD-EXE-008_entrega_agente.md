# VTT.CARD-EXE-008 — Entrega final del agente + manifest v1.0

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-008` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = closing AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-EXE-005`, `CARD-EXE-006`, `CARD-EXE-007`, `CARD-MAN-001` |
| **Pertenece a** | WORKFLOW-ASG-001.010 |
| **Tokens estimados** | ~1,250 |

---

## Cierre ordenado de la ejecución

**EL ORDEN IMPORTA** — manifest v1.0 al FINAL (lección PROC-MANIFEST-01: generarlo antes resulta en campos null).

### Orden obligatorio

1. Fulfill CAs (CARD-EXE-004 Paso 8 lo hizo, verificar)
2. Postear SKL-REPORT-01 como comment
3. Verificar review-gate
4. Mover a `task_in_review`
5. Generar manifest v1.0 (AL FINAL)
6. Subir manifest como attachment
7. Commit manifest al PR
8. Render manifest en pantalla

## Paso 1 — Verificar fulfill de TODOS los CAs

```bash
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>/criteria" \
  -H "Authorization: Bearer $VTT_TOKEN" | python -m json.tool
```

Todos los CAs deben estar en `met` / `na` (justificado). Si alguno en `pending`/`not_met` → resolver antes de continuar.

## Paso 2 — Postear SKL-REPORT-01

```markdown
## 📤 ENTREGA: <TASK_ID> — <título>

### 🎯 Resumen
<1-2 líneas>

### 📦 Entregables
- Código: src/...
- PR: <URL>
- Devlog: <path>
- Code Logic: N archivos

### ✅ CAs
| CA | Status | Evidencia |
|---|---|---|

### 📄 Living Documents
- Total: N / N revisados
- Modificados: <lista>
- Sin cambios: N (devlog observations)

### 📄 Document Impacts
- Total: N (endpoint: N | fallback: N)

### 🔐 Hardcode Check
- Críticos/altos en producción: 0 ✅
- FPs justificados: N (devlog: DLE-X...)
- Status: PASS

### 📊 Devlog por status
- resolved: N | pending (low): N | wont_fix: N | deferred: N

### 🔗 TrackableItems
- Creados: N | Vinculados: N | N/A: <justificación si aplica>

—
Workflow: VTT.WORKFLOW-ASG-001.010 v1.0.0
```

**Si > 5000 chars** → subir como attachment `fileType=report` + comment con link.

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/comments" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d "{\"comment\": \"<contenido>\", \"authorId\": \"<AGENT_UUID>\"}"
```

## Paso 3 — Verificar review-gate

```bash
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>/review-gate" \
  -H "Authorization: Bearer $VTT_TOKEN" | python -m json.tool
```

Si `canProceedToReview=false` → leer `blockers[]` + resolver + reintentar (max 3).

## Paso 4 — Mover a `task_in_review`

```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-002_mover_in_review.py \
  --task-id "$TASK_ID" \
  --agent-id "$AGENT_UUID" \
  --reason "Entrega completa según WORKFLOW-ASG-001.010"
```

## Paso 5 — Generar manifest v1.0 (AL FINAL — PROC-MANIFEST-01)

Aplicar **CARD-MAN-001**:

```bash
python $VTT_SETUP/02.normativa/04.Scripts/manifest/SCRIPT-MAN-001_generate_v10.py \
  --task-id "$TASK_ID" \
  --output "knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_v1.0.json"
```

> ⚠️ Por qué AL FINAL: el manifest necesita `task_status=in_review`, attachments, pr_url, cas_summary. Generar antes = campos null.

## Paso 6 — Subir como attachment

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/attachments" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -F "file=@<path_manifest>" \
  -F "fileType=manifest" \
  -F "description=Task Manifest v1.0"
```

## Paso 7 — Commit manifest al PR

```bash
git add knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_v1.0.json
git commit -m "chore(<TASK_ID>): Task Manifest v1.0

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin feature/<TASK_ID>
```

## Paso 8 — Render en pantalla (auditoría visual obligatoria)

```bash
cat knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_v1.0.json | python -m json.tool
```

## Si falla

| Síntoma | Acción |
|---|---|
| review-gate=false | Leer `blockers[]` + resolver + reintentar |
| Manifest con campos null | Generaste antes de in_review → re-generar después |
| Comment > 5000 chars | Subir SKL-REPORT-01 como attachment + comment con link |
| Manifest no commiteado al PR | git add + commit + push (sin nuevo PR) |

## Output

Tarea en `task_in_review` + SKL-REPORT-01 posteado + manifest v1.0 attachment + committeado al PR + renderizado. **Listo para review del TL.**
