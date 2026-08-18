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

> **Límites de la plataforma.** La plataforma no adopta decisiones y no puede adoptarlas. Las decisiones vinculantes las adopta únicamente la Asamblea DAO. La plataforma es el nivel de ejecución: ofrece la interfaz, hace constar el resultado y lo pone en obra. Ninguno de sus componentes, ningún mecanismo automático y ninguna persona que la opere puede modificar, anular ni bloquear una decisión de la Asamblea.

---

# SECCIÓN 02. Niveles de la arquitectura

La arquitectura se construye por capas. Cada capa resuelve su tarea e interviene lo mínimo en las demás.

**1. Nivel de presentación.** Interfaces web, aplicaciones móviles, API para integraciones externas. Aquí la persona ve la Declaración, el mapa de proyectos, el panel de células, las votaciones, su área personal. La prioridad es la accesibilidad y la claridad.

**2. Nivel de aplicaciones.** Módulos de funcionalidad: gestión del perfil, presentación de iniciativas, trabajo de las células, votaciones, delegación, gestión de los fondos, herramientas auxiliares de IA. Lógica de negocio sin almacenamiento de datos de bajo nivel.

**3. Nivel de datos.** Almacenes de perfiles, metadatos de los proyectos, estados de las células, configuraciones de la DAO, resultados de las votaciones, registros de eventos. Principios de minimización, de separación y de «no recoger de más».

**4. Nivel de identidad y confianza.** Sistema propio de verificación de identidad, emisión y registro de los tokens de identidad intransmisibles, constancia de la firma de la Declaración. La capa está aislada y protegida al máximo.

**5. Nivel de economía de la participación.** Infraestructura de la unidad de cuenta, fondo común, distribución de las remuneraciones, integración con los proyectos y las células.

**6. Nivel de integración con la DAO.** Interfaces y protocolos por los que las decisiones de la Asamblea se reflejan en el funcionamiento de la plataforma: ajustes, accesos, parámetros de la economía, prioridades de desarrollo.

Las capas evolucionan por separado: se puede actualizar el nivel de aplicaciones sin tocar la identidad, o cambiar los mecanismos económicos sin afectar al núcleo de la DAO.

### Quién opera la plataforma

La explotación técnica la aseguran los **Core Nodes**, coordinadores técnicos elegidos (Carta, artículo 2). Mantienen la infraestructura, responden de la ciberseguridad y del soporte técnico de las votaciones, pero no adoptan decisiones en nombre del pueblo, no gestionan las finanzas, no tienen un peso especial en las votaciones y no pueden bloquear las decisiones de la DAO. Se revocan por mayoría simple en cualquier momento.

El **Emergency Multisig** (Carta, artículo 3) puede suspender el funcionamiento de determinados contratos inteligentes al detectarse una vulnerabilidad crítica o un ciberataque. Cada acto de ese tipo exige un informe público en el plazo de 48 horas y la confirmación de la Asamblea en el plazo de 7 días; de lo contrario queda anulado.

No existen otras personas ni estructuras con facultades técnicas sobre la plataforma.

### Sobre la IA

En la etapa inicial la plataforma emplea modelos de inteligencia artificial ya existentes para analizar iniciativas, apoyar proyectos y automatizar tareas rutinarias. En perspectiva se contempla desarrollar un modelo propio adaptado a las tareas del pueblo.

Los límites del uso de la IA están establecidos en el artículo 10 de la Declaración: ninguna arquitectura digital puede justificar la manipulación encubierta o la supresión de la autonomía humana. De ahí tres reglas estrictas que rigen con independencia del modelo que se emplee:

- **La IA no decide nada.** Cualquier conclusión suya tiene carácter de recomendación y no es fundamento de denegación.
- **Los fundamentos se revelan.** La persona cuya iniciativa haya marcado la IA recibe una exposición de los motivos en forma comprensible, y no una negativa sin explicación.
- **La revisión humana está garantizada.** Quien presenta la iniciativa puede exigir el examen por una persona, y ese examen se realiza en el plazo establecido.

---

# SECCIÓN 03. Identidad: verificación de identidad y pasaporte intransmisible

La identidad se construye en torno a un pasaporte digital intransmisible (SBT) ligado a una identidad verificada. Se observa una separación estricta:

