# conftest.py teilen

256 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Nach [251](251-hoechstmassFuerConftest.md) gilt für
`technik/tests/akzeptanz/conftest.py` das Maß für Code-Module, 12.000/8.000
(`prozess/kennzahlen.md`). Die Datei hat 13.700 Zeichen: Sie darf nicht weiter wachsen und
wird auf 8.000 geteilt. In ihr stehen drei Themen: Testdaten (Armeen, Ausgangslage), Abläufe
in der Aufstellung (Stellen einer Reihe, `Platz`, Einheiten aufstellen, Modelle setzen) und
Bildschirm (`Element`, `Bildschirm`, Browser).

**Kosten.** Bis zur Teilung kommt keine Fixture dazu, auch keine für die Items nach Plan 3;
die Prüfung dazu steht im Backlog und wäre ab dann rot. Teilen
heißt rund 6.000 Zeichen in zwei Module verschieben; die Testdateien bleiben, wie sie sind.

**Gegenvorschlag.** Neben `conftest.py` zwei Module ohne pytest, etwa `bildschirm.py`
(`Element`, `_elementeLesen`, `wartezeitInMillisekunden`, `Bildschirm`) und `handgriffe.py`
(Stellen, `Platz`, Aufstellen, Setzen, Sperrgründe). `conftest.py` behält nur die Fixtures und
importiert, etwa `from tests.akzeptanz.bildschirm import Bildschirm`. Das trägt ohne Eingriff
in `sys.path`: `technik/tests/` hat keine `__init__.py`, `tests` ist darum ein Namespace-Paket
im `pythonpath` aus `pyproject.toml` (probiert:
`PYTHONPATH=technik python3 -c "import tests.akzeptanz.conftest"`). Kein `pytest_plugins`:
pytest erlaubt es nur im obersten `conftest.py`. Die Namen der Module wählst du.

Erledigt, wenn `conftest.py` höchstens 8.000 Zeichen hat, jedes neue Modul höchstens
12.000, und `python3 -m pytest technik/tests` dieselben Tests sammelt wie vorher.

**Stellungnahme.** Angenommen und umgesetzt: `conftest.py` hat 5.646 Zeichen, `handgriffe.py` 5.595,
`bildschirm.py` 3.344. Gesammelt wird dasselbe wie vorher (61 Tests laufen oder scheitern wie
zuvor, aus fehlendem Code). Die Module heißen `tests.akzeptanz.handgriffe` und
`tests.akzeptanz.bildschirm`; `conftest.py` importiert sie. Offen: Die Benennungsprüfung
meldet beide Module (`<anforderung>Test.py`), siehe [257](257-hilfsmoduleImAkzeptanzordner.md).
