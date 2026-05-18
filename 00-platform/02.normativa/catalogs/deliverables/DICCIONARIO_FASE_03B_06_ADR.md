# DICCIONARIO DE DELIVERABLES — FASE 3B.6: ADR (ARCHITECTURE DECISION RECORDS)

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.6 — ADR (Architecture Decision Records)  
**Total deliverables:** 4  
**Responsable de subfase:** Solution Architect  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Los Architecture Decision Records (ADRs) documentan las decisiones técnicas importantes del proyecto: qué se decidió, por qué, qué alternativas se evaluaron, y qué consecuencias tiene la decisión. Son la "memoria institucional" del proyecto técnico. Sin ADRs, cada 6 meses alguien pregunta "¿por qué usamos PostgreSQL y no MongoDB?" y nadie recuerda — o peor, se rediscute la decisión sin nueva información.

**Prerequisitos de subfase:**
- Decisiones técnicas tomadas en las subfases anteriores (3B.1-3B.5)
- Technology Stack definido (3B.1.5)

**Entrega de subfase:**
- Colección de ADRs que documentan las decisiones técnicas principales, indexada y mantenible

---

### 3B.6.1 ADR Template

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.6 ADR |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect |
| **Aprueba** | Tech Lead |
| **Formato** | MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de la estructura de ADRs (Michael Nygard format o variantes) y juicio sobre qué nivel de detalle incluir.  
En VTT: un agente puede generar el template de ADR basado en el formato estándar de la industria (Nygard, Madr, o variante custom). Es altamente delegable — es un template, no una decisión. Necesita brief con: formato preferido (Nygard, Madr, custom), secciones obligatorias vs opcionales, y metadata requerida.

**Qué es:** Template estandarizado que se usa para documentar cada decisión arquitectónica. Define las secciones que toda ADR debe tener: título, status, contexto, decisión, alternativas evaluadas, consecuencias, y metadata. Es el formato que se copia cada vez que se documenta una nueva decisión.

**Para qué sirve:** Garantiza que todas las ADRs tienen la misma estructura, el mismo nivel de detalle, y son comparables entre sí. Sin template, cada ADR tiene un formato diferente: una es un párrafo, otra una tabla, otra un email reenviado. El template estandariza la calidad de documentación.

**Inputs requeridos:**
- Formato de ADR elegido (Nygard, Madr, custom)
- Convenciones de naming (ADR-001, ADR-002, ...)

**Dependencias (predecessors):**
- Ninguna — es un template, puede crearse en cualquier momento

**Habilita (successors):**
- `3B.6.3` ADR Documents — cada ADR usa este template
- `3B.6.2` ADR Index — ADRs indexables porque comparten estructura

**Audiencia:**
- **Solution Architect** — usa el template para cada ADR
- **Tech Lead** — valida que las ADRs siguen el template
- **Todo el equipo técnico** — sabe qué esperar en cada ADR

**Secciones esperadas (del template):**
1. **Title:** ADR-NNN: Título descriptivo de la decisión
2. **Status:** Proposed / Accepted / Deprecated / Superseded by ADR-XXX
3. **Date:** Fecha de la decisión
4. **Context:** Cuál es el problema o la necesidad que requiere una decisión
5. **Decision:** Qué se decidió (statement claro)
6. **Alternatives Considered:** Opciones evaluadas con pros/cons
7. **Consequences:** Qué implica la decisión (positivo y negativo)
8. **Participants:** Quiénes participaron en la decisión
9. **Related ADRs:** Referencias a ADRs relacionadas

**Criterio de completitud:**
- [ ] Template creado con todas las secciones definidas
- [ ] Naming convention documentada (ADR-001, ADR-002, ...)
- [ ] Status values definidos (Proposed, Accepted, Deprecated, Superseded)
- [ ] Ejemplo de ADR completa usando el template
- [ ] Ubicación de los archivos de ADR definida (e.g., `/docs/adr/`)

