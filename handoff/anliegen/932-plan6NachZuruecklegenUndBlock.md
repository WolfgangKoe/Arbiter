# Plan 6 nach 890, 920 und 923: Kennungen und Sätze nachziehen

932 · Kritik · von Anforderungsautor → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, Item 2 nennt den Happy Path zum *Zurücklegen* und
Verschieben nicht mehr richtig. Geändert habe ich:
- Neu [AUF-24](../../domaene/anforderungen/phasen/aufstellen/blockAlsGanzes.md): 24.1 der Block
  schon beim Ziehen am Ziel (923, Punkt 4), 24.2 die *Modelle* der *Einheit* sperren einander
  beim Verschieben nicht ([920](920-blockSperrtSichAnDenEigenenVorigenStellen.md)).
- [AUF-23](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md): 23.1 neu
  gefasst, 23.2 neu ([890](890-zuruecklegenInGanzeEinheit.md), [931](931-zuruecklegenInEinzelmodelle.md)).
  Damit entfällt AUF-8.3 mit Test.
- AUF-18.4 gelöscht (ohne Test): Nach 890 hat keine *Einheit* *gesetzte* und nicht *gesetzte*
  *Modelle*, außer eines ist *gesperrt*, und dann sperrt AUF-12.1. AUF-14.1 entfällt damit
  ohne Nachfolger ([801](801-plan6KriterienDieEntfallen.md) nannte 18.4).
- AUF-19.4, 19.5, 12.5 gekürzt, 21.1 und 21.3 ohne neuen Inhalt; neu AUF-16.7
  ([930](930-modellLoslassenDasNichtMehrGesetztIst.md), abseits des Happy Path).

Veraltet sind damit: im Plan „ein zurückgelegtes *Modell* holt der nächste Klick einzeln
zurück“; in [Etappe 1](../../domaene/etappen/01-aufstellen.md) „zurücklegen, holen“ einzeln.
Dazu: AUF-10.2 und 10.5 (‚Modelle fehlen‘, übergangen: *vernichtet*) erreicht am Bildschirm
nichts mehr, denn jede *Einheit in Aufstellung* hat entweder alle *Modelle* *gesetzt* oder ein
*gesperrtes*, für das AUF-12.1 zuerst sperrt; die Etappe verlangt es noch.

**Kosten.** Ohne Nachziehen fehlen AUF-23.2 und AUF-24 in Item 2, AUF-8.3 bleibt mit einem
Test, der dem neuen *Zurücklegen* widerspricht, und Plan und Etappe versprechen ein Holen
einzelner *Modelle*, das es nicht gibt.

**Gegenvorschlag.** Item 2: AUF-23.2 und AUF-24 dazu, „Entfällt mit Test: AUF-8.3“. Item 1:
18.4 streichen, falls genannt, AUF-14.1 bleibt bei „entfällt“. Plan und Etappe ohne das
einzelne Holen und Zurücklegen; zu AUF-10.2 und 10.5 entscheidest du mit dem Stakeholder, ob
die Etappe sie weiter verlangt. AUF-16.7 planst du nach Nutzen. Erledigt, wenn Items, Plan und
Etappe den neuen Kennungen folgen oder du begründest, warum nicht.

**Stellungnahme.** Angenommen, umgesetzt.
[Item 2](../../domaene/items/einheitVerschieben.md) nimmt AUF-23 und AUF-24 und nennt „entfällt
mit Test, AUF: 8.3“, dazu die Mockups auf-23-sperre und auf-21 (933). Item 1 nannte 18.4 nicht
einzeln, AUF-14.1 bleibt bei „entfällt“. [Plan 6](../plan.md) und
[Etappe 1](../../domaene/etappen/01-aufstellen.md) sprechen nicht mehr vom einzelnen Holen und
Zurücklegen. Zu AUF-10.2 und 10.5 frage ich den Stakeholder in
[945](945-etappe1OhneFehlendeModelle.md). Bis er antwortet, gilt die Annahme A: Die Etappe
verlangt das Beenden mit fehlenden *Modellen* nicht mehr, und Plan 7 nennt 10.5 nicht. AUF-16.7
liegt abseits des Happy Path und kommt in Plan 7.
