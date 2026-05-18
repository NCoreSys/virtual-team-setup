# HANDOFF — Fase 0: Discovery · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_FASE_0_DISCOVERY_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PJM — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Para** | PM — `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |
| **Rol líder** | PM (Martin Rivas) |
| **Proyecto** | Memory Service |
| **Fase VTT** | Discovery (Phase order 2) |
| **Estado** | ✅ APROBADO — listo para ejecución |

---

## RESUMEN EJECUTIVO

Esta fase formaliza el **por qué** del Memory Service. Tiene 4 tareas VTT (MEM-006..009), 9h totales, y produce 10 deliverables SDLC distribuidos en 2 VTT Deliveries.

**Roles activos:** SA · PM  
**Líder de seguimiento:** PM  
**Criterio de entrada:** Gate Iniciación cerrado (MEM-005 `task_completed`)  
**Criterio de salida:** MEM-009 `task_completed` + sign-off PM de todos los 0.3.* y 0.4.*

---

## 1. ARQUITECTURA DE LA FASE

```
╔══════════════════════════════════════════════════════╗
║   GATE DE ENTRADA: MEM-005 task_completed            ║
║   (Kickoff cerrado — gate de Iniciación OK)          ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   DELIVERY 1: Problem Definition (VTT)               ║
║   ├─ MEM-006  Problem Definition      SA   3h  MED  ║
║   └─ MEM-007  Problem Validation      PM   2h  LOW  ║
║                                                      ║
║   DELIVERY 2: Value Proposition (VTT)                ║
║   ├─ MEM-008  Value Proposition       SA   3h  MED  ║
║   └─ MEM-009  Value Validation        PM   1h  LOW  ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║   GATE DE SALIDA: 4/4 tasks completed + 10 docs     ║
║   → Habilita Fase 1 Planning                         ║
╚══════════════════════════════════════════════════════╝
```

---

## 2. TAREAS VTT — MEM-006..009

### 2.1 Tabla completa

| ID | Título | Rol | Cat | Cmplx | Horas | Pri | Delivery VTT |
|----|--------|-----|-----|:-----:|------:|:---:|--------------|
| MEM-006 | Problem Definition | SA | documentation | MEDIUM | 3 | M | Problem Definition |
| MEM-007 | Problem Validation | PM | documentation | LOW | 2 | M | Problem Definition |
| MEM-008 | Value Proposition | SA | documentation | MEDIUM | 3 | M | Value Proposition |
| MEM-009 | Value Validation | PM | documentation | LOW | 1 | M | Value Proposition |

**Total fase:** 4 tareas · 9h

### 2.2 Descripciones de tareas (campo `description` en VTT)

**MEM-006 — Problem Definition**
```
Autorar 4 docs SDLC del bloque Problem: 0.3.1 Problem Statement (dolor principal
del equipo VTT sin memoria centralizada de agentes), 0.3.2 User Pain Points
(testimonios del equipo VTT), 0.3.3 Current Solutions (VTM legacy, módulo 5F —
limitaciones documentadas), 0.3.4 Why Now (urgencia + costos sin trackear).
Todos los docs en /docs/discovery/problem/.
```

**MEM-007 — Problem Validation**
```
Validación interna del Problem Statement con equipo VTT. Entregable 0.3.5
Problem Validation Report: consultas a TL, SA, DL confirmando pain points reales
y priorizados. Debe incluir firmas de validación de al menos 3 roles VTT.
Ubicación: /docs/discovery/problem/0.3.5_problem_validation.md.
```

**MEM-008 — Value Proposition**
```
Autorar 5 docs SDLC del bloque Value: 0.4.1 Value Proposition Canvas (VPC),
0.4.2 UVP Statement (1 frase), 0.4.3 Key Differentiators vs VTM legacy y
submódulo 5F, 0.4.4 Target Customer Profile (agentes AI + devs VTT),
0.4.5 Value Hypothesis. Todos en /docs/discovery/value/.
```

**MEM-009 — Value Validation**
```
Sign-off formal de todos los docs 0.4.* tras revisión con equipo VTT interno.
Confirmar UVP y diferenciadores antes de Planning. Documento de cierre:
0.4.6 Value Validation Sign-off con firma PM + SA. Sin este sign-off no
se puede iniciar Fase 1 Planning.
```

### 2.3 UUIDs para creación / actualización en VTT

