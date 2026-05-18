# ASSIGNMENT: MS-139 - README + CONTRIBUTING del repo

**Task ID**: MS-139
**Brief ref**: INIT-F-01
**Titulo**: README + CONTRIBUTING del repo memory-service-project
**Repositorio destino**: memory-service (este repo)
**Asignado a**: PM (Martin Rivas)
**Prioridad**: M (MEDIUM)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: documentation
**Generado por**: PJM
**Fecha asignacion**: 2026-05-01

---

## 1. Objetivo

Crear o actualizar el `README.md` en la raíz del repo `memory-service` con descripción del proyecto, estructura, y guía de inicio rápido. También documentar en `CONTRIBUTING.md` el proceso de contribución para agentes.

**Resultado esperado:** `README.md` y `CONTRIBUTING.md` actualizados y committeados en `main`.

---

## 2. Contexto

Todo repo necesita un README que explique qué es, cómo está organizado, y cómo empezar a trabajar con él. El `memory-service` repo es el repo de coordinación del proyecto, no el backend en sí. El README debe reflejar eso.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `.claude/rules/PROJECT_RULES.md` — estructura del proyecto y reglas
2. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — spec técnica
3. `memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md` — estrategia multi-repo
4. `README.md` actual (si existe) — para actualizar en lugar de sobrescribir

---

## 4. Prerequisitos

- [ ] Acceso al repo `memory-service`
- [ ] Token VTT válido

---

## 5. Implementación

### 5.1. `README.md` — Contenido Mínimo Requerido

```markdown
# Memory Service

Sistema de gestión de memoria contextual para agentes de IA, desarrollado como parte del ecosistema Virtual Teams.

## ¿Qué es este repo?

Este repo (`memory-service`) es el **repo de coordinación del proyecto**. Contiene:
- Documentación del proyecto
- Reglas para agentes
- Knowledge base (development logs, code logic)
- Project management (BRIEFs, ASSIGNMENTs)

El código fuente está en repos separados por rol (ver ADR-001):
| Repo | Contenido |
|------|-----------|
| `memory-service-backend` | API Node.js (BE + DB) |
| `memory-service-frontend` | UI (FE + DL) |
| `memory-service-infra` | Infraestructura (DO) |
| `memory-service-api` | Contrato OpenAPI |

## Estructura del Repo

```
memory-service/
├── .claude/
│   ├── agents/           ← OPERATIVO de cada rol
│   └── rules/            ← Reglas del proyecto (PROJECT_RULES.md)
├── docs/                 ← Docs públicos (ARCHITECTURE, INFRASTRUCTURE)
├── knowledge/            ← Docs de salida (development-log, code-logic)
│   └── agent-tasks/      ← BRIEFs, ASSIGNMENTs, CONTEXTOs por rol
├── memory-service-project/  ← Docs de gestión del proyecto
└── src/                  ← (vacío en este repo — código en repos específicos)
```

## Quick Start para Agentes

1. Leer `CONTRIBUTING.md` para entender el workflow
2. Leer tu `OPERATIVO_<ROL>.md` en `.claude/agents/`
3. Leer tu `CONTEXTO_<ROL>_SESION.md` en `knowledge/agent-tasks/`
4. Obtener token VTT: `POST http://77.42.88.106:3000/api/auth/service-token`
5. Ver tus tareas asignadas en VTT

## Stack Técnico

- **Backend**: Node.js 20 + TypeScript + Express
- **Base de datos**: PostgreSQL + Prisma
- **Cache**: Redis
- **API docs**: Swagger UI (puerto 3002/api-docs en producción)
- **Infra**: VM Ubuntu en 77.42.88.106

## Contacto

**PM**: Martin Rivas — martin.rivas@prompt-ai.studio
**VTT**: http://77.42.88.106:3000
**Swagger VTT**: http://77.42.88.106:3000/api-docs
```

### 5.2. `CONTRIBUTING.md` — Si no existe (ver MS-126)

Si MS-126 ya fue completada, `CONTRIBUTING.md` ya existe. En ese caso, solo verificar que está alineado con el README. Si no existe, crear según el ASSIGNMENT MS-126.

---

## 6. Verificación

- [ ] `README.md` en raíz del repo existe y cubre: descripción, estructura, repos separados, quick start
- [ ] `CONTRIBUTING.md` en raíz del repo existe con formato de commits
- [ ] Links en README son válidos (no referencian rutas que no existen)

---

## 7. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | `README.md` | Raíz del repo `memory-service` |
| 2 | Development Log | `knowledge/development-log/2026-05-XX_MS-139_readme-contributing.md` |
| 3 | Code Logic | No aplica (documentación, no código) |
| 4 | Commit + PR | Branch `feature/MS-139`, PR a `main` |

---

## 8. Workflow

```bash
# 1. Cambiar estado en VTT
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-139-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_progress","comment":"Actualizando README.md y CONTRIBUTING.md"}'

# 2. Crear branch
git checkout -b feature/MS-139

# 3. Crear/actualizar README.md y CONTRIBUTING.md (sección 5)

# 4. Commit
git add README.md CONTRIBUTING.md
git commit -m "docs [MS-139]: README + CONTRIBUTING del repo memory-service

- README.md: descripción, estructura, repos separados (ADR-001), quick start
- CONTRIBUTING.md: workflow git, formato de commits, Co-Authored-By obligatorio

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-139"

# 5. Push + PR
git push origin feature/MS-139
gh pr create --title "[MS-139] README + CONTRIBUTING del repo" --body "Ver devlog para detalles." --base main

# 6. Cambiar estado
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-139-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_review","comment":"README y CONTRIBUTING completos, PR creado"}'
```

---

## 9. Notas

- Si `README.md` ya existe con contenido, **actualizar** en lugar de reemplazar — mantener lo que ya estaba si es relevante
- Verificar con `git diff` antes del commit que no se perdió información existente

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-01
**Version**: 1.0
