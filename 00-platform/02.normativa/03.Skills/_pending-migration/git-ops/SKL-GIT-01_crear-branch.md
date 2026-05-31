# SKL-GIT-01: Crear branch de tarea

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-GIT-003_crear_branch_tarea.md`** en `02.normativa/03.Skills/git/`.
> Migración 1:1, **renumeración a GIT-003..006** (GIT-001/002 ya estaban tomados por PROTOCOL-GOV-002). Contrato sin cambios.


**Categoría:** GIT-OPS  
**Aplica a:** BE, DB, FE, QA, DO, DL, UX, TL, AR, SA  
**Tokens estimados:** ~55  
**Cuándo:** Paso 0 del workflow — antes de cualquier modificación de código

## Precondición

Estar en `main` actualizado.

## Ejecución

```bash
git checkout main
git pull origin main
git checkout -b feature/$TASK_ID
```

## Validación

`git branch` muestra `* feature/$TASK_ID`

## Error común

Crear branch desde otro branch que no sea `main` → commits de otra tarea quedan mezclados.
