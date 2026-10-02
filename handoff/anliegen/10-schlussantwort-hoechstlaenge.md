# Höchstlänge der Schlussantwort als Mechanismus

10 · Vorschlag · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Die Regel zur Schlussantwort ([CLAUDE.md](../../CLAUDE.md), Arbeitsweise) ist
nur Text. In Zyklus 1 kamen lange Schlussantworten, der Koordinator reichte sie inhaltlich
weiter.

**Vorschlag.** Ein Hook sperrt Schlussantworten über 800 Zeichen. Das reicht für Status und
rund zehn Pfade, nicht für eine Begründung.
- `prozess/pruefungen/schlussantwort.py` am vorhandenen `SubagentStop`: liest
  `last_assistant_message`; zu lang → `{"decision": "block", "reason": "Inhalte nach
  handoff/, hier nur Pfade und Status"}`. Die Rolle arbeitet weiter, legt den Inhalt ab und
  kürzt. Bei `stop_hook_active` sperrt er nicht erneut, sonst droht eine Schleife.
- Kommt der Bericht über ein Werkzeug (`SubagentHandback`, Feld `message`), prüft dasselbe
  Skript ihn als `PreToolUse` mit diesem Matcher. Welcher Weg greift, prüft der Regelumsetzer
  per Scheiter-Test.
- Schwelle als Konstante im Skript, Anpassung aus der Retro.

**Kosten.** Ein Skript mit Test (rund 40 Zeilen), ein Eintrag in `.claude/settings.json`,
Auftrag an den Regelumsetzer. Tokens nur beim Auslösen: eine Zusatzrunde der Rolle.

**Grenze.** Die Länge prüft nicht den Inhalt: eine kurze Frage passt durch. Dass der
Koordinator Pfade statt Inhalte weitergibt, bleibt nur Text; ein `Stop`-Hook auf ihn würde
auch das Gespräch mit dir kürzen. Erst beobachten, dann in der Retro entscheiden.

**Frage.** Soll der Regelumsetzer den Hook so bauen? Empfehlung: ja, mit 800 Zeichen.
