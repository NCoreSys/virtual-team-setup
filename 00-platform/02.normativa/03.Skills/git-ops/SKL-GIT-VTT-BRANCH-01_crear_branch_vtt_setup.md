---
skill_code: SKL-GIT-VTT-BRANCH-01
title: Crear branch en virtual-teams-setup con formato VTT
version: 1.0.0
status: active
category: git-ops
applies_to: [tl, be, pm, pjm, do, db, fe, qa, ux, dl, sa, ar, sec, setup]
applies_repo: virtual-teams-setup
related_skills: [SKL-GIT-VTT-COMMIT-01]
related_scripts: [SCR-GIT-VTT-VALIDATE-01]
last_updated: 2026-05-17
---

# SKL-GIT-VTT-BRANCH-01 — Crear branch en virtual-teams-setup

| Campo | Valor |
|---|---|
| **Código** | SKL-GIT-VTT-BRANCH-01 |
| **Versión** | 1.0.0 |
| **Categoría** | GIT-OPS |
| **Aplica a** | Todos los agentes que editen en `virtual-teams-setup/` |
| **Tokens estimados** | ~120 |
| **Cuándo** | ANTES de modificar cualquier archivo del repo `virtual-teams-setup` |

---

## 1. Propósito

Crear una rama de Git con el formato obligatorio del repo `virtual-teams-setup` para que **todo cambio sea atribuible** a un rol y a un proyecto de origen, sin necesidad de daily review ni asignación previa de carpetas.

> Esta skill es **obligatoria** durante la Fase de Desarrollo del gobierno editorial (ver `PROCESO_EDICION_VTT_SETUP_FASE_DESARROLLO.md`). En Fase de Producción será reemplazada por tickets en el proyecto VTT-SETUP de VTT API.

---

## 2. Formato obligatorio de branch

```
agent/<rol>/<proyecto-origen>/<descripcion-kebab-case>
```

### 2.1 Campos

| Campo | Reglas | Ejemplos válidos |
|---|---|---|
| `<rol>` | Código corto del rol del agente. Debe estar en lista autorizada (ver §3). | `tl`, `be`, `pjm` |
| `<proyecto-origen>` | Proyecto donde el agente opera (no donde edita). Slug del repo. | `vtt-setup`, `memory-service`, `designmine` |
| `<descripcion-kebab-case>` | Qué se cambia. Solo `[a-z0-9-]`. Entre 3 y 50 chars. | `protocol-asg-paso-5-3-7-hardcode-check` |

### 2.2 Ejemplos completos

```
agent/tl/memory-service/protocol-asg-update
agent/be/designmine/add-rule-be-coverage
agent/pjm/vtt-setup/profile-pjm-v2
agent/pm/vtt-setup/governance-fase-desarrollo
```

### 2.3 Anti-patrones (RECHAZAR)

| Branch | Razón de rechazo |
|---|---|
| `fix-typo` | Falta prefijo `agent/...` |
| `agent/tl/protocol-update` | Falta `<proyecto-origen>` |
| `agent/TL/memory-service/Update` | Mayúsculas en `<rol>` o `<descripcion>` |
| `agent/architect/.../...` | `architect` no está en lista (usar `ar`) |
| `agent/tl/memory_service/...` | Underscore en `<proyecto-origen>` (usar guion: `memory-service`) |

---

## 3. Lista autorizada de roles

| Código | Rol completo |
|---|---|
| `tl` | Tech Lead |
| `pm` | Product Manager |
| `pjm` | Project Manager |
| `be` | Backend Engineer |
| `db` | Database Engineer |
| `fe` | Frontend Developer |
| `do` | DevOps Engineer |
| `qa` | QA Engineer |
| `ux` | UX Designer |
| `dl` | Design Lead |
| `sa` | Solution Analyst |
| `ar` | Architect |
| `sec` | Security Engineer |
| `setup` | Setup Agent |

> Si tu rol no está en esta lista, **NO inventes uno** — escalar al PM para extender el catálogo.

---

## 4. Precondiciones

Antes de ejecutar la skill, verificar:

1. Estás dentro del repo `virtual-teams-setup` (`pwd` lo confirma)
2. Tienes claro el `<rol>` autorizado de §3
3. Tienes claro el `<proyecto-origen>` (de qué proyecto viene la necesidad del cambio)
4. Tienes un `<descripcion-kebab-case>` corto que describe el cambio
5. NO estás trabajando ya en otra rama sin terminar (esto evita mezclar cambios no relacionados)

