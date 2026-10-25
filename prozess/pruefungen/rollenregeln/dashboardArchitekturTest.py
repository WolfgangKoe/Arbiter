import pytest

from formregeln.erlaubteImporte import kastenNamen, pfeilErlaubt
from gemeinsam.pfade import projektordner
from rollenregeln.architekturMessung import importzeilen, kästenMessen, pfeileMessen
from rollenregeln.dashboardArchitektur import architekturKarte, kartenBild


def datei(wurzel, pfad, text="x = 1\n"):
    ziel = wurzel / pfad
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, encoding="utf-8")


def baum(wurzel):
    datei(wurzel, "technik/arbiter/domaene/sperre.py", "import fractions\n")
    datei(wurzel, "technik/arbiter/web/server.py", "from arbiter.domaene import sperre\n")
    datei(wurzel, "technik/arbiter/katalog/ausgangslage.py", "from ..domaene import sperre\n")
    datei(wurzel, "technik/arbiter/__main__.py", "from arbiter.web import server\n")
    datei(wurzel, "technik/frontend/seite.js", "abc")
    datei(wurzel, "technik/architektur.md", "übersicht")
    datei(wurzel, "technik/architektur/web.md", "web beschrieben")
    datei(wurzel, "technik/architektur/vertrag/ebene.json", "{}")


def pfeile(wurzel):
    return {(pfeil.von, pfeil.nach): pfeil for pfeil in pfeileMessen(wurzel, kästenMessen(wurzel))}


def testEinVerbotenerPfeilIstRotUndErlaubteSindGrau(tmp_path):
    baum(tmp_path)
    verboten = "from arbiter.katalog import ausgangslage\n"
    datei(tmp_path, "technik/arbiter/domaene/phase.py", verboten)
    karte = architekturKarte(tmp_path)
    assert pfeile(tmp_path)[("domaene", "katalog")].erlaubt is False
    assert karte.count('class="pfeil verboten"') == 1
    assert 'class="pfeil"' in karte
    assert "Verbotene Pfeile: Domäne → Katalog" in karte


def testErlaubteImporteZeigenKeinenRotenPfeilMitAnzahlDerZeilen(tmp_path):
    baum(tmp_path)
    datei(tmp_path, "technik/arbiter/web/darstellung.py", "from arbiter.domaene import sperre\n")
    gemessen = pfeile(tmp_path)
    assert gemessen[("web", "domaene")].anzahl == 2  # noqa: PLR2004
    assert all(pfeil.erlaubt for pfeil in gemessen.values())
    assert "Kein verbotener Pfeil." in architekturKarte(tmp_path)


def testEinKastenOhneCodeIstGestricheltUndEinMitCodeNicht(tmp_path):
    baum(tmp_path)
    karte = architekturKarte(tmp_path)
    assert 'data-kasten="anwendung"><rect class="karte-kasten leer"' in karte
    assert 'data-kasten="domaene"><rect class="karte-kasten"' in karte


def testZeichenCodeGegenArchitekturUndKeineDatei(tmp_path):
    baum(tmp_path)
    karte = architekturKarte(tmp_path)
    assert "Architektur 15" in karte
    assert "keine Datei" in karte
    kästen = {kasten.name: kasten for kasten in kästenMessen(tmp_path)}
    assert kästen["seite"].codeZeichen == 3  # noqa: PLR2004
    assert kästen["web"].architekturZeichen == 15  # noqa: PLR2004
    assert kästen["katalog"].architekturZeichen is None


def testDieFußzeileNenntÜbersichtUndVertrag(tmp_path):
    baum(tmp_path)
    assert "Übersicht 9 und Vertrag 2." in architekturKarte(tmp_path)


def testWebDarfDieDomäneNurSolangeAnwendungKeinenCodeHat():
    ohne = frozenset({"web", "domaene"})
    mit = ohne | {"anwendung"}
    assert pfeilErlaubt("web", "domaene", ohne)
    assert not pfeilErlaubt("web", "domaene", mit)
    assert pfeilErlaubt("web", "anwendung", mit)


@pytest.mark.parametrize("nach", [name for name in kastenNamen if name != "domaene"])
def testDieDomäneDarfKeinenAnderenKastenImportieren(nach):
    assert not pfeilErlaubt("domaene", nach, frozenset())


def testDieKarteZeichnetJedenKastenUndDenFestenPfeilHttp(tmp_path):
    baum(tmp_path)
    bild = kartenBild(kästenMessen(tmp_path), [])
    assert all(f'data-kasten="{name}"' in bild for name in kastenNamen)
    assert ">HTTP<" in bild


@pytest.mark.stand
def testDasRepoZeigtKeinenRotenPfeilUndLeereKästenGestrichelt():
    wurzel = projektordner()
    assert importzeilen(wurzel)
    assert all(pfeil.erlaubt for pfeil in pfeileMessen(wurzel, kästenMessen(wurzel)))
    karte = architekturKarte(wurzel)
    assert 'data-kasten="anwendung"><rect class="karte-kasten leer"' in karte
    assert 'data-kasten="speicher"><rect class="karte-kasten leer"' in karte
