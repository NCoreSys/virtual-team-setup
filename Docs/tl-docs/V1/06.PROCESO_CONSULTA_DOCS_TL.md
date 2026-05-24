# Proceso de Consulta de Documentación — Tech Lead (VTT)

**Versión:** 1.0
**Fecha:** 2026-03-19
**Propósito:** Establecer qué documentos consultar, en qué orden y para qué, antes de escribir un brief o assignment. Complementa `PROCESO_ASIGNACION_TAREAS.md` v1.4.

---

## Por Qué Existe Este Documento

VTT tiene documentos de diseño originales en `_project-management/planV2/` y código implementado en `backend/` y `frontend/`. Sin un procedimiento formal que los enlace, el TL escribe assignments desde la memoria del handoff — lo que genera errores de contrato (rutas incorrectas, campos inexistentes, componentes ya creados que se inventan de cero).

Este documento cierra esa brecha.

---

## Mapa de Fuentes de Verdad por Capa

| Capa | Fuente Primaria (verdad real) | Fuente Secundaria (diseño original) |
|------|-------------------------------|-------------------------------------|
| **API Contract** | `backend/src/routes/[modulo].ts` o `[modulo].routes.ts` | `_project-management/planV2/DOC-003_ARQUITECTURA_API.md` |
| **Modelo de Datos** | `backend/prisma/schema.prisma` | `_project-management/planV2/DOC-002_MODELO_DATOS.md` + `DIAGRAMA_ER_V2.md` |
| **Arquitectura Sistema** | `docker-compose.yml` + `backend/src/server.ts` | `_project-management/planV2/DOC-001_ARQUITECTURA_SISTEMA.md` |
| **Flujos de Proceso** | `backend/src/` (código) + `knowledge/development-log/` | `_project-management/planV2/DOC-004_FLUJO_PROCESO_COMPLETO.md` |
| **Patrones FE** | `frontend/src/router/index.tsx` + `frontend/src/hooks/` + componentes existentes | `_project-management/planV2/DOC-007_FLUJO_PANTALLAS.md` |
| **Design System** | `frontend/src/index.css` (tokens App) | `_project-management/Documentacion/05_DESIGN_SYSTEM_Especificaciones_UI.md` |
| **UX / Landing** | `frontend/src/components/landing/` (código) | `knowledge/design/` (specs copywriting y assets) |
| **Permisos / Auth** | `backend/src/middleware/` + `backend/src/services/permissions.service.ts` | `_project-management/planV2/DOC-001_ARQUITECTURA_SISTEMA.md` sección Auth |

> **Regla de jerarquía:** Si hay conflicto entre fuentes, el código implementado **siempre gana** sobre documentos de planV2. El código es la verdad final.

---

## Cadena de Consulta por Tipo de Tarea

### FE — Implementación de Componente / Página

**Orden de consulta obligatorio:**

1. **`frontend/src/router/index.tsx`** — Verificar si la ruta ya existe. Identificar el componente que la maneja. Si no existe, confirmar dónde agregarla (bajo ProtectedRoute o ruta pública).

2. **`backend/src/routes/[modulo].ts`** — Obtener los endpoints que el componente FE va a consumir: método HTTP, path exacto, query params, body. Este archivo es la verdad final, no el handoff.

3. **Componentes FE existentes** — Buscar si el componente ya existe en `frontend/src/components/features/` o `frontend/src/pages/`. Si existe, entender su estructura antes de modificarlo.

4. **`frontend/src/hooks/`** — Verificar si ya existe un hook que consume el endpoint (ej: `useProjects`, `useTasks`). Si existe, el agente lo usa — no crea uno nuevo.

5. **`frontend/src/index.css`** — Verificar tokens VTT disponibles (variables CSS `--color-*`, `--spacing-*`). El agente NO inventa tokens ni usa colores hardcodeados.

**Secciones del assignment que cada fuente alimenta:**

| Sección del Assignment | Fuente |
|------------------------|--------|
| `API/RECURSOS DISPONIBLES` | `backend/src/routes/[modulo].ts` |
| `CRITICO ANTES DE EMPEZAR` → componentes existentes | `frontend/src/components/` + `frontend/src/hooks/` |
| `RUTAS FRONTEND` | `frontend/src/router/index.tsx` |
| `ARQUITECTURA` → tokens y design system | `frontend/src/index.css` + DOC-005 |
| Contexto de la feature | `_project-management/planV2/DOC-007_FLUJO_PANTALLAS.md` |

---

### BE — Endpoint / Servicio Backend

**Orden de consulta obligatorio:**

1. **`backend/src/routes/index.ts`** — Ver qué módulos están registrados y con qué prefijo. Confirmar si el módulo ya existe o hay que crearlo.

2. **`backend/src/routes/[modulo].ts`** — Si el módulo ya existe, ver los endpoints actuales para no duplicarlos. Ver patrones de autenticación usados (`authenticateToken`, `requireCapability`).

