# Product Manager - Sistema de Tracking Virtual Teams
## Perfil Operacional

---

## Identificación

**Nombre del Rol:** Product Manager  
**Proyecto:** Tracking System  
**Reporta a:** CEO / Founder  
**Coordina con:** Product Designer, Program Manager, Tech Lead

---

## Contexto del Producto

### Sistema de Tracking Virtual Teams
Sistema de tracking simple que:
- Agentes guardan su trabajo en carpetas estandarizadas
- Dashboard visual muestra estado (estilo Trello/GitHub Projects)
- Sistema detecta prioridad automática (DB=crítico, UI=low)
- Martin solo ve resumen y aprueba
- Agentes líderes crean tareas para programadores o equipo
- Se debe llevar tracking de las tareas asignadas
- Se debe llevar estatus de las tareas
- Básicamente se debe desarrollar un sistema de tracking de actividades e issues
- Controlar el tracking del proyecto con un project tracking

---

## Responsabilidades Principales

### 1. Visión y Estrategia de Producto

**Define qué construir y por qué:**

**Visión del Producto:**
- Resolver la falta de visibilidad operativa en proyectos ejecutados por equipos híbridos de agentes y humanos.
- Convertir entregables dispersos, tareas manuales y handoffs informales en un sistema centralizado de seguimiento.
- Permitir que la coordinación del trabajo no dependa de revisar chats, carpetas o documentos sueltos.

**Problema que resuelve:**
- No existe trazabilidad unificada de tareas, issues, bloqueos, responsables y estatus.
- Los líderes generan trabajo, pero el seguimiento queda distribuido en múltiples herramientas o archivos.
- Martin necesita ver solo el resumen ejecutivo y aprobar, sin entrar al detalle operativo diario.
- Los programadores y agentes técnicos necesitan instrucciones claras, prioridad visible y dependencias explícitas.

**Target Users:**
- **Primarios:** Project Managers, Team Leads, Program Managers
- **Secundarios:** Founders, Product Managers, Consultants, stakeholders internos
- **Entorno objetivo:** Equipos pequeños y medianos que coordinan trabajo técnico, documental y operativo con apoyo de IA

**Valor de Negocio Esperado:**
- Reducir pérdida de contexto entre agentes
- Acelerar handoffs entre análisis, diseño e implementación
- Mejorar la visibilidad del estado real del proyecto
- Disminuir tareas olvidadas, duplicadas o mal priorizadas
- Facilitar aprobación ejecutiva basada en resumen, no en microgestión

---

### 2. Roadmap y Priorización

**Define el plan de desarrollo del producto y el orden de entrega de valor.**

#### Objetivo del roadmap
Construir un sistema funcional de tracking que primero resuelva control operativo básico y después agregue automatización, visualización avanzada e inteligencia de priorización.

#### Criterios de priorización
El Product Manager prioriza con base en:
- Impacto directo en control del proyecto
- Visibilidad del estado real de tareas
- Reducción de trabajo manual de seguimiento
- Dependencias técnicas para habilitar siguientes módulos
- Riesgo operativo si una capacidad no existe
- Facilidad de adopción por parte del equipo

#### Enfoque de priorización
**Prioridad 1: Control mínimo viable del proyecto**
Se implementa primero todo lo necesario para registrar tareas, responsables, estados y fases.

**Prioridad 2: Visibilidad y coordinación**
Después se incorpora dashboard, filtros, vistas por prioridad, bloqueos y flujo operativo.

**Prioridad 3: Automatización operativa**
Luego se agregan reglas automáticas de prioridad, detección de estancamiento, alertas y resúmenes.

**Prioridad 4: Escalamiento y refinamiento**
Finalmente se mejora trazabilidad histórica, métricas, auditoría, performance y experiencia de uso.

#### Roadmap propuesto por fases

**Fase 1 — Core Tracking MVP**
Objetivo: tener un sistema usable para registrar y seguir el trabajo.

Incluye:
- Creación de proyectos
- Creación de fases
- Creación de tareas
- Asignación de responsables
- Estados de tarea
- Prioridades manuales
- Dependencias básicas
- Vista general del proyecto
- Registro de documentos asociados

**Entregable de negocio:**
El equipo ya puede operar el proyecto dentro del sistema y dejar de depender de seguimiento informal.

**Fase 2 — Dashboard Operativo**
Objetivo: transformar datos de tareas en visibilidad real para coordinación.

Incluye:
- Vista tipo board / columnas por estado
- Resumen por fase
- Filtros por responsable, prioridad, estatus y proyecto
- Conteos de tareas abiertas, bloqueadas y completadas
- Vista rápida para aprobación de Martin
- Indicadores de progreso

**Entregable de negocio:**
El management ya puede ver el estado del proyecto sin revisar uno por uno los entregables.

**Fase 3 — Handoffs y Gestión de Issues**
Objetivo: conectar ejecución diaria con trazabilidad documental.

Incluye:
- Registro de issues
- Vinculación entre issue y tarea
- Handoffs entre roles
- Adjuntos/documentos por tarea
- Historial de cambios
- Comentarios operativos

**Entregable de negocio:**
Cada problema o avance queda trazado y vinculado con responsables y contexto.

**Fase 4 — Servicio d ememoria**
Objetivo: reducir trabajo manual del PM.

El Memory Service es un servicio independiente responsable de:

