# CONTEXTO BE — Estado de Sesión Persistente

> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** 2026-05-01

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | Backend Engineer |
| UUID | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| Email | `memory-service.be@vtt.ai` |
| API VTT | `http://77.42.88.106:3000` |
| Proyecto ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| Project Key | MS |
| Repo principal | `memory-service-backend` (ADR-001) |

---

## Estado del Proyecto

**Fase actual:** Project Setup (Phase 1) — pre-desarrollo.
**Sprint activo:** Pre-Sprint (INIT-*).
**Código backend:** ⏳ Pendiente — arranca en Sprint 2 (Development Phase 7).

---

## Mis Responsabilidades

- Implementar API Memory Service (Node.js + Express + TypeScript)
- Endpoints: import, import-review, context, timeline, cost-report, dashboard, health
- Puerto de la API: **3002**
- ORM: Prisma + PostgreSQL (`memory_service_db`)
- Trabajar en repo `memory-service-backend` con mi Fine-grained PAT

---

## Tareas Asignadas a Mí

| Tarea | Título | Estado |
|-------|--------|--------|
| *(consultar VTT al iniciar sesión)* | — | — |

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&assigneeId=ebbe3cee-abed-4b3b-860d-0a81f632b08a" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## Próximos Pasos

1. Obtener token JWT (ver OPERATIVO_BE si existe, o SKL-AUTH-01)
2. Consultar mis tareas asignadas en VTT
3. Leer ASSIGNMENT de la tarea actual antes de implementar
4. Trabajar en branch `feature/[TASK_ID]` en repo `memory-service-backend`

---

## Contexto Técnico Relevante

| Recurso | Valor |
|---------|-------|
| Stack | Node.js 20 + TypeScript + Express |
| ORM | Prisma |
| BD | PostgreSQL `memory_service_db` en `shared-postgres` |
| Cache | Redis `shared-redis` (prefix: `mem`) |
| Storage | `/root/memory-service-storage/` (bind mount) |
| API port | **3002** |
| SPEC endpoints | SPEC v1.9 §8 |
| Modelo de datos | SPEC v1.9 §4 (19 tablas + 10 catálogos) |

### Reglas críticas de implementación

- `GET /context` debe responder **<500ms** (fail-fast, no degradar)
- Idempotencia: `@@unique([sourceId, externalSessionId])` — capturar P2002 → ALREADY_INDEXED
- Catálogos en BD (no enums Prisma) — cache en startup
- Partial indexes: SQL manual en `partial_indexes.sql` (Prisma no los soporta)
- Cleanup job: cron cada 5 min, 3 retries → ERROR

---

## Documentos Clave

1. `knowledge/PROJECT_MEMORY.md` — stack, decisiones D-MEM-XX, contratos API
2. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — SPEC completa
3. `.claude/rules/PROJECT_RULES.md` — workflow y entregables obligatorios
4. `knowledge/GUIA_AGENTES_MODELO_DINAMICO_V4.md` — endpoints VTT V4

---

## Notas de Coordinación

- DB Engineer crea schema Prisma (MEM-048) — bloquea mi primer sprint de desarrollo
- Partial indexes se aplican DESPUÉS de `prisma migrate deploy`
- NO consultar VTT desde Memory Service — `agentId` viene en el import request

---

## Cómo Actualizar Este Archivo

Al terminar sesión: tareas completadas, decisiones técnicas importantes, próxima tarea, fecha.
