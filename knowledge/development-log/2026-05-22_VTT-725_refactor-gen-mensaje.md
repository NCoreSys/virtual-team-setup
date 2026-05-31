# Development Log — VTT-725: Refactor gen_mensaje.py → VTT.SCRIPT-MSG-001

| Campo | Valor |
|---|---|
| **Fecha** | 2026-05-22 |
| **Tarea** | VTT-725 — [Refactor] gen_mensaje.py → VTT.SCRIPT-MSG-001 con lectura formal del template + modo validate |
| **Fase** | Fase 9 — Mejoras y Pendientes |
| **Sprint** | S00 (sin sprint formal) |
| **Repo** | `virtual-teams-setup` (rama actual: `agent/pm/vtt-setup/skills-gobierno-edicion-fase-desarrollo`) |
| **Agente** | Backend API Specialist (`8834830b-578f-46be-933b-0abcbbc5da99`) |
| **Estimación** | 6h |
| **Tiempo real** | ~3.5h (sesión continua) |

---

## 1. Resumen ejecutivo

Refactor del script legacy `gen_mensaje.py` (que vivía en 5 copias dispersas en worktrees de `memory-service`) al script canónico de plataforma `VTT.SCRIPT-MSG-001_gen_mensaje.py` ubicado en el path normativo de VTT.

El refactor cumple dos reglas operativas nuevas activadas en OLA 1:
- **`RULE-SCRIPT-001`** — path canónico único para scripts (prohibido copias locales)
- **`RULE-TEMPLATE-001`** — lectura formal del template (prohibido hardcode del formato en f-strings)

El script implementa 3 modos de operación (`--output`, `--post`, `--validate`) con un sistema de validación de 3 bloques (A=secciones obligatorias, B=coherencia cruzada con VTT, C=higiene) que detecta exactamente el drift entre los mensajes correctos (formato MS-290) y los rotos (formato MS-333 con bug del wrapper `/devlog-entries`).

Se creó también la skill `VTT.SKILL-MSG-001` (categoría MSG formalizada en OLA 1) y se marcó `VTT.SKILL-TASK-004` como DEPRECATED con redirect explícito.

---

## 2. Archivos creados / modificados

### En repo `virtual-teams-setup`

| # | Path | Tipo | Bytes |
|---|---|---|---:|
| 1 | `00-platform/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py` | NUEVO — script canónico | 34.773 |
| 2 | `00-platform/02.normativa/03.Skills/msg/VTT.SKILL-MSG-001_gen_mensaje.md` | NUEVO — skill MSG-001 | 10.536 |
| 3 | `00-platform/02.normativa/03.Skills/task/VTT.SKILL-TASK-004_mensaje_agente.md` | MODIFICADO — banner DEPRECATED + changelog | 10.244 |
| 4 | `knowledge/code-logic/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.LOGIC.md` | NUEVO — code logic | 13.267 |
| 5 | `knowledge/task-manifests/09-mejoras/S00/VTT-725_REPORT.md` | NUEVO — reporte 16 secciones | 8.306 |
| 6 | `knowledge/task-manifests/09-mejoras/S00/VTT-725.json` | NUEVO — manifest v1.0 | 8.374 |
| 7 | `knowledge/task-manifests/09-mejoras/S00/VTT-725.manifest.md` | NUEVO — wrapper del manifest | 8.426 |
| 8 | `knowledge/development-log/2026-05-22_VTT-725_refactor-gen-mensaje.md` | NUEVO — **este archivo** | — |

### NO modifiqué (trabajos del PM en este branch)

Hay ~59 archivos modificados + decenas de archivos untracked en `agent/pm/vtt-setup/skills-gobierno-edicion-fase-desarrollo` que son **trabajo en curso del PM** (setups, init-messages, protocols legacy, etc.). **NO los toqué.**

---

## 3. Decisiones técnicas

### D1 — stdlib pura (sin `requests` / `httpx`)

**Decisión**: usar solo `urllib.request`, `json`, `argparse`, `re`.

**Razón**: el script debe correr en cualquier worktree sin `pip install`. Mismo patrón que `VTT.SCRIPT-MAN-001` y `VTT.SCRIPT-EXM-001`.

**Trade-off**: código un poco más verboso para multipart/form-data, pero portabilidad total.

### D2 — `strip_variant()` antes de `resolve_placeholders()`

**Decisión**: borrar la variante A/B del template antes de resolver `{{VAR}}`.

**Razón**: si resuelvo placeholders primero, los markers HTML `<!-- VARIANTE A -->` quedan adentro de bloques expandidos y el regex puede no encontrarlos por interpolación de variables.

**Implementación**: regex sobre el template raw, detección de markers, partición en `[pre] + [chosen] + [post]`, limpieza de comentarios.

