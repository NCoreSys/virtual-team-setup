# Entrega: VTT-725 — Refactor gen_mensaje.py → VTT.SCRIPT-MSG-001 con lectura formal del template + modo validate

## Lo que se hizo

Migración completa del script legacy `gen_mensaje.py` (5 copias dispersas en memory-service worktrees) al script canónico `VTT.SCRIPT-MSG-001_gen_mensaje.py` ubicado en el path normativo de la plataforma VTT (`$VTT_SETUP/02.normativa/04.Scripts/msg/`).

El refactor cumple dos reglas operativas nuevas: **RULE-SCRIPT-001** (path canónico único) y **RULE-TEMPLATE-001** (lectura formal del template, no hardcode en f-strings).

El script implementa 3 modos (`--output`, `--post`, `--validate`) con un sistema de validación de 3 bloques (A=secciones obligatorias, B=coherencia cruzada con VTT, C=higiene) que detecta exactamente el drift entre los mensajes correctos (formato MS-290) y los rotos (formato MS-333 con bug del wrapper `/devlog-entries`).

Se creó la skill `VTT.SKILL-MSG-001` en `03.Skills/msg/` (categoría MSG formalizada) y se marcó `VTT.SKILL-TASK-004` como DEPRECATED con redirect explícito a MSG-001.

## Código

- `00-platform/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py` — Script canónico nuevo (615 líneas, stdlib pura, 3 modos, 3 bloques de validación)
- `00-platform/02.normativa/03.Skills/msg/VTT.SKILL-MSG-001_gen_mensaje.md` — Skill nueva del sub-sistema MSG (creado)
- `00-platform/02.normativa/03.Skills/task/VTT.SKILL-TASK-004_mensaje_agente.md` — Modificado: marcado DEPRECATED con redirect a MSG-001 + changelog actualizado

## Development Log

`knowledge/development-log/2026-05-22_VTT-725_refactor-gen-mensaje.md` (pendiente de generar — el grueso del contexto está en el devlog decision posteado en VTT-725)

## Code Logic

- `knowledge/code-logic/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.LOGIC.md` — Documenta funciones principales, decisiones de diseño D1-D7, dependencias, pruebas ejecutadas, diff vs legacy

## Criterios de aceptación

| CA | Criterio | Resultado | Evidencia |
|---|---|---|---|
| CA-01 | Script vive en `$VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py` | met | Archivo creado en path canónico |
| CA-02 | Script lee `TEMPLATE_MENSAJE_ASIGNACION.md` v2.1 — `grep -c 'f".*###'` = 0 | met | `0` (verificado con grep) |
| CA-03 | Template actualizado con I1/I2/I3 bumped a v2.1 | met | Hecho por PM en OLA 1 antes de este refactor |
| CA-04 | `--validate` sobre `MENSAJE_MS-290.md` → `valid: true` | met | Output: `{"valid": true, "findings": [warning I1, info B skip]}` |
| CA-05 | `--validate` sobre `MENSAJE_MS-333.md` → `valid: false` con findings | met | Output: `{"valid": false, "findings": [9 errors]}` — Bloque A: 7 errors, Bloque C: 2 errors |
| CA-06 | `--post` para tarea de prueba (MS-328) sin placeholders sin resolver | met | 3 comments posteados (`2a432f91...`, `63dce168...`, `edc482a5...`), 0 placeholders, validate interno `valid:true` |
| CA-07 | 5 copias legacy eliminadas en memory-service worktrees | not_met (delegado al TL) | El cleanup es paso operativo del TL — guía `CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md` |
| CA-08 | PROTOCOL-ASG-001 §5.2.13 actualizado | met | Hecho por PM en OLA 1 (v1.4.0) |
| CA-09 | `VTT.SKILL-MSG-001` creada en `03.Skills/msg/` | met | Archivo creado con contrato completo + 3 modos + validación A/B/C documentada |
| CA-10 | `VTT.SKILL-TASK-004` marcada deprecated | met | Banner `🛑 DEPRECATED` + redirect MSG-001 + changelog `2026-05-22` |
| CA-11 | Devlog decision registrando el cambio | met | Comment id `d1206bb9-b0e7-42a5-bafd-6bec16f18784` posteado en VTT-725 |
| CA-12 | `code_logic` del script generado | met | `knowledge/code-logic/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.LOGIC.md` |

## Devlog entries registrados en VTT

| Categoría | Severidad | Título | Estado |
|---|---|---|---|
| decision | low | Refactor gen_mensaje.py: path legacy -> canonico (VTT.SCRIPT-MSG-001) | pending |

## Findings / Deuda técnica

