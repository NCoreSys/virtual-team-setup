# ESPECIFICACION - INDICE DE RUTEO GLOBAL DE DELIVERABLES SDLC

**Version:** 1.0  
**Fecha:** 2026-05-19  
**Proposito:** Definir el formato canonico para mapear cada deliverable del SDLC a sus documentos fuente, dependencias y set minimo de lectura para agentes VTT.  
**Alcance:** Todas las fases del framework SDLC de Virtual Teams: `0`, `1`, `2`, `3A`, `3B`, `4`, `5`, `6`, `7`.  
**Cobertura esperada:** `438 deliverables`, `43 documentos fuente de diccionario`.

---

## 1. Problema Que Resuelve

El ejemplo de Memory Service resolvia un caso puntual:
- un `task breakdown` tecnico,
- un conjunto acotado de deliverables de fases `4-7`,
- y decisiones `D-MEM-*` propias de un solo proyecto.

Para `Virtual Teams Setup` eso no alcanza.

Necesitamos un formato general que permita:
- mapear **todos** los deliverables del SDLC,
- desde **todas** las fases,
- contra su documento fuente real,
- con sus prerequisitos,
- y con el set minimo de documentos que un agente debe leer antes de ejecutar.

---

## 2. Principio De Normalizacion

El formato del PM se conserva, pero se vuelve generico.

### Formato original del ejemplo

| Deliverable ID | Nombre | Spec Source | Seccion | D-MEM aplicables | Docs para el agente |
|---|---|---|---|---|---|

### Formato canonico global

| Deliverable ID | Nombre | Spec Source | Seccion | Reglas aplicables | Docs para el agente |
|---|---|---|---|---|---|

### Cambio clave

`D-MEM aplicables` se reemplaza por `Reglas aplicables`, porque fuera de Memory Service no siempre existen decisiones `D-*`.

Ese campo debe aceptar cualquiera de estas clases de referencia:
- decisiones cerradas del proyecto: `D-XXX`
- reglas de negocio: `BR-XXX`
- requisitos funcionales: `RF-XXX`
- requisitos no funcionales: `NFR-XXX`
- criterios de aceptacion: `CA-XXX`
- politicas o SOPs del framework
- `N/A` si el deliverable no depende de una regla formal identificable

---

## 3. Definicion De Columnas

| Columna | Que poner | Regla |
|---------|-----------|-------|
| **Deliverable ID** | ID oficial del deliverable | Ej: `0.1.1`, `3A.4.2`, `4.3.7` |
| **Nombre** | Nombre oficial del deliverable | Debe coincidir con el diccionario |
| **Spec Source** | Documento fuente donde se define el deliverable | Normalmente el `DICCIONARIO_FASE_*` correspondiente |
| **Seccion** | Seccion exacta dentro del doc fuente | Preferir el heading del deliverable; usar `completo` solo si aplica a todo el documento |
| **Reglas aplicables** | Reglas, decisiones o constraints que el agente debe respetar | Puede ser `D-*`, `BR-*`, `RF-*`, `NFR-*`, `CA-*`, SOPs, o `N/A` |
| **Docs para el agente** | Set minimo de lectura antes de ejecutar | Debe incluir doc fuente + docs de inputs/prerequisitos relevantes |

---

## 4. Fuentes De Verdad Para Construir El Indice

En este repo ya existen las fuentes necesarias.

### 4.1 Catalogo estructurado

Archivo:
- `00-platform/02.normativa/catalogs/deliverables/deliverables_catalog.json`

Campos utiles ya presentes:
- `deliverable_id`
- `name`
- `source_file`
- `source_file_name`
- `inputs_required`
- `predecessors`
- `successors`
- `template_path`

### 4.2 Diccionarios de deliverables

Ubicacion:
- `00-platform/02.normativa/catalogs/deliverables/`

