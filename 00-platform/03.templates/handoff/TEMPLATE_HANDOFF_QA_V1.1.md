# HANDOFF QA: [PROYECTO] — Sprint [N]

**Documento:** HANDOFF_QA_SPRINT_[N].md  
**Versión:** 1.1  
**De:** PJM-Agent  
**Para:** QA (QA Engineer)  
**Fecha:** [YYYY-MM-DD]  
**Sprint:** [N] — [Nombre del Sprint]  
**Estado:** 📋 BLOCKED (espera FE completado)  
**Prerrequisitos:** FE completado, DL-REVIEW aprobado

---

## 0. RESUMEN EJECUTIVO

[2-3 párrafos describiendo:]
- Objetivo de testing del sprint
- Qué funcionalidades se van a validar
- Flujos críticos a testear
- Riesgos específicos a cubrir

**Duración total:** [X] horas  
**Escenarios BE:** [N]  
**Escenarios FE:** [N]  
**QA-FLOW scenarios:** [N]

---

## 1. ESTRATEGIA DE TESTING

### 1.1 Cobertura Requerida

| Capa | Objetivo | Herramienta |
|------|----------|-------------|
| Unit BE | ≥ 70% | Jest/pytest |
| Unit FE | ≥ 60% | Jest/Vitest |
| Integration | 100% endpoints | Supertest |
| E2E | Flujos críticos | Playwright |

### 1.2 Priorización

| Prioridad | Descripción | Ejemplo |
|-----------|-------------|---------|
| P0 | Bloquea uso del sistema | Login, flujo principal |
| P1 | Feature crítica | CRUD principal |
| P2 | Feature secundaria | Filtros, ordenamiento |
| P3 | Nice to have | Animaciones, tooltips |

---

## 2. ESCENARIOS BACKEND

### 2.1 Resumen de Endpoints

| Endpoint | Método | Casos | Prioridad |
|----------|--------|-------|-----------|
| `/api/[recurso]` | GET | 4 | P1 |
| `/api/[recurso]` | POST | 5 | P0 |
| `/api/[recurso]/:id` | PATCH | 4 | P1 |
| `/api/[recurso]/:id` | DELETE | 3 | P2 |

### 2.2 Detalle por Endpoint

#### GET /api/[recurso]

| ID | Escenario | Input | Expected | Prioridad |
|----|-----------|-------|----------|-----------|
| BE-GET-01 | Lista vacía | Sin datos en DB | `200`, `data: []` | P1 |
| BE-GET-02 | Lista con datos | 5 registros en DB | `200`, `data.length === 5` | P1 |
| BE-GET-03 | Paginación | `?page=2&perPage=10` | `200`, meta correcta | P2 |
| BE-GET-04 | Sin auth | Sin token | `401` | P0 |

#### POST /api/[recurso]

| ID | Escenario | Input | Expected | Prioridad |
|----|-----------|-------|----------|-----------|
| BE-POST-01 | Crear válido | Datos completos | `201`, recurso creado | P0 |
| BE-POST-02 | Campo faltante | Sin `field1` | `400`, error de validación | P0 |
| BE-POST-03 | Tipo inválido | `field1: 123` (debe ser string) | `400` | P1 |
| BE-POST-04 | Duplicado | Registro existente | `409` | P1 |
| BE-POST-05 | Sin auth | Sin token | `401` | P0 |

#### PATCH /api/[recurso]/:id

| ID | Escenario | Input | Expected | Prioridad |
|----|-----------|-------|----------|-----------|
| BE-PATCH-01 | Update válido | Datos parciales | `200`, recurso actualizado | P1 |
| BE-PATCH-02 | ID no existe | UUID inexistente | `404` | P1 |
| BE-PATCH-03 | Validación falla | Datos inválidos | `400` | P1 |
| BE-PATCH-04 | Sin auth | Sin token | `401` | P0 |

#### DELETE /api/[recurso]/:id

