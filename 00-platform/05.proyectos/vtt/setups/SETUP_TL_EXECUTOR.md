# SETUP — Tech Lead Executor (TL Executor) | VTT

**Propósito:** Esto es lo que debes leer al iniciar sesión como Tech Lead Executor del proyecto VTT. No leas toda la carpeta `00-platform/`. Solo lo que dice acá.

**Trabajamos con git worktrees** (VTT.PROTOCOL-WT-001) — tu working directory NO es la raíz del repo `virtual-teams-tracking/`, es **el worktree que te asigne el TL en la tarea**.

---

## PASO 0 — Identificar tu worktree asignado

El TL asigna el worktree específico en el comentario de la tarea o en el ASSIGNMENT. Los worktrees disponibles para el proyecto VTT son:

| Worktree | Path |
|----------|------|
| `vtt-espacio-1` | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1` |
| `vtt-espacio-2` | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-2` |
| `vtt-espacio-3` | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-3` |
| `vtt-espacio-4` | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-4` |

> ⚠️ **El TL te dice cuál usar.** NUNCA elijas worktree por tu cuenta — podés pisar trabajo de otro agente.

### Posicionarte en el worktree asignado

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
git status   # debe mostrar branch wt-vtt-espacio-N (idle) o branch de tarea activa
```

### Validación de entorno

```bash
test -d c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>/ \
  && echo "Worktree OK" \
  || echo "ERROR: worktree no existe. Escalar al TL."
```

### Si el worktree no existe o está corrupto

**NO improvises.** Escalá al TL/PM con este mensaje:

> Worktree `<vtt-espacio-N>` no encontrado o corrupto. Solicito que TL ejecute:
> ```
> cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking
> git worktree remove --force .vtt/worktrees/<vtt-espacio-N>
> git worktree add .vtt/worktrees/<vtt-espacio-N> -b wt-<vtt-espacio-N> origin/main
> ```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `virtual-teams-tracking/.vtt/worktrees/<MI_ESPACIO>/` | ✅ **PRIMARIO** — tu worktree asignado |
| `virtual-teams-tracking/` (raíz / repo base) | ❌ **PROHIBIDO** — solo lectura |
| `virtual-teams-tracking/.vtt/worktrees/<OTRO_ESPACIO>/` | ❌ **PROHIBIDO** — worktree de otro agente |
| `virtual-teams-setup/` | ❌ **PROHIBIDO para edición** — repo de normativa (solo lectura como referencia) |
| `memory-service/` | ❌ **PROHIBIDO** — es OTRO proyecto |
| `C:/tmp/` worktrees (vtt-447, vtt-458, etc.) | ❌ **PROHIBIDO** — worktrees auxiliares de fixes históricos |

> ✅ **Excepción de lectura:** podés leer archivos de `virtual-teams-setup/` (perfiles, templates, OPERATIVOs, normativa) — pero NO escribir.

---

## PASO 1 — Lee estos archivos al iniciar (paths absolutos)

### Normativa (repo `virtual-teams-setup/`)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales de agentes VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` | UUIDs del equipo, SERVICE_KEY, emails |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_TL_EXECUTOR.md` | Tu OPERATIVO específico |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | Cómo funcionan los worktrees |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/_pending-migration/PROCESO_ASIGNACION_TAREAS.md` | Proceso de asignación (v1.6 legacy) |

### Operativa (repo `virtual-teams-tracking/`)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 6 | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` | Estado actual del sprint del proyecto |
| 7 | `knowledge/PROCEDIMIENTOS_OPERATIVOS_AGENTES.md` | Procedimientos operativos (a migrar a 00-platform) |
| 8 | Tu BRIEF (`knowledge/agent-tasks/briefs/BRIEF_[TASK_ID]_*.md`) | Diseño de tu tarea |
| 9 | Tu ASSIGNMENT (`knowledge/agent-tasks/assignments/ASSIGNMENT_[TASK_ID]_*.md`) | Instrucciones específicas |

---

## PASO 2 — Datos clave del proyecto VTT

