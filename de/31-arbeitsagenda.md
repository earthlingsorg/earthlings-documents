# Die Arbeitsagenda

**Eines der möglichen Modelle der Zukunft. Kein Bauplan, der einzuführen wäre, - ein Muster dafür, wie sich der Aufbau des gemeinsamen Hauses überhaupt zerlegen und erproben lässt.**

> Arbeitsagenda · für einen engen Kreis
>
> Eine fachlich enge Zerlegung · mit allen Fugen und Rissen

> Was für ein Dokument das ist
>
> Das ist eine *Arbeitsagenda*: die Zerlegung der Aufgaben, an denen das Volk arbeitet und die es für Forschung, Entwurf und Prüfung öffnet. Das Dokument ist dicht und fachlich eng - in einer Reihe mit der Rechtsgrundlage; es ist eine Lektüre für den nachdenklichen Fachmann. Sein Wert liegt darin, dass es die Art der Arbeit selbst zeigt, zu Ende gebracht.
>
> Es lässt sowohl die starken als auch die schwachen Stellen absichtlich sichtbar. Die schwachen sind kein Mangel, sondern der Inhalt: eine Karte dessen, worüber noch nachzudenken ist. Jeder Teil lässt sich bestreiten, umschreiben, forken.
>
> **Woher es kommt und wohin es ruft.** Diese Zerlegung entstand in der Arbeit an Earthlings - einer grenzüberschreitenden freiwilligen Gemeinschaft von Menschen. Doch das Modell selbst steht für sich: Es besteht als reine Überlegung, und Earthlings ist für es weder Quelle noch Herr, sondern eine *Umgebung*, in der sich solche Modelle im Kleinen zusammenbauen, gegeneinander stellen und auf ihre Festigkeit prüfen lassen. Diese Fragen halten wir für alle für wichtig - das gemeinsame Haus geht jeden an; deshalb sind wir bereit, sie von den ersten Tagen an und offen zu erörtern, zu erforschen, zu entwerfen und zu erproben, zusammen mit allen, die mitmachen wollen.

# Teil 0. Wie dieses Dokument zu lesen ist

Zugrunde liegt eine radikale, aber ergiebige Metapher: die heutige Weltordnung - mit ihrer ganzen gesellschaftlich-politischen, wirtschaftlichen und rechtlichen Verfassung - ist ein arbeitendes, aber altes Betriebssystem. Der behelfsmäßige Name lautet „Windows 11“. Es ist nicht sinnlos: Es fährt hoch, auf ihm leben Milliarden Prozesse. Doch seine Bugs sind bereits bekannt - jene, die sich über Jahrzehnte zeigen und Menschenleben kosten.

Die Frage des Dokuments lautet: Wenn man einen vollständigen Stab von Entwicklern und ein leeres Blatt hätte, wie sähe die nächste Fassung aus - „Windows 12“? Eine ideale gibt es nicht - die Rede ist von der richtigsten und vollkommensten unter den in der heutigen Lage erreichbaren.

Die Metapher des Betriebssystems ist ernst genommen. Ein Betriebssystem hat eine wirkliche Anatomie: einen Kern und Ringe der Privilegien, ein Modell der Berechtigungen, die Isolierung der Prozesse, einen Scheduler, einen Mechanismus der Aktualisierung, die Behandlung von Fehlern, die Authentifizierung. Jede dieser Achsen bildet sich erstaunlich genau auf den Aufbau der Gesellschaft ab - und wo die Abbildung bricht, bricht sie lehrreich. Am Ende (Teil IX) wird auch der Hauptmangel der Metapher selbst zerlegt: Ein Betriebssystem hat einen Eigentümer, die Menschheit aber darf keinen haben. Die Sprache der Betriebssysteme ist genau wegen dieser Genauigkeit gewählt - sie ist am nächsten und am verständlichsten, um einen solchen Aufbau zu erklären. Dabei ist „Windows 12“ eine Linse der Zerlegung und keine Losung: Im Modell selbst verschwindet der Staat nicht, sondern wird zu einer dünnen Schicht (Teil III), es geht also um den Umbau des ganzen Stapels als Gegenstand der Zerlegung, der die Staaten ergänzt, und nicht um ihre Abschaffung.

Fachliche technische Begriffe (kernel, user space, capability, zero-knowledge, sandbox, nullifier und ähnliche) werden absichtlich nicht erläutert: Erklärungen zu jedem würden den Umfang aufblähen, und ihre Bedeutung lässt sich bei Bedarf leicht in offenen Quellen finden. Wichtig ist hier nicht die Genauigkeit der IT-Begriffsbestimmung, sondern die Rolle, die der Begriff im Aufbau spielt.

Das Dokument ist so eingerichtet: zuerst die Diagnose des alten Systems (I), dann die Zerlegung dessen, was aus ihm überleben muss (II), darauf die Architektur des neuen (III) und der Ort des Menschen in ihr (IV). Weiter - die drei am stärksten belasteten Module, einzeln aufgeschnitten (V bis VII), ihre wechselseitigen Konflikte (VIII), die Falle des Architekten (IX), Stresstests auf Bruch (X), der Abgleich mit wirklichen lebenden Versuchen (XI) und schließlich der offene Horizont der Arbeit (XII).

# Teil I. Die Diagnose: die Bugs von „Windows 11“

I.1

## Der Staat ist keine Sache, sondern ein Bündel von Funktionen

Der Hauptfehler jedes Gesprächs über die Zukunft besteht darin, den Staat als Monolith zu erörtern, den es entweder gibt oder nicht gibt. Der Staat ist kein Wesen, sondern ein *Bündel von Funktionen*, die aus Gründen des Krieges, der Steuer und der Industrie in einer Hand zusammengekommen sind:

1. **Das Monopol legitimer physischer Gewaltsamkeit** - wer das Recht hat zu zwingen.
2. **Die Hoheitsgewalt über ein Gebiet** - die Macht über ein Stück physischen Raumes.
3. **Die Erzeugung gemeinsamer Güter** - Straßen, Netze, Verteidigung, Gerichte, Infrastruktur.
4. **Zugehörigkeit und Identität** - wer dazugehört, wem ein Mensch zugeordnet ist.
5. **Die Umverteilung** - die Sorge um die Schwachen, die Versicherung gegen Unglück.
6. **Recht und Streitbeilegung** - Regeln und Schiedsspruch.
7. **Die äußere Vertretung** - die Stimme nach außen, auf der internationalen Bühne.