| ID | Escenario | Input | Expected | Prioridad |
|----|-----------|-------|----------|-----------|
| BE-DEL-01 | Delete válido | ID existente | `200` o `204` | P1 |
| BE-DEL-02 | ID no existe | UUID inexistente | `404` | P2 |
| BE-DEL-03 | Sin auth | Sin token | `401` | P0 |

---

## 3. ESCENARIOS FRONTEND

### 3.1 Resumen de Páginas

| Página | Componentes | Casos | Prioridad |
|--------|-------------|-------|-----------|
| [Página 1] | 5 | 8 | P0 |
| [Página 2] | 3 | 6 | P1 |

### 3.2 Detalle por Página

#### [Página 1]

| ID | Escenario | Pasos | Expected | Prioridad |
|----|-----------|-------|----------|-----------|
| FE-P1-01 | Render inicial | Navegar a `/[path]` | Página carga sin errores | P0 |
| FE-P1-02 | Estado vacío | Sin datos | Mensaje "No hay datos" visible | P1 |
| FE-P1-03 | Estado loading | Fetch en progreso | Skeleton/spinner visible | P2 |
| FE-P1-04 | Estado error | API retorna 500 | Mensaje de error + retry | P1 |
| FE-P1-05 | Estado con datos | 5 registros | Lista con 5 items | P0 |
| FE-P1-06 | Click en item | Click en primer item | Navega a detalle | P0 |
| FE-P1-07 | Responsive mobile | Viewport 375px | Layout correcto | P2 |
| FE-P1-08 | Accesibilidad | Tab navigation | Todos los elementos focusables | P2 |

#### [Página 2]

| ID | Escenario | Pasos | Expected | Prioridad |
|----|-----------|-------|----------|-----------|
| FE-P2-01 | Render inicial | Navegar a `/[path]` | Página carga | P0 |
| FE-P2-02 | Formulario válido | Completar todos los campos | Submit exitoso | P0 |
| FE-P2-03 | Validación inline | Campo inválido | Error bajo el campo | P1 |
| FE-P2-04 | Submit error | API falla | Toast de error | P1 |
| FE-P2-05 | Cancelar | Click "Cancelar" | Vuelve a página anterior | P2 |
| FE-P2-06 | Datos persistidos | Refresh post-submit | Datos visibles | P1 |

---

## 4. QA-FLOW SCENARIOS

### 4.1 Flujos de Navegación

| ID | Flujo | Pasa si... | Prioridad |
|----|-------|-----------|-----------|
| QA-FLOW-01 | [Pantalla A] → [Pantalla B] | Navegación automática correcta | P0 |
| QA-FLOW-02 | [Step X] → [Step Y] | Progress bar actualizado, datos persistidos | P0 |
| QA-FLOW-03 | Flujo completo del sprint | Todos los steps navegados sin error | P0 |
| QA-FLOW-04 | Resume draft en step intermedio | Navega al step correcto según estado guardado | P1 |
| QA-FLOW-05 | Pantallas vs HTML DL | Sin desviaciones críticas (coordinado con DL-REVIEW) | P1 |
| QA-FLOW-06 | Ruta directa inválida | Redirige al step correcto | P2 |

> **Nota QA-FLOW-05:** Siempre se coordina con DL-REVIEW.
> DL valida visualmente (impl vs HTMLs), QA valida navegación funcional.
> Ejecutar en paralelo — no son redundantes.

### 4.2 Detalle de Flujos Críticos

#### QA-FLOW-03: Flujo Completo

**Precondiciones:**
- Usuario autenticado
- [Otras precondiciones]

**Pasos:**
1. Navegar a `/[inicio-del-flujo]`
2. [Acción 1]
3. [Acción 2]
4. [Acción 3]
5. Verificar estado final

**Resultado esperado:**
- [Estado final esperado]
- Datos persistidos en DB
- Notificaciones correctas

**Verificaciones adicionales:**
- [ ] URL correcta en cada step
- [ ] Progress bar actualizado
- [ ] Botones habilitados/deshabilitados correctamente
- [ ] No hay errores en consola

---

## 5. PROCESO DE BUGS

### 5.1 Flujo de Reporte