### D3 — `--post` ejecuta `--validate` interno antes de postear

**Decisión**: regla R4 de la skill. El modo `--post` corre `validate_message()` sobre el archivo generado y si retorna `valid:false` aborta con exit 4 sin postear.

**Razón**: prevenir que vuelva a propagarse el bug del wrapper `/devlog-entries` que motivó la refactorización (caso MS-333).

### D4 — Skip Bloque B sin token

**Decisión**: si `--validate <path>` se invoca sin TOKEN en env, el Bloque B (coherencia cruzada con VTT) se reporta como `severity: info` "skipped" en vez de error.

**Razón**: permitir validar mensajes locales offline. Los bloques A (secciones) y C (higiene) son suficientes para detectar el drift estructural sin necesidad de consultar VTT.

### D5 — `effective_size = chunk_size - 8` en chunking

**Decisión**: reservar 8 chars del límite de 5000 para el prefijo `[N/M]\n` cuando se hace chunking.

**Razón**: heredado del fix anterior — primera versión usaba `chunk_size = 5000` sin reserva, el prefijo `[1/2]\n` agregaba 6 chars y daba 5006 → HTTP 400. Con reserva de 8 hay margen para `[10/10]\n`.

### D6 — `ROLE_BY_EMAIL` como dict in-source

**Decisión**: mantener el mapping email→agente hardcoded en el script en vez de cargarlo de un archivo externo.

**Razón**: scope actual = Memory Service. Para escalar a más proyectos, considerar migrar a `$VTT_SETUP/02.normativa/05.Catalogs/` cuando esa carpeta exista. Documentado como F-01 (deuda técnica low).

### D7 — Acepta 2 convenciones de email

**Decisión**: el mapping acepta tanto `memory-service.<rol>@vtt.ai` como `<rol>@memory-service.vtt.ai`.

**Razón**: hay legacy de ambas convenciones en VTT. Aceptar las dos evita falsos negativos al detectar el agente asignado.

---

## 4. Pruebas ejecutadas

### CA-02 — sin f-strings con headings

```bash
$ grep -c 'f".*###' VTT.SCRIPT-MSG-001_gen_mensaje.py
0
```

✅ Pasa (template se lee como archivo, no se hardcodea formato).

### CA-04 — `--validate MENSAJE_MS-290.md`

```json
{
  "valid": true,
  "findings": [
    {"block": "A", "severity": "warning", "msg": "Falta referencia a VTT.SKILL-REPORT-001 (instruccion I1)"},
    {"block": "B", "severity": "info", "msg": "Bloque B skipped (sin token)"}
  ]
}
```

✅ Pasa con 1 warning informativo (I1 es nueva en v2.1) + 1 info (skip B).

### CA-05 — `--validate MENSAJE_MS-333.md`

```json
{
  "valid": false,
  "findings": [
    {"block": "A", "severity": "error", "msg": "Falta seccion 'WORKING DIRECTORY'"},
    {"block": "A", "severity": "error", "msg": "Falta 'Execution manifest:' con path .vtt/manifests/<TASK_ID>.execution.json"},
    {"block": "A", "severity": "error", "msg": "Falta seccion 'NORMATIVA DE REFERENCIA' (Reglas aplicables)"},
    {"block": "A", "severity": "error", "msg": "Falta invocacion de VTT.SCRIPT-MAN-001_gen_task_manifest.py"},
    {"block": "A", "severity": "error", "msg": "Falta seccion 'ENTREGABLES AL CERRAR'"},
    {"block": "A", "severity": "error", "msg": "Falta definicion de '$VTT_SETUP=...'"},
    {"block": "A", "severity": "error", "msg": "Falta seccion 'QUE PASA DESPUES'"},
    {"block": "C", "severity": "error", "msg": "POST a /devlog-entries SIN wrapper '{entries:[...]}'"},
    {"block": "C", "severity": "error", "msg": "Endpoint incorrecto 'POST /criteria/.../fulfill'"}
  ]
}
```

✅ Pasa con **9 errors detectados** (7 estructurales + 2 de endpoints). Exit code 4 (validate failed) — esperado.

### CA-06 — `--post` end-to-end contra MS-328

```json
{
  "success": true,
  "mode": "post",
  "output_path": "c:/.../MENSAJE_MS-328.md",
  "comment_ids": ["2a432f91-9ac3-4d28-8c90-9c3867b5542d", "63dce168-67ce-4c7e-ba30-7119a8b58d5f", "edc482a5-4fb6-45e1-be16-00537b536bbc"],
  "chunks": 3,
  "rendered_size": 11287,
  "variant": "A",
  "validation_warnings": []
}
```

