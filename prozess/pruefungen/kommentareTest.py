import pytest

from kommentare import docstringVerstöße, kommentarVerstöße, verstöße
from pfade import wurzel


@pytest.mark.stand
def testDasRepoHältDieKommentarregel():
    assert verstöße(wurzel) == []


@pytest.mark.parametrize(
    "quelltext",
    [
        pytest.param("x = 1  # Zähler erhöhen\n", id="Erklärkommentar"),
        pytest.param("# Art, Pfad, Zeile\n", id="Kommentar ohne Marke"),
        pytest.param("# Regel:\n", id="Marke ohne Inhalt"),
        pytest.param("# TODO später\n", id="TODO"),
        pytest.param("# Warum: FIXME\n", id="FIXME mit Marke"),
    ],
)
def testUnerlaubteKommentareSindRot(quelltext):
    assert kommentarVerstöße(quelltext)


@pytest.mark.parametrize(
    "quelltext",
    [
        pytest.param("# Regel: wir.md 8\n", id="Regel"),
        pytest.param("# Warum: pytest gibt den Namen vor\n", id="Warum"),
        pytest.param("x = 1  # noqa: PLR2004\n", id="Werkzeugkommentar"),
        pytest.param('x = "# kein Kommentar"\n', id="Raute im Text"),
    ],
)
def testErlaubteKommentareSindGrün(quelltext):
    assert kommentarVerstöße(quelltext) == []


@pytest.mark.parametrize(
    "quelltext",
    [
        pytest.param('"""Erste.\n\nZweite."""\n', id="Modul mehrzeilig"),
        pytest.param('def tun():\n    """Erste.\n\n    Zweite.\n    """\n', id="Funktion"),
        pytest.param('class Ort:\n    """TODO: später."""\n', id="TODO im Docstring"),
    ],
)
def testUnerlaubteDocstringsSindRot(quelltext):
    assert docstringVerstöße(quelltext)


def testEinzeiligerDocstringIstGrün():
    assert docstringVerstöße('def tun():\n    """Tut etwas."""\n') == []


def testDieVerstößeEinesVerzeichnissesNennenDateiUndGrund(tmp_path):
    (tmp_path / "prozess").mkdir()
    (tmp_path / "prozess" / "gut.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "prozess" / "schlecht.py").write_text("x = 1  # Zähler\n", encoding="utf-8")
    (tmp_path / "prozess" / "notiz.md").write_text("# TODO\n", encoding="utf-8")
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert meldungen[0].startswith("prozess/schlecht.py: ")
