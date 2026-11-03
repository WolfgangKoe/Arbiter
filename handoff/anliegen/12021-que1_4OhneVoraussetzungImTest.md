# QUE-1.4: Der Test sichert das Anhalten nicht

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet (Kritik: keine Prüfung rot, Test trifft sein Kriterium heute).
`testQue1_4SperrtBaseÜberdecktNachDemAnhaltenBietetDerDienstGemeinsamÜbergehenNichtAn`
([setzenTest.py](../../technik/tests/akzeptanz/querschnitt/setzenTest.py)) prüft
[QUE-1.4](../../domaene/anforderungen/querschnitt/setzen.md) nur, wenn BEW-3.1 den Warboss
anhält; sonst böte BEW-8.3 ohnehin nichts an. Nachgerechnet hält er nach 5″ an, *überdeckt*
dort nur den fünften Boy (wie an `zuvor`), der vierte liegt 0,013″ außerhalb. Der Test sagt
das nicht: Rücken die Boyz in den Daten, prüft er still nichts mehr oder sperrt wegen eines
anderen Boys.

**Kosten.** Heute keine; nach einer Änderung an `formation.yaml` ein grüner Test ohne
Aussage (Absicht 1, 692).

**Gegenvorschlag.** Vor dem Handeln eine Zusicherung mit Meldung wie in
`warbossÜbergehenBisZumZugDerNecrons`: Die *Distanz* vom Warboss zum siebten Boy liegt über
seiner *Bewegungsweite*, und der Punkt nach BEW-3.1 *überdeckt* nur den fünften Boy.

**Stellungnahme.**
