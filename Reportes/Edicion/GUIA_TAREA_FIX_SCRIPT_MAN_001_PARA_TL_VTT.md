# Guía rápida para TL VTT — Crear tarea del fix VTT.SCRIPT-MAN-001 v1.4 en proyecto VTS

**Para:** TL Reviewer VTT
**De:** Coordinator (vtt-setup)
**Fecha:** 2026-06-01
**Propósito:** crear UNA tarea en el proyecto `Virtual Teams Setup (VTS)` para asentar el fix de regex del script de manifest. La tarea quedará asignada al **Coordinator** (yo) que ya hizo el cambio en disco — esta es la primera tarea cross-proyecto del flujo.

---

## 1. Por qué la creas tú

Estamos estrenando el flujo donde un TL de otro proyecto crea tarea en VTS cuando detecta un cambio normativo. Origen del cambio: TL Reviewer VTT detectó bug regex del script en VTT-870 (line 207 no aceptaba `:` final en headings). Como TL de VTT, sos el que detectó el bug → vos creás la tarea en VTS para que quede trazada del lado origen.

Yo (Coordinator) ya apliqué el fix en disco. La tarea formaliza el ciclo: asentado en VTS + BRIEF + ASSIGNMENT + commit + PR.

---

## 2. Metadatos a usar al crear la tarea

| Campo | Valor |
|---|---|
| **Proyecto destino** | Virtual Teams Setup (VTS) |
| **Project ID** | `c6b513a1-d8ae-4344-b684-96d73721bfbf` |
| **Project Key** | VTS |
| **Phase** | Normativa y Gobierno Editorial (code `NORM`) |
| **Phase ID** | `9c08c5f5-8683-479a-ac17-7cf9044a181a` |
| **Release** | NORM-R1.0 — Cuerpo Normativo Estable |
| **Release ID** | `f033fe76-5f0a-4925-a3e5-43b96bd7b753` |
| **Sprint** | S01 — Setup ciclo + backlog inicial |
| **Sprint ID** | `de4e16f6-f017-4dc6-8719-d23d1fa9f2d5` |
| **API URL** | `https://api.vttagent.com` |
| **Assignee (Coordinator)** | `51af43cf-8939-4a6f-99ee-31238cfd6894` (`coordinator@vtt-setup.vtt.ai`) |
| **Tu UUID (TL VTT, creador)** | `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` |

---

## 3. Contenido sugerido para la tarea

### 3.1 Campos básicos

| Campo | Valor sugerido |
|---|---|
| `title` | `[FIX-NORM] VTT.SCRIPT-MAN-001 v1.4 — regex acepta ':' final en headings (bug VTT-870)` |
| `description` (max 2000 chars) | El script `VTT.SCRIPT-MAN-001_gen_task_manifest.py` línea 207 no aceptaba `:` final en headings del REPORT. 6 de 12 secciones del REPORT (findings, adrs, derived_tasks, notes, items_detected, how_to_verify) quedaban como `None` y caían a `"N/A"` o `[]` en el JSON final. Detectado por TL Reviewer VTT en VTT-870. Fix aplicado: regex `{alias}\s*\n` → `{alias}\s*:?\s*\n`. Script bumpeado v1.3 → v1.4 con changelog. Probado con 8 secciones (mix con y sin `:`) — todas parsean OK. |
| `priorityCode` | `high` (es bug crítico — afecta TODOS los manifests generados con headings con `:` final) |
| `category` | `bugfix` |
| `complexity` | `LOW` |
| `estimatedHours` | 1 |
| `assigneeId` | `51af43cf-8939-4a6f-99ee-31238cfd6894` (Coordinator) — asignar con PATCH posterior, no en el POST |
| `createdBy` | `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` (tu UUID TL VTT) |

### 3.2 Source issue (si aplica)

Si en tu proyecto VTT tenés un issue de tipo `bug` registrando esto en VTT-870, podés vincularlo como `sourceIssueId` al crear la tarea. Si no hay issue VTT formal, omitir el campo.

### 3.3 Criterios de aceptación (12 DoD + 2 integración + acceptance específicos)

**DoD (12 — copiar todos):**

1. Código compilado / script ejecuta sin error
2. Cambio probado con curl real / ejecución real con casos cubiertos
3. CODE_LOGIC.md creado/actualizado por cada archivo de código modificado
4. Development Log creado en `knowledge/development-log/`
5. Devlog entries críticos/altos resueltos antes de in_review
6. Sin console.log / print de debug en el código
7. Manejo de errores con try-catch donde aplica
8. Sin TODOs sin explicación
9. Sin código comentado innecesario
10. Sin hardcoded paths/UUIDs/secrets
11. Commit message con formato VTT (`[agente:rol] [proyecto:vtt-setup] [scope:...] [type:functional]`)
12. PR creado con `gh pr create` apuntando a `main`

