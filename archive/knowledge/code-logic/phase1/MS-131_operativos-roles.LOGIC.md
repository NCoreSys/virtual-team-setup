# Code Logic — MS-131 · INIT-D-01: Crear OPERATIVO por cada rol activo

## Tipo de entregable

Documentación operativa (no código fuente). Los OPERATIVOs son archivos markdown que actúan como "system prompt contextualizado" para cada agente Claude.

## Propósito

Permitir que cualquier agente (BE, FE, QA, etc.) arranque una sesión con toda la información necesaria: identidad, credenciales, endpoints VTT, reglas del rol, workflow y rutina de apertura. Sin este contexto, el agente necesitaría leer múltiples documentos antes de poder operar.

## Estructura de cada OPERATIVO

```
Identidad (UUID, email, service key, repos)
  → Rol (qué hace / qué no hace)
    → Stack técnico específico del rol
      → Auth snippet (Python, listo para copiar/pegar)
        → Endpoints VTT relevantes para el rol
          → Reglas críticas del rol
            → Workflow 12 pasos (adaptado al rol)
              → Rutina de apertura de sesión
                → Referencias (archivos clave a leer)
                  → Workspace (qué repos abrir)
```

## Decisiones de diseño

- **UUID hardcodeado en cada archivo**: el agente no necesita buscarlo en ningún otro lugar
- **Auth snippet copiable**: mínima fricción para autenticarse contra VTT
- **Sí/NO table en Rol**: evita ambigüedad sobre alcance — cada rol sabe exactamente qué no debe hacer
- **Rutina de apertura explícita**: garantiza que el agente lee `.vtt/memory/` antes de operar

## Dependencias

- `PROJECT_RULES.md` — referenciado por todos los OPERATIVOs
- `.vtt/memory/*_memory.md` — memoria persistente de cada rol
- `.vtt/teams.md` — estructura de equipos y scopes
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — fuente de verdad funcional

## Sin código fuente

Este entregable es 100% markdown. No hay lógica de programación que documentar.
