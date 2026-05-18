# 📚 Guía de Uso de Templates - Sistema de Tracking Virtual Teams

**Fecha:** 2025-01-19  
**Versión:** 1.0  
**Proyecto:** Virtual Teams Tracking

---

## 📋 Templates Disponibles

Este proyecto incluye 6 templates principales para estandarizar la documentación:

1. **TEMPLATE_BRIEF.md** - Para especificar tareas nuevas
2. **TEMPLATE_HANDOFF.md** - Para entregar tareas a agentes
3. **TEMPLATE_DEVLOG.md** - Para documentar trabajo completado
4. **TEMPLATE_CODE_LOGIC.md** - Para explicar arquitectura y flujos
5. **TEMPLATE_ISSUE.md** - Para reportar problemas
6. **TEMPLATE_DECISION.md** - Para documentar decisiones importantes

---

## 🎯 Cuándo Usar Cada Template

### 1. TEMPLATE_BRIEF.md

**Úsalo cuando:** Necesitas crear una nueva tarea

**Quién lo usa:** Product Manager (Martin) o PM Coordinator (Claude)

**Ubicación final:** `_project-management/briefs/BRIEF_TASK-XXX_[Nombre].md`

**Ejemplo:**
```
_project-management/briefs/BRIEF_TASK-008_Script_Update_Tasks.md
```

**Cuándo crearlo:**
- Al inicio de cada sprint
- Cuando surge una nueva necesidad
- Para dividir tareas grandes en subtareas

---

### 2. TEMPLATE_HANDOFF.md

**Úsalo cuando:** Necesitas asignar una tarea a un agente específico

**Quién lo usa:** Product Manager (Martin) o PM Coordinator (Claude)

**Ubicación final:** `knowledge/handoffs/HANDOFF_[ROL]_TASK-XXX.md`

**Ejemplo:**
```
knowledge/handoffs/HANDOFF_BACKEND-API_TASK-008.md
```

**Cuándo crearlo:**
- Después de aprobar un BRIEF
- Antes de ejecutar la tarea con Claude Code
- Cuando necesitas dar instrucciones paso a paso

**Relación con BRIEF:**
- El HANDOFF referencia al BRIEF
- BRIEF = QUÉ hacer (specs)
- HANDOFF = CÓMO hacerlo (pasos)

---

### 3. TEMPLATE_DEVLOG.md

**Úsalo cuando:** Un agente completa una tarea

**Quién lo usa:** Agentes Claude (automáticamente al terminar tareas)

**Ubicación final:** `knowledge/development-log/[YYYY-MM-DD]_TASK-XXX_[Nombre].md`

**Ejemplo:**
```
knowledge/development-log/2025-01-19_TASK-003_Setup_BD.md
```

**Cuándo crearlo:**
- SIEMPRE al completar una tarea
- Antes de hacer el commit final
- Como parte de los criterios de éxito

**Información que debe incluir:**
- Qué se hizo exactamente
- Problemas encontrados y soluciones
- Tiempo real vs estimado
- Tareas desbloqueadas

---

### 4. TEMPLATE_CODE_LOGIC.md

**Úsalo cuando:** Implementas lógica compleja que necesita documentación

**Quién lo usa:** Agentes de desarrollo (Backend, Frontend, Scripts)

**Ubicación final:** `knowledge/code-logic/[YYYY-MM-DD]_[Nombre_Descriptivo].md`

**Ejemplo:**
```
knowledge/code-logic/2025-01-20_API_Authentication_Flow.md
knowledge/code-logic/2025-01-21_File_System_Watcher_Logic.md
```

**Cuándo crearlo:**
- Para sistemas con múltiples componentes
- Cuando hay flujos de datos complejos
- Para decisiones de arquitectura importantes
- Cuando otros agentes necesitarán modificar el código

**NO es necesario para:**
- Código simple y autoexplicativo
- Funciones utilitarias básicas
- Componentes UI simples

---

### 5. TEMPLATE_ISSUE.md

**Úsalo cuando:** Encuentras un problema o bug

**Quién lo usa:** Cualquier agente o Martin

**Ubicación inicial:** `issues/ISS-XXX_[Nombre].md`

**Ubicación después de resolver:** `issues/processed/ISS-XXX_[Nombre].md`

