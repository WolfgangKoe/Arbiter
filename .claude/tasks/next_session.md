# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — Ziel 3b/3c + neue Blöcke
3. `docs/architecture.md` — aktuell
4. `docs/processes.md` — P-08 (AttackSequence)
5. `src/engine.py` — _unit_state, _reset_turn_state, set_charged
6. `src/gameMechanic/phase_runner.py` + `_common.py` — aktuelle Infrastruktur
7. `src/gameMechanic/shootingPhase.py` + `fightPhase.py` — aktuelle Stubs

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.  
Starten: `streamlit run src/app.py`  
Aktueller Branch: `dev`

```
src/
  app.py
  engine.py                   ← _unit_state (turn_flags), set_charged, reset_turn_flags
  constants/colors.py
  uiLayout/
    _common.py                ← lookup, state_badges_html, render_player_column, PHASE_RULES
    gameActionsArea.py        ← Setup + phase_runner delegation (sehr schlank)
    unitCard.py               ← _state_badges_html (auf turn_flags, NOCH OHNE movement_choice)
    gameProtocoll.py / armyList.py / …
  gameObjects/
    ability.py / unit.py / weapon.py / loader.py / …
  gameMechanic/
    phase_handler.py          ← PhaseHandler Protocol
    phase_runner.py           ← PHASE_REGISTRY + render_current_phase
    commandPhase.py           ← CommandPhaseHandler
    movementPhase.py          ← MovementPhaseHandler (fertig, aber movement_choice fehlt)
    chargephase.py            ← ChargePhaseHandler (nur single-target, muss auf multi-target)
    psychicPhase.py / moralePhase.py
    shootingPhase.py          ← Stub (wird in 3c ersetzt)
    fightPhase.py             ← Stub (wird in 3c ersetzt)
    ability_engine.py         ← TIMING_* Konstanten vorhanden

data/wh40k_9e/
  necrons/ (army.yaml, unit_abilities.yaml, …)
  orks/ _shared/

tests/ — 73 Tests, alle grün (Stand: Ziel 3a)
```

---

## Aktueller Stand (Ziel 3a fertig)

| Ziel | Status |
|------|--------|
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Ziel 2 — commandPhase + Ability-System | ✅ fertig |
| Ziel 3a — Phase-Infrastruktur | ✅ fertig (73 Tests grün) |
| **Bug 1 — STATIONARY/NORMAL Badge** | 🐛 erster Schritt |
| **Multi-Target-Block** | ⏳ vor 3b/3c |
| **Ziel 3b — combat.py** | ⏳ |
| **Ziel 3c — Shooting + Fight Phase** | ⏳ |
| **Design-Block** | ⏳ parallel |

---

## Offene Bugs & neue Anforderungen (aus Session vom 2026-05-27)

### 🐛 Bug 1 — STATIONARY / NORMAL Badge (sofort fixen)

**Problem:** Nach der turn_flags-Migration zeigt unitCard keine Badges für
`Normal`- oder `Stationary`-Bewegung. Nur `ADVANCED` und `RETREATED` erscheinen.

**Lösung — `movement_choice: str | None` in `_unit_state()`:**
```python
"movement_choice": None,  # None | "normal" | "advanced" | "stationary" | "retreated"
```
- Separate vom `turn_flags`-Dict (weil Bewegung ein Single-Choice ist, kein Bool-Flag)
- Badges in `state_badges_html()` und `unitCard._state_badges_html()` auf `movement_choice` umstellen:
  - `None` → kein Bewegungs-Badge (noch nicht bewegt)
  - `"normal"` → NORMAL Badge
  - `"stationary"` → STATIONARY Badge
  - `"advanced"` → ADVANCED Badge
  - `"retreated"` → RETREATED Badge
- `set_movement_status()` in `engine.py` setzt `movement_choice` + `turn_flags`
- `_reset_turn_state()` setzt `movement_choice = None` zurück

**Badges-Design-Entscheidung:**
- Mehrere Flags können gleichzeitig angezeigt werden (z.B. CHARGED + ein Ability-Flag)
- Ability-Flags kommen aus `active_buffs` / `unit_state`-Feldern, NICHT aus `turn_flags`
- `turn_flags` bleiben rein für Spielmechanik-Checks (can_shoot, can_charge etc.)

**Neue Tests (`tests/uiLayout/test_state_badges.py` oder `tests/engine/test_state_badges.py`):**
```
test_no_flags_no_movement_badge
test_movement_choice_normal_shows_normal_badge
test_movement_choice_stationary_shows_stationary_badge
test_movement_choice_advanced_shows_advanced_badge
test_movement_choice_retreated_shows_retreated_badge
test_charged_flag_shows_charged_badge
test_in_melee_no_charged_shows_melee_badge
test_in_reserve_shows_reserve_badge
test_advanced_and_in_reserve_shows_both_badges
test_charged_and_advanced_coexist_shows_both_badges (edge case)
```

---

### Block: Multi-Target (vor 3b/3c)

**Entscheidung (bestätigt):** Vor 3c implementieren, weil 3c (Shooting + Fight) direkt darauf aufbaut.

**Daten-Modell-Änderung:**
```python
# JETZT (falsch):
st.session_state.selected_target = None  # tuple[str, str] | None

# NEU (korrekt):
st.session_state.selected_targets = []   # list[tuple[str, str]]
```

**Regelgrundlage aus schlachtrunden.md:**
- Angriffsphase: "Wähle **eine oder mehrere** feindliche Einheiten innerhalb von 12 Zoll"
- Fernkampfphase: Eine Einheit kann auf mehrere Ziele schießen (pro Waffe ein Ziel)
- Nahkampfphase: Eine Einheit kann mehrere Ziele bekämpfen (wenn in Reichweite)

