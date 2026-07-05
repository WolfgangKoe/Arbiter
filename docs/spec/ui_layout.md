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

Fixed bar across the full width at the top. **Read-only display** — no adjustment buttons.
VP and CP are modified exclusively inside the game phases, not from the header.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  VP  X=0    │  Arbiter · gameTitel  │  gameSize  │  gameType  │  VP  X=0   │
│  CP  Y=…    │                       │            │            │  CP  Y=…   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Properties

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `vp_p1` | int | 0 | Victory Points, firstPlayer — display only |
| `vp_p2` | int | 0 | Victory Points, secondPlayer — display only |
| `cp_p1` | int | gameSize-dependent | Command Points, firstPlayer — display only |
| `cp_p2` | int | gameSize-dependent | Command Points, secondPlayer — display only |
| `game_title` | str | "" | Optional custom game name |
| `game_size` | enum | — | Patrol / Incursion / Strike Force / Onslaught |
| `game_type` | enum | matched | matched / open / crusade |
| `current_round` | int | 0 | 0 = Setup not yet complete |
| `current_phase` | str | — | see phase list |

### Where VP and CP are modified

| Stat | Where modified | Notes |
|------|---------------|-------|
| VP | gameActionsArea — dedicated VP phase (Command or other, see Setup) | +5/−5 steppers appear at end of the configured scoring phase |
| CP | gameActionsArea — Command Phase (Grant +1 CP button) | Additional CP via abilities or Setup screen (initial value) |

### VP Scoring Phase (configured in Setup)

The player selects at which phase end VPs are counted:
`Command Phase` / `Movement Phase` / `Psychic Phase` / `Shooting Phase` / `Charge Phase` / `Fight Phase` / `Morale Phase`

At the end of the chosen phase, VP adjustment buttons (+5 / −5) appear in the gameActionsArea for both players.

### CP Starting Values by gameSize

| gameSize | CP start |
|----------|----------|
| Patrol | 3 |
| Incursion | 6 |
| Strike Force | 12 |
| Onslaught | 18 |

---

## 3. armyCard

Displayed once at the top of each player's armyList. Shows faction identity and army-wide ability buttons.

```
┌──────────────────────────────────────────────┐
│  armyName                                    │
│  (default: "{faction} — {subfaction}")       │
│  ──────────────────────────────────────────  │
│  [{faction}]  [{subfaction}]                 │
│  ──────────────────────────────────────────  │
│  [Ability Button]   (phase-dependent)        │
│  [Ability Button]   (phase-dependent)        │
└──────────────────────────────────────────────┘
```

The card has a visible thin border.

### Properties

| Property | Type | Notes |
|----------|------|-------|
| `army_name` | str | Custom name; default = "{faction} — {subfaction}" |
| `faction` | str | Main faction keyword, e.g. "Necrons" |
| `subfaction` | str \| None | Subfaction keyword chosen at army build, e.g. "Nephrekh" |
| `faction_abilities` | list[Ability] | Loaded from faction_abilities.yaml |

### Faction keyword badges

Two badges are shown:
- **faction badge** — the main faction keyword (e.g. "Necrons", "Orks")
- **subfaction badge** — the chosen subfaction keyword (e.g. "Nephrekh", "Bad Moons")

These are the only two faction-level keywords shown here. Further subfaction keywords (e.g. sub-cult or dynasty variants) are intentionally omitted as no army-wide abilities target them.

### Ability buttons (TriggeredAbility vs. ActivatedAbility)

Army abilities fall into two categories:

| Type | Behaviour | Shown when |
|------|-----------|------------|
| `triggered` | Auto-fires when trigger conditions are met; button appears to confirm/apply | Current phase matches `trigger.phase` AND all conditions met |
| `activated` | Must be deliberately chosen by the player | Per-unit selection (not in armyCard) |

`triggered` ability buttons appear in the armyCard only for the active player, only in the matching phase.

**Examples:**
- *Triggered (command phase):* faction heal ability — button visible at start of command phase when any eligible unit has lost wounds.
- *Triggered (shooting + fight phase):* faction reanimate ability — button visible after enemy attacks when conditions are met.
- *Activated:* unit-specific abilities (e.g. character commands, one-use items) — shown in gameActionsArea when the relevant unit is selected, not in armyCard.

### actionArea context when no unit is selected

When no unit is selected, the playerArea in gameActionsArea shows which faction and unit abilities are available in the current phase — so the area is never empty.

---

## 4. unitCard

One card per unit. Displayed inside a detachmentCard, grouped by battlefield role.
The card has a visible thin border so state badges are unambiguously grouped with their unit.

```
┌───────────────────────────────────────────────────────┐
│  ❤  ████████████░░░░  8 / 10                          │
│  ⬡  ████████████░░░░  8 / 10                         │
│  ──────────────────────────────────────────────────── │
│  [unitName]  ← clickable → toggles selected state     │
│  ──────────────────────────────────────────────────── │
│  [state1] [state2] ...                                │
│  [keyword1] [keyword2] [keyword3] ...                 │
└───────────────────────────────────────────────────────┘
```

