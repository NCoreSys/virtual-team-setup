# HANDOFF — Fase 3A: Design UX/UI · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_FASE_3A_DESIGN_UXUI_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PJM — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Para** | DL — `b3a09269-cded-468c-a475-15a48f203cb0` |
| **CC** | UX — `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` · PM — `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |
| **Rol líder** | DL (Design Lead) |
| **Proyecto** | Memory Service |
| **Fase VTT** | Design UX/UI (Phase order 5) |
| **Estado** | ✅ APROBADO — listo para ejecución |

---

## RESUMEN EJECUTIVO

Esta fase diseña la **interfaz visual completa** del Memory Service antes de que FE arranque. Tiene 13 tareas VTT (MEM-026..038), 35h totales, y produce los activos de diseño en 6 VTT Deliveries.

**Roles activos:** DL · UX  
**Líder de seguimiento:** DL  
**Criterio de entrada:** Gate Analysis cerrado (MEM-025 `task_completed`)  
**Criterio de salida:** MEM-038 `task_completed` (HITO CRÍTICO) + sign-off DL

> 🚨 **MEM-038 (Design Handoff Final) es un HITO CRÍTICO con prioridad CRITICAL.**  
> Su completion desbloquea MEM-081 (FE Setup) y todo el desarrollo frontend.

---

## 1. ARQUITECTURA DE LA FASE

```
╔══════════════════════════════════════════════════════════════╗
║   GATE DE ENTRADA: MEM-025 task_completed                    ║
║   (Traceability Matrix cerrada — Analysis OK)                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   DELIVERY 1: Personas (VTT)                                 ║
║   └─ MEM-026  Personas              UX   3h  MED             ║
║                                                              ║
║   DELIVERY 2: Information Architecture (VTT)                 ║
║   └─ MEM-027  Information Arch.     UX   4h  MED             ║
║                                                              ║
║   DELIVERY 3: Design System (VTT)                            ║
║   └─ MEM-028  Design System         DL   3h  MED             ║
║                                                              ║
║   DELIVERY 4: Wireframes (VTT)  [7 wireframes tasks]         ║
║   ├─ MEM-029  WF Dashboard          DL   4h  HIGH            ║
║   ├─ MEM-030  WF Timeline           DL   3h  MED             ║
║   ├─ MEM-031  WF Viewer             DL   4h  HIGH            ║
║   ├─ MEM-032  WF Cost Report        DL   4h  HIGH            ║
║   ├─ MEM-033  WF Lista Convs        DL   2h  MED             ║
║   ├─ MEM-034  WF Import Manual      DL   2h  MED             ║
║   ├─ MEM-035  WF Health             DL   2h  MED             ║
║   └─ MEM-036  WF Extras             DL   1h  LOW             ║
║                                                              ║
║   DELIVERY 5: Mockups UI Design (VTT)                        ║
║   └─ MEM-037  Design Handoff Assets DL   2h  MED             ║
║                                                              ║
║   DELIVERY 6: Design Handoff (VTT)   🚨 CRÍTICO              ║
║   └─ MEM-038  Design Handoff Final  DL   1h  CRITICAL        ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║   GATE DE SALIDA: MEM-038 CRITICAL task_completed            ║
║   → Desbloquea MEM-081 (FE Setup) — Fase Development FE     ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. DEPENDENCIAS INTERNAS

```
MEM-025 (Analysis gate)
    │
    ├──────────────────────────────────► MEM-026 (Personas)
    │                                          │
    │                                          ▼
    │                                    MEM-027 (IA)
    │                                          │
    └──────────────────────────────────► MEM-028 (Design System)
                                               │
                                    ┌──────────┴──────────┐
                        MEM-027 (IA) ────────►             │
                                    ▼                      ▼
                            MEM-029 (WF Dashboard)   MEM-030 (WF Timeline)
                            MEM-031 (WF Viewer)      MEM-032 (WF Cost)
                            MEM-033 (WF Lista)       MEM-034 (WF Import)
                            MEM-035 (WF Health)      MEM-036 (WF Extras)
                                    │
                                    ▼
                             MEM-037 (Handoff Assets)
                                    │
                                    ▼
                        🚨 MEM-038 (Design Handoff Final — CRITICAL)
                                    │
                                    ▼
                            DESBLOQUEA MEM-081 (FE)
```

**Notas de ejecución:**
- MEM-026 (Personas) y MEM-028 (Design System) pueden arrancar en paralelo
- MEM-027 (IA) depende de MEM-026 (Personas definen la arquitectura de navegación)
- Los 8 wireframes (MEM-029..036) requieren MEM-027 + MEM-028 completados
- Los wireframes pueden ejecutarse en paralelo entre sí
- MEM-037 requiere wireframes completados (exporta assets de los WF)
- MEM-038 cierra la fase y tiene prioridad CRITICAL

