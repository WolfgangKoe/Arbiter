"""Hook `PreToolUse` auf `SubagentHandback`: Schlussantworten nennen nur Status und Pfade."""

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung

höchstlänge = 800


def grund(länge: int) -> str:
    return (
        f"Schlussantwort hat {länge} Zeichen, höchstens {höchstlänge}. Inhalte, Fragen und "
        "Empfehlungen gehören in eine Datei in handoff/; hier nur Status und Pfade."
    )


def entscheide(daten: dict) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    if not eingabe.rolle:
        return None
    # Warum: Im Headless-Lauf ruft die Rolle `SubagentHandback` nicht auf; dort gilt `SubagentStop`.
    if eingabe.ereignis == "SubagentStop":
        bericht = eingabe.letzteAntwort
        if len(bericht) <= höchstlänge or eingabe.stoppWiederholt:
            return None
        return {"decision": "block", "reason": grund(len(bericht))}
    if eingabe.werkzeug != "SubagentHandback":
        return None
    bericht = eingabe.angaben.get("message", "")
    if len(bericht) <= höchstlänge:
        return None
    return verweigerung(grund(len(bericht)))


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen()))
