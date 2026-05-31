# VTT.SKILL-DEV-001 — Registrar decisión en devlog

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-DEV-001` |
| **Categoría** | DEV (Devlog) |
| **Versión** | 1.1 |
| **Fecha** | 2026-05-22 |
| **Aplica a** | Todos los roles ejecutores |
| **Tokens estimados** | ~200 |
| **Cuándo se usa** | Para registrar decisiones técnicas o de producto durante la ejecución de una tarea — quedan vinculadas al review gate del cierre |
| **Reemplaza** | `SKL-DEVLOG-01_decision.md` (legacy) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `agent_uuid` | uuid | sí | UUID del agente (= `reportedBy`) |
| `title` | string ≤200 | sí | Título corto de la decisión |
| `description` | string ≤5000 | **sí (obligatorio)** | Descripción detallada: qué se decidió y por qué. **NO omitir** — sin description el TL no entiende el contexto y borra el entry (caso MS-333). |
| `severity` | enum | sí/no | `low` (default) / `medium` / `high` / `critical` |
| `impact_description` | string | sí/no | Áreas afectadas por la decisión |

> **Política de payload:** VTT usa el campo `categoryCode` para el tipo de entry (no `type` como decía el legacy). Para decisiones → `categoryCode: "decision"`.

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Tarea en status `task_in_progress` o `task_in_review`
- La decisión ya está tomada (esta skill registra, no propone)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID                # = reportedBy
```

---

## Ejecución

> **IMPORTANTE — Hay 2 endpoints distintos para POST.** Elegir según el caso:
>
> | Endpoint | Cuándo | Payload |
> |---|---|---|
> | `POST /api/tasks/$TASK_ID/devlog` (singular) | Registrar **1 entry** | Objeto directo `{categoryCode, title, ...}` |
> | `POST /api/tasks/$TASK_ID/devlog-entries` (plural) | Registrar **varias entries** en una sola llamada (batch) | Wrapper `{ "entries": [{...}, {...}] }` |

### Opción A — Registrar 1 decisión (recomendado, más simple)

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"categoryCode\": \"decision\",
    \"title\": \"$DECISION_TITLE\",
    \"description\": \"$DECISION_DESCRIPTION\",
    \"severity\": \"low\",
    \"reportedBy\": \"$AGENT_UUID\"
  }"
```

### Opción B — Registrar varias decisiones en batch

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog-entries" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"entries\": [
      {
        \"categoryCode\": \"decision\",
        \"title\": \"$DECISION_TITLE_1\",
        \"description\": \"$DECISION_DESCRIPTION_1\",
        \"severity\": \"low\",
        \"reportedBy\": \"$AGENT_UUID\"
      },
      {
        \"categoryCode\": \"decision\",
        \"title\": \"$DECISION_TITLE_2\",
        \"description\": \"$DECISION_DESCRIPTION_2\",
        \"severity\": \"medium\",
        \"reportedBy\": \"$AGENT_UUID\"
      }
    ]
  }"
```

> **Nota técnica:**
> - El campo `severity` debe ser **enum no-null** (low/medium/high/critical). NO usar `null` ni omitir el campo. Si no estás seguro → `low`.
> - El campo `description` es **obligatorio** (caso MS-333: decisions sin description fueron borradas por el TL).

---

## Cuándo registrar una decisión

| Caso | ¿Registrar? |
|---|---|
| Elegiste un patrón de diseño vs otro | ✅ Sí |
| Hay un trade-off explícito (ej. performance vs legibilidad) | ✅ Sí |
| Aplicaste una excepción a una regla de la SPEC | ✅ Sí (más con `impact_description`) |
| Cambiaste el approach respecto al BRIEF original | ✅ Sí — el TL necesita saber por qué |
| Solo seguiste el ASSIGNMENT al pie de la letra | ❌ No |
| Es una observación sin decisión activa | ❌ No — usar `VTT.SKILL-DEV-002` (observación) |

---

## Validación

```bash
# Confirmar que el entry quedó registrado
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
entries = json.load(sys.stdin).get('data', [])
decisions = [e for e in entries if (e.get('category') or {}).get('code') == 'decision' or e.get('categoryCode') == 'decision']
print(f'decisions: {len(decisions)}')
if decisions:
    last = decisions[-1]
    print(f'  last: {last.get(\"title\")}')
"
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| HTTP 400 `INVALID_TYPE` | Usar `type` en lugar de `categoryCode` | El backend usa `categoryCode`. Legacy decía `type` (deprecado) |
| HTTP 400 `severity null` | Omitir `severity` o pasar `null` | Default `low` siempre |
| HTTP 400 al hacer POST a `/devlog-entries` | Falta el wrapper `{ "entries": [...] }` | Si vas a registrar 1 sola entry → usar **Opción A** (`/devlog` singular con objeto directo). Si vas a registrar varias → usar **Opción B** con wrapper `entries[]` |
| HTTP 400 `description required` | Description faltante o vacía | `description` es **obligatorio** — agregar contexto del "por qué" (caso MS-333) |
| Endpoint 404 GET | Confundir endpoints | GET es siempre `/devlog` (singular). POST tiene 2 variantes: `/devlog` (1 entry) o `/devlog-entries` (batch con wrapper) |
| TL borró mi decision | Decision sin description o trivial | NO registrar decisions vacías. Si seguiste el ASSIGNMENT al pie de la letra → NO es decisión, NO registrar |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- Workflow del agente durante ejecución de tarea (siempre que tome decisión técnica)
- `VTT.WORKFLOW-MAN-001.003` Paso 3 — el agente lista sus devlog entries en el reporte SKL-REPORT-01

---

## Cuándo NO usar esta Skill

- **Si es solo observación (no decisión)** → usar `VTT.SKILL-DEV-002` (observation)
- **Si es bloqueante real** → usar `VTT.SKILL-ISS-001` (crear issue) — pone tarea en on_hold
- **Si es notificación al equipo** → usar `VTT.SKILL-COMMENT-001` (comment, no devlog)

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-DEVLOG-01_decision.md`. **Corrección crítica:** legacy decía `"type"` pero VTT backend usa `"categoryCode"`. También documenta el bug de `severity null` (debe ser enum no-null). Agrega tabla de cuándo registrar una decisión vs cuándo no. |
| 1.1 | 2026-05-20 | **Fixes reportados por BE de VTT tras incidente MS-333.** (1) `description` ahora marcado como **obligatorio** (estaba como "sí/no" — caso real: 3 decisions sin description tuvieron que borrarse por el TL). (2) **Bug crítico del ejemplo curl corregido:** la skill usaba `/devlog-entries` (plural) sin el wrapper `{entries: [...]}` requerido → HTTP 400 garantizado. Ahora documenta 2 endpoints distintos: **Opción A** `POST /devlog` (singular, 1 entry, payload directo, recomendado) y **Opción B** `POST /devlog-entries` (plural, batch, con wrapper). (3) Tabla de errores comunes ampliada con 3 nuevos casos: wrapper faltante, description required, TL borra decisions sin contexto. |
