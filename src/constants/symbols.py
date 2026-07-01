"""App-wide UI glyph constants — one canonical source per symbol.

Pure Unicode string literals, no logic and no faction knowledge. Centralising
them means a symbol can be swapped project-wide in one place and missing glyphs
stay consistent (design_system.md §3).

Usage
-----
    from constants.symbols import SYM_EXPAND, SYM_CHECK
    label = f"{SYM_EXPAND} {unit.name_en}"
"""

# Selection / navigation arrows
SYM_EXPAND: str = "▶"  # not selected → click to expand / view
SYM_COLLAPSE: str = "◀"  # selected / active → click to collapse
SYM_EXPAND_ALT: str = "▷"  # expand variant for a row with no selectable target

# Confirmation / actions
SYM_CHECK: str = "✓"  # passed / done / assigned
SYM_CROSS: str = "✕"  # failed / remove / cancel
SYM_ADD: str = "＋"  # add / assign
SYM_SWORDS: str = "⚔"  # combat / fight action
SYM_RESET: str = "↺"  # reset / undo / reroll