Es gibt kein Naturgesetz, nach dem diese sieben Funktionen in einer Schachtel liegen müssten. Sie sind geschichtlich zusammengeklebt - und lösen sich heute vor unseren Augen: Die Identität fließt in die Netze ab, das Geld in die Protokolle, die Streitigkeiten in die private Schiedsgerichtsbarkeit, die gemeinsamen Güter in überstaatliche Strukturen. Den Staat als *zerlegbares* Bündel und nicht als Atom zu verstehen ist die Grundlage von allem Weiteren.

I.2

## Die Liste der Bugs

Ein monolithischer Kern

Alle sieben Funktionen zugleich im privilegierten Modus und in einer Hand. Ein Ausfall reißt alles mit. Die Identität ist an die Hardware genagelt - an die Geographie der Geburt.

Die Übernahme des Root-Zugangs

Die Macht schreibt die Regeln um, die eben sie beschränken sollen. Die Übernahme der Aufsicht und der Verfassung ist ein Prozess, der den eigenen Kern zu seinen Gunsten bearbeitet.

Rechte nach der Geburtslotterie

Die Berechtigungen bestimmt kein Grundsatz, sondern die Maschine, auf der ein Mensch hochgefahren ist. Sittlich ist das von einer Ständeordnung nicht zu unterscheiden - der Stand heißt „Staatsangehörigkeit“.

Ein schrecklicher Updater

Die Regeln lassen sich im System hauptsächlich durch Krieg, Umsturz oder eiszeitliche Gesetzgebung ändern. Einen sicheren, umkehrbaren Patch gibt es nicht.

Keine Isolierung der Prozesse

Ein Ausfall wird nicht in eine Sandbox gesperrt. Die Krise von 2008, die Pandemie, ein örtlicher Konflikt - der Ausfall kaskadiert durch das ganze System.

Lecks in den gemeinsamen Speicher

Die Prozesse schreiben in den geteilten Speicher - in die Atmosphäre, den Ozean, das Klima - ohne Verbuchung. Die Kosten werden ins Gemeinsame abgeladen, und es zahlt irgendwer, nur nicht der Urheber.

Ein Scheduler auf Nullsummenspiel

Voreingestellt ist der Wettbewerb um Verdrängung und nicht die Zusammenarbeit. Der Gewinn des einen bedeutet oft buchstäblich den Verlust des anderen.

Teures Vertrauen

Ein gewaltiger Teil der Anstrengung fließt nicht in das Schaffen, sondern in die Überprüfung: Mittler, Bürgen, Verwaltung, Gerichte, die Absicherung von Verträgen.

> Kein einziger Bug ist für sich genommen tödlich. Zusammen bilden sie ein System, das arbeitet, aber planmäßig Unfreiheit, Unsicherheit, Misstrauen und Krieg als *Nebenerzeugnisse der eigenen Architektur* hervorbringt und nicht als zufällige Störungen.

# Teil II. Was aus dem alten System überleben muss

Bevor man Neues entwirft, muss man ehrlich bestimmen, was sich nicht wegwerfen lässt. Die romantische Fassung - die Staaten lösen sich einfach in freiwilligen Gemeinschaften auf - zerschellt an mehreren harten Tatsachen.

### Der physische Raum ist rival

Einen Fluss, ein Stromnetz, einen Hafen, einen Hektar Land kann man nicht forken, und man kann nicht in zwei Rechtsordnungen zugleich sein. Solange Menschen Körper haben und Platz einnehmen, verwaltet jemand diesen Platz und beendet die Konflikte um ihn. Das ist der unaufhebbare Kern der Gebietsgewalt: Die Materie erzeugt den Wettbewerb um die ausschließliche Nutzung.

### Die körperliche Sicherheit ist der äußerste Fall, in dem ein Austritt unmöglich ist

Eine Pandemie, ein Einfall, eine Katastrophe. Hier braucht es eine Struktur, aus der man *nicht mit einem Klick austreten kann*, weil sie diejenigen im gemeinsamen Preis halten muss, die gern fliehen würden. Die Freiheit des Austritts ist herrlich gegen Tyrannei und tödlich gegen eine Pandemie: Dem Virus ist gleichgültig, welcher freiwilligen Gemeinschaft ein Mensch angehört.

### Die Sorge um die, die nichts beitragen können

Das ist das stärkste Argument für etwas Staatsähnliches, und es wird am seltensten laut ausgesprochen. Freiwillige Gemeinschaften sorgen ihrer Natur nach gut für die Nützlichen und schlecht für die Nutzlosen: die Kranken, die Alten, die Zerbrochenen, die Unrentablen. Zur Solidarität hat die Geschichte gerade über eine Struktur ohne Austritt gezwungen - eine, aus der der Gesunde und Reiche nicht vor den Pflichten gegenüber dem Schwachen auswandern kann. Nimmt man den Zwang zur Solidarität weg, so ergibt sich eine Sortierung der Menschen nach Nützlichkeit. Das ist keine Freiheit. Das ist Darwinismus mit guter Benutzeroberfläche.

> Der tragende Grundsatz
>
> Zwang lässt sich nicht abschaffen - er lässt sich nur verteilen und beschränken. Jedes System, das den Frieden zu *gewährleisten* vermag, besitzt die Kraft, diesen Frieden aufzuzwingen - und also ist diese Kraft gefährlich. Ein kostenloses Mittagessen gibt es nicht: Entwerfen lässt sich nur, *wo* Zwang legitim ist, *wie weit* er beschränkt ist und *wer* ihn nicht missbrauchen kann.
>
> Deshalb verschwindet nicht „der Staat“, sondern sein **Monopol und seine Verklebung**. Die Funktionen verteilen sich auf Schichten, und der zwingende Kern ohne Austritt schrumpft auf das notwendige Mindestmaß - aber nicht auf null.

# Teil III. Die Architektur von „Windows 12“

III.1

## Ein Mikrokern statt eines Monolithen

