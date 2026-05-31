# SKL-STRUCTURE-01: Ubicar entregable en estructura del proyecto

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-FILE-001_ubicar_entregable.md`** en `02.normativa/03.Skills/file/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** FILE-STRUCTURE  
**Aplica a:** SA, DL, UX, AR, TL, BE, DB, FE, QA, DO, SA Reviewer, PJM  
**Tokens estimados:** ~120  
**Cuándo:** Antes de crear cualquier entregable — determinar ruta correcta

## Regla fundamental

> Todo entregable va en `phases/{fase}/deliverables/`. NUNCA en `docs/`, `Release2.0/`, ni carpetas ad-hoc.

**Fuente de verdad:** `memory-service-project/00-platform/06.Documentos_soporte/ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md`

## Mapa fase → carpeta

| Fase del proyecto | Carpeta de entregables |
|-------------------|----------------------|
| Discovery (MS-006..009) | `phases/00-discovery/deliverables/` |
| Planning (MS-010..017) | `phases/01-planning/deliverables/` |
| Analysis (MS-018..025) | `phases/02-analysis/deliverables/` |
| Design UX/UI (MS-026..038) | `phases/03-design/deliverables/` |
| Design Technical (MS-039..047) | `phases/03-design/deliverables/` |
| Development (MS-048..093) | `phases/04-development/deliverables/` |
| Testing (MS-094..103) | `phases/05-testing/deliverables/` |
| Deploy (MS-104..110) | `phases/06-deploy/deliverables/` |
| Operations (MS-111..116) | `phases/07-operations/deliverables/` |

## Naming del archivo

```
{ID_DELIVERABLE}_{descripcion-corta}.md
```

Ejemplos:
- `0.3.1_problem_statement.md`
- `1.1.1_vision_statement.md`
- `3B.1.1_solution_architecture.md`

## Subcarpetas dentro de deliverables/ (cuando hay muchos archivos)

Agrupar por subfase solo si hay más de 5 archivos:
```
phases/00-discovery/deliverables/
├── problem/        ← subfase 0.3
│   ├── 0.3.1_problem_statement.md
│   └── 0.3.2_user_pain_points.md
└── value/          ← subfase 0.4
    ├── 0.4.1_value_proposition_canvas.md
    └── 0.4.2_uvp_statement.md
```

## Validación antes de crear

1. ¿La carpeta `phases/{fase}/deliverables/` existe? Si no, crearla.
2. ¿El ASSIGNMENT indica una ruta diferente? → La ruta correcta es SIEMPRE la de esta skill. Si el ASSIGNMENT dice `docs/`, está desactualizado — usar `phases/` igualmente.
3. ¿El archivo ya existe? → Actualizar, no duplicar.

## Error común

Crear el entregable en `docs/planning/`, `Release2.0/`, o en la raíz del repo. Esas rutas son incorrectas. La única ruta válida para entregables de fases es `phases/{fase}/deliverables/`.
