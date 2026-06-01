# VTT.CARD-EXE-004 — Agente ejecuta workflow 13 pasos del ASSIGNMENT

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-004` |
| **Tipo** | `CARD-large` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-EXE-003`, `CARD-MAN-004` |
| **Pertenece a** | WORKFLOW-ASG-001.034 |
| **Tokens estimados** | ~2,100 |

---

## Núcleo operativo del agente

Esta CARD es el **corazón** de tu ejecución. Cubre los 13 pasos canónicos del `TEMPLATE_ASIGNACION_TAREARev.md` v3.2.

### Diagrama

```
0. Crear branch feature/<TASK_ID>
1. Mover a task_in_progress (CARD-EXE-003)
2. Leer brief COMPLETO
3. Leer N archivos de referencia
4. Paso específico de la tarea
5. IMPLEMENTAR código
   ├── (transversal) devlog entries
   ├── (transversal) .LOGIC.md espejo
   └── (transversal) Si bloqueante → CARD-ISS-001 (FASE 3.5)
6-7. Consolidar devlogs y .LOGIC.md
8. Reportar fulfill de CAs
9. Crear/vincular TrackableItems
10. Crear Development Log
11. Commit + push (precond: CARDs EXE-005/006/007)
12. Review-gate + in_review (delegado CARD-EXE-008)
13. Crear PR con gh
```

## Paso 0 — Crear branch (NUNCA tocar código sin esto)

```bash
cd .vtt/worktrees/<repo>-<rol>
git checkout main && git pull
git checkout -b feature/<TASK_ID> origin/main
```

## Paso 5 — IMPLEMENTAR (transversales obligatorios)

### 5.a — Devlog entries durante implementación

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/devlog-entries" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entries":[{
    "categoryCode":"decision",
    "severity":"low",
    "title":"...",
    "description":"...",
    "reportedBy":"<AGENT_UUID>"
  }]}'
```

**Categorías:** `decision` / `tech_debt` / `blocker` / `risk` / `testing_note` / `observation` / `improvement` / `brand_issue`

**Severity:** entries `critical`/`high` `pending` **bloquean review gate** — resolver antes del paso 12.

**Endpoint plural requiere wrapper `{"entries":[...]}`.** Singular `/devlog` recibe entry directo.

### 5.b — `.LOGIC.md` espejo por archivo

```
src/controllers/example.ts → knowledge/code-logic/controllers/example.LOGIC.md
```

Si ya existe → **ACTUALIZAR** (agregar entry "Historial de Cambios"). NUNCA crear segundo. NO incluir código fuente — solo descripciones.

### 5.c — Si bloqueante → CARD-ISS-001 (FASE 3.5)

**PROHIBIDO mockear datos** (`RULE-DATA-001`).
**PROHIBIDO improvisar** ante conflicto TI ↔ ASSIGNMENT (lección MS-328).

Si detectás:
- Datos faltantes → CARD-ISS-001 con `type=dato_faltante`
- Conflicto TI vinculado vs ASSIGNMENT → CARD-ISS-001 con `type=requirement`, severity=`high`
- Dependencia no implementada → CARD-ISS-001 con `type=dependency`
- Error técnico irresoluble → CARD-ISS-001 con `type=tech_error`

## Paso 8 — Fulfill CAs

```bash
curl -X PATCH "$VTT_BASE_URL/api/tasks/<TASK_ID>/criteria/<CRITERIA_ID>" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "met",
    "evidence": "<concreta + path/url/commit SHA>",
    "notes": "<opcional>"
  }'
```

**Endpoint correcto:** `PATCH /criteria/:cid`. **NO usar `POST /fulfill` — devuelve 404.**

Estados: `met` / `not_met` (abrir issue + justificar) / `na` (justificar en notes)

## Paso 11 — Commit + push (precondiciones obligatorias)

**ANTES de commitear, ejecutar en este orden:**

1. **CARD-EXE-005** revisar Living Documents (todos del catálogo, declarar "sin cambios" si no aplica)
2. **CARD-EXE-006** registrar Document Impacts
3. **CARD-EXE-007** ejecutar Hardcode Check (debe ser PASS)

```bash
git add <archivos_específicos>     # NUNCA git add -A en scope acotado
git commit -m "$(cat <<EOF
<tipo>(<repo>) [<TASK_ID>]: <descripción breve>

- Cambio 1
- Cambio 2

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #<TASK_ID>
EOF
)"

git push origin feature/<TASK_ID>
```

**Tipos válidos:** `feat` / `fix` / `docs` / `refactor` / `test` / `chore`

## Paso 12 — Review gate + in_review

Verificar gate:

```bash
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>/review-gate" \
  -H "Authorization: Bearer $VTT_TOKEN" | python -m json.tool
```

Si `canProceedToReview = false` → leer `blockers[]` + resolver + reintentar (max 3).

**Delegado: CARD-EXE-008** orquesta entrega final + manifest v1.0 (AL FINAL, lección PROC-MANIFEST-01).

## Paso 13 — PR

```bash
gh pr create \
  --title "[<TASK_ID>] <título descriptivo>" \
  --body "Ver devlog + manifest. Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>" \
  --base main
```

## Reglas críticas (lecciones aprendidas)

| # | Regla | Lección |
|---|---|---|
| R1 | Branch ANTES de tocar código | `RULE-GIT-004` |
| R7 | PROHIBIDO tocar fuera de `allowedPaths` del manifest | Escalar al TL si requiere |
| R8 | PROHIBIDO mockear datos | `RULE-DATA-001` |
| R9 | Conflicto TI → Issue antes de código | MS-328 (~1M tokens perdidos) |
| R10 | `PATCH /criteria/:cid`, NO `POST /fulfill` | 404 conocido |
| R13 | Sub-workflows `.017/.018/.019` ANTES del paso 12 | Bloquean gate |
| R14 | Manifest v1.0 AL FINAL (delegado a CARD-EXE-008) | PROC-MANIFEST-01 |

## Output

Tarea en `task_in_review`, PR creado, SKL-REPORT-01 posteado, manifest v1.0 subido como attachment + committeado al PR. Listo para review del TL.
