# Reglas para Agentes - Virtual Teams Tracking

## Versión: 1.2
## Fecha: 2026-02-02
## Proyecto: Prompt AI Studio / Virtual Teams Tracking / DesignMine

---

## REGLAS OBLIGATORIAS

Todo agente DEBE seguir estas reglas sin excepción.

---

## 1. Antes de Empezar Cualquier Tarea

### SIEMPRE leer primero:
1. **Brief de la tarea** — `/briefs/[TASK_ID]_[nombre].md`
2. **TASK_TRACKING.md** — Verificar estado y dependencias

### Verificar que:
- La tarea está en estado 🟡 pending (NO bloqueada 🔴)
- Todas las dependencias están en estado 🟢 approved
- Tienes clara la ubicación de archivos a crear/modificar

### NUNCA:
- Empezar una tarea en estado 🔴 blocked
- Asumir contexto que no esté en los documentos
- Empezar a codificar sin leer el brief completo
- Modificar archivos fuera del alcance de la tarea

---

## 2. Al Iniciar una Tarea

### Cambiar estado en TASK_TRACKING.md:

```markdown
**Estado**: 🔵 in_progress
```

### Agregar registro en Historial de Cambios:

```markdown
| YYYY-MM-DD HH:MM | 🔵 in_progress | Tarea iniciada | [Tu nombre] |
```

### Crear rama de Git:

```bash
git checkout -b feature/[TASK_ID]
# Ejemplo: git checkout -b feature/F1-AUTH-01
```

---

## 3. Entregables por Cada Tarea

### TODA tarea debe entregar CUATRO cosas (+ Swagger si hay endpoints):

| # | Entregable | Ubicación | Obligatorio |
|---|------------|-----------|-------------|
| 1 | **Código** | `/src/...` | ✅ Sí |
| 2 | **Development Log** | `/knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[descripcion].md` | ✅ Sí |
| 3 | **Code Logic** | `/knowledge/code-logic/[espejo-de-src]/[archivo].LOGIC.md` | ✅ Sí |
| 4 | **Commit & Push** | GitHub con mensaje descriptivo | ✅ Sí |
| 5 | **Swagger Docs** | JSDoc inline + visible en `/api-docs` | ✅ Si hay endpoints |

### Si falta alguno → ENTREGA INCOMPLETA

---

## 4. Reglas de Code Logic

### REGLA FUNDAMENTAL: UN archivo de lógica por archivo de código

```
/src/controllers/webhookController.js
              ↓
/knowledge/code-logic/controllers/webhookController.LOGIC.md
```

### Cuando CREAS un archivo nuevo:
1. Crear el archivo de código en `/src/...`
2. Crear el archivo `.LOGIC.md` en ubicación espejo
3. Usar template: `/_project-management/templates/TEMPLATE_CODE_LOGIC.md`
4. Documentar: propósito, dependencias, flujo

### Cuando MODIFICAS un archivo existente:
1. Modificar código en `/src/...`
2. **BUSCAR** si ya existe el archivo `.LOGIC.md`
3. Si existe: **ACTUALIZAR** (no crear uno nuevo)
4. Agregar entrada en "Historial de Cambios"
5. Si no existe: **CREAR** el archivo `.LOGIC.md`

### Contenido de `.LOGIC.md`:
- ✅ QUÉ hace el archivo
- ✅ CÓMO fluye la lógica
- ✅ Dependencias importantes
- ✅ Decisiones de diseño
- ❌ NO incluir código fuente (solo descripciones)

### NUNCA:
- Crear un segundo archivo de lógica para el mismo código
- Dejar un archivo de código sin su archivo de lógica
- Incluir código fuente en el archivo de lógica

---

## 5. Reglas de Development Log

### Nombrado:
```
YYYY-MM-DD_[TASK_ID]_[descripcion-corta].md
```

Ejemplos:
- `2026-01-15_F1-AUTH-01_webhook-clerk.md`
- `2026-01-16_F1-AUTH-02_middleware-auth.md`

### Contenido obligatorio:
- Información general (fecha, tarea, repo)
- Resumen de qué se hizo
- Archivos creados/modificados
- Decisiones técnicas tomadas
- Dependencias agregadas
- Cómo probar/validar
- Pendientes (si los hay)

