from pathlib import Path

import pytest

from gemeinsam.pfade import wurzel
from standregeln.freigabeFormat import verstöße
from standregeln.freigabeKommentare import abschnitte
from standregeln.standTest import Repo

vorgehen = "## Nächstes Vorgehen\n- Produktziel: a\n- Etappenziel: b\n- Zyklusziel: c\n\n"


def schreiben(ordner: Path, name: str, text: str) -> None:
    (ordner / "handoff").mkdir(exist_ok=True)
    (ordner / "handoff" / name).write_text(text, encoding="utf-8")


@pytest.mark.stand
def testDasRepoHältDasFreigabeFormat():
    assert verstöße(wurzel) == []


def testPlanMitFreigabeAbschnittIstGrün(tmp_path):
    schreiben(tmp_path, "plan.md", "# Plan · Zyklus 3\n\n## Freigabe\nFreigabe: offen\n")
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize(
    "text",
    [
        "# Plan · Zyklus 3\n\nKein Abschnitt\n",
        "# Plan · Zyklus 3\n\n## Freigabe\nFreigabe: vielleicht\n",
        "# Plan · Zyklus 3\n\n## Freigabe\nFreigabe: ja\nFreigabe: offen\n",
        "# Plan · Zyklus 3\n\n## Freigabe\nFreigabe: ja\n\n## Danach\n",
    ],
)
def testPlanOhneGültigenFreigabeAbschnittIstRot(tmp_path, text):
    schreiben(tmp_path, "plan.md", text)
    assert len(verstöße(tmp_path)) == 1


def testReviewMitVorgehenIstGrünOhneZykluszielRot(tmp_path):
    kopf = "# Review · Zyklus 3\n\n"
    schreiben(tmp_path, "review.md", kopf + vorgehen + "## Freigabe\nFreigabe: offen\n")
    assert verstöße(tmp_path) == []
    schreiben(
        tmp_path,
        "review.md",
        kopf + vorgehen.replace("Zyklusziel", "") + "## Freigabe\nFreigabe: ja\n",
    )
    assert "Zyklusziel fehlt" in verstöße(tmp_path)[0]


def testReviewOhneVorgehenIstRot(tmp_path):
    schreiben(tmp_path, "review.md", "# Review · Zyklus 3\n\n## Freigabe\nFreigabe: offen\n")
    assert "Nächstes Vorgehen" in verstöße(tmp_path)[0]


def testDateiMitFreigabeCommitBleibtUngeprüft(tmp_path):
    repo = Repo(tmp_path)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 2\n\nKein Abschnitt\n")
    assert len(verstöße(tmp_path)) == 1
    repo.freigabe("Plan", 2)
    assert verstöße(tmp_path) == []


def testReviewMitVorliegenderRetroBleibtUngeprüft(tmp_path):
    schreiben(tmp_path, "review.md", "# Review · Zyklus 2\n")
    schreiben(tmp_path, "retro.md", "# Retro · Zyklus 2\n\n## Freigabe\nFreigabe: offen\n")
    assert verstöße(tmp_path) == []


def testWiederholteFreigabeÜberschriftAmEndeIstGrün(tmp_path):
    text = "# Plan · Zyklus 3\n\n## Freigabe\n\n## Danach\n\n## Freigabe\nFreigabe: offen\n"
    schreiben(tmp_path, "plan.md", text)
    assert verstöße(tmp_path) == []


def testFreigabeFeldAußerhalbDesAbschnittsZähltNicht(tmp_path):
    text = "# Plan · Zyklus 3\n\nFreigabe: ja\n\n## Freigabe\nKommentar: .\n"
    schreiben(tmp_path, "plan.md", text)
    assert len(verstöße(tmp_path)) == 1


def testAbschnitteNennenTitelUndZeilen():
    teile = abschnitte(["vorab", "## Plan", "eins", "## Freigabe", "Freigabe: ja"])
    assert [teil.titel for teil in teile] == ["Plan", "Freigabe"]
    assert teile[-1].zeilen == ["Freigabe: ja"]