```
QA encuentra bug durante testing
        │
        ▼
POST /api/tasks/{taskId}/issues   ← tarea pasa a on_hold AUTOMÁTICAMENTE
        │
        ▼
TL crea FIX task → asigna a desarrollador
        │
        ▼
Developer corrige + agrega test de regresión
        │
        ▼
TL revisa fix → FIX task a task_completed
        │
        ▼
PUT /api/issues/{id} {"isResolved": true}  ← TL ejecuta esto, NO QA
        │
        ▼
Tarea vuelve a previousStatus automáticamente
```

> **⚠️ NUNCA:** QA no debe cambiar estado a `on_hold` manualmente (PATCH /status).
> El sistema lo hace solo al crear el issue. Hacerlo manual deja `previousStatus=null`
> y rompe el flujo de restauración.

### 5.2 Formato de Issue

```json
POST /api/tasks/{taskId}/issues
{
  "title": "[QA-XXX] [Descripción corta del bug]",
  "description": "**Pasos para reproducir:**\n1. ...\n2. ...\n\n**Resultado actual:**\n...\n\n**Resultado esperado:**\n...\n\n**Evidencia:**\n[Screenshot/video]",
  "priorityId": "[UUID según severidad]"
}
```

### 5.3 Severidad → priorityId

| Severidad | Criterio | priorityId |
|-----------|----------|------------|
| S1 (Blocker) | Funcionalidad core rota | `90ec3df2-fac4-40fa-b2ce-29daf0f4956e` |
| S2 (Critical) | Feature importante no funciona | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |
| S3 (Major) | Feature secundaria afectada | `d0b619ef-b92c-4aff-b58d-7b4a0f3d9a02` *(verificar en sistema)* |
| S4 (Minor) | Cosmético, UX degradada | `95f2e731-c123-4b56-9a78-d0e1f2a3b4c5` *(verificar en sistema)* |

> **Nota:** Verificar IDs reales de Medium/Low en `GET /api/priorities` antes de usar en producción.

---

## 6. TAREAS DEL SPRINT

### Fase: Testing (Días X-Y)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| QA-001 | Test Plan Sprint [N] | QA | [X]h | MEDIUM | testing |
| QA-002 | Escenarios BE | QA | [X]h | MEDIUM | testing |
| QA-003 | Escenarios FE | QA | [X]h | MEDIUM | testing |
| QA-004 | QA-FLOW scenarios | QA | [X]h | HIGH | testing |
| QA-005 | Regression tests | QA | [X]h | MEDIUM | testing |

### Fase: Validación (Días Y-Z)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| APR-QA | Firma QA Sprint [N] | QA | 1h | LOW | review |

---

## 7. DEPENDENCIAS ENTRE TAREAS

| Tarea | Depende de | Tipo | Nota |
|-------|-----------|------|------|
| QA-001 | Sprint iniciado | — | Plan de testing |
| QA-002 | BE completado | FS | Endpoints disponibles |
| QA-003 | FE completado | FS | Páginas disponibles |
| QA-004 | QA-003 | FS | Flujos E2E |
| QA-005 | QA-002, QA-003, QA-004 | FS | Post-testing inicial |
| APR-QA | QA-005 | FS | Todo testeado |

---

## 8. VTT PLANNING DATA

> **QA crea sus propias tareas** en VTT cuando TL notifica que el gate QA se activó (ver Handoff TL §11).  
> A diferencia de FE, QA crea sus propias tareas — TL solo notifica, no las crea.

| Tarea | estimatedHours | complexity | category | dependsOn |
|-------|---------------|-----------|----------|-----------|
| QA-001 | [X] | MEDIUM | testing | — |
| QA-002 | [X] | MEDIUM | testing | [BE-XXX completadas] |
| QA-003 | [X] | MEDIUM | testing | [FE-XXX completadas] |
| QA-004 | [X] | HIGH | testing | QA-003 |
| QA-005 | [X] | MEDIUM | testing | QA-002, QA-003, QA-004 |
| APR-QA | 1 | LOW | review | QA-005 |

