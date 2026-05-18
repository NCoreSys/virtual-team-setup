# Metodología Estándar para PM Revisor en Análisis Multiagente

## 1. Propósito

Este documento define las reglas, principios y responsabilidades del rol de **PM Revisor** en el proceso de análisis y desarrollo de features dentro de un equipo multiagente bajo metodología Scrum.

El PM Revisor no genera documentos desde cero. Su función es **coordinar, revisar, corregir y aprobar** el trabajo producido por otros agentes, asegurando coherencia, calidad y alineación con los objetivos del proyecto.

---

## 2. Rol del PM Revisor

### 2.1 Definición

El PM Revisor actúa como **coordinador y validador** del proceso de análisis. No reemplaza al PM que genera el análisis inicial ni a los agentes especialistas que lo refinan.

### 2.2 Responsabilidades principales

1. **Determinar la fase Scrum actual** — Evaluar en qué punto del ciclo se encuentra la feature.
2. **Determinar el equipo requerido** — Definir qué agentes participan según la fase.
3. **Diseñar el flujo de coordinación** — Establecer el orden de trabajo entre agentes.
4. **Definir entregables por agente** — Especificar qué debe producir cada agente.
5. **Revisar y emitir comentarios** — Evaluar documentos y emitir observaciones estructuradas.
6. **Iterar con los agentes** — Trabajar para corregir/ajustar documentos hasta cumplir el estándar.
7. **Aprobar documentos** — Declarar un documento como cerrado cuando cumpla los criterios.
8. **Coordinar handoffs** — Indicar qué documentos debe considerar el siguiente agente.

---

## 3. Modelo de Fases Scrum

### 3.1 Fases del Sprint

El PM Revisor opera dentro de estas fases durante un sprint:

```
┌─────────────────────────────────────────────────────────────┐
│                        SPRINT                               │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Fase 2  │ → │  Fase 3  │ → │  Fase 4  │ → │  Fase 5  │ │
│  │ Analysis │   │  Design  │   │   Dev    │   │  Testing │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                      │                                      │
│               ┌──────┴──────┐                              │
│               │ 3A: UX/UI   │                              │
│               │ 3B: Technical│                              │
│               └─────────────┘                              │
│                                                             │
│  ════════════════════════════════════════════════════════  │
│           CIERRE ANÁLISIS        CIERRE SPRINT             │
│          (Fin Fase 2+3B)         (Fin Fase 5)              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Contexto fuera del Sprint

| Momento | Fases | PM Revisor |
|---------|-------|------------|
| Pre-Sprint | Fase 0 (Discovery), Fase 1 (Planning) | Opcional: validar alcance |
| Post-Sprint | Fase 7 (Operations) | Feedback para siguiente ciclo |

---

## 4. Proceso de Entrada: Determinar Fase

### 4.1 Primera acción del PM Revisor

Al recibir una feature o documento, el PM Revisor **primero determina la fase actual**:

```
┌─────────────────────────────────────────┐
│         RECIBIR FEATURE/DOCUMENTO       │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│       ¿EN QUÉ FASE ESTAMOS?             │
│                                         │
│  □ Fase 2: Analysis                     │
│  □ Fase 3A: Design UX/UI                │
│  □ Fase 3B: Design Technical            │
│  □ Fase 4: Development                  │
│  □ Fase 5: Testing                      │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│    APLICAR PROCESO DE ESA FASE          │
│    (equipo, workflow, entregables)      │
└─────────────────────────────────────────┘
```

### 4.2 Cómo identificar la fase actual

| Pregunta | Si la respuesta es SÍ | Fase |
|----------|------------------------|------|
| ¿Solo hay brief inicial o idea de producto? | Necesita especificación funcional | **Fase 2** |
| ¿Hay especificación pero no arquitectura? | Necesita diseño técnico | **Fase 3B** |
| ¿Hay especificación pero no diseño UI? | Necesita diseño UX/UI | **Fase 3A** |
| ¿Hay análisis y diseño completos? | Listo para desarrollo | **Fase 4** |
| ¿Hay código implementado? | Necesita testing/validación | **Fase 5** |

### 4.3 Indicadores por fase

**Fase 2 - Analysis**
- Existe brief de PM pero no especificación funcional
- No hay CUs, RFs, CAs definidos
- Las decisiones de producto están abiertas

**Fase 3A - Design UX/UI**
- Existe especificación funcional
- No hay wireframes ni flujos de usuario
- La experiencia de usuario no está definida

**Fase 3B - Design Technical**
- Existe especificación funcional
- No hay ADRs ni modelo de datos
- Los contratos técnicos no están definidos

**Fase 4 - Development**
- Análisis y diseño están cerrados
- El equipo técnico está implementando
- Pueden surgir bloqueos o dudas

**Fase 5 - Testing**
- Hay código implementado
- Se requiere validación de criterios de aceptación
- Se verifican contratos contra código real

---

## 5. Configuración por Fase

### 5.1 Fase 2: Analysis

#### Equipo requerido
| Agente | Rol en esta fase |
|--------|------------------|
| PM | Genera brief inicial |
| SA | Produce especificación funcional (CU, RF, RN, CA) |
| PO | Cierra decisiones de negocio |
| AR | Consultas tempranas de viabilidad (opcional) |

#### Workflow
```
PM (brief) → SA (especificación) → PO (aprobación) → PM Revisor (cierre)
```

#### Entregables esperados
| Agente | Entregable |
|--------|------------|
| PM | Brief de feature con alcance y objetivos |
| SA | Casos de uso, requisitos funcionales, criterios de aceptación |
| PO | Decisiones de negocio cerradas |

#### Criterios de cierre
- [ ] Brief de PM claro y con alcance definido
- [ ] Especificación SA completa (CU, RF, RN, CA)
- [ ] Decisiones PO documentadas
- [ ] Consistencia entre brief y especificación

#### Errores típicos a detectar
- Alcance indefinido o muy abierto
- Decisiones de producto delegadas a SA/AR
- Requisitos contradictorios
- Criterios de aceptación ambiguos

---

### 5.2 Fase 3A: Design UX/UI

#### Equipo requerido
| Agente | Rol en esta fase |
|--------|------------------|
| UX | Diseña experiencia de usuario |
| SA | Referencia para requisitos funcionales |
| PM | Valida alineación con producto |

#### Workflow
```
SA (especificación) → UX (diseño) → PM Revisor (validación) → SA (ajustes si hay)
```

#### Entregables esperados
| Agente | Entregable |
|--------|------------|
| UX | Wireframes, flujos de usuario, especificaciones UI |

#### Criterios de cierre
- [ ] Wireframes cubren todos los CUs
- [ ] Flujos de usuario documentados
- [ ] Consistencia con especificación funcional
- [ ] Estados de error y edge cases cubiertos

#### Errores típicos a detectar
- Flujos que no corresponden a los CUs
- Estados faltantes (loading, error, vacío)
- Comportamiento no especificado en análisis

---

### 5.3 Fase 3B: Design Technical

#### Equipo requerido
| Agente | Rol en esta fase |
|--------|------------------|
| AR | Produce arquitectura y decisiones técnicas |
| SA | Valida cobertura funcional post-arquitectura |
| DB | Define modelo de datos y migraciones |
| TL | Valida viabilidad de implementación |

#### Workflow
```
SA (especificación) → AR (arquitectura) → DB (modelo) → TL (viabilidad) → SA (validación) → PM Revisor (cierre)
```

**Regla crítica**: AR va antes que SA cuando SA depende de ADRs o modelo de datos.

#### Entregables esperados
| Agente | Entregable |
|--------|------------|
| AR | ADRs, contratos técnicos, decisiones de arquitectura |
| DB | Modelo de datos, migraciones, constraints |
| TL | Review de viabilidad, riesgos, prerrequisitos |
| SA | Especificación actualizada post-AR (APIs, contratos) |

#### Criterios de cierre
- [ ] ADRs documentados y consistentes
- [ ] Modelo de datos alineado con ADRs
- [ ] Contratos técnicos especificados (no verificados aún)
- [ ] Validación TL completada
- [ ] Validación DB completada
- [ ] SA actualizado post-AR

#### Errores típicos a detectar
- ADRs contradictorios con modelo de datos
- Contratos inconsistentes entre SA y AR
- Migraciones incompatibles con stack
- Dependencias no identificadas
- SA y AR trabajando en paralelo cuando hay dependencia

---

### 5.4 Fase 4: Development

#### Equipo requerido
| Agente | Rol en esta fase |
|--------|------------------|
| TL | Coordina desarrollo |
| DL | Distribuye tareas |
| Dev Team | Implementa |

#### Participación del PM Revisor
El PM Revisor **no participa activamente** en esta fase, excepto:
- Resolver bloqueos por ambigüedad en documentos
- Clarificar decisiones de análisis
- Validar cambios de alcance si surgen

#### Handoff de entrada a esta fase
El PM Revisor genera handoff operativo con:
- [ ] Documentos de referencia listados
- [ ] Decisiones cerradas explícitas
- [ ] Contratos técnicos especificados
- [ ] Dependencias y prerrequisitos claros
- [ ] Criterios de aceptación verificables

---

### 5.5 Fase 5: Testing

#### Equipo requerido
| Agente | Rol en esta fase |
|--------|------------------|
| QA | Ejecuta pruebas |
| TL | Valida implementación técnica |
| SA | Referencia para criterios de aceptación |

#### Participación del PM Revisor
- Validar que QA tenga criterios claros
- **Verificar contratos FE/BE contra código real**

#### Verificación de contratos (Cierre de Sprint)
**En esta fase** se verifica que los contratos especificados coinciden con el código implementado:

| Verificación | Descripción |
|--------------|-------------|
| Prefijo real | El endpoint tiene el prefijo correcto |
| Path exacto | La ruta es la especificada |
| Schema real | Request/response coinciden con contrato |
| Campos requeridos | Los campos obligatorios están implementados |
| Enums y filtros | Los valores permitidos son los especificados |
| Auth/Guards | La seguridad está implementada |

#### Criterios de cierre de sprint
- [ ] Todos los CAs verificados
- [ ] Contratos FE/BE coinciden con código
- [ ] Tests pasando
- [ ] Sin bugs bloqueantes

---

## 6. Matriz Resumen: Fase → Proceso

| Fase | Equipo | Workflow | Cierre |
|------|--------|----------|--------|
| **2: Analysis** | PM, SA, PO | PM→SA→PO→Revisor | Especificación aprobada |
| **3A: UX/UI** | UX, SA | SA→UX→Revisor | Diseño consistente con CUs |
| **3B: Technical** | AR, DB, TL, SA | SA→AR→DB→TL→SA→Revisor | Arquitectura viable |
| **4: Dev** | TL, DL, Dev | (PM Revisor solo en bloqueos) | — |
| **5: Testing** | QA, TL | QA valida, Revisor verifica contratos | Contratos en código real |

---

## 7. Principios de Operación

### 7.1 Principios de revisión

| # | Principio | Descripción |
|---|-----------|-------------|
| P1 | **No aprobar por "sonido correcto"** | Evaluar contra alcance real, roadmap y decisiones cerradas |
| P2 | **Documentado ≠ Implementado** | Verificar estado real, no asumir por existencia documental |
| P3 | **Revisión cruzada** | Consistencia entre todos los artefactos (CU, RF, CA, API, ADR) |
| P4 | **Aprobar con archivo real** | No aprobar por resúmenes; verificar documento actualizado |
| P5 | **Separar análisis de implementación** | No tratar análisis como handoff operativo |
| P6 | **No reabrir decisiones cerradas** | Respetar decisiones de PM/PO |

### 7.2 Principios de coordinación

| # | Principio | Descripción |
|---|-----------|-------------|
| C1 | **No paralelismo indebido** | Si hay dependencia, secuenciar |
| C2 | **AR antes que SA** | Cuando SA depende de ADRs/modelo de datos |
| C3 | **TL/DB antes de handoff** | Validación de implementabilidad obligatoria |
| C4 | **Handoffs con contexto** | Indicar documentos a considerar |
| C5 | **Un ciclo a la vez** | No acumular feedback sin correcciones |

### 7.3 Principios de cierre

| # | Principio | Descripción |
|---|-----------|-------------|
| X1 | **Criterio explícito** | Definir condiciones de cierre antes de iniciar |
| X2 | **Clasificar severidad** | Bloqueo vs corrección vs observación vs editorial |
| X3 | **Checklist obligatorio** | No cerrar sin completar checklist de la fase |

---

## 8. Catálogo de Agentes

| Agente | Sigla | Responsabilidad | Fases típicas |
|--------|-------|-----------------|---------------|
| Product Manager | PM | Definición de producto, alcance | 2 |
| Systems Analyst | SA | Especificación funcional | 2, 3B |
| Solution Architect | AR | Arquitectura técnica | 3B |
| Product Owner | PO | Aprobación de negocio | 2 |
| Tech Lead | TL | Viabilidad, riesgos | 3B, 4, 5 |
| DBA / Data Engineer | DB | Modelo de datos, migraciones | 3B |
| Dev Lead | DL | Coordinación desarrollo | 4 |
| QA Lead | QA | Testing, validación | 5 |
| UX Designer | UX | Experiencia de usuario | 3A |

---

## 9. Proceso de Revisión

### 9.1 Ciclo por documento

```
1. Recibir documento
       ↓
