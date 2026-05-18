# 📋 TEMPLATE: Asignación de Tarea a Agente

**Versión:** 3.0 — Modelo Dinámico V4
**Usar este template cada vez que asignes una tarea a un agente**

---

```
Hola [NOMBRE_AGENTE],

[CONTEXTO_BREVE: 1-2 líneas explicando el estado del proyecto o sprint]

Te asigno la siguiente tarea:

### 🎯 TAREA ASIGNADA

**[ID_TAREA]: [TITULO_TAREA]**
- Estimación: [X] horas
- Complejidad: [low | medium | high | critical]
- Categoría: [feature | bug | improvement | documentation | refactor | test | infrastructure]
- Prioridad: P[0-3] - [CRÍTICO/ALTO/MEDIO/BAJO]
- Inicio planificado: YYYY-MM-DD (para Gantt — opcional)
- Fin planificado: YYYY-MM-DD (para Gantt — opcional)
- Brief: `briefs/[sprint]/[ID_TAREA]_[nombre].md`
- Branch: `feature/[ID_TAREA]`

---

### 📋 ANTES DE EMPEZAR - LEE ESTO PRIMERO

1. **Reglas del Proyecto**: `.claude/rules/PROJECT_RULES.md`
   - ⚠️ Si es tu primera tarea, léelo completo
   - ⚠️ Si ya lo leíste, revisa sección 6.5 (Workflow 12 pasos) y sección 9 (Checklist)
   - ⚠️ Revisa sección 11 "Lo que NO Debes Hacer"

2. **Tu OPERATIVO**: `.claude/agents/OPERATIVO_[ROL]_MEMORY-SERVICE.md`
   - Rutina de apertura, endpoints VTT, credenciales

3. **Configuración Git** (ejecutar ANTES de hacer commits):
   ```bash
   git config user.name "Martin Rivas"
   git config user.email "martin.rivas@prompt-ai.studio"
   ```

4. **Guía Modelo Dinámico V4**: `knowledge/GUIA_AGENTES_MODELO_DINAMICO_V4.md`
   - Referencia de todos los endpoints VTT V4 disponibles

---

### 📝 ENTREGABLES OBLIGATORIOS

TODA tarea debe entregar (N/A si no aplica, nunca omitir):

| # | Entregable | Ubicación | Obligatorio |
|---|------------|-----------|-------------|
| 1 | **Código** | `src/...` | ✅ Sí |
| 2 | **Development Log** | `knowledge/development-log/YYYY-MM-DD_[ID]_[desc].md` | ✅ Sí |
| 3 | **Code Logic** | `knowledge/code-logic/[espejo]/[archivo].LOGIC.md` (1 por archivo) | ✅ Sí |
| 4 | **Commit + PR** | GitHub — branch `feature/[ID_TAREA]` | ✅ Sí |
| 5 | **Swagger Docs** | JSDoc inline + visible en `/api-docs` (si hay endpoints) | ✅ Si hay endpoints |
| 6 | **Devlog entries en VTT** | `POST /api/tasks/[ID]/devlog-entries` — decisiones, blockers, ADRs | ✅ Sí |
| 7 | **Criterios cumplidos** | `POST /api/tasks/[ID]/criteria/[criteriaId]/fulfill` | ✅ Sí |
| 8 | **TrackableItems** | Crear/vincular si aplica (RFs, ADRs, User Stories, KPIs) | ✅ Si aplica / N/A |
| 9 | **Review gate limpio** | `GET /api/tasks/[ID]/review-gate` → `canProceedToReview: true` | ✅ Sí |

⚠️ **Si falta UNO → ENTREGA INCOMPLETA**

---

### ⚠️ CRÍTICO ANTES DE EMPEZAR

**El brief tiene sección "[NOMBRE_SECCION]"** con [N] archivos que DEBES leer primero:

1. `[RUTA_ARCHIVO_1]` - [PROPOSITO]
2. `[RUTA_ARCHIVO_2]` - [PROPOSITO]
3. `[RUTA_ARCHIVO_3]` - [PROPOSITO]
[... más archivos si aplica]

**NO implementes sin leer estos archivos primero.**

---

### 🔴 [TITULO_PUNTO_CRITICO_ESPECIFICO]

[DESCRIPCION_DETALLADA_DEL_PUNTO_CRITICO]

**[Subtítulo si aplica]**: `[archivo_critico]`
- [Instrucción específica 1]
- [Instrucción específica 2]

**[Especificación técnica crítica]**:
```[LENGUAJE]
[CODIGO_O_ESPECIFICACION_EJEMPLO]
```

[ENFASIS_FINAL: ej "El brief tiene el código completo ya corregido según este diseño."]

---

### 📚 LO QUE CONTIENE EL BRIEF

El brief de [ID_TAREA] tiene **[N]+ líneas** con TODO lo necesario:
- ✅ [ITEM_1]
- ✅ [ITEM_2]
- ✅ [ITEM_3]
- ✅ [ITEM_4]
- ✅ [ITEM_5]

**No necesitas inventar nada, solo implementar lo que está especificado.**

---

### 🔌 [API/RECURSOS] DISPONIBLE[S]

[SI ES BACKEND/FRONTEND: Listar endpoints]

**✅ YA FUNCIONAN** (puedes usarlos):
```bash
[METODO] [URL_COMPLETA] - [Descripción]
```

**⚠️ EN DESARROLLO** (esperar a [TAREA]):
```bash
[METODO] [URL_COMPLETA] - [Descripción]
```

**❌ NO EXISTEN** (no implementar aún):
```bash
[METODO] [URL_COMPLETA] - [Razón]
```

[SI ES DB: Listar tablas/modelos]
```sql
[ESQUEMA_O_MODELO]
```

[SI ES DISEÑO: Listar componentes]
- [COMPONENTE_1]
- [COMPONENTE_2]

[NOTA]: [recurso] funciona y está [probado/documentado]. Puedes [verificar_como] antes de empezar.

---

### ✅ CRITERIOS DE ACEPTACIÓN

Los CAs están registrados en VTT. Al completar cada uno, reportar cumplimiento:
```bash
POST /api/tasks/[ID_TAREA]/criteria/[criteriaId]/fulfill
{ "status": "met", "evidence": "Descripción de evidencia", "notes": "Notas opcionales" }
```

| CA | criteriaId | Criterio | Cómo verificar |
|----|------------|----------|----------------|
| CA-1 | [UUID] | [CRITERIO_1] | [COMO_VERIFICAR] |
| CA-2 | [UUID] | [CRITERIO_2] | [COMO_VERIFICAR] |
| CA-3 | [UUID] | [CRITERIO_3] | [COMO_VERIFICAR] |

---

### 📊 DEVLOG ENTRIES — QUÉ REGISTRAR

Durante la ejecución registrar en VTT (`POST /api/tasks/[ID]/devlog-entries`):

| Cuándo registrar | categoryCode | severity |
|-----------------|--------------|----------|
| Tomas una decisión técnica | `decision` | null |
| Detectas deuda técnica | `tech_debt` | high/medium/low |
| Hay un blocker | `blocker` | critical/high |
| Identificas un riesgo | `risk` | high/medium |
| Resultado de testing | `testing_note` | según impacto |
| Observación relevante | `observation` | null |
| Mejora para iteración futura | `improvement` | medium/low |
| Issue de diseño/marca (DL) | `brand_issue` | según impacto |

**IMPORTANTE:** Los entries con `severity=critical|high` y `status=pending` bloquean el gate de revisión.
Resolverlos antes de mover a `task_in_review`.

---

### 🔗 TRACKABLE ITEMS — CREAR O VINCULAR SI APLICA

Si la tarea genera o implementa un RF, ADR, User Story, Bug formal o KPI:

```bash
# Crear nuevo TrackableItem
POST /api/projects/[PROJECT_ID]/trackable-items
{ "typeCode": "ADR", "title": "...", "description": "...", "priority": "high" }

