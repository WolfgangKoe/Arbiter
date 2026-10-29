import json
import re

import pytest

from formregeln.erlaubteImporte import kastenNamen, pfeilErlaubt
from gemeinsam.pfade import projektordner
from rollenregeln.architekturKanten import kantenMessen, kastenPfeile
from rollenregeln.architekturMessung import kästenMessen
from rollenregeln.dashboardArchitektur import architekturSeite
from rollenregeln.dashboardServer import antworten

kopf = {"Origin": None, "Host": "127.0.0.1:8765"}
produkt = "technik/arbiter"


def datei(wurzel, pfad, text="x = 1\n"):
    ziel = wurzel / pfad
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, encoding="utf-8")


def baum(wurzel):
    datei(wurzel, f"{produkt}/domaene/sperre.py", "import fractions\n")
    datei(wurzel, f"{produkt}/domaene/phasen/__init__.py", "")
    datei(wurzel, f"{produkt}/domaene/phasen/aufstellen/beenden.py", "from .. import x\n")
    datei(wurzel, f"{produkt}/web/server.py", "from arbiter.domaene import sperre\n")
    datei(wurzel, f"{produkt}/katalog/ausgangslage.py", "from ..domaene import sperre\n")
    datei(wurzel, f"{produkt}/__main__.py", "from arbiter.web import server\n")
    datei(wurzel, "technik/frontend/seite.js", 'import { a } from "./anfragen.js"\n')
    datei(wurzel, "technik/frontend/anfragen.js", "abc")
    datei(wurzel, "technik/frontend/index.html", '<script src="seite.js"></script>\n')
    datei(wurzel, "technik/architektur.md", "übersicht")
    datei(wurzel, "technik/architektur/web.md", "web beschrieben")
    datei(wurzel, "technik/architektur/vertrag/ebene.json", "{}")


def kanten(wurzel):
    gemessen = kantenMessen(wurzel, kästenMessen(wurzel))
    return {(kante.von, kante.nach): kante for kante in gemessen}


def seite(wurzel):
    return architekturSeite(wurzel)


def testDerReiterArchitekturLiefertDieKarteUndDerTokenberichtNicht(tmp_path):
    (tmp_path / "handoff" / "anliegen").mkdir(parents=True)
    baum(tmp_path)
    architektur = antworten(tmp_path, "GET", "/architektur", b"", kopf).inhalt.decode()
    tokens = antworten(tmp_path, "GET", "/tokens", b"", kopf).inhalt.decode()
    assert 'id="architektur"' in architektur
    assert 'aria-current="page">Architektur' in architektur
    assert 'id="architektur"' not in tokens
    assert "architekturkarte" not in tokens


def testBeimÖffnenSindDieKästenDerSchichtenDaUndDieDateienEingebettet(tmp_path):
    baum(tmp_path)
    text = seite(tmp_path)
    assert all(f'data-kasten="{name}"' in text for name in kastenNamen)
    assert 'data-kasten="anwendung"' in text
    assert re.search(r'class="ak ordner leer" data-kasten="anwendung"', text) is None
    assert re.search(r'class="ak datei leer" data-kasten="anwendung"', text)
    assert f'data-pfad="{produkt}/domaene/phasen/aufstellen/beenden.py"' in text


def testEinOrdnerÖffnetSichBisZurDateiUndLeereInitDateienFehlen(tmp_path):
    baum(tmp_path)
    text = seite(tmp_path)
    for pfad in (f"{produkt}/domaene", f"{produkt}/domaene/phasen", f"{produkt}/domaene/sperre.py"):
        assert f'data-pfad="{pfad}"' in text
    assert "__init__.py" not in text
    assert 'class="ak ordner"' in text
    assert "ak-kinder" in text and 'classList.toggle("offen")' in text


def testPfeileZählenImportzeilenAusPythonJavaScriptUndHtml(tmp_path):
    baum(tmp_path)
    gemessen = kanten(tmp_path)
    assert gemessen[(f"{produkt}/web/server.py", f"{produkt}/domaene/sperre.py")].anzahl == 1
    assert gemessen[("technik/frontend/seite.js", "technik/frontend/anfragen.js")].anzahl == 1
    assert gemessen[("technik/frontend/index.html", "technik/frontend/seite.js")].anzahl == 1
    eingebettet = re.search(r'id="architektur-kanten">(.*?)</script>', seite(tmp_path))
    http = {"von": "technik/frontend", "nach": f"{produkt}/web", "anzahl": 0, "erlaubt": True}
    assert http | {"text": "HTTP"} in json.loads(eingebettet.group(1))


