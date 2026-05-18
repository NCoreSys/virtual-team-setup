# DICCIONARIO DE DELIVERABLES — FASE 3B.3: DATABASE DESIGN

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.3 — Database Design  
**Total deliverables:** 8  
**Responsable de subfase:** Database Engineer  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Database Design define el modelo de datos del sistema: qué entidades existen, cómo se relacionan, cómo se almacenan, y cómo se acceden eficientemente. Un mal diseño de BD es la deuda técnica más cara de pagar — cambiar un schema en producción con datos es orden de magnitud más complejo que cambiar código de aplicación.

**Prerequisitos de subfase:**
- Solution Architecture definida (3B.1) — tipo de BD elegida
- Detailed Use Cases (2.3.4) — entidades del dominio identificadas
- Business Rules Document (2.5.1) — reglas que afectan el modelo

**Entrega de subfase:**
- Modelo de datos completo, schema definido, estrategias de indexación, migración, seed data y backups documentadas

---

### 3B.3.1 ERD Complete

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.3 Database Design |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | Diagrama (Mermaid/dbdiagram.io/Draw.io) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + actualizaciones por feature nueva |

**Perfil de ejecución:** Requiere experiencia en modelado de datos: normalización (3NF), desnormalización estratégica, cardinalidades, y trade-offs entre models relacionales, documentales y de grafos.  
En VTT: un agente puede generar el ERD en Mermaid o dbdiagram.io syntax a partir de una descripción de entidades y sus relaciones. Puede también derivar entidades de los use cases y business rules. Es bastante delegable. Necesita brief con: lista de entidades del dominio, atributos principales, cardinalidades, y decisiones de normalización ya tomadas.

**Qué es:** Diagrama Entidad-Relación completo que muestra todas las entidades (tablas) del sistema, sus atributos principales, y las relaciones entre ellas con cardinalidad (1:1, 1:N, N:M). Incluye entidades de dominio (User, Order, Product), entidades de sistema (AuditLog, Session, Migration), y tablas intermedias para relaciones N:M.

**Para qué sirve:** Es el mapa del modelo de datos. Permite al equipo visualizar la estructura completa de la BD antes de escribir schema. Detecta problemas de diseño temprano (entidades faltantes, relaciones incorrectas, campos mal ubicados). Es referencia para Backend Developers al escribir queries y para QA al preparar test data.

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — entidades del dominio extraídas
- `2.5.1` Business Rules Document — reglas que afectan el modelo
- `3B.1.7` Data Flow Diagram — datos que fluyen por el sistema
- `3B.1.4` Component Diagram — bounded contexts que agrupan entidades
- `2.5.7` Business Glossary — nomenclatura de entidades

**Dependencias (predecessors):**
- `2.3.4` Detailed Use Cases *(obligatorio)* — entidades derivadas de funcionalidad
- `2.5.1` Business Rules Document *(obligatorio)* — constraints del modelo
- `3B.1.7` Data Flow Diagram *(recomendado)* — entidades identificadas en flujos
- `3B.1.5` Technology Stack *(obligatorio)* — tipo de BD condiciona el modelado

**Habilita (successors):**
- `3B.3.2` Schema Definition — implementación del ERD en SQL/ORM
- `3B.3.3` Table Specifications — detalle de cada tabla
- `3B.3.4` Index Strategy — índices basados en relaciones y queries
- `3B.3.5` Data Dictionary — documentación de cada campo
- `3B.4.1` OpenAPI Spec — entidades mapeadas a API resources

**Audiencia:**
- **Database Engineer** — referencia propia para schema definition
- **Backend Developer** — entiende el modelo para escribir queries
- **Tech Lead** — validación del modelo
- **QA Engineer** — entiende relaciones para preparar test data
- **Product Owner** — validación de que las entidades reflejan el dominio

**Secciones esperadas:**
1. ERD completo (diagrama visual con todas las entidades y relaciones)
2. Leyenda (PK, FK, nullable, unique, cardinalidades)
3. Entidades de dominio agrupadas por bounded context
4. Entidades de sistema (audit, auth, config)
5. Tablas intermedias (N:M relationships)
6. Notas de normalización (decisiones de 3NF vs desnormalización)
7. Enum values documentados por tabla

