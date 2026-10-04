import pytest

from mockups import verstöße
from pfade import mockupOrdner, wurzel


@pytest.mark.stand
def testDieMockupsHaltenDieRegel():
    assert verstöße(wurzel) == []


def mockupDatei(tmp_path, name: str, inhalt: str):
    ordner = tmp_path / mockupOrdner
    ordner.mkdir(parents=True, exist_ok=True)
    (ordner / name).write_text(inhalt, encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize(
    "name, inhalt",
    [
        pytest.param("a.html", "<!-- Hinweis -->", id="HTML-Kommentar"),
        pytest.param("a.html", "<script>x()</script>", id="Script"),
        pytest.param("a.html", "<style>p{}</style>", id="Style-Element"),
        pytest.param("a.html", '<p style="color:red">x</p>', id="Style-Attribut"),
        pytest.param("a.html", "<P STYLE = 'x'>", id="Großschreibung und Leerzeichen"),
        pytest.param("vorschlag.css", "/* Hinweis */ p{}", id="CSS-Kommentar"),
    ],
)
def testVerstoßIstRot(tmp_path, name, inhalt):
    assert verstöße(mockupDatei(tmp_path, name, inhalt))


def testSauberesMockupIstGrün(tmp_path):
    wurzelOrdner = mockupDatei(tmp_path, "a.html", '<p class="knopf">x</p>')
    mockupDatei(tmp_path, "vorschlag.css", ".knopf{color:red}")
    assert verstöße(wurzelOrdner) == []


def testSternImHtmlTextIstGrün(tmp_path):
    assert verstöße(mockupDatei(tmp_path, "a.html", "<p>/* kein CSS */</p>")) == []


def testFehlenderOrdnerIstGrün(tmp_path):
    assert verstöße(tmp_path) == []


def testLeererOrdnerIstGrün(tmp_path):
    (tmp_path / mockupOrdner).mkdir(parents=True)
    assert verstöße(tmp_path) == []
