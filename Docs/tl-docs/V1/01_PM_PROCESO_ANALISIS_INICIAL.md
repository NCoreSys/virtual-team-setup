# 09 — PROCESO DE CIERRE PM + HANDOFF PJM

**Capa:** Estándar (genérico, portable)
**Audiencia:** PM (Product Manager) en cualquier proyecto gestionado en VTT
**Versión:** 1.0
**Fecha:** 2026-04-22
**Complementa:** `08_FLUJO_PM.md` (flujo general PM) · `07_FLUJO_PJM.md` (flujo PJM)
**Caso validado con:** Memory Service R1 (2026-04-22)

---

## 1. PROPÓSITO

Este documento estandariza el **proceso de entrega del PM al PJM** para iniciar operativamente un proyecto en VTT. Define los pasos, entradas, salidas y gates de calidad que todo PM debe seguir para cerrar su análisis y habilitar la ejecución.

> **Principio:** el PM no se considera "cerrado" hasta que **el PJM puede ejecutar un script y cargar 100% del proyecto a VTT en una sola pasada, sin repetir análisis**.

---

## 2. CUÁNDO APLICA ESTE PROCESO

Aplica cuando:

- El proyecto tiene análisis técnico aprobado (SPEC, metodología, addendums)
- Se requiere cargar estructura completa a VTT (Project + Phases + Deliveries + Tasks + Dependencies)
- El equipo operativo (PJM, TL, agentes) aún no ha arrancado

**No aplica** cuando:

- El proyecto ya está en ejecución (se usa flujo normal de handoffs por sprint)
- El alcance aún no está cerrado (se necesita cerrar análisis primero)

---

## 3. PRERREQUISITOS

Antes de iniciar este proceso, el PM debe tener:

| Prerrequisito | Responsable | Validación |
|---------------|-------------|------------|
| Spec técnica aprobada | SA + AR + TL + PM | Documento en estado `APROBADO` |
| Reviews AR/DB/TL integrados al SPEC | PM | Changelog del SPEC refleja observaciones cerradas |
| Addendums de integración aprobados | PM | Cambios integrados al SPEC base |
| Metodología funcional documentada | PM | Doc de metodología vigente |
| Catálogo SDLC de deliverables disponible | Sistema | `ANALISIS_FASES_COMPLETO_PARA_PM.md` o equivalente |
| Estructura de fases del sistema definida | Sistema | `ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md` |
| Estándar de endpoints VTT disponible | Sistema | `PROCESO_ASIGNACION_TAREAS.md` |
| UUIDs de usuarios del proyecto creados | Admin / PM | Documento con UUIDs reales por rol |

---

## 4. LOS 9 PASOS DEL PROCESO

```
  Paso 1: Leer análisis de feature
      ↓
  Paso 2: Cerrar docs PM (freeze)
      ↓
  Paso 3: Filtrar deliverables aplicables
      ↓
  Paso 4: Definir fase de iniciación (pre-SDLC)
      ↓
  Paso 5: Consolidar plan maestro
      ↓
  Paso 6: Generar Cierre PM + Handoff operativo
      ↓
  Paso 7: Generar Task Index Seed (metadata + UUIDs)
      ↓
  Paso 8: Generar script ejecutable de carga
      ↓
  Paso 9: Generar HO de ejecución para PJM
      ↓
  [FIN: PJM ejecuta · PM firma sign-off]
```

Cada paso tiene **inputs**, **outputs**, **template de referencia** y **gate de calidad**.

---

### PASO 1 — Leer análisis de feature

**Inputs:**
- Spec técnica (versión más reciente aprobada)
- Metodología funcional
- Addendum(s) de integración cross-service
- Reviews de roles técnicos (AR, DB, TL, BE)
- Documento metodológico conceptual (si existe)

**Acciones del PM:**
1. Leer cada documento completo (no resumen)
2. Identificar decisiones ya tomadas (congeladas)
3. Identificar ambigüedades o preguntas abiertas
4. Verificar que las reviews de roles técnicos están integradas al SPEC

