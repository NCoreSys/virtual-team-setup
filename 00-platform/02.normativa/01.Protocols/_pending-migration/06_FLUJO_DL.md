# 06 — FLUJO OPERATIVO DEL DESIGN LEAD

**Capa:** Estándar (genérico, portable)
**Audiencia:** Design Lead de cualquier proyecto gestionado en la plataforma
**Versión:** 1.0
**Complementa:** `00_INDEX.md`, `02_OPERACION_AGENTE.md`, `03_FLUJO_TL.md`

---

## 1. PROPÓSITO

Define el flujo de trabajo del Design Lead (DL) desde que recibe un handoff de diseño del PM/PJM hasta que cierra el ciclo con APR-DL y DL-REVIEW. Cubre gestión del Design System, creación de BRIEFs para el UX-Agent, QA Visual, handoff a FE y validación post-implementación.

> **Regla fundamental:** El DL NO genera HTML. El DL organiza, coordina, valida y revisa. El HTML lo genera el UX-Agent.

---

## 2. ROL DEL DL — COORDINADOR DE DISEÑO

**El DL es al diseño lo que el TL es al código.**

| Actividad | Quién |
|-----------|-------|
| Leer handoff del PM sobre diseño | DL |
| Gestionar Design System (tokens, foundations) | DL |
| Crear tareas en el sistema para UX | DL |
| Escribir BRIEFs y ASSIGNMENTs para UX | DL |
| **Generar HTML mockups** | **UX** |
| QA Visual (revisar outputs del UX) | DL |
| Mover tareas de diseño a `task_completed` | DL |
| Crear UX Specs (handoff a FE) | DL |
| Validar implementación FE (DL-REVIEW) | DL |
| Aprobar terminalmente (`task_approved`) | **PM** (nunca DL) |

---

## 3. LAS FASES DEL PROCESO DEL DL

### FASE 1 — Análisis del Handoff (al recibir HANDOFF_DL_S{XX}.md)

**Cuando el PM/PJM entrega un handoff de diseño, el DL NO empieza a crear tareas inmediatamente.** Primero analiza:

#### Paso 1 — Lectura estructural

- Leer el handoff completo
- Identificar pantallas a diseñar, estados requeridos, oleadas

#### Paso 2 — Extracción de datos por pantalla

| Dato | Fuente |
|------|--------|
| Estados requeridos | Sección "Estados a diseñar" del HO |
| Componentes nuevos vs existentes | `frontend/src/components/` (Glob) |
| Datos que muestra la pantalla | `backend/src/routes/[modulo].ts` |
| Responsive requerido | Sección de breakpoints del HO |
| Estimado y complejidad | Tabla de estimados del HO |

#### Paso 3 — Verificación de prerrequisitos

- ¿Existen los endpoints BE necesarios?
- ¿Existen los componentes UI referenciados?
- ¿Hay tokens que faltan en el Design System?

#### Paso 4 — Dependencias entre tareas

- Mapear cuáles pantallas bloquean a otras
- Identificar oleadas y gates intermedios

#### Paso 5 — Ambigüedades (detectar ANTES de crear BRIEFs)

> **Regla:** Ambigüedad → preguntar al PM ANTES de crear la tarea.

#### Paso 6 — Reporte al PM (antes de crear tareas)

- Confirmar alcance, dependencias y dudas detectadas

---

### FASE 2 — Creación de Tareas y BRIEFs

- Crear una tarea en el sistema por cada pantalla / bloque de diseño
- Escribir un BRIEF por cada tarea siguiendo el proceso detallado en sección 5
- Subir BRIEF como attachment (`fileType="brief"`)
- Asignar la tarea al UX-Agent (o solicitar al PM)

---

### FASE 3 — QA Visual (cuando UX entrega)

- El UX mueve la tarea a `in_review` con HTML + DevLog + comentario
- El DL compara HTML vs specs del BRIEF
- Aprueba, rechaza u observa

---

### FASE 4 — Handoff a FE

- Tras APR-DL, el DL crea UX Specs para las tareas FE
- Adjunta HTML aprobado + UX Spec
- Postea comentario de handoff en la tarea FE

---

### FASE 5 — DL-REVIEW

