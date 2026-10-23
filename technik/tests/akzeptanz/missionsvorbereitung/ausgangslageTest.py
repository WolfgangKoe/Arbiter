"""MIV-1 · Ausgangslage."""

from fractions import Fraction

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Grund
from tests.akzeptanz.handgriffe import durchmesserJeEinheit, sperrgründe


def modelleDerArmeen(ausgangslage):
    return [modell for einheit in einheitenDerArmeen(ausgangslage) for modell in einheit.modelle]


def einheitenDerArmeen(ausgangslage):
    return [
        einheit
        for spieler in (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
        for einheit in spieler.armee.einheiten
    ]


def durchmesserDerArmeen(ausgangslage) -> list[tuple[tuple[int, ...], ...]]:
    return sorted(
        [
            durchmesserJeEinheit(ausgangslage.ersterSpieler),
            durchmesserJeEinheit(ausgangslage.zweiterSpieler),
        ]
    )


def testMiv1_1EineBaseAnDerTiefeDerZoneLiegtGanzInDerZone(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    stelle = platz.stelle(platz.tiefeDerZone - platz.radius, 10)

    aufstellung.modellSetzen(erstesModell, stelle)

    assert aufstellung.gesetzt(erstesModell)


def testMiv1_1EineBaseJenseitsDerTiefeLiegtNichtGanzInDerZone(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    stelle = platz.stelle(platz.tiefeDerZone - platz.radius + platz.millionstel, 10)

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone}
    assert not aufstellung.gesetzt(erstesModell)


def testMiv1_1DieZoneBeginntAmAnfangDerSpielfeldkante(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    stelle = platz.stelle(platz.radius, platz.radius)

    aufstellung.modellSetzen(erstesModell, stelle)

    assert aufstellung.gesetzt(erstesModell)


def testMiv1_1DieZoneReichtBisZumEndeDerSpielfeldkante(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    stelle = platz.stelle(platz.radius, platz.längeDerSpielfeldkante - platz.radius)

    aufstellung.modellSetzen(erstesModell, stelle)

    assert aufstellung.gesetzt(erstesModell)


def testMiv1_2InDerAusgangslageIstKeinModellGesetzt(ausgangslage):
    aufstellung = Aufstellung(ausgangslage)
    modelle = modelleDerArmeen(ausgangslage)

    gesetzteModelle = [modell for modell in modelle if aufstellung.gesetzt(modell)]

    assert gesetzteModelle == []


def testMiv1_2InDerAusgangslageIstKeineEinheitAufgestellt(ausgangslage):
    aufstellung = Aufstellung(ausgangslage)
    einheiten = einheitenDerArmeen(ausgangslage)

    aufgestellteEinheiten = [einheit for einheit in einheiten if aufstellung.aufgestellt(einheit)]

    assert aufgestellteEinheiten == []


def testMiv1_3DieAusgangslageHatDieZweiArmeenMitJeZweiEinheiten(ausgangslage):
    einheitenJeArmee = [
        len(ausgangslage.ersterSpieler.armee.einheiten),
        len(ausgangslage.zweiterSpieler.armee.einheiten),
    ]

    assert einheitenJeArmee == [2, 2]


def testMiv1_3JederEintragUnterDurchmesserIstEinModellDerEinheit(ausgangslage):
    zahlenDerModelle = sorted(
        tuple(len(einheit.modelle) for einheit in spieler.armee.einheiten)
        for spieler in (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
    )

    assert zahlenDerModelle == [(10, 1), (10, 1)]


def testMiv1_3DieBaseJedesModellsHatDenDurchmesserDesEintrags(ausgangslage):
    orks = ((32,) * 10, (40,))
    necrons = ((32,) * 10, (32,))

    durchmesser = durchmesserDerArmeen(ausgangslage)

    assert durchmesser == sorted([orks, necrons])


def testMiv1_4DasSpielfeldHatDieSeitenlängenAusOnlyWar(ausgangslage):
    seitenlängen = ausgangslage.spielfeld.seitenlängen

    assert seitenlängen == (Fraction(44), Fraction(60))
