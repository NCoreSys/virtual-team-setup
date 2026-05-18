# Kickoff — Memory Service R1

**Fecha**: 2026-05-04
**Versión**: 1.0
**Estado**: Activo
**Firmado por**: Memory Service PM — Product Manager

---

## 1. Visión del Producto

Memory Service es un sistema independiente de memoria centralizada para agentes de IA. Persiste conversaciones provenientes de 5 fuentes (CLI, Web, SDK, ChatGPT, VTT_CHANNEL), las clasifica automáticamente mediante reglas determinísticas, calcula costos de tokens, y entrega contexto estructurado en menos de 500ms al runtime de agentes.

**Problema que resuelve:** Los agentes de IA no tienen memoria persistente entre sesiones. Cada conversación se pierde al terminar, lo que impide que los agentes mejoren con el tiempo, recuerden contexto previo, o sean auditados. Memory Service centraliza toda la memoria de los agentes en un único sistema consultable.

**Propuesta de valor:** Un microservicio standalone, reutilizable y resiliente que permite a cualquier agente acceder a su historial, timeline de actividad, reporte de costos y contexto relevante — todo en una sola API, en tiempo real, sin convertirse en un cuello de botella.

---

## 2. Objetivos de Release 1 (R1)

1. **Importar conversaciones** desde 5 fuentes (CLI, Web, SDK, ChatGPT, VTT_CHANNEL) via endpoints REST
2. **Clasificar automáticamente** cada conversación por tipo (TASK_EXECUTION, AGENT_REVIEW, AGENT_CLARIFICATION) usando reglas determinísticas
3. **Proveer contexto runtime** en <500ms (síncrono, fail-fast) para el Runtime v1.1
4. **Exponer timeline** de actividad por agente (`GET /agents/:id/timeline`)
5. **Calcular y reportar costos** de tokens por agente y por proyecto
6. **UI Standalone** en puerto 3003 para visualización de conversaciones, timeline y costos
7. **Integrar** con Runtime v1.1, Prompt Builder v1.3 y Hook Manager VTT

**Fecha objetivo R1**: TBD — se definirá en fase Discovery (MS-142 Kickoff Call es el gate de inicio)

---

## 3. Alcance R1

### IN SCOPE

- `POST /import` — Importación batch JSONL desde CLI/Web/SDK/ChatGPT
- `POST /import-review` — Importación incremental desde VTT_CHANNEL
- `POST /upload` — Subida manual de archivos de conversación
- `GET /agents/:id/timeline` — Timeline de actividad por agente
- `GET /conversations/:id/content` — Lectura de contenido desde storage
- `GET /context` — Contexto runtime <500ms (síncrono, fail-fast)
- `GET /projects/:id/cost-report` — Reporte de costos por proyecto
- `GET /agents/:id/cost-report` — Reporte de costos por agente
- `GET /conversations` — Lista con filtros para UI
- `GET /dashboard/stats` — Estadísticas globales
- `GET /health` — Health check
- Clasificación determinística por reglas (sin ML)
- Cleanup job automático cada 5 minutos (recovery de estados PENDING/PROCESSING colgados)
- Cache de catálogos en startup
- UI Standalone (React + Vite + Tailwind) en puerto 3003
- Infraestructura: Node.js 20 + TypeScript + Express + Prisma + PostgreSQL + Redis

### OUT OF SCOPE (R2+)

- Almacenamiento en MinIO (R1 usa bind mount en filesystem de VM)
- Machine Learning para clasificación
- Multi-tenancy
- Exportación a servicios externos (Google Drive, etc.)
- Búsqueda semántica / embeddings
- Autenticación JWT para usuarios finales (R1 solo SERVICE_KEY)
- Dashboard de administración avanzado
- Webhooks para notificaciones en tiempo real

---

## 4. Equipo

