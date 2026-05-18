# Code Logic - MS-129: Distribucion SERVICE_KEY a consumidores

## Informacion General

| Campo | Valor |
|-------|-------|
| Tarea | MS-129 / INIT-C-03 |
| Tipo | Infrastructure / Security |
| Fecha | 2026-04-30 |

---

## Proposito

Distribuir la SERVICE_KEY del Memory Service a los servicios consumidores,
garantizando que la key nunca se exponga en codigo o documentacion.

---

## Flujo de Distribucion

VM /root/memory-service/.env
  -> (leer via SSH, valor en memoria del agente)
  -> gh secret set MEMORY_SERVICE_KEY --repo NCoreSys/<repo-consumidor>
  -> GitHub Actions Secret (encrypted at rest)
  -> Disponible como env var en CI/CD del consumidor
  -> curl -H "X-Service-Key: " http://77.42.88.106:3002/api/health

---

## Consumidores

| Consumidor | Metodo | Estado |
|------------|--------|--------|
| memory-service-frontend | GitHub Secret | Activo |
| Runtime v1.1 | - | Pendiente repo |
| Prompt Builder v1.3 | - | Pendiente repo |
| Hook Manager | - | Pendiente repo |

---

## Decisiones de Diseno

GitHub Secrets sobre .env directo: encriptados en reposo, no aparecen en logs CI,
se pueden rotar sin acceso SSH. Metodo preferido para servicios con GitHub Actions.

3 consumidores sin repo: No se mockean ni se crean repos ficticios (PROJECT_RULES 15.3).
Se distribuira cuando los servicios tengan repos activos.

---

## Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-04-30 | Creacion - distribucion inicial a memory-service-frontend | DO Agent |
