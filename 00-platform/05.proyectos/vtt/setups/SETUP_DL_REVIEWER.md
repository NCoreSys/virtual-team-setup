# SETUP — Design Lead Reviewer | VTT

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

> Típicamente el mismo worktree donde el FE implementó la feature.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>` | ✅ Solo para levantar frontend y hacer QA Visual |
| `<MI_WORKTREE>/frontend/src/` | ❌ NUNCA modificar código del FE |
| Otros worktrees | ❌ PROHIBIDO |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_DL_REVIEWER.md` |
| 4 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_DL_EXECUTOR.md` (mi otro modo) |
| 5 | Spec del DL Executor (en `_project-management/Documentacion/UI_UX_SPECS/`) |
| 6 | HTMLs del UX en `knowledge/design/screens/` |
| 7 | Tokens vigentes: `frontend/src/index.css` |
| 8 | Implementación FE a auditar (en el worktree) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `ebf0f384-51ba-49f5-8e98-fa7569ce1d31` |
| Email | `design.lead@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas pendientes de review

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?status=task_in_review"
# Filtrar tipo design/ux/frontend manualmente
```

---

## PASO 4 — DIAGNÓSTICO worktree

Árbol de 6 estados — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

---

## PASO 5 — Workflow de review

Ver `OPERATIVO_DL_REVIEWER.md` §5.

### 5.1 Review HTML del UX
- Verificar tokens correctos
- Layout coincide con spec
- Estados presentes
- Responsive
- Accesibilidad básica

### 5.2 QA Visual de implementación FE
```bash
cd <MI_WORKTREE>/frontend
npm ci && npm run dev
# Navegar a la pantalla implementada
# Comparar contra spec/mockup
```

Verificar:
- Tokens correctos (NO hardcoded)
- Spacing/tipografía exactos
- Estados (loading/empty/error/success)
- Responsive
- Hover/focus states
- Accesibilidad

### 5.3 Decisión
- OK → APR-DL en comentario (el TL aprueba técnicamente)
- Cambios → REV-DL con feedback específico (queda in_review)

---

## NUNCA HAGAS ESTO

- ❌ NUNCA aprobar implementación con colores hardcoded
- ❌ NUNCA aprobar sin estados completos
- ❌ NUNCA aprobar mezcla de tokens Landing/App
- ❌ NUNCA implementar el fix yo mismo
- ❌ NUNCA firmar stage design con hardcode pendiente
- ❌ NUNCA aprobar terminalmente (es del PM)
- ❌ NUNCA aprobar mis propios specs

---

## R-AGENTE-WT-01

Como no escribís código:
```bash
git status                              # solo dinámicos
git stash list                          # vacío
git clean -fd                           # eliminar untracked accidentales
```

---

**Fuente de verdad:** `OPERATIVO_DL_REVIEWER.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29

---

## ANEXO (v1.1) — Donde encontrar el REPORT del agente que revisas

> **Cambio v1.1 (2026-06-03):** path canónico del REPORT cambió en SKILL-REPORT-001 v1.1.

Cuando revisas una tarea entregada por un agente ejecutor (BE, DB, FE, DO, etc.), el `<TASK_ID>_REPORT.md` vive en:

```
knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md
```

⚠️ **Path legacy DEPRECADO** (NO buscar ahí para tareas nuevas):
```
knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md
```

El REPORT está en la MISMA carpeta que el `<TASK_ID>.json` + `<TASK_ID>.manifest.md` (los 3 archivos del manifest viven juntos).

Referencia normativa:
- `00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` v1.1 (R6: path canónico) — explica el formato esperado del REPORT (14 secciones) y dónde vive.

Si una tarea vieja tiene el REPORT en el path legacy, dejarlo (legacy compatible). Para tareas nuevas exigir el path canónico al agente. Si el agente entregó en path legacy → rechazar review hasta que mueva al canónico.

---

> **Cambio v1.1 (2026-06-03):** URL backend `:3000` → `https://api.vttagent.com` (VTT-870). SERVICE_KEY hardcoded → `$BE_SERVICE_KEY` del `.env` (rotada VTT-957). Agregado anexo SKILL-REPORT-001 con path canónico — alineado con SETUPs ejecutores.
