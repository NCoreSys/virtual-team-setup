# FASES Y ENTREGABLES APLICABLES — Memory Service

**Documento:** FASES_APLICABLES_MEMORY_SERVICE.md  
**Versión:** 2.0  
**Fecha:** 2026-04-22  
**Autor:** PM (Martin Rivas)  
**Proyecto:** Memory Service (feature interna de VTT)  
**Estado:** ✅ Aprobado PM  

---

## CAMBIOS vs v1.0

| # | Cambio |
|---|--------|
| 1 | Filtro rehecho desde cero contra el catálogo completo (438 deliverables) |
| 2 | Criterios de exclusión consolidados y consistentes |
| 3 | Sin categorías intermedias (solo ✅ aplica / ❌ no aplica) |
| 4 | 390 aplican (vs 391 en v1.0) — ajustes en OAuth, Stored Procedures, Views, Prototypes, Accessibility |
| 5 | Referencia explícita al Modelo Dinámico V3 (jerarquía Project → Release → Phase → Deliverable → Task) |

---

## JERARQUÍA DEL PROYECTO (Modelo Dinámico V3)

```
Memory Service (Project)
  └── R1 (Release)
        └── 9 Fases SDLC aplicables (Phase)
              └── 390 Deliverables individuales (Deliverable)
                    └── 116 Tasks (Task) — ver PLAN_116_TAREAS.md
```

> **Nota:** Los 65 "deliveries" en `HO_ACTUALIZAR_TAREAS_VTT.md v2.1` son **agrupadores** por subfase SDLC (p. ej. 0.3, 0.4, 1.1, ...). Los **Deliverables reales** son los 390 documentos individuales listados en este archivo.

---

## CRITERIOS DE FILTRADO

| Criterio | Consecuencia |
|----------|-------------|
| Memory Service es **feature interna de VTT**, no producto de mercado | ❌ Market research, competitive analysis, brand guidelines |
| Usuarios = **agentes AI + developers internos** | ❌ User research externo, usability testing, anti-personas, empathy maps, card sorting, prototypes para testing |
| UI admin **desktop only** en R1 | ❌ Mobile/tablet wireframes y mockups, dark mode, responsive variants |
| Auth = **SERVICE_KEY pattern** (D-MEM-26) | ❌ OAuth integrations |
| Stack **sin Stored Procedures ni Views** (SPEC v1.9 no los usa) | ❌ SP, Views |
| Herramienta administrativa interna | ❌ Screen reader test (admin, no público) |

---

## LEYENDA

| Icono | Significado |
|-------|-------------|
| ✅ | Aplica |
| ❌ | No aplica (con razón breve) |

---

## FASE 0 · DISCOVERY

**Entregables originales:** 22 · **Aplicables:** 10 · **Excluidos:** 12

### 0.1 Market Research — ❌ No aplica (5/5 excluidos)

> Razón: Memory Service es feature interna de VTT, no producto de mercado.

| # | Deliverable | Estado |
|---|-------------|--------|
| 0.1.1 | Market Research Report | ❌ |
| 0.1.2 | TAM/SAM/SOM | ❌ |
| 0.1.3 | Market Trends | ❌ |
| 0.1.4 | Market Segments | ❌ |
| 0.1.5 | Target Market | ❌ |

### 0.2 Competitive Analysis — ❌ No aplica (7/7 excluidos)

> Razón: Feature interna, no compite en mercado.

| # | Deliverable | Estado |
|---|-------------|--------|
| 0.2.1 | Competitive Analysis Doc | ❌ |
| 0.2.2 | Competitor List | ❌ |
| 0.2.3 | Feature Comparison | ❌ |
| 0.2.4 | Pricing Comparison | ❌ |
| 0.2.5 | SWOT Analysis | ❌ |
| 0.2.6 | Market Opportunities | ❌ |
| 0.2.7 | UX Benchmarking | ❌ |

### 0.3 Problem Definition — ✅ Aplica completa (5/5)

| # | Deliverable | Estado |
|---|-------------|--------|
| 0.3.1 | Problem Statement | ✅ |
| 0.3.2 | User Pain Points | ✅ |
| 0.3.3 | Current Solutions | ✅ (VTM legacy, módulo 5F) |
| 0.3.4 | Why Now | ✅ |
| 0.3.5 | Problem Validation | ✅ (validación interna equipo VTT) |

