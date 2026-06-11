# Plan 012: Loader-Caching vervollständigen und auf ein Idiom konsolidieren

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat 225d13b..HEAD -- src/gameObjects/loader.py src/uiLayout/armyList.py`
> ACHTUNG: Plan 006 ändert `loader.py` flächig (yaml.safe_load → load_yaml).
> Das ist erwarteter Drift — die Cache-Logik dieses Plans ist davon unabhängig.
> Wenn aber die Funktions-Signaturen der unten genannten Loader abweichen: STOP.

## Status

- **Priority**: P3 (aufschiebbar; spürbar bei jedem UI-Klick, aber kein Bug)
- **Effort**: S
- **Risk**: LOW
- **Depends on**: 006 (beide ändern `loader.py` — NACH 006 ausführen, sonst
  Merge-Konflikte)
- **Category**: perf
- **Planned at**: commit `225d13b`, 2026-06-11

## Why this matters

Streamlit führt das Skript bei JEDER Interaktion komplett neu aus. Plan 005 hat
deshalb `load_round_choice_abilities`/`load_round_choice_label` pro Prozess
gecacht — aber fünf weitere Loader-Funktionen mit Call-Sites in Render-Pfaden
parsen ihre YAML weiterhin bei jedem Rerun: Stratagems (2 Dateien × 2 Spieler),
Fähigkeiten (2–3 Dateien pro selektierter Einheit), Deny-Wargear. Zusätzlich
existieren jetzt ZWEI Caching-Idiome im Repo: der Modul-Dict-Cache in `loader.py`
(Plan 005) und ein älterer Sondercache `_ABILITIES_CACHE` in `armyList.py`.
Dieser Plan dehnt das Plan-005-Idiom auf die restlichen Loader aus und entfernt
den Sondercache — ein Idiom, eine Stelle, alle Render-Pfade abgedeckt.

## Current state

**Bereits gecacht** (Muster aus Plan 005, `src/gameObjects/loader.py:29-30, 435-461`):

```python
_ROUND_CHOICE_CACHE: dict[str, list] = {}
_ROUND_CHOICE_LABEL_CACHE: dict[str, str] = {}

def load_round_choice_abilities(faction_dir: str) -> list[CommandProtocol]:
    if faction_dir in _ROUND_CHOICE_CACHE:
        return _ROUND_CHOICE_CACHE[faction_dir]
    ...
    _ROUND_CHOICE_CACHE[faction_dir] = result
    return result
```

**Ungecacht, mit Render-Pfad-Call-Sites** (alle in `src/gameObjects/loader.py`):

| Funktion | Zeile | Render-Call-Site |
|---|---|---|
| `load_faction_abilities` | 412 | `armyList.py:18` (via Sondercache), `get_abilities_for_unit` |
| `load_unit_abilities` | 482 | `ability_engine.py:121,144`; via `get_abilities_for_unit` ← `gameActionsArea.py:84` |
| `load_subfaction_abilities` | 492 | `ability_engine.py:145` |
| `load_stratagems` | 505 | `gameProtocoll.py:139-141` (pro Rerun, beide Spieler) |
| `load_deny_wargear_names` | 710 | `psychicPhase.py:62` |

**Sondercache** — `src/uiLayout/armyList.py:11-21`:

```python
_ABILITIES_CACHE: dict[str, list] = {}


def _faction_abilities_for(faction: str) -> list:
    faction_dir = faction_dir_for(faction)
    if faction_dir not in _ABILITIES_CACHE:
        try:
            _ABILITIES_CACHE[faction_dir] = load_faction_abilities(faction_dir)
        except Exception:
            _ABILITIES_CACHE[faction_dir] = []
    return _ABILITIES_CACHE[faction_dir]
```

**Bestehende Cache-Tests** (Vorlage, `tests/gameObjects/test_loader.py:1051-1058`):

```python
def test_round_choice_abilities_are_cached() -> None:
    first = load_round_choice_abilities("necrons")
    second = load_round_choice_abilities("necrons")
    assert first is second
```

Die YAML-Daten ändern sich nur bei Spielinitialisierung/Deploy — Prozess-Lebensdauer-
Caching ist semantisch korrekt (von Plan 005 etabliert).

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | passt |
| Loader-Tests | `python -m pytest tests/gameObjects/test_loader.py -q` | grün |
| Vollsuite + Coverage | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `src/gameObjects/loader.py` — Cache-Dicts + Guards für die 5 Funktionen
- `src/uiLayout/armyList.py` — `_ABILITIES_CACHE` entfernen
- `tests/gameObjects/test_loader.py` — Cache-Tests ergänzen

**Out of scope** (NICHT anfassen):
- `load_weapon_catalog`, `load_army`, `load_roster`, `load_points`,
  `load_wargear_catalog`, `load_relic_catalog`, `load_detachment_types` —
  laufen nur bei Spielinitialisierung, kein Rerun-Pfad; Caching dort wäre
  Komplexität ohne Nutzen.
- Kein Wechsel auf `@st.cache_data` — das Modul-Dict-Idiom ist etabliert
  (Plan 005) und hält `loader.py` Streamlit-frei.
- Die Call-Sites (`gameProtocoll.py`, `ability_engine.py`, `psychicPhase.py`,
  `gameActionsArea.py`) — sie profitieren automatisch.

## Git workflow

- Branch: `advisor/012-loader-cache-consolidation`.
- Commit-Stil imperativ Englisch, z. B. `Cache remaining loader YAML per process`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Cache-Dicts in `loader.py` ergänzen

Unter den bestehenden Cache-Dicts (Zeile ~30):

```python
_FACTION_ABILITIES_CACHE: dict[str, list[Ability]] = {}
_UNIT_ABILITIES_CACHE: dict[str, list[Ability]] = {}
_SUBFACTION_ABILITIES_CACHE: dict[str, list[Ability]] = {}
_STRATAGEM_CACHE: dict[str, list[Stratagem]] = {}
_DENY_WARGEAR_CACHE: dict[str, frozenset[str]] = {}
```

Dann in jeder der 5 Funktionen das exakte Plan-005-Muster: Guard als erste
Zeile (`if faction_dir in CACHE: return CACHE[faction_dir]`), Ergebnis vor dem
`return` eintragen. WICHTIG bei `load_faction_abilities`/`load_unit_abilities`/
`load_subfaction_abilities`/`load_deny_wargear_names`: auch den
`if not path.exists()`-Frühausstieg cachen (leere Liste/frozenset in den Cache),
genau wie `load_round_choice_abilities` es vormacht (Zeilen 438-440).

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` → grün.

