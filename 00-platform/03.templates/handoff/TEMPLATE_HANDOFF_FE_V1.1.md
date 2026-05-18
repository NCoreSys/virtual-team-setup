# HANDOFF FE: [PROYECTO] — Sprint [N]

**Documento:** HANDOFF_FE_SPRINT_[N].md  
**Versión:** 1.1  
**De:** PJM-Agent  
**Para:** FE (Frontend Engineer)  
**Fecha:** [YYYY-MM-DD]  
**Sprint:** [N] — [Nombre del Sprint]  
**Estado:** 📋 BLOCKED (espera HTMLs + BE endpoints)  
**Prerrequisitos:** APR-DL aprobado, BE endpoints en `in_review`

---

## 0. RESUMEN EJECUTIVO

[2-3 párrafos describiendo:]
- Objetivo de implementación del sprint
- Qué pantallas/componentes implementar
- Cómo interactúan con el backend
- Qué flujos de usuario habilita

**Duración total:** [X] horas  
**Pantallas a implementar:** [N]  
**Componentes nuevos:** [N]

> **⚠️ IMPORTANTE:** FE solo implementa lo que DL diseñó. Nunca diseña pantallas. Si el HTML no existe → reportar al PM antes de empezar.

---

## 1. ESTRUCTURA DE ARCHIVOS

### 1.1 Archivos a Crear

```
src/
├── features/
│   └── [feature-name]/
│       ├── components/
│       │   ├── [ComponenteA]/
│       │   │   ├── [ComponenteA].tsx
│       │   │   ├── [ComponenteA].test.tsx
│       │   │   └── index.ts
│       │   └── [ComponenteB]/
│       │       └── ...
│       ├── hooks/
│       │   ├── use[Feature].ts
│       │   └── use[Feature].test.ts
│       ├── pages/
│       │   ├── [PageName]Page.tsx
│       │   └── [PageName]Page.test.tsx
│       ├── types/
│       │   └── [feature].types.ts
│       └── index.ts
├── stores/
│   └── [feature]Store.ts (si usa Zustand)
└── services/
    └── [feature].service.ts (si tiene lógica de API compleja)
```

### 1.2 Archivos a Modificar

| Archivo | Cambio | Razón |
|---------|--------|-------|
| `src/routes/index.tsx` | Agregar rutas | Nuevas páginas |
| `src/App.tsx` | Import lazy | Code splitting |

---

## 2. RUTAS

### 2.1 Rutas Nuevas

| Ruta | Componente | Protegida | Lazy |
|------|------------|-----------|------|
| `/[path]` | `[PageName]Page` | ✅/❌ | ✅ |
| `/[path]/:id` | `[DetailPage]` | ✅/❌ | ✅ |

### 2.2 Configuración de Rutas

```typescript
// En src/routes/index.tsx

const [PageName]Page = lazy(() => import('@/features/[feature]/pages/[PageName]Page'));

// En el Router
<Route 
  path="/[path]" 
  element={
    <ProtectedRoute>
      <Suspense fallback={<PageSkeleton />}>
        <[PageName]Page />
      </Suspense>
    </ProtectedRoute>
  } 
/>
```

---

## 3. CONTRATOS API

### 3.1 Endpoints a Consumir

| Método | Endpoint | Hook/Service | Respuesta |
|--------|----------|--------------|-----------|
| GET | `/api/[recurso]` | `use[Recurso]Query` | `[Recurso][]` |
| POST | `/api/[recurso]` | `use[Recurso]Mutation` | `[Recurso]` |
| PATCH | `/api/[recurso]/:id` | `useUpdate[Recurso]` | `[Recurso]` |

### 3.2 Detalle de Contratos

#### GET /api/[recurso]

**Request:**
```typescript
// Query params
interface Get[Recurso]Params {
  page?: number;
  perPage?: number;
  filter?: string;
}
```

**Response:**
```typescript
interface Get[Recurso]Response {
  data: [Recurso][];
  meta: {
    total: number;
    page: number;
    perPage: number;
  };
}
```

**Hook:**
```typescript
// hooks/use[Recurso].ts
export function use[Recurso]Query(params: Get[Recurso]Params) {
  return useQuery({
    queryKey: ['[recurso]', params],
    queryFn: () => api.get('/api/[recurso]', { params }),
  });
}
```

#### POST /api/[recurso]

**Request:**
```typescript
interface Create[Recurso]Request {
  field1: string;
  field2: number;
}
```

