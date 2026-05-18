---
name: analizar-spec
description: Analiza la SPEC del proyecto para extraer decisiones técnicas, detectar gaps, validar coherencia con ADR y generar el resumen ejecutivo que el PM necesita para iniciar el proceso de cierre.
role: PM
vtt_version: "1.0"
---

# Skill: /analizar-spec

## Propósito
Lee y analiza la SPEC del proyecto, extrae las decisiones técnicas congeladas (D-XXX),
detecta gaps o inconsistencias, y valida coherencia con el ADR de repositorios.
Produce el resumen que alimenta el CONSOLIDADO y el HO PJM.

## Cuándo usar
- Al iniciar el análisis PM (PASO 1 del proceso estándar)
- Cuando el PM recibe una SPEC nueva o una nueva versión
- Antes de ejecutar /filtrar-fases

## Inputs requeridos
1. SPEC del proyecto (archivo .md con versión APPROVED o pendiente)
2. ADDENDUM si existe (cambios post-SPEC)
3. ADR-001 si ya está firmado

## Pasos de ejecución

### 1. Leer la SPEC completa
Identificar y extraer:
- Stack tecnológico (lenguajes, frameworks, BDs, infra)
- Decisiones técnicas congeladas (sección D-XXX o equivalente)
- SLAs y contratos de performance (ej: <500ms en endpoints críticos)
- Modelo de datos principal (entidades, relaciones)
- Integraciones externas requeridas
- Roles de usuario del sistema
- Restricciones y non-goals explícitos

### 2. Detectar gaps o ambigüedades

Marcar como GAP cuando:
- Un componente se menciona pero no tiene spec de implementación
- Hay contradicción entre dos secciones
- Un SLA no tiene mécanismo de medición definido
- Una integración externa no tiene contrato de API definido

Formato de GAP:
```
GAP-[N]: [Sección] — [Descripción del gap] — Impacto: Alto/Medio/Bajo
```

### 3. Validar coherencia con ADR-001

Si ADR-001 existe, verificar:
- ¿La SPEC menciona módulos que cruzan el límite de repos? → requiere contrato API explícito
- ¿Los roles de la SPEC están mapeados a los roles del equipo?
- ¿El modelo de datos está distribuido correctamente entre repos?

### 4. Catalogar decisiones técnicas

Generar tabla de decisiones en formato estándar:
```
| ID | Área | Decisión | Justificación | Revisable |
|----|------|----------|---------------|-----------|
| D-[PROY]-01 | Stack | Node.js 20 + TypeScript | ... | No |
```

### 5. Producir resumen ejecutivo

Output: sección "Estado de la SPEC" con:
- Versión analizada y estado (APPROVED / DRAFT / PENDING)
- N decisiones técnicas congeladas
- N GAPs detectados (con severidad)
- Coherencia con ADR: OK / REQUIERE_AJUSTE
- Recomendación: PROCEDER / RESOLVER_GAPS_PRIMERO

## Output generado
Sección inline en el mensaje de respuesta. No genera archivo — el resumen se integra
al CONSOLIDADO en el paso siguiente.

## Lección aprendida (Memory Service)
La SPEC tuvo un ADDENDUM v1.1 que agregó `platformRefs` al modelo de datos
y un índice GIN a PostgreSQL. El análisis inicial sin el ADDENDUM estaba incompleto.
**Siempre buscar ADDENDUMs antes de declarar la SPEC como "leída".**

## Referencia
- Caso Memory Service: SPEC v1.9 + ADDENDUM v1.1 → 48 decisiones congeladas (D-MEM-01..43 + D-INT-01..05)
- Ruta: `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`
