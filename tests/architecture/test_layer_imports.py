"""Guard: layer dependency direction.

The data layer (gameObjects/) is the foundation: it must not depend on the
mechanic layer (gameMechanic/) or the view layer (uiLayout/). Dependencies point
inward only — uiLayout/gameMechanic may use gameObjects, never the reverse.

NOTE — known coupling, deliberately NOT guarded here:
gameMechanic/ currently imports render helpers from ``uiLayout._common`` (6 files).
That violates the original "gameMechanic = no Streamlit" vision but is the real
state today (the phase modules render). It is tracked as debt in
docs/goals/backlog.md, not enforced as a guard (a guard would be red on day 1).

Status: the gameObjects rule holds today (0 violations).
See docs/spec/architecture_invariants.md (INV-3).
"""

from __future__ import annotations

from tests.architecture._arch import parse, py_files, rel, top_level_imports

FORBIDDEN_FOR_GAMEOBJECTS = {"gameMechanic", "uiLayout"}


def test_gameobjects_does_not_depend_on_outer_layers() -> None:
    violations = []
    for path in py_files("gameObjects"):
        leaked = top_level_imports(parse(path)) & FORBIDDEN_FOR_GAMEOBJECTS
        if leaked:
            violations.append(f"{rel(path)} imports {sorted(leaked)}")
    assert not violations, (
        "gameObjects/ is the foundation layer and must not import "
        "gameMechanic/ or uiLayout/:\n" + "\n".join(violations)
    )