**Response:**
```typescript
interface Create[Recurso]Response {
  data: [Recurso];
}
```

**Hook:**
```typescript
export function useCreate[Recurso]() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: Create[Recurso]Request) => 
      api.post('/api/[recurso]', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['[recurso]'] });
      toast.success('[Recurso] creado');
    },
    onError: (error) => {
      toast.error(error.message || 'Error al crear');
    },
  });
}
```

---

## 4. STORE (ZUSTAND)

### 4.1 Estado a Manejar

```typescript
// stores/[feature]Store.ts

interface [Feature]State {
  // Estado
  selectedId: string | null;
  filters: FilterState;
  
  // Acciones
  setSelectedId: (id: string | null) => void;
  setFilters: (filters: Partial<FilterState>) => void;
  reset: () => void;
}

export const use[Feature]Store = create<[Feature]State>((set) => ({
  selectedId: null,
  filters: defaultFilters,
  
  setSelectedId: (id) => set({ selectedId: id }),
  setFilters: (filters) => set((state) => ({ 
    filters: { ...state.filters, ...filters } 
  })),
  reset: () => set({ selectedId: null, filters: defaultFilters }),
}));
```

### 4.2 Persistencia (si aplica)

```typescript
// Si necesita persistir en localStorage
export const use[Feature]Store = create<[Feature]State>()(
  persist(
    (set) => ({
      // ...estado y acciones
    }),
    {
      name: '[proyecto]_[feature]',
      partialize: (state) => ({ filters: state.filters }),
    }
  )
);
```

---

## 5. COMPONENTES A IMPLEMENTAR

### 5.1 Resumen

| Componente | HTML de DL | Props | Estados |
|------------|-----------|-------|---------|
| `[ComponenteA]` | `[nombre].html` | title, onClick | default, hover, disabled |
| `[ComponenteB]` | `[nombre].html` | items, onSelect | empty, loading, loaded |

### 5.2 Implementación por Componente

#### [ComponenteA]

**HTML de referencia:** `Design/specs/sprint_[N]/[nombre].html`  
**UX Spec:** `Design/specs/sprint_[N]/[nombre]_SPEC.md`

**Props:**
```typescript
interface [ComponenteA]Props {
  title: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}
```

**Tests requeridos:**
- [ ] Render con props mínimas
- [ ] Click handler se llama
- [ ] Variantes aplican estilos correctos
- [ ] Estado disabled funciona

---

## 6. DEPENDENCIAS NPM

### 6.1 Nuevas Dependencias

| Paquete | Versión | Para qué |
|---------|---------|----------|
| `@dnd-kit/core` | ^6.0.0 | Drag and drop |
| `[paquete]` | ^X.Y.Z | [Propósito] |

**Instalar:**
```bash
npm install @dnd-kit/core [otros-paquetes]
```

### 6.2 Dependencias Existentes a Usar

| Paquete | Uso en este sprint |
|---------|-------------------|
| `@tanstack/react-query` | Fetching de datos |
| `zustand` | Estado global |
| `react-hook-form` | Formularios |
| `zod` | Validación |

---

## 7. TAREAS DEL SPRINT

### Fase: Implementación (Días X-Y)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| FE-001 | Implementar [Página 1] | FE | [X]h | HIGH/MEDIUM/LOW | development |
| FE-002 | Implementar [Página 2] | FE | [X]h | HIGH/MEDIUM/LOW | development |
| FE-003 | Implementar [Componente A] | FE | [X]h | MEDIUM | development |
| FE-004 | Hooks + Store | FE | [X]h | MEDIUM | development |
| FE-005 | Tests de componentes | FE | [X]h | MEDIUM | testing |

### Fase: Validación (Días Y-Z)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| DL-REVIEW | DL valida impl vs HTMLs | DL | 3h | MEDIUM | review |
| QA-FE | QA testea FE | QA | [X]h | MEDIUM | testing |

---

## 8. DEPENDENCIAS ENTRE TAREAS

| Tarea | Depende de | Tipo | Nota |
|-------|-----------|------|------|
| FE-001 | APR-DL, BE-XXX | FS | Necesita HTML + endpoint |
| FE-002 | FE-001 | FS | Flujo secuencial |
| FE-003 | DL-003 | FS | Componente diseñado |
| FE-004 | FE-001, FE-002 | FS | Hooks para páginas |
| FE-005 | FE-001, FE-002, FE-003 | FS | Tests post-implementación |
| DL-REVIEW | FE-005 | FS | Post-implementación completa |

