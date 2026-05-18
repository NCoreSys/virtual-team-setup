# Framework Base de Arquitectura de Software para la Aplicación

## Curso 01 — Fundamentos de Arquitectura de Software

## 1. Propósito del documento

Este documento consolida la primera extracción metodológica del curso **Fundamentos de Arquitectura de Software**, perteneciente a la **Escuela de Desarrollo Web** y a la ruta **15 Arquitecturas Web Modernas y Escalabilidad**.

El objetivo no es resumir el curso, sino transformar su contenido en un framework operativo para la aplicación.

La aplicación no debe funcionar como un generador simple de pantallas o código. Debe funcionar como una **capa de inteligencia arquitectónica para desarrollo asistido por IA**, capaz de convertir una idea en un sistema diagnosticado, justificado, documentado, gobernable y evolutivo.

---

# 2. Tesis central del curso aplicada a la aplicación

La tesis central derivada del curso es:

**Antes de generar código, la aplicación debe ayudar a entender, justificar, diseñar, validar y evolucionar la arquitectura del sistema.**

Esto diferencia a la aplicación de herramientas que operan bajo el flujo:

**prompt → pantalla/app → iteración visual → deploy**

La aplicación debe operar bajo un flujo más profundo:

**problema → diagnóstico → requisitos → riesgos → costos → estrategia → arquitectura → diseño interno → evolución → documentos vivos → agentes gobernados**

El diferenciador estratégico es:

**La capa de arquitectura que falta entre el prompt y el código.**

---

# 3. Flujo metodológico completo

El framework derivado del curso se organiza en cinco pilares y una capa transversal.

## Pilares

1. **Diagnóstico Arquitectónico Inicial**
2. **Frugalidad Arquitectónica y Alineación Estratégica**
3. **Selección de Estilo Arquitectónico**
4. **Diseño Interno y Limpieza Arquitectónica**
5. **Evolución Arquitectónica de MVP a Producto**

## Capa transversal

6. **Comunicación Arquitectónica y Preguntas de Descubrimiento**

La capa transversal atraviesa todos los pilares. No ocurre solo al inicio ni al final.

---

# 4. Pilar 1 — Diagnóstico Arquitectónico Inicial

## Pregunta central

**¿Qué problema estamos resolviendo realmente?**

## Función

Evitar que la aplicación salte directamente de una idea a una implementación sin entender primero el problema, el contexto, los riesgos, las restricciones y las decisiones asumidas.

## Problema que resuelve

Muchas herramientas de generación con IA empiezan cuando el usuario ya pide una solución:

- “Hazme una app.”
- “Hazme un CRM.”
- “Hazme microservicios.”
- “Hazme una plataforma con IA.”

El Pilar 1 obliga a retroceder y preguntar:

- ¿Qué problema real hay detrás?
- ¿Quién lo tiene?
- ¿Cómo se resuelve hoy?
- ¿Qué pasa si no se resuelve?
- ¿Qué solución está siendo asumida sin validación?

## Capacidades principales

### 1. Architecture Intake Wizard

Asistente inicial para capturar problema, actores, contexto, restricciones, riesgos y supuestos antes de generar solución.

### 2. Problem/Solution Separator

Módulo para detectar cuando el usuario mezcla problema con solución.

Ejemplo:

> “Necesitamos un microservicio de detección de fraude.”

La aplicación debe reformular:

> “Primero definamos qué significa fraude, cómo se detecta hoy, qué errores son aceptables, qué volumen existe y qué restricciones regulatorias aplican.”

### 3. Essential vs Incidental Classifier

Clasificador de problemas esenciales e incidentales.

Problemas esenciales:

- Complejidad
- Conformidad
- Tolerancia al cambio
- Invisibilidad/incertidumbre

Problemas incidentales:

- Codificar
- Testear
- Desplegar
- Configurar

### 4. Architecture Decision Logger

Registro inicial de decisiones arquitectónicas, alternativas, trade-offs, riesgos y consecuencias.

### 5. Fitness Function Builder

