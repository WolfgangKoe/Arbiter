# Backlog · Prozess

Zurückgestellt, bis ein Befund es auslöst. Was ausgelöst ist, wird ein Prozess-Item der Retro.

- Ausgelöst, Prozess-Item der Retro 2 (Stakeholder in Anliegen 90, F1 B; Entwurf dort, git):
  Dashboard aus ArbiterMap. Die Seite ist `dashboard.html` neben `domaene/`, `technik/` und
  `prozess/`; Daten und Skripte liegen in `prozess/dashboard/`, die Laufdaten nicht in git.
  Kein Plugin: Die Hooks stehen wie alle in `.claude/settings.json` und wirken nur hier.
  Der Regelumsetzer bekommt die Schreibpfade `dashboard.html` und `prozess/dashboard/` und
  überarbeitet die Seite.

- Grund- und Arbeitslast je Rolle messen (Probe, `PostToolUse` nach Artefakttyp,
  `VORGEHEN.md` E47). Auslöser: Belegung einer Rolle zweimal über 120.000 Token.
- Auslösezähler für Regeln, Rollen und Skills (E26). Auslöser: Retro 3, oder eine Regel
  steht im Verdacht, nie zu greifen.
- Prüfungen zu DoR 1 bis 5 und kursiven Begriffen gegen das Glossar (E35). Auslöser: ein Item
  geht mit einem dieser Mängel in die Technikphase.
- Werkzeuge der DoD ([Ablauf](ablauf.md#dod-item-fertig)) außer complexipy, ruff und
  Code → Glossar. Auslöser: Review oder Kritik am Code findet, was das Werkzeug meldet.
- Skills `anforderung-schreiben`, `regel-nachschlagen`, `improve` (E19, E30). Auslöser: dieselbe
  Kritik an derselben Art Artefakt zweimal.

Mechanismus: nur Text, Höchstmaß `prozess/kennzahlen.md` (Backlog je Perspektive).
