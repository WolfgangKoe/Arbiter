# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `src/engine.py` — _unit_state, enter_melee, leave_melee, selected_targets
3. `src/uiLayout/_common.py` — state_badges_html, render_player_column
4. `src/uiLayout/unitCard.py` — _state_badges_html, target-toggle
5. `src/gameMechanic/fightPhase.py` — Stub + _render_display
6. `src/uiLayout/gameProtocoll.py` — aktueller Stand
7. `data/log/game_log.json` — Format der Log-Einträge

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`
Aktueller Branch: `dev`

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A/1B — Struktur + gameObjects | ✅ fertig |
| Ziel 2 — commandPhase + Ability-System | ✅ fertig |
| Ziel 3a — Phase-Infrastruktur | ✅ fertig |
| Bug 1 — NORMAL/STATIONARY Badge | ✅ behoben |
| Multi-Target-Block | ✅ fertig (102 Tests grün) |
| **4 neue Bugs (Session 2026-05-28)** | ⏳ nächste Session |
| Design-Block — Farben | ⏳ eigene Session |
| Ziel 3b — combat.py | ⏳ nach den Bugs |
| Ziel 3c — Shooting + Fight Phase | ⏳ |

---

## SOFORT zu fixen: 4 Bugs (vor Ziel 3b)

### Bug A — Badge-Konflikt: movement_choice + CHARGED

**Problem:** Eine Einheit, die "Normal" bewegt und danach chargert, zeigt NORMAL + CHARGED gleichzeitig. Das ist inhaltlich falsch (Charge ist der relevante Zustand, Normal ist obsolet).

**Fix:** In `state_badges_html()` und `_state_badges_html()` — Bewegungs-Badge überspringen wenn `charged=True`:

```python
# In _common.py state_badges_html():
mc = unit_state.get("movement_choice")
flags = unit_state.get("turn_flags", {})
# Bewegungs-Badge nur zeigen wenn Einheit NICHT gechargt hat
if mc in _MOVEMENT_BADGE and not flags.get("charged"):
    parts.append(_badge(_MOVEMENT_BADGE[mc]))
```

**Dateien:** `src/uiLayout/_common.py`, `src/uiLayout/unitCard.py`
**Tests:** `tests/engine/test_state_badges.py` — Test ergänzen: `test_charged_suppresses_movement_badge`

---

### Bug B — Melee-Paare nicht in gameActionDisplayArea

**Problem:** Nach einem Charge ist nicht sichtbar, welche Einheiten miteinander im Nahkampf sind. Die Fight-Phase-Anzeige zeigt keine Engagement-Übersicht.

**Fix:** In `fightPhase.py` `_render_display()` — wenn kein Angreifer+Ziel selektiert: alle aktiven Melee-Paare durch Scan der unit states anzeigen.

```python
def _render_melee_pairs(state: dict) -> None:
    """Show all active melee engagements from unit states."""
    from engine import _NECRON_UNITS, _ORK_UNITS  # noqa
    pairs: list[str] = []
    necron_states = st.session_state.necron_units
    ork_names = {u.id: u.name_en for u in _ORK_UNITS}
    necron_names = {u.id: u.name_en for u in _NECRON_UNITS}
    for uid, s in necron_states.items():
        for enemy_uid in s.get("melee_with", []):
            pairs.append(f"**{necron_names.get(uid, uid)}** ↔ **{ork_names.get(enemy_uid, enemy_uid)}**")
    if pairs:
        st.markdown("**Active Melee Engagements:**")
        for p in pairs:
            st.markdown(f"- {p}")
    else:
        st.info(PHASE_RULES["fight"])
```

**Datei:** `src/gameMechanic/fightPhase.py`

---

### Bug C — Protocol zeigt kein Game-Log

**Problem:** Tab "📋 Command Protocol" zeigt nur statischen Deployment-Snapshot, nicht die tatsächlich geloggten Aktionen aus `data/log/game_log.json`.

**Format game_log.json** (pro Eintrag):
```json
{ "round": 1, "phase": "movement", "unit": "Big Mek in Mega Armour",
  "action": "movement: advanced", "timestamp": "2026-05-25T..." }
