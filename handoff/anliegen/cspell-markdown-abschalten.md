# cSpell für Markdown abschalten braucht den Schreibpfad `.vscode/`

Von: Regelumsetzer (Prozess, ausführend). An: Organisationsentwickler.

## Befund
Der Stakeholder hat entschieden, cSpell für Markdown abzuschalten (VORGEHEN.md, Harness-Fakten).
Die Bordmittel von Claude Code reichen dafür nicht:
- cSpell ist eine VS-Code-Erweiterung. Keine Einstellung in `.claude/settings.json` steuert sie.
- Einzig vorhanden ist ein Deny auf `mcp__ide__getDiagnostics` und
  `mcp__claude-vscode__getDiagnostics`. Das sperrt alle Diagnosen, nicht nur die von cSpell
  für Markdown, und würde später auch ruff und mypy im Editor ausblenden. Ob es die automatisch
  angehängten Diagnosen nach einem Edit verhindert oder nur das Werkzeug, ist nicht dokumentiert.

## Mechanismus
`.vscode/settings.json` im Repo mit
`{"cSpell.enableFiletypes": ["!markdown"]}`
(`!markdown` nimmt den Dateityp aus der Prüfung, die übrigen Typen bleiben unverändert).
Scheiter-Test: `prozess/pruefungen/test_cspell.py` liest die Datei und verlangt den Eintrag.

## Blockiert
`.vscode/` liegt nicht in den `schreibpfade` des Regelumsetzers (`.claude/agents/regelumsetzer.md`),
die Schreibgrenze sperrt die Datei. Nötig: `.vscode/settings.json` in die `schreibpfade`
aufnehmen, danach setzt der Regelumsetzer Datei und Test um.

## Offen
Hängen die Diagnosen auch an Edits von Subagenten? Nicht belegt. Die Doku nennt nur das
Werkzeug `getDiagnostics`, das ein Agent mit diesem Werkzeug selbst aufruft. Prüfbar mit einem
Subagenten, der eine Markdown-Datei ändert, solange cSpell noch aktiv ist.

## Stellungnahme (Organisationsentwickler)
Angenommen, vom Stakeholder freigegeben: `.vscode/settings.json` steht in den `schreibpfade`
des Regelumsetzers. Nächster Schritt: Regelumsetzer baut Datei und Test, prüft nach und
löscht dieses Anliegen.
