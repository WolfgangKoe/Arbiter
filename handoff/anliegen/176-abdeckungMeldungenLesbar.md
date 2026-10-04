# Meldungen der Abdeckung lesbar

176 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
Kritik am Code zu Commit `f87a822`, `prozess/pruefungen/abdeckung.py`. Was
[175](175-abdeckungKleinigkeiten.md) nennt, wiederhole ich nicht.

**Befund.**
1. Die grüne Meldung des Hooks `abdeckungPruefskripte` gibt das Tupel roh aus:
   `ausreichend (Abdeckung(zeilen=98.20659971305595, zweige=96.69260700389106))`. Die rote
   Meldung nutzt dafür `prozentText`, die grüne nicht.
2. Ein falscher Pfad in `quelle` (ausprobiert: `prozess/pruefungn`) endet in
   `CalledProcessError … coverage json … exit status 1`. stderr ist abgefangen und fehlt in
   der Meldung; dass „No data was collected“ der Grund ist, sieht niemand. Die Prüfung ist rot,
   nicht falsch grün; nur die Ursache bleibt verborgen.

**Kosten.** 1: Der Stakeholder liest bei jedem Commit an den Prüfskripten eine Zeile
Python-Interna statt zweier Zahlen. 2: Wer `technik/arbiter` umbenennt, sucht die Ursache im
Werkzeug statt im Pfad. Je wenige Minuten.

**Gegenvorschlag.**
1. Grün wie rot formatieren, etwa `Abdeckung von prozess/pruefungen: Zeilen 98.2 %, Zweige
   96.6 %`; dieselbe Funktion baut beide Meldungen.
2. Den Lauf von `coverage json` mit `check=False` und, wenn er scheitert, eine Meldung mit
   seinem stderr, wie `unbenutzterCode` es für vulture tut. Scheiter-Test: ein falscher
   `quelle`-Pfad nennt den Pfad oder die Ausgabe von coverage.

**Stellungnahme (Regelumsetzer).** Umgesetzt wie vorgeschlagen; Scheiter-Tests in `abdeckungTest.py`.
