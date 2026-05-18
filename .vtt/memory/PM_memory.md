# Memoria del Agente PM — Memory Service

> Capa 2 de memoria: registro histórico del rol PM en este proyecto.
> Cada entrada captura qué se hizo, qué se decidió, y qué aprendió el PM.
> Cualquier agente que tome el rol PM en una sesión futura lee esto primero.

---

## Template de entrada (copiar para cada sesión/tarea)

```markdown
## YYYY-MM-DD — [TASK_ID o descripción de la sesión]

**Tarea/Actividad:** [qué se hizo]
**Estado resultante:** [APPROVED / COMPLETO / EN_PROGRESO / BLOQUEADO]

### Qué se produjo
- [archivo/entregable 1]
- [archivo/entregable 2]

### Decisiones tomadas
- [decisión + razón]

### Lecciones / alertas para próxima sesión
- [algo que no salió bien o que hay que recordar]

### Próximo paso
- [qué sigue]
```

---

## Historial

### 2026-04-23 — Sesión de cierre PM (análisis + consolidación)

**Actividad:** Proceso completo de cierre PM — SPEC, filtro fases, PRE_HANDOFFs, CONSOLIDADO, HO PJM
**Estado resultante:** COMPLETO — HO firmado, listo para PJM

#### Qué se produjo
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — SPEC cerrada, ADDENDUM v1.1 integrado
- `FASES_APLICABLES_MEMORY_SERVICE.md` v2.0 — 390/438 aplican
- `PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md` — 24 sub-tareas en 7 categorías (A-G)
- `PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md` — 66 tareas de código
- `CONSOLIDADO_MEMORY_SERVICE_R1.md` — plan maestro
- `CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md` — HO formal a PJM

#### Decisiones tomadas
- SPEC v1.9 cerrada como APPROVED PM — no acepta más cambios sin ADR
- Fase de Iniciación separada de Implementación (2 PRE_HANDOFFs distintos)
- ADDENDUM v1.1 integrado directamente a SPEC (no vive separado)

#### Lecciones / alertas
- El proceso PM original no tenía PASO 0 (ADR repos) — se generó estructura monorepo que luego se invalidó
- Siempre pedir ADR de repos antes de generar cualquier documento con rutas físicas
- Los UUIDs de usuarios son ESPECÍFICOS del proyecto — no reutilizar de otros proyectos

#### Próximo paso
- PJM ejecuta carga en VTT con el script Python

---

### 2026-04-24 — TASK_INDEX_SEED + Script Python

**Actividad:** Generar seed completo con 116 tareas y script de carga VTT
**Estado resultante:** COMPLETO

#### Qué se produjo
- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — 116 tareas con UUIDs correctos
- `create_memory_service_vtt.py` — script Python listo para ejecutar

#### Decisiones tomadas
- 65 deliveries agrupando los 390 deliverables aplicables
- 15 dependencias críticas documentadas (camino crítico)
- UUIDs obtenidos de `Proyect_data.md` (no de proceso genérico)

#### Lecciones / alertas
- Primera versión del seed tenía UUIDs incorrectos (de VTT genérico, no de Memory Service)
- `Proyect_data.md` en `.claude/rules/` es la fuente de verdad de UUIDs — siempre leer primero
- VTT fue limpiado completamente entre sesiones — el script debe crear todo desde cero con POST

#### Próximo paso
- PJM ejecuta `create_memory_service_vtt.py` contra `http://77.42.88.106:3000`

---

### 2026-04-23 — ADR-001 + Estructura multi-repo

**Actividad:** Regenerar estructura de repos después de ADR-001 aprobado (4 repos)
**Estado resultante:** COMPLETO

#### Qué se produjo
- `ADR-001_estrategia_repositorios.md` — (creado externamente por PM, integrado aquí)
- `ESTRUCTURA_REPO_MEMORY_SERVICE.md` v2.0 — blueprint 4 repos
- `WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md` — cómo trabajan los agentes
- 9 archivos `.code-workspace` — uno por rol
- `ADDON_PASO0_ADR_REPOS_LECCION_APRENDIDA.md` — lección documentada

#### Decisiones tomadas
- 4 repos: `memory-service-project`, `memory-service-api`, `memory-service-backend`, `memory-service-frontend`
- Devlogs SIEMPRE en `memory-service-project/devlogs/` — nunca distribuidos
- Code-logic vive en el repo del código, no en project

#### Lecciones / alertas
- La ESTRUCTURA_REPO v1.0 se invalidó porque asumía monorepo
- PASO 0 es OBLIGATORIO: ADR de repos antes de cualquier documento con rutas físicas
- Este error costó regenerar 3 documentos

---

### 2026-04-27 — Setup .vtt/ simulado

**Actividad:** Crear estructura `.vtt/` como simulación del Daemon VTT en el repo local
**Estado resultante:** COMPLETO (estructura creada, contenido parcial)

#### Qué se produjo
- `.vtt/manifest.yaml` — mapa de sync completo con sync_map y teams
- `.vtt/teams.md` — composición de 3 equipos (BE, FE, Testing/QA)
- `.vtt/memory/project_index.md` — índice vivo del proyecto
- `.vtt/memory/PM_memory.md` — este archivo
- `.vtt/skills/` — 6 skills: filtrar-fases, generar-seed, analizar-spec, iniciar-tarea, entregar-tarea, verificar-sprint

#### Decisiones tomadas
- 3 equipos operativos: BE (backend+DB+DO), FE (frontend+DL+UX), Testing/QA (acceso todos los repos)
- QA tiene write en backend y frontend (solo `tests/`) — necesario para crear archivos de test
- `.vtt/` simula lo que el Daemon sincronizaría desde VTT backend central
- `manifest.yaml` define el contrato de sync: sync_mode pull_only / push_pull / read_only

#### Próximo paso
- Definir template de memoria para otros roles (TL, BE, QA)
- Reorganizar workspaces (`.code-workspace`) a `.vtt/workspaces/`
- Agregar `00-agent-setup/` al mapa de sync del manifest
