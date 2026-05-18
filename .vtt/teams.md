# Composición de Equipos — Memory Service

| Campo | Valor |
|-------|-------|
| **Proyecto** | Memory Service R1 |
| **Estrategia repos** | ADR-001 — 4 repos (project, api, backend, frontend) |
| **Fecha** | 2026-04-27 |

---

## Modelo de 3 equipos operativos

```
┌─────────────────────────────────────────────────────────┐
│                memory-service-project                    │
│           (TODOS tienen acceso — devlogs, docs)          │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐
│  Equipo BE   │  │  Equipo FE   │  │  Equipo Testing/QA   │
│              │  │              │  │  /Integraciones       │
│ memory-      │  │ memory-      │  │  memory-service-      │
│ service-     │  │ service-     │  │  backend (tests/)     │
│ backend      │  │ frontend     │  │  memory-service-      │
│ (write)      │  │ (write)      │  │  frontend (tests/)    │
│              │  │              │  │  memory-service-api   │
│ + api (read) │  │ + api (read) │  │  (read — contratos)   │
└──────────────┘  └──────────────┘  └──────────────────────┘
```

---

## Equipo BE — Backend

**Repos:**
| Repo | Acceso | Scope |
|------|--------|-------|
| `memory-service-backend` | Write | Todo |
| `memory-service-api` | Read | Contratos de API |
| `memory-service-project` | Write | Solo `devlogs/` |

**Roles:**
| Rol | Responsabilidad en este equipo |
|-----|-------------------------------|
| BE (Backend Engineer) | Implementación de endpoints, lógica de negocio |
| DB (Database Engineer) | Schema Prisma, migraciones, queries |
| DO (DevOps) | `infra/`, `.github/workflows/`, Docker en BE |
| TL (Tech Lead) | Revisión de PRs, decisiones técnicas BE |

**Workspace:** `be.code-workspace` — abre `memory-service-backend` + `memory-service-project`

---

## Equipo FE — Frontend

**Repos:**
| Repo | Acceso | Scope |
|------|--------|-------|
| `memory-service-frontend` | Write | Todo |
| `memory-service-api` | Read | Contratos de API |
| `memory-service-project` | Write | Solo `devlogs/` |

**Roles:**
| Rol | Responsabilidad en este equipo |
|-----|-------------------------------|
| FE (Frontend Developer) | Implementación React/Vite/TailwindCSS |
| DL (Design Lead) | Revisión visual, design tokens, componentes |
| UX (UX Designer) | Flujos de usuario, especificaciones |
| TL (Tech Lead) | Revisión de PRs, decisiones técnicas FE |

**Workspace:** `fe.code-workspace` — abre `memory-service-frontend` + `memory-service-project`

---

## Equipo Testing / QA / Integraciones

**Repos:**
| Repo | Acceso | Scope |
|------|--------|-------|
| `memory-service-backend` | Write | Solo `tests/` |
| `memory-service-frontend` | Write | Solo `tests/` |
| `memory-service-api` | Read | Contratos para validar |
| `memory-service-project` | Write | Solo `devlogs/` |

**Por qué write en ambos repos de código:** el QA necesita crear y mantener archivos de test (`*.spec.ts`, `*.test.ts`, fixtures, mocks de contrato) directamente en los repos donde vive el código que prueba. No puede hacer su trabajo solo con read-only.

**Roles:**
| Rol | Responsabilidad en este equipo |
|-----|-------------------------------|
| QA (Quality Assurance) | Tests unitarios, integración, E2E, contratos |

**Workspace:** `qa.code-workspace` — abre `memory-service-backend` + `memory-service-frontend` + `memory-service-project`

> **Nota:** El QA es el único rol que abre 3 repos al mismo tiempo. Esto es intencional — su trabajo requiere ver backend y frontend simultáneamente para testing de integración.

---

## Roles transversales (no son equipo de código)

| Rol | Repos | Acceso |
|-----|-------|--------|
| PM | `memory-service-project`, `memory-service-api` | Write ambos |
| PJM | `memory-service-project` | Write |
| AR (Architect) | `memory-service-api` (write), todos (read) | Dueño del contrato API |
| SA (Solution Analyst) | `memory-service-project` (write), todos (read) | Análisis cross-repo |
| Analyst (SA/AR/UX/DL) | `memory-service-project` | Write solo docs |

**Workspace:** `analyst.code-workspace`, `pm.code-workspace`, `pjm.code-workspace`

---

## Fine-grained PATs requeridos

| Equipo/Rol | Token scope |
|-----------|-------------|
| BE | `memory-service-backend` write + `memory-service-api` read |
| FE | `memory-service-frontend` write + `memory-service-api` read |
| QA | `memory-service-backend` write (tests/) + `memory-service-frontend` write (tests/) + `memory-service-api` read |
| DO | `memory-service-backend` write (infra/) + `memory-service-frontend` write (.github/) |
| AR | `memory-service-api` write |
| PM/PJM/SA | `memory-service-project` write |
| TL | Todos los repos read + `memory-service-project` write |

> Implementación de PATs: tarea INIT-E-01 (asignada a DO). Ver ADR-001.
