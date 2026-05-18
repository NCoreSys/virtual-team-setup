# Guia de Contribucion -- Memory Service

## Workflow de 12 Pasos

**Paso 0** -- Crear rama
```bash
git checkout -b feature/[TASK_ID]
```

**Paso 1** -- Mover a `task_in_progress` en VTT
```bash
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/[TASK_ID]/status" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"statusId":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56","comment":"Iniciando tarea"}'
```

**Pasos 2-4** -- Leer ASSIGNMENT + referencias + verificar prerequisitos

**Paso 5** -- Implementar en `/src/...` segun ASSIGNMENT y SPEC v1.9

**Paso 6** -- Crear `.LOGIC.md` en `knowledge/code-logic/` por cada archivo

**Pasos 7-8** -- Probar localmente + escenarios del ASSIGNMENT

**Paso 9** -- Development Log en `knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[desc].md`

**Paso 10** -- Commit y push
```bash
git add <archivos>
git commit -m "tipo [TASK_ID]: Descripcion

- Cambio 1
- Cambio 2

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #[TASK_ID]"
git push origin feature/[TASK_ID]
```

**Paso 11** -- Crear PR
```bash
gh pr create --title "[[TASK_ID]] Titulo" --body "Ver devlog." --base main
```

**Paso 12** -- Mover a `task_in_review` en VTT
```bash
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/[TASK_ID]/status" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","comment":"PR creado"}'
```

---

## Formato de Commits

```
tipo [TASK_ID]: Descripcion breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #TASK_ID
```

**`Co-Authored-By` es OBLIGATORIO** en todos los commits.

| Tipo | Cuando usar |
|------|-------------|
| `feat` | Nueva funcionalidad |
| `fix` | Bug fix |
| `docs` | Solo documentacion |
| `refactor` | Refactorizacion |
| `test` | Tests |
| `chore` | Mantenimiento |

---

## Entregables por Tarea

| # | Entregable | Obligatorio |
|---|-----------|-------------|
| 1 | Codigo en `/src/...` | Si |
| 2 | Development Log en `knowledge/development-log/` | Si |
| 3 | Code Logic en `knowledge/code-logic/` (uno por archivo) | Si |
| 4 | Commit + Push + PR | Si |
| 5 | Swagger JSDoc inline | Si hay endpoints |

---

## Reglas Criticas

- **Nunca** commit directo a `main`
- **Nunca** mockear datos -- crear ISSUE y poner tarea en `task_on_hold`
- **Siempre** rebase con `origin/main` antes del PR
- **Maximo** 24h en un branch sin rebase

---

## UUIDs de Estado VTT

| Estado | UUID |
|--------|------|
| `task_in_progress` | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| `task_in_review` | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| `task_completed` | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |

Fuente completa: `.claude/rules/PROJECT_RULES.md`
