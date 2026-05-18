# PRE-HANDOFF — Tareas de Iniciación del Proyecto Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **Autor** | PM (Martin Rivas) |
| **Propósito** | Inventario de tareas **pre-implementación** necesarias para iniciar operativamente el proyecto Memory Service: VTT, repo, VM, equipo, tooling, kickoff. |
| **Alcance** | Tareas previas a Development. Reemplaza/expande MEM-001..005 (genéricas 11h) con detalle accionable. |
| **Complementa** | `PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md` (tareas de código, 66 tareas 212h) |
| **Estado** | ✅ Listo para revisión PM |

---

## 1. CONTEXTO

MEM-001..005 en VTT son tareas **genéricas** (11h totales) que no especifican qué se hace exactamente:

| Task actual | Título genérico | Horas | Rol |
|-------------|-----------------|------:|-----|
| MEM-001 | Infra Setup | 2h | DO |
| MEM-002 | Repo Structure | 2h | PJM |
| MEM-003 | Team Onboarding | 1h | PJM |
| MEM-004 | Tooling Setup | 2h | DO |
| MEM-005 | Project Kickoff | 4h | PM |

Este documento las **expande con tareas concretas accionables** y agrega tareas faltantes detectadas.

---

## 2. CATEGORÍAS DE INICIACIÓN

| Categoría | Propósito |
|-----------|-----------|
| A. VTT Setup | Proyecto + fases + deliveries + tareas + dependencias en VTT |
| B. Repository Setup | Repo Git, estructura V3.1, convenciones, protección |
| C. VM Configuration | BD, volumen, SERVICE_KEY, Redis, firewall, network (vía Admin VM) |
| D. Agent Team Setup | OPERATIVO por rol, PROJECT_MEMORY, contexto de sesión, acceso |
| E. Tooling Setup | Node, TypeScript, linters, formatters, hooks, CI básico |
| F. Documentation | README, CONTRIBUTING, ARCHITECTURE, reglas |
| G. Kickoff | Doc formal, sprint 1 plan, primer sync |

---

## 3. INVENTARIO DE TAREAS DE INICIACIÓN

**Total propuesto: 24 tareas · ~32h** (vs 11h actuales en MEM-001..005).

### 3.1 Resumen por categoría

| Categoría | Tareas | Horas | Mapeo a MEM-001..005 |
|-----------|-------:|------:|---------------------|
| A. VTT Setup | 5 | 6h | MEM-003 (parcial) |
| B. Repository Setup | 5 | 5h | MEM-002 |
| C. VM Configuration | 4 | 4h | MEM-001 |
| D. Agent Team Setup | 5 | 8h | MEM-003 |
| E. Tooling Setup | 3 | 4h | MEM-004 |
| F. Documentation | 2 | 2h | MEM-005 (parcial) |
| G. Kickoff | 2 | 3h | MEM-005 |
| **TOTAL** | **24** | **32h** | — |

### 3.2 Resumen por rol

| Rol | Tareas | Horas |
|-----|-------:|------:|
| DO | 7 | 9h |
| PJM | 7 | 9h |
| PM | 5 | 8h |
| TL | 3 | 4h |
| Admin VM (externo) | 2 | 2h (coordinados por DO) |
| **TOTAL** | **24** | **32h** |

---

## 4. TAREAS DETALLADAS POR CATEGORÍA

### A. VTT Setup (5 tareas · 6h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-A-01 | Verificar proyecto en VTT | PJM | 0.5h | Confirmación: Project `51e169f7-...` existe con key MEM | ✅ Hecho |
| INIT-A-02 | Verificar 10 fases en VTT | PJM | 0.5h | Confirmación: Phase UUIDs registrados en PROJECT_MEMORY §6 | ✅ Hecho |
| INIT-A-03 | Verificar 65 deliveries en VTT | PJM | 0.5h | Confirmación: Delivery UUIDs registrados en HO v2.1 §6 | ✅ Hecho |
| INIT-A-04 | **Ejecutar PATCH de 116 tareas en VTT** | PJM + DO | 2h | Script Python corre `PATCH /api/tasks/{id}` con `assigneeId`, `priorityId`, `complexity`, `category`, `estimatedHours` para las 116 tareas (incluye reassignments PM aprobados: MEM-022→SA, MEM-039→AR) | 🟡 Pendiente |
| INIT-A-05 | Crear dependencias en VTT (manual) | PJM | 2.5h | 15 dependencias críticas registradas (cadena S01→S06, MEM-038→MEM-081, testing→deploy). Endpoint VTT aún no confirmado — por eso manual | 🟡 Pendiente (bloqueado hasta endpoint) |

