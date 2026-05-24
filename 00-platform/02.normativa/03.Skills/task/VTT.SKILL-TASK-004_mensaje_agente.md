# ⚠️ DEPRECATED — VTT.SKILL-TASK-004 → migrar a VTT.SKILL-MSG-001

> 🛑 **Esta skill está DEPRECATED desde 2026-05-22.**
> El sub-sistema MSG fue formalizado en OLA 1. La skill canónica ahora es:
>
> **`VTT.SKILL-MSG-001`** — `$VTT_SETUP/02.normativa/03.Skills/msg/VTT.SKILL-MSG-001_gen_mensaje.md`
>
> Razón de la deprecación:
> - TASK-004 v1.0 referenciaba el script legacy `gen_mensaje.py` con formato hardcoded
> - El formato hardcoded violaba `RULE-TEMPLATE-001` (no leía el template formalmente)
> - El payload tenía bug del wrapper `/devlog-entries` (caso MS-333 — HTTP 400 garantizado)
>
> MSG-001 corrige todo lo anterior:
> - Script canónico `VTT.SCRIPT-MSG-001_gen_mensaje.py` en `04.Scripts/msg/` (RULE-SCRIPT-001)
> - Lee `TEMPLATE_MENSAJE_ASIGNACION.md v2.1` formalmente
> - 3 modos: `--output`, `--post`, `--validate` (con bloques A/B/C de checks)
>
> **NO usar TASK-004 para nuevos workflows.** El PROTOCOL-ASG-001 §5.2.13 ya apunta a MSG-001 desde v1.4.0.
>
> El contenido legacy queda abajo solo como referencia histórica.

---

# VTT.SKILL-TASK-004 — Generar Mensaje al Agente (LEGACY)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-TASK-004` |
| **Categoría** | TASK (Task CRUD) |
| **Versión** | 1.0 (deprecated) |
| **Estado** | 🛑 DEPRECATED desde 2026-05-22 |
| **Reemplazada por** | `VTT.SKILL-MSG-001` |
| **Fecha original** | 2026-05-19 |
| **Aplica a** | TL |
| **Tokens estimados** | ~300 |
| **Cuándo se usa** | ~~FASE 2 del PROTOCOL-ASG-001 §5.2.13~~ — NO usar, ver MSG-001 |
| **Reemplaza** | `SKL-TASK-04_mensaje-agente.md` (legacy, mal-nombrado como SKL-TASK-03 en su header) |

> **Nota sobre nomenclatura futura:** esta Skill fue migrada a `VTT.SKILL-MSG-001` el 2026-05-22 (sub-sistema MSG formalizado en OLA 1).

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `task_title` | string | sí | Título de la tarea |
| `assignee_role` | enum | sí | BE/DB/FE/DO/QA/DL/UX/AR/SA |
| `assignee_uuid` | uuid | sí | UUID del agente |
| `service_key` | string | sí | Service key del proyecto |
| `brief_path` | path | sí | Ruta al BRIEF |
| `assignment_path` | path | sí | Ruta al ASSIGNMENT |
| `execution_manifest_path` | path | sí | `.vtt/manifests/<TASK_ID>.execution.json` (output de `WORKFLOW-MAN-001.001`) |
| `worktree_path` | path | sí | Ruta absoluta al worktree del agente (`.vtt/worktrees/<repo>-<rol>/`) |
| `workspace_path` | path | sí | Ruta absoluta al `.code-workspace` del rol |
| `port_npm` | number | sí/no | Puerto npm asignado (si aplica) |
| `vtt_setup_path` | path | sí | `$VTT_SETUP` para referenciar la normativa |
| `lista_cas` | array | sí | CAs con UUIDs (output de `GET /tasks/<TASK_ID>/criteria`) |

> **Política contractual:** los inputs son fijos. Si el proyecto no usa worktrees, `worktree_path`/`workspace_path` se ponen como `null` y se selecciona Variante B del template.

---

## Precondición

- Tarea creada y asignada (`VTT.SKILL-TASK-001` + `VTT.SKILL-TASK-003`)
- BRIEF + ASSIGNMENT subidos como attachments
- Execution Manifest generado (`VTT.WORKFLOW-MAN-001.001` — paso 5.2.11)
- Worktree del agente verificado (`VTT.PROTOCOL-WT-001` §5.2/§5.3 — paso 5.2.10)
- $TOKEN obtenido (`VTT.SKILL-AUTH-001`)

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL
$AGENT_UUID         # del TL que envía
$VTT_SETUP          # Source of Truth de la normativa
```

---

## Reglas obligatorias

### R1 — Usar el template oficial

**Formato obligatorio:** `$VTT_SETUP/03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md` v2.0

Esta es la **única plantilla autorizada** para el mensaje TL→agente. Tiene sección `## Working Directory` condicional con dos variantes:
- **Variante A** — proyecto con worktrees (`.vtt/worktrees/<repo>-<rol>/`)
- **Variante B** — proyecto sin worktrees (clon directo)

### R2 — Reemplazar TODOS los placeholders

Cada `{{VAR}}` del template debe reemplazarse con dato real. Ver tabla §"Placeholders" del template para mapeo completo.

### R3 — Postear en VTT como comment

El mensaje se postea como comment en la tarea (`POST /api/tasks/<TASK_ID>/comments`). El agente lo recibe ahí, no por email.

### R4 — Guardar copia local

Por trazabilidad, guardar el texto del mensaje generado en:
```
knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md
```

---

## Ejecución

### Opción A — Automatizado (`gen_mensaje.py --post`)

Si existe `scripts/gen_mensaje.py` en el proyecto:

```bash
python scripts/gen_mensaje.py <TASK_ID> --post
```

