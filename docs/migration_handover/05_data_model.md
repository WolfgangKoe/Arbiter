# 05 — Data Model & Loader Contract

> Part of the migration handover set. Documents the YAML data layer and the loader that turns
> it into runtime objects, as they exist today — not as originally planned. Where a planning
> spec (`docs/spec/loader_contract.md`, `docs/spec/army_builder.md`) describes a field or API
> that the current code does not implement, this is called out explicitly rather than glossed
> over, because the rebuild team must not assume the aspirational spec is the shipped contract.

## 1. Binding principle: the YAML layer is stable, reuse it as-is

`data/wh40k_9e/` is framework-independent — plain YAML, no Streamlit, no Python object
references. **The rebuild does not need to redesign this layer.** It needs a loader in the new
stack that reproduces the parsing/validation behavior documented below. Do not propose schema
changes as part of the migration; if a schema gap is found, record it as a finding, not a
rewrite.

The complementary binding principle is **generic `src/`**: no faction name or faction-specific
string may appear in code — every faction difference is expressed in YAML. This is enforced
today by architecture guards (`tests/architecture/test_generic_src.py`,
`test_generic_src_vocab.py`, tracked in `docs/spec/architecture_invariants.md` INV-4/INV-4b) and
must be preserved by the rebuild: a hardcoded `if faction == "necrons"` anywhere outside a YAML
file is a bug, not a shortcut. `gameObjects/roszImporter.py`'s faction-name-string mapping
(`_FACTION_CATALOGUE_MAP`, BattleScribe catalogue name → internal faction slug) is the one
accepted exception — it normalizes an external I/O format at the import boundary, not game
logic.

A second invariant worth carrying forward: YAML is read **only** through the loader
(`gameObjects/loader.py`; `gameObjects/roszImporter.py` only **writes** converted rosters and
reads back through `load_unit_catalog`). No other module parses YAML directly. This is INV-2 in
`docs/spec/architecture_invariants.md`.

## 2. Directory layout

```
data/wh40k_9e/
  _schema/                        # annotated example YAML for the 3 faction-ability
                                   # progression types (see §7) — documentation only,
                                   # not loaded by any code path
  _shared/                        # cross-faction data, loaded for every faction
    stratagems.yaml                 # 7 "core" stratagems, wired
    shared_abilities.yaml           # universal rules (ObjSec, Deep Strike, FNP, Fly, …) — stub, not wired
    shared_powers.yaml              # Smite / Deny the Witch / Perils of the Warp — stub, not wired
    detachment_types.yaml           # detachment CP cost/benefit table, wired
  necrons/  orks/  adeptus_custodes/     # one directory per implemented faction
    units.yaml                      # unit catalog (statlines + weapon refs)
    weapons.yaml                    # weapon catalog (profiles)
    faction_abilities.yaml          # faction-wide rules; ability_type distinguishes categories
    unit_abilities.yaml             # rules bound to a specific unit_id or keyword
    subfaction_abilities.yaml       # rules bound to a subfaction (Dynasty/Clan/Shield Host)
    wargear.yaml                    # wargear items, some carrying an ability
    relics.yaml                     # named relics (weapon or wargear replacements)
    warlord_traits.yaml             # warlord traits (display-only today, see §8)
    arkana.yaml                     # Necrons only — Cryptek arkana (display-only, see §8)
    stratagems.yaml                 # faction-specific stratagems (appended after _shared)
    points.yaml                     # Matched Play point costs (setup screen only, not loaded in-game)

data/rosters/
  <name>.yaml                      # one file per saved army list, see §6
```

`data/wh40k_9e/_schema/*.example.yaml` files are richly commented reference material for the
three `faction_abilities.yaml` progression mechanics (`auto_progression`, `one_time`,
`round_choice`) — they are never read by `loader.py`; treat them as schema documentation to
carry into the rebuild's own docs, not as data.

## 3. Loader entry points (`src/gameObjects/loader.py`)

The **actual** public surface is a set of per-concern functions, not the single
`load_army(faction, roster_path) -> Army` API that `docs/spec/loader_contract.md` and
`docs/spec/army_builder.md` describe as the target design. Both specs are forward-looking
design documents from an earlier planning session ("Ziel 5c") that has not been fully carried
out. The rebuild should treat those two documents as **design intent**, and this section as
**what ships today**:

