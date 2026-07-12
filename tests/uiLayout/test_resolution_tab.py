"""Bug 1 characterisation: D2 Fall-Back −1 Hit debuff renders in red (#ef4444).

Tests the HTML-output path from _render_dice_roll_block through modifier_die_pair_html
to verify that a shoot_after_fall_back modifier (value=-1) produces #ef4444 in the
generated HTML — the same red path already used by Dense Cover −1.

This is an HTML-output test per the Test Mandate: Render-Code (diceHtml.py) is excluded
from coverage measurement but must still be tested via HTML output.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.modules.setdefault("streamlit", MagicMock())
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout.diceHtml import _render_dice_roll_block, _render_dice_wound_block  # noqa: E402

_DEBUFF_RED = "#ef4444"


def _collect_markdown(monkeypatch) -> list[str]:  # type: ignore[no-untyped-def]
    """Capture all HTML strings passed to st.markdown during the test."""
    import uiLayout.diceHtml as dice_html_mod  # noqa: PLC0415

    captured: list[str] = []

    def fake_markdown(html: str, **_kwargs: object) -> None:
        captured.append(html)

    monkeypatch.setattr(dice_html_mod.st, "markdown", fake_markdown)
    return captured


# ---------------------------------------------------------------------------
# Bug 1 — characterisation: Fall-Back −1 modifier renders red in HIT block
# ---------------------------------------------------------------------------


def test_fall_back_hit_modifier_renders_red_in_hit_block(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """D2 Conquering Tyrant shoot_after_fall_back: −1 Hit modifier must render #ef4444.

    The modifier is already assembled as a dict in _render_resolution_tab and passed
    as part of the hit-stack to resolve_attack_modifiers, which returns it in
    hit["stack"]. This test feeds that stack directly to _render_dice_roll_block
    and verifies the red debuff colour appears in the HTML output.

    Without the debuff entry in the stack: no #ef4444 → test would be RED.
    With the debuff entry (value=-1, roll_type='hit'): #ef4444 → GREEN.
    """
    captured = _collect_markdown(monkeypatch)

    fall_back_modifier = {
        "label": "CT (Fall Back)",
        "value": -1,
        "roll_type": "hit",
        "source": "round_choice",
    }
    hit_block = {
        "base": 4,
        "stack": [fall_back_modifier],
        "modified": 5,
    }

    _render_dice_roll_block("HIT", "BS", hit_block, weapon_special=None)

    combined_html = "\n".join(captured)
    assert _DEBUFF_RED in combined_html, (
        f"Expected #ef4444 (debuff red) in HIT block HTML when fall_back_hit_mod=-1, "
        f"but got:\n{combined_html}"
    )


def test_stacked_hit_debuffs_both_reference_base_threshold(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Regression: two stacked −1 Hit debuffs must BOTH reference the profile threshold (base),
    not each other (chained). base=3, two debuffs (e.g. Conquering Tyrant + Dense Cover).

    Expected: BOTH modifier die-pairs show the red die at value 3 (the profile threshold).
    Without the fix (chained): modifier_die_pair_html gets called as (3,4,...) then (4,5,...).
    The second call's red 'from' die would be at value 4, not 3.

    The signal used: for a −1 penalty, modifier_die_pair_html(from_thresh, ...) renders a
    colored die at from_thresh (right_val = from_clamped). So with fix: dice_face_svg(3, color=
    "#ef4444") appears TWICE in the stacked HTML. With the old chained code: the second call
    would produce dice_face_svg(4, color="#ef4444") instead — so the 3-die appears only once.

    Why the test would be RED without the fix: chained rendering passes from_thresh=4 to the
    second modifier_die_pair_html call, producing a red-4 die instead of red-3. The count
    of red-3 die SVGs would be 1, not 2 — failing the >= 2 assertion.
    """
    captured = _collect_markdown(monkeypatch)

    debuff_a = {
        "label": "CT (Fall Back)",
        "value": -1,
        "roll_type": "hit",
        "source": "round_choice",
    }
    debuff_b = {
        "label": "Dense Cover",
        "value": -1,
        "roll_type": "hit",
        "source": "global",
    }
    hit_block = {
        "base": 3,
        "stack": [debuff_a, debuff_b],
        "modified": 4,  # 9E ±1 cap: net = -2, capped to -1 → effective 4+
    }

    _render_dice_roll_block("HIT", "BS", hit_block, weapon_special=None)

    combined_html = "\n".join(captured)

    # For a −1 penalty with from_thresh=3: modifier_die_pair_html renders the colored
    # (red) die at from_clamped=3. The SVG for a red die-3 contains exactly 3 pips at
    # specific positions and uses fill="#ef4444". We use dice_face_svg as the source of
    # truth — its output is deterministic for a given (value, color) pair.
    from uiLayout.diceCompose import dice_face_svg  # noqa: PLC0415

    red_die_3 = dice_face_svg(3, color=_DEBUFF_RED)
    count_red_3 = combined_html.count(red_die_3)
    assert count_red_3 >= 2, (
        f"Expected red die-3 (from_thresh=3) to appear at least twice — "
        f"once per stacked debuff anchored to base=3. "
        f"Got {count_red_3} occurrence(s). "
        f"Chained rendering would use from_thresh=4 for the second debuff, "
        f"producing a red die-4 instead of red die-3.\n"
        f"Combined HTML snippet:\n{combined_html[:800]}"
    )

    # Sanity: effective row shows 9E-capped result
    assert (
        "Eff. 4+" in combined_html
    ), f"Expected 'Eff. 4+' in combined HTML, got:\n{combined_html[:400]}"


