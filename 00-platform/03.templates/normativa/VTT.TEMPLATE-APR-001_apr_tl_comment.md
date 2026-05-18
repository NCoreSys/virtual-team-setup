# TEMPLATE — APR-TL Comment (Aprobación del TL Reviewer)

| Campo | Valor |
|---|---|
| **Código** | `VTT.TEMPLATE-APR-001` |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-13 |
| **Aplica a** | TL Reviewer al cerrar una tarea |
| **Cuándo se usa** | FASE 4 — Cierre, paso 4.10 del SOP-ASG-001 |
| **Endpoint API** | `POST /api/tasks/:taskId/comments` (después del cierre con modelo dinámico, antes de `task_completed`) |
| **Límite VTT** | Comment ≤ 5000 chars |

---

## Notas de uso del template

- Reemplazar todos los `[PLACEHOLDER]` con valores reales
- El comment se postea **ANTES** de mover la tarea a `task_completed`
- Debe incluir resumen de **acciones del modelo dinámico aplicado** (TIs creados, evidencias, devlog resueltos)
- Si el verdict es **rechazado** → usar template diferente para `task_rejected` (no aplica este)
- Reglas críticas:
  - **R1**: Incluir todas las verificaciones (gates automáticos + manuales)
  - **R2**: Listar las acciones del modelo dinámico con conteo exacto
  - **R3**: Marker explícito de pendientes (PRs sin merge, PM approval pendiente)
  - **R4**: Si excede 5000 chars → dividir en 2 comments o subir como attachment

---

## Patrón base del comment APR-TL

```markdown
## APR-TL: [TASK_ID] aprobado por TL Reviewer

**Code review según `VTT.PROTOCOL-ASG-001` FASE 4 (Pasos 4.1-4.14):**

### Gates automáticos
- [x] Review Gate: canProceedToReview=true ([N] blockers, [N] warning low)
- [x] CAs: [N]/[N] met con evidencia válida
- [x] Devlog: [N] entries — todos resueltos por TL al cierre
- [x] Attachments: brief + assignment + devlog + code_logic + manifest v1.0
- [x] TIs heredados: [LISTA con linkType]
- [x] LD-[XX] declarado/actualizado [según aplique]

### Verificación manual
- [x] Entregables presentes: [lista de archivos/PRs producidos]
- [x] [Validación funcional específica de la tarea]
- [x] Hardcode Check: 0 findings critical/high reales ([N] FPs justificados)
- [x] PRs creados: [repo] #[N], [otro repo] #[M]
- [x] Branch base correcto (si encadenada: `feature/[ID_ANTERIOR]`)

### Acciones aplicadas al cerrar (modelo dinámico)
- [N] TIs nuevos creados y vinculados:
  - [CODE-001] ([tipo]) — [breve descripción]
  - [CODE-002] ([tipo]) — [breve descripción]
- Evidencias agregadas a [N] TIs con marker `[TASK:[TASK_ID]] [SPRINT:[SX]]`
- [N] devlog entries marcados resolved

### Pendientes operativos
- [Lista de pendientes — ej. PRs sin merge, valores reales por cargar]
- [Rebases necesarios si la branch está encadenada]

### Tech debts registradas para R2
- [CODE-XXX] — [descripción] (urgencia: baja|media|alta)

### Veredicto
APROBADO. Tarea movida a `task_completed`. Pendiente aprobación terminal PM.
```

---

## Ejemplos reales aplicados

### Ejemplo 1 — Tarea de documentación (MS-284 Environment Setup Guide)

