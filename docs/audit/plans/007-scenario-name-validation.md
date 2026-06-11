# Plan 007: Scenario-Namen gegen Allowlist validieren (Pfad-Traversal schließen)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat 225d13b..HEAD -- src/gameMechanic/scenarios.py src/app.py`
> Wenn sich diese Dateien seit Plan-Erstellung geändert haben, vergleiche die
> „Current state"-Auszüge mit dem Live-Code; bei Abweichung: STOP.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: security
- **Planned at**: commit `225d13b`, 2026-06-11

## Why this matters

Die App akzeptiert `?scenario=<name>` als URL-Query-Parameter und baut daraus
ungeprüft einen Dateipfad (`data/scenarios/<name>.json`). Mit `?scenario=../...`
lässt sich auf JSON-Dateien außerhalb des Scenario-Ordners zeigen. Der Inhalt wird
dem Angreifer nicht zurückgegeben und die Datei muss serverseitig existieren —
die reale Auswirkung ist also begrenzt. Aber die App läuft auf einem öffentlichen
Hugging-Face-Space, und der Riegel kostet drei Zeilen: Defense-in-Depth.

`save_scenario` hat aktuell **keinen** Produktions-Caller in `src/` (nur
`load_scenario` wird aus `app.py` aufgerufen) — es wird trotzdem mit validiert,
damit ein künftiger Caller die Lücke nicht wieder öffnet.

## Current state

- `src/app.py:24-29` — der einzige web-exponierte Einstieg:

```python
_scenario = st.query_params.get("scenario")
if _scenario and "scenario_loaded" not in st.session_state:
    from gameMechanic.scenarios import load_scenario  # noqa: PLC0415

    load_scenario(_scenario)
    st.session_state.scenario_loaded = True
```

- `src/gameMechanic/scenarios.py:14-19` — ungeprüfte Pfad-Konstruktion:

```python
def get_scenario_data(name: str) -> dict[str, Any] | None:
    """Return parsed scenario JSON or None if not found."""
    path = _SCENARIOS_DIR / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())  # type: ignore[no-any-return]
```

- `src/gameMechanic/scenarios.py:87-105` — `save_scenario` schreibt mit
  unvalidiertem Namen: `(_SCENARIOS_DIR / f"{name}.json").write_text(...)`.
- `load_scenario` (Zeile 72) ruft `get_scenario_data(name)` auf und gibt bei
  `None` bereits `False` zurück — die Validierung in `get_scenario_data` deckt
  den Lese-Pfad damit vollständig ab, `app.py` braucht keine Änderung.
- Bestehende Scenario-Dateien (alle passen zur Allowlist unten):
  `charge_phase`, `command_phase`, `fight_phase`, `morale_phase`,
  `movement_phase`, `necrons_fight_orks`, `necrons_shoot_orks`,
  `orks_fight_necrons`, `orks_shoot_necrons`, `psychic_phase`, `shooting_phase`.
- Tests: `tests/gameMechanic/test_scenarios.py` existiert und testet v. a. das
  Streamlit-freie `apply_scenario`; `get_scenario_data` ist ebenfalls
  Streamlit-frei und direkt testbar.

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Lint | `ruff check src/` | passt |
| Scenario-Tests | `python -m pytest tests/gameMechanic/test_scenarios.py -q` | grün |
| Vollsuite + Coverage-Gate | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `src/gameMechanic/scenarios.py` — Validierung in `get_scenario_data` und
  `save_scenario`
- `tests/gameMechanic/test_scenarios.py` — neue Tests

**Out of scope** (NICHT anfassen):
- `src/app.py` — braucht keine Änderung (siehe Current state).
- `load_scenario`/`apply_scenario` — Logik unverändert.
- Kein Umbau auf `path.resolve().relative_to(...)` — die Allowlist ist strenger
  und einfacher.

## Git workflow

- Branch: `advisor/007-scenario-name-validation`.
- Commit-Stil imperativ Englisch, z. B. `Validate scenario names against allowlist`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Allowlist-Regex + Validierung einbauen

In `src/gameMechanic/scenarios.py`:

1. Oben `import re` ergänzen (alphabetisch in den stdlib-Import-Block, isort-konform).
2. Unter `_SCENARIOS_DIR` die Konstante definieren:

```python
_VALID_NAME = re.compile(r"^[A-Za-z0-9_-]+$")
```

3. `get_scenario_data` — als erste Zeile der Funktion:

```python
    if not _VALID_NAME.fullmatch(name):
        return None
```

4. `save_scenario` — als erste Zeile der Funktion:

```python
    if not _VALID_NAME.fullmatch(name):
        raise ValueError(f"Invalid scenario name {name!r}: only [A-Za-z0-9_-] allowed.")
```

Begründung der Asymmetrie: Der Lese-Pfad ist web-exponiert und soll sich wie
„nicht gefunden" verhalten (kein Fehler-Oracle für Angreifer); der Schreib-Pfad
ist ein Entwickler-Werkzeug und soll laut scheitern.

**Verify**: `ruff check src/` → passt;
`python -m pytest tests/gameMechanic/test_scenarios.py -q` → bestehende Tests grün.

### Step 2: Tests ergänzen

In `tests/gameMechanic/test_scenarios.py` (Strukturvorlage: bestehende Tests
derselben Datei; `import pytest` ggf. ergänzen):

```python
def test_get_scenario_data_rejects_path_traversal() -> None:
    from gameMechanic.scenarios import get_scenario_data

    assert get_scenario_data("../rosters/necrons_alpha") is None
    assert get_scenario_data("..") is None
    assert get_scenario_data("a/b") is None
    assert get_scenario_data("") is None


def test_get_scenario_data_accepts_valid_names() -> None:
    from gameMechanic.scenarios import get_scenario_data

    # Existierendes Scenario lädt weiterhin
    assert get_scenario_data("shooting_phase") is not None
    # Valider, aber nicht existenter Name → None (kein Crash)
    assert get_scenario_data("does-not-exist_123") is None


def test_save_scenario_rejects_invalid_name() -> None:
    from gameMechanic.scenarios import save_scenario

    with pytest.raises(ValueError, match="Invalid scenario name"):
        save_scenario("../evil")
```

Hinweis: `save_scenario` greift erst NACH der Validierung auf
`st.session_state` zu — der Test braucht daher kein Streamlit-Setup, die
Exception kommt vorher.

**Verify**: `python -m pytest tests/gameMechanic/test_scenarios.py -q` → grün
inkl. 3 neuer Tests.

### Step 3: Vollsuite

**Verify**: `pytest --tb=short` → alle Tests grün (Baseline bei Plan-Erstellung 767,
+3 neue aus diesem Plan; durch andere abgeschlossene Pläne kann die Zahl höher liegen),
Coverage ≥ 80 %.

## Test plan

- Traversal-Namen (`../…`, `a/b`, leer) → `None` aus `get_scenario_data`.
- Valider existierender Name → lädt weiterhin (Regression).
- Valider nicht-existenter Name → `None` (Verhalten unverändert).
- `save_scenario` mit Traversal-Namen → `ValueError` vor jedem Dateizugriff.
- Strukturvorlage: bestehende Tests in `tests/gameMechanic/test_scenarios.py`.

## Done criteria

ALLE müssen gelten:

- [ ] `grep -n "_VALID_NAME" src/gameMechanic/scenarios.py` → 3 Treffer
  (Definition + 2 Verwendungen)
- [ ] 3 neue Tests vorhanden und grün
- [ ] `pytest --tb=short` → alle grün, Coverage-Gate erfüllt
- [ ] `ruff check src/ && black --check src/ && isort --check-only src/` → passt
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- Ein bestehender Test rot wird (z. B. weil er Scenario-Namen mit Sonderzeichen
  verwendet) — Repo-Regel: rote Tests = STOP, Nutzer fragen.
- Sich herausstellt, dass `save_scenario` doch einen Produktions-Caller hat, der
  Namen mit anderen Zeichen übergibt (mit `grep -rn "save_scenario" src/` prüfen).
- Es Scenario-Dateien gibt, deren Name NICHT zur Allowlist passt
  (`ls data/scenarios/` prüfen) — dann Regex-Anpassung melden statt raten.

## Maintenance notes

- Wer künftig Scenario-Namen mit neuen Zeichen braucht (z. B. Punkte), muss die
  Allowlist bewusst erweitern — das ist Absicht, nicht Versehen.
- Reviewer: prüfen, dass die Validierung VOR jedem Dateisystem-Zugriff steht.
- Bewusst nicht gemacht: `save_scenario` aus der Codebasis entfernen, obwohl es
  keinen Produktions-Caller hat — es ist als Dev-Werkzeug dokumentiert
  („Snapshot the current game state").