### 0.4 Value Proposition — ✅ Aplica completa (5/5)

| # | Deliverable | Estado |
|---|-------------|--------|
| 0.4.1 | Value Proposition Canvas | ✅ |
| 0.4.2 | UVP Statement | ✅ |
| 0.4.3 | Key Differentiators | ✅ |
| 0.4.4 | Target Customer Profile | ✅ (agentes AI + devs VTT) |
| 0.4.5 | Value Hypothesis | ✅ |

---

## FASE 1 · PLANNING

**Entregables originales:** 33 · **Aplicables:** 33 · **Excluidos:** 0

### 1.1 Vision & Objectives — ✅ (6/6)

| # | Deliverable | Estado |
|---|-------------|--------|
| 1.1.1 | Vision Statement | ✅ |
| 1.1.2 | Mission Statement | ✅ |
| 1.1.3 | Product Goals | ✅ |
| 1.1.4 | Success Metrics (KPIs) | ✅ |
| 1.1.5 | North Star Metric | ✅ |
| 1.1.6 | OKRs | ✅ (de feature, no de producto) |

### 1.2 Scope — ✅ (6/6)

| # | Deliverable | Estado |
|---|-------------|--------|
| 1.2.1 | Scope Statement | ✅ |
| 1.2.2 | In-Scope | ✅ |
| 1.2.3 | Out-of-Scope | ✅ |
| 1.2.4 | MVP Definition | ✅ |
| 1.2.5 | Future Phases | ✅ |
| 1.2.6 | Assumptions | ✅ |

### 1.3 Stakeholders — ✅ (4/4)

| # | Deliverable | Estado |
|---|-------------|--------|
| 1.3.1 | Stakeholder Map | ✅ |
| 1.3.2 | Stakeholder Register | ✅ |
| 1.3.3 | RACI Matrix | ✅ |
| 1.3.4 | Communication Plan | ✅ |

### 1.4 Risks — ✅ (5/5)

| # | Deliverable | Estado |
|---|-------------|--------|
| 1.4.1 | Risk Register | ✅ |
| 1.4.2 | Risk Assessment | ✅ |
| 1.4.3 | Mitigation Plan | ✅ |
| 1.4.4 | Contingency Plan | ✅ |
| 1.4.5 | Risk Monitoring | ✅ |

### 1.5 Timeline — ✅ (7/7)

| # | Deliverable | Estado |
|---|-------------|--------|
| 1.5.1 | Project Schedule | ✅ |
| 1.5.2 | Milestones | ✅ |
| 1.5.3 | Phase Breakdown | ✅ |
| 1.5.4 | Sprint Calendar | ✅ |
| 1.5.5 | Dependencies | ✅ |
| 1.5.6 | Critical Path | ✅ |
| 1.5.7 | Buffer Time | ✅ |

### 1.6 Budget — ✅ (5/5)

| # | Deliverable | Estado |
|---|-------------|--------|
| 1.6.1 | Budget Estimate | ✅ (horas por rol) |
| 1.6.2 | Cost Breakdown | ✅ |
| 1.6.3 | Resource Plan | ✅ |
| 1.6.4 | ROI Analysis | ✅ (valor aportado al sistema VTT) |
| 1.6.5 | Budget Tracking | ✅ |

---

## FASE 2 · ANALYSIS

**Entregables originales:** 47 · **Aplicables:** 47 · **Excluidos:** 0

### 2.1 Functional Requirements — ✅ (6/6)

2.1.1 SRS Document · 2.1.2 Requirements List · 2.1.3 Priority Matrix MoSCoW · 2.1.4 Feature List · 2.1.5 Functional Decomposition · 2.1.6 Requirements Approval

### 2.2 Non-Functional Requirements — ✅ (6/6)

2.2.1 NFR Document · 2.2.2 Performance Requirements (`<500ms` contexto) · 2.2.3 Security Requirements (SERVICE_KEY) · 2.2.4 Scalability Requirements · 2.2.5 Availability Requirements · 2.2.6 Usability Requirements

