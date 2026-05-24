# VTT.SKILL-ATTACH-001 — Subir archivo como attachment

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-ATTACH-001` |
| **Categoría** | ATTACH (Attachment) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles |
| **Tokens estimados** | ~200 |
| **Cuándo se usa** | Skill **base** de attachments — invocada por todas las skills/workflows que suben archivos (briefs, assignments, devlogs, code_logic, manifests, reports) |
| **Reemplaza** | `SKL-ATTACH-01_subir-archivo.md` (legacy) |

---

## ⚠️ CRÍTICO — campo `uploadedById` obligatorio

VTT exige `uploadedById` en el form-data del multipart. **Sin este campo → HTTP 400.**

(Bug #6 del SCRIPT-MAN-001 v1.1 — origen: olvido recurrente de este campo).

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea destino |
| `file_path` | path | sí | Ruta local al archivo a subir |
| `file_type` | enum | sí | `brief` / `assignment` / `devlog` / `code_logic` / `manifest` / `report` / `spec` / `log` |
| `uploaded_by_id` | uuid | sí | UUID del agente que sube |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- El archivo existe en disco (`ls $FILE_PATH` retorna)
- El `fileType` es válido (uno del enum de VTT)
- El tamaño del archivo NO excede el límite del backend (~5MB típico)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID
```

---

## Ejecución

### Opción A — Bash con curl multipart

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$FILE_PATH" \
  -F "fileType=$FILE_TYPE" \
  -F "uploadedById=$AGENT_UUID"
```

Capturar el `attachment_id` del response:

```bash
ATTACHMENT_RESPONSE=$(curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$FILE_PATH" \
  -F "fileType=$FILE_TYPE" \
  -F "uploadedById=$AGENT_UUID")

ATTACHMENT_ID=$(echo "$ATTACHMENT_RESPONSE" | python -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
echo "ATTACHMENT_ID=$ATTACHMENT_ID"
```

### Opción B — Python (para scripts que ya están en Python)

```python
import urllib.request
import os

boundary = "----VTTBoundary7MA4YWxkTrZu0gW"

with open(file_path, "rb") as f:
    file_bytes = f.read()
filename = os.path.basename(file_path)

body = b""
body += f"--{boundary}\r\n".encode()
body += b'Content-Disposition: form-data; name="fileType"\r\n\r\n'
body += f"{file_type}\r\n".encode()
body += f"--{boundary}\r\n".encode()
body += b'Content-Disposition: form-data; name="uploadedById"\r\n\r\n'
body += f"{uploaded_by_id}\r\n".encode()
body += f"--{boundary}\r\n".encode()
body += f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode()
body += b'Content-Type: text/markdown\r\n\r\n'
body += file_bytes
body += f"\r\n--{boundary}--\r\n".encode()

req = urllib.request.Request(
    f"{vtt_base_url}/api/tasks/{task_id}/attachments",
    data=body,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    },
    method="POST"
)
import json
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    attachment_id = data['data']['id']
```

---

## Validación

```bash
# El attachment debe aparecer en el listado
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
ats = json.load(sys.stdin).get('data', [])
last = ats[-1] if ats else None
if last:
    print(f\"last: id={last['id']} type={last.get('fileType')} file={last.get('fileName')}\")
else:
    print('SIN_ATTACHMENTS')
"
```

---

## Cómo descargar un archivo subido

VTT tiene endpoint dedicado:

```bash
# El endpoint /file devuelve el binario directo
curl -s "$VTT_BASE_URL/api/attachments/$ATTACHMENT_ID/file" \
  -H "Authorization: Bearer $TOKEN" \
  --output downloaded_file.md
```

> **Nota:** NO usar `GET /api/tasks/<task_id>/attachments/<id>` para descargar — eso devuelve metadata. El endpoint correcto es `/api/attachments/<id>/file` (Bug #7 del SCRIPT-MAN-001).

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `MISSING_FIELD: uploadedById` | Falta `uploadedById` en form-data | Agregar `-F "uploadedById=$AGENT_UUID"` |
| HTTP 400 `INVALID_FILE_TYPE` | `fileType` fuera del enum | Usar uno de: brief/assignment/devlog/code_logic/manifest/report/spec/log |
| HTTP 413 `PAYLOAD_TOO_LARGE` | Archivo > 5MB | Comprimir, partir, o subir como `log` con compresión |
| HTTP 415 `UNSUPPORTED_MEDIA` | Subir JSON puro como `application/json` | Wrappear en `.md` con bloque ` ```json ` (caso manifest) |
| HTTP 404 task | `task_id` incorrecto | Verificar ID externo (MS-XXX) |
| File path con espacios falla | Bash no maneja bien espacios | Usar comillas: `-F "file=@\"$FILE_PATH\""` |
| Atajo `multipart/form-data` mal armado | Boundary incorrecto en Python manual | Copiar exactamente el snippet Opción B |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- `VTT.SKILL-ATTACH-002` — caso específico devlog
- `VTT.SKILL-TASK-001` — subir BRIEF (`fileType=brief`)
- `VTT.SKILL-TASK-003` — subir ASSIGNMENT (`fileType=assignment`)
- `VTT.WORKFLOW-MAN-001.003` — subir manifest (`fileType=manifest`)
- `VTT.SKILL-REPORT-001` — subir reporte (`fileType=report`)
- Cualquier workflow que genere un archivo a vincular a la tarea

---

## Cuándo NO usar esta Skill

- **Si solo querés enlazar un URL** (no archivo físico) — usar `VTT.SKILL-COMMENT-001` con el URL en el mensaje
- **Si el archivo es ephemeral/debug** — no abusar de attachments, dejarlo en logs locales

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-ATTACH-01_subir-archivo.md`. Ampliación: Opción B (Python manual con multipart) que se reutiliza en SCRIPT-MAN-001. Documentación del endpoint de descarga `/api/attachments/<id>/file` (Bug #7 documentado). Tabla de errores comunes con 7 casos. |
