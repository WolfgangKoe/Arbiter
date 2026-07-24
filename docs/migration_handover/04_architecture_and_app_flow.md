# Architecture & App Flow — Migration Handover

> Part of the migration handover set. This document explains **how Arbiter is built today**
> and, critically, **which parts of that construction are permanent domain architecture
> (must survive the rebuild)** versus **which parts are artifacts of Streamlit's execution
> model (must NOT be copied into the new framework)**.
>
> Source docs read to compile this: `docs/spec/architecture.md`,
> `docs/spec/architecture_invariants.md`, `docs/spec/processes.md`,
> `docs/spec/unit_states.md`, `docs/spec/setup.md`, plus the `src/` tree itself.
> Where this document and the specs disagree in nuance, the specs remain canonical for
> day-to-day work — this document's job is to separate signal from Streamlit noise for
> whoever rebuilds the app.

---

## 0. The one-sentence framing

Arbiter is a **rule-tracking companion for a physically-played tabletop game**, not a game
engine. It never rolls dice for the player and never measures distances — it takes
player-entered die results and roster data, and computes/reminds/enforces what 9th-Edition
Warhammer 40k rules say should happen next. That framing matters for the rebuild: the domain
core is a deterministic calculator + state machine over "phase / unit / pending decision",
and the UI is a thin, replaceable shell around it.

---

## 1. Layer model

### 1.1 The three modules and their intended direction

```
gameObjects/   →  gameMechanic/   →  uiLayout/
"what things are"   "what things do"    "how things look"
```

| Module | Responsibility | May import |
|---|---|---|
| `gameObjects/` | Pure Python dataclasses (`Unit`, `Weapon`, `Ability`, `Stratagem`, `Detachment`, `RoundChoiceAbility`) + the YAML loader (`loader.py`). No Streamlit, no session state, no UI concerns. | stdlib only |
| `gameMechanic/` | Phase state machine, the attack-resolution engine, unit-state mutations, ability/stratagem eligibility logic. **Also, in practice, phase rendering** (see 1.2). | `gameObjects/`, (in practice) `uiLayout._common` |
| `uiLayout/` | Streamlit render functions and pure HTML/SVG composition (`diceCompose.py`). | `gameMechanic/`, `gameObjects/` |

`app.py` is the sole composition root: it owns the top-level page layout and is the only
file that should touch `st.session_state` directly at the wiring level (in practice several
`gameMechanic` modules also read/write it directly — see the state-model section).

**Migration takeaway:** the `gameObjects → gameMechanic → uiLayout` layering itself is a
sound target architecture for any framework — domain model, then rules/state engine, then
view. Reproduce this direction. Do **not** reproduce module names or the specific Streamlit
coupling described next; those are implementation detail.

### 1.2 Where the real architecture deviates from the documented ideal — and why it matters for the rebuild

`docs/spec/architecture.md` originally wanted `gameMechanic/` to be Streamlit-free, mirroring
`gameObjects/`. It is not: the seven `*Phase.py` files (`commandPhase.py`, `movementPhase.py`,
`psychicPhase.py`, `shootingPhase.py`, `chargePhase.py`, `fightPhase.py`, `moralePhase.py`)
both hold phase transition/eligibility logic **and** call Streamlit render helpers from
`uiLayout/_common.py`. This is tracked as a documented, deliberate exception in
`docs/spec/architecture_invariants.md` ("NICHT erzwungen"), not silently ignored.

This matters directly for the rebuild: it means the current `gameMechanic/*Phase.py` files are
not a clean "logic module" to port wholesale. Each one bundles two things that must be
split when moving to a new framework:

1. **Phase logic** — what actions a unit is eligible for, what state changes when an action
   resolves, what modifiers apply. This is domain logic and must survive.
2. **Phase rendering** — which buttons/inputs appear, in what layout, calling into
   `uiLayout._common.py`'s shared render helpers (attack-form composer, wound buttons,
   ability cards, GO/Stratagem cards). This is Streamlit-specific view code and should be
   rewritten, not ported, in the new framework's idiom.

When planning the rebuild, budget explicit effort to **separate these two concerns per
phase file** rather than assuming a 1:1 file transplant.

### 1.3 The four (six) architecture invariants — migration requirements, not legacy

