import pytest

from arbiter.domaene.spielobjekte import Base


@pytest.fixture
def zehnZoll() -> Base:
    return Base(durchmesser=254)
