# Commit-Hooks prüfen, was der Commit berührt, und parallel

601 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 2/3 · erledigt

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
Umgesetzt (Regelumsetzer): Hooks `stand` (immer), `abdeckung` (bei `technik/`, `pyproject.toml`)
und `proben` (bei Prüfskripten, `.claude/` und Konfiguration) in `.pre-commit-config.yaml`;
`benennung` entfällt. Marke `abdeckung` am Abdeckungstest, der Test über `web/` in
`sonarlintTest.py` trägt jetzt `stand`. Scheiter-Test:
`prozess/pruefungen/formregeln/commitHooksTest.py`; Zeile in `prozess/regeln.md`
(Formregeln). Der Commit nur mit Texten braucht rund 4 Sekunden für den Stand.

## Runde 2
**Befund.** Nachgeprüft: `commitHooksTest.py` ist grün (12), der Stand braucht 3,8 Sekunden,
die Zeile in `prozess/regeln.md` steht. Ein Test über das echte Repo trägt aber kein `stand`:
`testRetroDesRepoNenntDenBefehl` in `rollenregeln/dashboardTest.py` liest
`handoff/retro.md`. Er läuft nur noch in `proben`, also nicht, wenn ein Commit nur die Retro
ändert. Die Zeile in `prozess/regeln.md` sagt „jeder Test über das echte Repo trägt `stand`“,
geprüft wird das nicht.

**Kosten.** Eine Retro ohne den Befehl zum Öffnen des Dashboards geht unbemerkt durch den
Commit; die Zeile in den Regeln verspricht mehr, als geprüft wird.

**Gegenvorschlag.** Gib `testRetroDesRepoNenntDenBefehl` die Marke `stand`. In der Zeile in
`prozess/regeln.md` steht hinter „jeder Test über das echte Repo trägt `stand`“ „nur Text“,
solange kein Test es prüft.

Erledigt, wenn `python3 -m pytest prozess/pruefungen -q -m "stand and not abdeckung"` den
Test sammelt und die Zeile in den Regeln „nur Text“ nennt.

**Stellungnahme.**
Übernommen: `testRetroDesRepoNenntDenBefehl` trägt `stand`; die Zeile in `prozess/regeln.md`
nennt „nur Text“ hinter der Zusage.
