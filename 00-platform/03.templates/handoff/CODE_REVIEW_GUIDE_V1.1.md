# GUÍA DE CODE REVIEW

**Documento:** CODE_REVIEW_GUIDE.md  
**Versión:** 1.1  
**Fecha:** 2026-03-30  
**Autor:** PJM-Agent  
**Aplica a:** Todos los proyectos con equipo de agentes  
**Estado:** 📋 ESTÁNDAR OBLIGATORIO

---

## 0. PROPÓSITO

Esta guía define el proceso estándar de Code Review para equipos de agentes virtuales. Es un documento **cross-sprint** que explica **cómo** hacer code review — los handoffs de cada sprint definen **qué** revisar.

> **Regla fundamental:** Code Review es OBLIGATORIO antes de cada merge. No hay excepción.

> **Alcance:** Este documento cubre Code Review técnico (calidad de código, tests, seguridad). 
> DL-REVIEW (validación visual de implementación FE vs HTMLs) es proceso separado — 
> ver `METODOLOGIA_EJECUCION_SPRINTS.md §3.3`.

---

## 1. PROCESO DE CODE REVIEW

### 1.1 Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                     FLUJO DE CODE REVIEW                        │
└─────────────────────────────────────────────────────────────────┘

    Developer                    Reviewer                  Merge
        │                           │                        │
        │   1. Crear PR             │                        │
        │   ───────────────────────►│                        │
        │   • Descripción           │                        │
        │   • Link a tarea          │                        │
        │   • Tests pasando         │                        │
        │   • Screenshots (FE)      │                        │
        │                           │                        │
        │                           │ 2. Review usando       │
        │                           │    checklist §3        │
        │                           │                        │
        │   3. Resolver             │                        │
        │◄──────────────────────────│ Comentarios            │
        │   comentarios             │                        │
        │                           │                        │
        │   4. Push fixes           │                        │
        │   ───────────────────────►│                        │
        │                           │                        │
        │                           │ 5. Re-review           │
        │                           │                        │
        │                           │ 6. Approve             │
        │                           │─────────────────────────►│
        │                           │                        │ 7. Merge
```

### 1.2 Modelo Escalonado por Tamaño de PR

| Tamaño PR | Líneas | Reviewer | Tiempo máximo | Escalación |
|-----------|--------|----------|---------------|------------|
| Hotfix | Cualquiera | TL | 2 horas | PJM |
| Pequeño | < 100 | TL solo | 4 horas | PJM |
| Mediano | 100-500 | TL + Code Reviewer | 8 horas | PJM |
| Grande | > 500 | Code Reviewer obligatorio | 24 horas | PJM + AR |
| Arquitectura | Cualquiera con ADR | Code Reviewer + AR | 24 horas | PM |

### 1.3 Árbol de Decisión

```
PR creado
    │
    ▼
¿Es hotfix?
    │
    ├── Sí → TL solo (2h max)
    │
    └── No → ¿Tiene ADR asociado?
                │
                ├── Sí → Code Reviewer + AR obligatorios
                │
                └── No → ¿Cuántas líneas?
                            │
                            ├── < 100 → TL solo (4h max)
                            │
                            ├── 100-500 → TL + Code Reviewer (8h max)
                            │
                            └── > 500 → Code Reviewer obligatorio (24h max)
```

---

## 2. ROLES Y RESPONSABILIDADES

### 2.1 Matriz de Reviewers

| Tipo de PR | Reviewer Principal | Reviewer Secundario |
|------------|-------------------|---------------------|
| BE (endpoints, services) | **TL** | Otro BE dev |
| FE (componentes, páginas) | **TL** | Otro FE dev |
| DB (migraciones) | **TL** + **DB Lead** | — |
| Infra (DO) | **TL** | — |
| Cross-cutting (auth, integración) | **TL** | AR (si aplica) |

> **TL es el reviewer obligatorio de todo PR.** Puede delegar revisión técnica a otro dev, pero el sign-off final es del TL.

### 2.2 Responsabilidades por Rol

**Developer (autor del PR):**
- Crear PR con descripción completa
- Vincular a tarea VTT
- Asegurar que tests pasan antes de solicitar review
- Responder comentarios en < 4 horas
- No hacer merge sin aprobación

**TL (reviewer principal):**
- Revisar usando checklist completo
- Aprobar o solicitar cambios en tiempo establecido
- Escalar si encuentra issues de arquitectura
- Sign-off final obligatorio

**Code Reviewer (externo):**
- Revisión técnica profunda
- Enfoque en calidad de código y patrones
- Puede bloquear merge si encuentra issues críticos

**AR (cuando aplica):**
- Verifica que código respeta ADRs
- Revisa boundaries y arquitectura
- Puede bloquear merge si hay violaciones arquitectónicas

---

## 3. CHECKLISTS DE REVIEW

### 3.1 Checklist Backend

```markdown
## Code Review Checklist — Backend