| Function | Returns | Notes |
|---|---|---|
| `load_army(faction_dir)` | `(list[Unit], list[str])` | Loads every unit in `units.yaml` (or legacy `army.yaml`), resolves weapon refs. Second tuple element (`unmatched`) is always `[]` — roster-driven unmatched-handling is not implemented here. |
| `load_unit_catalog(faction_dir)` | `dict[unit_id, Unit]` | Thin wrapper over `load_army`. |
| `load_weapon_catalog(faction_dir)` | `dict[weapon_id, Weapon]` | Parses `weapons.yaml`. |
| `load_weapon_abilities(faction_dir)` | `dict[weapon_id, list[effect dict]]` | Inline `effect:` blocks per weapon profile. |
| `load_faction_abilities(faction_dir)` | `list[Ability]` | Skips `round_choice` and `descriptive` entries. Cached per faction. |
| `load_round_choice_abilities(faction_dir)` | `list[RoundChoiceAbility]` | Filters `faction_abilities.yaml` for `ability_type: round_choice`. Cached. |
| `load_round_choice_label(faction_dir)` | `str` | Reads top-level `round_choice_label`, default `"Round Abilities"`. Cached. |
| `load_faction_display_name(faction_dir)` | `str` | Reads top-level `faction:`. |
| `load_subfaction_meta(faction_dir)` | `(field_name \| None, ui_label)` | Reads top-level `subfaction_field`/`subfaction_label` — the mechanism that keeps "Dynasty" vs. "Clan" vocabulary out of `src/`. |
| `load_unit_abilities(faction_dir)` | `list[Ability]` | Parses `unit_abilities.yaml`. Raises `ValueError` at load time for two effect-type shape violations (see §5.4). Cached. |
| `load_subfaction_abilities(faction_dir)` | `list[Ability]` | Flattens all `subfactions[].abilities[]`. Cached. |
| `load_stratagems(faction_dir)` | `list[Stratagem]` | Loads `_shared/stratagems.yaml` first, then `<faction>/stratagems.yaml`. Cached. |
| `load_wargear_catalog(faction_dir)` | `dict[wargear_id, raw dict]` | **Not** turned into a dataclass — raw YAML dict is the runtime shape. |
| `load_relic_catalog(faction_dir)` | `dict[relic_id, raw dict]` | Same — raw dict, converted to `Weapon`/`TriggeredEffect` lazily by `_apply_relic`. |
| `load_wargear_abilities(faction_dir)` | `list[Ability]` | Only wargear entries carrying an `effect:` block become `Ability` objects. |
| `load_detachment_types()` | `list[DetachmentType]` | Faction-independent, reads `_shared/detachment_types.yaml`. |
| `load_points(faction_dir)` | `dict[id, int]` | Flattens `points.yaml` units + wargear + faction-ability `cost_pts` (Arkana) into one id→cost map. **Not used during a game** — setup-screen only (see §3.1). |
| `resolve_bracket_stats(unit, current_wounds)` | `dict[str, str \| None]` | Vehicle damage-bracket degradation lookup. |
| `load_roster_metadata(roster_path)` | `dict` | Cheap metadata read (`display_name`, `faction_dir`, resolved `subfaction`) without loading units. |
| `load_roster(roster_path, catalog)` | `(list[(Unit, model_count)], list[unmatched_id])` | The actual roster resolver — see §6. |

No function named `load_army(faction, roster_path)` returning an `Army` dataclass exists; no
`Army` dataclass exists at all. `gameObjects/detachment.py` defines `Detachment` and
`DetachmentType`/`SlotConstraint`, but nothing in `loader.py` currently builds a `Detachment`
from a roster — detachment typing is loaded (`load_detachment_types`) but not yet bound to a
roster's units.

### 3.1 What the loader deliberately does not load during a game

| File / field | Reason |
|---|---|
| `points.yaml` | Only consulted by `load_points()` for the setup/army-builder screen, not during play. |
| `power_level` (in `units.yaml`) | Setup-screen Open-Play balancing only (`scaled_pl()`). |
| `relics.yaml` / `wargear.yaml` / `warlord_traits.yaml` / `arkana.yaml` (in full) | Only the specific entries a roster references get resolved; the loader never table-scans these for a whole faction during play. |

### 3.2 Validation and error behavior

- `load_yaml(path)` wraps `yaml.safe_load`; a YAML syntax error raises `YamlDataError` (subclass
  of `ValueError`) carrying the file path — the only place a bad file surfaces as an exception
  from parsing itself.