`docs/spec/architecture_invariants.md` defines guard tests in `tests/architecture/` that run
inside the normal `pytest` suite. These encode requirements that should be re-established
in the new stack, independent of framework choice:

| ID | Invariant | Why it matters beyond Streamlit |
|---|---|---|
| INV-1 | `gameObjects/` imports no UI framework — pure data layer. | Guarantees the domain model is portable/testable without spinning up any UI runtime — directly enables porting it unchanged into a new framework. |
| INV-2 | YAML game data is read **only** through `gameObjects/loader.py` (two documented exceptions: the loader itself and `roszImporter.py`'s roster-conversion writer). | A single data-access seam means the rebuild can swap the storage/query mechanism (e.g. move from YAML-on-disk to a database) by rewriting one module, not hunting scattered file reads. |
| INV-3 | `gameObjects/` does not depend on `gameMechanic/` or `uiLayout/`. | Enforces the layering direction in 1.1 — the domain model never reaches "up" into rules or view code. |
| INV-4 / INV-4b | `src/` contains no faction-specific names or vocabulary (Necron/Ork/Custodes strings) — every faction decision is data-driven from YAML. | This is a core product requirement, not a Streamlit artifact: the app must support adding a new 40k faction by adding YAML, never by touching code. The rebuild must preserve this generic-engine property or the multi-faction extensibility is lost. |
| INV-5 | Documentation/spec/test/acceptance-catalog cross-references stay in sync (own guard tests in `tests/docs/`, `tests/acceptance/`). | Not code architecture per se, but a process invariant worth keeping: rule coverage claims are machine-checked against actual tests, not just asserted in prose. |
| INV-6 | Pure HTML/SVG composition for the attack UI lives in `diceCompose.py` — Streamlit-free and coverage-measured; only thin `st.markdown()` wrappers remain in the excluded `diceHtml.py`. | This is the template for how to keep *any* future render layer's composition logic testable: separate "build the markup/structure" (pure function, testable) from "hand it to the UI framework" (thin, excluded from coverage). Reproduce this seam pattern regardless of which framework replaces Streamlit. |

INV-4/INV-4b in particular are the most consequential for the rebuild: they are what make
Arbiter a generic 9th-Edition engine rather than a Necron-only or Ork-only tool. Any rewrite
that reintroduces `if faction == "necrons"` branches in engine code would be a regression
against a hard-won property (see the Necron/Ork/Custodes vocabulary-leak cleanup history in
`architecture_invariants.md`'s debt ledger).

---

## 2. State model

### 2.1 What constitutes "the game state" (semantics — this must survive)

Conceptually, the full game state at any moment is:

- **Meta**: game size/type/mission, current battle round, current phase, which player is
  active, whether setup is complete, whether the battle has ended.
- **Score**: CP and VP per player.
- **Armies**: per player — faction, subfaction, battle-forged flag, roster-derived unit list,
  detachments, faction/subfaction properties.
- **Per-unit runtime state**: current wounds (or, for units with model groups, per-group wound
  pools), model count, destroyed flag, in-melee flag + which enemy units it's engaged with,
  in-reserve flag, this-turn action flags (advanced/retreated/charged/shot/fought/…),
  per-battle bookkeeping (models lost this turn, active buffs, used abilities/stratagems).
  See `docs/spec/unit_states.md` for the full badge vocabulary and every legal/illegal
  transition — that document is a **behavioral spec**, effectively a state-machine contract,
  independent of Streamlit.
- **Selections**: which unit is selected, which unit(s) are targeted, any pending
  multi-step interaction (a pending ability/target request, a pending explode-tile resolution,
  a pending Heroic Intervention, etc.).
- **Log**: an append-only, per-round/per-phase action log with an immutability rule (entries
  for completed turns cannot be edited) — `gameMechanic/gameLog.py`.

This is the part of "state" that is pure domain semantics and must be preserved by any
rebuild, regardless of what technology stores it (a database, a client-side store, a
different in-memory session object, etc.).

### 2.2 Where it lives today — Streamlit-specific, must NOT be copied verbatim

All of the above lives in `st.session_state`, a single flat, dynamically-typed dict-like
object that Streamlit preserves across script reruns for one browser session
(`gameMechanic/gameState.py` documents the full schema in `docs/spec/architecture.md`'s
"session_state Schema" section). Concretely:

- There is no formal schema/type at runtime — `gameState.py` establishes keys by convention
  (`init_state()` sets ~40 top-level keys) and other modules read/write them via helper
  functions (`units_key_for`, `faction_dir_for`, etc.) or directly.
- State is **per-browser-session**, not persisted anywhere durable except the append-only
  JSON game log (`data/log/game_log.json` + its archive) — closing the browser tab or
  restarting the server loses all in-progress game state except that log.
  `gameMechanic/scenarios.py` exists specifically to let developers/testers load a
  pre-built state snapshot via a `?scenario=` query param, which is itself evidence that
  there is no first-class save/restore of `st.session_state`.
- Many `gameMechanic/*Phase.py` and `gameObjects/loader.py`/`gameState.py` functions read
  `st.session_state` directly rather than receiving state as a parameter — despite
  `architecture.md`'s stated intent ("components receive all data as arguments"). This
  direct global-mutable-state access pattern is idiomatic Streamlit but is exactly the kind
  of implicit dependency a rebuild should replace with an explicit state object/store passed
  through function signatures (or a proper backend session/store, depending on chosen
  architecture — client-heavy SPA vs. server-authoritative).

**Migration takeaway:** treat `docs/spec/architecture.md`'s "session_state Schema" and
`docs/spec/unit_states.md`'s badge/transition tables as the state **shape and semantics**
specification (port these), and treat "it's a flat dict called `st.session_state`, read from
anywhere" as pure Streamlit plumbing (do not port this — replace with an explicit,
typed/validated state store with a defined access API).

### 2.3 Lifecycle: setup → game → end

1. **Setup** (`uiLayout/setupScreen.py`, spec: `docs/spec/setup.md`): choose game mode
   (Matched/Open/Crusade), game size (determines starting CP and points limit via
   `gameState.CP_BY_GAME_SIZE` / `PTS_LIMIT_BY_GAME_SIZE`), pick each player's roster from
   `data/rosters/`, resolve attacker/defender and first player, optionally configure secondary
   objectives. Ends by calling `gameState.init_state()`, which sets `st.session_state.initialized
   = True` and populates the full schema from the loaded rosters. `app.py` gates on this flag:
   while absent, only the setup screen renders (`st.stop()` short-circuits the rest of the
   script — a Streamlit-specific control-flow trick, see §3.1).
2. **Game** — a loop of battle rounds (max 5, `gameState.MAX_BATTLE_ROUNDS`), each round a loop
   of 7 phases (`gameState.PHASES`, excluding the synthetic "Setup" entry): Command → Movement
   → Psychic → Shooting → Charge → Fight → Morale, played once per active player. See §3.3 for
   the phase engine.
3. **End** — reaching the Morale phase of round 5 for the second player sets `battle_over =
   True` instead of starting round 6 (`gameState.next_phase`, rule source:
   `docs/work/wahapedia_core_rules/core_rules.txt:2337`). The header then shows a win/draw
   result instead of the "→ Next phase" control. This end state is explicitly **not a dead
   end** — `gameState.prev_phase()` can step back and clears `battle_over`, so a
   too-early click is correctable. "Army destroyed" as an alternate end condition is
   acknowledged as out of scope (backlog item), not implemented.
4. **Reset** (`gameState.reset_game()`) — archives the current game log and wipes every
   `st.session_state` key, returning to setup.

---

## 3. App flow

### 3.1 Startup and the rerun model — the mechanic that most needs replacing

`src/app.py` is the entry point (`streamlit run src/app.py`). Every single user interaction
(button click, number input change, selectbox change) causes Streamlit to **re-execute the
entire `app.py` script top to bottom** — there is no persistent server process holding
application state in memory across interactions in the traditional sense; `st.session_state`
is the one piece of memory that survives the rerun, everything else (local variables, which
branch of an `if` executed) is recomputed from scratch each time.

Concretely, on each run: `app.py` sets page config, injects a CSS theme, checks
`"initialized" not in st.session_state` to decide setup-screen vs. game-screen, loads a
`?scenario=` query param exactly once, conditionally renders a "scroll to top" JS snippet,
then renders the header, a three-column layout (`left` = first player's army list, `center`
= the phase's action area + protocol log, `right` = second player's army list).

**This full-script-rerun model is the single biggest thing that must NOT be carried over.**
Every render function in `uiLayout/` and every phase handler in `gameMechanic/*Phase.py` is
written under the assumption "this whole function reruns from the top on every click,"
which shapes patterns like:
- Heavy reliance on `st.session_state` as the only cross-run memory.
- Frequent explicit `st.rerun()` calls to force a fresh pass after a state mutation
  (see §3.2 for why this is now actively being phased out in favor of callbacks).
- `st.stop()` used as an early-exit/short-circuit for "don't render the rest of this script
  this run" (`app.py`'s setup-screen gate).

A rebuild on any framework with persistent component state (React/Vue SPA + backend API,
a different Python framework with explicit render trees, etc.) should model interactions as
discrete events dispatched to state-mutation functions, not as "the whole page recomputes."
The *mutation functions themselves* (`gameMechanic/unitMutations.py`,
`gameMechanic/gameState.py`'s phase transitions) are exactly what should be preserved —
they are pure(-ish) state-transition logic once decoupled from `st.session_state` as their
data source.

### 3.2 How a user action travels — and the callback-timing lesson (B-134)

The generic path for any in-game action:

```
Widget event (button click / number_input change)
        │
        ▼
Streamlit re-executes app.py from the top OR (preferred, see below) fires an on_click/
on_change callback BEFORE the rerun's script body executes
        │
        ▼
Callback / inline handler calls a gameMechanic mutation function
  (apply_damage, heal_unit, set_movement_status, next_phase, ...)
        │
        ▼
Mutation function reads/writes st.session_state directly
        │
        ▼
Script body (re-)renders uiLayout components from the now-current st.session_state
```

Two mechanically different sub-patterns exist in the codebase today, and the difference is
instructive for the rebuild:

- **Older pattern** (inline mutation + explicit `st.rerun()`): a button's `if st.button(...):`
  branch calls the mutation function directly, then calls `st.rerun()` to force a fresh pass.
  This works, but there is a window where two on-screen renderings of the *same* underlying
  unit (e.g. its card in the owner's sidebar and a reference to it elsewhere in the action
  area) can disagree for one frame, because the rerun restarts the whole script rather than
  patching just the affected views.
- **Current pattern, fixed 2026-07-24 (commit `4a562ef`, backlog item B-134 "stale
  UnitCard")**: the mutation is moved into a dedicated function passed as the widget's
  `on_click=`/`on_change=` callback. Streamlit guarantees callbacks run *before* the script
  body re-executes for that run, so by the time rendering happens, every view of the mutated
  unit is already consistent — and the explicit `st.rerun()` becomes unnecessary because the
  natural rerun-on-interaction already picks up the fresh state. Example:
  `src/uiLayout/_common.py:_wound_adjustment_click` (registered via
  `wound_adjustment_buttons`'s `on_click=_wound_adjustment_click, args=(faction, uid, unit,
  delta)`), and the analogous `_explode_toggle_click` / `_explode_direct_apply_change` for the
  explode-damage multi-unit panel.

**Why this belongs in the handover:** it is a concrete, recent, real bug (not hypothetical)
caused entirely by *when* Streamlit executes code relative to a rerender — a category of bug
that is specific to Streamlit's execution model and has no equivalent in a framework with
synchronous, explicit state updates (e.g. a reducer/store pattern, or server-rendered
request/response with no partial-view staleness). The rebuild should not need an
"on_click timing" concept at all if state mutation and view rendering are properly
sequenced by construction — but it is worth knowing this class of bug existed, so equivalent
sequencing guarantees are deliberately designed in, not assumed.

### 3.3 The phase sequence per battle round

`gameMechanic/phaseRunner.py` holds `PHASE_REGISTRY: dict[str, PhaseHandler]`, populated once
at import time with one handler instance per phase
(`CommandPhaseHandler`, `MovementPhaseHandler`, `PsychicPhaseHandler`, `ShootingPhaseHandler`,
`ChargePhaseHandler`, `FightPhaseHandler`, `MoralePhaseHandler` — each implementing the
`PhaseHandler` Protocol from `gameMechanic/phaseHandler.py`, a single method
`render_active(state)`). `render_current_phase(state)` looks up `PHASES[state["phase_idx"]]`
and dispatches. There is deliberately no `start`/`active`/`end` stage concept per phase — each
phase has exactly one view.

Phase transitions run exclusively through `gameMechanic/gameState.py:next_phase()` (bound to
the header's "→" button) and its inverse `prev_phase()`. `next_phase()`:
- Always resets `selected_unit`, `selected_targets`, and psychic-phase scratch state.
- Calls `_reset_phase_state()` on every transition (clears phase-scoped bookkeeping like
  per-phase stratagem usage, pending reactive-stratagem windows, the explode-tile group).
- Only on a **player switch** (after the second player's Morale phase — i.e. once per full
  battle round) calls `_reset_turn_state()`, which clears the ephemeral turn flags
  (`advanced`/`retreated`/`charged`/`shot`/`fought`/…) for every unit on both sides, and
  `_reset_round_choice_state()` when a genuinely new round begins (both players have acted).

The concrete rules content of each phase (eligibility, e.g. "advanced units cannot shoot
except with Assault weapons") lives in the corresponding `*Phase.py` file and is documented
process-by-process in `docs/spec/processes.md` (P-05 Command, P-10 Movement, P-12 Psychic,
P-07 Shooting, P-13 Charge, P-14 Fight, P-15 Morale) — those Mermaid diagrams are a good
direct source for re-implementing phase logic in a new framework, since they describe
*decisions and state changes*, not rendering.

**Migration takeaway:** `PHASE_REGISTRY` + a `PhaseHandler` protocol with one
`render`-equivalent method is a reasonable pattern to keep (phase-keyed dispatch table), but
"phase eligibility/mutation logic" and "phase rendering" should be two separate methods/objects
in the rebuild, not bundled in one `render_active()` as they are today (see §1.2).

---

## 4. Key domain mechanics — location map

One line each; the code remains available for detail, this is a navigation aid.

| Mechanic | What it is | Where it lives |
|---|---|---|
| Attack sequence (core) | The 9E hit → wound → save → damage resolution, given player-entered roll counts; AP modifies the roll not the threshold; unmodified 1/6 always fail/succeed; net roll modifier capped ±1. | `src/gameMechanic/combat.py:resolve_attack_sequence` / `resolve_attack`, `wound_threshold`, `resolve_attack_modifiers`, `resolve_save` |
| Strength/toughness parsing | Weapon strength as `"User"`/`"+N"`/`"×N"`/fixed-int notation resolved against the bearer's stat — never a bare `int()` cast. | `src/gameMechanic/combat.py:resolve_weapon_strength`, `src/gameMechanic/attackMath.py:_parse_strength` |
| Damage/wound application | HP reduction, model-count derivation, destruction, per-model-group wound pools (mixed-wound units), forced/locked damage allocation, melee auto-clear on destruction. | `src/gameMechanic/unitMutations.py:apply_damage`, `heal_unit`, `_apply_group_wound_damage`, `get_locked_group` |
| Turn/badge state machine | Legal movement/action badges per unit (STATIONARY/MOVED/ADVANCED/RETREATED/CHARGED/…), transition constraints, reset timing. | Semantics: `docs/spec/unit_states.md`; code: `src/gameMechanic/unitMutations.py:set_movement_status`, `src/gameMechanic/movementPhase.py:_active_movement`, badge rendering (excluded from coverage) `src/uiLayout/_common.py:state_badges_html` |
| Phase transitions / round structure | Phase index advance, player switch, round increment, battle-end detection, turn-flag/round-choice resets. | `src/gameMechanic/gameState.py:next_phase`, `prev_phase`, `_reset_turn_state`, `_reset_round_choice_state` |
| Auras / passive & triggered abilities | Trigger/condition matching, effect execution (heal, buff, invuln grant, wound-auto-fail floors, reroll grants), aura-donor lookups (e.g. "aura still active only if the donor unit is alive"). | `src/gameMechanic/abilityEngine.py` (check_trigger, check_conditions, execute_effect, get_triggered_abilities, unit_hit_reroll_ones/unit_wound_reroll_ones, buff_stat_bonus, ability_invuln_save) |
| Command-phase round-choice abilities (e.g. Necron Command Protocols) | Once-per-battle-round faction-wide directive selection, primary/secondary/extra effects. | `src/gameObjects/roundChoiceAbility.py` (data), `src/gameMechanic/abilityEngine.py:_active_directive_effects`/`get_active_round_choice_modifier`, `src/gameMechanic/commandPhase.py` |
| Stratagems (Gefechtsoptionen/GO) | CP-cost eligibility/visibility (clickable/greyed/hidden), phase/player/keyword/weapon-shape gating, once-per-phase/battle tracking, reactive (event-triggered) stratagems, variable CP cost by keyword. | Data model: `src/gameObjects/stratagem.py`; effect application: `src/gameMechanic/stratagemEngine.py`; visibility spec: `docs/spec/processes.md` P-06 |
| Rerolls | Hit/wound reroll-of-1s from unit/aura abilities, surfaced as reroll slots in the modifier stack (checked against the unmodified die per 9E rules). | `src/gameMechanic/abilityEngine.py:unit_hit_reroll_ones`/`unit_wound_reroll_ones`, consumed by `src/gameMechanic/combat.py:resolve_attack_modifiers`'s `reroll_slots` |
| Explodes / mandatory destruction triggers | Model destruction → mandatory (non-optional) explosion check → area mortal-wound assignment to units in range; distinguished from the `auto_explode`/`pre_explode_stratagem` GOs that are genuine CP-spend decisions. | Rule mapping: `docs/spec/processes.md` P-16; data: `Ability.mandatory` field, `Effect.type == "explode"` (`src/gameObjects/ability.py`); engine: `src/gameMechanic/abilityEngine.py:resolve_explode_effect` |
| Dice-result display / "dice hints" | Pure HTML/SVG composition of threshold headers, dice-face glyphs, modifier rows, reroll/auto-fail marker rows — a visual reminder of what to roll/interpret, never an actual RNG die for the player. | `src/uiLayout/diceCompose.py` (Streamlit-free, INV-6, coverage-measured); thin `st.markdown()` wrappers in the excluded `src/uiLayout/diceHtml.py` |
| Dice-notation parsing (D3/D6/2D6+N) | Used only for effect-size resolution where the app itself needs a concrete number (e.g. an ability's own damage roll count), not for resolving player-facing attack rolls (the app never rolls "for" the player's own attacks). | `src/gameMechanic/combat.py:parse_dice` |
| YAML data loading | Single entry point for all faction/unit/weapon/ability/stratagem/roster data; resolves weapon-ID references, wargear options, model-group specs, relic application. | `src/gameObjects/loader.py` (`load_unit_catalog`, `load_army`, `load_stratagems`, `load_roster`, `get_abilities_for_unit`, etc.) |
| Roster import (BattleScribe `.rosz`) | External file → internal roster YAML converter; the one legitimate faction-label-mapping exception to the generic-`src/` invariant (I/O normalization at the import boundary). | `src/gameObjects/roszImporter.py` |
| Action log | Append-only per-round/per-phase event log with an immutability rule for completed turns; archived on game reset. | `src/gameMechanic/gameLog.py` |

---

## 5. Quality gates & testing strategy

### 5.1 Today's gates (measured by `pytest --tb=short`)

- **Coverage gate: 99%** (`pyproject.toml [tool.coverage.report] fail_under = 99`), measured
  over everything in `src/` **except** an explicit `omit` list: `src/app.py`,
  `src/constants/*`, every `uiLayout/*.py` render module (`_common.py`, `armyCard.py`,
  `armyList.py`, `detachmentCard.py`, `diceHtml.py`, `gameActionsArea.py`, `gameHeader.py`,
  `gameProtocoll.py`, `setupScreen.py`, `unitCard.py`), and the seven `gameMechanic/*Phase.py`
  render-bundling files (`commandPhase.py`, `chargePhase.py`, `fightPhase.py`,
  `moralePhase.py`, `movementPhase.py`, `psychicPhase.py`, `shootingPhase.py`).
- **Why render code is excluded**: Streamlit render functions are technically testable, but
  testing them means mocking widget interaction order (which button/input appears in which
  sequence), and that mock breaks on essentially every UI layout change — high maintenance
  cost, low bug-catching value, per CLAUDE.md's Testing section. The actual business logic
  those render functions call into (state mutations, computations) already lives in
  directly-tested modules (`combat.py`, `unitMutations.py`, `gameState.py`,
  `abilityEngine.py`, `stratagemEngine.py`) and is covered there. Render output is instead
  **manually verified** whenever UI changes, with the specific verification steps named
  explicitly (never assumed "done" without it).
- **The one deliberate exception to "render is untested"**: `src/uiLayout/diceCompose.py`
  (INV-6) — pure HTML/SVG composition, no Streamlit import, fully unit-tested and **not** in
  the coverage `omit` list. This is the template pattern: whenever meaningful *composition
  logic* (not framework glue) hides inside a render function, it gets pulled out into a
  Streamlit-free, directly-tested module. `test_render_composition_seam.py` guards both halves
  of this rule (no Streamlit import in `diceCompose.py`; the omit list must not accidentally
  swallow it via a wildcard).
- **Architecture guard tests** (`tests/architecture/`) — enforce INV-1 through INV-6 above,
  run inside the normal `pytest` pass; a broken guard breaks the build exactly like a failing
  unit test. Fast standalone measurement: `pytest tests/architecture/ tests/docs/
  tests/acceptance/ --no-cov -q`.
- **Acceptance/rule-coverage catalog** (`docs/spec/acceptance/rules.md`) — the *denominator*
  against which "how much of the 9E rulebook does this app actually implement/test" is
  measured, independent of code coverage percentages. Each rule is one `R-<AREA>-<NN>` entry
  classified as:
  - **Class A** — the app computes/enforces the rule; acceptance requires code + a test.
  - **Class B** — only checkable at the physical table (distances, line of sight, unit
    coherency); acceptance requires the app to show a reminder + a test that the reminder
    appears.
  - **Class C** — hybrid: an app-enforceable part plus a table-only part (e.g. "locked in
    combat" — the app enforces the `in_melee` flag, but not the underlying distance).
  Each entry records `status` (implemented/open), `getestet` (tested: yes—with test name, or
  no), and `code: file:function`. `status: implementiert` + `getestet: nein` is tracked as
  debt (ratchet: only allowed to shrink). `tests/acceptance/` cross-checks that every
  acceptance ID maps to exactly one test and vice versa (part of INV-5).
- **Architecture-invariant debt ledgers** (INV-4/INV-4b in
  `architecture_invariants.md`) — a live, shrinking-only count of faction-specific
  leaks into `src/`, tracked per session rather than allowed to silently grow.

### 5.2 What the rebuild should keep, and what's negotiable

- **Keep**: the *concept* of a rule-coverage ledger separate from code coverage — this is
  the actual fachlich (domain) safety net, and it is framework-agnostic. Whatever the new
  stack is, `docs/spec/acceptance/rules.md`'s A/B/C classification and per-rule
  code-pointer/test-pointer discipline should carry over largely unchanged; it is a
  rules-engine testing strategy, not a Streamlit one.
- **Keep**: the domain test suite itself (`tests/gameMechanic/`, `tests/gameObjects/`, 28 +
  8 test files respectively) as the primary regression net for the ported logic — these
  tests exercise `combat.py`, `unitMutations.py`, `gameState.py`, `abilityEngine.py`,
  `stratagemEngine.py`, `loader.py` etc. directly, with no Streamlit runtime involved, and
  should port with only import-path changes if the domain modules themselves are carried
  over largely as-is (once decoupled from `st.session_state`, see §2.2).
  `tests/uiLayout/` (16 files) tests the Streamlit-free composition seam
  (`diceCompose.py`) and HTML-output assertions for the excluded render modules where
  feasible — these will need to be rewritten against whatever the new render layer is.
- **Revisit**: the **render-exclusion tradeoff itself** was a Streamlit-driven decision
  (full-script rerun makes render-order mocking brittle). A framework with component-level
  state and more surgical re-render (e.g. a React tree, or a Python framework with explicit
  component props) may make render-layer testing cheap enough that the 99%-with-omit-list
  approach should become 99%-with-a-much-shorter-list, or drop the omit list entirely. This
  is worth an explicit decision early in the rebuild rather than defaulting to "carry the
  same omit list forward."
- **Revisit**: the mypy ratchet (`tools/mypy_gate.py`, frozen error-count baseline) is a
  reasonable pattern for any statically-typed rebuild target, but is Python/mypy-specific
  tooling — re-derive the equivalent gate for whatever type system the new stack uses
  (TypeScript `strict`, etc.) rather than assuming the tool itself ports.

