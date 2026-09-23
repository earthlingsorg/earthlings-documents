# Plateforme numérique des Earthlings

**L'infrastructure d'identité, de participation et de projets du peuple des Earthlings**

> Le présent document décrit la réalisation technique des règles établies par la Charte des Earthlings. En cas de divergence, la Charte s'applique, et en cas de divergence entre la Charte et la Déclaration, la Déclaration. La plateforme n'établit pas de règles: elle les exécute.

---

# SECTION 01. L'objet de la plateforme

La Plateforme numérique des Earthlings est le noyau où se rejoignent quatre niveaux du peuple:

- **l'identité** - vérifiée et pourtant privée;
- **la participation** - signature de la Déclaration, vote, débats, actions communes;
- **les projets et les cellules** - déclenchement, formation, coordination, exécution et consignation des résultats;
- **l'économie de participation** - unité de compte, fonds commun, rémunération de l'apport.

La plateforme n'est ni un réseau social ni un système de chaîne de blocs de plus. C'est l'outil grâce auquel le peuple des Earthlings peut exister: avec une infrastructure transparente et pourtant respectueuse de la personne.

Sa tâche principale est de rendre la participation pratique, sûre et honnête: de la première signature de la Déclaration à la réalisation de projets internationaux complexes.

> **Les limites de la plateforme.** La plateforme ne prend pas de décisions et ne peut pas en prendre. Seule l'Assemblée DAO prend des décisions obligatoires. La plateforme est le niveau d'exécution: elle fournit l'interface, consigne le résultat et le met en œuvre. Aucun de ses composants, aucun mécanisme automatique et aucune personne qui l'exploite n'a le droit de modifier, d'annuler ou de bloquer une décision de l'Assemblée. La Charte entre en vigueur avec l'adoption de la Déclaration (Charte, article 38); jusque-là, il n'y a ni Assemblée DAO, ni Core Nodes, ni Emergency Multisig, ni Conseil indépendant, et le seul pouvoir discrétionnaire de la période constituante à l'égard des textes est la décision de l'auteur de la Déclaration d'incorporer des propositions au texte (document « La période constituante »).

---

# SECTION 02. Les niveaux de l'architecture

L'architecture est bâtie en couches. Chaque couche remplit sa tâche et intervient au minimum dans les autres.

**1. La couche de présentation.** Interfaces web; applications mobiles et API pour les intégrations extérieures - à terme. C'est ici que la personne voit la Déclaration, la carte des participants par pays, le tableau des cellules, les votes, son espace personnel. Priorité à l'accessibilité et à la clarté.

**2. La couche applicative.** Modules fonctionnels: gestion du profil, dépôt d'initiatives, travail des cellules, votes, délégation, gestion des fonds, outils d'IA auxiliaires. Logique métier sans conservation de données de bas niveau.

**3. La couche de données.** Stockage des profils, métadonnées des projets, états des cellules, configurations de la DAO, résultats des votes, journaux d'événements. Principes de minimisation, de séparation et de « ne pas collecter le superflu ».

**4. La couche d'identité et de confiance.** Système propre de vérification d'identité, émission et suivi de jetons d'identité intransmissibles, consignation de la signature de la Déclaration. Cette couche est isolée et protégée au maximum.

**5. La couche d'économie de participation.** Infrastructure de l'unité de compte, fonds commun, répartition des rémunérations, intégration avec les projets et les cellules.

**6. La couche d'intégration avec la DAO.** Interfaces et protocoles par lesquels les décisions de l'Assemblée se reflètent dans le fonctionnement de la plateforme: réglages, accès, paramètres de l'économie, priorités de développement.

Les couches évoluent séparément: on peut mettre à jour la couche applicative sans toucher à l'identité, ou modifier les mécanismes économiques sans toucher au noyau de la DAO.

### Qui exploite la plateforme

