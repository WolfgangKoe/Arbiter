# Hindernis: Kritik an den Tests zu Item ruhigeKarte

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testQue7_1DieKarteBleibtStehenWennEinGrundAufhörtZuSehenZuSein[fenster1024], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenZuSehenBeginnt[fenster1100], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenZuSehenBeginnt[fenster1280], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenZuSehenBeginnt[fenster1920], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenAufhörtZuSehenZuSein[fenster1100], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenAufhörtZuSehenZuSein[fenster1280], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenAufhörtZuSehenZuSein[fenster1920], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1100-vonSpielerEinsZuSpielerZwei], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1100-vonSpielerZweiZuSpielerEins], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1280-vonSpielerEinsZuSpielerZwei], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1280-vonSpielerZweiZuSpielerEins], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1920-vonSpielerEinsZuSpielerZwei], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1920-vonSpielerZweiZuSpielerEins], testQue7_1DieKarteBleibtStehenWennEineEinheitAusgewähltWird[fenster1024], testQue7_1DieKarteBleibtStehenWennEineEinheitAusgewähltWird[fenster1100], testQue7_1DieKarteBleibtStehenWennEineEinheitAusgewähltWird[fenster1280], testQue7_1DieKarteBleibtStehenWennEineEinheitAusgewähltWird[fenster1920], testQue7_1DieKarteBleibtStehenWennEineEinheitNichtMehrAusgewähltIst[fenster1024], testQue7_1DieKarteBleibtStehenWennEineEinheitNichtMehrAusgewähltIst[fenster1100], testQue7_1DieKarteBleibtStehenWennEineEinheitNichtMehrAusgewähltIst[fenster1280], testQue7_1DieKarteBleibtStehenWennEineEinheitNichtMehrAusgewähltIst[fenster1920], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt[fenster1024], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt[fenster1100], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt[fenster1280], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt[fenster1920], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenDieKnöpfeZumUmbruchBringt[fenster1920], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAmZugIst[fenster1024], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAmZugIst[fenster1100], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAmZugIst[fenster1280], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAmZugIst[fenster1920]. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item ruhigeKarte“ von Fachkritiker im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Angenommen, die Tests bleiben, wie sie sind. Am Produkt aus 4fd5bd9 sind genau
diese 30 grün, 62 sind rot. Gemessen in `/tmp`. Die Stelle: `.spalteMitte` in
`technik/frontend/komponenten.css` (4fd5bd9) gibt der *Karte* den restlichen Platz (`minmax(0, 1fr)`).
Sie bleibt stehen, solange die Zeilen darunter gleich hoch bleiben. Das ist hier der Fall: Die
Knopfzeile bleibt einzeilig (40 Pixel), die Kopfzeile 75 Pixel. Der neue Knopf („Vorrücken“,
„gemeinsam übergehen“, „Einheit zurücklegen“) passt neben „Phase beenden“ oder „Aufstellen der
Einheit beenden“. In den roten Fenstern bricht er um (92 Pixel). Bei
`…EinGrundAufhörtZuSehenZuSein[fenster1024]` nimmt der Umbruch genau den Platz des verschwundenen
*Grunds* ein (52 Pixel). Jede Handlung ist in einem anderen Fenster rot, bis auf die vier Tests aus
14501. Diese werden rot, sobald ihr Knopf umbricht.
