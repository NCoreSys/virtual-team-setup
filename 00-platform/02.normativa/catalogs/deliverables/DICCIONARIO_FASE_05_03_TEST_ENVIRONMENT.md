# DICCIONARIO DE DELIVERABLES — FASE 5.3: TEST ENVIRONMENT

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.3 — Test Environment  
**Total deliverables:** 4  
**Responsable de subfase:** DevOps Lead  
**Aprueba:** QA Lead

---

## Contexto de la subfase

Test Environment provee la infraestructura donde se ejecutan los tests: un ambiente separado de development, con datos controlados, configuración production-like, y acceso para el equipo de QA. Sin ambiente de test, QA testea en dev (datos inestables, código en progreso) o peor, en producción.

**Prerequisitos de subfase:**
- Development Environment (4.1.1) — base para test environment
- Environment Matrix (3B.8.5) — configuración de ambientes
- Database Implementation (4.2) — schema y seed data

**Entrega de subfase:**
- Ambiente de testing configurado, con datos, y documentado

---

### 5.3.1 Test Environment

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.3 Test Environment |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | QA Lead |
| **Formato** | Docker/Server |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + mantenimiento |

**Perfil de ejecución:** Requiere provisionar un ambiente staging/QA con configuración production-like.  
En VTT: un agente puede generar IaC para el test environment. Es bastante delegable.

**Qué es:** Ambiente dedicado para testing (staging/QA): deployment del sistema completo (frontend + backend + DB + cache) en un server/cluster separado de development, con configuración lo más cercana posible a producción. URL accesible por el equipo de QA. Deploy automático desde branch main (o release).

**Para qué sirve:** QA necesita testear en un ambiente estable — no en el laptop de un developer. El test environment tiene: código de la última versión testeable, datos controlados (seed + test data), y configuración production-like (para detectar bugs que solo aparecen en prod configs).

**Inputs requeridos:**
- `3B.8.5` Environment Matrix — spec del ambiente QA/staging
- `4.1.1` Development Environment — base Docker
- CI/CD pipeline — deploy automático

**Dependencias (predecessors):**
- `3B.8.5` Environment Matrix *(obligatorio)*
- `4.1.1` Development Environment *(obligatorio)*

**Habilita (successors):**
- `5.4.1` Functional Test Results — tests ejecutados en este ambiente
- `5.6.1` E2E Test Suite — E2E contra este ambiente
- `5.10.1` UAT Plan — UAT en este ambiente

**Audiencia:**
- **QA Team** — ambiente de trabajo
- **DevOps Lead** — mantenimiento
- **Product Owner** — preview de features

**Secciones esperadas:**
1. URL del ambiente (staging.app.com o similar)
2. Componentes deployed (frontend, backend, DB, cache)
3. Configuración vs producción (qué es igual, qué difiere)
4. Deploy process (automático desde qué branch)
5. Access control (quién puede acceder)
6. Reset process (cómo resetear el ambiente a estado limpio)

**Criterio de completitud:**
- [ ] Ambiente accesible por URL
- [ ] Frontend y backend deployed y funcionales
- [ ] BD con datos (seed + test data)
- [ ] Deploy automático configurado
- [ ] Configuración production-like (mismas env vars excepto credentials)
- [ ] Documentado (URL, access, reset process)

**Anti-patrones:**
- ❌ **Testing en development:** Datos inestables, código en progreso — resultados no confiables.
- ❌ **Test env muy diferente a prod:** Diferente OS, DB version, config — bugs "only in prod".
- ❌ **Sin reset process:** Datos de testing acumulados que causan false positives/negatives.

**Template:** `phases/05-testing/deliverables/test-environment.md` *(pendiente)*

---

### 5.3.2 Test Database

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.3 Test Environment |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead / Database Engineer |
| **Aprueba** | QA Lead |
| **Formato** | PostgreSQL |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + resets |

**Perfil de ejecución:** Requiere configurar BD de test con datos controlados y aislados.  
En VTT: un agente puede configurar test DB con migrations y seeds. Es altamente delegable.

**Qué es:** Base de datos dedicada para el ambiente de testing: schema actual (todas las migrations aplicadas), seed data (catálogos, roles), y test data controlado. Aislada de la BD de development para que los tests no se contaminen con datos de desarrollo.

**Para qué sirve:** QA necesita datos predecibles para testear. Si un test case dice "verificar que la lista muestra 10 usuarios", la BD de test debe tener exactamente 10 usuarios — no los 3 que el developer creó ayer.

**Inputs requeridos:**
- `4.2.1` Initial Migration — schema
- `4.2.3` Seed Data — datos base
- `4.2.4` Test Data — datos de testing

**Dependencias (predecessors):**
- `4.2.1` Initial Migration *(obligatorio)*
- `4.2.3` Seed Data *(obligatorio)*

**Habilita (successors):**
- Ejecución de todos los tests

**Audiencia:**
- **QA Team** — datos de testing

**Secciones esperadas:**
1. BD configurada con schema actual
2. Seed data aplicado
3. Test data cargado
4. Reset script (volver a estado limpio)
5. Backup pre-test (para restore si se corrompe)

**Criterio de completitud:**
- [ ] Schema actual aplicado (todas las migrations)
- [ ] Seed data cargado
- [ ] Test data controlado cargado
- [ ] Reset script funcional (`make reset-test-db`)
- [ ] Aislada de BD de development

