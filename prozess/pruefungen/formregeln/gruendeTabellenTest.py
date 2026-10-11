import pytest

from formregeln.gruendeTabellen import quelltextVerstöße, verstöße
from gemeinsam.pfade import wurzel

sauber = """
class Handlung:
    def wächter(self):
        raise Sperre(Grund.nichtWählbar)

    def sammeln(self, gründe):
        raise Sperre(*gründe)

    _prüfungen = {Grund.baseÜberdeckt: 1, Grund.nahkampfreichweite: 2}
    _gegenDasBeenden: ClassVar[dict] = {Grund.modelleFehlen: 3}
"""


def meldungenZu(**module: str) -> list[str]:
    return quelltextVerstöße(module)


@pytest.mark.stand
def testDasRepoHältDieTabellenDerGründe():
    assert verstöße(wurzel) == []


def testWächterSammlungUndGetrennteTabellenSindGrün():
    assert meldungenZu(modul=sauber) == []


def testSperreMitZweiFestenGründenScheitert():
    quelltext = "raise Sperre(Grund.baseÜberdeckt, Grund.modelleFehlen)\n"
    assert len(meldungenZu(modul=quelltext)) == 1


def testSperreMitEinemFremdenAusdruckScheitert():
    assert len(meldungenZu(modul="raise Sperre(grund)\n")) == 1


def testSperreOhneGrundScheitert():
    assert len(meldungenZu(modul="raise Sperre()\n")) == 1


def testWächterGrundAlsTabellenschlüsselScheitert():
    quelltext = sauber + "\nraise Sperre(Grund.baseÜberdeckt)\n"
    meldungen = meldungenZu(modul=quelltext)
    assert len(meldungen) == 1
    assert "Wächter und Tabellenschlüssel" in meldungen[0]


def testWächterUndTabelleInVerschiedenenModulenScheitern():
    meldungen = meldungenZu(
        eins="raise Sperre(Grund.modelleFehlen)\n", zwei="tabelle = {Grund.modelleFehlen: 1}\n"
    )
    assert len(meldungen) == 1


def testGrundInZweiTabellenScheitert():
    meldungen = meldungenZu(
        eins="tabelle = {Grund.modelleFehlen: 1}\n", zwei="andere = {Grund.modelleFehlen: 2}\n"
    )
    assert len(meldungen) == 1
    assert "zwei Tabellen" in meldungen[0]


def testAndereRaisesUndSchlüsselOhneGrundBleibenUnberührt():
    quelltext = "raise ValueError('x')\nraise Fehler\ntabelle = {'a': 1, **rest}\n"
    assert meldungenZu(modul=quelltext) == []
