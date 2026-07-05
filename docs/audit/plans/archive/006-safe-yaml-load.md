# Plan 006: Alle `yaml.safe_load`-Aufrufe durch einen Helper mit klarer Fehlermeldung ersetzen

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat 225d13b..HEAD -- src/gameObjects/loader.py src/gameMechanic/game_state.py`
> Wenn sich diese Dateien seit Plan-Erstellung geändert haben, vergleiche die
> „Current state"-Auszüge mit dem Live-Code; bei Abweichung: STOP.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: bug
- **Planned at**: commit `225d13b`, 2026-06-11

## Why this matters

Die App lädt alle Spieldaten (Einheiten, Waffen, Rosters, Fähigkeiten) aus
YAML-Dateien. 19 `yaml.safe_load`-Aufrufe (17 in `loader.py`, 2 in `game_state.py`)
laufen ohne jede Fehlerbehandlung: Eine syntaktisch kaputte oder abgeschnittene
YAML-Datei wirft `yaml.YAMLError` als rohen Stacktrace in die Streamlit-UI, **ohne
die betroffene Datei zu benennen**. Der Nutzer editiert Roster-YAML von Hand —
dieser Fall ist realistisch. Nach diesem Plan nennt der Fehler die Datei und die
Parse-Position im Klartext.

**Design-Entscheidung (bewusst):** Laut scheitern, nicht still degradieren. Eine
kaputte Datendatei soll einen klaren Fehler erzeugen, kein leeres Spiel. Das ist
konsistent mit der jüngsten Repo-Linie (Commit `7dd1f17`, „Raise clear error when
lookup finds no unit"). Es wird also KEIN Default-Rückgabewert eingeführt.

## Current state

- `src/gameObjects/loader.py` — 17 Aufrufstellen in den Zeilen 83, 383, 389, 421,
  442, 476, 488, 498, 513, 569, 580, 719, 737, 782, 827, 852, 943. Muster überall
  identisch (teils mit `or []` / `or {}` für leere Dateien):

```python
# loader.py:82-83 (repräsentativ)
    with open(path) as f:
        data = yaml.safe_load(f)
```

```python
# loader.py:568-569 (Variante mit Default für leere Datei)
    with open(path) as f:
        data = yaml.safe_load(f) or []
```

- `src/gameMechanic/game_state.py:93-97` — 2 Aufrufstellen:

```python
    with open(pts_path) as f:
        pts_data = yaml.safe_load(f) or {}
    units_pts: dict[str, dict] = pts_data.get("units") or {}
    with open(roster_path) as f:
        roster_data = yaml.safe_load(f) or {}
```

- `game_state.py` importiert bereits aus `gameObjects.loader` (Import-Block oben in
  der Datei) — ein weiterer Import von dort ist konventionskonform.
- Die `if not path.exists(): return …`-Guards VOR den Aufrufen bleiben unverändert —
  fehlende Dateien sind ein anderer (bereits behandelter) Fall als kaputte Dateien.

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Lint | `ruff check src/` | passt |
| Loader-Tests | `python -m pytest tests/gameObjects/test_loader.py -q` | grün |
| Vollsuite + Coverage-Gate | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `src/gameObjects/loader.py` — Helper hinzufügen, 17 Aufrufstellen umstellen
- `src/gameMechanic/game_state.py` — 2 Aufrufstellen umstellen
- `tests/gameObjects/test_loader.py` — neue Tests für den Helper

**Out of scope** (NICHT anfassen):
- `src/uiLayout/armyList.py` — dessen `try/except Exception` um
  `load_faction_abilities` bleibt wie es ist (separates Thema, Plan 012).
- Jegliche UI-Behandlung des neuen Fehlers (z. B. `st.error` im Setup-Screen) —
  bewusst aufgeschoben, siehe Maintenance notes.
- `tools/` (Scraper) — eigene YAML-Aufrufe dort sind lokale Dev-CLIs.

## Git workflow

- Branch: `advisor/006-safe-yaml-load`.
- Commit-Stil imperativ Englisch, z. B. `Wrap YAML loading in clear data errors`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Helper + Exception-Klasse in `loader.py` einführen

Füge in `src/gameObjects/loader.py` direkt unter den Modul-Konstanten
(`_ROUND_CHOICE_LABEL_CACHE`, ~Zeile 30) ein:

```python
class YamlDataError(ValueError):
    """A game data YAML file exists but cannot be parsed."""