| Rol | Agente | UUID VTT | Email |
|-----|--------|----------|-------|
| PM | Memory Service PM | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` | `pm@memory-service.vtt.ai` |
| Tech Lead | Memory Service TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` | `memory-service.tl@vtt.ai` |
| Backend Engineer | Memory Service BE | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | `memory-service.be@vtt.ai` |
| Database Engineer | Memory Service DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | `memory-service.db@vtt.ai` |
| Frontend Developer | Memory Service FE | `d23c9cd9-a156-433b-8900-94add5488eec` | `memory-service.fe@vtt.ai` |
| QA Engineer | Memory Service QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | `memory-service.qa@vtt.ai` |
| DevOps Engineer | Memory Service DO | `322e3745-9756-4a7c-af11-44b33edef44d` | `memory-service.devops@vtt.ai` |
| Design Lead | Memory Service DL | `b3a09269-cded-468c-a475-15a48f203cb0` | `memory-service.dl@vtt.ai` |
| Architect | Memory Service AR | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | `ar@memory-service.vtt.ai` |
| Solution Analyst | Memory Service SA | `0c128e3b-db3b-4e31-b107-0379b5791233` | `sa@memory-service.vtt.ai` |

---

## 5. Roadmap por Fase

| Fase | Nombre | Inicio | Fin | Estado |
|------|--------|--------|-----|--------|
| Phase 1 | Project Setup (INIT) | 2026-04-22 | 2026-05-04 | 🔵 En progreso |
| Phase 2 | Discovery | TBD* | TBD | ⏳ Pendiente |
| Phase 3 | Planning | TBD | TBD | ⏳ Pendiente |
| Phase 4 | Analysis | TBD | TBD | ⏳ Pendiente |
| Phase 5 | Design (UX/UI + Técnico) | TBD | TBD | ⏳ Pendiente |
| Phase 6 | Development | TBD | TBD | ⏳ Pendiente |
| Phase 7 | Testing | TBD | TBD | ⏳ Pendiente |
| Phase 8 | Deploy | TBD | TBD | ⏳ Pendiente |
| Phase 9 | Operations | TBD | TBD | ⏳ Pendiente |

> *Las fechas de Discovery en adelante se definirán en el Kickoff Call (MS-142), que es el GATE de inicio de Fase 2.

---

## 6. Riesgos Identificados

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|---|--------|-------------|---------|------------|
| R1 | **Latencia GET /context >500ms** bajo carga: la VM compartida tiene límite de 512MB RAM y 20 conexiones PostgreSQL | Alta | Alto | Cache de catálogos en startup; fail-fast implementado; connection_limit=20 en docker-compose; índice GIN en platformRefs |
| R2 | **Filesystem storage se llena**: R1 usa bind mount en `/root/memory-service-storage/` sin cuota ni compresión | Media | Alto | Cleanup job cada 5min; migración a MinIO planificada para R2; monitoreo de disco en VM |
| R3 | **Integración VTT_CHANNEL falla silenciosamente**: import incremental de VTT_CHANNEL es append-only, errores de red pueden dejar conversaciones en estado PROCESSING | Media | Medio | Recovery automático del cleanup job (PENDING/PROCESSING >10min → retry o ERROR); logs explícitos de cada transición |
| R4 | **Conflictos de idempotencia**: múltiples imports concurrentes del mismo `sourceId + externalSessionId` pueden generar race conditions | Baja | Medio | Constraint único compuesto en BD; manejo explícito de error P2002 en handlers |
| R5 | **Scope creep en Discovery**: la SPEC v1.9 es extensa; el equipo puede intentar incluir features de R2 en R1 | Media | Medio | Alcance IN/OUT definido en este documento; SA revisa cada tarea de Discovery contra este alcance |

---

## 7. Criterios de Éxito R1

- [ ] `GET /health` responde 200 en producción (VM Hetzner)
- [ ] `GET /context` responde en <500ms con carga de 10 conversaciones concurrentes
- [ ] Importación exitosa desde las 5 fuentes (CLI, Web, SDK, ChatGPT, VTT_CHANNEL)
- [ ] UI Standalone accesible en puerto 3003 con Dashboard, Timeline y Cost Report funcionando
- [ ] Cleanup job ejecutándose cada 5 minutos sin errores en 24h continuas
- [ ] 0 conversaciones en estado PROCESSING por más de 15 minutos en producción
- [ ] Reporte de costos por agente y proyecto con datos reales de al menos 1 semana de uso
- [ ] Integración validada con Runtime v1.1 (contexto entregado correctamente en sesión real)

---

## 8. Firma

**Firmado por**: Memory Service PM
**Fecha**: 2026-05-04
**Versión**: 1.0

---

*Este documento es el punto de partida formal del proyecto Memory Service R1. Cualquier cambio de alcance posterior debe ser aprobado por el PM y registrado como addendum a este documento.*
