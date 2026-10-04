# Verteilung: Test erkennt die Zahl je Balken nicht, Achsenmarke doppelt

202 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · offen

## Runde 1
Kritik am Code von 6d0c615 (Anliegen 191, zweite Runde). a214e08 (Anliegen 179) ist ohne
Befund: `sonarlint.py` meldet mit `technik/tests/einheit` keine Funde, `sonarlintTest.py` grün.

**Befund 1 (Test).** `testVerteilungHatYAchseUndZahlJeBalken` in
`prozess/pruefungen/dashboardTest.py` prüft die Zahl je Balken mit
`">2</text>" in verteilung and ">1</text>" in verteilung`. Bei den Testdaten (höchste
Anzahl 2) schreibt die y-Achse die Marken 0, 1 und 2 als `<text class="achse-text" …>1</text>`
und `…>2</text>`. Die Bedingung gilt also schon durch die Achse. Nachgeprüft: Entfernt man
aus der erzeugten Seite alle `<text class="wert-text" …>`, gilt die Bedingung weiter. Fehlt die
Zahl über dem Balken, bleibt der Test grün, solange die Bildunterschrift bleibt.

**Befund 2 (Wiederverwendung).** In `histogramm` (`prozess/pruefungen/dashboard.py`) steht
das Markup der Achsenmarke (kurzer `gitter`-Strich, `achse-text` rechtsbündig, 4 und 6 Pixel
links vom Rand, Text 3 Pixel tiefer) noch einmal. `achsenmarke` macht dasselbe für das
Säulendiagramm, nur mit `randLinks` und `kilo(wert)`. Zwei Kopien: Ändert sich der Stil der
Achse, muss man beide Stellen anfassen.

**Kosten.** Befund 1: eine Bedingung im Test. Befund 2: eine Funktion bekommt Lage, Rand und
Text als Parameter; keine Änderung an der Ausgabe.

**Gegenvorschlag.**
1. Im Test die Klasse mitprüfen, etwa
   `re.findall(r'class="wert-text"[^>]*>(\d+)</text>', verteilung)[:3] == ["2", "0", "1"]`,
   oder die Zahl je Balken mit Werten prüfen, die keine Achsenmarke ergeben.
2. `achsenmarke(lage, rand, text)` für beide Diagramme verwenden: Das Säulendiagramm ruft sie
   mit seiner Lage, `randLinks` und `kilo(wert)` auf, das Histogramm mit `oben(marke)`,
   `histogrammRand` und `marke`.

**Stellungnahme (Regelumsetzer).**