### Usar template:
`/templates/TEMPLATE_DEVELOPMENT_LOG.md`

---

## 6. Reglas de Código

### Estructura:
- Seguir la estructura existente del proyecto
- No crear carpetas nuevas sin autorización del Coordinador
- Mantener nomenclatura consistente con el proyecto

### Calidad:
- Código funcional (debe compilar/ejecutar)
- Sin `console.log` de debug (solo logs informativos)
- Sin código comentado innecesario
- Sin TODOs sin explicación
- Manejo de errores con try-catch

### Dependencias:
- Reportar TODA dependencia nueva en el Development Log
- No instalar dependencias sin mencionarlo
- Usar versiones específicas (no `latest`)

---

## 6.5 Workflow Completo (Actualizado v1.2)

### 📝 WORKFLOW DE 12 PASOS

**Paso 0: Crear rama de Git** ⚠️ NO OLVIDAR
```bash
git checkout -b feature/[TASK_ID]
```

**Paso 1: Cambiar estado** en TASK_TRACKING.md a 🔵 in_progress

**Paso 2: Leer brief completo** (todas las líneas del brief)

**Paso 3: Leer archivos de referencia** listados en el assignment o brief

**Paso 4: Verificar prerequisitos** (servicios corriendo, BD accesible, dependencias)

**Paso 5: Implementar archivos** siguiendo especificación del brief

**Paso 6: Crear archivos .LOGIC.md** (uno por cada archivo de código creado/modificado)

**Paso 7: Probar que funciona** localmente con los comandos del brief

**Paso 8: Testing manual** ejecutar todos los escenarios del brief

**Paso 9: Crear Development Log** completo con decisiones técnicas

**Paso 10: Commit y push** con formato:
```bash
git add .
git commit -m "[tipo]([repo]) [TASK_ID]: Descripción breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Refs: #[TASK_ID]"

git push origin feature/[TASK_ID]
```

**Paso 11: Crear PR** con gh CLI:
```bash
gh pr create \
  --title "[[TASK_ID]] Título descriptivo" \
  --body "Descripción de cambios. Ver devlog para detalles." \
  --base main
```

**Paso 12: Cambiar estado** a 🟣 completed en TASK_TRACKING.md y reportar con formato

**⚠️ IMPORTANTE**: Seguir TODOS los pasos en orden. NO saltarte ninguno.

---

## 7. Documentación de APIs con Swagger

### 🚨 REGLA OBLIGATORIA

> Todo endpoint que se cree DEBE incluir su documentación Swagger inline.
> Sin documentación Swagger = TAREA INCOMPLETA (si hay endpoints)

### ¿Por qué es obligatorio?

- ✅ Documentar después es caótico (lección aprendida)
- ✅ Inline es 10x más fácil que documentar después
- ✅ Docs siempre actualizadas con el código
- ✅ Frontend sabe qué esperar sin preguntar
- ✅ Testing más fácil con "Try it out" en Swagger UI

### Setup Inicial (Solo en F1-AUTH-01)

```bash
npm install swagger-jsdoc swagger-ui-express
```

Crear `src/config/swagger.js` y modificar `src/app.js` según el brief.

**Resultado**: `http://localhost:3001/api-docs` funcionando

### En Cada Endpoint (Todas las tareas con APIs)

Agregar comentario JSDoc **ANTES** del route:

```javascript
/**
 * @swagger
 * /ruta:
 *   post:
 *     summary: Descripción breve
 *     description: Descripción detallada
 *     tags:
 *       - NombreModulo
 *     security: []  # Si no requiere auth
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: Éxito
 *       400:
 *         description: Error de validación
 *       401:
 *         description: No autenticado
 *       403:
 *         description: Sin permisos
 *       500:
 *         description: Error interno
 */
router.post('/ruta', handler);
```

### Checklist de Swagger (si la tarea crea endpoints)

- [ ] Comentarios JSDoc agregados al route
- [ ] Endpoint visible en `/api-docs`
- [ ] Request body documentado (si aplica)
- [ ] Todas las responses documentadas
- [ ] "Try it out" funciona en Swagger UI
- [ ] Ejemplos incluidos cuando sea útil

### Cómo Verificar

