# DICCIONARIO DE DELIVERABLES — FASE 5.9: ACCESSIBILITY TESTING

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.9 — Accessibility Testing  
**Total deliverables:** 4  
**Responsable de subfase:** QA Engineer  
**Aprueba:** Design Lead

---

### 5.9.1 WCAG Audit

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.9 Accessibility Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | Design Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere conocimiento de WCAG 2.1 AA criteria y herramientas de auditoría (axe, Lighthouse, WAVE).  
En VTT: un agente puede ejecutar automated a11y scans (axe-core, Lighthouse) y compilar resultados. Manual testing (screen reader, keyboard) requiere humano. Es parcialmente delegable.

**Qué es:** Auditoría completa de accesibilidad contra WCAG 2.1 AA: automated scan de todas las páginas (axe-core violations con severity y WCAG criterion), manual testing con screen reader (VoiceOver/NVDA) de flujos críticos, manual testing de keyboard navigation, y report consolidado de findings con severity, affected element, WCAG criterion violated, y fix recommendation.

**Para qué sirve:** Verifica que el producto es usable por personas con discapacidades: visual (screen reader, contraste), motora (keyboard only), auditiva (captions si hay media), y cognitiva (layout claro, language simple). WCAG AA es requisito legal en muchas jurisdicciones (ADA, EAA) y es buena práctica de UX para todos los usuarios.

**Inputs requeridos:**
- `4.4.14` Accessibility — implementación a auditar
- WCAG 2.1 AA criteria list
- Herramientas: axe-core, Lighthouse, WAVE
- Screen reader: VoiceOver (Mac) o NVDA (Windows)

**Dependencias (predecessors):**
- `4.4.14` Accessibility *(obligatorio)* — implementación a verificar
- `5.3.1` Test Environment *(obligatorio)*

**Habilita (successors):**
- `5.9.2` Accessibility Score — puntuación
- `5.9.3` Screen Reader Test — testing manual
- `5.9.4` Keyboard Navigation — testing manual
- Fixes de accesibilidad en sprint backlog

**Audiencia:**
- **Frontend Developer** — fixes a implementar
- **Design Lead** — validación de a11y design decisions
- **Compliance** — evidence de WCAG compliance
- **Product Owner** — awareness de gaps

**Secciones esperadas:**
1. Automated scan results (axe-core violations por página)
2. Manual testing results summary
3. Findings table (ID, page, element, WCAG criterion, severity, description, fix recommendation)
4. Findings by severity (critical, serious, moderate, minor)
5. Findings by WCAG principle (Perceivable, Operable, Understandable, Robust)
6. Pages audited (tabla: page, automated issues, manual issues, overall status)
7. Compliance summary (% of WCAG AA criteria met)
8. Recommendations prioritizadas

**Criterio de completitud:**
- [ ] Automated scan ejecutado en todas las páginas principales
- [ ] Manual testing de flujos críticos (al menos screen reader + keyboard)
- [ ] Findings documentados con WCAG criterion referenciado
- [ ] Severity clasificada por cada finding
- [ ] Fix recommendations incluidas
- [ ] Compliance summary calculado

**Anti-patrones:**
- ❌ **Solo automated scan:** axe detecta ~30-40% de issues — el resto requiere testing manual (heading hierarchy, reading order, meaningful link text).
- ❌ **"No tenemos usuarios con discapacidad":** 15% de la población tiene alguna discapacidad. Además, es requisito legal en muchas jurisdicciones.
- ❌ **A11y testing al final:** Encontrar 50 issues de a11y 1 semana antes del launch — demasiado tarde para arreglar.
- ❌ **Solo Lighthouse score:** Lighthouse es un subset — no reemplaza axe-core detallado ni testing manual.

**Template:** `phases/05-testing/deliverables/wcag-audit.md` *(pendiente)*

---

### 5.9.2 Accessibility Score

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.9 Accessibility Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | Design Lead |
| **Formato** | Métrica |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Pre-release + por sprint |

**Perfil de ejecución:** Requiere ejecutar Lighthouse y axe-core para obtener scores automatizados.  
En VTT: un agente puede ejecutar Lighthouse CI y reportar scores. Es altamente delegable.

**Qué es:** Puntuación de accesibilidad como métrica trackeable: Lighthouse a11y score (0-100, target ≥ 90), axe-core violation count por severity (critical: 0, serious: 0, moderate: < 5), y trend over time para verificar que no empeora con nuevos features. Medido por página principal y como score global.

