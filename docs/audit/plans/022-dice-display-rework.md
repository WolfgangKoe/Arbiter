# Plan 022 — Dice Display Rework

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat HEAD -- src/uiLayout/dice_html.py src/gameMechanic/ability_engine.py src/gameMechanic/attack_math.py`
> Wenn `rightward = value < 0` in `dice_html.py` nicht mehr vorhanden ist
> (Arrow-Bug bereits gefixt): nur die verbleibenden Steps ausführen; STOP
> wenn unbekannte Drift vorliegt.

## Status

- **Priority**: P1 (HOCH)
- **Effort**: M
- **Risk**: MEDIUM
- **Depends on**: —
- **Category**: bugfix + feature + refactor (Dice Display, INV-4b Cluster 1)
- **Planned at**: 2026-06-20

## Why this matters

`src/uiLayout/dice_html.py` hat mindestens 4 bekannte Bugs/Lücken, die
direkt die Spielunterstützung beeinträchtigen:

1. **Arrow-Direction-Bug (aktiv):** `rightward = value < 0` (Z. 200) —
   Debuffs zeigen Pfeil RECHTS, Buffs LINKS. **Falsch und verwirrend.**
   Korrekt: Buff zeigt Pfeil RECHTS (niedrigere Würfelergebnisse genügen),
   Debuff zeigt Pfeil LINKS (höhere Würfelergebnisse nötig). War früher
   korrekt, dann beim Refactoring (Plan 008) invertiert (Refinement 2026-06-20).
2. **Badge-Breite:** `_BADGE_COL_W = 96px` + `white-space:nowrap` → lange
   Labels (z. B. „Power Klaw") überlappen Würfel-Slot 1.
3. **Fehlende Edge Cases:** Grenzfall 6+ (Debuff über 6 → ✕-Slot rechts),
   Grenzfall gegen 1 (Buff macht 1 nie erfolgreich → ✕-Slot bleibt links).
4. **Kein `color_hint`-Feld:** Quantum Shield (auto-fail für Angreifer)
   hat keinen expliziten Buff/Debuff-Hinweis — Vorzeichen allein reicht nicht.

Außerdem: `attack_math.py` enthält hardcodierte Dict-Keys `dakka`/`klaw`/
`tesla` (INV-4b Cluster 1) — generisch über YAML lösbar.

**Test-Pflicht (KRITISCH):** Dieser Bereich hat früher massiv versagt.
Jede Änderung braucht HTML-Output-Tests. Spec: `docs/spec/dice_display.md`.

## Current state

- `src/uiLayout/dice_html.py:200` — `rightward = value < 0` (Pfeil invertiert)
- `src/uiLayout/dice_html.py` — `_BADGE_COL_W = 96px`, `white-space:nowrap`
- `src/uiLayout/dice_html.py` — keine Edge-Case-Behandlung für 6+ / gegen-1
- `src/gameMechanic/ability_engine.py` — kein `color_hint`-Feld im Modifier-Dict
- `src/gameMechanic/attack_math.py` — `dakka`/`klaw`/`tesla` als Literal-Keys
- `tests/uiLayout/` — kein `test_dice_html.py` (muss neu angelegt werden)

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Dice-Tests | `python -m pytest tests/uiLayout/test_dice_html.py -q` | grün (nach Step 1) |
| Vollsuite | `pytest --tb=short` | grün, ≥ 90 % |
| Architektur-Gate | `pytest tests/architecture/ --no-cov -q` | grün |
| INV-4b prüfen | `grep -rn "dakka\|klaw\|tesla" src/gameMechanic/attack_math.py` | kein Treffer nach Step 5 |

## Scope

**In scope:**
- `dice_html.py`: Arrow-Direction-Fix, Badge truncate, Edge-Case-Render,
  `color_hint`-Feld, Reroll- und Always-fail-Muster
- `ability_engine.py`: optionales `color_hint`-Feld in Modifier-Dict
  (rückwärtskompatibel)
- `tests/uiLayout/test_dice_html.py`: neue Test-Suite (HTML-Output-Tests)
- `attack_math.py`: `dakka`/`klaw`/`tesla`-Keys → YAML-gesteuert (INV-4b Cluster 1)
- `docs/spec/dice_display.md`: aktuell halten nach jedem Step

**Out of scope:**
- Komplette Neuimplementierung der Würfel-Engine
- Andere UI-Komponenten
- Reroll-Logik in der Spielmechanik (nur Anzeige)

## Git workflow

- Branch: `feature/022-dice-display-rework`.
- Commits per Step (nach Step 1 bereits committen — Arrow-Fix ist eigenständig).
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Arrow-Direction-Fix + Regression-Tests (SOFORT committen)

`dice_html.py:200`: `rightward = value < 0` → `rightward = value > 0`

Gleichzeitig `tests/uiLayout/test_dice_html.py` anlegen mit:
- `test_buff_arrow_points_right`: positiver Modifier → Pfeil-HTML enthält
  Rechts-Indikator
- `test_debuff_arrow_points_left`: negativer Modifier → Pfeil-HTML enthält
  Links-Indikator

**Verify**: `pytest tests/uiLayout/test_dice_html.py -q` grün.
Danach sofort committen: `Fix dice arrow direction (buff→right, debuff→left)`.

STOP wenn vorher grüne Tests rot werden — Nutzer informieren (war das Verhalten
bewusst invertiert?).

### Step 2: Badge truncate

`dice_html.py`: `_badge_chip()`: CSS `white-space:nowrap` →
`overflow:hidden; text-overflow:ellipsis` (Breite 96px bleibt).

Test: `test_long_badge_does_not_overflow` — langer Label-String erzeugt
kein `white-space:nowrap` im HTML-Output.

**Verify**: manuell — „Power Klaw" in Würfelzeile abgeschnitten, kein Overlap.

### Step 3: `color_hint`-Feld

`ability_engine.py`: Modifier-Dict-Builder erhält optionales Feld
`color_hint: "buff" | "debuff"` (wenn nicht gesetzt: wertbasiert wie bisher,
Rückwärtskompatibilität gewahrt).

`dice_html.py`: wenn `color_hint` vorhanden, `color_hint` verwenden statt
Vorzeichen des Werts.

Test: `test_color_hint_overrides_value_sign` — Modifier mit `value=-1,
color_hint="buff"` → grüne Farbe im HTML-Output.

**Verify**: `pytest tests/uiLayout/test_dice_html.py -q` grün.

### Step 4: Edge Cases

Zwei Grenzfälle implementieren und testen:

**6+ Debuff über 6:**
- Basis 6+, Debuff −1 → 7+ = unmöglich → ✕-Symbol rechts von Slot 6
- Basis 6+, Debuff −2 → weiteres ✕ rechts

**Buff gegen die 1:**
- Basis 3+, Buff +2 → Slot 1 bleibt ✕ (Invariante: unmodifiziertes 1
  misslingt immer)

**Reroll-Marker:**
- `↺`-Symbol unter betroffenen Slots (z. B. Reroll-1 → unter Slot 1)

**Always-fail-Marker:**
- `✕`-Symbol unter Slots die immer scheitern (Quantum Shield: Slots 1–3
  für den Angreifer)

Tests: je Fallkategorie einen HTML-Output-Test (s. Test-Plan).

**Verify**: `pytest tests/uiLayout/test_dice_html.py -q` grün.

### Step 5: INV-4b Cluster 1 (`dakka`/`klaw`/`tesla`)

`attack_math.py`: Dict-Keys `dakka`, `klaw`, `tesla` → generisch via
YAML-Schema (z. B. `effect_type` aus YAML statt Literal-Key).

`dice_html.py`: `.get("tesla")` etc. → generisch via Schema-Feld.

Test: `test_no_faction_string_in_attack_math` — Architektur-Gate:
`dakka`/`klaw`/`tesla` nicht in `attack_math.py`.

**Verify**: `pytest tests/architecture/ --no-cov -q` grün;
`grep -rn "dakka\|klaw\|tesla" src/gameMechanic/attack_math.py` → kein Treffer.

### Step 6: Vollsuite + Lint + Doku

`pytest --tb=short` grün, Coverage ≥ 90 %;
`ruff check src/ && black --check src/ && isort --check-only src/` passt;
`docs/spec/dice_display.md` auf aktuellen Stand bringen (Arrow-Fix als
`GEFIXT` markieren, Edge-Case-Tabellen verifizieren).

## Test plan (Pflicht-Tests)

| Test | Kategorie |
|------|-----------|
| `test_buff_arrow_points_right` | Regression (Bug-Fix Step 1) |
| `test_debuff_arrow_points_left` | Regression (Bug-Fix Step 1) |
| `test_slot_1_always_shows_x` | Invariante |
| `test_long_badge_does_not_overflow` | Badge-Fix Step 2 |
| `test_color_hint_overrides_value_sign` | color_hint Step 3 |
| `test_debuff_beyond_6_shows_x_slot` | Edge Case 6+ Step 4 |
| `test_buff_cannot_make_1_succeed` | Edge Case gegen 1 Step 4 |
| `test_reroll_marker_correct_slot` | Reroll Step 4 |
| `test_always_fail_marks_correct_slots` | Always-fail Step 4 |
| `test_no_faction_string_in_attack_math` | Architektur Step 5 |

## Done criteria

ALLE müssen gelten:

- [ ] Arrow-Direction-Fix + Regression-Tests grün
- [ ] Badge truncate, kein Overflow mehr
- [ ] `color_hint` funktioniert (rückwärtskompatibel)
- [ ] Edge Cases 6+/gegen-1 korrekt dargestellt
- [ ] Reroll- und Always-fail-Muster implementiert und getestet
- [ ] INV-4b: `dakka`/`klaw`/`tesla` aus `src/` entfernt
- [ ] `pytest --tb=short` grün, Coverage ≥ 90 %
- [ ] Architektur-Gate grün (`pytest tests/architecture/ --no-cov -q`)
- [ ] `docs/spec/dice_display.md` aktuell
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Arrow-Fix (Step 1) bricht vorher grüne Tests → STOP, Nutzer informieren:
  War das invertierte Verhalten bewusst eingeführt?
- Edge-Case-Render (Step 4) erfordert strukturellen Umbau der Slot-Schleife
  (> 20 Zeilen Änderung) → Scope-Überprüfung, Nutzer fragen
- `dakka`/`klaw`/`tesla`-Generalisierung erfordert YAML-Schema-Änderung
  in Waffendaten → Scope abgrenzen, Nutzer informieren

## Maintenance notes

- `test_dice_html.py` ist das primäre Sicherheitsnetz für diesen Bereich.
  Jede Änderung an `dice_html.py` braucht einen neuen oder angepassten Test.
- `color_hint` ist das Erweiterungsventil für perspektivabhängige Modifier
  (Quantum Shield, Transhuman Physiology etc.) — nicht via Vorzeichen-Hack
  lösen.
- `docs/spec/dice_display.md` ist die kanonische Quelle für die
  Würfelanzeige-Semantik. Bei Abweichung zwischen Code und Spec: Spec hat
  Vorrang, außer bewusste Entscheidung mit Kommentar.
