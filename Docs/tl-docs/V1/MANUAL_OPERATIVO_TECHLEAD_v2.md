# 📘 MANUAL OPERATIVO - Tech Lead

**Versión:** 2.0  
**Fecha:** Febrero 2025  
**Propósito:** Guía única para coordinar el desarrollo con múltiples agentes

---

## CÓMO USAR ESTE MANUAL

Este es tu **único documento de referencia**. Sigue el flujo paso a paso.
Los documentos detallados (NIVEL1, NIVEL2, NIVEL3) se consultan cuando este manual lo indique.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TU FLUJO DE TRABAJO                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   TAREA LLEGA                                                               │
│        │                                                                    │
│        ▼                                                                    │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐               │
│   │ PASO 1  │────▶│ PASO 2  │────▶│ PASO 3  │────▶│ PASO 4  │             │
│   │Clasificar│    │Verificar│     │ Armar   │     │Asignar  │               │
│   │  Tarea  │     │Dependen.│     │Assignment│    │ y Noti- │               │
│   │         │     │         │     │         │     │  ficar  │               │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ESTRUCTURA DE LA METODOLOGÍA

Tienes 3 niveles de documentación por cada elemento:

| Nivel | Pregunta que responde | Cuándo consultar |
|-------|----------------------|------------------|
| **NIVEL 1** | ¿QUÉ es y POR QUÉ? | Cuando necesites entender principios o decisiones |
| **NIVEL 2** | ¿CÓMO se hace? (Input → Proceso → Output) | Cuando necesites los pasos detallados |
| **NIVEL 3** | ¿QUIÉN lo hace? (Responsables y dependencias) | Cuando necesites saber quién y qué depende de qué |

**Regla:** No necesitas leer los 3 niveles para cada tarea. Este manual te dice cuál consultar.

---

# PASO 1: CLASIFICAR LA TAREA

## 1.1 ¿Qué tipo de tarea es?

| Tipo | Descripción | Agente | Elemento Metodología |
|------|-------------|--------|---------------------|
| **DB** | Migración, nuevo campo, nueva tabla | Database Engineer | Elemento 4 |
| **CATÁLOGOS** | Seed de datos, valores de catálogo | Database Engineer | Elemento 5 |
| **API** | Nuevo endpoint, modificar endpoint | Backend Dev | Elemento 6 |
| **DOC-API** | Documentar en Swagger | Backend Dev | Elemento 7 |
| **AUTH** | Autenticación, permisos, tokens | Backend Dev | Elemento 8 |
| **FE-BASE** | Setup inicial frontend, config | Frontend Dev | Elemento 9 |
| **FE-COMPONENTE** | Nuevo componente UI | Frontend Dev | Elemento 10 |
| **FE-PANTALLA** | Nueva pantalla completa | Frontend Dev | Elemento 11 |
| **INTEGRACIÓN** | Conectar FE con BE | Frontend Dev | Elemento 12 |
| **TESTING** | Tests unitarios, E2E | QA | Elemento 13 |
| **QA-VISUAL** | Revisión visual vs diseño | Design Lead | Elemento 14 |
| **DEPLOY** | Despliegue a producción | DevOps | Elemento 15 |

## 1.2 Documentos de metodología por tipo

Una vez identificado el tipo, estos son los documentos de referencia:

### Para tareas de BASE DE DATOS (Elemento 4)
```
📖 Consultar si necesitas contexto:
   └── METODOLOGIA_NIVEL1_ELEMENTO4_BASE_DATOS_v2.md (QUÉ y POR QUÉ)

📋 Consultar para los pasos:
   └── METODOLOGIA_NIVEL2_ELEMENTO4_BASE_DATOS.md (CÓMO)

👥 Consultar para dependencias:
   └── METODOLOGIA_NIVEL3_ELEMENTO4_BASE_DATOS.md (QUIÉN)
```

### Para tareas de CATÁLOGOS (Elemento 5)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO5_CATALOGOS_v2.md
📋 METODOLOGIA_NIVEL2_ELEMENTO5_CATALOGOS.md
👥 METODOLOGIA_NIVEL3_ELEMENTO5_CATALOGOS.md
```

### Para tareas de APIs (Elemento 6)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO6_APIS_v2.md
📋 METODOLOGIA_NIVEL2_ELEMENTO6_APIS.md
👥 METODOLOGIA_NIVEL3_ELEMENTO6_APIS.md
```

