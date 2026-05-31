# ESTRUCTURA DE FASES DE DESARROLLO — ESTÁNDAR VTT V3.1

**Versión:** 3.1.0  
**Fecha:** 2026-03-16  
**Cambios vs V3:** Code-logic con espejo src/, _pm/operativos/, flujo análisis, archive con ruta  
**Propósito:** Estructura estándar replicable en VTT, optimizada para uso práctico.

---

## 1. PRINCIPIOS

| Principio | Regla |
|-----------|-------|
| **Máximo 4 niveles** | `phases/04-development/devlogs/archivo.md` |
| **Sprint en nombre** | `DEVLOG_BE_S01_VTT-001_descripcion.md` (no carpeta) |
| **Solo carpetas necesarias** | Crear cuando haya archivos, no estructura vacía |
| **Versionado en carpeta** | `arquitectura/v1/`, `arquitectura/v2/` |
| **Disciplina en nombre** | `BE`, `FE`, `DB`, `UX`, `QA`, `DO` |

---

## 2. ESTRUCTURA BASE (4 NIVELES MÁXIMO)

```
proyecto/
│
├── phases/                              # Nivel 1
│   ├── 00-discovery/                    # Nivel 2
│   │   ├── deliverables/                # Nivel 3
│   │   │   └── archivo.md               # Nivel 4
│   │   ├── _pm/
│   │   └── knowledge/
│   │
│   ├── 01-planning/
│   ├── 02-analysis/
│   │   ├── deliverables/
│   │   ├── _pm/
│   │   │   └── analisis/                # Flujo PM→SA→AR→TL por sprint
│   │   │       └── S01/
│   │   │           ├── 01-PM/
│   │   │           ├── 02-SA/
│   │   │           ├── 03-AR/
│   │   │           └── 04-TL/
│   │   └── knowledge/
│   │
│   ├── 03-design/
│   ├── 04-development/
│   │   ├── deliverables/
│   │   ├── _pm/
│   │   └── knowledge/
│   │       ├── code-logic/              # Excepción: espejo de src/
│   │       │   ├── backend/
│   │       │   │   ├── controllers/
│   │       │   │   ├── services/
│   │       │   │   └── middleware/
│   │       │   └── frontend/
│   │       │       ├── components/
│   │       │       └── hooks/
│   │       └── [devlogs, errors, etc.]  # Archivos planos
│   │
│   ├── 05-testing/
│   ├── 06-deploy/
│   └── 07-operations/
│
├── _pm/                                 # Governance global
│   ├── roles/
│   ├── templates/
│   └── operativos/                      # OPERATIVO_*, PROCESO_*, MEMO_*, COORDINACION_*
│
├── docs/                                # Referencia técnica
│
├── archive/                             # Histórico (preserva ruta original)
│   └── phases/
│       ├── 03-design/
│       └── 04-development/
│
├── backend/                             # Código
└── frontend/
```

---

## 3. ESTRUCTURA POR FASE (SOLO 3 SUBCARPETAS)

Cada fase tiene máximo 3 subcarpetas:

```
phases/XX-nombre/
├── deliverables/          # Entregables formales aprobados
├── _pm/                   # Gestión: handoffs, briefs, assignments
└── knowledge/             # Ejecución: devlogs, errors, qa-reports
```

**NO crear subcarpetas adicionales** (como `devlogs/backend/sprint-01/`). Todo va en el nombre del archivo.

---

## 4. NAMING CONVENTION

### Formato general

```
<TIPO>_<DISC>_<SPRINT>_<ID>_<descripcion>.md
```

### Componentes

| Campo | Valores | Ejemplo |
|-------|---------|---------|
| TIPO | `HANDOFF`, `BRIEF`, `ASSIGNMENT`, `DEVLOG`, `ERROR`, `BUG`, `QA`, `AUDIT` | `DEVLOG` |
| DISC | `BE`, `FE`, `DB`, `UX`, `UI`, `QA`, `DO`, `SA`, `AR` | `BE` |
| SPRINT | `S01`, `S02`, `S03`... | `S01` |
| ID | Task ID o código único | `VTT-001` |
| descripcion | kebab-case | `auth-middleware` |

### Ejemplos

```
# Gestión (_pm/)
HANDOFF_BE_S01_api-users.md
BRIEF_FE_S01_VTT-156_dashboard-component.md
ASSIGNMENT_DB_S01_VTT-142_migrations.md

# Ejecución (knowledge/)
DEVLOG_BE_S01_VTT-001_auth-middleware.md
DEVLOG_FE_S02_VTT-089_login-form.md
ERROR_BE_S01_ERR-001_prisma-timeout.md
BUG_FE_S01_BUG-003_modal-overflow.md
QA_BE_S01_code-review.md
AUDIT_S01_security-scan.md

# Deliverables (deliverables/)
# Sin prefijo de tipo, organizados por subfase si es necesario
arquitectura-sistema.md
api-design.md
erd-v1.md
```

