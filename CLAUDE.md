# Arbiter

@domaene/ziel.md

## Drei Perspektiven
Domäne (`domaene/`: was das Produkt kann) · Technik (`technik/`: wie es gebaut ist) ·
Prozess (`prozess/`, `.claude/`: wie wir arbeiten). Ein Zyklus hat drei Phasen in dieser
Reihenfolge; in jeder arbeitet eine Perspektive, die anderen kritisieren.
`handoff/` richtet sich an den Stakeholder: Plan, Review, Retro, Anliegen.

## Arbeitsweise
- Schreibe nur im Ordner deiner Perspektive, lies alles.
- Kritik an einem fremden Artefakt wird eine Datei in `handoff/anliegen/`, nie eine Änderung.
  Kopf, Status und wer dann dran ist: `prozess/ablauf.md` (Anliegen).
- Fragen, Empfehlungen und Einschätzungen an den Stakeholder stehen als Datei in `handoff/`,
  nicht in der Schlussantwort. Die Schlussantwort einer Rolle nennt nur Pfade und Status; der
  Koordinator reicht Pfade weiter, keine Inhalte; er liest Dateien bis 4.000 Zeichen,
  `git show` nur mit `--stat`. Mechanismus:
  `prozess/pruefungen/schlussantwort.py`, `lesegrenze.py`.
- Jede Aussage steht genau einmal. Verlinke, statt zu wiederholen.
- Fachsprache = Codesprache = Deutsch. Ein Begriff aus der Anforderung steht wörtlich im
  Code und im Glossar (`domaene/glossar.md`, per grep). Benennung und Lesbarkeit von Code:
  `prozess/praemissen/wir.md`.
- Keine Historie in Dateien, git ist das Archiv.
- Erfinde nichts. Fehlt eine Regel oder Entscheidung, wird daraus ein Anliegen.

## Technik-Rahmen
Python und Flask, Frontend und Backend getrennt. Die Domäne kennt weder Flask noch die
Datenbank. Akzeptanztests entstehen vor dem Code.

## Nur lesbar
`VORGEHEN.md`, `handoff/kritik-entwickler.md`, `Arbiter/` und `ArbiterMap/` sind für alle
Rollen nur lesbar; löschen tut sie der Stakeholder. Mechanismus: `schreibgrenze.py`,
`bashPositivliste.py`. Was aus `VORGEHEN.md` gilt, steht an seinem Ort; Offenes:
[`prozess/backlog.md`](prozess/backlog.md).
