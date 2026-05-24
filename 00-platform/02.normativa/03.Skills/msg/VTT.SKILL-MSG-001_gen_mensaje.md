# VTT.SKILL-MSG-001 — Generar Mensaje de Asignación

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-MSG-001` |
| **Categoría** | MSG (Mensajes de asignación) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-22 |
| **Aplica a** | TL Asignador |
| **Tokens estimados** | ~280 |
| **Cuándo se usa** | FASE 2 del `VTT.PROTOCOL-ASG-001 §5.2.13` — después de generar el execution_manifest |
| **Reemplaza** | `VTT.SKILL-TASK-004` (deprecated en v1.0) |
| **Reglas aplicables** | `RULE-SCRIPT-001` (path canónico), `RULE-TEMPLATE-001` (lectura formal del template) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX / VTT-XXX) | sí | ID de la tarea |
| `project_root` | path | sí | Path raíz del proyecto (con `.vtt/worktrees/` si aplica variante A) |
| `vtt_setup` | path | sí | Path a `$VTT_SETUP` (default `00-platform`) |
| `mode` | enum | sí | `output` (archivo local) / `post` (postear VTT + copia) / `validate` (verificar mensaje existente) |
| `output_path` | path | condicional | Requerido si `mode=output` |
| `validate_path` | path | condicional | Requerido si `mode=validate` |
| `token_env` | string | sí/no | Env var con JWT (default: `TOKEN`) |
| `base_url` | string | sí/no | VTT base URL (default: `http://77.42.88.106:3000`) |

> **Política contractual:** los datos del agente, CAs, phase/sprint, worktree y variante A/B se **resuelven automáticamente** desde VTT API + filesystem. El TL solo provee `task_id`. No se aceptan overrides manuales.

---

## Precondición

- $TOKEN obtenido (`VTT.SKILL-AUTH-001`) — o el script lo obtiene vía service-token si el TL UUID está disponible
- Tarea existe en VTT con `assignedTo` (no se puede generar mensaje sin agente)
- Template canónico v2.1 en `$VTT_SETUP/03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md`
- Si modo=`post`: chunking automático para mensajes >5000 chars (limit de comments VTT)
- Si proyecto usa worktrees: directorio `.vtt/worktrees/<repo>-<rol>/` existe (sino → variante B)

---

## Variables del entorno

```bash
$TOKEN              # JWT VTT (default env var: TOKEN)
$VTT_BASE_URL       # http://77.42.88.106:3000 (default)
$VTT_SETUP          # path a $VTT_SETUP/00-platform
$TL_UUID            # UUID del TL que postea (default Memory Service TL)
```

---

## Reglas obligatorias

### R1 — Path canónico del script (RULE-SCRIPT-001)

El script SIEMPRE se invoca desde su path canónico:
```
$VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py
```

❌ **PROHIBIDO** invocar copias locales del script en `scripts/` del worktree o del proyecto.

### R2 — Lectura formal del template (RULE-TEMPLATE-001)

El script lee `TEMPLATE_MENSAJE_ASIGNACION.md` v2.1 como archivo y resuelve placeholders `{{VAR}}` con datos vivos. El formato del mensaje **NO está hardcoded** en el script.

### R3 — Variante A o B automática

Detecta variante por filesystem:
- **A** (con worktrees): `{project_root}/.vtt/worktrees/{repo}-{rol}/` existe
- **B** (sin worktrees): no existe → usa `project_root` como cwd

La variante NO elegida se borra del template antes de resolver placeholders.

### R4 — `--validate` antes de `--post`

El modo `--post` ejecuta `--validate` internamente sobre el archivo generado. Si la validación falla con errors → NO postea y retorna exit 4.

### R5 — Trazabilidad obligatoria

El mensaje se guarda en disco ANTES de postear, en:
```
{project_root}/.vtt/worktrees/project-tl/knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md
```

Si `--output <path>` se especifica, se usa ese path en lugar del default.

---

## Ejecución

### Modo 1 — `--output` (preview sin postear)