### 📋 Funcionalidad
- [ ] Implementa el requisito según tarea asignada
- [ ] Endpoint sigue contrato definido en API_CONTRACT.md
- [ ] Tests unitarios presentes y pasan
- [ ] Tests de integración presentes (si es endpoint nuevo)
- [ ] No hay lógica hardcodeada que debería venir de config/DB

### 🔗 Integración
- [ ] Routing sigue patrones existentes
- [ ] Usa dependencias de inyección correctamente
- [ ] Manejo de errores sigue patrón estándar
- [ ] Logging apropiado en operaciones críticas

### ✅ Calidad de Código
- [ ] Sin código comentado innecesario
- [ ] Nombres descriptivos (variables, funciones, clases)
- [ ] Sin duplicación obvia (DRY)
- [ ] Complejidad razonable (funciones < 50 líneas)
- [ ] Docstrings/comentarios en funciones públicas
- [ ] Type hints presentes (si TypeScript/Python)

### 🔒 Seguridad
- [ ] Endpoints protegidos requieren autenticación
- [ ] No hay secrets hardcodeados
- [ ] Input validado antes de usar
- [ ] Sin SQL injection posible (usa ORM o params)
- [ ] Autorización: usuario solo accede a sus recursos

### ⚡ Performance
- [ ] No hay N+1 queries obvios
- [ ] Queries usan índices apropiados
- [ ] No hay fetches redundantes
- [ ] Operaciones pesadas son async cuando aplica

### 📊 Observabilidad
- [ ] Errores loggeados con contexto suficiente
- [ ] Métricas relevantes expuestas (si aplica)
```

### 3.2 Checklist Frontend

```markdown
## Code Review Checklist — Frontend

### 📋 Funcionalidad
- [ ] Implementa el requisito visual según spec de DL
- [ ] Componentes funcionan en estados: idle, loading, error, success
- [ ] Interacciones responden correctamente
- [ ] Tests de componentes presentes

### 🔗 Integración
- [ ] Routing sigue patrones definidos
- [ ] Estado usa hooks/stores correctamente
- [ ] Llamadas API usan el cliente centralizado
- [ ] Manejo de errores sigue patrón estándar

### ✅ Calidad de Código
- [ ] Sin código comentado innecesario
- [ ] Nombres descriptivos (componentes, props, handlers)
- [ ] Sin duplicación obvia
- [ ] Componentes < 200 líneas (dividir si más grande)
- [ ] Props tipadas con TypeScript
- [ ] No hay `any` innecesarios

### ♿ Accesibilidad
- [ ] Elementos interactivos tienen labels
- [ ] Keyboard navigation funciona
- [ ] Color contrast cumple WCAG AA
- [ ] ARIA labels donde aplica

### 🎨 UI/UX
- [ ] Sigue design tokens definidos
- [ ] Responsive funciona en mobile/tablet/desktop
- [ ] Estados de carga son claros
- [ ] Errores son informativos

### ⚡ Performance
- [ ] No hay re-renders innecesarios
- [ ] useMemo/useCallback donde aplica
- [ ] No hay fetches en cada render
- [ ] Images optimizadas
```

### 3.3 Checklist Database

```markdown
## Code Review Checklist — Migraciones

### 📋 Funcionalidad
- [ ] Schema coincide con MODELO_DATOS.md
- [ ] Nombres de tablas/columnas siguen convención (snake_case)
- [ ] Tipos de datos correctos
- [ ] Constraints implementados (FK, UNIQUE, CHECK)

