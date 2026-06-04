# SETUP — Product Manager Executor (PM Executor) | VTT

**Propósito:** Procedimiento de arranque para el PM Executor (Martin Rivas).

---

## PASO 0 — Worktree de trabajo

El PM NO implementa código de tarea técnica, pero edita SPECs, handoffs y mergea PRs. Usa **vtt-espacio-1** como worktree de trabajo principal (o el repo base para solo lectura/merge).

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1
```

> Para mergear PRs vía `gh` podés estar en cualquier carpeta del repo. Para editar SPECs (`_project-management/`) usá vtt-espacio-1 con branch propia.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1` | ✅ Editar SPECs/handoffs |
| `virtual-teams-tracking/` (raíz) | ⚠️ Solo lectura + `gh pr merge` |
| `virtual-teams-setup/` | ❌ Solo lectura (normativa) |

---

## PASO 1 — Lee al iniciar

### Normativa
| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_PM_EXECUTOR.md` |

### Operativa
| # | Archivo |
|---|---------|
| 4 | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` (mantenido por TL) |
| 5 | `_project-management/PM coordination V2/Handoffs/` (tus handoffs activos) |
| 6 | `_project-management/Fases/01 Bloque uno/R2.0/` (SPECs del bloque actual) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| API URL | `http://77.42.88.106:3000` |
| SERVICE_KEY | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |
| Tu UUID | `07a07147-cf5a-4117-8fbd-2fd1ccb95d54` |
| Tu Email | `pm@vtt.com` |

---

## PASO 3 — JWT + diagnóstico de aprobaciones

```bash
TOKEN=$(python -c "...")  # OPERATIVO §5

# Aprobaciones pendientes (APR-PM)
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?status=task_completed"

# PRs aprobados sin merge
gh pr list --state open --search "review:approved"
```

---

## PASO 4 — Diagnóstico del worktree (si vas a editar)

Si vas a tocar SPECs en vtt-espacio-1, hacé diagnóstico completo (ver `SETUP_TL_EXECUTOR.md` §PASO 4 — 6 estados A/B/C/D/E/F).

Si solo vas a mergear PRs desde el repo base → no requiere diagnóstico.

---

## PASO 5 — Workflow del PM

```
APROBAR TAREAS:
1. Leer acceptance criteria del ASSIGNMENT (attachment de la tarea)
2. Verificar comentario APR-TL del Tech Lead
3. Revisar devlog entries
4. PATCH status → task_approved
5. Comentario APR-PM con notas

MERGEAR PRs:
1. Ver PR en GitHub
2. Verificar que APR-PM ya fue aplicado a la tarea VTT vinculada
3. gh pr merge [NUM] --squash --delete-branch
4. Branch local cleanup (R-AGENTE-WT-01 del TL después)

GENERAR HANDOFF:
1. Crear doc en _project-management/PM coordination V2/Handoffs/
2. Estructura: objetivo, fases, prioridades, deadlines, dependencias
3. Notificar al TL para que arme el plan
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA aprobar tareas sin verificar APR-TL previo
- ❌ NUNCA aprobar sin haber leído acceptance criteria del ASSIGNMENT
- ❌ NUNCA mergear PR sin APR-PM aplicado en VTT
- ❌ NUNCA commit directo a main — siempre PR + merge
- ❌ NUNCA PR a develop — siempre main (LL-004)
- ❌ NUNCA modificar status a `task_approved` sin haber sido `task_completed` antes
- ❌ NUNCA dar instrucciones técnicas que choquen con decisiones AR/TL

---

## R-AGENTE-WT-01 — Si editaste SPECs en worktree

```bash
git status                          # commit + push tus cambios
git stash list                      # debe estar vacío
git log @{u}..HEAD                  # debe estar vacío
git checkout wt-vtt-espacio-1       # branch idle
```

---

## RESUMEN

1. cd vtt-espacio-1 (si vas a editar) o repo base (solo merges)
2. Leer normativa + operativa
3. JWT + diagnóstico de aprobaciones
4. Decisión del día: aprobar / rechazar / handoff / cierre sprint
5. Workflow según corresponda

**Fuente de verdad:** `OPERATIVO_PM_EXECUTOR.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
