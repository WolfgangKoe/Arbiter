"""Guard (INV-6): pure HTML/SVG composition lives in a Streamlit-free, coverage-measured module.

Background — the recurring 'render edge had untested business logic → crash' pattern:
Badge-composition bugs and the Heroic-Intervention duplicate-key crash both hid in
render helpers that were bundled with Streamlit render functions and therefore excluded
from coverage measurement.  The fix was to separate the pure building blocks
(SVG faces, threshold headers, modifier rows, grid rows) into ``dice_compose.py`` —
measured at 100% — while only the three ``st.markdown`` wrapper functions remain in
the omitted ``dice_html.py``.

This guard locks in that seam with two assertions:

1. ``src/uiLayout/dice_compose.py`` imports no ``streamlit`` in any form (AST-checked).
   It is the pure composition layer; any accidental ``import streamlit`` or
   ``from streamlit import …`` would make it untestable without a Streamlit runtime.

2. ``src/uiLayout/dice_compose.py`` is NOT present in the ``[tool.coverage.run] omit``
   list in ``pyproject.toml``, and the list does NOT contain a bare ``src/uiLayout/*``
   wildcard.  A future blanket glob that re-swallows ``dice_compose.py`` into the omit
   set would silently remove the coverage safety net — this test fails it instead.

Status: holds today (0 violations). See docs/spec/architecture_invariants.md (INV-6).
"""

from __future__ import annotations

import tomllib
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
_PYPROJECT = _ROOT / "pyproject.toml"
_COMPOSE_MODULE = _SRC / "uiLayout" / "dice_compose.py"
_COMPOSE_REL = "src/uiLayout/dice_compose.py"


# ---------------------------------------------------------------------------
# Assertion 1 — dice_compose.py is Streamlit-free
# ---------------------------------------------------------------------------


def test_dice_compose_has_no_streamlit_import() -> None:
    """dice_compose.py must never import streamlit in any form.

    This is the pure-composition contract: all SVG/HTML building blocks must be
    importable and testable without a Streamlit runtime.  Any ``import streamlit``
    or ``from streamlit import …`` here defeats the entire seam.
    """
    import ast

    assert (
        _COMPOSE_MODULE.exists()
    ), f"{_COMPOSE_REL} does not exist — the pure composition module was removed or moved"
    source = _COMPOSE_MODULE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(_COMPOSE_MODULE))

    violations: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] == "streamlit":
                    violations.append(f"line {node.lineno}: import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] == "streamlit":
                violations.append(f"line {node.lineno}: from {node.module} import …")

    assert not violations, (
        f"{_COMPOSE_REL} must stay Streamlit-free (pure composition layer, INV-6). "
        f"Streamlit imports found:\n" + "\n".join(violations)
    )


# ---------------------------------------------------------------------------
# Assertion 2 — dice_compose.py is NOT in the coverage omit list
# ---------------------------------------------------------------------------


def test_dice_compose_is_coverage_measured() -> None:
    """dice_compose.py must remain in the coverage-measured set.

    The module must NOT appear in ``[tool.coverage.run] omit`` in pyproject.toml,
    and the omit list must NOT contain a bare ``src/uiLayout/*`` wildcard that
    would silently re-swallow it.  Either of those regressions would remove the
    coverage safety net that guards against untested composition logic.
    """
    data = tomllib.loads(_PYPROJECT.read_text(encoding="utf-8"))
    omit: list[str] = data.get("tool", {}).get("coverage", {}).get("run", {}).get("omit", [])

    # 2a — the module itself is not listed
    assert _COMPOSE_REL not in omit, (
        f"{_COMPOSE_REL} must NOT be in [tool.coverage.run] omit (INV-6). "
        "The pure composition layer must stay coverage-measured."
    )

    # 2b — no coarse wildcard that would swallow it
    assert "src/uiLayout/*" not in omit, (
        "pyproject.toml [tool.coverage.run] omit must NOT contain the bare "
        "'src/uiLayout/*' wildcard (INV-6). "
        "uiLayout files must be enumerated explicitly so dice_compose.py stays measured."
    )
