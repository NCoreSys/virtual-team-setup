# VTT.SKILL-FILE-001 — Ubicar entregable en estructura del proyecto

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-FILE-001` |
| **Categoría** | FILE (Filesystem) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | SA, DL, UX, AR, TL, BE, DB, FE, QA, DO, SA Reviewer, PJM, PM |
| **Tokens estimados** | ~200 |
| **Cuándo se usa** | Antes de crear cualquier entregable — determinar ruta correcta |
| **Reemplaza** | `SKL-STRUCTURE-01_ubicar-entregable.md` (legacy, categoría legacy `FILE-STRUCTURE`) |

---

## Regla fundamental

> **Todo entregable de fase va en `phases/<fase>/deliverables/`.** NUNCA en `docs/`, `Release2.0/`, ni carpetas ad-hoc.

**Source of Truth:** `02.normativa/00_CONVENCIONES_FILESYSTEM.md` v1.0 + `04.docs-soporte/guias-operativas/ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md`

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `fase` | enum | sí | Identificador de la fase (ver tabla abajo) |
| `deliverable_id` | string | sí | ID jerárquico del deliverable (ej. `0.3.1`, `3B.1.1`) |
| `descripcion_corta` | string snake_case | sí | Slug del nombre |

---

## Variables del entorno

Ninguna específica.

---

## Mapa fase → carpeta

| Fase del SDLC | Tareas típicas | Carpeta de entregables |
|---|---|---|
| **Discovery** | Problem statement, Value proposition, Personas iniciales | `phases/00-discovery/deliverables/` |
| **Planning** | Vision, Scope, Roadmap, Risks | `phases/01-planning/deliverables/` |
| **Analysis** | User Stories, Use Cases, Functional & Non-Functional Reqs | `phases/02-analysis/deliverables/` |
| **Design UX/UI** | Personas, User Flows, Site Map, Wireframes, Design System | `phases/03-design/deliverables/` |
| **Design Technical** | Architecture, ERD, API Spec, ADRs | `phases/03-design/deliverables/` |
| **Development** | Código, tests, migrations, docs técnicos | `phases/04-development/deliverables/` |
| **Testing** | Test plans, results, performance reports | `phases/05-testing/deliverables/` |
| **Deploy** | Deployment plans, runbooks, monitoring | `phases/06-deploy/deliverables/` |
| **Operations** | Incident reports, post-mortems, capacity plans | `phases/07-operations/deliverables/` |

---

## Naming del archivo

```
<DELIVERABLE_ID>_<descripcion-corta>.md
```

### Ejemplos

| Deliverable | Path |
|---|---|
| Problem statement (fase Discovery, item 0.3.1) | `phases/00-discovery/deliverables/0.3.1_problem_statement.md` |
| Vision statement (fase Planning, item 1.1.1) | `phases/01-planning/deliverables/1.1.1_vision_statement.md` |
| Solution architecture (fase Design, item 3B.1.1) | `phases/03-design/deliverables/3B.1.1_solution_architecture.md` |
| API spec (Design Technical, item 3B.4.1) | `phases/03-design/deliverables/3B.4.1_api_spec.md` |

---

## Subcarpetas dentro de `deliverables/`

Agrupar por subfase **solo si hay >5 archivos** en la fase. Para evitar proliferación:

```
phases/00-discovery/deliverables/
├── problem/                              ← subfase 0.3
│   ├── 0.3.1_problem_statement.md
│   └── 0.3.2_user_pain_points.md
└── value/                                ← subfase 0.4
    ├── 0.4.1_value_proposition_canvas.md
    └── 0.4.2_uvp_statement.md
```

---

## Casos especiales (NO van en phases/)

| Tipo de archivo | Path correcto |
|---|---|
| Código fuente (TS, JS, Python, SQL) | `backend/src/`, `frontend/src/`, etc. — NO va en `phases/` |
| Tests | `backend/src/__tests__/`, `frontend/src/__tests__/` |
| Migrations de BD | `backend/prisma/migrations/` |
| Configs | `backend/.env.example`, `docker-compose.yml`, etc. (raíz del repo correspondiente) |
| BRIEFs / ASSIGNMENTs | `knowledge/agent-tasks/{briefs,assignments}/<phase>/<sprint>/` (ver `00_CONVENCIONES_FILESYSTEM`) |
| Reports / Manifests | `knowledge/agent-tasks/reports/<phase>/<sprint>/` (ver `00_CONVENCIONES_FILESYSTEM`) |
| Devlogs | `knowledge/development-log/` |
| Code Logic | `knowledge/code-logic/<modulo>/` |
| Living Documents | `knowledge/living-documents/` |

---

## Validación antes de crear

```bash
PHASE_DIR="phases/<fase>/deliverables"
DELIVERABLE_FILE="$PHASE_DIR/<DELIVERABLE_ID>_<descripcion>.md"

# 1. ¿La carpeta existe?
if [ ! -d "$PHASE_DIR" ]; then
    mkdir -p "$PHASE_DIR"
    echo "Carpeta creada: $PHASE_DIR"
fi

# 2. ¿El archivo ya existe?
if [ -f "$DELIVERABLE_FILE" ]; then
    echo "Archivo existe — ACTUALIZAR, no duplicar"
else
    echo "Crear nuevo: $DELIVERABLE_FILE"
fi

# 3. ¿El ASSIGNMENT indica una ruta diferente?
# Si dice docs/ o Release2.0/, está desactualizado.
# La ruta correcta es SIEMPRE phases/<fase>/deliverables/
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Entregable en `docs/planning/` | ASSIGNMENT desactualizado | Usar `phases/01-planning/deliverables/` igual |
| Entregable en `Release2.0/` | Convención vieja del proyecto | Migrar a `phases/<fase>/deliverables/` |
| Entregable en raíz del repo | Salto de proceso | Mover a la fase correspondiente |
| Subcarpeta innecesaria (1 archivo) | Sobre-organización | Aplanar — agrupar solo con >5 archivos |
| Subcarpeta con nombre inventado | No respeta `problem/`, `value/`, etc. | Usar nombres de subfase según `ESTRUCTURA_FASES_DESARROLLO` |
| Naming sin DELIVERABLE_ID | Sin trazabilidad al catálogo | Buscar el ID en `catalogs/deliverables/` o consultar al PJM |

---

## Skills invocadas

Ninguna — operaciones de filesystem locales.

---

## Skills que invocan ESTA

- Cualquier rol que cree un entregable de fase (DL, UX, SA, AR, etc.)
- Workflow del agente al determinar dónde guardar un nuevo archivo

---

## Cuándo NO usar esta Skill

- **Si es código fuente** — va en `src/` del repo correspondiente, no en `phases/`
- **Si es BRIEF/ASSIGNMENT/REPORT/MANIFEST** — va en `knowledge/agent-tasks/` (ver `00_CONVENCIONES_FILESYSTEM`)
- **Si es devlog o code-logic** — va en `knowledge/development-log/` o `knowledge/code-logic/`

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-STRUCTURE-01_ubicar-entregable.md` con cambio de categoría `FILE-STRUCTURE` → `FILE` (formal del registro). Cross-ref con `00_CONVENCIONES_FILESYSTEM.md` v1.0 — incluye sección "Casos especiales" que clarifica cuándo NO va en `phases/`. |
