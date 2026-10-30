# Vorrückwurf statt Zuschlag, ohne noqa

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf (neuer Code verletzt Lesbarkeit, [Es](../../prozess/praemissen/es.md)),
Stand 4b2f2ec, Item grenzkreise.
1. [anhaltenAnDerBewegungsweite.py](../../technik/arbiter/domaene/phasen/bewegung/anhaltenAnDerBewegungsweite.py)
   nennt den *Vorrückwurf* `zuschlag`. BEW-5.3 sagt „*Bewegungsweite* plus *Vorrückwurf*“,
   das [Glossar](../../domaene/glossar.md) führt `vorrückwurf`; „Zuschlag“ steht in keinem
   von beiden ([Wir 2](../../prozess/praemissen/wir.md)). Der Standardwert `= 0` dient nur
   den drei alten Einheitstests; der einzige Aufruf im Produkt übergibt immer einen Wert.
2. `stellenMitGründenNachDemZiehen` in
   [bewegung/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py)
   bekommt `einheit` als sechsten Parameter und schaltet dafür mit `# noqa: PLR0913` die
   Schwelle aus den [Werkzeugen](../../prozess/ablauf/werkzeuge.md) ab, als einzige Stelle
   im Produkt. `einheit` dient nur `self._vorrückwürfe.get(einheit, 0)`. Eine Ausnahme von
   einer Schwelle erteilt der Stakeholder ([Absicht 6](../../prozess/praemissen/absicht.md)).

**Kosten.** Am Bildschirm nichts. Bleibt es, liest man an der Bewegungsweite ein Wort, das die
Anforderung nicht kennt, und das erste `noqa` gegen eine Schwelle wird zum Vorbild. Umbau:
etwa 10 Zeilen in zwei Modulen; der Aufruf in
[schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) und
[bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py) wird wie vor
10abbe9.

**Gegenvorschlag.**
1. Parameter und Argument `vorrückwurf: int` heißen; den Standardwert streichen, die drei
   Aufrufe in `anhaltenAnDerBewegungsweiteTest.py` übergeben `0`.
2. `einheit` aus der Signatur nehmen; `Bewegungsphase` findet den Wurf über das gezogene
   *Modell*, etwa
   `def _vorrückwurfDes(self, gezogenes: Modell) -> int: return next((wurf for einheit, wurf in self._vorrückwürfe.items() if gezogenes in einheit.modelle), 0)`.
   Das `noqa` entfällt. Denselben Schalter nennt der Architekt in
   [8620](8620-ziehenVerlangtMehrAlsEsBraucht.md) Punkt 1 als wartend; dessen Weg, nur
   `gegner` zu übergeben, trägt nicht allein: `gründeBeimZiehen` braucht weiter `fremde`
   (auch die eigenen *Modelle* außerhalb der *Ebene*) und `eigene`.

**Stellungnahme.**
