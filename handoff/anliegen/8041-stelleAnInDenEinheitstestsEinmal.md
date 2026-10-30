# stelleAn in den Einheitstests einmal

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit), `git diff 0491ad5 0015ae7`. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Ablage einer Hilfsfunktion, keine Prüfung rot.
Mit [bewegungsphaseTest.py](../../technik/tests/einheit/domaene/phasen/bewegung/bewegungsphaseTest.py)
steht `stelleAn(inX, inY)` zum vierten Mal gleich im Text, daneben in
`anhaltenAnDerBewegungsweiteTest.py`, `anhaltenAnEinerBaseTest.py` und
`einheitVerschiebenTest.py` ([Wir 3](../../prozess/praemissen/wir.md)).

**Kosten.** Am Bildschirm nichts. Ändert sich `Stelle`, ändern sich vier Hilfen.

**Gegenvorschlag.** `stelleAn` einmal neben `modellMit` in
[modelle.py](../../technik/tests/einheit/modelle.py) (oder einer eigenen Hilfsdatei der
Einheitstests), die vier Tests importieren es.

**Stellungnahme.**
