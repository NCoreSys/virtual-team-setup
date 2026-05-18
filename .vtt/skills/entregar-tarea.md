---
name: entregar-tarea
description: Checklist completo de entrega de tarea — valida código, crea devlog y code-logic, hace commit+push, crea PR, y cambia estado a task_in_review en VTT.
role: ALL
vtt_version: "1.0"
---

# Skill: /entregar-tarea [TASK_ID]

## Propósito
Ejecuta el checklist de entrega del PROJECT_RULES §9 y §6.5 (pasos 6-12).
Garantiza que ningún entregable obligatorio quede faltante.

## Cuándo usar
Cuando el agente terminó la implementación y va a entregar la tarea.

## Parámetros
- `TASK_ID` — ID de la tarea completada (ej: MEM-BE-001)

## Pasos de ejecución

### 1. Validar funcionalidad

```bash
# El agente debe ejecutar y confirmar:
npm run build     # sin errores
npm run dev       # levanta OK
npm test          # tests pasan (si aplica)
```

**NO entregar si hay errores de compilación o tests fallando.**

### 2. Crear/actualizar archivos .LOGIC.md

Por cada archivo de código creado o modificado:
```
src/controllers/memoryController.ts
  → knowledge/code-logic/controllers/memoryController.LOGIC.md
```

Verificar que cada `.LOGIC.md`:
- [ ] Existe (crear si no existe)
- [ ] Está actualizado con los cambios de esta tarea
- [ ] Tiene historial de cambios con entry de hoy
- [ ] NO incluye código fuente (solo descripciones)

### 3. Crear Development Log

```
knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[descripcion-corta].md
```

Usar template: `.vtt/templates/exec/TEMPLATE_DEVELOPMENT_LOG.md`

Contenido obligatorio:
- Qué se implementó
- Decisiones técnicas tomadas (y por qué)
- Dependencias agregadas (con versión exacta)
- Cómo probar/validar
- Pendientes si los hay

### 4. Verificar Swagger (si la tarea creó endpoints)

```bash
npm run dev
# abrir http://localhost:3002/api-docs
# verificar que el endpoint aparece
# probar con "Try it out"
```

Si los endpoints no aparecen en `/api-docs` → la tarea está incompleta.

### 5. Commit y push

```bash
# Solo agregar archivos de tu tarea (NO git add .)
git add src/[archivos-de-tu-tarea]
git add knowledge/development-log/YYYY-MM-DD_[TASK_ID]_*.md
git add knowledge/code-logic/[archivos-logic-de-tu-tarea]

git commit -m "$(cat <<'EOF'
[tipo] [TASK_ID]: Descripción breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Refs: #[TASK_ID]
EOF
)"

# Rebase con main antes de push
git fetch origin
git rebase origin/main
git push origin feature/[TASK_ID]
```

### 6. Crear Pull Request

```bash
gh pr create \
  --title "[[TASK_ID]] Título descriptivo" \
  --body "$(cat <<'EOF'
## Cambios
- [resumen de implementación]

## Cómo probar
- [pasos para validar]

## Devlog
`knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[nombre].md`
EOF
)" \
  --base main
```

### 7. Cambiar estado en VTT a task_in_review

```bash
PR_URL=$(gh pr view --json url -q .url)

curl -X PATCH "$API_URL/api/tasks/$TASK_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"task_in_review\",\"comment\":\"Entregada. PR: $PR_URL\"}"
```

### 8. Reportar al TL con formato estándar

```markdown
## Entrega: [TASK_ID] — [Título]

### Código:
- `src/[archivo]` — [descripción]

### Development Log:
`knowledge/development-log/YYYY-MM-DD_[TASK_ID]_[nombre].md`

### Code Logic:
- `knowledge/code-logic/[archivo].LOGIC.md`

### PR:
[URL del PR en GitHub]

### Cómo probar:
[comandos o pasos para validar]
```

## Checklist final

- [ ] Código compila sin errores
- [ ] Tests pasan
- [ ] `.LOGIC.md` por cada archivo de código
- [ ] Development Log completo
- [ ] Swagger docs (si hay endpoints)
- [ ] Commit bien formateado con Co-Authored-By
- [ ] Push hecho
- [ ] PR creado
- [ ] Estado VTT en `task_in_review`
- [ ] TL notificado

**Si falta UNO → NO reportar como completada**