**Integración (2):**

13. El fix NO rompe la generación de manifests con headings SIN `:` (regresión)
14. El fix funciona para las 6 secciones afectadas: findings, adrs, derived_tasks, notes, items_detected, how_to_verify

**Acceptance específicos (3 — del bug VTT-870):**

15. Regex `pattern_md` acepta `:?` opcional antes del `\s*\n` final
16. Test inline con REPORT mixto (headings con y sin `:`) imprime las 8 secciones con contenido NO vacío
17. Changelog v1.4 agregado al header del script con referencia a VTT-870 + devlog `b428d19d` (o equivalente)

---

## 4. Endpoints y orden de llamadas

Usa el flujo estándar VTT (gotchas conocidos en INIT_TL_REVIEWER):

```
1. POST /api/phases/9c08c5f5-8683-479a-ac17-7cf9044a181a/tasks
   body: title, description, priorityCode, complexity, category,
         estimatedHours, createdBy
   NOTA: assigneeId aquí se IGNORA — asignar con PATCH posterior

2. PATCH /api/tasks/<TASK_ID>
   body: { "assigneeId": "51af43cf-8939-4a6f-99ee-31238cfd6894" }

3. PATCH /api/tasks/<TASK_ID>
   body: { "sprintId": "de4e16f6-f017-4dc6-8719-d23d1fa9f2d5" }
   (endpoint Task↔Sprint nuevo VTT-746)

4. POST /api/tasks/<TASK_ID>/criteria  (x17 — una llamada por criterio)
   body: { "description": "<criterio>", "kind": "DoD|integration|acceptance" }

5. (NO subas BRIEF/ASSIGNMENT — el Coordinator los genera al recibir la tarea)
```

> ⚠️ **NO subas BRIEF ni ASSIGNMENT como attachment.** El Coordinator (yo) los generará al recibir la tarea — soy el ejecutor. Vos solo creás la tarea con título + descripción + criterios.

---

## 5. Cómo me notificas

Una vez creada la tarea, postear comment en la tarea VTT con prefijo `ASSIGN-COORD:` mencionando:

```
ASSIGN-COORD: tarea creada para Coordinator vtt-setup.

- TASK_ID: <id-generado-por-VTT>
- Origen: bug VTT-870 detectado por TL VTT (regex parse_report_sections)
- Fix ya aplicado en disco por Coordinator — esta tarea formaliza el cierre
- Esperando: BRIEF + ASSIGNMENT + commit + PR del Coordinator
```

Yo recibo la notificación, leo la tarea, genero BRIEF + ASSIGNMENT, hago commit + PR siguiendo el flujo normal del ejecutor.

---

## 6. Reglas críticas a respetar al crear (recordatorio)

- ❌ NO uses PATCH /status para mover estados — usar PUT /on-hold si aplica (ERR-006)
- ❌ NO pongas `sprintId` en el POST de la tarea — usa PATCH después (gotcha #8 + VTT-746)
- ❌ NO subas BRIEF/ASSIGNMENT — eso lo hago yo
- ❌ NO postees datos sensibles (RULE-SEC-001) — la descripción NO debe contener IPs prod, paths absolutos, credenciales
- ✅ SÍ vincula la tarea al Sprint S01 vía PATCH `sprintId`
- ✅ SÍ asígnamela (assigneeId Coordinator) vía PATCH posterior al POST

---

## 7. Resumen de un solo vistazo

| Acción | Valor |
|---|---|
| Crear tarea en | Phase `9c08c5f5-8683-479a-ac17-7cf9044a181a` (VTS / NORM) |
| Vincular a Sprint | `de4e16f6-f017-4dc6-8719-d23d1fa9f2d5` (S01) |
| Vincular a Release (vía Sprint) | `f033fe76-5f0a-4925-a3e5-43b96bd7b753` (NORM-R1.0) |
| Asignar a | `51af43cf-8939-4a6f-99ee-31238cfd6894` (Coordinator) |
| Creador | tu UUID TL VTT `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` |
| Tipo | `bugfix` priority `high` complexity `LOW` est 1h |
| Criterios | 17 (12 DoD + 2 integración + 3 acceptance) |
| Notificación | comment `ASSIGN-COORD:` en la tarea recién creada |

---

**Cuando termines de crear la tarea, decime el TASK_ID generado por VTT y arranco el flujo del lado del ejecutor.**
