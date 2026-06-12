"""SVG dice + HTML building blocks for the attack-resolution UI (6d-v3)."""

from __future__ import annotations

import streamlit as st

_THRESHOLD_COLOR: dict[int, str] = {
    2: "#22c55e",
    3: "#22c55e",
    4: "#f59e0b",
    5: "#f97316",
    6: "#f97316",
}

_PIP_POSITIONS: dict[int, list[tuple[int, int]]] = {
    1: [(16, 16)],
    2: [(9, 9), (23, 23)],
    3: [(9, 9), (16, 16), (23, 23)],
    4: [(9, 9), (9, 23), (23, 9), (23, 23)],
    5: [(9, 9), (9, 23), (23, 9), (23, 23), (16, 16)],
    6: [(9, 9), (9, 16), (9, 23), (23, 9), (23, 16), (23, 23)],
}


# Shared column grid (D5): every dice row = badge column + die-sized slots.
# The boundary gap (one die wide) appears in header AND dice row → labels stay
# flush above the die of their value.
_DIE_SLOT = 34  # svg 32px + 2px margin
_FRAME_INSET = 5  # success-frame border+padding shifts dice right by this much
_BUFF_COLOR_HEX = "#4a9a5a"  # Buff = grün (design_colors.md §0)
_DEBUFF_COLOR_HEX = "#ef4444"


def _boundary_gap_html(with_line: bool) -> str:
    """One die-wide gap slot at the success boundary ('Luft' + separator line)."""
    line = (
        '<span style="display:inline-block;width:2px;height:34px;'
        'background:#6b7280;border-radius:1px;"></span>'
        if with_line
        else ""
    )
    return (
        f'<span style="display:inline-block;width:{_DIE_SLOT}px;text-align:center;'
        f'vertical-align:middle;">{line}</span>'
    )


def threshold_header_html(threshold: int) -> str:
    """Header labels 1..6, die-sized and full brightness, aligned with dice_row_html."""
    color = _THRESHOLD_COLOR.get(min(6, threshold), "#f97316")
    parts = []
    for v in range(1, 7):
        if 2 <= threshold <= 6 and v == threshold:
            parts.append(_boundary_gap_html(with_line=False))
        label = f"{v}+"
        if v == threshold:
            style = (
                f"width:{_DIE_SLOT}px;text-align:center;display:inline-block;"
                f"font-size:15px;font-weight:700;color:{color};"
                f"border:1px solid {color};border-radius:3px;"
            )
        else:
            style = (
                f"width:{_DIE_SLOT}px;text-align:center;display:inline-block;"
                f"font-size:15px;font-weight:600;color:#e7e5e4;"
            )
        parts.append(f'<span style="{style}">{label}</span>')
    return f'<div style="display:flex;align-items:center;margin:0 0 1px 0;">{"".join(parts)}</div>'


def dice_face_svg(value: int, color: str = "#6b7280", miss: bool = False, size: int = 32) -> str:
    """SVG for a single d6 face with pip pattern. Value 1 always shows × (always-miss marker)."""
    pips = _PIP_POSITIONS.get(max(1, min(6, value)), [])
    bg = "#111827" if miss else "#1e293b"
    border = "#374151" if miss else color
    if miss and value == 1:
        pip_html = (
            '<line x1="9" y1="9" x2="23" y2="23" stroke="#c0392b" stroke-width="2.5"/>'
            '<line x1="23" y1="9" x2="9" y2="23" stroke="#c0392b" stroke-width="2.5"/>'
        )
    else:
        pip_color = "#374151" if miss else color
        pip_html = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="{pip_color}"/>' for x, y in pips)
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 32 32" '
        f'style="display:inline-block;vertical-align:middle;margin:1px;">'
        f'<rect x="1" y="1" width="30" height="30" rx="4" ry="4" '
        f'fill="{bg}" stroke="{border}" stroke-width="1.5"/>'
        f"{pip_html}</svg>"
    )


