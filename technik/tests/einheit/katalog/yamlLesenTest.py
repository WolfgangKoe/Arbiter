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
        "yes: 1\ntrue: 2\n",
        "1: a\n0x1: b\n",
        "? [a, b]\n: 1\n",
        "? {a: 1}\n: 1\n",
    ],
    ids=[
        "zweimal",
        "zweimalTiefer",
        "zweimalInListe",
        "anker",
        "verweisAufZahl",
        "verweisAufMap",
        "wahrheitswerte",
        "zahlen",
        "listeAlsSchlüssel",
        "abbildungAlsSchlüssel",
    ],
)
def testEinDoppelterSchlüsselEinAnkerEinVerweisOderEinSchlüsselKeinTextIstEinFehler(text):
    with pytest.raises(ValueError):
        yamlPrüfen(text, "probe.yaml")
