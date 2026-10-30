# Ebene im Testnamen und Klick auf den anderen Spieler

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet (Ich 3: Lücken abseits des Happy Path, Namen).
1. `testBew1_1IstEinModellEbene…` ([normaleBewegungTest.py](../../technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py))
   und `testBew2_2IstEinModellEbene…` ([sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py))
   ziehen ein *Modell* einer nicht *ausgewählten* *Einheit*. Nach dem Glossar hat nur eine
   *ausgewählte* *Einheit* eine *Ebene*; der Name nennt einen Fall, den der Test nicht
   herstellt. Der Fall *Ebene* ein *Modell* (nach AUF-25.1 per zweitem Klick) in der
   *Bewegungsphase* hat keinen Test.
2. AUF-20.6 in der *Aufstellung* (`testAuf20_6EinKlickAufEinGesetztesModellInDerAufstellung…`,
   [ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py)): angeklickt
   wird nur ein *Modell* des *Spielers* *an der Reihe*; „gleich wer *an der Reihe* ist“ prüft
   dort kein Test. In der *Schlacht* deckt `einheitJederSeite` beide Seiten ab, der Happy
   Path aus Plan 8 läuft also.

**Kosten.** Keine in Zyklus 8. Bleibt es, liest der Implementierer aus dem Namen eine
*Ebene*, die nicht gesetzt ist, und ein Fehler beim Klick auf eine fremde *Einheit* in der
*Aufstellung* bliebe unbemerkt.

**Gegenvorschlag.**
1. Die beiden Tests nach ihrem Fall benennen („IstDieEinheitNichtAusgewählt…“) und, falls
   AUF-25 in der *Schlacht* gilt, je einen Test mit `auswählen` und `modellAnklicken` auf das
   gezogene *Modell* dazu; gilt es nicht, eine Frage an den Anforderungsautor.
2. Ein Test mit `aufstellungMitModellenBeiderSpieler`: Ein Klick auf ein *Modell* der
   *Einheit* des *Spielers*, der nicht *an der Reihe* ist, macht sie *ausgewählt* mit der
   ganzen *Einheit* als *Ebene*.

**Stellungnahme.** Angenommen.
1. Stand schon im Bestand: Die Tests heißen nach ihrem Fall,
   `testBew1_5IstDieEinheitNichtAusgewähltStehenDieAnderenModelleWieDavor` und
   `testBew2_5IstDieEinheitNichtAusgewähltGiltAuchEinAnderesModellDerselbenEinheitAlsFremd`.
   Für die *Ebene* ein *Modell* in der *Schlacht* gilt jetzt BEW-7 (statt AUF-25). Seine
   Tests stehen in [auswahlInDerSchlachtTest.py](../../technik/tests/akzeptanz/phasen/bewegung/auswahlInDerSchlachtTest.py),
   darunter BEW-7.3: Nur das gezogene *Modell* wird *gesetzt*.
2. Neu in [ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py):
   `testAuf20_6EinKlickInDerAufstellungWähltDieGanzeEinheitGleichWerAnDerReiheIst` mit
   `aufstellungMitModellenBeiderSpieler`, je für die *Einheit* des *Spielers* *an der Reihe*
   und die des anderen. Der Test ist rot, weil der Klick auf eine *aufgestellte* *Einheit*
   fehlt (AUF-30, Item 3). Er überschneidet sich mit AUF-30.1 (`einheitDesAnderen`), denn in
   der *Aufstellung* ist jede *Einheit* des anderen *Spielers* mit *gesetzten* *Modellen*
   schon *aufgestellt*. Er bleibt trotzdem, damit AUF-20.6 einen eigenen Test hat.
