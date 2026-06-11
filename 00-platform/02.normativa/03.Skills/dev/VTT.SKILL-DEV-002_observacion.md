# VTT.SKILL-DEV-002 — Registrar observación en devlog

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-DEV-002` |
| **Categoría** | DEV (Devlog) |
| **Versión** | 1.2 |
| **Fecha** | 2026-06-10 |
| **Aplica a** | Todos los roles ejecutores |
| **Tokens estimados** | ~200 |
| **Cuándo se usa** | Para registrar observaciones, hallazgos o notas técnicas durante la ejecución (no son decisiones ni bloqueantes) |
| **Reemplaza** | `SKL-DEVLOG-02_observacion.md` (legacy) |
| **Pertenece a** | `VTT.WORKFLOW-DEV-001.001` (FASE 1 del `VTT.PROTOCOL-DEV-001` v1.1.0) |
| **Acepta** | Cualquier `categoryCode` del catálogo vivo de 12 valores (`PROTOCOL-DEV-001 v1.1.0 §3.1`). Esta Skill y DEV-001 son **intercambiables operativamente** — ambas hacen `POST /api/tasks/:id/devlog`; la diferencia es semántica del payload típico documentado. **NO se crean Skills nuevas por categoría** (anti-pattern 1 de `GUIA_AUTOR` — decisión VTS-026 §4.2 + VTS-028). |

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
$VTT_BASE_URL              # https://api.vttagent.com  (siempre dominio — RULE-SEC-001 prohibe IP)
$AGENT_UUID
```

> **⚠️ Drift IP corregido en v1.2 (VTS-028):** versiones anteriores (≤v1.1) documentaban `$VTT_BASE_URL=http://77.42.88.106:3000` (IP de dev/staging). Esto **violaba RULE-SEC-001** que exige usar el dominio `https://api.vttagent.com` siempre. Hallazgo registrado en reporte VTS-026 Anexo C.

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

### Notas técnicas

#### ⚠️ H-2 — `severity` ignorada silenciosamente en `observation` (corregido v1.2)

**Hallazgo H-2 confirmado empíricamente VTS-026 §2.1.2:**

El catálogo vivo de devlog categories declara `severityLevels: []` para `categoryCode: "observation"`. El backend **descarta silenciosamente** cualquier `severity` enviado — la normaliza a `null` sin retornar warning ni HTTP 400.

```bash
# Payload enviado por el cliente:
POST /api/tasks/.../devlog
{ "categoryCode": "observation", "severity": "high", ... }

# Respuesta del backend:
{ "data": { "categoryCode": "observation", "severity": null, ... } }
#                                                     ^^^^^ silenciosamente descartada
```

**Recomendación operativa v1.2:** **OMITIR el campo `severity`** en payloads de `observation`. Confiar en severity para `observation` no bloquea el Review Gate aunque se envíe `high`/`critical` — la severity efectiva en BD será siempre `null`.

> Versiones ≤v1.1 decían "severity enum no-null obligatorio" — **incorrecto**. Documentación corregida en v1.2 con base en validación empírica VTS-026.

#### Otras notas técnicas

- `description` es **obligatorio** — sin descripción la observación pierde valor para el TL.
- Si usás `/devlog-entries` (plural) **sin** el wrapper `{ entries: [...] }` → HTTP 400.
- Esta Skill acepta cualquier `categoryCode` del catálogo vivo de 12 valores (ver `PROTOCOL-DEV-001 v1.1.0 §3.1`). El nombre "observation" es semántico — para `decision` invocar `DEV-001` por convención (mismo endpoint singular).

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
| 1.2 | 2026-06-10 | **Bump VTS-028 sobre hallazgos VTS-026 + alineación con Protocol DEV-001 v1.1.0** (mismo perfil de cambios que DEV-001 v1.2). (1) **Drift IP corregido (RULE-SEC-001):** `$VTT_BASE_URL` cambia de `http://77.42.88.106:3000` a `https://api.vttagent.com`. Hallazgo VTS-026 Anexo C. (2) **H-2 documentado correctamente:** la "Nota técnica" v1.1 decía "severity enum no-null obligatorio" — incorrecto para `observation`. El catálogo vivo declara `severityLevels: []` para `observation` y el backend descarta silenciosamente cualquier severity enviado. Validación empírica VTS-026 §2.1.2. Recomendación operativa: **omitir `severity`** en payloads de `observation`. (3) Header agrega "Pertenece a `VTT.WORKFLOW-DEV-001.001`". (4) Aclaración explícita: esta Skill acepta cualquier `categoryCode` del catálogo vivo de 12 valores. **NO se crean Skills nuevas DEV-006..010 por categoría** (decisión VTS-026 §4.2 + VTS-028). DEV-001 y DEV-002 son intercambiables operativamente. |