```bash
export VTT_SETUP=c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform

python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  MS-XXX \
  --output /tmp/MENSAJE_MS-XXX_preview.md \
  --project-root c:/Users/Martin/Documents/virtual-teams/<proyecto> \
  --vtt-setup $VTT_SETUP
```

**Output esperado** (stdout JSON):
```json
{
  "success": true,
  "mode": "output",
  "output_path": "/tmp/MENSAJE_MS-XXX_preview.md",
  "rendered_size": 13730,
  "variant": "A"
}
```

### Modo 2 — `--post` (postear como comment en VTT)

```bash
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  MS-XXX \
  --post \
  --project-root c:/Users/Martin/Documents/virtual-teams/<proyecto> \
  --vtt-setup $VTT_SETUP
```

El script:
1. Lee template v2.1
2. Hace `GET /api/tasks/MS-XXX` + `/criteria` (resuelve agente, CAs, phase/sprint)
3. Detecta variante A/B y borra la NO elegida
4. Resuelve TODOS los `{{VAR}}` con datos reales
5. Guarda copia local
6. Ejecuta `--validate` interno (aborta con exit 4 si hay errors)
7. Postea como comment en VTT (chunking si >5000 chars)

**Output esperado**:
```json
{
  "success": true,
  "mode": "post",
  "output_path": "c:/.../project-tl/knowledge/agent-tasks/messages/04-development/S01/MENSAJE_MS-XXX.md",
  "comment_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "chunks": 3,
  "rendered_size": 11287,
  "variant": "A",
  "validation_warnings": []
}
```

### Modo 3 — `--validate` (verificar mensaje existente)

```bash
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  --validate /path/to/MENSAJE_MS-XXX.md
```

**Output esperado** (sin TOKEN → Bloque B skipped):
```json
{
  "valid": true,
  "findings": [
    {"block": "B", "severity": "info", "msg": "Bloque B skipped (no se proveyo --token-env con valor)"}
  ]
}
```

**Con TOKEN** → ejecuta los 3 bloques (A=secciones, B=coherencia VTT, C=higiene).

---

## Validación (qué chequea `--validate`)

### Bloque A — Secciones obligatorias

1. Sección `WORKING DIRECTORY` con UNA variante (no las dos)
2. Patrón `feature/<TASK_ID>` (branch convencional)
3. `Execution manifest:` con path `.vtt/manifests/<TASK_ID>.execution.json`
4. `Workspace VSCode:` con path `.code-workspace`
5. Sección `NORMATIVA DE REFERENCIA` (Reglas aplicables)
6. Invocación de `VTT.SCRIPT-MAN-001_gen_task_manifest.py` con flags pre-rellenados (`--task-id`, `--version 1.0`, `--agent-uuid`)
7. Sección `ENTREGABLES AL CERRAR` con `git add knowledge/task-manifests/.../<TASK_ID>.json`
8. Definición de `$VTT_SETUP=...`
9. Sección `QUE PASA DESPUES`
10. Referencia a `VTT.SKILL-REPORT-001` (instrucción I1)

### Bloque B — Coherencia cruzada con VTT (requiere token)

1. `agent_uuid` del mensaje (`Tu user ID`) coincide con `assignee.id` de la task en VTT
2. `taskId` en path del `execution_manifest` == `TASK_ID` del mensaje
3. `worktree_path` apunta a directorio existente
4. CAs listadas (count + UUIDs) coinciden con `GET /criteria`
5. Reporte ubicado en `knowledge/task-manifests/<phase>/<sprint>/` (no en `knowledge/agent-tasks/reports/` que está deprecado en v2.1)

### Bloque C — Higiene