### Para devlogs con fecha

```
DEVLOG_BE_S01_2026-03-16_VTT-001_auth-middleware.md
```

---

## 5. VERSIONADO DE DELIVERABLES

Cuando un deliverable tiene versiones, crear subcarpeta:

```
phases/03-design/deliverables/
├── arquitectura/
│   ├── v1/
│   │   └── ARQUITECTURA_SISTEMA_v1.md
│   └── v2/
│       └── ARQUITECTURA_SISTEMA_v2.md
├── erd/
│   ├── v1/
│   │   └── ERD_v1.md
│   └── v2/
│       └── ERD_v2.md
└── api-design.md                        # Sin versiones aún
```

**Regla:** Solo crear subcarpeta de versión cuando exista más de una versión.

---

## 6. ESTRUCTURA MÍNIMA (ESQUELETO)

Crear solo esto al inicio:

```
proyecto/
├── phases/
│   ├── 00-discovery/
│   ├── 01-planning/
│   ├── 02-analysis/
│   ├── 03-design/
│   │   ├── deliverables/
│   │   ├── _pm/
│   │   └── knowledge/
│   ├── 04-development/
│   │   ├── deliverables/
│   │   ├── _pm/
│   │   └── knowledge/
│   ├── 05-testing/
│   ├── 06-deploy/
│   └── 07-operations/
├── _pm/
│   ├── roles/
│   └── templates/
├── docs/
└── archive/
```

Las subcarpetas `deliverables/`, `_pm/`, `knowledge/` se crean **solo cuando la fase tiene archivos**.

---

## 7. REGLA DE UBICACIÓN POR TIPO

### Gestión (`phases/XX/_pm/`)

| Tipo | Naming | Ejemplo |
|------|--------|---------|
| Handoff | `HANDOFF_<DISC>_<SPRINT>_<desc>.md` | `HANDOFF_BE_S01_api-users.md` |
| Brief | `BRIEF_<DISC>_<SPRINT>_<ID>_<desc>.md` | `BRIEF_BE_S01_VTT-001_auth.md` |
| Assignment | `ASSIGNMENT_<DISC>_<SPRINT>_<ID>.md` | `ASSIGNMENT_BE_S01_VTT-001.md` |

### Ejecución (`phases/XX/knowledge/`)

| Tipo | Naming | Ejemplo |
|------|--------|---------|
| Devlog | `DEVLOG_<DISC>_<SPRINT>_<ID>_<desc>.md` | `DEVLOG_BE_S01_VTT-001_auth.md` |
| Error | `ERROR_<DISC>_<SPRINT>_<ID>_<desc>.md` | `ERROR_BE_S01_ERR-001_timeout.md` |
| Bug | `BUG_<DISC>_<SPRINT>_<ID>_<desc>.md` | `BUG_FE_S01_BUG-003_modal.md` |
| Issue | `ISSUE_<SPRINT>_<ID>_<desc>.md` | `ISSUE_S01_ISS-005_deploy.md` |
| QA Report | `QA_<DISC>_<SPRINT>_<desc>.md` | `QA_BE_S01_code-review.md` |
| Audit | `AUDIT_<SPRINT>_<desc>.md` | `AUDIT_S01_security.md` |
| Lesson Learned | `LL_<SPRINT>_<ID>_<desc>.md` | `LL_S01_LL-001_migrations.md` |

### Deliverables (`phases/XX/deliverables/`)

Sin prefijo de tipo. Nombrar por contenido:

```
arquitectura-sistema.md
api-endpoints.md
erd.md
wireframes-dashboard.html
mockup-login.html
test-plan.md
deployment-guide.md
```

Si hay versiones:
```
arquitectura/v1/arquitectura-sistema.md
arquitectura/v2/arquitectura-sistema.md
```

---

## 8. CASOS CROSS-FASE

Si un error/issue cruza fases (ej: error en development que afecta testing):

1. **Va en la fase donde se detectó**
2. **Referenciar en la otra fase** con link relativo

Ejemplo:
```markdown
# En phases/05-testing/knowledge/BUG_FE_S02_BUG-015_modal.md

## Relacionado
- Ver error original: [ERROR_FE_S01_ERR-008](../../04-development/knowledge/ERROR_FE_S01_ERR-008_modal-state.md)
```