def testSeitenVerweiseAufDateienAußerhalbDerSeiteZählenNicht(tmp_path):
    baum(tmp_path)
    datei(tmp_path, "technik/frontend/zeichnen.js", 'import x from "./gibtEsNicht.js"\n')
    assert not [kante for kante in kanten(tmp_path).values() if kante.von.endswith("zeichnen.js")]


def testJedeDateiNenntIhrenPfadAbDemRepoUndIhreZeichen(tmp_path):
    baum(tmp_path)
    text = seite(tmp_path)
    assert f'<span class="ak-zahl">{produkt}/web/server.py</span>' in text
    assert "35 Zeichen" in text


def testEinOrdnerDenDieArchitekturNichtKenntBekommtEinenRotenKasten(tmp_path):
    baum(tmp_path)
    datei(tmp_path, f"{produkt}/neuling/werk.py", "from arbiter.domaene import sperre\n")
    datei(tmp_path, f"{produkt}/domaene/nutzt.py", "from arbiter.neuling import werk\n")
    text = seite(tmp_path)
    assert "neuling · nicht in der Architektur" in text
    assert 'class="ak ordner unbekannt" data-kasten="neuling"' in text
    gemessen = kanten(tmp_path)
    assert gemessen[(f"{produkt}/neuling/werk.py", f"{produkt}/domaene/sperre.py")].erlaubt is False
    assert gemessen[(f"{produkt}/domaene/nutzt.py", f"{produkt}/neuling/werk.py")].erlaubt is False
    assert "Verbotene Pfeile: " in text and "neuling · nicht in der Architektur → Domäne" in text


def testEinVerbotenerPfeilStehtAlsUrteilUndErlaubteNicht(tmp_path):
    baum(tmp_path)
    assert "Kein verbotener Pfeil." in seite(tmp_path)
    datei(tmp_path, f"{produkt}/domaene/phase.py", "from arbiter.katalog import ausgangslage\n")
    assert "Verbotene Pfeile: Domäne → Katalog" in seite(tmp_path)
    assert (
        kanten(tmp_path)[
            (f"{produkt}/domaene/phase.py", f"{produkt}/katalog/ausgangslage.py")
        ].erlaubt
        is False
    )


@pytest.mark.parametrize(
    "zeile",
    [
        "from arbiter.domaene import sperre\n",
        "from arbiter.domaene.sperre import etwas\n",
        "from ..domaene import sperre\n",
        "from arbiter import domaene\n",
    ],
)
def testAbsoluteUndRelativeImporteBisArbiterZählenGleich(tmp_path, zeile):
    baum(tmp_path)
    datei(tmp_path, f"{produkt}/web/darstellung.py", zeile)
    gemessen = kanten(tmp_path)
    ziel = [kante for kante in gemessen.values() if kante.von.endswith("web/darstellung.py")]
    assert len(ziel) == 1
    assert ziel[0].nach.startswith(f"{produkt}/domaene")
    assert ziel[0].anzahl == 1


def testKastenPfeileFassenDieDateienZusammen(tmp_path):
    baum(tmp_path)
    datei(tmp_path, f"{produkt}/web/darstellung.py", "from arbiter.domaene import sperre\n")
    zusammen = kastenPfeile(list(kanten(tmp_path).values()))
    pfeile = {(pfeil.von, pfeil.nach): pfeil for pfeil in zusammen}
    assert pfeile[("web", "domaene")].anzahl == 2  # noqa: PLR2004


def testWebDarfDieDomäneNurSolangeAnwendungKeinenCodeHat():
    ohne = frozenset({"web", "domaene"})
    mit = ohne | {"anwendung"}
    assert pfeilErlaubt("web", "domaene", ohne)
    assert not pfeilErlaubt("web", "domaene", mit)
    assert pfeilErlaubt("web", "anwendung", mit)


@pytest.mark.parametrize("nach", [name for name in kastenNamen if name != "domaene"])
def testDieDomäneDarfKeinenAnderenKastenImportieren(nach):
    assert not pfeilErlaubt("domaene", nach, frozenset())


def testDieFußzeileNenntÜbersichtUndVertrag(tmp_path):
    baum(tmp_path)
    assert "Übersicht 9 und Vertrag 2." in seite(tmp_path)


@pytest.mark.stand
def testDasRepoZeigtKeinenRotenPfeilUndDieStartDateiAlsKasten():
    wurzel = projektordner()
    gemessen = kantenMessen(wurzel, kästenMessen(wurzel))
    assert gemessen
    assert all(kante.erlaubt for kante in gemessen)
    text = architekturSeite(wurzel)
    assert 'data-pfad="technik/arbiter/__main__.py"' in text
    assert f'data-pfad="{produkt}/web/server.py"' in text
