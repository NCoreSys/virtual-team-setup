# VTT.SKILL-ISS-001 — Crear issue/blocker en tarea

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-ISS-001` |
| **Categoría** | ISS (Issue) |
| **Versión** | 1.2 |
| **Fecha** | 2026-06-02 |
| **Aplica a** | Todos los roles |
| **Tokens estimados** | ~270 |
| **Cuándo se usa** | Cuando hay un blocker real, un bug detectado, una mejora propuesta, o una duda formal que necesita decisión del TL/PM (type=question, no bloqueante) |
| **Reemplaza** | `SKL-ISSUE-01_crear-issue.md` (legacy) |

---

## ⚠️ CRÍTICO — efecto colateral en la tarea

Crear un issue **NO pone automáticamente** la tarea en `task_on_hold` (corrección al legacy — esto era impreciso).

El comportamiento correcto:

| Acción | Skill |
|---|---|
| Crear issue (registrar el problema) | **`VTT.SKILL-ISS-001`** (esta) — solo crea el record |
| Poner tarea en `task_on_hold` | `VTT.SKILL-STATUS-005` (endpoint `PUT /on-hold` distinto) |

> **Workflow estándar al bloquearse:**
> 1. Crear issue (esta skill) → genera record del problema
> 2. Mover a `task_on_hold` con `VTT.SKILL-STATUS-005` → vincula la tarea al issue por `sourceIssueId`
> 3. Cuando el issue se resuelva, VTT auto-resume la tarea al `previousStatus`

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea donde nace el issue |
| `agent_uuid` | uuid | sí | UUID del que reporta (= `reportedBy`) |
| `title` | string ≤200 | sí | Título del issue (descripción corta del bloqueo) |
| `description` | string ≤5000 | sí | Descripción detallada — qué pasa, qué intentaste, qué necesitás para desbloquear |
| `issue_type` | enum | sí | **5 valores válidos (v1.2 — verificado contra backend):** `bug` / `question` / `blocker` / `improvement` / `other`. CAMBIO v1.2: `requirement` REMOVIDO (no existe en backend), `other` AGREGADO. |
| `severity` | enum | sí | `low` / `medium` / `high` / `critical` |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- El bloqueante es **real y verificable** — no se abren issues por "tengo dudas"
- El agente ya intentó resolverlo (o documenta que no es resoluble localmente)

---

## Variables del entorno

```bash
$TOKEN                     # JWT (ver VTT.SKILL-AUTH-001)
$VTT_BASE_URL              # https://api.vttagent.com (NO IP — RULE-SEC-001)
$AGENT_UUID
```

---

## Ejecución

```bash
ISSUE_RESPONSE=$(curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/issues" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"title\": \"$ISSUE_TITLE\",
    \"description\": \"$ISSUE_DESCRIPTION\",
    \"type\": \"$ISSUE_TYPE\",
    \"severity\": \"$ISSUE_SEVERITY\",
    \"reportedBy\": \"$AGENT_UUID\"
  }")