- Beyond that, the loader is **permissive by construction**, not by an explicit "warnings list."
  There is no `Army.warnings` collection as `docs/spec/loader_contract.md` describes. Missing
  optional keys fall back to sane defaults (`d.get(...)`); missing *required* keys (e.g. `d["id"]`,
  `d["wounds"]`) raise a plain `KeyError`/`ValueError` from dict access — uncaught, so a malformed
  catalog entry crashes the load rather than degrading gracefully.
- Two loud, explicit load-time guards exist and should be reproduced 1:1 in the rebuild, because
  they exist specifically to prevent a broken UI state discovered only at render time:
  - `_require_wound_auto_fail_label` (`loader.py:678`) — an ability with
    `effect.type: wound_auto_fail` must carry a `badge_label` or `name_en`, else `ValueError` at
    load time (the auto-fail badge has nothing to render otherwise).
  - `_require_explode_effect_shape` (`loader.py:697`) — an ability with `effect.type: explode`
    must carry `roll_threshold`, `radius` and `damage`, else `ValueError` at load time.
  - `_check_exclusive_swaps` (`loader.py:240`) — a roster picking two mutually-exclusive
    `scope: group` weapon swaps (both replacing the same base weapon) raises `ValueError` when
    the roster is resolved, not silently picking one.
- `load_roster()` raises `ValueError` if a roster YAML is missing `faction_dir` — there is no
  faction fallback/guess (this was itself a fixed bug, see `architecture_invariants.md` INV-4
  debt-ledger entry "S128").
- Unresolvable unit IDs in a roster are **not** an error: they are collected into the
  `unmatched: list[str]` return value and simply not loaded — the caller (setup screen) is
  expected to display them.

## 4. Entity schemas

All stat fields that can render as `"3+"`, `"*"`, `"N/A"` are stored as `str` in YAML and parsed
individually by the loader (never a blanket "everything is a string" — e.g. `wounds`,
`models_min/max`, `strength`, `toughness`, `oc` are parsed to `int`).

### 4.1 Unit (`units.yaml` → `gameObjects.unit.Unit`)

