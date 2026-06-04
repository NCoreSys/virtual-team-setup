# SETUP — Integration Reviewer (IR) | VTT

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

> Típicamente el mismo worktree donde el agente implementó la feature (para acceder al código actual del branch).

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>` | ✅ Solo para ejecutar comandos de verificación |
| Cualquier `src/` | ❌ NUNCA modificar código del dev |
| Otros worktrees | ❌ PROHIBIDO |

> Como IR no escribís código de prod. Tu worktree debe quedar como llegó (solo dinámicos modificados).

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_IR.md` |
| 4 | `.claude/agents/INTEGRATION_REVIEWER.md` (perfil base v1.0) |
| 5 | `00-platform/03.templates/handoff/INTEGRATION_AUDIT_CHECKLIST_V1.1.md` |
| 6 | ASSIGNMENT original (attachment en VTT) — fuente de verdad de lo que debe existir |
| 7 | Schema: `backend/prisma/schema.prisma` |
| 8 | Routes: `backend/src/routes/` |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `fbef6ae6-ba0d-43ce-8cc1-2f28c9c6346d` |
| Email | `integration.reviewer@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas en review asignadas

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?status=task_in_review&assigneeId=fbef6ae6-ba0d-43ce-8cc1-2f28c9c6346d"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Árbol de 6 estados — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

> Estado E (branch de otra tarea) es esperable: vas a revisar la branch `feature/[TASK_ID]` del agente. Verificá que sea la branch que te asignaron.

---

## PASO 5 — Workflow de 19 checks

Ver `OPERATIVO_IR.md` §5-§7.

### Checks A (conformidad)
- A1-A6: archivos, nombres, endpoints, schema, validaciones, campos

### Checks B (integración)
- B1-B8: exports, imports, rutas, tsc, prisma, migration, env vars, middleware

### Checks C (E2E)
- C1: `cd backend && npm run dev` → server inicia
- C2: `curl http://localhost:3000/api/[endpoint]` → 200 + JSON
- C3: response structure correcta
- C4: errores manejados (400/401/403/404/500)
- C5: smoke test (otros endpoints siguen 200)

### Comandos de verificación
```bash
cd backend && npx tsc --noEmit
cd backend && npx prisma validate
cd backend && npm run dev
curl http://localhost:3000/health
```

### Decisión
- 0 críticos → APROBADO (PATCH task_completed + APR-IR)
- >0 críticos → RECHAZADO (REV-IR con feedback, queda in_review)
- >3 medios → RECHAZADO

---

## NUNCA HAGAS ESTO

- ❌ NUNCA aprobar sin ejecutar comandos
- ❌ NUNCA aprobar con críticos abiertos
- ❌ NUNCA corregir código del dev — solo reportar
- ❌ NUNCA agrupar problemas en un issue
- ❌ NUNCA dar feedback ambiguo
- ❌ NUNCA aprobar sin smoke test
- ❌ NUNCA modificar código del repo

---

## R-AGENTE-WT-01

Como no escribís código:
```bash
git status                              # debe estar limpio (solo dinámicos)
git stash list                          # debe estar vacío
git clean -fd                           # eliminar untracked accidentales (test scripts)
```

No volvés a branch idle porque no creaste branch propia.

---

## RESUMEN

1. Worktree asignado por TL → cd
2. Lee perfil IR + ASSIGNMENT (fuente de verdad)
3. JWT + tareas in_review asignadas
4. DIAGNÓSTICO worktree
5. Ejecutar 19 checks
6. Para cada FAIL → issue + evidencia + severidad
7. Reporte APROBADO o RECHAZADO con template
8. Cleanup del worktree

**Fuente de verdad:** `OPERATIVO_IR.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
