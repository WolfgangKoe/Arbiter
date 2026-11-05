# Fliegen: Absatz „Prüft“ zu BEW-18.7 nennt drei Fälle der Tests nicht

Form: Kritik
Von: Testautor
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält den Happy Path nicht auf. Der [Vertrag Fliegen](../../technik/architektur/vertrag/bewegung/fliegen.md),
Absatz „Prüft“, nennt für 18.7 den Punkt hinter der Mitte eines Warriors jenseits der
*Bewegungsweite* (*Distanz* über 6″, ‚Bewegungsweite‘) und „in der *Nahkampfreichweite* des
Warboss: außerhalb“. Die Tests in
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py) prüfen dazu:
1. Ohne fremde *Base* am Punkt *setzt* Arbiter die Spinne nach dem Übergehen dorthin, der
   *Eintrag* nennt ‚Bewegungsweite‘ (zuvor 18.5, unverändert übernommen).
2. Punkt vor der Mitte des Warriors: Arbiter rückt die Spinne zurück in die
   *Bewegungsweite*, der *Eintrag* nennt keinen *Grund*. Warum: „BEW-8.5 an der *Stelle*
   danach“; nur so zeigt ein Test, dass der *Eintrag* nach dem Rücken entsteht.
3. „Nahkampfreichweite“ zweifach: nur die *Bewegungsweite* übergangen, der Warboss hinter dem
   Warrior; und die *Nahkampfreichweite* übergangen (6.2 hielt an, Anliegen 13010 F3 A). Im
   zweiten Fall nennt der *Eintrag* nach dem Rücken keinen *Grund*.

**Kosten.** Zwei Halbsätze im Absatz „Prüft“; im Code nichts.

**Gegenvorschlag.** „Prüft“ nennt für 18.7 zusätzlich: ohne fremde *Base* am Punkt; vor der
Mitte zurück in die *Bewegungsweite*, *Eintrag* ohne *Grund*; die *Nahkampfreichweite* auch
übergangen, *Eintrag* ohne *Grund*. Hältst du einen Fall für überzählig, nenne das Kriterium,
das ihn schon abdeckt.

**Stellungnahme.** Angenommen, keiner ist überzählig: Fall 1 zeigt, dass ohne fremde *Base*
nichts rückt; 2 und 3 belegen „BEW-8.5 an der *Stelle* danach“, das sonst kein Test trifft.
Im [Vertrag Fliegen](../../technik/architektur/vertrag/bewegung/fliegen.md), Absatz „Prüft“,
nennt 18.7 jetzt alle sechs Tests; Platz schaffte die gekürzte Begründung zum Warboss.
