# Klick neben eine stehende Einheit, Anhalten beim Ziehen

987 · Fragen · von Anforderungsautor → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Du willst, dass eine *Base* an einer anderen anhält wie in ArbiterMap
([984](984-klemmenStattSperreUndOhneAbzeichen.md)). Beim Ziehen ist das gebaut
(`ArbiterMap/backend/app/services/movement_service.py:299`, `:472`). Zwei Stellen weichen ab.

**Kosten.** Ohne Antwort gelten die Empfehlungen; antwortest du anders, ändern sich zwei
Kriterien vor dem Test.

**Gegenvorschlag.**

**F1 · Du klickst so nah an eine stehende Einheit, dass die neue sie überdecken würde.**
ArbiterMap prüft das beim Klick nicht: Die neue *Einheit* steht dann auf der anderen
(`ArbiterMap/backend/app/services/deployment_service.py:108`).
- A · Es erscheint nichts; du klickst weiter weg. Empfehlung: Keine *Base* steht je auf einer
  anderen, kein *Grund*, kein Knopf, kostet am wenigsten.
- B · Wie ArbiterMap: Sie steht auf der anderen, du ziehst sie weg. Eine Überdeckung bleibt,
  wenn du es vergisst.
- C · Arbiter rückt sie an die nächste freie Stelle in der Zone. Bequemer, kostet mehr.

Annahme: A ([AUF-18.7](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md)).
Antwort: C

**F2 · Was zeigt die Karte, wenn du ein einzelnes Modell in eine andere Base ziehst?**
- A · Es bleibt dort stehen, wo es auf dem geraden Weg anstößt, bis du es frei hinziehst; so
  landet es beim Loslassen. Empfehlung: dieselbe Regel wie für den Block, wenig Aufwand.
- B · Wie ArbiterMap gleitet es an der anderen *Base* entlang
  (`ArbiterMap/frontend/static/js/model_drag.js:186`); das hat dort mehrere Sitzungen gekostet.

Annahme: A ([AUF-26.4](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md)).
Antwort: A

**Stellungnahme.**
