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
  Kopf: Von <Rolle> an <Rolle> · Runde <n>/3; je Runde Befund, Kosten, Gegenvorschlag,
  Stellungnahme.
- Fragen, Empfehlungen und Einschätzungen an den Stakeholder stehen als Datei in `handoff/`,
  nicht in der Schlussantwort. Die Schlussantwort einer Rolle nennt nur Pfade und Status; der
  Koordinator reicht Pfade weiter, keine Inhalte. Mechanismus:
  `prozess/pruefungen/schlussantwort.py`, `lesegrenze.py`.
- Jede Aussage steht genau einmal. Verlinke, statt zu wiederholen.
- Fachsprache = Codesprache = Deutsch. Ein Begriff aus der Anforderung steht wörtlich im
  Code und im Glossar (`domaene/glossar.md`, per grep).
- Keine Historie in Dateien, git ist das Archiv.
- Erfinde nichts. Fehlt eine Regel oder Entscheidung, wird daraus ein Anliegen.

## Technik-Rahmen
Python und Flask, Frontend und Backend getrennt. Die Domäne kennt weder Flask noch die
Datenbank. Akzeptanztests entstehen vor dem Code.

## Übergang
Entscheidungen aus dem Aufbau stehen in `VORGEHEN.md`, bis sie an ihren Ort überführt sind.