3. **`backend/prisma/schema.prisma`** — Verificar las entidades y relaciones que el endpoint debe persistir. Confirmar nombres reales de campos (camelCase en Prisma → mismos en queries). Ver si hay campos UUID Text vs UUID nativo (ERR-006).

4. **`_project-management/planV2/DOC-003_ARQUITECTURA_API.md`** — Leer el diseño original del endpoint (parámetros, responses, reglas de negocio). Comparar contra el código para detectar drift.

5. **`backend/src/middleware/`** — Si la tarea toca auth o permisos, leer el middleware existente para entender el patrón correcto.

---

### DB — Migración / Schema

**Orden de consulta obligatorio:**

1. **`backend/prisma/schema.prisma`** — Estado actual del modelo. Ver convenciones usadas: PKs como `String @default(cuid())`, tablas con `@@map("nombre_tabla")`, etc.

2. **`_project-management/planV2/DOC-002_MODELO_DATOS.md`** + **`DIAGRAMA_ER_V2.md`** — Entender el modelo lógico de las entidades a agregar. Comparar con schema actual para detectar drift.

3. **`backend/prisma/migrations/`** — Ver las últimas migraciones para entender el patrón SQL usado. Si hay migraciones manuales (sin archivo), revisar si se usó `prisma db push` en lugar de `migrate dev`.

4. **Reglas críticas DB para VTT** (incluir SIEMPRE en briefs de DB Engineer):
   - PKs son `TEXT` en PostgreSQL (ERR-006) — nunca `UUID` nativo en SQL manual
   - Columnas camelCase requieren comillas dobles en SQL raw: `"statusId"` (ERR-008)
   - Tablas en prod son **lowercase**: `tasks`, `users` (ERR-009)

---

### DevOps — Infraestructura / Deploy

**Orden de consulta obligatorio:**

1. **`docker-compose.yml`** — Ver servicios actuales, puertos, variables de entorno, nombres de contenedores (`vtt-backend`, `shared-postgres`).

2. **`backend/.env.example`** — Variables de entorno requeridas. Verificar si la variable que necesita la tarea ya está declarada.

3. **`frontend/nginx.conf`** — Si la tarea toca routing o proxy.

4. **`_project-management/planV2/DOC-001_ARQUITECTURA_SISTEMA.md`** — Arquitectura de referencia (Hetzner VM, MinIO, PostgreSQL).

---

### Design — Componente de Landing / UI

**Orden de consulta obligatorio:**

1. **`frontend/src/components/landing/`** — Ver componentes existentes. Identificar qué ya está implementado.

