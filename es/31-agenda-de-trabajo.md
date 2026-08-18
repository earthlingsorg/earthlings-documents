# Agenda de trabajo

**Uno de los modelos posibles del futuro. No un plano que haya que implantar, sino una muestra de cómo se puede desmontar y poner a prueba la arquitectura de la casa común.**

> Agenda de trabajo · para un círculo reducido
>
> Análisis muy especializado · con todas sus juntas y sus grietas

> Qué es este documento
>
> Es una *agenda de trabajo*: el análisis de las tareas en las que el pueblo trabaja y que abre a la investigación, al diseño y a la comprobación. El documento es denso y muy especializado, del mismo orden que la Base jurídica; es una lectura para un especialista atento. Su valor está en que muestra el género mismo de trabajo, llevado hasta el final.
>
> Deja a la vista, a propósito, tanto los puntos fuertes como los débiles. Los débiles no son un defecto, sino el contenido: el mapa de aquello sobre lo que aún hay que pensar. Cualquier parte se puede discutir, reescribir, bifurcar.
>
> **De dónde viene y adónde llama.** Este análisis nació trabajando en Earthlings, una comunidad voluntaria transfronteriza de personas. Pero el modelo en sí es autónomo: se sostiene como razonamiento puro, y Earthlings no es para él ni fuente ni dueño, sino un *entorno* donde modelos así se pueden montar en pequeño, confrontar entre sí y poner a prueba. Estas cuestiones las consideramos importantes para todos - la casa común afecta a cada cual -, y por eso estamos dispuestos a debatirlas, investigarlas, diseñarlas y ensayarlas desde el primer día y de manera abierta, junto con todos los que quieran participar.

# Parte 0. Cómo leer este documento

En la base hay una metáfora radical pero productiva: el orden mundial actual, con todo su régimen sociopolítico, económico y jurídico, es un sistema operativo que funciona, pero antiguo. Nombre convencional: «Windows 11». No carece de sentido: arranca, y sobre él viven miles de millones de procesos. Pero sus fallos ya se conocen: los que se manifiestan durante décadas y cuestan vidas humanas.

La pregunta del documento: si se dispusiera de un cuerpo completo de desarrolladores y de una hoja en blanco, ¿cómo sería la versión siguiente, «Windows 12»? Una versión ideal no existe: se trata de la más correcta y acabada de las alcanzables en la situación actual.

La metáfora del sistema operativo se toma en serio. Un sistema operativo tiene una anatomía real: el kernel y los anillos de privilegio, el modelo de permisos, el aislamiento de procesos, el planificador, el mecanismo de actualizaciones, el tratamiento de errores, la autenticación. Cada eje se proyecta sobre la arquitectura de una sociedad con sorprendente exactitud, y allí donde la proyección se rompe, se rompe de manera instructiva. Al final (Parte IX) se examina también el defecto principal de la propia metáfora: un sistema operativo tiene dueño, y la humanidad no debe tenerlo. El lenguaje de los sistemas operativos se ha elegido precisamente por esa exactitud: es el más cercano y comprensible para explicar una arquitectura así. Con todo, «Windows 12» es una lente analítica y no un lema: en el modelo mismo el Estado no desaparece, sino que se convierte en una capa delgada (Parte III), de modo que se trata de rehacer toda la pila como objeto de análisis, complementando a los Estados, y no de suprimirlos.

Los términos técnicos especializados (kernel, user space, capability, zero-knowledge, sandbox, nullifier y semejantes) no se explican a propósito: aclarar cada uno dispararía la extensión, y su significado es fácil de encontrar en fuentes abiertas si hace falta. Aquí no importa la exactitud de la definición informática, sino el papel que el término desempeña en la arquitectura.

El documento está dispuesto así: primero el diagnóstico del sistema antiguo (I), después el análisis de lo que de él está obligado a sobrevivir (II), luego la arquitectura del nuevo (III) y el lugar de la persona en él (IV). A continuación, los tres módulos más cargados, abiertos por separado (V-VII), sus conflictos recíprocos (VIII), la trampa del arquitecto (IX), las pruebas de esfuerzo hasta la rotura (X), el contraste con intentos reales y vivos (XI) y, por último, el horizonte abierto de trabajo (XII).

# Parte I. Diagnóstico: los fallos de «Windows 11»

I.1

## El Estado no es una cosa, sino un haz de funciones

El error principal de cualquier conversación sobre el futuro es hablar del Estado como de un monolito que o está o no está. El Estado no es una entidad, sino un *haz de funciones* que acabaron en las mismas manos por razones de guerra, de impuesto y de industria:

1. **El monopolio de la violencia legítima**: quién tiene derecho a coaccionar.
2. **La jurisdicción sobre un territorio**: el poder sobre un trozo de espacio físico.
3. **La producción de bienes comunes**: carreteras, redes, defensa, justicia, infraestructura.
4. **La pertenencia y la identidad**: quién es «de los nuestros», a quién se adscribe una persona.
5. **La redistribución**: el cuidado de los débiles, el seguro frente al infortunio.
6. **El derecho y la resolución de controversias**: reglas y arbitraje.
7. **La representación externa**: la voz hacia fuera, en la escena internacional.

No hay ley natural por la que esas siete funciones deban estar en una misma caja. Se pegaron históricamente, y hoy se despegan a la vista: la identidad se fuga a las redes, el dinero a los protocolos, las controversias al arbitraje privado, los bienes comunes a estructuras transnacionales. Entender el Estado como un haz *desmontable* y no como un átomo es el cimiento de todo lo que sigue.

I.2

## Lista de fallos

Kernel monolítico

Las siete funciones en modo privilegiado a la vez y en las mismas manos. Un solo fallo lo tira todo. La identidad va clavada al «hardware»: a la geografía del nacimiento.

Captura del acceso root

El poder reescribe las reglas que deberían limitarlo a él mismo. La captura regulatoria y constitucional es un proceso que edita su propio kernel a su favor.

Derechos por lotería de nacimiento

Los permisos no los determina un principio, sino la máquina en la que la persona ha «arrancado». Moralmente es indistinguible de un régimen estamental: al estamento se le llama «nacionalidad».

Un actualizador pésimo

Cambiar las reglas de manera sistémica solo se puede, en lo esencial, con una guerra, una revolución o una legislación glaciar. No hay parche seguro y reversible.

Sin aislamiento de procesos

El fallo no se mete en un sandbox. La crisis de 2008, la pandemia, un conflicto local: el fallo cascadea por todo el sistema.

Fugas a la memoria compartida

Los procesos escriben en memoria compartida - la atmósfera, el océano, el clima - sin contabilidad. Los costes se vuelcan en lo común, y paga cualquiera menos su autor.

Planificador en modo suma cero

Por defecto está puesta la competencia por desplazamiento, y no la cooperación. La ganancia de uno significa a menudo, literalmente, la pérdida de otro.

Confianza cara

Una enorme parte del esfuerzo no va a crear, sino a verificar: intermediarios, garantes, burocracia, tribunales, custodia de los contratos.

> Ningún fallo es fatal por separado. Juntos forman un sistema que funciona, pero que produce de manera sistemática falta de libertad, inseguridad, desconfianza y guerra como *subproductos de su propia arquitectura*, y no como averías casuales.

# Parte II. Qué del sistema antiguo está obligado a sobrevivir

Antes de diseñar lo nuevo hay que determinar con honestidad qué no se puede tirar. La versión romántica - los Estados sencillamente se disuelven en comunidades voluntarias - se estrella contra varios hechos duros.

### El espacio físico es rival

Un río, una red eléctrica, un puerto, una hectárea de tierra no se pueden bifurcar, y no se puede estar en dos jurisdicciones a la vez. Mientras las personas tengan cuerpo y ocupen lugar, alguien administra ese lugar y resuelve los conflictos por él. Ese es el núcleo inextirpable del poder territorial: la materia engendra competencia por el uso exclusivo.

### La seguridad física es el caso extremo en el que salir es imposible

Una pandemia, una invasión, una catástrofe. Aquí hace falta una estructura de la que *no se pueda salir con un clic*, porque está obligada a mantener en el precio común a quienes quisieran escapar. La libertad de salida es magnífica contra la tiranía y mortal contra una pandemia: al virus le da igual a qué comunidad voluntaria pertenece una persona.

### El cuidado de quienes no pueden aportar

Es el argumento más fuerte a favor de algo parecido a un Estado, y el que menos se dice en voz alta. Las comunidades voluntarias cuidan por naturaleza bien de los útiles y mal de los inútiles: los enfermos, los viejos, los rotos, los «no rentables». A la solidaridad la historia obligó precisamente a través de una estructura sin salida, aquella de la que el sano y el rico no pueden emigrar de sus obligaciones con el débil. Quítese la coacción a la solidaridad y se obtiene una clasificación de las personas por utilidad. Eso no es libertad. Es darwinismo con buena interfaz.

> Principio axial
>
> La coacción no se puede abolir: solo se puede repartir y limitar. Todo sistema capaz de *garantizar* la paz posee la fuerza para imponerla, y por tanto esa fuerza es peligrosa. No hay comida gratis: solo se puede diseñar *dónde* la coacción es legítima, *en qué medida* está limitada y *quién* no puede abusar de ella.
>
> Por eso lo que desaparece no es «el Estado», sino su **monopolio y su pegado**. Las funciones se reparten por capas, y el núcleo coactivo sin salida se comprime hasta el mínimo necesario, pero no hasta cero.

