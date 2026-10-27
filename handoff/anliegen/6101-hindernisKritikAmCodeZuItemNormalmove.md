# Hindernis: Kritik am Code zu Item normalMove

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** AUF-8.7 hat keinen Akzeptanztest, bedienung.js setzt es aber schon um (stelleDesZugs: vorige Stelle plus Weg des Zeigers seit dem Greifen; Anliegen 6100 F1 A); Akzeptanztests entstehen vor dem Code. Empfehlung: in ziehenTest.py ein gesetztes Modell abseits seiner Mitte greifen, mit Maus und Finger ziehen und loslassen; die Stelle danach ist die vorige plus der Weg des Zeigers, auf einen Pixel genau (B5), nicht der Punkt unter dem Zeiger. Das hält den Schritt „Kritik am Code zu Item normalMove“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.**