### Para tareas de DOCUMENTACIÓN API (Elemento 7)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO7_DOCUMENTACION_API_v2.md
📋 METODOLOGIA_NIVEL2_ELEMENTO7_DOCUMENTACION_API.md
👥 METODOLOGIA_NIVEL3_ELEMENTO7_DOCUMENTACION_API.md
```

### Para tareas de AUTENTICACIÓN (Elemento 8)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO8_AUTENTICACION_v2.md
📋 METODOLOGIA_NIVEL2_ELEMENTO8_AUTENTICACION.md
👥 METODOLOGIA_NIVEL3_ELEMENTO8_AUTENTICACION.md
```

### Para tareas de FRONTEND BASE (Elemento 9)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO9_FRONTEND_BASE_v2.md
📋 METODOLOGIA_NIVEL2_ELEMENTO9_FRONTEND_BASE.md
👥 METODOLOGIA_NIVEL3_ELEMENTO9_FRONTEND_BASE.md
```

### Para tareas de COMPONENTES UI (Elemento 10)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO10_COMPONENTES.md
📋 METODOLOGIA_NIVEL2_ELEMENTO10_COMPONENTES.md
👥 METODOLOGIA_NIVEL3_ELEMENTO10_COMPONENTES.md
```

### Para tareas de PANTALLAS (Elemento 11)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO11_PANTALLAS.md
📋 METODOLOGIA_NIVEL2_ELEMENTO11_PANTALLAS.md
👥 METODOLOGIA_NIVEL3_ELEMENTO11_PANTALLAS.md
```

### Para tareas de INTEGRACIÓN (Elemento 12)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO12_INTEGRACION.md
📋 METODOLOGIA_NIVEL2_ELEMENTO12_INTEGRACION.md
👥 METODOLOGIA_NIVEL3_ELEMENTO12_INTEGRACION.md
```

### Para tareas de TESTING (Elemento 13)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO13_TESTING.md
📋 METODOLOGIA_NIVEL2_ELEMENTO13_TESTING.md
👥 METODOLOGIA_NIVEL3_ELEMENTO13_TESTING.md
```

### Para tareas de QA VISUAL (Elemento 14)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO14_QA_VISUAL.md
📋 METODOLOGIA_NIVEL2_ELEMENTO14_QA_VISUAL.md
👥 METODOLOGIA_NIVEL3_ELEMENTO14_QA_VISUAL.md
```

### Para tareas de DEPLOY (Elemento 15)
```
📖 METODOLOGIA_NIVEL1_ELEMENTO15_DEPLOY.md
📋 METODOLOGIA_NIVEL2_ELEMENTO15_DEPLOY.md
👥 METODOLOGIA_NIVEL3_ELEMENTO15_DEPLOY.md
```

---

# PASO 2: VERIFICAR DEPENDENCIAS

## 2.1 Orden obligatorio de construcción

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ORDEN DE CONSTRUCCIÓN (NO SALTARSE)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   FASE 0: FUNDAMENTOS                                                       │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                        │
│   │ 1. Arquitec.│  │ 2. Infra    │  │ 3. Arq.Cód. │                        │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                        │
│          └────────────────┴────────────────┘                               │
│                           │                                                 │
│                           ▼                                                 │
│   FASE 1: BACKEND                                                           │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│   │ 4. BD       │─▶│ 5. Catálog. │─▶│ 6. APIs     │─▶│ 7. Doc API  │       │
│   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
│                                            │                                │
│                           ┌────────────────┘                                │
│                           ▼                                                 │
│   FASE 1: FRONTEND (puede iniciar en paralelo con Backend después de BD)   │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                        │
│   │ 9. FE Base  │─▶│10. Componen.│─▶│11. Pantallas│                        │
│   └─────────────┘  └─────────────┘  └─────────────┘                        │
│                                            │                                │
│                           ┌────────────────┘                                │
│                           ▼                                                 │
│   FASE 2: INTEGRACIÓN                                                       │
│   ┌─────────────┐                                                           │
│   │12. Integrac.│  ◄── SOLO cuando APIs Y Pantallas están listas           │
│   └──────┬──────┘                                                           │
│          │                                                                  │
│          ▼                                                                  │
│   FASE 3: VALIDACIÓN                                                        │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                        │
│   │13. Testing  │─▶│14. QA Visual│─▶│15. Deploy   │                        │
│   └─────────────┘  └─────────────┘  └─────────────┘                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Matriz de dependencias rápida

