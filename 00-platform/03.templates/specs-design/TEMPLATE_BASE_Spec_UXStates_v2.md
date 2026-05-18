# 🧩 TEMPLATE BASE — SPEC UX STATES PACK (Empty/Error/Loading/Feedback)

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P1 — Core (Transversal)  
> **Última actualización:** {{FECHA_ACTUALIZACION}}

---

## 🔖 GUÍA DE USO DEL TEMPLATE

### Marcadores de obligatoriedad

| Marcador | Significado | Regla |
|----------|-------------|-------|
| `[OBL]` | **Obligatorio** | Siempre debe completarse |
| `[OPC]` | **Opcional** | Completar si aplica al proyecto |
| `[COND]` | **Condicional** | Completar solo si se cumple la condición indicada |

### Naturaleza especial de este template

Este template es **diferente** a los demás:
- Es un **estándar transversal** que se referencia desde otros templates
- Se completa **una vez por producto** (no por pantalla)
- Define reglas globales que todos los módulos deben seguir
- Otros templates (AppScreen, Form, Wizard, etc.) **referencian** este documento en lugar de redefinir estados

### Cuándo usar este template

- ✅ **Siempre** — Todo producto necesita definir sus UX states
- ✅ Al inicio del proyecto como estándar global
- ✅ Al agregar nuevos tipos de estados
- ✅ Al estandarizar mensajes de error/empty/feedback

---

