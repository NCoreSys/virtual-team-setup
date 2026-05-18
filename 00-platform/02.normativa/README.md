# Guía Normativa VTT — Modelo Operativo de 4 Niveles

| Campo | Valor |
|---|---|
| **Código** | `VTT.PROTOCOL-GOV-001` |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-13 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | Todos los agentes y roles que escriben o ejecutan documentación normativa en VTT |
| **Estado** | Aprobado para uso |

---

## Tabla de Contenido

1. [Propósito y alcance](#1-propósito-y-alcance)
2. [Modelo Operativo VTT de 4 niveles](#2-modelo-operativo-vtt-de-4-niveles)
3. [Cómo decidir el nivel correcto](#3-cómo-decidir-el-nivel-correcto)
4. [Convención de nombres](#4-convención-de-nombres)
5. [Estructura obligatoria del Protocol](#5-estructura-obligatoria-del-protocol)
6. [Estructura obligatoria del Workflow](#6-estructura-obligatoria-del-workflow)
7. [Estructura obligatoria del Skill](#7-estructura-obligatoria-del-skill)
8. [Estructura obligatoria del Script](#8-estructura-obligatoria-del-script)
9. [Reglas de invocación entre niveles](#9-reglas-de-invocación-entre-niveles)
10. [Versionado y cambios](#10-versionado-y-cambios)
11. [Cómo crear un documento nuevo](#11-cómo-crear-un-documento-nuevo)
12. [Migración de SOPs existentes](#12-migración-de-sops-existentes)
13. [Glosario](#13-glosario)
14. [Anexos](#14-anexos)

---

## 1. Propósito y alcance

### 1.1 Propósito

Establecer el modelo normativo para documentar todos los procesos operativos de VTT (Virtual Teams Tracking) de manera consistente, jerárquica y reutilizable entre proyectos.

### 1.2 Problema que resuelve

Antes de esta guía, la documentación normativa de VTT mezclaba niveles: un mismo documento describía a la vez **qué se hace, cómo se hace, qué comandos ejecutar y qué reglas aplican**. El resultado:

- Documentos largos difíciles de leer
- Skills específicas que no se reutilizan
- Procesos duplicados entre proyectos
- Agentes que no saben qué nivel de documento están leyendo

Esta guía separa responsabilidades en **4 niveles claros** y los agentes pueden identificar de inmediato qué tipo de documento están consultando por su nombre.

### 1.3 Alcance

Aplica a:

- Toda nueva documentación operativa de VTT (a partir de 2026-05-13)
- Migración progresiva de documentos legacy (SOP-*, FLUJO_*, PROCESO_*)
- Cualquier proyecto que use VTT como sistema de gestión (Memory Service, DesignMine, Prompt AI Studio, futuros)

No aplica a:

- Documentación interna del backend VTT (código, schemas) — eso vive en su propio repo
- Documentos de proyecto específicos (BRIEF, ASSIGNMENT, devlogs) — esos son **artefactos**, no normativa

---

## 2. Modelo Operativo VTT de 4 niveles + Nivel 0 transversal

```
NIVEL 0 — Rules       "restringe transversalmente"  ←── aplica a TODOS los niveles
              │
              ▼ se aplican a
NIVEL 4 — Protocol    "gobierna"
              ↓ invoca
NIVEL 3 — Workflow    "guía"
              ↓ usa
NIVEL 2 — Skill       "ejecuta capacidad reusable"
              ↓ corre
NIVEL 1 — Script      "automatiza acción atómica"
```

> **Nivel 0 — Rules** es transversal. No es un nivel operativo (no se invoca por sí solo);
> es una capa de **restricciones y condiciones** que cualquier Protocol/Workflow/Skill/Script
> debe respetar al ejecutarse. Define qué puede hacer cada actor en cada scope.
> Ver `00.Rules/README.md` para el modelo completo de 8 niveles de scope, 4 tipos de actor
> y markers operativos (mandatory, sensitive, human_only, sod_enforcement, blocks_review_gate, auto_detect).

### 2.0 Rules — restringe transversalmente (Nivel 0)

**Restricciones y condiciones que aplican a todos los niveles operativos.**

Responde a: *¿Qué puede hacer cada actor en cada scope, bajo qué condiciones?*

Características:
- **Transversal** — aplica a Protocols, Workflows, Skills, Scripts
- No es un procedimiento (no se "ejecuta")
- Cada regla tiene: scope jerárquico (Platform → Org → Workspace → Project → Phase → Task → Role → Agent), tipo de actor (Human/Agent/Service/External), capabilities requeridas, markers operativos
- Alineada con doc_sec_01..04 (Bloque 1 de autorización VTT)

Ejemplo:
> `RULE-CODE-001 — UN archivo .LOGIC.md por archivo de código`
> Scope: TASK (criterio: has_code_files=true) · Actor: HUMAN+AGENT · Markers: mandatory, blocks_review_gate, auto_detect

Catálogo: `00.Rules/rules_catalog.json` (43 reglas iniciales). Motor: `00.Rules/query_rules.py`.

### 2.1 Protocol — gobierna

**Define la regla operativa completa de un proceso de negocio.**

Responde a: *¿Cuál es el proceso correcto para X?*

Características:
- Proceso end-to-end con principio y fin claros
- Multi-fase (varias etapas secuenciales)
- Multi-rol (involucra distintos actores)
- Contiene **decisiones de negocio**
- Tiene §Propósito, §Responsabilidades, §Definiciones
- Es la **fuente de verdad** del proceso

Ejemplo:
> `VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea` — "Cómo se asigna y se cierra una tarea en VTT"

### 2.2 Workflow — guía

**Describe el flujo paso a paso de una actividad concreta.**

Responde a: *¿Qué pasos debo seguir para hacer X?*

Características:
- Sub-proceso atómico dentro de un Protocol
- Secuencia fija de pasos
- **Sin decisiones de negocio** — ejecución guiada
- Lleva las **reglas del paso** (qué es válido, qué no)
- Define inputs y outputs estrictos
- Invoca Skills para ejecutar

Ejemplo:
> `VTT.WORKFLOW-ASG-001.003_generar_y_subir_briefs` — "Para generar BRIEFs: por cada tarea, leer template, escribir archivo, subir attachment"

### 2.3 Skill — ejecuta capacidad reusable

**Bloque reusable de ejecución que el agente invoca.**

Responde a: *¿Cómo ejecuto esta capacidad?*

Características:
- Encapsula una acción discreta y reusable
- Inputs/outputs **contractuales** (siempre los mismos para esa skill)
- Inyectable en múltiples Workflows
- Orquesta uno o más Scripts
- Tamaño compacto (60-150 tokens)
- Incluye precondición, ejecución, validación, error común

Ejemplo:
> `VTT.SKILL-ATTACH-001_subir_attachment_a_tarea` — Capacidad "subir cualquier tipo de archivo a una tarea VTT" con `file_type` parametrizado

**Regla de reutilización:** Si dos Workflows hacen lo mismo con datos distintos, **usan la misma Skill** — no se crean skills específicas del contexto.

### 2.4 Script — automatiza acción atómica

**Comando concreto que se ejecuta técnicamente.**

Responde a: *¿Qué comando exacto corro?*

Características:
- Atómico, idempotente (cuando es posible)
- Sin lógica de negocio
- Parámetros bien definidos
- Logging y manejo de errores estándar
- Reusable entre Skills

Ejemplo:
> `VTT.SCRIPT-ATTACH-001_post_attachment_multipart.py` — `POST /api/tasks/:id/attachments` con file binary + fields

### 2.5 Diagrama de invocación

```
┌──────────────────────────────────────────┐
│ PROTOCOL                                 │
│  Define proceso completo                 │
│  §6 Referencias Cruzadas:                │
│    → Workflow A                          │
│    → Workflow B                          │
└──────────────────────────────────────────┘
                  ↓ invoca
┌──────────────────────────────────────────┐
│ WORKFLOW                                 │
│  Pasos secuenciales con reglas           │
│  "Paso 3: subir BRIEF                    │
│   → invocar SKILL-ATTACH-001 con         │
│     file_type='brief'"                   │
└──────────────────────────────────────────┘
                  ↓ usa
┌──────────────────────────────────────────┐
│ SKILL                                    │
│  Capacidad parametrizada                 │
│  Inputs: task_id, file_path,             │
│          file_type, uploaded_by          │
│  Ejecución: corre SCRIPT-ATTACH-001      │
└──────────────────────────────────────────┘
                  ↓ corre
┌──────────────────────────────────────────┐
│ SCRIPT                                   │
│  POST /api/tasks/:id/attachments         │
│  multipart/form-data                     │
└──────────────────────────────────────────┘
```

### 2.6 Filosofía: nombres interpretables por agentes

La nomenclatura `Protocol / Workflow / Skill / Script` se eligió porque cada palabra **es interpretable por sí sola** para un agente IA:

| Nombre | Lo que entiende el agente |
|---|---|
| Protocol | "Esto gobierna mi conducta en este proceso" |
| Workflow | "Estos son los pasos que debo seguir en orden" |
| Skill | "Esta es una capacidad que puedo invocar" |
| Script | "Esto se ejecuta técnicamente" |

Se evitaron acrónimos como `SOP/WI/ITV` porque requieren explicación previa y no se traducen igual de bien al inglés (donde el agente opera la mayoría del tiempo).

### 2.7 Equivalencias externas (solo para auditoría)

| VTT | Equivalente ISO/9001 | Cuándo usar |
|---|---|---|
| Rules | Policies / Controls | Auditoría de compliance (SOC2, ISO 27001) |
| Protocol | SOP (Standard Operating Procedure) | Auditoría externa, certificación |
| Workflow | WI (Work Instruction) | Equivalencia formal |
| Skill | — (no tiene equivalente directo) | Solo VTT |
| Script | — (sería herramienta o automation) | Solo VTT |

Esta equivalencia solo se menciona cuando hay auditoría externa. **La nomenclatura operativa siempre es la VTT.**

### 2.8 Documentos fuente del modelo de autorización (Nivel 0 Rules)

El Nivel 0 Rules está alineado con el Bloque 1 de autorización VTT documentado en:

- `00-platform/04.Process/01.authorizaton/doc_sec_01_modelo_seguridad_actores_scopes` — actores, recursos, jerarquía
- `00-platform/04.Process/01.authorizaton/doc_sec_02_politicas_permisos_rbac_abac` — 30 capabilities + 9 roles + reglas ABAC
- `00-platform/04.Process/01.authorizaton/doc_sec_03_arquitectura_implementacion_autorizacion` — middleware
- `00-platform/04.Process/01.authorizaton/doc_sec_04_matriz_autorizacion` — matriz RBAC

La implementación operativa de estos documentos vive en:
- `IMPROVE-004_rules_como_feature_vtt.md` (motor + API + Hook Manager)
- `IMPROVE-005_extension_recursos_vtt_especificos.md` (extensión a TIs, manifests, devlogs, LDs)

---

## 3. Cómo decidir el nivel correcto

### 3.1 Tabla decisoria

| Pregunta | Protocol | Workflow | Skill | Script |
|---|---|---|---|---|
| ¿Cubre un proceso de negocio end-to-end? | Sí | No | No | No |
| ¿Tiene fases? | Sí (varias) | No (una actividad) | No | No |
| ¿Decisiones de negocio? | Sí | No (ejecución guiada) | No | No |
| ¿Orquesta varios scripts? | Sí (a través de skills) | A través de skills | Sí | No |
| ¿Es un comando atómico? | No | No | No | Sí |
| ¿Idempotente? | No | Parcial | Cuando es posible | Sí (obligatorio) |
| ¿Reusable entre proyectos? | Sí (genérico VTT) | Sí | Sí | Sí |
| ¿Quién lo escribe? | PM/TL líder | TL | TL técnico | Dev/agente |
| ¿Quién lo lee primero? | Líderes + ejecutores | Ejecutor que planea | Agente que ejecuta | Ejecutor inmediato |
| Tamaño típico | 400-700 líneas | 150-300 líneas | 60-150 tokens (~30-80 líneas) | 5-50 líneas |

### 3.2 La pregunta clave: ¿Workflow o Skill?

Es la confusión más frecuente. Regla simple:

```
Si lo que escribes contiene PASOS DECISIVOS
   ("primero hacer X, después verificar Y, si Z entonces W")
   → es WORKFLOW

Si lo que escribes contiene una CAPACIDAD PARAMETRIZADA
   ("dame inputs A, B, C — yo ejecuto la acción y devuelvo resultado")
   → es SKILL
```

### 3.3 Regla de reutilización de Skills

> **Las Skills NUNCA son específicas del contexto.**
>
> Si te tienta crear `SKILL-BRIEF-UPLOAD-001` porque "es para subir BRIEFs", esa lógica pertenece al **Workflow** que la invoca, no a una Skill nueva.
>
> Crea `SKILL-ATTACH-001` (subir cualquier tipo de attachment) y deja que el Workflow le pase `file_type="brief"` o `file_type="devlog"` según corresponda.

Anti-patrón:

```
❌ SKILL-BRIEF-UPLOAD-001     "Subir BRIEF a tarea"
❌ SKILL-DEVLOG-UPLOAD-001    "Subir devlog a tarea"
❌ SKILL-MANIFEST-UPLOAD-001  "Subir manifest a tarea"
❌ SKILL-CODELOGIC-UPLOAD-001 "Subir code logic a tarea"
   → 4 skills haciendo casi lo mismo
```

Patrón correcto:

```
✅ SKILL-ATTACH-001 "Subir attachment a tarea"
   Inputs: task_id, file_path, file_type, uploaded_by
   → 1 skill reusable, el Workflow le pasa el file_type que necesita
```

### 3.4 Ejemplo lado a lado (Workflow vs Skill vs Script)

**Caso:** "Generar y subir BRIEFs de un sprint"

```
─────────────────────────────────────────────────────────────
WORKFLOW: VTT.WORKFLOW-ASG-001.003_generar_y_subir_briefs
─────────────────────────────────────────────────────────────
INPUTS:
  - lista_tareas: array de {task_id, titulo, agente}

REGLAS DEL WORKFLOW:
  - El BRIEF es inmutable (no se edita después de creado)
  - Una tarea = un BRIEF
  - Ubicación: knowledge/agent-tasks/briefs/[sprint]/BRIEF_[ID]_[nombre].md
  - Usar VTT.TEMPLATE-ASG-001_brief.md

PASOS:
  Por cada tarea en lista_tareas:
    1. Generar contenido del BRIEF usando el template
       → invoca SKILL-FILE-WRITE-001
    2. Validar formato del BRIEF generado
    3. Subir como attachment a la tarea VTT
       → invoca SKILL-ATTACH-001 con file_type="brief"
    4. Registrar en log local: "BRIEF [ID] subido (attachment_id: ...)"

OUTPUTS:
  - BRIEFs en disco
  - N attachments en VTT con fileType=brief
  - Log con UUIDs de cada attachment

─────────────────────────────────────────────────────────────
SKILL: VTT.SKILL-ATTACH-001_subir_attachment_a_tarea
─────────────────────────────────────────────────────────────
APLICA A: Todos los agentes
TOKENS: ~120

INPUTS (contractuales):
  - task_id        (ej. "MS-286")
  - file_path      (path local del archivo)
  - file_type      (enum: brief|assignment|devlog|code_logic|manifest|attachment)
  - uploaded_by    (UUID del usuario)
  - description    (opcional)

PRECONDICIÓN:
  - TOKEN JWT válido en $TOKEN
  - Archivo existe en file_path
  - file_type ∈ enum permitido

EJECUCIÓN:
  Llamar VTT.SCRIPT-ATTACH-001 con los inputs.

VALIDACIÓN:
  - HTTP 201
  - response.data.id es UUID válido
  - GET /api/tasks/{task_id}/attachments retorna el nuevo archivo

ERROR COMÚN:
  - 400 "uploadedById is required" → falta param
  - 400 "Invalid fileType" → file_type fuera del enum
  - 413 → archivo supera límite

─────────────────────────────────────────────────────────────
SCRIPT: VTT.SCRIPT-ATTACH-001_post_attachment_multipart.py
─────────────────────────────────────────────────────────────
POST {BASE_URL}/api/tasks/{task_id}/attachments
Content-Type: multipart/form-data; boundary=<boundary>
Authorization: Bearer <TOKEN>

Multipart fields:
  file:         <binario>
  fileType:     <file_type>
  uploadedById: <uploaded_by>
  description:  <description> (opcional)

Returns: { data: { id, fileType, fileSize, fileName, createdAt } }
Idempotencia: No (siempre crea un nuevo attachment, no dedup)
```

---

## 4. Convención de nombres

### 4.1 Pattern

```
VTT.<NIVEL>-<CAT>-<NNN>[.MMM]_titulo_snake_case.<ext>
   │  │       │     │    │     │                  │
   │  │       │     │    │     │                  └── md|py|sh|ts|mmd
   │  │       │     │    │     └────────────────────── snake_case minúsculas
   │  │       │     │    └──────────────────────────── sub-ID (solo Workflows)
   │  │       │     └───────────────────────────────── ID 3 dígitos
   │  │       └─────────────────────────────────────── categoría temática
   │  └─────────────────────────────────────────────── nivel: PROTOCOL|WORKFLOW|SKILL|SCRIPT|FLOWCHART|TEMPLATE
   └────────────────────────────────────────────────── prefijo plataforma (siempre "VTT")
```

### 4.2 Categorías estandarizadas

| Categoría | Tema |
|---|---|
| `GOV` | Gobierno operativo (transversal — esta guía vive aquí) |
| `ASG` | Asignación de tareas |
| `ISS` | Issues y on-hold |
| `TRK` | Trackable Items (ADRs, RFs, NFRs, Assumptions) |
| `LD` | Living Documents |
| `EVD` | Evidencias |
| `DEV` | Devlog entries |
| `MAN` | Manifests |
| `EST` | Estimaciones |
| `VEL` | Velocity |
| `RET` | Retrospectivas |
| `AUTH` | Autenticación / tokens |
| `TASK` | CRUD de tareas (script-level) |
| `ATTACH` | Attachments / archivos |
| `STATUS` | Cambios de estado de tareas |
| `COMMENT` | Comentarios en tareas |
| `PB` | Prompt Builder (futuro) |
| `QA` | Quality Assurance |
| `DB` | Operaciones de base de datos |
| `GIT` | Operaciones de Git/GitHub |
| `FILE` | Operaciones de filesystem |

Para agregar una categoría nueva → notificar PM y actualizar esta sección.

### 4.3 Numeración

- **3 dígitos** (`001` a `999`) — soporta escala sin renombrado
- **Sub-IDs** para Workflows que pertenecen a un Protocol específico: `.001`, `.002`, etc.
  Ejemplo: `WORKFLOW-ASG-001.003` = tercer workflow del protocol ASG-001

### 4.4 Extensiones por tipo

| Nivel | Extensión |
|---|---|
| Protocol | `.md` |
| Workflow | `.md` |
| Skill | `.md` |
| Script | `.py` (preferido) / `.sh` / `.ts` |
| Flowchart | `.mmd` (mermaid) o `.pdf` |
| Template | `.md` (con bloque code para JSON/YAML si aplica) |

### 4.5 Ejemplos

```
VTT.PROTOCOL-GOV-001_modelo_normativo_documental.md       (esta guía)
VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md
VTT.WORKFLOW-ASG-001.001_recibir_handoff.md
VTT.WORKFLOW-ASG-001.003_generar_y_subir_briefs.md
VTT.WORKFLOW-ASG-001.015_aplicar_modelo_dinamico.md
VTT.SKILL-AUTH-001_obtener_jwt.md
VTT.SKILL-ATTACH-001_subir_attachment_a_tarea.md
VTT.SKILL-TRK-001_crear_trackable_item.md
VTT.SCRIPT-ATTACH-001_post_attachment_multipart.py
VTT.SCRIPT-TRK-001_post_trackable_item.py
VTT.FLOWCHART-ASG-001_ciclo_asignacion.mmd
VTT.TEMPLATE-ASG-001_brief.md
```

---

## 5. Estructura obligatoria del Protocol

Un Protocol siempre tiene 7 secciones + Anexos + Footer.

### 5.1 Header

```markdown
# [Título del Protocol]

| Campo | Valor |
|---|---|
| **Código** | `VTT.PROTOCOL-<CAT>-<NNN>` |
| **Versión** | <X.Y.Z> |
| **Fecha** | YYYY-MM-DD |
| **Autor** | Nombre + rol |
| **Aplica a** | Roles separados por coma |
| **Estado** | Borrador / Aprobado / Deprecated |
```

### 5.2 Secciones §1 a §7

**§1 Propósito** — 1-2 párrafos. El **qué** y el **por qué**.

**§2 Campo de Aplicación** — Dónde y cuándo aplica el protocol.

**§3 Responsabilidades** — Por rol, qué le toca hacer:
```markdown
3.1 PM — recibir handoff, aprobar terminalmente
3.2 TL — planificar y revisar
3.3 Agente ejecutor — implementar y entregar
```

**§4 Definiciones** — Glosario de términos clave usados en el protocol.

**§5 Procedimiento** — El cuerpo del protocol, subdividido en fases:
```markdown
### 5.1 Fase 1 — [nombre]
5.1.1 Paso → ver WORKFLOW-XXX-NNN.001
5.1.2 Paso → ver WORKFLOW-XXX-NNN.002

### 5.2 Fase 2 — [nombre]
...
```

**§6 Referencias Cruzadas** — Tabla con todos los Workflows, Templates y otros documentos invocados:
```markdown
| Código | Documento |
|---|---|
| VTT.WORKFLOW-XXX-NNN.001 | Título |
| VTT.WORKFLOW-XXX-NNN.002 | Título |
| VTT.TEMPLATE-XXX-NNN | Título |
```

**§7 Resumen de Revisiones** — Versionado:
```markdown
| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | YYYY-MM-DD | Nombre | Versión inicial |
```

### 5.3 Anexos

Templates, ejemplos, formatos referenciados desde el cuerpo.

### 5.4 Footer

```markdown
---

| Editor | Dueño | Última Actualización |
|---|---|---|
| Nombre + rol | Nombre + rol | YYYY-MM-DD |
```

---

## 6. Estructura obligatoria del Workflow

Un Workflow es más compacto que un Protocol — no tiene §Responsabilidades ni §Definiciones globales.

```markdown
# [Título del Workflow]

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-<CAT>-<NNN>.<MMM>` |
| **Pertenece a** | `VTT.PROTOCOL-<CAT>-<NNN>` |
| **Versión** | <X.Y.Z> |
| **Fecha** | YYYY-MM-DD |
| **Aplica a** | Rol(es) |

## 1. Propósito
Una línea que dice qué hace este workflow.

## 2. Inputs
- input_1: descripción + formato esperado
- input_2: descripción + formato esperado

## 3. Precondiciones
- Condición que debe ser verdadera antes de ejecutar
- Estados de VTT requeridos
- Recursos necesarios

## 4. Reglas del Workflow
- Regla 1 (ej. "el BRIEF es inmutable")
- Regla 2 (ej. "usar template X")
- Convenciones aplicables (paths, naming)

## 5. Pasos

### Paso 1: [acción]
Descripción del paso.
Decisiones intermedias si las hay.
Si invoca skill: → invoca **VTT.SKILL-XXX-NNN** con inputs (param1=valor1, param2=valor2)

### Paso 2: [acción]
...

### Paso N: [acción]
...

## 6. Outputs
- output_1: descripción + formato
- output_2: descripción + formato

## 7. Validación
Cómo verificar que el workflow se completó correctamente:
- Check 1
- Check 2

## 8. Errores comunes
| Síntoma | Causa probable | Solución |
|---|---|---|

## 9. Skills invocadas
- VTT.SKILL-XXX-NNN
- VTT.SKILL-YYY-NNN
```

---

## 7. Estructura obligatoria del Skill

```markdown
# [Título del Skill]

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-<CAT>-<NNN>` |
| **Versión** | <X.Y> |
| **Aplica a** | Roles (o "Todos") |
| **Tokens estimados** | ~XXX |
| **Cuándo se usa** | Una línea sobre el momento de uso |

## Inputs (contractuales)
- input_1 (tipo): descripción
- input_2 (tipo): descripción

## Precondición
- Qué debe ser cierto antes de ejecutar

## Variables del entorno
- $TOKEN
- $VTT_BASE_URL
- $AGENT_UUID
- etc.

## Ejecución
Descripción de lo que hace la skill, en términos de scripts orquestados.

```bash
# Ejemplo de invocación
python VTT.SCRIPT-XXX-NNN.py --task_id=$TASK_ID --file_path=$PATH
```

## Validación
- Cómo saber si funcionó
- Qué response indica éxito

## Error común
- Error 1 → causa → solución
- Error 2 → causa → solución

## Scripts invocados
- VTT.SCRIPT-XXX-NNN
- VTT.SCRIPT-YYY-NNN
```

---

## 8. Estructura obligatoria del Script

```python
#!/usr/bin/env python3
"""
VTT.SCRIPT-<CAT>-<NNN> — [Título del script]

Propósito: [una línea]
Idempotente: [Sí / No / Parcial — explicar]

Inputs (CLI args o env vars):
  --task_id      ID de la tarea (ej. MS-286)
  --file_path    Path local al archivo
  --file_type    enum: brief|assignment|devlog|...
  $TOKEN         JWT VTT (env var)
  $VTT_BASE_URL  Base URL (env var, default http://77.42.88.106:3000)

Outputs (stdout JSON):
  { "success": true, "data": { "id": "...", "fileSize": N } }

Errores:
  Exit 1: argumentos inválidos
  Exit 2: precondición no cumplida
  Exit 3: respuesta HTTP de error
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", required=True)
    # ... resto de args
    args = parser.parse_args()

    # Validación de precondiciones
    token = os.environ.get("TOKEN")
    if not token:
        print(json.dumps({"success": False, "error": "TOKEN env var required"}))
        sys.exit(2)

    # Ejecución (con manejo de errores estándar)
    try:
        # ... lógica
        pass
    except urllib.error.HTTPError as e:
        print(json.dumps({
            "success": False,
            "http_status": e.code,
            "error": e.read().decode()[:300]
        }))
        sys.exit(3)

    # Output
    print(json.dumps({"success": True, "data": result}))


if __name__ == "__main__":
    main()
```

**Requisitos obligatorios de todo Script:**

1. **Header docstring** con propósito, inputs, outputs, errores, idempotencia
2. **Stdout en JSON** — para que las skills puedan parsear el resultado
3. **Exit codes claros** — 0 OK, 1 args, 2 precondición, 3 HTTP error
4. **Sin secrets hardcoded** — usar env vars
5. **Idempotencia documentada** — Sí / No / Parcial + por qué

---

## 9. Reglas de invocación entre niveles

### 9.1 Cómo se invoca cada nivel

| De → A | Mecanismo |
|---|---|
| **Protocol → Workflow** | En §5 Procedimiento: "→ ver `VTT.WORKFLOW-XXX-NNN.MMM`" + listado en §6 Referencias Cruzadas |
| **Workflow → Skill** | En el paso correspondiente: "→ invoca **VTT.SKILL-XXX-NNN** con (param=valor, ...)" |
| **Skill → Script** | En la sección Ejecución de la skill: comando inline `python VTT.SCRIPT-XXX-NNN.py --args` |
| **Script → APIs externas** | El script hace los HTTP calls finales |

### 9.2 Prohibido saltar niveles

❌ Un Protocol no invoca skills directamente — siempre pasa por Workflow.
❌ Un Workflow no invoca scripts directamente — siempre pasa por Skill.
❌ Una Skill no contiene scripts inline — siempre referencia un Script existente.

**Excepciones documentadas** (cuando la regla aplica, registrar en §8 del documento):
- Skills muy simples pueden contener el curl inline (≤5 líneas) sin crear Script aparte
- Para esos casos, agregar nota explícita en la skill

### 9.3 Cómo se propagan variables

Variables del entorno disponibles en todos los niveles:

```
$TOKEN           — JWT VTT (obtenido vía SKILL-AUTH-001)
$VTT_BASE_URL    — Base URL del backend VTT
$AGENT_UUID      — UUID del agente en sesión
$PROJECT_ID      — UUID del proyecto activo
$SERVICE_KEY     — Service key (solo para AUTH)
```

Estas son **comunes a todos los proyectos VTT**. Los IDs específicos del proyecto (UUIDs de tareas, deliveries, etc.) son **inputs explícitos** de cada Workflow/Skill, no env vars.

---

## 10. Versionado y cambios

### 10.1 Esquemas por nivel

| Nivel | Esquema | Razón |
|---|---|---|
| Protocol | SemVer (X.Y.Z) | Cambios de proceso son significativos |
| Workflow | SemVer (X.Y.Z) | Cambian inputs/outputs y secuencia |
| Skill | Incremental (v1, v2) | Cambios atómicos en contrato |
| Script | Incremental (v1, v2) | Cambios técnicos en endpoints |

### 10.2 Cuándo es major vs minor

**Protocol / Workflow (SemVer):**

| Cambio | Tipo | Ejemplo |
|---|---|---|
| Major (X) | Cambio incompatible | Agregar fase obligatoria nueva |
| Minor (Y) | Funcionalidad nueva compatible | Paso opcional adicional |
| Patch (Z) | Aclaración o fix de typos | Corregir ejemplo |

**Skill / Script (Incremental):**

| Cambio | Tipo | Acción |
|---|---|---|
| Cambia contrato (inputs/outputs) | Nueva versión | Crear `SKILL-XXX-NNN_v2` |
| Mejora interna sin romper | Mismo número, update | Actualizar contenido + bump fecha |

### 10.3 Quién aprueba cambios

| Nivel | Aprobador |
|---|---|
| Protocol | PM (cambios major) / TL (minor/patch) |
| Workflow | TL del proceso |
| Skill | TL técnico |
| Script | Cualquier dev/agente que sepa que funciona |

### 10.4 Registro de cambios

Todo Protocol y Workflow lleva tabla §7 Resumen de Revisiones con cada versión, fecha, editor y resumen.

Skills y Scripts llevan changelog en el header del documento/archivo.

---

## 11. Cómo crear un documento nuevo

### 11.1 Workflow del autor

```
1. Identifica el nivel correcto (sección §3 de esta guía)
2. Elige código siguiendo §4
3. Copia plantilla del Anexo correspondiente
4. Completa todas las secciones obligatorias
5. Valida con el checklist (§11.5)
6. Sube al repo en la carpeta correcta
7. Notifica al PM si es Protocol nuevo
```

### 11.2 Checklist Protocol

```
[ ] Código sigue pattern VTT.PROTOCOL-<CAT>-<NNN>
[ ] Header con todos los campos
[ ] §1 Propósito (1-2 párrafos)
[ ] §2 Campo de Aplicación
[ ] §3 Responsabilidades (por rol)
[ ] §4 Definiciones (al menos 3 términos clave)
[ ] §5 Procedimiento (subdividido en fases)
[ ] §6 Referencias Cruzadas (tabla completa)
[ ] §7 Resumen de Revisiones (versión inicial registrada)
[ ] Anexos (si aplica)
[ ] Footer con editor/dueño
[ ] Todos los Workflows referenciados existen o están en plan
[ ] Aprobación PM si es Protocol nuevo
```

### 11.3 Checklist Workflow

```
[ ] Código VTT.WORKFLOW-<CAT>-<NNN>.<MMM>
[ ] Header indica a qué Protocol pertenece
[ ] §1 Propósito (1 línea)
[ ] §2 Inputs claros con tipo y formato
[ ] §3 Precondiciones listadas
[ ] §4 Reglas del Workflow
[ ] §5 Pasos numerados con decisiones intermedias
[ ] §6 Outputs definidos
[ ] §7 Validación (cómo verificar éxito)
[ ] §8 Errores comunes
[ ] §9 Skills invocadas (todas listadas)
[ ] Cada paso que ejecuta algo invoca una Skill (no inline scripts)
```

### 11.4 Checklist Skill

```
[ ] Código VTT.SKILL-<CAT>-<NNN>
[ ] Inputs contractuales (siempre los mismos)
[ ] Precondición clara
[ ] Variables del entorno listadas
[ ] Ejecución referencia Scripts (no inline endpoints)
[ ] Validación específica con códigos HTTP esperados
[ ] Error común documentado
[ ] Scripts invocados listados
[ ] No es específica del contexto (es reusable)
[ ] Tokens estimados ≤ 200
```

### 11.5 Checklist Script

```
[ ] Código VTT.SCRIPT-<CAT>-<NNN>
[ ] Header docstring completo
[ ] Argparse o env vars (no hardcode)
[ ] Idempotencia documentada
[ ] Stdout en JSON
[ ] Exit codes 0/1/2/3
[ ] Manejo de HTTPError
[ ] Sin secrets hardcoded
[ ] Testeado con un caso real
```

---

## 12. Migración de SOPs existentes

### 12.1 Inventario actual

En el repo `virtual-teams-setup` (al 2026-05-13):

| Archivo legacy | Nivel actual | Migración propuesta |
|---|---|---|
| `SOP-EST-01_technical_estimates.md` | Mezcla SOP + WI | → 1 Protocol + 2 Workflows |
| `SOP-LD-01_living_documents.md` | SOP genérico | → Protocol (genérico) |
| `SOP-TRK-01_trackable_items_workflow.md` | Mezcla SOP + WI | → 1 Protocol + N Workflows |
| `SOP-TRK-02_dynamic_item_creation.md` | Workflow + Skills mezclados | → 1 Workflow + 2 Skills |
| `SOP-VEL-01_velocity_methodology.md` | Conceptual / metodología | → Protocol |
| `SOP-RET-01_retrospective_analysis.md` | SOP genérico | → Protocol + 1 Workflow |
| `PROCESO_ASIGNACION_TAREAS.md` | Híbrido | → 1 Protocol + N Workflows |

### 12.2 Plan progresivo

**No migrar todo de una vez.** La migración se hace cuando un documento se edita por otra razón:

```
1. Si un SOP existente NO necesita cambios → dejarlo como está
2. Si necesita actualización → migrarlo al nuevo modelo en el mismo PR
3. Si es nuevo → siempre nacer en el nuevo modelo
```

### 12.3 Tabla de equivalencias

```
SOP-XXX-NN (legacy)  →  VTT.PROTOCOL-XXX-NNN o VTT.WORKFLOW-XXX-NNN
                        (según contenga proceso de negocio o flujo guiado)

SKL-XXX-NN (legacy)  →  VTT.SKILL-XXX-NNN (renombrado directo)

Curls inline         →  Extraer como VTT.SCRIPT-XXX-NNN
```

---

## 13. Glosario

**Agente**: instancia de modelo IA (Claude/GPT/etc.) operando bajo un rol específico (TL, BE, PM, etc.).

**Artefacto**: documento generado durante la ejecución de un proceso (BRIEF, ASSIGNMENT, devlog, manifest). **No** es normativa.

**Capacidad reusable**: bloque de funcionalidad que se invoca con inputs distintos sin modificar la implementación interna. Equivale a una función parametrizada.

**Contractual (inputs/outputs)**: definidos formalmente — siempre los mismos para esa Skill/Script, sin importar quién la llame.

**Idempotencia**: propiedad de un script que produce el mismo resultado si se ejecuta varias veces con los mismos inputs.

**Marker**: convención textual estructurada que se embebe en datos sin schema dedicado (ej. `[TASK:MS-285] [SPRINT:S1]` en evidencias).

**Normativa**: conjunto de documentos que **gobiernan cómo se opera** (Protocol/Workflow/Skill/Script).

**Protocol**: nivel 4 del modelo — proceso de negocio end-to-end.

**Pool de transacciones (futuro)**: sistema centralizado que recibe operaciones VTT en JSON, las dedupa y las ejecuta atómicamente. Idea pendiente de implementación.

**Skill**: nivel 2 del modelo — capacidad reusable parametrizada.

**Script**: nivel 1 del modelo — comando atómico ejecutable.

**Workflow**: nivel 3 del modelo — secuencia guiada de pasos.

**VTT (Virtual Teams Tracking)**: plataforma de gestión de proyectos con agentes IA.

---

## 14. Anexos

### Anexo A — Ejemplo mínimo de Protocol

Ver `VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` (cuando exista).

Plantilla mínima:

```markdown
# Ciclo de [proceso]

| Código | VTT.PROTOCOL-XXX-001 |
| Versión | 1.0.0 |
| Fecha | YYYY-MM-DD |
| Autor | Nombre |
| Aplica a | Roles |
| Estado | Borrador |

## 1. Propósito
[1-2 párrafos]

## 2. Campo de Aplicación
[Dónde y cuándo aplica]

## 3. Responsabilidades
3.1 Rol A — qué hace
3.2 Rol B — qué hace

## 4. Definiciones
**Término 1**: definición
**Término 2**: definición

## 5. Procedimiento

### 5.1 Fase 1 — [nombre]
5.1.1 Paso → ver VTT.WORKFLOW-XXX-001.001
5.1.2 Paso → ver VTT.WORKFLOW-XXX-001.002

## 6. Referencias Cruzadas

| Código | Documento |
|---|---|

## 7. Resumen de Revisiones

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | YYYY-MM-DD | Nombre | Versión inicial |

---

| Editor | Dueño | Última Actualización |
|---|---|---|
```

### Anexo B — Ejemplo mínimo de Workflow

```markdown
# [Acción]

| Código | VTT.WORKFLOW-XXX-001.001 |
| Pertenece a | VTT.PROTOCOL-XXX-001 |
| Versión | 1.0.0 |
| Aplica a | Rol |

## 1. Propósito
[1 línea]

## 2. Inputs
- input_1 (tipo)

## 3. Precondiciones
- [...]

## 4. Reglas
- Regla 1

## 5. Pasos

### Paso 1: [acción]
[Descripción]
→ invoca **VTT.SKILL-XXX-001** con (param=valor)

## 6. Outputs
- output_1

## 7. Validación
- Check 1

## 8. Errores comunes
| Síntoma | Causa | Solución |
|---|---|---|

## 9. Skills invocadas
- VTT.SKILL-XXX-001
```

### Anexo C — Ejemplo mínimo de Skill

```markdown
# [Capacidad]

| Código | VTT.SKILL-XXX-001 |
| Versión | 1.0 |
| Aplica a | Todos |
| Tokens estimados | ~100 |
| Cuándo | [una línea] |

## Inputs (contractuales)
- input_1 (tipo): descripción

## Precondición
- TOKEN válido

## Variables del entorno
- $TOKEN
- $VTT_BASE_URL

## Ejecución
Llamar VTT.SCRIPT-XXX-001 con los inputs.

```bash
python VTT.SCRIPT-XXX-001.py --param=$VALOR
```

## Validación
- HTTP 200/201
- response.data.id existe

## Error común
- Error 1 → causa → solución

## Scripts invocados
- VTT.SCRIPT-XXX-001
```

### Anexo D — Ejemplo mínimo de Script

```python
#!/usr/bin/env python3
"""
VTT.SCRIPT-XXX-001 — [Título]

Propósito: [una línea]
Idempotente: Sí/No/Parcial — [razón]

Inputs:
  --param1   [descripción]
  $TOKEN     JWT VTT

Outputs (stdout JSON):
  { "success": true, "data": {...} }

Errores:
  Exit 1: args inválidos
  Exit 2: precondición no cumplida
  Exit 3: HTTP error
"""

import argparse, json, os, sys
import urllib.request, urllib.error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--param1", required=True)
    args = parser.parse_args()

    token = os.environ.get("TOKEN")
    if not token:
        print(json.dumps({"success": False, "error": "TOKEN required"}))
        sys.exit(2)

    try:
        # lógica HTTP
        result = {"id": "ejemplo"}
        print(json.dumps({"success": True, "data": result}))
    except urllib.error.HTTPError as e:
        print(json.dumps({
            "success": False,
            "http_status": e.code,
            "error": e.read().decode()[:300]
        }))
        sys.exit(3)


if __name__ == "__main__":
    main()
```

### Anexo E — Diagrama de niveles (mermaid)

```mermaid
flowchart TD
    P[PROTOCOL<br/>Gobierna proceso completo<br/>Multi-fase, multi-rol]
    W[WORKFLOW<br/>Guía pasos secuenciales<br/>Sin decisiones de negocio]
    S[SKILL<br/>Capacidad reusable parametrizada<br/>Inputs/Outputs contractuales]
    SC[SCRIPT<br/>Comando atómico ejecutable<br/>Idempotente cuando es posible]

    P -->|"§6 Referencias Cruzadas"| W
    W -->|"en cada Paso → invoca"| S
    S -->|"sección Ejecución → corre"| SC
    SC -->|"HTTP/Bash/Python"| API[(VTT Backend<br/>GitHub<br/>Filesystem)]

    style P fill:#1f4e79,color:#fff
    style W fill:#2e75b6,color:#fff
    style S fill:#9dc3e6,color:#000
    style SC fill:#bdd7ee,color:#000
```

### Anexo F — Checklist de calidad por nivel

**Antes de publicar cualquier documento normativo, verificar:**

```
[ ] Código sigue pattern VTT.<NIVEL>-<CAT>-<NNN>
[ ] Nombre es interpretable (no acrónimos opacos)
[ ] Nivel correcto (revisar §3 de esta guía)
[ ] Estructura obligatoria completa (revisar §5/6/7/8)
[ ] Sin información específica de proyecto hardcoded
[ ] Variables del entorno con $PREFIX
[ ] Referencias cruzadas válidas (los archivos existen o están en plan)
[ ] Versionado correcto (SemVer o Incremental según nivel)
[ ] Checklist específico del nivel completo (§11.2/3/4/5)
```

### Anexo G — Tabla de equivalencias externa

Para auditoría ISO 9001 o referencia con sistemas externos (KN/CUP, ITIL, etc.):

| VTT | ISO 9001 / Industria | Notas |
|---|---|---|
| Protocol | SOP (Standard Operating Procedure) / PNO | Equivalencia directa |
| Workflow | WI (Work Instruction) | Equivalencia directa |
| Skill | — | Concepto nativo VTT, no tiene equivalente formal |
| Script | Automation / Tool | Nivel técnico |
| Flowchart | Flowchart / Diagrama de Flujo | Igual |
| Template | Formato / Formulario | Igual |

---

| Editor | Dueño | Última Actualización |
|---|---|---|
| PM Martin Rivas | PM Martin Rivas | 2026-05-13 |

**Versión:** 1.0.0 — Documento inicial — Modelo Operativo VTT de 4 niveles (Protocol / Workflow / Skill / Script)
**Estado:** Aprobado para uso

*Versión más reciente en el repo `virtual-teams-setup`. No controlada si se imprime.*