# Vincular tarea a un TrackableItem existente
POST /api/trackable-items/[ITEM_ID]/tasks
{ "taskId": "[ID_TAREA]" }
```

TrackableItems a crear/vincular en esta tarea:
- [TRACKABLE_1]: [DESCRIPCION] — [crear | vincular]
- N/A si no aplica

---

### 🗂️ CODE LOGIC - REGLA FUNDAMENTAL

> UN archivo .LOGIC.md por CADA archivo de código que crees o modifiques

**Ubicación espejo**:
```
src/controllers/ejemplo.ts
         ↓
knowledge/code-logic/controllers/ejemplo.LOGIC.md
```

**Si CREAS archivo nuevo**:
1. Crear el archivo de código en `src/...`
2. Crear el archivo `.LOGIC.md` en ubicación espejo
3. Documentar: propósito, dependencias, flujo, decisiones

**Si MODIFICAS archivo existente**:
1. **BUSCAR** si ya existe el archivo `.LOGIC.md`
2. Si existe: **ACTUALIZAR** (no crear uno nuevo)
3. Agregar entrada en "Historial de Cambios"
4. Si no existe: **CREAR** el archivo `.LOGIC.md`

**Archivos para esta tarea** (crear/actualizar .LOGIC.md):
- `[RUTA_ARCHIVO_1]` → `knowledge/code-logic/[espejo]/[archivo_1].LOGIC.md` (crear)
- `[RUTA_ARCHIVO_2]` → `knowledge/code-logic/[espejo]/[archivo_2].LOGIC.md` (actualizar)

**NUNCA:**
- ❌ Crear un segundo archivo de lógica para el mismo código
- ❌ Dejar un archivo de código sin su archivo de lógica
- ❌ Incluir código fuente en el archivo de lógica (solo descripciones)

---

### 📝 WORKFLOW (12 pasos)

**0. Crear rama de Git** ⚠️ NO OLVIDAR
```bash
git checkout -b feature/[ID_TAREA]
```

**1. Mover a in_progress en VTT:**
```bash
curl -X PATCH "$VTT_BASE_URL/api/tasks/[ID_TAREA]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56", "changedBy": "$AGENT_UUID"}'
```

**2. Leer brief completo** ([N] líneas)

**3. Leer los [N] archivos** listados arriba

**4. [PASO_ESPECIFICO]** [detalles]

**5. Implementar [ARCHIVOS_A_CREAR]** siguiendo especificación del brief y SPEC v1.9

**6. Registrar devlog entries en VTT** durante la implementación:
```bash
POST $VTT_BASE_URL/api/tasks/[ID_TAREA]/devlog-entries
{ "categoryCode": "decision", "severity": null, "title": "...", "reportedBy": "$AGENT_UUID" }
```

**7. Crear archivos .LOGIC.md** (uno por archivo de código)

**8. Reportar cumplimiento de CAs** en VTT:
```bash
POST $VTT_BASE_URL/api/tasks/[ID_TAREA]/criteria/[criteriaId]/fulfill
{ "status": "met", "evidence": "Descripción de evidencia" }
```

**9. Crear/vincular TrackableItems** si aplica

**10. Crear Development Log** completo

**11. Commit y push:**
```bash
git add [ARCHIVOS_ESPECIFICOS]
git commit -m "[tipo] [ID_TAREA]: [Descripción breve]

