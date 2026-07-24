# Arbiter — Migration Handover (Index)

**Purpose:** Arbiter, a play-companion app for Warhammer 40,000 9th Edition, is
currently built on Streamlit. Streamlit's execution model has reached its limits
(see `07_streamlit_pain_points.md`); the app will be rebuilt on a different,
not-yet-chosen technology. This directory is the **primary input for that
rebuild**, next to the codebase itself: it captures the full picture
(scope, features, design, architecture, data, domain knowledge) in a
framework-agnostic form, so the app can be reconstructed on any stack. For
implementation specifics, the referenced code (`path/file.py:function`) and
specs (`docs/spec/…`) remain available.

**Written:** 2026-07-24, branch `dev`, commit baseline `4a562ef`. Everything
documented here was verified against the code at that state — not against
plans, backlog wishes, or memory.

## Reading order

| File | Answers | Read when |
|---|---|---|
| `01_scope_and_purpose.md` | What is Arbiter, for whom, which game/factions, deliberate non-goals | First — the product frame everything else hangs on |
| `02_working_features.md` | What is **actually implemented** today, per area, with code references and an explicit "not implemented" list | Defining the rebuild's feature parity target |
| `03_design_stack_and_rules.md` | Binding design system (colors, layout invariants, card anatomy, dice display, wording) — separated from Streamlit workarounds | Building the new UI layer |
| `04_architecture_and_app_flow.md` | Layer model, state semantics, app/phase flow, quality gates — split into "must survive" vs. "Streamlit artifact, do not copy" | Designing the new architecture; deciding what to port vs. rewrite |
| `05_data_model.md` | YAML schemas, loader contract as **shipped** (vs. aspirational specs), roster format, value conventions | Writing the new loader — the YAML layer is reused as-is |
| `06_domain_rules_and_gotchas.md` | Non-obvious 9E rule interpretations and hard-won fixes the rebuild would otherwise re-break | Implementing any game mechanic |
| `07_streamlit_pain_points.md` | Why Streamlit is being abandoned: 7 concrete pain points → 6 requirements to evaluate candidate frameworks against | Choosing the next framework |

## The five facts to internalize before writing any code

1. **The app is a referee, not a simulator.** No auto-dice, no board state, no
   spatial reasoning — players roll physically and enter results; the app
   computes thresholds, enforces state machines, and does the bookkeeping
   (`01`, §"What Arbiter is").
2. **Generic engine, data-driven factions.** No faction name or vocabulary may
   appear in engine code; every faction difference is YAML. This is enforced by
   architecture guard tests today and is the property that makes Arbiter a
   generic 9E engine (`04` §1.3 INV-4/4b, `05` §1, `06` §6.4).
3. **The YAML data layer is stable — reuse it as-is.** The rebuild needs a new
   loader that reproduces the documented parsing behavior, not a new schema
   (`05` §1).
4. **Separate domain logic from rendering per phase file.** The current
   `gameMechanic/*Phase.py` files bundle both; the rebuild must split them
   (`04` §1.2). The pure domain modules (`combat.py`, `unitMutations.py`,
   `gameState.py`, `abilityEngine.py`, `stratagemEngine.py`) and their test
   suite port largely as-is once decoupled from `st.session_state`.
5. **Some specs are aspirational, not shipped.** `docs/spec/loader_contract.md`
   and `docs/spec/army_builder.md` describe a richer API/roster schema
   (`Army` dataclass, `warlord`, `arkana`, `weapon_loadout`, detachment
   binding) that was never implemented. The handover documents the shipped
   contract and flags each divergence explicitly (`05` §3, §6.2, §8). Do not
   treat a spec as ground truth without checking the corresponding handover
   section or the code.

## Relationship to the rest of the repo

- `docs/spec/` — canonical working specs (design system, processes, acceptance
  catalog, invariants). The handover **digests and references** them; for full
  detail (e.g. every acceptance rule, every Mermaid phase diagram) follow the
  links in each document.
- `docs/spec/acceptance/rules.md` — the rule-coverage ledger (classes A/B/C).
  Framework-agnostic; carries over into the rebuild as the domain safety net
  (`04` §5.2).
- `tests/gameMechanic/`, `tests/gameObjects/` — the domain regression suite,
  intended to port with the domain modules.
- `data/wh40k_9e/`, `data/rosters/` — the reusable data layer (`05`).

These seven documents are a snapshot. If the Streamlit app continues to evolve
before the migration starts, re-verify `02_working_features.md` against
`git log` since `4a562ef` before treating it as the parity target.