### 2.3 Use Cases — ✅ (6/6)

2.3.1 Use Case Document · 2.3.2 Use Case Diagram · 2.3.3 Use Case List · 2.3.4 Detailed Use Cases · 2.3.5 Actor Definitions · 2.3.6 Use Case Relationships

### 2.4 User Stories — ✅ (6/6)

2.4.1 Product Backlog · 2.4.2 User Stories · 2.4.3 Story Map · 2.4.4 Epics · 2.4.5 Story Estimation · 2.4.6 Sprint Assignment

### 2.5 Business Rules — ✅ (7/7)

2.5.1 Business Rules Document · 2.5.2 Rules List · 2.5.3 Validation Rules · 2.5.4 Calculation Rules (costo USD) · 2.5.5 Authorization Rules (SERVICE_KEY policy) · 2.5.6 State Transition Rules (PENDING→PROCESSING→IMPORTED/ERROR) · 2.5.7 Business Glossary

### 2.6 User Flows — ✅ (7/7)

2.6.1 User Flow Diagrams · 2.6.2 Happy Path Flows · 2.6.3 Error Flows · 2.6.4 Edge Cases · 2.6.5 User Journey Maps (agentes usando el sistema) · 2.6.6 Task Flows · 2.6.7 Navigation Map (UI Memory Service)

### 2.7 Acceptance Criteria — ✅ (5/5)

2.7.1 Acceptance Criteria Doc · 2.7.2 Criteria per Story · 2.7.3 Definition of Done · 2.7.4 Definition of Ready · 2.7.5 Test Scenarios

### 2.8 Traceability Matrix — ✅ (4/4)

2.8.1 Traceability Matrix · 2.8.2 RF to US Mapping · 2.8.3 US to Test Mapping · 2.8.4 Coverage Report

---

## FASE 3A · DESIGN UX/UI

**Entregables originales:** 72 · **Aplicables:** 40 · **Excluidos:** 32

### 3A.1 User Research — ❌ No aplica (9/9 excluidos)

> Razón: Usuarios son agentes AI + developers internos. No hay usuarios externos que entrevistar ni encuestar.

3A.1.1 a 3A.1.9 — todos excluidos.

### 3A.2 Personas — aplica adaptado (6/8)

| # | Deliverable | Estado |
|---|-------------|--------|
| 3A.2.1 | Personas Document | ✅ (agentes y roles que interactúan) |
| 3A.2.2 | Persona Cards | ✅ |
| 3A.2.3 | Primary Persona | ✅ (ej: TL consultando historial) |
| 3A.2.4 | Secondary Personas | ✅ |
| 3A.2.5 | Anti-Personas | ❌ No aplica herramienta interna |
| 3A.2.6 | Scenarios | ✅ |
| 3A.2.7 | Empathy Maps | ❌ No aplica herramienta interna |
| 3A.2.8 | Jobs to be Done | ✅ |

### 3A.3 Information Architecture — aplica adaptado (7/8)

| # | Deliverable | Estado |
|---|-------------|--------|
| 3A.3.1 | Site Map | ✅ |
| 3A.3.2 | Navigation Structure | ✅ |
| 3A.3.3 | Navigation Patterns | ✅ |
| 3A.3.4 | Content Inventory | ✅ |
| 3A.3.5 | Taxonomy | ✅ |
| 3A.3.6 | Card Sorting Results | ❌ No aplica, sin usuarios externos |
| 3A.3.7 | Menu Structure | ✅ |
| 3A.3.8 | URL Structure | ✅ |

### 3A.4 Wireframes — aplica adaptado (7/9)

| # | Deliverable | Estado |
|---|-------------|--------|
| 3A.4.1 | Wireframe Document | ✅ |
| 3A.4.2 | Low-Fi Wireframes | ✅ |
| 3A.4.3 | Mid-Fi Wireframes | ✅ |
| 3A.4.4 | Desktop Wireframes | ✅ |
| 3A.4.5 | Mobile Wireframes | ❌ Admin tool desktop only |
| 3A.4.6 | Tablet Wireframes | ❌ Admin tool desktop only |
| 3A.4.7 | Wireframe Annotations | ✅ |
| 3A.4.8 | Wireframe Flows | ✅ |
| 3A.4.9 | Responsive Breakpoints | ✅ (solo desktop) |

