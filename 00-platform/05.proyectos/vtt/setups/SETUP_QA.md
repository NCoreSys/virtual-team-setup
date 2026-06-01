# SETUP — QA Engineer (QA) | VTT

**Propósito:** Procedimiento de arranque del QA (cubre QA #1 y QA #2).

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

> El TL te asigna en la tarea cuál usar (típicamente el mismo worktree donde el agente implementó la feature).

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>` | ✅ Solo para LEER código y probar |
| Cualquier `src/` | ❌ NUNCA modificar código de prod |
| Otros worktrees | ❌ PROHIBIDO |

> Como QA no escribís código de prod, tu worktree debe quedar idéntico al estado en que lo recibiste (solo cambios dinámicos del sistema).

---

## PASO 1 — Lee al iniciar

### Normativa
| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_QA.md` |
| 4 | `00-platform/03.templates/handoff/TESTING_GUIDE_V1.1.md` |

### Operativa
| # | Archivo |
|---|---------|
| 5 | ASSIGNMENT de la tarea a testear (attachment) |
| 6 | Acceptance criteria del BRIEF |
| 7 | Swagger: `http://77.42.88.106:3000/api-docs` |
| 8 | Implementación a probar (en el worktree) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID #1 | `1d8eb958-aef7-42f4-ba30-1a7d33a60d39` |
| UUID #2 | `40aea495-5129-4d40-bf10-86f448329f1a` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| API URL | `http://77.42.88.106:3000` |

---

## PASO 3 — JWT + tareas asignadas para testing

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?assigneeId=<TU_UUID>"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Mismo árbol de 6 estados — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

> Para QA es especialmente importante el Estado E (branch de otra tarea) → revisar si es la branch que vas a testear.

---

## PASO 5 — Workflow de testing

```
Para cada tarea asignada:
1. Leer ASSIGNMENT + acceptance criteria
2. Diseñar test cases (o reusar test plan si existe)
3. Levantar entorno:
   - BE: cd backend && npm run dev
   - FE: cd frontend && npm run dev
4. Ejecutar tests:
   - Endpoints con curl (BE)
   - Pantallas en navegador (FE)
   - Edge cases
   - Validaciones (400/401/403/404/500)
   - Regresión de features adyacentes
5. Por cada bug → POST /api/tasks/[TASK_ID]/issues con severidad justificada
6. Reportar resultado al TL Reviewer en comentario:
   - "QA OK: X tests ejecutados, 0 críticos" → APR-TL puede aprobar
   - "QA BUGS: N issues creados, X críticos" → TL no aprueba
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA implementar fixes — solo reportar bugs
- ❌ NUNCA aprobar tareas (es del TL Reviewer)
- ❌ NUNCA cerrar bugs ajenos — solo reportás
- ❌ NUNCA firmar stage testing con bugs critical/high abiertos
- ❌ NUNCA modificar código del repo
- ❌ SIEMPRE issue con severidad justificada + evidencia
- ❌ SIEMPRE probar regresión
- ❌ NUNCA usar PATCH /status para on_hold — usar PUT /on-hold (ERR-006)

---

## R-AGENTE-WT-01

Como QA no escribís código de prod:

```bash
git status                              # debe ser idéntico a cuando llegaste
git stash list                          # debe estar vacío
# Si hay cambios accidentales (test scripts, debug files):
git checkout -- <archivo>
git clean -fd                           # eliminar untracked accidentales
```

No necesitás `git checkout wt-...` porque no creaste branch propia (solo testeaste la del agente).

---

## RESUMEN

1. Worktree asignado por TL → cd
2. Lee operativo + ASSIGNMENT + acceptance criteria
3. JWT + tareas asignadas
4. DIAGNÓSTICO worktree
5. Workflow testing: diseñar tests + ejecutar + reportar bugs como issues
6. Reportar al TL Reviewer (OK / BUGS)
7. Cleanup del worktree (no debiste haber escrito nada)

**Fuente de verdad:** `OPERATIVO_QA.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