L'exploitation technique est assurée par les **Core Nodes**, coordinateurs techniques élus (Charte, article 2). Ils maintiennent l'infrastructure, répondent de la cybersécurité et du soutien technique des votes, mais ne prennent pas de décisions au nom du peuple, ne gèrent pas les finances, n'ont pas de poids particulier dans les votes et ne peuvent pas bloquer les décisions de la DAO. Ils sont révoqués à la majorité simple à tout moment.

L'**Emergency Multisig** (Charte, article 3) a le droit de suspendre le fonctionnement de certains contrats intelligents en cas de découverte d'une vulnérabilité critique ou de cyberattaque. Chacun de ces actes exige un rapport public dans les 48 heures et une confirmation par l'Assemblée dans les 7 jours, faute de quoi il est annulé.

La Charte ne prévoit aucune autre structure dotée de pouvoirs techniques sur la plateforme. Avant l'adoption de la Déclaration, ces organes n'existent pas (Charte, article 38) et, après l'adoption, jusqu'à l'élection des Core Nodes et de l'Emergency Multisig, leurs fonctions sont exercées par voie de procédure (Charte, article 39); les endroits où il faut aujourd'hui faire confiance à ceux qui exploitent la plateforme sont nommés dans le document « Où nous en sommes ».

### Sur l'IA

Pour analyser les initiatives, soutenir les projets et automatiser les tâches répétitives, la plateforme utilisera des modèles d'intelligence artificielle existants; aujourd'hui, elle ne dispose pas de tels outils. À terme, le développement d'un modèle propre, adapté aux tâches du peuple, est envisagé.

Les limites d'emploi de l'IA sont prévues à l'article 3 de la Déclaration: aucun algorithme, aucun code et aucun système d'intelligence artificielle ne peut être la source définitive d'une décision touchant les droits, la dignité ou la situation d'une personne, et aucune technologie ne peut être employée pour manipuler les gens de façon dissimulée ou pour étouffer l'autonomie humaine. D'où trois règles strictes, valables quel que soit le modèle utilisé:

- **L'IA ne décide de rien définitivement** (Déclaration, article 3). La conclusion de l'IA sur une initiative ou un projet est consultative et ne constitue pas un motif de refus; le refus du système automatique lors de la vérification d'identité n'est pas définitif, et le réexamen par un être humain se fait selon la Politique de vérification biométrique.
- **Les motifs sont divulgués.** La personne dont l'IA a marqué l'initiative reçoit un exposé des raisons sous une forme compréhensible, et non un refus sans explication.
- **Un réexamen humain est garanti.** L'auteur de l'initiative a le droit d'exiger un examen par un être humain, et cet examen a lieu dans le délai fixé.

---

# SECTION 03. L'identité: vérification et passeport intransmissible

L'identité est bâtie autour d'un passeport numérique intransmissible (SBT) lié à une identité vérifiée. Une séparation stricte est observée:

- la biométrie et les documents sont traités en temps réel par le système propre de vérification d'identité;
- du système de vérification d'identité, la plateforme reçoit le résultat de la vérification, le numéro de l'inscription du passeport, l'identifiant du participant, le pseudonyme, l'adresse du portefeuille, l'adresse électronique et le pays, mais ni données biométriques, ni prises de vue, ni données du document;
- après la vérification et la signature de la Déclaration, un passeport attestant son appartenance est émis à l'adresse du portefeuille du participant; pendant la période constituante, la signature est suspendue et, à l'issue de la vérification d'identité, il est délivré un document temporaire de participant à la constitution (document « La période constituante », partie 2, point 5);
- une personne, un passeport; le passeport ne se transmet pas, ne se vend pas et ne se retire pas.

### La séparation des axes: identité, voix, économie

L'architecture exige que l'identité, la voix et l'empreinte économique ne se rejoignent pas en un unique point de pouvoir:

- **l'identité** est donnée par le passeport et par la vérification;
- **la voix** découle du statut d'earthling: une personne, une voix;
- **l'activité économique** se reflète dans l'unité de compte et ne donne aucune voix supplémentaire, à aucun volume.

### La destruction du passeport