- [Cambio 1]
- [Cambio 2]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #[ID_TAREA]"

git push origin feature/[ID_TAREA]
```

**Tipos de commit**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

**12. Verificar review gate y mover a in_review:**
```bash
# Verificar gate primero
curl -s "$VTT_BASE_URL/api/tasks/[ID_TAREA]/review-gate" \
  -H "Authorization: Bearer $TOKEN"

# Si canProceedToReview = true → mover a in_review
curl -X PATCH "$VTT_BASE_URL/api/tasks/[ID_TAREA]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId": "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d", "changedBy": "$AGENT_UUID"}'
```

**13. Crear PR:**
```bash
gh pr create \
  --title "[[ID_TAREA]] [Título descriptivo]" \
  --body "Descripción de cambios. Ver devlog para detalles." \
  --base main
```

---

### 📂 ARCHIVOS A CREAR/MODIFICAR

**Archivos nuevos**:
```
[RUTA_COMPLETA_ARCHIVO_1]
[RUTA_COMPLETA_ARCHIVO_2]
```

**Archivos a modificar**:
```
[RUTA_COMPLETA_ARCHIVO_A]
[RUTA_COMPLETA_ARCHIVO_B]
```

**Code Logic** (crear/actualizar):
```
knowledge/code-logic/[espejo]/[archivo_1].LOGIC.md
knowledge/code-logic/[espejo]/[archivo_2].LOGIC.md
knowledge/code-logic/[espejo]/[archivo_a].LOGIC.md (actualizar)
```

[NOTA_ADICIONAL si aplica]

---

### ✅ CHECKLIST DE ENTREGA (Revisar ANTES de reportar)

**Funcionalidad:**
- [ ] Código compila/ejecuta sin errores
- [ ] Probé que funciona localmente
- [ ] [VALIDACION_ESPECIFICA_1]
- [ ] [VALIDACION_ESPECIFICA_2]

**Calidad de Código:**
- [ ] Seguí arquitectura existente
- [ ] Nombres consistentes con el proyecto
- [ ] Sin console.log de debug
- [ ] Manejo de errores con try-catch

**Documentación:**
- [ ] Code Logic creado/actualizado para CADA archivo de código
- [ ] Development Log completo con decisiones técnicas
- [ ] Swagger JSDoc en cada endpoint nuevo (si aplica)
- [ ] Swagger visible en /api-docs con "Try it out" funcional (si aplica)

**VTT V4:**
- [ ] Devlog entries registrados (decisiones, blockers, ADRs, mejoras)
- [ ] Todos los blockers severity=critical|high resueltos
- [ ] CAs reportados con fulfill en VTT
- [ ] TrackableItems creados/vinculados (o N/A confirmado)
- [ ] Review gate: `canProceedToReview = true`

**Git:**
- [ ] Branch `feature/[ID_TAREA]` creado desde main actualizado
- [ ] Commit con Co-Authored-By obligatorio
- [ ] Push exitoso
- [ ] PR creado con `gh pr create`

**Estado VTT:**
- [ ] Tarea movida a `task_in_review`
- [ ] Reporte de entrega enviado al TL (formato SKL-REPORT-01)

#### Criterios Funcionales del Brief:
- [ ] [CRITERIO_1]
- [ ] [CRITERIO_2]
- [ ] [CRITERIO_3]
- [ ] [CRITERIO_4]
- [ ] [CRITERIO_5]

⚠️ **Si falta UNO de estos checks → NO REPORTAR COMO COMPLETADA**

---

### 📤 FORMATO DE REPORTE AL COMPLETAR

Usar SKL-REPORT-01 (`00-platform/06.Skills/report/SKL-REPORT-01_entrega-tarea.md`).

Todos los campos obligatorios — poner N/A si no aplica, nunca omitir secciones.

---

**Empieza leyendo el brief completo y los [N] archivos de referencia. Avísame cuando completes la tarea.**

[NOTA_SIGUIENTE_PASO: ej "Una vez apruebe esta tarea, te asignaré [PROXIMA_TAREA]."]

Saludos,
Tech Lead
```