**Outputs:**
- Entendimiento consolidado del alcance (en un párrafo el PM debe poder explicar qué se construye)
- Lista de documentos consumidos (para el HO final)
- Lista de decisiones cerradas (D-XX con estado FROZEN)
- Lista de correcciones incorporadas (por origen: AR-OBS-XX, DB-OBS-XX, TL-OBS-XX)

**Gate de calidad:**
- [ ] PM puede explicar el producto en 1 párrafo sin consultar docs
- [ ] PM identifica mínimo 30 decisiones cerradas (proyecto promedio)
- [ ] Reviews técnicas sin observaciones abiertas

---

### PASO 2 — Cerrar docs PM (freeze)

**Inputs:**
- Outputs del Paso 1

**Acciones del PM:**
1. Para cada doc, validar si está en estado final o pendiente cierre
2. Integrar addendums al SPEC base (si son compatibles)
3. Marcar docs obsoletos/reemplazados con aviso explícito (no borrar)
4. Actualizar versionado (header, changelog, footer) de forma consistente
5. Firmar cierre como PM en cada doc

**Outputs:**
- SPEC técnica en versión final con changelog claro
- Addendums integrados o explícitamente pendientes
- Docs obsoletos marcados con aviso
- Registro de decisiones cerradas actualizado

**Template de referencia:**
- Changelog típico: tabla con `versión | fecha | cambios`
- Veredicto PM en caja ASCII (ver `PASO 6` templates)

**Gate de calidad:**
- [ ] Ningún doc PM en estado `BORRADOR` o `PENDIENTE`
- [ ] Versionado consistente entre nombre de archivo, header, changelog, footer
- [ ] Addendums integrados al SPEC base o con plan de integración

---

### PASO 3 — Filtrar deliverables aplicables

**Inputs:**
- Catálogo SDLC completo (~438 deliverables estándar)
- Contexto del proyecto (interno vs externo, stack, restricciones de alcance)

**Acciones del PM:**
1. Recorrer las 9 fases SDLC con sus subfases
2. Por cada deliverable decidir `✅ Aplica` o `❌ No aplica`
3. Para `❌` documentar razón breve (feature interna, desktop only, stack sin X, etc.)
4. Consolidar **criterios de filtrado** reutilizables
5. Calcular totales por fase + total general

**Outputs:**
- `FASES_APLICABLES_<PROYECTO>.md` con tabla por fase
- Criterios de exclusión consolidados
- Número total de deliverables aplicables (típico: 80-95% del catálogo)

**Template de referencia:**
- Memory Service R1 terminó con 390/438 (89%)
- Criterios típicos de exclusión: "feature interna", "sin usuarios externos", "desktop only", "stack sin OAuth/SP/Views"

**Gate de calidad:**
- [ ] Cada exclusión tiene razón documentada (no solo ❌)
- [ ] Totales por fase suman el total original
- [ ] Criterios de filtrado son consistentes (no hay exclusiones con criterios opuestos)

---

### PASO 4 — Definir fase de iniciación (pre-SDLC)

**Inputs:**
- Outputs del Paso 3
- Contexto operativo (VM, repo, equipo, tooling)

**Acciones del PM:**
1. Identificar tareas de setup que **no están** en el catálogo SDLC (configuración VTT, repo, VM, onboarding)
2. Agruparlas en categorías operativas: A) VTT Setup · B) Repo · C) VM · D) Team · E) Tooling · F) Documentation · G) Kickoff
3. Desglosar las tareas genéricas MEM-001..005 (o equivalentes) en sub-tareas concretas
4. Validar si las horas genéricas (ej: 11h) reflejan el trabajo real (típicamente ~32h)

**Outputs:**
- `PRE_HANDOFF_INICIACION_<PROYECTO>.md` con 20-30 sub-tareas
- Mapeo INIT-* → MEM-001..005 (qué sub-tareas absorbe cada umbrella)
- Estimación realista de horas

**Template de referencia:**
- 7 categorías A-G con 2-5 sub-tareas cada una
- Total típico: 24 sub-tareas · 32h (expande 5 tareas/11h del umbrella)

**Gate de calidad:**
- [ ] Cada sub-tarea tiene rol + horas + output claro
- [ ] Total de horas realista para el esfuerzo de setup
- [ ] Ninguna sub-tarea duplica una tarea del catálogo SDLC

