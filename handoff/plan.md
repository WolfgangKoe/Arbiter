# Plan · Zyklus 6

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md). Grundlage: [Review 5](review.md)
und deine Kommentare: nur dein Happy Path wie in ArbiterMap.

## Dein Happy Path nach Zyklus 6
1. Arbiter startet mit verteilten Zonen, Spieler 2 ist *an der Reihe*. (gebaut)
2. Er klickt eine *Einheit* in seiner *Ablage* an: goldener Rahmen, nur sie ist
   *ausgewählt*. (Item 1)
3. Er klickt in seine Zone: Die *Einheit* steht dort als *Formation*, ragt sie hinaus,
   rückt Arbiter sie hinein; sie bleibt *ausgewählt*. (Item 1)
4. Er hält ein *Modell* gedrückt und zieht: Die *Einheit* wandert mit (Item 2) und hält
   schon beim Ziehen am Rand der Zone und vor fremden *Bases* an (Item 3).
5. Ein Klick auf ein *Modell* wählt nur dieses, er zieht es allein, ein weiterer Klick
   darauf wählt wieder die *Einheit* (Item 2); es hält ebenso an (Item 3).
6. „Aufstellen der Einheit beenden“: Der andere ist *an der Reihe*, wer fertig ist, wird
   übersprungen. (gebaut)

Keine Knöpfe in der *Ablage*, kein „in Aufstellung“. Ein *Grund* nur, wenn ein Klick, ein Zug
oder das Beenden gerade nicht geht (995).

## Items
1. [Setzen per Klick](../domaene/items/setzenPerKlick.md): Schritte 2, 3. Vorab der Test zur
   Zugschwelle (Anliegen 622).
2. [Einheit und Modell verschieben](../domaene/items/einheitVerschieben.md): Schritte 4, 5.
3. [Anhalten an Bases](../domaene/items/anhaltenAnBases.md): Risiko des Zyklus.

Testautor: Ein *gesperrtes* *Modell* (AUF-9.3, 12.1, 17.1, QUE-3.5) entsteht in den Tests ab
Item 1 per Ziehen auf ein *gesetztes* (AUF-8.2), ab Item 2 mit der *Ebene* *Modell*.
Architekt: Ist Item 2 grün, vor Item 3 grün, stehen die Beispiele des Vertrags ohne
*gesperrtes* *Modell*; die Tests zu Item 3 lesen sie, statt sie zu kopieren. Mit Item 3 gibt es
bis AUF-13.1 (Plan 7) kein „zurück“ am Bildschirm, den Bildschirmtest zu 17.1 streicht der
Testautor dann, die übrigen Tests zu 17.1 bleiben (1210).
Reihenfolge 1, 2, 3: Jedes baut auf dem vorigen auf. Klemmt Item 3, siehst du 2 bis 5
trotzdem (996). Gleichzeitig: Verträge zu 1 und 2 in einem Lauf, der Architekt probiert das
Anhalten neben Item 1 aus.

## Randfälle, Plan 7
„gemeinsam übergehen“ (AUF-13, QUE-5), *zurücklegen* (AUF-23), AUF-22, *ruhige Karte*
(QUE-7), AUF-16.7, Klick auf ein *Modell* einer nicht *ausgewählten* *Einheit*, Klick, dessen
*Formation* fremde *Bases* überdecken würde (AUF-18.7, 27; dazu Etappe 1, 999); bis Item 3
ein Block, auf fremden *Bases* losgelassen. Danach ist Etappe 1 erreicht.

## Empfehlung
Gib die drei Items frei, wenn der Happy Path deinem Bild entspricht.

## Offene Anliegen
An dich, an den Anforderungsautor, Vorschläge von ihm: keine. Sonst: [Moderation](moderation.md).

## Fortschritt
- [x] Architekt: Vertrag zu Item setzenPerKlick, bei beiden Hälften
- [x] Testautor: Tests zu Item setzenPerKlick
- [x] Fachkritiker: Kritik an den Tests zu Item setzenPerKlick
  Hindernis: 1120: Tests zu AUF-18.2, 18.3 prüfen Formation und kürzesten Weg nicht, QUE-3.4 widerspricht AUF-16.6; dazu 1121 an den Anforderungsautor (Anliegen 1143)
- [x] Architekt: Kritik an den Tests zu Item setzenPerKlick
  Hindernis: Anliegen 1140: Spiegel, Ruff und toter Code rot (Anliegen 1142)
- [x] Implementierer: Tests zu Item setzenPerKlick grün
- [x] Architekt: Kritik am Code zu Item setzenPerKlick
  Hindernis: Anliegen 1212: ruff E501 in aufstellen/__init__.py, ziehen.py nach setzenPerKlick.py, tote Klassen des Abzeichens in komponenten.css und komponenten.html (Anliegen 1214)