---

## 📝 NOTAS DE USO DEL TEMPLATE

### Cuándo usar este template:
- ✅ **Siempre** que asignes una tarea nueva a un agente
- ✅ Al inicio de cada tarea (no dar múltiples tareas al mismo tiempo)
- ✅ Después de aprobar la tarea anterior
- ✅ Cuando el brief puede estar desactualizado vs estado real del proyecto

### Cómo llenar el template:

1. **[NOMBRE_AGENTE]**: Backend Engineer, DB Engineer, Frontend Developer, etc.
2. **[CONTEXTO_BREVE]**: "MS-101 completado, estructura DB disponible"
3. **[ID_TAREA]**: MS-101, MS-BE-001, etc.
4. **[NOMBRE_SECCION]**: "ARCHIVOS A REVISAR", "ARCHIVOS DB A REVISAR", etc.
5. **[TITULO_PUNTO_CRITICO]**: Punto más importante específico de la tarea
6. **[N] archivos**: Número exacto de archivos a leer
7. **[RUTA_ARCHIVO_X]**: Ruta completa y propósito claro
8. **[LENGUAJE]**: typescript, python, sql, bash, etc.
9. **[METODO]**: POST, GET, PUT, DELETE, PATCH
10. **[ESCENARIO_X]**: Casos de prueba específicos
11. **[CRITERIO_X]**: Lista de checkboxes funcionales del brief
12. **[tipo]**: feat, fix, docs, refactor, test, chore
13. **TrackableItems**: Verificar en VTT si hay RFs/ADRs a crear o vincular