Cobertura actual:
- `DICCIONARIO_FASE_00_DISCOVERY.md`
- `DICCIONARIO_FASE_01_PLANNING.md`
- `DICCIONARIO_FASE_02_ANALYSIS.md`
- `DICCIONARIO_FASE_03A_01_USER_RESEARCH.md`
- `DICCIONARIO_FASE_03A_02_PERSONAS.md`
- `DICCIONARIO_FASE_03A_03_INFORMATION_ARCHITECTURE.md`
- `DICCIONARIO_FASE_03A_04_WIREFRAMES.md`
- `DICCIONARIO_FASE_03A_05_MOCKUPS.md`
- `DICCIONARIO_FASE_03A_06_PROTOTYPES.md`
- `DICCIONARIO_FASE_03A_07_DESIGN_SYSTEM.md`
- `DICCIONARIO_FASE_03A_08_USABILITY_TESTING.md`
- `DICCIONARIO_FASE_03A_09_DESIGN_HANDOFF.md`
- `DICCIONARIO_FASE_03B_01_SOLUTION_ARCHITECTURE.md`
- `DICCIONARIO_FASE_03B_02_CODE_ARCHITECTURE.md`
- `DICCIONARIO_FASE_03B_03_DATABASE_DESIGN.md`
- `DICCIONARIO_FASE_03B_04_API_DESIGN.md`
- `DICCIONARIO_FASE_03B_05_SEQUENCE_DIAGRAMS.md`
- `DICCIONARIO_FASE_03B_06_ADR.md`
- `DICCIONARIO_FASE_03B_07_SECURITY_PLAN.md`
- `DICCIONARIO_FASE_03B_08_INFRASTRUCTURE_PLAN.md`
- `DICCIONARIO_FASE_03B_09_TECHNICAL_ESTIMATES.md`
- `DICCIONARIO_FASE_04_01_ENVIRONMENT_SETUP.md`
- `DICCIONARIO_FASE_04_02_DATABASE_IMPLEMENTATION.md`
- `DICCIONARIO_FASE_04_03_BACKEND_DEVELOPMENT.md`
- `DICCIONARIO_FASE_04_04_FRONTEND_DEVELOPMENT.md`
- `DICCIONARIO_FASE_04_05_INTEGRATIONS.md`
- `DICCIONARIO_FASE_04_06_UNIT_TESTS.md`
- `DICCIONARIO_FASE_04_07_TECHNICAL_DOCUMENTATION.md`
- `DICCIONARIO_FASE_04_08_CODE_REVIEW.md`
- `DICCIONARIO_FASE_05_01_TEST_PLANNING.md`
- `DICCIONARIO_FASE_05_02_TEST_CASES.md`
- `DICCIONARIO_FASE_05_03_TEST_ENVIRONMENT.md`
- `DICCIONARIO_FASE_05_04_FUNCTIONAL_TESTING.md`
- `DICCIONARIO_FASE_05_05_INTEGRATION_TESTING.md`
- `DICCIONARIO_FASE_05_06_E2E_TESTING.md`
- `DICCIONARIO_FASE_05_07_PERFORMANCE_TESTING.md`
- `DICCIONARIO_FASE_05_08_SECURITY_TESTING.md`
- `DICCIONARIO_FASE_05_09_ACCESSIBILITY_TESTING.md`
- `DICCIONARIO_FASE_05_10_UAT.md`
- `DICCIONARIO_FASE_05_11_BUG_FIXES.md`
- `DICCIONARIO_FASE_06_DEPLOY.md`
- `DICCIONARIO_FASE_07_PARTE1_MONITORING_SUPPORT_BUGFIXES.md`
- `DICCIONARIO_FASE_07_PARTE2_IMPROVEMENTS_SECURITY_SCALING.md`

### 4.3 Analisis maestro de fases

Archivo:
- `ANALISIS_FASES_COMPLETO_PARA_PM.md`

Uso:
- validar conteos,
- validar nombres oficiales,
- validar la estructura total de fases y subfases.

---

## 5. Regla De Mapeo

Cada fila del indice global se construye asi:

1. `Deliverable ID`
   - sale del identificador oficial del deliverable en el diccionario o catalogo.

2. `Nombre`
   - sale del nombre oficial del deliverable en el diccionario o catalogo.

3. `Spec Source`
   - sale de `source_file_name` del catalogo.
   - si hay conflicto, gana el archivo de diccionario donde vive el heading del deliverable.

4. `Seccion`
   - por defecto es el heading del deliverable dentro del diccionario.
   - si el deliverable depende de una subseccion muy puntual, se puede refinar con `§...`.
   - usar `completo` solo si el documento entero aplica como fuente.

5. `Reglas aplicables`
   - se llena con referencias formales del proyecto o del framework.
   - si el framework aun no tiene decision IDs o rule IDs para ese deliverable, usar `N/A`.
   - no inventar IDs.

6. `Docs para el agente`
   - debe incluir siempre el `Spec Source`.
   - debe incluir los docs fuente de los `predecessors` o `inputs_required` que sean obligatorios o claramente relevantes.
   - puede incluir el `template_path` como artefacto operativo adicional, pero no sustituye al doc fuente.

---

## 6. Regla Especial Para "Docs Para El Agente"

Esta columna no es "todo lo relacionado". Es el set minimo y accionable.

Debe priorizar:
- el diccionario donde se define el deliverable,
- los docs de inputs obligatorios,
- los docs de dependencias marcadas como `obligatorio`,
- y solo despues docs complementarios.

No debe incluir:
- listas gigantes de documentos irrelevantes,
- docs de la fase completa cuando basta una subfase,
- referencias genericas tipo `leer todo el proyecto`.

---

## 7. Ejemplos De Adaptacion Global

### 7.1 Discovery