### 3A.5 Mockups / UI Design — aplica adaptado (6/10)

| # | Deliverable | Estado |
|---|-------------|--------|
| 3A.5.1 | UI Mockups Complete | ✅ |
| 3A.5.2 | Desktop Mockups | ✅ |
| 3A.5.3 | Mobile Mockups | ❌ Desktop only |
| 3A.5.4 | Tablet Mockups | ❌ Desktop only |
| 3A.5.5 | Component States | ✅ |
| 3A.5.6 | Empty States | ✅ |
| 3A.5.7 | Error States | ✅ |
| 3A.5.8 | Loading States | ✅ |
| 3A.5.9 | Dark Mode | ❌ No en R1 |
| 3A.5.10 | Responsive Variants | ❌ Desktop only |

### 3A.6 Prototypes — ❌ No aplica (6/6 excluidos)

> Razón: Herramienta interna, sin usuarios externos para testing.

3A.6.1 a 3A.6.6 — todos excluidos.

### 3A.7 Design System — aplica adaptado (9/10)

| # | Deliverable | Estado |
|---|-------------|--------|
| 3A.7.1 | Design Tokens | ✅ |
| 3A.7.2 | Color Palette | ✅ |
| 3A.7.3 | Typography Scale | ✅ |
| 3A.7.4 | Spacing System | ✅ |
| 3A.7.5 | Icon Library | ✅ |
| 3A.7.6 | Component Library | ✅ |
| 3A.7.7 | Component Documentation | ✅ |
| 3A.7.8 | Pattern Library | ✅ |
| 3A.7.9 | Brand Guidelines | ❌ Herramienta interna |
| 3A.7.10 | Asset Library | ✅ |

### 3A.8 Usability Testing — ❌ No aplica (7/7 excluidos)

> Razón: Herramienta interna. No hay usuarios externos para testing.

3A.8.1 a 3A.8.7 — todos excluidos.

### 3A.9 Design Handoff — ✅ (5/5)

3A.9.1 Handoff Document · 3A.9.2 Specs Export · 3A.9.3 Asset Export · 3A.9.4 CSS Variables · 3A.9.5 Redlines

---

## FASE 3B · DESIGN TECHNICAL

**Entregables originales:** 73 · **Aplicables:** 73 · **Excluidos:** 0

### 3B.1 Solution Architecture — ✅ (7/7)

3B.1.1 Architecture Document · 3B.1.2 System Context Diagram (C4 L1) · 3B.1.3 Container Diagram (C4 L2) · 3B.1.4 Component Diagram (C4 L3) · 3B.1.5 Technology Stack · 3B.1.6 Integration Points · 3B.1.7 Data Flow Diagram

### 3B.2 Code Architecture — ✅ (6/6)

3B.2.1 Folder Structure · 3B.2.2 Coding Standards · 3B.2.3 Design Patterns · 3B.2.4 Module Dependencies · 3B.2.5 Naming Conventions · 3B.2.6 Error Handling Strategy

### 3B.3 Database Design — ✅ (8/8)

3B.3.1 ERD Complete · 3B.3.2 Schema Definition (Prisma) · 3B.3.3 Table Specifications · 3B.3.4 Index Strategy · 3B.3.5 Data Dictionary · 3B.3.6 Migration Strategy · 3B.3.7 Seed Data Plan · 3B.3.8 Backup Strategy

### 3B.4 API Design — ✅ (11/11)

3B.4.1 OpenAPI Spec · 3B.4.2 Endpoints List · 3B.4.3 Request/Response Examples · 3B.4.4 Pagination Strategy · 3B.4.5 Error Codes (MEM-ERR-*) · 3B.4.6 Authentication Spec · 3B.4.7 Authorization Spec · 3B.4.8 Rate Limiting · 3B.4.9 Versioning Strategy · 3B.4.10 Postman Collection · 3B.4.11 API Guidelines

### 3B.5 Sequence Diagrams — ✅ (6/6)

