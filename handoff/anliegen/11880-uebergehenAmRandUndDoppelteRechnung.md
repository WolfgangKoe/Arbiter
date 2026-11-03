# Übergehen am Rand ohne Grund, doppelte Rechnung beim Loslassen

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet (Kritik: Randfall abseits des Happy Path, Form von Hilfsfunktionen, keine
Prüfung rot), uncommitteter Stand zu Item anhaltenUebergehen.
1. BEW-25 am Rand: Steht ein *Modell* nach dem Übergehen über seiner *Bewegungsweite* an der
   Spielfeldkante und wird weiter nach außen gezogen, bietet Arbiter *gemeinsam übergehen*
   an (Anteile 0, 0, 1). Der Klick lässt das *Modell* stehen und trägt einen *Eintrag* ohne
   *Grund* ins *Protokoll* ein; BEW-8.5 verlangt ‚Bewegungsweite‘. Ursache in
   `Bewegungsphase.übergangen`
   ([\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py)): Die *Gründe*
   rechnet es auf `kurz`, das die Kante auf (0, 0) kürzt, und dort liefert
   `anteilBisZurBewegungsweite` 1. Erprobt mit `Bewegungsphase` allein (Start x 30,
   Stelle x 55, Ziel x 70, *Spielfeld* 60″): `angehalten=frozenset()`.
   [V18](../../technik/architektur/vertrag/schlacht/uebergehen.md) sagt anders: Das Angebot
   merkt die *Stelle* des gezogenen vor dem Ziehen, die *Gründe* gelten für den Weg von dort
   zur neuen *Stelle*.
2. [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py),
   `gemeinsamÜbergehen`: `or spieler is None` ist tot, ohne *Spieler* am Zug gibt es kein
   Angebot (gleichwertiger Mutant). `_stellenDesGegners` trägt `spieler is None or` nur, weil
   es vor dieser Prüfung läuft; ohne *Spieler* nennt es alle *Modelle* „Gegner“.
3. Ebenda, `modellLoslassen`: `_ebeneDes`, `_stellenDesGegners` und `Bewegungsphase._anteile`
   laufen je zweimal mit denselben Werten, einmal in `_stellenMitGründen`, einmal für
   `angebotNachDemZiehen`; jeder Anteil sucht Schritt für Schritt über alle *Modelle* und
   Gegner.
4. [uebergehenBeimZiehen.py](../../technik/arbiter/domaene/phasen/bewegung/uebergehenBeimZiehen.py),
   `gründeBeimÜbergehen`: Die Schleife über `befundeDesSetzens` wiederholt die aus
   `gründeBeimZiehen` ([normaleBewegung.py](../../technik/arbiter/domaene/phasen/bewegung/normaleBewegung.py)).

**Kosten.** 1: am Bildschirm ein Knopf, der nichts bewegt, und ein *Eintrag* ohne *Grund*
(selten, nur nach einem Übergehen am Rand). 2: ein Überlebender im Mutationslauf und ein
Leser, der eine Lage ohne *Spieler* sucht, die es nicht gibt. 3: doppelte Rechenzeit je
Loslassen, zwei Aufrufe, die zusammen stimmen müssen. 4: zwei Stellen für eine Regel. Je
Punkt wenige Zeilen.

**Gegenvorschlag.**
1. Wie V18: `Angebot` merkt die *Stelle* des gezogenen vor dem Ziehen, `übergangen` rechnet
   die `Anteile` auf dem Weg von dort zur neuen *Stelle*; ein Einheitstest mit dem Fall oben.
2. In `gemeinsamÜbergehen` zuerst `if spieler is None: return`, `_stellenDesGegners(spieler)`
   mit dem *Spieler* als Parameter, ohne `spieler is None or`; dann nur
   `if übergangen is None: return`.
3. `stellenMitGründenNachDemZiehen` gibt die `Anteile` mit zurück (oder die
   *Bewegungsphase* bildet das Angebot dort), `Schlacht` holt *Ebene* und Gegner einmal.
4. Eine gemeinsame Hilfe in `querschnitt/setzen.py`, die aus `befundeDesSetzens` die
   zutreffenden *Gründe* bildet; beide Funktionen rufen sie.

**Stellungnahme.**
