# ADD-ON — Paso 0: ADR Estrategia de Repositorios (Lección Aprendida)

| Campo | Valor |
|-------|-------|
| **Documento** | ADDON_PASO0_ADR_REPOS_LECCION_APRENDIDA.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-23 |
| **Autor** | PM (Martin Rivas) |
| **Propósito** | Lección aprendida del proyecto Memory Service. Define la necesidad de un PASO 0 en el proceso PM y los ajustes derivados a templates y procesos existentes. |
| **Caso origen** | Memory Service R1 — ADR-001 estrategia de 4 repos |
| **Estado** | ✅ Listo para integrar |

---

## 1. PROBLEMA DETECTADO

Durante la planeación de Memory Service R1, el PM avanzó hasta el **PASO 6 del proceso de cierre PM** (CIERRE + Handoff operativo) **sin tener decidida la estrategia de repositorios**.

**Síntoma:** al generar `ESTRUCTURA_REPO_MEMORY_SERVICE.md v1.0`, se asumió monorepo único. Días después se aprobó **ADR-001** (polirrepo de 4 repos categorizado), invalidando v1.0 y requiriendo regenerar el documento como v2.0 con distribución cross-repo.

**Causa raíz:** el proceso original (`09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` v1.0 / actuales `01_PM_PROCESO_ANALISIS_INICIAL.md` y derivados) **no exige** que la estrategia de repositorios esté definida antes de generar la estructura física. Tampoco lo exigen los templates de iniciación (`TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md`).

---

## 2. AJUSTES PROPUESTOS

### 2.1 Agregar PASO 0 al proceso PM

**Antes** del PASO 1 (Leer análisis de feature) — agregar:

```
PASO 0 — Definir estrategia de repositorios (ADR de gobernanza)
```

#### Contenido del paso

| Aspecto | Detalle |
|---------|---------|
| **Inputs** | Stack del proyecto · Composición del equipo (cuántos roles ejecutan código) · Restricciones de gobernanza (ej. "agentes IA con scope físico") · Experiencia de proyectos previos (incidentes de scope leak) |
| **Acciones del PM** | 1. Evaluar opciones (monorepo / polirrepo BE+FE / polirrepo categorizado / 1 repo por agente)<br>2. Documentar pros/contras de cada opción (no solo la elegida)<br>3. Decidir con criterio explícito<br>4. Formalizar como ADR-001 |
| **Outputs** | `ADR-001_estrategia_repositorios.md` aprobado · Repos creados en la org · PATs por rol generados · Branch protection configurado |
| **Template ref** | `ADR-001_estrategia_repositorios.md` (caso Memory Service: polirrepo de 4) |
| **Gate** | ADR firmado por PM · Pros/contras documentados · Decisiones derivadas (PATs, gobernanza, workflow) explícitas · Repos creados antes de pasar al PASO 1 |

#### Reglas adicionales del PASO 0

