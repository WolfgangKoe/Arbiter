"""AUF-1 · Reihenfolge der Aufstellung (domaene/anforderungen/phasen/aufstellen.md)."""

import pytest

from arbiter.domaene.armeen import Einheit, Spieler
from arbiter.domaene.aufstellung import Aufstellung, Aufstellungszone, Grund, Sperre

ZONE, ANDERE_ZONE = list(Aufstellungszone)


def nach_der_wahl(aufstellung: Aufstellung, gewinner: Spieler) -> None:
    aufstellung.gewinner_wählen(gewinner)
    aufstellung.aufstellungszone_wählen(ZONE)


def aufgestellt(aufstellung: Aufstellung, einheit: Einheit) -> None:
    """Wählt die Einheit, setzt alle ihre Modelle und beendet (Plan: keine Sperren beim Beenden)."""
    aufstellung.einheit_in_aufstellung_wählen(einheit)
    for modell in einheit.modelle:
        aufstellung.modell_setzen(modell)
    aufstellung.aufstellen_der_einheit_beenden()


def sperrgrund(aktion) -> Grund:
    with pytest.raises(Sperre) as fehler:
        aktion()
    return fehler.value.grund


# AUF-1.1

@pytest.mark.parametrize("zone", list(Aufstellungszone))
def test_auf_1_1_die_gewählte_aufstellungszone_gehört_dem_gewinner(aufstellung, a, b, zone):
    aufstellung.gewinner_wählen(a)
    aufstellung.aufstellungszone_wählen(zone)

    assert aufstellung.gewinner is a
    assert aufstellung.aufstellungszone(a) == zone


@pytest.mark.parametrize("zone", list(Aufstellungszone))
def test_auf_1_1_die_andere_aufstellungszone_gehört_dem_anderen_spieler(aufstellung, a, b, zone):
    aufstellung.gewinner_wählen(a)
    aufstellung.aufstellungszone_wählen(zone)

    assert aufstellung.aufstellungszone(b) != zone
    assert aufstellung.aufstellungszone(b) in Aufstellungszone


def test_auf_1_1_gewinner_kann_jeder_der_beiden_spieler_sein(aufstellung, a, b):
    aufstellung.gewinner_wählen(b)
    aufstellung.aufstellungszone_wählen(ZONE)

    assert aufstellung.gewinner is b
    assert aufstellung.aufstellungszone(b) == ZONE
    assert aufstellung.aufstellungszone(a) == ANDERE_ZONE


# AUF-1.2

def test_auf_1_2_erst_der_gewinner_dann_die_aufstellungszone_ist_erlaubt(aufstellung, a):
    aufstellung.gewinner_wählen(a)
    aufstellung.aufstellungszone_wählen(ZONE)


def test_auf_1_2_die_aufstellungszone_vor_dem_gewinner_ist_nicht_wählbar(aufstellung):
    grund = sperrgrund(lambda: aufstellung.aufstellungszone_wählen(ZONE))

    assert grund is Grund.NICHT_WÄHLBAR


def test_auf_1_2_nach_der_gesperrten_zone_ist_der_gewinner_noch_wählbar(aufstellung, a):
    with pytest.raises(Sperre):
        aufstellung.aufstellungszone_wählen(ZONE)

    aufstellung.gewinner_wählen(a)
    aufstellung.aufstellungszone_wählen(ZONE)

    assert aufstellung.aufstellungszone(a) == ZONE


def test_auf_1_2_der_gewinner_ein_zweites_mal_ist_nicht_wählbar(aufstellung, a, b):
    aufstellung.gewinner_wählen(a)

    grund = sperrgrund(lambda: aufstellung.gewinner_wählen(b))

    assert grund is Grund.NICHT_WÄHLBAR
    assert aufstellung.gewinner is a


def test_auf_1_2_derselbe_gewinner_ein_zweites_mal_ist_nicht_wählbar(aufstellung, a):
    aufstellung.gewinner_wählen(a)

    assert sperrgrund(lambda: aufstellung.gewinner_wählen(a)) is Grund.NICHT_WÄHLBAR


@pytest.mark.parametrize("zweite", list(Aufstellungszone))
def test_auf_1_2_die_aufstellungszone_ein_zweites_mal_ist_nicht_wählbar(aufstellung, a, zweite):
    aufstellung.gewinner_wählen(a)
    aufstellung.aufstellungszone_wählen(ZONE)

    grund = sperrgrund(lambda: aufstellung.aufstellungszone_wählen(zweite))

    assert grund is Grund.NICHT_WÄHLBAR
    assert aufstellung.aufstellungszone(a) == ZONE


# AUF-1.3

def test_auf_1_3_vor_der_wahl_ist_keiner_an_der_reihe(aufstellung):
    assert aufstellung.an_der_reihe is None


def test_auf_1_3_nach_der_wahl_ist_an_der_reihe_wer_nicht_gewinner_ist(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)

    assert aufstellung.an_der_reihe is b


