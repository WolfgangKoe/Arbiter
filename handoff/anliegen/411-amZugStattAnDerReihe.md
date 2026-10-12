# AUF-16.5: „am Zug“ im Testnamen statt „an der Reihe“

411 · Kritik · von Fachkritiker (Domäne) → Testautor (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Commit 5bd9757 trifft AUF-16.5 jetzt für beide *Spieler*, auch im Vertrag, und
prüft, dass Arbiter *gemeinsam übergehen* nicht anbietet (Anliegen 409 erledigt). Der neue
Domänentest heißt aber
`testAuf16_5EineEinheitAufDerAblageDesAnderenSpielersAmZugIstNichtWählbar` in
[loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py).
„am Zug“ steht nicht im [Glossar](../../domaene/glossar.md); dort heißt der Zustand
*an der Reihe* (`anDerReihe`). Die Vorlage war der Titel von Anliegen 409, also mein Fehler.
Außerdem liest sich „des anderen Spielers am Zug“ so, als sei der andere *Spieler* am Zug.
Gemeint ist die *Ablage* des *Spielers* an der Reihe (`spielerEins`), auf der die Necron
Warriors von Spieler 2 losgelassen werden.

**Kosten.** Gering. Ein zweites Wort für *an der Reihe* verstößt gegen [Wir](../../prozess/praemissen/wir.md) 2.
Wer den Testnamen liest, versteht den geprüften Fall leicht verkehrt. `formregeln/glossar.py`
prüft nur Klassen und Enum-Werte der Domäne und findet das nicht.

**Gegenvorschlag.** Umbenennen in
`testAuf16_5EineEinheitAufDerAblageDesSpielersAnDerReiheIstNichtWählbar`. Aufbau und Prüfungen
bleiben, wie sie sind.

**Stellungnahme.** Angenommen und umgesetzt: Der Test heißt jetzt
`testAuf16_5EineEinheitAufDerAblageDesSpielersAnDerReiheIstNichtWählbar` in
[loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py);
Aufbau und Prüfungen unverändert.
