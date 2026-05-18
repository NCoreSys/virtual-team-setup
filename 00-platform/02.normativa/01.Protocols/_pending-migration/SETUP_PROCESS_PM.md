
Set up
@.claude/agents/product-manager.md -- identidad 
@memory-service-project/00-platform/agent-setup/SETUP_PM.md -- set up agente Pm
| `.claude/agents/OPERATIVO_PM_MEMORY-SERVICE.md` | ❌ Falta |
| `knowledge/PROJECT_MEMORY.md` | ✅ Existe |
| `knowledge/agent-tasks/CONTEXTO_PM_SESION.md` | ❌ Falta |
OPERATIVO_TECH_LEAD.md` activo. Lo leo para extraer UUIDs del equipo.
1. Leer los 2 archivos del estándar (`02_OPERACION_AGENTE.md`, `08_FLUJO_PM.md`) si es primera vez en la plataforma.
@memory-service-project/Release2.0/Analisis/METODOLOGIA_TRABAJO_PM_VTT.md
---
archivos del proyecto
`@memory-service-project/Release2.0/01-PM/MEMORY_SERVICE_METODOLOGICO_v1.1.md`
@memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md  
@memory-service-project/Release2.0/01-PM/METODOLOGIA_MEMORY_SERVICE_v1.2.md  
@memory-service-project/Release2.0/01-PM/ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md
---

```
Estructura del proecyto
@memory-service-project/Release2.0/Analisis/ANALISIS_FASES_COMPLETO_PARA_PM.md 
@memory-service-project/Release2.0/Analisis/ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md 
@C:\Users\Martin\Documents\virtual-teams\virtual-teams-tracking\_project-management\Fases\11 Gestion de Proyectos\R3\00 Analisis\01 PM\METODOLOGIA_MODELO_DINAMICO_V3.md
```
se genran las fases aplciables
@memory-service-project/00-platform/SETUP_HETZNER_COMPARTIDO.md 

ejemplos de hand off
@memory-service-project/Release2.0/Analisis/CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md 
@memory-service-project/Release2.0/Analisis/HANDOFF_PJM_ADDENDUM_V4.5.md 


 # Paso 1: Leer análisis de feature

  **PASO 1 completado — Cuatro documentos PM leídos.** 

### Resumen en 1 párrafo (prueba de entendimiento)

Memory Service es un **sistema independiente** (no parte de VTT) de **memoria centralizada para agentes de IA** que importa conversaciones de **5 fuentes** (CLAUDE_CLI, CLAUDE_WEB, CLAUDE_SDK, CHATGPT, VTT_CHANNEL), las clasifica por **reglas determinísticas**, persiste `contentPreview` en BD + contenido completo en `/storage/`, y entrega **contexto estructurado a Runtime en <500ms síncrono con fail-fast**. Corre en puertos 3002 (API) y 3003 (UI), con SERVICE_KEY auth para integraciones (Runtime, Prompt Builder, Hook Manager) y endpoints públicos para la UI standalone. Principio fundamental: **storage es fuente de verdad del contenido**; **BD solo indexa metadata**; **no consulta a VTT en runtime** (Runtime envía datos desnormalizados en el import).

### Cobertura documental observada

| Doc | Versión | Estado declarado | Congelado |
|---|---|---|---|
| METODOLÓGICO | 1.1 | BORRADOR PARA VALIDACIÓN PM | ❌ |
| METODOLOGÍA | 1.1 (archivo dice v1.2) | LISTO PARA VALIDACIÓN | ❌ |
| SPEC | 1.8 (archivo dice v1.9) | CONSOLIDADO SA — PENDIENTE CIERRE FINAL PM REVISOR | ❌ |
| ADDENDUM integración | 1.1 | BORRADOR — PENDIENTE CIERRE PM | ❌ |

**Los 4 documentos PM están técnicamente sin cierre formal.** Todos esperan mi firma como PM.

### Discrepancias / gaps detectados (para cuestionar, no resolver solo)

| # | Discrepancia | Qué implica |
|---|---|---|
| **G1** | PROJECT_MEMORY dice **116 tareas, 381h** (HO v2.1). SPEC v1.9 §14 dice **150h** (76h BE + 74h UI). Gap de 231h. | Alguien ajustó el alcance y no lo reflejó en ambos docs. Pendiente aclarar cuál manda. |
| **G2** | Nombres de archivo (v1.9, v1.2) ≠ versión interna declarada (v1.8, v1.1). | Inconsistencia de versionado. Riesgo: lectores no saben qué "final" es. |
| **G3** | Metodológico tiene Q-01, Q-03, Q-04, Q-05 abiertas, pero SPEC ya las cierra (D-MEM-36, D-MEM-26, METODOLOGIA §12.1, D-MEM-37). | Metodológico debe actualizarse o marcarse como obsoleto. |
| **G4** | ADDENDUM modifica SPEC (§5.2 platformRefs, §5.3 índice GIN). SPEC v1.8 **no** incluye aún estos cambios. | Gap de integración entre addendum y SPEC base. |
| **G5** | Metodológico tiene **4 fuentes** (CLI, Web, SDK, ChatGPT). METODOLOGÍA+SPEC tienen **5** (agrega VTT_CHANNEL). | Metodológico está desactualizado. |
| **G6** | Metodológico y METODOLOGÍA están en subcarpeta `01-PM/` pero también el SPEC. No hay separación clara entre docs de producto (PM) y técnicos (SA/AR/TL). | Organización. Menor. |

### Preguntas/decisiones que me toca validar como PM

1. **¿Cierro SPEC v1.9 como PM Revisor** (estado final)? Si sí, debo resolver G2-G5 primero.
2. **¿Valido METODOLÓGICO v1.1** o lo marco como obsoleto (reemplazado por METODOLOGÍA v1.1 + SPEC v1.8)?
3. **¿Apruebo ADDENDUM v1.1** y disparo sub-task para integrar §5.2 y §5.3 en el SPEC base?
4. **¿Cuál es el alcance real del proyecto:** las 116 tareas/381h del HO v2.1, o las 76h+74h del SPEC §14?

### Propuesta del siguiente paso (PASO 2 — Identificar fase actual)

Antes de avanzar a cobertura y plan de trabajo, necesito que me indiques:

- **(a)** La **fase SDLC actual** del proyecto (el SPEC sugiere que estamos al final de Analysis/Design Technical, pero no arrancó Development), o
- **(b)** Si esperas que yo **consulte VTT vía API** para verificar el estado real de las 116 tareas y de ahí inferir la fase, o
- **(c)** Si prefieres que primero **resuelva los 6 gaps (G1-G6)** antes de avanzar a PASO 2.

      ↓
 # Paso 2: Cerrar docs PM (freeze)
      ↓

      ### Cierre de documentos PM — 2026-04-21

| Documento | Antes | Ahora |
|---|---|---|
| [SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md](memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md) | v1.8 — CONSOLIDADO SA PENDIENTE | **v1.9 — ✅ APROBADO PM, CIERRE FINAL** |
| [ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md](memory-service-project/Release2.0/01-PM/ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md) | BORRADOR PENDIENTE CIERRE PM | **✅ APROBADO PM — INTEGRADO AL SPEC v1.9** |
| [MEMORY_SERVICE_METODOLOGICO_v1.1.md](memory-service-project/Release2.0/01-PM/MEMORY_SERVICE_METODOLOGICO_v1.1.md) | BORRADOR PARA VALIDACIÓN PM | **🔴 OBSOLETO — conservado como histórico** |
| [METODOLOGIA_MEMORY_SERVICE_v1.2.md](memory-service-project/Release2.0/01-PM/METODOLOGIA_MEMORY_SERVICE_v1.2.md) | LISTO PARA VALIDACIÓN | Sigue vigente (no requirió cambios) |

### Gaps resueltos

- **G2 (versionado)**: SPEC header/footer/changelog ahora dicen v1.9 — alineado con el nombre de archivo.
- **G3 (Q-XX obsoletas)**: METODOLÓGICO marcado como obsoleto con mapeo explícito de Q-01→D-MEM-36, Q-03→D-MEM-26, Q-04→METODOLOGIA §12.1, Q-05→D-MEM-37.
- **G4 (ADDENDUM integración)**: §5.2 (platformRefs Runtime) integrada en SPEC §4.1 como comentario del campo `platformRefs`. §5.3 (índice GIN `idx_conv_runtime_run`) integrada en SPEC §6.1.
- **G5 (5 fuentes)**: resuelto vía cierre de METODOLÓGICO (tenía 4 fuentes). SPEC y METODOLOGIA ya tienen las 5.
- **Alcance 381h**: SPEC §14 marcada como OBSOLETA con apuntador explícito a `HO_ACTUALIZAR_TAREAS_VTT.md v2.1`.

### Siguiente paso

Mis preguntas cerradas. Según metodología, el siguiente paso es **PASO 2 — Identificar fase actual** (vía query a VTT o confirmación directa). ¿Avanzo a PASO 2, o prefieres que antes resuelva los pendientes técnicos (repo Git, multi-repo, endpoint deps)?
 # Paso 3: Filtrar deliverables aplicables
      ↓

      Entendido completo. Cierro el mapeo con los números reales:

### Inventario real del proyecto

| Fase | Deliveries VTT | Tareas MEM | Deliverables SDLC aplicables |
|---|---|---|---|
| 1. Project Setup | 1 | MEM-001..005 (5) | — (setup, no SDLC) |
| 2. Discovery | 2 | MEM-006..009 (4) | 10 de 22 |
| 3. Planning | 6 | MEM-010..017 (8) | 33 de 33 |
| 4. Analysis | 8 | MEM-018..025 (8) | 47 de 47 |
| 5. Design UX/UI | 6 | MEM-026..038 (13) | 47 de 72 |
| 6. Design Technical | 9 | MEM-039..047 (9) | 70 de 73 |
| 7. Development | 10 | MEM-048..093 (46) | 78 de 78 |
| 8. Testing | 10 | MEM-094..103 (10) | 45 de 52 |
| 9. Deploy | 7 | MEM-104..110 (7) | 38 de 38 |
| 10. Operations | 6 | MEM-111..116 (6) | 23 de 23 |
| **TOTAL** | **65** | **116** | **391 de 438 (89%)** |

> El "69 deliveries" que mencionaste probablemente es aproximado — cuento 65 exactos en el HO v2.1, pero la estructura está clara.

### Qué ya tenemos vs. qué falta

**Fase 6 (Design Technical)** — 9 deliveries: prácticamente **cubierta** por los 4 docs PM que cerré hoy.

| Delivery VTT | Cubierto por |
|---|---|
| Solution Architecture | SPEC §1, §4, §13 |
| Code Architecture | SPEC §3.2 (folder structure), §9 (flujos) |
| Database Design | SPEC §4.1 (schema Prisma), §5 (seeds), §6 (indexes) |
| API Design | SPEC §7 (auth), §8, §11 (context), §15 (aceptación) |
| Sequence Diagrams | SPEC §9, §10 (parcialmente, en ASCII) |
| ADRs | SPEC §2 (43 D-MEM) + ADDENDUM (5 D-INT) — **falta formato ADR formal** |
| Security Plan | SPEC §7 (SERVICE_KEY), §15.4 |
| Infrastructure Plan | SPEC §1.4, §16 (docker-compose) |
| Technical Estimates | SPEC §14 (marcada obsoleta, reemplazar con plan real) |

**Resto**: fases 2, 3, 4, 5, 7, 8, 9, 10 → documentación por crear casi en blanco.

### Lo que implica crear

- **Estructura física V3.1**: crear `phases/00-discovery/... phases/07-operations/` (crear solo carpetas cuando haya archivos).
- **391 documentos de deliverable** a lo largo del ciclo (no todos de una, se construyen conforme la fase avanza).
- **Mapeo explícito** de cada `MEM-XXX` → `phases/XX-name/deliverables/archivo.md` para trazabilidad.

### Antes de ejecutar — preguntas de alcance

1. **¿Dónde van las fases?** Opciones:
   - **(a)** Dentro de `memory-service-project/` (paralelo a `Release2.0/`).
   - **(b)** En la raíz del repo (`phases/` al nivel de `src/`, `knowledge/`, `.claude/`).
   - **(c)** Dentro de `memory-service-project/Release2.0/` (reemplazar estructura por-rol actual).

2. **¿Arrancamos por Fase 3B** (cosechar los 9 deliveries aprovechando el SPEC v1.9 ya cerrado — trabajo más rápido, alto valor de ordenación) **o por Fase 0** (secuencial SDLC, desde Discovery)?

3. **¿Creamos todos los 391 deliverables como placeholders** (estructura completa, llenar después) **o solo los 4-6 de la fase en la que arrancamos**?

Dame esas 3 respuestas y arranco la ejecución concreta.

 # Paso 4: Definir fase de iniciación (pre-SDLC)
      ↓
      Validé MEM-001..005 y el SETUP_HETZNER. Aquí está la brecha real.

### Estado actual de Phase 1: Project Setup (11h)

| Task | Título actual | Rol | Horas | Cubre coordinación con admin VM? |
|---|---|---|---|---|
| MEM-001 | Infra Setup | DO | 2h | 🟠 **Genérico** — no menciona VM admin, shared-postgres, shared-redis, /storage/ |
| MEM-002 | Repo Structure | PJM | 2h | ✅ Crear repos |
| MEM-003 | Team Onboarding | PJM | 1h | ✅ Onboarding |
| MEM-004 | Tooling Setup | DO | 2h | ⚠️ Genérico (linters/IDE) |
| MEM-005 | Project Kickoff | PM | 4h | ✅ Kickoff |

### Lo que ya está hecho (según PROJECT_MEMORY §8 + SETUP_HETZNER)

| Item | Quién lo hizo | Estado |
|---|---|---|
| BD `memory_service_db` creada en shared-postgres | Admin VM (externa) | ✅ |
| Volumen `/root/memory-service-storage/` creado | Admin VM | ✅ |
| SERVICE_KEY generada | Admin VM | ✅ |
| Redis prefix `mem` definido | Admin VM | ✅ |
| docker-compose.yml base | Admin VM | ✅ |
| Firewall ports 5432/6379 | Admin VM | presumiblemente ✅ |

**Conclusión:** la infra de base está provisionada, pero el proceso **no está formalizado como tarea** en VTT. MEM-001 es una caja negra de 2h que describe "Infra Setup" sin deliverables claros.

### Brecha identificada (lo que falta en las 116 tareas)

**El rol "Admin VM" no existe** en los 12 roles de nuestro equipo (PM, PJM, TL, SA, AR, BE, DB, FE, UX, DL, QA, DO). Es **una persona externa** con la que hay que coordinar. Esto cambia la dinámica:

| Necesidad | ¿Está cubierta en las 116? |
|---|---|
| Protocolo de coordinación con Admin VM (cómo pedir cambios, SLA, handoff format) | 🔴 **No** |
| Documentación de la infra provisionada (qué hay, credenciales, paths, puertos) | 🟠 Solo implícito en SPEC §16 + PROJECT_MEMORY §8 |
| Runbook: solicitar nueva tabla / cambio de config / escalación | 🔴 **No** |
| Runbook: rollback + coordinación cross-service si VM cae | 🟠 MEM-110 (Rollback Plan) lo cubre parcial |
| Verificación post-provisión (DB accesible, Redis responde, /storage/ escribible) | 🔴 **No** |
| Distribución de SERVICE_KEY al equipo (quién lo recibe, cómo se rota) | 🔴 **No** |

### Mi propuesta (para validar contigo antes de ejecutar)

**Expandir Phase 1 con 3-4 tareas nuevas** específicas de coordinación Admin VM, sin romper la numeración existente. Opciones:

#### Opción A — Renombrar MEM-001 + agregar 3 tareas nuevas

| Task | Título propuesto | Rol | Horas | Qué entrega |
|---|---|---|---|---|
| MEM-001 | ~~Infra Setup~~ → **"VM Admin Handoff Protocol"** | DO+PJM | 2h | Protocolo de coordinación con Admin VM (cómo solicitar, cómo escalar, formato de requests) |
| **MEM-001b (nueva)** | **"Shared Infra Provisioning Request"** | DO | 2h | Request formal al Admin VM: crear BD, volumen, SERVICE_KEY, firewall, Redis prefix. Documento de handoff. |
| **MEM-001c (nueva)** | **"Infra Provisioning Verification"** | DO+BE | 2h | Tests de conectividad desde local: `Test-NetConnection` a 5432/6379, conexión a BD, escritura en /storage/ |
| **MEM-001d (nueva)** | **"Infra Config Documentation"** | DO | 1h | `docs/INFRASTRUCTURE_VM.md` — consolidar config final (puertos, URLs, credenciales ubicación, paths, backup schedule) |

**Impacto**: Phase 1 pasa de 11h → 16h (+5h). Total del proyecto 381h → 386h.

#### Opción B — Nueva "Fase 0: Pre-Project Setup" antes de Phase 1

Crear una fase nueva en VTT con 3-4 tareas de coordinación Admin VM. Más limpio conceptualmente pero rompe la numeración/orden VTT existente.

### Antes de ejecutar necesito saber

1. **¿Validas que MEM-001 actual es insuficiente** y quieres formalizarlo?
2. **¿Prefieres Opción A (expandir Phase 1) u Opción B (nueva fase)?**
3. **¿Cómo se llama el Admin VM** y cuál es el canal de coordinación (email, slack, ticket)? Lo necesito para el protocolo.
4. **¿Quieres que también agregue un rol "EXTERNAL_VM_ADMIN"** al equipo en PROJECT_MEMORY §6, o lo dejamos solo como "stakeholder externo"?

Con esas 4 respuestas arranco.


### Pre-handoff de iniciación creado

[PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md](memory-service-project/Release2.0/01-PM/PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md)

### Qué contiene

**24 tareas · 32h** organizadas en 7 categorías:

| Categoría | Tareas | Horas | Cubre |
|---|---:|---:|---|
| **A. VTT Setup** | 5 | 6h | Verificar proyecto/fases/deliveries + PATCH 116 tareas + dependencias |
| **B. Repository Setup** | 5 | 5h | Repo Git, estructura V3.1, branch protection, CODEOWNERS |
| **C. VM Configuration** | 4 | 4h | Verificar infra, conectividad, SERVICE_KEY, documentar |
| **D. Agent Team Setup** | 5 | 8h | 12 OPERATIVOs, CONTEXTOs, accesos, onboarding |
| **E. Tooling Setup** | 3 | 4h | Node/TS, linters, pre-commit, CI mínimo |
| **F. Documentation** | 2 | 2h | README, CONTRIBUTING, ARCHITECTURE |
| **G. Kickoff** | 2 | 3h | Doc kickoff + sync inicial |

### Gap detectado

Las **MEM-001..005 actuales en VTT suman 11h** pero el trabajo real de iniciación es **~32h**. Propongo **Opción A**: mantener los 5 MEM como "umbrella" pero **actualizar horas estimadas** (11h → 32h) vía PATCH, y usar este doc como desglose operativo.

### Estado real detectado (lo que ya está hecho vs pendiente)

**✅ Hecho:**
- Proyecto en VTT + 10 fases + 65 deliveries + 116 tareas creadas
- Infraestructura VM provisionada (BD, volumen, SERVICE_KEY, Redis)
- `PROJECT_MEMORY.md`, `OPERATIVO_PM_MEMORY-SERVICE.md`, `OPERATIVO_TECH_LEAD.md`

**🟡 Pendiente:**
- PATCH de 116 tareas con assignees y metadata
- Dependencias en VTT (15 críticas)
- Crear 10 OPERATIVOs faltantes (PJM, SA, AR, BE, DB, FE, UX, DL, QA, DO)
- Repo Git estructura V3.1
- Tooling (eslint, prettier, husky, CI)
- Documentación (README, CONTRIBUTING, ARCHITECTURE, KICKOFF)

**🔴 Bloqueado:**
- Repo Git (remoto actual apunta a `twitter-react` — incorrecto; requiere decisión multi-repo del PM)
- Endpoint VTT de dependencias (HO v2.1 §10)

Listo para tu siguiente paso.
 # Paso 5: Consolidar plan maestro
      ↓
      ### Consolidado creado

[CONSOLIDADO_MEMORY_SERVICE_R1.md](memory-service-project/Release2.0/01-PM/CONSOLIDADO_MEMORY_SERVICE_R1.md)

### Estructura siguiendo tu orden

**§1 Jerarquía y contexto** (Modelo Dinámico V3 + stack + totales)

**§2 FASE DE INICIACIÓN (pre-SDLC)** ← al principio como pediste
- 24 tareas · 32h · 7 categorías (A-G)
- Mapeo explícito de INIT-* a MEM-001..005 actuales (11h → 32h)

**§3 FASES SDLC APLICABLES** ← después como pediste
- **§3.1 a §3.5 (Fases 0, 1, 2, 3A, 3B):** deliverables preservados + tareas VTT asociadas
- **§3.6 a §3.9 (Fases 4, 5, 6, 7):** **deliverables REEMPLAZADOS por tareas del pre-handoff de implementación** como pediste

### Análisis de mapeo pre-handoff IMPL → fases

| Fase SDLC | Deliverables (reemplazados) | Tareas que los reemplazan |
|---|---:|---|
| **Fase 4 Development** | 75 | 46 tareas MEM-048..093 (S01..S06 + UI-01..04) |
| **Fase 5 Testing** | 51 | 10 tareas MEM-094..103 |
| **Fase 6 Deploy** | 38 | 7 tareas MEM-104..110 |
| **Fase 7 Operations** | 23 | 6 tareas MEM-111..116 |

§3.6.8 tiene el mapeo inverso: cada subfase SDLC (4.1 Environment Setup, 4.2 DB Implementation, etc.) indica qué tareas la cubren.

### Totales maestros

| Bloque | Tareas | Horas |
|---|---:|---:|
| Iniciación | 24 | 32h |
| Fase 0 (Discovery) | 4 | 9h |
| Fase 1 (Planning) | 8 | 23h |
| Fase 2 (Analysis) | 8 | 41h |
| Fase 3A (Design UX/UI) | 13 | 35h |
| Fase 3B (Design Technical) | 9 | 45h |
| Fase 4 (Development) | 46 | 116h |
| Fase 5 (Testing) | 10 | 60h |
| Fase 6 (Deploy) | 7 | 26h |
| Fase 7 (Operations) | 6 | 15h |
| **TOTAL** | **135** | **402h** |

> 116 tareas VTT oficiales + 24 INIT (desglose de MEM-001..005 pasando de 11h → 32h).

Listo para tu siguiente paso.
 # Paso 6: Generar Cierre PM + Handoff operativo
      ↓
      ### HO formal emitido

[CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md](memory-service-project/Release2.0/01-PM/CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md)

### Sigue el formato V4.2 exacto

**PARTE I — CIERRE PM DEL ANÁLISIS (§1-§6):**
1. Documentos consumidos (14)
2. Decisiones PM finales (48 FROZEN)
3. Correcciones incorporadas (24)
4. Limitaciones R1 (10)
5. Reassignments (2)
6. Veredicto PM (caja ASCII)

**PARTE II — HANDOFF OPERATIVO (§7-§17):**
7. Alcance final R1 (19 tablas, 11 endpoints, 9 UIs, infra, integraciones)
8. **Fase de Iniciación (pre-SDLC)** — 24 tareas · 32h ← nuevo, no estaba en V4.2
9. Secuencia de fases (caja ASCII con 6 fases A..F)
10. **Plan completo con mapeo explícito tarea→deliverables** ← la columna "Produce" está en TODAS las tablas de las 9 fases
11. Dependencias por rol (7 roles)
12. Dependencias críticas (15)
13. Riesgos R1-R12
14. Checklist PJM (5 bloques)
15. Criterio de éxito (20 items verificables)
16. BRIEFs downstream (22 por rol/sprint)
17. Firmas (12 roles, PM aprobado)

### Lección aprendida aplicada

Como me advertiste: **una tarea cubre varios deliverables**, pero el mapeo debe ser explícito para no repetir el análisis. Resolví esto con la columna **"Produce"** en CADA tabla de tareas de TODAS las fases (incluyendo las 33 de Planning, las 47 de Analysis, las 40 de Design UX/UI, etc.).

Cada fila dice literalmente "MEM-XXX produce 0.Y.Z, 0.Y.W, ..." — sin ambigüedad.

### Totales formales firmados

```
135 tareas · 405h · 10 fases SDLC + iniciación
  (116 tareas VTT + 24 INIT como desglose operativo)
