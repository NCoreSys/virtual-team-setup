# VTT.WORKFLOW-ASG-001.034 — Agente ejecuta workflow de 13 pasos del ASSIGNMENT

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.034` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.4 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Agente ejecutor (BE/DB/FE/DO/QA/DL/UX/AR/SA) |
| **Reglas Nivel 0** | `RULE-AGENT-001`, `RULE-CODE-001`, `RULE-DELIV-001`, `RULE-DATA-001`, `RULE-GIT-004`, `RULE-SCRIPT-001`, `RULE-TEMPLATE-001` |
| **Origen** | `TEMPLATE_ASIGNACION_TAREARev.md` v3.2 — formaliza los 13 pasos del template como proceso canónico VTT |
| **CARD asociada** | `VTT.CARD-EXE-004` (CARD-large ~2,100 tok) |

---

## 1. Propósito

Formalizar el **ciclo completo de ejecución del agente** desde que abre el ASSIGNMENT hasta que mueve a `task_in_review` con PR creado. Núcleo operativo del agente.

**No cubre:**
- `.031` lectura inputs iniciales
- `.032` verificación worktree
- `.022` lectura execution_manifest
- `.017` Living Documents (sub-workflow)
- `.018` Document Impacts (sub-workflow)
- `.019` Hardcode Check (sub-workflow)
- `.010` entrega final + manifest v1.0 (sub-workflow)

Este workflow es **orquestador** que invoca esos sub-workflows en el orden correcto.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `task_id` | string (MS-XXX) | |
| `agent_id` | UUID | |
| `agent_role` | enum | BE/DB/FE/DO/QA/DL/UX/AR/SA |
| `assignment_path` | path | |
| `brief_path` | path | |
| `worktree_path` | path | |
| `execution_manifest_path` | path | `.vtt/manifests/<TASK_ID>.execution.json` |
| `sprint` | string | |
| `vtt_token` | JWT | |

## 3. Precondiciones

- `.031` `.032` `.022` `.033` completados
- TIs aplicables vinculados a la tarea
- Branch base `main` actualizada
- Git config aplicado

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Branch ANTES de tocar código (`RULE-GIT-004`) |
| R2 | Leer brief COMPLETO (MS-029..035) |
| R3 | Leer TODOS los archivos referencia listados |
| R4 | `.LOGIC.md` espejo por archivo (`RULE-CODE-001`) |
| R5 | Devlog entries durante implementación, no al final |
| R6 | Entries `critical`/`high` `pending` bloquean review gate |
| R7 | PROHIBIDO tocar fuera de `allowedPaths` del manifest |
| R8 | PROHIBIDO mockear datos (`RULE-DATA-001`) |
| R9 | Conflicto TI → `SKILL-ISSUE-001` ANTES de tocar código (MS-328) |
| R10 | Fulfill via `PATCH /criteria/:cid`, NO `POST /fulfill` (404) |
| R11 | Commits con `Co-Authored-By` obligatorio |
| R12 | Verificar `review-gate` ANTES de mover a in_review |
| R13 | Sub-workflows `.017/.018/.019` ANTES de paso 12 |
| R14 | Manifest v1.0 AL FINAL via `.010` (PROC-MANIFEST-01) |
| R15 | PR via `gh pr create` desde worktree del rol |

## 5. Pasos

### Diagrama

```
0. Crear feature/<TASK_ID>
1. task_in_progress (.033)
2. Leer brief COMPLETO
3. Leer N archivos referencia
4. Paso específico de la tarea
5. IMPLEMENTAR
   ├── 5.a devlog entries
   ├── 5.b .LOGIC.md espejo
   └── 5.c Si bloqueante → .035 (FASE 3.5)
6-7. Consolidar
8. Fulfill CAs (PATCH /criteria/:cid)
9. TrackableItems
10. Development Log
11. Commit + push
    ├── precond .017 Living Docs
    ├── precond .018 Document Impacts
    └── precond .019 Hardcode Check
