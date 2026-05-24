# Guía — Task Manifest para agentes ejecutores

**Versión:** 3.1

**Changelog v2.0 → v3.1:**
- `skl_report_01_full` ahora se lee del archivo local `knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md` (sin truncar)
- Agente debe guardar reporte completo en archivo ANTES de generar manifest
- Comment de VTT es solo extracto (max 5000 chars)
- Campo nuevo `skl_report_01_source` referencia el archivo fuente
- Coordinado con SKL-REPORT-01 v2.0 + SKL-MANIFEST-01 v4.1
**Fecha:** 2026-05-14
**Aplicable a:** BE, DB, FE, QA, DO, DL, UX, AR, SA (cualquier agente ejecutor)
**Complemento de:** `SKL-MANIFEST-01` (skill del TL Reviewer)

---

## Qué es el manifest

Es un archivo JSON estructurado que vive en `knowledge/task-manifests/[fase]/[sprint]/MS-XXX.json` + wrapper `.md` para subirlo a VTT. Captura **todo el ciclo de vida de una tarea** en un solo documento auditable: BRIEF, ASSIGNMENT, entrega del agente, decisiones, evidencias, review del TL.

## Quién hace qué con el manifest

| Versión | Quién | Cuándo | Contenido |
|---|---|---|---|
| **v1.0** | **Agente ejecutor (TÚ)** | Paso 15 de tu workflow — AL FINAL, después de attachments + status `in_review` + PRs | Bloques `task`, `brief`, `assignment`, `agent_message`, `delivery` poblados con TU trabajo real |
| **v1.5** | TL Reviewer | Paso 14 del cierre | Lee tu v1.0 → agrega `delivery.dynamic_model_actions` + `review.tl_review` → sube como nuevo attachment |

**Tu rol:** generar la v1.0 con `current_status: task_in_review` y subir como attachment `fileType=manifest`.

**No es opcional.** Es el entregable #7.5 obligatorio del ASSIGNMENT.

---

## Regla crítica de orden — manifest AL FINAL

> Generar el manifest **DESPUÉS** de estos pasos. Si lo generas antes, quedan campos `null` en `delivery`.

```
Paso 14 del workflow:
  [x] Devlog subido como attachment
  [x] Code Logic subido (real o placeholder N/A)
  [x] Status moved → task_in_review
  [x] PR(s) creado(s) con URL específica
  [x] Review Gate canProceedToReview=true

Paso 15:
  → Recolectar IDs reales de todo lo anterior
  → Construir MS-XXX.json con bloques completos
  → Subir como attachment fileType=manifest
```

**Lección PROC-MANIFEST-01:** la primera versión de MS-284 tuvo 10+ campos null porque se generó prematuramente.

---

## Esquema del JSON v1.0 (lo que tú generas)