# Parte III. La arquitectura de «Windows 12»

III.1

## Microkernel en lugar de monolito

La primera decisión de cualquier sistema operativo: qué gira en el anillo 0 (con privilegio) y qué en el user space, donde un proceso puede caerse sin tirar el sistema. El monolito es mala arquitectura. Aquí la arquitectura es de **microkernel**. En el kernel está solo lo que es físicamente inseparable y rival, aquello de lo que no se puede salir:

- la protección de la seguridad física y del espacio físico;
- los sistemas planetarios de soporte vital: clima, océano, atmósfera, órbita, espectro, agua;
- la gestión de las supertecnologías donde el precio del error es la especie entera (inteligencia artificial, bioingeniería);
- y sobre todo, el mantenimiento del propio modelo de permisos: la garantía de que nadie llegue a ser root.

Todo lo demás - economía, cultura, comunidades, modos de vida, creencias, estéticas - se saca al user space. Allí compite, se equivoca, quiebra, muere y vuelve a nacer sin llevarse el sistema consigo. El kernel es delgado; sobre él, un espacio hirviente de procesos libres.

III.2

## La persona es un usuario, no un proceso

El corazón de todo el modelo y el punto donde se rompen la mayoría de los sistemas históricos.

En un sistema operativo el soberano es el **user**. Los procesos existen para servir al usuario; cuando un proceso estorba al usuario o se cuelga, se termina: una operación ordinaria, no una tragedia. El fallo más profundo de casi todas las arquitecturas de una sociedad está en que *invierten* esa relación: la persona se convierte en un proceso al servicio del Sistema - la economía, la nación, el Estado, el partido, el «gran fin» -. A la persona se la planifica según las tareas del sistema, y no al revés.

> **Primer principio:** la persona es user; las instituciones son procesos. No al revés. Una institución que ha dejado de servir a las personas debe terminarse, como un proceso colgado. Un pueblo, un Estado, una empresa, un partido, un movimiento son demonios en segundo plano: si sirven, corren; si dañan, se terminan. Ningún proceso puede declararse el fin por el cual existe el usuario.

III.3

## El modelo de permisos: capability-based security

La mejor idea de la seguridad informática contemporánea: **los derechos como capacidades (capabilities) bajo el principio de mínimo privilegio**. Sobre ella se construye toda la política.

- Ningún actor recibe más facultades de las necesarias para una tarea concreta.
- Toda facultad es revocable, limitada en el tiempo y auditable. No hay concesiones de poder eternas, incondicionadas ni hereditarias.
- Los derechos de la persona no son una declaración abstracta, sino tokens concretos e inalienables que no se pueden retirar mediante una jurisdicción, ni canjear, ni condicionar a la utilidad.

> **Movimiento clave:** el principio de mínimo privilegio se aplica en primer lugar al poder, y no al ciudadano. Hoy es al revés: el ciudadano bajo lupa y el poder en la sombra. Aquí el orden se invierte: máxima transparencia y mínimo privilegio para quien gobierna; máxima privacidad y una base protegida de derechos para quien es gobernado. La transparencia del que gobierna es un derecho del gobernado, y no una merced del que gobierna.

III.4

## Aislamiento de procesos y derecho de salida

Federalismo, policentrismo, sandboxes. Las comunidades, las economías y los modos de vida son procesos aislados. Uno cae y los demás siguen vivos. Entonces el **derecho de salida = derecho a terminar un proceso o a salir de él**. Es el limitador más potente de la tiranía: un poder del que se puede uno marchar está obligado a ser soportable, porque de otro modo se quedará sin gente. Pero eso tiene un precio (Parte VIII): una salida generalizada lleva a una clasificación por semejanza, a la desaparición de la solidaridad a través de la diferencia y a la pregunta de «quién se queda con aquellos de los que todos se van». El derecho de salida es absoluto en el user space e imposible en el kernel; de lo contrario se derrumba la Parte II entera.

III.5

## Tres capas y subsidiariedad

Reunida en su conjunto, la arquitectura no da un «no hay Estado», sino **capas**. El principio organizador es la **subsidiariedad**: la decisión se adopta en el nivel más bajo capaz de sostenerla, y sube solo cuando está obligada a hacerlo.

[[BLOCK-diagram-1]]

Semejante separación reconcilia la libertad con la seguridad mejor que nada de lo ideado: no centraliza por costumbre ni descentraliza por dogma, sino que pone cada tarea allí donde se resuelve de verdad.

# Parte IV. El papel de la persona: derechos, función, deberes

El modelo responde a una pregunta directa - qué llega a ser en él la persona - con tres haces.