**Criterio de completitud:**
- [ ] Todas las entidades del dominio representadas
- [ ] Cardinalidad (1:1, 1:N, N:M) en todas las relaciones
- [ ] PKs y FKs indicados
- [ ] Entidades de sistema incluidas (audit, auth, sessions)
- [ ] Tablas intermedias para relaciones N:M
- [ ] Leyenda incluida
- [ ] Validado contra use cases (cada use case tiene las entidades que necesita)

**Anti-patrones:**
- ❌ **ERD como afterthought:** Diseñar la BD al vuelo durante desarrollo — cambios de schema con datos son costosos.
- ❌ **Sobre-normalización:** 7 tablas para representar una dirección con 5 campos — complejidad en queries sin beneficio real.
- ❌ **Desnormalización prematura:** Duplicar datos "por performance" sin evidencia — deuda de consistencia.
- ❌ **Sin entidades de auditoría:** No planear audit logs, soft deletes, ni timestamps — imposible rastrear qué pasó.
- ❌ **Entity Attribute Value (EAV):** Usar una tabla key-value genérica para todo — anti-pattern que destruye queryability.

**Template:** `phases/03B-design-technical/deliverables/erd-complete.mmd` *(pendiente)*

---

### 3B.3.2 Schema Definition

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.3 Database Design |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | SQL / Prisma / TypeORM |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + migraciones incrementales |

**Perfil de ejecución:** Requiere dominio del ORM o query builder elegido (Prisma, TypeORM, Sequelize, Django ORM, SQLAlchemy) o SQL puro. Debe conocer tipos de datos óptimos, constraints, y defaults.  
En VTT: un agente puede generar el schema definition completo en Prisma/SQL/TypeORM a partir del ERD. Puede producir la migration initial y seed scripts. Es altamente delegable. Necesita brief con: ERD completo, ORM/tool elegido, tipos de datos por campo, constraints, defaults, y convención de naming de tablas/columnas.

**Qué es:** Implementación formal del ERD en código de schema: archivos SQL (CREATE TABLE), o schema files del ORM elegido (Prisma schema, TypeORM entities, Django models). Define cada tabla con: columnas, tipos de datos, constraints (NOT NULL, UNIQUE, CHECK), defaults, foreign keys, y enums. Es el código que crea la base de datos.

**Para qué sirve:** Transforma el diagrama conceptual (ERD) en código ejecutable. Es la fuente de verdad del modelo de datos — no el diagrama, sino el schema que realmente se ejecuta. Permite crear la BD con un solo comando y garantiza que todos los environments (dev, staging, prod) tienen la misma estructura.

**Inputs requeridos:**
- `3B.3.1` ERD Complete — modelo a implementar
- `3B.1.5` Technology Stack — ORM/tool elegido
- `3B.2.5` Naming Conventions — naming de tablas y columnas
- `3B.3.3` Table Specifications — detalle de cada tabla

**Dependencias (predecessors):**
- `3B.3.1` ERD Complete *(obligatorio)* — modelo a implementar
- `3B.1.5` Technology Stack *(obligatorio)* — ORM/tool
- `3B.2.5` Naming Conventions *(obligatorio)* — naming de tablas/columnas

**Habilita (successors):**
- `3B.3.6` Migration Strategy — migration initial basada en el schema
- `3B.3.7` Seed Data Plan — datos iniciales para las tablas definidas
- `4.2.1` Database Setup — creación de BD con el schema
- `4.3.2` Database Models — models de aplicación basados en el schema

**Audiencia:**
- **Database Engineer** — mantiene y evoluciona el schema
- **Backend Developer** — referencia de tipos y constraints al codificar
- **DevOps Lead** — migration scripts para deploy
- **QA Engineer** — estructura de BD para test data

**Secciones esperadas:**
1. Schema file(s) completo (SQL/Prisma/ORM)
2. Tabla de tipos de datos (columna, tipo elegido, justificación si no es obvio)
3. Constraints documentados (UNIQUE, CHECK, NOT NULL con justificación)
4. Defaults documentados (timestamps, UUIDs, estados iniciales)
5. Enums definidos (valores posibles, significado)
6. Foreign keys con ON DELETE/ON UPDATE behavior
7. Instrucciones de ejecución (cómo crear la BD desde 0)

**Criterio de completitud:**
- [ ] Todas las tablas del ERD implementadas
- [ ] Tipos de datos apropiados (no todo VARCHAR(255))
- [ ] Constraints NOT NULL donde corresponde
- [ ] UNIQUE constraints donde corresponde
- [ ] Foreign keys con cascade behavior definido
- [ ] Timestamps (created_at, updated_at) en todas las tablas
- [ ] Soft delete (deleted_at) donde aplique
- [ ] Schema ejecutable sin errores

