---
skill_code: SKL-GIT-VTT-COMMIT-01
title: Commit estructurado en virtual-teams-setup
version: 1.0.0
status: active
category: git-ops
applies_to: [tl, be, pm, pjm, do, db, fe, qa, ux, dl, sa, ar, sec, setup]
applies_repo: virtual-teams-setup
related_skills: [SKL-GIT-VTT-BRANCH-01]
related_scripts: [SCR-GIT-VTT-VALIDATE-01]
last_updated: 2026-05-17
---

# SKL-GIT-VTT-COMMIT-01 — Commit estructurado en virtual-teams-setup

| Campo | Valor |
|---|---|
| **Código** | SKL-GIT-VTT-COMMIT-01 |
| **Versión** | 1.0.0 |
| **Categoría** | GIT-OPS |
| **Aplica a** | Todos los agentes que editen en `virtual-teams-setup/` |
| **Tokens estimados** | ~140 |
| **Cuándo** | Inmediatamente DESPUÉS de modificar uno o más archivos en una rama `agent/...` |

---

## 1. Propósito

Crear un commit en `virtual-teams-setup` con metadata estructurada en el mensaje, de modo que el `git log` sea **filtrable, auditable y trazable** sin necesidad de un sistema de tickets externo durante la Fase de Desarrollo.

> Esta skill es **obligatoria** para todo commit en el repo. Acompaña a `SKL-GIT-VTT-BRANCH-01` (la rama se crea con esa skill; los commits dentro de la rama se hacen con esta).

---

## 2. Formato obligatorio del commit message

```
[agente:<rol>] [proyecto:<origen>] [scope:<ruta>] [type:<tipo>]
<titulo-corto-max-60-chars>

<descripcion-3-a-5-lineas>

Motivo: <razon-del-cambio>
Origen: <ticket-sesion-PR-leccion>
Consumidores: <lista-proyectos-afectados-o-none>

Co-Authored-By: Claude <model> <noreply@anthropic.com>
```

### 2.1 Línea 1 — Markers (todos obligatorios)

| Marker | Valores válidos | Significado |
|---|---|---|
| `[agente:<rol>]` | Lista de 14 roles (ver SKL-GIT-VTT-BRANCH-01 §3) | Qué rol hizo el commit |
| `[proyecto:<origen>]` | Slug del proyecto que originó el cambio | De qué proyecto viene la necesidad |
| `[scope:<ruta>]` | Carpeta(s) tocada(s). Si >1 carpeta raíz: `multiple` | Qué área del repo se tocó |
| `[type:<tipo>]` | `editorial \| functional \| structural \| breaking` | Severidad del cambio (ver §3) |

### 2.2 Líneas 2-3 — Título y descripción

- **Título**: máximo 60 chars, frase imperativa corta (`PROTOCOL-ASG-001: agregar paso 5.3.7`)
- **Descripción**: 3 a 5 líneas, en presente, qué cambió y por qué

### 2.3 Líneas 4-6 — Trazabilidad (todos obligatorios)

| Campo | Contenido |
|---|---|
| `Motivo:` | Razón del cambio (lección aprendida, bug, mejora propuesta) |
| `Origen:` | ID de ticket VTT, fecha de sesión, PR ref, o referencia a la lección |
| `Consumidores:` | Lista de proyectos consumidores afectados, o `none` |

### 2.4 Línea Co-Authored-By

Obligatoria si el commit fue generado con asistencia de IA. Usar el modelo correcto (ver `rules_agents.instructions.md` §8).

---

## 3. Tipos de cambio (`[type:...]`)

| Tipo | Cuándo usarlo | Ejemplo |
|---|---|---|
| `editorial` | Typo, ejemplo, aclaración. NO cambia proceso ni schema | "Corregir typo en línea 42 de PROTOCOL-ASG" |
| `functional` | Paso nuevo, regla nueva, mejora de procedimiento | "PROTOCOL-ASG-001: agregar paso 5.3.7 Hardcode Check" |
| `structural` | Cambio de schema, nueva carpeta, nueva entidad, renombre | "Mover SKL-MANIFEST a 03.Skills/manifest/" |
| `breaking` | Rompe consumidores (elimina campo, renombra path canónico) | "Eliminar campo `skl_report_01_full` del manifest" |