**Total QA scope:** [X]h

---

## 9. DOCUMENTOS DINÁMICOS A ACTUALIZAR

| Documento | Quién actualiza | Cuándo | Verificado en |
|-----------|----------------|--------|---------------|
| `TEST_PLAN_SPRINT_[N].md` | QA | Al inicio del sprint | APR-QA |
| `TEST_RESULTS_SPRINT_[N].md` | QA | Al finalizar testing | APR-QA |

---

## 10. DoD — QA

### Planificación:
- [ ] Test Plan creado con todos los escenarios
- [ ] Escenarios priorizados (P0, P1, P2, P3)
- [ ] Ambiente de testing configurado

### Ejecución:
- [ ] 100% escenarios P0 ejecutados y pasando
- [ ] 100% escenarios P1 ejecutados y pasando
- [ ] ≥80% escenarios P2 ejecutados
- [ ] QA-FLOW scenarios ejecutados

### Bugs:
- [ ] Todos los bugs reportados via POST /api/tasks/{id}/issues
- [ ] Bugs S1/S2 confirmados como resueltos por TL (QA verifica resolución, no ejecuta el fix ni resuelve el issue)
- [ ] Bugs S3/S4 documentados (pueden quedar para siguiente sprint)

### Cobertura:
- [ ] BE coverage ≥ 70%
- [ ] FE coverage ≥ 60%
- [ ] E2E flujos críticos cubiertos

### Documentación:
- [ ] Test Results documentados
- [ ] Evidencia de bugs (screenshots/videos)
- [ ] APR-QA firmado

---

## 11. GATES DE APROBACIÓN

| Gate | Condición | Acción en VTT |
|------|-----------|---------------|
| QA puede arrancar | FE completado + DL-REVIEW aprobado | TL notifica |
| Testing BE | BE endpoints disponibles | QA ejecuta |
| Testing FE | FE páginas disponibles | QA ejecuta |
| Bugs bloqueantes | Issues S1/S2 detectados | QA crea issue → on_hold auto |
| APR-QA | Todos los P0/P1 pasando, S1/S2 resueltos | QA firma |
| Sprint cerrado | APR-QA firmado | Parte de 4 firmas |

---

## 12. AMBIENTE DE TESTING

### 12.1 Configuración

| Aspecto | Valor |
|---------|-------|
| URL | `http://localhost:[PORT]` o `https://[staging-url]` |
| DB | Test database (datos de prueba) |
| Auth | Usuario de test: `test@test.com` / `password` |

### 12.2 Datos de Prueba

```sql
-- Seeds requeridos para testing
-- [Describir qué datos necesita el ambiente de test]
```

### 12.3 Comandos

```bash
# === BACKEND (Python/pytest) ===
# Unitarios BE
pytest backend/tests/unit/ -v

# Integración BE (endpoints)
pytest backend/tests/integration/ -v

# Cobertura BE
pytest backend/tests/ --cov=backend/src --cov-report=html

# === FRONTEND (Vitest) ===
# Unitarios FE
npm run test --prefix frontend

# Cobertura FE
npm run test:coverage --prefix frontend

# === E2E (Playwright) ===
npx playwright test
```

---

## 13. REFERENCIAS

| Documento | Ubicación | Para qué |
|-----------|-----------|----------|
| `TESTING_GUIDE.md` | `_project_manager/Templates/` | Proceso completo de testing |
| `API_CONTRACT.md` | `backend/knowledge/` | Contratos de API verificados |
| HTMLs de DL | `Design/specs/sprint_[N]/` | Referencia visual de pantallas |
| `METODOLOGIA_EJECUCION_SPRINTS.md` | `_project_manager/Templates/` | Proceso de sprint |

---

## 14. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | [YYYY-MM-DD] | PJM-Agent | Versión inicial |
| 1.1 | 2026-03-30 | PJM-Agent | UUIDs S3/S4 completos, QA crea sus tareas (TL notifica), DoD bugs clarificado, comandos Python/Vitest/Playwright, referencias actualizadas |

---

**FIN DEL HANDOFF QA**