def dice_row_html(threshold: int) -> str:
    """Row of 6 dice (values 1–6): miss dice left, success dice inside colored frame.

    D5: one die-wide boundary gap with a separator line sits between the last
    miss die and the success frame — same gap as in threshold_header_html, so
    the columns stay aligned. Threshold > 6 (impossible): 6 miss dice + red ×.
    """
    if threshold > 6:
        miss_dice = "".join(dice_face_svg(v, miss=True) for v in range(1, 7))
        impossible = (
            '<span style="font-size:16px;color:#ef4444;vertical-align:middle;'
            'margin:0 4px;font-weight:bold;">×</span>'
        )
        return f'<div style="margin:4px 0;">{miss_dice}{impossible}</div>'
    frame_color = _THRESHOLD_COLOR.get(threshold, "#f97316")
    success_dice = "".join(dice_face_svg(v, color=frame_color) for v in range(threshold, 7))
    framed = (
        f'<span style="border:2px solid {frame_color};border-radius:5px;'
        f"padding:2px 3px;display:inline-block;vertical-align:middle;"
        f'margin-left:-{_FRAME_INSET}px;">'
        f"{success_dice}</span>"
    )
    if threshold <= 1:
        # All dice succeed — no miss dice, no gap
        return f'<div style="margin:4px 0;">{framed}</div>'
    miss_section = "".join(dice_face_svg(v, miss=True) for v in range(1, threshold))
    gap = _boundary_gap_html(with_line=True)
    return f'<div style="margin:4px 0;">{miss_section}{gap}{framed}</div>'


_BADGE_COL_W = 96  # left badge column (D5): AP-X, Heavy Cover, MWBD, Eff., …


def _badge_chip(label: str, color: str) -> str:
    return (
        f'<span style="font-size:11px;color:{color};background:#111827;'
        f"border:1px solid {color};border-radius:3px;padding:1px 5px;"
        f'white-space:nowrap;">{label}</span>'
    )


def grid_row_html(label_html: str, content: str) -> str:
    """One row of the D5 grid: fixed badge column on the left, content right.

    Every row of a dice block (header+dice, modifier pairs, Eff., Inv.) goes
    through this so the dice columns align vertically.
    """
    return (
        f'<div style="display:flex;align-items:center;margin:2px 0;">'
        f'<div style="width:{_BADGE_COL_W}px;flex-shrink:0;display:flex;'
        f'align-items:center;font-size:12px;color:#9ca3af;">{label_html}</div>'
        f'<div style="flex:1;">{content}</div></div>'
    )


def block_divider_html() -> str:
    """Horizontal separator between HIT / WOUND / SAVE blocks (D5: 'Luft')."""
    return '<hr style="border:none;border-top:1px solid #2e2618;margin:10px 0;">'


def modifier_die_pair_html(
    from_thresh: int, to_thresh: int, label: str, value: int, color: str
) -> str:
    """Modifier row: badge column + from-die (neutral) + arrow + to-die (colored).

    Convention: lower die value always on left, higher on right (aligns with dice row).
    Arrow: → for improvements (value > 0), ← for penalties (value < 0).
    For improvements the threshold decreases, so to_thresh < from_thresh — swap so
    the lower value (to_thresh) appears on the left and higher (from_thresh) on the right.
    """
    sign = "+" if value > 0 else ("-" if value < 0 else "")
    arrow = "→" if value > 0 else "←"
    from_clamped = max(1, min(6, from_thresh))
    to_clamped = max(1, min(6, to_thresh))
    # Improvements: grey = new threshold, colored = old threshold (newly passes).
    # Penalties: grey = from_thresh−1 (never hit anyway), colored = from_thresh (newly fails).
    boundary = max(1, min(6, from_thresh - 1))
    if value > 0:
        left_die = dice_face_svg(to_clamped, color="#6b7280")
        right_die = dice_face_svg(from_clamped, color=color)
    else:
        left_die = dice_face_svg(boundary, color="#6b7280")
        right_die = dice_face_svg(from_clamped, color=color)
    pair = (
        f'<div style="display:flex;align-items:center;gap:4px;">'
        f"{left_die}"
        f'<span style="color:{color};font-size:12px;font-weight:bold;">'
        f"{arrow}{sign}{abs(value)}{arrow}</span>"
        f"{right_die}</div>"
    )
    return grid_row_html(_badge_chip(label, color), pair)


