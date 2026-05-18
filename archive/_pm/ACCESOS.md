# Matriz de Accesos — Memory Service

**Fecha última actualización:** 2026-05-02
**Mantenido por:** PJM (Memory Service Project Manager)

---

## Accesos por Rol

| Rol | Email VTT | UUID VTT | Repo Principal | Estado |
|-----|-----------|----------|----------------|--------|
| PM (Martin Rivas) | martin.rivas@prompt-ai.studio | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` | memory-service | ✅ activo |
| Tech Lead | memory-service.tl@vtt.ai | `92225290-6b6b-4c1f-a940-dcb4262507aa` | memory-service | ✅ activo |
| PJM | pjm@memory-service.vtt.ai | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` | memory-service | ✅ activo |
| SA (Solution Analyst) | sa@memory-service.vtt.ai | `0c128e3b-db3b-4e31-b107-0379b5791233` | memory-service | ✅ activo |
| AR (Architect) | ar@memory-service.vtt.ai | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | memory-service | ✅ activo |
| Backend Engineer | memory-service.be@vtt.ai | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | memory-service-backend | ✅ activo |
| Database Engineer | memory-service.db@vtt.ai | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | memory-service-backend | ✅ activo |
| Frontend Developer | memory-service.fe@vtt.ai | `d23c9cd9-a156-433b-8900-94add5488eec` | memory-service-frontend | ✅ activo |
| QA Engineer | memory-service.qa@vtt.ai | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | memory-service | ✅ activo |
| DevOps Engineer | memory-service.devops@vtt.ai | `322e3745-9756-4a7c-af11-44b33edef44d` | memory-service-infra | ✅ activo |
| Design Lead | memory-service.dl@vtt.ai | `b3a09269-cded-468c-a475-15a48f203cb0` | memory-service-frontend | ✅ activo |
| UX Designer | memory-service.ux@vtt.ai | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` | memory-service-frontend | ✅ activo |

**SERVICE_KEY (todos los roles):** `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d`

---

## Repos por Rol (ADR-001)

| Repo GitHub | Roles con acceso | Propósito |
|-------------|-----------------|-----------|
| `memory-service` | PM, TL, PJM, SA, AR, QA | Coordinación, docs, knowledge, tests |
| `memory-service-backend` | BE, DB | Código backend Node.js + TypeScript + Prisma |
| `memory-service-frontend` | FE, DL, UX | Código frontend React + Vite + TailwindCSS |
| `memory-service-infra` | DO | Infra, docker-compose, CI/CD |
| `memory-service-api` | TL | Contrato de API (OpenAPI spec) |

> Referencia: `memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md`

---

## Verificación de Acceso VTT

Para verificar que un rol tiene acceso al sistema VTT:

```bash
curl -s -X POST "http://77.42.88.106:3000/api/auth/service-token" \
  -H "Content-Type: application/json" \
  -d '{"userId":"[UUID_DEL_ROL]","serviceKey":"hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"}'
# → Debe devolver {"data":{"token":"eyJ..."}}
```

---

## Proceso de Onboarding Nuevo Agente

1. PM crea el agente en VTT y obtiene UUID
2. PM actualiza `.claude/rules/Proyect_data.md` con el nuevo UUID y email
3. PM actualiza esta matriz con el nuevo rol
4. PM notifica al agente con: UUID, SERVICE_KEY, email VTT, repos con acceso
5. Agente verifica acceso con el comando de verificación arriba
6. Agente lee su `OPERATIVO_[ROL]_MEMORY-SERVICE.md` al iniciar

---

## Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-05-02 | Matriz inicial creada con 12 roles | PJM (MS-134) |