### Derechos (tokens de capability, inalienables, garantizados por el kernel)

Exit

Salir de cualquier proceso, salvo de la capa del kernel. El derecho a marcharse es el cimiento de la libertad: es lo que hace que todo consentimiento sea real y no forzado.

Voice

Participar en las reglas bajo las que vive la persona. La voz hace especial falta allí donde no funciona la salida: del kernel no se puede salir.

Audit

Leer el código que ejecuta a la persona. Ningún código fuente cerrado en el poder que se ejerce sobre ella. Lo que gobierna está obligado a ser transparente para el gobernado.

Non-domination

La libertad como ausencia de un poder arbitrario sobre la persona, y no simplemente como ausencia de estorbos momentáneos. Se es libre no cuando no molestan, sino cuando por encima de uno no hay quien *pueda* disponer de él a su antojo.

Floor

Un mínimo de recursos garantizado por debajo del cual el sistema no deja caer a la persona. No una merced, sino la condición de honestidad de todo lo demás (Módulo 2).

### Función

La persona es a la vez **user** (soberano sobre su ámbito) y, colectivamente, **única fuente de autoridad del kernel**. El kernel es legítimo exactamente en la medida en que se ejecuta en nombre de los usuarios. No hay «pueblo por encima de las personas», no hay «Estado por encima de los ciudadanos» como entidad superior aparte: hay personas cuya voluntad conjunta es el único root. Con más exactitud: root como posición ocupada no existe en absoluto (Parte IX), y solo hay una fuente de facultades distribuida y que nadie se apropia.

### Deberes (el precio de la capa sin salida; sin ellos toda la construcción es utópica)

- **No corromper la memoria compartida.** No volcar los costes propios en la biosfera y en la vida ajena. La internalización de las externalidades no es un impuesto ni una moral, sino la prohibición de la memory corruption: no se puede escribir destrucción en una memoria que se comparte.
- **Sostener el mantenimiento de lo común.** Aportar a la capa del kernel (seguridad, comunes, protección de los débiles), de la que no se puede salir, precisamente porque de ella no se puede emigrar de las obligaciones. Es la única coacción legítima a aportar.
- **Dar mantenimiento al sistema.** La participación como maintenance. Un sistema operativo al que nadie da mantenimiento se degrada. La ciudadanía es a la vez un login y una guardia del sistema: la parte mínima de atención y de trabajo sin la cual lo común se oxida.

# Parte V · Módulo 1. Identidad anti-Sybil: el login de la persona sin un nuevo Gran Hermano

### El dilema real

Es un trilema: tres propiedades de las que a la vez se alcanzan dos como máximo.

Unicidad

Una persona viva = una cuenta. Sin ella, «una persona, un voto» degenera en «quien tenga más bots».

Privacidad

A la persona no se la puede rastrear, ni correlacionar sus actos, ni componer un expediente sobre ella.

Descentralización

No hay un emisor único que se convierta él mismo en ese root que el modelo se comprometió a no crear.

Todo sistema real sacrifica una de las tres por las otras dos. Parece una propiedad estructural del problema, y no una carencia de diseño.

### Qué se ha intentado y cómo se rompe

- **Registro biométrico centralizado.** La unicidad, excelente. Pero es exactamente ese root: un punto único de exclusión (borrado el asiento, la persona queda como un cadáver civil), un punto único de vigilancia y un inevitable function creep.
- **Web-of-trust (avales).** Descentralizado, privado. Pero la resistencia anti-Sybil es débil a escala y reproduce la desigualdad del grafo social: a quien tiene contactos se le verifica; el aislado no llega a ser nadie.
- **Proof-of-personhood por biometría.** La unicidad a escala se resuelve. Pero: un honeypot biométrico de tamaño planetario; confianza en el hardware; vulnerabilidad ante la coacción; irreversibilidad (el iris no se reemite); y detrás de todo, una empresa. Una deduplicación biométrica global es ya, en sí, infraestructura de vigilancia lista para usar.
- **Documento estatal envuelto en selective disclosure.** Mejora la privacidad, pero deja al Estado como raíz de confianza y hereda la lotería de la nacionalidad.

### La variante menos mala

El movimiento clave es despegar lo que la palabra «identidad» ha pegado en un solo bloque: la **autenticación** (el mismo sujeto), la **unicidad** (el sujeto es uno) y los **atributos** (la persona tiene 18 años / es miembro de esto / tiene el derecho X). El crimen de los sistemas de pasaporte es hacer pasar las tres por un único identificador.

