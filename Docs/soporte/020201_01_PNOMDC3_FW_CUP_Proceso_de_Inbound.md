# CL Procedimiento Normalizado de Operación

**Código:** 020201.01.PNOMDC3.FW.CUP
**Título:** Proceso de Inbound de Cambridge University Press
**Página:** 10 de 10

---

## Tabla de Contenido

1. [Propósito](#10-propósito)
2. [Campo de Aplicación](#20-campo-de-aplicación)
3. [Responsabilidades](#30-responsabilidades)
4. [Definiciones](#40-definiciones)
5. [Procedimiento](#50-procedimiento)
   - 5.1 [Planeación](#51-planeación)
   - 5.2 [Recibo](#52-recibo)
   - 5.3 [Ingreso](#53-ingreso)
6. [Referencias Cruzadas](#60-referencias-cruzadas)
7. [Resumen de Revisiones](#70-resumen-de-revisiones)
8. [Anexos](#anexos)

---

## 1.0 Propósito

El propósito de este procedimiento es establecer los pasos a seguir bajo la conformidad de los estándares de calidad establecidas por Kuehne-Nagel para el recibo e ingreso de los productos de Cambridge University Press.

## 2.0 Campo de Aplicación

Este procedimiento aplica para el proceso de recibo en la cuenta del cliente Cambridge University Press en el MDC F-III, para todos los arribos.

## 3.0 Responsabilidades

3.1 Es responsabilidad del **Gerente de Operaciones** asegurar el cumplimiento del presente procedimiento y proporcionar los recursos necesarios para el cumplimiento correcto de este proceso.

3.2 Es responsabilidad del **Gerente de Operaciones** y el **Supervisor** realizar las actualizaciones, cumplimiento y validación del PNO de Inbound, así como la capacitación del personal involucrado en el procedimiento.

3.3 **Personal Operativo** apegarse a lo indicado en el procedimiento.

## 4.0 Definiciones

**Acta de Hechos** (MDC.CL.0029 Anexo No. 3): Documento en el cual se registran las incidencias al término de la descarga (dañados, sobrantes, faltantes de origen).

**Boleta de Carga y/o Descarga** (MX.QSHE.0005 Anexo No. 2): Formato que se expide en el área de vigilancia para controlar el acceso y la salida del transporte.

**CIEL-FW**: WMS utilizado en las instalaciones del MDC para el control del inventario de los clientes.

**CUP**: Cambridge University Press, es el nombre del cliente a quien Kuehne-Nagel prestará sus servicios.

**EDI**: Electronic Data Interchange, archivo generado de manera automática que es utilizado para transmitir información de un sistema a otro.

**Folio de RD**: Numeración ascendente, con el cual ingresa la mercancía en el sistema.

**ISBN**: Es el número de producto con el cuál CUP identifica sus productos. Este número es el mismo que EAN.

**MDC** (Master Distribution Center): Lugar en donde se almacena, retrabaja y se distribuye la mercancía de los clientes.

**RD** (Recibo de Depósito, MDC.CL.0005 Anexo No. 1): Documento en el cual se registran las cualidades y cantidades de los productos que ingresan al MDC, el cual será emitido y se asigna un número en el área de recibo dentro del MDC y anexos de K+N.

**SAP**: ERP utilizado para controlar las operaciones de varias áreas de una organización.

**WMS** (Warehouse Management System): Sistema en el cual se registran los ingresos de las mercancías de nuestros clientes (CIEL-FW).

## 5.0 Procedimiento

### 5.1 Planeación

5.1 CUP genera la orden de compra en el sistema SAP. El sistema SAP es utilizado por CUP en sus operaciones. El sistema SAP generará el EDI para envío de información a CIEL-FW.

5.1.1 Si el ISBN que se quiere agregar CUP en la PO no se encuentra en la base de datos de SAP, CUP deberá dar de alta el ISBN en su sistema.

5.1.2 Una vez dado de alta el ISBN en el sistema SAP, se dará de alta el nuevo ISBN en el sistema CIEL-FW de acuerdo al procedimiento "Alta de códigos nuevos en CIEL-FW".

5.1.3 CUP revisa con el Auxiliar Administrativo de Kuehne-Nagel acerca de la disponibilidad de recibo de acuerdo a la capacidad diaria.

5.1.4 En caso de que no se tenga capacidad de ingreso, el Auxiliar Administrativo enviará una notificación vía correo electrónico a CUP informando de la situación. CUP reprogramará el recibo de la unidad.

5.1.5 CUP envía a KN la prealerta con los datos generales de recibo:

- Datos de la PO
- Información del transporte, placas, tipo de unidad
- Datos de llegada
- Tipo de recibo: nacional o exportación

5.1.6 El Auxiliar Administrativo confirma que la PO exista en CIEL-FW. En caso de que la PO no exista, informará al Supervisor de Operaciones, quien escalará el tema con el equipo de IT de KN y de CUP para determinar si la PO no existe por algún problema de transmisión de datos.

5.1.7 El Auxiliar Administrativo programará el recibo de la unidad en el archivo electrónico "Plan de Recibos" (Ver "Llenado de Plan de Recibos") y generará los documentos de ingreso:

- Recibo de Depósito (MDC.CL.0005)
- Check List verificación Unidad Transporte (MDC.CL.0007)
- Acta de Hechos (MDC.CL.0029)

Los documentos los mantendrá almacenados hasta la llegada de la unidad.

5.1.8 El Auxiliar Administrativo imprimirá de manera diaria el Plan de Recibos y se lo entregará al Supervisor de Operaciones y al Coordinador de Operaciones. Adicional, mantendrá el Plan de Recibos a la mano para revisar el avance de los recibos.

### 5.2 Recibo

5.2.1 El transporte llega a las instalaciones de KN y realiza los procedimientos de seguridad requeridos. El área de patios entrega la Boleta de Carga y/o Descarga.

5.2.2 El Chofer se reporta con el Auxiliar Administrativo en la mesa de control, a quien le entrega la "Boleta de Carga y/o Descarga", así como los documentos de ingreso, tales como: Factura, Factura comercial, Carta Porte, Pedimento, etc.

5.2.3 El Auxiliar Administrativo informa al conductor el número de cortina en la que se debe colocar la unidad, informándole que no rompa el sello.

5.2.4 El Auxiliar Administrativo actualizará la Bitácora de Unidades con los datos de la unidad y del chofer. Así mismo actualizará el plan de descarga.

5.2.5 El Auxiliar Administrativo informa al Supervisor de Operaciones y/o Coordinador de Operaciones de la llegada del transporte y le entrega los documentos recibidos en el punto 5.2.2 y los documentos que previamente generó en el punto 5.1.7, así como la cámara fotográfica.

5.2.6 El Supervisor de Operaciones y/o Coordinador de Operaciones realizan el recibo de producto de acuerdo a la Instrucción de Trabajo "Proceso de Recibo".

5.2.7 Una vez concluido el recibo, el Auxiliar Administrativo recibirá los documentos de recibo llenos y la cámara fotográfica y procederá al cierre del recibo en la Bitácora de Recibos (Ver "Llenado de Bitácora de Unidades" - 020401.01.ITVMDC3.FW).

5.2.8 El Auxiliar Administrativo liberará al transporte y le entregará una copia de:

- Recibo de Depósito (MDC.CL.0005)
- Check List verificación Unidad Transporte (MDC.CL.0007)
- Acta de Hechos (MDC.CL.0029) — en caso de que aplique
- Sellar la Factura y/o PO
- Boleta de Carga y/o Descarga (MX.QSHE.0005)

5.2.9 El Auxiliar Administrativo informará al Supervisor de Operaciones y al Auxiliar Administrativo acerca de la conclusión del recibo.

### 5.3 Ingreso

5.3.1 El Supervisor de Operaciones y/o Coordinador de Operaciones realizan el Ingreso de producto de acuerdo a la Instrucción de Trabajo "Proceso de Ingreso".

5.3.2 Una vez terminado el ingreso de Producto en CIEL-FW, el WMS generará el EDI correspondiente para el envío de información al sistema SAP de CUP.

> **Nota:** En el caso del ingreso de las devoluciones, el sistema no enviará algún EDI a CUP, ya que no existe interface.

5.3.3 El Auxiliar Administrativo almacena las evidencias de recibo de acuerdo a las instrucciones de trabajo:

- Almacenamiento de Documentos
- Almacenamiento de Evidencia Fotográfica

5.3.4 El Auxiliar Administrativo al final de la jornada laboral, enviará vía correo electrónico el Plan de Recibos actualizado al Gerente de Operaciones.

5.3.5 El Auxiliar Administrativo actualizará el "Dashboard Gerencial" con los datos de recibo.

## 6.0 Referencias Cruzadas

| Código | Documento |
|---|---|
| MDC.CL.0029 | Acta de Hechos |
| MX.QSHE.0005 | Boleta de Carga y/o Descarga |
| MDC.CL.0005 | Recibo de Depósito |
| 020301.01.WIMDC3.FW.CUP | Alta de códigos nuevos en CIEL-FW |
| 020401.01.ITVMDC3.FW | Llenado de Bitácora Unidades |
| 020303.01.WIMDC3.FW.CUP | Proceso de Recibo |
| 020304.01.WIMDC3.FW.CUP | Proceso de Ingreso CUP |
| 090301.01.WIMDC3.FW.CUP | Almacenamiento de Documentos |
| 090302.01.WIMDC3.FW.CUP | Almacenamiento de Evidencia Fotográfica |
| — | Plan de Recibos |
| — | Llenado de Plan de Recibos |
| — | Dashboard Gerencial |

## 7.0 Resumen de Revisiones

Todos los cambios y las revisiones se identifican con letras itálicas y con texto *café*.

| Versión | Fecha de Revisión | Editores | Detalles |
|---|---|---|---|
| 001 | 19-Jun-2021 | Martin Rivas | Documento Inicial |

## Anexos

### Anexo 1 — Recibo de Depósito

*(Ver documento MDC.CL.0005)*

### Anexo 2 — Boleta de Carga y/o Descarga

*(Ver documento MX.QSHE.0005)*

### Anexo 3 — Acta de Hechos

*(Ver documento MDC.CL.0029)*

### Anexo 4 — Diagrama de Flujo

*(Ver documento 020601.01.FWCMDC3.FW.CUP Diagramas Inbound)*

---

| Editor (elaboró/revisó) | Dueño (aprobó) | Última Actualización |
|---|---|---|
| Martin Rivas Reynoso, MEX WM Gerente de Operaciones | Aldo Robles, MEX FW Distribution Center Manager | 19/06/2021 |

*Versión: 001 — Versión más reciente en Intranet — No controlada si se imprime*

*MX.QSHE.0002 Rev. Jun-2020*
