# Drei Reste aus P3: Regelzeile, Testname, Item ohne Umfang

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Nachprüfung von 11500, 12900 und 13102 (aed32df): Das Verhalten stimmt, die
Scheiter-Tests in `standregeln/abhakenTest.py` sind grün und wären ohne die Änderung rot.
Drei Reste:
1. [Standregeln](../../prozess/regeln/standregeln.md) widerspricht sich: Die Zeile Retro 9 P1
   sagt weiter „den kein beseitigtes Hindernis desselben Schritts nennt“ und nennt als
   Scheiter-Test „Hindernis des anderen Kritikers zählt nicht“; diesen Test gibt es umgekehrt.
   Die Zeile Retro 10 P3 „ändert Retro 9 P1“: Wer liest, muss beide zusammensetzen
   ([Wir 3, 4](../../prozess/praemissen/wir.md)).
2. `standJeTest` in `standVorDerUmsetzung.py` sucht den Commit eines Tests mit
   `-S "def <name>"`. Das trifft auch längere Namen mit demselben Anfang: Unter den 673
   Akzeptanztests beginnt `testAuf7_2EinModellEinerAufgestelltenEinheitIstNichtWählbar` mit
   einem anderen Testnamen. Ist der längere älter, misst Abhaken einen nachgereichten Test
   wieder am Stand vor der Umsetzung, der Fall von 12900.
3. `umfangDes` in `testsRot.py` liefert für ein Item ohne Zeile „Umfang:“ nichts; dann prüft
   Abhaken keinen Test und hakt ab. Heute haben alle Items die Zeile (auch alle gelöschten in
   git), Pflicht ist sie nur als Text ([Domäne](../../domaene/CLAUDE.md), `items/<id>.md`).
   Eine Prüfung, die still nichts prüft, ist der Fall aus [Absicht 1](../../prozess/praemissen/absicht.md).

**Kosten.** 1: eine Zeile Text. 2: ein Zeichen im Muster und ein Fall in `abhakenTest.py`.
3: wenige Zeilen und ein Fall. Bleibt es: 1 kostet jeden Leser die Auflösung, 2 und 3 je
einen falschen Haken oder eine Runde des Testautors, selten.

**Gegenvorschlag.** Ohne Probe in `/tmp`; die gehört zur Umsetzung.
1. Die Zeilen Retro 9 P1 und Retro 10 P3 zu einer mit dem geltenden Stand zusammenführen,
   die Liste der Scheiter-Tests berichtigt.
2. `-S "def <name>("`; Fall: ein älterer Test mit längerem Namen und ein nachgereichter mit
   kürzerem, der nachgereichte wird am Stand seines Commits gemessen.
3. Ein Item ohne „Umfang:“ macht Abhaken rot und nennt das Item, statt still abzuhaken
   (bestehende Regel: Format der Items in [Domäne](../../domaene/CLAUDE.md)); Fall in
   `abhakenTest.py`.

**Stellungnahme.**