Generador de validaciones arquitectónicas iniciales para verificar que la arquitectura siga cumpliendo sus objetivos.

## Documentos vivos generados

- Architecture Brief
- Problem Definition Document
- Solution Options Document
- ARCHITECTURE.md
- ADR Log
- Architecture Risk Register

## Regla estratégica

**La aplicación no debe permitir pasar directamente a implementación si el problema no está definido y separado de la solución.**

---

# 5. Pilar 2 — Frugalidad Arquitectónica y Alineación Estratégica

## Pregunta central

**¿La solución es sostenible, costeable y coherente con el negocio?**

## Función

Evaluar requisitos funcionales, requisitos no funcionales, riesgos, restricciones, costos, criticidad de cargas y estrategia empresarial antes de seleccionar una arquitectura.

## Problema que resuelve

Muchas soluciones generadas con IA funcionan en demo, pero no son sostenibles porque nadie evaluó:

- Costo de operación
- Requisitos no funcionales
- Riesgos
- Restricciones
- Criticidad de cargas
- Estrategia de negocio
- Costo humano
- Dependencias externas

## Capacidades principales

### 1. NFR Profiler

Módulo para capturar requisitos no funcionales:

- Disponibilidad
- Seguridad
- Privacidad
- Rendimiento
- Escalabilidad
- Mantenibilidad
- Extensibilidad
- Usabilidad
- Observabilidad
- Resiliencia
- Compliance
- Tolerancia a errores

### 2. Risk & Constraint Register

Registro vivo de riesgos y restricciones.

### 3. Cost & Operation Estimator

Estimador cualitativo o cuantitativo de:

- CAPEX
- OPEX
- Costo humano
- Costo de capacitación
- Costo de observabilidad
- Costo de mantenimiento
- Costos ocultos

### 4. Workload Criticality Mapper

Clasificador de cargas:

- Críticas
- Importantes
- Accesorias

### 5. Strategy Alignment Matrix

Matriz para conectar arquitectura con estrategia:

- Exploración
- Expansión
- Ahorro

Y dimensiones de ingreso:

- Ventaja competitiva
- Regulación
- Disponibilidad
- Cumplimiento

### 6. Ubiquitous Language Builder

Constructor de glosario vivo entre negocio, tecnología y agentes.

### 7. Innovation Review Assistant

Revisor de innovación para evaluar nuevas herramientas, frameworks o propuestas de IA antes de adoptarlas.

## Documentos vivos generados

- NFR Specification
- Risk & Constraint Register
- Cost Model / TCO Document
- Workload Criticality Map
- Business & Architecture Alignment Document
- Ubiquitous Language Glossary

## Regla estratégica

**La arquitectura correcta no es la más sofisticada; es la que resuelve el problema con calidad suficiente, costo sostenible y alineación estratégica.**

---

# 6. Pilar 3 — Selección de Estilo Arquitectónico

## Pregunta central

**¿Qué estilo arquitectónico conviene y por qué?**

## Función

Seleccionar entre cliente-servidor, capas, monolito, monolito modular, servicios, eventos, microservicios o arquitectura híbrida con base en contexto, no en moda.

## Problema que resuelve

Los modelos suelen recomendar arquitecturas sin suficiente justificación:

> “Usemos microservicios con Node.js, PostgreSQL, Redis, Docker, Kubernetes y API Gateway.”

Pero no preguntan:

- ¿Cuántos equipos hay?
- ¿Qué dominios están separados?
- ¿Qué necesita desplegarse por separado?
- ¿Qué costo operativo introduce?
- ¿Existe observabilidad suficiente?
- ¿Un monolito modular sería suficiente?

## Capacidades principales

### 1. Architectural Style Selector

Motor de recomendación de estilo arquitectónico según:

- Tamaño del problema
- Complejidad del dominio
- Tamaño del equipo
- Número de equipos
- Necesidad de escalamiento
- Necesidad de despliegue independiente
- Necesidad de integración externa
- NFRs
- Restricciones
- Costo operativo aceptable

### 2. Architecture Trade-off Matrix

