# 🚀 HANDOFF: [Rol del Agente] - TASK-XXX [Nombre de la Tarea]

**De:** Martin Rivas (Product Manager)  
**Para:** [Rol del Agente]  
**Fecha:** [YYYY-MM-DD]  
**Prioridad:** [P0-CRÍTICO | P1-ALTA | P2-MEDIA | P3-BAJA]  
**Estimación:** [X horas]  
**Depende de:** [TASK-XXX, TASK-YYY] (estado: [completadas/en progreso])

---

## 📋 CONTEXTO RÁPIDO

[2-3 oraciones explicando el estado actual del proyecto y por qué esta tarea es necesaria ahora.]

**Tu tarea:** TASK-XXX - [Nombre de la tarea]

---

## 📚 ARCHIVOS QUE DEBES LEER ANTES DE EMPEZAR

**OBLIGATORIO leer en orden:**

1. **BRIEF_TASK-XXX_[Nombre].md** ([XX] min)
   - Contiene TODAS las especificaciones
   - [Qué información clave incluye]
   - [Otra información importante]

2. **[Otro documento relevante]** - Sección X ([XX] min)
   - Para entender [aspecto importante]
   - Confirmar [detalles críticos]

**OPCIONAL (si tienes dudas):**
- `[Documento de referencia]` - Sección X

---

## ✅ PASOS A SEGUIR

### PASO 1: [Nombre del paso] ([XX] min)

[Descripción breve de qué se hace en este paso]

```bash
# Comandos exactos a ejecutar
comando 1
comando 2
```

**Verificar:**
```bash
# Comando de verificación
comando de test
# Resultado esperado: [qué debe mostrar]
```

---

### PASO 2: [Nombre del paso] ([XX] min)

[Descripción del paso]

**Crear:** `ruta/al/archivo.ext`

```[lenguaje]
// Contenido completo del archivo
// con comentarios explicativos
```

---

### PASO 3: [Nombre del paso] ([XX] min)

[Descripción del paso]

**Actualizar:** `ruta/al/archivo.ext`

Agregar/modificar:
```[lenguaje]
// Código a agregar o cambiar
```

---

### PASO 4: [Nombre del paso] ([XX] min)

[Instrucciones del paso]

---

### PASO 5: Verificar que Todo Funciona ([XX] min)

```bash
# Checklist de verificación

# 1. Test 1
comando_test_1
# Debe retornar: [resultado esperado]

# 2. Test 2
comando_test_2
# Debe retornar: [resultado esperado]

# 3. Test 3
comando_test_3
# Debe retornar: [resultado esperado]
```

---

### PASO 6: Commit de Cambios ([XX] min)

```bash
cd ~/proyectos/virtual-teams-tracking

git add [archivos modificados]
git status
# Verificar que [archivos sensibles] NO están en la lista

git commit -m "[tipo]([scope]): [descripción corta]

[Descripción detallada de los cambios]
[Lista de archivos/funcionalidades agregadas]

TASK-XXX: [Nombre de la tarea]"

git push origin develop
```

---

## ✅ CRITERIOS DE ÉXITO (Definition of Done)

**Antes de reportar como completado, verificar:**

- [ ] [Criterio funcional 1]
- [ ] [Criterio funcional 2]
- [ ] [Criterio de calidad 1]
- [ ] [Criterio de calidad 2]
- [ ] Código sin errores
- [ ] Tests pasando
- [ ] Commit y push exitoso
- [ ] Development Log creado

---

## 📋 CÓMO REPORTAR CUANDO TERMINES

### 1. Crear Development Log

Crear archivo: `/knowledge/development-log/[YYYY-MM-DD]_TASK-XXX_[Nombre].md`

```markdown
# Development Log - TASK-XXX

**Tarea:** [Nombre de la tarea]  
**Fecha:** [YYYY-MM-DD]  
**Agente:** [Rol del Agente]  
**Estado:** COMPLETADO

## Qué se hizo

- [x] [Logro 1]
- [x] [Logro 2]
- [x] [Logro 3]

## Decisiones tomadas

[Si hubo alguna decisión técnica importante]

## Problemas encontrados

[Si hubo alguno y cómo se resolvió]

## Tiempo real

[X horas]

## Siguiente paso

[Qué tareas se desbloquean o qué sigue]
```

### 2. Crear Code Logic (si aplica)

Si la tarea involucra lógica compleja, crear:
`/knowledge/code-logic/[YYYY-MM-DD]_[Nombre_Descriptivo].md`

Documentar:
- Flujo de la aplicación
- Decisiones de arquitectura
- Algoritmos importantes

### 3. Notificar a Martin

```
✅ TASK-XXX COMPLETADA

[Descripción breve de lo logrado]

Archivos:
- Dev Log: /knowledge/development-log/...
- Code Logic: /knowledge/code-logic/... (si aplica)

Tareas desbloqueadas:
- TASK-YYY: [Nombre]

Tiempo: [X horas]
```

---

## 🚨 SI TIENES PROBLEMAS

**Problema 1: [Error común esperado]**
→ Solución: [Cómo resolverlo]

**Problema 2: [Otro error común]**
→ Solución: [Cómo resolverlo]

**Si persiste el problema:** Reportar a Martin inmediatamente con:
- Qué intentaste
- Error específico
- Logs relevantes

---

## ⏱️ TIEMPO ESTIMADO

**Total:** [X] horas

Desglose:
- Paso 1: XX min
- Paso 2: XX min
- Paso 3: XX min
- Paso 4: XX min
- Paso 5: XX min
- Paso 6: XX min
- Documentation: XX min
- Buffer: XX min

---

## 🎯 PRÓXIMOS PASOS (Después de Completar)

**Se desbloquean estas tareas:**

1. **TASK-YYY** - [Nombre] ([Agente]) - [X]h
2. **TASK-ZZZ** - [Nombre] ([Agente]) - [X]h

O bien: "Esta tarea completa el sprint/milestone."

---

## 📞 CONTACTO

**Product Manager:** Martin Rivas  
**PM Coordinator:** Claude  
**Urgente:** Reportar bloqueadores inmediatamente

---

**¡Éxito con la tarea! 🚀**

*Este handoff contiene TODO lo que necesitas. Si tienes dudas, lee el BRIEF completo.*
