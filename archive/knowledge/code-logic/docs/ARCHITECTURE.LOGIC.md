# Code Logic — docs/ARCHITECTURE.md

**Archivo de código**: `docs/ARCHITECTURE.md`
**Tarea**: MS-140
**Fecha**: 2026-05-04

---

## Propósito

Documento de arquitectura de alto nivel del Memory Service R1. Sirve como punto de entrada para onboarding rápido (~5 minutos) y referencia a la fuente de verdad completa (SPEC v1.9).

## Contenido y Flujo Lógico

El documento es estático (no contiene lógica ejecutable). Estructura:

1. **Visión General** — qué es Memory Service y qué problema resuelve
2. **Componentes Principales** — diagrama ASCII + tabla de sub-componentes
3. **Stack Tecnológico** — tabla de dependencias con versiones y puertos
4. **Repositorios** — mapeo de repos a responsabilidades
5. **Flujo de Importación** — 5 pasos del proceso de import
6. **Flujo de Contexto Runtime** — SLA <500ms explicado
7. **Decisiones Clave** — 5 D-MEM cerradas, no renegociables
8. **Documentación Completa** — links al SPEC v1.9

## Dependencias Importantes

- SPEC v1.9 (`Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`) — fuente de verdad
- `docs/INFRASTRUCTURE.md` — documento hermano con datos de infraestructura

## Decisiones de Diseño

- NO duplica el SPEC: el SPEC tiene 43 decisiones cerradas, schema BD, contratos API. Este documento solo referencia.
- Diagrama ASCII elegido sobre Mermaid para compatibilidad universal (GitHub, editores de texto, PDF).
- Incluye solo 5 decisiones D-MEM críticas — las que afectan el diseño del backend más profundamente.
