# Sperre ohne Stelle gehört zu Item 2

379 · Fragen · von Architekt (Technik) → Planer (Domäne) · Runde 1/3 · angenommen

## Runde 1
**Befund.** [Plan 5](../plan.md), Empfehlung: „Reicht die Technikphase nicht für drei, rückt
Item 3 in Plan 6; Item 1 und 2 sind das Zyklusziel.“ Item 3 trägt aber AUF-12 und AUF-8.4,
ohne die Item 1 und 2 Lücken auf dem Bildschirm lassen:
- AUF-12.1: Steht ein *Modell* *gesperrt* (Item 2), dürfte jemand weitere *setzen* oder
  *zurücklegen*; der Zustand mit zwei offenen *Sperren* ist nirgends geregelt.
- AUF-12.2, 12.3: Zieht jemand außer der Reihe (AUF-7.2, 7.3, Item 1), bleibt offen, wo das
  Gezogene steht und ob Arbiter den *Grund* nennt.
Item 3 hat zudem 12 Kriterien, Item 1 sechs, Item 2 vier.

**Kosten.** Im Rückfall gibt der Stakeholder einen Bildschirm frei, der Fehler zulässt; das
widerspricht „Regelkonformität vor Komfort“ ([Ziel](../../domaene/ziel.md)).

**Gegenvorschlag.**

**F1 · Schnitt.** A: AUF-12 und AUF-8.4 wandern in Item 2, mit Mockup auf-12; den Teil von
AUF-12.1 zu *Aufstellen der Einheit beenden* prüft der Test über die Domäne, bis Item 3 den
Knopf bringt. Item 3 ist dann AUF-10.1 bis 10.4 und QUE-4. Je Item sechs bis acht
Kriterien, der Rückfall bleibt regelkonform. B: Der Rückfall entfällt, alle drei Items gelten
nur zusammen. Empfehlung A: Ein kleinerer Schnitt und ein Rückfall, der trägt.

Antwort: .

**Stellungnahme.** A, mit einer Ausnahme: AUF-12.4 (neu aus 378 F1 A) bleibt in Item 3, denn
es nennt den *Grund* der *Sperren* nach AUF-10.2 und 10.3, die erst Item 3 bringt. AUF-8.4
prüft wie AUF-12.1 zum Beenden der Test über die Domäne, bis Item 3 den Knopf bringt.
Umgesetzt: [Item 2](../../domaene/items/gesperrtStehenUndZurueck.md) AUF-9.1, 9.3, 9.4,
AUF-15.1, AUF-8.4, AUF-12.1 bis 12.3, Mockup auf-12 (acht Kriterien);
[Item 3](../../domaene/items/beendenUndSperreOhneStelle.md) heißt „Beenden mit Kohärenz“,
AUF-10.1 bis 10.4, QUE-4, AUF-12.4 (neun); [Plan 5](../plan.md) Items, Reihenfolge und
Empfehlung: Der Rückfall auf Item 1 und 2 sperrt regelkonform.
