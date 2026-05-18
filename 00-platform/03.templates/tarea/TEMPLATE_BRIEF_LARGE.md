# BRIEF: [TASK_ID] - [Nombre de la Tarea]

**Tarea**: [TASK_ID]
**Título**: [Título completo]
**Repositorio**: [nombre-repo]
**Asignado a**: [Agente]
**Prioridad**: [P0/P1/P2/P3]
**Estimación**: [X horas]
**Complejidad**: [low | medium | high | critical]
**Categoría**: [feature | bug | improvement | documentation | refactor | test | infrastructure]
**Inicio planificado**: YYYY-MM-DD (para Gantt — opcional si no hay plan activo)
**Fin planificado**: YYYY-MM-DD (para Gantt — opcional si no hay plan activo)
**Fecha límite**: YYYY-MM-DD
**Creado por**: [Coordinador]
**Fecha de creación**: YYYY-MM-DD

---

## 📋 Tabla de Contenidos

1. [Objetivo](#objetivo)
2. [Contexto](#contexto)
3. [Campos del Sistema](#campos-del-sistema)
4. [Requisitos Técnicos](#requisitos-técnicos)
5. [Dependencias](#dependencias)
6. [Archivos a Crear/Modificar](#archivos-a-crearmodificar)
7. [Criterios de Éxito](#criterios-de-éxito)
8. [Cómo Probar](#cómo-probar)
9. [Referencias](#referencias)
10. [Notas Importantes](#notas-importantes)

---

## 🗄️ Campos del Sistema

Valores a usar al crear la tarea via API (`POST /api/phases/{phaseId}/tasks`):

| Campo API | Valor | Notas |
|-----------|-------|-------|
| `title` | [TASK_ID]: [Título completo] | |
| `estimatedHours` | [X] | Suma de la tabla de estimación detallada |
| `complexity` | [low \| medium \| high \| critical] | **Obligatorio** |
| `category` | [feature \| bug \| improvement \| documentation \| refactor \| test \| infrastructure] | **Obligatorio** |
| `priorityId` | UUID de prioridad | Ver UUIDs en PROCESO_ASIGNACION_TAREAS.md |
| `plannedStartDate` | YYYY-MM-DDT00:00:00Z | Solo si hay plan Gantt activo |
| `plannedEndDate` | YYYY-MM-DDT00:00:00Z | Solo si hay plan Gantt activo |
| `assignedToId` | UUID del agente | Ver UUIDs en PROCESO_ASIGNACION_TAREAS.md |

> `complexity` y `category` son **obligatorios** — la API rechaza la creación sin ellos.
> `plannedStartDate/EndDate` son opcionales; afectan el Gantt y la ruta crítica si hay plan activo.

---

## 🎯 Objetivo

[Descripción clara en 2-3 líneas de QUÉ hay que hacer y POR QUÉ]

**Resultado esperado**:  
[Qué debe funcionar al terminar esta tarea]

---

## 🔍 Contexto

### Problema que Resuelve

[Explicar el problema actual o la necesidad que cubre esta tarea]

### Situación Actual

[Describir el estado actual del código/proyecto relacionado con esta tarea]

### Situación Deseada

[Describir cómo debe quedar después de implementar esta tarea]

---

## 🔧 Requisitos Técnicos

### Stack Tecnológico

**Lenguaje**: [JavaScript/TypeScript/etc]  
**Framework**: [Express/React/etc]  
**Librerías a usar**:
- `nombre-libreria@version` - Para qué se usa

### Instalación de Dependencias

```bash
npm install libreria-1 libreria-2
```

### Variables de Entorno

```bash
# Agregar a .env
VARIABLE_NAME=value
OTRA_VARIABLE=value
```

---

## 📦 Dependencias

### Tareas que Deben Estar Completadas Primero

- [ ] [TASK_ID] - [Nombre] - Estado: [estado actual]

**Por qué**: [Explicar por qué necesitas que estén completadas]

### Archivos/Módulos Existentes que Usarás

- `ruta/al/archivo.js` - [Qué funcionalidad usarás de aquí]
- `otro/archivo.js` - [Qué funcionalidad usarás]

---

## 📂 Archivos a Crear/Modificar

### Archivos Nuevos

**1. `src/path/to/newfile.js`**

**Propósito**: [Qué hace este archivo]

**Estructura esperada**:

```javascript
// Pseudocódigo / estructura básica

const dependency = require('./dependency');

async function mainFunction(param1, param2) {
  // 1. Validar inputs
  // 2. Hacer X
  // 3. Retornar Y
}

module.exports = { mainFunction };
```

**Funciones principales**:
- `functionName(params)` - [Qué hace]
- `anotherFunction(params)` - [Qué hace]

---

**2. `src/path/to/anotherfile.js`**

[Repetir estructura anterior]

---

### Archivos a Modificar

**1. `src/existing/file.js`**

**Qué cambiar**:
- Línea X: Agregar import de nuevo módulo
- Línea Y: Registrar nueva ruta
- Función Z: Modificar para incluir nueva lógica

**Código específico a agregar**:

```javascript
// Agregar en línea 15
const newModule = require('./path/to/newmodule');

// Agregar en línea 45
app.use('/api/new-route', newModule);
```

---

## ✅ Criterios de Éxito

### Funcionales

- [ ] [Criterio funcional 1 - debe ser verificable]
- [ ] [Criterio funcional 2]
- [ ] [Criterio funcional 3]

**Ejemplo**:
- [ ] Endpoint POST /api/webhooks/clerk retorna 200 cuando firma es válida
- [ ] Evento user.created crea usuario en tabla `users`
- [ ] Usuario creado tiene clerk_id, email y created_at

### No Funcionales

- [ ] Código sigue convenciones del proyecto
- [ ] Sin console.log de debug
- [ ] Manejo de errores con try-catch
- [ ] Variables de entorno documentadas

### Documentación

- [ ] Development Log completo
- [ ] Code Logic creado para cada archivo
- [ ] Comentarios en código complejo
- [ ] README actualizado (si aplica)

---

## 🧪 Cómo Probar

### Setup Inicial

```bash
# Comandos para preparar el ambiente
npm install
# ... otros comandos
```

### Prueba Manual 1: [Nombre del escenario]

**Objetivo**: [Qué estamos probando]

**Pasos**:
1. [Paso 1 detallado]
2. [Paso 2 detallado]
3. [Paso 3 detallado]

**Resultado esperado**:
[Qué debe pasar]

**Comando para ejecutar**:
```bash
curl -X POST http://localhost:3001/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"data": "value"}'
```

**Output esperado**:
```json
{
  "success": true,
  "data": {...}
}
```

---

### Prueba Manual 2: [Caso de error]

[Repetir estructura anterior]

---

### Prueba en Base de Datos

**Verificar que se creó el registro**:
```sql
SELECT * FROM table_name WHERE condition;
```

**Resultado esperado**:
```
id | clerk_id | email | created_at
...
```

---

### Tests Automatizados (si aplica)

```bash
npm test
```

**Tests que deben pasar**:
- [ ] test-name-1
- [ ] test-name-2

---

## 📚 Referencias

### Documentación Interna

- `/mnt/project/01_Plan_Autenticacion_Seguridad_Clerk.md` - Líneas X-Y
- `/docs/context/PROJECT_CONTEXT.md` - Sección de autenticación

### Documentación Externa

- [Clerk Webhooks](https://clerk.com/docs/integrations/webhooks) - Documentación oficial
- [Svix Library](https://github.com/svix/svix-webhooks) - Validación de firma
- [Express Raw Body](https://expressjs.com/en/api.html#express.raw) - Para webhooks

### Código de Referencia

- `src/existing/similar-file.js` - Tiene estructura similar
- Otro proyecto que hace algo parecido

---

## 📝 Notas Importantes

### Decisiones de Diseño

**1. ¿Por qué usar Librería X en lugar de Y?**  
[Explicación de la decisión]

**2. ¿Por qué estructurar el código de esta manera?**  
[Explicación de la decisión]

### Cosas a Evitar

- ❌ No usar console.log en producción - usar logger
- ❌ No hardcodear secrets - usar .env
- ❌ No hacer queries sin Prisma - usar ORM

### Tips para el Agente

- 💡 Este archivo es crítico para la seguridad
- 💡 Probar con múltiples escenarios de error
- 💡 La validación de firma es esencial

### Problemas Conocidos o Limitaciones

[Si hay algo que el agente debe saber de antemano]

---

## 🔄 Dependencias de Esta Tarea

### Tareas que se Desbloquearán al Completar Esta

- [TASK_ID] - [Nombre] - [Por qué depende de esta]
- [TASK_ID] - [Nombre] - [Por qué depende de esta]

### Impacto de Esta Tarea

[Explicar qué otras partes del sistema se ven afectadas]

---

## 📞 Contacto

**PM/Coordinador**: Martin Rivas (martin.rivas@prompt-ai.studio)  
**Preguntas**: Crear issue en TASK_TRACKING.md o comentar directamente

---

**Última actualización**: YYYY-MM-DD  
**Versión**: 1.0  
**Estado**: [Draft / Ready / In Use]
