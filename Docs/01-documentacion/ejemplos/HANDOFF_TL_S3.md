# HANDOFF TL: Memory Service — Sprint S3

**Documento:** HANDOFF_TL_S3.md
**Versión:** 1.0
**De:** PJM-Agent
**Para:** TL (Tech Lead)
**Fecha:** 2026-05-12
**Sprint:** S3 — Features BE + FE Start
**Estado:** 📋 READY
**Prerrequisitos:** Sprint S2 completado (APR-S2 ✅)

> **Nota:** S3 es el primer sprint con FE. Incluye HANDOFF implícito para FE (§2.3). DL revisa foundation visual (DL-S3-REV). Las firmas de cierre son 3: TL + AR + DL.

---

## 0. RESUMEN EJECUTIVO

Sprint S3 tiene dos tracks paralelos:

1. **Backend — Endpoints + Integrations:** Exponer los 11 endpoints HTTP sobre los services de S2, implementar Cleanup Job, y codificar las 3 integraciones externas (Runtime v1.1, PB v1.3, Hook Manager)
2. **Frontend — Foundation:** Componentes base, layout shell, API client, hooks de data fetching, state management, types compartidos, Tailwind setup

Al terminar S3, el sistema tiene API funcional end-to-end (POST /import → GET /context → GET /conversations) y la SPA de FE con foundation desplegada (sin páginas aún — esas van en S4).

**Duración total:** ~85h (13 deliverables: 74h + TL 3h + validación/cierre 8h)
**Distribución:** BE: 42h | FE: 32h | TL: 3h | Review+Cierre: 8h
**Milestone M3:** POST /import e2e OK, JSONL procesado, estado IMPORTED en BD, FE foundation desplegada

---

## 1. ARQUITECTURA DEL SPRINT

### 1.1 Diagrama de Componentes

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    SPRINT S3: FEATURES BE + FE START                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ BE: Endpoints + Integrations + Worker (42h) → Delivery: DEL_BE_S3    │  │
│  │                                                                       │  │
│  │  4.3.1 API Endpoints (11 endpoints, 13h VERY HIGH)                   │  │
│  │  4.3.6 Cleanup Job (node-cron 5min, retry ≤3)                        │  │
│  │  4.5.1 Integration Code → 4.5.2 API Clients                          │  │
│  │                         → 4.5.3 Webhooks                              │  │
│  │  4.5.5 Third-party SDKs (ioredis, node-cron, multer)                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ FE: Foundation (32h) → Delivery: DEL_FE_S3           [PARALELO]      │  │
│  │                                                                       │  │
│  │  4.4.8 Styles (Tailwind) → 4.4.1 Components → 4.4.3 Layouts         │  │
│  │                                              → 4.4.5 State Mgmt      │  │
│  │  4.4.7 Types → 4.4.6 API Client → 4.4.4 Hooks                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  TOTAL: 13 deliverables | 4 Deliveries | 74h dev + 11h review/cierre        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 ADRs del Sprint

**ADRs nuevos:** Ninguno.

**ADRs previos relevantes:**

| ADR / Decisión | Título | Por qué aplica en S3 |
|----------------|--------|---------------------|
| D-MEM-07 | Fail-fast <500ms | 4.3.1 implementa GET /context con Promise.race |
| D-MEM-05/42 | Idempotencia P2002 | 4.3.1 POST /import maneja ALREADY_INDEXED |
| D-MEM-01 | Standalone UI | 4.4.x arranca React+Vite+Tailwind en puerto 3003 |

### 1.3 Dependencias Externas

| Servicio | Usado para | Configuración |
|----------|-----------|---------------|
| Runtime v1.1 | Consumidor de POST /import | 4.5.1 define contrato |
| Prompt Builder v1.3 | Consumidor de GET /context | 4.5.1 define contrato |
| Hook Manager VTT | Envía POST /import-review | 4.5.3 implementa webhook |
| npm: ioredis, node-cron, multer | Dependencias de 4.5.5 | package.json |

---

## 2. BRIEFS PARA AGENTES

### 2.1 Brief BE (Backend Engineer) — 42h

| Tarea | Descripción | Estimado | Depende de |
|-------|-------------|----------|-----------|
| 4.3.1 | API Endpoints — 11 endpoints con routes + controllers | 13h | 4.3.2, 4.3.7, 4.2.5 (S2) |
| 4.3.6 | Workers — Cleanup Job node-cron cada 5min | 8h | 4.3.2 (S2) |
| 4.5.1 | Integration Code — contratos con 3 sistemas externos | 8h | 4.3.2 (S2) |
| 4.5.2 | API Clients — HTTP clients para consumidores | 5h | 4.5.1 |
| 4.5.3 | Webhooks — POST /import-review para VTT_CHANNEL | 5h | 4.5.1 |
| 4.5.5 | Third-party SDKs — ioredis 5.x, node-cron, multer | 3h | SETUP |

