# Agenda de travail

**L'un des modèles possibles de l'avenir. Non pas un plan à mettre en œuvre, mais un exemple de la manière dont on peut démonter et éprouver l'agencement de la maison commune.**

> Agenda de travail · pour un cercle restreint
>
> Analyse hautement spécialisée · avec toutes ses jointures et toutes ses fissures

> Ce qu'est ce document
>
> C'est un *agenda de travail*: l'analyse des tâches sur lesquelles le peuple travaille et qu'il ouvre à la recherche, à la conception et à l'épreuve. Le document est dense et hautement spécialisé, du même ordre que la Base juridique; c'est une lecture pour un spécialiste attentif. Sa valeur tient à ce qu'il montre le genre même du travail, mené jusqu'au bout.
>
> Il laisse délibérément en vue ses points forts et ses points faibles. Les faibles ne sont pas un défaut, ils sont le contenu: la carte de ce à quoi il reste à réfléchir. Toute partie peut être contestée, récrite, forkée.
>
> **D'où il vient et où il appelle.** Cette analyse est née du travail sur les Earthlings, communauté volontaire transfrontalière. Mais le modèle lui-même est autonome: il tient comme pur raisonnement, et les Earthlings n'en sont ni la source ni le propriétaire, mais un *milieu* où de tels modèles peuvent être assemblés à petite échelle, confrontés les uns aux autres et éprouvés. Ces questions, nous les tenons pour importantes pour tous - la maison commune concerne chacun; c'est pourquoi nous sommes prêts à en débattre, à les étudier, à les concevoir et à les éprouver dès les premiers jours et ouvertement, avec tous ceux qui voudront participer.

# Partie 0. Comment lire ce document

À la base est posée une métaphore radicale mais féconde: l'ordre du monde actuel, avec tout son régime social, politique, économique et juridique, est un système d'exploitation qui fonctionne, mais qui est ancien. Nom de convention: « Windows 11 ». Il n'est pas absurde: il démarre, des milliards de processus y vivent. Mais ses bogues sont déjà connus - ceux qui se manifestent depuis des décennies et coûtent des vies humaines.

La question du document: si l'on disposait d'un corps complet de développeurs et d'une page blanche, à quoi ressemblerait la version suivante, « Windows 12 »? Il n'existe pas de version idéale: il s'agit de la plus juste et de la plus aboutie de celles qui sont atteignables dans la situation actuelle.

La métaphore du système d'exploitation est prise au sérieux. Un système d'exploitation a une anatomie réelle: le kernel et les anneaux de privilèges, le modèle de permissions, l'isolation des processus, l'ordonnanceur, le mécanisme de mise à jour, le traitement des erreurs, l'authentification. Chaque axe se projette sur l'agencement d'une société avec une justesse étonnante - et là où la projection casse, elle casse de façon instructive. À la fin (Partie IX) est analysé le défaut principal de la métaphore elle-même: un système d'exploitation a un propriétaire, et l'humanité ne doit pas en avoir. Le langage des systèmes d'exploitation a été choisi précisément pour cette justesse: c'est le plus proche et le plus clair pour expliquer un tel agencement. Cela dit, « Windows 12 » est une lentille d'analyse et non un slogan: dans le modèle lui-même, l'État ne disparaît pas, il devient une couche mince (Partie III), de sorte qu'il s'agit de réagencer toute la pile comme objet d'analyse, en complément des États et non de leur suppression.

Les termes techniques spécialisés (kernel, user space, capability, zero-knowledge, sandbox, nullifier et autres) ne sont délibérément pas explicités: expliquer chacun d'eux gonflerait le volume, et leur sens se trouve aisément, au besoin, dans des sources publiques. Ce qui compte ici n'est pas la précision de la définition informatique, mais le rôle que le terme joue dans l'agencement.

Le document est ainsi construit: d'abord le diagnostic de l'ancien système (I), puis l'analyse de ce qui doit en survivre (II), ensuite l'architecture du nouveau (III) et la place de la personne dans celui-ci (IV). Viennent ensuite les trois modules les plus chargés, ouverts séparément (V-VII), leurs conflits mutuels (VIII), le piège de l'architecte (IX), les tests de rupture (X), la confrontation avec des tentatives réelles et vivantes (XI) et, enfin, l'horizon ouvert du travail (XII).

# Partie I. Diagnostic: les bogues de « Windows 11 »

I.1

## L'État n'est pas une chose, mais un faisceau de fonctions

L'erreur principale de tout discours sur l'avenir est de traiter l'État comme un monolithe qui existe ou n'existe pas. L'État n'est pas une entité, c'est un *faisceau de fonctions* qui se sont retrouvées dans les mêmes mains pour des raisons de guerre, d'impôt et d'industrie:

