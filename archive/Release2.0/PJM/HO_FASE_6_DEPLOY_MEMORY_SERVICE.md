# HANDOFF — Fase 6: Deploy · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_FASE_6_DEPLOY_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PJM — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Para** | DO — `322e3745-9756-4a7c-af11-44b33edef44d` |
| **CC** | TL — `92225290-6b6b-4c1f-a940-dcb4262507aa` · QA — `613c9538-658c-45fe-a6d7-c1ea9ff04b78` · PM — `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |
| **Rol líder** | DO (DevOps Engineer) + TL |
| **Proyecto** | Memory Service |
| **Fase VTT** | Deploy (Phase order 9) |
| **Estado** | ✅ APROBADO — listo para ejecución |

---

## RESUMEN EJECUTIVO

Esta fase lleva el Memory Service a **producción en el servidor Hetzner** (`77.42.88.106`). Tiene 7 tareas VTT (MEM-104..110), 26h totales, distribuidas en 7 VTT Deliveries.

**Roles activos:** DO · QA · TL  
**Líder de seguimiento:** DO + TL  
**Criterio de entrada:** Gate Testing cerrado (MEM-103 `task_completed`) + p95 <500ms verificado + UAT aprobado  
**Criterio de salida:** MEM-110 `task_completed` + Memory Service en producción + Rollback Plan documentado

---

## 1. ARQUITECTURA DE LA FASE

```
╔══════════════════════════════════════════════════════════════╗
║   GATE DE ENTRADA: MEM-103 task_completed                    ║
║   (Testing completo + UAT aprobado + 0 bugs críticos)        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   DELIVERY 1: Infrastructure Setup                           ║
║   └─ MEM-104  Infrastructure Setup    DO   4h  MED          ║
║                                                              ║
║   DELIVERY 2: CI/CD Configuration                            ║
║   └─ MEM-105  CI/CD Configuration     DO   6h  MED          ║
║                                                              ║
║   DELIVERY 3: Staging Deploy                                 ║
║   └─ MEM-106  Staging Deploy          DO   4h  MED          ║
║                                                              ║
║   DELIVERY 4: Smoke Testing                                  ║
║   └─ MEM-107  Smoke Testing           QA   3h  MED          ║
║                                                              ║
║   DELIVERY 5: Production Deploy                              ║
║   └─ MEM-108  Production Deploy       DO   4h  CRITICAL     ║
║                                                              ║
║   DELIVERY 6: Post-Deploy Monitoring                         ║
║   └─ MEM-109  Post-Deploy Monitoring  DO   3h  MED          ║
║                                                              ║
║   DELIVERY 7: Rollback Plan                                  ║
║   └─ MEM-110  Rollback Plan           TL   2h  MED          ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║   GATE DE SALIDA: MEM-110 completed + Prod funcionando       ║
║   → Habilita Fase 7 Operations (MEM-111)                     ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. DEPENDENCIAS INTERNAS

```
MEM-103 (Testing gate)
    │
    ▼
MEM-104 (Infrastructure Setup)
    │
    ▼
MEM-105 (CI/CD Configuration)
    │
    ├──────────────────────────────────► MEM-106 (Staging Deploy)
    │                                          │
    │                                          ▼
    │                                    MEM-107 (Smoke Testing)
    │                                          │
    │                                          ▼
    │                                    MEM-108 (Production Deploy) 🚨 CRITICAL
    │                                          │
    │                    ┌─────────────────────┤
    │                    ▼                     ▼
    │               MEM-109 (Post-Deploy)  MEM-110 (Rollback Plan)
    │               Monitoring
    │
    └──────────────────────────────────► MEM-110 (puede prepararse en paralelo)
```

---

## 3. TAREAS VTT — DETALLE

### MEM-104 · Infrastructure Setup

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-104 |
| **Rol** | DO (`322e3745-9756-4a7c-af11-44b33edef44d`) |
| **Delivery** | Infrastructure Setup |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | deployment |

**Descripción:** Preparar la infraestructura de producción en Hetzner:
- Verificar que la BD `memory_service_db` existe y está accesible desde shared-postgres.
- Verificar que el volumen `/root/memory-service-storage/` existe y tiene permisos correctos.
- Verificar Redis con prefix `mem` accesible desde shared-network Docker.
- Verificar que los puertos 3002 (API) y 3003 (UI) están abiertos en firewall.
- Verificar que shared-network Docker está configurada.
- Ejecutar `prisma migrate deploy` para aplicar schema en producción.
- Ejecutar `prisma db seed` para cargar los 10 catálogos iniciales.
- Documentar en `docs/INFRASTRUCTURE.md` con estado de cada verificación.