**F-01 (low)** — `ROLE_BY_EMAIL` y `PHASE_MAP` viven hardcoded en el script. Para escalabilidad multi-proyecto convendría migrarlos a un catálogo en `$VTT_SETUP/02.normativa/05.Catalogs/` cuando esa carpeta exista. Documentado en code_logic §9 (Migración futura sugerida).

**F-02 (low)** — Modo `--dry-run` (combinaría `--output` + `--validate` en un solo paso) podría agregarse en una iteración futura. Hoy se cubre con dos invocaciones consecutivas.

## ADRs tomados

**ADR-1** — stdlib pura (urllib en vez de `requests`): el script debe correr en cualquier worktree sin `pip install`, mismo patrón que `VTT.SCRIPT-MAN-001`/`SCRIPT-EXM-001`. Sin dependencias externas.

**ADR-2** — `strip_variant` antes de `resolve_placeholders`: si se resuelven los placeholders primero, los markers HTML quedan adentro de bloques expandidos y el regex puede no encontrarlos. Strip first, resolve second.

**ADR-3** — `--post` ejecuta `--validate` interno antes de postear (R4 de la skill): previene postear mensajes con el bug del wrapper `/devlog-entries`. Si validate falla → exit 4 sin postear.

**ADR-4** — Skip Bloque B sin token: permite ejecutar `--validate` offline sobre archivos locales. El skip se reporta como `severity: info` (no error).

## TrackableItems creados o vinculados

N/A

## Items detectados para trackeo (TL revisar)

| Tipo sugerido | Código sugerido | Descripción breve | Retroactivo? | Urgencia |
|---|---|---|---|---|
| DEBT | DEBT-MSG-001 | Catalogar `ROLE_BY_EMAIL` y `PHASE_MAP` a archivo externo cuando exista `05.Catalogs/` | No | low |

## Tareas derivadas generadas

N/A (el cleanup de las 5 copias legacy lo ejecuta el TL siguiendo `CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md`)

## Cómo verificar

```bash
# 1. CA-02 — sin f-strings con headings
grep -c 'f".*###' "$VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py"
# Esperado: 0

# 2. CA-04 — MS-290 debe pasar
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  --validate c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl/knowledge/agent-tasks/messages/04-development/S01/MENSAJE_MS-290.md
# Esperado: {"valid": true, ...}

# 3. CA-05 — MS-333 debe fallar
python $VTT_SETUP/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py \
  --validate c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl/knowledge/agent-tasks/messages/04-development/S01/MENSAJE_MS-333.md
# Esperado: {"valid": false, "findings": [9 errors]}, exit 4

# 4. CA-06 — --post end-to-end contra MS-328 (ya ejecutado)
# Verificar comments en MS-328:
curl -s "http://77.42.88.106:3000/api/tasks/MS-328/comments" -H "Authorization: Bearer $TOKEN" | python -c "import sys,json; d=json.load(sys.stdin).get('data',[]); print([c['id'][:8] for c in d[-3:]])"
```

## Notas

- VTT-725 no tiene `sprint` asignado al momento del cierre — phase `09-mejoras`, sprint placeholder `S00`.
- VTT-725 no tiene CAs creados en VTT (el PM las puede crear como parte del review). Este reporte documenta los 12 CAs del brief original con su evidencia.
- El cleanup de las 5 copias legacy (CA-07) NO está hecho por mí — el PM aclaró que es paso operativo del TL con guía dedicada. Lo dejé como `not_met` por transparencia, no por falla.

## Review gate al entregar

`canProceedToReview: true` (target) — 1 entry de devlog (decision), 1 pending. Severidad `low` (no bloqueante en gate D-41).

## Commit

`refactor(msg) [VTT-725]: gen_mensaje.py -> VTT.SCRIPT-MSG-001 canonico + skill MSG-001`
SHA: pendiente (se generará al hacer el commit final)

## PR

note: PR pendiente — el agente BE no tiene permiso de push directo a `virtual-teams-setup` main. El TL crea el PR como parte de FASE 4.5 del PROTOCOL-ASG-001 con los siguientes archivos en el commit:
- Script nuevo en `00-platform/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py`
- Skill nueva en `00-platform/02.normativa/03.Skills/msg/VTT.SKILL-MSG-001_gen_mensaje.md`
- Skill TASK-004 modificada (deprecated banner)
- code_logic en `knowledge/code-logic/02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.LOGIC.md`
- Este reporte en `knowledge/task-manifests/09-mejoras/S00/VTT-725_REPORT.md`
- Manifest v1.0 generado por VTT.SCRIPT-MAN-001
