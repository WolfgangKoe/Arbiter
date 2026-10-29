# Kriterium für Grenzkreise von Bewegung und Nahkampfreichweite

Form: Auftrag
Von: Ux
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder wünscht Grenzkreise für *Bewegungsweite* und *Nahkampfreichweite* ([Anliegen 6410](6410-grenzkreiseNahkampfUndBewegung.md)). Kein Kriterium nennt sie; Ux zeigt im Mockup nur, was ein Kriterium verlangt (Ich 1).

**Kosten.** Ohne Kriterium bleibt das Mockup aus oder wäre erfunden.

**Gegenvorschlag.** Ein Kriterium je Kreis: wann er erscheint (bei *ausgewählter* *Einheit*, bei *Vorrücken* auch bis *Bewegungsweite* plus *Vorrückwurf*), Radius aus Glossar und `domaene/daten/`. Vorbild: [ArbiterMap, Reichweiten](../../ArbiterMap/docs/spec/interaction_map.md), Abschnitt 5. Offen für den Stakeholder: ArbiterMap zeichnet alle sechs Vorrückringe vor; BEW-5 lässt den *Vorrückwurf* wählen. Empfehlung: nach der Wahl nur den Ring des Wurfs.

**Stellungnahme.** Umgesetzt in [BEW-11](../../domaene/anforderungen/phasen/bewegung/grenzkreise.md), Begriff *Grenzkreis* im [Glossar](../../domaene/glossar.md). Er erscheint bei *ausgewählter* *Einheit* des *Spielers* *am Zug* in der *Bewegungsphase* (11.1, 11.3), sonst nicht (11.4). Eigene *Modelle*: Mittelpunkt die *Stelle* zu Beginn der Phase wie bei der *Distanz*, Radius *Bewegungsweite* plus halber *Durchmesser*, weil von der *Base* aus gemessen wird (`core_rules.txt:464`, so auch `ArbiterMap/steering/backlog/items/013-spike-reichweiten-darstellung.md:78`); *vorgerückt* plus *Vorrückwurf* (11.2). *Modelle* des anderen *Spielers*: halber *Durchmesser* plus 1″. Die Werte stehen in `ausgangslage.yaml` und im Glossar, neue Daten braucht es nicht. Die Vorrückringe frage ich in [Anliegen 6998](6998-grenzkreiseVorrueckenUndBegriff.md) F1, deine Empfehlung als Annahme; wählt der Stakeholder B, folgt ein neues Kriterium.
