# Arbiter — UI Layout Specification

> Source: hand-drawn sketches in `Layout_Print/` + design session 2026-05-26
> Status: Reference document for UI Refactoring. TBD items are open design decisions.

---

## 1. Overall Layout

Three-column layout with a fixed top header. Each column scrolls independently.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              gameHeader                                      │
├──────────────────────┬───────────────────────────────┬───────────────────────┤
│   firstPlayer        │      gameActionsArea          │   secondPlayer        │
│   (armyList)         │      (phase-dependent)        │   (armyList)          │
│                      │                               │                       │
│  ┌────────────────┐  │                               │  ┌─────────────────┐  │
│  │   armyCard     │  │                               │  │    armyCard     │  │
│  └────────────────┘  │                               │  └─────────────────┘  │
│  ┌────────────────┐  │                               │  ┌─────────────────┐  │
│  │detachmentCard  │  │                               │  │ detachmentCard  │  │
│  │  ┌──────────┐  │  │───────────────────────────────│  │  ┌───────────┐  │  │
│  │  │ unitCard │  │  │       gameProtocoll           │  │  │ unitCard  │  │  │
│  │  └──────────┘  │  │       (collapsible)           │  │  └───────────┘  │  │
│  │  ┌──────────┐  │  │                               │  │  ┌───────────┐  │  │
│  │  │ unitCard │  │  │                               │  │  │ unitCard  │  │  │
│  │  └──────────┘  │  │                               │  │  └───────────┘  │  │
│  └────────────────┘  │                               │  └─────────────────┘  │
│  ┌────────────────┐  │                               │                       │
│  │detachmentCard  │  │                               │                       │
│  └────────────────┘  │                               │                       │
└──────────────────────┴───────────────────────────────┴───────────────────────┘
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
│  [unitName]  ← clickable → toggles selected state     │
│  ──────────────────────────────────────────────────── │
│  [keyword1] [keyword2] [keyword3] ...                 │
│  ──────────────────────────────────────────────────── │
│  ❤  ████████████░░░░  8 / 10                          │
│  ⬡  ████████████░░░░  8 / 10                         │
│  ──────────────────────────────────────────────────── │
│  [state1] [state2] ...                                │
│  ──────────────────────────────────────────────────── │
│  ▼ phase area  [collapsible]                          │
│  ┌────────────────────────────────────────────────┐   │
│  │ commandPhase:   informations, active abilities │   │
│  │ movementPhase:  move value, allowed actions    │   │
│  │ ...                                            │   │
│  └────────────────────────────────────────────────┘   │
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
│  ──────────────────────────────────────────────────── │
│  HQ                                                   │
│    [unitCard]                                         │
│    [unitCard]                                         │
│  ──────────────────────────────────────────────────── │
│  Troops                                               │
│    [unitCard]                                         │
│  ──────────────────────────────────────────────────── │
│  Elites                                               │
│    [unitCard]                                         │
│  ──────────────────────────────────────────────────── │
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

Center column, upper section. Two sections stacked vertically. Highest dynamic of all components.
The `gameProtocoll` panel (Section 8) is rendered **below** this area as a separate component.

