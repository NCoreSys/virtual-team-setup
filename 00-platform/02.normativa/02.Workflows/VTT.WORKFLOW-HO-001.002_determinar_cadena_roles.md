# VTT.WORKFLOW-HO-001.002 — Determinar Cadena de Roles del Bloque

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.002` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.0.2 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PM |
| **Tipo** | [PROCESO] sub-procedimiento de inicio |

---

## 1. Propósito

Determinar la cadena específica de roles que entra al ciclo de generación del HO para una feature concreta. La cadena determina quién produce cada 3B.X, qué dictámenes son obligatorios en FASE 3 y qué handoffs por rol genera el PJM en FASE 6.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `metodologia_path` | path | producido por PM análisis | sí | Documento METODOLOGIA borrador |
| `spec_path` | path | producido por PM análisis | sí | Documento SPEC borrador |
| `superficies_afectadas` | array<string> | análisis del PM | sí | Lista de superficies: backend, ui, db, infra, security, etc. |

---

## 3. Precondiciones

- METODOLOGIA + SPEC borradores existen en disco.
- PM tiene visibilidad de la complejidad del bloque.
- OPERATIVO del proyecto con UUIDs de roles disponibles.

---

## 4. Reglas del Workflow

- **R1:** TL es OBLIGATORIO en toda cadena (no negociable).
- **R2:** La cadena determina dictámenes obligatorios en FASE 3: cada rol técnico productor emite dictamen.
- **R3:** AR siempre emite REVIEW_AR_CROSS_MODULE (independiente de su participación en producción).
- **R4:** SA es OPCIONAL — PM decide si incluirlo para REVISION_SA_FUNCIONAL.
- **R5:** Roles ausentes en la cadena no producen dictámenes ni handoffs en FASE 6.

---

## 5. Pasos

### Paso 1 — PM analiza superficies de la feature

PM identifica qué superficies técnicas toca la feature:
- ¿Hay endpoints nuevos? → BE entra
- ¿Hay schema/migraciones? → DB entra
- ¿Hay UI nueva? → DL + UX + FE entran
- ¿Hay despliegue nuevo / infra nueva? → DO entra
- ¿Hay superficie crítica de seguridad? → SEC entra
- ¿Hay testing formal requerido? → QA entra

### Paso 2 — PM aplica composición mínima

Cadena mínima OBLIGATORIA siempre incluye:
- PM (ejecutor del Protocol)
- PM Revisor (auditor independiente)
- TL (productor de 3B.2, 3B.5, 3B.6, 3B.9)
- AR (productor de 3B.1 + REVIEW cross-module)

### Paso 3 — PM agrega roles condicionales

Según superficies de Paso 1:
- DB si hay schema
- BE si hay endpoints
- FE + DL + UX si hay UI
- SEC si hay seguridad crítica
- DO si hay infra/despliegue
- SA si PM decide incluir validación funcional cross-rol

### Paso 4 — PM registra cadena en DECISION_BLOQUE

PM crea documento `DECISION_BLOQUE_<NOMBRE>_v1.0.md` con:
- Nombre del bloque/feature
- Cadena de roles (lista con UUIDs)
- Justificación de inclusión/exclusión por rol
- Camino elegido (A/B/C) — referencia a WORKFLOW-HO-001.003

### Paso 5 — PM comunica cadena a los roles involucrados

PM notifica a cada rol de la cadena que entrarán al ciclo.

→ invoca **`VTT.SKILL-COMMENT-001`** por cada rol notificado.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Documento DECISION_BLOQUE | archivo .md | `_project-management/Fases/<BLOQUE>/` |
| Notificaciones a roles | comentarios formales | VTT |

---

## 7. Validación

- Cadena incluye al menos TL + AR + PM + PM Revisor.
- Cada rol tiene UUID válido del OPERATIVO.
- Documento DECISION_BLOQUE existe y está versionado.
- Todos los roles notificados acusaron recibo.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Se omite SEC en feature con auth nueva | No se mapeó superficie | Re-revisar Paso 1 con check de seguridad obligatorio |
| Cadena incluye FE pero no DL | Inconsistencia | Si hay FE, hay UI → DL obligatorio |
| TL no está en cadena | Violación R1 | Bloquear arranque del Protocol |

---

## 9. Skills invocadas

- `VTT.SKILL-COMMENT-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.002_determinar_cadena_roles.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
