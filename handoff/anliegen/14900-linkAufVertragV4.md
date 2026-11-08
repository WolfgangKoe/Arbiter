# Link auf Vertrag V4 nach dem Teilen des Querschnitts

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält den Happy Path nicht auf. Nach [12993](12993-querschnittUeberDemHoechstmass.md)
ist `technik/architektur/vertrag/querschnitt.md` in den Ordner `vertrag/querschnitt/` geteilt.
[formregeln.md](../../prozess/regeln/formregeln.md), Zeile zu SonarLint, verlinkt „Vertrag V4“
noch auf die gelöschte Datei; V4 steht jetzt in
[anfragen.md](../../technik/architektur/vertrag/querschnitt/anfragen.md).

**Kosten.** Ein Link, eine Minute. Ohne ihn führt die Begründung der Ausnahme von
`python:S4502` ins Leere.

**Gegenvorschlag.** Link ersetzen durch
`../../technik/architektur/vertrag/querschnitt/anfragen.md`.

**Stellungnahme.** Umgesetzt: Der Link in [formregeln.md](../../prozess/regeln/formregeln.md)
zeigt auf `vertrag/querschnitt/anfragen.md`.
