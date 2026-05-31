# 00-platform — Plataforma VTT

> **Renombrado completado (2026-05-17):** de `00-agent-setup/` → `00-platform/`. El alcance ya no es solo "setup de agentes", sino la plataforma completa de conocimiento operativo VTT.

| Campo | Valor |
|---|---|
| **Versión** | 1.0 — Reorganización en 5 entidades |
| **Fecha** | 2026-05-17 |
| **Mantenedor** | PM Martin Rivas |
| **Propósito** | Fuente única de verdad de la plataforma VTT: agentes, normativa, templates, soporte y proyectos |

---

## 1. Para qué sirve este repo

`virtual-teams-setup/` es la **fuente única de verdad** de:

- **Cómo se organizan los agentes** (roles, setups, onboarding, kits, init-messages)
- **Cómo se opera el sistema** (Protocols, Workflows, Skills, Scripts, Rules)
- **Qué templates se usan** (BRIEF, ASSIGNMENT, manifest, handoffs, specs)
- **Documentación de soporte** (guías operativas, lecciones aprendidas)
- **Instancias por proyecto** (Memory Service y futuros)

Los proyectos consumidores (memory-service-project, memory-service-backend, futuros DesignMine, etc.) **referencian** este repo, no duplican su contenido.

## 2. Las 5 entidades

```
00-platform/
│
├── 01.agents/                    ← TODO sobre AGENTES (genérico, reutilizable)
├── 02.normativa/                 ← NORMATIVA: Rules + Protocols + Workflows + Skills + Scripts + catálogos
├── 03.templates/                 ← TEMPLATES genéricos (BRIEF, ASSIGNMENT, manifest, etc.)
├── 04.docs-soporte/              ← Guías operativas + lecciones + legacy
└── 05.proyectos/                 ← Instancias por proyecto (memory-service, futuros)
```

### Regla clave de organización

> **Lo genérico va en 01-04. Lo específico de un proyecto va en 05.**
>
> Si un documento tiene UUIDs reales, paths absolutos del proyecto, o nombres concretos de equipo → es **instancia** y vive en `05.proyectos/<proyecto>/`.
>
> Si un documento usa placeholders (`<PROJECT_ID>`, `<UUID_TL>`, etc.) o es agnóstico al proyecto → es **plantilla/genérico** y vive en 01-04.

## 3. Mapa detallado por entidad

### 3.1 `01.agents/` — Todo sobre agentes

```
01.agents/
├── roles/                        Perfiles base por rol (AGENT_PROFILE_BASE_*)
├── setups/                       Configs iniciales por rol (SETUP_BE, SETUP_DB, SETUP_TL, etc.)
├── onboarding/                   Cómo arranca un agente (01_ONBOARDING.md, 02_OPERACION_AGENTE.md)
├── operativos-templates/         Plantillas operativos por rol (OPERATIVO_*_TEMPLATE.md)
├── init-messages/                Mensajes iniciales por rol (INIT_BE.md, INIT_DO.md, etc.)
└── kits/                         Zips de kits por rol (KIT_TL_REVIEWER.zip, etc.)
```

**Cuándo entrar aquí:**
- Configurar un agente nuevo
- Editar el perfil base de un rol
- Crear/actualizar onboarding
- Empaquetar un kit nuevo

### 3.2 `02.normativa/` — La normativa operativa

