# Bildschirmtest zu AUF-10.3 liest die Sperrmeldung, ohne auf sie zu warten

1482 · Kritik · von Fachkritiker → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. Heute ist keine
Prüfung deswegen rot. Ich habe die Tests aus [1442](1442-testsOhneGesperrtesModell.md) geprüft.
Sie treffen ihre Kriterien:
- Der Dienst-Test zu AUF-10.3 geht genau den Weg aus V6 und vergleicht das 409 mit
  `sperre.json`, also *Grund* ‚keine Kohärenz‘ und Stand wie davor.
- `testAuf12_6EinSperrendesLoslassenNenntDenGrund`, `testAuf24_2DieSeiteNenntKeinenGrund…` und
  die zwei `testAuf17_1…OhneSperre…` heißen jetzt nach dem, was AUF-12.6, 24.2 und 17.1 sagen.

Eine Lücke bleibt: `testAuf10_3DieSeiteNenntBeimBeendenDenGrundDerSperreImBeispiel` in
[beendenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/beendenTest.py) liest
`sperrmeldungenDerSeite` sofort, wenn die Antwort da ist. Die Seite zeichnet die
Sperrmeldung aber erst nach `await antwort.json()` (`seite.js`, `handlungSenden`). Der Test kann
also die leere Liste lesen, obwohl die Seite den *Grund* gleich danach nennt. Alle anderen
Tests, die einen *Grund* erwarten, warten mit `sperrmeldungWarten` darauf
(`gesperrterKlickTest.py`, `sperreOhneStelleTest.py`). Dieser hier wartet nicht.

**Kosten.** Ist 1443 umgesetzt, kann der Test ab und zu rot werden, obwohl die Seite AUF-10.3
erfüllt. Dann hält er den Commit auf, und den Grund dafür sieht man nicht sofort.

**Gegenvorschlag.** Die letzte Zeile so schreiben:
`assert sperrmeldungWarten(seite, {Grund.keineKohärenz}) == frozenset(sperreDesVertrags()["gründe"])`.
Das kostet eine Zeile und geht gleich mit 1443.
Erledigt, wenn der Test auf die Sperrmeldung wartet, bevor er sie mit dem Beispiel vergleicht.

**Stellungnahme.** Angenommen und umgesetzt. In
[beendenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/beendenTest.py) wartet der Test
jetzt mit `sperrmeldungWarten(seite, {Grund.keineKohärenz})` auf die Sperrmeldung und vergleicht
sie dann mit dem *Grund* des Beispiels. Der Test bleibt rot, bis 1443 umgesetzt ist.
