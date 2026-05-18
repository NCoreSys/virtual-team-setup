# TEMPLATE — PRE-HANDOFF Iniciación del Proyecto (pre-SDLC)

> **Cómo usar:**
> 1. Copiar a `01-PM/PRE_HANDOFF_INICIACION_<<PROYECTO>>.md`
> 2. Llenar las 7 categorías A-G con sub-tareas reales del proyecto
> 3. Calcular horas reales (típico: ~32h vs ~11h umbrella)
> 4. Mapear INIT-* → MEM-001..005
> 5. Borrar este bloque antes de emitir

---

# PRE-HANDOFF — Tareas de Iniciación del Proyecto <<NOMBRE_PROYECTO>>

| Campo | Valor |
|-------|-------|
| **Documento** | PRE_HANDOFF_INICIACION_<<PROYECTO>>.md |
| **Versión** | 1.0 |
| **Fecha** | <<YYYY-MM-DD>> |
| **Autor** | PM (<<Nombre>>) |
| **Propósito** | Inventario de tareas pre-SDLC necesarias para iniciar el proyecto: VTT, repo, VM, equipo, tooling, kickoff |
| **Alcance** | Tareas previas a Development (Fase 0 Discovery). Reemplaza/expande MEM-001..005 |
| **Complementa** | `PRE_HANDOFF_IMPLEMENTACION_<<PROYECTO>>.md` |
| **Estado** | ✅ Listo para revisión PM |

---

## 1. CONTEXTO

MEM-001..005 en VTT son tareas **genéricas** que no especifican qué se hace exactamente:

| Task actual | Título genérico | Horas | Rol |
|-------------|-----------------|------:|-----|
| MEM-001 | Infra Setup | <<N>>h | DO |
| MEM-002 | Repo Structure | <<N>>h | PJM |
| MEM-003 | Team Onboarding | <<N>>h | PJM |
| MEM-004 | Tooling Setup | <<N>>h | DO |
| MEM-005 | Project Kickoff | <<N>>h | PM |

Este documento las expande con tareas concretas accionables.

---

## 2. CATEGORÍAS DE INICIACIÓN

| Categoría | Propósito |
|-----------|-----------|
| A. VTT Setup | Proyecto + fases + deliveries + tareas + dependencias en VTT |
| B. Repository Setup | Repo Git, estructura V3.1, convenciones, protección |
| C. VM Configuration | BD, volumen, SERVICE_KEY, Redis, firewall, network |
| D. Agent Team Setup | OPERATIVO por rol, PROJECT_MEMORY, contexto de sesión, acceso |
| E. Tooling Setup | Node, TypeScript, linters, formatters, hooks, CI básico |
| F. Documentation | README, CONTRIBUTING, ARCHITECTURE, reglas |
| G. Kickoff | Doc formal, sprint 1 plan, primer sync |

---

## 3. INVENTARIO DE TAREAS DE INICIACIÓN

**Total propuesto: <<N>> tareas · ~<<N>>h** (vs ~11h actuales en MEM-001..005).

### 3.1 Resumen por categoría

| Categoría | Tareas | Horas | Mapeo a MEM-001..005 |
|-----------|-------:|------:|---------------------|
| A. VTT Setup | <<N>> | <<N>>h | MEM-003 (parcial) |
| B. Repository Setup | <<N>> | <<N>>h | MEM-002 |
| C. VM Configuration | <<N>> | <<N>>h | MEM-001 |
| D. Agent Team Setup | <<N>> | <<N>>h | MEM-003 |
| E. Tooling Setup | <<N>> | <<N>>h | MEM-004 |
| F. Documentation | <<N>> | <<N>>h | MEM-005 (parcial) |
| G. Kickoff | <<N>> | <<N>>h | MEM-005 |
| **TOTAL** | **<<N>>** | **<<N>>h** | — |

### 3.2 Resumen por rol

| Rol | Tareas | Horas |
|-----|-------:|------:|
| DO | <<N>> | <<N>>h |
| PJM | <<N>> | <<N>>h |
| PM | <<N>> | <<N>>h |
| TL | <<N>> | <<N>>h |
| Admin VM (externo) | <<N>> | <<N>>h (coordinados por DO) |

---

## 4. TAREAS DETALLADAS POR CATEGORÍA

