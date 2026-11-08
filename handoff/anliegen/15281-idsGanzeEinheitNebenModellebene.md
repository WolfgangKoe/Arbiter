# ids und Hilfen sagen noch ganzeEinheit neben modellebene

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik zum Umbenennen nach [7800](7800-karteUndEbeneBenennen.md) (Commit 1523136),
Ergänzung zu [15260](15260-testnamenUeberHundertZeichen.md) Punkt 2, der die ids in
`vorruecken.py` und `ziehen.py` behandelt. Dieselbe Paarung steht noch an drei Stellen, je
neben einer schon umbenannten Hilfe:
- [einheitZuruecklegenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitZuruecklegenTest.py):
  ids `ganzeEinheit` und `einModell` für `ausgewählt` und `modellebeneWählen`.
- [modellPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/modellPerKlickTest.py):
  `ganzeEinheitDavor` mit id `ganzeEinheit` in der Fixture `zweitesBoyzModellOhneModellebene`.
- [vorruecken.py](../../technik/tests/akzeptanz/vorruecken.py): `ganzeEinheitAuswählen` neben
  `modellebeneDesLetztenWählen`, auch als Vorgabe `ebene: str = "ganzeEinheit"`.

**Kosten.** ids, eine Hilfe und ihre Aufrufe (`vorrueckenTest.py`, `vorrueckenZuruecknehmenTest.py`,
`grenzkreiseTest.py`, `einheitZuruecksetzenTest.py`), mechanisch, ohne Folge für Code oder Vertrag.
Ohne die Änderung heißt derselbe Fall im Testlauf je Datei anders.

**Gegenvorschlag.** Mit 15260 in Technikphase 11: ids `einheitenebene` und `modellebene`,
`ganzeEinheitDavor` → `einheitenebeneDavor`, `ganzeEinheitAuswählen` → `mitEinheitenebeneAuswählen`.

**Stellungnahme.**
