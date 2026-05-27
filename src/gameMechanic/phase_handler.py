"""PhaseHandler — Protocol definition for all game phase handlers."""

from __future__ import annotations

from typing import ClassVar, Protocol


class PhaseHandler(Protocol):
    """Common interface for all game phase handlers.

    Each handler manages one phase of the 40k turn sequence.
    The phase_runner dispatches to render_{stage}() based on state["phase_stage"].

    Stage lifecycle per phase:  start → active → end → next_phase
    """

    phase_name: ClassVar[str]

    def render_start(self, state: dict) -> None:
        """Render phase-start stage UI (e.g. triggered abilities at phase start)."""
        ...

    def render_active(self, state: dict) -> None:
        """Render main phase UI — two player columns + display area."""
        ...

    def render_end(self, state: dict) -> None:
        """Render phase-end stage UI (e.g. triggered abilities at phase end)."""
        ...
