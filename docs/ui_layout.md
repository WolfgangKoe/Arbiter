# Arbiter — UI Layout Specification

> Source: hand-drawn sketches in `Layout_Print/` + design session 2026-05-26
> Status: Reference document for UI Refactoring. TBD items are open design decisions.

---

## 1. Overall Layout

Three-column layout with a fixed top header. Each column scrolls independently.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              gameHeader                                      │
├──────────────────────┬──────────────────────────────┬───────────────────────┤
│   firstPlayer        │      gameActionsArea          │   secondPlayer        │
│   (armyList)         │      (phase-dependent)        │   (armyList)          │
│                      │                               │                       │
│  ┌────────────────┐  │                               │  ┌─────────────────┐  │
│  │   armyCard     │  │                               │  │    armyCard     │  │
│  └────────────────┘  │                               │  └─────────────────┘  │
│  ┌────────────────┐  │                               │  ┌─────────────────┐  │
│  │detachmentCard  │  │                               │  │ detachmentCard  │  │
│  │  ┌──────────┐  │  │───────────────────────────────│  │  ┌───────────┐  │  │
│  │  │ unitCard │  │  │       gameProtocoll            │  │  │ unitCard  │  │  │
│  │  └──────────┘  │  │       (collapsible)            │  │  └───────────┘  │  │
│  │  ┌──────────┐  │  │                               │  │  ┌───────────┐  │  │
│  │  │ unitCard │  │  │                               │  │  │ unitCard  │  │  │
│  │  └──────────┘  │  │                               │  │  └───────────┘  │  │
│  └────────────────┘  │                               │  └─────────────────┘  │
│  ┌────────────────┐  │                               │                       │
│  │detachmentCard  │  │                               │                       │
│  └────────────────┘  │                               │                       │
└──────────────────────┴──────────────────────────────┴───────────────────────┘
```

**Column widths:** TBD — estimate ~25% / ~50% / ~25%
**Scroll:** Each column independent.
**Target devices:** Tablet/desktop landscape. No mobile optimization.

---

## 2. gameHeader

Fixed bar across the full width at the top.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  VP [+5][-5]  X=0    │  Arbiter · gameTitel  │  gameSize  │  gameType  │  VP [+5][-5]  X=0   │
│  CP [+1][-1]  Y=…    │                       │            │            │  CP [+1][-1]  Y=…   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Properties

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `vp_p1` | int | 0 | Victory Points, firstPlayer |
| `vp_p2` | int | 0 | Victory Points, secondPlayer |
| `cp_p1` | int | gameSize-dependent | Command Points, firstPlayer |
| `cp_p2` | int | gameSize-dependent | Command Points, secondPlayer |
| `game_title` | str | "" | Optional custom game name |
| `game_size` | enum | — | Patrol / Incursion / Strike Force / Onslaught |
| `game_type` | enum | matched | matched / open / crusade |
| `current_round` | int | 0 | 0 = Setup not yet complete |
| `current_phase` | str | — | see phase list |

### Controls

- **VP stepper:** `[+5]` / `[−5]` per player. Step size = 5 (typical scoring is 5 / 10 / 15 VP).
- **CP stepper:** `[+1]` / `[−1]` per player. Step size = 1.
- **X** (VP value) starts at 0.
- **Y** (CP value) starts at a value determined by `game_size` during setup — TBD, see note below.
- `game_size` and `game_type` are set in the setup screen and not changeable mid-game.

### CP Starting Values by gameSize (TBD — verify against Wahapedia)

| gameSize | CP start |
|----------|----------|
| Patrol | 3 |
| Incursion | 4 |
| Strike Force | 5 |
| Onslaught | 6 |

---

## 3. armyCard

Displayed once at the top of each player's armyList. Read-only display, no interaction.

```
┌──────────────────────────────────────────────┐
│  armyName                                    │
│  (default: "{faction} — {subfaction}")       │
│  ──────────────────────────────────────────  │
│  [Faction]  [Subfaction]  [Battle-Forged]    │
│  ──────────────────────────────────────────  │
│  factionProperty ▸  <rule name / text>       │
│  subfactionProperty ▸  <rule name / text>    │
└──────────────────────────────────────────────┘
```

### Properties

| Property | Type | Notes |
|----------|------|-------|
| `army_name` | str | Custom name; default = "{faction} — {subfaction}" |
| `faction` | str | e.g., "Necrons" |
| `subfaction` | str \| None | e.g., "Nephrekh" |
| `battle_forged` | bool | Badge shown only if True |
| `faction_properties` | list[FactionProperty] | From gameObjects data |
| `subfaction_properties` | list[FactionProperty] | From gameObjects data |

### FactionProperty display

Each property is shown as: name and short rule text. Not clickable.
The phase/parameter data is stored in gameObjects but not surfaced as interactive UI here.

**Examples (Necrons):**
- factionProperty — *Living Metal:* "At the start of your Command phase, each NECRONS unit recovers 1 lost wound."
- subfactionProperty (Nephrekh) — *Translocation Beams:* "Models have a 6+ invulnerable save." *(triggers in: shooting, fight)*

---

## 4. unitCard

One card per unit. Displayed inside a detachmentCard, grouped by battlefield role.

```
┌───────────────────────────────────────────────────────┐
│  [unitName]  ← clickable → toggles selected state    │
│  ─────────────────────────────────────────────────── │
│  [keyword1] [keyword2] [keyword3] ...                 │
│  ─────────────────────────────────────────────────── │
│  LP  ████████████░░░░  8 / 10                         │
│  ⬡   ████████████░░░░  8 / 10                         │
│  ─────────────────────────────────────────────────── │
│  [state1] [state2] ...                                │
│  ─────────────────────────────────────────────────── │
│  ▼ phase area  [collapsible]                          │
│  ┌───────────────────────────────────────────────┐   │
│  │ commandPhase:   informations, active abilities │   │
│  │ movementPhase:  move value, allowed actions    │   │
│  │ ...                                            │   │
│  └───────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────┘
```

### Interaction

- **Click unitName:** Toggles `selected` state for this unit.
  - Only active after Setup is complete (`setup_complete = True`).
  - Selected units feed into `gameActionsArea` — content there is driven by phase + selected units.
  - Whether multi-select is allowed depends on the phase and keyword logic (defined per-phase in gameMechanic).
- **LP-bar + model-bar:** Display only. Wound-change buttons move to `gameActionsArea` when unit is selected.
- **Phase area:** Collapsible per unit. Content is phase-driven (rendered by gameMechanic phase modules).

### LP-bar / model-bar

Stays coupled as currently implemented: LP = total remaining wounds summed across models; model count decrements when a model reaches 0 wounds. No per-model individual tracking in the sidebar.

### State badges

| State key | Badge label | When shown |
|-----------|-------------|------------|
| `destroyed` | DESTROYED | wounds_remaining == 0 |
| `in_reserve` | RESERVE | deployment_status == "reserve" |
| `in_melee` | ENGAGED | in melee range of enemy unit |
| `charged_this_turn` | CHARGED | charged this turn → fights first in fight phase |
| `advanced` | ADVANCED | advanced in movement phase → cannot shoot / charge |
| `fell_back` | FELL BACK | fell back → cannot shoot / charge / use psychic |
| `acted_this_phase` | ACTED | already acted in current phase |
| `stationary` | STATIONARY | did not move → Heavy weapons fire without penalty |

### Dynamic area — content per phase

| Phase | informations | actions (TBD) |
|-------|-------------|---------------|
| command | active abilities, heal amounts | TBD |
| movement | move value (M"), allowed move types | move type selector |
| psychic | PSYKER abilities if applicable | manifest / deny |
| shooting | ranged weapon profiles | target select |
| charge | charge eligibility (within 12"), targets | charge declaration |
| fight | melee weapon profiles, fights-first flag | attack |
| morale | morale value, models lost this turn | test trigger |

---

## 5. detachmentCard

Groups the units of one detachment by battlefield role.

```
┌───────────────────────────────────────────────────────┐
│  [detachmentType]  detachmentName                     │
│  (e.g.,  "Patrol"  ·  "My Custom Name")               │
│  ─────────────────────────────────────────────────── │
│  HQ                                                   │
│    [unitCard]                                         │
│    [unitCard]                                         │
│  ─────────────────────────────────────────────────── │
│  Troops                                               │
│    [unitCard]                                         │
│  ─────────────────────────────────────────────────── │
│  Elites                                               │
│    [unitCard]                                         │
│  ─────────────────────────────────────────────────── │
│  ...                                                  │
└───────────────────────────────────────────────────────┘
```

### Properties

| Property | Type | Notes |
|----------|------|-------|
| `detachment_type` | str | e.g., "patrol", "brigade" |
| `detachment_name` | str | Custom name; default = type name |
| `units_by_role` | dict[str, list[Unit]] | Battlefield role → units |
| `slot_constraints` | dict[str, tuple[int,int]] | role → (min, max); reference only |

### Battlefield roles (from units.yaml `keywords.battlefield_role`)

HQ · Troops · Elites · Fast Attack · Heavy Support · Flyer · Dedicated Transport · Lord of War

Roles with 0 units assigned are hidden.

### Detachment types and slot constraints

Defined in `gameObjects/detachment_types.yaml` (TBD). Constraints are informational (shown as reference during setup; not enforced mid-game).

| Type | HQ | Troops | Elites | Fast Attack | Heavy Support | Flyer | DT |
|------|----|--------|--------|-------------|---------------|-------|----|
| Patrol | 1–2 | 0–2 | 0–2 | 0–2 | 0–2 | 0–1 | 0–2 |
| Battalion | 2–3 | 3–5 | 0–6 | 0–3 | 0–3 | 0–2 | 0–3 |
| Brigade | 2–5 | 3–6 | 3–5 | 2–5 | 3–5 | 0–2 | 0–3 |
| Spearhead | 1–2 | 0–1 | 0–2 | 0–2 | 3+ | 0–1 | 0–2 |
| Outrider | 1–2 | 0–1 | 0–2 | 3+ | 0–2 | 0–1 | 0–2 |
| Vanguard | 1–2 | 0–1 | 3+ | 0–2 | 0–2 | 0–1 | 0–2 |
| Air Wing | — | — | — | — | — | 3+ | — |
| Super-Heavy | — | — | — | — | — | — | — |

> Verify exact numbers against Wahapedia. Add LoW column for Super-Heavy.

---

## 6. armyList (full sidebar)

```
┌──────────────────────────────────────────────────────────┐
│                      armyCard                            │
├──────────────────────────────────────────────────────────┤
│  detachmentCard  (Patrol · "Main Force")                 │
│    HQ                                                    │
│      unitCard  [Overlord]                                │
│    Troops                                                │
│      unitCard  [Necron Warriors]                         │
│      unitCard  [Necron Warriors]                         │
│    Heavy Support                                         │
│      unitCard  [Doomsday Ark]                            │
├──────────────────────────────────────────────────────────┤
│  detachmentCard  (Outrider · "Flanking Force")           │
│    HQ                                                    │
│      unitCard  [Destroyer Lord]                          │
│    Fast Attack                                           │
│      unitCard  [Canoptek Wraiths]                        │
│      unitCard  [Scarab Swarms]                           │
└──────────────────────────────────────────────────────────┘
```

Both sidebars are structurally identical — firstPlayer left, secondPlayer right. armyList is the container for 1–n detachmentCards, each of which contains unitCards grouped by role.

Typical army: 1 detachment. Large games (Onslaught): up to 3+ detachments.

---

## 7. gameActionsArea

Center column, upper section. Completely replaced per phase. Highest dynamic of all components.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  gameActionsArea  [phase: movementPhase]                                  │
│  ────────────────────────────────────────────────────────────────────── │
│                                                                          │
│   [  PHASE-SPECIFIC CONTENT                                           ]  │
│   [  Rendered by gameMechanic/<phase>.py                              ]  │
│   [  Two-column layout expected for most phases (TBD per phase)       ]  │
│   [  Container only in uiLayout — logic lives in gameMechanic         ]  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Design principles

- Content is determined by: current phase + selected unit(s) + unit keywords + faction/subfaction properties + game state.
- `uiLayout/gameActionsArea.py` is the container. It delegates to the relevant `gameMechanic/<phase>.py` render function.
- Two-column layout expected (e.g., attacker left / target right) but not final — designed per phase.
- Wound-change buttons appear here when a unit is selected (not on the unitCard).

### Conceptual base value modification pattern (from sketch)

When a combat roll is involved:

```
[unit profile]    ±  modifier    =   [ result ]
[weapon profile]
────────────────────────────────────────────────
ability / inform.:   [+1]   [−1]
```

### Per-phase content sketch

| Phase | Left area | Right area |
|-------|-----------|------------|
| command | selected unit + active abilities | heal preview, CP options |
| movement | selected unit + move type options + M" value | reserve deploy (if applicable) |
| psychic | PSYKER unit + power selector + roll | target unit + deny attempt |
| shooting | attacker + weapon profile(s) + hit modifier | target unit + toughness/save + damage |
| charge | selected unit + 2D6 roll trigger + range check | target unit(s) within 12" |
| fight | active melee unit + weapon profiles + KG modifier | target unit + save + damage |
| morale | units with model losses + D6+losses vs Ld | test result, models removed |

> Each phase must be individually designed before implementation. This is a free canvas until then.

---

## 8. gameProtocoll

Center column, lower section. Collapsible. Shows the event log filtered by round and phase.

```
┌──────────────────────────────────────────────────────────┐
│  gameProtocoll                          [▼ collapse]     │
│  ──────────────────────────────────────────────────────  │
│  [Setup] │ [R1 ▼] │ [R2 ▼] │ [R3 ▼] │ ...              │
│                [com] [mov] [psy] [sho] [cha] [fig] [mor] │
│  ──────────────────────────────────────────────────────  │
│  · log entry ...                                         │
│  · log entry ...                                         │
│  · ...                                                   │
│                                      [⬇ Download log]   │
└──────────────────────────────────────────────────────────┘
```

### Navigation model

- Top row: clickable round tabs — `[Setup]` `[R1]` `[R2]` `[R3]` ...
- Sub-row: phase tabs for the selected round — `[com]` `[mov]` `[psy]` `[sho]` `[cha]` `[fig]` `[mor]`
- Clicking navigates the log view (read-only for past turns).

### Immutability rules

- **Within the current turn:** Navigating back to a previous phase shows its log and allows corrections (e.g., wrong move type, missed VP/CP adjustment). The log for that phase is still writable.
- **After a turn ends:** All log entries for that turn are frozen. No changes possible.
- Enforcement is in `gameMechanic/protocol.py`.

### What is logged per phase (TBD — to be defined as each phase is implemented)

| Phase | Log entry content |
|-------|------------------|
| setup | army composition, game size, game type, first player, initial CP |
| command | abilities triggered, wounds healed, CP gained/spent |
| movement | each unit: move type chosen, distance, reserve deployments |
| psychic | manifest attempts + rolls + outcomes, deny attempts |
| shooting | per unit: target, weapon, hits, wounds, saves, damage |
| charge | charge declarations, 2D6 rolls, success/fail, overwatch |
| fight | per unit: target, hits, wounds, saves, damage, consolidation |
| morale | per unit tested: roll + modifier, pass/fail, models removed |

### Download

- Exports `data/log/game_log.json`.
- Button always visible at footer of gameProtocoll.
- Export format: TBD (JSON or human-readable text).
