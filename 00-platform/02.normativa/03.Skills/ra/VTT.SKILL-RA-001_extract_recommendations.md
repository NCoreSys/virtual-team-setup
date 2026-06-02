# VTT.SKILL-RA-001 — Extract recommendations from research consolidated

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-RA-001` |
| **Categoría** | RA (Research Analyst) |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-02 |
| **Aplica a** | Research Analyst (RA) |
| **Tokens estimados** | ~320 |
| **Cuándo se usa** | Paso 1 del pipeline RA — UNA invocación por cada `CONSOLIDADO_<feature>-<bloque>.md` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `consolidated_path` | string (path absoluto) | sí | Ruta al `CONSOLIDADO_<feature>-<bloque>.md` |
| `feature_name` | string (kebab-case) | sí | Nombre de la feature (ej. `hook-manager`) |
| `bloque_id` | string | sí | ID del bloque (ej. `HM-01`) |
| `output_dir` | path | sí | Dónde escribir el EXTRACT (típicamente `knowledge/research/<repo>/<feature>/`) |
| `template_path` | path | sí | Path a `TEMPLATE_EXTRACT_PER_FILE.md` |

> **Política contractual:** la skill recibe paths absolutos. NO infiere paths del contexto.

---

## Precondición

- El archivo `consolidated_path` existe y es legible (lectura `.md` con UTF-8)
- El template `template_path` existe y es válido
- `output_dir` existe (si no, crear con `mkdir -p`)
- El RA tiene en contexto los 8 marcadores definidos en `AGENT_PROFILE_BASE_RA.md` §4
- El RA tiene en contexto el `PLAN_INVESTIGACION_<feature>_*.md` (si existe) para conocer las subpreguntas del bloque

---

## Variables del entorno

```bash
$VTT_SETUP          # path al repo virtual-teams-setup/00-platform/
$REPO_ORIGEN        # path al repo origen donde están las investigaciones (ej. virtual-teams-Hook-Manager)
```

---

## Ejecución

### Lógica de extracción (paso a paso)

1. **Lectura completa línea por línea** del `CONSOLIDADO`. Prohibido escanear/resumir mentalmente.

2. **Identificar candidatos por patrón** (NO automatizable 100%, requiere lectura humana del agente):
   - Verbos modales/imperativos: "se recomienda", "se debe", "no se debe", "es crítico", "obligatorio", "evitar"
   - Marcadores estructurales del consolidado: `[CONSENSO 4/4]`, `[DIVERGENCIA]`, `Confianza 5/5`, `MEJORA`, `ALERTA`, `CONFIRMA`, `NEUTRO`
   - Frases con datos duros: números, %, umbrales, benchmarks, precios

3. **Clasificar cada candidato** con UN marcador (o combinación) de los 8:
   - 🔴 `[CRÍTICO]` — el consolidado dice explícitamente "debe" / "crítico" / "obligatorio"
   - 🟠 `[RECOMENDADO]` — "se recomienda" sin "crítico"
   - 🟡 `[OPCIONAL]` — "nice-to-have", "puede considerar"
   - ⚫ `[ANTI-PATRÓN]` — "no se debe", "evitar", "deprecated"
   - 🔵 `[DECISIÓN-CONFIRMADA]` — el consolidado marca `CONFIRMA` o equivalente
   - 🟣 `[GAP-DETECTADO]` — `ALERTA` o "VTT no contempla"
   - 🟢 `[VENTAJA-COMPETITIVA]` — "ningún framework", "diferenciador", "propietario único"
   - 🟤 `[CONVERGENCIA]` / `[DIVERGENCIA]` — metadata combinable con los anteriores

4. **Asignar `Impacto`** (Alto/Medio/Bajo) a cada recomendación basado en:
   - Alto: afecta arquitectura, decisión irreversible, mucha deuda si se ignora
   - Medio: afecta un subsistema, reversible con esfuerzo
   - Bajo: detalle de implementación

5. **Preservar citas literales** en `[CRÍTICO]` — entre comillas dobles `"..."` con `§` del consolidado de origen

6. **Detectar dependencias** entre recomendaciones ("X requiere Y antes") — anotar explícitamente

7. **Extraer datos duros** (números, benchmarks, umbrales, precios) con fuente original

8. **Verificar cobertura de subpreguntas** del prompt original (si el PLAN está disponible)

9. **Rellenar las 9 secciones del TEMPLATE_EXTRACT_PER_FILE.md**:
   - §1 Resumen (1-2 párrafos sintetizando §Resumen Ejecutivo del CONSOLIDADO)
   - §2 Recomendaciones agrupadas por marcador (8 subsecciones con tabla)
   - §3 Dependencias detectadas
   - §4 Datos duros
   - §5 Conflictos pendientes PM
   - §6 Subpreguntas cobertura
   - §7 Trazabilidad inversa
   - §8 Stats
   - §9 Notas RA

10. **Validar output**: cada recomendación tiene `Impacto`. Cada `[CRÍTICO]` tiene cita literal. Trazabilidad `§N.M` por ítem.

11. **Escribir el archivo** `EXTRACT_<feature>_<bloque>.md` en `output_dir`.

### Comando (Bash)

```bash
# Variables
CONS_PATH="<consolidated_path>"
FEATURE="<feature_name>"
BLOQUE="<bloque_id>"
OUTPUT_DIR="<output_dir>"
TEMPLATE="$VTT_SETUP/03.templates/research/TEMPLATE_EXTRACT_PER_FILE.md"
OUTFILE="$OUTPUT_DIR/EXTRACT_${FEATURE}_${BLOQUE}.md"

