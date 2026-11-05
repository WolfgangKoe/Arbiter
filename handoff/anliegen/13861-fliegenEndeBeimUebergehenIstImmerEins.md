# Fliegen: Das Ende beim Übergehen ist immer die ganze Strecke

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet ([Kritik](../../prozess/ablauf/kritik.md)): keine Prüfung rot, am Bildschirm
kein Unterschied. Vereinfachung in
[\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py), Kritik am Code zu
Item fliegen, Abschnitt A (`f7f8b57`). `_nurSpielfeldkante` gibt beim Übergehen den Anteil der
*Spielfeldkante* auf dem gegangenen Weg zurück, und der ist immer 1: Der Weg ist schon an der
*Spielfeldkante* gekürzt, und die *Stelle* nach dem Rücken liegt *ganz in* dem *Spielfeld*.
Probe auf einer Kopie: Mit `return Fraction(1)` bleiben alle 569 Tests unter `phasen/bewegung`
(Akzeptanz und Einheit) grün. Der Parameter `endeDerStrecke` mit dem Typ `EndeDerStrecke` kennt
damit drei Zustände (`None`, `min`, `_nurSpielfeldkante`), wo es zwei und eine Zahl auch täten.

**Kosten.** Bleibt es so, trägt Abschnitt B einen Typalias und eine Hilfsfunktion mit, und die
Mutationsprüfung ([DoD](../../prozess/ablauf/dod.md)) meldet einen gleichwertigen Mutanten mit
Begründung. Der Wechsel kostet nichts extra, wenn er mit dem Umbau kommt.

**Gegenvorschlag.** Im Umbau nach [13740](13740-fliegenAlsTypUndZweiFehler.md), Punkt 1: Der Anteil
von 6.2 bekommt sein Ende als Zahl, beim Übergehen `Fraction(1)`, beim Ziehen der kleinere
Anteil von 3.1 und 6.1. `EndeDerStrecke` und `_nurSpielfeldkante` entfallen. Der Vertrag bleibt
richtig: Ende 6.1 ist auf dem gekürzten Weg die ganze Strecke.

**Stellungnahme.** Angenommen und umgesetzt im Umbau von 13740: `Fliegen._anteile` nimmt das
Ende als `Fraction`, beim Übergehen `Fraction(1)`, beim Ziehen den kleineren Anteil von 3.1 und
6.1. `EndeDerStrecke` und `_nurSpielfeldkante` entfallen.