### 🔒 Seguridad de Datos
- [ ] Migración es reversible (tiene downgrade)
- [ ] No hay pérdida de datos en upgrade
- [ ] Seeds no contienen datos sensibles

### ⚡ Performance
- [ ] Índices creados para columnas de búsqueda frecuente
- [ ] No hay operaciones que bloqueen tablas grandes

### ✅ Operacional
- [ ] Migración probada en entorno local
- [ ] Dependencias de migración correctas
- [ ] Seed data completo y válido
```

---

## 4. TEMPLATES DE PR

### 4.1 Template Backend

```markdown
## Descripción
[Breve descripción del cambio]

## Tipo de cambio
- [ ] Nueva funcionalidad
- [ ] Bug fix
- [ ] Refactoring
- [ ] Documentación

## Tarea VTT
- ID: [ID de tarea]
- Link: [URL]

## Cambios realizados
- [Lista de cambios principales]

## Tests
- [ ] Unit tests agregados/actualizados
- [ ] Integration tests agregados/actualizados
- [ ] Tests pasan localmente

## Checklist
- [ ] Código sigue guías de estilo
- [ ] Self-review realizado
- [ ] Documentación actualizada (si aplica)
- [ ] .LOGIC.md actualizado

## Screenshots (si aplica)
[Screenshots de Swagger/Postman]

## Notas para reviewer
[Áreas específicas donde necesitas feedback]
```

### 4.2 Template Frontend

```markdown
## Descripción
[Breve descripción del cambio]

## Tipo de cambio
- [ ] Nueva funcionalidad
- [ ] Bug fix
- [ ] Refactoring
- [ ] Estilos

## Tarea VTT
- ID: [ID de tarea]
- Link: [URL]

## Cambios realizados
- [Lista de cambios principales]

## Tests
- [ ] Tests de componentes agregados
- [ ] Tests pasan localmente

## Screenshots
### Desktop
[Screenshot desktop]

### Mobile
[Screenshot mobile]

## Checklist
- [ ] Responsive verificado
- [ ] Accesibilidad verificada (keyboard nav, labels)
- [ ] Self-review realizado
- [ ] .LOGIC.md actualizado (por cada archivo creado/modificado)

## Notas para reviewer
[Áreas específicas donde necesitas feedback]
```

---

## 5. SISTEMA DE COMENTARIOS

### 5.1 Prefijos de Comentarios

| Prefijo | Significado | Acción requerida |
|---------|-------------|------------------|
| `🔴 BLOCKER:` | Issue que impide merge | Fix obligatorio |
| `🟡 SUGGESTION:` | Mejora recomendada | Discutir o implementar |
| `🟢 NIT:` | Detalle menor | Opcional |
| `❓ QUESTION:` | Necesito entender | Responder |
| `💡 IDEA:` | Idea para futuro | No bloquea, considerar |

### 5.2 Ejemplos de Comentarios

```
🔴 BLOCKER: Este endpoint no tiene autenticación.
Agregar middleware de auth antes de procesar.

🟡 SUGGESTION: Considera extraer esta lógica a un helper.
Facilitaría testing y reutilización.

🟢 NIT: Typo en el nombre de la variable: "reccomendation" → "recommendation"

❓ QUESTION: ¿Por qué usamos esta constante aquí?
¿Hay alguna restricción de negocio?

💡 IDEA: Para el siguiente sprint, podríamos cachear este resultado.
```

---

## 6. RESOLUCIÓN DE CONFLICTOS

### 6.1 Proceso de Escalación

```
Conflicto Developer ↔ Reviewer
           │
           ▼
    ¿Es tema técnico?
     /            \
   Sí              No
    │               │
    ▼               ▼
  TL decide     PJM media
    │               │
    ▼               ▼
¿Tema de         Decisión
arquitectura?    final
     │
    Sí
     │
     ▼
  AR decide