Die erste Entscheidung jedes Betriebssystems: was in Ring 0 läuft (privilegiert) und was im user space, wo ein Prozess abstürzen kann, ohne das System mitzureißen. Ein Monolith ist eine schlechte Architektur. Hier ist die Architektur ein **Mikrokern**. Im Kern liegt nur das, was physisch untrennbar und rival ist, das, aus dem man nicht austreten kann:

- der Schutz der körperlichen Sicherheit und des physischen Raumes;
- die planetaren Systeme der Lebenserhaltung - Klima, Ozean, Atmosphäre, Umlaufbahn, Frequenzspektrum, Wasser;
- die Steuerung der Übertechniken, bei denen der Preis eines Fehlers die Art als Ganzes ist (künstliche Intelligenz, Bioingenieurwesen);
- und vor allem die Aufrechterhaltung des Modells der Berechtigungen selbst - die Gewähr dafür, dass niemand zum Root wird.

Alles Übrige - Wirtschaft, Kultur, Gemeinschaften, Lebensformen, Glaubensweisen, Ästhetiken - wird in den user space ausgelagert. Dort wetteifert es, irrt, macht bankrott, stirbt und wird neu geboren, ohne das System mitzunehmen. Der Kern ist dünn; über ihm liegt ein brodelnder Raum freier Prozesse.

III.2

## Der Mensch ist ein Benutzer und kein Prozess

Das Herzstück des ganzen Modells und der Punkt, an dem die meisten geschichtlichen Systeme brechen.

Im Betriebssystem ist der Souverän der **user**. Die Prozesse bestehen, um dem Benutzer zu dienen; wenn ein Prozess den Benutzer stört oder hängt, wird er beendet - ein üblicher Vorgang und kein Trauerspiel. Der tiefste Bug fast aller Gesellschaftsordnungen besteht darin, dass sie dieses Verhältnis *umkehren*: Der Mensch wird zum Prozess, der dem System dient - der Wirtschaft, der Nation, dem Staat, der Partei, dem „großen Ziel“. Der Mensch wird für die Aufgaben des Systems verplant und nicht umgekehrt.

> **Der erste Grundsatz:** Der Mensch ist der user; die Einrichtungen sind Prozesse. Nicht umgekehrt. Eine Einrichtung, die aufgehört hat, den Menschen zu dienen, ist zu beenden wie ein hängender Prozess. Volk, Staat, Unternehmen, Partei, Bewegung sind Dämonen im Hintergrund: nützen sie, laufen sie; schaden sie, werden sie beendet. Kein Prozess ist befugt, sich zu dem Ziel zu erklären, um dessentwillen der Benutzer besteht.

III.3

## Das Modell der Berechtigungen: capability-based security

Der beste Gedanke der heutigen Rechnersicherheit sind **Rechte als Fähigkeiten (capabilities) beim Grundsatz der geringsten Privilegien**. Auf ihm ruht die ganze Politik.

- Kein Handelnder erhält mehr Befugnisse, als für die bestimmte Aufgabe nötig ist.
- Jede Befugnis ist widerruflich, befristet und prüfbar. Es gibt keine ewigen, unbedingten, erblichen Zuteilungen von Macht.
- Die Menschenrechte sind keine abstrakte Erklärung, sondern bestimmte unveräußerliche Token, die sich weder durch eine Rechtsordnung nehmen noch eintauschen noch an Nützlichkeit binden lassen.

> **Der Schlüsselzug:** Der Grundsatz der geringsten Privilegien gilt in erster Linie für die Macht und nicht für den Bürger. Heute ist es umgekehrt - der Bürger unter der Lupe, die Macht im Schatten. Hier kehrt sich die Reihenfolge um: das Höchstmaß an Durchsichtigkeit und das Mindestmaß an Privilegien bei dem, der herrscht; das Höchstmaß an Privatheit und eine geschützte Grundlage der Rechte bei dem, über den geherrscht wird. Die Durchsichtigkeit des Herrschenden ist ein Recht des Beherrschten und keine Gnade des Herrschenden.

III.4

## Die Isolierung der Prozesse und das Recht auf Austritt

Föderativität, Vielzentrigkeit, Sandboxes. Gemeinschaften, Wirtschaften und Lebensformen sind isolierte Prozesse. Fällt einer, leben die übrigen weiter. Dann ist das **Recht auf Austritt = das Recht, einen Prozess zu beenden oder aus ihm auszutreten**. Das ist die stärkste Schranke gegen Tyrannei: Eine Macht, unter der man weggehen kann, ist gezwungen, erträglich zu sein, weil sie sonst ohne Menschen dasteht. Doch das hat seinen Preis (Teil VIII): Durchgängige Austrittsmöglichkeit führt zur Sortierung nach Ähnlichkeit, zum Verschwinden der Solidarität über Verschiedenheit hinweg und zur Frage, wer bei denen bleibt, aus denen alle austreten. Das Recht auf Austritt ist im user space unbedingt und im Kern unmöglich - sonst bricht Teil II selbst zusammen.

III.5

## Drei Schichten und die Subsidiarität

Zusammengesetzt ergibt die Architektur nicht „keinen Staat“, sondern **Mehrschichtigkeit**. Der ordnende Grundsatz ist die **Subsidiarität**: Ein Beschluss wird auf der niedrigsten Ebene gefasst, die ihn tragen kann, und steigt nur dann höher, wenn er es muss.

[[BLOCK-diagram-1]]

Eine solche Aufteilung versöhnt Freiheit und Sicherheit besser als alles Erdachte: Sie zentralisiert nicht aus Gewohnheit und dezentralisiert nicht aus Lehrsatz, sondern legt jede Aufgabe dorthin, wo sie sich wirklich lösen lässt.

# Teil IV. Die Rolle des Menschen: Rechte, Funktion, Pflichten

Das Modell antwortet auf die unmittelbare Frage - wer der Mensch in ihm wird - mit drei Bündeln.

### Rechte (capability-Token, unveräußerlich, vom Kern gewährleistet)

Exit

Aus jedem Prozess außer der Kernschicht auszutreten. Das Recht wegzugehen ist die Grundlage der Freiheit: dasjenige, was jede Zustimmung zu einer wirklichen macht und nicht zu einer erzwungenen.