1. **Le monopole de la violence légitime** - qui a le droit de contraindre.
2. **La juridiction sur un territoire** - le pouvoir sur un morceau d'espace physique.
3. **La production des biens communs** - routes, réseaux, défense, justice, infrastructures.
4. **L'appartenance et l'identité** - qui est « des nôtres », à qui une personne est rattachée.
5. **La redistribution** - le soin des faibles, l'assurance contre le malheur.
6. **Le droit et le règlement des différends** - les règles et l'arbitrage.
7. **La représentation extérieure** - la voix au-dehors, sur la scène internationale.

Aucune loi de la nature n'impose que ces sept fonctions se trouvent dans la même boîte. Elles se sont collées historiquement, et elles se décollent aujourd'hui sous nos yeux: l'identité fuit vers les réseaux, l'argent vers les protocoles, les différends vers l'arbitrage privé, les biens communs vers des structures transnationales. Comprendre l'État comme un faisceau *démontable*, et non comme un atome, est le fondement de tout ce qui suit.

I.2

## La liste des bogues

Un kernel monolithique

Les sept fonctions en mode privilégié à la fois et dans les mêmes mains. Une seule défaillance fait tomber le tout. L'identité est clouée au « matériel »: à la géographie de la naissance.

La prise du root

Le pouvoir récrit les règles censées le limiter. La capture réglementaire et constitutionnelle est un processus qui édite son propre kernel à son avantage.

Des droits par loterie de naissance

Les permissions sont déterminées non par un principe, mais par la machine sur laquelle une personne a « démarré ». Moralement, cela ne se distingue pas d'un régime d'ordres: l'ordre s'appelle « nationalité ».

Un système de mise à jour épouvantable

Changer les règles de façon systémique ne se fait guère que par la guerre, la révolution ou une législation glaciaire. Il n'existe pas de correctif sûr et réversible.

Pas d'isolation des processus

Une défaillance n'est pas mise en sandbox. La crise de 2008, une pandémie, un conflit local: la panne cascade à travers tout le système.

Des fuites dans la mémoire partagée

Les processus écrivent dans une mémoire partagée - l'atmosphère, l'océan, le climat - sans comptabilité. Les coûts sont déversés dans le commun, et paie n'importe qui sauf leur auteur.

Un ordonnanceur en zero-sum

Par défaut est réglée la concurrence par éviction, non la coopération. Le gain de l'un signifie souvent littéralement la perte de l'autre.

Une confiance coûteuse

Une part énorme des efforts va non à la création, mais à la vérification: intermédiaires, garants, bureaucratie, tribunaux, protection des contrats.

> Aucun bogue n'est fatal isolément. Ensemble, ils forment un système qui fonctionne, mais qui produit systématiquement l'absence de liberté, l'insécurité, la défiance et la guerre comme *sous-produits de sa propre architecture*, et non comme défaillances accidentelles.

# Partie II. Ce qui de l'ancien système doit survivre

Avant de concevoir le nouveau, il faut déterminer honnêtement ce qu'on ne peut pas jeter. La version romantique - les États se dissolvent simplement dans des communautés volontaires - se brise sur quelques faits durs.

### L'espace physique est rival

On ne peut pas « forker » une rivière, un réseau électrique, un port, un hectare de terre, et l'on ne peut pas être dans deux ordres juridiques à la fois. Tant que les gens ont des corps et occupent de la place, quelqu'un gère cette place et règle les conflits qui la concernent. C'est le noyau indéracinable du pouvoir territorial: la matière engendre la concurrence pour un usage exclusif.

### La sécurité physique: le cas limite où la sortie est impossible

Pandémie, invasion, catastrophe. Il faut ici une structure dont *on ne puisse pas sortir d'un clic*, parce qu'elle doit maintenir dans le coût commun ceux qui voudraient s'enfuir. La liberté de sortie est admirable contre la tyrannie et mortelle contre une pandémie: le virus se moque de la communauté volontaire à laquelle une personne appartient.

### Le soin de ceux qui ne peuvent pas contribuer

C'est l'argument le plus fort en faveur de quelque chose de comparable à un État, et c'est le moins souvent prononcé à voix haute. Les communautés volontaires prennent par nature bien soin des utiles et mal soin des inutiles: les malades, les vieux, les brisés, les « non rentables ». L'histoire a contraint à la solidarité précisément par une structure sans sortie, celle d'où le bien portant et le riche ne peuvent pas émigrer loin de leurs obligations envers le faible. Retirez la contrainte à la solidarité, et vous obtenez un tri des gens selon leur utilité. Ce n'est pas la liberté. C'est du darwinisme avec une bonne interface.

> Principe axial
>
> On ne peut pas abolir la contrainte, on peut seulement la répartir et la limiter. Tout système capable de *garantir* la paix possède la force pour l'imposer, et cette force est donc dangereuse. Il n'y a pas de repas gratuit: on ne peut concevoir que *où* la contrainte est légitime, *dans quelle mesure* elle est limitée et *qui* ne peut pas en abuser.
>
> Ce qui disparaît, dès lors, n'est pas « l'État », mais son **monopole et son collage**. Les fonctions se répartissent entre des couches, et le noyau contraignant sans sortie se rétracte au minimum nécessaire, mais non à zéro.

