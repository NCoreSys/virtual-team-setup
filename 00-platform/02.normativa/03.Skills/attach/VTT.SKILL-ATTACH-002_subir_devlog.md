# VTT.SKILL-ATTACH-002 — Subir devlog de tarea

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-ATTACH-002` |
| **Categoría** | ATTACH (Attachment) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles ejecutores |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Paso 11 del workflow del agente — al completar tarea, ANTES de mover a `task_in_review` |
| **Reemplaza** | `SKL-ATTACH-02_subir-devlog.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `agent_uuid` | uuid | sí | UUID del agente |
| `task_slug` | string snake_case | sí | Nombre corto (ej. `setup-express`, `schema-usuarios`) — usado en filename |
| `devlog_path` | path | sí/no | Ruta al devlog (default: convención abajo) |

### Convención del path

```
knowledge/development-log/<YYYY-MM-DD>_<TASK_ID>_<task_slug>.md
```

Ejemplo: `knowledge/development-log/2026-05-19_MS-293_error-handling.md`

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Devlog archivo existe en disco
- El devlog está completo (no es un placeholder)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID
```

---

## Ejecución

```bash
DEVLOG_PATH="knowledge/development-log/$(date +%Y-%m-%d)_${TASK_ID}_${TASK_SLUG}.md"

# Verificar que existe
if [ ! -f "$DEVLOG_PATH" ]; then
    echo "ERROR: devlog no existe en $DEVLOG_PATH"
    exit 1
fi

# Subir como attachment fileType=devlog
DEVLOG_ATTACHMENT_ID=$(curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$DEVLOG_PATH" \
  -F "fileType=devlog" \
  -F "uploadedById=$AGENT_UUID" \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

echo "DEVLOG_ATTACHMENT_ID=$DEVLOG_ATTACHMENT_ID"
```

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
ats = json.load(sys.stdin).get('data', [])
devlogs = [a for a in ats if a.get('fileType') == 'devlog']
print(f'devlogs_attached: {len(devlogs)}')
"
# Esperado: >= 1
```

---

## Diferencia con `VTT.SKILL-DEV-001/002` (entries de devlog en VTT)

| Aspecto | Esta skill (ATTACH-002) | `VTT.SKILL-DEV-001/002` |
|---|---|---|
| Qué sube | Archivo .md completo del devlog | Entry individual en la API de devlog de VTT |
| Endpoint | `POST /tasks/<id>/attachments` (multipart) | `POST /tasks/<id>/devlog-entries` (JSON) |
| Cuándo | AL CIERRE de la tarea (1 vez) | DURANTE la ejecución (cada vez que hay decisión/observación) |
| Visibilidad | Attachment listado en VTT | Listado en la pestaña devlog de VTT |
| Manifest | Va en `delivery.vtt_attachments.devlog_id` | Va en `delivery.devlog_entries[]` |

**El agente DEBE hacer ambos:**
1. Durante ejecución → `VTT.SKILL-DEV-001/002` para cada decisión/observación
2. Al cierre → esta skill para subir el archivo .md completo

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Devlog no existe en path esperado | Filename no sigue convención | Generar con formato `<YYYY-MM-DD>_<TASK_ID>_<slug>.md` |
| Subir devlog vacío | Olvido de poblar antes | Confirmar `cat $DEVLOG_PATH` antes de subir |
| `uploadedById` faltante | Olvido del campo | Ver `VTT.SKILL-ATTACH-001` Error #1 |
| Subir devlog 2 veces | Re-ejecución sin querer | OK — VTT permite múltiples attachments del mismo tipo. El consumer usa el más reciente |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-ATTACH-001` — esta es una variante específica que invoca la skill base

---

## Skills que invocan ESTA

- Workflow del agente al cerrar tarea (Paso 11 estándar)
- `VTT.WORKFLOW-MAN-001.003` — precondición #3 (devlog subido) antes de generar manifest v1.0

---

## Cuándo NO usar esta Skill

- **Durante la tarea** (no al cierre) — usar `VTT.SKILL-DEV-001/002` para entries individuales
- **Si el devlog es vacío/placeholder** — generar contenido real antes

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-ATTACH-02_subir-devlog.md`. Ampliación: tabla comparativa con DEV-001/002 (legacy confundía los dos conceptos). Captura de `DEVLOG_ATTACHMENT_ID` para inyectar en manifest v1.0. |
