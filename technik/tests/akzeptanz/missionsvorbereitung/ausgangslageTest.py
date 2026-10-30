"""MIV-1 · Ausgangslage."""

from fractions import Fraction

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Grund
from tests.akzeptanz.handgriffe import profileDerModelle, sperrgründe, yamlAusDenDaten


def modelleDerArmeen(ausgangslage):
    return [modell for einheit in einheitenDerArmeen(ausgangslage) for modell in einheit.modelle]


def einheitenDerArmeen(ausgangslage):
    return [
        einheit
        for spieler in (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
        for einheit in spieler.armee.einheiten
    ]


def armeenAusDenDaten() -> list[list[dict]]:
    return yamlAusDenDaten("ausgangslage.yaml")["Armee"]


def einheitenAusDenDaten(*schlüssel: str) -> list:
    return sorted(
        sorted(
            (
                eintrag["datenblatt"],
                sorted(
                    (modellart, *(profil[name] for name in schlüssel))
                    for modellart, profil in profileDerModelle(eintrag)
                ),
            )
            for eintrag in armee
        )
        for armee in armeenAusDenDaten()
    )


def einheitenDerAusgangslage(ausgangslage, *merkmale) -> list:
    return sorted(
        sorted(
            (
                einheit.name,
                sorted(
                    (modell.modellart, *(merkmal(modell) for merkmal in merkmale))
                    for modell in einheit.modelle
                ),
            )
            for einheit in spieler.armee.einheiten
        )
        for spieler in (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
    )


def bewegungsweiteDes(modell):
    return modell.bewegungsweite


def durchmesserDes(modell):
    return modell.base.durchmesser


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
    datenblätterJeArmee = sorted(
        sorted(eintrag["datenblatt"] for eintrag in armee) for armee in armeenAusDenDaten()
    )
    namenJeArmee = sorted(
        sorted(einheit.name for einheit in spieler.armee.einheiten)
        for spieler in (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
    )

    assert namenJeArmee == datenblätterJeArmee


def testMiv1_5JedeEinheitHatJeModellartSoVieleModelleWieDortSteht(ausgangslage):
    erwartet = einheitenAusDenDaten()
    modellartenJeEinheit = einheitenDerAusgangslage(ausgangslage)

    assert modellartenJeEinheit == erwartet


def testMiv1_5JedesModellHatDieBewegungsweiteSeinerModellartImDatenblatt(ausgangslage):
    erwartet = einheitenAusDenDaten("bewegungsweite")
    bewegungsweitenJeEinheit = einheitenDerAusgangslage(ausgangslage, bewegungsweiteDes)

    assert bewegungsweitenJeEinheit == erwartet


def testMiv1_5JedesModellHatEineBaseMitDemDurchmesserSeinerModellart(ausgangslage):
    erwartet = einheitenAusDenDaten("durchmesser")
    durchmesserJeEinheit = einheitenDerAusgangslage(ausgangslage, durchmesserDes)

    assert durchmesserJeEinheit == erwartet
