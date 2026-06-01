# `_autoria/` — Templates para autores de la normativa

Esta carpeta contiene los **moldes** que el autor (PM/TL) usa para crear nuevos documentos normativos en los 4 niveles del modelo VTT.

| Campo | Valor |
|---|---|
| **Versión** | 1.1 |
| **Fecha** | 2026-05-31 |
| **Mantenedor** | PM Martin Rivas |
| **Audiencia** | Quien va a escribir un Protocol / Workflow / Skill / Script / **CARD** nuevo |

> **v1.1 (2026-05-31):** Agregado `TEMPLATE_CARD.md` (Nivel R). Ver `README.md` §2.4.bis y `GUIA_AUTOR.md` §4.5/§4.6 para detalles del Nivel R.

---

## 1. Templates disponibles

| Template | Para crear | Destino del archivo creado | Tipo |
|---|---|---|---|
| `TEMPLATE_PROTOCOL.md` | Un Protocol nuevo (Nivel 4) | `02.normativa/01.Protocols/` | Markdown |
| `TEMPLATE_WORKFLOW.md` | Un Workflow nuevo (Nivel 3) | `02.normativa/02.Workflows/` | Markdown |
| `TEMPLATE_SKILL.md` | Una Skill nueva (Nivel 2) | `02.normativa/03.Skills/<categoria>/` | Markdown |
| `TEMPLATE_SCRIPT.py` | Un Script nuevo (Nivel 1) | `02.normativa/04.Scripts/<categoria>/` | Python |
| `TEMPLATE_CARD.md` | Una CARD nueva (Nivel R Runtime) | `02.normativa/05.Cards/<categoria>/` | Markdown |

---

## 2. Cómo usar un template

### Paso 1 — Decidir el nivel

Antes de copiar nada, verificar que estás creando algo del nivel correcto. Ver `02.normativa/README.md` §3 — Tabla decisoria:

| Pregunta | Si la respuesta es SÍ |
|---|---|
| ¿Cubre proceso de negocio end-to-end con varias fases y roles? | → **Protocol** (Nivel 4) |
| ¿Es un sub-procedimiento con pasos secuenciales fijos sin decisiones mayores? | → **Workflow** (Nivel 3) |
| ¿Es una capacidad reusable con inputs/outputs contractuales que orquesta scripts? | → **Skill** (Nivel 2) |
| ¿Es un comando atómico ejecutable? | → **Script** (Nivel 1) |
| ¿Es una vista runtime comprimida del happy path de un Workflow para inyectar al prompt del agente? | → **CARD** (Nivel R) — requiere Workflow padre existente (1:1) |

### Paso 2 — Asignar código

Pattern: `VTT.<NIVEL>-<CAT>-<NNN>[.<MMM>]_<titulo_snake_case>.<ext>`

| Nivel | Pattern | Ejemplo |
|---|---|---|
| Protocol | `VTT.PROTOCOL-<CAT>-<NNN>_<titulo>.md` | `VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` |
| Workflow | `VTT.WORKFLOW-<CAT>-<NNN>.<MMM>_<titulo>.md` | `VTT.WORKFLOW-ASG-001.003_generar_briefs.md` |
| Skill | `VTT.SKILL-<CAT>-<NNN>_<titulo>.md` | `VTT.SKILL-ATTACH-001_subir_attachment.md` |
| Script | `VTT.SCRIPT-<CAT>-<NNN>_<titulo>.py` | `VTT.SCRIPT-ATTACH-001_post_attachment_multipart.py` |
| CARD | `VTT.CARD-<CAT>-<NNN>_<titulo>.md` | `VTT.CARD-EXE-004_agente_ejecuta_workflow_assignment.md` |

**Cómo encontrar el `<NNN>` siguiente disponible:**

```bash
cd 00-platform/02.normativa/<carpeta>
ls VTT.<NIVEL>-<CAT>-*.md | sort
# Toma el último número + 1
```

**Categorías estándar (`<CAT>`):**

Ver el registro maestro en `02.normativa/00_REGISTRO_ACRONIMOS.md` §3.

> **Antes de elegir `<CAT>`:**
> 1. Abrir `02.normativa/00_REGISTRO_ACRONIMOS.md`
> 2. Confirmar que el acrónimo existe en §3.1 (Activas)
> 3. Si no existe → seguir el procedimiento §5 del registro para agregarlo PRIMERO
> 4. **NO uses un acrónimo no registrado** — el review lo rechazará

Checklist de paso 2:
- [ ] Verifiqué que `<CAT>` está en `00_REGISTRO_ACRONIMOS.md` §3.1 (Activas)
- [ ] Si fue necesario, lo agregué siguiendo §5 del registro
- [ ] Verifiqué que `<NNN>` siguiente disponible no choca con archivos existentes

### Paso 3 — Copiar y rellenar

```bash
# Ejemplo: crear un Workflow nuevo
cp 03.templates/normativa/_autoria/TEMPLATE_WORKFLOW.md \
   02.normativa/02.Workflows/VTT.WORKFLOW-ASG-001.003_generar_briefs.md

# Editar y reemplazar todos los <placeholders>
# Borrar el bloque de instrucciones del autor (al inicio del template)
```