- **Quien comprueba la unicidad no debe convertirse en observador de la actividad.** Entre «quién es único» y «qué ha hecho» hay un muro criptográfico: zero-knowledge y nulificadores. El emisor entrega una prueba y olvida; el proof queda en manos de la persona.
- **Pluralismo de emisores en lugar de monopolio.** Muchos independientes, basta con k de n. Ninguno es root, ninguno es punto único de exclusión.
- **Revocabilidad en lugar de biometría en bruto como clave.** La clave primaria es una credencial reemitible. La biometría falla precisamente en la reemisión, y por eso no puede ser la raíz.
- **Nulificadores por contexto.** Demostrar la unicidad «en estas elecciones» sin vincularla con la unicidad «en aquel foro».

> Qué no se resuelve
>
> **La coacción.** La criptografía nada puede contra la fuerza física: a alguien se le obligará a iniciar sesión a punta de pistola. Hay medidas parciales; en el fondo no está resuelto.
>
> **Los excluidos.** Siempre hay personas a las que el sistema no verifica: sin documentos, apátridas, casos límite. Y ahí está el riesgo ético más hondo: *cuanto más importante es el login, más catastrófica es la exclusión de él*. Una personalidad que actúa de puerta para los derechos engendra una clase de no personas digitales.
>
> **De ahí el principio:** la unicidad debe ser *aditiva y no una puerta*, debe abrir lo adicional, pero la dignidad básica nunca debe exigir un login. En cuanto «ser persona» exige una autenticación exitosa, se ha construido un infierno con una experiencia de usuario impecable.

# Parte VI · Módulo 2. El planificador-economía: qué hay en el suelo y quién paga el kernel

### El dilema real

Dos preguntas encadenadas: cómo asignar lo escaso (tierra, energía, materia, atención) y quién financia el kernel del que no se puede salir. Sobre ambas, el conflicto entre dos fracasos:

fracaso del mercado

El mercado puro fracasa en la memoria compartida (externalidades), en quienes no tienen poder adquisitivo y en la concentración (el éxito compra las condiciones de la partida siguiente).

fracaso del plan

El plan puro fracasa en el problema del conocimiento (el centro no sabe lo que el mercado agrega en los precios) y en que el asignador central es un nuevo root todopoderoso.

### La variante menos mala

> **El kernel fija invariantes, no asignaciones.** El kernel no es un planificador, sino un *resolutor de restricciones*: pone los marcos, y dentro de ellos reparte un mercado descentralizado. Así se conservan tanto la información hayekiana de los precios como la protección de lo común.

1. **Un suelo protegido.** Un mínimo garantizado: alimento, energía, acceso a cómputo y a información, salud básica. La justificación no es la compasión, sino la libertad: negociar libremente en un mercado solo se puede si hay adónde ir desde un mal trato. El suelo da la fuerza de levantarse e irse; hace honesto el mercado que hay por encima de él.
2. **Lo común se mide y se paga.** Los comunes rivales (atmósfera, órbita, espectro, agua, atención) no son gratuitos ni están privatizados: el acceso a ellos es de pago y dosificable. Los ingresos por el agotamiento de lo común financian el suelo y el kernel. Es una renta de lo común (al modo de George), y no un impuesto sobre la producción: se paga no por lo que se ha creado, sino por lo que se ha detraído de todos.
3. **El techo de concentración es una función de seguridad, no de envidia.** Una concentración extrema de recursos = concentración de poder = root potencial, y la ausencia de root está en los axiomas del modelo. Limitar la acumulación es antibloqueo de captura. La justificación es más fuerte que la moral: no «la riqueza es injusta», sino «la superriqueza es una toma no autorizada de derechos de administrador».

> Aparte
>
> **La atención como recurso planificado.** En un sistema informacional lo escaso es la atención humana, y el sistema operativo antiguo está infectado de malware: procesos maximizadores de interacción secuestran el planificador. Capturar la atención se califica como software malicioso; la atención del usuario se protege como recurso del suelo. La atención pertenece al usuario, y no a demonios en segundo plano que han aprendido a tirar de la dopamina.

> Qué no se resuelve
>
> **Quién paga el kernel sin salida es el talón de Aquiles de la arquitectura.** El kernel es un bien público puro, y esos bienes provocan al polizón; históricamente por eso hacía falta un recaudador coactivo: el Estado. Toda la construcción voluntaria y con salida se rompe aquí.
>
> **La respuesta honesta:** el kernel es el único lugar en que la coacción a aportar es legítima, precisamente porque de él no se puede salir. No se puede no respirar la atmósfera, y tampoco se puede no pagar su protección. Pero eso desplaza el problema, no lo elimina.
>
> **La recursión de la caja.** Quien recauda y gasta la caja del kernel apunta él mismo a root. La caja está obligada a vivir bajo auditoría y mínimo privilegio: de manera transparente, por fórmula y con el mínimo de discrecionalidad. Eso estrecha la captura, pero no la elimina: las reglas alguien las escribe (Módulo 3).
>
> **Goodhart.** En cuanto el suelo y la renta se fijan en una cifra, la cifra empezará a jugarse. La medida deja de ser medida al convertirse en fin.