**Dependencia externa:** resolver gotcha VTT API — "POST/PATCH task acepta `deliveryId` pero NO lo persiste" (HO v2.1 §5). Documentar como issue sin bloquear.

---

### B. Repository Setup (5 tareas · 5h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-B-01 | Crear/verificar repo Git de Memory Service | DO | 1h | Repo en GitHub/GitLab con URL documentada. **Atención:** remoto actual apunta a `twitter-react.git` (incorrecto) | 🔴 Bloqueado (requiere PM definir multi-repo) |
| INIT-B-02 | Inicializar estructura V3.1 | PJM | 1h | Carpetas: `phases/00-discovery/` a `phases/07-operations/` · `_pm/{roles,templates,operativos}/` · `docs/` · `archive/` · `.claude/agents/` según V3.1 §2 y §6 | 🟡 Pendiente |
| INIT-B-03 | Configurar archivos base del repo | PJM | 1h | `.gitignore`, `.gitattributes`, `.editorconfig`, `README.md` inicial, `CONTRIBUTING.md`, licencia | 🟡 Pendiente |
| INIT-B-04 | Branch protection + CODEOWNERS | DO | 1h | Protección de `main`: requiere PR + 1 approval · `CODEOWNERS` con PM/TL como reviewers · templates PR (`.github/PULL_REQUEST_TEMPLATE.md`) | 🟡 Pendiente |
| INIT-B-05 | Configurar git user + conventions | PJM | 1h | Convenciones commit `[tipo] [TASK_ID]: descripción` + `Co-Authored-By` configuradas. Git config con `martin.rivas@prompt-ai.studio` (ver PROJECT_RULES §8) | 🟡 Pendiente |

**Bloqueo crítico:** INIT-B-01 depende de decisión PM sobre multi-repo (pendiente desde PROJECT_RULES v1.4).

---

### C. VM Configuration (4 tareas · 4h)

Coordinación con **Admin VM externo** (no es parte del equipo de 12 roles). El DO de Memory Service gestiona los requests.

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-C-01 | Verificar infraestructura provisionada | DO | 1h | Checklist confirmado: BD `memory_service_db` accesible · volumen `/root/memory-service-storage/` escribible · SERVICE_KEY en `.env` · Redis con prefix `mem` · shared-network activa · firewall puertos 3002/3003 | ✅ Hecho (confirmar operativamente) |
| INIT-C-02 | Tests de conectividad desde local | DO | 1h | `Test-NetConnection 77.42.88.106 -Port 5432/6379/3002/3003` exitoso · conexión Prisma desde local OK · escritura a `/storage/` desde container OK | 🟡 Pendiente |
| INIT-C-03 | Distribuir SERVICE_KEY a agentes consumidores | DO | 1h | SERVICE_KEY distribuida vía secret management a: Runtime v1.1, Prompt Builder v1.3, Hook Manager, UI FE (via env var) | 🟡 Pendiente |
| INIT-C-04 | Documentar config VM en repo | DO | 1h | `docs/INFRASTRUCTURE.md` con: IP, puertos, credenciales ubicación, paths, backup schedule, escalación Admin VM, comandos útiles | 🟡 Pendiente |

**Dependencia externa:** cualquier cambio en VM requiere coordinar con Admin VM. Protocolo simple: DO solicita → PM escala si hay bloqueo.

---

### D. Agent Team Setup (5 tareas · 8h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-D-01 | Crear OPERATIVO por rol activo | PM + PJM | 3h | `.claude/agents/OPERATIVO_<ROL>.md` para los 12 roles. Ya existen: OPERATIVO_PM_MEMORY-SERVICE · OPERATIVO_TECH_LEAD. Pendientes: PJM, SA, AR, BE, DB, FE, UX, DL, QA, DO | 🟡 Parcial (2/12 hechos) |
| INIT-D-02 | PROJECT_MEMORY.md consolidado | PM | 0.5h | Memoria persistente del proyecto con stack, fases, decisiones, UUIDs | ✅ Hecho |
| INIT-D-03 | CONTEXTO de sesión por rol | PJM | 1h | `knowledge/agent-tasks/CONTEXTO_<ROL>_SESION.md` por rol activo. Ya existe: PM. Pendientes: TL, PJM, BE, FE, DB, DO, QA | 🟡 Parcial (1/7+) |
| INIT-D-04 | Distribuir accesos al equipo | PJM | 1h | Acceso repo Git + acceso VTT API (UUID + SERVICE_KEY) + acceso docs compartidos verificado por cada rol activo | 🟡 Pendiente |
| INIT-D-05 | Reuniones de onboarding por rol | PM | 2.5h | Sesión kick-off por cada rol activo: revisión SPEC, PROJECT_MEMORY, OPERATIVO, preguntas | 🟡 Pendiente |

