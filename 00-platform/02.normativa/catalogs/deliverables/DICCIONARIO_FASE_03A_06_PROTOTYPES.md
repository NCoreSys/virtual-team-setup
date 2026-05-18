# DICCIONARIO DE DELIVERABLES — FASE 3A.6: PROTOTYPES

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 3A — Design UX/UI  
**Subfase:** 3A.6 — Prototypes  
**Total deliverables:** 6  
**Responsable de subfase:** UI Designer  
**Aprueba:** Design Lead

---

## Contexto de la subfase

Prototypes transforman los mockups estáticos en experiencias interactivas: el usuario puede clickear, navegar, y recorrer flujos como si el producto existiera. Son la herramienta de validación más poderosa antes de escribir código: permiten testear usabilidad, presentar a stakeholders, y alinear expectativas con una experiencia real, no con imágenes estáticas.

**Prerequisitos de subfase:**
- Mockups de alta fidelidad aprobados (3A.5)
- User Flows definidos (2.6)
- Wireframe Flows definidos (3A.4.8)

**Entrega de subfase:**
- Prototipo interactivo navegable con flujos principales y secundarios, listo para usability testing

---

### 3A.6.1 Interactive Prototype

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.6 Prototypes |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + actualizaciones post-testing |

**Perfil de ejecución:** Requiere dominio de Figma prototyping: connections, interactions, animations, overlays, scroll behavior, y component interactions.  
En VTT: un agente NO puede crear prototipos en Figma — es trabajo de conexión visual entre frames. Puede listar todas las interacciones que deben conectarse como checklist para el UI Designer. Necesita brief con: mockups, user flows, y interacciones esperadas.

**Qué es:** Prototipo clickeable completo en Figma que conecta todos los mockups en flujos navegables. El usuario puede clickear botones, navegar entre páginas, llenar formularios (simulados), ver transiciones, y recorrer los flujos principales y secundarios del producto como si fuera real. Incluye interacciones básicas: page transitions, overlays (modals), scroll, y tab switching.

**Para qué sirve:** Es la experiencia más cercana al producto final sin código. Permite: usability testing con usuarios reales (3A.8), presentaciones a stakeholders (más convincente que mockups estáticos), alineación con developers (ven exactamente cómo debe funcionar), y detección de problemas de flujo (un botón que no lleva a ningún lado, un paso faltante).

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — pantallas a conectar
- `3A.4.8` Wireframe Flows — secuencia de pantallas por flujo
- `2.6.1` User Flow Diagrams — flujos principales
- `3A.5.5` Component States — estados interactivos

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)* — mockups finales
- `3A.4.8` Wireframe Flows *(obligatorio)* — secuencia de pantallas
- `2.6.1` User Flow Diagrams *(obligatorio)* — flujos a prototipar

**Habilita (successors):**
- `3A.6.2` Main Flow Prototype — flujo principal como subset
- `3A.6.3` Secondary Flows — flujos secundarios
- `3A.6.5` Prototype Links — links compartibles
- `3A.8.1` Usability Test Plan — prototipo como objeto de testing
- `3A.8.2` Test Script — tareas basadas en el prototipo

**Audiencia:**
- **Usability testing participants** — lo que testean
- **Design Lead** — review de flujos
- **Product Owner** — validación de experiencia
- **Stakeholders** — presentación del producto
- **Frontend Developer** — referencia de interacciones

**Secciones esperadas:**
1. Prototipo navegable en Figma (todas las pantallas conectadas)
2. Starting points por flujo (frame de inicio de cada flujo)
3. Interacciones configuradas (click, hover, scroll, overlay)
4. Transitions (tipo: dissolve, slide, smart animate; duración)
5. Overlay behavior (modals, drawers, dropdowns, tooltips)
6. Device frame (iPhone/desktop para contexto visual)

**Criterio de completitud:**
- [ ] Flujos principales navegables de inicio a fin
- [ ] Flujos secundarios conectados
- [ ] Navegación global funcional (menú, tabs, sidebar)
- [ ] Modals y overlays funcionales
- [ ] No hay "dead ends" (pantallas sin salida)
- [ ] Transiciones configuradas (no corte abrupto)
- [ ] Versión desktop y mobile (si aplica)

**Anti-patrones:**
- ❌ **Dead ends:** El usuario clickea un botón y no pasa nada — confuso en testing.
- ❌ **Solo happy path:** El prototipo solo funciona si el usuario hace exactamente lo esperado — cualquier desvío rompe la ilusión.
- ❌ **Prototipo como demo, no como test:** Diseñado para impresionar stakeholders pero no para testear con usuarios — pierde su propósito principal.
- ❌ **Over-prototyping:** Invertir 2 semanas en animaciones micro cuando el objetivo es validar flujos — scope creep.