---

### MEM-105 · CI/CD Configuration

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-105 |
| **Rol** | DO (`322e3745-9756-4a7c-af11-44b33edef44d`) |
| **Delivery** | CI/CD Configuration |
| **Horas** | 6h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | deployment |

**Descripción:** Configurar el pipeline completo de CI/CD:
- GitHub Actions: `.github/workflows/ci.yml` — lint + type-check + test + build en cada PR.
- GitHub Actions: `.github/workflows/deploy.yml` — deploy automático a staging en merge a main; deploy manual a producción con aprobación.
- Secrets configurados en GitHub: `VTT_SERVICE_KEY`, credenciales BD, SERVER_SSH_KEY.
- Deploy script: SSH al servidor Hetzner → git pull → docker-compose up -d --build.
- Health check post-deploy: verificar GET /health responde `{"status":"healthy"}` en < 5s.
- Rollback automático: si health check falla → revertir a imagen anterior.

---

### MEM-106 · Staging Deploy

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-106 |
| **Rol** | DO (`322e3745-9756-4a7c-af11-44b33edef44d`) |
| **Delivery** | Staging Deploy |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | deployment |

**Descripción:** Desplegar el Memory Service en el entorno de staging:
- Build de imagen Docker con `docker-compose -f docker-compose.staging.yml up -d --build`.
- Verificar que los contenedores arrancan sin errores.
- Verificar que la BD de staging está correctamente migrada y seeded.
- Verificar conectividad al shared-network y Redis.
- Ejecutar el test de humo manual: GET /health → `{"status":"healthy"}`.
- Documentar la URL de staging y las credenciales de acceso.

---

### MEM-107 · Smoke Testing

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-107 |
| **Rol** | QA (`613c9538-658c-45fe-a6d7-c1ea9ff04b78`) |
| **Delivery** | Smoke Testing |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | testing |

**Descripción:** Ejecutar smoke tests sobre el entorno de staging:
- GET /health → `{"status":"healthy","checks":{"db":"ok","storage":"ok","redis":"ok"}}`.
- POST /import con payload minimal → status 201, conversación persistida.
- GET /context con projectId válido → respuesta < 500ms.
- GET /conversations → lista devuelve conversación importada.
- GET /dashboard/stats → métricas coherentes.
- UI: abrir el browser en staging → Dashboard carga sin errores.
- Documentar resultado de cada smoke test. Si alguno falla → **bloquear Production Deploy**.

---

### MEM-108 · Production Deploy

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-108 |
| **Rol** | DO (`322e3745-9756-4a7c-af11-44b33edef44d`) |
| **Delivery** | Production Deploy |
| **Horas** | 4h |
| **Prioridad** | **CRITICAL** |
| **Complejidad** | HIGH |
| **Categoría** | deployment |

**Descripción:** Desplegar el Memory Service en producción (Hetzner 77.42.88.106):

> ⚠️ **PRERREQUISITO ABSOLUTO:** MEM-107 Smoke Testing completado sin errores. PM aprobado.

- Crear backup de la BD antes del deploy.
- Ejecutar deploy en producción vía pipeline CI/CD (merge a rama `release/v1.0`).
- Monitorear logs durante los primeros 10 minutos post-deploy.
- Verificar GET /health en producción → `{"status":"healthy"}`.
- Verificar que los datos en producción son independientes del staging.
- Notificar al equipo: Memory Service en producción.
- Registrar: versión deployada, timestamp, commit hash.

---

### MEM-109 · Post-Deploy Monitoring

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-109 |
| **Rol** | DO (`322e3745-9756-4a7c-af11-44b33edef44d`) |
| **Delivery** | Post-Deploy Monitoring |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | deployment |

**Descripción:** Monitorear el sistema durante las primeras 24-48h post-deploy:
- Configurar alertas: latencia GET /context > 400ms, error rate > 1%, health check failure.
- Monitorear logs: errores 5xx, timeouts, cleanup cron funcionando.
- Verificar que el cleanup cron (5min) está corriendo y procesando STALE correctamente.
- Revisar storage: crecimiento de archivos JSONL en `/root/memory-service-storage/`.
- Reporte de métricas: p50, p95, p99 de cada endpoint después de 24h en producción.
- Documentar cualquier issue encontrado y acción tomada.

