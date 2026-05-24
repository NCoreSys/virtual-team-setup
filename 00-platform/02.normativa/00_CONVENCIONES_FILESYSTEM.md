# Convenciones de Filesystem — Proyectos VTT

| Campo | Valor |
|---|---|
| **Versión** | 1.0 |
| **Fecha** | 2026-05-18 |
| **Mantenedor** | PM Martin Rivas |
| **Audiencia** | TL al iniciar proyecto, agentes al ejecutar tareas, PJM al hacer setup |
| **Source of Truth** | Este archivo define la estructura obligatoria que TODO proyecto VTT debe tener |

---

## 1. Propósito

Estandarizar la estructura de carpetas que **todo proyecto VTT** debe contener para que agentes, scripts y procesos normativos funcionen sin ambigüedad.

> **Problema que resuelve:** sin convención fija, cada proyecto improvisa paths (`S01/`, `04-development/S01/`, `dev/S01/`, etc.). Esto rompe scripts genéricos, queries de IMPROVE-002, y obliga a cada agente a "adivinar" dónde dejar entregables. Caso real: VTT-718 generó manifests en 2 carpetas distintas por drift de paths.

---

## 2. Estructura obligatoria

Todo proyecto VTT (memory-service, virtual-teams-tracking, etc.) debe tener exactamente esta estructura:

```
<project_root>/
├── knowledge/
│   ├── agent-tasks/
│   │   ├── briefs/<phase>/<sprint>/BRIEF_<TASK_ID>_<slug>.md
│   │   ├── assignments/<phase>/<sprint>/ASSIGNMENT_<TASK_ID>_<slug>.md
│   │   ├── messages/<phase>/<sprint>/MENSAJE_<TASK_ID>.md
│   │   └── reports/<phase>/<sprint>/<TASK_ID>_REPORT.md
│   ├── task-manifests/<phase>/<sprint>/<TASK_ID>.json (+ <TASK_ID>.manifest.md)
│   ├── development-log/<YYYY-MM-DD>_<TASK_ID>_<slug>.md
│   ├── code-logic/<modulo>/<archivo>.LOGIC.md
│   └── platform-feedback/ (opcional — gaps/mejoras de VTT)
├── scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py (copia del setup)
├── .vtt/ (opcional — solo proyectos con worktrees por rol)
│   ├── worktrees/<repo>-<rol>/
│   ├── workspaces/<repo>-<rol>.code-workspace
│   └── manifests/<TASK_ID>.execution.json
└── (código del proyecto en su layout natural)
```

### 2.1 Glosario de variables

| Variable | Ejemplo | Donde se define |
|---|---|---|
| `<phase>` | `04-development`, `03-design`, `05-testing` | Estructura SDLC del proyecto |
| `<sprint>` | `S01`, `S06-FIX-A` | Plan del proyecto |
| `<TASK_ID>` | `MS-293`, `VTT-721` | VTT al crear la tarea |
| `<slug>` | `error-handling`, `mime-validation` | Título de la tarea en snake-case |
| `<modulo>` | `backend/src/controllers/`, `frontend/src/components/` | Espejo del código fuente |

---

## 3. Carpetas obligatorias — propósito de cada una

| Carpeta | Quién escribe | Quién lee | Contenido |
|---|---|---|---|
| `knowledge/agent-tasks/briefs/` | TL/PJM al asignar | Agente al iniciar tarea | BRIEF inmutable de la tarea |
| `knowledge/agent-tasks/assignments/` | TL al asignar | Agente al iniciar tarea | ASSIGNMENT (snapshot del estado del proyecto) |
| `knowledge/agent-tasks/messages/` | TL al asignar | Agente (lo recibe en VTT como comment) | Mensaje del TL para arrancar |
| `knowledge/agent-tasks/reports/` | Agente al cerrar tarea | TL al revisar | Reporte SKL-REPORT-01 |
| `knowledge/task-manifests/` | Agente (v1.0) + TL (v1.5) | Auditoría + futura BD IMPROVE-002 | JSON + wrapper .md del manifest |
| `knowledge/development-log/` | Agente durante ejecución | TL al revisar | Devlog narrativo de la tarea |
| `knowledge/code-logic/` | Agente durante ejecución | TL al revisar + agentes futuros | .LOGIC.md por archivo de código (espejo) |

