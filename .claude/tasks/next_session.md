# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — Ziel 3b/3c + neue Blöcke
3. `src/engine.py` — enter_melee, leave_melee, _unit_state, selected_targets
4. `src/gameMechanic/phase_runner.py` + `_common.py`
5. `src/gameMechanic/shootingPhase.py` + `fightPhase.py` — aktuelle Stubs

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.  
Starten: `streamlit run src/app.py`  
Aktueller Branch: `dev`

```
src/
  app.py
  engine.py                   ← _unit_state (movement_choice, melee_with),
                                  enter_melee / leave_melee, selected_targets
  constants/colors.py
  uiLayout/
    _common.py                ← state_badges_html (movement_choice), render_player_column
    gameActionsArea.py
    unitCard.py               ← selected_targets toggle, movement_choice badges
    gameProtocoll.py / armyList.py / …
  gameObjects/
    ability.py / unit.py / weapon.py / loader.py / …
  gameMechanic/
    phase_handler.py
    phase_runner.py
    commandPhase.py
    movementPhase.py          ← liest movement_choice für Button-Highlight
    chargephase.py            ← Multi-Ziel-UI (selected_targets, enter_melee)
    psychicPhase.py / moralePhase.py
    shootingPhase.py          ← Stub (Ziel 3c)
    fightPhase.py             ← Stub (Ziel 3c)
    ability_engine.py

data/wh40k_9e/
  necrons/ (army.yaml, unit_abilities.yaml, …)
  orks/ _shared/

tests/ — 102 Tests, alle grün (Stand: Multi-Target-Block)
```

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Ziel 2 — commandPhase + Ability-System | ✅ fertig |
| Ziel 3a — Phase-Infrastruktur | ✅ fertig |
| **Bug 1 — STATIONARY/NORMAL Badge** | ✅ behoben (movement_choice) |
| **Multi-Target-Block** | ✅ fertig (102 Tests grün) |
| **Design-Block** | ⏳ parallel / eigene Session |
| **Ziel 3b — combat.py** | ⏳ nächster Schritt |
| **Ziel 3c — Shooting + Fight Phase** | ⏳ |

---

## Was in der letzten Session implementiert wurde

### Multi-Target-Block (commit: fb2fa0c)

**`engine.py`:**
- `movement_choice: None | "normal" | "stationary" | "advanced" | "retreated"` in `_unit_state()`
- `melee_with: list[str]` in `_unit_state()` — bidirektionale Melee-Verfolgung
- `enter_melee(attacker_uid, attacker_faction, target_uid, target_faction)` — beide Seiten eintragen
- `leave_melee(uid, faction)` — beide Seiten bereinigen; prüft ob Gegner noch andere Engagements hat
- `set_charged()` ruft `enter_melee()` auf (kein manuelles `in_melee = True` mehr)
- `set_movement_status(retreated)` ruft `leave_melee()` auf
- `selected_target: tuple | None` → `selected_targets: list[tuple[str, str]]` überall

**Badges:**
- `state_badges_html()` + `_state_badges_html()` lesen `movement_choice` statt `turn_flags`
- NORMAL + STATIONARY Badges jetzt sichtbar (Bug 1 behoben)

**ChargePhase:**
- Multi-Ziel-UI: beliebig viele Ziele per `▷`-Toggle wählbar
- "Charge Successful" trägt alle Ziele als Melee-Engagement ein

**Tests:** 29 neue Tests (test_state_badges.py, test_multi_target.py)

---

## Nächster Schritt: Ziel 3b — combat.py

### Was ist combat.py?

Eine eigenständige Datei `src/gameMechanic/combat.py` die die vollständige
**Angriffs-Auflösung** nach WH40k 9E implementiert (P-08 AttackSequence).

**Ablauf:**
1. Anzahl Angriffe bestimmen (`attacks × models`)
2. Trefferwürfe (`BS` oder `WS`, hit modifier)
3. Verwundungswürfe (`wound_threshold(S, T)`)
4. Rettungswürfe (`save + AP`, Invuln wenn besser)
5. Feel No Pain (wenn vorhanden)
6. Schaden summieren → gibt `(total_dmg, list[str])` zurück

