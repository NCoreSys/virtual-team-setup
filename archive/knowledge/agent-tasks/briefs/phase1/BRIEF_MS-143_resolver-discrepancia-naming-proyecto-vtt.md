# BRIEF: MS-143 - ISS-25b344aa: Resolver discrepancia naming proyecto VTT (name + key)

**Tarea**: MS-143
**Titulo**: ISS-25b344aa: Resolver discrepancia naming proyecto VTT (name + key)
**Repositorio**: memory-service
**Asignado a**: (pendiente — PM asigna via UI. Responsable natural: PM por ser decision de producto)
**Prioridad**: P2 (Medium)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: documentation
**Estado inicial**: task_pending (o task_blocked automatico por tener sourceIssueId activo)
**Creado por**: PJM (Martin Rivas)
**Fecha de creacion**: 2026-04-22

**ISSUE que resuelve**: `25b344aa-4ab7-4edd-ae5b-9f6856f3a1c0` (abierto en MS-117)
**Tarea que desbloquea al resolver**: MS-117 (actualmente en task_on_hold por este issue)

---

## 1. Objetivo

Tomar **una decision** sobre el naming del proyecto Memory Service en VTT vs la documentacion (HO_INICIACION, PROJECT_MEMORY, BRIEFs, ASSIGNMENTs) y **ejecutar la accion resultante** para cerrar la divergencia.

**Resultado esperado:** Proyecto VTT y documentacion consistentes entre si. Al cerrar esta tarea, el sistema auto-resolvera el ISSUE y auto-resumira MS-117.

---

## 2. Contexto

En la verificacion del proyecto (MS-117 / INIT-A-01) se encontro:

| Campo | VTT (actual) | HO esperado |
|-------|--------------|-------------|
| `name` | **"Memory Service"** | "Memory Service R1" |
| `key`  | **"MS"** | "MEM" |

Ambos valores son tecnicamente validos, pero **divergen entre el sistema real y la documentacion**. Esto causa confusion en:

- Los 26 BRIEFs de Fase 1 que mencionan "key MEM"
- El ASSIGNMENT ya adjunto en MS-117
- PROJECT_MEMORY.md
- Referencias cruzadas en el HO_INICIACION

Sin decidir, avanzar con los siguientes INIT-A-* (A-02 a A-05) generara mas deuda documental.

---

## 3. Opciones de Solucion

### Opcion A — Actualizar VTT para coincidir con HO (name="Memory Service R1", key="MEM")

**Pros:**
- Refleja que es el Release 1 (util cuando arranquen R1.1, R2)
- Consistente con los task codes MEM-* del seed original
- PROJECT_MEMORY y docs no se tocan

**Contras:**
- Los task codes actuales en VTT son MS-001..MS-142. Si cambias `key` a "MEM", los codes nuevos serian MEM-143+, quedando mezclados con los MS-* viejos (o requeriria regenerar todos los codes).
- VTT puede no permitir PATCH de `key` si genera conflicto de unicidad.

**Accion:**
```
PATCH /api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803
body: {"name": "Memory Service R1", "key": "MEM"}
```

### Opcion B — Actualizar docs para coincidir con VTT (name="Memory Service", key="MS")

**Pros:**
- No se tocan task codes existentes (142 en uso)
- Cambio rapido y seguro: solo docs
- "MS" como prefijo ya esta en uso en todas las tareas; mantener consistencia

**Contras:**
- Se pierde la referencia explicita a "R1" (si el producto evoluciona a R2, el project VTT seguiria llamandose "Memory Service" a secas)
- Hay que actualizar: HO_INICIACION, PROJECT_MEMORY, 26 BRIEFs, 1 ASSIGNMENT

**Accion:**
1. Script que actualiza todos los docs (regex sobre "Memory Service R1" -> "Memory Service" y "key MEM" -> "key MS" donde aplique).
2. Commit al repo (cuando INIT-B-01 este desbloqueada).

### Opcion C — Divergencia intencional (MS en VTT, "Memory Service R1" y alias MEM en docs)

**Pros:**
- No se cambia nada

**Contras:**
- Deuda documental permanente
- Confusion para los 8 agentes del equipo
- **No se recomienda**.

---

## 4. Campos del Sistema VTT (de la tarea creada)

| Campo | Valor |
|-------|-------|
| `title` | ISS-25b344aa: Resolver discrepancia naming proyecto VTT (name + key) |
| `estimatedHours` | 1 |
| `complexity` | LOW |
| `category` | documentation |
| `priorityId` | UUID Medium |
| `statusId` | UUID task_pending (el sistema puede haberla movido a task_blocked automaticamente por tener sourceIssueId activo) |
| `assignedToId` | NULL al crear — PM asigna via UI |
| `sourceIssueId` | 25b344aa-4ab7-4edd-ae5b-9f6856f3a1c0 |
| `deliveryId` | 98a0be7a-... (A. VTT Setup) |

