# 06 — Domain Rules & Implementation Gotchas

> Part of the migration handover set. This is the distilled list of Warhammer 40,000 9th
> Edition rule interpretations that were non-obvious enough to cost real debugging time, plus
> the invariant domain constraints the rebuild must not silently relax. Each entry gives the
> rule, why it is non-obvious, and where it lives in code today. Long-form rule research lives
> in `docs/spec/rules_insights.md`, `docs/spec/faction_abilities.md`, `docs/spec/unit_states.md`
> and `docs/spec/army_builder.md` — this document extracts the parts that would otherwise be
> silently reintroduced as bugs by a rebuild team starting from a rules book instead of from
> this codebase's accumulated fixes.

## 1. Faction ability category system

Faction-specific rules in 9E fall into 6 mechanically distinct categories. Every category is
distinguished by `Ability`/`RoundChoiceAbility` YAML shape alone (`ability_type` +
structural fields) — **adding a new faction that only reuses existing categories requires zero
code changes**, only new YAML. This generic-dispatch property is the single most important
architectural fact to preserve in the rebuild; it is what currently keeps `src/` faction-free.
Full schema per category: `05_data_model.md` §7 and `docs/spec/faction_abilities.md`.

| # | Category | `ability_type` | State model | Engine entry point |
|---|---|---|---|---|
| 1 | Round-choice | `round_choice` | `active_protocol_id`, `active_directive`, `used_protocol_ids` (session, reset every round) | `get_active_round_choice_modifier/rerolls/rp_modifiers` (`abilityEngine.py`) |
| 2 | One-time/staged | `activated` | `{player: {stage, round_activated}}` + battle-scoped `used_once_per_battle_abilities` ledger | `armyCard._render_once_per_battle_ability_ui` (generic — handles WAAAGH! too, no faction-specific function) |
| 3 | Auto-progression | `auto_progression` | none — recomputed from `current_round` every render (by design) | *(not implemented)* — no faction currently in the repo (Necrons/Orks/Adeptus Custodes) uses `auto_progression`; `docs/spec/faction_abilities.md` names `get_auto_progression_modifier(faction_dir, phase, round)` as the planned engine function, but no such function exists in `abilityEngine.py` today. This category exists only as the `_schema/auto_progression.example.yaml` reference doc, written for factions (Space Marines, Death Guard) not yet present in `data/wh40k_9e/`. |
| 4 | Resource-based | `resource_based` | *(not implemented — no faction using it yet)* | — |
| 5 | Distribution | `distribution` | *(not implemented — no faction using it yet)* | — |
| 6 | Passive/persistent | `passive` / `triggered` + `timing: persistent` | none, keyword/rule-gated | direct condition checks, no dedicated engine fn |

### 1.1 Round-choice: directive re-selection is per-round, not once-per-battle

**Rule:** Necron Command Protocols (and structurally identical mechanics: Custodes Ka'tahs,
AdMech Canticles, Tyranid Synaptic Imperatives) are re-chosen **every battle round** — 9E wording
is "at the start of each battle round," not "once per battle."

**Why non-obvious:** the "used once" ledger (`used_protocol_ids`) makes it easy to assume each
option, once picked, is fixed for the rest of the game — it is not; only *reuse of the same
option in a later round* is forbidden, not re-selection each round.

**Where implemented:** `gameState.py:_reset_round_choice_state()` re-opens the choice window
every round. The one genuine exception is **Voice of the Triarch** (Silent King), which swaps
the *active protocol itself* mid-round — it does not touch the per-round directive-choice window.

### 1.2 Round-choice: subfaction affinity activates both directives at once

**Rule:** if the active subfaction (Dynasty/Shield Host/etc.) matches a round-choice option's
`subfaction_affinity`, **both** directives (primary + secondary) apply simultaneously that
round instead of the player choosing one.

**Why non-obvious:** the rest of the round-choice UI is built around an exclusive primary-vs-
secondary pick; this is the one case where the choice is bypassed entirely, with a
"… BONUS (BOTH)" badge replacing the normal picker.

