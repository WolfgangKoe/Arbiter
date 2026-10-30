# Ziehen in der Bewegungsphase rechnet die Stellen doppelt

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf (neuer Code gegen [Wir 3](../../prozess/praemissen/wir.md), Nacharbeit
zu 6122), uncommittet seit `e1fb48b`.
1. [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py),
   `stellenBeimLoslassen`: `verschobeneStellen(ebene, modell, stelle)` baut die Stellen der
   ganzen *Ebene*, gelesen wird nur `verschoben[modell]`, und das ist `stelle`. Den Block
   verschiebt danach `anDerBewegungsweiteAngehalten` ein zweites Mal.
2. [anhaltenAnDerBewegungsweite.py](../../technik/arbiter/domaene/phasen/bewegung/anhaltenAnDerBewegungsweite.py):
   Der ungekürzte Fall baut mit eigener Comprehension dieselben Stellen, die
   `überBeiSchritt(schritte)` eben mit `stellenBeiSchritt(schritte)` gebaut hat.

**Kosten.** Der Leser sucht, wozu die *Ebene* vorab verschoben wird; ändert sich das
Verschieben, steht es an zwei Stellen. Fünf Zeilen Arbeit.

**Gegenvorschlag.**
1. `weg = messen.wegZwischen(ebene[modell], stelle)`, `verschoben` und der Import von
   `verschobeneStellen` in `schlachtrunden.py` entfallen.
2. `if schritte == 0: return dict(vorige)`, dann
   `if not überBeiSchritt(schritte): return stellenBeiSchritt(schritte)`.

Status: offen
