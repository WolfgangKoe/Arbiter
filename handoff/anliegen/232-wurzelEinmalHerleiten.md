# Wurzel nur einmal herleiten; Starter-Test ist ein Stand-Test

232 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 4b492f5 (114 Teil A a), zwei Kleinigkeiten:

1. Die Wurzel des Repos wird an mehreren Stellen aus `__file__` neu berechnet, mit je eigener
   Tiefe: `conftest.py` (`parents[2]`), `standregeln/standTest.py` (`parents[3]`),
   `standregeln/kennzahlenTest.py` (`rsplit("/prozess/")`),
   `anliegenregeln/erledigteLoeschenTest.py` (`parents[1]`), `gemeinsam/lauf.py`
   (`parents[1]` für den Ordner der Prüfskripte), `formregeln/einstellungen.py`
   (`parents[1]` hinter `lauf.py`). Es gibt dafür schon `gemeinsam/pfade.py` (`wurzel`).
   Gerade dieser Umzug musste `hoechstmassTest` nachziehen, weil eine Tiefe nicht mehr
   stimmte. `konfigurationTest.py` ist ein Fall davon, der still falsch wurde (231).
2. `gemeinsam/laufTest.py`, `testDerStarterFindetQuerimporteOhnePythonpath`, lässt
   `formregeln.einstellungen` gegen das echte Repo laufen und verlangt Code 0. Er hängt also
   am Stand von `.claude/settings.json`, ist aber nicht mit `stand` markiert. Ein Hook auf ein
   fehlendes Skript macht ihn rot, mit einer Meldung über den Starter.

**Kosten.** (1) Bei jedem weiteren Umzug zählt man an jeder dieser Stellen die Ebenen nach, und ein
Fehler fällt nur auf, wenn ein Test zufällig daran hängt. „Jede Aussage steht genau einmal“
(CLAUDE.md). (2) Ein roter Starter-Test führt auf die falsche Spur. Er wird auch nicht
mitgemessen, obwohl `stand` laut `pyproject.toml` genau solche Prüfungen kennzeichnet.

**Gegenvorschlag.**
1. In `gemeinsam/pfade.py` steht neben `wurzel` ein Name für den Ordner der Prüfskripte,
   etwa `prüfskripteOrdner = wurzel / "prozess" / "pruefungen"`. `conftest.py`,
   `standTest.py`, `kennzahlenTest.py`, `erledigteLoeschenTest.py` und `konfigurationTest.py`
   nehmen ihn oder `wurzel`.
   `lauf.py` muss den Pfad vor dem ersten Querimport selbst kennen und bleibt die eine
   Ausnahme. `einstellungen.skripte` leitet die Moduldatei über eine Funktion in `lauf.py`
   her, statt den Weg nachzubauen. Mit 229 Punkt 1 gibt es diese Funktion ohnehin.
2. Der Starter-Test ruft ein Modul ohne Bezug zum Stand, etwa `gemeinsam.argumenteProbe`
   mit Querimport, oder er bekommt `@pytest.mark.stand`.

Erledigt, wenn `grep -rln __file__ prozess/pruefungen` nur noch `gemeinsam/pfade.py` und
`gemeinsam/lauf.py` trifft, `einstellungen.py` die Moduldatei aus `lauf.py` bezieht und `python3 -m pytest prozess/pruefungen`
grün ist.

**Stellungnahme.**
