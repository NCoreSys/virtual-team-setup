# VTT.SKILL-COMMENT-003 — APR-TL (Aprobación técnica del TL)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-COMMENT-003` |
| **Categoría** | COMMENT (Comments) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | **TL Reviewer únicamente** |
| **Tokens estimados** | ~250 |
| **Cuándo se usa** | Al aprobar técnicamente — **ejecutar ANTES de `VTT.SKILL-STATUS-003`** (mover a `task_completed`) |
| **Reemplaza** | `SKL-COMMENT-03_apr-tl.md` (legacy) |
| **Template asociado** | `03.templates/normativa/VTT.TEMPLATE-APR-001_apr_tl_comment.md` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `tl_uuid` | uuid | sí | UUID del TL |
| `verifications` | object | sí | Resultado de las 8 verifications (review gate, CAs, LDs, hardcode, deliverables, dynamic_model, worktree discipline, allowed paths) |
| `dynamic_model_summary` | string | sí | Resumen de las 4 acciones del modelo dinámico aplicadas (TIs nuevos, evidencias, devlog resolved) |
| `findings` | array | sí/no | Items que se aprobaron con observación (no rechazo, pero queda registro) |
| `notas` | string | sí/no | Notas adicionales del TL |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en status `task_in_review`
- **Las 11 precondiciones del Workflow MAN-001.004 cumplidas:**
  - Review Gate verificado (`canProceedToReview=true`)
  - CAs todos en `met` con evidencia
  - Attachments completos (brief, assignment, devlog, code_logic, manifest v1.0)
  - PRs verificados en GitHub
  - Disciplina de worktree verificada (diff respeta `allowedPaths`)
  - Living Documents declarados
  - Hardcode Check verificado
  - Code review técnico aprobado
  - Modelo Dinámico aplicado (TIs + evidencias + devlog resolved)
  - Status sigue en `task_in_review` (todavía no movido)
  - Manifest v1.0 del agente commiteado al PR (`PROTOCOL-MAN-001 §5.3.7`)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID                # = TL_UUID
```

---

## Formato del mensaje (template)

```
APR-TL: revisión técnica aprobada.

Verificaciones:
- Review gate: ✅
- Acceptance Criteria: <met>/<total> ✅
- Living Documents declarados: ✅ (LD-XX, LD-YY)
- Hardcode Check: ✅ (criticals=0, fps=N justificados)
- Deliverables matchean assignment: ✅
- Worktree discipline: ✅ (diff dentro de allowedPaths)
- Dynamic Model aplicado: ✅
  - TIs nuevos creados: <N>
  - Evidencias agregadas: <N>
  - Devlog entries resolved: <N>

Findings (no bloqueantes):
- <item 1>
- <item 2>

Notas: <notas opcionales>
```

> **Ver template oficial:** `$VTT_SETUP/03.templates/normativa/VTT.TEMPLATE-APR-001_apr_tl_comment.md`

---

## Ejecución

```bash
# Construir el mensaje (típicamente desde el resultado del review en VTT.SKILL-TASK-005)
APR_MESSAGE=$(cat <<EOF
APR-TL: revisión técnica aprobada.

Verificaciones:
- Review gate: ✅
- Acceptance Criteria: $CAS_MET/$CAS_TOTAL ✅
- Living Documents declarados: $LDS_STATUS
- Hardcode Check: $HARDCODE_STATUS
- Deliverables matchean assignment: ✅
- Worktree discipline: ✅
- Dynamic Model aplicado: ✅
  - TIs nuevos creados: $NEW_TIS
  - Evidencias agregadas: $NEW_EVIDENCES
  - Devlog entries resolved: $DEVLOG_RESOLVED

Findings (no bloqueantes):
$FINDINGS

Notas: $NOTAS
EOF
)

# Postear comment con tipo 'approval'
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
# Capturar el comment_id del response (se usa en el manifest v1.5)
APR_COMMENT_ID=$(curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
cs = json.load(sys.stdin).get('data', [])
apr_tl = [c for c in cs if 'APR-TL' in (c.get('message') or '')]
if apr_tl:
    print(apr_tl[-1]['id'])  # más reciente
")
echo "APR_COMMENT_ID=$APR_COMMENT_ID"
# Esperado: UUID válido — se inyecta en el manifest v1.5 (review.tl_review.comment_id)
```

---

## Restricción

**Solo TL puede ejecutar esta skill.**

El PM tiene su propia aprobación con `VTT.SKILL-COMMENT-002` (APR-PM), que se postea **DESPUÉS** del APR-TL.

Flujo:
```
TL: APR-TL (esta skill)  →  STATUS-003 (task_completed)
                          →  WORKFLOW-MAN-001.004 (v1.5 con apr_tl_comment_id)
                          →  FASE 4.5 (commit del TL)
PM: APR-PM (COMMENT-002)  →  STATUS-004 (task_approved)
```

---

## Reglas críticas

- ❌ NUNCA aprobar con CA `not_met` o `pending` (rechazar con feedback)
- ❌ NUNCA aprobar con Living Document faltante
- ❌ NUNCA aprobar con hardcode finding crítico/alto sin justificar
- ❌ NUNCA aprobar antes de aplicar el Modelo Dinámico
- ❌ NUNCA aprobar antes de generar el v1.5 del manifest — el `apr_tl_comment_id` se necesita ahí
- ✅ Postear APR-TL **ANTES** del PATCH de status

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Aprobar antes del Modelo Dinámico | Saltar paso del review | Aplicar dynamic_model primero, después APR-TL |
| `apr_tl_comment_id` perdido | No se capturó del response | Usar query post-POST como en §Validación |
| HTTP 400 con JSON anidado | Newlines sin escapar en heredoc | Usar `json.dumps` para serializar correctamente |
| Aprobar pero LD faltante | Saltar verificación #6 | Rechazar — esta es regla crítica |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-TASK-005_review_tarea` Paso 8 Opción A — esta skill se ejecuta como parte de "Aprobar"

---

## Skills que invocan ESTA

- `VTT.SKILL-TASK-005` Paso 8 Opción A (aprobar) — esta skill se ejecuta primero
- Después de esta: `VTT.SKILL-STATUS-003` (mover a `task_completed`)
- Después de status: `VTT.WORKFLOW-MAN-001.004` (generar manifest v1.5 con `comment_id` capturado aquí)

---

## Cuándo NO usar esta Skill

- **Si vas a rechazar** — usar `VTT.SKILL-COMMENT-001` con feedback específico, sin cambiar status
- **Si hay observación menor pero aprobas igual** — agregar en sección `Findings (no bloqueantes)` del template

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-COMMENT-03_apr-tl.md`. Ampliación mayor: template estructurado con 8 verifications (matchea las del manifest v1.5) + sección dinámica del Modelo Dinámico + captura del `apr_tl_comment_id` (que se usa en `review.tl_review.comment_id` del v1.5). |