```json
{
  "schema_version": "1.0",
  "manifest_id": "MS-XXX",
  "generated_at": "<ISO timestamp>",
  "generated_by": "<TU_UUID>",
  "generation_note": "Generado por <rol> al cerrar el workflow del agente. v1.0 — sin review.tl_review (lo agrega el TL Reviewer).",
  "last_updated": "<ISO timestamp>",
  "last_updated_block": "delivery",

  "task": {
    "id": "MS-XXX",
    "title": "<titulo>",
    "sprint": { "id": "<uuid>", "name": "S1 - ..." },
    "stage": "development",
    "assignee": { "id": "<TU_UUID>", "role": "<tu_rol>" },
    "estimated_hours": N,
    "actual_hours": N,
    "complexity": "LOW|MEDIUM|HIGH",
    "category": "development|deployment|documentation",
    "sdlc_catalog_id": "4.X.Y",
    "current_status": "task_in_review",
    "dependencies_upstream": ["MS-YYY", "MS-ZZZ"]
  },

  "brief": {
    "vtt_attachment_id": "<uuid>",
    "file_path": "knowledge/agent-tasks/briefs/04-development/S01/BRIEF_MS-XXX_<slug>.md"
  },
  "assignment": {
    "vtt_attachment_id": "<uuid>",
    "file_path": "knowledge/agent-tasks/assignments/04-development/S01/ASSIGNMENT_MS-XXX_<slug>.md",
    "criteria_count": N
  },
  "agent_message": {
    "template_version": "3.0",
    "agent_role": "<tu_rol>",
    "agent_uuid": "<TU_UUID>",
    "generated_by_script": "scripts/gen_mensaje.py"
  },

  "delivery": {
    "delivered_at": "<ISO timestamp>",
    "delivered_by": "<TU_UUID>",
    "vtt_report_comment_id": "<id del comment-extracto posteado en VTT (max 5000 chars)>",
    "skl_report_01_full": "<reporte COMPLETO leido del archivo knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md>",
    "skl_report_01_source": "knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md",

    "deliverables_actual": [
      { "path": "memory-service-backend/src/...", "state": "created|modified" }
    ],
    "code_logic_files": [
      "memory-service-backend/knowledge/code-logic/.../X.LOGIC.md"
    ],
    "code_logic_attachment_strategy": {
      "placeholder_uploaded": false,
      "placeholder_attachment_id": null,
      "reason": "Tarea produce código TS, code_logic real"
    },

    "vtt_attachments": {
      "brief_id": "<uuid>",
      "assignment_id": "<uuid>",
      "devlog_id": "<uuid>",
      "code_logic_ids": ["<uuid>", "<uuid>"]
    },

    "criteria_results": [
      { "id": "<uuid>", "title": "CA-XX: ...", "status": "met" }
    ],
    "criteria_summary": { "total": N, "met": N },

    "devlog_summary": { "total": N, "all_resolved_by_tl": false },

    "hardcode_check": {
      "executed": true,
      "findings_total": N,
      "findings_critical_high": 0,
      "false_positives_justified": N
    },

    "tests": {
      "framework": "Jest|Vitest|N/A",
      "tests_passing": N,
      "coverage_stmts": N.NN,
      "threshold_met": true
    },

    "trackable_items_actual": {
      "implements": [
        { "code": "NFR-SEC-XX", "uuid": "<uuid>" }
      ],
      "related_to": [
        { "code": "AS-001", "uuid": "<uuid>" }
      ]
    },

    "living_documents_declared_no_change": ["LD-XX"],

    "tech_debt_for_r2": [
      {
        "code_suggested": "DEBT-XXX-NN",
        "title": "<descripcion>",
        "urgency": "low|medium|high",
        "retroactive": false
      }
    ],

    "items_detected_for_tl_review": [
      {
        "type_suggested": "tech_debt|process_improvement",
        "code_suggested": "DEBT-XXX-NN | PROC-XXX-NN",
        "description": "<descripcion>",
        "urgency": "baja|media|alta"
      }
    ],

    "how_to_verify": [
      "curl ... | jq ...",
      "cd <repo> && npm test"
    ],

    "git": {
      "backend": {
        "pr_number": N,
        "pr_url": "https://github.com/NCoreSys/memory-service-backend/pull/N",
        "commit_sha": "<sha>",
        "base_branch": "main"
      },
      "project": {
        "pr_number": M,
        "pr_url": "https://github.com/NCoreSys/memory-service-project/pull/M",
        "commit_sha": "<sha>"
      }
    },

    "metrics": {
      "actual_hours": N,
      "deliverables_count": N
    }
  },

  "review": {
    "tl_review": null,
    "pm_approval": null
  },

  "indexes": {
    "implements_codes": ["NFR-SEC-XX"],
    "related_to_codes": ["AS-001"],
    "tech_debt_count": N,
    "criteria_met_ratio": "N/N",
    "devlog_entries_count": N,
    "files_created_count": N
  }
}
```

> `review.tl_review` queda en `null`. El TL lo poblará en v1.5.

---

## Generación práctica — Snippet Python

Recolectar IDs reales desde VTT en lugar de hardcodear:

```python
import urllib.request, json, os, sys, uuid
from datetime import datetime, timezone

BASE_URL = "http://77.42.88.106:3000"
TASK_ID = "MS-XXX"
AGENT_UUID = os.environ["AGENT_UUID"]
SK = os.environ["MEM_VTT_SERVICE_KEY"]

# Token
req = urllib.request.Request(f'{BASE_URL}/api/auth/service-token',
    data=json.dumps({'userId':AGENT_UUID,'serviceKey':SK}).encode(),
    headers={'Content-Type':'application/json'}, method='POST')
TOKEN = json.loads(urllib.request.urlopen(req).read())['data']['token']
H = {'Authorization': f'Bearer {TOKEN}'}

def g(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(
        f'{BASE_URL}{path}', headers=H)).read()).get('data')

# Recolectar
task = g(f'/api/tasks/{TASK_ID}')
criteria = g(f'/api/tasks/{TASK_ID}/criteria')
devlog = g(f'/api/tasks/{TASK_ID}/devlog')
atts = g(f'/api/tasks/{TASK_ID}/attachments')
comments = g(f'/api/tasks/{TASK_ID}/comments')

brief_att = next((a for a in atts if a.get('fileType') == 'brief'), None)
assignment_att = next((a for a in atts if a.get('fileType') == 'assignment'), None)
devlog_att = next((a for a in atts if a.get('fileType') == 'devlog'), None)
code_logic_atts = [a for a in atts if a.get('fileType') == 'code_logic']

# Buscar TU comment SKL-REPORT-01 (debe existir antes de generar manifest)
skl_comment = next(
    (c for c in comments if c.get('userId') == AGENT_UUID
     and 'Entrega' in c.get('message','')[:30]),
    None
)
if not skl_comment:
    sys.exit("ABORT: Comment SKL-REPORT-01 no existe aun. Postealo PRIMERO.")

manifest = {
    "schema_version": "1.0",
    "manifest_id": TASK_ID,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "generated_by": AGENT_UUID,
    "generation_note": "v1.0 generado por agente al cerrar workflow. TL Reviewer agregara review.tl_review en v1.5.",
    "last_updated": datetime.now(timezone.utc).isoformat(),
    "last_updated_block": "delivery",
    "task": {
        "id": TASK_ID,
        "title": task.get('title'),
        "current_status": task.get('status',{}).get('code'),
        # ... resto de campos
    },
    "brief": {
        "vtt_attachment_id": brief_att.get('id') if brief_att else None,
        "file_path": f"knowledge/agent-tasks/briefs/04-development/S01/BRIEF_{TASK_ID}_<slug>.md"
    },
    "assignment": {
        "vtt_attachment_id": assignment_att.get('id') if assignment_att else None,
        "file_path": f"knowledge/agent-tasks/assignments/04-development/S01/ASSIGNMENT_{TASK_ID}_<slug>.md",
        "criteria_count": len(criteria)
    },
    "delivery": {
        "vtt_report_comment_id": skl_comment.get('id'),
        "skl_report_01_full": skl_comment.get('message'),
        "vtt_attachments": {
            "brief_id": brief_att.get('id') if brief_att else None,
            "assignment_id": assignment_att.get('id') if assignment_att else None,
            "devlog_id": devlog_att.get('id') if devlog_att else None,
            "code_logic_ids": [a.get('id') for a in code_logic_atts]
        },
        "criteria_results": [{"id": ca.get('id'), "title": ca.get('title'), "status": ca.get('status')} for ca in criteria],
        "criteria_summary": {"total": len(criteria), "met": sum(1 for c in criteria if c.get('status')=='met')},
        "devlog_summary": {"total": len(devlog), "all_resolved_by_tl": False},
        # ... completar con tu información
    },
    "review": {"tl_review": None, "pm_approval": None},
    # ... indexes
}

# Guardar JSON
out_dir = "knowledge/task-manifests/04-development/S01"
os.makedirs(out_dir, exist_ok=True)
json_path = f"{out_dir}/{TASK_ID}.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# Wrapper MD (porque VTT no acepta application/json)
md_path = f"{out_dir}/{TASK_ID}.manifest.md"
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"# Task Manifest — {TASK_ID} (v1.0 — entrega del agente)\n\n```json\n{json.dumps(manifest, indent=2, ensure_ascii=False)}\n```\n")

# Subir a VTT
with open(md_path, 'rb') as f:
    content = f.read()
boundary = '----' + uuid.uuid4().hex
fields = {"fileType":"manifest","uploadedById":AGENT_UUID,
          "description":f"Manifest {TASK_ID} v1.0 - entrega del agente. Pendiente review TL."}
parts = []
for k, v in fields.items():
    parts.append(f'--{boundary}\r\n'.encode())
    parts.append(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode())
    parts.append(f'{v}\r\n'.encode())
parts.append(f'--{boundary}\r\n'.encode())
parts.append(f'Content-Disposition: form-data; name="file"; filename="{TASK_ID}.manifest.md"\r\n'.encode())
parts.append(b'Content-Type: text/markdown\r\n\r\n')
parts.append(content)
parts.append(f'\r\n--{boundary}--\r\n'.encode())
body = b''.join(parts)
req = urllib.request.Request(f'{BASE_URL}/api/tasks/{TASK_ID}/attachments',
    data=body,
    headers={'Authorization': f'Bearer {TOKEN}',
             'Content-Type': f'multipart/form-data; boundary={boundary}'},
    method='POST')
urllib.request.urlopen(req)
print(f"Manifest v1.0 subido")
```

---

## Antes de generar v1.0 — Checklist

```
[ ] Implementación commiteada y pusheada en feature/MS-XXX
[ ] PR(s) creado(s) con URL específica .../pull/N
[ ] Devlog entries registrados en VTT
[ ] CAs reportados con PATCH /criteria/:cid
[ ] Review Gate verde (canProceedToReview=true)
[ ] Status moved a task_in_review
[ ] Attachments subidos: devlog + code_logic (real o placeholder)
[ ] **Reporte SKL-REPORT-01 GUARDADO en archivo local:**
    knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md
    (Este es el reporte COMPLETO sin truncar — fuente de verdad)
[ ] **Extracto del reporte posteado como comment en VTT** (max 5000 chars,
    con link al archivo completo)
[ ] AHORA SÍ: generar manifest v1.0 y subir
    (El script SKL-MANIFEST-01 v4.1+ lee skl_report_01_full DESDE EL ARCHIVO,
    no desde el comment — asi el reporte queda completo en el JSON)
```