**Where implemented:** `abilityEngine.py` (`_active_directive_effects`/`_extra_directive_effects`);
applies both to the round-assigned protocol and to the always-on 6th protocol.

### 1.3 One-time/staged abilities expire at the owner's Command phase, not at turn change

**Rule:** a staged ability (e.g. WAAAGH! Stage 1 → Stage 2) transitions or expires at the
**start of the owner's own Command phase**, not at any turn or round boundary. Stage 2 therefore
persists through the opponent's entire intervening turn.

**Why non-obvious:** it is tempting to reset staged abilities on `_reset_turn_state()` (which
runs on every turn change, for both players) — that would end Stage 2 one turn early. The actual
anchor is asymmetric: only checked, and only advanced, when the ability's own owner becomes the
active player again.

**Where implemented:** `gameState.py:_reset_turn_state()` — only advances/expires a staged
ability when `owner == new active player` **and** `round_activated < current round`.  When a
stage has no `next_stage_id`, the ability is removed from `activated_abilities[player]`
entirely (generic — applies to any staged ability, not just WAAAGH!). The once-per-battle usage
ledger (`used_once_per_battle_abilities`) is **not** cleared by stage expiry — clearing it would
let the ability be re-activated after its stages ran out, which is wrong.

## 2. Unit state model

Full state machine, badge vocabulary and forbidden transitions: `docs/spec/unit_states.md`.
Key structural facts a rebuild's state model must reproduce:

### 2.1 Movement badges are mutex; action badges are additive; two badges are persistent

The rendered badge set for a unit combines three independent layers:

- **Movement slot (mutex, one active at a time):** `STATIONARY` \| `MOVED` \| `ADVANCED` \|
  `RETREATED` \| `CHARGED`, with `FOUGHT` displacing `CHARGED` once combat resolves in the same
  slot position. Reset to `STATIONARY` on every turn change.
- **Action badges (additive, on top of the movement slot):** `SHOT` (persists after being set,
  shown alongside whatever movement badge is active), `FOUGHT`.
- **Persistent badges (survive turn change, not reset by `_reset_turn_state`):** `IN MELEE`,
  `RESERVE`.

**Why non-obvious:** `FOUGHT` does **not** suppress `IN MELEE` — both display together when a
unit fought and is still engaged; it *does* suppress `CHARGED` in the movement slot (a unit that
charged and then fought shows FOUGHT, not CHARGED, once combat resolves).

**Where implemented:** `src/uiLayout/_common.py:state_badges_html()`, unit-card variant
`src/uiLayout/unitCard.py:_state_badges_html()`.

### 2.2 A retreated unit is permanently locked out of movement/shoot/charge/fight for the turn — and a documented regression exists for it

**Rule:** `RETREATED` is a dead-end state for the rest of that unit's turn — no further movement
choice, no shoot, no charge, no fight.

**Why non-obvious / regression history:** `set_movement_status("stationary")` (used generically
whenever a movement choice resets) also clears `flags["retreated"] = False` as a side effect —
which, without a guard, lets a retreated unit be flipped back to "stationary" and then re-enabled
for further movement/actions in the same turn. This is codified as a **mandatory regression
test** in `docs/spec/unit_states.md` §"Regressionstest-Pflicht", not just a fixed bug: the guard
is an early-return in `movementPhase.py:_active_movement()` when `already_retreated == True`.

### 2.3 Model-group death order is priority-based, and Triarchal-Menhir-style units force allocation from the first wound

**Rule (models-lost cap / allocation order):**
- Units with `model_groups` lose models from the **lowest-priority group first**
  (`_apply_group_losses`, sorts by `priority` ascending) — e.g. standard Ork Boyz die before
  the Boss Nob.
- A single attack's damage is capped at the current front model's remaining HP — a single hit
  cannot "spill" its own excess onto the next model within the same attack (9E: excess damage
  from one attack is lost, not carried over). This cap only applies to **single-hit, unresolved**
  damage calls (`apply_damage(..., resolved=False)`, used by the legacy per-wound button flow);
  the newer resolved-total flow (`resolved=True`, from the full attack-sequence renderer) already
  computes the correct total and is not re-clamped.
