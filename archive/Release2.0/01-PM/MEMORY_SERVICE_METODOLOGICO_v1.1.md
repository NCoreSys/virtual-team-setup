# MEMORY SERVICE — Documento Metodológico

**Proyecto:** Virtual Teams Memory  
**Versión:** 1.1  
**Fecha:** 2026-04-10  
**Estado:** 🔴 OBSOLETO — REEMPLAZADO  
**Tipo:** Documento conceptual (histórico)  
**Decisión cierre:** PM Martin Rivas — 2026-04-21

---

## ⚠️ AVISO DE OBSOLESCENCIA

> **Este documento quedó OBSOLETO el 2026-04-21.** No debe usarse como fuente de verdad.
>
> **Reemplazado por:**
> - `METODOLOGIA_MEMORY_SERVICE_v1.2.md` (documento metodológico vigente, cubre lo conceptual con contenido actualizado)
> - `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` (especificación técnica final, cierra las decisiones)
>
> **Razones del cierre:**
> 1. Solo lista **4 fuentes** (CLI, Web, SDK, ChatGPT). El alcance actual incluye **5 fuentes** — se agregó `VTT_CHANNEL` para comunicación multi-agente.
> 2. Contiene **preguntas pendientes Q-01, Q-03, Q-04, Q-05** que **ya fueron respondidas** en la SPEC v1.9:
>    - Q-01 (agentId) → cerrada por D-MEM-36 (= User.id de VTT, sin catálogo propio).
>    - Q-03 (auth service-to-service) → cerrada por D-MEM-26 (SERVICE_KEY pattern).
>    - Q-04 (consultas a VTT en runtime) → cerrada en METODOLOGIA §12.1 (no consulta; Hook Manager desnormaliza).
>    - Q-05 (contexto síncrono vs asíncrono) → cerrada por D-MEM-37 (siempre síncrono <500ms, fail-fast).
> 3. No refleja las **43 decisiones D-MEM-01 a D-MEM-43** cerradas posteriormente.
> 4. No refleja las **decisiones D-INT-01 a D-INT-05** del ADDENDUM v1.1 (integración Runtime v1.1 y Prompt Builder v1.3).
>
> **Se conserva como histórico** para trazabilidad del razonamiento conceptual inicial. Los glosarios y analogías siguen siendo útiles como material de onboarding, pero **cualquier regla, fuente, decisión o alcance aquí declarado puede estar desactualizado**.
>
> **Para contexto vigente del proyecto, leer:**
> 1. `METODOLOGIA_MEMORY_SERVICE_v1.2.md` — metodología funcional
> 2. `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — contrato técnico
> 3. `ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md` — integración cross-service

---

## PROPÓSITO DE ESTE DOCUMENTO (histórico)

Definir **QUÉ** es el Memory Service y **POR QUÉ** existe. Este documento NO incluye implementación técnica — está diseñado para que cualquier persona pueda validar los conceptos antes de pasar a diseño técnico.

---

## ÍNDICE

1. [Definición del Problema](#1-definición-del-problema)
2. [Qué es el Memory Service](#2-qué-es-el-memory-service)
3. [Conceptos y Definiciones](#3-conceptos-y-definiciones)
4. [Actores del Sistema](#4-actores-del-sistema)
5. [Fuentes de Información](#5-fuentes-de-información)
6. [Procesos del Sistema](#6-procesos-del-sistema)
7. [Información que se Almacena](#7-información-que-se-almacena)
8. [Información que se Consulta](#8-información-que-se-consulta)
9. [Reglas de Negocio](#9-reglas-de-negocio)
10. [Alcance y Exclusiones](#10-alcance-y-exclusiones)
11. [Relación con Otros Módulos](#11-relación-con-otros-módulos)
12. [Decisiones Tomadas](#12-decisiones-tomadas)
13. [Preguntas Pendientes](#13-preguntas-pendientes)
14. [Glosario](#14-glosario)

---

## 1. DEFINICIÓN DEL PROBLEMA

### 1.1 Situación actual

Los agentes de IA ejecutan tareas y generan conversaciones, pero:

- **No hay memoria entre sesiones** — cada vez que un agente arranca, no sabe qué hizo antes
- **El historial está disperso** — archivos en diferentes formatos y ubicaciones
- **No hay contexto para nuevas tareas** — el orquestador no puede informar al agente qué trabajo previo es relevante
- **No se puede medir el consumo** — solo algunas fuentes tienen información de costo

### 1.2 Consecuencias

| Problema | Impacto |
|----------|---------|
| Sin memoria | Los agentes repiten errores que ya cometieron |
| Sin contexto | No aprovechan lecciones aprendidas de tareas similares |
| Sin métricas | El PM no tiene visibilidad del costo por agente o proyecto |
| Sin trazabilidad | No hay registro de qué hizo cada agente y cuándo |

### 1.3 Lo que necesitamos

Un sistema centralizado que:

1. **Reciba** conversaciones de múltiples fuentes
2. **Almacene** el historial de forma organizada
3. **Clasifique** el contenido para búsqueda rápida
4. **Provea contexto** antes de lanzar un agente
5. **Exponga métricas** de uso y costo

---

## 2. QUÉ ES EL MEMORY SERVICE

### 2.1 Definición

El Memory Service es el **sistema de memoria centralizado** para los agentes de IA. Funciona como un repositorio que:

- Recibe y guarda las conversaciones de los agentes
- Organiza el historial por agente, proyecto y tarea
- Permite consultar qué trabajo previo es relevante para una nueva tarea
- Registra métricas de consumo

### 2.2 Analogía

Piensa en el Memory Service como el **cuaderno de bitácora compartido** de un equipo:

- Cada vez que alguien termina una tarea, anota qué hizo y qué aprendió
- Antes de empezar una tarea nueva, revisa si alguien más ya trabajó en algo similar
- El gerente puede consultar cuánto tiempo y recursos se han invertido

### 2.3 Principio fundamental

> **Los archivos originales se guardan completos. El sistema guarda solo metadatos para búsqueda.**

Esto significa:
- El texto completo de las conversaciones vive en archivos
- El sistema tiene índices y resúmenes para búsqueda rápida
- Se puede reconstruir cualquier conversación leyendo el archivo original

### 2.4 Por qué es un sistema independiente

| Razón | Beneficio |
|-------|-----------|
| Tiene su propio almacenamiento | No depende de VTT para funcionar |
| Vive separado | Puede servir a múltiples proyectos |
| Sin dependencias cruzadas | Si VTT cae, el Memory Service sigue funcionando |

---

## 3. CONCEPTOS Y DEFINICIONES

### 3.1 Conversación

Una **conversación** es una sesión completa de trabajo entre un usuario (o sistema) y un agente de IA.

| Atributo | Descripción |
|----------|-------------|
| Inicio y fin | Tiene timestamps de cuándo empezó y terminó |
| Turnos | Contiene uno o más intercambios |
| Resultado | Éxito, error, o incompleto |
| Tarea asociada | Opcionalmente vinculada a una tarea de VTT |

### 3.2 Turno

Un **turno** es un intercambio individual dentro de una conversación.

| Tipo | Descripción |
|------|-------------|
| Turno de usuario | El mensaje o instrucción enviada al agente |
| Turno de asistente | La respuesta del agente |

### 3.3 Bloque

Un **bloque** es una unidad dentro de un turno de asistente. Los agentes no solo responden con texto — también ejecutan acciones.

| Tipo de bloque | Descripción |
|----------------|-------------|
| Texto | Respuesta en lenguaje natural |
| Pensamiento | Razonamiento interno del agente (no siempre visible) |
| Uso de herramienta | Cuando el agente ejecuta una acción (leer archivo, editar código, ejecutar comando) |
| Resultado de herramienta | El output de la acción ejecutada |

### 3.4 Timeline del Agente

El **timeline** es la línea de tiempo acumulada de todas las conversaciones de un agente, ordenadas cronológicamente.

Representa **"todo lo que este agente ha hecho"** — su historial completo.

### 3.5 Contexto Runtime

El **contexto runtime** es un resumen compacto de información relevante que se inyecta al agente antes de ejecutar una tarea.

| Incluye | Descripción |
|---------|-------------|
| Trabajo reciente | Qué hizo el agente en las últimas sesiones |
| Sesiones relacionadas | Trabajo previo sobre temas similares |
| Archivos frecuentes | Archivos que el agente modifica seguido |
| Lecciones aprendidas | Errores o patrones a evitar (futuro) |

### 3.6 Clasificación

La **clasificación** es el proceso de etiquetar una conversación automáticamente.

| Etiqueta | Ejemplos |
|----------|----------|
| Temas | autenticación, base de datos, frontend, testing |
| Tipo de trabajo | implementación, corrección de bug, revisión, migración |
| Archivos modificados | lista de archivos tocados durante la sesión |
| Entidades | nombres de servicios, clases o componentes mencionados |

---

## 4. ACTORES DEL SISTEMA

### 4.1 Hook Manager (Orquestador)

El Hook Manager es el sistema que lanza y coordina a los agentes.

| Momento | Qué necesita del Memory Service |
|---------|--------------------------------|
| **Antes de lanzar agente** | Contexto relevante para inyectar en el prompt |
| **Después de que termina** | Guardar la conversación que generó |

### 4.2 Agentes de IA

Los agentes son los ejecutores de tareas (BE-Agent, FE-Agent, TL-Agent, etc.)

| Interacción | Descripción |
|-------------|-------------|
| No directa | Los agentes no hablan con Memory Service — el Hook Manager es el intermediario |
| Reciben contexto | El contexto histórico les llega como parte de su prompt inicial |

### 4.3 PM (Product Manager)

| Necesita | Para qué |
|----------|----------|
| Ver historial de cada agente | Saber qué ha trabajado cada uno |
| Conocer costos por proyecto | Presupuesto y proyecciones |
| Entender consumo por tarea | Identificar tareas costosas |

### 4.4 TL-Agent (Tech Lead Agent)

| Necesita | Para qué |
|----------|----------|
| Contexto histórico | Armar mejores asignaciones |
| Saber qué agente trabajó qué | Asignar al agente con más experiencia en el tema |
| Archivos frecuentes | Identificar módulos que se modifican seguido |

### 4.5 Dashboard VTT

| Necesita | Para qué |
|----------|----------|
| Timeline de conversaciones | Mostrar historial por agente |
| Contenido de conversación | Renderizar el detalle de una sesión |
| Métricas de costo | Mostrar consumo en pantallas de reportes |

---

## 5. FUENTES DE INFORMACIÓN

El Memory Service recibe conversaciones de **cuatro fuentes principales** y está diseñado para agregar más en el futuro.

### 5.1 Claude CLI (Claude Code)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Sesiones manuales ejecutadas desde terminal |
| **Quién lo usa** | Desarrolladores usando Claude Code directamente |
| **Qué contiene** | Historial completo, herramientas usadas, archivos tocados |
| **Costo disponible** | ❌ No — Claude Code no expone el costo |

### 5.2 Claude Web

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Conversaciones exportadas desde claude.ai |
| **Quién lo usa** | Usuarios que exportan manualmente |
| **Qué contiene** | Historial completo, timestamps, archivos adjuntos |
| **Costo disponible** | ❌ No — claude.ai no expone el costo |

### 5.3 Agent SDK

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Agentes ejecutados programáticamente |
| **Quién lo usa** | El sistema automatizado de agentes |
| **Qué contiene** | Historial completo, herramientas, archivos, **costo real**, tokens, duración |
| **Costo disponible** | ✅ Sí — esta es la única fuente con costo real |

### 5.4 ChatGPT Export

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Conversaciones exportadas desde ChatGPT |
| **Quién lo usa** | Usuarios que exportan manualmente |
| **Qué contiene** | Historial de turnos |
| **Costo disponible** | ❌ No — ChatGPT no expone el costo |

### 5.5 Extensibilidad

El sistema está diseñado para agregar nuevas fuentes:
- Gemini (Google)
- Copilot (GitHub/Microsoft)
- Otros modelos de IA
- Importación manual

---

## 6. PROCESOS DEL SISTEMA

### 6.1 Proceso: Importación de Conversación

**Disparador**: Un agente termina su ejecución, o un usuario sube un archivo manualmente.

**Flujo**:

```
RECEPCIÓN
   │
   ├─ El sistema recibe el archivo de conversación
   ├─ Identifica la fuente (CLI, Web, SDK, ChatGPT)
   └─ Verifica que no sea un duplicado
         │
         ▼
