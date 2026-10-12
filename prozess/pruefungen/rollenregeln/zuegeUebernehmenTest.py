from pathlib import Path

import pytest

from gemeinsam.hookProtokoll import HookEingabe
from rollenregeln.eingang import Zug, verworfene, vorgemerkte, zugVormerken
from rollenregeln.zuegeUebernehmen import löstAus, übernehmen

fragen = """# Titel

{nummer} · {form} · von {absender} → {empfänger} · Runde {runde}/3 · {status}

## Runde 1
**Befund.** Text.

**F1 · Eins.** A oder B.
Antwort:

**F2 · Zwei.** A oder B.
Antwort: .

**Stellungnahme.**
"""


@pytest.fixture
def ordner(tmp_path):
    (tmp_path / "handoff" / "anliegen").mkdir(parents=True)
    return tmp_path


def anlegen(ordner: Path, nummer=10, form="Fragen", richtung=("planer", "Stakeholder"), **kopf):
    absender, empfänger = richtung
    text = fragen.format(
        nummer=nummer,
        form=form,
        absender=absender,
        empfänger=empfänger,
        runde=kopf.get("runde", 1),
        status=kopf.get("status", "offen"),
    )
    datei = ordner / "handoff" / "anliegen" / f"{nummer}-titel.md"
    datei.write_text(text, encoding="utf-8")
    return datei


def testStatusDesEmpfängersLandetImKopfUndDerZugIstAusDemEingang(ordner):
    datei = anlegen(ordner)
    zugVormerken(ordner, Zug(10, "status", "angenommen"))
    assert übernehmen(ordner) == (1, 0)
    assert "· Runde 1/3 · angenommen" in datei.read_text(encoding="utf-8").splitlines()[2]
    assert vorgemerkte(ordner) == []


def testStatusDerNichtMehrZumAnliegenPasstWirdVerworfenUndGemeldet(ordner):
    datei = anlegen(ordner, status="angenommen")
    vorher = datei.read_text(encoding="utf-8")
    zugVormerken(ordner, Zug(10, "status", "angenommen"))
    assert übernehmen(ordner) == (0, 1)
    assert datei.read_text(encoding="utf-8") == vorher
    assert "erlaubt angenommen nicht" in verworfene(ordner).pop().grund


def testStatusFremderAnliegenWirdVerworfenKommentarAberÜbernommen(ordner):
    datei = anlegen(ordner, richtung=("planer", "architekt"))
    zugVormerken(ordner, Zug(10, "status", "erledigt"))
    zugVormerken(ordner, Zug(10, "kommentar", "Bitte\nvorher klären."))
    assert übernehmen(ordner) == (1, 1)
    assert datei.read_text(encoding="utf-8").endswith("Kommentar: Bitte vorher klären.\n")


def testAntwortStehtNurUnterDerGenanntenFrage(ordner):
    datei = anlegen(ordner)
    zugVormerken(ordner, Zug(10, "antwort", "B", frage="F1"))
    assert übernehmen(ordner) == (1, 0)
    zeilen = datei.read_text(encoding="utf-8").splitlines()
    assert "Antwort: B" in zeilen and "Antwort: ." in zeilen and "Antwort:" not in zeilen


def testAntwortAufEineFehlendeFrageWirdVerworfen(ordner):
    anlegen(ordner)
    zugVormerken(ordner, Zug(10, "antwort", "B", frage="F7"))
    assert übernehmen(ordner) == (0, 1)


def testAntwortGibtEsNurAufOffeneFragenAnDenStakeholder(ordner):
    anlegen(ordner, richtung=("Stakeholder", "planer"))
    zugVormerken(ordner, Zug(10, "antwort", "B", frage="F1"))
    assert übernehmen(ordner) == (0, 1)


def testRundeSenkenNurBeiEskaliert(ordner):
    gesenkt = anlegen(ordner, nummer=10, status="eskaliert", runde=3)
    offen = anlegen(ordner, nummer=11, status="offen", runde=3)
    zugVormerken(ordner, Zug(10, "runde"))
    zugVormerken(ordner, Zug(11, "runde"))
    assert übernehmen(ordner) == (1, 1)
    assert "Runde 2/3 · eskaliert" in gesenkt.read_text(encoding="utf-8")
    assert "Runde 3/3 · offen" in offen.read_text(encoding="utf-8")


def testSpätereZügeWerdenGegenDenNeuenStatusGeprüft(ordner):
    anlegen(ordner, status="eskaliert", runde=3)
    zugVormerken(ordner, Zug(10, "status", "offen"))
    zugVormerken(ordner, Zug(10, "runde"))
    assert übernehmen(ordner) == (1, 1)


def testAntwortKommtAnAuchWennDerStatusDavorVorgemerktWurde(ordner):
    datei = anlegen(ordner)
    zugVormerken(ordner, Zug(10, "status", "angenommen"))
    zugVormerken(ordner, Zug(10, "antwort", "A", frage="F1"))
    assert übernehmen(ordner) == (2, 0)
    assert "Antwort: A" in datei.read_text(encoding="utf-8").splitlines()


def testUnbekanntesAnliegenWirdVerworfen(ordner):
    zugVormerken(ordner, Zug(99, "kommentar", "x"))
    assert übernehmen(ordner) == (0, 1)
    assert "gibt es nicht mehr" in verworfene(ordner).pop().grund


def hook(ereignis, rolle=None, befehl=""):
    return HookEingabe.aus(
        {
            "hook_event_name": ereignis,
            "agent_type": rolle,
            "tool_name": "Bash",
            "tool_input": {"command": befehl},
        }
    )


@pytest.mark.parametrize(
    "eingabe, löst",
    [
        pytest.param(hook("SubagentStart", "planer"), True, id="Rollenstart"),
        pytest.param(
            hook("PreToolUse", None, "git commit -m x"), True, id="Commit des Koordinators"
        ),
        pytest.param(
            hook("PreToolUse", "planer", "git commit -m x"), False, id="Commit einer Rolle"
        ),
        pytest.param(hook("PreToolUse", None, "git status"), False, id="anderer Befehl"),
        pytest.param(
            hook("PreToolUse", None, "cd /tmp/x && git add a && git commit -m y"),
            True,
            id="Commit nach cd und add",
        ),
        pytest.param(
            hook("PreToolUse", "planer", "cd x && git commit -m y"),
            False,
            id="verketteter Commit einer Rolle",
        ),
        pytest.param(hook("PreToolUse", None, "echo git commit"), False, id="nur erwähnt"),
    ],
)
def testDieÜbernahmeLöstNurBeiRollenstartUndCommitAus(eingabe, löst):
    assert löstAus(eingabe) is löst