---

## 5. Ejecución (paso a paso)

### 5.1 Validar inputs

```bash
# Inputs requeridos
AGENT_ROLE="tl"                                    # ver §3
ORIGIN_PROJECT="memory-service"                    # slug del proyecto que origina el cambio
BRANCH_DESC="protocol-asg-paso-5-3-7-hardcode"     # kebab-case, 3-50 chars

# Validar rol contra lista autorizada
case "$AGENT_ROLE" in
  tl|pm|pjm|be|db|fe|do|qa|ux|dl|sa|ar|sec|setup) ;;
  *) echo "ABORT: rol '$AGENT_ROLE' no autorizado. Ver SKL-GIT-VTT-BRANCH-01 §3"; exit 1 ;;
esac

# Validar formato del proyecto (slug minúsculas, guiones)
echo "$ORIGIN_PROJECT" | grep -qE '^[a-z0-9-]{3,30}$' || \
  { echo "ABORT: proyecto-origen debe ser kebab-case 3-30 chars"; exit 1; }

# Validar descripción
echo "$BRANCH_DESC" | grep -qE '^[a-z0-9-]{3,50}$' || \
  { echo "ABORT: descripcion debe ser kebab-case 3-50 chars"; exit 1; }
```

### 5.2 Sincronizar main

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
```

Si `git pull` falla por divergencia local en main → **PARAR** y escalar al PM (alguien commiteó directo a main).

### 5.3 Crear y cambiar a la nueva rama

```bash
BRANCH="agent/${AGENT_ROLE}/${ORIGIN_PROJECT}/${BRANCH_DESC}"
git checkout -b "$BRANCH"
echo "Branch creada: $BRANCH"
```

---

## 6. Validación post-ejecución

```bash
# 1. HEAD apunta al nuevo branch
CURRENT=$(git rev-parse --abbrev-ref HEAD)
[ "$CURRENT" = "$BRANCH" ] || { echo "FAIL: HEAD no apunta a $BRANCH"; exit 1; }

# 2. Branch tiene formato correcto
echo "$CURRENT" | grep -qE '^agent/(tl|pm|pjm|be|db|fe|do|qa|ux|dl|sa|ar|sec|setup)/[a-z0-9-]{3,30}/[a-z0-9-]{3,50}$' || \
  { echo "FAIL: formato de branch invalido"; exit 1; }

echo "OK — listo para editar en $CURRENT"
```

---

## 7. Errores comunes y cómo resolverlos

| Síntoma | Causa probable | Acción |
|---|---|---|
| `rol 'X' no autorizado` | Usaste `architect` en vez de `ar` | Ver §3, usar código corto |
| `git pull` con conflict en main | Otro agente commiteó directo a main | **PARAR** — escalar al PM |
| `branch already exists` | Trabajo previo no terminado en esa rama | Hacer rebase o renombrar |
| `descripcion debe ser kebab-case` | Pusiste mayúsculas o underscore | Solo `[a-z0-9-]` |
| `not a git repository` | No estás dentro de `virtual-teams-setup` | `cd` al repo correcto |
| `proyecto-origen` no claro | El cambio no viene de un proyecto concreto | Usar `vtt-setup` (cambio nacido en el propio repo) |

---

## 8. Reglas duras

| # | Regla |
|---|---|
| R1 | **NUNCA** commitear directo a `main`. Toda edición vive en una rama `agent/...` |
| R2 | **Una rama = un cambio relacionado**. No acumular cambios sin relación en la misma rama |
| R3 | La rama se borra después del merge (`git branch -d agent/...`) |
| R4 | Si el rol que necesitas no está en §3 → escalar al PM, NO inventar |
| R5 | Si `<proyecto-origen>` no es obvio → usar `vtt-setup` para cambios nacidos en el propio repo |

---

## 9. Integración con otras skills

| Skill | Cuándo |
|---|---|
| `SKL-GIT-VTT-COMMIT-01` | Después de editar, para hacer commit con metadata estructurada |
| `SCR-GIT-VTT-VALIDATE-01` | Pre-commit hook que valida formato de branch antes de aceptar el commit |

---

## 10. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-05-17 | Versión inicial. Define formato `agent/<rol>/<proyecto>/<desc>`, lista de 14 roles autorizados, validaciones pre/post ejecución. |