```
┌────────────────────────────────────────────────────────────────────────┐
│  firstPlayerArea (50%)        │  secondPlayerArea (50%)                │
│  ──────────────────────────────────────────────────────────────────────│
│  Main interaction surface     │  Main interaction surface              │
│  for the first player:        │  for the second player:                │
│  active actions + reactions   │  active actions + reactions            │
│  + wound adjustment buttons.  │  + wound adjustment buttons.           │
├────────────────────────────────────────────────────────────────────────┤
│  gameActionDisplayArea (full width)                                    │
│  Combined view of all effects (including passive auras).               │
│  Modifier chain → final result. Phase rules text + attack summary.     │
│  Setup: unit datasheet when a unit is selected.                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Design principles

- **PlayerAreas** are the main interaction surface for each player.
  - Active player: action buttons for selected unit (movement, charge, fight, abilities).
  - Inactive player: target info + reaction buttons (overwatch, stratagems, etc.).
  - Wound adjustment buttons appear in the relevant PlayerArea when an effect targets a unit.
  - Both players may have active buttons simultaneously (e.g. active shoots, inactive reacts).
- **gameActionDisplayArea** is a passive combined result view — not an interaction surface.
  Shows how all effects (including auras) interact and what the final outcome is.
- `uiLayout/gameActionsArea.py` owns the layout. Phase logic is delegated to
  `gameMechanic/<phase>.py` render functions.
- Wound-change buttons are **not** on the unitCard — they live in the PlayerArea.

### Per-phase content

| Phase | firstPlayerArea | secondPlayerArea | displayArea |
|-------|-----------------|------------------|-------------|
| setup | — | — | unit datasheet (when unit selected) or setup instructions |
| command | selected unit + ability buttons + heal | reactions / — | Living Metal results, CP |
| movement | move type buttons + M" value | — | phase rules |
| psychic | PSYKER + power + roll | target + deny | phase rules |
| shooting | attacker + weapon profiles + wound buttons | target T/Sv/++ + wound buttons | attack summary |
| charge | charge declaration + 2D6 | overwatch reaction | phase rules |
| fight | melee attacker + weapons + wound buttons | defender + wound buttons | fight summary |
| morale | morale test + result | — | phase rules |

### Setup — unit datasheet in displayArea

During Setup, clicking a unit name (via the selector button) shows that unit's full datasheet
in the `gameActionDisplayArea`. This lets players review unit profiles before the game starts.

**Datasheet content:** stats table (M · T · Sv · W · ++ · Ld · OC), weapon profiles with
all attributes, keyword list, ability rule texts.

The selector button in unitCard is active in setup phase for this purpose (unlike normal phases
where it drives game actions). Deployment selectbox remains on the unitCard as before.

### Phase stages

Each phase has three stages: **start → active → end**.
The → arrow advances through stages first, then to the next phase (see [processes.md P-03](processes.md)).

| Stage  | Typical effects                                              |
|--------|--------------------------------------------------------------|
| start  | Automatic triggers: Living Metal, CP gain, protocol select   |
| active | Manual player actions: movement, shooting, fight, abilities  |
| end    | Reactive triggers: Reanimation Protocols, morale tests       |

---

## 8. gameProtocoll

Center column, lower section. Tabbed panel — two views, switchable.
One view is never needed while using the other, so tabs are the right pattern.

```
┌──────────────────────────────────────────────────────────┐
│  [📋 Command Protocol]  [⚔️ Stratagems]                  │
│  ──────────────────────────────────────────────────────  │
│  (active tab content below)                              │
└──────────────────────────────────────────────────────────┘
```

---

### 8a. Tab 1 — Command Protocol

Shows the event log filtered by round and phase.

```
┌──────────────────────────────────────────────────────────┐
│  [📋 Command Protocol]  [⚔️ Stratagems]                  │
│  ──────────────────────────────────────────────────────  │
│  Round 2  ·  Phase: Shooting                             │
│  Active player: Necrons                                  │
│  ──────────────────────────────────────────────────────  │
│  [Setup] │ [R1 ▼] │ [R2 ▼] │ ...                         │
│          [com] [mov] [psy] [sho] [cha] [fig] [mor]       │
│  ──────────────────────────────────────────────────────  │
│  · log entry ...                                         │
│  · log entry ...                                         │
│  · ...                                        [⬇ log]    │
└──────────────────────────────────────────────────────────┘
```

#### Navigation model

- Top row: clickable round tabs — `[Setup]` `[R1]` `[R2]` `[R3]` ...
- Sub-row: phase tabs for the selected round — `[com]` `[mov]` ... `[mor]`
- Clicking navigates the log view (read-only for past turns).

#### Immutability rules

- **Within the current turn:** Log for the current phase is still writable (corrections allowed).
- **After a turn ends:** All log entries for that turn are frozen. No changes possible.
- Enforcement is in `gameMechanic/protocol.py`.

---

### 8b. Tab 2 — Stratagems (Gefechtsoption / GO)

Shows all Stratagems available to either player, filtered by current phase and conditions.
No scrolling between both players' GOs is needed — the tab shows both.

```
┌──────────────────────────────────────────────────────────┐
│  [📋 Command Protocol]  [⚔️ Stratagems]                  │
│  ──────────────────────────────────────────────────────  │
│  Necrons · CP: 4                                         │
│  ──────────────────────────────────────────────────────  │
│  [GO name]  CP 1                           [Use]         │  ← clickable
│  [GO name]  CP 2                           [—]           │  ← greyed: CP insufficient
│  [GO name]  CP 1  ✓ used                   [—]           │  ← greyed: used this phase
│  ──────────────────────────────────────────────────────  │
│  Orks · CP: 2                                            │
│  [GO name]  CP 1  (reaction)               [Use]         │
└──────────────────────────────────────────────────────────┘
```

#### GO visibility rules (see also `docs/processes.md P-06`)

| Display state | Condition |
|---------------|-----------|
| shown, **clickable** | conditions met + CP ≥ cost + not yet used this phase |
| shown, **greyed** | conditions met + CP insufficient |
| shown, **greyed** | conditions met + already used this phase |
| **not shown** | conditions not met (wrong phase, stage, or keywords) |

#### GO properties (from `gameObjects/stratagem.py`)

Each GO has: `phase`, `stage` (start/active/end), `player` (active/inactive/both),
`cp_cost`, `conditions` (keyword list), `once_per_phase`.

The `player` field determines who can see and use the GO — a reactive GO (`player: "inactive"`)
only appears for the non-active player and allows them to respond to the active player's action.

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
