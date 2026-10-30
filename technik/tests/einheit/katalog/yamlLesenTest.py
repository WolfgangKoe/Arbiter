import pytest

from arbiter.katalog.yamlLesen import yamlLesen, yamlPrüfen


def testEineDateiOhneBesonderheitenWirdGelesen():
    assert yamlLesen("katalog", "orks", "datenblaetter.yaml")["Warboss"]


@pytest.mark.parametrize(
    "text",
    [
        "Boyz: 1\nBoyz: 2\n",
        "Orks:\n  Boyz: 1\n  Boyz: 2\n",
        "Liste:\n  - Boyz: 1\n    Boyz: 2\n",
        "Boyz: &boyz 1\n",
        "Boyz: &boyz 1\nGrots: *boyz\n",
        "Boyz: &boyz\n  Ork Boy: 1\nGrots: *boyz\n",
    ],
    ids=["zweimal", "zweimalTiefer", "zweimalInListe", "anker", "verweisAufZahl", "verweisAufMap"],
)
def testEinDoppelterSchlüsselEinAnkerOderEinVerweisIstEinFehler(text):
    with pytest.raises(ValueError):
        yamlPrüfen(text, "probe.yaml")