- la biometría y los documentos los trata en tiempo real el sistema propio de verificación de identidad;
- la plataforma recibe solo el hecho de que la comprobación ha sido satisfactoria, y no los datos biométricos en bruto ni los escaneos;
- tras la comprobación se emite en la dirección del participante un pasaporte que acredita su condición;
- una persona, un pasaporte; el pasaporte no se cede, no se vende y no se retira.

### Separación de los ejes: identidad, voto, economía

La arquitectura exige que la identidad, el voto y la huella económica no se fundan en un único punto de poder:

- la **identidad** la fija el pasaporte y la verificación de identidad;
- el **voto** deriva de la condición de earthling: una persona, un voto;
- la **actividad económica** se refleja en la unidad de cuenta y no da votos adicionales en ninguna cantidad.

### Destrucción del pasaporte

Por regla general el pasaporte solo lo destruye su titular, con su propia clave y desde su propio monedero. La plataforma no guarda las claves del participante y es técnicamente incapaz tanto de ejecutar la destrucción en su lugar como de impedirla.

La Carta (artículo 21) establece dos y solo dos excepciones, que la plataforma está obligada a soportar y no puede ampliar:

1. **la anulación de una emisión inválida**, si se establece que el pasaporte se emitió infringiendo las condiciones de emisión; únicamente por decisión de la Asamblea con mayoría sancionadora, en votación secreta y con derecho de recurso;
2. **la reemisión técnica**, a solicitud del propio titular en caso de pérdida de acceso al monedero o de migración del contrato; la pertenencia no se interrumpe.

En la plataforma no se implementan otros fundamentos de destrucción contra la voluntad del titular. Entre ellos no está el fallecimiento del titular: la plataforma no dispone ni puede disponer de datos sobre defunciones, y el cese de la participación lo recoge el mecanismo de inactividad (Carta, artículo 20).

---

# SECCIÓN 04. Área personal y perfil

El área personal es el punto principal de contacto de la persona con el ecosistema.

### Elementos principales del perfil

- el seudónimo del earthling: el nombre público en el ecosistema;
- el país de residencia o de pertenencia, a elección del participante;
- el estado de la firma de la Declaración;
- la marca de que se tiene pasaporte, sin revelar datos personales;
- las áreas de interés y de competencia, si así se desea.

### Marcas de participación

- participación en células;
- participación en proyectos: papel, aportación, estado de conclusión;
- participación en votaciones, en la medida establecida por las reglas de apertura y secreto (sección 06);
- marcas de reconocimiento recibidas.

