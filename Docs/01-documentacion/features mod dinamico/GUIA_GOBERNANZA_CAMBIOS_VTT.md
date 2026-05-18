# GUÍA DE GOBERNANZA: Administración de Cambios en VTT

| Campo | Valor |
|-------|-------|
| **Documento** | GUIA_GOBERNANZA_CAMBIOS_VTT.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-04 |
| **Autor** | PM (Martin Rivas) |
| **Propósito** | Definir cómo se administran releases, features y cambios al modelo dentro del sistema VTT |
| **Estado** | ✅ Activo |

---

## 1. OBJETIVO

Establecer el proceso para:
1. Dar de alta nuevos releases/features en el sistema
2. Detectar y gestionar gaps del modelo dinámico
3. Controlar cambios mediante tareas y fases dentro de VTT
4. Mantener trazabilidad de todo lo que se implementa

---

## 2. FLUJO DE ALTA DE NUEVO RELEASE/FEATURE

### 2.1 Diagrama General

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ALTA DE NUEVO RELEASE/FEATURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. PM recibe requerimiento                                            │
│     │                                                                   │
│     ▼                                                                   │
│  2. PM genera documento base (ej: R3_METRICAS_PLANNING_COSTOS.pdf)     │
│     │                                                                   │
│     ▼                                                                   │
│  3. PM + Claude analizan mapeo a estructura V4                         │
│     │                                                                   │
│     ├── ¿Mapea sin gaps? ──────────────────────────────────────────┐   │
│     │         │                                                     │   │
│     │         ▼                                                     │   │
│     │   4a. Generar SETUP_TEORICO_[RELEASE].md                     │   │
│     │         │                                                     │   │
│     │         ▼                                                     │   │
│     │   5a. PJM ejecuta setup en sistema                           │   │
│     │                                                               │   │
│     └── ¿Hay gaps? ────────────────────────────────────────────────┘   │
│               │                                                         │
│               ▼                                                         │
│         4b. Clasificar gap (ver sección 3)                             │
│               │                                                         │
│               ▼                                                         │
│         5b. Crear tarea/CR/addendum según severidad                    │
│               │                                                         │
│               ▼                                                         │
│         6b. Resolver gap → volver a paso 4a                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Entregables por Paso

| Paso | Entregable | Responsable |
|------|------------|-------------|
| 1 | Documento de requerimiento | PM |
| 2 | Documento base del release/feature | PM |
| 3 | Análisis de mapeo | PM + Claude |
| 4a | SETUP_TEORICO_[RELEASE].md | Claude |
| 5a | Release/sprints/deliveries en sistema | PJM |
| 4b | Nota de gap con clasificación | Claude |
| 5b | Tarea/CR/Addendum | PM |

---

## 3. CLASIFICACIÓN DE GAPS

### 3.1 Tipos de Gap

| Tipo | Descripción | Severidad | Vehículo | Tiempo Resolución |
|------|-------------|-----------|----------|-------------------|
| **CONFIG** | Falta seed en catálogo existente | Baja | Tarea en sprint actual | < 1 día |
| **CAMPO** | Falta campo en tabla existente | Media | Change Request | 1-3 días |
| **TABLA** | Falta tabla completa | Media-Alta | Change Request | 3-5 días |
| **CONCEPTO** | Falta concepto en el modelo | Alta | Addendum + Sprint dedicado | 1-2 semanas |

### 3.2 Cómo se Registra Cada Tipo

#### Gap tipo CONFIG

```
Crear en sistema:
- Task en sprint actual
- Phase: 03-development
- Delivery: "Configuración de catálogos"
- Descripción: "Agregar seed X al catálogo Y"
```

#### Gap tipo CAMPO

```
Crear en sistema:
- Change Request (TrackableItem tipo CR)
- Vinculado al release afectado
- Task de migración en sprint siguiente
```

#### Gap tipo TABLA

```
Crear en sistema:
- Change Request (TrackableItem tipo CR)
- Sprint dedicado para implementación
- Deliverables: Schema, Migration, API, Tests
```

#### Gap tipo CONCEPTO

```
Crear en sistema:
- Addendum (documento fuera de sistema)
- Nuevo release o sprint para implementación
- Ciclo SDLC completo
```

---

## 4. ESTRUCTURA DE CONTROL EN SISTEMA

### 4.1 Proyecto de Gobernanza

```
Project: VTT
└── Release: R-GOV (Gobernanza y Mejoras)
    │
    ├── Sprint: GOV-GAPS (Gestión de Gaps)
    │   └── Tasks: Gaps detectados durante análisis
    │
    ├── Sprint: GOV-CR (Change Requests)
    │   └── Tasks: CRs aprobados pendientes de implementar
    │
    └── Sprint: GOV-HOTFIX (Hotfixes)
        └── Tasks: Correcciones urgentes
```

### 4.2 Catálogo de Tipos de TrackableItem para Gobernanza

| Code | Nombre | Uso |
|------|--------|-----|
| `GAP` | Gap Detectado | Cuando se detecta un gap durante análisis |
| `CR` | Change Request | Solicitud formal de cambio al modelo |
| `HOTFIX` | Hotfix | Corrección urgente |
| `IMPROVEMENT` | Mejora | Mejora no urgente |

