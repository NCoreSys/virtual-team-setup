# VTT.CARD-ISS-003 — TL analiza Issue y clasifica S1-S4

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-ISS-003` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role = TL` |
| **Requiere Cards previas** | ninguna |
| **Pertenece a** | WORKFLOW-ASG-001.011 |
| **Tokens estimados** | ~1,050 |

---

## Qué hacer (TL)

Cuando recibís notificación de Issue creado por agente, analizar dentro de **24h máximo** (si tardás más, escalar al PM).

## Paso 1 — Acknowledge

```bash
curl -X PATCH "$VTT_BASE_URL/api/issues/<ISSUE_ID>" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{"status":"acknowledged","acknowledgedBy":"<TL_UUID>"}'
```

## Paso 2 — Leer contexto COMPLETO antes de clasificar

- Issue completo (Síntoma + Intentado + Solicitud + Impacto)
- Brief y ASSIGNMENT de la tarea origen
- Devlog `blocker` enlazado al Issue
- Otros devlogs relacionados

NO clasificar "desde el título".

## Paso 3 — Clasificar S1-S4 (matriz)

| Issue.severity | + downstream | = Clasificación | Acción |
|---|---|---|---|
| critical | sí | **S1** | Consultar PM inmediato + resolución express |
| critical | no | **S2** | Consultar PM + correctiva P0 |
| high | sí | **S2** | Consultar PM + correctiva P0 |
| high | no | **S3** | Decisión TL: correctiva o inline |
| medium | sí | **S3** | Decisión TL |
| medium | no | **S4** | Decisión TL: workaround posible |
| low | * | **S4** | Aceptar workaround + tech_debt |

## Paso 4 — Si S1/S2 → consultar PM ANTES de decidir acción

```bash
curl -X POST "$VTT_BASE_URL/api/issues/<ISSUE_ID>/comments" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{
    "comment": "@PM: Issue S<1|2> — consulta requerida.\nResumen: <síntoma>\nImpacto downstream: <tareas afectadas>\nOpciones contempladas: <A/B/C>",
    "authorId": "<TL_UUID>"
  }'
```

Esperar respuesta del PM antes de pasar a CARD-ISS-004.

## Paso 5 — Si S3/S4 → decisión unilateral del TL

Evalúa internamente las 4 opciones:
- A `create_corrective_task` — tarea hija con `sourceIssueId`
- B `resolve_inline` — agente arregla en la misma tarea
- C `accept_workaround` + tech_debt — TI creado para sprint futuro
- D `reject_issue` — Issue no aplica

## Paso 6 — Postear análisis estructurado como comment

```markdown
## 🔍 Análisis ISS-<ID>

**Clasificación operativa:** S<X>
**Issue.severity:** <V>
**Impacto downstream:** <sí/no — qué tareas>

### Análisis
<causa raíz + opciones consideradas>

### Decisión
- Acción: <create_corrective_task | resolve_inline | accept_workaround | reject_issue>
- Justificación: <breve>
- Próximo: CARD-ISS-004 (WORKFLOW-ASG-001.037)

### Comunicación al agente
<mensaje claro>
```

Postear como comment en el Issue + comment notificación en tarea origen.

## Paso 7 — Actualizar SPRINT_STATUS

Invocar **CARD-EXE-009** con `trigger_event=issue_created`.

## Si falla

| Síntoma | Acción |
|---|---|
| TL clasificó sin leer contexto | Re-leer + re-clasificar (no apurarse) |
| S1/S2 sin consulta PM | Revertir + consultar PM |
| Agente sin notificación | Postear comment en tarea origen |
| Issue queda en `open` | PATCH status → `acknowledged` |

## Output

Issue en `acknowledged` + clasificación S1-S4 + análisis estructurado + acción decidida. Próximo: **CARD-ISS-004** (ejecutar acción).