| Si la tarea es... | Debe estar LISTO antes... |
|-------------------|---------------------------|
| **4. Base de Datos** | Elemento 3 (Arquitectura de Código) |
| **5. Catálogos** | Elemento 4 (Base de Datos) |
| **6. APIs** | Elementos 4 y 5 (BD y Catálogos) |
| **7. Doc API** | Elemento 6 (APIs) |
| **9. Frontend Base** | Elemento 3 (Arquitectura de Código) |
| **10. Componentes** | Elemento 9 (Frontend Base) |
| **11. Pantallas** | Elementos 6 y 10 (APIs y Componentes) |
| **12. Integración** | Elementos 6 y 11 (APIs y Pantallas) |
| **13. Testing** | Elemento 12 (Integración) |
| **14. QA Visual** | Elemento 11 (Pantallas) |
| **15. Deploy** | Elementos 13 y 14 (Testing y QA) |

## 2.3 Checklist de dependencias por tipo

### Si es tarea de BASE DE DATOS (Elemento 4):
```
□ ¿Arquitectura de código definida? (Elemento 3)
□ ¿Modelo de datos diseñado?
→ Si todo SÍ: Puede iniciar
→ Consultar: METODOLOGIA_NIVEL3_ELEMENTO4_BASE_DATOS.md
```

### Si es tarea de APIs (Elemento 6):
```
□ ¿La tabla en BD existe? (Elemento 4)
□ ¿Los catálogos están cargados? (Elemento 5)
□ ¿El endpoint está definido en API_CONTRACT.md?
→ Si todo SÍ: Puede iniciar
→ Si BD NO existe: BLOQUEAR - Crear tarea de BD primero
→ Consultar: METODOLOGIA_NIVEL3_ELEMENTO6_APIS.md
```

### Si es tarea de PANTALLA (Elemento 11):
```
□ ¿El endpoint que consume está IMPLEMENTADO? (Elemento 6)
□ ¿Los componentes necesarios existen? (Elemento 10)
□ ¿Hay diseño/mockup disponible?
→ Si todo SÍ: Puede iniciar
→ Si endpoint NO existe: BLOQUEAR - Crear tarea de API primero
→ Consultar: METODOLOGIA_NIVEL3_ELEMENTO11_PANTALLAS.md
```

### Si es tarea de INTEGRACIÓN (Elemento 12):
```
□ ¿El endpoint está implementado? (Elemento 6)
□ ¿La pantalla está implementada? (Elemento 11)
→ Si todo SÍ: Puede iniciar
→ Si algo NO: BLOQUEAR hasta que esté listo
→ Consultar: METODOLOGIA_NIVEL3_ELEMENTO12_INTEGRACION.md
```

## 2.4 ¿Qué hacer si hay dependencias bloqueantes?

```
1. NO asignar la tarea
2. Identificar qué tarea debe completarse primero
3. Informar al PM: "Tarea X está bloqueada por Y"
4. Esperar a que Y se complete
5. Entonces asignar X
```

**→ Si las dependencias están listas, continúa al PASO 3**

---

# PASO 3: ARMAR EL ASSIGNMENT

## 3.1 Qué documentos consultar según el tipo

| Tipo de Tarea | Documentos de METODOLOGÍA | Otros documentos |
|---------------|---------------------------|------------------|
| **DB** | NIVEL2_ELEMENTO4 (pasos) | 04_ESQUEMA_BD.md |
| **Catálogos** | NIVEL2_ELEMENTO5 (pasos) | 05_CATALOGOS.md |
| **API** | NIVEL2_ELEMENTO6 (pasos) | API_CONTRACT.md, 10_REGLAS_NEGOCIO.md |
| **FE-Pantalla** | NIVEL2_ELEMENTO11 (pasos) | API_CONTRACT.md, Diseño/Mockup |
| **FE-Componente** | NIVEL2_ELEMENTO10 (pasos) | DESIGN_SYSTEM.md, Diseño/Mockup |
| **Integración** | NIVEL2_ELEMENTO12 (pasos) | API_CONTRACT.md, INTEGRATION_RULES.md |