### A. VTT Setup (<<N>> tareas · <<N>>h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-A-01 | Verificar proyecto en VTT | PJM | 0.5h | Confirmación existencia | ✅ / 🟡 / 🔴 |
| INIT-A-02 | Verificar N fases en VTT | PJM | 0.5h | Confirmación Phase UUIDs | ✅ / 🟡 |
| INIT-A-03 | Verificar N deliveries en VTT | PJM | 0.5h | Confirmación Delivery UUIDs | ✅ / 🟡 |
| INIT-A-04 | Ejecutar PATCH de tareas en VTT con metadata | PJM + DO | <<N>>h | assigneeId, complexity, category, hours | 🟡 Pendiente |
| INIT-A-05 | Crear N dependencias en VTT | PJM | <<N>>h | N dependencias registradas | 🟡 Pendiente |

### B. Repository Setup (<<N>> tareas · <<N>>h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-B-01 | Crear/verificar repo Git | DO | <<N>>h | Repo con URL documentada | 🟡 / 🔴 |
| INIT-B-02 | Inicializar estructura V3.1 | PJM | <<N>>h | Carpetas phases/, _pm/, docs/, archive/, .claude/agents/ | 🟡 |
| INIT-B-03 | Configurar archivos base del repo | PJM | <<N>>h | .gitignore, .editorconfig, README, CONTRIBUTING | 🟡 |
| INIT-B-04 | Branch protection + CODEOWNERS + PR templates | DO | <<N>>h | Protección de main + CODEOWNERS + templates | 🟡 |
| INIT-B-05 | Configurar git user + conventions | PJM | <<N>>h | Convenciones commit + git config | 🟡 |

### C. VM Configuration (<<N>> tareas · <<N>>h)

Coordinación con **Admin VM externo**. DO gestiona los requests.

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-C-01 | Verificar infraestructura provisionada | DO | <<N>>h | Checklist: BD, volumen, SERVICE_KEY, Redis, firewall | ✅ / 🟡 |
| INIT-C-02 | Tests de conectividad desde local | DO | <<N>>h | Tests Test-NetConnection, Prisma, storage | 🟡 |
| INIT-C-03 | Distribuir SERVICE_KEY a agentes consumidores | DO | <<N>>h | SERVICE_KEY vía secret management | 🟡 |
| INIT-C-04 | Documentar config VM en repo | DO | <<N>>h | docs/INFRASTRUCTURE.md | 🟡 |

### D. Agent Team Setup (<<N>> tareas · <<N>>h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-D-01 | Crear OPERATIVO por rol activo | PM + PJM | <<N>>h | .claude/agents/OPERATIVO_<ROL>.md × 12 | 🟡 Parcial (<<X>>/12) |
| INIT-D-02 | PROJECT_MEMORY.md consolidado | PM | <<N>>h | Memoria persistente | ✅ / 🟡 |
| INIT-D-03 | CONTEXTO de sesión por rol | PJM | <<N>>h | knowledge/agent-tasks/CONTEXTO_<ROL>_SESION.md × N | 🟡 |
| INIT-D-04 | Distribuir accesos al equipo | PJM | <<N>>h | Acceso repo + VTT + docs por rol | 🟡 |
| INIT-D-05 | Reuniones de onboarding por rol | PM | <<N>>h | Sesiones kick-off por rol activo | 🟡 |

### E. Tooling Setup (<<N>> tareas · <<N>>h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-E-01 | Base Node + TypeScript del backend | DO + TL | <<N>>h | package.json scripts, tsconfig, .nvmrc | 🟡 |
| INIT-E-02 | Linters + formatters + pre-commit | DO | <<N>>h | .eslintrc, .prettierrc, Husky, lint-staged | 🟡 |
| INIT-E-03 | CI mínimo (smoke) | DO | <<N>>h | GitHub Actions build + lint + test | 🟡 |

### F. Documentation (<<N>> tareas · <<N>>h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-F-01 | README + CONTRIBUTING del repo | PM + TL | <<N>>h | README.md + CONTRIBUTING.md | 🟡 |
| INIT-F-02 | ARCHITECTURE.md operativo | TL | <<N>>h | docs/ARCHITECTURE.md con link a SPEC | 🟡 |

### G. Kickoff (<<N>> tareas · <<N>>h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-G-01 | Documento formal de Kickoff | PM | <<N>>h | KICKOFF_<<PROYECTO>>.md | 🟡 |
| INIT-G-02 | Primer sync del equipo | PM + todos | <<N>>h | Acta de kickoff con action items | 🟡 |