---

### PASO 5 — Consolidar plan maestro

**Inputs:**
- Outputs de Pasos 3 y 4
- Listado de tareas VTT existentes (116 típico, equivalente en otros proyectos)

**Acciones del PM:**
1. Combinar: iniciación + 10 fases SDLC + tareas específicas del proyecto
2. Por cada tarea definir: **Título · Delivery VTT · Rol · Horas · Complexity · Produce (deliverables)**
3. Mapear explícitamente **tarea → deliverables individuales** (una tarea produce N documentos)
4. Calcular totales por rol, por fase, por sprint
5. Identificar dependencias críticas entre tareas

**Outputs:**
- `CONSOLIDADO_<PROYECTO>.md` con todas las tareas organizadas por fase
- Resumen por rol (horas totales por cada uno)
- Lista de dependencias críticas (típico: 10-15)

**Template de referencia:**
- Para fases de planeación/análisis: mostrar deliverables (documentos a producir)
- Para fases de desarrollo/testing/deploy: reemplazar deliverables por tareas (el código produce los docs)
- Para fase 3B Design Technical: consolidar contenido del SPEC en docs independientes

**Lección aprendida (importante):**

> Una tarea puede producir múltiples deliverables SDLC. **Explicitar la columna `Produce`** en cada tabla de tareas evita que se repita el análisis. Ejemplo: MEM-006 Problem Definition (3h) produce 4 documentos: 0.3.1, 0.3.2, 0.3.3, 0.3.4.

**Gate de calidad:**
- [ ] Cada tarea tiene el mapeo explícito `tarea → deliverables que produce`
- [ ] Suma de deliverables producidos = total de deliverables aplicables
- [ ] Dependencias críticas identificadas con impacto

---

### PASO 6 — Generar Cierre PM + Handoff operativo

**Inputs:**
- Todos los outputs anteriores

**Acciones del PM:**
1. Usar formato **V4.2 / V4.5** (ver ejemplos en `Analisis/`)
2. Estructurar en 2 partes:
   - **PARTE I: CIERRE PM DEL ANÁLISIS** — Docs consumidos · Decisiones FROZEN · Correcciones · Limitaciones · Reassignments · Veredicto ASCII
   - **PARTE II: HANDOFF OPERATIVO** — Alcance · Iniciación · Secuencia de fases · Plan completo con mapeo tarea→deliverables · Dependencias · Endpoints · Riesgos · Checklist PJM · Criterios de éxito · HOs downstream · Firmas

**Outputs:**
- `CIERRE_PM_HANDOFF_PJM_<PROYECTO>.md` (el documento principal de entrega)

**Template de referencia:**

```markdown
# CIERRE PM + HANDOFF OPERATIVO PJM — <PROYECTO>

| Metadata tabla |

## PARTE I: CIERRE PM DEL ANÁLISIS
1. Documentos consumidos
2. Decisiones PM finales (lista D-XX FROZEN)
3. Correcciones incorporadas (por origen)
4. Limitaciones documentadas (LIM-XX)
5. Reassignments aprobados (si aplica)
6. Veredicto PM (caja ASCII)

## PARTE II: HANDOFF OPERATIVO PARA PJM
7. Alcance final
8. Fase de iniciación (pre-SDLC)
9. Secuencia de fases (caja ASCII con paralelismo)
10. Plan completo por fase (con mapeo explícito tarea→deliverables)
11. Dependencias por rol
12. Dependencias críticas
13. Riesgos y mitigaciones
14. Checklist PJM antes de iniciar
15. Criterios de éxito (N items verificables)
16. Handoffs downstream (por fase, 1 por fase)
17. Firmas
```

**Regla de HOs downstream:**

> Los HOs se generan para el **líder de área** o para **roles con responsabilidad** (PM, PJM, SA, AR, QA, TL, DL). No se generan HOs individuales para cada agente ejecutor.
>
> Estructura recomendada: **1 HO por fase** (10 totales) con el líder correspondiente (TL para código, DL para diseño, PM/PJM para fases de análisis/planning).

