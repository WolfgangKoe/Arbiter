# Test zu BEW-19

Form: Kritik
Von: Anforderungsautor
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Nach Anliegen 9420 steht das gestrichene BEW-2.7
wieder als [BEW-19.1](../../domaene/anforderungen/phasen/bewegung/einheitAlsGanzes.md). Sein
Test fiel mit `sperrenBeimZiehenTest.py` (9272); es steht noch in
`HEAD:technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py:288`.

**Kosten.** Ohne Test merkt niemand, wenn die Ausnahme beim Umbau im Item
[anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md) fortfällt.

**Gegenvorschlag.** Den Test als `einheitAlsGanzesTest.py` wiederherstellen; er zieht die
ganze *Einheit* um weniger als den *Durchmesser* ihrer *Bases*.

Wann: Technikphase, vor dem Item anhaltenAufDemWeg.

**Stellungnahme.**