**Anti-patrones:**
- ❌ **VARCHAR(255) para todo:** No dimensionar strings — un email no necesita 255 chars, un slug menos.
- ❌ **Sin constraints:** Tablas sin NOT NULL, UNIQUE, ni CHECK — la BD no valida nada, los bugs llegan a datos.
- ❌ **Cascade DELETE sin pensar:** ON DELETE CASCADE en tablas de auditoría — borras un user y desaparecen sus logs.
- ❌ **IDs auto-incrementales expuestos:** Usar INT sequential IDs en APIs públicas — expone volumen de datos y es enumerable.
- ❌ **Sin timestamps:** Tablas sin created_at/updated_at — imposible saber cuándo se creó o modificó un registro.

**Template:** `phases/03B-design-technical/deliverables/schema-definition.prisma` *(pendiente)*

---

### 3B.3.3 Table Specifications

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.3 Database Design |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | Documento (MD/Tabla) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + actualizaciones por migration |

**Perfil de ejecución:** Requiere atención al detalle y conocimiento del dominio para describir cada campo con su propósito de negocio, no solo su tipo técnico.  
En VTT: un agente puede generar las especificaciones de cada tabla a partir del schema definition: tabla de columnas con tipo, nullable, default, descripción. Es altamente delegable. Necesita brief con: schema definition, contexto de negocio de cada campo, y validaciones esperadas.

**Qué es:** Documentación detallada de cada tabla de la base de datos. Para cada tabla: propósito, columnas con tipo/constraints/descripción, relaciones con otras tablas, volumen esperado de datos, frecuencia de lectura vs escritura, y queries más frecuentes. Es el "manual de cada tabla" que va más allá del schema técnico.

**Para qué sirve:** El schema dice que `status` es `VARCHAR(20)` — la especificación dice que los valores válidos son 'draft', 'pending', 'approved', 'rejected' y que la transición de 'approved' a 'draft' está prohibida. La especificación agrega el contexto de negocio que el schema no puede expresar.

**Inputs requeridos:**
- `3B.3.1` ERD Complete — modelo de referencia
- `3B.3.2` Schema Definition — tipos y constraints técnicos
- `2.5.1` Business Rules Document — reglas por entidad
- `2.5.3` Validation Rules — validaciones de campos

**Dependencias (predecessors):**
- `3B.3.1` ERD Complete *(obligatorio)*
- `3B.3.2` Schema Definition *(obligatorio)*
- `2.5.1` Business Rules Document *(recomendado)*

**Habilita (successors):**
- `3B.3.4` Index Strategy — queries frecuentes identifican índices necesarios
- `3B.3.5` Data Dictionary — fields documentados en detalle
- `4.3.2` Database Models — developers entienden cada campo

**Audiencia:**
- **Backend Developer** — entiende qué representa cada campo y sus constraints de negocio
- **Database Engineer** — referencia propia
- **QA Engineer** — sabe qué valores son válidos para test data
- **Business Analyst** — valida que el modelo refleja el dominio

**Secciones esperadas (por tabla):**
1. Nombre y propósito de la tabla
2. Tabla de columnas (nombre, tipo, nullable, default, unique, descripción, validaciones)
3. Primary key (tipo: UUID, serial, composite)
4. Foreign keys (referencia, on delete, on update)
5. Indexes (ver 3B.3.4 — referencia)
6. Constraints especiales (CHECK, exclusion)
7. Enum values con significado de cada valor
8. Volumen esperado (filas estimadas en 1 año, growth rate)
9. Access pattern (reads vs writes, queries más comunes)
10. Soft delete behavior (si aplica)
11. Notas de negocio (reglas que afectan esta tabla)

**Criterio de completitud:**
- [ ] Todas las tablas del schema especificadas
- [ ] Cada columna tiene descripción de negocio (no solo tipo)
- [ ] Enum values documentados con significado
- [ ] Volumen estimado por tabla
- [ ] Access patterns identificados (read-heavy, write-heavy)
- [ ] Constraints de negocio documentados (no solo técnicos)
- [ ] Validado por Product Owner o Business Analyst