---

## 3. TAREAS VTT — DETALLE

### MEM-026 · Personas

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-026 |
| **Rol** | UX (`a75a1dae-754a-4b6f-a3ff-db8d51f6a91b`) |
| **Delivery** | Personas |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Crear el documento de personas del Memory Service UI:
- `3A.1.1 Personas Document` — Marco y metodología de creación de personas.
- `3A.1.2 Persona Cards (3-5)` — Fichas detalladas de cada persona con foto, bio, objetivos, frustraciones.
- `3A.1.3 Primary Persona` — TL consultando contexto de conversaciones anteriores para retomar tareas.
- `3A.1.4 Secondary Personas` — PM revisando costos de tokens por proyecto, BE importando conversaciones manualmente.
- `3A.1.5 Scenarios` — Escenarios de uso por persona: cuándo y por qué abre la UI.
- `3A.1.6 Jobs to Be Done` — Framework JTBD por persona: "cuando [situación], quiero [motivación], para [resultado esperado]".

**Entregables SDLC:** 3A.1.1 · 3A.1.2 · 3A.1.3 · 3A.1.4 · 3A.1.5 · 3A.1.6

---

### MEM-027 · Information Architecture

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-027 |
| **Rol** | UX (`a75a1dae-754a-4b6f-a3ff-db8d51f6a91b`) |
| **Delivery** | Information Architecture |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Diseñar la arquitectura de información de la UI:
- `3A.2.1 Site Map` — Mapa completo de la app: Dashboard → Timeline → Viewer → Import → Cost → Health. Estructura jerárquica.
- `3A.2.2 Navigation Patterns` — Cómo se navega entre secciones (sidebar, breadcrumbs, tabs).
- `3A.2.3 IA Patterns` — Patrones de organización del contenido: listas, filtros, drill-down.
- `3A.2.4 Content Inventory` — Inventario de todos los tipos de contenido por pantalla.
- `3A.2.5 Taxonomy` — Clasificación y etiquetado de contenidos (conversationTypes, workTypes, sources).
- `3A.2.6 Menu Structure` — Estructura del menú principal y sub-menús.
- `3A.2.7 URL Structure` — Esquema de rutas de la SPA (ej: `/timeline/:agentId`, `/conversations`, `/cost/:projectId`).

**Entregables SDLC:** 3A.2.1 · 3A.2.2 · 3A.2.3 · 3A.2.4 · 3A.2.5 · 3A.2.6 · 3A.2.7

---

### MEM-028 · Design System

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-028 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Design System |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Crear el Design System independiente para Memory Service UI:
- `3A.3.1 Design Tokens` — Tokens base independientes del VTT principal: colores, tipografía, espaciado, radios, sombras.
- `3A.3.2 Color System` — Paleta primaria, secundaria, semántica (error, warning, success, info), dark/light mode base.
- `3A.3.3 Typography` — Escala tipográfica (h1..h6, body, caption, code). Font: Inter o sistema.
- `3A.3.4 Spacing System` — Escala de espaciado base 4px (4, 8, 12, 16, 24, 32, 48, 64).
- `3A.3.5 Icons` — Set de iconos seleccionados (Lucide, Heroicons u otro). Iconos por sección de la app.
- `3A.3.6 Component Library` — Componentes base: Button, Input, Card, Table, Badge, Spinner, Modal, Tooltip, Chart.
- `3A.3.7 Component Docs` — Documentación de uso por componente: variantes, props, estados.
- `3A.3.8 Pattern Library` — Patrones UI recurrentes: empty states, error states, loading states, pagination.
- `3A.3.9 Design Assets` — Exportación de assets: SVGs, fuentes, favicon.

**Entregables SDLC:** 3A.3.1 · 3A.3.2 · 3A.3.3 · 3A.3.4 · 3A.3.5 · 3A.3.6 · 3A.3.7 · 3A.3.8 · 3A.3.9

---

### MEM-029 · Wireframes — Dashboard

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-029 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Wireframes |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | design |

**Descripción:** Wireframes de la pantalla Dashboard (3A.5.1): low-fi + mid-fi + desktop layout. Debe mostrar: totales globales (conversaciones, costo total, agentes activos), gráfico últimos 7 días, distribución por source, errores pendientes de review, acceso rápido a otras secciones.

---

### MEM-030 · Wireframes — Timeline

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-030 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Wireframes |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Wireframes del Timeline de agente (3A.5.2): vista cronológica de conversaciones de un agente específico. Debe incluir: selector de agente, filtros por fecha/tipo/proyecto, lista de conversaciones con metadata (fecha, duración, costo, workType), paginación cursor.