- Cuando FE pone tarea en `in_review`, el TL crea tarea DL-REVIEW
- DL valida implementación FE vs mockup aprobado
- Si hay discrepancias → comentario en la tarea DL-REVIEW (NO issue VTT)
- TL lee el comentario y crea fix tasks para FE

---

## 4. MAPA DE FUENTES DE VERDAD

| Capa | Fuente Primaria (verdad real) | Fuente Secundaria |
|------|-------------------------------|-------------------|
| **Tokens App** | `frontend/src/index.css` | DOC de Design System sección App |
| **Tokens Landing** | DOC de Design System sección Landing | `knowledge/design/` (specs copywriting) |
| **Componentes existentes** | `frontend/src/components/features/` + `frontend/src/components/ui/` | Handoff del sprint |
| **Páginas existentes** | `frontend/src/pages/` | DOC de flujo de pantallas |
| **Datos disponibles (API)** | `backend/src/routes/[modulo].ts` (solo leer) | Handoff TL / ASSIGNMENT |
| **Flujos de navegación** | `frontend/src/router/index.tsx` | DOC de flujo de pantallas |
| **Especificación de pantalla** | HANDOFF_DL_S{XX}.md | ASSIGNMENT de la tarea |
| **Mockups previos del DL** | `knowledge/design/sprint_XX/` | — |

### Reglas de jerarquía de diseño

- **Para la App:** `frontend/src/index.css` siempre gana sobre cualquier documento de especificación.
- **Para la Landing:** el DOC de Design System sección Landing es la fuente de tokens.
- **NUNCA mezclar tokens App con tokens Landing.** Son sistemas separados.

---

## 5. CADENA DE CONSULTA POR TIPO DE TAREA

### 5.1 APP — Crear BRIEF para el UX (tipo más común)

**Orden de consulta obligatorio antes de escribir el BRIEF:**

1. **HANDOFF del PM** — Leer completo. Identificar: qué pantallas crear, qué estados, qué componentes nuevos vs existentes.
2. **`frontend/src/components/features/`** — Verificar componentes similares existentes. Especificar en el BRIEF cuáles reusar y cuáles crear nuevos.
3. **`frontend/src/components/ui/`** — Componentes base disponibles (Button, Input, Modal, Badge). El BRIEF debe listar cuáles usar con sus nombres exactos.
4. **`frontend/src/index.css`** — Tokens disponibles. El BRIEF debe especificar tokens exactos a usar.
5. **`frontend/src/pages/`** — Patrones de layout existentes. El BRIEF debe indicar qué patrón heredar.
6. **`backend/src/routes/[modulo].ts`** — Campos reales de la API. El BRIEF debe especificar qué datos mostrar y cuándo ocurren los estados (vacío, error).

**Lo que cada fuente alimenta en el BRIEF:**

| Elemento del BRIEF | Fuente |
|--------------------|--------|
| Tokens CSS a usar | `frontend/src/index.css` |
| Componentes existentes a referenciar | `frontend/src/components/ui/` |
| Patrones de layout a heredar | `frontend/src/pages/` + features existentes |
| Estados loading/empty/error | `backend/src/routes/` |
| Pantallas y flujos a diseñar | HANDOFF_DL_S{XX}.md |

---

### 5.2 LANDING — Mockup de Componente de Marketing

**Orden de consulta obligatorio:**

1. **DOC de Design System sección Landing** — Tokens de la landing. Tema oscuro específico. NUNCA los tokens de la App.
2. **`frontend/src/components/landing/`** — Componentes landing ya implementados. Ver qué existe para no duplicar.
3. **`knowledge/design/`** — Specs de copywriting, assets, imágenes y guidelines de la landing.
4. **ASSIGNMENT de la tarea** — Qué componente / sección diseñar específicamente.

> **Regla crítica:** Si el mockup usa tokens del sistema App → está mal. La landing tiene su propio sistema de tokens.

---

### 5.3 DESIGN SYSTEM — Agregar o Modificar Tokens

**Orden de consulta obligatorio:**

1. **`frontend/src/index.css`** — Ver todos los tokens existentes. Verificar si el token que necesito YA existe con otro nombre antes de crear uno nuevo.
2. **DOC de Design System** — Convenciones de naming, categorías existentes.
3. **HANDOFF o ASSIGNMENT que solicita el nuevo token** — Confirmar el valor exacto pedido, no estimarlo.
4. **Componentes que usarán el token** — `frontend/src/components/` — Verificar cuántos componentes lo necesitarán para validar que el nombre es genérico suficiente.