**Anti-patrones:**
- ❌ **Solo tipos sin contexto:** `status: VARCHAR(20)` sin documentar los valores válidos ni las transiciones — el developer inventa.
- ❌ **Sin estimación de volumen:** No saber si una tabla tendrá 100 o 100M de rows — afecta drasticamente las decisiones de índices y partitioning.
- ❌ **Especificaciones desactualizadas:** Schema evoluciona con migrations pero las specs no se actualizan — documentación muerta.
- ❌ **Copiar el schema:** La especificación no es un dump del schema — agrega el contexto de negocio que el schema no tiene.

**Template:** `phases/03B-design-technical/deliverables/table-specifications.md` *(pendiente)*

---

### 3B.3.4 Index Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.3 Database Design |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + refinamientos post-profiling |

**Perfil de ejecución:** Requiere conocimiento de indexación: tipos de índices (B-tree, hash, GIN, GiST), composite indexes, partial indexes, covering indexes, y cómo impactan en read/write performance.  
En VTT: un agente puede proponer índices basándose en las queries más frecuentes documentadas en Table Specifications y los access patterns. Puede generar los CREATE INDEX statements. NO puede decidir trade-offs performance-críticos sin profiling real. Necesita brief con: queries más comunes por tabla, access patterns, volumen esperado, y constraints de write performance.

**Qué es:** Documento que define la estrategia de indexación: qué índices crear en cada tabla, de qué tipo, en qué columnas, y por qué. Incluye índices para: primary keys (automáticos), foreign keys, campos de búsqueda frecuente, campos de ordering, y campos de filtering. Documenta el trade-off entre read performance (más índices = reads más rápidos) y write performance (más índices = writes más lentos).

**Para qué sirve:** Los índices correctos pueden hacer una query de 30 segundos en 30 milisegundos. Los índices incorrectos (o faltantes) causan full table scans en producción que tumban el sistema. Planificar los índices antes de tener datos previene los "incendios" de performance en producción.

**Inputs requeridos:**
- `3B.3.3` Table Specifications — queries frecuentes y access patterns
- `3B.3.1` ERD Complete — relaciones que necesitan índices en FKs
- `3B.4.2` Endpoints List — endpoints que generan queries frecuentes
- Volumen estimado de datos

**Dependencias (predecessors):**
- `3B.3.3` Table Specifications *(obligatorio)* — access patterns y volumen
- `3B.3.1` ERD Complete *(obligatorio)* — foreign keys a indexar
- `3B.3.2` Schema Definition *(obligatorio)* — tipos de datos (afectan tipo de índice)

**Habilita (successors):**
- `3B.3.2` Schema Definition — índices incluidos en el schema final
- `4.2.1` Database Setup — índices creados al inicializar la BD
- `5.7.1` Performance Testing — benchmarks verifican efectividad de índices

**Audiencia:**
- **Database Engineer** — implementación y mantenimiento
- **Backend Developer** — entiende qué queries son eficientes
- **Tech Lead** — validación de strategy
- **DevOps Lead** — impacto en storage y mantenimiento

**Secciones esperadas:**
1. Principios de indexación del proyecto (cuándo indexar, cuándo no)
2. Tabla de índices (tabla, columnas, tipo, justificación)
3. Índices en foreign keys (automatizados o manuales según el engine)
4. Índices compuestos (orden de columnas y justificación)
5. Partial indexes (índices condicionales para subsets de datos)
6. Full-text search indexes (si aplica)
7. Unique indexes (constraints de unicidad)
8. Análisis de write impact (overhead estimado en writes)
9. Plan de profiling post-deploy (EXPLAIN ANALYZE, pg_stat_user_indexes)
10. Índices a NO crear (y por qué — evitar over-indexing)

**Criterio de completitud:**
- [ ] Todas las foreign keys indexadas
- [ ] Campos de búsqueda frecuente indexados
- [ ] Campos de sorting frecuente indexados
- [ ] Tipo de índice justificado (B-tree vs GIN vs hash)
- [ ] Composite indexes con orden de columnas correcto
- [ ] Write impact considerado
- [ ] Plan de profiling post-deploy definido

**Anti-patrones:**
- ❌ **Indexar todo:** Índice en cada columna — write performance destruida, storage inflado.
- ❌ **No indexar foreign keys:** Queries con JOINs hacen full table scan — performance disaster a escala.
- ❌ **Composite index con orden incorrecto:** Index en `(status, created_at)` cuando las queries filtran por `created_at` primero — el índice no se usa.
- ❌ **Índices sin uso:** Índices creados "por si acaso" que ninguna query utiliza — overhead sin beneficio.
- ❌ **Sin plan de profiling:** No planear cómo verificar que los índices funcionan — optimización a ciegas.

