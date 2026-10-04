"""Hook `PreToolUse` auf `SubagentHandback`: Schlussantworten nennen nur Status und Pfade."""

from gemeinsam.hookProtokoll import antwortAusgeben, eingabeLesen, verweigerung, werkzeugAngaben

höchstlänge = 800


def grund(länge: int) -> str:
    return (
        f"Schlussantwort hat {länge} Zeichen, höchstens {höchstlänge}. Inhalte, Fragen und "
        "Empfehlungen gehören in eine Datei in handoff/; hier nur Status und Pfade."
    )


def entscheide(eingabe: dict) -> dict | None:
    if not eingabe.get("agent_type"):
        return None
    # Warum: Im Headless-Lauf ruft die Rolle `SubagentHandback` nicht auf; dort gilt `SubagentStop`.
    if eingabe.get("hook_event_name") == "SubagentStop":
        bericht = eingabe.get("last_assistant_message") or ""
        if len(bericht) <= höchstlänge or eingabe.get("stop_hook_active"):
            return None
        return {"decision": "block", "reason": grund(len(bericht))}
    if eingabe.get("tool_name") != "SubagentHandback":
        return None
    bericht = werkzeugAngaben(eingabe).get("message", "")
    if len(bericht) <= höchstlänge:
        return None
    return verweigerung(grund(len(bericht)))


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen()))
