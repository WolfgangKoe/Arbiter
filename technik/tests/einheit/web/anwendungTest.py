from fractions import Fraction
from http import HTTPStatus

import pytest

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.domaene.spielobjekte import Stelle
from arbiter.web.anwendung import anwendungFür
from tests.akzeptanz.handgriffe import alleEinheitenAufstellen, aufstellungVon, spielerMit

pfadDerAuswahl = "/api/spieler/{}/einheiten/{}/ausgewählt"
pfadDerAbfrage = "/api/spieler/{}/einheiten/{}/modelle/{}/stelleBeimLoslassen"


@pytest.fixture
def aufstellung():
    return aufstellungVon(spielerMit(1, 1), spielerMit(1, 1))


@pytest.mark.parametrize(("spielernummer", "einheitennummer"), [(0, 1), (3, 1), (1, 0), (1, 3)])
@pytest.mark.parametrize("methode", ["put", "delete"])
def testEinPfadOhneEinheitInDerArmeelisteIstNichtGefunden(
    aufstellung, spielernummer, einheitennummer, methode
):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = getattr(dienst, methode)(pfadDerAuswahl.format(spielernummer, einheitennummer))

    assert antwort.status_code == HTTPStatus.NOT_FOUND


def testEineAufgestellteEinheitIstNichtMehrInDerArmeelisteUndNichtGefunden(aufstellung):
    aufstellung.gewinnerWählen(aufstellung.ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    alleEinheitenAufstellen(aufstellung)
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put(pfadDerAuswahl.format(1, 1))

    assert antwort.status_code == HTTPStatus.NOT_FOUND


pfadDesModells = "/api/spieler/{}/einheiten/{}/modelle/{}/stelle"
eineStelle = {"x": 3, "y": 20}


@pytest.mark.parametrize(
    ("spielernummer", "einheitennummer", "modellnummer"), [(3, 1, 1), (1, 3, 1), (1, 1, 3)]
)
def testEinModellOhneKennungIstNichtGefunden(
    aufstellung, spielernummer, einheitennummer, modellnummer
):
    dienst = anwendungFür(aufstellung).test_client()
    pfad = pfadDesModells.format(spielernummer, einheitennummer, modellnummer)

    antwort = dienst.put(pfad, json=eineStelle)

    assert antwort.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("körper", [None, {}, {"x": 3}, {"x": "3", "y": 2}, {"x": True, "y": 2}])
def testEinModellOhneZahlenFürXUndYIstEineFehlerhafteAnfrage(aufstellung, körper):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put(pfadDesModells.format(1, 1, 1), json=körper)

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "abfrage",
    [{}, {"x": 3}, {"y": 2}, {"x": "a", "y": 2}, {"x": 3, "y": ""}, {"x": "NaN", "y": 2}]
    + [{"x": "1_0", "y": 2}, {"x": " 3 ", "y": 2}, {"x": "true", "y": 2}, {"x": "[" * 999, "y": 2}]
    + [{"x": "1" * 5000, "y": 2}, {"x": "1٣", "y": 2}],
)
def testEineAbfrageDerStelleBeimLoslassenOhneZahlenFürXUndYIstEineFehlerhafteAnfrage(
    aufstellung, abfrage
):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.get(pfadDerAbfrage.format(1, 1, 1), query_string=abfrage)

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("zahl", ["NaN", "Infinity", "-Infinity"])
def testEineStelleMitUnendlicherOderUnbestimmterZahlIstEineFehlerhafteAnfrage(aufstellung, zahl):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put(
        "/api/karteAnklicken", data=f'{{"x": {zahl}, "y": 2}}', content_type="application/json"
    )

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


