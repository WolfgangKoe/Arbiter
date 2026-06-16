"""Correlation gate: docs/spec/acceptance/index.md  <->  tests/acceptance/.

Keeps the acceptance spec and the tests in lockstep. A criterion documented but
not pinned by a test (or a test pinning an undocumented criterion) is a drift and
fails the build. See docs/spec/acceptance/README.md.
"""

from __future__ import annotations

from tests.acceptance import _acceptance


def test_spec_has_at_least_one_ac() -> None:
    assert _acceptance.spec_ac_ids(), "Acceptance index is empty — add the first AC to index.md."


def test_every_spec_ac_has_a_pinning_test() -> None:
    missing = sorted(_acceptance.spec_ac_ids() - set(_acceptance.tested_ac_ids()))
    assert not missing, (
        "Acceptance criteria documented in index.md but pinned by no test "
        f"(@acceptance(...)): {missing}"
    )


def test_every_tested_ac_is_documented() -> None:
    tested = _acceptance.tested_ac_ids()
    orphan = sorted(set(tested) - _acceptance.spec_ac_ids())
    assert (
        not orphan
    ), "Tests reference AC-IDs absent from docs/spec/acceptance/index.md: " + ", ".join(
        f"{ac} ({tested[ac]})" for ac in orphan
    )
