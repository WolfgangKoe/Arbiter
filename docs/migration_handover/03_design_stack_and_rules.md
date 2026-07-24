# 03 — Design System & Rules (Framework-Agnostic)

> Audience: engineers rebuilding Arbiter on a new UI stack. This document extracts the
> **design system** — the rules that must survive a framework change — from its current
> Streamlit implementation. Where a rule exists only because of Streamlit's rendering
> model, it is explicitly labelled **"Streamlit workaround — do not carry over."**
>
> Canonical specs (do not duplicate, read these for full detail):
> `docs/spec/design_colors.md`, `docs/spec/design_system.md`, `docs/spec/ui_layout.md`,
> `docs/spec/dice_display.md`. This document is the migration-oriented digest of all four,
> plus the concrete implementation techniques found in `src/uiLayout/`.

---

## 1. Binding design rules (carry over as-is)

These are product decisions the stakeholder made explicitly (colors, wording, layout
invariants). They are technology-independent and must be re-implemented identically in
the new stack, not reinterpreted.

### 1.1 Color palette — semantic meaning

Source of truth: `docs/spec/design_colors.md`. Base theme tokens (dark theme only — no
light-mode variant exists today):

| Token | Hex | Meaning |
|---|---|---|
| `--arb-bg` | `#0f0e0c` | page background |
| `--arb-surface` | `#1c1a14` | card/panel surface |
| `--arb-border` | `#2e2618` | borders, dividers |
| `--arb-accent` | `#d4a017` | gold accent — headings, primary actions, "ready"/"used" GO-card border |
| `--arb-accent-lt` | `#fbbf24` | bright gold — number highlights (Attacks, Damage) |
| `--arb-muted` | `#6b5f44` | dimmed text/captions, "dormant"/"locked" GO-card border |
| `--arb-text` | `#e7e5e4` | body text |
| `--arb-red` | `#991b1b` | destructive/negative (also `error` notice type) |
| `--arb-green` | `#166534` | success (notice type) |
| `--arb-blue` | `#1e3a8a` | info (notice type, phase-rule box) |

**Semantic color families** (the meaning is the binding rule, not the hex — hex values
are given for reference):

- **Buff family — green `#4a9a5a`**: any advantage regardless of source (MWBD, cover,
  army-wide abilities such as WAAAGH!/active Command Protocols, reroll markers, "buff"
  `color_hint`). One green for all buffs — the palette deliberately does not distinguish
  buff *sources* by color ("damit die Farben nicht ausgehen" — so colors don't run out
  as more factions are added).
- **Debuff family — red `#ef4444`**: any disadvantage from the acting unit's own
  perspective (auto-fail markers, "debuff" `color_hint`).
- **State badges on a unit** (see §1.3) each own one fixed color — MOVED blue, ADVANCED
  gold, STATIONARY muted-brown, RETREATED/DESTROYED red, IN MELEE orange, CHARGED/FOUGHT
  violet, SHOT/CAST cyan-blue, RESERVE/HEROIC INT. salmon-orange.
- **No faction colors.** Explicitly rejected by the stakeholder (`design_colors.md` §4c)
  — one gold theme for every faction. Faction identity is carried by badge *text*
  (keyword chips), never by a faction-specific hue.
- **No per-effect-category colors beyond buff/debuff.** Relic badges and
  wargear-keyword-blue were tried and explicitly retired — an effect is either a buff, a
  debuff, or a plain (uncolored) keyword chip. Nothing else.

**Notice convention** (`design_system.md` §3) — four types, one rule each:

| Type | Color | When |
|---|---|---|
| `success` | green | action succeeded / expected rule outcome |
| `info` | blue | neutral rule reminder, no win/lose framing |
| `warning` | Streamlit's native amber (no `--arb-warning` token — deliberate) | expected, rules-legal failure (failed test, lost roll) |
| `error` | red | rule violation / data error / failure with extra consequence (Perils, missing config) |

**Wording budget (ratchet, `design_system.md` §3.1):** every notice/warning text is at
most one short imperative or declarative sentence. The *why* (rule justification) never
goes in the UI string — it belongs in the spec (`rules_insights.md` /
`acceptance/rules.md`). The UI says only what the player must do now or what currently
holds, never why.

### 1.2 Layout invariants

Three-column layout, fixed top header (`ui_layout.md` §1):

