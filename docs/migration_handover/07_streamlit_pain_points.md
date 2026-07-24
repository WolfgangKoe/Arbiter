# 07 — Streamlit Pain Points (Why We're Leaving)

> Audience: whoever evaluates candidate frameworks for the rebuild. Each pain point below
> states the **symptom** observed in this codebase, its **root cause** in Streamlit's
> execution model, **how it was worked around** here (with file/function references),
> and the **requirement it implies** for the next framework. Bug IDs refer to
> `docs/goals/backlog.md` / `docs/goals/backlog_archive.md`.

---

## 1. Full-script rerun causes cross-column staleness (B-134)

**Symptom:** After a damage-adjustment button click, the left army-list sidebar showed
the *pre-mutation* unit HP (e.g. "3/3") while the center DAMAGE panel already displayed
the post-mutation consequence ("1 LP left") for the next unit — a one-interaction-late,
board-side-asymmetric inconsistency. Confirmed via screenshot evidence
(`docs/handoff/Bildschirmfoto vom 2026-07-23 23-44-40.png`) during S183.

**Root cause:** Streamlit re-executes the *entire* Python script top-to-bottom on every
interaction. `src/app.py` renders `render_army_list(first_player)` **before** the center
`gameActionsArea` block, and `render_army_list(second_player)` **after** it
(`src/app.py:44-54`). When a damage mutation (`apply_damage(...)`) ran inline inside a
button's `if st.button(...):` body — i.e., mid-script, in the center block — the left
sidebar had already rendered *before* that mutation happened in the *same* script pass;
only the right sidebar (rendered after) picked up the fresh state. The `st.rerun()` that
followed synced things up, but one interaction late, producing the visible flicker/lag
and the board-side asymmetry. Confirmed *not* a fragment-isolation bug
(`grep -rn st.fragment src/` → 0 hits) — a pure consequence of linear single-pass
rendering plus inline mutation.

**Workaround in this codebase:** Move every mutation into the widget's `on_click`/
`on_change` callback, which Streamlit runs **before** the script body on the next run —
so both sidebars observe the same post-mutation state in one pass, and the trailing
`st.rerun()` becomes unnecessary (removed as part of the fix). Concretely (S183,
`4a562ef`): `uiLayout/_common.py::_wound_adjustment_click`,
`_explode_toggle_click`, `_explode_direct_apply_change` — three call sites, each
converted from "compute inline, then `st.rerun()`" to "mutate in the callback, let the
natural rerun after the callback pick it up." Playwright-verified same-frame update
(no visible staleness).

**Implication for the next framework:** state mutations must be visible to **every**
consumer in the same reactive tick regardless of DOM/render order — i.e., genuine
fine-grained reactivity (signals/observables/a virtual-DOM diffing model that re-renders
dependents, not a fixed linear top-to-bottom script). A framework where component A's
render order relative to component B can leak stale state, purely because of source
order, reproduces this exact bug class. This was treated as a "Fachlichkeit" bug
(gameplay-correctness impacting), not cosmetic — worth weighing heavily.

---

## 2. Performance cost of full rerun on rapid interaction (B-135, deferred to S184)

**Symptom (hypothesis, not yet measured — S183 Planning §0 Befund 2):** rapid clicks on
a damage `number_input`'s step arrows (`ml_`/`gwd_`/`wf_`-prefixed widgets,
`_common.py`) feel sluggish. Each click is hypothesized to trigger a full
app rerun — both complete army-list sidebars, the entire actions area, and the protocol
panel all re-render, even though only one unit's HP number actually changed.

**Root cause (hypothesis):** same linear full-script re-execution model as Pain Point 1,
compounded by an additional suspected issue: `abilityEngine.py`'s
`get_wound_reroll_aura_donor_names` / `get_unit_rp_reroll_ability` call an **uncached**
`load_army` directly in the render hot path (B-132, flagged S180-Review Minor 2) — i.e.
a YAML-backed loader call potentially re-executed on every widget interaction, not just
once per session.

**Planned measurement/fix (not yet executed, backlog B-135/B-132):** T4a measures
per-click rerun cost via Playwright timing and counts `load_army` invocations in the hot
path; T4b applies `functools.lru_cache`/`st.cache_data` at the loader entry point if the
measurement confirms it's worth it, closing both B-135 and B-132 together.

**Implication for the next framework:** the *architectural* fix here is orthogonal to
Streamlit and would recur on any framework unless component-level re-render scope is
narrow by default — i.e., a single number field's change should re-render that field
(and its direct dependents) only, not two entire sidebars. Additionally: **any**
data-loading call reachable from a render path needs a caching story the framework
either provides natively (memoized selectors, request-scoped caches) or that the app
must build explicitly — this is a lesson to carry regardless of the chosen stack, but
Streamlit's full-rerun model makes an uncached loader call in a render path far more
expensive than it would be in a framework that only re-renders the changed subtree.

---

## 3. Scroll-position fights: layout shift + browser scroll-anchoring (B1/S136)

