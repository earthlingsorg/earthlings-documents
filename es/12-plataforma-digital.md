# Plataforma digital de los Earthlings

**Infraestructura de identidad, participación y proyectos para el pueblo Earthlings**

> El presente documento describe la realización técnica de las reglas establecidas en la Carta de los Earthlings. En caso de discrepancia se aplica la Carta, y en caso de discrepancia de la Carta con la Declaración, la Declaración. La plataforma no establece reglas: las ejecuta.

---

# SECCIÓN 01. Finalidad de la plataforma

La Plataforma digital de los Earthlings es el núcleo en el que se unen cuatro niveles del pueblo:

- **identidad**: verificada y a la vez privada;
- **participación**: firma de la Declaración, votación, debates, actuaciones conjuntas;
- **proyectos y células**: iniciativa, formación, coordinación, ejecución y registro de resultados;
- **economía de la participación**: unidad de cuenta, fondo común, remuneración por la aportación.

La plataforma no es una red social ni un sistema de cadena de bloques más. Es la herramienta con la que el pueblo Earthlings puede existir: con una infraestructura transparente y a la vez cuidadosa con la persona.

La tarea principal es hacer la participación práctica, segura y honesta: desde la primera firma de la Declaración hasta la realización de proyectos internacionales complejos.

> **Límites de la plataforma.** La plataforma no adopta decisiones y no puede adoptarlas. Las decisiones vinculantes las adopta únicamente la Asamblea DAO. La plataforma es el nivel de ejecución: ofrece la interfaz, hace constar el resultado y lo pone en obra. Ninguno de sus componentes, ningún mecanismo automático y ninguna persona que la opere puede modificar, anular ni bloquear una decisión de la Asamblea. La Carta entra en vigor con la adopción de la Declaración (Carta, artículo 38); hasta entonces no existen ni la Asamblea DAO, ni los Core Nodes, ni el Emergency Multisig, ni el Consejo Independiente, y la única facultad discrecional del período constituyente respecto de los textos es la decisión del autor de la Declaración de incorporar propuestas al texto (documento «El período constituyente»).

---

# SECCIÓN 02. Niveles de la arquitectura

La arquitectura se construye por capas. Cada capa resuelve su tarea e interviene lo mínimo en las demás.

**1. Nivel de presentación.** Interfaces web; las aplicaciones móviles y la API para integraciones externas, en perspectiva. Aquí la persona ve la Declaración, el mapa de participantes por países, el panel de células, las votaciones, su área personal. La prioridad es la accesibilidad y la claridad.

**2. Nivel de aplicaciones.** Módulos de funcionalidad: gestión del perfil, presentación de iniciativas, trabajo de las células, votaciones, delegación, gestión de los fondos, herramientas auxiliares de IA. Lógica de negocio sin almacenamiento de datos de bajo nivel.

**3. Nivel de datos.** Almacenes de perfiles, metadatos de los proyectos, estados de las células, configuraciones de la DAO, resultados de las votaciones, registros de eventos. Principios de minimización, de separación y de «no recoger de más».

**4. Nivel de identidad y confianza.** Sistema propio de verificación de identidad, emisión y registro de los tokens de identidad intransmisibles, constancia de la firma de la Declaración. La capa está aislada y protegida al máximo.

**5. Nivel de economía de la participación.** Infraestructura de la unidad de cuenta, fondo común, distribución de las remuneraciones, integración con los proyectos y las células.

**6. Nivel de integración con la DAO.** Interfaces y protocolos por los que las decisiones de la Asamblea se reflejan en el funcionamiento de la plataforma: ajustes, accesos, parámetros de la economía, prioridades de desarrollo.

Las capas evolucionan por separado: se puede actualizar el nivel de aplicaciones sin tocar la identidad, o cambiar los mecanismos económicos sin afectar al núcleo de la DAO.

### Quién opera la plataforma

La explotación técnica la aseguran los **Core Nodes**, coordinadores técnicos elegidos (Carta, artículo 2). Mantienen la infraestructura, responden de la ciberseguridad y del soporte técnico de las votaciones, pero no adoptan decisiones en nombre del pueblo, no gestionan las finanzas, no tienen un peso especial en las votaciones y no pueden bloquear las decisiones de la DAO. Se revocan por mayoría simple en cualquier momento.

El **Emergency Multisig** (Carta, artículo 3) puede suspender el funcionamiento de determinados contratos inteligentes al detectarse una vulnerabilidad crítica o un ciberataque. Cada acto de ese tipo exige un informe público en el plazo de 48 horas y la confirmación de la Asamblea en el plazo de 7 días; de lo contrario queda anulado.

