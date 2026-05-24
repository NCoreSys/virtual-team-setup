# VTT.SKILL-ISS-001 — Crear issue/blocker en tarea

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-ISS-001` |
| **Categoría** | ISS (Issue) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles |
| **Tokens estimados** | ~250 |
| **Cuándo se usa** | Cuando hay un blocker real — datos faltantes, dependencia rota, decisión PM pendiente |
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
| `issue_type` | enum | sí | `blocker` / `requirement` / `improvement` / `bug` |
| `severity` | enum | sí | `low` / `medium` / `high` / `critical` |

---

## Precondición

- `$TOKEN` obtenido (`VTT.SKILL-AUTH-001`)
- El bloqueante es **real y verificable** — no se abren issues por "tengo dudas"
- El agente ya intentó resolverlo (o documenta que no es resoluble localmente)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
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

```bash
curl -s -X PATCH "$VTT_BASE_URL/api/issues/$ISSUE_ID/resolve" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"resolution\": \"Descripción del fix aplicado\",
    \"resolvedBy\": \"$AGENT_UUID\"
  }"
```

> **Auto-resume:** si la tarea estaba en `task_on_hold` por este issue (con `sourceIssueId` apuntando aquí), al resolverlo VTT **automáticamente** vuelve la tarea a su `previousStatus`.

---

## Cuándo crear un issue

| Caso | Type | Severity típica | ¿Tarea va a on_hold? |
|---|---|---|---|
| Falta dato del PM (especificación incompleta) | `blocker` | `high` | Sí |
| Dependencia rota (otro módulo no funciona) | `blocker` | `critical` | Sí |
| Detectaste bug en otro módulo durante la tarea | `bug` | `medium`/`high` | No necesariamente — depende |
| Falta una capability/feature de VTT | `requirement` | `medium` | Solo si bloquea tu tarea |
| Tenés idea de mejora que no es scope | `improvement` | `low` | No |

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Issue se crea pero tarea sigue en in_progress | Esperabas auto-on_hold | Comportamiento corregido: necesitás llamar a `VTT.SKILL-STATUS-005` después |
| HTTP 400 type inválido | Usar enum no listado | Solo: blocker/requirement/improvement/bug |
| HTTP 400 severity inválido | Mismo | Solo: low/medium/high/critical |
| Issue sin contexto | Faltó description detallada | El TL/PM necesita reproducir el problema — agregar contexto |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`

---

## Skills que invocan ESTA

- Workflow del agente al encontrar bloqueante
- Después de esta skill, típicamente: `VTT.SKILL-STATUS-005` (poner tarea en on_hold)

---

## Cuándo NO usar esta Skill

- **Si es duda no bloqueante** → usar `VTT.SKILL-COMMENT-001` para consultar
- **Si es observación técnica** → usar `VTT.SKILL-DEV-002`
- **Si es decisión propia** → usar `VTT.SKILL-DEV-001`
- **Si ya hay un issue para esto** → no duplicar, agregar comment al issue existente

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-ISSUE-01_crear-issue.md`. **Corrección crítica:** legacy decía que crear issue ponía la tarea en on_hold automáticamente — eso NO es así. Requiere llamar `VTT.SKILL-STATUS-005` después. Documenta el flujo de auto-resume cuando se resuelve el issue. Tabla de cuándo crear cada `type`. |
