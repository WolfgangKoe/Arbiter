import pytest

from arbiter.domaene.spielobjekte import Base


@pytest.fixture
def zehnZoll() -> Base:
    # Warum: 254 mm sind 10″, der Durchmesser 254 mm hat den Radius 5″
    return Base(durchmesser=254)
