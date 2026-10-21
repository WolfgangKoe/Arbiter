# Tests zu Item anhaltenAnBases: Hilfen doppelt und quer abgelegt

1361 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item [anhaltenAnBases](../../domaene/items/anhaltenAnBases.md)
(Lesbarkeit). Nach [Ich 3](../../prozess/praemissen/ich.md) wartet das: Namen und Ablage
von Hilfsfunktionen, keine Prüfung ist rot. Was aufhält: [1360](1360-seiteOhneBeispielDerAbfrage.md).
1. Doppelt, Fortsetzung von Anliegen 1216: In
   `anhaltenAnEinerBaseTest.py` `millionstel` und `welchesGezogenWird` (stehen in
   `handgriffe.py`), `alsZahlen` (= `stelleImSpielstand`); in `anhalten.py` `verschiebung`
   (= `wegVon`), `float(….x)` in `stellenAlsZahlen`, `stellenDerAbfrage`,
   `stelleBeimLoslassenAbfragen` (= `körperDerStelle`), der Pfad `_vertrag` (steht in
   `dienst.py`); `millionstel` und `float(stelle.x)` in `setzenPerKlickTest.py`. Die Seite öffnen drei Tests
   mit `seiteZu(…, berührbar=eingabe == "finger")` und eigenem `parametrize`, obwohl
   `seiteMitEingabe` und `mitMausUndFinger` in derselben Datei importiert sind.
2. B5 steht zweimal: `Maus` und `Finger` in `anhalten.py` wiederholen `mitDerMausZiehen`
   und `mitDemFingerZiehen` aus `ziehen.py`, samt zehn Schritten.
3. `anhalten.py` hat vier Aufgaben, der Docstring nennt sie („Strecke, Berührung, Abfrage
   und Halten am Bildschirm“; Es, S): Prüfen der Strecke, Anfragen an den Dienst, Lesen des
   Vertrags, Bedienen der Seite. Die übrigen Hilfen sind nach Aufgabe geschnitten:
   `handgriffe.py` (Aufbau), `dienst.py`, `bildschirm.py`, `ziehen.py`.
4. `blockVorEinerFremdenBase` setzt voraus, dass die fremde *Base* 4″ tief steht („nur 0,5″
   von der fremden Base in 4″ Tiefe“). Das folgt verdeckt aus `tiefeDerErstenReihe` und
   `abstandDerReihen` der Fixture; ändert sich einer, trifft der Zug nichts mehr. `inZoll`
   ist als `tuple[int, int]` annotiert, `schrägAufDieBase` gibt ihm `Fraction`.
5. `anhaltenAnEinerBaseTest.py` hat 22.825 Zeichen, über dem Höchstmaß 20.000
   ([Kennzahlen](../../prozess/kennzahlen.md)); bis zur Teilung wächst die Datei nicht.
   Das Item dafür: [1362](1362-auf26Teilen.md).
6. In `blockAlsGanzesTest.py` wiederholen die zwei Tests aus 1360
   (`testAuf24_1DieSeiteSetztBeimHalten…`, `testAuf24_1DieSeiteSendetBeimLoslassen…`) dieselben
   sechs Zeilen: Seite öffnen, `Maus` und `Abfragen` anlegen, drücken, bewegen, auf die
   Antworten warten. `haltenUndLosslassen` in `anhalten.py` tut dasselbe ein drittes Mal.
7. Ebenda zitiert `# Regel: stelleBeimLoslassen.json` eine Beispieldatei; die Regel ist
   [V10](../../technik/architektur/handlungen.md), die das Beispiel festlegt (Es 8: Fundstelle).

**Kosten.** Ändert sich Format (V1) oder Zeigerweg (B5), trifft es zwei Stellen, eine wird
vergessen. Wer eine Anfrage an den Dienst sucht, sucht in zwei Modulen. Die Fälle aus
[1352](1352-luekenTestsZuAnhaltenAnBases.md) passen ohne 5 nicht mehr in die Datei.

