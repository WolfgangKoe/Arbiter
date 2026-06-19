"""Freigabe-Gate decision (PreToolUse hook): edits allowed iff marker exists."""

from tools.freigabe_gate import is_allowed


def test_edit_blocked_when_marker_absent(tmp_path):
    assert is_allowed(tmp_path / ".freigabe") is False


def test_edit_allowed_when_marker_present(tmp_path):
    marker = tmp_path / ".freigabe"
    marker.touch()
    assert is_allowed(marker) is True