ALMACENAMIENTO
   │
   ├─ Guarda el archivo original en el servidor
   └─ Lo organiza por agente y fecha
         │
         ▼
PROCESAMIENTO
   │
   ├─ Lee el archivo según su formato
   ├─ Extrae los turnos y bloques
   └─ Extrae métricas si están disponibles
         │
         ▼
CLASIFICACIÓN
   │
   ├─ Identifica los temas tratados
   ├─ Detecta el tipo de trabajo realizado
   ├─ Lista los archivos modificados
   └─ Extrae entidades mencionadas
         │
         ▼
INDEXACIÓN
   │
   ├─ Guarda los metadatos para búsqueda
   ├─ Actualiza el timeline del agente
   └─ Queda disponible para consultas
```

**Resultado**: La conversación está almacenada, clasificada e indexada.

---

### 6.2 Proceso: Consulta de Contexto Runtime

**Disparador**: El orquestador está por lanzar un agente para una nueva tarea.

**Flujo**:

```
SOLICITUD
   │
   ├─ El orquestador pide contexto para un agente específico
   └─ Indica el proyecto, la tarea, y opcionalmente los temas relevantes
         │
         ▼
BÚSQUEDA
   │
   ├─ Busca las últimas sesiones del agente
   ├─ Busca sesiones con temas similares
   └─ Identifica archivos que el agente modifica frecuentemente
         │
         ▼
