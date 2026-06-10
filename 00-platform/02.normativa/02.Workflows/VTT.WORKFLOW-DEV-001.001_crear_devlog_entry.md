# VTT.WORKFLOW-DEV-001.001 — Crear devlog entry durante ejecución

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-DEV-001.001` |
| **Pertenece a** | `VTT.PROTOCOL-DEV-001` v1.1.0 §5.1 (FASE 1 — Creación durante ejecución) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-10 |
| **Autor** | TW-OPS (Technical Writer of Operational Processes) |
| **Aplica a** | Agentes ejecutores (BE/DB/FE/DO/QA/DL/UX/AR/SA), QA durante pase de testing, TL durante revisión propia |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por `PROTOCOL-DEV-001 §5.1.3` |

---

## 1. Propósito

Registrar una nueva **devlog entry** durante la ejecución de una tarea VTT, eligiendo correctamente la categoría del catálogo vivo y aplicando la matriz de 4 entidades (D-61) para no duplicar registro con findings/issues/TIs.

> **Cuándo se invoca:** durante `task_in_progress` o `task_in_review`, cada vez que el agente detecta un hecho que requiere trazabilidad (decisión técnica, observación, bloqueante, deuda, testing note, riesgo, etc.). Es la operación atómica de la FASE 1 del lifecycle.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `taskId` | string (`VTS-XXX` / `MS-XXX`) | Tarea VTT activa del agente | sí | ID de la tarea a la que pertenece la entry |
| `categoryCode` | enum (12 valores) | Catálogo vivo `GET /api/catalogs/devlog-categories` | sí | Una de las 12 categorías activas — ver §4 tabla |
| `title` | string ≤200 | Decisión del agente | sí | Título descriptivo del hecho |
| `description` | string ≤5000 | Decisión del agente | **sí (obligatorio)** | Descripción detallada con contexto del "por qué" — caso MS-333: entries sin description son borradas por el TL |
| `severity` | enum (`critical`/`high`/`medium`/`low`) o **omitir** | Decisión del agente según categoría | condicional | Solo si la categoría tiene `severityLevels ≠ []` — ver §4 nota crítica H-2 |
| `reportedBy` | UUID | Sesión del agente | sí | UUID del agente que crea la entry (mismo agente queda en `resolvedBy` cuando se transicione a `resolved` por backend) |

---

## 3. Precondiciones

- Token JWT válido (`VTT.SKILL-AUTH-001` ya ejecutado, `$TOKEN` cacheado).
- Tarea `taskId` existe en VTT y está asignada al agente (`assignedToId` = `reportedBy`).
- Tarea en estado `task_in_progress` o `task_in_review` (entries en otros estados serán rechazadas operativamente).
- Agente tiene capability `tasks.update` (verificado por el JWT emitido).
- El hecho a registrar **NO** es ninguna de las 3 entidades excluidas (ver §4 árbol de decisión P1-P3).

> **Si una precondición falla:** el endpoint retorna 401/403/404 — ver §8 Errores comunes.

---

## 4. Reglas del Workflow

### 4.1 Aplicar matriz D-61 antes de registrar (regla bloqueante)

Cada hecho durante la ejecución se mapea a **una** de las 4 entidades del Modelo Dinámico V4 (ver `PROTOCOL-DEV-001 §0`). Antes de invocar este Workflow, responder:

| Pregunta | Respuesta → Entidad → Acción |
|---|---|
| ¿Es un **HECHO** del proceso que no exige acción? | **Devlog entry** → seguir este Workflow |
| ¿Es un **hallazgo accionable** que el TL debe dictaminar? | **Finding** → invocar `POST /api/tasks/:id/findings` (NO este Workflow) |
| ¿Es un **bug** que impide cumplir los CAs de la tarea? | **Issue** `type=bug` → invocar `PROTOCOL-ASG-001 §5.4` (sub-ciclo bloqueante, NO este Workflow) |
| ¿Es un **compromiso del proyecto** cross-tarea / largo plazo? | **TrackableItem** → registrar como devlog primero y elevar a TI en FASE 3 (D-64) |

**D-62 (registro único):** prohibidos los pares espejo. No registrar el mismo hecho como devlog Y como finding/issue/TI al mismo tiempo.

### 4.2 Tabla canónica de 12 categorías del catálogo vivo

Esta tabla **debe consultarse** antes de elegir `categoryCode`. Es replica de `PROTOCOL-DEV-001 §3.1` para que el agente la tenga visible sin saltar de doc.

| `categoryCode` | `severityLevels` permitidos | Cuándo usar |
|---|---|---|
| `decision` | (sin severity — `[]`) | Decisión técnica activa con trade-off explícito |
| `observation` | (sin severity — `[]`) | Observación de comportamiento o contexto a documentar |
| `blocker` | critical/high/medium/low | Bloqueante real que detiene la tarea (si es bug de scope → preferir Issue) |
| `tech_debt` | critical/high/medium/low | Deuda técnica detectada — nota narrativa; lo accionable va a finding (D-62) |
| `testing_note` | critical/high/medium/low | Resultado de prueba o verificación (QA típicamente) |
| `risk` | critical/high/medium/low | Riesgo local identificado |
| `issue` | critical/high/medium/low | Inconsistencia narrativa — el bug accionable va a finding/issue |
| `question` | high/medium/low | Consulta del agente al TL no resoluble localmente — ver `PROTOCOL-ASG-001 §5.4.bis` |
| `dependency` | high/medium | Dependencia externa detectada entre tareas o sistemas |
| `improvement` | medium/low | Mejora propuesta para iteración futura |
| `feedback` | high/medium/low | Feedback recibido de stakeholder o usuario |
| `brand_issue` | critical/high/medium | Tema de adherencia a guías de marca |

> **⚠️ H-2 (confirmado VTS-026):** las categorías `decision` y `observation` declaran `severityLevels: []`. El backend **descarta silenciosamente** cualquier `severity` enviado en esas categorías (lo normaliza a `null` sin retornar warning ni 400). **NO incluir el campo `severity` en payloads de `decision` u `observation`** — confiar en severity en esas categorías no bloquea el Review Gate aunque se envíe `high`/`critical`.

### 4.3 Convenciones

- **`description` obligatorio con contexto del por qué.** Una entry sin `description` o solo con la decisión sin razón es candidata a borrado por el TL (`VTT.SKILL-DEV-005` con comment de trazabilidad previo).
- **NO transicionar la entry** a estado terminal desde este Workflow. La entry nace `pending`; la transición la hace el TL en FASE 3 (ver `VTT.WORKFLOW-DEV-001.002`) o el PM al cierre del sprint (ver `VTT.WORKFLOW-DEV-001.003`).
- **Para registrar varias entries en lote:** usar la Opción B de §5 (endpoint plural con wrapper `{entries:[]}`). Para 1 entry, usar la Opción A (endpoint singular con objeto directo) — es la recomendada.

---

## 5. Pasos

### Paso 1 — Identificar tipo de evento

El agente detecta uno de los 7 tipos de evento descritos en `PROTOCOL-DEV-001 §5.1.1`:

| Evento detectado | Pre-elección de `categoryCode` |
|---|---|
| Decisión técnica con trade-off explícito | `decision` |
| Observación de comportamiento / contexto | `observation` |
| Bloqueante que detiene avance | `blocker` |
| Deuda técnica fuera de scope | `tech_debt` |
| Resultado de testing | `testing_note` |
| Riesgo potencial | `risk` |
| Inconsistencia narrativa | `issue` |

Si el evento encaja en una de las 5 categorías agregadas en v1.1.0 (`question`, `dependency`, `improvement`, `feedback`, `brand_issue`), elegir esa según la tabla §4.2.

### Paso 2 — [DECISIÓN] ¿devlog, finding, issue o TI?

Aplicar el árbol P1-P3 de `PROTOCOL-DEV-001 §0` + `GUIA_DEVLOG_FINDINGS §0.1`:

¿Bloquea cumplimiento de CAs de esta tarea? →
- **SÍ** → **NO es devlog.** Es Issue `type=bug` por `PROTOCOL-ASG-001 §5.4`. Salir de este Workflow.
- **NO** → continuar Paso 3.

¿Exige decisión accionable del TL (no es un hecho cerrado)? →
- **SÍ** → **NO es devlog.** Es Finding (`POST /api/tasks/:id/findings`). Salir de este Workflow.
- **NO** → continuar Paso 3 (es un hecho → devlog correcto).

### Paso 3 — Verificar matriz D-61 (anti-duplicación)

Antes de crear: confirmar que el mismo hecho **NO** está ya registrado como finding/issue/TI. Si existe, este registro como devlog viola D-62 (pares espejo) — abortar y referenciar el registro original.

### Paso 4 — [DECISIÓN] ¿severity aplica a esta categoría?

Consultar §4.2:

- Si `categoryCode ∈ {decision, observation}` → **OMITIR el campo `severity` en el payload** (H-2: backend lo normaliza a null silenciosamente).
- Si `categoryCode ∈ {blocker, tech_debt, testing_note, risk, issue, question, dependency, improvement, feedback, brand_issue}` → incluir `severity` con un valor permitido por la tabla `severityLevels` de la categoría.

### Paso 5 — Invocar la Skill según tipo de evento

→ invoca **`VTT.SKILL-DEV-001`** (registrar decisión) si `categoryCode = decision`
→ invoca **`VTT.SKILL-DEV-002`** (registrar observación) si `categoryCode = observation`
→ para las otras 10 categorías: invocar `VTT.SKILL-DEV-001` o `VTT.SKILL-DEV-002` con `categoryCode` parametrizado (ambas Skills aceptan cualquier `categoryCode` del catálogo vivo — solo cambian la severity default y la semántica documental)

> **Comando atómico (Opción A — recomendada para 1 entry):**
>
> ```bash
> curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer $TOKEN" \
>   -d "{
>     \"categoryCode\": \"$CATEGORY_CODE\",
>     \"title\": \"$TITLE\",
>     \"description\": \"$DESCRIPTION\",
>     \"severity\": \"$SEVERITY\",   // omitir esta linea si categoria es decision/observation
>     \"reportedBy\": \"$AGENT_UUID\"
>   }"
> ```

### Paso 6 — Validar respuesta del backend

Backend retorna HTTP 200 con la entry creada:

```json
{
  "data": {
    "id": "<UUID>",
    "taskId": "<task_id>",
    "categoryCode": "<categoria>",
    "severity": null o "<severity>",   // null para decision/observation por catalogo
    "title": "...",
    "description": "...",
    "status": "pending",
    "reportedBy": "<agent_uuid>",
    "resolvedAt": null,
    "resolvedBy": null,
    "resolution": null,
    "deferredToPhaseId": null,
    "fixTaskId": null,
    "createdAt": "...",
    "updatedAt": "..."
  }
}
```

Capturar `data.id` (UUID de la entry) — necesario para futuras invocaciones de `VTT.WORKFLOW-DEV-001.002` (editar/transicionar).

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| Entry persistida | record VTT en `task_devlog_entries` | BD del backend VTT | Entry con `status:pending`, vinculada a `taskId` |
| `entryId` | UUID | Variable de sesión del agente | ID retornado por el backend, necesario para tracking posterior |
| Trazabilidad en feed | activity entry | Backend VTT | El backend registra automáticamente la creación en el activity feed de la tarea |

---

## 7. Validación de salida

```bash
# Check 1: la entry aparece en GET /devlog de la tarea
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
entries = json.load(sys.stdin).get('data', [])
match = [e for e in entries if e.get('id') == '$ENTRY_ID']
print('OK' if match else 'NOT FOUND')
if match:
    e = match[0]
    print(f\"categoryCode: {e.get('categoryCode')}\")
    print(f\"status: {e.get('status')}\")
    print(f\"description len: {len(e.get('description') or '')}\")
"

# Check 2: la entry NO bloquea el review gate de forma indebida
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/review-gate" -H "Authorization: Bearer $TOKEN"
# Esperado: si severity high/critical → blocker aparece. Si decision/observation → sin blocker.
```

Lista verificable:

- [ ] Entry creada con `status: pending`
- [ ] `description` NO vacío (≥1 char)
- [ ] `severity` consistente con `severityLevels` de la categoría (null para `decision`/`observation`)
- [ ] La entry aparece en `GET /devlog` con `id` retornado

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| HTTP 400 `INVALID_CATEGORY` `"Categoria 'X' no existe"` | `categoryCode` fuera del catálogo vivo de 12 valores | Consultar `GET /api/catalogs/devlog-categories` y usar uno de los 12 valores activos |
| HTTP 400 `description required` | `description` faltante o string vacío | Agregar contexto del por qué (≥1 char, recomendado ≥50 chars) |
| HTTP 400 al hacer POST a `/devlog-entries` (plural) | Falta wrapper `{ "entries": [...] }` | Para 1 entry usar `/devlog` (singular) con objeto directo. Para varias usar `/devlog-entries` con wrapper |
| `severity` enviada queda en `null` post-creación | Categoría tiene `severityLevels: []` (H-2: decision/observation) | Comportamiento BY-DESIGN. Omitir `severity` en el payload para evitar confusión |
| TL borró la entry días después | Entry con `description` trivial o vacío (MS-333) | NO crear entries sin contexto. Si seguiste el ASSIGNMENT al pie de la letra → NO es decisión, NO registrar |
| HTTP 401 / 403 | JWT inválido o sin capability `tasks.update` | Renovar JWT con `VTT.SKILL-AUTH-001` (L8: JWT cacheado puede tener capabilities viejas) |
| HTTP 404 | `taskId` incorrecto o tarea no existe | Verificar `taskId` con `GET /api/tasks/:id` |

---

## 9. Skills invocadas

| Skill | Para qué se usa en este Workflow |
|---|---|
| `VTT.SKILL-AUTH-001` | Obtener `$TOKEN` JWT antes del POST |
| `VTT.SKILL-DEV-001` (decision) | Registrar entry `categoryCode=decision` (o cualquier categoría usando el endpoint singular) |
| `VTT.SKILL-DEV-002` (observation) | Registrar entry `categoryCode=observation` (o cualquier categoría usando el endpoint singular) |

> Las Skills DEV-001 y DEV-002 son intercambiables operativamente — ambas hacen `POST /api/tasks/:id/devlog`. La diferencia es semántica/documental (qué payload típico se documenta en cada Skill). Para `decision` invocar DEV-001; para `observation` invocar DEV-002; para las otras 10 categorías invocar la que sea — el `categoryCode` es el que determina la categoría real en la BD.

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-SEC-001` No postear datos sensibles en VTT | El `description` de la entry queda visible a cualquier usuario autenticado. Prohibido incluir IPs prod, credenciales, paths absolutos sensibles. Ver `OPERATIVO_TW-OPS §11` para detalle. |
| `RULE-DATA-001` Prohibido mockear datos | Si el agente detecta datos faltantes (catálogo vacío, configuración incompleta), debe crear `blocker` en devlog Y abrir Issue `type=blocker` por `PROTOCOL-ASG-001 §5.4` — NO improvisar valores ficticios. |
| `RULE-AGENT-001` Worktree por rol | El agente registra entries operando desde su worktree de rol — el `reportedBy` del JWT debe coincidir con el dueño del worktree. |

> Para descubrir reglas adicionales aplicables al contexto del agente: `python 00.Rules/query_rules.py --simulate-task <TASK_ID>`.

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-06-10 | TW-OPS (VTS-027) — revisión LEAD_NPL | Versión inicial. Materializa FASE 1 del `PROTOCOL-DEV-001 v1.1.0` §5.1. Incorpora: matriz D-61/D-62 (regla 4.1) + tabla canónica de 12 categorías del catálogo vivo (regla 4.2) + nota crítica H-2 sobre `severity` ignorada en `decision`/`observation` + Opción A endpoint singular recomendada para 1 entry. Skills invocadas: DEV-001 (decision) / DEV-002 (observation) / AUTH-001. Origen: reporte VTS-026 §4.1 + bump Protocol VTS-051. |