def save_modifier_die_pair_html(armour: int, value: int, label: str, color: str) -> str:
    """SAVE modifier pair always anchored to the base armour value (never cumulative).

    Buff  (value > 0, e.g. Cover+1, armour=3): grün(armour-value) → grau(armour)
      "A 2 that used to fail at 3+ now passes."
    Debuff (value < 0, e.g. AP-2,   armour=3): grau(armour-1) → rot(armour+|value|-1)
      "A 4 that used to pass at 3+ now fails (4-2=2 < 3)."
    P16 edge: if the newly-failing value exceeds 6 (e.g. Sv 6+ with AP-4), no die
    can show it — a red × marks the impossible range instead of a clamped die.
    """
    sign = "+" if value > 0 else ("-" if value < 0 else "")
    n = abs(value)
    if value > 0:
        left_val = max(1, min(6, armour - n))
        right_val = max(1, min(6, armour))
        arrow = "→"
        left_die = dice_face_svg(left_val, color=color)
        right_die = dice_face_svg(right_val, color="#6b7280")
    else:
        left_val = max(1, min(6, armour - 1))
        right_raw = armour + n - 1
        right_val = max(1, min(6, right_raw))
        arrow = "←"
        left_die = dice_face_svg(left_val, color="#6b7280")
        if right_raw > 6:
            right_die = (
                f'<span style="font-size:16px;color:{color};vertical-align:middle;'
                f'font-weight:bold;" title="exceeds 6 — save impossible">×</span>'
            )
        else:
            right_die = dice_face_svg(right_val, color=color)
    pair = (
        f'<div style="display:flex;align-items:center;gap:4px;">'
        f"{left_die}"
        f'<span style="color:{color};font-size:12px;font-weight:bold;">'
        f"{arrow}{sign}{n}{arrow}</span>"
        f"{right_die}</div>"
    )
    return grid_row_html(_badge_chip(label, color), pair)


def special_die_html(label: str, content: str = "") -> str:
    """Badge for special weapon abilities (Tesla, Dakka, Power Klaw, Reroll, etc.)."""
    text = f"{label}: {content}" if content else label
    return (
        f'<span style="background:#111827;border:1px solid #f59e0b;border-radius:4px;'
        f'padding:2px 6px;font-size:11px;color:#f59e0b;margin:2px;">'
        f"{text}</span>"
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
            color = _BUFF_COLOR_HEX if entry["value"] > 0 else _DEBUFF_COLOR_HEX
            parts.append(
                modifier_die_pair_html(current, next_thresh, entry["label"], entry["value"], color)
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
        if weapon_special.get("tesla"):
            badges.append(special_die_html("Tesla", "unmod. 6 = +2 Hits"))
        if weapon_special.get("dakka"):
            badges.append(special_die_html("Dakka"))
        if weapon_special.get("klaw_penalty"):
            badges.append(special_die_html("Power Klaw", "−1 to Hit"))
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
            color = _BUFF_COLOR_HEX if entry["value"] > 0 else _DEBUFF_COLOR_HEX
            parts.append(
                modifier_die_pair_html(current, next_thresh, entry["label"], entry["value"], color)
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
        rows.append(save_modifier_die_pair_html(armour, ap, f"AP{ap}", _DEBUFF_COLOR_HEX))
    for m in stack:
        color = _BUFF_COLOR_HEX if m["value"] > 0 else _DEBUFF_COLOR_HEX
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
