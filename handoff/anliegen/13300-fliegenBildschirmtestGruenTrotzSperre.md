# Fliegen: Der Test am Bildschirm ist auch grün, wenn Arbiter sperrt

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** In [fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py)
prüft `testBew18_2DieKarteZeigtDieSpinneBeimHaltenÜberDerBaseUndDanachAnIhrerStelle` nach dem
Loslassen nur, dass die Spinne frei steht und die *Karte* sie an ihrer *Stelle* im Spielstand
zeigt. Sperrt QUE-1.2 beim Loslassen, wie heute, bleibt die Spinne an der *Stelle* vor dem
Ziehen (`schlachtrunden.py:133`): auch die ist frei und gezeigt, der Test bliebe grün. Am
Bildschirm sähe der Stakeholder die Spinne zurückspringen statt neben den Warrior rücken, und
kein Test am Dienst oder an der Seite fängt das; BEW-18.2 prüfen nur die Tests an `Schlacht`.
Das Kriterium (rücken an die nächste freie *Stelle*) prüft dieser Test also nicht, obwohl
„Am Bildschirm“ von BEW-18 genau diesen Handgriff nennt.

**Kosten.** Eine Zeile im Test; ohne sie kann die Umsetzung am Bildschirm falsch sein und
die Abnahme grün.

**Gegenvorschlag.** Nach dem Loslassen wie in
`testBew18_2AufDerFremdenBaseLosgelassenSetztArbiterDieSpinneAnDieNächsteFreieStelle`
zusätzlich `höchstensUmHundertstelWeiter(punkt, danach, summeDerRadien(spinne, warrior) - Fraction(1, 2))`
prüfen; das schließt die *Stelle* vor dem Ziehen (3″ entfernt) aus.

**Stellungnahme.** Angenommen. In
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py) prüft
`testBew18_2DieKarteZeigtDieSpinneBeimHaltenÜberDerBaseUndDanachAnIhrerStelle` nach dem
Loslassen zusätzlich `höchstensUmHundertstelWeiter(punkt, danach, kürzesterWeg)` mit
`kürzesterWeg = summeDerRadien(spinne, warrior) - halbesZoll`; der Punkt steht jetzt als
`-halbesZoll` neben der Mitte. Die *Stelle* vor dem Ziehen liegt 3½″ vom Punkt, der kürzeste
Weg bei etwa 1,3″: Ein Zurückspringen macht den Test rot.
