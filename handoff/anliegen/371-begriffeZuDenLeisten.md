# Begriffe zu den Leisten

371 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Deine Antwort in 366 F1 A (git) steht als
[QUE-6 · Leisten](../../domaene/anforderungen/querschnitt/leisten.md): links die *Ablage* von
„Spieler 1“, rechts die von „Spieler 2“, unten das *Protokoll*; jede fährt per *Griff* ein und
aus, beim Start ist keine eingefahren, und Tippen mit dem Finger wirkt wie ein Klick. Dafür
brauchen die Kriterien drei neue Begriffe, die im [Glossar](../../domaene/glossar.md) stehen.
Keiner hat einen englischen Regelbegriff; die Code-Bezeichner sind die Namen, die der Architekt
in [Oberfläche, O4](../../technik/architektur/oberflaeche.md) schon gewählt hat.

**Kosten.** Ohne deine Freigabe der Begriffe ist QUE-6 nicht bereit für einen Plan.

**Gegenvorschlag.** Du gibst die Begriffe frei; ein anderes Wort ändert Glossar und QUE-6.

**F1 · Leiste** (Code `leiste`): Bereich am Rand des Bildschirms neben der *Karte*, den die
*Spieler* ein- und ausfahren; es gibt drei: links, rechts und unten. Empfehlung: dein Wort aus
362 („einfahrbare Seitenleisten“), gekürzt, weil die untere keine Seite ist.

Antwort: .

**F2 · Griff** (Code `leistenGriff`): Schaltfläche am Rand einer *Leiste*, mit der die
*Spieler* sie ein- und ausfahren. Empfehlung: das Wort aus ArbiterMap
(`ArbiterMap/docs/spec/design_system.md:87`).

Antwort: .

**F3 · eingefahren** (Code `eingefahren`): Zustand einer *Leiste*, die nur ihren *Griff* zeigt;
das Gegenteil heißt „nicht eingefahren“, damit ein Begriff genügt. Empfehlung: so.

Antwort: .

**Stellungnahme.**
