# Test der Bewegungsphase: Ablage und Erwartung

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit), `git diff 0491ad5 0015ae7`. Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md): neuer Test gegen [Es 2](../../prozess/praemissen/es.md)
und ein Test, der weniger prüft, als sein Name sagt ([Absicht 1](../../prozess/praemissen/absicht.md)).
1. [bewegungsphaseTest.py](../../technik/tests/einheit/domaene/phasen/bewegung/bewegungsphaseTest.py)
   prüft `phasen/bewegung/__init__.py`, heißt aber nach der Klasse und liegt im Paket. Das
   Gegenstück der *Aufstellung* (`phasen/aufstellen/__init__.py`) ist
   [aufstellenTest.py](../../technik/tests/einheit/domaene/phasen/aufstellenTest.py) neben
   dem Paket. Wer den Test zu `bewegung` sucht, findet ihn nicht nach Es 2.
2. `testDieBewegungsweiteZähltVomBeginnDerBewegungsphase` prüft nur
   `neue[modell].x <= bewegungsweiteDerTestmodelle`. Das gilt auch, wenn das *Modell* bei 3
   stehen bleibt oder in y abweicht. Erprobt: Die *Bewegungsphase* hält es genau bei (5, 0)
   an.

**Kosten.** Am Bildschirm nichts. Ein `mv` und eine Zeile.

**Gegenvorschlag.**
1. `mv` nach `technik/tests/einheit/domaene/phasen/bewegungTest.py`.
2. `assert neue == {modell: stelleAn(5, 0)}`.

**Stellungnahme.**
1. Angenommen. Verschoben nach `technik/tests/einheit/domaene/phasen/bewegungTest.py`.
2. Angenommen. Der Test prüft die ganze Stelle (5, 0), mit `bewegungsweiteDerTestmodelle` statt der Zahl 5.
