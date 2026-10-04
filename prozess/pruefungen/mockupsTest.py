import pytest

from mockups import verstöße
from pfade import mockupOrdner, wurzel


@pytest.mark.stand
def testDieMockupsHaltenDieRegel():
    assert verstöße(wurzel) == []


def mockupDatei(tmp_path, name: str, inhalt: str | bytes):
    ordner = tmp_path / mockupOrdner
    ordner.mkdir(parents=True, exist_ok=True)
    if isinstance(inhalt, bytes):
        (ordner / name).write_bytes(inhalt)
    else:
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
        pytest.param("a.html", '<p style\t="x">', id="Tab vor Gleichheitszeichen"),
        pytest.param("a.html", '<p\n style\n="x">', id="Zeilenumbruch"),
        pytest.param("vorschlag.css", "/* Hinweis */ p{}", id="CSS-Kommentar"),
        pytest.param("A.HTML", "<script>x()</script>", id="Endung groß"),
        pytest.param("b.htm", "<p>x</p>", id="fremde Endung htm"),
        pytest.param("c.svg", "<svg/>", id="fremde Endung svg"),
        pytest.param("bild.png", b"\xff\xfe\x00", id="Bytes ohne UTF-8"),
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


@pytest.mark.parametrize("inhalt", ['<p data-style="x">', "<p>style=fett</p>"])
def testStyleAlsFremdesAttributOderTextIstGrün(tmp_path, inhalt):
    assert verstöße(mockupDatei(tmp_path, "a.html", inhalt)) == []


def testMeldungNenntDenPfadImOrdner(tmp_path):
    ordner = tmp_path / mockupOrdner / "unter"
    ordner.mkdir(parents=True)
    (ordner / "a.html").write_text("<script>", encoding="utf-8")
    assert verstöße(tmp_path) == [f"{mockupOrdner}/unter/a.html: <script"]
