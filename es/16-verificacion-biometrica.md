# Política de verificación biométrica de los Earthlings

**En vigor desde el momento de su publicación**

> En caso de discrepancia de la presente Política con la [Carta](https://earth-lings.org/documents/es/es05-carta.html) se aplica la Carta, y en caso de discrepancia de la Carta con la [Declaración](https://earth-lings.org/documents/es/es01-declaracion.html), la Declaración. Las reglas generales de tratamiento de datos personales están en la [Política de privacidad](https://earth-lings.org/documents/es/es28-politica-de-privacidad.html).

## Lo esencial, en breve

- la biometría se trata en el momento de la comprobación y no se conserva;
- para que una misma persona no pueda tener dos pasaportes en vigor, se conservan únicamente hashes criptográficos irreversibles;
- se puede volver tras la salida en cualquier momento;
- un seudónimo en lugar del nombre real: usted elige;
- la biometría sirve a la confianza, no al control;
- sistema propio de comprobación, separación de los almacenes, minimización de datos.

---

# SECCIÓN 01. Principios

## Para qué la biometría

Sirve a un solo fin: acreditar que detrás de cada voto hay una sola persona viva y única. Es la base de la confianza entre desconocidos, y nada más. El sistema está diseñado de modo que no pueda emplearse para vigilar.

## La persona, no los documentos

La persona importa más que los documentos. Su pertenencia al pueblo la determina su libre elección, y no un pasaporte o una nacionalidad. La tarea de la comprobación no es un reconocimiento desde fuera, sino la confirmación de un hecho simple: usted es usted, y es uno solo.

## Cuatro principios

**1. Confirmación de la unicidad, no control.** La comprobación protege al pueblo de los registros múltiples, pero no crea una base para vigilar.

**2. La pertenencia se acredita personalmente.** Los documentos estatales siguen en su lugar: la comprobación se limita a cotejar la identidad, sin sustituir nada.

**3. Confianza mediante la comprobación.** En una comunidad sin poder central, una unicidad acreditada crea una capa básica de confianza. Eso no garantiza la buena fe en un trato concreto, pero elimina la multiplicidad anónima de cuentas como fuente de manipulaciones.

**4. Protección frente a los abusos.** La separación de los almacenes, el cifrado y la imposibilidad práctica de reconstruir una imagen a partir de los datos conservados están hechos para que el sistema no pueda emplearse para una vigilancia masiva.

---

# SECCIÓN 02. Ámbito de aplicación y consentimiento

La presente Política determina el tratamiento de los datos biométricos al firmar la Declaración, al obtener la condición de earthling y al participar en la infraestructura del pueblo.

## Base jurídica

Los datos biométricos pertenecen a la categoría especial de datos personales conforme al artículo 9 del RGPD y se tratan **exclusivamente sobre la base de su consentimiento explícito** (artículos 6.1.a y 9.2.a del RGPD).

Es la única base: ni la ejecución de un contrato ni el interés legítimo legitiman por sí solos una categoría especial de datos.

## Su consentimiento y su revocación

La comprobación es voluntaria. Usted puede revocar el consentimiento en cualquier momento escribiendo a privacy@earth-lings.org.

**Qué ocurre al revocarlo:**

- el tratamiento cesa y los hashes conservados se suprimen;
- dado que la unicidad acreditada es condición del derecho de voto, seguir participando en las votaciones se hace imposible;
- **el pasaporte lo destruye usted mismo**, con su propia clave, como en una salida voluntaria ordinaria.

> **No podemos destruir su pasaporte en su lugar.** La Carta (artículo 21) admite la destrucción contra la voluntad del titular solo en dos casos: la anulación de una emisión inválida por decisión de la Asamblea y la reemisión técnica a solicitud suya. La revocación del consentimiento no figura entre ellos, y la plataforma no guarda sus claves. Si usted revoca el consentimiento y no destruye el pasaporte, suprimiremos los datos por nuestra parte, pero el asiento del registro permanecerá hasta que usted lo destruya.

---

# SECCIÓN 03. Condiciones para obtener la condición de earthling

- **edad**: haber cumplido 18 años;
- **consentimiento**: aceptación voluntaria de la Declaración;
- **verificación de identidad**: confirmación de la unicidad;
- **pasaporte**: emisión de un token intransmisible en su dirección.

## Qué datos hacen falta

La lista completa y las bases jurídicas están en la Política de privacidad. Para la comprobación se requieren:

- **seudónimo**: a su elección, se emplea en el pasaporte y para entrar en la plataforma;
- **dirección de correo electrónico**: para el contacto;
- **comprobación del documento y del rostro**.

**El nombre y los apellidos reales no se conservan.** Los datos del documento se emplean solo en el momento de la comprobación - para cotejar el rostro con el documento y confirmar la unicidad - y tras concluir esta se suprimen. Su seudónimo sigue siendo su nombre público.

## Qué da la condición de earthling

- **pasaporte**: acreditación de la pertenencia al pueblo;
- **derecho de voto** en la Asamblea DAO: una persona, un voto;
- **acceso a la infraestructura**: participación en proyectos, servicios, coordinación;
- **derecho a presentar propuestas** y a participar en las decisiones sobre cualquier cuestión.

> **Qué no da esa condición.** El pasaporte no da nacionalidad ni residencia, ni derechos de visado, ni eficacia ante las instituciones estatales, y no sustituye a los documentos de su país. El pueblo Earthlings no tiene personalidad jurídica internacional y no puede representar los intereses de nadie ante los tribunales o ante los órganos del Estado. La lista completa está en los documentos [El camino del earthling](https://earth-lings.org/documents/es/es14-camino-del-earthling.html) y [Pasaporte SBT](https://earth-lings.org/documents/es/es15-pasaporte-sbt.html).

---

# SECCIÓN 04. Cómo funciona la comprobación

**Documento → rostro → comprobación de presencia viva → cotejo del documento y el rostro → resultado → conservación protegida del resultado**

## Qué se comprueba

- **el documento**: cotejo de los datos con un documento oficial acreditativo de la identidad;
- **la geometría del rostro**: puntos clave y proporciones;
- **la presencia viva**: protección frente a fotografías, grabaciones de vídeo y máscaras. La comprobación se construye según el modelo de detección de ataques de presentación descrito en la norma ISO/IEC 30107; el nivel de resistencia declarado y los resultados de la comprobación independiente se publican al entrar el sistema en explotación industrial.

## Procedimiento

1. **Recepción** de la imagen del documento y del rostro por una conexión protegida.
2. **Comprobación de presencia viva.**
3. **Extracción de rasgos**: datos del documento y puntos clave del rostro.
4. **Construcción de una plantilla matemática**: un conjunto de números que describe las características. La plantilla existe únicamente en la memoria durante la comprobación.
5. **Cotejo** de la biometría con el documento y comprobación de la unicidad.
6. **Conservación del resultado**, cifrado.

> **Qué queda tras la comprobación.** Las fotografías, los escaneos de los documentos y las plantillas biométricas **no se conservan**. Quedan: el estado de la comprobación (superada o no) y unos hashes criptográficos irreversibles calculados a partir del número del documento y de la combinación del nombre con el país.
>
> Los hashes no impiden volver. Solo impiden que una misma persona tenga dos pasaportes en vigor a la vez: al adherirse de nuevo, el sistema encuentra la coincidencia, comprueba que el pasaporte anterior está destruido y emite uno nuevo.

> **Con precisión, sobre la condición de los hashes.** Un hash es irreversible: de él no se puede leer ni el nombre ni el número del documento. Pero permite **distinguir a una persona concreta** entre otras; de lo contrario no cumpliría su tarea. Por eso, conforme al RGPD, son datos **seudonimizados y no anónimos**, y la protección de datos personales se les aplica en su totalidad. No los llamamos anonimizados porque sería inexacto.

---

# SECCIÓN 05. Protección de los datos

Las medidas generales están descritas en la Política de privacidad; a continuación, las específicas de la biometría.

**Transmisión protegida.** Todos los datos se transmiten por canales protegidos con cifrado de extremo a extremo entre su dispositivo y los servidores del sistema de comprobación.

**Cifrado en la conservación.** Los hashes se conservan cifrados (AES-256). Las claves de descifrado se conservan aparte de los datos.

**Separación de los almacenes.** Los hashes y los resultados de la comprobación se conservan aparte de los datos de la cuenta.

**Supresión inmediata de los materiales originales.** Las fotografías y los escaneos se suprimen en cuanto concluye la comprobación.

**Control de acceso.** Autenticación de varios niveles y registro: todos los accesos a los datos de la comprobación quedan registrados y pueden verificarse.

> **Filosofía de la seguridad:** la mejor protección es que no haya nada que robar. No conservamos aquello que pueda emplearse contra usted.

---

# SECCIÓN 06. Sus derechos

Los derechos generales del participante están en la Política de privacidad y en las Condiciones de uso. A continuación, los específicos de la biometría.

**Revocar el consentimiento**: en cualquier momento; el procedimiento y las consecuencias están descritos en la sección 02.

**Pasar la comprobación de nuevo.** Si su aspecto ha cambiado mucho y la comprobación no lo reconoce, usted la pasa de nuevo. La plantilla no se «actualiza» con ello: no se conserva en ninguna parte, y el cotejo se realiza cada vez desde cero.

**Exigir la revisión por una persona.** Una denegación automática no es definitiva (artículo 22 del RGPD). Usted puede exponer su posición e impugnar el resultado. Tras dos intentos automáticos fallidos, el asunto pasa a una persona **sin necesidad de solicitarlo**. El número de solicitudes reiteradas no está limitado.

**Presentar una reclamación** ante la autoridad de control de protección de datos de su país; el procedimiento está en la Política de privacidad.

## Qué ocurre al salir

- el vínculo entre los datos de la comprobación y su identidad se rompe;
- los hashes seudonimizados se conservan exclusivamente para que una misma persona no pueda tener dos pasaportes en vigor;
- **el derecho a volver se conserva**: al adherirse de nuevo, el sistema comprueba que el pasaporte anterior está destruido y emite uno nuevo;
- reconstruir una imagen a partir de los hashes o establecer una identidad es prácticamente imposible.

---

# SECCIÓN 07. Para qué se emplea la comprobación

La lista es exhaustiva: no se realiza tratamiento con otros fines.

- confirmación de la unicidad al registrarse;
- emisión del pasaporte;
- acreditación de la condición de participante;
- aseguramiento del principio «una persona, un voto» en las votaciones;
- acceso a los servicios que exigen una condición acreditada.

> **Qué no hacemos.** No seguimos la localización. No analizamos el comportamiento. No vendemos datos a terceros. No elaboramos perfiles para publicidad. No empleamos el sistema para vigilar. No entregamos datos a los órganos del Estado si no es por una resolución judicial firme o un requerimiento legal equivalente, cuya legitimidad se comprueba en cada caso.
>
> De los requerimientos atendidos se informa al participante, salvo que la propia resolución lo prohíba. Un resumen de tales casos se publica en el informe de transparencia.

---

# SECCIÓN 08. Transparencia y supervisión

## Qué es abierto y qué es cerrado

El código del contrato inteligente del pasaporte es abierto bajo licencia MIT y verificable en el explorador de la red.

**El código del sistema de verificación de identidad es cerrado**, precisamente porque trabaja con datos personales y su publicación facilitaría eludir la protección. Es una elección consciente y no un silencio; la lista con sus motivos está en el documento [Dónde estamos ahora](https://earth-lings.org/documents/es/es32-donde-estamos-ahora.html).

A cambio de esa opacidad asumimos lo siguiente:

- **auditoría independiente de seguridad**: prevista antes de ampliar las operaciones; el informe se publica;
- **documentación técnica**: accesible para su estudio;
- **informes de seguridad**: se publican con regularidad;
- **registro de los accesos** a los datos de comprobación: se lleva y está sujeto a auditoría.

## Supervisión independiente

Las cuestiones de ética en el tratamiento de datos biométricos se someten al [Consejo Independiente](https://earth-lings.org/documents/es/es11-consejo-independiente.html), órgano no subordinado a quienes operan la plataforma. Hasta que el Consejo se constituya, tales cuestiones las examina la Asamblea DAO, y los plazos de debate público se duplican (Carta, artículo 39).

Las propuestas de modificación de la presente Política se someten a votación de la Asamblea.

---

# SECCIÓN 09. Reparto de responsabilidades

## Sistema de verificación de identidad

- recepción y tratamiento de los datos del documento y del rostro;
- reconocimiento del documento con extracción de los datos de la zona de lectura mecánica;
- comprobación de presencia viva;
- cotejo de la fotografía con el documento;
- confirmación de la unicidad.

## Registro del pueblo

**Qué no se conserva:** nombres y apellidos reales; números de pasaporte y de documentos; fechas exactas de nacimiento; domicilios; fotografías y plantillas biométricas; números de teléfono, salvo en los casos de autenticación de dos factores.

**Qué se conserva:** el seudónimo; la dirección de correo electrónico; la confirmación de ser mayor de 18 años; el país de residencia (para estadística); el estado de la verificación de identidad; el vínculo con el pasaporte; la fecha de obtención de la condición.

## Minimización

El registro sigue el principio de minimización de datos conforme al RGPD. Se conserva únicamente lo necesario: la unicidad acreditada, el vínculo con el pasaporte para participar en las decisiones y un identificador interno para distribuir las remuneraciones.

Las fotografías y los escaneos se suprimen en cuanto concluye la comprobación, pero su resultado sigue siendo válido y verificable, del mismo modo que un Estado no conserva de manera permanente las muestras biométricas al expedir un pasaporte, aunque el hecho de la expedición siga siendo válido.

> **El vínculo entre la identidad real y el seudónimo no se conserva.** Los datos del documento se tratan solo en el momento de la comprobación. En el registro quedan el seudónimo, el estado de la comprobación y la confirmación criptográfica de la unicidad. Esa arquitectura excluye que se revele la identidad de un participante - a otros participantes, a los administradores y a terceros - porque no hay nada que revelar.

---

# SECCIÓN 10. Preguntas frecuentes

**¿Pueden reconstruir mi rostro a partir de lo que conservan?**
No. La plantilla biométrica no se conserva en absoluto: la comparación se realiza en el momento de la comprobación, tras lo cual los datos originales se suprimen. Quedan hashes irreversibles de los que no se puede obtener ni una imagen ni los datos del documento.

**¿Qué ocurre si pierdo el teléfono?**
Los datos de la comprobación están a salvo. Para recuperar el acceso basta con instalar la aplicación en un dispositivo nuevo y pasar la comprobación de nuevo.

**¿Pueden robar mi biometría?**
Solo se pueden robar hashes cifrados e irreversibles, inútiles sin las claves de descifrado. Reconstruir a partir de ellos una imagen del rostro es prácticamente imposible.

**¿Es obligatorio indicar el nombre verdadero?**
No. El nombre y los apellidos reales no se conservan. Los datos del documento se comprueban solo en el momento de la comprobación y después se suprimen. En la relación cotidiana se le conoce por su seudónimo.

**¿Qué ocurre con los datos al salir?**
El vínculo entre los datos de la comprobación y su identidad se rompe. Los hashes seudonimizados se conservan exclusivamente para que una misma persona no pueda tener dos pasaportes en vigor. Eso no impide volver.

**¿Qué hacer si mi aspecto ha cambiado mucho?**
Pasar la comprobación de nuevo. No existe una plantilla conservada que hubiera que actualizar.

**¿Y si la comprobación se rechaza?**
Recibirá un aviso con los motivos. Se puede repetir el intento tras subsanarlos, por ejemplo con imágenes de mejor calidad o con otro documento. Si no está de acuerdo, puede exigir la revisión por una persona, y tras dos intentos automáticos fallidos esa revisión se produce de manera automática.

**¿Quién puede ver mi nombre y mis apellidos reales?**
Nadie: no se conservan. El pueblo no puede técnicamente revelar datos de los que no dispone.

**¿Entregan datos a los Estados?**
Solo por una resolución judicial firme o un requerimiento legal equivalente; el procedimiento y el aviso al participante están descritos en la [Política de privacidad](https://earth-lings.org/documents/es/es28-politica-de-privacidad.html).

---

# SECCIÓN 11. Modificaciones de la Política

La Política se actualiza a medida que avanzan las tecnologías y la legislación. Las modificaciones se publican indicando la fecha de entrada en vigor.

El procedimiento de modificación - aviso con no menos de 30 días de antelación, publicación de la lista de cambios y derecho a objetar - está establecido en la Política de privacidad.

---

**Para cuestiones de verificación de identidad:** privacy@earth-lings.org
