import pytest

from arbiter.domaene.sperre import Grund, Sperre


def testEineSperreIstNichtÜbergehbarOhneAngabe():
    assert Sperre(Grund.überEineBase).übergehbar is False


def testEineÜbergehbareSperreBleibtÜbergehbar():
    assert Sperre(Grund.überEineBase, Grund.baseÜberdeckt, übergehbar=True).übergehbar is True


@pytest.mark.parametrize("weitere", [(), (Grund.überEineBase,)])
def testKeineKohärenzIstNieÜbergehbar(weitere):
    assert Sperre(Grund.keineKohärenz, *weitere, übergehbar=True).übergehbar is False