def load_yaml(path: Path) -> Any:
    """Parse a YAML file, raising YamlDataError with the file path on syntax errors."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise YamlDataError(f"Invalid YAML in {path}: {exc}") from exc
```

`Path` und `Any` sind in `loader.py` bereits importiert.

**Verify**: `python -c "from gameObjects.loader import load_yaml, YamlDataError"` —
ausgeführt mit `PYTHONPATH=src` bzw. wie die Tests es tun (`cd` ins Repo-Root reicht,
pytest-Konfiguration setzt den Pfad): `python -m pytest tests/gameObjects/test_loader.py -q --co | head -3` → sammelt ohne ImportError.

### Step 2: Alle 17 Stellen in `loader.py` umstellen

Ersetze jedes Vorkommen des Zwei-Zeilen-Musters

```python
    with open(path) as f:
        data = yaml.safe_load(f)
```

durch

```python
    data = load_yaml(path)
```

Varianten beachten:
- `yaml.safe_load(f) or []` → `load_yaml(path) or []`
- `yaml.safe_load(f) or {}` → `load_yaml(path) or {}`
- In `load_army` (Zeilen 381–389) heißen die Pfadvariablen `units_path`/`army_path`;
  in `load_stratagems` (Zeile 512) heißt sie `path` innerhalb der Schleife;
  in `load_roster_metadata`/`load_roster` (Zeilen 851, 942) ebenfalls `path`.
  Verwende jeweils die lokale Pfadvariable.

**Verify**: `grep -c "yaml.safe_load" src/gameObjects/loader.py` → `1`
(nur noch der Aufruf im Helper selbst). `ruff check src/` → passt.

### Step 3: Die 2 Stellen in `game_state.py` umstellen

Importiere `load_yaml` im bestehenden `gameObjects.loader`-Import von
`game_state.py` mit. Ersetze (Zeilen 93–97):

```python
    pts_data = load_yaml(pts_path) or {}
    units_pts: dict[str, dict] = pts_data.get("units") or {}
    roster_data = load_yaml(roster_path) or {}
```

**Verify**: `grep -c "yaml.safe_load" src/gameMechanic/game_state.py` → `0`.
Prüfe danach: `grep -n "^import yaml\|^import" src/gameMechanic/game_state.py` —
wenn `yaml` in der Datei nun ungenutzt ist, entferne den `import yaml` (ruff F401
meldet das): `ruff check src/` → passt.

### Step 4: Tests

Ergänze in `tests/gameObjects/test_loader.py` (Strukturvorlage: die bestehenden
Tests derselben Datei, z. B. `test_round_choice_abilities_are_cached` ganz unten):

```python
def test_load_yaml_raises_clear_error_on_broken_file(tmp_path) -> None:
    from gameObjects.loader import YamlDataError, load_yaml

    broken = tmp_path / "broken.yaml"
    broken.write_text("units:\n  - id: [unclosed")
    with pytest.raises(YamlDataError, match="broken.yaml"):
        load_yaml(broken)


def test_load_yaml_returns_parsed_data(tmp_path) -> None:
    from gameObjects.loader import load_yaml

    ok = tmp_path / "ok.yaml"
    ok.write_text("units:\n  - id: a\n")
    assert load_yaml(ok) == {"units": [{"id": "a"}]}
```

Stelle sicher, dass `import pytest` oben vorhanden ist (sonst ergänzen).

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` → grün inkl.
2 neuer Tests.

### Step 5: Vollsuite

**Verify**: `pytest --tb=short` → alle Tests grün (Baseline bei Plan-Erstellung 767,
+2 neue aus diesem Plan; durch andere abgeschlossene Pläne kann die Zahl höher liegen),
Coverage ≥ 80 %.

## Test plan

- `test_load_yaml_raises_clear_error_on_broken_file`: kaputte YAML →
  `YamlDataError`, Meldung enthält den Dateinamen.
- `test_load_yaml_returns_parsed_data`: intakte YAML → geparste Struktur.
- Alle bestehenden Loader-Tests bleiben grün (Verhalten bei validen Dateien
  ist unverändert).

## Done criteria

ALLE müssen gelten:

- [ ] `grep -c "yaml.safe_load" src/gameObjects/loader.py` → `1`
- [ ] `grep -c "yaml.safe_load" src/gameMechanic/game_state.py` → `0`
- [ ] `grep -n "class YamlDataError" src/gameObjects/loader.py` → 1 Treffer
- [ ] 2 neue Tests vorhanden und grün
- [ ] `pytest --tb=short` → alle grün, Coverage-Gate erfüllt
- [ ] `ruff check src/ && black --check src/ && isort --check-only src/` → passt
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- Ein bestehender Test nach der Umstellung rot wird (z. B. weil er gezielt
  `yaml.YAMLError` erwartet) — Repo-Regel: rote Tests = STOP, Nutzer fragen.
- Eine der 19 Stellen strukturell anders aussieht als das Zwei-Zeilen-Muster
  (z. B. das File-Handle wird noch für etwas anderes benutzt).
- `grep -c` nach Step 2 nicht `1` ergibt — dann wurden Stellen übersehen oder
  es sind seit Plan-Erstellung neue hinzugekommen; melden statt raten.

## Maintenance notes

- Künftige Loader-Funktionen MÜSSEN `load_yaml` statt `yaml.safe_load` verwenden —
  Reviewer sollten in PRs auf neue `safe_load`-Aufrufe achten
  (`grep -rn "yaml.safe_load" src/` sollte dauerhaft genau 1 Treffer liefern).
- Bewusst aufgeschoben: eine UI-freundliche Darstellung des `YamlDataError`
  (z. B. `st.error` mit Reparatur-Hinweis im Setup-Screen). Der rohe, aber jetzt
  aussagekräftige Fehler ist für ein Dev-Tool akzeptabel.
- Plan 012 (Loader-Caching) baut auf denselben Funktionen auf — bei paralleler
  Ausführung Merge-Konflikte in `loader.py` erwartbar; nacheinander ausführen.
