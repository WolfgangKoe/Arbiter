# pyproject.toml: Warum-Kommentare an ihrer Stelle, pytest mit fester Minor-Version

346 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code zu 814e21e ([216](216-commitHooksWirksamMachen.md)), dazu d3012e2
(Anliegen 304), weil der Organisationsentwickler die Stelle angemerkt hat.
1. `[tool.pytest.ini_options]`: Der Kommentar zu `stand` steht über dem zu `addopts`, die
   Zeile `markers`, die er erklärt, erst unter `addopts`. Zwei Warum stehen gestapelt über
   einer Zeile, eines davon gehört zu ihr nicht.
2. `[dependency-groups]`: „pre-commit (Hooks beim Commit)“ ist in die erste Zeile
   eingeschoben, sie hat jetzt 146 Zeichen, die Folgezeilen sind nicht umbrochen.
   „Hooks beim Commit“ sagt, was pre-commit tut, nicht warum die Version fest ist; der
   Grund dahinter („neue Regeln oder eine andere Zählweise“) passt auf ruff und complexipy,
   kaum auf pre-commit.
3. `pytest` steht als einziges Werkzeug ohne Version in `entwicklung`. pytest trägt aber
   Regeln dieser Datei: `testpaths`, `python_files`, `markers` und
   `--continue-on-collection-errors` ([Regeln](../../prozess/regeln.md#formregeln), 304), und
   er ist der Hook `pruefungen`. Beispiel: `.venv` hat pytest 9.1.1, das System-Python 9.0.3;
   dieselbe Konfiguration läuft heute schon unter zwei Versionen.

**Kosten.** 1 und 2: Wer die Datei liest, ordnet einen Grund der falschen Zeile zu oder
findet keinen; zwei Minuten Arbeit. 3: Ein Update von pytest kann das Sammeln oder den
Exit-Code bei Sammelfehlern still ändern, und die Sperre beim Commit hängt daran.

**Gegenvorschlag.** Die bestehende Regel deckt 3 ab: der Warum-Kommentar über
`entwicklung` (feste Minor-Version, damit ein Update nicht still etwas ändert); sie gilt
nur noch nicht für pytest.
1. Je Schlüssel steht sein Warum direkt darüber: `addopts` mit seinem Kommentar vor den
   Kommentar zu `stand`, dieser direkt über `markers`.
2. Der Kommentar über `entwicklung` nennt je Werkzeug den Grund und ist umbrochen wie die
   übrigen Kommentare der Datei (dort höchstens 104 Zeichen), etwa: ruff, complexipy, coverage und vulture
   (neue Regeln, andere Zählweise), pytest und pre-commit (Sammeln, Hooks und Exit-Code der
   Sperre), Playwright (Chromium-Build).
3. `pytest==9.1.*` in `entwicklung`.

Erledigt, wenn die drei Punkte in `pyproject.toml` stehen und
`python3 -m pytest prozess/pruefungen` sowie `python3 -m pytest technik/tests` grün sind.
Einen Test dafür verlange ich nicht.

**Stellungnahme.** Alle drei Punkte umgesetzt wie vorgeschlagen. Das System-Python hat pytest
9.0.3, `.venv` 9.1.1; die Datei verlangt nun 9.1.*, das System-Python bleibt bis zu einem
Update davon abweichend.
