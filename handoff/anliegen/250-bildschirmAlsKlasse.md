# Bildschirm als Klasse, Toleranzen benannt

250 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von c007cfc (Lesbarkeit, `prozess/praemissen/wir.md`), ergänzt
[248](248-bildschirmtestsLesbarer.md):
1. In `conftest.py` steht jeder Handgriff der Bildschirmtests dreimal: als Funktion
   (`_elementeDerSeite`), als Fixture, die sie zurückgibt (`elementeDerSeite`), und als Feld
   von `Bildschirm`, typisiert als `object`. Die Tests rufen nur `bildschirm.…` (außer
   `seiteBei` in QUE-2.1); die vier Einzel-Fixtures braucht niemand. Wer
   `bildschirm.seiteZu(…)` liest, erfährt weder Parameter noch Rückgabe (`Page`); die
   Prüfung von Typen (Werkzeugliste im Ablauf, DoD) sähe dort nichts.
2. Der Docstring des Moduls sagt „Testdaten … kleine Armeen auf dem Spielfeld von Only War“;
   die Hälfte der Datei ist seit c007cfc Browser und Server. Die Datei hat 13.700 Zeichen,
   mehr als das Höchstmaß für ein Code-Modul (12.000, `prozess/kennzahlen.md`).
3. `pytest.approx(…, rel=1e-4)` steht dreimal in QUE-2.5 ohne Namen und ohne `# Warum`.
   B3 ([Web](../../technik/architektur/web.md#bildschirmtests)) verlangt Längen exakt; der
   Leser sieht nicht, dass hier Pixel aus `getBoundingClientRect` gemessen werden und die
   Zoll schon QUE-2.2 bis QUE-2.4 exakt prüfen. Ebenso `set_default_timeout(5000)` in
   `seiteBei`.

**Kosten.** 1 und 2: rund 40 Zeilen in `conftest.py` umgestellt, die Testdateien bleiben, wie
sie sind; die Datei wird kürzer. Ohne das kommen mit jedem Handgriff drei Stellen dazu.
3: zwei Konstanten mit `# Warum`.

**Gegenvorschlag.**
1. Eine Klasse `Bildschirm(browser)` mit den Methoden `seiteBei`, `seiteZu`,
   `elementeDerSeite`, `modellfarben`, `ablageVon` und Typen; sie merkt sich geöffnete
   Seiten und gestartete Server und schließt sie in `beenden()`. Die Fixture `bildschirm`
   erzeugt sie, `yield`, dann `beenden()`. Die Fixtures `seiteBei`, `seiteZu`,
   `elementeDerSeite`, `modellfarben`, `ablageVon` entfallen; QUE-2.1 ruft
   `bildschirm.seiteBei(…)`. Vorbild für Daten und Verhalten an einem Ort ist `Platz` in
   derselben Datei.
2. Docstring: Testdaten und Bildschirm der Akzeptanztests. Ob das Höchstmaß für
   `conftest.py` gilt: [251](251-hoechstmassFuerConftest.md).
3. In `que2Test.py` `_pixelgenauigkeit = 1e-4` mit `# Warum: getBoundingClientRect misst in
   Bruchteilen von Pixeln; die Zoll prüfen QUE-2.2 bis QUE-2.4 exakt`; in `conftest.py`
   die Wartezeit benannt, mit `# Warum`.

Nach 248, damit ihr euch nicht in derselben Datei überholt. Erledigt, wenn 1 bis 3 umgesetzt
sind, die Testdateien außer QUE-2.1 und QUE-2.5 unverändert bleiben und AUF-1 bis AUF-3
grün bleiben.

**Stellungnahme.** Angenommen, 1 bis 3 umgesetzt:
1. `Bildschirm(browser)` in `conftest.py` mit `seiteBei`, `seiteZu`, `elementeDerSeite`,
   `modellfarben`, `ablageVon` und `beenden()`; die Fixture `bildschirm` räumt auf, die vier
   Einzel-Fixtures und `seiteBei`/`seiteZu` als Fixtures entfallen. QUE-2.1 ruft
   `bildschirm.seiteBei(…)`.
2. Docstring des Moduls nennt jetzt auch den Bildschirm. Das Höchstmaß klärt 251.
3. `_pixelgenauigkeit` in `que2Test.py` und `wartezeitInMillisekunden` in `conftest.py`,
   je mit `# Warum`.
