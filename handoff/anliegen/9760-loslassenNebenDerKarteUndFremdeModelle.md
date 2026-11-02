# Loslassen neben der Karte und fremde Modelle in der Bewegungsphase

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Zwei Fälle der *Bewegungsphase* regeln Regeltext und Ziel nicht eindeutig.
- F1 aus [8480](8480-ueberDieKanteHinausLoslassen.md), Plan 10, Item
  [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md): Zieht ihr einen Boy
  über die Kante der *Karte* hinaus, zeigt die *Karte* ihn an der *Spielfeldkante* angehalten
  (BEW-6.4). Lasst ihr dort los, springt er heute zurück, wo er vor dem Ziehen stand.
- F2 aus [6986](6986-bewegungLueckenFuerSpaeter.md) Punkt 2, in keinem Plan: Zieht jemand ein
  *Modell* des *Spielers*, der nicht *am Zug* ist, springt es beim Loslassen ohne *Grund* zurück
  (BEW-10.1). Das hat niemand entschieden, es kam aus dem Code.

**Kosten.** Je Frage ein Kriterium und ein Test. F1 A ändert das Frontend (Item
loslassenNebenDerKarte), F1 B nichts. F2 B bringt eine *Sperre* mit neuem *Grund* und
„gemeinsam übergehen“, F2 A nichts.

**Gegenvorschlag.** Siehe Fragen. Du musst nur je Frage den Buchstaben eintragen.

**Stellungnahme.**

Annahme: [BEW-20.1](../../domaene/anforderungen/phasen/bewegung/loslassenNebenDerKarte.md) steht nach F1 A.
**F1 · Was geschieht, wenn ihr in der Bewegungsphase ein Modell neben der Karte loslasst?**
A: Arbiter *setzt* es, wo die *Karte* es zuletzt zeigte, etwa an der Kante angehalten (ArbiterMap `model_drag.js:1536`, wie AUF-28.1).
B: Es steht, wo es vor dem Ziehen war, ohne *Grund* (Anliegen 380 F1 A, wie AUF-16.8).
Empfehlung: A, denn die *Karte* zeigt beim Ziehen schon das Anhalten, ArbiterMap setzt dort, und das Loslassen nimmt den Zug nicht zurück.
Antwort: WIe bei ArbiterMap klemmt ein Modell am Kartenrand, es sei denn bei Flugzeugen. Die kommen in die Reserve oder sind dannzerstört. Mache ein Regelrecherche dazu,

**F2 · Was geschieht, wenn jemand in der Bewegungsphase ein Modell des Spielers zieht, der nicht am Zug ist?**
A: Es springt beim Loslassen zurück, ohne *Grund*, wie heute und in den übrigen *Phasen* (Anliegen 07, wie QUE-10.5).
B: Arbiter sperrt mit dem *Grund* ‚nicht am Zug‘; ihr könnt die *Sperre* *gemeinsam übergehen*, etwa für ein verrutschtes *Modell* (Ziel: „Was nicht erlaubt ist, wird gesperrt“, wie AUF-22.1).
Empfehlung: B, denn das Ziel verlangt die *Sperre*, und die *Aufstellung* regelt denselben Fall so; einplanen erst nach Etappe 2.
Antwort: Das soll nicht möglich sein außer durch "übergehen",also eher B
