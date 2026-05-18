---
name: iniciar-tarea
description: Workflow completo de inicio de tarea — verifica estado en VTT, cambia a task_in_progress, crea branch Git, y confirma que el agente tiene todo para trabajar.
role: ALL
vtt_version: "1.0"
---

# Skill: /iniciar-tarea [TASK_ID]

## Propósito
Ejecuta los pasos obligatorios de inicio de tarea según PROJECT_RULES §2 y §6.5.
Verifica dependencias, cambia estado en VTT, crea branch, y valida que el entorno esté listo.

## Cuándo usar
Siempre que un agente va a comenzar a trabajar en una tarea asignada.

## Parámetros
- `TASK_ID` — ID de la tarea a iniciar (ej: MEM-BE-001, MEM-DB-003)

## Pasos de ejecución

### 1. Verificar estado en VTT
```bash
curl -s -X GET "$API_URL/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '{id,status,assignee,dependencies}'
```

**Criterio para proceder:**
- Estado debe ser `pending` o `task_assigned`
- NO proceder si es `task_on_hold`, `task_rejected`, `task_cancelled`

### 2. Verificar dependencias
```bash
curl -s -X GET "$API_URL/api/tasks/$TASK_ID/dependencies" \
  -H "Authorization: Bearer $TOKEN" | jq '.[] | {id,status,title}'
```

**Criterio:** todas las dependencias deben estar en `task_completed`.
Si alguna está en otro estado → reportar blocker al TL, NO iniciar.

### 3. Leer el ASSIGNMENT completo
El TL envía el ASSIGNMENT por VTT o en sesión. Leerlo COMPLETO antes de continuar.
Confirmar que está claro:
- Qué archivos crear/modificar
- Qué endpoints/funciones implementar
- Criterios de aceptación
- Cómo probar

### 4. Crear branch Git
```bash
git checkout main
git pull origin main
git checkout -b feature/$TASK_ID
```

Verificar que el branch se creó:
```bash
git branch --show-current
# debe mostrar: feature/TASK_ID
```

### 5. Cambiar estado en VTT a task_in_progress
```bash
curl -X PATCH "$API_URL/api/tasks/$TASK_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"task_in_progress\",\"comment\":\"Tarea iniciada. Branch: feature/$TASK_ID\"}"
```

### 6. Confirmar entorno

Verificar que el entorno local está listo:
- [ ] Variables de entorno configuradas (`.env` existe y tiene valores)
- [ ] Dependencias instaladas (`npm install` o equivalente)
- [ ] Base de datos accesible (si aplica)
- [ ] Servidor levanta sin errores (`npm run dev`)

### 7. Reportar inicio

```markdown
## Iniciando: [TASK_ID] — [Título]

**Branch:** feature/[TASK_ID]
**Estado VTT:** task_in_progress ✅
**Dependencias:** todas en task_completed ✅
**Entorno:** listo ✅

Comenzando implementación...
```

## Si algo falla

**Dependencia no completada:**
→ Notificar al TL con: qué tarea está bloqueando, qué estado tiene

**Branch ya existe:**
```bash
git checkout feature/$TASK_ID
git rebase origin/main
```

**Entorno no listo:**
→ Documentar qué falta, reportar al TL/DO como blocker
→ Cambiar estado a `task_on_hold` con comentario explicativo
