# SETUP TEÓRICO: R3 — Métricas, Planning y Costos

| Campo | Valor |
|-------|-------|
| **Documento** | SETUP_TEORICO_R3_METRICAS_PLANNING_COSTOS.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-04 |
| **Autor** | PM (Martin Rivas) |
| **Proyecto** | VTT (Virtual Teams Tracking) |
| **Release** | R3 |
| **Estado** | ✅ Setup teórico definido |

---

## 1. MAPEO A ESTRUCTURA V4

### 1.1 Jerarquía Aplicada

```
Project: VTT
└── Release: R3 - Métricas, Planning y Costos
    │
    ├── Sprint: P0-ACTN (Fundamentos)
    │   ├── Phase: 01-analysis
    │   ├── Phase: 02-design
    │   ├── Phase: 03-development
    │   └── Phase: 04-testing
    │
    ├── Sprint: P1-PLANNING (Planning V2)
    │   ├── Phase: 01-analysis
    │   ├── Phase: 02-design
    │   ├── Phase: 03-development
    │   └── Phase: 04-testing
    │
    ├── Sprint: P2-METRICAS (Métricas)
    │   └── ... ciclo SDLC completo
    │
    ├── Sprint: P3-COSTOS (Costos/Tokens)
    │   └── ... ciclo SDLC completo
    │
    ├── Sprint: P4-SETTINGS (Settings Proyecto)
    │   └── ... ciclo SDLC completo
    │
    └── Sprint: P5-DASHBOARD (Dashboard UX)
        └── ... ciclo SDLC completo
```

### 1.2 Configuración del Release

| Campo | Valor |
|-------|-------|
| `releases.code` | `R3` |
| `releases.name` | `Métricas, Planning y Costos` |
| `releases.projectId` | `<VTT_PROJECT_ID>` |
| `releases.status` | `release_planned` |
| `releases.startDate` | `2026-04-04` |

---

## 2. SPRINTS DEL RELEASE

### 2.1 Inventario de Sprints

| Sprint Code | Nombre | Descripción | Dependencias |
|-------------|--------|-------------|--------------|
| `P0-ACTN` | Fundamentos | Corregir algoritmo ACTN de tiempo real | — |
| `P1-PLANNING` | Planning V2 | Planificación a dos niveles + ciclo de vida de fase | P0-ACTN |
| `P2-METRICAS` | Métricas | Sistema de ~70 KPIs | P0-ACTN |
| `P3-COSTOS` | Costos/Tokens | Tracking de consumo de tokens por agente | P0-ACTN |
| `P4-SETTINGS` | Settings Proyecto | Modificación de config post-creación | P1, P2, P3 |
| `P5-DASHBOARD` | Dashboard UX | Visualización unificada | P1, P2, P3, P4 |

### 2.2 Diagrama de Dependencias

```
                    P0-ACTN (Fundamentos)
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    P1-PLANNING      P2-METRICAS      P3-COSTOS
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    P4-SETTINGS
                           │
                           ▼
                    P5-DASHBOARD
```

### 2.3 Configuración por Sprint

#### Sprint P0-ACTN

| Campo | Valor |
|-------|-------|
| `sprints.code` | `P0-ACTN` |
| `sprints.name` | `Fundamentos` |
| `sprints.releaseId` | `<R3_RELEASE_ID>` |
| `sprints.order` | `1` |
| `sprints.status` | `sprint_planned` |

#### Sprint P1-PLANNING

| Campo | Valor |
|-------|-------|
| `sprints.code` | `P1-PLANNING` |
| `sprints.name` | `Planning V2` |
| `sprints.releaseId` | `<R3_RELEASE_ID>` |
| `sprints.order` | `2` |
| `sprints.status` | `sprint_planned` |
| `sprints.dependsOn` | `P0-ACTN` |

#### Sprint P2-METRICAS

| Campo | Valor |
|-------|-------|
| `sprints.code` | `P2-METRICAS` |
| `sprints.name` | `Métricas` |
| `sprints.releaseId` | `<R3_RELEASE_ID>` |
| `sprints.order` | `3` |
| `sprints.status` | `sprint_planned` |
| `sprints.dependsOn` | `P0-ACTN` |

#### Sprint P3-COSTOS

| Campo | Valor |
|-------|-------|
| `sprints.code` | `P3-COSTOS` |
| `sprints.name` | `Costos/Tokens` |
| `sprints.releaseId` | `<R3_RELEASE_ID>` |
| `sprints.order` | `4` |
| `sprints.status` | `sprint_planned` |
| `sprints.dependsOn` | `P0-ACTN` |

#### Sprint P4-SETTINGS

