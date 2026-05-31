# VTT.SKILL-EXM-001 — Execution Manifest (Generar / Leer)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-EXM-001` |
| **Categoría** | MAN (Manifest) — sub-tipo execution |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-17 |
| **Aplica a** | TL Asignador (generar) + Agente ejecutor (leer) |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | TL: al asignar tarea (después de crear BRIEF + ASSIGNMENT). Agente: al recibir asignación, ANTES de tocar código. |
| **Schema soportado** | v1.0 (execution_manifest) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `action` | enum | sí | Una de: `load_template` / `fetch_task_metadata` / `compose_manifest` / `validate` / `write_file` / `read_manifest` |
| `task_id` | string (MS-XXX) | sí | ID externo de la tarea |
| `agent_uuid` | uuid | sí (TL) | UUID del agente al que se le asigna |
| `agent_role` | enum | sí (TL) | Rol del agente (BE/DB/FE/DO/QA/DL/UX/AR/SA) |
| `assignment_path` | path | sí (TL) | Ruta al ASSIGNMENT local — fuente para `allowedPaths` y `expectedOutputs` |
| `worktree_path` | path | sí (TL) | Ruta al worktree del rol (`.vtt/worktrees/<repo>-<rol>/`) |
| `branch_expected` | string | sí (TL) | Default `feature/<TASK_ID>` |
| `template_path` | path | sí (TL) | Plantilla en `.vtt/manifests/_template.execution.json` |
| `manifest_path` | path | sí (agente) | `.vtt/manifests/<TASK_ID>.execution.json` |
| `expected_uuid` | uuid | sí (agente) | UUID del propio agente para verificar identidad |

> **Regla contractual:** mismos inputs aplican independiente del rol invocador — el `action` determina qué subset usar.

---

## Precondición

### Para generación (TL)
- ASSIGNMENT del agente ya generado y subido a VTT
- BRIEF del agente ya generado y subido a VTT
- Worktree del rol existe en `.vtt/worktrees/<repo>-<rol>/`
- Plantilla `.vtt/manifests/_template.execution.json` existe
- TL tiene JWT (`SKL-AUTH-01`)

### Para lectura (agente)
- TL ya ejecutó la generación → archivo existe en `.vtt/manifests/<TASK_ID>.execution.json`
- Agente conoce su propio UUID

---

## Variables del entorno

```bash
$TOKEN              # JWT
$VTT_BASE_URL       # default http://77.42.88.106:3000
$AGENT_UUID         # UUID del actor que invoca
$PROJECT_ROOT       # raíz del proyecto local (para resolver .vtt/manifests/)
```

---

## Esquema del Execution Manifest (v1.0)

```json
{
  "schema_version": "1.0",
  "manifest_type": "execution",
  "generated_at": "<ISO timestamp UTC>",
  "generated_by": "<TL_UUID>",

  "task": {
    "id": "<TASK_ID>",
    "title": "<title desde VTT>",
    "sprint": { "id": "<uuid>", "name": "..." },
    "vtt_task_uuid": "<uuid VTT>",
    "estimated_hours": <N>,
    "complexity": "LOW|MEDIUM|HIGH",
    "category": "..."
  },

  "agent": {
    "uuid": "<agent_uuid>",
    "role": "BE|DB|FE|DO|QA|DL|UX|AR|SA",
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
    { "type": "code|migration|test|documentation|devlog_entry|code_logic|pr",
      "description": "..." }
  ],

  "deadlines": {
    "due_at": "<ISO timestamp o null>",
    "soft_deadline_at": "<ISO timestamp o null>"
  },

  "references": {
    "assignment_path": "knowledge/agent-tasks/assignments/.../ASSIGNMENT_<TASK_ID>_<slug>.md",
    "brief_path": "knowledge/agent-tasks/briefs/.../BRIEF_<TASK_ID>_<slug>.md",
    "vtt_assignment_attachment_id": "<uuid>",
    "vtt_brief_attachment_id": "<uuid>"
  },

  "constraints": {
    "must_create_pr": true,
    "must_run_tests": true,
    "must_update_code_logic": true,
    "max_files_outside_allowed_paths": 0
  }
}
```

---

## Ejecución

La Skill orquesta `VTT.SCRIPT-EXM-001` (`gen_execution_manifest.py`):

### Generación (TL)

