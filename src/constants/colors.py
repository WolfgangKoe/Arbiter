"""Semantic colour constants — Tailwind v3 palette extracts.

Only the five required palettes are included. No Tailwind framework dependency.
Hex values from https://tailwindcss.com/docs/customizing-colors (Tailwind CSS v3).

Usage
-----
    from constants.colors import COLOR_ACTION, EMERALD

Semantic aliases map to a specific shade from each palette.
UI components should use the semantic aliases; raw palettes are for advanced use.
"""

# ── Raw palettes (shade → hex) ──────────────────────────────────────────────

EMERALD: dict[str, str] = {
    "300": "#6ee7b7",
    "400": "#34d399",
    "500": "#10b981",
    "600": "#059669",
}

NEUTRAL: dict[str, str] = {
    "300": "#d4d4d4",
    "400": "#a3a3a3",
    "500": "#737373",
    "600": "#525252",
}

AMBER: dict[str, str] = {
    "300": "#fcd34d",
    "400": "#fbbf24",
    "500": "#f59e0b",
    "600": "#d97706",
}

RED: dict[str, str] = {
    "300": "#fca5a5",
    "400": "#f87171",
    "500": "#ef4444",
    "600": "#dc2626",
}

BLUE: dict[str, str] = {
    "300": "#93c5fd",
    "400": "#60a5fa",
    "500": "#3b82f6",
    "600": "#2563eb",
}

# ── Semantic aliases ─────────────────────────────────────────────────────────

COLOR_ACTION: str = EMERALD["500"]  # own actions & positive effects
COLOR_STATUS: str = NEUTRAL["400"]  # neutral status information
COLOR_WARNING: str = AMBER["500"]  # enemy presence, caution
COLOR_CRITICAL: str = RED["500"]  # critical buttons & danger info
COLOR_EFFECT: str = BLUE["500"]  # abilities, guidelines, passive effects

# Lighter variants for backgrounds / muted display
COLOR_ACTION_MUTED: str = EMERALD["300"]
COLOR_WARNING_MUTED: str = AMBER["300"]
COLOR_CRITICAL_MUTED: str = RED["300"]
COLOR_EFFECT_MUTED: str = BLUE["300"]
