"""Parse-Funktion des mypy-Ratchet-Gates (Plan 038).

Der Subprozess-Aufruf selbst (mypy braucht ~20-30s) wird bewusst NICHT
getestet — nur die reine Parse-Logik gegen die drei bekannten mypy-
Ausgabeformen.
"""

import pytest

from tools.mypy_gate import parse_error_count


def test_parse_error_count_from_found_errors_line():
    output = (
        "src/foo.py:1: error: Something bad  [arg-type]\n"
        "Found 134 errors in 25 files (checked 43 source files)\n"
    )
    assert parse_error_count(output) == 134


def test_parse_error_count_singular_file_and_error():
    output = "Found 1 error in 1 file (checked 43 source files)\n"
    assert parse_error_count(output) == 1


def test_parse_error_count_success_is_zero():
    output = "Success: no issues found in 43 source files\n"
    assert parse_error_count(output) == 0


def test_parse_error_count_unrecognized_output_raises():
    with pytest.raises(ValueError):
        parse_error_count("mypy: error: config file not found\n")


def test_parse_error_count_empty_output_raises():
    with pytest.raises(ValueError):
        parse_error_count("")