**Gate de calidad:**
- [ ] 100% de las decisiones del PASO 2 listadas como FROZEN
- [ ] Criterios de éxito son verificables (no vagos)
- [ ] Plan de tareas incluye columna `Produce` en todas las fases
- [ ] Firmas con PM ✅ APROBADO + resto pendientes

---

### PASO 7 — Generar Task Index Seed (metadata + UUIDs)

**Inputs:**
- Output del Paso 6
- UUIDs reales de usuarios del proyecto
- UUIDs globales (status, priority)
- UUIDs de catálogos específicos (deliveries, phases) — si el proyecto ya los tiene

**Acciones del PM:**
1. Listar UUIDs de referencia (status, priority, users, phases, deliveries)
2. Por cada tarea escribir descripción de 150-300 chars (máx 2000 chars por limite VTT)
3. Validar campos obligatorios del sistema VTT:
   - `title` · `description` (≤2000) · `priorityId` · `statusId` · `assignedToId` · `assignedBy` · `category` · `complexity` (MAYÚSCULAS) · `estimatedHours` · `createdBy`
4. Mapear roles del proyecto a users VTT reales
5. Documentar 15 dependencias críticas como tuplas `(task, dependsOn)`

**Outputs:**
- `TASK_INDEX_SEED_<PROYECTO>.md` con todas las tareas y metadata para carga

**Lecciones aprendidas (importante):**

> **Errores típicos del sistema VTT a evitar:**
> - `assignedTo` se ignora silenciosamente → usar `assignedToId`
> - `priority_id` → rechazado → usar camelCase `priorityId`
> - `complexity: "medium"` → rechazado → usar MAYÚSCULAS `"MEDIUM"`
> - `description > 2000 chars` → 400 too_big

**Gate de calidad:**
- [ ] UUIDs reales verificados (no placeholders)
- [ ] Cada tarea tiene los 10 campos obligatorios del sistema
- [ ] Descripciones entre 100-2000 chars
- [ ] Roles mapeados a users VTT reales (no fallbacks ambiguos)

---

### PASO 8 — Generar script ejecutable de carga

**Inputs:**
- Output del Paso 7

**Acciones del PM:**
1. Crear script Python 3.8+ con todas las tuplas expandidas
2. Secuencia de 6 pasos:
   - 1) `POST /api/projects` (NO wizard)
   - 2) `POST /api/projects/:id/phases` × N
   - 3) `POST /api/deliveries` × N
   - 4) `POST /api/phases/:id/tasks` × N (con toda la metadata)
   - 5) `POST /api/deliveries/:id/tasks/:id` (asociar)
   - 6) `POST /api/tasks/:id/dependencies` × N
3. Helpers: `auth_token()`, `post()`, `extract_id()`, `log()`
4. Manejo de errores: auth fail aborta, delivery/dep fail solo warn
5. Output: `VTT_UUIDS_<PROYECTO>.json` con todos los UUIDs capturados

**Outputs:**
- `scripts/create_<proyecto>_vtt.py` ejecutable

**Template de referencia:**

```python
#!/usr/bin/env python3
"""Script de creación VTT — <Proyecto>"""
import os, json, urllib.request, sys, time

API_URL = os.environ.get("VTT_API_URL", "http://77.42.88.106:3000")
SERVICE_KEY = os.environ.get("VTT_SERVICE_KEY")
if not SERVICE_KEY:
    sys.exit("ERROR: Define VTT_SERVICE_KEY")

# Constantes: USERS, STATUS_PENDING, PRIORITY
# Data: PROJECT, PHASES, DELIVERIES, TASKS, DEPENDENCIES

def main():
    token = auth_token(PJM_UUID)
    uuids = {"projectId": None, "phases": {}, "deliveries": {}, "tasks": {}}

    # 6 pasos secuenciales con logging

    with open(OUTPUT_FILE, "w") as f:
        json.dump(uuids, f, indent=2)

if __name__ == "__main__":
    main()
```

**Gate de calidad:**
- [ ] Script se ejecuta con `python3 script.py` sin errores de sintaxis
- [ ] Todas las tuplas tienen el número correcto de elementos
- [ ] Variables de entorno documentadas en header
- [ ] Output JSON estructurado correctamente

---

### PASO 9 — Generar HO de ejecución para PJM