| Campo | Valor |
|-------|-------|
| `assignedToId` SA | `0c128e3b-db3b-4e31-b107-0379b5791233` |
| `assignedToId` PM | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |
| `assignedBy` (PJM) | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| `createdBy` (PJM) | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| `priorityId` medium | `d0b619ef-27e7-42d8-8879-41030a602eed` |
| `priorityId` low | `95f2e731-41b9-4a7d-9a43-31f00a4ddd7e` |
| `statusId` task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |

---

## 3. DELIVERABLES SDLC PRODUCIDOS

### 3.1 Bloque Problem (Delivery VTT: "Problem Definition")

| ID | Deliverable SDLC | Responsable | Producido por |
|----|------------------|-------------|---------------|
| 0.3.1 | Problem Statement | SA | MEM-006 |
| 0.3.2 | User Pain Points | SA | MEM-006 |
| 0.3.3 | Current Solutions | SA | MEM-006 |
| 0.3.4 | Why Now | SA | MEM-006 |
| 0.3.5 | Problem Validation Report | PM | MEM-007 |

### 3.2 Bloque Value (Delivery VTT: "Value Proposition")

| ID | Deliverable SDLC | Responsable | Producido por |
|----|------------------|-------------|---------------|
| 0.4.1 | Value Proposition Canvas (VPC) | SA | MEM-008 |
| 0.4.2 | UVP Statement | SA | MEM-008 |
| 0.4.3 | Key Differentiators | SA | MEM-008 |
| 0.4.4 | Target Customer Profile | SA | MEM-008 |
| 0.4.5 | Value Hypothesis | SA | MEM-008 |
| 0.4.6 | Value Validation Sign-off | PM | MEM-009 |

**Total:** 10 deliverables SDLC en 2 VTT Deliveries

---

## 4. ESTRUCTURA DE CARPETAS ESPERADA

```
docs/
└── discovery/
    ├── problem/
    │   ├── 0.3.1_problem_statement.md
    │   ├── 0.3.2_user_pain_points.md
    │   ├── 0.3.3_current_solutions.md
    │   ├── 0.3.4_why_now.md
    │   └── 0.3.5_problem_validation.md
    └── value/
        ├── 0.4.1_value_proposition_canvas.md
        ├── 0.4.2_uvp_statement.md
        ├── 0.4.3_key_differentiators.md
        ├── 0.4.4_target_customer_profile.md
        ├── 0.4.5_value_hypothesis.md
        └── 0.4.6_value_validation_signoff.md
```

---

## 5. DEPENDENCIAS

### 5.1 Dependencia de entrada (VTT)

| Task | Depende de | Razón | Crítico |
|------|-----------|-------|:-------:|
| MEM-006 | MEM-005 | Discovery no inicia sin Kickoff completado | ✅ Sí |

### 5.2 Dependencia de salida

| Fase siguiente | Gate requerido |
|---------------|----------------|
| Fase 1 Planning (MEM-010) | MEM-009 `task_completed` + sign-off 0.4.6 |

### 5.3 Flujo dentro de la fase

```
MEM-006 (SA, 3h) ──┐
                   ├──► MEM-007 (PM, 2h) ──┐
MEM-008 (SA, 3h) ──┘                       ├──► MEM-009 (PM, 1h) → GATE SALIDA
                   └─────────────────────── ┘
```

> MEM-006 y MEM-008 pueden ejecutarse en paralelo. MEM-007 y MEM-009 son validaciones que dependen de su bloque previo.

---

## 6. INPUTS POR ROL

### SA — Solution Analyst (`0c128e3b-db3b-4e31-b107-0379b5791233`)

Antes de iniciar MEM-006, el SA debe haber leído:

| Documento | Ruta | Para qué |
|-----------|------|----------|
| SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md | `Release2.0/01-PM/` | Contexto del sistema completo |
| ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md | `Release2.0/01-PM/` | Integraciones upstream (Runtime, PromptBuilder) |
| AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md | `Release2.0/` | 7 decisiones de arquitectura aprobadas |
| TL_REVIEW_SPEC_MEMORY_SERVICE_v1.md | `Release2.0/` | Aprobación TL + resolución AMB-01 |
| KICKOFF_MEMORY_SERVICE.md | `/docs/` | Visión, objetivos, alcance (generado en MEM-005) |

### PM — Project Manager (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)

Para MEM-007 y MEM-009 (validaciones):