### Paso 4 — Validar con checklist

Cada template termina con secciones obligatorias. Verifica:

**Protocol:**
- [ ] Header con metadata completa
- [ ] §1-§7 + Anexos
- [ ] §6 Referencias Cruzadas (Workflows, Skills, Reglas Nivel 0)
- [ ] Diagrama mermaid en Anexo A (opcional pero recomendado)

**Workflow:**
- [ ] Header indica a qué Protocol pertenece
- [ ] §2 Inputs contractuales claros (tabla con tipo + origen)
- [ ] §5 Pasos numerados con decisiones intermedias documentadas
- [ ] §6 Outputs definidos
- [ ] §9 Skills invocadas listadas

**Skill:**
- [ ] Inputs contractuales (NO específicos del contexto)
- [ ] Variables del entorno listadas
- [ ] Ejecución referencia un Script (o lógica inline ≤5 líneas)
- [ ] Validación con códigos HTTP esperados

**Script:**
- [ ] Docstring header completo (Propósito + Idempotencia + Inputs + Outputs + Exit codes)
- [ ] argparse (NO hardcode de inputs)
- [ ] Stdout en JSON
- [ ] Exit codes 0/1/2/3
- [ ] Sin secrets hardcoded

### Paso 5 — Actualizar referencias cruzadas

Después de crear el documento, actualizar:

| Si creaste... | Actualiza... |
|---|---|
| Un Protocol | `02.normativa/INVENTARIO.md` + lista en `README.md` §3 |
| Un Workflow | Tabla §6 del Protocol padre + `INVENTARIO.md` |
| Una Skill | `INVENTARIO.md` + tabla §9 de Workflows que la invocan |
| Un Script | Tabla "Scripts invocados" en Skills que lo invocan |

---

## 3. Anti-patterns comunes (qué NO hacer)

### Anti-pattern 1 — Skill específica del contexto

**❌ Mal:**
```
SKILL-BRIEF-UPLOAD-001    "Subir BRIEF a tarea"
SKILL-DEVLOG-UPLOAD-001   "Subir devlog a tarea"
SKILL-MANIFEST-UPLOAD-001 "Subir manifest a tarea"
```

**✅ Bien:**
```
SKILL-ATTACH-001 "Subir attachment a tarea"
   Inputs: task_id, file_path, file_type, uploaded_by
   → 1 Skill reusable; el Workflow le pasa file_type según corresponda
```

### Anti-pattern 2 — Mezclar niveles

**❌ Mal:** Documento llamado "Protocol" pero que solo tiene pasos secuenciales sin decisiones de negocio → es un Workflow.

**❌ Mal:** Documento llamado "Workflow" pero con 5 fases y 4 roles distintos → es un Protocol.

**✅ Bien:** Aplicar la tabla decisoria del §3 del README de normativa.

### Anti-pattern 3 — Script con lógica de negocio

**❌ Mal:** Script de 200 líneas que decide qué endpoint llamar según el contexto.

**✅ Bien:** Script atómico de 50 líneas que hace 1 cosa (1 HTTP call). La lógica de "qué endpoint" vive en la Skill que orquesta.

### Anti-pattern 4 — Workflow sin inputs/outputs claros

**❌ Mal:** "Paso 1: configurar el entorno. Paso 2: ejecutar la tarea."

**✅ Bien:** "Paso 1: invoca `SKL-AUTH-01` para obtener TOKEN. Paso 2: crea branch `feature/<task_id>` con `SKL-GIT-01`."

### Anti-pattern 5 — Copiar template sin borrar instrucciones del autor

Cada template empieza con un bloque `> Cómo usar...`. **Borrarlo antes de publicar.** El documento publicado debe verse limpio.

---

## 4. Después de publicar

### 4.1 Notificar

- Si es **Protocol** nuevo: avisar al PM + actualizar `INVENTARIO.md`
- Si es **Workflow / Skill / Script** nuevo: avisar al TL del Protocol padre

### 4.2 Versionar

| Nivel | Esquema |
|---|---|
| Protocol | SemVer (`1.0.0`, `1.1.0`, `2.0.0`) |
| Workflow | SemVer (`1.0.0`) |
| Skill | Incremental (`v1`, `v2`) |
| Script | Incremental (`v1`, `v2`) |

### 4.3 Mantener

- Si cambias un input contractual de Skill/Script → bump versión + nota en changelog
- Si cambias estructura del Protocol → bump major
- Si solo aclaras texto → bump patch (no requiere notificación)

---

## 5. Recursos relacionados

- **Conceptual:** `02.normativa/README.md` (Guía Normativa VTT — modelo 4 niveles)
- **Catálogo:** `02.normativa/INVENTARIO.md` (qué documentos existen)
- **Reglas Nivel 0:** `02.normativa/00.Rules/` (capabilities, roles, rules)
- **Ejemplos reales:**
  - Protocol: `02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_*.md`
  - Workflow / Skill / Script: pendientes (legacy en `_pending-migration/`)
- **Guía de autor con anti-patterns detallados:** `02.normativa/GUIA_AUTOR.md` (futuro — cuando se cree)

---

## 6. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial — 4 templates + README de uso |
