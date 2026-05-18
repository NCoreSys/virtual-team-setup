# Guía Universal para Agente: Generación de SOPs con Diagramas de Flujo

## Propósito

Esta guía instruye al agente para transformar la descripción de **cualquier proceso operativo** — sin importar industria, dominio o complejidad — en un SOP (Standard Operating Procedure) profesional con diagramas de flujo estructurados.

El agente no necesita conocimiento previo del dominio. Su trabajo es extraer la lógica del proceso a partir de lo que el usuario describe y organizarla en un formato estandarizado, completo y sin ambigüedades.

---

## 1. Qué es un SOP y qué debe lograr

Un SOP es un documento que permite a cualquier persona con el rol adecuado ejecutar un proceso de principio a fin sin depender de conocimiento tribal. Para lograr esto, debe responder cinco preguntas en cada paso:

1. **¿Quién?** — Qué actor o rol ejecuta la acción.
2. **¿Qué?** — Qué acción concreta se realiza.
3. **¿Con qué?** — Qué herramientas, sistemas o documentos se usan.
4. **¿Qué puede salir mal?** — Qué decisiones o bifurcaciones existen.
5. **¿Qué se produce?** — Qué output genera el paso (documento, registro, estado, notificación).

Si un paso del flujo no responde al menos las primeras dos preguntas, está incompleto.

---

## 2. Vocabulario Gráfico Estándar

Todos los diagramas producidos por el agente deben usar esta simbología consistente:

| Elemento | Forma | Cuándo usarlo |
|---|---|---|
| **Inicio / Fin** | Cápsula (rectángulo redondeado) | Exactamente un inicio y al menos un fin por proceso. Si hay múltiples puntos de entrada, cada uno es un proceso separado. |
| **Paso de proceso** | Rectángulo | Cualquier acción ejecutada por un actor. Siempre lleva prefijo del actor responsable. |
| **Decisión** | Rombo | Cualquier punto donde el flujo se bifurca. Siempre tiene exactamente dos o más salidas etiquetadas (Sí/No, o valores específicos). |
| **Subproceso** | Rectángulo con bordes dobles | Referencia a otro proceso documentado por separado. Indica que el flujo "sale" hacia otro SOP. |
| **Documento** | Rectángulo con base ondulada | Cualquier artefacto documental que se genera, consume o transforma en el paso. |
| **Datos / Sistema** | Paralelogramo | Dato o información que entra o sale del proceso, o interacción con un sistema. |
| **Conector** | Círculo con número o letra | Vincula puntos del diagrama que no pueden conectarse con una línea directa (por espacio o porque cruzan páginas). |
| **Nota contextual** | Caja de texto con borde punteado | Información aclaratoria que no es un paso del flujo: reglas de negocio, umbrales, contenido requerido, excepciones. |

**Regla:** El agente debe incluir una página de leyenda al inicio del SOP si el documento contiene más de un diagrama.

---

## 3. Anatomía de un SOP Completo

### 3.1 Estructura del documento

```
1. Portada / Encabezado
   - Nombre del proceso
   - Versión y fecha
   - Actores involucrados
   - Sistemas involucrados

2. Leyenda de simbología
   - Solo si hay más de un diagrama

3. Diagrama(s) de flujo del proceso principal
   - Organizado por fases
   - Con happy path + excepciones integradas

4. Diagramas de subprocesos
   - Uno por cada subproceso referenciado desde el principal

5. Anexos (opcional)
   - Templates de documentos mencionados en el flujo
   - Tablas de referencia (códigos de error, criterios de decisión, etc.)
```

### 3.2 Organización espacial del diagrama

El agente debe organizar cada diagrama en dos dimensiones:

**Eje horizontal → Fases:** Las etapas macro-secuenciales del proceso. Cada fase agrupa pasos que comparten un propósito. Un proceso típico tiene entre 2 y 5 fases. Nombrarlas con sustantivos o gerundios descriptivos.

**Eje vertical → Actores (swimlanes):** Cada fila horizontal corresponde a un actor o rol. Los pasos se colocan en la fila del actor responsable. Esto hace inmediatamente visible quién hace qué.

Si el proceso tiene pocos actores (1-2), los swimlanes pueden ser implícitos (el actor se indica como prefijo en cada paso). Si tiene 3+ actores, los swimlanes deben ser explícitos.

---

## 4. Metodología de Extracción: De Descripción a Diagrama

Cuando el usuario describe un proceso (en texto libre, en bullets, en conversación, o con un documento existente), el agente sigue estos pasos en orden:

### Paso 1: Identificar el alcance

Determinar dónde empieza y dónde termina el proceso.

- **Trigger de inicio:** ¿Qué evento dispara el proceso? (una solicitud, una llegada, un evento temporal, una señal de sistema).
- **Condición de fin:** ¿Qué estado marca el proceso como completado? Puede haber múltiples finales (éxito, cancelación, escalamiento).

*Pregunta al usuario si no es claro:* "¿Qué evento inicia este proceso y qué resultado marca que está completo?"

### Paso 2: Listar actores

