# VTT.WORKFLOW-HO-001.022 — Redactar Secciones del HO Maestro

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.022` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.5.7 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PM |
| **Tipo** | [PROCESO] sub-procedimiento de redacción |

---

## 1. Propósito

PM redacta las 13-17 secciones obligatorias del HO Maestro según template canónico, citando contenido desde docs upstream sin inventar.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `template_ho_maestro` | path | templates | sí | Template canónico |
| `datos_extraidos` | objeto | WORKFLOW-021 Paso 2 | sí | Datos del paquete técnico |
| `pendientes_clasificados` | objeto | WORKFLOW-021 Paso 3 | sí | P0/GATE/DIFERIDO |
| `operativo_proyecto` | path | configuración | sí | UUIDs del equipo |

---

## 3. Precondiciones

- Validación inicial de WORKFLOW-021 pasó.
- Pendientes clasificados.

---

## 4. Reglas del Workflow

- **R1:** Cada sección debe estar completa o explícitamente marcada como N/A con razón.
- **R2:** §5 Routing Index incluye ejemplo concreto de cómo usarlo.
- **R3:** §6 Plan de Sprints tiene una sub-sección por sprint con tabla de deliverables.
- **R4:** Cada tabla de sprint incluye columna "Spec Source (3B.9.10)" llenada desde Routing Index — NO se inventa.
- **R5:** §11 Primera acción exacta del PJM tiene comando ejecutable, no descripción genérica.

---

## 5. Pasos

### Paso 1 — PM redacta §1 Perfil y Rol Operativo del PJM

Define qué hace el PJM en este bloque, qué NO hace, UUID, email.

Fuente: OPERATIVO del proyecto.

### Paso 2 — PM redacta §2 Contexto del Proyecto

Tech stack, repos, URLs, SPEC de referencia.

Fuente: SPEC + 3B.1 + 3B.8 + OPERATIVO.

### Paso 3 — PM redacta §3 Estado Actual / Lo que se Completó

Tabla de fases completadas con gates. Decisiones cerradas hasta ahora.

Fuente: estado del proyecto (operativo) + DECISION_BLOQUE.

### Paso 4 — PM redacta §4 Decisiones Cerradas

Tabla de D-XX-NN clave del bloque — NO reabrir.

Fuente: 3B.6 ADRs + SPEC §2.

### Paso 5 — PM redacta §5 Documento Clave: Routing Index

Explicación de qué es 3B.9.10, cómo usarlo, ejemplo concreto.

Estructura sugerida:
```
## 5. Documento Clave: Routing Index (3B.9.10)

**Ruta:** [ruta en repo]

Este documento es OBLIGATORIO para generar cualquier HANDOFF o ASSIGNMENT.

Cómo usarlo (ejemplo):

  Deliverable: 4.2.3 Seed Data
  Routing Index dice:
    Spec Source: 3B.3_DATABASE_DESIGN.md
    Sección: §catálogos — 10 tablas
    Decisiones: D-XX-14, D-XX-20
    Docs para el agente: 3B.3, 3B.3.2

Regla: si un doc referenciado no existe → task_on_hold + notificar TL.
```

### Paso 6 — PM redacta §6 Plan de Sprints

Una sub-sección por sprint con:
- Objetivo del sprint
- Agentes activos
- Tabla deliverables (ID, deliverable, rol, horas, **Spec Source (3B.9.10)**)
- Gate M[N] con criterios

Fuente: 3B.9.9 Capacity Plan + 3B.9.3 Task Breakdown + 3B.9.10 Routing Index.

### Paso 7 — PM redacta §7 Dependencias

Las 4 dimensiones explicadas + tabla síntesis cross-sprint.

Fuente: 3B.9.3 + 3B.9.4.

### Paso 8 — PM redacta §8 Critical Path

Diagrama + lista de deliverables bloqueantes.

Fuente: 3B.9.4.

### Paso 9 — PM redacta §9 Paralelismo

Tabla sprint × agentes simultáneos.

Fuente: 3B.9.7.

### Paso 10 — PM redacta §10 Riesgos

Top 10-15 riesgos con probabilidad, buffer, sprint afectado, mitigación.

Fuente: 3B.9.6.

### Paso 11 — PM redacta §11 Contingencias

Tabla situación → acción.

Fuente: PAQUETE_TRAZABILIDAD + análisis PM.

### Paso 12 — PM redacta §12 DoD Resumido

Checklist por deliverable.

Fuente: 3B.9.3 columna `criterio_aceptacion`.

### Paso 13 — PM redacta §13 Pendientes GATE

Tabla de pendientes clasificados como GATE con owner y momento de bloqueo.

Fuente: pendientes_clasificados de WORKFLOW-021.

### Paso 14 — PM redacta §14 Diferidos

Lista de deliverables ❌ o ⚪ diferidos a próximos bloques.

Fuente: 3B.9.3 + DECISION_BLOQUE.

### Paso 15 — PM redacta §15 Equipo

Tabla rol, UUID, horas, función, picos de carga.

Fuente: OPERATIVO + 3B.9.4 Effort Matrix.

### Paso 16 — PM redacta §16 Reglas de Escalación

Tabla situación → acción.

### Paso 17 — PM redacta §17 Primera Acción Exacta del PJM

Comando concreto que el PJM debe ejecutar (NO descripción genérica).

Ejemplo:
```
1. Leer HO Maestro completo
2. Abrir 3B.9.10 Routing Index
3. Comenzar generación de SETUP_S00 invocando WORKFLOW-026
```

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| HO Maestro con 13-17 secciones llenas | sección dentro del .md | mismo archivo .md |

---

## 7. Validación

- Las 13-17 secciones existen y están llenas.
- §5 tiene ejemplo concreto del Routing Index.
- §6 tiene columna "Spec Source" llenada desde 3B.9.10.
- §17 tiene comando ejecutable.
- Sin contenido inventado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Sección vacía sin marcar N/A | Olvido | Llenar o marcar explícito |
| §5 sin ejemplo | Atajo | Agregar ejemplo concreto |
| §6 con "Spec Source" inventado | Violación R4 | Copiar desde 3B.9.10 |
| §17 con descripción genérica | "Empezar a planear" | Reemplazar por comando ejecutable |

---

## 9. Skills invocadas

(Ninguna directa — es redacción)

---

**Documento:** `VTT.WORKFLOW-HO-001.022_redactar_secciones_ho_maestro.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
