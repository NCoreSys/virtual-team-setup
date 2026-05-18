# ADR-001: Estrategia de Repositorios — Memory Service

## Metadata

| Campo | Valor |
|-------|-------|
| **ADR ID** | ADR-001 |
| **Titulo** | Estrategia de Repositorios — Memory Service |
| **Estado** | Aprobado |
| **Decidido por** | PM (Martin Rivas) |
| **Fecha propuesta** | 2026-04-23 |
| **Fecha decision** | 2026-04-23 |
| **Supersede** | N/A (primer ADR del proyecto) |
| **Superseded by** | N/A |
| **Tags** | `repositorios`, `gobernanza`, `gitflow`, `seguridad` |

---

## 1. Contexto

Memory Service es un servicio independiente de VTT (D-MEM-01) compuesto por:

- **Backend** Node.js 20 + Express + TypeScript + Prisma (puerto 3002)
- **Frontend** React + Vite + TailwindCSS standalone (puerto 3003)
- **Infra** Docker compose unificado, PostgreSQL `memory_service_db`, Redis `shared-redis`
- **Documentacion** SPEC v1.9, handoffs PJM, devlogs por tarea, knowledge base

El equipo activo opera con **8 roles agentes** (PM, PJM, TL, BE, DB, FE, QA, DO + soporte UX/DL/SA/AR) sobre 116 tareas en 10 fases (381h totales).

### Problema operativo detectado

Durante la operacion de proyectos previos (otro proyecto del mismo equipo) se detecto que los agentes IA (Claude Code) presentan los siguientes patrones:

1. **Scope leak**: cuando un agente trabaja en su tarea (ej: BE) y necesita "consultar" otro componente (ej: FE), termina **modificando** archivos fuera de su area asignada
2. **Cambios fantasma locales**: el agente edita archivos pero no los sube a git, contaminando el working tree y generando inconsistencias entre lo que el agente "cree" que existe y lo que esta versionado
3. **Bypass de branch protection**: pese a tener `main` protegida en monorepo, los agentes con rol Admin/Owner pueden mergear sin pasar por revision

La regla v1.4 del proyecto (`.claude/rules/PROJECT_RULES.md`) deja como pendiente la decision de "1 repo por agente" — esta directiva no tiene autor tecnico ni justificacion documentada.

### Decision pendiente

Definir formalmente la estrategia de repositorios (monorepo vs polirrepo vs 1-por-agente) con la justificacion de por que se elige y los costos aceptados.

---

## 2. Opciones Consideradas

### Opcion A — Monorepo unico con CODEOWNERS

Un solo repo `memory-service` con estructura `backend/`, `frontend/`, `infra/`, `docs/`.

**Pros:**
- 1 PR por feature cross (BE+FE+contratos)
- Types/contratos compartidos via `shared/` folder
- CI unificado con paths filters
- Documentacion centralizada
- Onboarding mas rapido (1 clone)

**Contras:**
- **No resuelve el problema de scope leak** — el agente sigue teniendo el filesystem completo en su workspace. CODEOWNERS bloquea merge pero no commit local
- Branch protection bypass por rol Admin sigue siendo viable
- Agente puede modificar archivos fuera de su scope y no hay barrera fisica que lo impida

**Veredicto:** Probada en proyecto previo del equipo. La gobernanza por software (CODEOWNERS + branch protection) **no fue suficiente** para detener el scope leak.

### Opcion B — Polirrepo de 2 (backend + frontend)

Dos repos: `memory-service-backend` y `memory-service-frontend`.

**Pros:**
- Separacion fisica BE vs FE
- Deploys desacoplados

**Contras:**
- Contratos API se desincronizan silenciosamente (no hay repo dedicado al contrato)
- Docs sin home claro (¿en backend o frontend?)
- Releases coordinados sin tooling de soporte

**Veredicto:** Mejora marginal sobre monorepo. El contrato API queda implicito en el backend, lo que invita drift.

### Opcion C — Polirrepo de 4 (categorizacion por componente) ✅

Cuatro repos especializados:

| Repo | Funcion |
|------|---------|
| `memory-service-project` | Docs, handoffs, ADRs, devlogs, knowledge, materiales PM/PJM |
| `memory-service-api` | **Contrato OpenAPI + types compartidos** (source of truth) |
| `memory-service-backend` | Implementacion Node + Express + Prisma + tests BE |
| `memory-service-frontend` | Implementacion React + Vite + tests FE |