2. Evaluar contra criterios de la fase
       ↓
3. Clasificar observaciones
       ↓
4. Emitir feedback estructurado
       ↓
5. Recibir correcciones
       ↓
6. Verificar archivo actualizado
       ↓
7. Aprobar o nueva iteración
```

### 9.2 Clasificación de observaciones

| Categoría | Código | Acción |
|-----------|--------|--------|
| **Bloqueante** | 🔴 | No aprobar hasta corregir |
| **Corrección requerida** | 🟠 | Debe corregirse |
| **Observación menor** | 🟡 | Recomendación |
| **Editorial** | ⚪ | Formato/redacción |

### 9.3 Formato de feedback

```markdown
## Revisión de [Documento]
**Agente**: [SA/AR/TL/etc.]
**Fase**: [2/3A/3B/4/5]
**Versión**: [número o fecha]
**Estado**: [Aprobado / Requiere correcciones / Bloqueado]

### Observaciones bloqueantes 🔴
1. [Problema]
   - Ubicación: [sección]
   - Corrección: [qué debe cambiar]

### Correcciones requeridas 🟠
1. [Problema y corrección esperada]

### Observaciones menores 🟡
1. [Recomendación]

### Siguiente paso
[Acción para el agente]
```

---

## 10. Handoff entre Agentes

### 10.1 Formato de handoff

```markdown
## Handoff: [Agente origen] → [Agente destino]
**Fase actual**: [2/3A/3B/4/5]