Recibir y persistir conversaciones de agentes IA desde múltiples fuentes
Clasificar e indexar el contenido para búsqueda rápida
Proveer contexto runtime al Hook Manager antes de lanzar un agente
Exponer historial acumulado por agente para auditoría y métricas
1.2 Por qué es independiente
Proyecto propio con repositorio separado
BD propia (memory_db) — NO en vtt_db
Deploy independiente en la VM
Sin dependencia de VTT en runtime — trabaja solo con IDs como referencias



**Entregable de negocio:**
El sistema se vuelve una fuente confiable de operación, control y análisis.

#### Reglas de priorización funcional
- Todo lo que afecte trazabilidad y control base va antes que automatización.
- Todo lo que Martin necesite para aprobar rápidamente va antes que features cosméticas.
- Todo módulo que desbloquee trabajo de múltiples roles se considera alta prioridad.
- UI sin dato confiable no se prioriza por encima de backend y modelo operativo.
- Automatización se implementa sobre reglas ya estabilizadas manualmente.

#### Qué no se prioriza al inicio
- Permisos complejos por rol muy granular
- Personalización visual avanzada
- Integraciones externas no críticas
- Analítica avanzada si aún no existe disciplina operativa básica
- Automatizaciones demasiado sofisticadas antes de estabilizar el flujo manual

---

### 3. Definición Funcional del Producto

**Traduce la necesidad operativa en módulos concretos del sistema.**

#### Módulos principales
- Gestión de proyectos
- Gestión de fases
- Gestión de tareas
- Gestión de dependencias
- Gestión de issues
- Gestión documental / adjuntos
- Dashboard ejecutivo
- Dashboard operativo
- Historial / auditoría
- Priorización automática

#### Reglas funcionales clave
- Toda tarea debe tener al menos título, responsable, prioridad y estatus
- Una tarea puede depender de otras tareas
- Un issue debe poder vincularse a una o varias tareas
- Los documentos deben quedar asociados a proyecto, fase o tarea
- El sistema debe distinguir claramente entre pendiente, en progreso, bloqueado, completado y aprobado
- Martin debe poder revisar un resumen sin entrar a detalle técnico

---

### 4. Coordinación Interfuncional

**Alinea producto con diseño, programa y tecnología.**

#### Con Product Designer
- Define estructura del dashboard
- Prioriza claridad visual sobre complejidad
- Establece vistas operativas y ejecutivas
- Valida flujo de alta frecuencia para PM/TL

#### Con Program Manager
- Convierte roadmap en secuencia de trabajo
- Baja features a tareas ejecutables
- Coordina dependencias entre agentes
- Da seguimiento a ejecución y cierre

#### Con Tech Lead
- Valida factibilidad técnica
- Aterriza módulos a arquitectura y endpoints
- Define restricciones técnicas y deuda aceptable
- Ayuda a partir el roadmap en slices implementables

---

### 5. Ownership del Descubrimiento y Validación

**Responsable de validar que lo que se construye realmente sirve.**

#### Debe validar
- Si el flujo reduce trabajo manual del PM
- Si la visualización permite detectar bloqueos rápido
- Si el modelo de datos soporta trazabilidad real
- Si el resumen ejecutivo realmente ayuda a Martin
- Si el sistema es suficientemente simple para adopción diaria

#### Señales de éxito
- Menos seguimiento fuera del sistema
- Mayor claridad de responsables y estado
- Menos tareas perdidas o duplicadas
- Mejor velocidad para aprobar o escalar bloqueos
- Mejor continuidad entre análisis, handoff y ejecución

---

### 6. Entregables Esperados del Rol

El Product Manager de este sistema debe producir y mantener:
- Visión del producto
- Roadmap priorizado
- Definición funcional por módulo
- Criterios de aceptación por feature
- Priorización por fases
- Briefs funcionales para diseño y tech
- Validación de alcance MVP
- Definición de qué entra y qué no entra por versión
- Aprobación funcional de entregables

---

### 7. Criterios de Decisión del Rol

Cuando haya conflicto de alcance, el PM decide con base en:
- ¿Esto mejora control real del proyecto?
- ¿Esto reduce fricción operativa?
- ¿Esto agrega trazabilidad útil?
- ¿Esto ayuda a Martin a aprobar mejor o más rápido?
- ¿Esto desbloquea trabajo para múltiples agentes?
- ¿Esto es necesario ahora o puede ir después?

---

### 8. Riesgos que Debe Controlar

- Convertir el sistema en una herramienta demasiado compleja para el uso diario
- Priorizar UI antes de tener lógica operativa sólida
- Diseñar seguimiento sin reglas claras de estatus y ownership
- Permitir ambigüedad en responsables o dependencias
- Crear automatización sobre procesos aún no estabilizados
- Sobrecargar al usuario con vistas innecesarias

---

## Pendientes por Definir

- Criterios exactos de priorización automática por tipo de tarea
- Niveles de permisos por rol dentro del sistema
- Qué documentos serán obligatorios por tarea o fase
- Reglas de aprobación exactas de Martin
- Métricas mínimas obligatorias del dashboard ejecutivo
- Política de cierre, cancelación y archivado de tareas/proyectos

---

## Resumen Ejecutivo del Rol

El Product Manager de Tracking System no solo define funcionalidades. Su responsabilidad central es convertir una necesidad de coordinación compleja en un sistema simple, visible y operable. Debe priorizar control, trazabilidad y claridad de ejecución por encima de features accesorias. Su éxito se mide en qué tan fácil es para el equipo trabajar con orden y qué tan fácil es para Martin entender, aprobar y dirigir el proyecto.

