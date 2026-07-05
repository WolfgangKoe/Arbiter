"""PhaseHandler — Protocol definition for all game phase handlers."""

from __future__ import annotations

from typing import ClassVar, Protocol


class PhaseHandler(Protocol):
    """Common interface for all game phase handlers.

    Each handler manages one phase of the 40k turn sequence.
    The phase_runner renders exactly one view per phase via render_active();
    phase transitions are driven by game_state.next_phase() (Next-Phase button).
    """

    phase_name: ClassVar[str]

    def render_active(self, state: dict) -> None:
        """Render main phase UI — two player columns + display area."""
        ...
