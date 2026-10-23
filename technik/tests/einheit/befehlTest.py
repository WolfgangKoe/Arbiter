from arbiter.__main__ import festerPort, portDesBefehls


def testOhneAngabeGiltDerFestePort():
    assert portDesBefehls([]) == festerPort


def testMitPortGiltDieAngabe():
    assert portDesBefehls(["--port", "0"]) == 0