La Carta no prevé otras estructuras con facultades técnicas sobre la plataforma. Hasta la adopción de la Declaración esos órganos no existen (Carta, artículo 38) y, tras la adopción, hasta la elección de los Core Nodes y del Emergency Multisig, sus funciones se ejercen de manera procedimental (Carta, artículo 39); dónde hay que confiar hoy en quienes operan la plataforma está señalado en el documento «Dónde estamos ahora».

### Sobre la IA

Para analizar iniciativas, apoyar proyectos y automatizar tareas rutinarias la plataforma empleará modelos de inteligencia artificial ya existentes; hoy no dispone de tales herramientas. En perspectiva se contempla desarrollar un modelo propio adaptado a las tareas del pueblo.

Los límites del uso de la IA se establecen en el artículo 3 de la Declaración: ningún algoritmo, código o sistema de inteligencia artificial puede ser la fuente última de una decisión que afecte a los derechos, a la dignidad o a la situación de una persona, y ninguna tecnología puede emplearse para manipular a las personas de manera encubierta o para suprimir la autonomía humana. De ahí tres reglas estrictas que rigen con independencia del modelo que se emplee:

- **La IA no decide nada de manera definitiva** (Declaración, artículo 3). La conclusión de la IA sobre una iniciativa o un proyecto tiene carácter de recomendación y no es fundamento de denegación; la denegación del sistema automático en la verificación de identidad no es definitiva, y la revisión por una persona se rige por la Política de verificación biométrica.
- **Los fundamentos se revelan.** La persona cuya iniciativa haya sido señalada por la IA recibe una exposición de los motivos en forma comprensible, y no una negativa sin explicación.
- **La revisión humana está garantizada.** Quien presenta la iniciativa puede exigir el examen por una persona, y ese examen se realiza en el plazo establecido.

---

# SECCIÓN 03. Identidad: verificación de identidad y pasaporte intransmisible

La identidad se construye en torno a un pasaporte digital intransmisible (SBT) ligado a una identidad verificada. Se observa una separación estricta:

- la biometría y los documentos los trata en tiempo real el sistema propio de verificación de identidad;
- del sistema de verificación de identidad la plataforma recibe el resultado de la comprobación, el número del asiento del pasaporte, el identificador del participante, el seudónimo, la dirección del monedero, el correo y el país, pero no los datos biométricos, ni las imágenes, ni los datos del documento;
- tras la comprobación y la firma de la Declaración se emite un pasaporte a la dirección del monedero del participante que acredita su pertenencia; en el período constituyente la firma está suspendida y, como resultado de la verificación de identidad, se entrega un documento temporal de participante en la constitución (documento «El período constituyente», parte 2, apartado 5);
- una persona, un pasaporte; el pasaporte no se cede, no se vende y no se retira.

### Separación de los ejes: identidad, voto, economía

La arquitectura exige que la identidad, el voto y la huella económica no se fundan en un único punto de poder:

- la **identidad** la fija el pasaporte y la verificación de identidad;
- el **voto** deriva de la condición de earthling: una persona, un voto;
- la **actividad económica** se refleja en la unidad de cuenta y no da votos adicionales en ninguna cantidad.

### Destrucción del pasaporte

Por regla general el pasaporte solo lo destruye su titular, con su propia clave y desde su propio monedero. La plataforma no guarda las claves del participante y es técnicamente incapaz de impedir la destrucción; nadie tiene derecho a destruir el pasaporte en lugar del participante pero, mientras los derechos del propietario del contrato no se hayan traspasado a una firma múltiple, la emisión y la destrucción del pasaporte están técnicamente al alcance de una sola clave (documento «Dónde estamos ahora»).

La Carta (artículo 21) establece dos y solo dos excepciones, que la plataforma está obligada a soportar y no puede ampliar:

1. **la anulación de una emisión inválida**, si se establece que el pasaporte se emitió infringiendo las condiciones de emisión; únicamente por decisión de la Asamblea con mayoría sancionadora, en votación secreta y con derecho de recurso;
2. **la reemisión técnica**, a solicitud del propio titular en caso de pérdida de acceso al monedero o de migración del contrato; la pertenencia no se interrumpe.