**Ejemplo:**
```
issues/ISS-001_Backend_CORS_Error.md
```

**Cuándo crearlo:**
- Al detectar un bug
- Cuando algo no funciona como esperado
- Cuando un test falla
- Cuando un script de validación reporta problemas

**Severidades:**
- **CRITICAL:** Sistema no funciona, bloqueante
- **HIGH:** Funcionalidad importante rota
- **MEDIUM:** Funcionalidad menor afectada
- **LOW:** Mejora o problema cosmético

---

### 6. TEMPLATE_DECISION.md

**Úsalo cuando:** Necesitas documentar una decisión importante

**Quién lo usa:** Product Manager (Martin) o Tech Lead

**Ubicación inicial:** `decisions/DEC-XXX_[Nombre].md`

**Ubicación después de aprobar:** `decisions/processed/DEC-XXX_[Nombre].md`

**Ejemplo:**
```
decisions/DEC-001_Use_PostgreSQL_Database.md
decisions/DEC-002_Monorepo_vs_Multirepo.md
```

**Cuándo crearlo:**
- Decisiones técnicas que afectan arquitectura
- Decisiones de negocio que impactan desarrollo
- Cambios de proceso o metodología
- Trade-offs importantes

**Status posibles:**
- **PENDING:** Esperando discusión/aprobación
- **APPROVED:** Aprobada, listo para implementar
- **REJECTED:** No se va a implementar
- **DEFERRED:** Pospuesta para más adelante

---

## 🔄 Flujo de Trabajo Típico

### Crear Nueva Tarea

```
1. Martin crea BRIEF_TASK-XXX.md
   ↓
2. Martin crea HANDOFF_[ROL]_TASK-XXX.md
   ↓
3. Agente lee ambos archivos
   ↓
4. Agente ejecuta la tarea
   ↓
5. Agente crea DEVLOG_TASK-XXX.md
   ↓
6. Agente crea CODE_LOGIC (si necesario)
   ↓
7. Martin revisa y aprueba
```

### Reportar Problema

```
1. Agente/Martin detecta problema
   ↓
2. Crear ISS-XXX_[Nombre].md en /issues/
   ↓
3. Asignar severity y prioridad
   ↓
4. Investigar y proponer solución
   ↓
5. Implementar fix
   ↓
6. Actualizar issue con resolución
   ↓
7. Mover a /issues/processed/
```

### Tomar Decisión Importante

```
1. Identificar necesidad de decisión
   ↓
2. Crear DEC-XXX_[Nombre].md en /decisions/
   ↓
3. Documentar opciones y análisis
   ↓
4. Discutir con stakeholders
   ↓
5. Martin aprueba/rechaza
   ↓
6. Si aprobado: mover a /processed/ e implementar
```

---

## 📁 Estructura de Carpetas

```
virtual-teams-tracking/
├── _project-management/
│   ├── briefs/
│   │   └── BRIEF_TASK-XXX_[Nombre].md
│   └── templates/
│       ├── TEMPLATE_BRIEF.md
│       ├── TEMPLATE_HANDOFF.md
│       ├── TEMPLATE_DEVLOG.md
│       ├── TEMPLATE_CODE_LOGIC.md
│       ├── TEMPLATE_ISSUE.md
│       └── TEMPLATE_DECISION.md
├── knowledge/
│   ├── development-log/
│   │   └── [YYYY-MM-DD]_TASK-XXX_[Nombre].md
│   ├── code-logic/
│   │   └── [YYYY-MM-DD]_[Nombre].md
│   ├── handoffs/
│   │   └── HANDOFF_[ROL]_TASK-XXX.md
│   └── validations/
│       └── [reportes de validación]
├── decisions/
│   ├── DEC-XXX_[Nombre].md
│   └── processed/
│       └── DEC-XXX_[Nombre].md (aprobadas)
└── issues/
    ├── ISS-XXX_[Nombre].md
    └── processed/
        └── ISS-XXX_[Nombre].md (resueltas)
```

---

## 🎨 Convenciones de Nombres

### IDs Numéricos
- **TASK-XXX:** Usa el número secuencial (001, 002, 003...)
- **ISS-XXX:** Usa número secuencial independiente
- **DEC-XXX:** Usa número secuencial independiente

