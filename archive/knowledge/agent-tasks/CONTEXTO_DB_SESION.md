# CONTEXTO DB — Estado de Sesión Persistente

> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** 2026-05-01

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | Database Engineer |
| UUID | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| Email | `memory-service.db@vtt.ai` |
| API VTT | `http://77.42.88.106:3000` |
| Proyecto ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| Project Key | MS |
| Repo principal | `memory-service-backend` (ADR-001) |

---

## Estado del Proyecto

**Fase actual:** Project Setup (Phase 1).
**Mi trabajo arranca en:** Development Phase 7 — delivery S01 (Schema + Seeds).
**BD:** `memory_service_db` ya provisionada en `shared-postgres`.

---

## Mis Responsabilidades

- Diseñar e implementar schema Prisma (MEM-048) — bloquea todo el desarrollo backend
- Crear seeds para los 10 catálogos (MEM-049)
- Diseñar índices (normales + partial via SQL manual)
- Trabajar en repo `memory-service-backend` con mi Fine-grained PAT

---

## Tareas Asignadas a Mí

| Tarea | Título | Estado |
|-------|--------|--------|
| *(consultar VTT al iniciar sesión)* | — | — |

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&assigneeId=6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## Próximos Pasos

1. Obtener token JWT
2. Consultar mis tareas asignadas
3. Al llegar MEM-048: leer SPEC v1.9 §4 completo antes de implementar
4. Schema Prisma es la tarea más crítica del proyecto — MEM-048 bloquea S02..S06

---

## Contexto Técnico Relevante

| Recurso | Valor |
|---------|-------|
| BD | PostgreSQL `memory_service_db` |
| ORM | Prisma |
| Conexión | `shared-postgres`, `connection_limit=20` |
| Tablas principales | 19 tablas (ver SPEC v1.9 §4) |
| Catálogos | 10 tablas (seed data, cache en startup) |

### Decisiones de BD cerradas (no reabrir)

| D-MEM | Decisión |
|-------|---------|
| D-MEM-05/42 | Idempotencia: `@@unique([sourceId, externalSessionId])` |
| D-MEM-20 | Catálogos en BD, NO enums Prisma |
| D-MEM-41 | `@@unique([conversationId, turnIndex])` y `@@unique([turnId, blockIndex])` |
| D-MEM-43 | Solo `contentPreview` (500 chars) en BD — contenido completo en `/storage/` |

### Partial indexes (Prisma no los soporta — SQL manual)

```sql
-- Aplicar DESPUÉS de prisma migrate deploy
-- Ver SPEC v1.9 §6 / archivo partial_indexes.sql
```

---

## Documentos Clave

1. `knowledge/PROJECT_MEMORY.md` — modelo de datos resumen §3
2. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — §4 modelo completo, §6 índices
3. `memory-service-project/Release2.0/03-DB/DB_REVIEW_SPEC_MEMORY_SERVICE_v1.md` — review DB previo
4. `.claude/rules/PROJECT_RULES.md` — workflow obligatorio

---

## Notas de Coordinación

- MEM-048 (Schema) es el bloqueador de toda la fase Development — prioridad máxima
- Coordinar con BE el orden de campos y relaciones antes de finalizar schema
- Los 10 catálogos necesitan seed data completo (no vacíos) para que BE pueda trabajar

---

## Cómo Actualizar Este Archivo

Al terminar sesión: schema decisions, migraciones aplicadas, próxima tarea, fecha.