**Template:** `phases/03B-design-technical/deliverables/index-strategy.md` *(pendiente)*

---

### 3B.3.5 Data Dictionary

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.3 Database Design |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer / Technical Writer |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla (MD/Spreadsheet) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + actualizaciones por migration |

**Perfil de ejecución:** Requiere conocimiento del dominio de negocio para describir cada campo con significado, no solo su tipo técnico. Es trabajo de documentación meticuloso.  
En VTT: un agente puede generar el data dictionary completo a partir del schema y las table specifications. Es altamente delegable — es fundamentalmente un ejercicio de documentación estructurada. Necesita brief con: schema definition, table specifications, y business glossary para términos de dominio.

**Qué es:** Catálogo exhaustivo de cada campo de cada tabla: nombre, tipo, descripción de negocio, ejemplo de valor, constraints, fuente del dato (user input, calculated, system-generated, external), y mapping a conceptos de dominio. Es más granular que las Table Specifications — documenta cada campo individualmente.

**Para qué sirve:** Es el Rosetta Stone entre el mundo técnico y el de negocio. Cuando alguien pregunta "¿qué es `accrued_interest_rate`?", el data dictionary responde sin que nadie tenga que leer código. Facilita reporting, data analysis, compliance (GDPR: ¿qué campos son PII?), y onboarding de nuevos miembros.

**Inputs requeridos:**
- `3B.3.2` Schema Definition — campos técnicos
- `3B.3.3` Table Specifications — contexto de negocio
- `2.5.7` Business Glossary — términos de dominio
- `2.5.4` Calculation Rules — campos calculados

**Dependencias (predecessors):**
- `3B.3.2` Schema Definition *(obligatorio)* — campos a documentar
- `3B.3.3` Table Specifications *(obligatorio)* — contexto por tabla
- `2.5.7` Business Glossary *(recomendado)* — vocabulario estandarizado

**Habilita (successors):**
- `4.3.2` Database Models — developers entienden cada campo
- `5.1.3` Test Data Strategy — datos de prueba con valores correctos
- Reports y analytics — queries con campos correctos

**Audiencia:**
- **Backend Developer** — entiende qué representa cada campo
- **Data Analyst** — queries e interpretación de datos
- **QA Engineer** — test data con valores correctos
- **Compliance** — campos PII identificados
- **Business Analyst** — validación de que el modelo refleja el dominio

**Secciones esperadas:**
1. Tabla maestra del diccionario (tabla, campo, tipo, nullable, descripción, ejemplo, fuente, PII flag)
2. Sección por tabla con campos agrupados
3. Campos PII marcados (para compliance GDPR/CCPA)
4. Campos calculados con fórmula
5. Campos con enum: valores posibles y significado
6. Campos deprecados o en proceso de eliminación
7. Mapping a conceptos de dominio del Business Glossary

**Criterio de completitud:**
- [ ] Todos los campos de todas las tablas documentados
- [ ] Cada campo tiene descripción de negocio (no solo tipo)
- [ ] Ejemplo de valor válido para cada campo
- [ ] Fuente del dato documentada (user input, system, calculated, external)
- [ ] Campos PII identificados
- [ ] Enums con valores y significado
- [ ] Campos calculados con fórmula o referencia

**Anti-patrones:**
- ❌ **Copiar tipos sin descripción:** `user_id: UUID` sin explicar "ID del usuario que creó el registro" — no agrega valor sobre el schema.
- ❌ **Sin ejemplos:** Describir el campo sin ejemplo de valor — el developer no sabe qué esperar.
- ❌ **PII no marcado:** No identificar campos como email, phone, address como PII — compliance risk.
- ❌ **Diccionario desactualizado:** Schema evoluciona, diccionario no — documentación engañosa.

**Template:** `phases/03B-design-technical/deliverables/data-dictionary.md` *(pendiente)*

---

### 3B.3.6 Migration Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.3 Database Design |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere experiencia con herramientas de migration (Prisma Migrate, Flyway, Alembic, Django migrations) y entendimiento de zero-downtime migrations en producción.  
En VTT: un agente puede documentar la estrategia de migrations basándose en el ORM/tool elegido: convenciones de naming, proceso de creación/aplicación, rollback, y best practices. Es altamente delegable. Necesita brief con: herramienta de migration, ambientes (dev/staging/prod), proceso de deploy, y policy de rollback.

