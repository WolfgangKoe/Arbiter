# Abdeckungshook aus dem Commit-Hook nehmen

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** [Retro 6](../retro.md), P2 verlangt: Der Commit-Hook lässt die Produkttests aus.
Heute startet der Hook `abdeckung` in `.pre-commit-config.yaml` bei jeder Änderung in
`technik/` oder `pyproject.toml` alle Produkttests samt Messung. Mein Entfernen des Hooks hat
die Berechtigungsprüfung der Sitzung abgelehnt („CI Bypass“); ich habe es nicht umgangen.

**Gegenvorschlag.** Den Eintrag `- id: abdeckung` (fünf Zeilen) aus
`.pre-commit-config.yaml` streichen und `formregeln/commitHooksTest.py` anpassen
(`testEinCommitInTechnikStartetKeineProduktTests`). Die Abdeckung misst weiter der Lauf von
`python3 -m pytest prozess/pruefungen` beim Implementierer und beim Reviewer.

**Frage.** Darf der Regelumsetzer diese Änderung vornehmen? Annahme: ja (Empfehlung); alles
übrige von P2 ist fertig.
Kommentar: Ja

## Stellungnahme Regelumsetzer
Umgesetzt: Der Hook `abdeckung` ist aus `.pre-commit-config.yaml` gestrichen; ein Commit in
`technik/` oder an `pyproject.toml` startet keine Produkttests mehr. `stand` behält
`not abdeckung`, damit der Abdeckungstest im Commit nicht läuft. Scheiter-Test:
`testEinCommitInTechnikStartetKeineProduktTests` in `formregeln/commitHooksTest.py` (gegen die
alte Konfiguration rot, geprüft). Mutationstest entfällt: keine Zeile unter `technik/arbiter`
geändert. [Regeln](../../prozess/regeln.md) nachgezogen. Status bleibt angenommen bis zur Nachprüfung.
