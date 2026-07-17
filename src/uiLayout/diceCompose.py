"""Pure SVG/HTML building blocks for the attack-resolution UI — no Streamlit, fully unit-testable."""

from __future__ import annotations

from constants.symbols import SYM_CROSS, SYM_RESET


def light_cover_label(directive_short_label: str | None = None) -> str:
    """Checkbox label for the Light Cover toggle.

    When a directive negates Light Cover within half range (Vengeful Stars D2),
    a green badge and hint are appended inline so the player sees the hint right
    where they would tick the box. The checkbox remains manually settable.

    Args:
        directive_short_label: short protocol name (e.g. "Vengeful Stars") when
            the directive is active; None for the plain label.
    """
    base = "Light Cover (+1 Save vs Ranged)"
    if directive_short_label:
        return (
            f"{base}  :green-badge[{directive_short_label}]" " :green[No Light Cover ≤ half range]"
        )
    return base


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


def miss_die_html(size: int = 32) -> str:
    """Die-shaped always-miss marker (×).

    The same icon as the value-1 die (left of 2); also used as the general miss
    icon right of the 6 when a threshold is pushed above 6 (AP / heavy penalty),
    so misses read as dice everywhere instead of a bare text ×.
    """
    return dice_face_svg(1, miss=True, size=size)


def dice_row_html(threshold: int) -> str:
    """Row of 6 dice (values 1–6): miss dice left, success dice inside colored frame.

    D5: one die-wide boundary gap with a separator line sits between the last
    miss die and the success frame — same gap as in threshold_header_html, so
    the columns stay aligned. Threshold > 6 (impossible): 6 miss dice + red ×.
    """
    if threshold > 6:
        # All six fail; a miss die right of the 6 marks the impossible 7+ result.
        miss_dice = "".join(dice_face_svg(v, miss=True) for v in range(1, 7))
        return f'<div style="margin:4px 0;">{miss_dice}{miss_die_html()}</div>'
    frame_color = _THRESHOLD_COLOR.get(threshold, "#f97316")
    # An unmodified 1 always fails (core_rules.txt: Hit/Wound/Save rolls) — even when
    # threshold <= 1 pulls it into the success range mathematically, it must still
    # render as the ×-miss die, never as a normal success pip.
    success_dice = "".join(
        dice_face_svg(1, miss=True) if v == 1 else dice_face_svg(v, color=frame_color)
        for v in range(threshold, 7)
    )
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
    # Long labels (e.g. "Power Klaw") are clipped with an ellipsis instead of
    # spilling into dice slot 1. Single-line truncation needs the canonical trio:
    # a bounded width + overflow:hidden + text-overflow:ellipsis (white-space:nowrap).
    return (
        f'<span style="font-size:11px;color:{color};background:#111827;'
        f"border:1px solid {color};border-radius:3px;padding:1px 5px;"
        f"display:inline-block;max-width:{_BADGE_COL_W - 8}px;overflow:hidden;"
        f'text-overflow:ellipsis;white-space:nowrap;vertical-align:middle;">{label}</span>'
    )


def _modifier_color(entry: dict) -> str:  # type: ignore[type-arg]
    """Colour for a modifier badge/arrow (dice_display.md §6).

    An explicit ``color_hint`` ('buff' | 'debuff') wins when present — needed for
    perspective-dependent effects like Quantum Shield, where the sign of ``value``
    does not match who benefits. Otherwise the sign decides (value > 0 → buff/green),
    keeping older modifier dicts that carry no hint backward compatible.
    """
    hint = entry.get("color_hint")
    if hint == "buff":
        return _BUFF_COLOR_HEX
    if hint == "debuff":
        return _DEBUFF_COLOR_HEX
    return _BUFF_COLOR_HEX if entry.get("value", 0) > 0 else _DEBUFF_COLOR_HEX


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


def _modifier_columns(
    left_val: int, right_val: int, right_off_scale: bool = False
) -> tuple[int, int]:
    """Clamp a modifier's two die values to grid columns 1..6 (pure, testable).

    right_off_scale (a save worsened past 6) anchors the right marker at column 6;
    the renderer appends a miss die after the 6 for that case.
    """
    left_col = max(1, min(6, left_val))
    right_col = 6 if right_off_scale else max(1, min(6, right_val))
    return left_col, right_col


def _modifier_slot_html(inner: str) -> str:
    return (
        f'<span style="display:inline-block;width:{_DIE_SLOT}px;text-align:center;'
        f'vertical-align:middle;">{inner}</span>'
    )


def _glyph_span(glyph: str, color: str) -> str:
    return f'<span style="color:{color};font-weight:bold;">{glyph}</span>'