## 3.2 Los 8 elementos OBLIGATORIOS en cada Assignment

Todo assignment DEBE incluir estos 8 elementos (del PERFIL_TECHLEAD_STANDARD.md):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     8 ELEMENTOS OBLIGATORIOS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. ESTADO ACTUAL DEL PROYECTO                                              │
│     └── ¿Qué está completado? ¿Qué branches hay? ¿Qué PRs están abiertos? │
│                                                                             │
│  2. APIs Y SERVICIOS DISPONIBLES                                            │
│     └── Endpoints con ejemplos REALES de request/response                  │
│                                                                             │
│  3. ARQUITECTURA Y ESTRUCTURA                                               │
│     └── Carpetas, patrones, convenciones del proyecto                      │
│                                                                             │
│  4. CONTEXTO DE INTEGRACIÓN                                                 │
│     └── ¿Cómo se conecta con el resto? ¿Qué afecta?                        │
│                                                                             │
│  5. ENTIDADES Y MODELOS                                                     │
│     └── Schema de BD, relaciones, tipos                                    │
│                                                                             │
│  6. RECURSOS DE DISEÑO                                                      │
│     └── Mockups, design specs, tokens (si aplica)                          │
│                                                                             │
│  7. CHECKLIST DETALLADO                                                     │
│     └── Mínimo 10-15 items verificables                                    │
│                                                                             │
│  8. ARCHIVOS A REVISAR ANTES DE EMPEZAR                                     │
│     └── Lista con ruta y propósito de cada archivo                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3.3 Template rápido por tipo de tarea

### Para tarea de BASE DE DATOS (Elemento 4):

```markdown
## ASSIGNMENT: [ID] - [Título]

### Metodología de referencia
- Consultar: METODOLOGIA_NIVEL2_ELEMENTO4_BASE_DATOS.md

### 1. Estado actual
- Branch base: `main`
- Migraciones existentes: [lista]
- Última migración: [nombre]

### 2. Modelo de datos
Ver 04_ESQUEMA_BD.md:
**Tabla a crear/modificar:** [nombre]
| Campo | Tipo | Nullable | Default | Descripción |
|-------|------|----------|---------|-------------|
| ... | ... | ... | ... | ... |

### 3. Relaciones
- FK a [tabla]: [campo] → [tabla.campo]

### 4. Datos semilla (si aplica)
Ver 05_CATALOGOS.md:
[SQL o datos a insertar]

### 5. Checklist
- [ ] Migración creada
- [ ] Migración aplicada sin errores
- [ ] Seed ejecutado (si aplica)
- [ ] Rollback probado
[...mínimo 10 items]

### 6. Archivos a revisar
| Archivo | Propósito |
|---------|-----------|
| `METODOLOGIA_NIVEL1_ELEMENTO4_BASE_DATOS_v2.md` | Principios de BD |
| `prisma/schema.prisma` | Schema actual |
```

### Para tarea de API (Elemento 6):