> Regla simple: si dudas entre dos tipos, **elige el de mayor severidad**. Mejor sobre-clasificar que sub-clasificar.

---

## 4. Ejemplo completo (commit real)

```
[agente:tl] [proyecto:memory-service] [scope:02.normativa/01.Protocols] [type:functional]
PROTOCOL-ASG-001: agregar paso 5.3.7 Hardcode Check

Agente debe ejecutar grep de patrones de secretos antes de
mover tarea a in_review. Findings critical/high bloquean el
Review Gate. Falsos positivos requieren justificacion explicita
en el devlog.

Motivo: leccion de MS-285 — varios agentes saltaron este check
Origen: sesion 2026-05-17 con PM (revision de incidente MS-285)
Consumidores: memory-service-project

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## 5. Precondiciones

Antes de ejecutar la skill, verificar:

1. Estás en una rama `agent/...` (NO en `main`). Validar con `git rev-parse --abbrev-ref HEAD`.
2. Tienes al menos un archivo staged (`git diff --cached --name-only` muestra ≥1 archivo).
3. Sabes el `<rol>`, `<proyecto-origen>` (los mismos que usaste para crear la rama).
4. Tienes claro el `<tipo>` según §3.
5. Tienes el `Origen:` definido (ID de ticket, fecha de sesión, o referencia clara).

---

## 6. Ejecución

### 6.1 Stagear los archivos a commitear

```bash
git add <ruta1> <ruta2> ...
# o todo lo modificado:
git add -A

# Verificar
git diff --cached --name-only
```

### 6.2 Detectar `<scope>` automáticamente

```bash
# Toma las carpetas raíz de los archivos staged
SCOPE=$(git diff --cached --name-only \
  | awk -F/ '{print $1"/"$2}' \
  | sort -u \
  | head -3 \
  | paste -sd,)

# Si toca más de 1 carpeta raíz, usar "multiple"
COUNT=$(echo "$SCOPE" | tr ',' '\n' | wc -l)
[ "$COUNT" -gt 1 ] && SCOPE="multiple"

echo "Scope detectado: $SCOPE"
```

### 6.3 Construir y ejecutar el commit

```bash
AGENT_ROLE="tl"
ORIGIN_PROJECT="memory-service"
TYPE="functional"
TITLE="PROTOCOL-ASG-001: agregar paso 5.3.7 Hardcode Check"
DESCRIPTION="Agente debe ejecutar grep de patrones de secretos antes de
mover tarea a in_review. Findings critical/high bloquean el
Review Gate. Falsos positivos requieren justificacion explicita
en el devlog."
MOTIVO="leccion de MS-285 — varios agentes saltaron este check"
ORIGEN="sesion 2026-05-17 con PM (revision de incidente MS-285)"
CONSUMIDORES="memory-service-project"
CO_AUTHOR="Claude Opus 4.7 (1M context) <noreply@anthropic.com>"

git commit -m "[agente:${AGENT_ROLE}] [proyecto:${ORIGIN_PROJECT}] [scope:${SCOPE}] [type:${TYPE}]
${TITLE}

${DESCRIPTION}

Motivo: ${MOTIVO}
Origen: ${ORIGEN}
Consumidores: ${CONSUMIDORES}

Co-Authored-By: ${CO_AUTHOR}"
```

### 6.4 (Recomendado) Usar HEREDOC para preservar formato

Si el commit tiene caracteres especiales o múltiples líneas, usar HEREDOC con `cat`:

```bash
git commit -m "$(cat <<'EOF'
[agente:tl] [proyecto:memory-service] [scope:02.normativa/01.Protocols] [type:functional]
PROTOCOL-ASG-001: agregar paso 5.3.7 Hardcode Check

Agente debe ejecutar grep de patrones de secretos antes de
mover tarea a in_review. Findings critical/high bloquean el
Review Gate.

Motivo: leccion de MS-285
Origen: sesion 2026-05-17 con PM
Consumidores: memory-service-project

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## 7. Validación post-ejecución