---

## 5. MAPEO A TAREAS MEM ACTUALES EN VTT

### Opción A — Mantener MEM-001..005 como "umbrella" (recomendada)

| MEM actual | INIT-* que absorbe |
|-----------|---------------------|
| MEM-001 Infra Setup | INIT-C-01 a INIT-C-04 |
| MEM-002 Repo Structure | INIT-B-01 a INIT-B-05 |
| MEM-003 Team Onboarding | INIT-A-01..05 + INIT-D-01..05 |
| MEM-004 Tooling Setup | INIT-E-01 a INIT-E-03 |
| MEM-005 Project Kickoff | INIT-F-01..02 + INIT-G-01..02 |

**Nuevo total Phase 1:** <<N>>h. Las horas de MEM-001..005 actuales deben **incrementarse** vía PATCH.

---

## 6. DEPENDENCIAS CRÍTICAS DE INICIACIÓN

| # | Bloqueo | Desbloquea | Acción requerida |
|---|---------|------------|------------------|
| 1 | <<bloqueo>> | <<qué desbloquea>> | <<acción>> |

---

## 7. ORDEN DE EJECUCIÓN SUGERIDO

```
SEMANA 0 (Pre-kickoff):
  C. VM Configuration (verificación + docs)
  B. Repository Setup (si está desbloqueado)
  A.04 + A.05 — PATCH tareas en VTT + dependencias

SEMANA 1 (Onboarding):
  D. Agent Team Setup
  E. Tooling Setup
  F. Documentation

SEMANA 1 (Kickoff):
  G. Kickoff
  → Arranque formal de Phase 0 Discovery
```

---

## 8. CHECKLIST DE CIERRE DE INICIACIÓN

```
VTT:
[ ] Tareas con assigneeId, complexity, category, estimatedHours correctos
[ ] Reassignments aplicados
[ ] Dependencias críticas registradas
[ ] Deliveries visibles y vinculadas

REPO:
[ ] Repo Git accesible
[ ] Estructura V3.1 inicializada
[ ] Branch protection en main
[ ] CODEOWNERS + PR template

VM:
[ ] Conectividad local → VM verificada
[ ] SERVICE_KEY distribuida
[ ] docs/INFRASTRUCTURE.md escrito

EQUIPO:
[ ] OPERATIVO_<ROL>.md creado para roles activos
[ ] CONTEXTO_<ROL>_SESION.md para roles principales
[ ] Acceso a repo + VTT + docs verificado

TOOLING:
[ ] package.json con scripts funcionando
[ ] ESLint + Prettier + pre-commit hooks operativos
[ ] CI mínimo corriendo en PRs

DOCS:
[ ] README + CONTRIBUTING + ARCHITECTURE en el repo
[ ] KICKOFF doc firmado por PM

KICKOFF:
[ ] Kickoff call ejecutado, acta firmada
[ ] PJM confirma sprint 1 plan
```

---

## 9. RIESGOS DE INICIACIÓN

| # | Riesgo | Mitigación |
|---|--------|------------|
| IR-1 | Repo Git no definido | PM decide antes de cualquier código |
| IR-2 | Endpoint VTT de dependencias no disponible | Registrar manualmente |
| IR-3 | Admin VM no disponible | DO anticipa pedidos + PM escala >24h |
| IR-4 | OPERATIVOs incompletos | PM prioriza roles críticos primero |
| IR-5 | Kickoff no reúne equipo completo | Grabación + material asíncrono |

---

## 10. SIGUIENTE PASO

Con este pre-handoff aprobado:

1. PM **aprueba**
2. PM **actualiza MEM-001..005 en VTT** con horas reales (<<N>>h → <<N>>h)
3. PM **genera HO formal al PJM consolidado**
4. **PJM descompone los HOs en BRIEFs** por rol/sprint
5. **Equipo ejecuta iniciación** (semana 0) antes del kickoff

---

**Documento:** PRE_HANDOFF_INICIACION_<<PROYECTO>>.md
**Versión:** 1.0
**Estado:** ✅ Listo para revisión PM
**Fecha:** <<YYYY-MM-DD>>

---

**PM — <<Nombre>>**

---

**Template source:** `TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md`
**Proceso asociado:** `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` (paso 4)