---

## 9. MAPEO DE ARCHIVOS EXISTENTES

### Por patrón de nombre actual

| Si el archivo... | Va a... | Nuevo nombre |
|------------------|---------|--------------|
| `HANDOFF_*.md` | `phases/XX/_pm/` | `HANDOFF_<DISC>_<SPRINT>_<desc>.md` |
| `BRIEF_*.md` | `phases/XX/_pm/` | `BRIEF_<DISC>_<SPRINT>_<ID>_<desc>.md` |
| `ASSIGNMENT_*.md` | `phases/XX/_pm/` | `ASSIGNMENT_<DISC>_<SPRINT>_<ID>.md` |
| `YYYY-MM-DD_*.md` (devlog) | `phases/XX/knowledge/` | `DEVLOG_<DISC>_<SPRINT>_<fecha>_<ID>_<desc>.md` |
| `*.LOGIC.md` | `phases/04-development/knowledge/` | `LOGIC_<DISC>_<modulo>_<archivo>.md` |
| `ERR-*.md` | `phases/XX/knowledge/` | `ERROR_<DISC>_<SPRINT>_<ID>_<desc>.md` |
| `BUG-*.md` | `phases/XX/knowledge/` | `BUG_<DISC>_<SPRINT>_<ID>_<desc>.md` |
| `AGENT_PROFILE_*.md` | `_pm/roles/` | Sin cambio |
| `TEMPLATE_*.md` | `_pm/templates/` | Sin cambio |
| `ARQUITECTURA*.md` | `phases/03-design/deliverables/` | `arquitectura-sistema.md` o con versión |
| `ERD*.md` | `phases/03-design/deliverables/` | `erd.md` o con versión |
| `API_ENDPOINTS*.md` | `docs/` | Sin cambio (referencia técnica viva) |

### Por contenido (si nombre no es claro)

| Si el contenido... | Fase | Carpeta |
|--------------------|------|---------|
| Define arquitectura del sistema | 03-design | deliverables/ |
| Define cómo se ve la UI | 03-design | deliverables/ |
| Es instrucción para un agente | XX | _pm/ |
| Es registro de trabajo diario | XX | knowledge/ |
| Es reporte de pruebas | 05-testing | knowledge/ |
| Es configuración de deploy | 06-deploy | deliverables/ |

---

## 10. CREAR CARPETA SOLO CUANDO SEA NECESARIO

### Ejemplo: Proyecto nuevo

Inicio:
```
proyecto/
├── phases/
│   └── (vacío)
├── _pm/
│   ├── roles/
│   └── templates/
└── docs/
```

Cuando llega el primer archivo de arquitectura:
```
proyecto/
├── phases/
│   └── 03-design/
│       └── deliverables/
│           └── arquitectura-sistema.md
```

Cuando llega el primer handoff de desarrollo:
```
proyecto/
├── phases/
│   ├── 03-design/
│   │   └── deliverables/
│   └── 04-development/
│       └── _pm/
│           └── HANDOFF_BE_S01_api-users.md
```

---

## 11. REGLA DE ORO (SIMPLIFICADA)

| Pregunta | Respuesta |
|----------|-----------|
| ¿Es entregable formal aprobado? | → `phases/XX/deliverables/` |
| ¿Es para asignar trabajo? | → `phases/XX/_pm/` |
| ¿Se generó al trabajar? | → `phases/XX/knowledge/` |
| ¿Es perfil de agente o template? | → `_pm/` (raíz) |
| ¿Es referencia técnica viva? | → `docs/` |
| ¿Ya no es activo? | → `archive/` |

---

## 12. COMPARATIVA V2 vs V3

| Aspecto | V2 | V3 |
|---------|----|----|
| Niveles máximos | 6 | **4** |
| Sprint como carpeta | Sí | **No (en nombre)** |
| Disciplina como carpeta | Sí | **No (en nombre)** |
| Carpetas vacías | Crear todas | **Solo las necesarias** |
| Ejemplo ruta larga | `phases/04-development/knowledge/devlogs/backend/sprint-01/archivo.md` | `phases/04-development/knowledge/DEVLOG_BE_S01_archivo.md` |

---

## 13. COMANDOS PARA CREAR ESTRUCTURA MÍNIMA

```bash
# Crear esqueleto base
mkdir -p phases/{00-discovery,01-planning,02-analysis,03-design,04-development,05-testing,06-deploy,07-operations}
mkdir -p _pm/{roles,templates}
mkdir -p docs
mkdir -p archive

# Crear subcarpetas solo en fases que ya tienen archivos
# Ejemplo: si ya tienes archivos de diseño y desarrollo
mkdir -p phases/03-design/{deliverables,_pm,knowledge}
mkdir -p phases/04-development/{deliverables,_pm,knowledge}
```

