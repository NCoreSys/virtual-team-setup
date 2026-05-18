# 📘 TEMPLATE BASE — SPEC APPSCREEN (Web/Mobile Product Screen)

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P1 — Core  
> **Última actualización:** {{FECHA_ACTUALIZACION}}

---

## 🔖 GUÍA DE USO DEL TEMPLATE

### Marcadores de obligatoriedad

| Marcador | Significado | Regla |
|----------|-------------|-------|
| `[OBL]` | **Obligatorio** | Siempre debe completarse |
| `[OPC]` | **Opcional** | Completar si aplica al proyecto |
| `[COND]` | **Condicional** | Completar solo si se cumple la condición indicada |

### Placeholders

- `{{NOMBRE}}` → Reemplazar con valor específico del proyecto
- `[Elegir: opción1 / opción2]` → Seleccionar una opción
- `[Listar...]` → Agregar items según aplique

### Reglas de activación

Cada sección indica cuándo debe incluirse. Si no aplica, **omitir la sección completa** (no dejar vacía).

---

# ESPECIFICACIÓN FUNCIONAL + UI/UX — APPSCREEN

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_{{NOMBRE_PANTALLA}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{NOMBRE_MODULO}} |
| **Pantalla / Vista** | {{NOMBRE_PANTALLA}} |
| **ID técnico** | `{{PREFIJO}}-{{NUM}}-{{SLUG}}` (ej: `screen-01-home-feed`) |
| **Versión** | {{VERSION}} (ej: v1.0) |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Tipo** | [Elegir: Mobile / Web / Responsive / Desktop / Tablet] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_PM}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito de la pantalla [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Esta pantalla permite a **{{TIPO_USUARIO}}** realizar **{{ACCION_PRINCIPAL}}**.

- **Función dentro del sistema:** {{ROL_EN_FLUJO}}
- **Clasificación:** [Elegir: MVP / Fase 2 / Enterprise-only / Admin-only]

### 1.2 Objetivos de negocio [OBL]

1. {{OBJETIVO_NEGOCIO_1}}
2. {{OBJETIVO_NEGOCIO_2}}
3. {{OBJETIVO_NEGOCIO_3}}

### 1.3 Objetivos UX [OBL]

1. {{OBJETIVO_UX_1}} (ej: reducir fricción, mejorar discovery, aumentar conversión)
2. {{OBJETIVO_UX_2}}
3. {{OBJETIVO_UX_3}}

### 1.4 KPIs / Métricas objetivo [OBL]

| Métrica | Valor objetivo | Método de medición |
|---------|----------------|-------------------|
| CTR esperado | {{VALOR}} | {{METODO}} |
| Tiempo promedio en pantalla | {{VALOR}} | {{METODO}} |
| Tasa de conversión | {{VALOR}} | {{METODO}} |
| Errores UX tolerables | {{VALOR}} | {{METODO}} |
| Retención / retorno | {{VALOR}} | {{METODO}} |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{FUNCIONALIDAD_1}}
- {{FUNCIONALIDAD_2}}
- {{FUNCIONALIDAD_3}}

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUSION_1}}
- {{EXCLUSION_2}}
- {{EXCLUSION_3}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| API | {{ENDPOINT}} | [Elegir: Disponible / En desarrollo / Pendiente] | {{OWNER}} |
| Auth | {{SISTEMA_AUTH}} | [Elegir: Disponible / En desarrollo / Pendiente] | {{OWNER}} |
| Feature Flag | {{FLAG_NAME}} | [Elegir: Activo / Inactivo] | {{OWNER}} |
| Componente compartido | {{COMPONENTE}} | [Elegir: Disponible / En desarrollo] | {{OWNER}} |

---

## 3) Usuarios, roles y permisos [COND]

> **Activación:** Incluir si hay múltiples roles o permisos diferenciados. Si es pantalla pública sin roles, omitir.

### 3.1 Matriz de permisos por rol [COND]

| Rol | Puede ver | Puede interactuar | Puede editar | Puede aprobar | Restricciones |
|-----|-----------|-------------------|--------------|---------------|---------------|
| {{ROL_1}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{RESTRICCION}} |
| {{ROL_2}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{RESTRICCION}} |
| {{ROL_ADMIN}} | ✅ | ✅ | ✅ | ✅ | {{RESTRICCION}} |

### 3.2 Usuarios objetivo (UX) [OBL]

| Tipo | Descripción | Frecuencia de uso |
|------|-------------|-------------------|
| Usuario primario | {{DESCRIPCION}} | {{FRECUENCIA}} |
| Usuario secundario | {{DESCRIPCION}} | {{FRECUENCIA}} |
| Usuario ocasional | {{DESCRIPCION}} | {{FRECUENCIA}} |

### 3.3 Variaciones por rol [COND]

| Elemento | Cambio por rol | Roles afectados |
|----------|----------------|-----------------|
| UI visible | {{CAMBIO}} | {{ROLES}} |
| Data visible | {{CAMBIO}} | {{ROLES}} |
| Navegación | {{CAMBIO}} | {{ROLES}} |
| Copy / CTA | {{CAMBIO}} | {{ROLES}} |

---

## 4) Contexto dentro del flujo (Journey) [OBL]

> **Activación:** Siempre obligatorio.

### 4.1 Puntos de entrada [OBL]

| Origen | Contexto | Datos que trae |
|--------|----------|----------------|
| {{ORIGEN_1}} | {{CONTEXTO}} | {{DATOS}} |
| {{ORIGEN_2}} | {{CONTEXTO}} | {{DATOS}} |
| {{ORIGEN_3}} | {{CONTEXTO}} | {{DATOS}} |

### 4.2 Puntos de salida [OBL]

| Destino | Trigger | Datos que lleva |
|---------|---------|-----------------|
| {{DESTINO_1}} | {{TRIGGER}} | {{DATOS}} |
| {{DESTINO_2}} | {{TRIGGER}} | {{DATOS}} |
| {{DESTINO_3}} | {{TRIGGER}} | {{DATOS}} |

### 4.3 Flujo principal (Happy Path) [OBL]

```
1. Usuario entra desde {{ORIGEN}}
2. Sistema muestra {{CONTENIDO_INICIAL}}
3. Usuario visualiza {{CONTENIDO_CLAVE}}
4. Usuario interactúa con {{COMPONENTE_PRINCIPAL}}
5. Sistema responde con {{RESULTADO}}
6. Usuario continúa a {{SIGUIENTE_PANTALLA}}
```

### 4.4 Flujos alternos [OPC]

| Flujo | Trigger | Comportamiento |
|-------|---------|----------------|
| Búsqueda rápida | {{TRIGGER}} | {{COMPORTAMIENTO}} |
| Filtrado | {{TRIGGER}} | {{COMPORTAMIENTO}} |
| Sin resultados | {{TRIGGER}} | {{COMPORTAMIENTO}} |
| Error | {{TRIGGER}} | {{COMPORTAMIENTO}} |
| Cancelación / regreso | {{TRIGGER}} | {{COMPORTAMIENTO}} |

---

## 5) Inventario de componentes UI [OBL]

> **Activación:** Siempre obligatorio. Es la sección núcleo del template.

### 5.1 Lista de componentes [OBL]

| ID | Nombre | Tipo | Reutilizable | Prioridad | Fuente | Estado |
|----|--------|------|--------------|-----------|--------|--------|
| `cmp-01` | {{NOMBRE}} | {{TIPO}} | Sí/No | [Crítica/Alta/Media/Baja] | [DS/Shared/Nuevo] | [Listo/En desarrollo/Pendiente] |
| `cmp-02` | {{NOMBRE}} | {{TIPO}} | Sí/No | [Crítica/Alta/Media/Baja] | [DS/Shared/Nuevo] | [Listo/En desarrollo/Pendiente] |
| `cmp-03` | {{NOMBRE}} | {{TIPO}} | Sí/No | [Crítica/Alta/Media/Baja] | [DS/Shared/Nuevo] | [Listo/En desarrollo/Pendiente] |

### 5.2 Jerarquía visual [OBL]

| Nivel | Componentes | Justificación |
|-------|-------------|---------------|
| **Primario** | {{COMPONENTES}} | {{JUSTIFICACION}} |
| **Secundario** | {{COMPONENTES}} | {{JUSTIFICACION}} |
| **Terciario** | {{COMPONENTES}} | {{JUSTIFICACION}} |

### 5.3 Clasificación de componentes [OBL]

| Categoría | Componentes | Notas |
|-----------|-------------|-------|
| **Obligatorios** | {{LISTA}} | Siempre visibles |
| **Opcionales** | {{LISTA}} | Según contexto |
| **Condicionales** | {{LISTA}} | Según estado/rol/data |

---

## 6) Especificación por componente [OBL]

> **Activación:** Repetir esta sección por cada componente crítico (prioridad Crítica o Alta).

---

### 6.X {{NOMBRE_COMPONENTE}} [OBL por componente crítico]

#### a) Identificación [OBL]

| Campo | Valor |
|-------|-------|
| **ID** | `cmp-{{NUM}}` |
| **Nombre técnico** | `{{slug-componente}}` |
| **Tipo** | [Elegir: Card / Input / Button / Modal / Tab / List / Navigation / Other] |
| **Reutilizable** | Sí / No |
| **Owner** | [Elegir: Design System / Frontend / Feature Team] |

#### b) Propósito [OBL]

{{DESCRIPCION_PROPOSITO}}

#### c) Estructura interna [OBL]

| Elemento | Requerido | Fuente de datos | Fallback |
|----------|-----------|-----------------|----------|
| {{ELEMENTO_1}} | Sí/No | {{CAMPO_API}} | {{FALLBACK}} |
| {{ELEMENTO_2}} | Sí/No | {{CAMPO_API}} | {{FALLBACK}} |
| {{ELEMENTO_3}} | Sí/No | {{CAMPO_API}} | {{FALLBACK}} |

#### d) Variantes [OPC]

| Variante | Cuándo aplica | Diferencias |
|----------|---------------|-------------|
| Default | {{CONDICION}} | — |
| Compact | {{CONDICION}} | {{DIFERENCIAS}} |
| Expanded | {{CONDICION}} | {{DIFERENCIAS}} |
| Mobile | {{CONDICION}} | {{DIFERENCIAS}} |
| Desktop | {{CONDICION}} | {{DIFERENCIAS}} |
| Read-only | {{CONDICION}} | {{DIFERENCIAS}} |

#### e) Estados visuales [OBL]

| Estado | Apariencia | Trigger |
|--------|------------|---------|
| `default` | {{DESCRIPCION}} | Estado inicial |
| `hover` | {{DESCRIPCION}} | Mouse over (si aplica) |
| `focus` | {{DESCRIPCION}} | Foco de teclado |
| `pressed` | {{DESCRIPCION}} | Click/tap activo |
| `disabled` | {{DESCRIPCION}} | {{CONDICION}} |
| `loading` | {{DESCRIPCION}} | Cargando datos |
| `empty` | {{DESCRIPCION}} | Sin datos |
| `error` | {{DESCRIPCION}} | Error en datos/acción |
| `selected` | {{DESCRIPCION}} | Selección activa |

#### f) Reglas de comportamiento [OBL]

| Evento | Comportamiento | Notas |
|--------|----------------|-------|
| Click/Tap | {{COMPORTAMIENTO}} | {{NOTAS}} |
| Sin data | {{COMPORTAMIENTO}} | {{NOTAS}} |
| Texto largo | {{COMPORTAMIENTO}} | (truncar, wrap, tooltip) |
| Imagen falla | {{COMPORTAMIENTO}} | {{NOTAS}} |
| Sin permisos | {{COMPORTAMIENTO}} | {{NOTAS}} |

#### g) Specs visuales (UI) [OPC]

| Propiedad | Valor | Token (si aplica) |
|-----------|-------|-------------------|
| Width | {{VALOR}} | {{TOKEN}} |
| Height | {{VALOR}} | {{TOKEN}} |
| Padding | {{VALOR}} | {{TOKEN}} |
| Gap | {{VALOR}} | {{TOKEN}} |
| Border radius | {{VALOR}} | {{TOKEN}} |
| Shadow | {{VALOR}} | {{TOKEN}} |
| Typography | {{VALOR}} | {{TOKEN}} |
| Color | {{VALOR}} | {{TOKEN}} |

#### h) Responsive [OPC]

| Breakpoint | Comportamiento |
|------------|----------------|
| Mobile (320-767) | {{COMPORTAMIENTO}} |
| Tablet (768-1023) | {{COMPORTAMIENTO}} |
| Desktop (1024+) | {{COMPORTAMIENTO}} |

#### i) Accesibilidad (A11Y) [OBL]

| Requisito | Implementación |
|-----------|----------------|
| `aria-label` | {{VALOR}} |
| Orden de tab | {{POSICION}} |
| Soporte teclado | {{TECLAS}} |
| Target táctil | Mínimo 44x44px |
| Contraste | WCAG AA (4.5:1) |
| Screen reader | {{TEXTO_ANUNCIADO}} |

#### j) Analytics [COND]

> **Activación:** Incluir si el componente tiene interacciones trackeables.

| Evento | Trigger | Payload |
|--------|---------|---------|
| `{{EVENTO_VIEW}}` | Componente visible | `screen_id, component_id` |
| `{{EVENTO_CLICK}}` | Click/tap | `screen_id, component_id, item_id, position` |
| `{{EVENTO_ERROR}}` | Error mostrado | `screen_id, component_id, error_type` |

---

## 7) Layout y estructura de pantalla [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Estructura general [OBL]

```
┌─────────────────────────────────────┐
│            HEADER / TOP BAR         │
├─────────────────────────────────────┤
│  SIDEBAR  │    CONTENIDO PRINCIPAL  │
│  (si hay) │                         │
│           │                         │
├───────────┴─────────────────────────┤
│         FOOTER / BOTTOM NAV         │
└─────────────────────────────────────┘
```

**Zonas activas en esta pantalla:**
- [ ] Header / Top bar
- [ ] Zona de filtros
- [ ] Sidebar
- [ ] Contenido principal
- [ ] Footer / Bottom nav
- [ ] Overlays (modal, drawer, toast)

### 7.2 Grid / Layout system [OBL]

| Propiedad | Valor |
|-----------|-------|
| Tipo de layout | [Elegir: Flex / Grid / Mixto] |
| Columnas | {{NUM_COLUMNAS}} |
| Gap | {{VALOR}} |
| Max width | {{VALOR}} |
| Container padding | {{VALOR}} |

### 7.3 Jerarquía de zonas [OBL]

| Zona | Descripción | Prioridad | Sticky | Scroll |
|------|-------------|-----------|--------|--------|
| Header | {{DESCRIPCION}} | [Alta/Media/Baja] | Sí/No | No |
| Sidebar | {{DESCRIPCION}} | [Alta/Media/Baja] | Sí/No | Sí/No |
| Main Content | {{DESCRIPCION}} | Crítica | No | Sí |
| Footer/Nav | {{DESCRIPCION}} | [Alta/Media/Baja] | Sí/No | No |

---

## 8) Navegación y comportamiento [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Rutas [OBL]

| Tipo | Valor |
|------|-------|
| Ruta URL | `{{RUTA}}` (ej: `/dashboard/home`) |
| Ruta técnica interna | `{{RUTA_INTERNA}}` (si difiere) |
| Deep links | {{DEEP_LINKS}} |
| Parámetros URL | {{PARAMS}} (ej: `?tab=`, `&filter=`) |

### 8.2 Acciones de navegación [OBL]

| Acción | Trigger | Destino | Tipo | Animación |
|--------|---------|---------|------|-----------|
| {{ACCION_1}} | {{TRIGGER}} | `{{RUTA}}` | [Push/Pop/Replace/Modal] | {{ANIMACION}} |
| {{ACCION_2}} | {{TRIGGER}} | `{{RUTA}}` | [Push/Pop/Replace/Modal] | {{ANIMACION}} |
| Back | Back nav / gesture | Pantalla anterior | Pop | {{ANIMACION}} |

### 8.3 Persistencia de estado [OBL]

| Estado | Persiste al salir | Persiste al volver | Storage |
|--------|-------------------|-------------------|---------|
| Scroll position | Sí/No | Sí/No | {{STORAGE}} |
| Filtros aplicados | Sí/No | Sí/No | {{STORAGE}} |
| Tab activa | Sí/No | Sí/No | {{STORAGE}} |
| Form parcial | Sí/No | Sí/No | {{STORAGE}} |

---

## 9) Datos y contratos (API Mapping) [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 Fuentes de datos [OBL]

| Fuente | Tipo | Prioridad | Fallback |
|--------|------|-----------|----------|
| {{FUENTE_1}} | [REST/GraphQL/Cache/Mock] | {{PRIORIDAD}} | {{FALLBACK}} |
| {{FUENTE_2}} | [REST/GraphQL/Cache/Mock] | {{PRIORIDAD}} | {{FALLBACK}} |

### 9.2 Endpoints [OBL]

| Endpoint | Método | Uso | Prioridad | Cache TTL | Owner |
|----------|--------|-----|-----------|-----------|-------|
| `{{ENDPOINT_1}}` | GET/POST | {{USO}} | {{PRIORIDAD}} | {{TTL}} | {{OWNER}} |
| `{{ENDPOINT_2}}` | GET/POST | {{USO}} | {{PRIORIDAD}} | {{TTL}} | {{OWNER}} |

### 9.3 Mapping de datos por componente [OBL]

| Componente | Campo UI | Campo API | Tipo | Requerido | Fallback |
|------------|----------|-----------|------|-----------|----------|
| {{COMPONENTE}} | {{CAMPO_UI}} | `{{campo_api}}` | {{TIPO}} | Sí/No | {{FALLBACK}} |
| {{COMPONENTE}} | {{CAMPO_UI}} | `{{campo_api}}` | {{TIPO}} | Sí/No | {{FALLBACK}} |

### 9.4 Validaciones de datos [OPC]

| Campo | Validación | Mensaje de error |
|-------|------------|------------------|
| {{CAMPO}} | {{REGLA}} | {{MENSAJE}} |
| {{CAMPO}} | {{REGLA}} | {{MENSAJE}} |

### 9.5 Estrategia de cache [OPC]

| Endpoint | TTL | Invalidación | Fallback offline |
|----------|-----|--------------|------------------|
| {{ENDPOINT}} | {{TTL}} | {{EVENTO}} | {{FALLBACK}} |

---

## 10) Reglas de negocio [OBL]

> **Activación:** Siempre obligatorio.

### 10.1 Reglas funcionales [OBL]

| ID | Regla | Componentes afectados | Prioridad |
|----|-------|----------------------|-----------|
| BR-01 | {{REGLA}} | {{COMPONENTES}} | {{PRIORIDAD}} |
| BR-02 | {{REGLA}} | {{COMPONENTES}} | {{PRIORIDAD}} |
| BR-03 | {{REGLA}} | {{COMPONENTES}} | {{PRIORIDAD}} |

### 10.2 Reglas por rol [COND]

> **Activación:** Incluir solo si hay diferencias por rol.

| Rol | Regla específica |
|-----|------------------|
| {{ROL}} | {{REGLA}} |

### 10.3 Reglas de ordenamiento/prioridad [OPC]

| Contenido | Criterio de orden | Dirección |
|-----------|-------------------|-----------|
| {{CONTENIDO}} | {{CRITERIO}} | [ASC/DESC] |

### 10.4 Reglas de visibilidad condicional [OPC]

| Elemento | Condición para mostrar | Condición para ocultar |
|----------|------------------------|------------------------|
| {{ELEMENTO}} | {{CONDICION_SHOW}} | {{CONDICION_HIDE}} |

---

## 11) Estados de pantalla (UX States) [OBL]

> **Activación:** Siempre obligatorio. Referencia a TEMPLATE_BASE_Spec_UXStates si existe estándar global.

### 11.1 Loading [OBL]

| Elemento | Tipo de loading | Duración mín | UI bloqueada |
|----------|-----------------|--------------|--------------|
| Pantalla completa | {{TIPO}} | {{DURACION}} | Sí/No |
| {{COMPONENTE}} | {{TIPO}} | {{DURACION}} | Sí/No |

### 11.2 Empty State [OBL]

| Contexto | Mensaje | CTA | Ilustración |
|----------|---------|-----|-------------|
| Sin datos inicial | {{MENSAJE}} | {{CTA}} | {{ILUSTRACION}} |
| Sin resultados búsqueda | {{MENSAJE}} | {{CTA}} | {{ILUSTRACION}} |
| Filtros sin match | {{MENSAJE}} | {{CTA}} | {{ILUSTRACION}} |

### 11.3 Error States [OBL]

| Tipo de error | Mensaje | CTA | Comportamiento |
|---------------|---------|-----|----------------|
| Error de red | {{MENSAJE}} | {{CTA}} | {{COMPORTAMIENTO}} |
| Error servidor (5xx) | {{MENSAJE}} | {{CTA}} | {{COMPORTAMIENTO}} |
| Error permisos (403) | {{MENSAJE}} | {{CTA}} | {{COMPORTAMIENTO}} |
| Timeout | {{MENSAJE}} | {{CTA}} | {{COMPORTAMIENTO}} |

### 11.4 Success / Feedback [OPC]

| Acción | Tipo feedback | Mensaje | Duración |
|--------|---------------|---------|----------|
| {{ACCION}} | [Toast/Banner/Inline/Modal] | {{MENSAJE}} | {{DURACION}} |

---

## 12) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Estándar aplicable [OBL]

- **Nivel objetivo:** WCAG 2.1 AA
- **Contraste mínimo:** 4.5:1 (texto normal), 3:1 (texto grande)
- **Focus visible:** Sí, obligatorio

### 12.2 Navegación por teclado [OBL]

| Elemento | Tecla | Acción |
|----------|-------|--------|
| Navegación general | Tab | Mover foco adelante |
| Navegación general | Shift+Tab | Mover foco atrás |
| Botones/Links | Enter/Space | Activar |
| Modales | Escape | Cerrar |
| {{ELEMENTO}} | {{TECLA}} | {{ACCION}} |

### 12.3 Screen readers [OBL]

| Elemento | Texto anunciado | Notas |
|----------|-----------------|-------|
| {{ELEMENTO}} | {{TEXTO}} | {{NOTAS}} |

### 12.4 Touch targets (mobile) [OBL]

- **Tamaño mínimo:** 44x44px
- **Espaciado mínimo entre targets:** 8px

---

## 13) Responsive [OBL]

> **Activación:** Siempre obligatorio para productos multi-dispositivo.

### 13.1 Breakpoints del proyecto [OBL]

| Nombre | Rango | Tipo |
|--------|-------|------|
| Mobile | 320–767px | Primario |
| Tablet | 768–1023px | Secundario |
| Desktop | 1024–1439px | Primario |
| Large Desktop | 1440px+ | Secundario |

### 13.2 Cambios por breakpoint [OBL]

| Elemento | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| Grid principal | {{CONFIG}} | {{CONFIG}} | {{CONFIG}} |
| Sidebar | {{CONFIG}} | {{CONFIG}} | {{CONFIG}} |
| Navegación | {{CONFIG}} | {{CONFIG}} | {{CONFIG}} |
| Cards/Items | {{CONFIG}} | {{CONFIG}} | {{CONFIG}} |
| CTAs | {{CONFIG}} | {{CONFIG}} | {{CONFIG}} |

### 13.3 Comportamientos especiales [OPC]

| Comportamiento | Breakpoints | Descripción |
|----------------|-------------|-------------|
| {{COMPORTAMIENTO}} | {{BREAKPOINTS}} | {{DESCRIPCION}} |

---

## 14) Design System / Tokens [OPC]

> **Activación:** Incluir si el proyecto tiene design system definido. Si no, omitir y usar specs inline en componentes.

### 14.1 Tokens de color aplicables [OPC]

| Uso | Token | Valor |
|-----|-------|-------|
| Primary | `--color-primary` | {{VALOR}} |
| Background | `--color-bg` | {{VALOR}} |
| Text | `--color-text` | {{VALOR}} |
| Error | `--color-error` | {{VALOR}} |

### 14.2 Tokens de tipografía [OPC]

| Uso | Token | Valor |
|-----|-------|-------|
| Heading 1 | `--font-h1` | {{VALOR}} |
| Body | `--font-body` | {{VALOR}} |

### 14.3 Tokens de espaciado [OPC]

| Uso | Token | Valor |
|-----|-------|-------|
| Spacing base | `--space-base` | {{VALOR}} |

---

## 15) Copy UX / Contenido [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Tono y estilo [OBL]

- **Tono general:** [Elegir: Profesional / Cercano / Experto / Enterprise / Playful]
- **Voz:** [Elegir: Primera persona / Segunda persona / Impersonal]

### 15.2 Textos clave [OBL]

| Elemento | Copy | Variante A/B (si aplica) | Notas |
|----------|------|--------------------------|-------|
| Título pantalla | {{COPY}} | {{VARIANTE}} | {{NOTAS}} |
| CTA principal | {{COPY}} | {{VARIANTE}} | {{NOTAS}} |
| Empty state | {{COPY}} | {{VARIANTE}} | {{NOTAS}} |
| Error genérico | {{COPY}} | {{VARIANTE}} | {{NOTAS}} |

### 15.3 Reglas de microcopy [OBL]

- Usar verbos de acción en CTAs
- Mensajes de error accionables (qué hacer, no solo qué pasó)
- Consistencia terminológica con el resto del producto
- Evitar jerga técnica para usuarios finales

---

## 16) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio para producto.

### 16.1 Eventos de pantalla [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `screen_view` | Pantalla visible | `screen_id, user_id, timestamp, entry_point` |
| `screen_loaded` | Contenido cargado | `screen_id, load_time_ms` |
| `screen_error` | Error mostrado | `screen_id, error_type, error_code` |

### 16.2 Eventos de interacción [OBL]

| Evento | Trigger | Payload mínimo |
|--------|---------|----------------|
| {{EVENTO}} | {{TRIGGER}} | {{PAYLOAD}} |

### 16.3 Métricas derivadas [OPC]

| Métrica | Cálculo | Dashboard |
|---------|---------|-----------|
| {{METRICA}} | {{CALCULO}} | {{DASHBOARD}} |

---

## 17) Performance [OPC]

> **Activación:** Incluir para pantallas críticas o con requisitos de performance específicos.

### 17.1 Objetivos [OPC]

| Métrica | Objetivo | Crítico si excede |
|---------|----------|-------------------|
| Tiempo de carga inicial | {{VALOR}} | {{VALOR}} |
| LCP (web) | {{VALOR}} | {{VALOR}} |
| TTI / INP (web) | {{VALOR}} | {{VALOR}} |
| FPS (animaciones) | {{VALOR}} | {{VALOR}} |
| Peso máximo assets | {{VALOR}} | {{VALOR}} |

### 17.2 Estrategias [OPC]

| Estrategia | Aplica a | Implementación |
|------------|----------|----------------|
| Lazy loading | {{ELEMENTOS}} | {{IMPLEMENTACION}} |
| Code splitting | {{MODULOS}} | {{IMPLEMENTACION}} |
| Image optimization | {{IMAGENES}} | {{IMPLEMENTACION}} |

### 17.3 Riesgos técnicos [OPC]

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| {{RIESGO}} | {{IMPACTO}} | {{MITIGACION}} |

---

## 18) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 18.1 Casos funcionales [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TC-01 | {{CASO}} | {{RESULTADO}} | {{PRIORIDAD}} |
| TC-02 | {{CASO}} | {{RESULTADO}} | {{PRIORIDAD}} |

### 18.2 Casos visuales [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TV-01 | Alignment correcto en {{BREAKPOINT}} | {{RESULTADO}} |
| TV-02 | Truncado de texto largo | {{RESULTADO}} |
| TV-03 | Estados hover/focus visibles | {{RESULTADO}} |

### 18.3 Casos de error [OBL]

| ID | Escenario | Resultado esperado |
|----|-----------|-------------------|
| TE-01 | Sin conexión a red | {{RESULTADO}} |
| TE-02 | API retorna 500 | {{RESULTADO}} |
| TE-03 | Timeout | {{RESULTADO}} |
| TE-04 | Permisos insuficientes | {{RESULTADO}} |

### 18.4 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Navegación completa con teclado | {{RESULTADO}} |
| TA-02 | Focus visible en todos los elementos interactivos | {{RESULTADO}} |
| TA-03 | Screen reader anuncia correctamente | {{RESULTADO}} |
| TA-04 | Contraste cumple WCAG AA | {{RESULTADO}} |

---

## 19) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 19.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Owner |
|----|--------|--------------|---------|------------|-------|
| R-01 | {{RIESGO}} | [Alta/Media/Baja] | [Alto/Medio/Bajo] | {{MITIGACION}} | {{OWNER}} |

### 19.2 Supuestos [OBL]

| ID | Supuesto | Validado | Fecha validación |
|----|----------|----------|------------------|
| S-01 | {{SUPUESTO}} | Sí/No | {{FECHA}} |

### 19.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión pendiente | Responsable | Fecha límite |
|----|------|-------------------|-------------|--------------|
| D-01 | {{TEMA}} | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |

---

## 20) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio. Última sección antes de cerrar spec.

### 20.1 Producto / UX [OBL]

- [ ] Objetivo de pantalla documentado
- [ ] Flujos (happy path + alternos) documentados
- [ ] Inventario de componentes completo
- [ ] Copy base definido
- [ ] Estados (loading/empty/error) definidos

### 20.2 Técnica [OBL]

- [ ] APIs mapeadas con owners
- [ ] Contratos de datos definidos
- [ ] Reglas de negocio confirmadas
- [ ] Dependencias identificadas

### 20.3 Calidad [OBL]

- [ ] Responsive definido por breakpoint
- [ ] Accesibilidad mínima definida
- [ ] Analytics instrumentado
- [ ] Casos de prueba definidos

### 20.4 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 21) Particularidades del proyecto [OPC]

> **Activación:** Usar esta sección para documentar excepciones o customizaciones específicas de este proyecto que no encajan en las secciones estándar.

### 21.1 Excepciones al estándar

| Sección afectada | Excepción | Justificación | Aprobado por |
|------------------|-----------|---------------|--------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} | {{APROBADOR}} |