Matriz comparativa de estilos arquitectónicos.

### 3. Monolith Modularity Checklist

Checklist para evaluar si un monolito simple o modular es suficiente.

### 4. Service Contract Readiness Checklist

Checklist para validar servicios, contratos, consumidores, proveedores y versionamiento.

### 5. Event-Driven Readiness Checklist

Checklist para validar eventos, productores, consumidores, payloads, consistencia, orden y trazabilidad.

### 6. Microservices Readiness Assessment

Evaluación formal de madurez para microservicios.

### 7. Distributed Complexity Warning System

Sistema de alertas para detectar complejidad distribuida innecesaria.

### 8. Architecture Style ADR Generator

Generador de ADR para documentar la selección de estilo arquitectónico.

## Documentos vivos generados

- Architecture Style Decision Matrix
- Architecture Style ADR
- Architectural Trade-off Register
- Distributed Complexity Risk Register
- Service Contract Inventory
- Event Catalog

## Regla estratégica

**No existe un estilo arquitectónico universalmente mejor. Cada estilo introduce restricciones, costos y beneficios. La decisión correcta depende del contexto.**

---

# 7. Pilar 4 — Diseño Interno y Limpieza Arquitectónica

## Pregunta central

**¿La arquitectura elegida está bien diseñada por dentro?**

## Función

Evaluar responsabilidades, dependencias, contratos, reglas de negocio, patrones, SOLID, arquitectura limpia y testabilidad.

## Problema que resuelve

El código generado puede funcionar, pero estar mal estructurado:

- Lógica de negocio en UI
- Servicios con demasiadas responsabilidades
- DTOs con lógica indebida
- Casos de uso acoplados a base de datos
- Dependencias directas a frameworks
- Interfaces demasiado grandes
- Patrones usados sin necesidad
- Módulos con múltiples razones de cambio

## Capacidades principales

### 1. SOLID Review Checklist

Checklist para revisar responsabilidad única, apertura/cierre, sustitución de Liskov, segregación de interfaces e inversión de dependencias.

### 2. Clean Architecture Fitness Checklist

Checklist para evaluar separación de capas, dominio, casos de uso, adaptadores, infraestructura, UI y persistencia.

### 3. Dependency Direction Map

Mapa de dirección de dependencias.

### 4. Business Rules Isolation Checker

Validador de aislamiento de reglas de negocio.

### 5. Pattern Recommendation Matrix

Recomendador de patrones según contexto y problema específico.

### 6. Anti-pattern Detector

Detector de señales de mala estructura:

- Lógica en UI
- DTOs con lógica
- Servicios gigantes
- Controladores pesados
- Dependencia excesiva de framework
- Interfaces infladas
- Abstracciones innecesarias

### 7. Architecture Cleanliness Score

Métrica cualitativa de limpieza arquitectónica.

### 8. Internal Design ADR Generator

Generador de ADRs para decisiones de diseño interno.

## Documentos vivos generados

- Internal Design Review Report
- SOLID Compliance Checklist
- Clean Architecture Evaluation
- Dependency Map
- Pattern Decision Log
- Anti-pattern Register

## Regla estratégica

**No basta con que el software funcione; debe estar diseñado para cambiar.**

---

# 8. Pilar 5 — Evolución Arquitectónica de MVP a Producto

## Pregunta central

**¿La arquitectura actual todavía sirve o necesita evolucionar?**

## Función

Evaluar cómo debe evolucionar la arquitectura cuando cambian el alcance, los usuarios, los roles, las funcionalidades, los costos, los requisitos no funcionales o el modelo de negocio.

## Problema que resuelve

Un MVP puede crecer sin revisión arquitectónica hasta volverse frágil:

- Se agregan features sin evaluar impacto
- Aparecen nuevos roles sin permisos claros
- Se acumulan integraciones externas
- Suben costos sin control
- Cambian NFRs
- El producto pasa a clientes externos
- Se necesita multiusuario o multi-tenant
- La arquitectura inicial ya no soporta el nuevo uso

