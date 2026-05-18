# TEMPLATE — FASES Y ENTREGABLES APLICABLES

> **Cómo usar:**
> 1. Copiar a `01-PM/FASES_APLICABLES_<<PROYECTO>>.md`
> 2. Tomar el catálogo completo de `ANALISIS_FASES_COMPLETO_PARA_PM.md` (438 deliverables)
> 3. Filtrar cada deliverable con ✅ aplica o ❌ no aplica
> 4. Documentar criterios de exclusión en §CRITERIOS
> 5. Borrar este bloque antes de emitir

---

# FASES Y ENTREGABLES APLICABLES — <<NOMBRE_PROYECTO>>

| Campo | Valor |
|-------|-------|
| **Documento** | FASES_APLICABLES_<<PROYECTO>>.md |
| **Versión** | X.0 |
| **Fecha** | <<YYYY-MM-DD>> |
| **Autor** | PM (<<Nombre>>) |
| **Proyecto** | <<NOMBRE_PROYECTO>> |
| **Estado** | ✅ Aprobado PM |

---

## JERARQUÍA DEL PROYECTO (Modelo Dinámico V3)

```
<<PROYECTO>> (Project)
  └── R1 (Release)
        └── N Fases SDLC aplicables (Phase)
              └── <<N>> Deliverables individuales (Deliverable)
                    └── <<N>> Tasks (Task) — ver TASK_INDEX_SEED
```

> **Nota:** Los "deliveries" en VTT son agrupadores por subfase. Los Deliverables reales son los documentos individuales listados abajo.

---

## CRITERIOS DE FILTRADO

| Criterio | Consecuencia |
|----------|-------------|
| <<Criterio 1, ej: feature interna>> | ❌ Market research, competitive analysis, etc. |
| <<Criterio 2, ej: usuarios internos>> | ❌ User research, usability testing, etc. |
| <<Criterio 3, ej: desktop only>> | ❌ Mobile/tablet wireframes, dark mode |
| <<Criterio 4, ej: auth con SERVICE_KEY>> | ❌ OAuth integrations |
| <<Criterio 5, ej: stack sin X>> | ❌ <<exclusión específica>> |

---

## LEYENDA

| Icono | Significado |
|-------|-------------|
| ✅ | Aplica |
| ❌ | No aplica (con razón breve) |

---

## FASE 0 · DISCOVERY

**Entregables originales:** 22 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 0.1 Market Research

| # | Deliverable | Estado |
|---|-------------|--------|
| 0.1.1 | Market Research Report | ✅ / ❌ (<<razón>>) |
| ... | ... | ... |

### 0.2 Competitive Analysis

<<repetir estructura>>

### 0.3 Problem Definition

### 0.4 Value Proposition

---

## FASE 1 · PLANNING

**Entregables originales:** 33 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 1.1 Vision & Objectives
### 1.2 Scope
### 1.3 Stakeholders
### 1.4 Risks
### 1.5 Timeline
### 1.6 Budget

---

## FASE 2 · ANALYSIS

**Entregables originales:** 47 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 2.1 Functional Requirements
### 2.2 Non-Functional Requirements
### 2.3 Use Cases
### 2.4 User Stories
### 2.5 Business Rules
### 2.6 User Flows
### 2.7 Acceptance Criteria
### 2.8 Traceability Matrix

---

## FASE 3A · DESIGN UX/UI

**Entregables originales:** 72 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 3A.1 User Research
### 3A.2 Personas
### 3A.3 Information Architecture
### 3A.4 Wireframes
### 3A.5 Mockups / UI Design
### 3A.6 Prototypes
### 3A.7 Design System
### 3A.8 Usability Testing
### 3A.9 Design Handoff

---

## FASE 3B · DESIGN TECHNICAL

**Entregables originales:** 73 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 3B.1 Solution Architecture
### 3B.2 Code Architecture
### 3B.3 Database Design
### 3B.4 API Design
### 3B.5 Sequence Diagrams
### 3B.6 ADRs
### 3B.7 Security Plan
### 3B.8 Infrastructure Plan
### 3B.9 Technical Estimates

---

## FASE 4 · DEVELOPMENT

**Entregables originales:** 78 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 4.1 Environment Setup
### 4.2 Database Implementation
### 4.3 Backend Development
### 4.4 Frontend Development
### 4.5 Integrations
### 4.6 Unit Tests
### 4.7 Technical Documentation
### 4.8 Code Review

---

## FASE 5 · TESTING

**Entregables originales:** 52 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 5.1 Test Planning
### 5.2 Test Cases
### 5.3 Test Environment
### 5.4 Functional Testing
### 5.5 Integration Testing
### 5.6 E2E Testing
### 5.7 Performance Testing
### 5.8 Security Testing
### 5.9 Accessibility Testing
### 5.10 UAT
### 5.11 Bug Fixes

---

## FASE 6 · DEPLOY

**Entregables originales:** 38 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 6.1 Infrastructure Setup
### 6.2 CI/CD Configuration
### 6.3 Staging Deploy
### 6.4 Smoke Testing
### 6.5 Production Deploy
### 6.6 Post-Deploy Monitoring
### 6.7 Rollback Plan

---

## FASE 7 · OPERATIONS

**Entregables originales:** 23 · **Aplicables:** <<N>> · **Excluidos:** <<N>>

### 7.1 Monitoring
### 7.2 User Support
### 7.3 Bug Fixes
### 7.4 Incremental Improvements
### 7.5 Security Updates
### 7.6 Scaling

---

## RESUMEN EJECUTIVO

| Fase | Aplican | No aplican | Total | % Aplicabilidad |
|------|--------:|-----------:|------:|----------------:|
| 0 Discovery | <<N>> | <<N>> | 22 | <<%>> |
| 1 Planning | <<N>> | <<N>> | 33 | <<%>> |
| 2 Analysis | <<N>> | <<N>> | 47 | <<%>> |
| 3A Design UX/UI | <<N>> | <<N>> | 72 | <<%>> |
| 3B Design Technical | <<N>> | <<N>> | 73 | <<%>> |
| 4 Development | <<N>> | <<N>> | 78 | <<%>> |
| 5 Testing | <<N>> | <<N>> | 52 | <<%>> |
| 6 Deploy | <<N>> | <<N>> | 38 | <<%>> |
| 7 Operations | <<N>> | <<N>> | 23 | <<%>> |
| **TOTAL** | **<<N>>** | **<<N>>** | **438** | **<<%>>** |

---

## RESUMEN DE EXCLUSIONES

### Por razón "<<Criterio 1>>" (<<N>> deliverables)

<<Listar>>

### Por razón "<<Criterio 2>>" (<<N>> deliverables)

<<Listar>>

### Por razón "<<Criterio N>>" (<<N>> deliverables)

<<Listar>>

---

## SIGUIENTE PASO

Con los **<<N>> deliverables aplicables** definidos, el siguiente paso es:

**Generar HOs por fase**, cada uno con:
- Lista de deliverables individuales de la fase
- Responsable por deliverable
- Inputs requeridos
- Outputs esperados (archivo + ubicación V3.1)
- Criterios de aceptación
- Dependencias
- Task VTT que lo produce

---

**Documento:** FASES_APLICABLES_<<PROYECTO>>.md
**Versión:** X.0
**Estado:** ✅ Aprobado PM — <<YYYY-MM-DD>>

---

**Template source:** `TEMPLATE_FASES_APLICABLES_V1.0.md`
**Proceso asociado:** `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` (paso 3)
