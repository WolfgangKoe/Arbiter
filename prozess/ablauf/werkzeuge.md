# Werkzeuge

Der Regelumsetzer baut sie, der Architekt kritisiert: complexipy (Schwelle 15), ruff (Stil,
ARG, PLR2004, PLR0913, FBT, ERA, `PLR0912` mit 12), eslint und stylelint fürs Frontend. Die Sperre der Agenten ist für Python mindestens so
streng wie SonarLint, die Sicht des Stakeholders; Mechanismus: `formregeln/sonarlint.py` ([DoD 2](dod.md)).
SonarLint prüft nur Python, das Frontend prüfen eslint und stylelint (Anliegen 280). Nicht verwendet: ruff format (Anliegen 1581), radon-Wartbarkeitsindex,
ruff-McCabe, ruff `PLR0911` (meldet frühes `return`).
