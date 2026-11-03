from arbiter.domaene.sperre import Grund, Sperre


def testEineSperreNenntIhreGründeAlsText():
    sperre = Sperre(Grund.baseÜberdeckt, Grund.nahkampfreichweite)

    assert sperre.gründe == {Grund.baseÜberdeckt, Grund.nahkampfreichweite}
    assert str(sperre) == "Base überdeckt, Nahkampfreichweite"
