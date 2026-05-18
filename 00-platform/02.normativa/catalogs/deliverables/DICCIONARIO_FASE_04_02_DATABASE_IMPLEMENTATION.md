# DICCIONARIO DE DELIVERABLES — FASE 4.2: DATABASE IMPLEMENTATION

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 4 — Development  
**Subfase:** 4.2 — Database Implementation  
**Total deliverables:** 10  
**Responsable de subfase:** Database Engineer  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Database Implementation traduce el diseño de BD (3B.3) en código ejecutable: migrations que crean el schema, seed data que puebla catálogos, índices que optimizan queries, y scripts de rollback que permiten revertir cambios. Es la primera implementación de "diseño → código" del proyecto y establece el modelo de datos sobre el que se construye todo el backend.

**Prerequisitos de subfase:**
- Database Design completo (3B.3) — ERD, schema, index strategy
- Development Environment (4.1.1) — BD local corriendo
- Migration Strategy (3B.3.6) — herramienta y proceso definidos

**Entrega de subfase:**
- BD completamente inicializada con schema, índices, constraints, seed data, y guía de migraciones

---

### 4.2.1 Initial Migration

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | SQL / Prisma Migrate |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere traducir el ERD y Schema Definition en la primera migration ejecutable.  
En VTT: un agente puede generar la migration inicial completa desde el schema definition (3B.3.2). Es altamente delegable. Necesita brief con: schema definition en Prisma/SQL, y convención de naming de migrations.

**Qué es:** Primera migration que crea el schema completo de la base de datos desde cero: todas las tablas, columnas, tipos, constraints, foreign keys, y enums definidos en el Schema Definition (3B.3.2). Es el "CREATE TABLE" de todo el modelo de datos. Se ejecuta una vez para inicializar cualquier ambiente nuevo.

**Para qué sirve:** Crea la BD con un solo comando (`prisma migrate dev` o `flyway migrate`). Cualquier ambiente nuevo (developer local, staging, prod) ejecuta esta migration y tiene la estructura de BD completa. Es reproducible, versionada, y reversible.

**Inputs requeridos:**
- `3B.3.2` Schema Definition — schema a implementar
- `3B.3.1` ERD Complete — referencia visual
- `3B.3.6` Migration Strategy — herramienta y naming

**Dependencias (predecessors):**
- `3B.3.2` Schema Definition *(obligatorio)*
- `4.1.1` Development Environment *(obligatorio)* — BD local corriendo

**Habilita (successors):**
- `4.2.2` Schema Migrations — migrations incrementales
- `4.2.3` Seed Data — datos sobre el schema
- `4.2.5` Indexes — índices en las tablas
- `4.3.3` Models — modelos de aplicación

**Secciones esperadas:
- `prisma/migrations/YYYYMMDD_init/migration.sql` (Prisma)
- o `migrations/V1__initial_schema.sql` (Flyway)
- `prisma/schema.prisma` (si Prisma)

**Criterio de completitud:
- [ ] Migration crea todas las tablas del ERD
- [ ] Tipos de datos correctos por columna
- [ ] NOT NULL, UNIQUE, CHECK constraints aplicados
- [ ] Foreign keys con CASCADE behavior correcto
- [ ] Timestamps (created_at, updated_at) en todas las tablas
- [ ] Migration ejecutable sin errores en BD limpia
- [ ] Migration reversible (down migration funciona)
- [ ] Schema validado contra el ERD (nada faltante)

**Anti-patrones:**
- ❌ **Schema manual sin migration:** `CREATE TABLE` ejecutado a mano — no reproducible ni versionado.
- ❌ **Migration con datos:** Mezclar DDL (schema) con DML (inserts) — difícil de revertir parcialmente.
- ❌ **Schema que no coincide con ERD:** El ERD dice una cosa y la migration otra — desincronización.

**Template:** `phases/04-development/deliverables/initial-migration.sql` *(pendiente)*

---

