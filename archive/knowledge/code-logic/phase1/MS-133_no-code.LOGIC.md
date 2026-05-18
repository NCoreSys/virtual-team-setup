# Code Logic — MS-133: CONTEXTO de sesión por rol

**Tarea:** MS-133 (INIT-D-03)
**Archivos creados:** `knowledge/agent-tasks/CONTEXTO_*.md` (5 archivos)
**Fecha:** 2026-05-02

## Nota

Esta tarea no genera código fuente ejecutable. Los entregables son documentos de contexto de sesión para agentes.

## Archivos generados

| Archivo | Propósito |
|---------|-----------|
| `CONTEXTO_TL_SESION.md` | Estado persistente Tech Lead |
| `CONTEXTO_BE_SESION.md` | Estado persistente Backend Engineer |
| `CONTEXTO_DB_SESION.md` | Estado persistente Database Engineer |
| `CONTEXTO_FE_SESION.md` | Estado persistente Frontend Developer |
| `CONTEXTO_QA_SESION.md` | Estado persistente QA Engineer |

## Propósito de los CONTEXTO files

Cada archivo es leído por el agente al inicio de sesión y actualizado al final. Contiene: identidad (UUID, email), estado del proyecto, responsabilidades, tareas asignadas, próximos pasos, contexto técnico, documentos clave y notas de coordinación.

## Decisiones

- No sobreescribir los 4 archivos ya existentes (PM, PJM, DO, TECH_LEAD)
- Formato basado en CONTEXTO_PM como plantilla
- Contenido técnico específico por rol
