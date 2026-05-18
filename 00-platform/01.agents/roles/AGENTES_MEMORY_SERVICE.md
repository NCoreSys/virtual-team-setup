# Agentes — memory-service

**Fecha:** 2026-04-22
**Proyecto:** memory-service
**Dominio email:** `@memory-service.vtt.ai`
**Password (todos):** `VttAgent2026`
**Platform Role:** `platform_super_admin` (bypass todos los permission checks)
**Auth:** `POST /api/auth/service-token` con `{ userId, serviceKey }` o login con email/password

---

## 1. Equipo Core Tecnico (8)

| Code | Rol | Email | UUID | Descripcion |
|------|-----|-------|------|-------------|
| TL | Tech Lead | `tl@memory-service.vtt.ai` | `92225290-6b6b-4c1f-a940-dcb4262507aa` | Liderazgo tecnico, arquitectura, revision de codigo |
| BE | Backend Engineer | `backend@memory-service.vtt.ai` | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | Node.js + Express + Prisma, APIs, integracion |
| DB | Database Engineer | `database@memory-service.vtt.ai` | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | PostgreSQL, Prisma schema, migraciones, queries |
| FE | Frontend Developer | `frontend@memory-service.vtt.ai` | `d23c9cd9-a156-433b-8900-94add5488eec` | React + TypeScript + Vite + TailwindCSS |
| QAE | QA Engineer | `qae@memory-service.vtt.ai` | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | Test cases, manual testing, bug reporting |
| DO | DevOps Engineer | `devops@memory-service.vtt.ai` | `322e3745-9756-4a7c-af11-44b33edef44d` | Docker, CI/CD, migraciones prod, infraestructura |
| DL | Design Lead | `design-lead@memory-service.vtt.ai` | `b3a09269-cded-468c-a475-15a48f203cb0` | Design system, tokens, review de HTML, specs UX |
| UX | UX Designer | `ux@memory-service.vtt.ai` | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` | Wireframes, mockups HTML, flujos de usuario |

---

## 2. Equipo de Gestion (4)

| Code | Rol | Email | UUID | Descripcion |
|------|-----|-------|------|-------------|
| PM | Project Manager | `pm@memory-service.vtt.ai` | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` | Coordinacion proyecto, aprobaciones, roadmap |
| PJM | Project Manager (PJM) | `pjm@memory-service.vtt.ai` | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` | Sprints, desviaciones, reporte al PM |
| SA | Solution Analyst (Systems Analyst) | `sa@memory-service.vtt.ai` | `0c128e3b-db3b-4e31-b107-0379b5791233` | Analisis funcional, requerimientos, specs |
| AR | Auditor Reviewer (Architect) | `ar@memory-service.vtt.ai` | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | Arquitectura, revision de disenos, compliance |

---

## 3. Equipo Discovery & Planning / Analysis (4)

| Code | Rol | Email | UUID | Descripcion |
|------|-----|-------|------|-------------|
| PSA | Product Strategy Analyst | `psa@memory-service.vtt.ai` | `a43f6bd0-3452-46ea-85ae-78589c071a3e` | Value proposition, UVP, positioning, customer profiles |
| CIA | Competitive Intelligence Analyst | `cia@memory-service.vtt.ai` | `4ccfe002-ddd3-4df7-bf31-825dcebd576e` | SWOT, benchmarking, feature comparison, pricing analysis |
| MRA | Market Research Analyst | `mra@memory-service.vtt.ai` | `44e7bfb3-2aca-4ac1-820e-0836e95cd718` | Market sizing, TAM/SAM/SOM, trends, segmentacion |
| IR | Integration Reviewer | `integration-reviewer@memory-service.vtt.ai` | `f3e358f7-679f-400f-8dd7-df41517bca15` | Revision end-to-end de integraciones entre modulos |

---

## 4. Especialistas - Alta Prioridad (3 adicionales)

| Code | Rol | Email | UUID | Descripcion |
|------|-----|-------|------|-------------|
| UXR | UX Researcher | `uxr@memory-service.vtt.ai` | `32ffc894-bcd6-4ba6-bcf0-6b9267409d6b` | User research, interviews, usability testing, personas |
| SEC | Security Engineer | `sec@memory-service.vtt.ai` | `5e73d18c-e77e-41a7-9abf-25138a069407` | Security design, pentesting, OWASP, vulnerability assessment |
| QAA | QA Automation Engineer | `qaa@memory-service.vtt.ai` | `2204d168-886e-4b1c-aa62-834f581af382` | Test automation, E2E, integration tests, CI/CD |

---

## 5. Especialistas - Media Prioridad (4)

| Code | Rol | Email | UUID | Descripcion |
|------|-----|-------|------|-------------|
| FA | Financial Analyst | `fa@memory-service.vtt.ai` | `82f46fad-0e0c-476c-a778-d7b30140f94b` | Budget, ROI, cost modeling, financial tracking |
| TW | Technical Writer | `tw@memory-service.vtt.ai` | `10ae0abb-d35a-41e7-9126-3cac7471bcf0` | Documentation, READMEs, API docs, guides |
| PTE | Performance Test Engineer | `pte@memory-service.vtt.ai` | `11e4e316-a220-446b-b408-2dcf5e8d3222` | Load testing, stress testing, performance optimization |
| SRE | Site Reliability Engineer | `sre@memory-service.vtt.ai` | `4f664e98-fa36-4c09-beaa-493f27d7c456` | Monitoring, reliability, scaling, incident response |

---

## Resumen

**Total agentes memory-service:** 23

| Categoria | Cantidad |
|-----------|----------|
| Core tecnico | 8 |
| Gestion | 4 |
| Discovery & Planning / Analysis | 4 |
| Especialistas alta prioridad | 3 |
| Especialistas media prioridad | 4 |

---

## Credenciales

Todos los agentes comparten:

- **Password:** `VttAgent2026`
- **Platform Role:** `platform_super_admin` - bypass de todos los permission checks (no requiere headers `X-Organization-Id` ni `X-Workspace-Id`)

### Login humano

```http
POST http://77.42.88.106:3000/api/auth/login
Content-Type: application/json