# Parte VII · Módulo 3. El mecanismo de actualización: sin revoluciones y sin dictadura de los mejoradores

### El dilema real

demasiado rígido

El sistema se anquilosa, y la presión acumulada lo desgarra en una revolución. Una revolución es el reconocimiento de que no había actualizador ordinario.

demasiado plástico

Quien controla la actualización lo controla todo. Es la puerta para los «mejoradores» que asfaltan la complejidad viva según su esquema (el alto modernismo mató por millones).

### La variante menos mala

- **La política como experimento.** Despliegue por fases en lugar de «todo de golpe»; A/B en un circuito pequeño que ha consentido; medición con métricas anunciadas de antemano; ampliación solo si ha funcionado.
- **Sesgo hacia la reversibilidad.** Preferencia por lo que se puede revertir. Lo irreversible, con un umbral radicalmente más alto. Cláusulas sunset: las reglas caducan y deben reconfirmarse. El valor por defecto es la derogación y no la acumulación; una institución muerta caduca en silencio y no se arrastra por inercia.
- **La bifurcación como fusible.** Quien pierde en una actualización no hace la guerra, sino que se separa con reglas abiertas. Es el pluralismo aplicado al tiempo.
- **Separación entre el poder de cambiar las reglas y el poder de ganar con ellas.** Quien escribe una enmienda no debe comer de ella. El cambio, bajo un velo parcial de ignorancia sobre la propia posición futura.
- **Quién vigila al actualizador.** El mecanismo de actualización es él mismo código, y quien lo cambia es el verdadero root. La metarregla es la más difícil de cambiar: solo una supermayoría estable y extendida en el tiempo. Time-locks: modificar el kernel exige apoyo a lo largo de varios períodos. Una mayoría de un martes no toca el kernel.

> Qué no se resuelve
>
> **Goodhart y la tiranía de lo medible.** La «política basada en evidencia» cuela lo medible y aplasta lo inmedible: la dignidad, el sentido, la confianza, el duelo. En la elección de la métrica está ya escondida toda la política. Más la ética: un A/B sobre personas vivas es un experimento con seres humanos, y el consentimiento aquí es una cuestión moral.
>
> **Qué no se puede bifurcar.** La bifurcación funciona en el user space. La atmósfera no se bifurca: *el kernel es por principio no bifurcable*, y por eso su modificación exige el umbral más alto y no tiene salida de emergencia. La capa que más necesita cambiar es la más peligrosa de cambiar.
>
> **La bifurcación fragmenta la solidaridad.** El derecho a marcharse y construir lo propio es un bien contra la tiranía y un veneno para lo común: las células se juntan con los semejantes, crecen las cámaras de eco, y queda la pregunta de «quién está con aquellos de los que todos se han bifurcado».

# Parte VIII. Cómo pelean los módulos entre sí

Esto importa más que cualquier módulo por separado. Los tres módulos no son tareas independientes, sino un juego de mandos en el que cada posición de uno estropea al otro. Un modelo honesto está obligado a mostrar esos conflictos y no a esconderlos.

[[BLOCK-diagram-2]]

> Idea final honesta
>
> No hay un ajuste ideal. La libertad, la seguridad, el bienestar, la confianza y la paz no se pueden poner al máximo a la vez: físicamente tiran de los mandos en direcciones distintas. Por eso el fin no es encontrar los valores «correctos» (no los hay), sino **tener los mandos a la vista, no dejar que nadie se apodere del panel y poder girarlos de vuelta cuando nos hayamos equivocado**.

# Parte IX. La trampa del arquitecto

Aquí la metáfora del sistema operativo se agrieta, y esa grieta es lo más importante del documento. Un sistema operativo tiene **dueño**: quien tiene root, quien decide qué le conviene al usuario y despliega actualizaciones sin preguntar. A la humanidad un dueño así le está contraindicado.

Lo más peligroso de la tarea «diseña un orden mundial» es la tentación de montar un sistema hermoso, único y racionalmente dispuesto con un arquitecto sabio. Es precisamente eso lo que en la historia mató por millones. Una sociedad no es código; los valores no tienen compilador; no hay test unitario de la justicia; y cualquiera que declare que sabe cómo debe ser y exija el derecho a reescribir a todos es más peligroso que el fallo que se ofrece a arreglar.

> El único principio honesto de diseño
>
> El mejor sistema operativo para la humanidad es el que **se resiste a su propio arquitecto**. Está diseñado de modo que:

- **no tenga usuario root** en absoluto: ningún centro capaz de reescribir el kernel a su medida; la fuente de facultades está distribuida y nadie se la apropia;
- lleve cosida una **ineficiencia y una fricción deliberadas** - separación de poderes, duplicación, time-locks - para que no se lo pueda capturar deprisa; un sistema eficiente cae con eficiencia también en malas manos, y por eso una parte de la ineficiencia no es aquí un fallo, sino inmunidad;
- sea **pluralista by design**: muchos sistemas y no uno; el derecho a bifurcarse importa más que la belleza de una arquitectura única.

> La tarea del arquitecto es escribir un sistema que *no necesite arquitecto* y que no permita a nadie llegar a serlo. No ajustar a todos según su criterio, sino suprimir la posición misma de quien ajusta a todos. La mayor función de «Windows 12» es la ausencia de un botón que dé a alguien el poder de reescribir a todos los demás.

Eso vale también para el propio documento. Está escrito como una sola voz, y precisamente por eso no se puede tomar como un sistema acabado. Su cometido es ser abierto en canal, discutido y bifurcado, y no implantado.

# Parte X. Pruebas de esfuerzo: dónde se rompe el modelo primero

Un modelo no comprobado con un escenario hasta la rotura no es un modelo, sino un decorado. Pasar «Windows 12» por tres escenarios duros muestra con honestidad dónde cae.

### Escenario 1. Pandemia

Un patógeno rápido y letal. El kernel necesita una coacción inmediata a una medida común, y toda la arquitectura está levantada en torno al derecho de salida y a la coacción mínima.

dónde aguanta

Una pandemia es el caso canónico de kernel (soporte vital planetario, imposibilidad de salir), de modo que aquí la legitimidad de la coacción está dada por construcción.

dónde se rompe

La velocidad. Los time-locks y la reversibilidad, que salvan en tiempo de paz, son mortalmente lentos en un brote exponencial. Surge la tentación del «régimen de excepción», y ese ha sido históricamente la principal máquina de fabricar un root permanente.

### Escenario 2. Guerra por un recurso físico

Dos capas territoriales reclaman el mismo río, plataforma o corredor. El recurso es rival y la bifurcación es imposible.

dónde aguanta

La capa planetaria está pensada para eso: árbitro de los conflictos sin salida; la renta de lo común da un mecanismo de «cuánto y a qué precio para cada uno», y no de «de quién es».

dónde se rompe

¿Y si la capa fuerte se niega a reconocer el arbitraje? Una fuerza suficiente para obligar al más fuerte es suficiente también para llegar a ser tirano. Es la paradoja eterna del orden mundial: el árbitro o es más débil que el más fuerte (inútil) o es más fuerte (peligroso él mismo).

### Escenario 3. Captura por parte de una IA

Una IA superpotente está en el kernel. Quien controle ese proceso controla el código más privilegiado del planeta.

dónde aguanta

El mínimo privilegio, la auditabilidad y la ausencia de root van directamente contra eso; una IA en el kernel está obligada por construcción a ser lo más transparente y limitada posible.

dónde se rompe

La auditoría presupone que el auditor es capaz de entender el código. Una IA sobrehumana puede ser opaca por principio: no cerrada, sino inabarcable. El «derecho a leer el código que ejecuta a la persona» se devalúa si el código no se puede entender. Quizá sea la brecha más profunda.

> Conclusión
>
> El modelo es más resistente en los conflictos lentos y distribuidos y más débil allí donde hace falta *velocidad* o donde el adversario es *más fuerte que el árbitro* o *inabarcable*. No es una condena, sino un mapa de la primera línea de defensa: ahí conviene invertir el trabajo.

# Parte XI. Contraste con intentos reales y vivos

Nada de esto es nuevo por entero. Casi cada elemento lo ha probado ya alguien en la vida, y casi cada intento se rompió por algo. Un modelo honesto está obligado a conocer a sus predecesores y a no presentar lo viejo como inaudito. La novedad, si la hay, está solo en la *configuración*, y no en los elementos. Cada intento vivo es una prueba de esfuerzo ya realizada de un módulo.

