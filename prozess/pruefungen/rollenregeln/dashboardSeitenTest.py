from rollenregeln.dashboard import seiteErzeugen
from rollenregeln.dashboardSeiten import sitzungenJeSeite
from rollenregeln.laufLesen import Lauf


def läufeInSitzungen(anzahl):
    return [Lauf("a", "planer", 1, sitzung=f"{nummer:08d}-x") for nummer in range(anzahl)]


def testAlleSitzungenSindImDashboardAuffindbar():
    anzahl = 3 * sitzungenJeSeite + 1
    seite = seiteErzeugen(läufeInSitzungen(anzahl))
    assert seite.count('class="sitzungs-karte"') == anzahl


def testSechsSitzungenJeSeite():
    assert sitzungenJeSeite == 6  # noqa: PLR2004
    assert 'data-pro-seite="6"' in seiteErzeugen(läufeInSitzungen(7))


def testSeitenschalterMitSkriptErscheintErstAbSiebenSitzungen():
    genug = seiteErzeugen(läufeInSitzungen(sitzungenJeSeite + 1))
    assert 'id="seitenschalter"' in genug and "‹ Zurück" in genug and "Weiter ›" in genug
    assert "neueste zuerst" in genug
    knapp = seiteErzeugen(läufeInSitzungen(sitzungenJeSeite))
    assert 'id="seitenschalter"' not in knapp and "<script>" not in knapp


def testNeuesteSitzungStehtZuerst():
    seite = seiteErzeugen(läufeInSitzungen(8))
    assert seite.index("Sitzung 00000007") < seite.index("Sitzung 00000000")
