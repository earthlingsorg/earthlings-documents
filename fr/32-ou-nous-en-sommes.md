# Où nous en sommes

*Peuple des Earthlings*

## À quoi sert ce document

Nous affirmons que les Earthlings sont vérifiables. Une telle affirmation n'a de sens que si l'on peut indiquer exactement ce qui est vérifiable et par quel moyen. C'est pourquoi, au lieu de la formule générale « notre code est ouvert », nous publions la limite exacte: ce qui est ouvert, ce qui est fermé et pour quelle raison.

La période constituante est en cours: jusqu'au jour de l'adoption de la Déclaration, le peuple est encore en train de se constituer, et une partie des chiffres ci-dessous ne se lit pas comme elle se lira après. Ses règles et ses délais sont exposés dans le document [La période constituante](https://earth-lings.org/documents/fr/fr20-periode-constituante.html); nous ne les répétons pas ici, pour que les dates gardent une source unique.

> **Principe.** Est ouvert ce dont dépend la vérifiabilité du peuple: qui est participant, comment il l'est devenu, combien nous sommes et comment la voix est décomptée. Est fermé ce dont la publication n'ajouterait rien à la vérifiabilité mais créerait un risque pour les participants: la couche serveur et le traitement des données personnelles.

## Ce qui est ouvert

| Composant | Où | Licence |
|---|---|---|
| Contrat intelligent du passeport EarthlingPassportV2 | [github.com/earthlingsorg/earthlings-contracts](https://github.com/earthlingsorg/earthlings-contracts) | MIT |
| Documentation d'architecture | dossier `/docs` du même dépôt: modèle d'identité, minimisation des données, sécurité, réputation, flux des apports | MIT |
| Adresse du contrat et toutes ses transactions | [0x20e7962878429B803E35F83ba34eD291afEC2Be4](https://polygonscan.com/address/0x20e7962878429B803E35F83ba34eD291afEC2Be4) | données publiques |
| Registre des passeports | chaîne de blocs Polygon, lu directement depuis le contrat | données publiques |
| Canal public des votes de la DAO | [snapshot.org, espace earthlings-dao.eth](https://snapshot.org/#/s:earthlings-dao.eth) | données publiques |
| Trésor on-chain | [0xaEC7016218f7883bf6e47a2C932FdE6d822086C0](https://app.safe.global/home?safe=matic:0xaEC7016218f7883bf6e47a2C932FdE6d822086C0) | données publiques |

## Ce qui est fermé et pourquoi

| Composant | Raison |
|---|---|
| Partie serveur de la plateforme | Elle contient la logique d'accès aux comptes. Sa publication avant un audit indépendant accroît le risque d'intrusion dans les comptes des participants et n'ajoute rien à la vérifiabilité du peuple. |
| Système de vérification d'identité | Il traite des documents et de la biométrie. Ici, la fermeture fait partie de la protection des données personnelles, elle n'est pas une dissimulation. La manière dont la minimisation des données est agencée est décrite dans la documentation ouverte. |
| Infrastructure de déploiement | Elle contient la configuration des serveurs. Sa publication serait une carte pour un attaquant. |

Aucun des composants fermés ne détermine qui est earthling ni comment la voix est décomptée. C'est le contrat intelligent ouvert qui le détermine.

## Ce que l'on peut vérifier dès maintenant, sans nous faire confiance

- **Les règles du passeport.** Lire le code source du contrat dans le dépôt: le passeport est intransmissible, un seul par portefeuille, et son titulaire peut le détruire lui-même.
- **Combien de passeports ont été délivrés.** Appeler `totalSupply` sur le contrat. Ce n'est pas nous qui donnons ce nombre: c'est la chaîne de blocs. Mais il faut le lire correctement, et nous expliquons comment. **Il s'y trouve aujourd'hui quatre inscriptions de test**, faites lors de la mise au point du système avant son lancement, et il n'y a pas de participants réels parmi elles. **Du 7 septembre 2026 au jour de l'adoption du texte**, ce nombre désigne les personnes ayant fait vérifier leur identité et participant à la constitution: elles ne deviendront earthlings qu'après l'adoption de la Déclaration. **Après l'adoption**, le nombre de passeports délivrés est le nombre d'earthlings.
- **Si une adresse déterminée détient un passeport.** Appeler `balanceOf`. Réponse: 1 ou 0.
- **Les votes de la DAO.** Ouvrir l'espace sur Snapshot et voir les propositions, les voix et les signatures. Chaque voix est signée par le portefeuille du votant: nous ne pouvons ni ajouter une voix ni en falsifier une.
- **Le droit de vote.** Snapshot demande à notre serveur si une adresse détient un passeport. Il faut faire confiance à cette étape au moment du vote, mais pas après: les adresses de tous les votants sont publiques, et chacun peut vérifier lui-même chacune d'elles dans le contrat sur Polygon. Un écart deviendrait visible.

Nous décrivons ce dernier point sans détour, car c'est l'un des deux endroits où il faut nous faire confiance. Nous préférons les nommer nous-mêmes plutôt que d'en laisser la découverte à un vérificateur.

Le second endroit est la clé du propriétaire du contrat. Dans la version déployée du contrat, les fonctions d'émission et de destruction du passeport sont accessibles au propriétaire, et la clé du propriétaire est aujourd'hui chez le fondateur. La Charte, article 21, n'admet la destruction contre la volonté du titulaire que pour deux motifs et seulement avec une procédure: notification, délai d'objection, avis du Conseil, vote secret à majorité renforcée, recours. Ces garanties ne figurent pas dans le code: elles sont procédurales. Elles reposent donc aujourd'hui sur notre parole et non sur la technique, et nous le reconnaissons. Ce qui est fait à ce sujet: séparation des droits d'émission et de destruction en rôles distincts, délai d'exécution de la destruction et transfert de la propriété à une multisig de six signataires élus. Les échéances figurent dans la [Feuille de route](https://earth-lings.org/documents/fr/fr19-feuille-de-route.html).

## Ce qui n'existe pas encore

Liste honnête de ce qui est annoncé comme principe mais n'est pas encore fait:

- Le code source du contrat est publié dans le dépôt, mais **il n'est pas encore vérifié dans l'explorateur de la chaîne**. Cela signifie que la correspondance entre la source publiée et le bytecode déployé doit pour l'instant être vérifiée par soi-même. La vérification est en cours.
- **Aucun audit de sécurité indépendant n'a été réalisé.** Il est prévu avant l'extension des opérations.
- **Les contrats intelligents de la Trésorerie ne sont pas déployés.** Seul le contrat du passeport l'est; l'économie interne de participation est pour l'instant tenue dans la comptabilité de la plateforme.
- Le canal public de vote **est déployé et fonctionne techniquement, mais aucun vote de fond ne s'y est encore tenu**.
- Le programme de recherche de vulnérabilités (bug bounty) est annoncé comme principe, mais **n'est pas encore ouvert**.
- **Les droits du propriétaire du contrat ne sont ni séparés ni transférés.** L'émission et la destruction du passeport sont accessibles à une seule clé, il n'y a pas de délai d'exécution, et la clé est chez le fondateur. Les limites de l'article 21 de la Charte jouent par voie de procédure.
- **Il n'y a pas encore de multisig sur le portefeuille du trésor.** Le seuil de signatures est de une; cela se vérifie à l'adresse du portefeuille. Le passage à une composition de six signataires est un critère de passage entre les phases.

## Le droit de reproduction

Le registre des passeports vit dans la chaîne de blocs et non sur nos serveurs, et le code du contrat est ouvert. Il en découle une chose pratique: si l'infrastructure est arrêtée ou si son fonctionnement est accaparé, la communauté peut bâtir une nouvelle plateforme sur le même registre. Ce qui se transfère, ce sont les gens et leurs passeports; la couche serveur est interchangeable.

La reproduction a deux appuis, et le second n'est pas moins important que le premier. Le registre donne la continuité des personnes, et la **spécification publiée** donne la possibilité de rebâtir l'outil: les règles, les seuils, les quorums, les délais et les procédures sont intégralement exposés dans la Charte, dans la Trésorerie et dans les présents documents. Ce n'est donc pas notre code qui se reproduit, mais le système décrit. Copier la partie serveur fermée n'est pas nécessaire et ne le sera pas.

C'est pourquoi la fermeture de la partie serveur n'ôte pas au peuple le droit de continuer sans les fondateurs. Les caractères d'une continuation légitime - noyau intangible conservé, volonté de personnes vérifiées et continuité des procédures - sont décrits dans le document [Feuille de route de la période de transition](https://earth-lings.org/documents/fr/fr19-feuille-de-route.html).
