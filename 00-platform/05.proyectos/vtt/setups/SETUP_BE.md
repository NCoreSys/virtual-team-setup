# SETUP — Backend Engineer (BE) | VTT

**Propósito:** Procedimiento de arranque del BE (cubre BE #1 y BE #2).

**Trabajamos con git worktrees** (VTT.PROTOCOL-WT-001) — tu working directory es **el worktree que te asigne el TL en la tarea**.

---

## PASO 0 — Identificar tu worktree asignado

El TL te asigna el worktree en el comentario de la tarea o en el ASSIGNMENT. Worktrees disponibles:

| Worktree | Path |
|----------|------|
| `vtt-espacio-1` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1` (TL coordinación) |
| `vtt-espacio-2` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-2` |
| `vtt-espacio-3` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-3` |
| `vtt-espacio-4` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-4` |

> ⚠️ El TL te dice cuál usar. NUNCA elijas por tu cuenta.

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>` | ✅ PRIMARIO |
| Repo base `virtual-teams-tracking/` | ❌ PROHIBIDO |
| Otros worktrees | ❌ PROHIBIDO |
| `virtual-teams-setup/` | ❌ Solo lectura (normativa) |

---

## PASO 1 — Lee al iniciar

### Normativa
| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_BE.md` |
| 4 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` |

### Operativa
| # | Archivo |
|---|---------|
| 5 | Tu BRIEF (attachment) |
| 6 | Tu ASSIGNMENT (attachment) |
| 7 | `backend/prisma/schema.prisma` (read-only — base del schema) |
| 8 | `backend/src/routes/` (endpoints existentes) |
| 9 | `backend/src/services/` (services existentes para reutilizar patrones) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID #1 | `8834830b-578f-46be-933b-0abcbbc5da99` |
| UUID #2 | `008cacfc-d0cb-41d2-8628-def9571f8c77` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| API URL | `http://77.42.88.106:3000` |
| SERVICE_KEY | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |
| Swagger | `http://77.42.88.106:3000/api-docs` |

---

## PASO 3 — JWT + tareas asignadas

```bash
TOKEN=$(curl -s -X POST http://77.42.88.106:3000/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d '{"userId":"<TU_UUID>","serviceKey":"hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")

curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?assigneeId=<TU_UUID>"
```

---

## PASO 4 — DIAGNÓSTICO obligatorio del worktree

```bash
git branch --show-current
git status
git stash list
git fetch origin
git log --oneline @{u}..HEAD 2>/dev/null
```

**6 estados** (A/B/C/D/E/F) — ver `SETUP_TL_EXECUTOR.md` §PASO 4.2.

- ✅ A/B → continuar (sync con main + crear branch)
- ✅ C → tu tarea en curso
- ⚠️ D → archivos extraños (excepto dinámicos del sistema) → STOP + reportar
- 🛑 E → branch de otra tarea → STOP + reportar al TL
- 🛑 F → stash sin label → STOP + reportar

### Archivos dinámicos del sistema (es normal verlos modificados):
- `knowledge/agent-tasks/agents-status.json`
- `knowledge/agent-tasks/notifications.txt`
- `.claude/settings.json`

---

## PASO 5 — Workflow de 12 pasos

Ver `OPERATIVO_BE.md` §7 — pasos 0-12 con curls y comandos.

Resumen:
```
0. git checkout main && git pull && git checkout -b feature/[TASK_ID]
1. PATCH status → in_progress
2-3. Leer brief + ASSIGNMENT + archivos de referencia
4. Verificar entorno (npm run dev OK, BD accesible)
5. Implementar siguiendo patrón Router → Service → Prisma
6. Crear .LOGIC.md por cada archivo
7. Probar localmente (curl real con 200)
8. Testing manual (edge cases, errors)
9. Development Log
10. Commit + push
11. PR a main con gh CLI
12. Subir attachments (devlog, code_logic) + comentario + PATCH status → in_review
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA modificar `backend/prisma/schema.prisma` (es del DB)
- ❌ NUNCA modificar `docker-compose.yml` / `.env` / `nginx.conf` (es del DO)
- ❌ NUNCA modificar `frontend/` (es del FE)
- ❌ NUNCA inventar campos del schema — verificar contra schema.prisma
- ❌ NUNCA inventar endpoints — verificar contra routes/
- ❌ NUNCA mockear datos — crear issue si faltan
- ❌ NUNCA commit directo a main
- ❌ NUNCA PR a develop — siempre main
- ❌ NUNCA dejar console.log de debug
- ❌ NUNCA endpoint sin try-catch ni Swagger JSDoc inline
- ❌ NUNCA usar PATCH /status para on_hold — usar PUT /on-hold (ERR-006)
- ❌ Comentarios con `!` en bash → ERR-002 → usar Python urllib

---

## R-AGENTE-WT-01 — Cleanup al cerrar

Ver `SETUP_TL_EXECUTOR.md` §R-AGENTE-WT-01 — árbol completo.

**Regla de oro:** ante duda → commit + push. NUNCA dejar trabajo local sin pushear.

Pasos resumidos:
1. `git status` → decidir por tipo de archivo (commit+push default / ignorar dinámicos / discard tests / stash+reportar excepción)
2. `git stash list` → debe estar vacío (excepción documentada en devlog observation)
3. `git log @{u}..HEAD` → debe estar vacío (todo pusheado)
4. `git checkout wt-<vtt-espacio-N>` (branch idle)
5. RECIÉN AHORA → PATCH status → task_in_review

---

## RESUMEN

1. Worktree asignado por el TL → cd ahí
2. Lee normativa + ASSIGNMENT + brief
3. JWT + listar tareas
4. DIAGNÓSTICO worktree (6 estados)
5. Workflow 12 pasos
6. Cleanup R-AGENTE-WT-01 antes de in_review

**Fuente de verdad:** `OPERATIVO_BE.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
