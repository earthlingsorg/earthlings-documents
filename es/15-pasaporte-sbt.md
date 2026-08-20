# Pasaporte SBT earthling

**Acreditación digital de la pertenencia al pueblo Earthlings**

> El presente documento describe la arquitectura y el significado jurídico del pasaporte. En caso de discrepancia se aplica la [Carta](https://earth-lings.org/documents/es/es05-carta.html), y en caso de discrepancia de la Carta con la [Declaración](https://earth-lings.org/documents/es/es01-declaracion.html), la Declaración. El procedimiento de adhesión está descrito en el documento [El camino del earthling](https://earth-lings.org/documents/es/es14-camino-del-earthling.html).

---

## Qué es

El pasaporte SBT earthling es un token digital intransmisible (Soulbound Token) que se expide a cada participante tras firmar la Declaración, verificar su identidad y abonar la cuota. Acredita criptográficamente la pertenencia al pueblo y se conserva en un registro distribuido como asiento único protegido frente a la falsificación.

A diferencia de los pasaportes estatales, ligados a un territorio y acreditativos de la nacionalidad, este pasaporte acredita la pertenencia a un pueblo unido por valores comunes. No puede cederse a otra persona, ni venderse, ni enajenarse.

**Intransmisibilidad.** El pasaporte está ligado a su monedero, y la cesión está bloqueada en el propio contrato, y no por una regla que se pueda eludir. La unicidad de la identidad está verificada en la emisión.

**Protección criptográfica.** El asiento se conserva en una red distribuida y no puede falsificarse ni alterarse sin que se advierta.

**Igualdad.** Todos reciben el mismo pasaporte con los mismos derechos. No existen clases privilegiadas ni niveles de pertenencia. Una persona, un pasaporte, un voto.

---

## Qué da el pasaporte

### Participación en el gobierno

- derecho de voto en la Asamblea DAO;
- presentación de propuestas e iniciativas;
- participación en las decisiones sobre cualquier cuestión.

> **El voto es inalienable** y no puede retirarse ni suspenderse por las opiniones, por el sentido del voto, por el desacuerdo con las decisiones o como medida general de responsabilidad (Declaración, artículo 10; [Carta, artículos 17 y 37](https://earth-lings.org/documents/es/es05-carta.html)). El voto es el contenido de la pertenencia: al retirarlo por tales fundamentos, el pueblo estaría expulsando a la persona dejándole solo el nombre.

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

El historial de participación y de aportación se hace constar públicamente: votaciones, proyectos concluidos, trabajo en las células.

> **Esas marcas no influyen en nada** y tienen carácter exclusivamente informativo: [Carta, artículo 8](https://earth-lings.org/documents/es/es05-carta.html).

---

## Cómo obtenerlo

**1. Firma de la Declaración.** Estudio de los documentos, comprensión de los principios, confirmación del acuerdo con una firma digital. Es ese acto el que crea la pertenencia.

**2. Verificación de identidad.** Comprobación de que usted es una persona viva y de que es una sola. Asegura el principio «una persona, un voto». Las imágenes originales y los escaneos de los documentos no se conservan.

**3. Abono de la cuota.** El equivalente a 79 USD, en criptomoneda (ETH, USDT, USDC). Cubre el coste de la verificación de identidad y de la emisión del pasaporte y sostiene la infraestructura del pueblo, ingresa en la caja común y se distribuye conforme a las partes publicadas.

> Quien no puede abonar la cuota por sí mismo entra en una cola abierta, y su cuota la abona otra persona o la Tesorería. El pasaporte no se diferencia en nada de los demás: en el registro no consta quién abonó la cuota. La cuota no compra la pertenencia: esta nace al firmar la Declaración.

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

- **en el registro:** identificador, seudónimo, hash de la comprobación. Los datos personales no se inscriben en el registro;
- **fuera del registro:** los datos personales de la cuenta, cifrados y en el volumen mínimo;
- **biometría:** no se conserva. Se conservan únicamente hashes criptográficos irreversibles, y solo para que una misma persona no pueda tener dos pasaportes en vigor;
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
- los asientos del registro distribuido, por definición técnica, no se suprimen, y precisamente por eso no contienen datos personales: allí hay direcciones seudónimas y marcas de actos;
- minimización del tratamiento; cifrado de los datos personales;
- las fotografías y los escaneos no se conservan.

### Responsabilidad y controversias

- DAO Earthlings no es una persona jurídica inscrita;
- los participantes responden individualmente del cumplimiento de las leyes de sus países;
- las controversias internas se resuelven con los procedimientos de la Carta: diálogo, mediación y, ante infracciones graves, recurso al Consejo Independiente. El pueblo no suplanta a los tribunales ni a los mecanismos jurídicos estatales y no ofrece arbitraje fuera de su ecosistema.

---

## Extinción del pasaporte

**Por regla general el pasaporte solo lo destruye usted mismo**, con su propia clave y desde su propio monedero (función `burnByHolder`). La plataforma no guarda sus claves y no puede ni ejecutar la destrucción en su lugar ni impedirla.

La Carta (artículo 21) establece **dos y solo dos** excepciones, y esa lista no puede ampliarse.

> **Sobre el fallecimiento del titular.** La pertenencia cesa por el fallecimiento de la persona, pero el pasaporte no se destruye por ello. El pueblo no tiene acceso a los registros de defunción de todo el mundo, de modo que tal fundamento se apoyaría en datos no verificables y se convertiría en el modo más barato de retirar a un participante. El pasaporte permanece en el registro; la participación que ya no existe la recoge el mecanismo de inactividad (Carta, artículo 20). El pasaporte no se transmite por sucesión ni se cede en ninguna circunstancia.

### 1. Anulación de una emisión inválida

Se aplica si se establece que el pasaporte se emitió infringiendo las condiciones de emisión: se emitió a una misma persona más de un pasaporte en vigor, o la comprobación se pasó con datos falsos o con la identidad de otra persona.

**No es una medida de responsabilidad ni una expulsión del pueblo.** Solo se establece que la emisión no llegó a producirse válidamente. No se sigue una reemisión automática: si se ha removido el impedimento a una emisión válida, la persona puede pasar la comprobación de nuevo en las condiciones generales.

**El procedimiento** es una decisión de la Asamblea, y no un acto del operador:

- escrito motivado con pruebas;
- notificación al titular y **no menos de 21 días** para objetar; el titular puede recabar el apoyo de otros participantes;
- dictamen del Consejo Independiente;
- votación de la Asamblea: **75 por ciento con quórum del 25, secreta y sin delegación**;
- **recurso en el plazo de 30 días**, y para anular la decisión basta la mayoría simple.

Las facultades técnicas del operador se limitan a ejecutar una decisión ya adoptada por la Asamblea. El operador no puede anular un pasaporte por sí mismo.

### 2. Reemisión técnica

A **solicitud del propio titular** en caso de pérdida de acceso al monedero o de migración del contrato. El pasaporte se destruye y se emite de nuevo de inmediato en la misma dirección o en una nueva. **La pertenencia no se interrumpe** y no hace falta votación.

### Principio de inalienabilidad

Nadie puede ser privado por la fuerza de la pertenencia al pueblo. No existe procedimiento de expulsión.

Al aplicarse medidas limitativas por infracciones graves de las reglas comunes, el pasaporte se conserva, **el derecho de voto se conserva íntegramente** y las limitaciones afectan solo a la participación en las células, al derecho de presentar propuestas y al acceso a determinados servicios, por el procedimiento del artículo 22 de la Carta, con derecho de defensa, voto secreto y recurso.

### Qué ocurre técnicamente

- la destrucción se ejecuta con la función `burn` del contrato inteligente;
- los datos del pasaporte se suprimen del registro vigente del contrato;
- en el historial inmutable queda una marca seudónima de que el pasaporte existió y fue destruido: es un hecho del pasado, y no una pertenencia continuada;
- en el registro no hay datos personales reales;
- para adherirse de nuevo se pasa el procedimiento completo y se emite un pasaporte nuevo.

---

## Sobre la financiación

A día de hoy el pueblo se desarrolla con los fondos de sus participantes: no se ha captado financiación externa.

La Carta y el documento [Tesorería](https://earth-lings.org/documents/es/es09-tesoreria.html) prevén la posibilidad de aceptar subvenciones y donaciones de organizaciones externas, con publicación obligatoria de la fuente, sin condiciones contrarias a los principios del pueblo y con una prohibición expresa: el donante no obtiene ni voto ni influencia sobre las decisiones. La cuantía de una donación no da nada.

Las cuotas de los participantes cubren el coste de la verificación de identidad y de la emisión de los pasaportes, el desarrollo de la infraestructura, el acompañamiento jurídico y el funcionamiento del ecosistema. Todas las decisiones de gasto se adoptan por votación de la Asamblea DAO y se publican.