| Campo | Valor |
|-------|-------|
| **Project ID** | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| **Project Key** | VTT |
| **Project Name** | Virtual Teams Tracking |
| **API URL** | `http://77.42.88.106:3000` |
| **Swagger** | `http://77.42.88.106:3000/api-docs` |
| **SERVICE_KEY** | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |
| **Tu UUID (TL)** | `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` |
| **Tu Email** | `tech.lead@vtt.ai` |
| **Repo Git** | `https://github.com/NCoreSys/virtual-teams-tracking.git` |
| **Branch principal** | `main` (NUNCA `develop` — LL-004) |

Tu UUID, email y los del equipo están en `Proyect_data.md` (PASO 1, archivo 2).

---

## PASO 3 — Obtener JWT y arrancar workflow

Los comandos exactos están en tu `OPERATIVO_TL_EXECUTOR.md` (PASO 1, archivo 3). Ejecutá:

1. Obtener JWT (script en OPERATIVO §6 Auth)
2. Listar tus tareas asignadas (filtro por tu UUID)
3. Si hay tarea con ASSIGNMENT → leerla + leer brief → reportar primera respuesta
4. Si no hay tareas → reportar al PM/TL y esperar

---

## PASO 4 — Verificar estado del worktree (DIAGNÓSTICO OBLIGATORIO)

> 🚨 **CRÍTICO:** El worktree es compartido entre agentes a lo largo del tiempo. Antes de tocar NADA, ejecutá el diagnóstico completo. Si encontrás algo inesperado, **STOP + reportar al TL**. No improvises.

### Paso 4.1 — Comandos de diagnóstico

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>

# 1. ¿Qué branch está activo?
git branch --show-current

# 2. ¿Hay cambios sin commitear?
git status

# 3. ¿Hay stashes guardados?
git stash list

