# Vertrag Grenzkreise verlinkt ein gelöschtes Mockup

Form: Kritik
Von: Reviewer
An: Architekt
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Nachprüfung von [15321](15321-mockupsGebauterItemsLoeschen.md): Das Mockup
`domaene/mockups/bew-24.html` ist gelöscht, weil BEW-24 gebaut ist. Der
[Vertrag Grenzkreise](../../technik/architektur/vertrag/bewegung/grenzkreise.md), Abschnitt
Knöpfe (V7), verweist noch darauf: „alle vor ‚Phase beenden‘ (Mockup [bew-24](…))“. Der Link
führt ins Leere.

**Kosten.** Eine Zeile. Bleibt sie, sucht wer den Vertrag liest ein Mockup, das es nicht mehr
gibt; die Reihenfolge der Knöpfe ist im Satz davor schon genannt.

**Gegenvorschlag.** Den Klammerzusatz „(Mockup bew-24)“ streichen; der Satz endet mit „alle vor
‚Phase beenden‘.“ Belegt ist die Reihenfolge durch die Bildschirmtests zu BEW-24.

**Stellungnahme.** Umgesetzt wie vorgeschlagen: In
[Grenzkreise](../../technik/architektur/vertrag/bewegung/grenzkreise.md), Abschnitt Seite,
Knöpfe (V7), endet der Satz mit „alle vor ‚Phase beenden‘.“ Die Reihenfolge belegt
`testBew24_1DieSeiteZeigtZurGezogenenEinheitDenKnopfVorPhaseBeenden` in
`technik/tests/akzeptanz/phasen/bewegung/einheitZuruecksetzenTest.py`. Sonst verlinkt
`technik/` keines der drei gelöschten Mockups (grep nach `bew-8`, `bew-24`, `que-7`).
