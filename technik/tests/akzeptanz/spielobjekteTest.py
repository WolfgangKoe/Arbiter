"""OBJ-1 · Armeen und Spielfeld."""


def testObj1_1JederSpielerFührtEineArmeeMitEinheiten(ausgangslage):
    ersterSpieler, zweiterSpieler = ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler

    einheitenDerSpieler = [ersterSpieler.armee.einheiten, zweiterSpieler.armee.einheiten]

    assert all(einheiten for einheiten in einheitenDerSpieler)


def testObj1_1DieZweiSpielerFührenVerschiedeneArmeen(ausgangslage):
    ersterSpieler, zweiterSpieler = ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler

    assert ersterSpieler.armee is not zweiterSpieler.armee


def testObj1_1KeineEinheitGehörtZuBeidenArmeen(ausgangslage):
    ersterSpieler, zweiterSpieler = ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler

    gemeinsameEinheiten = [
        einheit
        for einheit in ersterSpieler.armee.einheiten
        if einheit in zweiterSpieler.armee.einheiten
    ]

    assert gemeinsameEinheiten == []
