# Angebot zum Vorrücken an zwei Stellen

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: neuer Code teilt eine Regel der *Bewegungsphase* zwischen ihr und der
*Schlacht* ([Grundschnitt](../../technik/architektur/domaene.md#grundschnitt-der-domäne):
Die *Schlacht* reicht weiter, was eine *Phase* tut). Seit 4f5dc07 entscheidet
`Schlacht.vorrückenAngeboten` in
[schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) BEW-22.1
selbst und importiert dafür `einModellInNahkampfreichweite` aus `phasen/bewegung/`; die
gleichnamige `Bewegungsphase.vorrückenAngeboten` in
[bewegung/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py) kennt
nur BEW-5.1 und schützt damit `vorrückenBeginnen`. Folge: Zwei Abfragen gleichen Namens
sagen Verschiedenes; wer nur die `Bewegungsphase` liest, glaubt ihr. Der Einheitstest
`testEineEinheitDieNichtVorrückteWirdVorrückenAngeboten` belegt ein Angebot, das am
Bildschirm fehlen kann. Am Bildschirm ändert sich nichts, `Schlacht.vorrücken` prüft
richtig. Im selben Commit steht es richtig: `einheitZurücksetzenAngeboten(einheit, stellen)`
entscheidet BEW-24.1 ganz in der `Bewegungsphase`, die `Schlacht` reicht nur weiter.
Mein Vertrag (V20, „bietet `Schlacht` … nicht an“) lud dazu ein; ich habe ihn in
[grenzkreise.md](../../technik/architektur/vertrag/bewegung/grenzkreise.md) geschärft.

**Kosten.** Implementierer, etwa 20 Minuten: zwei Methoden, ein Import, fünf Aufrufe in
[bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py). Die Datei der
`Bewegungsphase` wächst um rund 150 Zeichen auf etwa 10.700 von 12.000
([Höchstmaß](../../prozess/kennzahlen.md#höchstmaße)), `schlachtrunden.py` schrumpft.

**Gegenvorschlag.** Wie bei `einheitZurücksetzenAngeboten`:
`Bewegungsphase.vorrückenAngeboten(einheit, stellen, gegner)` prüft BEW-5.1 und BEW-22.1,
`vorrückenBeginnen` nimmt dieselben Parameter und prüft damit; `Schlacht.vorrückenAngeboten`
reicht `self._stellen` und `self._stellenDesGegners()` weiter und importiert
`keinVorrueckenAusDerNahkampfreichweite` nicht mehr. Der Einheitstest bekommt einen Fall mit
einem *Modell* in *Nahkampfreichweite*.

**Stellungnahme.** Angenommen und umgesetzt wie vorgeschlagen:
`Bewegungsphase.vorrückenAngeboten(einheit, stellen, gegner)` prüft BEW-5.1 und BEW-22.1,
`vorrückenBeginnen` nimmt dieselben Parameter; `Schlacht.vorrückenAngeboten` reicht nur
weiter und importiert die Regel nicht mehr. Neuer Einheitstest mit einem *Modell* in
*Nahkampfreichweite*, die übrigen Aufrufe in bewegungTest.py angepasst. Bewegungs- und
Einheitstests grün bis auf die bekannt roten zu Fliegen.