| Insumo | Descripción |
|--------|-------------|
| Docs 0.3.1..0.3.4 entregados por SA | Revisar y validar coherencia con visión del proyecto |
| Docs 0.4.1..0.4.5 entregados por SA | Confirmar UVP y diferenciadores con equipo VTT |
| Criterio de firma | Consultar mínimo a TL + SA + DL antes de sign-off 0.3.5 y 0.4.6 |

---

## 7. ORDEN DE EJECUCIÓN RECOMENDADO

### Semana 1 · Discovery

| Día | Tarea | Responsable | Horas | Output |
|-----|-------|-------------|------:|--------|
| Día 1 | MEM-006 Problem Definition | SA | 3h | 0.3.1, 0.3.2, 0.3.3, 0.3.4 |
| Día 1 (paralelo) | MEM-008 Value Proposition | SA | 3h | 0.4.1..0.4.5 |
| Día 2 | MEM-007 Problem Validation | PM | 2h | 0.3.5 (con firmas TL + SA + DL) |
| Día 2 (tarde) | MEM-009 Value Validation | PM | 1h | 0.4.6 sign-off |

> MEM-006 y MEM-008 pueden ejecutarse en el mismo día si el SA tiene disponibilidad. Si no, ejecutar MEM-006 primero (el bloque Problem es prerequisito conceptual del Value).

---

## 8. PROTOCOL DE ESTADO EN VTT

### Al iniciar MEM-006 (SA):

```bash
curl -X PATCH "$API_URL/api/tasks/{MEM-006-UUID}/status" \
  -H "Authorization: Bearer $SA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"task_in_progress","comment":"Iniciando Problem Definition — SA"}'
```

### Al completar cada tarea:

```bash
# SA completa MEM-006
curl -X PATCH "$API_URL/api/tasks/{MEM-006-UUID}/status" \
  -H "Authorization: Bearer $SA_TOKEN" \
  -d '{"status":"task_in_review","comment":"Problem Definition completo. Docs 0.3.1..0.3.4 en /docs/discovery/problem/"}'

# PM valida y aprueba → task_completed
curl -X PATCH "$API_URL/api/tasks/{MEM-006-UUID}/status" \
  -H "Authorization: Bearer $PM_TOKEN" \
  -d '{"status":"task_completed","comment":"Problem Definition aprobado por PM"}'
```

> Repetir el mismo patrón para MEM-007, MEM-008, MEM-009.

---

## 9. CRITERIOS DE ACEPTACIÓN

### 9.1 Por tarea

| Task | Criterio de aceptación |
|------|------------------------|
| MEM-006 | Los 4 docs (0.3.1..0.3.4) están en `/docs/discovery/problem/`, completos, en markdown, sin secciones vacías |
| MEM-007 | 0.3.5 Problem Validation incluye firmas de TL + SA + DL, y confirma que los pain points son reales y priorizados |
| MEM-008 | Los 5 docs (0.4.1..0.4.5) están en `/docs/discovery/value/`, VPC estructurado, UVP en 1 frase sin ambigüedad |
| MEM-009 | 0.4.6 Value Validation Sign-off firmado por PM + SA, declarando que la Value Proposition es válida y diferenciadora |

### 9.2 Cierre de fase

```
[ ] 4/4 tasks en estado task_completed en VTT
[ ] 10 deliverables SDLC creados (0.3.1..0.3.5 + 0.4.1..0.4.5 + 0.4.6)
[ ] Estructura /docs/discovery/ creada con subcarpetas problem/ y value/
[ ] 0.3.5 tiene firmas de validación (TL, SA, DL)
[ ] 0.4.6 tiene sign-off PM + SA
[ ] UVP Statement (0.4.2) aprobado explícitamente por PM
[ ] No hay secciones TODO ni placeholders sin completar en ningún doc
[ ] PM notifica a PJM: "Discovery cerrado — Planning habilitado"
```

---

## 10. GATE CHECKLIST — CIERRE DE DISCOVERY

Antes de emitir `HO_FASE_1_PLANNING_MEMORY_SERVICE.md`, el PM verifica:

### VTT
- [ ] MEM-006 `task_completed`
- [ ] MEM-007 `task_completed`
- [ ] MEM-008 `task_completed`
- [ ] MEM-009 `task_completed`
- [ ] VTT Delivery "Problem Definition" tiene MEM-006 + MEM-007 vinculados
- [ ] VTT Delivery "Value Proposition" tiene MEM-008 + MEM-009 vinculados

