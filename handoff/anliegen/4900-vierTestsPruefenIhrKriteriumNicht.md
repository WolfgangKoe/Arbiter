# Vier Tests prüfen ihr Kriterium nicht

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: ein Test prüft sein Kriterium nicht). Jedes Mal wird eine falsche
Umsetzung grün.
1. QUE-10.3 und 10.4 ([schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py)):
   Den *ersten Zug* hat immer Spieler 1 (`schlachtInDerKommandophase`). Eine Umsetzung, die
   die neue *Schlachtrunde* und das Ende der *Schlacht* am ersten *Spieler* der *Ausgangslage*
   festmacht statt am *ersten Zug*, besteht alle Tests. Das Kriterium regelt genau das: „hat
   er den *ersten Zug*“. Im Happy Path (Plan 8, Schritt 1) kann jeder den Roll-off gewinnen.
2. BEW-2.4 (`testBew2_4…`, [sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py)):
   Mit dem Weg `(2, 3)` überdeckt keine neue *Stelle* eines Boyz die vorige eines anderen;
   der waagrechte Teil 2 ist größer als der Durchmesser 32 mm (1,26 Zoll; nachgerechnet:
   0 Überdeckungen, mit `(1, 2)` 17, mit `(0, 3)` 15). Der Test wird also auch grün, wenn
   QUE-1.2 die eigenen *Modelle* an ihrer vorigen *Stelle* mitzählt.
3. BEW-2.1, *Distanz*: Jede Grenze bei *B* liegt auf einer Achse; die schrägen Wege bleiben
   weit unter *B*. Eine *Distanz* als Summe |x| + |y| oder als größter Teil besteht jeden Test.
   Plan 8 nennt gerade das genaue Messen der *Distanz* als das einzig Neue im Item 3; das
   Glossar sagt „Summe der geraden Strecken“.
4. BEW-2.3, „nennt jeden *Grund*“: Jeder Test erwartet genau einen *Grund* oder prüft nur
   „in“ (wegen Anliegen 4860). Eine Umsetzung, die mit dem ersten *Grund* abbricht, besteht.

**Kosten.** Bleibt es so, kann die Abnahme nicht zeigen, dass Arbiter den *ersten Zug* des
zweiten *Spielers*, eine schräge *Normale Bewegung* und zwei *Gründe* zugleich richtig
behandelt. Nachbessern kostet je Punkt wenige Zeilen mit vorhandenen Fixtures und Handgriffen.

**Gegenvorschlag.**
1. Die Tests zu QUE-10.3 und 10.4 über `spielerMitDemErstenZug` laufen lassen (wie QUE-9.2):
   eine Fixture, die ihm den *ersten Zug* gibt, und „der andere *Spieler*“ statt `spielerZwei`.
2. In `testBew2_4…` den Weg `nachNorden(dreiZoll)` oder `(1, 2)` nehmen; beide bleiben unter
   *B*, und der Warboss liegt 2,5 Zoll daneben, also ohne fremde *Base* auf der Strecke.
3. Die zwei Grenzfälle von BEW-2.1 (genau *B*, *B* + `millionstel`) zusätzlich schräg mit
   `schrägOhneWurzel` aus `handgriffe.py`, etwa der Warboss um `(3, 4)`.
4. Ein Test zu BEW-2.3 mit zwei *Gründen*, die Anliegen 4860 nicht berühren: das erste Boyz
   (nicht *ausgewählt*) um `nachOsten(fünfZoll + millionstel)`; es zieht über den Warboss und
   endet 2,5 Zoll neben ihm, also `{Grund.weiterAlsB, Grund.überEineBase}` und jedes *Modell*
   wie davor.

Die Teile am Bildschirm (QUE-9.1, QUE-10.1, „Arbiter zeigt es“ in 10.4, BEW-1.4, „bis zur
nächsten Handlung“ in BEW-2.3, der Klick in AUF-20.6) prüfe ich, wenn sie nach dem Vertrag
stehen.

**Stellungnahme.** Alle vier Punkte angenommen und umgesetzt.
1. [schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py):
   QUE-10.3 und 10.4 laufen über `spielerMitDemErstenZug` (Fixture `schlachtMitErstemZug`);
   „der andere Spieler“ ist die Fixture `andererSpieler`. QUE-10.2 und 10.5 bleiben bei
   Spieler 1, sie hängen nicht an der Wahl.
2. [sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py):
   `testBew2_4…` zieht um `schrägOhneHindernis` (1, 2), jetzt in
   [schlacht.py](../../technik/tests/akzeptanz/schlacht.py), wie BEW-1.1.
3. BEW-2.1: zwei neue Tests, schräg genau *B* (Warboss um 3, 4) und *B* + `millionstel`,
   mit `schrägOhneWurzel`. Summe |x| + |y| scheitert am ersten, der größte Teil am zweiten.
4. 4860 geprüft: `testBew2_3SetztEinModellAufEineFremdeBase…` erwartet
   `{baseÜberdeckt, überEineBase}`. Neu `testBew2_3ZiehtEinModellÜberEineBaseUndWeiterAlsB…`
   mit `{weiterAlsB, überEineBase}` und unveränderten *Modellen* beider *Einheiten*.
