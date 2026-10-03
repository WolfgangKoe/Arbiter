# Ruff prüft nichts, und der eigene Code wäre rot

35 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Die Regel „Ruff nach E37“ in [regeln.md](../../prozess/regeln.md) hat keinen
wirksamen Mechanismus:
1. ruff ist nicht installiert, pre-commit auch nicht (`.git/hooks/pre-commit` fehlt). Die
   [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) läuft also nie, und der einzige
   ruff-Test in `konfigurationTest.py` wird übersprungen (`skipif`). Das Gate des
   Koordinators, `python3 -m pytest prozess/pruefungen`, bleibt grün, ohne ruff je zu rufen.
   Wo ruff nicht installiert ist, ist auch DoD 2 („ruff grün“) nicht prüfbar.
2. Wegwerf-Versuch mit ruff 0.16 in einer eigenen venv, mit dieser `pyproject.toml`:
   `prozess/` und `.claude/` haben 12 Verstöße. 9 × I001: ruff kennt `benennung`,
   `agenten` usw. nicht als eigene Module und sortiert `import benennung` zu den fremden
   Paketen; mit `src = ["prozess/pruefungen", "technik"]` unter `[tool.ruff]` sind alle 9
   weg (geprüft). 3 × E501 in `statusrecht.py` und `statusrechtTest.py`.
3. N818 fehlt in `ignore`. `aufstellenTest.py` erwartet `pytest.raises(Sperre)`; der
   Implementierer schreibt also `class Sperre(Exception)`, und ruff verlangt
   `SperreError` (geprüft). Deutsche Namen enden nie auf „Error“; die Regel widerspricht
   dem Glossar so wie N802 bis N816 der Prämisse.

**Kosten.** Ohne Mechanismus merkt keiner die Verstöße, bis jemand ruff installiert; dann
ist alles auf einmal rot, auch Code, auf den andere schon aufbauen. Der erste Fall ist da:
Dein eigener Code verstößt, unbemerkt. Bei 3 bekäme jede Ausnahme des Produkts einen
englischen Anhang oder ein `noqa`.

**Gegenvorschlag.**
1. Abhängigkeiten in `pyproject.toml` nennen, mit fester Version, damit ruff nicht mit
   jedem Update neue Regeln bringt:
   `[dependency-groups]` `entwicklung = ["pytest", "ruff==0.16.*"]`. Installieren muss sie
   der Stakeholder einmal; darum ein Satz in `handoff/`, sobald es soweit ist.
2. Im Gate statt `skipif`: ein Test „das Repo ist ruff-sauber“, der rot ist, wenn ruff
   fehlt. Er prüft alles außer den Dateien, die `benennung.rückstand()` heute schon
   ausnimmt (`conftest.py`, `test_auf_1.py`, zusammen 13 Verstöße); so gilt ein
   Rückstand für beide Prüfungen, und neue Dateien sind nie ausgenommen.
3. `src` wie oben, `N818` in `ignore` mit derselben Begründung wie die anderen N-Regeln;
   die drei langen Zeilen kürzen.
4. pre-commit: entweder `pre-commit install` als Teil der Einrichtung, oder die Datei
   streichen und in `regeln.md` nur das pytest-Gate nennen. Heute nennt `regeln.md` zwei
   Mechanismen, von denen einer nie läuft.

**Stellungnahme.** Angenommen, umgesetzt: Punkt 1 (`dependency-groups`, `ruff==0.16.*`), 2 (`testDasRepoIstRuffSauber`, rot ohne ruff, mit Rückstand aus `benennungRueckstand.txt`), 3 (`src`, N818, lange Zeilen gekürzt, `ARG001` in `conftest.py` behoben). Punkt 4: Der ruff-Hook in `.pre-commit-config.yaml` entfällt, das pytest-Gate deckt ihn ab; die übrigen Hooks laufen nur nach `pre-commit install`. Folge: Ohne ruff im PATH ist das Gate rot, bis der Stakeholder einmal `pip install --group entwicklung` (oder `pip install ruff==0.16.*`) ausführt; mit ruff 0.16.10 sind alle 284 Prüfungen grün. Das braucht eine Entscheidung des Stakeholders.
