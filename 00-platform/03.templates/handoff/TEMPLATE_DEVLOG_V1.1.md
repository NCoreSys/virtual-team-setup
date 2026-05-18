# DEVLOG: [TASK-ID] — [Nombre de la Tarea]

**Documento:** DEVLOG_[TASK-ID].md
**Versión:** 1.1
**Tarea:** [TASK-ID] — [Nombre completo de la tarea]
**Agente:** [Rol del Agente]
**Fecha inicio:** [YYYY-MM-DD]
**Fecha fin:** [YYYY-MM-DD]
**Estado:** ✅ COMPLETADO | ⚠️ PARCIAL | ❌ BLOQUEADO

---

## 1. RESUMEN

**Objetivo:** [1-2 oraciones describiendo qué se debía lograr]

**Resultado:** [1-2 oraciones describiendo qué se logró]

**Tiempo:**
- Estimado: [X]h
- Real: [X]h
- Variación: [+X/-X]h ([razón breve si hay variación significativa])

**Desglose:**
- Implementación: [XX] min
- Testing: [XX] min
- Documentación: [XX] min
- Troubleshooting: [XX] min

---

## 2. QUÉ SE HIZO

### Archivos Creados

| Archivo | Descripción | Líneas |
|---------|-------------|--------|
| `[ruta/archivo.ext]` | [Qué hace] | [~N] |
| `[ruta/archivo.ext]` | [Qué hace] | [~N] |

### Archivos Modificados

| Archivo | Cambio | Razón |
|---------|--------|-------|
| `[ruta/archivo.ext]` | [Qué se cambió] | [Por qué] |

### Migraciones/Schema (si aplica)

```sql
-- Resumen de cambios de schema
-- Tabla: [nombre]
-- Cambios: [descripción]
```

### Endpoints (si aplica)

| Método | Path | Descripción |
|--------|------|-------------|
| [GET/POST/etc] | `/api/[path]` | [Qué hace] |

---

## 3. DEPENDENCIAS AGREGADAS

| Paquete | Versión | Tipo | Para qué |
|---------|---------|------|----------|
| `[paquete]` | `^X.Y.Z` | dep / devDep | [Propósito] |

> **Si no se agregaron dependencias:** "Sin dependencias nuevas en esta tarea."

---

## 4. DECISIONES TOMADAS

### Decisión 1: [Título]

**Contexto:** [Por qué se necesitó tomar esta decisión]

**Opciones consideradas:**
1. [Opción A] — [Pro/contra]
2. [Opción B] — [Pro/contra]

**Decisión:** [Qué se eligió]

**Razón:** [Por qué se eligió]

> **Nota:** Si no hubo decisiones técnicas significativas, escribir: "No hubo decisiones técnicas significativas. Se siguió el diseño del handoff."

---

## 5. ISSUES ENCONTRADOS

### Issue 1: [Título del problema]

**Síntoma:** [Qué se observó]

**Causa:** [Por qué pasó]

**Solución:** [Cómo se resolvió]

**Tiempo perdido:** [X]h

---

### Issue 2: [Título del problema]

[Repetir estructura]

> **Nota:** Si no hubo issues, escribir: "No se encontraron issues durante la implementación."

---

## 6. CÓMO PROBAR

### 6.1 Prerequisitos

```bash
# Comandos de setup necesarios
[comando 1]
[comando 2]
```

### 6.2 Tests Automatizados

```bash
# Backend (pytest)
pytest tests/[path] -v

# Frontend (Vitest)
npm run test --prefix frontend -- --grep "[pattern]"

# E2E (Playwright)
npx playwright test [archivo]
```

### 6.3 Prueba Manual

**Paso 1:** [Descripción]
```bash
# Comando o acción
[comando]
# Resultado esperado: [qué debe pasar]
```

**Paso 2:** [Descripción]
```bash
# Comando o acción
[comando]
# Resultado esperado: [qué debe pasar]
```

### 6.4 Verificación Rápida

```bash
# Checklist de verificación rápida
# [ ] Test 1: [descripción] — [comando]
# [ ] Test 2: [descripción] — [comando]
# [ ] Test 3: [descripción] — [comando]
```

---

## 7. DOCUMENTACIÓN ACTUALIZADA

| Documento | Sección | Cambio |
|-----------|---------|--------|
| `[documento].md` | [Sección] | [Qué se actualizó] |
| `[archivo].LOGIC.md` | — | Creado |

---

## 8. DEPENDENCIAS DESBLOQUEADAS

| Tarea | Agente | Descripción |
|-------|--------|-------------|
| [TASK-ID] | [Rol] | [Qué puede hacer ahora] |

> **Si no desbloquea nada:** "Esta tarea no desbloquea otras tareas directamente."

---

## 9. DEUDA TÉCNICA (si aplica)

| Item | Descripción | Prioridad | Sugerencia |
|------|-------------|-----------|------------|
| [DT-001] | [Qué se dejó pendiente] | Alta/Media/Baja | [Cómo resolverlo] |

> **Si no hay deuda:** "No se generó deuda técnica."

---

## 10. NOTAS PARA EL SIGUIENTE AGENTE

[Cualquier información útil para quien trabaje en tareas relacionadas]

- [Nota 1]
- [Nota 2]
- [Nota 3]

---

## 11. COMMITS

| Hash | Mensaje | Archivos |
|------|---------|----------|
| `[abc123]` | `[tipo]([scope]): [mensaje]` | [N] archivos |

**Branch:** `feature/[TASK-ID]`
**PR:** `#[número]`

---

## 12. MÉTRICAS

| Métrica | Valor |
|---------|-------|
| Archivos creados | [N] |
| Archivos modificados | [N] |
| Líneas agregadas | [~N] |
| Líneas eliminadas | [~N] |
| Tests agregados | [N] |
| Cobertura nueva | [X]% |

---

## 13. CRITERIOS DE ÉXITO

- [ ] Todos los CAs del brief completados
- [ ] `.LOGIC.md` creado/actualizado por cada archivo de código
- [ ] Tests pasando (sin regresiones)
- [ ] PR creado en rama `feature/[TASK-ID]`
- [ ] Comentario de entrega posteado en VTT (`POST /api/tasks/{id}/comments`)
- [ ] Tarea movida a `task_in_review` en VTT
- [ ] Documentación dinámica actualizada (`API_CONTRACT.md`, `MODELO_DATOS.md` si aplica)

---

## 14. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | [YYYY-MM-DD] | [Agente] | Versión inicial |
| 1.1 | 2026-03-30 | TL-Agent | Desglose de tiempo, Dependencias Agregadas, Criterios de Éxito, comandos BE/FE/E2E separados |

---

**FIN DEL DEVLOG**
