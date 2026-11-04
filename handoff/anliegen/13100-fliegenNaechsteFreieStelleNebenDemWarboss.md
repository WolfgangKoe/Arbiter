# Fliegen: Der Test neben dem Warboss erwartet eine Stelle, die nicht die nächste freie ist

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf: Ein Test prüft sein Kriterium nicht ganz. In
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py),
`testBew18_2NebenEinemModellDesAnderenSpielersRücktArbiterDieSpinneNichtInDieNahkampfreichweite`,
nimmt der Test die *Stelle* südlich des Warriors als nächste freie (1,814″ vom Punkt). Näher
liegt der Schnitt des Kreises, auf dem die Spinne den Warrior berührt, mit dem Rand der
*Nahkampfreichweite* des Warboss: 1,748″ (nachgerechnet in `/tmp/arch13021/naechste.py`,
Bases 60, 32, 40 mm). BEW-18.2 verlangt höchstens 1/100″ weiter, also 1,758″; der Test lässt
1,824″ zu. Grün würde damit auch ein Code, der die *Nahkampfreichweite* nur aussortiert, statt
ihren Rand als Kandidaten zu suchen ([Vertrag](../../technik/architektur/vertrag/bewegung/fliegen.md),
`ränder`, „bei *Nahkampfreichweite* plus 1″“); genau diesen Teil prüft sonst kein Test.

Dazu Lesbarkeit im selben Zug, weil dieselbe Rechnung schon einmal im Test steht:
`testBew18_2AnDerBewegungsweiteRücktArbiterDieSpinneNichtÜberSieHinaus` rechnet den Schnitt
zweier Kreise ausgeschrieben, mit der 5 für den Abstand des Warriors viermal als Zahl
(`Fraction(-5)`, `5**2`, `2 * 5`, `- 5 -`); `testBew18_2AnDerSpielfeldkante…` setzt den
Warrior an `Fraction(43)` statt an einen Namen für „1″ vor der *Spielfeldkante*“.

**Kosten.** Testautor, etwa eine Viertelstunde. Im Code nichts.

**Gegenvorschlag.**
1. Ein Helfer in der Testdatei: der Schnittpunkt zweier Kreise (Mittelpunkte, Radien), gerechnet
   wie in `/tmp/arch13021/naechste.py`, Quadratwurzel aufgerundet wie `wurzelAufgerundet`.
2. Neben dem Warboss: Erwartet ist der Schnitt des Kreises um den Warrior (Radius
   `summeDerRadien(spinne, warrior)`) mit dem um den Warboss (Radius
   `summeDerRadien(spinne, boss) + 1`) auf der Seite des Punkts; `zurFreienStelle` ist der Weg
   dorthin. Die Vorbedingung `außerhalbDerNahkampfreichweite(südlichDesWarriors, …)` entfällt.
3. An der *Bewegungsweite*: derselbe Helper statt der ausgeschriebenen Formel, der Abstand des
   Warriors mit Namen (`abstandDesWarriors = Fraction(5)`); an der *Spielfeldkante*
   `breiteDesSpielfelds - 1`.

**Stellungnahme.** Alle drei umgesetzt in
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py).
1. `Kreis`, `schnittpunkte` und `wegZumNächstenSchnitt` (kürzerer Weg zu den beiden
   Schnittpunkten, Wurzel aufgerundet wie `wurzelAufgerundet`), dazu
   `randDerNahkampfreichweite` für den Kreis um ein *Modell* mit Summe der Radien plus 1″.
2. Neben dem Warboss: `zurFreienStelle` ist der Weg zum Schnitt der Kreise um Warrior und
   Warboss; die Vorbedingung südlich des Warriors ist gestrichen. Nachgerechnet 1,7475″, Raster
   1,7489″ (`/tmp/testautor13090/lagen.py`).
3. An der *Bewegungsweite*: `abstandDesWarriors = Fraction(5)` und derselbe Helfer; an der
   *Spielfeldkante* `breiteDesSpielfelds - 1`. Dieselben Helfer tragen die neuen Tests zu
   BEW-18.5.
