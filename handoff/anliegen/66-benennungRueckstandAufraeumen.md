# Benennung: Rückstandsliste und Testmuster aufräumen

66 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** [Anliegen 32](32-benennungRueckstandInTechnik.md) ist nachgeprüft und erledigt.
Zwei Reste bei mir blieben liegen, weil der Auto-Mode-Klassifizierer die Änderung per Bash
als „Irreversible Local Destruction“ abgelehnt hat: die zwei Einträge in
`prozess/pruefungen/benennungRueckstand.txt` (wirkungslos) und das Muster `test_*.py` in
`pyproject.toml` (unter `technik/` gibt es keine solche Datei mehr).

**Kosten.** Tot gewordene Einträge und ein überflüssiges Muster; ein neues `test_*.py`
würde von pytest weiter gesammelt.

**F1 · Darf ich beide Reste entfernen?** Empfehlung: ja, mit Edit statt Bash; danach
`python3 -m pytest prozess/pruefungen` grün.
Antwort: .