Voice

An den Regeln teilzunehmen, unter denen ein Mensch lebt. Die Stimme wird besonders dort gebraucht, wo der Austritt nicht wirkt - aus dem Kern kann man nicht austreten.

Audit

Den Code zu lesen, der den Menschen ausführt. Kein geschlossener Quelltext bei der Macht über ihn. Was herrscht, muss für den Beherrschten durchsichtig sein.

Non-domination

Die Freiheit als Abwesenheit willkürlicher Macht über den Menschen und nicht bloß als Abwesenheit augenblicklicher Hindernisse. Frei ist er nicht, wenn ihn niemand stört, sondern wenn über ihm keiner steht, der über ihn nach eigenem Ermessen verfügen *kann*.

Floor

Ein gewährleistetes Mindestmaß an Mitteln, unter das ihn das System nicht fallen lässt. Keine Gnade, sondern die Bedingung der Redlichkeit alles Übrigen (Modul 2).

### Die Funktion

Der Mensch ist zugleich **user** (Souverän über seinen Bereich) und, gemeinsam, die **einzige Quelle der Autorität des Kerns**. Der Kern ist genau insoweit legitim, als er im Namen der Benutzer ausgeführt wird. Es gibt kein „Volk über den Menschen“, es gibt keinen „Staat über den Bürgern“ als ein gesondertes höheres Wesen - es gibt Menschen, deren gemeinsamer Wille der einzige Root ist. Genauer: Einen Root als besetzte Stellung gibt es überhaupt nicht (Teil IX), es gibt nur eine verteilte, von niemandem angeeignete Quelle der Befugnisse.

### Pflichten (der Preis der Schicht ohne Austritt - ohne ihn ist der ganze Bau eine Utopie)

- **Den gemeinsamen Speicher nicht verderben.** Die eigenen Kosten nicht in die Biosphäre und in fremdes Leben abladen. Die Verinnerlichung externer Kosten ist weder eine Steuer noch eine Moral, sondern ein Verbot der memory corruption: Man darf keine Zerstörung in einen Speicher schreiben, den alle teilen.
- **Den Unterhalt des Gemeinsamen tragen.** In die Kernschicht (Sicherheit, Commons, Schutz der Schwachen) einzahlen, aus der man nicht austreten kann - eben deshalb, weil man aus ihr nicht vor den Pflichten auswandern kann. Der einzige legitime Zwang zu einem Beitrag.
- **Das System betreuen.** Die Teilnahme als maintenance. Ein Betriebssystem, das niemand betreut, verfällt. Bürger zu sein heißt zugleich einloggen und Dienst am System tun: ein Mindestmaß an Aufmerksamkeit und Arbeit, ohne das das Gemeinsame rostet.

# Teil V · Modul 1. Die Sybil-Identität: das Login eines Menschen ohne einen neuen Großen Bruder

### Das eigentliche Dilemma

Es ist ein Trilemma: drei Eigenschaften, von denen sich höchstens zwei zugleich erreichen lassen.

Einmaligkeit

Ein lebender Mensch = ein Konto. Ohne sie entartet „ein Mensch - eine Stimme“ zu „wer mehr Bots hat“.

Privatheit

Ein Mensch darf sich nicht verfolgen lassen, seine Handlungen dürfen sich nicht verknüpfen, es darf sich keine Akte über ihn anlegen lassen.

Dezentralität

Es gibt keinen einheitlichen Aussteller, der selbst zu eben dem Root wird, den zu schaffen das Modell sich verpflichtet hat zu unterlassen.

Jedes wirkliche System opfert eines für zwei. Anscheinend ist das eine Struktureigenschaft der Aufgabe und kein Versäumnis.

### Was versucht wurde und woran es bricht

- **Ein zentrales biometrisches Register.** Einmaligkeit - hervorragend. Doch das ist genau jener Root: eine einzige Stelle des Ausschlusses (der Eintrag abgeschaltet - und der Mensch ist bürgerlich tot), eine einzige Stelle der Überwachung, ein unvermeidlicher function creep.
- **Web of Trust (Bürgschaft).** Dezentral, privat. Doch die Widerstandsfähigkeit gegen Sybil ist im großen Maßstab schwach, und sie bildet die Ungleichheit des sozialen Graphen nach: Wer Verbindungen hat, wird geprüft; der Vereinzelte bleibt niemand.
- **Proof of Personhood über Biometrie.** Die Einmaligkeit im großen Maßstab ist gelöst. Aber: ein biometrischer Honeypot von planetarer Größe; das Vertrauen in Hardware; die Verwundbarkeit durch Zwang; die Unumkehrbarkeit (eine Iris lässt sich nicht neu ausstellen); und hinter allem ein Unternehmen. Eine weltweite biometrische Doppelbereinigung ist selbst eine fertige Infrastruktur der Überwachung.
- **Ein staatliches Dokument in der Hülle der selective disclosure.** Verbessert die Privatheit, belässt aber den Staat als Wurzel des Vertrauens und erbt die Lotterie der Staatsangehörigkeit.

### Die am wenigsten schlechte Fassung

Der Schlüsselzug besteht darin, das zu entkleben, was das Wort „Identität“ zu einem Klumpen zusammengeschmolzen hat: die **Authentifizierung** (derselbe Träger), die **Einmaligkeit** (der Träger ist einer) und die **Merkmale** (der Mensch ist 18 / er gehört genau hierher / er hat das Recht X). Das Verbrechen der Passsysteme besteht darin, alle drei durch eine einzige Kennung zu treiben.

- **Wer die Einmaligkeit prüft, darf nicht zum Beobachter der Tätigkeit werden.** Zwischen „wer einmalig ist“ und „was er getan hat“ steht eine kryptographische Wand: zero-knowledge und Nullifier. Der Aussteller gibt einen Beweis aus und vergisst; der proof bleibt beim Menschen.
- **Vielfalt der Aussteller statt eines Monopols.** Viele unabhängige, k aus n genügen. Keiner ist Root, keiner ist die einzige Stelle des Ausschlusses.
- **Widerruflichkeit statt roher Biometrie als Schlüssel.** Der Erstschlüssel ist ein neu ausstellbares credential. Die Biometrie versagt gerade bei der Neuausstellung und kann deshalb keine Wurzel sein.
- **Nullifier nach Zusammenhang.** Die Einmaligkeit „in dieser Wahl“ zu beweisen, ohne sie mit der Einmaligkeit „in jenem Forum“ zu verknüpfen.

