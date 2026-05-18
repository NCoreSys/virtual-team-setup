# HANDOFF DL: [PROYECTO] — Sprint [N]

**Documento:** HANDOFF_DL_SPRINT_[N].md  
**Versión:** 1.1  
**De:** PJM-Agent  
**Para:** DL (Design Lead)  
**Fecha:** [YYYY-MM-DD]  
**Sprint:** [N] — [Nombre del Sprint]  
**Estado:** 📋 READY  
**Prerrequisitos:** [Lista de dependencias o "Ninguno"]

---

## 0. RESUMEN EJECUTIVO

[2-3 párrafos describiendo:]
- Objetivo de diseño del sprint
- Contexto del proyecto y flujo del usuario
- Qué pantallas/componentes se necesitan
- Cómo encaja con el diseño existente

**Duración total:** [X] horas  
**Pantallas a diseñar:** [N]  
**Componentes nuevos:** [N]

---

## 1. PANTALLAS A DISEÑAR

### 1.1 Resumen de Pantallas

| ID | Pantalla | Descripción | Complejidad | Estimado |
|----|----------|-------------|-------------|----------|
| DL-001 | [Nombre pantalla] | [Descripción breve] | HIGH/MEDIUM/LOW | [X]h |
| DL-002 | [Nombre pantalla] | [Descripción breve] | HIGH/MEDIUM/LOW | [X]h |

### 1.2 Flujo de Navegación

```
[Pantalla A]
     │
     ▼
[Pantalla B] ──────────────────┐
     │                         │
     ├── Acción 1 ──▶ [Pantalla C]
     │                         │
     └── Acción 2 ──▶ [Pantalla D]
                               │
                               ▼
                         [Pantalla E]
```

---

## 2. DETALLE POR PANTALLA

### 2.1 [Nombre Pantalla] (DL-001)

**Propósito:** [Qué hace el usuario en esta pantalla]

**Elementos requeridos:**
- [ ] [Elemento 1: descripción]
- [ ] [Elemento 2: descripción]
- [ ] [Elemento 3: descripción]

**Estados a diseñar:**
| Estado | Descripción | Notas |
|--------|-------------|-------|
| Empty | Sin datos | Mostrar mensaje + CTA |
| Loading | Cargando datos | Skeleton o spinner |
| Loaded | Con datos | Estado principal |
| Error | Error de carga | Mensaje + retry |

**Acciones del usuario:**
1. [Acción 1] → [Qué sucede]
2. [Acción 2] → [Qué sucede]

**Responsive:**
| Breakpoint | Adaptación |
|------------|------------|
| Desktop (≥1024px) | [Descripción] |
| Tablet (768-1023px) | [Descripción] |
| Mobile (<768px) | [Descripción] |

---

### 2.2 [Nombre Pantalla] (DL-002)

[Repetir estructura anterior para cada pantalla]

---

## 3. COMPONENTES NUEVOS

### 3.1 Resumen de Componentes

| Componente | Usado en | Props principales | Variantes |
|------------|----------|-------------------|-----------|
| [ComponenteA] | DL-001, DL-002 | title, onClick | primary, secondary |
| [ComponenteB] | DL-003 | items, onSelect | — |

### 3.2 Especificación de Componentes

#### [ComponenteA]

**Props:**
```typescript
interface [ComponenteA]Props {
  title: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}
```

**Estados:**
- Default
- Hover
- Active/Pressed
- Disabled
- Focus (accesibilidad)

**Medidas:**
- Altura: [X]px
- Padding: [X]px [Y]px
- Border radius: [X]px

---

## 4. DESIGN SYSTEM

### 4.1 Tokens a Usar

| Categoría | Token | Valor | Uso |
|-----------|-------|-------|-----|
| Color | `--primary-500` | #3B82F6 | Acciones principales |
| Color | `--gray-100` | #F3F4F6 | Backgrounds |
| Spacing | `--space-4` | 16px | Padding estándar |
| Font | `--text-lg` | 18px | Títulos de sección |

### 4.2 Tokens Nuevos (si aplica)

| Token | Valor | Propósito |
|-------|-------|-----------|
| `--[nuevo-token]` | [valor] | [Para qué se usa] |

> **Si no hay tokens nuevos:** "Este sprint usa tokens existentes del Design System."

### 4.3 Iconografía

| Icono | Nombre | Usado en | Fuente |
|-------|--------|----------|--------|
| 🔍 | search | Header | Lucide |
| ➕ | plus | Botón agregar | Lucide |

---

## 5. ASSETS REQUERIDOS

| Asset | Formato | Tamaños | Notas |
|-------|---------|---------|-------|
| [Nombre] | SVG | — | Exportar desde Figma |
| [Nombre] | PNG | 1x, 2x | Para fallback |

**Ubicación de exportación:** `Design/specs/sprint_[N]/assets/`

---

## 6. ENTREGABLES

### 6.1 Por Pantalla

| Pantalla | HTML | UX Spec | Assets |
|----------|------|---------|--------|
| [Nombre] | `[nombre].html` | `[nombre]_SPEC.md` | ✅/❌ |

### 6.2 Estructura de Archivos

```
Design/specs/sprint_[N]/
├── [pantalla-1].html
├── [pantalla-2].html
├── [pantalla-1]_SPEC.md
├── [pantalla-2]_SPEC.md
├── assets/
│   └── [assets exportados]
└── tokens/
    └── new_tokens.json (si aplica)
```

---

## 7. TAREAS DEL SPRINT