2. **`_project-management/Documentacion/05_DESIGN_SYSTEM_Especificaciones_UI.md`** sección 2.0 — Tokens de la landing (oscuro, dramático, #0f172a bg, #6366f1 primary). NUNCA mezclar con tokens de la App.

3. **`knowledge/design/`** — Specs de copywriting y assets de la landing.

4. **`_project-management/planV2/DOC-008_WIREFRAMES.md`** + **`DOC-009_DESIGN_SPECS.md`** — Diseño original para referencia.

---

## Proceso Paso a Paso — Antes de Escribir un Assignment

### Paso A: Identificar el módulo y los archivos afectados (< 5 min)

```
1. Leer el handoff del PM — qué feature/módulo implementar
2. Usar Glob para encontrar el archivo de ruta:
   → Glob: backend/src/routes/[modulo]*.ts
3. Usar Glob para encontrar componentes FE:
   → Glob: frontend/src/components/features/[Modulo]*.tsx
   → Glob: frontend/src/pages/[Modulo]*.tsx
4. Anotar:
   - Ruta del archivo backend (real)
   - Ruta del componente FE (si existe o hay que crearlo)
   - Si es modificación o creación nueva
```

### Paso B: Verificar Contrato de API (< 10 min) — solo si la tarea toca API

```
1. Abrir: backend/src/routes/[modulo].ts
   → Buscar los @router.get/post/patch o router.get/post/patch
   → Copiar: método, path exacto, middleware aplicado
   → Identificar si usa authenticateToken, requireCapability

2. Si el endpoint no existe aún → confirmarlo en el assignment:
   → Marcar como [FALTA — BE debe crear primero]
   → Verificar si hay una tarea BE pendiente que lo cree

3. Verificar tipos en el mismo archivo o en:
   → backend/src/types/ (si existen)
   → Interfaces inline en el route handler
```

### Paso C: Verificar Estado de los Componentes FE (solo tareas FE)

```
1. Glob: frontend/src/components/features/*.tsx  ← componentes existentes
2. Glob: frontend/src/hooks/use*.ts  ← hooks disponibles
3. Leer router: frontend/src/router/index.tsx
   → ¿La ruta existe? ¿Está bajo ProtectedRoute?
4. Para cada archivo que el agente DEBE modificar:
   → Listar la ruta exacta en el campo CRITICO ANTES DE EMPEZAR
   → NO listar el handoff — ese ya fue leído en Fase 1
```

### Paso D: Verificar Schema Prisma (solo tareas BE o DB)

```
1. Abrir: backend/prisma/schema.prisma
2. Buscar el modelo relevante
3. Anotar:
   - Nombre real del campo (camelCase o snake_case con @map)
   - Tipo (String, Int, DateTime, etc.)
   - Si es FK o PK
   - Tabla real (@@map si existe)
4. Copiar al assignment — NO inventar nombres de campos
```

### Paso E: Revisar Reglas de Permisos (opcional — solo si la tarea toca auth)

```
Si la tarea toca autenticación, permisos o RBAC:
1. Abrir: backend/src/middleware/authorization.middleware.ts
2. Abrir: backend/src/services/permissions.service.ts
3. Ver cómo se usa requireCapability en rutas similares
4. Incluir en el assignment: patrón de middleware a seguir
```

---

## Checklist Rápido — Antes de Entregar el Assignment

```
[ ] ¿Abrí backend/src/routes/[modulo].ts para copiar paths reales?
[ ] ¿Para tareas FE: verifiqué si el componente/hook ya existe?
[ ] ¿Para tareas FE: anoté las rutas exactas en CRITICO ANTES DE EMPEZAR?
[ ] ¿El campo API/RECURSOS del assignment tiene paths verificados (no del handoff)?
[ ] ¿Para tareas DB: copié nombres reales de campos desde schema.prisma?
[ ] ¿Incluí las reglas ERR-006/ERR-008/ERR-009 en briefs de DB Engineer?
```

---

## Referencia Rápida — Documentos VTT por Tipo de Consulta

| Documento | Cuándo consultarlo |
|-----------|-------------------|
| `backend/src/routes/[modulo].ts` | **SIEMPRE** para tareas FE y BE — paths y contratos reales |
| `backend/prisma/schema.prisma` | **SIEMPRE** para tareas BE y DB — campos y tipos reales |
| `frontend/src/router/index.tsx` | **SIEMPRE** para tareas FE — rutas y ProtectedRoutes |
| `frontend/src/hooks/use*.ts` | Tareas FE — verificar hooks disponibles antes de crearlos |
| `frontend/src/index.css` | Tareas FE y Design — tokens VTT disponibles |
| `_project-management/planV2/DOC-001_ARQUITECTURA_SISTEMA.md` | Arquitectura general, tech stack, infraestructura |
| `_project-management/planV2/DOC-002_MODELO_DATOS.md` + `DIAGRAMA_ER_V2.md` | Diseño original del modelo de datos |
| `_project-management/planV2/DOC-003_ARQUITECTURA_API.md` | Diseño original de la API (intención, no verdad final) |
| `_project-management/planV2/DOC-004_FLUJO_PROCESO_COMPLETO.md` | Flujos de proceso end-to-end |
| `_project-management/planV2/DOC-007_FLUJO_PANTALLAS.md` | Navegación entre pantallas |
| `_project-management/Documentacion/05_DESIGN_SYSTEM_Especificaciones_UI.md` | Tokens y design system (sección 1 = App, sección 2 = Landing) |
| `knowledge/design/` | Assets y copywriting de la landing page |
| `docker-compose.yml` + `backend/.env.example` | Tareas DevOps — servicios y variables de entorno |

---

## Lo Que NO Hace Este Proceso

- **No reemplaza leer el código fuente** — Los documentos de planV2 son referencia de intención. El código implementado es siempre la verdad final.
- **No aplica a tareas de documentación pura** (devlogs, LOGIC.md) — Para esas, ir directo al archivo de código a documentar.
- **No genera el assignment solo** — Este proceso alimenta las secciones del template `TEMPLATE_ASIGNACION_TAREARev.md`, pero el TL aún debe redactar el assignment completo.
- **No requiere leer al nivel de detalle de colores o radio buttons** — Ese nivel de detalle lo lee el agente desde los componentes existentes.

---

## Integración con el Proceso de Asignación

Este documento complementa (no reemplaza) `PROCESO_ASIGNACION_TAREAS.md` v1.4.

**Ubicación en el flujo existente:**

```
PM Handoff recibido
      ↓
[FASE 1] Crear tareas + BRIEFs (solo desde el handoff — sin leer código)
      ↓
[ESTE PROCESO] Al asignar una tarea:
   → Paso A: Identificar archivos afectados (Glob)
   → Paso B: Verificar contrato API (routes/)
   → Paso C: Verificar componentes FE existentes
   → Paso D: Verificar schema Prisma
   → Paso E: Reglas de permisos (opcional)
      ↓
Escribir Assignment usando TEMPLATE_ASIGNACION_TAREARev.md
   → Sección API/RECURSOS DISPONIBLES = datos de routes/ real
   → Sección CRITICO = archivos FE existentes a leer
      ↓
Subir BRIEF + ASSIGNMENT como adjuntos de la tarea
      ↓
Asignar en sistema (PROCESO_ASIGNACION_TAREAS.md → Paso 4)
```

---

**Última actualización:** 2026-03-19
**Versión:** 1.0
**Aplicable desde:** Fase 12 en adelante