### Documentación
- [ ] 0.3.1 Problem Statement — presente y aprobado
- [ ] 0.3.2 User Pain Points — presente y aprobado
- [ ] 0.3.3 Current Solutions — presente y aprobado
- [ ] 0.3.4 Why Now — presente y aprobado
- [ ] 0.3.5 Problem Validation — firmas TL + SA + DL
- [ ] 0.4.1 Value Proposition Canvas — presente y aprobado
- [ ] 0.4.2 UVP Statement — 1 frase, aprobada por PM
- [ ] 0.4.3 Key Differentiators — vs VTM legacy + módulo 5F
- [ ] 0.4.4 Target Customer Profile — definido para agentes AI + devs VTT
- [ ] 0.4.5 Value Hypothesis — presente y aprobado
- [ ] 0.4.6 Value Validation Sign-off — firma PM + SA

### Calidad
- [ ] Ningún doc tiene secciones vacías, TODOs, o placeholders
- [ ] Los docs referencian correctamente a SPEC v1.9 donde corresponde
- [ ] Problem y Value son consistentes entre sí (el Pain Points explica por qué la Value Proposition es necesaria)

---

## 11. RIESGOS

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|:------------:|:-------:|-----------|
| R-D01 | SA no tiene acceso al repositorio al momento de iniciar | Alta | Alto | Verificar INIT-B completada antes de activar MEM-006 |
| R-D02 | Problem Validation necesita consenso de 3+ roles → demora coordinación | Media | Medio | PM agenda sesión de 30 min con TL + SA + DL en paralelo a la redacción de MEM-006 |
| R-D03 | UVP Statement iterativo: PM puede rechazar varias versiones | Media | Bajo | SA presenta borrador informal antes del entregable final |
| R-D04 | VTT no tiene los UUIDs de las tasks aún (carga pendiente) | Alta | Crítico | Este HO se activa solo tras confirmar que el script de carga en VTT fue ejecutado exitosamente (VTT_UUIDS_MEMORY_SERVICE.json disponible) |

> **R-D04 es el riesgo más crítico.** Si el PJM no ha ejecutado aún `create_memory_service_vtt.py`, los UUIDs de MEM-006..009 no existen. Este HO no es ejecutable sin VTT_UUIDS_MEMORY_SERVICE.json.

---

## 12. REFERENCIA A SIGUIENTE FASE

Al cerrar el gate de Discovery, el PM emite:

**`HO_FASE_1_PLANNING_MEMORY_SERVICE.md`**

| Campo | Valor |
|-------|-------|
| Fase | 1 · Planning |
| Líder | PM + PJM |
| Tareas VTT | MEM-010..017 (8 tareas) |
| Horas | 23h |
| Roles | PM, PJM, SA |
| Prerequisito | MEM-009 `task_completed` |

---

## 13. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PJM (emite)** | Project Manager | ✅ EMITIDO | 2026-04-22 |
| **PM (recibe y lidera)** | Martin Rivas | ✅ APROBADO | 2026-04-22 |
| **PM (reporta cierre)** | Martin Rivas | ⬜ Pendiente cierre Discovery | — |
| **PJM (sign-off post-cierre)** | Project Manager | ⬜ Pendiente | — |

---

## 14. REFERENCIAS

| Documento | Ruta | Relevancia |
|-----------|------|------------|
| TASK_INDEX_SEED_MEMORY_SERVICE.md v2.1 | `Release2.0/01-PM/` | UUIDs, campos, descripciones MEM-006..009 |
| CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md v1.0 | `Release2.0/01-PM/` | §10.1 tabla de deliverables Discovery, §16 HO sequence |
| SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md | `Release2.0/01-PM/` | Fuente de verdad del sistema |
| HO_INICIACION_MEMORY_SERVICE.md v1.0 | `Release2.0/PJM/` | Gate de entrada a esta fase |
| HO_PJM_CARGA_VTT_MEMORY_SERVICE.md v1.0 | `Release2.0/01-PM/` | Script que crea los UUIDs de MEM-006..009 en VTT |
| VTT_UUIDS_MEMORY_SERVICE.json | `Release2.0/scripts/` | UUIDs reales capturados tras carga (prerequisito) |

---

**Documento:** HO_FASE_0_DISCOVERY_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ APROBADO — Ejecutable tras cierre de Iniciación y carga VTT  
**Fecha:** 2026-04-22  

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
