# VTT.PROTOCOL-MAN-001 — Gobernanza del Manifest

| Campo | Valor |
|---|---|
| **Código** | `VTT.PROTOCOL-MAN-001` |
| **Título** | Gobernanza del Manifest (Task Manifest + Execution Manifest) |
| **Versión** | 1.1.1 |
| **Fecha** | 2026-05-18 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL Asignador, Agentes ejecutores, TL Reviewer, PM (aprobación terminal) |
| **Estado** | Aprobado para uso |
| **Tipo** | Genérico VTT — aplica a cualquier proyecto y cualquier fase del SDLC |
| **Reglas aplicables (Nivel 0)** | Ver `00.Rules/rules_catalog.json` — incluye `RULE-WT-002`, `RULE-VTT-004` (Manifest AL FINAL), `RULE-AGENT-001 v2.0` |
| **Schema del Task Manifest** | v1.2 (definido en `SKL-MAN-001` §Esquema) |
| **Schema del Execution Manifest** | v1.0 (template en `.vtt/manifests/_template.execution.json`) |
| **Protocol relacionado** | `VTT.PROTOCOL-ASG-001` v1.2.0 — este Protocol cubre las 4 invocaciones de manifest de ese ciclo |

---

## Tabla de Contenido

1. [Propósito](#1-propósito)
2. [Campo de Aplicación](#2-campo-de-aplicación)
3. [Responsabilidades](#3-responsabilidades)
4. [Definiciones](#4-definiciones)
5. [Procedimiento](#5-procedimiento)
   - 5.1 [FASE 1 — Generación del Execution Manifest (asignación)](#51-fase-1--generación-del-execution-manifest)
   - 5.2 [FASE 2 — Lectura del Execution Manifest (inicio de ejecución)](#52-fase-2--lectura-del-execution-manifest)
   - 5.3 [FASE 3 — Generación del Task Manifest v1.0 (cierre del agente)](#53-fase-3--generación-del-task-manifest-v10)
   - 5.4 [FASE 4 — Actualización del Task Manifest v1.5 (cierre del TL)](#54-fase-4--actualización-del-task-manifest-v15)
   - 5.5 [FASE 5 — (Futuro) Aprobación PM → v2.0](#55-fase-5--futuro-aprobación-pm--v20)
6. [Referencias Cruzadas](#6-referencias-cruzadas)
7. [Reglas críticas](#7-reglas-críticas)
8. [Resumen de Revisiones](#8-resumen-de-revisiones)

---

## 1. Propósito

Establecer el proceso normativo único para crear, leer, actualizar y validar los **dos tipos de manifest** que VTT usa en el ciclo de una tarea:

- **Execution Manifest** — instructivo local del TL al agente (qué puede tocar, dónde, con qué outputs esperados). No se sube a VTT.
- **Task Manifest** — JSON queryable v1.2 que captura toda la entrega (v1.0 = agente cierra, v1.5 = TL aprueba). Se sube como attachment a VTT.

> **Por qué existe este Protocol:** los manifests se invocan desde 4 puntos del PROTOCOL-ASG-001 (5.2.11, 5.3.2.b, 5.3.9, 5.5.13). Sin gobernanza unificada, cada agente improvisa formato y rompe trazabilidad. Este Protocol es el **único** punto de entrada — los Workflows y Skills se subordinan a él.

## 2. Campo de Aplicación

Aplica a:

- **Toda tarea VTT** que pase por el ciclo `task_pending → task_in_progress → task_in_review → task_completed → task_approved`
- Cualquier rol ejecutor (BE, DB, FE, DO, QA, DL, UX, AR, SA)
- Cualquier categoría de tarea (development, deployment, devops, documentation, testing, design)

No aplica a:

- Tareas internas de coordinación que NO transitan por estados de delivery (ej. comments de planning)
- Manifests de plataforma VTT (código fuente del backend)

## 3. Responsabilidades

### 3.1 TL Asignador
- Generar el **Execution Manifest** al asignar (FASE 1)
- Verificar que el manifest está completo antes de notificar al agente
- Mantener `.vtt/manifests/_template.execution.json` actualizado

### 3.2 Agente ejecutor
- Leer el **Execution Manifest** ANTES de empezar a trabajar (FASE 2)
- Operar SIEMPRE dentro de `allowedPaths` del manifest
- Generar el **Task Manifest v1.0** AL FINAL del workflow (FASE 3) — nunca antes de attachments + status + PRs
- Validar v1.0 contra schema antes de subir

### 3.3 TL Reviewer
- Leer v1.0 del agente
- Aplicar Modelo Dinámico (4 acciones de cierre del PROTOCOL-ASG-001)
- Generar **Task Manifest v1.5** (FASE 4) agregando `review.tl_review` + `delivery.dynamic_model_actions`
- Validar v1.5 contra schema antes de subir
- Verificar disciplina de worktree contra `allowedPaths` del Execution Manifest

### 3.4 PM (terminal — futuro)
- Generar v2.0 con `review.pm_approval` al mover a `task_approved` (FASE 5 — no implementada aún)

## 4. Definiciones

**Execution Manifest:** archivo JSON local `.vtt/manifests/<TASK_ID>.execution.json` que contiene las instrucciones del TL al agente: `allowedPaths`, `agentId`, `expectedOutputs`, `taskId`, `branchExpected`. **No se sube a VTT** — vive en disco junto al worktree.

**Task Manifest:** archivo JSON `<TASK_ID>.json` (schema v1.2) con el ciclo de vida completo de la tarea. Se sube a VTT como attachment `fileType=manifest`.

**Schema v1.2:** versión actual del JSON schema del Task Manifest. Definido formalmente en `SKL-MAN-001 §Esquema`. Reemplaza v1.0/v1.1 (eliminó el blob `skl_report_01_full` que contaminaba con texto duplicado).

**v1.0 / v1.5 / v2.0:** versiones del *instance* (tarea individual), NO del schema. v1.0 la genera el agente, v1.5 el TL, v2.0 el PM (futuro).

**Wrapper .md:** archivo markdown que envuelve el JSON dentro de un bloque ` ```json ` para poder subirlo a VTT como attachment (el backend no acepta MIME application/json puro).

**`allowedPaths`:** lista del Execution Manifest con las rutas que el agente PUEDE modificar. Cualquier path fuera de esta lista → violación de disciplina → `task_rejected`.

**PROC-MANIFEST-01:** lección aprendida — el Task Manifest debe generarse AL FINAL del workflow para evitar campos null en `delivery.*`. Caso fuente: MS-284 con 10+ campos null por generación prematura.

**Modelo dinámico:** 4 acciones del cierre que el TL aplica (crear TIs detectados, agregar evidencias con marker, resolver devlog entries, registrar todo en `delivery.dynamic_model_actions` del v1.5). Definido en `SKL-DYNAMIC-MODEL-01`.

## 5. Procedimiento

### 5.1 FASE 1 — Generación del Execution Manifest

> **Trigger:** TL terminó de generar ASSIGNMENT y va a notificar al agente (paso 5.2.11 del PROTOCOL-ASG-001).
> **Quién ejecuta:** TL Asignador.

5.1.1 TL verifica que existen: tarea en VTT, BRIEF y ASSIGNMENT como attachments, agente identificado con UUID → **[ACTIVIDAD]**

5.1.2 TL genera el Execution Manifest → **[PROCESO]** → ver `VTT.WORKFLOW-MAN-001.001_generar_execution_manifest`
   - Output: `.vtt/manifests/<TASK_ID>.execution.json`
   - Invoca: `VTT.SKILL-EXM-001` (que orquesta `VTT.SCRIPT-EXM-001`)

5.1.3 TL valida el manifest generado contra estos campos obligatorios → **[ACTIVIDAD]**:
   - `taskId` (MS-XXX)
   - `agentId` (UUID del rol)
   - `allowedPaths[]` (≥1 entry, paths relativos al repo)
   - `branchExpected` (típicamente `feature/<TASK_ID>`)
   - `worktreePath` (`.vtt/worktrees/<repo>-<rol>/`)
   - `expectedOutputs[]` (lista descriptiva de qué debe entregar el agente)

5.1.4 ¿Manifest válido? → **[DECISIÓN]**
- **NO** → corregir y regenerar
- **SÍ** → continuar

5.1.5 TL referencia el manifest en el mensaje al agente → **[ACTIVIDAD]**:
   - Mensaje incluye: "Lee `.vtt/manifests/<TASK_ID>.execution.json` ANTES de empezar"
   - Mensaje incluye: path al worktree donde el agente debe operar

5.1.6 **Fin de FASE 1.** El agente recibe el mensaje y procede a FASE 2.

---

### 5.2 FASE 2 — Lectura del Execution Manifest

> **Trigger:** agente recibió el mensaje de asignación y va a empezar a trabajar (paso 5.3.2.b del PROTOCOL-ASG-001).
> **Quién ejecuta:** Agente ejecutor.

5.2.1 Agente lee el Execution Manifest → **[PROCESO]** → ver `VTT.WORKFLOW-MAN-001.002_leer_execution_manifest`
   - Input: `.vtt/manifests/<TASK_ID>.execution.json`
   - Output: validación local de que puede empezar

5.2.2 Agente verifica que su `agentId` coincide con el del manifest → **[ACTIVIDAD]**
   - Si NO coincide → STOP y escalar al TL (no es su tarea)

5.2.3 Agente verifica que está en el `worktreePath` correcto → **[ACTIVIDAD]**
   ```
   pwd                         # debe terminar en .vtt/worktrees/<repo>-<rol>
   git branch --show-current   # debe ser feature/<TASK_ID> o creará la branch
   ```

5.2.4 Agente memoriza `allowedPaths` y opera dentro de ese alcance durante toda la ejecución → **[ACTIVIDAD]**
   - Cualquier archivo que el agente quiera tocar debe estar dentro de `allowedPaths`
   - Si necesita tocar algo fuera → STOP y escalar (no inventar)

5.2.5 Agente memoriza `expectedOutputs` y los usa como checklist final → **[ACTIVIDAD]**

5.2.6 **Fin de FASE 2.** Agente procede con su workflow normal del ASSIGNMENT.

---

### 5.3 FASE 3 — Generación del Task Manifest v1.0

> **Trigger:** agente terminó su workflow (paso 5.3.9 del PROTOCOL-ASG-001). Específicamente, ANTES debe haber completado:
>
> 1. ✅ Reporte SKL-REPORT-01 guardado como archivo local
> 2. ✅ Extracto del reporte posteado como comment en VTT
> 3. ✅ Devlog subido como attachment `fileType=devlog`
> 4. ✅ Code Logic subido (real o placeholder N/A) como `fileType=code_logic`
> 5. ✅ Status moveado a `task_in_review`
> 6. ✅ PR(s) creados con URL específica
> 7. ✅ CAs reportados con `PATCH /criteria/:cid`
> 8. ✅ Review Gate `canProceedToReview=true`
>
> Si CUALQUIERA de los 8 anteriores no está hecho → NO generar el manifest. Quedan campos null.
>
> **Quién ejecuta:** Agente ejecutor.

5.3.1 Agente verifica los 8 precondiciones del trigger → **[ACTIVIDAD]**
   - Si alguna falta → completarla primero
   - Si todas OK → continuar

5.3.2 Agente genera el Task Manifest v1.0 → **[PROCESO]** → ver `VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10`
   - Input: `report_file_path`, `task_id`, `agent_uuid`, JWT token
   - Output: `<TASK_ID>.json` (schema v1.2) + wrapper `.md`
   - Invoca: `VTT.SKILL-MAN-001` (que orquesta `VTT.SCRIPT-MAN-001`)

5.3.3 Agente valida v1.0 contra schema antes de subir → **[ACTIVIDAD]**
   - Validaciones obligatorias (ver `SKL-MAN-001 §Validación v1.0`):
     - `schema_version="1.2"`
     - `delivery.what_was_done` no vacío (>20 chars)
     - `delivery.deliverables_actual[]` ≥ 1 entrada con `{path, state, what}`
     - `delivery.report_file_path` existe en disco
     - `delivery.vtt_report_comment_id` presente
     - `delivery.vtt_attachments.devlog_id` presente
     - `delivery.review_gate.canProceedToReview=true`
     - `delivery.git.{pr_url, pr_number, commit_sha}` presentes (o `note` si DevOps)
     - `indexes.deliverables_paths` espeja `delivery.deliverables_actual[].path`
     - `review.tl_review === null` (NO tocar — es del TL)

5.3.4 ¿Validación v1.0 OK? → **[DECISIÓN]**
- **NO** → corregir campos y regenerar
- **SÍ** → continuar

5.3.5 Agente sube el v1.0 como attachment `fileType=manifest` → **[ACTIVIDAD]**
   - Wrapper `.md` con bloque ` ```json ` (VTT no acepta application/json puro)
   - Local: `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json` + `<TASK_ID>.manifest.md` (un solo par, sin sufijo de versión)

5.3.6 Agente registra el `attachment_id` retornado por VTT en su reporte de entrega → **[ACTIVIDAD]**

5.3.7 **Agente commitea el manifest al PR de la tarea** (OBLIGATORIO) → **[ACTIVIDAD]**
   - Agrega `<TASK_ID>.json` + `<TASK_ID>.manifest.md` al branch `feature/<TASK_ID>` del agente
   - Mismo PR de la tarea (no PR separado)
   - Mensaje: `[<TASK_ID>] manifest v1.0 — agent delivery`
   - Esto preserva snapshot v1.0 en git para auditoría del TL ANTES de que el TL lo sobreescriba con v1.5

5.3.7 **Fin de FASE 3.** Agente ya cumplió con manifest. El TL Reviewer toma el relevo en FASE 4.

---

### 5.4 FASE 4 — Actualización del Task Manifest v1.5

> **Trigger:** TL terminó el Modelo Dinámico (paso 5.5.13 del PROTOCOL-ASG-001). Específicamente, ANTES debe haber completado:
>
> 1. ✅ Review Gate verificado (`canProceedToReview=true`)
> 2. ✅ CAs verificados (todos `met` con evidencia)
> 3. ✅ Attachments verificados (`brief`, `assignment`, `devlog`, `code_logic`, manifest v1.0)
> 4. ✅ PRs verificados en GitHub
> 5. ✅ Disciplina de worktree verificada (diff respeta `allowedPaths` del Execution Manifest)
> 6. ✅ Living Documents declarados
> 7. ✅ Hardcode Check verificado
> 8. ✅ Code review técnico aprobado
> 9. ✅ Modelo Dinámico aplicado (TIs creados, evidencias agregadas, devlog resolved)
> 10. ✅ APR-TL comment posteado
> 11. ✅ Status moveado a `task_completed`
>
> Si CUALQUIERA falta → NO generar v1.5.
>
> **Quién ejecuta:** TL Reviewer.

5.4.1 TL verifica los 11 precondiciones del trigger → **[ACTIVIDAD]**

5.4.2 TL descarga el v1.0 del agente → **[ACTIVIDAD]**
   ```
   GET /api/tasks/<TASK_ID>/attachments
   # filtrar fileType=manifest, generated_by=<agent_uuid>
   ```
   - Output: copia local del v1.0 JSON

5.4.3 TL genera el Task Manifest v1.5 → **[PROCESO]** → ver `VTT.WORKFLOW-MAN-001.004_actualizar_task_manifest_v15`
   - Input: v1.0 del agente + datos de Modelo Dinámico aplicado + APR-TL comment_id
   - Output: `<TASK_ID>_v1.5.json` (schema v1.2) + wrapper `.md`
   - Invoca: `VTT.SKILL-MAN-001` con `--version=1.5`

5.4.4 TL valida v1.5 contra schema antes de subir → **[ACTIVIDAD]**
   - Validaciones específicas v1.5 (ver `SKL-MAN-001 §Validación v1.5`):
     - `task.current_status="task_completed"` (cambió desde `task_in_review`)
     - `last_updated` con timestamp actual del TL
     - `last_updated_block="review.tl_review + delivery.dynamic_model_actions"`
     - `delivery.dynamic_model_actions` presente con `{new_tis_created, evidences_added, devlog_resolved_count}`
     - `delivery.devlog_summary.all_resolved_by_tl=true`
     - `delivery.devlog_entries[].status="resolved"` para los que el TL cerró
     - `review.tl_review.verdict="approved"`
     - `review.tl_review.comment_id` presente (APR-TL comment ID)
     - `review.tl_review.verifications.*` todos `true`
     - `review.pm_approval` queda `null` (es del PM en v2.0)

5.4.5 ¿Validación v1.5 OK? → **[DECISIÓN]**
- **NO** → corregir y regenerar
- **SÍ** → continuar

5.4.6 TL sube el v1.5 como **NUEVO** attachment `fileType=manifest` → **[ACTIVIDAD]**
   - VTT NO permite reemplazar attachments — v1.0 y v1.5 coexisten como historial
   - El backend resuelve "manifest vigente" por `generated_by=TL` + `generated_at` más reciente
   - Wrapper `.md` con bloque ` ```json `
   - Local: el script SOBREESCRIBE el `<TASK_ID>.json` + `<TASK_ID>.manifest.md` que el agente commiteó en su PR
   - Historial del v1.0 del agente queda preservado en `git log` (commit del agente ya mergeado)

5.4.7 TL registra el nuevo `attachment_id` en el APR-TL comment si todavía no lo hizo → **[ACTIVIDAD]**

5.4.8 **TL commitea el v1.5 en su propio PR** (OBLIGATORIO) → **[PROCESO]** → ver `PROTOCOL-ASG-001` §5.5.bis FASE 4.5
   - Branch: `tl/<TASK_ID>-close` desde main
   - Agrega `<TASK_ID>.json` + `<TASK_ID>.manifest.md` overwritten + cualquier otro archivo modificado por el TL durante el review (BRIEF, ASSIGNMENT, etc.)
   - PR a main para aprobación del PM
   - **NO** se hace commit directo a main
   - **NO** se mezcla con el PR del agente (ya mergeado)
   - Garantiza `git status` limpio del worktree TL antes de la siguiente tarea

5.4.8 **Fin de FASE 4.** Manifest v1.5 vigente. PM puede proceder a aprobación terminal.

---

### 5.5 FASE 5 — (Futuro) Aprobación PM → v2.0

> **Estado:** no implementado en v1.0 de este Protocol. Reservado.
> **Cuándo se diseñará:** cuando el PM tenga workflow formal de aprobación terminal.

5.5.1 PM genera `WORKFLOW-MAN-001.005_actualizar_task_manifest_v20` (pendiente)

5.5.2 v2.0 agrega `review.pm_approval` + cambia `task.current_status="task_approved"`

5.5.3 v2.0 NO bumpea schema_version (sigue v1.2) — solo es un instance bump

---

## 6. Referencias Cruzadas

### 6.1 Workflows (Nivel 3) de este Protocol

| Código | Título | Invocado desde |
|---|---|---|
| `VTT.WORKFLOW-MAN-001.001` | Generar Execution Manifest | §5.1.2 |
| `VTT.WORKFLOW-MAN-001.002` | Leer Execution Manifest | §5.2.1 |
| `VTT.WORKFLOW-MAN-001.003` | Generar Task Manifest v1.0 | §5.3.2 |
| `VTT.WORKFLOW-MAN-001.004` | Actualizar Task Manifest v1.5 | §5.4.3 |
| `VTT.WORKFLOW-MAN-001.005` | (Futuro) Actualizar Task Manifest v2.0 (PM) | §5.5 — pendiente |

### 6.2 Skills (Nivel 2) invocadas

| Código | Título | Invocada por |
|---|---|---|
| `VTT.SKILL-MAN-001` | Generar/validar Task Manifest (v1.0 o v1.5) | WORKFLOW-MAN-001.003 y .004 |
| `VTT.SKILL-EXM-001` | Generar/leer Execution Manifest | WORKFLOW-MAN-001.001 y .002 |
| `VTT.SKILL-AUTH-01` (legacy) | Obtener JWT | Todas las anteriores |
| `VTT.SKILL-ATTACH-01` (legacy) | Subir attachment a VTT | SKL-MAN-001 |

### 6.3 Scripts (Nivel 1) ejecutados

| Código | Título | Invocado por |
|---|---|---|
| `VTT.SCRIPT-MAN-001` | `gen_task_manifest.py` | SKILL-MAN-001 |
| `VTT.SCRIPT-EXM-001` | `gen_execution_manifest.py` | SKILL-EXM-001 |

### 6.4 Protocol padre

- `VTT.PROTOCOL-ASG-001` v1.2.0 §5.2.11 / §5.3.2.b / §5.3.9 / §5.5.13 — los 4 puntos del ciclo donde se invoca este Protocol

### 6.5 Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-VTT-004` Manifest AL FINAL (PROC-MANIFEST-01) | Aplica en FASE 3 y FASE 4 — bloquea generación prematura |
| `RULE-WT-002` Execution manifest | Aplica en FASE 1 y FASE 2 |
| `RULE-AGENT-001 v2.0` Worktree por rol | Determina `worktreePath` del Execution Manifest |
| `RULE-TL-001` Worktree TL | TL opera en `project-tl` para generar Execution Manifest |
| `RULE-WT-003` Cleanup post-aprobación | Archivar Execution Manifest tras `task_approved` |

### 6.6 Convenciones operativas (meta-índices)

| Documento | Path canónico | Uso en este Protocol |
|---|---|---|
| Convenciones de filesystem | `02.normativa/00_CONVENCIONES_FILESYSTEM.md` v1.0 | Estructura obligatoria `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json` (+ `.manifest.md`) usada por el script en §5.3.2 y §5.4.3. Define `$VTT_SETUP` para referenciar el setup desde mensajes y operativos. |
| Registro de acrónimos + branches Git | `02.normativa/00_REGISTRO_ACRONIMOS.md` §3.bis v1.2 | Patterns `feature/<TASK_ID>` (agente, §5.3.7) y `tl/<TASK_ID>-close` (TL, §5.4.8) |
| Template del mensaje al agente | `03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md` v2.0 | El mensaje del TL al asignar incluye el comando exacto para que el agente ejecute el script `gen_task_manifest.py` al cerrar |

### 6.7 Documentos relacionados

- `04.docs-soporte/guias-operativas/GUIA_MANIFEST_PARA_AGENTES.md` v4.0 — guía descriptiva (qué/por qué/reglas); este Protocol es la versión normativa ejecutable
- `02.normativa/06.Improvements/IMPROVE-002_bd_manifiestos_y_tis.md` — BD queryable que consumirá los manifests v1.2 cuando se implemente
- `00.Rules/rules_catalog.json` — catálogo de reglas Nivel 0

---

## 7. Reglas críticas

### 7.1 NUNCA generar Task Manifest prematuramente (PROC-MANIFEST-01)

El v1.0 va **AL FINAL** del workflow del agente, después de los 8 precondiciones de §5.3. Si se genera antes, quedan campos null en `delivery.*`.

Lección original: MS-284 tuvo 10+ campos null por generación prematura.

### 7.2 Execution Manifest NO se sube a VTT

Es local del worktree. Vive en `.vtt/manifests/<TASK_ID>.execution.json`. Si alguien lo sube como attachment → ruido. Si alguien lo confunde con Task Manifest → cierre roto.

### 7.3 Task Manifest se SUMA (no reemplaza)

VTT no permite DELETE de attachments. v1.0 y v1.5 coexisten — el backend resuelve "manifest vigente" por `generated_by=TL` + `generated_at` más reciente. Si el TL re-sube v1.5 con corrección, queda como v1.5.1 (3 manifests del mismo task).

### 7.4 Schema version fija en v1.2 — instance version varía

`schema_version="1.2"` en todos los manifests (v1.0, v1.5, futuro v2.0). Las "v1.0/v1.5" se refieren al *instance* (qué bloques están poblados), NO al schema.

### 7.5 Disciplina de worktree del Execution Manifest

El TL Reviewer verifica en §5.5.5.b del PROTOCOL-ASG-001 que `git diff main...feature/<TASK_ID>` solo tocó paths dentro de `allowedPaths` del Execution Manifest. Cross-contamination → `task_rejected`.

### 7.6 DevOps tasks usan bloque `delivery.operations`

Tareas con `task.category ∈ [deployment, devops, operation, sql_migration, rollback, smoke_test, config_change, restart_service]` requieren el bloque `delivery.operations` poblado. Sin él → manifest inválido.

### 7.7 Campos `null` con `note` explicativo

Si `brief`, `assignment`, o `delivery.git` quedan `null` (DevOps típico), agregar campo `note` explicando POR QUÉ. Sin `note` → validador aborta.

---

## 8. Resumen de Revisiones

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-17 | PM Martin Rivas | Versión inicial. Define gobernanza unificada de Task Manifest + Execution Manifest. 4 FASEs operativas + 1 futura (PM v2.0). Consolida los 4 toques del PROTOCOL-ASG-001 (5.2.11/5.3.2.b/5.3.9/5.5.13) bajo un solo Protocol. Reemplaza la confusión histórica donde la GUIA_MANIFEST_PARA_AGENTES.md mezclaba lo descriptivo con lo ejecutable. |
| 1.1.0 | 2026-05-18 | PM Martin Rivas | **Commits a PR obligatorios.** §5.3.5 actualizado: un solo par de archivos (`<TASK_ID>.json` + `<TASK_ID>.manifest.md`) sin sufijo de versión. §5.3.7 nuevo: agente commitea ambos archivos al PR `feature/<TASK_ID>`. §5.4.6 actualizado: TL sobreescribe local. §5.4.8 nuevo: TL commitea v1.5 en branch `tl/<TASK_ID>-close` con PR a main (NO merge directo). Refleja `SCRIPT-MAN-001` v1.2 + `WORKFLOW-MAN-001.003` v1.1.0 + `WORKFLOW-MAN-001.004` v1.1.0 + nueva FASE 4.5 del `PROTOCOL-ASG-001` v1.3.0. |
| 1.1.1 | 2026-05-18 | PM Martin Rivas | Nueva §6.6 **"Convenciones operativas (meta-índices)"** con 3 referencias: `00_CONVENCIONES_FILESYSTEM.md` (path obligatorio del manifest local), `00_REGISTRO_ACRONIMOS.md §3.bis` (branches Git aplicadas en §5.3.7 y §5.4.8) y `TEMPLATE_MENSAJE_ASIGNACION.md` v2.0 (mensaje del TL que invoca el script al cerrar). Sin cambios en procedimiento. |

---

**Fin del Protocol.** Para implementar, ver los 4 Workflows (`VTT.WORKFLOW-MAN-001.001..004`), 2 Skills (`VTT.SKILL-MAN-001`, `VTT.SKILL-EXM-001`) y 2 Scripts (`VTT.SCRIPT-MAN-001`, `VTT.SCRIPT-EXM-001`).
