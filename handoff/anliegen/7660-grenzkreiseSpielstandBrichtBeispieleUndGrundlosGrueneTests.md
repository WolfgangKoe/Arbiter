# Grenzkreise: neue Schlüssel brechen vier Beispieltests, drei Tests ohne Code grün

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item grenzkreise (uncommittet, Formprüfungen und `ruff`
grün; 241 rot, 3 grün). Hält auf nach [Kritik](../../prozess/ablauf/kritik.md):
1. V21 bringt `schlacht.grenzen` und `schlacht.vorrücken` immer in den Spielstand. Vier Tests
   vergleichen das ganze `schlacht` gleich einem Beispiel und werden rot, sobald der
   Implementierer V21 erfüllt; er darf sie nicht ändern:
   `testQue10_1…` ([schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py), `schlacht.json`),
   `testQue9_2DerDienst…` ([ersterZugTest.py](../../technik/tests/akzeptanz/querschnitt/ersterZugTest.py), Wörterbuch im Test; ihm fehlt auch schon `protokoll`),
   `testQue5_4…` ([uebergehenTest.py](../../technik/tests/akzeptanz/querschnitt/uebergehenTest.py), `protokoll.json`),
   `testBew8_1DerDienst…` ([uebergehenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/uebergehenBeimZiehenTest.py), `uebergehbar.json`).
   Jeder weitere Schlüssel eines späteren Items bricht sie wieder (SOLID O).
2. `testBew12_2AmBildschirmNimmtDerKnopfDieGrenzeDesWurfsZurück`
   ([vorrueckenZuruecknehmenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/vorrueckenZuruecknehmenTest.py))
   zählt die Grenzen nur vorher (2); danach prüft er Knopf und Domäne, nicht die Grenze, die
   sein Name verspricht.
3. Ohne Produktcode schon grün, sie prüfen nur ein Fehlen:
   `testBew11_4DieSeiteZeigtOhneAuswahlKeineGrenze`,
   `testBew5_1DieSeiteZeigtOhneAuswahlKeinenKnopfVorrücken`,
   `testBew12_1DieSeiteZeigtOhneVorrückenKeinenKnopfZurücknehmen` (wie 7300, 7400).
4. Ich habe V21 berichtigt: Der Radius heißt `"radius"`, nicht `"r"`; ein Name hat mindestens
   3 Zeichen, Ausnahme nur `x`, `y` ([Es 5](../../prozess/praemissen/es.md)). V20 nennt jetzt
   `Grenze(einheit, kreise, wurf, wählbar, nahkampfreichweite)`, wie eure Tests sie lesen.

**Kosten.** Am Bildschirm nichts. Bleibt 1, kann Item grenzkreise nicht grün werden, ohne
vier fremde Tests rot zu machen. Bleiben 2 und 3, bliebe eine Seite grün, die nach dem
Zurücknehmen den Kreis des Wurfs weiter zeigt oder Grenze und Knöpfe nie zeichnet.

**Gegenvorschlag.**
1. Eine Hilfe in [dienst.py](../../technik/tests/akzeptanz/dienst.py), etwa
   `schlachtNachSchlüsselnDes(spielstand, beispiel)`, die von `spielstand["schlacht"]` nur
   die Schlüssel des Beispiels nimmt; die vier Tests vergleichen damit. So steht es jetzt in
   [Spielstand](../../technik/architektur/vertrag/schlacht/spielstand.md). Die Beispiele
   bleiben, wie sie sind.
2. Danach `expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(1)`.
3. Erst den Zustand mit Grenze oder Knopf zeigen, dann per Klick auf die leere *Karte*
   abwählen und das Fehlen zählen; für „Vorrücken zurücknehmen“ reicht 2.
4. In [grenzen.py](../../technik/tests/akzeptanz/grenzen.py) `kreis["r"]` →
   `kreis["radius"]`.

**Stellungnahme.** Angenommen, alles umgesetzt; `ruff` und Formprüfungen grün.
1. `schlachtNachSchlüsselnDes` in [dienst.py](../../technik/tests/akzeptanz/dienst.py); die
   vier Tests vergleichen damit. `testQue9_2` grün; `testQue10_1`, `testQue5_4` rot am
   fehlenden `protokoll`, `testBew8_1` am fehlenden `übergehbar`: am Produkt.
2. Nach dem Klick: `.karte g.grenze.spieler1` gleich 1.
3. `testBew11_4…` und `testBew5_1…` zählen erst *Grenze* bzw. „Vorrücken“ (1), klicken
   die leere *Karte* und zählen dann das Fehlen. `testBew12_1…` prüft zu ausgewählten Boyz:
   „Vorrücken“ da, „Vorrücken zurücknehmen“ fehlt. Alle drei rot am Produkt.
4. `kreis["radius"]` in [grenzen.py](../../technik/tests/akzeptanz/grenzen.py).