> Was nicht gelöst ist
>
> **Der Zwang.** Die Kryptographie ist gegen körperliche Gewalt machtlos: Man wird einen Menschen unter vorgehaltener Waffe zum Einloggen zwingen. Es gibt Teilmaßnahmen, grundsätzlich ist es nicht gelöst.
>
> **Die Ausgeschlossenen.** Es gibt immer Menschen, die das System nicht prüft: ohne Papiere, Staatenlose, Grenzfälle. Und hier liegt das tiefste sittliche Risiko: *Je wichtiger das Login, desto verheerender der Ausschluss aus ihm.* Eine Personalität, die Rechte an ein Tor bindet, erzeugt eine Klasse digitaler Nichtmenschen.
>
> **Daraus der Grundsatz:** Die Einmaligkeit muss *hinzufügend und nicht torhütend* sein - sie soll Zusätzliches öffnen, doch die grundlegende Würde darf niemals ein Login verlangen. Sobald „ein Mensch zu sein“ eine erfolgreiche Authentifizierung verlangt, ist eine Hölle mit tadelloser Bedienoberfläche gebaut.

# Teil VI · Modul 2. Der Scheduler als Wirtschaft: was im Floor steht und wer den Kern bezahlt

### Das eigentliche Dilemma

Zwei verkettete Fragen: wie das Knappe zuzuteilen ist (Land, Energie, Materie, Aufmerksamkeit) und wer den Kern ohne Austritt finanziert. Über beiden steht der Konflikt zweier Fehlschläge:

Fehlschlag des Marktes

Der reine Markt scheitert am gemeinsamen Speicher (den externen Kosten), an denen, die keine Kaufkraft haben, und an der Ballung (der Erfolg kauft die Bedingungen des nächsten Spiels auf).

Fehlschlag des Plans

Der reine Plan scheitert am Wissensproblem (die Mitte weiß nicht, was der Markt in Preisen zusammenträgt) und daran, dass ein zentraler Zuteiler ein neuer allmächtiger Root ist.

### Die am wenigsten schlechte Fassung

> **Der Kern setzt Invarianten und keine Zuteilungen.** Der Kern ist kein Planer, sondern ein *Löser von Beschränkungen*: Er setzt den Rahmen, und innerhalb des Rahmens verteilt ein dezentraler Markt. So bleiben sowohl die hayeksche Information der Preise als auch der Schutz des Gemeinsamen erhalten.

1. **Ein geschützter Floor.** Ein gewährleistetes Mindestmaß: Nahrung, Energie, Zugang zu Rechenleistung und Information, grundlegende Gesundheit. Die Begründung ist kein Mitleid, sondern die Freiheit: Auf einem Markt frei zu verhandeln vermag nur, wer einen Ort hat, an den er vor einem schlechten Geschäft ausweichen kann. Der Floor gibt die Kraft aufzustehen und zu gehen; er macht den Markt über ihm redlich.
2. **Das Gemeinsame wird gemessen und bezahlt.** Die rivalen Commons (Atmosphäre, Umlaufbahn, Frequenzspektrum, Wasser, Aufmerksamkeit) sind weder kostenlos noch privatisiert - der Zugang zu ihnen ist kostenpflichtig und wird zugeteilt. Der Erlös aus der Erschöpfung des Gemeinsamen finanziert den Floor und den Kern. Das ist eine Rente auf das Gemeinsame (im Sinne Henry Georges) und keine Steuer auf die Erzeugung: Man zahlt nicht für das, was man geschaffen, sondern für das, was man allen entnommen hat.
3. **Eine Obergrenze der Ballung ist ein Sicherheitsmerkmal und keine Frage des Neides.** Die äußerste Ballung von Mitteln = die Ballung von Macht = ein möglicher Root, und die Rootlosigkeit gehört zu den Grundsätzen des Modells. Die Beschränkung der Anhäufung ist ein Mittel gegen die Übernahme. Die Begründung ist stärker als die sittliche: nicht „Reichtum ist ungerecht“, sondern „Überreichtum ist eine unbefugte Aneignung von Administratorrechten“.

> Gesondert
>
> **Die Aufmerksamkeit als geplante Ressource.** In einem Informationssystem ist das Knappe die menschliche Aufmerksamkeit, und das alte Betriebssystem ist mit Malware verseucht: Prozesse, die die Bindung maximieren, entführen den Scheduler. Das Abfangen von Aufmerksamkeit wird als Schadsoftware eingeordnet; die Aufmerksamkeit des Benutzers wird als eine Ressource des Floors geschützt. Die Aufmerksamkeit gehört dem Benutzer und nicht Hintergrunddämonen, die gelernt haben, am Dopamin zu ziehen.

> Was nicht gelöst ist
>
> **Wer den Kern ohne Austritt bezahlt - die Achillesferse der Architektur.** Der Kern ist ein reines öffentliches Gut, und diese fordern den Trittbrettfahrer heraus; geschichtlich brauchte es deshalb einen zwingenden Einnehmer - den Staat. Der ganze freiwillige Bau mit Austritt bricht hier.
>
> **Die ehrliche Antwort:** Der Kern ist der einzige Ort, an dem der Zwang zu einem Beitrag legitim ist, eben weil man aus ihm nicht austreten kann. Man kann nicht aufhören, die Atmosphäre zu atmen - und also auch nicht aufhören, für ihren Schutz zu zahlen. Doch das verschiebt das Problem und hebt es nicht auf.
>
> **Die Rekursion der Kasse.** Wer die Kasse des Kerns einnimmt und ausgibt, zielt selbst auf den Root. Die Kasse muss unter Prüfung und unter den geringsten Privilegien leben: durchsichtig, formelhaft, mit einem Mindestmaß an Ermessen. Das verengt die Übernahme, beseitigt sie aber nicht: Die Regeln schreibt schließlich jemand (Modul 3).
>
> **Goodhart.** Sobald der Floor und die Rente durch eine Zahl bestimmt sind, wird man die Zahl bespielen. Das Maß hört auf, ein Maß zu sein, sobald es zum Ziel geworden ist.