1. Levantar servidor: `npm run dev`
2. Abrir: `http://localhost:3001/api-docs`
3. Verificar que el endpoint aparece
4. Probar con "Try it out"

---

## 8. Convenciones de Commits

### Formato obligatorio (Actualizado v1.2):

```
[tipo](repo) [TASK_ID]: Descripción breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Refs: #TASK_ID
```

⚠️ **Co-Authored-By es OBLIGATORIO** en todos los commits

### Tipos de commit:
- `feat` — Nueva funcionalidad
- `fix` — Corrección de bug
- `docs` — Solo documentación
- `refactor` — Refactorización sin cambios funcionales
- `test` — Agregar/modificar tests
- `chore` — Mantenimiento (deps, config)

### Ejemplo:

```bash
git commit -m "feat(core-engine) [F1-AUTH-01]: Implementar webhook de Clerk

- Crear webhookController.js
- Agregar validación de firma con svix
- Handlers para user.created, updated, deleted

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Refs: #F1-AUTH-01"
```
### configuracion del repósitorio

el usuario y cuenta apra realizar la actualizacion del repositorio son:
**Coordinador**: Martin Rivas  
**Email**: martin.rivas@prompt-ai.studio  

Realizar la configuracion del repositorio con estos datos

---

## 9. Al Completar una Tarea

### Checklist antes de entregar (Actualizado v1.2):

#### Funcionalidad:
- [ ] ¿El código compila/ejecuta sin errores?
- [ ] ¿Probé que funciona localmente?
- [ ] ¿Todas las pruebas del brief pasaron?

#### Calidad de Código:
- [ ] ¿Seguí la arquitectura existente?
- [ ] ¿Los nombres son consistentes con el proyecto?
- [ ] ¿No hay console.log de debug?
- [ ] ¿Manejo de errores con try-catch?

#### Documentación:
- [ ] ¿Creé/actualicé TODOS los archivos `.LOGIC.md`? (uno por archivo de código)
- [ ] ¿El Development Log está completo?
- [ ] ¿Expliqué las decisiones técnicas en el devlog?
- [ ] ¿Swagger docs creadas? (si hay endpoints)
- [ ] ¿Probé en /api-docs que funciona "Try it out"? (si hay endpoints)

#### Git:
- [ ] ¿Rama creada: `feature/[TASK_ID]`?
- [ ] ¿El commit tiene mensaje descriptivo?
- [ ] ¿Commit incluye Co-Authored-By: Claude Sonnet 4.5?
- [ ] ¿Hice push a GitHub?
- [ ] ¿Creé PR con `gh pr create`?
- [ ] ¿PR tiene título descriptivo?

#### Estado:
- [ ] ¿Cambié estado a 🟣 completed en TASK_TRACKING.md?
- [ ] ¿Agregué entry en Historial de Cambios?

⚠️ **Si falta UNO de estos checks → NO REPORTAR COMO COMPLETADA**

### Cambiar estado en TASK_TRACKING.md:

```markdown
**Estado**: 🟣 completed
```

### Agregar registro en Historial:

```markdown
| YYYY-MM-DD HH:MM | 🟣 completed | Tarea completada, pendiente revisión | [Tu nombre] |
```

### Notificar al Coordinador con formato:

```markdown
## Entrega: [TASK_ID] - [Nombre de la tarea]

### Código:
- `src/...` - [descripción]
- `src/...` - [descripción]

### Development Log:
`knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[nombre].md`

### Code Logic:
- `knowledge/code-logic/.../[archivo].LOGIC.md`

### Commit:
[tipo](repo) [TASK_ID]: Descripción
SHA: [hash del commit]

### Cómo probar:
[comandos o pasos para validar]
```

---

## 10. Manejo de Problemas

### Si encuentras un problema:

1. **Describir** el problema claramente
2. **Explicar** qué intentaste
3. **Proponer** soluciones alternativas
4. **Cambiar estado** a 🟠 on_hold si es bloqueante
5. **Notificar** al Coordinador inmediatamente

### Formato para reportar problema:

```markdown
### 🟠 PROBLEMA ENCONTRADO

**Tarea**: [TASK_ID]
**Descripción**: [Qué pasó]
**Intenté**: [Qué soluciones probaste]
**Opciones**:
1. [Opción A]
2. [Opción B]

**Acción necesaria**: [Qué necesitas del Coordinador]
```