### 21.2 Customizaciones específicas

{{DESCRIPCION_CUSTOMIZACIONES}}

### 21.3 Notas para el equipo

{{NOTAS_ADICIONALES}}

---

## 📋 ANEXOS REQUERIDOS

> Marcar los anexos que aplican a esta pantalla:

- [ ] **Anexo Form** → Si hay formularios complejos (usar TEMPLATE_BASE_Spec_Form)
- [ ] **Anexo DataGrid** → Si hay tablas enterprise (usar TEMPLATE_BASE_Spec_DataGrid)
- [ ] **Anexo ModalOverlay** → Si hay modales/drawers críticos (usar TEMPLATE_BASE_Spec_ModalOverlay)
- [ ] **Anexo UXStates** → Referencia a estándar global (usar TEMPLATE_BASE_Spec_UXStates)

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template completo
2. **Reemplazar** todos los `{{PLACEHOLDER}}` con valores específicos
3. **Seleccionar** opciones en `[Elegir: ...]`
4. **Omitir** secciones marcadas `[OPC]` o `[COND]` si no aplican
5. **Repetir** sección 6 por cada componente crítico
6. **Validar** con checklist (sección 20) antes de entregar

### Secciones núcleo (mínimo viable):

Si hay restricción de tiempo, completar al menos:
- §0 Metadatos
- §1 Propósito
- §2 Scope
- §4 Flujo
- §5 Inventario de componentes
- §6 Specs de componentes críticos
- §9 APIs/Datos
- §10 Reglas de negocio
- §11 Estados
- §16 Analytics
- §20 Checklist

### Validación cruzada:

- Cada componente en §5 debe tener spec en §6 (si es crítico)
- Cada endpoint en §9 debe mapear a un componente
- Cada regla en §10 debe indicar componentes afectados
- Cada evento en §16 debe corresponder a una interacción documentada

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
