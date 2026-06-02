# VTT.WORKFLOW-HO-001.008 — Producir 3B.2 Code Architecture

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.008` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.2.3 (rol TL) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL (productor primario), BE/FE (co-productores si aplica) |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 2 |

---

## 1. Propósito

Producir 3B.2 Code Architecture — estructura de carpetas, coding standards, design patterns, naming conventions, error handling strategy. Depende de 3B.1 (necesita los componentes para organizar el código).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `3b1_path` | path | WORKFLOW-007 aprobado | sí | Solution Architecture |
| `spec_path` | path | FASE 1 | sí | SPEC |
| `docs_actuales` | array<path> | WORKFLOW-006 (camino C) | no | Estructura actual del repo |

---

## 3. Precondiciones

- 3B.1 aprobado.
- TL está en cadena de roles.

---

## 4. Reglas del Workflow

- **R1:** Estructura de carpetas respeta convenciones de la plataforma (services/, routes/, validators/, etc.).
- **R2:** Naming conventions documentadas: snake_case BD, camelCase JS, PascalCase clases, etc.
- **R3:** Error handling strategy: una jerarquía de errores única + AppError base.
- **R4:** En camino C, 3B.2 declara qué carpetas/archivos se modifican y cuáles se crean nuevos.

---

## 5. Pasos

### Paso 1 — TL lee 3B.1 + estructura actual (si C)

Identifica:
- Componentes que necesitan estructura de carpetas
- Patrones existentes a mantener (si C)
- Patrones nuevos a introducir

### Paso 2 — TL documenta estructura de carpetas

Por cada componente principal, declara estructura:
```
src/
├── services/
│   └── <componente>.service.ts
├── routes/
│   └── <componente>.routes.ts
└── validators/
    └── <componente>.validator.ts
```

### Paso 3 — TL documenta coding standards

- Lint rules
- Formatter config
- Naming conventions
- Comentarios y docstrings
- TypeScript strict / Python type hints

### Paso 4 — TL documenta design patterns

- Patrones aplicados (Repository, Service Layer, etc.)
- Dependency injection (si aplica)
- Manejo de transacciones

### Paso 5 — TL documenta error handling strategy

- Jerarquía AppError base + sub-errores por dominio
- Códigos de error MEM-ERR-xxx (o equivalente del proyecto)
- Logging asociado

### Paso 6 — TL ejecuta REVMA sobre 3B.2

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`** con (`documento=3B.2_CODE_ARCHITECTURE.md`, `agente_generador=TL`, `contexto=[3B.1, SPEC]`)

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `3B.2_CODE_ARCHITECTURE.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |

---

## 7. Validación

- Estructura de carpetas consistente con 3B.1.
- Standards declarados son ejecutables (lint config existe o se define).
- REVMA aprobado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Estructura propuesta no encaja con repo actual (camino C) | No se consultó `actual_structure` | Revisar y ajustar |
| Patrones inconsistentes entre módulos | TL improvisó | Unificar patrones |
| Error handling sin jerarquía clara | Estrategia parcial | Completar jerarquía AppError |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.008_producir_3b2_code_architecture.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
