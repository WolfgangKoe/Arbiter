# Fliegen: Kein Test zum Vorrückwurf beim Rücken und zur Spielfeldkante als Ende der Strecke

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf ([Kritik](../../prozess/ablauf/kritik.md)): Zwei Tests prüfen ihr Kriterium
nur zum Teil. Kritik am Code zu Item fliegen, Abschnitt B (`3c78499`), Probe an einer Kopie in
`/tmp/rev13861`. Der Produktcode ist in beiden Fällen richtig; nur fängt kein Test einen Fehler
darin.
1. BEW-18.2 lässt beim Rücken BEW-3.1 gelten, nach BEW-5.3 also *Bewegungsweite* plus
   *Vorrückwurf*. Kein Test zu [fliegen](../../domaene/anforderungen/phasen/bewegung/fliegen.md)
   zieht einen vorgerückten Flieger. Ohne den *Vorrückwurf* in `Bewegungsphase._weitenDer`
   (`__init__.py` Zeile 120) bleiben alle 696 Tests unter `akzeptanz/phasen/bewegung`,
   `einheit/domaene/phasen` und `einheit/web` grün. Am Bildschirm wäre das so: Ein Flieger mit
   *Bewegungsweite* 5″ und *Vorrückwurf* 3 wird 7,6″ weit auf einer fremden *Base* losgelassen.
   Richtig steht er danach 8″ vom Anfang (`/tmp/rev13861_probe.py`: x 17,952), mit dem Fehler
   springt er auf 5″ zurück (x 15).
2. BEW-18.3 nennt das Ende der Strecke nach BEW-6.3. Geprüft ist es an der *Bewegungsweite*
   (`testBew18_3EndetDieBewegungsweiteInDerNahkampfreichweite…`), nicht an der
   *Spielfeldkante*. Mit `bewegungsweite` statt `min(bewegungsweite, spielfeldkante)` in
   `Fliegen.gezeigt` (`fliegen.py` Zeile 44) bleiben die 55 Tests der Dateien zu Fliegen grün;
   den breiteren Lauf aus 1 habe ich dafür nicht gemacht. Am Bildschirm wäre das so
   (`/tmp/rev13861_probe2.py`): Die Strecke endet an der *Spielfeldkante* in
   *Nahkampfreichweite*, hinter der Kante läge sie wieder außerhalb. Richtig hält der Flieger
   davor an, außerhalb und ohne *Grund*. Mit dem Fehler steht er an der Kante darin, und die
   *Sperre* ‚Nahkampfreichweite‘ steht da.

**Kosten.** Bleibt es so, kann der Fehler unbemerkt entstehen, und das sind genau die grünen
Tests, die nichts prüfen ([Absicht 1](../../prozess/praemissen/absicht.md)). Zeile 120 zählt
außerdem zu den geänderten Zeilen der Mutationsprüfung ([DoD](../../prozess/ablauf/dod.md)). Zwei
Tests in einer Datei, ohne Produktcode: ein Testautor-Lauf.

**Gegenvorschlag.** In
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py):
1. `testBew18_2NachDemVorrückenRücktArbiterDieSpinne…`: nach dem Muster von
   `testBew18_2AnDerBewegungsweiteRücktArbiterDieSpinneNichtÜberSieHinaus`, die Spinne vorgerückt,
   der Warrior hinter ihrer *Bewegungsweite*, aber in *Bewegungsweite* plus *Vorrückwurf*.
   Erwartet: frei, *Distanz* höchstens beides zusammen, und höchstens 1/100″ weiter als die
   nächste freie *Stelle* (`wegZumNächstenSchnitt` mit dem größeren Kreis).
2. `testBew18_3EndetDieStreckeAnDerSpielfeldkanteInDerNahkampfreichweite…`: die Spinne zieht
   flach über die *Spielfeldkante* hinaus. Das *Modell* des anderen *Spielers* steht so, dass
   die letzte *Stelle* an der Kante in seiner *Nahkampfreichweite* liegt, die Anfangsstelle und
   der Punkt nach der *Bewegungsweite* aber außerhalb. Erwartet: außerhalb, auf der Strecke.

Beide Tests sind sofort grün. Beleg, dass sie prüfen: An einer Kopie mit den beiden Änderungen
oben werden sie rot.

**Stellungnahme.**