```

### 6.2 Reglas de Resolución

1. **Documentación gana:** Si hay decisión documentada en ADR/handoff, esa es la respuesta
2. **Tests prueban:** Si hay test que demuestra comportamiento esperado, el test define
3. **TL tiene última palabra** en temas técnicos dentro del sprint
4. **AR tiene última palabra** en temas de arquitectura transversal

---

## 7. MÉTRICAS DE CODE REVIEW

### 7.1 Métricas a Trackear

| Métrica | Objetivo | Alerta si |
|---------|----------|-----------|
| Tiempo promedio de review | < 4 horas | > 8 horas |
| % PRs con review completo | 100% | < 100% |
| # comentarios por PR | 3-10 | > 20 (PR muy grande) |
| % PRs aprobados primera vez | > 60% | < 40% |
| Defectos encontrados post-merge | < 2/sprint | > 5/sprint |

### 7.2 Template de Reporte Semanal

```markdown
## Code Review Report — Semana [X]

### Resumen
- PRs creados: XX
- PRs mergeados: XX
- Tiempo promedio de review: X horas

### Por Reviewer
| Reviewer | PRs revisados | Comentarios | Tiempo promedio |
|----------|---------------|-------------|-----------------|
| TL       | XX            | XX          | X horas         |
| CR       | XX            | XX          | X horas         |

### Issues Detectados
- Blockers encontrados: X
- Bugs prevenidos: X

### Áreas de Mejora
- [Lista de patrones problemáticos recurrentes]
```

---

## 8. ANTI-PATRONES A EVITAR

### 8.1 Anti-patrones del Autor

| Anti-patrón | Por qué es malo | Qué hacer |
|-------------|-----------------|-----------|
| PR de >500 líneas | Imposible de revisar bien | Dividir en PRs más pequeños |
| Sin descripción | Reviewer pierde tiempo entendiendo | Usar template |
| Tests faltantes | Bugs pasan a producción | Escribir tests primero |
| Force push durante review | Pierde contexto de conversación | Commits adicionales |
| No responder comentarios | Bloquea el proceso | Responder en < 4h |

### 8.2 Anti-patrones del Reviewer

| Anti-patrón | Por qué es malo | Qué hacer |
|-------------|-----------------|-----------|
| Rubber stamp (aprobar sin revisar) | Bugs pasan | Usar checklist |
| Nitpicking excesivo | Desmotiva, retrasa | Priorizar blockers |
| Review después de días | Bloquea al equipo | Respetar timeouts |
| Solo criticar | Ambiente tóxico | Reconocer lo bueno también |
| No explicar el "por qué" | No hay aprendizaje | Siempre dar contexto |

---

## 9. INTEGRACIÓN CON VTT

### 9.1 Estados de Tarea Durante Code Review

```
task_in_progress
       │
       │  Developer crea PR
       ▼
task_in_review
       │
       ├── 🔴 Changes requested → Developer corrige → permanece en task_in_review
       │
       ├── 🐛 Issue detectado → POST /api/tasks/{id}/issues → task_on_hold
       │       │
       │       └── Fix resuelto → PUT /api/issues/{id} → vuelve a task_in_review
       │
       └── ✅ Approved + Merged → task_completed
```

### 9.2 Tareas de Review en VTT

| ID Típico | Descripción | Agente | Estimado |
|-----------|-------------|--------|----------|
| TL-XXX | Code Review PRs [área] | TL | 2-4h |
| CR-XXX | Code Review externo | CR | 2-4h |
| AR-XXX | Review arquitectura | AR | 2h |

---

## 10. APÉNDICE: CHECKLIST RÁPIDO

### Pre-PR (Developer)

```
[ ] Tests pasan localmente
[ ] Linting sin errores
[ ] Descripción completa
[ ] Link a tarea VTT
[ ] Self-review realizado
[ ] .LOGIC.md actualizado (si aplica)
```

### Durante Review (Reviewer)

```
[ ] Checklist del §3 aplicado
[ ] Comentarios con prefijos correctos
[ ] Blockers claramente marcados
[ ] Feedback constructivo
```

### Post-Review (Developer)

```
[ ] Todos los comentarios respondidos
[ ] Blockers resueltos
[ ] Tests siguen pasando
[ ] Re-request review si hubo cambios significativos
```

---

## 11. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-03-30 | PJM-Agent | Versión inicial estandarizada |
| 1.1 | 2026-03-30 | PJM-Agent | Correcciones: árbol decisión con rama Hotfix, nota DL-REVIEW en §0, .LOGIC.md en template FE, task_on_hold en diagrama estados |

---

**FIN DEL DOCUMENTO**
