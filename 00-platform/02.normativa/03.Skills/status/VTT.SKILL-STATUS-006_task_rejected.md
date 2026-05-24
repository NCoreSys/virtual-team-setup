# VTT.SKILL-STATUS-006 — Rechazar tarea (`task_rejected`, solo PM)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-STATUS-006` |
| **Categoría** | STATUS (Status transitions) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | **PM únicamente** |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | Cuando la revisión funcional NO cumple los Acceptance Criteria — `task_completed` regresa a `task_rejected` |
| **Reemplaza** | `SKL-STATUS-06_task-rejected-pm.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `pm_uuid` | uuid | sí | UUID del PM (= `changedBy`) |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en status `task_completed` (post-aprobación TL pero antes de PM)
- **OBLIGATORIO: comment con feedback específico posteado ANTES** (`VTT.SKILL-COMMENT-001`)

> **Regla:** rechazar sin feedback puntual genera fricción innecesaria. El agente debe saber **exactamente** qué corregir.

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL
$AGENT_UUID                # = PM_UUID
$STATUS_REJECTED_UUID      # 335fd9c6-f0d6-4966-a6ea-f518c78bc422 (NOTA: mismo UUID que task_pending — VTT los distingue por contexto)
```

> ⚠️ **Observación del backend:** el UUID `335fd9c6-f0d6-4966-a6ea-f518c78bc422` se usa tanto para `task_pending` (estado inicial) como `task_rejected` (post-completed). VTT distingue por contexto: si la tarea estaba en `task_completed` → `task_rejected`; si está nueva → `task_pending`.

---

## Ejecución

```bash
# 1. Postear comment con feedback específico ANTES
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"message\": \"RECHAZO-PM: CAs no cumplidos. Items a corregir:\n1. $ITEM_1\n2. $ITEM_2\nVolver a in_review tras corregir.\",
    \"userId\": \"$AGENT_UUID\"
  }"

# 2. Cambiar status a task_rejected
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"statusId\": \"335fd9c6-f0d6-4966-a6ea-f518c78bc422\",
    \"changedBy\": \"$AGENT_UUID\"
  }"
```

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['statusCode'])"
# Esperado: task_rejected
```

```bash
# Check que el comment de feedback está
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
comments = json.load(sys.stdin)['data']
rejection = [c for c in comments if 'RECHAZO' in (c.get('message') or '').upper()]
print('rejection_comments:', len(rejection))
"
# Esperado: >= 1
```

---

## Restricción

**Solo PM puede ejecutar esta skill.**

El TL **NO puede rechazar a `task_rejected`** — el TL solo puede:
- Aprobar al pasar a `task_completed` (`VTT.SKILL-STATUS-003`)
- Rechazar internamente devolviendo a `task_in_review` con un comment de feedback (sin cambiar status)
- Escalar bloqueante con `VTT.SKILL-STATUS-005` (on_hold)

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Rechazar sin comment | Saltar Paso 1 | El agente no sabe qué corregir — postear feedback ANTES |
| HTTP 400 `INVALID_TRANSITION` | Tarea no estaba en `task_completed` | Verificar — solo se rechaza post-TL |
| HTTP 403 | UUID no es el PM | Confirmar rol |
| Rechazar y aprobar después sin re-review | Inconsistencia | Si el agente corrige, vuelve a `task_in_review` y reinicia el flujo |
| UUID compartido con pending confunde | Comportamiento normal de VTT | Verificar contexto: si venía de `task_completed`, es `task_rejected` |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-COMMENT-001` — para el comment de feedback obligatorio

---

## Flujo después del rechazo

```
task_rejected  →  agente lee comment de feedback
              →  corrige código
              →  vuelve a task_in_progress (manualmente con STATUS-001 o regresa al worktree)
              →  task_in_review (STATUS-002 cuando termine)
              →  task_completed (TL con STATUS-003)
              →  task_approved (PM con STATUS-004)
```

---

## Cuándo NO usar esta Skill

- **Si la tarea tiene CAs cumplidos pero hay observación menor** — postear comment al TL para que rectifique antes (`task_in_review` re-abierto manualmente)
- **Si el problema es deuda técnica no bloqueante** — aprobar + crear tarea nueva de fix
- **Si hay duda sobre el alcance** — discutir con el TL/agente antes de rechazar

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-STATUS-06_task-rejected-pm.md`. Contrato sin cambios. Ampliación: explicación del UUID compartido con `task_pending` (distinción por contexto del backend) y flujo completo post-rechazo. |
