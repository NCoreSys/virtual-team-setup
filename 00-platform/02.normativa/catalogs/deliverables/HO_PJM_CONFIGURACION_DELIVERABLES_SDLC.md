# HANDOFF — PJM: Catálogo SDLC para Configuración de Deliverables

| Campo | Valor |
|-------|-------|
| **Documento** | HO_PJM_CONFIGURACION_DELIVERABLES_SDLC.md |
| **Fecha de generación** | 2026-05-15T04:28:29.678460+00:00 |
| **Origen** | deliverables_catalog.json |
| **Estado** | Borrador técnico generado desde diccionarios SDLC |

---

## 1. Objetivo

Entregar al PJM una fuente estructurada del catálogo SDLC para configurar deliverables, dependencias y trazabilidad en VTT a partir de los diccionarios de `configuracion_deliverables`.

Este HO expone explícitamente los faltantes que siguen pendientes antes de una carga final en VTT:

- `hours` vacíos: **438**
- `complexity` vacíos: **438**

---

## 2. Datos de Proyecto VTT

| Campo | Valor |
|-------|-------|
| **Project ID VTT** | `` |
| **Phase ID VTT — 00-Discovery** | `` |
| **Phase ID VTT — 01-Planning** | `` |
| **Phase ID VTT — 02-Analysis** | `` |
| **Phase ID VTT — 3A-Design UX/UI** | `` |
| **Phase ID VTT — 3B-Design Technical** | `` |
| **Phase ID VTT — 04-Development** | `` |
| **Phase ID VTT — 05-Testing** | `` |
| **Phase ID VTT — 06-Deploy** | `` |
| **Phase ID VTT — 07-Operations** | `` |

### 2.1 UUIDs del equipo

| Rol | UUID VTT |
|-----|----------|
| Automático | `` |
| Backend Developer | `` |
| Brand Designer | `` |
| Business Users | `` |
| Content Writer | `` |
| Database Engineer | `` |
| Design Lead | `` |
| DevOps | `` |
| DevOps Lead | `` |
| DevOps Lead (automático via CD) | `` |
| Developer | `` |
| Developer (con cada fix) | `` |
| Developer asignado | `` |
| Developer asignado al bug | `` |
| Developers | `` |
| Development Team | `` |
| External Pentester | `` |
| External pentester | `` |
| Frontend Developer | `` |
| PM | `` |
| Product Manager | `` |
| Product Manager (workshop) | `` |
| Product Owner | `` |
| Product Owner (con datos del PM) | `` |
| Product Owner (con input de PM | `` |
| Program Manager | `` |
| QA | `` |
| QA Automation | `` |
| QA Engineer | `` |
| QA Lead | `` |
| Research Agent | `` |
| Risk Owners (según register) | `` |
| SA) | `` |
| SRE | `` |
| Security Engineer | `` |
| Security Engineer (si existe) | `` |
| Solution Architect | `` |
| Systems Analyst | `` |
| Tech Lead | `` |
| Technical Writer | `` |
| Todo el equipo | `` |
| Todo el equipo de desarrollo | `` |
| Transcription service | `` |
| UI Designer | `` |
| UX Designer | `` |
| UX Researcher | `` |

---

## 3. Resumen del Catálogo

| Fase | Nombre | Deliverables | Obligatorios | Opcionales |
|------|--------|--------------|--------------|------------|
| 00 | 00-Discovery | 22 | 22 | 0 |
| 01 | 01-Planning | 33 | 33 | 0 |
| 02 | 02-Analysis | 47 | 47 | 0 |
| 3A | 3A-Design UX/UI | 72 | 69 | 3 |
| 3B | 3B-Design Technical | 73 | 73 | 0 |
| 04 | 4-Development | 78 | 76 | 2 |
| 05 | 5-Testing | 52 | 52 | 0 |
| 06 | 6-Deploy | 38 | 38 | 0 |
| 07 | 7-Operations | 23 | 23 | 0 |

**Total deliverables extraídos:** 438

**Total dependencias trazadas:** 1553

---

## 4. Campos mínimos por Deliverable

Cada deliverable quedó normalizado con estos campos:

- `id`
- `name`
- `responsible_role`
- `executor_role`
- `required`
- `typical_effort`
- `hours`
- `complexity`
- `dependencies`

Regla aplicada: cuando el documento no trae el campo, el JSON deja `""` en texto y `[]` en listas.

---

## 5. Deliverables por Fase

### 00 — 00-Discovery

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 0.1.1 | Market Research Report | Product Manager | Research Agent / Systems Analyst | required | 3-5 días |  |  |  |
| 0.1.2 | TAM/SAM/SOM | Product Manager | Research Agent / Systems Analyst | required | 1-2 días |  |  | 0.1.1 |
| 0.1.3 | Market Trends | Product Manager | Research Agent / Systems Analyst | required | 1 día |  |  | 0.1.1 |
| 0.1.4 | Market Segments | Product Manager | Research Agent / Systems Analyst / PM | required | 1 día |  |  | 0.1.1, 0.1.2 |
| 0.1.5 | Target Market | Product Manager | Product Manager | required | 0.5 días |  |  | 0.1.4, 0.1.2 |
| 0.2.1 | Competitive Analysis Doc | Product Manager | Research Agent / Systems Analyst | required | 3-5 días |  |  | 0.1.5, 0.1.1 |
| 0.2.2 | Competitor List | Product Manager | Research Agent | required | 1 día |  |  | 0.1.5 |
| 0.2.3 | Feature Comparison | Product Manager | Systems Analyst + UX Designer | required | 2 días |  |  | 0.2.2 |
| 0.2.4 | Pricing Comparison | Product Manager | Research Agent / Systems Analyst | required | 1 día |  |  | 0.2.2, 0.2.3 |
| 0.2.5 | SWOT Analysis | Product Manager | Product Manager / Systems Analyst | required | 1 día |  |  | 0.2.2, 0.2.3 |
| 0.2.6 | Market Opportunities | Product Manager | Product Manager | required | 1 día |  |  | 0.2.3, 0.2.5, 0.1.3 |
| 0.2.7 | UX Benchmarking | Product Manager | UX Designer / Design Lead | required | 2-3 días |  |  | 0.2.2, 0.2.3 |
| 0.3.1 | Problem Statement | Product Owner | Product Owner (con input de PM y SA) | required | 1 día |  |  | 0.1.5 |
| 0.3.2 | User Pain Points | Product Owner | UX Researcher / Systems Analyst | required | 1-2 días |  |  | 0.3.1, 0.1.5 |
| 0.3.3 | Current Solutions | Product Owner | Systems Analyst / Research Agent | required | 1 día |  |  | 0.3.1, 0.3.2 |
| 0.3.4 | Why Now | Product Owner | Product Owner (con datos del PM) | required | 0.5 días |  |  | 0.3.1, 0.1.3 |
| 0.3.5 | Problem Validation | Product Owner | UX Researcher / Systems Analyst | required | 3-5 días |  |  | 0.3.1, 0.3.2, 0.1.5 |
| 0.4.1 | Value Proposition Canvas | Product Owner | Product Owner + Product Manager (workshop) | required | 1 día |  |  | 0.3.1, 0.3.2, 0.3.5 |
| 0.4.2 | UVP Statement | Product Owner | Product Owner | required | 0.5 días |  |  | 0.4.1 |
| 0.4.3 | Key Differentiators | Product Owner | Product Owner + Product Manager | required | 0.5 días |  |  | 0.4.1, 0.2.3 |
| 0.4.4 | Target Customer Profile | Product Owner | UX Designer / UX Researcher | required | 1 día |  |  | 0.1.5, 0.3.2 |
| 0.4.5 | Value Hypothesis | Product Owner | Product Owner + Product Manager | required | 0.5 días |  |  | 0.4.1, 0.3.5 |

### 01 — 01-Planning

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 1.1.1 | Vision Statement | Product Owner | Product Owner | required | 0.5 días |  |  | 0.3.1, 0.4.2 |
| 1.1.2 | Mission Statement | Product Owner | Product Owner | required | 0.5 días |  |  | 1.1.1 |
| 1.1.3 | Product Goals | Product Owner | Product Manager | required | 1 día |  |  | 1.1.1, 1.1.2 |
| 1.1.4 | Success Metrics (KPIs) | Product Owner | Product Manager | required | 1 día |  |  | 1.1.3, 0.4.5 |
| 1.1.5 | North Star Metric | Product Owner | Product Owner | required | 0.5 días |  |  | 1.1.4 |
| 1.1.6 | OKRs | Product Owner | Product Manager + Program Manager | required | 1 día |  |  | 1.1.3, 1.1.4 |
| 1.2.1 | Scope Statement | Product Manager | Product Manager | required | 1 día |  |  | 1.1.3, 0.3.1, 0.1.5 |
| 1.2.2 | In-Scope | Product Manager | Product Manager + Systems Analyst | required | 0.5 días |  |  | 1.2.1 |
| 1.2.3 | Out-of-Scope | Product Manager | Product Manager | required | 0.5 días |  |  | 1.2.1 |
| 1.2.4 | MVP Definition | Product Manager | Product Manager + Tech Lead | required | 2 días |  |  | 0.4.5, 1.2.2, 0.4.3 |
| 1.2.5 | Future Phases | Product Manager | Product Manager | required | 0.5 días |  |  | 1.2.3 |
| 1.2.6 | Assumptions | Product Manager | Product Manager + Systems Analyst | required | 0.5 días |  |  | 1.2.1 |
| 1.3.1 | Stakeholder Map | Program Manager | Program Manager | required | 0.5 días |  |  |  |
| 1.3.2 | Stakeholder Register | Program Manager | Program Manager | required | 0.5 días |  |  | 1.3.1 |
| 1.3.3 | RACI Matrix | Program Manager | Program Manager + Product Manager | required | 1 día |  |  | 1.3.2 |
| 1.3.4 | Communication Plan | Program Manager | Program Manager | required | 0.5 días |  |  | 1.3.1, 1.3.3 |
| 1.4.1 | Risk Register | Program Manager | Program Manager + Tech Lead + Systems Analyst | required | 1 día |  |  | 1.2.6, 1.2.1 |
| 1.4.2 | Risk Assessment | Program Manager | Program Manager | required | 0.5 días |  |  | 1.4.1 |
| 1.4.3 | Mitigation Plan | Program Manager | Risk Owners (según register) | required | 1 día |  |  | 1.4.2 |
| 1.4.4 | Contingency Plan | Program Manager | Program Manager + Tech Lead | required | 1 día |  |  | 1.4.2 |
| 1.4.5 | Risk Monitoring | Program Manager | Program Manager | required | 0.5 días (setup) |  |  | 1.4.1 |
| 1.5.1 | Project Schedule | Program Manager | Program Manager + Tech Lead | required | 2 días |  |  | 1.2.4, 1.1.6 |
| 1.5.2 | Milestones | Program Manager | Program Manager | required | 0.5 días |  |  | 1.5.1 |
| 1.5.3 | Phase Breakdown | Program Manager | Program Manager | required | 0.5 días |  |  | 1.5.1 |
| 1.5.4 | Sprint Calendar | Program Manager | Program Manager | required | 0.5 días |  |  | 1.5.1 |
| 1.5.5 | Dependencies | Program Manager | Program Manager + Tech Lead | required | 1 día |  |  | 1.5.1 |
| 1.5.6 | Critical Path | Program Manager | Program Manager | required | 0.5 días |  |  | 1.5.5 |
| 1.5.7 | Buffer Time | Program Manager | Program Manager | required | 0.5 días |  |  | 1.5.6 |
| 1.6.1 | Budget Estimate | Program Manager | Program Manager + Tech Lead | required | 1-2 días |  |  | 1.5.1, 1.6.3 |
| 1.6.2 | Cost Breakdown | Program Manager | Program Manager | required | 0.5 días |  |  | 1.6.1 |
| 1.6.3 | Resource Plan | Program Manager | Program Manager | required | 1 día |  |  | 1.5.1, 1.3.3 |
| 1.6.4 | ROI Analysis | Program Manager | Program Manager + Product Manager | required | 1 día |  |  | 1.6.1, 0.1.2 |
| 1.6.5 | Budget Tracking | Program Manager | Program Manager | required | 0.5 días (setup) |  |  | 1.6.1 |

### 02 — 02-Analysis

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 2.1.1 | SRS Document | Systems Analyst | Systems Analyst | required | 3-5 días |  |  | 1.2.4, 1.2.2, 0.3.1 |
| 2.1.2 | Requirements List | Systems Analyst | Systems Analyst | required | 1 día |  |  | 2.1.1 |
| 2.1.3 | Priority Matrix | Systems Analyst | Systems Analyst + Product Manager | required | 0.5 días |  |  | 2.1.2 |
| 2.1.4 | Feature List | Systems Analyst | Systems Analyst + Product Manager | required | 0.5 días |  |  | 2.1.2 |
| 2.1.5 | Functional Decomposition | Systems Analyst | Systems Analyst | required | 1 día |  |  | 2.1.4 |
| 2.1.6 | Requirements Approval | Systems Analyst | Product Owner | required | 0.5 días |  |  | 2.1.1, 2.1.3 |
| 2.2.1 | NFR Document | Systems Analyst | Systems Analyst + Solution Architect | required | 2-3 días |  |  | 2.1.1 |
| 2.2.2 | Performance Requirements | Systems Analyst | Systems Analyst + Tech Lead | required | 0.5 días |  |  |  |
| 2.2.3 | Security Requirements | Systems Analyst | Systems Analyst + Security Engineer (si existe) | required | 1 día |  |  |  |
| 2.2.4 | Scalability Requirements | Systems Analyst | Systems Analyst + Solution Architect | required | 0.5 días |  |  |  |
| 2.2.5 | Availability Requirements | Systems Analyst | Systems Analyst + DevOps | required | 0.5 días |  |  |  |
| 2.2.6 | Usability Requirements | Systems Analyst | UX Designer + Systems Analyst | required | 0.5 días |  |  |  |
| 2.3.1 | Use Case Document | Systems Analyst | Systems Analyst | required | 3-5 días |  |  | 2.1.1 |
| 2.3.2 | Use Case Diagram | Systems Analyst | Systems Analyst | required | 0.5 días |  |  |  |
| 2.3.3 | Use Case List | Systems Analyst | Systems Analyst | required | 0.5 días |  |  |  |
| 2.3.4 | Detailed Use Cases | Systems Analyst | Systems Analyst | required | 2-3 días |  |  |  |
| 2.3.5 | Actor Definitions | Systems Analyst | Systems Analyst | required | 0.5 días |  |  |  |
| 2.3.6 | Use Case Relationships | Systems Analyst | Systems Analyst | required | 0.5 días |  |  |  |
| 2.4.1 | Product Backlog | Product Manager | Product Manager | required | 2 días (inicial) |  |  | 2.3.1, 2.1.6 |
| 2.4.2 | User Stories | Product Manager | Product Manager + Systems Analyst | required | 3-5 días (batch inicial) |  |  | 2.4.1, 2.3.4 |
| 2.4.3 | Story Map | Product Manager | Product Manager | required | 1 día |  |  |  |
| 2.4.4 | Epics | Product Manager | Product Manager | required | 0.5 días |  |  |  |
| 2.4.5 | Story Estimation | Product Manager | Tech Lead + Developers | required | 0.5 días por sprint |  |  |  |
| 2.4.6 | Sprint Assignment | Product Manager | Product Manager + Tech Lead | required | En sprint planning |  |  | 2.4.5, 1.5.4 |
| 2.5.1 | Business Rules Document | Systems Analyst | Systems Analyst | required | 2-3 días |  |  | 2.1.1, 2.3.4 |
| 2.5.2 | Rules List | Systems Analyst | Systems Analyst | required | 0.5 días |  |  |  |
| 2.5.3 | Validation Rules | Systems Analyst | Systems Analyst | required | 1 día |  |  |  |
| 2.5.4 | Calculation Rules | Systems Analyst | Systems Analyst | required | 0.5 días |  |  |  |
| 2.5.5 | Authorization Rules | Systems Analyst | Systems Analyst | required | 1 día |  |  | 2.3.5, 2.5.1 |
| 2.5.6 | State Transition Rules | Systems Analyst | Systems Analyst | required | 1 día |  |  |  |
| 2.5.7 | Business Glossary | Systems Analyst | Systems Analyst | required | 1 día |  |  |  |
| 2.6.1 | User Flow Diagrams | UX Designer | UX Designer | required | 2-3 días |  |  | 2.3.4 |
| 2.6.2 | Happy Path Flows | UX Designer | UX Designer | required | 1 día |  |  |  |
| 2.6.3 | Error Flows | UX Designer | UX Designer | required | 1 día |  |  |  |
| 2.6.4 | Edge Cases | UX Designer | UX Designer + Systems Analyst | required | 1 día |  |  |  |
| 2.6.5 | User Journey Maps | UX Designer | UX Designer | required | 1-2 días |  |  | 2.6.1, 0.4.4 |
| 2.6.6 | Task Flows | UX Designer | UX Designer | required | 1 día |  |  |  |
| 2.6.7 | Navigation Map | UX Designer | UX Designer | required | 0.5 días |  |  |  |
| 2.7.1 | Acceptance Criteria Doc | QA Lead | QA Lead + Systems Analyst | required | 2 días |  |  | 2.1.1, 2.3.4 |
| 2.7.2 | Criteria per Story | QA Lead | QA Lead + Product Manager | required | Continuo (en refinement) |  |  | 2.4.2 |
| 2.7.3 | Definition of Done | QA Lead | QA Lead + Tech Lead | required | 0.5 días |  |  |  |
| 2.7.4 | Definition of Ready | QA Lead | QA Lead + Product Manager | required | 0.5 días |  |  |  |
| 2.7.5 | Test Scenarios | QA Lead | QA Lead + QA Engineer | required | Continuo |  |  |  |
| 2.8.1 | Traceability Matrix | Systems Analyst | Systems Analyst | required | 2 días |  |  | 2.1.2, 2.3.3 |
| 2.8.2 | RF to US Mapping | Systems Analyst | Systems Analyst | required | 0.5 días |  |  |  |
| 2.8.3 | US to Test Mapping | Systems Analyst | QA Lead + Systems Analyst | required | 0.5 días |  |  |  |
| 2.8.4 | Coverage Report | Systems Analyst | Systems Analyst | required | 0.5 días |  |  |  |

