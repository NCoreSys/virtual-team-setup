# CONTEXTO TL — Estado de Sesión Persistente

> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** 2026-05-01

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | Tech Lead |
| UUID | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| Email | `memory-service.tl@vtt.ai` |
| API VTT | `http://77.42.88.106:3000` |
| Proyecto ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| Project Key | MS |
| Fase activa | Phase 1 — Project Setup |

---

## Estado del Proyecto

**Fase actual:** Project Setup (Phase 1) — en curso.
**Sprint activo:** Pre-Sprint (INIT-*) — tareas de inicialización.
**Release actual:** Release 2.0 (Memory Service MVP).
**Código backend:** ⏳ Pendiente — arranque en Sprint 2.

---

## Mis Responsabilidades como TL

- Revisor y aprobador de fases 7-10 (Development, Testing, Deploy, Operations)
- Crear BRIEFs y ASSIGNMENTs para agentes ejecutores
- Mover tareas a `task_completed` tras review técnico
- Escalar al PM si hay cambios de alcance

---

## Tareas en `task_in_review` Pendientes de Mi Revisión

| Tarea | Agente | Descripción | Días en review |
|-------|--------|-------------|----------------|
| *(consultar VTT al iniciar sesión)* | — | — | — |

```bash
# Consultar tareas en review
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## Tareas Asignadas a Mí (INIT-*)

| Tarea | Título | Estado |
|-------|--------|--------|
| *(consultar VTT al iniciar sesión)* | — | — |

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&assigneeId=92225290-6b6b-4c1f-a940-dcb4262507aa" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## Próximos Pasos

1. Obtener token JWT (ver OPERATIVO_TECH_LEAD §4)
2. Consultar tareas en `task_in_review` para revisar
3. Continuar asignando tareas INIT pendientes
4. Coordinar con SA cuando fases 1-4 estén completas

---

## Contexto Técnico Relevante

| Recurso | Valor |
|---------|-------|
| API Memory Service | puerto `3002` (NO 3000) |
| API VTT | puerto `3000` |
| UI Memory Service | puerto `3003` |
| Repo principal | `memory-service` |
| SPEC fuente de verdad | `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` |

---

## Documentos Clave

1. `knowledge/PROJECT_MEMORY.md` — contexto completo del proyecto
2. `.claude/agents/OPERATIVO_TECH_LEAD.md` — endpoints, comandos, proceso review
3. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — SPEC v1.9
4. `.claude/rules/PROJECT_RULES.md` — reglas operativas
5. `knowledge/agent-tasks/PLAN_116_TAREAS.md` — plan con asignaciones

---

## Notas de Coordinación

- Decisiones D-MEM-01..43 están **cerradas** — no reabrir sin justificación formal
- SA revisa fases 1-4; DL revisa fases 5-6; yo reviso fases 7-10
- Design Handoff (MEM-038) bloquea inicio de UI (MEM-081+)
- ADR-001: cada agente trabaja en su repo con su Fine-grained PAT

---

## Cómo Actualizar Este Archivo

Al terminar sesión, actualizar: tareas revisadas, decisiones tomadas, próximos pasos, fecha.