> **Las marcas de reconocimiento no influyen en nada** y siguen siendo exclusivamente informativas ([Carta, artículo 8](https://earth-lings.org/documents/ru/ru05-ustav.html)). La plataforma no puede emplear indicadores de reputación como condición de acceso a ninguna función.

### Qué no hay en el área personal

Los datos del documento de identidad, la biometría y los atributos jurídicos sensibles no se muestran ni se conservan. Quedan en el sistema de verificación de identidad y no se guardan tras la comprobación. La plataforma trabaja con el seudónimo, con la marca de pasaporte y con indicadores agregados de participación.

Las fotografías y los escaneos no se conservan; la biometría se trata solo en el momento de la comprobación. Qué se conserva exactamente para impedir un registro repetido está en la [Política de verificación biométrica](https://earth-lings.org/documents/ru/ru16-biometricheskaya-verifikaciya.html).

---

# SECCIÓN 05. Células y flujo de proyectos

La plataforma asegura el ciclo completo: desde la aparición de la idea hasta la conclusión del proyecto.

**1. Solicitud de proyecto.** Cualquier earthling propone un proyecto desde su área personal. La solicitud incluye la descripción del tema, el fin, el efecto esperado, las competencias necesarias y el horizonte de realización. El análisis inicial lo realiza la IA - sobre la conformidad con la Declaración, con la ética y con las prioridades - y ese análisis es de recomendación: no constituye denegación, los fundamentos se revelan y el examen por una persona está garantizado (sección 02).

**2. Aviso a los participantes del área.** Tras el análisis inicial, la solicitud se remite a aquellos cuyas competencias declaradas se corresponden con ella: juristas, ingenieros, programadores, analistas y otros.

**3. Formación de la célula.** La célula se forma con quienes han respondido. El tamaño va de 2 a 6 personas (Carta, artículo 23). Si la tarea exige más personas, se crean varias células vinculadas y no una sola pesada.

**4. Coordinación y ejecución.** Tablero de tareas, cronogramas, canales de comunicación, rendición de cuentas por etapas, integración con los repositorios de documentos y con las herramientas auxiliares.

**5. Conclusión y registro.** La plataforma registra el resultado, reparte las remuneraciones si están previstas, actualiza el estado de los participantes y refleja la aportación del proyecto en el mapa general de actividad.

> **Sobre la división en células profesionales y de proyecto.** La Carta conoce una sola forma: la célula de dos a seis personas. La división en agrupaciones profesionales permanentes por competencias y en equipos temporales de proyecto es un **recurso de organización del trabajo en la plataforma**, y no una estructura aparte del pueblo. Puede modificarse por decisión de la Asamblea y no crea ni órganos, ni facultades, ni representación: ninguna célula tiene voto colectivo y ninguna interviene en nombre de otros participantes.

---

# SECCIÓN 06. Votación y delegación

## Un earthling, un voto

Cada participante que tenga pasaporte y haya firmado la Declaración dispone de un voto. El voto no se refuerza con la cantidad de unidades de cuenta, con la posición en las células ni con la reputación. El peso económico y el derecho de voto están separados por arquitectura, y no de manera declarativa.

**El derecho de voto no puede limitarse por las opiniones, por el sentido del voto o como medida general de responsabilidad** (Declaración, artículo 10; Carta, artículos 17 y 37). Las limitaciones previstas en el artículo 22 de la Carta afectan a la participación en las células, al derecho de presentar propuestas y al acceso a determinados servicios, pero no al voto ni al acceso a las votaciones mismas.

El único caso en que la plataforma ejecuta una suspensión del voto es una decisión de la Asamblea conforme al artículo 22 bis de la Carta por socavamiento probado de la integridad de la votación, por un plazo no superior a 6 meses. La plataforma ejecuta tal decisión y no puede ni promoverla, ni aplicarla por otro fundamento, ni prorrogarla.

## Apertura y secreto

Por regla general las votaciones son abiertas: el hecho de la participación y la expresión de la voluntad están disponibles para su verificación por todos los participantes. La apertura es el modo de comprobar que el recuento es honesto.

Pero la transparencia alcanza a los actos de las instituciones, no a los datos personales de las personas. Por eso la plataforma está obligada a soportar el **voto secreto con recuento verificable**: el resultado lo verifican todos y el vínculo entre el voto y quien vota no se revela a nadie, incluidos quienes operan la plataforma. Cuándo se aplica el modo secreto: [Carta, artículo 6](https://earth-lings.org/documents/ru/ru05-ustav.html).

El voto secreto se aplica:

- **obligatoriamente**, al examinar una limitación de facultades y en la anulación de una emisión inválida de pasaporte;
- **por decisión de la Asamblea**, para cuestiones o categorías concretas, en particular las que afectan a la posición del pueblo sobre los actos de los Estados y sobre cuestiones internacionales.

En todos los casos se publican la cuestión, el resultado, el número de votantes y el resultado de la verificación del recuento.

## Delegación

La plataforma soporta la cesión del voto en un ámbito concreto a otro participante. Las exigencias de la Carta (artículo 7) se implementan técnicamente y se comprueban en cada operación:

- **solo por ámbitos**: delegar el voto en todas las cuestiones a la vez es técnicamente imposible;
- **prohibición de la autodelegación**: se comprueba en cada operación;
- **prohibición de las cadenas**: un voto delegado recibido no puede cederse a su vez;
- **techo**: el 5 por ciento de los participantes, y no menos de 10 delegantes;
- **una sola delegación activa por ámbito**: no cabe repetirla sin revocar la anterior;
- **revocación en un solo paso**: en cualquier momento, sin explicar los motivos y sin el consentimiento de aquel a quien se cedió el voto;
- **cuestiones sin delegación**: la modificación de la Carta y de las reglas básicas de la tesorería, la financiación por encima del umbral establecido, la formación del Emergency Multisig, la limitación de facultades y la anulación de un pasaporte: en ellas se vota solo personalmente.

Delegado puede ser cualquier earthling: la única selección es la elección de quien delega (Carta, artículo 7).

## Lista de propuestas

Todas las propuestas se muestran **por orden cronológico de presentación**. La reputación del autor no influye en su lugar en la lista. El filtrado por reputación está disponible solo como modo de visualización que cada participante activa para sí.

Una priorización automática de las propuestas formaría un orden del día sin responsabilidad formal, y por eso no se implementa en la plataforma.

## Qué hace la plataforma dentro del circuito de la DAO

- interfaz de votación y de debate;
- constancia pública de las decisiones adoptadas y de sus estados de ejecución;
- realización técnica de las decisiones: cambio de ajustes, actualización de las reglas de distribución de fondos, puesta en marcha de programas;
- registro de las acciones clave para su auditoría posterior.

La infraestructura de bajo nivel puede ser cualquiera; los principios no dependen de ella.

---

# SECCIÓN 07. La unidad de cuenta en la plataforma

La plataforma es la interfaz principal de uso práctico de la unidad de cuenta. La separación entre economía y poder se observa con rigor.

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

Los datos que se encuentran en las bases de la plataforma se rectifican y se suprimen a petición del participante. Los asientos del registro distribuido, por su naturaleza, no se suprimen, y precisamente por eso no contienen datos personales: allí hay direcciones seudónimas y marcas de actos, pero no nombre, ni documento, ni biometría.

Al salir, el pasaporte se destruye y en el registro queda una marca seudónima de que la pertenencia existió en un período determinado. Es un hecho del pasado, y no una pertenencia continuada. Ese modelo se corresponde con la práctica asentada en los litigios europeos sobre los libros parroquiales: el asiento se conserva, la condición se marca.

La libertad de asociación no exige el borrado de la historia: la renuncia a una nacionalidad no destruye los archivos del Estado.

### Verificación de identidad y protección de datos

- la biometría y los documentos los trata el sistema propio en el momento de la comprobación; las imágenes y los escaneos no se conservan;
- la plataforma recibe solo el resultado técnico: satisfactorio o no satisfactorio;
- ante requerimientos de órganos del Estado, el pueblo puede confirmar el hecho de la condición de participante si hay fundamentos legales, pero no revela datos biométricos, que no tiene;
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

> **Capacidad de existir sin operador.** El registro de pasaportes se lleva en una red distribuida, y no en los servidores de la plataforma. Eso significa que la composición del pueblo no depende de quién opere la plataforma hoy, y se conserva al cambiar de operador, al migrar la infraestructura y en una reconstitución reconocida por la Hoja de ruta como continuación legítima.

---

# SECCIÓN 10. Etapas de realización

Importa tanto cómo está hecha la arquitectura de destino como cómo llegar a ella.

**Etapa 1. Núcleo: construido y desplegado.**
Área personal, firma de la Declaración, mapa de proyectos, estados de las células, mecanismo de votación, integración con el sistema propio de verificación de identidad. El mínimo de funciones suficiente para empezar.

**Etapa 2. Células y proyectos: construido y desplegado.**
Ciclo de trabajo con las células: solicitudes, formación, realización, registro de resultados. Herramientas auxiliares de IA para analizar iniciativas.

**Etapa 3. Llenado con práctica: pendiente.**
Votaciones de fondo regulares, voto secreto con recuento verificable, delegación por ámbitos, fondos en funcionamiento, ampliación de los escenarios de uso de la unidad de cuenta. El llenado empieza con la apertura de las adhesiones y se produce a medida que crece el número de participantes.

**Etapa 4. Relación externa: pendiente.**
Relación con organizaciones internacionales, universidades y centros de investigación. Puesta a disposición de datos agregados para el análisis de procesos globales. Participación del pueblo en el debate de cuestiones que exceden el marco de un solo país.

> **Sobre el límite de la cuarta etapa.** Se trata del derecho a ser oído, y no del poder en la decisión. La plataforma no se convierte ni puede convertirse en un lugar donde se adopten decisiones obligatorias para nadie que no sean los propios Earthlings. Las facultades de los Estados no se ven afectadas (Declaración, artículo 7).

La división entre lo construido y lo pendiente se expone con honestidad: la infraestructura existe y está comprobada en entorno de producción, pero su valor probatorio y práctico nace a medida que se acumula participación, y no en el momento del despliegue.

---

## Nota: la interfaz jurídica externa

Para relacionarse con la infraestructura jurídica, administrativa y financiera tradicional, el pueblo Earthlings emplea instrumentos jurídicos inscritos en distintas jurisdicciones. Tales instrumentos son medios operativos sustituibles de relación externa y no definen al pueblo.

Las personas que actúan a través de esos instrumentos ejecutan un encargo de la Asamblea, revocable en cualquier momento por mayoría simple, y no constituyen cargos. El modelo jurídico detallado está en el documento [Base jurídica](https://earth-lings.org/documents/ru/ru04-pravovoe-obosnovanie.html).