| Deliverable ID | Nombre | Spec Source | Seccion | Reglas aplicables | Docs para el agente |
|---|---|---|---|---|---|
| 0.1.1 | Market Research Report | DICCIONARIO_FASE_00_DISCOVERY.md | 0.1.1 Market Research Report | N/A | DICCIONARIO_FASE_00_DISCOVERY.md |
| 0.3.1 | Problem Statement | DICCIONARIO_FASE_00_DISCOVERY.md | 0.3.1 Problem Statement | N/A | DICCIONARIO_FASE_00_DISCOVERY.md, DICCIONARIO_FASE_00_DISCOVERY.md |

### 7.2 Analysis

| Deliverable ID | Nombre | Spec Source | Seccion | Reglas aplicables | Docs para el agente |
|---|---|---|---|---|---|
| 2.1.1 | SRS Document | DICCIONARIO_FASE_02_ANALYSIS.md | 2.1.1 SRS Document | RF-*, BR-* segun proyecto | DICCIONARIO_FASE_02_ANALYSIS.md |
| 2.7.1 | Acceptance Criteria Doc | DICCIONARIO_FASE_02_ANALYSIS.md | 2.7.1 Acceptance Criteria Doc | CA-* segun proyecto | DICCIONARIO_FASE_02_ANALYSIS.md, DICCIONARIO_FASE_02_ANALYSIS.md |

### 7.3 Design Technical

| Deliverable ID | Nombre | Spec Source | Seccion | Reglas aplicables | Docs para el agente |
|---|---|---|---|---|---|
| 3B.9.3 | Task Breakdown | DICCIONARIO_FASE_03B_09_TECHNICAL_ESTIMATES.md | 3B.9.3 Task Breakdown | N/A o decisiones del proyecto | DICCIONARIO_FASE_03B_09_TECHNICAL_ESTIMATES.md, DICCIONARIO_FASE_03B_04_API_DESIGN.md, DICCIONARIO_FASE_03B_03_DATABASE_DESIGN.md, DICCIONARIO_FASE_03B_02_CODE_ARCHITECTURE.md |

### 7.4 Development

| Deliverable ID | Nombre | Spec Source | Seccion | Reglas aplicables | Docs para el agente |
|---|---|---|---|---|---|
| 4.3.1 | API Endpoints | DICCIONARIO_FASE_04_03_BACKEND_DEVELOPMENT.md | 4.3.1 API Endpoints | RF-*, BR-*, NFR-* segun proyecto | DICCIONARIO_FASE_04_03_BACKEND_DEVELOPMENT.md, DICCIONARIO_FASE_03B_04_API_DESIGN.md |

---

## 8. Artefactos Que Debemos Tener

Para operar bien a nivel framework conviene separar dos niveles:

### 8.1 Indice maestro de deliverables

Archivo sugerido:
- `INDICE_RUTEO_DELIVERABLES_SDLC.md`

Contenido:
- una fila por deliverable,
- cobertura total de los `438` deliverables.

### 8.2 Matriz de documentos fuente

Archivo sugerido:
- `MATRIZ_DOCUMENTOS_FUENTE_SDLC.md`

Contenido:
- una fila por documento fuente,
- cobertura de los `43` diccionarios,
- con fase, subfase, rango de deliverables y rol owner.

La matriz de documentos fuente sirve para auditar.
El indice de ruteo sirve para operar.

---

## 9. Orden Recomendado De Construccion

1. Construir la `MATRIZ_DOCUMENTOS_FUENTE_SDLC.md`.
2. Generar luego el `INDICE_RUTEO_DELIVERABLES_SDLC.md`.
3. Empezar por fases de mayor uso operativo:
   - `4 Development`
   - `3A Design UX/UI`
   - `3B Design Technical`
   - `5 Testing`
4. Completar luego:
   - `0 Discovery`
   - `1 Planning`
   - `2 Analysis`
   - `6 Deploy`
   - `7 Operations`

---

## 10. Decision Operativa

Para `Virtual Teams Setup`, este debe ser el criterio vigente:

- el caso de Memory Service es un ejemplo local, no la norma global;
- el formato correcto para el framework es el de este documento;
- el campo de decisiones debe ser generico, no amarrado a `D-MEM-*`;
- el mapeo debe salir del catalogo y de los diccionarios, no de memoria del TL.

---

## 11. Siguiente Entregable Recomendado

El siguiente paso natural no es empezar "a mano" con 438 filas.

El siguiente artefacto a producir deberia ser:
- `MATRIZ_DOCUMENTOS_FUENTE_SDLC.md`

Porque ese archivo define:
- que documentos existen,
- que rango de deliverables cubre cada uno,
- y desde ahi ya se puede expandir el indice fila por fila sin inventar rutas.

---

**Estado:** Base lista para iniciar el mapeo global de deliverables del SDLC.
