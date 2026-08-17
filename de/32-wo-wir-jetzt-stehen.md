# Wo wir jetzt stehen

*Das Volk der Earthlings*

## Wozu dieses Dokument

Wir behaupten, dass die Earthlings überprüfbar sind. Eine solche Behauptung hat nur dann einen Sinn, wenn sich genau angeben lässt, was überprüft wird und auf welche Weise. Deshalb veröffentlichen wir statt der allgemeinen Formel „unser Code ist offen“ die genaue Grenze: was offen ist, was verschlossen ist und aus welchem Grund.

Zurzeit läuft die Gründungsphase: Bis zum Tag der Annahme der Erklärung wird das Volk erst konstituiert, und ein Teil der unten angeführten Zahlen liest sich anders, als er sich danach lesen wird. Ihre Regeln und Fristen sind im Dokument [Die Gründungsphase](https://earth-lings.org/documents/de/de20-gruendungsphase.html) dargelegt - hier wiederholen wir sie nicht, damit die Daten eine einzige Quelle behalten.

> **Der Grundsatz.** Offen ist das, wovon die Überprüfbarkeit des Volkes abhängt: wer Teilnehmer ist, wie er es geworden ist, wie viele wir sind und wie eine Stimme gezählt wird. Verschlossen ist das, dessen Veröffentlichung der Überprüfbarkeit nichts hinzufügen, aber ein Risiko für die Teilnehmer schaffen würde: die Serverumgebung und die Verarbeitung personenbezogener Daten.

## Was offen ist

| Bestandteil | Wo | Lizenz |
|---|---|---|
| Smart Contract des Passes EarthlingPassportV2 | [github.com/earthlingsorg/earthlings-contracts](https://github.com/earthlingsorg/earthlings-contracts) | MIT |
| Dokumentation der Architektur | Ordner `/docs` desselben Repositoriums: Modell der Identität, Datensparsamkeit, Sicherheit, Ansehen, Fluss der Beiträge | MIT |
| Adresse des Vertrags und alle seine Vorgänge | [0x20e7962878429B803E35F83ba34eD291afEC2Be4](https://polygonscan.com/address/0x20e7962878429B803E35F83ba34eD291afEC2Be4) | öffentliche Daten |
| Register der Pässe | Blockchain Polygon, wird unmittelbar aus dem Vertrag gelesen | öffentliche Daten |
| Öffentlicher Kanal der Abstimmungen der DAO | [snapshot.org, Raum earthlings-dao.eth](https://snapshot.org/#/s:earthlings-dao.eth) | öffentliche Daten |
| Kasse on-chain | [0xaEC7016218f7883bf6e47a2C932FdE6d822086C0](https://app.safe.global/home?safe=matic:0xaEC7016218f7883bf6e47a2C932FdE6d822086C0) | öffentliche Daten |

## Was verschlossen ist und warum

| Bestandteil | Grund |
|---|---|
| Der Serverteil der Plattform | Enthält die Logik des Zugangs zu den Konten. Seine Veröffentlichung vor einer unabhängigen Prüfung erhöht das Risiko eines Einbruchs in die Konten der Teilnehmer und fügt der Überprüfbarkeit des Volkes dabei nichts hinzu. |
| Das System der Identitätsprüfung | Arbeitet mit Papieren und mit Biometrie. Hier ist die Verschlossenheit ein Teil des Schutzes personenbezogener Daten und keine Verheimlichung. Wie die Datensparsamkeit eingerichtet ist, ist in der offenen Dokumentation beschrieben. |
| Die Infrastruktur der Ausrollung | Enthält die Konfiguration der Server. Ihre Veröffentlichung wäre eine Karte für einen Angreifer. |

Keiner der verschlossenen Bestandteile bestimmt, wer ein Earthling ist und wie eine Stimme gezählt wird. Das bestimmt der offene Smart Contract.

## Was sich sofort überprüfen lässt, ohne uns zu vertrauen

- **Die Regeln des Passes.** Den Quellcode des Vertrags im Repositorium lesen: Der Pass ist unübertragbar, einer je Geldbörse, der Inhaber kann ihn selbst verbrennen.
- **Wie viele Pässe ausgegeben sind.** Die Funktion `totalSupply` des Vertrags aufrufen. Diese Zahl nennen nicht wir - sie nennt die Blockchain. Doch sie ist richtig zu lesen, und wir erklären, wie. **Zurzeit stehen dort vier Testeinträge**, die bei der Fehlersuche vor dem Start des Systems angelegt wurden, und wirkliche Teilnehmer sind nicht darunter. **Vom 7. September 2026 bis zum Tag der Annahme des Textes** bedeutet diese Zahl die Menschen, die ihre Identität haben prüfen lassen und an der Konstituierung teilnehmen: Earthlings werden sie erst nach der Annahme der Erklärung. **Nach der Annahme** ist die Zahl der ausgegebenen Pässe die Zahl der Earthlings.
- **Ob eine bestimmte Adresse einen Pass hat.** Die Funktion `balanceOf` aufrufen. Die Antwort: 1 oder 0.
- **Die Abstimmungen der DAO.** Den Raum in Snapshot öffnen und die Vorschläge, die Stimmen und die Unterschriften sehen. Jede Stimme ist mit der Geldbörse des Abstimmenden unterzeichnet - wir können weder eine Stimme hinzufügen noch eine fremde fälschen.
- **Das Stimmrecht.** Snapshot fragt bei unserem Server an, ob eine Adresse einen Pass hat. Diesem Schritt muss man im Augenblick der Abstimmung vertrauen - danach aber nicht: Die Adressen aller Abstimmenden sind öffentlich, und jeder Mensch kann jede von ihnen selbst im Vertrag auf Polygon überprüfen. Eine Abweichung würde sichtbar.

Den letzten Punkt beschreiben wir unmittelbar, weil das eine der beiden Stellen ist, an denen man uns vertrauen muss. Wir ziehen es vor, sie selbst zu benennen, statt sie als Fund für einen Prüfenden liegen zu lassen.

Die zweite Stelle sind die Schlüssel des Eigentümers des Vertrags. In der ausgerollten Fassung des Vertrags stehen die Funktionen der Ausgabe und der Entwertung eines Passes dem Eigentümer offen, und der Schlüssel des Eigentümers liegt zurzeit beim Gründer. Die Charta, Artikel 21, lässt eine Entwertung gegen den Willen des Inhabers nur aus zwei Gründen und nur mit einem Verfahren zu: Benachrichtigung, Frist für Einwendungen, Stellungnahme des Rates, geheime Abstimmung mit erhöhter Mehrheit, Beschwerde. Im Code stehen diese Gewährleistungen nicht - sie sind verfahrensmäßig. Also beruhen sie zurzeit auf unserem Wort und nicht auf der Technik, und wir gestehen das ein. Was daran getan wird: die Trennung der Rechte zur Ausgabe und zur Entwertung in gesonderte Rollen, eine Verzögerung bis zur Ausführung der Entwertung und die Übergabe der Eigentümerschaft an eine Multisig aus sechs gewählten Unterzeichnern. Die Fristen stehen im [Fahrplan](https://earth-lings.org/documents/de/de19-fahrplan.html).

## Was es noch nicht gibt

Eine ehrliche Aufzählung dessen, was als Grundsatz erklärt, aber noch nicht getan ist:

- Der Quellcode des Vertrags ist im Repositorium veröffentlicht, aber **im Blockchain-Explorer noch nicht verifiziert**. Das bedeutet, dass die Übereinstimmung des veröffentlichten Quellcodes mit dem ausgerollten Bytecode zurzeit selbst zu überprüfen ist. Die Verifizierung ist in Arbeit.
- **Eine unabhängige Sicherheitsprüfung wurde nicht durchgeführt.** Sie ist vor der Ausweitung des Betriebs vorgesehen.
- **Die Smart Contracts der Schatzkammer sind nicht ausgerollt.** Ausgerollt ist nur der Vertrag des Passes; die innere Wirtschaft der Teilnahme wird zurzeit in der Buchführung der Plattform geführt.
- Der öffentliche Kanal der Abstimmung ist **ausgerollt und arbeitet technisch, doch inhaltliche Abstimmungen haben darin noch nicht stattgefunden**.
- Ein Programm zur Suche nach Schwachstellen (bug bounty) ist als Grundsatz angekündigt, aber **noch nicht eröffnet**.
- **Die Rechte des Eigentümers des Vertrags sind weder getrennt noch übergeben.** Ausgabe und Entwertung eines Passes stehen einem einzigen Schlüssel offen, eine Verzögerung bis zur Ausführung gibt es nicht, der Schlüssel liegt beim Gründer. Die Beschränkungen des Artikels 21 der Charta wirken verfahrensmäßig.
- **Eine Multisig auf der Geldbörse der Kasse gibt es noch nicht.** Die Schwelle der Unterschriften beträgt eine; das lässt sich an der Adresse der Geldbörse überprüfen. Der Übergang zu einer Zusammensetzung aus sechs Unterzeichnern ist ein Maßstab für den Übergang zwischen den Abschnitten.

## Das Recht auf Nachbildung

Das Register der Pässe lebt in der Blockchain und nicht auf unseren Servern, und der Code des Vertrags ist offen. Daraus folgt das Praktische: Wird die Infrastruktur angehalten oder ihr Betrieb übernommen, so kann die Gemeinschaft eine neue Plattform gegen dasselbe Register bauen. Übertragen werden die Menschen und ihre Pässe; die Serverumgebung ist austauschbar.

Die Nachbildung hat zwei Stützen, und die zweite ist nicht weniger wichtig als die erste. Das Register gibt die Fortdauer der Menschen, und die **veröffentlichte Beschreibung** gibt die Möglichkeit, das Werkzeug neu zu bauen: Regeln, Schwellen, Quoren, Fristen und Verfahren sind in der Charta, in der Schatzkammer und in diesen Dokumenten vollständig dargelegt. Deshalb wird nicht unser Code nachgebildet, sondern das beschriebene System. Den verschlossenen Serverteil zu kopieren ist nicht nötig und wird nicht nötig sein.

Deshalb hebt die Verschlossenheit des Serverteils das Recht des Volkes nicht auf, ohne die Gründer fortzudauern. Die Merkmale einer rechtmäßigen Fortsetzung - ein bewahrter unabänderlicher Kern, der Wille der geprüften Menschen und die Fortdauer der Verfahren - sind im Dokument [Der Fahrplan des Übergangs](https://earth-lings.org/documents/de/de19-fahrplan.html) beschrieben.
