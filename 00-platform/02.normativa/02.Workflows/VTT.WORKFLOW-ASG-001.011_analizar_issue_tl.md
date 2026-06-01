# VTT.WORKFLOW-ASG-001.011 — TL analiza Issue y clasifica S1-S4

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.011` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.4.3 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | TL Reviewer al recibir notificación de Issue |
| **Reglas Nivel 0** | `RULE-SCRIPT-001`, `RULE-TEMPLATE-001` |
| **CARD asociada** | `VTT.CARD-ISS-003` |

---

## 1. Propósito

Análisis estructurado del Issue por el TL con clasificación operativa S1-S4 (matriz severity × impacto downstream). Desbloquea camino hacia `.037` (decidir acción).

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `issue_id` | UUID | |
| `tl_id` | UUID | |

## 3. Precondiciones

- Issue en `status=open`
- Tarea origen en `task_on_hold` con `onHoldIssueId = issue_id`
- Devlog `blocker` registrado

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Clasificación S1-S4 obligatoria |
| R2 | Responder ≤24h o escalar al PM |
| R3 | TL debe leer Issue + tarea + devlog completo ANTES de clasificar |
| R4 | S1/S2 → consultar PM antes de decidir |
| R5 | Análisis como comment estructurado para auditoría |
| R6 | Status Issue → `acknowledged` al iniciar análisis |

## 5. Pasos

### Paso 1 — Acknowledge
```bash
curl -X PATCH "$VTT_BASE_URL/api/issues/<ISSUE_ID>" \
  -d '{"status":"acknowledged","acknowledgedBy":"<TL_UUID>"}'
```

### Paso 2 — Leer contexto COMPLETO (R3)
- Issue completo
- Brief + ASSIGNMENT tarea origen
- Devlog `blocker` enlazado
- Otros devlogs relacionados

### Paso 3 — Clasificar S1-S4

Matriz:

| Issue.severity | + downstream | = Clasificación |
|---|---|---|
| critical | sí | **S1** |
| critical | no | **S2** |
| high | sí | **S2** |
| high | no | **S3** |
| medium | sí | **S3** |
| medium | no | **S4** |
| low | * | **S4** |

### Paso 4 — Si S1/S2 → consultar PM (R4)
```bash
curl -X POST "$VTT_BASE_URL/api/issues/<ISSUE_ID>/comments" \
  -d '{"comment":"@PM: Issue S<1|2> — consulta requerida.\nResumen: ...\nImpacto: ...\nOpciones: A/B/C","authorId":"<TL_UUID>"}'
```

Esperar PM antes de avanzar al `.037`.

### Paso 5 — Si S3/S4 → decisión unilateral
TL evalúa 4 opciones del `.037`: A correctiva / B inline / C workaround / D reject.

### Paso 6 — Análisis estructurado como comment (R5)

```markdown
## 🔍 Análisis ISS-<ID>

**Clasificación operativa:** S<X>
**Issue.severity:** <V>
**Impacto downstream:** <sí/no — qué tareas>

### Análisis
<causa raíz + opciones>

### Decisión
- Acción: <create_corrective_task | resolve_inline | accept_workaround | reject_issue>
- Justificación: <breve>
- Próximo: WORKFLOW-ASG-001.037

### Comunicación al agente
<mensaje claro>
```

### Paso 7 — Notificar agente
Comment en tarea origen.

### Paso 8 — Actualizar SPRINT_STATUS
Invocar `WORKFLOW-ASG-001.028` con `trigger_event=issue_created`.

## 6. Outputs

| Output | Descripción |
|---|---|
| `issue_status` | `acknowledged` (o `pm_consultation_pending`) |
| `severity_operational` | S1/S2/S3/S4 |
| `action_decided` | enum del `.037` |
| `analysis_comment_id` | UUID |
| `pm_consulted` | bool |

## 7. Validación

Análisis posteado + agente notificado + clasificación documentada.

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Clasificó sin leer contexto | Apuro | R3: re-leer + re-clasificar |
| S1/S2 sin consulta PM | Apuro | Revertir + consultar |
| Agente sin notificación | Olvido Paso 7 | Postear comment |

## 9. Skills invocadas

- `SKILL-ISSUE-002`, `SKILL-QUERY-001`, `SKILL-COMMENT-001`

## 10. Scripts invocados

- `SCRIPT-ISSUE-002_classify_severity.py`

## 11. Sub-workflows invocados

- `WORKFLOW-ASG-001.037` (siguiente)
- `WORKFLOW-ASG-001.028` (mantener_sprint_status)

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Matriz S1-S4. Análisis estructurado. SLA 24h. |
