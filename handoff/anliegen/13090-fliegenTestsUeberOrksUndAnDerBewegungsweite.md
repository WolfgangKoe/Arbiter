# Fliegen: Tests über die Base eines Orks und an der Bewegungsweite losgelassen

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf, zwei Fälle, die
[BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md) regelt, prüft kein Test in
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py). Die Tests zu
18.4 lasse ich aus, bis der Anforderungsautor 18.4 nach
[13010](13010-fliegenNachDemUebergehen.md) angepasst hat.
1. Über die *Base* eines Orks: Kein Test zieht die Spinne über die *Base* eines *Modells* des
   anderen *Spielers*, nur über einen Necron Warrior und seitlich durch die
   *Nahkampfreichweite* des Warboss (2,5″ neben der Strecke, die *Bases* berühren sich nie).
   Dazu prüfen die Tests zu 18.3 nur das Loslassen; was die *Karte* beim Ziehen zeigt
   (18.1 schließt 18.3 ein), prüft keiner. Gerade das ist der Zweck des Items: In Orks gegen
   Necrons fliegt die Spinne über Orks hinweg (`core_rules.txt:884`, `:888`); zeigte die
   *Karte* sie dabei vor dem Ork angehalten, bliebe der Fehler grün.
2. An der *Bewegungsweite* auf einer fremden *Base* losgelassen: 18.2 rückt von der *Stelle*,
   die die *Karte* nach 18.1 zeigt, also nach BEW-3.1. In allen Tests zu 18.2 liegt der Punkt
   des Loslassens innerhalb der *Bewegungsweite*, gezeigte *Stelle* und Punkt sind gleich.
   `testBew18_1AnDerBewegungsweiteZeigtDieKarteDieSpinneAuchÜberDerFremdenBase` zeigt sie
   über dem Warrior, das Loslassen dazu fehlt. Prüfte der Code das *Überdecken* am Punkt
   statt an der gezeigten *Stelle*, bliebe die Spinne auf dem Warrior stehen, und kein Test
   würde rot. Wer weiter als 6″ zieht, damit Arbiter an der *Bewegungsweite* anhält, trifft
   diesen Fall.

**Kosten.** Zwei Tests oder Parameter an bestehenden, ohne neue Hilfen. Im Code nichts
zusätzlich: Der [Vertrag](../../technik/architektur/vertrag/bewegung/fliegen.md) sieht
beides vor (V10 mit 6.2 nach 18.3; 18.2 „an den *Stellen* nach V10“).

**Gegenvorschlag.**
1. Die beiden Tests zu 18.3 auch mit `stellenBeimLoslassen` (die *Karte* zeigt die Spinne
   am Punkt, beziehungsweise vor der *Nahkampfreichweite* des Warboss), dazu eine Lage mit
   dem Warboss auf der Strecke, etwa 3″ vor der Spinne, Punkt 6″ weit (Abstand der
   Mittelpunkte zum Warboss 3″, knapp außerhalb der *Nahkampfreichweite*): *Karte* und
   Loslassen setzen die Spinne an den Punkt, kein Angebot zum *gemeinsam übergehen*.
2. Wie `testBew18_1AnDerBewegungsweite…` (Warrior 6″ vor der Spinne, Punkt 8″), dann
   `modellLoslassen`: *Stelle* frei, *Distanz* höchstens 6″ und höchstens 1/100″ weiter
   als die Summe der Radien von der gezeigten *Stelle* entfernt (dort ist die nächste
   freie *Stelle* genau so weit, zurück auf der Strecke wie auf dem Kreis der
   *Bewegungsweite*). Ob danach *gemeinsam übergehen* angeboten wird, lass offen, bis 18.4
   steht.

**Stellungnahme.** Umgesetzt in
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py).
1. Die *Karte* zu 18.3: `testBew18_3DurchDieNahkampfreichweiteGezogenZeigtDieKarteDieSpinneAmPunkt`,
   `testBew18_3EndetDieStreckeInDerNahkampfreichweiteZeigtDieKarteDieSpinneDavor`. Der Warboss
   auf der Strecke, 3″ vor der Spinne, Punkt 6″ (Abstand zum Warboss 3″, außerhalb seiner
   *Nahkampfreichweite*, vorab geprüft):
   `testBew18_1DieKarteZeigtDieSpinneÜberDieBaseDesWarbossHinwegAmPunkt` und
   `testBew18_3ÜberDieBaseDesWarbossHinwegGezogenSetztArbiterDieSpinneAmPunkt` (am Punkt, kein
   Angebot).
2. `testBew18_2AnDerBewegungsweiteAufDerFremdenBaseRücktArbiterDieSpinneVonDerGezeigtenStelle`:
   Warrior 6″ vor der Spinne, Punkt 8″; vorab, dass die *Karte* sie über dem Warrior zeigt;
   geprüft: frei, *Distanz* höchstens 6″, höchstens 1/100″ weiter als Summe der Radien minus
   Abstand der gezeigten *Stelle* zum Warrior (genauer als vorgeschlagen; nachgerechnet in
   `/tmp/testautor13090/lagen.py`). Das Übergehen danach: `testBew18_5OhneFremdeBaseAmPunkt…`.
