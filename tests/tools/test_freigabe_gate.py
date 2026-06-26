"""Freigabe-Gate decision (PreToolUse hook): edits allowed iff marker exists,
except mailbox writes under ``docs/handoff/`` which bypass the gate."""

from tools.freigabe_gate import HANDOFF_DIR, REPO_ROOT, is_allowed, is_exempt


def test_edit_blocked_when_marker_absent(tmp_path):
    assert is_allowed(tmp_path / ".freigabe") is False


def test_edit_allowed_when_marker_present(tmp_path):
    marker = tmp_path / ".freigabe"
    marker.touch()
    assert is_allowed(marker) is True


def test_handoff_mailbox_write_is_exempt():
    assert is_exempt(str(HANDOFF_DIR / "plan-025-step4.md")) is True


def test_handoff_directory_itself_is_exempt():
    assert is_exempt(str(HANDOFF_DIR)) is True


def test_code_path_is_not_exempt():
    assert is_exempt(str(REPO_ROOT / "src" / "app.py")) is False


def test_missing_file_path_is_not_exempt():
    assert is_exempt(None) is False
