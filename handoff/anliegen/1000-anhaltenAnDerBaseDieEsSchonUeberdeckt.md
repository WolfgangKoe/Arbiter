# Anhalten an der Base, auf der ein Modell schon steht

1000 · Fragen · von Anforderungsautor → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Passt die *Formation* nirgends frei in deine Zone, steht sie trotzdem auf fremden
*Bases*, und du ziehst die *Modelle* frei (deine Antwort C in
[992](992-keineFreieStelleFuerDieFormation.md),
[AUF-27.1](../../domaene/anforderungen/phasen/aufstellen/formationOhneFreieStelle.md)). Beim
Ziehen hält Arbiter ein *Modell* oder den Block an der ersten *Base* an, an die es stößt
([AUF-26.2 und 26.3](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md)).
Ein *Modell*, das schon auf einer *Base* steht, stößt dort sofort an. Darum habe ich
[AUF-27.2](../../domaene/anforderungen/phasen/aufstellen/formationOhneFreieStelle.md) nach
ArbiterMap geschrieben: An der *Base*, die es schon *überdeckt*, hält Arbiter es nicht an
(`ArbiterMap/backend/app/domain/geometry.py:734`). Das hast du nicht entschieden.

Einordnung nach Ich 3: Der Fall liegt abseits deines Happy Path. Er wartet wie AUF-27 auf die
Domänenphase von Plan 7 ([999](999-itemsUndEtappeNach997Und992.md), Punkt 2) und hält Plan 6
nicht auf.

**Kosten.** Ohne Antwort gilt die Empfehlung. Antwortest du anders, ändert sich AUF-27, bevor
ein Test dazu entsteht.

**Gegenvorschlag.**

**F1 · Du ziehst ein Modell, das auf einer fremden Base steht.**
- A · Wie ArbiterMap: Diese *Base* hält es nicht an. Es folgt deinem Finger und bleibt dort, wo
  du loslässt, auch wenn es sie dort noch *überdeckt*. Jede andere *Base* hält es weiter an.
  ArbiterMap merkt sich eine bleibende Überdeckung, zeigt aber nichts
  (`ArbiterMap/backend/app/services/movement_service.py:178`). Empfehlung: Du ziehst die
  *Modelle* frei, wie du es in 992 gewählt hast, und es kostet am wenigsten.
- B · Ohne AUF-27.2: Das *Modell* bleibt an seiner *Stelle*, bis du es an eine *Stelle* ziehst,
  an der es keine *Base* mehr *überdeckt*; dort springt es hin. Eine Überdeckung wird nie
  größer, aber das *Modell* klebt fest, bis es frei ist. Den Block hält Arbiter an, solange
  eines seiner *Modelle* auf einer fremden *Base* bliebe.

Annahme: A, AUF-27.2 bleibt, wie es steht.
Antwort: A

**Stellungnahme.**