def test_auf_1_3_ist_der_zweite_spieler_gewinner_ist_der_erste_an_der_reihe(aufstellung, a, b):
    nach_der_wahl(aufstellung, b)

    assert aufstellung.an_der_reihe is a


# AUF-1.4

def test_auf_1_4_ein_modell_der_einheit_in_aufstellung_lässt_sich_setzen(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    einheit = b.armee.einheiten[0]
    aufstellung.einheit_in_aufstellung_wählen(einheit)

    aufstellung.modell_setzen(einheit.modelle[0])

    assert einheit.modelle[0].gesetzt


def test_auf_1_4_ohne_einheit_in_aufstellung_ist_setzen_nicht_in_aufstellung(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    modell = b.armee.einheiten[0].modelle[0]

    assert sperrgrund(lambda: aufstellung.modell_setzen(modell)) is Grund.NICHT_IN_AUFSTELLUNG
    assert not modell.gesetzt


def test_auf_1_4_vor_der_wahl_ist_setzen_nicht_in_aufstellung(aufstellung, a):
    modell = a.armee.einheiten[0].modelle[0]

    assert sperrgrund(lambda: aufstellung.modell_setzen(modell)) is Grund.NICHT_IN_AUFSTELLUNG


def test_auf_1_4_ein_modell_einer_anderen_einheit_ist_nicht_in_aufstellung(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    aufstellung.einheit_in_aufstellung_wählen(b.armee.einheiten[0])
    fremdes = b.armee.einheiten[1].modelle[0]

    assert sperrgrund(lambda: aufstellung.modell_setzen(fremdes)) is Grund.NICHT_IN_AUFSTELLUNG
    assert not fremdes.gesetzt


def test_auf_1_4_ein_modell_des_gegners_ist_nicht_in_aufstellung(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    aufstellung.einheit_in_aufstellung_wählen(b.armee.einheiten[0])
    gegnerisches = a.armee.einheiten[0].modelle[0]

    assert sperrgrund(lambda: aufstellung.modell_setzen(gegnerisches)) is Grund.NICHT_IN_AUFSTELLUNG
    assert not gegnerisches.gesetzt


def test_auf_1_4_ohne_einheit_in_aufstellung_ist_beenden_nicht_in_aufstellung(aufstellung, a):
    nach_der_wahl(aufstellung, a)

    grund = sperrgrund(aufstellung.aufstellen_der_einheit_beenden)

    assert grund is Grund.NICHT_IN_AUFSTELLUNG


def test_auf_1_4_vor_der_wahl_ist_beenden_nicht_in_aufstellung(aufstellung):
    grund = sperrgrund(aufstellung.aufstellen_der_einheit_beenden)

    assert grund is Grund.NICHT_IN_AUFSTELLUNG


def test_auf_1_4_nach_dem_beenden_gibt_es_keine_einheit_zum_erneuten_beenden(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    aufgestellt(aufstellung, b.armee.einheiten[0])

    grund = sperrgrund(aufstellung.aufstellen_der_einheit_beenden)

    assert grund is Grund.NICHT_IN_AUFSTELLUNG


# AUF-1.5

def test_auf_1_5_eine_nicht_aufgestellte_einheit_des_spielers_an_der_reihe_ist_wählbar(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    einheit = b.armee.einheiten[1]

    aufstellung.einheit_in_aufstellung_wählen(einheit)

    assert aufstellung.einheit_in_aufstellung is einheit


def test_auf_1_5_vor_der_wahl_ist_keine_einheit_wählbar(aufstellung, a):
    einheit = a.armee.einheiten[0]

    assert sperrgrund(lambda: aufstellung.einheit_in_aufstellung_wählen(einheit)) is Grund.NICHT_WÄHLBAR
    assert aufstellung.einheit_in_aufstellung is None


def test_auf_1_5_eine_einheit_des_spielers_nicht_an_der_reihe_ist_nicht_wählbar(aufstellung, a):
    nach_der_wahl(aufstellung, a)
    einheit = a.armee.einheiten[0]

    assert sperrgrund(lambda: aufstellung.einheit_in_aufstellung_wählen(einheit)) is Grund.NICHT_WÄHLBAR
    assert aufstellung.einheit_in_aufstellung is None


def test_auf_1_5_eine_aufgestellte_einheit_ist_nicht_wählbar(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    aufgestellt(aufstellung, b.armee.einheiten[0])
    aufgestellt(aufstellung, a.armee.einheiten[0])
    fertige = b.armee.einheiten[0]

    assert sperrgrund(lambda: aufstellung.einheit_in_aufstellung_wählen(fertige)) is Grund.NICHT_WÄHLBAR
    assert aufstellung.einheit_in_aufstellung is None


def test_auf_1_5_nach_der_aufstellung_ist_keine_einheit_wählbar(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    for einheit_b, einheit_a in zip(b.armee.einheiten, a.armee.einheiten):
        aufgestellt(aufstellung, einheit_b)
        aufgestellt(aufstellung, einheit_a)

    for einheit in a.armee.einheiten + b.armee.einheiten:
        assert sperrgrund(lambda e=einheit: aufstellung.einheit_in_aufstellung_wählen(e)) is Grund.NICHT_WÄHLBAR


def test_auf_1_5_gegen_eine_nicht_wählbare_einheit_gilt_nicht_wählbar_auch_nach_begonnener_einheit(
    aufstellung, a, b
):
    nach_der_wahl(aufstellung, a)
    begonnene = b.armee.einheiten[0]
    aufstellung.einheit_in_aufstellung_wählen(begonnene)
    aufstellung.modell_setzen(begonnene.modelle[0])

    grund = sperrgrund(lambda: aufstellung.einheit_in_aufstellung_wählen(a.armee.einheiten[0]))

    assert grund is Grund.NICHT_WÄHLBAR


# AUF-1.6

def test_auf_1_6_ohne_gesetztes_modell_löst_die_wählbare_einheit_die_bisherige_ab(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    aufstellung.einheit_in_aufstellung_wählen(b.armee.einheiten[0])

    aufstellung.einheit_in_aufstellung_wählen(b.armee.einheiten[1])

    assert aufstellung.einheit_in_aufstellung is b.armee.einheiten[1]


def test_auf_1_6_mit_gesetztem_modell_ist_die_einheit_begonnen(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    begonnene = b.armee.einheiten[0]
    aufstellung.einheit_in_aufstellung_wählen(begonnene)
    aufstellung.modell_setzen(begonnene.modelle[0])

    grund = sperrgrund(lambda: aufstellung.einheit_in_aufstellung_wählen(b.armee.einheiten[1]))

    assert grund is Grund.EINHEIT_BEGONNEN
    assert aufstellung.einheit_in_aufstellung is begonnene


def test_auf_1_6_die_begonnene_einheit_erneut_zu_wählen_ist_nicht_gesperrt(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    begonnene = b.armee.einheiten[0]
    aufstellung.einheit_in_aufstellung_wählen(begonnene)
    aufstellung.modell_setzen(begonnene.modelle[0])

    aufstellung.einheit_in_aufstellung_wählen(begonnene)

    assert aufstellung.einheit_in_aufstellung is begonnene


# AUF-1.7

def test_auf_1_7_nach_dem_beenden_ist_die_einheit_aufgestellt_und_keine_in_aufstellung(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    einheit = b.armee.einheiten[0]

    aufgestellt(aufstellung, einheit)

    assert einheit.aufgestellt
    assert aufstellung.einheit_in_aufstellung is None
    assert not b.armee.einheiten[1].aufgestellt


def test_auf_1_7_nach_dem_beenden_ist_der_andere_spieler_an_der_reihe(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)

    aufgestellt(aufstellung, b.armee.einheiten[0])

    assert aufstellung.an_der_reihe is a


def test_auf_1_7_die_spieler_stellen_abwechselnd_auf(aufstellung, a, b):
    nach_der_wahl(aufstellung, a)
    reihenfolge = []
    for einheit_b, einheit_a in zip(b.armee.einheiten, a.armee.einheiten):
        reihenfolge.append(aufstellung.an_der_reihe)
        aufgestellt(aufstellung, einheit_b)
        reihenfolge.append(aufstellung.an_der_reihe)
        aufgestellt(aufstellung, einheit_a)

    assert reihenfolge == [b, a, b, a]


def test_auf_1_7_hat_der_andere_alle_einheiten_aufgestellt_ist_derselbe_wieder_an_der_reihe(spieler_mit_einheiten):
    kleiner, größer = spieler_mit_einheiten(1), spieler_mit_einheiten(1, 1, 1)
    aufstellung = Aufstellung(kleiner, größer)
    nach_der_wahl(aufstellung, größer)

    aufgestellt(aufstellung, kleiner.armee.einheiten[0])
    assert aufstellung.an_der_reihe is größer
    aufgestellt(aufstellung, größer.armee.einheiten[0])
    assert aufstellung.an_der_reihe is größer
    aufgestellt(aufstellung, größer.armee.einheiten[1])
    assert aufstellung.an_der_reihe is größer


def test_auf_1_7_haben_beide_alle_einheiten_aufgestellt_ist_die_aufstellung_beendet(spieler_mit_einheiten):
    kleiner, größer = spieler_mit_einheiten(1), spieler_mit_einheiten(1, 1)
    aufstellung = Aufstellung(kleiner, größer)
    nach_der_wahl(aufstellung, größer)

    aufgestellt(aufstellung, kleiner.armee.einheiten[0])
    aufgestellt(aufstellung, größer.armee.einheiten[0])
    assert not aufstellung.beendet
    aufgestellt(aufstellung, größer.armee.einheiten[1])

    assert aufstellung.beendet
    assert aufstellung.an_der_reihe is None
    assert aufstellung.einheit_in_aufstellung is None


def test_auf_1_7_vor_dem_letzten_beenden_ist_die_aufstellung_nicht_beendet(aufstellung, a):
    assert not aufstellung.beendet
    nach_der_wahl(aufstellung, a)
    assert not aufstellung.beendet