Extraer todos los roles, personas, equipos o sistemas que participan.

Para cada actor, determinar:
- **Nombre o rol** (no personas específicas, sino roles: "Supervisor", "Sistema ERP", "Cliente").
- **Tipo:** Humano, sistema automático, o actor externo.
- **Responsabilidad general:** Qué tipo de acciones realiza (ejecuta, aprueba, notifica, registra).

### Paso 3: Mapear el happy path

Documentar el camino ideal — el flujo cuando todo sale bien, sin excepciones ni errores. Este es el esqueleto del diagrama.

Cada paso debe seguir el formato:

```
[Actor] + [verbo en presente indicativo] + [objeto] + [complemento opcional]
```

Ejemplos válidos para cualquier dominio:
- "Supervisor aprueba la solicitud en el sistema"
- "Sistema envía notificación al solicitante"
- "Técnico ejecuta la inspección según protocolo"
- "Cliente firma el acta de entrega"

**Regla:** Los pasos deben ser atómicos. Si un paso contiene "y" o "luego", probablemente son dos pasos.

### Paso 4: Inyectar puntos de decisión

Recorrer el happy path y en cada paso preguntar: "¿Puede esto NO salir bien?" o "¿Hay condiciones que cambien el siguiente paso?"

Por cada respuesta afirmativa, insertar un rombo de decisión. Cada decisión debe tener:
- **Pregunta clara** (no ambigua).
- **Todas las salidas posibles** (mínimo 2), cada una etiquetada.
- **Un camino completo para cada salida** — nunca dejar un camino sin destino.

### Paso 5: Desarrollar caminos alternativos

Para cada salida negativa o excepcional de una decisión, documentar el flujo completo hasta que:
- Se reincorpore al happy path, O
- Llegue a un fin alternativo, O
- Salga hacia un subproceso.

**Regla crítica:** El agente nunca debe resolver una excepción con un solo paso genérico como "resolver el problema". Debe documentar quién se entera, quién actúa, qué se hace, y cómo se cierra.

### Paso 6: Identificar artefactos documentales

Recorrer todos los pasos y para cada uno preguntar: "¿Este paso genera, consume o modifica algún documento, registro, formulario, checklist, reporte o archivo?"

Cada artefacto identificado debe:
- Aparecer como elemento `Document` en el diagrama, conectado al paso que lo genera/consume.
- Tener un nombre consistente a lo largo de todo el SOP (no llamarlo "checklist" en un lugar y "lista de verificación" en otro).

### Paso 7: Identificar integraciones de sistema

Si el proceso involucra sistemas (software, bases de datos, APIs, integraciones), documentar:
- **Qué sistema** ejecuta o recibe la acción.
- **Qué dato** se transmite.
- **Qué pasa si la integración falla** (siempre incluir el camino de error).

### Paso 8: Agregar notas contextuales

Recorrer el diagrama y para cada paso o decisión preguntar: "¿Hay información que el ejecutor necesita saber pero que no es un paso del flujo?"

Tipos comunes de notas:
- **Contenido requerido:** Qué campos o datos debe contener un input.
- **Reglas de negocio:** Umbrales, porcentajes, criterios de decisión.
- **Configuración operativa:** Horarios, frecuencias, capacidades.
- **Excepciones conocidas:** Casos edge que no ameritan su propio camino en el diagrama.
- **Referencias normativas:** Estándares, políticas o regulaciones aplicables.

### Paso 9: Agrupar en fases

Con el diagrama completo, agrupar los pasos en fases lógicas. Criterios para dividir fases:
- **Cambio de responsabilidad principal:** Cuando el actor dominante cambia.
- **Cambio de naturaleza de la actividad:** De planificación a ejecución, de ejecución a verificación.
- **Punto de no retorno:** Momentos donde el proceso cambia de estado irreversiblemente.
- **Handoff entre equipos o sistemas.**

### Paso 10: Validar completitud

Checklist final antes de entregar:

- [ ] ¿Todo camino llega a un End o a un conector hacia otro proceso?
- [ ] ¿Toda decisión tiene todas sus salidas documentadas con caminos completos?
- [ ] ¿Todo paso tiene un actor explícito?
- [ ] ¿Todo documento mencionado en texto aparece como elemento en el diagrama?
- [ ] ¿Todo sistema con integración tiene su camino de error?
- [ ] ¿Las notas contextuales cubren reglas de negocio que no son obvias?
- [ ] ¿Los conectores entre páginas/procesos están numerados y tienen destino claro?
- [ ] ¿Se puede recorrer el diagrama de Start a End sin encontrar un punto muerto?

---

## 5. Patrones Recurrentes

Los procesos operativos, sin importar el dominio, tienden a reutilizar patrones estructurales. El agente debe reconocer cuándo aplicar cada uno:

### 5.1 Patrón: Validación con bifurcación

**Cuándo aparece:** Cada vez que algo debe ser revisado antes de continuar.

```
[Actor] valida [objeto] contra [criterio]
    → ¿Válido?
        → Sí: continuar flujo
        → No: [acción correctiva] → reintentar o escalar
```