## Capacidades principales

### 1. MVP Architecture Fit Review

Evalúa si el MVP resuelve el problema principal con mínima complejidad razonable.

### 2. Scope Reduction Matrix

Matriz para decidir qué entra y qué no entra en el MVP.

### 3. Evolution Readiness Assessment

Evaluación para decidir si mantener, evolucionar, modularizar o rearquitectar.

### 4. Build vs External Tool Decision Log

Registro de decisiones entre construir internamente o usar herramienta externa.

### 5. Dependency Abstraction Map

Mapa de dependencias externas y cómo abstraerlas.

### 6. Enterprise Transition Checklist

Checklist para evaluar transición a producto empresarial.

### 7. Role Evolution Map

Mapa de evolución de actores, roles, permisos y responsabilidades.

### 8. Architecture Evolution ADR Generator

Generador de ADR para decisiones de evolución arquitectónica.

## Documentos vivos generados

- MVP Architecture Review
- Scope Reduction Matrix
- Evolution Readiness Report
- Build vs External Tool Log
- Dependency Abstraction Map
- Enterprise Transition Assessment
- Role Evolution Map
- Architecture Evolution ADR

## Regla estratégica

**Un MVP debe empezar simple, pero no debe evolucionar a ciegas.**

---

# 9. Capa Transversal — Comunicación Arquitectónica y Preguntas de Descubrimiento

## Pregunta central

**¿Qué debemos preguntar para no asumir mal?**

## Función

Generar preguntas, repreguntas, entrevistas, mapas de responsabilidad, registros de ambigüedad y respuestas basadas en evidencia.

Esta capa atraviesa todos los pilares.

## Problema que resuelve

Muchos errores arquitectónicos no nacen por falta de código. Nacen por:

- Preguntas débiles
- Supuestos no validados
- Conceptos ambiguos
- Decisiones sin responsables
- Respuestas sin evidencia
- Falta de repreguntas

## Capacidades principales

### 1. Architecture Question Engine

Motor de preguntas arquitectónicas contextualizadas.

### 2. Question Reframing Assistant

Reformulador de preguntas defensivas o mal enfocadas.

### 3. Stakeholder Interview Script Generator

Generador de guiones para entrevistas con negocio, desarrollo, QA, operaciones o seguridad.

### 4. Decision Responsibility Map

Mapa de quién decide, aprueba, ejecuta y opera.

### 5. Architectural Q&A Log

Bitácora viva de preguntas y respuestas arquitectónicas.

### 6. Ambiguity Register

Registro de conceptos, decisiones o respuestas ambiguas.

### 7. Evidence-Based Response Checklist

Checklist para responder preguntas operativas con evidencia.

### 8. Architect Role Competency Matrix

Matriz de competencias del rol arquitectónico o agentes arquitectónicos.

## Documentos vivos generados

- Architectural Q&A Log
- Ambiguity Register
- Stakeholder Interview Notes
- Decision Responsibility Map
- Evidence Log

## Regla estratégica

**La calidad de la arquitectura depende de la calidad de las preguntas que la originan.**

---

# 10. Backlog funcional inicial derivado del curso

## Core MVP

1. Architecture Intake Wizard
2. Problem/Solution Separator
3. NFR Profiler
4. Risk & Constraint Register
5. Architectural Style Selector
6. Architecture Trade-off Matrix
7. Architecture Style ADR Generator
8. ARCHITECTURE.md Generator
9. Architecture Question Engine
10. Ambiguity Register

## Nivel avanzado

11. Cost & Operation Estimator
12. Workload Criticality Mapper
13. Strategy Alignment Matrix
14. Microservices Readiness Assessment
15. Event-Driven Readiness Checklist
16. Clean Architecture Fitness Checklist
17. Anti-pattern Detector
18. Evolution Readiness Assessment
19. Enterprise Transition Checklist
20. Evidence-Based Response Checklist

## Nivel enterprise