### NUNCA:
- Asumir una solución sin consultar
- Dejar el problema sin reportar
- Modificar código fuera del alcance para "arreglar" algo
- Continuar si algo crítico no funciona

---

## 11. Lo que NO Debes Hacer

❌ Empezar tarea en estado 🔴 blocked  
❌ Modificar archivos fuera del alcance de la tarea  
❌ Modificar .env o docker-compose sin instrucción explícita  
❌ Cambiar la estructura de carpetas del proyecto  
❌ Instalar dependencias sin reportar  
❌ Crear archivos de prueba y dejarlos  
❌ Duplicar código existente  
❌ Duplicar archivos de lógica  
❌ Incluir código en los archivos de lógica  
❌ Saltarte la documentación  
❌ Dejar console.log de debug  
❌ Hacer commit directo a main (usar ramas)  
❌ Crear endpoints sin documentación Swagger  

---

## 12. Sistema de Estados (Referencia)

| Estado | Icono | Significado |
|--------|-------|-------------|
| pending | 🟡 | Lista para empezar |
| blocked | 🔴 | Esperando dependencias |
| on_hold | 🟠 | Pausada por problema externo |
| in_progress | 🔵 | Trabajando activamente |
| completed | 🟣 | Terminada, pendiente revisión |
| under_review | 🟤 | Coordinador revisando |
| approved | 🟢 | Aprobada y cerrada |
| rejected | 🔴 | Necesita correcciones |
| cancelled | ⚫ | Cancelada |

---

## 13. Estructura de Carpetas (Referencia)

```
[repositorio]/
├── src/                          ← CÓDIGO
├── docs/                         ← DOCS DE ENTRADA (se sube a git)
│   └── context/
│       ├── PROJECT_CONTEXT.md
│       └── ARCHITECTURE.md
├── knowledge/                    ← DOCS DE SALIDA (NO se sube a git)
│   ├── development-log/          ← Un log por tarea
│   └── code-logic/               ← Espejo de /src
└── prisma/                       ← Schema de BD (si aplica)
```

---

## 14. Recordatorio Final

```
CÓDIGO SIN DOCUMENTACIÓN = ENTREGA INCOMPLETA

Por cada archivo de código:
  → UN archivo de lógica
  → EN la carpeta espejo correcta
  → ACTUALIZADO si ya existía

Por cada endpoint:
  → Comentario JSDoc con Swagger
  → Visible en /api-docs
  → "Try it out" funciona

Por cada tarea:
  → Development Log completo
  → Code Logic por cada archivo
  → Swagger docs (si hay endpoints)
  → Commit bien formateado
  → Push a GitHub

## proceso apra el agregar a git
  Los agentes pueden usar este comando para crear PRs:


# Crear un nuevo branch
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y commit
git add .
git commit -m "descripción de cambios"

# Push del branch
git push origin feature/nueva-funcionalidad

# Crear el PR automáticamente
gh pr create \
  --title "Título del PR" \
  --body "Descripción de los cambios realizados" \
  --base main
```

---

## 15. REGLAS CRÍTICAS DE WORKFLOW (OBLIGATORIAS)

### 🔴 CRÍTICO: Estas reglas son ABSOLUTAS y NO se pueden violar

---

### 15.1. Branch Management - Evitar Pérdida de Código

#### 🚨 PROBLEMA QUE RESUELVE:
Cuando los agentes se quedan mucho tiempo en branches y hacen merge tarde, se pierden modificaciones de otros PRs por conflictos mal resueltos.

#### ✅ REGLAS OBLIGATORIAS:

**1. Crear branch al inicio de tarea:**
```bash
git checkout -b feature/[TASK_ID]
```

**2. Rebase frecuente con main (ANTES de crear PR):**
```bash
git fetch origin
git rebase origin/main
# Resolver conflictos si los hay
git push origin feature/[TASK_ID] --force-with-lease
```

**3. Tiempo máximo en branch: 24 horas**
- Si tu tarea toma más de 24h, hacer rebase diario con main
- NUNCA esperar días para crear el PR

**4. Crear PR INMEDIATAMENTE después de completar:**
```bash
gh pr create --title "[TASK_ID] Descripción" --body "Ver devlog" --base main
```

