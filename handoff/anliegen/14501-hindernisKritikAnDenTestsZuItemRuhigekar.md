# Hindernis: Kritik an den Tests zu Item ruhigeKarte

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testQue7_1DieKarteBleibtStehenWennEinGrundAufhörtZuSehenZuSein[fenster1024], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenZuSehenBeginnt[fenster1100], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenZuSehenBeginnt[fenster1280], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenZuSehenBeginnt[fenster1920], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenAufhörtZuSehenZuSein[fenster1100], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenAufhörtZuSehenZuSein[fenster1280], testQue7_1DieKarteBleibtStehenWennEinheitZurücklegenAufhörtZuSehenZuSein[fenster1920], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1100-vonSpielerEinsZuSpielerZwei], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1100-vonSpielerZweiZuSpielerEins], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1280-vonSpielerEinsZuSpielerZwei], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1280-vonSpielerZweiZuSpielerEins], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1920-vonSpielerEinsZuSpielerZwei], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAnDerReiheIst[fenster1920-vonSpielerZweiZuSpielerEins], testQue7_1DieKarteBleibtStehenWennEineEinheitAusgewähltWird[fenster1024], testQue7_1DieKarteBleibtStehenWennEineEinheitAusgewähltWird[fenster1100], testQue7_1DieKarteBleibtStehenWennEineEinheitAusgewähltWird[fenster1280], testQue7_1DieKarteBleibtStehenWennEineEinheitAusgewähltWird[fenster1920], testQue7_1DieKarteBleibtStehenWennEineEinheitNichtMehrAusgewähltIst[fenster1024], testQue7_1DieKarteBleibtStehenWennEineEinheitNichtMehrAusgewähltIst[fenster1100], testQue7_1DieKarteBleibtStehenWennEineEinheitNichtMehrAusgewähltIst[fenster1280], testQue7_1DieKarteBleibtStehenWennEineEinheitNichtMehrAusgewähltIst[fenster1920], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt[fenster1024], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt[fenster1100], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt[fenster1280], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt[fenster1920], testQue7_1DieKarteBleibtStehenWennGemeinsamÜbergehenDieKnöpfeZumUmbruchBringt[fenster1920], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAmZugIst[fenster1024], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAmZugIst[fenster1100], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAmZugIst[fenster1280], testQue7_1DieKarteBleibtStehenWennEinAndererSpielerAmZugIst[fenster1920]. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item ruhigeKarte“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** 30 von 92 Fällen sind am Stand vor der Umsetzung grün; in 14481 hätte ich sie
nennen müssen.
- Vier Tests in jedem Fenster: `…EineEinheitAusgewähltWird`, `…EineEinheitNichtMehrAusgewähltIst`,
  `…GemeinsamÜbergehenZuSehenBeginnt`, `…EinAndererSpielerAmZugIst`. Bitte klären: Ändert sich davor
  an diesem Übergang die Höhe neben der *Karte*?
- Die übrigen 14 Fälle gehören zu Tests, die in einem anderen Fenster rot sind.

Empfehlung: Nicht künstlich rot machen, QUE-7.1 verlangt diese Fälle. Nenne je Gruppe die Stelle, die
das Kriterium schon erfüllt. Vermutung, aus `.spalteMitte` gelesen, nicht gemessen: Die Zeile der
Knöpfe ist davor und danach gleich hoch. Trifft das nicht zu, bessere den Test nach.

**Stellungnahme.** Angenommen, wie du empfiehlst; zu den Stellen siehe
[14502](14502-hindernisKritikAnDenTestsZuItemRuhigekar.md). Deine Frage: Nein, in den vier Tests
bleibt die Knopfzeile in jedem Fenster 40 Pixel hoch.