**Qué es:** Documento que define cómo se gestionan los cambios al schema de la base de datos a lo largo del tiempo: herramienta de migration, convención de naming de migrations, proceso de creación y aplicación, rollback strategy, y reglas para migrations en producción (zero-downtime, backward compatibility).

**Para qué sirve:** La BD evoluciona con cada sprint (nueva tabla, nuevo campo, cambio de tipo). Sin una estrategia, los cambios se hacen manualmente ("corre este ALTER TABLE en producción") — propenso a errores, no reproducible, y no reversible. La estrategia garantiza que los cambios son versionados, reproducibles, y reversibles.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — herramienta de migration
- `3B.3.2` Schema Definition — schema inicial como primera migration
- Proceso de deploy del proyecto (CI/CD pipeline)

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)* — herramienta de migration
- `3B.3.2` Schema Definition *(obligatorio)* — schema que se versiona
- `3B.8.5` Environment Matrix *(recomendado)* — ambientes donde aplicar migrations

**Habilita (successors):**
- `4.2.1` Database Setup — proceso de setup usa migrations
- `4.1.4` CI/CD Pipeline — migration step en el pipeline de deploy
- Todas las futuras migrations del proyecto

**Audiencia:**
- **Database Engineer** — proceso a seguir
- **Backend Developer** — cómo crear y aplicar migrations
- **DevOps Lead** — migration step en CI/CD
- **Tech Lead** — revisión de migrations en PRs

**Secciones esperadas:**
1. Herramienta de migration (nombre, versión, configuración)
2. Convención de naming (timestamp-based, sequential, descriptivo)
3. Proceso de creación de migrations (comando, revisión, testing)
4. Proceso de aplicación (dev → staging → prod)
5. Rollback strategy (down migrations, manual rollback, forward-fix)
6. Reglas para migrations en producción (no-lock migrations, backward compatibility)
7. Dangerous operations checklist (DROP, RENAME, ALTER TYPE, NOT NULL without default)
8. Migration review process (quién revisa, qué verificar)
9. Seed data vs migration data (cuándo es seed, cuándo es data migration)
10. Disaster recovery para migrations fallidas

**Criterio de completitud:**
- [ ] Herramienta de migration configurada y documentada
- [ ] Naming convention definida
- [ ] Proceso de creación y aplicación step-by-step
- [ ] Rollback strategy definida
- [ ] Reglas de producción documentadas (zero-downtime)
- [ ] Dangerous operations listadas con proceso de aprobación
- [ ] Migration review integrado en PR process

**Anti-patrones:**
- ❌ **Migrations manuales:** `ALTER TABLE users ADD COLUMN ...` ejecutado a mano en producción — no versionado, no reversible.
- ❌ **Sin rollback plan:** Aplicar migration sin saber cómo revertir — si falla, hay que improvisar.
- ❌ **Lock tables en producción:** `ALTER TABLE` que lockea una tabla de 10M rows durante minutos — downtime.
- ❌ **Migrations con datos de negocio:** Mezclar schema changes con data inserts — difícil de revertir parcialmente.
- ❌ **Sin review:** Migrations que van directo a producción sin revisión — un typo puede borrar datos.

**Template:** `phases/03B-design-technical/deliverables/migration-strategy.md` *(pendiente)*

---

### 3B.3.7 Seed Data Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.3 Database Design |
| **Responsable** | Database Engineer |
| **Ejecuta** | Database Engineer / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Documento (MD) + Scripts |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + actualizaciones incrementales |

**Perfil de ejecución:** Requiere conocimiento del dominio para generar datos de prueba realistas y datos de catálogo correctos. Debe diferenciar entre seed data de sistema (roles, permisos, catálogos) y seed data de desarrollo (datos fake para testing).  
En VTT: un agente puede generar seed scripts completos: catálogos de sistema, datos fake realistas con Faker/factories, y scripts de ejecución. Es altamente delegable. Necesita brief con: tablas de catálogo con valores, cantidad de registros fake por tabla, relaciones entre datos (orders deben referenciar users existentes), y herramienta de seeding.

**Qué es:** Plan que define qué datos iniciales necesita la base de datos y scripts para generarlos. Incluye: datos de sistema (roles, permisos, configuraciones, catálogos), datos de catálogo (países, estados, categorías), y datos de desarrollo (usuarios fake, órdenes fake, para testing local). Diferencia claramente entre datos que van a producción y datos solo para desarrollo.

