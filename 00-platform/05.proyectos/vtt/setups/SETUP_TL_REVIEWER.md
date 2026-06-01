# SETUP — Tech Lead Reviewer (TL-R / Coordinador) | VTT

**Propósito:** Procedimiento de arranque para el TL Reviewer del proyecto VTT.

**Trabajamos con git worktrees** (VTT.PROTOCOL-WT-001). El TL Reviewer opera principalmente desde **vtt-espacio-1** como "espacio de coordinación".

---

## PASO 0 — Posicionarte en tu worktree de coordinación

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1
```

> El TL Reviewer **no implementa código** — usa el worktree para tener acceso al codebase al hacer review (leer routes, schema, components). Si necesitás ejecutar tarea técnica → cambiá a modo Executor con su propio SETUP.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1` | ✅ **PRIMARIO** (coordinación) |
| `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-2/3/4` | ⚠️ **AUXILIAR** — para hacer review accediendo al PR/branch del agente |
| `virtual-teams-tracking/` (raíz) | ❌ **PROHIBIDO** — solo lectura |
| `virtual-teams-setup/` | ❌ **PROHIBIDO para edición** — repo normativa (solo lectura como referencia) |

---

## PASO 1 — Lee estos archivos al iniciar (paths absolutos)

### Normativa (repo `virtual-teams-setup/`)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` | UUIDs + service key + paths |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_TL_REVIEWER.md` | Tu OPERATIVO |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | Worktrees |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/_pending-migration/PROCESO_ASIGNACION_TAREAS.md` | Proceso asignación v1.6 |

### Operativa (repo `virtual-teams-tracking/`)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 6 | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` | Estado actual del sprint |

---

## PASO 2 — Datos clave del proyecto VTT

| Campo | Valor |
|-------|-------|
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| Project Key | VTT |
| API URL | `http://77.42.88.106:3000` |
| SERVICE_KEY | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |
| Tu UUID | `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` |
| Tu Email | `tech.lead@vtt.ai` |

---

## PASO 3 — JWT + diagnóstico del sprint

```bash
# Obtener JWT (en OPERATIVO §5)
TOKEN=$(curl ...)

# Diagnóstico inicial
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?status=task_in_review"
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?status=task_on_hold"
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?status=task_pending"
```

Reportar al PM (formato §8 del OPERATIVO).

---

## PASO 4 — Diagnóstico del worktree (mismo que TL Executor)

```bash
git branch --show-current
git status
git stash list
git fetch origin
git log --oneline @{u}..HEAD 2>/dev/null
```

**6 estados posibles** (A/B/C/D/E/F) — ver `SETUP_TL_EXECUTOR.md` §PASO 4.2 para árbol completo.

- ✅ A/B → continuar
- ✅ C → tu propia branch en curso
- ⚠️ D → archivos extraños → STOP + investigar
- 🛑 E → branch de otra tarea → STOP + decidir
- 🛑 F → stash sin label → investigar

---

## PASO 5 — Asignar worktree a un agente (cuando creás ASSIGNMENT)

Cuando preparás un ASSIGNMENT para un agente ejecutor, **vos elegís el worktree** que usa:

```
Worktrees disponibles:
- vtt-espacio-1 (TL coordinación)
- vtt-espacio-2 (agente)
- vtt-espacio-3 (agente)
- vtt-espacio-4 (agente)
```

Reglas:
- 1 agente = 1 worktree por tarea
- NO asignar 2 agentes al mismo worktree simultáneamente
- Verificá disponibilidad: `git -C virtual-teams-tracking worktree list` + confirmar que el worktree elegido está idle (no en branch feature de tarea activa)

Documentá en el ASSIGNMENT (sección "Worktree asignado") y en el mensaje al agente.

---

## NUNCA HAGAS ESTO

- ❌ NUNCA aprobar terminalmente (`task_approved`) — es del PM
- ❌ NUNCA mergear PRs — es del PM
- ❌ NUNCA implementar código de prod en modo Reviewer — usá modo Executor
- ❌ NUNCA asignar 2 agentes al mismo worktree en simultáneo
- ❌ NUNCA escribir ASSIGNMENT desde memoria — verificar contra código real
- ❌ NUNCA aprobar sin review gate verde + criterios met
- ❌ NUNCA firmar stage con findings critical/high abiertos
- ❌ NUNCA spawnar sub-agente TL — actuá directo

---

## R-AGENTE-WT-01 — Cleanup al cambiar de worktree

Si rotás entre worktrees durante la sesión (revisar PR del agente en vtt-espacio-2, después volver a vtt-espacio-1):

1. Antes de dejar un worktree, `git status` debe estar limpio (excepto dinámicos)
2. NO commitear cambios en branches de otros agentes
3. Volver siempre a `vtt-espacio-1` para coordinación

---

## RESUMEN

1. **PASO 0** — cd a vtt-espacio-1
2. **PASO 1** — Leer normativa + operativa
3. **PASO 2** — Datos clave
4. **PASO 3** — JWT + diagnóstico sprint
5. **PASO 4** — Diagnóstico worktree (6 estados)
6. **PASO 5** — Al asignar tareas, elegir worktree libre para cada agente

**Fuente de verdad:** `OPERATIVO_TL_REVIEWER.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
