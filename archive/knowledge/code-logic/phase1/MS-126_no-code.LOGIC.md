# Code Logic — MS-126: Git user config + commit conventions

**Tarea:** MS-126 / INIT-B-05
**Fecha:** 2026-05-01
**Agente:** PJM-Agent

---

## Nota

Esta tarea es 100% de configuración y documentación — no produce archivos de código fuente. No hay lógica ejecutable que documentar.

El assignment (§7) confirma explícitamente: *"Code Logic: No aplica (no hay código, solo config/docs)"*.

Este archivo existe para satisfacer el requisito del sistema VTT de adjuntar un `code_logic` antes de mover a `task_in_review`.

---

## Qué hace esta tarea

Configura la identidad Git local del repo (`user.name`, `user.email`) y establece la convención oficial de commits en `CONTRIBUTING.md` para que todos los agentes del equipo usen el mismo formato.

---

## Archivos Afectados

| Archivo | Tipo | Cambio |
|---------|------|--------|
| `CONTRIBUTING.md` | Documentación | Actualizado v1.0 → v1.1: sección Convención de Commits |
| `.git/config` (local) | Configuración Git | `user.name` y `user.email` establecidos |

---

## Lógica de Configuración

**`.git/config` (local):**  
`git config user.name` y `git config user.email` sin `--global` — aplican solo al repo `memory-service`, no al sistema global.

**`CONTRIBUTING.md`:**  
Documento estático leído por humanos y agentes. No tiene lógica ejecutable.

---

## Historial de Cambios

| Fecha | Cambio | Agente |
|-------|--------|--------|
| 2026-05-01 | Creación — tarea no-code, git config + docs | PJM-Agent |
