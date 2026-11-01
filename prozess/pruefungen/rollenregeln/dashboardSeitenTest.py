from rollenregeln.dashboard import seiteErzeugen
from rollenregeln.dashboardSeiten import sitzungenJeSeite
from rollenregeln.laufLesen import Lauf


def läufeInSitzungen(anzahl):
    return [Lauf("a", "planer", 1, sitzung=f"{nummer:08d}-x") for nummer in range(anzahl)]


def testNurDieSechsSitzungenDerSeiteStehenImHtml():
    assert sitzungenJeSeite == 6  # noqa: PLR2004
    läufe = läufeInSitzungen(3 * sitzungenJeSeite + 1)
    erste = seiteErzeugen(läufe, seite=1)
    letzte = seiteErzeugen(läufe, seite=4)
    assert erste.count('class="sitzungs-karte"') == sitzungenJeSeite
    assert letzte.count('class="sitzungs-karte"') == 1
    assert "Sitzung 00000018" in erste and "Sitzung 00000018" not in letzte
    assert "Sitzung 00000000" in letzte


def testSeitenschalterSindVerweiseAufDenServerUndErscheinenErstAbSiebenSitzungen():
    genug = seiteErzeugen(läufeInSitzungen(sitzungenJeSeite + 1), seite=2)
    assert '<a href="/tokens?seite=1">1</a>' in genug
    assert '<a href="/tokens?seite=1">‹ Zurück</a>' in genug
    assert '<a href="/tokens?seite=2" aria-current="page">2</a>' in genug
    assert '<span class="gesperrt">Weiter ›</span>' in genug
    assert "<script>" not in genug
    knapp = seiteErzeugen(läufeInSitzungen(sitzungenJeSeite))
    assert 'id="seitenschalter"' not in knapp


def testEineSeiteAußerhalbDesBereichsZeigtDieNächsteGültige():
    läufe = läufeInSitzungen(8)
    assert "Sitzung 00000000" in seiteErzeugen(läufe, seite=99)
    assert "Sitzung 00000007" in seiteErzeugen(läufe, seite=0)


def testNeuesteSitzungStehtZuerst():
    seite = seiteErzeugen(läufeInSitzungen(8))
    assert seite.index("Sitzung 00000007") < seite.index("Sitzung 00000002")
