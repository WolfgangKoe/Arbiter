# Umbau nach 8840 mit höchster Priorität planen

Form: Auftrag
Von: Stakeholder
An: Planer
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 10

## Runde 1
**Befund.** Wortlaut des Stakeholders, auf die Frage, ob `Grund.überEineBase` jetzt aus dem
Code fällt (B) oder der Glossareintrag bleibt, bis das Item ihn entfernt (A):
„Okay, dann folge ich deiner Empfehlung A von vorhin und wir bauen es korrekt um. Bitte ein
Anliegen für die Domänenphase anlegen. Es hat höchste Priorität.“

Festgehalten vom Planer. Gemeint ist der Umbau nach
[8840](8840-baseNichtUeberdeckenAnhaltenStattSperre.md), wie in
[9271](9271-anhaltenVorFremdenBasesPlanen.md) und
[9320](9320-testsMitUeberEineBaseAlsMittel.md) geplant:
- Anhalten übergehen und Umbau der Tests, die ‚über eine Base‘ als Mittel nutzen: Item
  [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md);
- Anhalten vor fremden *Bases* und Entfernen von ‚über eine Base‘ aus dem Code: Item
  [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md);
- dabei bleibt die Ausnahme für *Modelle* derselben *Einheit*:
  [9420](9420-bew15ModelleDerselbenEinheit.md).

Bis dahin bleibt der Glossareintrag zu ‚über eine Base‘ (A).

**Kosten.** Wie in 9271, Folgen.

**Gegenvorschlag.** Keiner.

**Stellungnahme.**