---

## 14. RESUMEN

| Elemento | Valor |
|----------|-------|
| Fases | 8 (0-7) |
| Niveles máximos | 4 (excepción: code-logic puede tener 5) |
| Subcarpetas por fase | 3 (`deliverables/`, `_pm/`, `knowledge/`) |
| Sprint | En nombre del archivo (`S01`, `S02`) |
| Disciplina | En nombre del archivo (`BE`, `FE`, `UX`) |
| Carpetas vacías | No crear |
| Versionado | Subcarpeta solo si hay >1 versión |

---

## 15. CODE-LOGIC (EXCEPCIÓN AL LÍMITE DE 4 NIVELES)

El code-logic mantiene estructura espejo de `src/` para facilitar navegación:

```
phases/04-development/knowledge/code-logic/
├── backend/
│   ├── controllers/
│   │   └── auth.controller.LOGIC.md
│   ├── services/
│   │   └── auth.service.LOGIC.md
│   ├── middleware/
│   │   └── authenticate.LOGIC.md
│   └── routes/
│       └── auth.routes.LOGIC.md
└── frontend/
    ├── components/
    │   └── LoginForm.LOGIC.md
    ├── hooks/
    │   └── useAuth.LOGIC.md
    └── pages/
        └── Dashboard.LOGIC.md
```

**Naming:** `<nombre-archivo>.LOGIC.md` (mantiene nombre original del código)

**Máximo 5 niveles** para code-logic: `phases/04-development/knowledge/code-logic/backend/services/auth.LOGIC.md`

---

## 16. OPERATIVOS (`_pm/operativos/`)

Documentos de operación del equipo que no son específicos de una fase:

```
_pm/operativos/
├── OPERATIVO_AGENTES.md
├── OPERATIVO_QA.md
├── PROCESO_DESARROLLO_v3.md
├── PROCESO_CODE_REVIEW.md
├── MEMO_DECISION_EQUIPO_2026-03-15.md
├── COORDINACION_EQUIPO.md
└── MANUAL_ONBOARDING.md
```

**Tipos de archivos:**
- `OPERATIVO_*.md` — Procedimientos operativos
- `PROCESO_*.md` — Definiciones de proceso
- `MEMO_*.md` — Decisiones de equipo
- `COORDINACION_*.md` — Documentos de coordinación
- `MANUAL_*.md` — Manuales y guías

---

## 17. FLUJO DE ANÁLISIS (`phases/XX/_pm/analisis/`)

El flujo de análisis previo al handoff (PM→SA→AR→TL→PJM) va organizado por sprint:

```
phases/02-analysis/_pm/analisis/
├── S01/
│   ├── 01-PM/
│   │   └── ANALISIS_PM_S01_requerimientos.md
│   ├── 02-SA/
│   │   └── ANALISIS_SA_S01_casos-uso.md
│   ├── 03-AR/
│   │   └── ANALISIS_AR_S01_arquitectura.md
│   ├── 04-TL/
│   │   └── ANALISIS_TL_S01_tareas.md
│   └── 05-PJM/
│       └── ANALISIS_PJM_S01_plan.md
├── S02/
│   └── ...
└── S03/
    └── ...
```

**Flujo:** PM analiza → SA refina → AR diseña → TL planea → PJM aprueba → HANDOFF

---

## 18. ARCHIVE (PRESERVAR RUTA ORIGINAL)

Cuando un archivo se archiva, se mueve preservando su ruta original:

```
archive/
├── phases/
│   ├── 03-design/
│   │   └── deliverables/
│   │       └── arquitectura-v1/         # Versión anterior archivada
│   │           └── arquitectura-sistema.md
│   └── 04-development/
│       └── _pm/
│           └── HANDOFF_BE_S01_api-v1.md # Handoff reemplazado
├── legacy/                               # Archivos de estructura anterior
│   └── _project-management/
│       └── PM-coordination-V2/
└── deprecated/                           # Archivos obsoletos
    └── TEMPLATE_BRIEF_v1.md
```

**Reglas de archive:**
1. Preservar ruta original dentro de `archive/phases/`
2. `archive/legacy/` para archivos de estructuras anteriores
3. `archive/deprecated/` para templates/docs obsoletos
4. Agregar sufijo de fecha si es necesario: `archivo_ARCHIVED-2026-03-16.md`

---

**Documento:** ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md  
**Versión:** 3.1.0  
**Estado:** ✅ Aprobado para implementación
