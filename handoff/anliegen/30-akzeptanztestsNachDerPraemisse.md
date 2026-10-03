# AUF-1-Tests nach der Prämisse zur Benennung

30 · Kritik · von Organisationsentwickler (Prozess) → Testautor · Runde 1/3 · angenommen

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

**Stellungnahme.** Angenommen und umgesetzt: `phasen/aufstellenTest.py` ersetzt `test_auf_1.py`;
Funktionen, Variablen und Fixtures in camelCase (`ersterSpieler`, `zweiterSpieler`), Testnamen
`testAuf1_<m>…`, Enum-Werte nach Anliegen 28 F1 (`Grund.nichtWählbar`, `nichtInAufstellung`,
`einheitBegonnen`), Fachobjekte entpackt, `sperrgrund(handlung, *argumente)` ohne lambda,
Docstrings einzeilig, Prozessverweise entfernt. Fälle und Kriterien bleiben; wo ein Test zwei
Handlungen trug, ist er nach Handlung geteilt (AUF-1.7), AUF-1.5 nach der Aufstellung ist
parametrisiert statt Schleife. Neu ist nur, dass AUF-1.2 „erst Gewinner, dann Zone“ die Zone
prüft statt nichts. Die Code-Bezeichner folgen dem Glossar (Anliegen 29). Ort und Importpfade
bleiben bei [Anliegen 27](27-auf1-tests-ort-und-importpfade.md), Wahl und Gewinner bei 26.
