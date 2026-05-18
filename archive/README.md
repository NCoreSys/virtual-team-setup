# Memory Service

Sistema de gestion de memoria contextual para agentes de IA, parte del ecosistema Virtual Teams Tracking (VTT).

## Que es este repo?

Este repo (`memory-service`) es el **repo de coordinacion del proyecto**. Contiene documentacion, reglas para agentes, knowledge base y gestion de tareas.

El codigo fuente esta en repos separados por rol (ADR-001):

| Repo | Contenido | Roles |
|------|-----------|-------|
| `memory-service-backend` | API Node.js + Prisma | BE, DB |
| `memory-service-frontend` | UI React + Vite | FE, DL |
| `memory-service-infra` | Docker, CI/CD | DO |
| `memory-service-api` | Contrato OpenAPI | TL |

## Estructura del Repo

```
memory-service/
+-- .claude/
|   +-- agents/           <- OPERATIVO_[ROL].md
|   +-- rules/            <- PROJECT_RULES.md
+-- docs/                 <- Arquitectura, infraestructura
+-- knowledge/
|   +-- agent-tasks/      <- BRIEFs, ASSIGNMENTs, CONTEXTOs
|   +-- development-log/  <- Un devlog por tarea
|   +-- code-logic/       <- Documentacion logica espejo de /src
+-- memory-service-project/ <- SPEC v1.9, handoffs, ADR-001
+-- _pm/                  <- Matriz de accesos, material PM
```

## Quick Start para Agentes

1. Leer `CONTRIBUTING.md` -- workflow completo
2. Leer tu `OPERATIVO_<ROL>_MEMORY-SERVICE.md` en `.claude/agents/`
3. Leer tu `CONTEXTO_<ROL>_SESION.md` en `knowledge/agent-tasks/`
4. Obtener token VTT:
   ```bash
   curl -s -X POST "http://77.42.88.106:3000/api/auth/service-token" \\
     -H "Content-Type: application/json" \\
     -d '{"userId":"<TU_UUID>","serviceKey":"<SERVICE_KEY>"}'
   ```
5. Consultar tus tareas en VTT y comenzar

## Stack Tecnico

| Componente | Tecnologia | Puerto |
|------------|-----------|--------|
| API Memory Service | Node.js 20 + TypeScript + Express | 3002 |
| UI Standalone | React + Vite + TailwindCSS | 3003 |
| Base de datos | PostgreSQL + Prisma | -- |
| Cache | Redis | -- |
| API Docs | Swagger UI | 3002/api-docs |
| Infra | VM Ubuntu -- 77.42.88.106 | -- |

## Documentacion Clave

| Documento | Ubicacion |
|-----------|-----------|
| SPEC v1.9 | `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` |
| ADR-001 (multi-repo) | `memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md` |
| Reglas del proyecto | `.claude/rules/PROJECT_RULES.md` |
| Matriz de accesos | `_pm/ACCESOS.md` |

## Contacto

**PM**: Martin Rivas -- martin.rivas@prompt-ai.studio
**VTT API**: http://77.42.88.106:3000
**Swagger VTT**: http://77.42.88.106:3000/api-docs
