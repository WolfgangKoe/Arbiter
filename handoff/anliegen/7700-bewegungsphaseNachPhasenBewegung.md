# Das Ziehen der Bewegungsphase gehört nach phasen/bewegung/

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code zur Umsetzung von Anliegen 6122 (Architektur), `git diff e1fb48b`;
zugleich die Entscheidung zu dessen Befund 5. Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md): Es S ([Es](../../prozess/praemissen/es.md)) und
der [Grundschnitt der Domäne](../../technik/architektur/domaene.md#grundschnitt-der-domäne).
1. [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) führt
   Zug, *Schlachtrunde* und *Phase* (QUE-10) und dazu das Ziehen der *Bewegungsphase*:
   `_stellenZuBeginn`, `stellenBeimLoslassen` (Weg, Anhalten nach BEW-3, *Gründe* beim
   Ziehen), die *Sperre* gegen das Beenden. Dafür stehen zwei Wächter
   `Phase.bewegungsphase` und ein Zurücksetzen beim Eintritt in `phaseBeenden`.
2. Die Lösung aus 6122 (Docstring nennt das Ziehen) fällt mit Es 8: Ab Plan 9 entfällt jeder
   Docstring im Produktcode (Anliegen 6982). Dann nennt nur der Name `schlachtrunden` die
   Aufgabe, und er nennt das Ziehen nicht.
3. Die Tests der Items anhaltenUndAuswahl und grenzkreise rufen an der *Schlacht*
   `vorrücken`, `vorgerückt`, `vorrückwurf`, `wartetAufVorrückwurf`, `vorrückenAngeboten`,
   `vorrückenZurücknehmen`, `vorrückenZurücknehmenAngeboten`, `grenzen`, `karteAnklicken`:
   fast alles *Bewegungsphase*. Ohne Schnitt landen Zustand und Zurücksetzen davon in
   `Schlacht` (heute 6.100 Zeichen, Höchstmaß 12.000 nach
   [Kennzahlen](../../prozess/kennzahlen.md)).
4. Nebenbei: In `stellenBeimLoslassen` dient `verschobeneStellen` nur dazu,
   `verschoben[modell]` zu lesen, und das ist `stelle`.

Ich habe den Grundschnitt in [domaene.md](../../technik/architektur/domaene.md) um diesen
Fall ergänzt: Was eine *Phase* tut, steht im Paket ihres Ordners (`Bewegungsphase` neben
`Aufstellung`), die *Schlacht* reicht es weiter.

**Kosten.** Am Bildschirm nichts; die Schnittstelle der *Schlacht* für `web/` und die Tests
bleibt. Jetzt: eine Klasse mit dem heutigen Code, einige Importe. Nach den Items 3 und 4 zieht
man rund zehn Methoden samt Zustand um. Token: eine Umsetzung, gering.

**Gegenvorschlag.** Vor dem Code zu Item anhaltenUndAuswahl:
1. `class Bewegungsphase` in
   [phasen/bewegung/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py)
   hält `_stellenZuBeginn` (mit Item 4 auch *Vorrückwurf* und vorgerückte *Einheiten*) und
   bietet `stellenNachDemZiehen(ebene, gezogenes, ziel, stellen, eigene)` (Weg
   `messen.wegZwischen(ebene[gezogenes], ziel)`, Anhalten, *Gründe*, *Sperre*) und
   `gründeGegenDasBeenden(einheiten, stellen)`. Sie gibt neue *Stellen* zurück, die *Schlacht*
   übernimmt sie wie heute in `modellLoslassen`; beide teilen kein `dict` (D3).
2. Die *Schlacht* erzeugt `Bewegungsphase(self._stellen)` in `__init__` und beim Eintritt in
   die *Bewegungsphase*; das ersetzt das Zurücksetzen von `_stellenZuBeginn`. Sie behält Zug,
   *Schlachtrunde*, *Phase*, *Stellen*, *Auswahl* und die Wächter (welche *Phase*, wer *am
   Zug*, eigenes *Modell*); ihre Methoden aus Items 3 und 4 reichen an die *Bewegungsphase*
   weiter.
3. Ein Typ je *Phase* erst, wenn eine zweite *Phase* eigenes Verhalten hat; bis dahin bleibt
   der eine Wächter (Es 9: wenige Fälle als `if`).

Prüfen: `importvertrag.py` und `spiegel.py` grün, die Tests der *Schlacht* unverändert grün.

**Stellungnahme.** Angenommen und umgesetzt, wie vorgeschlagen.