```
02.normativa/
├── README.md                      ← Guía Normativa VTT (modelo de 4 niveles + Nivel 0)
├── INVENTARIO.md                  ← Inventario maestro con equivalencias legacy
│
├── 00.Rules/                      ← Nivel 0 — Reglas transversales (47 reglas activas)
│   ├── rules_catalog.json
│   ├── capabilities_catalog.json  (30 capabilities de doc_sec_02)
│   ├── roles_catalog.json         (9 roles + matriz RBAC)
│   ├── rules_schema.json
│   ├── query_rules.py             (motor de filtros funcional)
│   └── sources/                   (doc_sec_01..04 + AGENT_RULES_Rev — fuentes originales)
│
├── 01.Protocols/                  ← Nivel 4 — Procesos completos
│   ├── VTT.PROTOCOL-ASG-001       (Ciclo de asignación y cierre)
│   ├── VTT.PROTOCOL-GOV-001       (Esta guía normativa)
│   └── _pending-migration/        (21 SOPs/PROCESOS/FLUJOS legacy pendientes de convertir)
│
├── 02.Workflows/                  ← Nivel 3 — Sub-procesos (24 catalogados, 0 escritos)
├── 03.Skills/                     ← Nivel 2 — Capacidades reusables
│   └── _pending-migration/        (34 skills legacy del catálogo Memory Service)
├── 04.Scripts/                    ← Nivel 1 — Comandos atómicos
├── 05.Flowcharts/                 ← Diagramas mermaid
├── 06.Improvements/               ← Propuestas de mejora (IMPROVE-001 a 006)
│
└── catalogs/                      ← Datos de referencia (no procesos)
    ├── 04_ESTRUCTURA_FASES.md
    ├── 05_CATALOGO_DELIVERABLES.md
    ├── ANALISIS_FASES_COMPLETO_PARA_PM.md
    ├── ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md
    └── deliverables/              (50 archivos DICCIONARIO_FASE_* + catalog JSON)
```

**Cuándo entrar aquí:**
- Crear/editar un Protocol, Workflow, Skill o Script
- Consultar las reglas (`00.Rules/`) que aplican a una tarea
- Consultar el catálogo de los 438 deliverables del SDLC
- Proponer una mejora (`06.Improvements/`)
- Migrar un SOP/proceso legacy del `_pending-migration/`

### 3.3 `03.templates/` — Templates genéricos

```
03.templates/
├── tarea/                         BRIEF, ASSIGNMENT, devlog, code_logic genéricos
├── handoff/                       TEMPLATE_HANDOFF_TL_V2.1, guías de revisión
├── normativa/                     CLO, CFL, APR (templates de cierre)
├── memoria/                       MEMORY_TEMPLATE
├── contexto/                      CONTEXTO_*_SESION_TEMPLATE (sesión por rol)
├── specs-design/                  TEMPLATE_BASE_Spec_* (12+ specs UI/UX)
└── setup-vtt/                     Templates para setup de proyecto VTT
```

**Cuándo entrar aquí:**
- Instanciar un nuevo BRIEF/ASSIGNMENT
- Crear template nuevo
- Spec de UI/UX

### 3.4 `04.docs-soporte/` — Documentación complementaria

```
04.docs-soporte/
├── guias-operativas/              GUIA_WORKTREES, GUIA_ASIGNACION_TL_*, etc.
├── lecciones/                     Lecciones aprendidas (ADDON_PASO0_ADR_REPOS_*)
└── legacy/                        Documentos viejos pendientes de migrar/eliminar
```

**Cuándo entrar aquí:**
- Buscar una guía operativa específica (worktrees, asignación, revisión)
- Consultar una lección aprendida
- Archivar un doc viejo

### 3.5 `05.proyectos/` — Instancias por proyecto

```
05.proyectos/
└── memory-service/
    ├── Proyect_data.md            UUIDs y datos del equipo Memory Service
    ├── operativos-instancias/     OPERATIVO_BE_MEMORY-SERVICE.md, etc. (18 instancias)
    ├── templates-proyecto/        Templates específicos del proyecto (futuro)
    ├── living-documents/          LIVING_DOCUMENTS_MEMORY_SERVICE.md
    ├── setup-proyecto/            SETUP_HETZNER_COMPARTIDO.md, etc.
    └── onboarding/                ONBOARDING_AGENTE_EJECUTOR_MEMORY_SERVICE.md, ONBOARDING_TL_*.md
```

**Cuándo entrar aquí:**
- Cuando trabajas con el proyecto específico (Memory Service hoy)
- Cuando agregas un proyecto nuevo (crear `05.proyectos/<nuevo>/`)