```
┌──────────────────────────────────────────────────────────────────────────┐
│                              gameHeader (fixed)                          │
├───────────────────────┬───────────────────────────────┬──────────────────┤
│   firstPlayer sidebar │      gameActionsArea (center)  │  secondPlayer    │
│   (armyList)          │      (phase-dependent)         │  sidebar         │
│                       │  ┌─ gameActionDisplayArea ───┐  │  (armyList)      │
│                       │  │ (full width, context)     │  │                  │
│                       │  ├─ firstPlayerArea ┬─────────┤  │                  │
│                       │  │ (50%)            │ 2nd (50%)│  │                  │
│                       │  └──────────────────┴─────────┘  │                  │
│                       │      gameProtocoll (below)     │                  │
└───────────────────────┴───────────────────────────────┴──────────────────┘
```

**Hard invariant — sidebar binding (CLAUDE.md domain constraint, `design_system.md`
§1.9):** the left sidebar is *always* `first_player`, the right sidebar is *always*
`second_player`. Layout must **never** be bound to `active` (whoever's turn it currently
is). This applies transitively to every generic building block: the Pflicht-Trigger
tile family (§1.9), the binary-roll widget, the info notice box all render inside the
controlling player's own half (`firstPlayerArea`/`secondPlayerArea`), never swapped by
turn order. Only the Multi-Unit target-selection panel (§1.7) is a deliberate exception
and spans the full center width, showing both armies side by side.

**Center column render order:** `gameActionDisplayArea` (context: phase rules, attack
summary, modifier chain) renders **above** the two player-interaction halves — the
player reads the situation before acting. Effect-execution UI (Pflicht-Trigger tiles,
GO cards) renders exclusively in the center column, never inside a sidebar — the
sidebars stay purely reactive (HP bars, badges, sort-to-top for the last-touched unit).

**Column semantics:**

- **armyCard** — one per sidebar, faction + subfaction badges, army-wide ability buttons.
- **detachmentCard** — groups units by battlefield role (HQ/Troops/Elites/...), roles
  with 0 units are hidden.