| Field | YAML key | Required | Convention |
|---|---|---|---|
| id | `id` | yes | dotted namespace, e.g. `wh40k_9e.necrons.unit.warriors` |
| name_en / name_de | `name_en` / `name_de` | yes | — |
| faction | (injected by loader from directory, not per-unit YAML) | — | — |
| subfaction | `subfaction` | no | only used to resolve `<PLACEHOLDER>` keywords (§5.2); rosters carry the actual subfaction choice separately |
| battlefield_role | `battlefield_role` | yes | list, e.g. `[HQ]`, `[Troops]` |
| keywords | `keywords` | yes | **list, every entry UPPERCASE** (CLAUDE.md domain constraint) |
| wounds | `wounds` | yes | int, per-model wounds (base value; per-group override via `model_groups[].stats.wounds`) |
| models_min / models_max | `models_min` / `models_max` | yes | int |
| power_level | `power_level` | no | int, default 0 if absent; setup-screen only |
| move / ws / bs | `move` / `ws` / `bs` | yes | `str`, e.g. `6"`, `3+` |
| strength / toughness | `strength` / `toughness` | yes | `int` (unit's own S/T — **not** the weapon-strength grammar, see §5.1) |
| attacks | `attacks` | no | `int`, `null`/`"-"` for buildings/fortifications → `None` |
| save | `save` | yes | `int` (target number, e.g. `3` = 3+) |
| invuln_save | `invuln_save` | no | `int` or `null`; only unit-intrinsic invulns (dynasty/subfaction invulns are applied later by `subfaction_abilities.yaml` effects) |
| leadership | `leadership` | no | `int` or `None` for buildings |
| oc | `oc` | yes | `int`, Objective Control |
| fnp | `fnp` | no | `int` or `null` |
| rules | `rules` | no | list of internal rule-keyword strings (e.g. `livingMetal`) — the vocabulary `Ability.Condition.has_rules` gates against |
| weapons | `weapons: [{ref, model_restriction?}]` | conditional | list of weapon-catalog refs; **omitted** if the unit has `model_groups` (§4.3) — the loader derives the union instead |
| wargear_options | `wargear_options: [{type, with, replaces?, item?}]` | no | `type` is `replace` \| `replace_pair` \| `add` |
| damage_bracket | `damage_bracket: [{wounds_min, wounds_max, move?, ws?, bs?, attacks?}]` | no | vehicle degradation table; only fields that actually change need to be listed |
| model_groups | `model_groups: [...]` | no | see §4.3 |

**Close Combat Weapon default:** any unit resolved without at least one melee-profile weapon
gets a synthetic `close_combat_weapon` (S/AP/D "User"/0/1) appended automatically
(`loader.py:434`, and again after relic/wargear swaps at `loader.py:1174`) — this is not a YAML
entry, it is loader-injected.

### 4.2 Weapon / WeaponProfile (`weapons.yaml` → `gameObjects.weapon.Weapon`/`WeaponProfile`)

Every weapon is a `profiles: [...]` list, even single-profile weapons (one-entry list) — this
keeps combat code free of a dual-profile special case. Dual-profile weapons (e.g. Staff of
Light) give each profile a `name_en` ("Shooting"/"Melee"); single-profile weapons omit it.

| Field | YAML key | Convention |
|---|---|---|
| weapon_type | `weapon_type` | free text, e.g. `"Rapid Fire 1"`, `"Assault 4"`, `"Melee"`, `"Heavy 2D6"` |
| range_inches | `range_inches` | `int`, `0` for melee |
| attacks | `attacks` | `str`: fixed int as string (`"1"`), dice notation (`"D6"`, `"2D3"`), or `"*"` = use `unit.attacks` (resolved before `resolve_attack_sequence()`, same as `"User"` strength) |
| strength | `strength` | `int` **or** the strength grammar string — see §5.1, never `int()` it directly |
| ap | `ap` | parsed to `int`; `"*"`/`"-"` in YAML are treated as `0` |
| damage | `damage` | `str`, dice notation allowed (`"1"`, `"D3"`, `"D3+3"`) |
| abilities | `abilities` | free-text special-rule string |
| is_melee | `is_melee` | `bool` |
| ignores_fnp | `ignores_fnp` | `bool`, default `False` |
| effect | `effect: {...}` | optional structured effect dict (same vocabulary as `Ability.effect`), consumed by `load_weapon_abilities()` |
| max_attacks | `max_attacks` | optional int cap, used together with `effect.type: extra_attacks` (see `docs/spec/rules_insights.md` "extra_attacks — two classes") |
| grantsKeyword | `grantsKeyword` (**camelCase — deliberate exception**, see §8) | optional str; grants this keyword to the bearing unit generically, resolved by `_apply_weapon_granted_keywords` |
| combi | `combi` | `bool`, default `False`; marks a "select one or both profiles" weapon — see `docs/spec/rules_insights.md` "Kombi-Waffen" |

### 4.3 Model groups (`units.yaml: model_groups` / roster `group_loadouts`)

Units whose datasheet has genuinely different sub-models (Ork Boyz + Boss Nob, Necron Silent
King's Szarekh + Triarchal Menhirs) declare `model_groups` instead of a flat `weapons:` list:

| Field | YAML key | Notes |
|---|---|---|
| id / name_en | `id` / `name_en` | — |
| count | `count` | `int`, `"remainder"` (fills whatever is left after fixed-count groups), or `"models_max"` (whole unit is this one group) |
| weapons | `weapons: [{ref}]` | this group's default loadout |
| priority | `priority` | `int`; **lowest priority dies first** when the unit takes losses (`_apply_group_losses`) |
| stats | `stats: {attacks?, strength?, wounds?, ws?, bs?}` | per-group stat override; missing keys fall back to the unit-level stat |
| weapon_swaps | `weapon_swaps: [{id, scope, replaces, options, pick?, limit?}]` | datasheet wargear options, expressed as *replacements* (`replaces: []` = pure addition). `scope: group` = whole group swaps together; `scope: per_model` = individual models swap and the loader splits them into fixed-weapon sub-groups. `limit`: `any` \| `per_10` \| `per_5` \| `per_3`. `pick`: how many options are chosen (repeats allowed, e.g. 2× killsaw). |

Units *without* `model_groups` get a synthetic single group `{id: "models", weapons: unit.weapons,
priority: 1}` created by `load_roster()` after resolution (`loader.py:1246`), so all runtime unit
state uses the same group-based flow regardless of whether the YAML declared groups explicitly.
A `units.yaml` entry with only one `model_groups` entry is invalid data (the synthetic-group path
exists precisely so a single group is never hand-declared).

Two `scope: group` swaps on the same group that both list an overlapping `replaces` weapon are
mutually exclusive — the loader raises if a roster picks both (`_check_exclusive_swaps`).
`scope: per_model` swaps are exempt from this check by design: they split disjoint model subsets
of the same group, so overlapping `replaces` lists across them is expected, not a conflict
(`docs/spec/rules_insights.md`).

### 4.4 Ability (`faction_abilities.yaml` / `unit_abilities.yaml` / `subfaction_abilities.yaml` / `wargear.yaml` → `gameObjects.ability.Ability`)

| Field | YAML key | Notes |
|---|---|---|
| id | `id` | dotted namespace |
| name_en | `name_en` | — |
| source | `source` | free text, e.g. `faction_rule`, `unit_ability`, `dynastic_code`, `wargear` |
| rule_text | `rule_text` | English rules text, shown in UI |
| trigger | `trigger: {timing, phase, player?, stage?, event?}` | `timing` values seen: `phase_start`, `phase_end`, `phase_any`, `phase_reactive`, `persistent`, `pre_game`; `player`: `active` \| `inactive` \| `either`; `stage` is schema-only (data documentation — no code branches on it, per `Trigger` docstring) |
| conditions | `conditions: [{has_rules?, has_keywords?, within_inches?, max_uses?, min_round?, unit_not_destroyed?, needs_healing?, once_per_battle?}]` | list, ANDed by `get_abilities_for_unit`/engine callers |
| effect | `effect: {type, target?, amount?, stat?, modifier?, success_on?, handler?, revive?, effects?, roll_threshold?, roll_type?, radius?, damage?}` | `type` is the dispatch key read by `abilityEngine.py`; unrecognized types are safe (descriptive-only) unless the loader has an explicit shape guard (§3.2) |
| ability_type | `ability_type` | `triggered` (default) \| `activated` \| `round_choice` \| `descriptive` \| `passive` \| `auto_progression` — drives which of the 6 category flows picks the entry up (see `06_domain_rules_and_gotchas.md` §1) |
| badge_label | `badge_label` | optional UI badge text |
| extra_uses | `extra_uses: [{has_keyword, bonus}]` | data-driven extra activation uses, e.g. PHAERON gives My Will Be Done +1 use |
| unit_id | `unit_id` | set only for `unit_abilities.yaml` entries |
| wargear_id | `wargear_id` | set only for wargear-derived abilities |

`round_choice` and `descriptive` entries in `faction_abilities.yaml` are **excluded** from
`load_faction_abilities()` — they are loaded by `load_round_choice_abilities()` instead, or (for
`descriptive`, e.g. Arkana entries with no engine handler) not converted into an `Ability` object
at all; they remain reachable only as raw YAML for display purposes.

### 4.5 RoundChoiceAbility (`faction_abilities.yaml` entries with `ability_type: round_choice`)

| Field | YAML key |
|---|---|
| id / name_en / name_de | `id` / `name_en` / `name_de` |
| primary / secondary | `primary` / `secondary` (rule-text strings; `secondary` optional — absent for single-effect "Canticle style" entries) |
| primary_effect / secondary_effect | `directives.primary.effect` / `directives.secondary.effect` (dicts, same effect vocabulary as `Ability.effect`) |
| subfaction_affinity | `subfaction_affinity` | optional subfaction id; when the roster's active subfaction matches, **both** directives apply simultaneously instead of one (see `06_domain_rules_and_gotchas.md` §2) |

Top-level `round_choice_label` (e.g. `"Command Protocols"`, `"Ka'tahs of the Broadsword"`) lives
once per file, read via `load_round_choice_label()`.

### 4.6 Stratagem (`_shared/stratagems.yaml` + `<faction>/stratagems.yaml` → `gameObjects.stratagem.Stratagem`)

| Field | YAML key | Convention |
|---|---|---|
| id / name_en | `id` / `name_en` | — |
| cp_cost | `cp_cost` | `int`, `0` = free |
| phase | `phase` | `str` or `list[str]`; `"any"` matches every phase |
| stage | `stage` | `start` \| `active` \| `end` — data schema only, no visibility effect; in-phase timing lives in `rule_text` |
| player | `player` | `active` \| `inactive` \| `both` |
| conditions | `conditions: [KEYWORD, ...]` | keyword list, ANDed against the target unit |
| weapon_conditions | `weapon_conditions: [MELEE\|RANGED]` | matched against a `Weapon`'s profile shape, not the unit |
| once_per_phase | `once_per_phase` | `bool`, default `True` |
| once_per_battle | `once_per_battle` | `bool`, default `False`; overrides `once_per_phase` |
| timing / event | `timing` / `event` | `None` (proactive) \| `phase_reactive` \| `phase_start` \| `phase_end`; `event` e.g. `after_roll`, `on_destroy`, `on_target`, `on_declaration` |
| effect | `effect: {type, target?, amount?, stat?, modifier?, handler?}` | same vocabulary as `Ability.effect` |
| detachment | `detachment` | optional required detachment type id |
| modifier | `modifier: {roll_type, value, target, expires_at?, source_label?, phase?}` | attack-sequence modifier stack entry — **note the `modifier` key is overloaded**, see §8 |
| cp_overrides | `cp_overrides: [{has_keyword, cp_cost}]` | variable CP cost by target keyword, e.g. Curse of the Phaeron: 1 CP normally, 3 CP vs. TITANIC |

### 4.7 DetachmentType (`_shared/detachment_types.yaml`)

| Field | YAML key |
|---|---|
| id / name_en | `id` / `name_en` |
| command_cost / command_benefit | top-level per entry (CP cost to take it / CP awarded) |
| slots | `slots: [{role, min, max}]` — `max: -1` = unlimited |

### 4.8 Relics / Wargear / Warlord Traits / Arkana — raw-dict, not typed catalogs

Unlike units/weapons/abilities, these four files are **not** parsed into their own dataclasses at
catalog-load time — `load_relic_catalog`/`load_wargear_catalog` return `dict[id, raw YAML dict]`.
They only become typed objects lazily, when a roster actually references one:

- A relic with `profiles:` becomes a `Weapon` via `_relic_weapon_from_dict` when applied
  (`_apply_relic`); a relic with `persistent_effects:` (stat buffs, invuln grants, keyword grants)
  is applied directly to the `Unit` dataclass via `_apply_persistent_effect`.
- A relic/wargear item with `ability_en`/`rule_text` but no `effect:` block stays permanently
  raw-dict (display-only) — there is no forced conversion.
- `warlord_traits.yaml` and `arkana.yaml` have **no loader function at all** today.
  `arkana.yaml` carries a comment `"Geladen via load_arkana() (noch nicht implementiert)"` — this
  is accurate: no such function exists in `loader.py`, and no roster field for arkana selection
  is read by `load_roster()` either. Treat both files as reference data pending a loader path,
  not as a currently-wired mechanic.

## 5. Value conventions

### 5.1 Weapon strength grammar — never `int()` a raw strength value

`gameMechanic/attackMath.py:_parse_strength(raw, unit_strength)` is the **only** correct way to
resolve a weapon's strength field:

| YAML value | Meaning |
|---|---|
| `4` (bare int) | fixed strength 4 |
| `"User"` | equals the wielding model's own Strength characteristic |
| `"+N"` / `"User+N"` | unit strength + N |
| `"×N"` / `"User×N"` | unit strength × N |
| `"-N"` / `"User-N"` | unit strength − N (rare) |
| `"*"` | special-mechanic weapon, resolves to `0` — actual value comes from an `effect` handler, not this field |

Calling `int(profile.strength)` directly crashes on every non-numeric value above and is called
out as a recurring bug pattern (`docs/spec/rules_insights.md`, CLAUDE.md domain constraints,
memory `feedback_parse_strength.md`). The rebuild's parser must reproduce this exact grammar,
including the `*` sentinel.

### 5.2 Keyword casing and subfaction placeholders

All `keywords` entries are **UPPERCASE** by convention — this is asserted, not just styled, at
several call sites (`Unit.has_keyword()` upper-cases both sides defensively, but source data is
expected to already be uppercase). Wahapedia-sourced unit keyword lists sometimes carry a
subfaction placeholder token like `<DYNASTY>` or `<CLAN>` — any `<...>` bracketed token, not a
fixed vocabulary. `_resolve_keyword_placeholders()` (`loader.py:384`) replaces it with the
resolved subfaction (upper-cased) if one is known, or **drops** it entirely rather than leaving
a literal placeholder string reaching the UI (CLAUDE.md "No Placeholders — Ever"). Catalog loads
today never pass a subfaction at this call site, so in practice the placeholder is always
dropped at catalog-load time and only re-appears resolved once a roster-bound subfaction flows
through a caller that re-runs this resolution.

### 5.3 Dice notation

Free-form strings, not a constrained enum: seen values include `"1"`, `"D3"`, `"D6"`, `"2D3"`,
`"D3+3"` for `damage`/`attacks`, and `"2D6"` embedded in a `weapon_type` string like `"Heavy 2D6"`
(parsed out by `_attacks_from_weapon_type` when building a relic weapon profile). There is no
shared dice-notation parser exposed from `gameObjects` — dice resolution is UI/mechanic-layer
responsibility (`gameMechanic/unitMutations.py:dice_notation_max` computes only the *maximum*
value of a notation string, for display bounds).

### 5.4 Loud validation on two effect shapes

Two effect types are rejected at load time if incomplete, both intentionally "fail loud beats
fail silent in the UI" design (see §3.2): `wound_auto_fail` (needs a renderable label) and
`explode` (needs `roll_threshold`+`radius`+`damage` together, since it drives a mandatory,
un-skippable "Explodes"-family prompt).

## 6. Roster format

### 6.1 Actual schema (as read by `load_roster()`, `loader.py:1202`)

```yaml
display_name: "Necrons α"        # optional, UI label
faction_dir: "necrons"           # REQUIRED — ValueError if missing, no faction guess
dynasty: nihilakh                # subfaction field name is faction-declared (subfaction_field
                                  # in faction_abilities.yaml, e.g. "dynasty" for Necrons,
                                  # "clan" for Orks) — read generically by load_roster_metadata
units:
  - id: wh40k_9e.necrons.unit.overlord     # REQUIRED, catalog reference
    models: 1                              # optional, defaults to unit.models_max
    wargear: [wh40k_9e.necrons.wargear.resurrection_orb]   # optional, flat list of wargear IDs
    relic: wh40k_9e.necrons.relic.schleier_der_finsternis  # optional, single relic ID
    group_loadouts:                        # optional — only for units with model_groups
      <group_id>:
        swaps:
          <swap_id>:                       # scope: group  → single {weapons: [...]}
            weapons: [wh40k_9e.necrons.weapon.hyperphase_reap_blade]
          # scope: per_model → LIST of {weapons: [...], count: N}
```

This is confirmed against every file actually present in `data/rosters/` (8 files, Necrons and
Orks) — none of them use fields beyond `display_name`, `faction_dir`, the subfaction field,
`units[].{id, models, wargear, relic, group_loadouts}`.

### 6.2 Fields documented in specs but not implemented by the current loader

`docs/spec/loader_contract.md` §2 describes a considerably richer roster schema —
`roster_id`, `game_size`, `battle_forged`, `command_protocols` (explicit round-to-protocol
assignment), `detachments` (with `detachment_type`/named sub-lists), per-unit `warlord`,
`warlord_trait`, `arkana`, and `weapon_loadout` (as distinct from `group_loadouts`). **None of
these keys are read by `load_roster()`** as it exists today — grep of `loader.py` confirms no
`entry.get("warlord")`, `entry.get("arkana")`, or `entry.get("weapon_loadout")` call exists, and
no roster file in the repo sets any of them. `docs/spec/army_builder.md`'s earlier roster
schema (`roster_id`, `points_limit`, `created`, `detachments[].units[].wargear` as slot-tagged
dicts) is likewise design intent, not the shipped format.

**Implication for the rebuild:** treat §6.1 as the contract to reproduce; treat the richer
schema in the two specs as a *backlog of roster features* (warlord designation, per-model
weapon loadout distinct from the group mechanism, explicit command-protocol-to-round
assignment, multi-detachment army composition) that the current app has never actually wired
end-to-end. Warlord/army-composition validation, CP-cost detachment slot-checking, and
points-budget enforcement described in both specs are similarly aspirational — `load_points()`
exists and is called by the setup screen, but no hard budget gate blocks starting a game.

## 7. Faction ability categories — schema pointer

Faction abilities fall into 6 categories distinguished purely by `ability_type` +
structural fields, documented in full in `docs/spec/faction_abilities.md` and with worked YAML
examples in `data/wh40k_9e/_schema/*.example.yaml`. Summary of the schema shape per category
(mechanics/engine detail is in `06_domain_rules_and_gotchas.md` §1):

| Category | `ability_type` | Distinguishing YAML shape |
|---|---|---|
| Round-choice | `round_choice` | `directives.primary/secondary.effect`, optional `subfaction_affinity` |
| One-time/staged | `activated` (+ separate stage entries with `next_stage_id`) | `trigger.phase: command`, `stage_effects` |
| Auto-progression | `auto_progression` | `progression: [{round, effects, round_max?}]`, optionally hybrid with `player_choice: true` + `choice_options` from round N onward |
| Resource-based | *(none implemented)* | not yet used by any faction in the repo |
| Distribution | *(none implemented)* | not yet used by any faction in the repo |
| Passive/persistent | `passive` or plain `triggered` with `trigger.timing: persistent` | no activation UI |

## 8. BattleScribe (.rosz) import (`src/gameObjects/roszImporter.py`)

Implemented and considerably narrower than `docs/spec/army_builder.md`'s description:

1. `parse_rosz_bytes`/`parse_ros_bytes` — unzips (if `.rosz`) and parses the BattleScribe XML
   with `defusedxml`, with explicit size caps (5 MB compressed, 20 MB decompressed) and a
   namespace check (`http://www.battlescribe.net/schema/rosterSchema`).
2. `_detect_faction` — matches `force[@catalogueName]` (lowercased) against a small hardcoded
   `_FACTION_CATALOGUE_MAP` (`necrons`, `adeptus custodes`/`custodes`, `orks`/`ork` → faction
   dir). This is the one place a faction *name string* legitimately lives in `src/` — it maps an
   external vocabulary at the I/O boundary (see §1).
3. `_extract_units` — walks `<selection type="unit">`/`type="model"` elements, counts nested
   `type="model"` sub-selections for quantity, and collects all nested `type="upgrade"` names as
   flat `wargear_names`.
4. `_match_unit_name`/`_build_name_map` — fuzzy-matches BattleScribe display names (and their
   catalog-id slug) against the faction's unit catalog, normalizing to `[a-z0-9]+` joined by
   underscores, stripping a `{faction_dir}_`/`{singular}_` prefix if the raw match fails.
   Same normalize-and-match approach for weapon/wargear names via `_build_weapon_name_map`.
5. `import_roster` writes a YAML with **only** `display_name`, `faction_dir`, and
   `units: [{id, models, wargear?}]` — no relic, no warlord flag, no model-group loadout
   resolution, no points validation. Unmatched unit names are returned as a list, not written
   into the output YAML at all (`docs/spec/army_builder.md`'s `unmatched:` roster section does
   not exist in the actual output).

There is no `tools/import_rosz.py` CLI entry point matching the exact path named in
`docs/spec/army_builder.md`; the importable logic lives in `src/gameObjects/roszImporter.py` as
library functions (`parse_rosz_bytes`, `import_roster`) — whatever CLI/UI wraps them is outside
this module's own responsibility.

## 9. camelCase — the one deliberate naming exception

Every field in this data layer is `snake_case`, with a single documented exception:
`WeaponProfile.grants_keyword` is read from YAML key `grantsKeyword` (21 Necron weapon profiles
in `weapons.yaml` + one relic exception in `relics.yaml`). This was a conscious,
stakeholder-approved break from the otherwise universal snake_case convention (S148 Brief 4,
full rationale and a **complete field-rename mapping table for a possible future camelCase
migration** in `docs/spec/loader_contract.md` §8) — that migration has **not** been executed;
every other field remains snake_case today. The rebuild team should pick one casing convention
up front rather than inherit this partial state, and should not read the mapping table in
§8 of `loader_contract.md` as "already done" — it is a considered proposal, not a changelog.

Two more overload/collision notes from that same section worth carrying forward as gotchas for
schema design (not code — nothing needs fixing today, just awareness):

- `modifier` is overloaded in `stratagems.yaml`: as an int leaf under `effect:` (a plain
  numeric payload) versus as a top-level block (`{roll_type, value, target, expires_at,
  source_label}`, the `StratagemModifier` shape). Same key, two unrelated shapes, disambiguated
  today only by position in the tree.
- `target` is similarly overloaded: `effect.target` (coarse recipient, e.g. `selected_unit`,
  `enemy`) versus `modifier.target` (strictly `attacker`/`defender`, the roll-pipeline role).
