# Akzeptanztests zu Item einheitVerschieben: Fälle abseits des Happy Path

1300 · Kritik · von Fachkritiker → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Tests zu AUF-20.2, 20.4, 20.5, 21.1, 21.2, 24.2, 25.1 bis 25.4 und 26.1 treffen
ihre Kriterien und decken den Happy Path (Schritte 4 und 5): *Einheit* ziehen, *Modell*
anklicken, dieses *Modell* ziehen, noch einmal anklicken. Sie sind rot, weil die Funktionen
fehlen, nicht wegen Testfehlern. Die Annahmen aus Anliegen 1211 trage ich mit: Dienst und
Seite nur in der zweiten *Aufstellungszone* genügen, weil die Domänentests beide Zonen
prüfen; die zwei Seitentests zum Beispiel des Vertrags (25.1, 25.2) nur mit der Maus genügen,
weil die anderen Seitentests zu 25.1 und 25.2 Maus und Finger prüfen. Es fehlen vier Fälle
abseits des Happy Path:
1. AUF-20.4 sagt „eines ihrer *Modelle*“. Ist die *Ebene* ein *Modell*, ziehen die Tests nur
   dieses. Dass beim Ziehen eines anderen *Modells* derselben *Einheit* auch nur dieses sich
   bewegt (Vorbild `ArbiterMap/docs/spec/interaction_map.md:376`: „nur das gegriffene“),
   prüft kein Test.
2. AUF-24.2 gilt für „AUF-21.1 oder 21.2“. Die Tests zu 24.2 prüfen nur Züge innerhalb der
   Zone. Rückt 21.2 den Block wieder hinein und landet dabei ein *Modell* auf der vorigen
   *Stelle* eines anderen, prüft kein Test, dass keines *gesperrt* ist.
3. AUF-25.1 und 25.2 gelten für Anklicken. Dass ein Zug kein Anklicken ist, die *Ebene* also
   nach dem Ziehen bleibt, prüft kein Test (Vorbild `ArbiterMap/frontend/CLAUDE.md`, Abschnitt
   „Einheit als Block ziehen“; [Vertrag V8](../../technik/architektur/handlungen.md): „Ein Zug
   wählt nie aus“).
4. Nach AUF-25.2 ist die *Ebene* wieder die ganze *Einheit*, und die *Karte* kennzeichnet
   nach AUF-5.7 wieder alle ihre *gesetzten* *Modelle*. Die Seitentests zu 25.2 prüfen nur
   die Anfrage und die *Ebene*, nicht die Kennzeichnung.

**Kosten.** Ohne 3 bemerkt kein Test, wenn der Spieler die *Einheit* zweimal hintereinander
zieht und beim zweiten Mal nur ein *Modell* mitgeht; Vertrag und Seite verhindern das heute
schon. Ohne 1, 2 und 4 bleiben Fehler an seltenen Stellen unbemerkt: ein anderes *Modell*
der *Einheit* gezogen, ein Block knapp über die Grenze gezogen, die Kennzeichnung nach dem
zweiten Klick. Je Fall ein Test oder ein weiterer Parameter.

**Gegenvorschlag.** In der nächsten Technikphase:
1. In `ebeneTest.py` (20.4) bei `ebeneIstEinModell` ein *Modell* ziehen, das nicht die
   *Ebene* ist.
2. In `blockAlsGanzesTest.py` (24.2) einen Fall in der Domäne: zwei *Modelle* in einer Reihe
   quer zur Grenze, *Bases* bei Tiefe 9 − 5 Radien und 9 − 3 Radien, um 4 Radien tiefer
   gezogen. 21.2 rückt um 2 Radien zurück, das erste steht an der vorigen *Stelle* des
   zweiten. Danach ist keines *gesperrt*.
3. In `modellPerKlickTest.py` (25.1) ein Seitentest mit Maus und Finger: Nach einem Zug der
   *Einheit* ist die *Ebene* die ganze *Einheit*, nach einem Zug des *Modells*, das die
   *Ebene* ist, bleibt es die *Ebene*.
4. Im Seitentest zu 25.2 zusätzlich prüfen, dass nach dem Klick alle *gesetzten* *Modelle*
   gekennzeichnet sind.

**Stellungnahme.** Alle vier Fälle umgesetzt, wie vorgeschlagen:
1. `ebeneTest.py`: `testAuf20_4ZiehenEinesAnderenModellsAlsDerEbeneLässtAuchDieEbeneStehen`
   (Domäne): Die *Ebene* liegt auf dem ersten *Modell*, gezogen wird das zweite; erstes und
   drittes stehen wie davor.
2. `blockAlsGanzesTest.py`: `testAuf24_2KeinModellIstGesperrtWennBeimHineinrückenEinesAufDieVorigeStelleDesAnderenRückt`
   (Domäne, beide *Modelle* als gezogenes): *Bases* bei Tiefe 9 − 5 und 9 − 3 Radien, 4 Radien tiefer
   gezogen; das erste steht danach an der vorigen *Stelle* des zweiten, das zweite bei 9 − 1
   Radius, der Zug wird nicht gesperrt.
3. `modellPerKlickTest.py`: `testAuf25_1NachDemZiehenDerEinheitIstDieEbeneDieGanzeEinheit` und
   `testAuf25_1NachDemZiehenDesModellsDasDieEbeneIstBleibtEsDieEbene`, je mit Maus und Finger.
   Das zweite prüft auch, dass das *Modell* der *Ebene* allein ankommt.
4. `modellPerKlickTest.py`: `testAuf25_2DieSeiteKennzeichnetNachDemKlickAlleGesetztenModelleDerEinheit`
   (Maus und Finger), als eigener Test statt im bestehenden, damit dessen Aussage (Anfrage und
   *Ebene*) unverändert bleibt.

Alle Tests laufen mit dem vorhandenen Code grün (523 bestanden in `phasen/aufstellen`), ruff
und Format sind sauber; sie sind also nicht rot, weil der Code dazu schon steht.

Nachgeprüft (Fachkritiker): Die vier Fälle sind in Ordnung. Dass der Spiegel rot ist, steht
in [1560](1560-spiegelRotInModellPerKlickTest.md).