# Setup
mkdir -p "$OUTPUT_DIR"
cp "$TEMPLATE" "$OUTFILE"

# Pasos 1-10: el agente RA edita $OUTFILE con su lectura quirúrgica
# (no hay comando bash atómico — la skill es ejecutada cognitivamente por el agente)

# Paso 11 — Validar output con grep
grep -c "Impacto.*Alto\|Impacto.*Medio\|Impacto.*Bajo" "$OUTFILE"
grep -c "\[CRÍTICO\]" "$OUTFILE"
grep -c "§" "$OUTFILE"  # cuenta referencias § (trazabilidad)
```

> **Política:** esta skill es **cognitiva** — la ejecuta el agente leyendo y clasificando. No hay un script Python que la automatice porque depende del juicio del modelo. Lo que se valida es el output (cumple template + 8 marcadores + Impacto en todos).

---

## Validación

Cómo saber si el EXTRACT está bien hecho:

- `cat "$OUTFILE" | head -20` muestra el header con metadata (feature, bloque, fecha, procesado por)
- Cada recomendación tiene `Impacto: Alto|Medio|Bajo` (R3 del perfil)
- Cada `[CRÍTICO]` tiene cita literal entre comillas (R1)
- Las 9 secciones del template están completas o marcadas explícitamente como "Sin contenido en este consolidado"
- Stats §8 muestra conteos coherentes
- Notas §9 reflejan observaciones honestas del RA sobre la calidad del consolidado

```bash
# Validación quick
test -f "$OUTFILE" && wc -l "$OUTFILE"   # debe ser >100 líneas para consolidados de 200+ líneas
grep -q "## 1. Resumen del consolidado" "$OUTFILE" && echo "§1 OK"
grep -q "## 2. Recomendaciones" "$OUTFILE" && echo "§2 OK"
grep -q "## 9. Notas del RA" "$OUTFILE" && echo "§9 OK"
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| EXTRACT muy corto (<50 líneas) | El RA escaneó en vez de leer línea-por-línea | Re-procesar con lectura quirúrgica |
| Faltan citas literales en `[CRÍTICO]` | Parafraseo no permitido (R1) | Volver al consolidado y copiar las frases textuales |
| Faltan `Impacto:` en algunas filas | Olvido del campo obligatorio (R3) | Auditar tabla por tabla y completar |
| Subpreguntas §6 sin coberturar | El RA no leyó el `PLAN_INVESTIGACION_*.md` | Leer el PLAN antes de procesar |
| Marcadores inventados | Los 8 son cerrados (R2) | Usar el más cercano + nota explicativa |

---

## Scripts invocados

Sin scripts externos — esta skill es cognitiva. El bash de §Ejecución solo facilita setup + validación.

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-06-02 | Versión inicial. Lectura quirúrgica de 1 CONSOLIDADO → 1 EXTRACT siguiendo `TEMPLATE_EXTRACT_PER_FILE.md`. 8 marcadores cerrados + Impacto obligatorio + citas literales en CRÍTICO. Origen: necesidad de procesar investigaciones consolidadas multi-agente sin perder recomendaciones críticas (caso Hook Manager R2.0). |
