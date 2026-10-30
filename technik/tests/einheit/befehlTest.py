import pytest

from arbiter.__main__ import festerPort, portDesBefehls


def testOhneAngabeGiltDerFestePort():
    assert portDesBefehls([]) == festerPort


@pytest.mark.parametrize("port", [0, 65535])
def testMitPortGiltDieAngabe(port):
    assert portDesBefehls(["--port", str(port)]) == port


@pytest.mark.parametrize("port", ["-1", "65536", "70000"])
def testEinPortAußerhalbDesPortbereichsWirdAbgelehnt(port):
    with pytest.raises(SystemExit):
        portDesBefehls(["--port", port])
