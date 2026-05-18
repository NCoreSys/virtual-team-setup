# CONTEXTO FE — Estado de Sesión Persistente

> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** 2026-05-01

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | Frontend Developer |
| UUID | `d23c9cd9-a156-433b-8900-94add5488eec` |
| Email | `memory-service.fe@vtt.ai` |
| API VTT | `http://77.42.88.106:3000` |
| Proyecto ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| Project Key | MS |
| Repo principal | `memory-service-frontend` (ADR-001) |

---

## Estado del Proyecto

**Fase actual:** Project Setup (Phase 1).
**Mi trabajo arranca en:** Development Phase 7 — deliveries UI-01..UI-04.
**⚠️ Bloqueado por:** MEM-038 (Design Handoff del DL) — no puedo iniciar UI sin él.

---

## Mis Responsabilidades

- Implementar UI Standalone Memory Service (React + Vite + TailwindCSS)
- Puerto: **3003**
- Timeline view, cost-report, dashboard stats, upload manual, health
- Consumir API Memory Service en puerto 3002
- Trabajar en repo `memory-service-frontend` con mi Fine-grained PAT

---

## Tareas Asignadas a Mí

| Tarea | Título | Estado |
|-------|--------|--------|
| *(consultar VTT al iniciar sesión)* | — | — |

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&assigneeId=d23c9cd9-a156-433b-8900-94add5488eec" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## Próximos Pasos

1. Esperar MEM-038 (Design Handoff del DL) — **bloquea todo UI**
2. Al recibir handoff: leer `knowledge/design-handoff/DESIGN_HANDOFF_MEM-038.md`
3. Implementar UI-01: Setup React + timeline + conversation viewer
4. Trabajar en branch `feature/[TASK_ID]` en repo `memory-service-frontend`

---

## Contexto Técnico Relevante

| Recurso | Valor |
|---------|-------|
| Stack | React + Vite + TailwindCSS |
| UI port | **3003** |
| API Memory Service | `http://[host]:3002` |
| Auth | Sin auth para UI (upload manual sin auth) |
| Endpoints que consumes | GET /conversations, GET /context, GET /agents/:id/timeline, GET /dashboard/stats, POST /upload |

### Deliveries UI

| Delivery | Tareas | Contenido |
|----------|--------|-----------|
| UI-01 | MEM-081..085 | Setup React + timeline view + conversation viewer |
| UI-02 | MEM-086..088 | Dashboard stats + cost UI + upload manual |
| UI-03 | MEM-089..090 | Lista conversaciones + detalle |
| UI-04 | MEM-091..093 | Cost breakdown agente + health |

---

## Documentos Clave

1. `knowledge/PROJECT_MEMORY.md` — stack, endpoints disponibles §4
2. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — contratos API §8
3. `knowledge/design-handoff/DESIGN_HANDOFF_MEM-038.md` — **leer antes de cualquier UI** (cuando exista)
4. `.claude/rules/PROJECT_RULES.md` — workflow obligatorio

---

## Notas de Coordinación

- **No iniciar UI sin Design Handoff (MEM-038)** — DL debe completar fases 5-6 primero
- UI-01 → UI-02 → UI-03 → UI-04 son secuenciales
- La UI es solo para operadores/agentes, no para usuarios finales

---

## Cómo Actualizar Este Archivo

Al terminar sesión: componentes implementados, decisiones de diseño, próxima tarea, fecha.