**5. Merge rápido (max 2 horas después de approval):**
- Una vez aprobado el PR, hacer merge inmediato
- No dejar PRs aprobados sin merge

**6. ANTES de hacer merge, validar que NO se perdió código:**
- Revisar Files Changed en GitHub
- Verificar que solo se modificaron archivos de TU tarea
- Si ves archivos que no tocaste, PARAR y notificar al Coordinador

#### ⚠️ NUNCA:
- ❌ Quedarte en un branch más de 24h sin rebase
- ❌ Hacer merge sin revisar Files Changed
- ❌ Forzar un merge que tiene conflictos sin entender
- ❌ Salir del branch sin hacer merge del PR

---

### 15.2. NUNCA Commit Directo a Main

#### 🚨 REGLA ABSOLUTA:

```
PROHIBIDO HACER COMMIT DIRECTO A MAIN
```

#### ✅ PROCESO CORRECTO:

**Siempre seguir este flujo:**
1. Crear branch: `git checkout -b feature/[TASK_ID]`
2. Hacer commits en el branch
3. Push del branch: `git push origin feature/[TASK_ID]`
4. Crear PR con `gh pr create`
5. Esperar approval del Coordinador
6. Coordinador hace merge

#### ⚠️ SI DETECTAS QUE ESTÁS EN MAIN:

```bash
# Verificar en qué branch estás
git branch

# Si estás en main y no has hecho commit:
git checkout -b feature/[TASK_ID]

# Si ya hiciste commit en main (EMERGENCIA):
# NO HACER PUSH - notificar inmediatamente al Coordinador
```

#### 🚨 CONSECUENCIAS DE VIOLAR ESTA REGLA:
- Se rompe el flujo de revisión
- Se pierde historial de cambios
- Branch protection se desactiva
- Código sin revisar entra a producción

---

### 15.3. NUNCA Mockear Datos - Crear ISSUE en su lugar

#### 🚨 PROBLEMA QUE RESUELVE:
Datos mockeados causan bugs en producción, inconsistencias en testing, y trabajo extra para limpiar después.

#### ✅ REGLA ABSOLUTA:

```
SI DETECTAS QUE FALTAN DATOS REALES
  → NUNCA crear/mockear datos
  → CREAR un ISSUE
  → COMPLETAR lo posible de la tarea
  → DEJAR tarea en 🟠 on_hold
  → ESPERAR a que se resuelva el ISSUE
  → REGRESAR a completar la implementación
```

#### 📋 PROCESO DETALLADO:

**Paso 1: Detectar datos faltantes**

Ejemplos de datos faltantes:
- Catálogos vacíos (status, prioridades, roles)
- Tablas sin seed data
- Configuraciones incompletas
- Variables de entorno sin definir
- Archivos de prueba inexistentes

**Paso 2: Crear ISSUE usando template**

Ver sección 15.4 para template completo.

Ubicación: `_project-management/issues/ISS-[NUM]_Falta_[Descripcion].md`

**Paso 3: Completar implementación hasta donde sea posible**

```markdown
// Ejemplo en código:
// TODO: Completar cuando se resuelva ISS-042 (catálogo de prioridades)
const priorities = await getPriorities();
if (priorities.length === 0) {
  throw new Error('No hay prioridades configuradas. Ver ISS-042');
}
```

**Paso 4: Cambiar estado a 🟠 on_hold**

En TASK_TRACKING.md:
```markdown
**Estado**: 🟠 on_hold

**Bloqueado por**: ISS-042 - Falta catálogo de prioridades

**Progreso**: 80% completado, solo falta integración con catálogos
```

**Paso 5: Notificar al Coordinador**

```markdown
### 🟠 TAREA EN HOLD: [TASK_ID]

**Razón**: Faltan datos reales para completar

**ISSUE creado**: ISS-[NUM] - [Descripción]

**Implementado hasta ahora**:
- ✅ Endpoints creados
- ✅ Validaciones implementadas
- ✅ Lógica de negocio completa
- ⏸️ FALTA: Integración con catálogo (sin datos)

**Para completar necesito**:
- Catálogo de [X] con al menos [Y] registros

**Archivos listos**:
- src/...
- Documentación completa

**Tiempo estimado para terminar**: 30 min después de tener datos
```

