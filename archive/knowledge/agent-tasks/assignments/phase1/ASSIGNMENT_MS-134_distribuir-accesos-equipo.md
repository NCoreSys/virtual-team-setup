# ASSIGNMENT: MS-134 - Distribuir accesos al equipo

**Task ID**: MS-134
**Brief ref**: INIT-D-04
**Titulo**: Distribuir accesos al equipo
**Repositorio destino**: memory-service (este repo)
**Asignado a**: PJM (Martin Rivas)
**Prioridad**: M (MEDIUM)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: documentation
**Generado por**: PJM
**Fecha asignacion**: 2026-05-01

---

## 1. Objetivo

Verificar que cada rol activo tiene los accesos necesarios (repo Git, UUID VTT, SERVICE_KEY) y documentar la matriz de accesos.

**Resultado esperado:** Archivo `_pm/ACCESOS.md` con la matriz completa rol × recurso.

---

## 2. Contexto

Sin una matriz documentada de accesos, es imposible saber si un rol está bloqueado por falta de credenciales. Esta tarea formaliza el estado de accesos actual y crea un documento de referencia para onboarding de nuevos agentes.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `.claude/rules/Proyect_data.md` — UUIDs y emails de todos los roles (fuente de datos)
2. `memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md` — qué repo accede cada rol
3. `.claude/rules/PROJECT_RULES.md` — roles y responsabilidades

---

## 4. Prerequisitos

- [ ] Acceso al repo `memory-service`
- [ ] Token VTT válido
- [ ] Información de SERVICE_KEYs por rol (desde VTT o admin)

---

## 5. Implementación — Archivo a Crear

**Ruta**: `_pm/ACCESOS.md`

> Si la carpeta `_pm/` no existe, crearla.

### Contenido:

```markdown
# Matriz de Accesos — Memory Service

**Fecha última actualización**: 2026-05-01
**Mantenido por**: PJM (Martin Rivas)

---

## Accesos por Rol

| Rol | Email VTT | UUID VTT | Repo Principal | SERVICE_KEY | Estado |
|-----|-----------|----------|----------------|-------------|--------|
| PM (Martin Rivas) | martin.rivas@prompt-ai.studio | [UUID PM] | memory-service | [key] | ✅ activo |
| Tech Lead | memory-service.tl@vtt.ai | 92225290-6b6b-4c1f-a940-dcb4262507aa | memory-service | [key] | [verificar] |
| Backend Engineer | memory-service.be@vtt.ai | ebbe3cee-abed-4b3b-860d-0a81f632b08a | memory-service-backend | [key] | [verificar] |
| Database Engineer | memory-service.db@vtt.ai | 6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7 | memory-service-backend | [key] | [verificar] |
| Frontend Developer | memory-service.fe@vtt.ai | d23c9cd9-a156-433b-8900-94add5488eec | memory-service-frontend | [key] | [verificar] |
| QA Engineer | memory-service.qa@vtt.ai | 613c9538-658c-45fe-a6d7-c1ea9ff04b78 | memory-service | [key] | [verificar] |
| DevOps Engineer | memory-service.devops@vtt.ai | 322e3745-9756-4a7c-af11-44b33edef44d | memory-service-infra | [key] | [verificar] |
| Design Lead | memory-service.dl@vtt.ai | b3a09269-cded-468c-a475-15a48f203cb0 | memory-service-frontend | [key] | [verificar] |

---

## Repos por Rol (ADR-001)

| Repo GitHub | Rol con acceso | Propósito |
|-------------|----------------|-----------|
| `memory-service` | PM, TL, PJM, QA | Coordinación, docs, tests |
| `memory-service-backend` | BE, DB | Código backend Node.js |
| `memory-service-frontend` | FE, DL | Código frontend |
| `memory-service-infra` | DO | Infra, docker, CI/CD |
| `memory-service-api` | TL | Contrato de API (OpenAPI) |

---

## Verificación de Accesos

Para verificar que un rol tiene acceso VTT:
```bash
curl -X POST "http://77.42.88.106:3000/api/auth/service-token" \
  -H "Content-Type: application/json" \
  -d '{"serviceKey":"[SERVICE_KEY_DEL_ROL]"}'
# → Debe devolver JWT válido
```

---

## Proceso de Onboarding Nuevo Agente

1. PM crea el agente en VTT y obtiene UUID
2. Admin genera SERVICE_KEY para el agente
3. PM actualiza esta matriz
4. PM notifica al agente con: UUID, SERVICE_KEY, email VTT, repos con acceso
5. Agente verifica acceso con el comando de verificación arriba

---

## Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-05-01 | Matriz inicial creada | PJM |
```

---

## 6. Verificación

- [ ] `_pm/ACCESOS.md` existe con la matriz completa
- [ ] Todos los roles de la Fase 1 están listados
- [ ] UUIDs completos y verificados contra `Proyect_data.md`
- [ ] Repos asignados alineados con ADR-001

---

## 7. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | `_pm/ACCESOS.md` | Carpeta `_pm/` en repo `memory-service` |
| 2 | Development Log | `knowledge/development-log/2026-05-XX_MS-134_matriz-accesos.md` |
| 3 | Code Logic | No aplica (documentación, no código) |
| 4 | Commit + PR | Branch `feature/MS-134`, PR a `main` |

---

## 8. Workflow

```bash
# 1. Cambiar estado en VTT
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-134-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_progress","comment":"Creando matriz de accesos en _pm/ACCESOS.md"}'

# 2. Crear branch
git checkout -b feature/MS-134

# 3. Crear _pm/ACCESOS.md (sección 5)

# 4. Commit
git add _pm/ACCESOS.md
git commit -m "docs [MS-134]: Matriz de accesos rol x recurso en _pm/ACCESOS.md

- Roles: PM, TL, BE, DB, FE, QA, DO, DL
- Accesos: UUID VTT, email, repo GitHub, SERVICE_KEY
- Repos asignados según ADR-001
- Proceso de onboarding documentado

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-134"

# 5. Push + PR
git push origin feature/MS-134
gh pr create --title "[MS-134] Matriz de accesos al equipo" --body "Ver devlog para detalles." --base main

# 6. Cambiar estado
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-134-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_review","comment":"Matriz completa en _pm/ACCESOS.md, PR creado"}'
```

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-01
**Version**: 1.0