{
  "email": "tl@memory-service.vtt.ai",
  "password": "VttAgent2026"
}
```

### Service token (agentes AI)

```http
POST http://77.42.88.106:3000/api/auth/service-token
Content-Type: application/json

{
  "userId": "92225290-6b6b-4c1f-a940-dcb4262507aa",
  "serviceKey": "hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"
}
```

Respuesta: JWT valido por 30 dias.

### Uso en requests autenticados

```http
Authorization: Bearer <JWT>
```

---

## Lista plana de UUIDs (copy/paste)

```
TL   92225290-6b6b-4c1f-a940-dcb4262507aa  tl@memory-service.vtt.ai
BE   ebbe3cee-abed-4b3b-860d-0a81f632b08a  backend@memory-service.vtt.ai
DB   6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7  database@memory-service.vtt.ai
FE   d23c9cd9-a156-433b-8900-94add5488eec  frontend@memory-service.vtt.ai
QAE  613c9538-658c-45fe-a6d7-c1ea9ff04b78  qae@memory-service.vtt.ai
DO   322e3745-9756-4a7c-af11-44b33edef44d  devops@memory-service.vtt.ai
DL   b3a09269-cded-468c-a475-15a48f203cb0  design-lead@memory-service.vtt.ai
UX   a75a1dae-754a-4b6f-a3ff-db8d51f6a91b  ux@memory-service.vtt.ai
PM   350831b2-e1ae-4dbe-b2eb-7e023ec2e103  pm@memory-service.vtt.ai
PJM  0ff63a29-0bc0-465a-b9bd-5f71476bc91d  pjm@memory-service.vtt.ai
SA   0c128e3b-db3b-4e31-b107-0379b5791233  sa@memory-service.vtt.ai
AR   e9403c25-c1f8-4b64-b2ef-f447d53115e2  ar@memory-service.vtt.ai
PSA  a43f6bd0-3452-46ea-85ae-78589c071a3e  psa@memory-service.vtt.ai
CIA  4ccfe002-ddd3-4df7-bf31-825dcebd576e  cia@memory-service.vtt.ai
MRA  44e7bfb3-2aca-4ac1-820e-0836e95cd718  mra@memory-service.vtt.ai
IR   f3e358f7-679f-400f-8dd7-df41517bca15  integration-reviewer@memory-service.vtt.ai
UXR  32ffc894-bcd6-4ba6-bcf0-6b9267409d6b  uxr@memory-service.vtt.ai
SEC  5e73d18c-e77e-41a7-9abf-25138a069407  sec@memory-service.vtt.ai
QAA  2204d168-886e-4b1c-aa62-834f581af382  qaa@memory-service.vtt.ai
FA   82f46fad-0e0c-476c-a778-d7b30140f94b  fa@memory-service.vtt.ai
TW   10ae0abb-d35a-41e7-9126-3cac7471bcf0  tw@memory-service.vtt.ai
PTE  11e4e316-a220-446b-b408-2dcf5e8d3222  pte@memory-service.vtt.ai
SRE  4f664e98-fa36-4c09-beaa-493f27d7c456  sre@memory-service.vtt.ai
```

---

**Ultima actualizacion:** 2026-04-22
**Generado por:** DB Engineer (`a3a2ce62-28d8-419d-9888-44203a963894`)
