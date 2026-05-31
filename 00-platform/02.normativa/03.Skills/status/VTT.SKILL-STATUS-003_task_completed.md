# VTT.SKILL-STATUS-003 — Mover tarea a `task_completed` (solo TL)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-STATUS-003` |
| **Categoría** | STATUS (Status transitions) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | **TL únicamente** (Reviewer) |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Después de aprobar la revisión técnica (APR-TL posteado) — paso 5.5.12 del PROTOCOL-ASG-001 |
| **Reemplaza** | `SKL-STATUS-03_task-completed-tl.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `tl_uuid` | uuid | sí | UUID del TL Reviewer (= `changedBy`) |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en status `task_in_review`
- **APR-TL comment posteado** (`VTT.SKILL-COMMENT-003` cuando se migre)
- Revisión técnica aprobada (`VTT.SKILL-TASK-005` Paso 8 Opción A ya pasó)
- Modelo Dinámico aplicado (TIs creados, evidencias agregadas, devlog resolved — ver `PROTOCOL-ASG-001 §5.5.10`)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL
$AGENT_UUID                # = TL_UUID
$STATUS_COMPLETED_UUID     # aa5ceb90-5209-42a2-b874-a8cbee597a97 (fijo)
```

---

## Ejecución

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"statusId\": \"aa5ceb90-5209-42a2-b874-a8cbee597a97\",
    \"changedBy\": \"$AGENT_UUID\"
  }"
```

---

## Restricción

**Solo TL puede ejecutar esta skill.** El PM tiene su propia transición a `task_approved` (`VTT.SKILL-STATUS-004`).

El flujo correcto es:
```
task_in_review  →  task_completed (TL)  →  task_approved (PM)
                   ↑ ESTA SKILL          ↑ STATUS-004
```

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])"
# Esperado: task_completed
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `INVALID_TRANSITION` | Tarea no estaba en `task_in_review` | Verificar status — solo from `task_in_review` |
| HTTP 403 | UUID no es el TL del proyecto | Confirmar rol — esta skill es exclusiva del TL |
| Saltar APR-TL | No posteó comment antes | Postear APR-TL primero — regla operativa del review |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- `VTT.SKILL-TASK-005_review_tarea` (Paso 8 Opción A)
- Después de esta, `VTT.WORKFLOW-MAN-001.004_actualizar_task_manifest_v15` (generar v1.5)
- Después, `PROTOCOL-ASG-001 §5.5.bis FASE 4.5` (commit del TL en `tl/<TASK_ID>-close`)

---

## Cuándo NO usar esta Skill

- **Si los CAs no están todos `met` con evidencia** — rechazar (no completar)
- **Si hay issues abiertos** — resolver issues primero
- **Si falta Living Document declarado en el ASSIGNMENT** — rechazar
- **Si el manifest v1.0 del agente no está commiteado al PR** — rechazar (PROTOCOL-MAN-001 §5.3.7)

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-STATUS-03_task-completed-tl.md`. Contrato sin cambios. Cross-ref con WORKFLOW-MAN-001.004 + FASE 4.5 actualizado. |
