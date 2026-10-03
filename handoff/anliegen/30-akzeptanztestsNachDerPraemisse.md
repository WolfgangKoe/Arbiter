# AUF-1-Tests nach der Prämisse zur Benennung

30 · Kritik · von Organisationsentwickler (Prozess) → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** [test_auf_1.py](../../technik/tests/akzeptanz/phasen/test_auf_1.py) und
[conftest.py](../../technik/tests/akzeptanz/conftest.py) folgen nicht der
[Prämisse](../../prozess/praemissen/wir.md): Dateiname, snake_case bei Funktionen und
Fixtures, Fixtures `a` und `b`, Indizes wie `b.armee.einheiten[0]`, lambda als Hülle um die
Handlung und `lambda e=einheit:` in AUF-1.5.

**Kosten.** Der Implementierer übernimmt die Namen der Schnittstelle; jeder spätere Umbau
ändert Tests und Code zugleich. Jetzt sind es zwei Dateien.

**Gegenvorschlag.** Umbenennen nach dem Skill `akzeptanztest-schreiben`:
`phasen/aufstellenTest.py`, `testAuf1_6MitGesetztemModellIstDieEinheitBegonnen`,
`sperrgrund(handlung, *argumente)`, Fixtures `ersterSpieler`, `zweiterSpieler`, Fachobjekte
entpacken. Code-Bezeichner nach [Anliegen 29](29-glossarCodeBezeichnerInCamelCase.md),
zusammen mit [26](26-auf1-tests-erneute-wahl-und-gewinner-nach-zone.md) und
[27](27-auf1-tests-ort-und-importpfade.md).

**Stellungnahme.**
