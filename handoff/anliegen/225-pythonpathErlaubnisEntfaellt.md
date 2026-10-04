# Ausnahmeerlaubnis PYTHONPATH aus 114 entfällt

225 · Anliegen · von Regelumsetzer → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** In [114](114-pruefskripteOrdnenUndLesbarMachen.md) F1 wolltest du eine
Ausnahmeerlaubnis `Bash(PYTHONPATH=prozess/pruefungen python3 *)`, nach der Abnahme zu entziehen.
Sie steht nicht in `.claude/settings.json`. Sie ist auch nicht mehr nötig: Jeder Aufruf läuft
über `prozess/pruefungen/gemeinsam/lauf.py <ordner>.<modul>`, ohne `PYTHONPATH`. Die Hook-Befehle,
`.pre-commit-config.yaml` und der Aufruf von Hand nutzen das; die bestehende Erlaubnis
`python3 prozess/pruefungen/*` genügt.

**Kosten.** Bliebe eine solche Erlaubnis später stehen, wäre sie eine Lücke für beliebiges
`PYTHONPATH`.

**Gegenvorschlag.** Die Erlaubnis wird nie angelegt; das ist der Entzug. Scheiter-Test:
`einstellungenTest.py` (`testKeineErlaubnisNenntPythonpath`, `testKeinHookBrauchtPythonpath`)
wird rot, sobald ein Hook oder eine Erlaubnis `PYTHONPATH` nennt.

**F1 · Ist damit die Ausnahme aus 114 erledigt?**
- a) Ja, du trägst `erledigt` ein.
- b) Nein, du willst `PYTHONPATH` trotzdem erlauben.
Empfehlung: a.
Antwort: .

**Stellungnahme.** Falls es nicht nötig ist, brauchen wir auch keine Ausnahme gestatten. Du kannst dieses Anliegen auf "erledigt" setzen.