**Reglas:**

- Naming: `--[prefijo-proyecto]-[categoría]-[variante]` (ej: `--vtt-wizard-step-size`)
- Documentar en `tokens/sXX_tokens.json` con nombre, valor y propósito
- NO modificar tokens existentes si hay componentes que los usan — crear variante nueva

---

### 5.4 QA VISUAL — Comparar Implementación FE vs Mockup (DL-REVIEW)

**Orden de consulta obligatorio:**

1. **Mockup HTML original del DL** — `knowledge/design/sprint_XX/[pantalla].html` — El DL abre su propio mockup para tener referencia exacta.
2. **Implementación FE real** — `frontend/src/pages/[Pagina].tsx` + `frontend/src/components/features/[Componente].tsx` — Leer el código implementado, no solo verlo en browser.
3. **ASSIGNMENT original** — Verificar los criterios de aceptación que el DL mismo especificó.

**Qué validar en QA Visual:**

| Elemento | Qué verificar |
|----------|---------------|
| Tokens | ¿El FE usa los mismos CSS vars que el mockup? |
| Layout | ¿El contenedor, padding, gap coinciden? |
| Estados | ¿Están todos los estados: loading, empty, error, disabled? |
| Responsive | ¿Los 3 breakpoints se comportan como el mockup? |
| Componentes | ¿Se usaron los componentes del mockup o se inventaron nuevos? |
| Iconos | ¿Los iconos son los mismos (Lucide, etc.) con el mismo nombre? |

**Resultado del QA:**

- Sin diferencias / diferencias menores → comentar en tarea + mover a `completed`
- Diferencias significativas → comentar con discrepancias + dejar en `in_review`

> ⚠️ **REGLA CRÍTICA DL-REVIEW:** Las discrepancias en implementación FE van como **comentario en la tarea DL-REVIEW** — NO crear issues VTT. Crear un issue en VTT pone la tarea en `on_hold` automáticamente y rompe el flujo de cierre. El TL lee el comentario y crea fix tasks para FE.

---

## 6. PROCESO PASO A PASO PARA CREAR BRIEF PARA EL UX

### Paso A — Leer el Handoff del PM (obligatorio)

```
1. Abrir: HANDOFF_DL_S{XX}.md
2. Identificar por cada pantalla:
   - Nombre y propósito
   - Elementos requeridos
   - Estados a diseñar
   - Comportamientos y reglas
3. Mapear dependencias entre pantallas
4. NO escribir el BRIEF hasta tener claro el scope completo
```

### Paso B — Auditar componentes existentes (incluir en BRIEF)

```
1. Glob: frontend/src/components/features/*.tsx
   → Listar en el BRIEF: "Componente X ya existe — UX debe ser coherente"

2. Glob: frontend/src/components/ui/*.tsx
   → Listar en el BRIEF: "Usar <Button variant='primary'>, <Badge>, etc."

3. Glob: frontend/src/pages/*.tsx
   → Indicar en el BRIEF: "Heredar patrón de layout de [Página]"
```

### Paso C — Verificar tokens reales (incluir en BRIEF)

```
1. Abrir: frontend/src/index.css
2. Identificar tokens relevantes para la pantalla:
   - Colores: --[proyecto]-text-primary, --[proyecto]-border, etc.
   - Sombras: --[proyecto]-shadow-card, --[proyecto]-shadow-modal
3. Incluir en el BRIEF: lista de tokens que el UX DEBE usar
4. Incluir tokens nuevos si aplica (sXX_tokens.json)
```

### Paso D — Verificar datos reales de API (incluir en BRIEF)

```
1. Abrir: backend/src/routes/[modulo].ts
   → ¿Qué campos devuelve el endpoint de esta pantalla?
2. Incluir en el BRIEF:
   - Campos reales disponibles
   - Cuándo ocurre el estado vacío (lista = [])
   - Cuándo ocurre el estado error (500/404)
3. Especificar: "UX NO debe diseñar campos que la API no devuelve"
```

