# HANDOFF — Fase 1: Planning · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_FASE_1_PLANNING_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PJM — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Para** | PM — `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |
| **CC** | SA — `0c128e3b-db3b-4e31-b107-0379b5791233` |
| **Rol líder** | PM (Martin Rivas) |
| **Proyecto** | Memory Service |
| **Fase VTT** | Planning (Phase order 3) |
| **Estado** | ✅ APROBADO — listo para ejecución |

---

## RESUMEN EJECUTIVO

Esta fase define **el qué y el cómo** del Memory Service antes de entrar en análisis técnico. Tiene 8 tareas VTT (MEM-010..017), 23h totales, y produce 33 deliverables SDLC distribuidos en 6 VTT Deliveries.

**Roles activos:** PM · PJM · SA  
**Líder de seguimiento:** PM  
**Criterio de entrada:** Gate Discovery cerrado (MEM-009 `task_completed`)  
**Criterio de salida:** MEM-017 `task_completed` + sign-off PM en todos los 1.1.* al 1.6.*

---

## 1. ARQUITECTURA DE LA FASE

```
╔══════════════════════════════════════════════════════╗
║   GATE DE ENTRADA: MEM-009 task_completed            ║
║   (Value Validation cerrado — Discovery OK)          ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   DELIVERY 1: Vision & Objectives (VTT)              ║
║   ├─ MEM-010  Vision             PM   3h  MED        ║
║   └─ MEM-011  Objectives         PM   2h  MED        ║
║                                                      ║
║   DELIVERY 2: Scope (VTT)                            ║
║   └─ MEM-012  Scope              SA   4h  HIGH       ║
║                                                      ║
║   DELIVERY 3: Stakeholders (VTT)                     ║
║   └─ MEM-013  Stakeholders       PJM  2h  LOW        ║
║                                                      ║
║   DELIVERY 4: Risks (VTT)                            ║
║   └─ MEM-014  Risks              PJM  3h  MED        ║
║                                                      ║
║   DELIVERY 5: Timeline (VTT)                         ║
║   ├─ MEM-015  Timeline           PJM  4h  HIGH       ║
║   └─ MEM-016  Milestones         PJM  3h  MED        ║
║                                                      ║
║   DELIVERY 6: Budget & Resources (VTT)               ║
║   └─ MEM-017  Budget & Resources PM   2h  LOW        ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║   GATE DE SALIDA: 8/8 tasks completed + 33 docs      ║
║   → Habilita Fase 2 Analysis                         ║
╚══════════════════════════════════════════════════════╝
```

---

## 2. DEPENDENCIAS INTERNAS

```
MEM-009 (Discovery gate)
    │
    ▼
MEM-010 (Vision) ──────────► MEM-011 (Objectives)
                                    │
                                    ▼
                              MEM-012 (Scope)  ──────► MEM-013 (Stakeholders)
                                    │
                                    ├──────────────► MEM-014 (Risks)
                                    │
                                    └──────────────► MEM-015 (Timeline) ──► MEM-016 (Milestones)
                                                                                    │
                                                                                    ▼
                                                                              MEM-017 (Budget)
```

**Notas de ejecución:**
- MEM-010 y MEM-011 se pueden trabajar en paralelo una vez disponible Vision borrador
- MEM-012 depende de MEM-011 (Objectives define el alcance)
- MEM-013, MEM-014 y MEM-015 pueden arrancar en paralelo después de MEM-012
- MEM-016 depende de MEM-015 (requiere Schedule como base)
- MEM-017 depende de MEM-016 (requiere Milestones + Sprint Calendar para calcular recursos)

---

## 3. TAREAS VTT — DETALLE