```markdown
## ASSIGNMENT: [ID] - [Título]

### Metodología de referencia
- Consultar: METODOLOGIA_NIVEL2_ELEMENTO6_APIS.md

### 1. Estado actual
- Branch base: `main`
- PRs pendientes: [lista]

### 2. Contrato de API
Ver API_CONTRACT.md sección [X]

**Ruta:** [MÉTODO] /api/v1/[ruta]
**Auth:** Sí/No

**Request:**
```json
{ ... }
```

**Response:**
```json
{ ... }
```

**Errores:**
| Código | Condición |
|--------|-----------|
| 400 | ... |
| 404 | ... |

### 3. Base de datos
Ver 04_ESQUEMA_BD.md:
- Tabla: [nombre]
- Campos: [lista]

### 4. Reglas de negocio
Ver 10_REGLAS_DE_NEGOCIO.md:
- RN-XXX: [descripción]

### 5. Arquitectura
Ver METODOLOGIA_NIVEL1_ELEMENTO6_APIS_v2.md sección 12:
- Patrón: Controller → Service → Repository
- Carpeta: `backend/app/api/v1/[modulo]/`

### 6. Checklist
- [ ] Endpoint creado
- [ ] Validaciones implementadas
- [ ] Errores con formato estándar
- [ ] Tests unitarios
- [ ] Swagger actualizado
[...mínimo 10 items]

### 7. Archivos a revisar
| Archivo | Propósito |
|---------|-----------|
| `METODOLOGIA_NIVEL1_ELEMENTO6_APIS_v2.md` | Principios REST |
| `API_CONTRACT.md` | Contrato del endpoint |
| `backend/app/api/v1/auth/router.py` | Ejemplo de patrón |
```

### Para tarea de PANTALLA (Elemento 11):

```markdown
## ASSIGNMENT: [ID] - [Título]

### Metodología de referencia
- Consultar: METODOLOGIA_NIVEL2_ELEMENTO11_PANTALLAS.md

### 1. Estado actual
- Branch base: `main`
- Endpoints disponibles: ✅ [lista]
- Componentes disponibles: ✅ [lista]

### 2. API que consume
Ver API_CONTRACT.md:

**GET /api/v1/[ruta]**
Response:
```json
{ ... }
```

### 3. Componentes a usar
Ver METODOLOGIA_NIVEL1_ELEMENTO10_COMPONENTES.md:
- [Componente1] - para [uso]
- [Componente2] - para [uso]

### 4. Diseño
- Mockup: [link o descripción]
- Estados UI: loading, empty, error, success

### 5. Transformación de datos
```typescript
// API response (snake_case) → Store (camelCase)
```

### 6. Checklist
- [ ] Pantalla implementada
- [ ] Estados (loading, empty, error) funcionando
- [ ] Conectada a API real
- [ ] Responsive
[...mínimo 10 items]

### 7. Archivos a revisar
| Archivo | Propósito |
|---------|-----------|
| `METODOLOGIA_NIVEL1_ELEMENTO11_PANTALLAS.md` | Principios de pantallas |
| `API_CONTRACT.md` | Endpoints que consume |
| `frontend/src/pages/auth/SignIn.tsx` | Ejemplo de patrón |
```

### Para tarea de INTEGRACIÓN (Elemento 12):

```markdown
## ASSIGNMENT: [ID] - [Título]

### Metodología de referencia
- Consultar: METODOLOGIA_NIVEL2_ELEMENTO12_INTEGRACION.md

### 1. Estado actual
- Endpoint: ✅ [ruta] implementado
- Pantalla: ✅ [nombre] implementada

### 2. Contrato de API
Ver API_CONTRACT.md:
[JSON del endpoint]

### 3. Transformación de datos
Ver INTEGRATION_RULES.md:
```typescript
// snake_case → camelCase
```

### 4. Manejo de errores
| Código API | Acción en UI |
|------------|--------------|
| 401 | Redirect a login |
| 404 | Mostrar "No encontrado" |
| 500 | Mostrar "Error del servidor" |

### 5. Checklist
- [ ] Flujo completo funciona
- [ ] Datos se guardan correctamente
- [ ] Errores se muestran correctamente
- [ ] Loading states funcionan
[...mínimo 10 items]

### 6. Archivos a revisar
| Archivo | Propósito |
|---------|-----------|
| `METODOLOGIA_NIVEL1_ELEMENTO12_INTEGRACION.md` | Principios |
| `API_CONTRACT.md` | Contrato |
| `INTEGRATION_RULES.md` | Reglas de transformación |
```

## 3.4 ¿Dónde guardar el assignment?

```
knowledge/agent-tasks/ASSIGNMENT_[ID]_[nombre].md
```

**→ Cuando el assignment está listo, continúa al PASO 4**

---

# PASO 4: ASIGNAR Y NOTIFICAR

