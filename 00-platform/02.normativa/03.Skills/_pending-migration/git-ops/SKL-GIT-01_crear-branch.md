# SKL-GIT-01: Crear branch de tarea

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