COMPILACIÓN
   │
   ├─ Arma un resumen compacto con la información relevante
   ├─ NO incluye el texto completo de las conversaciones
   └─ Solo metadatos y resúmenes
         │
         ▼
RESPUESTA
   │
   ├─ Retorna el contexto rápidamente (requisito de velocidad)
   └─ El orquestador lo inyecta en el prompt del agente
```

**Resultado**: El agente arranca con conocimiento de su trabajo previo relevante.

**Requisito crítico**: Este proceso debe ser muy rápido porque se ejecuta antes de cada lanzamiento de agente.

---

### 6.3 Proceso: Consulta de Timeline

**Disparador**: Un usuario quiere ver el historial de un agente.

**Flujo**:

```
SOLICITUD
   │
   ├─ El usuario pide el timeline de un agente
   └─ Puede filtrar por proyecto
         │
         ▼
BÚSQUEDA
   │
   ├─ Obtiene todas las conversaciones del agente
   └─ Las ordena cronológicamente (más reciente primero)
         │
         ▼
RESPUESTA
   │
   └─ Retorna la lista con metadatos de cada sesión:
        - Fecha
        - Tarea asociada
        - Cantidad de turnos
        - Costo (si está disponible)
        - Temas identificados
```

**Resultado**: El usuario ve la línea de tiempo completa del agente.

---

### 6.4 Proceso: Lectura de Conversación Completa

**Disparador**: Un usuario selecciona una conversación para ver el detalle.

**Flujo**:

```
SOLICITUD
   │
   └─ El usuario pide el contenido de una conversación específica
         │
         ▼