### 4.2.2 Schema Migrations

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | SQL / Prisma Migrate |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (por sprint) |
| **Frecuencia** | Por sprint / por feature |

**Perfil de ejecución:** Requiere conocimiento de migrations incrementales y zero-downtime schema changes.  
En VTT: un agente puede generar migrations incrementales a partir de cambios en el schema. Es altamente delegable. Necesita brief con: cambios requeridos (nueva tabla, nuevo campo, cambio de tipo).

**Qué es:** Migrations incrementales que evolucionan el schema después de la initial migration: agregar columnas, crear nuevas tablas, modificar tipos, agregar constraints. Cada migration es un archivo versionado con timestamp que se aplica en orden. Son el historial de evolución del schema.

**Para qué sirve:** El schema cambia con cada sprint (nueva feature = nueva tabla o campo). Las migrations son la forma controlada de aplicar esos cambios: versionadas, ordenadas, reversibles, y aplicables en cualquier ambiente de forma idéntica.

**Inputs requeridos:**
- Cambios requeridos por nuevas features/user stories
- `3B.3.6` Migration Strategy — proceso y reglas

**Dependencias (predecessors):**
- `4.2.1` Initial Migration *(obligatorio)*
- `3B.3.6` Migration Strategy *(obligatorio)*

**Habilita (successors):**
- Features que requieren cambios de schema

**Secciones esperadas:
- `prisma/migrations/YYYYMMDD_description/migration.sql` (por migration)

**Criterio de completitud:
- [ ] Migration ejecutable sin errores
- [ ] Down migration funciona (reversible)
- [ ] No lockea tablas grandes en producción
- [ ] Backward compatible (app vieja funciona con schema nuevo)
- [ ] Revisada por Tech Lead antes de apply en staging/prod
- [ ] Naming descriptivo (`add_status_to_orders`, no `migration_47`)

**Anti-patrones:**
- ❌ **Migration que lockea tabla:** `ALTER TABLE users ADD COLUMN` con lock en tabla de 10M rows — downtime.
- ❌ **Sin down migration:** Aplicar y no poder revertir — riesgo en producción.
- ❌ **Breaking changes sin backward compatibility:** Renombrar columna que la app actual usa — deploy falla.
- ❌ **Migrations editadas post-apply:** Modificar una migration ya aplicada — desincronización entre ambientes.

**Template:** `phases/04-development/deliverables/schema-migration.sql` *(pendiente)*

---

### 4.2.3 Seed Data

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | SQL / TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + adiciones |

**Perfil de ejecución:** Requiere conocimiento del dominio para generar datos de catálogo correctos.  
En VTT: un agente puede generar seed scripts completos. Es altamente delegable. Necesita brief con: tablas de catálogo con valores, roles, y permisos del sistema.

**Qué es:** Scripts que insertan datos iniciales de sistema necesarios para que la aplicación funcione: roles (admin, user, editor), permisos, catálogos (países, estados, categorías), configuraciones default, y el usuario admin inicial. Son datos que van a TODOS los ambientes (dev, staging, prod).

**Para qué sirve:** Sin seed data, la app no funciona: no hay roles para asignar, no hay categorías para clasificar, no hay configuraciones default. El seed script asegura que cada ambiente nuevo tiene los datos base idénticos.

**Inputs requeridos:**
- `3B.3.7` Seed Data Plan — qué datos sembrar
- `2.5.5` Authorization Rules — roles y permisos
- Catálogos del dominio

**Dependencias (predecessors):**
- `4.2.1` Initial Migration *(obligatorio)* — tablas deben existir
- `3B.3.7` Seed Data Plan *(obligatorio)*

**Habilita (successors):**
- `4.2.4` Test Data — datos de prueba sobre el seed
- Funcionamiento de la aplicación

**Secciones esperadas:
- `prisma/seed.ts` o `scripts/seed.sql`

