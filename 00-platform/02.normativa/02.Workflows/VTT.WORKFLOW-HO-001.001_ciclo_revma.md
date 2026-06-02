# VTT.WORKFLOW-HO-001.001 — Ciclo REVMA (Revisión Multiagente)

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.001` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.1, §5.2.3, §5.4.11, §5.6.8 (uso fractal) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PM (bus de mensajes), PM Revisor (OpenAI), Agente generador (Claude) |
| **Tipo** | [PROCESO] sub-procedimiento transversal — invocado fractalmente |

---

## 1. Propósito

Auditar un documento producido por un agente generador (Claude) mediante revisión independiente de un PM Revisor en modelo distinto (OpenAI), con el PM humano como bus de mensajes, con tope aspiracional de 3 vueltas por agente.

Es el workflow más invocado del Protocol — se ejecuta sobre SPEC inicial, sobre cada 3B.X, sobre el Task Breakdown, sobre cada doc del paquete operativo PJM.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `documento_a_revisar` | path | producido por agente generador | sí | El archivo .md que se audita |
| `agente_generador_id` | string | composición de cadena (FASE 0) | sí | Identidad del agente Claude que produjo el doc |
| `pm_revisor_session_id` | string | output de WORKFLOW-HO-001.004 | sí | Identidad de la sesión OpenAI configurada |
| `contexto_referencia` | array<path> | inputs upstream del Protocol | sí | Documentos contra los cuales se valida (SPEC, 3B.X anteriores, etc.) |
| `cadena_revisores` | array<rol> | composición FASE 0 | no | Si vacío, solo PM Revisor audita |
| `vuelta_actual` | int | contador del workflow | sí | 1, 2 o 3 |

---

## 3. Precondiciones

- Documento existe en disco con versión declarada (v1.0, v1.1, etc.)
- PM Revisor está seteado y tiene los inputs de contexto
- PM tiene acceso a ambos modelos (Claude del generador + OpenAI del revisor)
- No hay otro ciclo REVMA en curso sobre el mismo documento

---

## 4. Reglas del Workflow

- **R1:** El PM Revisor SIEMPRE es modelo distinto al del agente generador. Si ambos son Claude, no es REVMA — es auto-revisión y no aplica.
- **R2:** El PM humano NO edita contenido — solo transporta mensajes y archivos.
- **R3:** Tope aspiracional de 3 vueltas por agente. Excepción documentable si la feature genuinamente requiere más vueltas (PM autoriza).
- **R4:** Si las vueltas exceden 3 por correcciones cosméticas (versionado, redacción), PM corta el ciclo y escala al PM Revisor — señal de revisor mal calibrado.
- **R5:** Si el agente generador detecta que un comentario downstream rompe la SPEC base → activar backfeed legítimo (escalar al PM, NO aplicar el comentario sin SPEC actualizada).
- **R6:** Cada vuelta genera nueva versión del documento (v1.0 → v1.1 → ...). Versiones intermedias se preservan hasta cierre del ciclo.

---

## 5. Pasos

### Paso 1 — PM transporta documento al PM Revisor

PM toma `documento_a_revisar` + `contexto_referencia` y los entrega al `pm_revisor_session_id` (OpenAI).

→ invoca **`VTT.SKILL-COMMENT-001`** (registro del envío en bitácora)

### Paso 2 — PM Revisor genera mensaje de revisión

PM Revisor audita el documento contra el contexto de referencia y genera mensaje estructurado:
- Si aprueba sin observaciones → emite **APROBADO**.
- Si tiene observaciones → emite **DEVUELTO** + lista de correcciones específicas con referencia a sección/línea.

### Paso 3 — PM transporta dictamen al agente generador

PM lleva el mensaje del PM Revisor al `agente_generador_id` (Claude).

Si el dictamen es **APROBADO** → saltar al Paso 7.
Si es **DEVUELTO** → continuar a Paso 4.

### Paso 4 — Agente generador procesa correcciones

Agente Claude lee las observaciones del PM Revisor.

¿Las correcciones rompen SPEC base? → **[DECISIÓN]**
- **SÍ** → activar backfeed: agente NO aplica correcciones, escala al PM con justificación. PM debe actualizar SPEC en FASE 1 antes de continuar. Workflow se SUSPENDE hasta que SPEC se actualice.
- **NO** → continuar a Paso 5.

### Paso 5 — Agente generador produce nueva versión

Agente aplica correcciones y emite versión incrementada (v1.0 → v1.1, etc.).

Documento nuevo se guarda en disco con sufijo de versión.
Versión anterior se mueve a `Versiones deprecadas/` o se preserva con sufijo `_vN_old`.

### Paso 6 — Verificar tope de vueltas

¿`vuelta_actual` < 3? → **[DECISIÓN]**
- **SÍ** → incrementar contador, regresar a Paso 1 con el documento nuevo.
- **NO** → continuar a Paso 6.bis (tope excedido).

### Paso 6.bis — Tope de 3 vueltas excedido

PM evalúa naturaleza de las correcciones pendientes:
- Si son cosméticas/redacción → cortar ciclo, registrar como cierre administrativo, emitir APROBADO con observaciones diferidas.
- Si son sustantivas → solicitar autorización al PM operativo para cuarta vuelta documentada.
- Si el PM operativo niega → escalar al PM Revisor (calibración mal hecha) y resetear ciclo con nuevo PM Revisor.

### Paso 7 — Cierre del ciclo

Documento aprobado:
- Se versiona como `v<X>_final` (o `v<X>` si versionado lineal).
- Se firma con metadata: `APROBADO_POR=pm_revisor_session_id`, `VUELTAS=<N>`, `FECHA=<ISO>`.
- Versiones intermedias se archivan en `Versiones deprecadas/`.

→ invoca **`VTT.SKILL-ATTACH-001`** para registrar el cierre del ciclo en bitácora del Protocol.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Documento aprobado versión final | archivo .md | misma ubicación del input, versión incrementada |
| Bitácora del ciclo | registro estructurado | bitácora del Protocol con vueltas, fechas, dictámenes |
| Versiones intermedias | archivos .md | carpeta `Versiones deprecadas/` |

---

## 7. Validación

Cómo verificar éxito del Workflow:
- Documento existe con versión final firmada.
- Bitácora registra cierre exitoso del ciclo.
- Todas las versiones intermedias están archivadas, no sueltas.
- No quedó ciclo REVMA suspendido sin resolución.

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Vueltas exceden 3 por temas cosméticos | PM Revisor mal calibrado | Cortar ciclo, escalar al PM Revisor para reajustar criterios |
| Agente generador insiste en aplicar correcciones que rompen SPEC | No detectó backfeed | PM activa backfeed manualmente, suspende ciclo |
| PM Revisor aprueba documento que claramente tiene gap | Auditor poco riguroso | Re-auditar con segundo PM Revisor (paralelo) |
| Versiones intermedias se pierden o pisan | No se aplicó regla R6 | Restaurar de git history, aplicar archivado correcto |
| Backfeed se activa pero nadie actualiza SPEC | Coordinación rota | PM escala para reactivar FASE 1 del Protocol padre |

---

## 9. Skills invocadas

- `VTT.SKILL-COMMENT-001` (registro de envíos en bitácora)
- `VTT.SKILL-ATTACH-001` (cierre del ciclo)

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón de aplicación |
|---|---|
| `RULE-REV-001` Tope 3 vueltas aspiracional | Paso 6 |
| `RULE-REV-002` Conflictos >20% rehacer auditoría | Métrica de salud agregada del ciclo |
| `RULE-ABAC-007` Aprobaciones solo HUMAN | Paso 7 — la firma final la respalda el PM humano |

---

**Documento:** `VTT.WORKFLOW-HO-001.001_ciclo_revma.md`
**Versión:** 1.0.0 — Workflow transversal del Protocol HO-001
**Fecha:** 2026-06-01
