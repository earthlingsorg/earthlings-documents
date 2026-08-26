# Dónde estamos ahora

*Pueblo Earthlings*

## Para qué este documento

Afirmamos que los Earthlings son verificables. Una afirmación así solo tiene sentido cuando se puede indicar con exactitud qué es lo que se verifica y de qué manera. Por eso, en lugar de la fórmula general «tenemos el código abierto», publicamos la frontera exacta: qué está abierto, qué está cerrado y por qué motivo.

Ahora está en curso el período constituyente: hasta el día de la adopción de la Declaración el pueblo todavía se está constituyendo, y parte de las cifras que siguen se lee de otro modo que después. Sus reglas y sus plazos están expuestos en el documento [El período constituyente](https://earth-lings.org/documents/es/es20-periodo-constituyente.html); aquí no los repetimos, para que las fechas tengan una sola fuente.

> **Principio.** Está abierto aquello de lo que depende la verificabilidad del pueblo: quién es participante, cómo llegó a serlo, cuántos somos y cómo se cuenta el voto. Está cerrado aquello cuya publicación no añadiría verificabilidad pero crearía un riesgo para los participantes: la capa de servidor y el tratamiento de datos personales.

## Qué está abierto

| Componente | Dónde | Licencia |
|---|---|---|
| Contrato inteligente del pasaporte EarthlingPassportV2 | [github.com/earthlingsorg/earthlings-contracts](https://github.com/earthlingsorg/earthlings-contracts) | MIT |
| Documentación de arquitectura | carpeta `/docs` de ese mismo repositorio: modelo de identidad, minimización de datos, seguridad, reputación, flujo de aportaciones | MIT |
| Dirección del contrato y todas sus transacciones | [0x20e7962878429B803E35F83ba34eD291afEC2Be4](https://polygonscan.com/address/0x20e7962878429B803E35F83ba34eD291afEC2Be4) | datos públicos |
| Registro de pasaportes | cadena de bloques Polygon, se lee directamente del contrato | datos públicos |
| Canal público de votaciones de la DAO | [snapshot.org, espacio earthlings-dao.eth](https://snapshot.org/#/s:earthlings-dao.eth) | datos públicos |
| Caja on-chain | [0xaEC7016218f7883bf6e47a2C932FdE6d822086C0](https://app.safe.global/home?safe=matic:0xaEC7016218f7883bf6e47a2C932FdE6d822086C0) | datos públicos |

## Qué está cerrado y por qué

| Componente | Motivo |
|---|---|
| Parte de servidor de la plataforma | Contiene la lógica de acceso a las cuentas. Publicarla antes de una auditoría independiente aumenta el riesgo de intrusión en las cuentas de los participantes y no añade nada a la verificabilidad del pueblo. |
| Sistema de verificación de identidad | Trabaja con documentos y biometría. Aquí la opacidad es parte de la protección de los datos personales, y no un ocultamiento. Cómo funciona la minimización de datos está descrito en la documentación abierta. |
| Infraestructura de despliegue | Contiene la configuración de los servidores. Publicarla sería dar un mapa a quien ataque. |

Ninguno de los componentes cerrados determina quién es earthling ni cómo se cuenta el voto. Eso lo determina el contrato inteligente abierto.

## Qué se puede verificar ahora mismo sin confiar en nosotros

- **Las reglas del pasaporte.** Leer el código fuente del contrato en el repositorio: el pasaporte es intransmisible, uno por monedero, y su titular puede quemarlo él mismo.
- **Cuántos pasaportes se han emitido.** Llamar a `totalSupply` del contrato. Esa cifra no la decimos nosotros: la dice la cadena de bloques. Pero hay que leerla correctamente, y explicamos cómo. **Ahora hay allí cuatro asientos de prueba**, hechos al depurar el sistema antes de su puesta en marcha, y entre ellos no hay participantes reales. **Desde el 22 de octubre de 2026 hasta el día de la adopción del texto**, esa cifra significa las personas que han verificado su identidad y participan en la constitución: earthlings lo serán solo tras la adopción de la Declaración. **Tras la adopción**, el número de pasaportes emitidos es el número de earthlings.
- **Si una dirección concreta tiene pasaporte.** Llamar a `balanceOf`. La respuesta es 1 o 0.
- **Las votaciones de la DAO.** Abrir el espacio en Snapshot y ver las propuestas, los votos y las firmas. Cada voto está firmado con el monedero de quien vota: nosotros no podemos ni añadir un voto ni falsificar el de otro.
- **El derecho de voto.** Snapshot consulta a nuestro servidor si una dirección tiene pasaporte. En ese paso hay que confiar en el momento de la votación, pero no después: las direcciones de todos los que han votado son públicas, y cualquier persona puede comprobar cada una de ellas por sí misma en el contrato de Polygon. Una discrepancia se vería.

El último punto lo describimos de manera expresa porque es uno de los dos lugares en los que hay que confiar en nosotros. Preferimos nombrarlos nosotros mismos y no dejarlos como hallazgo para quien verifique.

El segundo lugar son las claves del propietario del contrato. En la versión desplegada del contrato, las funciones de emisión y de destrucción del pasaporte están a disposición del propietario, y la clave del propietario está ahora en manos del fundador. La Carta, artículo 21, admite la destrucción contra la voluntad del titular por un solo fundamento - la anulación de una emisión inválida - y solo con un procedimiento: notificación, plazo para objetar, dictamen del Consejo, votación secreta con mayoría reforzada, recurso. En el código esas garantías no están: son procedimentales. Es decir, ahora se sostienen en nuestra palabra y no en la técnica, y lo reconocemos. Qué se está haciendo al respecto: separar los derechos de emisión y de destrucción en papeles distintos, poner un retardo a la ejecución de la destrucción y traspasar la titularidad a una firma múltiple de seis firmantes elegidos. Los plazos están en la [Hoja de ruta](https://earth-lings.org/documents/es/es19-hoja-de-ruta.html).

## Qué no hay todavía

Lista honesta de lo que se ha declarado como principio pero aún no está hecho:

- El código fuente del contrato está publicado en el repositorio, pero **todavía no está verificado en el explorador de la cadena de bloques**. Eso significa que la correspondencia entre el código fuente publicado y el bytecode desplegado hay que comprobarla por ahora uno mismo. La verificación está en curso.
- **No se ha realizado una auditoría independiente de seguridad.** Está prevista antes de ampliar las operaciones.
- **Los contratos inteligentes de la Tesorería no están desplegados.** Está desplegado solo el contrato del pasaporte; la economía interna de la participación se lleva por ahora en la contabilidad de la plataforma.
- El canal público de votación **está desplegado y funciona técnicamente, pero por él no han pasado todavía votaciones de fondo**.
- El programa de búsqueda de vulnerabilidades (bug bounty) está anunciado como principio, pero **todavía no está abierto**.
- **Los derechos del propietario del contrato no están separados ni traspasados.** La emisión y la destrucción del pasaporte están a disposición de una sola clave, no hay retardo de ejecución y la clave está en manos del fundador. Las limitaciones del artículo 21 de la Carta rigen de manera procedimental.
- **Todavía no hay firma múltiple en el monedero de la caja.** El umbral de firmas es de una; eso se comprueba en la dirección del monedero. El paso a una composición de seis firmantes es criterio de tránsito entre fases.

## Derecho de reproducción

El registro de pasaportes vive en la cadena de bloques y no en nuestros servidores, y el código del contrato es abierto. De ahí se sigue algo práctico: si la infraestructura se detiene o su funcionamiento resulta capturado, la comunidad puede construir una plataforma nueva contra ese mismo registro. Se trasladan las personas y sus pasaportes; la capa de servidor es sustituible.

La reproducción tiene dos apoyos, y el segundo no es menos importante que el primero. El registro da la continuidad de las personas, y la **especificación publicada** da la posibilidad de volver a montar el instrumento: las reglas, los umbrales, los quórums, los plazos y los procedimientos están expuestos por completo en la Carta, en la Tesorería y en los presentes documentos. Por eso no se reproduce nuestro código, sino el sistema descrito. Copiar la parte cerrada de servidor no hace falta y no hará falta.

Por eso la opacidad de la parte de servidor no suprime el derecho del pueblo a continuar sin los fundadores. Los rasgos de una continuación legítima - núcleo intangible conservado, voluntad de las personas verificadas y continuidad de los procedimientos - están descritos en el documento [Hoja de ruta del período de transición](https://earth-lings.org/documents/es/es19-hoja-de-ruta.html).