El script:
1. Lee el template `TEMPLATE_MENSAJE_ASIGNACION.md` v2.0
2. Hace GET a VTT para obtener metadata de la tarea (CAs, assignee, etc.)
3. Reemplaza `{{VAR}}` con datos reales
4. Detecta automáticamente si el proyecto usa worktrees → elige Variante A o B
5. Postea como comment en VTT
6. Guarda copia local en `knowledge/agent-tasks/messages/<phase>/<sprint>/`

> **Pendiente normativo:** el script actual `gen_mensaje.py` (memory-service) **NO lee el template formalmente** — tiene el formato hardcodeado. Refactor pendiente para que lea el template v2.0 directamente.

### Opción B — Manual (sin script)

Si el proyecto no tiene `gen_mensaje.py`:

1. **Abrir template:** `$VTT_SETUP/03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md`
2. **Copiar el bloque ` ``` ` interior**
3. **Reemplazar manualmente** todos los `{{VAR}}` con datos reales
4. **Elegir variante** (A si hay worktree, B si no — borrar la otra)
5. **Guardar** el resultado en `knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md`
6. **Postear** via curl:

```bash
MENSAJE_CONTENT=$(cat knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md)

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$(python -c "
import json, sys
msg = open('knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md').read()
print(json.dumps({'message': msg, 'type': 'assignment', 'userId': '$AGENT_UUID'}))
")"
```

---

## Validación

```bash
# Check 1: archivo local guardado
ls knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md

# Check 2: NO quedan placeholders sin reemplazar
grep -c "{{" knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md
# Esperado: 0

# Check 3: variante elegida (no quedaron las 2)
grep -c "VARIANTE A\|VARIANTE B" knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md
# Esperado: 0 o 1 (no debe quedar la otra)

# Check 4: comment posteado en VTT
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
comments = json.load(sys.stdin)['data']
assignment_comments = [c for c in comments if c.get('type') == 'assignment']
print('assignment_comments:', len(assignment_comments))
"
# Esperado: >= 1
```

---

## Contenido obligatorio del mensaje (lo cubre el template)

El template ya incluye TODO lo siguiente — solo verificar que los placeholders se reemplazaron:

1. **Saludo + TASK_ID + TITULO**
2. **Sección Working Directory** (variante A o B)
3. **Lectura obligatoria** — paths al BRIEF, ASSIGNMENT, OPERATIVO del rol
4. **Execution manifest path** (si variante A)
5. **Worktree + workspace** paths (si variante A)
6. **CAs listadas con UUIDs**
7. **Comandos VTT** — login + status in_progress + devlog + fulfill criteria
8. **Entregables al cerrar** — orden de 9 pasos (incluye Paso 8 = generar manifest v1.0 con script, Paso 9 = commit del manifest al PR)
9. **Datos del sistema** — UUIDs status, backend URL, service key
10. **Qué pasa después** — FASE 4.5 del TL (FYI no requiere acción del agente)

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Placeholders `{{X}}` sin reemplazar | Falta Paso 3 del flujo manual | Re-leer el template + verificar cada placeholder de la tabla |
| Variante WT incluida sin worktree | Falta Paso 4 (decidir variante) | Borrar variante A si proyecto no usa worktrees |
| Mensaje sin CAs | `lista_cas` vacía o no consultada | `GET /api/tasks/<TASK_ID>/criteria` antes de generar |
| Falta path del execution_manifest | Mensaje generado antes de `WORKFLOW-MAN-001.001` | Generar manifest primero (paso 5.2.11) — esta skill es §5.2.13 |
| Comment no aparece en VTT | `userId` faltante en payload | Agregar `"userId": "$AGENT_UUID"` |
| Comment muy largo (>5000 chars) | Mensaje supera límite VTT | Mover detalles a BRIEF/ASSIGNMENT, dejar mensaje breve |

---

## Scripts invocados

- `scripts/gen_mensaje.py` (legacy del proyecto memory-service) — versión Opción A
- Futuro: `VTT.SCRIPT-MSG-001_gen_mensaje.py` cuando se formalice el sub-sistema MSG

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-QUERY-003_detalle_tarea` (cuando se migre) — obtener metadata + CAs
- (depende de) `VTT.WORKFLOW-MAN-001.001` — sin manifest no hay paths para incluir
- (depende de) `VTT.PROTOCOL-WT-001` — si variante A, el worktree debe existir

---

## Cuándo NO usar esta Skill

- **Re-asignación de tarea ya en curso** — usar comment simple "Re-asignada, continuar" en lugar de regenerar todo el mensaje
- **Tarea fue rechazada y se re-trabaja** — usar comment de feedback, no nuevo mensaje completo

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-TASK-04_mensaje-agente.md`. Apunta al `TEMPLATE_MENSAJE_ASIGNACION.md v2.0` como fuente única. Documenta 2 opciones (automatizada con `gen_mensaje.py` / manual). Cross-ref con PROTOCOL-WT-001 + PROTOCOL-MAN-001. Marca migración futura a sub-sistema MSG cuando se registre. |
| 1.0 + DEPRECATED | 2026-05-22 | 🛑 Marcada como DEPRECATED. Reemplazada por `VTT.SKILL-MSG-001` (sub-sistema MSG formalizado en OLA 1). Razón: TASK-004 referenciaba el script legacy con formato hardcoded (violaba RULE-TEMPLATE-001) y bug del wrapper `/devlog-entries` (caso MS-333). MSG-001 corrige ambos: lee `TEMPLATE_MENSAJE_ASIGNACION.md v2.1` formalmente y usa el script canónico `VTT.SCRIPT-MSG-001_gen_mensaje.py` en `04.Scripts/msg/`. |
