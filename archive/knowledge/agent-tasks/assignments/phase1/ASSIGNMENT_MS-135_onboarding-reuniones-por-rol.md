# ASSIGNMENT: MS-135 - Reuniones de onboarding por rol

**Task ID**: MS-135
**Brief ref**: INIT-D-05
**Titulo**: Reuniones de onboarding por rol
**Repositorio destino**: memory-service (este repo)
**Asignado a**: PM (Memory Service PM)
**Prioridad**: M (MEDIUM)
**Estimacion**: 3 horas
**Complejidad**: LOW
**Categoria**: documentation
**Generado por**: PJM
**Fecha asignacion**: 2026-05-02
**Dependencias**: MS-131 (OPERATIVOS creados ✅), MS-134 (accesos distribuidos ✅)

---

## 1. Objetivo

Conducir sesiones de kick-off por cada rol activo donde se revisa: SPEC v1.9, PROJECT_RULES, OPERATIVO del rol, y se resuelven preguntas iniciales.

**Resultado esperado:** Actas de onboarding por rol en `knowledge/onboarding/` — un archivo por cada sesión realizada.

---

## 2. Contexto

Con los OPERATIVOs creados (MS-131) y los accesos distribuidos (MS-134), cada agente ya puede iniciar su trabajo. Esta tarea formaliza el onboarding documentando qué se revisó con cada rol y qué acuerdos se alcanzaron. Las actas sirven como referencia para el TL y como prueba de que el rol fue correctamente inicializado.

El PM actúa como facilitador: revisa con cada agente su OPERATIVO, responde preguntas, y registra el acta.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `.claude/agents/OPERATIVO_<ROL>.md` — uno por cada rol a onboardear
2. `.claude/rules/PROJECT_RULES.md` — reglas del proyecto
3. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — spec técnica
4. `knowledge/agent-tasks/CONTEXTO_<ROL>_SESION.md` — contexto de sesión de cada rol
5. `_pm/ACCESOS.md` — matriz de accesos (para verificar que cada rol tiene sus credenciales)

---

## 4. Roles a Onboardear

| Rol | Email VTT | UUID |
|-----|-----------|------|
| Tech Lead | memory-service.tl@vtt.ai | 92225290-6b6b-4c1f-a940-dcb4262507aa |
| Backend Engineer | memory-service.be@vtt.ai | ebbe3cee-abed-4b3b-860d-0a81f632b08a |
| Database Engineer | memory-service.db@vtt.ai | 6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7 |
| Frontend Developer | memory-service.fe@vtt.ai | d23c9cd9-a156-433b-8900-94add5488eec |
| QA Engineer | memory-service.qa@vtt.ai | 613c9538-658c-45fe-a6d7-c1ea9ff04b78 |
| DevOps Engineer | memory-service.devops@vtt.ai | 322e3745-9756-4a7c-af11-44b33edef44d |
| Design Lead | memory-service.dl@vtt.ai | b3a09269-cded-468c-a475-15a48f203cb0 |

---

## 5. Implementación — Actas a Crear

**Ruta base**: `knowledge/onboarding/`

> Si la carpeta `knowledge/onboarding/` no existe, crearla.

### Estructura de cada acta

**Nombre de archivo**: `ONBOARDING_<ROL>_2026-05-XX.md`

```markdown
# Acta de Onboarding — [ROL]

**Fecha**: 2026-05-XX
**Facilitador**: PM (Memory Service PM)
**Rol onboardeado**: [Nombre completo]
**Email VTT**: [email]
**UUID VTT**: [uuid]

---

## Documentos Revisados

- [ ] OPERATIVO_<ROL>.md — leído y confirmado por el agente
- [ ] PROJECT_RULES.md — reglas entendidas
- [ ] SPEC v1.9 §[secciones relevantes para el rol]
- [ ] CONTEXTO_<ROL>_SESION.md — estado del sprint revisado
- [ ] Accesos verificados (VTT token funcional)

---

## Resumen de la Sesión

[Qué se cubrió, qué preguntas surgieron, qué acuerdos se alcanzaron]

---

## Tareas Asignadas al Rol (Estado al momento del onboarding)

| Task ID | Título | Estado |
|---------|--------|--------|
| [ID] | [título] | pending |

---

## Acuerdos y Compromisos

- [Acuerdo 1]
- [Acuerdo 2]

---

## Blockers Detectados

[Si ninguno: "Ninguno detectado al momento del onboarding"]

---

## Próximos Pasos para el Rol

1. [Paso 1]
2. [Paso 2]

---

**Acta generada por**: PM
**Fecha**: 2026-05-XX
```

### Actas a crear (7 archivos)