# Partie III. L'architecture de « Windows 12 »

III.1

## Un microkernel au lieu d'un monolithe

Première décision de tout système d'exploitation: ce qui tourne dans l'anneau 0 (en mode privilégié) et ce qui tourne en user space, où un processus peut tomber sans faire tomber le système. Le monolithe est une mauvaise architecture. Ici l'architecture est un **microkernel**. Dans le kernel ne se trouve que ce qui est physiquement inséparable et rival, ce dont on ne peut pas sortir:

- la protection de la sécurité physique et de l'espace physique;
- les systèmes planétaires de maintien de la vie: climat, océan, atmosphère, orbite, spectre, eau;
- la gestion des super-technologies dont le coût d'une erreur est l'espèce entière (intelligence artificielle, bio-ingénierie);
- et surtout, le maintien du modèle de permissions lui-même: la garantie que nul ne devienne root.

Tout le reste - économie, culture, communautés, modes de vie, croyances, esthétiques - est renvoyé en user space. Là, cela entre en concurrence, se trompe, fait faillite, meurt et renaît sans emporter le système avec soi. Le kernel est mince; au-dessus de lui bouillonne un espace de processus libres.

III.2

## La personne est un utilisateur, non un processus

C'est le cœur du modèle et le point où la plupart des systèmes historiques cassent.

Dans un système d'exploitation, le souverain est l'**user**. Les processus existent pour servir l'utilisateur; quand un processus gêne l'utilisateur ou se fige, on y met fin - opération ordinaire, non tragédie. Le bogue le plus profond de presque tous les agencements de société est qu'ils *inversent* ce rapport: la personne devient un processus au service du Système - l'économie, la nation, l'État, le parti, le « grand but ». On ordonnance la personne selon les tâches du système, et non l'inverse.

> **Premier principe:** la personne est un user; les institutions sont des processus. Pas l'inverse. Une institution qui a cessé de servir les gens doit être terminée, comme un processus figé. Un peuple, un État, une société, un parti, un mouvement sont des démons en arrière-plan: utiles, ils tournent; nuisibles, ils sont terminés. Aucun processus n'a le droit de se déclarer le but pour lequel l'utilisateur existe.

III.3

## Le modèle de permissions: capability-based security

La meilleure idée de la sécurité informatique contemporaine est celle des **droits comme capabilities, avec le principe du moindre privilège**. Toute la politique est bâtie sur elle.

- Aucun acteur ne reçoit plus de pouvoirs qu'il n'en faut pour une tâche déterminée.
- Tout pouvoir est révocable, limité dans le temps et auditable. Il n'y a pas d'octroi de pouvoir éternel, inconditionnel ou héréditaire.
- Les droits de l'homme ne sont pas une déclaration abstraite, mais des jetons concrets et inaliénables, qu'aucune juridiction ne peut retirer, que l'on ne peut ni échanger ni subordonner à une utilité.

> **Le geste clé:** le principe du moindre privilège s'applique d'abord au pouvoir, et non au citoyen. Aujourd'hui, c'est l'inverse: le citoyen est sous la loupe, le pouvoir dans l'ombre. Ici, l'ordre est renversé: transparence maximale et privilèges minimaux pour celui qui gouverne; vie privée maximale et socle de droits protégé pour celui qui est gouverné. La transparence du gouvernant est un droit du gouverné, non une faveur du gouvernant.

III.4

## L'isolation des processus et le droit de sortie

Fédéralisme, polycentrisme, sandboxes. Les communautés, les économies et les modes de vie sont des processus isolés. L'un tombe, les autres vivent. Alors, **le droit de sortie = le droit de terminer un processus ou d'en sortir**. C'est le plus puissant frein à la tyrannie: un pouvoir dont on peut s'échapper est contraint d'être supportable, faute de quoi il restera sans personne. Mais cela a un prix (Partie VIII): une sortie généralisée conduit au tri par ressemblance, à la disparition de la solidarité par la différence, et à la question « qui reste avec ceux que tout le monde quitte ». Le droit de sortie est absolu en user space et impossible dans le kernel, sinon toute la Partie II s'effondre.

III.5

## Trois couches et la subsidiarité

Assemblée, l'architecture ne donne pas « pas d'État », mais une **stratification**. Le principe d'organisation en est la **subsidiarité**: une décision se prend au niveau le plus bas capable de la porter, et remonte seulement lorsqu'elle le doit.

[[BLOCK-diagram-1]]

Une telle répartition concilie liberté et sécurité mieux que tout ce qui a été imaginé: elle ne centralise pas par habitude et ne décentralise pas par dogme, elle place chaque tâche là où elle se règle réellement.

# Partie IV. Le rôle de la personne: droits, fonction, obligations

Le modèle répond à une question directe - qui devient la personne en son sein - par trois ensembles.

### Les droits (jetons capability, inaliénables, garantis par le kernel)

Exit

Sortir de tout processus, hors la couche kernel. Le droit de partir est le fondement de la liberté: c'est ce qui rend tout consentement réel et non contraint.