### Step 2: Sondercache in `armyList.py` entfernen

Lösche `_ABILITIES_CACHE` und vereinfache:

```python
def _faction_abilities_for(faction: str) -> list:
    faction_dir = faction_dir_for(faction)
    try:
        return load_faction_abilities(faction_dir)
    except Exception:
        return []
```

(Das breite `except Exception` bleibt bewusst erhalten — Verhaltensänderung der
Sidebar bei kaputter YAML ist NICHT Teil dieses Plans; siehe Maintenance notes.)

**Verify**: `grep -n "_ABILITIES_CACHE" src/` → 0 Treffer; `ruff check src/` → passt.

### Step 3: Cache-Tests ergänzen

In `tests/gameObjects/test_loader.py`, direkt neben den Plan-005-Tests
(Strukturvorlage `test_round_choice_abilities_are_cached`):

```python
def test_faction_abilities_are_cached() -> None:
    assert load_faction_abilities("orks") is load_faction_abilities("orks")


def test_stratagems_are_cached() -> None:
    assert load_stratagems("orks") is load_stratagems("orks")


def test_unit_abilities_are_cached() -> None:
    assert load_unit_abilities("necrons") is load_unit_abilities("necrons")


def test_deny_wargear_names_are_cached() -> None:
    assert load_deny_wargear_names("necrons") is load_deny_wargear_names("necrons")
```

(Imports oben in der Datei ergänzen, falls die Funktionen dort noch nicht
importiert sind.)

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` → grün inkl.
4 neuer Tests.

### Step 4: Vollsuite — Cache-Verträglichkeit der Gesamt-Suite prüfen

Die Suite lädt durchgehend die echten Daten-Verzeichnisse (`necrons`, `orks`,
`custodes`) — Caching über Testgrenzen hinweg ist daher unkritisch (gleicher
Input → gleiches Ergebnis), wie Plan 005 bewiesen hat. Trotzdem:

**Verify**: `pytest --tb=short` → alle Tests grün (Baseline bei Plan-Erstellung 767,
+4 neue aus diesem Plan; durch andere abgeschlossene Pläne kann die Zahl höher liegen),
Coverage ≥ 80 %. Wird ein BESTEHENDER Test rot, der vorher grün war: STOP (siehe unten).

## Test plan

- 4 neue Identitäts-Tests (`is`-Vergleich beweist Cache-Hit), Vorlage Plan 005.
- Vollsuite als Cache-Verträglichkeits-Nachweis: kein Test darf von
  Re-Parsing zwischen Aufrufen abhängen.

## Done criteria

ALLE müssen gelten:

- [ ] 5 neue Cache-Dicts in `loader.py`; alle 5 Funktionen mit Guard
  (`grep -c "_CACHE\[faction_dir\]" src/gameObjects/loader.py` → deutlich gestiegen;
  pro Funktion: Guard + Eintrag)
- [ ] `grep -rn "_ABILITIES_CACHE" src/` → 0 Treffer
- [ ] 4 neue Tests vorhanden und grün
- [ ] `pytest --tb=short` → alle grün, Coverage-Gate erfüllt
- [ ] `ruff check src/ && black --check src/ && isort --check-only src/` → passt
- [ ] Keine Dateien außerhalb der In-scope-Liste geändert (`git status`)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

Stoppen und zurückmelden, wenn:

- Ein bestehender Test rot wird, weil er zwischen zwei Aufrufen die YAML-Datei
  wechselt/patcht und nun den Cache-Treffer sieht — dann braucht es einen
  Test-Reset-Mechanismus (z. B. autouse-Fixture, die die Cache-Dicts leert);
  das ist eine Designentscheidung → melden, nicht eigenmächtig einbauen.
- `get_abilities_for_unit` oder ein anderer Caller das zurückgegebene
  Listen-Objekt MUTIERT (z. B. `.append`) — Cache-Pollution-Gefahr; mit
  `grep -n "abilities.append\|.extend(" src/` prüfen; bei Fund: melden.
- Plan 006 ist noch nicht gelaufen und `loader.py` sieht strukturell anders aus
  als erwartet.

## Maintenance notes

- Damit gilt repo-weit: **Loader-Caching lebt ausschließlich in `loader.py`** —
  Reviewer sollten neue Sondercaches in UI-Modulen ablehnen.
- Das breite `except Exception` in `armyList._faction_abilities_for` versteckt
  nach Plan 006 die neue, klare `YamlDataError`-Meldung in der Sidebar
  (leere Liste statt Fehler). Bewusst unverändert gelassen; Kandidat für eine
  spätere UX-Entscheidung des Nutzers.
- Wer einen Daten-Reload zur Laufzeit baut (z. B. „Roster neu laden"-Button),
  muss ALLE Cache-Dicts leeren — ggf. dann eine `clear_loader_caches()`-Funktion
  einführen.