> **Regla crítica:** FE no comienza hasta que: (1) APR-DL está aprobado, (2) BE endpoints están en `in_review`.

---

## 9. VTT PLANNING DATA

> **TL crea y asigna las tareas FE en VTT** al activarse el Gate FE (ver Handoff TL §11).  
> FE recibe la asignación y puede usar esta tabla como referencia de estimaciones y dependencias.  
> FE no crea sus tareas — solo ejecuta las que TL creó.

| Tarea | estimatedHours | complexity | category | dependsOn |
|-------|---------------|-----------|----------|-----------|
| FE-001 | [X] | [HIGH/MEDIUM/LOW] | development | APR-DL, BE-XXX |
| FE-002 | [X] | [HIGH/MEDIUM/LOW] | development | FE-001 |
| FE-003 | [X] | MEDIUM | development | DL-003 |
| FE-004 | [X] | MEDIUM | development | FE-001, FE-002 |
| FE-005 | [X] | MEDIUM | testing | FE-003, FE-004 |

**Total FE scope:** [X]h

---

## 10. DOCUMENTOS DINÁMICOS A ACTUALIZAR

| Documento | Quién actualiza | Cuándo | Verificado en |
|-----------|----------------|--------|---------------|
| `*.LOGIC.md` | FE | Por cada archivo creado/modificado | Code Review (TL) |
| `COMPONENT_LIBRARY.md` | FE | Si hay componentes reutilizables | Code Review (TL) |

---

## 11. DoD — FE

### Implementación:
- [ ] Todas las páginas implementadas según HTMLs de DL
- [ ] Todos los componentes implementados según specs
- [ ] Estados visuales funcionando (empty, loading, error, success)
- [ ] Responsive funcionando (desktop, tablet, mobile)
- [ ] Integración con API funcionando

### Calidad:
- [ ] Tests de componentes escritos (cobertura ≥ 60%)
- [ ] Sin errores de ESLint
- [ ] Sin errores de TypeScript
- [ ] Accesibilidad verificada (keyboard nav, ARIA labels)
- [ ] `.LOGIC.md` actualizado por cada archivo

### Validación:
- [ ] DL-REVIEW pasado (impl coincide con diseño)
- [ ] QA-FE pasado (funcionalidad OK)
- [ ] Code Review aprobado por TL

---

## 12. GATES DE APROBACIÓN

| Gate | Condición | Acción en VTT |
|------|-----------|---------------|
| FE puede arrancar | APR-DL aprobado + BE endpoints `in_review` | TL notifica |
| Code Review | PRs creados | TL revisa |
| DL-REVIEW | FE completado | DL valida |
| QA-FE | DL-REVIEW completado + FE aprobado | TL notifica a QA |
| Sprint cerrado | Todas las validaciones OK | Parte de 4 firmas |

---

## 13. MANEJO DE ERRORES

### 13.1 Patrón de Error Handling

```typescript
// Componente con error handling
function [PageName]Page() {
  const { data, isLoading, error } = use[Recurso]Query();
  
  if (isLoading) return <PageSkeleton />;
  
  if (error) {
    return (
      <ErrorState
        message="No pudimos cargar los datos"
        onRetry={() => refetch()}
      />
    );
  }
  
  if (!data?.length) {
    return <EmptyState message="No hay datos aún" />;
  }
  
  return <[Content] data={data} />;
}
```

### 13.2 Toast de Errores

```typescript
// En mutations
onError: (error: ApiError) => {
  toast.error(error.message || 'Ocurrió un error');
}
```

---

## 14. REFERENCIAS

| Documento | Ubicación | Para qué |
|-----------|-----------|----------|
| HTMLs de DL | `Design/specs/sprint_[N]/` | Markup a implementar |
| UX Specs | `Design/specs/sprint_[N]/` | Comportamientos detallados por pantalla |
| `API_CONTRACT.md` | `backend/knowledge/` | Contratos de API verificados |
| `TESTING_GUIDE.md` | `_project_manager/Templates/` | Cómo testear componentes FE |
| `CODE_REVIEW_GUIDE.md` | `_project_manager/Templates/` | Checklist que TL usa en Code Review |

---

## 15. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | [YYYY-MM-DD] | PJM-Agent | Versión inicial |
| 1.1 | 2026-03-30 | PJM-Agent | TL crea tareas FE (no FE), rutas Design/specs/, gate QA-FE con TL notifica, referencias actualizadas |

---

**FIN DEL HANDOFF FE**
