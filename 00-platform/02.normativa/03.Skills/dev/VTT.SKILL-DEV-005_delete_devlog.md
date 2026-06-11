# VTT.SKILL-DEV-005 — Eliminar devlog entry (DELETE permanente)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-DEV-005` |
| **Categoría** | DEV (Devlog) |
| **Versión** | 1.1 |
| **Fecha** | 2026-06-10 |
| **Aplica a** | Todos los roles con `tasks.update` (TL Reviewer típico, también agente para entries propios) |
| **Tokens estimados** | ~360 |
| **Cuándo se usa** | Eliminar **permanente** un devlog entry. Operación **destructiva e irreversible** (sin soft-delete, sin rollback) |
| **Permiso requerido** | `tasks.update` |
| **Pertenece a** | `VTT.WORKFLOW-DEV-001.002` (FASE 3 del `VTT.PROTOCOL-DEV-001` v1.1.0) — Paso 7 borrar entry duplicada/errónea |

---

## 🚨 OPERACIÓN DESTRUCTIVA — Reglas críticas

| Regla | Detalle |
|---|---|
| **Sin soft-delete** | El registro se elimina **físicamente** de `TaskDevlogEntry`. No hay papelera. No hay rollback. |
| **Sin audit log específico** | El backend NO registra quién/cuándo borró el entry (verificado en service). |
| **Sin restricción de autoría** | Cualquier agente con `tasks.update` puede borrar entries de **otros agentes**. |
| **Acepta cualquier status** | Incluso `resolved`/`wont_fix`/`deferred` (estados finales). Esto convierte al DELETE en el **único workaround** para corregir un entry mal marcado como final. |
| **Trazabilidad la pone vos** | Documentar el "por qué" en un comment de la tarea **ANTES** del DELETE (ver §Reglas de negocio). |

---

## ⚠️ ANTES DE BORRAR — árbol de decisión

```
¿El entry es contenido erróneo o duplicado?
  ├─ SÍ → DELETE (esta skill)
  └─ NO
       │
       ├─ ¿El contenido es correcto pero incompleto?
       │     └─ SÍ → usar VTT.SKILL-DEV-003 (edit)
       │
       ├─ ¿El contenido es correcto pero cambió de estado?
       │     └─ SÍ → usar VTT.SKILL-DEV-004 (lifecycle)
       │
       └─ ¿Entry en estado final pero contenido CORRECTO?
             └─ NO BORRAR — preservar el histórico
```

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX / VTT-XXX) | sí | ID de la tarea propietaria del entry |
| `entry_id` | uuid | sí | UUID del devlog entry a eliminar (formato 36 chars con guiones) |
| `confirm_intent` | string ≥20 chars | sí | **Justificación del borrado** — NO se envía a la API, queda en el workflow/comment como trazabilidad |

> **Política contractual:** sin `confirm_intent` válido (≥20 chars descriptivos), la skill se considera invocada incorrectamente. El agente DEBE entender qué borra antes de borrar.

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- Confirmar que el entry **realmente debe borrarse** (no solo editarse) — ver árbol de decisión arriba
- El actor tiene permiso `tasks.update`
- **Recomendado:** verificar con GET previo el contenido del entry antes de borrar
- **Recomendado:** postear comment en la tarea con el `confirm_intent` ANTES del DELETE (trazabilidad — ver §Reglas de negocio)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # https://api.vttagent.com  (siempre dominio — RULE-SEC-001 prohibe IP)
$TASK_ID                   # MS-XXX / VTS-XXX
$ENTRY_ID                  # UUID del entry
$AGENT_UUID                # UUID del actor (para comment de trazabilidad)
$CONFIRM_INTENT            # justificación del borrado
```

> **⚠️ Drift IP corregido en v1.1 (VTS-028):** la versión 1.0 documentaba `$VTT_BASE_URL=http://77.42.88.106:3000` — violaba RULE-SEC-001. Corregido a dominio prod. Hallazgo VTS-026 Anexo C.

---

## Ejecución

### Paso 1 — Trazabilidad ANTES del DELETE (recomendado)

Postear comment en la tarea explicando el motivo del borrado:

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Eliminando devlog entry $ENTRY_ID — razón: $CONFIRM_INTENT\",
    \"userId\": \"$AGENT_UUID\"
  }"
