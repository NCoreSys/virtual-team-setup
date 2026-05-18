# Code Logic — PROJECT_MEMORY.md

**Archivo de código:** `knowledge/PROJECT_MEMORY.md`
**Tarea:** MS-132 (INIT-D-02)
**Tipo:** Documentación — sin código ejecutable

---

## Propósito

Archivo de memoria persistente del proyecto Memory Service. Todos los agentes lo leen al iniciar sesión para obtener contexto del proyecto sin necesidad de leer documentos dispersos.

---

## Estructura

```
PROJECT_MEMORY.md
├── Stack técnico (lenguajes, frameworks, puertos)
├── Fases del proyecto (Setup, Backend, Frontend, DevOps)
├── Decisiones de arquitectura D-XX
├── UUIDs del equipo
└── Referencias a SPEC v1.9
```

---

## Dependencias

- **Fuente de verdad**: `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`
- **Decisiones**: ADR-001 y decisiones D-XX del proyecto
- **Equipo**: `.claude/rules/Proyect_data.md`

---

## Flujo de uso

1. Agente inicia sesión
2. Lee `PROJECT_MEMORY.md` (rutina de apertura en OPERATIVO_[ROL])
3. Obtiene contexto de stack, fases activas y UUIDs
4. Comienza trabajo sin necesidad de leer documentos adicionales

---

## Historial de Cambios

| Fecha | Cambio | Tarea |
|-------|--------|-------|
| 2026-05-01 | Creación inicial | MS-132 |
