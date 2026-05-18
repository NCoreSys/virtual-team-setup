# PROMPT DE CONTINUACIÓN — DICCIONARIO DE DELIVERABLES SDLC

## Contexto

Estamos generando un **Diccionario de Deliverables** para un SDLC de 8 fases (0-7) con 438 deliverables totales. El diccionario documenta cada deliverable con un template estandarizado para que agentes de un sistema multi-agente (VTT) y humanos sepan exactamente qué es cada documento, quién lo produce, qué inputs necesita, y qué habilita.

## Archivos de referencia necesarios

Adjunta estos 2 archivos a la conversación:

1. **ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3_1.md** — Estructura de carpetas y naming convention del proyecto
2. **ANALISIS_FASES_COMPLETO_PARA_PM.md** — Catálogo completo de las 8 fases con 438 deliverables (fuente de datos)

## Template por deliverable

Cada deliverable se documenta con esta estructura exacta:

```markdown
### [ID] [Nombre del Deliverable]

| Campo | Valor |
|-------|-------|
| **Fase** | XX-Nombre |
| **Subfase** | X.X Nombre |
| **Responsable** | Rol que es dueño del resultado |
| **Ejecuta** | Rol/agente que hace el trabajo operativo |
| **Aprueba** | Rol que da go/no-go |
| **Formato** | PDF/MD/Figma/Tabla/etc |
| **Obligatorio** | ✅ / ⚪ Opcional |
| **Esfuerzo típico** | X días |
| **Frecuencia** | Una vez / Por sprint / Continua |

**Perfil de ejecución:** Qué habilidades necesita quien lo ejecuta. 
En VTT: qué puede hacer un agente y qué no. Qué brief necesita del responsable.

**Qué es:** Descripción concreta del documento/artefacto.

**Para qué sirve:** Qué decisión habilita o qué riesgo mitiga.

**Inputs requeridos:**
- Deliverables previos necesarios (con ID)
- Datos, acceso o herramientas requeridas

**Dependencias (predecessors):**
- `X.X.X` Nombre *(obligatorio/recomendado)*

**Habilita (successors):**
- `X.X.X` Nombre — qué deliverables dependen de este

**Audiencia:**
- **Rol** — para qué lo usa

**Secciones esperadas:**
1. Sección 1
2. Sección 2
(estructura interna mínima del documento)

**Criterio de completitud:**
- [ ] Check verificable 1
- [ ] Check verificable 2

**Anti-patrones:**
- ❌ **Nombre:** Descripción del error común.

**Template:** `ruta/al/template` *(pendiente)*
```

**Campos clave que NO deben omitirse:**
- **Ejecuta** — diferente del Responsable. El responsable es dueño, el ejecuta hace el trabajo.
- **Perfil de ejecución** — incluye explícitamente qué puede hacer un agente VTT y qué no.
- **Dependencias y Habilita** — crea el grafo de precedencia entre deliverables.
- **Anti-patrones** — errores comunes, tan importante como lo que SÍ hacer.

## Al final de cada archivo incluir:

1. **Tabla resumen de ejecutores** con columnas: Deliverable | Responsable | Ejecuta | Delegable VTT (✅/🔶/❌)
2. **Nombre del siguiente archivo** a generar
