# Plan 4: Wo die Sperre einer Wahl steht, was ein Neustart zeigt

309 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 2/3 · offen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Plan 4: Spieler 2 klickt eine seiner *Einheiten* in seiner *Ablage* an, sie wird
*Einheit in Aufstellung* (AUF-5, AUF-6); Arbiter behält das (QUE-3).

**Kosten.** Ohne Antwort hätte die Technik den Neustart entschieden.

**F1 · Wo, wie lange und mit welchem Satz zeigt Arbiter, dass eine Wahl abgelehnt ist?**
A: an der *Einheit* in der *Ablage*; B: an einem festen Ort bei der *Karte*; C: anders.

Antwort: Eine Einheit kann immer angeklickt werden. Und zwar egal, welcher Spieler dran ist. Die Einheit eines Spielers, der NICHT an der Reihe ist, darf im Zug des Spielers, der an der Reihe ist, beispielswesie nicht in der Bewegungsphase bewegt werden. Schau nochmal in ArbiterMap, wie es gemacht wurde. Dort ist die Regelung in Ordnung gewesen.

**F2 · Was seht ihr, wenn ihr Arbiter beendet und neu startet?** A: die *Ausgangslage*
mit der Wahl nach AUF-6; B: die letzte Partie, mit Knopf „Neue Partie“.

Antwort: A

**Stellungnahme.**

## Runde 2
**Befund.** F2 steht als QUE-3.3 in
[querschnitt.md](../../domaene/anforderungen/querschnitt.md). Zu F1: In ArbiterMap wählt ein
Klick jede *Einheit* beider *Spieler* jederzeit aus; sie wird hervorgehoben, gesperrt wird erst
die Handlung (`ArbiterMap/docs/spec/interaction_map.md:228`, `:282`). Bei uns macht der Klick
die *Einheit* zur *Einheit in Aufstellung* und trifft darum eine *Sperre*, wenn AUF-1.5 oder
AUF-1.6 es verbieten (AUF-5). Eine *Einheit in Aufstellung* gab es in ArbiterMap nicht; wie
beides zusammengeht, sagen weder Regeln noch ArbiterMap.

**Kosten.** Bis zur Antwort bleibt AUF-5, wie es ist, und zur Auswahl trage ich nichts ein.
Bei F1 B entfällt AUF-5, bevor es einen Test hat.

**Gegenvorschlag.** Neuer Begriff für beide Wege: *ausgewählt* | – | `ausgewählt` | Zustand
einer *Einheit*, die ein *Spieler* angeklickt hat, gleich wer *an der Reihe* ist; erlaubt
keine Handlung. Die *Ablage* kennzeichnet sie, die *Karte* ihre *gesetzten* *Modelle*.

**F1 · Was bewirkt ein Klick auf eine Einheit in einer Ablage?**
- A: Er wählt sie immer aus. Ist sie nach AUF-1.5 und AUF-1.6 wählbar, wird sie zugleich
  *Einheit in Aufstellung*; *setzen* lassen sich nur deren *Modelle* (AUF-1.4). AUF-1 und
  AUF-5 bleiben, die *Ablage* kennzeichnet zwei Dinge.
- B: Er wählt sie nur aus, wie in ArbiterMap. *Einheit in Aufstellung* wird eine *Einheit*,
  sobald ihr erstes *Modell* *gesetzt* ist; ‚nicht wählbar‘ und ‚Einheit begonnen‘ sperren
  dann das *Setzen* auf der *Karte*, wo das *Modell* mit *Grund* stehen bleibt (Etappe 1).
  AUF-1.4 bis AUF-1.6 und AUF-5 werden neu gefasst, mit neuen Kennungen.

Empfehlung B: Wählen ist frei, gesperrt wird die Handlung, wie in ArbiterMap; kein Klick wird
abgelehnt, also braucht es keinen Satz dafür. Kosten: Die grünen Tests zu AUF-1.4 bis AUF-1.6
werden ersetzt; nach QUE-3.2 behält Arbiter auch die Auswahl.

Antwort: .

**F2 · Wie viele Einheiten sind zugleich ausgewählt?**
- A: Höchstens eine; ein Klick auf eine andere ersetzt sie, auf dieselbe hebt er sie auf.
- B: Wie ArbiterMap: je *Spieler* bis zu zwei, ein Klick fügt hinzu oder hebt auf, eine
  dritte verdrängt die älteste (`interaction_map.md:296`, `:337`).

Empfehlung A: In Etappe 1 zeigt die Auswahl nur, welche *Einheit* gemeint ist; braucht eine
spätere Etappe mehrere, frage ich neu.

Antwort: .

**Stellungnahme.**