**Criterio de completitud:
- [ ] Datos de sistema completos (roles, permisos, catálogos)
- [ ] Script idempotente (ejecutable múltiples veces sin duplicar)
- [ ] Orden de ejecución respeta FK constraints
- [ ] No incluye datos personales reales
- [ ] Ejecutable con un solo comando (`make seed`)

**Anti-patrones:**
- ❌ **Seed no idempotente:** Ejecutar 2 veces = datos duplicados.
- ❌ **Datos reales de personas en seed:** Violación de privacidad.
- ❌ **Seed de dev en producción:** Datos fake visibles a usuarios reales.

**Template:** `phases/04-development/deliverables/seed.ts` *(pendiente)*

---

### 4.2.4 Test Data

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Backend Developer / QA |
| **Aprueba** | Tech Lead |
| **Formato** | SQL / TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Continuo |

**Perfil de ejecución:** Requiere Faker o factories para generar datos realistas.  
En VTT: un agente puede generar factories y fixtures con datos fake realistas. Es altamente delegable.

**Qué es:** Scripts y factories que generan datos fake realistas para desarrollo y testing: usuarios con nombres fake (Faker), órdenes con datos aleatorios pero coherentes, y relaciones entre entidades. Separado del seed data — estos son SOLO para dev/test, nunca para producción.

**Para qué sirve:** Un developer necesita 50 usuarios con órdenes para probar una lista paginada. Sin test data, crea 3 usuarios a mano — insuficiente para detectar problemas de paginación, performance, o layout con datos largos.

**Inputs requeridos:**
- `4.2.3` Seed Data — base sobre la que se agrega test data
- `3B.3.3` Table Specifications — campos y constraints

**Dependencias (predecessors):**
- `4.2.3` Seed Data *(obligatorio)* — catálogos base
- `4.2.1` Initial Migration *(obligatorio)*

**Habilita (successors):**
- `4.6.5` Mock Factories — factories reutilizables en tests
- Testing manual con datos realistas

**Secciones esperadas:
- `scripts/test-data.ts` o `tests/factories/`
- Configuración de Faker

**Criterio de completitud:
- [ ] Factories para entidades principales (User, Order, Product, etc.)
- [ ] Datos realistas (Faker con locale correcto)
- [ ] Relaciones entre entidades coherentes
- [ ] Ejecutable con `make test-data`
- [ ] Solo se ejecuta en dev/test (never prod)

**Anti-patrones:**
- ❌ **Datos manuales:** 3 usuarios creados a mano en cada DB reset — tedioso y no escalable.
- ❌ **Test data con datos reales:** Copiar producción a dev — violación de privacidad.
- ❌ **Test data sin relaciones:** Users sin orders, orders sin products — FK errors.

**Template:** `phases/04-development/deliverables/test-data.ts` *(pendiente)*

---

### 4.2.5 Indexes

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | SQL |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + ajustes post-profiling |

**Perfil de ejecución:** Requiere implementar la Index Strategy (3B.3.4) en SQL.  
En VTT: un agente puede generar CREATE INDEX statements desde la index strategy. Es altamente delegable.

**Qué es:** Implementación de los índices definidos en la Index Strategy: CREATE INDEX para foreign keys, campos de búsqueda frecuente, campos de sorting, y composite indexes. Implementados como parte de la initial migration o como migration separada.

**Para qué sirve:** Sin índices, queries en tablas grandes hacen full table scan — queries de 30 segundos en producción. Los índices correctos reducen eso a milisegundos.

**Inputs requeridos:**
- `3B.3.4` Index Strategy — qué índices crear
- `4.2.1` Initial Migration — tablas donde crear índices

**Dependencias (predecessors):**
- `3B.3.4` Index Strategy *(obligatorio)*
- `4.2.1` Initial Migration *(obligatorio)*

**Habilita (successors):**
- Performance de queries del backend

**Secciones esperadas:
- Incluidos en migrations o `migrations/add_indexes.sql`