# UX STATES PACK — ESTÁNDAR TRANSVERSAL

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | UXStates_Pack_{{NOMBRE_PROYECTO}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Alcance** | [Elegir: Global (todo el producto) / Módulo específico] |
| **ID técnico** | `uxstates-{{NUM}}-{{SLUG}}` (ej: `uxstates-01-global`) |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito del pack [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este documento define el **estándar único** para todos los estados de UX del producto:

| Categoría | Estados incluidos |
|-----------|-------------------|
| **Loading** | Skeleton, spinner, refresh, infinite scroll |
| **Empty** | Sin datos, primera vez, sin resultados, filtros vacíos |
| **Error** | Red, servidor, permisos, validación, timeout |
| **Offline** | Sin conexión, cache, cola de acciones |
| **Feedback** | Toast, banner, confirmaciones, warnings |

### 1.2 Objetivos [OBL]

- **Consistencia:** Mismos patrones en todo el producto
- **Claridad:** Mensajes accionables (qué pasó + qué hacer)
- **Recuperabilidad:** Retry claro y funcional
- **Reducir frustración:** No culpar al usuario
- **Facilitar QA:** Estados predecibles y testeables
- **Analytics:** Trackear frecuencia de estados problemáticos

---

## 2) Taxonomía oficial de estados [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio. Esta es la sección más importante del template.

### 2.1 Estados de carga (Loading) [OBL]

| State ID | Nombre | Descripción | UI recomendada |
|----------|--------|-------------|----------------|
| `loading_initial` | Carga inicial | Primera carga de pantalla | Skeleton full |
| `loading_partial` | Carga parcial | Un componente cargando | Skeleton del componente |
| `loading_refresh` | Refresh | Pull-to-refresh o botón | Indicador + mantener contenido |
| `loading_infinite` | Infinite scroll | Paginación al scroll | Spinner al final |
| `loading_action` | Acción en progreso | Submit, save, delete | Spinner en botón |
| `loading_background` | Background sync | Actualización silenciosa | Indicador sutil (opcional) |

### 2.2 Estados vacíos (Empty) [OBL]

| State ID | Nombre | Descripción | Causa típica |
|----------|--------|-------------|--------------|
| `empty_first_time` | Primera vez | Usuario nuevo, sin datos | Onboarding incompleto |
| `empty_no_results` | Sin resultados | Búsqueda sin matches | Query sin coincidencias |
| `empty_no_content` | Sin contenido | Feed/lista vacía | Datos eliminados o no creados |
| `empty_filtered_out` | Filtros vacíos | Filtros excluyen todo | Filtros muy restrictivos |
| `empty_permission` | Sin permisos | No visible por rol | RBAC restrictivo |

### 2.3 Estados de error (Error) [OBL]

| State ID | Nombre | HTTP | Descripción | Retry permitido |
|----------|--------|------|-------------|-----------------|
| `error_network` | Sin conexión | — | No hay red/DNS | Sí (inmediato) |
| `error_timeout` | Timeout | — | Respuesta muy lenta | Sí (inmediato) |
| `error_server_5xx` | Error servidor | 500-599 | Problema backend | Sí (con backoff) |
| `error_not_found` | No encontrado | 404 | Recurso no existe | No |
| `error_bad_request` | Request inválido | 400 | Datos malformados | No (fix datos) |
| `error_unauthorized` | No autenticado | 401 | Sesión expirada | No (re-login) |
| `error_forbidden` | Sin permisos | 403 | Acceso denegado | No (solicitar) |
| `error_validation` | Validación | 422 | Campos inválidos | No (fix campos) |
| `error_rate_limit` | Rate limit | 429 | Demasiadas requests | Sí (con delay) |
| `error_dependency` | Servicio externo | — | API tercero falló | Sí (con backoff) |
| `error_unknown` | Error desconocido | — | Causa no identificada | Sí |

### 2.4 Estados offline [COND]

> **Activación:** Incluir si el producto soporta modo offline.

| State ID | Nombre | Descripción |
|----------|--------|-------------|
| `offline_detected` | Sin conexión | Red no disponible |
| `offline_cached` | Vista en cache | Mostrando datos guardados |
| `offline_queued` | Acciones en cola | Cambios pendientes de sync |
| `offline_syncing` | Sincronizando | Reconectando y enviando cola |

### 2.5 Estados de feedback [OBL]

| State ID | Nombre | Duración | Placement |
|----------|--------|----------|-----------|
| `success_toast` | Toast éxito | {{DURACION}}s | Bottom/Top |
| `success_inline` | Inline éxito | Persistente | En componente |
| `success_banner` | Banner éxito | Persistente/Dismissable | Top de página |
| `info_toast` | Toast info | {{DURACION}}s | Bottom/Top |
| `warning_toast` | Toast warning | {{DURACION}}s | Bottom/Top |
| `warning_banner` | Banner warning | Persistente | Top de página |

---

## 3) Reglas globales de diseño [OBL]

> **Activación:** Siempre obligatorio.

### 3.1 Principios de UX [OBL]

| Principio | Descripción | Ejemplo |
|-----------|-------------|---------|
| **No bloquear** | Degradar gracefully si es posible | Mostrar cache en lugar de error |
| **Mensajes accionables** | Decir qué pasó + qué hacer | "Sin conexión. Reintentar" |
| **Retry visible** | Botón claro para reintentar | CTA primario en errores |
| **No culpar** | Evitar lenguaje acusatorio | "Algo salió mal" vs "Hiciste algo mal" |
| **Consistencia** | Mismos patrones en todo el producto | Un solo estilo de empty state |

### 3.2 Estructura de mensajes [OBL]

```
┌─────────────────────────────────────┐
│ [Ícono/Ilustración]                 │
│                                     │
│ TÍTULO (qué pasó)                   │  ← 1 línea, claro
│ Descripción breve                   │  ← 1-2 líneas
│                                     │
│ [CTA Primario]  [CTA Secundario]    │  ← Acciones
│                                     │
│ Código: ERR_XXX (opcional)          │  ← Solo enterprise
└─────────────────────────────────────┘
```

### 3.3 Placement por tipo [OBL]

| Tipo de estado | Placement | Comportamiento |
|----------------|-----------|----------------|
| Error de pantalla | Full-screen | Bloquea contenido |
| Error de sección | Inline section | Reemplaza sección |
| Error de componente | Inline component | Dentro del componente |
| Error de acción | Toast/Modal | Temporal |
| Empty state | Inline section | Reemplaza lista/contenido |
| Loading | Inline (skeleton) | Placeholder del contenido |
| Success | Toast | Auto-dismiss |
| Warning | Banner | Dismissable |

---

## 4) Loading States — Especificación [OBL]

> **Activación:** Siempre obligatorio.

### 4.1 Skeleton vs Spinner [OBL]

| Usar Skeleton cuando... | Usar Spinner cuando... |
|-------------------------|------------------------|
| Layout es conocido y predecible | No hay layout definido |
| Carga de listas/cards/tablas | Acciones rápidas (submit) |
| Carga inicial de página | Operaciones puntuales |
| Se quiere reducir percepción de espera | Carga de modal/overlay |

### 4.2 Configuración de timeouts [OBL]

| Evento | Tiempo | Acción |
|--------|--------|--------|
| Loading normal | 0 - {{TIEMPO_NORMAL}}s | Mostrar skeleton/spinner |
| Loading prolongado | {{TIEMPO_NORMAL}} - {{TIEMPO_WARNING}}s | Agregar mensaje "Sigue cargando..." |
| Timeout | > {{TIEMPO_TIMEOUT}}s | Mostrar `error_timeout` |

**Valores recomendados:**
- `TIEMPO_NORMAL`: 3 segundos
- `TIEMPO_WARNING`: 8 segundos
- `TIEMPO_TIMEOUT`: 15-30 segundos

### 4.3 Componentes de loading [OPC]

| Componente | Uso | Specs |
|------------|-----|-------|
| Skeleton rect | Texto, imágenes | Border-radius: {{VALOR}}, Color: {{TOKEN}} |
| Skeleton circle | Avatares | Tamaños: S/M/L |
| Spinner | Acciones | Tamaños: S/M/L, Color: {{TOKEN}} |
| Progress bar | Uploads, procesos largos | Determinado/Indeterminado |
| Shimmer animation | Opcional en skeletons | {{DURACION}}ms |

### 4.4 Accesibilidad de loading [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Anuncio de carga | `aria-busy="true"` en contenedor |
| Texto para screen reader | `aria-label="Cargando contenido"` |
| Reducir motion | Respetar `prefers-reduced-motion` |

---

## 5) Empty States — Especificación [OBL]

> **Activación:** Siempre obligatorio.

### 5.1 Estructura de empty state [OBL]

| Elemento | Requerido | Notas |
|----------|-----------|-------|
| Ilustración/Ícono | Recomendado | Humaniza el mensaje |
| Título | Sí | Qué está vacío |
| Descripción | Sí | Por qué y qué hacer |
| CTA primario | Sí | Acción principal |
| CTA secundario | Opcional | Alternativa |

### 5.2 Catálogo de empty states [OBL]

#### `empty_first_time` — Primera vez

| Campo | Copy default | Personalizable |
|-------|--------------|----------------|
| **Título** | "{{ENTIDAD}} vacío" | Sí |
| **Descripción** | "Comienza agregando tu primer {{ITEM}}." | Sí |
| **CTA primario** | "Crear {{ITEM}}" | Sí |
| **CTA secundario** | "Ver ejemplos" / "Explorar" | Opcional |
| **Ilustración** | {{ILUSTRACION}} | Opcional |

#### `empty_no_results` — Sin resultados de búsqueda

| Campo | Copy default | Personalizable |
|-------|--------------|----------------|
| **Título** | "No encontramos resultados" | Sí |
| **Descripción** | "Prueba con otros términos o ajusta los filtros." | Sí |
| **CTA primario** | "Limpiar búsqueda" | Sí |
| **CTA secundario** | "Ver todo" / "Sugerencias" | Opcional |

#### `empty_filtered_out` — Filtros vacíos

| Campo | Copy default | Personalizable |
|-------|--------------|----------------|
| **Título** | "Nada coincide con tus filtros" | Sí |
| **Descripción** | "Reduce los filtros para ver más opciones." | Sí |
| **CTA primario** | "Ajustar filtros" | Sí |
| **CTA secundario** | "Restablecer todo" | Opcional |

#### `empty_no_content` — Sin contenido

| Campo | Copy default | Personalizable |
|-------|--------------|----------------|
| **Título** | "Aún no hay {{CONTENIDO}}" | Sí |
| **Descripción** | "Cuando haya {{CONTENIDO}}, aparecerá aquí." | Sí |
| **CTA primario** | "Crear {{CONTENIDO}}" / "Explorar" | Sí |

#### `empty_permission` — Sin permisos

| Campo | Copy default | Personalizable |
|-------|--------------|----------------|
| **Título** | "Sin acceso a este contenido" | Sí |
| **Descripción** | "Contacta a un administrador si necesitas permisos." | Sí |
| **CTA primario** | "Solicitar acceso" | Sí |
| **CTA secundario** | "Volver" | Opcional |

### 5.3 Accesibilidad de empty states [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Semántica | Título como H2/H3 |
| CTA claro | Texto descriptivo en botón |
| Ilustración | `aria-hidden="true"` o alt descriptivo |

---

## 6) Error States — Especificación [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Estructura de error state [OBL]

| Elemento | Requerido | Notas |
|----------|-----------|-------|
| Ícono de error | Recomendado | Indica severidad |
| Título | Sí | Qué pasó (sin culpar) |
| Descripción | Sí | Breve + qué hacer |
| CTA primario | Sí | Retry / Resolver |
| CTA secundario | Opcional | Soporte / Volver |
| Código de error | Opcional | Solo para enterprise/soporte |

### 6.2 Catálogo de errores [OBL]

#### `error_network` — Sin conexión

| Campo | Copy default |
|-------|--------------|
| **Título** | "Sin conexión" |
| **Descripción** | "Revisa tu conexión a internet e inténtalo de nuevo." |
| **CTA primario** | "Reintentar" |
| **CTA secundario** | "Ver contenido guardado" (si hay cache) |

#### `error_timeout` — Timeout

| Campo | Copy default |
|-------|--------------|
| **Título** | "Tardó demasiado" |
| **Descripción** | "El servidor no respondió a tiempo. Intenta de nuevo." |
| **CTA primario** | "Reintentar" |
| **CTA secundario** | "Contactar soporte" |

#### `error_server_5xx` — Error de servidor

| Campo | Copy default |
|-------|--------------|
| **Título** | "Algo salió mal" |
| **Descripción** | "Estamos teniendo problemas. Intenta en unos minutos." |
| **CTA primario** | "Reintentar" |
| **CTA secundario** | "Reportar problema" |
| **Código** | `ERR_SERVER_{{CODE}}` |

#### `error_not_found` — 404

| Campo | Copy default |
|-------|--------------|
| **Título** | "Página no encontrada" |
| **Descripción** | "El contenido que buscas no existe o fue eliminado." |
| **CTA primario** | "Ir al inicio" |
| **CTA secundario** | "Buscar" |

#### `error_unauthorized` — 401 Sesión expirada

| Campo | Copy default |
|-------|--------------|
| **Título** | "Sesión expirada" |
| **Descripción** | "Inicia sesión nuevamente para continuar." |
| **CTA primario** | "Iniciar sesión" |
| **CTA secundario** | — |

#### `error_forbidden` — 403 Sin permisos

| Campo | Copy default |
|-------|--------------|
| **Título** | "Acceso restringido" |
| **Descripción** | "No tienes permisos para ver este contenido." |
| **CTA primario** | "Solicitar acceso" |
| **CTA secundario** | "Volver" |

#### `error_validation` — Validación de formulario

| Campo | Copy default |
|-------|--------------|
| **Título** | "Revisa los campos" |
| **Descripción** | "Corrige los errores marcados para continuar." |
| **CTA primario** | "Ir al primer error" |
| **CTA secundario** | "Cancelar" |

#### `error_rate_limit` — 429 Too many requests

| Campo | Copy default |
|-------|--------------|
| **Título** | "Demasiadas solicitudes" |
| **Descripción** | "Espera un momento antes de intentar de nuevo." |
| **CTA primario** | "Reintentar en {{TIEMPO}}" |

#### `error_unknown` — Error desconocido

| Campo | Copy default |
|-------|--------------|
| **Título** | "Ocurrió un error inesperado" |
| **Descripción** | "Algo no funcionó correctamente. Inténtalo de nuevo." |
| **CTA primario** | "Reintentar" |
| **CTA secundario** | "Contactar soporte" |
| **Código** | `ERR_UNKNOWN_{{ID}}` |

### 6.3 Reglas de retry [OBL]

| Tipo de error | Retry automático | Retry manual | Backoff |
|---------------|------------------|--------------|---------|
| `error_network` | No | Sí (inmediato) | No |
| `error_timeout` | Opcional (1x) | Sí | No |
| `error_server_5xx` | Opcional (2x) | Sí | Sí (exponencial) |
| `error_rate_limit` | Sí (después de delay) | Sí | Sí (por header) |
| `error_unauthorized` | No | No (re-login) | — |
| `error_forbidden` | No | No | — |
| `error_validation` | No | No (fix datos) | — |

### 6.4 Códigos de error [COND]

> **Activación:** Incluir para productos enterprise con soporte técnico.

| Formato | Ejemplo | Cuándo mostrar |
|---------|---------|----------------|
| `ERR_{{CATEGORIA}}_{{CODIGO}}` | `ERR_AUTH_401` | Siempre visible para 5xx |
| Botón "Copiar código" | — | Cuando hay código |
| Incluir en reporte | — | Al contactar soporte |

---

## 7) Offline States — Especificación [COND]

> **Activación:** Incluir si el producto soporta modo offline o PWA.

### 7.1 Detección de offline [COND]

| Trigger | Comportamiento |
|---------|----------------|
| `navigator.onLine = false` | Mostrar banner offline |
| Request falla por red | Mostrar error + banner |
| Reconexión detectada | Iniciar sync, ocultar banner |

### 7.2 UI de offline [COND]

| Elemento | Implementación |
|----------|----------------|
| Banner persistente | "Estás sin conexión" — top de página |
| Indicador de cache | "Mostrando datos guardados" |
| Cola de acciones | Badge con número de pendientes |
| Sync en progreso | Spinner + "Sincronizando..." |

### 7.3 Comportamiento de acciones [COND]

| Acción | Comportamiento offline |
|--------|------------------------|
| Lectura | Mostrar cache si existe |
| Escritura | Encolar + confirmar encolado |
| Envío crítico | Bloquear + mostrar error |

---

## 8) Success/Feedback States — Especificación [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Tipos de feedback [OBL]

| Tipo | Duración | Dismissable | Cuándo usar |
|------|----------|-------------|-------------|
| **Toast success** | {{DURACION}}s | Auto | Confirmación rápida |
| **Toast info** | {{DURACION}}s | Auto | Información contextual |
| **Toast warning** | {{DURACION}}s | Manual | Advertencia importante |
| **Banner success** | Persistente | Manual | Confirmación con undo |
| **Banner warning** | Persistente | Manual | Advertencia crítica |
| **Inline success** | Persistente | — | Dentro de componente |

**Duración recomendada:** 3-5 segundos

### 8.2 Catálogo de feedback [OBL]

| State ID | Copy default | Icono |
|----------|--------------|-------|
| `success_save` | "Cambios guardados" | ✓ |
| `success_create` | "{{ITEM}} creado correctamente" | ✓ |
| `success_delete` | "{{ITEM}} eliminado" | ✓ |
| `success_send` | "Enviado correctamente" | ✓ |
| `success_copy` | "Copiado al portapapeles" | ✓ |
| `info_update` | "Actualizando datos..." | ℹ |
| `info_sync` | "Sincronizando..." | ↻ |
| `warning_unsaved` | "Tienes cambios sin guardar" | ⚠ |
| `warning_expiring` | "Tu sesión expirará pronto" | ⚠ |

### 8.3 Placement de toasts [OBL]

| Posición | Cuándo usar |
|----------|-------------|
| Top-right | Default para desktop |
| Top-center | Mensajes críticos |
| Bottom-center | Mobile default |
| Bottom-right | Alternativa desktop |

### 8.4 Stacking de toasts [OPC]

| Regla | Valor |
|-------|-------|
| Máximo visible | {{NUM}} toasts |
| Comportamiento al exceder | Queue / Dismiss oldest |
| Spacing entre toasts | {{VALOR}}px |

---

## 9) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 ARIA live regions [OBL]

| Tipo de estado | `aria-live` | Prioridad |
|----------------|-------------|-----------|
| Error crítico | `assertive` | Interrumpe |
| Error normal | `polite` | Espera pausa |
| Loading | `polite` | Espera pausa |
| Success | `polite` | Espera pausa |
| Warning | `polite` / `assertive` | Según severidad |

### 9.2 Focus management [OBL]

| Evento | Comportamiento |
|--------|----------------|
| Error en form | Focus al primer campo con error |
| Error de página | Focus al título del error |
| Modal de error | Focus trap dentro del modal |
| Toast | No robar focus |

### 9.3 Contraste y legibilidad [OBL]

| Elemento | Requisito |
|----------|-----------|
| Texto de error | Contraste WCAG AA (4.5:1) |
| Iconos | Contraste WCAG AA (3:1) |
| Botones | Contraste WCAG AA |
| No depender solo de color | Usar iconos + texto |

---

## 10) Componentes del Design System [OPC]

> **Activación:** Incluir si hay Design System definido.

### 10.1 Mapping de componentes [OPC]

| Estado | Componente DS | Variantes |
|--------|---------------|-----------|
| Loading | `Skeleton`, `Spinner` | S/M/L |
| Empty | `EmptyState` | Con/sin ilustración |
| Error | `ErrorState`, `ErrorBanner` | Inline, Full-page |
| Toast | `Toast` | Success, Info, Warning, Error |
| Banner | `Banner` | Info, Warning, Error |

### 10.2 Tokens de color [OPC]

| Estado | Background | Text | Border |
|--------|------------|------|--------|
| Success | `--color-success-bg` | `--color-success-text` | `--color-success-border` |
| Error | `--color-error-bg` | `--color-error-text` | `--color-error-border` |
| Warning | `--color-warning-bg` | `--color-warning-text` | `--color-warning-border` |
| Info | `--color-info-bg` | `--color-info-text` | `--color-info-border` |

---

## 11) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Eventos de estados [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `state_loading_shown` | Loading visible | `screen_id, component_id, loading_type` |
| `state_empty_shown` | Empty state visible | `screen_id, empty_type` |
| `state_error_shown` | Error visible | `screen_id, error_type, error_code` |
| `state_offline_shown` | Offline detectado | `screen_id, has_cache` |
| `state_success_shown` | Success feedback | `screen_id, action_type` |
| `state_retry_clicked` | Click en retry | `screen_id, error_type, retry_count` |

### 11.2 Métricas derivadas [OBL]

| Métrica | Cálculo | Umbral de alerta |
|---------|---------|------------------|
| Error rate por pantalla | `error_shown / screen_view` | > {{UMBRAL}}% |
| Retry success rate | `success después de retry / retry_clicked` | < {{UMBRAL}}% |
| Timeout rate | `error_timeout / loading_shown` | > {{UMBRAL}}% |
| Empty state frequency | `empty_shown / screen_view` | Depende del contexto |

---

## 12) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Casos de Loading [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TL-01 | Carga inicial de pantalla | Skeleton visible → contenido |
| TL-02 | Carga > timeout | Mostrar `error_timeout` |
| TL-03 | Loading prolongado (>8s) | Mostrar mensaje "Sigue cargando" |

### 12.2 Casos de Empty [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TE-01 | Usuario nuevo sin datos | `empty_first_time` con CTA crear |
| TE-02 | Búsqueda sin resultados | `empty_no_results` con limpiar |
| TE-03 | Filtros excluyentes | `empty_filtered_out` con ajustar |

### 12.3 Casos de Error [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TR-01 | Sin conexión | `error_network` con retry |
| TR-02 | API 500 | `error_server_5xx` con retry |
| TR-03 | API 401 | `error_unauthorized` → login |
| TR-04 | API 403 | `error_forbidden` con solicitar |
| TR-05 | Retry exitoso | Contenido cargado |

### 12.4 Casos de Offline [COND]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TO-01 | Pérdida de conexión | Banner offline visible |
| TO-02 | Vista con cache | Contenido de cache + indicador |
| TO-03 | Acción offline | Encolada + confirmación |
| TO-04 | Reconexión | Sync automático |

### 12.5 Casos de Accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Error anunciado | Screen reader lee el error |
| TA-02 | Focus en error | Focus al título o primer campo |
| TA-03 | Contraste de mensajes | WCAG AA cumplido |

---

## 13) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Definición [OBL]

- [ ] Taxonomía de estados completa
- [ ] Catálogo de copy para cada estado
- [ ] Placement definido por tipo
- [ ] Reglas de retry documentadas

### 13.2 UX [OBL]

- [ ] Mensajes accionables (qué pasó + qué hacer)
- [ ] Consistencia visual
- [ ] Ilustraciones/iconos definidos

### 13.3 Técnica [OBL]

- [ ] Timeouts configurados
- [ ] Retry con backoff (si aplica)
- [ ] Códigos de error mapeados

### 13.4 Accesibilidad [OBL]

- [ ] `aria-live` implementado
- [ ] Focus management definido
- [ ] Contraste validado

### 13.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 14) Particularidades del proyecto [OPC]

> **Activación:** Usar para estados custom o excepciones.

### 14.1 Estados custom del proyecto

| State ID | Nombre | Descripción | Copy |
|----------|--------|-------------|------|
| `{{STATE_ID}}` | {{NOMBRE}} | {{DESCRIPCION}} | {{COPY}} |

### 14.2 Excepciones al estándar

| Estado | Excepción | Justificación |
|--------|-----------|---------------|
| {{ESTADO}} | {{EXCEPCION}} | {{JUSTIFICACION}} |

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Completar una vez** al inicio del proyecto
2. **Referenciar desde otros templates** (AppScreen, Form, Wizard, etc.)
3. **Usar el catálogo de copy** como fuente de verdad
4. **Agregar estados custom** en §14 si es necesario

### Cómo referenciar desde otros templates:

En lugar de redefinir estados en cada spec, escribir:

```
### 11) Estados de pantalla
Ver estándar global: `UXStates_Pack_{{PROYECTO}}_v{{VERSION}}`

Estados específicos de esta pantalla:
- Loading: `loading_initial` (skeleton de cards)
- Empty: `empty_no_results` (búsqueda vacía)
- Error: `error_network`, `error_server_5xx`
```

### Secciones núcleo (mínimo viable):

- §2 **Taxonomía de estados** ← CRÍTICO
- §4 Loading states
- §5 Empty states + catálogo
- §6 Error states + catálogo
- §8 Feedback states
- §9 Accesibilidad
- §11 Analytics
- §13 Checklist

### Validación cruzada:

- Cada estado en §2 debe tener copy en §4-§8
- Cada error debe tener regla de retry en §6.3
- Cada estado debe tener evento en §11
- Cada estado debe tener caso QA en §12

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
