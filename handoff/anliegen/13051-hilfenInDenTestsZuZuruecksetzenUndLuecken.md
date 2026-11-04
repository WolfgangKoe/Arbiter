# Hilfen in den Tests zu zuruecksetzenUndLuecken

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Hält nicht auf: Namen und Ablage von Hilfen.
1. [keinVorrueckenAusDerNahkampfreichweiteTest.py](../../technik/tests/akzeptanz/phasen/bewegung/keinVorrueckenAusDerNahkampfreichweiteTest.py):
   `inDerNahkampfreichweite` wiederholt Wahl des Spielers und ersten Zug aus `einheitAmZug`
   (`conftest.py`) mit eigener Tabelle; darum wählt
   `testBew22_1EineAndereEinheitAußerhalbDerNahkampfreichweiteDarfVorrücken` die andere
   *Einheit* mit `if … else`, die `einheitAmZug` schon liefert. Die Richtung zum Gegner
   (`richtung = 1 if … else -1`) rechnet der Test selbst neben `aufeinanderZuZiehen`.
   `assert not außerhalb` verneint doppelt.
2. [einheitZuruecksetzenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/einheitZuruecksetzenTest.py):
   „mit drei Augen vorgerückt, dann das erste *Modell* 2″ gezogen“ steht dreimal ausgeschrieben
   (`testBew24_1IstDieGezogeneEinheitVorgerückt…`, `testBew24_1DerDienstNenntZurVorgerückten…`,
   `testBew24_2OhneAngebot…`), neben der Hilfe `ganzeEinheitZiehen` für denselben Zweck.
3. [phaseBeendenTest.py](../../technik/tests/akzeptanz/querschnitt/phaseBeendenTest.py):
   `zügeBeenden(schlacht, 2 * letzteSchlachtrunde())` zweimal; die `2` steht für die Züge einer
   *Schlachtrunde*, wie in `zurLetztenSchlachtrunde` (`schlacht.py`).

**Kosten.** Testautor, etwa 20 Minuten; zieht 13050 die Fixture ohnehin um, gleich mit.

**Gegenvorschlag.** (1) `inDerNahkampfreichweite` baut auf `einheitAmZug` auf und liefert die
andere *Einheit* mit; eine Hilfe in `schlacht.py` zieht ein *Modell* um eine Länge auf ein
anderes zu; der Test prüft `assert innerhalb`. (2) Eine Hilfe `vorgerücktUndGezogen` neben
`ganzeEinheitZiehen`. (3) Eine Hilfe `schlachtBeenden` in `schlacht.py`.

**Stellungnahme.**
