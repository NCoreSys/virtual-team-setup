# VTT.SKILL-DEV-002 — Registrar observación en devlog

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-DEV-002` |
| **Categoría** | DEV (Devlog) |
| **Versión** | 1.1 |
| **Fecha** | 2026-05-20 |
| **Aplica a** | Todos los roles ejecutores |
| **Tokens estimados** | ~180 |
| **Cuándo se usa** | Para registrar observaciones, hallazgos o notas técnicas durante la ejecución (no son decisiones ni bloqueantes) |
| **Reemplaza** | `SKL-DEVLOG-02_observacion.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `agent_uuid` | uuid | sí | UUID del agente (= `reportedBy`) |
| `title` | string ≤200 | sí | Título de la observación |
| `description` | string ≤5000 | sí | Descripción detallada |
| `severity` | enum | sí/no | `low` (default) / `medium` / `high` / `critical` |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en status `task_in_progress` o `task_in_review`

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID
```

---

## Ejecución

> **IMPORTANTE — 2 endpoints distintos para POST.** Ver `VTT.SKILL-DEV-001 §Ejecución` para detalle completo:
>
> | Endpoint | Cuándo | Payload |
> |---|---|---|
> | `POST /api/tasks/$TASK_ID/devlog` (singular) | Registrar **1 entry** | Objeto directo |
> | `POST /api/tasks/$TASK_ID/devlog-entries` (plural) | Registrar **varias** en batch | Wrapper `{ "entries": [...] }` |

### Opción A — Registrar 1 observación (recomendado)

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"categoryCode\": \"observation\",
    \"title\": \"$OBS_TITLE\",
    \"description\": \"$OBS_DESCRIPTION\",
    \"severity\": \"low\",
    \"reportedBy\": \"$AGENT_UUID\"
  }"
```

### Opción B — Registrar varias observaciones en batch

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog-entries" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"entries\": [
      { \"categoryCode\": \"observation\", \"title\": \"...\", \"description\": \"...\", \"severity\": \"low\", \"reportedBy\": \"$AGENT_UUID\" },
      { \"categoryCode\": \"observation\", \"title\": \"...\", \"description\": \"...\", \"severity\": \"medium\", \"reportedBy\": \"$AGENT_UUID\" }
    ]
  }"
```

> **Nota técnica:**
> - `severity` enum no-null obligatorio (mismo issue que DEV-001). Default `low`.
> - `description` es **obligatorio** — sin descripción la observación pierde valor para el TL.
> - Si usás `/devlog-entries` (plural) **sin** el wrapper `{ entries: [...] }` → HTTP 400.

---

## Cuándo registrar una observación

| Caso | ¿Registrar? |
|---|---|
| Detectaste deuda técnica preexistente (no introducida por tu tarea) | ✅ Sí — `severity: medium` típicamente |
| Patrón mejorable que viste pero no es alcance de esta tarea | ✅ Sí |
| Vulnerabilidad/error en otro módulo | ✅ Sí — `severity: high` o `critical` |
| El SPEC no especifica un caso edge y resolviste de forma X | ✅ Mejor `decision` con `VTT.SKILL-DEV-001` |
| Trade-off menor que tomaste | Decision → `VTT.SKILL-DEV-001` |
| Bloqueante real | Issue → `VTT.SKILL-ISS-001` |

---

## Validación

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
entries = json.load(sys.stdin).get('data', [])
obs = [e for e in entries if (e.get('category') or {}).get('code') == 'observation' or e.get('categoryCode') == 'observation']
print(f'observations: {len(obs)}')
"
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `categoryCode invalid` | Usar `type` o `observation_type` | Usar `categoryCode: "observation"` exacto |
| Observación trivial registrada | Esta skill se usa de más | Pasar a un comment con `VTT.SKILL-COMMENT-001` si no es relevante para el cierre |
| Observación high/critical sin acción | Detectaste algo grave pero solo lo registraste | Considerar abrir issue con `VTT.SKILL-ISS-001` adicional |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- Workflow del agente durante ejecución
- `VTT.WORKFLOW-MAN-001.003` Paso 3 — listado en SKL-REPORT-01

---

## Cuándo NO usar esta Skill

- **Si es decisión técnica activa** → `VTT.SKILL-DEV-001`
- **Si es bloqueante** → `VTT.SKILL-ISS-001`
- **Si es comunicación al equipo** → `VTT.SKILL-COMMENT-001`

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-DEVLOG-02_observacion.md`. Misma corrección del bug `categoryCode` y `severity` que en DEV-001. Tabla de cuándo usar observation vs otras categorías. |
| 1.1 | 2026-05-20 | **Mismo fix que DEV-001 v1.1.** El ejemplo curl usaba `/devlog-entries` (plural) **sin el wrapper requerido** `{ entries: [...] }` → HTTP 400. Ahora documenta 2 endpoints: Opción A `/devlog` (singular, 1 entry) y Opción B `/devlog-entries` (batch con wrapper). Reportado por BE de VTT tras incidente MS-333. |