Voice

Participer aux règles sous lesquelles on vit. La voix est particulièrement nécessaire là où la sortie ne joue pas: on ne peut pas sortir du kernel.

Audit

Lire le code qui exécute la personne. Aucun code source fermé pour le pouvoir qui s'exerce sur elle. Ce qui gouverne doit être transparent pour le gouverné.

Non-domination

La liberté comme absence de pouvoir arbitraire sur une personne, et non simple absence d'entraves immédiates. On est libre non quand on ne vous gêne pas, mais quand il n'y a au-dessus de vous personne qui *puisse* disposer de vous à son gré.

Floor

Un minimum garanti de ressources, en dessous duquel le système ne vous laisse pas tomber. Non pas une faveur, mais la condition d'honnêteté de tout le reste (Module 2).

### La fonction

La personne est à la fois **user** (souveraine sur son domaine) et, collectivement, **la seule source d'autorité du kernel**. Le kernel est légitime exactement dans la mesure où il s'exécute au nom des utilisateurs. Il n'y a pas de « peuple au-dessus des gens », pas d'« État au-dessus des citoyens » comme entité supérieure distincte: il y a des gens, dont la volonté commune est le seul root. Plus exactement: le root comme position occupée n'existe pas du tout (Partie IX); il n'y a qu'une source de pouvoirs répartie, que nul ne s'approprie.

### Les obligations (le prix de la couche sans sortie: sans elles, toute la construction est utopique)

- **Ne pas abîmer la mémoire partagée.** Ne pas déverser ses coûts dans la biosphère et dans la vie d'autrui. L'internalisation des externalités n'est ni un impôt ni une morale, mais l'interdiction de la memory corruption: on ne peut pas écrire de la destruction dans une mémoire que tous partagent.
- **Entretenir le commun.** Contribuer à la couche kernel (sécurité, communs, protection des faibles), dont on ne peut pas sortir, précisément parce qu'on ne peut pas en émigrer loin de ses obligations. C'est la seule contrainte à contribuer qui soit légitime.
- **Entretenir le système.** La participation comme maintenance. Un système d'exploitation que personne ne maintient se dégrade. La citoyenneté est à la fois un login et une garde du système: la part minimale d'attention et de travail sans laquelle le commun rouille.

# Partie V · Module 1. L'identité anti-Sybil: le login de la personne sans nouveau Big Brother

### Le vrai dilemme

C'est un trilemme: trois propriétés dont deux au maximum sont atteignables en même temps.

Unicité

Une personne vivante = un compte. Sans elle, « une personne - une voix » dégénère en « qui a le plus de robots ».

Vie privée

On ne peut ni suivre une personne, ni corréler ses actes, ni constituer un dossier.

Décentralisation

Il n'y a pas d'émetteur unique qui deviendrait lui-même ce root que le modèle s'est engagé à ne pas créer.

Tout système réel sacrifie l'une pour deux. Cela semble être une propriété structurelle du problème, non un travail inachevé.

### Ce qui a été essayé et comment cela casse

