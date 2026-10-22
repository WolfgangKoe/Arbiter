import pytest

from formregeln.kommentare import (
    docstringVerstöße,
    höchstzahlOffenerPunkte,
    kommentarVerstöße,
    todoZeilen,
    verstöße,
)
from formregeln.technikphase import technikGeprüft, zeilenVorDerTechnikphase
from gemeinsam.pfade import wurzel


@pytest.mark.stand
def testDasRepoHältDieKommentarregel():
    assert verstöße(wurzel) == []


@pytest.mark.parametrize(
    ("quelltext", "endung"),
    [
        pytest.param("x = 1  # Zähler erhöhen\n", ".py", id="Erklärkommentar"),
        pytest.param("# Regel: wir.md 8\n", ".py", id="Regel"),
        pytest.param("# Warum: pytest gibt den Namen vor\n", ".py", id="Warum"),
        pytest.param("# TODO später\n", ".py", id="TODO ohne Doppelpunkt"),
        pytest.param("# TODO:\n", ".py", id="TODO ohne Text"),
        pytest.param("x = 1  # noqa\n", ".py", id="noqa ohne Regelcode"),
        pytest.param("x = 1  # type: ignore\n", ".py", id="type ignore ohne Regelcode"),
        pytest.param("// erklärt nur\n", ".js", id="JavaScript Prosa"),
        pytest.param("// Warum: weil\n", ".js", id="JavaScript Warum"),
        pytest.param("// eslint-disable-next-line\n", ".mjs", id="eslint ohne Regel"),
    ],
)
def testUnerlaubteKommentareSindRot(quelltext, endung):
    assert kommentarVerstöße(quelltext, endung)


@pytest.mark.parametrize(
    ("quelltext", "endung"),
    [
        pytest.param("# TODO: Namen klären\n", ".py", id="TODO"),
        pytest.param("x = 1  # noqa: PLR2004\n", ".py", id="Werkzeugkommentar"),
        pytest.param("x = 1  # type: ignore[arg-type]\n", ".py", id="type ignore mit Code"),
        pytest.param("#!/usr/bin/env python3\n", ".py", id="Shebang"),
        pytest.param('x = "# kein Kommentar"\n', ".py", id="Raute im Text"),
        pytest.param("// TODO: Namen klären\n", ".js", id="JavaScript TODO"),
        pytest.param("// eslint-disable-next-line no-var\n", ".js", id="eslint mit Regel"),
        pytest.param('const url = "http://x";\n', ".js", id="Schrägstriche im Text"),
    ],
)
def testErlaubteKommentareSindGrün(quelltext, endung):
    assert kommentarVerstöße(quelltext, endung) == []


def testTodoZeilenNennenNurTodoKommentare():
    assert todoZeilen("x = 1\n# TODO: eins\n# noqa: A1\ny = 2  # TODO: zwei\n") == [2, 4]


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


def testMehrTodosAlsDerDeckelSindRot(tmp_path):
    (tmp_path / "prozess").mkdir()
    todos = "".join(f"# TODO: Fall {nummer}\n" for nummer in range(höchstzahlOffenerPunkte + 1))
    (tmp_path / "prozess" / "viele.py").write_text(todos, encoding="utf-8")
    assert verstöße(tmp_path) == [f"{höchstzahlOffenerPunkte + 1} TODOs, höchstens 3 erlaubt"]


def testDerDeckelAnTodosGiltAlsGrün(tmp_path):
    (tmp_path / "prozess").mkdir()
    todos = "".join(f"# TODO: Fall {nummer}\n" for nummer in range(höchstzahlOffenerPunkte))
    (tmp_path / "prozess" / "genug.py").write_text(todos, encoding="utf-8")
    assert verstöße(tmp_path) == []


def testEinKommentarUnterTechnikIstErstAbTechnikphaseSiebenRot(tmp_path, gitRepo):
    (tmp_path / "technik").mkdir()
    (tmp_path / "technik" / "modul.py").write_text("x = 1  # Zähler\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 6")
    assert not technikGeprüft(tmp_path)
    assert verstöße(tmp_path) == []
    gitRepo.festhalten("Freigabe Plan 7")
    assert technikGeprüft(tmp_path)
    assert [meldung.split(": ")[0] for meldung in verstöße(tmp_path)] == ["technik/modul.py"]


def testEinTodoVonVorDerTechnikphaseIstRotEinNeuesBleibt(tmp_path, gitRepo):
    (tmp_path / "prozess").mkdir()
    datei = tmp_path / "prozess" / "modul.py"
    datei.write_text("# TODO: alt\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 7")
    datei.write_text("# TODO: alt\n# TODO: neu\n", encoding="utf-8")
    assert zeilenVorDerTechnikphase(tmp_path, "prozess/modul.py", [1, 2]) == [1]
    gitRepo.festhalten("neu dazu")
    assert zeilenVorDerTechnikphase(tmp_path, "prozess/modul.py", [1, 2]) == [1]
    assert verstöße(tmp_path) == [
        "prozess/modul.py: Zeile 1: TODO von vor der laufenden Technikphase"
    ]