LECTURA
   │
   ├─ El sistema lee el archivo original del servidor
   └─ Lo procesa según su formato
         │
         ▼
RESPUESTA
   │
   └─ Retorna todos los turnos con su contenido completo:
        - Mensajes del usuario
        - Respuestas del agente
        - Herramientas usadas
        - Resultados de herramientas
```

**Resultado**: El usuario puede leer toda la conversación.

---

### 6.5 Proceso: Consulta de Costos

**Disparador**: El PM quiere saber cuánto se ha gastado.

**Flujo**:

```
SOLICITUD
   │
   └─ Se pide un reporte de costos por proyecto
         │
         ▼
AGREGACIÓN
   │
   ├─ Suma los costos de todas las conversaciones del proyecto
   └─ Agrupa por agente y por tarea
         │
         ▼
RESPUESTA
   │
   └─ Retorna:
        - Total del proyecto
        - Desglose por agente
        - Desglose por tarea
        - Nota: solo las conversaciones de Agent SDK tienen costo real
```

**Resultado**: El PM tiene visibilidad del gasto.

---

## 7. INFORMACIÓN QUE SE ALMACENA

### 7.1 Por cada conversación

| Información | Descripción | Siempre disponible |
|-------------|-------------|-------------------|
| Identificador único | ID interno del sistema | ✅ Siempre |
| Identificador original | ID de la sesión en la fuente | ✅ Siempre |
| Fuente | CLI, Web, SDK, ChatGPT | ✅ Siempre |
| Agente | Quién ejecutó la conversación | ✅ Siempre |
| Proyecto | A qué proyecto pertenece | ✅ Siempre |
| Tarea | A qué tarea está asociada | ⚠️ Opcional |
| Fecha de inicio | Cuándo empezó | ✅ Siempre |
| Fecha de fin | Cuándo terminó | ✅ Siempre |
| Cantidad de turnos | Cuántos intercambios hubo | ✅ Siempre |
| Estado | Importada, procesando, error | ✅ Siempre |

### 7.2 Por cada turno

| Información | Descripción |
|-------------|-------------|
| Posición | Número de turno en la conversación (1, 2, 3...) |
| Rol | Usuario o asistente |
| Cuándo ocurrió | Timestamp |
| Vista previa | Primeros caracteres del contenido |

### 7.3 Por cada bloque

| Información | Descripción |
|-------------|-------------|
| Posición | Número de bloque dentro del turno |
| Tipo | Texto, uso de herramienta, resultado, pensamiento |
| Herramienta | Nombre de la herramienta (si aplica) |
| Archivo | Archivo tocado (si aplica) |
| Éxito | Si la herramienta ejecutó correctamente |

### 7.4 Métricas de uso (solo Agent SDK)

| Información | Descripción |
|-------------|-------------|
| Tokens de entrada | Cuántos tokens envió el usuario/sistema |
| Tokens de salida | Cuántos tokens generó el agente |
| Tokens de cache | Tokens reutilizados (más económicos) |
| Costo en USD | Costo total de la sesión |
| Duración | Cuánto tardó |
| Modelo usado | Qué modelo de IA se utilizó |
| Si hubo error | Si la sesión terminó en error |

### 7.5 Clasificación

| Información | Descripción |
|-------------|-------------|
| Temas | Lista de temas detectados |
| Tipo de trabajo | Implementación, bug-fix, revisión, etc. |
| Archivos modificados | Lista de archivos tocados |
| Entidades | Servicios, clases, componentes mencionados |
| Nivel de confianza | Qué tan seguro está el sistema de la clasificación |

---

## 8. INFORMACIÓN QUE SE CONSULTA

### 8.1 Lo que necesita el Orquestador (Hook Manager)

| Consulta | Para qué |
|----------|----------|
| Contexto para un agente en una tarea | Armar el prompt inicial del agente |
| Últimas sesiones de un agente | Saber qué hizo recientemente |
| Sesiones relacionadas con un tema | Encontrar trabajo previo relevante |

### 8.2 Lo que necesita el Dashboard

| Consulta | Para qué |
|----------|----------|
| Timeline de un agente | Ver todo el historial del agente |
| Contenido de una conversación | Leer una conversación específica |
| Costos de un proyecto | Ver cuánto se ha gastado |

### 8.3 Lo que necesita el PM

| Consulta | Para qué |
|----------|----------|
| Costo total por proyecto | Presupuesto y proyecciones |
| Costo por tarea | Identificar tareas costosas |
| Costo por agente | Ver qué agentes consumen más |
| Sesiones sin tarea asignada | Identificar trabajo no trackeado |

---

## 9. REGLAS DE NEGOCIO

### RN-01: No se duplican conversaciones

> Si se intenta importar una conversación que ya existe (mismo identificador original), el sistema la ignora sin reportar error.

**Razón**: Evita duplicados si hay reintentos de importación.

---

### RN-02: El archivo original siempre se preserva

> El archivo original de la conversación se guarda completo y nunca se modifica.

**Razón**: Permite reprocesar, auditar, y reconstruir cualquier conversación.

---

### RN-03: Solo Agent SDK tiene costo real

> Las conversaciones de CLI, Web y ChatGPT no tienen información de costo. Solo Agent SDK provee el costo real en USD.

**Razón**: Las otras fuentes no exponen esta información.

---

### RN-04: El contexto runtime debe ser rápido

> La consulta de contexto para el orquestador debe responder en menos de 500 milisegundos.

**Razón**: No debe retrasar el lanzamiento de agentes.

---

### RN-05: El contexto runtime no lee archivos completos

> El contexto se arma solo con metadatos almacenados, sin leer los archivos originales.

**Razón**: Garantiza velocidad de respuesta.

---

### RN-06: Toda conversación se clasifica automáticamente

> Cuando se importa una conversación, se clasifica automáticamente usando reglas.

**Razón**: No depende de intervención humana.

---

### RN-07: Se pueden agregar nuevas fuentes

> El sistema acepta fuentes adicionales sin necesidad de cambios estructurales.

**Razón**: Flexibilidad para incorporar nuevos modelos de IA.

---

### RN-08: Las referencias a VTT son solo por identificador

> El Memory Service guarda los identificadores de agentes, proyectos y tareas de VTT, pero no tiene relaciones directas con VTT.

**Razón**: Independencia entre sistemas.

---

### RN-09: Los archivos se organizan por agente y fecha

> Los archivos se almacenan en carpetas organizadas por agente y mes.

**Razón**: Facilita la navegación y el mantenimiento.

---

### RN-10: Una conversación puede no tener tarea

> Una conversación puede existir sin estar vinculada a una tarea específica.

**Razón**: No todo el trabajo está vinculado a una tarea formal (debugging, exploración, etc.).

---

## 10. ALCANCE Y EXCLUSIONES

### 10.1 Incluido en este módulo

| Funcionalidad | Descripción |
|---------------|-------------|
| Importación de conversaciones | Recibir y almacenar desde 4 fuentes |
| Clasificación automática | Etiquetar por reglas determinísticas |
| Timeline por agente | Historial acumulado ordenado |
| Contexto runtime | Información para el orquestador |
| Lectura de conversaciones | Ver el contenido completo |
| Métricas de costo | Agregados por proyecto/tarea/agente |
| Almacenamiento de archivos | Guardar originales en el servidor |

### 10.2 Excluido de este módulo

| Funcionalidad | Dónde vive | Razón |
|---------------|------------|-------|
| Tracking manual de costos CLI | Submódulo 5F en VTT | Propósito diferente |
| Interfaz visual | VTT Frontend | Este módulo solo provee datos |
| Orquestación de agentes | Hook Manager | Este módulo es consumido por él |
| Control de acceso | VTT | Se integrará cuando esté activo |
| Búsqueda semántica | Fase futura | Requiere tecnología adicional |
| Clasificación por IA | Fase futura | Por ahora solo reglas |

### 10.3 Fases futuras

| Funcionalidad | Fase |
|---------------|------|
| Búsqueda de texto completo | Fase 2 |
| Búsqueda semántica inteligente | Fase 2 |
| Múltiples agentes en una conversación | Fase 2 |
| Limpieza automática de datos viejos | Fase 2 |
| Clasificación usando IA | Fase 3 |
| Búsqueda por relaciones | Fase 3 |

---

## 11. RELACIÓN CON OTROS MÓDULOS

### 11.1 Con el Hook Manager (Orquestador)

El Hook Manager es el **consumidor principal** del Memory Service.

| Momento | Interacción |
|---------|-------------|
| Antes de lanzar agente | Pide contexto relevante |
| Después de terminar agente | Envía la conversación para almacenar |

**Flujo simplificado**:

```
Hook Manager: "Voy a lanzar BE-Agent para tarea de autenticación"
     │
     ├──────► Memory Service: "Dame contexto relevante"
     │
     │◄────── Memory Service: "Aquí tienes: últimas 3 sesiones,
     │                         archivos frecuentes, temas relacionados"
     │
     │        ... agente ejecuta ...
     │
     ├──────► Memory Service: "Guarda esta conversación"
     │
     │◄────── Memory Service: "Guardada y clasificada"
