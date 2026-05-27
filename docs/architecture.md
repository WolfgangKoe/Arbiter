# Arbiter — Architecture

> Redesigned: 2026-05-26
> Replaces previous plan (domain/ / session/ / ui/).
> UI wireframes and component specs: see `docs/ui_layout.md`.

---

## Vision

One entry point, three bounded modules:

| Module | Responsibility |
|--------|---------------|
| `uiLayout/` | How things look. Streamlit render functions. No game logic. |
| `gameObjects/` | What things are. Pure Python dataclasses + YAML data. No Streamlit. |
| `gameMechanic/` | What things do. Phase logic, state transitions. No Streamlit. |

`app.py` wires them together and is the sole owner of `st.session_state`.

---

## Target Directory Structure

```
src/
  app.py                           ← page config, session_state init, layout assembly

  uiLayout/
    gameHeader.py                  ← VP/CP steppers, game params display
    armyList.py                    ← Player sidebar: armyCard + detachmentCards
    armyCard.py                    ← Faction/subfaction/battleForged + properties display
    detachmentCard.py              ← Detachment header + unitCards grouped by role
    unitCard.py                    ← Name (select trigger), keywords, LP/model bars, states, phase area
    gameActionsArea.py             ← Center canvas (container only; delegated to gameMechanic)
    gameProtocoll.py               ← Round/phase log navigator + download

  gameObjects/
    unit.py                        ← Unit dataclass
    weapon.py                      ← Weapon dataclass
    detachment.py                  ← Detachment dataclass (type, name, slot constraints, units by role)
    faction_property.py            ← FactionProperty dataclass
    keyword.py                     ← Keyword constants / registry (TBD)
    loader.py                      ← YAML loader: reads faction data, resolves weapon references

  gameMechanic/
    state.py                       ← session_state schema, init_state, reset_game, next_phase
    setup.py                       ← Pre-game setup logic (army composition, game params)
    commandPhase.py                ← Command phase: logic + gameActionsArea fill
    movementPhase.py               ← Movement phase: logic + gameActionsArea fill
    psychicPhase.py                ← Psychic phase: logic + gameActionsArea fill
    shootingPhase.py               ← Shooting phase: logic + gameActionsArea fill
    chargePhase.py                 ← Charge phase: logic + gameActionsArea fill
    fightPhase.py                  ← Fight phase: logic + gameActionsArea fill
    moralePhase.py                 ← Morale phase: logic + gameActionsArea fill
    combat.py                      ← Shared: parse_dice, hit_roll, wound_roll, save_roll, damage
    protocol.py                    ← Log writes (append-only within turn), immutability enforcement

data/
  wh40k_9e/
    necrons/
      units.yaml
      weapons.yaml
      wargear.yaml
      relics.yaml
      arkana.yaml
      warlord_traits.yaml
      faction_properties.yaml      ← TBD: Living Metal, Reanimation Protocols, etc.
      subfaction_properties.yaml   ← TBD: Dynasty rules (Nephrekh, Sautekh, etc.)
    orks/
      units.yaml
      weapons.yaml
      ...
    _shared/
      detachment_types.yaml        ← TBD: Patrol/Brigade/etc. with slot constraints
```

---

## Component Responsibilities

### app.py

- `st.set_page_config()`
- Call `gameMechanic/state.py: init_state()` on first load
- Assemble the three-column layout: `gameHeader` | `col_first` | `col_center` | `col_second`
- No game logic. No direct YAML access. Pure wiring.

### uiLayout/

Each file exports one render function: `render_<component>(props) -> None`.
Components receive all data as arguments — no direct `st.session_state` reads inside components.
No game logic in this layer.

**gameActionsArea.py** is structured in three internal sections (see `docs/ui_layout.md §7`):
1. `firstPlayerArea` | `secondPlayerArea` — 50/50 split; main interaction surface per player.
2. `gameActionDisplayArea` — full-width combined effect view (passive, no buttons).
3. `gameProtocoll` tabs — CommandProtocol log | Stratagems GO list.

**unitCard.py** — single selector button per card. No expander, no stats table, no wound buttons.
- Own unit: click = select (`selected_unit`)
- Enemy unit: click = designate target (`selected_target`) in shooting/charge/fight phases
- Wound adjustment buttons live in the PlayerArea of gameActionsArea, not on the card.

### gameObjects/

Pure Python dataclasses. No Streamlit. No session_state.
`loader.py` is the single entry point for reading YAML. No other module reads YAML directly.
All army data flows through the loader; no hardcoded unit lists remain in the codebase.

### gameMechanic/