def testEineSehrGroßeGanzeZahlIstEineFehlerhafteAnfrageUndLässtDenSpielstandLesbar(aufstellung):
    aufstellung.gewinnerWählen(aufstellung.ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    dienst = anwendungFür(aufstellung).test_client()
    dienst.put(pfadDerAuswahl.format(2, 1))
    groß = "1" + "0" * 400

    antwort = dienst.put(
        pfadDesModells.format(2, 1, 1),
        data=f'{{"x": 3, "y": {groß}}}',
        content_type="application/json",
    )

    assert antwort.status_code == HTTPStatus.BAD_REQUEST
    assert dienst.get("/api/spielstand").status_code == HTTPStatus.OK


def stellenAbfangen(aufstellung, monkeypatch, aufruf):
    stellen = []
    echte = getattr(aufstellung, aufruf)

    def abfangen(modell, stelle):
        stellen.append(stelle)
        return echte(modell, stelle)

    monkeypatch.setattr(aufstellung, aufruf, abfangen)
    return stellen


def testEineGleitkommazahlKommtImKörperAlsBruchMitKleinemNennerInDieDomäne(
    aufstellung, monkeypatch
):
    stellen = stellenAbfangen(aufstellung, monkeypatch, "modellLoslassen")
    dienst = anwendungFür(aufstellung).test_client()

    dienst.put(pfadDesModells.format(1, 1, 1), json={"x": 160 / 127, "y": 121 / 3})

    assert stellen == [Stelle(x=Fraction(160, 127), y=Fraction(121, 3))]


def testEineGleitkommazahlKommtInDerAbfrageAlsBruchMitKleinemNennerInDieDomäne(
    aufstellung, monkeypatch
):
    stellen = stellenAbfangen(aufstellung, monkeypatch, "stellenBeimLoslassen")
    dienst = anwendungFür(aufstellung).test_client()

    dienst.get(pfadDerAbfrage.format(1, 1, 1), query_string={"x": 160 / 127, "y": 121 / 3})

    assert stellen == [Stelle(x=Fraction(160, 127), y=Fraction(121, 3))]


def testEinKlickAufDieKarteOhneZahlenFürXUndYIstEineFehlerhafteAnfrage(aufstellung):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.put("/api/karteAnklicken", json={"y": 2})

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


def testEinFremderHostBekommtBadRequest(aufstellung):
    dienst = anwendungFür(aufstellung).test_client()

    antwort = dienst.get("/api/spielstand", headers={"Host": "fremd.example"})

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


pfadDerEbene = "/api/spieler/{}/einheiten/{}/modelle/{}/ebene"


@pytest.mark.parametrize("methode", ["put", "delete"])
def testEineEbeneOhneGesetztesModellDerAusgewähltenEinheitIstNichtGefunden(aufstellung, methode):
    aufstellung.gewinnerWählen(aufstellung.ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    dienst = anwendungFür(aufstellung).test_client()
    pfad = pfadDerEbene.format(1, 1, 1)

    ohneAuswahl = getattr(dienst, methode)(pfad)
    dienst.put(pfadDerAuswahl.format(1, 1))
    ohneGesetztesModell = getattr(dienst, methode)(pfad)

    assert ohneAuswahl.status_code == HTTPStatus.NOT_FOUND
    assert ohneGesetztesModell.status_code == HTTPStatus.NOT_FOUND


pfadDesErstenZugs = "/api/spieler/{}/ersterZug"
pfadPhaseBeenden = "/api/phaseBeenden"
kommandophaseVonSpielerEins = {"schlachtrunde": 1, "spieler": 1, "phase": "Kommandophase"}


@pytest.fixture
def dienstNachDerAufstellung(aufstellung):
    aufstellung.gewinnerWählen(aufstellung.ausgangslage.ersterSpieler)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    alleEinheitenAufstellen(aufstellung)
    return anwendungFür(aufstellung).test_client()


def testSchlachtHandlungenSindVorDemEndeDerAufstellungNichtGefunden(aufstellung):
    dienst = anwendungFür(aufstellung).test_client()

    ersterZug = dienst.put(pfadDesErstenZugs.format(1))
    phaseBeenden = dienst.put(pfadPhaseBeenden, json=kommandophaseVonSpielerEins)

    assert ersterZug.status_code == HTTPStatus.NOT_FOUND
    assert phaseBeenden.status_code == HTTPStatus.NOT_FOUND
    assert "schlacht" not in dienst.get("/api/spielstand").get_json()


@pytest.mark.parametrize("spielernummer", [0, 3])
def testEinUnbekannterSpielerKannDenErstenZugNichtHaben(dienstNachDerAufstellung, spielernummer):
    antwort = dienstNachDerAufstellung.put(pfadDesErstenZugs.format(spielernummer))

    assert antwort.status_code == HTTPStatus.NOT_FOUND


def testDerErsteZugÄndertSichNichtBeimZweitenKlick(dienstNachDerAufstellung):
    dienstNachDerAufstellung.put(pfadDesErstenZugs.format(1))

    antwort = dienstNachDerAufstellung.put(pfadDesErstenZugs.format(2))

    assert antwort.get_json()["schlacht"]["ersterZug"] == 1


@pytest.mark.parametrize(
    "körper",
    [
        None,
        [],
        {"spieler": 1, "phase": "Kommandophase"},
        {"schlachtrunde": 1, "phase": "Kommandophase"},
        {"schlachtrunde": True, "spieler": 1, "phase": "Kommandophase"},
        {"schlachtrunde": 1, "spieler": 1.5, "phase": "Kommandophase"},
        {"schlachtrunde": 1, "spieler": 1},
        {"schlachtrunde": 1, "spieler": 1, "phase": "Spielphase"},
        {"schlachtrunde": 1, "spieler": 1, "phase": ["Kommandophase"]},
    ],
)
def testPhaseBeendenMitUnvollständigemKörperIstEineFalscheAnfrage(dienstNachDerAufstellung, körper):
    dienstNachDerAufstellung.put(pfadDesErstenZugs.format(1))

    antwort = dienstNachDerAufstellung.put(pfadPhaseBeenden, json=körper)

    assert antwort.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "körper",
    [
        {"schlachtrunde": 2, "spieler": 1, "phase": "Kommandophase"},
        {"schlachtrunde": 1, "spieler": 2, "phase": "Kommandophase"},
        {"schlachtrunde": 1, "spieler": 1, "phase": "Bewegungsphase"},
    ],
)
def testPhaseBeendenMitFremdemStandÄndertNichts(dienstNachDerAufstellung, körper):
    dienstNachDerAufstellung.put(pfadDesErstenZugs.format(1))
    davor = dienstNachDerAufstellung.get("/api/spielstand").get_json()

    antwort = dienstNachDerAufstellung.put(pfadPhaseBeenden, json=körper)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == davor
