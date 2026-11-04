"""MIV-3 · Canoptek-Spinne."""


def einheitenDerAusgangslage(ausgangslage):
    return [
        einheit
        for spieler in (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
        for einheit in spieler.armee.einheiten
    ]


def testMiv3_1DieArmeeDerNecronsHatEineEinheitCanoptekSpyderAusEinemModell(ausgangslage):
    armeeDerNecrons = ausgangslage.zweiterSpieler.armee
    spinnen = [
        einheit for einheit in armeeDerNecrons.einheiten if einheit.name == "Canoptek Spyder"
    ]

    (spinne,) = spinnen
    assert len(spinne.modelle) == 1


def testMiv3_2DieEinheitCanoptekSpyderHatFliegen(ausgangslage):
    einheiten = einheitenDerAusgangslage(ausgangslage)

    (spinne,) = (einheit for einheit in einheiten if einheit.name == "Canoptek Spyder")

    assert spinne.fliegen is True


def testMiv3_2KeineAndereEinheitDerAusgangslageHatFliegen(ausgangslage):
    einheiten = einheitenDerAusgangslage(ausgangslage)

    andereMitFliegen = [
        einheit.name
        for einheit in einheiten
        if einheit.name != "Canoptek Spyder" and einheit.fliegen
    ]

    assert andereMitFliegen == []