1. **Descartar siempre "1 repo por agente"** — anti-patrón documentado: confunde código con organigrama humano (Conway's Law mal aplicado).
2. **Si el proyecto tiene >5 roles ejecutores con riesgo de scope leak → considerar polirrepo categorizado** (project + api + backend + frontend) como opción base.
3. **Si el proyecto tiene contratos cross-service (otros sistemas que consumen una API) → aislar el contrato en repo dedicado** (`<proyecto>-api`).

### 2.2 Actualizar `TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md`

**Sección a agregar** después de la introducción del template:

```markdown
## 0. PRERREQUISITO — Estrategia de Repositorios definida

Antes de llenar este template, validar que existe `ADR-XXX_estrategia_repositorios.md` aprobado por PM.

**Si la estrategia es monorepo:** las tareas de la categoría B (Repository Setup) crean 1 repo.

**Si la estrategia es polirrepo:** las tareas de la categoría B se multiplican por N repos. Agregar:
- INIT-B-01a..N: Crear repo N (uno por componente)
- INIT-B-02a..N: Inicializar estructura de cada repo (script init_structure_<repo>.sh)
- INIT-B-04a..N: Branch protection + CODEOWNERS por repo
- INIT-B-06: Generar PATs por rol con scope correcto
- INIT-B-07: Bootstrap script + workspace files (.code-workspace por rol)
- INIT-B-08: Documentar workflow operativo multi-repo
```

### 2.3 Agregar a "Errores Comunes" del proceso PM

| Error | Consecuencia | Corrección |
|-------|--------------|------------|
| Generar estructura de repo (INIT-B-02) antes de tener ADR de gobernanza aprobado | Estructura asume monorepo y se invalida cuando se aprueba multi-repo · retrabajo de docs físicos | **PASO 0 obligatorio: ADR de gobernanza antes que cualquier blueprint físico** |
| Olvidar `.claude/agents/` en el setup multi-repo | Claude Code no encuentra OPERATIVOs cuando trabaja en repo de código | Regla: todo agente activo incluye `<proyecto>-project` en su workspace `.code-workspace` |
| No definir cómo trabajan físicamente los agentes con N repos | Confusión "¿abro N ventanas de VS Code?" · sesiones desorganizadas | Generar `WORKFLOW_OPERATIVO_MULTIREPO_<PROYECTO>.md` + `.code-workspace` por rol |
| Distribuir devlogs entre los N repos | Imposible auditar trabajo cross-repo · devlogs perdidos | Devlogs SIEMPRE en `<proyecto>-project/devlogs/` con prefijo `[ROL]` |
| Code-logic en `<proyecto>-project` separado del código | Espejo de `src/` se desincroniza · muerto al primer refactor | Code-logic vive en repo del código, en `knowledge/code-logic/` |

### 2.4 Crear nuevo template

Sugerencia: agregar al `05.Templates/01.SETUP/01_PM/`:

- `TEMPLATE_ADR_ESTRATEGIA_REPOSITORIOS_V1.0.md` — basado en `ADR-001_estrategia_repositorios.md` de Memory Service
- `TEMPLATE_WORKFLOW_OPERATIVO_MULTIREPO_V1.0.md` — basado en `WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md`
- `TEMPLATE_ESTRUCTURA_REPO_V2.0.md` — versión multi-repo del v1.0 monorepo (overwrites el actual o coexiste)

---

## 3. UBICACIONES SUGERIDAS DE ESTOS CAMBIOS

Dada la reorganización actual de `00-platform/`:

| Cambio | Archivo a modificar | Carpeta |
|--------|---------------------|---------|
| PASO 0 al inicio del proceso | `01_PM_PROCESO_ANALISIS_INICIAL.md` o el doc maestro PM | `04.Process/` |
| Errores comunes | Mismo doc del proceso PM | `04.Process/` |
| Sección 0 del template iniciación | `TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md` | `05.Templates/01.SETUP/01_PM/` |
| Templates nuevos (ADR, workflow, estructura v2) | Crear 3 archivos nuevos | `05.Templates/01.SETUP/01_PM/` |
| Actualizar índice de templates | `INDEX_TEMPLATES_CIERRE_PM_HANDOFF_PJM.md` | `05.Templates/01.SETUP/01_PM/` |

---

## 4. ARTEFACTOS YA GENERADOS (caso Memory Service)

Como evidencia y referencia para los templates:

| Artefacto | Ruta | Reusable como template |
|-----------|------|------------------------|
| ADR de gobernanza | `Release2.0/01-PM/ADR-001_estrategia_repositorios.md` | ✅ → TEMPLATE_ADR_REPOSITORIOS |
| Estructura física multi-repo | `Release2.0/01-PM/ESTRUCTURA_REPO_MEMORY_SERVICE.md` v2.0 | ✅ → TEMPLATE_ESTRUCTURA_REPO_V2 |
| Workflow operativo | `Release2.0/01-PM/WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md` | ✅ → TEMPLATE_WORKFLOW_MULTIREPO |
| Workspaces VS Code (9) | `Release2.0/scripts/workspaces/*.code-workspace` | ✅ → templates por rol |
| README de workspaces | `Release2.0/scripts/workspaces/README.md` | ✅ |

---

## 5. CHECKLIST PARA INTEGRAR ESTA LECCIÓN

```
[ ] Agregar PASO 0 al proceso PM principal en 04.Process/
[ ] Agregar sección "Errores comunes" relacionada a estrategia de repos
[ ] Modificar TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md con sección 0
[ ] Crear TEMPLATE_ADR_ESTRATEGIA_REPOSITORIOS_V1.0.md (basado en ADR-001 de Memory Service)
[ ] Crear TEMPLATE_WORKFLOW_OPERATIVO_MULTIREPO_V1.0.md
[ ] Crear TEMPLATE_ESTRUCTURA_REPO_V2.0.md (multi-repo)
[ ] Crear templates de .code-workspace por rol (9 archivos)
[ ] Actualizar INDEX_TEMPLATES_CIERRE_PM_HANDOFF_PJM.md con los nuevos templates
[ ] Validar que el flujo PM ahora ordena: ADR → Análisis → Filtro → Iniciación → Consolidado → Cierre → Seed → Script → HO PJM
```

---

## 6. POR QUÉ ESTE ADD-ON SEPARADO Y NO EDIT IN-PLACE

Tu reorganización reciente de `00-platform/` (de `agent-setup/standard/templates/` → `01.agent-setup/02.roles/03.standard/04.Process/05.Templates/06.Documentos_soporte/`) implica que los procesos y templates están en archivos que tú ya tocaste y posiblemente modificaste con criterios que yo no veo.

Dejo este add-on como **propuesta documentada** para que tú decidas dónde y cómo integrarlo, sin sobreescribir tus ajustes.

---

**Documento:** ADDON_PASO0_ADR_REPOS_LECCION_APRENDIDA.md
**Versión:** 1.0
**Estado:** ✅ Listo para integrar
**Fecha:** 2026-04-23

---

**PM — Martin Rivas**
