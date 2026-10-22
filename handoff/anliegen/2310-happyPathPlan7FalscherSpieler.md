# Plan 7: Spieler 2 hat keine Boyz, der Happy Path lässt sich so nicht spielen

Form: Kritik
Von: Fachkritiker
An: Planer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf, ein Schritt
des Happy Path fehlt. Der Stakeholder gibt nach Schritt 1 bis 6 im [Plan](../plan.md) frei
und prüft das Review daran.
1. Schritt 2: „Spieler 2 klickt die Boyz in seiner Spalte an“. Die Boyz gehören Spieler 1
   ([Ausgangslage](../../domaene/daten/ausgangslage.yaml): erste Armee; links nach
   [QUE-6.1](../../domaene/anforderungen/querschnitt/leisten.md); so auch alle Mockups). In
   der Spalte von Spieler 2 stehen Necron Warriors und Overlord. Beim Start ist Spieler 2 *an
   der Reihe* ([AUF-6.1](../../domaene/anforderungen/phasen/aufstellen/vorlaeufigerStart.md)).
   Folgerichtig falsch sind Schritt 6 („Spieler 1 ist an der Reihe“, *Protokoll*: „Boyz,
   Spieler 2“) und, sobald Spieler 1 die Boyz erst nach einer Einheit von Spieler 2
   aufstellt, Schritt 3 („Die *Karte* ist leer“).
2. Schritt 5: „Er zieht einen Boy weit weg“. Nach Schritt 4 ist die ganze *Einheit* die
   *Ebene*, Ziehen bewegt den Block (AUF-21.1). Es fehlt der Klick auf den einen Boy, der
   ihn allein *ausgewählt* macht (Review 6, Schritt 5). Ohne ihn kommt ‚keine Kohärenz‘ nie.
3. Nebenbei, für sich allein wartete es: „dazu ist AUF-29.2 noch offen, 2212“ stimmt nicht
   mehr. Der Anforderungsautor hat AUF-29.1 und 29.2 nachgebessert, 2212 ist erledigt; die
   Abhängigkeit im Item [Anhalten auf dem Weg](../../domaene/items/anhaltenAufDemWeg.md) ist
   damit nur noch Item 2. An Umfang und Reihenfolge von Plan 7 ändert das nichts: Item 1
   folgt den Entscheidungen 1650 und 1652, die drei Schritte dem Zyklusziel.

**Kosten.** Wer den Plan nachspielt, bleibt bei Schritt 2 hängen: Der Klick in die Zone bringt
‚nicht an der Reihe‘ ([AUF-22.1](../../domaene/anforderungen/phasen/aufstellen/ausserDerReihe.md)). Bei Schritt 5 zieht er den Block und sieht keine *Sperre*. Der Reviewer
übernimmt die Schritte ins Review.

**Gegenvorschlag.** Die Schritte 2 bis 6 mit der *Einheit* von Spieler 2 erzählen: Necron
Warriors statt Boyz, „ein Necron Warrior“ statt „ein Boy“; dann stimmen „Die *Karte* ist
leer“, „Spieler 1 ist *an der Reihe*“ und der Eintrag „Necron Warriors, Spieler 2, ‚keine
Kohärenz‘“. In Schritt 5 vor dem Ziehen: „Er klickt einen Necron Warrior an, nur er ist
golden umrandet, und zieht ihn weit weg“. In „Abweichung vom Zyklusziel“ den Halbsatz zu
2212 streichen.
Erledigt, wenn sich Schritt 1 bis 6 vom Start an so am Bildschirm spielen lassen.

**Stellungnahme.** Umgesetzt im neuen Happy Path des [Plans](../plan.md), der nach dem neuen
Schnitt (Anliegen 2363) ohne Übergehen auskommt: Spieler 2
stellt die Necron Warriors auf, klickt vor dem Ziehen einen Necron Warrior an, nur er ist
golden umrandet; nach dem Beenden ist Spieler 1 *an der Reihe*. Der Halbsatz zu 2212 ist mit
dem Abschnitt weg; das Item [Anhalten auf dem Weg](../../domaene/items/anhaltenAufDemWeg.md)
hängt nicht mehr an 2212.
