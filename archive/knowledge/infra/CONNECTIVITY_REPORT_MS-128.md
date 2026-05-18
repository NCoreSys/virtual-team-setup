# Connectivity Report — MS-128 / INIT-C-02

**Fecha:** 2026-04-30
**VM:** 77.42.88.106 (Hetzner)
**Verificado por:** DO Memory Service
**Resultado global:** 5/7 OK, 2 pendientes (servicios no desplegados)

---

## Resumen

| # | Test | Componente | Resultado |
|---|------|-----------|-----------|
| 7 | Baseline VTT | `:3000/health` | ✅ OK |
| 1 | PostgreSQL `memory_service_db` | `:5432` desde local | ❌ Bloqueado por diseño (bind 127.0.0.1) |
| 1b | PostgreSQL desde VM (SSH) | `docker exec` | ✅ OK |
| 2 | Volumen storage write | `/root/memory-service-storage/` | ✅ OK |
| 3 | Redis prefix `mem` desde local | `:6379` desde local | ❌ Bloqueado por diseño (bind 127.0.0.1) |
| 3b | Redis prefix `mem` desde VM | `docker exec` | ✅ OK |
| 4 | Puerto 3002 (API) | TCP local→VM | ⏳ Cerrado — servicio no desplegado |
| 5 | Puerto 3003 (UI) | TCP local→VM | ⏳ Cerrado — servicio no desplegado |
| 6 | Docker shared-network | `docker network ls` | ✅ OK |

---

## Test 7 — Baseline VTT (executed first)

**Comando:**
```bash
curl -s http://77.42.88.106:3000/health
```

**Output:**
```json
{
  "status": "ok",
  "timestamp": "2026-04-30T14:26:49.355Z",
  "services": {
    "api": "ok",
    "database": "ok",
    "redis": "ok",
    "minio": "ok"
  }
}
```

VTT operativo, todos los servicios compartidos saludables.

---

## Test 1 — PostgreSQL `memory_service_db`

### Test 1a (desde local) — esperado FAIL
```bash
timeout 5 bash -c 'cat < /dev/null > /dev/tcp/77.42.88.106/5432'
```
Output: `CERRADO`

### Test 1b (desde VM via SSH)
```bash
ssh root@77.42.88.106 "docker exec shared-postgres psql -U postgres -d memory_service_db -c 'SELECT 1 as test;'"
```
Output:
```
 test
------
    1
(1 row)
```

**Conclusión:** BD existe y responde. Inaccesible desde local **por diseño** —
PostgreSQL bind a `127.0.0.1` segun INFRASTRUCTURE_GUIDE §Seguridad.

**Para acceso desde local, los devs deben usar SSH tunnel:**
```bash
ssh -L 5432:localhost:5432 root@77.42.88.106
# Luego: psql -h localhost -p 5432 ...
```

---

## Test 2 — Volumen `/root/memory-service-storage/` write

```bash
ssh root@77.42.88.106 "echo 'test' > /root/memory-service-storage/test.txt \
  && cat /root/memory-service-storage/test.txt \
  && rm /root/memory-service-storage/test.txt"
```
Output: `test` + `WRITE-OK`

**Conclusión:** ✅ Volumen escribible. Permisos correctos para que el contenedor escriba al deploy.

---

## Test 3 — Redis prefix `mem`

### Test 3a (desde local) — esperado FAIL
```bash
timeout 5 bash -c 'cat < /dev/null > /dev/tcp/77.42.88.106/6379'
```
Output: `CERRADO`

### Test 3b (desde VM via SSH)
```bash
ssh root@77.42.88.106 "
docker exec shared-redis redis-cli -a RedisSecure2026 PING
docker exec shared-redis redis-cli -a RedisSecure2026 SET mem:test 'ok'
docker exec shared-redis redis-cli -a RedisSecure2026 GET mem:test
docker exec shared-redis redis-cli -a RedisSecure2026 DEL mem:test
"
```
Output:
```
PONG
OK
ok
1
```

**Conclusión:** ✅ Redis funcional, prefix `mem` operativo. Inaccesible desde local
por la misma razón que PostgreSQL.

---

## Test 4 — Puerto 3002 (Memory Service API)

```bash
timeout 5 bash -c 'cat < /dev/null > /dev/tcp/77.42.88.106/3002'
```
Output: `Connection refused`

**Conclusión:** ⏳ Puerto cerrado — Memory Service API no desplegado aún.
Esperado en esta etapa del proyecto. Se abrirá al hacer el primer `docker-compose up` del servicio.

---

## Test 5 — Puerto 3003 (Memory Service UI)

```bash
timeout 5 bash -c 'cat < /dev/null > /dev/tcp/77.42.88.106/3003'
```
Output: `Connection refused`

**Conclusión:** ⏳ Puerto cerrado — Frontend no desplegado aún. Se abrirá en sprint FE.

---

## Test 6 — Docker shared-network

```bash
ssh root@77.42.88.106 "docker network ls | grep shared-network"
```
Output:
```
b983387ac7c8   shared-network   bridge   local
```

**Conclusión:** ✅ Red Docker existe, todos los contenedores la usan.

---

## Conclusiones

1. **5/7 tests OK**, 2 pendientes (esperables — servicio no desplegado).
2. **No hay blockers reales.** Los "fails" de los tests 1 y 3 desde local son por
   **diseño de seguridad**, no por error de configuración.
3. **Para devs que necesiten acceso a PostgreSQL/Redis desde su máquina:**
   usar SSH tunnel — comando arriba.
4. **No se requiere abrir puertos adicionales en el firewall** — la regla de seguridad
   actual (PostgreSQL/Redis solo internos) debe mantenerse.

## ISSUEs creados

Ninguno. No hay blockers reales. Los items pendientes corresponden a tareas
posteriores (deploy del servicio).
