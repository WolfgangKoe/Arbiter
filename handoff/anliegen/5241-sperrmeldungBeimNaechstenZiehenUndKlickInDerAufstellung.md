# Sperrmeldung beim nächsten Ziehen und Klick in der Aufstellung

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Lücken abseits des Happy Path).
1. BEW-2.3, „nennt jeden *Grund* bis zur nächsten Handlung“:
   `testBew2_3DieSeiteNenntDenGrundBisDieNächsteHandlungBeantwortetIst`
   ([sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py))
   prüft nur, dass der *Grund* nach der nächsten Handlung fehlt, nicht, dass er bis dahin
   steht. Hält man das *Modell* beim nächsten Ziehen, fragt die Seite nach V10, ohne Handlung;
   V7 ([Querschnitt](../../technik/architektur/vertrag/querschnitt.md)) nimmt nur V2 und V9
   aus, die Meldung verschwände also schon beim Halten. Der Happy Path läuft: Der *Spieler*
   hat den *Grund* nach dem Loslassen gelesen.
2. AUF-20.6, „und keine andere“, in der *Aufstellung*
   ([ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py)): Vor dem Klick
   ist dort keine *Einheit* *ausgewählt*; in der *Schlacht* prüft es
   `testAuf20_6EinKlickAufEinModellWähltKeineAndereEinheit`.

**Kosten.** Keine in Zyklus 8. Bleibt 1, verschwindet der *Grund*, sobald man wieder zieht;
bleibt 2, bliebe in der *Aufstellung* eine zweite *Einheit* *ausgewählt*, unbemerkt.

**Gegenvorschlag.**
1. Im Test nach dem zweiten Drücken mit `halten` den *Grund* noch prüfen, erst nach dem
   Loslassen keinen; vorher eine Frage an den Architekten, V7 um V10 zu ergänzen (wie V14 in
   Anliegen 5140).
2. Ein Test in der *Aufstellung*: Warboss *ausgewählt*, Klick auf ein *gesetztes* Boyz; danach
   sind nur die Boyz *ausgewählt*.

**Stellungnahme.**