```

> Esto preserva en VTT la **razón** del borrado, ya que el backend NO loggea quién/cuándo borró.

### Paso 2 — Verificar el entry antes de borrar (opcional pero recomendado)

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
e = next((x for x in json.load(sys.stdin).get('data', []) if x.get('id') == '$ENTRY_ID'), None)
if not e:
    print('ENTRY NO EXISTE — no hay nada que borrar')
else:
    print(f'A BORRAR:')
    print(f'  title: {e.get(\"title\")}')
    print(f'  status: {e.get(\"status\")}')
    print(f'  categoryCode: {(e.get(\"category\") or {}).get(\"code\") or e.get(\"categoryCode\")}')
    print(f'  severity: {e.get(\"severity\")}')
    print(f'  fixTaskId: {e.get(\"fixTaskId\")}')
    print(f'  description (len): {len(e.get(\"description\") or \"\")}')
"
```

### Paso 3 — DELETE (sin body, retorna 204)

```bash
curl -s -X DELETE "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -w "HTTP %{http_code}\n"
```

**Salida esperada:** `HTTP 204` (sin body).

### Paso 4 — Ejecución en lote (varios entries de la misma task)

```bash
for ENTRY_ID in 2be1bc25-18cd-4f97-bec8-d57bd7841ba1 6dac4dbf-6d4c-4a9d-9600-6ffac9a25a37 3a63681b-b8f3-400f-9cdb-788176ddeb39; do
  echo "=== DELETE $ENTRY_ID ==="
  curl -s -o /dev/null -w "HTTP %{http_code}\n" \
    -X DELETE "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID" \
    -H "Authorization: Bearer $TOKEN"
done
```

> **Sin endpoint batch DELETE oficial** — iterar uno por uno. Si necesitás atomicidad (todo-o-nada) → coordinar con DevOps para SQL directo.

---

## Validación post-delete

```bash
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog" \
  -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
data = json.load(sys.stdin).get('data', [])
still = [e for e in data if e.get('id') == '$ENTRY_ID']
print('✅ ENTRY ELIMINADO' if not still else f'❌ ERROR: aun existe — {still[0]}')
"
```

---

## Respuestas del backend

| Código | Significado | Acción |
|---|---|---|
| **204** | Eliminado correctamente (sin body) | Validar con GET |
| **400** `"entryId debe ser un UUID válido"` | `entry_id` no es UUID | Verificar formato (36 chars con guiones) |
| **401** | Sin token | Renovar con `VTT.SKILL-AUTH-001` |
| **403** | Sin permiso `tasks.update` | Verificar rol del agente |
| **404** `ENTRY_NOT_FOUND` | Entry no existe o no pertenece a la tarea del path | Verificar `task_id` + `entry_id` (deben coincidir) |

---

## Reglas de negocio (recomendaciones operativas)

### R1 — Trazabilidad obligatoria

**Documentar el "por qué"** del borrado en un comment de la tarea **ANTES** del DELETE. El backend NO loggea la eliminación, así que el comment es la única evidencia que queda.

### R2 — Cuidado con `blockingEntries` del gate D-32

Si el entry borrado era `critical` o `high` con `status` no resuelto, podía estar bloqueando el `canProceed` de la fase. Coordinar con el TL ANTES de borrar entries que afecten el gate.

```bash
# Verificar si afecta el gate antes de borrar
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/review-gate" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
gate = json.load(sys.stdin).get('data', {})
print(f'canProceed: {gate.get(\"canProceedToReview\")}')
print(f'blockers: {gate.get(\"blockers\", [])}')
"
```

### R3 — Re-vincular `fixTaskId` si aplica

Si el entry a borrar tenía `fixTaskId` apuntando a una tarea real (esa tarea "resolvía" este devlog), evaluar si esa tarea debe re-vincularse a otro entry **antes** de borrar.

### R4 — Si está en estado final con contenido correcto → NO borrar

Los entries finales (`resolved`/`wont_fix`/`deferred`) con contenido válido son **histórico**. Borrarlos pierde trazabilidad de decisiones tomadas. Solo borrar si el entry estaba **mal marcado** como final.

