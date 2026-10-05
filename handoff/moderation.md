# Moderation

Stand: Zyklus 3, Prozessphase, 39 Anliegen-Dateien; nächster Schritt Retro 3.

## Dran
Blockiert das Inkrement: nichts. Plan 4 baut auf der Komponentenseite aus
[262](anliegen/262-komponentenseiteOhnePruefung.md) auf; dessen Nachprüfung ist fällig.
- Organisationsentwickler: Retro 3; [282](anliegen/282-schichtenInEsUndAblauf.md); 107 (Antwort des
  Stakeholders: noch keine Reaktion), 150 (Antwort: SonarLint scharfstellen), 138, 219.
- Regelumsetzer (27): 253 Punkte 5, 7; 240 Runde 2; 268; 272 bis 276, 278; 281; 246, 247, 249;
  215, 216, 218, 220, 221, 228 bis 232; 202 bis 206.
- Architekt: Nachprüfung 262, 265. Reviewer: Nachprüfung 270, 279; Kritik an 9d6514a.
- Stakeholder: Fragen unten. Testautor, Anforderungsautor, Planer: nichts offen.

## Vorschläge
Stränge nach [Ablauf, Gleichzeitige Läufe](../prozess/ablauf.md#gleichzeitige-läufe). Vor jedem
Start `git status` gegen die Dateien des Nachbarn prüfen.

Regelumsetzer, drei Stränge gleichzeitig:
1. Kette (Hook-Code, höchstens ein Lauf): 253 P5 → P7 → 281 → 272 → 278 → 273 → 274 → 276 (nach
   268) → 275 mit 246; danach 215, 218, 220 (ebenfalls Hooks).
   281 und 272 prüfen beide die Schichten; ein Lauf, wenn die Dateien dieselben sind.
2. Linter, kein Hook: 268 (`eslint.config.mjs`, `frontendTest.py`; Schreibpfad hängt an F2 in 279),
   240 Runde 2 (Status klären, Commit 973cb7b liegt vor). 276 wartet auf 268.
3. Prüfskript-Werkzeug, kein Hook: 229 mit 232, dann 231 mit 247 (`konfigurationTest.py`), 228 mit
   230, 249; daneben 221 und 202 bis 206 (204 mit 205), solange ihre Dateien frei sind. 216 erst
   nach der Kette.

Reviewer: Nachprüfung 270, 279 und Kritik 9d6514a gleichzeitig (nur Anliegen); danach je Lauf der
Kette Kritik am Code. 279 wartet auf F1, F2.
Architekt: Nachprüfung 262, 265 gleichzeitig mit allen anderen; später Kritik an
Linter-Konfiguration aus Strang 2.
Organisationsentwickler: Retro 3 (`retro.md`) und 282 (`ablauf.md`, `es.md`) gleichzeitig, Dateien
getrennt. 282 deckt dieselben Pfadzeilen wie [281](anliegen/281-schichtenLassenKreiseUndUnterordnerDurch.md)
Befund 1 und 2 in `regeln.md`; das Anliegen trägt je Rolle ihre Datei. Schließen: 107, 226 nach
253; 138 nach 215; 219 nach 220; 150 nach 216 und Antwort auf 280.
Ablegen: 267 ist erledigt, die Datei geht von selbst. 153 ist gelöscht und nicht mehr offen.

## Fragen an dich
- [279](anliegen/279-gleicheRolleParallel.md) F1: Worktree je Lauf jetzt (Empfehlung: nein).
- 279 F2: darf der Regelumsetzer `eslint.config.mjs`, `.stylelintrc.json`, `package.json`,
  `package-lock.json` schreiben (Empfehlung: ja); blockiert 268 und 276.
- [280](anliegen/280-sonarlintPrueftNurPython.md) F1: soll `sonarlint.py` das Frontend prüfen
  (Empfehlung: nein, Node ≥ 22.12 wäre Voraussetzung).