Si saltaste alguno → tu manifest tendrá campos `null` o el reporte truncado. Vuelve atrás.

> **REGLA CLAVE (v3.1+):** El reporte completo vive en el ARCHIVO. El comment de VTT
> es solo un extracto navegable (limite 5000 chars). El JSON del manifest debe contener
> el reporte completo en `skl_report_01_full` leyendo del archivo, no del comment.

---

## Qué pasa después de tu entrega

El TL Reviewer ejecuta su workflow de cierre (`GUIA_REVISION_TAREA_TL_REVIEWER.md`):

1. **FASE A:** lee tu SKL-REPORT-01, valida CAs, gate, attachments, PRs, manifest v1.0
2. **FASE B (modelo dinámico):**
   - Crea TIs nuevos desde tu sección "Items detectados para trackeo" del reporte
   - Agrega evidencias con marker `[TASK:MS-XXX]` a TIs heredados y nuevos
   - Marca tus devlog entries como `resolved` con `resolution`
3. **FASE C (cierre):**
   - Postea APR-TL comment
   - Mueve a `task_completed`
   - **Lee tu manifest v1.0** y genera **v1.5**:
     - Agrega `delivery.dynamic_model_actions` con lo que él hizo en FASE B
     - Agrega `review.tl_review` con su verdict y verifications
     - Sube como nuevo attachment `fileType=manifest`

Tu v1.0 NO se borra (no hay DELETE de attachments). Convive con v1.5. El último `fileType=manifest` por `createdAt` es la fuente de verdad.

---

## Lo que SÍ y NO debes hacer

| Acción | ¿Tú lo haces? |
|---|---|
| Generar v1.0 del manifest al final de tu workflow | ✅ SÍ |
| Subirlo como `fileType=manifest` a VTT | ✅ SÍ |
| Incluir `delivery.skl_report_01_full` con texto literal de tu comment | ✅ SÍ |
| Dejar `review.tl_review: null` | ✅ SÍ (eso es del TL) |
| Marcar `current_status: "task_in_review"` | ✅ SÍ (ese es tu estado al cerrar) |
| Generar v1.5 con review.tl_review | ❌ NO (es del TL) |
| Resolver tus propios devlog entries | ❌ NO (es del TL al cerrar) |
| Crear TIs con `[DEFER R2]` marker | ❌ NO (el TL los crea desde tu reporte) |
| Agregar evidencias a TIs heredados | ❌ NO (el TL las agrega con marker `[TASK:MS-XXX]`) |
| Mover a `task_completed` | ❌ NO (eso es del TL Reviewer) |

---

## Errores comunes

| Error | Síntoma | Solución |
|---|---|---|
| Generar manifest antes de paso 14 (status `in_review`) | `current_status: task_in_progress`, devlog incompleto | Postergar a paso 15, después de status change |
| Generar manifest sin haber guardado el reporte en archivo | `skl_report_01_full: null` o script ABORT | Crear archivo `knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md` con reporte completo PRIMERO |
| `skl_report_01_full` truncado a 5000 chars | Script viejo (v4.0-) leía del comment VTT | Actualizar SKL-MANIFEST-01 a v4.1+ que lee del archivo |
| Generar manifest antes de crear PRs | `git.pr_url: null` | Crear PRs PRIMERO |
| Subir como JSON puro | 400 Bad Request | Wrappear en `.md` con bloque ` ```json ` |
| Incluir `review.tl_review` poblado | Conflict con v1.5 del TL | Dejar `null` |
| URLs base del repo | Evidencias del TL quedan inútiles | Usar `.../pull/N` específico |
| Omitir "Items detectados para trackeo" del SKL-REPORT-01 | TL no crea TIs nuevos | Siempre rellenar tabla |

---

## Documentos relacionados

| Doc | Para qué sirve |
|---|---|
| `SKL-MANIFEST-01_generar-manifest.md` | Skill operativa (cubre v1.0 agente + v1.5 TL) |
| `SKL-REPORT-01_entrega-tarea.md` | Skill del comment SKL-REPORT-01 |
| `TEMPLATE_ASIGNACION_TAREARev.md` v3.1 | Tu ASSIGNMENT (entregable #7.5 = manifest) |
| `GUIA_REVISION_TAREA_TL_REVIEWER.md` | Lo que el TL hace con tu v1.0 |
| `OPERATIVO_<TU_ROL>_MEMORY-SERVICE.md` | Tu operativo de rol |
