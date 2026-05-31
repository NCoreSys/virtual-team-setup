# Cleanup Operativo — Copias locales de scripts (OLA 1 del cierre MSG)

| Campo | Valor |
|---|---|
| **Tipo** | Guía operativa — checklist one-shot |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-22 |
| **Aplica a** | TL Memory Service (y futuros TLs de otros proyectos) |
| **Origen** | OLA 1 cierre sub-sistema MSG — drift visible MS-290 vs MS-333 |
| **Reglas aplicables** | `RULE-SCRIPT-001` v1.0 (no copias locales), `RULE-TEMPLATE-001` v1.0 |
| **Status** | 🟡 PENDIENTE EJECUCIÓN |

---

## 1. Qué problema resuelve

5 copias de `gen_mensaje.py` distribuidas por el proyecto memory-service generaron **mensajes incompatibles** entre tareas asignadas el mismo sprint:

- `MENSAJE_MS-290.md` → correcto (endpoint devlog OK, fulfill CAs OK, sección execution_manifest presente)
- `MENSAJE_MS-333.md` → drift (endpoint devlog incorrecto → HTTP 400, fulfill CAs incorrecto → 404, sección execution_manifest ausente, `$VTT_SETUP` ausente)

El backlog técnico tiene el refactor pendiente (`gen_mensaje.py` → `VTT.SCRIPT-MSG-001` con lectura formal del template). Mientras tanto, este cleanup elimina las **copias divergentes** para reducir el blast radius.

---

## 2. Inventario actual (auditoría 2026-05-22)

### Copias de `gen_mensaje.py` en memory-service (5 copias)

| # | Path | Status |
|---|---|---|
| 1 | `memory-service-project/scripts/gen_mensaje.py` | Origen histórico |
| 2 | `.vtt/worktrees/project-pm/scripts/gen_mensaje.py` | Copia |
| 3 | `.vtt/worktrees/project-sa/scripts/gen_mensaje.py` | Copia |
| 4 | `.vtt/worktrees/project-tl/scripts/gen_mensaje.py` | Copia (la que generó MS-290 — "candidata ganadora") |
| 5 | `.vtt/worktrees/project-tl/scripts/gen_mensaje copy.py` | Duplicado huérfano |

### Copias de `VTT.SCRIPT-MAN-001` en worktrees (al menos 2 detectadas)

| # | Path | Status |
|---|---|---|
| 1 | `.vtt/worktrees/project-tl/scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` | Copia local |
| 2 | `.vtt/worktrees/frontend-fe/scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` | Copia copiada al worktree FE en la sesión MS-333 |

### Fuente única canónica

```
$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py  ← EXISTE (registrada en INVENTARIO 2026-05-17)
$VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py             ← PENDIENTE (tarea de refactor en backlog)
```

---

## 3. Checklist de ejecución (TL)

### Pre-condición

- [ ] Tener una sesión de Claude Code abierta en el worktree TL
- [ ] Confirmar que ninguna tarea VTT está en proceso de asignación AHORA mismo (evitar interrumpir un mensaje en vuelo)
- [ ] Confirmar con el PM que la copia de `project-tl/` es la "candidata ganadora" (la que generó MS-290)

### Paso 1 — Respaldar la copia ganadora antes de borrar

```bash
cd c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl
mkdir -p _archive/gen_mensaje_pre_msg001
cp scripts/gen_mensaje.py _archive/gen_mensaje_pre_msg001/gen_mensaje_2026-05-22.py
git add _archive/
git commit -m "[cleanup-ola1] archive gen_mensaje.py candidata ganadora antes de migración a VTT.SCRIPT-MSG-001"
```

> Esta copia archivada será el **input** del refactor task (CA-01..CA-12) — el DO/BE leerá ese archivo para portar la lógica al script formal.

### Paso 2 — Eliminar las 4 copias divergentes de `gen_mensaje.py`

```bash
# Copias divergentes (NO la ganadora)
rm c:/Users/Martin/Documents/virtual-teams/memory-service/memory-service-project/scripts/gen_mensaje.py
rm c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-pm/scripts/gen_mensaje.py
rm c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-sa/scripts/gen_mensaje.py
rm "c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl/scripts/gen_mensaje copy.py"
```

> La copia de `project-tl/scripts/gen_mensaje.py` queda como ÚNICA viva hasta que el refactor formal la promueva a `$VTT_SETUP`.

### Paso 3 — Eliminar las copias locales de `VTT.SCRIPT-MAN-001`

```bash
# Si existen, eliminarlas — el script vive en $VTT_SETUP
rm c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl/scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py 2>/dev/null || true
rm c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/frontend-fe/scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py 2>/dev/null || true

# Verificar que no quedan más copias
find c:/Users/Martin/Documents/virtual-teams/memory-service -name "VTT.SCRIPT-MAN-001*.py" -not -path "*/virtual-teams-setup/*"
# Esperado: vacío
```

