# Architecture — Memory Service R1

**Versión**: 1.0
**Fecha**: 2026-05-04
**Fuente de verdad completa**: [SPEC v1.9](../memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md)

---

## 1. Visión General

Memory Service es un sistema independiente de memoria centralizada para agentes de IA. Importa conversaciones de 5 fuentes (CLI, Web, SDK, ChatGPT, VTT_CHANNEL), las clasifica automáticamente por reglas determinísticas, y provee contexto runtime en <500ms para que los agentes recuperen su historial antes de ejecutar tareas. Corre en infraestructura compartida Hetzner como servicio Docker autónomo.

---

## 2. Componentes Principales

```
┌─────────────────────────────────────────────────────────────────┐
│                        Memory Service                           │
│                                                                 │
│  ┌──────────────┐    ┌─────────────────────────────────────┐   │
│  │   API REST   │    │           Core Engine               │   │
│  │  Express     │───▶│  Importers · Classifier · Cleanup   │   │
│  │  Port 3002   │    │  Context Service · Catalog Cache    │   │
│  └──────────────┘    └──────────────────┬────────────────--┘   │
│                                         │                       │
│              ┌──────────────────────────┼─────────────────┐    │
│              │                          │                  │    │
│  ┌───────────▼───────┐    ┌─────────────▼──────┐  ┌──────▼──┐ │
│  │  PostgreSQL        │    │  Redis (prefix:mem) │  │ Storage │ │
│  │  memory_service_db │    │  shared-redis       │  │ /storage│ │
│  └───────────────────┘    └────────────────────┘  └─────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │   UI Standalone (SPA)   Port 3003                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Red Docker: shared-network                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Sub-componentes del Core Engine

| Componente | Responsabilidad |
|------------|----------------|
| Importers (5 adapters) | CLI · Web · SDK · ChatGPT · VTT_CHANNEL |
| Classifier Service | Reglas determinísticas, sin ML |
| Context Service | GET /context síncrono <500ms, fail-fast (D-MEM-07) |
| Cleanup Job | Cron cada 5 min: PENDING/PROCESSING > 10 min → retry o ERROR |
| Catalog Cache | Catálogos en memoria al startup; evita N+1 en /context |
| Storage Service | Bind mount `/root/memory-service-storage/` → `/storage/` |

---

## 3. Stack Tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Runtime | Node.js | 20.x |
| Lenguaje | TypeScript | latest |
| Framework | Express | latest |
| ORM | Prisma | latest |
| Base de datos | PostgreSQL | shared-postgres (`memory_service_db`) |
| Cache / Rate Limit | Redis | shared-redis (prefix `mem`) |
| Storage | Volumen Docker bind mount | `/root/memory-service-storage/` |
| Containerización | Docker | — |
| Puerto API | 3002 | — |
| Puerto UI | 3003 | — |
| Red | Docker shared-network | — |
| Path VM | `/root/memory-service/` | Hetzner |

---

## 4. Repositorios del Proyecto

| Repo | Propósito |
|------|-----------|
| `NCoreSys/memory-service-project` | Documentación central, specs, assignments, onboarding |
| `NCoreSys/memory-service-backend` | API REST + Core Engine (Express + Prisma) |
| `NCoreSys/memory-service-frontend` | UI Standalone SPA (Puerto 3003) |

---

## 5. Flujo Principal de Importación

```
1. Cliente → POST /import (JSONL) o POST /import-review (VTT_CHANNEL)
             o POST /upload (archivo manual)
2. API → Adapter correspondiente parsea el payload
3. Conversation se crea en estado PENDING → PROCESSING
4. Classifier Service aplica reglas determinísticas (conversationType, workType)
5. Archivo completo escrito en /storage/{agentId}/{YYYY-MM}/{sessionId}/
6. Estado → IMPORTED  (o ERROR con cleanup job para recovery)
7. Catalog Cache precargado evita N+1 en queries del contexto
```

---

## 6. Flujo de Contexto Runtime

```
Agente → GET /context?projectId=X&taskId=Y
         ↓  (< 500ms SLA — fail-fast, síncrono)
Context Service → Query PostgreSQL (filtrado por projectId)
                → Retorna conversaciones relevantes + metadata
                → contentPreview en BD (500 chars)
                → contenido completo en GET /conversations/:id/content (lee /storage/)
```

---

## 7. Decisiones Clave (no reabrir)

| ID | Decisión |
|----|---------|
| D-MEM-01 | Sistema independiente (no acoplado a VTT) |
| D-MEM-07 | GET /context síncrono <500ms, fail-fast — no negociable |
| D-MEM-08 | Clasificación por reglas determinísticas (no ML) |
| D-MEM-43 | `contentPreview` en BD solo 500 chars; contenido completo en /storage/ |
| D-MEM-26 | Auth service-to-service via SERVICE_KEY (patrón VTT) |

---

## 8. Documentación Completa

Ver [SPEC Memory Service v1.9](../memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md) para:
- Contrato técnico completo (43 decisiones cerradas D-MEM-01..43)
- Endpoints y modelos de datos (§4, §8)
- Catálogos y seed data (§5)
- Índices de base de datos (§6)
- Reglas de clasificación (§12)
- Docker-Compose producción (§16)
- Plan de implementación activo: `HO_ACTUALIZAR_TAREAS_VTT.md v2.1` — 116 tareas, 381h
