# Code Logic — VTT.SCRIPT-MSG-001_gen_mensaje.py

| Campo | Valor |
|---|---|
| **Archivo de código** | `00-platform/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py` |
| **Versión** | 1.0.0 (2026-05-22) |
| **Tarea origen** | VTT-725 |
| **Tipo** | Python 3 — stdlib pura (urllib, json, argparse, re) — sin dependencias externas |
| **Reglas aplicables** | `RULE-SCRIPT-001` (path canónico), `RULE-TEMPLATE-001` (lectura formal del template) |

---

## 1. Propósito

Generar el mensaje de asignación de tarea (TL → Agente) leyendo formalmente el template canónico `TEMPLATE_MENSAJE_ASIGNACION.md v2.1` y resolviendo placeholders `{{VAR}}` con datos vivos de la VTT API.

Reemplaza al script legacy `gen_mensaje.py` (5 copias dispersas en memory-service worktrees) que tenía el formato del mensaje **hardcoded en f-strings**.

---

## 2. Estructura del archivo

```
1-53     Header docstring (propósito, modos, inputs, outputs, exit codes, reglas)
55-62    Imports (stdlib only)
64-111   Constantes (BASE_URL, SERVICE_KEY, status UUIDs, ROLE_BY_EMAIL, ROLE_TO_REPO, PHASE_MAP)
118-158  HTTP helpers (vtt_get, vtt_post_comment con chunking, obtain_token)
164-217  Template loader (load_template, resolve_placeholders, strip_variant)
223-310  Build context (slugify, detect_phase_folder, detect_sprint_code, port_for_task, build_cas_section, build_context, render_message)
316-324  Output writers (default_output_path, write_local)
330-490  validate_message (Bloques A/B/C — 20+ checks)
496-615  main() — argparse + dispatch a los 3 modos
```

---

## 3. Funciones principales

### 3.1 `load_template(template_path)` — lectura formal (RULE-TEMPLATE-001)

```python
def load_template(template_path):
    """Carga el template canónico y extrae el bloque markdown."""
```

**Por qué importa**: implementa la regla R1/R2 de la skill. El script **NO contiene** el formato del mensaje en código — lo lee como archivo de texto y extrae solo el cuerpo entre los fences ` ```markdown ... ``` ` con regex non-greedy.

**Decisión de diseño**: uso regex con `re.DOTALL` para que `.` capture saltos de línea, pero `?` non-greedy para detenerme en el primer ` ``` ` de cierre (importante porque el template tiene bloques ` ```bash ` anidados dentro del bloque externo ` ```markdown `).

```python
m = re.search(r"```markdown\s*\n(.*?)\n```", raw, re.DOTALL)
```

**Falla si**: no hay bloque ` ```markdown ` (lanza `ValueError`) o el archivo no existe (`FileNotFoundError` → exit 2).

### 3.2 `strip_variant(template, keep="A")` — variante A/B

Elimina la variante NO elegida de la sección `## Working Directory`.

**Por qué importa**: el template tiene 2 variantes para proyectos con/sin worktrees. La detección automática evita que el TL tenga que editar manualmente.

**Algoritmo**:
1. Busca markers `<!-- VARIANTE A -->`, `<!-- VARIANTE B -->`, `<!-- FIN -->`
2. Si no encuentra los 3 → devuelve template intacto (defensa)
3. Si encuentra: parte el template en `[pre]` + `[variante A]` + `[variante B]` + `[post]`
4. Elige el block correspondiente, limpia los markers HTML, ensambla `[pre] + [elegido] + [post]`

**Edge case**: variantes con espacios distintos en los markers cubiertos con `\s*` y `.*?` en los regex.

### 3.3 `resolve_placeholders(template, mapping)`

```python
def resolve_placeholders(template, mapping):
    result = template
    for k, v in mapping.items():
        result = result.replace("{{" + k + "}}", str(v) if v is not None else "")
    return result
```