### 4.3 Flujo de Estados

```
GAP detectado
    │
    ▼
[gap_identified] ─── PM clasifica ───► [gap_classified]
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
                    ▼                         ▼                         ▼
            [CONFIG]                    [CAMPO/TABLA]              [CONCEPTO]
                    │                         │                         │
                    ▼                         ▼                         ▼
            Crear Task                  Crear CR                  Crear Addendum
                    │                         │                         │
                    ▼                         ▼                         ▼
            [in_progress]              [cr_pending]              [addendum_draft]
                    │                         │                         │
                    ▼                         ▼                         ▼
            [completed]                [cr_approved]             [addendum_approved]
                                              │                         │
                                              ▼                         ▼
                                        Crear Sprint              Crear Release
```

---

## 5. REGISTRO DE GAPS

### 5.1 Tabla de Seguimiento

| ID | Fecha | Release | Descripción | Tipo | Severidad | Estado | Resolución |
|----|-------|---------|-------------|------|-----------|--------|------------|
| GAP-R3-001 | 2026-04-04 | R3 | Campo `dependsOn` faltante en `sprints` | CAMPO | Media | ⬜ Pendiente | — |

### 5.2 Formato de Registro en Sistema

```json
{
  "type": "GAP",
  "code": "GAP-R3-001",
  "title": "Campo dependsOn faltante en sprints",
  "description": "El modelo V4 no tiene campo dependsOn en tabla sprints para modelar dependencias entre sprints",
  "severity": "media",
  "releaseId": "<R3_ID>",
  "status": "gap_identified",
  "resolution": null
}
```

---

## 6. DOCUMENTOS DE GOBERNANZA

### 6.1 Inventario de Documentos

| Documento | Propósito | Cuándo se Genera |
|-----------|-----------|------------------|
| `SETUP_TEORICO_[RELEASE].md` | Mapeo de release a estructura V4 | Al recibir nuevo release |
| `NOTA_GAP_[ID].md` | Detalle de gap detectado | Al detectar gap |
| `CR_[ID].md` | Change Request formal | Cuando gap es CAMPO o TABLA |
| `ADDENDUM_[NOMBRE].md` | Extensión del modelo | Cuando gap es CONCEPTO |
| `GUIA_GOBERNANZA_CAMBIOS_VTT.md` | Este documento | Una vez, se actualiza |

### 6.2 Ubicación de Documentos

```
/docs/governance/
├── GUIA_GOBERNANZA_CAMBIOS_VTT.md (este documento)
├── gaps/
│   ├── GAP-R3-001.md
│   └── ...
├── change-requests/
│   ├── CR-001.md
│   └── ...
├── setups/
│   ├── SETUP_TEORICO_R3_METRICAS_PLANNING_COSTOS.md
│   └── ...
└── addendums/
    ├── ADDENDUM_TRAZABILIDAD_V4.md
    └── ...
```

---

## 7. CHECKLIST PARA NUEVO RELEASE/FEATURE

```
RECEPCIÓN:
[ ] Documento de requerimiento recibido
[ ] Nombre del release definido (ej: R3)
[ ] Alcance general identificado

ANÁLISIS:
[ ] Mapeo a estructura V4 completado
[ ] Sprints identificados
[ ] Deliverables por sprint listados
[ ] Dependencias entre sprints documentadas
[ ] Gaps detectados (si hay)

DOCUMENTACIÓN:
[ ] SETUP_TEORICO_[RELEASE].md generado
[ ] Gaps registrados en tabla de seguimiento
[ ] CRs creados (si aplica)

SETUP EN SISTEMA:
[ ] Release creado en VTT
[ ] Sprints creados
[ ] Deliverables creados
[ ] Dependencias documentadas
[ ] Estado inicial: planned

INICIO:
[ ] Primer sprint activado
[ ] SA asignado para análisis
[ ] Ciclo SDLC iniciado
```

---

## 8. RESPONSABILIDADES

| Rol | Responsabilidad en Gobernanza |
|-----|-------------------------------|
| **PM** | Recibir requerimientos, aprobar CRs, cerrar gaps |
| **Claude (PM Assistant)** | Analizar mapeo, detectar gaps, generar setups |
| **PJM** | Ejecutar setup en sistema, coordinar resolución de gaps |
| **SA** | Analizar gaps tipo CONCEPTO |
| **AR** | Validar CRs de tipo TABLA o CONCEPTO |
| **TL** | Implementar resolución de gaps tipo CAMPO/TABLA |

---

## 9. MÉTRICAS DE GOBERNANZA

| Métrica | Descripción | Meta |
|---------|-------------|------|
| Gaps detectados por release | Cantidad de gaps identificados | < 5 por release |
| Tiempo de resolución de gap | Días desde detección hasta cierre | CONFIG < 1d, CAMPO < 5d |
| CRs pendientes | Change requests sin resolver | < 3 simultáneos |
| Cobertura de setup | % de releases con SETUP_TEORICO | 100% |

---

## 10. HISTORIAL DE CAMBIOS

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-04-04 | Documento creado | PM |

---

**Documento:** GUIA_GOBERNANZA_CAMBIOS_VTT.md  
**Versión:** 1.0  
**Estado:** ✅ Activo  
**Fecha:** 2026-04-04

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
