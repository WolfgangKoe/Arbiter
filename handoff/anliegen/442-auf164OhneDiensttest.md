# AUF-16.4 ohne Test in der Domäne, bildschirm.py über dem Höchstmaß

442 · Kritik · von Reviewer → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** DoD über das Inkrement von Plan 5.
1. `einheitAufAblageLoslassen` mit der eigenen *Ablage* ändert nichts
   ([V5](../../technik/architektur/handlungen.md), AUF-16.4). Diesen Weg ruft kein Test:
   Der Akzeptanztest `testAuf16_4…` in
   [loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py)
   prüft nur, dass die Seite keine Anfrage sendet; Coverage meldet den Zweig
   `135->exit` in [aufstellen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py)
   als nie genommen, auch nicht von Einheitstests.
2. [bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py) hat 13.670 Zeichen; als
   Code-Modul gilt 12.000/8.000 ([Kennzahlen](../../prozess/kennzahlen.md)).

**Kosten.** (1) Wirft die Domäne bei der eigenen *Ablage* künftig eine *Sperre*, bleibt
jeder Test grün; per HTTP bekäme der *Spieler* dann einen *Grund*, den AUF-16.4 verbietet.
(2) Read lädt die ganze Datei; über dem Höchstmaß wächst sie nicht weiter.

**Gegenvorschlag.**
1. Ein zweiter Test zu AUF-16.4 über `einheitAufAblageLoslassen(einheit, eigeneAblage)`:
   *Stellen* und *Einheit in Aufstellung* wie davor, keine *Sperre* (Fixture wie
   `testAuf16_5…`).
2. `bildschirm.py` teilen, etwa Ziehen (B5) in ein eigenes Modul, bis 8.000 Zeichen.

**Stellungnahme.** Angenommen.
1. In [loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py)
   zwei neue Tests zu AUF-16.4, je ohne und mit drei *gesetzten* *Modellen*: in der Domäne
   (`einheitAufAblageLoslassen` mit der eigenen *Ablage*, keine *Sperre*, *Stellen* und
   *Einheit in Aufstellung* wie davor) und über den Dienst (200, Spielstand unverändert).
2. Das Ziehen (Maus, Finger, Bildpunkt, Warten auf die Antwort) steht jetzt in
   [ziehen.py](../../technik/tests/akzeptanz/ziehen.py) (5.135 Zeichen); `bildschirm.py` hat
   8.880, unter dem Höchstmaß 12.000, über dem Kürzungsmaß 8.000. Weiter teilen
   bringt keinen klaren Schnitt (Lesen der Seite, Auswahl, Browser hängen zusammen); sag, wenn
   du 8.000 verlangst. Die Importe der sechs betroffenen Testdateien sind angepasst, alle 347
   Akzeptanztests laufen grün.

Nebenbei: Dass „AUF-5.5, AUF-10.5, AUF-15.2, AUF-13, AUF-9.2, AUF-9.5, AUF-11, QUE-6, QUE-5
wartet auf den Testautor“ steht, liegt an der Stand-Anzeige. Diese Kriterien gehören nicht zu
Plan 5: [Plan 5](../plan.md) nennt sie unter „Noch nicht“ und „Danach“ (Plan 6), AUF-5.5
bleibt draußen. Ich schreibe dazu keine Tests; die Anzeige gehört dem Organisationsentwickler.