**Template:** `phases/03-design/deliverables/interactive-prototype.figma` *(pendiente)*

---

### 3A.6.2 Main Flow Prototype

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.6 Prototypes |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 3A.6.1 |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere identificar el flujo principal y asegurar que es navegable sin errores.  
En VTT: un agente NO puede crear el prototipo. Puede identificar cuál es el main flow y listar la secuencia de pantallas.

**Qué es:** Subset del prototipo interactivo que cubre el flujo principal del producto (el core value loop): la secuencia de pantallas que el usuario recorre para obtener el valor principal del producto. Ejemplo: para un e-commerce es buscar → seleccionar → agregar al carrito → checkout → confirmación. Para un project management tool es crear proyecto → agregar tareas → asignar → completar.

**Para qué sirve:** Es la primera prioridad de prototyping. Si solo hay tiempo para prototipar un flujo, es este. Es el flujo que se testea primero en usability testing, el que se demuestra a stakeholders, y el que define el core experience del producto.

**Inputs requeridos:**
- `3A.6.1` Interactive Prototype — subset del prototipo completo
- `2.6.2` Happy Path Flows — flujo principal identificado

**Dependencias (predecessors):**
- `3A.6.1` Interactive Prototype *(obligatorio)*
- `2.6.2` Happy Path Flows *(obligatorio)*

**Habilita (successors):**
- `3A.8.2` Test Script — main flow como primera tarea de testing
- Demos a stakeholders

**Audiencia:**
- **Todos** — el flujo principal es la experiencia core del producto

**Secciones esperadas:**
1. Flujo principal identificado (qué secuencia de pantallas)
2. Starting point del flujo
3. Todas las pantallas del flujo conectadas sin dead ends
4. Variaciones mínimas (error en un paso, campo vacío)

**Criterio de completitud:**
- [ ] Main flow identificado y aprobado por PO
- [ ] Navegable de inicio a fin sin errores
- [ ] Cubre el core value loop del producto
- [ ] Testeable sin asistencia del moderador

**Anti-patrones:**
- ❌ **Main flow = todo el producto:** Si el "flujo principal" tiene 20 pantallas, no se ha identificado el core — priorizar el valor principal.
- ❌ **Main flow roto:** Dead ends, botones no conectados — arruina usability testing.

**Template:** `phases/03-design/deliverables/main-flow-prototype.figma` *(pendiente)*

---

### 3A.6.3 Secondary Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.6 Prototypes |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere prototipar los flujos de soporte: registration, settings, profile, notifications.  
En VTT: un agente NO puede crear prototipos. Puede listar flujos secundarios y sus secuencias.

**Qué es:** Prototipos de los flujos secundarios del producto: registro/onboarding, configuración de cuenta, gestión de perfil, notificaciones, búsqueda, filtrado, y cualquier flujo que no es el core value loop pero es necesario para una experiencia completa.

**Para qué sirve:** El main flow es el core; los secondary flows son el ecosystem. Un usuario no puede usar el main flow sin registrarse primero (onboarding), ni puede personalizar su experiencia sin settings. Los secondary flows aseguran que la experiencia completa es navegable.

**Inputs requeridos:**
- `3A.6.1` Interactive Prototype — parte del prototipo
- `2.6.1` User Flow Diagrams — flujos secundarios identificados

**Dependencias (predecessors):**
- `3A.6.1` Interactive Prototype *(obligatorio)*
- `3A.6.2` Main Flow Prototype *(obligatorio)* — el main flow se protutipa primero

**Habilita (successors):**
- `3A.8.2` Test Script — tareas de testing secundarias
- Usability testing de flujos completos

**Audiencia:**
- **UX Designer** — validación de flujos secundarios
- **QA Engineer** — test scenarios

**Secciones esperadas:**
1. Lista de flujos secundarios prototipados
2. Prototipo navegable de cada flujo
3. Conexión con el main flow (cómo se llega al flujo secundario desde el main)

**Criterio de completitud:**
- [ ] Flujos de registro/onboarding prototipados
- [ ] Flujos de settings/profile prototipados
- [ ] Conexión con el main flow funcional
- [ ] No hay dead ends en flujos secundarios

**Anti-patrones:**
- ❌ **Flujos secundarios aislados:** No se puede llegar al flujo de settings desde el main flow — no están conectados.
- ❌ **Solo main flow prototipado:** "Los secundarios ya se entienden" — no si no se pueden recorrer.

**Template:** `phases/03-design/deliverables/secondary-flows.figma` *(pendiente)*

---