### Fase: Diseño (Días 1-X)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| DL-001 | HTML + Spec [Pantalla 1] | DL | [X]h | HIGH/MEDIUM/LOW | design |
| DL-002 | HTML + Spec [Pantalla 2] | DL | [X]h | HIGH/MEDIUM/LOW | design |
| DL-003 | Componentes nuevos | DL | [X]h | MEDIUM | design |
| DL-004 | Assets exportados | DL | [X]h | LOW | design |

### Fase: Validación (Días X-Y)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| APR-DL | PM aprueba diseños | PM | [X]h | LOW | review |
| DL-REVIEW | Validar impl FE vs HTMLs | DL | 3h | MEDIUM | review |

---

## 8. DEPENDENCIAS ENTRE TAREAS

| Tarea | Depende de | Tipo | Nota |
|-------|-----------|------|------|
| DL-002 | DL-001 | FS | Flujo secuencial |
| DL-003 | DL-001, DL-002 | FS | Componentes usados en ambas |
| APR-DL | DL-001, DL-002, DL-003, DL-004 | FS | PM aprueba todo |
| DL-REVIEW | FE completado | FS | Post-implementación |

---

## 9. VTT PLANNING DATA

> **DL crea** sus tareas de diseño (DL-001..DL-00N, APR-DL) en el sistema.  
> **DL-REVIEW es creada por TL** cuando FE pasa a `in_review` (Gate en Handoff TL §11).  
> DL no necesita crear DL-REVIEW — solo ejecutarla cuando TL la asigne.

| Tarea | estimatedHours | complexity | category | dependsOn |
|-------|---------------|-----------|----------|-----------|
| DL-001 | [X] | [HIGH/MEDIUM/LOW] | design | — |
| DL-002 | [X] | [HIGH/MEDIUM/LOW] | design | DL-001 |
| DL-003 | [X] | MEDIUM | design | DL-001, DL-002 |
| DL-004 | [X] | LOW | design | DL-003 |
| APR-DL | 1 | LOW | review | DL-004 |
| DL-REVIEW | 3 | MEDIUM | review | [TL la crea al gate FE — no crear manualmente] |

**Total DL scope:** [X]h

---

## 10. DOCUMENTOS DINÁMICOS A ACTUALIZAR

| Documento | Quién actualiza | Cuándo | Verificado en |
|-----------|----------------|--------|---------------|
| `DESIGN_SYSTEM.md` | DL | Si hay tokens nuevos | APR-DL (PM) |
| `COMPONENT_LIBRARY.md` | DL | Si hay componentes nuevos | APR-DL (PM) |

---

## 11. DoD — DL

### Diseño:
- [ ] Todos los HTMLs generados según specs
- [ ] UX Specs completos para cada pantalla
- [ ] Estados visuales diseñados (empty, loading, error, success)
- [ ] Responsive verificado (desktop, tablet, mobile)

### Design System:
- [ ] Tokens nuevos documentados (si aplica)
- [ ] Componentes nuevos especificados
- [ ] Assets exportados en formatos correctos

### Validación:
- [ ] PM aprobó diseños (APR-DL)
- [ ] TL notificado que FE puede arrancar
- [ ] DL-REVIEW completado post-implementación FE

### Documentación:
- [ ] Archivos en estructura correcta
- [ ] Specs legibles para FE

---

## 12. GATES DE APROBACIÓN

| Gate | Condición | Acción en VTT |
|------|-----------|---------------|
| DL puede arrancar | Sprint iniciado | PJM notifica |
| PM revisa diseños | Todos los HTMLs + Specs listos | DL solicita APR-DL |
| FE puede arrancar | APR-DL aprobado + BE endpoints in_review | TL notifica a FE |
| DL-REVIEW inicia | FE completado | TL notifica a DL |
| Sprint cerrado | DL-REVIEW completada (firma DL) | Parte de las 4 firmas de cierre |

---

## 13. COORDINACIÓN CON FE

### Lo que FE espera de DL:

1. **HTMLs completos:** Markup funcional, no placeholders
2. **Specs detallados:** Comportamientos, estados, interacciones
3. **Tokens referenciados:** Usar variables CSS, no valores hardcodeados
4. **Assets listos:** SVGs optimizados, PNGs en múltiples resoluciones

### Comunicación:

- **Preguntas de FE sobre diseño:** DL responde en < 4h
- **Cambios post-aprobación:** Requieren nuevo APR-DL

**Discrepancias en DL-REVIEW:**
1. DL postea comentario en la tarea DL-REVIEW listando todos los items con discrepancia
2. DL mueve DL-REVIEW a `in_review` con el comentario de entrega
3. TL revisa el comentario → crea FIX tasks para FE (sin crear issue en VTT)
4. FE corrige → DL re-valida en un ciclo corto

> ⚠️ **NO crear issues VTT para discrepancias DL-REVIEW** — eso pone la tarea en `on_hold` automáticamente y rompe el flujo de cierre.

---

## 14. REFERENCIAS

| Documento | Ubicación | Para qué |
|-----------|-----------|----------|
| `DESIGN_SYSTEM.md` | `Design/` | Tokens y patrones del proyecto |
| `COMPONENT_LIBRARY.md` | `Design/` | Componentes existentes |
| `METODOLOGIA_EJECUCION_SPRINTS.md` | `_project_manager/Templates/` | Proceso completo |
| `CODE_REVIEW_GUIDE.md` | `_project_manager/Templates/` | Criterios que TL usa en Code Review (afecta DL-REVIEW) |

---

## 15. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | [YYYY-MM-DD] | PJM-Agent | Versión inicial |
| 1.1 | 2026-03-30 | PJM-Agent | DL-REVIEW creada por TL, proceso discrepancias sin issues, gate Sprint cerrado corregido, rutas Design/specs/, referencias actualizadas |

---

**FIN DEL HANDOFF DL**
