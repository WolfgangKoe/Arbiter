# Keine freie Stelle für die Formation

992 · Fragen · von Anforderungsautor → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Wenn du in deine Zone klickst und die neue *Formation* eine stehende *Base*
überdecken würde, rückt Arbiter sie an die nächste freie Stelle
([AUF-18.7](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md), deine Antwort C
in [987](987-klickAufEineBaseUndAnhaltenBeimZiehen.md)). Offen ist, was passiert, wenn die Zone
so voll ist, dass die ganze *Formation* nirgends mehr hineinpasst. ArbiterMap prüft das nicht
(`ArbiterMap/backend/app/services/deployment_service.py:108`). Der Fall liegt abseits deines
Happy Path. Nach Ich 3 wartet er auf die Domänenphase von Plan 7, also dahin, wo auch AUF-18.7
gebaut wird ([Plan 6, Randfälle](../plan.md)).

**Kosten.** Ohne Antwort bleibt AUF-18.7 bei voller Zone unbestimmt, und kein Test kann
den Fall prüfen.

**Gegenvorschlag.**

**F1 · Die Formation passt nirgends in deiner Zone, ohne eine stehende Base zu überdecken.**
- A · Es kommt kein *Modell* dazu. Arbiter nennt den *Grund*, wie bei einem Klick, der gerade
  nicht geht ([AUF-19](../../domaene/anforderungen/phasen/aufstellen/gesperrterKlick.md)). Du
  ziehst dann einzelne *Modelle* oder stellst die *Einheit* in Reserve. Empfehlung: Es passt
  zu deiner Vorgabe „ein *Grund* bei einem Klick, der nicht geht“ in Plan 6, und keine *Base*
  steht je auf einer anderen.
- B · Es kommt kein *Modell* dazu, und Arbiter nennt keinen *Grund*. Das ist ruhiger, aber du
  weißt nicht, warum nichts geschieht.
- C · Wie ArbiterMap: Die *Formation* steht trotzdem auf der Stelle des Klicks, und du ziehst
  die *Modelle* frei. Eine Überdeckung bleibt, wenn du es vergisst.

Antwort: C

**Stellungnahme.**