### MEM-010 · Vision

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-010 |
| **Rol** | PM (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`) |
| **Delivery** | Vision & Objectives |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Autorar 3 documentos de visión estratégica del producto:
- `1.1.1 Vision Statement` — Hacia dónde va Memory Service en 1-3 años. Una frase inspiracional + párrafo de contexto.
- `1.1.2 Mission Statement` — Para qué existe ahora mismo: "persistir y recuperar memoria de agentes AI en < 500ms".
- `1.1.5 North Star Metric` — Métrica única de éxito del producto (p.ej. "latencia p95 contexto < 500ms con 100k conversaciones activas").

**Entregables SDLC:** 1.1.1 · 1.1.2 · 1.1.5

---

### MEM-011 · Objectives

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-011 |
| **Rol** | PM (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`) |
| **Delivery** | Vision & Objectives |
| **Horas** | 2h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Autorar los objetivos medibles del proyecto:
- `1.1.3 Product Goals SMART` — 4-6 objetivos específicos, medibles, alcanzables, relevantes, temporales.
- `1.1.4 Success Metrics KPIs` — Incluye obligatoriamente `<500ms` p95, tasa de importación exitosa, uptime.
- `1.1.6 OKRs de feature` — Objectives & Key Results del R1: qué se quiere lograr y cómo se mide.

**Entregables SDLC:** 1.1.3 · 1.1.4 · 1.1.6

---

### MEM-012 · Scope

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-012 |
| **Rol** | SA (`0c128e3b-db3b-4e31-b107-0379b5791233`) |
| **Delivery** | Scope |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el documento de alcance completo del proyecto:
- `1.2.1 Scope Statement` — Definición formal del alcance de Memory Service.
- `1.2.2 In-Scope` — Lista explícita de lo que incluye R1: 11 endpoints, 19 tablas, 5 adapters, UI 7 pantallas.
- `1.2.3 Out-of-Scope` — Lo que explícitamente NO se hace en R1 (multitenancy, billing externo, LLM nativo).
- `1.2.4 MVP Definition` — Subconjunto mínimo viable entregable.
- `1.2.5 Future Phases` — Roadmap R2+: features diferidas, integraciones previstas.
- `1.2.6 Assumptions` — Supuestos de negocio y técnicos (servidor Hetzner disponible, VTT no-SaaS, etc.).

**Entregables SDLC:** 1.2.1 · 1.2.2 · 1.2.3 · 1.2.4 · 1.2.5 · 1.2.6

---

### MEM-013 · Stakeholders

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-013 |
| **Rol** | PJM (`0ff63a29-0bc0-465a-b9bd-5f71476bc91d`) |
| **Delivery** | Stakeholders |
| **Horas** | 2h |
| **Prioridad** | MEDIUM |
| **Complejidad** | LOW |
| **Categoría** | documentation |

**Descripción:** Autorar la gestión completa de interesados del proyecto:
- `1.3.1 Stakeholder Map` — Mapa visual de stakeholders por influencia/interés.
- `1.3.2 Stakeholder Register` — Registro con datos de contacto, rol, expectativas de cada stakeholder.
- `1.3.3 RACI Matrix` — Responsible, Accountable, Consulted, Informed por entregable / decisión clave.
- `1.3.4 Communication Plan` — Cadencia de updates por stakeholder (diario, semanal, por hito).

**Entregables SDLC:** 1.3.1 · 1.3.2 · 1.3.3 · 1.3.4

---

### MEM-014 · Risks

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-014 |
| **Rol** | PJM (`0ff63a29-0bc0-465a-b9bd-5f71476bc91d`) |
| **Delivery** | Risks |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Autorar el plan de gestión de riesgos del proyecto:
- `1.4.1 Risk Register` — Inventario de todos los riesgos identificados con ID, categoría, descripción.
- `1.4.2 Risk Assessment` — Probabilidad × Impacto para cada riesgo. Matriz de criticidad.
- `1.4.3 Mitigation Plan` — Acciones preventivas por riesgo crítico y alto.
- `1.4.4 Contingency Plan` — Qué se hace si el riesgo se materializa.
- `1.4.5 Risk Monitoring` — Cómo y cuándo se revisan los riesgos durante el proyecto.

**Riesgos clave a cubrir:** latencia >500ms en contexto, complejidad integración Hook Manager, single server (no HA), scope creep R1.

**Entregables SDLC:** 1.4.1 · 1.4.2 · 1.4.3 · 1.4.4 · 1.4.5

---