## 4.1 Flujo de asignación

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FLUJO DE ASIGNACIÓN                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Tech Lead genera BRIEF + ASSIGNMENT                                     │
│        │                                                                    │
│        ▼                                                                    │
│  2. Tech Lead genera MENSAJE para el agente                                 │
│        │                                                                    │
│        ▼                                                                    │
│  3. Tech Lead entrega todo al PM (Martin)                                   │
│        │                                                                    │
│        ▼                                                                    │
│  4. PM asigna la tarea en la UI                                             │
│        │                                                                    │
│        ▼                                                                    │
│  5. PM pega el mensaje como comentario                                      │
│        │                                                                    │
│        ▼                                                                    │
│  6. PM notifica al agente                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Template del mensaje para el agente

```markdown
Tienes tarea nueva asignada: [ID] ([Título]).

## Documentos a leer

1. **Assignment:** knowledge/agent-tasks/ASSIGNMENT_[ID]_[nombre].md
2. **Brief:** knowledge/agent-tasks/BRIEF_[ID]_[nombre].md
3. **Metodología:** METODOLOGIA_NIVEL2_ELEMENTO[X]_[nombre].md
4. **Procedimientos:** knowledge/PROCEDIMIENTOS_OPERATIVOS_AGENTES.md

## Comandos del sistema

### Al iniciar (mover a in_progress):
```bash
curl -s -X PATCH {BASE_URL}/api/tasks/[ID]/status \
  -H "Content-Type: application/json" \
  -d '{"statusId": "{UUID_IN_PROGRESS}", "changedBy": "{UUID_AGENTE}"}'
```

### Al terminar (mover a in_review):
```bash
curl -s -X PATCH {BASE_URL}/api/tasks/[ID]/status \
  -H "Content-Type: application/json" \
  -d '{"statusId": "{UUID_IN_REVIEW}", "changedBy": "{UUID_AGENTE}"}'
```

## Datos del sistema
- Tu user ID: {UUID_AGENTE}
- Status in_progress: {UUID}
- Status in_review: {UUID}
- Backend: {BASE_URL}

## Al terminar
Entrega el reporte con el formato del assignment para revisión.
```

## 4.3 Consultar UUIDs del proyecto

Antes de generar el mensaje, consulta los UUIDs:

```bash
# Status
curl -s "{BASE_URL}/api/catalogs/status?process=task"

# Usuarios/Agentes
curl -s "{BASE_URL}/api/users"
```

**→ Documenta:** `knowledge/PROJECT_REFERENCE.md`

## 4.4 Qué entregas al PM

```markdown
## Entrega para PM

### Archivos generados:
1. ✅ knowledge/agent-tasks/BRIEF_[ID]_[nombre].md
2. ✅ knowledge/agent-tasks/ASSIGNMENT_[ID]_[nombre].md

### Mensaje para el agente:
[Copiar el mensaje generado arriba]

### Agente recomendado:
[Tipo de agente según el elemento de metodología]

### Metodología aplicable:
METODOLOGIA_NIVEL2_ELEMENTO[X]_[nombre].md

### Dependencias verificadas:
✅ [Lista de dependencias completadas]

### Listo para asignar.
```

---

# PASO 5: DURANTE LA EJECUCIÓN (Monitoreo)

## 5.1 Qué monitorear

```
□ ¿El agente movió la tarea a in_progress?
□ ¿Hay bloqueos reportados?
□ ¿Está siguiendo el assignment?
□ ¿Está siguiendo la metodología (NIVEL2)?
□ ¿Creó el branch correcto?
```

## 5.2 Si el agente reporta bloqueo

```
1. Identificar el tipo de bloqueo:
   ├── Falta dato/API → Crear issue, poner tarea on_hold
   ├── Duda técnica → Responder o escalar a PM
   ├── Dependencia no lista → Verificar NIVEL3 del elemento
   └── No entiende el proceso → Referir a NIVEL1 o NIVEL2

2. Actualizar estado si es necesario:
   curl -s -X PUT {BASE_URL}/api/tasks/[ID]/on-hold \
     -H "x-user-id: {UUID_TECH_LEAD}"
```

## 5.3 Si necesitas crear un issue

```bash
curl -s -X POST {BASE_URL}/api/tasks/[TASK_ID]/issues \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Título descriptivo",
    "description": "Contexto, causa, solución propuesta",
    "type": "requirement",
    "severity": "high"
  }'
```