### 3A — 3A-Design UX/UI

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 3A.1.1 | User Research Plan | UX Designer | UX Researcher / UX Designer | required | 1-2 días |  |  | 0.3.1, 0.4.4, 0.3.2 |
| 3A.1.2 | User Research Report | UX Designer | UX Researcher / UX Designer | required | 2-3 días |  |  | 3A.1.1, 3A.1.4, 3A.1.5 |
| 3A.1.3 | Interview Guide | UX Designer | UX Researcher / UX Designer | required | 0.5-1 día |  |  | 3A.1.1 |
| 3A.1.4 | Interview Transcripts | UX Designer | UX Researcher / Transcription service | required | 0.5 día por entrevista (o automático con herramienta) |  |  | 3A.1.3 |
| 3A.1.5 | Survey Results | UX Designer | UX Researcher / UX Designer | required | 1-2 días (análisis y visualización) |  |  | 3A.1.1 |
| 3A.1.6 | User Insights | UX Designer | UX Designer | required | 0.5-1 día |  |  | 3A.1.2 |
| 3A.1.7 | Pain Points | UX Designer | UX Designer | required | 0.5 día |  |  | 3A.1.2 |
| 3A.1.8 | User Needs | UX Designer | UX Designer | required | 0.5 día |  |  | 3A.1.2, 3A.1.6 |
| 3A.1.9 | Behavioral Patterns | UX Designer | UX Researcher / UX Designer | required | 1 día |  |  | 3A.1.2, 3A.1.4 |
| 3A.2.1 | Personas Document | UX Designer | UX Designer | required | 2-3 días |  |  | 3A.1.2, 3A.1.9, 3A.1.7 |
| 3A.2.2 | Persona Cards | UX Designer | UX Designer / UI Designer | required | 0.5-1 día |  |  | 3A.2.1 |
| 3A.2.3 | Primary Persona | UX Designer | UX Designer | required | 0.5 día |  |  | 3A.2.1 |
| 3A.2.4 | Secondary Personas | UX Designer | UX Designer | required | 0.5-1 día |  |  | 3A.2.1, 3A.2.3 |
| 3A.2.5 | Anti-Personas | UX Designer | UX Designer | required | 0.25 día |  |  | 3A.2.1, 0.4.4 |
| 3A.2.6 | Scenarios | UX Designer | UX Designer | required | 1 día |  |  | 3A.2.1, 3A.1.8 |
| 3A.2.7 | Empathy Maps | UX Designer | UX Designer | required | 0.5 día |  |  | 3A.2.1, 3A.1.2 |
| 3A.2.8 | Jobs to be Done | UX Designer | UX Designer | required | 0.5-1 día |  |  | 3A.2.1, 3A.1.8, 3A.2.6 |
| 3A.3.1 | Site Map | UX Designer | UX Designer | required | 1-2 días |  |  | 2.3.3, 3A.2.3, 3A.3.6 |
| 3A.3.2 | Navigation Structure | UX Designer | UX Designer | required | 0.5-1 día |  |  | 3A.3.1 |
| 3A.3.3 | Navigation Patterns | UX Designer | UX Designer | required | 0.5 día |  |  | 3A.3.2 |
| 3A.3.4 | Content Inventory | UX Designer | UX Designer / Content Writer | required | 1 día |  |  | 3A.3.1 |
| 3A.3.5 | Taxonomy | UX Designer | UX Designer | required | 0.5-1 día |  |  | 3A.3.4, 3A.3.6 |
| 3A.3.6 | Card Sorting Results | UX Designer | UX Researcher / UX Designer | required | 1-2 días (ejecución + análisis) |  |  | 3A.3.4, 3A.2.3 |
| 3A.3.7 | Menu Structure | UX Designer | UX Designer | required | 0.5 día |  |  | 3A.3.2, 3A.3.1 |
| 3A.3.8 | URL Structure | UX Designer | UX Designer / Frontend Developer | required | 0.5 día |  |  | 3A.3.1 |
| 3A.4.1 | Wireframe Document | UX Designer | UX Designer | required | 0.5 día (compilación) |  |  | 3A.4.2, 3A.4.3, 3A.3.1 |
| 3A.4.2 | Low-Fi Wireframes | UX Designer | UX Designer | required | 1-2 días |  |  | 3A.3.1, 3A.3.2 |
| 3A.4.3 | Mid-Fi Wireframes | UX Designer | UX Designer | required | 3-5 días |  |  | 3A.4.2, 3A.3.2, 3A.3.4 |
| 3A.4.4 | Desktop Wireframes | UX Designer | UX Designer | required | Incluido en 3A.4.3 |  |  | 3A.4.3 |
| 3A.4.5 | Mobile Wireframes | UX Designer | UX Designer | required | 2-3 días |  |  | 3A.4.3, 3A.3.3 |
| 3A.4.6 | Tablet Wireframes | UX Designer | UX Designer | optional | 1-2 días |  |  | 3A.4.4, 3A.4.5 |
| 3A.4.7 | Wireframe Annotations | UX Designer | UX Designer | required | 1 día |  |  | 3A.4.3, 2.3.4 |
| 3A.4.8 | Wireframe Flows | UX Designer | UX Designer | required | 1 día |  |  | 3A.4.3, 2.6.1 |
| 3A.4.9 | Responsive Breakpoints | UX Designer | UX Designer / Frontend Developer | required | 0.5 día |  |  | 3A.4.4, 3A.4.5 |
| 3A.5.1 | UI Mockups Complete | UI Designer | UI Designer | required | 5-10 días |  |  | 3A.4.3, 3A.4.7 |
| 3A.5.10 | Responsive Variants | UI Designer | UI Designer | required | Incluido en desktop + mobile |  |  | 3A.5.2, 3A.5.3, 3A.4.9 |
| 3A.5.2 | Desktop Mockups | UI Designer | UI Designer | required | Incluido en 3A.5.1 |  |  | 3A.4.4 |
| 3A.5.3 | Mobile Mockups | UI Designer | UI Designer | required | 3-5 días |  |  | 3A.4.5 |
| 3A.5.4 | Tablet Mockups | UI Designer | UI Designer | optional | 2-3 días |  |  | 3A.4.6 |
| 3A.5.5 | Component States | UI Designer | UI Designer | required | 2-3 días |  |  | 3A.5.1 |
| 3A.5.6 | Empty States | UI Designer | UI Designer | required | 1 día |  |  | 3A.5.1 |
| 3A.5.7 | Error States | UI Designer | UI Designer | required | 1 día |  |  | 3A.5.1 |
| 3A.5.8 | Loading States | UI Designer | UI Designer | required | 0.5-1 día |  |  | 3A.5.1 |
| 3A.5.9 | Dark Mode | UI Designer | UI Designer | optional | 2-3 días |  |  | 3A.5.1, 3A.7.2 |
| 3A.6.1 | Interactive Prototype | UI Designer | UI Designer | required | 2-3 días |  |  | 3A.5.1, 3A.4.8, 2.6.1 |
| 3A.6.2 | Main Flow Prototype | UI Designer | UI Designer | required | Incluido en 3A.6.1 |  |  | 3A.6.1, 2.6.2 |
| 3A.6.3 | Secondary Flows | UI Designer | UI Designer | required | 1-2 días |  |  | 3A.6.1, 3A.6.2 |
| 3A.6.4 | Micro-interactions | UI Designer | UI Designer | required | 1-2 días |  |  | 3A.5.1, 3A.5.5 |
| 3A.6.5 | Prototype Links | UI Designer | UI Designer | required | 0.25 día |  |  | 3A.6.1 |
| 3A.6.6 | Prototype Documentation | UI Designer | UI Designer | required | 0.5 día |  |  | 3A.6.1, 3A.6.5 |
| 3A.7.1 | Design Tokens | UI Designer | UI Designer / Frontend Developer | required | 2-3 días |  |  | 3A.5.1, 3A.7.2, 3A.7.3, 3A.7.4 |
| 3A.7.10 | Asset Library | UI Designer | UI Designer | required | 1-2 días |  |  | 3A.7.5, 3A.7.9, 3A.5.1 |
| 3A.7.2 | Color Palette | UI Designer | UI Designer | required | 1-2 días |  |  | 3A.5.1, 3A.7.9 |
| 3A.7.3 | Typography Scale | UI Designer | UI Designer | required | 1 día |  |  | 3A.5.1, 3A.7.9 |
| 3A.7.4 | Spacing System | UI Designer | UI Designer | required | 1 día |  |  | 3A.5.1, 3A.4.9 |
| 3A.7.5 | Icon Library | UI Designer | UI Designer | required | 2-3 días |  |  | 3A.5.1, 3A.7.2, 3A.7.4 |
| 3A.7.6 | Component Library | UI Designer | UI Designer | required | 5-8 días |  |  | 3A.5.1, 3A.5.5, 3A.7.1, 3A.7.2, 3A.7.3, 3A.7.4, 3A.7.5 |
| 3A.7.7 | Component Documentation | UI Designer | UI Designer / Technical Writer | required | 3-5 días |  |  | 3A.7.6, 3A.7.1 |
| 3A.7.8 | Pattern Library | UI Designer | UX Designer / UI Designer | required | 3-4 días |  |  | 3A.7.6, 3A.5.1, 3A.3.3 |
| 3A.7.9 | Brand Guidelines | UI Designer | UI Designer / Brand Designer | required | 2-3 días |  |  | 0.4.2, 0.4.4, 3A.7.2, 3A.7.3 |
| 3A.8.1 | Usability Test Plan | UX Designer | UX Researcher / UX Designer | required | 1-2 días |  |  | 3A.6.1, 3A.2.1, 2.6.1, 2.6.2 |
| 3A.8.2 | Test Script | UX Designer | UX Researcher / UX Designer | required | 1 día |  |  | 3A.8.1, 3A.6.1, 3A.6.5 |
| 3A.8.3 | Participant Criteria | UX Designer | UX Researcher / UX Designer | required | 0.5 días |  |  | 3A.8.1, 3A.2.1, 3A.2.3 |
| 3A.8.4 | Test Results | UX Designer | UX Researcher / UX Designer | required | 2-3 días |  |  | 3A.8.1, 3A.8.2, 3A.8.3 |
| 3A.8.5 | Findings & Recommendations | UX Designer | UX Researcher / UX Designer | required | 2-3 días |  |  | 3A.8.4, 3A.8.1 |
| 3A.8.6 | Iteration Log | UX Designer | UI Designer / UX Designer | required | 1-2 días (paralelo a iteraciones) |  |  | 3A.8.5, 3A.5.1 |
| 3A.8.7 | Final Validation | UX Designer | UX Designer | required | 0.5-1 día |  |  | 3A.8.4, 3A.8.5, 3A.8.6 |
| 3A.9.1 | Handoff Document | UI Designer | UI Designer / UX Designer | required | 1-2 días |  |  | 3A.8.7, 3A.5.1, 3A.6.1, 3A.7.6, 3A.7.7 |
| 3A.9.2 | Specs Export | UI Designer | UI Designer | required | 1 día |  |  | 3A.5.1, 3A.7.1, 3A.7.6, 3A.8.7 |
| 3A.9.3 | Asset Export | UI Designer | UI Designer | required | 0.5-1 día |  |  | 3A.7.10, 3A.7.5, 3A.8.7 |
| 3A.9.4 | CSS Variables | UI Designer | UI Designer / Frontend Developer | required | 0.5-1 día |  |  | 3A.7.1, 3A.7.2, 3A.7.3, 3A.7.4 |
| 3A.9.5 | Redlines | UI Designer | UI Designer | required | 1-2 días |  |  | 3A.5.1, 3A.7.4, 3A.8.7, 3A.9.2 |

### 3B — 3B-Design Technical

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 3B.1.1 | Architecture Document | Solution Architect | Solution Architect | required | 3-5 días |  |  | 2.3.4, 2.5.1, 1.2.2, 1.4.1, 3A.9.1 |
| 3B.1.2 | System Context Diagram | Solution Architect | Solution Architect | required | 0.5 días |  |  | 3B.1.1, 2.3.5, 1.2.2 |
| 3B.1.3 | Container Diagram | Solution Architect | Solution Architect | required | 1 día |  |  | 3B.1.1, 3B.1.2, 3B.1.5 |
| 3B.1.4 | Component Diagram | Solution Architect | Solution Architect / Tech Lead | required | 1-2 días |  |  | 3B.1.3, 2.3.4, 3B.2.3 |
| 3B.1.5 | Technology Stack | Solution Architect | Solution Architect / Tech Lead | required | 1 día |  |  | 3B.1.1, 1.2.6, 1.4.1 |
| 3B.1.6 | Integration Points | Solution Architect | Solution Architect / Backend Developer | required | 1-2 días |  |  | 3B.1.2, 3B.1.1, 2.3.4 |
| 3B.1.7 | Data Flow Diagram | Solution Architect | Solution Architect | required | 1 día |  |  | 3B.1.3, 3B.1.6, 2.3.4 |
| 3B.2.1 | Folder Structure | Tech Lead | Tech Lead | required | 0.5-1 día |  |  | 3B.1.5, 3B.1.4, 3B.2.3 |
| 3B.2.2 | Coding Standards | Tech Lead | Tech Lead | required | 1-2 días |  |  | 3B.1.5, 3B.2.5 |
| 3B.2.3 | Design Patterns | Tech Lead | Tech Lead / Solution Architect | required | 1-2 días |  |  | 3B.1.1, 3B.1.4, 3B.1.5 |
| 3B.2.4 | Module Dependencies | Tech Lead | Tech Lead | required | 0.5-1 día |  |  | 3B.1.4, 3B.2.1, 3B.2.3 |
| 3B.2.5 | Naming Conventions | Tech Lead | Tech Lead | required | 0.5 día |  |  | 3B.1.5, 2.5.7 |
| 3B.2.6 | Error Handling Strategy | Tech Lead | Tech Lead / Backend Developer | required | 1 día |  |  | 3B.1.5, 3B.2.3, 3B.4.5 |
| 3B.3.1 | ERD Complete | Database Engineer | Database Engineer | required | 2-3 días |  |  | 2.3.4, 2.5.1, 3B.1.7, 3B.1.5 |
| 3B.3.2 | Schema Definition | Database Engineer | Database Engineer / Backend Developer | required | 2-3 días |  |  | 3B.3.1, 3B.1.5, 3B.2.5 |
| 3B.3.3 | Table Specifications | Database Engineer | Database Engineer | required | 2-3 días |  |  | 3B.3.1, 3B.3.2, 2.5.1 |
| 3B.3.4 | Index Strategy | Database Engineer | Database Engineer | required | 1 día |  |  | 3B.3.3, 3B.3.1, 3B.3.2 |
| 3B.3.5 | Data Dictionary | Database Engineer | Database Engineer / Technical Writer | required | 1-2 días |  |  | 3B.3.2, 3B.3.3, 2.5.7 |
| 3B.3.6 | Migration Strategy | Database Engineer | Database Engineer / Backend Developer | required | 0.5-1 día |  |  | 3B.1.5, 3B.3.2, 3B.8.5 |
| 3B.3.7 | Seed Data Plan | Database Engineer | Database Engineer / Backend Developer | required | 1 día |  |  | 3B.3.2, 3B.3.3, 2.5.5 |
| 3B.3.8 | Backup Strategy | Database Engineer | DevOps Lead / Database Engineer | required | 0.5-1 día |  |  | 3B.1.5, 3B.3.2, 3B.8.1, 3B.8.8 |
| 3B.4.1 | OpenAPI Spec | Tech Lead | Tech Lead / Backend Developer | required | 3-5 días |  |  | 3B.4.2, 3B.3.1, 3B.4.6, 2.3.4 |
| 3B.4.10 | Postman Collection | Tech Lead | Backend Developer | required | 0.5-1 día |  |  | 3B.4.1, 3B.4.3, 3B.4.6 |
| 3B.4.11 | API Guidelines | Tech Lead | Tech Lead | required | 1 día |  |  | 3B.4.4, 3B.4.5, 3B.4.9, 3B.2.5 |
| 3B.4.2 | Endpoints List | Tech Lead | Tech Lead / Backend Developer | required | 1 día |  |  | 2.3.4, 3B.3.1, 2.5.5 |
| 3B.4.3 | Request/Response Examples | Tech Lead | Backend Developer | required | 1-2 días |  |  | 3B.4.2, 3B.3.5, 3B.4.5 |
| 3B.4.4 | Pagination Strategy | Tech Lead | Backend Developer | required | 0.5 día |  |  | 3B.4.2, 3B.3.3 |
| 3B.4.5 | Error Codes | Tech Lead | Backend Developer | required | 0.5-1 día |  |  | 3B.2.6, 2.5.3, 2.5.1 |
| 3B.4.6 | Authentication Spec | Tech Lead | Backend Developer / Security Engineer | required | 1-2 días |  |  | 3B.7.2, 3B.1.5, 3B.4.2 |
| 3B.4.7 | Authorization Spec | Tech Lead | Backend Developer / Security Engineer | required | 1-2 días |  |  | 2.5.5, 3B.7.3, 3B.4.2, 2.3.5 |
| 3B.4.8 | Rate Limiting | Tech Lead | Backend Developer | required | 0.5 día |  |  | 3B.4.2, 3B.1.5 |
| 3B.4.9 | Versioning Strategy | Tech Lead | Tech Lead | required | 0.5 día |  |  | 3B.4.2, 3B.1.1 |
| 3B.5.1 | Sequence Diagrams Doc | Solution Architect | Solution Architect | required | 0.5 día |  |  | 3B.5.2, 3B.5.3, 3B.5.4, 3B.5.5, 3B.5.6 |
| 3B.5.2 | Auth Flow | Solution Architect | Solution Architect / Backend Developer | required | 0.5 día |  |  | 3B.4.6, 3B.1.3 |
| 3B.5.3 | Main Business Flows | Solution Architect | Solution Architect / Backend Developer | required | 2-3 días |  |  | 2.3.4, 3B.1.4, 3B.4.2, 2.5.1 |
| 3B.5.4 | Error Flows | Solution Architect | Solution Architect / Backend Developer | required | 1 día |  |  | 3B.2.6, 3B.5.3, 3B.4.5 |
| 3B.5.5 | Integration Flows | Solution Architect | Solution Architect / Backend Developer | required | 1-2 días |  |  | 3B.1.6, 3B.1.3 |
| 3B.5.6 | Async Flows | Solution Architect | Solution Architect / Backend Developer | required | 1 día |  |  | 3B.1.3, 3B.1.7, 3B.1.5 |
| 3B.6.1 | ADR Template | Solution Architect | Solution Architect | required | 0.25 día |  |  |  |
| 3B.6.2 | ADR Index | Solution Architect | Solution Architect | required | 0.25 día |  |  | 3B.6.1, 3B.6.3 |
| 3B.6.3 | ADR Documents | Solution Architect | Solution Architect / Tech Lead | required | 0.5 día por ADR (5-10 ADRs iniciales = 3-5 días) |  |  | 3B.6.1 |
| 3B.6.4 | Decision Log | Solution Architect | Solution Architect / Tech Lead | required | 0.25 día + actualización continua |  |  | 3B.6.1 |
| 3B.7.1 | Security Plan | Security Engineer | Security Engineer | required | 2-3 días |  |  | 3B.1.2, 3B.3.5, 3B.4.6, 3B.4.7 |
| 3B.7.10 | Security Logging | Security Engineer | Backend Developer / DevOps Lead | required | 0.5-1 día |  |  | 3B.7.1, 3B.8.11 |
| 3B.7.11 | Incident Response Plan | Security Engineer | Security Engineer / DevOps Lead | required | 1 día |  |  | 3B.7.1, 3B.7.10 |
| 3B.7.2 | Authentication Design | Security Engineer | Security Engineer / Backend Developer | required | 1-2 días |  |  | 3B.4.6, 3B.7.1 |
| 3B.7.3 | Authorization Design | Security Engineer | Security Engineer / Backend Developer | required | 1-2 días |  |  | 3B.4.7, 3B.7.1 |
| 3B.7.4 | Data Protection Plan | Security Engineer | Security Engineer | required | 1-2 días |  |  | 3B.3.5, 3B.1.7 |
| 3B.7.5 | Encryption Strategy | Security Engineer | Security Engineer / Backend Developer | required | 0.5-1 día |  |  | 3B.7.4, 3B.1.5 |
| 3B.7.6 | OWASP Checklist | Security Engineer | Security Engineer | required | 1 día |  |  | 3B.7.1, 3B.1.5 |
| 3B.7.7 | Security Headers | Security Engineer | Backend Developer / DevOps Lead | required | 0.5 día |  |  | 3B.1.5, 3B.7.1 |
| 3B.7.8 | Secrets Management | Security Engineer | DevOps Lead | required | 0.5-1 día |  |  | 3B.1.5, 3B.1.6 |
| 3B.7.9 | Input Validation Rules | Security Engineer | Backend Developer | required | 1 día |  |  | 3B.4.1, 2.5.3 |
| 3B.8.1 | Infrastructure Plan | DevOps Lead | DevOps Lead | required | 2-3 días |  |  | 3B.1.3, 3B.1.5, 3B.7.1 |
| 3B.8.10 | SLA Definition | DevOps Lead | DevOps Lead / Solution Architect | required | 0.5 día |  |  | 3B.8.1 |
| 3B.8.11 | Monitoring Strategy | DevOps Lead | DevOps Lead | required | 1 día |  |  | 3B.8.10, 3B.1.5 |
| 3B.8.2 | Infrastructure Diagram | DevOps Lead | DevOps Lead | required | 0.5-1 día |  |  | 3B.1.3, 3B.8.3, 3B.8.4 |
| 3B.8.3 | Server Specifications | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 3B.1.3, 3B.9.1 |
| 3B.8.4 | Network Design | DevOps Lead | DevOps Lead | required | 0.5-1 día |  |  | 3B.8.2, 3B.7.1 |
| 3B.8.5 | Environment Matrix | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 3B.8.3 |
| 3B.8.6 | Scaling Strategy | DevOps Lead | DevOps Lead | required | 0.5-1 día |  |  | 3B.8.3, 3B.1.3 |
| 3B.8.7 | Backup Strategy | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 3B.3.8, 3B.8.1 |
| 3B.8.8 | Disaster Recovery Plan | DevOps Lead | DevOps Lead | required | 1 día |  |  | 3B.3.8, 3B.8.7, 3B.8.1 |
| 3B.8.9 | Cost Estimate | DevOps Lead | DevOps Lead | required | 0.5-1 día |  |  | 3B.8.3, 3B.8.5 |
| 3B.9.1 | Technical Estimates | Tech Lead | Tech Lead / Development Team | required | 2-3 días |  |  | 2.4.5, 3B.9.3, 3B.9.5 |
| 3B.9.2 | Story Points | Tech Lead | Development Team | required | 1 día (sesión de estimación) |  |  | 2.4.1, 3B.9.5 |
| 3B.9.3 | Task Breakdown | Tech Lead | Tech Lead / Development Team | required | 1-2 días |  |  | 2.4.1, 3B.4.2, 3B.3.1 |
| 3B.9.4 | Effort Matrix | Tech Lead | Tech Lead | required | 0.5 día |  |  | 3B.9.1, 2.4.4 |
| 3B.9.5 | Complexity Assessment | Tech Lead | Tech Lead / Solution Architect | required | 1 día |  |  | 3B.1.4, 3B.1.6, 2.5.1 |
| 3B.9.6 | Risk-adjusted Estimates | Tech Lead | Tech Lead | required | 0.5 día |  |  | 3B.9.1, 3B.9.5, 1.4.1 |
| 3B.9.7 | Dependencies Map | Tech Lead | Tech Lead | required | 0.5-1 día |  |  | 3B.9.3, 3B.2.4 |
| 3B.9.8 | Velocity Baseline | Tech Lead | Tech Lead | required | 0.25 día (setup) + medición continua |  |  | 3B.9.2 |
| 3B.9.9 | Capacity Planning | Tech Lead | Tech Lead / Program Manager | required | 1 día |  |  | 3B.9.1, 3B.9.4, 3B.9.8 |

