# Plan 008: `_common.py` entlasten — Attack-Mathematik in gemessenes Modul, Dice-HTML auslagern

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat 225d13b..HEAD -- src/uiLayout/_common.py`
> Dieser Plan zitiert Zeilennummern vom Stand `225d13b`. Wenn `_common.py`
> seitdem geändert wurde (insb. durch Plan 010, der VOR diesem Plan laufen
> soll), verschieben sich Zeilennummern — orientiere dich dann an den
> Funktionsnamen, nicht an den Zeilen. Wenn eine der zu verschiebenden
> Funktionen strukturell anders aussieht als beschrieben: STOP.

## Status

- **Priority**: P2
- **Effort**: M–L
- **Risk**: MED
- **Depends on**: 010 (tote Variablen in genau diesem Code zuerst entfernen);
  009 empfohlen vorher (fasst Nachbar-Code an)
- **Category**: tech-debt
- **Planned at**: commit `225d13b`, 2026-06-11

## Why this matters

`src/uiLayout/_common.py` ist mit 2088 Zeilen das größte Modul des Repos und
mischt drei Verantwortlichkeiten: reine Spielmathematik (Stärke-Parsing,
Attackenzahl-Berechnung), SVG/HTML-Würfelgrafik und Streamlit-Render-Flows.

Das eigentliche Problem ist nicht die Größe, sondern: **`src/uiLayout/*` steht in
der Coverage-omit-Liste** (`pyproject.toml`). Die reine Mathematik —
`_parse_strength`, `_compute_attacks`, `_total_attacks_int`,
`_group_melee_budget` — ist testbare Business-Logik und wird von
`tests/uiLayout/test_common.py` auch direkt getestet, zählt aber nicht ins
80 %-Coverage-Gate. Sie liegt damit außerhalb des Sicherheitsnetzes, das genau
für solchen Code gebaut wurde.

Dieser Plan macht zwei mechanische Schnitte:
1. **Reine Mathematik → `src/gameMechanic/attack_math.py`** (gemessenes Modul,
   zählt ab sofort ins Coverage-Gate).
2. **Dice-HTML-Block → `src/uiLayout/dice_html.py`** (bleibt ungemessen, ist
   reine Darstellung — aber `_common.py` schrumpft um ~390 Zeilen).

Beide Schnitte arbeiten mit Re-Exports: **kein einziger Aufrufer und kein Test
wird umgestellt.** Ziel: `_common.py` unter ~1550 Zeilen, Mathematik im
Coverage-Netz, Verhalten byte-identisch.

## Current state

`src/uiLayout/_common.py` (2088 Zeilen, Stand `225d13b`):

- Modul-Level-Imports (Zeilen 10–19): `streamlit`, `gameMechanic.game_state`,
  `gameMechanic.unit_mutations`, `gameObjects.unit`, `gameObjects.weapon`.
  → Modul-Level-Imports aus `gameMechanic` sind etabliert; `gameMechanic/__init__.py`
  ist leer; ein neues Modul dort erzeugt keinen Import-Zyklus, solange es selbst
  nichts aus `uiLayout` oder `streamlit` importiert.

**Block A — zu verschiebende reine Funktionen** (keine nutzt `st.`/Session-State;
verifiziert am Stand `225d13b`):

| Funktion | Zeilen | Signatur |
|---|---|---|
| `_parse_strength` | 335–360 | `(raw: int \| str, unit_strength: int) -> int` |
| `_restriction_label` | 375–382 | `(restriction: str) -> str` |
| `_compute_attacks` | 384–406 | `(attacks_str, models_count, unit_attacks, effect=None, max_attacks=None) -> str` |
| `_total_attacks_int` | 408–430 | `(attacks_str, models_alive, unit_attacks, effect=None, max_attacks=None) -> int \| None` |
| `_detect_weapon_special` | 518–528 | `(profile: WeaponProfile) -> dict` |
| `_group_melee_budget` | 1410–1430 | `(grp_weapons: list, alive: int, eff_attacks: int) -> int` |

NICHT verschieben (nutzen `st.session_state`): `_protocol_source_label`,
`_collect_atk_modifiers`, `_collect_def_save_modifiers`.

**Block B — Dice-HTML-Block, Zeilen 530–916.** Per AST-Analyse verifiziert:
Der Block ist in sich geschlossen — er referenziert **keinen** Namen, der
außerhalb des Blocks in `_common.py` definiert ist, und von seinen Namen werden
außerhalb nur drei genutzt (`_render_dice_roll_block` Z. 1250,
`_render_dice_wound_block` Z. 1259, `_render_dice_save_block` Z. 1264 — alle in
`_render_resolution_tab`). Inhalt des Blocks:

- Konstanten: `_THRESHOLD_COLOR`, `_PIP_POSITIONS`, `_DIE_SLOT`, `_FRAME_INSET`,
  `_BUFF_COLOR_HEX`, `_DEBUFF_COLOR_HEX`, `_BADGE_COL_W`
- Funktionen: `_boundary_gap_html`, `threshold_header_html`, `dice_face_svg`,
  `dice_row_html`, `_badge_chip`, `grid_row_html`, `block_divider_html`,
  `modifier_die_pair_html`, `save_modifier_die_pair_html`, `special_die_html`,
  `_render_dice_roll_block`, `_render_dice_wound_block`, `_render_dice_save_block`

Tests: `tests/uiLayout/test_common.py` importiert die Mathe-Funktionen aus
`uiLayout._common` (Streamlit ist dort gemockt). Über die Re-Exports laufen diese
Tests unverändert weiter — und führen dabei den Code im neuen, GEMESSENEN Modul
aus. Genau dadurch erscheint `attack_math.py` mit Coverage im Report.

`pyproject.toml` `[tool.coverage.run] omit` enthält `src/uiLayout/*` —
`src/gameMechanic/attack_math.py` fällt NICHT darunter (nicht ändern!).

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | passt |
| Schnelltest | `python -m pytest tests/uiLayout/test_common.py -q` | grün |
| Vollsuite + Coverage | `pytest --tb=short` | grün, ≥80 % |
| LOC-Kontrolle | `wc -l src/uiLayout/_common.py` | < 1600 |

## Scope

**In scope**:
- `src/gameMechanic/attack_math.py` (NEU)
- `src/uiLayout/dice_html.py` (NEU)
- `src/uiLayout/_common.py` (Funktionen entfernen, Re-Import-Zeilen einfügen)

**Out of scope** (NICHT anfassen):
- Alle Aufrufer (`shootingPhase.py`, `fightPhase.py`, `gameActionsArea.py`, …) —
  sie importieren weiter aus `_common`.
- `tests/uiLayout/test_common.py` — Tests bleiben unverändert (sie beweisen die
  Re-Export-Kompatibilität).
- `pyproject.toml` — die omit-Liste bleibt wie sie ist.
- KEINE Umbenennung der Funktionen (auch nicht das Entfernen des `_`-Präfixes) —
  Re-Export-Kompatibilität geht vor Ästhetik.
- `_collect_atk_modifiers` / `_collect_def_save_modifiers` /
  `_protocol_source_label` bleiben in `_common.py`.

## Git workflow

- Branch: `advisor/008-split-common-module`.
- Zwei Commits (einer pro Schnitt), imperativ Englisch, z. B.
  `Extract pure attack math into measured module` und
  `Move dice HTML rendering into dice_html module`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: `attack_math.py` anlegen und Block A verschieben

Erzeuge `src/gameMechanic/attack_math.py`:

```python
"""Pure attack-math helpers — no Streamlit, no session state.

Extracted from uiLayout/_common.py so this logic counts toward the
coverage gate (src/uiLayout/* is omitted from measurement).
"""

from __future__ import annotations

from gameObjects.weapon import WeaponProfile
```

Verschiebe die sechs Funktionen aus Block A (Funktionskörper **unverändert**,
inkl. Docstrings) in diese Datei. Lösche sie in `_common.py` und füge dort —
im Import-Block oben, nach den bestehenden `gameMechanic`-Imports — ein:

```python
from gameMechanic.attack_math import (  # noqa: F401
    _compute_attacks,
    _detect_weapon_special,
    _group_melee_budget,
    _parse_strength,
    _restriction_label,
    _total_attacks_int,
)
```

(`# noqa: F401` weil einige Namen in `_common` nur noch re-exportiert werden.)

**Verify**:
`python -m pytest tests/uiLayout/test_common.py -q` → grün;
`ruff check src/` → passt;
`grep -n "def _parse_strength" src/uiLayout/_common.py` → 0 Treffer;
`grep -n "def _parse_strength" src/gameMechanic/attack_math.py` → 1 Treffer.

### Step 2: Coverage-Nachweis für `attack_math.py`

**Verify**: `pytest --tb=short 2>&1 | grep attack_math` → Zeile
`src/gameMechanic/attack_math.py` erscheint im Coverage-Report mit ≥ 90 %
(die bestehenden Tests in `test_common.py` decken die Funktionen bereits ab).
Gesamtgate ≥ 80 % weiterhin erfüllt.

### Step 3: `dice_html.py` anlegen und Block B verschieben

Erzeuge `src/uiLayout/dice_html.py` mit Kopf:

```python
"""SVG dice + HTML building blocks for the attack-resolution UI (6d-v3)."""

from __future__ import annotations

import streamlit as st
```

Verschiebe den kompletten Block der Zeilen 530–916 (alle Konstanten und
Funktionen aus der Liste in „Current state", Körper unverändert) dorthin.
Lösche den Block in `_common.py` und füge im Import-Block ein:

```python
from uiLayout.dice_html import (  # noqa: F401
    _render_dice_roll_block,
    _render_dice_save_block,
    _render_dice_wound_block,
    block_divider_html,
    dice_face_svg,
    dice_row_html,
    grid_row_html,
    modifier_die_pair_html,
    save_modifier_die_pair_html,
    special_die_html,
    threshold_header_html,
)
```

(Die rein blockinternen Namen `_boundary_gap_html`, `_badge_chip` und die
Konstanten müssen NICHT re-exportiert werden — falls `ruff` danach
F821-„undefined name"-Fehler in `_common.py` meldet, den betreffenden Namen in
die Importliste aufnehmen statt zu improvisieren.)

**Verify**: `ruff check src/` → passt (keine F821);
`python -m pytest tests/ -q` → grün;
`wc -l src/uiLayout/_common.py` → < 1600.

### Step 4: Manuelle UI-Verifikation vorbereiten

Render-Code ist laut Repo-Regel manuell zu prüfen. Nimm in deine Abschlussmeldung
auf, was der Nutzer in der laufenden App prüfen soll:
**Shooting- und Fight-Phase einmal bis zur Resolution durchspielen — Würfelblöcke
(Hit/Wound/Save) müssen identisch aussehen wie vorher (SVG-Würfel, Modifier-Paare,
7+-Handling).**

## Test plan

- KEINE neuen Tests nötig — der Plan ist verhaltensneutral; die bestehenden
  Tests in `tests/uiLayout/test_common.py` beweisen die Re-Export-Kompatibilität
  und erzeugen die Coverage im neuen Modul.
- Verifikation: `pytest --tb=short` → 767 Tests grün; `attack_math.py` im
  Coverage-Report.

## Done criteria

ALLE müssen gelten:

- [ ] `src/gameMechanic/attack_math.py` existiert, enthält genau die 6 Funktionen,
  importiert weder `streamlit` noch aus `uiLayout`
  (`grep -n "streamlit\|uiLayout" src/gameMechanic/attack_math.py` → 0 Treffer)
- [ ] `src/uiLayout/dice_html.py` existiert; `_common.py` enthält keinen der
  Block-B-Funktionskörper mehr (`grep -c "def dice_face_svg" src/uiLayout/_common.py` → 0)
- [ ] `wc -l src/uiLayout/_common.py` → < 1600
- [ ] `pytest --tb=short` → 767 Tests grün, Coverage-Gate erfüllt,
  `attack_math.py` erscheint im Report
- [ ] `ruff check src/ && black --check src/ && isort --check-only src/` → passt
- [ ] Kein Aufrufer und kein Test wurde geändert (`git status` zeigt nur die
  3 In-scope-Dateien)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert
- [ ] Abschlussmeldung enthält die manuelle UI-Prüfliste aus Step 4

## STOP conditions

Stoppen und zurückmelden, wenn:

- Eine der 6 Block-A-Funktionen doch `st.` oder Session-State referenziert
  (Drift seit Plan-Erstellung) — dann gehört sie NICHT in `attack_math.py`.
- Nach Step 3 mehr als 2 zusätzliche F821-Namen nötig werden — das hieße, der
  Block ist nicht mehr self-contained (Drift); melden statt weiter importieren.
- Ein Import-Zyklus auftritt (`ImportError: cannot import name …  (circular import)`).
- Irgendein bestehender Test rot wird — Repo-Regel: STOP, Nutzer fragen.
- `_common.py` nach beiden Schnitten NICHT unter 1600 Zeilen liegt — dann wurde
  etwas nicht entfernt; prüfen statt weiterschneiden.

## Maintenance notes

- **Folgearbeit (bewusst NICHT in diesem Plan):** Die verbleibenden Brocken in
  `_common.py` — `render_attack_declaration` (~250 Z.), `render_group_assignment`
  (~215 Z.), `_render_resolution_tab` (~190 Z.) — sind Render-Flows mit
  Session-State und brauchen einen eigenen, vorsichtigeren Plan. Ebenso das
  Umstellen der Aufrufer auf Direkt-Importe aus `attack_math`/`dice_html`
  (dann können die Re-Exports weg).
- CLAUDE.md/Memory-Regel „immer `_parse_strength` aus `_common.py` verwenden"
  bleibt durch den Re-Export wörtlich gültig; langfristig sollte die Doku auf
  `gameMechanic.attack_math` zeigen.
- Reviewer: Diff sollte fast ausschließlich aus verschobenen, unveränderten
  Funktionskörpern bestehen — jede inhaltliche Änderung an einem Funktionskörper
  ist ein Warnsignal.
- Wer neue Attack-Mathematik schreibt: direkt in `attack_math.py`, nicht in
  `_common.py` — sie ist dort automatisch im Coverage-Gate.
