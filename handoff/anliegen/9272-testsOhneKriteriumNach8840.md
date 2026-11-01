# Tests ohne Kriterium nach 8840

Form: Kritik
Von: Anforderungsautor
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach [8840](8840-baseNichtUeberdeckenAnhaltenStattSperre.md) sind gestrichen:
BEW-2 ganz (die Datei `sperrenBeimZiehen.md`), BEW-8.1, 8.2 und AUF-12.6 (neu gefasst als
AUF-12.9). Ohne Kriterium sind damit `testBew8_1…`, `testBew8_2…` in
`technik/tests/akzeptanz/phasen/bewegung/uebergehenBeimZiehenTest.py`, `testAuf12_6…` in
`technik/tests/akzeptanz/phasen/aufstellen/sperreOhneStelleTest.py` und die ganze
`technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py`. `kriterienregeln.rueckverfolgung`
meldet die ersten drei rot, damit jeden Commit.

**Kosten.** Bis sie fort sind, kann niemand committen.

**Gegenvorschlag.** Jetzt diese Tests löschen. `testBew3_1HältArbiterAnDerBewegungsweiteAnPrüftEsÜberEineBaseNurAnDerAngehaltenenStelle`
prüft ‚über eine Base‘ mit; ob er bleibt, entscheidest du. Tests zu BEW-17, BEW-8.3 bis 8.5,
QUE-1.4 und AUF-12.9 kommen mit dem Item des Planers ([9271](9271-anhaltenVorFremdenBasesPlanen.md)).

Wann: jetzt, vor dem Commit.

**Stellungnahme.** Umgesetzt: `sperrenBeimZiehenTest.py` und `uebergehenBeimZiehenTest.py`
gelöscht (dort standen nur BEW-8.1 und 8.2), die AUF-12.6-Tests samt ihrer Helfer aus
`sperreOhneStelleTest.py` entfernt, ebenso die verwaisten Helfer `übergehbarDesVertrags`
(`dienst.py`) und `ostenUndNorden` (`schlacht.py`). Auch
`testBew3_1HältArbiterAnDerBewegungsweiteAnPrüftEsÜberEineBaseNurAnDerAngehaltenenStelle` ist
fort: Seine eigene Aussage, ‚über eine Base‘ an der angehaltenen *Stelle*, hat kein Kriterium
mehr; BEW-3.1 prüfen die übrigen Tests. `kriterienregeln.rueckverfolgung` ist grün. Tests, die
‚über eine Base‘ nur als Mittel nutzen (QUE-5, QUE-6, BEW-1.7), habe ich dem Planer gemeldet:
[9320](9320-testsMitUeberEineBaseAlsMittel.md).