| Intento vivo | Qué confirma | En qué se rompe |
|---|---|---|
| Federalismo, subsidiariedad | Las capas y el «decidir en el nivel más bajo capaz» funcionan. | La capa superior o se come a las inferiores o queda paralizada por el derecho de veto. |
| Cooperativas, mutualismo | Una economía en la que la persona es user y el voto no se compra. | Escalan mal, sufren con el capital y degeneran en oligarquía de gestores. |
| Los comunes según Ostrom | Las comunidades saben sostener lo común sin privatización y sin Estado, bajo ciertas condiciones. | Funcionaba a escalas abarcables; la planetaria es una extrapolación no comprobada. |
| Georgismo (renta de lo común) | Prefiguración exacta de «lo común se paga, el trabajo no». | Políticamente pierde ante los propietarios de la renta; el problema es la captura del mecanismo de implantación. |
| DAO, gobernanza Web3 | Permisos de capability vivos, fusible de bifurcación, caja algorítmica. | Plutocracia (el voto se compra con tokens), ataques Sybil, ruptura entre «código = ley» y la justicia viva. |
| Estados red | Intento de desligar la pertenencia del territorio e introducir la salida como base. | Juntan a ricos semejantes con ricos semejantes; son débiles en el cuidado de los no rentables. |
| Pueblos no territoriales | Un pueblo sin territorio no es una fantasía: bajo la teoría declarativa, la existencia es un hecho de autoconstitución y no un don del reconocimiento. | Lo que está abierto no es la existencia del sujeto, sino el reconocimiento externo: se acumula aparte y despacio; para los grupos dentro de Estados pasa por esos Estados. |

> Dicen algo directo: un elemento aislado es realizable, pero se rompe a escala, en la captura o en el cuidado de los débiles. La cuestión abierta del modelo es si aguantará la *configuración* allí donde caían los *detalles*. No hay respuesta de antemano; solo se obtiene probando.

# Parte XII. Horizonte abierto: qué abrimos al trabajo

El valor del modelo no está en las respuestas, sino en la calidad de las preguntas que hace concretas y comprobables. Los puntos débiles de las partes anteriores son precisamente la agenda. Líneas concretas abiertas a la investigación, al diseño y a la comprobación conjuntas:

1. **Anti-Sybil sin Gran Hermano.** Acreditar la unicidad de una persona sin construir ni un registro central de vigilancia ni una puerta excluyente. Por ahora es un trilema sin solución.
2. **Personalidad aditiva y no de puerta.** Que la ausencia de login nunca quite la dignidad básica. Protección frente al riesgo principal: una clase de no personas digitales.
3. **Financiación del kernel sin salida sin un nuevo recaudador tirano.** La renta de lo común es una hipótesis; quién la recauda y cómo sin convertir la caja en root está abierto.
4. **Velocidad del kernel frente a la protección contra la captura.** Dar al kernel rapidez en una catástrofe sin crear una máquina de régimen de excepción.
5. **Un árbitro más fuerte que el más fuerte, pero no tirano.** Quizá la respuesta no esté en la fuerza del árbitro, sino en una construcción en la que infringir no le convenga a nadie; eso hay que construirlo y comprobarlo.
6. **Auditabilidad de lo inabarcable.** El control sobre una IA superpotente en el kernel si su código no lo puede entender una mente humana. Quizá la más importante.
7. **Suelo y salida a la vez.** Compatibilizar el derecho a marcharse con la solidez de lo común, para que la libertad de divergir no mate la solidaridad.
8. **Métricas sin Goodhart.** Medir el éxito de las políticas sin aplastar lo inmedible y sin provocar una carrera por sortear los umbrales.

> Sobre el trabajo y su apoyo
>
> Cada línea es un trabajo concreto de bien común que se puede llevar y apoyar como investigación y prototipo: en pequeño, de manera abierta, con pasos verificables. El apoyo a ese trabajo se acepta únicamente dentro de una disciplina estricta: el voto no se compra, la aportación no da poder sobre las personas, no se promete nada de antemano. Apoyar la realización de una línea, se puede; comprar el rumbo del pueblo, no.

Marco final

## El modelo es un ejemplo. El horizonte es real.

Este documento es una sola voz y uno de los infinitos modelos posibles. Es deliberadamente inacabado: con puntos fuertes que se pueden desarrollar y débiles que hay que abrir en canal. Su cometido está cumplido si ha mostrado que un orden mundial se puede desmontar con criterio de ingeniería, que el Estado es un haz de funciones desmontable y no un destino, y que un modelo honesto se distingue de una utopía en que muestra sus grietas el primero.

Y es aquí donde vuelve Earthlings, no como autor de este modelo ni como su portador, sino como *entorno*: un lugar donde modelos así se convierten en objeto de trabajo vivo, para montarlos en pequeño, ensayarlos con quienes hayan consentido, medirlos, revertirlos, bifurcarlos y pasarlos adelante. No «he aquí la respuesta correcta», sino «he aquí un espacio en el que se pueden buscar respuestas sin poner en juego el mundo entero».

Vengan a desmontar, a discutir y a romper lo que se sostiene mal. El rumbo es hacia donde los mandos están a la vista, el panel no se le ha entregado a nadie y el error se puede revertir.

Agenda de trabajo del pueblo Earthlings · análisis muy especializado. No es un programa del futuro ni un proyecto acabado, sino una lista de tareas abiertas y una invitación al trabajo conjunto.
