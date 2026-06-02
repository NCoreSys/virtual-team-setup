# VTT.WORKFLOW-HO-001.004 — Setear PM Revisor en Modelo Distinto

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.004` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.0.4 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PM |
| **Tipo** | [PROCESO] sub-procedimiento de setup |

---

## 1. Propósito

Configurar una sesión de PM Revisor en un modelo IA distinto al de los agentes generadores (típicamente OpenAI cuando los generadores son Claude), con contexto suficiente para auditar los outputs del Protocol durante todas las iteraciones REVMA.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `metodologia_path` | path | FASE 1 (borrador inicial) | sí | METODOLOGIA del bloque |
| `spec_path` | path | FASE 1 (borrador inicial) | sí | SPEC del bloque |
| `cadena_roles` | array | output de WORKFLOW-HO-001.002 | sí | Composición de la cadena de revisores |
| `camino_elegido` | enum (A/B/C) | output de WORKFLOW-HO-001.003 | sí | Determina contexto adicional |
| `modelo_revisor` | enum | configuración PM | sí | `openai_gpt-4` / `openai_gpt-5` / otro modelo distinto al generador |

---

## 3. Precondiciones

- METODOLOGIA + SPEC borradores existen.
- PM tiene acceso a 2 modelos IA distintos (uno para generadores, otro para revisor).
- DECISION_BLOQUE registrado con cadena y camino.

---

## 4. Reglas del Workflow

- **R1:** El modelo del revisor SIEMPRE debe ser de proveedor distinto al de los generadores (Claude → OpenAI o viceversa). NO puede ser Claude revisando Claude.
- **R2:** El revisor recibe METODOLOGIA + SPEC + cadena como contexto base, NO los outputs intermedios.
- **R3:** El revisor NO debe tener acceso a versiones previas del documento que audita (para que su revisión sea independiente, no comparativa).
- **R4:** Una sesión de PM Revisor cubre TODO el ciclo del Protocol, no se cambia entre fases (salvo recalibración explícita §6.bis del WORKFLOW-001).

---

## 5. Pasos

### Paso 1 — PM abre sesión nueva en modelo revisor

PM inicia sesión en el modelo distinto (`modelo_revisor`).

### Paso 2 — PM provee contexto base al revisor

PM entrega al revisor:
- Documento METODOLOGIA (borrador inicial)
- Documento SPEC (borrador inicial)
- Lista de cadena de roles que entrarán al ciclo
- Camino elegido (A/B/C) y sus implicaciones
- Formato de dictamen esperado (APROBADO / DEVUELTO con correcciones específicas)

### Paso 3 — PM provee criterios de revisión al revisor

PM instruye al revisor sobre:
- Tope aspiracional de 3 vueltas por agente.
- Cómo distinguir corrección sustantiva vs. cosmética.
- Cuándo emitir backfeed (si detecta que el documento revela gap en SPEC base).
- Severidad de observaciones: bloqueante / mayor / menor.

### Paso 4 — PM registra session_id del revisor

PM guarda identificador de la sesión OpenAI (o equivalente) en DECISION_BLOQUE para referencia durante todo el ciclo.

### Paso 5 — PM ejecuta prueba de calibración

PM hace una pregunta de prueba al revisor sobre la SPEC para verificar que entiende el contexto.

¿La respuesta del revisor refleja entendimiento correcto? → **[DECISIÓN]**
- **NO** → re-proveer contexto + ajustar instrucciones, repetir Paso 5.
- **SÍ** → revisor calibrado, listo para iniciar FASE 1.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Sesión PM Revisor configurada | session_id registrado | DECISION_BLOQUE |
| Criterios de revisión documentados | sección en DECISION_BLOQUE | mismo doc |

---

## 7. Validación

- session_id del PM Revisor está registrado en DECISION_BLOQUE.
- Prueba de calibración exitosa.
- Revisor tiene acceso a METODOLOGIA + SPEC borradores.
- Revisor entiende el formato de dictamen esperado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Revisor da feedback genérico sin referencia a SPEC | Contexto no se entregó completo | Re-proveer SPEC + insistir en citas específicas |
| Revisor aprueba todo en primera vuelta sistemáticamente | Calibrado para complacer | Re-instruir con criterios estrictos + dar ejemplos de DEVUELTO esperado |
| Revisor demanda correcciones cosméticas en vuelta 3+ | Calibrado mal | Cortar ciclo, resetear sesión con criterios "sustantivo > cosmético" |
| PM usa Claude como revisor de Claude | Viola R1 | Cancelar setup, recrear con modelo distinto |

---

## 9. Skills invocadas

(Ninguna — es setup manual del PM)

---

**Documento:** `VTT.WORKFLOW-HO-001.004_setear_pm_revisor.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