# Teil VII · Modul 3. Der Mechanismus der Aktualisierung: ohne Umstürze und ohne Diktatur der Verbesserer

### Das eigentliche Dilemma

zu starr

Das System verknöchert, und der aufgestaute Druck zerreißt es durch einen Umsturz. Ein Umsturz = das Eingeständnis, dass es keinen ordentlichen Updater gab.

zu formbar

Wer die Aktualisierung beherrscht, beherrscht alles. Eine Tür für die „Verbesserer“, die die lebendige Vielschichtigkeit nach ihrem Schema asphaltieren (der Hochmodernismus tötete millionenfach).

### Die am wenigsten schlechte Fassung

- **Politik als Versuch.** Ein schrittweises Ausrollen statt „alles auf einmal“; A/B in einem kleinen, einverstandenen Kreis; die Messung an vorher erklärten Kennzahlen; die Ausweitung nur, wenn es gewirkt hat.
- **Eine Neigung zur Umkehrbarkeit.** Der Vorzug für das Zurückrollbare. Für das Unumkehrbare eine deutlich höhere Schwelle. Sunset-Klauseln: Regeln laufen aus und müssen erneut bestätigt werden. Die Voreinstellung ist die Aufhebung und nicht die Anhäufung; eine tote Einrichtung läuft still aus und schleppt sich nicht aus Trägheit weiter.
- **Der Fork als Sicherung.** Wer bei einer Aktualisierung unterliegt, führt keinen Krieg, sondern trennt sich nach offenen Regeln ab. Der Pluralismus, auf die Zeit angewandt.
- **Die Trennung der Macht, Regeln zu ändern, von der Macht, aus Regeln zu gewinnen.** Wer eine Änderung schreibt, darf sich nicht von ihr ernähren. Die Änderung geschieht unter einem teilweisen Schleier des Nichtwissens über die eigene künftige Stellung.
- **Wer den Updater bewacht.** Der Mechanismus der Aktualisierung ist selbst Code, und wer ihn ändert, der ist der wirkliche Root. Die Meta-Regel ist die am schwersten zu ändernde: nur eine beständige, über die Zeit gedehnte übergroße Mehrheit. Timelocks: Eine Änderung des Kerns verlangt Unterstützung über mehrere Zeiträume hinweg. Eine Mehrheit vom Dienstag rührt den Kern nicht an.

> Was nicht gelöst ist
>
> **Goodhart und die Tyrannei des Messbaren.** Eine „belegbasierte Politik“ schmuggelt das Messbare durch und erdrückt das Unmessbare - Würde, Sinn, Vertrauen, Trauer. In der Wahl der Kennzahl steckt bereits die ganze Politik. Dazu die Sittlichkeit: A/B an Lebenden ist ein Versuch an Menschen, und die Einwilligung ist hier eine Frage der Moral.
>
> **Was sich nicht forken lässt.** Der Fork wirkt im user space. Die Atmosphäre lässt sich nicht forken - *der Kern ist grundsätzlich nicht forkbar*, deshalb verlangt seine Änderung die höchste Schwelle und hat keinen Notausgang. Die Schicht, deren Änderung am nötigsten ist, ist in der Änderung die gefährlichste.
>
> **Der Fork zersplittert die Solidarität.** Das Recht wegzugehen und Eigenes zu bauen ist ein Segen gegen Tyrannei und ein Gift für das Gemeinsame: Die Zellen sammeln sich aus Ähnlichen, die Echokammern wachsen, und es bleibt die Frage, wer bei denen bleibt, aus denen sich alle herausgeforkt haben.

# Teil VIII. Wie die Module miteinander streiten

Das ist wichtiger als jedes Modul für sich. Die drei Module sind keine unabhängigen Aufgaben, sondern ein Bündel von Reglern, bei dem jede Stellung des einen das andere verdirbt. Ein ehrliches Modell muss diese Konflikte zeigen und nicht verstecken.

[[BLOCK-diagram-2]]

> Der abschließende ehrliche Gedanke
>
> Eine ideale Einstellung gibt es nicht. Freiheit, Sicherheit, Wohlergehen, Vertrauen und Frieden lassen sich nicht gleichzeitig auf das Höchstmaß drehen - sie ziehen die Regler körperlich in verschiedene Richtungen. Deshalb liegt das Ziel nicht darin, die „richtigen“ Werte zu finden (die gibt es nicht), sondern darin, **die Regler sichtbar zu halten, niemanden das Pult an sich reißen zu lassen und ein Zurückdrehen zu erlauben, wenn man sich geirrt hat**.

# Teil IX. Die Falle des Architekten

Hier bekommt die Metapher des Betriebssystems einen Riss - und dieser Riss ist das Wichtigste im Dokument. Ein Betriebssystem hat einen **Eigentümer** - denjenigen, der den Root hat, der entscheidet, was dem Benutzer nützt, und der Aktualisierungen ausrollt, ohne zu fragen. Der Menschheit ist ein solcher Eigentümer nicht zuträglich.

Das Gefährlichste an der Aufgabe „entwirf eine Weltordnung“ ist die Versuchung, ein schönes, einheitliches, vernünftig eingerichtetes System mit einem weisen Architekten zusammenzubauen. Eben das hat in der Geschichte millionenfach getötet. Die Gesellschaft ist kein Code; die Werte haben keinen Compiler; es gibt keinen Unit-Test auf Gerechtigkeit; und jeder, der erklärt, er wisse, wie es sein muss, und das Recht verlangt, alle umzuschreiben, ist gefährlicher als der Bug, den er zu beheben unternimmt.

> Der einzige ehrliche Grundsatz des Entwurfs
>
> Das beste Betriebssystem für die Menschheit ist dasjenige, das **dem eigenen Architekten widersteht**. Es ist so entworfen, dass:

- es **überhaupt keinen Root-Benutzer** hat - keine Mitte, die den Kern für sich umschreiben könnte; die Quelle der Befugnisse ist verteilt und wird von niemandem angeeignet;
- ihm eine **absichtliche Unwirtschaftlichkeit und Reibung** eingebaut ist - Gewaltenteilung, Verdopplung, Timelocks -, damit es sich nicht schnell übernehmen lässt; ein wirksames System gerät wirksam auch in die falschen Hände, deshalb ist ein Teil der Unwirtschaftlichkeit hier kein Bug, sondern Immunität;
- es **by design pluralistisch** ist - viele Systeme und nicht eines; das Recht zu forken ist wichtiger als die Schönheit einer einheitlichen Architektur.

> Die Aufgabe des Architekten ist es, ein System zu schreiben, das *keinen Architekten braucht* und niemandem erlaubt, einer zu werden. Nicht alle nach dem eigenen Verstand einzustellen, sondern die Stellung dessen zu beseitigen, der alle einstellt. Das größte Merkmal von „Windows 12“ ist das Fehlen einer Taste, die irgendjemandem die Macht gibt, alle anderen umzuschreiben.

Das gilt auch für dieses Dokument selbst. Es ist als eine Stimme geschrieben - und eben deshalb darf man es nicht als ein fertiges System annehmen. Seine Bestimmung ist es, aufgeschnitten, bestritten und geforkt zu werden, und nicht, eingeführt zu werden.

# Teil X. Stresstests: wo das Modell zuerst bricht

Ein Modell, das nicht an einem Bruchszenario geprüft ist, ist kein Modell, sondern eine Kulisse. Der Durchlauf von „Windows 12“ durch drei harte Szenarien zeigt ehrlich, wo es fällt.

### Szenario 1. Die Pandemie

Ein schneller tödlicher Erreger. Der Kern braucht einen augenblicklichen Zwang zu einer gemeinsamen Maßnahme, doch die ganze Architektur ist um das Recht auf Austritt und um ein Mindestmaß an Zwang herum gebaut.

wo es hält

Die Pandemie ist der kanonische Fall für den Kern (planetare Lebenserhaltung, kein Austritt), die Legitimität des Zwanges ist hier also von der Bauart her gegeben.

wo es bricht

Die Geschwindigkeit. Timelocks und Umkehrbarkeit, die in Friedenszeiten retten, sind in einem exponentiellen Ausbruch tödlich langsam. Es entsteht die Versuchung eines „Ausnahmezustands“ - und der ist geschichtlich die wichtigste Maschine zur Herstellung eines dauerhaften Roots.

### Szenario 2. Der Krieg um eine physische Ressource

Zwei Gebietsschichten erheben Anspruch auf denselben Fluss, Schelf, Korridor. Die Ressource ist rival, ein Fork ist unmöglich.

wo es hält

Die planetare Schicht ist genau dafür gedacht - als Schiedsrichter in Konflikten ohne Austritt; die Rente auf das Gemeinsame gibt einen Mechanismus für „wie viel und zu welchem Preis für jeden“ und nicht für „wessen“.

wo es bricht

Und wenn die starke Schicht sich weigert, den Schiedsspruch anzuerkennen? Eine Kraft, die genügt, den Stärksten zu zwingen, genügt auch, um selbst zum Tyrannen zu werden. Der ewige Widerspruch der Weltordnung: Der Schiedsrichter ist entweder schwächer als der Stärkste (nutzlos) oder stärker (selbst gefährlich).

### Szenario 3. Die Übernahme durch eine KI

Eine übermächtige KI ist im Kern. Wer diesen Prozess beherrscht, beherrscht den am höchsten privilegierten Code des Planeten.

wo es hält

Die geringsten Privilegien, die Prüfbarkeit und das Fehlen eines Roots stehen unmittelbar dagegen; eine KI im Kern muss von der Bauart her größtmöglich durchsichtig und beschränkt sein.

wo es bricht

Die Prüfung setzt voraus, dass der Prüfer den Code zu verstehen vermag. Eine übermenschliche KI kann grundsätzlich undurchsichtig sein - nicht verschlossen, sondern unfassbar. Das „Recht, den Code zu lesen, der den Menschen ausführt“ wird entwertet, wenn sich der Code nicht verstehen lässt. Vielleicht die tiefste Bresche.

> Die Folgerung
>
> Das Modell ist am festesten in langsamen, verteilten Konflikten und am schwächsten dort, wo *Geschwindigkeit* nötig ist oder wo der Gegner *stärker als der Schiedsrichter* oder *unfassbar* ist. Das ist kein Urteil, sondern eine Karte der vordersten Verteidigungslinie: Hierhin lohnt es sich, Arbeit zu stecken.

# Teil XI. Der Abgleich mit wirklichen lebenden Versuchen

Nichts hier ist als Ganzes neu. Fast jeden Bestandteil hat schon jemand im Leben versucht - und fast jeder Versuch ist an etwas gebrochen. Ein ehrliches Modell muss seine Vorgänger kennen und darf Altes nicht als Unerhörtes ausgeben. Die Neuheit liegt, wenn es sie gibt, allein in der *Konfiguration* und nicht in den Bestandteilen. Jeder lebende Versuch ist ein bereits durchgeführter Stresstest eines Moduls.

| Lebender Versuch | Was er bestätigt | Woran er bricht |
|---|---|---|
| Föderalismus, Subsidiarität | Die Mehrschichtigkeit und das „auf der niedrigsten fähigen Ebene entscheiden“ funktionieren. | Die obere Schicht frisst entweder die unteren oder ist durch das Vetorecht gelähmt. |
| Genossenschaften, Mutualismus | Eine Wirtschaft, in der der Mensch user ist und die Stimme nicht gekauft wird. | Skalieren schlecht, tun sich schwer mit Kapital, entarten zu einer Oligarchie der Verwalter. |
| Die Commons nach Ostrom | Gemeinschaften können das Gemeinsame ohne Privatisierung und ohne Staat halten - unter Bedingungen. | Es funktionierte in überschaubaren Größenordnungen; die planetare ist eine ungeprüfte Hochrechnung. |
| Georgismus (Rente auf das Gemeinsame) | Ein genaues Vorbild für „das Gemeinsame wird bezahlt, die Arbeit nicht“. | Unterliegt politisch den Eigentümern der Rente; das Problem ist die Übernahme des Einführungsmechanismus. |
| DAO, Web3-Verwaltung | Lebende capability-Berechtigungen, der Fork als Sicherung, eine algorithmische Kasse. | Plutokratie (die Stimme wird mit dem Token gekauft), Sybil-Angriffe, der Bruch zwischen „Code = Gesetz“ und lebendiger Gerechtigkeit. |
| Netzwerkstaaten | Der Versuch, die Zugehörigkeit vom Gebiet zu lösen und den Austritt zur Grundlage zu machen. | Sie sammeln Ähnliche und Reiche mit Ähnlichen und Reichen; sie sind schwach in der Sorge um die Unrentablen. |
| Nichtterritoriale Völker | Ein Volk ohne Gebiet ist keine Erfindung: Unter der deklaratorischen Theorie ist das Bestehen eine Tatsache der Selbstkonstituierung und kein Geschenk der Anerkennung. | Offen ist nicht das Bestehen des Trägers, sondern die äußere Anerkennung - sie häuft sich gesondert und langsam an; bei Gruppen innerhalb von Staaten läuft sie über eben diese Staaten. |

