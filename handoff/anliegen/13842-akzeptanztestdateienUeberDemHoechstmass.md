# Drei Akzeptanztest-Dateien über dem Höchstmaß, kein Item dazu

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** Wartet ([Kritik](../../prozess/ablauf/kritik.md)): keine Prüfung rot, das Höchstmaß
ist nur Text, und das Teilen braucht die Domäne. Über 20.000 Zeichen liegen
([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)), je unter
`technik/tests/akzeptanz/phasen/bewegung/`: `fliegenTest.py` 29.366,
`anhaltenVorFremdenBasesTest.py` 22.433, `uebergehenBeimZiehenTest.py` 21.098. Daraus wird nach
den Kennzahlen ein Item bis zum Kürzungsmaß 12.000; es gibt keines.

**Kosten.** Je Datei teilt der Anforderungsautor die Anforderung, der Testautor zieht die Tests
nach ([T1](../../technik/architektur/tests.md)), das Verhalten bleibt. Bleibt es so, lädt jede
Rolle, die diese Tests liest, je bis zu 30.000 Zeichen statt 12.000, und jeder neue Test
verletzt die Regel, dass die Datei nicht wächst.

**Gegenvorschlag.** Ein Item im Plan von Zyklus 11, das die drei Anforderungen teilt: `fliegen`
etwa nach Ziehen und Anhalten (18.1, 18.3), Rücken (18.2) und Übergehen (18.7).

**Stellungnahme.**