---

### MEM-110 · Rollback Plan

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-110 |
| **Rol** | TL (`92225290-6b6b-4c1f-a940-dcb4262507aa`) |
| **Delivery** | Rollback Plan |
| **Horas** | 2h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Documentar el plan de rollback del Memory Service:
- Condiciones que gatillan un rollback: health check failure >5min, p95 >1000ms sostenido, bug crítico de datos.
- Procedimiento de rollback: paso a paso con comandos exactos para volver a imagen anterior.
- Comunicación durante rollback: quién notifica, a quién, con qué formato.
- Restauración de BD: procedimiento para restaurar desde backup si necesario.
- Tiempo máximo de rollback objetivo: < 15 minutos.
- Post-mortem template: qué documentar después de un rollback.

---

## 4. RESUMEN DE TAREAS

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-104 | Infrastructure Setup | DO | 4 | MEDIUM | M |
| MS-105 | CI/CD Configuration | DO | 6 | HIGH | M |
| MS-106 | Staging Deploy | DO | 4 | MEDIUM | M |
| MS-107 | Smoke Testing | QA | 3 | MEDIUM | M |
| **MS-108** | **Production Deploy** | **DO** | **4** | **HIGH** | **C** |
| MS-109 | Post-Deploy Monitoring | DO | 3 | MEDIUM | M |
| MS-110 | Rollback Plan | TL | 2 | MEDIUM | M |
| **TOTAL** | | | **26h** | | |

---

## 5. INFRAESTRUCTURA DE REFERENCIA

| Componente | Valor |
|-----------|-------|
| Servidor | Hetzner 77.42.88.106 |
| API puerto | 3002 |
| UI puerto | 3003 |
| BD | memory_service_db en shared-postgres |
| Storage | /root/memory-service-storage/ |
| Redis prefix | mem |
| Network | shared-network (Docker) |
| SLA | GET /context p95 < 500ms |

---

## 6. GATE DE SALIDA — CRITERIOS DE COMPLETITUD

```
[ ] MEM-104 task_completed — Infra verificada + schema migrado + seeds aplicados
[ ] MEM-105 task_completed — CI/CD pipeline funcionando (lint + test + deploy)
[ ] MEM-106 task_completed — Staging up + healthy
[ ] MEM-107 task_completed — Smoke tests en staging: todos pasados
[ ] MEM-108 task_completed (CRITICAL) — Production deploy exitoso + /health OK
[ ] MEM-109 task_completed — Monitoring configurado + primeras 24h sin issues críticos
[ ] MEM-110 task_completed — Rollback Plan documentado y validado por TL
[ ] PM notificado: Memory Service en producción
[ ] MEM-111 desbloqueado en VTT (Fase Operations arranca)
```

---

## 7. ESCALACIÓN

| Bloqueo | Escalar a |
|---------|-----------|
| Infra no disponible (DB, storage, Redis) | PM (Admin VM) |
| Smoke test falla en staging | TL + BE |
| Deploy production falla | TL + PM (decisión rollback) |
| p95 >500ms en producción | TL + AR |
| Rollback necesario | TL lidera, notificar PM inmediatamente |

---

## 8. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PJM (emite)** | PJM Agent | ✅ EMITIDO | 2026-04-22 |
| **DO (recibe y lidera)** | DO Agent | ⬜ Pendiente acuse | — |
| **TL (Rollback Plan)** | TL Agent | ⬜ Pendiente acuse | — |
| **PM (autoriza Production Deploy)** | Martin Rivas | ⬜ Pendiente autorización | — |

---

## 9. REFERENCIAS

- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — §4.9 Deploy tasks
- `HO_FASE_3B_DESIGN_TECH_MEMORY_SERVICE.md` — §MEM-046 Infrastructure Plan (diseño infra)
- `HO_FASE_5_TESTING_MEMORY_SERVICE.md` — Gate previo (smoke test baseline)
- `VTT_UUIDS_MEMORY_SERVICE.json` — UUIDs tareas MS-104..110

---

**Documento:** HO_FASE_6_DEPLOY_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ EMITIDO — Pendiente autorización PM para Production Deploy  
**Fecha:** 2026-04-22

---

**PJM — Memory Service**  
Virtual Teams Tracking