✅ Pasa: 3 chunks posteados (`[1/3]`, `[2/3]`, `[3/3]`), 0 placeholders sin resolver, validate interno `valid: true`.

---

## 5. Cómo probar / validar

### Test 1 — Script válido sintácticamente

```bash
python -c "import py_compile; py_compile.compile(r'C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\00-platform\02.normativa\04.Scripts\msg\VTT.SCRIPT-MSG-001_gen_mensaje.py', doraise=True)"
# Esperado: nada (silenciosa) → OK
```

### Test 2 — CA-02 (sin f-strings con headings)

```bash
grep -c 'f".*###' $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py
# Esperado: 0
```

### Test 3 — Validate sobre mensaje correcto

```bash
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  --validate <path al mensaje>
# Esperado: {"valid": true, ...}
```

### Test 4 — Generar mensaje nuevo

```bash
export VTT_SETUP=c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  MS-XXX \
  --output /tmp/preview.md \
  --project-root c:/Users/Martin/Documents/virtual-teams/memory-service \
  --vtt-setup $VTT_SETUP
# Esperado: exit 0 + archivo escrito + JSON con success:true
```

---

## 6. Dependencias

### Librerías
- Python ≥3.8 (uso de f-strings, `dict` ordenado, `subprocess` opcional)
- **Solo stdlib** — sin `pip install`

### Externas
- VTT backend API en `http://77.42.88.106:3000`
- Endpoint `/api/auth/service-token` para JWT
- Endpoints `/api/tasks/:id`, `/criteria`, `/comments`, `/attachments`, `/devlog`

### Documentos / Templates
- **Template canónico**: `$VTT_SETUP/03.templates/tarea/TEMPLATE_MENSAJE_ASIGNACION.md v2.1` (creado por PM en OLA 1)
- **Skill predecesora**: `VTT.SKILL-TASK-004` (ahora DEPRECATED)

---

## 7. Issues resueltos / detectados

### Resueltos
- ✅ Bug del wrapper `/devlog-entries` (caso MS-333) — el template v2.1 usa `/devlog` singular y el `--validate` Bloque C detecta el patrón roto
- ✅ Drift entre formato MS-290 (correcto) vs MS-333 (legacy) — bloques A/B/C cubren ambos
- ✅ Hardcode del formato en f-strings — refactor a lectura formal del template (RULE-TEMPLATE-001)
- ✅ Copias dispersas del script — path canónico único (RULE-SCRIPT-001)

### Detectados (deuda técnica para futuro)

**F-01 (low)** — `ROLE_BY_EMAIL` y `PHASE_MAP` viven hardcoded en el script. Migrarlos a un catálogo externo cuando exista `$VTT_SETUP/02.normativa/05.Catalogs/`.

**F-02 (low)** — Modo `--dry-run` (combinaría `--output` + `--validate` en una sola invocación). Hoy se cubre con dos invocaciones consecutivas.

**F-03 (low)** — El script `VTT.SCRIPT-MAN-001` exige `git.note` cuando no hay `git.pr_url`, pero **no parsea el campo `note:` del reporte .md** (solo parsea `pr_url` y `commit_sha`). Esto obliga a workarounds cuando el agente no tiene push rights al repo (caso real durante este refactor). Sugerencia de fix: agregar parsing de `note:` en `parse_report()` del MAN-001.

---

## 8. Criterios de aceptación

| CA | Criterio | Resultado |
|---|---|:---:|
| CA-01 | Script en path canónico `$VTT_SETUP/02.normativa/04.Scripts/msg/...` | ✅ met |
| CA-02 | `grep -c 'f".*###' script` = 0 | ✅ met |
| CA-03 | Template v2.1 con I1/I2/I3 | ✅ met (PM lo hizo en OLA 1) |
| CA-04 | `--validate MS-290.md` → `valid: true` | ✅ met |
| CA-05 | `--validate MS-333.md` → `valid: false` con findings | ✅ met (9 errors) |
| CA-06 | `--post` para tarea de prueba sin placeholders | ✅ met (MS-328) |
| CA-07 | 5 copias legacy eliminadas | ⚠️ delegado al TL |
| CA-08 | PROTOCOL-ASG-001 §5.2.13 actualizado | ✅ met (PM lo hizo en OLA 1) |
| CA-09 | `VTT.SKILL-MSG-001` creada | ✅ met |
| CA-10 | `VTT.SKILL-TASK-004` deprecated | ✅ met |
| CA-11 | Devlog decision en VTT-725 | ✅ met (comment `d1206bb9-...`) |
| CA-12 | code_logic generado | ✅ met |

**Score: 11/12 met + 1 delegado al TL.**

---

## 9. Inventario de attachments en VTT-725

