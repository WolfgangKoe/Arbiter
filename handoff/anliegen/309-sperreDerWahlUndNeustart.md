# Plan 4: Wo die Sperre einer Wahl steht, was ein Neustart zeigt

309 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 3/3 · erledigt

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
**Befund.** Ein Klick wählt in ArbiterMap jede *Einheit* aus, gesperrt wird erst die Handlung
(`ArbiterMap/docs/spec/interaction_map.md:228`, `:282`).

**Kosten.** Ohne Antwort blieb offen, wie Auswahl und *Einheit in Aufstellung* zusammengehen.

**Gegenvorschlag.** Neuer Begriff *ausgewählt*.

**F1 · Was bewirkt ein Klick auf eine Einheit in einer Ablage?** A: Auswahl, und ist sie
wählbar, zugleich *Einheit in Aufstellung*; B: nur Auswahl, *Einheit in Aufstellung* wird sie
mit dem ersten *gesetzten* *Modell*. Empfehlung B.

Antwort: .

**F2 · Wie viele Einheiten sind zugleich ausgewählt?** A: höchstens eine; B: wie ArbiterMap,
je *Spieler* bis zu zwei, die dritte verdrängt die älteste.

Antwort: B

**Stellungnahme.**

## Runde 3
**Befund.** Eingetragen sind AUF-1.8 bis AUF-1.11, AUF-3.8, AUF-5.3 bis AUF-5.9
([aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md)), QUE-3.3
([querschnitt.md](../../domaene/anforderungen/querschnitt.md)) und *ausgewählt* im
[Glossar](../../domaene/glossar.md). Eine Lücke bleibt: Abwählen geht nur per Klick in der
*Ablage* (AUF-5.4). Ist eine *ausgewählte* *Einheit* *aufgestellt*, steht sie nicht mehr in der
*Ablage* (AUF-4.3); die *Karte* kennzeichnet ihre *Modelle* weiter (AUF-5.7), und abwählen könnt
ihr sie nur noch, indem ihr zwei andere *Einheiten* desselben *Spielers* auswählt (AUF-5.5).
In ArbiterMap wählt man auf der *Karte* ab (Klick ins Leere, `interaction_map.md:260`); das
kennt Etappe 1 nicht.

**Kosten.** Ohne Antwort bleibt die Auswahl einer *aufgestellten* *Einheit* bestehen, wie oben;
ein Kriterium dazu trage ich nicht ein.

**F1 · Was wird aus der Auswahl einer Einheit, die aufgestellt ist?**
- A: Sie endet; die *Karte* kennzeichnet ihre *Modelle* nicht mehr.
- B: Sie bleibt, bis ein Klick auf der *Karte* abwählen kann (spätere Anforderung).

Empfehlung A: In Etappe 1 könnt ihr sie sonst nicht gezielt abwählen; kommt das Auswählen auf
der *Karte*, frage ich neu.

Antwort: .

**Stellungnahme.**
