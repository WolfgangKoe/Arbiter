"""Guard: only the loader may read YAML.

All army data flows through gameObjects/loader.py. No other module imports the
``yaml`` package or opens a ``.yaml``/``.yml`` file directly — that keeps the
single-entry-point contract intact and prevents ad-hoc data access scattered
across the codebase.

Status: holds today (0 violations). See docs/spec/architecture_invariants.md (INV-2).
"""

from __future__ import annotations

import ast

from tests.architecture._arch import parse, py_files, rel, top_level_imports

# file (relative to src/) -> reason it may touch YAML directly.
YAML_ALLOWED: dict[str, str] = {
    # Single read entry point for all army/catalog data.
    "gameObjects/loader.py": "loader: reads all game data",
    # .rosz -> roster YAML converter: only *writes* the converted roster via
    # yaml.dump; reading the catalog still goes through loader.load_unit_catalog.
    "gameObjects/roszImporter.py": "rosz importer: writes converted rosters",
}


def _opens_yaml_path(tree: ast.Module) -> bool:
    """True if the module calls ``open(...)`` on a literal .yaml/.yml path."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
            continue
        if node.func.id != "open" or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            if first.value.endswith((".yaml", ".yml")):
                return True
    return False


def test_yaml_access_is_confined_to_loader() -> None:
    offenders = []
    for path in py_files():
        if rel(path) in YAML_ALLOWED:
            continue
        tree = parse(path)
        if "yaml" in top_level_imports(tree) or _opens_yaml_path(tree):
            offenders.append(rel(path))
    assert not offenders, (
        "YAML access must go through the loader (single read entry point). "
        f"Unexpected direct YAML access in: {offenders}. "
        f"If legitimate, add to YAML_ALLOWED with a reason. "
        f"Currently allowed: {sorted(YAML_ALLOWED)}"
    )
