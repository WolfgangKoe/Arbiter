# Gründe beim Setzen und Ziehen wieder als Tabelle (D4)

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: neuer Code verletzt Architektur), Diff `7684034..d527459`.
[Architektur D4](../../technik/architektur/domaene.md) verlangt: Gründe, die zusammen gelten,
stehen in einer Tabelle Grund → Befund, ein neuer Grund ist eine Zeile, und nennt
`sperrenBeimSetzen.py` als Beispiel. Seit `gründeDesSetzens` QUE-1 teilt (gut, Wir 3), kommt
der Grund der Phase als Zweig dazu:
1. [sperrenBeimSetzen.py](../../technik/arbiter/domaene/phasen/aufstellen/sperrenBeimSetzen.py),
   Z. 20 bis 23: `if not messen.ganzIn(...): gründe.add(Grund.nichtGanzInDerZone)`; vorher
   stand er in der Tabelle.
2. [sperrenBeimZiehen.py](../../technik/arbiter/domaene/phasen/bewegung/sperrenBeimZiehen.py),
   Z. 30 bis 33: `if _überEineBase(...): gründe.add(Grund.überEineBase)`.

`formregeln/gruendeTabellen.py` ist grün, weil sie nur Wächter gegen Tabellen prüft.

**Kosten.** Der nächste Grund der Bewegung (Etappe 2: über die Kante, *Nahkampfreichweite*
beim Advance) wird ein weiterer Zweig in `gründeBeimZiehen`; die Tabelle, die D4 als einzige
Stelle je Anforderung verspricht, gibt es dann in zwei Modulen nicht mehr.

**Gegenvorschlag.** `querschnitt` liefert die Befunde statt der Gründe, jede Phase ergänzt
ihre Zeile und sammelt ein:
```python
befunde = {
    **befundeDesSetzens(modell, stelle, stellen, eigene),
    Grund.nichtGanzInDerZone: not messen.ganzIn(modell.base, stelle, *zone),
}
return {grund for grund, trifft in befunde.items() if trifft}
```
in `gründeBeimZiehen` ebenso mit `Grund.überEineBase: _überEineBase(...)` je Modell. Den
Namen `befundeDesSetzens` entscheidest du.

**Stellungnahme.** Angenommen, wie vorgeschlagen. `gründeDesSetzens` heißt jetzt `befundeDesSetzens` und liefert je Grund nach QUE-1, ob er gilt ([querschnitt](../../technik/arbiter/domaene/querschnitt/__init__.py)). `gründeGegenDieStelle` ([sperrenBeimSetzen.py](../../technik/arbiter/domaene/phasen/aufstellen/sperrenBeimSetzen.py)) ergänzt die Zeile `nichtGanzInDerZone`, `gründeBeimZiehen` ([sperrenBeimZiehen.py](../../technik/arbiter/domaene/phasen/bewegung/sperrenBeimZiehen.py)) die Zeile `überEineBase`; beide sammeln die zutreffenden ein. Alle 841 Tests in technik/tests, die Formregeln und SonarLint sind grün.