### 04 — 4-Development

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 4.1.1 | Development Environment | DevOps Lead | DevOps Lead | required | 1-2 días |  |  | 3B.1.5, 3B.8.5 |
| 4.1.10 | Formatter Configuration | DevOps Lead | Tech Lead | required | 0.25 día |  |  | 3B.2.2 |
| 4.1.2 | Environment Setup Guide | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 4.1.1 |
| 4.1.3 | Environment Variables | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 3B.7.8, 3B.1.5 |
| 4.1.4 | Docker Compose | DevOps Lead | DevOps Lead | required | Incluido en 4.1.1 |  |  | 3B.1.5, 4.1.3 |
| 4.1.5 | Makefile / Scripts | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 4.1.1 |
| 4.1.6 | IDE Configuration | DevOps Lead | Tech Lead | required | 0.25 día |  |  | 3B.2.2 |
| 4.1.7 | Pre-commit Hooks | DevOps Lead | DevOps Lead / Tech Lead | required | 0.25 día |  |  | 4.1.9, 4.1.10 |
| 4.1.8 | Git Configuration | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 3B.1.5 |
| 4.1.9 | Linter Configuration | DevOps Lead | Tech Lead | required | 0.5 día |  |  | 3B.2.2, 3B.1.5 |
| 4.2.1 | Initial Migration | Database Engineer | Database Engineer / Backend Developer | required | 1-2 días |  |  | 3B.3.2, 4.1.1 |
| 4.2.10 | Rollback Scripts | Database Engineer | Database Engineer / DevOps Lead | required | Incluido en cada migration |  |  | 4.2.2 |
| 4.2.2 | Schema Migrations | Database Engineer | Database Engineer / Backend Developer | required | Continuo (por sprint) |  |  | 4.2.1, 3B.3.6 |
| 4.2.3 | Seed Data | Database Engineer | Database Engineer / Backend Developer | required | 0.5-1 día |  |  | 4.2.1, 3B.3.7 |
| 4.2.4 | Test Data | Database Engineer | Backend Developer / QA | required | 0.5-1 día |  |  | 4.2.3, 4.2.1 |
| 4.2.5 | Indexes | Database Engineer | Database Engineer | required | 0.5 día |  |  | 3B.3.4, 4.2.1 |
| 4.2.6 | Constraints | Database Engineer | Database Engineer | required | Incluido en 4.2.1 |  |  | 4.2.1, 3B.3.3 |
| 4.2.7 | Stored Procedures | Database Engineer | Database Engineer | optional | 1-2 días (si aplica) |  |  | 4.2.1 |
| 4.2.8 | Views | Database Engineer | Database Engineer | optional | 0.5-1 día (si aplica) |  |  | 4.2.1 |
| 4.2.9 | Migration Guide | Database Engineer | Database Engineer | required | 0.5 día |  |  | 3B.3.6, 4.2.1 |
| 4.3.1 | API Endpoints | Backend Developer | Backend Developer | required | 5-10 días (continuo por sprint) |  |  | 3B.4.1, 4.2.1, 4.3.2, 4.3.5 |
| 4.3.10 | Integration Tests | Backend Developer | Backend Developer | required | 2-3 días |  |  | 4.3.1, 4.2.4 |
| 4.3.11 | API Documentation | Backend Developer | Backend Developer | required | Incluido en implementación (auto-generado) |  |  | 4.3.1, 4.3.5 |
| 4.3.12 | Postman Collection | Backend Developer | Backend Developer | required | 0.5 día (actualización) |  |  | 3B.4.10, 4.3.1 |
| 4.3.13 | Backend README | Backend Developer | Backend Developer | required | 0.5 día |  |  |  |
| 4.3.14 | Error Handling | Backend Developer | Backend Developer | required | 1 día |  |  | 3B.2.6, 3B.4.5 |
| 4.3.15 | Logging | Backend Developer | Backend Developer | required | 0.5-1 día |  |  | 3B.7.10, 3B.8.11 |
| 4.3.2 | Services | Backend Developer | Backend Developer | required | 5-10 días (continuo por sprint) |  |  | 2.5.1, 4.3.4, 4.3.3 |
| 4.3.3 | Models | Backend Developer | Backend Developer | required | 1-2 días |  |  | 4.2.1, 3B.3.2 |
| 4.3.4 | Repositories | Backend Developer | Backend Developer | required | 2-3 días |  |  | 4.3.3, 3B.2.3 |
| 4.3.5 | DTOs/Schemas | Backend Developer | Backend Developer | required | 1-2 días |  |  | 3B.4.1, 4.3.3 |
| 4.3.6 | Workers | Backend Developer | Backend Developer | required | 2-3 días |  |  | 3B.5.6, 4.3.2 |
| 4.3.7 | Middlewares | Backend Developer | Backend Developer | required | 1-2 días |  |  | 3B.4.6, 3B.2.6 |
| 4.3.8 | Utils | Backend Developer | Backend Developer | required | Continuo (por necesidad) |  |  | 3B.2.1 |
| 4.3.9 | Unit Tests BE | Backend Developer | Backend Developer | required | Continuo (30% del tiempo de dev) |  |  | 4.3.2, 4.6.5 |
| 4.4.1 | Components | Frontend Developer | Frontend Developer | required | 5-10 días (continuo) |  |  | 3A.7.6, 3A.9.4, 3A.9.2 |
| 4.4.10 | Unit Tests FE | Frontend Developer | Frontend Developer | required | Continuo (30% del tiempo dev) |  |  | 4.4.4, 4.4.9 |
| 4.4.11 | Component Tests | Frontend Developer | Frontend Developer | required | Continuo |  |  | 4.4.1 |
| 4.4.12 | Storybook | Frontend Developer | Frontend Developer | required | 2-3 días + continuo |  |  | 4.4.1 |
| 4.4.13 | Frontend README | Frontend Developer | Frontend Developer | required | 0.5 día |  |  |  |
| 4.4.14 | Accessibility | Frontend Developer | Frontend Developer | required | Continuo (incluido en cada componente) |  |  | 4.4.1 |
| 4.4.15 | Responsive Implementation | Frontend Developer | Frontend Developer | required | Continuo (incluido en cada componente/page) |  |  | 3A.4.9, 3A.5.10, 4.4.1, 4.4.3 |
| 4.4.2 | Pages | Frontend Developer | Frontend Developer | required | 5-10 días (continuo) |  |  | 4.4.1, 4.4.6, 4.4.3 |
| 4.4.3 | Layouts | Frontend Developer | Frontend Developer | required | 1-2 días |  |  | 3A.3.2, 4.4.1 |
| 4.4.4 | Hooks | Frontend Developer | Frontend Developer | required | Continuo |  |  | 4.4.6, 4.4.5 |
| 4.4.5 | State Management | Frontend Developer | Frontend Developer | required | 1-2 días |  |  | 3B.1.5 |
| 4.4.6 | API Client | Frontend Developer | Frontend Developer | required | 1 día |  |  | 3B.4.1, 3B.4.6 |
| 4.4.7 | Types/Interfaces | Frontend Developer | Frontend Developer | required | 1 día + continuo |  |  | 3B.4.1 |
| 4.4.8 | Styles | Frontend Developer | Frontend Developer | required | Continuo |  |  | 3A.9.4, 3B.1.5 |
| 4.4.9 | Utils | Frontend Developer | Frontend Developer | required | Continuo |  |  | 3B.2.1 |
| 4.5.1 | Integration Code | Backend Developer | Backend Developer | required | 3-5 días (por integración) |  |  | 3B.1.6, 3B.5.5, 4.3.2 |
| 4.5.2 | API Clients | Backend Developer | Backend Developer | required | Incluido en 4.5.1 |  |  | 3B.1.6 |
| 4.5.3 | Webhooks | Backend Developer | Backend Developer | required | 1-2 días |  |  | 3B.5.5, 4.3.1 |
| 4.5.4 | OAuth Integrations | Backend Developer | Backend Developer | required | 1-2 días por provider |  |  | 3B.4.6, 4.3.2 |
| 4.5.5 | Third-party SDKs | Backend Developer | Backend Developer | required | 0.5-1 día por SDK |  |  | 3B.1.6, 4.1.3 |
| 4.5.6 | Integration Tests | Backend Developer | Backend Developer | required | 1-2 días |  |  | 4.5.1 |
| 4.5.7 | Integration Docs | Backend Developer | Backend Developer | required | 0.5 día por integración |  |  | 4.5.1 |
| 4.5.8 | Error Handling | Backend Developer | Backend Developer | required | Incluido en 4.5.1 |  |  | 4.5.1, 3B.2.6 |
| 4.5.9 | Retry Logic | Backend Developer | Backend Developer | required | 0.5-1 día |  |  | 3B.2.6 |
| 4.6.1 | Unit Tests BE | QA Automation | QA Automation / Backend Developer | required | Continuo |  |  | 4.3.9, 4.6.3 |
| 4.6.2 | Unit Tests FE | QA Automation | QA Automation / Frontend Developer | required | Continuo |  |  | 4.4.10, 4.6.3 |
| 4.6.3 | Test Coverage Report | QA Automation | QA Automation | required | Automático (configuración 0.25 día) |  |  |  |
| 4.6.4 | Coverage ≥80% | QA Automation | Todo el equipo de desarrollo | required | Continuo |  |  | 4.6.3 |
| 4.6.5 | Mock Factories | QA Automation | QA Automation / Backend Developer | required | 1 día |  |  | 4.3.3 |
| 4.6.6 | Test Fixtures | QA Automation | QA Automation | required | 0.5 día |  |  | 3B.4.3 |
| 4.6.7 | Test Utils | QA Automation | QA Automation | required | 0.5 día |  |  |  |
| 4.7.1 | Main README | Technical Writer | Technical Writer / Tech Lead | required | 0.5 día |  |  |  |
| 4.7.2 | Backend README | Technical Writer | Technical Writer / Backend Developer | required | 0.5 día |  |  | 4.3.13 |
| 4.7.3 | Frontend README | Technical Writer | Technical Writer / Frontend Developer | required | 0.5 día |  |  | 4.4.13 |
| 4.7.4 | API Docs | Technical Writer | Backend Developer | required | Automático (mantenimiento 0.5 día) |  |  | 4.3.11 |
| 4.7.5 | Code Comments | Technical Writer | Todo el equipo de desarrollo | required | Continuo |  |  |  |
| 4.7.6 | Architecture Docs | Technical Writer | Technical Writer / Solution Architect | required | 1 día |  |  | 3B.1.1 |
| 4.7.7 | Contributing Guide | Technical Writer | Technical Writer / Tech Lead | required | 0.5 día |  |  | 4.1.8 |
| 4.7.8 | Changelog | Technical Writer | Automático / Tech Lead | required | Automático (configuración 0.25 día) |  |  | 4.7.7 |
| 4.8.1 | PR Reviews | Tech Lead | Todo el equipo de desarrollo | required | Continuo (20-30% del tiempo de dev) |  |  | 3B.2.2, 4.7.7 |
| 4.8.2 | Code Quality Report | Tech Lead | Tech Lead / QA Lead | required | 0.5 día por sprint |  |  | 4.6.3 |
| 4.8.3 | Technical Debt Log | Tech Lead | Tech Lead / Todo el equipo | required | Continuo (actualización por sprint) |  |  |  |
| 4.8.4 | Refactoring Plan | Tech Lead | Tech Lead | required | 0.5 día por sprint |  |  | 4.8.3, 4.8.2 |

### 05 — 5-Testing

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 5.1.1 | Test Plan | QA Lead | QA Lead | required | 1-2 días |  |  | 2.3.4, 5.1.2 |
| 5.1.2 | Test Strategy | QA Lead | QA Lead | required | 1 día |  |  | 3B.1.5 |
| 5.1.3 | Test Scope | QA Lead | QA Lead | required | 0.5 día |  |  | 5.1.1 |
| 5.1.4 | Test Schedule | QA Lead | QA Lead | required | 0.25 día |  |  | 5.1.1 |
| 5.1.5 | Resource Allocation | QA Lead | QA Lead | required | 0.25 día |  |  | 5.1.4 |
| 5.10.1 | UAT Plan | Product Owner | Product Owner / Business Users | required | 0.5 día |  |  | 5.4.4, 5.3.1 |
| 5.10.2 | UAT Test Cases | Product Owner | Product Owner / Business Users | required | 0.5 día |  |  | 5.10.1 |
| 5.10.3 | UAT Results | Product Owner | Business Users | required | 1-2 días (durante UAT) |  |  | 5.10.2 |
| 5.10.4 | User Feedback | Product Owner | Business Users | required | Incluido en UAT |  |  | 5.10.3 |
| 5.10.5 | UAT Sign-off | Product Owner | Product Owner | required | 0.25 día |  |  | 5.10.3, 5.4.4 |
| 5.11.1 | Bug Fixes Implemented | Backend Developer / Frontend Developer | Developer asignado al bug | required | Variable (por bug) |  |  | 5.4.3 |
| 5.11.2 | Regression Tests | QA Automation / Developer | Developer (con cada fix) | required | Incluido en cada fix |  |  | 5.11.1 |
| 5.11.3 | Bug Resolution Report | QA Lead | QA Lead | required | 0.5 día |  |  | 5.11.1 |
| 5.2.1 | Test Cases Document | QA Engineer | QA Engineer | required | 3-5 días |  |  | 2.3.4, 5.1.3 |
| 5.2.2 | Test Case IDs | QA Engineer | QA Engineer | required | Incluido en 5.2.1 |  |  | 5.2.1 |
| 5.2.3 | Test Data | QA Engineer | QA Engineer | required | 1 día |  |  | 5.2.1 |
| 5.2.4 | Expected Results | QA Engineer | QA Engineer | required | Incluido en 5.2.1 |  |  | 5.2.1 |
| 5.3.1 | Test Environment | DevOps Lead | DevOps Lead | required | 1 día |  |  | 3B.8.5, 4.1.1 |
| 5.3.2 | Test Database | DevOps Lead | DevOps Lead / Database Engineer | required | 0.5 día |  |  | 4.2.1, 4.2.3 |
| 5.3.3 | Test Data Seeding | DevOps Lead | QA Engineer / DevOps Lead | required | 0.5 día |  |  | 5.3.2, 5.2.3 |
| 5.3.4 | Environment Documentation | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 5.3.1 |
| 5.4.1 | Functional Test Results | QA Engineer | QA Engineer | required | 3-5 días por sprint |  |  | 5.2.1, 5.3.1 |
| 5.4.2 | Test Execution Log | QA Engineer | QA Engineer | required | Continuo (durante ejecución) |  |  | 5.4.1 |
| 5.4.3 | Defects Found | QA Engineer | QA Engineer | required | Continuo |  |  | 5.4.1 |
| 5.4.4 | Pass/Fail Summary | QA Engineer | QA Engineer | required | 0.25 día |  |  | 5.4.1 |
| 5.4.5 | Screenshots/Evidence | QA Engineer | QA Engineer | required | Continuo (durante testing) |  |  | 5.4.1 |
| 5.5.1 | Integration Test Suite | QA Automation | QA Automation | required | 3-5 días |  |  | 4.3.10, 5.3.1 |
| 5.5.2 | Integration Test Results | QA Automation | QA Automation | required | Automático |  |  | 5.5.1 |
| 5.5.3 | API Contract Tests | QA Automation | QA Automation | required | 1-2 días |  |  | 3B.4.1, 4.3.1 |
| 5.5.4 | Integration Coverage | QA Automation | QA Automation | required | 0.25 día |  |  | 5.5.1, 3B.4.2 |
| 5.6.1 | E2E Test Suite | QA Automation | QA Automation | required | 5-8 días |  |  | 5.3.1, 2.6.2 |
| 5.6.2 | E2E Test Results | QA Automation | QA Automation | required | Automático |  |  | 5.6.1 |
| 5.6.3 | Critical Path Coverage | QA Automation | QA Automation | required | 0.25 día |  |  | 5.6.1, 2.6.2 |
| 5.6.4 | Visual Regression | QA Automation | QA Automation | required | 1-2 días setup |  |  | 5.6.1 |
| 5.6.5 | E2E Documentation | QA Automation | QA Automation | required | 0.5 día |  |  | 5.6.1 |
| 5.7.1 | Load Test Plan | QA Automation | QA Automation | required | 1 día |  |  | 3B.4.2, 5.3.1 |
| 5.7.2 | Load Test Results | QA Automation | QA Automation | required | 1-2 días |  |  | 5.7.1, 5.3.1 |
| 5.7.3 | Stress Test Results | QA Automation | QA Automation | required | 1 día |  |  | 5.7.1, 5.7.2 |
| 5.7.4 | Performance Metrics | QA Automation | QA Automation | required | 0.5 día |  |  | 5.7.2 |
| 5.7.5 | Bottleneck Analysis | QA Automation | QA Automation / Tech Lead | required | 1 día |  |  | 5.7.2, 5.7.3 |
| 5.7.6 | Optimization Recommendations | QA Automation | Tech Lead | required | 0.5 día |  |  | 5.7.5 |
| 5.8.1 | Security Test Plan | Security Engineer | Security Engineer | required | 1 día |  |  | 3B.7.1, 3B.7.6 |
| 5.8.2 | Penetration Test Results | Security Engineer | Security Engineer / External pentester | required | 3-5 días |  |  | 5.8.1, 5.3.1 |
| 5.8.3 | Vulnerability Scan | Security Engineer | Security Engineer | required | 1 día |  |  | 5.8.1 |
| 5.8.4 | OWASP Compliance | Security Engineer | Security Engineer | required | 0.5 día |  |  | 3B.7.6, 5.8.2, 5.8.3 |
| 5.8.5 | Security Findings | Security Engineer | Security Engineer | required | 1 día |  |  | 5.8.2, 5.8.3, 5.8.4 |
| 5.8.6 | Remediation Plan | Security Engineer | Backend Developer / DevOps Lead | required | 0.5-1 día |  |  | 5.8.5 |
| 5.8.7 | Security Sign-off | Security Engineer | Security Engineer | required | 0.25 día |  |  | 5.8.6 |
| 5.9.1 | WCAG Audit | QA Engineer | QA Engineer | required | 2-3 días |  |  | 4.4.14, 5.3.1 |
| 5.9.2 | Accessibility Score | QA Engineer | QA Engineer | required | 0.25 día |  |  | 5.9.1 |
| 5.9.3 | Screen Reader Test | QA Engineer | QA Engineer | required | 1 día |  |  | 5.9.1, 4.4.14 |
| 5.9.4 | Keyboard Navigation | QA Engineer | QA Engineer | required | 0.5 día |  |  | 5.9.1, 4.4.14 |

### 06 — 6-Deploy

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 6.1.1 | Infrastructure Ready | DevOps Lead | DevOps Lead | required | 2-3 días |  |  | 3B.8.1, 5.8.7 |
| 6.1.2 | Servers Provisioned | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.1.1, 3B.8.3 |
| 6.1.3 | Network Configured | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.1.1, 3B.8.4 |
| 6.1.4 | Security Groups | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 6.1.3 |
| 6.1.5 | Load Balancer | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 6.1.2, 6.1.8 |
| 6.1.6 | Database Ready | DevOps Lead | DevOps Lead / Database Engineer | required | 0.5 día |  |  | 6.1.3, 6.1.4 |
| 6.1.7 | Storage Ready | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 6.1.1 |
| 6.1.8 | SSL Certificates | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 6.1.5 |
| 6.2.1 | CI Pipeline | DevOps Lead | DevOps Lead | required | 1-2 días |  |  | 4.1.9 |
| 6.2.2 | CD Pipeline | DevOps Lead | DevOps Lead | required | 1-2 días |  |  | 6.2.1, 6.1.1 |
| 6.2.3 | Build Scripts | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 3B.1.5 |
| 6.2.4 | Deploy Scripts | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.2.3, 6.1.1 |
| 6.2.5 | Environment Configs | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 3B.8.5, 4.1.3 |
| 6.2.6 | Pipeline Documentation | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.2.1, 6.2.2 |
| 6.3.1 | Staging Deploy | DevOps Lead | DevOps Lead (automático via CD) | required | Automático (15 min) |  |  | 6.2.2, 6.1.1 |
| 6.3.2 | Staging URL | DevOps Lead | DevOps Lead | required | Incluido |  |  | 6.3.1 |
| 6.3.3 | Migration Run | DevOps Lead | DevOps Lead | required | Automático |  |  | 6.3.1 |
| 6.3.4 | Health Check | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 6.3.1, 6.3.3 |
| 6.4.1 | Smoke Test Results | QA Engineer | QA Engineer | required | 0.5 día |  |  | 6.3.4 |
| 6.4.2 | Critical Paths Verified | QA Engineer | QA Engineer | required | Incluido en 6.4.1 |  |  | 6.4.1 |
| 6.4.3 | Smoke Test Sign-off | QA Lead | QA Lead | required | 0.25 día |  |  | 6.4.1, 6.4.2 |
| 6.5.1 | Production Deploy | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.4.3, 5.10.5, 5.8.7, 6.7.3 |
| 6.5.2 | Production URL | DevOps Lead | DevOps Lead | required | Incluido |  |  | 6.5.1, 6.5.3 |
| 6.5.3 | DNS Configured | DevOps Lead | DevOps Lead | required | 0.25 día |  |  | 6.1.5 |
| 6.5.4 | SSL Active | DevOps Lead | DevOps Lead | required | Incluido |  |  | 6.1.8, 6.5.1 |
| 6.5.5 | Release Notes | Tech Lead | Tech Lead / Technical Writer | required | 0.5 día |  |  | 4.7.8 |
| 6.5.6 | Deployment Log | DevOps Lead | DevOps Lead | required | Incluido |  |  | 6.5.1 |
| 6.6.1 | Monitoring Dashboard | SRE | SRE | required | 1 día |  |  | 6.5.1, 6.6.4 |
| 6.6.2 | Alerts Configured | SRE | SRE | required | 0.5 día |  |  | 6.6.1 |
| 6.6.3 | Log Aggregation | SRE | SRE | required | 0.5 día |  |  | 6.5.1, 4.3.15 |
| 6.6.4 | Metrics Collection | SRE | SRE | required | 0.5 día |  |  | 6.5.1 |
| 6.6.5 | Error Tracking | SRE | SRE | required | 0.25 día |  |  | 6.5.1 |
| 6.6.6 | Post-Deploy Report (24h) | SRE | SRE | required | 0.5 día |  |  | 6.5.1 |
| 6.7.1 | Rollback Plan | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.2.4, 4.2.10 |
| 6.7.2 | Rollback Scripts | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.7.1 |
| 6.7.3 | Rollback Tested | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.7.2, 6.3.1 |
| 6.7.4 | Rollback Runbook | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.7.1, 6.7.2 |
| 6.7.5 | Decision Criteria | Tech Lead | Tech Lead | required | 0.25 día |  |  | 3B.8.10 |

### 07 — 7-Operations

| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |
|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|
| 7.1.1 | Uptime Reports | SRE | SRE | required | Automático + 0.25 día review |  |  | 6.6.1, 3B.8.10 |
| 7.1.2 | Performance Reports | SRE | SRE | required | Automático + 0.25 día review |  |  | 6.6.1, 6.6.4 |
| 7.1.3 | Error Reports | SRE | SRE | required | Automático + 0.25 día review |  |  | 6.6.5 |
| 7.1.4 | Weekly Reports | SRE | SRE | required | 0.5 día |  |  | 7.1.1 |
| 7.2.1 | Support Process | Tech Lead | Tech Lead | required | 0.5 día |  |  |  |
| 7.2.2 | Ticket System | Tech Lead | DevOps Lead | required | 0.5 día |  |  | 7.2.1 |
| 7.2.3 | SLA Definitions | Tech Lead | Tech Lead | required | 0.5 día |  |  | 7.2.1 |
| 7.2.4 | Support Metrics | Tech Lead | SRE | required | 0.5 día setup + automático |  |  | 7.2.2, 7.2.3 |
| 7.3.1 | Hotfix Process | Tech Lead | Tech Lead | required | 0.5 día |  |  |  |
| 7.3.2 | Hotfix Releases | Developers | Developer asignado | required | Variable (por bug) |  |  | 7.3.1 |
| 7.3.3 | Bug Tracking | QA Lead | QA Lead | required | Continuo |  |  | 7.2.2 |
| 7.4.1 | Minor Releases | Tech Lead | Developers | required | Por sprint |  |  | 7.4.4 |
| 7.4.2 | Feature Flags | Tech Lead | Developers | required | 0.5 día setup + por feature |  |  |  |
| 7.4.3 | A/B Tests | Product Owner | Developers | required | Variable (por experimento) |  |  | 7.4.2 |
| 7.4.4 | Improvement Backlog | Product Owner | Product Owner | required | Continuo |  |  |  |
| 7.5.1 | Security Patches | Security Engineer | Developers | required | Variable (por vulnerabilidad) |  |  |  |
| 7.5.2 | Dependency Updates | Security Engineer | Developers | required | 0.5 día/mes |  |  |  |
| 7.5.3 | Security Audits | Security Engineer | Security Engineer / External Pentester | required | 3-5 días (por auditoría) |  |  |  |
| 7.5.4 | Vulnerability Reports | Security Engineer | Security Engineer | required | Automático + 0.25 día review |  |  |  |
| 7.6.1 | Scaling Reports | DevOps Lead | SRE | required | 0.5 día/mes |  |  | 6.6.4 |
| 7.6.2 | Capacity Planning | DevOps Lead | DevOps Lead | required | 1 día/trimestre |  |  | 7.6.1 |
| 7.6.3 | Auto-scaling Config | DevOps Lead | DevOps Lead | required | 0.5 día |  |  | 6.1.2, 7.6.1 |
| 7.6.4 | Cost Optimization | DevOps Lead | DevOps Lead | required | 0.5 día/mes |  |  | 7.6.1 |