```bash
python 02.normativa/04.Scripts/manifest/VTT.SCRIPT-EXM-001_gen_execution_manifest.py \
  --task-id "$TASK_ID" \
  --agent-uuid "$AGENT_UUID" \
  --agent-role "BE" \
  --assignment-path "knowledge/agent-tasks/assignments/$PHASE/$SPRINT/ASSIGNMENT_${TASK_ID}_${SLUG}.md" \
  --worktree-path ".vtt/worktrees/backend-be/" \
  --branch-expected "feature/${TASK_ID}" \
  --template-path ".vtt/manifests/_template.execution.json" \
  --output ".vtt/manifests/${TASK_ID}.execution.json"
```

### Lectura (agente)

El script tiene un modo `--validate-and-read` que:
1. Lee el archivo
2. Valida schema v1.0
3. Confirma `agent.uuid == expected_uuid`
4. Imprime `allowedPaths`, `expectedOutputs`, `worktreePath`, `branchExpected` en stdout JSON

```bash
python 02.normativa/04.Scripts/manifest/VTT.SCRIPT-EXM-001_gen_execution_manifest.py \
  --validate-and-read \
  --manifest-path ".vtt/manifests/${TASK_ID}.execution.json" \
  --expected-uuid "$AGENT_UUID"
```

Stdout JSON:
```json
{
  "success": true,
  "worktreePath": "...",
  "branchExpected": "...",
  "allowedPaths": [...],
  "expectedOutputs": [...]
}
```

Exit codes:
- 0 — OK
- 1 — manifest no existe o JSON inválido
- 2 — `agent.uuid` no coincide con `expected_uuid`
- 3 — schema inválido

---

## Validación

### Al generar (TL)

| Check | Falla si |
|---|---|
| `schema_version="1.0"` | distinto |
| `manifest_type="execution"` | distinto |
| `task.id` | vacío |
| `agent.uuid` | no es UUID válido |
| `agent.role` | no en enum |
| `allowedPaths[]` | array vacío o < 1 elemento |
| `expectedOutputs[]` | array vacío |
| `worktreePath` | string vacío |
| Worktree existe en disco | no existe |
| `branchExpected` | no matches pattern `feature/<TASK_ID>` sin excepción documentada |

### Al leer (agente)

| Check | Falla si |
|---|---|
| Archivo existe | no |
| JSON parseable | no |
| `agent.uuid == expected_uuid` | no coinciden |
| `allowedPaths[]` no vacío | vacío |
| Worktree existe en disco | no |

---

## Error común

| Error | Causa probable | Solución |
|---|---|---|
| Template no encontrado | `.vtt/manifests/_template.execution.json` no creado | Generar desde `00-platform/03.templates/normativa/_template.execution.json` |
| ASSIGNMENT no parseable | Mal formato — falta sección `## Scope` | Solicitar regeneración del ASSIGNMENT |
| Worktree no existe | Setup incompleto del rol | Ejecutar setup de worktrees por rol antes |
| `allowedPaths: []` | Parser no encontró paths en ASSIGNMENT | Verificar que ASSIGNMENT tiene heading `## Scope` o `## Archivos autorizados` con bullets |
| Agente rechaza por UUID mismatch | TL se confundió de agente | Regenerar manifest con UUID correcto |
| Manifest sobrescrito en re-entrega | Esperado | Comportamiento correcto — un manifest por tarea, no se versiona |

---

## Scripts invocados

- `VTT.SCRIPT-EXM-001_gen_execution_manifest.py` — script único atómico (~150 líneas) que cubre generación y lectura

---

## Diferencias clave con SKILL-MAN-001

| Aspecto | SKILL-EXM-001 (Execution) | SKILL-MAN-001 (Task) |
|---|---|---|
| Propósito | Instructivo del TL al agente | Entregable queryable de cierre |
| Schema | v1.0 simple (~10 campos) | v1.2 complejo (~80 campos) |
| Ubicación | `.vtt/manifests/` local — NO se sube a VTT | `knowledge/task-manifests/` + VTT attachment |
| Versiones | 1 por tarea (sobrescribe en re-entregas) | v1.0 (agente) + v1.5 (TL) coexisten en VTT |
| Validación | Liviana (que existe, UUID, paths) | Estricta (~15 aborts) |
| Líneas del script | ~150 | ~300 |

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial. Skill nueva — antes existía solo como template suelto `.vtt/manifests/_template.execution.json` sin gobernanza. |