- **unitCard** — one per unit (see §1.3 for anatomy).
- **gameProtocoll** — tabbed panel below the center column: Command Protocol log (event
  log, round/phase filterable, frozen once a turn ends) and Stratagems tab (both
  players' available GOs, filtered by phase/conditions).

### 1.3 unitCard anatomy (the GO-card's sibling component)

```
┌───────────────────────────────────────────────────────┐
│  ❤  ████████████░░░░  8 / 10                          │
│  ⬡  ████████████░░░░  8 / 10                          │
│  ──────────────────────────────────────────────────── │
│  [unitName]  ← clickable → toggles selected state      │
│  ──────────────────────────────────────────────────── │
│  [state1] [state2] ...                                 │
│  [keyword1] [keyword2] [keyword3] ...                  │
└───────────────────────────────────────────────────────┘
```

Rationale (`ui_layout.md` §4): HP/model bars sit *above* the name for an immediate health
read; state badges sit directly *below* the name so they are visually bound to this unit,
not the one above/below it. LP-bar and model-bar stay coupled (summed remaining wounds;
model count decrements at 0 wounds) — no per-model tracking in the sidebar.

**Keyword rule:** the unit's main faction keyword (e.g. "NECRONS") is never shown on the
unitCard — it is shown once, in the armyCard. All other keywords render as chips.
Keyword *highlighting* is all-or-nothing: if a target-selection ability requires keywords
`[A, B]`, either both matching chips light up or none do — never a partial highlight.

**State badges** (fixed vocabulary, one badge per concept, `ui_layout.md` §4 /
`design_colors.md` §2):

| Badge | Color | Meaning |
|---|---|---|
| MOVED | blue | moved normally |
| ADVANCED | gold | advanced (restricted afterwards) |
| STATIONARY | muted brown | did not move |
| RETREATED / DESTROYED | red | negative state |
| IN MELEE | orange | engaged |
| CHARGED / FOUGHT | violet | melee activation |
| SHOT | cyan | ranged activation |
| CAST | blue-family | psychic activation |
| RESERVE / HEROIC INT. | salmon-orange | temporary special state |

Badges are additive: movement-slot badge (FOUGHT > CHARGED > movement type, mutually
exclusive) plus always-additive SHOT/CAST/IN MELEE/RESERVE, plus one buff-green badge
per active buff (label from data, e.g. army-ability name).

**Interaction contract:** exactly one clickable element per card — the unit name. Click
toggles `selected` (own units) or `target` (enemy units, phase-dependent). No wound
buttons live on the card; those render in the center column's player area once a unit is
selected. This "one button, everything else derived from state" rule is what any new
framework's unit-card component must preserve — it is a UX decision, not a Streamlit
limitation.

### 1.4 The GO card — one component, three render sites, five states

`design_system.md` §6 is the single most important component spec for the rebuild: GOs
(Stratagems + comparable optional rules) used to exist in three divergent, hand-rolled
shapes (reactive box, inline offer, tab expander) before S115/S130–S139 unified them into
**one** card, rendered either in full form (central Stratagems list) or compact form
(inline anchor at the trigger site).

```
▸ Fire Overwatch · 1 CP                    [Use]
[CORE] [CHARGE] [reaktiv]
   (▸ expands the rule text — that's its only job)
```

- Header line: name · CP cost · exactly **one** action slot on the right (`Use` or
  `↺ Undo`).
- Keyword chips below (full form only — compact form omits them, it's an inline anchor
  next to a table-roll entry).
- Rule text is accordion-only, and the accordion never auto-collapses (an explicit
  stakeholder complaint fix, S130).
- No "pass" button — declining a GO is simply not pressing `Use`.
- No CP total on the card — that lives only in the header (GameHeader), never repeated.

**Five states, one vocabulary family** (`design_system.md` §6.1, §6.4):

| State | Meaning | Visual |
|---|---|---|
| dormant | trigger not met | dimmed, `Use` disabled |
| ready | trigger met, CP sufficient | gold-accent border, `Use` enabled |
| used-here | pressed at *this* anchor, window still open | `↺ Undo` (full rollback: CP + effect both revert) |
| used-elsewhere | same (player, GO) spent this phase at a *different* anchor | dimmed, disabled `Used` label (no undo — undo only makes sense where the spend happened) |
| locked | CP missing / precondition gone | dimmed, reason suffixed onto header |

**Placement rule (static, not situational — `design_system.md` §6.2):** a GO's
reactive/proactive classification is a YAML property, never a runtime toggle.
`timing: phase_reactive` GOs render **only** inline at their trigger site, never in the
central list. Everything else renders **only** in the central Stratagems list, never
inline. This binary rule (one GO, one canonical render site per its class) is a design
invariant worth preserving regardless of framework — it prevents the "does this button
exist in two places with two different states" bug class entirely.

**Action vocabulary — one family, not four (`design_system.md` §6.4):** `Use` ·
`↺ Undo` · disabled `Used` · `Confirm ⟨Action⟩` / `Cancel` · toggle-selection with a
`✓` prefix. No "Reset", "Undo deny", or ad-hoc synonyms. CP cost is stated once, in the
card header, never repeated on the button.

### 1.5 Generic building-block family (Pflicht-Trigger tiles)

`design_system.md` §1.5–§1.9 defines a small vocabulary of **mandatory-event** UI blocks
(distinct from GO cards, which are always a player's voluntary Use/Undo decision):

- **§1.5 Pflicht-Trigger tile** — same shell as a GO card (bordered container,
  header + rule caption + divider) but **no** action slot, no CP suffix — for automatic
  events (e.g. a destroyed unit's "Explodes" ability).
- **§1.6 Binary-roll widget** — two buttons (success label / failure label) instead of a
  number field, for table rolls where only pass/fail matters to the app, not the exact
  value. Two states: "open" (both buttons) → "decided" (single `↺ Reset` button, which
  reopens "open").
- **§1.7 Multi-unit target-selection panel** — both armies side by side, toggle rows +
  a fixed-width value column; the panel is the sole exception to the sidebar-binding
  invariant (spans full center width). The **last-touched unit sorts to the top** of its
  sidebar for visibility while the panel is open.
- **§1.8 Info notice box** — reuse of the `info` notice type (§1.1) for a mandatory
  event's single-sentence outcome ("X explodes." / "X does not explode."). Exactly one
  box active at a time, never both outcomes shown together.
- **§1.9 Layout invariant** — all of the above render exclusively in the center column
  (never a sidebar); §1.9.1 further restricts tiles ①/③ to the *controlling player's*
  half of the center column, not the full width — again bound to `first_player`/
  `second_player`, never `active`.

### 1.6 Dice display design (`docs/spec/dice_display.md`)

The dice-roll visualization is a fixed geometric grid, independent of any specific
framework's rendering primitives:

- **Row structure**: `[BADGE 96px] [Slot 34px]×6 [threshold separator]` — a modifier
  label badge, six die-face slots (32px SVG + 2px margin each), and a `|` separator
  marking the pass/fail boundary at the current threshold.
- **Invariant: slot 1 always shows a miss (✕).** An unmodified roll of 1 always fails —
  no buff stack may turn slot 1 into a success pip. This is a rules invariant
  (`core_rules.txt` "Hit/Wound/Save Roll"), not a display preference — any reimplementation
  must floor the effective threshold display at 2+ the same way `resolve_save()` floors
  the computed value.
  - This is a **hard modeling requirement for the new framework's dice component**, not
  just a CSS detail: whatever draws the die-face grid must special-case slot 1 as an
  always-miss face regardless of computed threshold.
- **Direction convention**: buff arrows point right (`[+N→]`, green), debuff arrows
  point left (`[←N]`, red) — the effective threshold visually shifts in the direction of
  player benefit.
- **Marker families** (below/alongside the base row, not replacing it): reroll (`↺`,
  buff-green, positioned under the affected slot), always-fail (`✕` under each affected
  slot, perspective-colored — buff-green for the defender's benefit, debuff-red for the
  attacker's own risk), value-triggered effects (`AP-N`/`+N` chip in a specific column,
  e.g. "on an unmodified 6").
- **Two symbol families**: real die-face SVGs (32×32, rounded rect, 1.5px border) for
  anything that *is* a die result (success pip, miss cross, reroll glyph), versus text
  chips (30×30 box, `border-radius:4px`) for effects that are not literal die faces
  (AP-modifier trigger, extra-hits count). New framework: keep this distinction — it is
  what lets a player visually parse "this is a real roll outcome" vs. "this is a rule
  annotation" at a glance.
- **Wurf-Block-Pattern (`design_system.md` §4.4)** — the canonical anatomy of any dice
  block: title + comparison value → threshold header + base dice row → marker rows
  (auto-fail/reroll/value-trigger) → modifier rows (each a compare-pair + effective row) →
  final effective row → optional source chips (which GO/ability granted a buff/debuff).
  Every current and future roll type (Hit/Wound/Save/Damage, table rolls) follows this
  same skeleton — worth keeping as a named pattern in the new framework's component
  library rather than re-deriving it per screen.

### 1.7 Wording conventions

- **UI language is English throughout** (design decision, independent of the
  German-language dev workflow — `design_system.md` §6.4). A few legacy modules
  (`moralePhase.py`, parts of the subgroup selector) still have residual German strings;
  these are documented debt, not the target state.
- One action vocabulary family (§1.4 above) for every interactive affordance in the app,
  not per-screen synonyms.
- Wording budget: one sentence per notice (§1.1).
- Sub-header pattern for multi-step forms: a dim, non-bold caption ("Enter damage
  taken") sits between a structural divider and the actual input fields, making a
  shared frame visible across otherwise different input paths (`design_system.md`
  §1.4.1) — a wording+layout micro-pattern worth keeping as a generic form convention.

### 1.8 Geometry tokens (component sizing, framework-agnostic)

`design_system.md` §2, sourced from `src/uiLayout/badges.py`:

| Token | badge | chip |
|---|---|---|
| border-radius | 2px | 2px |
| padding | 1px 6px | 1px 5px |
| font-size | 10px | 9px |
| font-weight | 600 | 400 |
| letter-spacing | 0.06em | 0.05em |

A `badge` uses its foreground color doubly as its border color (an outlined pill). A
`chip` allows a border color independent of its foreground (used for a dimmed
keyword-chip look). These two are the *only* two badge/chip geometry classes in the
whole app — a third divergent shape is a bug, not a variant, per the design system's own
ratchet rule.

---

## 2. Current CSS/HTML implementation techniques worth knowing (context, not to blindly port)

These describe *how* the design system above is realized today, in case they inform
component-library decisions for the new stack (e.g. "we need first-class badge/chip
primitives" or "we need an SVG die-face component with parametrized color/value").

- **Pure HTML string composition, no Streamlit dependency.** `src/uiLayout/badges.py`,
  `src/uiLayout/goCard.py`, `src/uiLayout/diceCompose.py` are plain Python functions that
  return HTML strings — no `import streamlit`, unit-tested and coverage-measured like any
  other business logic (architecture invariant INV-6). The Streamlit wrapper
  (`uiLayout/_common.py`) is a thin layer that calls these builders and passes the
  result to `st.markdown(..., unsafe_allow_html=True)`. This separation (pure
  HTML-composition layer vs. thin framework-glue layer) is the one implementation
  pattern worth deliberately carrying into the new stack's architecture, independent of
  which framework is chosen — it is what makes the design system's building blocks
  testable without a browser.
- **One badge/chip builder, colors supplied at the call site.** `badges.py` owns
  geometry centrally; `fg`/`bg` hex values are passed in by each caller from the
  semantic tables in `design_colors.md`. Avoids the pre-S115 drift where four call
  sites had each hand-rolled a slightly different `<span>`.
- **Die faces are hand-built SVG**, not an icon font or external library:
  `dice_face_svg(value, color, miss, size)` — 32×32 viewBox, rounded rect, pips as
  `<circle r="2">` at fixed positions, a miss face swaps pips for a diagonal-cross
  `<line>` pair. Fully parametrized by color and value, single source for every die-face
  variant (success, miss, off-scale-miss, reroll, all interpreted through one function).
- **CSS custom properties (`--arb-*`) defined once**, in `gameHeader.py`'s `CSS_THEME`
  string, injected via `st.markdown` at app start. Everything downstream references the
  variables, not literal hex — except the pure-HTML composition layer (badges/goCard/
  diceCompose), which mirrors the hex values as Python constants because those functions
  run outside the page's injected `<style>` scope and cannot reach CSS custom properties
  from a plain returned string. Any reimplementation in a component-based framework
  should be able to eliminate this literal-mirroring entirely (real component
  props/theme context instead of two hardcoded copies of the same hex).

---

## 3. Streamlit workarounds — do NOT carry over

These exist purely to compensate for something Streamlit's rendering/session model does
not natively support. In a new framework with real component state and stable DOM
identity, none of the following should be reproduced — they are symptoms, not design
intent. (Full pain-point analysis: `docs/migration_handover/07_streamlit_pain_points.md`.)

- **`overflow-anchor: none` on `section[data-testid="stMain"]`** — a global CSS override
  to defeat Chrome's scroll-anchoring heuristic, needed only because Streamlit's
  full-script rerun causes layout shifts above the visible viewport (`CLAUDE.md`
  "Streamlit CSS", B1/S136). A framework with fine-grained, localized DOM updates would
  not shift unrelated layout on unrelated state changes, so this hack becomes moot.
- **Scoped `<style>` blocks targeting `st-key-<sanitized-key>` classes** to color one
  specific `st.container(border=True, key=...)`'s border per GO-card state
  (`uiLayout/goCard.py::go_card_container_style`). This works only by replicating
  Streamlit 1.57's own internal key-sanitization regex in Python and hoping it never
  changes between Streamlit versions — a real component framework would expose a
  `border-color` prop or CSS class directly, no reverse-engineered selector needed.
- **Mirrored hex constants in the pure-HTML layer** (`goCard.py`'s `_ACCENT`/`_MUTED`/
  `_SURFACE` etc., `unitCard.py`/`_common.py`'s duplicated `_BADGE_COLORS` tables)
  because CSS custom properties defined in the page's injected `<style>` are not
  reachable from an HTML string built in Python outside that scope. A framework with a
  real theme/token system (CSS-in-JS, design tokens, CSS variables scoped to component
  trees) removes the need for two hand-synced copies of the same color table — worth
  actively flagging as tech debt during the port, not preserving.
- **Widget-key-based state smuggling** (e.g. `value=` seeded manually from a side dict
  because "Streamlit drops a widget's key-state once it unmounts", B-125 comment in
  `_common.py::_render_explode_target_panel`) — a workaround for Streamlit's
  re-mount-on-rerun widget lifecycle, not a UI design decision. A framework with
  persistent component instances would not need this.
- **`st.rerun()` calls to force a second full-script pass** so that a mutation applied
  in one column becomes visible in a sibling column rendered earlier in the same script
  run (B-134) — purely a consequence of Streamlit's linear top-to-bottom single-pass
  render plus its callback-timing quirk (mutations must happen in `on_click`/`on_change`
  to run *before* the script body, not inline). See 07 for the full analysis; a
  framework with reactive/fine-grained updates does not have an "earlier column renders
  stale data" class of bug in the first place.
- **`st.container(border=True)`'s one single fixed border color**, worked around via the
  scoped-`<style>`-per-key trick above, rather than a component that accepts a color
  prop directly.
