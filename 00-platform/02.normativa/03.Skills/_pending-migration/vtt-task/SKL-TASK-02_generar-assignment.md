# SKL-TASK-02: Generar ASSIGNMENT

**Categoría:** VTT-TASK  
**Aplica a:** TL  
**Tokens estimados:** ~200  
**Cuándo:** FASE 2 — antes de asignar una tarea, para preparar el documento de instrucciones al agente ejecutor

---

## Precondición

- BRIEF de la tarea existe en `knowledge/agent-tasks/briefs/BRIEF_$TASK_ID_$SLUG.md`
- Tarea creada en VTT con status `task_pending` (SKL-TASK-01 ejecutada)

---

## Paso 1 — Verificar dependencias de datos (ANTES de escribir)

> **Regla absoluta:** Ningún assignment se genera sin completar este análisis. Un assignment sin dependencias verificadas = el agente trabaja en el vacío = entrega incorrecta.

### 1.1 Leer el brief completo
- ¿Qué tipo de entregable produce? (wireframe / código / análisis / doc)
- ¿Qué archivos específicos debe generar?
- ¿Cuáles son los criterios de completitud?

### 1.2 Identificar qué datos necesita el agente según tipo de tarea

| Tipo | Datos necesarios |
|------|-----------------|
| Wireframes | Personas, User Flows, Site Map/IA, Design System, User Stories |
| Design System | Brand guidelines, tokens previos, referencias |
| Especificación técnica | SPEC, decisiones de arquitectura (D-MEM-xx), modelo de datos |
| Código BE | Schema Prisma, contratos de API, reglas de negocio, error codes |
| Código FE | Wireframes aprobados, Design System, contratos de API |
| Tests | Código a testear, criterios de aceptación, casos de error |
| Documentación | Todo lo anterior del módulo correspondiente |

### 1.3 Trazar dependencias → documento concreto → ruta exacta

```
Tarea dependencia → Entregable específico → Ruta en repo
```

### 1.4 Verificar que los documentos existen en el repo

```bash
ls phases/03-design/deliverables/personas/
ls phases/02-analysis/deliverables/user-flows/
# etc. según las dependencias identificadas
```

**Si un documento NO existe → NO generar el assignment:**
```bash
# Marcar tarea como bloqueada
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\": \"$STATUS_BLOCKED_UUID\", \"changedBy\": \"$AGENT_UUID\", \"reason\": \"Falta [documento] de [tarea origen]\"}"
```
Luego notificar al PM.

### 1.5 Verificar que las tareas dependencia están en `task_completed` o `task_approved`

```bash
curl -s "$VTT_BASE_URL/api/tasks/$DEPENDS_ON_TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['status'])"
```

Si una dependencia está en `task_pending` o `task_in_progress` → la tarea no puede ejecutarse aún.

---

## Paso 2 — Leer artefactos reales del codebase

> **Regla LL-005:** Llenar el ASSIGNMENT desde artefactos verificados, NUNCA desde memoria o el handoff del PM.

### Según tipo de tarea:

**FE:**
```
1. frontend/src/router/index.tsx         → rutas existentes
2. backend/src/routes/[modulo].ts        → endpoints que consumirá
3. frontend/src/components/features/     → componentes existentes
4. frontend/src/hooks/use*.ts            → hooks disponibles
5. frontend/src/index.css                → tokens disponibles
```

**BE:**
```
1. backend/src/routes/index.ts           → módulos registrados
2. backend/src/routes/[modulo].ts        → endpoints actuales
3. backend/prisma/schema.prisma          → entidades y relaciones
4. backend/src/middleware/               → patrones de auth
```

**DB:**
```
1. backend/prisma/schema.prisma          → estado actual del modelo
2. DOC de modelo de datos + ERD          → modelo lógico
3. backend/prisma/migrations/ (último)  → patrón SQL
```

**DevOps:**
```
1. docker-compose.yml                    → servicios, puertos, env vars
2. backend/.env.example                  → variables requeridas
3. frontend/nginx.conf (si aplica)       → routing/proxy
```

**Design (DL/UX):**
```
1. frontend/src/components/              → componentes existentes
2. DOC de design system                  → tokens por contexto
3. knowledge/design/                     → specs y assets
4. Wireframes / mockups aprobados        → diseño original
```

---

## Paso 3 — Escribir el ASSIGNMENT

**Ubicación:** `knowledge/agent-tasks/assignments/ASSIGNMENT_$TASK_ID_$SLUG.md`

### 8 elementos obligatorios:

```markdown
## 1. Estado actual del proyecto
- Branches abiertos: [lista]
- PRs pendientes de merge: [lista]
- Qué debe estar mergeado antes de empezar

## 2. APIs y servicios disponibles
| Endpoint | Método | Estado | Notas |
|----------|--------|--------|-------|
| /api/... | POST   | [OK]   | ...   |
| /api/... | GET    | [FALTA]| BE debe crear primero |

## 3. Arquitectura y estructura
- Carpetas del proyecto
- Patrones y convenciones
- Nomenclatura

## 4. Contexto de integración
- Cómo se conecta con el resto del sistema
- Dependencias con otros módulos

## 5. Entidades y modelos
(Copiar desde schema.prisma — NO inventar nombres de campos)
model NombreModelo {
  id    String @id
  ...
}

## 6. Recursos de diseño (si aplica)
- Wireframe: [ruta exacta]
- Design tokens: [ruta exacta]
- Mockup: [ruta exacta]

## 7. Checklist detallado (mínimo 10-15 items)
- [ ] Item 1
- [ ] Item 2
...

## 8. Archivos a revisar ANTES de empezar
| Archivo | Propósito |
|---------|-----------|
| ruta/exacta/archivo.ts | descripción |

## DOCUMENTOS DE REFERENCIA OBLIGATORIOS
Leer TODOS antes de comenzar. Sin estos documentos no se puede ejecutar la tarea.

| Documento | Tarea origen | Ruta exacta |
|-----------|-------------|-------------|
| Nombre doc | MS-XXX | phases/.../archivo.md |
```

---

## Paso 3.5 — Agregar sección de Living Documents al ASSIGNMENT

Según el tipo de tarea, incluir en el ASSIGNMENT qué Living Documents debe actualizar el agente.
Ver tabla completa en `00-platform/06.Documentos_soporte/LIVING_DOCUMENTS_MEMORY_SERVICE.md §5`.

Para tareas DB (4.2.x) → copiar checklist LD-01, LD-02 (+ LD-06 si hay índices)  
Para tareas BE (4.3.x) → copiar checklist LD-03, LD-04 (+ LD-05 si hay errores nuevos)  
Para tareas DO (4.1.x, 6.x) → copiar checklist LD-12 si hay variables de entorno  

```markdown
## Living Documents a actualizar (obligatorio antes de task_in_review)

Actualizar ANTES de mover a in_review. Incluir en SKL-REPORT-01 sección "Document Impacts".

- [ ] **LD-XX** `phases/.../archivo.md` — [qué actualizar]
- [ ] **LD-XX** `phases/.../archivo.md` — [qué actualizar]
```

Si la tarea no toca ningún Living Document → omitir la sección del ASSIGNMENT.

---

## Paso 4 — Linkear Trackable Items al ASSIGNMENT

Identificar qué RFs, NFRs, ADRs y BRs implementa esta tarea (ver SOP-TRK-01 §4).

```markdown
## Trackable Items linkeados (TL ya los registró en VTT)

| Código | Tipo | Título |
|--------|------|--------|
| RF-001 | rf   | El sistema permite registrar memorias |
| NFR-PERF-01 | rnf | GET /context < 500ms P95 |
| ADR-SA-004 | adr | X-Service-Key para autenticación |

**Acceptance Criteria en VTT** (visibles en la tarea — marcar como met/not_met al completar)
```

---

## Validación (checklist antes de entregar)

```
[ ] ¿Leí el brief completo incluyendo criterios de completitud?
[ ] ¿Identifiqué el tipo de entregable y qué datos necesita?
[ ] ¿Tracé cada dependencia a su documento concreto con ruta exacta?
[ ] ¿Verifiqué que esos documentos existen en el repo?
[ ] ¿Las tareas dependencia están en task_completed o task_approved?
[ ] ¿El ASSIGNMENT incluye la sección "Documentos de referencia OBLIGATORIOS"?
[ ] ¿Las rutas en el ASSIGNMENT son exactas (no aproximadas)?
[ ] ¿Los 8 elementos obligatorios están presentes?
[ ] ¿El checklist tiene mínimo 10 items verificables?
[ ] ¿El agente puede ejecutar SIN suponer nada?
[ ] ¿Incluí sección de Living Documents si la tarea toca BD, endpoints o infra?
[ ] ¿Incluí sección de Trackable Items linkeados (RFs, NFRs, ADRs que aplican)?
```

**Si algún check falla → NO entregar el assignment hasta resolverlo.**

---

## Error crítico a evitar

> El DL ejecutó wireframes (MS-029..035) sin leer User Flows, Site Map ni Personas — supuso 9 pantallas desde la SPEC. Costo: ~1M tokens en regeneración. Esta skill existe para evitar que se repita.
