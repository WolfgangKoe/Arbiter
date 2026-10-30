# Bewegungsweite der Testhilfe liest die alte Ausgangslage

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (eine Prüfung ist rot; Plan 9, Item 1). `bewegungsweite(einheitenname)`
in [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) sucht in `ausgangslage.yaml` die
Schlüssel `Einheit` und `bewegungsweite`. Die gibt es seit der neuen Gliederung nicht mehr
([Katalog, K1](../../technik/architektur/katalog.md)): Die *Bewegungsweite* steht je
*Modellart* im *Datenblatt*. Folge: `pytest --co technik/tests/akzeptanz` bricht ab,
[anhaltenAnDerBewegungsweiteTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenAnDerBewegungsweiteTest.py)
mit `KeyError: 'Einheit'` schon beim Sammeln (Zeile 24), die Aufrufe in
[normaleBewegungTest.py](../../technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py)
(Zeilen 116, 173, 308) beim Lauf. Item 1 wird so nicht grün, und der Implementierer darf die
Hilfe nicht ändern. Daneben lesen jetzt zwei Funktionen YAML aus `domaene/daten/`: `_daten` in
`schlacht.py` und das neue `yamlAusDenDaten` in
[handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py) ([Wir 3](../../prozess/praemissen/wir.md)).

**Kosten.** Eine Hilfe und ihre gut 20 Aufrufe, ohne neue Tests. Bleibt es, sieht der
Stakeholder am Bildschirm, dass Arbiter wieder startet, aber die Tests der *Bewegungsphase*
laufen nicht, und keiner merkt, wenn die *Bewegungsweite* bricht.

**Gegenvorschlag.** In `schlacht.py`:
1. `bewegungsweite(datenblatt, modellart)` liest die *Bewegungsweite* der *Modellart* aus
   `katalog/<fraktion>/datenblaetter.yaml`, die *Fraktion* aus dem Eintrag der Ausgangslage
   mit diesem `datenblatt`, wie `profileDerModelle` in
   [ausgangslageTest.py](../../technik/tests/akzeptanz/missionsvorbereitung/ausgangslageTest.py);
   diese Suche zieht dazu in die gemeinsame Hilfe um, der Test nutzt sie von dort.
   Aufrufe: `bewegungsweite("Warboss", "Warboss")`, bei den Boyz die *Modellart* des
   gezogenen *Modells* (`gezogenes.modellart`), wo der Test eines hat, sonst `"Ork Boy"`.
2. `_daten` und `_datenordner` entfallen; `letzteSchlachtrunde` liest über `yamlAusDenDaten`.

**Stellungnahme.** Angenommen, wie vorgeschlagen. `bewegungsweite(datenblatt, modellart)` in
[schlacht.py](../../technik/tests/akzeptanz/schlacht.py) liest die *Modellart* aus dem
*Datenblatt* im Katalog; die Suche (`eintragDerAusgangslage`, `modellartenImKatalog`,
`profileDerModelle`) steht in [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py),
`ausgangslageTest.py` nutzt sie von dort. `_daten` und `_datenordner` sind weg,
`letzteSchlachtrunde` liest über `yamlAusDenDaten`. Aufrufe: Warboss und Overlord mit sich
selbst, Boyz mit `gezogenes.modellart` oder `weitesModell.modellart`, ohne *Modell* `"Ork Boy"`.
