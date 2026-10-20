# Hindernis: Tests zu Item einheitVerschieben

1211 · Kritik · von Testautor → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Belegungsschwelle erreicht. Fertig: Tests AUF-20/21/24/25/26 in Domäne, Dienst und Bildschirm geschrieben (ebeneTest, einheitVerschiebenTest, blockAlsGanzesTest, modellPerKlickTest, anhaltenAnEinerBaseTest). Offen: 1. ruff (PLR0913 mehr als 5 Parameter in 13 Bildschirm- und Dienst-Tests, ARG001 in modellPerKlickTest anderesModellDavor und spielerEins, E501 anhaltenAnEinerBaseTest:97 und einheitVerschiebenTest:177, I001 ebeneTest). 2. Die Bildschirmtests zu 21.1, 21.2, 24.2, 26.1 laufen rot, ob aus dem richtigen Grund (nicht wegen Testfehler wie Zielpunkt außerhalb der Karte), ist ungeprüft. 3. 10 Tests grün (Randfälle Grenze berührt, nichtAusgewählt bei 20.4, Dienst 20.2), vor allem Regressionswächter. 4. Benennung, vulture, Spiegel (python3 -m pytest prozess/pruefungen) nicht gelaufen. 5. setzenPerKlickDavor in modellPerKlickTest unbenutzt, löschen. Anliegen 1190 ist erledigt. Das hält den Schritt „Tests zu Item einheitVerschieben“ von Testautor im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.**
Für [ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py) (AUF-20) und
[modellPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/modellPerKlickTest.py)
(AUF-25) erledigt: 1. ruff ohne Fehler (PLR0913 durch Fixtures mit Vorgeschichte, ARG001 durch
schlankere Vorgeschichten, I001). 2. Rot aus dem richtigen Grund geprüft: es fehlen `ebeneWählen`,
`ebeneAbwählen`, `ebene`, die Ebenen-Route des Dienstes (405) und der Klick der Seite. Die zwei
Seitentests zum Beispiel des Vertrags (25.1, 25.2) laufen nur mit der Maus, denn
`seiteMitSpielstand` kann keinen Finger. 3. Die acht grünen Tests sind Wächter für Bestehendes
(nichtAusgewählt bei 20.4 prüft jetzt, dass das gezogene Modell sich wirklich bewegt; der
Dienst-Test zu 20.2 prüft zusätzlich die Auswahl der Boyz). 4. `prozess/pruefungen` gelaufen: rot
blieb `klicken.py` außerhalb der Liste der Hilfsmodule; die Klickhandgriffe stehen jetzt in
`ziehen.py`, `klicken.py` ist gelöscht (Anliegen 1240 erledigt). Die Rückverfolgung zu AUF-26.2
und 26.3 gehört dem Testautor zu anhaltenAnBases; an meinen Dateien nichts. 5.
`setzenPerKlickDavor` entfernt. Offen für die Dateien des zweiten Testautors: Punkt 1 bis 3 dort.
Erledigt für einheitVerschiebenTest, blockAlsGanzesTest, anhaltenAnEinerBaseTest (Punkte 1 bis 4); offen bleiben ebeneTest und modellPerKlickTest (Punkte 1 und 5, Sache des zweiten Testautors).
- ruff: ohne Fehler, auch PLR0913 und E501. Weniger Parameter durch `stelleInDerZoneDesSpielersAnDerReihe` (neu in `handgriffe.py`, ersetzt `spielerEins`/`ersterSpieler`) und `modelleSetzen` statt `boyzSetzen`; in 24.2 ein Parameter `zugAufDenNachbarn`. `dx`/`dy` heißen `weg`.
- Bildschirmtests: rot aus dem richtigen Grund. Die Ziele (12 Zoll tief) liegen im Fenster und auf der Karte (Viewbox 44 x 60, Punkt im 1280 x 720 Fenster geprüft), es lag kein Testfehler vor. Der Grund: das Modell steht nach dem Loslassen nicht (26.1, 21.2: `gesetzt` ist falsch, jetzt vor dem Vergleich der Stelle geprüft, statt `NoneType` aus dem Vergleich) beziehungsweise das gezogene Modell ist gesperrt oder die Einheit rückt nicht mit (21.1, 24.2).
- Wächter: 26.1 in zwei Tests geteilt (Base berührt die Grenze, grün; ein Millionstel Zoll darüber, rot), beide prüfen auch keine Sperre und keinen Grund. 21.1 „Ungesetzte bleiben ungesetzt“ prüft nur noch die ungesetzten Modelle und dass das gezogene am Ziel steht (grün); die Verschiebung der gesetzten steht in den anderen 21.1-Tests.
- Zweite Zone: Domänentests laufen in beiden Zonen und scheitern in beiden an der fehlenden Funktion (`Base überdeckt`, nicht verschoben, nicht hineingerückt). Dienst- und Bildschirmtests laufen nur in der zweiten Zone, denn Spieler 1 hat dort die zweite Zone (`aufstellungNachDerZonenwahl`); das genügt, weil das Hineinrücken in der Domäne beide Zonen prüft.
- Kommentarregel und Benennung für die drei Dateien grün, Spiegel, Glossar, Importvertrag grün. Rot in `prozess/pruefungen` bleibt, was nicht an meinen Dateien liegt: `klicken.py` (Benennung), Rückverfolgung AUF-26.2 und 26.3 (Item anhaltenAnBases), Abdeckung und Starter.
