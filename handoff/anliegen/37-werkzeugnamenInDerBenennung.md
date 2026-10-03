# Benennung: Namen, die ein Werkzeug vorgibt

37 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** [wir.md](../../prozess/praemissen/wir.md) sagt: „Namen, die ein Werkzeug
vorgibt (`conftest.py`, `__init__`, …), bleiben.“ `benennung.py` setzt das nur für Dateinamen,
Dunder-Namen und `werkzeugnamen = {"tmp_path", "tmp_path_factory"}` um. Alles andere, was ein
Werkzeug über den Namen findet, ist ein Verstoß; geprüft mit `quelltextVerstöße`:
`def pytest_configure(config)` in `conftest.py` → „nicht in camelCase“.

Die Folge steht schon im Code: `prozess/pruefungen/conftest.py` löscht die erledigten
Anliegen als Nebenwirkung beim Import, weil der Hook `pytest_configure` „nicht in camelCase
wäre“ (Docstring). Code, der beim bloßen Import Dateien löscht, ist schwer zu lesen und
läuft bei jedem Import mit, nicht erst, wenn pytest ihn ruft. Die Prüfung ist hier
strenger als die Prämisse, und der Autor hat um sie herum gebaut.

**Kosten.** Das trifft bald die Technik: Ein Akzeptanz- oder Bildschirmtest, der einen
pytest-Hook braucht (`pytest_collection_modifyitems`, `pytest_generate_tests`), muss
ebenso tricksen oder bleibt rot. Jeder Trick ist eine Stelle, an der der Name nicht mehr
sagt, was passiert.

**Gegenvorschlag.** In `conftest.py` sind Funktionen `pytest_<hook>` Werkzeugnamen, mit
Scheiter-Test (ein `pytest_irgendwas` außerhalb von `conftest.py` bleibt rot). Danach
kann `prozess/pruefungen/conftest.py` den Hook nutzen. Weitere Werkzeugnamen erst, wenn
Code sie braucht: Flask lässt sich ohne vorgegebene Namen einrichten
(`app.config.from_mapping(SECRET_KEY=…)` statt Großbuchstaben-Attributen, `--app` statt
`create_app`), dafür reicht die Prüfung, wie sie ist.

**Stellungnahme.**
