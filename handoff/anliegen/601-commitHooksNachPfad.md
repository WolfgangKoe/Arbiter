# Commit-Hooks prüfen, was der Commit berührt, und parallel

601 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Ein Commit wartet 7 bis 8 Minuten auf die Prüfungen. Messung und Ursachen
stehen in Anliegen 600: Die Abdeckung über das echte Repo braucht 1:40, drei SonarLint-Proben
1:05, die übrigen 599 Prüfungen 54 Sekunden. Der Hook `benennung` wiederholt
`testDasRepoHältDieBenennung` aus `pruefungen`.

**Kosten.** Wie in Anliegen 600: Stunden je Zyklus und ein Anreiz, im Hintergrund zu
committen (Anliegen 610).

**Gegenvorschlag.** Beginne erst, wenn der Stakeholder Anliegen 600 beantwortet hat. Es gilt,
was er wählt; F1 und F3 (Runde 2) betreffen nur Texte von Koordinator und Ablauf, das
übernehme ich.
- Bei F2 A: Mit den Bordmitteln von pre-commit (`files:` je Hook) wird `pruefungen` geteilt:
  1. Stand, immer: die Tests mit Marke `stand` ohne die Abdeckung über das echte Repo.
  2. Abdeckung: nur bei `^(technik/|pyproject\.toml)`.
  3. Proben der Prüfskripte (ohne Marke `stand`): nur bei `prozess/pruefungen/`,
     `pyproject.toml`, `.pre-commit-config.yaml` oder Linter-Konfiguration.
  Der Hook `benennung` entfällt. Eine Marke für die Abdeckung legst du fest. Prüfe, dass
  jeder Test über das echte Repo `stand` trägt; sonst fiele er in Text-Commits aus.

Erledigt, wenn ein Scheiter-Test über `.pre-commit-config.yaml` (wie
`formregeln/konfigurationTest.py`) zeigt: Ein Commit nur in `handoff/` startet weder
Abdeckung noch Proben, einer in `technik/` startet die Abdeckung, einer in
`prozess/pruefungen/` die Proben. Außerdem stehen die Zeilen in `prozess/regeln.md`.

**Stellungnahme.**
