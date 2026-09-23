# Política de verificación biométrica de los Earthlings

**En vigor desde el momento de su publicación**

> En caso de discrepancia de la presente Política con la [Carta](https://earth-lings.org/documents/es/es05-carta.html) se aplica la Carta, y en caso de discrepancia de la Carta con la [Declaración](https://earth-lings.org/documents/es/es01-declaracion.html), la Declaración. Las reglas generales de tratamiento de datos personales están en la [Política de privacidad](https://earth-lings.org/documents/es/es28-politica-de-privacidad.html). En el período constituyente - desde el 22 de octubre de 2026 hasta la adopción de la Declaración - la firma de la Declaración y la adhesión al pueblo están suspendidas: un pueblo definido por un texto adoptado todavía no existe. La verificación de identidad en ese período se realiza gratuitamente y, como resultado, se entrega un documento temporal de participante en la constitución, y no un pasaporte (documento «El período constituyente», parte 2, apartado 5). El documento temporal se emite en el mismo contrato que el pasaporte (documento «Dónde estamos ahora»). La presente Política se aplica también a esa verificación; lo que en ella se dice sobre la firma y sobre el pasaporte se refiere al régimen principal posterior a la adopción de la Declaración.

## Lo esencial, en breve

- la biometría se trata en el momento de la comprobación y no se conserva;
- para que una misma persona no pueda tener dos pasaportes en vigor, se conservan hashes criptográficos irreversibles;
- se puede volver tras la salida en cualquier momento;
- el nombre y los apellidos, tal como figuran en el documento, hacen falta para cotejarlos con él; los demás participantes le ven a usted bajo el seudónimo que haya elegido;
- la biometría sirve a la confianza, no al control;
- sistema propio de comprobación, minimización de datos.

---

# SECCIÓN 01. Principios

## Para qué la biometría

Sirve a un solo fin: acreditar que detrás de cada voto hay una sola persona viva y única. Es la base de la confianza entre desconocidos, y nada más. El sistema está diseñado para conservar lo menos posible.

## La persona, no los documentos

La persona importa más que los documentos. Su pertenencia al pueblo la determina su libre elección, y no un pasaporte o una nacionalidad. La tarea de la comprobación no es un reconocimiento desde fuera, sino la confirmación de un hecho simple: usted es usted, y es uno solo.

## Cuatro principios

**1. Confirmación de la unicidad, no control.** La comprobación protege al pueblo frente a las inscripciones múltiples de una misma persona y no se emplea para vigilar.

**2. La pertenencia se acredita personalmente.** Los documentos estatales siguen en su lugar: la comprobación se limita a cotejar la identidad, sin sustituir nada.

**3. Confianza mediante la comprobación.** En una comunidad sin poder central, una unicidad acreditada crea una capa básica de confianza. Eso no garantiza la buena fe en un trato concreto, pero elimina la multiplicidad anónima de cuentas como fuente de manipulaciones.

**4. Protección frente a los abusos.** La renuncia a conservar imágenes y plantillas, los hashes calculados con la clave secreta del servidor y la imposibilidad práctica de reconstruir una imagen a partir de los datos conservados tienen por finalidad impedir que el sistema pueda emplearse para una vigilancia masiva.

---

# SECCIÓN 02. Ámbito de aplicación y consentimiento

La presente Política regula el tratamiento de los datos biométricos que se realiza con ocasión de la firma de la Declaración, de la obtención de la condición de earthling y de la participación en la infraestructura del pueblo y, en el período constituyente, de la verificación de identidad para el documento temporal de participante en la constitución.

## Base jurídica

Los datos biométricos pertenecen a la categoría especial de datos personales conforme al artículo 9 del RGPD y se tratan **exclusivamente sobre la base de su consentimiento explícito** (artículos 6.1.a y 9.2.a del RGPD).

Es la única base: ni la ejecución de un contrato ni el interés legítimo legitiman por sí solos una categoría especial de datos.

## Su consentimiento y su revocación

La comprobación es voluntaria. Usted puede revocar el consentimiento en cualquier momento escribiendo a privacy@earth-lings.org.

**Qué ocurre al revocarlo:**

- el tratamiento de los datos biométricos cesa (tras la comprobación tampoco se conservan); el resultado de la comprobación (sección 04) se conserva: no es un dato biométrico;
- **el hash irreversible de unicidad también se conserva.** Está calculado a partir de los datos del documento y no de la biometría, por lo que no queda comprendido en el consentimiento del artículo 9 del RGPD y se conserva por otro fundamento. Sin él, una misma persona podría obtener un segundo pasaporte con los mismos datos del documento: el hash permite detectar ese intento, incluso cuando provenga de usted mismo, y un pasaporte emitido eludiendo la comprobación se anula (Declaración, artículo 8);
- la revocación del consentimiento no afecta a la pertenencia ni al derecho de voto, y la cuenta de usuario tampoco se suprime por esa revocación; para quien pertenece al pueblo, la supresión de la cuenta de usuario solo va unida a la salida;
- **el pasaporte lo destruye usted mismo**, con su propia clave, si decide salir: la revocación del consentimiento no destruye el pasaporte.

> **No tenemos derecho a destruir su pasaporte en su lugar.** La Carta (artículo 21) admite la destrucción del pasaporte por persona distinta de su titular solo en dos casos: la anulación de una emisión inválida por decisión de la Asamblea y la reemisión técnica a solicitud suya; contra su voluntad el pasaporte solo puede destruirse en el primero de ellos. La revocación del consentimiento no figura entre esos casos, y la plataforma no guarda sus claves; pero, mientras los derechos del propietario del contrato no se hayan traspasado a una firma múltiple, la emisión y la destrucción del pasaporte están técnicamente al alcance de una sola clave (documento «Dónde estamos ahora»). El asiento del registro permanece tras la revocación del consentimiento. Hasta la adopción de la Declaración no hay Asamblea (Carta, artículo 38), y el documento temporal de participante en la constitución se destruye contra la voluntad de su titular en la forma prevista en el documento «El período constituyente» (parte 2, apartado 5).

---

# SECCIÓN 03. Condiciones para obtener la condición de earthling

- **edad**: haber cumplido 18 años;
- **consentimiento**: firma voluntaria de la Declaración;
- **verificación de identidad**: confirmación de la unicidad;
- **pasaporte**: emisión de un token intransmisible a su dirección; el pasaporte acredita la condición que nace al firmar la Declaración.

## Qué datos hacen falta

La lista completa y las bases jurídicas están en la Política de privacidad. Para la comprobación se requieren:

- **seudónimo**: a su elección, se emplea en el pasaporte y para entrar en la plataforma;
- **dirección de correo electrónico**: para el contacto;
- **comprobación del documento y del rostro**, junto con el nombre y los apellidos en alfabeto latino tal como figuran en el documento; además, se indica el país de residencia y se confirma la edad de 18 años o más.

**El nombre y los apellidos reales no se conservan.** Los datos del documento se emplean solo en el momento de la comprobación, para cotejar el rostro con el documento y confirmar la unicidad; tras concluir esta, de ellos solo quedan el tipo y el país de expedición del documento y unos hashes irreversibles. Su seudónimo sigue siendo el nombre bajo el que le ven los demás participantes.

## Qué da la condición de earthling

- **pasaporte**: acreditación de la pertenencia al pueblo;
- **derecho de voto** en la Asamblea DAO: una persona, un voto;
- **acceso a la infraestructura**: participación en proyectos, servicios, coordinación;
- **derecho a presentar propuestas** y a participar en las decisiones sobre cualquier cuestión.

> **Qué no da esa condición.** El pasaporte no da nacionalidad ni residencia, ni derechos de visado, ni eficacia ante las instituciones estatales, y no sustituye a los documentos de su país. El pueblo Earthlings no tiene personalidad jurídica internacional y no puede representar los intereses de nadie ante los tribunales o ante los órganos del Estado. La lista completa está en los documentos [El camino del earthling](https://earth-lings.org/documents/es/es14-camino-del-earthling.html) y [Pasaporte SBT](https://earth-lings.org/documents/es/es15-pasaporte-sbt.html).

---

# SECCIÓN 04. Cómo funciona la comprobación

**Documento → rostro → comprobación de presencia viva → cotejo del documento y el rostro → resultado → conservación del resultado**

## Qué se comprueba

- **el documento**: cotejo de los datos con un documento oficial acreditativo de la identidad;
- **la geometría del rostro**: puntos clave y proporciones;
- **la presencia viva**: por ahora es una comprobación pasiva básica sobre una sola imagen del rostro: está concebida para detectar falsificaciones simples - la captura de una fotografía impresa o de la imagen de una pantalla -; no protege frente a grabaciones de vídeo ni frente a máscaras, y la imagen se puede subir como archivo. La comprobación según el modelo de detección de ataques de presentación descrito en la norma ISO/IEC 30107 todavía no está implantada; el nivel de resistencia declarado y los resultados de la comprobación independiente se publicarán cuando se implante.

## Procedimiento

1. **Recepción** de la imagen del documento y del rostro por una conexión protegida.
2. **Comprobación de presencia viva.**
3. **Extracción de rasgos**: datos del documento y puntos clave del rostro.
4. **Construcción de una plantilla matemática**: un conjunto de números que describe las características. La plantilla existe únicamente en la memoria durante la comprobación.
5. **Cotejo** de la biometría con el documento y comprobación de la unicidad.
6. **Conservación del resultado**, sin imágenes ni plantillas.

> **Qué queda tras la comprobación.** Las fotografías, los escaneos de los documentos y las plantillas biométricas **no se conservan**. Quedan: el estado de la comprobación, el tipo y el país de expedición del documento, las puntuaciones numéricas de la comprobación, los motivos de denegación y hashes irreversibles, calculados con la clave secreta del servidor, del número del documento, del nombre, de los apellidos y de la fecha de nacimiento que figuran en el documento.
>
> Los hashes no impiden volver. Solo impiden que una misma persona tenga dos pasaportes en vigor a la vez: al adherirse de nuevo, el sistema encuentra la coincidencia, comprueba que el pasaporte anterior está destruido y emite uno nuevo.

> **Con precisión, sobre la condición de los hashes.** Un hash es irreversible y se calcula con la clave secreta del servidor: de él no se puede leer ni el nombre ni el número del documento y, sin la clave, tampoco se pueden obtener por fuerza bruta. Pero permite **distinguir a una persona concreta** entre otras; de lo contrario no cumpliría su tarea. Por eso, conforme al RGPD, son datos **seudonimizados y no anónimos**, y la protección de datos personales se les aplica en su totalidad. No los llamamos anonimizados porque sería inexacto.

---

# SECCIÓN 05. Protección de los datos

Las medidas generales están descritas en la Política de privacidad; a continuación, las específicas de la biometría.

**Transmisión protegida.** Todos los datos se transmiten por canales protegidos con cifrado de extremo a extremo entre su dispositivo y los servidores del sistema de comprobación.

**La clave de los hashes.** Los hashes se calculan con la clave secreta del servidor (HMAC-SHA256); la clave se conserva fuera de la base de datos. En el nivel de la aplicación no se cifran los datos conservados.

**Un solo almacén.** Los hashes y los resultados de la comprobación se conservan en la misma base que los datos de la cuenta de usuario; los datos de la plataforma están en una base aparte.

**Supresión inmediata de los materiales originales.** Las fotografías y los escaneos se suprimen en cuanto concluye la comprobación.

**Control de acceso.** Solo los administradores tienen acceso a los datos de la comprobación, mediante la clave de administrador; todavía no hay autenticación de varios niveles, y no se registran todos los accesos.

> **Filosofía de la seguridad:** cuanto menos se conserva, menos se puede robar. No conservamos imágenes, plantillas biométricas, el nombre ni el número del documento; lo que se conserva está enumerado en la sección 09 y en la Política de privacidad.

---

# SECCIÓN 06. Sus derechos

Los derechos generales del participante están en la Política de privacidad y en las Condiciones de uso. A continuación, los específicos de la biometría.

**Revocar el consentimiento**: en cualquier momento; el procedimiento y las consecuencias están descritos en la sección 02.

**Pasar la comprobación de nuevo.** Si su aspecto ha cambiado mucho y la comprobación no lo reconoce, usted la pasa de nuevo. La plantilla no se «actualiza» con ello: no se conserva en ninguna parte, y el cotejo se realiza cada vez desde cero.

**Exigir la revisión por una persona.** Una denegación automática no es definitiva (artículo 22 del RGPD). Usted puede exponer su posición e impugnar el resultado. Tras dos intentos automáticos fallidos, la revisión por una persona se realiza **sin necesidad de solicitarla**. El número de solicitudes reiteradas no está limitado.

**Presentar una reclamación** ante la autoridad de control de protección de datos de su país; el procedimiento está en la Política de privacidad.

## Qué ocurre al salir

- la destrucción del pasaporte no suprime por sí sola los datos: los datos de la cuenta de usuario se suprimen a petición suya y, tras la supresión, quedan la dirección del monedero, el número del asiento del pasaporte, el seudónimo, el país, el resultado y las puntuaciones de la comprobación y los hashes irreversibles;
- los hashes seudonimizados se conservan exclusivamente para que una misma persona no pueda tener dos pasaportes en vigor;
- **el derecho a volver se conserva**: al adherirse de nuevo, el sistema comprueba que el pasaporte anterior está destruido y emite uno nuevo;
- a partir de los hashes no se puede reconstruir una imagen; de ellos no se puede leer ni el nombre ni el número del documento y, sin la clave secreta del servidor, tampoco se pueden obtener por fuerza bruta.

---

# SECCIÓN 07. Para qué se emplea la comprobación

La lista es exhaustiva: no se realiza tratamiento con otros fines.

- confirmación de la unicidad al registrarse;
- emisión del pasaporte y, en el período constituyente, del documento temporal de participante en la constitución;
- acreditación de la condición de participante;
- aseguramiento del principio «una persona, un voto» en las votaciones;
- acceso a los servicios que exigen una condición acreditada.

> **Qué no hacemos.** No seguimos la localización. No analizamos el comportamiento, salvo en la estadística agregada de visitas, en la que se cuentan también los pasos del formulario de comprobación (Política de privacidad, sección 04). No vendemos datos a terceros. No elaboramos perfiles para publicidad. No empleamos el sistema para vigilar. No entregamos datos a los órganos del Estado si no es por una resolución judicial firme o un requerimiento legal equivalente, cuya legitimidad se comprueba en cada caso.
>
> De los requerimientos atendidos se informa al participante, salvo que la propia resolución lo prohíba. Un resumen de tales casos se publica en el informe de transparencia.

---

# SECCIÓN 08. Transparencia y supervisión

## Qué es abierto y qué es cerrado

El código del contrato inteligente del pasaporte es abierto bajo licencia MIT; en el explorador de la red el contrato no está verificado, y la correspondencia entre el código fuente y el contrato desplegado hay que comprobarla por cuenta propia (documento «Dónde estamos ahora»).

**El código del sistema de verificación de identidad es cerrado**, precisamente porque trabaja con datos personales y su publicación facilitaría eludir la protección. Es una elección consciente y no un silencio; la lista con sus motivos está en el documento [Dónde estamos ahora](https://earth-lings.org/documents/es/es32-donde-estamos-ahora.html).

A cambio de esa opacidad asumimos lo siguiente:

- **auditoría independiente de seguridad**: prevista antes de ampliar las operaciones; el informe se publica;
- **documentación técnica**: accesible para su estudio;
- **informes de seguridad**: se publican con regularidad;
- **registro de los accesos** a los datos de comprobación: está sujeto a auditoría; por ahora no se registran todos los accesos.

## Supervisión independiente

Las cuestiones de ética en el tratamiento de datos biométricos se someten al [Consejo Independiente](https://earth-lings.org/documents/es/es11-consejo-independiente.html), órgano no subordinado a quienes operan la plataforma. Tras la adopción de la Declaración, mientras el Consejo no esté constituido, esta fase se omite y los plazos de debate público de tales cuestiones se duplican (Carta, artículo 39); hasta la adopción de la Declaración no hay Consejo (Carta, artículo 38).

Tras la adopción de la Declaración, las propuestas de modificación de la presente Política se someten a votación de la Asamblea y, antes de la adopción de la Declaración, decide sobre ellas el autor de la Declaración en la forma prevista en el documento «El período constituyente» (parte 2, apartado 2).

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

**Qué se conserva:** el seudónimo; la dirección de correo electrónico; la confirmación de ser mayor de 18 años; el país de residencia (para estadística); el estado de la verificación de identidad; el vínculo con el pasaporte; la fecha de obtención de la condición; la dirección del monedero; la dirección IP y el tipo de navegador en el momento de la comprobación, durante no más de 12 meses.

## Minimización

El registro sigue el principio de minimización de datos conforme al RGPD. Se conserva únicamente lo necesario para confirmar la unicidad y para el vínculo con el pasaporte que permite participar en las decisiones; lo que se conserva exactamente se detalla más arriba, en el recuadro siguiente y en la Política de privacidad.

Las fotografías y los escaneos se suprimen en cuanto concluye la comprobación, pero su resultado sigue siendo válido y verificable.

> **El nombre y los apellidos reales no se conservan.** Los datos del documento se tratan solo en el momento de la comprobación. En el sistema de verificación de identidad quedan el seudónimo, la dirección de correo, el país, la dirección del monedero, la dirección IP y el tipo de navegador en el momento de la comprobación y, de la comprobación, el estado de la comprobación, el tipo y el país de expedición del documento, las puntuaciones numéricas de la comprobación, los motivos de denegación y hashes irreversibles, calculados con la clave secreta del servidor, del número del documento, del nombre, de los apellidos y de la fecha de nacimiento que figuran en el documento; el seudónimo no se inscribe en el registro abierto. Por eso su nombre o el número de su documento no se pueden revelar ni a otros participantes, ni a los administradores, ni a terceros: no los tenemos.

---

# SECCIÓN 10. Preguntas frecuentes

**¿Pueden reconstruir mi rostro a partir de lo que conservan?**
No. La plantilla biométrica no se conserva en absoluto: la comparación se realiza en el momento de la comprobación, tras lo cual los datos originales se suprimen. Quedan el resultado de la comprobación y unos hashes irreversibles de los que no se puede obtener una imagen; de ellos no se puede leer ni el nombre ni el número del documento y, sin la clave secreta del servidor, tampoco se pueden obtener por fuerza bruta.

**¿Qué ocurre si pierdo el teléfono?**
Los datos de la comprobación están a salvo. No hay aplicación: la comprobación se pasa en el navegador. Si el monedero se creó entrando con el correo, con Google o con Apple, basta con entrar del mismo modo en el dispositivo nuevo. Si se pierde el acceso al monedero, el pasaporte se reemite a una dirección nueva a solicitud suya, y la pertenencia no se interrumpe (Carta, artículo 21).

**¿Pueden robar mi biometría?**
La biometría no se puede robar: no la conservamos. Los hashes que conservamos están calculados con la clave secreta del servidor a partir de los datos del documento, y no de la biometría, y no contienen imagen alguna del rostro.

**¿Es obligatorio indicar el nombre verdadero?**
Para la comprobación, sí: el nombre y los apellidos, tal como figuran en el documento, hacen falta para cotejarlos con él. El nombre y los apellidos reales no se conservan. Los datos del documento se comprueban solo en el momento de la comprobación; después de ella, de ellos solo quedan el tipo y el país de expedición del documento y unos hashes irreversibles. En la relación cotidiana se le conoce por su seudónimo.

**¿Qué ocurre con los datos al salir?**
La destrucción del pasaporte no suprime por sí sola los datos: los datos de la cuenta de usuario se suprimen a petición suya y, tras la supresión, quedan la dirección del monedero, el número del asiento del pasaporte, el seudónimo, el país, el resultado y las puntuaciones de la comprobación y los hashes irreversibles. Los hashes seudonimizados se conservan exclusivamente para que una misma persona no pueda tener dos pasaportes en vigor. Eso no impide volver.

**¿Qué hacer si mi aspecto ha cambiado mucho?**
Pasar la comprobación de nuevo. No existe una plantilla conservada que hubiera que actualizar.

**¿Y si la comprobación se rechaza?**
Los motivos de la denegación automática se muestran en la pantalla de comprobación, por ahora con códigos de servicio, y la decisión posterior a la revisión por una persona llega por correo. Se puede repetir el intento una vez subsanados los defectos señalados, por ejemplo con imágenes de mejor calidad o con otro documento. Si no está de acuerdo, puede exigir la revisión por una persona y, tras dos intentos automáticos fallidos, la revisión por una persona se realiza sin necesidad de solicitarla.

**¿Quién puede ver mi nombre y mis apellidos reales?**
Nadie: no se conservan. El pueblo no puede técnicamente revelar datos de los que no dispone.

**¿Entregan datos a los Estados?**
Solo por una resolución judicial firme o un requerimiento legal equivalente; el procedimiento y el aviso al participante están descritos en la [Política de privacidad](https://earth-lings.org/documents/es/es28-politica-de-privacidad.html).

---

# SECCIÓN 11. Modificaciones de la Política

La Política se actualiza a medida que avanzan las tecnologías y la legislación. Las modificaciones se publican indicando la fecha de entrada en vigor.

El procedimiento de modificación - aviso por correo electrónico con no menos de 30 días de antelación, aviso en la plataforma en el siguiente acceso, publicación de la lista de cambios y derecho a objetar - está establecido en la Política de privacidad.

---

**Para cuestiones de verificación de identidad:** privacy@earth-lings.org