**Criterio de completitud:
- [ ] Todos los índices del Index Strategy implementados
- [ ] Foreign keys indexados
- [ ] Composite indexes con orden correcto de columnas
- [ ] EXPLAIN ANALYZE verificado en queries principales
- [ ] No over-indexing (índices sin uso removidos)

**Anti-patrones:**
- ❌ **Sin índices en FK:** JOINs hacen full scan — performance disaster.
- ❌ **Índices duplicados:** El ORM crea un índice y el dev agrega otro manualmente — overhead sin beneficio.

**Template:** `phases/04-development/deliverables/indexes.sql` *(pendiente)*

---

### 4.2.6 Constraints

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | SQL |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 4.2.1 |
| **Frecuencia** | Una vez + por migration |

**Perfil de ejecución:** Requiere conocimiento de constraints de BD: CHECK, UNIQUE, EXCLUSION, y FK behaviors.  
En VTT: un agente puede generar constraints desde las validation rules y table specifications. Es altamente delegable.

**Qué es:** Constraints de base de datos que garantizan integridad de datos a nivel de BD (no solo de aplicación): UNIQUE (email único por usuario), CHECK (price > 0, status IN ('draft', 'active', 'closed')), NOT NULL, y FK con ON DELETE/ON UPDATE behavior definido. La BD es la última línea de defensa de data integrity.

**Para qué sirve:** La validación en la aplicación puede bypassearse (import directo, script, bug). Los constraints de BD son infranqueables: si `email` tiene UNIQUE constraint, no puede haber duplicados sin importar de dónde venga el INSERT. Son la garantía de que los datos siempre son válidos.

**Inputs requeridos:**
- `3B.3.3` Table Specifications — constraints por tabla
- `2.5.3` Validation Rules — reglas a enforcar en BD

**Dependencias (predecessors):**
- `4.2.1` Initial Migration *(obligatorio)*
- `3B.3.3` Table Specifications *(obligatorio)*

**Habilita (successors):**
- Integridad de datos garantizada

**Secciones esperadas:
- Incluidos en migrations (ALTER TABLE ADD CONSTRAINT)

**Criterio de completitud:
- [ ] UNIQUE constraints en campos que deben ser únicos
- [ ] CHECK constraints en campos con valores válidos definidos
- [ ] NOT NULL en campos requeridos
- [ ] FK CASCADE behavior correcto (no cascade deletes accidentales)
- [ ] Constraints nombrados descriptivamente

**Anti-patrones:**
- ❌ **Sin constraints:** BD acepta cualquier dato — data corruption inevitable.
- ❌ **Cascade DELETE sin pensar:** Borrar un user borra todas sus órdenes, facturas, logs — data loss.
- ❌ **Solo validación en app:** Un script de import directo bypassa la app — datos inválidos en BD.

**Template:** `phases/04-development/deliverables/constraints.sql` *(pendiente)*

---

### 4.2.7 Stored Procedures

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | SQL |
| **Obligatorio** | ⚪ Opcional |
| **Esfuerzo típico** | 1-2 días (si aplica) |
| **Frecuencia** | Por necesidad |

**Perfil de ejecución:** Requiere PL/pgSQL u otro procedural SQL si se necesitan stored procedures.  
En VTT: un agente puede generar stored procedures desde especificaciones. Necesita brief con: lógica a implementar y parámetros.

**Qué es:** Procedimientos almacenados en la BD para lógica que es más eficiente o segura ejecutar a nivel de BD: cálculos complejos sobre grandes volúmenes de datos, operaciones atómicas multi-tabla, triggers, y funciones reutilizables. Solo se crean cuando hay justificación de performance o atomicidad que la aplicación no puede lograr eficientemente.

**Para qué sirve:** Operaciones que procesan millones de registros son más eficientes en la BD (sin transferencia de datos a la app). También garantizan atomicidad en operaciones multi-tabla sin depender del application-level transaction management.

**Inputs requeridos:**
- Requisitos de performance o atomicidad que justifiquen stored procedures
- `3B.3.3` Table Specifications — tablas involucradas