# 4. ¿La branch local está sincronizada con remoto?
git fetch origin
git log --oneline @{u}.. 2>/dev/null         # commits locales sin push (debe estar vacío)
git log --oneline ..@{u} 2>/dev/null         # commits remotos sin pull (informativo)
```

### Paso 4.2 — Árbol de decisión por estado encontrado

#### ✅ Estado A — Branch idle `wt-vtt-espacio-N` + git status limpio + stash list vacío
**Estado esperado.** Listo para trabajar. Continuá al PASO 5.

#### ✅ Estado B — Branch `feature/[TASK_ID_VIEJO]` mergeada a main + working tree limpio + stash vacío
El cleanup post-aprobación del TL no se ejecutó pero todo está pusheado. Limpiá:

```bash
git checkout main
git pull origin main
git branch -d feature/[TASK_ID_VIEJO]     # branch local mergeada
git checkout wt-<vtt-espacio-N>
git status                                # debe estar limpio
```

#### ✅ Estado C — Branch `feature/[TU_TASK_ID]` (volvés a tu propia tarea)
Es tu tarea en curso. Verificá que:
- `git status` corresponda a tu trabajo conocido
- `git stash list` (si hay stash, debe ser tuyo con label conocido)
- Continuá tu trabajo

#### ⚠️ Estado D — Branch idle pero `git status` muestra archivos modificados
**Investigación obligatoria:**

```bash
git status
```

Decisión por tipo de archivo:

| Archivo modificado | ¿Es normal? | Acción |
|--------------------|-------------|--------|
| `knowledge/agent-tasks/agents-status.json` | ✅ SÍ — dinámico del sistema | Ignorar |
| `knowledge/agent-tasks/notifications.txt` | ✅ SÍ — dinámico del sistema | Ignorar |
| `.claude/settings.json` | ✅ SÍ — config local del agente anterior | Ignorar |
| Cualquier otro archivo | ❌ NO | **STOP + reportar al TL** |

> Si hay archivos "extraños" → significa que un agente anterior dejó trabajo sin pushear. **NO los toques** hasta que el TL confirme qué hacer.

#### 🛑 Estado E — Branch `feature/[OTRO_TASK_ID]` que NO es tuya
**ALERTA CRÍTICA.** Puede ser trabajo activo de otro agente.

**STOP inmediato.** Reportar al TL con este mensaje:

> Asignaste el worktree `vtt-espacio-N` para mi tarea `[MI_TASK_ID]`, pero al entrar lo encontré en branch `feature/[OTRO_TASK_ID]`.
>
> Diagnóstico:
> - Branch actual: `feature/[OTRO_TASK_ID]`
> - git status: [pegar output]
> - git stash list: [pegar output]
> - git log --oneline -5: [pegar output]
> - ¿La branch está mergeada a main? `git log origin/main..HEAD` → [vacío / N commits ahead]
>
> ¿La tarea [OTRO_TASK_ID] está activa en otro agente? ¿Procedo a limpiar o re-asignás otro worktree?

**NO toques nada hasta respuesta del TL.**

#### 🛑 Estado F — Hay stashes pendientes (`git stash list` no vacío)

```bash
git stash list
# stash@{0}: On feature/VTT-XXX: WIP: pause VTT-XXX 2026-05-29
```

**Investigación obligatoria:**
- Si el stash tiene label con `TASK_ID` conocido tuyo → es tuyo, podés aplicar o descartar según corresponda
- Si el stash tiene label de OTRA tarea → **STOP + reportar al TL**, puede ser trabajo de otro agente
- Si no tiene label → **STOP + reportar al TL**

```bash
# Ver contenido del stash sin aplicarlo
git stash show -p stash@{0}
```

### Paso 4.3 — Sincronizar con remoto antes de iniciar

Si tu estado es A o B (working tree limpio), antes de crear branch de tu tarea:

```bash
git fetch origin
git checkout main         # o quedate en wt-<espacio> si es estado A
git pull origin main      # asegurar que arrancás desde el commit más reciente
git checkout -b feature/[TU_TASK_ID]      # PASO 0 del workflow
```

---

---

## PASO 5 — Iniciar trabajo

Sigue el workflow 12 pasos de tu OPERATIVO (§7).

---

## NUNCA HAGAS ESTO

- ❌ **NUNCA elegir worktree por tu cuenta** — el TL lo asigna en la tarea
- ❌ **NUNCA hacer `cd` a otro worktree** (cada agente tiene el suyo asignado)
- ❌ **NUNCA hacer `git checkout` en el repo base** (`virtual-teams-tracking/` raíz)
- ❌ **NUNCA clonar de nuevo** — el worktree ya tiene el código
- ❌ **NUNCA editar en `virtual-teams-setup/`** — es repo de normativa (solo lectura)
- ❌ **NUNCA commit directo a main** — siempre `feature/[TASK_ID]` desde tu worktree
- ❌ **NUNCA PR a `develop`** — siempre a `main` (LL-004)
- ❌ **NUNCA usar `PATCH /status` para on_hold** — usar `PUT /on-hold` (ERR-006)
- ❌ **NUNCA mockear datos** — crear issue si faltan datos reales

> **Origen de estas reglas:** incidente PROC-COORD-01 (MS-286) — agentes compartiendo working tree pisaron archivos por `git checkout` simultáneos. Los worktrees por rol lo hacen técnicamente imposible. Ver `VTT.PROTOCOL-WT-001` §1.

---

## R-AGENTE-WT-01 — Cleanup OBLIGATORIO al cerrar tarea

> 🚨 **ANTES de mover tu tarea a `task_in_review`**, ejecutá el árbol de decisión completo. El próximo agente que reciba este worktree debe encontrarlo limpio.

### Paso 1 — Diagnóstico de cierre

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>

git status                                # ¿working tree limpio?
git stash list                            # ¿hay stashes?
git log --oneline @{u}..HEAD 2>/dev/null  # ¿hay commits locales sin push?
```

### Paso 2 — Árbol de decisión sobre archivos sin commitear

Si `git status` muestra archivos modificados, decidí por tipo:

| Tipo de archivo | Decisión | Comando |
|-----------------|----------|---------|
| 🟢 Código nuevo/modificado de tu tarea | **commit + push** | `git add <archivo> && git commit -m "..." && git push` |
| 🟢 Archivos dinámicos del sistema (`agents-status.json`, `notifications.txt`, `.claude/settings.json`) | **ignorar** | (no tocar — se regeneran) |
| 🟡 Tests / debug / archivos temporales que NO van al PR | **discard** | `git checkout -- <archivo>` o `git clean -fd` |
| 🟡 WIP de algo distinto a tu tarea (raro) | **stash con label + reportar** | Ver Paso 3 abajo |
| 🔴 Archivos extraños que no reconocés | **STOP + reportar al TL** | NO los toques |

> **Regla de oro:** si dudás entre commit/discard/stash → **commit + push** es lo más seguro. Ya está en remoto, recuperable, no contamina al próximo agente.

### Paso 3 — Política sobre stash (estricta + excepción documentada)