---

### MEM-031 · Wireframes — Viewer

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-031 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Wireframes |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | design |

**Descripción:** Wireframes del Conversation Viewer (3A.5.3): visualización del contenido de una conversación. Debe incluir: metadata de la conv (agente, tarea, proyecto, costo, source), lista de turns con mensajes expandibles, bloques de contenido (tool calls, archivos, código), navegación entre turns.

---

### MEM-032 · Wireframes — Cost Report

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-032 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Wireframes |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | design |

**Descripción:** Wireframes del Cost Report (3A.5.4): reporte de costos por proyecto o agente. Debe incluir: selector proyecto/agente, métricas totales (costo USD, tokens input/output, conversaciones), breakdown por workType, gráfico temporal por semana, tabla detalle.

---

### MEM-033 · Wireframes — Lista Conversaciones

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-033 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Wireframes |
| **Horas** | 2h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Wireframes de la Lista de Conversaciones (3A.5.5): vista global de todas las conversaciones con filtros múltiples. Filtros: agentId, projectId, taskId, conversationType, sourceCode, fechas, status. Columnas: agente, proyecto, tipo, source, fecha, costo, status.

---

### MEM-034 · Wireframes — Import Manual

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-034 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Wireframes |
| **Horas** | 2h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Wireframes del Import Manual vía UI (3A.5.6): pantalla para subir conversaciones manualmente (POST /upload). Debe incluir: drop zone para archivo JSON, campos de metadata manual (agente, proyecto, tipo), preview de validación, botón import, estados de proceso (uploading, processing, success, error).

---

### MEM-035 · Wireframes — Health

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-035 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Wireframes |
| **Horas** | 2h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Wireframes del Health Dashboard (3A.5.7): estado operativo del sistema. Debe mostrar: status general (healthy/degraded/down), checks individuales (BD, storage, Redis), versión del servicio, últimas métricas de latencia.

---

### MEM-036 · Wireframes — Extras

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-036 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Wireframes |
| **Horas** | 1h |
| **Prioridad** | MEDIUM |
| **Complejidad** | LOW |
| **Categoría** | design |

**Descripción:** Wireframes complementarios y anotaciones:
- `3A.6.1 Annotations` — Notas de comportamiento e interacción sobre los wireframes.
- `3A.6.2 Connected Flows` — Wireframes enlazados mostrando navegación completa.
- `3A.6.3 Responsive Breakpoints` — Variantes desktop (no se requiere mobile en R1).
- `3A.6.4 State Variations` — Empty states, error states, loading states, skeleton screens.

---

### MEM-037 · Design Handoff — Assets

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-037 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Design Handoff |
| **Horas** | 2h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Preparar los activos técnicos para el handoff a FE:
- `3A.9.2 Specs Export` — Medidas, espaciados y propiedades de cada componente en formato para FE.
- `3A.9.3 Asset Export` — SVGs, iconos, imágenes en resoluciones correctas.
- `3A.9.4 CSS Variables` — Variables CSS correspondientes a los Design Tokens (colores, tipografía, espaciado).

---

### MEM-038 · Design Handoff — Final 🚨 CRÍTICO

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-038 |
| **Rol** | DL (`b3a09269-cded-468c-a475-15a48f203cb0`) |
| **Delivery** | Design Handoff |
| **Horas** | 1h |
| **Prioridad** | **CRITICAL** |
| **Complejidad** | LOW |
| **Categoría** | design |

**Descripción:** Cierre formal del diseño y habilitación del desarrollo FE:
- `3A.9.1 Design Handoff Document` — Documento maestro que referencia todos los assets, specs y guidelines para FE. Incluye cómo interpretar los wireframes, qué componentes crear, convenciones de naming.
- `3A.9.5 Redlines` — Anotaciones técnicas de tamaños, márgenes, colores exactos (hex/rgb) para cada pantalla.

> **🚨 Al completar MEM-038 → notificar inmediatamente a PJM para que desbloquee MEM-081 (FE Setup).**

---

## 4. RESUMEN DE TAREAS

