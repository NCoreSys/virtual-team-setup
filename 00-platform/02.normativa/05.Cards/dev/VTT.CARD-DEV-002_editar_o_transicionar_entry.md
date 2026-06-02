# VTT.CARD-DEV-002 — Editar o transicionar devlog entry

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-DEV-002` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase IN [execution, review] AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA,TL]` |
| **Requiere Cards previas** | `CARD-DEV-001` (entry debe existir) |
| **Pertenece a** | `WORKFLOW-DEV-001.002` |
| **Tokens estimados** | ~1036 (medidos con chars/4 el 2026-06-02) |

---

## Qué hacer

Modificar una entry existente. **2 vías mutuamente excluyentes** (endpoints distintos — confundirlos es error común):

### Vía A — Editar contenido (NO cambia status)

Cuando hay typo / falta contexto / hay que corregir `severity`:

```bash
TOKEN=$(cat .vtt_jwt)
curl -s -X PATCH "https://api.vttagent.com/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "<nuevo titulo si cambia>",
    "description": "<nueva descripcion si cambia>",
    "severity": "<nueva severidad si cambia>"
  }'
```

Body parcial OK — sólo enviar campos que cambian.

### Vía B — Transicionar lifecycle (cambia status)

Cuando movés la entry por los estados hasta terminal. **Estados terminales son irreversibles** (R3 — `ENTRY_ALREADY_FINAL` si se intenta cambiar después).

```bash
# Acknowledged (intermedio — TL reconoce)
curl -s -X PATCH "https://api.vttagent.com/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"status":"acknowledged"}'

# Resolved (terminal — resolution OBLIGATORIA)
curl -s -X PATCH "https://api.vttagent.com/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"status":"resolved","resolution":"<como se resolvio>","fixTaskId":"<PROJ-NNN si aplica>"}'

# Wont_fix (terminal — resolution OBLIGATORIA, justificacion)
curl -s -X PATCH "https://api.vttagent.com/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"status":"wont_fix","resolution":"<por que no se resuelve>"}'

# Deferred (terminal — deferredToPhaseId OBLIGATORIO)
curl -s -X PATCH "https://api.vttagent.com/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"status":"deferred","resolution":"<a donde se difiere>","deferredToPhaseId":"<UUID>"}'
```

## Reglas duras

- **Vía A y Vía B son endpoints distintos.** Usar `/devlog/:id` (sin `/status`) sólo edita; usar `/devlog/:id/status` sólo transiciona. **No combinables** (FEATURE §9 — error documentado)
- `resolution` obligatorio en `resolved`/`wont_fix` (R7)
- `deferredToPhaseId` obligatorio en `deferred` (R8)
- Transiciones irreversibles (R3) — `resolved`/`wont_fix`/`deferred` no se pueden cambiar. Workaround: borrar (CARD-DEV-005 / Workflow .003) + recrear (CARD-DEV-001)
- Backend setea `resolvedBy` y `resolvedAt` automáticamente (R9). NO enviar `resolvedBy` en body
- Si actor ≠ `reportedBy` original: coordinar con TL antes de cambiar contenido ajeno (Vía A)

## Si falla

| Síntoma | Acción |
|---|---|
| 400 `ENTRY_ALREADY_FINAL` | Terminal irreversible — borrar+recrear si necesitás cambiar algo |
| 400 `resolution es requerido cuando status es resolved o wont_fix` | Agregar `resolution` ≥1 char en payload |
| 400 `deferredToPhaseId es requerido cuando status es deferred` | Agregar UUID válido de fase destino |
| Entry sigue en `pending` post-PATCH | Se usó endpoint Vía A para cambiar status — corregir a `/status` |
| 422 `task status invalid` | Verificar status de la tarea contenedora |

## Output

Entry con nuevo estado (Vía B) o nuevo contenido (Vía A). Si transición terminal → `resolvedAt` y `resolvedBy` setteados por backend. Si `deferred` → `resolvedAt`/`resolvedBy`/`resolution` limpios.

Si fue parte del procesamiento FASE 3 del TL → actualizar conteos en Task Manifest v1.5 (`devlog_resolved_count`/`wontfix`/`deferred`) — ver `VTT.PROTOCOL-MAN-001` §5.4.
