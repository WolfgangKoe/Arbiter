# Arbiter — Working Features (as of 2026-07-24, branch `dev`)

This is an inventory of what is **actually implemented and working** in the
current codebase, grouped by area. Every feature entry names the
user-visible behavior and the code that implements it. Rule classes follow
`docs/spec/acceptance/rules.md`: **A** = the app computes/enforces the rule,
**B** = the rule is table-only and the app at most shows a hint, **C** =
hybrid (part app, part table). Rule IDs (e.g. `R-COMBAT-07`) refer to entries
in that acceptance catalog and are given so the rebuild team can look up the
exact Given/When/Then and existing test names.

The final section lists what is **not** implemented — read it before
assuming a gap in this document is an oversight.

---

## 1. Setup and roster selection

All of this runs before `st.session_state.initialized` is set — a single
one-shot screen, `src/uiLayout/setupScreen.py:render_setup_screen`.

| Feature | Behavior | Code |
|---|---|---|
| Game mode selection | Choose Matched Play / Open Play / Crusade. Crusade shows an info message and stops (not implemented). | `setupScreen.py:render_setup_screen` |
| Game size (Matched only) | Combat Patrol / Incursion / Strike Force / Onslaught selects starting CP and a points limit. | `gameState.py: CP_BY_GAME_SIZE`, `PTS_LIMIT_BY_GAME_SIZE` |
| Open Play fixed CP | Open Play always starts both players at 3 CP, no points check, no mission. | `setupScreen.py:render_setup_screen` |
| BattleScribe import | Upload a `.rosz`/`.ros` file; the app parses it, matches unit names/counts against the local catalog, and writes a new roster YAML. Unmatched units are reported; wargear is not imported. | `gameObjects/roszImporter.py: parse_rosz_bytes / parse_ros_bytes / import_roster` |
| Roster selection | Pick one YAML roster per player from `data/rosters/`; the two rosters must differ (Start Game is disabled otherwise). | `setupScreen.py:render_setup_screen`, `gameState.py:list_available_rosters` |
| Points-limit check | Computes each roster's total points and warns if either exceeds the selected game size's limit. | `gameState.py:compute_roster_total_pts` |
| Mission selection (Matched only) | Pick one of a fixed GT-mission-pack list per game size (informational only — the app does not encode the mission's actual rules). | `setupScreen.py: _MISSIONS_BY_SIZE` |
| VP scoring configuration | Choose which phase (e.g. "Morale") and from which round primary VP scoring becomes visible during the game. | `setupScreen.py:render_setup_screen`, consumed by `gameActionsArea.py:_render_vp_scoring` |
| Attacker/Defender roll-off | A "Roll Off" button randomly assigns Attacker/Defender labels (cosmetic; does not by itself set first turn). | `setupScreen.py:render_setup_screen` |
| Secondary objectives (Matched only, optional) | Toggle on; each player picks 3 category+objective pairs (no repeated category) from a fixed list, each starting at 0/15 VP. | `setupScreen.py:_render_secondary_picker` |
| Battle log archive browser | Expander listing previously archived games (from prior resets) with per-entry download (raw JSON) and delete (with confirm step). | `setupScreen.py:_render_archive_section`, `gameLog.py:list_archived_logs` |
| Start Game | Initializes full game state (`gameState.py:init_state`) from the choices above and proceeds to the in-game screen. | `setupScreen.py:render_setup_screen` → `gameState.py:init_state` |

Once the game starts, an additional **in-game setup phase** (`phase_idx == 0`,
distinct from the pre-game screen above) shows the unit datasheet viewer, a
first-player roll-off (re-selectable), and — for factions with Command
Protocols/directives — a pre-battle protocol/directive assignment UI, before
a "Start Game" button advances to the Command phase. Code:
`src/uiLayout/gameActionsArea.py:_render_setup`.

## 2. Game header and round tracking

Rendered once per page load above the three-column layout
(`gameHeader.py:render_game_header`).

| Feature | Behavior | Code |
|---|---|---|
| Phase indicator | Shows the current battle round number and a row of phase badges (Command/Movement/Psychic/Shooting/Charge/Fight/Morale) with the active one highlighted. | `gameHeader.py:_phase_badges_html` |
| Phase navigation | A "→" control advances to the next phase; a "←" control reverts to the previous one. Phase jumps are never hard-blocked — the app trusts the player's own judgment about legality of undoing/redoing a phase. | `gameHeader.py:render_game_header` → `gameState.py:next_phase / prev_phase` |
| Turn/round transition | Advancing past the second player's Morale phase switches active player, resets per-turn unit flags (`moved`, `advanced`, `shot`, `charged`, `fought`, etc.) via `_reset_turn_state`, and increments the round. | `gameState.py:next_phase`, `_reset_turn_state` |
| Fixed 5-round game length (R-ROUND-*, class A) | The transition that would start round 6 instead sets `battle_over = True` and freezes the state at round 5/Morale; going back with "←" un-sets it (not a dead end). | `gameState.py: MAX_BATTLE_ROUNDS`, `next_phase`, `is_battle_over` |
| End-of-battle result | Once `battle_over`, the header replaces the phase arrow with a result banner: winner = higher VP, tie = Draw. Purely a VP-number comparison — no mission/army-destruction win conditions (R-SCORE-11/12, class B, open). | `gameHeader.py:battle_result_html` |
| CP/VP display | Per-player CP and VP shown as Streamlit metrics in the header. | `gameHeader.py:_score_group` |
| Reset game | A reset control archives the current game log to disk and clears session state back to the setup screen. | `gameState.py:reset_game`, `gameLog.py:archive_and_reset_log` |

## 3. Army list, unit cards, and unit state

Each player's side column renders their `armyList.py:render_army_list` →
one army/faction card (`armyCard.py:render_army_card`) plus one detachment
card per unit group (`detachmentCard.py:render_detachment_card`), which in
turn renders one `unitCard.py:render_unit_card` per unit.

| Feature | Behavior | Code |
|---|---|---|
| Unit selection | Clicking a unit's name button toggles it as `selected_unit` (own side) or `selected_target` (enemy side, only in phases where targeting makes sense: shooting/charge/fight/psychic). Selecting a new unit always clears any previous target. | `unitCard.py:render_unit_card`, `gameState.TargetSelectionRequest` |
| Wounds/model bars | A visual bar shows remaining wounds/models for the unit at the top of its card. | `unitCard.py:render_unit_card` |
| State badges | Colored badges reflect current unit state: MOVED, ADVANCED, STATIONARY, RETREATED, IN MELEE, CHARGED, FOUGHT, SHOT, CAST, RESERVE, DESTROYED, HEROIC INT. | `unitCard.py: _BADGE_COLORS`, `_state_badges_html` |
| Keyword chips | Unit keywords are shown as chips; the unit's own faction keyword is folded out (shown once on the army card instead). An optional "highlight" mode lights up chips that match a keyword set of interest. | `unitCard.py:_keywords_html / _keyword_chip / _fold_faction_keyword` |
| Deployment control (setup only) | Inline selectbox per unit: Normal / Stationary / Reserve. | `unitCard.py:render_unit_card` → `unitMutations.py:set_deployment` |
| Model-group sub-cards | Units with multiple internal model profiles (e.g. mixed-weapon squads) get per-group sub-cards inside the active player's action area, used to target/apply damage to a specific group. | `_common.py:render_group_cards`, `unitMutations.py:_apply_group_wound_damage` |
| Army/faction card | Shows the faction's display name, subfaction badge (dynasty/clan — "missing"/"error" states are shown, never silently hidden), army-wide triggered abilities relevant to the current phase, and (for factions that have them) the Command-Protocol/round-choice directive picker and once-per-battle abilities. | `armyCard.py:render_army_card`, `gameState.py:subfaction_badge_for / faction_display_name_for` |
| Datasheet viewer | Selecting a unit during the setup phase shows its full stat line (M/T/Sv/W/Ld/OC, weapons) in the central display area. | `gameActionsArea.py:_display_unit_datasheet` |

## 4. Phase-by-phase flow

Each phase has exactly one view (no start/active/end sub-stages); dispatch
goes through `phaseRunner.py:render_current_phase`, which looks up the phase
key in a registry and calls that phase module's `render_active`.

**Command Phase** (`commandPhase.py`)
- CP gain: +1 automatically for a Battle-forged army at the start of the
  phase (R-CMD-09, class A: `commandPhase.py:resolve_command_start`); an
  additional "roll for CP" mechanic exists for missions/abilities that grant
  it (`resolve_gain_cp_roll`, R-CMD-11).
- Necron Command Protocols: one of five protocols may be picked once per
  game per protocol; both directives it grants (primary/secondary) then
  apply. Round 1 auto-activates "Eternal Guardian" without a manual pick.
  Mechanical directive effects are only partially wired: Eternal Guardian
  Directive 1 (auto Light Cover if stationary, R-PROTO-01) and Conquering
  Tyrant Directive 2 (shoot-after-fall-back, −1 to hit, R-PROTO-03) are both
  class A and implemented; Conquering Tyrant Directive 1 (+3" aura range) is
  class B and currently shows no app hint at all (R-PROTO-02, open).
- Living Metal healing (Necron-specific YAML ability) auto-applies at
  command-phase start, capped so a unit is never healed past its starting
  model/wound count. Code: `commandPhase.py:_render_faction_actions`.

**Movement Phase** (`movementPhase.py`)
- Per unit: Move / Advance / Stationary / Retreat buttons, gated by current
  state (already-retreated units are locked out of further movement;
  in-melee units may only go Stationary or Retreat, never Move/Advance).
  Advancing marks the unit ineligible to Charge and (outside
  Assault-weapon exceptions elsewhere in the attack sequence) to shoot.
- Reserves: units deployed to reserve get a "Deploy from Reserve" button,
  disabled in round 1 and enabled from round 2 onward; deploying counts the
  unit as having moved (may still shoot/charge as appropriate).
- Code: `movementPhase.py:_active_movement / _render_reinforcements_step`,
  `unitMutations.py:set_movement_status`.

**Psychic Phase** (`psychicPhase.py`) — Smite only, no other powers
- Requires a PSYKER unit to be selected; shows a Smite (Warp Charge 5)
  action with a 2D6 roll-input field.
- Perils of the Warp on a roll of 2 or 12: prompts a D3 mortal-wound input
  applied to the caster itself.
- Manifest succeeds at roll ≥ 5; the opposing player, if they have a
  deny-capable unit (PSYKER keyword or a unit-level `deny_psychic` ability,
  e.g. Canoptek Spyder's Gloom Prism, Silent King's Noctilith Beacons), gets
  a Deny the Witch 2D6 roll that must exceed the manifest roll to block it.
  Deny eligibility beyond the crude "within 24 inches" table-check
  (R-PSYCHIC-13) is not distance-verified by the app.
- On a successful, undenied manifest, damage is D3 mortal wounds (D6 if the
  original roll was ≥ 11) applied to a target the player selects from the
  opposing army list.
- Code: `psychicPhase.py:has_psyker / cast_eligibility / is_manifested /
  is_perils / can_deny / deny_succeeds / smite_damage_die`.

**Shooting Phase** (`shootingPhase.py`)
- Select an attacking unit (blocked with a warning if it advanced, retreated,
  or is in melee without a ranged-from-melee allowance); its weapon profiles
  are shown.
- Select a target unit from the opposing army list; its T/Sv/invuln are
  shown alongside a combined attack-math summary.
- The player rolls physically and enters hit/wound/save counts; `apply_damage`
  removes wounds/models accordingly.
- If the defending unit is a Necron unit that lost models, a Reanimation
  Protocol prompt appears for the defending player (see §6).
- Code: `shootingPhase.py:can_shoot`, `combat.py:resolve_attack`,
  `unitMutations.py:apply_damage`.

**Charge Phase** (`chargePhase.py`)
- Select a charging unit (blocked if it advanced, retreated, or is already in
  melee); select one or more enemy targets; the app shows a reminder that
  the charge roll is 2D6 and must reach the target(s) — it does not verify
  distance. The player then reports Charge Successful/Failed; success marks
  the unit charged and puts both sides `in_melee`.
- Fire Overwatch is offered to the non-active player as a stratagem/GO card
  when the target is not itself already in melee and carries a ranged
  weapon; its "only unmodified 6 hits" rule is stated in the card's rule
  text rather than a separate enforced flow.
- Heroic Intervention: an eligible CHARACTER unit (not destroyed, not
  already in melee, not yet intervened this turn) belonging to the inactive
  player may intervene, marking it as having fought/engaged.
- Code: `chargePhase.py:ChargePhaseHandler.render_active`, `hi_eligible_units`,
  `unitMutations.py:set_charged / enter_melee`.

**Fight Phase** (`fightPhase.py`)
- The non-active player picks first (fight priority is a stated rule, not
  separately enforced beyond ordering the UI hint); a selected unit must be
  in melee or have charged this turn to act, and can only resolve attacks
  against a target that is actually engaged with it (`melee_with` check).
- Otherwise identical attack-sequence flow to Shooting (A/WS/S/AP/D shown,
  manual hit/wound/save entry, `apply_damage`).
- Code: `fightPhase.py:can_fight_now / _is_target_engaged`,
  `uiLayout/_common.py:render_attack_form`.

**Morale Phase** (`moralePhase.py`)
- Only relevant to units that lost models this turn and have more than 1
  starting model; single-model units and untouched units are auto-skipped.
- Threshold = Leadership − models lost this turn + 1: threshold > 6 is an
  auto-pass (one-click confirm), threshold ≤ 1 always fails, otherwise the
  player rolls a D6 physically and clicks Passed/Failed.
- On failure, the player enters how many models fled; `flee_models` removes
  them and rolls that loss into the turn's loss count.
- Code: `moralePhase.py:_fail_threshold / _render_unit_morale`,
  `unitMutations.py:flee_models`.

## 5. Attack sequence and damage resolution

The core, most heavily tested part of the app —
`combat.py:resolve_attack` (and helpers) implements the full 9E
hit→wound→save→damage pipeline as pure functions, called identically from
Shooting and Fight. It is **semi-manual**: the app never rolls dice, only
computes thresholds/modifiers and applies player-entered results.

Implemented, class A (app computes/enforces) unless noted:

- Hit roll and wound-roll tables, including the fixed 9E wound table
  (S≥2×T → 2+, S>T → 3+, S=T → 4+, S<T → 5+, S≤T/2 → 6+) — `combat.py:wound_threshold`.
- Hit/wound modifier cap at net ±1, floor at 2+ — `combat.py:resolve_attack_modifiers`.
- Unmodified 1 always fails, unmodified 6 always succeeds, independent of
  modifiers — enforced throughout `combat.py:resolve_attack`.
- Save resolution: AP worsens the *roll*, not the threshold; invulnerable
  saves ignore AP entirely and the better of armour/invuln is used
  automatically; if a unit has multiple invulnerable sources, the best
  (lowest) is picked — `combat.py:resolve_save`, `abilityEngine.py:ability_invuln_save`.
  (R-COMBAT-07/08/09)
- Damage per failed save = weapon's Damage characteristic, applied as model
  loss (with proper multi-wound-model bookkeeping) — `unitMutations.py:apply_damage`.
- Feel No Pain — `combat.py:resolve_fnp`.
- Weapon strength parsing (`"User"`, `"+N"`, `"×N"`, fixed int) —
  `attackMath.py:_parse_strength`, never a raw `int()` cast.
- Rapid Fire captions, Combi-weapon profile-selection hit penalty, hit/wound
  reroll-ones (from unit or aura abilities), a unit-level wound-auto-fail
  cap ability — `abilityEngine.py:unit_hit_reroll_ones / unit_wound_reroll_ones /
  unit_wound_auto_fail_max`.
- Mortal-wounds-on-destroy "Explodes" as a mandatory, YAML-declared trigger
  (not a stratagem): the controlling player rolls physically, the app takes
  the gate outcome and applies mortal wounds to nearby units the player
  designates (distance itself is not modeled) — `abilityEngine.py:resolve_explode_effect`,
  wired for several Necron/Ork units (Triarch Stalker, Annihilation Barge,
  Night Scythe, Gunwagon). A stratagem (Curse of the Phaeron) can force an
  automatic explode with a keyword-based CP-cost override.
- Damage-block dice display (thresholds, modifier chips, marker rows) via a
  shared HTML component reused for hit/wound/save — `uiLayout/diceHtml.py`,
  `uiLayout/diceCompose.py`.

Not app-enforced (class B, table-only) even though they are catalogued:
Assault (-1 to hit after Advance), Pistol, Blast, Grenade, weapon-range/LoS,
range measurement, Cover eligibility, Look Out Sir, engagement-only melee
attackers, vehicle/monster shoot-from-melee restrictions — the app has no
weapon-keyword-driven auto-modifiers for these yet (see acceptance catalog
R-COMBAT-18 through 34 for the exact list).

## 6. Abilities, auras, and faction mechanics (`abilityEngine.py`)

A single generic engine reads ability definitions from YAML (`Trigger` /
`Condition` / `Effect` on a shared `Ability` dataclass) and answers whether
an ability currently applies, rather than encoding any faction by name in
`src/`. Concretely working today:

- **Reanimation Protocols** (Necron faction ability, class C): after an
  enemy's attack in Shooting/Fight destroys models but not the whole unit,
  the app computes the D6 pool size (sum of Wounds of destroyed models) and
  a success threshold, both driven by the faction-ability YAML
  (`D6_per_wound` / `success_on: 5`, not hardcoded in `src/`); the player
  rolls physically, enters how many models come back, and the app heals
  them via
  `unitMutations.heal_unit` while correctly removing them from this turn's
  Morale-relevant loss count. Code: `abilityEngine.py:get_after_attack_revive_ability`.
- **Aura-based rerolls** (hit-ones / wound-ones): donor unit must still be
  alive for the aura to apply — `abilityEngine.py:_aura_source_alive`,
  `get_wound_reroll_aura_donor_names`.
- **Buffs** applied to a unit (stat bonuses, invuln grants) via
  `unitMutations.py:apply_buff_to_unit`, read back through
  `abilityEngine.py:buff_stat_bonus`.
- **Once-per-battle abilities** are tracked per player
  (`gameState.py:mark_once_per_battle_used / is_once_per_battle_used`) and
  rendered from the army card.
- **Round-choice / directive abilities** (the generic mechanism behind
  Necron Command Protocol directives) can inject hit/wound/strength/AP
  modifiers or conditional effects (e.g. Light Cover if stationary, shoot
  after Fall Back) into the attack-resolution tab for the current phase.
  Code: `abilityEngine.py:get_active_round_choice_modifier` and the
  `get_active_round_choice_*` family.
- **Deny-capable non-PSYKER units** (e.g. Gloom Prism) are looked up
  generically via `find_unit_ability_by_effect(faction_dir, unit_id,
  "deny_psychic")` rather than a hardcoded unit list.

## 7. Stratagems (Gefechtsoptionen / "GO cards")

All stratagem-like optional rules (core stratagems in `_shared/`, plus
per-faction stratagems) are rendered through one shared component, the "GO
card" (`uiLayout/goCard.py`, wired up by `uiLayout/_common.py` and
`gameProtocoll.py:_render_stratagem_column`), instead of separate bespoke
widgets per stratagem type.

- **Visibility gating**: a GO is only shown if its conditions are met, its
  phase matches the current phase, and (for `phase_reactive` timing) it is
  hidden entirely rather than always-on. If it was already used this
  phase/battle, or the player lacks CP, it is shown greyed-out rather than
  hidden — visibility logic in `gameObjects/stratagem.py:stratagem_visibility`.
- **Five card states**: dormant / ready / used / used_elsewhere / locked,
  each with a distinct border color, so the player can see at a glance
  whether a GO is available, already spent, spent by/for someone else, or
  gated. Code: `goCard.py: GoCardState`.
- **CP cost overrides**: a stratagem's CP cost can vary by target keyword
  (e.g. more expensive against TITANIC units) via `CpOverride` entries —
  `gameObjects/stratagem.py:effective_cp_cost`.
- **Use / Undo**: spending a stratagem deducts CP and marks it used; an Undo
  path exists to reverse a misclick within the same phase where applicable.
  Code: `uiLayout/_common.py:spend_stratagem / undo_stratagem`.
- **Reactive stratagems** (rerolls offered inline at the point of a specific
  roll — damage rolls, psychic tests, charge rolls, advance rolls, attack
  declarations, hit/wound/save rolls) render as an inline reroll box or
  pull-button directly under the relevant dice block rather than in a
  separate stratagem list. Code: `uiLayout/_common.py:render_reactive_stratagem_box /
  render_inline_command_reroll`.
- **Player-scoped visibility**: a GO's `player` field (`active` / `inactive`
  / `both`) determines which player's column it appears in — e.g. Insane
  Bravery (usable by either side) versus a purely offensive stratagem.