---

## 4. Reglas operativas

1. **Todas las carpetas se versionan en git.** Excepción: `.vtt/` (no se commitea — vive solo en disco local).
2. **Si una carpeta no existe al iniciar tarea, el agente la crea** con `os.makedirs(path, exist_ok=True)` o `mkdir -p` antes de escribir.
3. **No se duplican archivos** entre `<sprint>/` y `<phase>/<sprint>/`. Si el script o agente intenta escribir sin `<phase>/`, es un bug — reportar.
4. **Naming `<TASK_ID>` respeta mayúsculas** como aparece en VTT (`MS-293`, no `ms-293`).
5. **`<slug>` en snake_case minúsculas** sin caracteres especiales (`error-handling` ✅, `Error Handling` ❌).
6. **Un archivo por entregable por versión** — el manifest es el caso especial: `<TASK_ID>.json` + `<TASK_ID>.manifest.md` que se sobreescriben en v1.5 (ver PROTOCOL-MAN-001).

---

## 5. Verificación al iniciar proyecto

Comando que el TL ejecuta al inicializar un proyecto nuevo:

```bash
# Crear estructura completa
mkdir -p knowledge/agent-tasks/{briefs,assignments,messages,reports}
mkdir -p knowledge/{task-manifests,development-log,code-logic,platform-feedback}
mkdir -p scripts/manifest

# Copiar script normativo desde el setup
cp $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
   scripts/manifest/

# Verificar
ls -la knowledge/agent-tasks/
ls -la knowledge/
ls scripts/manifest/
```

---

## 6. Verificación al iniciar tarea (agente)

Antes de escribir entregables, el agente verifica que su `<phase>/<sprint>/` existe:

```bash
PHASE=04-development
SPRINT=S01
TASK_ID=MS-XXX

mkdir -p knowledge/agent-tasks/{briefs,assignments,messages,reports}/$PHASE/$SPRINT
mkdir -p knowledge/task-manifests/$PHASE/$SPRINT
```

Si la carpeta del sprint anterior no tiene `<phase>/`, es proyecto legacy — reportar al TL para migración.

---

## 7. Variable de entorno $VTT_SETUP

Todos los operativos (TL, agentes) deben tener cargada esta variable:

```bash
export VTT_SETUP=c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform
```

Apunta al Source of Truth de la normativa VTT. Mensajes y operativos referencian archivos como `$VTT_SETUP/02.normativa/...`.

> **Por qué:** evita hardcodear paths absolutos en cada mensaje. Si el setup se mueve, solo cambia 1 variable.

---

## 8. Cambios incompatibles con esta convención

Si un proyecto tiene paths legacy (ej. archivos directamente en `S01/` sin `<phase>/`):

1. Identificar archivos legacy con `find knowledge/ -path '*/S0*/*' -not -path '*/[0-9][0-9]-*/*'`
2. Crear PR `chore/filesystem-migration-<proyecto>` que mueve archivos legacy a `_archive/<phase>/<sprint>/`
3. NO se eliminan (preservar para auditoría)
4. Documentar en `platform-feedback/` el caso

---

## 9. Documentos relacionados

- `02.normativa/00_REGISTRO_ACRONIMOS.md` §3.bis — Convenciones de branch Git
- `02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001` — Ciclo de asignación (qué entregables genera el agente)
- `02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001` — Gobernanza del manifest (qué carpeta usa)
- `03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md` — Mensaje del TL al agente (referencia $VTT_SETUP)

---

## 10. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-18 | Versión inicial. Formaliza la estructura `knowledge/agent-tasks/{briefs,assignments,messages,reports}/<phase>/<sprint>/` que ya se usaba de hecho en memory-service pero sin convención. Define `$VTT_SETUP` como variable de entorno para referenciar el Source of Truth. Origen: drift de paths detectado en VTT-718 (archivos duplicados en `S06-FIX-A/` y `04-development/S06-FIX-A/`). |
