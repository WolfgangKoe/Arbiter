# Ziehen verlangt mehr, als es braucht

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet (Ablage und Schnittstelle von Hilfsfunktionen, keine Prüfung rot),
Änderung 10abbe9..4b2f2ec zu Item grenzkreise.
1. `Bewegungsphase.stellenMitGründenNachDemZiehen` in
   [bewegung/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py)
   hat mit `einheit` sechs Parameter und schweigt Ruff mit `# noqa: PLR0913`. Zwei davon,
   `stellen` und `eigene`, dienen nur dazu, die Stellen der Gegner auszusondern; das kann
   `Schlacht`, die den Gegner schon kennt (`gegnerVon` in `grenzen`). Eine Schnittstelle
   verlangt nur, was ihr Nutzer braucht ([Es](../../prozess/praemissen/es.md), I); der
   Schalter verdeckt, dass sie wächst.
2. `kleinsterWurfAn` in
   [grenzkreise.py](../../technik/arbiter/domaene/phasen/bewegung/grenzkreise.py) nimmt den
   ersten Wurf in der Reihenfolge von `würfe`, nicht den kleinsten; richtig ist das nur,
   weil `möglicheWürfe` aufsteigt. Der Name verspricht, was die Reihenfolge des Aufrufers
   hält.

**Kosten.** Am Bildschirm nichts. Bleibt 1, kommt der nächste Parameter wieder mit einem
`noqa`. Bleibt 2, liefert ein Aufruf mit anderer Reihenfolge
einen zu großen *Vorrückwurf*, ohne dass ein Test es merkt. Änderung: etwa zehn Zeilen in
`Bewegungsphase`, `Schlacht` und zwei Einheitstests in `bewegungTest.py`.

**Gegenvorschlag.**
1. `stellenMitGründenNachDemZiehen(einheit, ebene, gezogenes, ziel, gegner)` mit
   `gegner: Mapping[Modell, Stelle]`; `Schlacht` sondert sie aus, das `noqa` entfällt.
2. `min((grenze.wurf for grenze in würfe if enthält(grenze.kreise, stelle)), default=None)`.

**Stellungnahme.** Angenommen, mit einer Abweichung bei 1. `stellenMitGründenNachDemZiehen`
nimmt `ebene, gezogenes, ziel, stellen, gegner` (fünf Parameter, `noqa` entfällt); `Schlacht`
sondert die `gegner` aus, die eigenen Modelle folgen aus `stellen` ohne `gegner`. Die
`einheit` braucht es nicht, weil der Wurf über `einheitDes` (siehe 8740) gefunden wird. 2:
`kleinsterWurfAn` nimmt `min` über die Würfe der Kreise, die die Stelle enthalten.
