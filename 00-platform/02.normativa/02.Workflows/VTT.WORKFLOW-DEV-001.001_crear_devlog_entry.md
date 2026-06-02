# VTT.WORKFLOW-DEV-001.001 — Crear devlog entry

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-DEV-001.001` |
| **Pertenece a** | `VTT.PROTOCOL-DEV-001` §5.1 (FASE 1 — Creación durante ejecución) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-02 |
| **Autor** | TW-OPS (auditoría VTS-007) |
| **Aplica a** | Agente ejecutor (BE/DB/FE/DO/QA/DL/UX/AR/SA) y QA durante pase de testing |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por Protocol padre §5.1.3 |
| **CARD asociada** | `VTT.CARD-DEV-001` (pendiente — creada en commit 4 de VTS-007) |

---

## 1. Propósito

Registrar de forma uniforme una **devlog entry** durante la ejecución de una tarea VTT, garantizando que tiene los campos contractuales (`categoryCode`, `title`, `description`, `severity?`, `reportedBy`) y queda en `status: pending` lista para procesamiento posterior por el TL (FASE 3) o el PM (FASE 4).

Cubre los 7 `categoryCode` válidos: `decision`, `observation`, `blocker`, `tech_debt`, `testing_note`, `risk`, `issue`.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_id` | string (`PROJ-NNN`) | Tarea en curso del agente | sí | ID de la tarea VTT donde se registra la entry |
| `agent_uuid` | UUID | OPERATIVO del rol | sí | UUID del agente — se usa como `reportedBy` |
| `vtt_token` | string (JWT) | `VTT.SKILL-AUTH-001` previo | sí | Token de autenticación (cacheado en `.vtt_jwt`) |
| `category_code` | enum | Decisión del agente (ver §5.1) | sí | Uno de: `decision`, `observation`, `blocker`, `tech_debt`, `testing_note`, `risk`, `issue` |
| `title` | string ≤200 chars | Decisión del agente | sí | Título corto descriptivo |
| `description` | string ≥1 char | Decisión del agente | **sí (R1 — bloqueante)** | Contexto real: qué, por qué, impacto. NO vacío. NO solo espacios |
| `severity` | enum | Decisión del agente (ver §5.2) | sí si categoría con severidad; no si `decision`/`observation` | `low` / `medium` / `high` / `critical` |
| `impact_description` | string | Decisión del agente | no | Áreas afectadas (opcional) |

> **Categorías que requieren `severity`:** `blocker`, `tech_debt`, `testing_note`, `risk`, `issue`.
> **Categorías sin `severity`:** `decision`, `observation` (no usan el campo).

---

## 3. Precondiciones

- `$VTT_TOKEN` (o `.vtt_jwt`) válido — invocar `VTT.SKILL-AUTH-001` si expiró
- Tarea en `status ∈ {task_in_progress, task_in_review}` — el backend rechaza POST devlog en otras estados
- El evento a registrar **ya ocurrió** (esta Workflow registra, no propone)
- Si el evento es un bloqueante técnico o consulta de scope que requiere Issue formal → **NO usar esta Workflow**, ver `VTT.PROTOCOL-DEV-001` §5.1.2.bis (escalación a ASG-001 §5.4 / §5.4.bis)

---

## 4. Reglas operativas del Workflow

| # | Regla |
|---|---|
| WF1 | `description` obligatorio y no-vacío. Lección MS-333: el TL borra entries sin description |
| WF2 | Si categoría usa severidad, `severity` debe ser uno de los 4 enum válidos (`low/medium/high/critical`) — sin valor → HTTP 400 |
| WF3 | `reportedBy` = `agent_uuid` propio. NO suplantar identidad de otro agente |
| WF4 | Si la entry resulta en `critical`/`high` → considerar si en realidad es `blocker` para sub-ciclo ASG-001 §5.4 (mover tarea a `task_on_hold`). Una entry `critical`/`high` que queda en devlog bloquea el Review Gate |
| WF5 | Endpoint canónico: `POST /api/tasks/:taskId/devlog` (singular). Para batch de varias entries usar `POST /devlog-entries` con wrapper `{entries:[...]}` (R6) — pero esta Workflow cubre el caso 1 entry |
| WF6 | No usar copias locales del comando — Skills DEV son curls atómicos invocados directamente desde este Workflow |

---

## 5. Pasos

### Paso 1 — Decisión del `categoryCode`

Identificar uno de los 7 tipos según la naturaleza del evento (ver tabla §5.1.1 del Protocol DEV-001):

| Evento detectado | `categoryCode` | ¿Severidad? |
|---|---|---|
| Decisión técnica con trade-off | `decision` | no |
| Observación de comportamiento | `observation` | no |
| Bloqueante real que impide avanzar | `blocker` | sí (`high`/`critical` típicamente) |
| Deuda técnica fuera de scope | `tech_debt` | sí (`low`/`medium` típicamente) |
| Resultado de testing | `testing_note` | sí (según resultado) |
| Riesgo identificado | `risk` | sí (según probabilidad) |
| Inconsistencia no-bug | `issue` | sí (según gravedad) |