def _aligned_modifier_row_html(
    label: str,
    value: int,
    left_val: int,
    left_color: str,
    right_val: int,
    right_color: str,
    base_threshold: int,
    right_off_scale: bool = False,
    badge_color: str | None = None,
    left_miss: bool = False,
) -> str:
    """Modifier row aligned to the 1..6 scale (D5, Finding 9.2).

    The two dice sit under their own value columns; the slots between them carry a
    connector arrow, so the visual length is proportional to the shift (AP-3 spans
    three columns, Cover +1 one). The boundary gap is placed at base_threshold so
    the columns line up with the header / dice rows above. Off-scale (>6) appends a
    miss die right of the 6. left_miss draws the left die as the ×-miss face —
    used when it stands for a natural 1, which always fails (S122/F3, Variante A).
    """
    left_col, right_col = _modifier_columns(left_val, right_val, right_off_scale)
    lo, hi = sorted((left_col, right_col))
    shift = hi - lo
    rightward = (
        value > 0
    )  # buff widens the success window → arrow points right (lower rolls suffice)
    glyph_color = _BUFF_COLOR_HEX if rightward else _DEBUFF_COLOR_HEX
    head_glyph = f"+{abs(value)}→" if rightward else f"←{abs(value)}"  # spec §2.1
    slots: list[str] = []
    for v in range(1, 7):
        if 2 <= base_threshold <= 6 and v == base_threshold:
            # A 1-column shift leaves no slot between the two dice, so the magnitude
            # label rides in the boundary gap that sits between them (spec §3.1 ±1).
            if shift == 1 and v == hi and lo == hi - 1:
                slots.append(_modifier_slot_html(_glyph_span(head_glyph, glyph_color)))
            else:
                slots.append(_boundary_gap_html(with_line=False))
        if v == left_col:
            inner = (
                dice_face_svg(1, miss=True)
                if left_miss
                else dice_face_svg(left_val, color=left_color)
            )
        elif v == right_col and not right_off_scale:
            inner = dice_face_svg(right_val, color=right_color)
        elif lo < v < hi:
            head = (rightward and v == hi - 1) or (not rightward and v == lo + 1)
            inner = _glyph_span(head_glyph if head else "─", glyph_color)
        else:
            inner = ""
        slots.append(_modifier_slot_html(inner))
    if right_off_scale:
        slots.append(miss_die_html())
    sign = "+" if value > 0 else ("-" if value < 0 else "")
    chip_color = badge_color if badge_color is not None else right_color
    # A label that already leads with its signed value (e.g. "−1 to Hit") keeps
    # the badge as-is — appending the value again would double it to
    # "−1 to Hit -1" (same doubling bug documented at save_ap_modifier_row_html).
    value_token = f"{sign}{abs(value)}"
    label_leads_with_value = label.replace("−", "-").startswith(value_token)
    badge_text = label if label_leads_with_value else f"{label} {value_token}"
    badge = _badge_chip(badge_text, chip_color)
    content = f'<div style="display:flex;align-items:center;">{"".join(slots)}</div>'
    return grid_row_html(badge, content)


def modifier_die_pair_html(
    from_thresh: int, to_thresh: int, label: str, value: int, color: str, base_threshold: int = 0
) -> str:
    """HIT/WOUND modifier row, aligned to the scale.

    Improvement (value > 0): grey new threshold (lower) ← colored old threshold.
    Penalty (value < 0): grey from−1 (already missed) → colored from (newly fails).
    base_threshold positions the boundary gap (defaults to from_thresh).
    """
    base = base_threshold or from_thresh
    from_clamped = max(1, min(6, from_thresh))
    to_clamped = max(1, min(6, to_thresh))
    boundary = max(1, min(6, from_thresh - 1))
    if value > 0:
        left_val, left_color, right_val, right_color = to_clamped, "#6b7280", from_clamped, color
    else:
        left_val, left_color, right_val, right_color = boundary, "#6b7280", from_clamped, color
    return _aligned_modifier_row_html(
        label, value, left_val, left_color, right_val, right_color, base, badge_color=color
    )


def save_modifier_die_pair_html(armour: int, value: int, label: str, color: str) -> str:
    """SAVE modifier row, anchored to the base armour value (never cumulative).

    Buff  (value > 0, e.g. Cover +1, armour 3): colored(armour−value) ← grey(armour).
    Debuff (value < 0, e.g. AP-2,    armour 3): grey(armour−1) → colored(armour+|value|−1).
    If the newly-failing value exceeds 6 (e.g. Sv 6+ with AP-4) a miss die marks it.
    If a buff pushes the target below 2+ (armour − value ≤ 1), the source die stands
    for a natural 1 — which always fails — and is drawn as the ×-miss face (S122/F3).
    """
    n = abs(value)
    if value > 0:
        left_val, left_color = max(1, min(6, armour - n)), color
        right_val, right_color = max(1, min(6, armour)), "#6b7280"
        off_scale = False
        left_miss = armour - n <= 1
    else:
        left_val, left_color = max(1, min(6, armour - 1)), "#6b7280"
        right_raw = armour + n - 1
        right_val, right_color = max(1, min(6, right_raw)), color
        off_scale = right_raw > 6
        left_miss = False
    return _aligned_modifier_row_html(
        label,
        value,
        left_val,
        left_color,
        right_val,
        right_color,
        min(armour, 6),
        off_scale,
        badge_color=color,
        left_miss=left_miss,
    )