---

## 6. Dependencias Trazadas

| From | To | Requirement | Notes |
|------|----|-------------|-------|
| 0.1.1 | 0.1.2 |  | provee datos base |
| 0.1.1 | 0.1.3 |  |  |
| 0.1.1 | 0.1.4 |  |  |
| 0.1.1 | 0.2.1 |  | necesita el contexto de mercado |
| 0.1.1 | 0.2.1 | recomendado |  |
| 0.1.1 | 0.3.1 |  | los pain points de mercado informan la definición del problema |
| 0.1.1 | 1.2.1 |  | el tamaño de oportunidad influye en el alcance del MVP |
| 0.1.2 | 0.1.4 |  |  |
| 0.1.2 | 0.1.5 | obligatorio |  |
| 0.1.2 | 0.4.1 |  |  |
| 0.1.2 | 1.6.1 |  |  |
| 0.1.2 | 1.6.4 |  |  |
| 0.1.2 | 1.6.4 | obligatorio |  |
| 0.1.3 | 0.2.6 |  |  |
| 0.1.3 | 0.2.6 | recomendado |  |
| 0.1.3 | 0.3.4 |  |  |
| 0.1.3 | 0.3.4 | obligatorio |  |
| 0.1.3 | 0.4.4 |  |  |
| 0.1.4 | 0.1.5 |  |  |
| 0.1.4 | 0.1.5 | obligatorio |  |
| 0.1.4 | 0.2.1 |  |  |
| 0.1.4 | 0.4.4 |  |  |
| 0.1.5 | 0.2.1 |  |  |
| 0.1.5 | 0.2.1 | obligatorio |  |
| 0.1.5 | 0.2.2 | obligatorio |  |
| 0.1.5 | 0.3.1 |  |  |
| 0.1.5 | 0.3.1 | obligatorio |  |
| 0.1.5 | 0.3.2 |  |  |
| 0.1.5 | 0.3.2 | obligatorio |  |
| 0.1.5 | 0.3.5 | obligatorio |  |
| 0.1.5 | 0.4.4 |  |  |
| 0.1.5 | 0.4.4 | obligatorio |  |
| 0.1.5 | 1.2.1 | obligatorio |  |
| 0.1.5 | 1.2.4 |  |  |
| 0.2.1 | 0.2.3 |  |  |
| 0.2.1 | 0.2.6 |  |  |
| 0.2.1 | 0.4.1 |  |  |
| 0.2.1 | 0.4.3 |  |  |
| 0.2.1 | 1.2.4 |  |  |
| 0.2.2 | 0.2.1 |  |  |
| 0.2.2 | 0.2.3 |  |  |
| 0.2.2 | 0.2.3 | obligatorio |  |
| 0.2.2 | 0.2.4 |  |  |
| 0.2.2 | 0.2.4 | obligatorio |  |
| 0.2.2 | 0.2.5 |  |  |
| 0.2.2 | 0.2.5 | obligatorio |  |
| 0.2.2 | 0.2.7 |  |  |
| 0.2.2 | 0.2.7 | obligatorio |  |
| 0.2.3 | 0.2.4 | recomendado |  |
| 0.2.3 | 0.2.5 | recomendado |  |
| 0.2.3 | 0.2.6 |  |  |
| 0.2.3 | 0.2.6 | obligatorio |  |
| 0.2.3 | 0.2.7 | recomendado |  |
| 0.2.3 | 0.4.3 |  |  |
| 0.2.3 | 0.4.3 | obligatorio |  |
| 0.2.3 | 1.2.4 |  |  |
| 0.2.3 | 2.1.1 |  |  |
| 0.2.4 | 0.4.1 |  |  |
| 0.2.4 | 1.6.1 |  |  |
| 0.2.4 | 1.6.4 |  |  |
| 0.2.5 | 0.2.6 |  |  |
| 0.2.5 | 0.2.6 | obligatorio |  |
| 0.2.5 | 0.4.3 |  |  |
| 0.2.6 | 0.4.1 |  |  |
| 0.2.6 | 0.4.3 |  |  |
| 0.2.6 | 1.2.4 |  |  |
| 0.2.7 | 3A.1.1 |  |  |
| 0.2.7 | 3A.3.1 |  |  |
| 0.2.7 | 3A.4.1 |  |  |
| 0.3.1 | 0.3.2 |  |  |
| 0.3.1 | 0.3.2 | obligatorio |  |
| 0.3.1 | 0.3.3 |  |  |
| 0.3.1 | 0.3.3 | obligatorio |  |
| 0.3.1 | 0.3.4 |  |  |
| 0.3.1 | 0.3.4 | obligatorio |  |
| 0.3.1 | 0.3.5 | obligatorio |  |
| 0.3.1 | 0.4.1 |  |  |
| 0.3.1 | 0.4.1 | obligatorio |  |
| 0.3.1 | 1.1.1 |  |  |
| 0.3.1 | 1.1.1 | obligatorio |  |
| 0.3.1 | 1.2.1 |  |  |
| 0.3.1 | 1.2.1 | obligatorio |  |
| 0.3.1 | 2.1.1 |  |  |
| 0.3.1 | 2.1.1 | obligatorio |  |
| 0.3.1 | 3A.1.1 | obligatorio | contexto del problema |
| 0.3.2 | 0.3.3 | recomendado |  |
| 0.3.2 | 0.3.5 |  |  |
| 0.3.2 | 0.3.5 | obligatorio |  |
| 0.3.2 | 0.4.1 |  |  |
| 0.3.2 | 0.4.1 | obligatorio |  |
| 0.3.2 | 0.4.4 | obligatorio |  |
| 0.3.2 | 2.1.1 |  |  |
| 0.3.2 | 3A.1.1 | recomendado | hipótesis a validar |
| 0.3.2 | 3A.1.2 |  |  |
| 0.3.3 | 0.4.1 |  |  |
| 0.3.3 | 0.4.2 |  |  |
| 0.3.3 | 1.2.4 |  |  |
| 0.3.4 | 0.4.1 |  |  |
| 0.3.4 | 1.1.1 |  |  |
| 0.3.5 | 0.4.1 |  | basado en problema validado |
| 0.3.5 | 0.4.1 | obligatorio |  |
| 0.3.5 | 0.4.5 | obligatorio |  |
| 0.3.5 | 1.2.4 |  |  |
| 0.4.1 | 0.4.2 |  |  |
| 0.4.1 | 0.4.2 | obligatorio |  |
| 0.4.1 | 0.4.3 |  |  |
| 0.4.1 | 0.4.3 | obligatorio |  |
| 0.4.1 | 0.4.5 |  |  |
| 0.4.1 | 0.4.5 | obligatorio |  |
| 0.4.1 | 1.2.4 |  |  |
| 0.4.1 | 2.1.1 |  |  |
| 0.4.2 | 1.1.1 |  |  |
| 0.4.2 | 1.1.1 | obligatorio |  |
| 0.4.2 | 3A.7.9 | recomendado | propuesta de valor informa personalidad de marca |
| 0.4.3 | 0.4.2 |  |  |
| 0.4.3 | 1.2.4 |  |  |
| 0.4.3 | 1.2.4 | obligatorio |  |
| 0.4.3 | 3B.1.1 |  |  |
| 0.4.4 | 1.3.4 |  |  |
| 0.4.4 | 2.6.5 | obligatorio |  |
| 0.4.4 | 3A.1.1 | obligatorio | audiencia target |
| 0.4.4 | 3A.1.2 |  |  |
| 0.4.4 | 3A.1.3 |  |  |
| 0.4.4 | 3A.2.5 | recomendado |  |
| 0.4.4 | 3A.7.9 | recomendado | audiencia informa tono visual |
| 0.4.5 | 1.1.4 |  |  |
| 0.4.5 | 1.1.4 | recomendado |  |
| 0.4.5 | 1.2.4 |  |  |
| 0.4.5 | 1.2.4 | obligatorio |  |
| 0.4.5 | 5.x |  |  |
| 1.1.1 | 1.1.2 |  | la misión operacionaliza la visión |
| 1.1.1 | 1.1.2 | obligatorio |  |
| 1.1.1 | 1.1.3 |  | objetivos concretos derivados de la visión |
| 1.1.1 | 1.1.3 | obligatorio |  |
| 1.1.1 | 1.2.1 |  | el alcance se define dentro de la visión |
| 1.1.2 | 1.1.3 |  |  |
| 1.1.2 | 1.1.3 | obligatorio |  |
| 1.1.2 | 1.2.1 |  |  |
| 1.1.3 | 1.1.4 |  | métricas para medir los goals |
| 1.1.3 | 1.1.4 | obligatorio |  |
| 1.1.3 | 1.1.6 |  | goals se convierten en OKRs |
| 1.1.3 | 1.1.6 | obligatorio |  |
| 1.1.3 | 1.2.1 |  | el alcance se define para lograr los goals |
| 1.1.3 | 1.2.1 | obligatorio |  |
| 1.1.4 | 1.1.5 |  | se selecciona de estos KPIs |
| 1.1.4 | 1.1.5 | obligatorio |  |
| 1.1.4 | 1.1.6 |  | los Key Results son KPIs |
| 1.1.4 | 1.1.6 | obligatorio |  |
| 1.1.4 | 6.6.1 |  | dashboard trackea estos KPIs |
| 1.1.5 | 6.6.1 |  | la métrica más prominente |
| 1.1.6 | 1.5.1 |  | los OKRs informan el timeline |
| 1.1.6 | 1.5.1 | obligatorio |  |
| 1.2.1 | 1.2.2 |  | detalle de lo incluido |
| 1.2.1 | 1.2.2 | obligatorio |  |
| 1.2.1 | 1.2.3 |  | detalle de lo excluido |
| 1.2.1 | 1.2.3 | obligatorio |  |
| 1.2.1 | 1.2.4 |  | MVP es un subconjunto del scope |
| 1.2.1 | 1.2.6 | obligatorio |  |
| 1.2.1 | 1.4.1 | obligatorio |  |
| 1.2.1 | 2.1.1 |  | requirements dentro del scope |
| 1.2.2 | 1.2.4 |  |  |
| 1.2.2 | 1.2.4 | obligatorio |  |
| 1.2.2 | 2.1.1 |  |  |
| 1.2.2 | 2.1.1 | obligatorio |  |
| 1.2.2 | 3B.1.1 | obligatorio | alcance del sistema |
| 1.2.2 | 3B.1.2 | recomendado | boundaries del sistema |
| 1.2.3 | 1.2.5 |  | algunos excluidos se convierten en roadmap |
| 1.2.3 | 1.2.5 | obligatorio |  |
| 1.2.4 | 1.5.1 |  | timeline del MVP |
| 1.2.4 | 1.5.1 | obligatorio |  |
| 1.2.4 | 2.1.1 |  | requirements del MVP |
| 1.2.4 | 2.1.1 | obligatorio |  |
| 1.2.4 | 2.4.1 |  | stories del MVP |
| 1.2.4 | 3B.1.1 |  | arquitectura para el MVP |
| 1.2.6 | 1.4.1 |  | cada supuesto es un riesgo potencial si falla |
| 1.2.6 | 1.4.1 | obligatorio |  |
| 1.2.6 | 3B.1.5 | recomendado | supuestos sobre tecnología |
| 1.3.1 | 1.3.2 |  | detalle de cada stakeholder |
| 1.3.1 | 1.3.2 | obligatorio |  |
| 1.3.1 | 1.3.3 |  | responsabilidades formales |
| 1.3.1 | 1.3.4 |  | estrategia por stakeholder |
| 1.3.1 | 1.3.4 | obligatorio |  |
| 1.3.2 | 1.3.3 |  |  |
| 1.3.2 | 1.3.3 | obligatorio |  |
| 1.3.2 | 1.3.4 |  |  |
| 1.3.3 | 1.3.4 |  |  |
| 1.3.3 | 1.3.4 | obligatorio |  |
| 1.3.3 | 1.6.3 | obligatorio |  |
| 1.3.4 | 7.2.1 |  | base para comunicación con usuarios |
| 1.4.1 | 1.4.2 |  | evaluación formal |
| 1.4.1 | 1.4.2 | obligatorio |  |
| 1.4.1 | 1.4.3 |  |  |
| 1.4.1 | 1.4.4 |  |  |
| 1.4.1 | 1.4.5 | obligatorio |  |
| 1.4.1 | 3B.1.1 | recomendado | riesgos técnicos a mitigar en la arquitectura |
| 1.4.1 | 3B.1.5 | recomendado | riesgos técnicos que influyen en elección |
| 1.4.1 | 3B.9.6 | recomendado |  |
| 1.4.2 | 1.4.3 |  | para los riesgos altos |
| 1.4.2 | 1.4.3 | obligatorio |  |
| 1.4.2 | 1.4.4 |  | para los riesgos críticos |
| 1.4.2 | 1.4.4 | obligatorio |  |
| 1.4.3 | 1.4.5 |  |  |
| 1.4.4 | 6.7.1 |  | contingencia específica de deploy |
| 1.5.1 | 1.5.2 |  |  |
| 1.5.1 | 1.5.2 | obligatorio |  |
| 1.5.1 | 1.5.3 | obligatorio |  |
| 1.5.1 | 1.5.4 |  |  |
| 1.5.1 | 1.5.4 | obligatorio |  |
| 1.5.1 | 1.5.5 |  |  |
| 1.5.1 | 1.5.5 | obligatorio |  |
| 1.5.1 | 1.5.6 |  |  |
| 1.5.1 | 1.6.1 | obligatorio |  |
| 1.5.1 | 1.6.3 | obligatorio |  |
| 1.5.4 | 2.4.6 |  | stories asignadas a sprints del calendario |
| 1.5.4 | 2.4.6 | obligatorio |  |
| 1.5.5 | 1.5.6 |  | se calcula a partir de las dependencias |
| 1.5.5 | 1.5.6 | obligatorio |  |
| 1.5.6 | 1.5.7 |  | buffer en el critical path |
| 1.5.6 | 1.5.7 | obligatorio |  |
| 1.6.1 | 1.6.2 |  |  |
| 1.6.1 | 1.6.2 | obligatorio |  |
| 1.6.1 | 1.6.4 |  |  |
| 1.6.1 | 1.6.4 | obligatorio |  |
| 1.6.1 | 1.6.5 |  |  |
| 1.6.1 | 1.6.5 | obligatorio |  |
| 1.6.3 | 1.6.1 | obligatorio |  |
| 1.6.3 | 1.6.1 |  | costos de personal |
| 1.6.4 | 1.6.5 |  | tracking contra lo proyectado |
| 2.1.1 | 2.1.2 |  | lista derivada del SRS |
| 2.1.1 | 2.1.2 | obligatorio |  |
| 2.1.1 | 2.1.3 |  | priorización de requisitos |
| 2.1.1 | 2.1.6 | obligatorio |  |
| 2.1.1 | 2.2.1 | obligatorio |  |
| 2.1.1 | 2.3.1 |  | use cases implementan los requisitos |
| 2.1.1 | 2.3.1 | obligatorio |  |
| 2.1.1 | 2.5.1 | obligatorio |  |
| 2.1.1 | 2.7.1 | obligatorio |  |
| 2.1.1 | 3B.1.1 |  | la arquitectura soporta los requisitos |
| 2.1.1 | 5.1.1 |  | los tests validan los requisitos |
| 2.1.2 | 2.1.3 |  |  |
| 2.1.2 | 2.1.3 | obligatorio |  |
| 2.1.2 | 2.1.4 | obligatorio |  |
| 2.1.2 | 2.8.1 |  | mapeo RF a todo lo demás |
| 2.1.2 | 2.8.1 | obligatorio |  |
| 2.1.3 | 2.1.6 | obligatorio |  |
| 2.1.3 | 2.4.1 |  | prioridad informa el backlog |
| 2.1.4 | 2.1.5 |  |  |
| 2.1.4 | 2.1.5 | obligatorio |  |
| 2.1.4 | 2.4.4 |  | features se convierten en epics |
| 2.1.5 | 2.4.4 |  | los módulos pueden mapearse a epics |
| 2.1.5 | 3B.1.1 |  | la descomposición funcional informa los componentes |
| 2.1.6 | 2.4.1 |  | baseline para crear stories |
| 2.1.6 | 2.4.1 | obligatorio |  |
| 2.2.1 | 2.2.2 |  | secciones detalladas por categoría |
| 2.2.1 | 3B.1.1 |  | los NFRs determinan la arquitectura |
| 2.2.1 | 5.3.1 |  | tests validan los NFRs |
| 2.3.1 | 2.3.2 |  |  |
| 2.3.1 | 2.3.4 |  |  |
| 2.3.1 | 2.4.1 | obligatorio |  |
| 2.3.1 | 2.4.2 |  | stories se derivan de use cases |
| 2.3.1 | 2.7.2 |  |  |
| 2.3.1 | 5.2.1 |  | tests basados en use cases |
| 2.3.3 | 2.8.1 | obligatorio |  |
| 2.3.3 | 3A.3.1 | obligatorio | funcionalidades a incluir |
| 2.3.4 | 2.4.2 |  | cada use case genera 1+ stories |
| 2.3.4 | 2.4.2 | obligatorio |  |
| 2.3.4 | 2.5.1 | recomendado |  |
| 2.3.4 | 2.6.1 | obligatorio |  |
| 2.3.4 | 2.7.1 | obligatorio |  |
| 2.3.4 | 2.7.5 |  | cada flujo es un test scenario |
| 2.3.4 | 3A.4.7 | obligatorio |  |
| 2.3.4 | 3B.1.1 | obligatorio | requisitos funcionales |
| 2.3.4 | 3B.1.4 | obligatorio | funcionalidades a mapear a componentes |
| 2.3.4 | 3B.1.6 | recomendado | qué funcionalidades requieren integraciones |
| 2.3.4 | 3B.1.7 | recomendado | flujos principales |
| 2.3.4 | 3B.3.1 | obligatorio | entidades derivadas de funcionalidad |
| 2.3.4 | 3B.4.1 | recomendado | operaciones de negocio |
| 2.3.4 | 3B.4.2 | obligatorio | funcionalidades a exponer |
| 2.3.4 | 3B.5.3 | obligatorio | flujos fuente |
| 2.3.4 | 5.1.1 | obligatorio |  |
| 2.3.4 | 5.2.1 |  |  |
| 2.3.4 | 5.2.1 | obligatorio |  |
| 2.3.5 | 2.5.5 | obligatorio |  |
| 2.3.5 | 3B.1.2 | obligatorio | actores del diagrama |
| 2.3.5 | 3B.4.7 | obligatorio | roles del sistema |
| 2.4.1 | 2.4.2 |  | cada ítem se detalla |
| 2.4.1 | 2.4.2 | obligatorio |  |
| 2.4.1 | 2.4.3 |  |  |
| 2.4.1 | 3B.9.2 | obligatorio | stories a estimar |
| 2.4.1 | 3B.9.3 | obligatorio |  |
| 2.4.2 | 2.4.5 |  |  |
| 2.4.2 | 2.7.2 |  |  |
| 2.4.2 | 2.7.2 | obligatorio |  |
| 2.4.4 | 3B.9.4 | obligatorio |  |
| 2.4.5 | 2.4.6 | obligatorio |  |
| 2.4.5 | 3B.9.1 | obligatorio | estimaciones iniciales |
| 2.5.1 | 2.4.2 |  | stories referencian reglas (BR-XXX) |
| 2.5.1 | 2.5.2 |  | reglas detalladas por tipo |
| 2.5.1 | 2.5.5 | obligatorio |  |
| 2.5.1 | 3B.1.1 | obligatorio | reglas de negocio que afectan diseño |
| 2.5.1 | 3B.3.1 | obligatorio | constraints del modelo |
| 2.5.1 | 3B.3.3 | recomendado |  |
| 2.5.1 | 3B.4.5 | recomendado | business errors |
| 2.5.1 | 3B.5.3 | recomendado | validaciones en el flujo |
| 2.5.1 | 3B.9.5 | recomendado |  |
| 2.5.1 | 4.3.2 | obligatorio | lógica a implementar |
| 2.5.1 | 4.x |  | developers implementan las reglas |
| 2.5.3 | 3B.4.5 | recomendado | validation errors |
| 2.5.3 | 3B.7.9 | obligatorio | reglas de negocio |
| 2.5.5 | 3B.3.7 | recomendado | roles y permisos como seed |
| 2.5.5 | 3B.4.2 | recomendado | permisos por endpoint |
| 2.5.5 | 3B.4.7 | obligatorio | reglas de negocio de permisos |
| 2.5.7 | 3B.2.5 | recomendado | vocabulario de dominio estandarizado |
| 2.5.7 | 3B.3.5 | recomendado | vocabulario estandarizado |
| 2.6.1 | 2.6.2 |  | flujos específicos |
| 2.6.1 | 2.6.5 | obligatorio |  |
| 2.6.1 | 3A.3.1 |  | se deriva de los flujos |
| 2.6.1 | 3A.4.8 | obligatorio | flujos de referencia |
| 2.6.1 | 3A.4.x |  | los wireframes implementan los flujos |
| 2.6.1 | 3A.6.1 | obligatorio | flujos a prototipar |
| 2.6.1 | 3A.8.1 | obligatorio | flujos a evaluar |
| 2.6.2 | 3A.6.2 | obligatorio |  |
| 2.6.2 | 3A.8.1 | recomendado | base para definir tareas |
| 2.6.2 | 5.6.1 | obligatorio |  |
| 2.6.2 | 5.6.3 | obligatorio |  |
| 2.7.1 | 2.7.2 |  | criterios específicos |
| 2.7.1 | 5.2.1 |  | se derivan de los AC |
| 2.8.1 | 2.8.4 |  |  |
| 3A.1.1 | 3A.1.2 |  | resultados del plan ejecutado |
| 3A.1.1 | 3A.1.2 | obligatorio | plan que se ejecutó |
| 3A.1.1 | 3A.1.3 |  | guía derivada del plan |
| 3A.1.1 | 3A.1.3 | obligatorio | preguntas de investigación |
| 3A.1.1 | 3A.1.5 |  | survey derivada del plan |
| 3A.1.1 | 3A.1.5 | obligatorio | survey planificado |
| 3A.1.2 | 3A.1.6 |  | insights extraídos del reporte |
| 3A.1.2 | 3A.1.6 | obligatorio | insights extraídos del reporte |
| 3A.1.2 | 3A.1.7 |  | puntos de dolor validados |
| 3A.1.2 | 3A.1.7 | obligatorio | fuente de pain points validados |
| 3A.1.2 | 3A.1.8 |  | necesidades identificadas |
| 3A.1.2 | 3A.1.8 | obligatorio |  |
| 3A.1.2 | 3A.1.9 |  | patrones de comportamiento |
| 3A.1.2 | 3A.1.9 | obligatorio |  |
| 3A.1.2 | 3A.2.1 |  | personas basadas en research |
| 3A.1.2 | 3A.2.1 | obligatorio | base empírica |
| 3A.1.2 | 3A.2.7 | obligatorio | datos empíricos |
| 3A.1.3 | 3A.1.2 |  | datos producidos con la guía |
| 3A.1.3 | 3A.1.4 |  | entrevistas ejecutadas con la guía |
| 3A.1.3 | 3A.1.4 | obligatorio | guía usada en las entrevistas |
| 3A.1.4 | 3A.1.2 | obligatorio | datos de entrevistas |
| 3A.1.4 | 3A.1.2 |  | análisis de transcripciones |
| 3A.1.4 | 3A.1.6 |  | insights extraídos |
| 3A.1.4 | 3A.1.9 |  | patrones identificados en transcripciones |
| 3A.1.4 | 3A.1.9 | obligatorio |  |
| 3A.1.5 | 3A.1.2 | recomendado | datos cuantitativos |
| 3A.1.5 | 3A.1.2 |  | datos cuantitativos del reporte |
| 3A.1.5 | 3A.1.6 |  | insights cuantitativos |
| 3A.1.5 | 3A.1.7 |  | puntos de dolor cuantificados |
| 3A.1.6 | 3A.1.8 | recomendado |  |
| 3A.1.6 | 3A.2.1 |  | insights informan personas |
| 3A.1.6 | 3A.3.1 |  | insights sobre mental models informan IA |
| 3A.1.6 | 3A.4.1 |  | insights guían diseño de pantallas |
| 3A.1.7 | 1.2.4 |  | features que resuelven top pain points |
| 3A.1.7 | 3A.2.1 |  | pain points por persona |
| 3A.1.7 | 3A.2.1 | obligatorio | frustraciones |
| 3A.1.7 | 3A.2.8 |  | pain points informan JTBD |
| 3A.1.8 | 2.4.1 |  | user stories que abordan necesidades |
| 3A.1.8 | 3A.2.6 |  | escenarios que satisfacen necesidades |
| 3A.1.8 | 3A.2.6 | obligatorio |  |
| 3A.1.8 | 3A.2.8 |  | JTBD derivados de necesidades |
| 3A.1.8 | 3A.2.8 | obligatorio |  |
| 3A.1.9 | 3A.2.1 |  | personas basadas en patrones de comportamiento |
| 3A.1.9 | 3A.2.1 | obligatorio | segmentación |
| 3A.1.9 | 3A.2.6 |  | escenarios basados en comportamiento real |
| 3A.1.9 | 3A.3.2 |  | navegación alineada a patrones |
| 3A.1.9 | 3A.4.8 |  | flujos basados en comportamiento real |
| 3A.2.1 | 3A.2.2 |  | cards visuales derivadas |
| 3A.2.1 | 3A.2.2 | obligatorio |  |
| 3A.2.1 | 3A.2.3 |  | persona principal seleccionada |
| 3A.2.1 | 3A.2.3 | obligatorio |  |
| 3A.2.1 | 3A.2.4 | obligatorio |  |
| 3A.2.1 | 3A.2.5 | obligatorio |  |
| 3A.2.1 | 3A.2.6 |  | escenarios por persona |
| 3A.2.1 | 3A.2.6 | obligatorio |  |
| 3A.2.1 | 3A.2.7 |  | mapas de empatía |
| 3A.2.1 | 3A.2.7 | obligatorio |  |
| 3A.2.1 | 3A.2.8 |  | JTBD por persona |
| 3A.2.1 | 3A.2.8 | obligatorio |  |
| 3A.2.1 | 3A.3.1 |  | IA diseñada para la persona primaria |
| 3A.2.1 | 3A.8.1 | obligatorio | criterios de reclutamiento |
| 3A.2.1 | 3A.8.3 |  | criterios de reclutamiento para testing |
| 3A.2.1 | 3A.8.3 | obligatorio | base para criterios demográficos |
| 3A.2.3 | 3A.2.4 | obligatorio | definida primero para diferenciar |
| 3A.2.3 | 3A.3.1 |  | IA optimizada para la primaria |
| 3A.2.3 | 3A.3.1 | obligatorio | mental model del usuario |
| 3A.2.3 | 3A.3.6 | obligatorio | perfil de participantes |
| 3A.2.3 | 3A.4.1 |  | wireframes diseñados para la primaria |
| 3A.2.3 | 3A.8.3 |  | reclutamiento prioriza perfil de la primaria |
| 3A.2.3 | 3A.8.3 | obligatorio | perfil prioritario |
| 3A.2.4 | 3A.2.6 |  | escenarios específicos por persona secundaria |
| 3A.2.4 | 3A.2.7 |  | mapas por persona |
| 3A.2.5 | 3A.8.3 |  | exclusión en reclutamiento |
| 3A.2.6 | 2.4.2 |  | escenarios informan stories |
| 3A.2.6 | 3A.2.8 | recomendado |  |
| 3A.2.6 | 3A.4.8 |  | flujos diseñados para escenarios |
| 3A.2.6 | 3A.8.2 |  | escenarios como base de tareas de testing |
| 3A.2.7 | 3A.4.1 |  | diseño empático |
| 3A.2.8 | 1.2.4 |  | features que resuelven top jobs |
| 3A.2.8 | 2.4.2 |  | stories derivadas de JTBD |
| 3A.3.1 | 3A.3.2 |  | navegación derivada del sitemap |
| 3A.3.1 | 3A.3.2 | obligatorio |  |
| 3A.3.1 | 3A.3.4 | obligatorio |  |
| 3A.3.1 | 3A.3.7 |  | menús basados en la jerarquía |
| 3A.3.1 | 3A.3.7 | obligatorio |  |
| 3A.3.1 | 3A.3.8 |  | URLs derivadas del sitemap |
| 3A.3.1 | 3A.3.8 | obligatorio |  |
| 3A.3.1 | 3A.4.1 |  | pantallas a wireframear |
| 3A.3.1 | 3A.4.1 | obligatorio | estructura del producto |
| 3A.3.1 | 3A.4.2 | obligatorio | pantallas identificadas |
| 3A.3.2 | 3A.3.3 |  | patrones de UI elegidos |
| 3A.3.2 | 3A.3.3 | obligatorio |  |
| 3A.3.2 | 3A.3.7 |  | menús como implementación |
| 3A.3.2 | 3A.3.7 | obligatorio |  |
| 3A.3.2 | 3A.4.1 |  | navegación en wireframes |
| 3A.3.2 | 3A.4.2 | obligatorio | navegación definida |
| 3A.3.2 | 3A.4.3 | obligatorio | navegación |
| 3A.3.2 | 4.4.3 | obligatorio |  |
| 3A.3.3 | 3A.4.1 |  | patterns aplicados en wireframes |
| 3A.3.3 | 3A.4.5 | obligatorio | nav mobile definida |
| 3A.3.3 | 3A.7.8 |  | patterns de navegación incluidos |
| 3A.3.3 | 3A.7.8 | recomendado | patterns de navegación |
| 3A.3.3 | 4.4.3 |  | layouts implementan los patterns |
| 3A.3.4 | 3A.3.5 |  | categorización del contenido |
| 3A.3.4 | 3A.3.5 | obligatorio |  |
| 3A.3.4 | 3A.3.6 | obligatorio | items para las cards |
| 3A.3.4 | 3A.4.3 | recomendado | contenido real |
| 3A.3.4 | 3A.4.7 |  | contenido en wireframes |
| 3A.3.5 | 3A.3.7 |  | categorías como ítems de menú |
| 3A.3.5 | 3B.3.5 |  | taxonomía reflejada en la BD |
| 3A.3.5 | 4.4.1 |  | filtros y categorías en UI |
| 3A.3.6 | 3A.3.1 | recomendado | organización validada |
| 3A.3.6 | 3A.3.1 |  | estructura validada |
| 3A.3.6 | 3A.3.5 | recomendado |  |
| 3A.3.6 | 3A.3.5 |  | categorías validadas |
| 3A.3.6 | 3A.3.7 |  | menú basado en agrupación del usuario |
| 3A.3.7 | 3A.4.1 |  | menú en wireframes |
| 3A.3.7 | 3A.7.8 |  | menú como pattern |
| 3A.3.7 | 4.4.3 |  | componente de menú implementado |
| 3A.3.8 | 3B.4.2 |  | consistencia con API paths |
| 3A.3.8 | 4.4.4 |  | implementación de rutas frontend |
| 3A.4.1 | 3A.5.1 |  | mockups basados en wireframes aprobados |
| 3A.4.2 | 3A.4.1 | obligatorio |  |
| 3A.4.2 | 3A.4.3 |  | versión refinada del layout elegido |
| 3A.4.2 | 3A.4.3 | obligatorio | layout aprobado |
| 3A.4.3 | 3A.4.1 | obligatorio |  |
| 3A.4.3 | 3A.4.4 |  | wireframes desktop derivados |
| 3A.4.3 | 3A.4.4 | obligatorio |  |
| 3A.4.3 | 3A.4.5 |  | wireframes mobile derivados |
| 3A.4.3 | 3A.4.5 | obligatorio |  |
| 3A.4.3 | 3A.4.7 |  | anotaciones sobre mid-fi |
| 3A.4.3 | 3A.4.7 | obligatorio |  |
| 3A.4.3 | 3A.4.8 |  | flujos conectados |
| 3A.4.3 | 3A.4.8 | obligatorio |  |
| 3A.4.3 | 3A.5.1 |  | base para mockups |
| 3A.4.3 | 3A.5.1 | obligatorio | estructura aprobada |
| 3A.4.4 | 3A.4.6 | obligatorio |  |
| 3A.4.4 | 3A.4.8 |  | flujos desktop |
| 3A.4.4 | 3A.4.9 | obligatorio |  |
| 3A.4.4 | 3A.5.2 |  | mockups desktop basados en wireframes |
| 3A.4.4 | 3A.5.2 | obligatorio |  |
| 3A.4.5 | 3A.4.6 | obligatorio |  |
| 3A.4.5 | 3A.4.8 |  | flujos mobile |
| 3A.4.5 | 3A.4.9 | obligatorio |  |
| 3A.4.5 | 3A.5.3 |  | mockups mobile |
| 3A.4.5 | 3A.5.3 | obligatorio |  |
| 3A.4.6 | 3A.5.4 |  | mockups tablet |
| 3A.4.6 | 3A.5.4 | obligatorio |  |
| 3A.4.7 | 3A.5.1 |  | comportamiento documentado para mockups |
| 3A.4.7 | 3A.5.1 | obligatorio | comportamientos |
| 3A.4.7 | 3A.9.1 |  | anotaciones se heredan al handoff |
| 3A.4.7 | 4.4.1 |  | developers entienden el comportamiento |
| 3A.4.8 | 3A.5.1 |  | flujos a mockupear |
| 3A.4.8 | 3A.6.1 |  | prototipo basado en flujos |
| 3A.4.8 | 3A.6.1 | obligatorio | secuencia de pantallas |
| 3A.4.8 | 3A.8.2 |  | flujos como base de tareas de testing |
| 3A.4.9 | 3A.5.10 |  | mockups por breakpoint |
| 3A.4.9 | 3A.5.10 | obligatorio |  |
| 3A.4.9 | 3A.7.4 |  | spacing responsive |
| 3A.4.9 | 3A.7.4 | recomendado | ajustes responsive del spacing |
| 3A.4.9 | 3A.9.5 |  | medidas por breakpoint |
| 3A.4.9 | 4.4.15 |  | implementación frontend |
| 3A.4.9 | 4.4.15 | obligatorio |  |
| 3A.5.1 | 3A.5.2 |  | versiones específicas derivadas |
| 3A.5.1 | 3A.5.5 | obligatorio |  |
| 3A.5.1 | 3A.5.6 | obligatorio |  |
| 3A.5.1 | 3A.5.7 | obligatorio |  |
| 3A.5.1 | 3A.5.8 | obligatorio |  |
| 3A.5.1 | 3A.5.9 | obligatorio |  |
| 3A.5.1 | 3A.6.1 |  | prototipo basado en mockups |
| 3A.5.1 | 3A.6.1 | obligatorio | mockups finales |
| 3A.5.1 | 3A.6.4 | obligatorio |  |
| 3A.5.1 | 3A.7.1 |  | tokens extraídos de mockups |
| 3A.5.1 | 3A.7.1 | obligatorio | los mockups contienen los valores que se extraen |
| 3A.5.1 | 3A.7.10 | obligatorio | assets usados en diseños |
| 3A.5.1 | 3A.7.2 | obligatorio | colores validados visualmente |
| 3A.5.1 | 3A.7.3 | obligatorio | tipografía validada visualmente |
| 3A.5.1 | 3A.7.4 | obligatorio | spacing validado visualmente |
| 3A.5.1 | 3A.7.5 | obligatorio | inventario de iconos necesarios |
| 3A.5.1 | 3A.7.6 |  | componentes extraídos |
| 3A.5.1 | 3A.7.6 | obligatorio |  |
| 3A.5.1 | 3A.7.8 | obligatorio | patterns extraídos de diseños |
| 3A.5.1 | 3A.8.1 |  | mockups como objeto de test |
| 3A.5.1 | 3A.8.6 | obligatorio | diseños que se iteran |
| 3A.5.1 | 3A.9.1 |  | mockups como entregable a dev |
| 3A.5.1 | 3A.9.1 | obligatorio | mockups que se entregan |
| 3A.5.1 | 3A.9.2 | obligatorio | mockups finales |
| 3A.5.1 | 3A.9.5 | obligatorio | mockups finales |
| 3A.5.10 | 3A.9.1 |  | responsive behavior documentado |
| 3A.5.10 | 3A.9.5 |  | medidas por breakpoint |
| 3A.5.10 | 4.4.15 |  | implementación |
| 3A.5.10 | 4.4.15 | obligatorio |  |
| 3A.5.2 | 3A.5.10 | obligatorio |  |
| 3A.5.2 | 3A.6.1 |  | prototipo desktop |
| 3A.5.2 | 3A.9.2 |  | specs desktop |
| 3A.5.3 | 3A.5.10 | obligatorio |  |
| 3A.5.3 | 3A.6.1 |  | prototipo mobile |
| 3A.5.3 | 3A.9.2 |  | specs mobile |
| 3A.5.4 | 3A.9.2 |  | specs tablet |
| 3A.5.5 | 3A.6.4 | obligatorio | estados a transicionar |
| 3A.5.5 | 3A.7.6 |  | variants de states |
| 3A.5.5 | 3A.7.6 | obligatorio | define todos los estados |
| 3A.5.5 | 3A.9.2 |  | specs de states |
| 3A.5.5 | 4.4.1 |  | implementación de states CSS |
| 3A.5.6 | 3A.7.8 |  | empty state como pattern |
| 3A.5.6 | 4.4.1 |  | empty state components |
| 3A.5.7 | 3A.7.8 |  | error patterns |
| 3A.5.7 | 3B.2.6 |  | visual alignment |
| 3A.5.7 | 4.4.1 |  | error components |
| 3A.5.8 | 3A.7.8 |  | loading patterns |
| 3A.5.8 | 4.4.1 |  | loading components |
| 3A.5.9 | 3A.7.1 |  | tokens dark theme |
| 3A.5.9 | 3A.9.4 |  | dark mode CSS variables |
| 3A.6.1 | 3A.6.2 |  | flujo principal como subset |
| 3A.6.1 | 3A.6.2 | obligatorio |  |
| 3A.6.1 | 3A.6.3 |  | flujos secundarios |
| 3A.6.1 | 3A.6.3 | obligatorio |  |
| 3A.6.1 | 3A.6.5 |  | links compartibles |
| 3A.6.1 | 3A.6.5 | obligatorio |  |
| 3A.6.1 | 3A.6.6 | obligatorio |  |
| 3A.6.1 | 3A.8.1 |  | prototipo como objeto de testing |
| 3A.6.1 | 3A.8.1 | obligatorio | sin prototipo no hay qué testear |
| 3A.6.1 | 3A.8.2 |  | tareas basadas en el prototipo |
| 3A.6.1 | 3A.8.2 | obligatorio | el script referencia pantallas del prototipo |
| 3A.6.1 | 3A.9.1 | obligatorio | referencia de flujos |
| 3A.6.2 | 3A.6.3 | obligatorio | el main flow se protutipa primero |
| 3A.6.2 | 3A.8.2 |  | main flow como primera tarea de testing |
| 3A.6.3 | 3A.8.2 |  | tareas de testing secundarias |
| 3A.6.4 | 3A.7.1 |  | animation tokens (duration, easing) |
| 3A.6.4 | 3A.9.1 |  | animaciones documentadas para dev |
| 3A.6.4 | 4.4.1 |  | implementación de animaciones CSS/JS |
| 3A.6.5 | 3A.6.6 | obligatorio |  |
| 3A.6.5 | 3A.8.2 |  | links para participantes de testing |
| 3A.6.5 | 3A.8.2 | obligatorio | links para que el participante acceda |
| 3A.6.6 | 3A.8.2 |  | moderador conoce limitaciones |
| 3A.7.1 | 3A.7.6 |  | los componentes consumen tokens |
| 3A.7.1 | 3A.7.6 | obligatorio | componentes consumen tokens |
| 3A.7.1 | 3A.7.7 | recomendado | referencia de tokens en docs |
| 3A.7.1 | 3A.9.2 | obligatorio | specs deben reflejar tokens, no valores hardcoded |
| 3A.7.1 | 3A.9.4 |  | exportación directa de tokens a CSS |
| 3A.7.1 | 3A.9.4 | obligatorio | fuente de las variables |
| 3A.7.1 | 4.4.1 |  | componentes React referencian tokens |
| 3A.7.1 | 4.4.8 |  | desarrollo frontend consume tokens |
| 3A.7.10 | 3A.9.3 |  | assets listos para handoff a desarrollo |
| 3A.7.10 | 3A.9.3 | obligatorio | fuente de assets |
| 3A.7.10 | 4.4.1 |  | frontend consume assets |
| 3A.7.10 | 4.4.8 |  | imágenes y recursos referenciados |
| 3A.7.2 | 3A.5.9 | obligatorio | paleta dark definida |
| 3A.7.2 | 3A.5.9 |  | paleta dark derivada de la paleta light |
| 3A.7.2 | 3A.7.1 | obligatorio | colores como tokens primitivos |
| 3A.7.2 | 3A.7.1 |  | colores se convierten en tokens |
| 3A.7.2 | 3A.7.5 | recomendado | colores aplicados a iconos |
| 3A.7.2 | 3A.7.6 |  | componentes usan la paleta |
| 3A.7.2 | 3A.7.6 | obligatorio |  |
| 3A.7.2 | 3A.7.8 |  | patrones referencian colores semánticos |
| 3A.7.2 | 3A.7.9 | obligatorio | colores de la marca |
| 3A.7.2 | 3A.9.4 | obligatorio | tokens de color |
| 3A.7.3 | 3A.7.1 | obligatorio | tipografía tokenizada |
| 3A.7.3 | 3A.7.1 |  | tipografía tokenizada |
| 3A.7.3 | 3A.7.6 |  | componentes usan la escala |
| 3A.7.3 | 3A.7.6 | obligatorio |  |
| 3A.7.3 | 3A.7.7 |  | documentación referencia la escala |
| 3A.7.3 | 3A.7.9 | obligatorio | tipografía de la marca |
| 3A.7.3 | 3A.9.4 | obligatorio | tokens de tipografía |
| 3A.7.3 | 4.4.8 |  | frontend implementa la escala |
| 3A.7.4 | 3A.7.1 | obligatorio | espaciado tokenizado |
| 3A.7.4 | 3A.7.1 |  | spacing tokenizado |
| 3A.7.4 | 3A.7.5 | recomendado | tamaños de icono alineados al spacing |
| 3A.7.4 | 3A.7.6 |  | componentes usan spacing del sistema |
| 3A.7.4 | 3A.7.6 | obligatorio |  |
| 3A.7.4 | 3A.9.4 | obligatorio | tokens de spacing |
| 3A.7.4 | 3A.9.5 | obligatorio | redlines deben usar valores del spacing system |
| 3A.7.4 | 4.4.8 |  | frontend usa spacing scale (e.g., Tailwind spacing) |
| 3A.7.5 | 3A.7.10 |  | iconos como parte de assets exportables |
| 3A.7.5 | 3A.7.10 | obligatorio | iconos como assets |
| 3A.7.5 | 3A.7.6 |  | componentes que incluyen iconos |
| 3A.7.5 | 3A.7.6 | obligatorio |  |
| 3A.7.5 | 3A.9.3 |  | SVGs listos para desarrollo |
| 3A.7.5 | 3A.9.3 | obligatorio | iconos a exportar |
| 3A.7.5 | 4.4.1 |  | componentes React consumen iconos |
| 3A.7.6 | 3A.7.7 |  | documentación de cada componente |
| 3A.7.6 | 3A.7.7 | obligatorio | componentes construidos antes de documentar |
| 3A.7.6 | 3A.7.8 |  | patrones compuestos por componentes |
| 3A.7.6 | 3A.7.8 | obligatorio | patterns se construyen con componentes |
| 3A.7.6 | 3A.9.1 |  | referencia de componentes para devs |
| 3A.7.6 | 3A.9.1 | obligatorio | componentes a usar |
| 3A.7.6 | 3A.9.2 |  | specs exportadas de componentes |
| 3A.7.6 | 3A.9.2 | obligatorio | componentes bien estructurados para inspect |
| 3A.7.6 | 4.4.1 |  | implementación React de los componentes |
| 3A.7.6 | 4.4.1 | obligatorio | referencia visual |
| 3A.7.6 | 4.4.12 |  | stories basadas en variantes de Figma |
| 3A.7.7 | 3A.9.1 |  | referencia de componentes para handoff |
| 3A.7.7 | 3A.9.1 | recomendado | docs de apoyo |
| 3A.7.7 | 4.4.1 |  | devs consultan docs al implementar |
| 3A.7.7 | 4.4.12 |  | stories alineadas a la documentación de diseño |
| 3A.7.8 | 3A.7.7 |  | docs referencian patterns |
| 3A.7.8 | 3A.9.1 |  | patterns como referencia para devs |
| 3A.7.8 | 4.4.2 |  | pages implementan patterns |
| 3A.7.9 | 3A.7.1 |  | tokens alineados a brand |
| 3A.7.9 | 3A.7.10 |  | assets de marca exportables |
| 3A.7.9 | 3A.7.10 | obligatorio | logo y assets de marca |
| 3A.7.9 | 3A.7.2 | recomendado | si existe branding previo, la paleta debe alinearse |
| 3A.7.9 | 3A.7.3 | recomendado | fuentes de marca |
| 3A.7.9 | 3A.7.6 |  | componentes siguen brand guidelines |
| 3A.8.1 | 3A.8.2 |  | guión basado en el plan |
| 3A.8.1 | 3A.8.2 | obligatorio | tareas y metodología definen el script |
| 3A.8.1 | 3A.8.3 |  | criterios derivados del plan |
| 3A.8.1 | 3A.8.3 | obligatorio | número de participantes y segmentos |
| 3A.8.1 | 3A.8.4 |  | resultados del estudio planificado |
| 3A.8.1 | 3A.8.4 | obligatorio | define qué se mide |
| 3A.8.1 | 3A.8.5 | recomendado | contexto de las preguntas de investigación |
| 3A.8.2 | 3A.8.4 |  | el script se ejecuta para producir resultados |
| 3A.8.2 | 3A.8.4 | obligatorio | se ejecutó para producir datos |
| 3A.8.2 | 3A.8.5 |  | hallazgos derivados de la ejecución del script |
| 3A.8.3 | 3A.8.4 |  | participantes reclutados según criterios producen resultados válidos |
| 3A.8.3 | 3A.8.4 | obligatorio | participantes reclutados según criterios |
| 3A.8.4 | 3A.8.5 |  | interpretación de los resultados |
| 3A.8.4 | 3A.8.5 | obligatorio | datos que se interpretan |
| 3A.8.4 | 3A.8.6 |  | iteraciones basadas en resultados |
| 3A.8.4 | 3A.8.7 | obligatorio | evidencia del testing |
| 3A.8.5 | 3A.5.1 |  | mockups actualizados según recomendaciones |
| 3A.8.5 | 3A.6.1 |  | prototipo actualizado |
| 3A.8.5 | 3A.8.6 |  | iteraciones basadas en recomendaciones |
| 3A.8.5 | 3A.8.6 | obligatorio | hallazgos que disparan las iteraciones |
| 3A.8.5 | 3A.8.7 |  | validación post-iteración |
| 3A.8.5 | 3A.8.7 | obligatorio | hallazgos resueltos |
| 3A.8.6 | 3A.8.7 |  | registro de iteraciones previo a validación final |
| 3A.8.6 | 3A.8.7 | obligatorio | iteraciones completadas |
| 3A.8.6 | 3A.9.1 |  | historial de decisiones de diseño para contexto del developer |
| 3A.8.7 | 3A.9.1 |  | gate de entrada a design handoff |
| 3A.8.7 | 3A.9.1 | obligatorio | gate: diseños deben estar validados |
| 3A.8.7 | 3A.9.2 |  | diseños validados listos para exportar specs |
| 3A.8.7 | 3A.9.2 | obligatorio | specs de diseños validados |
| 3A.8.7 | 3A.9.3 |  | assets de diseños validados |
| 3A.8.7 | 3A.9.3 | obligatorio | assets de diseños validados |
| 3A.8.7 | 3A.9.5 | obligatorio | redlines de diseños validados |
| 3A.9.1 | 3B.1.1 | recomendado | contexto de lo que el frontend necesita |
| 3A.9.1 | 4.4.1 |  | developers implementan componentes |
| 3A.9.1 | 4.4.14 |  | specs de accesibilidad para implementación |
| 3A.9.1 | 4.4.15 |  | breakpoints y responsive specs |
| 3A.9.1 | 4.4.2 |  | developers construyen páginas |
| 3A.9.2 | 3A.9.5 | recomendado | redlines complementan specs automáticas |
| 3A.9.2 | 4.4.1 |  | developers implementan con specs exactas |
| 3A.9.2 | 4.4.1 | obligatorio | specs exactas |
| 3A.9.2 | 4.4.15 |  | specs por breakpoint |
| 3A.9.2 | 4.4.8 |  | estilos CSS derivados de specs |
| 3A.9.3 | 4.4.1 |  | componentes React importan assets |
| 3A.9.3 | 4.4.8 |  | imágenes referenciadas en estilos |
| 3A.9.3 | 4.4.9 |  | utilidades de carga de assets |
| 3A.9.4 | 4.4.1 |  | componentes React consumen variables |
| 3A.9.4 | 4.4.1 | obligatorio | design tokens |
| 3A.9.4 | 4.4.15 |  | breakpoint variables |
| 3A.9.4 | 4.4.8 |  | estilos referencia las variables |
| 3A.9.4 | 4.4.8 | obligatorio | tokens |
| 3A.9.5 | 4.4.1 |  | developers implementan con medidas exactas |
| 3A.9.5 | 4.4.15 |  | medidas por breakpoint |
| 3A.9.5 | 4.4.3 |  | layouts implementados con medidas de redlines |
| 3B.1.1 | 3B.1.2 |  | vista L1 derivada del documento |
| 3B.1.1 | 3B.1.2 | obligatorio | define el contexto |
| 3B.1.1 | 3B.1.3 |  | vista L2 |
| 3B.1.1 | 3B.1.3 | obligatorio | decisiones que definen los contenedores |
| 3B.1.1 | 3B.1.4 |  | vista L3 |
| 3B.1.1 | 3B.1.5 |  | stack derivado de decisiones |
| 3B.1.1 | 3B.1.5 | obligatorio | contexto de decisiones |
| 3B.1.1 | 3B.1.6 | obligatorio | contexto técnico |
| 3B.1.1 | 3B.2.1 |  | estructura de código alineada a arquitectura |
| 3B.1.1 | 3B.2.3 | obligatorio | contexto arquitectónico |
| 3B.1.1 | 3B.3.1 |  | modelo de datos derivado de la arquitectura |
| 3B.1.1 | 3B.4.1 |  | contratos de API entre componentes |
| 3B.1.1 | 3B.4.9 | recomendado | contexto |
| 3B.1.1 | 3B.6.3 |  | decisiones documentadas |
| 3B.1.1 | 4.7.6 | obligatorio | base |
| 3B.1.2 | 3B.1.3 |  | zoom in del sistema |
| 3B.1.2 | 3B.1.3 | obligatorio | contexto externo |
| 3B.1.2 | 3B.1.6 |  | detalle de cada integración |
| 3B.1.2 | 3B.1.6 | obligatorio | sistemas externos identificados |
| 3B.1.2 | 3B.7.1 |  | superficie de ataque visible |
| 3B.1.2 | 3B.7.1 | obligatorio | superficie de ataque |
| 3B.1.3 | 3B.1.4 |  | zoom in de cada contenedor |
| 3B.1.3 | 3B.1.4 | obligatorio | define los contenedores a descomponer |
| 3B.1.3 | 3B.1.7 |  | flujo de datos entre contenedores |
| 3B.1.3 | 3B.1.7 | obligatorio | contenedores de procesamiento y almacenamiento |
| 3B.1.3 | 3B.3.1 |  | diseño de cada base de datos |
| 3B.1.3 | 3B.4.1 |  | contrato de cada API |
| 3B.1.3 | 3B.5.2 | obligatorio | participantes |
| 3B.1.3 | 3B.5.5 | obligatorio | participantes |
| 3B.1.3 | 3B.5.6 | obligatorio | workers y queues |
| 3B.1.3 | 3B.8.1 |  | infra para cada contenedor |
| 3B.1.3 | 3B.8.1 | obligatorio | contenedores a desplegar |
| 3B.1.3 | 3B.8.2 |  | mapping contenedor → infra |
| 3B.1.3 | 3B.8.2 | obligatorio |  |
| 3B.1.3 | 3B.8.3 | obligatorio |  |
| 3B.1.3 | 3B.8.6 | obligatorio |  |
| 3B.1.4 | 3B.2.1 |  | carpetas alineadas a componentes |
| 3B.1.4 | 3B.2.1 | obligatorio | módulos se mapean a carpetas |
| 3B.1.4 | 3B.2.3 | obligatorio | estructura que los patterns implementan |
| 3B.1.4 | 3B.2.4 |  | dependencias formalizadas |
| 3B.1.4 | 3B.2.4 | obligatorio | módulos identificados |
| 3B.1.4 | 3B.5.3 |  | sequences entre componentes |
| 3B.1.4 | 3B.5.3 | obligatorio | participantes |
| 3B.1.4 | 3B.9.5 | obligatorio |  |
| 3B.1.4 | 4.3.1 |  | implementación directa de componentes |
| 3B.1.5 | 3B.1.3 | recomendado | tecnología etiquetada en cada contenedor |
| 3B.1.5 | 3B.1.3 |  | tecnología etiquetada en cada contenedor |
| 3B.1.5 | 3B.2.1 |  | estructura depende del framework |
| 3B.1.5 | 3B.2.1 | obligatorio | framework condiciona la estructura |
| 3B.1.5 | 3B.2.2 |  | estándares dependen del lenguaje |
| 3B.1.5 | 3B.2.2 | obligatorio | lenguaje define las reglas aplicables |
| 3B.1.5 | 3B.2.3 | obligatorio | patterns dependen del lenguaje |
| 3B.1.5 | 3B.2.5 | obligatorio | lenguaje define las convenciones |
| 3B.1.5 | 3B.2.6 | obligatorio | mecanismos de error del lenguaje |
| 3B.1.5 | 3B.3.1 | obligatorio | tipo de BD condiciona el modelado |
| 3B.1.5 | 3B.3.2 |  | ORM/query builder depende del stack |
| 3B.1.5 | 3B.3.2 | obligatorio | ORM/tool |
| 3B.1.5 | 3B.3.6 | obligatorio | herramienta de migration |
| 3B.1.5 | 3B.3.8 | obligatorio | engine de BD |
| 3B.1.5 | 3B.4.6 | obligatorio | tools y providers |
| 3B.1.5 | 3B.4.8 | obligatorio | herramienta |
| 3B.1.5 | 3B.5.6 | obligatorio | herramienta de messaging |
| 3B.1.5 | 3B.6.3 |  | decisiones de stack como ADRs |
| 3B.1.5 | 3B.7.5 | obligatorio | herramientas |
| 3B.1.5 | 3B.7.6 | obligatorio |  |
| 3B.1.5 | 3B.7.7 | obligatorio |  |
| 3B.1.5 | 3B.7.8 | obligatorio | herramientas disponibles |
| 3B.1.5 | 3B.8.1 | obligatorio | servicios |
| 3B.1.5 | 3B.8.11 | obligatorio | herramientas |
| 3B.1.5 | 4.1.1 |  | instalación del stack elegido |
| 3B.1.5 | 4.1.1 | obligatorio |  |
| 3B.1.5 | 4.1.3 | obligatorio |  |
| 3B.1.5 | 4.1.4 | obligatorio |  |
| 3B.1.5 | 4.1.8 | obligatorio |  |
| 3B.1.5 | 4.1.9 | obligatorio |  |
| 3B.1.5 | 4.4.5 | obligatorio | library elegida |
| 3B.1.5 | 4.4.8 | obligatorio | approach |
| 3B.1.5 | 5.1.2 | obligatorio |  |
| 3B.1.5 | 6.2.3 | obligatorio |  |
| 3B.1.6 | 3B.1.7 | obligatorio | fuentes externas de datos |
| 3B.1.6 | 3B.4.1 |  | endpoints de integración documentados |
| 3B.1.6 | 3B.5.5 |  | sequence diagrams de cada integración |
| 3B.1.6 | 3B.5.5 | obligatorio | integraciones a diagramar |
| 3B.1.6 | 3B.7.1 |  | seguridad de cada integración |
| 3B.1.6 | 3B.7.8 | obligatorio | inventario de credentials |
| 3B.1.6 | 3B.9.5 | recomendado |  |
| 3B.1.6 | 4.3.6 |  | implementación de integraciones |
| 3B.1.6 | 4.5.1 | obligatorio |  |
| 3B.1.6 | 4.5.2 | obligatorio |  |
| 3B.1.6 | 4.5.5 | obligatorio |  |
| 3B.1.7 | 3B.3.1 |  | entidades identificadas en los flujos |
| 3B.1.7 | 3B.3.1 | recomendado | entidades identificadas en flujos |
| 3B.1.7 | 3B.3.5 |  | campos de datos documentados |
| 3B.1.7 | 3B.5.3 |  | secuencias basadas en flujos de datos |
| 3B.1.7 | 3B.5.6 | recomendado | flujos async |
| 3B.1.7 | 3B.7.4 |  | datos sensibles identificados en los flujos |
| 3B.1.7 | 3B.7.4 | obligatorio | flujo de datos sensibles |
| 3B.1.7 | 3B.8.7 |  | data stores identificados |
| 3B.2.1 | 3B.2.4 | obligatorio | organización de módulos |
| 3B.2.1 | 4.1.2 |  | repo creado con la estructura definida |
| 3B.2.1 | 4.1.3 |  | scaffolding sigue la estructura |
| 3B.2.1 | 4.3.1 |  | developers saben dónde crear módulos |
| 3B.2.1 | 4.3.8 | obligatorio | dónde viven los utils |
| 3B.2.1 | 4.4.1 |  | developers saben dónde crear componentes |
| 3B.2.1 | 4.4.9 | obligatorio | dónde viven |
| 3B.2.2 | 4.1.10 | obligatorio |  |
| 3B.2.2 | 4.1.3 |  | linting y formatting configurados desde el inicio |
| 3B.2.2 | 4.1.4 |  | linting como step del pipeline |
| 3B.2.2 | 4.1.6 | obligatorio |  |
| 3B.2.2 | 4.1.9 | obligatorio |  |
| 3B.2.2 | 4.8.1 | obligatorio | qué evaluar |
| 3B.2.3 | 3B.1.4 | recomendado | patterns que definen layers/modules |
| 3B.2.3 | 3B.2.1 | recomendado | patterns definen layers |
| 3B.2.3 | 3B.2.1 |  | estructura refleja los layers de los patterns |
| 3B.2.3 | 3B.2.4 | recomendado | layers definen reglas de dependencia |
| 3B.2.3 | 3B.2.6 |  | patterns de error handling |
| 3B.2.3 | 3B.2.6 | recomendado | patterns de error handling |
| 3B.2.3 | 4.3.1 |  | developers implementan usando los patterns |
| 3B.2.3 | 4.3.4 | obligatorio | pattern a seguir |
| 3B.2.3 | 4.4.1 |  | frontend patterns aplicados |
| 3B.2.4 | 3B.9.7 |  | dependencias técnicas de tareas |
| 3B.2.4 | 3B.9.7 | recomendado |  |
| 3B.2.4 | 4.1.3 |  | módulos creados con dependencias correctas |
| 3B.2.4 | 4.3.1 |  | implementación respetando dependencias |
| 3B.2.5 | 3B.2.2 | obligatorio | naming es parte de los standards |
| 3B.2.5 | 3B.2.2 |  | naming es parte de los standards |
| 3B.2.5 | 3B.3.2 | obligatorio | naming de tablas/columnas |
| 3B.2.5 | 3B.3.3 |  | naming de tablas y columnas |
| 3B.2.5 | 3B.4.11 | obligatorio | naming de API paths |
| 3B.2.5 | 3B.4.2 |  | naming de endpoints |
| 3B.2.6 | 3B.4.5 | obligatorio | clasificación de errores |
| 3B.2.6 | 3B.5.4 | obligatorio |  |
| 3B.2.6 | 4.3.1 |  | developers implementan error handling estándar |
| 3B.2.6 | 4.3.14 | obligatorio |  |
| 3B.2.6 | 4.3.7 |  | error handling middleware |
| 3B.2.6 | 4.3.7 | obligatorio |  |
| 3B.2.6 | 4.4.1 |  | frontend error boundaries implementados |
| 3B.2.6 | 4.5.3 |  | tests de error handling |
| 3B.2.6 | 4.5.8 | obligatorio |  |
| 3B.2.6 | 4.5.9 | obligatorio |  |
| 3B.3.1 | 3B.3.2 |  | implementación del ERD en SQL/ORM |
| 3B.3.1 | 3B.3.2 | obligatorio | modelo a implementar |
| 3B.3.1 | 3B.3.3 |  | detalle de cada tabla |
| 3B.3.1 | 3B.3.3 | obligatorio |  |
| 3B.3.1 | 3B.3.4 |  | índices basados en relaciones y queries |
| 3B.3.1 | 3B.3.4 | obligatorio | foreign keys a indexar |
| 3B.3.1 | 3B.3.5 |  | documentación de cada campo |
| 3B.3.1 | 3B.4.1 |  | entidades mapeadas a API resources |
| 3B.3.1 | 3B.4.1 | obligatorio | schemas derivados del modelo de datos |
| 3B.3.1 | 3B.4.2 | obligatorio | resources derivados de entidades |
| 3B.3.1 | 3B.9.3 | recomendado |  |
| 3B.3.2 | 3B.3.3 | obligatorio |  |
| 3B.3.2 | 3B.3.4 | obligatorio | tipos de datos (afectan tipo de índice) |
| 3B.3.2 | 3B.3.5 | obligatorio | campos a documentar |
| 3B.3.2 | 3B.3.6 |  | migration initial basada en el schema |
| 3B.3.2 | 3B.3.6 | obligatorio | schema que se versiona |
| 3B.3.2 | 3B.3.7 |  | datos iniciales para las tablas definidas |
| 3B.3.2 | 3B.3.7 | obligatorio | tablas que existen |
| 3B.3.2 | 3B.3.8 | obligatorio | qué se respalda |
| 3B.3.2 | 4.2.1 |  | creación de BD con el schema |
| 3B.3.2 | 4.2.1 | obligatorio |  |
| 3B.3.2 | 4.3.2 |  | models de aplicación basados en el schema |
| 3B.3.2 | 4.3.3 | obligatorio | base del modelo |
| 3B.3.3 | 3B.3.4 |  | queries frecuentes identifican índices necesarios |
| 3B.3.3 | 3B.3.4 | obligatorio | access patterns y volumen |
| 3B.3.3 | 3B.3.5 |  | fields documentados en detalle |
| 3B.3.3 | 3B.3.5 | obligatorio | contexto por tabla |
| 3B.3.3 | 3B.3.7 | obligatorio | valores de catálogo |
| 3B.3.3 | 3B.4.4 | recomendado | volumen esperado |
| 3B.3.3 | 4.2.6 | obligatorio |  |
| 3B.3.3 | 4.3.2 |  | developers entienden cada campo |
| 3B.3.4 | 3B.3.2 |  | índices incluidos en el schema final |
| 3B.3.4 | 4.2.1 |  | índices creados al inicializar la BD |
| 3B.3.4 | 4.2.5 | obligatorio |  |
| 3B.3.4 | 5.7.1 |  | benchmarks verifican efectividad de índices |
| 3B.3.5 | 3B.4.3 | recomendado | valores realistas |
| 3B.3.5 | 3B.7.1 | obligatorio | datos sensibles identificados |
| 3B.3.5 | 3B.7.4 | obligatorio | campos PII identificados |
| 3B.3.5 | 4.3.2 |  | developers entienden cada campo |
| 3B.3.5 | 5.1.3 |  | datos de prueba con valores correctos |
| 3B.3.6 | 4.1.4 |  | migration step en el pipeline de deploy |
| 3B.3.6 | 4.2.1 |  | proceso de setup usa migrations |
| 3B.3.6 | 4.2.2 | obligatorio |  |
| 3B.3.6 | 4.2.9 | obligatorio |  |
| 3B.3.7 | 4.1.3 |  | seed script incluido en setup |
| 3B.3.7 | 4.2.1 |  | seed ejecutado post-migration |
| 3B.3.7 | 4.2.3 | obligatorio |  |
| 3B.3.7 | 5.1.3 |  | seed data como base para test data |
| 3B.3.8 | 3B.8.7 | obligatorio | referencia cruzada |
| 3B.3.8 | 3B.8.8 |  | backups como mecanismo de recovery |
| 3B.3.8 | 3B.8.8 | obligatorio |  |
| 3B.3.8 | 6.3.1 |  | backups configurados en prod |
| 3B.3.8 | 7.2.1 |  | testing regular de backups |
| 3B.4.1 | 3B.4.10 |  | generada desde el OpenAPI spec |
| 3B.4.1 | 3B.4.10 | obligatorio | fuente para generación |
| 3B.4.1 | 3B.7.9 | obligatorio | schemas a validar |
| 3B.4.1 | 4.3.1 | obligatorio | contrato |
| 3B.4.1 | 4.3.3 |  | implementación directa del spec |
| 3B.4.1 | 4.3.5 | obligatorio | schemas |
| 3B.4.1 | 4.4.1 |  | frontend genera types desde el spec |
| 3B.4.1 | 4.4.6 | obligatorio | types |
| 3B.4.1 | 4.4.7 | obligatorio | API contracts |
| 3B.4.1 | 5.3.1 |  | tests de contrato basados en el spec |
| 3B.4.1 | 5.5.3 | obligatorio | el contrato |
| 3B.4.10 | 4.3.12 | obligatorio | base |
| 3B.4.10 | 4.3.3 |  | developers verifican implementación contra collection |
| 3B.4.10 | 5.3.1 |  | base para automation con Newman |
| 3B.4.11 | 4.3.3 |  | implementación consistente |
| 3B.4.2 | 3B.4.1 | obligatorio | qué endpoints incluir |
| 3B.4.2 | 3B.4.1 |  | endpoints detallados en el spec |
| 3B.4.2 | 3B.4.10 |  | colección con todos los endpoints |
| 3B.4.2 | 3B.4.3 |  | examples por endpoint |
| 3B.4.2 | 3B.4.3 | obligatorio | qué endpoints ejemplificar |
| 3B.4.2 | 3B.4.4 | obligatorio | qué endpoints paginan |
| 3B.4.2 | 3B.4.6 | recomendado | endpoints de auth |
| 3B.4.2 | 3B.4.7 | obligatorio | endpoints a proteger |
| 3B.4.2 | 3B.4.8 | obligatorio | endpoints a proteger |
| 3B.4.2 | 3B.4.9 | obligatorio | endpoints que se versionan |
| 3B.4.2 | 3B.5.3 | obligatorio | API calls |
| 3B.4.2 | 3B.9.3 |  | estimación por endpoint |
| 3B.4.2 | 3B.9.3 | recomendado |  |
| 3B.4.2 | 5.5.4 | obligatorio |  |
| 3B.4.2 | 5.7.1 | obligatorio |  |
| 3B.4.3 | 3B.4.1 |  | examples embebidos en el spec |
| 3B.4.3 | 3B.4.10 |  | examples como pre-filled bodies |
| 3B.4.3 | 3B.4.10 | obligatorio | bodies pre-populated |
| 3B.4.3 | 4.6.6 | recomendado |  |
| 3B.4.3 | 5.3.1 |  | fixtures basados en examples |
| 3B.4.4 | 3B.4.1 |  | pagination parameters y response format documentados |
| 3B.4.4 | 3B.4.11 | obligatorio | sección de guidelines |
| 3B.4.4 | 3B.4.3 |  | pagination examples |
| 3B.4.4 | 4.3.3 |  | implementación uniforme |
| 3B.4.5 | 3B.2.6 | recomendado | códigos estándar para API responses |
| 3B.4.5 | 3B.4.1 |  | error responses documentados |
| 3B.4.5 | 3B.4.11 | obligatorio | sección de guidelines |
| 3B.4.5 | 3B.4.3 | recomendado | error response format |
| 3B.4.5 | 3B.4.3 |  | error response examples |
| 3B.4.5 | 3B.5.4 | recomendado |  |
| 3B.4.5 | 4.3.14 | obligatorio |  |
| 3B.4.5 | 4.3.7 |  | error handler implementa los codes |
| 3B.4.5 | 4.4.1 |  | frontend maneja error codes específicos |
| 3B.4.6 | 3B.4.1 | obligatorio | security schemes del spec |
| 3B.4.6 | 3B.4.1 |  | security schemes |
| 3B.4.6 | 3B.4.10 | obligatorio | auth configurada en la collection |
| 3B.4.6 | 3B.5.2 |  | sequence diagram de auth |
| 3B.4.6 | 3B.5.2 | obligatorio | flujos a diagramar |
| 3B.4.6 | 3B.7.1 | obligatorio |  |
| 3B.4.6 | 3B.7.2 | obligatorio |  |
| 3B.4.6 | 4.3.4 |  | implementación del spec |
| 3B.4.6 | 4.3.7 | obligatorio |  |
| 3B.4.6 | 4.4.1 |  | frontend auth flow (login form, token management) |
| 3B.4.6 | 4.4.6 | obligatorio | auth handling |
| 3B.4.6 | 4.5.4 | obligatorio |  |
| 3B.4.7 | 3B.4.1 |  | security requirements por endpoint |
| 3B.4.7 | 3B.7.1 | obligatorio |  |
| 3B.4.7 | 3B.7.3 | obligatorio |  |
| 3B.4.7 | 4.3.4 |  | middleware de autorización |
| 3B.4.7 | 4.3.7 |  | guards/policies implementados |
| 3B.4.7 | 5.3.1 |  | tests de autorización por rol |
| 3B.4.8 | 3B.4.1 |  | rate limit headers documentados |
| 3B.4.8 | 3B.7.1 |  | rate limiting como control de seguridad |
| 3B.4.8 | 4.3.7 |  | rate limit middleware implementado |
| 3B.4.9 | 3B.4.1 |  | versioning reflejado en server URLs y paths |
| 3B.4.9 | 3B.4.11 |  | reglas de evolución de la API |
| 3B.4.9 | 3B.4.11 | obligatorio | sección de guidelines |
| 3B.5.1 | 4.3.1 |  | developers consultan flujos al implementar |
| 3B.5.1 | 5.3.1 |  | flujos como base de test scenarios |
| 3B.5.2 | 3B.5.1 | obligatorio |  |
| 3B.5.2 | 3B.5.1 |  | incluido en el documento |
| 3B.5.2 | 4.3.4 |  | implementación directa |
| 3B.5.2 | 5.3.2 |  | test scenarios basados en el flujo |
| 3B.5.3 | 3B.5.1 | obligatorio |  |
| 3B.5.3 | 3B.5.1 |  | incluidos en el documento |
| 3B.5.3 | 3B.5.4 | obligatorio | flujos base |
| 3B.5.3 | 4.3.1 |  | implementación basada en los flujos |
| 3B.5.3 | 5.1.1 |  | test scenarios derivados de flujos |
| 3B.5.3 | 5.3.1 |  | flujos como escenarios de test end-to-end |
| 3B.5.4 | 3B.5.1 | obligatorio |  |
| 3B.5.4 | 3B.5.1 |  | incluidos |
| 3B.5.4 | 4.3.7 |  | error handling middleware |
| 3B.5.4 | 5.4.1 |  | scenarios de test |
| 3B.5.5 | 3B.5.1 | obligatorio |  |
| 3B.5.5 | 3B.5.1 |  | incluidos |
| 3B.5.5 | 4.3.6 |  | implementación directa |
| 3B.5.5 | 4.5.1 | obligatorio |  |
| 3B.5.5 | 4.5.3 | obligatorio |  |
| 3B.5.5 | 5.6.1 |  | test scenarios |
| 3B.5.6 | 3B.5.1 | obligatorio |  |
| 3B.5.6 | 3B.5.1 |  | incluidos |
| 3B.5.6 | 3B.8.11 |  | monitoring de queues y workers |
| 3B.5.6 | 4.3.5 |  | implementación de workers |
| 3B.5.6 | 4.3.6 | obligatorio | diseño de flujos async |
| 3B.5.6 | 5.5.1 |  | test scenarios |
| 3B.6.1 | 3B.6.2 |  | ADRs indexables porque comparten estructura |
| 3B.6.1 | 3B.6.2 | obligatorio | estructura que permite indexar |
| 3B.6.1 | 3B.6.3 |  | cada ADR usa este template |
| 3B.6.1 | 3B.6.3 | obligatorio | formato a seguir |
| 3B.6.1 | 3B.6.4 | recomendado | para saber qué es ADR vs decision log entry |
| 3B.6.3 | 3B.6.2 | obligatorio | documentos a indexar |
| 3B.6.3 | 3B.6.2 |  | ADRs indexadas |
| 3B.6.3 | 3B.6.4 |  | decisiones resumidas |
| 3B.7.1 | 3B.7.10 | obligatorio |  |
| 3B.7.1 | 3B.7.11 | obligatorio |  |
| 3B.7.1 | 3B.7.2 |  | secciones detalladas del plan |
| 3B.7.1 | 3B.7.2 | recomendado | contexto de seguridad general |
| 3B.7.1 | 3B.7.3 | recomendado |  |
| 3B.7.1 | 3B.7.6 | obligatorio | contexto de seguridad |
| 3B.7.1 | 3B.7.7 | recomendado |  |
| 3B.7.1 | 3B.8.1 | obligatorio | controles de seguridad |
| 3B.7.1 | 3B.8.4 | recomendado |  |
| 3B.7.1 | 4.3.7 |  | security middleware |
| 3B.7.1 | 5.8.1 |  | test plan de seguridad |
| 3B.7.1 | 5.8.1 | obligatorio |  |
| 3B.7.1 | 6.3.1 |  | hardening de producción |
| 3B.7.10 | 3B.7.11 | recomendado |  |
| 3B.7.10 | 4.3.15 | obligatorio | eventos a loggear |
| 3B.7.10 | 4.3.7 |  | logging middleware |
| 3B.7.10 | 7.1.1 |  | dashboards de security events |
| 3B.7.11 | 7.3.1 |  | operación de incidents en producción |
| 3B.7.2 | 3B.4.6 | obligatorio | decisiones de seguridad de auth |
| 3B.7.2 | 4.3.4 |  | implementación segura |
| 3B.7.2 | 5.8.1 |  | test cases de auth security |
| 3B.7.3 | 3B.4.7 | obligatorio | modelo RBAC/ABAC |
| 3B.7.3 | 4.3.4 |  | guards/policies |
| 3B.7.3 | 5.8.1 |  | authorization bypass tests |
| 3B.7.4 | 3B.7.5 |  | encriptación de datos sensibles |
| 3B.7.4 | 3B.7.5 | obligatorio | qué encriptar |
| 3B.7.4 | 4.3.2 |  | soft delete, anonymization |
| 3B.7.4 | 7.5.1 |  | jobs de eliminación automática |
| 3B.7.5 | 4.2.1 |  | encryption at rest configurado |
| 3B.7.5 | 6.3.1 |  | TLS configurado |
| 3B.7.6 | 5.8.1 |  | test cases por vulnerabilidad OWASP |
| 3B.7.6 | 5.8.1 | obligatorio |  |
| 3B.7.6 | 5.8.4 | obligatorio |  |
| 3B.7.7 | 4.3.7 |  | headers configurados en middleware |
| 3B.7.7 | 5.8.1 |  | verificación de headers |
| 3B.7.8 | 4.1.3 |  | .env setup y .gitignore |
| 3B.7.8 | 4.1.3 | obligatorio |  |
| 3B.7.8 | 4.1.4 |  | secrets injection en pipeline |
| 3B.7.8 | 6.3.1 |  | secrets configurados |
| 3B.7.9 | 4.3.3 |  | validation en cada route |
| 3B.7.9 | 4.3.7 |  | validation middleware |
| 3B.7.9 | 5.3.1 |  | test cases de validation |
| 3B.8.1 | 3B.3.8 | recomendado | storage para backups |
| 3B.8.1 | 3B.8.10 | obligatorio |  |
| 3B.8.1 | 3B.8.2 |  | secciones detalladas |
| 3B.8.1 | 3B.8.7 | obligatorio |  |
| 3B.8.1 | 3B.8.8 | obligatorio |  |
| 3B.8.1 | 4.1.1 |  | provisión de ambientes |
| 3B.8.1 | 6.1.1 | obligatorio |  |
| 3B.8.1 | 6.3.1 |  | setup de producción |
| 3B.8.10 | 3B.8.11 |  | SLIs monitoreados |
| 3B.8.10 | 3B.8.11 | obligatorio | qué medir |
| 3B.8.10 | 6.7.5 | obligatorio |  |
| 3B.8.10 | 7.1.1 |  | dashboards de SLOs |
| 3B.8.10 | 7.1.1 | obligatorio |  |
| 3B.8.10 | 7.3.1 |  | escalation basado en SLA breach |
| 3B.8.11 | 3B.7.10 | recomendado | herramienta y formato |
| 3B.8.11 | 4.3.15 | recomendado | formato y destino |
| 3B.8.11 | 7.1.1 |  | implementación |
| 3B.8.11 | 7.1.2 |  | visualización de métricas |
| 3B.8.11 | 7.3.1 |  | alertas disparan incidents |
| 3B.8.2 | 3B.8.4 | obligatorio |  |
| 3B.8.2 | 4.1.1 |  | provisión basada en el diagrama |
| 3B.8.2 | 6.3.1 |  | referencia visual |
| 3B.8.3 | 3B.8.2 | recomendado |  |
| 3B.8.3 | 3B.8.2 |  | specs etiquetadas |
| 3B.8.3 | 3B.8.5 | recomendado |  |
| 3B.8.3 | 3B.8.6 | obligatorio |  |
| 3B.8.3 | 3B.8.9 |  | costos por servidor |
| 3B.8.3 | 3B.8.9 | obligatorio |  |
| 3B.8.3 | 4.1.1 |  | provisión con specs correctas |
| 3B.8.3 | 6.1.2 | obligatorio |  |
| 3B.8.4 | 3B.8.2 | recomendado |  |
| 3B.8.4 | 4.1.1 |  | VPC y networking provisionados |
| 3B.8.4 | 6.1.3 | obligatorio |  |
| 3B.8.4 | 6.3.1 |  | network hardening |
| 3B.8.5 | 3B.3.6 | recomendado | ambientes donde aplicar migrations |
| 3B.8.5 | 3B.7.8 |  | secrets por ambiente |
| 3B.8.5 | 3B.8.9 | obligatorio |  |
| 3B.8.5 | 4.1.1 |  | creación de ambientes |
| 3B.8.5 | 4.1.1 | obligatorio |  |
| 3B.8.5 | 4.1.4 |  | deploy targets |
| 3B.8.5 | 5.3.1 | obligatorio |  |
| 3B.8.5 | 6.2.5 | obligatorio |  |
| 3B.8.6 | 3B.8.9 |  | costos de scaling incluidos |
| 3B.8.6 | 4.1.1 |  | auto-scaling configurado |
| 3B.8.6 | 7.1.1 |  | scaling metrics monitoreadas |
| 3B.8.7 | 3B.8.8 |  | backups como mecanismo de recovery |
| 3B.8.7 | 3B.8.8 | obligatorio |  |
| 3B.8.7 | 7.2.1 |  | testing de todos los backups |
| 3B.8.8 | 3B.3.8 | recomendado | RPO/RTO |
| 3B.8.8 | 7.2.1 |  | DR testing |
| 3B.8.9 | 7.4.1 |  | baseline para alertas de costo |
| 3B.9.1 | 2.4.6 |  | asignación a sprints |
| 3B.9.1 | 3B.8.3 | recomendado | carga estimada |
| 3B.9.1 | 3B.9.4 |  | resumen de esfuerzo por módulo |
| 3B.9.1 | 3B.9.4 | obligatorio |  |
| 3B.9.1 | 3B.9.6 |  | estimaciones con buffer |
| 3B.9.1 | 3B.9.6 | obligatorio |  |
| 3B.9.1 | 3B.9.9 |  | planning de equipo |
| 3B.9.1 | 3B.9.9 | obligatorio |  |
| 3B.9.2 | 2.4.6 |  | stories asignadas por capacity en puntos |
| 3B.9.2 | 3B.9.1 |  | consolidated view |
| 3B.9.2 | 3B.9.8 |  | velocity derivada de story points |
| 3B.9.2 | 3B.9.8 | obligatorio |  |
| 3B.9.3 | 3B.9.1 | obligatorio | tareas identificadas |
| 3B.9.3 | 3B.9.1 |  | estimaciones por tarea |
| 3B.9.3 | 3B.9.7 |  | dependencias entre tareas |
| 3B.9.3 | 3B.9.7 | obligatorio |  |
| 3B.9.4 | 3B.9.9 |  | distribución de trabajo por equipo |
| 3B.9.4 | 3B.9.9 | obligatorio |  |
| 3B.9.5 | 3B.9.1 | obligatorio | factores de complejidad |
| 3B.9.5 | 3B.9.1 |  | complejidad informa estimaciones |
| 3B.9.5 | 3B.9.2 | recomendado | informa la estimación |
| 3B.9.5 | 3B.9.2 |  | complejidad informa puntos |
| 3B.9.5 | 3B.9.6 |  | riesgo correlaciona con complejidad |
| 3B.9.5 | 3B.9.6 | obligatorio |  |
| 3B.9.6 | 2.4.6 |  | capacity con buffer |
| 3B.9.6 | 3B.9.9 |  | planning con rangos |
| 3B.9.7 | 2.4.6 |  | sequencing de tareas |
| 3B.9.7 | 3B.9.9 |  | paralelismo posible |
| 3B.9.8 | 3B.9.9 |  | velocity informa capacity |
| 3B.9.8 | 3B.9.9 | recomendado |  |
| 3B.9.9 | 2.4.6 |  | sprints planificados con capacity real |
| 4.1.1 | 4.1.2 |  | documentación del setup |
| 4.1.1 | 4.1.2 | obligatorio |  |
| 4.1.1 | 4.1.5 | obligatorio |  |
| 4.1.1 | 4.2.1 |  | BD local lista |
| 4.1.1 | 4.2.1 | obligatorio | BD local corriendo |
| 4.1.1 | 5.3.1 | obligatorio |  |
| 4.1.10 | .prettierignore |  | archivos excluidos |
| 4.1.10 | .prettierrc |  | configuración |
| 4.1.10 | 4.1.6 |  | format on save |
| 4.1.10 | 4.1.7 | obligatorio |  |
| 4.1.10 | 4.1.7 |  | formatting en pre-commit |
| 4.1.2 | README.md |  |  |
| 4.1.3 | .env |  | valores reales locales |
| 4.1.3 | .env.example |  | template con valores de ejemplo |
| 4.1.3 | 4.1.1 |  | Docker Compose lee .env |
| 4.1.3 | 4.1.4 |  | servicios configurados con env vars |
| 4.1.3 | 4.1.4 | obligatorio |  |
| 4.1.3 | 4.5.5 | obligatorio | credentials |
| 4.1.3 | 6.2.5 | obligatorio |  |
| 4.1.4 | 4.1.1 |  | orquestación del ambiente |
| 4.1.4 | 4.2.1 |  | BD local lista |
| 4.1.4 | depends_on |  |  |
| 4.1.4 | docker-compose.override.yml |  |  |
| 4.1.4 | docker-compose.yml |  |  |
| 4.1.5 | Makefile |  |  |
| 4.1.5 | make help |  |  |
| 4.1.6 | .editorconfig |  | settings cross-IDE (tabs, line endings) |
| 4.1.6 | .vscode/extensions.json |  | extensiones recomendadas |
| 4.1.6 | .vscode/launch.json |  | debug configurations |
| 4.1.6 | .vscode/settings.json |  | settings del proyecto |
| 4.1.7 | --no-verify |  |  |
| 4.1.7 | .husky/pre-commit |  | hook de pre-commit |
| 4.1.7 | .lintstagedrc |  | configuración de lint-staged |
| 4.1.7 | package.json |  |  |
| 4.1.8 | .gitattributes |  | line endings, binary files |
| 4.1.8 | .gitignore |  | exclusiones |
| 4.1.8 | 4.7.7 | obligatorio |  |
| 4.1.8 | docs/BRANCHING.md |  | branching strategy |
| 4.1.9 | .eslintignore |  | archivos excluidos |
| 4.1.9 | .eslintrc.json |  | reglas |
| 4.1.9 | 4.1.7 | obligatorio |  |
| 4.1.9 | 4.1.7 |  | linting en pre-commit |
| 4.1.9 | 6.2.1 | obligatorio |  |
| 4.2.1 | 4.2.2 |  | migrations incrementales |
| 4.2.1 | 4.2.2 | obligatorio |  |
| 4.2.1 | 4.2.3 |  | datos sobre el schema |
| 4.2.1 | 4.2.3 | obligatorio | tablas deben existir |
| 4.2.1 | 4.2.4 | obligatorio |  |
| 4.2.1 | 4.2.5 |  | índices en las tablas |
| 4.2.1 | 4.2.5 | obligatorio |  |
| 4.2.1 | 4.2.6 | obligatorio |  |
| 4.2.1 | 4.2.7 | obligatorio |  |
| 4.2.1 | 4.2.8 | obligatorio |  |
| 4.2.1 | 4.2.9 | obligatorio | proceso probado |
| 4.2.1 | 4.3.1 | obligatorio | BD lista |
| 4.2.1 | 4.3.3 |  | modelos de aplicación |
| 4.2.1 | 4.3.3 | obligatorio | schema en BD |
| 4.2.1 | 5.3.2 | obligatorio |  |
| 4.2.1 | migrations/V1__initial_schema.sql |  |  |
| 4.2.1 | prisma/migrations/YYYYMMDD_init/migration.sql |  |  |
| 4.2.1 | prisma/schema.prisma |  |  |
| 4.2.10 | 6.7.1 | obligatorio |  |
| 4.2.2 | 4.2.10 | obligatorio | migration a revertir |
| 4.2.2 | add_status_to_orders |  |  |
| 4.2.2 | prisma/migrations/YYYYMMDD_description/migration.sql |  |  |
| 4.2.3 | 4.2.4 |  | datos de prueba sobre el seed |
| 4.2.3 | 4.2.4 | obligatorio | catálogos base |
| 4.2.3 | 5.3.2 | obligatorio |  |
| 4.2.3 | make seed |  |  |
| 4.2.3 | prisma/seed.ts |  |  |
| 4.2.4 | 4.3.10 | obligatorio | datos en test DB |
| 4.2.4 | 4.6.5 |  | factories reutilizables en tests |
| 4.2.4 | make test-data |  |  |
| 4.2.4 | scripts/test-data.ts |  |  |
| 4.2.5 | migrations/add_indexes.sql |  |  |
| 4.2.9 | docs/MIGRATIONS.md |  |  |
| 4.3.1 | 4.3.10 |  | tests end-to-end de API |
| 4.3.1 | 4.3.10 | obligatorio | endpoints implementados |
| 4.3.1 | 4.3.11 |  | Swagger generado desde código |
| 4.3.1 | 4.3.11 | obligatorio |  |
| 4.3.1 | 4.3.12 | obligatorio |  |
| 4.3.1 | 4.3.9 |  | tests de controllers |
| 4.3.1 | 4.4.6 |  | frontend consume endpoints |
| 4.3.1 | 4.5.3 | obligatorio | endpoint de webhook |
| 4.3.1 | 5.3.1 |  | QA tests de API |
| 4.3.1 | 5.5.3 | obligatorio | la implementación |
| 4.3.10 | 5.3.1 |  | QA tests de API (basados en integration tests) |
| 4.3.10 | 5.5.1 | obligatorio | base existente |
| 4.3.11 | 3B.4.10 |  | puede importar desde Swagger |
| 4.3.11 | 4.7.4 | obligatorio |  |
| 4.3.12 | 5.3.1 |  | automation con Newman |
| 4.3.13 | 4.7.2 | obligatorio | versión a actualizar |
| 4.3.14 | 4.3.1 |  | endpoints usan custom exceptions |
| 4.3.14 | 4.3.2 |  | services throw custom exceptions |
| 4.3.14 | 4.3.7 |  | global error handler |
| 4.3.15 | 6.6.3 | obligatorio |  |
| 4.3.15 | 7.1.1 |  | logs como input de monitoring |
| 4.3.2 | 4.3.1 | co-dependencia | controllers delegan a services |
| 4.3.2 | 4.3.1 |  | controllers delegan a services |
| 4.3.2 | 4.3.6 |  | workers reusan services |
| 4.3.2 | 4.3.6 | obligatorio | workers reusan services |
| 4.3.2 | 4.3.9 |  | tests de lógica de negocio |
| 4.3.2 | 4.3.9 | obligatorio | código a testear |
| 4.3.2 | 4.5.1 | obligatorio | services que orquestan integraciones |
| 4.3.2 | 4.5.4 | obligatorio | user management |
| 4.3.3 | 4.3.2 | obligatorio | entidades del dominio |
| 4.3.3 | 4.3.2 |  | services trabajan con models |
| 4.3.3 | 4.3.4 |  | repositories usan models |
| 4.3.3 | 4.3.4 | obligatorio | entidades del ORM |
| 4.3.3 | 4.3.5 |  | DTOs derivados de models |
| 4.3.3 | 4.3.5 | obligatorio | campos base |
| 4.3.3 | 4.6.5 | obligatorio | estructura de entidades |
| 4.3.4 | 4.3.2 | co-dependencia | services usan repositories |
| 4.3.4 | 4.3.2 |  | services consumen repositories |
| 4.3.4 | 4.3.9 |  | repositories mockeables |
| 4.3.5 | 4.3.1 | co-dependencia | validation schemas |
| 4.3.5 | 4.3.1 |  | controllers usan DTOs para validar |
| 4.3.5 | 4.3.11 | obligatorio |  |
| 4.3.5 | 4.4.7 |  | frontend puede derivar types de los DTOs |
| 4.3.6 | 3B.8.11 |  | monitoring de queues |
| 4.3.6 | 4.3.9 |  | tests de workers |
| 4.3.7 | 4.3.1 |  | endpoints usan middlewares |
| 4.3.7 | 4.3.15 |  | logging middleware implementado |
| 4.3.9 | 4.6.1 | obligatorio | tests existentes |
| 4.3.9 | 4.6.3 |  | coverage measurement |
| 4.3.9 | 4.6.4 |  | metric target |
| 4.4.1 | 4.4.11 |  | tests de componentes |
| 4.4.1 | 4.4.11 | obligatorio |  |
| 4.4.1 | 4.4.12 |  | stories de componentes |
| 4.4.1 | 4.4.12 | obligatorio |  |
| 4.4.1 | 4.4.14 | obligatorio | componentes implementados |
| 4.4.1 | 4.4.15 | obligatorio | componentes a hacer responsive |
| 4.4.1 | 4.4.2 |  | pages usan componentes |
| 4.4.1 | 4.4.2 | obligatorio | building blocks |
| 4.4.1 | 4.4.3 | obligatorio | Navbar, Sidebar como componentes |
| 4.4.10 | 4.6.2 | obligatorio |  |
| 4.4.10 | 4.6.3 |  | coverage medido |
| 4.4.11 | 4.6.3 |  | coverage |
| 4.4.13 | 4.7.3 | obligatorio |  |
| 4.4.14 | 5.9.1 |  | testing de a11y |
| 4.4.14 | 5.9.1 | obligatorio | implementación a verificar |
| 4.4.14 | 5.9.3 | obligatorio | implementación |
| 4.4.14 | 5.9.4 | obligatorio |  |
| 4.4.15 | 5.4.2 |  | testing en múltiples devices |
| 4.4.2 | 4.4.10 |  | tests de pages |
| 4.4.2 | 5.4.1 |  | tests end-to-end por page/flow |
| 4.4.3 | 4.4.15 |  | layouts responsive |
| 4.4.3 | 4.4.15 | obligatorio | layouts responsive |
| 4.4.3 | 4.4.2 | obligatorio | layout wrapper |
| 4.4.3 | 4.4.2 |  | pages usan layouts |
| 4.4.4 | 4.4.1 |  | components usan hooks |
| 4.4.4 | 4.4.10 |  | tests de hooks |
| 4.4.4 | 4.4.10 | obligatorio | código a testear |
| 4.4.4 | 4.4.2 |  | pages usan hooks |
| 4.4.5 | 4.4.10 |  | tests de store |
| 4.4.5 | 4.4.2 |  | pages acceden al store |
| 4.4.5 | 4.4.4 | recomendado | para state hooks |
| 4.4.5 | 4.4.4 |  | hooks wrappean store access |
| 4.4.6 | 4.4.2 | obligatorio | data fetching |
| 4.4.6 | 4.4.2 |  | pages consumen API vía hooks/client |
| 4.4.6 | 4.4.4 | recomendado | para data fetching hooks |
| 4.4.6 | 4.4.4 |  | data fetching hooks wrappean API client |
| 4.4.8 | 4.4.1 |  | componentes consumen estilos |
| 4.4.8 | 4.4.15 |  | media queries |
| 4.4.9 | 4.4.10 | obligatorio | código a testear |
| 4.5.1 | 4.5.6 |  | tests de integraciones |
| 4.5.1 | 4.5.6 | obligatorio |  |
| 4.5.1 | 4.5.7 |  | documentación |
| 4.5.1 | 4.5.7 | obligatorio |  |
| 4.5.1 | 4.5.8 | obligatorio |  |
| 4.5.2 | 4.5.1 |  | clients usados por integration code |
| 4.5.3 | 4.5.6 |  | tests de webhooks |
| 4.5.5 | 4.5.1 |  | integration usa SDKs |
| 4.6.1 | 4.6.4 |  | target alcanzado |
| 4.6.2 | 4.6.4 |  |  |
| 4.6.3 | 4.6.1 | obligatorio | gaps a cubrir |
| 4.6.3 | 4.6.1 |  | identifica gaps a cubrir |
| 4.6.3 | 4.6.2 | obligatorio |  |
| 4.6.3 | 4.6.4 |  | medición del target |
| 4.6.3 | 4.6.4 | obligatorio |  |
| 4.6.3 | 4.8.2 | obligatorio |  |
| 4.6.5 | 4.3.9 | recomendado | data de tests |
| 4.6.5 | 4.3.9 |  | factories usadas por developers |
| 4.6.5 | 4.6.1 |  | factories usadas en tests |
| 4.6.5 | 4.6.2 |  | factories usadas en tests |
| 4.6.5 | 4.6.6 |  | fixtures generados con factories |
| 4.7.7 | 4.7.8 | obligatorio | commit convention |
| 4.7.7 | 4.8.1 | obligatorio | proceso de PR |
| 4.7.8 | 6.5.5 | obligatorio |  |
| 4.8.1 | 4.8.2 |  | data de reviews |
| 4.8.2 | 4.8.4 |  | áreas a refactorizar basadas en métricas |
| 4.8.2 | 4.8.4 | recomendado | priorización data-driven |
| 4.8.3 | 4.8.4 |  | plan para pagar la deuda |
| 4.8.3 | 4.8.4 | obligatorio | items a planificar |
| 5.1.1 | 5.1.3 |  | scope detallado |
| 5.1.1 | 5.1.3 | obligatorio |  |
| 5.1.1 | 5.1.4 | obligatorio |  |
| 5.1.1 | 5.2.1 |  | test cases basados en el plan |
| 5.1.1 | 5.4.1 |  | ejecución del plan |
| 5.1.2 | 5.1.1 | co-dependencia | estrategia informa el plan |
| 5.1.2 | 5.1.1 |  | estrategia informa el plan |
| 5.1.3 | 5.2.1 |  | test cases dentro del scope |
| 5.1.3 | 5.2.1 | obligatorio | qué está in-scope |
| 5.1.4 | 5.1.5 | obligatorio |  |
| 5.10.1 | 5.10.2 |  | test cases para UAT |
| 5.10.1 | 5.10.2 | obligatorio |  |
| 5.10.1 | 5.10.3 |  | resultados |
| 5.10.1 | 5.10.5 |  | decisión final |
| 5.10.2 | 5.10.3 |  | test cases a ejecutar |
| 5.10.2 | 5.10.3 | obligatorio |  |
| 5.10.3 | 5.10.4 |  | feedback cualitativo |
| 5.10.3 | 5.10.4 | obligatorio |  |
| 5.10.3 | 5.10.5 |  | decisión |
| 5.10.3 | 5.10.5 | obligatorio |  |
| 5.10.4 | 7.4.4 |  | feedback como input de mejoras |
| 5.10.5 | 6.5.1 |  | gate de entrada (sin UAT sign-off, no deploy) |
| 5.10.5 | 6.5.1 | obligatorio |  |
| 5.11.1 | 5.10.5 |  | prerequisito para acceptance |
| 5.11.1 | 5.11.2 |  | verificación de no-regresión |
| 5.11.1 | 5.11.2 | co-dependencia | incluido en el PR del fix |
| 5.11.1 | 5.11.3 |  | tracking de resolución |
| 5.11.1 | 5.11.3 | obligatorio |  |
| 5.11.3 | 5.10.5 |  | prerequisito |
| 5.2.1 | 5.10.2 |  | subset para UAT |
| 5.2.1 | 5.2.2 | obligatorio |  |
| 5.2.1 | 5.2.3 | obligatorio |  |
| 5.2.1 | 5.2.4 | obligatorio |  |
| 5.2.1 | 5.4.1 |  | ejecución de test cases |
| 5.2.1 | 5.4.1 | obligatorio |  |
| 5.2.1 | 5.6.1 |  | E2E tests basados en test cases |
| 5.2.3 | 5.3.3 | obligatorio | datos a cargar |
| 5.2.3 | 5.4.1 |  | tests ejecutados con datos |
| 5.2.4 | 5.4.1 |  | pass/fail determination |
| 5.3.1 | 5.10.1 |  | UAT en este ambiente |
| 5.3.1 | 5.10.1 | obligatorio |  |
| 5.3.1 | 5.3.4 | obligatorio |  |
| 5.3.1 | 5.4.1 |  | tests ejecutados en este ambiente |
| 5.3.1 | 5.4.1 | obligatorio |  |
| 5.3.1 | 5.5.1 | obligatorio |  |
| 5.3.1 | 5.6.1 |  | E2E contra este ambiente |
| 5.3.1 | 5.6.1 | obligatorio |  |
| 5.3.1 | 5.7.1 | obligatorio |  |
| 5.3.1 | 5.7.2 | obligatorio |  |
| 5.3.1 | 5.8.2 | obligatorio |  |
| 5.3.1 | 5.9.1 | obligatorio |  |
| 5.3.2 | 5.3.3 | obligatorio | BD donde cargar |
| 5.4.1 | 5.11.1 |  | bugs a corregir |
| 5.4.1 | 5.4.2 | co-dependencia |  |
| 5.4.1 | 5.4.3 |  | bugs detectados |
| 5.4.1 | 5.4.3 | obligatorio | tests ejecutados |
| 5.4.1 | 5.4.4 |  | resumen de resultados |
| 5.4.1 | 5.4.4 | obligatorio |  |
| 5.4.1 | 5.4.5 | co-dependencia | evidence durante ejecución |
| 5.4.3 | 5.11.1 |  | bugs a corregir |
| 5.4.3 | 5.11.1 | obligatorio | bugs reportados |
| 5.4.3 | 5.11.3 |  | tracking de resolución |
| 5.4.3 | 5.4.4 |  | conteo de defectos |
| 5.4.4 | 5.10.1 | obligatorio | QA pass antes de UAT |
| 5.4.4 | 5.10.5 | obligatorio |  |
| 5.4.5 | 5.4.3 |  | evidence en bug reports |
| 5.5.1 | 5.5.2 |  | resultados de ejecución |
| 5.5.1 | 5.5.2 | obligatorio |  |
| 5.5.1 | 5.5.4 |  | medición de coverage |
| 5.5.1 | 5.5.4 | obligatorio |  |
| 5.5.2 | 5.5.4 |  | data de coverage |
| 5.6.1 | 5.6.2 |  | resultados |
| 5.6.1 | 5.6.2 | obligatorio |  |
| 5.6.1 | 5.6.3 |  | medición |
| 5.6.1 | 5.6.3 | obligatorio |  |
| 5.6.1 | 5.6.4 |  | screenshots de referencia |
| 5.6.1 | 5.6.4 | obligatorio | captura screenshots |
| 5.6.1 | 5.6.5 | obligatorio |  |
| 5.7.1 | 5.7.2 |  | ejecución del plan |
| 5.7.1 | 5.7.2 | obligatorio |  |
| 5.7.1 | 5.7.3 |  | ejecución del plan |
| 5.7.1 | 5.7.3 | obligatorio |  |
| 5.7.2 | 5.7.3 | recomendado | baseline antes de stress |
| 5.7.2 | 5.7.4 |  | métricas consolidadas |
| 5.7.2 | 5.7.4 | obligatorio |  |
| 5.7.2 | 5.7.5 |  | si hay failures |
| 5.7.2 | 5.7.5 | obligatorio |  |
| 5.7.3 | 5.7.5 |  | qué se saturó |
| 5.7.3 | 5.7.5 | recomendado |  |
| 5.7.3 | 5.7.6 |  | qué mejorar |
| 5.7.3 | 7.6.2 |  | breaking point como input |
| 5.7.5 | 5.7.6 |  | soluciones |
| 5.7.5 | 5.7.6 | obligatorio |  |
| 5.8.1 | 5.8.2 |  | ejecución del plan |
| 5.8.1 | 5.8.2 | obligatorio |  |
| 5.8.1 | 5.8.3 | obligatorio |  |
| 5.8.2 | 5.8.4 | obligatorio |  |
| 5.8.2 | 5.8.5 |  | findings consolidados |
| 5.8.2 | 5.8.5 | obligatorio |  |
| 5.8.2 | 5.8.6 |  | plan de corrección |
| 5.8.3 | 5.8.4 | obligatorio |  |
| 5.8.3 | 5.8.5 |  | findings consolidados |
| 5.8.3 | 5.8.5 | obligatorio |  |
| 5.8.3 | 5.8.6 |  | CVEs a remediar |
| 5.8.4 | 5.8.5 |  | findings de OWASP violations |
| 5.8.4 | 5.8.5 | obligatorio |  |
| 5.8.4 | 5.8.7 |  | evidence de compliance |
| 5.8.5 | 5.8.6 |  | findings a remediar |
| 5.8.5 | 5.8.6 | obligatorio |  |
| 5.8.5 | 5.8.7 |  | input para decisión |
| 5.8.6 | 5.8.7 |  | critical remediados para sign-off |
| 5.8.6 | 5.8.7 | obligatorio | critical remediados |
| 5.8.7 | 6.1.1 | obligatorio |  |
| 5.8.7 | 6.5.1 |  | gate de entrada |
| 5.8.7 | 6.5.1 | obligatorio |  |
| 5.9.1 | 5.9.2 |  | puntuación |
| 5.9.1 | 5.9.2 | obligatorio | baseline |
| 5.9.1 | 5.9.3 |  | testing manual |
| 5.9.1 | 5.9.3 | obligatorio |  |
| 5.9.1 | 5.9.4 |  | testing manual |
| 5.9.1 | 5.9.4 | obligatorio |  |
| 6.1.1 | 6.1.2 |  | componentes específicos |
| 6.1.1 | 6.1.2 | obligatorio |  |
| 6.1.1 | 6.1.3 | obligatorio |  |
| 6.1.1 | 6.1.7 | obligatorio |  |
| 6.1.1 | 6.2.1 |  | infra donde deployar |
| 6.1.1 | 6.2.2 | obligatorio |  |
| 6.1.1 | 6.2.4 | obligatorio |  |
| 6.1.1 | 6.3.1 | obligatorio |  |
| 6.1.1 | 6.5.1 |  | infra lista |
| 6.1.2 | 6.1.5 | obligatorio |  |
| 6.1.2 | 6.2.2 |  | target de deployment |
| 6.1.2 | 6.5.1 |  | servers donde deployar |
| 6.1.2 | 7.6.3 | obligatorio | config base |
| 6.1.3 | 6.1.4 |  | SGs en la VPC |
| 6.1.3 | 6.1.4 | obligatorio |  |
| 6.1.3 | 6.1.5 |  | LB en subnet pública |
| 6.1.3 | 6.1.6 |  | DB en subnet privada |
| 6.1.3 | 6.1.6 | obligatorio | subnet privada |
| 6.1.4 | 6.1.6 | obligatorio | SG de DB |
| 6.1.5 | 6.1.8 | obligatorio |  |
| 6.1.5 | 6.5.3 |  | DNS apunta al LB |
| 6.1.5 | 6.5.3 | obligatorio |  |
| 6.1.6 | 6.3.3 |  | migrations en prod DB |
| 6.1.8 | 6.1.5 | obligatorio |  |
| 6.1.8 | 6.5.4 |  | SSL en producción |
| 6.1.8 | 6.5.4 | obligatorio |  |
| 6.2.1 | 6.2.2 |  | build artifact |
| 6.2.1 | 6.2.2 | obligatorio |  |
| 6.2.1 | 6.2.6 | obligatorio |  |
| 6.2.2 | 6.2.6 | obligatorio |  |
| 6.2.2 | 6.3.1 |  | deploy automático |
| 6.2.2 | 6.3.1 | obligatorio |  |
| 6.2.2 | 6.5.1 |  | deploy con approval |
| 6.2.3 | 6.2.1 |  | build step |
| 6.2.3 | 6.2.2 |  | build step |
| 6.2.3 | 6.2.4 | obligatorio |  |
| 6.2.4 | 6.3.1 |  | deploy execution |
| 6.2.4 | 6.5.1 |  | deploy execution |
| 6.2.4 | 6.7.1 | obligatorio |  |
| 6.3.1 | 6.3.2 | obligatorio |  |
| 6.3.1 | 6.3.3 | co-dependencia |  |
| 6.3.1 | 6.3.4 |  | verificación |
| 6.3.1 | 6.3.4 | obligatorio |  |
| 6.3.1 | 6.4.1 |  | smoke test en staging |
| 6.3.1 | 6.7.3 | obligatorio |  |
| 6.3.3 | 6.3.4 | obligatorio |  |
| 6.3.4 | 6.4.1 |  | si health pasa, QA procede |
| 6.3.4 | 6.4.1 | obligatorio |  |
| 6.4.1 | 6.4.2 | co-dependencia |  |
| 6.4.1 | 6.4.3 |  | aprobación |
| 6.4.1 | 6.4.3 | obligatorio |  |
| 6.4.2 | 6.4.3 |  | evidencia |
| 6.4.2 | 6.4.3 | obligatorio |  |
| 6.4.3 | 6.5.1 |  | gate de entrada |
| 6.4.3 | 6.5.1 | obligatorio |  |
| 6.5.1 | 6.5.2 |  | post-deploy deliverables |
| 6.5.1 | 6.5.2 | obligatorio |  |
| 6.5.1 | 6.5.4 | obligatorio |  |
| 6.5.1 | 6.5.6 | co-dependencia |  |
| 6.5.1 | 6.6.1 |  | monitoring activo |
| 6.5.1 | 6.6.1 | obligatorio |  |
| 6.5.1 | 6.6.3 | obligatorio |  |
| 6.5.1 | 6.6.4 | obligatorio |  |
| 6.5.1 | 6.6.5 | obligatorio |  |
| 6.5.1 | 6.6.6 | obligatorio | 24h después |
| 6.5.3 | 6.5.2 | obligatorio |  |
| 6.5.3 | 6.5.2 |  |  |
| 6.6.1 | 6.6.2 | obligatorio |  |
| 6.6.1 | 7.1.1 |  | datos del dashboard |
| 6.6.1 | 7.1.1 | obligatorio |  |
| 6.6.1 | 7.1.2 | obligatorio |  |
| 6.6.3 | 7.1.3 |  |  |
| 6.6.4 | 6.6.1 | obligatorio |  |
| 6.6.4 | 6.6.1 |  | data source |
| 6.6.4 | 6.6.2 |  | conditions |
| 6.6.4 | 7.1.2 | obligatorio |  |
| 6.6.4 | 7.6.1 | obligatorio |  |
| 6.6.5 | 7.1.3 |  |  |
| 6.6.5 | 7.1.3 | obligatorio |  |
| 6.6.5 | 7.3.3 |  |  |
| 6.6.6 | 7.1.4 |  | primer data point |
| 6.7.1 | 6.7.2 |  |  |
| 6.7.1 | 6.7.2 | obligatorio |  |
| 6.7.1 | 6.7.3 |  |  |
| 6.7.1 | 6.7.4 | obligatorio |  |
| 6.7.2 | 6.7.3 |  |  |
| 6.7.2 | 6.7.3 | obligatorio |  |
| 6.7.2 | 6.7.4 | obligatorio |  |
| 6.7.3 | 6.5.1 | obligatorio |  |
| 6.7.3 | 6.5.1 |  | prerequisito |
| 7.1.1 | 7.1.4 |  | data de uptime |
| 7.1.1 | 7.1.4 | obligatorio | data sources |
| 7.1.2 | 7.1.4 |  | data de performance |
| 7.1.2 | 7.6.2 |  | trends informan capacity |
| 7.1.3 | 7.3.1 |  | errores críticos disparan hotfixes |
| 7.1.3 | 7.3.3 |  | nuevos bugs identificados |
| 7.2.1 | 7.2.2 |  | sistema configurado según el proceso |
| 7.2.1 | 7.2.2 | obligatorio | proceso que el sistema implementa |
| 7.2.1 | 7.2.3 |  | SLAs de soporte |
| 7.2.1 | 7.2.3 | obligatorio |  |
| 7.2.1 | 7.3.1 |  | bugs de soporte que necesitan hotfix |
| 7.2.2 | 7.2.4 |  | métricas del ticket system |
| 7.2.2 | 7.2.4 | obligatorio | data source |
| 7.2.2 | 7.3.3 |  | bugs como tickets |
| 7.2.2 | 7.3.3 | obligatorio | donde viven los bugs |
| 7.2.3 | 7.2.2 |  | SLA tracking configurado |
| 7.2.3 | 7.2.4 |  | SLA compliance como métrica |
| 7.2.3 | 7.2.4 | obligatorio | targets |
| 7.2.4 | 7.1.4 |  | support data |
| 7.3.1 | 7.3.2 |  | releases ejecutadas con este proceso |
| 7.3.1 | 7.3.2 | obligatorio |  |
| 7.3.3 | 7.3.1 |  | critical bugs → hotfix |
| 7.4.2 | 7.4.3 |  | flags como mecanismo de A/B |
| 7.4.2 | 7.4.3 | obligatorio | mecanismo de split |
| 7.4.4 | 7.4.1 |  | items a incluir |
| 7.5.1 | 7.5.4 |  | vulnerabilidad cerrada |
| 7.5.2 | 7.5.4 |  | CVEs cerradas |
| 7.5.3 | 7.5.1 |  | findings → patches |
| 7.5.3 | 7.5.4 |  | findings reportados |
| 7.5.4 | 7.5.1 |  | vulnerabilidades a parchear |
| 7.5.4 | 7.5.2 |  | dependencias a actualizar |
| 7.6.1 | 7.6.2 |  | trends informan projections |
| 7.6.1 | 7.6.2 | obligatorio | data de trends |
| 7.6.1 | 7.6.3 |  | tuning basado en datos reales |
| 7.6.1 | 7.6.3 | obligatorio | data para tuning |
| 7.6.1 | 7.6.4 |  | over-provisioning identificado |
| 7.6.1 | 7.6.4 | obligatorio | utilization data |
| 7.6.2 | 7.6.3 |  | adjustment basado en projections |

---

## 7. Próximo Paso Operativo

Antes de usar este catálogo para carga final en VTT o para un Project Plan ejecutable del PJM, completar:

1. `project_id_vtt`
2. `phase_ids_vtt` por fase
3. `team_uuids` por rol
4. `hours` por deliverable
5. `complexity` por deliverable

Una vez completados esos campos, este catálogo ya puede servir como base directa para:

- generación de seed de deliverables/tareas
- HO operativo de carga VTT
- trazabilidad de dependencias entre deliverables