**Anti-patrones:**
- ❌ **Template demasiado complejo:** 15 secciones obligatorias — nadie llena ADRs porque es mucho trabajo.
- ❌ **Template demasiado simple:** Solo "Decision: usamos X" — no documenta el por qué ni las alternativas.
- ❌ **Sin ejemplo:** Template vacío sin una ADR de ejemplo — nadie sabe qué nivel de detalle esperar.

**Template:** `phases/03B-design-technical/deliverables/adr-template.md` *(pendiente)*

---

### 3B.6.2 ADR Index

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.6 ADR |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect |
| **Aprueba** | Tech Lead |
| **Formato** | Lista (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Continua (se actualiza con cada ADR nueva) |

**Perfil de ejecución:** Requiere disciplina de mantener el índice actualizado cada vez que se agrega, depreca, o supersede una ADR.  
En VTT: un agente puede generar y mantener el índice de ADRs automáticamente a partir de los archivos de ADR. Es altamente delegable. Necesita brief con: lista de ADRs existentes con metadata (número, título, status, fecha).

**Qué es:** Archivo índice que lista todas las ADRs del proyecto en orden cronológico o por categoría: número, título, status, fecha, y categoría. Es la tabla de contenidos de todas las decisiones arquitectónicas del proyecto. Se mantiene actualizado cada vez que se agrega o modifica una ADR.

**Para qué sirve:** Sin índice, hay que buscar en una carpeta de archivos para encontrar una ADR. El índice permite: ver todas las decisiones de un vistazo, filtrar por status (qué está accepted, qué deprecated), buscar por categoría (database, auth, infra), y verificar que no se duplican decisiones.

**Inputs requeridos:**
- `3B.6.3` ADR Documents — ADRs a indexar
- Categorías de decisiones (database, infrastructure, auth, API, frontend)

**Dependencias (predecessors):**
- `3B.6.1` ADR Template *(obligatorio)* — estructura que permite indexar
- `3B.6.3` ADR Documents *(obligatorio)* — documentos a indexar

**Habilita (successors):**
- Navegación rápida a cualquier ADR
- Detección de decisiones duplicadas o conflictivas

**Audiencia:**
- **Todo el equipo técnico** — punto de entrada a las ADRs
- **New team members** — "lee las ADRs" empieza aquí

**Secciones esperadas:**
1. Tabla de ADRs (número, título, status, fecha, categoría, link)
2. Filtro por status (accepted, deprecated, superseded)
3. Agrupación por categoría (opcional)
4. Instrucciones para agregar nuevas ADRs
5. Total de ADRs por status

**Criterio de completitud:**
- [ ] Todas las ADRs existentes indexadas
- [ ] Metadata correcta (número, título, status, fecha)
- [ ] Links a cada ADR funcionales
- [ ] Instrucciones para agregar nuevas ADRs
- [ ] Actualizado al momento de la última ADR

**Anti-patrones:**
- ❌ **Índice desactualizado:** ADRs nuevas que no se agregan al índice — el índice pierde confiabilidad.
- ❌ **Sin status:** Todas las ADRs en la lista sin indicar cuáles están vigentes y cuáles deprecadas.
- ❌ **Sin categorías:** 30 ADRs en una lista plana sin agrupación — difícil de navegar.

**Template:** `phases/03B-design-technical/deliverables/adr-index.md` *(pendiente)*

---

### 3B.6.3 ADR Documents

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.6 ADR |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | MD por ADR |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día por ADR (5-10 ADRs iniciales = 3-5 días) |
| **Frecuencia** | Una vez + nuevas ADRs cuando surgen decisiones |

**Perfil de ejecución:** Requiere la capacidad de articular una decisión técnica con: contexto que la motivó, alternativas evaluadas con pros/cons objetivos, y consecuencias anticipadas. Debe ser objetivo y factual, no un argumento de venta de la opción elegida.  
En VTT: un agente puede redactar ADRs completas a partir de la justificación del Solution Architect. Puede también investigar pros/cons de alternativas tecnológicas. Es bastante delegable si el Architect provee la decisión y el contexto. Necesita brief con: qué se decidió, por qué, qué alternativas se evaluaron, y qué consecuencias tiene.

**Qué es:** Colección de documentos individuales de ADR, cada uno documentando una decisión técnica importante. Las ADRs iniciales típicas incluyen: elección de base de datos, elección de framework backend, elección de framework frontend, estrategia de autenticación, modelo de deployment, estrategia de testing, y herramienta de CI/CD. Cada ADR sigue el template (3B.6.1).

**Para qué sirve:** Son la memoria del proyecto. Cuando en 6 meses alguien pregunta "¿por qué elegimos cursor pagination en vez de offset?" la ADR responde: contexto, alternativas, y razones. Cuando se revisa una decisión, la ADR proporciona el baseline: "esto se decidió por X razones — ¿han cambiado esas razones?". También protegen contra la rotación de equipo — las decisiones no se van con las personas.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — decisiones de stack como ADRs
- `3B.1.1` Architecture Document — decisiones arquitectónicas
- `3B.4.4` Pagination Strategy — decisión de paginación como ADR
- `3B.4.6` Authentication Spec — decisión de auth como ADR
- Cualquier decisión técnica significativa del proyecto

**Dependencias (predecessors):**
- `3B.6.1` ADR Template *(obligatorio)* — formato a seguir
- Decisiones técnicas tomadas en subfases 3B.1-3B.5

**Habilita (successors):**
- `3B.6.2` ADR Index — ADRs indexadas
- `3B.6.4` Decision Log — decisiones resumidas
- Futuras revisiones de decisiones — baseline documentado

**Audiencia:**
- **Todo el equipo técnico** — consulta de decisiones
- **New team members** — entender por qué el sistema es como es
- **Solution Architect** — referencia propia y para futuras decisiones
- **Management** — visibilidad de decisiones técnicas (si lo requieren)

**Secciones esperadas (ADRs iniciales típicas):**
1. ADR-001: Elección de base de datos
2. ADR-002: Elección de framework backend
3. ADR-003: Elección de framework frontend
4. ADR-004: Estrategia de autenticación
5. ADR-005: Modelo de deployment (monolith, microservices, serverless)
6. ADR-006: Estrategia de testing
7. ADR-007: Herramienta de CI/CD
8. ADR-008: ORM / Data access layer
9. ADR-009: API style (REST, GraphQL, gRPC)
10. ADR-010: Estrategia de state management (frontend)
(La lista varía por proyecto — estas son las más comunes)

**Criterio de completitud:**
- [ ] Al menos 5 ADRs iniciales documentadas
- [ ] Cada ADR sigue el template (3B.6.1)
- [ ] Cada ADR tiene al menos 2 alternativas evaluadas
- [ ] Consecuencias documentadas (positivas y negativas)
- [ ] Status de cada ADR definido (Accepted para las iniciales)
- [ ] ADRs indexadas en 3B.6.2

**Anti-patrones:**
- ❌ **ADR como justificación post-hoc:** Escribir la ADR después de implementar para "documentar" lo que ya se hizo — pierde el valor de la deliberación.
- ❌ **Solo una alternativa:** "Decidimos usar PostgreSQL. No evaluamos otras opciones." — no es una decisión, es una imposición.
- ❌ **Sin consecuencias negativas:** Toda decisión tiene trade-offs — documentar solo lo positivo es dishonesto.
- ❌ **ADRs nunca revisadas:** Decisiones de hace 2 años que ya no aplican pero siguen como "Accepted" — deberían ser Deprecated o Superseded.
- ❌ **Nivel de detalle inconsistente:** Una ADR de 3 párrafos y otra de 5 páginas — falta de estándar.

**Template:** `phases/03B-design-technical/deliverables/adr/` *(pendiente)*

---

### 3B.6.4 Decision Log

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.6 ADR |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día + actualización continua |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere disciplina de registro — cada decisión técnica significativa se registra, no solo las que ameritan una ADR completa.  
En VTT: un agente puede mantener el decision log actualizado recibiendo inputs del equipo técnico. Es altamente delegable. Necesita brief con: decisiones tomadas (nombre, fecha, participantes, outcome).

**Qué es:** Registro cronológico de todas las decisiones técnicas del proyecto, incluyendo las que no ameritan una ADR completa. Es más ligero que una ADR: una tabla con fecha, decisión, participantes, resultado, y referencia a ADR si existe. Captura decisiones de sprint (qué library usar, qué pattern aplicar) que no son arquitectónicas pero sí relevantes.

**Para qué sirve:** Las ADRs capturan decisiones grandes. El decision log captura todo lo demás: "decidimos usar date-fns en vez de moment.js", "decidimos no implementar WebSockets en MVP", "decidimos usar Zod para validación". Son decisiones que no ameritan una ADR pero que sí conviene recordar. También sirve como "agenda" de decisiones pendientes.

**Inputs requeridos:**
- Decisiones tomadas en reuniones técnicas
- Sprint planning decisions
- Code review decisions (patterns, libraries)
- `3B.6.3` ADR Documents — decisiones grandes referenciadas

**Dependencias (predecessors):**
- `3B.6.1` ADR Template *(recomendado)* — para saber qué es ADR vs decision log entry
- Reuniones técnicas del proyecto

**Habilita (successors):**
- Referencia rápida de decisiones menores
- Input para futuras ADRs (una decisión del log puede promover a ADR)
- Onboarding de nuevos developers

**Audiencia:**
- **Todo el equipo técnico** — consulta rápida
- **Tech Lead** — tracking de decisiones
- **New team members** — entiende decisiones pasadas rápidamente

**Secciones esperadas:**
1. Tabla de decisiones (fecha, decisión, categoría, participantes, outcome, ADR ref)
2. Filtro por categoría (backend, frontend, infra, testing, tooling)
3. Decisiones pendientes (backlog de decisiones por tomar)
4. Instrucciones para agregar entradas

**Criterio de completitud:**
- [ ] Todas las decisiones técnicas significativas registradas
- [ ] Fecha y participantes incluidos
- [ ] Referencia a ADR cuando existe
- [ ] Decisiones pendientes identificadas
- [ ] Actualizado regularmente (al menos por sprint)

**Anti-patrones:**
- ❌ **Solo ADRs, no log:** Solo documentar las decisiones "grandes" y perder las medianas — el 80% de las decisiones son medianas.
- ❌ **Log no actualizado:** Llenarlo la primera semana y abandonarlo — pierde su propósito.
- ❌ **Demasiado detalle:** Convertir cada entrada del log en una ADR — el log es un registro rápido, no un documento exhaustivo.
- ❌ **Sin decisiones pendientes:** No registrar qué falta decidir — las decisiones se difieren indefinidamente.

**Template:** `phases/03B-design-technical/deliverables/decision-log.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.6 ADR

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.6.1 ADR Template | Solution Architect | Solution Architect | ✅ — puede generar template estándar |
| 3B.6.2 ADR Index | Solution Architect | Solution Architect | ✅ — puede generar y mantener el índice automáticamente |
| 3B.6.3 ADR Documents | Solution Architect | Solution Architect / Tech Lead | 🔶 Parcial — puede redactar ADRs con input del Architect, no puede tomar las decisiones |
| 3B.6.4 Decision Log | Solution Architect | Solution Architect / Tech Lead | ✅ — puede mantener el log actualizado recibiendo inputs del equipo |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03B_07_SECURITY_PLAN.md` — 11 deliverables (3B.7.1 a 3B.7.11)