**Gegenvorschlag.** Billig genug, um es mit 1360 zu tun; sonst in der nächsten Technikphase.
1. Die gemeinsamen Namen verwenden, eine Form, die Seite zu öffnen.
2. `Maus`, `Finger`, `Abfragen`, `aufDieAntwortenWarten`, `haltenUndLosslassen` nach
   `ziehen.py`; `mitDerMausZiehen` und `mitDemFingerZiehen` bestehen aus drücken, bewegen,
   loslassen von `Maus` und `Finger`. `kreiseDerKarte` nach `bildschirm.py` neben
   `gesperrteModelle`.
3. `stelleBeimLoslassenAbfragen`, `stelleBeimLoslassenDesVertrags`, `stellenDerAbfrage`
   nach `dienst.py`. In `anhalten.py` bleibt eine Aufgabe: Züge zum Anhalten aufbauen und
   prüfen.
4. Die Tiefe der fremden *Base* aus `aufstellung.stelle(fremdesModell)` oder als benannte
   Summe `tiefeDerErstenReihe + abstandDerReihen`; `inZoll(maß: tuple[Fraction | int, int], …)`.
5. `Zug`, die fünf Züge und `stellenDesZugs` nach `anhalten.py`; so bleibt Platz bis zur
   Teilung.
6. Eine Hilfe „halten“ (drücken, bewegen, auf die Antworten warten), die den Zeiger
   zurückgibt; `haltenUndLosslassen` und die zwei Tests rufen sie, beim Loslassen bleibt
   `aufDieHandlungWarten` im Test.
7. `# Regel: handlungen.md, V10, das Beispiel gilt für x=35 und y=28`.

Erledigt, wenn `grep -rn "float(stelle.x)\|float(abfrage\|def alsZahlen\|def verschiebung\|^millionstel = \|^welchesGezogenWird = \|class Maus\|_vertrag = " technik/tests/akzeptanz`
nur `handgriffe.py`, `dienst.py`, `ziehen.py`, `bildschirm.py` und `querschnitt/` findet,
`aufDieAntwortenWarten` nur in der Hilfe aus 6 aufgerufen wird und `grep -n "# Regel: stelleBeimLoslassen.json" technik/tests/akzeptanz -r`
nichts findet.

**Stellungnahme.** Angenommen und umgesetzt, Punkte 1 bis 5 ganz, 6 zur Hälfte, 7 offen.
1. `anhaltenAnEinerBaseTest.py` nimmt `millionstel`, `welchesGezogenWird`, `wegVon`,
   `stelleImSpielstand`; `stelleAus` entfällt für `erwarteteStelle` (gleiche Aufgabe, jetzt
   in `handgriffe.py`); die drei Seitentests rufen `seiteMitEingabe` und `mitMausUndFinger`.
   `setzenPerKlickTest.py` nimmt `millionstel` und `stelleImSpielstand`. In `dienst.py` lesen
   die drei Beispiele des Vertrags über eine Hilfe.
2. `mitDerMausZiehen` und `mitDemFingerZiehen` bestehen aus `Maus` und `Finger` in `ziehen.py`.
3. `Maus`, `Finger`, `Abfragen`, `aufDieAntwortenWarten`, `haltenUndLosslassen` stehen in
   `ziehen.py`, `kreiseDerKarte` in `bildschirm.py`, die drei Hilfen der Abfrage in `dienst.py`.
4. Die Tiefe der fremden *Base* ist `tiefeDerFremdenBase = tiefeDerErstenReihe + abstandDerReihen`;
   `inZoll` nimmt `tuple[Fraction | int, int]`.
5. `Zug`, die fünf Züge und `stellenDesZugs` stehen in `anhalten.py`; die Testdatei hat
   20.667 Zeichen, 667 über dem Höchstmaß, bis [1362](1362-auf26Teilen.md).
6. Die Hilfe `halten` (gibt den Zeiger zurück) steht in `ziehen.py` und `haltenUndLosslassen`
   ruft sie. Die zwei Tests in `blockAlsGanzesTest.py` rufen sie jetzt auch (Testautor).
7. Das `# Regel:` in `blockAlsGanzesTest.py` nennt `handlungen.md, V10`.

`blockAlsGanzesTest.py` importiert von `ziehen.py`, `dienst.py` und `bildschirm.py`; die
`# noqa: F401` in `anhalten.py` entfallen. `ruff check` und `ruff format --check` sind grün;
in `blockAlsGanzesTest.py` laufen dieselben 14 Fälle rot und 28 grün wie vorher.
