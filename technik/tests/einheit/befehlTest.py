import pytest

from arbiter.__main__ import festerPort, portDesBefehls


def testOhneAngabeGiltDerFestePort():
    assert portDesBefehls([]) == festerPort


def testMitPortGiltDieAngabe():
    assert portDesBefehls(["--port", "0"]) == 0


@pytest.mark.parametrize("port", ["-1", "65536", "70000"])
def testEinPortAußerhalbDesPortbereichsWirdAbgelehnt(port):
    with pytest.raises(SystemExit):
        portDesBefehls(["--port", port])
