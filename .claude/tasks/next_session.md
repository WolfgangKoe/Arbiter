# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py`
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — alle Ziele, aktueller Status
3. `docs/review/architecture_review_2026-05.md` — vollständiger Review aus letzter Session
4. `src/gameMechanic/combat.py` — für Blocker 1 fix
5. `src/gameMechanic/shootingPhase.py` — für Blocker 2 fix
6. `src/gameMechanic/fightPhase.py` — für Blocker 3 fix

---

## Was in dieser Session gemacht wurde

### Ziel A — Architektur-Review (fertig)

**A3 — Test-Refactoring:**
- `tests/engine/` komplett gelöscht (war verwaist, `engine.py` existiert nicht mehr)
- `test_unit_mutations.py` — 29 Tests (apply_damage, heal_unit, enter/leave_melee, set_charged, set_movement_status)
- `test_game_state.py` — 6 Tests (next_phase Transitionen)
- `tests/uiLayout/test_common.py` — 13 Tests (state_badges_html)
- 11 Duplikate (parse_dice + wound_threshold) korrekt entfernt
- Ergebnis: **166 Tests, alle grün**

**A1 + A2 — Review-Dokument:**
- `docs/review/architecture_review_2026-05.md` geschrieben
- Alle Phasen klassifiziert, 3 Blocker identifiziert, YAML-Template erstellt

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3a — Phase-Infrastruktur | ✅ fertig |
| Ziel 3b — combat.py Kernel | ✅ fertig |
| Ziel 3c — Shooting + Fight Phase | ✅ fertig |
| **Ziel A — Architektur-Review** | ✅ **fertig** |
| **Ziel 4 — Phasen ausbauen** | ⏳ **nächste Session** |

---

## Nächste Session: Blocker beheben, dann Ziel 4

Der Review hat 3 Blocker vor Ziel 4 identifiziert. Diese sind schnell fixbar (P1: 1 Zeile, P2: 1 Check, P3: Turn-Order-Logik). Danach kann Ziel 4 beginnen.

### Reihenfolge

```
1. Blocker 1 — parse_dice() W-Notation fix  (src/gameMechanic/combat.py)
2. Blocker 2 — in_melee-Check in can_shoot()  (src/gameMechanic/shootingPhase.py)
3. Blocker 3 — Nahkampfphase Turn-Order  (src/gameMechanic/fightPhase.py)
4. Tests für alle 3 Fixes
5. Ziel 4 starten: Bewegungsphase ausbauen (Advance-Roll, Reserve)
```

---

## Blocker-Details

### Blocker 1 — parse_dice() crasht auf W-Notation (P1)

**Problem:** Necron-YAML nutzt `W3`, `W6`, `W3+3`, `3W3`. `parse_dice()` kennt nur D-Notation.
**Fix:** In `src/gameMechanic/combat.py`, Funktion `parse_dice()`, vor dem bestehenden Code:
```python
s = str(s).upper().replace("W", "D")
```
**Tests:** Neue Tests für `parse_dice("W3")`, `parse_dice("W6")`, `parse_dice("3W3")`, `parse_dice("W3+3")`

Zusätzlich fehlt `resolve_weapon_strength()` für relative Stärkewerte (`Träger`, `+1`, `x2`).
Das ist ein separater Fix — auch in `combat.py` als neue Funktion.

### Blocker 2 — in_melee-Check fehlt in can_shoot() (P2)

**Problem:** Gebundene Einheiten dürfen laut Regelwerk nicht schießen. `can_shoot()` prüft das nicht.
**Fix:** In `src/gameMechanic/shootingPhase.py`, Funktion `can_shoot()`:
```python
if unit_state.get("in_melee"):
    return False
```
Analog: Schießen auf Freunde die im Nahkampf gebunden sind — noch out-of-scope, nur eigene Einheit prüfen.

### Blocker 3 — Nahkampfphase startet mit falschem Spieler (P3)

**Problem:** Regelwerk: Nahkampfrunde beginnt beim Nicht-aktiven Spieler. App startet beim aktiven Spieler.
**Fix:** In `src/gameMechanic/fightPhase.py` Turn-Order-Logik: Nicht-aktiver Spieler wird als erster zum Kämpfen aufgefordert.

---

## Architektur (Kurzreferenz)

```
src/
  app.py                    ← Streamlit-Einstieg
  gameMechanic/
    combat.py               ← AttackParams, DefendParams, resolve_attack(), parse_dice()
    commandPhase.py         ← Command Phase Handler
    shootingPhase.py        ← can_shoot(), ShootingPhaseHandler
    fightPhase.py           ← can_fight(), FightPhaseHandler
    movementPhase.py        ← MovementPhaseHandler
    chargephase.py          ← Stub
    game_state.py           ← init_state, next_phase, PHASES
    unit_mutations.py       ← apply_damage, heal_unit, enter/leave_melee, set_charged
    game_log.py             ← log_action
    ability_engine.py       ← Timing-Konstanten, Trigger-System
    phase_runner.py         ← PHASE_REGISTRY, render_current_phase()
  gameObjects/
    unit.py                 ← Unit-Dataclass
    weapon.py               ← Weapon-Dataclass
    loader.py               ← YAML → Objekte
  uiLayout/
    _common.py              ← lookup(), render_player_column(), render_attack_form()
    unitCard.py             ← Einheitenkarte inkl. MWBD/ResOrb-Awaiting-Flow
    gameActionsArea.py      ← delegiert an phase_runner
data/
  wh40k_9e/
    necrons/                ← units.yaml (W-Notation!), weapons.yaml, army.yaml
    orks/                   ← army.yaml (6 Einheiten, keine units.yaml)
tests/
  gameMechanic/             ← test_combat.py, test_unit_mutations.py, test_game_state.py,
                               test_command_phase.py, test_shooting.py, test_fight.py,
                               test_ability_engine.py
  uiLayout/                 ← test_common.py (NEU)
  gameObjects/              ← (vorhanden)
```

## Designentscheidungen (unveränderlich)

- `turn_flags` = Spielmechanik-Checks only
- `selected_targets: list[tuple[str, str]]` — nie single-target
- `can_fight()` prüft `in_melee` ODER `charged`
- `render_attack_form()` in `_common.py` — shared, kein Duplikat
- Attack-Form immer im unteren `_render_display`-Bereich, nicht in der Spalte
- Aktionen erscheinen NUR kontextabhängig zur ausgewählten Einheit
- Alle Engine-Importe direkt aus `gameMechanic.*` — kein Shim mehr
- Kein direktes Committen auf `main`
