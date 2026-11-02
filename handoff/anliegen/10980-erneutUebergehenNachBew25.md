# Tests zu Item anhaltenUebergehen: erneut übergehen nach BEW-25.1

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Kritik an den Tests zu Item anhaltenUebergehen. Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md): Ein Test prüft sein Kriterium nicht.

[BEW-25.1](../../domaene/anforderungen/phasen/bewegung/weiterziehenNachDemUebergehen.md)
endet mit „und BEW-8.3 gilt“; der Zweck von BEW-25 ist, dass ein *Modell* nach dem Übergehen
nicht „ohne *Eintrag* im *Protokoll* beliebig weit“ zieht, und
[Schritt 2 im Plan](../plan.md) sagt: „Arbiter bietet wieder ‚gemeinsam übergehen‘ an“.
Die Tests in
[weiterziehenNachDemUebergehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/weiterziehenNachDemUebergehenTest.py)
prüfen nach dem zweiten Loslassen nur `gemeinsamÜbergehenAngeboten is True`. Kein Test wählt
danach *gemeinsam übergehen*: Ein Produkt, das das Angebot nur wieder einschaltet, ohne den neuen
Punkt des Loslassens zu merken, oder das beim zweiten Übergehen keinen *Grund* findet, weil das
*Modell* schon über der *Bewegungsweite* oder in *Nahkampfreichweite* steht und nichts mehr neu
überschritten wird, bestünde alle Tests. Genau das soll BEW-25 verhindern. Auch die Tests zu
BEW-8.4 und 8.5 übergehen jedes *Modell* nur einmal.

**Kosten.** Ohne Test kann das *Protokoll* am Bildschirm einen *Eintrag* ohne *Grund* oder gar
keinen zeigen, oder das *Modell* bleibt nach dem Klick stehen; der *Stakeholder* sähe es erst
im Review. Ein parametrierter Test in der Domäne, einer am Dienst, rot aus demselben Grund wie
die übrigen.

**Gegenvorschlag.** In `weiterziehenNachDemUebergehenTest.py` mit den drei Fällen von
`testBew25_1ZiehtEinÜbergangenesModellWeiter…` (über der *Bewegungsweite*, in *Nahkampfreichweite*,
beide): nach dem zweiten Loslassen `gemeinsamÜbergehen()`; das *Modell* steht am zweiten Punkt
des Loslassens, das *Protokoll* hat zwei *Einträge*, der neuere mit ‚Bewegungsweite‘, mit
‚Nahkampfreichweite‘ bzw. beiden (BEW-25.1 „im ersten Fall BEW-3.1, im zweiten 6.2, in beiden
beide“, BEW-8.5). Dazu am Dienst: `PUT /api/gemeinsamÜbergehen` nach dem zweiten Loslassen, 200,
*Stelle* am zweiten Punkt, zwei *Einträge*. Weg und Richtung wie im bestehenden Test.