**Por qué importa**: este es el método "formal" que reemplaza el f-string del script legacy. Cada `{{VAR}}` del template se sustituye por su valor desde el `mapping` dict.

**Decisión**: usa `str.replace()` en vez de `re.sub()` porque:
- No hay riesgo de inyección regex (las claves del dict son control del autor)
- Más rápido para muchos placeholders pequeños
- Deja `{{VAR}}` intacto si la clave no está en el mapping → detectable por el Bloque C de `--validate`

### 3.4 `build_context(task_id, project_root, vtt_setup_path, token, base_url)`

Hace las llamadas a VTT y deriva todos los valores. Devuelve un dict con:

| Clave | Origen | Notas |
|---|---|---|
| `_task`, `_criteria` | `GET /api/tasks/:id`, `GET /criteria` | Datos brutos para uso interno |
| `_variant` | filesystem `os.path.isdir(worktree)` | A si existe worktree, B si no |
| `ROL_NOMBRE`, `ROL`, `ROL_LOWER` | `ROLE_BY_EMAIL[assignee.email]` | Falla con `RuntimeError` si email no está en el mapa |
| `TASK_ID`, `TITULO` | task.id + task.title | — |
| `SPRINT`, `PHASE` | `detect_sprint_code`, `detect_phase_folder` | Normalización con regex |
| `SLUG` | `slugify(task.title)` | Para nombres de archivo |
| `PROJECT_ROOT`, `REPO`, `CWD_DEL_AGENTE` | Inputs + `ROLE_TO_REPO[rol]` | `CWD_DEL_AGENTE` cambia según variante |
| `AGENT_UUID`, `SERVICE_KEY` | Mapping + constante | Service key fijo de Memory Service |
| `PORT` | `port_for_task(task_id)` | Fixed dict + fallback `3000 + (suffix % 1000)` |
| `LISTA_CAs` | `build_cas_section(criteria)` | Lista con UUID + título por CA |

**Falla si**: task no existe en VTT (`RuntimeError` → exit 3), agente no está en `ROLE_BY_EMAIL` (`RuntimeError` → exit 2).

### 3.5 `vtt_post_comment(task_id, message, user_id, token, base_url, chunk_size=5000)`

Postea el mensaje como comment, con **chunking automático** si supera 5000 chars.

**Por qué importa**: el bug original que motivó el fix anterior. El backend VTT rechaza comments >5000 chars con HTTP 400.

**Algoritmo**:
1. `effective = chunk_size - 8` (reserva 8 chars para prefijo `[N/N]\n`)
2. Divide el mensaje en chunks de `effective` chars
3. Si hay >1 chunks, prepende prefijo `[1/N]\n`, `[2/N]\n`, etc.
4. POST cada chunk como comment separado
5. Devuelve lista de `comment_ids`

**Output esperado**: mensaje de 11.287 chars → 3 chunks → 3 comments.

### 3.6 `validate_message(message_path, token=None, base_url=...)`

3 bloques de checks, 20+ validaciones individuales.

#### Bloque A — Secciones obligatorias (10 checks)
1. Sección `WORKING DIRECTORY` presente
2. NO quedan markers `<!-- VARIANTE A/B -->` (significaría que `strip_variant` no se ejecutó)
3. Patrón `feature/<TASK_ID>` (branch)
4. `Execution manifest:` con path `.vtt/manifests/<TASK_ID>.execution.json`
5. `Workspace VSCode:` con `.code-workspace`
6. Sección `NORMATIVA DE REFERENCIA`
7. Invocación de `VTT.SCRIPT-MAN-001_gen_task_manifest.py` con flags pre-rellenados
8. Sección `ENTREGABLES AL CERRAR` con `git add knowledge/task-manifests/...`
9. Definición `$VTT_SETUP=...`
10. Sección `QUE PASA DESPUES`
+ Warning: referencia a `VTT.SKILL-REPORT-001` (I1 v2.1)

