"""Streamlit render blocks for the attack-resolution UI (HIT / WOUND / SAVE)."""

from __future__ import annotations

import streamlit as st

from uiLayout.diceCompose import (
    _BUFF_COLOR_HEX,
    _THRESHOLD_COLOR,
    _modifier_color,
    block_divider_html,
    dice_row_html,
    grid_row_html,
    modifier_die_pair_html,
    save_ap_modifier_row_html,
    save_modifier_die_pair_html,
    special_die_html,
    threshold_header_html,
    value_triggered_die_row_html,
)


def _capped_modifier_threshold(base: int, modifier_total: int) -> int:
    """Threshold after the 9E hit/wound modifier cap: at most ±1 from base, range [2, 6].

    ``modifier_total`` may be a single modifier value or an uncapped sum; a positive
    modifier lowers the threshold, a negative one raises it — never by more than one
    step from ``base``. An unmodified 6 always succeeds and an unmodified 1 always
    fails (core_rules.txt "Hit Roll"/"Wound Roll"), so the result never leaves [2, 6].
    """
    return min(6, max(2, max(base - 1, min(base + 1, base - modifier_total))))


def _render_dice_roll_block(
    title: str,
    skill_label: str,
    block: dict,  # type: ignore[type-arg]
    weapon_special: dict | None = None,  # type: ignore[type-arg]
) -> None:
    """HIT or WOUND roll block: threshold header + dice row + modifier pairs."""
    base = block["base"]
    stack = block.get("stack", [])
    modified = block.get("modified", base)
    st.markdown(f"**{title}** &nbsp; {skill_label} {base}+", unsafe_allow_html=True)
    st.markdown(
        grid_row_html("", threshold_header_html(base) + dice_row_html(base)),
        unsafe_allow_html=True,
    )
    if stack:
        parts = []
        for entry in stack:
            next_thresh = _capped_modifier_threshold(base, entry["value"])
            color = _modifier_color(entry)
            parts.append(
                modifier_die_pair_html(
                    base, next_thresh, entry["label"], entry["value"], color, base_threshold=base
                )
            )
        parts.append(
            grid_row_html(
                f'<span style="color:#f8fafc;font-weight:600;">Eff. {modified}+</span>',
                threshold_header_html(modified) + dice_row_html(modified),
            )
        )
        st.markdown("".join(parts), unsafe_allow_html=True)
    if weapon_special:
        badges = []
        if weapon_special.get("extra_hits"):
            badges.append(special_die_html("Extra Hits", "unmod. 6 = +2 Hits"))
        if weapon_special.get("alternating_fire"):
            badges.append(special_die_html("Alt. Fire", "First attacks if within half range"))
        # hit_roll_penalty gets NO badge here: it already renders as a
        # modifier row inside the dice grid (_common.py final_atk_mods) —
        # a second badge showed the same −1 twice (S137 Bug B).
        if badges:
            st.markdown(
                f'<div style="margin-top:4px;">{"".join(badges)}</div>',
                unsafe_allow_html=True,
            )


