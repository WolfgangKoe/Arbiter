# Rücken eines Fliegers hängt an der Reihenfolge der Ebene

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit), Item fliegen, Abschnitt 2 (`git diff` auf
`phasen/bewegung/__init__.py`, `schlachtrunden.py` und zwei Testdateien). Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md): eine *Sperre* greift zu Unrecht, ein Test prüft
nicht, was sein Name sagt, [Es 6](../../prozess/praemissen/es.md). Beides an `/tmp/rev13760`
geprobt.
1. `Bewegungsphase._nachFremdenBasesGerückt` in
   [\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py) misst `zurück`
   von der *Stelle* des ersten *Modells* in `gesetzt` (`next(iter(gesetzt.values()))`) zur
   *Stelle* des gezogenen davor. Ist die Ebene die ganze *Einheit* und das gezogene nicht ihr
   erstes, ist der Weg falsch lang. Probe: Flieger A (10, 20) und B (14, 20), 1″-*Bases*,
   B auf eine fremde *Base* bei (18, 20) gezogen. B zuerst in der Ebene: rückt auf (18,98, 20),
   kein *Grund*. A zuerst: `zurück` hat Länge 0, die Suche findet nichts, Sperre
   ‚Base überdeckt‘. Dasselbe in `übergangen`.
2. `testEinFliegerFindetBeimLoslassenKeineStelleInDerBewegungsweiteUndWirdGesperrt` in
   [bewegungsphaseTest.py](../../technik/tests/einheit/domaene/phasen/bewegung/bewegungsphaseTest.py):
   Mit dem Mutanten `weiten = {}` (ohne *Bewegungsweite*) bleibt er grün. Es sperrt die
   Grenze `zurück` (Länge 2″), nicht die *Bewegungsweite*.

**Kosten.** Am Bildschirm: Zieht der Spieler bei einer Einheit mit mehreren fliegenden
*Modellen* nicht das erste, sperrt Arbiter, wo eine freie *Stelle* nah liegt. Umbau: etwa
fünf Zeilen Produktcode, ein Einheitstest dazu, ein Test umgebaut.

**Gegenvorschlag.**
1. `_nachFremdenBasesGerückt` bekommt das gezogene *Modell* und misst
   `messen.wegZwischen(gesetzt[gezogenes], davor)`; kein `next(iter(…))`. Einheitstest mit
   zwei *Modellen*, das gezogene als zweites in der Ebene.
2. Den Test so legen, dass eine freie *Stelle* innerhalb von `zurück` liegt, aber außerhalb
   der *Bewegungsweite* (etwa `stellenZuBeginn` der Phase anders als die Ebene), und mit dem
   Mutanten `weiten = {}` prüfen; sonst umbenennen nach dem, was er prüft.

**Stellungnahme.**