---

# PASO 6: AL COMPLETARSE LA TAREA (Review)

## 6.1 Checklist de review

```markdown
## Review de [ID] - Elemento [X]

### Metodología
- [ ] Siguió los pasos del NIVEL2_ELEMENTO[X]
- [ ] Cumplió los criterios de salida del NIVEL2

### Documentación
- [ ] Development Log creado
- [ ] Code Logic creado (si aplica)

### Código
- [ ] Sigue los patrones del proyecto
- [ ] No modificó archivos fuera del scope
- [ ] Tests incluidos (si aplica)

### Assignment
- [ ] Todos los items del checklist cumplidos
- [ ] Criterios de aceptación verificados

### Git
- [ ] PR creado
- [ ] Branch correcto
- [ ] Commits descriptivos

### Resultado
- [ ] ✅ APROBADO → Notificar al PM para merge
- [ ] 🔄 CAMBIOS REQUERIDOS → Devolver al agente
- [ ] ❌ RECHAZADO → Documentar razón
```

## 6.2 Verificar criterios de salida (del NIVEL2)

Cada NIVEL2 tiene una sección "CRITERIOS DE SALIDA". Verificar que se cumplan:

```
Ejemplo para APIs (NIVEL2_ELEMENTO6):
□ Todos los endpoints del catálogo implementados
□ Validaciones funcionando
□ Errores con estructura consistente
□ Seguridad aplicada (auth, roles)
□ Tests pasando
□ Frontend puede consumir las APIs
```

## 6.3 Aprobar la tarea

```bash
# Mover a completed
curl -s -X PATCH {BASE_URL}/api/tasks/[ID]/status \
  -H "Content-Type: application/json" \
  -d '{"statusId": "{UUID_COMPLETED}", "changedBy": "{UUID_TECH_LEAD}"}'
```

## 6.4 Notificar al PM

```markdown
## Tarea lista para merge: [ID]

**PR:** #[número]
**Branch:** feature/[ID]
**Agente:** [nombre]
**Elemento:** [X] - [nombre]

### Review completado:
✅ Código sigue patrones
✅ Tests pasan
✅ Documentación creada
✅ Checklist cumplido
✅ Criterios de salida del NIVEL2 cumplidos

**Listo para merge cuando autorices.**
```

---

# REFERENCIA RÁPIDA

## Documentos de Metodología (48 documentos)

| Elemento | NIVEL 1 (QUÉ) | NIVEL 2 (CÓMO) | NIVEL 3 (QUIÉN) |
|----------|---------------|----------------|-----------------|
| 1. Arquitectura Solución | ✅ | ✅ | ✅ |
| 2. Infraestructura | ✅ | ✅ | ✅ |
| 3. Arquitectura Código | ✅ (v2) | ✅ | ✅ |
| 4. Base de Datos | ✅ (v2) | ✅ | ✅ |
| 5. Catálogos | ✅ (v2) | ✅ | ✅ |
| 6. APIs | ✅ (v2) | ✅ | ✅ |
| 7. Documentación API | ✅ (v2) | ✅ | ✅ |
| 8. Autenticación | ✅ (v2) | ✅ | ✅ |
| 9. Frontend Base | ✅ (v2) | ✅ | ✅ |
| 10. Componentes | ✅ | ✅ | ✅ |
| 11. Pantallas | ✅ | ✅ | ✅ |
| 12. Integración | ✅ | ✅ | ✅ |
| 13. Testing | ✅ | ✅ | ✅ |
| 14. QA Visual | ✅ | ✅ | ✅ |
| 15. Deploy | ✅ | ✅ | ✅ |

## Otros documentos clave

| Necesito... | Documento |
|-------------|-----------|
| APIs del sistema de tracking | `PROCEDIMIENTOS_OPERATIVOS_STANDARD.md` |
| Mis responsabilidades | `PERFIL_TECHLEAD_STANDARD.md` |
| UUIDs del proyecto actual | `knowledge/PROJECT_REFERENCE.md` |
| Contratos de API | `API_CONTRACT.md` |
| Reglas de integración | `INTEGRATION_RULES.md` |
| Flujo general de construcción | `METODOLOGIA_SISTEMA_AGENTES_FLUJO_CONSTRUCCION_v1.md` |