### 3A.6.4 Micro-interactions

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.6 Prototypes |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma/Video |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere sensibilidad de motion design: easing curves, timing, y cuándo la animación agrega valor vs cuándo distrae.  
En VTT: un agente NO puede crear micro-interactions. Puede especificar textualmente las animaciones (tipo, duración, easing, trigger) como referencia para el UI Designer. Necesita brief con: interacciones que necesitan animación y el "feeling" deseado (snappy, smooth, playful).

**Qué es:** Definición y demostración de las animaciones y transiciones del producto: page transitions (slide, fade, dissolve), component animations (button press, toggle switch, accordion expand), feedback animations (success checkmark, error shake, loading pulse), y gesture responses (swipe, pull-to-refresh). Pueden ser prototipos en Figma (Smart Animate) o videos/GIFs de referencia.

**Para qué sirve:** Las micro-interactions son el "polish" que diferencia una app profesional de una amateur. Un toggle que se desliza smoothly vs uno que cambia abruptamente — la funcionalidad es igual, pero la sensación es completamente diferente. Las micro-interactions dan feedback, guían la atención, y crean delicia.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — componentes a animar
- `3A.5.5` Component States — transiciones entre estados
- Motion design references (si hay brand guidelines de motion)

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)*
- `3A.5.5` Component States *(obligatorio)* — estados a transicionar

**Habilita (successors):**
- `3A.9.1` Handoff Document — animaciones documentadas para dev
- `4.4.1` Components — implementación de animaciones CSS/JS
- `3A.7.1` Design Tokens — animation tokens (duration, easing)

**Audiencia:**
- **Frontend Developer** — implementación de animaciones
- **Design Lead** — aprobación de motion design
- **QA Engineer** — verificación de animaciones

**Secciones esperadas:**
1. Catálogo de micro-interactions (tabla: componente, trigger, animation, duration, easing)
2. Page transitions (tipo, dirección, duración)
3. Component animations (expand, collapse, toggle, slide)
4. Feedback animations (success, error, loading)
5. Motion principles del producto (fast/slow, bouncy/smooth, subtle/dramatic)
6. Demos en Figma (Smart Animate) o videos/GIFs

**Criterio de completitud:**
- [ ] Page transitions definidas
- [ ] Component animations principales definidas
- [ ] Feedback animations definidas (success, error)
- [ ] Duration y easing especificados por animación
- [ ] Motion principles documentados
- [ ] Al menos 5 micro-interactions demostradas

**Anti-patrones:**
- ❌ **Animaciones lentas:** Transiciones de 500ms+ se sienten sluggish — 200-300ms es el sweet spot.
- ❌ **Animaciones en todo:** Cada elemento se anima — distrae y fatiga. Solo animar donde agrega valor.
- ❌ **Sin easing:** Animaciones lineales se sienten mecánicas — usar ease-out para entradas, ease-in para salidas.
- ❌ **Animaciones no especificadas:** "Ponle una animación" — el developer inventa algo inconsistente.

**Template:** `phases/03-design/deliverables/micro-interactions.md` *(pendiente)*

---

### 3A.6.5 Prototype Links

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.6 Prototypes |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | URLs |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez + actualización si cambian los flows |

**Perfil de ejecución:** Requiere configurar los share links de Figma con los starting points correctos.  
En VTT: un agente puede documentar los links y verificar que funcionan. Es altamente delegable. Necesita brief con: links generados por el UI Designer.

**Qué es:** Colección de URLs compartibles del prototipo en Figma, organizadas por flujo y por device. Cada link tiene un starting point específico (frame de inicio) y device frame configurado (iPhone, desktop). Los links se usan para: usability testing (participantes acceden al prototipo), stakeholder review, y developer reference.

**Para qué sirve:** Sin links organizados, cada persona que necesita ver el prototipo tiene que pedir al UI Designer "¿cuál es el link del flujo de registro en mobile?". Los links organizados son self-service: cualquier miembro del equipo accede al flujo que necesita sin intermediario.

**Inputs requeridos:**
- `3A.6.1` Interactive Prototype — prototipo con flows
- `3A.6.2` Main Flow Prototype — starting point del main flow
- `3A.6.3` Secondary Flows — starting points de secondary flows

**Dependencias (predecessors):**
- `3A.6.1` Interactive Prototype *(obligatorio)*

**Habilita (successors):**
- `3A.8.2` Test Script — links para participantes de testing
- Stakeholder reviews — links para presentaciones
- Developer reference — links para consulta

**Audiencia:**
- **Todos** — acceso self-service al prototipo

**Secciones esperadas:**
1. Tabla de links (flujo, device, starting point, URL, permisos)
2. Instrucciones de uso (cómo navegar, cómo reportar issues)
3. Permisos configurados (quién puede acceder)
4. Version/date del prototipo linkeado