¿Es realmente un evento devlog y no algo que debería ser comment o Issue formal? → ver §5.1.2 + §5.1.2.bis del Protocol DEV-001.

### Paso 2 — Decisión de `severity` (si aplica)

Sólo para categorías con severidad. Aplicar criterio del Review Gate:

| `severity` | Bloquea Review Gate? | Cuándo usar |
|---|---|---|
| `critical` | sí | Impide funcionamiento del sistema |
| `high` | sí | Problema serio que debe resolverse |
| `medium` | no | Debería resolverse, no urgente |
| `low` | no | Nice to have / observación |

### Paso 3 — Composición del payload

Construir JSON con los campos del §2. Para categorías sin severidad omitir el campo `severity`.

### Paso 4 — Invocar Skill según categoryCode

→ invoca la Skill que mejor mapea al evento:

| `categoryCode` | Skill |
|---|---|
| `decision` | `VTT.SKILL-DEV-001` (registrar decisión) |
| `observation` | `VTT.SKILL-DEV-002` (registrar observación) |
| `blocker` / `tech_debt` / `testing_note` / `risk` / `issue` | `VTT.SKILL-DEV-001` o `-002` adaptando `categoryCode` (las 2 Skills son atómicas sobre el mismo endpoint POST) |

> **Nota:** las 5 Skills DEV-001..005 atienden los 4 verbos REST sobre `/devlog`. Para esta Workflow (POST), DEV-001/DEV-002 son los puntos de entrada documentados. Si la categoría no es `decision`/`observation`, usar DEV-001 como wrapper genérico cambiando el `categoryCode`.

### Paso 5 — Validación de respuesta

¿HTTP 201? →
- **SÍ** → entry creada en `status: pending`. Capturar `entry_id` del response para trazabilidad.
- **NO** → ver §8 Errores comunes.

### Paso 6 — Registro local (opcional pero recomendado)

Anotar `entry_id` en log local (`.vtt/devlog-trail.log` u otro) para que el agente pueda hacer follow-up sin re-listar el devlog completo.

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `entry_id` | UUID | Response del POST | ID único de la entry creada |
| `entry_status` | string | Response | Siempre `pending` al crearse |
| `created_at` | ISO 8601 | Response | Timestamp del backend |
| `reportedBy` | UUID | Response | Igual a `agent_uuid` del input |

---

## 7. Validación de salida

```bash
# Listar entries de la tarea y verificar que la nueva aparece en pending
TOKEN=$(cat .vtt_jwt)
curl -s "https://api.vttagent.com/api/tasks/$TASK_ID/devlog" \
  -H "Authorization: Bearer $TOKEN" \
  | python -m json.tool | grep -A 3 "\"id\": \"$ENTRY_ID\""

# Debe mostrar: "status": "pending", "categoryCode": "<el elegido>"
```

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| HTTP 400 `"description es requerido"` | `description` vacío o ausente | Re-enviar con `description` no-vacío (R1 del Protocol) |
| HTTP 400 `"severity must be one of [low,medium,high,critical]"` | Categoría requiere severity y no se envió o se envió valor inválido | Verificar tabla §5.2 + enviar enum válido |
| HTTP 400 `"categoryCode is required"` | Falta el campo o se usó `type` (campo legacy) | El campo correcto es `categoryCode` (no `type`) |
| HTTP 403 `Missing capability` | Agente sin capability `tasks.update` o similar | Escalar al Coord — gap RBAC |
| HTTP 404 `Task not found` | `task_id` no existe o el agente no tiene visibilidad | Verificar con `GET /api/tasks/:id` |
| HTTP 422 `task status invalid` | Tarea no está en `in_progress`/`in_review` | Mover tarea al estado correcto primero |

---

## 9. Skills invocadas

| Skill | Cuándo |
|---|---|
| `VTT.SKILL-AUTH-001` | Si `$VTT_TOKEN` expiró |
| `VTT.SKILL-DEV-001` | Para `categoryCode: decision` (y wrapper genérico) |
| `VTT.SKILL-DEV-002` | Para `categoryCode: observation` |

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-SEC-001` | No incluir IPs prod, paths absolutos prod, credenciales en `title`/`description` |
| `RULE-VTT-001` | Devlog `critical`/`high` pending bloquea Review Gate — el agente debe ser consciente al crear con severidad alta |
| `RULE-VTT-002` | (aplica en transiciones, no en creación — ver Workflow .002) |

---

## 11. Cambios

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-06-02 | TW-OPS (auditoría VTS-007) | Versión inicial. Workflow operativo de la FASE 1 del PROTOCOL-DEV-001. Cubre POST a `/api/tasks/:taskId/devlog` con los 7 categoryCode válidos y los 4 niveles de severity. Origen: gap G1 detectado en auditoría VTS-007 (Protocol referencia este Workflow pero no existía). |

---

**Pertenece a:** `VTT.PROTOCOL-DEV-001` §5.1
**Workflow padre:** `VTT.PROTOCOL-DEV-001`
