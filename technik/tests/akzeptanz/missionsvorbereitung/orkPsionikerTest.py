"""MIV-2 · Ork-Psioniker."""


def testMiv2_1DieArmeeDerOrksHatEineEinheitWeirdboyAusEinemModell(ausgangslage):
    armeeDerOrks = ausgangslage.ersterSpieler.armee
    weirdboys = [einheit for einheit in armeeDerOrks.einheiten if einheit.name == "Weirdboy"]

    (weirdboy,) = weirdboys
    assert len(weirdboy.modelle) == 1