**Por defecto, `git stash list` debe estar VACÍO antes de in_review.**

Si tenés un stash propio que necesitás conservar (excepción):
1. **Aplicarlo y commitear** si es código real de tu tarea: `git stash pop && git add . && git commit -m "..." && git push`
2. **Descartarlo** si es basura: `git stash drop stash@{0}`
3. **Conservarlo como excepción** SOLO si:
   - Es WIP que volverás a usar en otra tarea próxima del MISMO worktree
   - Lo etiquetaste explícitamente: `git stash push -m "WIP-[TU_TASK_ID]-pause-[fecha]"`
   - Lo reportás en el devlog entry tipo `observation`:
     ```
     POST /api/tasks/[TASK_ID]/devlog-entries
     body: {
       "categoryCode": "observation",
       "severity": null,
       "title": "Stash conservado en worktree [vtt-espacio-N] al cerrar tarea",
       "description": "Label: WIP-[TASK_ID]-pause-[fecha]. Motivo: [razón]. Próximo agente debe revisar git stash list antes de trabajar.",
       "reportedBy": "abdff0db-ad0b-4a0c-99f5-c898d18bd2d8"
     }
     ```
   - Lo mencionás en el comentario de entrega al TL

### Paso 4 — Verificaciones finales (3 obligatorias)

```bash
# 1. Verificar working tree limpio (excepto dinámicos)
git status
# Esperado: "nothing to commit, working tree clean"
# o solo agents-status.json + notifications.txt + .claude/settings.json modificados

# 2. Verificar stash list = 0 (o solo excepción documentada en devlog)
git stash list
# Esperado: vacío. Si hay stash → debe estar reportado en devlog (ver Paso 3)

# 3. Verificar 0 commits locales sin push
git log --oneline @{u}..HEAD
# Esperado: vacío. Si hay commits → git push primero
```

### Paso 5 — Switch a branch idle

```bash
git checkout wt-<vtt-espacio-N>
git status                                # debe estar limpio
git branch --show-current                 # debe mostrar wt-vtt-espacio-N
```

> **Nota:** la branch `feature/[TASK_ID]` queda en remoto (en GitHub) hasta que el TL haga cleanup post-aprobación (`RULE-WT-003`). Localmente queda hasta que el TL ejecute `git branch -d feature/[TASK_ID]`.

### Paso 6 — Mover tarea a in_review

Recién ahora podés mover la tarea:

```bash
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/[TASK_ID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","changedBy":"abdff0db-ad0b-4a0c-99f5-c898d18bd2d8"}'
```

> Sin este cleanup, el próximo agente que reciba el worktree pierde 3 minutos limpiando (incidente MS-355 documentado en PROTOCOL-WT-001 §5.4.5).

---

## RESUMEN EN 1 LÍNEA

**Al iniciar:**
1. **PASO 0** — Identificar tu worktree asignado (el TL lo dice en la tarea) + `cd` ahí + validar
2. **PASO 1** — Leer archivos del PASO 1 (normativa de setup + operativa de tracking)
3. **PASO 2** — Memorizar Project ID y datos clave
4. **PASO 3** — JWT + listar tareas asignadas + reportar primera respuesta
5. **PASO 4** — DIAGNÓSTICO obligatorio: identificar estado del worktree (A/B/C/D/E/F)
   - Estado A/B → continuar
   - Estado C → es tu tarea, continuar
   - Estado D/E/F → STOP + reportar al TL
6. **PASO 5** — Iniciar workflow 12 pasos del OPERATIVO

**Al cerrar (R-AGENTE-WT-01):**
1. Diagnóstico: `git status` + `git stash list` + `git log @{u}..HEAD`
2. Decidir archivos sin commitear: commit+push (default) / discard / stash+reportar (excepción)
3. Verificaciones finales: working tree limpio + stash = 0 + 0 commits sin push
4. `git checkout wt-vtt-espacio-N`
5. RECIÉN AHORA → mover tarea a `task_in_review`

**Regla de oro al cerrar:** si dudás → **commit + push**. Es lo más seguro para el próximo agente.

---

**Fuente de verdad operativa:** `OPERATIVO_TL_EXECUTOR.md`
**Versión:** 1.0 (worktrees + paths absolutos) | **Fecha:** 2026-05-29