### MEM-015 · Timeline

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-015 |
| **Rol** | PJM (`0ff63a29-0bc0-465a-b9bd-5f71476bc91d`) |
| **Delivery** | Timeline |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el cronograma maestro del proyecto:
- `1.5.1 Project Schedule` — Gantt por fase con fechas de inicio/fin estimadas.
- `1.5.5 Dependencies Map` — Las 15 dependencias críticas del proyecto + 63 intra-fase registradas en VTT.
- `1.5.6 Critical Path` — Identificar el camino crítico. Referencia clave: MEM-038 (Design Handoff Final) → MEM-081 (FE Setup).
- `1.5.7 Buffer Plan` — Reservas de tiempo por fase para imprevistos.

**Entregables SDLC:** 1.5.1 · 1.5.5 · 1.5.6 · 1.5.7

---

### MEM-016 · Milestones

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-016 |
| **Rol** | PJM (`0ff63a29-0bc0-465a-b9bd-5f71476bc91d`) |
| **Delivery** | Timeline |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Autorar la descomposición de hitos y sprints:
- `1.5.2 Milestone Plan` — Hitos clave del proyecto con criterios de completitud (ej: "Design Handoff Final aprobado", "GET /context < 500ms verificado").
- `1.5.3 Phase Breakdown` — Desglose de esfuerzo y duración por fase (Project Setup 32h, Discovery 9h, Planning 23h, etc.).
- `1.5.4 Sprint Calendar` — Distribución de tareas en sprints. Referencia: S01..S06 (backend) + UI-01..04 (frontend).

**Entregables SDLC:** 1.5.2 · 1.5.3 · 1.5.4

---

