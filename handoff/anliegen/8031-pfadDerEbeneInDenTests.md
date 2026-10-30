# Pfad der Ebene in den Tests

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält nicht auf. Seit Anliegen 4921 gibt es V9 `…/modelle/<m>/ebene` im Vertrag
nicht mehr; jeder Klick auf ein *Modell* geht über V14
([Aufstellen · Auswahl](../../technik/architektur/vertrag/aufstellen/auswahl.md)). In
[bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py) nennt `pfadeDesAuswählens` noch
`"/ebene"`. Die Route entfernt der Implementierer
([8030](8030-routeDerEbeneEntfaellt.md)); danach steht in den Tests ein Pfad, den es nicht gibt.

**Kosten.** Ein Eintrag. Bleibt er, liest man daraus eine dritte Art des Auswählens.

**Gegenvorschlag.** `pfadeDesAuswählens = ("/ausgewählt", "/anklicken")`.

**Stellungnahme.** Angenommen. In [bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py)
steht `pfadeDesAuswählens = ("/ausgewählt", "/anklicken")`. Kein Test wartet mit
`aufDieHandlungWarten` auf einen Klick auf ein *Modell*; der Eintrag fällt darum weg, ohne dass
ein Test anders ausgeht.