**Paso 6: Cuando el ISSUE se resuelva**

```bash
# Regresar al branch
git checkout feature/[TASK_ID]

# Actualizar con main (por si pasó tiempo)
git rebase origin/main

# Completar la implementación
# ... hacer cambios ...

# Commit y push
git add .
git commit -m "feat: Complete [TASK_ID] after ISS-[NUM] resolved"
git push origin feature/[TASK_ID]

# Cambiar estado a 🟣 completed
```

#### ⚠️ NUNCA:
- ❌ Crear datos ficticios o mock data
- ❌ Hardcodear valores temporales
- ❌ "Inventar" catálogos o configuraciones
- ❌ Usar datos de ejemplo en vez de esperar datos reales
- ❌ Continuar sin reportar que faltan datos

---

### 15.4. Template ISSUE - Falta Catálogo/Datos

Cuando detectes datos faltantes, crear este archivo:

**Ubicación**: `_project-management/issues/ISS-[NUM]_Falta_[Nombre].md`

**Contenido**:

```markdown
# ISSUE: ISS-[NUM] - Falta [Catálogo/Datos]

## Información General

**Fecha creación**: YYYY-MM-DD
**Reportado por**: [Tu nombre de agente]
**Tarea bloqueada**: [TASK_ID]
**Prioridad**: 🔴 Alta / 🟡 Media / 🟢 Baja
**Estado**: 🟡 pending

---

## Descripción del Problema

[Explicar qué datos faltan y por qué son necesarios]

**Datos faltantes**:
- [Tabla/Catálogo/Archivo] - [Qué debe contener]

**Impacto**:
- [TASK_ID] no se puede completar sin estos datos
- [Otros impactos si los hay]

---

## Datos Requeridos

### Tabla/Catálogo: [Nombre]

**Ubicación esperada**:
- Base de datos: `[tabla]`
- O archivo: `[ruta]`

**Campos requeridos**:
| Campo | Tipo | Ejemplo | Obligatorio |
|-------|------|---------|-------------|
| id | UUID | ... | Sí |
| name | String | ... | Sí |
| ... | ... | ... | ... |

**Registros mínimos necesarios**:
- [ ] [Registro 1 descripción]
- [ ] [Registro 2 descripción]
- [ ] ...

**Ejemplo de datos esperados**:
```json
[
  {
    "id": "uuid-1",
    "name": "...",
    "..."
  }
]
```

---

## Tareas Bloqueadas

- [ ] [TASK_ID] - [Nombre] (🟠 on_hold)

---

## Solución Propuesta

**Opción 1**: [Descripción de cómo cargar/crear los datos]

**Opción 2**: [Si hay alternativa]

---

## Checklist para Resolver

- [ ] Crear/insertar datos en [ubicación]
- [ ] Verificar que datos son accesibles vía [API/query]
- [ ] Notificar a [agente] para que complete [TASK_ID]
- [ ] Actualizar estado de ISSUE a 🟢 resolved

---

## Notas Adicionales

[Cualquier información extra relevante]

---

**Última actualización**: YYYY-MM-DD
```

---

### 15.5. Checklist - ¿Qué Hacer Cuando Faltan Datos?

```
[ ] 1. DETENER implementación cuando detectes datos faltantes
[ ] 2. CREAR ISSUE usando template 15.4
[ ] 3. COMPLETAR todo lo posible de la tarea
[ ] 4. DOCUMENTAR qué falta en el devlog
[ ] 5. CAMBIAR estado a 🟠 on_hold en TASK_TRACKING.md
[ ] 6. NOTIFICAR Coordinador con formato de sección 15.3
[ ] 7. ESPERAR resolución del ISSUE
[ ] 8. REGRESAR cuando datos estén listos
[ ] 9. COMPLETAR tarea y cambiar a 🟣 completed
```

---

## 16. Contacto

**Coordinador**: Martin Rivas
**Email**: martin.rivas@prompt-ai.studio
**Preguntas**: Comentar en TASK_TRACKING.md o mensaje directo

---

**Última actualización**: 2026-02-03
**Versión**: 1.3 (Reglas críticas de workflow: branch management, no commit to main, no mock data)
