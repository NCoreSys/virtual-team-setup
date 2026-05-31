# SKL-QUERY-04: Obtener avance por fases del proyecto

> 🟤 **DEPRECADA (2026-05-19) — ver `VTT.SKILL-QUERY-004_avance_fases.md`** en `02.normativa/03.Skills/query/`.
> Migración 1:1, contrato sin cambios.


**Categoría:** VTT-QUERY  
**Aplica a:** PJM, TL, PM  
**Tokens estimados:** ~60  
**Cuándo:** Reporte ejecutivo, apertura de sesión PJM

## Ejecución

```bash
curl -s "$VTT_BASE_URL/api/projects/$PROJECT_ID/phases" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Constante:** `$PROJECT_ID=d0fc276d-e764-4a83-96e9-d65f086ed803`

## Datos útiles en el response

Cada fase incluye `tasksCount` y `completedTasksCount` — calcular `%` como `completedTasksCount / tasksCount * 100`.
