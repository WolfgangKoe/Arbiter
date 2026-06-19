"""Pytest-detection for the token-report reminder (PostToolUse hook)."""

from tools.test_report_reminder import is_pytest_call


def test_detects_pytest_command():
    assert is_pytest_call({"tool_input": {"command": "pytest --tb=short"}}) is True


def test_detects_python_m_pytest():
    assert is_pytest_call({"tool_input": {"command": "python -m pytest tests/"}}) is True


def test_ignores_non_pytest_command():
    assert is_pytest_call({"tool_input": {"command": "git status"}}) is False


def test_ignores_missing_command():
    assert is_pytest_call({}) is False