**Archivos a crear:**
```
src/
├── routes/
│   ├── import.routes.ts          (POST /import, /import-review, /upload)
│   ├── context.routes.ts         (GET /context)
│   ├── conversations.routes.ts   (GET /conversations, /:id/content)
│   ├── agents.routes.ts          (GET /agents/:id/timeline, /cost-report)
│   ├── projects.routes.ts        (GET /projects/:id/cost-report)
│   ├── dashboard.routes.ts       (GET /dashboard/stats)
│   └── health.routes.ts          (GET /health)
├── controllers/
│   └── [uno por dominio, llama services]
├── workers/
│   └── cleanup.worker.ts         (node-cron + retry logic)
├── integrations/
│   ├── runtime.client.ts         (Runtime v1.1 POST /import consumer)
│   ├── promptBuilder.client.ts   (PB v1.3 context adapter)
│   └── hookManager.client.ts     (Hook Manager webhook)
└── app.ts                         (Express app + middleware chain + routes)
```

**Criterios de Aceptación BE:**
- [ ] CA-BE-01: Los 11 endpoints responden con status codes correctos (200, 201, 400, 401, 404, 500)
- [ ] CA-BE-02: POST /import procesa JSONL end-to-end: archivo → storage → classify → cost → persist → IMPORTED
- [ ] CA-BE-03: GET /context retorna JSON estructurado con 6 secciones del context, <500ms en dev local
- [ ] CA-BE-04: GET /conversations soporta filtros + cursor-based pagination
- [ ] CA-BE-05: Cleanup Job ejecuta cada 5min, retry ≤3, estados PENDING/PROCESSING stuck → retry → ERROR
- [ ] CA-BE-06: POST /import-review acepta formato VTT_CHANNEL con múltiples participantes
- [ ] CA-BE-07: GET /health retorna status de BD + storage + Redis
- [ ] CA-BE-08: `.LOGIC.md` para cada archivo nuevo

### 2.2 Brief FE (Frontend Developer) — 32h

| Tarea | Descripción | Estimado | Depende de |
|-------|-------------|----------|-----------|
| 4.4.7 | Types/Interfaces — @NCoreSys/api-types compartidos | 3h | SETUP |
| 4.4.8 | Styles — Tailwind CSS 3.x con design tokens | 3h | SETUP |
| 4.4.1 | Components — shared components, layout shell, nav | 8h | 4.4.8 |
| 4.4.3 | Layouts — MainLayout con sidebar + content | 3h | 4.4.1 |
| 4.4.6 | API Client FE — fetch wrapper + X-Service-Key + error handling | 5h | 4.4.7 |
| 4.4.4 | Hooks — useConversations, useContext, useCosts | 5h | 4.4.6 |
| 4.4.5 | State Management — React Context (AuthContext, FilterContext) | 5h | 4.4.1 |

**Archivos a crear:**
```
src/
├── types/
│   └── api.types.ts              (shared types con backend)
├── styles/
│   └── tailwind.config.ts        (design tokens)
├── components/
│   ├── AppShell.tsx, Sidebar.tsx, Header.tsx
│   ├── Card.tsx, Table.tsx, Badge.tsx, Button.tsx
│   └── StatusIndicator.tsx       (PENDING/PROCESSING/COMPLETED/ERROR)
├── layouts/
│   └── MainLayout.tsx
├── hooks/
│   ├── useConversations.ts
│   ├── useContext.ts
│   └── useCosts.ts
├── context/
│   ├── AuthContext.tsx
│   └── FilterContext.tsx
├── lib/
│   └── apiClient.ts              (fetch + X-Service-Key + base URL)
└── App.tsx + main.tsx
```

**Criterios de Aceptación FE:**
- [ ] CA-FE-01: `npm run dev` levanta SPA en localhost:3003 sin errores
- [ ] CA-FE-02: AppShell renderiza con sidebar + header + content area
- [ ] CA-FE-03: API Client envía X-Service-Key en cada request
- [ ] CA-FE-04: Hooks retornan `{ data, loading, error }` correctamente
- [ ] CA-FE-05: StatusIndicator renderiza 4 estados con colores del design system
- [ ] CA-FE-06: Tailwind tokens alineados con design system de fases 5-6
- [ ] CA-FE-07: `.LOGIC.md` para cada componente nuevo