**Anti-patrones:**
- ❌ **BD compartida con dev:** Tests de QA se mezclan con datos de desarrollo.
- ❌ **Sin reset:** Datos de tests anteriores contaminan tests nuevos.
- ❌ **Datos de producción:** Datos reales de usuarios en test DB — violación de privacidad.

**Template:** `phases/05-testing/deliverables/test-database.md` *(pendiente)*

---

### 5.3.3 Test Data Seeding

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.3 Test Environment |
| **Responsable** | DevOps Lead |
| **Ejecuta** | QA Engineer / DevOps Lead |
| **Aprueba** | QA Lead |
| **Formato** | Scripts |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por reset de ambiente |

**Perfil de ejecución:** Requiere scripts que cargan datos específicos para testing.  
En VTT: un agente puede generar seeding scripts. Es altamente delegable.

**Qué es:** Scripts que cargan datos específicos para testing en el test environment: usuarios de test con diferentes roles (admin, user, editor), entidades con diferentes estados (draft, active, completed), y datos para edge cases (usuario sin órdenes, producto sin stock). Ejecutables con un solo comando para resetear el ambiente.

**Para qué sirve:** QA no debería crear datos manualmente antes de cada sesión de testing. Los seeding scripts crean el "escenario de partida" predecible en un comando: `make seed-test-data` → 50 usuarios, 200 órdenes, 30 productos en diferentes estados.

**Inputs requeridos:**
- `5.2.3` Test Data — datos definidos
- `4.2.3` Seed Data — seed base
- `4.6.5` Mock Factories — factories reutilizables

**Dependencias (predecessors):**
- `5.3.2` Test Database *(obligatorio)* — BD donde cargar
- `5.2.3` Test Data *(obligatorio)* — datos a cargar

**Habilita (successors):**
- Test execution con datos controlados

**Audiencia:**
- **QA Team** — preparación de datos

**Secciones esperadas:**
1. Script de seeding completo
2. Datos por escenario (happy path, error cases, edge cases)
3. Comando de ejecución (`make seed-test`)
4. Idempotencia (ejecutable múltiples veces)

**Criterio de completitud:**
- [ ] Script crea datos para los test cases principales
- [ ] Usuarios con diferentes roles (admin, user, editor)
- [ ] Entidades en diferentes estados
- [ ] Idempotente (puede re-ejecutarse)
- [ ] Ejecutable con un solo comando

**Anti-patrones:**
- ❌ **Seeding manual:** QA crea datos a mano antes de cada sesión — tedioso y propenso a errores.
- ❌ **Seeds no idempotentes:** Re-ejecutar duplica datos — BD corrupta.

**Template:** `phases/05-testing/deliverables/test-data-seeding.ts` *(pendiente)*

---

### 5.3.4 Environment Documentation

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.3 Test Environment |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | QA Lead |
| **Formato** | MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere documentar cómo acceder y usar el test environment.  
En VTT: un agente puede generar la documentación. Es altamente delegable.

**Qué es:** Documentación del test environment: URL, credenciales de acceso (test accounts), cómo resetear datos, cómo deployar una versión específica, limitaciones conocidas, y troubleshooting. Es la guía para que QA use el ambiente sin depender de DevOps.

**Para qué sirve:** QA no debería necesitar a DevOps para: acceder al ambiente, resetear datos, o entender por qué algo no funciona. La documentación les da autonomía.

**Inputs requeridos:**
- `5.3.1` Test Environment — ambiente a documentar

**Dependencias (predecessors):**
- `5.3.1` Test Environment *(obligatorio)*

**Habilita (successors):**
- QA autónomo en el uso del ambiente

**Audiencia:**
- **QA Team** — uso del ambiente
- **Product Owner** — acceso para preview

**Secciones esperadas:**
1. URLs (frontend, backend, Swagger, Storybook)
2. Test accounts (admin, user, editor — con credenciales)
3. Cómo resetear datos (`make reset-staging`)
4. Cómo deployar versión específica
5. Limitaciones conocidas
6. Troubleshooting

**Criterio de completitud:**
- [ ] URLs documentadas
- [ ] Test accounts con credenciales
- [ ] Reset process documentado
- [ ] Troubleshooting de problemas comunes
- [ ] QA puede usar sin ayuda de DevOps

**Anti-patrones:**
- ❌ **Sin documentación:** QA pregunta a DevOps cada vez — bottleneck.
- ❌ **Test accounts no documentadas:** "¿Cuál es el password del admin de staging?" — pregunta repetitiva.

**Template:** `phases/05-testing/deliverables/environment-docs.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 5.3 Test Environment

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 5.3.1 Test Environment | DevOps Lead | DevOps Lead | ✅ — puede generar IaC y config |
| 5.3.2 Test Database | DevOps Lead | DevOps Lead / DB Engineer | ✅ — puede configurar test DB |
| 5.3.3 Test Data Seeding | DevOps Lead | QA Engineer / DevOps | ✅ — puede generar seeding scripts |
| 5.3.4 Environment Documentation | DevOps Lead | DevOps Lead | ✅ — puede generar documentación |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_05_04_FUNCTIONAL_TESTING.md` — 5 deliverables (5.4.1 a 5.4.5)