**Para qué sirve:** El score es un "health check" rápido de accesibilidad: si era 95 y bajó a 82 después de un sprint, algo se rompió. El trend previene degradación gradual — cada sprint que agrega features puede introducir violations si no se monitorea.

**Inputs requeridos:**
- `5.9.1` WCAG Audit — findings como baseline
- Lighthouse CI configurado
- axe-core configurado

**Dependencias (predecessors):**
- `5.9.1` WCAG Audit *(obligatorio)* — baseline

**Habilita (successors):**
- Trend tracking de a11y quality
- CI gate (fail if score < threshold)

**Audiencia:**
- **QA Lead** — quality oversight
- **Frontend Developer** — awareness
- **Design Lead** — design quality

**Secciones esperadas:**
1. Lighthouse a11y score por página (tabla: page, score, target, pass/fail)
2. Global score (promedio ponderado por importancia de página)
3. axe-core violation count by severity (critical, serious, moderate, minor)
4. Trend vs sprint/release anterior
5. Target compliance (≥ 90 Lighthouse, 0 critical/serious axe violations)
6. Pages below target (lista con action items)

**Criterio de completitud:**
- [ ] Score calculado para todas las páginas principales
- [ ] Global score ≥ 90 (o plan para alcanzar)
- [ ] 0 critical y 0 serious axe violations
- [ ] Trend documentado vs periodo anterior
- [ ] CI gate configurado (opcional pero recomendado)

**Anti-patrones:**
- ❌ **Solo score global sin per-page:** Score promedio 92 pero la página de checkout tiene 65 — el promedio oculta problemas.
- ❌ **Score sin action:** Score de 78 sin plan para mejorar — data sin acción.
- ❌ **Score como único indicador:** Lighthouse 100 no garantiza accesibilidad real — screen reader testing aún necesario.

**Template:** `phases/05-testing/deliverables/accessibility-score.md` *(pendiente)*

---

### 5.9.3 Screen Reader Test

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.9 Accessibility Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | Design Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere testing manual con screen reader (VoiceOver en Mac, NVDA en Windows) — navegar la app completa sin ver la pantalla.  
En VTT: un agente NO puede ejecutar screen reader testing (requiere interacción auditiva con la app real). Puede generar el test plan y el report template. Es mínimamente delegable.

**Qué es:** Resultados de testing con screen reader en los flujos críticos del producto: cada página verificada para que el screen reader anuncie correctamente el contenido (heading hierarchy, landmarks, alt text, form labels, error messages, dynamic content updates, modal focus trap). Documenta qué funciona y qué no con steps para reproducir cada issue.

**Para qué sirve:** Un screen reader es cómo una persona ciega interactúa con el producto. Si el login form no tiene labels, el screen reader dice "edit text, blank" — el usuario no sabe qué campo es. Si un modal no tiene focus trap, el screen reader navega detrás del modal — confusión total. Este testing verifica la experiencia real de un usuario de screen reader.

**Inputs requeridos:**
- `5.9.1` WCAG Audit — automated findings como guide
- Screen reader instalado (VoiceOver/NVDA)
- `2.6.2` Happy Path Flows — flujos a testear con screen reader

**Dependencias (predecessors):**
- `5.9.1` WCAG Audit *(obligatorio)*
- `4.4.14` Accessibility *(obligatorio)* — implementación

**Habilita (successors):**
- Fixes de screen reader issues
- A11y compliance evidence

**Audiencia:**
- **Frontend Developer** — fixes (ARIA attributes, semantic HTML)
- **Design Lead** — heading hierarchy, content structure
- **QA Engineer** — documentation

**Secciones esperadas:**
1. Screen reader used (VoiceOver version, NVDA version, browser)
2. Flows tested (tabla: flow, pages, result pass/fail)
3. Per-page results:
   - Heading hierarchy (H1 → H2 → H3 logical order)
   - Landmarks (header, nav, main, footer announced correctly)
   - Images (alt text present and descriptive)
   - Forms (labels associated, error messages announced)
   - Dynamic content (live regions for updates, toasts, loading states)
   - Modals (focus trap, escape closes, focus returns)
4. Issues found (tabla: page, element, issue, WCAG criterion, severity, fix)
5. Overall assessment (usable/partially usable/not usable with screen reader)

**Criterio de completitud:**
- [ ] Flujos críticos (3-5) testeados con screen reader
- [ ] Heading hierarchy verificada por página
- [ ] Form labels verificados
- [ ] Modal focus trap verificado
- [ ] Alt text verificado en imágenes
- [ ] Dynamic content (toasts, loading) verificado
- [ ] Issues documentados con reproducción steps
- [ ] Overall assessment documentado

