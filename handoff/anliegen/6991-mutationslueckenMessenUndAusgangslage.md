# Mutationslücken in messen und der Ausgangslage

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

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

**Stellungnahme.** Angenommen, beide Punkte umgesetzt. 1: Zwei Tests in
[messenTest.py](../../technik/tests/einheit/domaene/messenTest.py) mit schrägem Weg und Start
außerhalb des Ursprungs, einer für `anteilBisZurBerührung`, einer für `streckeÜberdeckt`
(Zeile 133, dort liegt die Berührung vor dem Streckenende, damit ein falscher Anteil auffällt).
Die Formel steht schon als eine Funktion, `_anteilDesNächstenPunkts`, für beide Aufrufer.
2: Die Prüfung „derselbe Spieler“ in
[ausgangslage.py](../../technik/arbiter/domaene/missionsvorbereitung/ausgangslage.py)
gestrichen; der Test bleibt grün. Der Mutationslauf selbst ist nicht wiederholt.

**Nachprüfung.** In Ordnung, je Mutant von Hand in einer Kopie in `/tmp` eingesetzt. 2: Die
Prüfung ist gestrichen; fällt auch der verbleibende `raise` weg, wird
`testDerselbeSpielerAlsBeideSpielerIstEineVorbedingungsverletzung` rot. 1: Mit den ersten
Zahlen überlebten drei Mutanten im Zähler; den Rest führt
[7600](7600-schraegeTestsFangenDenZaehlerNicht.md). Mit den Zahlen von dort, die jetzt in
[messenTest.py](../../technik/tests/einheit/domaene/messenTest.py) stehen, sind alle sieben
geprobten Mutanten der Formel gefangen. Lesbarkeit der Tests: kein Befund.