```

### 11.2 Con VTT (Dashboard)

VTT consume el Memory Service para mostrar información en sus pantallas.

| Pantalla | Qué consume |
|----------|-------------|
| Timeline de agente | Lista de conversaciones con metadatos |
| Visor de conversación | Contenido completo de una sesión |
| Reportes de costo | Métricas agregadas |

### 11.3 Comparación con Submódulo 5F

Son módulos **complementarios**, no duplicados:

| Aspecto | Memory Service | Submódulo 5F |
|---------|----------------|--------------|
| **Propósito principal** | Memoria y contexto para agentes | Auditoría de costos para PM |
| **Fuentes de datos** | 4 fuentes (CLI, Web, SDK, ChatGPT) | Solo CLI |
| **Cómo llegan los datos** | Automáticamente via orquestador | Manual via upload |
| **Costo** | Solo SDK tiene real | Calcula desde catálogo de precios |
| **Independencia** | Sistema separado | Dentro de VTT |

---

## 12. DECISIONES TOMADAS

### D-01: Es un sistema independiente

El Memory Service vive separado de VTT, con su propio almacenamiento.

**Razón**: Permite reutilizarlo para otros proyectos y garantiza independencia.

---

### D-02: Los archivos se copian al servidor

El orquestador envía los archivos completos al Memory Service, que los guarda permanentemente.

**Razón**: El Memory Service no accede al filesystem local de nadie.

---

### D-03: Agent SDK envía dos archivos

Las conversaciones de Agent SDK incluyen dos archivos: el historial y el log de eventos (donde está el costo).

**Razón**: El costo y los tokens están en el log, no en el historial.

---

### D-04: Si ya existe, se ignora

Si una conversación ya fue importada (mismo identificador), se ignora sin error.

**Razón**: Permite reintentos seguros.

---

### D-05: El sistema anterior se descarta

El módulo VTM legacy no se migra ni se usa como base.

**Razón**: Su diseño es incompatible con los requerimientos actuales.

---

### D-06: El timeline es simplemente un listado ordenado

No hay estructura especial — es la lista de conversaciones del agente ordenada por fecha.

**Razón**: Simplicidad.

---

### D-07: El contexto runtime debe responder en menos de 500ms

La consulta de contexto debe ser muy rápida.

**Razón**: Se ejecuta antes de cada lanzamiento de agente — no puede ser cuello de botella.

---

### D-08: La clasificación inicial usa reglas simples

En la primera fase, la clasificación usa reglas determinísticas (palabras clave, patrones).

**Razón**: Más simple y predecible. Clasificación por IA viene después.

---

### D-09: Las fuentes son extensibles

El campo que indica la fuente acepta cualquier valor, no una lista fija.

**Razón**: Permite agregar nuevas fuentes sin necesidad de cambios estructurales.

---

### D-10: La interfaz visual sigue en VTT

El visor de conversaciones se rediseña dentro de VTT, no dentro del Memory Service.

**Razón**: Memory Service es solo el sistema de datos, no tiene interfaz visual propia.

---

## 13. PREGUNTAS PENDIENTES

### Q-01: Identificador del agente

**Pregunta**: ¿El identificador de agente en Memory Service es el mismo que usa VTT, o se crea un catálogo propio?

**Para**: SA (Systems Analyst)

**Impacto**: Define si hay duplicación de datos o solo referencias.

---

### Q-03: Autenticación entre servicios

**Pregunta**: ¿Cómo se verifica que el Hook Manager es legítimo cuando hace peticiones? ¿Clave compartida o mecanismo propio?

**Para**: AR (Arquitecto)

**Impacto**: Seguridad de la comunicación entre sistemas.

---

### Q-04: Consultas a VTT

**Pregunta**: ¿Memory Service necesita consultar información a VTT en tiempo real (por ejemplo, el nombre de una tarea)? ¿O trabaja solo con los identificadores que recibe?

**Para**: SA (Systems Analyst)

**Impacto**: Define si hay dependencia en tiempo de ejecución o no.

---

### Q-05: Contexto síncrono vs asíncrono

**Pregunta**: ¿El contexto runtime siempre debe responder inmediatamente, o puede haber una versión que tome más tiempo para contextos más elaborados?

**Para**: AR (Arquitecto)

**Impacto**: Arquitectura del servicio y experiencia de uso.

---

## 14. GLOSARIO

| Término | Definición |
|---------|------------|
| **Agente** | Instancia de IA que ejecuta tareas (BE-Agent, FE-Agent, TL-Agent, etc.) |
| **Bloque** | Unidad dentro de un turno: texto, uso de herramienta, resultado, pensamiento |
| **Clasificación** | Etiquetas asignadas a una conversación (temas, tipo de trabajo, archivos) |
| **Contexto runtime** | Información resumida que se inyecta en el prompt de un agente antes de ejecutar |
| **Conversación** | Sesión completa de trabajo entre usuario/sistema y un agente |
| **Hook Manager** | Orquestador que lanza agentes, solicita contexto, y reporta resultados |
| **Idempotencia** | Propiedad de que una operación puede ejecutarse múltiples veces con el mismo resultado |
| **Metadatos** | Información sobre la conversación (fecha, duración, costo) sin el contenido completo |
| **Source / Fuente** | Origen de la conversación (CLI, Web, SDK, ChatGPT) |
| **Timeline** | Línea de tiempo de todas las conversaciones de un agente |
| **Token** | Unidad de texto procesada por el modelo de IA |
| **Turno** | Un intercambio individual: mensaje del usuario + respuesta del agente |
| **VTM** | Virtual Teams Memory — módulo anterior que se descarta |
| **VTT** | Virtual Teams Tracking — sistema principal de gestión de proyectos |

---

## PRÓXIMOS PASOS

| # | Paso | Responsable |
|---|------|-------------|
| 1 | Validar este documento metodológico | PM |
| 2 | Responder Q-01 y Q-04 | SA |
| 3 | Responder Q-03 y Q-05 | AR |
| 4 | Generar documento técnico basado en este | SA → AR → TL |

---

**Documento:** MEMORY_SERVICE_METODOLOGICO_v1.1.md  
**Tipo:** Conceptual — sin implementación técnica  
**Estado:** BORRADOR PARA VALIDACIÓN PM  
**Fecha:** 2026-04-10