**Para qué sirve:** Sin seed data, un developer que clona el repo tiene una BD vacía y no puede probar nada. Los datos de catálogo son necesarios para que la aplicación funcione (no puedes crear un usuario sin el catálogo de roles). Los datos fake aceleran el desarrollo local y el testing manual.

**Inputs requeridos:**
- `3B.3.2` Schema Definition — tablas a sembrar
- `3B.3.3` Table Specifications — enum values y catálogos
- `2.5.5` Authorization Rules — roles y permisos del sistema
- Catálogos del dominio (proporcionados por Product Owner)

**Dependencias (predecessors):**
- `3B.3.2` Schema Definition *(obligatorio)* — tablas que existen
- `3B.3.3` Table Specifications *(obligatorio)* — valores de catálogo
- `2.5.5` Authorization Rules *(recomendado)* — roles y permisos como seed

**Habilita (successors):**
- `4.2.1` Database Setup — seed ejecutado post-migration
- `5.1.3` Test Data Strategy — seed data como base para test data
- `4.1.3` Project Scaffolding — seed script incluido en setup

**Audiencia:**
- **Backend Developer** — datos para desarrollo local
- **Frontend Developer** — datos para prototyping y testing visual
- **QA Engineer** — datos base para testing
- **DevOps Lead** — seed scripts para nuevos ambientes

**Secciones esperadas:**
1. Clasificación de seed data (sistema, catálogo, desarrollo)
2. Datos de sistema (tabla: tabla, datos, destino: dev+staging+prod)
3. Datos de catálogo (tabla: tabla, fuente, actualización)
4. Datos de desarrollo (tabla: tabla, cantidad, herramienta de generación)
5. Dependencias de orden (qué tablas seedear primero por FK constraints)
6. Script de ejecución (comando, idempotencia, verificación)
7. Datos sensibles en seed (NO usar datos reales — solo fake)
8. Refresh strategy (cómo reset-ear seed data en desarrollo)

**Criterio de completitud:**
- [ ] Datos de sistema definidos (roles, permisos, configuraciones)
- [ ] Datos de catálogo definidos con fuente
- [ ] Datos de desarrollo especificados (cantidad, realismo)
- [ ] Orden de ejecución documentado (respeta FK constraints)
- [ ] Script idempotente (ejecutable múltiples veces sin duplicar)
- [ ] No incluye datos reales de personas (solo fake data)
- [ ] Instrucciones de ejecución claras

**Anti-patrones:**
- ❌ **Sin seed data:** Developer clona el repo y tiene que crear datos manualmente — pierde 2 horas antes de poder probar.
- ❌ **Datos reales en seed:** Copiar datos de producción como seed — violación de privacidad y posible leak de datos.
- ❌ **Seed no idempotente:** Ejecutar seed 2 veces crea duplicados — breaks la BD.
- ❌ **Sin orden de dependencias:** Intentar crear orders antes de users — FK constraint errors.
- ❌ **Seed de dev en producción:** Datos fake que accidentalmente se insertan en prod — "usuario Test McTestface" visible a clientes.

**Template:** `phases/03B-design-technical/deliverables/seed-data-plan.md` *(pendiente)*

---

### 3B.3.8 Backup Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.3 Database Design |
| **Responsable** | Database Engineer |
| **Ejecuta** | DevOps Lead / Database Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere experiencia en backup/restore de bases de datos en producción: tipos de backup (full, incremental, differential), herramientas (pg_dump, AWS RDS snapshots, Cloud SQL backups), y disaster recovery procedures.  
En VTT: un agente puede generar la estrategia de backup documentada basándose en el engine de BD y la infraestructura elegida. Puede producir scripts de backup/restore y documentar el proceso. NO puede tomar decisiones sobre RPO/RTO — esas dependen de requisitos de negocio. Necesita brief con: engine de BD, plataforma de hosting, RPO/RTO requeridos, volumen de datos, y budget para storage de backups.

**Qué es:** Documento que define cómo se respalda la base de datos: tipo de backup (full/incremental), frecuencia, retención, storage, encriptación, proceso de restore, y testing de backups. Incluye RPO (Recovery Point Objective — cuántos datos puedes perder) y RTO (Recovery Time Objective — cuánto puede durar el downtime).

