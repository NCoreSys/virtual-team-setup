# ASSIGNMENT: MS-133 - CONTEXTO de sesión por rol

**Task ID**: MS-133
**Brief ref**: INIT-D-03
**Titulo**: CONTEXTO de sesión por rol
**Repositorio destino**: memory-service (este repo)
**Asignado a**: PJM (Martin Rivas)
**Prioridad**: M (MEDIUM)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: documentation
**Estado actual**: in_progress (ya iniciada)
**Generado por**: PJM
**Fecha asignacion**: 2026-05-01

---

## 1. Objetivo

Crear los 7 archivos `CONTEXTO_<ROL>_SESION.md` faltantes en `knowledge/agent-tasks/`.

**Resultado esperado:** 8 archivos CONTEXTO en `knowledge/agent-tasks/` (PM ya existe ✅).

---

## 2. Contexto

El CONTEXTO es el resumen que cada rol lee al retomar una sesión. Es diferente del OPERATIVO (que es permanente): el CONTEXTO refleja el estado actual del sprint, tareas activas, y próximos pasos para ese rol específico.

**Estado actual**: `CONTEXTO_PM_SESION.md` ya existe (1/8). Faltan 7.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `knowledge/agent-tasks/CONTEXTO_PM_SESION.md` — ejemplo del formato a seguir
2. `.claude/rules/PROJECT_RULES.md` — roles y responsabilidades
3. `.claude/rules/Proyect_data.md` — UUIDs y emails de cada rol
4. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — spec técnica

---

## 4. Prerequisitos

- [ ] Leer el CONTEXTO_PM existente para entender el formato
- [ ] Conocer el estado actual de tareas en VTT por rol

---

## 5. Archivos a Crear

**Ruta base**: `knowledge/agent-tasks/`

### Roles pendientes (7):

| Archivo | Rol | Email | UUID |
|---------|-----|-------|------|
| `CONTEXTO_TL_SESION.md` | Tech Lead | memory-service.tl@vtt.ai | 92225290-6b6b-4c1f-a940-dcb4262507aa |
| `CONTEXTO_PJM_SESION.md` | Program Manager Jr | — | — |
| `CONTEXTO_BE_SESION.md` | Backend Engineer | memory-service.be@vtt.ai | ebbe3cee-abed-4b3b-860d-0a81f632b08a |
| `CONTEXTO_FE_SESION.md` | Frontend Developer | memory-service.fe@vtt.ai | d23c9cd9-a156-433b-8900-94add5488eec |
| `CONTEXTO_DB_SESION.md` | Database Engineer | memory-service.db@vtt.ai | 6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7 |
| `CONTEXTO_DO_SESION.md` | DevOps Engineer | memory-service.devops@vtt.ai | 322e3745-9756-4a7c-af11-44b33edef44d |
| `CONTEXTO_QA_SESION.md` | QA Engineer | memory-service.qa@vtt.ai | 613c9538-658c-45fe-a6d7-c1ea9ff04b78 |

### Estructura de cada archivo (usar CONTEXTO_PM como modelo):

```markdown
# CONTEXTO DE SESIÓN — [ROL]

**Rol**: [Nombre completo del rol]
**Email VTT**: [email]
**UUID VTT**: [uuid]
**Proyecto**: Memory Service
**Última actualización**: 2026-05-01

---

## Estado Actual del Sprint

**Fase activa**: Phase 1 — Inicialización
**Sprint**: Pre-Sprint (INIT-*)

---

## Tareas Asignadas a Este Rol

[Lista de tareas en VTT asignadas a este rol, con estado actual]

---

## Próximos Pasos

[Qué debe hacer este rol al iniciar su próxima sesión]

---

## Contexto Técnico Relevante

[Solo lo que este rol necesita saber para trabajar:
- Stack relevante para su rol
- Puertos/endpoints que usa
- Repos a los que tiene acceso]

---

## Documentos Clave Para Este Rol

[Lista de 3-5 docs más importantes para el rol]

---

## Notas de Coordinación

[Dependencias con otros roles, blockers actuales]
```

---

## 6. Verificación

```bash
ls knowledge/agent-tasks/CONTEXTO_*.md
# → Debe listar 8 archivos
```

- [ ] `CONTEXTO_PM_SESION.md` ✅ (ya existe)
- [ ] `CONTEXTO_TL_SESION.md`
- [ ] `CONTEXTO_PJM_SESION.md`
- [ ] `CONTEXTO_BE_SESION.md`
- [ ] `CONTEXTO_FE_SESION.md`
- [ ] `CONTEXTO_DB_SESION.md`
- [ ] `CONTEXTO_DO_SESION.md`
- [ ] `CONTEXTO_QA_SESION.md`

---

## 7. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | 7 archivos CONTEXTO_*.md | `knowledge/agent-tasks/` |
| 2 | Development Log | `knowledge/development-log/2026-05-XX_MS-133_contexto-sesion-roles.md` |
| 3 | Code Logic | No aplica (documentación, no código) |
| 4 | Commit + PR | Branch `feature/MS-133`, PR a `main` |

---

## 8. Workflow

```bash
# 1. Cambiar estado en VTT (ya está in_progress — si no, actualizarlo)
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-133-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_progress","comment":"Creando 7 archivos CONTEXTO faltantes"}'

# 2. Branch (si no existe)
git checkout -b feature/MS-133

# 3. Crear los 7 archivos (sección 5)

# 4. Commit
git add knowledge/agent-tasks/CONTEXTO_*.md
git commit -m "docs [MS-133]: CONTEXTO de sesión para 7 roles

- CONTEXTO_TL_SESION.md
- CONTEXTO_PJM_SESION.md
- CONTEXTO_BE_SESION.md
- CONTEXTO_FE_SESION.md
- CONTEXTO_DB_SESION.md
- CONTEXTO_DO_SESION.md
- CONTEXTO_QA_SESION.md

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-133"

# 5. Push + PR
git push origin feature/MS-133
gh pr create --title "[MS-133] CONTEXTO de sesión por rol (7 roles)" --body "Ver devlog para detalles." --base main

# 6. Cambiar estado
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-133-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_review","comment":"8 archivos CONTEXTO completos, PR creado"}'
```

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-01
**Version**: 1.0