def test_stacked_wound_debuffs_both_reference_base_threshold(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Regression: two stacked −1 Wound debuffs must BOTH reference the base threshold,
    not each other (chained). base=4 (S4 vs T4), two debuffs.

    Expected: BOTH modifier die-pairs show the red die at value 4 (the base threshold).
    Without the fix (chained): modifier_die_pair_html gets called as (4,5,...) then (5,6,...).
    The second call's red 'from' die would be at value 5, not 4.

    The signal used: for a −1 penalty with base=4, modifier_die_pair_html renders the
    colored (red) die at from_thresh=4. So with fix: dice_face_svg(4, color="#ef4444")
    appears TWICE. With the old chained code: the second call passes from_thresh=5,
    producing a red die-5 instead — so red-4 appears only once.
    """
    captured = _collect_markdown(monkeypatch)

    debuff_a = {"label": "Modifier A", "value": -1, "roll_type": "wound", "source": "global"}
    debuff_b = {"label": "Modifier B", "value": -1, "roll_type": "wound", "source": "global"}

    # S4 vs T4 → wound_threshold = 4; two −1 wound debuffs stacked
    _render_dice_wound_block(
        strength=4,
        toughness=4,
        wound_stack=[debuff_a, debuff_b],
        strength_buff=0,
        on_six_ap=0,
    )

    combined_html = "\n".join(captured)

    from uiLayout.diceCompose import dice_face_svg  # noqa: PLC0415

    red_die_4 = dice_face_svg(4, color=_DEBUFF_RED)
    count_red_4 = combined_html.count(red_die_4)
    assert count_red_4 >= 2, (
        f"Expected red die-4 (from_thresh=4) to appear at least twice — "
        f"once per stacked wound debuff anchored to base=4. "
        f"Got {count_red_4} occurrence(s). "
        f"Chained rendering would use from_thresh=5 for the second debuff, "
        f"producing a red die-5 instead of red die-4.\n"
        f"Combined HTML snippet:\n{combined_html[:800]}"
    )

    # Sanity: effective row shows 9E-capped result (net=-2 capped to -1 → eff 5+)
    assert (
        "Eff. 5+" in combined_html
    ), f"Expected 'Eff. 5+' in combined HTML, got:\n{combined_html[:400]}"


def test_no_fall_back_modifier_no_red_in_hit_block(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Control: without a fall_back modifier in the stack, no debuff-red in the HIT block.

    Verifies that #ef4444 is NOT produced when movement_choice != 'retreated'
    (i.e. when the modifier is absent from the stack).
    """
    captured = _collect_markdown(monkeypatch)

    hit_block = {
        "base": 4,
        "stack": [],  # no fall_back modifier
        "modified": 4,
    }

    _render_dice_roll_block("HIT", "BS", hit_block, weapon_special=None)

    combined_html = "\n".join(captured)
    assert _DEBUFF_RED not in combined_html, (
        f"Expected no #ef4444 in HIT block without fall_back modifier, "
        f"but found it in:\n{combined_html}"
    )


# ---------------------------------------------------------------------------
# S122 F1 fix — display path: stratagem_strength_bonus scoping must reach the
# rendered WOUND block. A Strength stratagem (e.g. Disruption Fields) activated
# for one unit must not highlight the S value for a different attacker.
# ---------------------------------------------------------------------------


def test_strength_stratagem_scoped_to_activating_unit_shows_buff_border(
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    """The attacker the stratagem was activated for sees the green buff border on S."""
    from gameMechanic.stratagemEngine import stratagem_strength_bonus  # noqa: PLC0415
    from uiLayout.diceCompose import _BUFF_COLOR_HEX  # noqa: PLC0415

    active_modifiers = [
        {
            "unit_key": "wh40k_9e.necrons.unit.warriors",
            "source": "Disruption Fields",
            "effect": {"roll_type": "strength", "value": 1, "target": "attacker", "phase": "fight"},
            "expires_at_phase": "fight",
            "expires_at_round": None,
        }
    ]
    str_bonus = stratagem_strength_bonus(active_modifiers, "wh40k_9e.necrons.unit.warriors")
    assert str_bonus == 1

    captured = _collect_markdown(monkeypatch)
    _render_dice_wound_block(
        strength=4 + str_bonus,
        toughness=4,
        wound_stack=[],
        strength_buff=str_bonus,
        on_six_ap=0,
    )
    combined_html = "\n".join(captured)
    assert _BUFF_COLOR_HEX in combined_html, (
        f"Expected buff colour {_BUFF_COLOR_HEX} in WOUND block for the unit the "
        f"stratagem was activated for, but got:\n{combined_html}"
    )


def test_strength_stratagem_not_scoped_to_other_unit_shows_no_buff_border(
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    """Regression (S122 bug): a different attacker in the same phase gets no S buff."""
    from gameMechanic.stratagemEngine import stratagem_strength_bonus  # noqa: PLC0415
    from uiLayout.diceCompose import _BUFF_COLOR_HEX  # noqa: PLC0415

    active_modifiers = [
        {
            "unit_key": "wh40k_9e.necrons.unit.warriors",
            "source": "Disruption Fields",
            "effect": {"roll_type": "strength", "value": 1, "target": "attacker", "phase": "fight"},
            "expires_at_phase": "fight",
            "expires_at_round": None,
        }
    ]
    str_bonus = stratagem_strength_bonus(active_modifiers, "wh40k_9e.necrons.unit.immortals")
    assert str_bonus == 0

    captured = _collect_markdown(monkeypatch)
    _render_dice_wound_block(
        strength=4 + str_bonus,
        toughness=4,
        wound_stack=[],
        strength_buff=str_bonus,
        on_six_ap=0,
    )
    combined_html = "\n".join(captured)
    assert _BUFF_COLOR_HEX not in combined_html, (
        f"Expected no buff colour {_BUFF_COLOR_HEX} in WOUND block for an attacker the "
        f"stratagem was NOT activated for, but found it in:\n{combined_html}"
    )


# ---------------------------------------------------------------------------
# S137 Bug B — hit_roll_penalty must render exactly ONCE (modifier row only)
# ---------------------------------------------------------------------------


def test_hit_roll_penalty_renders_once_no_duplicate_badge(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Regression (S137 Bug B, Power klaw): the weapon's −1-to-Hit shows once.

    The penalty reaches the HIT block twice from the same YAML effect field:
    as a '−1 to Hit' entry in the modifier stack (assembled in
    _render_resolution_tab via _detect_weapon_special) AND — before the fix —
    as an extra special_die_html badge inside _render_dice_roll_block keyed
    off the same weapon_special['hit_roll_penalty'] flag. The badge branch is
    removed; the label must appear exactly once in the HTML output.
    """
    captured = _collect_markdown(monkeypatch)

    penalty = {"label": "−1 to Hit", "value": -1, "roll_type": "hit", "source": "weapon"}
    hit_block = {"base": 2, "stack": [penalty], "modified": 3}
    weapon_special = {
        "auto_hit": False,
        "extra_hits": False,
        "alternating_fire": False,
        "hit_roll_penalty": True,
        "has_mortal_wounds": False,
    }

    _render_dice_roll_block("HIT", "WS", hit_block, weapon_special)

    combined_html = "\n".join(captured)
    count = combined_html.count("−1 to Hit")
    assert count == 1, (
        f"Expected the '−1 to Hit' label exactly once (modifier row in the dice "
        f"grid); a second occurrence means the duplicate special_die_html badge "
        f"is back. Got {count} occurrence(s)."
    )