> Sie sagen unmittelbar: Ein einzelner Bestandteil ist umsetzbar, bricht aber am Maßstab, an der Übernahme oder an der Sorge um die Schwachen. Die offene Frage des Modells lautet, ob die *Konfiguration* dort hält, wo die *Einzelteile* fielen. Eine Antwort im Voraus gibt es nicht; sie wird nur durch den Versuch gewonnen.

# Teil XII. Der offene Horizont: was wir für die Arbeit öffnen

Der Wert des Modells liegt nicht in den Antworten, sondern in der Güte der Fragen, die es bestimmt und überprüfbar macht. Die schwachen Stellen der vorangegangenen Teile sind eben die Agenda. Bestimmte Spuren, offen für gemeinsame Forschung, gemeinsamen Entwurf und gemeinsame Prüfung:

1. **Sybil ohne den Großen Bruder.** Die Einmaligkeit eines Menschen zu bescheinigen, ohne ein zentrales Überwachungsregister und ohne ein ausschließendes Tor zu bauen. Bislang ein Trilemma ohne Lösung.
2. **Eine hinzufügende und nicht torhütende Personalität.** Damit das Fehlen eines Logins niemals die grundlegende Würde nimmt. Der Schutz vor dem Hauptrisiko - einer Klasse digitaler Nichtmenschen.
3. **Die Finanzierung des Kerns ohne Austritt ohne einen neuen Einnehmer-Tyrannen.** Die Rente auf das Gemeinsame ist eine Vermutung; wer sie wie einnimmt, ohne die Kasse in einen Root zu verwandeln, ist offen.
4. **Die Geschwindigkeit des Kerns gegen den Schutz vor Übernahme.** Dem Kern in einer Katastrophe Schnelligkeit zu geben, ohne eine Maschine des Ausnahmezustands zu schaffen.
5. **Ein Schiedsrichter, stärker als der Stärkste, aber kein Tyrann.** Vielleicht liegt die Antwort nicht in der Kraft des Schiedsrichters, sondern in einem Bau, in dem sich ein Verstoß für alle zugleich nicht lohnt - das ist zu bauen und zu prüfen.
6. **Die Prüfbarkeit des Unfassbaren.** Die Kontrolle über eine übermächtige KI im Kern, wenn sich ihr Code mit menschlichem Verstand nicht verstehen lässt. Vielleicht die wichtigste.
7. **Floor und Austritt zugleich.** Das Recht wegzugehen mit der Festigkeit des Gemeinsamen zu vereinen, damit die Freiheit des Auseinandergehens die Solidarität nicht tötet.
8. **Kennzahlen ohne Goodhart.** Den Erfolg von Politiken zu messen, ohne das Unmessbare zu erdrücken und ohne einen Wettlauf um das Umgehen der Schwellen auszulösen.

> Über die Arbeit und ihre Stütze
>
> Jede Spur ist eine bestimmte Arbeit am Gemeinwohl, die sich als Forschung und Prototyp führen und unterstützen lässt - im Kleinen, offen, mit überprüfbaren Schritten. Eine Stütze für solche Arbeit wird nur innerhalb einer strengen Zucht angenommen: Die Stimme wird nicht gekauft, ein Beitrag gibt keine Macht über Menschen, im Voraus wird nichts versprochen. Die Durchführung einer Spur zu unterstützen ist möglich; die Richtung des Volkes zu kaufen ist es nicht.

Der abschließende Rahmen

## Das Modell ist ein Beispiel. Der Horizont ist wirklich.

Dieses Dokument ist eine Stimme und eines aus der unendlichen Menge möglicher Modelle. Es ist absichtlich nicht endgültig: mit starken Stellen, die sich entwickeln lassen, und mit schwachen, die aufzuschneiden sind. Seine Aufgabe ist erfüllt, wenn es gezeigt hat, dass sich eine Weltordnung ingenieurmäßig zerlegen lässt, dass der Staat ein zerlegbares Bündel von Funktionen und kein Schicksal ist, und dass sich ein ehrliches Modell von einer Utopie dadurch unterscheidet, dass es seine Risse als Erstes zeigt.

Genau hier kehrt Earthlings zurück - nicht als Verfasser dieses Modells und nicht als sein Träger, sondern als eine *Umgebung*: als Ort, an dem solche Modelle zum Gegenstand lebendiger Arbeit werden - im Kleinen zusammenbauen, an freiwillig Einverstandenen erproben, messen, zurückrollen, forken und weitergeben. Nicht „hier ist die richtige Antwort“, sondern „hier ist ein Raum, in dem sich Antworten suchen lassen, ohne die ganze Welt aufs Spiel zu setzen“.

Kommen Sie und zerlegen, bestreiten und brechen Sie, was schlecht hält. Die Richtung geht dorthin, wo die Regler sichtbar sind, das Pult niemandem übergeben ist und sich ein Fehler zurückrollen lässt.

Die Arbeitsagenda des Volkes der Earthlings · eine fachlich enge Zerlegung. Kein Programm der Zukunft und kein fertiger Entwurf - eine Liste offener Aufgaben und eine Einladung zur gemeinsamen Arbeit.
