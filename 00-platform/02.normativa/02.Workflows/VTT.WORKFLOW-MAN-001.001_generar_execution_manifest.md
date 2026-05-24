# VTT.WORKFLOW-MAN-001.001 — Generar Execution Manifest

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-MAN-001.001` |
| **Pertenece a** | `VTT.PROTOCOL-MAN-001` §5.1 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-17 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL Asignador |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-MAN-001 §5.1.2 (que a su vez es invocado por PROTOCOL-ASG-001 §5.2.11) |

---

## 1. Propósito

Generar el archivo `.vtt/manifests/<TASK_ID>.execution.json` que instruye al agente ejecutor sobre el alcance autorizado de su trabajo: qué paths puede tocar (`allowedPaths`), en qué worktree opera, qué branch usar, qué outputs se esperan.

> Este manifest NO se sube a VTT. Vive en disco local junto al worktree. El agente lo lee al inicio (FASE 2 del Protocol padre) y el TL Reviewer lo usa para verificar disciplina al cerrar.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_id` | string (ej. `MS-XXX`) | Tarea creada en VTT por el TL | sí | ID externo de la tarea |
| `agent_uuid` | uuid | Operativo del agente asignado | sí | UUID del rol que ejecutará |
| `agent_role` | enum (`BE`/`DB`/`FE`/`DO`/`QA`/`DL`/`UX`/`AR`/`SA`) | Operativo del agente | sí | Determina `worktreePath` |
| `assignment_path` | path | ASSIGNMENT generado en paso anterior | sí | Para extraer `allowedPaths` y `expectedOutputs` |
| `project_slug` | string (ej. `memory-service`) | Estructura local del proyecto | sí | Para construir paths absolutos |
| `repo_target` | enum (`backend`/`project`/`frontend`) | ASSIGNMENT §Scope | sí | Determina qué worktree de los del rol |
| `template_path` | path | `.vtt/manifests/_template.execution.json` | sí | Plantilla base — no se modifica, se copia |

---

## 3. Precondiciones

- Tarea existe en VTT con `task.status="task_pending"` o `task.status="task_in_progress"`
- ASSIGNMENT del agente ya fue generado y subido a VTT como attachment
- BRIEF del agente ya fue generado y subido como attachment
- Existe `.vtt/manifests/_template.execution.json` en la raíz del proyecto
- El worktree del rol existe en `.vtt/worktrees/<repo>-<rol>/`
- TL tiene JWT válido (`SKL-AUTH-01` ejecutado)

> **Si una precondición falla:** ver §8 Errores comunes.

---

## 4. Reglas del Workflow

- **R1:** El `allowedPaths` debe ser **explícito y completo**. NO usar wildcards genéricos como `src/**`. Listar carpetas/archivos específicos extraídos del ASSIGNMENT §Scope.
- **R2:** El `branchExpected` siempre sigue el formato `feature/<TASK_ID>` salvo excepciones documentadas en el ASSIGNMENT.
- **R3:** El `worktreePath` apunta al worktree del **rol** (no del task) — el agente reutiliza worktree entre tareas según `RULE-AGENT-001 v2.0`.
- **R4:** Un Execution Manifest por tarea. Si la tarea se rechaza y re-entrega, se sobreescribe el mismo archivo (no se versiona).
- **R5:** Naming del archivo: `<TASK_ID>.execution.json` en minúscula `execution`.

---

## 5. Pasos

### Paso 1 — Cargar template base

Lee la plantilla `.vtt/manifests/_template.execution.json` como JSON. Esta plantilla define la estructura esperada y los campos placeholder.

→ invoca **`VTT.SKILL-EXM-001`** con (`action=load_template`, `template_path=.vtt/manifests/_template.execution.json`)

### Paso 2 — Extraer datos de la tarea desde VTT

Obtener metadata actualizada de la tarea (título, sprint, deliveryId, dependencies):

```
GET /api/tasks/<TASK_ID>
```

→ invoca **`VTT.SKILL-EXM-001`** con (`action=fetch_task_metadata`, `task_id=<TASK_ID>`)

### Paso 3 — Extraer `allowedPaths` del ASSIGNMENT

Parsear el archivo `assignment_path` y extraer la sección `## Scope` o `## Archivos autorizados`. Cada bullet de path se agrega a `allowedPaths[]`.

¿El ASSIGNMENT lista paths explícitos? →
- **SÍ** → copiar tal cual al manifest
- **NO** → STOP y notificar al PJM/PM (ASSIGNMENT mal formado — debe listar paths)

### Paso 4 — Extraer `expectedOutputs` del ASSIGNMENT

Parsear sección `## Entregables` del ASSIGNMENT. Cada entregable se agrega a `expectedOutputs[]` con formato `{type, description}`.