## 4. Onramp por rol — ¿Qué leo primero?

### 4.1 Soy un agente nuevo (BE, DB, FE, DO, QA, etc.)

```
1. 01.agents/onboarding/01_ONBOARDING.md
2. 01.agents/onboarding/02_OPERACION_AGENTE.md
3. 01.agents/roles/AGENT_PROFILE_BASE_<MI_ROL>.md
4. 01.agents/setups/SETUP_<MI_ROL>.md
5. 01.agents/init-messages/INIT_<MI_ROL>.md
6. 05.proyectos/memory-service/operativos-instancias/OPERATIVO_<MI_ROL>_MEMORY-SERVICE.md
```

### 4.2 Soy el Tech Lead

```
1. Lo del agente arriba
2. 02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md
3. 04.docs-soporte/guias-operativas/GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md
4. 04.docs-soporte/guias-operativas/GUIA_REVISION_TAREA_TL_REVIEWER.md
5. 02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md
6. 02.normativa/01.Protocols/_pending-migration/PROCESO_CIERRE_TAREA_v2.md
7. 02.normativa/01.Protocols/_pending-migration/PROCESO_ASIGNACION_TAREAS_v3.md
```

### 4.3 Soy el PJM

```
1. Lo del agente
2. 02.normativa/01.Protocols/_pending-migration/02.PJM_PROCESO_SETUP_PROYECTO_VTT.md
3. 02.normativa/01.Protocols/_pending-migration/SOP_GENERACION_HO_PJM.md
4. 02.normativa/01.Protocols/_pending-migration/SOP_GENERACION_SPRINT_DOCS.md
5. 02.normativa/catalogs/ANALISIS_FASES_COMPLETO_PARA_PM.md
```

### 4.4 Soy el PM

```
1. Lo del agente
2. 02.normativa/README.md (Guía Normativa VTT)
3. 02.normativa/01.Protocols/_pending-migration/01_PM_PROCESO_ANALISIS_INICIAL.md
4. 02.normativa/01.Protocols/_pending-migration/SETUP_PROCESS_PM.md
5. 02.normativa/06.Improvements/ (revisar IMPROVE-001 a 006 pendientes de decisión)
```

### 4.5 Estoy escribiendo un Protocol o Workflow nuevo

```
1. 02.normativa/README.md — Modelo de 4 niveles
2. 02.normativa/INVENTARIO.md — qué documentos existen
3. 02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001 — ejemplo de Protocol completo
4. 03.templates/normativa/ — templates de salidas operativas (APR, CLO, CFL)
```

## 5. Cómo se consumen estos documentos desde proyectos

Cada proyecto (memory-service, futuro DesignMine, etc.) consume este repo:

```
memory-service/
├── memory-service-project/
│   ├── NORMATIVA_VTT_POINTER.md         ← apunta a virtual-teams-setup/
│   └── knowledge/                       ← artefactos del proyecto (BRIEF, ASSIGNMENT, manifests)
└── memory-service-backend/
    └── NORMATIVA_VTT_POINTER.md         ← idem
```

Política actual de paths (Opción C — durante migración):

```
1. Path canónico:  ../virtual-teams-setup/00-platform/02.normativa/...
2. Fallback legacy: ./00-platform/... (copia temporal en el proyecto)
```

Ver `IMPROVE-004_rules_como_feature_vtt.md` para la propuesta futura de Hook Manager + endpoints VTT que resolverán la propagación de cambios sin copy-paste manual.

## 6. Política de gobierno editorial

**Quién puede editar qué:**

