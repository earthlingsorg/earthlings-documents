# Pasaporte SBT earthling

**Acreditación digital de la pertenencia al pueblo Earthlings**

> El presente documento describe la arquitectura y el significado jurídico del pasaporte. En caso de discrepancia se aplica la [Carta](https://earth-lings.org/documents/es/es05-carta.html), y en caso de discrepancia de la Carta con la [Declaración](https://earth-lings.org/documents/es/es01-declaracion.html), la Declaración. El procedimiento de adhesión está descrito en el documento [El camino del earthling](https://earth-lings.org/documents/es/es14-camino-del-earthling.html). En el período constituyente - desde el 22 de octubre de 2026 hasta la adopción de la Declaración - la firma de la Declaración y la adhesión al pueblo están suspendidas: un pueblo definido por un texto adoptado todavía no existe. La verificación de identidad en ese período se realiza gratuitamente y, como resultado, se entrega un documento temporal de participante en la constitución, y no un pasaporte (documento «El período constituyente», parte 2, apartado 5). El documento temporal se emite en el mismo contrato que el pasaporte (documento «Dónde estamos ahora»), pero no documenta la firma de la Declaración. Más abajo se describe el régimen principal, que comenzará tras la adopción de la Declaración.

---

## Qué es

El pasaporte SBT earthling es un token digital intransmisible (Soulbound Token) que se expide a cada participante tras verificar su identidad, firmar la Declaración y abonar la cuota. Acredita criptográficamente la pertenencia al pueblo y se conserva en un registro distribuido como asiento único que no se puede alterar sin que se advierta.

A diferencia de los pasaportes estatales, ligados a un territorio y acreditativos de la nacionalidad, este pasaporte acredita la pertenencia a un pueblo unido por valores comunes. No puede cederse a otra persona, ni venderse, ni enajenarse.

**Intransmisibilidad.** El pasaporte está ligado a su monedero, y la cesión está bloqueada en el propio contrato, y no por una regla que se pueda eludir. La unicidad de la identidad está verificada en la emisión.

**Protección criptográfica.** El asiento se conserva en una red distribuida, y no se puede alterar sin que se advierta.

**Igualdad.** Todos reciben el mismo pasaporte con los mismos derechos. No existen clases privilegiadas ni niveles de pertenencia. Una persona, un pasaporte, un voto; el voto nace al firmar la Declaración, y el pasaporte lo acredita.

---

## Qué da el pasaporte

### Participación en el gobierno

- acreditación del derecho de voto en la Asamblea DAO;
- presentación de propuestas e iniciativas;
- participación en las decisiones sobre cualquier cuestión.

> **El voto es inalienable** y no puede retirarse ni suspenderse por las opiniones, por el sentido del voto, por el desacuerdo con las decisiones o como medida general de responsabilidad (Declaración, artículo 4; [Carta, artículos 17 y 37](https://earth-lings.org/documents/es/es05-carta.html)). El voto es el contenido de la pertenencia: al retirarlo por tales fundamentos, el pueblo estaría expulsando a la persona dejándole solo el nombre.

La única excepción son los actos probados dirigidos a socavar la integridad de la votación misma: concierto, compra o venta de un voto, coacción a otros, elusión de la regla «una persona, un pasaporte» (Carta, artículo 22 bis). Las opiniones, el sentido del voto y el desacuerdo con las decisiones no son fundamento, sea cual sea su presentación.

### Identificación digital

- acreditación públicamente verificable de la condición de participante;
- acceso a los servicios del ecosistema;
- posibilidad de emplearlo en aplicaciones descentralizadas que admitan este estándar.

### Acceso al ecosistema

- la plataforma digital del pueblo;
- participación en células y en proyectos conjuntos;
- recursos educativos;
- relación con otros participantes.

### Marcas de participación

El historial de participación y de aportación es visible para los participantes en la plataforma: proyectos concluidos, trabajo en las células. La participación en las votaciones no se publica: el voto personal es secreto (Carta, artículo 6).

> **Esas marcas no influyen en nada** y tienen carácter exclusivamente informativo: [Carta, artículo 8](https://earth-lings.org/documents/es/es05-carta.html).

---

## Cómo obtenerlo

**1. Verificación de identidad.** Comprobación de que usted es una persona viva y de que es una sola. Asegura el principio «una persona, un voto». Las imágenes originales y los escaneos de los documentos no se conservan.

**2. Firma de la Declaración.** Estudio de los documentos, comprensión de los principios, confirmación del acuerdo con una firma digital. Es ese acto el que crea la pertenencia.

**3. Abono de la cuota.** El equivalente a 79 USD, en criptomoneda (ETH, USDT, USDC). El destino de la cuota y el procedimiento de su gasto están en el documento [Tesorería](https://earth-lings.org/documents/es/es09-tesoreria.html).

> Quien no pueda abonar la cuota por sí mismo podrá, cuando la entrada sea de pago, entrar en una cola abierta, y su cuota podrá abonarla otra persona o la Tesorería; no hay garantía de ello. El pasaporte no se diferencia en nada de los demás: en el registro no consta quién abonó la cuota. La cuota no compra la pertenencia: esta nace al firmar la Declaración.

**4. Emisión del pasaporte.** El token se crea de manera automática y se liga a su monedero.

---

## Base técnica

### Infraestructura

- red: Polygon Mainnet, compatible con EVM;
- estándar: ERC-721, intransmisible (soulbound);
- dirección del contrato de los pasaportes: `0x20e7962878429B803E35F83ba34eD291afEC2Be4`;
- las transacciones son públicas y verificables en el explorador de la red sin intervención nuestra;
- el código fuente del contrato es abierto (licencia MIT).

### Seguridad del contrato

- base: bibliotecas contrastadas de OpenZeppelin;
- regla: un pasaporte por monedero; la cesión está bloqueada en el propio contrato;
- está prevista una auditoría independiente antes de ampliar las operaciones.

### Conservación de los datos

- **en el registro:** la dirección del monedero, el número del asiento del pasaporte, el identificador del participante por el que el asiento queda vinculado a los datos del sistema de verificación de identidad, y la hora de la emisión; en el campo del seudónimo se inscribe en la emisión una sola palabra, «Earthling», y en el campo del hash de la verificación, un valor aleatorio no relacionado con los datos de la verificación. El nombre, el documento, la biometría y los hashes de la verificación no se inscriben en el registro;
- **fuera del registro:** los datos personales de la cuenta, en el volumen mínimo;
- **biometría:** no se conserva. De la comprobación quedan el estado de la comprobación, el tipo y el país de expedición del documento, las puntuaciones numéricas de la comprobación, los motivos de denegación y hashes irreversibles, calculados con la clave secreta del servidor, del número del documento, del nombre, de los apellidos y de la fecha de nacimiento que figuran en el documento. Los hashes están calculados a partir de los datos del documento, y no de la biometría, y se conservan solo para que una misma persona no pueda tener dos pasaportes en vigor;
- se diseña conforme a los principios del RGPD.

### Criptografía

- firmas: ECDSA secp256k1;
- hash: Keccak-256.

Un estándar único de pasaporte para todos los participantes permite concentrar los recursos en la fiabilidad de un solo sistema y asegura una protección igual a cada cual.

---

## Significado jurídico

El pasaporte es una acreditación digital de la pertenencia al pueblo Earthlings.

### Qué no da el pasaporte

Esto importa entenderlo antes de adherirse, y no después.

- **no da nacionalidad ni residencia** de ningún país;
- **no proporciona ventajas de visado** ni derechos de entrada;
- **no tiene eficacia jurídica** ante las instituciones estatales de ningún país;
- **no sustituye a los documentos** acreditativos de la identidad;
- **no exime** de cumplir las leyes del país de residencia;
- **no crea derechos en el derecho internacional.**

El pasaporte documenta lo que documenta, y no es poco: una persona concreta ha sido verificada como viva y única y ha firmado la Declaración. Dentro del pueblo de ahí se sigue todo: voto igual, participación en las decisiones, pertenencia inalienable. Qué significa ese conjunto para el derecho internacional es objeto de un examen aparte en los documentos [Base jurídica](https://earth-lings.org/documents/es/es04-base-juridica.html) y [Objeciones jurídicas](https://earth-lings.org/documents/es/es26-objeciones-y-respuestas.html), donde se recogen también los argumentos en contra.

### Protección de datos

- derecho a la rectificación y a la supresión de los datos tratados por la plataforma;
- los asientos del registro distribuido, por definición técnica, no se suprimen, y precisamente por eso el nombre, el documento, la biometría y los hashes de la verificación no se inscriben en el registro en el momento de la emisión. En la emisión se inscriben en el registro la dirección del monedero, el número del asiento del pasaporte, el identificador del participante por el que el asiento queda vinculado a los datos del sistema de verificación de identidad, y la hora de la emisión; la emisión y la destrucción dejan marcas en el registro. Son datos seudónimos que nosotros tenemos vinculados a su cuenta de usuario;
- minimización del tratamiento; cifrado en la transmisión;
- las fotografías y los escaneos no se conservan.

### Responsabilidad y controversias

- DAO Earthlings no es una persona jurídica inscrita;
- los participantes responden individualmente del cumplimiento de las leyes de sus países;
- las controversias internas se resuelven en la forma establecida en el documento «Ética de los Earthlings»: diálogo directo, mediación con el consentimiento de ambas partes y, si no ha servido o si la otra parte no ha consentido en ella, examen por la Asamblea; ante una amenaza para la vida y la seguridad, una infracción manifiesta de la Declaración o un delito, la persona acude de inmediato a la Asamblea, sin pasar por el diálogo ni por la mediación. El pueblo no suplanta a los tribunales ni a los mecanismos jurídicos estatales y no ofrece arbitraje fuera de su ecosistema.

---

## Extinción del pasaporte

**Por regla general el pasaporte solo lo destruye usted mismo**, con su propia clave y desde su propio monedero (función `burnByHolder`). La plataforma no guarda sus claves y no puede impedir la destrucción; nadie tiene derecho a destruir el pasaporte en su lugar pero, mientras los derechos del propietario del contrato no se hayan traspasado a una firma múltiple, la emisión y la destrucción del pasaporte están técnicamente al alcance de una sola clave (documento «Dónde estamos ahora»).

La Carta (artículo 21) establece **dos y solo dos** excepciones, y esa lista no puede ampliarse.

> **Sobre el fallecimiento del titular.** La pertenencia cesa por el fallecimiento de la persona, pero el pasaporte no se destruye por ello. El pueblo no tiene acceso a los registros de defunción de todo el mundo, de modo que tal fundamento se apoyaría en datos no verificables y se convertiría en el modo más barato de retirar a un participante. El pasaporte permanece en el registro; la participación que ya no existe la recoge el mecanismo de inactividad (Carta, artículo 20). El pasaporte no se transmite por sucesión ni se cede en ninguna circunstancia.

### 1. Anulación de una emisión inválida

Se aplica si se establece que el pasaporte se emitió infringiendo las condiciones de emisión: se emitió a una misma persona más de un pasaporte en vigor, o la comprobación se pasó con datos falsos o con la identidad de otra persona, o el pasaporte se emitió a quien no había alcanzado la edad establecida en la Carta.

**No es una medida de responsabilidad ni una expulsión del pueblo.** Solo se establece que la emisión no llegó a producirse válidamente. No se sigue una reemisión automática: si se ha removido el impedimento a una emisión válida, la persona puede pasar la comprobación de nuevo en las condiciones generales.

**El procedimiento** es una decisión de la Asamblea, y no un acto del operador:

- escrito motivado con pruebas;
- notificación al titular y **no menos de 21 días** para objetar; el titular puede recabar el apoyo de otros participantes;
- dictamen del Consejo Independiente;
- votación de la Asamblea: **75 por ciento con quórum del 25, secreta y sin delegación**;
- **recurso en el plazo de 30 días**, y para anular la decisión basta la mayoría simple.

Las facultades del operador se limitan a ejecutar una decisión ya adoptada por la Asamblea. El operador no tiene derecho a anular por sí mismo la emisión de un pasaporte.

### 2. Reemisión técnica

A **solicitud del propio titular** en caso de pérdida de acceso al monedero o de migración del contrato. El pasaporte se destruye y se emite de nuevo de inmediato en la misma dirección o en una nueva. **La pertenencia no se interrumpe** y no hace falta votación.

### Principio de inalienabilidad

Nadie puede ser privado por la fuerza de la pertenencia al pueblo. No existe procedimiento de expulsión.

Al aplicarse medidas por infracciones graves de las reglas comunes, el pasaporte se conserva y **el derecho de voto se conserva íntegramente**. Sobre la persona recae una sola medida, la advertencia, y no le quita nada, ni el voto, ni el derecho a presentar propuestas, ni el derecho a crear células y a entrar en ellas, ni el acceso a los servicios, ni otra cosa alguna. Las demás medidas recaen sobre un proyecto o una célula y no afectan a los derechos de la persona; se adoptan por el procedimiento del artículo 22 de la Carta, con derecho de defensa, voto secreto y recurso.

### Qué ocurre técnicamente

- al salir, el titular destruye el pasaporte con la función `burnByHolder`, y en la anulación y en la reemisión técnica la destrucción la ejecuta el propietario del contrato con la función `burn`;
- los datos del pasaporte se suprimen del registro vigente del contrato;
- en el historial inmutable queda una marca seudónima de que el pasaporte existió y fue destruido: es un hecho del pasado, y no una pertenencia continuada;
- el nombre, el documento, la biometría y los hashes de la verificación no se inscriben en el registro en el momento de la emisión;
- para adherirse de nuevo se pasa el procedimiento completo y se emite un pasaporte nuevo.

---

## Sobre la financiación

Hasta ahora el proyecto se ha financiado con los fondos personales del autor de la Declaración (documento «Quiénes somos»): no se ha captado financiación externa.

La Carta y el documento [Tesorería](https://earth-lings.org/documents/es/es09-tesoreria.html) prevén la posibilidad de aceptar subvenciones y donaciones de organizaciones externas, con publicación de la fuente (y, si el donante ha querido permanecer anónimo, del hecho de la recepción y de la cuantía), sin condiciones contrarias a los principios del pueblo y con una prohibición expresa: el donante no obtiene ni voto ni influencia sobre las decisiones. La cuantía de la donación no otorga derecho ni ventaja alguna.

Tras la adopción de la Declaración, las decisiones de gasto se adoptan por votación de la Asamblea DAO y se publican y, mientras el monedero de la caja no tenga firma múltiple, su única clave está en manos del autor de la Declaración (documento «Tesorería»); las áreas de gasto y sus proporciones se establecen en el artículo 9 del documento [Tesorería](https://earth-lings.org/documents/es/es09-tesoreria.html).