### Nombres de Archivo
- **Usa guiones bajos:** `_` para separar palabras
- **Incluye fecha:** `YYYY-MM-DD` al inicio (excepto briefs/handoffs)
- **Sé descriptivo:** El nombre debe indicar el contenido
- **Usa formato:** `[TIPO]_[ID]_[Nombre_Descriptivo].md`

**Ejemplos correctos:**
```
✅ BRIEF_TASK-008_Script_Update_Tasks.md
✅ 2025-01-19_TASK-003_Setup_BD.md
✅ 2025-01-20_Authentication_Flow_Logic.md
✅ ISS-001_CORS_Error_Backend.md
✅ DEC-002_Use_Monorepo_Structure.md
```

**Ejemplos incorrectos:**
```
❌ brief.md (no indica qué brief)
❌ devlog-task3.md (sin fecha, sin nombre descriptivo)
❌ issue1.md (no indica problema)
❌ decision.md (no indica qué decisión)
```

---

## 📝 Consejos de Uso

### Para Martin (Product Manager)

1. **Crea BRIEFs antes de HANDOFFs**
   - BRIEF = Especificaciones completas
   - HANDOFF = Guía paso a paso

2. **Revisa Dev Logs regularmente**
   - Verificar que se siguen las specs
   - Identificar problemas temprano
   - Actualizar estimaciones

3. **Documenta decisiones importantes**
   - Hoy puede parecer obvio
   - En 6 meses no recordarás por qué

### Para Agentes Claude

1. **Lee HANDOFF primero, BRIEF después**
   - HANDOFF tiene los pasos exactos
   - BRIEF tiene el contexto completo

2. **Crea Dev Log SIEMPRE**
   - Es parte de los criterios de éxito
   - Ayuda al próximo agente
   - Martin lo necesita para seguimiento

3. **Crea Code Logic para lógica compleja**
   - Si otro agente lo tocará, documéntalo
   - Si tiene múltiples pasos, documéntalo
   - Si tiene trade-offs, documéntalos

4. **Reporta Issues inmediatamente**
   - No escondas problemas
   - Mejor temprano que tarde
   - Incluye toda la información posible

---

## 🔄 Mantenimiento de Templates

### Versionado
Los templates están en control de versiones (Git).

**Para actualizar un template:**
1. Editar archivo en `_project-management/templates/`
2. Documentar cambio en commit
3. Actualizar versión en este documento

### Retrocompatibilidad
Al actualizar templates:
- ✅ Agregar campos opcionales
- ✅ Mejorar descripciones
- ❌ NO remover campos existentes
- ❌ NO cambiar formato radicalmente

---

## 📊 Checklist de Calidad

### Para BRIEFs:
- [ ] Objetivo claro en 2-3 oraciones
- [ ] Entregables específicos listados
- [ ] Criterios de éxito medibles
- [ ] Estimación de tiempo
- [ ] Dependencias identificadas

### Para HANDOFFs:
- [ ] Referencias al BRIEF correcto
- [ ] Pasos numerados y ordenados
- [ ] Comandos exactos incluidos
- [ ] Criterios de éxito (DoD)
- [ ] Instrucciones de reporte

### Para Dev Logs:
- [ ] Lista de qué se hizo
- [ ] Problemas y soluciones
- [ ] Tiempo real vs estimado
- [ ] Archivos creados/modificados
- [ ] Siguiente paso claro

### Para Code Logic:
- [ ] Diagrama de arquitectura
- [ ] Flujo de datos explicado
- [ ] Decisiones de diseño
- [ ] Componentes principales
- [ ] Cómo probar

### Para Issues:
- [ ] Título descriptivo
- [ ] Severity correcta
- [ ] Pasos para reproducir
- [ ] Resultado actual vs esperado
- [ ] Solución propuesta

### Para Decisions:
- [ ] Opciones consideradas (mínimo 2)
- [ ] Pros y contras de cada una
- [ ] Decisión clara
- [ ] Razones de la decisión
- [ ] Plan de implementación

---

## 📞 Soporte

**Preguntas sobre templates:**
- Martin Rivas (Product Manager)
- Claude PM Coordinator

**Sugerencias de mejora:**
- Crear un Issue (ISS-XXX)
- Incluir template específico y mejora propuesta

---

**Versión:** 1.0  
**Última actualización:** 2025-01-19  
**Próxima revisión:** 2025-02-19
