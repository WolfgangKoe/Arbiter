# Einheitstests zur Auswahl sagen noch, ein Modell oder die Einheit sei die Ebene

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik am Code zum Umbenennen nach Anliegen 7800 (Commit
1523136), Lesbarkeit ([Es](../../prozess/praemissen/es.md), [Wir 2](../../prozess/praemissen/wir.md)).
Produktcode und Frontend folgen dem [Glossar](../../domaene/glossar.md): `hatEinheitenebene`,
`istModellebene`, `einheitenebeneWählen`, `.spielfeld`; ruff, Benennung, Glossar, Kommentare,
Frontendregeln und die Einheitstests sind grün, die umbenannten Akzeptanztestdateien zu QUE-2,
QUE-3, AUF-25 und BEW-9 auch. Nichts hält auf.
In [auswahlTest.py](../../technik/tests/einheit/domaene/phasen/aufstellen/auswahlTest.py)
sagen vier Testnamen noch, was 7800 F2 B abgelöst hat: Die *Einheit* oder ein *Modell* „ist“
die *Ebene*. Nach dem Glossar hat eine *ausgewählte* *Einheit* eine *Ebene*, die
*Einheitenebene* oder die *Modellebene* eines ihrer *Modelle*; der Code fragt
`hatEinheitenebene` und `istModellebene`, die Namen darüber nicht:
- `testEineAusgewählteEinheitIstSelbstDieEbeneUndAlleModelleSindAusgewählt`
- `testDieEbeneEinesModellsMachtNurDiesesModellAusgewählt`
- `testNurDasGewählteModellIstEbene` (darin `ohneEbene`, das `istModellebene` vor dem Klick hält)
- `testDasEbeneModellErneutAnklickenKehrtZurEinheitZurück`

**Kosten.** Vier Namen und eine Variable in einer Datei, mechanisch; kein Code, kein Vertrag,
keine Prüfung ändert sich. Ohne die Änderung liest man im Einheitstest ein anderes Modell als im
Glossar und im Code darunter.

**Gegenvorschlag.** In Technikphase 11 umbenennen:
- `testEineAusgewählteEinheitHatDieEinheitenebeneUndAlleModelleSindAusgewählt`
- `testDieModellebeneEinesModellsMachtNurDiesesAusgewählt`
- `testNurDasAngeklickteModellIstModellebene`, `ohneEbene` → `vorDemKlick`
- `testDasModellDerModellebeneErneutAnklickenKehrtZurEinheitenebeneZurück`

**Stellungnahme.**
