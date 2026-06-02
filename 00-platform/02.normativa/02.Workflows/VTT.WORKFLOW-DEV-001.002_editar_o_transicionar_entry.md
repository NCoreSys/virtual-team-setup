# VTT.WORKFLOW-DEV-001.002 — Editar o transicionar devlog entry

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-DEV-001.002` |
| **Pertenece a** | `VTT.PROTOCOL-DEV-001` §5.3 (FASE 3 — Procesamiento en code review) + §5.1.4 (corrección durante ejecución) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-02 |
| **Autor** | TW-OPS (auditoría VTS-007) |
| **Aplica a** | Agente ejecutor (correcciones propias §5.1.4), TL Reviewer (procesamiento §5.3) |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por Protocol padre §5.3.3 + §5.1.4 |
| **CARD asociada** | `VTT.CARD-DEV-002` (pendiente — creada en commit 4 de VTS-007) |

---

## 1. Propósito

Modificar una **devlog entry** existente mediante una de dos vías mutuamente excluyentes:

- **Vía A — Editar contenido** (`PATCH /devlog/:entryId`): cambiar `title`, `description`, `severity` u otros campos cuando hay typo o falta contexto. NO cambia `status`.
- **Vía B — Transicionar lifecycle** (`PATCH /devlog/:entryId/status`): mover la entry por los 6 estados del lifecycle hasta llegar a un estado terminal (`resolved`, `wont_fix`, `deferred`). Irreversible.

Las dos vías son endpoints distintos del backend. **Confundirlos es un error común documentado** (FEATURE §9 — "Endpoint incorrecto").

---

## 2. Inputs (estrictos)

### 2.1 Comunes a ambas vías

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_id` | string (`PROJ-NNN`) | Listado devlog | sí | ID de la tarea contenedora |
| `entry_id` | UUID | Listado devlog previo | sí | ID de la entry a modificar |
| `actor_uuid` | UUID | OPERATIVO del rol | sí | UUID del agente/TL que ejecuta |
| `vtt_token` | string (JWT) | `VTT.SKILL-AUTH-001` previo | sí | Token de autenticación |

### 2.2 Vía A — Editar contenido

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `title` | string ≤200 | no | Nuevo título (omitir si no cambia) |
| `description` | string ≥1 | no | Nueva descripción (omitir si no cambia) |
| `severity` | enum | no | Nueva severidad (omitir si no cambia) |
| `impact_description` | string | no | Nueva descripción de impacto |

### 2.3 Vía B — Transicionar lifecycle

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `target_status` | enum | sí | `acknowledged` / `in_progress` / `resolved` / `wont_fix` / `deferred` |
| `resolution` | string ≥1 | **sí si `resolved`/`wont_fix`** (R7) | Texto auditable de cómo se resolvió o por qué no |
| `deferredToPhaseId` | UUID | **sí si `deferred`** (R8) | Fase destino a la que se difiere |
| `fixTaskId` | string (`PROJ-NNN`) | no (recomendado en `resolved`) | Tarea que cierra el finding |

---

## 3. Precondiciones

- `$VTT_TOKEN` válido
- Vía A: entry **NO** está en estado terminal (los terminales sólo aceptan DELETE — ver Workflow .003 escenarios edge)
- Vía B: entry **NO** está en estado terminal (R3 — `ENTRY_ALREADY_FINAL` si lo está)
- Si `actor_uuid` ≠ `reportedBy` original: vía A coordinar con TL antes de cambiar contenido ajeno. Vía B sólo el TL/PM mueven entries de otros (excepto agente moviendo a `acknowledged` o resolviendo trabajo propio)
- La entry destino existe (no se borró previamente con `VTT.SKILL-DEV-005`)

---

## 4. Reglas operativas del Workflow

| # | Regla |
|---|---|
| WF1 | **Vía A y Vía B son endpoints distintos**. NO usar `/devlog/:entryId` con `{status: "resolved"}` — eso edita pero NO transiciona (FEATURE §9) |
| WF2 | `resolution` es obligatorio en `resolved`/`wont_fix` (R7 Protocol). Mensaje ≥1 char no-vacío |
| WF3 | `deferredToPhaseId` es obligatorio en `deferred` (R8 Protocol). UUID válido de la fase destino |
| WF4 | Transiciones son **irreversibles** (R3). `resolved`/`wont_fix`/`deferred` no se pueden cambiar. Workaround: borrar con Workflow .003 + recrear con Workflow .001 |
| WF5 | El backend setea `resolvedBy` automáticamente al `reportedBy` original (R9). NO enviar `resolvedBy` en el body |
| WF6 | El backend setea `resolvedAt` automáticamente en `resolved`/`wont_fix`. En `deferred` limpia `resolvedAt`/`resolvedBy`/`resolution` |
| WF7 | Si el agente transiciona a `resolved` su propia entry durante FASE 1, debe ser una entry de scope propio (no escalada del TL) |

---

## 5. Pasos

### Paso 1 — Decidir Vía A o Vía B