**Signatur (geplant):**
```python
@dataclass
class AttackParams:
    attacks: str           # "D6", "3", "2D6", etc.
    skill: int             # BS or WS (int, already stripped of "+")
    strength: int
    ap: int                # negative, e.g. -1
    damage: str            # "D3", "2", etc.
    hit_modifier: int = 0  # +1 Advance-shoot, -1 etc.; "only_6s" → overwatch special
    num_models: int = 1

@dataclass
class DefendParams:
    toughness: int
    save: int
    invuln_save: int | None
    fnp: int | None        # Feel No Pain (e.g. 5 → 5+)

def resolve_attack(params: AttackParams, defender: DefendParams) -> tuple[int, list[str]]:
    """Returns (total_damage, log_messages)."""
```

**Ziel: ≥ 40 Unit-Tests** für combat.py (kein Streamlit, rein mathematisch/logisch):
```
test_zero_attacks_returns_zero_damage
test_all_hits_miss_returns_zero_damage
test_all_wounds_fail_returns_zero_damage
test_all_saves_pass_returns_zero_damage
test_fnp_can_reduce_damage_to_zero
test_invuln_used_when_better_than_armour
test_double_strength_wounds_on_2plus
...
```

### Ablauf 3b:

1. `src/gameMechanic/combat.py` — `AttackParams`, `DefendParams`, `resolve_attack()`
2. `tests/gameMechanic/test_combat.py` — ≥40 Tests
3. Hilfsfunktionen `can_shoot(unit_state)` und `can_fight(unit_state)`:
   ```python
   def can_shoot(unit_state: dict) -> bool:
       flags = unit_state["turn_flags"]
       return not flags["advanced"] and not flags["retreated"] and not unit_state["in_melee"]

   def can_fight(unit_state: dict) -> bool:
       return bool(unit_state["melee_with"]) or unit_state["turn_flags"]["charged"]
   ```

---

## Ziel 3c — Shooting + Fight Phase (nach 3b)

Sobald combat.py fertig: ShootingPhaseHandler + FightPhaseHandler vollständig implementieren.

**ShootingPhase:**
- `can_shoot(unit_state)` als Gate (Advanced/Retreated/in_melee sperren)
- Ziel-Selektion aus `selected_targets[0]` (ein Ziel pro Schuss-Einheit, Ziel 4 für Mehrfach-Ziele)
- Pro Waffe: `AttackParams` aus Waffendaten, `DefendParams` aus Zieleinheit
- Ergebnis → `active_effect` setzen → LP-Buttons konditionieren (Bug 3)

**FightPhase:**
- `can_fight(unit_state)` als Gate
- Einheiten die `charged == True` kämpfen zuerst
- Ziel aus `selected_targets[0]` (muss in `melee_with` des Angreifers sein)
- `melee_with`-Visualisierung in gameActionDisplayArea

---

## Bug 3 — LP-Buttons Konditionierung (nach 3c)

**Konzept:**
```python
# active_effect Struktur:
{
    "target_uid": "wh40k_9e.necrons.unit.warriors",
    "target_faction": "Necrons",
    "damage": 3,        # oder None wenn Spieler eingeben soll
    "source": "shooting",  # "shooting" | "fight" | "mortal" | "psychic" | "ability"
}
```
LP-Buttons nur anzeigen wenn `active_effect` gesetzt UND `target_uid == uid`.

---

## Design-Block (parallel / eigene Session)

Tailwind-Farbpalette als Python-Konstanten + durchgängiges Designkonzept.
Details siehe letzte Session (unverändert).

---

## Reihenfolge der nächsten Schritte

```
1. Ziel 3b — combat.py (≥40 Tests)           (~2-3h)
2. Ziel 3c — Shooting + Fight Phase (voll)   (~2-3h)
   └── nutzt can_shoot / can_fight
   └── nutzt active_effect für LP-Buttons
3. Bug 3 — LP-Buttons (nach 3c)              (~30min)
4. Design-Block                               (eigene Session)
```

---

## Designentscheidungen die NICHT rückgängig gemacht werden

- `turn_flags` sind REIN für Spielmechanik-Checks (never display logic)
- `movement_choice` ist REIN für Display (never game mechanic checks)
- Ability-Flags leben in `active_buffs` / unit_state-Felder, NICHT in turn_flags
- `melee_with` ist bidirektional — enter_melee und leave_melee pflegen BEIDE Seiten
- `selected_targets` ist eine Liste — nie wieder single-target als Pattern
- LP-Buttons werden nur bei aktivem `active_effect` für die Zieleinheit angezeigt
- `render_player_column()` bleibt in `_common.py` als shared utility
- `can_fight()` prüft `melee_with` (NICHT `in_melee` direkt), weil `melee_with` die Quelle der Wahrheit ist
