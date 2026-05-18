# Índice Vivo del Proyecto — Memory Service

> Este archivo es la capa 1 de memoria del proyecto.
> Se actualiza cada vez que un documento importante se crea, modifica o aprueba.
> El INDICE_MAESTRO_DOCUMENTOS.md (raíz del repo) es la versión navegable completa.
> Este índice es el snapshot rápido para contexto de sesión.

**Última actualización:** 2026-04-27
**Versión proyecto:** R1 (Release 1)
**VTT Project ID:** d0fc276d-e764-4a83-96e9-d65f086ed803
**Project Key:** MS

---

## Estado actual del proyecto

| Hito | Estado | Fecha |
|------|--------|-------|
| SPEC v1.9 aprobada | ✅ APPROVED PM | 2026-04-23 |
| ADR-001 firmado (4 repos) | ✅ Aprobado | 2026-04-23 |
| FASES_APLICABLES (390/438) | ✅ Completo | 2026-04-23 |
| PRE_HANDOFF Iniciación (24 tareas) | ✅ Completo | 2026-04-23 |
| CONSOLIDADO master plan | ✅ Completo | 2026-04-23 |
| HO PJM firmado | ✅ Completo | 2026-04-23 |
| TASK_INDEX_SEED v2.1 (116 tareas) | ✅ Completo | 2026-04-24 |
| Script Python de carga VTT | ✅ Completo | 2026-04-24 |
| Carga en VTT ejecutada | ⏳ Pendiente PJM | - |
| Setup .vtt/ simulado | ✅ Completo | 2026-04-27 |

---

## Documentos clave — rutas rápidas

### Decisiones arquitecturales
- ADR-001 (repos): `Release2.0/01-PM/ADR-001_estrategia_repositorios.md`
- SPEC v1.9: `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`
- Estructura repos: `Release2.0/01-PM/ESTRUCTURA_REPO_MEMORY_SERVICE.md`

### Plan de proyecto
- Fases aplicables: `Release2.0/01-PM/FASES_APLICABLES_MEMORY_SERVICE.md`
- Consolidado: `Release2.0/01-PM/CONSOLIDADO_MEMORY_SERVICE_R1.md`
- TASK_INDEX_SEED: `Release2.0/01-PM/TASK_INDEX_SEED_MEMORY_SERVICE.md`

### Operativo
- Workflow multi-repo: `Release2.0/01-PM/WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md`
- Equipos por repo: `.vtt/teams.md`
- Workspaces: `Release2.0/scripts/workspaces/`

### Setup de agentes
- OPERATIVOs: `.claude/agents/`
- Reglas: `.claude/rules/PROJECT_RULES.md`
- UUIDs del proyecto: `.claude/rules/Proyect_data.md`

### Proceso y templates
- `00-agent-setup/` → estructura completa de procesos y templates estándar

---

## Repos del proyecto

| Repo | Responsabilidad | Equipo |
|------|----------------|--------|
| `memory-service-project` | Docs PM, devlogs, specs | TODOS |
| `memory-service-backend` | Node.js + Prisma + Express | Equipo BE |
| `memory-service-frontend` | React + Vite + TailwindCSS | Equipo FE |
| `memory-service-api` | Contratos TypeScript | AR + todos (read) |

---

## Decisiones críticas tomadas (no revertibles)

| ID | Decisión | Fecha |
|----|----------|-------|
| ADR-001 | 4 repos separados por rol (no monorepo) | 2026-04-23 |
| D-MEM-05 | PostgreSQL + Redis (no MongoDB) | Pre-SPEC |
| D-MEM-12 | Idempotencia por [sourceId + externalSessionId] | Pre-SPEC |
| D-INT-01 | SLA <500ms en GET /context, fail-fast | ADDENDUM v1.1 |
| D-INT-02 | platformRefs en MemoryContext | ADDENDUM v1.1 |
