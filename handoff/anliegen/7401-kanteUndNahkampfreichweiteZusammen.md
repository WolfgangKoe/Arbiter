# BEW-6.3 ohne Test für Kante und Nahkampfreichweite zusammen

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik an den Tests zu Item anhaltenUndAuswahl, wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Randfall abseits des Happy Path). BEW-6.3 regelt jedes
Paar aus BEW-3.1, 6.1 und 6.2; die vier Tests in
[anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py)
prüfen nur *Bewegungsweite* gegen *Spielfeldkante* und *Bewegungsweite* gegen
*Nahkampfreichweite*. Steht ein *Modell* des anderen *Spielers* nahe der *Spielfeldkante*, prüft
kein Test, welche der beiden Grenzen zuerst anhält.

**Kosten.** Am Bildschirm nichts, solange der Code die kürzeste Strecke über alle drei nimmt;
prüft er die Grenzen nacheinander, bleibt das unentdeckt. Zwei Tests.

**Gegenvorschlag.** Je ein Test „Liegt die Kante vor der Nahkampfreichweite …“ und „Liegt die
Nahkampfreichweite vor der Kante …“, etwa mit dem Overlord nahe einer *Spielfeldkante* und dem
Warboss, der schräg darauf zu zieht.

**Stellungnahme.** Angenommen, umgesetzt in
[anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py):
`testBew6_3LiegenKanteUndNahkampfreichweiteAufDemWegHältArbiterAnDerErstenAn` mit zwei Fällen
(`kanteVorDerNahkampfreichweite`, `nahkampfreichweiteVorDerKante`). Der Overlord steht an der
Nordkante, der Warboss zieht von zwei *Stellen* daneben auf dasselbe Ziel jenseits der Kante und
in dessen *Nahkampfreichweite*; die Vorgeschichte prüft beides und die *Bewegungsweite*. Geprüft
wird je Fall, dass er an der einen Grenze anhält und nicht an der anderen. Beide grün, ruff grün.
