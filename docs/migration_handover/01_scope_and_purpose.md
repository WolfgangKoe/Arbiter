# Arbiter — Scope and Purpose

This document is part of a handover set written to support a framework migration.
Arbiter is currently a Streamlit application (Python); it will be rebuilt on a
different, not-yet-chosen technology. Everything below describes *what the
application does*, independent of how Streamlit happens to render it. Where a
behavior exists only because of a Streamlit limitation, that is called out
explicitly so the rebuild does not copy an implementation artifact as if it
were a design requirement.

## What Arbiter is

Arbiter is a **play-companion / referee app** for a physical tabletop game of
**Warhammer 40,000, 9th Edition**. Two players sit at one table with their
physical miniatures, terrain, and dice; Arbiter runs on a single shared screen
(or device) between them and keeps track of everything that is tedious or
error-prone to track by hand: whose turn it is, which phase of the battle
round is active, how much damage each unit has taken, which stratagems and
abilities have already been used, and what the correct dice thresholds are
for the attack currently being resolved.

It is explicitly **not** a digital simulation or a virtual tabletop. The two
core design commitments (from `docs/concept.md`) are:

- **No auto-dice** — the player always rolls physical dice; the app only
  accepts the resulting numbers as input and validates/resolves them.
- **No board state** — the app has no concept of positions, distances,
  line-of-sight, or terrain. Anything that requires measuring the tabletop
  is left to the players and is, at most, surfaced as a textual reminder.

The app's own self-description in its concept doc captures the intent well:
it is a "referee" that enforces phase order, state transitions, and
eligibility rules, while leaving all tactical decisions and all physical
game elements to the players.

## Target users

Two players, both viewing the same screen (`initial_sidebar_state="collapsed"`,
wide layout, two mirrored side columns). There is no remote-multiplayer
concept, no per-player device/login, and no spectator mode. The interface is
entirely in English; all project documentation and stakeholder communication
is in German, but no UI-facing string is expected to be translated as part of
scope.

## Game system and edition

Warhammer 40,000, 9th Edition. Game modes offered at setup:

- **Matched Play** — the fully worked-out mode: game size (Combat Patrol /
  Incursion / Strike Force / Onslaught) drives starting CP and a points
  limit, plus a canned list of GT mission names and a Matched-Play secondary
  objectives structure (3 categories per player, from a fixed list).
- **Open Play** — a stripped-down mode: fixed 3 starting CP, no mission, no
  points-limit check, no secondaries.
- **Crusade** — selectable in the setup screen's game-mode dropdown, but
  choosing it immediately shows an informational message ("full Crusade
  mechanics are planned for Ziel 6") and returns from setup without letting
  the player proceed. It is not implemented; see `src/uiLayout/setupScreen.py`.

## Factions with data

Faction rules and unit data live under `data/wh40k_9e/<faction>/` as YAML,
loaded through `src/gameObjects/loader.py`. Coverage differs sharply by
faction:

| Faction | Data present | Depth |
|---|---|---|
| **Necrons** (`necrons/`) | units, weapons, wargear, relics, warlord traits, stratagems, faction/subfaction abilities, unit abilities, points, army rules, `arkana.yaml` | Full — the primary faction used to build out most mechanics (Reanimation Protocols, Command Protocols, Living Metal, explode-on-destroy, etc.) |
| **Orks** (`orks/`) | same file set as Necrons, plus `powers.yaml` (psychic powers for Weirdboy/Wurrboy) | Full — second faction, used to generalize mechanics away from Necron-only assumptions |
| **Adeptus Custodes** (`adeptus_custodes/`) | only `faction_abilities.yaml`, plus two files literally named `placeholder.relics.yaml` / `placeholder.warlord_traits.yaml` | Stub only — no units, weapons, or stratagems; not a playable faction yet |

A `_shared/` directory holds cross-faction data: `shared_abilities.yaml`,
`shared_powers.yaml`, generic core stratagems (Command Re-roll, Fire
Overwatch, Insane Bravery, Desperate Breakout, Emergency Disembarkation, Cut
Them Down, Counter-offensive), and detachment type definitions. `_schema/`
holds the YAML schema conventions the loader validates against.

Rosters (`data/rosters/*.yaml`) are army lists built against this catalog —
mostly Necron and Ork test/demo lists (e.g. `necrons_1500pts_silent_king.yaml`,
`orks_transport.yaml`). Rosters can also be produced by importing a
BattleScribe `.rosz`/`.ros` export (wargear is not imported from BattleScribe;
only unit selection and model counts are matched against the local catalog).

## What the app manages (in scope)

- **Roster selection and army setup** — pick a YAML roster per player (or
  import one from BattleScribe), configure game mode/size/mission/secondary
  objectives, roll off for attacker/defender and first turn.
- **Battle-round and phase progression** — a fixed phase sequence per round
  (Command → Movement → Psychic → Shooting → Charge → Fight → Morale),
  advancing/reverting via explicit player action, with a hard 5-round game
  length.
- **Command points and victory points** — CP gain/spend bookkeeping, primary
  VP with configurable scoring phase/round, and up to three named secondary
  objectives per player with a manually driven VP tracker.
- **Unit state** — per-unit movement status (stationary/moved/advanced/fell
  back), melee engagement, model losses, deployment (normal/reserve), and
  the turn-scoped flags that gate what a unit may still do this turn/phase.
- **Damage resolution** — a semi-manual attack-sequence calculator: the app
  computes hit/wound/save thresholds and modifiers, the player rolls
  physically and enters counts, the app applies the resulting model/wound
  loss and displays the correct dice math at every step.
- **Abilities, auras, and faction mechanics** — triggered and auto-applying
  abilities (rerolls, invulnerable saves, healing, Necron Reanimation
  Protocols, Necron Command Protocols/directives), scoped by phase, timing,
  and unit conditions declared in YAML.
- **Stratagems** — a single generic "GO card" component that shows a
  stratagem's availability (CP cost, phase/timing/eligibility gates,
  once-per-battle/phase usage), lets a player spend/undo it, and displays its
  rules text.