**Inputs:**
- Outputs de Pasos 6, 7 y 8

**Acciones del PM:**
1. Escribir HO dirigido específicamente al PJM con instrucciones de ejecución
2. Secciones clave:
   - Objetivo
   - Contexto (docs PM cerrados)
   - Entregable adjunto (referencia al script)
   - Prerrequisitos (checklist de ambiente)
   - Proceso de ejecución paso a paso
   - Salida esperada (muestra del log)
   - Verificación post-ejecución (checks automáticos + manuales)
   - Rollback/retry si falla
   - Acciones post-carga
   - Escalación
   - Criterio de éxito
   - Firmas

**Outputs:**
- `HO_PJM_CARGA_VTT_<PROYECTO>.md`

**Template de referencia:**

Ver `HO_PJM_CARGA_VTT_MEMORY_SERVICE.md` como ejemplo validado (2026-04-22, Memory Service R1).

**Gate de calidad:**
- [ ] Checklist de prerrequisitos es ejecutable (el PJM puede marcarlo uno a uno)
- [ ] Rollback tiene 3 opciones: completar manual, limpiar+reintentar, reanudar
- [ ] Acciones post-carga incluyen dónde guardar el JSON de UUIDs
- [ ] Criterio de éxito tiene N items verificables (típico: 5)

---

## 5. INVENTARIO COMPLETO DE ENTREGABLES

Tras los 9 pasos, el PM entrega al PJM:

| # | Documento | Paso origen | Audiencia |
|---|-----------|-------------|-----------|
| 1 | SPEC técnica final (versión cerrada) | 2 | TL, agentes técnicos |
| 2 | Metodología funcional | 2 | Todo el equipo |
| 3 | Addendums integrados | 2 | TL, agentes |
| 4 | `FASES_APLICABLES_<PROYECTO>.md` | 3 | PJM, TL |
| 5 | `PRE_HANDOFF_INICIACION_<PROYECTO>.md` | 4 | PJM, DO |
| 6 | `CONSOLIDADO_<PROYECTO>.md` | 5 | PJM, TL, todo el equipo |
| 7 | `CIERRE_PM_HANDOFF_PJM_<PROYECTO>.md` | 6 | **PJM (principal)** |
| 8 | `TASK_INDEX_SEED_<PROYECTO>.md` | 7 | PJM, TL |
| 9 | `scripts/create_<proyecto>_vtt.py` | 8 | PJM (ejecutable) |
| 10 | `HO_PJM_CARGA_VTT_<PROYECTO>.md` | 9 | **PJM (principal)** |

**Documentos críticos para el PJM:** #7, #8, #9, #10 (los cuatro últimos son el paquete de ejecución).

---

## 6. QUALITY GATES GLOBALES

Antes de firmar el HO final al PJM, el PM valida:

```
Cierre de análisis:
[ ] Todos los docs PM en estado FINAL (ninguno BORRADOR)
[ ] Todas las decisiones cerradas con código D-XX FROZEN
[ ] Todas las correcciones técnicas integradas al SPEC
[ ] Todas las limitaciones R1 documentadas (LIM-XX)

Filtro y consolidación:
[ ] Filtro de deliverables con razones documentadas
[ ] Mapeo explícito tarea → deliverables en TODAS las fases
[ ] Estimación realista de iniciación (no valores placeholder)
[ ] Dependencias críticas identificadas

Handoff operativo:
[ ] Plan por fase con líder de área claro
[ ] Criterios de éxito verificables
[ ] Riesgos con mitigación

Paquete de ejecución:
[ ] Seed con UUIDs reales (no placeholders)
[ ] Campos VTT correctos (assignedToId, priorityId, complexity MAYÚSCULAS, description ≤2000)
[ ] Script Python sin errores de sintaxis
[ ] HO PJM con rollback + verificación + sign-off
```

---

## 7. ERRORES COMUNES A EVITAR

Lecciones aprendidas de la aplicación del proceso:

| Error | Consecuencia | Corrección |
|-------|--------------|------------|
| Asumir que existen UUIDs en VTT cuando se hizo cleanup | Script falla con 404 | Confirmar con PM el estado real de VTT antes de scriptear |
| Mezclar "subfases SDLC" con "deliverables" en el conteo | Números inconsistentes (68 vs 438 vs 391) | Clarificar: subfases son agrupadores, deliverables son documentos individuales |
| No documentar mapeo tarea→deliverables | Ambigüedad que causa retrabajo | Columna `Produce` explícita en TODAS las tablas de tareas |
| Generar 1 HO por rol por sprint | Exceso de HOs (22 en un proyecto) | Regla: 1 HO por fase con líder de área |
| Omitir descripción en las tareas | PJM repite el análisis al crear las tareas | Cada tarea con descripción 150-300 chars en el seed |
| Hardcodear UUIDs en docs de PM | Stale data cuando se recrea el proyecto | Usar `TASK_INDEX_SEED_<PROYECTO>.md` como source of truth y referenciar |
| Usar wizard de creación de proyecto | Complica el control de la carga | POST simples separados: project → phases → deliveries → tasks |
| `complexity: "medium"` minúsculas | 400 Validation Error | Siempre MAYÚSCULAS: `"LOW" \| "MEDIUM" \| "HIGH"` |
| `assignedTo` en lugar de `assignedToId` | Campo ignorado, tarea sin asignar | Usar `assignedToId` siempre |

---

## 8. FLUJO POST-ENTREGA

```
PM firma HO de ejecución (HO_PJM_CARGA_VTT_<PROYECTO>.md)
       │
       ▼
PJM valida prerrequisitos del §4 del HO
       │
       ▼
PJM ejecuta `python3 create_<proyecto>_vtt.py`
       │
       ▼
PJM valida VTT_UUIDS_<PROYECTO>.json generado
       │
       ▼
PJM ejecuta checklist de verificación (§6.2 del HO)
       │
       ▼
PJM reporta al PM con log + JSON
       │
       ▼
PM firma sign-off post-carga en el HO
       │
       ▼
PM emite HO de Fase 0 Discovery (el primero operativo)
       │
       ▼
PJM descompone Fase 0 en BRIEFs por agente
       │
       ▼
Kickoff operativo del proyecto
```

---

## 9. TEMPLATES Y EJEMPLOS

**Ejemplo validado (Memory Service R1):**

| Paso | Archivo |
|------|---------|
| 2 | `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` |
| 3 | `Release2.0/01-PM/FASES_APLICABLES_MEMORY_SERVICE.md` |
| 4 | `Release2.0/01-PM/PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md` |
| 5 | `Release2.0/01-PM/CONSOLIDADO_MEMORY_SERVICE_R1.md` |
| 6 | `Release2.0/01-PM/CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md` |
| 7 | `Release2.0/01-PM/TASK_INDEX_SEED_MEMORY_SERVICE.md` |
| 8 | `Release2.0/scripts/create_memory_service_vtt.py` |
| 9 | `Release2.0/01-PM/HO_PJM_CARGA_VTT_MEMORY_SERVICE.md` |

---

## 10. RELACIÓN CON OTROS DOCUMENTOS DEL ESTÁNDAR

| Doc relacionado | Cómo se conecta |
|-----------------|-----------------|
| `08_FLUJO_PM.md` | Este proceso (09) es un SOP específico de la fase "Analysis → Cierre" del flujo general PM |
| `07_FLUJO_PJM.md` | El PJM recibe el paquete de este proceso y ejecuta la carga |
| `05_CATALOGO_DELIVERABLES.md` | Insumo para el PASO 3 (filtrado) |
| `04_ESTRUCTURA_FASES.md` | Define dónde van los artefactos generados |
| `02_OPERACION_AGENTE.md` | Define los endpoints VTT usados en el script |
| `roles/AGENT_PROFILE_BASE_PM.md` | Perfil base del PM que ejecuta este proceso |

---

## 11. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-22 | Versión inicial del estándar, validada con Memory Service R1. 9 pasos + 6 gates de calidad + 9 errores comunes documentados. |

---

**Documento:** `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md`
**Capa:** Estándar portable
**Estado:** ✅ Aprobado
**Caso de validación:** Memory Service R1 (ejecutado exitosamente 2026-04-22)

---

**PM — Martin Rivas**
CEO/Founder — Virtual Teams Tracking