### MEM-017 · Budget & Resources

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-017 |
| **Rol** | PM (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`) |
| **Delivery** | Budget & Resources |
| **Horas** | 2h |
| **Prioridad** | MEDIUM |
| **Complejidad** | LOW |
| **Categoría** | documentation |

**Descripción:** Autorar el plan financiero y de recursos del proyecto:
- `1.6.1 Budget Estimate` — Estimación total de esfuerzo: 381h totales distribuidas por fase y rol.
- `1.6.2 Cost Breakdown` — Desglose por rol (PM, PJM, TL, SA, AR, BE, DB, FE, UX, DL, QA, DO).
- `1.6.3 Resource Plan` — Disponibilidad y carga por agente durante el proyecto.
- `1.6.4 ROI Analysis` — Retorno sobre inversión: qué valor entrega el Memory Service al ecosistema VTT.
- `1.6.5 Budget Tracking` — Plantilla para seguimiento de horas consumidas vs. estimadas por sprint.

**Entregables SDLC:** 1.6.1 · 1.6.2 · 1.6.3 · 1.6.4 · 1.6.5

---

## 4. RESUMEN DE TAREAS

| VTT ID | Título | Rol | h | Cmplx | Pri | Delivery |
|--------|--------|-----|--:|-------|:---:|----------|
| MS-010 | Vision | PM | 3 | MEDIUM | M | Vision & Objectives |
| MS-011 | Objectives | PM | 2 | MEDIUM | M | Vision & Objectives |
| MS-012 | Scope | SA | 4 | HIGH | M | Scope |
| MS-013 | Stakeholders | PJM | 2 | LOW | M | Stakeholders |
| MS-014 | Risks | PJM | 3 | MEDIUM | M | Risks |
| MS-015 | Timeline | PJM | 4 | HIGH | M | Timeline |
| MS-016 | Milestones | PJM | 3 | MEDIUM | M | Timeline |
| MS-017 | Budget & Resources | PM | 2 | LOW | M | Budget & Resources |
| **TOTAL** | | | **23h** | | | **6 Deliveries** |

---

## 5. DELIVERABLES SDLC PRODUCIDOS

| VTT Delivery | Docs SDLC | Tareas |
|-------------|-----------|--------|
| Vision & Objectives | 1.1.1, 1.1.2, 1.1.3, 1.1.4, 1.1.5, 1.1.6 | MEM-010, MEM-011 |
| Scope | 1.2.1, 1.2.2, 1.2.3, 1.2.4, 1.2.5, 1.2.6 | MEM-012 |
| Stakeholders | 1.3.1, 1.3.2, 1.3.3, 1.3.4 | MEM-013 |
| Risks | 1.4.1, 1.4.2, 1.4.3, 1.4.4, 1.4.5 | MEM-014 |
| Timeline | 1.5.1, 1.5.2, 1.5.3, 1.5.4, 1.5.5, 1.5.6, 1.5.7 | MEM-015, MEM-016 |
| Budget & Resources | 1.6.1, 1.6.2, 1.6.3, 1.6.4, 1.6.5 | MEM-017 |

**Total SDLC:** 33 documentos en 6 VTT Deliveries

---

## 6. USUARIOS VTT ACTIVOS EN ESTA FASE

| Rol | Email | UUID |
|-----|-------|------|
| PM | pm@memory-service.vtt.ai | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |
| PJM | pjm@memory-service.vtt.ai | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| SA | sa@memory-service.vtt.ai | `0c128e3b-db3b-4e31-b107-0379b5791233` |

---

## 7. GATE DE SALIDA — CRITERIOS DE COMPLETITUD

La fase Planning se considera **COMPLETADA** cuando:

```
[ ] MEM-010 task_completed — Vision Statement + Mission + North Star
[ ] MEM-011 task_completed — Goals SMART + KPIs + OKRs
[ ] MEM-012 task_completed — Scope Statement + In/Out + MVP + Assumptions
[ ] MEM-013 task_completed — Stakeholder Map + Register + RACI + Comm Plan
[ ] MEM-014 task_completed — Risk Register + Assessment + Mitigation
[ ] MEM-015 task_completed — Project Schedule + Critical Path (MEM-038→MEM-081) + Buffer
[ ] MEM-016 task_completed — Milestones + Phase Breakdown + Sprint Calendar
[ ] MEM-017 task_completed — Budget 381h + Cost Breakdown + Resource Plan + ROI
[ ] PM sign-off en todos los 1.1.* al 1.6.* (33 docs)
[ ] MEM-018 desbloqueado en VTT (Fase 2 Analysis arranca)
```

---

## 8. RESTRICCIONES Y NOTAS CLAVE

1. **Scope conservador:** R1 incluye exactamente 11 endpoints, 19 tablas, 5 adapters, 7 pantallas UI. El SA debe resistir scope creep al redactar 1.2.2/1.2.3.
2. **Critical path explícito:** MEM-038 (Design Handoff Final) bloquea el arranque de FE (MEM-081). El Timeline debe documentar este gate en 1.5.6.
3. **381h de esfuerzo total:** Esta es la cifra maestra del Budget. Desglose por fase: Setup 32h + Discovery 9h + Planning 23h + Analysis 41h + Design UX 35h + Design Tech 45h + Development 116h + Testing 60h + Deploy 26h + Operations 15h = **402h** (incluye overlap de fases concurrentes).
4. **Servidor único Hetzner:** No hay HA en R1. El Risk Register debe capturar este single point of failure y su plan de contingencia.
5. **PJM como redactor principal de Timeline + Milestones + Stakeholders + Risks** — PM valida y hace sign-off, no redacta.

---

## 9. ESCALACIÓN

| Bloqueo | Escalar a |
|---------|-----------|
| Conflicto Scope In/Out (qué entra en R1) | PM (Martin Rivas) |
| Dudas sobre Critical Path técnico | TL |
| Riesgos de integración Hook Manager | TL + BE |
| Indefinición de Budget/ROI | PM |

---

## 10. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PJM (emite)** | PJM Agent | ✅ EMITIDO | 2026-04-22 |
| **PM (recibe y valida)** | Martin Rivas | ⬜ Pendiente sign-off | — |
| **SA (recibe)** | SA Agent | ⬜ Pendiente acuse | — |

---

## 11. REFERENCIAS

- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — §4.3 Planning tasks
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — §1 Vision & Planning
- `CONSOLIDADO_MEMORY_SERVICE_R1.md` — Plan maestro
- `VTT_UUIDS_MEMORY_SERVICE.json` — UUIDs de tareas MS-010..017
- `HO_FASE_0_DISCOVERY_MEMORY_SERVICE.md` — Gate previo

---

**Documento:** HO_FASE_1_PLANNING_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ EMITIDO — Pendiente sign-off PM  
**Fecha:** 2026-04-22  

---

**PJM — Memory Service**  
Virtual Teams Tracking