| Campo | Valor |
|-------|-------|
| `sprints.code` | `P4-SETTINGS` |
| `sprints.name` | `Settings Proyecto` |
| `sprints.releaseId` | `<R3_RELEASE_ID>` |
| `sprints.order` | `5` |
| `sprints.status` | `sprint_planned` |
| `sprints.dependsOn` | `P1-PLANNING, P2-METRICAS, P3-COSTOS` |

#### Sprint P5-DASHBOARD

| Campo | Valor |
|-------|-------|
| `sprints.code` | `P5-DASHBOARD` |
| `sprints.name` | `Dashboard UX` |
| `sprints.releaseId` | `<R3_RELEASE_ID>` |
| `sprints.order` | `6` |
| `sprints.status` | `sprint_planned` |
| `sprints.dependsOn` | `P4-SETTINGS` |

---

## 3. DELIVERABLES POR SPRINT

### 3.1 Sprint P0-ACTN (Fundamentos)

| Delivery Code | Nombre | Phase | Documento Base |
|---------------|--------|-------|----------------|
| `D0.1` | Análisis del Algoritmo ACTN | 01-analysis | — |
| `D0.2` | Schema (tablas/campos nuevos) | 02-design | — |
| `D0.3` | Implementación BE | 03-development | — |
| `D0.4` | Tests | 04-testing | — |

### 3.2 Sprint P1-PLANNING (Planning V2)

| Delivery Code | Nombre | Phase | Documento Base |
|---------------|--------|-------|----------------|
| `D1.1` | Schema Planning V2 | 02-design | REQUISITOS_PLANNING_V2_CONSOLIDADO.md |
| `D1.2` | Algoritmo Planning V2 | 03-development | — |
| `D1.3` | Ciclo de Vida de Fase | 03-development | — |
| `D1.4` | API Planning | 03-development | — |
| `D1.5` | Gantt Dual (FE) | 03-development | — |

### 3.3 Sprint P2-METRICAS (Métricas)

| Delivery Code | Nombre | Phase | Documento Base |
|---------------|--------|-------|----------------|
| `D2.1` | Schema Métricas | 02-design | DOCUMENTO_MAESTRO_METRICAS_PLANNING_VTT_V1_2_FINAL.md |
| `D2.2` | MVP 6 Métricas (FPY, THR, CYC, EXC, APC, WIA) | 03-development | — |
| `D2.3` | Fase 2 (~15 métricas) | 03-development | — |
| `D2.4` | Fase 3 (~14 métricas) | 03-development | — |
| `D2.5` | Fase 4 (~10 métricas DORA) | 03-development | — |
| `D2.6` | API Métricas | 03-development | — |
| `D2.7` | Métricas Operativas (anomalías) | 03-development | PROPUESTA_METRICAS_OPERATIVAS_VTT_R2.md |

### 3.4 Sprint P3-COSTOS (Costos/Tokens)

| Delivery Code | Nombre | Phase | Documento Base |
|---------------|--------|-------|----------------|
| `D3.1` | Schema Costos | 02-design | ANALISIS_CONVERSACIONES_AGENTES_VTT_v1_2.md |
| `D3.2` | ImporterService (parser JSONL) | 03-development | — |
| `D3.3` | ModelPricingCatalog (admin) | 03-development | — |
| `D3.4` | API Costos | 03-development | — |

### 3.5 Sprint P4-SETTINGS (Settings Proyecto)

| Delivery Code | Nombre | Phase | Documento Base |
|---------------|--------|-------|----------------|
| `D4.1` | Análisis de Modificabilidad | 01-analysis | ADDENDUM_UX_CONFIGURACION_PROYECTO_DINAMICO_V4.md |
| `D4.2` | API Settings | 03-development | — |
| `D4.3` | UI Settings (FE) | 03-development | — |

### 3.6 Sprint P5-DASHBOARD (Dashboard UX)

| Delivery Code | Nombre | Phase | Documento Base |
|---------------|--------|-------|----------------|
| `D5.1` | Diseño UX Dashboard | 02-design | — |
| `D5.2` | Componentes FE | 03-development | — |
| `D5.3` | Integración APIs | 03-development | — |

---

## 4. FASES SDLC POR SPRINT

Cada sprint sigue el ciclo estándar VTT:

| Phase Code | Nombre | Roles Activos |
|------------|--------|---------------|
| `01-analysis` | Análisis | SA, PM |
| `02-design` | Diseño | AR, TL |
| `03-development` | Desarrollo | DB, BE, FE |
| `04-testing` | Testing | QA |
| `05-deployment` | Despliegue | DevOps |

---

## 5. PARALELISMO PERMITIDO

### 5.1 Sprints que Pueden Correr en Paralelo

Una vez completado P0-ACTN:

```
P1-PLANNING ─────────────►
P2-METRICAS ─────────────► (en paralelo)
P3-COSTOS ───────────────►
```