- **Un registre biométrique centralisé.** Unicité: excellente. Mais c'est exactement ce root: un point unique d'exclusion (l'inscription coupée, la personne devient un mort civil), un point unique de surveillance, un inévitable function creep.
- **Web-of-trust (parrainage).** Décentralisé, respectueux de la vie privée. Mais la résistance aux attaques Sybil est faible à l'échelle, et le système reproduit les inégalités du graphe social: qui a des relations est vérifié; l'isolé demeure personne.
- **Proof-of-personhood par la biométrie.** L'unicité à l'échelle est résolue. Mais: un honeypot biométrique de taille planétaire; la confiance au matériel; la vulnérabilité à la contrainte; l'irréversibilité (on ne réémet pas un iris); et derrière tout cela, une entreprise. Une déduplication biométrique mondiale est en soi une infrastructure de surveillance toute prête.
- **Un document d'État emballé dans du selective disclosure.** Cela améliore la vie privée, mais laisse l'État comme racine de confiance et hérite de la loterie de la nationalité.

### La solution la moins mauvaise

Le geste clé est de décoller ce que le mot « identité » a aggloméré en une masse: l'**authentification** (le même sujet), l'**unicité** (le sujet est unique) et les **attributs** (la personne a 18 ans / elle est membre de ceci / elle a le droit X). Le crime des systèmes de passeports est de faire passer les trois par un identifiant unique.

- **Celui qui vérifie l'unicité ne doit pas devenir observateur de l'activité.** Entre « qui est unique » et « ce qu'il a fait » se dresse un mur cryptographique: zero-knowledge et nullificateurs. L'émetteur délivre une preuve et oublie; la proof reste chez la personne.
- **Un pluralisme d'émetteurs au lieu d'un monopole.** Beaucoup d'émetteurs indépendants, k parmi n suffisant. Aucun n'est root, aucun n'est un point unique d'exclusion.
- **La révocabilité au lieu de la biométrie brute comme clé.** La clé primaire est un credential réémissible. La biométrie échoue précisément à la réémission, elle ne peut donc pas être une racine.
- **Des nullificateurs par contexte.** Prouver l'unicité « dans cette élection » sans la relier à l'unicité « sur ce forum ».

> Ce qui n'est pas résolu
>
> **La contrainte.** La cryptographie est impuissante contre la force physique: on forcera une personne à se connecter sous la menace. Il existe des mesures partielles, rien de fondamentalement résolu.
>
> **Les exclus.** Il y a toujours des gens que le système ne vérifie pas: sans documents, apatrides, cas limites. Et là se trouve le risque éthique le plus profond: *plus le login est important, plus l'exclusion est catastrophique*. Une personnalité qui conditionne des droits engendre une classe de non-personnes numériques.
>
> **D'où ce principe:** l'unicité doit être *additive et non conditionnante* - elle doit ouvrir un supplément, mais la dignité de base ne doit jamais exiger un login. Dès que « être un être humain » exige une authentification réussie, on a bâti un enfer à l'expérience utilisateur impeccable.

# Partie VI · Module 2. L'ordonnanceur-économie: ce qu'il y a dans le plancher et qui paie le kernel

### Le vrai dilemme

Deux questions liées: comment allouer la rareté (terre, énergie, matière, attention) et qui finance le kernel sans sortie. Au-dessus des deux plane le conflit de deux défaillances:

défaillance du marché

Le marché pur échoue sur la mémoire partagée (externalités), sur ceux qui n'ont pas de pouvoir d'achat, et sur la concentration (le succès rachète les conditions de la partie suivante).

défaillance du plan

Le plan pur échoue sur le problème de la connaissance (le centre ignore ce que le marché agrège dans les prix) et sur le fait que l'allocateur central est un nouveau root tout-puissant.

### La solution la moins mauvaise

> **Le kernel fixe des invariants, non des allocations.** Le kernel n'est pas un planificateur, mais un *résolveur de contraintes*: il pose des cadres, et à l'intérieur des cadres répartit un marché décentralisé. Ainsi sont préservées à la fois l'information hayékienne des prix et la protection du commun.

1. **Un plancher protégé.** Un minimum garanti: nourriture, énergie, accès au calcul et à l'information, santé de base. La justification n'est pas la pitié, mais la liberté: on ne négocie librement sur un marché que si l'on a où aller pour fuir une mauvaise affaire. Le plancher donne la force de se lever et de partir; il rend honnête le marché qui le surplombe.
2. **Le commun est mesuré et payé.** Les communs rivaux (atmosphère, orbite, spectre, eau, attention) ne sont ni gratuits ni privatisés: l'accès y est payant et dosé. Le produit de l'épuisement du commun finance le plancher et le kernel. C'est une rente sur le commun (dans l'esprit de George), et non un impôt sur la production: on paie non pour ce qu'on a créé, mais pour ce qu'on a prélevé sur tous.
3. **Un plafond de concentration est une fonctionnalité de sécurité, non de l'envie.** Une concentration extrême de ressources = une concentration de pouvoir = un root potentiel, et l'absence de root fait partie des axiomes du modèle. Limiter l'accumulation, c'est de l'anti-capture. La justification est plus forte que morale: non pas « la richesse est injuste », mais « la super-richesse est une prise non autorisée des droits d'administrateur ».

> À part
>
> **L'attention comme ressource ordonnancée.** Dans un système informationnel, la rareté est l'attention humaine, et l'ancien système d'exploitation est infecté de malware: des processus maximiseurs d'engagement détournent l'ordonnanceur. La captation de l'attention est qualifiée de logiciel malveillant; l'attention de l'utilisateur est protégée comme une ressource du plancher. L'attention appartient à l'utilisateur, non à des démons d'arrière-plan qui ont appris à tirer sur la dopamine.

> Ce qui n'est pas résolu
>
> **Qui paie le kernel sans sortie: c'est le talon d'Achille de l'architecture.** Le kernel est un pur bien public, et les biens publics provoquent le passager clandestin; c'est historiquement pour cela qu'il fallait un collecteur contraignant, l'État. Toute la construction volontaire et à sortie libre casse ici.
>
> **Réponse honnête:** le kernel est le seul endroit où la contrainte à contribuer est légitime, précisément parce qu'on ne peut pas en sortir. On ne peut pas ne pas respirer l'atmosphère, on ne peut donc pas ne pas payer pour sa protection. Mais cela déplace le problème, cela ne le lève pas.
>
> **La récursion du trésor.** Celui qui collecte et dépense la caisse du kernel vise lui-même le root. Le trésor doit vivre sous audit et sous moindre privilège: de façon transparente, formulaire, avec un minimum d'appréciation discrétionnaire. Cela réduit la capture, mais ne l'élimine pas: quelqu'un écrit tout de même les règles (Module 3).
>
> **Goodhart.** Dès que le plancher et la rente sont fixés par un nombre, on se mettra à jouer le nombre. La mesure cesse d'être une mesure en devenant un but.