En règle générale, seul le titulaire détruit son passeport, avec sa propre clé, depuis son propre portefeuille. La plateforme ne conserve pas les clés du participant et n'est techniquement pas capable de faire obstacle à la destruction; nul n'a le droit de détruire le passeport à la place du participant, mais tant que les droits du propriétaire du contrat ne sont pas transférés à une signature multiple, l'émission et la destruction d'un passeport restent techniquement accessibles à une seule clé (document « Où nous en sommes »).

La Charte (article 21) établit deux exceptions et deux seulement, que la plateforme est tenue de prendre en charge et qu'elle n'a pas le droit d'élargir:

1. **l'annulation d'une délivrance non valide** - s'il est établi que le passeport a été délivré en méconnaissance des conditions de délivrance; uniquement par une décision de l'Assemblée à la majorité de sanction, par vote secret, avec droit de recours;
2. **la réémission technique** - à la demande du titulaire lui-même, en cas de perte d'accès au portefeuille ou de migration du contrat; l'appartenance n'est pas interrompue.

Aucun autre motif de destruction du passeport par une personne autre que son titulaire n'est mis en œuvre dans la plateforme, et contre la volonté du titulaire le passeport n'est détruit qu'en cas d'annulation d'une délivrance non valide. Le décès du titulaire ne figure pas parmi les motifs: la plateforme ne dispose pas et ne peut pas disposer d'informations sur les décès, et l'appartenance prend fin par l'effet du décès elle-même, sans décision de quiconque (Déclaration, article 4); le passeport demeure au registre, et la participation qui n'existe plus est prise en compte par le mécanisme d'inactivité (Charte, article 20).

---

# SECTION 04. L'espace personnel et le profil

L'espace personnel est le point de contact principal entre la personne et l'écosystème.

### Les éléments principaux du profil

- le pseudonyme d'earthling - nom public dans l'écosystème;
- le pays de résidence;
- l'état de la vérification d'identité;
- la marque attestant l'existence d'un passeport, sans divulgation de données personnelles;
- les domaines d'intérêt et de compétence - facultativement.

### Les marques de participation

- participation aux cellules;
- participation aux projets: rôle, apport, état d'achèvement;
- participation aux votes - non consignée: la participation d'une personne déterminée au vote n'est pas publiée (section 06);
- marques de reconnaissance reçues.

> **Les marques de reconnaissance n'ont aucun effet** et demeurent exclusivement informatives ([Charte, article 8](https://earth-lings.org/documents/fr/fr05-charte.html)). La plateforme n'a pas le droit d'utiliser les indicateurs de réputation comme condition d'accès à une fonction quelconque.

### Ce qui ne figure pas dans l'espace personnel

Les données de pièces d'identité, la biométrie et les attributs juridiques sensibles ne sont ni affichés ni conservés. Ils restent dans le système de vérification d'identité et ne sont pas conservés après la vérification. La plateforme travaille avec un pseudonyme, une adresse électronique, un pays, une adresse de portefeuille, une marque de passeport et des données d'usage de la plateforme; la liste et les finalités figurent dans la Politique de confidentialité.