| Carpeta | Quién edita | Aprobación |
|---|---|---|
| `01.agents/roles/`, `setups/`, `init-messages/`, `kits/` | Equipo Perfiles | PM |
| `01.agents/onboarding/` | Equipo Perfiles + TL | PM |
| `02.normativa/` (Protocols, Workflows, Skills, Scripts, Rules) | TL + PM | PM |
| `02.normativa/catalogs/deliverables/` | PJM + TL | PM |
| `03.templates/` | TL (con review PM) | PM |
| `04.docs-soporte/guias-operativas/` | Equipo Worktrees + TL | PM |
| `05.proyectos/memory-service/` | TL Memory Service | PM |

**Proceso de cambios:** todo cambio en VTT-setup va por PR (cuando convertamos a git repo). Mientras tanto, coordinación directa con PM.

Pendiente formalizar (TODOs):
- Convertir a repo git con branch protection
- CODEOWNERS por carpeta
- Sistema de tickets de mejora (los proyectos no editan VTT-setup directamente — levantan ticket)

## 7. TODOs pendientes

### Renombrado y limpieza

- [ ] **Renombrar `00-platform/` → `00-platform/`** (bloqueado por Windows lock — reintentar cuando se libere)
- [ ] Migrar 21 documentos de `02.normativa/01.Protocols/_pending-migration/` a Protocols VTT con código `VTT.PROTOCOL-*`
- [ ] Migrar 34 skills legacy de `02.normativa/03.Skills/_pending-migration/` al modelo Skill VTT
- [ ] Limpiar carpeta `04.docs-soporte/legacy/` cuando los docs ya no se referencien

### Gobierno

- [ ] Convertir `virtual-teams-setup/` a repo git con `git init`
- [ ] Crear `CODEOWNERS` con propiedad por carpeta
- [ ] Documento `GOBIERNO_VTT_SETUP.md` formal
- [ ] Proceso de tickets de mejora desde proyectos consumidores
- [ ] Sistema de releases con versionado SemVer (releases/v1.0.0/, etc.)

### Sincronización con proyectos

- [ ] Definir si los `operativos-instancias/` se quedan en VTT-setup o se mueven al repo del proyecto
- [ ] Implementar IMPROVE-004 (Rules como feature VTT) para que el Hook Manager inyecte normativa automáticamente
- [ ] Implementar IMPROVE-002 (BD de Manifiestos) para que los manifests JSON sean consultables

### Drift conocido

- [ ] `Docs/01-documentacion/` contiene copias de docs que también viven en `02.normativa/` y otros lugares — consolidar progresivamente
- [ ] `Docs/01-documentacion/_deprecated/RCBA/` movido aquí — equivalente en `02.normativa/00.Rules/sources/`
- [ ] Los `Docs/`, `archive/`, `Reportes/`, `00-cursos/` (raíz del repo) NO se tocaron en esta reorganización

## 8. Verificación rápida del repo

```bash
# Contar archivos por entidad
cd 00-platform
for d in 01.agents 02.normativa 03.templates 04.docs-soporte 05.proyectos; do
  count=$(find "$d" -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" -o -name "*.zip" \) 2>/dev/null | wc -l)
  echo "$count $d"
done

# Validar catálogo de reglas
python 02.normativa/00.Rules/query_rules.py --validate

# Simular reglas aplicables a una tarea típica
python 02.normativa/00.Rules/query_rules.py --simulate-task MS-285
```

## 9. Documentos relacionados

- `02.normativa/README.md` — Guía Normativa VTT (modelo de 4 niveles + Nivel 0)
- `02.normativa/INVENTARIO.md` — Inventario maestro con equivalencias legacy
- `02.normativa/00.Rules/README.md` — Sistema de Rules
- `02.normativa/06.Improvements/README.md` — Mejoras propuestas

## 10. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-17 | **Reorganización mayor**: de 12 carpetas top-level desordenadas a **5 entidades** (agents/normativa/templates/docs-soporte/proyectos). 21 SOPs legacy movidos a `_pending-migration/`. 34 skills legacy movidas a `_pending-migration/`. Sources de reglas consolidadas. Catálogos centralizados. Documentos específicos de Memory Service movidos a `05.proyectos/memory-service/`. RCBA deprecada. README maestro creado. |
