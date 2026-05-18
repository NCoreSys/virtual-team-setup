# Infrastructure Checklist — Memory Service

**Fecha verificacion**: 2026-04-24
**Servidor**: 77.42.88.106 (Hetzner)
**Verificado por**: DO (Memory Service DevOps Engineer)

---

| Item | Estado | Detalle |
|------|--------|---------|
| memory_service_db (PostgreSQL) | ✅ OK | Existe en shared-postgres. Listada en `\l`. |
| /root/memory-service-storage/ | ✅ OK | Existe. Permisos: drwxr-xr-x root root. Directorio vacio (sin datos aun). |
| Redis (shared-redis) | ✅ OK | PING → PONG con auth (RedisSecure2026). Prefix `mem` sera usado por el servicio en runtime. |
| Puerto 3002 (API) | ⏳ PENDIENTE | Cerrado — Memory Service no esta desplegado aun. Se abrira al hacer el primer deploy. |
| Puerto 3003 (UI) | ⏳ PENDIENTE | Cerrado — Frontend no esta desplegado. Se abrira en sprint de FE. |
| shared-network Docker | ✅ OK | Existe (ID: b983387ac7c8). Todos los servicios de la VM usan esta red. |
| SERVICE_KEY en .env | ✅ OK | Configurada en /root/memory-service/.env. Valor presente (no se loguea por seguridad). |

---

## Resumen

**5 de 7 items OK.** Los 2 pendientes son esperables — los puertos se abren al desplegar el servicio,
no antes. No hay items bloqueantes para iniciar el desarrollo.

## Pendientes de provisionamiento

- Puerto 3002: se abre al hacer el primer `docker-compose up` de memory-service
- Puerto 3003: se abre cuando FE tenga su primer deploy

## Notas adicionales

- `/root/memory-service/.env` existe con SERVICE_KEY configurada — infra provisionada correctamente
- Redis responde con auth habilitada — el servicio debe usar `REDIS_URL=redis://:RedisSecure2026@shared-redis:6379`
- El volumen `/root/memory-service-storage/` tiene permisos de root — verificar que el contenedor
  tenga acceso de escritura al momento del deploy
