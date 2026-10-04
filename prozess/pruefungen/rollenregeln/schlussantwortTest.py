from rollenregeln import schlussantwort


def handback(text, rolle="planer"):
    return {"agent_type": rolle, "tool_name": "SubagentHandback", "tool_input": {"message": text}}


def stopp(text, *, aktiv=False):
    return {
        "hook_event_name": "SubagentStop",
        "agent_type": "regelumsetzer",
        "last_assistant_message": text,
        "stop_hook_active": aktiv,
    }


def testLangeSchlussantwortWirdZurückgeschickt():
    antwort = schlussantwort.entscheide(handback("x" * 4714))
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testKurzeSchlussantwortMitPfadenGehtDurch():
    assert schlussantwort.entscheide(handback("Fertig: handoff/anliegen/09-x.md")) is None


def testOhneRollePrüftDerHookDieSchlussantwortNicht():
    assert schlussantwort.entscheide(handback("x" * 5000, rolle=None)) is None


def testLangeLetzteNachrichtSchicktDieRolleZurück():
    assert schlussantwort.entscheide(stopp("x" * 2246))["decision"] == "block"


def testBeimZweitenStoppWirdNichtErneutGesperrt():
    assert schlussantwort.entscheide(stopp("x" * 2246, aktiv=True)) is None


def testEinAndererWerkzeugaufrufWirdNichtGeprüft():
    eingabe = {**handback("x" * 4714), "tool_name": "Read"}
    assert schlussantwort.entscheide(eingabe) is None