- **Mortal wounds bypass both the front-model cap and any directed-group lock** (`mortal=True`
  in `apply_damage`) — they spill across model/group boundaries freely, per 9E's mortal-wound
  allocation rule.
- Cross-*attack* overflow (a volley's second, third, … attack, after the front model of the
  targeted group already died) **is not lost** — it spills into the next group in priority order
  (`_apply_directed_group_damage`'s `overflow` branch). This is the load-bearing distinction: an
  attack's own excess is capped/lost, but a volley's later attacks keep landing on the unit until
  either it dies or the volley ends.

**Rule (forced allocation — the "Triarchal Menhir" case):** for a unit whose model groups have
**different** per-model wound values (only the Necron Silent King qualifies today: Szarekh 16
wounds vs. Triarchal Menhirs 5 wounds), the codex forces every attack to be allocated to the
lower-wound group from the very **first** point of damage — not only once that group is already
partly wounded. Homogeneous multi-group units (Ork Boyz + Boss Nob, all Nobz wargear variants —
same per-model wounds in every group) keep the normal 9E free first-choice rule ("can be to any
model in the unit") until a group becomes partly wounded, at which point the partly-wounded
model must be finished off first (also enforced, independent of the heterogeneous-wounds case).

**Why non-obvious:** it would be easy to hardcode a Silent-King-specific check for the forced
allocation rule. Instead the codebase generalizes it correctly:
`Unit.has_per_group_wounds()` (any model group's `stats.wounds` differs from another) is the
data-driven trigger — any future unit with heterogeneous group wounds gets the same forced
allocation automatically, and no unit with homogeneous group wounds is ever wrongly locked.
Locking `model_groups` priority as an *always-on* forced order (regardless of wound
heterogeneity) would be the wrong generalization — it would break the free-choice rule for Ork
Boyz/Boss Nob-style units.

**Where implemented:** `gameMechanic/unitMutations.py:get_locked_group()` (the two-condition
lock check), `apply_damage()` (dispatch between simple/group-wound paths),
`_apply_group_wound_damage()` / `_apply_directed_group_damage()` (priority-ordered depletion).

### 2.4 Melee auto-clear

**Rule:** when a unit is destroyed while engaged, it leaves melee automatically — there is no
separate manual step.

**Where implemented:** `apply_damage()` calls `leave_melee()` whenever the destroyed flag becomes
true and `melee_with` is non-empty, in both the simple and group-wound branches.

### 2.5 Turn-change reset — persistent vs. ephemeral state

| Reset to default every turn change | Persists across turn change |
|---|---|
| `turn_flags.*` → `False` | `in_melee`, `melee_with` |
| `movement_choice` → `"stationary"` | `in_reserve` |
| `lost_models_this_turn` → `0` | `current_wounds`, `models`, `destroyed` |
| `my_will_be_done_active` → `False` | `group_models` |

Getting this table wrong in either direction silently reintroduces a class of bug this codebase
has already found and fixed once (see §2.2's regression test for the canonical example).

## 3. Aura / donor mechanics

Auras are not a single first-class concept — they show up as three different structural
patterns, all keyed off "friendly unit with keyword X within N inches of the donor":

1. **Fixed-range aura ability** (e.g. Royal Warden's Relentless March, Canoptek Control Node):
   plain `Ability` with `trigger.timing: persistent`, `effect.target` naming the recipient class
   (e.g. `friendly_dynasty`), and the range baked into the rule text / a `within_inches`
   condition — no dedicated "aura" dataclass, just a persistent triggered ability read by
   whichever phase handler checks it.
2. **Auto-progression aura with growing range** (Death Guard Contagions of Nurgle): the
   `progression[].aura_range` field grows per round (1"→3"→6"→9", `round_max: null` from round 4
   onward makes it permanent) — this is the one place `aura_range` is a named schema field
   rather than embedded prose.
3. **Round-choice directive framed as an aura** (e.g. Necron Command Protocols' Conquering
   Tyrant): same shape as any other directive effect, distinguished only by its `effect.type`
   and rule text implying a radius — there is no structural difference from a non-aura directive
   in the schema.

**Gotcha:** "donor" units (the model whose presence grants the buff) are never a separate
runtime concept from the unit that has the ability — the aura is just an `Ability`/effect
attached to the donor's own `Unit`/ability list; the "does a friendly unit have keyword X within
N inches" check is the caller's responsibility (largely still a manual/table-checked condition
in many cases — see `condition_prompt`/`applies_when` convention below), not something the
engine resolves geometrically. There is no spatial/proximity engine — several documented Arkana
entries remain `descriptive` specifically because a "spatial proximity tracking" subsystem does
not exist yet (`docs/spec/faction_abilities.md` §"Arkana — Dispatch- vs. Display-Status").

## 4. Reroll semantics

Reroll grants are tracked as a **set of reroll-kind tags**, not a boolean per stat:

`get_active_round_choice_rerolls(faction_dir, phase, use_melee)` returns
`set[str]` from `{"reroll_save_1", "reroll_hit_1", "reroll_wound_1"}`. A unit-ability reroll
(e.g. "The Lord's Will": `effect.type: reroll_hit_1`) is a separate ability-level dispatch, not
funneled through the same round-choice function — the two systems (round-choice rerolls vs.
unit-ability rerolls) are parallel, not unified under one reroll engine. `Ability.effect.type`
values seen for rerolls follow the pattern `reroll_<stat>_1` (reroll a natural 1 on that stat) —
there is no generalized "reroll all failed" or "reroll any N" grammar; each specific reroll rule
is its own named effect type.

**Gotcha for the rebuild:** do not assume a single `reroll: {stat, condition}` structured field
exists anywhere — reroll semantics are entirely encoded in the `effect.type` string itself
(`reroll_hit_1`, `reroll_wound_1`, `reroll_save_1`, `rp_reroll` for Reanimation Protocols), and
the numeric modifier system (`_WIRED_EFFECT_TYPES`: `hit_modifier`, `wound_modifier`,
`save_modifier`, `strength_modifier`, `ap_bonus`, `move_bonus`, `leadership_bonus`) is a
completely separate, generic dict-of-deltas mechanism from the reroll-tag-set mechanism. Adding
a new entry to `_WIRED_EFFECT_TYPES` (`docs/spec/faction_abilities.md` §"Direktiv-Wiring-Status")
wires it for **every** faction with round-choice directives automatically — no per-faction code.

## 5. Damage flow — the full picture

Combining §2.3 with the two systemic branches in `unitMutations.py:apply_damage()`:

```
apply_damage(uid, faction, dmg, unit, mortal=False, resolved=False)

  IF unit has group_wounds (per-model-group HP pools):
      IF a defender-chosen active group is set AND not mortal:
          the lock (get_locked_group) must match the active group, else ValueError
          IF not resolved: clamp dmg to that group's front-model remaining HP
          apply to that group; any overflow spills to the next group by priority
      ELSE (no directed target, OR mortal):
          IF not mortal and not resolved: clamp dmg to the front group's remaining HP
          deplete groups in priority order
      → recompute models/current_wounds/destroyed from group_wounds
      → auto leave_melee() if destroyed and still engaged

  ELSE (flat current_wounds/models unit, no per-group pools):
      IF not mortal and not resolved and models_max > 1:
          clamp dmg to the front model's remaining HP
          (front_hp = current_wounds − (models−1) × unit.wounds)
      current_wounds -= dmg (floor 0)
      models = full_models + (1 if partial wound remains else 0)
      IF current_wounds <= 0: destroyed = True, auto leave_melee()
      → track lost_models_this_turn; spill losses into group_models display bookkeeping
        if a legacy group_models dict exists without group_wounds (display-only path)
```

**The `resolved` flag is the load-bearing distinction between two calling conventions**: the
older per-wound-button UI calls with `resolved=False` (single hit at a time, needs the
front-model clamp applied here), while the newer full attack-sequence resolver
(`render_attack_form`, "6d-v2") already computes the correct total damage and calls with
`resolved=True` to skip the redundant clamp. A rebuild that unifies these two call sites onto one
resolved-total convention should drop the `resolved=False` clamp path entirely rather than port
both.

## 6. Invariant domain constraints (binding, do not relax)

These are asserted directly in `CLAUDE.md` and enforced by architecture tests
(`docs/spec/architecture_invariants.md`); they are listed here because a rebuild starting from
"clean" UI/UX instincts is the most likely place they get silently violated.

### 6.1 Player sidebars are bound to `first_player`/`second_player`, never to `active`

**Rule:** the left sidebar is always `first_player`, the right is always `second_player` —
**layout never follows whose turn it currently is.** `first_player`/`second_player` are fixed at
setup and immutable for the rest of the game; `active`/`inactive` is a separate, per-turn
concept that must never drive which side of the screen a player's army renders on.

**Why this needs to be said explicitly:** it is a natural UX instinct to put "the active player"
on a privileged side (e.g. always left) — that was an actual documented bug
(`project_bug_fightphase_enemy_disappears` in project memory: a `ValueError` from parsing a
weapon-strength string as `int()` crashed the center column and, while debugging it, the
active/inactive-vs-first/second conflation surfaced as a related layout defect). Keep the two
concepts (seating vs. turn) fully decoupled in the rebuild's data model, not just in the UI
layer.

### 6.2 Keywords are UPPERCASE in the data layer, always

See `05_data_model.md` §5.2. Any comparison against a keyword string must either rely on data
that is already uppercase, or explicitly `.upper()` both sides (`Unit.has_keyword()` does the
latter defensively) — never assume case-sensitivity is safe to skip on one side only.

### 6.3 Weapon strength is never `int()`-parsed directly

See `05_data_model.md` §5.1 for the full grammar; `gameMechanic/attackMath.py:_parse_strength`
is the only correct implementation. This is independently documented in three places (CLAUDE.md,
project memory, `rules_insights.md`) because it has recurred as a bug more than once — treat
"someone will eventually call `int(profile.strength)` directly" as a near-certainty in the
rebuild and design the type/API so that mistake is not representable (e.g. make strength a
small value type with an explicit `.resolve(unit_strength)` method rather than a bare
`int | str` union).

### 6.4 Generic `src/` — no faction name or faction vocabulary in code

See `05_data_model.md` §1. Enforced today by `tests/architecture/test_generic_src.py` (no
faction **names**) and `test_generic_src_vocab.py` (no faction-specific **vocabulary/strings**,
including inside string literals like `weapon_type == "Dakka"`, not just identifiers — a scanner
subtlety worth reproducing: architecture guards that only grep identifiers will miss
faction-specific behavior smuggled in as a string comparison). Any new mechanic that needs
faction-specific numbers or thresholds must express them as YAML data the generic engine reads,
not as a branch on faction name/dir.

### 6.5 Cover interacts with phase and charge status, not uniformly

**Rule:** Dense cover (−1 to hit) and Light cover (+1 to save) apply only in the Shooting phase;
Heavy cover (+1 to save) applies only in the Fight phase, **except** when the defending unit
itself charged this turn (in which case Heavy cover does not apply).

**Why non-obvious:** cover is easy to model as one flat "+1 save, always" toggle; the actual
rule is phase-gated on two different axes (which cover tier, which phase) plus one exception
tied to the defender's own movement history that turn.

**Where implemented:** table-checked by the player in most flows (`docs/spec/rules_insights.md`
"Cover"); the one exception with an actual engine hook is Eternal Guardian's stationary-cover
directive (§6.6 below), which is careful not to double-apply on top of a manual cover checkbox.

### 6.6 A directive-granted cover bonus and a manually-tracked cover bonus must never both apply

**Rule:** Eternal Guardian's Directive 1 (Necrons) grants Light Cover whenever the unit is
attacked while stationary, for the whole battle round it applies (9E: "each time an attack is
made against this unit," not phase-gated the way the ordinary cover rules are).

**Why non-obvious:** the ordinary Light Cover checkbox already exists in the Shooting-phase save
block for manually-declared cover. Adding the directive's own +1 in the same modifier-collection
function (`_collect_def_save_modifiers`) as well as the pre-checked checkbox would silently
double the bonus.

**Where implemented:** the directive is applied **only** via a pre-checked, disabled checkbox in
the Shooting-phase SAVE block (chosen pragmatically to cover the common case — a documented,
accepted 90%-coverage tradeoff, not a full 9E-literal "any phase" implementation) —
`unitMutations.py`'s `movement_choice == "stationary"` state check, engine function
`get_active_round_choice_light_cover_if_stationary(def_player, def_uid)`. The checkbox mechanic
is the single source of the +1; it is deliberately **not** additionally summed in
`_collect_def_save_modifiers`.

### 6.7 Combi-weapons: a "select one or both profiles" choice, made once, before targeting — not a permanent malus

**Rule:** for weapons offering two profiles that can be fired together (e.g. Shoota/Skorcha
combi-weapons), firing **both** profiles in the same phase applies a −1 hit-roll penalty to
**both** profiles equally. This choice is made **before** target selection, not as an
ever-present weapon-stat malus (unlike, say, a Power Klaw's fixed hit penalty).

**Why non-obvious:** it looks structurally similar to a fixed weapon-profile penalty
(`hit_roll_penalty`, as used by Power Klaw/Killsaw) but is actually conditional on a
same-phase, same-declaration choice — and needed its own `WeaponProfile.combi: bool` field
rather than reusing `effect`, because each profile of a combi-weapon already carries its own
distinct mechanic in `effect` (e.g. `alternating_fire`/`auto_hit`), leaving no room for a second
tag in the same dict.

**Where implemented:** `_combi_hit_penalty()` (`gameMechanic/attackMath.py`, pure function,
independently testable). Profile selection renders as a checkbox-per-profile (instead of a
radio button) whenever `any(p.combi for p in profiles)`
(`render_group_assignment`/`_common.py`); the result becomes a named hit-modifier entry
(`"Combi (both profiles)"`) fed into the same modifier stack `resolve_attack_modifiers`
(`combat.py`) already uses for Dense Cover / Fall-Back / Heavy-advanced — no combi-specific
branch inside `combat.py` itself. Full detail: `docs/spec/rules_insights.md` "Kombi-Waffen".

### 6.8 Two "Quantum Shielding"-named mechanics are unrelated — do not merge them

**Rule:** the Quantum Deflection **stratagem** (temporary fixed 4+ invulnerable save) and the
Quantum Shielding **vehicle ability** (permanent 5+ invuln + unmodified wound rolls of 1–3
auto-fail) share a name family but are mechanically and structurally independent — different
triggers, different durations, different carriers (Stratagem vs. Unit ability).

**Why non-obvious:** the shared name invites collapsing them into one mechanic during a rules
pass; they must stay separate YAML entries and separate engine handling.

**Where implemented:** the wound-auto-fail half is modeled as a generic floor —
`resolve_attack_modifiers(..., wound_auto_fail_max=N)` raises the wound-roll floor from 2 to
`N+1`, checked against the **unmodified** roll (no wound-roll buff can lower it below the floor)
— `gameMechanic/combat.py`.

**Adjacent naming trap (INV-4b scanner):** giving a new `unit_abilities.yaml` ability `id` a
substring like `..._wound_auto_fail` makes the substring "fail" register as a
necron-exclusive vocabulary token in the architecture guard's data scan
(`tests/architecture/_vocab.py`), which then false-flags every generic use of "fail" anywhere
in `src/` (`fightPhase.py`, `moralePhase.py`, `chargePhase.py`, …) as a suspected Necron leak.
Fix pattern: keep new ability `id` suffixes within the guard's already-allowed stopword list
(e.g. `quantum_shielding_wound_deny`, not `..._wound_auto_fail`) — `effect.type` itself is safe
to name freely, since it is not scanned under a `NAME_KEYS` field the way `id`/`keywords`/
`faction`/`subfaction` are. A rebuild's own architecture guard (if one is built) should decide up
front which fields are vocabulary-scanned, to avoid the same false-positive class.

### 6.9 `condition_prompt` / `applies_when` — the pattern for "app cannot verify this, ask the player"

**Rule shape, not a single rule:** several effects depend on a battlefield fact the app cannot
compute (e.g. Ork Gretchin's "Cowardly" attrition penalty depends on whether a friendly
RUNTHERD is within 6" — a spatial fact). These are modeled as a `condition_prompt` (the exact
checkbox wording shown to the player) + `applies_when` (whether the modifier is active when the
checkbox is checked `true` or unchecked `false`) pair, nested as a raw sub-entry inside
`effect.effects`, not as first-class fields on `Ability`/`Effect` (an intentional, still-open
schema debt — see backlog item "condition_prompt/applies_when as first-class fields").

**Why non-obvious:** this is the same pattern already used for manual cover-type checkboxes, but
generalized only informally — there is no single documented "table-checked condition" schema
field; each occurrence currently duplicates the same two ad hoc keys.

**Where implemented:** `moralePhase.attrition_modifier_abilities()` /
`moralePhase._attrition_threshold()` for the Cowardly example;
`docs/spec/faction_abilities.md` §"Effekttyp attrition_modifier" for the full worked case. A
rebuild should consider promoting this to a genuine first-class schema field (Class B/C rules in
the acceptance catalog vocabulary — `docs/spec/acceptance/rules.md`: App-computed vs.
table-verified vs. hybrid) rather than reproducing the ad hoc nesting.

## 7. Quick-reference: rule → non-obvious reason → code location

| Rule | Non-obvious because | Code |
|---|---|---|
| Command Protocol directive is chosen every round | Looks like a once-per-battle pick due to the used-ledger | `gameState.py:_reset_round_choice_state` |
| WAAAGH! Stage 2 outlives the opponent's turn | Anchored to owner's own Command phase, not turn change | `gameState.py:_reset_turn_state` |
| Retreated units can't be re-enabled via "stationary" | Shared reset function also clears the retreat flag | `movementPhase.py:_active_movement` (guarded regression) |
| Silent King forces allocation to Menhirs from wound 1 | Generalized via wound-heterogeneity, not a King-only special case | `unit.py:has_per_group_wounds`, `unitMutations.py:get_locked_group` |
| Mortal wounds ignore the front-model damage cap and group lock | Cap/lock exist only for normal-damage single hits | `unitMutations.py:apply_damage` (`mortal=True` branch) |
| A destroyed engaged unit leaves melee automatically | No separate manual "leave melee" step exists | `unitMutations.py:apply_damage` → `leave_melee()` |
| Eternal Guardian cover is a pre-checked disabled checkbox, not a second modifier source | Avoids double-counting against the manual cover checkbox | `unitMutations.py` (`movement_choice`), `abilityEngine.get_active_round_choice_light_cover_if_stationary` |
| Combi-weapon −1 applies to both profiles only if both are fired this phase | Looks like a fixed weapon malus (like Power Klaw) but is a per-declaration choice | `attackMath.py:_combi_hit_penalty` |
| Quantum Deflection (stratagem) ≠ Quantum Shielding (vehicle ability) | Same name family, unrelated mechanics | `combat.py` (`wound_auto_fail_max` floor) |
| Weapon strength string grammar (`User`, `+N`, `×N`, `*`) | `int()` crashes on every non-numeric case | `attackMath.py:_parse_strength` |
| Sidebar side is fixed to first/second player, never to active/inactive | UX instinct says "put the active player somewhere privileged" | layout constraint, `CLAUDE.md` |
