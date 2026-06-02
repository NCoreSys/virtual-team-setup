# VTT.WORKFLOW-HO-001.009 — Producir 3B.3 Database Design

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.009` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.2.3 (rol DB) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | DB (productor primario), TL (co-productor) |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 2 |

---

## 1. Propósito

Producir 3B.3 Database Design — ERD, Schema Prisma (o equivalente), tablas, índices, seeds, estrategia de migraciones. Depende de SPEC + 3B.1.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `3b1_path` | path | WORKFLOW-007 | sí | Componentes del sistema |
| `spec_path` | path | FASE 1 | sí | Modelo de datos requerido |
| `actual_schema` | path | WORKFLOW-006 (C) | no | Schema actual del repo |

---

## 3. Precondiciones

- 3B.1 aprobado.
- DB está en cadena de roles.
- Si camino C, `actual_schema` está disponible.

---

## 4. Reglas del Workflow

- **R1:** ERD obligatorio (mermaid o herramienta externa).
- **R2:** Schema Prisma (o equivalente) incluido en el documento.
- **R3:** Cada tabla nueva justifica su existencia contra SPEC (qué requisito funcional la motiva).
- **R4:** Constraints explícitos: PK, FK, UNIQUE, CHECK.
- **R5:** Estrategia de índices documentada con justificación de cada uno (qué query lo necesita).
- **R6:** En camino C, declara qué tablas EXTIENDE y cuáles CREA nuevas.
- **R7:** Plan de seeds: catálogos + datos iniciales + datos de prueba.
- **R8:** Migration strategy con orden topológico (M-XX-NN) y rollback documentado.

---

## 5. Pasos

### Paso 1 — DB lee SPEC + 3B.1 + `actual_schema` (si C)

Identifica:
- Entidades requeridas
- Relaciones entre entidades
- Restricciones de integridad
- Estado del schema actual (qué hay, qué falta)

### Paso 2 — DB produce ERD

Diagrama (mermaid `erDiagram` o equivalente) con entidades + relaciones + cardinalidad.

### Paso 3 — DB documenta Schema Prisma (o equivalente)

Por cada entidad:
- Campos con tipos
- Constraints (PK, FK, UNIQUE, CHECK)
- Índices
- Defaults

### Paso 4 — DB documenta estrategia de índices

Por cada índice declarado:
- Qué query lo va a usar
- Tipo de índice (B-tree, GIN, partial, etc.)
- Trade-off (escritura vs lectura)

### Paso 5 — DB documenta plan de seeds

- Catálogos (status, roles, permisos, etc.)
- Datos iniciales por entorno (dev, staging, prod)
- Datos de prueba (opcional)

### Paso 6 — DB documenta estrategia de migraciones

- Orden topológico de migraciones (M-XX-01, M-XX-02, ...)
- Rollback de cada migración
- Migraciones reversibles vs irreversibles (marcadas explícitamente)

### Paso 7 — DB ejecuta REVMA sobre 3B.3

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`** con (`documento=3B.3_DATABASE_DESIGN.md`, `agente_generador=DB`, `contexto=[SPEC, 3B.1, actual_schema]`)

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `3B.3_DATABASE_DESIGN.md` | archivo .md con ERD + Schema | `_project-management/Fases/<BLOQUE>/` |

---

## 7. Validación

- ERD presente y completo.
- Schema declarativo (Prisma o equivalente).
- Constraints explícitos.
- Índices justificados.
- Seeds planificados.
- Migration strategy con rollback.
- REVMA aprobado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| ERD incompleto (falta cardinalidad) | Rush | Completar antes de REVMA |
| Schema sin FK explícitas | Asume implícitas | Declarar todas |
| Índices sin justificación | Genéricos | Justificar contra queries reales |
| Migración irreversible sin marcar | Riesgo de pérdida de datos | Marcar explícitamente + plan de contingencia |
| Camino C: tabla declarada como nueva pero ya existe | No se consultó `actual_schema` | Revisar y corregir |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.009_producir_3b3_database_design.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