```

**Fix:** `gameProtocoll.py` — `_render_command_protocol()` liest `game_log.json`, gruppiert nach Round+Phase, zeigt als expandable Sections:

```python
# Pseudocode:
entries = load_game_log()  # list[dict] aus JSON
grouped = group_by(entries, key=lambda e: (e["round"], e["phase"]))
for (round_num, phase), items in sorted(grouped.items()):
    with st.expander(f"R{round_num} · {phase.capitalize()}", expanded=False):
        for item in items:
            st.caption(f"**{item['unit']}**: {item['action']}")
```

**Datei:** `src/uiLayout/gameProtocoll.py`
**Kein neuer Log-Mechanismus** — `engine.log_action()` bleibt unverändert.

---

### Bug D — LP-Buttons immer sichtbar (Zwischenfix vor Bug 3)

**Problem:** Wound-Adjustment-Buttons erscheinen für jede selektierte Einheit, unabhängig von Phase. Das ist unübersichtlich.

**Analyse der Abhängigkeit:**
- Bug 3 (aus Plan) ist der saubere Weg: LP-Buttons nur bei `active_effect` (braucht Ziel 3c)
- **Jetzt möglich ohne 3c:** LP-Buttons nur auf der **inaktiven** (Ziel-)Seite zeigen, nicht für die aktive Einheit
  - Semantisch korrekt: Du trägst Schaden beim Gegner ein, nicht bei dir selbst
  - Living Metal / Heilung: läuft über Command Phase Abilities (eigene Buttons)

**Fix:** In `render_player_column()` — `wound_adjustment_buttons` nur im `else`-Zweig (inaktive Seite):

```python
# AKTIVE Seite (is_active == True):
# ... active_content(...) anzeigen
# wound_adjustment_buttons ENTFERNEN

# INAKTIVE Seite (Ziele):
# ... wound_adjustment_buttons BEHALTEN (pro Ziel)
```

**Datei:** `src/uiLayout/_common.py`
**Hinweis:** Wenn später `active_effect` kommt (Bug 3 / nach 3c), wird auch die inaktive Seite konditioniert.

---

## Reihenfolge für nächste Session

```
1. Bug A — Badge-Konflikt (5 min)
2. Bug B — Melee-Paare anzeigen (20 min)
3. Bug C — Protocol-Log aus game_log.json (30 min)
4. Bug D — LP-Buttons Zwischenfix (10 min)
5. Tests aktualisieren (15 min)
   └── test_state_badges.py: test_charged_suppresses_movement_badge
6. Commit: "Fix UX bugs: badge conflict, melee display, protocol log, LP buttons"
7. Ziel 3b — combat.py (≥40 Tests)
```

---

## Designentscheidungen die NICHT rückgängig gemacht werden

- `turn_flags` = Spielmechanik-Checks only
- `movement_choice` = Display only; wird NICHT angezeigt wenn `charged=True`
- `melee_with` bidirektional (enter_melee / leave_melee)
- `selected_targets: list[tuple[str, str]]` — nie wieder single-target
- `can_fight()` prüft `melee_with` ODER `charged` flag
- LP-Buttons: aktive Seite KEIN Button; inaktive Seite (Ziele) ja — bis 3c active_effect kommt
- `render_player_column()` bleibt in `_common.py`

---

## Ziel 3b — combat.py (nach den Bugs)

`src/gameMechanic/combat.py` mit:
```python
@dataclass
class AttackParams:
    attacks: str       # "D6", "3", etc.
    skill: int         # BS/WS als int
    strength: int
    ap: int            # negativ z.B. -1
    damage: str        # "D3", "2", etc.
    hit_modifier: int = 0
    num_models: int = 1

@dataclass
class DefendParams:
    toughness: int
    save: int
    invuln_save: int | None
    fnp: int | None

def resolve_attack(params: AttackParams, defender: DefendParams) -> tuple[int, list[str]]:
    """Returns (total_damage, log_messages)."""
```

Hilfsfunktionen (in `engine.py` oder `combat.py`):
```python
def can_shoot(unit_state: dict) -> bool:
    flags = unit_state["turn_flags"]
    return not flags["advanced"] and not flags["retreated"] and not unit_state["in_melee"]

def can_fight(unit_state: dict) -> bool:
    return bool(unit_state["melee_with"]) or unit_state["turn_flags"]["charged"]
```

Ziel: ≥ 40 Tests in `tests/gameMechanic/test_combat.py`