```

Listo para siguiente paso.
 # Paso 7: Generar Task Index Seed (metadata + UUIDs)
      ↓
      ## TASK_INDEX_SEED regenerado a v2.0

[TASK_INDEX_SEED_MEMORY_SERVICE.md](memory-service-project/Release2.0/01-PM/TASK_INDEX_SEED_MEMORY_SERVICE.md)

### Cambios clave vs v1.0

| Cambio | v1.0 (obsoleta) | v2.0 (nueva) |
|---|---|---|
| **Estado VTT** | Asumía proyecto existente + UUIDs stale | 🆕 Nada existe, todo se crea |
| **Scripts** | PATCH a tareas existentes | POST para crear (6 pasos secuenciales) |
| **Wizard** | No usado | Explícitamente NO usado — POST simple |
| **User UUIDs** | 12 agentes con UUIDs inventados | 🆕 **UUIDs reales de PROCESO_ASIGNACION v1.6** |
| **Priority UUIDs** | Solo medium/high | 🆕 Los 4: critical, high, medium, low |
| **Fuente de endpoints** | Improvisada | 🆕 Documento PROCESO_ASIGNACION_TAREAS.md v1.6 |

### Mapeo real roles Memory Service → usuarios VTT

| Memory Service | Usuario VTT real | UUID |
|---|---|---|
| PM | Martin Rivas | `07a07147-...` |
| PJM | Project Manager | `49937318-...` |
| TL | Claude (Tech Lead) | `abdff0db-...` |
| SA | Systems Analyst | `becdf45a-...` |
| AR ⚠️ | Systems Analyst (fallback — no hay Architect en VTT) | `becdf45a-...` |
| BE | Backend API Specialist | `8834830b-...` |
| DB | Database Engineer | `a3a2ce62-...` |
| FE | Frontend Dev #1 | `84ad0fbe-...` |
| UX | UX Designer | `ce8a2ace-...` |
| DL | Design Lead | `ebf0f384-...` |
| QA | QA Engineer | `1d8eb958-...` |
| DO | DevOps Engineer | `b2e00b9d-...` |

> ⚠️ **AR flag:** No existe rol "Architect" en VTT. Fallback a Systems Analyst. Si prefieres otro (Integration Reviewer `fbef6ae6-...` o Integration Auditor `f294a61d-...`), lo ajusto.

### Los 6 pasos de creación

| Paso | Endpoint | Captura |
|---|---|---|
| 1 | `POST /api/projects` (simple, sin wizard) | `projectId` |
| 2 | `POST /api/projects/:id/phases` × 10 | 10 `phaseId` |
| 3 | `POST /api/deliveries` × 65 | 65 `deliveryId` |
| 4 | `POST /api/phases/{phaseId}/tasks` × 116 | 116 `taskId` |
| 5 | `POST /api/deliveries/{deliveryId}/tasks/{taskId}` × 116 | — |
| 6 | `POST /api/tasks/{id}/dependencies` × 15 | — |

Todo se guarda en `VTT_UUIDS_MEMORY_SERVICE.json` al final.

### Pendiente antes de ejecutar

1. **AR role** — decide si SA fallback está bien, o cambiar a otro usuario VTT
2. **Descripciones §4** — las 116 descripciones breves están, las largas están en CONSOLIDADO
3. **Script completo** — el §7 muestra el patrón Python; para 116 tareas hay que expandir las tuplas

¿Quieres que genere el **script Python completo** (con las 116 tuplas de TASKS y las 65 DELIVERIES expandidas) como archivo `.py` ejecutable separado, o sigues con otro paso?
 # Paso 8: Generar script ejecutable de carga
      ↓
      ### Ambos entregables listos

**1. Script Python ejecutable**

[create_memory_service_vtt.py](memory-service-project/Release2.0/scripts/create_memory_service_vtt.py)

- **~550 líneas** con los 116 tasks + 65 deliveries + 15 dependencies expandidos en tuplas Python.
- Usa los UUIDs reales de `Proyect_data.md` (12 roles + Solution Analyst + Architect).
- 6 pasos secuenciales con logging timestamped.
- Genera `VTT_UUIDS_MEMORY_SERVICE.json` al final.
- Manejo robusto: auth fail aborta; errores en dependencias/asignaciones solo warn (para poder continuar).

**2. HO formal PM → PJM**

[HO_PJM_CARGA_VTT_MEMORY_SERVICE.md](memory-service-project/Release2.0/01-PM/HO_PJM_CARGA_VTT_MEMORY_SERVICE.md)

11 secciones siguiendo el formato V4.2:

| §  | Contenido |
|----|-----------|
| 1 | Objetivo |
| 2 | Contexto + docs PM cerrados (7) |
| 3 | Entregable adjunto (el script) |
| 4 | Prerrequisitos (checklist + config entorno) |
| 5 | Proceso de ejecución + salida esperada |
| 6 | Verificación post-ejecución (checks automáticos + checklist manual + rollback) |
| 7 | Acciones post-carga |
| 8 | Escalación |
| 9 | Criterio de éxito |
| 10 | Firmas (PM ✅, 3 pendientes) |
| 11 | Referencias |

### Flujo operativo que habilita el HO

```
PJM ejecuta script
       │
       ▼
1 Project + 10 Phases + 65 Deliveries + 116 Tasks + 15 Deps creados en VTT
       │
       ▼
VTT_UUIDS_MEMORY_SERVICE.json capturado
       │
       ▼
PJM notifica al PM con log + JSON
       │
       ▼
PM hace sign-off del HO y emite HO_FASE_0_DISCOVERY
       │
       ▼
Kickoff operativo del proyecto
```

### Próximo paso lógico

Una vez PJM ejecute el script exitosamente, el siguiente artefacto a generar sería el **primer HO por fase: `HO_FASE_0_DISCOVERY_MEMORY_SERVICE.md`** (el más pequeño: 4 tareas, 9h, 10 deliverables).

¿Sigo con ese, o prefieres esperar a que el PJM ejecute primero?
 # Paso 9: Generar HO de ejecución para PJM
      ↓
  [FIN: PJM ejecuta · PM firma sign-off]