### 5.2 Dependencia Estricta

```
P4-SETTINGS espera: P1 + P2 + P3 completados
P5-DASHBOARD espera: P4 completado
```

---

## 6. CONFIGURACIÓN EN SISTEMA

### 6.1 Datos para Crear Release

```json
{
  "code": "R3",
  "name": "Métricas, Planning y Costos",
  "projectId": "<VTT_PROJECT_ID>",
  "status": "release_planned",
  "startDate": "2026-04-04"
}
```

### 6.2 Datos para Crear Sprints

```json
[
  { "code": "P0-ACTN", "name": "Fundamentos", "order": 1, "dependsOn": [] },
  { "code": "P1-PLANNING", "name": "Planning V2", "order": 2, "dependsOn": ["P0-ACTN"] },
  { "code": "P2-METRICAS", "name": "Métricas", "order": 3, "dependsOn": ["P0-ACTN"] },
  { "code": "P3-COSTOS", "name": "Costos/Tokens", "order": 4, "dependsOn": ["P0-ACTN"] },
  { "code": "P4-SETTINGS", "name": "Settings Proyecto", "order": 5, "dependsOn": ["P1-PLANNING", "P2-METRICAS", "P3-COSTOS"] },
  { "code": "P5-DASHBOARD", "name": "Dashboard UX", "order": 6, "dependsOn": ["P4-SETTINGS"] }
]
```

---

## 7. GAPS DETECTADOS

### 7.1 Gap: Dependencias entre Sprints

| Gap | Descripción | Severidad | Acción |
|-----|-------------|-----------|--------|
| GAP-R3-001 | El modelo V4 no tiene campo `dependsOn` en `sprints` | Media | CR para agregar campo o usar tabla de dependencias |

**Workaround temporal:** Documentar dependencias en `sprints.description` o crear `TrackableItemLink` entre sprints.

### 7.2 Gap: Sprints con Múltiples Fases SDLC

| Gap | Descripción | Severidad | Acción |
|-----|-------------|-----------|--------|
| GAP-R3-002 | Cada sprint de R3 tiene ciclo SDLC completo (analysis→testing) | Baja | No es gap, es uso válido del modelo |

**Nota:** El modelo V4 soporta que un sprint contenga todas las fases SDLC. No hay conflicto.

---

## 8. CHECKLIST DE SETUP EN SISTEMA

```
PRE-REQUISITOS:
[ ] Verificar que proyecto VTT existe en sistema
[ ] Verificar que catálogo de phases tiene 01-analysis, 02-design, 03-development, 04-testing
[ ] Verificar que StatusCatalog tiene release_planned, sprint_planned

CREAR RELEASE:
[ ] POST /api/releases con datos de sección 6.1
[ ] Verificar release creado con status release_planned

CREAR SPRINTS:
[ ] POST /api/releases/:id/sprints para P0-ACTN
[ ] POST /api/releases/:id/sprints para P1-PLANNING
[ ] POST /api/releases/:id/sprints para P2-METRICAS
[ ] POST /api/releases/:id/sprints para P3-COSTOS
[ ] POST /api/releases/:id/sprints para P4-SETTINGS
[ ] POST /api/releases/:id/sprints para P5-DASHBOARD

CREAR DELIVERABLES:
[ ] Crear deliveries de P0-ACTN (D0.1 - D0.4)
[ ] Crear deliveries de P1-PLANNING (D1.1 - D1.5)
[ ] Crear deliveries de P2-METRICAS (D2.1 - D2.7)
[ ] Crear deliveries de P3-COSTOS (D3.1 - D3.4)
[ ] Crear deliveries de P4-SETTINGS (D4.1 - D4.3)
[ ] Crear deliveries de P5-DASHBOARD (D5.1 - D5.3)

DOCUMENTAR DEPENDENCIAS:
[ ] Registrar dependencia P0 → P1, P2, P3
[ ] Registrar dependencia P1+P2+P3 → P4
[ ] Registrar dependencia P4 → P5
```

---

## 9. PRÓXIMOS PASOS

| # | Acción | Responsable | Estado |
|---|--------|-------------|--------|
| 1 | Resolver GAP-R3-001 (dependencias entre sprints) | PM/AR | ⬜ Pendiente |
| 2 | Crear release R3 en sistema | PJM | ⬜ Pendiente |
| 3 | Crear sprints P0-P5 | PJM | ⬜ Pendiente |
| 4 | Iniciar P0-ACTN con ciclo SDLC | SA | ⬜ Pendiente |

---

**Documento:** SETUP_TEORICO_R3_METRICAS_PLANNING_COSTOS.md  
**Versión:** 1.0  
**Estado:** ✅ Setup teórico definido  
**Fecha:** 2026-04-04

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