| VTT ID | Título | Rol | h | Cmplx | Pri | Delivery |
|--------|--------|-----|--:|-------|:---:|----------|
| MS-026 | Personas | UX | 3 | MEDIUM | M | Personas |
| MS-027 | Information Architecture | UX | 4 | MEDIUM | M | Information Architecture |
| MS-028 | Design System | DL | 3 | MEDIUM | M | Design System |
| MS-029 | Wireframes — Dashboard | DL | 4 | HIGH | M | Wireframes |
| MS-030 | Wireframes — Timeline | DL | 3 | MEDIUM | M | Wireframes |
| MS-031 | Wireframes — Viewer | DL | 4 | HIGH | M | Wireframes |
| MS-032 | Wireframes — Cost Report | DL | 4 | HIGH | M | Wireframes |
| MS-033 | Wireframes — Lista Convs | DL | 2 | MEDIUM | M | Wireframes |
| MS-034 | Wireframes — Import Manual | DL | 2 | MEDIUM | M | Wireframes |
| MS-035 | Wireframes — Health | DL | 2 | MEDIUM | M | Wireframes |
| MS-036 | Wireframes — Extras | DL | 1 | LOW | M | Wireframes |
| MS-037 | Design Handoff Assets | DL | 2 | MEDIUM | M | Design Handoff |
| **MS-038** | **Design Handoff Final** | **DL** | **1** | **LOW** | **C** | **Design Handoff** |
| **TOTAL** | | | **35h** | | | **6 Deliveries** |

---

## 5. USUARIOS VTT ACTIVOS EN ESTA FASE

| Rol | Email | UUID |
|-----|-------|------|
| DL | dl@memory-service.vtt.ai | `b3a09269-cded-468c-a475-15a48f203cb0` |
| UX | ux@memory-service.vtt.ai | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` |
| PM | pm@memory-service.vtt.ai | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |

---

## 6. GATE DE SALIDA — CRITERIOS DE COMPLETITUD

```
[ ] MEM-026 task_completed — Personas (3-5 fichas + Primary + Secondary + JTBD)
[ ] MEM-027 task_completed — Site Map 7 secciones + Navigation + URL Structure
[ ] MEM-028 task_completed — Design Tokens + Color + Typography + Component Library
[ ] MEM-029 task_completed — WF Dashboard (low-fi + mid-fi)
[ ] MEM-030 task_completed — WF Timeline
[ ] MEM-031 task_completed — WF Viewer
[ ] MEM-032 task_completed — WF Cost Report
[ ] MEM-033 task_completed — WF Lista Conversaciones
[ ] MEM-034 task_completed — WF Import Manual
[ ] MEM-035 task_completed — WF Health
[ ] MEM-036 task_completed — WF Extras (annotations + states)
[ ] MEM-037 task_completed — Specs Export + Asset Export + CSS Variables
[ ] MEM-038 task_completed (CRITICAL) — Handoff Doc + Redlines
[ ] DL sign-off en todos los 3A.* entregables
[ ] PJM notificado del cierre de MEM-038 → MEM-081 desbloqueado
```

---

## 7. RESTRICCIONES Y NOTAS CLAVE

1. **Design System independiente:** NO reutilizar estilos del VTT principal. Memory Service tiene su propio DS.
2. **7 pantallas de UI en R1:** Dashboard, Timeline, Viewer, Import Manual, Cost Report, Lista Conversaciones, Health. Ninguna más en R1.
3. **Desktop only:** No se requiere diseño responsive mobile en R1. Solo desktop (min 1280px).
4. **Wireframes, no Mockups de alta fidelidad:** R1 entrega wireframes mid-fi. Los mockups de alta fidelidad son opcionales (MEM-037 entrega assets para Handoff, no Mockups Figma terminados).
5. **MEM-038 es la puerta de FE:** Completar y hacer sign-off antes de que FE inicie cualquier tarea.

---

## 8. ESCALACIÓN

| Bloqueo | Escalar a |
|---------|-----------|
| Conflicto de scope (nueva pantalla no planificada) | PM |
| Inconsistencia IA vs User Flows (MEM-023) | UX + SA |
| Dudas sobre datos que muestra el Dashboard | BE + PM |
| Design System tokens en conflicto con VTT | PM |

---

## 9. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PJM (emite)** | PJM Agent | ✅ EMITIDO | 2026-04-22 |
| **DL (recibe y lidera)** | DL Agent | ⬜ Pendiente acuse | — |
| **PM (valida MEM-038)** | Martin Rivas | ⬜ Pendiente sign-off final | — |

---

## 10. REFERENCIAS

- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — §4.5 Design UX/UI tasks
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — §3A Design UX/UI
- `HO_FASE_2_ANALYSIS_MEMORY_SERVICE.md` — MEM-023 User Flows (input para IA + WF)
- `VTT_UUIDS_MEMORY_SERVICE.json` — UUIDs de tareas MS-026..038

---

**Documento:** HO_FASE_3A_DESIGN_UXUI_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ EMITIDO — Pendiente sign-off DL y PM  
**Fecha:** 2026-04-22  

---

**PJM — Memory Service**  
Virtual Teams Tracking