```markdown
## APR-TL: MS-284 aprobado por TL Reviewer

**Code review según OPERATIVO TL Reviewer §6 (Pasos 6-16):**

### Gates automáticos
- [x] Review Gate: canProceedToReview=true (0 blockers, 1 warning low)
- [x] CAs: 9/9 met con evidencia
- [x] Devlog: 6 entries (4 decisions + 1 testing_note + 1 observation) — todos resueltos
- [x] Attachments: brief + assignment + devlog + code_logic placeholder + 5 manifests
- [x] TIs heredados: AS-001 (related_to), NFR-SEC-05 (related_to)
- [x] LD-15 declarado "sin cambios" en devlog observation

### Verificación manual
- [x] 4 docs producidos: README.md, docs/SETUP.md, docs/TROUBLESHOOTING.md, 4.1.2_environment_setup_guide.md
- [x] CA-04 validado: 59s clone limpio → entorno listo (target <1800s)
- [x] Cross-OS coverage: Linux/macOS/Windows en SETUP.md
- [x] Sin secretos reales en snippets — 2 FP de hardcode check justificados
- [x] PRs creados: backend #14, project #58

### Tech debt registrada (4 items en manifest)
- DEBT-DOCS-01 (urgencia baja): automatizar prisma migrate dev cuando MS-295 esté listo
- DEBT-DOCS-02 (urgencia baja): referencias a docker-compose.yml prod cuando MS-286 esté listo
- DEBT-INFRA-VTT-01 (urgencia baja): /document-impacts exige documentSourceId no accesible al DO
- PROC-MANIFEST-01 (urgencia media, retroactivo): paso 15 del workflow se ejecutaba antes del 14 — fix aplicado a MS-285 y MS-286

### Manifest auditable
v1.4 (attachment 8207d26d) — incluye delivery.skl_report_01_full con reporte FINAL del DO, 4 tech_debts, 7 notes_for_reviewer, git multi-repo (backend #14 + project #58 + 2 commits gap-close).

### Pendientes de proceso
- Branch base feature/MS-284 sobre feature/MS-283 — rebasar antes del merge final cuando MS-283 caiga a main.
- Review Gate exige code_logic para tareas documentation — discutir con PM si se relaja para categoria=documentation.

### Veredicto
APROBADO. Tarea movida a task_completed. Pendiente aprobación terminal PM.
```

### Ejemplo 2 — Tarea con modelo dinámico completo (MS-285 Environment Variables)

```markdown
## APR-TL: MS-285 aprobado por TL Reviewer

**Code review según OPERATIVO TL Reviewer §6 (Pasos 6-16):**

### Gates automáticos
- [x] Review Gate: canProceedToReview=true (0 blockers, 1 warning low)
- [x] CAs: 8/8 met con evidencia
- [x] Devlog: 6 entries (4 decisions + 1 testing_note + 1 observation) — todos resueltos por TL al cierre
- [x] Attachments: brief + assignment + devlog + code_logic (placeholder N/A) + manifest v1.0
- [x] TIs heredados: NFR-SEC-05 (implements), AS-001 (related_to), NFR-SEC-01 (related_to)
- [x] LD-12 declarado "sin cambios" en devlog observation

### Verificación manual
- [x] docs/SECRETS.md presente (336 líneas, 10 secciones)
- [x] 8 GH Secrets configurados en NCoreSys/memory-service-backend con placeholder
- [x] Secret real (hBCGEKm41BijI6jJ-...) NO aparece en repo backend (grep 0 matches)
- [x] Distribution log creado con 8 filas initial_placeholder
- [x] FP hardcode (5 matches auto-referenciales) justificados — patrón validado en MS-283/284

### Acciones aplicadas al cerrar (modelo dinámico)
- 3 TIs nuevos creados y diferidos a R2:
  - DEBT-INFRA-VTT-02 (tech_debt): gh secret set write-only
  - PROC-SECRETS-01 (process_improvement): canal seguro estandar PM→Servidor
  - PROC-REVIEW-01 (process_improvement): Review Gate exige code_logic
- Evidencias agregadas a 3 TIs vinculadas (PRs #15, #59)
- 6 devlog entries marcados resolved

### Pendientes operativos
- 8 placeholders pendientes de reemplazo por PM (canal seguro)
- Branch base feature/MS-285 sobre feature/MS-284 — rebasar antes del merge final

### Veredicto
APROBADO. Tarea movida a task_completed. Pendiente aprobación terminal PM.
```

---

## Comando API para postear

```bash
TOKEN=$(curl -s -X POST $BASE/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"$TL_UUID\",\"serviceKey\":\"$SERVICE_KEY\"}" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['token'])")

# El comment APR debe ir en una sola línea con \n para los saltos
APR_TEXT='## APR-TL: ... (multi-linea con \n)'

curl -s -X POST "$BASE/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"$APR_TEXT\",
    \"userId\": \"$TL_UUID\"
  }"
```