---

## 3. VARIABLES DE ENTORNO

Sin variables nuevas. FE usa `VITE_API_URL` y `VITE_SERVICE_KEY` para conectar con el backend.

| Variable | Relevancia S3 |
|----------|---------------|
| `VITE_API_URL` | FE API Client se conecta al backend |
| `VITE_SERVICE_KEY` | FE envía X-Service-Key |

---

## 4. RIESGOS Y MITIGACIONES

| Riesgo | Prob. | Impacto | Mitigación |
|--------|:-----:|:-------:|------------|
| R-01: GET /context >500ms en dev local | 0.30 | HIGH | SLA check preliminar en S3. Si >400ms, alertar para S4. |
| R-02: Runtime v1.1 contrato incompleto | 0.25 | MEDIUM | Integration Code (4.5.1) documenta contrato. Mock si Runtime no disponible. |
| R-04: Hook Manager formato cambia | 0.20 | MEDIUM | 4.5.3 con mock. Integración real puede diferirse. |
| R-10: Renovate no bumps api-types | 0.20 | LOW | Bump manual si Renovate falla. |

---

## 5. TAREAS DEL SPRINT

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| 4.3.1 | API Endpoints — 11 endpoints | BE | 13h | VERY HIGH | development |
| 4.3.6 | Workers — Cleanup Job | BE | 8h | HIGH | development |
| 4.5.1 | Integration Code | BE | 8h | HIGH | development |
| 4.5.2 | API Clients | BE | 5h | MEDIUM | development |
| 4.5.3 | Webhooks | BE | 5h | MEDIUM | development |
| 4.5.5 | Third-party SDKs | BE | 3h | LOW | development |
| 4.4.1 | Components | FE | 8h | HIGH | development |
| 4.4.3 | Layouts | FE | 3h | LOW | development |
| 4.4.4 | Hooks | FE | 5h | MEDIUM | development |
| 4.4.5 | State Management | FE | 5h | MEDIUM | development |
| 4.4.6 | API Client FE | FE | 5h | MEDIUM | development |
| 4.4.7 | Types/Interfaces | FE | 3h | LOW | development |
| 4.4.8 | Styles | FE | 3h | LOW | development |
| TL-S3-REV | Reviews + SLA Check | TL | 3h | MEDIUM | review |
| AR-S3 | Integration Audit | AR | 3h | MEDIUM | review |
| DL-S3-REV | Visual Review FE Foundation | DL | 2h | LOW | review |
| CIERRE-S3 | Cierre Sprint S3 | TL | 2h | MEDIUM | review |
| APR-S3 | Aprobación PM | PM | 1h | LOW | review |

---

## 6. DEPENDENCIAS ENTRE TAREAS

| Tarea | Depende de | Tipo |
|-------|-----------|------|
| SETUP-S3 | CIERRE-S2 | FS |
| 4.3.1 | 4.3.2 (S2), 4.3.7 (S2), 4.2.5 (S2) | FS |
| 4.3.6 | 4.3.2 (S2) | FS |
| 4.5.1 | 4.3.2 (S2) | FS |
| 4.5.2 | 4.5.1 | FS |
| 4.5.3 | 4.5.1 | FS |
| 4.5.5 | SETUP-S3 | FS |
| 4.4.7 | SETUP-S3 | FS |
| 4.4.8 | SETUP-S3 | FS |
| 4.4.1 | 4.4.8 | FS |
| 4.4.3 | 4.4.1 | FS |
| 4.4.6 | 4.4.7 | FS |
| 4.4.4 | 4.4.6 | FS |
| 4.4.5 | 4.4.1 | FS |
| TL-S3-REV | 4.3.1, 4.3.6, 4.5.2, 4.5.3, 4.4.4, 4.4.5 | FS |
| DL-S3-REV | 4.4.1, 4.4.3, 4.4.8 | FS |
| AR-S3 | TL-S3-REV | FS |
| CIERRE-S3 | AR-S3, DL-S3-REV | FS |
| APR-S3 | CIERRE-S3 | FS |

---

## 7. VTT PLANNING DATA

