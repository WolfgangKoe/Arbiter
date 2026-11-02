# Testdaten zu BEW-25.1 doppelt

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet (Ablage von Testdaten, keine Prüfung rot), Kritik an den Tests zu Item
anhaltenUebergehen nach 8b3286f.
[weiterziehenNachDemUebergehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/weiterziehenNachDemUebergehenTest.py):
Die Tabelle Abstand, Weg und ids (`überDerBewegungsweite`, `inDerNahkampfreichweite`,
`beide`) steht zweimal, einmal als `("abstand", "weg")`, einmal als Tupel `abstandUndWeg`, das
der Test wieder entpackt (Wir 3).

**Kosten.** Wenige Zeilen. Bleibt es, ändert man einen Fall an zwei Stellen.

**Gegenvorschlag.** Eine benannte Tabelle mit `abstand`, `weg`, `gründe`; der erste Test
übergeht `gründe`.

**Stellungnahme.**