¿Qué necesito modificar? →
- **Contenido (title/description/severity)** → Vía A
- **Estado del lifecycle** → Vía B
- **Las dos cosas** → primero Vía A, luego Vía B (en orden, no en simultáneo — son endpoints distintos)

### Paso 2 — Verificar estado actual de la entry

```bash
TOKEN=$(cat .vtt_jwt)
curl -s "https://api.vttagent.com/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; [print(e) for e in json.load(sys.stdin)['data'] if e['id']=='$ENTRY_ID']"
```

¿`status ∈ {resolved, wont_fix, deferred}`? →
- **SÍ** → STOP. Entry en terminal. Si necesita corregirse, ver Workflow .003 (borrar + recrear).
- **NO** → continuar.

### Paso 3 — Vía A (si aplica): editar contenido

→ invoca **`VTT.SKILL-DEV-003`** con (`task_id`, `entry_id`, `actor_uuid`, [`title`?, `description`?, `severity`?, `impact_description`?])

Backend: `PATCH /api/tasks/:taskId/devlog/:entryId` con body parcial.

¿HTTP 200? → continuar Paso 4 si también Vía B; sino terminar.

### Paso 4 — Vía B (si aplica): transicionar lifecycle

Validar payload según `target_status`:

| `target_status` | Payload mínimo |
|---|---|
| `acknowledged` | `{"status": "acknowledged"}` |
| `in_progress` | `{"status": "in_progress"}` |
| `resolved` | `{"status": "resolved", "resolution": "...", "fixTaskId"?: "..."}` |
| `wont_fix` | `{"status": "wont_fix", "resolution": "..."}` |
| `deferred` | `{"status": "deferred", "resolution": "...", "deferredToPhaseId": "uuid"}` |

→ invoca **`VTT.SKILL-DEV-004`** con (`task_id`, `entry_id`, `actor_uuid`, `target_status`, payload)

Backend: `PATCH /api/tasks/:taskId/devlog/:entryId/status` con payload.

### Paso 5 — Validación de respuesta

¿HTTP 200? →
- **SÍ** → confirmar que `status` del response coincide con `target_status`.
- **NO** → ver §8 Errores comunes.

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `entry_status_new` | string | Response del PATCH | Nuevo estado de la entry |
| `resolvedAt` | ISO 8601 / null | Response | Timestamp si transición terminal a `resolved`/`wont_fix`; null si `deferred` |
| `resolvedBy` | UUID / null | Response | `reportedBy` original si terminal; null en `deferred` |
| `updatedAt` | ISO 8601 | Response | Timestamp del último cambio |

---

## 7. Validación de salida

```bash
# Re-leer devlog y verificar nuevo estado
TOKEN=$(cat .vtt_jwt)
curl -s "https://api.vttagent.com/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys,json; e=[x for x in json.load(sys.stdin)['data'] if x['id']=='$ENTRY_ID'][0]; print(f\"status={e['status']} resolvedAt={e.get('resolvedAt')} resolution={e.get('resolution')}\")"
```

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| HTTP 400 `ENTRY_ALREADY_FINAL` | Entry ya está en `resolved`/`wont_fix`/`deferred` | Las transiciones son irreversibles. Borrar+recrear vía Workflow .003 |
| HTTP 400 `"resolution es requerido cuando status es resolved o wont_fix"` | Falta `resolution` en payload | Agregar `resolution` ≥1 char |
| HTTP 400 `"deferredToPhaseId es requerido cuando status es deferred"` | Falta `deferredToPhaseId` | Agregar UUID válido de la fase destino |
| Entry sigue en `pending` después del PATCH | Se usó el endpoint Vía A en lugar de Vía B | Usar `/devlog/:id/status` (con `/status`) no `/devlog/:id` |
| HTTP 422 `task status invalid` | Tarea no está en estado que permita modificar devlog | Verificar status de la tarea |

---

## 9. Skills invocadas

| Skill | Cuándo |
|---|---|
| `VTT.SKILL-AUTH-001` | Si `$VTT_TOKEN` expiró |
| `VTT.SKILL-DEV-003` | Vía A — editar contenido |
| `VTT.SKILL-DEV-004` | Vía B — transicionar lifecycle |

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-VTT-002` | `resolution` requerido al resolver devlog (R7 del Protocol) |
| `RULE-SEC-001` | No incluir datos sensibles en `resolution` |
| `RULE-VTT-001` | Resolver entries `critical`/`high` para destrabar Review Gate |

---

## 11. Cambios

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-06-02 | TW-OPS (auditoría VTS-007) | Versión inicial. Workflow operativo de las FASES 1 (corrección §5.1.4) y 3 (procesamiento §5.3) del PROTOCOL-DEV-001. Cubre las 2 vías mutuamente excluyentes: PATCH body vs PATCH status. Origen: gap G1 detectado en auditoría VTS-007. |

---

**Pertenece a:** `VTT.PROTOCOL-DEV-001` §5.3 + §5.1.4
**Workflow padre:** `VTT.PROTOCOL-DEV-001`