### Paso E — Definir breakpoints en el BRIEF

```
1. Especificar los 3 breakpoints obligatorios:
   - Desktop: ≥1024px
   - Tablet: 768-1023px
   - Mobile: <768px
2. Si hay drag-and-drop: indicar "incluir alternativa mobile con botones up/down"
```

---

## 7. ESTRUCTURA OBLIGATORIA DEL BRIEF PARA EL UX

Cada BRIEF debe incluir:

```markdown
# BRIEF: [TASK_ID] — [Nombre Pantalla]
Sprint: S{XX} | Tarea: [TASK_ID] | Para: UX-Agent

## Pantallas a diseñar
- [Lista de pantallas con sus estados requeridos]

## Tokens a usar (de frontend/src/index.css)
- --[token-1]: [valor] — [uso]
- --[token-2]: [valor] — [uso]
[solo los relevantes]

## Componentes existentes a referenciar
- <Button variant="primary"> — frontend/src/components/ui/Button.tsx
- [lista de componentes base con sus rutas]

## Componentes nuevos a crear
- [NombreComponente] — descripción y props esperadas

## Datos reales de API
- Endpoint: [MÉTODO] /api/[modulo]
- Campos disponibles: [lista desde backend/src/routes/]
- Estado vacío: cuando [...] → mostrar [...]
- Estado error: cuando 500/404 → mostrar [...]

## Breakpoints requeridos
- Desktop ≥1024px, Tablet 768-1023px, Mobile <768px
- [Notas específicas de adaptación]

## Estados por pantalla
- default, hover, active, disabled, error, loading, empty

## Template a usar (por tipo de pantalla)
- [TEMPLATE_BASE_Spec_[Tipo]_v2.md]

## Entrega esperada
- knowledge/design/sprint_XX/[nombre].html (uno por pantalla)
```

---

## 8. TEMPLATES DISPONIBLES PARA EL UX

Ubicación estándar: `Project_setup/templates/Design/` (o espejo en `knowledge/design/TEMPLATE/` del proyecto)

| Tipo de pantalla | Template |
|-----------------|----------|
| Wizard multi-paso | `TEMPLATE_BASE_Spec_Wizard_v2.md` |
| Formulario / Settings | `TEMPLATE_BASE_Spec_Form_v2.md` |
| Modal o drawer | `TEMPLATE_BASE_Spec_ModalOverlay_v2.md` |
| Pantalla genérica App | `TEMPLATE_BASE_Spec_AppScreen_v2.md` |
| Tabla/lista de datos | `TEMPLATE_BASE_Spec_DataGrid_v2.md` |
| Dashboard/métricas | `TEMPLATE_BASE_Spec_DashboardKPI_v2.md` |
| Detalle de entidad | `TEMPLATE_BASE_Spec_EntityDetail_v2.md` |
| Estados UI globales | `TEMPLATE_BASE_Spec_UXStates_v2.md` |
| Landing page | `TEMPLATE_BASE_Spec_Landing_v2.md` |
| Admin / RBAC | `TEMPLATE_BASE_Spec_AdminRBAC_v2.md` |
| Checkout / pago | `TEMPLATE_BASE_Spec_Checkout_v2.md` |
| Content / SEO | `TEMPLATE_BASE_Spec_ContentSEO_v2.md` |
| Notificación | `TEMPLATE_BASE_Spec_Notification_v2.md` |
| Búsqueda semántica | `TEMPLATE_BASE_Spec_SemanticSearch_v2.md` |

**Documentos auxiliares:**

| Documento | Propósito |
|-----------|-----------|
| `index_templates_specs_v2.md` | Índice de todos los templates con matriz de decisión |
| `catalogo_maestro_templates_specs_uiux_v2.md` | Catálogo maestro con casos de uso por template |
| `GUIA_Design_Tokens_Checklist.md` | Checklist de tokens a validar antes de entregar BRIEF |
| `template_base_especificacion_funcional_uiux.md` | Template base de especificación funcional |
| `README_base_conocimiento_templates_specs_v2.md` | Guía de uso de la base de templates |

> Al escribir un BRIEF para UX: leer el template correspondiente, extraer la estructura relevante e incluirla en el BRIEF.

---

## 9. PROCESO DE HANDOFF A FE (después de APR-DL)