**Pros:**
- Barrera fisica de scope: BE Agent sin token de write a `frontend` recibe `403 Forbidden` al push
- `memory-service-api` aislado evita que BE modifique contratos sin pasar por TL
- Cada agente clona solo su repo + read-only de los demas
- Cambios fantasma locales mueren al borrar el clone (no contaminan origin)
- Audit log claro por repo (Plan Team)
- Repository Rulesets aplicables por repo

**Contras (aceptados):**
- Releases coordinados pagan round-trip (BE merge → publish package → FE bump → FE merge)
- Refactors cross-cutting requieren multiple PRs
- Onboarding 2-3x mas lento (4 repos vs 1)
- Git history fragmentado (no `git bisect` cross-repo)
- Setup inicial: ~1.5h DO + ~30min PM

**Veredicto:** Resuelve el problema raiz (scope leak) con barrera fisica. Los costos son medibles y aceptables para el tamaño del equipo.

### Opcion D — Polirrepo "1 repo por agente"

Un repo por cada rol del equipo (BE, FE, DB, QA, DO, ...).

**Pros:** Ninguno claro.

**Contras:**
- Anti-patron: confunde organizacion de codigo con organigrama humano (Conway's Law mal aplicado)
- `schema.prisma` lo necesita BE pero lo edita DB → ¿en repo de quien vive?
- Cuando un rol no tiene agente activo (ej: DO part-time), su repo queda huerfano
- Escalado negativo: agregar BE #2 → ¿otro repo o comparten?
- Cero base tecnica documentada

**Veredicto:** Descartada explicitamente.

---

## 3. Decision

**Se adopta la Opcion C — Polirrepo de 4 categorizado por componente.**

Los repos ya existen y estan creados en la organizacion `prompt-ai-studio`:

- https://github.com/prompt-ai-studio/memory-service-project
- https://github.com/prompt-ai-studio/memory-service-api
- https://github.com/prompt-ai-studio/memory-service-backend
- https://github.com/prompt-ai-studio/memory-service-frontend

### Razones principales

1. **Resuelve el problema raiz** detectado en el proyecto previo: los agentes que no tienen token de write a un repo no pueden contaminarlo, ni siquiera localmente (push falla con 403).
2. **Los repos ya existen** — la decision esta parcialmente tomada por el coordinador. Este ADR la formaliza.
3. **`memory-service-api` aislado** desactiva el peor dolor del multirepo (drift de contratos): el contrato vive solo, lo escribe TL, lo consumen BE/FE via package npm versionado.
4. **Costos aceptados** son proporcionales al tamaño del equipo (5 roles activos de codigo) y al beneficio de control fisico.

### Decisiones derivadas (forman parte de este ADR)

#### D-ADR-001-A: Identidad de los agentes

Los agentes IA **no tendran cuentas GitHub propias**. Se opta por **Fine-grained Personal Access Tokens** generados desde una cuenta unica (la del coordinador o una cuenta tecnica `memory-service-bot`).

| Token | `project` | `api` | `backend` | `frontend` |
|-------|:---:|:---:|:---:|:---:|
| `PAT_MEM_PM` | Write | Read | Read | Read |
| `PAT_MEM_TL` | Write | **Write** | Write | Write |
| `PAT_MEM_BE` | Write (devlogs) | Read | **Write** | Read |
| `PAT_MEM_FE` | Write (devlogs) | Read | Read | **Write** |
| `PAT_MEM_DB` | Write (devlogs) | Read | **Write** (prisma/) | Read |
| `PAT_MEM_QA` | Write (devlogs) | Read | Read (tests/) | Read (tests/) |
| `PAT_MEM_DO` | Write (devlogs) | Read | **Write** (infra/, .github/) | Read |

**Trade-off aceptado:** CODEOWNERS no podra distinguir entre agentes (todos los PRs vienen de la misma cuenta GitHub). La gobernanza humana queda en la revision de PRs por TL/PM, complementada por convencion `[ROLE: XX]` en titulos de PR.

#### D-ADR-001-B: Gobernanza de ramas

En cada uno de los 4 repos:

- **Branch protection** sobre `main` con:
  - Require pull request before merging (1 approval minimo)
  - Require review from CODEOWNERS
  - Dismiss stale approvals on new commits
  - Require status checks to pass
  - Require linear history
  - **Do not allow bypassing the above settings** ← critico
  - Block force pushes y deletions
- **Repository Rulesets** (Plan Team) para reglas adicionales por path donde aplique
- **Roles GitHub** restringidos:
  - Solo `martin-rivas` (humano) tiene `Owner` de la org
  - TL tiene `Maintain`
  - Agentes tienen `Write` solo en sus repos asignados, `Read` en los demas
  - **Ningun agente tiene `Admin`**

#### D-ADR-001-C: Gestion de contratos cross-repo

El repo `memory-service-api` es el **source of truth** del contrato:

1. Define `openapi.yaml` con todos los endpoints
2. CI genera y publica `@prompt-ai-studio/memory-service-api-types` en GitHub Packages en cada release
3. Backend **valida** contra el contrato publicado (contract test en CI)
4. Frontend **consume** via `pnpm add @prompt-ai-studio/memory-service-api-types@^1.X`
5. Renovate bot bumpea automaticamente el paquete en `frontend` cuando hay version nueva

#### D-ADR-001-D: Workflow de feature cross-repo

Para una feature que toca BE+FE+contrato:

```
1. TL → PR en memory-service-api (spec OpenAPI)
2. TL → merge → CI publica @memory-service/api-types@1.X.0
3. BE Agent → PR en memory-service-backend (implementa contra contrato)
4. FE Agent (sesion paralela) → PR en memory-service-frontend (consume types)
5. PM → mergea ambos cuando ambos esten aprobados (en orden BE → FE)
6. CI deploya como unidad (mismo docker-compose)
```

#### D-ADR-001-E: Documentacion y artefactos por repo

| Tipo de artefacto | Repo donde vive |
|-------------------|-----------------|
| ADRs, handoffs, SPEC, METODOLOGIA | `memory-service-project` |
| OpenAPI spec, contract tests, types | `memory-service-api` |
| Codigo backend, tests BE, prisma schema, migrations | `memory-service-backend` |
| Codigo frontend, tests FE, assets | `memory-service-frontend` |
| Devlogs por tarea | `memory-service-project/devlogs/` |
| Code Logic por archivo | repo del codigo correspondiente, en `knowledge/code-logic/` |
| docker-compose.yml | `memory-service-backend/infra/` (referencia builds locales) |

---

## 4. Consecuencias

### Positivas

- **Scope fisico garantizado**: agente BE no puede pushear a `frontend` ni `api` (403 al push)
- **Cambios fantasma controlados**: si el agente modifica un repo donde no tiene write, el cambio muere localmente al borrar el clone
- **Contratos sincronizados via tooling**: drift silencioso eliminado por codegen + contract tests
- **Audit log limpio** (Plan Team): visibilidad de quien mergea que y cuando
- **Rotacion trimestral de PATs**: superficie de ataque limitada en el tiempo

### Negativas (aceptadas)

- **Onboarding ~2-3x mas lento**: nuevo agente clona 4 repos vs 1
- **Releases cross-feature requieren coordinacion**: feature flags obligatorios para rollouts seguros
- **Refactors cross-cutting cuestan mas**: 3+ PRs coordinados para renombrar un endpoint
- **Git history fragmentado**: `git bisect` solo funciona dentro de cada repo
- **CODEOWNERS no distingue por agente**: gobernanza humana adicional via PR review (TL/PM)

### Mitigaciones aplicadas

| Riesgo | Mitigacion |
|--------|-----------|
| Drift de contratos | Codegen automatico + contract tests obligatorios |
| Releases descoordinadas | Feature flags + manifesto de deploy por sprint |
| Refactors paralizados | Tareas VTT explicitamente "cross-repo" con PJM coordinando |
| Onboarding lento | Script de bootstrap (`./bootstrap.sh` clona los 4 repos en estructura esperada) |
| Documentacion dispersa | `memory-service-project` es el unico home de docs; los demas repos solo tienen README + LOGIC.md |

---

## 5. Plan de Implementacion

### Fase 1 — Setup base (responsable: DO, ~2h)

1. **Generar 4 Fine-grained PATs** desde la cuenta tecnica `memory-service-bot` (o cuenta del coordinador)
2. **Configurar Branch Protection** en `main` de los 4 repos con las reglas de D-ADR-001-B
3. **Activar Repository Rulesets** en cada repo (Plan Team)
4. **Configurar GitHub Teams** en `prompt-ai-studio` con permisos por team
5. **Activar Secret scanning + Push protection + Dependabot** en los 4 repos
6. **Configurar Environment "production"** en `backend` y `frontend` con required reviewer = `martin-rivas`

### Fase 2 — CI codegen (responsable: DO + TL, ~4h)

1. En `memory-service-api`: workflow GitHub Actions que en cada merge a main:
   - Valida `openapi.yaml`
   - Ejecuta `openapi-typescript` para generar types
   - Publica `@prompt-ai-studio/memory-service-api-types` en GitHub Packages con version bump
2. En `memory-service-backend` y `memory-service-frontend`: configurar `.npmrc` para autenticar contra GitHub Packages
3. En `memory-service-frontend`: setup Renovate para bump automatico del paquete

### Fase 3 — Migracion de contenido existente (responsable: PM + DO, ~2h)

Estado actual: el repo local en disco (`c:\Users\Martin\Documents\virtual-teams\memory-service\`) tiene mezcla de contenido que debe distribuirse en los 4 repos:

| Carpeta local actual | Destino repo |
|----------------------|--------------|
| `memory-service-project/` | `memory-service-project/` |
| `knowledge/` (devlogs, code-logic, agent-tasks) | `memory-service-project/knowledge/` |
| `.claude/agents/`, `.claude/rules/` | `memory-service-project/.claude/` |
| `devlogs/` | `memory-service-project/devlogs/` |
| _(codigo BE: aun no implementado)_ | `memory-service-backend/` (cuando arranque Sprint 2) |
| _(codigo FE: aun no implementado)_ | `memory-service-frontend/` (cuando arranque Design Handoff) |
| _(OpenAPI: aun no creado)_ | `memory-service-api/` (cuando se defina contrato) |

### Fase 4 — Distribucion de PATs y actualizacion de OPERATIVOs (responsable: PM, ~1h)

1. Actualizar cada `OPERATIVO_<ROL>_MEMORY-SERVICE.md` con:
   - Variable env del PAT a usar (`GITHUB_TOKEN_VAR=PAT_MEM_BE`, etc.)
   - Comandos git con scope al repo correspondiente
   - Procedimiento de rotacion trimestral
2. Eliminar referencias al repo local mezclado en docs operativos
3. Documentar en CONTEXTO_PM_SESION la nueva estructura

### Fase 5 — Decommission del repo local actual (responsable: PM, ~30min)

El working dir actual `c:\Users\Martin\Documents\virtual-teams\memory-service\` con remoto a `twitter-react.git` queda como archivo de referencia hasta que la migracion termine. Se renombra a `memory-service.legacy/` y se documenta en el index.

---

## 6. Criterios de Exito

La decision se considera **exitosa** si en 60 dias:

- [ ] 0 incidentes de scope leak (agente push a repo fuera de su rol)
- [ ] 0 incidentes de drift de contratos detectados en runtime
- [ ] >90% de PRs siguen el workflow cross-repo definido (BE → API → FE)
- [ ] Rotacion de PATs ejecutada al menos 1 vez sin incidente
- [ ] Audit log revisado semanalmente sin findings criticos

La decision se considera **fracasada** si en 60 dias:

- Se detectan >3 incidentes de drift de contratos por mes
- El overhead de coordinacion cross-repo bloquea >2 features en la ruta critica
- El equipo solicita revertir a monorepo

En caso de fracaso → ADR-002 reevaluando con datos reales.

---

## 7. Decisiones Pendientes / Out of Scope

- **Eleccion del package manager** para `memory-service-api` (npm vs pnpm vs yarn) → decision del TL
- **Eleccion del registry** (GitHub Packages vs npm publico privado) → propuesta: GitHub Packages por estar incluido en Plan Team
- **Politica de versionado** del package de types (SemVer estricto vs date-based) → decision TL
- **Estrategia de monorepo virtual con git submodules**: descartada inicialmente, no se reconsidera salvo que aparezca un caso fuerte
- **Renovate config**: configuracion default por ahora, refinar en Fase 2

---

## 8. Referencias

- Discusion previa: sesion PM 2026-04-23 (chat con coordinador)
- Repos creados: ver seccion 3
- Regla derogada: `.claude/rules/PROJECT_RULES.md` v1.4 §"Multi-repo pendiente" (sera removida en v1.5)
- Stack tecnico: `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` §16 (Docker compose)
- Integraciones cross-service: `ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md`
- Bloqueador relacionado: MS-117/MS-143 — remoto local mal configurado a `twitter-react.git`
- GitHub Plan Team — features disponibles: https://github.com/pricing

---

## 9. Aprobaciones

| Rol | Nombre | Fecha | Estado |
|-----|--------|-------|--------|
| **PM** | Martin Rivas | 2026-04-23 | **Aprobado** |
| **TL** | _(notificar)_ | — | Pendiente |
| **DO** | _(ejecutar Fase 1+2)_ | — | Pendiente |

---

## 10. Historial de Versiones

| Version | Fecha | Cambio | Autor |
|---------|-------|--------|-------|
| 0.1 | 2026-04-23 | Propuesta inicial | PM (sesion con coordinador) |
| 1.0 | 2026-04-23 | Aprobado por PM (Martin Rivas) | PM |

---

**Estado actual:** Aprobado. Implementacion en curso.
**Siguiente paso:** Tarea VTT para DO (Fases 1+2) creada. PROJECT_RULES actualizado a v1.5.
