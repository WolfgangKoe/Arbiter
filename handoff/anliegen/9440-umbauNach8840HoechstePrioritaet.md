# Umbau nach 8840 mit höchster Priorität planen

Form: Auftrag
Von: Stakeholder
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wortlaut des Stakeholders, auf die Frage, ob `Grund.überEineBase` jetzt aus dem
Code fällt (B) oder der Glossareintrag bleibt, bis das Item ihn entfernt (A):
„Okay, dann folge ich deiner Empfehlung A von vorhin und wir bauen es korrekt um. Bitte ein
Anliegen für die Domänenphase anlegen. Es hat höchste Priorität.“

Festgehalten vom Planer. Gemeint ist der Umbau nach
Anliegen 8840, wie in
Anliegen 9271 und
Anliegen 9320 geplant:
- Anhalten übergehen und Umbau der Tests, die ‚über eine Base‘ als Mittel nutzen: Item
  [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md);
- Anhalten vor fremden *Bases* und Entfernen von ‚über eine Base‘ aus dem Code: Item
  [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md);
- dabei bleibt die Ausnahme für *Modelle* derselben *Einheit*:
  Anliegen 9420.

Bis dahin bleibt der Glossareintrag zu ‚über eine Base‘ (A).

**Kosten.** Wie in 9271, Folgen.

**Gegenvorschlag.** Keiner.

**Stellungnahme.** Umgesetzt in [Plan 10](../plan.md): anhaltenUebergehen als Item 1,
loslassenNebenDerKarte als Item 2 (sonst spränge zurück, wer vor einer *Base* anhält und neben
der *Karte* loslässt), anhaltenAufDemWeg als Item 3; es entfernt ‚über eine Base‘ aus dem Code,
BEW-19 hält die Ausnahme aus 9420. Bis dahin bleibt der Glossareintrag (A). Folge: Etappe 2
endet mit Zyklus 11 (höchstens drei Items je Plan).