Each phase file exports two functions:

```python
def resolve_<phase>(state: dict, ...) -> dict:
    # Pure state transition. No Streamlit.

def render_actions_<phase>(state: dict, selected_units: list[str]) -> None:
    # Fills gameActionsArea. Calls st.* here.
```

`state.py` owns the session_state schema. All reads and writes go through helper functions there — no direct `st.session_state["key"]` access scattered across modules.

`combat.py` contains shared attack resolution logic (used by shooting and fight phases).

`protocol.py` appends log entries and enforces immutability: entries for completed turns cannot be modified.

---

## Data Model Concepts (gameObjects)

### Unit

```python
@dataclass
class Unit:
    id: str                          # e.g., "wh40k_9e.necrons.unit.warriors"
    name_en: str
    name_de: str
    faction: str
    subfaction: str | None
    battlefield_role: list[str]      # ["Troops"]
    keywords: list[str]              # ["Infantry", "Necrons", "Living Metal", ...]
    wounds: int                      # base wounds per model
    models_min: int
    models_max: int
    move: int                        # movement in inches
    bs: int                          # ballistic skill (target number)
    ws: int                          # weapon skill (target number)
    strength: int
    toughness: int
    save: int                        # armour save target number
    invuln_save: int | None
    leadership: int
    weapons: list[Weapon]
```

### Weapon

```python
@dataclass
class Weapon:
    id: str
    name_en: str
    weapon_type: str                 # "Rapid Fire", "Heavy", "Assault", "Pistol", etc.
    range_inches: int
    attacks: str                     # e.g., "1", "D6", "2D3"
    strength: int
    ap: int                          # armour penetration (negative = DS modifier)
    damage: str                      # e.g., "1", "D3", "2"
    abilities: list[str]             # free-text ability strings
```

### FactionProperty

```python
@dataclass
class FactionProperty:
    id: str
    name_en: str
    triggers_phase: str              # "command", "shooting", "fight", etc.
    affects_parameter: str           # "wounds", "save", "hit_roll", etc.
    ability_keyword: str             # e.g., "livingMetal", "nephrekhInvuln"
    rule_text: str                   # Human-readable rule shown in armyCard
    applies_to_keyword: str | None   # e.g., "Living Metal" — only units with this keyword
```

### Stratagem (Gefechtsoption / GO)

```python
@dataclass(frozen=True)
class Stratagem:
    id: str
    name_en: str
    cp_cost: int                              # 0 = free
    phase: str                                # "command" | "movement" | ...
    stage: Literal["start", "active", "end"]  # phase stage when it may be used
    player: Literal["active", "inactive", "both"]
    conditions: list[str]                     # keyword conditions for eligibility
    rule_text: str
    once_per_phase: bool = True
```

GO visibility (see `docs/processes.md P-06` and `gameObjects/stratagem.py`):

| State | Condition |
|-------|-----------|
| shown, clickable | conditions met + CP ≥ cost + not yet used this phase |
| shown, greyed | conditions met, but CP < cost OR already used this phase |
| hidden | conditions not met |

---

**Example — Necron Living Metal:**
```yaml
id: necrons.faction.living_metal
name_en: Living Metal
triggers_phase: command
affects_parameter: wounds
ability_keyword: livingMetal
rule_text: "At the start of your Command phase, each NECRONS unit with this ability recovers 1 lost wound."
applies_to_keyword: Living Metal
```

**Example — Nephrekh subfaction:**
```yaml
id: necrons.dynasty.nephrekh.translocation_beams
name_en: Translocation Beams
triggers_phase: [shooting, fight]
affects_parameter: save
ability_keyword: nephrekhInvuln
rule_text: "Models in this unit have a 6+ invulnerable save."
applies_to_keyword: null   # applies to all units in the subfaction
```

### Detachment

```python
@dataclass
class Detachment:
    detachment_type: str                         # "patrol", "brigade", etc.
    name: str                                    # custom or default = type name
    slot_constraints: dict[str, tuple[int,int]]  # role → (min, max)
    units_by_role: dict[str, list[Unit]]         # role → list of units
```

---

## session_state Schema

Owned by `gameMechanic/state.py`. All other modules access state via helper functions.