#### Bloque B — Coherencia cruzada con VTT (requiere token)
1. `agent_uuid` del mensaje == `assignee.id` de VTT
2. `taskId` en path execution_manifest == `TASK_ID` del mensaje
3. `worktree_path` existe en disco
4. CAs listadas (count + UUIDs) coinciden con `GET /criteria`
5. Reporte en `knowledge/task-manifests/` (no `knowledge/agent-tasks/reports/` deprecado en v2.1)

#### Bloque C — Higiene (5 checks)
1. 0 placeholders `{{[A-Z_]+}}` sin resolver
2. Endpoint devlog correcto (no `/devlog-entries` SIN wrapper)
3. Endpoint fulfill CAs: `PATCH /criteria/:cid` (no `POST /fulfill`)
4. UTF-8 sin mojibake
5. Bloques ` ``` ` balanceados

**Veredicto**: `valid = not any(severity == "error")`. Warnings e info NO marcan invalid.

### 3.7 `main()` — dispatch de 3 modos

```python
if args.validate:    → validate_message() → exit 0 si valid else 4
if args.output:      → render + write_local() → exit 0
if args.post:        → render + write_local + validate interno + post → exit 0
else:                → error args → exit 1
```

**Orden de precedencia**: `--validate` tiene prioridad (no requiere `task_id`). Si no hay flag de modo → error con exit 1.

---

## 4. Modos de operación

| Modo | Argumentos requeridos | Idempotente | Side effects |
|---|---|---|---|
| `--output <path>` | `task_id`, `--project-root`, `--vtt-setup` | ✅ Sí | Escribe archivo local (sobreescribe) |
| `--post` | `task_id`, `--project-root`, `--vtt-setup` | ❌ No | Postea N comments en VTT + guarda copia local |
| `--validate <path>` | `--validate <path>` | ✅ Sí | Solo lectura, sin escrituras |

---

## 5. Exit codes (RULE-SCRIPT estándar)

| Code | Significado |
|---|---|
| 0 | OK |
| 1 | Argumentos inválidos (falta task_id en `output`/`post`, falta `--project-root`, etc.) |
| 2 | Precondición no cumplida (template no existe, agente no en `ROLE_BY_EMAIL`, sin token) |
| 3 | HTTP error de VTT (404 task no existe, 401 token inválido) |
| 4 | Validate falló (mensaje no cumple template — `--validate` devolvió `valid: false`) |

---

## 6. Decisiones de diseño

### D1 — stdlib pura (sin requests/httpx)

**Por qué**: el script se ejecuta en cualquier worktree sin `pip install`. `urllib.request` es feo pero universal. Mismo patrón que `VTT.SCRIPT-MAN-001` y `VTT.SCRIPT-EXM-001`.

### D2 — `effective_size = chunk_size - 8` en chunking

**Por qué**: heredado del fix anterior. El prefijo `[N/M]\n` agrega ~6-8 chars al chunk. Reservar 8 garantiza que `chunk + prefijo ≤ 5000`. Primer intento `chunk_size = 5000` sin reserva → 5006 chars → 400.

### D3 — `strip_variant` antes de `resolve_placeholders`

**Orden importante**: si resuelvo placeholders primero, los markers HTML quedan adentro de bloques expandidos y el regex de `strip_variant` puede no encontrarlos por interpolación de variables. Strip first, resolve second.

### D4 — Validación interna en `--post` (R4 de la skill)

`--post` ejecuta `validate_message()` sobre el archivo generado ANTES de postear. Si retorna `valid:false` → NO postea, retorna exit 4. Esto previene postear mensajes rotos (caso MS-333 nunca puede volver).

### D5 — Skip Bloque B si no hay token

`--validate <path>` se puede usar sin token. Bloque B (coherencia cruzada con VTT) requiere consultar la task, así que se reporta como `severity: info` "skipped" en vez de error. Esto permite validar mensajes locales offline.

### D6 — `ROLE_BY_EMAIL` como dict in-source

Acepta 2 convenciones de email por rol (legacy `memory-service.{rol}@vtt.ai` y nuevo `{rol}@memory-service.vtt.ai`). Para añadir un proyecto nuevo: agregar entradas al dict. **NO mover a archivo externo** — la skill MSG-001 documenta el dict como part del contrato del script.

### D7 — `PHASE_MAP` con default fallback

Si el slug de la phase no está en el mapa, devuelve el slug crudo (`unknown` si está vacío). NO falla — permite fases experimentales sin parchear el script.

---

## 7. Dependencias

### Lee:
- `$VTT_SETUP/03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md` (v2.1, RULE-TEMPLATE-001)

### Llama a VTT:
- `POST /api/auth/service-token` — si no hay token en env
- `GET /api/tasks/:id` — metadata de la task
- `GET /api/tasks/:id/criteria` — CAs
- `POST /api/tasks/:id/comments` — solo modo `--post`

### Escribe (filesystem):
- Modo `--output`: el path dado por `--output`
- Modo `--post`: `{project_root}/.vtt/worktrees/project-tl/knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md`
- Modo `--validate`: ninguno (solo stdout JSON)

---

## 8. Pruebas ejecutadas (Checkpoint 1+2+CA-06)

| Caso | Resultado |
|---|---|
| `--validate` sobre `MENSAJE_MS-290.md` | `valid: true` ✅ (1 warning I1, 1 info skip B sin token) |
| `--validate` sobre `MENSAJE_MS-333.md` | `valid: false` ✅ con 9 errors detallados (Bloque A: 7, Bloque C: 2) |
| `--post` sobre VTT MS-328 | 3 comments posteados (chunks `[1/3]`, `[2/3]`, `[3/3]`), 0 placeholders sin resolver, validate interno `valid:true` |
| `grep -c 'f".*###' VTT.SCRIPT-MSG-001*` (CA-02) | 0 ✅ — sin f-strings con headings |
| `python -c py_compile` | OK ✅ |

---

## 9. Migración futura sugerida

- `ROLE_BY_EMAIL` y `PHASE_MAP` podrían migrar a `$VTT_SETUP/02.normativa/05.Catalogs/` cuando se cree esa carpeta (compartirlos con otros scripts de la categoría MSG).
- Si surgen más proyectos VTT con worktrees, considerar leer la lista de roles desde un manifest del proyecto (`{project_root}/.vtt/project.json`) en vez de hardcode.
- Considerar agregar modo `--dry-run` que combina `--output` con `--validate` en una sola invocación.

---

## Cambios respecto al script legacy

| Aspecto | `scripts/gen_mensaje.py` (legacy) | `VTT.SCRIPT-MSG-001_gen_mensaje.py` (nuevo) |
|---|---|---|
| Path | 5 copias en memory-service worktrees | 1 sola copia canónica en `$VTT_SETUP/.../msg/` |
| Formato del mensaje | f-strings con `###` headings (R1 violada) | `open(template).read()` + `replace('{{VAR}}', valor)` ✓ |
| Endpoint devlog en mensaje generado | `/devlog-entries` sin wrapper → HTTP 400 | `/devlog` singular con `description` obligatorio ✓ |
| Variante A/B | `if worktree: ... else: ...` en código | `strip_variant()` que limpia el template |
| Modos | Solo `--post` y `--out-dir` | `--output`, `--post`, `--validate` |
| Validación pre-post | Ninguna | Bloques A/B/C ejecutados antes de postear |
| Chunking >5000 chars | Heredado del fix anterior | Heredado, refinado a `effective = chunk - 8` |
| Trazabilidad de la regla aplicada | No documentado | RULE-SCRIPT-001 + RULE-TEMPLATE-001 en docstring |