**Dependencias (predecessors):**
- `4.2.1` Initial Migration *(obligatorio)*

**Habilita (successors):**
- Backend consume stored procedures

**Criterio de completitud:
- [ ] Stored procedure documentada (qué hace, parámetros, return)
- [ ] Testeada con datos de prueba
- [ ] Performance verificada vs alternativa en aplicación
- [ ] Incluida en migrations (versionada)

**Anti-patrones:**
- ❌ **Lógica de negocio en stored procedures:** Toda la lógica en la BD — imposible de testear, debuggear, y versionar como código de aplicación.
- ❌ **Stored procedures para CRUD:** No hay justificación — el ORM lo hace igual de bien.

**Template:** `phases/04-development/deliverables/stored-procedures.sql` *(pendiente)*

---

### 4.2.8 Views

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | SQL |
| **Obligatorio** | ⚪ Opcional |
| **Esfuerzo típico** | 0.5-1 día (si aplica) |
| **Frecuencia** | Por necesidad |

**Perfil de ejecución:** Requiere diseño de queries complejas como vistas reutilizables.  
En VTT: un agente puede generar CREATE VIEW statements. Es altamente delegable.

**Qué es:** Vistas de base de datos que encapsulan queries complejas frecuentes: JOINs multi-tabla para reporting, aggregaciones para dashboards, y vistas materializadas para queries costosas. Las vistas simplifican el código de aplicación (SELECT * FROM user_summary en vez de un JOIN de 5 tablas).

**Para qué sirve:** Queries complejas que se repiten en múltiples partes del código se centralizan en una vista. Si la query cambia (nueva columna, nuevo JOIN), se actualiza la vista y todo el código que la consume se beneficia automáticamente.

**Inputs requeridos:**
- Queries complejas frecuentes identificadas
- `3B.3.3` Table Specifications — tablas involucradas

**Dependencias (predecessors):**
- `4.2.1` Initial Migration *(obligatorio)*

**Habilita (successors):**
- Backend consume vistas simplificadas
- Reporting queries

**Criterio de completitud:
- [ ] Vista creada con migration
- [ ] Query de la vista optimizada (EXPLAIN ANALYZE)
- [ ] Documentada (qué datos agrega, de qué tablas)
- [ ] Testeada con datos representativos

**Anti-patrones:**
- ❌ **Vistas anidadas:** Vista que consume otra vista que consume otra — performance degradada exponencialmente.
- ❌ **Vistas para todo:** SELECT simple no necesita vista — agrega complejidad sin beneficio.

**Template:** `phases/04-development/deliverables/views.sql` *(pendiente)*

---

### 4.2.9 Migration Guide

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | README |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere documentación clara del proceso de migrations para todo el equipo.  
En VTT: un agente puede generar la guía completa. Es altamente delegable.

**Qué es:** Guía operativa de cómo trabajar con migrations en el proyecto: cómo crear una nueva migration, cómo aplicarla en dev, cómo hacer rollback, qué revisar antes de aplicar en staging/prod, dangerous operations checklist, y proceso de PR review para migrations.

**Para qué sirve:** Cada backend developer crea migrations. Sin guía, cada uno lo hace diferente: uno nombra bien, otro no; uno hace down migration, otro no; uno prueba rollback, otro no. La guía estandariza el proceso.

**Inputs requeridos:**
- `3B.3.6` Migration Strategy — estrategia definida
- Herramienta de migrations (Prisma, Flyway, etc.)

**Dependencias (predecessors):**
- `3B.3.6` Migration Strategy *(obligatorio)*
- `4.2.1` Initial Migration *(obligatorio)* — proceso probado

**Habilita (successors):**
- Todo el equipo puede crear migrations correctamente

**Secciones esperadas:
- `docs/MIGRATIONS.md` o sección en README

**Criterio de completitud:
- [ ] Cómo crear migration (comando step-by-step)
- [ ] Cómo aplicar en dev (make migrate)
- [ ] Cómo hacer rollback
- [ ] Dangerous operations checklist
- [ ] PR review process para migrations
- [ ] Probada por un developer que no la escribió