Les photographies et les scans ne sont pas conservés; la biométrie n'est traitée qu'au moment de la vérification. Ce qui est exactement conservé pour empêcher une nouvelle inscription figure dans la [Politique de vérification biométrique](https://earth-lings.org/documents/fr/fr16-verification-biometrique.html).

---

# SECTION 05. Les cellules et le flux de projets

La plateforme assure le cycle complet: de la naissance d'une idée à l'achèvement d'un projet.

**1. Demande de projet.** Tout earthling propose un projet depuis son espace personnel. La demande comprend la description du sujet, le but, l'effet attendu, les compétences nécessaires et l'horizon de réalisation. L'analyse initiale peut être effectuée par l'IA - conformité à la Déclaration, à l'éthique et aux priorités - et cette analyse est consultative: elle ne constitue pas un refus, les motifs sont divulgués, l'examen par un être humain est garanti (section 02).

**2. Information des participants concernés.** Après l'analyse initiale, la demande est adressée à ceux dont les compétences déclarées y correspondent: juristes, ingénieurs, développeurs, analystes et autres.

**3. Formation de la cellule.** La cellule se forme de ceux qui ont répondu. Sa taille va de 2 à 6 personnes (Charte, article 23). Si la tâche exige davantage de personnes, on crée plusieurs cellules liées plutôt qu'une seule, encombrante.

**4. Coordination et exécution.** Tableau de tâches, calendriers, canaux de communication, comptes rendus par étape, intégration avec les espaces de stockage de documents et les outils auxiliaires. Les décisions au sein d'une cellule se prennent par consentement; si une objection motivée tirée du dommage, de l'impossibilité d'exécution ou d'un risque sérieux n'est pas levée, la question se règle par un vote de la cellule: la décision est prise s'il y a plus de voix pour que de voix contre; ceux qui se sont abstenus ont participé au vote, mais n'entrent pas dans le compte des voix pour et contre. Le vote est valable si plus de la moitié des participants de la cellule y ont pris part (document « Cellules », section 05).

**5. Achèvement et consignation.** La plateforme consigne le résultat, répartit les rémunérations si elles sont prévues, met à jour le statut des participants et reflète l'apport du projet dans la carte générale de l'activité.

> **Sur la distinction entre cellules professionnelles et cellules de projet.** La Charte ne connaît qu'une forme: la cellule de deux à six personnes. La distinction entre groupements professionnels permanents par compétence et équipes de projet temporaires est un **procédé d'organisation du travail sur la plateforme**, et non une structure distincte du peuple. Il peut être modifié par une décision de l'Assemblée et ne crée ni organe, ni pouvoir, ni représentation: aucune cellule n'a de voix collective et ne s'exprime au nom d'autres participants.

---

# SECTION 06. Vote et délégation

## Un earthling, une voix

Chaque participant qui a signé la Déclaration dispose d'une voix; le passeport confirme cette voix. La voix ne se renforce ni par le nombre d'unités de compte, ni par la position dans les cellules, ni par la réputation. Le poids économique et le droit de vote sont séparés par l'architecture, non par une déclaration d'intention.

**Le droit de vote ne peut être restreint en raison des opinions, du contenu du vote ou à titre de sanction générale** (Déclaration, article 4; Charte, articles 17 et 37). Au titre de l'article 22 de la Charte, une seule mesure s'adresse à la personne - l'avertissement, et il ne retire rien: ni la voix, ni l'accès aux votes eux-mêmes, ni le droit de faire des propositions, ni le droit de créer des cellules et d'y entrer, ni l'accès aux services, ni quoi que ce soit d'autre. Les autres mesures s'adressent à un projet ou à une cellule et ne portent aucune atteinte aux droits d'une personne.

Le seul cas dans lequel la plateforme exécute une suspension de la voix est une décision de l'Assemblée prise en application de l'article 22 bis de la Charte pour une atteinte établie à l'intégrité du vote, pour une durée maximale de 6 mois. La plateforme exécute une telle décision et ne peut ni la déclencher, ni l'appliquer pour un autre motif, ni la prolonger.

## Ouverture et secret

Le vote personnel est secret: le scrutin doit être agencé de manière que personne, y compris ceux qui exploitent la plateforme, ne puisse établir comment une personne déterminée a voté, ni s'en assurer même avec son accord. La participation d'une personne déterminée au vote n'est pas publiée. L'outil de vote secret n'existe pas encore - il est en cours de sélection, et ces règles ne sont aujourd'hui pas respectées partout: dans le canal ouvert des votes, le vote et l'adresse du portefeuille sont publics, et la plateforme conserve les votes exprimés dans les cellules en les reliant au compte (document « Où nous en sommes »; Politique de confidentialité, section 02).

La transparence porte sur les actes des institutions et non sur les données personnelles des gens. C'est pourquoi la plateforme est tenue d'assurer le **vote secret à décompte vérifiable**: le résultat est vérifié par tous, le lien entre le vote et le votant n'est divulgué à personne, y compris à ceux qui exploitent la plateforme. La procédure est établie par la [Charte, article 6](https://earth-lings.org/documents/fr/fr05-charte.html).

La plateforme doit également assurer:

- **jusqu'à la clôture du vote** - le masquage du décompte intermédiaire et la possibilité de voter à nouveau, le dernier vote exprimé étant retenu; un vote personnel sur une question annule la délégation sur cette question;
- **l'ouverture des votes du délégué** - les votes exprimés par le délégué au titre des voix qui lui ont été confiées sont visibles de tous; aucune publication ne fait connaître qui a confié sa voix au délégué.

La Charte exige que soient publiés la question, les options de réponse, les délais, le nombre de personnes ayant le droit de vote, le nombre de votants, le résultat, la preuve du décompte et la manière de recompter le résultat soi-même (article 6). Il n'existe aujourd'hui de preuve du décompte ni pour l'Assemblée ni pour les cellules: elle apparaîtra avec l'outil de vote secret (document « Où nous en sommes »).

## La délégation

La plateforme prend en charge la transmission de la voix, sur un domaine déterminé, à un autre participant. Les exigences de la Charte (article 7) doivent être mises en œuvre techniquement et vérifiées à chaque opération:

- **par domaine uniquement** - déléguer sa voix pour toutes les questions à la fois est techniquement impossible;
- **interdiction de l'auto-délégation** - vérifiée à chaque opération;
- **interdiction des chaînes** - une voix déléguée reçue ne peut pas être transmise plus loin;
- **plafond** - 5 pour cent des participants, mais au moins 10 délégants;
- **une seule délégation active par domaine** - une nouvelle est impossible sans révocation de la précédente;
- **révocation en une seule étape** - à tout moment, sans avoir à s'expliquer et sans l'accord de celui à qui la voix a été confiée;
- **questions sans délégation** - modification de la Charte et des règles de base de la trésorerie, financement au-delà du seuil fixé, constitution de l'Emergency Multisig, restriction de pouvoirs, suspension du droit de vote, annulation d'une délivrance de passeport et modification des principes intangibles: sur ces questions, on vote uniquement en personne.

Tout earthling peut être délégué: la seule sélection est le choix de celui qui délègue (Charte, article 7).

## Le fil des propositions

Toutes les propositions apparaissent **dans l'ordre chronologique de leur dépôt**. La réputation de l'auteur n'influe pas sur la place dans le fil. Le filtrage par réputation ne sera disponible que comme mode d'affichage, que chaque participant active pour lui-même; aujourd'hui, la plateforme n'en dispose pas.

Une priorisation automatique des propositions fixerait l'ordre du jour sans responsabilité formelle; elle n'est donc pas mise en œuvre dans la plateforme.

## Ce que la plateforme fait dans le circuit de la DAO

- interface de vote et de débat;
- consignation publique des décisions adoptées et de leur état d'exécution;
- réalisation technique des décisions: modification des réglages, mise à jour des règles de répartition des fonds, lancement de programmes;
- journalisation des actes clés en vue d'un audit ultérieur.

L'infrastructure de bas niveau peut être quelconque; les principes n'en dépendent pas.

---

# SECTION 07. L'unité de compte dans la plateforme

La plateforme sera l'interface principale de l'usage pratique de l'unité de compte; aujourd'hui, l'unité n'est pas émise: l'économie de la participation est tenue dans la comptabilité interne de la plateforme (document « Earthlings Coin », section 8), et les scénarios ci-dessous décrivent sa destination. La séparation entre l'économie et le pouvoir y est strictement observée.

### Les usages internes

- rémunération de l'apport aux projets et aux cellules;
- gestion des fonds internes;
- paiement de l'accès à certains services et outils;
- soutien d'initiatives: micro-subventions, expérimentations, programmes pilotes.

### Ce que l'unité de compte ne fait pas

- elle ne donne ni voix supplémentaire ni poids politique;
- elle ne conditionne pas l'accès à la participation de base: signature de la Déclaration, vote, débats;
- elle n'influe pas sur la place d'une proposition dans le fil ni sur la priorité d'examen;
- elle ne peut pas être employée comme instrument de pression ou d'exclusion des gens hors des processus;
- elle ne remplace pas les monnaies nationales et n'est pas imposée comme moyen de règlement quotidien.

L'unité de compte reflète l'apport et permet de lancer des projets, mais elle ne partage pas les gens entre importants et négligeables. La plateforme veille à ce que la logique économique ne détruise pas l'égalité de participation.

---

# SECTION 08. Données et vie privée

La plateforme est conçue en tenant compte des principes du RGPD et de normes analogues. Le principe de départ: la préservation de la dignité humaine et du droit à la vie privée importe plus que le confort de l'analyse.

### Les principes principaux

- **minimisation** - n'est collecté que ce qui est réellement nécessaire;
- **séparation** - identité, participation, économie et analyse sont réparties entre des couches et des espaces de stockage distincts;
- **transparence** - le participant comprend quelles données le concernant existent et comment elles sont utilisées;
- **contrôle** - le participant peut demander la rectification ou la suppression des données traitées par la plateforme.

### Ce qu'il advient des données dans le registre distribué

Il faut ici de l'honnêteté, et non une promesse impossible à tenir.

Les données qui se trouvent dans les bases de la plateforme sont rectifiées à la demande du participant et supprimées à sa demande, hormis celles que nomme la Politique de confidentialité; pour qui appartient au peuple, la suppression du compte ne va qu'avec la sortie. Les inscriptions dans le registre distribué ne se suppriment pas, par nature, et c'est précisément pour cela que le nom, le document, la biométrie et les hachages de vérification n'y sont pas inscrits lors de l'émission. Lors de l'émission, sont inscrits au registre l'adresse du portefeuille, le numéro de l'inscription du passeport, l'identifiant du participant par lequel l'inscription est reliée aux données du système de vérification d'identité, et l'heure de l'émission; dans le champ du pseudonyme est inscrit, lors de l'émission, le seul mot « Earthling », et dans le champ du hachage de vérification, une valeur aléatoire sans lien avec les données de la vérification; l'émission et la destruction laissent des marques au registre. Ce sont des données pseudonymes que nous relions à votre compte.

À la sortie, le passeport est détruit, et il reste dans le registre une marque pseudonyme indiquant que l'appartenance a existé pendant une période déterminée. C'est un fait du passé, non une appartenance qui dure. Ce modèle prédomine dans la pratique européenne relative aux registres paroissiaux: l'inscription est conservée, le statut est marqué; la question de savoir si ce modèle suffit est actuellement tranchée par la Cour de justice de l'Union européenne (affaire C-12/25).

La liberté d'association n'exige pas l'effacement de l'histoire: la renonciation à une nationalité ne détruit pas les archives de l'État.

### Vérification d'identité et protection des données

- la biométrie et les documents sont traités par un système propre au moment de la vérification; les prises de vue et les scans ne sont pas conservés;
- du système de vérification d'identité, la plateforme reçoit non pas la biométrie ni les données du document, mais le résultat de la vérification et les données destinées au compte (section 03);
- en vertu d'une décision de justice passée en force de chose jugée ou d'une exigence légale équivalente, les données sont communiquées selon la procédure de la Politique de confidentialité (section 05); il ne s'y trouve pas de données biométriques - elles ne sont pas conservées;
- les inscriptions au registre obéissent au principe de pseudonymat et de minimisation des liens personnels.

La plateforme n'est pas bâtie comme un système de surveillance généralisée. Elle vise à devenir un exemple de traitement respectueux des données à une époque où presque tout est techniquement possible.

---

# SECTION 09. Architecture technique et capacité de croissance

Les technologies concrètes - chaînes de blocs, bases de données, langages, cadriciels - peuvent changer. Ce qui compte, c'est la logique de l'architecture:

- **modularité** - le noyau, le sous-système d'identité, le composant DAO, la couche économique et les interfaces évoluent indépendamment;
- **capacité de croissance** - l'architecture est prévue pour une croissance de la composition de plusieurs ordres de grandeur sans perte de disponibilité ni de sécurité;
- **résistance** - configurations tolérantes aux pannes, stockages de secours, nœuds indépendants;
- **rétablissement** - sauvegardes, plan de rétablissement après défaillance critique, protocoles d'action en cas de compromission de clés;
- **auditabilité** - possibilité d'un audit technique et juridique extérieur des composants clés.

La plateforme n'est pas liée à jamais à une pile technologique. Lors de toute migration, les principes demeurent: identité intransmissible, voix égale et inaliénable, vérifiabilité des processus et protection de la personne.

> **La capacité d'exister sans exploitant.** Le registre des passeports est tenu dans un réseau distribué, et non sur les serveurs de la plateforme. C'est pourquoi les inscriptions du registre demeurent lors d'un changement d'exploitant, d'une migration d'infrastructure et d'une reconstitution reconnue par la Feuille de route comme continuation légitime; les endroits où le registre dépend aujourd'hui de qui l'exploite sont indiqués dans le document « Où nous en sommes ».

---

# SECTION 10. Les étapes de réalisation

Comptent à la fois l'agencement de l'architecture visée et la manière d'y parvenir.

**Étape 1. Le noyau - bâti et déployé.**
Espace personnel, carte des participants par pays, états des cellules, mécanisme de vote, intégration avec le système propre de vérification d'identité. Le minimum de fonctions, suffisant pour commencer.

**Étape 2. Les cellules et les projets - bâtis et déployés.**
Cycle de travail des cellules: demandes, formation, réalisation, consignation des résultats.

**Étape 3. Le remplissage par la pratique - à venir.**
Votes de fond réguliers, vote secret à décompte vérifiable, délégation par domaine, signature de la Déclaration, outils d'IA auxiliaires pour l'analyse des initiatives, fonds en fonctionnement, extension des usages de l'unité de compte. Le remplissage commence avec l'ouverture de l'adhésion et se fait à mesure que le nombre de participants augmente.

**Étape 4. Les relations extérieures - à venir.**
Relations avec les organisations internationales, les universités, les centres de recherche. Mise à disposition de données agrégées pour l'analyse des processus mondiaux. Participation du peuple au débat sur des questions qui dépassent le cadre d'un seul pays.

> **Sur la limite de la quatrième étape.** Il s'agit du droit d'être entendu, non d'un pouvoir dans la décision. La plateforme ne devient pas et ne peut pas devenir un lieu où se prennent des décisions obligatoires pour quiconque en dehors des Earthlings eux-mêmes. Les compétences des États ne sont pas touchées (Déclaration, article 6).

La distinction entre ce qui est bâti et ce qui reste à faire est présentée honnêtement. Le contrat du registre des passeports, la vérification d'identité, les cellules et la comptabilité de l'économie interne sont déployés et fonctionnent; le canal public de vote est déployé, mais aucun vote de fond n'y a encore eu lieu, l'outil de vote secret est en cours de sélection, et les contrats intelligents de la Trésorerie ne sont pas déployés (document « Où nous en sommes »). La valeur probante et pratique de l'infrastructure naît à mesure que la participation s'accumule, et non au moment du déploiement.

---

## Remarque: l'interface juridique extérieure

Pour les relations avec l'infrastructure juridique, administrative et financière traditionnelle, il est recouru à des instruments juridiques enregistrés dans un ou plusieurs ordres juridiques. Ces instruments sont des moyens opérationnels interchangeables de relations extérieures et ne définissent pas le peuple.

Après l'adoption de la Déclaration, les personnes qui agissent par ces instruments exécutent une mission révocable de l'Assemblée DAO et ne créent aucune fonction; avant l'adoption, il n'y a pas de peuple, et nul n'agit en son nom. Le modèle juridique détaillé figure dans le document [Base juridique](https://earth-lings.org/documents/fr/fr04-base-juridique.html).