3B.5.1 Sequence Diagrams Doc · 3B.5.2 Auth Flow (SERVICE_KEY) · 3B.5.3 Main Business Flows (import, context, cleanup) · 3B.5.4 Error Flows · 3B.5.5 Integration Flows (Runtime, Prompt Builder, Hook Manager) · 3B.5.6 Async Flows (cleanup job)

### 3B.6 ADR — ✅ (4/4)

3B.6.1 ADR Template · 3B.6.2 ADR Index · 3B.6.3 ADR Documents (D-MEM-01..43 + D-INT-01..05) · 3B.6.4 Decision Log

### 3B.7 Security Plan — ✅ (11/11)

3B.7.1 Security Plan · 3B.7.2 Authentication Design (SERVICE_KEY) · 3B.7.3 Authorization Design · 3B.7.4 Data Protection Plan · 3B.7.5 Encryption Strategy · 3B.7.6 OWASP Checklist · 3B.7.7 Security Headers · 3B.7.8 Secrets Management · 3B.7.9 Input Validation Rules · 3B.7.10 Security Logging · 3B.7.11 Incident Response Plan

### 3B.8 Infrastructure Plan — ✅ (11/11)

3B.8.1 Infrastructure Plan · 3B.8.2 Infrastructure Diagram (Hetzner 77.42.88.106) · 3B.8.3 Server Specifications · 3B.8.4 Network Design (shared-network) · 3B.8.5 Environment Matrix · 3B.8.6 Scaling Strategy · 3B.8.7 Backup Strategy · 3B.8.8 Disaster Recovery Plan · 3B.8.9 Cost Estimate · 3B.8.10 SLA Definition · 3B.8.11 Monitoring Strategy

### 3B.9 Technical Estimates — ✅ (9/9)

3B.9.1 Technical Estimates · 3B.9.2 Story Points · 3B.9.3 Task Breakdown · 3B.9.4 Effort Matrix · 3B.9.5 Complexity Assessment · 3B.9.6 Risk-adjusted Estimates · 3B.9.7 Dependencies Map · 3B.9.8 Velocity Baseline · 3B.9.9 Capacity Planning

---

## FASE 4 · DEVELOPMENT

**Entregables originales:** 78 · **Aplicables:** 75 · **Excluidos:** 3

### 4.1 Environment Setup — ✅ (10/10)

4.1.1 Development Environment · 4.1.2 Environment Setup Guide · 4.1.3 Environment Variables · 4.1.4 Docker Compose · 4.1.5 Makefile / Scripts · 4.1.6 IDE Configuration · 4.1.7 Pre-commit Hooks · 4.1.8 Git Configuration · 4.1.9 Linter Configuration · 4.1.10 Formatter Configuration

### 4.2 Database Implementation — aplica adaptado (8/10)

| # | Deliverable | Estado |
|---|-------------|--------|
| 4.2.1 | Initial Migration | ✅ |
| 4.2.2 | Schema Migrations | ✅ |
| 4.2.3 | Seed Data (10 catálogos) | ✅ |
| 4.2.4 | Test Data | ✅ |
| 4.2.5 | Indexes (incluye partial + GIN) | ✅ |
| 4.2.6 | Constraints | ✅ |
| 4.2.7 | Stored Procedures | ❌ SPEC v1.9 no usa SP |
| 4.2.8 | Views | ❌ SPEC v1.9 no usa Views |
| 4.2.9 | Migration Guide | ✅ |
| 4.2.10 | Rollback Scripts | ✅ |

### 4.3 Backend Development — ✅ (15/15)

4.3.1 a 4.3.15 — todos aplican (endpoints REST, services, models, repositories, DTOs, workers, middlewares, utils, unit tests BE, integration tests, API docs Swagger, Postman collection, BE README, error handling, logging).

### 4.4 Frontend Development — ✅ (15/15)

4.4.1 Components · 4.4.2 Pages · 4.4.3 Layouts · 4.4.4 Hooks · 4.4.5 State Management · 4.4.6 API Client · 4.4.7 Types/Interfaces · 4.4.8 Styles · 4.4.9 Utils · 4.4.10 Unit Tests FE · 4.4.11 Component Tests · 4.4.12 Storybook · 4.4.13 Frontend README · 4.4.14 Accessibility (básico) · 4.4.15 Responsive Implementation (desktop only)