| Tarea | estimatedHours | complexity | category | deliveryId | dependsOn |
|-------|:--------------:|:----------:|:--------:|:----------:|-----------|
| 4.3.1 | 13 | HIGH | development | DEL_BE_S3 | 4.3.2(S2), 4.3.7(S2), 4.2.5(S2) |
| 4.3.6 | 8 | HIGH | development | DEL_BE_S3 | 4.3.2(S2) |
| 4.5.1 | 8 | HIGH | development | DEL_BE_S3 | 4.3.2(S2) |
| 4.5.2 | 5 | MEDIUM | development | DEL_BE_S3 | 4.5.1 |
| 4.5.3 | 5 | MEDIUM | development | DEL_BE_S3 | 4.5.1 |
| 4.5.5 | 3 | LOW | development | DEL_BE_S3 | SETUP-S3 |
| 4.4.1 | 8 | HIGH | development | DEL_FE_S3 | 4.4.8 |
| 4.4.3 | 3 | LOW | development | DEL_FE_S3 | 4.4.1 |
| 4.4.4 | 5 | MEDIUM | development | DEL_FE_S3 | 4.4.6 |
| 4.4.5 | 5 | MEDIUM | development | DEL_FE_S3 | 4.4.1 |
| 4.4.6 | 5 | MEDIUM | development | DEL_FE_S3 | 4.4.7 |
| 4.4.7 | 3 | LOW | development | DEL_FE_S3 | SETUP-S3 |
| 4.4.8 | 3 | LOW | development | DEL_FE_S3 | SETUP-S3 |
| TL-S3 | 3 | MEDIUM | review | DEL_TL_S3 | 4.3.1,4.3.6,4.5.2,4.5.3,4.4.4,4.4.5 |
| AR-S3 | 3 | MEDIUM | review | DEL_REV_S3 | TL-S3-REV |
| DL-S3 | 2 | LOW | review | DEL_REV_S3 | 4.4.1,4.4.3,4.4.8 |
| CIERRE-S3 | 2 | MEDIUM | review | DEL_REV_S3 | AR-S3, DL-S3-REV |
| APR-S3 | 1 | LOW | review | DEL_REV_S3 | CIERRE-S3 |

**Total S3:** 85h

---

## 8. DOCUMENTOS DINÁMICOS A ACTUALIZAR

| Documento | Quién | Cuándo |
|-----------|-------|--------|
| `.LOGIC.md` por archivo | BE, FE | Al crear cada archivo |
| `API_CONTRACT.md` | BE | Al completar 4.3.1 |
| `INTEGRATION_DOCS.md` | BE | Al completar 4.5.7 (S4) — prep en S3 |

---

## 9. DoD — TL

### Coordinación:
- [ ] Tareas BE asignadas con dependencias
- [ ] Tareas FE asignadas con dependencias
- [ ] BE y FE trabajan en paralelo (repos separados)
- [ ] Briefs entregados a BE y FE

### Code Review:
- [ ] PRs BE revisados (endpoints, worker, integrations)
- [ ] PRs FE revisados (components, hooks, state)
- [ ] `.LOGIC.md` creado por archivo nuevo

### Validación:
- [ ] SLA check preliminar: GET /context <500ms en dev local
- [ ] POST /import e2e funcional
- [ ] FE SPA levanta en localhost:3003
- [ ] DL review de FE foundation coordinado
- [ ] ⚠️ **NUNCA** mover tarea a `task_approved`

### Gate M3 verificado:
- [ ] ✓ POST /import e2e OK (JSONL → IMPORTED)
- [ ] ✓ GET /context retorna JSON estructurado
- [ ] ✓ Cleanup Job ejecuta cada 5min sin error
- [ ] ✓ FE foundation desplegada (AppShell + Components + Hooks)

---

## 10. GATES DE APROBACIÓN

| Gate | Condición | Acción |
|------|-----------|--------|
| BE puede arrancar | SETUP-S3 + S2 cerrado | Desbloqueo automático |
| FE puede arrancar | SETUP-S3 + Design Handoff completado (fases 5-6) | En paralelo con BE |
| TL Review | Todos los deliverables BE + FE completados | TL-S3-REV desbloquea |
| DL Review | FE foundation (components, layouts, styles) completada | DL-S3-REV desbloquea |
| AR Audit | TL Review completado | AR-S3 desbloquea |
| Cierre | AR + DL completados | CIERRE-S3 desbloquea |
| APR PM | CIERRE completado | APR-S3 desbloquea |

---

## 11. REFERENCIAS

| Documento | Propósito |
|-----------|-----------|
| `3B.4.2_endpoints_list.md` | Contratos de 11 endpoints |
| `3B.1.6_integration_points.md` | 3 integraciones externas |
| `3B.5.1_sequence_diagrams.md` | Flujos import, context, cleanup |
| `3B.2.1_folder_structure.md` | Estructura FE |
| `CONTEXTO_S2.md` | IDs de tareas S2 para dependencias |

---

**FIN DEL HANDOFF TL S3**
