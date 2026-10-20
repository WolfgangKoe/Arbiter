# Kein Test hält die Zugschwelle an Karte und Einheitenkarte

1221 · Kritik · von Reviewer → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code zu Item [setzenPerKlick](../../domaene/items/setzenPerKlick.md).
Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet, denn es ist eine Lücke
abseits des Happy Path. Die Zugschwelle prüft nur
`testAuf8_2EinModellBleibtBeiWenigerAlsDerZugschwelleAbweichungAnSeinerStelle` an einem
*Modell* ([622](622-zugschwelleUngeprueft.md)). Dass ein Zug auf einer *Einheitenkarte* nicht
auswählt und ein Zug auf dem *Spielfeld* keine *Formation* *setzt* (V8, AUF-18.1), prüft kein
Test. Der Fehler in [1220](1220-zugAufKarteUndEinheitenkarteGiltAlsKlick.md) blieb deshalb in
allen Akzeptanztests grün.

**Kosten.** Mit Item 2 baut der Implementierer den Klick um (V9). Ein Rückfall bliebe
unbemerkt.

**Gegenvorschlag.** Je Eingabe ein Bildschirmtest: Maus auf einer *Einheitenkarte* drücken,
mehr als 4 px ziehen, loslassen. Erwartet wird, dass keine Anfrage an den Server geht und
nichts *ausgewählt* ist. Dasselbe auf dem *Spielfeld* mit einer *ausgewählten* *Einheit*:
keine Anfrage, kein *Modell* *gesetzt*. Erledigt, wenn beide Tests gegen den Stand vor 1220
rot sind und danach grün.

**Stellungnahme.** Angenommen. Zwei Bildschirmtests in
[setzenPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py):
`testAuf18_1EinZugAufDerEinheitenkarteWähltDieEinheitNichtAus` und
`testAuf18_1EinZugAufDemSpielfeldSetztDieAusgewählteEinheitNicht`. Beide drücken mit der Maus,
ziehen 12 px und lassen los; erwartet: keine ändernde Anfrage, nichts *ausgewählt* beziehungsweise
kein *Modell* *gesetzt*. Geprüft: Mit dem aktuellen Frontend grün, mit einem zusätzlichen
`click`-Listener (ein Zug gilt als Klick, Stand von 1220) beide rot.