```python
{
    # Game meta
    "game_title":      str,
    "game_size":       Literal["patrol", "incursion", "strike_force", "onslaught"],
    "game_type":       Literal["matched", "open", "crusade"],
    "current_round":   int,          # 0 = setup not complete
    "current_phase":   str,          # "command" | "movement" | "psychic" | "shooting" | "charge" | "fight" | "morale"
    "first_player":    Literal["p1", "p2"],
    "active_player":   Literal["p1", "p2"],
    "setup_complete":  bool,

    # Score
    "vp": {"p1": int, "p2": int},
    "cp": {"p1": int, "p2": int},

    # Armies
    "armies": {
        "p1": {
            "army_name":             str,
            "faction":               str,
            "subfaction":            str | None,
            "battle_forged":         bool,
            "faction_properties":    list[FactionProperty],
            "subfaction_properties": list[FactionProperty],
            "detachments":           list[Detachment],
        },
        "p2": { ... },  # same structure
    },

    # Phase stage (within the current phase)
    "phase_stage":   Literal["start", "active", "end"],

    # Active effect waiting for player confirmation (None when no effect is pending)
    # Set by gameMechanic phase modules; cleared after player confirms.
    "active_effect": dict | None,    # e.g. {"type": "heal", "target": uid, "amount": 1}

    # Unit runtime state (keyed by unit.id)
    "unit_state": {
        "<unit_id>": {
            "current_wounds":             int,
            "models":                     int,
            "destroyed":                  bool,
            "movement_status":            Literal["stationary", "normal", "advanced", "retreated"],
            "in_melee":                   bool,
            "in_reserve":                 bool,
            "deployment":                 Literal["normal", "stationary", "reserve"],
            "acted_this_phase":           bool,
            "lost_models_this_turn":      int,
            "charged_this_turn":          bool,
            # Ability system
            "my_will_be_done_active":     bool,
            "active_buffs":               list[str],
            "models_lost_since_last_rp":  int,
        }
    },

    # Selection
    "selected_unit":   tuple[str, str] | None,  # (faction, unit_id)
    "selected_target": tuple[str, str] | None,  # (faction, unit_id)

    # Protocol
    "game_log":       list[dict],    # append-only log entries; see protocol.py
    "turns_frozen":   list[int],     # round numbers whose logs are immutable
}
```

---

## Interaction Model — Unit Selection Flow

```
User clicks unitName (unitCard in sidebar)
        │
        ▼
gameMechanic/state.py  →  toggle selected_units[unit_id]
        │
        ▼
app.py  →  gameActionsArea.py  →  dispatch on current_phase
        │
        ├── command  → commandPhase.render_actions_command(state, selected_units)
        ├── movement → movementPhase.render_actions_movement(state, selected_units)
        ├── shooting → shootingPhase.render_actions_shooting(state, selected_units)
        └── ...
```

- **Select is only active** when `setup_complete == True`.
- **Multi-select:** Allowed or blocked per phase — determined by each gameMechanic phase module.
  - Example shooting: one attacker, one target → max 2 units selected (one per side).
  - Example fight: alternating, so only the active unit is relevant.
  - TBD per phase.
- **Wound-change buttons** appear in gameActionsArea when a unit is selected, not on the unitCard.

---

## Phase Stubs

Each phase must be individually designed before implementation. Below: known rules + open TBDs.

### commandPhase

**Known:**
- +1 CP if Battle-Forged (Schlachtordnung-BP-Bonus)
- factionProperties with `triggers_phase = "command"` are resolved: e.g., Living Metal → +1 wound on each eligible unit
- CP can be spent for Stratagems (TBD)

**gameActionsArea:** List of active abilities + their effects. Heal/apply buttons per ability.

**TBD:** Stratagem UI, NOBLE command aura interactions, full ability list per faction

---

### movementPhase

**Known:**
- Move types: normal move / advance / stationary / fall back
- Normal: up to M" — cannot end in melee range
- Advance: up to M+D6" — blocks shooting and charging this turn
- Fall back: up to M" out of melee — blocks shooting, charging, psychic
- FLY keyword: ignores vertical distance and other models
- Reinforcements: deploy from reserve (available from round 2)

**State changes:** `movement_status`, `advanced`, `fell_back`

**gameActionsArea:** Move type selector, M" display, advance roll, reserve deploy button

**TBD:** Terrain interaction UI, advance roll integration, exact column layout

---

### psychicPhase

**Known:**
- Only PSYKER units act
- Manifest: 2D6 ≥ warp charge value
- Deny: enemy PSYKER within 24", 2D6 > manifest roll
- Perils of the Warp: double-1 or double-6 → D3 mortal wounds on caster
- Smite: warp charge 5, D3 mortal wounds (D6 on roll 11+)

**gameActionsArea:** PSYKER selector, power selector, roll display, deny response panel

**TBD:** Full psychic power library scope (Smite only, or full 9E lists), multi-PSYKER flow

---

### shootingPhase

