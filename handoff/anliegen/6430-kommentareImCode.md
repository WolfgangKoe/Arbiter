# Kommentare im Code: sollten die nicht gelöscht werden?

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: 6431

## Runde 1
**Befund.** Wortlaut des Stakeholders:
„Ich finde immer noch viele Kommentare im Code, sollten die nicht gelöscht werden? -> Retro“

Festgehalten vom Organisationsentwickler. Beispiel: der einzeilige Docstring in
[anhaltenAnDerBewegungsweite.py](../../technik/arbiter/domaene/phasen/bewegung/anhaltenAnDerBewegungsweite.py),
Zeile 14. [Es 8](../../prozess/praemissen/es.md) erlaubt einzeilige Docstrings (Anliegen 1660,
1860), `formregeln/kommentare.py` prüft nur, dass sie einzeilig sind.

**Kosten.** Was ein Docstring sagt, muss der Name schon sagen; sonst veraltet es unbemerkt,
wie die Kommentare `# Regel:` aus Anliegen 1660.

**Gegenvorschlag.** Die [Retro 8](../retro.md) behandelt es; deine Wahl steht in
[Anliegen 6431](6431-fragenDerRetro8.md).

**Stellungnahme.**