---

## 5. Dependencias

**Bloquea al resolver:**
- Issue 25b344aa-... sera auto-marcado como resuelto al completar esta tarea
- MS-117 saldra automaticamente de task_on_hold (auto-resume)

**No depende de ninguna tarea previa.**

---

## 6. Criterios de Exito

### Funcionales (elegir UNA):

**Opcion A ejecutada:**
- [ ] PATCH a /api/projects/d0fc276d-... ejecutado
- [ ] GET posterior muestra `name="Memory Service R1"` y `key="MEM"`
- [ ] Reportar si los task codes requieren regeneracion y como se manejara

**Opcion B ejecutada:**
- [ ] HO_INICIACION_MEMORY_SERVICE.md actualizado (referencias a "Memory Service R1" -> "Memory Service" donde aplique)
- [ ] PROJECT_MEMORY.md actualizado
- [ ] 26 BRIEFs en knowledge/agent-tasks/briefs/phase1/ actualizados donde mencionan "MEM"
- [ ] ASSIGNMENT_INIT-A-01 actualizado
- [ ] Commit al repo (una vez desbloqueada INIT-B-01) o guardado local con nota

**Opcion C adoptada:**
- [ ] Documentar la divergencia en PROJECT_MEMORY.md como decision explicita
- [ ] Crear glosario "alias MEM = key MS en VTT"

### No Funcionales:
- [ ] Decision registrada en un comentario de la tarea MS-143 antes de mover a in_review
- [ ] Si se toca el proyecto VTT, confirmar que no rompe las 142 tareas existentes
- [ ] Si se tocan docs, confirmar que no quedaron referencias mixtas

### Documentacion:
- [ ] Development Log de la tarea MS-143
- [ ] Comentario/reporte con decision final y razon

---

## 7. Como Probar

### Si se elige Opcion A:
```bash
TOKEN=$(cat /tmp/vtt_token.txt)
# Ejecutar el PATCH
curl -s -X PATCH \
  http://77.42.88.106:3000/api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Memory Service R1", "key": "MEM"}'

# Verificar
curl -s -H "Authorization: Bearer $TOKEN" \
  http://77.42.88.106:3000/api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803 | jq '.data | {name, key}'
```

### Si se elige Opcion B:
```bash
# Buscar todas las referencias a actualizar
grep -rn "Memory Service R1" memory-service-project/ knowledge/
grep -rn "key MEM\|key.*MEM\"" knowledge/ memory-service-project/

# Despues de aplicar cambios, verificar que no quedan referencias mixtas
```

---

## 8. Referencias

### Documentacion Interna
- ISSUE completo: GET /api/issues/25b344aa-4ab7-4edd-ae5b-9f6856f3a1c0
- Tarea origen: MS-117 (INIT-A-01) — ver DevLog `devlogs/2026-04-22_INIT-A-01_verificar-proyecto-vtt.md`
- HO_INICIACION: `memory-service-project/01-project-management/00-setup/HO_INICIACION_MEMORY_SERVICE.md`
- PROJECT_MEMORY: a verificar en el repo

### Endpoints utiles
- GET  `/api/projects/{id}` — estado actual
- PATCH `/api/projects/{id}` — para Opcion A
- PUT  `/api/issues/{id}` — solo si hay que updatear el issue manualmente (normalmente no hace falta, el sistema auto-resuelve al completar esta tarea)

---

## 9. Notas Importantes

- **Esta tarea tiene `sourceIssueId`.** Al moverla a `task_completed`, el sistema automaticamente:
  1. Marca el issue 25b344aa como `isResolved=true`
  2. Detecta que MS-117 tiene todos sus issues resueltos
  3. Auto-resume MS-117: sale de `task_on_hold` y vuelve a su `previousStatus` (`task_in_progress`)
- **PM decide.** Esta tarea es sobre product decision (naming del proyecto), no ejecucion tecnica.
- **1 hora estimada** porque la decision en si toma 10 min; la ejecucion (Opcion A: 1 PATCH; Opcion B: actualizacion de docs) toma el resto.

---

## 10. Contacto

**Coordinador**: Martin Rivas (martin.rivas@prompt-ai.studio)
**Pregunta operativa**: via comment en esta misma tarea o al PJM

---

**Ultima actualizacion:** 2026-04-22
**Version:** 1.0
**Estado del BRIEF:** Ready
