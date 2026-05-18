# HANDOFF PJM: Memory Service

**Fecha:** 2026-04-15  
**De:** PM (Martin Rivas)  
**Para:** PJM  
**Proyecto:** Memory Service (independiente de VTT)

---

## 1. ESTADO ACTUAL

| Documento | Versión | Estado |
|-----------|---------|--------|
| SPEC_MEMORY_SERVICE | v1.8 | CONSOLIDADO SA — PENDIENTE CIERRE FINAL PM REVISOR |
| METODOLOGIA_MEMORY_SERVICE | v1.2 | Listo |
| ADDENDUM_INTEGRACION | v1.1 | BORRADOR — PENDIENTE CIERRE PM |

---

## 2. RESUMEN EJECUTIVO

Memory Service es un sistema independiente de memoria centralizada para agentes IA. Persiste conversaciones, clasifica por reglas, calcula costos y entrega contexto estructurado en <500ms.

| Aspecto | Valor |
|---------|-------|
| **Puerto API** | 3002 |
| **Puerto UI** | 3003 |
| **BD** | `memory_service_db` en shared-postgres |
| **Storage** | `/root/memory-service-storage/` |
| **Stack** | Node.js 20 + TypeScript + Express + Prisma + PostgreSQL |

---

## 3. PLAN DE IMPLEMENTACIÓN

### 3.1 Backend (76h)

| Sprint | Tareas | Horas | Owner |
|--------|--------|-------|-------|
| **S01** | Schema Prisma + migraciones + partial indexes + seed + setup + catalog-cache | 9h | DB + BE |
| **S02** | POST /import SDK + GET /timeline + clasificación | 12h | BE |
| **S03** | GET /content + GET /context (<500ms) + tests rendimiento | 12h | BE + QA |
| **S04** | POST /import-review + adapters Web/ChatGPT + cleanup job | 12h | BE |
| **S05** | GET /conversations + GET /cost-report + GET /dashboard + POST /upload + GET /health | 11h | BE |
| **S06** | Docker + deploy VM + integración Hook Manager + tests E2E | 14h | DevOps + BE + QA |

### 3.2 UI — Design Lead (28h)

| Sprint | Tareas | Horas |
|--------|--------|-------|
| **S-DL-01** | Design System tokens + wireframes Dashboard + Agent Timeline | 10h |
| **S-DL-02** | Wireframes Conversation Viewer (TASK + REVIEW) | 8h |
| **S-DL-03** | Wireframes Import + Cost Reports + Lista + Health | 7h |
| **S-DL-04** | UX Spec completo + handoff FE | 3h |

### 3.3 UI — Frontend (46h)

**DEPENDENCIA:** Inicia después de S-DL-04 (handoff DL).

| Sprint | Tareas | Horas |
|--------|--------|-------|
| **S-UI-01** | Setup + Agent Timeline + Conversation Viewer (TASK) | 16h |
| **S-UI-02** | Dashboard + Cost Report Proyecto + Import Manual | 12h |
| **S-UI-03** | Conversation Viewer (REVIEW) + Lista/Búsqueda | 10h |
| **S-UI-04** | Cost Report Agente + Health + estados error/empty/loading | 8h |

### 3.4 Resumen por Rol

| Rol | Horas |
|-----|-------|
| DB Engineer | 6h |
| BE Engineer | 57h |
| DevOps | 5h |
| QA | 8h |
| **Backend Total** | **76h** |
| Design Lead | 28h |
| Frontend | 46h |
| **UI Total** | **74h** |
| **PROYECTO TOTAL** | **150h** |

---

## 4. DEPENDENCIAS CRÍTICAS

```
S-DL-01 → S-DL-02 → S-DL-03 → S-DL-04 (handoff)
                                    ↓
                              S-UI-01 → S-UI-02 → S-UI-03 → S-UI-04

S01 (DB) → S02 → S03 → S04 → S05 → S06

S06 requiere integración con Hook Manager (VTT)
```

**FE no puede iniciar sin handoff de DL.**

---

## 5. INTEGRACIÓN CROSS-MODULE

Addendum v1.1 documenta alineación con:
- **Runtime v1.1:** Granularidad por ronda, `externalSessionId = {run_id}:r{N}:{agentRole}`, source `CLAUDE_SDK`
- **Prompt Builder v1.3:** Memory entrega JSON estructurado, PB transforma via adapter interno

No hay decisiones pendientes de Memory — solo cierre formal del addendum.

---

## 6. DECISIONES CERRADAS (D-MEM-01 a D-MEM-43)

43 decisiones de arquitectura cerradas incluyendo:
- Idempotencia compuesta `sourceId + externalSessionId`
- `primaryAgentRole` desnormalizado
- `contentPreview` en BD, contenido completo desde `/storage/`
- Cache de catálogos en startup
- Cleanup job por `statusId`, max 3 retries

---

## 7. INFRAESTRUCTURA PROVISIONADA

| Recurso | Estado |
|---------|--------|
| BD `memory_service_db` | ✅ Creada |
| Volumen storage | ✅ Creado |
| SERVICE_KEY | ✅ Generada |
| docker-compose.yml | ✅ Listo |
| Código | ⏳ Pendiente implementación |

---

## 8. PENDIENTES PARA CIERRE

| Item | Owner | Acción |
|------|-------|--------|
| SPEC v1.8 | PM Revisor | Cierre final |
| ADDENDUM v1.1 | PM | Cierre formal |
| Asignación recursos | PJM | Asignar DB, BE, DevOps, QA, DL, FE |
| Kick-off | PJM | Iniciar S01 (DB) y S-DL-01 (DL) en paralelo |

---

## 9. ARCHIVOS ENTREGADOS

| Archivo | Ubicación |
|---------|-----------|
| SPEC_MEMORY_SERVICE_v1.8_CONSOLIDADO.md | `/mnt/user-data/outputs/` |
| ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md | `/mnt/user-data/outputs/` |

---

**Handoff listo para PJM.**