21. Ubiquitous Language Builder
22. Dependency Direction Map
23. Service Contract Inventory
24. Event Catalog
25. Architecture Cleanliness Score
26. Role Evolution Map
27. Build vs External Tool Decision Log
28. Distributed Complexity Warning System
29. Architect Role Competency Matrix
30. Fitness Function Builder

---

# 11. Documentos vivos base del framework

1. Architecture Brief
2. Problem Definition Document
3. Solution Options Document
4. ARCHITECTURE.md
5. ADR Log
6. Risk & Constraint Register
7. NFR Specification
8. Cost Model / TCO Document
9. Workload Criticality Map
10. Business & Architecture Alignment Document
11. Architecture Style Decision Matrix
12. Architectural Trade-off Register
13. Internal Design Review Report
14. Dependency Map
15. Pattern Decision Log
16. Anti-pattern Register
17. MVP Architecture Review
18. Evolution Readiness Report
19. Enterprise Transition Assessment
20. Architectural Q&A Log
21. Ambiguity Register
22. Decision Responsibility Map

---

# 12. Reglas base para agentes

## Diagnóstico

1. No proponer solución sin definir problema.
2. No aceptar una solución como requerimiento.
3. Separar problema de solución.
4. Registrar riesgos y restricciones.
5. Registrar decisiones como ADR.

## Frugalidad

6. No recomendar arquitectura sin NFRs mínimos.
7. Si aumenta OPEX, justificar valor.
8. Clasificar cargas por criticidad.
9. Conectar decisiones técnicas con estrategia.
10. Evaluar costo humano y operación.

## Selección arquitectónica

11. No recomendar microservicios sin justificar dominio, equipos, despliegue independiente, observabilidad y costo.
12. No descartar monolito por prejuicio.
13. Si hay servicios, definir contratos.
14. Si hay eventos, definir productores, consumidores, payload y consistencia.
15. Registrar trade-offs.

## Diseño interno

16. No aplicar patrones sin problema específico.
17. No recomendar clean architecture como receta universal.
18. Aislar reglas de negocio.
19. Revisar dirección de dependencias.
20. Detectar antipatrones.

## Evolución

21. No ampliar MVP sin justificar valor principal.
22. Evaluar si conviene construir o integrar herramienta externa.
23. Agregar features no implica rearquitectar.
24. Si aparecen nuevos roles, revisar permisos y flujos.
25. Si cambia el modelo de negocio, reejecutar análisis estratégico.

## Comunicación

26. Si hay ambigüedad, repreguntar.
27. Si un concepto no está definido, preguntar qué significa.
28. Si una decisión requiere aprobación, identificar responsable.
29. Si una respuesta revela riesgo, actualizar Risk Register.
30. Si una respuesta revela decisión, actualizar ADR Log.

---

# 13. Diferenciador estratégico del producto

La propuesta diferencial queda así:

**Las herramientas actuales aceleran la generación de software. La aplicación estructura la toma de decisiones para que ese software tenga fundamento arquitectónico.**

Frases posibles de posicionamiento:

- **De idea a arquitectura justificable antes de generar código.**
- **No generamos solo apps; generamos criterio arquitectónico, decisiones trazables y documentos vivos.**
- **La capa de arquitectura que falta entre el prompt y el código.**
- **De prompt a sistema, no solo de prompt a pantalla.**

---

# 14. Conclusión maestra

El Curso 01 no solo aporta contenido de arquitectura. Aporta una estructura de producto.

La conclusión central es:

**La aplicación debe posicionarse como una capa de inteligencia arquitectónica para desarrollo asistido por IA, capaz de transformar una idea en un sistema diagnosticado, justificado, documentado, gobernable y evolutivo.**

El resultado metodológico del curso queda así:

1. Diagnosticar antes de construir.
2. Evaluar costo, riesgo y estrategia antes de diseñar.
3. Seleccionar arquitectura por contexto, no por moda.
4. Revisar limpieza interna antes de escalar código.
5. Gobernar la evolución del MVP hacia producto.
6. Hacer preguntas correctas durante todo el proceso.

Este documento constituye el primer framework base derivado de los cursos para la aplicación.

