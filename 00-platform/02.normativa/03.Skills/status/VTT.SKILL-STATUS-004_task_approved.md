# VTT.SKILL-STATUS-004 — Mover tarea a `task_approved` (solo PM)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-STATUS-004` |
| **Categoría** | STATUS (Status transitions) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | **PM únicamente** |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Después de aprobación funcional (APR-PM comment) — paso 5.5.17 del PROTOCOL-ASG-001 |
| **Reemplaza** | `SKL-STATUS-04_task-approved-pm.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `pm_uuid` | uuid | sí | UUID del PM (= `changedBy`) |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en status `task_completed`
- **APR-PM comment posteado** (`VTT.SKILL-COMMENT-002` cuando se migre)
- **NUNCA aprobar sin haber leído los Acceptance Criteria de la tarea**

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL
$AGENT_UUID                # = PM_UUID
$STATUS_APPROVED_UUID      # b9ca4951-6e14-4d82-b1d8-440793bbaf47 (fijo)
```

---

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"statusId\": \"b9ca4951-6e14-4d82-b1d8-440793bbaf47\",
    \"changedBy\": \"$AGENT_UUID\"
  }"
```

---

## Restricción

**Solo PM puede ejecutar esta skill.**

`task_approved` es el **estado terminal** de una tarea. Después de esto:
- El TL ejecuta cleanup branch (`PROTOCOL-ASG-001 §5.5.18`)
- El TL archiva el execution_manifest (opcional)
- La tarea queda histórica — NO se puede revertir desde la UI estándar

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])"
# Esperado: task_approved
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `INVALID_TRANSITION` | Tarea no estaba en `task_completed` | Verificar status — solo from `task_completed` |
| HTTP 403 | UUID no es el PM del proyecto | Confirmar rol — esta skill es exclusiva del PM |
| Aprobar sin leer CAs | Saltar precondición | NUNCA aprobar sin leer — afecta calidad del proyecto |
| Aprobar con APR-PM pendiente | No postear APR-PM antes | Postear comment APR-PM primero |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Cuándo NO usar esta Skill

- **Si la tarea está en `task_in_review`** — el TL debe completarla primero
- **Si los CAs no están todos en `met`** — rechazar con `VTT.SKILL-STATUS-006`
- **Si hay deuda técnica grave detectada en review** — solicitar tarea de fix primero

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-STATUS-04_task-approved-pm.md`. Contrato sin cambios. |