## Comandos más usados

```bash
# Ver tarea
curl -s {BASE_URL}/api/tasks/[ID]

# Cambiar status
curl -s -X PATCH {BASE_URL}/api/tasks/[ID]/status \
  -H "Content-Type: application/json" \
  -d '{"statusId": "{UUID}", "changedBy": "{UUID}"}'

# Crear issue
curl -s -X POST {BASE_URL}/api/tasks/[ID]/issues \
  -H "Content-Type: application/json" \
  -d '{"title": "...", "description": "...", "type": "bug", "severity": "high"}'

# Poner on-hold
curl -s -X PUT {BASE_URL}/api/tasks/[ID]/on-hold \
  -H "x-user-id: {UUID}"

# Ver status disponibles
curl -s {BASE_URL}/api/catalogs/status?process=task
```

---

# ERRORES COMUNES A EVITAR

| Error | Consecuencia | Cómo evitarlo |
|-------|--------------|---------------|
| Asignar FE antes de que API exista | Frontend trabaja con mocks, luego no integra | Verificar PASO 2 + NIVEL3 |
| Assignment sin ejemplos reales | Agente inventa o asume | Incluir JSON real del codebase |
| No verificar dependencias | Tarea se bloquea a mitad | Usar checklist del PASO 2 |
| Asignar sin que PM apruebe | PM pierde control | Siempre entregar al PM primero |
| No incluir archivos a revisar | Agente no sigue patrones | Elemento #8 es obligatorio |
| No referenciar metodología | Agente no sabe el proceso | Incluir NIVEL2 en el assignment |

---

# RESUMEN EN 1 PÁGINA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RESUMEN: FLUJO DEL TECH LEAD                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PASO 1: CLASIFICAR                                                         │
│          ¿Qué tipo? → Identificar elemento (1-15)                          │
│          Consultar: Tabla de tipos en sección 1.1                          │
│                                                                             │
│  PASO 2: VERIFICAR DEPENDENCIAS                                             │
│          ¿Qué debe estar listo antes?                                      │
│          Consultar: NIVEL3 del elemento + Matriz sección 2.2               │
│          Si dependencia no lista → BLOQUEAR                                │
│                                                                             │
│  PASO 3: ARMAR ASSIGNMENT                                                   │
│          8 elementos obligatorios + template del tipo                      │
│          Consultar: NIVEL2 del elemento para los pasos                     │
│          Guardar en: knowledge/agent-tasks/ASSIGNMENT_[ID].md              │
│                                                                             │
│  PASO 4: ENTREGAR AL PM                                                     │
│          Brief + Assignment + Mensaje para agente                          │
│          PM asigna en UI + pega comentario + notifica                      │
│                                                                             │
│  PASO 5: MONITOREAR                                                         │
│          Bloqueos → Issues → On-hold si es necesario                       │
│          Consultar: NIVEL1 si agente tiene dudas de principios             │
│                                                                             │
│  PASO 6: REVIEW                                                             │
│          Verificar criterios de salida del NIVEL2                          │
│          Checklist + Aprobar/Rechazar + Notificar PM para merge            │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CUÁNDO CONSULTAR CADA NIVEL:                                               │
│                                                                             │
│  NIVEL 1 → Cuando necesites entender POR QUÉ se hace algo                  │
│  NIVEL 2 → Cuando necesites saber CÓMO hacer algo (pasos)                  │
│  NIVEL 3 → Cuando necesites saber QUIÉN y QUÉ DEPENDE de qué              │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  REGLAS DE ORO:                                                             │
│  • NUNCA asignar sin verificar dependencias (NIVEL3)                       │
│  • SIEMPRE incluir referencia al NIVEL2 en el assignment                   │
│  • SIEMPRE entregar al PM para que él asigne                               │
│  • SIEMPRE verificar criterios de salida del NIVEL2 en review              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Documento:** MANUAL_OPERATIVO_TECHLEAD.md  
**Versión:** 2.0  
**Fecha:** Febrero 2025
