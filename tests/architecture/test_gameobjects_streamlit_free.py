"""Guard: the data layer (gameObjects/) must never import Streamlit.

gameObjects/ holds pure dataclasses + the YAML loader. Keeping it Streamlit-free
means it can be imported and tested without a Streamlit runtime, and guarantees
the "what things are" layer carries no "how things look" concern.

Status: holds today (0 violations). See docs/spec/architecture_invariants.md (INV-1).
"""

from __future__ import annotations

from tests.architecture._arch import parse, py_files, rel, top_level_imports


def test_gameobjects_has_no_streamlit_import() -> None:
    offenders = [
        rel(path)
        for path in py_files("gameObjects")
        if "streamlit" in top_level_imports(parse(path))
    ]
    assert not offenders, (
        "gameObjects/ must stay Streamlit-free (pure data layer). "
        f"Streamlit imported in: {offenders}"
    )