### Versión Python (recomendada para comments largos)

```python
import urllib.request, json, os, sys

BASE_URL = os.environ["VTT_BASE_URL"]
TASK_ID = sys.argv[1]
TL_UUID = os.environ["TL_UUID"]
TOKEN = os.environ["TOKEN"]

apr_text = """## APR-TL: {task_id} aprobado por TL Reviewer

**Code review según VTT.PROTOCOL-ASG-001 FASE 4:**

### Gates automáticos
- [x] Review Gate: canProceedToReview=true
...
""".format(task_id=TASK_ID)

# Validar tamaño antes de enviar
if len(apr_text) > 5000:
    sys.exit(f"ABORT: APR text excede 5000 chars ({len(apr_text)}). Dividir o usar attachment.")

body = json.dumps({"message": apr_text, "userId": TL_UUID}).encode()
req = urllib.request.Request(
    f'{BASE_URL}/api/tasks/{TASK_ID}/comments',
    data=body,
    headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
    method='POST'
)
response = json.loads(urllib.request.urlopen(req).read())
comment_id = response.get('data', {}).get('id')
print(f"APR-TL comment posted: {comment_id}")
```

---

## Secciones del template — qué incluir / qué evitar

### ✅ Incluir

- Conteos exactos (CAs met/total, devlog entries, TIs vinculados, FPs)
- Referencias a archivos producidos (paths o PR numbers)
- URLs específicas de PRs
- Códigos de TIs creados con tipo entre paréntesis
- Pendientes operativos concretos (no genéricos)
- Marcadores de manifest (versión, attachment ID si es relevante)

### ❌ Evitar

- "Funciona bien" / "Todo OK" → usar criterios verificables
- Texto narrativo largo → bullets concretos
- Repetir información del manifest → solo lo crítico para el review
- Cualquier secret real → usar placeholders o referencias documentadas

---

## Validación antes de mover a task_completed

Tras postear APR-TL, verificar:

```bash
# 1. Comment existe
curl -s "$BASE/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" | \
  jq '.data[] | select(.message | startswith("## APR-TL")) | {id, userId, createdAt}'

# 2. Devlog: 0 entries en pending
curl -s "$BASE/api/tasks/$TASK_ID/devlog" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.status != "resolved")) | length'
# Esperado: 0

# 3. Review Gate sigue OK
curl -s "$BASE/api/tasks/$TASK_ID/review-gate" -H "Authorization: Bearer $TOKEN" | \
  jq '.data.canProceedToReview'
# Esperado: true
```

Si los 3 pasan → mover a `task_completed`:

```bash
curl -s -X PATCH "$BASE/api/tasks/$TASK_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"statusId\": \"aa5ceb90-5209-42a2-b874-a8cbee597a97\",
    \"changedBy\": \"$TL_UUID\",
    \"reason\": \"APR-TL: aprobado tras code review + modelo dinámico aplicado\"
  }"
```

---

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| 400 "message too long" | Comment >5000 chars | Dividir en 2 comments o subir como attachment fileType=apr |
| 401 al postear | TOKEN expirado | Renovar token |
| Comment posted pero status no cambia | Olvidar el PATCH /status después | Ejecutar §Validación paso 4 |
| APR sin sección "Acciones aplicadas" | Olvido del modelo dinámico | Devolver tarea y aplicar FASE 4.8-4.9 antes |

---

## Referencias

- Endpoint: `POST /api/tasks/:taskId/comments` con `message` + `userId`
- Límite VTT: ≤5000 chars en `message`
- Documento padre: `VTT.PROTOCOL-ASG-001` FASE 4 — Cierre
- Skill relacionada: `SKL-DYNAMIC-MODEL-01` (genera las acciones a reportar)
- Template del rechazo: `VTT.TEMPLATE-REJ-001` (cuando no se aprueba) — pendiente

---

## Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Versión inicial — extraído del patrón APR-TL aplicado en MS-283/284/285 |