**Symptom:** Selecting a Command Protocol option during Setup caused the page to jump
scroll position abruptly (~2348px delta measured via Playwright).

**Root cause:** Two hypotheses were tested and **both refuted** via a Playwright probe
(`docs/handoff/S136_B1_probe.md`): H1 (focus-driven autoscroll) — refuted,
`document.activeElement` was `<body>`, not an input; H2 (a sixfold widget-key rewrite
forcing remounts) — also refuted. The actual cause: a full-script rerun changes layout
*above* the currently visible viewport (widgets appearing/disappearing higher up the
page as conditional branches change), and Chrome's native scroll-anchoring heuristic
(which tries to preserve the user's visual anchor point across layout shifts) then
"corrects" the scroll position based on a DOM node that shifted — the correction itself
is the visible jump. This is a direct consequence of full-page-rerun-induced layout
churn combined with a fixed-position, independently-scrolling column layout
(`ui_layout.md` §1: each of the three columns scrolls independently).

**Workaround in this codebase:** `overflow-anchor: none` set on
`section[data-testid="stMain"]` (`src/uiLayout/gameHeader.py`'s `CSS_THEME` block) —
Playwright-verified scroll delta 0/0/0 after the fix (down from +2348). Documented as a
known Streamlit CSS selector in `CLAUDE.md` "Streamlit CSS — Bekannte Selektoren".

**Implication for the next framework:** avoid layout shifts *above* the visible
viewport as a side effect of unrelated state changes in the first place — this requires
either (a) genuinely localized DOM updates (so a change in the center panel cannot shift
content in a sidebar column above the fold) or (b) stable DOM node identity so the
browser's own scroll-anchoring has nothing to "correct." Disabling scroll-anchoring
globally is a blunt workaround for a problem that a framework with stable, minimal DOM
diffs should not create in the first place — do not carry the workaround itself over;
verify the new framework doesn't reproduce the underlying layout churn.

---

## 4. Injected CSS against minified/internal class names, not first-class styling

**Symptom:** Styling any non-trivial Streamlit component (a bordered container, a
number-input's step buttons, a selectbox) requires reverse-engineering which
`data-testid` or auto-generated Emotion class Streamlit's compiled JS bundle currently
uses — these are internal implementation details, not a public API, and have changed
across Streamlit versions.

**Root cause:** Streamlit does not expose a first-class theming/component-props API
comparable to a component-based framework's props/CSS-modules/styled-components. All
visual customization beyond the built-in theme config happens via global `<style>`
injection targeting selectors discovered by grepping the installed package's minified JS.

**Workaround in this codebase:** `CLAUDE.md`'s "Streamlit CSS — Bekannte Selektoren"
table is maintained as living documentation of which selector currently works for which
component (NumberInput container/step-buttons, buttons by `kind`, bordered-container
Emotion class, selectbox inner div) — with an explicit warning to re-verify against the
installed Streamlit version's JS bundle before writing new CSS overrides:

```
find .venv -name "*.js" | xargs grep -l "<ComponentName>" | head -3
# then search the minified JS for the data-testid
```

The GO card's per-state border color goes further: `uiLayout/goCard.py`'s
`_sanitize_key()` function **literally reimplements Streamlit 1.57's own internal key
sanitization regex** (`"st-key-" + e.trim().replace(/[^a-zA-Z0-9_-]/g, "-")`, reverse
engineered from the built JS bundle — see the module docstring) purely so a scoped
`<style>` rule can target the exact class Streamlit stamps on one specific keyed
container. This is fragile by construction: it silently breaks if a Streamlit upgrade
changes the sanitization algorithm, and there is no compile-time or test-time signal
that would catch such a change short of a visual regression.

**Implication for the next framework:** need first-class support for styling individual
component instances (scoped CSS modules, styled-components, Tailwind + component
variants, or equivalent) — i.e. a `style`/`className`/`color` **prop** on components,
not a global stylesheet racing against a minified, versioned internal class name. This
single pain point is probably the strongest concrete argument against staying anywhere
near Streamlit's customization model.

---

## 5. No first-class component/border/state styling primitive

**Symptom:** `st.container(border=True)` provides exactly one theme-fixed border color.
The GO card needs five visually distinct states (dormant/ready/used/used-elsewhere/
locked, `design_system.md` §6.1) with two different border treatments (gold-accent vs.
dimmed).

**Root cause:** Streamlit's container primitive has no `border_color` parameter (as of
the version in use) — border styling is theme-global, not per-instance.

**Workaround in this codebase:** `uiLayout/goCard.py::go_card_container_style()`
generates a scoped `<style>` block per render, keyed to the container's sanitized key
class (see Pain Point 4) with `!important` overrides for `border-color`, `opacity`, and
`background`. This is emitted fresh on every render of every card instance — i.e., a
`<style>` tag per GO card, per rerun, rather than a component prop.

**Implication for the next framework:** components that need visual state (borders,
backgrounds, emphasis) should accept that as a typed prop/variant directly, resolved by
the framework's normal styling mechanism — no runtime-generated, key-matched CSS
injection required.

---

## 6. Widget lifecycle drops state across conditional remounts (B-125)

**Symptom:** A `number_input` inside the Multi-Unit target-selection panel
(`_common.py::_render_explode_target_panel`) reset to 0 on reopen after the panel had
previously been closed ("Confirm all") and was later reopened for correction — even
though the underlying data (`entry["damage"]`) still held the previously entered value.
The naive `on_change` handler then read the reset-to-0 widget value and re-applied a
damage of 0, silently nulling a previously correct assignment (B-125).

**Root cause:** Streamlit widgets are keyed by a `key=` string, and their internal state
is tied to that key's presence in `st.session_state` across reruns. When a conditional
branch stops rendering a widget (e.g. the panel closes), Streamlit drops that widget's
key-state; when the branch renders again (panel reopens) with the *same* key, the widget
starts fresh at its `value=` default rather than resuming where it left off — there is
no persistent component instance to resume, only a key lookup that may or may not still
be populated depending on unrelated conditional rendering elsewhere in the script.

**Workaround in this codebase:** explicitly seed `value=` from a side-channel dict
(`entry["damage"].get(target_key, 0)`) on every render, rather than relying on
Streamlit's own widget-state persistence — effectively re-implementing state persistence
manually outside the framework's own mechanism, with a code comment warning future
readers why (`_common.py` around the `number_input` call, B-125 reference).

**Implication for the next framework:** component instances tied to conditionally
rendered UI need persistent, addressable state that survives unmount/remount (or at
minimum, the framework's own state model must make "this instance's state was reset by
an unrelated conditional branch elsewhere in the tree" structurally impossible, not
something the app has to manually guard against with a side-channel dict per widget).

---

## 7. Coupling: render-order timing determines correctness, not just data flow

**Symptom (systemic, underlies Pain Points 1 and 6):** Correctness in the current
codebase repeatedly depends on *when in the script's linear execution* something
happens — "runs before the script body" (callbacks) vs. "runs inline" (component
lifecycle) vs. "renders before" vs. "renders after" (column order in `app.py`). Several
non-trivial bugs (B-134, B-125, B-126) trace back to a developer's mental model of
"the mutation happens, then everything reflects it" being wrong in subtle,
timing-dependent ways specific to Streamlit's execution contract.

**Root cause:** Streamlit's programming model is "linear imperative script, re-executed
top to bottom on every interaction, with a narrow callback exception (`on_click`/
`on_change` run once, before the next script pass)." This is a fundamentally different
mental model from declarative reactive UI (where a state change propagates to exactly
the components that depend on it, in dependency order, regardless of where they appear
in source/DOM order) — and the difference is easy to get subtly wrong, as this
codebase's bug history shows.

**Workaround in this codebase:** careful, documented convention — "mutation belongs in
an `on_click`/`on_change` callback, never inline in the render body" — enforced by
review and by comments referencing the precedent bugs (B-134's docstring on
`_wound_adjustment_click` explicitly explains the timing reasoning for future
maintainers), not by anything the framework itself enforces or makes impossible to get
wrong.

**Implication for the next framework:** prefer a model where **state mutation and its
propagation to all dependent views is a single, framework-guaranteed operation** — no
convention to remember, no docstring warning required, no possibility of "renders before
the mutation is visible" existing as a category. This is the most fundamental reason for
leaving Streamlit: multiple distinct bugs in this codebase's history (B-134, B-125,
B-126, the B1 scroll-anchoring jump) are all downstream of the same single root cause —
a linear full-rerun execution model without fine-grained reactivity — rather than being
unrelated one-off mistakes.

---

## Summary — requirements for the next framework

1. **Fine-grained reactive updates**, not full-page rerun: a state change must propagate
   only to its actual dependents, in the same tick, regardless of source-order or
   render-order elsewhere in the tree (fixes Pain Points 1, 2, 7).
2. **Stable DOM / no scroll-anchoring fights**: localized updates must not shift layout
   above the visible viewport as a side effect of unrelated state changes (fixes Pain
   Point 3).
3. **First-class component styling** (props/variants/scoped CSS), not global `<style>`
   injection racing against internal, versioned, potentially-minified class names (fixes
   Pain Points 4, 5).
4. **Persistent component/widget state** across conditional mount/unmount, without the
   app having to manually shadow state in a side dict (fixes Pain Point 6).
5. **Predictable, framework-enforced consistency** between state mutation and every
   view that depends on it — ideally structurally impossible to get "stale render before
   mutation" wrong, rather than relying on a documented convention (fixes Pain Point 7,
   the umbrella cause of 1 and 6).
6. **Cheap re-render at scale**: with two full army lists, a center action area, and a
   protocol log all potentially re-rendering on every micro-interaction, the new
   framework's baseline re-render cost for "one number changed" must be low — needed
   regardless of the caching fix planned for B-132/B-135.
