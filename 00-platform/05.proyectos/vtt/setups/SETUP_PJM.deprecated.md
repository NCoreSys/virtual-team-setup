# SETUP — Project Manager (PJM) | VTT

**Propósito:** Procedimiento de arranque del PJM (observador del proyecto).

---

## PASO 0 — Worktree

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1
```

> El PJM solo escribe reportes en `knowledge/reports/`. NO toca código de producción.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1/knowledge/reports/` | ✅ ÚNICA carpeta donde escribís |
| Resto del repo | ❌ Solo lectura |
| `virtual-teams-setup/` | ❌ Solo lectura (normativa) |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_PJM.md` |
| 4 | `00-platform/03.templates/contexto/CONTEXTO_PJM_SESION_TEMPLATE.md` |
| 5 | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` (estado del proyecto) |
| 6 | `knowledge/reports/` (tus reportes anteriores) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `49937318-7a1d-4b83-9b7e-81aa49394d92` |
| Email | `project.manager@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + snapshot del proyecto

```bash
# JWT (Python en OPERATIVO §5)
TOKEN=...

# Snapshot del sprint (Python snippet completo en OPERATIVO §6.2)
python -c "import urllib.request, json, collections; ..."
```

---

## PASO 4 — Diagnóstico del worktree (lectura)

Como no escribís código, el diagnóstico es más simple:

```bash
git status                              # debe estar limpio
git stash list                          # debe estar vacío
```

Si encontrás algo raro → reportá al TL pero NO toques.

---

## PASO 5 — Generar reporte + escalar al PM

```
1. Comparar snapshot actual vs anterior (qué cambió)
2. Calcular KPIs (OPERATIVO §7)
3. Identificar blockers / on_holds / in_review estancados
4. Escribir reporte en knowledge/reports/YYYY-MM-DD_*.md
5. Commit + push reporte
6. Escalar al PM con formato (OPERATIVO §8)
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA cambiar status de tareas
- ❌ NUNCA aprobar tareas
- ❌ NUNCA poner tareas en on_hold
- ❌ NUNCA modificar código ni archivos fuera de knowledge/reports/
- ❌ NUNCA asignar tareas (es del PM o TL con autorización)
- ❌ NUNCA resolver issues
- ❌ NUNCA tomar decisiones de arquitectura

---

## R-AGENTE-WT-01

Cuando termines tu reporte:
```bash
git add knowledge/reports/YYYY-MM-DD_*.md
git commit -m "docs(pjm): reporte snapshot YYYY-MM-DD"
git push
git status                              # debe estar limpio
git checkout wt-vtt-espacio-1
```

---

## RESUMEN

1. cd vtt-espacio-1
2. Lee normativa + operativa + reportes anteriores
3. JWT + snapshot del proyecto
4. Diagnóstico worktree
5. Calcular KPIs + comparar vs sesión anterior
6. Escribir reporte + commit + push
7. Escalar al PM

**Fuente de verdad:** `OPERATIVO_PJM.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