---

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| HTTP 404 `ENTRY_NOT_FOUND` | El `entry_id` existe pero pertenece a OTRA tarea | Verificar que el `task_id` del path corresponde a la tarea dueña del entry |
| HTTP 400 `"entryId debe ser un UUID válido"` | ID truncado o mal copiado | Validar formato — 36 chars con guiones (8-4-4-4-12) |
| Borraste el equivocado | Sin Paso 2 de verificación previa | **NO hay rollback** — recrear manualmente con `VTT.SKILL-DEV-001` o `DEV-002`, perdiste timestamps originales |
| Gate de fase quedó destrabado sin querer | Borraste un entry `critical`/`high` no resuelto | Coordinar con TL antes — revisar `review-gate` (ver R2) |
| El backend no me dice quién borró | Comportamiento esperado | Por eso es **obligatorio el comment ANTES** (R1) |
| `fixTaskId` quedó huérfano | Borraste el entry pero `fixTaskId` apuntaba acá | Re-vincular esa task a otro entry (R3) o aceptar que quedó sin link |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — obtener `$TOKEN`
- `VTT.SKILL-COMMENT-001` — postear comment de trazabilidad (Paso 1)
- `VTT.SKILL-QUERY-003` (opcional, GET devlog de tarea) — verificar contenido antes de borrar (Paso 2)

---

## Skills que invocan ESTA

- **TL Reviewer** cuando detecta entries duplicados/erróneos en review
- **Agente** que se equivocó al cerrar entry como `resolved` con resolution incorrecta → borrar y recrear (workaround del `ENTRY_ALREADY_FINAL`)
- **PM/TL** en cleanup de devlog del sprint antes de cierre

---

## Cuándo NO usar esta Skill

- **Para corregir typo en `title`/`description`** → usar `VTT.SKILL-DEV-003` (edit)
- **Para cambiar `severity` o status** → usar `VTT.SKILL-DEV-003` o `VTT.SKILL-DEV-004`
- **Entry en estado final con contenido correcto** → NO borrar, preservar histórico
- **Para "limpieza estética" del devlog** → NO borrar entries válidos solo porque son muchos; el devlog es histórico

---

## Casos de uso reales (cuándo SÍ borrar)

| Caso real | Justificación |
|---|---|
| Entry creado por error (duplicado del agente) | Es ruido — borrar y dejar el original |
| Entry mal-categorizado (`decision` que en realidad era `bug`) | Borrar y recrear con la categoría correcta |
| Entry resuelto con `resolution` incorrecta (`ENTRY_ALREADY_FINAL` impide edición) | **Único workaround** — borrar y recrear con DEV-004 |
| Entry de prueba/debug que se commiteó por error | Cleanup legítimo |
| Entry de un sprint cancelado | Si la tarea se canceló y el entry no aporta histórico, borrar |

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-22 | Versión inicial. Cubre el endpoint `DELETE /api/tasks/:taskId/devlog/:entryId` con énfasis en irreversibilidad (sin soft-delete, sin audit log específico). Spec provista por BE de VTT tras incidente MS-333 (3 decisions sin description eliminadas ad-hoc). Documenta el árbol de decisión "borrar vs editar vs lifecycle", las 4 reglas de negocio (R1 trazabilidad obligatoria, R2 gate D-32, R3 fixTaskId huérfano, R4 preservar histórico válido), el workaround para `ENTRY_ALREADY_FINAL` (borrar + recrear) y receta de ejecución en lote. |
| 1.1 | 2026-06-10 | **Bump VTS-028 sobre hallazgos VTS-026.** (1) **Drift IP corregido (RULE-SEC-001):** `$VTT_BASE_URL` cambia de `http://77.42.88.106:3000` a `https://api.vttagent.com`. Único cambio operativo. Hallazgo VTS-026 Anexo C. (2) Header agrega "Pertenece a `VTT.WORKFLOW-DEV-001.002`" (FASE 3 del Protocol — Paso 7 borrar entry duplicada/errónea con comment de trazabilidad previo según R1 del listado de reglas de negocio). Sin otros fixes: las reglas R1-R4 y el árbol de decisión siguen vigentes y alineados con Protocol DEV-001 v1.1.0. |