### 4.5 Integrations — aplica adaptado (8/9)

| # | Deliverable | Estado |
|---|-------------|--------|
| 4.5.1 | Integration Code | ✅ |
| 4.5.2 | API Clients | ✅ |
| 4.5.3 | Webhooks | ✅ |
| 4.5.4 | OAuth Integrations | ❌ Memory Service usa SERVICE_KEY |
| 4.5.5 | Third-party SDKs | ✅ (Anthropic SDK) |
| 4.5.6 | Integration Tests | ✅ |
| 4.5.7 | Integration Docs | ✅ |
| 4.5.8 | Error Handling | ✅ |
| 4.5.9 | Retry Logic | ✅ |

### 4.6 Unit Tests — ✅ (7/7)

4.6.1 a 4.6.7

### 4.7 Technical Documentation — ✅ (8/8)

4.7.1 a 4.7.8

### 4.8 Code Review — ✅ (4/4)

4.8.1 PR Reviews · 4.8.2 Code Quality Report · 4.8.3 Technical Debt Log · 4.8.4 Refactoring Plan

---

## FASE 5 · TESTING

**Entregables originales:** 52 · **Aplicables:** 51 · **Excluidos:** 1

### 5.1 Test Planning — ✅ (5/5)
### 5.2 Test Cases — ✅ (4/4)
### 5.3 Test Environment — ✅ (4/4)
### 5.4 Functional Testing — ✅ (5/5)
### 5.5 Integration Testing — ✅ (4/4)
### 5.6 E2E Testing — ✅ (5/5)
### 5.7 Performance Testing — ✅ (6/6) — **crítico: `<500ms` en `GET /context`**
### 5.8 Security Testing — ✅ (7/7)

### 5.9 Accessibility Testing — aplica adaptado (3/4)

| # | Deliverable | Estado |
|---|-------------|--------|
| 5.9.1 | WCAG Audit | ✅ (básico) |
| 5.9.2 | Accessibility Score | ✅ |
| 5.9.3 | Screen Reader Test | ❌ Herramienta interna admin |
| 5.9.4 | Keyboard Navigation | ✅ |

### 5.10 UAT — ✅ (5/5) — adaptado con equipo VTT interno

5.10.1 UAT Plan · 5.10.2 UAT Test Cases · 5.10.3 UAT Results · 5.10.4 User Feedback · 5.10.5 UAT Sign-off

### 5.11 Bug Fixes — ✅ (3/3)

5.11.1 Bug Fixes Implemented · 5.11.2 Regression Tests · 5.11.3 Bug Resolution Report

---

## FASE 6 · DEPLOY

**Entregables originales:** 38 · **Aplicables:** 38 · **Excluidos:** 0

### 6.1 Infrastructure Setup — ✅ (8/8)

6.1.1 Infrastructure Ready · 6.1.2 Servers Provisioned · 6.1.3 Network Configured · 6.1.4 Security Groups · 6.1.5 Load Balancer · 6.1.6 Database Ready · 6.1.7 Storage Ready · 6.1.8 SSL Certificates

### 6.2 CI/CD Configuration — ✅ (6/6)

6.2.1 CI Pipeline · 6.2.2 CD Pipeline · 6.2.3 Build Scripts · 6.2.4 Deploy Scripts · 6.2.5 Environment Configs · 6.2.6 Pipeline Documentation

### 6.3 Staging Deploy — ✅ (4/4)

6.3.1 Staging Deploy · 6.3.2 Staging URL · 6.3.3 Migration Run · 6.3.4 Health Check

### 6.4 Smoke Testing — ✅ (3/3)

6.4.1 Smoke Test Results · 6.4.2 Critical Paths Verified · 6.4.3 Smoke Test Sign-off

### 6.5 Production Deploy — ✅ (6/6)

6.5.1 Production Deploy · 6.5.2 Production URL · 6.5.3 DNS Configured · 6.5.4 SSL Active · 6.5.5 Release Notes · 6.5.6 Deployment Log

### 6.6 Post-Deploy Monitoring — ✅ (6/6)

