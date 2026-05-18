---
name: filtrar-fases
description: Filtra el catálogo SDLC (438 deliverables) para determinar cuáles aplican al proyecto actual, generando el documento FASES_APLICABLES con criterios explícitos por fase.
role: PM
vtt_version: "1.0"
---

# Skill: /filtrar-fases

## Propósito
Ejecuta el filtro del catálogo SDLC de 438 deliverables para determinar cuáles aplican al proyecto actual. Genera `FASES_APLICABLES_[PROYECTO].md` con criterio documentado por cada exclusión.

## Cuándo usar
- Al iniciar el proceso PM, después de tener la SPEC aprobada y ADR-001 firmado
- Antes de generar el PRE_HANDOFF de iniciación
- Equivale al PASO 2 del proceso PM estándar

## Inputs requeridos
Antes de ejecutar, leer:
1. SPEC del proyecto (versión APPROVED PM)
2. ADR-001 de estrategia de repositorios (si aplica)
3. Stack tecnológico definido
4. Composición del equipo (roles activos)

## Pasos de ejecución

### 1. Cargar catálogo base
El catálogo SDLC tiene 438 deliverables distribuidos en 9 fases:
- Phase 0: Project Setup (setup físico — repos, herramientas)
- Phase 1: Planning (plan de proyecto, roadmap)
- Phase 2: Analysis (discovery, requisitos)
- Phase 3: Design (arquitectura, diseño técnico y UX)
- Phase 4: Development (implementación)
- Phase 5: Testing (QA, performance, seguridad)
- Phase 6: Deploy (infraestructura, CI/CD, release)
- Phase 7: Operations (monitoreo, soporte)
- Phase 8: Closure (documentación final, retrospectiva)

### 2. Aplicar filtros por criterio

Para cada deliverable, evaluar:

**APLICA si:**
- El stack del proyecto usa la tecnología que cubre ese deliverable
- El rol responsable está activo en el equipo
- El riesgo que mitiga es relevante para el alcance del proyecto

**NO APLICA si:**
- La tecnología no está en el stack (ej: deliverable de iOS en proyecto web)
- El rol no existe en el equipo (ej: Mobile Dev en equipo BE+FE web)
- El deliverable es para un modelo de negocio diferente (ej: marketplace en proyecto interno)
- Ya está cubierto por otro deliverable más específico

### 3. Documentar criterios de exclusión
Para cada deliverable excluido, registrar el criterio. Agrupar exclusiones por criterio común.

Ejemplo del caso Memory Service (referencia):
- Criterio E1: "No es app móvil" → excluyó 48 deliverables de iOS/Android
- Criterio E2: "Microservicio interno sin portal de cliente" → excluyó 31 de UX externo
- Criterio E3: "Sin modelo freemium/marketplace" → excluyó 19 de billing/payments

### 4. Generar documento

Estructura del output `FASES_APLICABLES_[PROYECTO].md`:

```markdown
# Fases y Deliverables Aplicables — [PROYECTO]

## Resumen ejecutivo
- Total catálogo: 438
- Aplican: [N]
- Excluidos: [438-N]

## Criterios de exclusión aplicados
| Código | Criterio | Deliverables excluidos |
|--------|----------|----------------------|
| E1 | [razón] | [N] |
...

## Detalle por fase
### Phase 0: Project Setup
| ID | Deliverable | Aplica | Criterio exclusión |
|----|-------------|--------|-------------------|
...
```

### 5. Validar coherencia
- El total de APLICA + NO_APLICA debe sumar 438
- Cada exclusión debe tener criterio documentado
- Revisar que no excluyó deliverables críticos (testing, seguridad básica, documentación)

## Output generado
- `Release[X]/01-PM/FASES_APLICABLES_[PROYECTO].md`

## Referencia
- Caso Memory Service: 390/438 aplican — ver `Release2.0/01-PM/FASES_APLICABLES_MEMORY_SERVICE.md`
- Template base: `.vtt/templates/setup/pm/TEMPLATE_FASES_APLICABLES_V1.0.md`