### Secciones opcionales (eliminar si no aplica):
- **🔴 Punto crítico específico**: Solo si hay algo MUY importante que destacar
- **🔌 API/Recursos**: Solo para Backend/Frontend

### Secciones obligatorias (NUNCA eliminar):
- **📝 ENTREGABLES OBLIGATORIOS**: Tabla completa con #6-9 V4
- **✅ CRITERIOS DE ACEPTACIÓN**: Con criteriaId reales de VTT
- **📊 DEVLOG ENTRIES**: Tabla de categoryCode y cuándo registrar
- **🔗 TRACKABLE ITEMS**: Especificar o poner N/A
- **🗂️ CODE LOGIC**: Con lista de archivos específicos
- **📝 WORKFLOW**: 13 pasos completos incluyendo review gate
- **✅ CHECKLIST DE ENTREGA**: Con sección VTT V4 completa

### Checklist LL-005 para completar el template:
```
Sección: API/RECURSOS DISPONIBLES
  [ ] Abrir routes/ → identificar el router del módulo
  [ ] Leer decoradores/routes → copiar paths exactos al template
  [ ] Abrir schemas o types → copiar campos reales de response y body
  [ ] Marcar YA FUNCIONAN los que existen, EN DESARROLLO los pendientes

Sección: CRITERIOS DE ACEPTACIÓN
  [ ] Verificar CAs ya registrados en VTT: GET /api/tasks/:id/criteria
  [ ] Si no existen → crearlos: POST /api/projects/:id/acceptance-criteria
  [ ] Listar en el assignment con criteriaId real (UUID)

Sección: TRACKABLE ITEMS
  [ ] Identificar si la tarea crea/implementa RF, ADR, User Story, KPI
  [ ] Si hay → especificar typeCode y si crear o vincular

Sección: ARCHIVOS A REVISAR
  [ ] Listar cada archivo relevante con ruta y propósito
  [ ] NO listar el handoff del PM — ese ya fue leído en Fase 1
```

### Diferencia Brief vs Assignment:

| Aspecto | Brief | Assignment (este template) |
|---------|-------|---------------------------|
| Propósito | Diseño original | Estado actual al asignar |
| Estado | Inmutable | Snapshot del momento |
| Contenido | Especificación ideal | Realidad + Especificación |
| Fecha | Creación de tarea | Fecha de asignación |
| Endpoints | Los que se diseñaron | Los que YA funcionan |
| Archivos | Los que se crearán | Los que YA existen |
| Ubicación | `knowledge/agent-tasks/briefs/` | `knowledge/agent-tasks/assignments/` |

---

**Versión:** 3.0
**Última actualización:** 2026-05-01
**Cambios v3.0:** Integración completa Modelo Dinámico V4 — devlog entries obligatorios (#6), review gate (#9), CAs con fulfill + criteriaId en tabla, TrackableItems (#8), workflow actualizado a 13 pasos, checklist VTT V4, referencia a SKL-REPORT-01. Mantenido contenido completo de v2.1.