ISSUE_ID=$(echo "$ISSUE_RESPONSE" | python -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
echo "ISSUE_ID=$ISSUE_ID"
```

Capturar el `ISSUE_ID` — se usa para vincular en `VTT.SKILL-STATUS-005`.

---

## Validación

```bash
# Confirmar issue creado
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/issues" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
issues = json.load(sys.stdin).get('data', [])
print(f'issues_total: {len(issues)}')
for i in issues[-3:]:
    print(f\"  {i.get('severity'):<10} | {i.get('type'):<12} | {i.get('title')}\")
"
```

---

## Cómo resolver un issue

**v1.1 — ruta real verificada contra API:** `PUT /api/issues/<id>` (NO `PATCH .../resolve` — esa ruta documentada en v1.0 NO existe en backend).

```bash
curl -s -X PUT "$VTT_BASE_URL/api/issues/$ISSUE_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"isResolved\": true,
    \"resolution\": \"Descripción del fix aplicado\"
  }"
```

Respuesta esperada: el issue queda con `isResolved=true` y `resolvedAt=<timestamp>`. NO se borra — permanece visible en `GET /api/tasks/<TASK_ID>/issues` con flag resuelto.

> **Auto-resume:** si la tarea estaba en `task_on_hold` por este issue (con `sourceIssueId` apuntando aquí), al resolverlo VTT **automáticamente** vuelve la tarea a su `previousStatus`.

### Quién puede resolver

- **Issue type `question`** (§5.4.bis): el TL responde con comment en la tarea; el **agente que creó el issue** lo marca resuelto cuando aplica la respuesta (auto-cierre).
- **Issue type `bug`/`blocker`/`improvement`/`other`**: lo resuelve quien aporta el fix (puede ser el mismo agente o un TL/peer).

---

## Cuándo crear un issue

| Caso | Type | Severity típica | ¿Tarea va a on_hold? |
|---|---|---|---|
| Falta dato del PM (especificación incompleta) | `blocker` | `high` | Sí |
| Dependencia rota (otro módulo no funciona) | `blocker` | `critical` | Sí |
| Detectaste bug en otro módulo durante la tarea | `bug` | `medium`/`high` | No necesariamente — depende |
| Falta una capability/feature de VTT que bloquea tu tarea | `blocker` | `medium`/`high` | Sí (v1.2: ya no existe `requirement` en backend — usar `blocker` si bloquea, `improvement` si NO bloquea) |
| Tenés idea de mejora que no es scope | `improvement` | `low` | No |
| **Duda de scope/diseño que necesita decisión del TL/PM** | **`question`** | **`low`** o `medium` | **NO** (no bloqueante — sub-ciclo §5.4.bis ASG-001; agente sigue con FASE alternativa mientras espera respuesta) |
| Caso que no encaja en ninguno de los anteriores | `other` | según impacto | depende |

### Árbol de decisión para severity de `question`

| Caso | Severity |
|---|---|
| Duda conceptual sobre scope que NO te impide trabajar en NADA | `low` |
| Duda concreta que te impide arrancar UNA tarea (la actual) pero el resto del sprint avanza sin vos | `low` |
| Duda concreta que te impide arrancar TODAS tus tareas asignadas | `medium` |
| Duda que pone en riesgo el sprint o release timeline | NO usar question — usar `blocker` con severity high/critical |

### Aplicabilidad de `question` cuando la tarea está en `pending` (pre-arranque)

§5.4.bis ASG-001 aplica también a tareas en estado `pending` — NO solo a `in_progress`. Si necesitás aclaración antes de arrancar:

1. NO patches a `in_progress` todavía
2. Creá el issue `question` con la tarea aún en `pending` (el backend lo acepta — no exige `in_progress`)
3. En el comment paralelo agregá prefijo `[PRE-ARRANQUE]` para que el TL identifique el bloqueo pre-arranque
4. Cuando el TL responda y vos apliques la respuesta, recién entonces patcheás a `in_progress`

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Issue se crea pero tarea sigue en in_progress | Esperabas auto-on_hold | Comportamiento corregido: necesitás llamar a `VTT.SKILL-STATUS-005` después |
| HTTP 400 `Type must be one of: bug, question, blocker, improvement, other` | Usar enum no listado | **v1.2 enum oficial:** `bug` / `question` / `blocker` / `improvement` / `other`. `requirement` ya NO existe en backend (era ficticio en v1.0/v1.1) |
| HTTP 400 severity inválido | Usar enum no listado | Solo: low/medium/high/critical |
| HTTP 404 al resolver con `PATCH /api/issues/<id>/resolve` | Ruta NO existe (era doc errónea en v1.0) | Usar `PUT /api/issues/<id>` con `{isResolved:true,resolution:"..."}` |
| Issue sin contexto | Faltó description detallada | El TL/PM necesita reproducir el problema — agregar contexto (usar estructura de 4 secciones del final del doc) |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- Workflow del agente al encontrar bloqueante o necesitar decisión formal
- **Después de esta skill, según `type`:**
  - `type=blocker` o `bug` que impide continuar → invocar `VTT.SKILL-STATUS-005` (poner tarea en on_hold)
  - `type=question` (§5.4.bis no bloqueante) → invocar `VTT.SKILL-COMMENT-001` con prefijo `QUESTION-TL:` (paralelo, en la tarea — NO en el issue) y seguir trabajando en lo que NO depende de la decisión pendiente
  - `type=improvement` o `other` (informativo) → no invocar nada más, seguir trabajando

---

## Cuándo NO usar esta Skill

- **Si es duda conversacional rápida** (no necesita decisión formal del TL, no afecta scope) → usar `VTT.SKILL-COMMENT-001`
- **Si es duda de scope/diseño que necesita decisión formal del TL/PM** → SÍ usar esta Skill con `type=question` — sub-ciclo §5.4.bis ASG-001
- **Si es observación técnica** → usar `VTT.SKILL-DEV-002`
- **Si es decisión propia** → usar `VTT.SKILL-DEV-001`
- **Si ya hay un issue para esto** → no duplicar, agregar comment al issue existente

---

## Estructura recomendada del `description` (todos los types)

Para que el TL/PM pueda reproducir el problema sin pedirte aclaraciones, estructurá el `description` en 4 secciones:

```
## Síntoma
[Qué pasó — output exacto, error message, comando que falló]

## Intentado
[Qué soluciones probaste antes de escalar — comandos, links, archivos consultados]

## Solicitud
[Qué necesitás del TL/PM — decisión, fix, dato, capability]

## Impacto
[Qué tarea/sprint queda bloqueado o afectado, qué NO bloquea]
```

Esta estructura aplica especialmente para `question` (sub-ciclo §5.4.bis) — el TL responde como comment en la tarea siguiendo el orden de las 4 secciones.

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-ISSUE-01_crear-issue.md`. **Corrección crítica:** legacy decía que crear issue ponía la tarea en on_hold automáticamente — eso NO es así. Requiere llamar `VTT.SKILL-STATUS-005` después. Documenta el flujo de auto-resume cuando se resuelve el issue. Tabla de cuándo crear cada `type`. |
| 1.1 | 2026-06-02 | **Fixes verificados contra API real (gap reportado por TW-OPS en VTS-007 comment b863a39b y agente DB en VTT-949):** (a) `type=question` agregado al enum (sub-ciclo §5.4.bis ASG-001 — no bloqueante). (b) Ruta de resolución corregida: `PUT /api/issues/<id>` con `{isResolved:true}` — la doc v1.0 decía `PATCH .../resolve` pero esa ruta NO existe en backend (404). (c) `$VTT_BASE_URL` ejemplo cambiado a `https://api.vttagent.com` (IP de prod removida — RULE-SEC-001). (d) Sección "Cuándo NO usar" actualizada: dudas de scope/diseño SÍ usan esta Skill con type=question (antes mandaba a COMMENT-001 indistintamente). |
| 1.2 | 2026-06-02 | **Enum oficial corregido tras probe contra API real (gap reportado por agente DB en VTT-949 al pedir clarificación):** El backend valida `type` contra exactamente 5 valores: `bug, question, blocker, improvement, other`. (a) `requirement` REMOVIDO — NO existe en backend (era ficticio en v1.0 y heredado erróneamente en v1.1). Si necesitás reportar "falta una capability/feature de VTT que bloquea tu tarea" → usar `blocker`; si NO bloquea → `improvement`. (b) `other` AGREGADO — para casos que no encajan en los otros 4. (c) Árbol de decisión de severity para `question` agregado. (d) Aplicabilidad de `question` en tarea estado `pending` (pre-arranque) documentada — antes solo se asumía `in_progress`. (e) Estructura recomendada del `description` (4 secciones: Síntoma/Intentado/Solicitud/Impacto) agregada al final, aplicable a todos los types. (f) Mensaje de error 400 actualizado con el string EXACTO que devuelve el backend (`Type must be one of: bug, question, blocker, improvement, other`). |
