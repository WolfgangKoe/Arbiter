# Akzeptanztests: Importblock verletzt ruff (I001), sobald `arbiter` existiert

42 · Kritik · von Implementierer (Technik) → Testautor (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Mit `technik/arbiter/` erkennt ruff `arbiter` als eigenes Paket (`src` in
`pyproject.toml`) und verlangt in `technik/tests/akzeptanz/conftest.py` und
`technik/tests/akzeptanz/phasen/aufstellenTest.py` eine Leerzeile zwischen `import pytest` und
den `arbiter`-Importen. `testDasRepoIstRuffSauber` ist deshalb rot; die Akzeptanztests selbst
sind grün.

**Kosten.** Eine Leerzeile je Datei; ohne sie bleibt die Prüfung des Repos rot.

**Gegenvorschlag.** Beide Dateien mit `ruff check --fix` ordnen (nur I001).

**Stellungnahme.** Angenommen. In beiden Dateien steht eine Leerzeile zwischen `import pytest` und den `arbiter`-Importen. Prüfungen und Akzeptanztests laufen grün.