**Nota:** roles SA, AR, UX pueden no necesitar onboarding profundo si solo entregan artefactos puntuales (requirements, arquitectura, flows).

---

### E. Tooling Setup (3 tareas · 4h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-E-01 | Base Node + TypeScript del backend | DO + TL | 2h | `package.json` con scripts (`dev`, `build`, `start`, `test`, `lint`, `format`, `migrate`, `seed`) · `tsconfig.json` estricto · `nodemon.json` · Node 20 pinneado en `.nvmrc` | 🟡 Pendiente |
| INIT-E-02 | Linters + formatters + pre-commit | DO | 1h | `.eslintrc.json`, `.prettierrc`, `.prettierignore` · Husky + lint-staged configurados para pre-commit (lint + prettier + type-check) | 🟡 Pendiente |
| INIT-E-03 | CI mínimo (smoke) | DO | 1h | GitHub Actions (o equivalente) con job `build + lint + test` en cada PR. CI completo (deploy) se implementa en MEM-105 | 🟡 Pendiente |

---

### F. Documentation (2 tareas · 2h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-F-01 | README + CONTRIBUTING del repo | PM + TL | 1h | `README.md` con descripción, stack, setup local, enlaces a docs · `CONTRIBUTING.md` con flow de commits/PRs/branches | 🟡 Pendiente |
| INIT-F-02 | ARCHITECTURE.md operativo | TL | 1h | Resumen arquitectónico breve en `docs/ARCHITECTURE.md` con link al SPEC v1.9 como fuente completa. No duplica SPEC, solo punto de entrada | 🟡 Pendiente |

**Nota:** `PROJECT_RULES.md` ya existe (v1.4). `PROJECT_MEMORY.md` ya existe.

---

### G. Kickoff (2 tareas · 3h)

| ID | Título | Rol | Horas | Qué produce | Estado |
|----|--------|-----|------:|-------------|--------|
| INIT-G-01 | Documento formal de Kickoff | PM | 2h | `KICKOFF_MEMORY_SERVICE.md` con: visión, objetivos, alcance, equipo, roadmap alto nivel, riesgos iniciales, criterios de éxito. Basado en SPEC v1.9 + HO formal | 🟡 Pendiente |
| INIT-G-02 | Primer sync del equipo (kickoff call) | PM + todos | 1h | Sesión de arranque, preguntas abiertas, confirmación de compromiso por rol, acta de kickoff con action items | 🟡 Pendiente |

---

## 5. MAPEO A TAREAS MEM ACTUALES EN VTT

Opciones para reconciliar con MEM-001..005 existentes:

### Opción A — Mantener MEM-001..005 como "umbrella" y usar INIT-* como sub-tareas operativas

**Ventaja:** no cambia VTT. **Desventaja:** VTT solo ve el umbrella.

| MEM actual | INIT-* que absorbe |
|-----------|---------------------|
| MEM-001 Infra Setup (DO, 2h) | INIT-C-01, INIT-C-02, INIT-C-03, INIT-C-04 (4 tareas · 4h) |
| MEM-002 Repo Structure (PJM, 2h) | INIT-B-01 a INIT-B-05 (5 tareas · 5h) |
| MEM-003 Team Onboarding (PJM, 1h) | INIT-A-01 a INIT-A-05 + INIT-D-* (10 tareas · 14h) |
| MEM-004 Tooling Setup (DO, 2h) | INIT-E-01 a INIT-E-03 (3 tareas · 4h) |
| MEM-005 Project Kickoff (PM, 4h) | INIT-F-01, INIT-F-02, INIT-G-01, INIT-G-02 (4 tareas · 5h) |

**Nuevo total Phase 1:** 32h (vs 11h actuales). Las horas de MEM-001..005 actuales deben **incrementarse** vía PATCH.

### Opción B — Expandir MEM-001..005 en VTT a MEM-001..024 (nuevas tareas)

**Ventaja:** trazabilidad completa en VTT. **Desventaja:** requiere crear 19 tareas nuevas en VTT (POST) y renumerar toda la fase Project Setup.

### Recomendación PM

**Opción A** para R1 — mantener MEM-001..005 pero **actualizar horas estimadas** a lo real (11h → 32h). Este documento sirve como desglose operativo. En R2 evaluar migrar a Opción B si VTT soporta sub-tareas.

---

## 6. DEPENDENCIAS CRÍTICAS DE INICIACIÓN

