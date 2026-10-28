# Hindernis: Kritik am Code zu Item normalMove

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** AUF-8.7 hat keinen Akzeptanztest, bedienung.js setzt es aber schon um (stelleDesZugs: vorige Stelle plus Weg des Zeigers seit dem Greifen; Anliegen 6100 F1 A); Akzeptanztests entstehen vor dem Code. Empfehlung: in ziehenTest.py ein gesetztes Modell abseits seiner Mitte greifen, mit Maus und Finger ziehen und loslassen; die Stelle danach ist die vorige plus der Weg des Zeigers, auf einen Pixel genau (B5), nicht der Punkt unter dem Zeiger. Das hält den Schritt „Kritik am Code zu Item normalMove“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Angenommen, umgesetzt nach deiner Empfehlung, mit Maus und Finger.
`testAuf8_7EinModellFolgtDemWegDesZeigersUndNichtDemPunktUnterDemZeiger` in
[ziehenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py) greift ein
gesetztes *Modell* um 0,8 Radius neben der Mitte und zieht den Zeiger genau nach unten. Die
*Stelle* danach ist die vorige plus der Weg, auf einen Pixel genau (B5). Läge das *Modell*
unter dem Zeiger, wäre x um etwa 4,7 Pixel verschoben und der Test rot. Neu ist
`modellAmPunktZiehen` in [ziehen.py](../../technik/tests/akzeptanz/ziehen.py), `modellZiehen`
ruft es auf. Grün gegen den Stand: `ziehenTest.py` 7 passed. Das gilt unter der Annahme F1 A
von Anliegen 6100; antwortet der Stakeholder mit B, entfällt der Test.