12. Review-gate + in_review (delegado .010)
13. PR
```

### Paso 0 — Crear branch
```bash
cd .vtt/worktrees/<repo>-<rol>
git checkout main && git pull
git checkout -b feature/<TASK_ID> origin/main
```

### Paso 1 — task_in_progress (CARD-EXE-003 / WORKFLOW .033)

### Paso 2 — Leer brief COMPLETO
`SKILL-CFL-001`. Sin saltos. MS-029..035: ~1M tokens perdidos por lectura parcial.

### Paso 3 — Leer N archivos referencia
Listados en sección "DOCUMENTOS DE REFERENCIA OBLIGATORIOS". Si falta uno → STOP.

### Paso 4 — Paso específico de la tarea
Sección "🔴 PUNTO CRÍTICO" del ASSIGNMENT.

### Paso 5 — IMPLEMENTAR
`SKILL-CODE-001`. Reglas R4/R5/R7/R8/R9.

**5.a Devlog entries** (`SKILL-DEV-001`): por decisión técnica / tech_debt / blocker / risk / observation / improvement / brand_issue.

**5.b `.LOGIC.md` espejo** (`RULE-CODE-001`): por cada archivo creado/modificado.

**5.c Si bloqueante** → invocar `WORKFLOW-ASG-001.035` (crear Issue) + `.036` (on_hold).

### Paso 6 — Consolidar devlogs finales

### Paso 7 — Verificar `.LOGIC.md` por archivo
```bash
for f in $(git diff --name-only main...HEAD -- 'src/**'); do
  logic="knowledge/code-logic/${f#src/}"
  logic="${logic%.*}.LOGIC.md"
  [ -f "$logic" ] || echo "FALTA: $logic"
done
```

### Paso 8 — Fulfill CAs
```bash
curl -X PATCH "$VTT_BASE_URL/api/tasks/<TASK_ID>/criteria/<CRITERIA_ID>" \
  -d '{"status":"met","evidence":"<concreta>","notes":"<opt>"}'
```

NO `POST /fulfill` (R10).

### Paso 9 — TrackableItems
Crear/vincular si aplica. N/A si no aplica (declarar explícito).

### Paso 10 — Development Log
`knowledge/development-log/YYYY-MM-DD_<TASK_ID>_<desc>.md`

### Paso 11 — Commit + push (precondiciones obligatorias)

11.a → `WORKFLOW-ASG-001.017` Living Docs
11.b → `WORKFLOW-ASG-001.018` Document Impacts
11.c → `WORKFLOW-ASG-001.019` Hardcode Check

Commit:
```bash
git add <archivos_específicos>
git commit -m "<tipo>(<repo>) [<TASK_ID>]: <descripción>

- Cambio 1

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #<TASK_ID>"

git push origin feature/<TASK_ID>
```

### Paso 12 — Review-gate + in_review

12.a Verificar:
```bash
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>/review-gate"
```

Si `canProceedToReview=false` → resolver `blockers[]` + reintentar.

12.b Delegado: `WORKFLOW-ASG-001.010` orquesta:
1. Generar manifest v1.0 (AL FINAL — PROC-MANIFEST-01)
2. Subir como attachment fileType=manifest
3. SKL-REPORT-01 comment
4. Mover a `task_in_review`

### Paso 13 — PR
```bash
gh pr create --title "[<TASK_ID>] <título>" --body "..." --base main
```

## 6. Outputs

| Output | Descripción |
|---|---|
| `task_status` | `task_in_review` |
| `branch` | `feature/<TASK_ID>` |
| `pr_url` | URL del PR |
| `manifest_v10_path` | `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_v1.0.json` |
| `cas_met_count` / `cas_total_count` | |
| `review_gate_status` | `PASS` |

## 7. Validación

- `review-gate.canProceedToReview = true`
- PR existe en GitHub
- Manifest v1.0 attachment subido + commiteado al PR

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `review-gate` FAIL | Gap en checks | Leer `blockers[]` + resolver |
| 404 fulfill | Endpoint incorrecto | `PATCH /criteria/:cid` (R10) |
| Conflicto TI tardío | No se leyó TIs | Volver al paso 3 + `SKILL-ISSUE-001` |
| Tocar fuera de allowedPaths | Ignoró manifest | Revertir + escalar TL |
| Manifest con campos null | Generado antes | Mover paso al final (R14) |

## 9. Skills invocadas

`SKILL-GIT-001`, `SKILL-STATUS-001`, `SKILL-CFL-001`, `SKILL-CODE-001`, `SKILL-DEV-001..005`, `SKILL-TRK-001..004`, `SKILL-QUERY-003`, `SKILL-STATUS-002`, `SKILL-PR-001`, `SKILL-ISSUE-001` (condicional)

## 10. Sub-workflows invocados

`WORKFLOW-ASG-001.017`, `.018`, `.019`, `.010`, `.035` (condicional), `.036` (condicional), `.038`

## 11. Reglas Nivel 0 aplicables

Ver §4. Lecciones aprendidas críticas: PROC-MANIFEST-01, MS-029..035, MS-328, DEBT-INFRA-VTT-01, DEBT-SEC-01.

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Formaliza PROTOCOL-ASG-001 §5.3.4 (13 pasos del TEMPLATE_ASIGNACION_TAREARev v3.2). Orquesta sub-workflows. |
