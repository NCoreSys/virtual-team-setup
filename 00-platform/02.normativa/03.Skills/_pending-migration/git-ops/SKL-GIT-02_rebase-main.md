# SKL-GIT-02: Rebase con main antes de PR

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-GIT-004_rebase_main.md`** en `02.normativa/03.Skills/git/`.
> Migración 1:1, **renumeración a GIT-003..006** (GIT-001/002 ya estaban tomados por PROTOCOL-GOV-002). Contrato sin cambios.


**Categoría:** GIT-OPS  
**Aplica a:** Todos  
**Tokens estimados:** ~65  
**Cuándo:** Antes de crear PR — obligatorio si han pasado más de 4 horas desde crear el branch

## Ejecución

```bash
git fetch origin
git rebase origin/main
# Si hay conflictos: resolverlos, luego:
git push origin feature/$TASK_ID --force-with-lease
```

## Validación

`git log --oneline -5` muestra commits de main como base

## Error común

Conflictos durante rebase → resolverlos manualmente con editor. Nunca forzar con `--force` sin `--lease`.