**Betroffene Dateien:**
- `engine.py`: `init_state()` — `selected_target` → `selected_targets: list`; `_reset_phase_state()` leert Liste
- `gameMechanic/chargephase.py` — Multi-Ziel-UI (mehrere Einheiten anwählbar)
- `gameMechanic/shootingPhase.py` — Ziel-Selektion anpassen (kommt richtig erst in 3c)
- `gameMechanic/fightPhase.py` — Ziel-Selektion anpassen
- `uiLayout/_common.py` — `render_player_column` → `inactive_content` muss auf Liste prüfen
- `uiLayout/unitCard.py` — `selected_targets`-Prüfung für Target-Indikator (▷)
- Tests überall anpassen

---

### Block: Melee-Beziehungen (zusammen mit Multi-Target)

**Entscheidung (bestätigt):** `melee_with: list[str]` per `unit_state`

**Erweiterung `_unit_state()`:**
```python
"melee_with": [],   # list[uid-strings] — gegnerische Einheiten in Engagement
```

**Regeln die das antreibt:**
- Nahkampfphase: Nur Einheiten kämpfen, die innerhalb Nahkampfreichweite (1") einer feindlichen Einheit sind
- Wenn Einheit A zerstört wird: Entfernung aus `melee_with` aller Einheiten die auf A zeigen
- Wenn Einheit A retreated: Entfernt aus Melee + `melee_with` aller beteiligten bereinigen
- Fight Phase: `can_fight(unit_state)` prüft `len(unit_state["melee_with"]) > 0 or turn_flags["charged"]`

**Neue Funktion `engine.py`:**
```python
def enter_melee(attacker_uid: str, attacker_faction: str,
                 target_uid: str, target_faction: str) -> None:
    """Beide Einheiten tragen sich gegenseitig in melee_with ein."""

def leave_melee(uid: str, faction: str) -> None:
    """Einheit verlässt Melee — entfernt sich aus melee_with aller Gegner."""
```

**`set_charged()` nutzt `enter_melee()`** für jeden Charge-Erfolg gegen jedes Ziel.

**Visualisierung in gameActionDisplayArea:**
- Wenn Fight Phase aktiv: Zeige Melee-Paare im Display-Bereich
- "Deactivate" Select-Button für Einheiten die NICHT in `melee_with` des Angreifers sind

---

### Bug 3 — LP-Buttons Konditionierung (nach 3c)

**Entscheidung:** Komplett ausgeblendet wenn kein `active_effect` vorliegt.

**Bestehende Infrastruktur:** `st.session_state.active_effect = None` schon in `init_state()`.

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

**`render_player_column()`-Logik:**
```python
# Statt immer wound_adjustment_buttons zeigen:
active_effect = st.session_state.get("active_effect")
if active_effect and active_effect["target_uid"] == uid:
    wound_adjustment_buttons(faction, uid, unit)
```

**Timing:** Nach 3c implementieren (sobald `resolve_attack_sequence()` ein Ergebnis liefert,
das in `active_effect` landet).

---

### Design-Block (parallel / eigene Session)

**Anforderung:** Tailwind-CSS-Farbpalette importieren + durchgängiges Designkonzept.

**Problem:** Aktuell: Mix aus hardcodierten HEX-Farben in `constants/colors.py`,
inline-Styles in HTML-Badges, und Streamlit-Default-Farben für Buttons.

**Plan:**
1. Tailwind-Farbpalette als Python-Konstanten in `constants/colors.py` definieren
   (Stone, Amber, Red, Purple, Blue als Hauptpalette)
2. Design-Guide erstellen: welche Farbe für was? (aktive Phase, Warnung, Primär-Button, Badge)
3. Alle hardcodierten HEX-Werte durch benannte Konstanten ersetzen
4. Streamlit Custom CSS (`st.markdown(..., unsafe_allow_html=True)`) für Buttons
5. Einheitliche Badge-Farben mit semantischer Bedeutung

**Priorität:** Parallel zu 3b/3c als eigenständige Session, bevor 3c live geht.

---

## Reihenfolge der nächsten Schritte (verbindlich)

```
1. Bug 1 fixen: movement_choice + tests      (~1h)
2. Multi-Target-Block                         (~2h)
   └── selected_targets: list
   └── melee_with: list[str]
   └── enter_melee / leave_melee in engine
   └── ChargePhase auf Multi-Target
3. Design-Block                               (parallel / eigene Session)
4. Ziel 3b — combat.py (≥40 Tests)           (~2-3h)
5. Ziel 3c — Shooting + Fight Phase (voll)   (~2-3h)
   └── nutzt Multi-Target + melee_with
   └── nutzt active_effect für LP-Buttons
6. Bug 3 — LP-Buttons (nach 3c)             (~30min)
```

---

## Designentscheidungen die NICHT rückgängig gemacht werden

- `turn_flags` sind REIN für Spielmechanik-Checks (never display logic)
- `movement_choice` ist REIN für Display (never game mechanic checks)
- Ability-Flags leben in `active_buffs` / unit_state-Felder, NICHT in turn_flags
- `melee_with` ist eine bidirektionale Liste (A weiß von B, B weiß von A)
- `selected_targets` ist eine Liste — nie wieder single-target als Pattern
- LP-Buttons werden nur bei aktivem `active_effect` für die Zieleinheit angezeigt
- `render_player_column()` bleibt in `_common.py` als shared utility