**Layout rationale:** bars at the top give an immediate health read before the name.
State badges sit directly below the name — visually bound to this unit, not the one below.

### Keyword display rules

- The **main faction keyword** (`unit.faction`, e.g. the army's top-level faction) is **not shown** on the unitCard — it is shown once in the armyCard.
- The **subfaction keyword** and all other keywords are shown.
- When an ability requires specific keywords as a condition (e.g. during target selection), keyword highlighting activates:
  - If the unit satisfies **all** required keywords → all matching keyword chips are highlighted.
  - If even one required keyword is missing → no highlighting at all (all-or-nothing).
  - Highlighting is driven by `session_state.highlight_keywords: list[str]`.

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

Center column. Three sections stacked vertically. Highest dynamic of all components.
The `gameProtocoll` panel (Section 8) is rendered **below** this area as a separate component.

```
┌────────────────────────────────────────────────────────────────────────┐
│  gameActionDisplayArea (full width)                                    │
│  Combined view of all effects (including passive auras).               │
│  Modifier chain → final result. Phase rules text + attack summary.     │
│  Setup: unit datasheet when a unit is selected.                        │
│  VP scoring phase: +5 / −5 buttons for both players.                  │
├────────────────────────────────────────────────────────────────────────┤
│  firstPlayerArea (50%)        │  secondPlayerArea (50%)                │
│  ──────────────────────────────────────────────────────────────────────│
│  Main interaction surface     │  Main interaction surface              │
│  for the first player:        │  for the second player:                │
│  active actions + reactions   │  active actions + reactions            │
│  + wound adjustment buttons.  │  + wound adjustment buttons.           │
└────────────────────────────────────────────────────────────────────────┘
```

**Render order:** `gameActionDisplayArea` first (top), then the two-column `PlayerArea` split below.
This puts context (result summary, phase rules, attack form) above the action buttons,
so the player reads the situation before acting.

### Design principles

- **gameActionDisplayArea** is rendered first — it provides context for the player actions below.
  - Passive result view (phase rules, attack summary, modifier chain) in most phases.
  - Active surface only for VP scoring: `[+5]` / `[−5]` buttons for both players appear here
    at the end of the configured scoring phase (see Section 2, VP Scoring Phase).
  - Setup: shows unit datasheet when a unit is selected.
- **PlayerAreas** are the main interaction surface for each player.
  - Active player: action buttons for selected unit (movement, charge, fight, abilities).
  - Inactive player: target info + reaction buttons (overwatch, stratagems, etc.).
  - Wound adjustment buttons appear in the relevant PlayerArea when an effect targets a unit.
  - Both players may have active buttons simultaneously (e.g. active shoots, inactive reacts).
- `uiLayout/gameActionsArea.py` owns the layout. Phase logic is delegated to
  `gameMechanic/<phase>.py` render functions.
- Wound-change buttons are **not** on the unitCard — they live in the PlayerArea.

### Per-phase content

| Phase | displayArea (top) | firstPlayerArea | secondPlayerArea |
|-------|-------------------|-----------------|------------------|
| setup | unit datasheet (when selected) or setup instructions | — | — |
| command | Living Metal results, CP grant | selected unit + ability buttons + heal | reactions / — |
| movement | phase rules | move type buttons + M" value | — |
| psychic | phase rules | PSYKER + power + roll | target + deny |
| shooting | attack summary + attack form | attacker + weapon profiles + wound buttons | target T/Sv/++ + wound buttons |
| charge | phase rules | charge declaration + 2D6 | overwatch reaction |
| fight | fight summary + attack form | melee attacker + weapons + wound buttons | defender + wound buttons |
| morale | phase rules | morale test + result | — |
| (VP phase) | **VP: [+5][−5] for both players** | — | — |

The VP scoring row appears at the end of whichever phase was configured in Setup (e.g. end of Command Phase). It is shown in the displayArea so both players can confirm the score simultaneously.

### Setup — unit datasheet in displayArea

During Setup, clicking a unit name (via the selector button) shows that unit's full datasheet
in the `gameActionDisplayArea`. This lets players review unit profiles before the game starts.

**Datasheet content:** stats table (M · T · Sv · W · ++ · Ld · OC), weapon profiles with
all attributes, keyword list, ability rule texts.

The selector button in unitCard is active in setup phase for this purpose (unlike normal phases
where it drives game actions). Deployment selectbox remains on the unitCard as before.

### Phase transitions

There are no phase sub-stages. The → arrow advances directly to the next phase
via `game_state.next_phase()` (see [processes.md P-03](processes.md)): automatic
start-of-phase effects fire via `timing: phase_start` triggers, per-phase state
is reset in `_reset_phase_state()`, and each phase renders a single view
(`render_active`). Reactive mechanics (e.g. Reanimation Protocols) are handled
inside the phase views themselves.

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

#### GO visibility rules (see also `docs/spec/processes.md P-06`)

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
