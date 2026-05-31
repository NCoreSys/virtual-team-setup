# VTT.SKILL-COMMENT-001 — Postear comentario genérico en tarea

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-COMMENT-001` |
| **Categoría** | COMMENT (Comments) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Feedback, notas operativas, reportes, mensajes al equipo dentro de una tarea |
| **Reemplaza** | `SKL-COMMENT-01_comentario-generico.md` (legacy) |

---

## ⚠️ CRÍTICO — naming de campos del payload

El payload usa **`message` + `userId`** (NO `content` + `authorId`).

| ✅ Correcto | ❌ Incorrecto (HTTP 400) |
|---|---|
| `message` | `content` |
| `userId` | `authorId` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea donde postear |
| `agent_uuid` | uuid | sí | UUID del autor del comment (= `userId`) |
| `message` | string ≤5000 | sí | Texto del comment (markdown soportado) |
| `comment_type` | enum | sí/no | `general` (default) / `assignment` / `wontfix` / `closure` — algunos consumers filtran por tipo |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- La tarea existe y es accesible para el agente
- `message` no excede 5000 caracteres (límite de VTT)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID
```

---

## Ejecución

### Opción A — Comment simple

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"$COMMENT_MESSAGE\",
    \"userId\": \"$AGENT_UUID\"
  }"
```

### Opción B — Comment con tipo

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"$COMMENT_MESSAGE\",
    \"userId\": \"$AGENT_UUID\",
    \"type\": \"$COMMENT_TYPE\"
  }"
```

### Opción C — Mensaje multilínea (uso heredoc para escapar)

```bash
MESSAGE=$(cat <<'EOF'
Aviso al equipo:

- Punto 1
- Punto 2

Saludos, $AGENT_UUID
EOF
)

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$(python -c "import json; print(json.dumps({'message': '''$MESSAGE''', 'userId': '$AGENT_UUID'}))")"
```

---

## Validación

```bash
# El comment debe aparecer en el listado
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
cs = json.load(sys.stdin).get('data', [])
print('total_comments:', len(cs))
last = cs[-1] if cs else None
if last:
    print('last_message:', (last.get('message') or '')[:80])
"
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `INVALID_FIELDS` | Usar `content` / `authorId` | Usar `message` / `userId` exactos |
| HTTP 400 `TOO_LONG` | `message` > 5000 chars | Recortar o partir en múltiples comments |
| HTTP 400 JSON malformado | Comillas sin escapar en el texto | Usar Opción C con heredoc + `json.dumps` |
| HTTP 404 | TASK_ID incorrecto | Verificar ID externo (MS-XXX) |
| Comment no aparece | Cache | Hacer `GET` después de POST, no asumir éxito por HTTP 201 |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- `VTT.SKILL-COMMENT-002` (APR-PM) — formato específico de aprobación PM
- `VTT.SKILL-COMMENT-003` (APR-TL) — formato específico de aprobación TL
- Cualquier rol que necesite postear un comentario en una tarea (consultas, feedback, etc.)
- `VTT.SKILL-STATUS-006` — postear feedback de rechazo ANTES de cambiar status

---

## Cuándo NO usar esta Skill

- **Si es aprobación formal del TL** → usar `VTT.SKILL-COMMENT-003` (formato APR-TL)
- **Si es aprobación formal del PM** → usar `VTT.SKILL-COMMENT-002` (formato APR-PM)
- **Si es mensaje de asignación inicial** → usar `VTT.SKILL-TASK-004` con template oficial

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-COMMENT-01_comentario-generico.md`. Ampliación: 3 opciones (simple/tipado/multilínea con heredoc) + documentación del campo `type` que VTT acepta. Contrato sin cambios. |
