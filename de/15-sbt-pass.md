# Der SBT-Pass eines Earthling

**Der digitale Nachweis der Zugehörigkeit zum Volk der Earthlings**

> Dieses Dokument beschreibt den Aufbau und die rechtliche Bedeutung des Passes. Bei einer Abweichung gilt die [Charta](https://earth-lings.org/documents/de/de05-charta.html), und bei einer Abweichung der Charta von der [Erklärung](https://earth-lings.org/documents/de/de01-erklaerung.html) gilt die Erklärung. Der Ablauf des Beitritts ist im Dokument [Der Weg des Earthling](https://earth-lings.org/documents/de/de14-weg-des-earthling.html) beschrieben.

---

## Was das ist

Der SBT-Pass eines Earthling ist ein unübertragbares digitales Token (Soulbound Token), das jedem Teilnehmer nach der Unterzeichnung der Erklärung, der Identitätsprüfung und der Entrichtung des Beitrags ausgegeben wird. Er weist die Zugehörigkeit zum Volk kryptografisch nach und wird in einem verteilten Register als einmaliger, fälschungssicherer Eintrag aufbewahrt.

Anders als staatliche Pässe, die an ein Gebiet gebunden sind und eine Staatsangehörigkeit nachweisen, weist dieser Pass die Zugehörigkeit zu einem Volk nach, das gemeinsame Werte verbinden. Er kann weder einem anderen übertragen noch verkauft noch veräußert werden.

**Die Unübertragbarkeit.** Der Pass ist an Ihre Geldbörse gebunden, und die Übertragung ist im Vertrag selbst gesperrt und nicht durch eine Regel, die sich umgehen ließe. Die Einmaligkeit der Person ist bei der Ausgabe nachgewiesen.

**Der kryptografische Schutz.** Der Eintrag wird in einem verteilten Netz aufbewahrt und kann weder gefälscht noch unbemerkt geändert werden.

**Die Gleichheit.** Alle erhalten denselben Pass mit denselben Rechten. Bevorrechtigte Klassen und Stufen der Zugehörigkeit gibt es nicht. Ein Mensch - ein Pass - eine Stimme.

---

## Was der Pass gibt

### Die Teilnahme an der Verwaltung

- das Stimmrecht in der DAO-Vollversammlung;
- das Einbringen von Vorschlägen und Anregungen;
- die Teilnahme an den Entscheidungen zu jeder Frage.

> **Die Stimme ist unveräußerlich** und darf nicht wegen Ansichten, wegen des Inhalts der Stimmabgabe, wegen der Ablehnung von Beschlüssen oder als allgemeine Sanktion entzogen oder ausgesetzt werden (Erklärung, Artikel 4; [Charta, Artikel 17 und 37](https://earth-lings.org/documents/de/de05-charta.html)). Die Stimme ist der Inhalt der Zugehörigkeit: Entzöge das Volk sie aus solchen Gründen, so schlösse es den Menschen aus und ließe ihm nur den Namen.

Die einzige Ausnahme sind nachgewiesene Handlungen, die auf die Untergrabung der Unversehrtheit der Abstimmung selbst gerichtet sind: Absprache, Kauf oder Verkauf einer Stimme, Nötigung anderer, Umgehung der Regel „ein Mensch - ein Pass“ (Charta, Artikel 22-bis). Ansichten, der Inhalt der Stimmabgabe und die Ablehnung von Beschlüssen sind in keiner Darstellung ein Grund.

### Die digitale Identifizierung

- der öffentlich überprüfbare Nachweis des Status als Teilnehmer;
- der Zugang zu den Diensten des Ökosystems;
- die Möglichkeit der Verwendung in dezentralen Anwendungen, die diesen Standard unterstützen.

### Der Zugang zum Ökosystem

- die Digitale Plattform des Volkes;
- die Teilnahme an Zellen und gemeinsamen Projekten;
- Bildungsangebote;
- der Austausch mit anderen Teilnehmern.

### Vermerke über die Teilnahme

Die Geschichte der Teilnahme und des Beitrags wird öffentlich festgehalten: Abstimmungen, abgeschlossene Projekte, die Arbeit in Zellen.

> **Diese Vermerke wirken sich auf nichts aus** und haben ausschließlich Auskunftscharakter: [Charta, Artikel 8](https://earth-lings.org/documents/de/de05-charta.html).

---

## Wie man ihn erhält

**1. Die Unterzeichnung der Erklärung.** Das Studium der Dokumente, das Verständnis der Grundsätze, die Bestätigung der Zustimmung durch eine digitale Signatur. Eben dieser Akt begründet die Zugehörigkeit.

**2. Die Identitätsprüfung.** Die Prüfung, dass Sie ein lebender Mensch sind und dass Sie einer sind. Sie sichert den Grundsatz „ein Mensch - eine Stimme“. Die ursprünglichen Bilder und die Scans der Papiere werden nicht gespeichert.

**3. Die Entrichtung des Beitrags.** Der Gegenwert von 79 USD, in Kryptowährung (ETH, USDT, USDC). Der Zweck des Beitrags und das Verfahren seiner Verwendung - im Dokument [Die Schatzkammer](https://earth-lings.org/documents/de/de09-schatzkammer.html).

> Wer den Beitrag nicht selbst entrichten kann, stellt sich in eine offene Warteschlange, und den Beitrag entrichtet für ihn ein anderer Mensch oder die Schatzkammer. Der Pass unterscheidet sich dabei in nichts von den übrigen: Im Register ist nicht vermerkt, von wem der Beitrag entrichtet wurde. Die Zugehörigkeit kauft der Beitrag nicht: Sie entsteht durch die Unterzeichnung der Erklärung.

**4. Die Ausgabe des Passes.** Das Token wird selbsttätig erzeugt und an Ihre Geldbörse gebunden.

---

## Die technische Grundlage

### Die Infrastruktur

- Netz: Polygon Mainnet, EVM-verträglich;
- Standard: ERC-721, unübertragbar (soulbound);
- Adresse des Vertrags der Pässe: `0x20e7962878429B803E35F83ba34eD291afEC2Be4`;
- die Vorgänge sind öffentlich und im Explorer des Netzes ohne unser Zutun überprüfbar;
- der Quellcode des Vertrags ist offen (Lizenz MIT).

### Die Sicherheit des Vertrags

- Grundlage: die geprüften Bibliotheken von OpenZeppelin;
- Regel: ein Pass je Geldbörse; die Übertragung ist im Vertrag selbst gesperrt;
- eine unabhängige Prüfung ist vor der Ausweitung des Betriebs vorgesehen.

### Die Speicherung der Daten

- **im Register:** Kennung, Pseudonym, Hash der Prüfung. Personenbezogene Daten werden nicht in das Register eingetragen;
- **außerhalb des Registers:** die personenbezogenen Daten des Kontos, verschlüsselt und in möglichst geringem Umfang;
- **Biometrie:** wird nicht gespeichert. Gespeichert werden nur nicht umkehrbare kryptografische Hashes, und nur dafür, dass ein Mensch nicht zwei gültige Pässe haben kann;
- der Entwurf folgt den Grundsätzen der DSGVO.

### Die Kryptografie

- Signaturen: ECDSA secp256k1;
- Hashverfahren: Keccak-256.

Ein einheitlicher Standard des Passes für alle Teilnehmer erlaubt es, die Mittel auf die Verlässlichkeit eines einzigen Systems zu richten, und sichert jedem denselben Schutz.

---

## Die rechtliche Bedeutung

Der Pass ist ein digitaler Nachweis der Zugehörigkeit zum Volk der Earthlings.

### Was der Pass nicht gibt

Das ist vor dem Beitritt zu verstehen und nicht danach.

- **er gibt keine Staatsangehörigkeit und kein Aufenthaltsrecht** in irgendeinem Land;
- **er gewährt keine Visaerleichterungen** und keine Einreiserechte;
- **er hat keine rechtliche Geltung** in den staatlichen Stellen irgendeines Landes;
- **er ersetzt keine Papiere**, die die Identität nachweisen;
- **er befreit nicht** von der Beachtung der Gesetze des Wohnsitzlandes;
- **er begründet keine Rechte im Völkerrecht.**

Der Pass bezeugt das, was er bezeugt, und das ist nicht wenig: Ein bestimmter Mensch ist als lebend und einmalig nachgewiesen und hat die Erklärung unterzeichnet. Innerhalb des Volkes folgt daraus alles - die gleiche Stimme, die Teilnahme an Entscheidungen, die unveräußerliche Zugehörigkeit. Was diese Gesamtheit für das Völkerrecht bedeutet, ist Gegenstand einer eigenen Untersuchung in den Dokumenten [Die Rechtsgrundlage](https://earth-lings.org/documents/de/de04-rechtsgrundlage.html) und [Einwände und Antworten](https://earth-lings.org/documents/de/de26-einwaende-und-antworten.html), wo auch die Argumente dagegen angeführt sind.

### Der Schutz der Daten

- das Recht auf Berichtigung und Löschung der von der Plattform verarbeiteten Daten;
- Einträge in einem verteilten Register lassen sich technisch nicht löschen - und eben deshalb stehen keine personenbezogenen Daten in ihnen: Dort stehen pseudonyme Adressen und Vermerke über Handlungen;
- Datensparsamkeit bei der Verarbeitung; Verschlüsselung der personenbezogenen Daten;
- Lichtbilder und Scans werden nicht gespeichert.

### Verantwortung und Streitigkeiten

- die DAO der Earthlings ist keine eingetragene juristische Person;
- die Teilnehmer tragen einzeln die Verantwortung für die Beachtung der Gesetze ihrer Länder;
- innere Streitigkeiten werden nach den Verfahren der Charta beigelegt: Gespräch, Vermittlung, bei schweren Verletzungen die Anrufung des Unabhängigen Rates. Das Volk tritt nicht an die Stelle der Gerichte und der staatlichen Rechtsmechanismen und stellt außerhalb seines Ökosystems keine Schiedsstelle bereit.

---

## Das Ende der Geltung des Passes

**In der Regel entwerten nur Sie selbst den Pass**, mit dem eigenen Schlüssel, aus der eigenen Geldbörse (Funktion `burnByHolder`). Die Plattform bewahrt Ihre Schlüssel nicht auf und kann die Entwertung weder für Sie vornehmen noch sie verhindern.

Die Charta (Artikel 21) legt **zwei und nur zwei** Ausnahmen fest, und diese Aufzählung darf nicht erweitert werden.

> **Zum Tod des Inhabers.** Die Zugehörigkeit endet infolge des Todes eines Menschen, doch der Pass wird dabei nicht entwertet. Das Volk hat keinen Zugang zu den Sterberegistern der ganzen Welt, deshalb stützte sich ein solcher Grund auf nicht überprüfbare Angaben und wäre die billigste Weise, einen Teilnehmer zu beseitigen. Der Pass bleibt im Register; die Teilnahme, die es nicht mehr gibt, erfasst der Mechanismus der Inaktivität (Charta, Artikel 20). Der Pass wird unter keinen Umständen vererbt und nicht übertragen.

### 1. Die Aufhebung einer unwirksamen Ausgabe

Wird angewandt, wenn festgestellt ist, dass der Pass unter Verstoß gegen die Voraussetzungen der Ausgabe ausgegeben wurde: Einem Menschen ist mehr als ein gültiger Pass ausgegeben worden, oder die Prüfung wurde unter Verwendung falscher Angaben oder der Identität eines anderen durchlaufen.

**Das ist keine Sanktion und kein Ausschluss aus dem Volk.** Festgestellt wird nur, dass die Ausgabe von Anfang an nicht rechtmäßig zustande gekommen ist. Eine selbsttätige Neuausgabe folgt daraus nicht: Ist das Hindernis für eine rechtmäßige Ausgabe beseitigt, so ist der Mensch befugt, die Prüfung unter den allgemeinen Voraussetzungen erneut zu durchlaufen.

**Der Ablauf** - das ist ein Beschluss der Vollversammlung und keine Handlung eines Betreibers:

- eine begründete Darlegung mit Nachweisen;
- Benachrichtigung des Inhabers und **mindestens 21 Tage** für Einwendungen; der Inhaber ist befugt, andere Teilnehmer zu seiner Unterstützung heranzuziehen;
- Stellungnahme des Unabhängigen Rates;
- Abstimmung der Vollversammlung: **75 Prozent bei einem Quorum von 25, geheim, ohne Übertragung**;
- **Beschwerde binnen 30 Tagen**, wobei zur Aufhebung der Entscheidung eine einfache Mehrheit genügt.

Die technischen Befugnisse des Betreibers sind auf die Ausführung eines bereits von der Vollversammlung gefassten Beschlusses begrenzt. Selbständig die Ausgabe eines Passes aufheben kann der Betreiber nicht.

### 2. Die technische Neuausgabe

Auf **Antrag des Inhabers selbst** bei Verlust des Zugangs zur Geldbörse oder bei einer Migration des Vertrags. Der Pass wird entwertet und sogleich an dieselbe oder an eine neue Adresse neu ausgegeben. **Die Zugehörigkeit wird nicht unterbrochen**, eine Abstimmung ist nicht erforderlich.

### Der Grundsatz der Unveräußerlichkeit

Niemandem kann die Zugehörigkeit zum Volk zwangsweise genommen werden. Ein Verfahren des Ausschlusses gibt es nicht.

Werden für grobe Verletzungen der allgemeinen Regeln beschränkende Maßnahmen angewandt, so bleibt der Pass erhalten, **das Stimmrecht bleibt vollständig erhalten**, und die Beschränkungen betreffen nur die Teilnahme an Zellen, das Recht, Vorschläge einzubringen, und den Zugang zu einzelnen Diensten - nach dem Verfahren des Artikels 22 der Charta, mit dem Recht auf Verteidigung, geheimer Abstimmung und Beschwerde.

### Was technisch geschieht

- die Entwertung wird durch die Funktion `burn` des Smart Contracts ausgeführt;
- die Daten des Passes werden aus dem geltenden Register des Vertrags gelöscht;
- in der unabänderlichen Geschichte bleibt ein pseudonymer Vermerk darüber, dass der Pass bestand und entwertet wurde: Das ist eine Tatsache der Vergangenheit und keine fortdauernde Zugehörigkeit;
- wirkliche personenbezogene Daten stehen im Register nicht;
- für einen erneuten Beitritt wird das vollständige Verfahren durchlaufen und ein neuer Pass ausgegeben.

---

## Zur Finanzierung

Heute entwickelt sich das Volk mit den Mitteln der Teilnehmer: Eine äußere Finanzierung ist nicht eingeworben worden.

Die Charta und das Dokument [Die Schatzkammer](https://earth-lings.org/documents/de/de09-schatzkammer.html) sehen die Möglichkeit vor, Zuwendungen und Spenden von äußeren Organisationen anzunehmen - bei zwingender Veröffentlichung der Quelle, ohne Bedingungen, die den Grundsätzen des Volkes widersprechen, und mit einem ausdrücklichen Verbot: Ein Spender erhält weder eine Stimme noch Einfluss auf Beschlüsse. Die Höhe einer Spende gibt nichts.

Alle Beschlüsse über Ausgaben werden durch Abstimmung der DAO-Vollversammlung gefasst und veröffentlicht; die Bereiche der Ausgaben und ihre Anteile sind in Artikel 9 des Dokuments [Die Schatzkammer](https://earth-lings.org/documents/de/de09-schatzkammer.html) festgelegt.