**TRIGGER:** APR-DL completado por el PM.

### Pasos

```
1. Crear UX Spec por pantalla aprobada:
   - Estados y variantes
   - Componentes nuevos (nombre, props esperadas, variantes)
   - Componentes existentes a reutilizar (ruta exacta en /src)
   - Datos de API que alimentan la pantalla
   - CAs de accesibilidad
2. Localizar tareas FE en el sistema
3. Adjuntar HTML aprobado + UX Spec en tarea FE (fileType="spec")
4. Postear comentario en tarea FE con estructura de handoff
```

### Template de comentario handoff DL → FE

```markdown
## Handoff DL → FE: {nombre pantalla}

**Archivos de referencia:**
- HTML: knowledge/design/sprint_XX/{nombre}.html
- UX Spec: knowledge/design/sprint_XX/{nombre}.SPEC.md
- Tokens: knowledge/design/sprint_XX/tokens/sXX_tokens.json

**Componentes nuevos a implementar:**
- {ComponentName} — {descripción, props principales}

**Componentes existentes a reutilizar:**
- {ComponentName} → frontend/src/components/{ruta}

**CAs de accesibilidad obligatorios:**
- Contraste WCAG AA en todos los textos
- Touch targets ≥44px en mobile

**Notas para TL:**
- {dudas técnicas que FE debe confirmar con TL}
```

---

## 10. CHECKLISTS OPERATIVAS

### Checklist DL — Antes de entregar BRIEF al UX

```
[ ] ¿Leí el handoff completo del PM?
[ ] ¿Audité componentes existentes en frontend/src/components/?
[ ] ¿Verifiqué tokens reales en frontend/src/index.css?
[ ] ¿Verifiqué campos reales de API en backend/src/routes/?
[ ] ¿El BRIEF especifica tokens exactos (no inventados)?
[ ] ¿El BRIEF lista componentes existentes a referenciar?
[ ] ¿El BRIEF especifica todos los estados por pantalla?
[ ] ¿El BRIEF incluye los 3 breakpoints?
[ ] ¿El BRIEF indica el template a usar (por tipo de pantalla)?
[ ] ¿El BRIEF indica la ubicación de entrega: knowledge/design/sprint_XX/?
[ ] ¿Cambié status de mi tarea a in_progress al empezar?
[ ] ¿Asigné la tarea al UX-Agent?
[ ] ¿Adjunté el BRIEF como attachment (fileType="brief")?
```

### Checklist DL — QA Visual (tras entrega del UX)

```
[ ] ¿Los tokens en el HTML coinciden con lo especificado en el BRIEF?
[ ] ¿Se usaron los componentes indicados (no duplicados)?
[ ] ¿Están todos los estados: default, hover, active, disabled, error, loading, empty?
[ ] ¿Los 3 breakpoints están implementados?
[ ] ¿Contraste WCAG AA (texto ≥4.5:1, UI ≥3:1)?
[ ] ¿El HTML renderiza standalone sin errores?
[ ] ¿Si había drag-and-drop: está la alternativa mobile?
[ ] ¿El nombre del archivo sigue nomenclatura ({módulo}-{pantalla}.html)?
[ ] ¿Comenté en la tarea con resultado del QA?
[ ] ¿Cambié status a `completed` al aprobar?
```

### Checklist DL — Handoff a FE (post APR-DL)

```
[ ] ¿Creé UX Spec por cada pantalla aprobada?
[ ] ¿Adjunté HTML aprobado + UX Spec en tarea FE (fileType="spec")?
[ ] ¿Posteé comentario de handoff con componentes nuevos vs existentes?
[ ] ¿Incluí CAs de accesibilidad?
[ ] ¿Notifiqué al TL que FE puede arrancar?
```

### Checklist DL — DL-REVIEW (post implementación FE)

```
[ ] ¿Abrí mi mockup HTML original?
[ ] ¿Leí el código FE implementado (no solo el browser)?
[ ] ¿Verifiqué tokens, layout, estados, responsive, componentes?
[ ] Si hay discrepancias → ¿las listé como COMENTARIO (no issue)?
[ ] ¿Reporté al TL para que cree fix tasks?
[ ] Si todo OK → ¿moví DL-REVIEW a completed?
```

---