En la plataforma no se implementan otros fundamentos de destrucción por persona distinta del titular, y contra la voluntad de su titular el pasaporte se destruye únicamente en caso de anulación de una emisión inválida. Entre los fundamentos no está el fallecimiento del titular: la plataforma no dispone ni puede disponer de datos sobre defunciones, y la pertenencia cesa por el fallecimiento por sí misma, sin decisión de nadie (Declaración, artículo 4); el pasaporte permanece en el registro, y la falta de participación la contempla el mecanismo de inactividad (Carta, artículo 20).

---

# SECCIÓN 04. Área personal y perfil

El área personal es el punto principal de contacto de la persona con el ecosistema.

### Elementos principales del perfil

- el seudónimo del earthling: el nombre público en el ecosistema;
- el país de residencia;
- el estado de la verificación de identidad;
- la marca de que se tiene pasaporte, sin revelar datos personales;
- las áreas de interés y de competencia, si así se desea.

### Marcas de participación

- participación en células;
- participación en proyectos: papel, aportación, estado de conclusión;
- la participación en votaciones no se marca: la participación de una persona concreta en la votación no se publica (sección 06);
- marcas de reconocimiento recibidas.

> **Las marcas de reconocimiento no influyen en nada** y siguen siendo exclusivamente informativas ([Carta, artículo 8](https://earth-lings.org/documents/es/es05-carta.html)). La plataforma no puede emplear indicadores de reputación como condición de acceso a ninguna función.

### Qué no hay en el área personal

Los datos del documento de identidad, la biometría y los atributos jurídicos sensibles no se muestran ni se conservan. No salen del sistema de verificación de identidad y no se conservan una vez concluida la comprobación. La plataforma trabaja con el seudónimo, la dirección de correo, el país, la dirección del monedero, la marca de pasaporte y los datos sobre el uso de la plataforma; la lista y los fines están en la Política de privacidad.

Las fotografías y los escaneos no se conservan; la biometría se trata solo en el momento de la comprobación. Qué se conserva exactamente para impedir un registro repetido está en la [Política de verificación biométrica](https://earth-lings.org/documents/es/es16-verificacion-biometrica.html).

---

# SECCIÓN 05. Células y flujo de proyectos

La plataforma asegura el ciclo completo: desde la aparición de la idea hasta la conclusión del proyecto.

**1. Solicitud de proyecto.** Cualquier earthling propone un proyecto desde su área personal. La solicitud incluye la descripción del tema, el fin, el efecto esperado, las competencias necesarias y el horizonte de realización. El análisis inicial puede realizarlo la IA - sobre la conformidad con la Declaración, con la ética y con las prioridades - y ese análisis tiene carácter de recomendación: no constituye denegación, los fundamentos se revelan y el examen por una persona está garantizado (sección 02).

**2. Aviso a los participantes del área.** Tras el análisis inicial, la solicitud se remite a aquellos cuyas competencias declaradas se corresponden con ella: juristas, ingenieros, programadores, analistas y otros.

**3. Formación de la célula.** La célula se forma con quienes han respondido. El tamaño va de 2 a 6 personas (Carta, artículo 23). Si la tarea exige más personas, se crean varias células vinculadas y no una sola pesada.

**4. Coordinación y ejecución.** Tablero de tareas, cronogramas, canales de comunicación, rendición de cuentas por etapas, integración con los repositorios de documentos y con las herramientas auxiliares. Las decisiones dentro de la célula se adoptan por consentimiento; si una objeción fundada en daño, inviabilidad o riesgo grave no se resuelve, la cuestión la decide una votación de la célula: la decisión se adopta si hay más votos a favor que en contra; quienes se abstuvieron participaron en la votación, pero no cuentan ni a favor ni en contra. La votación es válida si ha participado en ella más de la mitad de los participantes de la célula (documento «Células», sección 05).

**5. Conclusión y registro.** La plataforma registra el resultado, reparte las remuneraciones si están previstas, actualiza el estado de los participantes y refleja la aportación del proyecto en el mapa general de actividad.

> **Sobre la división en células profesionales y de proyecto.** La Carta conoce una sola forma: la célula de dos a seis personas. La división en agrupaciones profesionales permanentes por competencias y en equipos temporales de proyecto es un **recurso de organización del trabajo en la plataforma**, y no una estructura aparte del pueblo. Puede modificarse por decisión de la Asamblea y no crea ni órganos, ni facultades, ni representación: ninguna célula tiene voto colectivo y ninguna interviene en nombre de otros participantes.

---

# SECCIÓN 06. Votación y delegación

## Un earthling, un voto

Cada participante que haya firmado la Declaración dispone de un voto; el pasaporte acredita ese voto. El voto no se refuerza con la cantidad de unidades de cuenta, con la posición en las células ni con la reputación. El peso económico y el derecho de voto están separados por arquitectura, y no de manera declarativa.

**El derecho de voto no puede limitarse por las opiniones, por el sentido del voto o como medida general de responsabilidad** (Declaración, artículo 4; Carta, artículos 17 y 37). Conforme al artículo 22 de la Carta hay una sola medida que recae sobre la persona: la advertencia, y no le quita nada, ni el voto, ni el acceso a las votaciones mismas, ni el derecho a presentar propuestas, ni el derecho a crear células y a entrar en ellas, ni el acceso a los servicios, ni otra cosa alguna. Las demás recaen sobre un proyecto o una célula y no afectan a los derechos de una persona.

El único caso en que la plataforma ejecuta una suspensión del voto es una decisión de la Asamblea conforme al artículo 22 bis de la Carta por socavamiento probado de la integridad de la votación, por un plazo no superior a 6 meses. La plataforma ejecuta tal decisión y no puede ni promoverla, ni aplicarla por otro fundamento, ni prorrogarla.

## Apertura y secreto

El voto personal es secreto: la votación debe estar organizada de modo que nadie, incluidos quienes operan la plataforma, pueda saber cómo ha votado una persona concreta, ni cerciorarse de ello aun con su consentimiento. La participación de una persona concreta en la votación no se publica. Todavía no existe un medio de votación secreta: se está eligiendo, y hoy estas reglas no se cumplen en todas partes: en el canal abierto de votaciones el voto y la dirección del monedero son públicos, y los votos emitidos en las células la plataforma los guarda junto con la cuenta de usuario (documento «Dónde estamos ahora»; Política de privacidad, sección 02).

La transparencia alcanza a los actos de las instituciones, no a los datos personales de las personas. Por eso la plataforma está obligada a asegurar el **voto secreto con recuento verificable**: el resultado lo verifican todos y el vínculo entre el voto y quien vota no se revela a nadie, incluidos quienes operan la plataforma. El procedimiento: [Carta, artículo 6](https://earth-lings.org/documents/es/es05-carta.html).

La plataforma debe asegurar también:

- **hasta el cierre de la votación**: el recuento parcial oculto y la posibilidad de volver a votar; se computa el último voto emitido; el voto personal sobre una cuestión deja sin efecto la delegación respecto de esa cuestión;
- **la apertura de los votos del delegado**: los votos cedidos que emite el delegado son visibles para todos; no se publica quién ha cedido su voto al delegado.

La Carta exige publicar la cuestión, las opciones de respuesta, los plazos, el número de quienes tenían derecho a voto, el número de votantes, el resultado, la prueba del recuento y el modo en que cualquier persona puede rehacer el recuento por su cuenta (artículo 6). Hoy no hay prueba del recuento ni para la Asamblea ni para las células: aparecerá junto con el medio de votación secreta (documento «Dónde estamos ahora»).

## Delegación

La plataforma soporta la cesión del voto en un ámbito concreto a otro participante. Las exigencias de la Carta (artículo 7) deben implementarse técnicamente y comprobarse en cada operación:

- **solo por ámbitos**: delegar el voto en todas las cuestiones a la vez es técnicamente imposible;
- **prohibición de la autodelegación**: se comprueba en cada operación;
- **prohibición de las cadenas**: un voto delegado recibido no puede cederse a su vez;
- **techo**: el 5 por ciento de los participantes, y no menos de 10 delegantes;
- **una sola delegación activa por ámbito**: no cabe repetirla sin revocar la anterior;
- **revocación en un solo paso**: en cualquier momento, sin explicar los motivos y sin el consentimiento de aquel a quien se cedió el voto;
- **cuestiones sin delegación**: la modificación de la Carta y de las reglas básicas de la tesorería, la financiación por encima del umbral establecido, la formación del Emergency Multisig, la limitación de facultades, la suspensión del derecho de voto, la anulación de la emisión de un pasaporte y la modificación de los principios intangibles: en ellas se vota solo personalmente.

Delegado puede ser cualquier earthling: la única selección es la elección de quien delega (Carta, artículo 7).

## Lista de propuestas

Todas las propuestas se muestran **por orden cronológico de presentación**. La reputación del autor no influye en su lugar en la lista. El filtrado por reputación estará disponible solo como modo de visualización que cada participante activa para sí; hoy la plataforma no lo tiene.

Una priorización automática de las propuestas formaría un orden del día sin responsabilidad formal, y por eso no se implementa en la plataforma.

## Qué hace la plataforma dentro del circuito de la DAO

- interfaz de votación y de debate;
- constancia pública de las decisiones adoptadas y de sus estados de ejecución;
- realización técnica de las decisiones: cambio de ajustes, actualización de las reglas de distribución de fondos, puesta en marcha de programas;
- registro de las acciones clave para su auditoría posterior.

La infraestructura de bajo nivel puede ser cualquiera; los principios no dependen de ella.

---

# SECCIÓN 07. La unidad de cuenta en la plataforma

La plataforma será la interfaz principal de uso práctico de la unidad de cuenta; hoy la unidad no está emitida: la economía de la participación se lleva en la contabilidad interna de la plataforma (documento «Earthlings Coin», sección 8), y los supuestos que siguen describen para qué está destinada. La separación entre economía y poder se observa con rigor.

### Escenarios internos

- remuneración por la aportación a proyectos y células;
- gestión de los fondos internos;
- pago del acceso a determinados servicios y herramientas;
- apoyo a iniciativas: microsubvenciones, experimentos, programas piloto.

### Qué no hace la unidad de cuenta

- no da votos adicionales ni peso político;
- no determina el acceso a la participación básica: firmar la Declaración, votar, debatir;
- no influye en el lugar de una propuesta en la lista ni en la prioridad de su examen;
- no puede emplearse como instrumento de presión o de exclusión de personas de los procesos;
- no sustituye a las monedas nacionales y no se impone como medio de pago cotidiano.

La unidad de cuenta refleja la aportación y permite poner en marcha proyectos, pero no divide a las personas en importantes y no importantes. La plataforma vela por que la lógica económica no destruya la igualdad de participación.

---

# SECCIÓN 08. Datos y privacidad

La plataforma se crea teniendo en cuenta los principios del RGPD y estándares análogos. El principio de partida es que preservar la dignidad humana y el derecho a la vida privada importa más que la comodidad de la analítica.

### Principios básicos

- **minimización**: se recoge únicamente lo que es realmente necesario;
- **separación**: identidad, participación, economía y analítica están repartidas en capas y almacenes distintos;
- **transparencia**: el participante sabe qué datos hay sobre él y cómo se emplean;
- **control**: el participante puede solicitar la rectificación o la supresión de los datos tratados por la plataforma.

### Qué ocurre con los datos en el registro distribuido

Aquí hace falta honestidad, y no una promesa que no se pueda cumplir.

Los datos que se encuentran en las bases de la plataforma se rectifican a petición del participante y a petición suya se suprimen, salvo los señalados en la Política de privacidad; para quien pertenece al pueblo, la supresión de la cuenta de usuario solo va unida a la salida. Los asientos del registro distribuido, por su naturaleza, no se suprimen, y precisamente por eso el nombre, el documento, la biometría y los hashes de la verificación no se inscriben en él en el momento de la emisión. En la emisión se inscriben en el registro la dirección del monedero, el número del asiento del pasaporte, el identificador del participante por el que el asiento queda vinculado a los datos del sistema de verificación de identidad, y la hora de la emisión; en el campo del seudónimo se inscribe en la emisión una sola palabra, «Earthling», y en el campo del hash de la verificación, un valor aleatorio no relacionado con los datos de la verificación; la emisión y la destrucción dejan marcas en el registro. Son datos seudónimos que nosotros tenemos vinculados a su cuenta de usuario.

Al salir, el pasaporte se destruye y en el registro queda una marca seudónima de que la pertenencia existió en un período determinado. Es un hecho del pasado, y no una pertenencia continuada. Ese modelo es el que predomina en la práctica europea en materia de libros parroquiales: el asiento se conserva, la condición se marca; si ese modelo basta lo está decidiendo ahora el Tribunal de Justicia de la Unión Europea (asunto C-12/25).

La libertad de asociación no exige el borrado de la historia: la renuncia a una nacionalidad no destruye los archivos del Estado.

### Verificación de identidad y protección de datos

- la biometría y los documentos los trata el sistema propio en el momento de la comprobación; las imágenes y los escaneos no se conservan;
- la plataforma recibe del sistema de verificación de identidad no la biometría ni los datos del documento, sino el resultado de la comprobación y los datos para la cuenta de usuario (sección 03);
- en virtud de una resolución judicial firme o de un requerimiento legal equivalente, los datos se comunican en la forma prevista en la Política de privacidad (sección 05); entre ellos no hay datos biométricos: no se conservan;
- los asientos del registro se someten al principio de seudonimia y de minimización de los vínculos personales.

La plataforma no se construye como un sistema de registro total. Aspira a ser un ejemplo de trato cuidadoso con los datos en una época en la que técnicamente es posible casi todo.

---

# SECCIÓN 09. Arquitectura técnica y escalabilidad

Las tecnologías concretas - cadenas de bloques, bases de datos, lenguajes, marcos de trabajo - pueden cambiar. Lo que importa es la lógica arquitectónica:

- **modularidad**: el núcleo, el subsistema de identidad, el componente DAO, la capa económica y las interfaces evolucionan de manera independiente;
- **escalabilidad**: la arquitectura está pensada para un crecimiento de la composición en órdenes de magnitud sin pérdida de disponibilidad ni de seguridad;
- **resistencia**: configuraciones tolerantes a fallos, almacenes de respaldo, nodos independientes;
- **recuperación**: copias de seguridad, plan de recuperación tras fallos críticos, protocolos de actuación ante el compromiso de claves;
- **auditabilidad**: posibilidad de auditoría técnica y jurídica externa de los componentes clave.

La plataforma no está ligada para siempre a una única pila tecnológica. En cualquier migración se conservan los principios: identidad intransmisible, voto igual e inalienable, verificabilidad de los procesos y protección de la persona.

> **Capacidad de existir sin operador.** El registro de pasaportes se lleva en una red distribuida, y no en los servidores de la plataforma. Por eso los asientos del registro se conservan al cambiar de operador, al migrar la infraestructura y en una reconstitución reconocida por la Hoja de ruta como continuación legítima; dónde depende hoy el registro de quien lo opera está en el documento «Dónde estamos ahora».

---

# SECCIÓN 10. Etapas de realización

Importa tanto cómo está hecha la arquitectura de destino como cómo llegar a ella.

**Etapa 1. Núcleo: construido y desplegado.**
Área personal, mapa de participantes por países, estados de las células, mecanismo de votación, integración con el sistema propio de verificación de identidad. El mínimo de funciones suficiente para empezar.

**Etapa 2. Células y proyectos: construido y desplegado.**
Ciclo de trabajo con las células: solicitudes, formación, realización, registro de resultados.

**Etapa 3. Llenado con práctica: pendiente.**
Votaciones de fondo regulares, voto secreto con recuento verificable, delegación por ámbitos, firma de la Declaración, herramientas auxiliares de IA para analizar iniciativas, fondos en funcionamiento, ampliación de los escenarios de uso de la unidad de cuenta. El llenado empieza con la apertura de las adhesiones y se produce a medida que crece el número de participantes.

**Etapa 4. Relación externa: pendiente.**
Relación con organizaciones internacionales, universidades y centros de investigación. Puesta a disposición de datos agregados para el análisis de procesos globales. Participación del pueblo en el debate de cuestiones que exceden el marco de un solo país.

> **Sobre el límite de la cuarta etapa.** Se trata del derecho a ser oído, y no del poder en la decisión. La plataforma no se convierte ni puede convertirse en un lugar donde se adopten decisiones obligatorias para nadie que no sean los propios Earthlings. Las facultades de los Estados no se ven afectadas (Declaración, artículo 6).

La división entre lo construido y lo pendiente se expone con honestidad. El contrato del registro de pasaportes, la verificación de identidad, las células y la contabilidad de la economía interna están desplegados y funcionan; el canal público de votación está desplegado, pero todavía no ha habido en él votaciones de fondo, el medio de votación secreta se está eligiendo y los contratos inteligentes de la Tesorería no están desplegados (documento «Dónde estamos ahora»). El valor probatorio y práctico de la infraestructura nace a medida que se acumula participación, y no en el momento del despliegue.

---

## Nota: la interfaz jurídica externa

Para la relación con la infraestructura jurídica, administrativa y financiera tradicional se emplean instrumentos jurídicos registrados en una o varias jurisdicciones. Tales instrumentos son medios operativos sustituibles de relación externa y no definen al pueblo.

Tras la adopción de la Declaración, las personas que actúan a través de esos instrumentos ejecutan un encargo revocable de la Asamblea DAO y no crean cargo alguno; antes de la adopción no hay pueblo, y nadie actúa en su nombre. El modelo jurídico detallado está en el documento [Base jurídica](https://earth-lings.org/documents/es/es04-base-juridica.html).
