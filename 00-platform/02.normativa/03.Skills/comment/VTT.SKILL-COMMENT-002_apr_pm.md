# VTT.SKILL-COMMENT-002 — APR-PM (Aprobación funcional del PM)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-COMMENT-002` |
| **Categoría** | COMMENT (Comments) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | **PM únicamente** |
| **Tokens estimados** | ~200 |
| **Cuándo se usa** | Al aprobar funcional una tarea — **ejecutar ANTES de `VTT.SKILL-STATUS-004`** (mover a `task_approved`) |
| **Reemplaza** | `SKL-COMMENT-02_apr-pm.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `pm_uuid` | uuid | sí | UUID del PM |
| `ac_verificados` | string o array | sí | Lista de Acceptance Criteria verificados (IDs o descripciones cortas) |
| `notas` | string | sí/no | Notas adicionales del PM al aprobar |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en status `task_completed` (post-aprobación TL)
- **OBLIGATORIO: el PM leyó los Acceptance Criteria** con `VTT.SKILL-QUERY-003` Opción B
- **OBLIGATORIO: cada CA verificado tiene status `met` con evidencia válida**

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID                # = PM_UUID
```

---

## Formato del mensaje (template)

```
APR-PM: tarea aprobada funcionalmente.

Acceptance criteria verificados:
- CA-XX: <título> ✅
- CA-YY: <título> ✅
- ...

Notas: <notas opcionales>
```

---

## Ejecución

```bash
# Construir el mensaje
APR_MESSAGE=$(cat <<EOF
APR-PM: tarea aprobada funcionalmente.

Acceptance criteria verificados:
$AC_VERIFICADOS

Notas: $NOTAS
EOF
)

# Postear comment
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$(python -c "
import json
print(json.dumps({
    'message': '''$APR_MESSAGE''',
    'userId': '$AGENT_UUID',
    'type': 'approval'
}))")"
```

---

## Validación

```bash
# El comment debe aparecer con tipo 'approval'
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
cs = json.load(sys.stdin).get('data', [])
apr_pm = [c for c in cs if 'APR-PM' in (c.get('message') or '')]
print('apr_pm_comments:', len(apr_pm))
"
# Esperado: >= 1
```

---

## Restricción

**Solo PM puede ejecutar esta skill.**

El TL tiene su propia aprobación con `VTT.SKILL-COMMENT-003` (APR-TL).

---

## Reglas críticas

- ❌ **NUNCA aprobar sin leer los Acceptance Criteria** (precondición #3)
- ❌ NUNCA aprobar si algún CA está `not_met` o `pending`
- ❌ NUNCA aprobar con issues abiertos (verificar con `VTT.SKILL-QUERY-003` Opción F)
- ✅ El comment va ANTES del PATCH de status — si invierte el orden, el agente recibe el cambio de status sin contexto

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Aprobar sin comment APR-PM | Saltar este paso | Postear primero, después cambiar status |
| HTTP 400 JSON malformado | Comillas sin escapar en notas | Usar Opción Python `json.dumps` |
| Aprobar con CA `not_met` | Saltar precondición | Rechazar con `VTT.SKILL-STATUS-006` en su lugar |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-QUERY-003` Opción B — leer CAs antes (precondición)

---

## Skills que invocan ESTA

- Workflow del PM al cerrar review final
- Antes de `VTT.SKILL-STATUS-004` (mover a `task_approved`)

---

## Cuándo NO usar esta Skill

- **Si la tarea no está en `task_completed`** — TL debe completar primero
- **Si vas a rechazar** — usar `VTT.SKILL-STATUS-006` con feedback específico
- **Si el comment es genérico (no aprobación)** — usar `VTT.SKILL-COMMENT-001`

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-COMMENT-02_apr-pm.md`. Ampliación: template estructurado del mensaje (CAs verificados como lista) + tipo `approval` en payload + reglas críticas para evitar aprobación prematura. |