**Anti-patrones:**
- ❌ **Skip screen reader testing:** "Nadie usa screen reader" — 2.2 mil millones de personas con discapacidad visual en el mundo.
- ❌ **Testing solo con VoiceOver:** NVDA (Windows) tiene comportamiento diferente — idealmente testear con ambos.
- ❌ **Solo home page:** Testear solo el landing — los forms y flujos interactivos son donde más falla la accesibilidad.
- ❌ **"No sé usar un screen reader":** Documentar cómo usar VoiceOver/NVDA en el E2E docs (5.6.5) para que todo el equipo pueda.

**Template:** `phases/05-testing/deliverables/screen-reader-test.md` *(pendiente)*

---

### 5.9.4 Keyboard Navigation

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.9 Accessibility Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | Design Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere testing manual navegando toda la app solo con keyboard (sin mouse).  
En VTT: un agente NO puede ejecutar keyboard testing real (requiere interacción con la app). Puede generar checklist. Es mínimamente delegable.

**Qué es:** Resultados de testing de navegación por teclado: verificar que toda la funcionalidad es accesible sin mouse. Tab order lógico (sigue el visual layout), Enter/Space activa controles interactivos, Escape cierra modals/dropdowns, Arrow keys navegan listas/tabs/menus, focus visible en todos los elementos interactivos (focus ring claro), y no hay "focus traps" inesperados (excepto modals intencionales).

**Para qué sirve:** Usuarios con discapacidades motoras usan teclado (o dispositivos que emulan teclado) en vez de mouse. Power users también prefieren keyboard para eficiencia. Si un botón no se puede activar con Enter, o si el Tab salta un campo del form, el producto es inutilizable para estos usuarios.

**Inputs requeridos:**
- `5.9.1` WCAG Audit — findings de keyboard como guide
- `2.6.2` Happy Path Flows — flujos a testear con keyboard

**Dependencias (predecessors):**
- `5.9.1` WCAG Audit *(obligatorio)*
- `4.4.14` Accessibility *(obligatorio)*

**Habilita (successors):**
- Fixes de keyboard navigation issues
- A11y compliance evidence

**Audiencia:**
- **Frontend Developer** — fixes (tabindex, focus management, event handlers)
- **Design Lead** — focus visible design
- **QA Engineer** — documentation

**Secciones esperadas:**
1. Test methodology (keyboard only, browser used, OS)
2. Per-page results:
   - Tab order (logical? follows visual layout?)
   - Focus visible (clear focus ring on all interactive elements?)
   - Interactive elements (all activatable with Enter/Space?)
   - Modals (focus trapped? Escape closes? focus returns on close?)
   - Dropdowns/menus (Arrow keys navigate? Enter selects?)
   - Skip link (present? works? skips to main content?)
3. Issues found (tabla: page, element, issue, expected behavior, actual behavior, severity)
4. Tab order map per page (ordered list of focusable elements)
5. Overall assessment (fully navigable/partially/not navigable with keyboard)

**Criterio de completitud:**
- [ ] Todas las páginas principales verificadas con keyboard
- [ ] Tab order lógico verificado
- [ ] Focus visible en todos los elementos interactivos
- [ ] Enter/Space activa todos los botones y links
- [ ] Escape cierra todos los modals y dropdowns
- [ ] Skip link presente y funcional
- [ ] No hay focus traps inesperados
- [ ] Issues documentados con expected vs actual behavior

**Anti-patrones:**
- ❌ **Custom components sin keyboard support:** `<div onclick>` en vez de `<button>` — no focusable, no activable con Enter.
- ❌ **Focus invisible:** Tab navega pero no se ve dónde está el focus — el usuario keyboard se pierde.
- ❌ **Focus trap sin Escape:** Modal abierto sin forma de cerrarlo con keyboard — el usuario queda atrapado.
- ❌ **"Solo testeamos con mouse":** El mouse testing no detecta ninguno de estos issues — keyboard testing es obligatorio.

**Template:** `phases/05-testing/deliverables/keyboard-navigation.md` *(pendiente)*

---

## Tabla resumen — Fase 5.9

| Deliverable | Responsable | Delegable VTT |
|-------------|-------------|---------------|
| 5.9.1 WCAG Audit | QA Engineer | 🔶 — automated scan sí, manual testing no |
| 5.9.2 Accessibility Score | QA Engineer | ✅ — Lighthouse score automático |
| 5.9.3 Screen Reader Test | QA Engineer | ❌ — requiere testing manual con screen reader |
| 5.9.4 Keyboard Navigation | QA Engineer | ❌ — requiere testing manual con keyboard |