### 5.2 Patrón: Aprobación

**Cuándo aparece:** Cuando un paso requiere autorización de un nivel superior.

```
[Actor] solicita aprobación a [Aprobador]
    → ¿Aprobado?
        → Sí: continuar
        → No: [Actor] realiza ajustes → reenviar para aprobación
                O → proceso se cancela/cierra
```

### 5.3 Patrón: Integración de sistema

**Cuándo aparece:** Cuando dos sistemas intercambian datos.

```
[Sistema A] envía [dato] a [Sistema B]
    → ¿Procesado correctamente?
        → Sí: continuar
        → No: escalar a [equipo técnico]
            → [Equipo] diagnostica y resuelve
            → ¿Resuelto?
                → Sí: reintentar transmisión
                → No: notificar a stakeholders sobre delay + ETA
```

### 5.4 Patrón: Inspección / Auditoría

**Cuándo aparece:** Cuando se debe verificar el estado físico o la calidad de algo.

```
[Actor] inspecciona [objeto]
    → ¿Incidencia detectada?
        → Sí: documentar (fotografía, registro, reporte)
              → segregar/aislar elemento afectado
              → notificar a [responsable]
              → esperar decisión
        → No: continuar
```

### 5.5 Patrón: Reconciliación / Conteo

**Cuándo aparece:** Cuando se comparan cantidades o datos esperados vs reales.

```
[Actor] compara [dato real] vs [dato esperado]
    → ¿Coinciden?
        → Sí: cerrar/confirmar
        → No: realizar segundo conteo/verificación
            → ¿Discrepancia persiste?
                → Sí: reportar → esperar resolución
                → No: continuar
```

### 5.6 Patrón: Escalamiento

**Cuándo aparece:** Cuando un problema excede la capacidad de resolución del nivel actual.

```
[Actor] detecta problema fuera de su alcance
    → escala a [nivel superior]
    → [Nivel superior] investiga
    → informa resultado
    → ¿Procede acción?
        → Sí: ejecutar → documentar como lección aprendida
        → No: cerrar → informar al interesado
```

### 5.7 Patrón: Capacidad / Disponibilidad

**Cuándo aparece:** Cuando el proceso depende de un recurso limitado.

```
[Actor] verifica disponibilidad de [recurso]
    → ¿Disponible?
        → Sí: asignar/programar
        → No: reprogramar / priorizar / buscar alternativa
```

### 5.8 Patrón: Manejo de variaciones (exceso/faltante)

**Cuándo aparece:** Cuando la realidad no coincide con lo esperado en cantidad o tipo.

```
Detectar variación
    → ¿Tipo de variación?
        → Exceso: [procedimiento de devolución o cuarentena]
        → Faltante: [notificar → reconciliar → documentar]
        → Error de tipo: [segregar → notificar → esperar instrucciones]
```

---

## 6. Manejo de Información Incompleta

El usuario rara vez entrega un proceso perfectamente descrito. El agente debe:

1. **Generar con lo que tiene:** Producir un primer borrador del SOP con la información disponible.
2. **Marcar huecos explícitamente:** Donde falte información, insertar un placeholder visible:
   ```
   [PENDIENTE: ¿Quién aprueba este paso?]
   [PENDIENTE: ¿Qué pasa si la validación falla?]
   [PENDIENTE: ¿Qué documento se genera aquí?]
   ```
3. **Hacer preguntas específicas:** Al entregar el borrador, listar las preguntas concretas que necesita responder para completar el SOP. No preguntar genéricamente "¿falta algo?" sino "¿Quién aprueba la solicitud de compra cuando supera X monto?"

---

## 7. Formato de Salida

El agente produce el SOP en el formato que el usuario solicite:

- **Markdown estructurado:** Descripción textual con indentación para decisiones y caminos. Ideal para documentación viva.
- **Mermaid:** Código de diagramas renderizable en GitHub, Notion, documentación técnica.
- **Descripción para herramienta visual:** Texto organizado para recrear en Visio, Lucidchart, draw.io u otra herramienta.
- **SVG/HTML renderizado:** Diagrama visual directo.

Independientemente del formato visual, el agente siempre debe acompañar el diagrama con:
- **Lista de actores** con sus responsabilidades.
- **Glosario de términos** si el proceso usa vocabulario especializado.
- **Lista de artefactos** (documentos, formularios, reportes) con descripción breve.

---

## 8. Prompt de Invocación

Para que el usuario active este comportamiento en el agente:

```
Genera un SOP con diagrama de flujo para el siguiente proceso:

[Descripción del proceso]

Contexto adicional:
- Actores principales: [listar si se conocen]
- Sistemas involucrados: [listar si se conocen]
- Documentos que se generan: [listar si se conocen]
- Reglas de negocio relevantes: [listar si se conocen]

Sigue la metodología definida en SOP_Generation_Guide.md.
Formato de salida: [markdown / mermaid / visual / texto para herramienta]
```

Si el usuario no proporciona contexto adicional, el agente procede con lo que tiene y marca los huecos como se indica en la sección 6.