**Para qué sirve:** Sin backups, un error humano (DROP TABLE), un fallo de hardware, o un ataque de ransomware significa pérdida total de datos. La estrategia define no solo los backups sino el proceso de restore — porque un backup que no se puede restaurar no es un backup. También define testing regular de restore para verificar que los backups funcionan.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — engine de BD
- `3B.8.1` Infrastructure Plan — plataforma de hosting
- `3B.8.8` Disaster Recovery Plan — RPO/RTO definidos
- Requisitos de negocio (cuántos datos se pueden perder, cuánto downtime es aceptable)

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)* — engine de BD
- `3B.3.2` Schema Definition *(obligatorio)* — qué se respalda
- `3B.8.1` Infrastructure Plan *(recomendado)* — storage para backups
- `3B.8.8` Disaster Recovery Plan *(recomendado)* — RPO/RTO

**Habilita (successors):**
- `6.3.1` Production Environment Setup — backups configurados en prod
- `7.2.1` Backup Verification — testing regular de backups
- `3B.8.8` Disaster Recovery Plan — backups como mecanismo de recovery

**Audiencia:**
- **DevOps Lead** — implementación y automatización de backups
- **Database Engineer** — configuración y testing
- **Tech Lead** — validación de strategy
- **CTO / Management** — RPO/RTO son decisiones de negocio

**Secciones esperadas:**
1. RPO y RTO definidos y aprobados por negocio
2. Tipo de backup (full, incremental, WAL archiving, snapshots)
3. Frecuencia (diario full, cada hora incremental, continuo WAL)
4. Retención (cuánto tiempo se guardan los backups: 7 días, 30 días, 1 año)
5. Storage de backups (ubicación, cross-region, encriptación)
6. Proceso de restore step-by-step (probado y documentado)
7. Testing de backups (frecuencia de restore tests, checklist de verificación)
8. Monitoring de backups (alertas si un backup falla)
9. Point-in-Time Recovery (PITR) si el engine lo soporta
10. Costos estimados de storage de backups

**Criterio de completitud:**
- [ ] RPO y RTO definidos con aprobación de negocio
- [ ] Tipo y frecuencia de backup documentados
- [ ] Retención definida
- [ ] Storage con encriptación
- [ ] Proceso de restore documentado step-by-step
- [ ] Testing de backups programado (al menos mensual)
- [ ] Monitoring y alerting configurados
- [ ] Costo estimado

**Anti-patrones:**
- ❌ **"Lo hace el cloud automáticamente":** Confiar en backups automáticos sin verificar configuración, retención, ni testear restore — falsa seguridad.
- ❌ **Backups sin restore testing:** Hacer backups religiosos que nunca se prueban — descubres que no funcionan cuando los necesitas.
- ❌ **Backups sin encriptación:** Datos sensibles en backups sin encriptar — violación de seguridad y compliance.
- ❌ **Sin monitoring:** El job de backup falla silenciosamente durante semanas — cuando necesitas restore, el último backup es de hace un mes.
- ❌ **RPO/RTO no discutidos con negocio:** El equipo técnico define 24h de RPO pero negocio necesita 1h — desalineación costosa.

**Template:** `phases/03B-design-technical/deliverables/backup-strategy.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.3 Database Design

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.3.1 ERD Complete | Database Engineer | Database Engineer | ✅ — puede generar ERD en Mermaid/dbdiagram a partir de entidades descritas |
| 3B.3.2 Schema Definition | Database Engineer | Database Engineer / Backend Developer | ✅ — puede generar schema completo en Prisma/SQL a partir del ERD |
| 3B.3.3 Table Specifications | Database Engineer | Database Engineer | ✅ — puede generar especificaciones detalladas de cada tabla |
| 3B.3.4 Index Strategy | Database Engineer | Database Engineer | 🔶 Parcial — puede proponer índices basándose en access patterns, pero tuning requiere profiling real |
| 3B.3.5 Data Dictionary | Database Engineer | Database Engineer / Technical Writer | ✅ — altamente delegable, es documentación estructurada |
| 3B.3.6 Migration Strategy | Database Engineer | Database Engineer / Backend Developer | ✅ — puede generar estrategia y scripts basándose en el ORM elegido |
| 3B.3.7 Seed Data Plan | Database Engineer | Database Engineer / Backend Developer | ✅ — puede generar plan y scripts de seed data completos |
| 3B.3.8 Backup Strategy | Database Engineer | DevOps Lead / Database Engineer | 🔶 Parcial — puede documentar estrategia, pero RPO/RTO son decisiones de negocio |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03B_04_API_DESIGN.md` — 11 deliverables (3B.4.1 a 3B.4.11)