- **Dice-math display** — a shared HTML-rendered "dice block" widget used
  throughout showing the threshold, applicable modifiers, and reroll/auto
  success-or-fail markers for hit/wound/save rolls.
- **Game log / protocol** — a running log of actions taken (unit selected,
  damage applied, stratagem used, etc.) for the current battle, archived to
  disk on reset so past games can be reviewed or downloaded later.

## What stays on the physical table (explicitly out of scope)

- Rolling dice itself — the app never generates a random result for combat,
  morale, charges, or psychic tests; the player always enters the outcome.
- Any spatial/geometric reasoning: unit positions, movement distances,
  charge-range measurement, line of sight, terrain height, cover
  determination, engagement-range measurement, unit coherency measurement,
  deployment-zone geometry.
- Mission objective-marker control and the VP it would generate — the app
  tracks a VP *number* per player, but does not know where objective markers
  are or which player controls them.
- Automatic win/draw determination — the app never declares "player X wins";
  it only fixes the round count and lets the players read the VP totals it
  is tracking.
- Model/army physical setup and BattleScribe wargear import (only unit
  identity and model count are imported; loadouts must still be checked at
  the table against the printed datasheet).

## Deliberate non-goals

- **Not a full rules reference.** Arbiter does not replace the rulebook; it
  only encodes the subset of rules that are worth automating (deterministic
  math, state machines, bookkeeping). Judgment calls and table-only rules
  are left to the players, sometimes with a textual hint, sometimes with
  nothing at all.
- **Not a virtual tabletop / board simulator.** There is intentionally no
  map, no model tokens, no drag-and-drop positioning.
- **Not (yet) a full army builder.** Roster *creation* from scratch inside
  the app is not a feature; rosters are pre-built YAML files or BattleScribe
  imports. There is no in-app points calculator/list-builder workflow beyond
  reading a roster's precomputed point total against the game-size limit.
- **Not multi-faction-complete.** Only Necrons and Orks are playable in
  practice today; Custodes and any other 9E faction are unimplemented data
  stubs at best.
- **Crusade mode is not implemented** despite being visible as a selectable
  option in the setup screen.

## High-level architecture (for context, not prescriptive for the rebuild)

- `src/gameObjects/` — pure data model (dataclasses for `Unit`, `Weapon`,
  `Ability`, `Stratagem`, `Detachment`, …) plus `loader.py`, the only code
  allowed to read the YAML files. Framework-agnostic.
- `src/gameMechanic/` — game/business logic: phase handlers (one module per
  phase, e.g. `shootingPhase.py`, `fightPhase.py`), the attack-resolution
  math (`combat.py`, `attackMath.py`), the ability/stratagem engines
  (`abilityEngine.py`, `stratagemEngine.py`), unit state mutation
  (`unitMutations.py`), the overall game-state container (`gameState.py`),
  and the append-only game log (`gameLog.py`). This layer holds essentially
  all of the logic that a rebuild needs to preserve. Caveat: the seven
  `*Phase.py` files also contain Streamlit rendering code and are excluded
  from test coverage — see `04_architecture_and_app_flow.md` §1.2 for the
  logic-vs-render split the rebuild must perform; the rest of the layer
  (`combat.py`, `unitMutations.py`, `gameState.py`, the engines) is
  framework-agnostic and fully covered by automated tests.
- `src/uiLayout/` — Streamlit rendering only: layout, HTML/CSS composition
  for dice grids and badges, and wiring of buttons/inputs to the
  `gameMechanic` functions above. This is the layer a framework migration
  replaces wholesale; it is deliberately excluded from automated test
  coverage and is documented behaviorally in
  `docs/migration_handover/02_working_features.md` instead.
- `src/app.py` — the Streamlit entry point: page config, one-time setup
  screen, then a three-column layout (army list / game actions / army list)
  driven by session state.

Game state itself is currently held entirely in Streamlit's `session_state`
(an in-memory, per-browser-session dictionary) — there is no database and no
persistence between sessions other than the on-disk game-log archive and
YAML roster files. A rebuild will need to decide how/where this state lives;
the shape of that state (what fields exist per unit, per player, per phase)
is described alongside the features that use it in
`02_working_features.md`.
