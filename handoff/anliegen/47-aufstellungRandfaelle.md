# Aufstellung: fremder Spieler, leere Armee, gespeichertes „beendet“

47 · Kritik · von Reviewer (Technik) → Implementierer · Runde 2/3 · angenommen

## Runde 1
Gegenstand: [`aufstellen.py`](../../technik/arbiter/domaene/phasen/aufstellen.py) aus `afe3205`.
Alle Befunde per Wegwerf-Aufruf belegt, die Akzeptanztests bleiben grün.

**Befund 1 · Ein fremder Spieler wird Gewinner.** `gewinnerWählen` prüft nicht, ob der Spieler
zur `Aufstellung` gehört. Mit einem dritten `Spieler` als Gewinner liefert `_gegnerVon` den
ersten Spieler; danach ist er *an der Reihe*, und `aufstellungszone()` gibt beiden Spielern
dieselbe Zone (`süd`, `süd`). `Aufstellung(spieler, spieler)` endet in `aufstellungszoneWählen`
mit `StopIteration`.
Kosten: ein still inkonsistenter Zustand statt eines Fehlers, sobald `web/` Spieler aus einer
Anfrage auflöst.
Gegenvorschlag: Vorbedingung, kein Fachfall und keine *Sperre* (die ließe sich übergehen):
`ValueError` in `gewinnerWählen`, wenn `gewinner not in self.spieler`, und im Konstruktor, wenn
beide Spieler dasselbe Objekt sind. Ein Einheitstest unter `tests/einheit/domaene/phasen/`.

**Befund 2 · Wer nichts aufzustellen hat, bleibt nach der Zonenwahl an der Reihe.**
`aufstellungszoneWählen` setzt `anDerReihe = _gegnerVon(gewinner)` ohne Blick auf die Armee.
Hat der andere keine Einheit (`Armee()` ist erlaubt), ist er *an der Reihe*, jede Wahl sperrt
‚nicht wählbar‘, die *Aufstellung* endet nie. Die Etappe sagt „wer fertig ist, wird
übersprungen“; `aufstellenDerEinheitBeenden` tut das schon über `_nächsterAnDerReihe`.
Kosten: Sackgasse ohne Ausweg; zwei Stellen entscheiden „wer ist dran“ verschieden.
Gegenvorschlag: `self.anDerReihe = self._nächsterAnDerReihe(self.gewinner)`; das ergibt in
jedem getesteten Fall den Nicht-Gewinner (AUF-1.3). Hältst du eine leere Armee für unmöglich,
dann stattdessen die Vorbedingung im Konstruktor wie in Befund 1.

**Befund 3 · `beendet` ist gespeicherter, ableitbarer Zustand.** Das Feld wird nur in
`aufstellenDerEinheitBeenden` gesetzt und ist dort gleich `anDerReihe is None`. Mit Befund 2
müsste auch `aufstellungszoneWählen` es setzen. Ebenso ist `self.anDerReihe is None` in
`aufstellenDerEinheitBeenden` (Zeile 55) unerreichbar: Eine *Einheit in Aufstellung* gibt es
nur, wenn jemand *an der Reihe* ist.
Kosten: zwei Wahrheiten, die beim nächsten Übergang auseinanderlaufen können; toter Zweig.
Gegenvorschlag: `beendet` als Property
`self._zoneDesGewinners is not None and self.anDerReihe is None`. Die Prüfung in Zeile 55 auf
`self.einheitInAufstellung is None` reduzieren; braucht der Typprüfer `anDerReihe`, ein
`# Warum:`-Kommentar oder ein `assert`.

**Zur Kenntnis, kein Befund:** Die *Einheit in Aufstellung* erneut zu wählen sperrt heute
‚Einheit begonnen‘; das regelt [Anliegen 41](41-dieselbeEinheitErneutWaehlen.md).

**Stellungnahme.** Angenommen, alle drei Befunde; umgesetzt mit Einheitstests.

## Runde 2
Nachgeprüft an `d7a468f`: Befund 1, 2 und `beendet` als Property in Ordnung.

**Rest Befund 3.** `or spieler is None` in `aufstellenDerEinheitBeenden` bleibt unerreichbar;
kein Test kann es töten, die Mutationsschwelle meldet es. Gegenvorschlag wie Runde 1: Sperre
nur auf `einheit is None`, für den Typ `assert spieler is not None`.

**Neu zu Befund 1.** `aufstellungszone(fremderSpieler)` liefert die Zone des Nicht-Gewinners.
Gegenvorschlag: dieselbe Vorbedingung (`ValueError`), ein Einheitstest.

Kosten: je zwei Zeilen; sonst ein falsches Ergebnis, sobald `web/` Spieler auflöst.
Blockiert nichts; am besten im Lauf zu [55](55-zustandInDerAufstellung.md), Runde 2.

**Stellungnahme.** Angenommen, beide Befunde. `or spieler is None` ist weg, dafür `assert` mit `# Warum:`. `aufstellungszone` wirft `ValueError` für einen fremden Spieler, Einheitstest ergänzt. Alle Tests und Prüfungen grün.
