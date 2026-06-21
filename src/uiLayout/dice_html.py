"""Streamlit render blocks for the attack-resolution UI (HIT / WOUND / SAVE)."""

from __future__ import annotations

import streamlit as st

from uiLayout.dice_compose import (
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
)


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
        current = base
        parts = []
        for entry in stack:
            next_thresh = max(2, current - entry["value"])
            color = _modifier_color(entry)
            parts.append(
                modifier_die_pair_html(
                    current, next_thresh, entry["label"], entry["value"], color, base_threshold=base
                )
            )
            current = next_thresh
        parts.append(
            grid_row_html(
                f'<span style="color:#f8fafc;font-weight:600;">Eff. {modified}+</span>',
                threshold_header_html(min(modified, 7)) + dice_row_html(min(modified, 7)),
            )
        )
        st.markdown("".join(parts), unsafe_allow_html=True)
    if weapon_special:
        badges = []
        if weapon_special.get("extra_hits"):
            badges.append(special_die_html("Extra Hits", "unmod. 6 = +2 Hits"))
        if weapon_special.get("alternating_fire"):
            badges.append(special_die_html("Alt. Fire"))
        if weapon_special.get("hit_roll_penalty"):
            badges.append(special_die_html("−1 to Hit"))
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
) -> None:
    """WOUND block: S vs T header, dice row, modifier pairs in blue."""
    from gameMechanic.combat import wound_threshold  # noqa: PLC0415

    base = wound_threshold(strength, toughness)
    net = min(1, max(-1, sum(e["value"] for e in wound_stack)))
    modified = max(2, base - net)
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
    if wound_stack:
        current = base
        parts = []
        for entry in wound_stack:
            next_thresh = max(2, current - entry["value"])
            color = _modifier_color(entry)
            parts.append(
                modifier_die_pair_html(
                    current, next_thresh, entry["label"], entry["value"], color, base_threshold=base
                )
            )
            current = next_thresh
        parts.append(
            grid_row_html(
                f'<span style="color:#f8fafc;font-weight:600;">Eff. {modified}+</span>',
                threshold_header_html(min(modified, 7)) + dice_row_html(min(modified, 7)),
            )
        )
        st.markdown("".join(parts), unsafe_allow_html=True)


def _render_dice_save_block(save: dict, ap: int, ability_invuln: bool = False) -> None:  # type: ignore[type-arg]
    """SAVE block: table-aligned rows (label | content) for armour, modifiers, eff, invuln."""
    armour = save["armour"]
    armour_eff = save["armour_eff"]
    invuln = save["invuln"]
    using_invuln = save["using_invuln"]
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
        armour_modified = armour_eff - sum(m["value"] for m in stack)
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
        active_badge = (
            f'<span style="font-size:10px;color:{inv_color};border:1px solid {inv_color};'
            f'border-radius:3px;padding:0 3px;margin-left:4px;">active</span>'
            if using_invuln
            else ""
        )
        note = '<span style="font-size:10px;color:#4b5563;margin-left:4px;">AP/Cover N/A</span>'
        inv_label = f"Inv {invuln}+{active_badge}{note}"
        inv_row = grid_row_html(
            inv_label,
            threshold_header_html(min(invuln, 7)) + dice_row_html(min(invuln, 7)),
        )
        st.markdown(inv_row, unsafe_allow_html=True)
