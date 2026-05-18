# CONTEXTO SA REVIEWER — Estado de Sesión Persistente

> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** 2026-05-04

---

## 1. IDENTIDAD

| Campo | Valor |
|-------|-------|
| Agente | Solution Analyst Reviewer |
| UUID | `0c128e3b-db3b-4e31-b107-0379b5791233` |
| Email | `sa@memory-service.vtt.ai` |
| API VTT | `http://77.42.88.106:3000` |
| Proyecto ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| Project Key | MS |
| SERVICE_KEY | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |

---

## 2. ESTADO DEL PROYECTO

| Fase | Estado |
|------|--------|
| Phase 1 — Project Setup | ✅ Completada — gate MS-142 aprobado 2026-05-04 |
| Phase 2 — Discovery | 🔵 En curso — recién iniciada |
| Phase 3 — Planning | ⏳ Pendiente |
| Phase 4 — Analysis | ⏳ Pendiente |

**Release actual:** Release 2.0 (Memory Service MVP)

---

## 3. FASES BAJO MI CARGO

| Fase | Phase UUID |
|------|-----------|
| Phase 1 — Project Setup | `52c37a8b-70de-48e6-80fb-30032805025e` |
| Phase 2 — Discovery | `e081a560-bc04-46bf-a170-bfcc17d802d4` |
| Phase 3 — Planning | `6e5b6f1f-07f4-446d-9b84-1d533f6d9d90` |
| Phase 4 — Analysis | *(consultar VTT)* |

---

## 4. TAREAS EN `task_in_review` PENDIENTES DE REVISIÓN

| Tarea | Agente | Descripción | Días en review |
|-------|--------|-------------|----------------|
| *(consultar VTT al iniciar sesión)* | — | — | — |

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## 5. TAREAS EN `task_pending` SIN ASIGNAR

| Tarea | Fase | ASSIGNMENT listo |
|-------|------|-----------------|
| *(consultar VTT al iniciar sesión)* | — | — |

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_pending" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## 6. TAREAS DE DISCOVERY ACTIVAS

| Tarea | Título | Status | Asignado a |
|-------|--------|--------|------------|
| MS-006 | Problem Definition | 🟡 Pending | SA ejecutor |
| MS-007 | Problem Validation | 🔴 Bloqueado (depende de MS-006) | PM |
| MS-008 | Value Proposition | 🔴 Bloqueado (depende de MS-006) | SA ejecutor |
| MS-009 | Value Validation | 🔴 Bloqueado (depende de MS-008) | PM |

---

## 7. PROMPT DE INICIO DE SESIÓN

```
PASO 1: Obtener token JWT
TOKEN=$(curl -s -X POST "http://77.42.88.106:3000/api/auth/service-token" \
  -H "Content-Type: application/json" \
  -d '{"userId": "0c128e3b-db3b-4e31-b107-0379b5791233", "serviceKey": "hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['token'])")

PASO 2: Tareas en task_in_review (revisar primero)
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN"

PASO 3: Tareas en task_on_hold (blockers)
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_on_hold" \
  -H "Authorization: Bearer $TOKEN"

PASO 4: Tareas en task_pending (sin asignar)
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_pending" \
  -H "Authorization: Bearer $TOKEN"

PASO 5: Reportar diagnóstico al PM con formato:
## Diagnóstico Inicial — SA Reviewer Memory Service

### Tareas en task_in_review (fases 1-4): [N]
[lista]

### Tareas en task_on_hold: [N]
[lista con causa]

### Tareas pending sin asignar: [N]
[lista]

### Acciones tomadas: [lo que ya hice]
### Pendientes para el PM: [decisiones que necesito]
```

---

## 8. DOCUMENTOS CLAVE

| # | Documento | Propósito |
|---|-----------|-----------|
| 1 | `.claude/agents/OPERATIVO_SA_REVIEWER.md` | **Central** — sistema prompt, flujo completo, comandos, UUIDs |
| 2 | `knowledge/PROJECT_MEMORY.md` | Contexto del proyecto, stack, decisiones D-MEM-XX |
| 3 | `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | SPEC v1.9 — fuente de verdad |
| 4 | `memory-service-project/knowledge/kickoff/KICKOFF_MEMORY_SERVICE.md` | Alcance IN/OUT aprobado |
| 5 | `memory-service-project/00-agent-setup/03.standard/10_FLUJO_SA_REVIEWER.md` | Flujo detallado paso a paso |

---

## 9. REGLAS CRÍTICAS (recordatorio rápido)

- Revisar siempre antes que planificar
- APR-SA o REJ-SA obligatorio en cada decisión
- SPEC v1.9 manda en conflictos
- NO mover a task_approved (solo el PM)
- NO revisar las propias tareas
- NO aprobar scope creep sin escalar al PM

---

## 10. CÓMO ACTUALIZAR ESTE ARCHIVO

Al terminar sesión actualizar:
- Sección 4: tareas revisadas hoy y resultado (APR/REJ)
- Sección 5: tareas asignadas hoy
- Sección 6: cambios de estado en tareas de Discovery
- Fecha de última actualización

---

**Mantenido por:** SA Reviewer + PM
**Versión:** 2.0 | **Fecha:** 2026-05-04
