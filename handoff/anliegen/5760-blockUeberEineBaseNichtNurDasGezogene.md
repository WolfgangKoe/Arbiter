# Block über eine Base: nicht nur das gezogene Modell

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: eine *Sperre* fehlt, die ein Kriterium verlangt; ein Test prüft
sein Kriterium nicht).
BEW-2.5 sperrt, wenn BEW-1.5 *ein* *Modell* *setzen* würde, dessen *Base* auf seiner Strecke
eine fremde *Base* *überdeckt*; ist die ganze *Einheit* die *Ebene*, *setzt* BEW-1.5 jedes ihrer
*Modelle*. Alle Tests mit dem Block
([sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py),
`testBew2_5IstDieGanzeEinheitEbeneGiltDieBaseEinerAnderenEinheitAlsFremd`,
`testBew2_6NachDerSperreÜberEineBaseStehtJedesModellDerGanzenEinheitWieDavor`) ziehen das
erste Boyz-*Modell* (1,5″|0,63″), dessen eigene Strecke über den Warboss (4″|0,79″) führt.
Eine Umsetzung, die nur die Strecke des gezogenen *Modells* prüft, besteht alle Tests. Im
Happy Path schieben die *Spieler* die Boyz als Block am Warboss vorbei; dann ginge ein
*Modell* über dessen *Base*, ohne *Sperre* (`core_rules.txt:729`).

**Kosten.** Bleibt es, kann die Abnahme die *Sperre* ‚über eine Base‘ für den Block nicht
belegen. Nachbessern: ein Test mit vorhandenen Fixtures und Handgriffen, wenige Zeilen.

**Gegenvorschlag.** Ein Test zu BEW-2.5: `auswählen(boyz)`, das dritte *Modell*
(1,5″|3,15″, Strecke frei) 5″ nach Osten loslassen; das erste und zweite gingen über den
Warboss. Erwartet `{Grund.überEineBase}` und jedes *Modell* der Boyz wie davor (BEW-2.6).

Stellungnahme: Angenommen. Neuer Test
`testBew2_5IstDieGanzeEinheitEbeneSperrtDieÜberEineBaseJedesModellsNichtNurDieDesGezogenen`
in [sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py):
das dritte Modell der ausgewählten Boyz 5″ nach Osten; erwartet `{Grund.überEineBase}`, jedes
Modell der Boyz wie davor.
