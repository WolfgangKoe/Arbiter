# Protokoll im Dienst-Test zu BEW-25.1 andersherum gelesen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (ein Test liest den Vertrag falsch), Kritik an den Tests zu Item
anhaltenUebergehen nach 8b3286f.
[weiterziehenNachDemUebergehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/weiterziehenNachDemUebergehenTest.py)
`testBew25_1DerDienstSetztNachDemErneutenGemeinsamenÜbergehenAmPunktDesLoslassens` entpackt
`_, neuer = …["schlacht"]["protokoll"]`. Am Dienst steht der neueste *Eintrag* zuerst (QUE-5.4,
[V18](../../technik/architektur/vertrag/schlacht/uebergehen.md), Spielstand), `neuer` ist also
der ältere. Beide nennen ‚Bewegungsweite‘, darum ist der Test grün oder rot, gleich welcher
*Eintrag* die *Gründe* trägt: Die *Gründe* des neuen prüft er nicht, und wer ihn liest, lernt
die falsche Reihenfolge. In der Domäne (`Schlacht.protokoll`) ist es umgekehrt, der Test daneben
liest dort richtig.

**Kosten.** Ein Wort. Bleibt es, prüft der Dienst-Test zu BEW-25.1 den neuen *Eintrag* nicht.

**Gegenvorschlag.** `neuer, älterer = …["schlacht"]["protokoll"]` und, wie im Test daneben,
`älterer` gleich dem *Eintrag* nach dem ersten Übergehen (vorher aus `spielstandVon` lesen).

**Stellungnahme.** Angenommen wie vorgeschlagen. Der Test liest vor dem Loslassen den
*Eintrag* nach dem ersten Übergehen aus `spielstandVon`, entpackt danach
`neuer, davor = …["schlacht"]["protokoll"]` und prüft `davor == älterer` und die *Gründe* von
`neuer`
([weiterziehenNachDemUebergehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/weiterziehenNachDemUebergehenTest.py)).
Rot wie zuvor, weil `gemeinsamÜbergehenAngeboten` fehlt.
