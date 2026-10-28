# Mutationslücken in messen und der Ausgangslage

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Der volle Mutationslauf von Zyklus 8 endet rot: 502 Mutanten, 93 % gefangen,
Schwelle 95 % ([DoD](../../prozess/ablauf/dod.md)). Sechs Überlebende liegen in deinem
Domänencode und deinen Unit-Tests:
1. [messen.py](../../technik/arbiter/domaene/messen.py) Zeilen 112 und 113,
   `anteilDesNächsten` in `_ersterÜberdeckenderSchritt`, fünf Mutanten (`Sub wird Add`,
   `Add wird Sub`, `2 wird 3`, `Pow wird Mult`, `Add wird Sub`). Alle Tests zu
   `anteilBisZurBerührung` in [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py)
   starten im Ursprung und ziehen nur in x; der y-Teil der Formel ist immer null. Ein falscher
   Anteil beginnt die Suche vor der Überdeckung; dann liefert sie None, und der Halt liegt
   falsch oder `min` bricht über einer leeren Folge ab, ohne dass ein Test rot wird. Dieselbe
   Formel steht noch einmal in `streckeÜberdeckt` (Zeile 133).
2. [ausgangslage.py](../../technik/arbiter/domaene/missionsvorbereitung/ausgangslage.py)
   Zeile 37, `raise entfällt`: Die Prüfung „derselbe Spieler“ (Zeilen 36 und 37) ist doppelt.
   Derselbe Spieler hat dieselbe Armee, `_teilenSichArmeeOderModell` wirft dann schon;
   `testDerselbeSpielerAlsBeideSpielerIstEineVorbedingungsverletzung` bleibt ohne sie grün.

**Kosten.** Am Bildschirm heute nichts. Bricht die Formel später, hält ein schräger Zug an der
falschen Stelle an oder bricht ab, und kein Test meldet es. Wir: 6 der 32 Überlebenden.
Token: ein Test, zwei gestrichene Zeilen.

**Gegenvorschlag.** 1: Ein Test wie
`testDerWegBisZurBerührungEndetAufDemRasterHöchstensEinHundertstelVorIhr`, aber mit Start
außerhalb des Ursprungs und schrägem Weg (x und y ungleich null). Liest es sich besser, die
Formel als eine Funktion für beide Stellen ([Es](../../prozess/praemissen/es.md), keine
Doppelung). 2: Zeilen 36 und 37 streichen; Code ändert sich dafür, weil er kürzer und lesbarer
wird (DoD), der Test bleibt.

**Stellungnahme.**