| Tipo | Attachment ID | Archivo |
|---|---|---|
| devlog (resumen) | `988ea40e-cbe7-4d62-8b65-da8269823460` | `VTT-725_devlog.md` (resumen ejecutivo) |
| code_logic | `96423c40-f03d-4d16-8987-fafbbcce808a` | `VTT.SCRIPT-MSG-001_gen_mensaje.LOGIC.md` |
| manifest | `3b524204-973b-41b9-bac9-1f9bb7c703b7` | `VTT-725.manifest.md` (v1.0) |
| development_log (este archivo) | _por subir_ | `2026-05-22_VTT-725_refactor-gen-mensaje.md` |

**Comments posteados:**
- `d1206bb9-b0e7-42a5-bafd-6bec16f18784` — devlog decision (CA-11)
- `4676f9ef-0b96-43b1-8126-2d11484bce14` — extracto del reporte SKL-REPORT-01

---

<<<<<<< HEAD
## 10. PR creado + bypass del hook autorizado por PM

### Bypass del hook commit-msg — autorización temporal del PM

Durante el cierre de VTT-725 se detectó que el hook `.git/hooks/commit-msg` de `virtual-teams-setup` llama a `VTT.SCRIPT-GIT-001_validate_branch_and_commit.py`, pero ese script **no existe todavía en `main`** (está en el trabajo de gobernanza en curso del PM en otra rama).

Esto bloqueaba el cierre de VTT-725. El PM autorizó explícitamente desactivar el hook temporalmente para esta tarea:

```bash
# Paso 1: Desactivar
mv .git/hooks/commit-msg .git/hooks/commit-msg.disabled

# Paso 2: Commit + push + PR con formato convencional
git commit -m "refactor(msg) [VTT-725]: ..."
git push origin feature/VTT-725
gh pr create --base main ...

# Paso 3: Re-activar al terminar
mv .git/hooks/commit-msg.disabled .git/hooks/commit-msg
```

**Por qué fue necesario**: la gobernanza commit-msg del repo está incompleta — espera un script que aún no se mergeó a `main`. El PM completará la gobernanza en sesión posterior y reescribirá los commits si hace falta.

**Sin riesgo permanente**: ningún hook se modificó (solo se renombró temporalmente). Al terminar este flujo el hook vuelve a estar activo.

### Pasos ejecutados para crear el PR

1. Stash del trabajo del PM en `agent/pm/vtt-setup/skills-gobierno-edicion-fase-desarrollo`
2. Checkout main + crear branch `feature/VTT-725`
3. Restaurar 8 archivos desde backup `/tmp/VTT-725-backup`
4. `git add` explícito de cada archivo (sin `-A`)
5. Commit con formato convencional + Co-Authored-By
6. Push + `gh pr create`
7. Re-activar hook al final
8. Volver al branch del PM + restaurar stash
=======
## 10. PR pendiente

**Nota importante**: el agente BE NO tiene push rights al branch `agent/pm/vtt-setup/skills-gobierno-edicion-fase-desarrollo` actual de `virtual-teams-setup` (es trabajo en curso del PM).

Para crear el PR de VTT-725 se requiere:
1. Crear branch limpio desde `main`: `feature/VTT-725`
2. Copiar **solo** los 8 archivos listados en §2 (no incluir los archivos del PM)
3. `git push origin feature/VTT-725`
4. `gh pr create --base main --title "[VTT-725] Refactor gen_mensaje.py → VTT.SCRIPT-MSG-001"`

**Esto requiere autorización explícita del PM** para asegurar que no se mezcla con su trabajo en curso.
>>>>>>> agent/pm/vtt-setup/skills-gobierno-edicion-fase-desarrollo

---

## 11. Próximos pasos

1. **PM/TL aprueba este devlog + reporte**
2. **TL ejecuta cleanup de las 5 copias legacy** según `CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md` (CA-07)
3. **TL crea el PR** con los 8 archivos a `main` de `virtual-teams-setup`
4. **TL ejecuta script v1.5** del manifest (FASE 4.5 del PROTOCOL-ASG-001) para enriquecimiento
5. **PM aprueba el PR del TL**

---

## 12. Referencias

- Tarea: VTT-725
- Skill nueva: `VTT.SKILL-MSG-001`
- Skill deprecada: `VTT.SKILL-TASK-004`
- Template: `TEMPLATE_MENSAJE_ASIGNACION.md v2.1`
- Reglas: `RULE-SCRIPT-001`, `RULE-TEMPLATE-001`
- Protocol: `VTT.PROTOCOL-ASG-001 §5.2.13` (v1.4.0)
- Caso de drift: MS-333 (rotos) vs MS-290 (correcto)
- Cleanup pendiente: `CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md` (ejecutado por TL)
