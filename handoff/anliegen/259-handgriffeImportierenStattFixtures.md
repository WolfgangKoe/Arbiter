# Handgriffe importieren, Fixtures nur für Zustand

259 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von d6e3af0 (Schnittstelle, `prozess/praemissen/wir.md`):
1. Zehn Fixtures in `technik/tests/akzeptanz/conftest.py` geben nur eine Funktion aus
   `handgriffe.py` zurück (`einheitenAufstellen`, `modelleSetzen`, `radiusInZoll`,
   `sperrgründe`, `spielerMit` …). Nötig war das, solange `conftest.py` nicht importierbar
   war; seit 256 ist `tests.akzeptanz.handgriffe` ein Modul. Wer einen Test liest, sieht
   `einheitenAufstellen` als Parameter ohne Typ, sucht in `conftest.py` und landet erst dann
   in `handgriffe.py`; die IDE zeigt keine Signatur. Dasselbe Muster hat 250 beim Bildschirm
   beseitigt. Die Parameter füllen die Liste: 18 Tests stehen auf dem Höchstwert 5 von ruff
   `PLR0913`. Die Folge zeigt sich schon: `testAuf4_6VorDerWahl…` nimmt `spielerEins` und
   `spielerZwei` nicht mehr als Fixture, sondern legt sie im Test aus `ausgangslage` an, unter
   denselben Namen.
2. `Bildschirm.elementeDerSeite` und `Bildschirm.ablageVon` benutzen `self` nicht (ruff
   `PLR6301`, preview, meldet beide), `modellfarben` nur für `self.elementeDerSeite`. Die
   Klasse hat damit zwei Gründe zur Änderung: Lebenszyklus (Browser, Server, schließen) und
   Lesen der Seite. Das geht auf meinen Gegenvorschlag in 250 zurück, der alles in die Klasse
   legte.
3. Der Docstring von `conftest.py` nennt Browser und Server; die stehen jetzt in
   `bildschirm.py`, `conftest.py` hat nur Fixtures.

Zur Einordnung: Eine Fixture lohnt sich für Zustand, den pytest je Test neu baut
(`aufstellungNachDerZonenwahl`) oder aufräumt (`bildschirm`). Eine Funktion ohne Zustand wird
importiert und gerufen, wie `sperrgrund` im Beispiel des Skills `akzeptanztest-schreiben`.

**Kosten.** Rund 50 Zeilen weniger in `conftest.py`; in den Testdateien je ein Import und
kürzere Parameterlisten, die Rümpfe bleiben (`einheitenAufstellen(…)` heißt weiter so). Ohne
das wächst `conftest.py` mit jedem Handgriff um eine Fixture, die nichts tut, und jeder
Handgriff drückt seinen Test an `PLR0913`. Kein Test prüft danach etwas anderes; der
Implementierer wird nicht blockiert.

**Gegenvorschlag.**
1. Die Testdateien importieren die Handgriffe, etwa
   `from tests.akzeptanz.handgriffe import einheitenAufstellen, modelleSetzen`; die zehn
   Fixtures, die nur eine Funktion zurückgeben, entfallen. `testAuf4_6VorDerWahl…` nimmt
   wieder `spielerEins` und `spielerZwei` als Fixture.
2. `elementeDerSeite`, `modellfarben` und `ablageVon` werden Funktionen in `bildschirm.py`
   (`ablageVon(seite, "Spieler 1")`), die Tests importieren sie; `Bildschirm` behält
   `seiteBei`, `seiteZu` und `beenden`. Alternative: eine Klasse `Seite` um `Page`, gelesen als
   `seite.ablageVon("Spieler 1")`; schöner, aber sie muss `locator`, `set_viewport_size` und
   `evaluate` weiterreichen. Ich empfehle die Funktionen.
3. Docstring etwa: „Fixtures der Akzeptanztests: Testdaten, Spielstände, Bildschirm.“

Am billigsten zusammen mit 248 Punkt 7 (git) nach dem Implementierer, damit `conftest.py` und
die Testdateien nur einmal angefasst werden. Erledigt, wenn 1 bis 3 umgesetzt sind, keine
Fixture nur eine Funktion zurückgibt und `python3 -m pytest technik/tests` dieselben Tests
sammelt und dieselben grün sind wie vorher.

**Stellungnahme.**