def save_ap_modifier_row_html(armour: int, ap: int) -> str:
    """SAVE block AP modifier row.

    Label is the name only ('AP'); the row appends the signed value once.
    Passing f"AP{ap}" as the label would produce "AP-4 -4" (doubling bug).
    """
    return save_modifier_die_pair_html(armour, ap, "AP", _DEBUFF_COLOR_HEX)


def special_die_html(label: str, content: str = "") -> str:
    """Badge for special weapon abilities (Tesla, Dakka, Power Klaw, Reroll, etc.)."""
    text = f"{label}: {content}" if content else label
    return (
        f'<span style="background:#111827;border:1px solid #f59e0b;border-radius:4px;'
        f'padding:2px 6px;font-size:11px;color:#f59e0b;margin:2px;">'
        f"{text}</span>"
    )


_REROLL_GLYPH = SYM_RESET  # app-wide reset/redo glyph (gameHeader, _common, gameProtocoll)
_AUTO_FAIL_GLYPH = SYM_CROSS  # below-slot annotation; distinct from the die-shaped miss icon


def _marker_row_html(
    label_html: str, glyph: str, marker_slots: set[int], base_threshold: int, color: str
) -> str:
    """Sub-row aligned to the 1..6 grid with *glyph* under each marker slot.

    Shared layout for the reroll (↺) and always-fail (✕) annotations: the glyph
    sits in the same die-sized column as the value it refers to, so it lines up
    under the dice rows above (dice_display.md §10.1 / §10.2).
    """
    slots: list[str] = []
    for v in range(1, 7):
        if 2 <= base_threshold <= 6 and v == base_threshold:
            slots.append(_boundary_gap_html(with_line=False))
        inner = (
            f'<span style="color:{color};font-weight:bold;">{glyph}</span>'
            if v in marker_slots
            else ""
        )
        slots.append(_modifier_slot_html(inner))
    content = f'<div style="display:flex;align-items:center;">{"".join(slots)}</div>'
    return grid_row_html(label_html, content)


def reroll_marker_row_html(slots: list[int], base_threshold: int = 0) -> str:
    """↺ marker below each re-rolled slot (dice_display.md §10.1).

    Display building block — not yet wired into a roll block; a producer that
    feeds reroll data (e.g. reroll_hit_1) into the dice block consumes it later.
    """
    badge = _badge_chip("Reroll", "#f59e0b")
    return _marker_row_html(badge, _REROLL_GLYPH, set(slots), base_threshold, "#f59e0b")


def always_fail_marker_row_html(
    slots: list[int],
    base_threshold: int = 0,
    color_hint: str | None = None,
    label: str | None = None,
) -> str:
    """✕ marker below each always-failing slot (dice_display.md §5 / §10.2).

    color_hint sets the perspective colour: the defender sees a buff (green, the
    attacker's low rolls fail), the rolling attacker a debuff (red). Display
    building block — wired once a producer (e.g. Quantum Shield) supplies the slots.
    ``label`` names the triggering ability (e.g. "Quantum Shielding"), read from
    YAML by the caller; falls back to the generic "Auto-fail" when no ability
    label is available (B-103).
    """
    color = _modifier_color({"color_hint": color_hint, "value": -1})
    badge = _badge_chip(label or "Auto-fail", color)
    return _marker_row_html(badge, _AUTO_FAIL_GLYPH, set(slots), base_threshold, color)


def _triggered_die_chip_html(content: str, color: str) -> str:
    """Die-shaped box (32px, like a face) holding short text such as 'AP-1'."""
    return (
        f'<span style="display:inline-block;width:30px;height:30px;line-height:30px;'
        f"border:1.5px solid {color};border-radius:4px;background:#1e293b;"
        f"font-size:9px;font-weight:700;color:{color};text-align:center;"
        f'vertical-align:middle;box-sizing:border-box;">{content}</span>'
    )


def value_triggered_die_row_html(
    label: str, trigger_value: int, content: str, color: str, base_threshold: int = 0
) -> str:
    """Die-shaped chip in the *trigger_value* column, all other slots empty.

    For directive effects that fire on a specific unmodified roll — Hungry Void D1:
    on an unmodified wound roll of 6, improve AP by 1, shown as ``[AP-1]`` in the 6
    column. Reads like the dice rows above: the chip sits in the same die-sized slot
    as the value it triggers on. base_threshold keeps the boundary gap aligned with
    the dice rows above so the columns stay flush.
    """
    slots: list[str] = []
    for v in range(1, 7):
        if 2 <= base_threshold <= 6 and v == base_threshold:
            slots.append(_boundary_gap_html(with_line=False))
        inner = _triggered_die_chip_html(content, color) if v == trigger_value else ""
        slots.append(_modifier_slot_html(inner))
    row = f'<div style="display:flex;align-items:center;">{"".join(slots)}</div>'
    return grid_row_html(_badge_chip(label, color), row)