**Criterio de completitud:**
- [ ] Un link por flujo principal (desktop y mobile)
- [ ] Starting points correctos configurados
- [ ] Permisos de acceso configurados
- [ ] Links funcionales verificados
- [ ] Instrucciones de uso incluidas

**Anti-patrones:**
- ❌ **Un solo link para todo:** Un link genérico al Figma file — el usuario no sabe dónde empezar.
- ❌ **Links rotos:** Prototipo actualizado pero links apuntan a frames viejos — confusión.
- ❌ **Sin permisos:** Link que requiere login en Figma — participantes de testing no pueden acceder.

**Template:** `phases/03-design/deliverables/prototype-links.md` *(pendiente)*

---

### 3A.6.6 Prototype Documentation

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.6 Prototypes |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de documentar las limitaciones y scope del prototipo para que los usuarios del prototipo (testers, stakeholders) entiendan qué funciona y qué no.  
En VTT: un agente puede generar la documentación del prototipo a partir de los flows prototipados y las limitaciones conocidas. Es altamente delegable. Necesita brief con: lista de flows, qué funciona, qué no, y limitaciones conocidas.

**Qué es:** Guía de uso del prototipo: qué flujos están prototipados, qué funciona (clickeable, navegable), qué NO funciona (formularios no validan, search no busca realmente, datos son estáticos), limitaciones conocidas, y cómo reportar issues encontrados. Es el "readme" del prototipo.

**Para qué sirve:** Un stakeholder que recibe el link del prototipo sin documentación no sabe: qué flujos probar, dónde empezar, qué es clickeable y qué no, ni qué bugs son "features del prototipo" vs problemas reales. La documentación contextualiza el prototipo para que se use correctamente.

**Inputs requeridos:**
- `3A.6.1` Interactive Prototype — prototipo a documentar
- `3A.6.5` Prototype Links — links a referenciar
- Lista de limitaciones conocidas

**Dependencias (predecessors):**
- `3A.6.1` Interactive Prototype *(obligatorio)*
- `3A.6.5` Prototype Links *(obligatorio)*

**Habilita (successors):**
- `3A.8.2` Test Script — moderador conoce limitaciones
- Stakeholder reviews — review informado

**Audiencia:**
- **Usability testing participants** — entender el scope
- **Stakeholders** — review informado
- **Design Lead** — verificación de scope

**Secciones esperadas:**
1. Overview (qué es el prototipo, para qué se usa)
2. Flujos disponibles (lista con links y descripción)
3. Qué funciona (interacciones, navegación, transiciones)
4. Qué NO funciona (formularios, search, datos dinámicos, responsive)
5. Limitaciones conocidas (dead ends intencionales, datos estáticos)
6. Instrucciones de navegación (cómo empezar, cómo reiniciar un flujo)
7. Cómo reportar issues
8. Versión y fecha del prototipo

**Criterio de completitud:**
- [ ] Flujos disponibles listados con links
- [ ] Limitaciones documentadas explícitamente
- [ ] Instrucciones de navegación claras
- [ ] Versión y fecha registradas
- [ ] Accesible por todos los stakeholders relevantes

**Anti-patrones:**
- ❌ **Sin documentación:** "Aquí está el prototipo, explórenlo" — el stakeholder hace click random y se frustra.
- ❌ **Sin limitaciones documentadas:** El tester reporta como "bug" que el formulario no valida — cuando es una limitación del prototipo.
- ❌ **Documentación desactualizada:** Documentación de la v1 cuando el prototipo va en v3.

**Template:** `phases/03-design/deliverables/prototype-documentation.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3A.6 Prototypes

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3A.6.1 Interactive Prototype | UI Designer | UI Designer | ❌ — trabajo de conexión visual en Figma |
| 3A.6.2 Main Flow Prototype | UI Designer | UI Designer | ❌ — subset del prototipo en Figma |
| 3A.6.3 Secondary Flows | UI Designer | UI Designer | ❌ — conexiones en Figma |
| 3A.6.4 Micro-interactions | UI Designer | UI Designer | 🔶 Parcial — puede especificar animaciones textualmente, no puede crearlas |
| 3A.6.5 Prototype Links | UI Designer | UI Designer | ✅ — puede documentar y verificar links |
| 3A.6.6 Prototype Documentation | UI Designer | UI Designer | ✅ — puede generar documentación completa del prototipo |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03A_07_DESIGN_SYSTEM.md` — 10 deliverables (3A.7.1 a 3A.7.10)  
*Nota: Este archivo ya fue generado previamente en esta sesión.*