## 11. ERRORES FRECUENTES DEL DL (APRENDER DE ESTOS)

| Error | Consecuencia | Corrección |
|-------|--------------|------------|
| **Generar HTML tú mismo** | DL no es el UX | Crear tarea y BRIEF para el UX |
| BRIEF con tokens inventados | UX hardcodea colores | Verificar `frontend/src/index.css` |
| BRIEF sin auditar componentes existentes | UX duplica componentes | Auditar `components/` primero |
| BRIEF sin estados especificados | UX omite loading/empty/error | Siempre listar todos los estados |
| BRIEF sin breakpoints | UX omite mobile | Siempre 3 breakpoints |
| BRIEF con campos que API no devuelve | FE no puede implementar | Leer `routes/` antes |
| QA sin comentar resultado | TL no puede validar | Siempre comentar en tarea |
| Crear issue VTT en DL-REVIEW | Tarea FE va a `on_hold` automáticamente y bloquea cierre | Usar comentario, dejar que TL cree fix tasks |
| Mezclar tokens App con Landing | Incoherencia visual | Son sistemas separados |

---

## 12. INTEGRACIÓN CON OTROS FLUJOS

```
PM entrega HANDOFF_DL_S{XX}.md al DL
      ↓
[FASE 1 DL] Análisis del handoff (Pasos 1-6)
      ↓
[FASE 2 DL] Crear tareas + BRIEFs para UX
      ↓
      ├─────────────────────────────────────┐
      ↓                                      ↓
UX genera HTMLs            (en paralelo, si aplica)
      ↓                     TL avanza con BE/FE
[FASE 3 DL] QA Visual
      ↓
(si aprobado) APR-DL → PM aprueba
      ↓
[FASE 4 DL] Crear UX Specs y handoff a FE
      ↓
FE implementa
      ↓
FE pone tarea en in_review → TL crea DL-REVIEW
      ↓
[FASE 5 DL] DL-REVIEW (validar FE vs mockup)
      ↓
(si OK) Sprint cerrado
```

---

## 13. LO QUE NO HACE ESTE PROCESO

- **No reemplaza leer el ASSIGNMENT** — El proceso complementa el assignment, no lo reemplaza. Si el assignment dice algo distinto al HANDOFF, el assignment tiene prioridad (es más reciente).
- **No aplica a QA de código** — El DL valida visual/UX, no lógica de negocio ni funcionamiento de API.
- **No autoriza modificar componentes FE** — El DL solo diseña. Si detecta que un componente existente necesita cambios, crear un issue para el Frontend Dev (NO en DL-REVIEW).
- **No genera assets finales** — Los mockups son especificación visual para el FE, no implementación final.
- **No decide la arquitectura de componentes** — Si hay duda sobre si crear componente nuevo o extender uno existente, crear issue y esperar decisión del TL.

---

## 14. DOCUMENTOS RELACIONADOS

| Documento | Propósito |
|-----------|-----------|
| `00_INDEX.md` | Jerarquía y precedencia de documentos |
| `01_ONBOARDING.md` | Taxonomía del sistema |
| `02_OPERACION_AGENTE.md` | Reglas operativas comunes a todos los agentes |
| `03_FLUJO_TL.md` | Flujo del Tech Lead (referencia cruzada — TL y DL colaboran) |
| `04_ESTRUCTURA_FASES.md` | Layout de carpetas por fase |
| `05_CATALOGO_DELIVERABLES.md` | 438 deliverables por fase (relevante para Fase 3A Design UX/UI) |
| `roles/AGENT_PROFILE_BASE_DL.md` | Perfil base del rol DL |
| `OPERATIVO_[PROYECTO]_DESIGN_LEAD.md` | Instancia específica del proyecto |
| `PROJECT_MEMORY.md` | Memoria del proyecto |
| `CONTEXTO_DL_SESION.md` | Estado actual del sprint (live) |

---

## 15. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-20 | Versión inicial consolidada desde `07.PROCESO_CONSULTA_DOCS_DL.md` v1.0 + parte genérica de `OPERATIVO_DESIGN_LEAD.md` del proyecto VTT. Extracción de la capa portable. |

---

**Fuente de verdad de este documento:** `Project_setup/standard/06_FLUJO_DL.md`