- [x] Reviewer: Kritik am Code zu Item setzenPerKlick
  Hindernis: Anliegen 1220: Ein Zug von mehr als 4 px auf der Einheitenkarte wählt aus, auf dem Spielfeld setzt er die Formation (V8) (Anliegen 1222)
- [x] Fachkritiker: Item setzenPerKlick abgenommen
- [x] Planer: Item setzenPerKlick gelöscht
- [x] Architekt: Vertrag zu Item einheitVerschieben, bei beiden Hälften
- [x] Testautor: Tests zu Item einheitVerschieben
  Hindernis: Belegungsschwelle erreicht. Fertig: Tests AUF-20/21/24/25/26 in Domäne, Dienst und Bildschirm geschrieben (ebeneTest, einheitVerschiebenTest, blockAlsGanzesTest, modellPerKlickTest, anhaltenAnEinerBaseTest). Offen: 1. ruff (PLR0913 mehr als 5 Parameter in 13 Bildschirm- und Dienst-Tests, ARG001 in modellPerKlickTest anderesModellDavor und spielerEins, E501 anhaltenAnEinerBaseTest:97 und einheitVerschiebenTest:177, I001 ebeneTest). 2. Die Bildschirmtests zu 21.1, 21.2, 24.2, 26.1 laufen rot, ob aus dem richtigen Grund (nicht wegen Testfehler wie Zielpunkt außerhalb der Karte), ist ungeprüft. 3. 10 Tests grün (Randfälle Grenze berührt, nichtAusgewählt bei 20.4, Dienst 20.2), vor allem Regressionswächter. 4. Benennung, vulture, Spiegel (python3 -m pytest prozess/pruefungen) nicht gelaufen. 5. setzenPerKlickDavor in modellPerKlickTest unbenutzt, löschen. Anliegen 1190 ist erledigt. (Anliegen 1211)
- [x] Fachkritiker: Kritik an den Tests zu Item einheitVerschieben
- [x] Architekt: Kritik an den Tests zu Item einheitVerschieben
  Hindernis: Anliegen 1215: Tests zu Item 2 prüfen ‚ohne Grund‘ über gesperrt und gründeDerGesperrten, die V10 mit Item 3 streicht; Docstring von ziehen.py, Wiederholungen, Ausschnitte statt Entpacken (Anliegen 1292)
- [x] Implementierer: Tests zu Item einheitVerschieben grün
- [x] Architekt: Kritik am Code zu Item einheitVerschieben
  Hindernis: Neuer Code verletzt Architektur M1: Das Hineinrücken in einheitVerschieben.py kennt die Baseform und doppelt _rückung aus setzenPerKlick.py; Befund und Gegenvorschlag in Anliegen 1410. (Anliegen 1411)
- [x] Reviewer: Kritik am Code zu Item einheitVerschieben
- [x] Fachkritiker: Item einheitVerschieben abgenommen
- [x] Planer: Item einheitVerschieben gelöscht
- [x] Architekt: Vertrag zu Item anhaltenAnBases, bei beiden Hälften
- [x] Testautor: Tests zu Item anhaltenAnBases
  Hindernis: Offen: 26.2 bis 26.4 stehen in anhaltenAnEinerBaseTest.py (ruff E501 und Format noch beheben; Hilfe anhalten.py; Fixture andereEinheitAufgestellt in conftest.py). AUF-24.1 fehlt in blockAlsGanzesTest.py: Abfrage stellenBeimLoslassen mit drei gesetzten Boyz (21.1, 21.2, fremde Base), Dienst samt Beispiel stelleBeimLoslassen.json, Seite mit haltenUndLosslassen. Danach Rotprüfung, ruff, prozess/pruefungen, abhaken (Anliegen 1291); beseitigt: Commit „Item setzenPerKlick: Modelle per Klick setzen, Tests grün, Kritik am Code umgesetzt“
- [x] Fachkritiker: Kritik an den Tests zu Item anhaltenAnBases
  Hindernis: 1350: Tests zu AUF-9.1, 9.3, 12.1, QUE-3.5 und der Bildschirmtest zu 17.1 stehen noch und widersprechen AUF-26.1 und 26.2; danach 1351 an den Anforderungsautor (Anliegen 1353)
- [x] Architekt: Kritik an den Tests zu Item anhaltenAnBases
  Hindernis: Die Seite wird nie gegen das Beispiel stelleBeimLoslassen.json geprüft (V10 verlangt page.route): ein Bildschirmtest in blockAlsGanzesTest.py fehlt, siehe Anliegen 1360. (Anliegen 1363)
- [x] Implementierer: Tests zu Item anhaltenAnBases grün
  Hindernis: 1460: vier von 160 Tests verlangen Exaktheit, die Eingabe nicht liefert (Fixture ohne Auswahl, Dezimalzahl des Dienstes, Pixel der Seite); 92 der 96 roten Fälle sind grün, kein anderer Test rot (Anliegen 1461)