Tipos típicos: `code`, `migration`, `test`, `documentation`, `devlog_entry`, `code_logic`, `pr`.

### Paso 5 — Construir paths del worktree

```
worktreePath = .vtt/worktrees/<project_slug>-<repo_target>-<agent_role_lowercase>/
            o
worktreePath = .vtt/worktrees/<project_slug>-<repo_target>/      (si no hay sub-rol)
```

Verificar que el worktree existe:
```
ls "<worktreePath>"  # debe existir y ser un git worktree válido
```

¿El worktree existe? →
- **SÍ** → continuar
- **NO** → STOP y notificar al TL para que invoque `VTT.WORKFLOW-WT-001.003_agregar_rol` (worktree del rol no creado — ver `VTT.PROTOCOL-WT-001` §5.3)

### Paso 6 — Componer el JSON final

Estructura mínima del Execution Manifest:

```json
{
  "schema_version": "1.0",
  "manifest_type": "execution",
  "generated_at": "<ISO timestamp UTC>",
  "generated_by": "<TL_UUID>",

  "task": {
    "id": "<TASK_ID>",
    "title": "<task.title desde VTT>",
    "sprint": { "id": "<uuid>", "name": "..." },
    "vtt_task_uuid": "<task.id de VTT>"
  },

  "agent": {
    "uuid": "<agent_uuid>",
    "role": "<agent_role>",
    "email": "<email del operativo>"
  },

  "worktreePath": ".vtt/worktrees/<repo>-<rol>/",
  "branchExpected": "feature/<TASK_ID>",

  "allowedPaths": [
    "src/services/foo/",
    "src/services/foo.service.ts",
    "tests/foo.test.ts"
  ],

  "expectedOutputs": [
    { "type": "code", "description": "src/services/foo.service.ts implementado" },
    { "type": "test", "description": "tests/foo.test.ts con coverage ≥80%" },
    { "type": "pr", "description": "PR a main desde feature/<TASK_ID>" }
  ],

  "deadlines": {
    "estimated_hours": <N>,
    "due_at": "<ISO timestamp>"
  },

  "references": {
    "assignment_path": "<assignment_path>",
    "brief_path": "<brief_path desde VTT>",
    "vtt_assignment_attachment_id": "<uuid>",
    "vtt_brief_attachment_id": "<uuid>"
  }
}
```

→ invoca **`VTT.SKILL-EXM-001`** con (`action=compose_manifest`, datos de pasos 1-5)

### Paso 7 — Validar el JSON

→ invoca **`VTT.SKILL-EXM-001`** con (`action=validate`, manifest del paso 6)

Validaciones obligatorias:
- `task.id` no vacío
- `agent.uuid` es UUID válido
- `allowedPaths[].length >= 1`
- `expectedOutputs[].length >= 1`
- `worktreePath` existe en disco
- `branchExpected` matches pattern `feature/<TASK_ID>` o tiene excepción documentada

¿Validación OK? →
- **NO** → corregir los campos que faltan y volver al Paso 6
- **SÍ** → continuar

### Paso 8 — Escribir el archivo

```
write .vtt/manifests/<TASK_ID>.execution.json
```

Si el archivo ya existe (re-entrega) → sobreescribir con mensaje "overwriting previous execution_manifest for <TASK_ID>" en stdout.

### Paso 9 — Verificar

```
cat .vtt/manifests/<TASK_ID>.execution.json | jq '.task.id'
# esperado: "<TASK_ID>"
```

### Paso 10 — Generar mensaje al agente usando el template oficial

**Formato obligatorio:** `$VTT_SETUP/03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md` v2.0

El TL genera el mensaje siguiendo ese template (única plantilla autorizada). Pasos:

1. **Copiar el bloque ` ``` ` del template** (la sección que dice "Cómo usar este template" §1)
2. **Reemplazar todos los placeholders `{{VAR}}`** con datos reales:
   - `{{TASK_ID}}`, `{{TITULO}}`, `{{SPRINT}}`, `{{PHASE}}` — desde VTT (Paso 2)
   - `{{AGENT_UUID}}`, `{{ROL}}`, `{{ROL_NOMBRE}}` — desde el manifest generado en Paso 6
   - `{{PROJECT_ROOT}}`, `{{REPO}}`, `{{CWD_DEL_AGENTE}}` — desde el manifest (`worktreePath`)
   - `{{LISTA_CAs}}` — desde `GET /api/tasks/<TASK_ID>/criteria`
   - Resto de placeholders — ver tabla §"Placeholders" del template
3. **Elegir variante de §Working Directory:**
   - **Variante A** si el proyecto usa worktrees (`.vtt/worktrees/` existe) → borrar variante B
   - **Variante B** si es proyecto clon simple → borrar variante A
4. **Postear el mensaje** como comment en VTT:
   ```
   POST /api/tasks/<TASK_ID>/comments
   { "message": "<contenido del mensaje>", "type": "assignment" }
   ```
5. **Guardar copia local** del mensaje en:
   ```
   knowledge/agent-tasks/messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md
   ```

**El mensaje DEBE incluir** (el template ya lo trae):
- Path del worktree del agente
- Path del execution_manifest generado en este Workflow
- Lista de CAs
- Comando exacto del script `gen_task_manifest.py` que el agente ejecutará al cerrar
- Paso 12 (commit del manifest al PR del agente — ver `WORKFLOW-MAN-001.003`)

> **Atajo automatizado:** si existe `scripts/gen_mensaje.py` en el proyecto, ejecuta:
> ```
> python scripts/gen_mensaje.py <TASK_ID> --post
> ```
> El script lee el template, reemplaza placeholders desde VTT, y postea automáticamente.
>
> **Si el script NO existe** (proyecto sin automatización) → el TL hace los pasos 1-5 manualmente con el template como referencia.

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `<TASK_ID>.execution.json` | archivo JSON | `.vtt/manifests/` | Manifest local del agente |
| Notificación al agente | mensaje markdown | comment VTT + clipboard | Referencia al manifest en el mensaje de asignación |

---

## 7. Validación de salida

```bash
# Check 1: archivo existe
ls .vtt/manifests/<TASK_ID>.execution.json
# Esperado: existe

# Check 2: JSON válido
jq '.' .vtt/manifests/<TASK_ID>.execution.json > /dev/null
# Esperado: sin error

# Check 3: campos obligatorios
jq '.task.id, .agent.uuid, (.allowedPaths | length), (.expectedOutputs | length)' \
   .vtt/manifests/<TASK_ID>.execution.json
# Esperado: id, uuid, num>=1, num>=1

# Check 4: worktree existe
WT=$(jq -r '.worktreePath' .vtt/manifests/<TASK_ID>.execution.json)
ls "$WT"
# Esperado: contenido del worktree
```

- [ ] `.vtt/manifests/<TASK_ID>.execution.json` existe
- [ ] JSON válido (parsea con jq)
- [ ] Campos obligatorios poblados
- [ ] Worktree referenciado existe
- [ ] Mensaje al agente referencia el manifest

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Template no encontrado | `.vtt/manifests/_template.execution.json` no creado | Crear desde `00-platform/03.templates/normativa/_template.execution.json` |
| ASSIGNMENT no lista paths | Mal formado por PJM/TL Asignador | Solicitar regeneración del ASSIGNMENT con §Scope explícito |
| Worktree no existe | Setup de worktrees por rol incompleto | Ejecutar `VTT.WORKFLOW-WT-001.001_setup_inicial` (proyecto nuevo) o `VTT.WORKFLOW-WT-001.003_agregar_rol` (rol nuevo en proyecto existente) |
| `allowedPaths: []` después de paso 3 | Parser no encontró sección | Revisar formato del ASSIGNMENT — debe tener heading `## Scope` o `## Archivos autorizados` |
| JSON inválido al escribir | Encoding incorrecto | Forzar UTF-8 al escribir (`open(..., encoding='utf-8')` en Python) |
| Agente reporta "no encuentro mi manifest" | Path absoluto vs relativo | Verificar que mensaje al agente usa path absoluto del worktree del agente |

---

## 9. Skills invocadas

- `VTT.SKILL-EXM-001` — Skill principal que orquesta este Workflow (load_template, fetch_task_metadata, compose_manifest, validate)
- `VTT.SKILL-AUTH-01` (legacy `SKL-AUTH-01`) — Obtener JWT para `GET /api/tasks/<TASK_ID>`

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-WT-002` Execution manifest | Aplica directamente — esta es la generación del artefacto que define la regla |
| `RULE-AGENT-001 v2.0` Worktree por rol | Determina la estructura del `worktreePath` |
| `RULE-TL-001` Worktree TL | El TL debe ejecutar este Workflow desde su worktree `project-tl` |

Para descubrir reglas adicionales en tiempo de ejecución:
```
python 00.Rules/query_rules.py --context-json '{"task_id":"<TASK_ID>","role":"TL","phase":"assignment"}'
```

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-17 | PM Martin Rivas | Versión inicial. Reemplaza la referencia legacy `VTT.WORKFLOW-ASG-001.021` (que apuntaba al mismo paso 5.2.11 del PROTOCOL-ASG-001 pero sin gobernanza unificada). Ahora vive bajo PROTOCOL-MAN-001. |