**Known:**
- Full attack sequence: hit roll → wound roll → save roll → damage
- Hit roll: D6 ≥ BS (or WS for melee); unmodified 6 always hits, 1 always misses
- Wound roll: D6 vs S/T table (2+ to 6+); unmodified 6 always wounds, 1 always fails
- Save roll: D6 + DS modifier ≥ armour save; invuln save never modified by DS
- Damage: weapon damage value; excess normal damage is lost; mortal wound excess carries over
- Modifiers: net maximum ±1 per roll
- Blocked by: advanced, fell back, in melee (attacker), target in melee with friendly (cannot target)

**gameActionsArea (two columns):**
- Left: attacker + weapon profile + hit/wound modifier buttons + result
- Right: target + T/Save values + damage tracker

**TBD:** Multi-target shooting, Rapid Fire at half range, Heavy weapon stationary bonus, Blast weapons

---

### chargePhase

**Known:**
- Eligible: within 12" of enemy, not advanced, not fell back
- Declare charge targets (can name multiple)
- 2D6 charge roll: must reach base-to-base with all declared targets
- Overwatch: defender can shoot back — only unmodified 6s hit
- Heroic Intervention: defender CHARACTERS within 3" horizontal / 5" vertical can move 3" to engage
- Charged units get `charged_this_turn = True` → fights first in fight phase

**gameActionsArea:** Charge declaration, 2D6 roll trigger, range check, overwatch response

**TBD:** Full overwatch flow (CP spend for defensive options), heroic intervention UI, multi-target charge

---

### fightPhase

**Known:**
- Charged units fight first; then alternating starting with non-active player
- Pile in: 3" move, must end closer to nearest enemy
- Attack sequence: same as shooting but uses WS instead of BS
- Consolidation: 3" move after fighting, must end closer to nearest enemy
- Units fight at most once per fight phase

**gameActionsArea (two columns):**
- Left: active melee unit + weapon profiles + WS modifier
- Right: target unit + T/Save + damage tracker

**TBD:** Fights-last keyword, multi-unit melee pile-in UI, consolidation move

---

### moralePhase

**Known:**
- Any unit that lost models this turn must take a morale test
- Roll D6 + models lost this turn; if result > Leadership → additional models removed = result − Ld
- Units of 1 model are exempt

**gameActionsArea:** List of eligible units + morale test button + result + models-removed display

**TBD:** Insane Bravery (CP spend to auto-pass), FEARLESS keyword, ATSKNF

---

## Colour System

Tailwind v3 palette extracts — **no Tailwind framework dependency**.
Defined in `src/constants/colors.py`. Injected once as custom CSS in `app.py`.

| Alias | Colour | Use |
|-------|--------|-----|
| `COLOR_ACTION` | Emerald-500 `#10b981` | Own actions and positive effects |
| `COLOR_STATUS` | Neutral-400 `#a3a3a3` | Neutral status information |
| `COLOR_WARNING` | Amber-500 `#f59e0b` | Enemy presence, caution |
| `COLOR_CRITICAL` | Red-500 `#ef4444` | Critical buttons and danger info |
| `COLOR_EFFECT` | Blue-500 `#3b82f6` | Abilities, guidelines, passive effects |

---

## Refactoring Plan

### Phase 0 — Documentation ✅ (this session)
- `docs/ui_layout.md` — wireframes + component specs
- `docs/architecture.md` — this file

### Phase 1 — Structural split of ui.py (no behavior change)
Split `src/ui.py` into `src/uiLayout/`:
- `gameHeader.py`
- `armyList.py` · `armyCard.py` · `detachmentCard.py` · `unitCard.py`
- `gameActionsArea.py` (container stub, delegates as before)
- `gameProtocoll.py`

All existing tests must remain green. Zero logic changes.

### Phase 2 — gameObjects (Army Abstraction)
- Create `src/gameObjects/` with dataclasses: `unit.py`, `weapon.py`, `detachment.py`, `faction_property.py`
- Write `loader.py`: reads YAML, resolves weapon ID references
- Write `data/wh40k_9e/_shared/detachment_types.yaml`
- Write `data/wh40k_9e/necrons/faction_properties.yaml` + `subfaction_properties.yaml`
- Migrate Necrons + Orks: remove hardcoded dicts from `models.py`, load from YAML via loader

### Phase 3 — gameMechanic (Phase Logic)
- Create `src/gameMechanic/` with `state.py`, `combat.py`, `protocol.py`
- Implement phases one at a time, starting with the simplest:
  `command → movement → shooting → fight → charge → morale → psychic`
- Each phase: design gameActionsArea layout → implement phase module → write tests → verify in app