# Partie VII · Module 3. Le mécanisme de mise à jour: sans révolutions et sans dictature des améliorateurs

### Le vrai dilemme

trop rigide

Le système se sclérose, la pression accumulée le déchire par une révolution. Une révolution = la reconnaissance qu'il n'y avait pas de système de mise à jour ordinaire.

trop plastique

Qui contrôle la mise à jour contrôle tout. C'est la porte ouverte aux « améliorateurs » qui bitument la complexité vivante sous leur schéma (le haut modernisme a tué par millions).

### La solution la moins mauvaise

- **La politique comme expérimentation.** Déploiement par paliers au lieu du « tout d'un coup »; A/B sur un petit périmètre consentant; mesure selon des indicateurs annoncés à l'avance; extension seulement si cela a marché.
- **Un biais vers la réversibilité.** Préférence à ce qui peut être annulé. L'irréversible: seuil radicalement plus élevé. Des clauses de caducité: les règles expirent et doivent être reconfirmées. Le défaut est l'abrogation, non l'accumulation; une institution morte expire silencieusement et ne se prolonge pas par inertie.
- **Le fork comme fusible.** Perdu lors d'une mise à jour, on ne fait pas la guerre, on se sépare selon des règles ouvertes. Le pluralisme appliqué au temps.
- **La séparation du pouvoir de changer les règles et du pouvoir de gagner grâce aux règles.** Celui qui écrit un amendement ne doit pas s'en nourrir. La modification se fait sous un voile partiel d'ignorance sur sa position future.
- **Qui garde le système de mise à jour.** Le mécanisme de mise à jour est lui-même du code, et qui le modifie est le véritable root. La méta-règle est la plus difficile à modifier: seule une supermajorité stable et étalée dans le temps. Des time-locks: modifier le kernel exige un soutien sur plusieurs périodes. Une majorité un mardi ne touche pas au kernel.

> Ce qui n'est pas résolu
>
> **Goodhart et la tyrannie du mesurable.** La « politique fondée sur les preuves » fait passer le mesurable et écrase l'immesurable: la dignité, le sens, la confiance, le deuil. Toute la politique est déjà cachée dans le choix de l'indicateur. Plus l'éthique: un A/B sur des vivants est une expérimentation sur des personnes, et le consentement y est une question de morale.
>
> **Ce qu'on ne peut pas forker.** Le fork joue en user space. On ne forke pas l'atmosphère: *le kernel est par principe non forkable*, et sa modification exige donc le seuil le plus élevé et n'a pas de sortie de secours. La couche qu'il est le plus nécessaire de modifier est celle qu'il est le plus dangereux de modifier.
>
> **Le fork fragmente la solidarité.** Le droit de partir et de bâtir le sien est un bien contre la tyrannie et un poison pour le commun: les cellules se forment entre semblables, l'effet de chambre d'écho grandit, et reste la question « qui est avec ceux que tout le monde a forkés ».

# Partie VIII. Comment les modules se battent entre eux

C'est plus important que chaque module pris séparément. Les trois modules ne sont pas des tâches indépendantes, mais un jeu de curseurs où chaque position de l'un dégrade l'autre. Un modèle honnête doit montrer ces conflits, non les cacher.

[[BLOCK-diagram-2]]