## 8. Game protocol / log

`uiLayout/gameProtocoll.py` renders a running battle log for the current
game (hidden during the pre-game setup phase):

- Every significant action (unit selection, phase-relevant action, damage
  application, stratagem use) is appended as a log line tagged with round,
  phase, and unit name. Code: `gameLog.py:log_action`.
- The log view groups entries by round/phase for readability
  (`gameProtocoll.py:_render_battle_log`).
- On game reset, the current log is archived to disk as a timestamped file
  (visible later in the setup screen's "Battle Log Archive" section) and a
  fresh log starts. Code: `gameLog.py:archive_and_reset_log`.

## 9. Victory points

- **Primary VP** (class C): +5/+1/−1/−5 buttons per active player, floored
  at 0; visibility is gated to a configured phase (`vp_phase`) and minimum
  round (`vp_from_round`) so the buttons only appear when scoring would
  actually happen. Code: `unitMutations.py:adjust_vp`,
  `gameActionsArea.py:_render_vp_scoring`.
- **Secondary VP** (class C, optional): up to 3 named slots per player, each
  independently capped at [0, 15]. Code: `unitMutations.py:adjust_secondary_vp`.
- Both are manual trackers — the app does not know *why* VP were earned
  (no objective-marker model, no Slay-the-Warlord flag, etc.); it only
  bookkeeps the number the players tell it to record.

## 10. Internal / developer-only tooling (not a player-facing feature)

`src/gameMechanic/scenarios.py` lets a specific named JSON fixture under
`data/scenarios/` be loaded via a `?scenario=<name>` URL query parameter,
patching session state for quick manual/QA testing of a mid-game situation.
This exists purely to speed up manual verification during development and
is not part of the intended player-facing feature set.

---

## Not implemented / explicitly out of scope

Read this list before assuming a missing behavior is a documentation gap —
these are confirmed absent from the current code, cross-checked against
`docs/spec/acceptance/rules.md` (status: `offen`) and `docs/goals/backlog.md`:

- **Crusade mode** — selectable in setup, immediately blocked with a "planned"
  message; no Crusade data model, no army XP/requisitions/battle traits.
- **Adeptus Custodes as a playable faction** — only a faction-abilities stub
  exists; no units, weapons, wargear, or stratagems. Not selectable as a
  real army.
- **Any faction beyond Necrons/Orks/Custodes** (Space Marines, Tyranids,
  T'au, Adeptus Mechanicus, etc.) — no data at all.
- **In-app army list building** — rosters are pre-authored YAML or
  BattleScribe imports; there is no points-calculator/list-builder UI.
- **Deployment geometry** — deployment zones, alternating placement order,
  post-deployment roll-off placement, Strategic Reserves as a CP-paid
  mechanic, large-model deployment-zone overhang, Fortification placement
  rules. All open/class B or unimplemented class A (R-DEPLOY-01–09,
  Strategic Reserves specifically R-DEPLOY-06, class A but unbuilt).
- **Mission objective-marker control and scoring** — no objective markers,
  no in-range/control computation, no Objective Secured logic, no automatic
  Capture-and-Control VP (R-SCORE-02 through 08).
- **Automatic win/loss/draw determination** beyond a VP-number comparison at
  the fixed round-5 cutoff** — no Warlord tracking, no army-destruction win
  condition (R-SCORE-11–13, R-ROUND-08).
- **Weapon-keyword-driven automatic combat modifiers**: Assault, Pistol,
  Blast, Grenade, automatic-hit weapons (Tesla-style — rendered as a manual
  badge only), reroll mechanics beyond hit/wound-ones, Lethal Hits — none of
  these are computed automatically by the attack sequence today (see
  R-COMBAT-18 through 25, 34, and open backlog items B-048 "Lethal Hits").
- **Overwatch as an enforced sub-flow** — the "only unmodified 6 hits" rule
  is stated as rule text on the Fire Overwatch GO card, not separately
  computed/enforced.
- **Full psychic power roster** — only Smite is implemented; power
  generation/selection before battle and any power beyond Smite (blessings,
  faction-specific powers in `powers.yaml`) are not wired into the Psychic
  Phase flow.
- **Klan/Dynasty-specific subfaction mechanics beyond one dynasty/clan each**
  — subfaction badges and a first subfaction ability set exist for
  Necrons/Orks, but most subfaction-specific keyword/ability variants
  (Novokh, Sautekh, Nephrekh, Snakebites, etc.) are backlog items (B-003),
  not yet functioning.
- **Command point spend/gain caps** — the 1-CP-per-round-from-abilities cap
  and the battle-forged/mission-CP-gain separation are not enforced
  (R-CMD-07/08).
- **Movement-phase geometry rules** — measured distances, terrain-height
  rules, unit coherency, FLY overflight rules, embarking into transports
  (R-MOVE-01, 04, 07, 09, 11–13).
- **Charge-phase geometry rules** — 12" charge-target range check, the 2D6
  charge roll itself (entered as pass/fail by the player, not computed),
  once-per-phase charge-attempt enforcement, Heroic Intervention's 3" move
  check, FLY overflight on charge moves (R-CHARGE-03/04/05/11/12/13).
- **Morale-phase Unit Coherency Check** (the phase's second step) — only
  the Morale Test step (step 1) is implemented (R-MORALE-01, 12, 13).
- **Necron Command Protocol full mechanical dispatch** — protocol/directive
  *selection* is implemented and displayed; most individual directive
  *effects* beyond the two called out in §4 above are display-only or
  unwired (see `docs/spec/processes.md` P-11: "mechanische Effekte noch
  nicht automatisch appliziert" for protocols generally).
