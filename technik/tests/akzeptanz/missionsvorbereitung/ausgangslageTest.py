"""MIV-1 · Ausgangslage."""

from fractions import Fraction

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Grund
from tests.akzeptanz.handgriffe import profileDerModelle, sperrgründe, yamlAusDenDaten


def modelleDerArmeen(ausgangslage):
    return [modell for einheit in einheitenDerArmeen(ausgangslage) for modell in einheit.modelle]


def spielerDer(ausgangslage):
    return (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)


def einheitenDerArmeen(ausgangslage):
    return [einheit for spieler in spielerDer(ausgangslage) for einheit in spieler.armee.einheiten]


def armeenAusDenDaten() -> list[list[dict]]:
    return yamlAusDenDaten("ausgangslage.yaml")["Armee"]


def bewegungsweiteDes(modell):
    return modell.bewegungsweite


def durchmesserDes(modell):
    return modell.base.durchmesser


merkmalZumSchlüssel = {"bewegungsweite": bewegungsweiteDes, "durchmesser": durchmesserDes}


def ohneReihenfolge(wert):
    if isinstance(wert, list):
        return sorted(ohneReihenfolge(element) for element in wert)
    if isinstance(wert, tuple):
        return tuple(ohneReihenfolge(element) for element in wert)
    return wert


def namenJeArmee(armeen: list) -> list[list[str]]:
    return [[name for name, _ in armee] for armee in armeen]


def einheitenAusDenDaten(*schlüssel: str) -> list:
    return [
        [
            (
                eintrag["datenblatt"],
                [
                    (modellart, *(profil[name] for name in schlüssel))
                    for modellart, profil in profileDerModelle(eintrag)
                ],
            )
            for eintrag in armee
        ]
        for armee in armeenAusDenDaten()
    ]


def einheitenDerAusgangslage(ausgangslage, *schlüssel: str) -> list:
    merkmale = [merkmalZumSchlüssel[name] for name in schlüssel]
    return [
        [
            (
                einheit.name,
                [
                    (modell.modellart, *(merkmal(modell) for merkmal in merkmale))
                    for modell in einheit.modelle
                ],
            )
            for einheit in spieler.armee.einheiten
        ]
        for spieler in spielerDer(ausgangslage)
    ]


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


def testMiv1_4DasSpielfeldHatDieSeitenlängenAusOnlyWar(ausgangslage):
    seitenlängen = ausgangslage.spielfeld.seitenlängen

    assert seitenlängen == (Fraction(44), Fraction(60))


def testMiv1_5DieAusgangslageHatDieZweiArmeenMitIhrenEinheiten(ausgangslage):
    datenblätterJeArmee = ohneReihenfolge(namenJeArmee(einheitenAusDenDaten()))

    einheitennamenJeArmee = ohneReihenfolge(namenJeArmee(einheitenDerAusgangslage(ausgangslage)))

    assert einheitennamenJeArmee == datenblätterJeArmee


def testMiv1_5JedeEinheitHatJeModellartSoVieleModelleWieDortSteht(ausgangslage):
    erwartet = ohneReihenfolge(einheitenAusDenDaten())

    modellartenJeEinheit = ohneReihenfolge(einheitenDerAusgangslage(ausgangslage))

    assert modellartenJeEinheit == erwartet


def testMiv1_5JedesModellHatDieBewegungsweiteSeinerModellartImDatenblatt(ausgangslage):
    erwartet = ohneReihenfolge(einheitenAusDenDaten("bewegungsweite"))

    bewegungsweitenJeEinheit = ohneReihenfolge(
        einheitenDerAusgangslage(ausgangslage, "bewegungsweite")
    )

    assert bewegungsweitenJeEinheit == erwartet


def testMiv1_5JedesModellHatEineBaseMitDemDurchmesserSeinerModellart(ausgangslage):
    erwartet = ohneReihenfolge(einheitenAusDenDaten("durchmesser"))

    durchmesserJeEinheit = ohneReihenfolge(einheitenDerAusgangslage(ausgangslage, "durchmesser"))

    assert durchmesserJeEinheit == erwartet