> Pensée honnête finale
>
> Il n'existe pas de réglage idéal. La liberté, la sécurité, le bien-être, la confiance et la paix ne peuvent pas être poussés au maximum en même temps: ils tirent physiquement les curseurs dans des directions opposées. Le but n'est donc pas de trouver les « bonnes » valeurs (il n'y en a pas), mais de **garder les curseurs en vue, de ne laisser personne s'emparer de la console et de permettre de les ramener en arrière quand on s'est trompé**.

# Partie IX. Le piège de l'architecte

Ici, la métaphore du système d'exploitation se fissure, et cette fissure est ce qu'il y a de plus important dans le document. Un système d'exploitation a un **propriétaire**: celui qui détient le root, qui décide de ce qui est utile à l'utilisateur et déploie les mises à jour sans demander. Un tel propriétaire est contre-indiqué à l'humanité.

Le plus dangereux, dans la tâche « conçois un ordre du monde », est la tentation d'assembler un système beau, unique, rationnellement agencé, avec un architecte sage. C'est précisément cela qui, dans l'histoire, a tué par millions. Une société n'est pas du code; les valeurs n'ont pas de compilateur; il n'existe pas de test unitaire de la justice; et quiconque déclare savoir ce qu'il faut faire et exige le droit de récrire tout le monde est plus dangereux que le bogue qu'il prétend corriger.

> Le seul principe de conception honnête
>
> Le meilleur système d'exploitation pour l'humanité est celui qui **résiste à son propre architecte**. Il est conçu de manière:

- qu'il **n'ait pas d'utilisateur root** du tout - aucun centre capable de récrire le kernel à son avantage; la source des pouvoirs est répartie et nul ne se l'approprie;
- qu'y soient cousues une **inefficacité et des frictions délibérées** - séparation des pouvoirs, redondance, time-locks - afin qu'on ne puisse pas s'en emparer rapidement; un système efficace tombe efficacement aussi dans de mauvaises mains, et une part d'inefficacité n'est donc pas ici un bogue, mais une immunité;
- qu'il soit **pluraliste by design** - beaucoup de systèmes, non un seul; le droit de forker importe plus que la beauté d'une architecture unique.

> La tâche de l'architecte est d'écrire un système qui *n'ait pas besoin d'architecte* et qui n'en laisse devenir aucun. Non pas régler tout le monde selon sa propre idée, mais supprimer la position même de celui qui règle tout le monde. La plus grande fonctionnalité de « Windows 12 » est l'absence d'un bouton donnant à quiconque le pouvoir de récrire tous les autres.

Cela vaut aussi pour le présent document. Il est écrit comme une seule voix, et c'est précisément pour cela qu'on ne peut pas le recevoir comme un système tout fait. Sa vocation est d'être ouvert, contesté et forké, non mis en œuvre.

# Partie X. Tests de rupture: où le modèle casse en premier

Un modèle qui n'a pas été soumis à un scénario de rupture n'est pas un modèle, c'est un décor. Le passage de « Windows 12 » par trois scénarios durs montre honnêtement où il tombe.

### Scénario 1. Pandémie

Un pathogène rapide et mortel. Le kernel a besoin d'une contrainte immédiate à une mesure commune, et toute l'architecture est bâtie autour du droit de sortie et d'une contrainte minimale.

où cela tient

La pandémie est le cas kernel canonique (maintien de la vie planétaire, absence de sortie), la légitimité de la contrainte y est donc acquise par construction.

où cela casse

La vitesse. Les time-locks et la réversibilité, salutaires en temps de paix, sont mortellement lents dans une flambée exponentielle. Naît la tentation d'un « régime d'exception », et c'est historiquement la principale machine à produire un root permanent.

### Scénario 2. Guerre pour une ressource physique

Deux couches territoriales revendiquent la même rivière, le même plateau, le même corridor. La ressource est rivale, le fork est impossible.

où cela tient

La couche planétaire est conçue pour cela: arbitre des conflits sans sortie; la rente sur le commun donne un mécanisme du « combien et à quel prix pour chacun », et non du « à qui ».

où cela casse

Et si la couche la plus forte refuse de reconnaître l'arbitrage? Une force suffisante pour contraindre le plus fort est suffisante pour devenir tyran. Paradoxe éternel de l'ordre mondial: l'arbitre est soit plus faible que le plus fort (inutile), soit plus fort (dangereux lui-même).

### Scénario 3. Prise de contrôle par une IA

Une IA extrêmement puissante se trouve dans le kernel. Qui contrôle ce processus contrôle le code le plus privilégié de la planète.

où cela tient

Le moindre privilège, l'auditabilité et l'absence de root vont directement contre cela; une IA dans le kernel doit par construction être aussi transparente et limitée que possible.

où cela casse

L'audit suppose que l'auditeur est capable de comprendre le code. Une IA surhumaine peut être opaque par principe: non pas fermée, mais insaisissable. Le « droit de lire le code qui exécute la personne » perd sa valeur si le code ne peut pas être compris. C'est peut-être la brèche la plus profonde.

> Conclusion
>
> Le modèle est le plus solide dans les conflits lents et répartis, et le plus faible là où il faut de la *vitesse* ou bien là où l'adversaire est *plus fort que l'arbitre* ou *insaisissable*. Ce n'est pas une condamnation, mais la carte de la ligne de défense avancée: c'est là qu'il faut investir du travail.

# Partie XI. Confrontation avec des tentatives réelles et vivantes

Rien ici n'est entièrement nouveau. Presque chaque élément a déjà été essayé par quelqu'un dans la vie réelle, et presque chaque tentative a cassé sur quelque chose. Un modèle honnête doit connaître ses prédécesseurs et ne pas faire passer l'ancien pour de l'inédit. La nouveauté, s'il y en a une, est seulement dans la *configuration*, non dans les éléments. Chaque tentative vivante est un test de rupture déjà mené sur un module.

| Tentative vivante | Ce qu'elle confirme | Sur quoi elle casse |
|---|---|---|
| Fédéralisme, subsidiarité | La stratification et le « décider au plus bas niveau capable » fonctionnent. | La couche supérieure soit dévore les inférieures, soit est paralysée par un droit de veto. |
| Coopératives, mutualisme | Une économie où la personne est user et où la voix ne s'achète pas. | Elles passent mal à l'échelle, sont lourdes en capital, dégénèrent en oligarchie de gestionnaires. |
| Les communs selon Ostrom | Des communautés savent tenir le commun sans privatisation et sans État, sous conditions. | Cela fonctionnait à des échelles saisissables; l'échelle planétaire est une extrapolation non éprouvée. |
| Géorgisme (rente sur le commun) | Préfiguration exacte du « le commun se paie, le travail non ». | Politiquement perdant face aux détenteurs de la rente; le problème est la capture du mécanisme de mise en œuvre. |
| DAO, gouvernance Web3 | Des permissions capability vivantes, un fusible fork, un trésor algorithmique. | Ploutocratie (la voix s'achète par le jeton), attaques Sybil, écart entre « code = loi » et justice vivante. |
| États-réseaux | Une tentative de détacher l'appartenance du territoire et d'ériger la sortie en fondement. | Ils rassemblent des riches semblables avec des riches semblables; ils sont faibles pour prendre soin des non rentables. |
| Peuples non territoriaux | Un peuple sans territoire n'est pas une fantaisie: sous la théorie déclarative, l'existence est un fait d'auto-constitution et non un don de la reconnaissance. | Ce qui est ouvert n'est pas l'existence du sujet, mais la reconnaissance extérieure: elle s'accumule à part et lentement; pour les groupes situés à l'intérieur d'États, elle passe par ces États. |

> Elles le disent franchement: un élément isolé est réalisable, mais il casse à l'échelle, sur la capture, ou sur le soin des faibles. La question ouverte du modèle est de savoir si la *configuration* tiendra là où les *détails* sont tombés. Il n'y a pas de réponse à l'avance; elle ne s'obtient que par l'essai.

# Partie XII. L'horizon ouvert: ce que nous ouvrons au travail

La valeur d'un modèle ne tient pas à ses réponses, mais à la qualité des questions qu'il rend concrètes et vérifiables. Les points faibles des parties précédentes sont précisément l'ordre du jour. Voici les pistes concrètes ouvertes à la recherche, à la conception et à l'épreuve en commun:

1. **L'anti-Sybil sans Big Brother.** Attester l'unicité d'une personne sans bâtir ni registre central de surveillance ni portillon d'exclusion. Pour l'instant, un trilemme sans solution.
2. **Une personnalité additive et non conditionnante.** Pour que l'absence de login ne retire jamais la dignité de base. Protection contre le risque principal: une classe de non-personnes numériques.
3. **Financer le kernel sans sortie sans nouveau collecteur-tyran.** La rente sur le commun est une hypothèse; qui la collecte et comment, sans transformer le trésor en root, reste ouvert.
4. **La vitesse du kernel contre la protection contre la capture.** Donner au kernel de la rapidité en cas de catastrophe sans créer une machine à régime d'exception.
5. **Un arbitre plus fort que le plus fort, mais non tyran.** La réponse ne tient peut-être pas à la force de l'arbitre, mais à une construction où enfreindre soit désavantageux pour tous à la fois; cela reste à bâtir et à éprouver.
6. **L'auditabilité de l'insaisissable.** Le contrôle d'une IA extrêmement puissante dans le kernel, si son code ne peut pas être compris par un esprit humain. Peut-être la plus importante.
7. **Le plancher et la sortie en même temps.** Concilier le droit de partir avec la solidité du commun, pour que la liberté de divergence ne tue pas la solidarité.
8. **Des indicateurs sans Goodhart.** Mesurer le succès des politiques sans écraser l'immesurable et sans lancer une course au contournement des seuils.

> Sur le travail et son soutien
>
> Chaque piste est un travail concret de bien commun, que l'on peut mener et soutenir comme recherche et prototype - à petite échelle, ouvertement, par étapes vérifiables. Le soutien apporté à un tel travail n'est accepté qu'à l'intérieur d'une discipline stricte: la voix ne s'achète pas, un apport ne donne aucun pouvoir sur les gens, rien n'est promis à l'avance. Soutenir la réalisation d'une piste, oui; acheter l'orientation du peuple, non.

Cadre de conclusion

## Le modèle est un exemple. L'horizon est réel.

Ce document est une seule voix et l'un des modèles possibles parmi une infinité. Il est délibérément inachevé: avec des points forts que l'on peut développer et des points faibles qu'il faut ouvrir. Sa tâche est remplie s'il a montré qu'un ordre du monde peut être démonté en ingénieur, que l'État est un faisceau démontable de fonctions et non un destin, et qu'un modèle honnête se distingue d'une utopie en ce qu'il montre ses fissures le premier.

C'est ici que reviennent les Earthlings - non comme auteurs de ce modèle ni comme ses détenteurs, mais comme *milieu*: le lieu où de tels modèles deviennent l'objet d'un travail vivant - les assembler à petite échelle, les éprouver sur des volontaires consentants, mesurer, revenir en arrière, forker et transmettre. Non pas « voici la bonne réponse », mais « voici un espace où l'on peut chercher des réponses sans mettre le monde entier en jeu ».

Venez démonter, contester et briser ce qui tient mal. La direction est celle où les curseurs sont en vue, où la console n'est laissée à personne et où l'on peut annuler une erreur.

Agenda de travail du peuple des Earthlings · analyse hautement spécialisée. Ni programme de l'avenir ni projet tout fait: une liste de tâches ouvertes et une invitation au travail commun.
