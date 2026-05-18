---
name: MS-023 User Flows Logic
description: Lógica y decisiones de diseño de los 7 documentos de User Flows de Memory Service UI R1
type: project
---

# Code Logic — MS-023: User Flows

**Tarea:** MS-023  
**Fase:** Analysis (Phase 4)  
**Tipo:** Documentación UX (no código)  
**Archivos documentados:** `phases/02-analysis/deliverables/user-flows/2.6.1..2.6.7`

---

## Propósito

Los User Flows documentan cómo los usuarios interactúan con Memory Service UI (puerto 3003). Son el puente entre el análisis (Use Cases, User Stories, Business Rules) y el diseño de pantallas (Fase 5).

---

## Estructura de los 7 documentos

| Doc | Tipo | Qué responde |
|-----|------|--------------|
| 2.6.1 | Diagramas + AMBs | ¿Cuál es el flujo general de cada pantalla? |
| 2.6.2 | Narrativa paso a paso | ¿Cómo se ve el happy path completo? |
| 2.6.3 | Mensajes de error | ¿Qué ve el usuario cuando algo falla? |
| 2.6.4 | Estados válidos inusuales | ¿Cómo manejamos casos borde sin errores técnicos? |
| 2.6.5 | Journey maps | ¿Cuál es la experiencia emocional completa de cada actor? |
| 2.6.6 | Pasos exactos por tarea | ¿Cuáles son los clics y acciones específicas de cada tarea? |
| 2.6.7 | Estructura de navegación | ¿Cómo se conectan todas las pantallas entre sí? |

---

## Decisiones de Diseño Clave

### D-UX-01: Conversation Viewer sin nav item
UF-03 es una pantalla contextual — solo se accede desde otras pantallas via click en una conversación. No tiene entrada directa en el menú de navegación.

**Por qué:** El Viewer siempre necesita un `conversationId` como contexto. No tiene sentido acceder sin ese dato.

### D-UX-02: Auto-poll cada 30s para estado PROCESSING
Cuando el upload responde PROCESSING, la UI hace polling cada 30s. Después de 6 intentos (3 min) muestra mensaje informativo.

**Por qué:** El cleanup cron corre cada 5 min (BR-006). 3 min es suficiente para el happy path (<10s). El usuario no necesita esperar indefinidamente.

### D-UX-03: ALREADY_INDEXED como azul, no rojo
La respuesta ALREADY_INDEXED se muestra como banner informativo (azul), no como error (rojo).

**Por qué:** Reimportar no es fallo del usuario — es la idempotencia funcionando (BR-001). Rojo sería confuso y generaría reportes de bug innecesarios.

### D-UX-04: Ventana temporal de 30 días para agentes activos
El dashboard muestra "Agentes activos (últimos 30 días)" con la ventana temporal visible.

**Por qué:** Coordinado con BR-015 que define 30 días fijos. El usuario debe saber qué ventana se usa para no malinterpretar el dato.

### D-UX-05: Estado global health = el peor componente
Si Redis está DOWN y BD y Storage están OK, el estado global es DOWN.

**Por qué:** Es la convención estándar de health checks. El Admin necesita saber si CUALQUIER componente falla, no el promedio.

---

## Flujo de Datos por Pantalla

| Pantalla | Endpoint | Origen de datos |
|----------|----------|-----------------|
| Dashboard | GET /dashboard/stats | BD (agregaciones) |
| Conversations List | GET /conversations | BD (metadata) |
| Conversation Viewer | GET /conversations/:id/content | /storage/ (JSONL completo) |
| Agent Timeline | GET /agents/:id/timeline | BD (metadata + ConversationParticipant) |
| Project Cost Report | GET /projects/:id/cost-report | BD (ConversationUsage agregado) |
| Agent Cost Report | GET /agents/:id/cost-report | BD (ConversationUsage por agente) |
| Manual Upload | POST /upload | Input usuario → adapter → /storage/ + BD |
| Health Status | GET /health | Estado real de BD + Storage + Redis |

---

## Pain Points R1 → Oportunidades R2

8 pain points documentados en 2.6.5 §6:
- PP-01: Sin búsqueda full-text → R2: búsqueda semántica
- PP-02: Sin batch upload → R2: upload múltiple con progress
- PP-03: JSONL grande carga lento → R2: lazy rendering de turns
- PP-04: Sin comparación temporal en cost → R2: comparación automática
- PP-08: $0.00 en fuentes sin SDK confunde → R2: separación visual

Todos los pain points R2 están fuera de scope R1 — documentados solo para roadmap.

---

## Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-05-06 | Creación — 7 documentos de user flows | UX Designer |