| # | Bloqueo | Desbloquea | Acción requerida |
|---|---------|------------|------------------|
| 1 | INIT-B-01 bloqueado | Toda la categoría B + ejecución de implementación | PM define multi-repo (PROJECT_RULES §8) |
| 2 | INIT-A-05 bloqueado | Gestión dependencias en VTT | DO/PM resuelven endpoint VTT de dependencias (HO v2.1 §10) |
| 3 | INIT-C-03 requiere acuerdo previo | Runtime, Prompt Builder, Hook Manager | DO coordina con equipos consumidores |
| 4 | INIT-D-01 parcial | Arranque operativo de cualquier rol | PM crea OPERATIVOs faltantes (10 de 12) |
| 5 | INIT-G-01 depende de HO formal | Kickoff formal | PM emite `CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE.md` (ya emitido ✅) |

---

## 7. ORDEN DE EJECUCIÓN SUGERIDO

```
SEMANA 0 (Pre-kickoff):
  C. VM Configuration (4 tareas, 4h) — verificación + docs
  B. Repository Setup (5 tareas, 5h) — requiere INIT-B-01 desbloqueado
  A.04 + A.05 — PATCH tareas en VTT + dependencias (pendiente endpoint)

SEMANA 1 (Onboarding):
  D. Agent Team Setup (5 tareas, 8h) — OPERATIVOs faltantes + accesos
  E. Tooling Setup (3 tareas, 4h) — base técnica
  F. Documentation (2 tareas, 2h) — README + ARCHITECTURE

SEMANA 1 (Kickoff):
  G. Kickoff (2 tareas, 3h) — doc + sync
  → Arranque formal de Phase 2 Discovery (ver HO_FASE_0_DISCOVERY.md)
```

---

## 8. CHECKLIST DE CIERRE DE INICIACIÓN

Antes de declarar "Project Setup" cerrado y arrancar Phase 2 Discovery:

```
VTT:
[ ] 116 tareas con assigneeId, complexity, category, estimatedHours correctos
[ ] Reassignments aplicados (MEM-022 → SA, MEM-039 → AR)
[ ] 15 dependencias críticas registradas
[ ] Deliveries (65) visibles y vinculadas a tareas

REPO:
[ ] Repo Git real confirmado y accesible
[ ] Estructura V3.1 inicializada (phases/, _pm/, docs/, archive/)
[ ] Branch protection en main
[ ] CODEOWNERS + PR template

VM:
[ ] Conectividad local → VM verificada (DB, Redis, /storage/)
[ ] SERVICE_KEY distribuida a Runtime, Prompt Builder, Hook Manager, FE
[ ] docs/INFRASTRUCTURE.md escrito

EQUIPO:
[ ] OPERATIVO_<ROL>.md creado para los 12 roles activos
[ ] CONTEXTO_<ROL>_SESION.md para roles principales (PM, PJM, TL, BE, FE, DB, DO, QA)
[ ] Acceso a repo + VTT + docs verificado por rol

TOOLING:
[ ] package.json con scripts funcionando
[ ] ESLint + Prettier + pre-commit hooks operativos
[ ] CI mínimo corriendo en PRs

DOCS:
[ ] README + CONTRIBUTING + ARCHITECTURE en el repo
[ ] KICKOFF doc firmado por PM

KICKOFF:
[ ] Kickoff call ejecutado, acta firmada
[ ] PJM confirma sprint 1 plan (Phase 2 Discovery)
```

---

## 9. RIESGOS DE INICIACIÓN

| # | Riesgo | Mitigación |
|---|--------|------------|
| IR-1 | Repo Git no definido bloquea todo | PM decide multi-repo **antes** de cualquier trabajo de código |
| IR-2 | Endpoint VTT de dependencias no llega | Registrar dependencias manualmente por ahora, migrar cuando exista |
| IR-3 | Admin VM no disponible para cambios | DO anticipa pedidos · PM escala si hay bloqueo `>24h` |
| IR-4 | OPERATIVOs incompletos bloquean onboarding | PM prioriza OPERATIVO_BE + OPERATIVO_DB + OPERATIVO_DO antes de Sprint S01 |
| IR-5 | Kickoff call no reúne al equipo completo | Grabación disponible · material asíncrono en KICKOFF doc |

---

## 10. SIGUIENTE PASO

Con este pre-handoff de iniciación + el pre-handoff de implementación, el PM tiene los dos insumos para generar el HO formal al PJM. Orden recomendado:

1. **Tú (Martin) aprobás este pre-handoff de iniciación**
2. **PM actualiza MEM-001..005 en VTT con horas reales** (11h → 32h) vía PATCH
3. **PM genera HO formal al PJM consolidado** (iniciación + implementación) o 2 HOs separados según preferencia
4. **PJM descompone los HOs en BRIEFs** operativos por rol/sprint
5. **Equipo ejecuta iniciación** (semana 0) antes del kickoff formal de Phase 2

---

**Documento:** PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ Listo para revisión PM  
**Fecha:** 2026-04-22  
**Complementa:** `PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md`

---

**PM — Martin Rivas**