- [x] Architekt: Kritik am Code zu Item anhaltenAnBases
  Hindernis: Benennungsprüfung rot: Typalias BasenAnStellen in messen.py; Befund und Gegenvorschlag in Anliegen 1440. (Anliegen 1441)
- [x] Reviewer: Kritik am Code zu Item anhaltenAnBases
- [x] Fachkritiker: Item anhaltenAnBases abgenommen
- [x] Planer: Item anhaltenAnBases gelöscht
- [x] Reviewer: DoD über das Inkrement
- [x] Reviewer: Review geschrieben
- [ ] Stakeholder: Freigabe Review 6

## Freigabe
Freigabe: ja.
Kommentar: Wenn ich mir die Mockups so anschauen, dann sehe ich da so viele Hinweise und Buttons als ich es aus Arbitermap kenne. Ich möchte in der Aufstellungsphase, dass die Spieler nach dem Rolloff abwechselnd ihre Einheiten komplett in ihrer Aufstellungszone aufstellen (indem sie in die Aufstellungszone klicken) und dort noch verschieben können bzw. einzelne Modelle verschieben können. Dann "Aufstellen beenden" und der andere Spieler ist dran. Das geht dann so weiter bis alle Einheiten auf dem Feld oder in Reserve stehen. ALles andere sind Randfälle. Ich kann den Plan so nicht freigeben, weil ich nicht glaube, dass hier meine Vorstellungen umgesetzt werden.
Stellungnahme: Neu geschnitten auf deinen Happy Path, Randfälle in Plan 7.
Kommentar: 1. Die zwei "Knöpfe" in der einheitenKarte möchte ich nicht!!! Die kommen weg! So wie es jetzt ist, sieht es an sich okay aus. Ich wähle die Einheit in der armeeListe, die bekommt dann den goldenen Rahmen, dass sie "ausgewählt" ist. Dann klicke ich auf die Aufstellungszone und sie erscheint dort. Wenn ich die Einheit verschieben will, halte ich auf einem Modell gedrückt und die ganze Einheit lässt sich ziehen. Möchte ich ein Modell der Einheit ziehen, muss ich nochmal auf das einzelne Modell klicken. Das Modell erscheint ausgewählt, die anderen der Einheit nicht. Dann kann ich dieses Modell mit der Maus halten (so wie es aktuell ist) und verschieben. Das ist alles schon in ArbiterMap umgesetzt. Warum wird hier neuer Kram erfunden?! - So keine Freigabe des Plans! 2. Der Ablaufplan soll in plan.md erscheinen. Warum erstellst du hierfür eine HTML? Das war nicht, was ich mit "Ausnahme" wollte. Warum verstehst du mich nicht? Oder warum kannst du dich in den Anliegen nicht verständlich ausdrücken?
Stellungnahme: 1. Die Knöpfe kommen weg, Schritte 4 und 5 sind deine Bedienung aus ArbiterMap. Ich hatte sie aus der Beschreibung statt aus dem Gebauten; das war falsch. Kriterien 980, Mockups 981. 2. Wer je Item was tut, zeigt jetzt der Abschnitt Fortschritt über der Freigabe; ihn schreibt das Skript (Anliegen 982). Meine Prosa dazu ist weg, unter Items steht nur, was nur der Plan weiß (Anliegen 983). Die HTML-Datei ist gelöscht (981).
Kommentar: Und nochmals in der unitCard braucht es keinen Hinweis "in Aufstellung". Auch "Base überdeckt" oder "in Nahkampfreichweite" sind faktisch völlig unsinnige Randfälle. ArbiterMap hat Baseüberdeckung durch Klemmen blockiert. Tu endlich, was ich will!
Stellungnahme: Umgesetzt. Das Wort „in Aufstellung“ fällt mit Item 1 weg. ‚Base überdeckt‘ und ‚Nahkampfreichweite‘ sind aus dem Happy Path: Block und *Modell* klemmen beim Ziehen wie in ArbiterMap am Rand der Zone und vor fremden *Bases* (Schritte 4, 5, Item 3); einen *Grund* nennt der Happy Path. [Etappe 1](../domaene/etappen/01-aufstellen.md) sagt dasselbe. Kriterien: Anliegen 984, Mockups: Anliegen 988.
Kommentar: Auch Rolloff gewonnen ist hier nicht erforderlich. Wir gehen bis auf Weiteres davon aus, dass Spieler 2 diesen gewonnen hat, es also "an der Reihe" anzeigt. Außerdem scheinen viele Mockups identisch zu sein. Wozu sind diese dann gut?
Stellungnahme: „Gewinner und Zone“ entfällt, Schritt 1 ist der gebaute Start (deine Antwort A in Anliegen 990), ebenso in [Etappe 1](../domaene/etappen/01-aufstellen.md). Gleiche Mockups hat Ux gestrichen (988), jedes übrige zeigt einen anderen Schritt.