### Phase 4 — Army Builder (TBD)
- Options: import from file / in-app builder / hardcoded presets
- Prerequisite: Phase 2 complete
- Decision deferred until Phase 2 is running

---

## Open Design Questions

| # | Question | Impact |
|---|----------|--------|
| 1 | Army Builder: file import vs. in-app builder vs. presets? | loader.py, setup.py |
| 2 | gameActionsArea column layout: exact ratio and behavior per phase? | uiLayout/gameActionsArea.py |
| 3 | Multi-select logic: which phases allow selecting multiple units? | gameMechanic per phase |
| 4 | Stratagem system: data model + UI for CP spend and stratagem effects? | gameObjects + gameMechanic |
| 5 | gameProtocoll log schema: exact fields per phase? | protocol.py |
| 6 | CP initial values: confirm per game size (Patrol/Incursion/Strike Force/Onslaught) | state.py, gameHeader |
| 7 | Psychic power library scope: Smite only, or full 9E power lists? | gameObjects + psychicPhase |
| 8 | Detachment slot constraints: verify exact numbers from Wahapedia | detachment_types.yaml |

---

## Erkenntnisse aus `backend/` (2026-05-26)

Der `backend/`-Ordner enthielt eine fertige Domänenlogik-Bibliothek (`tabletop`). Er wurde nach Extraktion der nützlichen Konzepte gelöscht. Die folgenden Teile sind direkt relevant für `gameObjects/` und `gameMechanic/`.

### `WeaponProfile` → `gameObjects/weapon.py`

Das Backend-Modell ist produktionsreif und passt fast unverändert:

```python
@dataclass(frozen=True)
class WeaponProfile:
    name_en: str
    name_de: str
    range_value: str       # z.B. "24", "Melee"
    weapon_type: str       # z.B. "Rapid Fire 1", "Heavy 3", "Assault D6"
    strength: str          # als String — z.B. "4", "User", "×2"
    ap: str                # als String — z.B. "0", "-1", "-3"
    damage: str            # als String — z.B. "1", "D3", "D6"
    ability_text: str      # Freitext-Sonderregel
```

Alle Werte als `str` statt `int` — das ist richtig, da viele Werte Würfelausdrücke oder Sonderfälle sind.

### `Rule` + `RuleVersionSet` → Pattern für `FactionProperty`

Das Backend versioniert Regeltexte in drei Modi: `original` / `current` / `overlay`.
Dieses Muster sollte für `FactionProperty.rule_text` übernommen werden — spätere Regelkorrekturen können so als Overlay eingebracht werden, ohne den Original-Text zu überschreiben.

```python
@dataclass(frozen=True)
class RuleVersionSet:
    original: RuleVersion
    current: RuleVersion
    overlay: RuleVersion | None = None

    def resolve(self, mode: str) -> RuleVersion: ...
```

### `Stratagem` → `gameObjects/stratagem.py` (Ziel 4)

Fertige Datenstruktur, direkt übernehmen:

```python
@dataclass(frozen=True)
class Stratagem:
    id: str
    name_de: str
    cp_cost: int
    text_de: str
    applies_to_keywords: list[str]
```

### `rule_eligibility.py` → Keyword-Dispatcher in `gameMechanic/`

Das Backend hat eine vollständige, getestete Logik für die Frage:
*„Gilt diese Regel für diese Einheit in diesem Kontext?"*

Matching-Kriterien: `faction`, `dynasty` (= subfaction), `unit_source_en`, `unit_keywords`.
Unterstützt: Ausschlüsse (`excluded_units`, `excluded_keywords`), Anforderungen (`keyword_any`, `keyword_none`, `warlord_keyword`).

Diese Logik **nicht neu schreiben**. Stattdessen bei Implementierung des Keyword-Dispatchers in `gameMechanic/` direkt adaptieren — die `RuleEvaluationContext`-Struktur passt 1:1 auf unseren `unit_state` + `army`-Kontext.

### YAML-Loader-Pattern → `gameObjects/loader.py`

Der Backend-Loader (`YamlDatasheetRepository`) zeigt das richtige Muster:
- Profile-basierte Pfadauflösung (kein hartcodierter Pfad)
- Overlay-Unterstützung für Regelkorrekturen
- Waffen-IDs werden bei Laden aufgelöst (keine ID-Referenzen im Laufzeit-Objekt)

Für `loader.py` in Ziel 1B: gleiche Prinzipien übernehmen, aber ohne die Crusade-spezifische Schichtung (ports/use_cases) — Streamlit braucht keine hexagonale Architektur.
