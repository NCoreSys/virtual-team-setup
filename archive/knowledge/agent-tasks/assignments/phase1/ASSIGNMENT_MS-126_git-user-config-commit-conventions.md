# ASSIGNMENT: MS-126 - Git user config + commit conventions

**Task ID**: MS-126
**Brief ref**: INIT-B-05
**Titulo**: Git user config + commit conventions
**Repositorio destino**: memory-service (este repo)
**Asignado a**: PJM (Martin Rivas)
**Prioridad**: M (MEDIUM)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: documentation
**Generado por**: PJM
**Fecha asignacion**: 2026-05-01

---

## 1. Objetivo

Configurar `git config user.name` y `user.email` locales en el repo, y documentar la convención de commits del proyecto en `CONTRIBUTING.md`.

**Resultado esperado:** Git config verificado. `CONTRIBUTING.md` en la raíz del repo con el formato oficial de commits.

---

## 2. Contexto

Sin convención documentada, cada agente usa su propio estilo y el changelog queda caótico. El formato `[tipo] [TASK_ID]: descripción + Co-Authored-By` permite trackear quién hizo qué y conectarlo con VTT.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `.claude/rules/PROJECT_RULES.md` §8 — Convenciones de Commits (fuente de verdad)
2. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` (§1 Overview)

---

## 4. Prerequisitos

- [ ] Acceso al repo `memory-service` con permisos de escritura
- [ ] Token VTT válido

---

## 5. Implementación

### 5.1. Configurar Git local

```bash
git config user.name "Martin Rivas"
git config user.email "martin.rivas@prompt-ai.studio"
```

Verificar:
```bash
git config --get user.name   # → Martin Rivas
git config --get user.email  # → martin.rivas@prompt-ai.studio
```

### 5.2. Crear `CONTRIBUTING.md` en la raíz del repo

Contenido:

```markdown
# Contributing to Memory Service

## Convención de Commits

### Formato

[tipo] [TASK_ID]: Descripción breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #TASK_ID


### Tipos de commit

| Tipo | Cuándo usarlo |
|------|---------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Solo documentación |
| `refactor` | Refactorización sin cambios funcionales |
| `test` | Agregar o modificar tests |
| `chore` | Mantenimiento (deps, config, CI) |

### Ejemplos

feat [MEM-BE-001]: Setup inicial Express + estructura carpetas

- Crear src/app.ts con middlewares base
- Configurar Swagger en src/config/swagger.ts
- Estructura de carpetas según SPEC v1.9 §3

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MEM-BE-001


docs [MS-126]: Git user config + CONTRIBUTING

- Configurar git user.name y user.email locales
- Crear CONTRIBUTING.md con convención oficial

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-126

---

## Reglas Obligatorias

- **Co-Authored-By es OBLIGATORIO** en todos los commits
- **NUNCA commit directo a main** — siempre branch + PR
- **Branch naming**: `feature/[TASK_ID]`
- **PR title**: `[[TASK_ID]] Título descriptivo`

## Workflow Git

```bash
# 1. Crear branch
git checkout -b feature/[TASK_ID]

# 2. Hacer cambios, luego commit
git add .
git commit -m "[tipo] [TASK_ID]: Descripción"

# 3. Push + PR
git push origin feature/[TASK_ID]
gh pr create --title "[[TASK_ID]] Título" --body "Ver devlog para detalles." --base main
```

## Recursos

- PROJECT_RULES.md — reglas operativas completas
- VTT API: http://77.42.88.106:3000/api-docs
```

---

## 6. Verificación

```bash
git config --get user.name
# → Martin Rivas

git config --get user.email
# → martin.rivas@prompt-ai.studio

ls CONTRIBUTING.md
# → CONTRIBUTING.md existe en raíz
```

---

## 7. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | `CONTRIBUTING.md` | Raíz del repo `memory-service` |
| 2 | Development Log | `knowledge/development-log/2026-05-XX_MS-126_git-config-contributing.md` |
| 3 | Code Logic | No aplica (no hay código, solo config/docs) |
| 4 | Commit + PR | Branch `feature/MS-126`, PR a `main` |

> Code Logic no es requerido para tareas 100% de documentación/configuración (sin código fuente).

---

## 8. Workflow

```bash
# 1. Cambiar estado en VTT
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-126-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_progress","comment":"Configurando git user y creando CONTRIBUTING.md"}'

# 2. Crear branch
git checkout -b feature/MS-126

# 3. Configurar git (sección 5.1)
# 4. Crear CONTRIBUTING.md (sección 5.2)

# 5. Commit
git add CONTRIBUTING.md
git commit -m "docs [MS-126]: Git user config + CONTRIBUTING.md

- Configurar git user.name='Martin Rivas' y user.email='martin.rivas@prompt-ai.studio'
- Crear CONTRIBUTING.md con convención oficial de commits
- Formato: [tipo] [TASK_ID]: descripción + Co-Authored-By obligatorio

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-126"

# 6. Push + PR
git push origin feature/MS-126
gh pr create --title "[MS-126] Git user config + CONTRIBUTING" --body "Ver devlog para detalles." --base main

# 7. Cambiar estado
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-126-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_review","comment":"PR creado, pendiente revisión"}'
```

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-01
**Version**: 1.0
