# Code Logic — MS-134: _pm/ACCESOS.md

**Archivo de código:** `_pm/ACCESOS.md`
**Tarea:** MS-134 (INIT-D-04)
**Fecha creación:** 2026-05-02

---

## Qué hace este archivo

Documento de referencia operativa que centraliza la matriz de accesos del equipo Memory Service. Responde a: ¿qué UUID, email y repo tiene cada rol?

## Propósito

- Punto único de verdad para credenciales y accesos del equipo
- Guía de onboarding para nuevos agentes
- Referencia rápida para el PM en coordinación diaria

## Estructura

1. **Tabla de roles**: UUID + email VTT + repo + estado
2. **SERVICE_KEY**: Key compartida para autenticación
3. **Repos por rol** (ADR-001): qué roles tienen acceso a cada repo
4. **Verificación VTT**: comando curl para validar token
5. **Onboarding**: proceso de 6 pasos para nuevos agentes
6. **Historial de cambios**: trazabilidad de actualizaciones

## Dependencias

- ADR-001 (`memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md`): define asignación de repos por rol
- VTT API (`http://77.42.88.106:3000`): fuente de verdad para UUIDs y estado de agentes
- `Proyect_data.md` (`.claude/rules/`): fuente de UUIDs y emails usados para poblar este archivo

## Decisiones de diseño

- Ubicado en `_pm/` (material administrativo PM, no docs técnicos)
- SERVICE_KEY incluida explícitamente — todos los roles la necesitan para autenticarse
- Estados iniciales todos `✅ activo` — se actualizarán si algún rol se suspende

## Historial de Cambios

| Fecha | Cambio | Tarea |
|-------|--------|-------|
| 2026-05-02 | Creación inicial con 12 roles | MS-134 |