6.6.1 Monitoring Dashboard · 6.6.2 Alerts Configured · 6.6.3 Log Aggregation · 6.6.4 Metrics Collection · 6.6.5 Error Tracking · 6.6.6 Post-Deploy Report (24h)

### 6.7 Rollback Plan — ✅ (5/5)

6.7.1 Rollback Plan · 6.7.2 Rollback Scripts · 6.7.3 Rollback Tested · 6.7.4 Rollback Runbook · 6.7.5 Decision Criteria

---

## FASE 7 · OPERATIONS

**Entregables originales:** 23 · **Aplicables:** 23 · **Excluidos:** 0

### 7.1 Monitoring — ✅ (4/4)

7.1.1 Uptime Reports · 7.1.2 Performance Reports · 7.1.3 Error Reports · 7.1.4 Weekly Reports

### 7.2 User Support — ✅ (4/4) — soporte interno VTT

7.2.1 Support Process · 7.2.2 Ticket System · 7.2.3 SLA Definitions · 7.2.4 Support Metrics

### 7.3 Bug Fixes — ✅ (3/3)

7.3.1 Hotfix Process · 7.3.2 Hotfix Releases · 7.3.3 Bug Tracking

### 7.4 Incremental Improvements — ✅ (4/4)

7.4.1 Minor Releases · 7.4.2 Feature Flags · 7.4.3 A/B Tests · 7.4.4 Improvement Backlog

### 7.5 Security Updates — ✅ (4/4)

7.5.1 Security Patches · 7.5.2 Dependency Updates · 7.5.3 Security Audits · 7.5.4 Vulnerability Reports

### 7.6 Scaling — ✅ (4/4)

7.6.1 Scaling Reports · 7.6.2 Capacity Planning · 7.6.3 Auto-scaling Config · 7.6.4 Cost Optimization

---

## RESUMEN EJECUTIVO

| Fase | Aplican | No aplican | Total | % Aplicabilidad |
|------|--------:|-----------:|------:|----------------:|
| 0 Discovery | 10 | 12 | 22 | 45% |
| 1 Planning | 33 | 0 | 33 | 100% |
| 2 Analysis | 47 | 0 | 47 | 100% |
| 3A Design UX/UI | 40 | 32 | 72 | 56% |
| 3B Design Technical | 73 | 0 | 73 | 100% |
| 4 Development | 75 | 3 | 78 | 96% |
| 5 Testing | 51 | 1 | 52 | 98% |
| 6 Deploy | 38 | 0 | 38 | 100% |
| 7 Operations | 23 | 0 | 23 | 100% |
| **TOTAL** | **390** | **48** | **438** | **89%** |

---

## RESUMEN DE EXCLUSIONES (48 deliverables)

### Por razón "Feature interna VTT" (12 deliverables)

Market Research (5) · Competitive Analysis (7).

### Por razón "Sin usuarios externos" (22 deliverables)

User Research (9) · Anti-Personas · Empathy Maps · Card Sorting · Prototypes (6) · Usability Testing (7) · Screen Reader Test.

### Por razón "Desktop only en R1" (8 deliverables)

Mobile Wireframes · Tablet Wireframes · Mobile Mockups · Tablet Mockups · Dark Mode · Responsive Variants · (más los breakpoints adaptados que no cuentan como exclusión).

### Por razón "Stack específico" (3 deliverables)

Stored Procedures · Views · OAuth Integrations.

### Por razón "Herramienta interna" (3 deliverables)

Brand Guidelines · (Anti-Personas, Empathy Maps, Card Sorting, Screen Reader Test ya contados arriba).

---

## SIGUIENTE PASO

Con los **390 deliverables aplicables** definidos, el siguiente paso es:

**Generar HOs por fase** (iniciando por Fase 0 Discovery con 10 deliverables), cada uno con:
- Lista de deliverables individuales
- Responsable por deliverable
- Inputs requeridos
- Outputs esperados (archivo + ubicación V3.1)
- Criterios de aceptación
- Dependencias
- Task VTT que lo produce (MEM-XXX)

---

**Documento:** FASES_APLICABLES_MEMORY_SERVICE.md  
**Versión:** 2.0  
**Estado:** ✅ Aprobado PM — 2026-04-22  
**Supersedes:** v1.0 (2026-04-18)
