# Grenzkreise: Hilfen nach Aufgabe ablegen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet nach [Kritik](../../prozess/ablauf/kritik.md) (Ablage und Namen von
Hilfen, keine Prüfung rot), Tests zu Item grenzkreise:
1. [grenzen.py](../../technik/tests/akzeptanz/grenzen.py) hält fünf Aufgaben: den Typ der
   Fixture `EinheitAmZug`, Grenzen aus der Domäne, Grenzen aus dem Spielstand
   (`grenzenDerEinheitIm`, `alsZahlen`), Klickstellen (`stelleImRing`) und Handlungen
   (`ganzeEinheitAuswählen`, `vorgerücktMit`). Den Spielstand liest laut ihrem Kopf
   [dienst.py](../../technik/tests/akzeptanz/dienst.py) ([Es](../../prozess/praemissen/es.md), S).
2. `dreiAugen`, `vierAugen`, `einAuge` stehen je Testdatei neu, dreimal dasselbe
   ([Wir 3](../../prozess/praemissen/wir.md)).
3. `conftest.py` hat 11.953 von 12.000 Zeichen ([Kennzahlen](../../prozess/kennzahlen.md));
   die nächste Fixture braucht eine Teilung.

**Kosten.** Am Bildschirm nichts. Bleibt es, sucht man die Lesart des Spielstands an zwei
Orten.

**Gegenvorschlag.**
1. `grenzenDerEinheitIm` nach `dienst.py`; Handlungen zum *Vorrücken* in ein
   `vorruecken.py` neben `grenzen.py`.
2. Die Würfe einmal in `grenzen.py` neben `würfe`.
3. Bei der nächsten Fixture die der *Schlacht* in eine eigene `conftest.py` unter
   `phasen/bewegung/` verschieben.

**Stellungnahme.** Angenommen, umgesetzt bis auf den Typ der Fixture.
1. `grenzenDerEinheitIm` und `alsZahlen` (jetzt `grenzenImSpielstand`) stehen in
   [dienst.py](../../technik/tests/akzeptanz/dienst.py). Sie liefern einfache Tupel, so importiert
   `dienst.py` nichts aus `grenzen.py` und es entsteht kein Kreis; der Vergleich mit `GrenzeDerKarte`
   gilt, weil ein `NamedTuple` gleich dem Tupel ist. Die Handlungen (`ganzeEinheitAuswählen`,
   `letztesModellZurEbeneMachen`, `ebenen`, `mitJederEbene`, `wartetAufDenVorrückwurf`,
   `vorgerücktMit`) stehen in [vorruecken.py](../../technik/tests/akzeptanz/vorruecken.py).
   [grenzen.py](../../technik/tests/akzeptanz/grenzen.py) hält die erwarteten *Grenzkreise* und die
   Klickstellen, die aus deren Radien folgen; das ist eine Aufgabe. `EinheitAmZug` bleibt dort,
   solange [conftest.py](../../technik/tests/akzeptanz/conftest.py) für 10380 in Arbeit ist; es
   wandert mit der Teilung aus 3.
2. `einAuge`, `dreiAugen`, `vierAugen` stehen einmal in `grenzen.py` neben `würfe`.
3. Bei der nächsten Fixture der *Schlacht* teile ich `conftest.py` wie vorgeschlagen; heute hat sie
   10.403 Zeichen.
