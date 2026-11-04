# Tests zu BEW-17 prüfen weder den Auslöser noch das Angebot danach

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Die Abweichungen aus Anliegen 12700 (Reviewer an Implementierer) sind grün: Kein Test zu BEW-17.1 stellt eine
fremde *Base* an die *Bewegungsweite* mit dem Punkt hinter ihr (heute 409 ‚Base überdeckt‘
statt Anhalten davor) oder eine *Base* hinter die *Bewegungsweite* mit dem Punkt schräg auf
ihr (heute 29.2 statt V16). Kein Test zu BEW-8.3 lässt nach 17.1 oder 17.4 los: Nach einem
Halt vor einer *Base* innerhalb der *Bewegungsweite* bietet Arbiter heute *gemeinsam übergehen*
an, nach einem Halt nach 17.4 vor der *Nahkampfreichweite* nicht.

**Kosten.** Die Tests zu BEW-17 und BEW-8.3 prüfen ihre Kriterien dort nicht, wo der Code
falsch ist; der Implementierer kann 12700 nicht gegen einen roten Test umsetzen.

**Gegenvorschlag.** Die Fälle aus dem Absatz „Prüft“ in
[Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md): 17.1 am Dienst mit einem
*Modell* einer anderen eigenen *Einheit* knapp hinter der *Bewegungsweite* und dem Punkt
dahinter, einmal ohne, einmal mit der Abfrage davor (200, vor ihr angehalten); 17.1 mit einer
*Base* hinter der *Bewegungsweite* (*Stellen* nach V16). BEW-8.3 nach einem Halt vor einer
*Base* (nicht angeboten) und nach 17.4 vor der *Nahkampfreichweite* (angeboten). Zahlen: Anliegen 12700; für 17.4 zuvor (−1,2″, 0),
Punkt (−1,2″, 4″), ein *Modell* des anderen *Spielers* bei (−3″, 2″), Boy-große *Bases*.

**Stellungnahme.** Angenommen, fünf neue Tests, alle rot gegen den jetzigen Code. In
[anhaltenVorFremdenBasesTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorFremdenBasesTest.py):
`testBew17_1StehtDerPunktHinterEinerBaseAnDerBewegungsweiteHältDerDienstDasModellVorIhrAn`
(der Warboss knapp hinter der *Bewegungsweite* eines Boys, Punkt dahinter; ohne und nach einer
Abfrage, die davor anhielt; heute 409) und
`testBew17_1EineBaseHinterDerBewegungsweiteLenktDasModellNichtAb` (Punkt schräg auf den
Warboss hinter der *Bewegungsweite* des Boss Nob; erwartet die *Stelle* nach V16 ohne
`angehaltenAufDemWeg`, heute nach 29.2 seitlich verschoben). In
[uebergehenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/uebergehenBeimZiehenTest.py):
`testBew8_3HältEineFremdeBaseVorDerBewegungsweiteAnBietetArbiterGemeinsamÜbergehenNichtAn`
(Punkt auf der *Base*, damit nur Fehler 2 aus 12700 greift; heute angeboten) und
`testBew8_3HältNachDemAnhaltenAufDemWegDieNahkampfreichweiteBietetDerDienstGemeinsamÜbergehenAn`
(heute nicht angeboten). Abweichung bei den Zahlen: Der Warboss steht nicht bei (−3″, 2″),
sondern wie in `testBew17_4…` bei (−3,4″, 2″). Mit seiner *Base* (40 mm) berührt bei (−3″, 2″)
schon die Strecke ab der *Stelle* vor dem Ziehen die *Nahkampfreichweite*, und der Test
wäre heute grün. Ein Boy lässt sich dort nicht hinstellen: Er stünde außerhalb der
Kohärenz, und die *Phase* ließe sich nicht beenden. Die Hilfen `warbossNebenDenBoyZiehen`
und `warbossÜbergehenBisZumZugDerNecrons` stehen jetzt in
[schlacht.py](../../technik/tests/akzeptanz/schlacht.py).
