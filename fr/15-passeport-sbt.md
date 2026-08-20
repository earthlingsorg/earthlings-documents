# Passeport SBT de l'earthling

**Le titre numérique d'appartenance au peuple des Earthlings**

> Le présent document décrit l'agencement et la portée juridique du passeport. En cas de divergence, la [Charte](https://earth-lings.org/documents/fr/fr05-charte.html) s'applique, et en cas de divergence entre la Charte et la [Déclaration](https://earth-lings.org/documents/fr/fr01-declaration.html), la Déclaration. Les modalités d'adhésion sont décrites dans le document [Le chemin de l'earthling](https://earth-lings.org/documents/fr/fr14-chemin-de-l-earthling.html).

---

## Ce que c'est

Le passeport SBT de l'earthling est un jeton numérique intransmissible (Soulbound Token), délivré à chaque participant après la signature de la Déclaration, la vérification de son identité et le versement de la cotisation. Il atteste cryptographiquement l'appartenance au peuple et est conservé dans un registre distribué comme une inscription unique, protégée contre la falsification.

À la différence des passeports d'État, rattachés à un territoire et attestant une nationalité, ce passeport atteste l'appartenance à un peuple réuni par des valeurs communes. Il ne peut être ni transmis à autrui, ni vendu, ni aliéné.

**Intransmissibilité.** Le passeport est rattaché à votre portefeuille, et la transmission est bloquée dans le contrat lui-même, et non par une règle que l'on pourrait contourner. L'unicité de la personne a été vérifiée à la délivrance.

**Protection cryptographique.** L'inscription est conservée dans un réseau distribué et ne peut être ni falsifiée ni modifiée à l'insu de tous.

**Égalité.** Tous reçoivent le même passeport avec les mêmes droits. Il n'existe ni classes privilégiées ni niveaux d'appartenance. Une personne - un passeport - une voix.

---

## Ce que donne le passeport

### La participation à la gouvernance

- le droit de vote à l'Assemblée DAO;
- le dépôt de propositions et d'initiatives;
- la participation aux décisions sur chaque question.

> **La voix est inaliénable** et ne peut être retirée ni suspendue en raison des opinions, du contenu du vote, d'un désaccord avec les décisions ou à titre de sanction générale (Déclaration, article 10; [Charte, articles 17 et 37](https://earth-lings.org/documents/fr/fr05-charte.html)). La voix est le contenu de l'appartenance: en la retirant pour de tels motifs, le peuple exclurait la personne en ne lui laissant que le nom.

La seule exception est constituée par des actes établis dirigés contre l'intégrité du vote lui-même: entente, achat ou vente d'une voix, contrainte exercée sur d'autres, contournement de la règle « une personne - un passeport » (Charte, article 22 bis). Les opinions, le contenu du vote et le désaccord avec les décisions ne sont un motif sous aucune présentation.

### L'identification numérique

- attestation publiquement vérifiable du statut de participant;
- accès aux services de l'écosystème;
- possibilité d'utilisation dans les applications décentralisées qui prennent en charge cette norme.

### L'accès à l'écosystème

- la plateforme numérique du peuple;
- la participation aux cellules et aux projets communs;
- les ressources éducatives;
- les échanges avec les autres participants.

### Les marques de participation

L'historique de la participation et de l'apport est consigné publiquement: votes, projets achevés, travail dans les cellules.

> **Ces marques n'ont aucun effet** et ont un caractère exclusivement informatif: [Charte, article 8](https://earth-lings.org/documents/fr/fr05-charte.html).

---

## Comment l'obtenir

**1. Signature de la Déclaration.** Étude des documents, compréhension des principes, confirmation de l'accord par signature numérique. C'est cet acte qui crée l'appartenance.

**2. Vérification de l'identité.** Vérification que vous êtes une personne vivante et que vous êtes unique. Elle assure le principe « une personne - une voix ». Les images d'origine et les scans de documents ne sont pas conservés.

**3. Versement de la cotisation.** L'équivalent de 79 USD, en cryptomonnaie (ETH, USDT, USDC). L'affectation de la cotisation et les modalités de sa dépense figurent dans le document [Trésorerie](https://earth-lings.org/documents/fr/fr09-tresorerie.html).

> Celui qui ne peut pas verser lui-même la cotisation entre dans une file d'attente ouverte, et la cotisation est versée pour lui par une autre personne ou par la Trésorerie. Le passeport ne se distingue alors en rien des autres: le registre n'inscrit pas qui a versé la cotisation. La cotisation n'achète pas l'appartenance: celle-ci naît de la signature de la Déclaration.

**4. Délivrance du passeport.** Le jeton est créé automatiquement et rattaché à votre portefeuille.

---

## Le socle technique

### L'infrastructure

- réseau: Polygon Mainnet, compatibilité EVM;
- norme: ERC-721, intransmissible (soulbound);
- adresse du contrat des passeports: `0x20e7962878429B803E35F83ba34eD291afEC2Be4`;
- les transactions sont publiques et vérifiables dans l'explorateur du réseau sans notre intervention;
- le code source du contrat est ouvert (licence MIT).

### La sécurité du contrat

- socle: bibliothèques éprouvées OpenZeppelin;
- règle: un passeport par portefeuille; la transmission est bloquée dans le contrat lui-même;
- un audit indépendant est prévu avant l'extension des opérations.

### La conservation des données

- **dans le registre:** identifiant, pseudonyme, empreinte de la vérification. Les données personnelles ne sont pas inscrites au registre;
- **hors registre:** les données personnelles du compte, sous forme chiffrée et en volume minimal;
- **biométrie:** non conservée. Ne sont conservées que des empreintes cryptographiques irréversibles, et uniquement pour qu'une même personne ne puisse pas détenir deux passeports valides;
- la conception suit les principes du RGPD.

### La cryptographie

- signatures: ECDSA secp256k1;
- hachage: Keccak-256.

Une norme de passeport unique pour tous les participants permet de concentrer les moyens sur la fiabilité d'un seul système et assure une protection égale à chacun.

---

## La portée juridique

Le passeport est un titre numérique d'appartenance au peuple des Earthlings.

### Ce que le passeport ne donne pas

Il importe de le comprendre avant l'adhésion et non après.

- **il ne donne ni nationalité ni résidence** d'un pays quelconque;
- **il n'ouvre aucune facilité de visa** ni droit d'entrée;
- **il n'a aucune force juridique** devant les administrations d'aucun pays;
- **il ne remplace pas les documents** d'identité;
- **il ne dispense pas** de respecter les lois du pays de résidence;
- **il ne crée aucun droit en droit international.**

Le passeport atteste ce qu'il atteste, et ce n'est pas peu: une personne déterminée est vérifiée comme vivante et unique et a signé la Déclaration. Au sein du peuple, tout en découle: voix égale, participation aux décisions, appartenance inaliénable. Ce que cet ensemble signifie pour le droit international fait l'objet d'un examen distinct dans les documents [Base juridique](https://earth-lings.org/documents/fr/fr04-base-juridique.html) et [Objections et réponses](https://earth-lings.org/documents/fr/fr26-objections-et-reponses.html), où sont exposés aussi les arguments contraires.

### La protection des données

- droit à la rectification et à la suppression des données traitées par la plateforme;
- les inscriptions dans le registre distribué ne se suppriment pas, par définition technique, et c'est précisément pour cela qu'elles ne contiennent pas de données personnelles: on y trouve des adresses pseudonymes et des marques d'actes;
- minimisation du traitement; chiffrement des données personnelles;
- les photographies et les scans ne sont pas conservés.

### Responsabilité et différends

- la DAO des Earthlings n'est pas une personne morale enregistrée;
- les participants répondent individuellement du respect des lois de leurs pays;
- les différends internes se règlent selon les procédures de la Charte: dialogue, médiation et, en cas de manquements graves, saisine du Conseil indépendant. Le peuple ne se substitue pas aux juridictions et aux mécanismes juridiques étatiques et n'offre pas d'arbitrage hors de son écosystème.

---

## La fin du passeport

**En règle générale, vous seul détruisez votre passeport**, avec votre propre clé, depuis votre propre portefeuille (fonction `burnByHolder`). La plateforme ne conserve pas vos clés et ne peut ni procéder à la destruction à votre place, ni y faire obstacle.

La Charte (article 21) établit **deux exceptions et deux seulement**, et cette liste ne peut pas être élargie.

> **Sur le décès du titulaire.** L'appartenance prend fin par l'effet du décès de la personne, mais le passeport n'est pas détruit pour autant. Le peuple n'a pas accès aux registres de décès du monde entier; un tel motif reposerait donc sur des informations invérifiables et deviendrait le moyen le moins coûteux d'écarter un participant. Le passeport demeure au registre; la participation qui n'existe plus est prise en compte par le mécanisme d'inactivité (Charte, article 20). Le passeport ne se transmet pas par succession et ne se transmet en aucune circonstance.

### 1. L'annulation d'une délivrance non valide

Elle s'applique s'il est établi que le passeport a été délivré en méconnaissance des conditions de délivrance: plus d'un passeport valide délivré à une même personne, ou vérification effectuée au moyen de données falsifiées ou de l'identité d'autrui.

**Ce n'est ni une sanction ni une exclusion du peuple.** Il est seulement établi que la délivrance n'a pas régulièrement eu lieu à l'origine. Aucune réémission automatique n'en découle: si l'obstacle à une délivrance régulière est levé, la personne a le droit de repasser la vérification dans les conditions de droit commun.

**La procédure** est une décision de l'Assemblée, non un acte de l'exploitant:

- mémoire motivé avec preuves;
- notification du titulaire et **au moins 21 jours** pour objecter; le titulaire a le droit d'appeler d'autres participants à son soutien;
- avis du Conseil indépendant;
- vote de l'Assemblée: **75 pour cent avec un quorum de 25, secret, sans délégation**;
- **recours dans les 30 jours**, la majorité simple suffisant pour annuler la décision.

Les pouvoirs techniques de l'exploitant se limitent à l'exécution d'une décision déjà prise par l'Assemblée. L'exploitant ne peut pas annuler un passeport de sa propre initiative.

### 2. La réémission technique

Sur **demande du titulaire lui-même**, en cas de perte d'accès au portefeuille ou de migration du contrat. Le passeport est détruit et immédiatement réémis à la même adresse ou à une nouvelle. **L'appartenance n'est pas interrompue**, aucun vote n'est nécessaire.

### Le principe d'inaliénabilité

Nul ne peut être privé de force de son appartenance au peuple. Il n'existe pas de procédure d'exclusion.

En cas de mesures de restriction pour manquements graves aux règles communes, le passeport est conservé, **le droit de vote est intégralement conservé**, et les restrictions ne touchent que la participation aux cellules, le droit de faire des propositions et l'accès à certains services - selon la procédure de l'article 22 de la Charte, avec droit de se défendre, vote secret et recours.

### Ce qui se passe techniquement

- la destruction est effectuée par la fonction `burn` du contrat intelligent;
- les données du passeport sont supprimées du registre actif du contrat;
- il subsiste dans l'historique immuable une marque pseudonyme indiquant que le passeport a existé et a été détruit: c'est un fait du passé, non une appartenance qui dure;
- il n'y a pas de données personnelles réelles dans le registre;
- pour une nouvelle adhésion, la procédure complète est suivie et un nouveau passeport est délivré.

---

## Sur le financement

À ce jour, le peuple se développe sur les fonds de ses participants: aucun financement extérieur n'a été recherché.

La Charte et le document [Trésorerie](https://earth-lings.org/documents/fr/fr09-tresorerie.html) prévoient la possibilité de recevoir des subventions et des dons d'organisations extérieures, à condition que la source soit obligatoirement publiée, qu'il n'y ait pas de conditions contraires aux principes du peuple, et avec une interdiction expresse: le donateur n'obtient ni voix ni influence sur les décisions. Le montant d'un don ne donne rien.

Toutes les décisions de dépense sont prises par un vote de l'Assemblée DAO et publiées; les postes de dépense et leurs parts sont fixés par l'article 9 du document [Trésorerie](https://earth-lings.org/documents/fr/fr09-tresorerie.html).