1. 0 placeholders `{{[A-Z_]+}}` sin resolver
2. Endpoint devlog correcto: `POST /devlog` (singular) o `POST /devlog-entries` con wrapper `{entries:[...]}`
3. Endpoint fulfill CAs: `PATCH /api/tasks/<id>/criteria/<cid>` (NO `POST /fulfill`)
4. Encoding UTF-8 sin mojibake
5. Bloques ` ``` ` balanceados (markdown bien formado)

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Exit 1 `task_id requerido (salvo en --validate)` | Modo `output`/`post` sin task_id | Pasar `MS-XXX` como primer arg posicional |
| Exit 1 `--project-root requerido` | Modo `output`/`post` sin project-root | Pasar `--project-root <path>` |
| Exit 2 `Template no existe` | Path `$VTT_SETUP` incorrecto | Verificar `--vtt-setup` apunta a `00-platform` |
| Exit 2 `Agente no esta en el mapa ROLE_BY_EMAIL` | Email del assignee no registrado | Agregar al `ROLE_BY_EMAIL` dict del script |
| Exit 3 `HTTP 404` task no existe | `task_id` incorrecto | Verificar con `GET /api/tasks/<id>` |
| Exit 4 validation failed con `Falta sección X` | Template incompleto o mal modificado | Restaurar template canónico v2.1 |
| Exit 4 `POST a /devlog-entries SIN wrapper` | Mensaje legacy (formato MS-333) | Regenerar con el script — el template v2.1 ya usa `/devlog` singular |
| Variante no detectada (queda placeholder VARIANTE A/B) | `strip_variant()` no encontró markers | Verificar template tiene `<!-- VARIANTE A -->` ... `<!-- FIN -->` |

---

## Scripts invocados

- `VTT.SCRIPT-MSG-001_gen_mensaje.py` (path canónico en `04.Scripts/msg/`)

---

## Skills invocadas / dependencias

- `VTT.SKILL-AUTH-001` — obtener $TOKEN (el script lo obtiene auto si no está en env)
- **Depende de**: `VTT.WORKFLOW-MAN-001.001` (execution_manifest debe existir antes — paso §5.2.11 del PROTOCOL-ASG-001)
- **Depende de**: `VTT.PROTOCOL-WT-001` §5.2/§5.3 (worktree del agente debe existir si variante A)

---

## Cuándo NO usar esta Skill

- **Re-asignación de tarea ya en curso** → usar comment simple "Re-asignada, continuar"
- **Tarea fue rechazada y se re-trabaja** → usar comment de feedback, no nuevo mensaje completo
- **Mensajes ad-hoc al agente** (preguntas, aclaraciones) → usar `VTT.SKILL-COMMENT-001`

---

## Cómo el modo `--post` cubre el bug del wrapper devlog-entries

El bug original que motivó la migración de TASK-004 → MSG-001:
- **TASK-004 v1.0** referenciaba el script legacy `gen_mensaje.py` que tenía el formato hardcoded
- El formato hardcoded usaba `POST /devlog-entries` SIN wrapper `{entries:[...]}` → HTTP 400 garantizado al ejecutarse (caso MS-333)
- El template v2.1 corrige a `POST /devlog` singular para 1 entry
- **MSG-001 v1.0** lee el template formalmente — el mensaje generado nunca puede regresar al bug del wrapper

El `--validate` Bloque C también detecta el bug si alguien reintroduce manualmente la versión rota.

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-22 | Versión inicial del sub-sistema MSG. Reemplaza `VTT.SKILL-TASK-004` (deprecated). Apunta al script canónico `VTT.SCRIPT-MSG-001_gen_mensaje.py` que lee `TEMPLATE_MENSAJE_ASIGNACION.md v2.1` formalmente (RULE-TEMPLATE-001). 3 modos: `--output`, `--post`, `--validate`. Bloques de validación A/B/C cubren secciones obligatorias, coherencia cruzada con VTT y higiene (placeholders, endpoints, markdown). Probado contra MS-290 (`valid:true`), MS-333 (`valid:false` con 9 errors detallados) y `--post` end-to-end contra MS-328 (3 chunks posteados, 0 placeholders sin resolver, validate post-generation `valid:true`). Origen: OLA 1 del sub-sistema MSG, RULE-SCRIPT-001 v1.0. |