**Anti-patrones:**
- ❌ **Sin guía:** Cada developer inventa su proceso — inconsistencia.
- ❌ **Guía solo para Prisma:** Sin explicar el razonamiento — cuando se cambie de herramienta, se pierde el conocimiento.

**Template:** `phases/04-development/deliverables/migration-guide.md` *(pendiente)*

---

### 4.2.10 Rollback Scripts

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.2 Database Implementation |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer / DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | SQL |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en cada migration |
| **Frecuencia** | Por migration |

**Perfil de ejecución:** Requiere escribir la operación inversa de cada migration (DROP lo que se CREATEó, remover lo que se ADDió).  
En VTT: un agente puede generar rollback scripts automáticamente como inversa de cada migration. Es altamente delegable.

**Qué es:** Scripts de rollback (down migrations) para cada migration: la operación inversa que deshace los cambios. Si la migration agrega una columna, el rollback la quita. Si crea una tabla, el rollback la dropea. Cada migration debe tener su rollback script listo ANTES de aplicarse en producción.

**Para qué sirve:** Si una migration causa problemas en producción (breaking change, data corruption, performance), el rollback permite revertir a la versión anterior en minutos. Sin rollback, el fix requiere una nueva migration hacia adelante — más riesgo y más tiempo.

**Inputs requeridos:**
- Cada migration creada en 4.2.2

**Dependencias (predecessors):**
- `4.2.2` Schema Migrations *(obligatorio)* — migration a revertir

**Habilita (successors):**
- Recovery rápido ante problemas de migration en producción

**Secciones esperadas:
- Down migration por cada up migration (automático en Prisma/Rails, manual en Flyway)

**Criterio de completitud:
- [ ] Cada migration tiene su rollback correspondiente
- [ ] Rollback testeado en dev (aplicar → rollback → verificar)
- [ ] Rollback no pierde datos (o documenta qué datos se pierden)
- [ ] Rollback ejecutable con un solo comando

**Anti-patrones:**
- ❌ **Sin rollback:** "Si falla, hacemos otra migration" — tiempo perdido en una emergencia.
- ❌ **Rollback no testeado:** El rollback existe pero nunca se probó — falla cuando se necesita.
- ❌ **Rollback destructivo no documentado:** DROP TABLE en el rollback sin advertir que pierde datos — sorpresa desagradable.

**Template:** `phases/04-development/deliverables/rollback-scripts.sql` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 4.2 Database Implementation

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 4.2.1 Initial Migration | Database Engineer | Database Engineer / Backend Dev | ✅ — puede generar migration desde schema definition |
| 4.2.2 Schema Migrations | Database Engineer | Database Engineer / Backend Dev | ✅ — puede generar migrations incrementales |
| 4.2.3 Seed Data | Database Engineer | Database Engineer / Backend Dev | ✅ — puede generar seed scripts completos |
| 4.2.4 Test Data | Database Engineer | Backend Dev / QA | ✅ — puede generar factories con Faker |
| 4.2.5 Indexes | Database Engineer | Database Engineer | ✅ — puede generar CREATE INDEX desde index strategy |
| 4.2.6 Constraints | Database Engineer | Database Engineer | ✅ — puede generar constraints desde table specs |
| 4.2.7 Stored Procedures | Database Engineer | Database Engineer | 🔶 Parcial — puede generar código, pero lógica requiere juicio |
| 4.2.8 Views | Database Engineer | Database Engineer | ✅ — puede generar CREATE VIEW desde queries |
| 4.2.9 Migration Guide | Database Engineer | Database Engineer | ✅ — puede generar guía completa |
| 4.2.10 Rollback Scripts | Database Engineer | Database Engineer / DevOps | ✅ — puede generar down migrations |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_04_03_BACKEND_DEVELOPMENT.md` — 15 deliverables (4.3.1 a 4.3.15)