| Archivo | Rol |
|---------|-----|
| `ONBOARDING_TL_2026-05-02.md` | Tech Lead |
| `ONBOARDING_BE_2026-05-02.md` | Backend Engineer |
| `ONBOARDING_DB_2026-05-02.md` | Database Engineer |
| `ONBOARDING_FE_2026-05-02.md` | Frontend Developer |
| `ONBOARDING_QA_2026-05-02.md` | QA Engineer |
| `ONBOARDING_DO_2026-05-02.md` | DevOps Engineer |
| `ONBOARDING_DL_2026-05-02.md` | Design Lead |

---

## 6. Contenido Mínimo por Rol

### Tech Lead (TL)
- Secciones SPEC relevantes: §1 Overview, §2 Architecture, §3 API Design
- Tareas asignadas: MS-138 (CI smoke — blocked esperando MS-137)
- Foco: revisar ADR-001 multi-repo, entender que el TL coordina al equipo técnico

### Backend Engineer (BE)
- Secciones SPEC relevantes: §3 API Design, §4 Endpoints, §5 Models
- Repositorio principal: `NCoreSys/memory-service-backend`
- Foco: base Node+TS ya lista (MS-136), próximos pasos según TL

### Database Engineer (DB)
- Secciones SPEC relevantes: §5 Models, §6 Database Schema
- Repositorio principal: `NCoreSys/memory-service-backend` (comparte con BE)
- Foco: schema Prisma, relaciones de datos

### Frontend Developer (FE)
- Secciones SPEC relevantes: §7 UI/UX, §8 Frontend Architecture
- Repositorio principal: `NCoreSys/memory-service-frontend`
- Foco: esperar spec de DL antes de iniciar componentes

### QA Engineer (QA)
- Secciones SPEC relevantes: §9 Testing Strategy
- Repositorio principal: `NCoreSys/memory-service` (tests E2E)
- Foco: strategy de testing, entender que QA valida entregas del equipo

### DevOps Engineer (DO)
- Secciones SPEC relevantes: §4 Deployment, §10 Infrastructure
- Repositorios: `NCoreSys/memory-service-infra`, `NCoreSys/memory-service-backend`
- Foco: MS-137 (linters) lista para iniciar, MS-145 (auto-merge workflows) pendiente

### Design Lead (DL)
- Secciones SPEC relevantes: §7 UI/UX
- Repositorio principal: `NCoreSys/memory-service-frontend`
- Foco: definir design system antes que FE empiece a codificar

---

## 7. Verificación

```bash
ls knowledge/onboarding/ONBOARDING_*.md
# → Debe listar 7 archivos
```

- [ ] `ONBOARDING_TL_2026-05-02.md`
- [ ] `ONBOARDING_BE_2026-05-02.md`
- [ ] `ONBOARDING_DB_2026-05-02.md`
- [ ] `ONBOARDING_FE_2026-05-02.md`
- [ ] `ONBOARDING_QA_2026-05-02.md`
- [ ] `ONBOARDING_DO_2026-05-02.md`
- [ ] `ONBOARDING_DL_2026-05-02.md`

---

## 8. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | 7 actas de onboarding | `knowledge/onboarding/ONBOARDING_<ROL>_2026-05-02.md` |
| 2 | Development Log | `knowledge/development-log/2026-05-XX_MS-135_onboarding-por-rol.md` |
| 3 | Code Logic | No aplica (documentación, no código) |
| 4 | Commit + PR | Branch `feature/MS-135`, PR a `main` |

---

## 9. Workflow

```bash
# 1. Cambiar estado en VTT
curl -X PATCH "http://77.42.88.106:3000/api/tasks/MS-135/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"<task_in_progress_uuid>","comment":"Iniciando onboarding de 7 roles"}'

# 2. Crear branch
git checkout -b feature/MS-135

# 3. Crear carpeta y archivos
mkdir -p knowledge/onboarding
# Crear 7 archivos ONBOARDING_*.md (sección 5)

# 4. Commit
git add knowledge/onboarding/
git commit -m "docs [MS-135]: Actas de onboarding para 7 roles

- ONBOARDING_TL, BE, DB, FE, QA, DO, DL — 2026-05-02
- Documentos revisados, tareas asignadas, proximos pasos por rol

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-135"

# 5. Push + PR
git push origin feature/MS-135
gh pr create --title "[MS-135] Actas de onboarding por rol (7 roles)" \
  --body "Ver devlog para detalles." --base main

# 6. Cambiar estado
curl -X PATCH "http://77.42.88.106:3000/api/tasks/MS-135/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"<task_in_review_uuid>","comment":"7 actas de onboarding completas, PR creado"}'
```

---

## 10. Notas

- Si un rol aún no tiene su SERVICE_KEY o no pudo autenticarse en VTT, documentarlo como blocker en el acta
- Las actas pueden generarse con información de contexto existente — no es necesaria una sesión interactiva real con el agente si este aún no está inicializado
- El CONTEXTO de sesión de cada rol (`CONTEXTO_<ROL>_SESION.md`) es la fuente principal para las "Tareas Asignadas" en el acta

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-02
**Version**: 1.0