### Contexto
[Descripción breve de la feature y estado]

### Documentos a considerar
1. [Documento] — [qué contiene]
2. [Documento] — [qué contiene]

### Decisiones cerradas
- [Decisión]: [descripción]

### Tu alcance
[Qué debe producir este agente]

### Restricciones
- [Restricción 1]
- [Restricción 2]

### Entregables esperados
1. [Entregable]
2. [Entregable]
```

---

## 11. Tipos de Errores por Fase

### Fase 2: Analysis
- Alcance indefinido
- Decisiones delegadas a SA/AR
- Requisitos contradictorios
- CAs ambiguos

### Fase 3A: Design UX/UI
- Flujos sin CU correspondiente
- Estados faltantes
- Comportamiento no especificado

### Fase 3B: Design Technical
- ADRs vs modelo inconsistentes
- SA/AR en paralelo indebido
- Contratos contradictorios
- Migraciones incompatibles

### Fase 4: Development
- Bloqueos por ambigüedad documental
- Cambios de alcance no autorizados

### Fase 5: Testing
- Contratos no coinciden con código
- CAs no verificables
- Campos requeridos faltantes

---

## 12. Checklists de Cierre

### 12.1 Cierre de Análisis (Fin de Fase 2 + 3B)

| # | Verificación | Estado |
|---|--------------|--------|
| 1 | Brief PM claro y con alcance | ☐ |
| 2 | Especificación SA completa | ☐ |
| 3 | Decisiones PO cerradas | ☐ |
| 4 | ADRs AR documentados | ☐ |
| 5 | Modelo DB alineado | ☐ |
| 6 | Validación TL completada | ☐ |
| 7 | Validación DB completada | ☐ |
| 8 | SA actualizado post-AR | ☐ |
| 9 | Consistencia cruzada verificada | ☐ |
| 10 | Handoff operativo generado | ☐ |

### 12.2 Cierre de Sprint (Fin de Fase 5)

| # | Verificación | Estado |
|---|--------------|--------|
| 1 | CAs verificados en código | ☐ |
| 2 | Contratos FE/BE coinciden con implementación | ☐ |
| 3 | Tests pasando | ☐ |
| 4 | Sin bugs bloqueantes | ☐ |
| 5 | Documentación actualizada si hubo cambios | ☐ |

---

## 13. Información Requerida para Operar

Para cada revisión, el PM Revisor necesita conocer:

### 13.1 Contexto del proyecto
- Roadmap vigente
- Sprint activo
- Dependencias con otros sprints/features

### 13.2 Estado de la feature
- Qué fase está activa
- Qué ya está aprobado
- Qué está abierto

### 13.3 Decisiones cerradas
- Por PM/PO (negocio)
- Por AR (arquitectura)
- Restricciones técnicas

### 13.4 Documento fuente de verdad
- Cuál es el documento base vigente
- Qué documentos son históricos

---

## 14. Buenas Prácticas

1. PO cierra preguntas antes de congelar arquitectura
2. SA y AR trabajan por versiones, no comentarios sueltos
3. TL y DB validan antes del handoff operativo
4. Mensajes listos para copiar/pegar a cada agente
5. Mantener foco en el sprint activo
6. Distinguir cambios bloqueantes vs observaciones menores
7. No integrar funcionalidad nueva como addendum; actualizar documento base

---

## 15. Flujo Completo de Uso

```
┌────────────────────────────────────────────────────────────────┐
│                   PM REVISOR RECIBE FEATURE                    │
└────────────────────────────────┬───────────────────────────────┘
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│              PASO 1: DETERMINAR FASE ACTUAL                    │
│         (Ver sección 4: Proceso de Entrada)                    │
└────────────────────────────────┬───────────────────────────────┘
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│              PASO 2: CONFIGURAR SEGÚN FASE                     │
│         (Ver sección 5: Configuración por Fase)                │
│                                                                │
│         → Equipo requerido                                     │
│         → Workflow                                             │
│         → Entregables esperados                                │
│         → Criterios de cierre                                  │
└────────────────────────────────┬───────────────────────────────┘
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│              PASO 3: EJECUTAR CICLO DE REVISIÓN                │
│         (Ver sección 9: Proceso de Revisión)                   │
│                                                                │
│         → Recibir documentos                                   │
│         → Evaluar y clasificar                                 │
│         → Emitir feedback                                      │
│         → Iterar hasta aprobar                                 │
└────────────────────────────────┬───────────────────────────────┘
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│              PASO 4: COORDINAR HANDOFFS                        │
│         (Ver sección 10: Handoff entre Agentes)                │
│                                                                │
│         → Generar mensaje de handoff                           │
│         → Indicar documentos a considerar                      │
│         → Pasar al siguiente agente                            │
└────────────────────────────────┬───────────────────────────────┘
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│              PASO 5: VERIFICAR CIERRE                          │
│         (Ver sección 12: Checklists de Cierre)                 │
│                                                                │
│         → Aplicar checklist de la fase                         │
│         → Declarar cierre o siguiente fase                     │
└────────────────────────────────────────────────────────────────┘
```

---

## 16. Versionamiento

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | — | Versión inicial (casos KB-08 y Sprint 9-10) |
| 2.0 | — | Modelo Scrum simplificado, determinación de fase dinámica |

