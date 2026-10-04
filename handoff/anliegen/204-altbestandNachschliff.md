# Altbestand: Regelzeile, Ableitung, Dateisuche

204 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 8d51d93 (Anliegen 163). Die Suite ist grün (549 Tests). Die
Gegenprobe greift: Fehlt `extend-exclude`, meldet ruff 7 Fehler im Altbestand. Drei Befunde:

**B1 · Die Regelzeile in `prozess/regeln.md:14` hat fünf Zellen, die Tabelle hat drei
Spalten.** Die Altbestand-Regel ist an die Scheiter-Test-Zelle der Regel „nur lesbar“
angehängt („…`bashPositivlisteTest.py`; der Altbestand … nicht im Lauf von pytest ohne Pfad |
`pyproject.toml` … | `konfigurationTest.py` …“). Gemessen: Zeile 14 hat 4 Trenner, alle
anderen 41 Zeilen haben 2. Der Satz ist außerdem nicht lesbar („steht in … und `testpaths`
nicht im Lauf“).
Kosten: In der gerenderten Tabelle fehlen Mechanismus und Scheiter-Test der neuen Regel ganz,
weil Markdown überzählige Zellen weglässt. Der Stakeholder findet gerade diese Regel nicht.
Gegenvorschlag: eine eigene Zeile, etwa „Der Altbestand (`agenten.altbestandOrdner`) wird
nicht geprüft: ruff, Benennung, pytest ohne Pfad; git ignoriert ihn | `pyproject.toml`
(`extend-exclude`, `testpaths`), `.gitignore`, `benennung.ausgeschlosseneOrdner` |
`konfigurationTest.py`, `benennungTest.py`“.

**B2 · `altbestandOrdner` nimmt jeden Ordner aus `nurLesbar`, auch einen verschachtelten.**
`agenten.py:57` leitet aus jedem Eintrag mit `/` am Ende ab. In 163, B3, stand „ohne
`handoff/`“. „Nur lesbar“ und „Altbestand“ sind zwei verschiedene Aussagen.
Kosten: Wird einmal ein Ordner wie `handoff/vorlagen/` nur lesbar, wird er still von ruff
ausgenommen. `ausgeschlosseneOrdner` vergleicht nur einzelne Ordnernamen, deshalb wirkt der
Eintrag dort nicht, und `testDieBenennungÜbergehtDenAltbestand` bleibt trotzdem grün.
`testGitIgnoriertDenAltbestand` verlangt dann, dass git einen versionierten Ordner ignoriert.
Gegenvorschlag: nur Einträge der obersten Ebene ableiten (`eintrag.count("/") == 1`, am Ende).
Ein Scheiter-Test mit einem verschachtelten Eintrag zeigt, dass er nicht zum Altbestand
gehört.

**B3 · `geprüfteDateien` sortiert und durchläuft alle Funde zweimal.** `benennung.py:199-200`
ruft `sorted(gefunden)` einmal je Endung auf und prüft die Endung erst in der Schleife.
Kosten: doppelte Arbeit bei jedem Commit. Außerdem liest sich die Funktion umständlicher als
nötig.
Gegenvorschlag: beim Abstieg nur `.py` und `.md` sammeln. Danach einmal sortieren, mit dem
Schlüssel (Endung `.py` zuerst, Pfad); so bleibt die Reihenfolge wie heute. Klein; wenn dir
das zu wenig bringt, darfst du begründet ablehnen.

Erledigt, wenn B1 und B2 umgesetzt sind, B3 umgesetzt oder begründet abgelehnt ist,
`python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Commit geprüft hat.