def _render_dice_wound_block(
    strength: int,
    toughness: int,
    wound_stack: list[dict],  # type: ignore[type-arg]
    strength_buff: int = 0,
    on_six_ap: int = 0,
    on_six_label: str = "",
    modified: int | None = None,
) -> None:
    """WOUND block: S vs T header, dice row, modifier pairs in blue.

    on_six_ap > 0 adds a value-triggered row showing ``[AP-N]`` in the 6 column
    (Hungry Void D1: unmodified wound roll of 6 improves AP). on_six_label is the
    data-driven directive name shown in the badge column. ``modified`` should be
    the effective threshold already resolved by combat.resolve_attack_modifiers
    (single source of truth for the 9E cap); when omitted, it is derived locally
    from wound_stack for callers that only have the stack.
    """
    from gameMechanic.combat import wound_threshold  # noqa: PLC0415

    base = wound_threshold(strength, toughness)
    if modified is None:
        modified = _capped_modifier_threshold(base, sum(e["value"] for e in wound_stack))
    rel = ">" if strength > toughness else ("=" if strength == toughness else "<")
    # D5: S/T comparison clearly highlighted; NO "→ N+" — the result is the
    # boxed threshold in the header row below.
    hl = 'style="font-size:1.05rem;font-weight:700;color:#fbbf24;"'
    if strength_buff > 0:
        s_style = (
            f'style="font-size:1.05rem;font-weight:700;color:{_BUFF_COLOR_HEX};'
            f'border:1px solid {_BUFF_COLOR_HEX};border-radius:3px;padding:0 3px;"'
        )
    else:
        s_style = hl
    st.markdown(block_divider_html(), unsafe_allow_html=True)
    st.markdown(
        f"**WOUND** &nbsp; <span {s_style}>S {strength}</span> "
        f'<span style="font-size:1.05rem;font-weight:700;color:#e7e5e4;">{rel}</span> '
        f"<span {hl}>T {toughness}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        grid_row_html("", threshold_header_html(base) + dice_row_html(base)),
        unsafe_allow_html=True,
    )
    if on_six_ap > 0:
        # Hungry Void D1 (class B): on an unmodified wound roll of 6, AP improves.
        # Applied at the table — shown as [AP-N] in the 6 column. Benefits the
        # attacker, so it reads as a buff (green), like any other attacker buff.
        st.markdown(
            value_triggered_die_row_html(
                on_six_label or "Directive",
                6,
                f"AP-{on_six_ap}",
                _BUFF_COLOR_HEX,
                base_threshold=base,
            ),
            unsafe_allow_html=True,
        )
    if wound_stack:
        parts = []
        for entry in wound_stack:
            next_thresh = _capped_modifier_threshold(base, entry["value"])
            color = _modifier_color(entry)
            parts.append(
                modifier_die_pair_html(
                    base, next_thresh, entry["label"], entry["value"], color, base_threshold=base
                )
            )
        parts.append(
            grid_row_html(
                f'<span style="color:#f8fafc;font-weight:600;">Eff. {modified}+</span>',
                threshold_header_html(modified) + dice_row_html(modified),
            )
        )
        st.markdown("".join(parts), unsafe_allow_html=True)


def _render_dice_save_block(save: dict, ap: int, ability_invuln: bool = False) -> None:  # type: ignore[type-arg]
    """SAVE block: table-aligned rows (label | content) for armour, modifiers, eff, invuln."""
    armour = save["armour"]
    armour_eff = save["armour_eff"]
    invuln = save["invuln"]
    stack = save.get("stack", [])

    # D5: Sv value next to the SAVE title — consistent with WS/BS in the HIT title
    sv_text = f"Sv {armour}+" if armour <= 6 else "Sv —"
    st.markdown(block_divider_html(), unsafe_allow_html=True)
    st.markdown(f"**SAVE** &nbsp; {sv_text}", unsafe_allow_html=True)

    rows: list[str] = []

    # Armour base row
    rows.append(
        grid_row_html("", threshold_header_html(min(armour, 7)) + dice_row_html(min(armour, 7)))
    )

    # Modifier rows (AP + cover stack) — each anchored to base armour, never cumulative
    has_modifiers = ap != 0 or bool(stack)
    if ap != 0:
        rows.append(save_ap_modifier_row_html(armour, ap))
    for m in stack:
        color = _modifier_color(m)
        rows.append(save_modifier_die_pair_html(armour, m["value"], m["label"], color))

    # Effective save row: always shows the armour-path result (after AP + cover).
    # Invuln is shown separately below with its own row — not mixed into this value.
    if has_modifiers:
        # Floor at 2+ (S122/F3): an unmodified 1 always fails, so the effective
        # save is never shown better than 2+ — mirrors resolve_save()'s max(2, …).
        armour_modified = max(2, armour_eff - sum(m["value"] for m in stack))
        eff_clamped = min(armour_modified, 7)
        eff_label_text = f"{armour_modified}+" if armour_modified <= 6 else "—"
        rows.append(
            grid_row_html(
                f'<span style="color:#f8fafc;font-weight:600;">Eff. {eff_label_text}</span>',
                threshold_header_html(eff_clamped) + dice_row_html(eff_clamped),
            )
        )

    st.markdown("".join(rows), unsafe_allow_html=True)

    # Invuln save block (separate section)
    if invuln is not None:
        inv_color = (
            _BUFF_COLOR_HEX if ability_invuln else _THRESHOLD_COLOR.get(min(6, invuln), "#f97316")
        )
        inv_label = f'<span style="color:{inv_color};font-weight:600;">Inv {invuln}+</span>'
        inv_row = grid_row_html(
            inv_label,
            threshold_header_html(min(invuln, 7)) + dice_row_html(min(invuln, 7)),
        )
        st.markdown(inv_row, unsafe_allow_html=True)