### Paso 4 — Verificar `$VTT_SETUP` definido en cada worktree

Para cada agente activo (BE, FE, DB, DO, QA, TL, PM, SA), verificar que su OPERATIVO o rutina de apertura exporta:

```bash
export VTT_SETUP=c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform
```

Si no lo tiene, agregar al `init-message` del rol.

### Paso 5 — Verificar invocaciones

Auditar que los próximos mensajes posteados por el TL usen el path canónico:

```bash
# El TL ejecuta para asignar
cd c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl

# Mientras NO esté refactorizado el gen_mensaje.py (tarea pendiente):
python scripts/gen_mensaje.py MS-XXX --post

# Cuando esté refactorizado (futuro):
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py MS-XXX --post
```

Para `VTT.SCRIPT-MAN-001` (manifest del agente), **ya** se debe usar el path canónico:

```bash
# CORRECTO ✅
python $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py --task-id MS-XXX ...

# INCORRECTO ❌ (RULE-SCRIPT-001 violación)
python scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py --task-id MS-XXX ...
```

### Paso 6 — Documentar lección en VTT

Postear comment en el último MS de memory-service donde se vio el drift (o crear devlog observation en una task abierta) referenciando esta guía:

```
[OLA 1 MSG] Cleanup de 4 copias divergentes de gen_mensaje.py ejecutado según
$VTT_SETUP/04.docs-soporte/guias-operativas/CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md.
Pendiente refactor formal del script (tarea backlog) — RULE-SCRIPT-001 v1.0 + RULE-TEMPLATE-001 v1.0 activas.
```

### Paso 7 — Commit del cleanup

```bash
cd c:/Users/Martin/Documents/virtual-teams/memory-service
git add -A
git status   # verificar que solo se borran scripts duplicados, nada más
git commit -m "[cleanup-ola1] eliminar copias divergentes de gen_mensaje.py y VTT.SCRIPT-MAN-001

- Mantener única copia viva de gen_mensaje.py en .vtt/worktrees/project-tl/scripts/
- Eliminadas 4 copias divergentes (memory-service-project, project-pm, project-sa, project-tl/copy)
- Eliminadas copias locales de VTT.SCRIPT-MAN-001 (script vive en \$VTT_SETUP)
- Aplica RULE-SCRIPT-001 v1.0 + RULE-TEMPLATE-001 v1.0
- Backup en _archive/gen_mensaje_pre_msg001/

Origen: drift MS-290 vs MS-333
Refs: PROTOCOL-ASG-001 v1.4.0 §5.2.13"
```

---

## 4. Validación post-cleanup

```bash
# Solo 1 copia de gen_mensaje.py debe existir (la del project-tl/)
find c:/Users/Martin/Documents/virtual-teams/memory-service -name "gen_mensaje*.py" -not -path "*/_archive/*"
# Esperado: 1 línea — c:/.../memory-service/.vtt/worktrees/project-tl/scripts/gen_mensaje.py

# 0 copias de VTT.SCRIPT-MAN-001 en worktrees
find c:/Users/Martin/Documents/virtual-teams/memory-service -name "VTT.SCRIPT-MAN-001*.py" -not -path "*/virtual-teams-setup/*"
# Esperado: vacío

# 1 copia de VTT.SCRIPT-MAN-001 en $VTT_SETUP (fuente única)
ls $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001*.py
# Esperado: 1 archivo
```

---

## 5. Que viene después (OLA 2)

Cuando el agente DO/BE complete el refactor task (CA-01..CA-12 del assignment):

1. Eliminar la última copia de `gen_mensaje.py` en `project-tl/scripts/`
2. El TL invoca `python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py` directamente
3. Esta guía se archiva (mover a `04.docs-soporte/legacy/`) — su función ya estará cubierta por las reglas activas

---

## 6. Riesgos conocidos

| Riesgo | Mitigación |
|---|---|
| El TL borra la copia ganadora por error | Paso 1 hace backup explícito antes |
| Algún agente sigue invocando copia local de SCRIPT-MAN-001 | Paso 5 valida que no quedan; RULE-SCRIPT-001 detecta en auditorías futuras |
| Mensaje generado durante el cleanup queda en MS-333 (drift) | Esperar a que NO haya asignación en vuelo (pre-condición) |
| Worktree de algún rol sin `$VTT_SETUP` | Paso 4 valida; agregar al `init-message` del rol si falta |

---

| Editor | Dueño | Última Actualización |
|---|---|---|
| PM Martin Rivas | PM Martin Rivas | 2026-05-22 |

**Versión:** 1.0 — Documento inicial — OLA 1 del cierre del sub-sistema MSG
**Estado:** Listo para ejecución por el TL