```bash
# 1. Commit existe
git log -1 --format=%H || { echo "FAIL: no se creo commit"; exit 1; }

# 2. Los 4 markers están presentes
MSG=$(git log -1 --format=%B)
echo "$MSG" | head -1 | grep -qE '\[agente:[a-z]+\] \[proyecto:[a-z0-9-]+\] \[scope:[^]]+\] \[type:(editorial|functional|structural|breaking)\]' || \
  { echo "FAIL: linea 1 no tiene los 4 markers obligatorios"; exit 1; }

# 3. Los 3 campos de trazabilidad están presentes
echo "$MSG" | grep -q '^Motivo: '       || { echo "FAIL: falta Motivo:"; exit 1; }
echo "$MSG" | grep -q '^Origen: '       || { echo "FAIL: falta Origen:"; exit 1; }
echo "$MSG" | grep -q '^Consumidores: ' || { echo "FAIL: falta Consumidores:"; exit 1; }

# 4. NO commiteamos a main
BRANCH=$(git rev-parse --abbrev-ref HEAD)
[ "$BRANCH" != "main" ] || { echo "FAIL: commit a main directo, prohibido"; exit 1; }

echo "OK — commit estructurado correctamente en $BRANCH"
```

---

## 8. Errores comunes y cómo resolverlos

| Síntoma | Causa probable | Acción |
|---|---|---|
| `nothing to commit` | Olvidaste `git add` | `git add <archivos>` y reintentar |
| Falta marker `[scope:...]` | El comando se cortó por mala expansión | Usar HEREDOC (§6.4) |
| Falta `Consumidores:` | Olvidaste el campo | Reescribir mensaje (`git commit --amend`) |
| Commit hecho a `main` | NO se ejecutó `SKL-GIT-VTT-BRANCH-01` antes | `git reset --soft HEAD~1`, crear branch, recommit |
| `<type>` inventado (ej. `chore`) | Tipos válidos son solo 4 (§3) | Usar `editorial` / `functional` / `structural` / `breaking` |
| Título >60 chars | Frase muy larga | Acortar título, mover detalle a descripción |

---

## 9. Reglas duras

| # | Regla |
|---|---|
| R1 | Los 4 markers en línea 1 son **obligatorios**. Faltar uno = commit inválido |
| R2 | Los 3 campos (`Motivo:`, `Origen:`, `Consumidores:`) son **obligatorios** |
| R3 | NUNCA commit a `main` directo. Si pasó por error → `git reset --soft HEAD~1` y crear branch |
| R4 | Si el cambio afecta a proyectos consumidores → listarlos en `Consumidores:` (no usar `none` si afecta) |
| R5 | Un commit = un cambio coherente. Si tocaste 2 cosas no relacionadas → 2 commits separados |
| R6 | Co-Authored-By cuando hay asistencia de IA (modelo correcto según `rules_agents` §8) |

---

## 10. Consultas útiles del git log (gracias a este formato)

```bash
# Todos los commits de un rol
git log --grep '^\[agente:tl\]' --oneline

# Todos los commits originados en memory-service
git log --grep '\[proyecto:memory-service\]' --oneline

# Solo cambios breaking
git log --grep '\[type:breaking\]' --oneline

# Cambios que tocaron 02.normativa
git log --grep '\[scope:02.normativa' --oneline

# Combinado: cambios breaking del TL
git log --grep '\[agente:tl\].*\[type:breaking\]' --oneline
```

---

## 11. Integración con otras skills

| Skill / Script | Cuándo |
|---|---|
| `SKL-GIT-VTT-BRANCH-01` | ANTES de editar, para crear la rama con formato correcto |
| `SCR-GIT-VTT-VALIDATE-01` | Pre-commit hook que valida formato automáticamente |

---

## 12. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-05-17 | Versión inicial. Define formato `[agente] [proyecto] [scope] [type] + título + descripción + Motivo/Origen/Consumidores`. 4 tipos de cambio (editorial/functional/structural/breaking). Validaciones automáticas pre/post commit. |
