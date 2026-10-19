# Ein Modell loslassen, das nicht mehr gesetzt ist

930 · Fragen · von Anforderungsautor → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Ziehen kann man nur *gesetzte* *Modelle* auf der *Karte*
([AUF-8.2](../../domaene/anforderungen/phasen/aufstellen/ziehen.md)). Habt ihr Arbiter auf
zwei Seiten offen, zeigt die zweite ein *Modell* noch auf der *Karte*, das die erste schon
*zurückgelegt* hat, bis sie neu geladen wird (QUE-3.2). Zieht jemand es dort und lässt es los,
sagt kein Kriterium, was geschieht; heute *setzt* Arbiter es einfach
([923](923-unerreichbareFaelleInAuf12Und19.md), Punkt 2). Die Regeln sagen nichts; ArbiterMap
lehnt das Verschieben eines nicht aufgestellten *Modells* ab und ändert nichts
(`ArbiterMap/backend/app/services/movement_service.py:223`).

**Kosten.** Kein Schritt des Happy Path hängt daran; ich arbeite mit der Empfehlung weiter.
Antwortest du B, ändere ich AUF-16.7 vor seinem Test.

**Gegenvorschlag.**

**F1 · Was tut Arbiter, wenn jemand ein nicht *gesetztes* *Modell* auf der *Karte* loslässt?**
- A · Nichts: Jedes *Modell* steht, wo es vor dem Ziehen war, kein *Grund*, wie neben der
  *Karte* losgelassen (AUF-16.6). Empfehlung: wie ArbiterMap; nach dem Neuladen sieht die
  zweite Seite den wahren Stand.
- B · *Sperre* ‚nicht wählbar‘ mit *Grund*, das *Modell* springt zurück wie nach AUF-12.5.

Annahme: A, so steht es in [AUF-16.7](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md).
Antwort: A

**Stellungnahme.**
