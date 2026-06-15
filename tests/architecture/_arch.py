"""Shared helpers for the architecture-conformance guards.

These guards read the source tree from disk (via ``ast`` + filesystem) and never
import ``src/`` modules. That keeps them runnable under the canonical
``pytest --tb=short`` regardless of how ``src`` happens to be on ``sys.path``,
and makes them immune to import-time side effects (Streamlit, session_state).

Invariant catalogue + status table: ``docs/spec/architecture_invariants.md``.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "src"


def py_files(*subdirs: str) -> list[Path]:
    """All ``*.py`` files under ``src`` (or a subpackage), excluding caches."""
    root = SRC.joinpath(*subdirs) if subdirs else SRC
    return sorted(p for p in root.rglob("*.py") if "__pycache__" not in p.parts)


def rel(path: Path) -> str:
    """Path relative to ``src``, posix-style — used as allowlist key."""
    return path.relative_to(SRC).as_posix()


def parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def top_level_imports(tree: ast.Module) -> set[str]:
    """Top-level package names imported by a module (absolute imports only)."""
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def docstring_node_ids(tree: ast.Module) -> set[int]:
    """ids() of the string-constant nodes that are module/class/function docstrings.

    Used to exclude documentation prose from string-literal scans — a faction
    name in an explanatory docstring is fine; a faction name in a value is not.
    """
    ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(
            node,
            ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
        ):
            if ast.get_docstring(node, clean=False) is not None:
                ids.add(id(node.body[0].value))  # type: ignore[attr-defined]
    return ids


def string_constants(tree: ast.Module) -> list[ast.Constant]:
    """Non-docstring ``str`` constants in a module, with line numbers."""
    skip = docstring_node_ids(tree)
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip
    ]
