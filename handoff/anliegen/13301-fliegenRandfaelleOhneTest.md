# Fliegen: zwei Fälle der Kriterien ohne Test

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** In [fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py)
fehlen zwei Fälle, die [BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md)
regelt; beide abseits des Happy Path, darum wartend:
1. BEW-18.3 misst am „Ende der Strecke nach 6.3 ohne 6.2“. Jeder 18.3-Test endet vor der
   *Bewegungsweite* und im *Spielfeld*, das Ende ist also stets der Punkt. Hält die
   *Spielfeldkante* früher an (6.1) und ist die Spinne dort in *Nahkampfreichweite*, der Punkt
   jenseits der Kante aber nicht, muss 6.2 davor anhalten. Code, der am Punkt misst, ließe
   sie in der *Nahkampfreichweite* stehen und bliebe grün; genau diesen Fall führte
   Anliegen 12985 F4 ein.
2. BEW-18.2 rückt nur, wo BEW-3.1 nicht anhielte; nach BEW-5.3 ist das *Bewegungsweite* plus
   *Vorrückwurf*. Kein Test rückt eine *vorgerückte* Spinne über 6″ hinaus.

**Kosten.** Je ein Test an `Schlacht`. Ohne sie kann die Spinne an der Kante regelwidrig in
*Nahkampfreichweite* enden oder nach dem *Vorrücken* zu kurz rücken, unbemerkt bis zum Spiel.

**Gegenvorschlag.**
1. Warboss nahe der *Spielfeldkante*, Spinne über die Kante hinaus an ihm vorbei gezogen,
   Punkt außerhalb, Halt nach 6.1 in seiner *Nahkampfreichweite*: `hältVorDerNahkampfreichweite`.
2. Spinne *vorgerückt*, auf einem Warrior hinter 6″ losgelassen: *Stelle* frei, *Distanz*
   über 6″, höchstens *Bewegungsweite* plus *Vorrückwurf*.

**Stellungnahme.**
