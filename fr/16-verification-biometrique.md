# Politique de vérification biométrique des Earthlings

**Entre en vigueur dès sa publication**

> En cas de divergence entre la présente Politique et la [Charte](https://earth-lings.org/documents/fr/fr05-charte.html), la Charte s'applique, et en cas de divergence entre la Charte et la [Déclaration](https://earth-lings.org/documents/fr/fr01-declaration.html), la Déclaration. Les règles générales de traitement des données personnelles figurent dans la [Politique de confidentialité](https://earth-lings.org/documents/fr/fr28-politique-de-confidentialite.html). Pendant la période constituante - du 22 octobre 2026 jusqu'à l'adoption de la Déclaration -, la signature de la Déclaration et l'adhésion au peuple sont suspendues: le peuple défini par un texte adopté n'existe pas encore. La vérification d'identité est menée gratuitement durant cette période et donne lieu à la délivrance d'un document temporaire de participant à la constitution, et non d'un passeport (document « La période constituante », partie 2, point 5). Le document temporaire est émis dans le même contrat que le passeport (document « Où nous en sommes »). La présente Politique s'applique aussi à cette vérification; ce qu'elle dit de la signature et du passeport se rapporte au régime principal, après l'adoption de la Déclaration.

## L'essentiel en bref

- la biométrie est traitée au moment de la vérification et n'est pas conservée;
- pour qu'une même personne ne puisse pas détenir deux passeports valides, des hachages cryptographiques irréversibles sont conservés;
- revenir après une sortie est possible à tout moment;
- le prénom et le nom tels qu'ils figurent dans le document sont nécessaires à la comparaison avec celui-ci; les autres participants vous voient sous le pseudonyme que vous avez choisi;
- la biométrie sert la confiance, non le contrôle;
- système de vérification propre, minimisation des données.

---

# SECTION 01. Les principes

## À quoi sert la biométrie

Elle sert un seul but: attester que derrière chaque voix se tient une seule personne vivante et unique. C'est le socle de la confiance entre inconnus, et rien de plus. Le système est conçu de manière à conserver le moins possible.

## La personne, non les documents

La personne compte plus que les documents. Votre appartenance au peuple est déterminée par votre libre choix, et non par un passeport ou une nationalité. Le but de la vérification n'est pas une reconnaissance venue de l'extérieur, mais la constatation d'un fait simple: vous êtes bien vous, et vous êtes unique.

## Quatre principes

**1. Vérifier l'unicité, non contrôler.** La vérification protège le peuple contre les inscriptions multiples et n'est pas employée à des fins de surveillance.

**2. L'appartenance s'atteste en personne.** Les documents d'État restent à leur place: la vérification ne fait que contrôler l'identité, sans rien remplacer.

**3. La confiance par la vérification.** Dans une communauté sans pouvoir central, une unicité vérifiée crée une couche de confiance de base. Cela ne garantit pas la bonne foi dans une opération déterminée, mais élimine la multiplication anonyme des comptes comme source de manipulations.

**4. La protection contre les abus.** Le fait de ne conserver ni images ni gabarits, les hachages calculés avec la clé secrète du serveur et l'impossibilité pratique de reconstituer une image à partir des données conservées sont conçus pour que le système ne puisse pas servir à une surveillance de masse.

---

# SECTION 02. Champ d'application et consentement

La présente Politique détermine le traitement des données biométriques lors de la signature de la Déclaration, de l'obtention du statut d'earthling et de la participation à l'infrastructure du peuple et, pendant la période constituante, lors de la vérification d'identité pour le document temporaire de participant à la constitution.

## Le fondement juridique

Les données biométriques relèvent d'une catégorie particulière de données personnelles selon l'article 9 du RGPD et sont traitées **exclusivement sur le fondement de votre consentement explicite** (articles 6(1)(a) et 9(2)(a) du RGPD).

C'est le seul fondement: ni l'exécution d'un contrat, ni l'intérêt légitime ne rendent licite par eux-mêmes le traitement d'une catégorie particulière de données.

## Votre consentement et son retrait

La vérification est volontaire. Vous avez le droit de retirer votre consentement à tout moment, en écrivant à privacy@earth-lings.org.

**Ce qui se passe au retrait:**

- le traitement des données biométriques cesse (après la vérification, elles ne sont de toute façon pas conservées); le résultat de la vérification (section 04) est conservé: il ne constitue pas une donnée biométrique;
- **le hachage irréversible d'unicité est lui aussi conservé.** Il est calculé à partir des données du document et non de la biométrie, il ne relève donc pas du consentement de l'article 9 du RGPD et est conservé sur un autre fondement. Sans lui, une même personne pourrait obtenir un second passeport avec les mêmes données de document: le hachage permet de déceler une telle tentative, y compris de sa part, et un passeport délivré en contournant la vérification est annulé (Déclaration, article 8);
- le retrait du consentement n'affecte ni l'appartenance ni le droit de vote, et le compte n'est pas supprimé de ce fait; pour qui appartient au peuple, la suppression du compte ne va qu'avec la sortie;
- **c'est vous qui détruisez le passeport**, avec votre propre clé, si vous décidez de sortir: le retrait du consentement ne détruit pas le passeport.

> **Nous n'avons pas le droit de détruire votre passeport à votre place.** La Charte (article 21) n'admet la destruction du passeport par une personne autre que son titulaire que dans deux cas: l'annulation d'une délivrance non valide par décision de l'Assemblée et la réémission technique à votre propre demande; contre votre volonté, le passeport ne peut être détruit que dans le premier de ces cas. Le retrait du consentement ne figure pas parmi ces cas, et la plateforme ne conserve pas vos clés; mais tant que les droits du propriétaire du contrat ne sont pas transférés à une signature multiple, l'émission et la destruction d'un passeport restent techniquement accessibles à une seule clé (document « Où nous en sommes »). L'inscription au registre demeure après le retrait du consentement. Avant l'adoption de la Déclaration, il n'y a pas d'Assemblée (Charte, article 38), et le document temporaire de participant à la constitution est détruit contre la volonté de son titulaire selon la procédure du document « La période constituante » (partie 2, point 5).

---

# SECTION 03. Les conditions d'obtention du statut

- **âge** - avoir atteint 18 ans;
- **consentement** - signature volontaire de la Déclaration;
- **vérification d'identité** - confirmation de l'unicité;
- **passeport** - émission d'un jeton intransmissible à votre adresse; le passeport atteste le statut qui naît de la signature de la Déclaration.

## Quelles données sont nécessaires

La liste complète et les fondements juridiques figurent dans la Politique de confidentialité. La vérification exige:

- **un pseudonyme** - à votre choix, utilisé dans le passeport et pour la connexion à la plateforme;
- **une adresse électronique** - pour le contact;
- **le contrôle du document et du visage** - avec le prénom et le nom en caractères latins tels qu'ils figurent dans le document; en outre, le pays de résidence est indiqué et l'âge de 18 ans révolus est confirmé.

**Les nom et prénom réels ne sont pas conservés.** Les données du document ne sont utilisées qu'au moment de la vérification, pour comparer le visage au document et confirmer l'unicité; une fois celle-ci achevée, il n'en subsiste que le type et le pays de délivrance du document et des hachages irréversibles. Votre pseudonyme demeure le nom sous lequel les autres participants vous voient.

## Ce que donne le statut

- **le passeport** - attestation de l'appartenance au peuple;
- **le droit de vote** à l'Assemblée DAO: une personne, une voix;
- **l'accès à l'infrastructure** - participation aux projets, services, coordination;
- **le droit de faire des propositions** et de participer aux décisions sur chaque question.

> **Ce que le statut ne donne pas.** Le passeport ne donne ni nationalité ni résidence, aucun droit de visa, aucune force devant les administrations, et ne remplace pas les documents de votre pays. Le peuple des Earthlings ne possède pas la personnalité juridique internationale et ne peut représenter les intérêts de quiconque devant des juridictions ou des organes de l'État. La liste complète figure dans les documents [Le chemin de l'earthling](https://earth-lings.org/documents/fr/fr14-chemin-de-l-earthling.html) et [Passeport SBT](https://earth-lings.org/documents/fr/fr15-passeport-sbt.html).

---

# SECTION 04. Comment se déroule la vérification

**Document → visage → contrôle de présence vivante → comparaison document/visage → résultat → conservation du résultat**

## Ce qui est vérifié

- **le document** - comparaison des données avec un document officiel d'identité;
- **la géométrie du visage** - points clés et proportions;
- **la présence vivante** - il s'agit aujourd'hui d'un contrôle passif de base, effectué sur une seule prise de vue du visage: il est conçu pour déceler des falsifications simples - la prise de vue d'une photographie ou d'un écran -, ne protège ni contre les enregistrements vidéo ni contre les masques, et la prise de vue peut être téléversée sous forme de fichier. Le contrôle suivant le modèle de détection des attaques par présentation décrit dans la norme ISO/IEC 30107 n'est pas encore mis en place; le niveau de résistance annoncé et les résultats d'une vérification indépendante seront publiés lors de sa mise en place.

## Le déroulement

1. **Réception** de l'image du document et du visage par une connexion protégée.
2. **Contrôle de présence vivante.**
3. **Extraction des caractéristiques** - données du document et points clés du visage.
4. **Construction d'un gabarit mathématique** - un ensemble de nombres décrivant les caractéristiques. Le gabarit n'existe qu'en mémoire vive pendant la durée de la vérification.
5. **Comparaison** de la biométrie avec le document et contrôle de l'unicité.
6. **Conservation du résultat** - sans images ni gabarits.

> **Ce qui subsiste après la vérification.** Les photographies, les scans de documents et les gabarits biométriques **ne sont pas conservés**. Subsistent: l'état de la vérification, le type et le pays de délivrance du document, les scores numériques de la vérification, les motifs de refus et des hachages irréversibles, calculés avec la clé secrète du serveur, du numéro du document, du prénom, du nom et de la date de naissance figurant dans le document.
>
> Les hachages n'interdisent pas de revenir. Ils empêchent seulement une même personne de détenir deux passeports valides en même temps: lors d'une nouvelle adhésion, le système trouve la correspondance, s'assure que l'ancien passeport a été détruit et en délivre un nouveau.

> **Précisément, sur le statut des hachages.** Un hachage est irréversible et se calcule avec la clé secrète du serveur: on ne peut pas en tirer un nom ou un numéro de document, et sans la clé on ne peut pas davantage les retrouver par force brute. Mais il permet de **distinguer une personne déterminée** des autres, sans quoi il ne remplirait pas sa tâche. Selon le RGPD, il s'agit donc de données **pseudonymisées et non anonymes**, et la protection des données personnelles leur est applicable dans son intégralité. Nous ne les qualifions pas d'anonymisées, car ce serait inexact.

---

# SECTION 05. La protection des données

Les mesures générales sont décrites dans la Politique de confidentialité; ci-dessous, celles qui sont propres à la biométrie.

**Transmission protégée.** Toutes les données sont transmises par des canaux protégés, avec un chiffrement de bout en bout entre votre appareil et les serveurs du système de vérification.

**La clé des hachages.** Les hachages sont calculés avec la clé secrète du serveur (HMAC-SHA256); la clé est conservée hors de la base de données. Il n'y a pas de chiffrement des données conservées au niveau de l'application.

**Un seul espace de stockage.** Les hachages et les résultats de vérification sont conservés dans la même base que les données du compte; les données de la plateforme se trouvent dans une base distincte.

**Suppression immédiate des éléments d'origine.** Les photographies et les scans sont supprimés dès l'achèvement de la vérification.

**Contrôle des accès.** L'accès aux données de vérification n'appartient qu'aux administrateurs, par une clé d'administrateur; il n'y a pas encore d'authentification à plusieurs niveaux, et les accès ne sont pas tous journalisés.

> **Philosophie de la sécurité:** moins il y a de données conservées, moins il y a à voler. Nous ne conservons ni images, ni gabarits biométriques, ni nom, ni numéro de document; ce qui est conservé est énuméré à la section 09 et dans la Politique de confidentialité.

---

# SECTION 06. Vos droits

Les droits généraux du participant figurent dans la Politique de confidentialité et dans les Conditions d'utilisation. Ci-dessous, ceux qui sont propres à la biométrie.

**Retirer votre consentement** - à tout moment; les modalités et les conséquences sont décrites à la section 02.

**Repasser la vérification.** Si votre apparence a beaucoup changé et que la vérification ne vous reconnaît pas, vous la repassez. Le gabarit n'est pas « mis à jour » pour autant: il n'est conservé nulle part, et la comparaison se refait chaque fois à partir de zéro.

**Exiger un réexamen par un être humain.** Un refus automatique n'est pas définitif (article 22 du RGPD). Vous avez le droit d'exposer votre position et de contester le résultat. Après deux tentatives automatiques infructueuses, le réexamen par un être humain a lieu **sans demande distincte**. Le nombre de nouvelles demandes n'est pas limité.

**Déposer une réclamation** auprès de l'autorité de contrôle de la protection des données de votre pays; les modalités figurent dans la Politique de confidentialité.

## Ce qui se passe à la sortie

- la destruction du passeport ne supprime pas par elle-même les données: les données du compte sont supprimées à votre demande et, après cette suppression, subsistent l'adresse du portefeuille, le numéro de l'inscription du passeport, le pseudonyme, le pays, le résultat et les scores de la vérification et les hachages irréversibles;
- les hachages pseudonymisés sont conservés exclusivement pour qu'une même personne ne puisse pas détenir deux passeports valides;
- **le droit de revenir est conservé**: lors d'une nouvelle adhésion, le système s'assure que l'ancien passeport a été détruit et en délivre un nouveau;
- on ne peut pas reconstituer une image à partir des hachages; on ne peut pas non plus y lire un nom ou un numéro de document, et sans la clé secrète du serveur on ne peut pas davantage les retrouver par force brute.

---

# SECTION 07. À quoi sert la vérification

La liste est exhaustive: aucun traitement à d'autres fins n'est effectué.

- confirmation de l'unicité lors de l'inscription;
- délivrance du passeport et, pendant la période constituante, du document temporaire de participant à la constitution;
- attestation du statut de participant;
- mise en œuvre du principe « une personne - une voix » lors des votes;
- accès aux services exigeant un statut vérifié.

> **Ce que nous ne faisons pas.** Nous ne suivons pas les déplacements. Nous n'analysons pas les comportements, hormis la statistique agrégée des visites, qui compte aussi les étapes du formulaire de vérification (Politique de confidentialité, section 04). Nous ne vendons pas de données à des tiers. Nous ne constituons pas de profils publicitaires. Nous n'utilisons pas le système à des fins de surveillance. Nous ne transmettons pas de données aux organes de l'État autrement qu'en vertu d'une décision de justice devenue définitive ou d'une exigence légale équivalente, dont la légitimité est vérifiée dans chaque cas.
>
> Le participant est informé des demandes auxquelles il a été fait droit, sauf si la décision elle-même l'interdit. Un relevé de ces cas est publié dans le rapport de transparence.

---

# SECTION 08. Transparence et contrôle

## Ce qui est ouvert et ce qui est fermé

Le code du contrat intelligent du passeport est ouvert sous licence MIT; dans l'explorateur du réseau, le contrat n'est pas vérifié, et la correspondance entre la source et le contrat déployé doit être vérifiée par soi-même (document « Où nous en sommes »).

**Le code du système de vérification d'identité est fermé**, précisément parce qu'il traite des données personnelles et que sa publication faciliterait le contournement des protections. C'est un choix assumé et non un non-dit; la liste avec les motifs figure dans le document [Où nous en sommes](https://earth-lings.org/documents/fr/fr32-ou-nous-en-sommes.html).

En contrepartie de cette fermeture, nous prenons les engagements suivants:

- un **audit de sécurité indépendant** est prévu avant l'extension des opérations; le rapport est publié;
- la **documentation technique** est accessible à l'étude;
- des **rapports de sécurité** sont publiés régulièrement;
- la **journalisation des accès** aux données de vérification peut être auditée; aujourd'hui, les accès ne sont pas tous journalisés.

## Le contrôle indépendant

Les questions d'éthique du traitement des données biométriques seront soumises au [Conseil indépendant](https://earth-lings.org/documents/fr/fr11-conseil-independant.html), organe non subordonné à ceux qui exploitent la plateforme. Après l'adoption de la Déclaration, tant que le Conseil n'est pas constitué, cette étape est omise et les délais de débat public sur ces questions sont doublés (Charte, article 39); avant l'adoption de la Déclaration, il n'y a pas de Conseil (Charte, article 38).

Après l'adoption de la Déclaration, les propositions de modification de la présente Politique sont soumises au vote de l'Assemblée; avant l'adoption, la décision les concernant est prise par l'auteur de la Déclaration selon la procédure du document « La période constituante » (partie 2, point 2).

---

# SECTION 09. La répartition des responsabilités

## Le système de vérification d'identité

- réception et traitement des données du document et du visage;
- reconnaissance du document avec extraction des données de la zone lisible par machine;
- contrôle de présence vivante;
- comparaison de la photographie avec le document;
- confirmation de l'unicité.

## Le registre du peuple

**Ce qui n'est pas conservé:** les nom et prénom réels; les numéros de passeport et de documents; les dates de naissance exactes; les adresses de résidence; les photographies et les gabarits biométriques; les numéros de téléphone, hors les cas d'authentification à deux facteurs.

**Ce qui est conservé:** le pseudonyme; l'adresse électronique; la confirmation d'avoir 18 ans; le pays de résidence (à des fins statistiques); l'état de la vérification d'identité; le lien avec le passeport; la date d'obtention du statut; l'adresse du portefeuille; l'adresse IP et le type de navigateur au moment de la vérification - pendant douze mois au plus.

## La minimisation

Le registre suit le principe de minimisation des données conformément au RGPD. N'est conservé que ce qui est nécessaire à la confirmation de l'unicité et au lien avec le passeport pour la participation aux décisions; ce qui est conservé exactement figure ci-dessus, dans l'encadré ci-dessous et dans la Politique de confidentialité.

Les photographies et les scans sont supprimés dès la vérification, mais son résultat reste valide et vérifiable.

> **Les nom et prénom réels ne sont pas conservés.** Les données du document ne sont traitées qu'au moment de la vérification. Il reste dans le système de vérification d'identité le pseudonyme, l'adresse électronique, le pays, l'adresse du portefeuille, l'adresse IP et le type de navigateur au moment de la vérification et, de la vérification elle-même, l'état de la vérification, le type et le pays de délivrance du document, les scores numériques de la vérification, les motifs de refus et des hachages irréversibles, calculés avec la clé secrète du serveur, du numéro du document, du prénom, du nom et de la date de naissance figurant dans le document; le pseudonyme n'est pas inscrit au registre public. Votre nom ou votre numéro de document ne peuvent donc être divulgués ni aux autres participants, ni aux administrateurs, ni à des tiers: nous ne les avons pas.

---

# SECTION 10. Questions fréquentes

**Pouvez-vous reconstituer mon visage à partir de ce que vous conservez?**
Non. Le gabarit biométrique n'est pas conservé du tout: la comparaison s'effectue au moment de la vérification, après quoi les données d'origine sont supprimées. Subsistent le résultat de la vérification et des hachages irréversibles dont on ne peut tirer aucune image; on ne peut pas non plus y lire un nom ou un numéro de document, et sans la clé secrète du serveur on ne peut pas davantage les retrouver par force brute.

**Que se passe-t-il si je perds mon téléphone?**
Les données de vérification sont en sécurité. Il n'y a pas d'application: la vérification se fait dans le navigateur. Si le portefeuille a été créé par une connexion avec le courriel, Google ou Apple, il suffit de se connecter de la même façon sur le nouvel appareil. Si l'accès au portefeuille est perdu, le passeport est réémis à une nouvelle adresse sur votre demande, et l'appartenance n'est pas interrompue (Charte, article 21).

**Ma biométrie peut-elle être dérobée?**
La biométrie ne peut pas être dérobée: nous ne la conservons pas. Les hachages que nous conservons sont calculés avec la clé secrète du serveur à partir des données du document et non de la biométrie, et ils ne contiennent aucune image du visage.

**Faut-il obligatoirement indiquer son vrai nom?**
Pour la vérification, oui: le prénom et le nom tels qu'ils figurent dans le document sont nécessaires à la comparaison avec celui-ci. Les nom et prénom réels ne sont pas conservés. Les données du document ne sont contrôlées qu'au moment de la vérification; après celle-ci, il n'en subsiste que le type et le pays de délivrance du document et des hachages irréversibles. Dans les échanges quotidiens, vous êtes connu par votre pseudonyme.

**Qu'advient-il des données à la sortie?**
La destruction du passeport ne supprime pas par elle-même les données: les données du compte sont supprimées à votre demande et, après cette suppression, subsistent l'adresse du portefeuille, le numéro de l'inscription du passeport, le pseudonyme, le pays, le résultat et les scores de la vérification et les hachages irréversibles. Les hachages pseudonymisés sont conservés exclusivement pour qu'une même personne ne puisse pas détenir deux passeports valides. Cela n'empêche pas de revenir.

**Que faire si mon apparence a beaucoup changé?**
Repasser la vérification. Il n'existe pas de gabarit conservé qu'il faudrait mettre à jour.

**Et si la vérification est rejetée?**
Les motifs d'un refus automatique sont affichés sur l'écran de vérification - pour l'instant sous forme de codes techniques -, et la décision prise après le réexamen par un être humain est envoyée par courriel. Vous pouvez recommencer après les avoir levés, par exemple avec des images de meilleure qualité ou un autre document. En cas de désaccord, vous avez le droit d'exiger un réexamen par un être humain et, après deux tentatives automatiques infructueuses, le réexamen par un être humain a lieu sans demande distincte.

**Qui a accès à mes nom et prénom réels?**
Personne: ils ne sont pas conservés. Le peuple ne peut techniquement pas divulguer des données dont il ne dispose pas.

**Transmettez-vous des données aux États?**
Uniquement en vertu d'une décision de justice devenue définitive ou d'une exigence légale équivalente; les modalités et l'information du participant sont décrites dans la [Politique de confidentialité](https://earth-lings.org/documents/fr/fr28-politique-de-confidentialite.html).

---

# SECTION 11. Les modifications de la Politique

La Politique est mise à jour à mesure que les technologies et la législation évoluent. Les modifications sont publiées avec l'indication de la date d'entrée en vigueur.

Les modalités de modification - notification par courriel au moins 30 jours à l'avance, notification sur la plateforme à la connexion suivante, publication de la liste des modifications et droit d'objecter - sont établies par la Politique de confidentialité.

---

**Pour toute question relative à la vérification d'identité:** privacy@earth-lings.org
